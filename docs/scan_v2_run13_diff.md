# full scan の突き合わせ: `scan_v2_run12` → `scan_v2_run13`

再現: `python scripts/compare_scans.py evidence/scan_v2_run12 evidence/scan_v2_run13`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run12 | scan_v2_run13 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 11500 | 11500 | +0 |
| 行 | 16406 | 16406 | +0 |
| `CONTRADICTION` の行 | 1217 | 1361 | +144 |
| `GAP_INJECT` の行 | 2760 | 2760 | +0 |
| `GAP_SELECT` の行 | 522 | 522 | +0 |
| `UNKNOWN` の行 | 13274 | 13274 | +0 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run12 | 178 |
| scan_v2_run13 | 220 |
| **増えた** | **80** |
| **消えた**（回帰の疑い） | **38** |

### 消えた CONTRADICTION — **1 件ずつ理由を確かめること**

- `v2-berkay2002__yt-scribe` / `create_mcp_server.agent_fetch_and_polish_youtube_tool` / `FS_WRITE@pathlib.Path.write_text`
- `v2-dddabtc__winremote-mcp` / `AnnotatedSnapshot` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `App` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `EventLog` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `Notification` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `OCR` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `Ping` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `PlaySound` / `FS_WRITE@builtins.open`
- `v2-dddabtc__winremote-mcp` / `PlaySound` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `ServiceList` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `Snapshot` / `SPAWN@subprocess.run`
- `v2-dddabtc__winremote-mcp` / `TaskList` / `SPAWN@subprocess.run`
- `v2-dondetir__codegrok_mcp` / `remember` / `FS_WRITE@builtins.open`
- `v2-fanfan-de__anybox` / `register.get_blendfile_summary_datablocks_for_cli` / `SPAWN@subprocess.run`
- `v2-fanfan-de__anybox` / `register.get_blendfile_summary_missing_files_for_cli` / `SPAWN@subprocess.run`
- `v2-fanfan-de__anybox` / `register.get_blendfile_summary_of_linked_libraries_for_cli` / `SPAWN@subprocess.run`
- `v2-fanfan-de__anybox` / `register.get_blendfile_summary_path_info_for_cli` / `SPAWN@subprocess.run`
- `v2-fanfan-de__anybox` / `register.get_blendfile_summary_usage_guess_for_cli` / `SPAWN@subprocess.run`
- `v2-fbratten__agentspool` / `comm_relay_gen_secret` / `FS_WRITE@pathlib.Path.write_text`
- `v2-gwicho38__write-like-me-mcp` / `analyze_writing_style` / `FS_WRITE@pathlib.Path.write_text`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_connection_tools.connect_to_robot` / `SPAWN@subprocess.run`
- `v2-ritikakumar0204__audience-trend-miner` / `run_audience_mining` / `FS_WRITE@pathlib.Path.open`
- `v2-rwheeler007__cohort` / `browser_action` / `SPAWN@subprocess.run`
- `v2-rwheeler007__cohort` / `cohort_assign_task` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_claim_next` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_compiled_discussion` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_complete_item` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_create_channel` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_discussion` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_enqueue_item` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_error` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_meeting_start` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_post` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_respond` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `condense_channel` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `local_llm_generate` / `SPAWN@subprocess.run`
- `v2-rwheeler007__cohort` / `post_message` / `FS_WRITE@pathlib.Path.write_text`

### 増えた CONTRADICTION

- `v2-fbratten__agentspool` / `comm_get_conversation` / `DB@psycopg.Cursor.execute`
- `v2-fbratten__agentspool` / `comm_spool_stats` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `install.room_manage` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.add_task` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `NET@httpx.AsyncClient.post`
- `v2-hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `NET@httpx.AsyncClient.request`
- `v2-hbg1345__teamplay-talk` / `register.assign_roles` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.build_roadmap` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.close_poll` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.create_daily_checkin` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.create_poll` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.create_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.decompose_roadmap` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.delete_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.delete_task` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.finalize_roles` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.gather_locations` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.gather_opinions` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.gather_task_opinions` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.get_poll_results` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.join_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.join_room` / `NET@httpx.AsyncClient.post`
- `v2-hbg1345__teamplay-talk` / `register.leave_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.member_tasks` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.restore_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.room_dashboard` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.rooms` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.schedule_meeting` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.schedule_roadmap` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.switch_room` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.update_task` / `NET@httpx.AsyncClient.get`
- `v2-hbg1345__teamplay-talk` / `register.view_roadmap` / `NET@httpx.AsyncClient.get`
- `v2-khairu-aqsara__code-rag` / `coderag_get_default_project` / `NET@httpx.AsyncClient.get`
- `v2-khairu-aqsara__code-rag` / `coderag_get_project_info` / `NET@httpx.AsyncClient.get`
- `v2-khairu-aqsara__code-rag` / `coderag_list_files` / `NET@httpx.AsyncClient.get`
- `v2-letsgojh0810__godsaeng-salon` / `check_reminders` / `DB@psycopg.Cursor.execute`
- `v2-nan-fe__agents` / `create_mcp.list_chat_messages` / `NET@httpx.AsyncClient.post`
- `v2-nan-fe__agents` / `create_mcp.list_chat_messages` / `NET@httpx.AsyncClient.request`
- `v2-nan-fe__agents` / `create_mcp.reply_message` / `NET@httpx.AsyncClient.post`
- `v2-nan-fe__agents` / `create_mcp.reply_message` / `NET@httpx.AsyncClient.request`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_capacitor_crossref` / `DB@psycopg.Cursor.execute`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_code_lookup` / `DB@psycopg.Cursor.execute`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_diagnostic_symptom_tree` / `DB@psycopg.Cursor.execute`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_fault_code_lookup` / `DB@psycopg.Cursor.execute`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_refrigerant_charge_check` / `DB@psycopg.Cursor.execute`
- `v2-nightfast-app__hvac-mcp` / `register.hvac_refrigerant_pt_lookup` / `DB@psycopg.Cursor.execute`
- `v2-peterhollens__dejavu` / `dejavu_reindex` / `NET@httpx.AsyncClient.get`
- `v2-peterhollens__dejavu` / `dejavu_reindex` / `NET@httpx.AsyncClient.post`
- `v2-peterhollens__dejavu` / `dejavu_search` / `NET@httpx.AsyncClient.get`
- `v2-peterhollens__dejavu` / `dejavu_search` / `NET@httpx.AsyncClient.post`
- `v2-redhat-ai-americas__memory-hub` / `manage_project` / `DB@sqlalchemy.Connection.execute`
- `v2-redhat-ai-americas__memory-hub` / `memory` / `DB@sqlalchemy.Connection.execute`
- `v2-rwheeler007__cohort` / `channel_summary` / `DB@psycopg.Cursor.execute`
- `v2-rwheeler007__cohort` / `cohort_complete_item` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_error` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `NET@urllib.request.urlopen`
- `v2-rwheeler007__cohort` / `cohort_get_mentions` / `DB@psycopg.Cursor.execute`
- `v2-rwheeler007__cohort` / `cohort_meeting_demote` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_meeting_disable` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_meeting_promote` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_meeting_remove_participant` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_requeue_item` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_respond` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_set_deliverables` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_submit_for_review` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `cohort_submit_review` / `NET@httpx.AsyncClient.request`
- `v2-rwheeler007__cohort` / `local_llm_generate` / `NET@urllib.request.urlopen`
- `v2-rwheeler007__cohort` / `read_channel` / `DB@psycopg.Cursor.execute`
- `v2-xorbitsai__xagent` / `deputy_create_resource` / `DB@sqlalchemy.Connection.execute`
- `v2-xorbitsai__xagent` / `deputy_update_resource` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_delete_list_item` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_update_list_item` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_upload_file` / `FS_WRITE@pathlib.Path.open`
- `v2-xorbitsai__xagent` / `sharepoint_upload_text_file` / `FS_WRITE@pathlib.Path.open`
- `v2-zelladir__asquared-mcp` / `build_mcp.coord_post` / `NET@httpx.AsyncClient.post`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_get_item` / `NET@httpx.AsyncClient.get`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_get_location_map` / `NET@httpx.AsyncClient.get`
- `v2-zelladir__asquared-mcp` / `register_inventory_tools.inventory_list_location_items` / `NET@httpx.AsyncClient.get`
- `v2-zomma-dev__quantcontext-mcp-server` / `factor_analysis` / `NET@urllib.request.urlopen`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run12 | scan_v2_run13 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 4196 | 4196 | +0 |
| `OP` / root なし | 12171 | 12171 | +0 |
| `OP` / root あり | 39 | 39 | +0 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 39 → 39（+0）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 0

