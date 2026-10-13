# Upstream reference results

[English](README.md) | [简体中文](README.zh-CN.md)

This local directory holds the author's results extracted from
`SMEFTsim_tutorial_results.zip`: compressed LHE files, ROOT histograms and reference PDFs.

These are upstream results, not the locally generated [examples](../examples/README.md).
The reference archive remains local; only this directory guide is included in Git.

## Where to find the ROOT files

The supplied reference package contains the author's ROOT files.
On the example Windows installation they are under:

```text
smeftsim/reference/Results/Root_files/
```

| File | Saved contributions |
|---|---|
| `Hvlvl_SM_run_01.root` | Direct SM sample and multiple reweighted contributions |
| `Hvlvl_SMEFT_run_01.root` | Direct squared dimension-six contribution |
| `Hvlvl_SMEFT_linear_run_01.root` | Direct ordinary SM–dimension-six interference |
| `Hvlvl_SMEFT_prop_run_01.root` | Direct linear propagator interference |

**The reference plot's multiple curves mainly come from different weight histograms in one SM ROOT file.**
The three direct EFT files serve separate consistency checks; merging them is not required to draw the reference plot.
The installation check reconstructed 92 histograms from the four upstream LHE files and compared their bin contents.
Freshly generated samples have statistical fluctuations and need not match the author's bins exactly.
The compressed reference LHE files are under `Results/Hvlvl_*/Events/run_01`.

Different official resources serve different purposes: the 2023 tutorial's result archive is separate
from [SMEFTsim UFO validation](https://github.com/SMEFTsim/UFO-validation).
Use the result archive corresponding to this exercise rather than expecting every UFO model to ship
with this particular ROOT sample.

This reference material is not needed to inspect the locally generated example.
See [handbook Section 6.5](../handbook.md#65-complete-lhe--root--pdf-with-the-authors-sample) for the
reference-analysis steps.
