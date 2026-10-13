# 项目专用 WSL 与虚拟磁盘

[English](README.md) | [简体中文](README.zh-CN.md)

准备好专用 Ubuntu 后，按 [首次克隆配置说明](../docs/setup/README.zh-CN.md) 完成项目配置。

本目录是当前电脑的环境资产，不是要上传的教学内容。
只发布此说明；安装包、镜像和磁盘由 Git 忽略规则排除。

| 本地内容 | 作用 |
|---|---|
| `downloads` | Windows WSL 安装包、Ubuntu rootfs 和校验材料 |
| `SMEFTsim/ext4.vhdx` | 整个专用 Linux 的磁盘，包括 `.venv`、生成器、过程和事件 |

`ext4.vhdx` 不能作为普通缓存删除，也不需要上传 GitHub。
要分享 Linux 中某个结果，复制该文件到 `examples` 或直接提交文件，
见 [发布步骤](../docs/publishing/README.zh-CN.md)。

当前采用 WSL2 Ubuntu 22.04，发行版名 `SMEFTsim`，Linux 用户 `smeft`。
新电脑可先参考
[Microsoft WSL 安装说明](https://learn.microsoft.com/en-us/windows/wsl/install)、
[导入自定义发行版](https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro)，
再准备 Python 3.10、`python3-venv`、`python3-dev`、`gcc`、`gfortran`、`make`、`git`、`perl`。
当前脚本要求这些前提，不是从空机器自动安装所有资源的发布包。

当前隔离方式与目录说明如下。

## 4. 环境隔离与文件位置

### 4.1 隔离到什么程度

采用项目专用 WSL2 Ubuntu 环境。WSL2 使用 Linux 内核和虚拟化机制，
日常通过终端操作；它没有在本任务中安装一个 Ubuntu 图形桌面。

| 层级 | 位置与用途 | 对宿主环境的影响 |
|---|---|---|
| Windows 共享运行支持 | Microsoft WSL 与虚拟机平台 | 已安装/启用，并已实际运行 |
| 项目 Ubuntu | WSL 名称 `SMEFTsim`；磁盘位于 `vm/SMEFTsim/ext4.vhdx` | 包、编译器和 Linux 文件保存在这块专用磁盘内 |
| Linux 统一项目环境 | `/home/smeft/smeftsim/.venv` | MadGraph、重加权和 PyROOT 共用；所有依赖与 ROOT 图形库保存在项目内 |

没有执行向现有 Windows Anaconda 安装物理依赖的操作，没有手动修改 Windows 全局 PATH、
其他项目环境或用户级 `.wslconfig`。
已关闭本发行版的 Windows PATH 自动追加；实际检查的 Linux PATH 未包含 Windows Anaconda。
Linux 的系统包会安装在这个专用 Ubuntu 内，不是 Windows 的全局 Python 环境。

### 4.2 文件地图

```text
smeftsim/
├── handbook.md                  本手册
├── tutorial/                    下载的 2023 年教程材料
├── tools/MG5_aMC_v2_9_27/        已下载的生成器源码
├── cards/                       可复用的过程定义
├── scripts/                     安装、启动、分析和校验入口
├── reference/Results/           2023 年教程参考结果
├── docs/figures/                可随教学文档分享的示例 PNG
├── outputs/                     本地运行数据、ROOT 与图
└── vm/                          安装包、镜像与项目虚拟磁盘
```

Ubuntu 中已有 `/home/smeft/smeftsim`，其中 `work/Material` 是实际生成工作的目录。
后续编辑和运行卡使用该工作目录。`tutorial/Material` 保留作为原始资料。
日常只需激活 Linux 的 `/home/smeft/smeftsim/.venv`，同一终端完成生成、重加权和 ROOT 绘图。
SMEFTsim 的 UFO 描述相互作用；MadGraph 将过程写成数值代码，编译器再把它构建成可运行程序。
因此依赖除了 Python 包，还有已安装在专用 Ubuntu 内的 `gcc`、`gfortran`、`make`、`git` 和 `perl`。
Python 3.10、NumPy 1.26.4 与固定的 setuptools 保留本教程重加权所需的旧 f2py 构建接口；
不用 Windows Python 3.14 来运行这一套 Linux 生成器。
Windows 主目录中的同名 `.venv` 是之前的 Windows 环境，路径不同；本手册的 `source .venv/bin/activate`
始终在 Linux 的 `/home/smeft/smeftsim` 执行。Windows 与 Linux 的环境不能混用。
