# Set up a fresh clone

[English](README.md) | [简体中文](README.zh-CN.md)

Use this guide on a **new machine** before starting the [handbook](../../handbook.md). If your existing environment already generates events and imports ROOT, keep it and skip this setup.

The public repository contains teaching notes, helper scripts, and a selected example. It does not contain a virtual disk, a virtual environment, MadGraph, the tutorial download, or analysis scripts from [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23). The steps below obtain those dependencies locally and prepare the analysis scripts without redistributing them.

## 1. Starting requirements and the two directories

This guide starts inside a **dedicated, x86-64 Ubuntu 22.04 environment**, with a regular Linux user who can install distribution packages using `sudo`. Python 3.10 is the runtime used for the lesson.

For Windows, create the dedicated WSL2 environment first using Microsoft's [WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install) and, for a separately named distribution, its [distribution-import guide](https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro). Complete the Linux-user setup there before continuing. These are operating-system setup steps, outside the commands below.

| Directory | Role |
|---|---|
| `~/smeftsim-source` | Git checkout, teaching documents, selected example, and locally downloaded upstream source |
| `~/smeftsim` | Separate runtime directory containing `.venv`, working cards, generated processes, and outputs |

`~` means the current Linux user's home directory. The setup helper requires the source and runtime directories to be different, with the runtime on the Linux filesystem and its path containing no spaces. Do not clone the repository into `~/smeftsim` and then use that same directory as the setup target.

The handbook's original machine uses WSL distribution `SMEFTsim`, user `smeft`, and runtime `/home/smeft/smeftsim`. If your names differ, substitute your distribution, username, and home path in its access and File Explorer commands. Its physics and analysis steps are otherwise the same.

**Input rule:** every line in a Bash block below is one complete command. Enter the whole line, press Enter once, and wait for the Bash prompt to return before entering the next. Do not type the prompt itself.

Check your Linux environment:

```bash
uname -m
cat /etc/os-release
whoami
```

Expect `x86_64`, Ubuntu version `22.04`, and your normal Linux username. Continue in this dedicated environment, rather than Windows PowerShell or Git Bash.

## 2. Install the Linux prerequisites

These packages are installed **inside this dedicated Ubuntu distribution**. Python physics dependencies will subsequently go into the project's `.venv`. This step does not install Python packages into Windows Anaconda.

**Linux Bash: one complete command, one Enter, then wait.**

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3 python3-venv python3-dev build-essential gfortran git perl ca-certificates coreutils sed gzip unzip
python3 -c "import sys; print(sys.version); assert sys.version_info[:2] == (3, 10), 'This lesson requires Python 3.10'"
```

If `sudo` asks for your Linux password, type it and press Enter. Password characters are not displayed. `build-essential` supplies GCC and Make; `gfortran` supplies the Fortran compiler. `coreutils`, `sed`, `gzip`, and `unzip` supply the conversion and archive tools used below. APT and `dpkg-deb` are available in this Ubuntu environment and are also used by the setup helper.

The Python check must finish without an assertion error. If it reports another version, stop and prepare the Ubuntu 22.04/Python 3.10 environment before proceeding. See Ubuntu's [package-management documentation](https://ubuntu.com/server/docs/how-to/software/package-management/) for APT usage.

## 3. Clone the teaching repository and pinned upstream sources

Use these directory names for a fresh setup. If any target already exists, inspect it first rather than repeating `git clone` into it. The public repositories can be downloaded without putting a token in a command.

**Linux Bash: enter and finish each command separately.**

```bash
cd ~
git clone https://github.com/RuneTan/smeftsim-learning.git smeftsim-source
cd ~/smeftsim-source
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
git -C tutorial rev-parse HEAD
git -C tools/MG5_aMC_v2_9_27 rev-parse HEAD
```

The last two commands should print the respective pinned hashes above. A “detached HEAD” notice after `checkout` is expected: these downloads are fixed to the recorded versions. The tutorial includes the SMEFTsim v3.0.2 UFO and the reference-results archive.

Source and license records are in the [project README](../../README.md) and [third-party notices](../../THIRD_PARTY_NOTICES.md). Keep upstream downloads local; they remain excluded from this teaching repository's Git commits.

## 4. Prepare the separate Linux runtime

Still in `~/smeftsim-source`, run:

```bash
bash scripts/setup_linux.sh ~/smeftsim
```

Wait for `Environment prepared at ...` and the Bash prompt. This helper copies the tutorial and process cards, creates a Linux MadGraph checkout with the expected symbolic links, installs the pinned dependencies into `~/smeftsim/.venv`, and extracts two ROOT graphics libraries into that environment. It then prepares `work/Material`. It does not generate events.

The helper never invokes `sudo` and does not install into the global Python environment. On this fresh setup the runtime is new; on an existing installation the helper preserves existing working files, so it should not be treated as an automatic upgrade procedure.

Then enter and check the runtime:

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
python -m pip check
gfortran --version
```

