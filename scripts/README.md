# Local helper script

[English](README.md) | [简体中文](README.zh-CN.md)

`fix_axes.py` applies display fixes to the Python 3 plotting copy prepared in [setup Section 5](../docs/setup/README.md#5-prepare-the-two-python-3-analysis-scripts).
From the project root, with `.venv` activated and Ghostscript installed, run:

```bash
python scripts/fix_axes.py
```

It reads and updates `work/Material/pyroot_python3/plot_histos.py`, correcting axis labels, panel spacing, SM-only layout and PDF font embedding. It preserves histogram calculations and the upstream originals in `tutorial`.
Before its first patch, it keeps a local backup at `.maintainer-notes/axes/plot_histos.before.py`; repeating the command leaves an already corrected copy unchanged.
The project root is resolved from the script's location, so it also works when invoked by absolute path from another directory.

Return to the [handbook](../docs/handbook.md) or [repository overview](../README.md).
