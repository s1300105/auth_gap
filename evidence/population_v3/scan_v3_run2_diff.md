# full scan の突き合わせ: `scan_v2_v3_run1` → `scan_v2_v3_run2`

再現: `python scripts/compare_scans.py evidence/scan_v2_v3_run1 evidence/scan_v2_v3_run2`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_v3_run1 | scan_v2_v3_run2 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 3065 | 3065 | +0 |
| ユニット（比較の鍵で数えたもの） | 3065 | 3065 | +0 |
| 効果 | 5369 | 5858 | +489 |
| 行 | 8854 | 9767 | +913 |
| `CONTRADICTION` の行 | 319 | 325 | +6 |
| `GAP_INJECT` の行 | 1564 | 1931 | +367 |
| `GAP_SELECT` の行 | 737 | 915 | +178 |
| `INVENTORY` の行 | 540 | 670 | +130 |
| `UNKNOWN` の行 | 7540 | 8234 | +694 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_v3_run1 | 87 |
| scan_v2_v3_run2 | 89 |
| **増えた** | **2** |
| **消えた**（回帰の疑い） | **0** |

### 増えた CONTRADICTION

- `v3-harshrathod7999-ops__taskpilot` / `list_tasks` / `DB@psycopg.Cursor.execute`
- `v3-ignatenkofi__memshelf-mcp` / `memshelf_rollup` / `FS_WRITE@pathlib.Path.unlink`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_v3_run1 | scan_v2_v3_run2 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 1575 | 1942 | +367 |
| `OP` / root なし | 6896 | 7430 | +534 |
| `OP` / root あり | 383 | 395 | +12 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 383 → 395（+12）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 101

- `v3-ignatenkofi__memshelf-mcp|mcp:memshelf_rollup:b1403382e1cd|memshelf_rollup|src/memshelf_mcp/server.py:332`: 0 → 37（+37）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_fleet:84cd4e2400ee|InkscapeMCPServer._register_portmanteau_tools.inkscape_fleet|mcp-server/src/inkscape_mcp/main.py:416`: 0 → 29（+29）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_fleet:84cd4e2400ee|InkscapeMCPServer._register_portmanteau_tools.inkscape_fleet|src/inkscape_mcp/main.py:418`: 0 → 29（+29）
- `v3-typerobot__klavis|mcp-lowlevel-v1:main.call_tool:965af40077db|main.call_tool|mcp_servers/clickup/server.py:647`: 18 → 46（+28）
- `v3-typerobot__klavis|mcp-lowlevel-v1:main.call_tool:965af40077db|main.call_tool|mcp_servers/freshdesk/server.py:1880`: 116 → 144（+28）
- `v3-ignatenkofi__memshelf-mcp|mcp:memshelf_purge:e89db8ee20f3|memshelf_purge|src/memshelf_mcp/server.py:351`: 0 → 27（+27）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_fab_art:bafaadc602dd|InkscapeMCPServer._register_portmanteau_tools.inkscape_fab_art|mcp-server/src/inkscape_mcp/main.py:468`: 0 → 26（+26）
- `v3-aslamkhan-github__lab|mcp:search_web:0f2766b6673f|search_web|AI/projects/agents/6_mcp/community_contributions/kachaje-andela-genai-bootcamp/web_search_server.py:19`: 0 → 24（+24）
- `v3-typerobot__klavis|mcp-lowlevel-v1:main.call_tool:965af40077db|main.call_tool|mcp_servers/motion/server.py:371`: 6 → 28（+22）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_fab_art:bafaadc602dd|InkscapeMCPServer._register_portmanteau_tools.inkscape_fab_art|src/inkscape_mcp/main.py:470`: 0 → 21（+21）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_sim_art:16611deeeef9|InkscapeMCPServer._register_portmanteau_tools.inkscape_sim_art|mcp-server/src/inkscape_mcp/main.py:512`: 0 → 21（+21）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_sim_art:16611deeeef9|InkscapeMCPServer._register_portmanteau_tools.inkscape_sim_art|src/inkscape_mcp/main.py:514`: 0 → 21（+21）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.llm_ops:c016d1bf9642|InkscapeMCPServer._register_portmanteau_tools.llm_ops|src/inkscape_mcp/main.py:615`: 0 → 12（+12）
- `v3-ignatenkofi__memshelf-mcp|mcp:memshelf_rebuild:e995a914ab4e|memshelf_rebuild|src/memshelf_mcp/server.py:312`: 17 → 26（+9）
- `v3-dreamrec__comfypilot|mcp:comfy_run_with_inputs:26106bbac869|comfy_run_with_inputs|src/comfy_mcp/tools/run_with_inputs.py:102`: 0 → 8（+8）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_vector:bdaa5bd070e7|InkscapeMCPServer._register_portmanteau_tools.inkscape_vector|mcp-server/src/inkscape_mcp/main.py:257`: 0 → 7（+7）
- `v3-sandraschi__inkscape-mcp|mcp:InkscapeMCPServer._register_portmanteau_tools.inkscape_vector:bdaa5bd070e7|InkscapeMCPServer._register_portmanteau_tools.inkscape_vector|src/inkscape_mcp/main.py:259`: 0 → 7（+7）
- `v3-typerobot__klavis|mcp-lowlevel-v1:main.call_tool:965af40077db|main.call_tool|mcp_servers/linear/server.py:969`: 12 → 18（+6）
- `v3-typerobot__klavis|mcp-lowlevel-v1:run_http_mode.call_tool_http:965af40077db|run_http_mode.call_tool_http|mcp_servers/msteams/server.py:290`: 16 → 22（+6）
- `v3-typerobot__klavis|mcp-lowlevel-v1:run_stdio_mode.call_tool:965af40077db|run_stdio_mode.call_tool|mcp_servers/msteams/server.py:243`: 16 → 22（+6）
