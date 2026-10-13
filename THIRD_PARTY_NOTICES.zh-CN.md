# 第三方来源与许可说明

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

核对时间：2026-10-13。此文件记录来源与发布边界，不代替具体上游许可证。

## SMEFTsim 模型与参数资料

来源：[SMEFTsim](https://github.com/SMEFTsim/SMEFTsim)，教程模型 v3.0.2。
官方 v3.0.2 标签的 LICENSE 为 MIT，Copyright (c) 2020 SMEFTsim。
完整许可保存在 [licenses/SMEFTsim-MIT.txt](licenses/SMEFTsim-MIT.txt)。

本项目参数索引静态整理模型声明、公式和作者卡的数值；它不是新的物理模型。
理论依据与引用论文见 [根 README](README.zh-CN.md)。
模型源码仍从上游获取，不随本仓库发布。

## 2023 年教程

作者：Ilaria Brivio。
来源：[SMEFTsim_tutorial_June23](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)，
提交 `92ffde994d7c0d90554ee629cc477ee171c76b84`。

原过程、卡、restriction、分析器和绘图逻辑均按该教程学习。
固定本地副本没有找到 LICENSE，当前 GitHub API 许可字段为 null；
没有据此认定其独立教程脚本已获 MIT 授权。

本地 `tutorial`、`work/Material` 的作者材料和两个 Python 3 兼容脚本被 Git 忽略。
兼容转换只有 tab 展开、Python 2 语法转换、`file()` 到 `open()`；
转换方法保留在 [工作副本说明](work/Material/pyroot_python3/README.zh-CN.md)。
希望公开再分发这些副本时，应另行核实作者许可。

## MadGraph 与 ROOT

MadGraph5_aMC@NLO 2.9.27，MadTeam：
本地核心 `madgraph/LICENSE` 是改写自 Illinois/NCSA 的许可，
原文保存在 [licenses/MadGraph-NCSA.txt](licenses/MadGraph-NCSA.txt)。
vendor 组件可能有其他许可。程序源码与二进制不纳入本项目发布。

ROOT/PyROOT 采用 [LGPL 2.1 或更新版本](https://root.cern/about/license/)，
本项目只在本地环境调用，不分发 ROOT 安装或共享库。

## 本项目生成的示例

`examples/reweighted` 是用户本地生成并重加权的 2,000 个事件，
不是上游参考包的复制。公开 LHE 保留数值初始化、事件和权重，省略完整生成器 banner 与卡片模板；本地原始文件不变。参数、运行设置、种子、版本、权重与原始及公开文件 SHA256 记录在 `metadata.json`。PDF 和 PNG 通过作者绘图方法生成并明确署名。

程序输出与程序代码的许可范围不同；生成文件含有的模板、上游文本或素材应分别考虑。
因此此说明不把整个示例包装成“所有内容均由本项目原创”。
不宣称原作者背书，也不宣称教学样本完成了独立 closure 或正式研究验证。

## 本项目自身许可

README、中英文操作说明和辅助入口属于本项目整理范围。
当前未选择统一发布许可证；此文件不对第三方内容重新授权。
相关选择说明见 [发布 README](docs/publishing/README.zh-CN.md)。
