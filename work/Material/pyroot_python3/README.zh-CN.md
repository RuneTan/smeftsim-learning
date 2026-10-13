# 本地 Python 3 兼容脚本

[English](README.md) | [简体中文](README.zh-CN.md)

| 脚本 | 输入 | 输出 | 功能 |
|---|---|---|---|
| `lhe_analyzer.py` | 输入 LHE、输出 ROOT 两个参数 | 每个权重的四个直方图 | 读取四动量、填 bin，按事件数归一化 |
| `plot_histos.py` | 输入 ROOT 一个参数 | 四张 `plot_*.pdf` | 按作者规则画 SM 加单项贡献及相对 SM 比值 |

原作者：Ilaria Brivio 的
[SMEFTsim_tutorial_June23](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)，
固定提交 `92ffde994d7c0d90554ee629cc477ee171c76b84`。
当前工作副本只做 Python 3 必需转换：展开 tab、转换 Python 2 语法、`file()` 改 `open()`。

上游教程未找到明确许可，因此两个 `.py` 保留本地运行并被 Git 忽略。
这份说明和转换步骤随教学仓库分享；若要直接再分发副本，应先向作者确认许可。
不要把这些脚本写成自己原创的分析算法。

## 新机器自行准备副本

**仅在当前目录还没有这两个脚本时执行。**
在已经激活的 Python 3.10 Linux 项目环境、项目根目录下，逐条输入并回车：

```bash
mkdir -p work/Material/pyroot_python3
expand -t 8 tutorial/Material/lhe_analyzer.py > work/Material/pyroot_python3/lhe_analyzer.py
expand -t 8 tutorial/Material/plot_histos.py > work/Material/pyroot_python3/plot_histos.py
python -m lib2to3 -w -n work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
sed -i 's/\bfile[[:space:]]*(/open(/g' work/Material/pyroot_python3/lhe_analyzer.py
sed -i '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' work/Material/pyroot_python3/lhe_analyzer.py work/Material/pyroot_python3/plot_histos.py
```

每条都是完整一行；工具结束再输入下一条。
`expand -t 8` 按 Python 的 tab 宽度展开缩进；`lib2to3` 转换旧语法；
后两条只修改刚创建的工作副本。上游 `tutorial/Material` 始终保留。

此转换步骤已与当前可用副本作语法树比较，两个脚本逻辑一致。
不要用 Python 3.14 执行这里的 `lib2to3`；本课程固定 Python 3.10。

运行方式见 [主手册](../../../handbook.zh-CN.md)，绘图单位见
[图的说明](../../../docs/figures/README.zh-CN.md)。
