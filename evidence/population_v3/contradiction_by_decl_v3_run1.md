# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）

再現: `python scripts/contradiction_by_decl.py evidence/scan_v2_v3_run1`

単位は (木, ユニット, site, kind)。**D1 / D2 は事前登録済みの主指標、D3 / D4 は探索的。合算しない。**

## 採った原理での件数

| 宣言 | 矛 | 不 | 矛の木 |
|---|---|---|---|
| D1 | 75 | 46 | 11 |
| D2 | 11 | 49 | 4 |
| D3 | 2 | 36 | 1 |
| D4 | 1 | 20 | 1 |

## 理由ごとの内訳（採った原理）

| 宣言 | 結果 | 理由 | 組 |
|---|---|---|---|
| D1 | 不 | `db_sql_model_opaque` | 3 |
| D1 | 不 | `db_sql_unreadable` | 1 |
| D1 | 不 | `net_method_unknown` | 3 |
| D1 | 不 | `net_post` | 13 |
| D1 | 不 | `spawn_command` | 20 |
| D1 | 不 | `spawn_model_opaque` | 15 |
| D1 | 矛 | `db_modify` | 17 |
| D1 | 矛 | `db_persistent` | 8 |
| D1 | 矛 | `fs_write` | 55 |
| D1 | 矛 | `spawn_model` | 2 |
| D2 | 不 | `db_persistent` | 1 |
| D2 | 不 | `fs_unknown` | 10 |
| D2 | 不 | `fs_writeout` | 8 |
| D2 | 不 | `fs_writeout_model_path_opaque` | 8 |
| D2 | 不 | `net_method_unknown` | 1 |
| D2 | 不 | `net_post` | 2 |
| D2 | 不 | `spawn_command` | 8 |
| D2 | 不 | `spawn_model_opaque` | 14 |
| D2 | 矛 | `fs_remove` | 11 |
| D3 | 不 | `net_host_unknown` | 6 |
| D3 | 不 | `net_model_host_opaque` | 13 |
| D3 | 不 | `spawn_command` | 19 |
| D3 | 不 | `spawn_model_opaque` | 4 |
| D3 | 矛 | `spawn_model` | 2 |
| D4 | 不 | `exec_or_spawn` | 18 |
| D4 | 不 | `net_method_unknown` | 1 |
| D4 | 不 | `net_nonidempotent_method` | 1 |
| D4 | 矛 | `fs_append` | 1 |

## 感度分析（原理を 1 つずつ反対側にする）

| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | **D1+D2 矛** | D3 矛 | D3 不 | D4 矛 | D4 不 |
|---|---|---|---|---|---|---|---|---|---|
| 採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a） | 75 | 46 | 11 | 49 | **86** | 2 | 36 | 1 | 20 |
| 1-i を a に（永続する設定を含めない） | 74 | 46 | 11 | 48 | **85** | 2 | 36 | 1 | 20 |
| 1-ii を a に（リモートの状態を含めない） | 75 | 31 | 11 | 46 | **86** | 2 | 36 | 1 | 20 |
| 2 を b に（不明を矛盾に倒す） | 121 | 0 | 60 | 0 | **180** | 38 | 0 | 21 | 0 |
| 2 を c に（不明を宣言内に倒す） | 75 | 0 | 11 | 0 | **86** | 2 | 0 | 1 | 0 |
| 3 を b に（モデル由来の値を能力として読まない） | 73 | 48 | 11 | 49 | **84** | 0 | 38 | 1 | 20 |
| 4 を b に（破壊性の 2 つだけ） | 75 | 46 | 11 | 49 | **86** | 0 | 0 | 0 | 0 |

