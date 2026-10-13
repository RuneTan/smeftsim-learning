# 发布到 GitHub：来源、许可与 WSL 文件

[English](README.md) | [简体中文](README.zh-CN.md)

## 1. 署名和许可是两件事

在根 [README](../../README.zh-CN.md) 列出原教程、作者、版本、论文与改动范围，
有助于读者分清原工具和自己的教学整理；但它不能代替再分发许可。
公开可读的仓库也不自动等于允许把全部代码移入另一个仓库。
[GitHub 的许可说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
解释了没有许可证时的默认版权规则。

2026-10-13 核对：

| 来源 | 核对结果 | 当前发布方式 |
|---|---|---|
| [SMEFTsim v3.0.2](https://github.com/SMEFTsim/SMEFTsim/blob/v3.0.2/LICENSE) | MIT | 参数资料注明来源并附原许可；模型源码本地下载 |
| MadGraph 2.9.27 的 `madgraph/LICENSE` | 改写自 Illinois/NCSA；需保留通知，禁止借作者名义背书 | 程序本地下载，附原许可作为示例来源记录 |
| [ROOT](https://root.cern/about/license/) | LGPL 2.1 或更新版本；部分组件另有许可 | 仅作为本地依赖，不上传环境和二进制 |
| [2023 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) | 固定副本未找到 LICENSE，GitHub API 许可字段为 null | 教程源码、卡副本和 Python 3 副本不发布；从上游下载 |

“未找到许可”是当前核对结果，不是断言作者永远不允许分享。
不要把模型主项目的 MIT 自动套用到教程的独立分析与绘图脚本。

**什么时候询问作者？** 如果希望把教程脚本、修改后的 Python 3 副本、
教程卡或文字材料直接放进自己的公开仓库，建议先确认授权范围及采用的许可。
可说明这是教学复现、保留署名、只做 Python 3 必需转换，并列出希望再分发的文件。
当前整理后的发布范围不包含这些副本，因此没有把邮件回复当作完成本地整理的前提。
没有替你给作者发送邮件。

自己的数值结果不因使用一个程序就自动继承该程序的代码许可。
输出中若复制了程序文本或上游素材，则仍应分别核对；
[GNU 关于程序输出的解释](https://www.gnu.org/licenses/gpl-faq.en.html#WhatCaseIsOutputGPL)
说明了这个区别。公开 LHE 省略完整生成器 banner 与卡片模板，保留数值初始化、事件和权重；输入设置、出处和许可记录另行保留。

本项目自有教材和辅助脚本尚未选择统一许可证。
公开上传与真正给予他人开源复用许可也不同；选择自己的许可时，
不要覆盖上游或声称所有内容均为自己的版权。

## 2. Linux 中的文件怎么带到仓库

**文件就存放在 Linux 文件系统里，并不需要上传虚拟磁盘。**
GitHub 接收 Git 提交中的普通文件，不关心它原来在 Windows 还是 WSL。

本项目以 Windows 的 `smeftsim` 目录作为整理与发布目录，
Linux 的 `/home/smeft/smeftsim` 继续负责运行。
你完成的重加权示例已经复制到仓库的 [examples/reweighted](../../examples/reweighted/README.zh-CN.md)，
公开 LHE 是分析用导出；ROOT 与 PDF 保留原始 SHA256。完整原始 run 仍在本地，无需上传 `ext4.vhdx`。

将来要复制另一个结果，可以从 Windows 打开 WSL 目录：

**Windows PowerShell，完整一行输入并回车：**

```powershell
explorer.exe '\\wsl.localhost\SMEFTsim\home\smeft\smeftsim\outputs'
```

选取需要的结果，复制到 Windows 项目的 `examples/你的示例名`，
并记录版本、参数、种子、事件数和来源。发布前检查生成文件 header 中是否包含上游文本，不要把整个环境当作示例。

也可以在 WSL 直接复制。下面是**将来的操作示意**，要替换目标路径；
当前示例已存在，不重复执行覆盖：

```bash
cp /home/smeft/smeftsim/work/Material/Hvlvl_SM_manual/Events/training_sm_2000/unweighted_events.lhe.gz '/mnt/c/Users/你的用户名/项目路径/smeftsim/examples/你的示例名/events.lhe.gz'
```

## 3. 通过 WSL 提交 Windows 整理目录

这一方案在 Linux 终端操作，但提交的是已经整理好的 Windows 项目目录。
不用把文档、数据和环境全部再搬回 Linux。

以下步骤解释手动发布流程。已经初始化并上传的仓库跳过初始化步骤，使用现有 `origin`。
先在 GitHub 网站创建自己的空仓库，不勾选自动生成 README、LICENSE 或 .gitignore。
[GitHub 官方步骤](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
采用相同的本地仓库流程。

### A. 创建本地 Git 仓库

**Linux Bash，每条完整输入后回车，等待结果。** 先将路径替换成你的 Windows 项目位置。
当前电脑的项目位置是 `/mnt/c/Users/符文/Desktop/NSBI/smeftsim`。

```bash
cd '/mnt/c/Users/符文/Desktop/NSBI/smeftsim'
git init -b main
git config user.name "你的提交署名"
git config user.email "你的GitHub提交邮箱"
git status --short
```

`git config` 没有 `--global`，只设置这个仓库；不改变其他项目。
署名与提交邮箱用于记录提交，不是登录凭据。

### B. 暂存并检查提交范围

**Linux Bash，逐条回车：**

```bash
git add .
git diff --cached --stat
git ls-files
```

应看到 README、handbook、docs、脚本、过程卡、许可证和 curated examples。
不应看到 `.venv`、`ext4.vhdx`、第三方源码、作者 Python 副本或大量运行日志。
`.gitignore` 已为这组示例的 LHE/ROOT 设置明确例外。
若以前曾跟踪过忽略文件，忽略规则不会自动让它们退出 Git，需先整理跟踪列表。

### C. 提交、设置远程并上传

**Linux Bash，逐条回车；替换 GitHub 用户名和仓库名：**

```bash
git commit -m "Add SMEFTsim learning notes and local reweight example"
git remote add origin https://github.com/你的用户名/你的仓库名.git
git remote -v
git push -u origin main
```

`git commit` 只在本地建立记录；`git push` 才发送到 GitHub。
首次通过 HTTPS 推送需要 GitHub 身份认证，不能使用账户密码代替 token。
[GitHub 的 Git 设置说明](https://docs.github.com/en/get-started/git-basics/set-up-git)
介绍 HTTPS、SSH 和凭据方式。不要把 token 写进命令、README 或远程 URL。
已经有 `origin` 时，不重复 `remote add`；先核对 `git remote -v`。

也可以在 Windows 的 Git Bash 或 GitHub Desktop 对同一整理目录提交。
若决定改用 Linux 原生目录作为仓库，应先把这套文档和忽略规则复制过去，
再提交必要文件；仍不上传完整 WSL 磁盘。

返回 [主手册](../../handbook.zh-CN.md) 或 [根 README](../../README.zh-CN.md)。
