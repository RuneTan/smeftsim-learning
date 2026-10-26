# Example plots

[English](README.md) | [简体中文](README.zh-CN.md)

These plots use this project's locally generated 2,000-event SM sample and its additional weights.
Histograms come from `lhe_analyzer.py`; both the SM-only and reweighted plots use a Python 3 copy of
Ilaria Brivio's [June 2023 tutorial `plot_histos.py`](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/plot_histos.py).
The setup guide applies `scripts/fix_axes.py` to correct local labels and layout; histogram calculations are unchanged. PDFs embed fonts with ROOT's `Print(..., "EmbedFonts")` and Ghostscript, so Greek letters do not depend on a viewer's substitute fonts. PNGs export the same ROOT canvases.

| Filename suffix | Horizontal axis | Definition |
|---|---|---|
| `mll` | $m(e,\mu)$ | Invariant mass of the electron–muon pair |
| `mmv` | $m(\mu,\nu_\mu)$ | Invariant mass of the muon and its neutrino, using generator momenta |
| `pTl1` | $p_T(l_1)$ | Leading charged-lepton transverse momentum: $\max(p_T(e),p_T(\mu))$ |
| `pTmu` | $p_T(\mu)$ | Muon transverse momentum |

`sm_*.png` show the SM alone in one panel. `rw_*.png` compare the SM with individual EFT corrections and include a ratio panel.
The vertical label is $\Gamma_{\mathrm{bin}}$ [GeV]: the bin content is `sum(weights)/N`, not a cross section in pb.
The bin widths are 5 GeV for `mll` and `mmv`, and 4 GeV for the two transverse-momentum distributions.
Divide by the bin width to obtain a differential width. The lower panels show dimensionless ratios to the SM.

`cHl3`, `cHl3_sq`, and `cHl3_propW` denote the linear, squared-amplitude, and propagator contributions, respectively.
Each colored curve adds one contribution to the SM; the plotter does not automatically sum all corrections.
These teaching plots show central values without complete uncertainty bands. Data and metadata are in
[examples/reweighted](../../examples/reweighted/README.md).
