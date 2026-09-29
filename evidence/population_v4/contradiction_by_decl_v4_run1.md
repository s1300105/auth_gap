# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）

再現: `python scripts/contradiction_by_decl.py evidence/scan_v2_v4_run1`

単位は (木, ユニットの relpath:行, qualname, site, kind)（D64 / U50）。**D1〜D4 は 4 つとも主指標（D62）。宣言ごとに読み、合算しない。**「D1+D2 矛」の列は過去の run と比べるためだけに残す（主指標ではない）。

## 採った原理での件数

| 宣言 | 矛 | 不 | 矛の木 |
|---|---|---|---|
| D1 | 323 | 171 | 17 |
| D2 | 155 | 257 | 14 |
| D3 | 0 | 74 | 0 |
| D4 | 3 | 73 | 1 |

## 理由ごとの内訳（採った原理）

| 宣言 | 結果 | 理由 | 組 |
|---|---|---|---|
| D1 | 不 | `db_sql_model_opaque` | 2 |
| D1 | 不 | `db_sql_unreadable` | 7 |
| D1 | 不 | `net_method_unknown` | 17 |
| D1 | 不 | `net_post` | 78 |
| D1 | 不 | `spawn_command` | 64 |
| D1 | 不 | `spawn_model_opaque` | 14 |
| D1 | 矛 | `db_model_sql` | 1 |
| D1 | 矛 | `db_modify` | 22 |
| D1 | 矛 | `db_persistent` | 15 |
| D1 | 矛 | `exec` | 1 |
| D1 | 矛 | `fs_write` | 298 |
| D1 | 矛 | `net_method_model` | 1 |
| D2 | 不 | `db_persistent` | 2 |
| D2 | 不 | `db_sql_model_opaque` | 1 |
| D2 | 不 | `db_sql_unreadable` | 15 |
| D2 | 不 | `fs_unknown` | 2 |
| D2 | 不 | `fs_writeout` | 121 |
| D2 | 不 | `fs_writeout_model_path_opaque` | 9 |
| D2 | 不 | `net_post` | 93 |
| D2 | 不 | `spawn_command` | 19 |
| D2 | 不 | `spawn_model_opaque` | 2 |
| D2 | 矛 | `db_modify` | 6 |
| D2 | 矛 | `fs_remove` | 144 |
| D2 | 矛 | `fs_writeout_model_path` | 2 |
| D2 | 矛 | `net_method_model` | 1 |
| D2 | 矛 | `net_modify` | 2 |
| D3 | 不 | `net_host_unknown` | 22 |
| D3 | 不 | `net_model_host_opaque` | 6 |
| D3 | 不 | `spawn_command` | 42 |
| D3 | 不 | `spawn_model_opaque` | 12 |
| D4 | 不 | `db_nonidempotent_statement` | 5 |
| D4 | 不 | `db_sql_unreadable` | 3 |
| D4 | 不 | `exec_or_spawn` | 1 |
| D4 | 不 | `net_nonidempotent_method` | 67 |
| D4 | 矛 | `fs_append` | 3 |

## 感度分析（原理を 1 つずつ反対側にする）

| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | D1+D2 矛（比較用） | D3 矛 | D3 不 | D4 矛 | D4 不 |
|---|---|---|---|---|---|---|---|---|---|
| 採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a） | 323 | 171 | 155 | 257 | 478 | 0 | 74 | 3 | 73 |
| 1-i を a に（永続する設定を含めない） | 323 | 171 | 155 | 257 | 478 | 0 | 74 | 3 | 73 |
| 1-ii を a に（リモートの状態を含めない） | 322 | 76 | 152 | 164 | 474 | 0 | 74 | 3 | 73 |
| 2 を b に（不明を矛盾に倒す） | 494 | 0 | 412 | 0 | 906 | 74 | 0 | 76 | 0 |
| 2 を c に（不明を宣言内に倒す） | 323 | 0 | 155 | 0 | 478 | 0 | 0 | 3 | 0 |
| 3 を b に（モデル由来の値を能力として読まない） | 321 | 173 | 152 | 260 | 473 | 0 | 74 | 3 | 73 |
| 4 を b に（破壊性の 2 つだけ） | 323 | 171 | 155 | 257 | 478 | 0 | 0 | 0 | 0 |

