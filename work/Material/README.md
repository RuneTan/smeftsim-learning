# Processes, cards, and working copies of the author's materials

[English](README.md) | [简体中文](README.zh-CN.md)

| Local file or directory | Source and purpose |
|---|---|
| `SMEFTsim_U35_MwScheme_UFO` | Tutorial UFO: particles, parameters, vertices, and the restriction are read when importing the model |
| `Hvlvl_SM` | SM process, cards, compiled code, and events |
| `Hvlvl_SM_manual` | Your working copy for reweighting, preserving the original SM process |
| `Hvlvl_SMEFT*` | Previously exported processes for independent EFT contributions; the current learning route does not require rerunning them |
| `param_card_Hvlvl.dat` | The author's SM parameter starting point; copy to the process's `Cards/param_card.dat` |
| `run_card_Hvlvl.dat` | The author's run card; edit the event count and seed after copying |
| `reweight_card_int.dat` | Four parameter points for interference, with one coefficient varied at a time |
| `reweight_card_squares.dat` | Four parameter points for squared-amplitude contributions, with one coefficient varied at a time |
| `reweight_card_propW.dat` | Three parameter points for propagator/width contributions |
| `reweight_card_mix_*.dat` | Examples of mixed contributions involving multiple coefficients; optional for the current exercise |
| `launch_reweighting.sh` | The author's batch reweighting helper; check its default process and run names |
| `make_rootfiles.sh` | The author's batch decompression and analysis helper; its default run is `run_01` |
| `lhe_analyzer.py`, `plot_histos.py` | Original Python 2 analysis and plotting working copies |
| [pyroot_python3](pyroot_python3/README.md) | The two Python 3 compatibility copies actually called in the current Linux environment |

The original author files here come from the [tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23).
They are used locally with their provenance retained and are excluded from this project's publication scope.
Final events are in `Events/<run>/`; `SubProcesses` contains the generator's build and integration working files.
