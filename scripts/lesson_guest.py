"""Stage the user's decay samples and reweight a separate process copy."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PROCESSES = {
    "sm": "Hvlvl_SM", "linear": "Hvlvl_SMEFT_linear",
    "square": "Hvlvl_SMEFT", "prop": "Hvlvl_SMEFT_prop",
}
TARGETS = {
    "linear": ("lesson_cHl3_linear", "NPprop=0 NP=1 NP^2==1"),
    "square": ("lesson_cHl3_sq", "NPprop=0 NP==1"),
    "prop": ("lesson_cHl3_propW", "NP=0 NPprop=2 NPprop^2==2"),
}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_run(material, role, requested):
    directory = material / PROCESSES[role] / "Events"
    if requested:
        if Path(requested).name != requested or requested in {".", ".."}:
            raise ValueError("Run name must be a single directory name")
        candidates = [directory / requested]
    else:
        candidates = sorted(p for p in directory.iterdir() if p.is_dir()
                            and not p.name.startswith("smoke_")
                            and (p / "unweighted_events.lhe.gz").is_file())
    if len(candidates) != 1:
        raise ValueError(f"Choose --{role}-run explicitly; found {[p.name for p in candidates]}")
    path = candidates[0] / "unweighted_events.lhe.gz"
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def header(path):
    lines = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            if line.strip().startswith("<event>"):
                break
            lines.append(line)
    return "".join(lines)


def first_weight_ids(path):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        inside = False
        lines = []
        for line in stream:
            if line.strip() == "<event>":
                inside = True
            elif inside and line.strip() == "</event>":
                return set(re.findall(r"<wgt\s+id=['\"]([^'\"]+)", "".join(lines)))
            elif inside:
                lines.append(line)
    raise ValueError("No complete event")


def copy_input(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination / "events.lhe.gz")
    for banner in source.parent.glob("*banner.txt"):
        shutil.copy2(banner, destination / banner.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["prepare", "reweight"], required=True)
    parser.add_argument("--project", type=Path, default=Path("/home/smeft/smeftsim"))
    parser.add_argument("--output", type=Path, required=True)
    for role in PROCESSES:
        parser.add_argument(f"--{role}-run")
    args = parser.parse_args()
    material = args.project / "work/Material"
    sources = {role: find_run(material, role, getattr(args, f"{role}_run"))
               for role in PROCESSES}
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {role: {"source": str(path), "run": path.parent.name,
                       "sha256": sha(path)} for role, path in sources.items()}
    for role, path in sources.items():
        copy_input(path, args.output / "inputs" / role)
    (args.output / "sources.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Copied original samples; original event files were not modified.", flush=True)
    if args.stage == "prepare":
        return

    validation_path = args.output / "direct_report.json"
    if not validation_path.is_file():
        raise ValueError("Run the direct comparison first so the source cards and normalization are checked")
    validated = json.loads(validation_path.read_text(encoding="utf-8"))["samples"]
    for role, record in manifest.items():
        if validated[role]["sha256"] != record["sha256"]:
            raise ValueError("A source sample changed; rerun the direct comparison before reweighting")

    original = sources["sm"]
    original_hash = sha(original)
    clone = material / "Hvlvl_SM_reweight_lesson"
    state_path = clone / "lesson_source.json"
    expected = {"source": str(original), "sha256": original_hash}
    if clone.exists() and not state_path.exists():
        if clone.resolve().parent != material.resolve() or clone.is_symlink():
            raise ValueError("Unexpected lesson copy path")
        preserved = clone.with_name(clone.name + "_incomplete_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
        clone.rename(preserved)
        print(f"Preserved an incomplete copy at {preserved}", flush=True)
    if clone.exists():
        if not state_path.is_file() or json.loads(state_path.read_text()) != expected:
            raise ValueError("An existing lesson copy belongs to another source. Inspect it before continuing.")
    else:
        # Previous reweight caches contain disposable and sometimes dangling links.
        # Preserve normal model links and regenerate all reweight code in the copy.
        shutil.copytree(material / PROCESSES["sm"], clone, symlinks=True,
                        ignore=shutil.ignore_patterns("rw_me", "rw_me_*"))
        state_path.write_text(json.dumps(expected, indent=2), encoding="utf-8")
    target = clone / "Events" / original.parent.name / original.name
    logdir = args.output / "reweight_logs"
    logdir.mkdir(exist_ok=True)
    environment = os.environ.copy()
    environment["PATH"] = str(args.project / ".venv/bin") + os.pathsep + environment.get("PATH", "")
    for role, (weight_id, orders) in TARGETS.items():
        if weight_id in first_weight_ids(target):
            print(f"Already present: {weight_id}", flush=True)
            continue
        card = (f"change process h > e- ve~ mu+ vm SMHLOOP=0 {orders}\n"
                f"launch --rwgt_name={weight_id}\n"
                "set cHbox 0\nset cHW 0\nset cHl3 1\nset cHq3 0\nset cll1 0\n"
                "set LambdaSMEFT 1000\ndone\n")
        card_path = clone / "Cards/reweight_card.dat"
        card_path.write_text(card, encoding="utf-8")
        (logdir / f"{role}_card.dat").write_text(card, encoding="utf-8")
        print(f"Computing {weight_id} on the existing SM events ...", flush=True)
        with (logdir / f"{role}.log").open("w", encoding="utf-8") as log:
            result = subprocess.run([str(clone / "bin/madevent"), "reweight", original.parent.name, "-f"],
                                    cwd=material, env=environment, stdout=log, stderr=subprocess.STDOUT)
        text = (logdir / f"{role}.log").read_text(encoding="utf-8", errors="replace")
        if result.returncode or re.search(r"Traceback|Error detected|InvalidCmd|Command .* interrupted", text, re.I):
            raise RuntimeError(f"Reweighting failed: see {logdir / f'{role}.log'}")
        if weight_id not in first_weight_ids(target):
            raise RuntimeError(f"Missing weight {weight_id}; see reweight log")
    if sha(original) != original_hash:
        raise RuntimeError("Original SM LHE changed unexpectedly")
    copy_input(target, args.output / "inputs/reweighted")
    report = {"original_sm_sha256": original_hash, "original_sm_unchanged": True,
              "lesson_process": str(clone), "reweighted_sha256": sha(target),
              "expected_weight_ids": [value[0] for value in TARGETS.values()]}
    (args.output / "reweight_execution.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Three weights exported. Original SM sample checksum is unchanged.", flush=True)


if __name__ == "__main__":
    main()
