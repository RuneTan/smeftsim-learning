# SMEFTsim 学习与操作手册

[English](handbook.md) | [简体中文](handbook.zh-CN.md)

新电脑先完成 [安装指南](docs/setup/README.zh-CN.md)，再执行本手册的运行步骤。

这是一份基于[Ilaria Brivio 的 2023 年 6 月 SMEFTsim 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)的实践笔记，学习目标是：
**理解 SMEFT → 读参考图 → 生成自己的 SM 样本并画图 → 用重加权比较 EFT 贡献。**

本手册使用 Linux 项目的统一 `.venv` 环境和 ROOT。
作者原始材料保留在 `tutorial`；本地分析和绘图使用 Python 3 兼容副本。
来源与阅读入口见 [根 README](README.zh-CN.md)，脚本功能与运行目录见 [安装指南](docs/setup/README.zh-CN.md)。
第 6、8、9 节统一调用教程已有的分析与绘图脚本，不需要手打画图程序。主要练习是理解模型、配置卡、生成事件和计算额外权重。

如果你不熟悉 Linux 或终端操作，可查阅可选的 [Linux 与终端入门手册](docs/linux-basics/README.zh-CN.md)。
已有 SM 样本时，从第 8.5–8.6 节得到自己的图，再完成第 9.3–9.4 节。
完成第 9 节即可结束这一轮教学练习。

所有工作命令都在 Linux 项目 `~/smeftsim` 中执行。安装指南创建名为 `SMEFTsim` 的 WSL 发行版和用户 `smeft`；名称不同时请替换。
公开仓库保留教学资料与选定结果，软件和环境在本地从上游获取并安装。

## 目录

