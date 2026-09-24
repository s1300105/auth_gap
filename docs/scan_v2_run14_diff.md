# full scan の突き合わせ: `scan_v2_run13` → `scan_v2_run14`

再現: `python scripts/compare_scans.py evidence/scan_v2_run13 evidence/scan_v2_run14`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run13 | scan_v2_run14 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 11500 | 10193 | -1307 |
| 行 | 16406 | 15311 | -1095 |
| `CONTRADICTION` の行 | 1361 | 1299 | -62 |
| `GAP_INJECT` の行 | 2760 | 2810 | +50 |
| `GAP_SELECT` の行 | 522 | 522 | +0 |
| `UNKNOWN` の行 | 13274 | 12156 | -1118 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run13 | 220 |
| scan_v2_run14 | 191 |
| **増えた** | **0** |
| **消えた**（回帰の疑い） | **29** |

### 消えた CONTRADICTION — **1 件ずつ理由を確かめること**

- `v2-dddoh__paper-access-mcp` / `download_paper_from_link_tool` / `FS_WRITE@pathlib.Path.write_bytes`
- `v2-diterex__youtube-research-mcp` / `get_video_frames` / `FS_WRITE@builtins.open`
- `v2-dondetir__codegrok_mcp` / `learn` / `FS_WRITE@builtins.open`
- `v2-khairu-aqsara__code-rag` / `coderag_get_default_project` / `NET@httpx.AsyncClient.get`
- `v2-khairu-aqsara__code-rag` / `coderag_get_project_info` / `NET@httpx.AsyncClient.get`
- `v2-peterhollens__dejavu` / `dejavu_reindex` / `NET@httpx.AsyncClient.get`
- `v2-peterhollens__dejavu` / `dejavu_reindex` / `NET@httpx.AsyncClient.post`
- `v2-peterhollens__dejavu` / `dejavu_search` / `NET@httpx.AsyncClient.get`
- `v2-peterhollens__dejavu` / `dejavu_search` / `NET@httpx.AsyncClient.post`
- `v2-redhat-ai-americas__memory-hub` / `manage_project` / `DB@sqlalchemy.Connection.execute`
- `v2-redhat-ai-americas__memory-hub` / `memory` / `DB@sqlalchemy.Connection.execute`
- `v2-rwheeler007__cohort` / `cohort_create_agent` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `NET@urllib.request.urlopen`
- `v2-rwheeler007__cohort` / `cohort_meeting_demote` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_meeting_promote` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_requeue_item` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_submit_for_review` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `local_llm_generate` / `NET@urllib.request.urlopen`
- `v2-sontanon__docx-mcp` / `apply_changes` / `FS_WRITE@pathlib.Path.write_bytes`
- `v2-sontanon__docx-mcp` / `apply_changes_from_file` / `FS_WRITE@pathlib.Path.write_bytes`
- `v2-xorbitsai__xagent` / `deputy_create_resource` / `DB@sqlalchemy.Connection.execute`
- `v2-xorbitsai__xagent` / `deputy_update_resource` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_delete_list_item` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_update_list_item` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_upload_file` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_upload_text_file` / `FS_WRITE@pathlib.Path.open`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_get_item` / `NET@httpx.AsyncClient.get`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_get_location_map` / `NET@httpx.AsyncClient.get`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_list_location_items` / `NET@httpx.AsyncClient.get`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run13 | scan_v2_run14 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 4196 | 4291 | +95 |
| `OP` / root なし | 12171 | 10979 | -1192 |
| `OP` / root あり | 39 | 41 | +2 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 39 → 41（+2）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 357

- `v2-moon201595__agent|mcp:dedupe_and_rank_papers:aa18a8669ea4|dedupe_and_rank_papers|server.py:794`: 0 → 34（+34）
- `v2-redhat-ai-americas__memory-hub|mcp:memory:8613685544bf|memory|memory-hub-mcp/src/tools/memory.py:116`: 125 → 157（+32）
- `v2-redhat-ai-americas__memory-hub|mcp:search_memory:bdc7af814629|search_memory|memory-hub-mcp/src/tools/search_memory.py:464`: 6 → 33（+27）
- `v2-8dionysus__abyss-stack|mcp:build_server.kag_read:2716ea7ece3d|build_server.kag_read|mcp/services/aoa-kag-mcp/src/aoa_kag_mcp/server.py:131`: 0 → 24（+24）
- `v2-moon201595__agent|mcp:s2_search_papers:c3930e32072a|s2_search_papers|server.py:605`: 0 → 15（+15）
- `v2-xorbitsai__xagent|mcp:slack_join_channel:065969e108b6|slack_join_channel|src/xagent/web/tools/mcp/slack.py:457`: 12 → 0（-12）
- `v2-xorbitsai__xagent|mcp:whatsapp_send_media_message:eec3edc000da|whatsapp_send_media_message|src/xagent/web/tools/mcp/whatsapp.py:675`: 12 → 0（-12）
- `v2-xorbitsai__xagent|mcp:whatsapp_send_template_message:9bc136087a57|whatsapp_send_template_message|src/xagent/web/tools/mcp/whatsapp.py:604`: 12 → 0（-12）
- `v2-xorbitsai__xagent|mcp:whatsapp_send_text_message:7a0b7258512e|whatsapp_send_text_message|src/xagent/web/tools/mcp/whatsapp.py:553`: 12 → 0（-12）
- `v2-moon201595__agent|mcp:hybrid_search_local_papers:4d57e3972468|hybrid_search_local_papers|server.py:722`: 11 → 20（+9）
- `v2-xorbitsai__xagent|mcp:facebook_auth_status:d36d5fd42096|facebook_auth_status|src/xagent/web/tools/mcp/facebook.py:91`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:facebook_list_page_posts:fcadd0a5bca4|facebook_list_page_posts|src/xagent/web/tools/mcp/facebook.py:126`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:facebook_list_pages:d36d5fd42096|facebook_list_pages|src/xagent/web/tools/mcp/facebook.py:112`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:facebook_list_post_comments:972ef063d293|facebook_list_post_comments|src/xagent/web/tools/mcp/facebook.py:175`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:facebook_publish_image_post:136f8564f78e|facebook_publish_image_post|src/xagent/web/tools/mcp/facebook.py:232`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:facebook_publish_text_post:d4b9b67ddf8d|facebook_publish_text_post|src/xagent/web/tools/mcp/facebook.py:210`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:gmail_search_messages:d0f7574023c9|gmail_search_messages|src/xagent/web/tools/mcp/gmail.py:155`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:google_drive_download_file:f77b5f6f9834|google_drive_download_file|src/xagent/web/tools/mcp/google_drive.py:1200`: 10 → 2（-8）
- `v2-xorbitsai__xagent|mcp:google_drive_get_file_content:fb5394515552|google_drive_get_file_content|src/xagent/web/tools/mcp/google_drive.py:1047`: 8 → 0（-8）
- `v2-xorbitsai__xagent|mcp:google_drive_list_permissions:184b51736134|google_drive_list_permissions|src/xagent/web/tools/mcp/google_drive.py:1717`: 8 → 0（-8）
