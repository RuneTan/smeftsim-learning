# Local outputs

[English](README.md) | [简体中文](README.zh-CN.md)

This directory stores regenerable results and local run records.
Its guide is shared; output data and logs are excluded from Git.

The two workspaces use names by purpose. Installation records are kept in the Windows publishing workspace.

| Directory | Contents |
|---|---|
| `my_sm_visual` | SM analysis ROOT file and the PDFs/PNGs from Chapter 8 |
| `my_pyroot_reweighted` | Your reweighted ROOT file and PDFs from Chapter 9 |
| `example_reweighted` | Outputs produced when reanalyzing or replotting the shared example |
| `installation` | Local installation state, license checks and cleanup records |

The selected teaching result was copied to [examples/reweighted](../examples/reweighted/README.md).
Generating fresh files under `outputs` does not change that shared input.
Duplicate plots, decompressed inputs and old test directories can be regenerated.
Keep the active environment, original runs, cards and `vm/SMEFTsim/ext4.vhdx`.