1. [学习目标与运行前提](#1-学习目标与运行前提)
2. [SMEFT 的背景知识](#2-smeft-的背景知识)
3. [SMEFTsim 的功能与边界](#3-smeftsim-的功能与边界)
4. [环境隔离与文件位置](#4-环境隔离与文件位置)
5. [启动环境与核对依赖](#5-启动环境与核对依赖)
6. [用作者的 ROOT 脚本复现参考图](#6-用作者的-root-脚本复现参考图)
7. [选择模型与理解过程命令](#7-选择模型与理解过程命令)
8. [亲手生成一个 SM 样本](#8-亲手生成一个-sm-样本)
9. [重加权与 ROOT 绘图](#9-重加权与-root-绘图)
10. [保存与复现结果](#10-保存与复现结果)
11. [学习节奏与掌握标准](#11-学习节奏与掌握标准)
12. [版本与参考资料](#12-版本与参考资料)

## 1. 学习目标与运行前提

完成本项目后，你应能：

1. 说明模型的 flavor、scheme、restriction 和 EFT 阶数。
2. 设置卡并生成一个独立命名的 SM run。
3. 解释 LHE 事件如何变成 ROOT 直方图，并调用现有脚本得到四个分布。
4. 读懂作者 reweight 卡，计算指定系数的贡献并与 SM 比较。

当前操作环境采用下列固定组合：

| 组件 | 本教程使用的配置 | 作用 |
|---|---|---|
| Linux | 项目专用 WSL2 Ubuntu 22.04，发行版名 `SMEFTsim` | 运行生成器与编译器 |
| Python | 3.10，Linux 项目内的 `.venv` | 同时运行生成、重加权与 ROOT |
| MadGraph | 2.9.27 | 生成过程、积分、事件和重加权 |
| SMEFTsim UFO | 教程 v3.0.2，U35 / MwScheme | 定义相互作用和输入参数 |
| NumPy / setuptools | 1.26.4 / 69.5.1 | 保留这条重加权路线所需的构建接口 |
| ROOT | 官方 Python 分发 0.1a12，对应 6.40.00 | 保存直方图与画图 |

这套配置已完成本地运行检查。精确依赖见 [docs/setup/requirements.txt](docs/setup/requirements.txt)。固定版本用于复现这份教程，不代表最新研究默认配置。

本手册的终端操作从**已准备好专用 Linux 环境**开始。
新电脑需先准备 WSL2/Ubuntu、Python 虚拟环境、编译器和第三方材料；
第 4 节说明目录，下载与环境准备统一见 [安装指南](docs/setup/README.zh-CN.md)。

## 2. SMEFT 的背景知识

完整背景移到 [docs/physics/README.md](docs/physics/README.zh-CN.md)；操作时按问题查阅即可。

### 2.1 为什么需要有效场论

高能新物理在低能过程里表现为额外相互作用。
[解释与展开](docs/physics/README.zh-CN.md#21-为什么需要有效场论)。

### 2.2 Wilson 系数、能标与单位

本教程的 Wilson 系数无量纲，能标以 GeV 输入；二者必须一起记录。
[公式与单位](docs/physics/README.zh-CN.md#22-wilson-系数能标与单位)。

### 2.3 Warsaw basis 是什么

它是消除冗余后的独立算子基底；场强本身包含导数。
[基底、导数与学习范围](docs/physics/README.zh-CN.md#23-warsaw-basis-是什么)。

### 2.4 为什么要区分线性项和平方项

SM、干涉、维六平方是振幅平方中的不同贡献，维六平方不构成完整的高阶 EFT 预测。
[完整说明](docs/physics/README.zh-CN.md#24-为什么要区分线性项和平方项)。

### 2.5 Flavor：新相互作用怎样区分不同代的费米子

本教程选 U35，不同 flavor 假设对应不同的代际关系。
[五种选择的物理含义](docs/physics/README.zh-CN.md#25-flavor新相互作用怎样区分不同代的费米子)。

### 2.6 Scheme：用哪些测量值确定电弱参数

MwScheme 使用 mW、mZ、GF 作为电弱输入。
[输入方案与参数推导](docs/physics/README.zh-CN.md#26-scheme用哪些测量值确定电弱参数)。

### 2.7 微分宽度：把一个衰变道的速率分配到运动学区域

本例积分量是部分衰变宽度，单位 GeV。直方图 bin 内容与除以 bin 宽后的密度不同。
[公式、符号与直方图解释](docs/physics/README.zh-CN.md#27-微分宽度把一个衰变道的速率分配到运动学区域)。

## 3. SMEFTsim 的功能与边界

### 3.1 它提供什么

SMEFTsim 提供 FeynRules/UFO 模型，供生成器计算；它不独立产生事件。

### 3.2 软件链中的职责

主线是 **UFO + 卡 → MadGraph → LHE 事件 → LHE 新权重 → ROOT 直方图 → PDF**。
每一步都会把文件或目录交给下一个程序：

| 环节 | 读取什么 | 做什么 | 输出什么；下一步谁读取 |
|---|---|---|---|
| 导入 SMEFTsim 模型 | UFO 和选定的 restriction | 提供粒子、相互作用和参数公式；删去 restriction 排除的相互作用 | MadGraph 内的模型，供后续构造矩阵元 |
| MadGraph 导出过程 | 已导入模型和 `generate ...` 命令 | 为指定过程与耦合阶数构造数值代码 | `Hvlvl_SM/`；其中的 `bin/generate_events` 用来运行计算 |
| MadEvent 生成 | 过程代码、`param_card.dat`、`run_card.dat` | 编译、积分衰变宽度、在相空间中抽样 | 压缩 LHE 事件和 banner；由重加权程序或分析器读取 |
| MadEvent 重加权 | 原始 LHE 和 `reweight_card.dat` | 在相同事件运动学上计算选定贡献 | 写入同一 LHE 的额外权重；由分析器读取 |
| `lhe_analyzer.py` | 一份解压后的 LHE | 根据粒子动量重建四个观测量，为每个观测量和权重填直方图 | 一个 ROOT 文件；由绘图器读取 |
| `plot_histos.py` | 一个 ROOT 文件 | 画出已有直方图；有修正项时分别将其加到 SM 上 | 四张 `plot_*.pdf`；由你阅读 |

LHE 保存逐粒子的事件记录和权重；这里的 ROOT 文件保存**分 bin 的汇总**，不是新的一批事件。
改显示范围不用重新生成事件；只在卡里改 Wilson 系数也不会自动改变结果，必须运行相应生成或重加权命令。
本次 Higgs 衰变练习不包含 Pythia、Delphes 或探测器响应。计算边界见 [软件说明](docs/model/README.zh-CN.md)。

### 3.3 计算范围要明确

本例是树级 Higgs 四轻子衰变；运行成功不自动证明完整物理精度。
模型和近似的边界见 [软件说明](docs/model/README.zh-CN.md#33-计算范围要明确)。

### 3.4 官方 Mathematica Notebook 用来做什么

Notebook 用于解析费曼规则和模型开发；已有 UFO 时不需要先运行它。
[Notebook 用途与两条工作路径](docs/model/README.zh-CN.md#34-smeftsim-的-mathematica-notebook-用来做什么)。

## 4. 环境隔离与文件位置

生成、重加权与 ROOT 共用 Linux 项目的 `.venv`。编译器及系统依赖安装在专用 WSL/Ubuntu 中，Windows Python 不参与计算。

所有操作都在一个 Linux 项目目录 `~/smeftsim` 中进行。新的分析练习使用短目录 `outputs/ref`、`outputs/sm`、`outputs/rw`，以前的本地输出可以留在原处；不再维护 Windows 与 Linux 两份项目副本。
Windows 只负责启动 Linux，并保存 WSL 虚拟磁盘。
若已完成旧版教程，可以继续使用已有 LHE 和 ROOT：仅因新版缩短输出目录名，不需要重新生成事件。
在分析和绘图命令中沿用已有路径，或按下文创建新的分析目录即可。
重复分析前先检查目标位置：Shell 的 `>` 会替换目标 LHE 副本，分析器会替换输出 ROOT，绘图器会替换同名 PDF。希望保留上一次练习时，请选另一个输出目录。

| 内容 | 位置 |
|---|---|
| 本手册与知识附录 | `handbook.zh-CN.md`、[docs](docs/README.zh-CN.md) |
| 仓库示例结果 | [examples/reweighted](examples/reweighted/README.zh-CN.md) |
| Python 环境 | `.venv`，本地安装时创建 |
| 原教程、MadGraph、工作文件、参考数据与输出 | `tutorial`、`tools`、`work`、`reference`、`outputs`，本地安装或操作时创建 |

软件获取、脚本功能和运行目录的说明集中在 [安装指南](docs/setup/README.zh-CN.md)。

## 5. 启动环境与核对依赖

### 5.1 进入项目 Linux

如果已在 Linux Bash 中，直接进入第 5.2 节。
Windows 用户在 **PowerShell** 中输入完整命令并回车一次：

```powershell
wsl -d SMEFTsim -u smeft --cd ~
```

这是安装指南采用的发行版与用户名；你使用其他名称时替换它们。
看到 Linux 提示符后才输入 Bash 命令。

### 5.2 激活统一环境

**Linux Bash｜逐条回车：** 每行是一条完整命令，回车后等待提示符返回。

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
gfortran --version
```

检查：

- `python --version` 应为 Python 3.10。
- `which python` 应指向 `/home/<your-user>/smeftsim/.venv/bin/python`。
- ROOT 应输出 `6.40.00`；编译器应能显示版本。

成功后继续第 6 节。同一终端可以连续完成生成、重加权和绘图，不用切换环境。
退出虚拟环境输入 `deactivate` 并回车；退出 Linux 输入 `exit` 并回车。

## 6. 用作者的 ROOT 脚本复现参考图

这一章在统一项目 `.venv` 内使用 PyROOT 和作者脚本的 Python 3 兼容副本。
操作链为：**LHE → `lhe_analyzer.py` → ROOT 直方图 → `plot_histos.py` → 四张 PDF**。
先用作者已有样本熟悉调用方式，再将输入换成自己的重加权 SM 样本。
纵轴、曲线面积和归一化的含义见第 2.7 节。

### 6.1 我们实际模拟什么

过程是：

$$h\to e^-\bar\nu_e\mu^+\nu_\mu.$$

它对应 Higgs 通过两个 W 的中间态产生四个轻子。
$m_h$ 小于两个 on-shell W 的质量之和，不能把两个 W 都当作 on-shell 粒子处理。
四体末态的运动学让我们比较 EFT 对不同区域的影响。

| 图名 | 观测量 | 含义 |
|---|---|---|
| `mll` | $m_{e\mu}$ | 带电轻子对的不变质量 |
| `mmv` | $m_{\mu\nu_\mu}$ | muon 与相应 neutrino 的不变质量 |
| `pTl1` | $\max(p_T^e,p_T^\mu)$ | 横动量较大的带电轻子的横动量 |
| `pTmu` | $p_T^\mu$ | muon 横动量 |

这些是生成器级变量；使用 neutrino 真值动量不代表真实探测器能直接测量同一个量。

这里是 Higgs **衰变**，积分结果是部分宽度 $\Gamma$，单位 GeV。
本地绘图副本将每 bin 的贡献标为 $\Delta\Gamma_{\mathrm{bin}}$ [GeV]；除以 bin 宽才得到微分宽度。
对散射过程才应根据生成器约定讨论截面等量，不能把此例的单位照搬过去。

### 6.2 看上半图还是下半图

作者上半图画各个运动学 bin 的宽度贡献；除以 bin 宽度才得到微分宽度。下半图是：

$$R(X)=\frac{(\text{SM}+\text{一个指定贡献})(X)}{\text{SM}(X)}.$$

黑线表示 SM；每条彩线只添加一个指定贡献，用来观察它的作用。
例如 `SM + cHl3 quadratic` 没有同时加入线性项。
因此不能把这一条曲线直接叫作 `cHl3=1` 的完整 EFT 预测。
作者图只展示中心值，没有统计误差带；SM 为零或统计稀疏的 bin 不适合作比值判断。

来自 [官方教程](https://smeftsim.github.io/tutorials.html) 的观察任务是：

- `cHbox`、`cll1` 线性项在这个例子中产生平坦比值，说明主要影响 rate。
- `cHW`、`cHl3` 线性项给出非平坦比值，说明还影响 shape。
- 传播子修正在 W 接近 on-shell 的区域值得关注。
- 此例中所用系数的平方项较小；这不是所有能区和系数的普遍规律。

本例作者 SM 样本的积分宽度约为 $1.00868\times10^{-5}\ \mathrm{GeV}$。
以后自己的小样本不必与最后几位数相同，需要连同积分误差来比较。

### 6.3 参考 ROOT 文件在哪里

按安装指南解压后，ROOT 文件在 Linux 项目内的 `reference/Results/Root_files`，LHE 文件在 `reference/Results/Hvlvl_*/Events/run_01`。
数据来自 Ilaria Brivio 教程随附的结果压缩包，不需要另外寻找 ROOT 下载链接。
[解压与文件检查步骤](docs/setup/README.zh-CN.md#7-解压参考结果并继续学习)。

### 6.4 激活 PyROOT，保留作者脚本

第 5 节激活的统一 `.venv` 已包含 ROOT；日常不切换环境。
实际调用 Linux 的 `work/Material/pyroot_python3/lhe_analyzer.py` 和 `plot_histos.py`。

原件、两个脚本的参数及新机器转换方法见
[安装指南第 5 节](docs/setup/README.zh-CN.md#5-准备两份-python-3-分析脚本)。已有安装可在 `~/smeftsim` 执行一次 `python fix_axes.py`，应用显示修正。
许可未明确的教程代码只在本地使用；公开仓库包含转换说明，不包含这些副本。

**Linux Bash，项目根目录，逐条回车：**

```bash
source .venv/bin/activate
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

Python 应来自项目 `.venv`，ROOT 应为 6.40.00。

### 6.5 先用教程样本完成 LHE → ROOT → PDF

**Linux Bash，已激活 `.venv`。** 下方每一行都是一条完整命令：完整输入，回车一次，等 Bash 提示符回来再继续。`gzip` 与 `> 输出路径` 必须在同一条命令中，屏幕自动折行不需要额外回车。
某条报错就停下来。更多终端操作解释见可选的 [Linux 入门](docs/linux-basics/README.zh-CN.md)。

#### A. 准备并检查 LHE 输入

```bash
cd ~/smeftsim
mkdir -p outputs/ref
gzip -dc reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz > outputs/ref/events.lhe
ls -lh outputs/ref/events.lhe
head -n 1 outputs/ref/events.lhe
```

`gzip -dc` 读取压缩样本而不修改原文件；`>` 将解压内容写入 `events.lhe`。
应得到约 **33 MiB** 的非空文件，开头为 `<LesHouchesEvents ...>`。
虽然文件名有 `SM`，这份随教程提供的样本已经包含额外重加权贡献，后面会用它们生成对比曲线。

#### B. 分析事件

```bash
python work/Material/pyroot_python3/lhe_analyzer.py outputs/ref/events.lhe outputs/ref/Hvlvl_SM.root
```

分析器需要**两个参数**：输入 LHE、输出 ROOT。两者都输入完整后再回车。
它读取粒子四动量和权重，计算 `mll`、`mmv`、`pTl1`、`pTmu`，为每个“观测量–权重”组合填直方图。
例如 `mmv_direct_sim` 保存 SM 贡献，`mmv_cHl3` 保存指定线性干涉贡献。
程序按实际事件数归一化，不要自己再除一次。
应看到 `processed 20000 events`、各贡献的积分值和 `file ... produced`，然后返回 Bash。
下一个程序读取这个 ROOT 文件，不再读取 LHE。

#### C. 画出已有直方图

```bash
cd outputs/ref
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
```

绘图器只需要**一个参数**，即输入 ROOT 文件；四张 PDF 写入**当前目录**。
它不计算新的矩阵元或事件权重，而是把选定修正分别加到 SM 上，再除以 SM 得到下半图。
应看到四张非空 PDF。WSL 用户可在 Bash 执行 `explorer.exe .`，用 Windows 打开当前目录。

检查点：沿着 `events.lhe → Hvlvl_SM.root → plot_mmv.pdf` 说出每个文件由哪个程序生成。
如果只想重画已有参考 ROOT，跳过 A–B，在 `~/smeftsim/outputs/ref` 使用这条替代命令：

```bash
python ../../work/Material/pyroot_python3/plot_histos.py ../../reference/Results/Root_files/Hvlvl_SM_run_01.root
```

选择一种绘图输入即可；再次调用会覆盖同名 PDF。学习这两次调用不需要使用批处理脚本 `make_rootfiles.sh`。

### 6.6 按需要调整作者已有的绘图设置

先保持作者默认设置完成第 6.5 节。
作者允许在 `plot_histos.py` 的 `weights_to_plot` 中选择曲线，
在 `histo_dc` 中修改显示范围。这些是可选设置，不是 Python 3 兼容要求。

如果希望只展示下面六个修正，
仅在 **Linux 工作副本** 中将 `weights_to_plot` 改为下面的文件内容。
**操作位置：文本编辑器，不是终端。** 编辑器里的回车只是换行；保留逗号、引号和括号，
完成后按 `Ctrl+S` 保存，再回到 Bash 运行绘图命令：

```python
weights_to_plot = [
    default_wgt,
    "cHbox",
    "cll1",
    "cHW",
    "cHl3",
    "cHl3_sq",
    "cHl3_propW",
]
```

作者 `pTl1` 的比值显示范围默认 `.95, 1.05`。
若曲线超出显示区，可把该处的两个范围值改为 `.68, 1.25`，
然后重新运行同一绘图命令。其他字典与算法保持原样。
文件中缺少的贡献不会被绘图程序计算出来；若缺一条曲线，先核对重加权标签。

作者原图的宽度单位、bin 宽和曲线含义见 [图的 README](docs/figures/README.zh-CN.md)。

## 7. 选择模型与理解过程命令

### 7.1 本例为什么选这个模型

模型为 `SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl`：
U35 flavor、MwScheme 电弱输入，以及教程自定义 restriction。
[模型说明](docs/processes/README.zh-CN.md#71-本例为什么选这个模型)。

### 7.2 Restriction 与参数卡不同

restriction 在导入时简化模型；参数卡设置本次运行的可调输入。
被导入时删除的顶点不会因为后来改参数卡就恢复。
[完整区别](docs/processes/README.zh-CN.md#72-restriction-与参数卡不同)。

### 7.3 阶数选项：先筛选振幅，再筛选振幅平方

| 目标 | 作者过程选项，均加 `SMHLOOP=0` |
|---|---|
| SM 基线 | `NP=0 NPprop=0` |
| 普通线性干涉 | `NP=1 NP^2==1 NPprop=0` |
| 普通维六平方 | `NP==1 NPprop=0` |
| 传播子干涉 | `NP=0 NPprop=2 NPprop^2==2` |

`NP=1` 是振幅层的上限，`NP==1` 是精确选择。
`NP^2` 在振幅乘积两侧相加计数；dummy vertices 的 `NPprop` 计数不是 EFT 插入次数。
展开公式、原来的两张详细表与 dummy 实现已移到
[docs/processes/README.md](docs/processes/README.zh-CN.md#73-阶数选项先筛选振幅再筛选振幅平方)。

### 7.4 UFO 中有哪些参数，哪些需要自己设置

本次主要记录模型、系数、`LambdaSMEFT`、宽度、种子和切选；
内部参数按模型公式计算，不能把它们都当成独立输入。
[参数分类与取值依据](docs/parameters/README.zh-CN.md)，
[完整参数索引](docs/parameters/model_parameter_reference.zh-CN.md)。

## 8. 亲手生成一个 SM 样本

**前提：环境已准备好并完成第 5 节检查。以下命令在 Linux Bash 中执行。**
第一次练习建议 2,000 个事件；这足以练习流程，精细分布比较时再增加统计量。

### 8.1 在 MadGraph 中导出过程

安装指南已准备好 `work/Material`。从 Linux Bash 逐条输入并回车，等提示符回来再继续：

```bash
cd ~/smeftsim
source .venv/bin/activate
cd work/Material
python ../../tools/MG5_aMC_v2_9_27/bin/mg5_aMC
```

最后一条进入 `MG5_aMC>` 提示符。接下来是 **MadGraph 命令**，每行输入完整后回车，等待执行完成；不要把它们当成 Bash 命令：

```text
set auto_update 0 --no_save
set auto_convert_model True --no_save
import model ./SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
display processes
```

这些命令的作用不同：

| 命令 | 本次含义 |
|---|---|
| `set ... --no_save` | 在当前会话关闭更新、允许本地模型转换，不修改保存的全局配置 |
| `import model ...` | 导入施加 `massless_Hvlvl` restriction 后的 SMEFTsim 相互作用 |
| `generate ...` | 选择 Higgs 衰变到 `e- ve~ mu+ vm` 并构造 SM 矩阵元，此时还没有抽样事件 |
| `display processes` | 打印已选过程，导出前发现末态或阶数设置错误 |

确认模型成功导入，选中的是预期衰变。
`generate h > ...` 中的 `>` 是 MadGraph 的过程语法，不是 Bash 的输出重定向。
首次导出时，在同一个 `MG5_aMC>` 中继续逐条执行：

```text
output Hvlvl_SM
quit
```

`output` 导出可用于数值计算的过程，不生成事件。`quit` 返回 Bash，此时仍在 `work/Material`。
检查导出文件：

```bash
ls Hvlvl_SM/Cards/param_card.dat Hvlvl_SM/Cards/run_card.dat
```

如果 `Hvlvl_SM` 已存在，跳过 `output`，只执行 `quit`，然后继续配置卡或使用新的 run 名称；不要覆盖已有过程。

### 8.2 设置卡

导出的过程决定**计算哪个矩阵元**，卡决定**使用哪些数值输入和抽样设置**。
先复制模板，使质量、宽度和切选约定与参考练习一致：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cd ~/smeftsim/work/Material
cp param_card_Hvlvl.dat Hvlvl_SM/Cards/param_card.dat
cp run_card_Hvlvl.dat Hvlvl_SM/Cards/run_card.dat
```

| 卡 | 主要内容 | 本次操作 |
|---|---|---|
| `param_card.dat` | 质量、耦合、Wilson 系数、能标、宽度 | EFT 系数全为零；`LambdaSMEFT=1000`；保留作者的宽度 |
| `run_card.dat` | 事件数、种子、积分和切选设置 | `nevents=2000`，`iseed=23456`，其余保留 |
| `reweight_card.dat` | 新参数点和新过程的权重定义 | SM 练习阶段暂不启用 |

在 **Linux Bash，当前目录 `~/smeftsim/work/Material`** 中，用终端编辑器打开两张卡；先完成第一张，再打开第二张：

```bash
nano Hvlvl_SM/Cards/param_card.dat
nano Hvlvl_SM/Cards/run_card.dat
```

进入 `nano` 后，修改表中指定的设置；按 `Ctrl+O` 保存，按 Enter 确认文件名，再按 `Ctrl+X` 返回 Bash。
在编辑器内，Enter 用于换行；卡内容不能当作 Bash 命令执行。
使用图形编辑器时按 `Ctrl+S` 保存，确认文件来自 Linux 工作目录。

确认修改的是 Linux 工作副本；事件数要改 `run_card.dat` 中的 `nevents`，
只给 run 起名 `...2000` 并不会让生成器自动生成 2,000 个事件。
卡的一般形式是 `数值 = 参数名` 或 `编号 数值 # 参数注释`，具体按原文件格式保留。

例如 `Block smeft` 中 `22 0.000000e+00 # cHl3` 将这个独立系数设为零；`Block smeftcutoff` 将 `LambdaSMEFT` 设为 1,000 GeV。
`nevents` 控制请求的事件数，`iseed` 控制伪随机抽样，两者都不改变相互作用模型。
这里计算衰变，没有质子束；通用卡虽然保留 beam/PDF 字段，不能由这些未使用条目推断是在做 13 TeV 碰撞。
切选保持模板原样：本例 `ptl=0` 没有正的下限，`ptlmax=-1` 表示不设上限，不要把探测器教程的 `ptl=10` 搬来这个参考衰变练习。
本练习没有 parton shower，也没有 matching/merging 环节；卡中不一定存在这些词本身。

检查点：找到 `cHl3`、`LambdaSMEFT`、`nevents`、`iseed`，说出它们各在哪张卡中。只修改卡不会生成事件。

### 8.3 生成一个独立命名的 run

**Linux Bash，当前目录 `work/Material`：**

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
./Hvlvl_SM/bin/generate_events training_sm_2000
```

`generate_events` 运行第 8.1 节导出的数值代码，读取刚才保存的两张卡。
编译生成可执行程序，积分估计部分宽度，事件抽样把粒子动量和权重写进 LHE。
`training_sm_2000` 选择结果目录，不是输入文件名，也不是事件数选项。

这条命令回车后会进入 MadGraph 的工具菜单，**此时不是普通 Bash**。
按下面顺序操作，不要把后面的分析命令提前粘进菜单：

1. 查看工具状态。需要关闭时，输入 `shower=OFF`，回车一次；
   `detector=OFF`、`analysis=OFF`、`reweight=OFF` 同样分别输入并回车。
   若某项已经为 OFF 或未安装，不必重复设置。
2. 工具状态确认后，输入 `done`，回车一次，进入下一步。
3. 若出现参数卡/运行卡编辑菜单，卡已按第 8.2 节保存时，输入该菜单的 `0` 或 `done`，
   回车一次，接受当前卡。若当前菜单不接受某个答案，以它显示的选项为准。
4. 接下来是积分、编译、生成日志。**等待，不连续按回车，也不输入其他命令。**
5. 只有程序结束并重新出现 Bash 提示符，才继续第 8.4 节。

`training_sm_2000` 是新 run 的名称。你已经用过这个名字时，先查看原结果；
要再生成一次，请换新名称，例如 `training_sm_v2`，并在后续路径中统一替换。
输出应位于 `Hvlvl_SM/Events/training_sm_2000`，其中包含 LHE 和 banner。
`smoke_sm_2000` 是安装检查的 run 名；这里用另一个名字保留它。

### 8.4 核对你生成了什么

`Hvlvl_SM/Events/training_sm_2000/` 下的重要输出是：

| 文件 | 查看什么 | 下一步用途 |
|---|---|---|
| `unweighted_events.lhe.gz` | LHE 头部、末态粒子记录和事件权重 | 第 8.5 节解压分析副本；原压缩文件留给第 9 节 |
| `training_sm_2000_tag_1_banner.txt` | 过程定义、卡和积分信息的快照 | 记录实际运行配置，避免把事后改过的卡当成当时输入 |

检查以下内容：

1. 过程是预期的 Higgs 衰变，模型和 restriction 没有换成其他版本。
2. banner 记录的参数、能标、种子和事件数与请求一致。
3. LHE 中有完整的事件和正确末态，积分宽度为正，并报告 MC 积分误差。
4. 与作者 SM 宽度和四个运动学分布比较；差异是否可由统计量与版本设定解释。

种子相同、版本相同、卡相同有助于复现，但不同编译器或并行方式也可能影响逐事件一致性。
科研记录应优先保存完整配置和统计结果，不把“末位数字相同”当作唯一标准。

### 8.5 为 SM 分布生成 ROOT 文件

**Linux Bash，已激活 `.venv`；每条命令完整输入后回车一次。** 输入是你自己生成的 LHE，不是参考样本。
在短分析目录 `outputs/sm` 建立解压副本：

```bash
cd ~/smeftsim
mkdir -p outputs/sm
gzip -dc work/Material/Hvlvl_SM/Events/training_sm_2000/unweighted_events.lhe.gz > outputs/sm/events_full.lhe
```

若使用其他 run 名，请统一替换 `training_sm_2000`。
教程分析器根据 LHE 头部的额外权重声明分配直方图；某些 SM 文件有声明，却没有完整的逐事件额外权重。
因此在**只分析 SM**时，另存一份删除声明和额外权重块的副本：

```bash
sed -e '/<initrwgt>/,/<\/initrwgt>/d' -e '/<rwgt>/,/<\/rwgt>/d' outputs/sm/events_full.lhe > outputs/sm/events_sm.lhe
ls -lh outputs/sm/events_sm.lhe
head -n 1 outputs/sm/events_sm.lhe
```

两条 `sed` 规则分别删除 `<initrwgt>...</initrwgt>`、`<rwgt>...</rwgt>` 块；不会重算权重，也不会用零补齐缺失的 EFT 贡献。
粒子动量、原始 SM 权重和事件数保留。原始 `.lhe.gz` 留给重加权；第 9 节不用这份删减副本。
应看到非空文件，开头为 `<LesHouchesEvents ...>`，然后运行与第 6 节相同的分析器：

```bash
python work/Material/pyroot_python3/lhe_analyzer.py outputs/sm/events_sm.lhe outputs/sm/Hvlvl_SM.root
```

**第一个参数**是输入，**第二个参数**是输出。等待 `processed 2000 events` 和 `file ... produced`；请求其他事件数时按实际数量检查。
SM 分析副本出现 `no new weights found` 属于预期情况。ROOT 中应有四个直方图：`mll_direct_sim`、`mmv_direct_sim`、`pTl1_direct_sim`、`pTmu_direct_sim`。
分析器已按事件数归一化。下一条命令直接画已有的 bin，不再读取 LHE。

### 8.6 调用 ROOT，画出自己的 SM 分布

使用参考图同一份**现有 `plot_histos.py`**，不需要在 Python 交互窗口手打循环。
在 Linux Bash 中完整输入一行，回车一次：

```bash
cd ~/smeftsim/outputs/sm
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
```

输入是第 8.5 节的四个 SM 直方图，输出是 `outputs/sm` 中的四张 PDF。
纯 SM 文件生成单面板图；第 9 节加入 EFT 修正后才出现比值面板。WSL 用户可在 Bash 执行 `explorer.exe .` 打开当前目录。

纵轴表示以 **GeV** 为单位的每 bin 部分衰变宽度贡献，详见第 6.2 节和[图的说明](docs/figures/README.zh-CN.md)。下面的示例也由同一绘图命令生成：

![SM 的电子与 muon 不变质量分布](docs/figures/sm_mll.png)

检查点：积分宽度量级约为 `1e-5 GeV`。指出哪一面板画出了你的 SM，以及为什么此时没有比值曲线。
你已沿着自己的事件走通**生成 → SM 分析副本 → ROOT → PDF**。
第 9 节继续使用原压缩事件。

## 9. 重加权与 ROOT 绘图

本章使用第 8 节生成的原始 SM LHE，在相同事件上计算作者卡定义的额外贡献。
第 8.5 节的 SM 分析副本只用于单独画 SM，不作为这里的重加权输入。
第 9.1–9.2 节解释原理与卡的含义；实际操作从第 9.3 节开始。
第 9.4 节将生成 `outputs/rw/Hvlvl_SM.root` 和四张对比图。

### 9.1 Reweighting 做了什么

对于同一个事件运动学点 $x$，常见的参数重加权概念是比较两个参数设定的矩阵元：

$$r(x)=\frac{|\mathcal M(x;\theta_{\rm target})|^2}{|\mathcal M(x;\theta_{\rm base})|^2}.$$

在满足相应采样和归一化约定的条件下，使用事件权重可估计目标分布，
避免对每个参数点都重新生成大量事件。
基础样本必须覆盖目标关心的运动学区域；权重极端集中时，统计效率会变差。

本教程还利用 `change process`，专门计算**线性、平方或传播子贡献**。
因此名为 `cHl3` 的权重是选出的线性干涉贡献，不是完整目标 EFT 点的概率比。
必须连同 reweight 卡里的过程和阶数解释这些标签。

### 9.2 读懂一张 reweight 卡

作者 `reweight_card_int.dat` 中 `cHl3` 这一段的含义如下。
**这是卡文件内容，只用于阅读或在编辑器修改，不在 Bash 逐行执行。**
卡里的 `done` 会被 MadGraph 读取，不是此刻需要你输入的菜单答案：

```text
change process h > e- ve~ mu+ vm SMHLOOP=0 NPprop=0 NP=1 NP^2==1
launch --rwgt_name="cHl3"
set cHbox 0
set cHW 0
set cHl3 1
set cHq3 0
set cll1 0
done
```

第一行选择干涉过程；`launch` 给输出权重命名；随后指定这个点的系数。
这张卡由 `madevent reweight` 读取，不需要重新进入事件生成菜单。
`change process` 决定分子的矩阵元贡献，`--rwgt_name` 决定 LHE 权重标签，`set` 行决定参数点；卡文件名不是权重标签。
LHE 中的 `<rwgt>` 会保存各权重。原 SM 权重和新增权重的意义不同，分析时应分开。
这里的 `cHl3` 权重代表所选线性干涉贡献；其他卡选择平方或传播子修正。

#### 从“矩阵元比”到实际画图的权重

对同一个 SM 事件 $x_i$，生成器比较目标贡献与 SM 矩阵元，然后把结果乘回基础事件权重。
例如线性项的概念是

$$
w_{L,i}=w_{S,i}\,
\frac{2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)(x_i)}{|\mathcal M_0(x_i)|^2}.
$$

$w_{S,i}$ 是 SM 权重，$w_{L,i}$ 是这个事件代表的线性贡献，可以为负。
本例保存的 LHE 权重已带生成器归一化，不能读出后再乘一次 SM 权重。
平方与传播子贡献有各自的目标矩阵元表达式。
事件的四动量和总事件数保持不变，变化的是这些额外权重；不需要为每个贡献重新抽一套事件。

画线性组合时，每个事件先计算 $w_S+w_L+w_P$；若额外加平方，再加 $w_Q$。
然后按所在 bin 求和、除以 $N$ 与 bin 宽度。
同一事件上的权重有相关性，组合误差也应按逐事件相加后的权重计算。

### 9.3 亲自用作者的 reweight 卡操作 MadGraph

目标是用教程提供的三张卡计算线性、平方和传播子贡献，供 ROOT 绘图使用。
下面每次调用都读取所选 run 的**已有 LHE**与过程副本中**当前的 `Cards/reweight_card.dat`**。
需要时编译目标矩阵元，在每个已有事件上计算目标贡献，然后向该 run 的压缩 LHE 更新权重标签和数值。
这一步不生成 ROOT 或 PDF；三次完成后，第 9.4 节统一分析更新后的 LHE。
用三张作者卡即可：线性卡一次计算四个单系数线性贡献，
平方卡计算四个平方贡献，传播子卡计算三个宽度/传播子贡献。
**不需要为每个系数重新生成事件，也不需要混合项卡才能画这六条参考曲线。**

| 作者卡 | 主要权重标签 |
|---|---|
| `reweight_card_int.dat` | `cHbox`、`cHW`、`cHl3`、`cll1` |
| `reweight_card_squares.dat` | `cHbox_sq`、`cHW_sq`、`cHl3_sq`、`cll1_sq` |
| `reweight_card_propW.dat` | `cHl3_propW`、`cHq3_propW`、`cll1_propW` |

卡里其他标签同样会被计算，但可以暂时不画。
每个 `launch` 对应一个参数点；例如 `cHbox` 那次是 `cHbox=1`、其他系数零，
并不是四个 Wilson 系数一起取 1。`LambdaSMEFT` 沿用基础样本的 1,000 GeV。
重加权卡中的 `change process` 改的是目标贡献，基础事件仍来自 SM。

#### A. 进入 Linux 并创建自己的工作副本

已经在 Linux 中时直接继续；否则先按第 5.1 节进入。
在 Linux Bash 中激活 `.venv`，已激活时可以直接使用。

**Linux Bash** 后，激活统一 `.venv`；已激活则继续使用：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cd ~/smeftsim
source .venv/bin/activate
which python
cd work/Material
ls Hvlvl_SM/Events/training_sm_2000
```

`which python` 应指向本项目 `.venv/bin/python`。
卡和编译器依赖必须使用这个环境，不要调用 Windows 的 Python。

这里使用另一个过程副本 `Hvlvl_SM_manual`，方便你亲自操作并保留原 SM。
**第一次执行时该目录应不存在**；若已经做过本节，复用它，跳过复制和旧缓存改名步骤。
先查看，再决定：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
ls -d Hvlvl_SM_manual
```

若提示目录不存在，执行：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cp -a Hvlvl_SM Hvlvl_SM_manual
```

如果原 SM 过程已做过重加权，目录中可能已有编译缓存 `rw_me`、`rw_me_2`。
在**刚复制的副本中**把它们改名保存，让这次练习重新建立自己的缓存：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
mv Hvlvl_SM_manual/rw_me Hvlvl_SM_manual/cache_before_manual_rw_me
mv Hvlvl_SM_manual/rw_me_2 Hvlvl_SM_manual/cache_before_manual_rw_me_2
```

仅对操作副本中实际存在的缓存执行重命名；若原 SM 过程从未做过重加权，
对应缓存不存在，则跳过不存在的那项。不要反复执行改名，也不要改原 `Hvlvl_SM`。
如果原样本已经有 `cHl3` 标签，作者卡会在这个副本中替换同名标签；
MadGraph 的 `tag ... already defines, will replace it` 提示应结合这一点理解。

#### B. 线性卡：先读，再复制，再运行

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cat reweight_card_int.dat
cp reweight_card_int.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

`cat` 打印卡内容，回车后读完再继续；`cp` 把这张卡放到生成器要求的位置。
第三条 `madevent reweight ...` 回车后会进入 MadGraph，先等它显示问题。
这里 **没有 `-f`**，保留 MadGraph 的交互步骤：
如果询问是否编辑 `reweight_card.dat`，先核对显示的文件，再输入 `0` 或菜单提示的 `done`，
按一次回车，接受当前卡。每个菜单答案都要单独输入并回车。
出现编译/事件处理日志后等待，不再输入 `done`，直到回到 Bash。
不同版本的提示文本可能略有差别，以当前菜单为准。
编译与处理事件需要等待；应看到四个参数点的结果，返回 Bash 后再做下一步。

检查 LHE 头部的新标签：

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
zcat Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz | sed -n '/<initrwgt>/,/<\/initrwgt>/p'
```

检查点：出现 `cHbox`、`cHW`、`cHl3`、`cll1`。
这些标签标记单独干涉贡献，可以为负，不是已经加了 SM 的完整速率。

#### C. 平方卡：只更换目标过程和参数点

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cat reweight_card_squares.dat
cp reweight_card_squares.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

同样接受当前卡。完成后再次执行 B 的 `zcat ... | sed ...` 检查，
应该新增 `cHbox_sq`、`cHW_sq`、`cHl3_sq`、`cll1_sq`。
作者卡在某些点显式写了 `set cHWB 0`；本 restriction 已把它固定为零，
若版本提示这个参数不作为自由输入，需检查其值与后续结果，不把它改为非零。
原先的线性标签应仍在文件中。

#### D. 传播子卡：用独立的阶数标签计算修正

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cat reweight_card_propW.dat
cp reweight_card_propW.dat Hvlvl_SM_manual/Cards/reweight_card.dat
./Hvlvl_SM_manual/bin/madevent reweight training_sm_2000
```

接受当前卡。完成后同样查看权重头部，
应该新增 `cHl3_propW`、`cHq3_propW`、`cll1_propW`，并保留前两次的标签。
这次 `NP=0 NPprop=2 NPprop^2==2` 选取传播子干涉；
它不是重复计算普通 `cHl3` 干涉，具体计数见第 7.3 节。

如果命令返回终端但没有对应标签，先查看屏幕中的错误和过程目录的 `ME5_debug`；
不要在失败后直接继续绘图。首次计算是否成功还要在下一节核对每个事件的权重，
不能只凭头部标签或进程退出码判断。

#### E. 先沿着一个系数核对流程

对 `cHl3`，找到三个独立标签：`cHl3`（普通线性）、`cHl3_sq`（维六平方）、`cHl3_propW`（传播子修正）。
输入的相空间点相同，目标阶数与权重不同。
绘图时每个选定标签**分别**加到 SM 上；选中三个标签不代表绘图器会把三项合成一条完整预测。
以后要研究其他参数点，先说明目标贡献和系数值，再编辑**独立的卡并使用新的权重标签**，重新执行重加权。
只改 `weights_to_plot` 是选择已有直方图，不会计算新物理。

三次重加权完成后，文件仍在 Linux 过程目录中。
按第 9.4 节继续在同一个 `.venv` 调用作者分析器和绘图脚本。
不必先把 LHE 复制到 Windows。

### 9.4 用自己的重加权 SM 样本调用作者 ROOT 绘图脚本

完成第 9.3 节后，文件应该包含作者卡产生的线性、平方、传播子标签。
**Linux Bash，继续使用已激活的统一 `.venv`：**

**Linux Bash｜逐条回车：** 每一行是一条完整命令；输完一行按一次 Enter，结束后再输入下一行。

```bash
cd ~/smeftsim
mkdir -p outputs/rw
gzip -dc work/Material/Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz > outputs/rw/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/rw/events.lhe outputs/rw/Hvlvl_SM.root
```

**先检查分析成功，再画图：** 应看到 `processed ... events`、各权重积分值和 `file ... produced`，
然后返回 Bash。当前 `training_sm_2000` 有 2,000 个事件，应显示 `processed 2000 events`；
将来换 run 时以实际事件数为准。出现错误时，先核对第 9.3 节的输入与权重。

**Linux Bash｜逐条回车：** 完整输入一行，回车一次，等待结果。

```bash
ls -lh outputs/rw/Hvlvl_SM.root
```

应看到非空的 ROOT 文件。这里的 `rw` 是目录，`Hvlvl_SM.root` 是文件。
它来自重加权后的 SM 副本，包含 SM 基线和额外贡献；第 8.5 节的 ROOT 只包含 SM 基线。

**Linux Bash｜逐条回车：** 先切换目录，回车；再输入完整绘图命令，回车并等待结束。

```bash
cd outputs/rw
python ../../work/Material/pyroot_python3/plot_histos.py Hvlvl_SM.root
```

分析器读取更新后的 LHE，包括原始 SM 权重和全部额外标签，为每类权重保存四个分布。
绘图器再读取这些分 bin 结果画对比，不需要打开多份独立 SM/EFT 模拟目录，也不会重新计算 `cHl3=1` 参数点。
本练习用一份重加权事件样本就包含画参考贡献所需的信息。
应生成四张 `plot_*.pdf`。在 WSL 的 Linux Bash 中打开输出目录：

**Linux Bash / WSL｜每条命令完整输入后回车：**

```bash
cd ~/smeftsim/outputs/rw
explorer.exe .
```

与第 6.5 节参考 PDF 比较时，保持相同的 `weights_to_plot` 和显示范围。
曲线应有相同含义、数量级与主要形状，不要求随机事件逐 bin 一样。
需要选择第 6.6 节列出的六项修正时，按该节调整工作副本设置。

LHE 中保存的额外权重已经包含生成器归一化，作者分析器再按约定除以事件数；
不要重复乘 SM 权重或再除一次事件数。
本次绘图保留作者的中心值画法，没有完整统计误差带。

检查输入 LHE 的权重声明与每个事件的实际权重一致，分析日志应显示完整事件数与各贡献积分值。

下面是本项目 2,000 个基础 SM 事件的重加权示例，使用已修正显示标签的教程绘图副本；bin 约定见第 6.6 节。

![重加权的 muon 与中微子不变质量分布](docs/figures/rw_mmv.png)

其他示例：[mll](docs/figures/rw_mll.png)、[leading lepton 横动量](docs/figures/rw_pTl1.png)、
[muon 横动量](docs/figures/rw_pTmu.png)。

**本章完成：** 已得到作者卡对应的多线图。完成这一节即可结束主要教学流程。

## 10. 保存与复现结果

### 10.1 日常操作速查

安装与脚本输入输出见 [安装指南](docs/setup/README.zh-CN.md)。
进入环境见第 5 节，生成见第 8 节，重加权见第 9 节。
重新分析和绘图已有示例见 [examples/reweighted](examples/reweighted/README.zh-CN.md)。

### 10.2 保存一次练习

保存原始压缩 LHE、卡、banner、版本、参数、种子、实际事件数和重要图。
本次已整理示例见 [examples/reweighted/metadata.json](examples/reweighted/metadata.json)。

### 10.3 分享可复现的结果

分享一张图时，应同时提供输入数据或获取方式、卡片和参数设置、软件版本、事件数、随机种子与分析命令，并说明图的单位和归一化方式。
[示例元数据](examples/reweighted/metadata.json) 展示这些记录；[示例说明](examples/reweighted/README.zh-CN.md) 给出了重新分析和绘图的步骤。

### 10.4 整理本地输出

自己的运行输出放在 `outputs`，仓库示例放在 `examples`。`outputs` 由命令创建，不作为空目录上传。
可清理能由原始压缩文件重新得到的解压副本；保留 `.venv`、原始 run、卡、banner 和虚拟磁盘。

## 11. 学习节奏与掌握标准

可分成四次主要练习，计算等待另算：

| 次数 | 主动学习时间 | 任务 | 自己应该能解释什么 |
|---|---:|---|---|
| 1 | 30–40 分钟 | 第 2–3 节，认识物理与软件链 | SMEFTsim 如何描述新相互作用 |
| 2 | 20–30 分钟 | 第 6 节，跟踪两次分析调用、读参考图 | 哪个文件保存粒子、权重或分 bin 汇总 |
| 3 | 30–45 分钟 | 第 7–8 节，生成并画自己的 SM | 模型、两张卡、LHE 与 ROOT 各自做什么 |
| 4 | 30–45 分钟 | 第 9 节，重加权并画对比图 | 不同贡献怎样来自同一组基础事件 |

做完后，再尝试用自己的话解释：

1. 为什么选择 U35 和 MwScheme，restriction 与参数卡有何不同。
2. SM、干涉、维六平方和传播子修正分别是什么。
3. 卡里的系数和能标怎样对应拉格朗日量。
4. 为什么同一个事件能有多个权重，为什么干涉权重可能为负。
5. 哪些算子主要改变整体速率，哪些还改变分布形状。

完成第 9 节即可结束这一轮教学练习。
研究应用还需进一步检查采样覆盖、统计误差以及重加权与直接生成的一致性。
同时应核对并记录所用模型版本、EFT 截断和宽度处理约定。

## 12. 版本与参考资料

本教程固定 Python 3.10、MadGraph 2.9.27、SMEFTsim v3.0.2 和 ROOT 6.40.00。
精确 Python 依赖见 [docs/setup/requirements.txt](docs/setup/requirements.txt)；
本次示例实际版本见 [metadata.json](examples/reweighted/metadata.json)。

完整教程、作者和论文集中列在 [根 README](README.zh-CN.md#来源与致谢)。
第三方许可与发布范围见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.zh-CN.md)。
