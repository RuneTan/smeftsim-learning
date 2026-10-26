# 示例图片

[English](README.md) | [简体中文](README.zh-CN.md)

这些图使用本项目在本地生成的 2,000 个 SM 基础事件及其额外权重。
直方图由 `lhe_analyzer.py` 生成；纯 SM 与重加权图都调用 Ilaria Brivio
[2023 年 6 月教程的 `plot_histos.py`](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/plot_histos.py) 的 Python 3 副本。
安装步骤通过 `scripts/fix_axes.py` 修正本地标签与布局，直方图计算保持不变。PDF 通过 ROOT 的 `Print(..., "EmbedFonts")` 与 Ghostscript 嵌入字体，避免希腊字母依赖阅读器的替代字体；PNG 导出自同一张 ROOT 画布。

| 文件名后缀 | 横轴 | 定义 |
|---|---|---|
| `mll` | $m(e,\mu)$ | 电子与 muon 的不变质量 |
| `mmv` | $m(\mu,\nu_\mu)$ | muon 与其对应中微子的不变质量，使用生成器真值动量 |
| `pTl1` | $p_T(l_1)$ | 领先带电轻子的横动量：$\max(p_T(e),p_T(\mu))$ |
| `pTmu` | $p_T(\mu)$ | muon 的横动量 |

`sm_*.png` 用单面板显示纯 SM；`rw_*.png` 比较 SM 与各项 EFT 修正，并附相对 SM 的比值面板。
纵轴标签为 $\Gamma_{\mathrm{bin}}$ [GeV]：bin 内容是 `sum(weights)/N`，表示部分衰变宽度贡献，不是以 pb 为单位的截面。
`mll`、`mmv` 的 bin 宽为 5 GeV，两个横动量分布的 bin 宽为 4 GeV。
除以 bin 宽才得到微分宽度；下半图是相对 SM 的无量纲比值。

`cHl3`、`cHl3_sq`、`cHl3_propW` 分别表示线性、振幅平方和传播子贡献。
每条彩色曲线只在 SM 上加一项，绘图器不会自动相加全部修正。
图是教学中心值，没有完整误差带。数据与元数据见
[examples/reweighted](../../examples/reweighted/README.zh-CN.md)。
