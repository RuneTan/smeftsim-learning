# Helper scripts

[English](README.md) | [简体中文](README.zh-CN.md)

The tutorial files read or copied by these helpers come from [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23).

For a new machine, use the [fresh-clone setup guide](../docs/setup/README.md).

This directory contains this project's environment, launch, and validation helpers. The SMEFTsim model is obtained separately.
The main learning route still involves editing cards by hand, responding to MadGraph menus, and calling `lhe_analyzer.py` and ROOT.

## Current workflow

| Script | Environment | Purpose | When to use it |
|---|---|---|---|
| `enter-linux.ps1` | Windows PowerShell | Enter the WSL distribution named `SMEFTsim` as user `smeft` | Daily access to the environment |
| `setup_linux.sh` | Linux Bash | Check system tools and prepare source files and the unified `.venv` in a separate Linux project directory | Initial environment setup |
| `prepare_work.py` | Project Python | Copy tutorial materials into `work/Material`, preserve existing files, and normalize shell-script line endings | Called automatically by the generator helper |
| `run_generator.sh` | Linux Bash | Activate the project environment, run MadGraph by stage, refuse to overwrite existing process directories, and inspect logs | `check_model`, `generate_sm`, and `generate_eft` |
| `validate_generated.py` | Project Python | Check events, final states, finite weights, four-momenta, and normalization; write a JSON report | Validation of the dedicated 2,000-event tutorial smoke sample |
| `validate_smoke.sh` | Linux Bash | Check small-sample generation and one reweighting contribution; reuse an existing smoke run when available | Environment validation; outside the main lesson |
| `inspect_parameters.py` | Python | Read UFO parameters and the tutorial input cards statically to generate an index | Refreshing the parameter reference |

## Windows installation helpers

| Script | Purpose | Prerequisite |
|---|---|---|
| `install-wsl-runtime.ps1` | Verify a local Microsoft installation package, install WSL, and enable the Virtual Machine Platform | Local installation package and administrator privileges |
| `bootstrap_guest.sh` | Install system dependencies and create user `smeft` in the dedicated Ubuntu environment | Called by the installation continuation helper |
| `resume-install.ps1` | Verify the local Ubuntu image, import the dedicated distribution, configure the environment, and run initial checks | Installation materials already prepared in `vm/downloads` |

These scripts retain the dedicated-distribution conventions used on the current machine. They require preparation and configuration on another computer.
On a new machine, first prepare the tools and materials described in the [environment guide](../vm/README.md).

## Earlier helpers

| File | Original purpose | Role in the current lesson |
|---|---|---|
| `analyze.ps1`, `analyze_tutorial.py` | Windows NumPy/Matplotlib analysis | Outside the ROOT learning route |
| `lesson.ps1`, `lesson_guest.py` | Automatically organize direct-generation and reweighting stages | Outside the manual learning route |
| `compare_lesson.py` | Automatically compare four directly generated samples with reweighted contributions | Optional; not required by the current lesson |

These files remain available to preserve existing entry points and imports. New learners can start with the current workflow.

## Example

**Linux Bash, from the project root: press Enter once after each complete line.**

```bash
source .venv/bin/activate
bash scripts/run_generator.sh check_model
```

This check constructs the model and processes without generating events. See [cards/README.md](../cards/README.md) for the physical meaning of the cards.
Results are written to `outputs`; see [outputs/README.md](../outputs/README.md) for that directory's contents.

`validate_generated.py` expects the fixed 2,000-event smoke sample, `IDWTUP=-4`, and the tutorial SM/cHl3-linear weight signs; it is not a general-purpose validator. `inspect_parameters.py` writes a scratch index and JSON under `outputs`; it does not replace the maintained bilingual reference in `docs/parameters`.
