"""Read UFO parameter declarations without importing or executing the model."""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
MODEL = BASE / "tutorial/Material/SMEFTsim_U35_MwScheme_UFO"


def read_card(path):
    values = {}
    block = None
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split("#", 1)[0].split()
        if not fields:
            continue
        if fields[0].lower() == "block":
            block = fields[1].upper()
        elif fields[0].lower() == "decay":
            values[("DECAY", int(fields[1]))] = float(fields[2])
            block = None
        elif block and len(fields) >= 2 and not block.startswith("QNUMBERS"):
            values[(block, int(fields[0]))] = float(fields[1].replace("D", "E"))
    return values


def main():
    source = MODEL / "parameters.py"
    restriction = read_card(MODEL / "restrict_massless_Hvlvl.dat")
    run_card = read_card(BASE / "tutorial/Material/param_card_Hvlvl.dat")
    rows = []
    for node in ast.parse(source.read_text(encoding="utf-8")).body:
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "Parameter"):
            continue
        row = {k.arg: ast.literal_eval(k.value) for k in node.value.keywords}
        row["source_line"] = node.lineno
        if row["nature"] == "external":
            key = (row["lhablock"].upper(), row["lhacode"][0])
            row["tutorial_restriction_value"] = restriction.get(key)
            row["tutorial_run_card_value"] = run_card.get(key)
            row["listed_in_tutorial_run_card"] = key in run_card
        rows.append(row)

    outdir = BASE / "outputs"
    outdir.mkdir(exist_ok=True)
    counts = dict(Counter(row["nature"] for row in rows))
    report = {
        "model": "SMEFTsim_U35_MwScheme_UFO",
        "version": (MODEL / "version.info").read_text().strip(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "scope": "Static declarations and author cards; not an evaluated MadGraph model",
        "counts": counts,
        "parameters": rows,
    }
    (outdir / "model_parameters.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 本教程 UFO 参数索引", "",
        "从 `tutorial/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py` 静态读取；版本 v3.0.2。",
        f"共 {len(rows)} 项：{counts['external']} 个 external、{counts['internal']} 个 internal。", "",
        "此表比较原始 UFO 默认值、作者 restriction 与作者运行卡，不修改它们。",
        "运行卡未列出某项，不等于值为零：它可能在导入时已被固定、合并或由公式计算。",
        "参数合并与最后采用的数值以导入后的 MadGraph 模型及 run banner 为准。",
        "restriction 中的 0/1 可固定参数，相等值也可能使参数合并；不要把 restriction 非零值当作测量结果。", "",
        f"每个源代码链接指向参数声明，可查看完整公式；完整数据另见 [model_parameters.json]({outdir.as_posix()}/model_parameters.json)。", "",
        "## External：原始模型的输入声明", "",
    ]
    external_rows = [row for row in rows if row["nature"] == "external"]
    for block in dict.fromkeys(row["lhablock"] for row in external_rows):
        lines.extend([f"### {block}", "",
                      "| 参数 | 编号 | UFO 默认值 | 教程 restriction | 作者运行卡中列出的值 |",
                      "|---|---:|---:|---:|---:|"])
        for row in external_rows:
            if row["lhablock"] != block:
                continue
            source_link = f"{source.as_posix()}:{row['source_line']}"
            restriction_value = row["tutorial_restriction_value"]
            run_value = row["tutorial_run_card_value"]
            lines.append(
                f"| [{row['name']}]({source_link}) | {row['lhacode'][0]} | {row['value']} | "
                f"{restriction_value if restriction_value is not None else '未列出'} | "
                f"{run_value if run_value is not None else '未列出'} |")
        lines.append("")

    lines.extend(["## Internal：按公式计算的参数", "",
                  "这些量不是相互独立的输入。下面列出全部名字；长公式请打开对应源代码或 JSON。", "",
                  "| 参数 | 类型 | 定义或查看方式 |", "|---|---|---|"])
    for row in rows:
        if row["nature"] != "internal":
            continue
        value = str(row["value"])
        display = f"`{value}`" if len(value) < 95 else "较长公式，查看源代码"
        source_link = f"{source.as_posix()}:{row['source_line']}"
        lines.append(f"| [{row['name']}]({source_link}) | {row['type']} | {display} |")
    (outdir / "model_parameter_reference.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Read {len(rows)} parameters: {counts}")
    print("Saved outputs/model_parameter_reference.md and outputs/model_parameters.json")


if __name__ == "__main__":
    main()
