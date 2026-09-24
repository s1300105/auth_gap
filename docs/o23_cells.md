# O23 の決めが要るマス — 母集団での件数（判断材料）

再現: `python scripts/o23_cells.py evidence/scan_v2_run11`

単位は**効果の位置**（木, ユニット, site, kind, relpath, lineno）。「木」はプロジェクト数。

## #1 `readOnlyHint: true` / `destructiveHint: false` × DB（SQL の先頭語）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| D2 destructive=false × DB_READ（宣言内） | 251 | 5 | `hbg1345__teamplay-talk` / `install.form_manage` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:118 / `SELECT`<br>`hbg1345__teamplay-talk` / `install.form_manage` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:120 / `SELECT`<br>`hbg1345__teamplay-talk` / `install.form_manage` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:128 / `SELECT` |
| D2 destructive=false × データの変更（INSERT） | 88 | 5 | `hbg1345__teamplay-talk` / `install.room_manage` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 / `INSERT`<br>`hbg1345__teamplay-talk` / `register.add_task` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 / `INSERT`<br>`hbg1345__teamplay-talk` / `register.add_task` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1517 / `INSERT` |
| D1 readOnly × SQL が読めない | 67 | 4 | `letsgojh0810__godsaeng-salon` / `check_reminders` / `psycopg.Cursor.execute` / server.py:677<br>`redhat-ai-americas__memory-hub` / `list_memory` / `sqlalchemy.Connection.execute` / src/memoryhub_core/services/campaign.py:39<br>`redhat-ai-americas__memory-hub` / `list_memory` / `sqlalchemy.Connection.execute` / src/memoryhub_core/services/project.py:46 |
| D1 readOnly × DB_READ（宣言内） | 66 | 6 | `fbratten__agentspool` / `comm_get_conversation` / `psycopg.Cursor.execute` / agent_comm/spool.py:244 / `SELECT`<br>`fbratten__agentspool` / `comm_spool_stats` / `psycopg.Cursor.execute` / agent_comm/spool.py:277 / `SELECT`<br>`fbratten__agentspool` / `comm_spool_stats` / `psycopg.Cursor.execute` / agent_comm/spool.py:278 / `SELECT` |
| D2 destructive=false × SQL が読めない | 63 | 3 | `hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1472<br>`hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1603<br>`hbg1345__teamplay-talk` / `register.daily_report` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1472 |
| D2 destructive=false × データの変更（UPDATE） | 34 | 2 | `hbg1345__teamplay-talk` / `install.room_manage` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE`<br>`hbg1345__teamplay-talk` / `register.add_task` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE`<br>`hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE` |
| D2 destructive=false × 接続・トランザクション（PRAGMA） | 20 | 1 | `rwheeler007__cohort` / `cohort_compiled_discussion` / `psycopg.Cursor.execute` / cohort/sqlite_storage.py:78 / `PRAGMA`<br>`rwheeler007__cohort` / `cohort_compiled_discussion` / `psycopg.Cursor.execute` / cohort/sqlite_storage.py:79 / `PRAGMA`<br>`rwheeler007__cohort` / `cohort_create_channel` / `psycopg.Cursor.execute` / cohort/sqlite_storage.py:78 / `PRAGMA` |
| D1 readOnly × 接続・トランザクション（PRAGMA） | 16 | 3 | `fbratten__agentspool` / `comm_get_conversation` / `psycopg.Cursor.execute` / agent_comm/spool.py:42 / `PRAGMA`<br>`fbratten__agentspool` / `comm_get_conversation` / `psycopg.Cursor.execute` / agent_comm/spool.py:43 / `PRAGMA`<br>`fbratten__agentspool` / `comm_spool_stats` / `psycopg.Cursor.execute` / agent_comm/spool.py:42 / `PRAGMA` |
| D1 readOnly × データの変更（INSERT） | 6 | 1 | `hbg1345__teamplay-talk` / `register.finalize_roles` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 / `INSERT`<br>`hbg1345__teamplay-talk` / `register.get_poll_results` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 / `INSERT`<br>`hbg1345__teamplay-talk` / `register.member_tasks` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 / `INSERT` |
| D1 readOnly × データの変更（UPDATE） | 6 | 1 | `hbg1345__teamplay-talk` / `register.finalize_roles` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE`<br>`hbg1345__teamplay-talk` / `register.get_poll_results` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE`<br>`hbg1345__teamplay-talk` / `register.member_tasks` / `psycopg.Cursor.execute` / src/teamplay_talk/kakao_store.py:36 / `UPDATE` |
| D2 destructive=false × データの変更（DELETE） | 1 | 1 | `hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1611 / `DELETE` |

## #2 `readOnlyHint: true` / `destructiveHint: false` × NET（HTTP メソッド）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| D1 readOnly × メソッドが読めない | 432 | 7 | `elewa-git__odoo-mcp-server` / `odoo_check_for_update` / `urllib.request.urlopen` / src/mcp/odoo/utils/update_manager.py:71<br>`kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_d` / `urllib.request.urlopen` / linkedin_mcp_server/error_diagnostics.py:339<br>`kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_l` / `urllib.request.urlopen` / linkedin_mcp_server/error_diagnostics.py:339 |
| D1 readOnly × 読み系 | 51 | 11 | `elewa-git__odoo-mcp-server` / `odoo_fields_get` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get`<br>`elewa-git__odoo-mcp-server` / `odoo_ping` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get`<br>`elewa-git__odoo-mcp-server` / `odoo_read_records` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get` |
| D2 destructive=false × メソッドが読めない | 47 | 5 | `dddoh__paper-access-mcp` / `download_paper_from_link_tool` / `urllib.request.urlopen` / packages/paper-access-mcp/src/paper_access_mcp/providers/informs/pdf_request.py:25<br>`hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `httpx.AsyncClient.request` / src/teamplay_talk/kakao_calendar.py:338<br>`nan-fe__agents` / `create_mcp.notify_review_passed` / `httpx.AsyncClient.request` / mcp-lark/lark_im/client.py:129 |
| D2 destructive=false × 書き込み系 POST | 40 | 9 | `elewa-git__odoo-mcp-server` / `odoo_log_internal_note` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post`<br>`elewa-git__odoo-mcp-server` / `odoo_schedule_activity` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post`<br>`elewa-git__odoo-mcp-server` / `odoo_setup_credentials` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post` |
| D2 destructive=false × 読み系 | 33 | 5 | `elewa-git__odoo-mcp-server` / `odoo_log_internal_note` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get`<br>`elewa-git__odoo-mcp-server` / `odoo_schedule_activity` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get`<br>`elewa-git__odoo-mcp-server` / `odoo_setup_credentials` / `httpx.AsyncClient.get` / src/mcp/odoo/connection/json2_transport.py:66 / `get` |
| D1 readOnly × 書き込み系 POST | 25 | 6 | `elewa-git__odoo-mcp-server` / `odoo_fields_get` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post`<br>`elewa-git__odoo-mcp-server` / `odoo_ping` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post`<br>`elewa-git__odoo-mcp-server` / `odoo_read_records` / `httpx.AsyncClient.post` / src/mcp/odoo/connection/json2_transport.py:98 / `post` |

