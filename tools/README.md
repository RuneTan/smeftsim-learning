# Third-party source downloads

[English](README.md) | [简体中文](README.zh-CN.md)

`MG5_aMC_v2_9_27` is a third-party MadGraph checkout.
It is not a generator developed by this project.
Retain its original documentation and licenses; obtain the source upstream rather than uploading
the entire checkout with these teaching notes.

| Program | Pinned version | Purpose |
|---|---|---|
| MadGraph5_aMC@NLO | 2.9.27; commit `eb76cab72b8d44aac7162ac7221ac08a4384a169` | Model import, process export, integration, event generation and reweighting |

**Download steps for a new machine. Skip them if these directories already exist.**
From the Windows project root, enter one complete command at a time, press Enter and wait:

```powershell
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
```

`tutorial` is a sibling directory at the project root. Keep the author's README there.
The Linux `setup_linux.sh` checks out the pinned source again to restore symbolic links.
These downloads are not a complete installation of the Linux environment.

The local MadGraph core uses a license adapted from Illinois/NCSA.
Vendor components may have other licenses; a single blanket MIT statement would not describe them.
