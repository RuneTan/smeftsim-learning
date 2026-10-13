"""Compare the four tutorial decay samples and their cHl3 reweights."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import re

from analyze_tutorial import OBS, events, plt, np

WEIGHT_IDS = {"linear": "lesson_cHl3_linear", "square": "lesson_cHl3_sq", "prop": "lesson_cHl3_propW"}
LABELS = {"linear": "vertex/input interference", "square": "dimension-6 square", "prop": "propagator interference"}


def card_values(text):
    match = re.search(r"<slha>\s*(.*?)</slha>", text, re.S | re.I)
    if not match:
        raise ValueError("Missing SLHA model parameters")
    block = None
    values = {}
    for line in match.group(1).splitlines():
        fields = line.split("#", 1)[0].split()
        if not fields:
            continue
        if fields[0].lower() == "block":
            block = fields[1].upper()
        elif fields[0].lower() == "decay":
            values[f"DECAY:{fields[1]}"] = float(fields[2])
            block = None
        elif block and not block.startswith("QNUMBERS") and len(fields) >= 2:
            values[f"{block}:{fields[0]}"] = float(fields[1].replace("D", "E"))
    return values


@dataclass
class Sample:
    path: Path
    role: str
    values: dict
    weights: dict
    init_rate: float
    init_error: float
    parameters: dict
    process: str
    seed: int
    run_settings: dict
    max_residual: float

    @property
    def n(self):
        return len(self.weights["direct_sim"])

    def moments(self, selected, observable=None):
        w = sum((self.weights[key] * factor for key, factor in selected.items()), np.zeros(self.n))
        norm = float(np.mean(np.abs(self.weights["direct_sim"])))
        if norm == 0:
            raise ValueError("Zero base normalization")
        if observable is None:
            mean = float(w.mean())
            variance = float(w.var(ddof=1) / self.n + (mean / norm * self.init_error) ** 2)
            return mean, variance
        edges = OBS[observable][0]
        indices = np.searchsorted(edges, self.values[observable], side="right")
        sums = np.bincount(indices, weights=w, minlength=len(edges) + 1)
        squares = np.bincount(indices, weights=w * w, minlength=len(edges) + 1)
        mean = sums / self.n
        variance = np.maximum(0, (squares - sums * sums / self.n) / (self.n * (self.n - 1)))
        variance += (mean / norm * self.init_error) ** 2
        return mean[1:-1], variance[1:-1]

    def entries(self, observable, selected=None):
        edges = OBS[observable][0]
        indices = np.searchsorted(edges, self.values[observable], side="right")
        if selected is None:
            return np.bincount(indices, minlength=len(edges) + 1)[1:-1]
        w = sum((self.weights[key] * factor for key, factor in selected.items()), np.zeros(self.n))
        absolute = np.bincount(indices, weights=np.abs(w), minlength=len(edges) + 1)
        squares = np.bincount(indices, weights=w * w, minlength=len(edges) + 1)
        effective = np.divide(absolute ** 2, squares, out=np.zeros_like(squares), where=squares > 0)
        return effective[1:-1]

    def metadata(self):
        rate, variance = self.moments({"direct_sim": 1})
        return {"input": str(self.path.resolve()), "role": self.role, "event_count": self.n,
                "sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(),
                "process": self.process, "seed": self.seed, "parameters": self.parameters,
                "mean_direct_width_GeV": rate, "init_width_GeV": self.init_rate,
                "init_integration_error_GeV": self.init_error,
                "approx_total_error_GeV": float(np.sqrt(variance)),
                "weight_ids": list(self.weights), "max_four_momentum_residual_GeV": self.max_residual}


def load(path, role):
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        header = []
        for line in stream:
            if line.strip().startswith("<event>"):
                break
            header.append(line)
    text = "".join(header)
    if "SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl" not in text:
        raise ValueError("Expected the tutorial's U35/MwScheme/Hvlvl model restriction")
    match = re.search(r"<init>\s*(.*?)</init>", text, re.S)
    if not match:
        raise ValueError("Missing init block")
    init = match.group(1).strip().splitlines()
    if int(init[0].split()[8]) != -4 or int(init[0].split()[9]) != 1:
        raise ValueError("Only this tutorial's IDWTUP=-4, single decay process is supported")
    rate, error = map(float, init[1].split()[:2])
    process = re.search(r"^generate\s+(.+)$", text, re.M).group(1).strip()
    settings = dict((name, " ".join(value.split())) for value, name in
                    re.findall(r"^\s*([^\n!=]+?)\s*=\s*(\w+)\s*(?:!|#)", text, re.M))
    if settings.get("event_norm") != "average":
        raise ValueError("Expected event_norm=average; do not apply sum(weights)/N to another convention")
    seed = int(settings["iseed"])
    parameters = card_values(text)
    arrays = {name: [] for name in OBS}
    rows = []
    keys = None
    max_residual = 0.0
    for values, weights, residual in events(path):
        if keys is None:
            keys = tuple(weights)
        if set(weights) != set(keys):
            raise ValueError("Weight IDs changed between events")
        row = [weights[key] for key in keys]
        if not np.all(np.isfinite(row)) or not np.all(np.isfinite(list(values.values()))):
            raise ValueError("Nonfinite event data")
        rows.append(row)
        for name in OBS:
            arrays[name].append(values[name])
        max_residual = max(max_residual, residual)
    if len(rows) < 2 or max_residual > 1e-6:
        raise ValueError("Incomplete sample or four-momentum conservation failure")
    weights = np.asarray(rows)
    sample = Sample(path, role, {name: np.asarray(value) for name, value in arrays.items()},
                    {key: weights[:, i] for i, key in enumerate(keys)}, rate, abs(error), parameters,
                    process, seed, settings, max_residual)
    mean, variance = sample.moments({"direct_sim": 1})
    if abs(mean - rate) > max(5 * np.sqrt(variance), abs(rate) * 3e-5, 1e-13):
        raise ValueError("Event weights and LHE init normalization disagree")
    return sample


def validate(samples):
    reference = samples["sm"]
    ignored_run = {"nevents", "iseed", "run_tag"}
    expected_orders = {
        "sm": {"NP=0", "NPprop=0"}, "linear": {"NP=1", "NP^2==1", "NPprop=0"},
        "square": {"NP==1", "NPprop=0"}, "prop": {"NP=0", "NPprop=2", "NPprop^2==2"},
    }
    for role, sample in samples.items():
        physical_role = "sm" if role == "reweighted" else role
        if not expected_orders[physical_role].issubset(set(sample.process.split())):
            raise ValueError(f"{role}: process orders do not match the expected contribution")
        if "SMHLOOP=0" not in sample.process.split():
            raise ValueError("This lesson excludes the effective SM Higgs loop vertices")
        if not sample.process.startswith("h > e- ve~ mu+ vm"):
            raise ValueError("Unexpected decay process")
        if sample.parameters.get("SMEFTCUTOFF:1") != 1000:
            raise ValueError("This lesson requires LambdaSMEFT=1000 GeV")
        if sample.parameters.get("SMEFT:22") != (0 if physical_role == "sm" else 1):
            raise ValueError(f"{role}: expected cHl3={'0' if physical_role == 'sm' else '1'}")
        for key in ("SMEFT:4", "SMEFT:7", "SMEFT:25", "SMEFT:30"):
            if sample.parameters.get(key) != 0:
                raise ValueError(f"{role}: another EFT coefficient is nonzero: {key}")
        for key, value in reference.parameters.items():
            if key == "SMEFT:22":
                continue
            if key not in sample.parameters or not np.isclose(value, sample.parameters[key], rtol=1e-9, atol=1e-14):
                raise ValueError(f"{role}: different model input {key}")
        for key, value in reference.run_settings.items():
            if key not in ignored_run and sample.run_settings.get(key) != value:
                raise ValueError(f"{role}: different run setting {key}")
    if len({samples[role].seed for role in expected_orders}) != 4:
        raise ValueError("Use distinct seeds for the four independent direct runs in this comparison")
    if "reweighted" in samples:
        rw = samples["reweighted"]
        if rw.n != reference.n or rw.seed != reference.seed:
            raise ValueError("Reweighting changed the base run identity")
        for name in OBS:
            if not np.allclose(rw.values[name], reference.values[name], rtol=0, atol=1e-12):
                raise ValueError("Reweighting changed event kinematics or event order")
        if not np.allclose(rw.weights["direct_sim"], reference.weights["direct_sim"], rtol=1e-10, atol=1e-14):
            raise ValueError("Reweighting changed original SM weights")
        missing = set(WEIGHT_IDS.values()) - set(rw.weights)
        if missing:
            raise ValueError(f"Missing lesson weights: {sorted(missing)}")


def direct_moments(samples, roles, observable=None):
    parts = [samples[role].moments({"direct_sim": 1}, observable) for role in roles]
    return sum(part[0] for part in parts), sum(part[1] for part in parts)


def plot_direct(samples, outdir, reweighted=False):
    outdir.mkdir(parents=True, exist_ok=True)
    def prediction(roles, observable):
        if not reweighted:
            return direct_moments(samples, roles, observable)
        selected = {("direct_sim" if role == "sm" else WEIGHT_IDS[role]): 1 for role in roles}
        return samples["reweighted"].moments(selected, observable)
    for name, (edges, xlabel) in OBS.items():
        sm, _ = prediction(["sm"], name)
        ratio_mask = (sm != 0) & (samples["sm"].entries(name) >= 10)
        widths = np.diff(edges)
        for kind in ("effects", "combined"):
            fig, (ax, ratio) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                                           gridspec_kw={"height_ratios": [2, 1]})
            curves = [("SM", ["sm"], "black")]
            if kind == "effects":
                curves += [("SM + vertex/input interference", ["sm", "linear"], "#d62728"),
                           ("SM + dimension-6 square", ["sm", "square"], "#1f77b4"),
                           ("SM + propagator interference", ["sm", "prop"], "#2ca02c")]
            else:
                curves += [("SM + both linear contributions", ["sm", "linear", "prop"], "#d62728"),
                           ("Above + dimension-6 square (selected terms)", ["sm", "linear", "prop", "square"], "#1f77b4")]
            for label, roles, color in curves:
                values, variance = prediction(roles, name)
                ax.stairs(values / widths, edges, color=color, baseline=None, label=label)
                if kind == "combined":
                    centers = (edges[1:] + edges[:-1]) / 2
                    ax.errorbar(centers, values / widths, yerr=np.sqrt(variance) / widths,
                                fmt="none", color=color, alpha=0.35, capsize=1)
                ratios = np.divide(values, sm, out=np.full_like(sm, np.nan), where=ratio_mask)
                ratio.stairs(ratios, edges, color=color, baseline=None)
            ax.set_ylabel(r"$d\Gamma/dX$ [GeV / GeV]")
            ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
            ax.legend(fontsize=8)
            ax.set_title(f"Your {'reweighted SM events' if reweighted else 'direct samples'}: cHl3=1, Lambda=1 TeV")
            ratio.set_ylabel("prediction / SM")
            ratio.set_xlabel(xlabel)
            ratio.axhline(1, color="grey", lw=0.8)
            for panel in (ax, ratio):
                panel.grid(alpha=0.2)
            note = "One term added at a time; ratio omitted for SM bins with fewer than 10 events." if kind == "effects" else "Approx. MC errors; ratio centers only, sparse SM bins omitted. Quadratic truncation is incomplete."
            fig.text(0.5, 0.015, note, ha="center", fontsize=8)
            fig.tight_layout(rect=(0, 0.045, 1, 1))
            fig.savefig(outdir / f"{name}_{kind}.png", dpi=150)
            plt.close(fig)


def plot_closure(samples, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    rw = samples["reweighted"]
    diagnostics = {}
    for name, (edges, xlabel) in OBS.items():
        widths = np.diff(edges)
        centers = (edges[1:] + edges[:-1]) / 2
        fig, axes = plt.subplots(3, 2, figsize=(12, 10), sharex=True)
        diagnostics[name] = {}
        for row, (role, weight_id) in enumerate(WEIGHT_IDS.items()):
            direct, dv = samples[role].moments({"direct_sim": 1}, name)
            reweighted, rv = rw.moments({weight_id: 1}, name)
            ax, pull_ax = axes[row]
            ax.errorbar(centers, direct / widths, yerr=np.sqrt(dv) / widths,
                        fmt="o", ms=3, color="#1f77b4", label=f"direct ({samples[role].n:,} events)")
            ax.errorbar(centers, reweighted / widths, yerr=np.sqrt(rv) / widths,
                        fmt="s", ms=2, color="#d62728", label=f"reweighted SM ({rw.n:,} events)")
            ax.set_title(LABELS[role])
            ax.set_ylabel(r"$d\Gamma_{term}/dX$ [GeV / GeV]")
            ax.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
            ax.legend(fontsize=8)
            denom = np.sqrt(dv + rv)
            direct_entries = samples[role].entries(name)
            effective_entries = rw.entries(name, {weight_id: 1})
            eligible = (denom > 0) & (direct_entries >= 10) & (effective_entries >= 10)
            pull = np.divide(reweighted - direct, denom, out=np.full_like(denom, np.nan), where=eligible)
            pull_ax.axhline(0, color="black", lw=1)
            pull_ax.axhline(3, color="grey", ls="--", lw=0.8)
            pull_ax.axhline(-3, color="grey", ls="--", lw=0.8)
            pull_ax.plot(centers, pull, "o", ms=3)
            pull_ax.set_ylabel("(reweight - direct) / approx. error")
            for panel in (ax, pull_ax):
                panel.grid(alpha=0.2)
            diagnostics[name][role] = {"max_abs_approx_bin_pull": float(np.nanmax(np.abs(pull))) if np.any(eligible) else None,
                                      "eligible_bin_count": int(eligible.sum()),
                                      "omitted_bin_count": int((~eligible).sum()),
                                      "direct_entries": direct_entries.tolist(),
                                      "reweighted_effective_entries": effective_entries.tolist(),
                                      "note": "Pull omitted below 10 direct or effective reweighted entries. Bin correlations are not modeled; not a formal global test."}
        for ax in axes[-1]:
            ax.set_xlabel(xlabel)
        fig.suptitle("Closure diagnostics: compare isolated contributions, including signed interference")
        fig.text(0.5, 0.012, "Approx. errors; pull omitted below 10 direct/effective entries. Reweights share the SM events.",
                 ha="center", fontsize=9)
        fig.tight_layout(rect=(0, 0.035, 1, 0.97))
        fig.savefig(outdir / f"{name}.png", dpi=150)
        plt.close(fig)
    return diagnostics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["direct", "closure"], required=True)
    parser.add_argument("--folder", type=Path, required=True)
    args = parser.parse_args()
    roles = ["sm", "linear", "square", "prop"] + (["reweighted"] if args.stage == "closure" else [])
    samples = {role: load(args.folder / "inputs" / role / "events.lhe.gz", role) for role in roles}
    validate(samples)
    plot_direct(samples, args.folder / "direct_plots")
    report = {"scope": "Your locally generated tutorial samples", "units": "GeV",
              "validation": "Process, model parameters, run settings, event data and normalization checked",
              "error_model": "Approximate independent-event sampling error plus LHE init integration error treated as a common normalization error. Bin covariance, unweighting/grid correlations and systematic uncertainties are not modeled.",
              "samples": {role: sample.metadata() for role, sample in samples.items()}, "totals": {}}
    text = ["# 本机四组样本比较", "", "参数：cHl3=1，LambdaSMEFT=1000 GeV；SM 基线 cHl3=0。", "",
            "负的线性贡献保留原符号。此报告的误差是近似 MC 误差，不是理论或实验系统误差。", "",
            "| 贡献 | 直接生成宽度 / GeV | 近似 MC 误差 / GeV | 重加权宽度 / GeV | 总量差 / 合并近似误差 |",
            "|---|---:|---:|---:|---:|"]
    for role in ["sm", "linear", "square", "prop"]:
        mean, variance = samples[role].moments({"direct_sim": 1})
        record = {"direct_GeV": mean, "direct_approx_error_GeV": float(np.sqrt(variance))}
        rw_text = pull_text = "—"
        if args.stage == "closure" and role in WEIGHT_IDS:
            rm, rv = samples["reweighted"].moments({WEIGHT_IDS[role]: 1})
            pull = (rm - mean) / np.sqrt(variance + rv)
            record.update({"reweighted_GeV": rm, "reweighted_approx_error_GeV": float(np.sqrt(rv)),
                           "approx_integrated_pull": float(pull)})
            rw_text, pull_text = f"{rm:.7e}", f"{pull:.2f}"
        report["totals"][role] = record
        text.append(f"| {role} | {mean:.7e} | {np.sqrt(variance):.3e} | {rw_text} | {pull_text} |")
    for label, roles_in_sum in {"SM_plus_linear": ["sm", "linear", "prop"],
                                "SM_plus_linear_plus_square": ["sm", "linear", "prop", "square"]}.items():
        mean, variance = direct_moments(samples, roles_in_sum)
        report["totals"][label] = {"direct_GeV": mean, "direct_approx_error_GeV": float(np.sqrt(variance))}
        if args.stage == "closure":
            selected = {"direct_sim": 1, WEIGHT_IDS["linear"]: 1, WEIGHT_IDS["prop"]: 1}
            if "square" in roles_in_sum:
                selected[WEIGHT_IDS["square"]] = 1
            rm, rv = samples["reweighted"].moments(selected)
            report["totals"][label].update({"reweighted_GeV": rm, "reweighted_approx_error_GeV": float(np.sqrt(rv)),
                                           "note": "Computed from event-level summed weights to retain correlation; not an independent test against the same SM base."})
        text.extend(["", f"{label}：{mean:.7e} ± {np.sqrt(variance):.3e} GeV。"])
    if args.stage == "closure":
        plot_direct(samples, args.folder / "reweighted_plots", reweighted=True)
        report["bin_diagnostics"] = plot_closure(samples, args.folder / "closure_plots")
        text.extend(["", "重加权保持原 SM 的事件运动学、事件顺序和基础权重。", "",
                     "closure 图逐项比较线性、平方、传播子贡献；不是把完整预测与单独修正混比。",
                     "三个重加权来自同一基础样本，组合误差按逐事件相加后计算，保留其相关性。",
                     "直接事件数或重加权有效事件数不足 10 的 bin 不显示 pull；SM 少于 10 事件的 bin 不显示比值。",
                     "bin pull 只是诊断：bin 间相关性及多次比较不允许据此作正式全局显著性结论。"])
    (args.folder / f"{args.stage}_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.folder / f"{args.stage}_summary.md").write_text("\n".join(text) + "\n", encoding="utf-8")
    print("\n".join(text))


if __name__ == "__main__":
    main()
