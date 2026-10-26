# SMEFTsim 学习教程

[English](README.md) | [简体中文](README.zh-CN.md)

这份独立的双语教程帮助读者用 SMEFTsim、MadGraph 和 ROOT，完成 Higgs 四轻子衰变的 SM 事件生成、分析及 SMEFT 重加权。
仓库提供操作手册、必要知识附录和自己生成的示例结果；运行软件直接从上游获取，在 Linux 中安装。

**第一次使用：先看 [安装指南](docs/setup/README.zh-CN.md)，再跟随 [handbook](docs/handbook.zh-CN.md)。**
安装指南先按你的现有环境分流：原生 Linux 或虚拟机、已有 WSL2 Ubuntu，或新建专用 WSL2；再将固定版本下载、单一 `.venv`、分析脚本准备和安装校验串在一起。
手册在调用旁解释读取、改变和写出的内容；分析与画图直接调用本地准备的教程脚本，无需手打画图程序。
所有操作在同一个 Linux 项目目录完成；无需逐个寻找运行目录的说明，也无需 Windows 项目副本。

| 阅读入口 | 用途 |
|---|---|
| [安装指南](docs/setup/README.zh-CN.md) | 选择已有或新建 Linux 环境，获取固定版本软件并检验示例 |
| [handbook](docs/handbook.zh-CN.md) | 模型与卡 → 生成自己的 SM → 重加权 → 分析和画图 |
| [知识附录](docs/README.zh-CN.md) | 需要时查物理、模型、阶数、参数、图或 Linux 入门 |
| [探测器链练习](https://github.com/RuneTan/detector-learning) | 继续学习独立的 Pythia → Delphes / Parnassus 教程 |
| [示例结果](examples/reweighted/README.zh-CN.md) | 2,000 个事件、11 个额外权重、ROOT 直方图与 PDF |
| [来源与许可证](THIRD_PARTY_NOTICES.zh-CN.md) | 软件、教程和本仓库材料的来源及许可范围 |

![本项目自行生成样本的重加权分布](docs/figures/rw_mmv.png)

图使用本地事件和 Ilaria Brivio 2023 教程 `plot_histos.py` 的 Python 3 副本，并作了本地显示修正。
坐标轴表示运动学变量和每 bin 的部分衰变宽度贡献，见 [图的说明](docs/figures/README.zh-CN.md)。

## 来源与致谢

| 项目或教程 | 作者/维护者 | 本项目如何使用 |
|---|---|---|
| [SMEFTsim 教程索引](https://smeftsim.github.io/tutorials.html) | SMEFTsim 项目 | 选择学习路线 |
| [2023 年 Higgs 衰变教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) | Ilaria Brivio | 过程、卡、UFO、分析器和绘图方法；固定提交 `92ffde994d7c0d90554ee629cc477ee171c76b84` |
| [SMEFTsim](https://github.com/SMEFTsim/SMEFTsim) | Ilaria Brivio、Yun Jiang、Michael Trott 等贡献者 | 教程模型 v3.0.2；模型与理论说明 |
| [MadGraph5_aMC@NLO](https://github.com/mg5amcnlo/mg5amcnlo) | MadTeam | 生成器 2.9.27；固定提交 `eb76cab72b8d44aac7162ac7221ac08a4384a169` |
| [ROOT / PyROOT](https://root.cern/) | ROOT 团队 | 读取直方图与绘图 |
| [SMEFTsim 3.0 practical guide](https://arxiv.org/abs/2012.11343) | Ilaria Brivio | 背景、参数与模型实现 |
| [The SMEFTsim package, theory and tools](https://arxiv.org/abs/1709.06492) | I. Brivio、Y. Jiang、M. Trott | 原始包的理论和工具说明 |
| [Warsaw basis](https://arxiv.org/abs/1008.4884) | B. Grzadkowski、M. Iskrzyński、M. Misiak、J. Rosiek | 算子基底的参考 |
| [PDG Kinematics](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf) | Particle Data Group | 宽度、相空间与运动学定义 |
| [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install) | Microsoft | 专用 Linux 运行环境 |

模型、生成器和教程的署名见上表。这是独立的学习整理，不代表所列项目或贡献者背书。
用于科学论文时，请按所使用工具的要求引用相关论文。

## 仓库包含什么

公开仓库保留文档、图片、参数索引、示例数据与来源/许可证记录。
MadGraph、ROOT、UFO、原教程和 Python 3 脚本副本在 Linux 安装时获取或准备，不随本仓库分发。
`.venv`、`tutorial`、`tools`、`work`、`reference`、`outputs` 都是本地运行目录，由安装或操作命令创建并由 Git 忽略。

示例 `examples/reweighted` 来自本地生成，不是上游参考结果的复制。
公开 LHE 是分析导出，保留数值初始化、事件和权重，省略完整软件模板和卡片文本；设置和校验值记录在 `metadata.json`。
SMEFTsim 模型的 MIT 许可不自动覆盖独立教程或整个教学仓库。
本项目自有文档尚未选择统一的再使用许可证；第三方许可及署名记录见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.zh-CN.md)。
