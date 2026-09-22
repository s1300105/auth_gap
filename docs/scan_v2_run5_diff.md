# full scan の突き合わせ: `scan_v2_run4` → `scan_v2_run5`

再現: `python scripts/compare_scans.py evidence/scan_v2_run4 evidence/scan_v2_run5`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run4 | scan_v2_run5 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 5906 | 5987 | +81 |
| 行 | 9492 | 9576 | +84 |
| `CONTRADICTION` の行 | 170 | 178 | +8 |
| `GAP_INJECT` の行 | 767 | 1928 | +1161 |
| `GAP_SELECT` の行 | 232 | 246 | +14 |
| `UNKNOWN` の行 | 7209 | 7288 | +79 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run4 | 79 |
| scan_v2_run5 | 85 |
| **増えた** | **6** |
| **消えた**（回帰の疑い） | **0** |

### 増えた CONTRADICTION

- `v2-fbratten__agentspool` / `comm_discover_agents` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-fbratten__agentspool` / `comm_get_conversation` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-fbratten__agentspool` / `comm_message_status` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-fbratten__agentspool` / `comm_relay_list_secrets` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-fbratten__agentspool` / `comm_spool_stats` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-rwheeler007__cohort` / `internal_web_fetch` / `FS_WRITE@pathlib.Path.mkdir`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run4 | scan_v2_run5 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 1074 | 3355 | +2281 |
| `OP` / root なし | 6365 | 6150 | -215 |
| `OP` / root あり | 2053 | 71 | -1982 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 2053 → 71（-1982）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 45

- `v2-constripacity__claude-replay|mcp-lowlevel-v1:call_tool:7071a54a23fa|call_tool|claude_replay/server.py:445`: 60 → 74（+14）
- `v2-nightfast-app__hvac-mcp|mcp:register.hvac_refrigerant_pt_lookup:6779de59da58|register.hvac_refrigerant_pt_lookup|src/hvac_mcp/tools/refrigerant.py:174`: 4 → 9（+5）
- `v2-rwheeler007__cohort|mcp:cohort_adopt_persona:4cfac1823ad4|cohort_adopt_persona|cohort/mcp/server.py:1633`: 4 → 8（+4）
- `v2-artyomzemlyak__tg-note|mcp:convert_document_from_content:9166d25bfdec|convert_document_from_content|docker/docling-mcp/app/tg_docling/tools.py:254`: 6 → 8（+2）
- `v2-dreamscaatcher__bigquery-defense-logistics-y42|mcp:query_depot_capacity:39e21309196f|query_depot_capacity|agent/tools/neo4j_tools.py:81`: 0 → 2（+2）
- `v2-dreamscaatcher__bigquery-defense-logistics-y42|mcp:query_route_utilization:e0ae80c638c8|query_route_utilization|agent/tools/neo4j_tools.py:114`: 0 → 2（+2）
- `v2-fbratten__agentspool|mcp:comm_relay_gen_secret:ffb20a048b97|comm_relay_gen_secret|agent_comm_mcp/server.py:597`: 2 → 4（+2）
- `v2-nightfast-app__hvac-mcp|mcp:register.hvac_diagnostic_symptom_tree:7cea92a8bd7a|register.hvac_diagnostic_symptom_tree|src/hvac_mcp/tools/diagnostics.py:136`: 26 → 28（+2）
- `v2-nightfast-app__hvac-mcp|mcp:register.hvac_fault_code_lookup:41e701c4e426|register.hvac_fault_code_lookup|src/hvac_mcp/tools/diagnostics.py:196`: 16 → 18（+2）
- `v2-nightfast-app__hvac-mcp|mcp:register.hvac_refrigerant_charge_check:29a4c41b10a6|register.hvac_refrigerant_charge_check|src/hvac_mcp/tools/refrigerant.py:241`: 0 → 2（+2）
- `v2-rahmanef63__cowork-kit-setup|mcp:list_documents:d36d5fd42096|list_documents|skills/cowork-automation-generator/assets/templates/mcp/server.py:66`: 0 → 2（+2）
- `v2-rahmanef63__cowork-kit-setup|mcp:list_tables:d36d5fd42096|list_tables|skills/cowork-automation-generator/assets/templates/mcp/server.py:25`: 0 → 2（+2）
- `v2-rahmanef63__cowork-kit-setup|mcp:read_document:459d43d19675|read_document|skills/cowork-automation-generator/assets/templates/mcp/server.py:72`: 0 → 2（+2）
- `v2-rahmanef63__cowork-kit-setup|mcp:write_document:17d9fe3000b2|write_document|skills/cowork-automation-generator/assets/templates/mcp/server.py:79`: 0 → 2（+2）
- `v2-rwheeler007__cohort|mcp:cohort_find_agents:c8c67bbcdf5e|cohort_find_agents|cohort/mcp/server.py:1793`: 5 → 7（+2）
- `v2-rwheeler007__cohort|mcp:cohort_partnership_graph:c9f40fd8d1af|cohort_partnership_graph|cohort/mcp/server.py:1838`: 5 → 7（+2）
- `v2-rwheeler007__cohort|mcp:cohort_route_task:130443b0a939|cohort_route_task|cohort/mcp/server.py:1722`: 5 → 7（+2）
- `v2-rwheeler007__cohort|mcp:desktop_action:c28e61cf8465|desktop_action|cohort/desktop/mcp_server.py:156`: 4 → 6（+2）
- `v2-rwheeler007__cohort|mcp:desktop_status:d36d5fd42096|desktop_status|cohort/desktop/mcp_server.py:248`: 5 → 7（+2）
- `v2-dddabtc__winremote-mcp|mcp:FileUpload:35f29b0058e0|FileUpload|src/winremote/__main__.py:1092`: 1 → 2（+1）
