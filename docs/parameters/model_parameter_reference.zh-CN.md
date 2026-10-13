# 本教程 UFO 参数索引

[English](model_parameter_reference.md) | [简体中文](model_parameter_reference.zh-CN.md)

输入卡来源：[Ilaria Brivio 的 2023 年 6 月 SMEFTsim 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)；比较使用 `restrict_massless_Hvlvl.dat` 和 `param_card_Hvlvl.dat`。

从 `tutorial/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py` 静态读取；版本 v3.0.2。
共 201 项：118 个 external、83 个 internal。

此表比较原始 UFO 默认值、教程 restriction 与 `param_card_Hvlvl.dat`，不修改它们。
参数卡未列出某项，不等于值为零：它可能在导入时已被固定、合并或由公式计算。
参数合并与最后采用的数值以导入后的 MadGraph 模型及 run banner 为准。
restriction 中的 0/1 可固定参数，相等值也可能使参数合并；不要把 restriction 非零值当作测量结果。

每个源代码链接指向参数声明，可查看完整公式；完整数据另见 [model_parameters.json](model_parameters.json)。

## External：原始模型的输入声明

### CKMBLOCK

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [CKMlambda](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L20) | 2 | 0.2265 | 0.0 | 未列出 |
| [CKMA](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L28) | 3 | 0.79 | 0.0 | 未列出 |
| [CKMrho](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L36) | 4 | 0.141 | 0.0 | 未列出 |
| [CKMeta](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L44) | 5 | 0.357 | 0.0 | 未列出 |

### SMEFT

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [cG](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L52) | 1 | 0 | 0.0 | 未列出 |
| [cW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L60) | 2 | 0 | 0.0 | 未列出 |
| [cH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L68) | 3 | 0 | 0.0 | 未列出 |
| [cHbox](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L76) | 4 | 0 | 0.2 | 0.0 |
| [cHDD](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L84) | 5 | 0 | 0.0 | 未列出 |
| [cHG](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L92) | 6 | 0 | 0.0 | 未列出 |
| [cHW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L100) | 7 | 0 | 0.3 | 0.0 |
| [cHB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L108) | 8 | 0 | 0.0 | 未列出 |
| [cHWB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L116) | 9 | 0 | 0.0 | 未列出 |
| [ceHRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L124) | 10 | 0 | 0.0 | 未列出 |
| [cuHRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L132) | 11 | 0 | 0.0 | 未列出 |
| [cdHRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L140) | 12 | 0 | 0.0 | 未列出 |
| [ceWRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L148) | 13 | 0 | 0.0 | 未列出 |
| [ceBRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L156) | 14 | 0 | 0.0 | 未列出 |
| [cuGRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L164) | 15 | 0 | 0.0 | 未列出 |
| [cuWRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L172) | 16 | 0 | 0.0 | 未列出 |
| [cuBRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L180) | 17 | 0 | 0.0 | 未列出 |
| [cdGRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L188) | 18 | 0 | 0.0 | 未列出 |
| [cdWRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L196) | 19 | 0 | 0.0 | 未列出 |
| [cdBRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L204) | 20 | 0 | 0.0 | 未列出 |
| [cHl1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L212) | 21 | 0 | 0.0 | 未列出 |
| [cHl3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L220) | 22 | 0 | 0.5 | 0.0 |
| [cHe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L228) | 23 | 0 | 0.0 | 未列出 |
| [cHq1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L236) | 24 | 0 | 0.0 | 未列出 |
| [cHq3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L244) | 25 | 0 | 0.6 | 0.0 |
| [cHu](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L252) | 26 | 0 | 0.0 | 未列出 |
| [cHd](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L260) | 27 | 0 | 0.0 | 未列出 |
| [cHudRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L268) | 28 | 0 | 0.0 | 未列出 |
| [cll](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L276) | 29 | 0 | 0.0 | 未列出 |
| [cll1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L284) | 30 | 0 | 0.7 | 0.0 |
| [cqq1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L292) | 31 | 0 | 0.0 | 未列出 |
| [cqq11](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L300) | 32 | 0 | 0.0 | 未列出 |
| [cqq3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L308) | 33 | 0 | 0.0 | 未列出 |
| [cqq31](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L316) | 34 | 0 | 0.0 | 未列出 |
| [clq1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L324) | 35 | 0 | 0.0 | 未列出 |
| [clq3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L332) | 36 | 0 | 0.0 | 未列出 |
| [cee](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L340) | 37 | 0 | 0.0 | 未列出 |
| [cuu](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L348) | 38 | 0 | 0.0 | 未列出 |
| [cuu1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L356) | 39 | 0 | 0.0 | 未列出 |
| [cdd](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L364) | 40 | 0 | 0.0 | 未列出 |
| [cdd1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L372) | 41 | 0 | 0.0 | 未列出 |
| [ceu](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L380) | 42 | 0 | 0.0 | 未列出 |
| [ced](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L388) | 43 | 0 | 0.0 | 未列出 |
| [cud1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L396) | 44 | 0 | 0.0 | 未列出 |
| [cud8](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L404) | 45 | 0 | 0.0 | 未列出 |
| [cle](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L412) | 46 | 0 | 0.0 | 未列出 |
| [clu](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L420) | 47 | 0 | 0.0 | 未列出 |
| [cld](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L428) | 48 | 0 | 0.0 | 未列出 |
| [cqe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L436) | 49 | 0 | 0.0 | 未列出 |
| [cqu1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L444) | 50 | 0 | 0.0 | 未列出 |
| [cqu8](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L452) | 51 | 0 | 0.0 | 未列出 |
| [cqd1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L460) | 52 | 0 | 0.0 | 未列出 |
| [cqd8](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L468) | 53 | 0 | 0.0 | 未列出 |
| [cledqRe](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L476) | 54 | 0 | 0.0 | 未列出 |
| [cquqd1Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L484) | 55 | 0 | 0.0 | 未列出 |
| [cquqd11Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L492) | 56 | 0 | 0.0 | 未列出 |
| [cquqd8Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L500) | 57 | 0 | 0.0 | 未列出 |
| [cquqd81Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L508) | 58 | 0 | 0.0 | 未列出 |
| [clequ1Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L516) | 59 | 0 | 0.0 | 未列出 |
| [clequ3Re](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L524) | 60 | 0 | 0.0 | 未列出 |