Expect Python 3.10, a Python path under your `~/smeftsim/.venv`, ROOT `6.40.00`, and no broken requirements. Keep this environment activated for the following steps.

## 5. Create the local Python 3 analysis copies

A fresh public clone contains the analysis directory's guide, **not its two `.py` files**. Create them now from the downloaded originals, before calling either analyzer or plotting script.

**Run these conversion commands only when the two working scripts are absent.** From the activated runtime root `~/smeftsim`, enter one complete command at a time:

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
python -m py_compile work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

`>` writes a newly created working copy; it is part of the command. The upstream files in `tutorial/Material` are unchanged. These are Python 3 compatibility changes: expand indentation, convert old syntax, replace `file()` with `open()`, and update the interpreter line. Python 3.10 supplies `lib2to3` for this conversion; Python 3.14 does not.

The final command checks syntax and should return quietly. More explanation is in the [working-copy guide](../../work/Material/pyroot_python3/README.md).

## 6. Make the shared example available to the runtime

The helper does not copy the public examples into the runtime. From `~/smeftsim`, copy the selected example without overwriting existing files:

```bash
mkdir -p examples/reweighted
cp -an "$HOME/smeftsim-source/examples/reweighted/." examples/reweighted/
ls -lh examples/reweighted/events.lhe.gz examples/reweighted/histograms.root
```

Expect two nonempty files. `cp -a` preserves the copied files' attributes; `-n` keeps any existing destination file. On a fresh setup, the files are the repository's supplied example. If you already had a different example, inspect it separately rather than assuming this command replaced it.

Documents remain in `~/smeftsim-source` or on GitHub; the working commands run in `~/smeftsim`. You can now follow [the example's reanalysis and replot instructions](../../examples/reweighted/README.md).

## 7. Prepare the optional upstream reference results

For handbook section 6, extract the locally downloaded result archive into the **source checkout**, keeping existing extracted files:

```bash
mkdir -p "$HOME/smeftsim-source/reference"
unzip -n "$HOME/smeftsim-source/tutorial/SMEFTsim_tutorial_results.zip" -d "$HOME/smeftsim-source/reference"
ls -lh "$HOME/smeftsim-source/reference/Results/Root_files/Hvlvl_SM_run_01.root"
```

The archive contains a top-level `Results` directory. `-n` prevents overwriting previously extracted files. The last command should list a nonempty ROOT file.

The original handbook uses the publishing machine's Windows-mounted reference path. In this fresh Linux setup, use `$HOME/smeftsim-source/reference` instead of `/mnt/c/Users/符文/Desktop/NSBI/smeftsim/reference`.

For section 6.5 A3, use this complete command from the runtime root:

```bash
cd ~/smeftsim
mkdir -p outputs/my_pyroot_reference
gzip -dc "$HOME/smeftsim-source/reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz" > outputs/my_pyroot_reference/events.lhe
```

After the Bash prompt returns, continue at section 6.5 A4, which checks the decompressed file before analysis. Preserve both the `>` symbol and the output filename before pressing Enter.

For its optional shortcut using the existing ROOT file, first enter `outputs/my_pyroot_reference`, then use:

```bash
cd ~/smeftsim/outputs/my_pyroot_reference
python ../../work/Material/pyroot_python3/plot_histos.py "$HOME/smeftsim-source/reference/Results/Root_files/Hvlvl_SM_run_01.root"
```

This shortcut replaces the LHE-analysis route; it is not an additional required step.

## 8. Continue the lesson

Return to the activated runtime root and check model construction:

```bash
cd ~/smeftsim
bash scripts/run_generator.sh check_model
```

This constructs processes without generating events. Then follow the [handbook](../../handbook.md): section 6 for reference plots, or sections 8–9 for your own SM generation and reweighting. Substitute your home path and WSL names as described in section 1.

The historical Windows helpers `install-wsl-runtime.ps1` and `resume-install.ps1` expect locally prepared installers and a specific Ubuntu image in `vm/downloads`; those downloads are not published. `resume-install.ps1` also assumes that the local analysis scripts are available before its ROOT check. They are not the entry point for this fresh-clone route. This guide uses the existing setup helper and explicit manual conversion steps, rather than a new all-in-one program.
