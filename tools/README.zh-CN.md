# 第三方程序源码

[English](README.md) | [简体中文](README.zh-CN.md)

本目录中的 `MG5_aMC_v2_9_27` 是第三方 MadGraph 源码，不是本项目开发的生成器。
保留其原始文档和许可，源码从上游获取，不随本教学仓库上传。

| 程序 | 固定版本 | 用途 |
|---|---|---|
| MadGraph5_aMC@NLO | 2.9.27，提交 `eb76cab72b8d44aac7162ac7221ac08a4384a169` | 模型导入、过程导出、积分、事件生成与重加权 |

**新电脑下载材料；当前电脑已有目录时跳过。**
在 Windows 项目根目录逐条回车：

```powershell
git clone https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial
git -C tutorial checkout 92ffde994d7c0d90554ee629cc477ee171c76b84
git clone https://github.com/mg5amcnlo/mg5amcnlo.git tools/MG5_aMC_v2_9_27
git -C tools/MG5_aMC_v2_9_27 checkout eb76cab72b8d44aac7162ac7221ac08a4384a169
```

`tutorial` 在项目根目录，保留下载的教程 README。
Linux 的 `setup_linux.sh` 从固定源码重新检出以恢复符号链接。
本地 MadGraph 核心许可是改写自 Illinois/NCSA 的许可；
第三方 vendor 组件可能采用不同许可，不能用一句全项目 MIT 覆盖它们。
