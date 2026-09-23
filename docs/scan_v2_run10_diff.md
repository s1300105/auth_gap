# full scan の突き合わせ: `scan_v2_run9` → `scan_v2_run10`

再現: `python scripts/compare_scans.py evidence/scan_v2_run9 evidence/scan_v2_run10`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run9 | scan_v2_run10 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 7462 | 7503 | +41 |
| 行 | 11534 | 11611 | +77 |
| `CONTRADICTION` の行 | 178 | 178 | +0 |
| `GAP_INJECT` の行 | 2204 | 2236 | +32 |
| `GAP_SELECT` の行 | 246 | 246 | +0 |
| `UNKNOWN` の行 | 9130 | 9193 | +63 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run9 | 85 |
| scan_v2_run10 | 85 |
| **増えた** | **0** |
| **消えた**（回帰の疑い） | **0** |

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run9 | scan_v2_run10 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 3631 | 3664 | +33 |
| `OP` / root なし | 7832 | 7876 | +44 |
| `OP` / root あり | 71 | 71 | +0 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 71 → 71（+0）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 15

- `v2-raphaelabenom__agents-repo|mcp:create_order:7de5ce21071b|create_order|2_langgraph/sales-ai-agent-langgraph/virtual_sales_agent/tools.py:138`: 0 → 10（+10）
- `v2-zelladir__asquared-mcp|mcp:build_mcp.coord_post:5fb70612b092|build_mcp.coord_post|src/asquared_mcp/server.py:221`: 1 → 9（+8）
- `v2-zelladir__asquared-mcp|mcp:build_mcp.coord_ack:1b7491e81c3f|build_mcp.coord_ack|src/asquared_mcp/server.py:329`: 0 → 4（+4）
- `v2-raphaelabenom__agents-repo|mcp:search_products:a52b97a17e1b|search_products|2_langgraph/sales-ai-agent-langgraph/virtual_sales_agent/tools.py:30`: 0 → 3（+3）
- `v2-raphaelabenom__agents-repo|mcp:search_products_recommendations:78058e6ed17a|search_products_recommendations|2_langgraph/sales-ai-agent-langgraph/virtual_sales_agent/tools.py:329`: 0 → 3（+3）
- `v2-zelladir__asquared-mcp|mcp:build_mcp.coord_threads_tool:6fc7a02837aa|build_mcp.coord_threads_tool|src/asquared_mcp/server.py:299`: 0 → 3（+3）
- `v2-raphaelabenom__agents-repo|mcp:check_order_status:4dbb9d1828bc|check_order_status|2_langgraph/sales-ai-agent-langgraph/virtual_sales_agent/tools.py:237`: 0 → 2（+2）
- `v2-franklinbaldo__sinustdd|mcp:sinustdd_begin:d36d5fd42096|sinustdd_begin|src/sinustdd/mcp.py:46`: 0 → 1（+1）
- `v2-franklinbaldo__sinustdd|mcp:sinustdd_green:d36d5fd42096|sinustdd_green|src/sinustdd/mcp.py:71`: 0 → 1（+1）
- `v2-franklinbaldo__sinustdd|mcp:sinustdd_red:d36d5fd42096|sinustdd_red|src/sinustdd/mcp.py:59`: 0 → 1（+1）
- `v2-franklinbaldo__sinustdd|mcp:sinustdd_refactor:d36d5fd42096|sinustdd_refactor|src/sinustdd/mcp.py:81`: 0 → 1（+1）
- `v2-raphaelabenom__agents-repo|mcp:get_available_categories:d36d5fd42096|get_available_categories|2_langgraph/sales-ai-agent-langgraph/virtual_sales_agent/tools.py:14`: 0 → 1（+1）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_file_tools.upload_course_file:8ad68cb2946c|register_educator_file_tools.upload_course_file|src/canvas_mcp/tools/files.py:320`: 22 → 23（+1）
- `v2-zelladir__asquared-mcp|mcp:build_mcp.coord_read:1316e6f7c6f0|build_mcp.coord_read|src/asquared_mcp/server.py:262`: 0 → 1（+1）
- `v2-zelladir__asquared-mcp|mcp:build_mcp.coord_status:8055283091fb|build_mcp.coord_status|src/asquared_mcp/server.py:347`: 0 → 1（+1）
