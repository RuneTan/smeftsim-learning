# 本地辅助脚本

[English](README.md) | [简体中文](README.zh-CN.md)

`fix_axes.py` 修正 [安装指南第 5 节](../docs/setup/README.zh-CN.md#5-准备两份-python-3-分析脚本)准备的 Python 3 绘图副本的显示效果。
激活 `.venv` 并安装 Ghostscript 后，在项目根目录执行：

```bash
python scripts/fix_axes.py
```

它读取并更新 `work/Material/pyroot_python3/plot_histos.py`，修正坐标轴标签、面板间距、纯 SM 布局和 PDF 字体嵌入；直方图计算与 `tutorial` 中的上游原文件保持不变。
首次修补前会在 `.maintainer-notes/axes/plot_histos.before.py` 保留本地备份；重复执行不会改写已修好的副本。
项目根目录按脚本自身位置定位，因此也可以在其他目录通过脚本绝对路径调用。

返回 [操作手册](../docs/handbook.zh-CN.md) 或 [仓库主页](../README.zh-CN.md)。
