# 2023 年教程参考结果

[English](README.md) | [简体中文](README.zh-CN.md)

这里存放从 [Ilaria Brivio 的 2023 年 6 月 SMEFTsim 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) 的 `SMEFTsim_tutorial_results.zip` 解压的参考结果：
压缩 LHE、ROOT 直方图和参考 PDF。

它与 [examples](../examples/README.zh-CN.md) 不同：这是教程提供的参考数据，不是本项目生成的样本。
参考包保留本地，Git 忽略规则只允许这份目录说明进入仓库。

完整路径与图的阅读方法如下。

### 6.3 参考 ROOT 文件在哪里

教程结果包 `tutorial/SMEFTsim_tutorial_results.zip` 已解压到 `reference/Results`。
对应来源是 [2023 年教程仓库](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)。

Windows 路径：

```text
C:\Users\符文\Desktop\NSBI\smeftsim\reference\Results\Root_files
```

| 文件 | 文件保存的贡献 |
|---|---|
| `Hvlvl_SM_run_01.root` | SM 直接样本及多个重加权贡献 |
| `Hvlvl_SMEFT_run_01.root` | 普通维六振幅平方的直接样本 |
| `Hvlvl_SMEFT_linear_run_01.root` | 普通 SM–维六干涉的直接样本 |
| `Hvlvl_SMEFT_prop_run_01.root` | 传播子线性干涉的直接样本 |

在本机 Linux 中，这些文件位于
`/mnt/c/Users/符文/Desktop/NSBI/smeftsim/reference/Results/Root_files`。

**参考图的多条曲线主要来自一个 SM ROOT 文件中的多个权重直方图。**
三个直接生成的 EFT 文件用来另作一致性检查，不必先把它们合并才能画参考图。
安装校验曾从四个参考 LHE 重建 92 个直方图并核对 bin 内容；
报告见 `outputs/pyroot_validation/report.json`。自己的新事件需要考虑统计波动，
不要求与参考结果逐 bin 完全一致。
