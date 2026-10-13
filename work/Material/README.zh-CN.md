# 过程、卡与作者工作副本

[English](README.md) | [简体中文](README.zh-CN.md)

| 本地文件/目录 | 来源与功能 |
|---|---|
| `SMEFTsim_U35_MwScheme_UFO` | 教程 UFO；导入模型时读取粒子、参数、顶点与 restriction |
| `Hvlvl_SM` | SM 过程、Cards、编译代码与 Events |
| `Hvlvl_SM_manual` | 你的重加权操作副本，保护原 SM |
| `Hvlvl_SMEFT*` | 之前导出的独立 EFT 贡献过程；当前主线不要求重新运行 |
| `param_card_Hvlvl.dat` | 作者的 SM 参数起点，复制到过程 `Cards/param_card.dat` |
| `run_card_Hvlvl.dat` | 作者的运行卡，复制后修改事件数与种子 |
| `reweight_card_int.dat` | 四个单系数线性干涉参数点 |
| `reweight_card_squares.dat` | 四个单系数平方参数点 |
| `reweight_card_propW.dat` | 三个传播子/宽度贡献参数点 |
| `reweight_card_mix_*.dat` | 多系数混合项示例，当前练习不需要 |
| `launch_reweighting.sh` | 作者批量调用 reweight；默认过程与 run 名需核对 |
| `make_rootfiles.sh` | 作者批量解压并调用分析器；默认 `run_01` |
| `lhe_analyzer.py`、`plot_histos.py` | 作者 Python 2 分析和绘图原工作副本 |
| [pyroot_python3](pyroot_python3/README.zh-CN.md) | 当前 Linux 环境实际调用的两个 Python 3 兼容副本 |

这里的原作者文件来自 [教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)，
在本机使用并保留出处，不纳入本项目发布范围。
`Events/<run>/` 才是最终事件；`SubProcesses` 是生成器的构建和积分工作文件。
