# 安装 Linux 环境

[English](README.md) | [简体中文](README.zh-CN.md)

开始阅读 [handbook](../handbook.zh-CN.md) 前，安装只需看这一份指南。
本仓库提供教学文档和本地生成的示例，不提供预装好的模拟器。
下面会从上游直接获取软件，并在 **一个项目目录 `~/smeftsim` 中配置一个 Python 环境 `.venv`**。

已验证的平台是 x86-64 Ubuntu 22.04、Python 3.10、MadGraph 2.9.27、教程提供的 SMEFTsim v3.0.2 模型和 ROOT 6.40.00。
固定版本是为了复现这次练习，不代表各软件的最新版本。
已有环境如果通过第 6 节检查，跳过安装，直接继续 handbook。

**输入规则：** PowerShell 或 Bash 代码块中每一行都是完整命令。输完一行，按一次 Enter，等提示符回来再输入下一行。不要输入终端显示的提示符。如果命令失败，先处理当前错误再继续。

## 1. 选择 Linux 环境

按自己的现有环境选择入口。后续命令面向 **x86-64 Ubuntu 22.04 和 Python 3.10**；其他发行版、版本或架构需要另行检查兼容性。

| 当前环境 | 从哪里继续 |
|---|---|
| 原生 Ubuntu 22.04 或已有 Ubuntu 22.04 虚拟机 | 第 1.1 节，再进入第 2 节 |
| 已有 WSL2 Ubuntu 22.04 | 第 1.2 节，再进入第 2 节 |
| Windows 尚无合适的 Linux，或希望单独隔离一个 Linux 环境 | 第 1.3 节 |

### 1.1 原生 Linux 或已有虚拟机

使用自己的普通 Linux 用户打开 Bash，从第 2 节继续。无需安装 WSL，也不要求用户名为 `smeft`。
后续项目目录 `~/smeftsim` 位于你自己的 Linux 主目录中，项目 Python 包统一安装到 `.venv`。

### 1.2 已有 WSL2 Ubuntu

在 **Windows PowerShell** 中查看已安装的发行版：

```powershell
wsl --list --verbose
```

选择已有的 Ubuntu 22.04，确认 VERSION 列为 `2`。
例如，它的名称为 `Ubuntu-22.04` 时，输入：

```powershell
wsl -d Ubuntu-22.04 --cd ~
```

把 `Ubuntu-22.04` 替换为列表中自己的发行版名称。该命令使用这个发行版的默认 Linux 用户。
请使用有 `sudo` 权限的普通用户，再到第 2 节核对系统版本和架构。
以后继续练习也使用自己的这条进入命令。已有环境不符合要求时，可按第 1.3 节另建兼容环境。

### 1.3 新建专用 WSL2 环境

这条可选路线创建独立的 Ubuntu 22.04，发行版命名为 `SMEFTsim`，普通用户命名为 `smeft`。
这些名称只用于本小节；第 2–7 节都使用自己的主目录，同样适用于第 1.1–1.2 节。
WSL2 在轻量虚拟机中运行 Linux；虚拟磁盘文件留在 Windows 上，计算和项目文件放在 Linux 内。

**以管理员身份打开 Windows PowerShell：**

```powershell
wsl --install --no-distribution
```

如果提示重启，重启 Windows 后再继续。已安装 WSL 时跳过这条命令。
然后在普通 **Windows PowerShell** 中逐条执行：

```powershell
wsl --list --verbose
```

如果已经存在 `SMEFTsim`，进入后检查原有环境，不要再次导入。
首次安装时，下载 Canonical 提供的 Ubuntu 22.04 x86-64 根文件系统及校验清单：

```powershell
$smeftDiskDir = "$env:USERPROFILE\SMEFTsim-WSL"
$smeftImage = "$env:TEMP\ubuntu-jammy-smeftsim.rootfs.tar.gz"
$smeftChecksums = "$env:TEMP\ubuntu-jammy-smeftsim-SHA256SUMS"
curl.exe --fail --location --output "$smeftImage" https://cloud-images.ubuntu.com/wsl/jammy/current/ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz
curl.exe --fail --location --output "$smeftChecksums" https://cloud-images.ubuntu.com/wsl/jammy/current/SHA256SUMS
(Get-FileHash -Algorithm SHA256 -LiteralPath "$smeftImage").Hash
Select-String -LiteralPath "$smeftChecksums" -Pattern 'ubuntu-jammy-wsl-amd64-ubuntu22.04lts.rootfs.tar.gz'
```

