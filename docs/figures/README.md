# Example plots

[English](README.md) | [简体中文](README.zh-CN.md)

These PNG files were made from this project's locally generated sample of 2,000 SM baseline events. Analysis and plotting use `lhe_analyzer.py` and `plot_histos.py` from [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23), as detailed below.

| Files | How they were made | Contents |
|---|---|---|
| `sm_mll.png`, `sm_mmv.png`, `sm_pTl1.png`, `sm_pTmu.png` | Fill histograms with `lhe_analyzer.py`, then call ROOT `Draw`/`SaveAs` | Pure SM contribution to the decay width in each bin |
| `rw_mll.png`, `rw_mmv.png`, `rw_pTl1.png`, `rw_pTmu.png` | Apply the plotting logic in `plot_histos.py` to the user's reweighted ROOT file | Compare the SM with individual EFT corrections |

The reweighting plots retain the style defined in `plot_histos.py`. Their historical `pb` labels do not apply to the Higgs decay in this example.
The actual bin content is `sum(weights)/N`, in GeV. The bin widths are 5 GeV for `mll` and `mmv`, and 4 GeV for the two transverse-momentum distributions.
To obtain a differential density, divide by the bin width as well.
The lower panels show ratios to the SM, which are unaffected by this unit convention.

`cHl3`, `cHl3_sq`, and `cHl3_propW` denote the linear, squared-amplitude, and propagator contributions, respectively.
`plot_histos.py` plots the SM plus one contribution at a time; it does not automatically sum all corrections.

These are central-value teaching plots without complete uncertainty bands. The example data and metadata are in
[examples/reweighted](../../examples/reweighted/README.md).
