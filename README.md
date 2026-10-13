# SMEFTsim Learning Tutorial

[English](README.md) | [简体中文](README.zh-CN.md)

An independent bilingual tutorial for SM event generation, ROOT analysis and SMEFT reweighting of a four-lepton Higgs decay using SMEFTsim and MadGraph.
The repository provides a handbook, topic notes and locally generated example results. Obtain the runtime software directly from upstream and install it inside Linux.

**First visit: follow the [installation guide](docs/setup/README.md), then the [handbook](handbook.md).**
The installation guide connects dedicated WSL2/Ubuntu creation, pinned downloads, one `.venv`, analysis-script preparation and installation checks.
All operations use one Linux project directory; no Windows project checkout or directory-by-directory setup is needed.

| Reading entry point | Purpose |
|---|---|
| [Installation](docs/setup/README.md) | Create Linux, obtain pinned software and check the example |
| [Handbook](handbook.md) | Reference plots → your own SM sample → ROOT → reweighting comparisons |
| [Topic notes](docs/README.md) | Consult physics, models, orders, parameters, figures or Linux basics as needed |
| [Example results](examples/reweighted/README.md) | 2,000 events, 11 extra weights, ROOT histograms and PDFs |
| [Sources and licenses](THIRD_PARTY_NOTICES.md) | Provenance and license scope of the software, tutorial and repository material |

![Reweighted distribution from the locally generated sample](docs/figures/rw_mmv.png)

The figure uses local events and `plot_histos.py` from Ilaria Brivio's 2023 tutorial, retaining the original axis labels.
This process measures a decay width; the old `pb` label is explained in the [figure guide](docs/figures/README.md).

## Sources and acknowledgments

| Project or resource | Authors or maintainers | Use in this project |
|---|---|---|
| [SMEFTsim tutorial index](https://smeftsim.github.io/tutorials.html) | SMEFTsim project | Learning route |
| [2023 Higgs-decay tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) | Ilaria Brivio | Processes, cards, UFO, analysis and plotting methods; pinned commit `92ffde994d7c0d90554ee629cc477ee171c76b84` |
| [SMEFTsim](https://github.com/SMEFTsim/SMEFTsim) | Ilaria Brivio, Yun Jiang, Michael Trott and other contributors | Tutorial model v3.0.2 and model documentation |
| [MadGraph5_aMC@NLO](https://github.com/mg5amcnlo/mg5amcnlo) | MadTeam | Generator 2.9.27; pinned commit `eb76cab72b8d44aac7162ac7221ac08a4384a169` |
| [ROOT / PyROOT](https://root.cern/) | ROOT team | Histogram access and plotting |
| [SMEFTsim 3.0 — a practical guide](https://arxiv.org/abs/2012.11343) | Ilaria Brivio | Theory, parameters and model implementation |
| [The SMEFTsim package, theory and tools](https://arxiv.org/abs/1709.06492) | I. Brivio, Y. Jiang and M. Trott | Theory and tools of the original package |
| [Warsaw basis](https://arxiv.org/abs/1008.4884) | B. Grzadkowski, M. Iskrzyński, M. Misiak and J. Rosiek | Operator-basis reference |
| [PDG Kinematics](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf) | Particle Data Group | Widths, phase space and kinematics |
| [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install) | Microsoft | Dedicated Linux environment |

These notes are an independent learning aid. Model, generator and tutorial credits are listed above;
this project does not imply endorsement by those projects or contributors.
For scientific publications, follow the citation requirements of the tools you use.

## What the repository contains

The public repository retains documentation, figures, the parameter index, example data and source/license records.
MadGraph, ROOT, the UFO, original tutorial and Python 3 script copies are obtained or prepared locally during Linux installation; they are not bundled here.
`.venv`, `tutorial`, `tools`, `work`, `reference` and `outputs` are local runtime directories created by installation or exercise commands and ignored by Git.

The example in `examples/reweighted` was generated locally, rather than copied from the upstream reference results.
Its public LHE is an analysis export preserving numerical initialization data, events and weights while omitting full software templates and card text. Settings and checksums are recorded in `metadata.json`.
The SMEFTsim model's MIT license does not automatically cover the independent tutorial or this entire teaching repository.
No project-wide reuse license has been selected for the project-owned documentation; third-party licenses and attribution are recorded in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).
