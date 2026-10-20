# SMEFTsim Learning and Operations Handbook

[English](handbook.md) | [简体中文](handbook.zh-CN.md)

These practical notes follow [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23). The learning sequence is:
**understand SMEFT → read the reference plots → generate and plot your own SM sample → compare EFT contributions through reweighting.**

This handbook uses the Linux project's shared `.venv` environment and ROOT.
The authors' original material remains in `tutorial`; local analysis and plotting use Python 3-compatible copies.
The [root README](README.md) lists the sources and reading entry points; the [installation guide](docs/setup/README.md) explains the scripts and runtime directories.
Analysis and plotting use the two existing tutorial scripts in Sections 6, 8 and 9. You do not need to type a plotting program. The main exercise is to understand the model, configure cards, generate events, and calculate additional weights.

For terminal prompts, paths or Enter-key conventions, see the optional [Linux and terminal basics guide](docs/linux-basics/README.md).
If you already have an SM sample, obtain your own plots in Sections 8.5–8.6, then complete Sections 9.3–9.4.
Section 9 completes the main tutorial exercise.

All working commands run in the Linux project `~/smeftsim`. The installation guide creates a dedicated WSL distribution named `SMEFTsim` and user `smeft`; substitute your own names if they differ.
The public repository contains teaching notes and selected results. Software and environments are installed locally from upstream sources.

## Contents

