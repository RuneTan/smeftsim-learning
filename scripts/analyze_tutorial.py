"""Analyze the author's decay samples with Python 3; never generate events."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile

os.environ["MPLCONFIGDIR"] = str(Path(__file__).resolve().parents[1] / "outputs/.matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import uproot

BASE = Path(__file__).resolve().parents[1]
OBS = {
    "mll": (np.linspace(0, 125, 26), r"$m_{e\mu}$ [GeV]"),
    "mmv": (np.linspace(0, 125, 26), r"$m_{\mu\nu_\mu}$ [GeV]"),
    "pTl1": (np.linspace(0, 64, 17), r"$p_T^{\ell_1}$ [GeV]"),
    "pTmu": (np.linspace(0, 64, 17), r"$p_T^\mu$ [GeV]"),
}
SAMPLES = ("Hvlvl_SM", "Hvlvl_SMEFT", "Hvlvl_SMEFT_linear", "Hvlvl_SMEFT_prop")
WGT = re.compile(r"<wgt\s+id=['\"]([^'\"]+)['\"]\s*>\s*([^<]+)</wgt>")


def extract_reference():
    archive = BASE / "tutorial/SMEFTsim_tutorial_results.zip"
    target = BASE / "reference"
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            name = entry.filename
            wanted = (
                name.endswith((".lhe.gz", "_banner.txt", ".root"))
                or name.startswith("Results/plot_") and name.endswith(".pdf")
            )
            if not wanted:
                continue
            path = (target / name).resolve()
            if not path.is_relative_to(target.resolve()):
                raise ValueError(f"Unsafe archive path: {name}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(z.read(entry))
    return archive


def number(value):
    return float(value.replace("D", "E").replace("d", "e"))


def events(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        lines = None
        for line in stream:
            stripped = line.strip()
            if stripped.startswith("<event>"):
                lines = []
            elif stripped == "</event>":
                if lines is None:
                    raise ValueError("Unmatched event end")
                yield parse_event(lines)
                lines = None
            elif lines is not None and stripped and not stripped.startswith("#"):
                lines.append(stripped)
        if lines is not None:
            raise ValueError("Incomplete last event")


def parse_event(lines):
    header = lines[0].split()
    count = int(header[0])
    weights = {"direct_sim": number(header[2])}
    particles = {}
    final = []
    incoming = []
    for line in lines[1:count + 1]:
        p = line.split()
        pdg, status = int(p[0]), int(p[1])
        vector = np.array([number(v) for v in p[6:10]])
        if status == 1:
            final.append(vector)
            if pdg in particles:
                raise ValueError("This analyzer expects a single particle per final-state PDG ID")
            particles[pdg] = vector
        elif status == -1:
            incoming.append(vector)
    if set(particles) != {11, -12, -13, 14}:
        raise ValueError(f"Expected e- ve~ mu+ vm, got {set(particles)}")
    for key, value in WGT.findall("\n".join(lines[count + 1:])):
        if key in weights:
            raise ValueError(f"Duplicate weight {key}")
        weights[key] = number(value)
    e, mu, nu = particles[11], particles[-13], particles[14]

    def mass(v):
        m2 = v[3] ** 2 - np.dot(v[:3], v[:3])
        if m2 < -1e-6:
            raise ValueError(f"Unphysical pair invariant mass squared: {m2}")
        return np.sqrt(max(0.0, m2))

    pt = lambda v: np.hypot(v[0], v[1])
    values = {"mll": mass(e + mu), "mmv": mass(mu + nu),
              "pTl1": max(pt(e), pt(mu)), "pTmu": pt(mu)}
    residual = np.max(np.abs(np.sum(incoming, axis=0) - np.sum(final, axis=0)))
    return values, weights, residual


def analyze(path):
    arrays = {name: [] for name in OBS}
    weight_rows = []
    keys = None
    max_residual = 0.0
    for values, weights, residual in events(path):
        if keys is None:
            keys = tuple(weights)
        if set(weights) != set(keys):
            raise ValueError("Weight IDs changed between events")
        row = [weights[k] for k in keys]
        if not np.all(np.isfinite(row)) or not np.all(np.isfinite(list(values.values()))):
            raise ValueError("Nonfinite event data")
        weight_rows.append(row)
        for name in OBS:
            arrays[name].append(values[name])
        max_residual = max(max_residual, residual)
    n = len(weight_rows)
    if not n:
        raise ValueError("No events")
    weights = np.asarray(weight_rows)
    histograms = {}
    for name, (edges, _) in OBS.items():
        # Include ROOT-style under/overflow; the uppermost edge is overflow.
        index = np.searchsorted(edges, arrays[name], side="right")
        sums = np.zeros((len(edges) + 1, len(keys)))
        np.add.at(sums, index, weights)
        histograms[name] = sums / n
    totals = {key: float(weights[:, i].mean()) for i, key in enumerate(keys)}
    summary = {
        "input": str(path), "event_count": n, "weight_ids": list(keys),
        "mean_weights_GeV": totals,
        "max_four_momentum_residual_GeV": float(max_residual),
        "negative_weight_counts": {key: int((weights[:, i] < 0).sum()) for i, key in enumerate(keys)},
        "normalization": "sum of event weights / event count; decay width in GeV",
    }
    if max_residual > 1e-6:
        raise ValueError(f"Four-momentum conservation failed: {max_residual} GeV")
    return histograms, summary


def verify_root(histograms, summary, root_path):
    checks = []
    keys = summary["weight_ids"]
    with uproot.open(root_path) as reference:
        for name, (edges, _) in OBS.items():
            for i, key in enumerate(keys):
                histogram_name = f"{name}_{key}"
                h = reference[histogram_name]
                np.testing.assert_allclose(h.axis().edges(), edges, rtol=0, atol=1e-12)
                expected = h.values(flow=True)
                actual = histograms[name][:, i]
                # The original TH1F accumulates in float32; tolerate rounding only.
                np.testing.assert_allclose(actual, expected, rtol=3e-4, atol=1e-13,
                                           err_msg=histogram_name)
                checks.append({"histogram": histogram_name,
                               "max_abs_bin_difference_GeV": float(np.max(np.abs(actual - expected)))})
    return checks


def draw(histograms, summary, outdir, sample_label):
    labels = summary["weight_ids"]
    contributions = [
        ("cHbox", "#9467bd", "-", "SM + cHbox linear"),
        ("cll1", "#17a2a4", "-", "SM + cll1 linear"),
        ("cHW", "#dd8c00", "-", "SM + cHW linear"),
        ("cHl3", "#d62728", "-", "SM + cHl3 linear"),
        ("cHl3_sq", "#d62728", "--", "SM + cHl3 quadratic"),
        ("cHl3_propW", "#d62728", ":", "SM + cHl3 propagator"),
    ]
    for name, (edges, xlabel) in OBS.items():
        h = histograms[name][1:-1]
        sm = h[:, labels.index("direct_sim")]
        widths = np.diff(edges)
        fig, (ax, ratio) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                                       gridspec_kw={"height_ratios": [1.35, 1]})
        ax.stairs(sm / widths, edges, baseline=None, color="black", lw=2, label="SM")
        ratio.axhline(1, color="black", lw=1)
        for key, color, style, legend in contributions:
            if key not in labels:
                continue
            target = sm + h[:, labels.index(key)]
            ax.stairs(target / widths, edges, baseline=None, color=color, ls=style, lw=1.6, label=legend)
            values = np.divide(target, sm, out=np.full_like(target, np.nan), where=sm != 0)
            ratio.stairs(values, edges, baseline=None, color=color, ls=style, lw=1.6)
        ax.set_yscale("log")
        ax.set_ylabel(r"$d\Gamma/dX$ [GeV / GeV]")
        ax.set_title(f"{sample_label}: {summary['event_count']:,} events")
        ax.legend(fontsize=8, ncols=2)
        ratio.set_ylabel(r"$(\mathrm{SM}+\mathrm{one\ term})/\mathrm{SM}$")
        ratio.set_xlabel(xlabel)
        for panel in (ax, ratio):
            panel.grid(alpha=0.2)
        fig.text(0.5, 0.012, "Each curve adds one contribution; it is not a complete EFT prediction. Central values only.",
                 ha="center", fontsize=8)
        fig.tight_layout(rect=(0, 0.04, 1, 1))
        fig.savefig(outdir / f"{name}.png", dpi=160)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lhe", type=Path, help="Analyze your own matching decay LHE file")
    parser.add_argument("--output", type=Path, help="Required with --lhe, keeps reference outputs separate")
    args = parser.parse_args()
    if args.lhe and not args.output:
        parser.error("--output is required with --lhe")
    outdir = args.output.resolve() if args.output else BASE / "outputs/reference_analysis"
    outdir.mkdir(parents=True, exist_ok=True)
    if args.lhe:
        histograms, summary = analyze(args.lhe.resolve())
        report = {"origin": "User-supplied LHE; not checked against author ROOT files", "samples": {"custom": summary}}
    else:
        archive = extract_reference()
        report = {"origin": "Official author-provided samples, not locally generated events",
                  "tutorial_commit": "92ffde994d7c0d90554ee629cc477ee171c76b84",
                  "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "samples": {}}
        for sample in SAMPLES:
            path = BASE / f"reference/Results/{sample}/Events/run_01/unweighted_events.lhe.gz"
            current, summary = analyze(path)
            summary["ROOT_checks"] = verify_root(current, summary,
                BASE / f"reference/Results/Root_files/{sample}_run_01.root")
            report["samples"][sample] = summary
            print(f"{sample}: {summary['event_count']} events; {len(summary['ROOT_checks'])} ROOT histograms verified")
            if sample == "Hvlvl_SM":
                histograms, sm_summary = current, summary
        summary = sm_summary
    sample_label = "User-supplied decay sample" if args.lhe else "SMEFTsim official reference sample"
    draw(histograms, summary, outdir, sample_label)
    (outdir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    with (outdir / "integrated_weights.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample", "weight_id", "mean_weight_GeV"])
        for sample, info in report["samples"].items():
            for key, value in info["mean_weights_GeV"].items():
                writer.writerow([sample, key, value])
    print(f"Plots and report: {outdir}")


if __name__ == "__main__":
    main()
