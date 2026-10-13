# 过程、卡与教程工作副本

[English](README.md) | [简体中文](README.zh-CN.md)

配套 UFO、输入卡和分析脚本是 [Ilaria Brivio 的 2023 年 6 月 SMEFTsim 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) 的本地副本；`Hvlvl_*` 过程目录是生成的工作文件。

| 本地文件/目录 | 来源与功能 |
|---|---|
| `SMEFTsim_U35_MwScheme_UFO` | 教程 UFO；导入模型时读取粒子、参数、顶点与 restriction |
| `Hvlvl_SM` | SM 过程、Cards、编译代码与 Events |
| `Hvlvl_SM_manual` | 你的重加权操作副本，保护原 SM |
| `Hvlvl_SMEFT*` | 之前导出的独立 EFT 贡献过程；当前主线不要求重新运行 |
| `param_card_Hvlvl.dat` | SM 参数起点，复制到过程 `Cards/param_card.dat` |
| `run_card_Hvlvl.dat` | 运行卡，复制后修改事件数与种子 |
| `reweight_card_int.dat` | 四个单系数线性干涉参数点 |
| `reweight_card_squares.dat` | 四个单系数平方参数点 |
| `reweight_card_propW.dat` | 三个传播子/宽度贡献参数点 |
| `reweight_card_mix_*.dat` | 多系数混合项示例，当前练习不需要 |
| `launch_reweighting.sh` | 批量调用 reweight；默认过程与 run 名需核对 |
| `make_rootfiles.sh` | 批量解压并调用分析器；默认 `run_01` |
| `lhe_analyzer.py`、`plot_histos.py` | 教程的 Python 2 分析和绘图工作副本 |
| [pyroot_python3](pyroot_python3/README.zh-CN.md) | 当前 Linux 环境实际调用的两个 Python 3 兼容副本 |

复制的教程文件在本机使用并保留出处，不纳入本项目发布范围。
`Events/<run>/` 才是最终事件；`SubProcesses` 是生成器的构建和积分工作文件。
