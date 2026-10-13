# If you are new to Linux

[English](README.md) | [简体中文](README.zh-CN.md)

This optional guide explains the terminal conventions used in this project: Bash commands, paths, Python prompts and MadGraph menus. Read the sections you need when an input step is unfamiliar.

The examples use this project's WSL environment, Linux user `smeft` and runtime directory `/home/smeft/smeftsim`. Substitute your own username and paths where needed.

Return to the [main handbook](../../handbook.md) for the SMEFTsim exercises. For installation on a new machine, use the [setup guide](../setup/README.md).

## Contents

1. [Ordinary terminal commands: finish the whole command, then press Enter once](#1-ordinary-terminal-commands-finish-the-whole-command-then-press-enter-once)
2. [Use the prompt to identify your current environment](#2-use-the-prompt-to-identify-your-current-environment)
3. [Distinguish interactive Python from editing a file](#3-distinguish-interactive-python-from-editing-a-file)
4. [Read the common Linux commands used in this tutorial](#4-read-the-common-linux-commands-used-in-this-tutorial)
5. [How to read paths](#5-how-to-read-paths)

## 1. Ordinary terminal commands: finish the whole command, then press Enter once

In the main handbook, `bash` and `powershell` blocks follow the same rule:

1. Copy or type **one complete command**.
2. Press **Enter once** to execute it.
3. Wait for it to finish and for the terminal prompt to return before typing the next command.
4. When a block contains several commands, run them one at a time in order; do not execute the entire block immediately.

**A line wrapping on screen does not start a new command.** A long command may occupy two screen lines,
but you must enter all of it before pressing Enter. Do not press Enter immediately after `.lhe`, or omit `>` or the output path.
Blank lines in ordinary terminal blocks are only for readability; you do not need to type them.

Executable terminal blocks in the main handbook are marked "one command at a time."
For a block containing `cd ...` followed by `python ...`, enter the complete `cd` command and press Enter,
wait for the prompt, then enter the complete `python` command and press Enter.

## 2. Use the prompt to identify your current environment

| Prompt shown by the terminal | Current environment | What to enter |
|---|---|---|
| `PS C:\...>` | Windows PowerShell | Commands in `powershell` blocks |
| `smeft@...:~/smeftsim$`, or similar | Linux Bash | Commands in `bash` blocks |
| `>>>` | Interactive Python interpreter | Code marked "interactive Python" |
| `...` | Python is waiting for an unfinished statement or indented block | Continue the statement; finish a loop with one blank line |
| `MG5_aMC>`, `MadEvent>`, or a tool-selection menu | MadGraph/MadEvent | The answer requested by the current menu, or a MadGraph command |

These are **prompts displayed by the terminal**; do not include them when typing a command.
Once you enter Linux, a Windows path such as `C:\...` cannot be used directly.
At Python's `>>>` prompt, do not enter Bash commands such as `cd` or `ls`.

If Linux displays a lone `>` and waits, your input usually contains an unclosed quote or unfinished statement.
Press `Ctrl+C` to cancel the unfinished input, then copy the complete command again.
A `>` **inside a command**, however, redirects output. It is part of the command and must stay.

Typing `python` and pressing Enter switches from Bash to Python's `>>>` prompt.
In Python, type `exit()` and press Enter to return to Bash.
In Bash, type `exit` and press Enter to leave the Ubuntu terminal; this differs from `exit()`.
`deactivate` only leaves the virtual environment, keeping the Linux terminal open.

## 3. Distinguish interactive Python from editing a file

- **Ordinary Python statements:** at `>>>`, enter one complete line and press Enter once; `>>>` should return when it finishes.
- **Python loops:** enter each line and press Enter, preserving indentation. After the last line, Python still displays `...`.
  **Type nothing and press Enter once more** to run the loop. [Handbook Section 8.6](../../handbook.md#86-use-root-to-plot-your-own-sm-distributions) gives line-by-line instructions.
- **Editing files:** code marked "file contents" belongs in the named file, opened in an editor.
  In the editor, Enter only inserts a new line. Press `Ctrl+S` to save your changes; do not execute these contents in the terminal.
- **Names, logs, and illustrations:** `text` blocks, file listings, and diagrams are usually for reading,
  not typing. Examples explicitly identified as MadGraph commands belong inside that tool.

If an error occurs, stop at the current step and check the environment, directory, complete arguments, and error message.
Do not paste later plotting commands into an unfinished loop or menu.

## 4. Read the common Linux commands used in this tutorial

| Command | What it does | What you normally see after pressing Enter |
|---|---|---|
| `pwd` | Shows the current directory | One absolute path |
| `cd directory` | Changes the current directory | Usually no output; the directory in the prompt changes |
| `mkdir -p directory` | Creates a directory, or reuses it if it exists | Usually no output on success |
| `source .venv/bin/activate` | Makes this terminal use the project's Python and dependencies | Often `(.venv)` in the prompt; check with `which python` |
| `which python` | Shows which Python interpreter is selected | Here, `/home/smeft/smeftsim/.venv/bin/python` |
| `ls -lh file` | Checks whether a file exists and displays its size | Filename, time, and a readable size |
| `head -n 1 file` | Shows the first line | An LHE file should start with `<LesHouchesEvents ...>` |
| `cat file` | Prints a card or text file | Its contents; the file is unchanged |
| `cp source destination` | Copies a file or directory | Usually returns quietly; an existing destination may be overwritten |
| `gzip -dc compressed_file > new_file` | Decompresses into a new file, keeping the compressed original | Usually no output on success; check with `ls` |
| `python script.py arguments...` | Runs a script with the current interpreter | Script logs, results, or an error |
| `./process/bin/generate_events run_name` | Starts the generator under the current directory | A tool menu, followed by integration and generation logs |
| `zcat file.gz \| sed ...` | Decompresses into a stream, then selects part of it | Here, the weight declarations; keep the pipe character `\|` |

For `gzip`, `-d` means decompress and `-c` sends the contents to standard output.
`>` then writes that output to the named file. It overwrites an existing file with the same name,
so use a separate output directory for each exercise.
The script filename after `python` does not count as a script argument:
`lhe_analyzer.py` needs two arguments, "input LHE + output ROOT";
`plot_histos.py` needs one, "input ROOT."

## 5. How to read paths

The main Linux working directory is `/home/smeft/smeftsim`.
Here, `~` means `/home/smeft`, so `~/smeftsim` identifies the same directory.
`outputs/my_pyroot_reference/events.lhe` is a relative path, interpreted from the project root.
`../../work/...` means go up two directory levels before locating the script.
Use `/mnt/c/...` to access the Windows C drive from Linux.

Linux filenames are case-sensitive: `Material` and `material` are different directories.
Copy quotes together with paths that are enclosed in single or double quotes.
If a step first asks you to `cd` into a directory, execute that command and press Enter before copying the script command.

Return to the [main handbook](../../handbook.md) for the SMEFTsim exercises. For installation on a new machine, use the [setup guide](../setup/README.md).