### SMEFTcpv

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [cGtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L532) | 1 | 0 | 0.0 | 未列出 |
| [cWtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L540) | 2 | 0 | 0.0 | 未列出 |
| [cHGtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L548) | 3 | 0 | 0.0 | 未列出 |
| [cHWtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L556) | 4 | 0 | 0.0 | 未列出 |
| [cHBtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L564) | 5 | 0 | 0.0 | 未列出 |
| [cHWBtil](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L572) | 6 | 0 | 0.0 | 未列出 |
| [ceWIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L580) | 7 | 0 | 0.0 | 未列出 |
| [ceBIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L588) | 8 | 0 | 0.0 | 未列出 |
| [cuGIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L596) | 9 | 0 | 0.0 | 未列出 |
| [cuWIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L604) | 10 | 0 | 0.0 | 未列出 |
| [cuBIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L612) | 11 | 0 | 0.0 | 未列出 |
| [cdGIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L620) | 12 | 0 | 0.0 | 未列出 |
| [cdWIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L628) | 13 | 0 | 0.0 | 未列出 |
| [cdBIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L636) | 14 | 0 | 0.0 | 未列出 |
| [cHudIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L644) | 15 | 0 | 0.0 | 未列出 |
| [ceHIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L652) | 16 | 0 | 0.0 | 未列出 |
| [cuHIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L660) | 17 | 0 | 0.0 | 未列出 |
| [cdHIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L668) | 18 | 0 | 0.0 | 未列出 |
| [cledqIm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L676) | 19 | 0 | 0.0 | 未列出 |
| [cquqd1Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L684) | 20 | 0 | 0.0 | 未列出 |
| [cquqd8Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L692) | 21 | 0 | 0.0 | 未列出 |
| [cquqd11Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L700) | 22 | 0 | 0.0 | 未列出 |
| [cquqd81Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L708) | 23 | 0 | 0.0 | 未列出 |
| [clequ1Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L716) | 24 | 0 | 0.0 | 未列出 |
| [clequ3Im](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L724) | 25 | 0 | 0.0 | 未列出 |

### SMEFTcutoff

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [LambdaSMEFT](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L732) | 1 | 1000 | 1000.0 | 1000.0 |

### SMINPUTS

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [MW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L740) | 1 | 80.387 | 80.387 | 80.387 |
| [Gf](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L748) | 2 | 1.1663787e-05 | 1.166379e-05 | 1.166379e-05 |
| [aS](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L756) | 3 | 0.1179 | 0.1179 | 0.1179 |

### SWITCHES

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [linearPropCorrections](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L764) | 1 | 0 | 1.0 | 未列出 |

### YUKAWA

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [ymdo](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L772) | 1 | 0.00467 | 0.0 | 未列出 |
| [ymup](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L780) | 2 | 0.00216 | 0.0 | 未列出 |
| [yms](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L788) | 3 | 0.093 | 0.0 | 未列出 |
| [ymc](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L796) | 4 | 1.27 | 0.0 | 未列出 |
| [ymb](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L804) | 5 | 4.18 | 4.18 | 4.18 |
| [ymt](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L812) | 6 | 172.76 | 172.76 | 172.76 |
| [yme](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L820) | 11 | 0.000511 | 0.0 | 未列出 |
| [ymm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L828) | 13 | 0.10566 | 0.0 | 未列出 |
| [ymtau](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L836) | 15 | 1.777 | 1.777 | 1.777 |

