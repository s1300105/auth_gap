# full scan の突き合わせ: `scan_v2_run20` → `scan_v2_run23`

再現: `python scripts/compare_scans.py evidence/scan_v2_run20 evidence/scan_v2_run23`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run20 | scan_v2_run23 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2289 | +58 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2289 | +58 |
| 効果（生の行数） | 8337 | 9423 | +1086 |
| 効果（一意の行数。バイト同一の複製を 1 本に） | 4461 | 4708 | +247 |
| 行 | 16268 | 17381 | +1113 |
| `CONTRADICTION` の行 | 1281 | 1284 | +3 |
| `GAP_INJECT` の行 | 2331 | 2512 | +181 |
| `GAP_SELECT` の行 | 496 | 495 | -1 |
| `INVENTORY` の行 | 0 | 1 | +1 |
| `UNKNOWN` の行 | 14153 | 15619 | +1466 |

## CONTRADICTION（ユニット × site × kind × 宣言。D1〜D4 は 4 つとも主指標、D62）

| | 計 | D1 | D2 | D3 |
|---|---|---|---|---|
| scan_v2_run20 | 192 | 109 | 44 | 39 |
| scan_v2_run23 | 194 | 110 | 45 | 39 |
| **増えた** | 2 | 1 | 1 | 0 |
| **消えた**（回帰の疑い） | 0 | 0 | 0 | 0 |

### 増えた CONTRADICTION

- `v2-gwicho38__write-like-me-mcp` / `analyze_writing_style`（src/write_like_me_mcp/server.py:584）/ `DB@psycopg.Cursor.execute` / D2
- `v2-vishalsachdev__canvas-mcp` / `register_shared_file_tools.download_course_file`（src/canvas_mcp/tools/files.py:46）/ `FS_WRITE@os.unlink` / D1

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run20 | scan_v2_run23 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 2928 | 3109 | +181 |
| `OP` / root なし | 13297 | 14123 | +826 |
| `OP` / root あり | 43 | 149 | +106 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 43 → 149（+106）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 58。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。

