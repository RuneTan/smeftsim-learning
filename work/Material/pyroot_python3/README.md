# Local Python 3 compatibility scripts

[English](README.md) | [简体中文](README.zh-CN.md)

| Script | Input | Output | Purpose |
|---|---|---|---|
| `lhe_analyzer.py` | Two arguments: input LHE and output ROOT file | Four histograms for each weight | Read four-momenta, fill bins, and normalize by the event count |
| `plot_histos.py` | One argument: input ROOT file | Four `plot_*.pdf` files | Plot the SM plus individual contributions, with ratios to the SM |

Source: Ilaria Brivio's
[SMEFTsim_tutorial_June23](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23),
pinned commit `92ffde994d7c0d90554ee629cc477ee171c76b84`.
The current working copies contain only the changes needed for Python 3: expand tabs, convert Python 2 syntax, and replace `file()` with `open()`.

No explicit license was found for the upstream tutorial. The two `.py` files therefore remain local and are ignored by Git.
This teaching repository includes the explanation and conversion instructions; the script copies are obtained locally from the linked tutorial.

## Prepare your own copies on a new machine

**Run these commands only if the two scripts are not already present in this directory.**
From the project root, with the project's Python 3.10 Linux environment activated, enter each complete line and press Enter:

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

Every command is one complete line. Wait for it to finish before entering the next.
`expand -t 8` expands indentation using Python's tab width; `lib2to3` converts the old syntax.
The last two commands modify only the newly created working copies. The upstream files in `tutorial/Material` are preserved.

These conversion steps were checked against the currently working copies by comparing syntax trees; both scripts have equivalent logic.
Use Python 3.10 for this lesson. Python 3.14 cannot run the `lib2to3` conversion shown here.

See the [main handbook](../../../handbook.md) for execution instructions, and the
[plot guide](../../../docs/figures/README.md) for units.
