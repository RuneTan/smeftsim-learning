# SMEFTsim Learning Project

[English](README.md) | [简体中文](README.zh-CN.md)

A personal learning and reproduction project using SMEFTsim, MadGraph and ROOT
to learn SM event generation, analysis and SMEFT reweighting of a four-lepton Higgs decay.
The project provides bilingual notes, an isolated environment, explicit terminal instructions,
helper commands and a locally generated example.

**Start with [handbook.md](handbook.md).** It contains the learning sequence and practical steps.
Background material, parameter explanations and directory guides are linked from it.
On a new machine, first follow the [fresh-clone setup guide](docs/setup/README.md).

| Entry point | Purpose |
|---|---|
| [Fresh-clone setup](docs/setup/README.md) | Download pinned dependencies and prepare the isolated runtime |
| [Handbook](handbook.md) | Generate an SM sample, use ROOT and perform reweighting |
| [Physics background](docs/physics/README.md) | Warsaw basis, flavor, input schemes and differential widths |
| [Software and notebooks](docs/model/README.md) | Roles of the model, generator and Mathematica |
| [Process cards](cards/README.md) | Model import, restrictions and NP/NPprop orders |
| [Helper scripts](scripts/README.md) | What each script does and which environment it uses |
| [Local reweighted example](examples/reweighted/README.md) | 2,000 events, 11 extra weights, ROOT histograms and PDFs |
| [Publishing and licensing](docs/publishing/README.md) | Attribution, upstream licenses and publishing from WSL |

![Reweighted distribution from this project's own sample](docs/figures/rw_mmv.png)

The figure uses locally generated events and the upstream plotting logic.
The upstream axis labels are retained. This process measures a decay width;
the old `pb` label is explained in the [figure guide](docs/figures/README.md).

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

These notes are a learning aid. The original models, tutorial and algorithms remain attributed
to their authors. This is an independent project and does not imply endorsement.
For scientific publications, cite the papers requested by the upstream projects.

## Publication and license scope

- The locally generated example is in `examples/reweighted`. Its versions, parameters and checksums are recorded in `metadata.json`.
- The public LHE is an analysis export: numerical initialization data, events and weights are preserved, while full software and card-template headers are omitted. The original run remains local.
- Third-party software, environments and downloaded tutorial materials are obtained upstream and are not bundled here.
- No explicit license was identified for the independent tutorial scripts. Local Python 3 copies remain usable but are excluded from Git.
- The parameter index uses the MIT-licensed SMEFTsim model; upstream license texts are retained in [licenses](licenses/README.md).

Attribution does not replace permission. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
Project-owned documentation and helper scripts do not yet have a project-wide reuse license.
Upstream licenses are not automatically licenses for this entire repository.