### MASS

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [MZ](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L844) | 23 | 91.1876 | 91.1876 | 91.1876 |
| [Me](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L852) | 11 | 0.000511 | 0.0 | 0.0 |
| [MMU](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L860) | 13 | 0.10566 | 0.0 | 0.0 |
| [MTA](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L868) | 15 | 1.777 | 1.777 | 1.777 |
| [MU](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L876) | 2 | 0.00216 | 0.0 | 0.0 |
| [MC](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L884) | 4 | 1.27 | 0.0 | 0.0 |
| [MT](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L892) | 6 | 172.76 | 172.76 | 172.76 |
| [MD](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L900) | 1 | 0.00467 | 0.0 | 0.0 |
| [MS](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L908) | 3 | 0.093 | 0.0 | 0.0 |
| [MB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L916) | 5 | 4.18 | 4.18 | 4.18 |
| [MH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L924) | 25 | 125.09 | 125.09 | 125.09 |

### DECAY

| 参数 | 编号 | UFO 默认值 | 教程 restriction | `param_card_Hvlvl.dat` 中列出的值 |
|---|---:|---:|---:|---:|
| [WZ](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L932) | 23 | 2.4952 | 2.4952 | 2.4952 |
| [WW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L940) | 24 | 2.085 | 2.085 | 2.085 |
| [WT](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L948) | 6 | 1.33 | 1.33 | 1.33 |
| [WH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L956) | 25 | 0.00407 | 0.00407 | 0.00407 |

## Internal：按公式计算的参数

这些量不是相互独立的输入。下面列出全部名字；长公式请打开对应源代码或 JSON。

