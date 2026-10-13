# 辅助脚本

[English](README.md) | [简体中文](README.zh-CN.md)

新电脑请从 [首次克隆配置说明](../docs/setup/README.zh-CN.md) 开始。

这里存放本项目编写的环境、启动和检查入口，不是 SMEFTsim 模型本身。
主学习路线仍是手动设置卡、回答 MadGraph 菜单、调用作者分析器与 ROOT。

## 当前主线

| 脚本 | 执行环境 | 功能 | 何时使用 |
|---|---|---|---|
| `enter-linux.ps1` | Windows PowerShell | 进入名称为 `SMEFTsim` 的 WSL，用户 `smeft` | 日常进入环境 |
| `setup_linux.sh` | Linux Bash | 检查系统工具，在单独 Linux 目标目录准备源码与统一 `.venv` | 初始环境准备 |
| `prepare_work.py` | 项目 Python | 将作者材料复制到 `work/Material`；已有文件保留，整理 shell 换行 | 生成器入口自动调用 |
| `run_generator.sh` | Linux Bash | 激活项目环境；按阶段调用 MadGraph；拒绝覆盖已有过程并检查日志 | `check_model`、`generate_sm`、`generate_eft` |
| `validate_generated.py` | 项目 Python | 检查事件、末态、有限权重、四动量与归一化，写出 JSON | 专用 2,000 事件教程 smoke 样本检查 |
| `validate_smoke.sh` | Linux Bash | 小样本生成与单项重加权检查；已有 smoke run 时复用 | 环境检查，不是课程主线 |
| `inspect_parameters.py` | Python | 静态读取 UFO 参数与作者卡，生成索引 | 需要刷新参数资料时 |

## Windows 安装入口

| 脚本 | 功能 | 前提 |
|---|---|---|
| `install-wsl-runtime.ps1` | 检验本地 Microsoft 安装包并安装 WSL/启用虚拟机平台 | 需要本地安装包和管理员环境 |
| `bootstrap_guest.sh` | 在专用 Ubuntu 内安装系统依赖并创建 `smeft` 用户 | 由接续安装入口调用 |
| `resume-install.ps1` | 校验本地 Ubuntu 镜像、导入专用发行版、配置环境并运行初始检查 | 依赖 `vm/downloads` 中已准备的安装材料 |

这些脚本保留当前机器的专用发行版约定，不是任意电脑的无参数安装器。
新电脑应先按 [环境说明](../vm/README.zh-CN.md) 准备所需工具与材料。

## 历史辅助工具

| 文件 | 原功能 | 当前课程 |
|---|---|---|
| `analyze.ps1`、`analyze_tutorial.py` | Windows NumPy/Matplotlib 分析 | 不在 ROOT 主线使用 |
| `lesson.ps1`、`lesson_guest.py` | 自动组织直接生成、重加权阶段 | 不在手动主线使用 |
| `compare_lesson.py` | 自动比较四组直接样本与重加权 | 当前课程不要求 |

保留这些文件避免破坏原入口和导入关系；新的学习者从当前主线开始即可。

## 使用例子

**Linux Bash，项目根目录；每行回车一次：**

```bash
source .venv/bin/activate
bash scripts/run_generator.sh check_model
```

该检查只构造模型与过程，不生成事件。卡的物理含义见 [cards/README.md](../cards/README.zh-CN.md)。
输出写入 `outputs`；目录说明见 [outputs/README.md](../outputs/README.zh-CN.md)。

`validate_generated.py` 针对固定的 2,000 事件 smoke 样本、`IDWTUP=-4` 和教程 SM/cHl3 线性权重符号，不是任意过程的通用校验器。`inspect_parameters.py` 把临时索引与 JSON 写入 `outputs`，不会覆盖 `docs/parameters` 中维护的双语资料。
