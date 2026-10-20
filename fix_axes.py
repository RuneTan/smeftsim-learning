#!/usr/bin/env python3
"""Apply display-only fixes to the locally prepared June 2023 tutorial plotter."""
from pathlib import Path
import ast
import shutil

MARKER = "# Local axis-label and SM-only layout fixes; see docs/figures/README.md."
LABELS = {
    "mll": "m(e,#mu) [GeV]",
    "mmv": "m(#mu,#nu_{#mu}) [GeV]",
    "pTl1": "p_{T}(l_{1}) [GeV]",
    "pTmu": "p_{T}(#mu) [GeV]",
}


def finish_display(source):
    source = source.replace("#Delta#Gamma_{bin} [GeV]", "#Gamma_{bin} [GeV]")
    source = source.replace('canvas.SaveAs("plot_" + histo_key + ".pdf")',
                            'canvas.Print("plot_" + histo_key + ".pdf", "EmbedFonts")')
    source = source.replace("pad1.SetBottomMargin(0 if _has_ratio else 0.16)",
                            "pad1.SetBottomMargin(0.035 if _has_ratio else 0.16)")
    source = source.replace("pad2.SetTopMargin(0.0)", "pad2.SetTopMargin(0.04)")
    source = source.replace("h_toPlot[hk].GetXaxis().SetTitleSize(0.05)",
                            "h_toPlot[hk].GetXaxis().SetTitleSize(0 if _has_ratio else 0.05)\n"
                            "                   h_toPlot[hk].GetXaxis().SetLabelSize(0 if _has_ratio else 0.035)")
    return source


def main():
    root = Path(__file__).resolve().parent
    target = root / "work/Material/pyroot_python3/plot_histos.py"
    if not target.is_file():
        raise SystemExit("Prepare the Python 3 plotting copy using docs/setup first.")
    source = target.read_text()
    if not shutil.which("gs"):
        raise SystemExit("Install Ghostscript in the Linux environment first; see docs/setup. No file was changed.")
    if MARKER in source:
        updated = finish_display(source)
        if updated == source:
            print("Local plot labels, SM-only layout and PDF font embedding are already fixed.")
        else:
            ast.parse(updated)
            target.write_text(updated)
            print("Updated local plot labels, layout and embedded PDF fonts.")
        return
    tree = ast.parse(source)
    settings = next(node.value for node in ast.walk(tree)
                    if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "histo_dc" for t in node.targets))
    original = ast.literal_eval(settings)
    for name, xlabel in LABELS.items():
        oldx, oldy = original[name][:2]
        source = source.replace(repr(oldx), repr(xlabel))
        source = source.replace('"' + oldx + '"', repr(xlabel))
        source = source.replace(repr(oldy), repr("#Gamma_{bin} [GeV]"))
        source = source.replace('"' + oldy + '"', repr("#Gamma_{bin} [GeV]"))

    def replace_once(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise SystemExit("Unexpected plotting-copy layout; no file was changed.")
        source = source.replace(old, new)

    replace_once("    for histo_key in histo_dc:\n", "    for histo_key in histo_dc:\n"
                 "        _has_ratio = any(name.startswith(histo_key + '_')\n"
                 "                         and name[len(histo_key) + 1:] in weights_to_plot[1:]\n"
                 "                         and name[len(histo_key) + 1:] not in histo_dc[histo_key][-1]\n"
                 "                         for name in histos)\n")
    replace_once('"histo_pos",0., 0.45, 1, 1)', '"histo_pos",0., 0.45 if _has_ratio else 0., 1, 1)')
    replace_once("pad1.SetBottomMargin(0)", "pad1.SetBottomMargin(0 if _has_ratio else 0.16)")
    replace_once("leg = ROOT.TLegend(.8,.55,.95,.95)",
                 "leg = ROOT.TLegend(.8,.55,.95,.95) if _has_ratio else ROOT.TLegend(.7,.82,.95,.95)")
    replace_once("leg.SetTextSize(.035)", "leg.SetTextSize(.035 if _has_ratio else .025)")
    replace_once("        ratio = {}", "        if not _has_ratio:\n"
                 '            canvas.SaveAs("plot_" + histo_key + ".pdf")\n'
                 "            continue\n\n        ratio = {}")
    source = finish_display(source)
    ast.parse(source)
    backup = root / ".maintainer-notes/axes/plot_histos.before.py"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(target, backup)
    first, separator, rest = source.partition("\n")
    source = first + separator + MARKER + "\n" + rest if first.startswith("#!") else MARKER + "\n" + source
    target.write_text(source)
    print("Fixed local labels, SM-only layout and PDF font embedding; histogram values and upstream files are unchanged.")


if __name__ == "__main__":
    main()
