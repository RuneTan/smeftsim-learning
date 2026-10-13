# 从新克隆的仓库配置环境

[English](README.md) | [简体中文](README.zh-CN.md)

在**新电脑**开始阅读[主手册](../../handbook.zh-CN.md)前，先按本说明准备环境。已有环境已经能够生成事件并导入 ROOT 时，继续使用它，跳过这里的安装步骤。

公开仓库包含教材、辅助脚本和选定的示例，不包含虚拟磁盘、虚拟环境、MadGraph、上游教程下载材料或作者分析脚本。以下步骤从上游取得本地依赖，并自行准备分析脚本，不把作者代码副本再次发布。

## 1. 起点与两个目录

本说明从一个**项目专用的 x86-64 Ubuntu 22.04 环境**开始，使用可以通过 `sudo` 安装发行版软件包的普通 Linux 用户。教材使用 Python 3.10。

Windows 读者应先按 Microsoft 的 [WSL 安装指南](https://learn.microsoft.com/en-us/windows/wsl/install)准备专用 WSL2 环境；若需单独命名的发行版，参考[导入发行版指南](https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro)。先完成 Linux 用户配置，再继续以下步骤。操作系统的创建过程不包含在下面的命令中。

| 目录 | 用途 |
|---|---|
| `~/smeftsim-source` | Git 工作区、教材、分享示例以及本地下载的上游源码 |
| `~/smeftsim` | 单独的运行目录：`.venv`、工作卡、生成的过程与输出 |

`~` 指当前 Linux 用户的主目录。安装辅助脚本要求源码目录与运行目录不同；运行目录必须位于 Linux 文件系统，且路径不能带空格。不要把仓库直接克隆到 `~/smeftsim`，然后又把同一个目录作为安装目标。

主手册原机器的 WSL 发行版名为 `SMEFTsim`，用户为 `smeft`，运行目录为 `/home/smeft/smeftsim`。你的名字不同时，应在进入环境和打开文件资源管理器的命令中替换发行版名、用户名和主目录路径；物理与分析操作不变。

**回车规则：** 下面每个 Bash 代码块中，每一行都是一条完整命令。输入完整一行，按一次回车，等待 Bash 提示符重新出现，再输入下一行。提示符本身不要输入。

先检查 Linux 环境：

```bash
uname -m
cat /etc/os-release
whoami
```

应看到 `x86_64`、Ubuntu 版本 `22.04` 和你的普通 Linux 用户名。继续在这个专用环境里操作，不要在 Windows PowerShell 或 Git Bash 中输入后续命令。

## 2. 安装 Linux 前置工具

这些软件包安装在**这个专用 Ubuntu 发行版内**。Python 物理依赖稍后放入项目 `.venv`，不会安装到 Windows Anaconda。

**Linux Bash：完整一行，按一次回车，再等待。**

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3 python3-venv python3-dev build-essential gfortran git perl ca-certificates coreutils sed gzip unzip
python3 -c "import sys; print(sys.version); assert sys.version_info[:2] == (3, 10), 'This lesson requires Python 3.10'"
```

如果 `sudo` 要求 Linux 密码，输入密码后回车；输入时不会显示字符。`build-essential` 提供 GCC 和 Make，`gfortran` 提供 Fortran 编译器。`coreutils`、`sed`、`gzip`、`unzip` 提供后续转换与解压工具。这个 Ubuntu 环境也包含安装辅助脚本使用的 APT 和 `dpkg-deb`。

Python 检查应正常结束，没有断言错误。若显示其他版本，先停下，准备 Ubuntu 22.04/Python 3.10 环境后再继续。APT 操作可查 [Ubuntu 软件包管理说明](https://ubuntu.com/server/docs/how-to/software/package-management/)。

## 3. 克隆教学仓库与固定版本的上游源码

新安装使用下面的目录名。目标已存在时，先检查，不要重复向它执行 `git clone`。公开仓库下载不需要在命令中写入 token。

**Linux Bash：每条命令单独输入、回车并等待完成。**

```bash
cd ~
git clone https://github.com/RuneTan/smeftsim-learning.git smeftsim-source
cd ~/smeftsim-source
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
git -C tutorial rev-parse HEAD
git -C tools/MG5_aMC_v2_9_27 rev-parse HEAD
```

最后两条命令应分别输出上面固定的提交哈希。`checkout` 后出现 “detached HEAD” 提示是正常的，表示源码固定在记录的版本。教程包含 SMEFTsim v3.0.2 UFO 和参考结果压缩包。

来源与许可记录见[根 README](../../README.zh-CN.md)和[第三方说明](../../THIRD_PARTY_NOTICES.zh-CN.md)。上游下载材料保留本地，由教学仓库的 Git 忽略规则排除。

## 4. 配置单独的 Linux 运行目录

仍在 `~/smeftsim-source`，执行：

```bash
bash scripts/setup_linux.sh ~/smeftsim
```

等待 `Environment prepared at ...` 和 Bash 提示符出现。辅助脚本复制教程与过程卡，建立保留正确符号链接的 Linux MadGraph 工作副本，将固定依赖安装到 `~/smeftsim/.venv`，并将两个 ROOT 图形库解压到该环境内，最后准备 `work/Material`。这一步尚未生成事件。

辅助脚本不调用 `sudo`，也不向全局 Python 安装依赖。本步骤面向新的运行目录；对已有安装，它会保留已有工作文件，不能把它当成自动升级程序。

随后进入运行目录并检查：

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
python -m pip check
gfortran --version
```

应得到 Python 3.10、位于 `~/smeftsim/.venv` 下的 Python 路径、ROOT `6.40.00`，且没有依赖冲突。以下步骤继续使用这个已激活的环境。

## 5. 生成本地 Python 3 分析副本

新克隆的公开仓库只提供分析目录的说明，**不提供其中的两个 `.py` 文件**。在调用分析器或绘图脚本前，先从刚下载的作者原文件生成工作副本。

**以下转换命令仅在两个工作脚本尚不存在时执行。** 从已激活环境的运行目录 `~/smeftsim` 逐条输入：

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
python -m py_compile work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

`>` 把内容写入新工作副本，是命令的一部分。`tutorial/Material` 的作者原文件不变。转换只处理 Python 3 兼容：展开缩进、转换旧语法、将 `file()` 替换为 `open()`、更新解释器行。Python 3.10 提供这里使用的 `lib2to3`，Python 3.14 已不提供。

最后一条命令检查语法，正常情况下没有输出。详细解释见[工作副本说明](../../work/Material/pyroot_python3/README.zh-CN.md)。

## 6. 将分享示例放入运行目录

安装辅助脚本不会把公开示例复制到运行目录。从 `~/smeftsim` 复制选定示例，保留已有目标文件：

```bash
mkdir -p examples/reweighted
cp -an "$HOME/smeftsim-source/examples/reweighted/." examples/reweighted/
ls -lh examples/reweighted/events.lhe.gz examples/reweighted/histograms.root
```

应看到两个非空文件。`cp -a` 保留复制文件的属性，`-n` 表示不覆盖已有文件。对于新安装，这就是仓库提供的示例；若目标原本有不同的示例，需另行核对，不能以为此命令已经替换它。

教材仍在 `~/smeftsim-source` 或 GitHub 上阅读，运行命令则在 `~/smeftsim` 执行。现在可以按[示例重新分析与绘图说明](../../examples/reweighted/README.zh-CN.md)操作。

## 7. 准备可选的作者参考结果

若要执行手册第 6 节，将本地下载的结果压缩包解压到**源码工作区**，保留已解压文件：

```bash
mkdir -p "$HOME/smeftsim-source/reference"
unzip -n "$HOME/smeftsim-source/tutorial/SMEFTsim_tutorial_results.zip" -d "$HOME/smeftsim-source/reference"
ls -lh "$HOME/smeftsim-source/reference/Results/Root_files/Hvlvl_SM_run_01.root"
```

压缩包内部已有顶层 `Results` 目录。`-n` 防止覆盖已解压文件。最后一条命令应列出非空 ROOT 文件。

原手册使用整理机器的 Windows 挂载路径。这里的新 Linux 配置应将 `/mnt/c/Users/符文/Desktop/NSBI/smeftsim/reference` 替换为 `$HOME/smeftsim-source/reference`。

在第 6.5 节 A3，从运行目录使用下面的完整命令：

```bash
cd ~/smeftsim
mkdir -p outputs/my_pyroot_reference
gzip -dc "$HOME/smeftsim-source/reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz" > outputs/my_pyroot_reference/events.lhe
```

等待 Bash 提示符返回，再接手册第 6.5 节 A4，先检查解压文件，再分析。输入时保留 `>` 和输出文件名，完整一行之后才回车。

若选择该节的“直接使用已有 ROOT”可选捷径，先进入 `outputs/my_pyroot_reference`，再执行：

```bash
cd ~/smeftsim/outputs/my_pyroot_reference
python ../../work/Material/pyroot_python3/plot_histos.py "$HOME/smeftsim-source/reference/Results/Root_files/Hvlvl_SM_run_01.root"
```

这一捷径替代 LHE 分析路线，不是另一个必需步骤。

## 8. 继续教材

回到已激活环境的运行目录，检查模型构造：

```bash
cd ~/smeftsim
bash scripts/run_generator.sh check_model
```

这里构造过程，不生成事件。然后按[主手册](../../handbook.zh-CN.md)继续：第 6 节复现参考图，或第 8–9 节自己生成 SM 并重加权。按本说明第 1 节替换你的主目录路径和 WSL 名称。

早期 Windows 辅助脚本 `install-wsl-runtime.ps1`、`resume-install.ps1` 需要 `vm/downloads` 内事先准备的安装包和特定 Ubuntu 镜像；这些下载文件没有发布。`resume-install.ps1` 的 ROOT 检查还假定本地分析脚本已经存在。它们不是这条新克隆配置路线的入口。本说明使用已有安装辅助脚本和明确的手动转换步骤，没有新增一键运行程序。
