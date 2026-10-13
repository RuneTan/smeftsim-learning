# Install the Linux environment

[English](README.md) | [简体中文](README.zh-CN.md)

This is the only installation guide needed before the [handbook](../../handbook.md).
The repository contains teaching notes and a locally generated example, rather than a preinstalled simulator.
You will obtain the software directly from its upstream repositories and prepare **one project directory, `~/smeftsim`, with one Python environment, `.venv`**.

The tested platform is x86-64 Ubuntu 22.04, Python 3.10, MadGraph 2.9.27, the tutorial's SMEFTsim v3.0.2 model, and ROOT 6.40.00.
The pinned versions are for this lesson; they are not claims about the latest releases.
If your existing installation already passes Section 6, skip installation and continue with the handbook.

**Input rule:** each line in a PowerShell or Bash block is a complete command. Finish the line, press Enter once, and wait for the prompt before entering the next line. Do not type displayed prompts. If a command fails, resolve it before continuing.

## 1. Create a dedicated Linux environment

Already using a dedicated x86-64 Ubuntu 22.04 virtual machine? Start at Section 2.
For Windows 10/11, the following route creates a WSL2 distribution named `SMEFTsim`, separate from any other Ubuntu installation.
WSL2 runs Linux in a lightweight virtual machine; its virtual disk remains on Windows, while calculations and project files live inside Linux.

**Windows PowerShell, run as administrator:**

```powershell
wsl --install --no-distribution
```

If prompted to restart Windows, restart before continuing. If WSL is already installed, skip this command.
Then use ordinary **Windows PowerShell**, one complete command at a time:

```powershell
wsl --list --verbose
```

If `SMEFTsim` already exists, enter it and check the existing installation; do not import over it.
For a new installation, download Canonical's Ubuntu 22.04 x86-64 root filesystem and its checksum list:

```powershell
$smeftDiskDir = "$env:USERPROFILE\SMEFTsim-WSL"
$smeftImage = "$env:TEMP\ubuntu-jammy-smeftsim.rootfs.tar.gz"
$smeftChecksums = "$env:TEMP\ubuntu-jammy-smeftsim-SHA256SUMS"
curl.exe --fail --location --output "$smeftImage" https://cloud-images.ubuntu.com/wsl/jammy/current/ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz
curl.exe --fail --location --output "$smeftChecksums" https://cloud-images.ubuntu.com/wsl/jammy/current/SHA256SUMS
(Get-FileHash -Algorithm SHA256 -LiteralPath "$smeftImage").Hash
Select-String -LiteralPath "$smeftChecksums" -Pattern 'ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz'
```

The two SHA256 values must match, ignoring letter case. These are commands in the same PowerShell session, so keep the variables defined above.
Then import and enter the new distribution:

```powershell
wsl --import SMEFTsim "$smeftDiskDir" "$smeftImage" --version 2
wsl -d SMEFTsim -u root
```

You are now at **Linux Bash as root**. Create the normal user used in this guide:

```bash
adduser smeft
usermod -aG sudo smeft
exit
```

`adduser` asks for a new Linux password twice; characters are not displayed. At the optional name/contact questions, press Enter to leave them blank, then confirm the details. Wait for each command to finish.
`exit` returns to PowerShell. Enter the normal user's Linux session:

```powershell
wsl -d SMEFTsim -u smeft --cd ~
```

