# full scan の突き合わせ: `scan_v2_run18` → `scan_v2_run20`

再現: `python scripts/compare_scans.py evidence/scan_v2_run18 evidence/scan_v2_run20`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run18 | scan_v2_run20 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 8254 | 8337 | +83 |
| 行 | 16109 | 16268 | +159 |
| `CONTRADICTION` の行 | 1279 | 1281 | +2 |
| `GAP_INJECT` の行 | 2290 | 2331 | +41 |
| `GAP_SELECT` の行 | 496 | 496 | +0 |
| `UNKNOWN` の行 | 14066 | 14153 | +87 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run18 | 189 |
| scan_v2_run20 | 191 |
| **増えた** | **2** |
| **消えた**（回帰の疑い） | **0** |

### 増えた CONTRADICTION

- `v2-jsyzlbw__bbwatch` / `list_courses` / `FS_WRITE@os.chmod`
- `v2-jsyzlbw__bbwatch` / `list_courses` / `FS_WRITE@os.replace`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run18 | scan_v2_run20 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 2887 | 2928 | +41 |
| `OP` / root なし | 13179 | 13297 | +118 |
| `OP` / root あり | 43 | 43 | +0 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 43 → 43（+0）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 32

- `v2-jsyzlbw__bbwatch|mcp:download_course:ebe0cd7e63e4|download_course|src/bbwatch/mcp_server.py:142`: 9 → 20（+11）
- `v2-redhat-ai-americas__memory-hub|mcp:thread:0f3a4e143afb|thread|memory-hub-mcp/src/tools/thread.py:60`: 13 → 23（+10）
- `v2-redhat-ai-americas__memory-hub|mcp:manage_graph:1d8deef2d07f|manage_graph|memory-hub-mcp/src/tools/manage_graph.py:69`: 13 → 21（+8）
- `v2-redhat-ai-americas__memory-hub|mcp:memory:8613685544bf|memory|memory-hub-mcp/src/tools/memory.py:116`: 131 → 139（+8）
- `v2-vishalsachdev__canvas-mcp|mcp:register_enrollment_tools.check_enrollment:94254c877c1c|register_enrollment_tools.check_enrollment|src/canvas_mcp/tools/enrollment.py:31`: 0 → 8（+8）
- `v2-jsyzlbw__bbwatch|mcp:list_courses:d36d5fd42096|list_courses|src/bbwatch/mcp_server.py:129`: 0 → 3（+3）
- `v2-jsyzlbw__bbwatch|mcp:scan_now:d36d5fd42096|scan_now|src/bbwatch/mcp_server.py:110`: 3 → 6（+3）
- `v2-xorbitsai__xagent|mcp:facebook_list_page_posts:fcadd0a5bca4|facebook_list_page_posts|src/xagent/web/tools/mcp/facebook.py:126`: 0 → 3（+3）
- `v2-rwheeler007__cohort|mcp:cohort_compiled_discussion:e3082790faba|cohort_compiled_discussion|cohort/mcp/server.py:1950`: 69 → 71（+2）
- `v2-xorbitsai__xagent|mcp:facebook_list_post_comments:972ef063d293|facebook_list_post_comments|src/xagent/web/tools/mcp/facebook.py:175`: 0 → 2（+2）
- `v2-xorbitsai__xagent|mcp:facebook_publish_image_post:136f8564f78e|facebook_publish_image_post|src/xagent/web/tools/mcp/facebook.py:232`: 0 → 2（+2）
- `v2-xorbitsai__xagent|mcp:facebook_publish_text_post:d4b9b67ddf8d|facebook_publish_text_post|src/xagent/web/tools/mcp/facebook.py:210`: 0 → 2（+2）
- `v2-xorbitsai__xagent|mcp:instagram_publish_image:10b7b77b5ab5|instagram_publish_image|src/xagent/web/tools/mcp/instagram.py:175`: 0 → 2（+2）
- `v2-xorbitsai__xagent|mcp:facebook_auth_status:d36d5fd42096|facebook_auth_status|src/xagent/web/tools/mcp/facebook.py:91`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:facebook_list_pages:d36d5fd42096|facebook_list_pages|src/xagent/web/tools/mcp/facebook.py:112`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:instagram_auth_status:d36d5fd42096|instagram_auth_status|src/xagent/web/tools/mcp/instagram.py:94`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:instagram_get_profile:c79d7d763617|instagram_get_profile|src/xagent/web/tools/mcp/instagram.py:128`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:instagram_list_linked_accounts:d36d5fd42096|instagram_list_linked_accounts|src/xagent/web/tools/mcp/instagram.py:115`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:instagram_list_media:4203f66d4a98|instagram_list_media|src/xagent/web/tools/mcp/instagram.py:150`: 0 → 1（+1）
- `v2-xorbitsai__xagent|mcp:meta_ads_auth_status:d36d5fd42096|meta_ads_auth_status|src/xagent/web/tools/mcp/meta_ads.py:189`: 0 → 1（+1）
