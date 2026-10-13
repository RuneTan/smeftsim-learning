# Publishing to GitHub: attribution, licenses and WSL files

[English](README.md) | [简体中文](README.zh-CN.md)

## 1. Attribution and permission are separate requirements

The [root README](../../README.md) lists upstream tutorials, authors, versions, papers and this project's changes.
This helps readers distinguish the original tools from these teaching notes, but it does not replace permission
to redistribute material. A publicly readable repository does not automatically permit copying all its code.
[GitHub's licensing guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
explains the default copyright rules when a license is absent.

Checked on 2026-10-13:

| Source | Finding | Publication approach |
|---|---|---|
| [SMEFTsim v3.0.2](https://github.com/SMEFTsim/SMEFTsim/blob/v3.0.2/LICENSE) | MIT | Attribute the parameter reference and retain the license; download model source locally |
| MadGraph 2.9.27, `madgraph/LICENSE` | Adapted from Illinois/NCSA; retain notices and do not imply endorsement | Download locally; retain its license as a record of the example's source |
| [ROOT](https://root.cern/about/license/) | LGPL 2.1 or later; some components have other licenses | Local dependency only; environments and binaries are excluded |
| [Ilaria Brivio's 2023 tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) | No LICENSE found in the pinned copy; GitHub API license field was null | Download upstream; tutorial source, card copies and Python 3 script copies are excluded |

Do not apply SMEFTsim's MIT license automatically to the independent tutorial scripts.

**Sharing tutorial files:** before redistributing tutorial scripts, modified Python 3 copies,
tutorial cards or text, ask Ilaria Brivio to confirm the scope of permission and the applicable license.
Explain the teaching purpose, attribution and minimal Python 3 conversion, and list the files you wish to share.
The current publication scope excludes those copies, so publishing these notes does not depend on an email reply.

Numerical results do not automatically inherit a program's source-code license merely because the program generated them.
Embedded program text or upstream material still needs separate consideration.
[GNU's explanation of program output](https://www.gnu.org/licenses/gpl-faq.en.html#WhatCaseIsOutputGPL)
describes this distinction. The public LHE omits the full generator banner and card templates,
while preserving numerical initialization data, events and weights. Input settings and provenance
are recorded in the [example metadata](../../examples/reweighted/metadata.json).

No project-wide license has yet been selected for these original notes and helper scripts.
Public uploading and granting open-source reuse rights are different decisions.
A future project license must preserve upstream rights and must not claim ownership of all third-party material.

## 2. Moving Linux files into the repository

**Upload ordinary files, not the WSL virtual disk.** GitHub receives files in Git commits;
their original Windows or Linux location does not matter.

The Windows `smeftsim` folder is the documentation and publication directory;
Linux `/home/smeft/smeftsim` remains the runtime directory.
The selected result is already in [examples/reweighted](../../examples/reweighted/README.md).
The public LHE is an analysis export; ROOT and PDF files retain their original checksums.
The complete raw run remains local. Do not upload `ext4.vhdx`.

To copy another result, open WSL from Windows.
**Windows PowerShell: enter the complete line and press Enter once.**

```powershell
explorer.exe '\\wsl.localhost\SMEFTsim\home\smeft\smeftsim\outputs'
```

Copy selected results into `examples/YOUR_EXAMPLE` and record versions, parameters, seed, event count and sources.
Check generated headers for copied upstream material before publishing.

You can also copy directly in WSL. The following is a **future-use illustration**:
replace the destination and review the copied file before publishing.
The current example already exists; do not overwrite it by repeating this command.

```bash
cp /home/smeft/smeftsim/work/Material/Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz '/mnt/c/Users/YOUR_USERNAME/PROJECT_PATH/smeftsim/examples/YOUR_EXAMPLE/events.lhe.gz'
```

## 3. Committing the Windows project from WSL

This method uses a Linux terminal to commit the curated Windows folder.
There is no need to move all documents and dependencies back into Linux.

The commands below explain manual publication. For a new project, first create an empty GitHub repository
without automatically adding README, LICENSE or `.gitignore`.
[GitHub's repository-import instructions](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
describe the same workflow. For a repository already published, skip initialization and use its existing `origin`.

### A. Initialize a local repository

**Linux Bash: enter each complete command, press Enter and wait.**
Replace the path with your Windows project location.
On the original machine it is `/mnt/c/Users/符文/Desktop/NSBI/smeftsim`.

```bash
cd '/mnt/c/Users/符文/Desktop/NSBI/smeftsim'
git init -b main
git config user.name "YOUR_COMMIT_NAME"
git config user.email "YOUR_GITHUB_COMMIT_EMAIL"
git status --short
```

Without `--global`, these settings apply only to this repository.
The commit name and email identify commits; they are not login credentials.

### B. Stage and inspect the publication scope

**Linux Bash: run one complete command at a time.**

```bash
git add .
git diff --cached --stat
git ls-files
```

Expect bilingual documents, helper scripts, original process cards, license records and selected examples.
Exclude `.venv`, `ext4.vhdx`, third-party source, tutorial script copies, bulk logs and credentials.
The `.gitignore` explicitly allows only the selected LHE/ROOT example.
Previously tracked files remain tracked after adding an ignore rule; inspect the file list.

### C. Commit, configure the remote and upload

**Linux Bash: run one command at a time; replace the GitHub username and repository name.**

```bash
git commit -m "Add bilingual SMEFTsim learning notes and local reweight example"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git remote -v
git push -u origin main
```

`git commit` records changes locally; `git push` sends them to GitHub.
HTTPS requires GitHub authentication; an account password cannot replace a token.
[GitHub's Git setup guide](https://docs.github.com/en/get-started/git-basics/set-up-git)
describes HTTPS, SSH and credential options. Keep tokens out of commands, documents and remote URLs.
If `origin` already exists, inspect it instead of repeating `remote add`.

Windows Git Bash or GitHub Desktop can commit the same folder.
If using a native Linux directory as the repository, copy these documents and ignore rules there first.
Continue to exclude the WSL disk image.

Return to the [handbook](../../handbook.md) or [root README](../../README.md).