- 増えた: `v2-8dionysus__abyss-stack|mcp:_exercise.stale_probe:d36d5fd42096|_exercise.stale_probe|mcp/protocol-lab/scripts/run_kag_cache_pair.py:221`（_exercise.stale_probe）
- 増えた: `v2-8dionysus__abyss-stack|mcp:_exercise.transient_probe:d36d5fd42096|_exercise.transient_probe|mcp/protocol-lab/scripts/run_kag_cache_pair.py:218`（_exercise.transient_probe）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_add:d2631a660bc5|cart_add|src/auto_grocer_mcp/tools/cart.py:121`（cart_add）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_add_many:1782120f4a43|cart_add_many|src/auto_grocer_mcp/tools/cart.py:552`（cart_add_many）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_add_with_retry:4c0ab3055c81|cart_add_with_retry|src/auto_grocer_mcp/tools/cart.py:454`（cart_add_with_retry）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_check_auth:d36d5fd42096|cart_check_auth|src/auto_grocer_mcp/tools/cart.py:111`（cart_check_auth）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_get:d36d5fd42096|cart_get|src/auto_grocer_mcp/tools/cart.py:386`（cart_get）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:cart_remove:78987d06efee|cart_remove|src/auto_grocer_mcp/tools/cart.py:288`（cart_remove）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:coupon_categories:d36d5fd42096|coupon_categories|src/auto_grocer_mcp/tools/coupon.py:221`（coupon_categories）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:coupon_clip:c4a97d26c147|coupon_clip|src/auto_grocer_mcp/tools/coupon.py:265`（coupon_clip）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:coupon_clipped:5b929c25903c|coupon_clipped|src/auto_grocer_mcp/tools/coupon.py:331`（coupon_clipped）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:coupon_list:9f7414366e45|coupon_list|src/auto_grocer_mcp/tools/coupon.py:69`（coupon_list）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:coupon_search:2c8d3244d6f6|coupon_search|src/auto_grocer_mcp/tools/coupon.py:149`（coupon_search）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:find_substitute:0dbc0e8844a0|find_substitute|src/auto_grocer_mcp/tools/substitution.py:111`（find_substitute）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:health_live:d36d5fd42096|health_live|src/auto_grocer_mcp/observability/health.py:22`（health_live）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:health_ready:d36d5fd42096|health_ready|src/auto_grocer_mcp/observability/health.py:30`（health_ready）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:product_get:296eecf21005|product_get|src/auto_grocer_mcp/tools/product.py:321`（product_get）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:product_search:2fd346809393|product_search|src/auto_grocer_mcp/tools/product.py:28`（product_search）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:product_search_batch:ab943538e382|product_search_batch|src/auto_grocer_mcp/tools/product.py:198`（product_search_batch）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_clear:d36d5fd42096|session_clear|src/auto_grocer_mcp/tools/session.py:241`（session_clear）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_clear_credentials:d36d5fd42096|session_clear_credentials|src/auto_grocer_mcp/tools/session.py:353`（session_clear_credentials）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_refresh:17303eb6a20e|session_refresh|src/auto_grocer_mcp/tools/session.py:101`（session_refresh）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_save_credentials:614ea370b20d|session_save_credentials|src/auto_grocer_mcp/tools/session.py:274`（session_save_credentials）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_save_instructions:d36d5fd42096|session_save_instructions|src/auto_grocer_mcp/tools/session.py:213`（session_save_instructions）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:session_status:d36d5fd42096|session_status|src/auto_grocer_mcp/tools/session.py:23`（session_status）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:store_change:1da5a8c565dc|store_change|src/auto_grocer_mcp/tools/store.py:148`（store_change）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:store_get_default:d36d5fd42096|store_get_default|src/auto_grocer_mcp/tools/store.py:84`（store_get_default）
- 増えた: `v2-benjaminwalkerbond__auto_grocer|mcp:store_search:53179c4733b5|store_search|src/auto_grocer_mcp/tools/store.py:20`（store_search）
- 増えた: `v2-crystaldba__postgres-mcp|mcp:execute_sql:2456b619ddbd|execute_sql|src/postgres_mcp/server.py:415`（execute_sql）
- 増えた: `v2-pdwhoward__llmacro-dynare-lsp|mcp:build_server._tool._decorator._wrapped:d36d5fd42096|build_server._tool._decorator._wrapped|dynare_lsp/mcp_server.py:308`（build_server._tool._decorator._wrapped）
- 増えた: `v2-pdwhoward__llmacro-dynare-lsp|mcp:dynare_preflight:98e8af0ae514|dynare_preflight|dynare_lsp/mcp_preflight_server.py:62`（dynare_preflight）
- 増えた: `v2-redhat-ai-americas__memory-hub|mcp:admin_memory:600922f86c39|admin_memory|memoryhub-local/src/memoryhub_local/tools/admin_memory.py:23`（admin_memory）
- 増えた: `v2-redhat-ai-americas__memory-hub|mcp:memory:a40760204c50|memory|memoryhub-local/src/memoryhub_local/tools/memory.py:40`（memory）
- 増えた: `v2-redhat-ai-americas__memory-hub|mcp:register_session:767bba57f070|register_session|memoryhub-local/src/memoryhub_local/tools/register_session.py:18`（register_session）
- 増えた: `v2-redhat-ai-americas__memory-hub|mcp:thread:62fce5c9cfb2|thread|memoryhub-local/src/memoryhub_local/tools/thread.py:30`（thread）
- 増えた: `v2-rootport-ai__nz-videomni|mcp:backend_status:d36d5fd42096|backend_status|mcp_server/tools/system.py:22`（backend_status）
- 増えた: `v2-rootport-ai__nz-videomni|mcp:cancel_job:28aebd3a7a1d|cancel_job|mcp_server/tools/jobs.py:148`（cancel_job）
- 増えた: `v2-rootport-ai__nz-videomni|mcp:delete_job:28aebd3a7a1d|delete_job|mcp_server/tools/jobs.py:183`（delete_job）
- 増えた: `v2-rootport-ai__nz-videomni|mcp:get_config:d36d5fd42096|get_config|mcp_server/tools/system.py:57`（get_config）
- 増えた: `v2-rootport-ai__nz-videomni|mcp:get_job_video_path:28aebd3a7a1d|get_job_video_path|mcp_server/tools/outputs.py:38`（get_job_video_path）

## 効果数が変わったユニット（上位 20）

変わったユニット: 4

- `v2-gwicho38__write-like-me-mcp|mcp:analyze_writing_style:3b7450831cc3|analyze_writing_style|src/write_like_me_mcp/server.py:584`: 2 → 12（+10）
- `v2-moon201595__agent|mcp:fetch_paper:829194cc7869|fetch_paper|server.py:817`: 2 → 4（+2）
- `v2-gwicho38__write-like-me-mcp|mcp:find_writing_examples:e32745f44ce8|find_writing_examples|src/write_like_me_mcp/server.py:786`: 0 → 1（+1）
- `v2-moon201595__agent|mcp:save_summary:4406086671fb|save_summary|server.py:1288`: 3 → 4（+1）
