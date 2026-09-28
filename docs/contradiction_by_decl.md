# CONTRADICTION の宣言ごとの件数と、判定原理の感度分析（D56）

再現: `python scripts/contradiction_by_decl.py evidence/scan_v2_run23`

単位は (木, ユニットの relpath:行, qualname, site, kind)（D64 / U50）。**D1〜D4 は 4 つとも主指標（D62）。宣言ごとに読み、合算しない。**「D1+D2 矛」の列は過去の run と比べるためだけに残す（主指標ではない）。

## 採った原理での件数

| 宣言 | 矛 | 不 | 矛の木 |
|---|---|---|---|
| D1 | 110 | 153 | 13 |
| D2 | 45 | 135 | 9 |
| D3 | 39 | 110 | 5 |
| D4 | 0 | 91 | 0 |

## 理由ごとの内訳（採った原理）

| 宣言 | 結果 | 理由 | 組 |
|---|---|---|---|
| D1 | 不 | `db_sql_model_opaque` | 1 |
| D1 | 不 | `db_sql_unreadable` | 25 |
| D1 | 不 | `db_unknown_statement` | 1 |
| D1 | 不 | `net_method_unknown` | 23 |
| D1 | 不 | `net_post` | 81 |
| D1 | 不 | `spawn_command` | 21 |
| D1 | 不 | `spawn_model_opaque` | 2 |
| D1 | 矛 | `db_modify` | 7 |
| D1 | 矛 | `db_persistent` | 11 |
| D1 | 矛 | `fs_write` | 92 |
| D2 | 不 | `db_persistent` | 10 |
| D2 | 不 | `db_sql_model_opaque` | 3 |
| D2 | 不 | `db_sql_unreadable` | 6 |
| D2 | 不 | `db_unknown_statement` | 1 |
| D2 | 不 | `fs_writeout` | 19 |
| D2 | 不 | `fs_writeout_model_path_opaque` | 9 |
| D2 | 不 | `net_method_unknown` | 4 |
| D2 | 不 | `net_post` | 72 |
| D2 | 不 | `net_put_model_url_opaque` | 2 |
| D2 | 不 | `spawn_command` | 11 |
| D2 | 不 | `spawn_model_opaque` | 3 |
| D2 | 矛 | `db_modify` | 27 |
| D2 | 矛 | `fs_remove` | 10 |
| D2 | 矛 | `net_modify` | 8 |
| D3 | 不 | `net_host_unknown` | 76 |
| D3 | 不 | `net_model_host_opaque` | 9 |
| D3 | 不 | `spawn_command` | 25 |
| D3 | 不 | `spawn_model_opaque` | 2 |
| D3 | 矛 | `net_external_host` | 38 |
| D3 | 矛 | `net_model_host` | 1 |
| D4 | 不 | `db_nonidempotent_statement` | 17 |
| D4 | 不 | `net_nonidempotent_method` | 74 |

## 感度分析（原理を 1 つずつ反対側にする）

| 変えた原理 | D1 矛 | D1 不 | D2 矛 | D2 不 | D1+D2 矛（比較用） | D3 矛 | D3 不 | D4 矛 | D4 不 |
|---|---|---|---|---|---|---|---|---|---|
| 採った原理（1-i b / 1-ii b / 2 a / 3 a / 4 a） | 110 | 153 | 45 | 135 | 155 | 39 | 110 | 0 | 91 |
| 1-i を a に（永続する設定を含めない） | 99 | 153 | 45 | 125 | 144 | 39 | 110 | 0 | 91 |
| 1-ii を a に（リモートの状態を含めない） | 110 | 49 | 37 | 59 | 147 | 39 | 110 | 0 | 91 |
| 2 を b に（不明を矛盾に倒す） | 263 | 0 | 180 | 0 | 443 | 149 | 0 | 91 | 0 |
| 2 を c に（不明を宣言内に倒す） | 110 | 0 | 45 | 0 | 155 | 39 | 0 | 0 | 0 |
| 3 を b に（モデル由来の値を能力として読まない） | 110 | 153 | 45 | 135 | 155 | 38 | 111 | 0 | 91 |
| 4 を b に（破壊性の 2 つだけ） | 110 | 153 | 45 | 135 | 155 | 0 | 0 | 0 | 0 |