| 参数 | 类型 | 定义或查看方式 |
|---|---|---|
| [ZERO](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L13) | real | `0.0` |
| [ceH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L964) | complex | `ceHRe + ceHIm*complex(0,1)` |
| [cuH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L970) | complex | `cuHRe + cuHIm*complex(0,1)` |
| [cdH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L976) | complex | `cdHRe + cdHIm*complex(0,1)` |
| [ceW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L982) | complex | `ceWRe + ceWIm*complex(0,1)` |
| [ceB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L988) | complex | `ceBRe + ceBIm*complex(0,1)` |
| [cuG](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L994) | complex | `cuGRe + cuGIm*complex(0,1)` |
| [cuW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1000) | complex | `cuWRe + cuWIm*complex(0,1)` |
| [cuB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1006) | complex | `cuBRe + cuBIm*complex(0,1)` |
| [cdG](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1012) | complex | `cdGRe + cdGIm*complex(0,1)` |
| [cdW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1018) | complex | `cdWRe + cdWIm*complex(0,1)` |
| [cdB](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1024) | complex | `cdBRe + cdBIm*complex(0,1)` |
| [cHud](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1030) | complex | `cHudRe + cHudIm*complex(0,1)` |
| [cledq](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1036) | complex | `cledqRe + cledqIm*complex(0,1)` |
| [cquqd1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1042) | complex | `cquqd1Re + cquqd1Im*complex(0,1)` |
| [cquqd11](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1048) | complex | `cquqd11Re + cquqd11Im*complex(0,1)` |
| [cquqd8](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1054) | complex | `cquqd8Re + cquqd8Im*complex(0,1)` |
| [cquqd81](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1060) | complex | `cquqd81Re + cquqd81Im*complex(0,1)` |
| [clequ1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1066) | complex | `clequ1Re + clequ1Im*complex(0,1)` |
| [clequ3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1072) | complex | `clequ3Re + clequ3Im*complex(0,1)` |
| [MWsm](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1078) | real | `MW` |
| [aEW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1084) | real | `(Gf*MW**2*(1 - MW**2/MZ**2)*cmath.sqrt(2))/cmath.pi` |
| [vevhat](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1090) | real | `1/(2**0.25*cmath.sqrt(Gf))` |
| [lam](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1096) | real | `(Gf*MH**2)/cmath.sqrt(2)` |
| [G](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1102) | real | `2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)` |
| [sth2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1108) | real | `1 - MW**2/MZ**2` |
| [CKM1x1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1114) | complex | `1 - CKMlambda**2/2.` |
| [CKM1x2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1120) | complex | `CKMlambda` |
| [CKM1x3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1126) | complex | `CKMA*CKMlambda**3*(CKMrho - CKMeta*complex(0,1))` |
| [CKM2x1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1132) | complex | `-CKMlambda` |
| [CKM2x2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1138) | complex | `1 - CKMlambda**2/2.` |
| [CKM2x3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1144) | complex | `CKMA*CKMlambda**2` |
| [CKM3x1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1150) | complex | `CKMA*CKMlambda**3*(1 - CKMrho - CKMeta*complex(0,1))` |
| [CKM3x2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1156) | complex | `-(CKMA*CKMlambda**2)` |
| [CKM3x3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1162) | complex | `1` |
| [propCorr](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1168) | real | `abs(linearPropCorrections)/(abs(linearPropCorrections) + 10**-40)` |
| [MZ1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1174) | real | `MZ` |
| [MH1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1180) | real | `MH` |
| [MT1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1186) | real | `MT` |
| [WZ1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1192) | real | `WZ` |
| [WW1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1198) | real | `WW` |
| [WH1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1204) | real | `WH` |
| [WT1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1210) | real | `WT` |
| [gHgg2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1216) | real | `(-7*aS)/(720.*cmath.pi)` |
| [gHgg4](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1222) | real | `aS/(360.*cmath.pi)` |
| [gHgg5](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1228) | real | `aS/(20.*cmath.pi)` |
| [cth](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1234) | real | `cmath.sqrt(1 - sth2)` |
| [MW1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1240) | real | `MWsm` |
| [sth](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1246) | real | `cmath.sqrt(sth2)` |
| [ee](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1252) | real | `2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)` |
| [yb](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1258) | real | `(ymb*cmath.sqrt(2))/vevhat` |
| [yc](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1264) | real | `(ymc*cmath.sqrt(2))/vevhat` |
| [ydo](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1270) | real | `(ymdo*cmath.sqrt(2))/vevhat` |
| [ye](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1276) | real | `(yme*cmath.sqrt(2))/vevhat` |
| [ym](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1282) | real | `(ymm*cmath.sqrt(2))/vevhat` |
| [ys](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1288) | real | `(yms*cmath.sqrt(2))/vevhat` |
| [yt](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1294) | real | `(ymt*cmath.sqrt(2))/vevhat` |
| [ytau](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1300) | real | `(ymtau*cmath.sqrt(2))/vevhat` |
| [yup](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1306) | real | `(ymup*cmath.sqrt(2))/vevhat` |
| [gHgg1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1312) | real | `G**2/(48.*cmath.pi**2)` |
| [gHgg3](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1318) | real | `(aS*G)/(60.*cmath.pi)` |
| [dGf](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1324) | real | `((2*cHl3 - cll1)*vevhat**2)/LambdaSMEFT**2` |
| [dkH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1330) | real | `((cHbox - cHDD/4.)*vevhat**2)/LambdaSMEFT**2` |
| [vevT](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1336) | real | `(1 + dGf/2.)*vevhat` |
| [g1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1342) | real | `ee/cth` |
| [gw](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1348) | real | `ee/sth` |
| [gHaa](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1354) | real | 较长公式，查看源代码 |
| [gHza](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1360) | real | 较长公式，查看源代码 |
| [dgw](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1366) | real | `-dGf/2.` |
| [dMZ2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1372) | real | `((cHDD/2. + 2*cHWB*cth*sth)*vevhat**2)/LambdaSMEFT**2` |
| [dMH2](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1378) | real | `2*dkH - (3*cH*vevhat**2)/(2.*lam*LambdaSMEFT**2)` |
| [barlam](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1384) | real | `(1 - dGf - dMH2)*lam` |
| [dWT](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1390) | real | 较长公式，查看源代码 |
| [dWW](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1396) | real | 较长公式，查看源代码 |
| [gwsh](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1402) | real | `(ee*(1 + dgw - (cHW*vevhat**2)/LambdaSMEFT**2))/sth` |
| [vev](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1408) | real | `(1 - (3*cH*vevhat**2)/(8.*lam*LambdaSMEFT**2))*vevT` |
| [dg1](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1414) | real | `(-dGf - dMZ2/sth**2)/2.` |
| [dWHc](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1420) | real | `yc/(yc + 10**-40)*(-0.02884*(dGf - 2.*dkH + (2.*cuHRe*vevhat**2)/LambdaSMEFT**2))` |
| [dWHb](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1426) | real | `yb/(yb + 10**-40)*(-0.5809*(dGf - 2.*dkH + (2.*cdHRe*vevhat**2)/LambdaSMEFT**2))` |
| [dWHta](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1432) | real | `ytau/(ytau + 10**-40)*(-0.06256*(dGf - 2.*dkH + (2.*ceHRe*vevhat**2)/LambdaSMEFT**2))` |
| [dWH](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1438) | real | 较长公式，查看源代码 |
| [dWZ](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1444) | real | 较长公式，查看源代码 |
| [g1sh](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23/blob/92ffde994d7c0d90554ee629cc477ee171c76b84/Material/SMEFTsim_U35_MwScheme_UFO/parameters.py#L1450) | real | `(ee*(1 + dg1 - (cHB*vevhat**2)/LambdaSMEFT**2))/cth` |
