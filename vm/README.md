# Dedicated WSL environment and virtual disk

[English](README.md) | [简体中文](README.zh-CN.md)

After preparing a dedicated Ubuntu environment, follow the [fresh-clone setup guide](../docs/setup/README.md).

This directory contains environment assets for the local machine.
Only this guide is published; installers, images and the virtual disk are ignored by Git.

| Local item | Purpose |
|---|---|
| `downloads` | Windows WSL installer, Ubuntu rootfs image and verification material |
| `SMEFTsim/ext4.vhdx` | The entire dedicated Linux disk, including its environment, generator, processes and events |

Do not delete `ext4.vhdx` as an ordinary cache file. Uploading it is not required.
Copy selected results to `examples` or commit ordinary files, as explained in the
[publishing guide](../docs/publishing/README.md).

The example installation uses WSL2 Ubuntu 22.04, distribution name `SMEFTsim` and Linux user `smeft`.
On a new machine, start with the official
[WSL installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install) and
[custom-distribution import guide](https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro).
Prepare Python 3.10, `python3-venv`, `python3-dev`, `gcc`, `gfortran`, `make`, `git` and `perl`.
The current helper scripts assume these prerequisites and local downloads are available.

## Isolation

The dedicated WSL2 Ubuntu uses a Linux kernel and virtualization.
It is operated through a terminal; this exercise does not require a Linux desktop.

| Layer | Location and purpose | Scope |
|---|---|---|
| Windows support | WSL and Virtual Machine Platform | Shared operating-system support |
| Dedicated Ubuntu | Distribution `SMEFTsim`; disk `vm/SMEFTsim/ext4.vhdx` | Linux tools and packages are kept in this disk |
| Unified project environment | `/home/smeft/smeftsim/.venv` | MadGraph, reweighting and PyROOT share project dependencies |

The physics dependencies were not installed into the existing global Windows Anaconda environment.
Windows PATH, other project environments and user-level `.wslconfig` were not manually changed.
Windows PATH inheritance is disabled for this distribution.
Linux system packages belong to the dedicated Ubuntu, not to the global Windows Python environment.

## Directory layout

```text
smeftsim/
├── README.md                    Project index and attribution
├── handbook.md                  Practical learning route
├── tutorial/                    Original upstream downloads
├── tools/MG5_aMC_v2_9_27/        Generator source
├── cards/                       Reusable process definitions
├── scripts/                     Setup, launch and validation helpers
├── reference/Results/           Upstream reference results
├── docs/figures/                 Shareable example PNGs
├── outputs/                     Local run data, ROOT files and plots
└── vm/                          Installers, images and virtual disk
```

The active Linux project is `/home/smeft/smeftsim`.
Edit run cards in its `work/Material` directory; `tutorial/Material` remains the upstream reference.
Activate `.venv` once and use the same terminal for generation, reweighting and ROOT plotting.

SMEFTsim describes interactions in a UFO. MadGraph produces numerical process code;
`gcc`, `gfortran` and `make` build executable components.
Python 3.10, NumPy 1.26.4 and the pinned setuptools version provide the older f2py build interface
used by this tutorial route. Windows Python 3.14 is not the runtime for these Linux tools.

A Windows environment named `.venv` may also exist at the Windows project path.
It is a separate environment. The handbook's `source .venv/bin/activate` is always executed
inside the Linux project; Windows and Linux environments are not interchangeable.