## #3 `destructiveHint: false` × FS_WRITE（mode 不明）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| 該当なし | 0 | 0 | — |

## #4 `openWorldHint: false` × NET（宛先）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| 読めない | 91 | 7 | `khairu-aqsara__code-rag` / `coderag_find_symbols` / `httpx.AsyncClient.post` / mcp/server.py:82<br>`khairu-aqsara__code-rag` / `coderag_get_default_project` / `httpx.AsyncClient.get` / mcp/server.py:96<br>`khairu-aqsara__code-rag` / `coderag_get_health` / `httpx.AsyncClient.get` / mcp/server.py:96 |
| 外部 | 38 | 4 | `hbg1345__teamplay-talk` / `install.room_manage` / `httpx.AsyncClient.get` / src/teamplay_talk/kakao.py:81<br>`hbg1345__teamplay-talk` / `register.add_task` / `httpx.AsyncClient.get` / src/teamplay_talk/kakao.py:81<br>`hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `httpx.AsyncClient.get` / src/teamplay_talk/kakao.py:81 |

## #5 `idempotentHint: true` × 非冪等の証拠

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| NET POST | 36 | 7 | `hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `httpx.AsyncClient.post` / src/teamplay_talk/kakao.py:74<br>`hbg1345__teamplay-talk` / `register.calendar_update_event` / `httpx.AsyncClient.post` / src/teamplay_talk/kakao_calendar.py:174<br>`hbg1345__teamplay-talk` / `register.daily_report` / `httpx.AsyncClient.post` / src/teamplay_talk/kakao.py:74 |
| INSERT（衝突時の指定なし） | 23 | 2 | `hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153<br>`hbg1345__teamplay-talk` / `register.close_poll` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153<br>`hbg1345__teamplay-talk` / `register.daily_report` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1153 |
| INSERT（ON CONFLICT / OR REPLACE あり） | 6 | 2 | `hbg1345__teamplay-talk` / `register.daily_report` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:1054<br>`hbg1345__teamplay-talk` / `register.join_room` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:103<br>`hbg1345__teamplay-talk` / `register.restore_room` / `psycopg.Cursor.execute` / src/teamplay_talk/storage.py:953 |

## #6 `readOnlyHint: true` / `destructiveHint: false` × SPAWN（**現行は全件 CONTRADICTION**）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| D1 readOnly × SPAWN_CONST_ARGV | 10 | 2 | `dddabtc__winremote-mcp` / `AnnotatedSnapshot` / `subprocess.run` / src/winremote/__main__.py:629 / `query`<br>`dddabtc__winremote-mcp` / `AnnotatedSnapshot` / `subprocess.run` / src/winremote/__main__.py:674 / `tscon`<br>`dddabtc__winremote-mcp` / `EventLog` / `subprocess.run` / src/winremote/services.py:10 / `powershell` |
| D2 destructive=false × SPAWN_CONST_ARGV | 6 | 3 | `dddabtc__winremote-mcp` / `App` / `subprocess.run` / src/winremote/desktop.py:258 / `powershell`<br>`dddabtc__winremote-mcp` / `Notification` / `subprocess.run` / src/winremote/desktop.py:357 / `powershell`<br>`dddabtc__winremote-mcp` / `PlaySound` / `subprocess.run` / src/winremote/__main__.py:827 / `powershell` |
| D1 readOnly × SPAWN_MODEL_ARGV | 5 | 1 | `fanfan-de__anybox` / `register.get_blendfile_summary_datablocks_for_cli` / `subprocess.run` / plugins/Anybox-Plugins/blender/runtime/blender-mcp/blmcp/tools_helpers/blender_cli.py:69 / `（argv0 が読めない）`<br>`fanfan-de__anybox` / `register.get_blendfile_summary_missing_files_for_c` / `subprocess.run` / plugins/Anybox-Plugins/blender/runtime/blender-mcp/blmcp/tools_helpers/blender_cli.py:69 / `（argv0 が読めない）`<br>`fanfan-de__anybox` / `register.get_blendfile_summary_of_linked_libraries` / `subprocess.run` / plugins/Anybox-Plugins/blender/runtime/blender-mcp/blmcp/tools_helpers/blender_cli.py:69 / `（argv0 が読めない）` |

argv0（定数に解決できたもの）: `powershell` 8, `（argv0 が読めない）` 5, `query` 2, `tscon` 2, `ping` 2, `nvidia-smi` 2

## #7 `destructiveHint: false` × FS_WRITE の上書き型（**現行は全件 CONTRADICTION**）

| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |
|---|---|---|---|
| pathlib.Path.write_text | 24 | 4 | `berkay2002__yt-scribe` / `create_mcp_server.agent_fetch_and_polish_youtube_t` / `pathlib.Path.write_text` / src/yt_scribe/file_io.py:13<br>`fbratten__agentspool` / `comm_relay_gen_secret` / `pathlib.Path.write_text` / agent_comm/relay/auth.py:32<br>`gwicho38__write-like-me-mcp` / `analyze_writing_style` / `pathlib.Path.write_text` / src/write_like_me_mcp/model.py:119 |
| shutil.rmtree | 8 | 3 | `artyomzemlyak__tg-note` / `convert_document_from_content` / `shutil.rmtree` / docker/docling-mcp/app/tg_docling/model_sync.py:515<br>`artyomzemlyak__tg-note` / `convert_document_from_content` / `shutil.rmtree` / docker/docling-mcp/app/tg_docling/model_sync.py:586<br>`artyomzemlyak__tg-note` / `sync_docling_models` / `shutil.rmtree` / docker/docling-mcp/app/tg_docling/model_sync.py:256 |
| pathlib.Path.write_bytes | 5 | 2 | `dddoh__paper-access-mcp` / `download_paper_from_link_tool` / `pathlib.Path.write_bytes` / packages/paper-access-mcp/src/paper_access_mcp/core.py:56<br>`dddoh__paper-access-mcp` / `download_paper_from_link_tool` / `pathlib.Path.write_bytes` / packages/paper-access-mcp/src/paper_access_mcp/providers/informs/pdf_request.py:34<br>`dddoh__paper-access-mcp` / `download_paper_from_link_tool` / `pathlib.Path.write_bytes` / packages/paper-access-mcp/src/paper_access_mcp/providers/wiley/chrome_extension.py:183 |
| builtins.open | 4 | 3 | `dddabtc__winremote-mcp` / `PlaySound` / `builtins.open` / src/winremote/__main__.py:798<br>`diterex__youtube-research-mcp` / `get_video_frames` / `builtins.open` / src/yt_research_mcp/server.py:998<br>`dondetir__codegrok_mcp` / `learn` / `builtins.open` / src/codegrok_mcp/indexing/source_retriever.py:628 |
| os.unlink | 3 | 2 | `dddabtc__winremote-mcp` / `PlaySound` / `os.unlink` / src/winremote/__main__.py:855<br>`fbratten__agentspool` / `comm_heartbeat` / `os.unlink` / agent_comm/registry.py:115<br>`fbratten__agentspool` / `comm_register_agent` / `os.unlink` / agent_comm/registry.py:115 |
| os.replace | 2 | 1 | `fbratten__agentspool` / `comm_heartbeat` / `os.replace` / agent_comm/registry.py:112<br>`fbratten__agentspool` / `comm_register_agent` / `os.replace` / agent_comm/registry.py:112 |
| os.chmod | 2 | 1 | `innovatehubph__innovatehub-ai-platform` / `send_message` / `os.chmod` / python/helpers/files.py:326<br>`innovatehubph__innovatehub-ai-platform` / `send_message` / `os.chmod` / python/helpers/files.py:329 |
| os.remove | 1 | 1 | `diterex__youtube-research-mcp` / `get_video_frames` / `os.remove` / src/yt_research_mcp/server.py:858 |
| pathlib.Path.open | 1 | 1 | `ritikakumar0204__audience-trend-miner` / `run_audience_mining` / `pathlib.Path.open` / storage/run_lock.py:26 |

