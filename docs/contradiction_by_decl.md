# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）

再現: `python scripts/contradiction_by_decl.py evidence/scan_v2_run13`

単位は (木, ユニット, site, kind)。**D1 / D2 は事前登録済みの主指標、D3 / D4 は探索的。合算しない。**

## 採った原理での件数

| 宣言 | 矛 | 不 | 矛の木 |
|---|---|---|---|
| D1 | 109 | 86 | 13 |
| D2 | 56 | 95 | 13 |
| D3 | 51 | 81 | 7 |
| D4 | 5 | 77 | 1 |

## 理由ごとの内訳（採った原理）

| 宣言 | 結果 | 理由 | 組 |
|---|---|---|---|
| D1 | 不 | `db_sql_unreadable` | 25 |
| D1 | 不 | `net_method_unknown` | 23 |
| D1 | 不 | `net_post` | 25 |
| D1 | 不 | `spawn_command` | 13 |
| D1 | 矛 | `db_model_sql` | 1 |
| D1 | 矛 | `db_modify` | 6 |
| D1 | 矛 | `db_persistent` | 11 |
| D1 | 矛 | `fs_write` | 91 |
| D2 | 不 | `db_persistent` | 10 |
| D2 | 不 | `db_sql_unreadable` | 13 |
| D2 | 不 | `fs_writeout` | 20 |
| D2 | 不 | `net_method_unknown` | 4 |
| D2 | 不 | `net_post` | 53 |
| D2 | 不 | `spawn_command` | 5 |
| D2 | 矛 | `db_model_sql` | 3 |
| D2 | 矛 | `db_modify` | 26 |
| D2 | 矛 | `fs_remove` | 11 |
| D2 | 矛 | `fs_writeout_model_path` | 6 |
| D2 | 矛 | `net_modify` | 8 |
| D2 | 矛 | `net_put_model_url` | 2 |
| D3 | 不 | `net_host_unknown` | 71 |
| D3 | 不 | `spawn_command` | 13 |
| D3 | 矛 | `net_external_host` | 37 |
| D3 | 矛 | `net_model_host` | 14 |
| D4 | 不 | `db_nonidempotent_statement` | 17 |
| D4 | 不 | `db_sql_unreadable` | 10 |
| D4 | 不 | `net_nonidempotent_method` | 54 |
| D4 | 矛 | `fs_append` | 5 |

## 感度分析（原理を 1 つずつ反対側にする）

| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | **D1+D2 矛** | D3 矛 | D3 不 | D4 矛 | D4 不 |
|---|---|---|---|---|---|---|---|---|---|
| 採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a） | 109 | 86 | 56 | 95 | **165** | 51 | 81 | 5 | 77 |
| 1-i を a に（永続する設定を含めない） | 98 | 86 | 56 | 85 | **154** | 51 | 81 | 5 | 77 |
| 1-ii を a に（リモートの状態を含めない） | 109 | 38 | 46 | 40 | **155** | 51 | 81 | 5 | 77 |
| 2 を b に（不明を矛盾に倒す） | 195 | 0 | 151 | 0 | **346** | 132 | 0 | 82 | 0 |
| 2 を c に（不明を宣言内に倒す） | 109 | 0 | 56 | 0 | **165** | 51 | 0 | 5 | 0 |
| 3 を b に（モデル由来の値を能力として読まない） | 108 | 87 | 45 | 106 | **153** | 37 | 95 | 5 | 77 |
| 4 を b に（破壊性の 2 つだけ） | 109 | 86 | 56 | 95 | **165** | 0 | 0 | 0 | 0 |