1. [Learning goals and prerequisites](#1-learning-goals-and-prerequisites)
2. [SMEFT background](#2-smeft-background)
3. [What SMEFTsim does and its limitations](#3-what-smeftsim-does-and-its-limitations)
4. [Environment isolation and file locations](#4-environment-isolation-and-file-locations)
5. [Start the environment and check dependencies](#5-start-the-environment-and-check-dependencies)
6. [Reproduce the reference plots with the authors' ROOT scripts](#6-reproduce-the-reference-plots-with-the-authors-root-scripts)
7. [Choose the model and understand process commands](#7-choose-the-model-and-understand-process-commands)
8. [Generate your own SM sample](#8-generate-your-own-sm-sample)
9. [Reweighting and ROOT plots](#9-reweighting-and-root-plots)
10. [Save and reproduce results](#10-save-and-reproduce-results)
11. [Learning schedule and completion criteria](#11-learning-schedule-and-completion-criteria)
12. [Versions and references](#12-versions-and-references)

## 1. Learning goals and prerequisites

After completing the project, you should be able to:

1. Explain the model's flavor assumption, input scheme, restriction, and EFT order.
2. Configure cards and generate an SM run with its own name.
3. Explain how LHE events become ROOT histograms, and call the existing scripts to obtain four distributions.
4. Read the authors' reweight cards, calculate contributions for specified coefficients, and compare them with the SM.

The tutorial uses this fixed combination:

| Component | Configuration used here | Purpose |
|---|---|---|
| Linux | Dedicated WSL2 Ubuntu 22.04 distribution named `SMEFTsim` | Runs the generator and compilers |
| Python | 3.10, in the Linux project's `.venv` | Runs generation, reweighting, and ROOT in one environment |
| MadGraph | 2.9.27 | Exports processes, integrates, generates events, and reweights |
| SMEFTsim UFO | Tutorial v3.0.2, U35 / MwScheme | Defines interactions and input parameters |
| NumPy / setuptools | 1.26.4 / 69.5.1 | Retains the build interfaces needed for this reweighting workflow |
| ROOT | Official Python distribution 0.1a12, corresponding to 6.40.00 | Stores histograms and produces plots |

This combination has passed local execution checks. Exact dependencies are listed in [the pinned requirements](docs/setup/requirements.txt). The pinned versions reproduce this tutorial; they are not a recommendation for the latest research setup.

Terminal instructions start from an **already prepared dedicated Linux environment**.
On a new computer, first prepare WSL2/Ubuntu, a Python virtual environment, compilers, and the third-party material.
Follow the [installation guide](docs/setup/README.md) for the complete preparation sequence.
Section 4 explains the directories; the [installation guide](docs/setup/README.md) covers all downloads and environment preparation.

## 2. SMEFT background

The full background is in [docs/physics/README.md](docs/physics/README.md). Refer to it as questions arise.

### 2.1 Why use an effective field theory?

New physics at high energies can appear as additional interactions in low-energy processes.
[Explanation and expansion](docs/physics/README.md#21-why-use-an-effective-field-theory).

### 2.2 Wilson coefficients, energy scales, and units

The tutorial's Wilson coefficients are dimensionless, while the scale is entered in GeV; record both.
[Formula and units](docs/physics/README.md#22-wilson-coefficients-the-scale-and-units).

### 2.3 What is the Warsaw basis?

It is a basis of independent operators after redundancies have been removed. Field strengths themselves contain derivatives.
[Basis, derivatives, and how much theory to learn](docs/physics/README.md#23-what-is-the-warsaw-basis).

### 2.4 Why separate linear and quadratic terms?

The SM term, interference, and dimension-six squared term are distinct contributions to the squared amplitude.
The dimension-six squared term alone is not a complete higher-order EFT prediction.
[Full explanation](docs/physics/README.md#24-why-distinguish-linear-and-quadratic-terms).

### 2.5 Flavor: how new interactions distinguish fermion generations

This tutorial chooses U35. Different flavor assumptions impose different relationships between generations.
[Physical meaning of the five choices](docs/physics/README.md#25-flavor-how-new-interactions-distinguish-fermion-generations).

### 2.6 Scheme: which measurements determine electroweak parameters?

MwScheme uses mW, mZ, and GF as electroweak inputs.
[Input schemes and derived parameters](docs/physics/README.md#26-scheme-which-measurements-determine-the-electroweak-parameters).

### 2.7 Differential width: distributing a decay rate over kinematic regions

Here, the integrated quantity is a partial decay width in GeV. Histogram bin contents differ from a density obtained by dividing by the bin width.
[Formulas, symbols, and histogram interpretation](docs/physics/README.md#27-differential-widths-distributing-a-decay-channels-rate-over-kinematic-regions).

## 3. What SMEFTsim does and its limitations

### 3.1 What it provides

SMEFTsim provides FeynRules/UFO models for generators to calculate with. It does not generate events by itself.

### 3.2 Responsibilities in the software chain

The main chain is **UFO + cards → MadGraph → LHE events → additional LHE weights → ROOT histograms → PDFs**.
Each arrow passes a file or directory to the next program:

| Stage | Reads | Does | Produces; next reader |
|---|---|---|---|
| SMEFTsim model import | UFO and the selected restriction | Supplies particles, interactions and parameter formulas; removes the interactions excluded by the restriction | A model in MadGraph; used to construct matrix elements |
| MadGraph process export | Imported model and `generate ...` command | Builds numerical code for the selected process and coupling orders | `Hvlvl_SM/`; its `bin/generate_events` runs the calculation |
| MadEvent generation | Process code, `param_card.dat`, `run_card.dat` | Compiles, integrates the decay width and samples phase space | Compressed LHE events and a banner; read by reweighting or the analyzer |
| MadEvent reweighting | The original LHE and `reweight_card.dat` | Evaluates selected contributions at the same event kinematics | Additional weights inside that LHE; read by the analyzer |
| `lhe_analyzer.py` | One decompressed LHE | Reconstructs four observables from particle momenta and fills one histogram per observable and weight | One ROOT file; read by the plotter |
| `plot_histos.py` | One ROOT file | Draws the stored histograms and, where present, each selected correction added to the SM | Four `plot_*.pdf` files; read by you |

LHE stores individual particles and event weights. The analyzer's ROOT file stores **binned summaries**, not a new event sample.
Changing a plot range does not rerun generation; changing a Wilson coefficient in a card does nothing until the relevant generator or reweighting command runs.
Pythia, Delphes and detector effects are outside this Higgs-decay exercise. See the [software guide](docs/model/README.md) for the calculation's scope.

### 3.3 Define the calculation's scope

This example is a tree-level Higgs decay to four leptons. Successful execution does not by itself establish the calculation's full physical accuracy.
See the [software guide](docs/model/README.md#33-state-the-calculations-scope-explicitly) for the model's scope and approximations.

### 3.4 What is the official Mathematica notebook for?

The notebook is used to derive Feynman rules and develop the model. You do not need to run it first if you already have the UFO.
[Notebook purpose and the two workflows](docs/model/README.md#34-what-the-smeftsim-mathematica-notebooks-do).

## 4. Environment isolation and file locations

Generation, reweighting and ROOT share the Linux project's `.venv`. Compilers and system libraries are installed inside the dedicated WSL/Ubuntu environment; Windows Python is not used.

All operations use one Linux project directory, `~/smeftsim`. New analysis exercises use the short directories `outputs/ref`, `outputs/sm` and `outputs/rw`; older local output directories can remain where they are. There is no second Windows project checkout to keep synchronized.
Windows starts Linux and stores the WSL virtual disk.
If you completed an earlier edition, keep your existing LHE and ROOT files: no regeneration is needed just because this edition uses shorter output names.
Use their existing paths in the analyzer/plotter calls, or create the new analysis directories below.
Before rerunning analysis, check the destination: shell `>` replaces the target LHE copy, the analyzer replaces its output ROOT file, and the plotter replaces same-named PDFs. Choose a different output directory to preserve an earlier exercise.

| Contents | Location |
|---|---|
| This handbook and topic notes | `handbook.md`, [docs](docs/README.md) |
| Supplied example results | [examples/reweighted](examples/reweighted/README.md) |
| Python environment | `.venv`, created during local installation |
| Original tutorial, MadGraph, working files, reference data and outputs | `tutorial`, `tools`, `work`, `reference`, `outputs`, created during installation or use |

Software sources, script functions and working directories are explained together in the [installation guide](docs/setup/README.md).

## 5. Start the environment and check dependencies

### 5.1 Enter the project's Linux environment

If you are already in Linux Bash, continue at Section 5.2.
On Windows, enter the complete command in **PowerShell** and press Enter once:

```powershell
wsl -d SMEFTsim -u smeft --cd ~
```

These are the distribution and user names used in the installation guide; replace them if yours differ.
Wait for the Linux prompt before entering Bash commands.

### 5.2 Activate the shared environment

**Linux Bash | one command at a time:** each line is a complete command. After pressing Enter, wait for the prompt to return.

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
gfortran --version
```

Check that:

- `python --version` reports Python 3.10.
- `which python` points to `/home/<your-user>/smeftsim/.venv/bin/python`.
- ROOT reports `6.40.00`, and the compiler displays its version.

Then continue to Section 6. You can generate, reweight, and plot in the same terminal without switching environments.
To leave the virtual environment, enter `deactivate` and press Enter. To leave Linux, enter `exit` and press Enter.

## 6. Reproduce the reference plots with the authors' ROOT scripts

This section uses PyROOT and Python 3-compatible copies of the authors' scripts inside the project's shared `.venv`.
The sequence is **LHE → `lhe_analyzer.py` → ROOT histograms → `plot_histos.py` → four PDFs**.
First learn the calls with the authors' existing sample, then replace the input with your own reweighted SM sample.
Section 2.7 explains the vertical axis, areas under curves, and normalization.

### 6.1 What are we simulating?

The process is:

$$h\to e^-\bar\nu_e\mu^+\nu_\mu.$$

The Higgs produces four leptons through two intermediate W bosons.
Since $m_h$ is smaller than the sum of two on-shell W masses, both W bosons cannot be on shell.
The four-body final-state kinematics let us compare EFT effects in different regions.

| Plot name | Observable | Meaning |
|---|---|---|
| `mll` | $m_{e\mu}$ | Invariant mass of the charged-lepton pair |
| `mmv` | $m_{\mu\nu_\mu}$ | Invariant mass of the muon and its corresponding neutrino |
| `pTl1` | $\max(p_T^e,p_T^\mu)$ | Transverse momentum of the charged lepton with the larger transverse momentum |
| `pTmu` | $p_T^\mu$ | Muon transverse momentum |

These are generator-level variables. Using the true neutrino momentum does not imply that a detector can directly measure the same quantity.

This process is a Higgs **decay**: the integrated result is a partial width $\Gamma$ in GeV.
The local plotting copy labels the bin contributions as $\Gamma_{\mathrm{bin}}$ [GeV]; dividing by the bin width gives a differential width.
For a scattering process, quantities such as cross sections must follow the generator's conventions; do not copy the units of this decay example.

### 6.2 Reading the upper and lower panels

The upper panel shows each kinematic bin's contribution to the width. Dividing by the bin width gives a differential width.
The lower panel shows:

$$R(X)=\frac{(\text{SM}+\text{one selected contribution})(X)}{\text{SM}(X)}.$$

The black line is the SM. Each colored line adds only one selected contribution to show its effect.
For example, `SM + cHl3 quadratic` does not also include the linear term.
That curve is therefore not a complete EFT prediction at `cHl3=1`.
The authors' plots show central values without statistical uncertainty bands. Bins with zero SM content or sparse statistics are unsuitable for judging ratios.

The [official tutorial](https://smeftsim.github.io/tutorials.html) suggests observing that:

- The `cHbox` and `cll1` linear terms give flat ratios in this example, indicating that they mainly change the rate.
- The `cHW` and `cHl3` linear terms give non-flat ratios, indicating that they also change the shape.
- Propagator corrections deserve attention where a W is close to being on shell.
- The squared terms for the chosen coefficients are small here; this is not a general result for all energy regions or coefficients.

The authors' SM sample has an integrated width of approximately $1.00868\times10^{-5}\ \mathrm{GeV}$.
Your smaller sample need not match its final digits; compare results together with their integration uncertainties.

### 6.3 Where are the reference ROOT files?

After the installation guide's extraction step, ROOT files are in the Linux project's `reference/Results/Root_files`, and LHE files in `reference/Results/Hvlvl_*/Events/run_01`.
They come from the results archive supplied with Ilaria Brivio's tutorial; no separate ROOT download is needed.
See the [extraction and file checks](docs/setup/README.md#7-extract-the-reference-results-and-continue).

### 6.4 Activate PyROOT while preserving the authors' scripts

The shared `.venv` activated in Section 5 already contains ROOT. There is no need to switch environments during normal use.
The actual scripts called in Linux are `work/Material/pyroot_python3/lhe_analyzer.py` and `plot_histos.py`.

The [installation guide, Section 5](docs/setup/README.md#5-prepare-the-two-python-3-analysis-scripts) describes the originals, the arguments required by both scripts,
and how to prepare them on a new computer. For an existing installation, first run `sudo apt-get install -y --no-install-recommends ghostscript` in Linux, then `python fix_axes.py` from `~/smeftsim` before replotting.
Tutorial code without a confirmed license is used only locally; the public repository includes conversion instructions rather than these copies.

**Linux Bash, project root | one command at a time:**

```bash
source .venv/bin/activate
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

Python should come from the project's `.venv`, and ROOT should report 6.40.00.

### 6.5 Complete LHE → ROOT → PDF with the tutorial sample

**Linux Bash, `.venv` active.** Each line below is one complete command: enter the whole line, press Enter once, and wait for Bash to return. Keep `> OUTPUT` on the same line as `gzip`; terminal line wrapping does not require an extra Enter.
Stop if a command fails. The optional [Linux guide](docs/linux-basics/README.md) explains the shell commands in more detail.

#### A. Prepare and inspect the LHE input

```bash
cd ~/smeftsim
mkdir -p outputs/ref
gzip -dc reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz > outputs/ref/events.lhe
ls -lh outputs/ref/events.lhe
head -n 1 outputs/ref/events.lhe
```

`gzip -dc` reads the compressed sample without changing it; `>` writes the decompressed contents to `events.lhe`.
Expect a nonempty file of about **33 MiB**, starting with `<LesHouchesEvents ...>`.
The filename contains `SM`, but this supplied sample already includes additional reweighting contributions; these will generate the comparison curves.

#### B. Analyze the events

```bash
python work/Material/pyroot_python3/lhe_analyzer.py outputs/ref/events.lhe outputs/ref/Hvlvl_SM.root
```

The analyzer takes **two arguments**: input LHE, then output ROOT. Enter both before pressing Enter.
It reads particle four-momenta and weights, calculates `mll`, `mmv`, `pTl1` and `pTmu`, and fills a histogram for each observable–weight pair.
For example, `mmv_direct_sim` contains the SM contribution and `mmv_cHl3` the selected linear interference contribution.
The program divides by the actual event count; do not divide again yourself.
Expect `processed 20000 events`, contribution integrals and `file ... produced`, followed by Bash.
The next program reads this ROOT file, not the LHE.

#### C. Draw the stored histograms

```bash
cd outputs/ref
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
```

The plotter takes **one argument**, the input ROOT file. It creates four PDFs in the **current directory**.
It does not calculate new matrix elements or event weights. For each selected correction it forms SM + that correction, then divides by SM for the lower panel.
Expect four nonempty PDFs. In WSL, run `explorer.exe .` in Bash to open this directory in Windows.

Checkpoint: trace `events.lhe → Hvlvl_SM.root → plot_mmv.pdf`, and identify which program creates each file.
If you only want to redraw the existing reference ROOT file, skip A–B and use this alternative in `~/smeftsim/outputs/ref`:

```bash
python ../../work/Material/pyroot_python3/plot_histos.py ../../reference/Results/Root_files/Hvlvl_SM_run_01.root
```

Choose one plotting input; another call overwrites PDFs with the same names. The batch script `make_rootfiles.sh` is unnecessary for learning these two calls.

### 6.6 Adjust the authors' existing plot settings if needed

First complete Section 6.5 with the authors' default settings.
In `plot_histos.py`, `weights_to_plot` selects curves and `histo_dc` controls display ranges.
These are optional plot settings, not changes required for Python 3 compatibility.

To show only the six corrections below, change `weights_to_plot` in the **Linux working copy** to these file contents.
**Where to do this: a text editor, not the terminal.** In the editor, Enter only inserts a new line.
Preserve commas, quotes, and brackets, press `Ctrl+S` to save, then return to Bash and run the plotting command:

```python
weights_to_plot = [
    default_wgt,
    "cHbox",
    "cll1",
    "cHW",
    "cHl3",
    "cHl3_sq",
    "cHl3_propW",
]
```

The authors' default ratio range for `pTl1` is `.95, 1.05`.
If curves extend beyond it, change those two limits to `.68, 1.25`, then rerun the same plotting command.
Keep the other dictionaries and algorithms unchanged.
The plotting script cannot calculate a contribution missing from the ROOT file. If a curve is absent, check the reweight labels first.

The [figure README](docs/figures/README.md) explains the original plots' width units, bin widths, and curve meanings.

## 7. Choose the model and understand process commands

### 7.1 Why this model is used

The model is `SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl`:
the U35 flavor assumption, MwScheme electroweak inputs, and the tutorial's custom restriction.
[Model explanation](docs/processes/README.md#71-why-this-example-uses-this-model).

### 7.2 A restriction differs from a parameter card

A restriction simplifies the model at import time; the parameter card sets the adjustable inputs for a run.
Vertices removed during import are not restored by subsequently editing the parameter card.
[Full distinction](docs/processes/README.md#72-a-restriction-is-different-from-a-parameter-card).

### 7.3 Order options: select amplitudes, then select their products

| Target | Authors' process options, all with `SMHLOOP=0` |
|---|---|
| SM baseline | `NP=0 NPprop=0` |
| Ordinary linear interference | `NP=1 NP^2==1 NPprop=0` |
| Ordinary dimension-six squared contribution | `NP==1 NPprop=0` |
| Propagator interference | `NP=0 NPprop=2 NPprop^2==2` |

`NP=1` is an upper bound at amplitude level; `NP==1` selects an exact order.
`NP^2` counts the sum of orders on the two sides of an amplitude product. The `NPprop` counting of dummy vertices is not the number of EFT insertions.
The expanded formulas, two detailed tables, and dummy-vertex implementation are in
[docs/processes/README.md](docs/processes/README.md#73-coupling-order-options-select-amplitudes-then-terms-in-their-square).

### 7.4 Which UFO parameters exist, and which should you set?

For this exercise, record the model, coefficients, `LambdaSMEFT`, widths, seed, and cuts.
Internal parameters follow the model's formulas and are not all independent inputs.
See [parameter categories and the basis for their values](docs/parameters/README.md)
and the [complete parameter index](docs/parameters/model_parameter_reference.md).

## 8. Generate your own SM sample

**Prerequisite: prepare the environment and pass the checks in Section 5. Run the following commands in Linux Bash.**
Start with 2,000 events: enough to practice the workflow. Increase the statistics later for detailed distribution comparisons.

### 8.1 Export the process directly in MadGraph

The installation guide has prepared `work/Material`. In Linux Bash, enter one complete command at a time, press Enter, and wait for the prompt:

```bash
cd ~/smeftsim
source .venv/bin/activate
cd work/Material
python ../../tools/MG5_aMC_v2_9_27/bin/mg5_aMC
```

The last command opens the `MG5_aMC>` prompt. The following are **MadGraph commands**: enter each complete line and press Enter, waiting for it to finish. Do not enter them in Bash.

```text
set auto_update 0 --no_save
set auto_convert_model True --no_save
import model ./SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
display processes
```

These commands have different jobs:

| Command | Meaning here |
|---|---|
| `set ... --no_save` | Disables updating and allows local model conversion for this session; does not edit your saved global configuration |
| `import model ...` | Loads SMEFTsim interactions after applying the `massless_Hvlvl` restriction |
| `generate ...` | Selects Higgs decay to `e- ve~ mu+ vm` and builds its SM matrix elements; no events are sampled yet |
| `display processes` | Prints what was selected, so you can catch a wrong final state or order before exporting |

Check that the model imports successfully and the selected process is the intended decay.
The `>` in `generate h > ...` belongs to MadGraph process syntax; it is not Bash output redirection.
For the first export, continue in the same `MG5_aMC>` session:

```text
output Hvlvl_SM
quit
```

`output` exports numerical process code; it does not generate events. `quit` returns to Bash in `work/Material`.
Check the exported files:

```bash
ls Hvlvl_SM/Cards/param_card.dat Hvlvl_SM/Cards/run_card.dat
```

If `Hvlvl_SM` already exists, skip `output`, enter only `quit`, and continue with card configuration or a new run name. Preserve the existing process.

### 8.2 Configure the cards

The exported process defines **which matrix element** to evaluate. These cards define **with which numerical inputs and sampling settings**.
Copy the supplied templates so the mass, width and cut conventions match the reference exercise:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cd ~/smeftsim/work/Material
cp param_card_Hvlvl.dat Hvlvl_SM/Cards/param_card.dat
cp run_card_Hvlvl.dat Hvlvl_SM/Cards/run_card.dat
```

| Card | Main contents | Settings for this exercise |
|---|---|---|
| `param_card.dat` | Masses, couplings, Wilson coefficients, scale, and widths | All EFT coefficients zero; `LambdaSMEFT=1000`; retain the authors' widths |
| `run_card.dat` | Event count, seed, integration, and cuts | `nevents=2000`, `iseed=23456`; retain the other settings |
| `reweight_card.dat` | Weight definitions for new parameter points and processes | Leave reweighting disabled during the SM exercise |

In **Linux Bash, in `~/smeftsim/work/Material`**, open the cards with the terminal editor, finishing the first before opening the second:

```bash
nano Hvlvl_SM/Cards/param_card.dat
nano Hvlvl_SM/Cards/run_card.dat
```

In `nano`, change the settings listed in the table. Press `Ctrl+O` to save, Enter to confirm the filename, then `Ctrl+X` to return to Bash.
Inside the editor, Enter inserts a new line; card contents are not Bash commands.
If you use a graphical editor, save with `Ctrl+S` and check that the files are in the Linux working directory.

Check that you are editing the Linux working copy. To change the event count, edit `nevents` in `run_card.dat`.
Naming a run `...2000` does not make the generator produce 2,000 events automatically.
Cards commonly use `value = parameter_name` or `index value # parameter comment`; preserve the original file's format.

For example, the `Block smeft` entry `22 0.000000e+00 # cHl3` sets this independent coefficient to zero; `Block smeftcutoff` sets `LambdaSMEFT` to 1,000 GeV.
`nevents` controls the requested sample size, while `iseed` controls pseudo-random sampling. Neither changes the interaction model.
The decay calculation has no proton beams, even though the generic card contains beam/PDF fields; do not infer a 13 TeV collision from those unused entries.
Leave the supplied cuts unchanged: here `ptl=0` sets no positive minimum and `ptlmax=-1` means no upper cut. Do not import the detector tutorial's `ptl=10` into this reference decay.
This exercise has no parton shower and no matching/merging step; these words need not appear as literal card entries.

Checkpoint: find `cHl3`, `LambdaSMEFT`, `nevents` and `iseed`, and identify which file contains each. Editing a card alone does not create any events.

### 8.3 Generate a run with its own name

**Linux Bash, current directory `work/Material`:**

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
./Hvlvl_SM/bin/generate_events training_sm_2000
```

`generate_events` runs the numerical code exported in Section 8.1, reading the two cards you just saved.
Compilation produces an executable, integration estimates the partial width, and event sampling writes particle momenta and weights to LHE.
`training_sm_2000` chooses the result directory; it is not an input filename or an event-count option.

After pressing Enter, you enter MadGraph's tool menu; **you are no longer at an ordinary Bash prompt**.
Follow this sequence, without pasting later analysis commands into the menu:

1. Check the tool statuses. If necessary, enter `shower=OFF` and press Enter once.
   Do the same separately for `detector=OFF`, `analysis=OFF`, and `reweight=OFF`.
   Do not repeat settings that are already OFF or unavailable because the tool is not installed.
2. Once the statuses are correct, enter `done` and press Enter once to continue.
3. If a parameter/run-card editing menu appears and you have already saved the cards in Section 8.2, enter that menu's `0` or `done`
   and press Enter once to accept the current cards. Follow the displayed options if the menu does not accept one of these answers.
4. Integration, compilation, and generation logs follow. **Wait. Do not repeatedly press Enter or type other commands.**
5. Continue to Section 8.4 only after the program finishes and the Bash prompt returns.

`training_sm_2000` is the new run name. If you have used it before, inspect the existing result first.
To generate again, choose a new name such as `training_sm_v2`, and replace it consistently in later paths.
The output should be under `Hvlvl_SM/Events/training_sm_2000`, including the LHE file and banner.
`smoke_sm_2000` names an installation-check run; the different name here preserves it.

### 8.4 Check what you generated

The important outputs under `Hvlvl_SM/Events/training_sm_2000/` are:

| File | What to inspect | Next use |
|---|---|---|
| `unweighted_events.lhe.gz` | LHE header, final-state particle records and event weights | Decompress an analysis copy in Section 8.5; keep the compressed original for Section 9 |
| `training_sm_2000_tag_1_banner.txt` | Snapshot of process definition, cards and integration information | Record the configuration actually used, rather than a card edited later |

Check the following:

1. The process is the intended Higgs decay, and the model and restriction have not changed to another version.
2. The banner records the requested parameters, scale, seed, and event count.
3. The LHE file contains complete events with the correct final state, and a positive integrated width with a reported Monte Carlo integration uncertainty.
4. Compare the SM width and four distributions with the authors' results. Consider whether any differences can be explained by statistics or version settings.

Matching the seed, versions, and cards helps reproducibility, but compiler differences and parallel execution can affect event-by-event agreement.
For research records, preserve the full configuration and statistical results; matching the final digit is not the only criterion.

### 8.5 Create a ROOT file for the SM distributions

**Linux Bash, `.venv` active; one complete command per Enter.** The input is your generated LHE, not the reference sample.
Make a decompressed copy in the short analysis directory `outputs/sm`:

```bash
cd ~/smeftsim
mkdir -p outputs/sm
gzip -dc work/Material/Hvlvl_SM/Events/training_sm_2000/unweighted_events.lhe.gz > outputs/sm/events_full.lhe
```

If your run has another name, replace `training_sm_2000` consistently.
The tutorial analyzer allocates histograms from the LHE header's extra-weight declarations. Some SM files carry declarations without a complete set of event weights.
For **SM-only analysis**, remove declarations and extra-weight blocks from a separate copy:

```bash
sed -e '/<initrwgt>/,/<\/initrwgt>/d' -e '/<rwgt>/,/<\/rwgt>/d' outputs/sm/events_full.lhe > outputs/sm/events_sm.lhe
ls -lh outputs/sm/events_sm.lhe
head -n 1 outputs/sm/events_sm.lhe
```

The two `sed` rules remove `<initrwgt>...</initrwgt>` and `<rwgt>...</rwgt>` blocks. They do not recalculate weights or replace missing EFT contributions with zero.
Particle momenta, original SM weights and event count are retained. Keep the original `.lhe.gz` for reweighting; do not use this stripped copy in Section 9.
Expect a nonempty file starting with `<LesHouchesEvents ...>`, then run the same analyzer as in Section 6:

```bash
python work/Material/pyroot_python3/lhe_analyzer.py outputs/sm/events_sm.lhe outputs/sm/Hvlvl_SM.root
```

The **first argument** is input, the **second** is output. Wait for `processed 2000 events` and `file ... produced`; use the actual count if you requested another size.
`no new weights found` is expected for this SM-only copy. The ROOT file contains four histograms: `mll_direct_sim`, `mmv_direct_sim`, `pTl1_direct_sim` and `pTmu_direct_sim`.
The analyzer already divides by the event count. The next command will draw these stored bins without rereading the LHE.

### 8.6 Use ROOT to plot your own SM distributions

Use the **same existing `plot_histos.py`** as for the reference; no interactive Python loop is needed.
In Linux Bash, enter each whole line and press Enter once:

```bash
cd ~/smeftsim/outputs/sm
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
```

Input: the four SM histograms from Section 8.5. Output: four PDFs in `outputs/sm`.
The SM-only file produces a single panel. Section 9 adds EFT corrections and a ratio panel.
In WSL, `explorer.exe .` opens this directory from Bash.

The vertical axis shows each bin's partial decay width in **GeV**; see Section 6.2 and the [figure guide](docs/figures/README.md). The same plotting call produces the example below:

![SM electron–muon invariant-mass distribution](docs/figures/sm_mll.png)

Checkpoint: the integrated width is of order `1e-5 GeV`. Identify which panel shows your SM and why no ratio curve has appeared yet.
You have now followed your own events through **generation → SM-only analysis copy → ROOT → PDFs**.
Continue to Section 9 using the original compressed events.

## 9. Reweighting and ROOT plots

This section uses the original SM LHE from Section 8 to calculate the additional contributions defined by the authors' cards on the same events.
The SM analysis copy in Section 8.5 is only for plotting the SM alone; it is not the reweighting input here.
Sections 9.1–9.2 explain the principles and card contents; the actual operations start in Section 9.3.
Section 9.4 produces `outputs/rw/Hvlvl_SM.root` and four comparison plots.

### 9.1 What does reweighting do?

For the same event kinematics $x$, ordinary parameter reweighting compares matrix elements at two parameter settings:

$$r(x)=\frac{|\mathcal M(x;\theta_{\rm target})|^2}{|\mathcal M(x;\theta_{\rm base})|^2}.$$

Under the appropriate sampling and normalization conventions, event weights can estimate a target distribution
without generating a large new sample for every parameter point.
The base sample must cover the target's relevant kinematic regions; statistical efficiency deteriorates when a few events carry extremely large weights.

This tutorial also uses `change process` to calculate **linear, squared, or propagator contributions** separately.
The weight named `cHl3` is therefore the selected linear interference contribution, not a probability ratio for a complete target EFT point.
Interpret each label together with the process and order selection in the reweight card.

### 9.2 Read a reweight card

The `cHl3` block in the authors' `reweight_card_int.dat` has the following meaning.
**These are card-file contents, for reading or editing in a text editor. Do not execute them line by line in Bash.**
MadGraph reads the `done` in the card; it is not a menu answer you need to type now:

```text
change process h > e- ve~ mu+ vm SMHLOOP=0 NPprop=0 NP=1 NP^2==1
launch --rwgt_name="cHl3"
set cHbox 0
set cHW 0
set cHl3 1
set cHq3 0
set cll1 0
done
```

The first line selects the interference process; `launch` names the output weight; the following lines set this point's coefficients.
MadGraph reads this card in `madevent reweight`; it does not run the generation menu again.
`change process` defines the matrix-element contribution used in the numerator, `--rwgt_name` defines its LHE label, and the `set` lines choose the parameter point.
The filename of the card is not the weight label. The LHE `<rwgt>` block stores the weights. The original SM weight and additional weights have different meanings and must be distinguished in analysis.
Here, `cHl3` represents the selected linear interference contribution. Other cards select squared or propagator corrections.

#### From a matrix-element ratio to the weights used in plotting

For the same SM event $x_i$, the generator compares the target contribution with the SM matrix element, then multiplies by the base event weight.
For example, the conceptual expression for the linear contribution is

$$
w_{L,i}=w_{S,i}\,
\frac{2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)(x_i)}{|\mathcal M_0(x_i)|^2}.
$$

$w_{S,i}$ is the SM weight, while $w_{L,i}$ is the linear contribution represented by this event; it can be negative.
The LHE weights saved in this example already include generator normalization. Do not multiply them by the SM weight again after reading them.
Squared and propagator contributions have their own target matrix-element expressions.
Event four-momenta and the total event count stay unchanged; only these additional weights change. A new set of events is not needed for each contribution.

For a linear combination, first form $w_S+w_L+w_P$ for each event; add $w_Q$ if also including the squared contribution.
Then sum in each bin and divide by $N$ and the bin width to obtain a density.
Weights on the same event are correlated, so combination uncertainties should be calculated from the summed weights event by event.

### 9.3 Use the authors' reweight cards in MadGraph yourself

The aim is to use the three supplied cards to calculate linear, squared, and propagator contributions for ROOT plotting.
Every call below reads the selected run's **existing LHE** and the process copy's **current `Cards/reweight_card.dat`**.
It compiles the target matrix element if needed, evaluates it at each existing event, and updates that run's compressed LHE with new labels and weights.
It produces neither ROOT nor PDF files. Section 9.4 analyzes this updated LHE once all three calls are complete.
The linear card calculates four single-coefficient linear contributions; the squared card calculates four squared contributions;
the propagator card calculates three width/propagator contributions.
**There is no need to regenerate events for each coefficient or to use the mixed-term card to draw the six reference correction curves.**

| Authors' card | Main weight labels |
|---|---|
| `reweight_card_int.dat` | `cHbox`, `cHW`, `cHl3`, `cll1` |
| `reweight_card_squares.dat` | `cHbox_sq`, `cHW_sq`, `cHl3_sq`, `cll1_sq` |
| `reweight_card_propW.dat` | `cHl3_propW`, `cHq3_propW`, `cll1_propW` |

Other labels in the cards are also calculated, but need not be plotted yet.
Each `launch` is a separate parameter point. For example, the `cHbox` launch has `cHbox=1` with the other coefficients zero;
it does not set all four Wilson coefficients to 1 together. `LambdaSMEFT` retains the base sample's value of 1,000 GeV.
The reweight card's `change process` changes the target contribution; the base events still come from the SM.

#### A. Enter Linux and create your own working copy

If you are already in Linux, continue below; otherwise enter it as in Section 5.1.
Activate `.venv` in Linux Bash, or keep using it if already active.

**Linux Bash**, activate the shared `.venv`, or keep using it if it is already active:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cd ~/smeftsim
source .venv/bin/activate
which python
cd work/Material
ls Hvlvl_SM/Events/training_sm_2000
```

`which python` should point to this project's `.venv/bin/python`.
The card and compiler dependencies require this environment; do not invoke Windows Python.

Use a separate process copy named `Hvlvl_SM_manual` to practice while keeping the original SM process.
**This directory should not exist the first time you do this.** If you have already completed this section, reuse it and skip the copy and old-cache renaming steps.
Check first:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
ls -d Hvlvl_SM_manual
```

If the directory does not exist, run:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cp -a Hvlvl_SM Hvlvl_SM_manual
```

If the original SM process has already been reweighted, it may contain compilation caches `rw_me` and `rw_me_2`.
In the **newly copied process**, rename them to keep them while allowing this exercise to build fresh caches:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
mv Hvlvl_SM_manual/rw_me Hvlvl_SM_manual/cache_before_manual_rw_me
mv Hvlvl_SM_manual/rw_me_2 Hvlvl_SM_manual/cache_before_manual_rw_me_2
```

Rename a cache only if it exists in your copied process. If you start from an SM process that has never been reweighted,
skip any cache that does not exist. Do not repeat the renaming or change the original `Hvlvl_SM`.
If the original sample already has a `cHl3` label, the authors' card replaces that label in this copy.
Interpret MadGraph's `tag ... already defines, will replace it` message accordingly.

#### B. Linear card: read, copy, then run

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cat reweight_card_int.dat
cp reweight_card_int.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

`cat` prints the card contents: read them before continuing. `cp` places the card where the generator expects it.
The third command, `madevent reweight ...`, enters MadGraph; wait for its question first.
There is **no `-f`**, so the interactive steps remain.
If it asks whether to edit `reweight_card.dat`, check the displayed file, enter `0` or the menu's `done`,
and press Enter once to accept the current card. Enter each menu answer separately and press Enter.
Once compilation/event-processing logs appear, wait without typing further `done` commands until Bash returns.
Prompt wording may vary between versions; follow the current menu.
Compilation and event processing take time. Expect results for four parameter points, then wait for Bash before the next step.

Check the new labels in the LHE header:

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
zcat Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz | sed -n '/<initrwgt>/,/<\/initrwgt>/p'
```

Checkpoint: `cHbox`, `cHW`, `cHl3`, and `cll1` appear.
These labels denote separate interference contributions, which can be negative; they are not full rates with the SM already added.

#### C. Squared card: change the target process and parameter points

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cat reweight_card_squares.dat
cp reweight_card_squares.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

Accept the current card as before. When it finishes, repeat B's `zcat ... | sed ...` check.
Expect new labels `cHbox_sq`, `cHW_sq`, `cHl3_sq`, and `cll1_sq`.
The authors' card explicitly includes `set cHWB 0` at some points. This restriction already fixes it to zero.
If your version says this parameter is not a free input, check its value and subsequent results; do not make it nonzero.
The previous linear labels should remain in the file.

#### D. Propagator card: calculate corrections with a separate order label

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cat reweight_card_propW.dat
cp reweight_card_propW.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

Accept the current card. After it finishes, inspect the weight header again.
Expect new labels `cHl3_propW`, `cHq3_propW`, and `cll1_propW`, with the earlier labels retained.
Here, `NP=0 NPprop=2 NPprop^2==2` selects propagator interference.
It does not calculate the ordinary `cHl3` interference a second time; Section 7.3 explains the counting.

If the command returns to the terminal without the corresponding labels, inspect the displayed error and the process directory's `ME5_debug`.
Do not continue straight to plotting after a failure. Confirming success also requires checking the actual per-event weights in the next section,
not just the header labels or the process exit code.

#### E. Trace one coefficient before continuing

For `cHl3`, trace these three independent labels: `cHl3` (ordinary linear), `cHl3_sq` (dimension-six squared), and `cHl3_propW` (propagator correction).
The input phase-space points are identical; the target order selection and weights differ.
When plotting, each selected label is added **separately** to the SM. Selecting three labels does not ask the plotter to add all three into one prediction.
To study another parameter point later, first state which contribution and coefficient value you want, then edit a **separate card with a distinct weight label** and rerun reweighting.
Changing only `weights_to_plot` selects existing histograms and cannot calculate new physics.

After all three reweighting calls, the file remains in the Linux process directory.
Continue with Section 9.4, calling the authors' analyzer and plotting script in the same `.venv`.
You do not need to copy the LHE file to Windows first.

### 9.4 Plot your own reweighted SM sample with the authors' ROOT script

After Section 9.3, the file should contain the linear, squared, and propagator labels from the authors' cards.
**Linux Bash, still using the activated shared `.venv`:**

**Linux Bash | one command at a time:** each line is one complete command. Press Enter once, wait for it to finish, then enter the next line.

```bash
cd ~/smeftsim
mkdir -p outputs/rw
gzip -dc work/Material/Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz > outputs/rw/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/rw/events.lhe outputs/rw/Hvlvl_SM.root
```

**Check successful analysis before plotting:** expect `processed ... events`, the integrated values of the weights, and `file ... produced`,
followed by the Bash prompt. The current `training_sm_2000` contains 2,000 events, so expect `processed 2000 events`.
For future runs, use their actual event count. If an error occurs, first check Section 9.3's input and weights.

**Linux Bash | one command at a time:** enter the whole line, press Enter once, and wait for the result.

```bash
ls -lh outputs/rw/Hvlvl_SM.root
```

Expect a nonempty ROOT file. `rw` is the directory and `Hvlvl_SM.root` the file.
It comes from the reweighted SM copy and contains the SM baseline plus additional contributions. The ROOT file from Section 8.5 contains only the SM baseline.

**Linux Bash | one command at a time:** first change directories and press Enter; then enter the complete plotting command, press Enter, and wait for it to finish.

```bash
cd outputs/rw
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
```

The analyzer reads the updated LHE, including its original SM weights and all additional labels, and stores the four distributions for each weight.
The plotter reads those binned results and writes the comparisons. It does not open several independent SM/EFT simulation directories or calculate a new `cHl3=1` point.
For this exercise, one reweighted event sample contains everything needed to draw the reference contributions.
Expect four `plot_*.pdf` files. In WSL, open the output directory from Linux Bash:

**Linux Bash / WSL | enter each complete command and press Enter:**

```bash
cd ~/smeftsim/outputs/rw
explorer.exe .
```

When comparing with Section 6.5's reference PDFs, keep the same `weights_to_plot` and display ranges.
Curves should have the same meanings, overall scales, and main shapes; randomly generated events need not agree bin by bin.
To select the six corrections listed in Section 6.6, adjust the working-copy settings as described there.

The additional LHE weights already include generator normalization; the authors' analyzer then divides by the event count according to its convention.
Do not multiply by the SM weight again or divide by the event count twice.
The plots retain the authors' central-value presentation without complete statistical uncertainty bands.

Check that the LHE weight declarations match the actual weights in every event. The analysis log should report the full event count and the integral of each contribution.

Below is this project's reweighted example, based on 2,000 SM events and the tutorial plotting copy with corrected display labels. Section 6.6 explains the bin convention.

![Reweighted muon–neutrino invariant-mass distribution](docs/figures/rw_mmv.png)

Other examples: [mll](docs/figures/rw_mll.png), [leading-lepton transverse momentum](docs/figures/rw_pTl1.png),
and [muon transverse momentum](docs/figures/rw_pTmu.png).

**Section complete:** you have the multi-curve plots corresponding to the authors' cards. This completes the main tutorial workflow.

## 10. Save and reproduce results

### 10.1 Quick reference for routine operations

Installation and script inputs/outputs are in the [installation guide](docs/setup/README.md).
Enter the environment in Section 5, generate in Section 8, and reweight in Section 9.
To analyze and redraw the supplied results, follow [examples/reweighted](examples/reweighted/README.md).

### 10.2 Save an exercise

Keep the original compressed LHE file, cards, banner, versions, parameters, seed, actual event count, and important plots.
See [examples/reweighted/metadata.json](examples/reweighted/metadata.json) for the saved example's records.

### 10.3 Share a reproducible result

When sharing a plot, include its input data or acquisition instructions, cards and parameter settings, software versions, event count, seed, and analysis commands. State the units and normalization used for each plot.
The [example metadata](examples/reweighted/metadata.json) illustrates these records, and the [example guide](examples/reweighted/README.md) shows how to reanalyze and replot the supplied files.

### 10.4 Organize local outputs

Put your run outputs in `outputs` and keep the supplied example in `examples`. Commands create `outputs` locally; the repository does not ship an empty placeholder.
You can remove decompressed copies that can be recreated from compressed originals. Preserve `.venv`, original runs, cards, banners and the virtual disk.

## 11. Learning schedule and completion criteria

The main work can be split into four sessions; computational waiting time is additional:

| Session | Active learning time | Task | What you should be able to explain |
|---|---:|---|---|
| 1 | 30–40 minutes | Sections 2–3: physics and the software chain | How SMEFTsim describes new interactions |
| 2 | 20–30 minutes | Section 6: trace the two analysis calls and read reference plots | Which file contains particles, weights or binned summaries |
| 3 | 30–45 minutes | Sections 7–8: generate and plot your own SM sample | The roles of the model, the two cards, LHE, and ROOT |
| 4 | 30–45 minutes | Section 9: reweight and plot comparisons | How different contributions come from the same base events |

Afterward, try explaining in your own words:

1. Why U35 and MwScheme were chosen, and how a restriction differs from a parameter card.
2. What the SM, interference, dimension-six squared, and propagator contributions mean.
3. How the coefficients and scale in the cards correspond to the Lagrangian.
4. Why one event can have several weights, and why interference weights can be negative.
5. Which operators mainly change the overall rate, and which also change the shape.

Completing Section 9 finishes this tutorial exercise.
Research use requires further checks of sampling coverage, statistical uncertainties, and agreement between reweighting and direct generation.
Before using this workflow for research, check and document the model version, EFT truncation, and width conventions.

## 12. Versions and references

This tutorial pins Python 3.10, MadGraph 2.9.27, SMEFTsim v3.0.2, and ROOT 6.40.00.
Exact Python dependencies are in [docs/setup/requirements.txt](docs/setup/requirements.txt).
See [metadata.json](examples/reweighted/metadata.json) for the actual versions used for this example.

The full tutorial list, authors, and papers are in the [root README](README.md#sources-and-acknowledgments).
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for third-party licensing and publication scope.