两处 SHA256 必须一致，大小写不影响比较。请在同一个 PowerShell 会话中继续，保留前面定义的变量。
然后导入并进入新发行版：

```powershell
wsl --import SMEFTsim "$smeftDiskDir" "$smeftImage" --version 2
wsl -d SMEFTsim -u root
```

现在处于 **Linux Bash，身份是 root**。创建本指南使用的普通用户：

```bash
adduser smeft
usermod -aG sudo smeft
exit
```

`adduser` 会要求输入两次新 Linux 密码，屏幕不显示密码字符。后续可选姓名、联系方式等问题直接回车留空，最后确认信息。每条命令结束后再执行下一条。
`exit` 返回 PowerShell。以普通用户进入 Linux：

```powershell
wsl -d SMEFTsim -u smeft --cd ~
```

以后每次继续练习都用这条命令。命令已明确指定用户，无需修改默认用户配置。
`$smeftDiskDir` 保存虚拟磁盘，必须保留；下载的压缩镜像是安装文件，不是已安装的磁盘。
来源：[Microsoft WSL 安装说明](https://learn.microsoft.com/en-us/windows/wsl/install)、[WSL 导入与用户命令](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)、[Canonical 的 Ubuntu 镜像](https://cloud-images.ubuntu.com/wsl/jammy/current/)。

## 2. 在这个 Linux 环境中安装基础依赖

**Linux Bash，普通用户：**

```bash
uname -m
cat /etc/os-release
whoami
```

应看到 `x86_64`、Ubuntu `22.04` 和你自己的普通 Linux 用户名；不应为 `root`。
以下系统软件包安装到你选定的 Linux 环境中。Python 包随后安装到项目 `.venv`，不使用 Windows Python 或 Anaconda。

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends python3 python3-venv python3-dev build-essential gfortran git perl ca-certificates coreutils sed gzip unzip nano ghostscript libsm6 libice6 libx11-6 libxext6 libxrender1 libxft2 libglu1-mesa
python3 -c "import sys; print(sys.version); assert sys.version_info[:2] == (3, 10), 'Use Ubuntu 22.04 / Python 3.10 for this lesson'"
```

`sudo` 要求密码时输入 Linux 密码。Python 检查应结束且没有断言错误。
`build-essential` 提供 GCC 和 Make；`gfortran` 编译生成器的 Fortran 代码；`lib...` 软件包提供 ROOT 图形库；Ghostscript 用于嵌入 PDF 字体；`nano` 是终端文本编辑器。

## 3. 获取教学文档与固定版本的软件

项目放在 Linux 主目录，不放在 `/mnt/c`。
以下命令用于首次安装；目标目录已存在时，先检查，不要覆盖式重复克隆。

```bash
cd ~
git clone https://github.com/RuneTan/smeftsim-learning.git smeftsim
cd ~/smeftsim
mkdir -p tools work/Material reference outputs
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
git -C tutorial rev-parse HEAD
git -C tools/MG5_aMC_v2_9_27 rev-parse HEAD
test -L tools/MG5_aMC_v2_9_27/madgraph/VERSION
```

两个哈希值应分别与上面的固定版本一致。“Detached HEAD” 表示固定到记录的版本，是预期提示。
最后一条命令在 MadGraph 的 Linux 符号链接完整时安静结束。
教程已包含需要的 SMEFTsim UFO 和 restriction，本练习不需要再单独下载 SMEFTsim 模型。

准备可编辑的工作副本，并关闭这份固定版本 MadGraph 的更新检查：

```bash
cp -an tutorial/Material/. work/Material/
printf 'auto_update = 0\n' > tools/MG5_aMC_v2_9_27/input/mg5_configuration.txt
```

`cp -a` 保留文件属性，`-n` 保留目标已有文件。`tutorial` 保存下载的原文件，改卡时只改 `work/Material`。
配置写入命令用于新下载的版本，会替换该文件内容；已有自定义配置时应保留原配置。

## 4. 创建唯一的 Python 环境

在 `~/smeftsim` 中逐条执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --index-url https://pypi.org/simple -r docs/setup/requirements.txt
python -m pip check
```

简短的 [依赖文件](requirements.txt) 固定 NumPy、six、setuptools 和 Linux ROOT wheel 的版本。
ROOT 的 PyPI 打包方式标为 alpha；本教程使用本地已验证的 `0.1a12`，其中包含 ROOT `6.40.00`。
说明见 [ROOT Python 接口文档](https://root.cern.ch/doc/master/group__Python.html) 和 [ROOT 安装方式](https://root.cern/install/)。
不要使用 `sudo pip`，也不要向 Windows Python 安装这些包。

## 5. 准备两份 Python 3 分析脚本

脚本来自第 3 节下载的教程。本教学仓库提供转换步骤，不重新分发脚本文件。
只在两份 Python 3 工作副本不存在时执行下面命令，否则 `>` 会覆盖它们。
保持 `.venv` 激活，并停留在 `~/smeftsim`：

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
python scripts/fix_axes.py
python -m py_compile work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

兼容转换展开 tab、更新 Python 2 语法和解释器行，将 `file()` 换成 `open()`。`scripts/fix_axes.py` 修正本地标签与面板间距，让纯 SM 文件使用单面板，并通过 ROOT/Ghostscript 嵌入 PDF 字体；直方图计算和上游原文件保持不变。
Python 3.10 带有 `lib2to3`，Python 3.14 没有。最后一条命令检查语法，正常时安静结束。

| 脚本 | 从项目根目录调用的完整形式 | 功能 |
|---|---|---|
| 分析器 | `python work/Material/pyroot_python3/lhe_analyzer.py INPUT.lhe OUTPUT.root` | 读取四动量和权重，为每个权重填充四个分布，并按实际事件数归一化 |
| 绘图器 | `python work/Material/pyroot_python3/plot_histos.py INPUT.root` | 向当前目录写出四张 PDF，显示单项贡献加 SM，以及对应的比值 |

分析器需要 **两个脚本参数**，绘图器需要 **一个**。把所有参数输入完整后再按 Enter。

## 6. 检查安装并复现仓库示例

```bash
cd ~/smeftsim
source .venv/bin/activate
python --version
which python
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
python -m pip check
gfortran --version
```

应看到 Python 3.10、位于自己 `~/smeftsim/.venv` 下的 Python 路径、ROOT `6.40.00`、无依赖冲突和编译器版本。
然后使用仓库提供的 2,000 事件示例验证分析流程：

```bash
mkdir -p outputs/example_reweighted
gzip -dc examples/reweighted/events.lhe.gz > outputs/example_reweighted/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/example_reweighted/events.lhe outputs/example_reweighted/histograms.root
cd outputs/example_reweighted
python ../../work/Material/pyroot_python3/plot_histos.py histograms.root
ls -lh plot_mll.pdf plot_mmv.pdf plot_pTl1.pdf plot_pTmu.pdf
cd ../..
```

应看到 `processed 2000 events`、48 个 ROOT 直方图和四个非空 PDF。
命令只写入本地输出，不改仓库提供的示例。在 WSL 的输出目录中执行 `explorer.exe .` 可以打开文件夹；Linux 桌面用户用自己的文件管理器查看。
这一步检查安装和分析；事件生成与重加权另见 handbook 第 8–9 节。

## 7. 解压参考结果并继续学习

固定版本教程内已有结果压缩包，解压后供 handbook 第 6 节使用：

```bash
cd ~/smeftsim
unzip -n tutorial/SMEFTsim_tutorial_results.zip -d reference
ls -lh reference/Results/Root_files/Hvlvl_SM_run_01.root
ls -lh reference/Results/Hvlvl_SM/Events/run_01/unweighted_events.lhe.gz
```

应看到两个非空文件。压缩包有顶层 `Results` 目录，`-n` 保留已有解压文件。
handbook 的参考数据路径现在都指向这个 Linux 目录。

| 本地创建的目录 | 存放内容 |
|---|---|
| `.venv` | 共用 Python、生成器依赖和 ROOT |
| `tutorial` | 固定版本的原教程，包括 UFO、输入卡、脚本和参考结果压缩包 |
| `tools` | 固定版本 MadGraph 源码与程序入口 |
| `work/Material` | 可编辑卡、Python 3 分析副本、生成的过程与 run |
| `reference` | 解压后的上游参考结果 |
| `outputs` | 自己的分析输出、解压副本、ROOT 文件和图 |

这些目录在安装或操作时创建，由 Git 忽略，教学仓库不再附带空目录占位说明。
仓库保留 handbook、知识附录、示例结果及来源和许可证记录。
不需要 Windows 源码副本或第二份 Python 环境。

从 [handbook 第 5 节](../handbook.zh-CN.md#5-启动环境与核对依赖) 继续，再依次完成第 6、8、9 节。
仓库示例的含义和来源见 [示例说明](../../examples/reweighted/README.zh-CN.md)。