Use this command whenever you return to the lesson. It specifies the user explicitly, so no default-user configuration is needed.
The directory `$smeftDiskDir` stores the virtual disk; preserve it. The downloaded image is an installer, not the installed disk.
Sources: [Microsoft WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install), [WSL import and user commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands), and [Canonical's Ubuntu images](https://cloud-images.ubuntu.com/wsl/jammy/current/).

## 2. Install prerequisites inside this Linux environment

**Linux Bash as the normal user:**

```bash
uname -m
cat /etc/os-release
whoami
```

Expect `x86_64`, Ubuntu `22.04`, and `smeft` (or your chosen normal username).
System packages below are installed only in this dedicated Linux environment. Python packages will go into the project's `.venv`; Windows Python and Anaconda are not used.

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3 python3-venv python3-dev build-essential gfortran git perl ca-certificates coreutils sed gzip unzip nano libsm6 libice6 libx11-6 libxext6 libxrender1 libxft2 libglu1-mesa
python3 -c "import sys; print(sys.version); assert sys.version_info[:2] == (3, 10), 'Use Ubuntu 22.04 / Python 3.10 for this lesson'"
```

Enter your Linux password if `sudo` asks. The Python check must finish without an assertion error.
`build-essential` supplies GCC and Make; `gfortran` compiles the generator's Fortran code. The `lib...` packages supply ROOT graphics libraries. `nano` is a terminal text editor.

## 3. Obtain the teaching notes and pinned software

Keep the project on the Linux filesystem, under your home directory, rather than `/mnt/c`.
Run the following only for a new installation; if a destination exists, inspect it instead of cloning over it.

```bash
cd ~
git clone https://github.com/RuneTan/smeftsim-learning.git smeftsim
cd ~/smeftsim
mkdir -p tools work/Material reference outputs
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
git -C tutorial rev-parse HEAD
git -C tools/MG5_aMC_v2_9_27 rev-parse HEAD
test -L tools/MG5_aMC_v2_9_27/madgraph/VERSION
```

The two hashes must match those above. “Detached HEAD” means the downloads are fixed to the recorded versions; it is expected.
The last command quietly succeeds when MadGraph's Linux symbolic link is intact.
The tutorial already supplies the required SMEFTsim UFO and its restriction, so a separate SMEFTsim model download is not needed for this exercise.

Prepare a working copy and turn off MadGraph's update checks for this pinned checkout:

```bash
cp -an tutorial/Material/. work/Material/
printf 'auto_update = 0\n' > tools/MG5_aMC_v2_9_27/input/mg5_configuration.txt
```

`cp -a` preserves the files and `-n` keeps existing destination files. Keep `tutorial` as the downloaded original; edit cards only in `work/Material`.
The configuration command is for a new checkout: it replaces that file's contents. Preserve a customized configuration if you already have one.

## 4. Create the single Python environment

From `~/smeftsim`, enter one complete command at a time:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --index-url https://pypi.org/simple -r docs/setup/requirements.txt
python -m pip check
```

The small [requirements file](requirements.txt) pins NumPy, six, setuptools and the Linux ROOT wheel. ROOT's PyPI packaging is marked alpha; this lesson uses the locally tested wheel version `0.1a12`, which contains ROOT `6.40.00`.
See [ROOT's Python interface documentation](https://root.cern.ch/doc/master/group__Python.html) for the PyPI distribution and [ROOT installation options](https://root.cern/install/).
Do not use `sudo pip` or install these packages into Windows Python.

## 5. Prepare the two Python 3 analysis scripts

Obtain these scripts from the tutorial downloaded in Section 3. The teaching repository provides the following conversion instructions, rather than redistributing the script files.
Run the commands only if the two Python 3 working copies are absent; `>` would otherwise replace them.
Keep `.venv` activated and stay in `~/smeftsim`:

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
python -m py_compile work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

These changes expand tabs, convert Python 2 syntax, replace `file()` with `open()`, and update the interpreter line. The algorithms and upstream originals are preserved. Python 3.10 supplies `lib2to3`; Python 3.14 does not.
The final command checks syntax and normally returns quietly.

| Script | Complete call from the project root | Function |
|---|---|---|
| Analyzer | `python work/Material/pyroot_python3/lhe_analyzer.py INPUT.lhe OUTPUT.root` | Reads momenta and weights, fills four distributions per weight, and normalizes by the event count |
| Plotter | `python work/Material/pyroot_python3/plot_histos.py INPUT.root` | Writes four PDF plots into the current directory, showing individual contributions added to the SM and their ratios |

The analyzer needs **two script arguments**, the plotter **one**. Include every argument before pressing Enter.

## 6. Check installation and reproduce the supplied example

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
python -m pip check
gfortran --version
```

Expect Python 3.10, a Python path under your `~/smeftsim/.venv`, ROOT `6.40.00`, no broken requirements, and a compiler version.
Then verify the analysis chain using the included 2,000-event example:

```bash
mkdir -p outputs/example_reweighted
gzip -dc examples/reweighted/events.lhe.gz > outputs/example_reweighted/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/example_reweighted/events.lhe outputs/example_reweighted/histograms.root
cd outputs/example_reweighted
python ../../work/Material/pyroot_python3/plot_histos.py histograms.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
cd ../..
```

Expect `processed 2000 events`, 48 ROOT histograms, and four nonempty PDFs. The commands write local outputs, leaving the supplied example unchanged.
To view the folder from WSL, run `explorer.exe .` in the output directory; in a Linux desktop, use its file manager.
This checks installation and analysis. Event generation and reweighting are exercised separately in handbook Sections 8–9.

## 7. Extract the reference results and continue

The pinned tutorial includes a results archive. Extract it locally for handbook Section 6:

```bash
cd ~/smeftsim
unzip -n tutorial/SMEFTsim_tutorial_results.zip -d reference
ls -lh reference/Results/Root_files/Hvlvl_SM_run_01.root
ls -lh reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz
```

Expect two nonempty files. The archive has a top-level `Results` directory; `-n` keeps existing extracted files.
All reference paths in the handbook now refer to this Linux directory.

| Directory created locally | Contents |
|---|---|
| `.venv` | Shared Python, generator dependencies and ROOT |
| `tutorial` | Pinned original tutorial, including UFO, input cards, scripts and reference archive |
| `tools` | Pinned MadGraph source and executable entry points |
| `work/Material` | Editable cards, Python 3 analysis copies and generated processes/runs |
| `reference` | Extracted upstream reference results |
| `outputs` | Your analysis outputs, decompressed copies, ROOT files and plots |

These directories are created during installation or use and are ignored by Git. They are not empty placeholders shipped in the teaching repository.
The repository itself retains the handbook, topic notes, example results, and source/license records.
No Windows source checkout or second Python environment is needed.

Continue at [handbook Section 5](../../handbook.md#5-start-the-environment-and-check-dependencies), then follow Sections 6, 8 and 9.
For the meaning and provenance of the included results, see the [example guide](../../examples/reweighted/README.md).
