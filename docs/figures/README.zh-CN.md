# 示例图片

[English](README.md) | [简体中文](README.zh-CN.md)

这些 PNG 来自本项目自己的 2,000 个 SM 基础事件，不是从作者参考结果包复制的图。

| 文件组 | 如何得到 | 内容 |
|---|---|---|
| `sm_mll.png`、`sm_mmv.png`、`sm_pTl1.png`、`sm_pTmu.png` | 作者分析器填好直方图，再调用 ROOT `Draw`/`SaveAs` | 纯 SM，每 bin 的宽度贡献 |
| `rw_mll.png`、`rw_mmv.png`、`rw_pTl1.png`、`rw_pTmu.png` | 用户重加权 ROOT，调用作者绘图逻辑 | SM 与单项 EFT 修正的比较 |

作者重加权图保留原样式；图中的旧 `pb` 标签不适用于本例的 Higgs 衰变。
实际 bin 内容为 `sum(weights)/N`，单位 GeV；`mll`、`mmv` 的 bin 宽为 5 GeV，
两个横动量分布的 bin 宽为 4 GeV。要得到微分密度，还要除以 bin 宽。
下半图是相对 SM 的比值，单位约定不会改变它。

`cHl3`、`cHl3_sq`、`cHl3_propW` 分别表示线性、平方和传播子贡献。
作者脚本分别画 SM 加一项，没有自动相加全部修正。

图是教学中心值，没有完整误差带。原始示例与元数据见
[examples/reweighted](../../examples/reweighted/README.zh-CN.md)。
