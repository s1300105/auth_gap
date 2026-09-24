# full scan の突き合わせ: `scan_v2_run14` → `scan_v2_run15`

再現: `python scripts/compare_scans.py evidence/scan_v2_run14 evidence/scan_v2_run15`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run14 | scan_v2_run15 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 10193 | 7847 | -2346 |
| 行 | 15311 | 12889 | -2422 |
| `CONTRADICTION` の行 | 1299 | 1263 | -36 |
| `GAP_INJECT` の行 | 2810 | 1695 | -1115 |
| `GAP_SELECT` の行 | 522 | 492 | -30 |
| `UNKNOWN` の行 | 12156 | 9152 | -3004 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run14 | 191 |
| scan_v2_run15 | 189 |
| **増えた** | **1** |
| **消えた**（回帰の疑い） | **3** |

### 消えた CONTRADICTION — **1 件ずつ理由を確かめること**

- `v2-artyomzemlyak__tg-note` / `convert_document_from_content` / `FS_WRITE@shutil.rmtree`
- `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.write_text`

### 増えた CONTRADICTION

- `v2-nan-fe__agents` / `create_mcp.get_lark_auth_status` / `NET@httpx.AsyncClient.post`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run14 | scan_v2_run15 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 4291 | 2288 | -2003 |
| `OP` / root なし | 10979 | 10564 | -415 |
| `OP` / root あり | 41 | 37 | -4 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 41 → 37（-4）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 194

- `v2-vishalsachdev__canvas-mcp|mcp:register_student_tools.get_my_peer_reviews_todo:fe63270694ca|register_student_tools.get_my_peer_reviews_todo|src/canvas_mcp/tools/student_tools.py:417`: 230 → 92（-138）
- `v2-redhat-ai-americas__memory-hub|mcp:memory:8613685544bf|memory|memory-hub-mcp/src/tools/memory.py:116`: 157 → 57（-100）
- `v2-vishalsachdev__canvas-mcp|mcp:register_course_tools.get_course_content_overview:80c51faf788a|register_course_tools.get_course_content_overview|src/canvas_mcp/tools/courses.py:365`: 110 → 44（-66）
- `v2-vishalsachdev__canvas-mcp|mcp:register_shared_discussion_tools.list_discussion_entries:17196394d2a8|register_shared_discussion_tools.list_discussion_entries|src/canvas_mcp/tools/discussions.py:263`: 100 → 40（-60）
- `v2-vishalsachdev__canvas-mcp|mcp:register_student_tools.get_my_submission_status:175a4efc5d6b|register_student_tools.get_my_submission_status|src/canvas_mcp/tools/student_tools.py:220`: 90 → 36（-54）
- `v2-vishalsachdev__canvas-mcp|mcp:register_peer_review_comment_tools.extract_peer_review_dataset:467f097c958c|register_peer_review_comment_tools.extract_peer_review_dataset|src/canvas_mcp/tools/peer_review_comments.py:204`: 83 → 35（-48）
- `v2-vishalsachdev__canvas-mcp|mcp:register_shared_discussion_tools.get_discussion_entry_details:81205e18834b|register_shared_discussion_tools.get_discussion_entry_details|src/canvas_mcp/tools/discussions.py:487`: 80 → 32（-48）
- `v2-vishalsachdev__canvas-mcp|mcp:register_shared_discussion_tools.get_discussion_with_replies:539c1803e51c|register_shared_discussion_tools.get_discussion_with_replies|src/canvas_mcp/tools/discussions.py:665`: 80 → 32（-48）
- `v2-vishalsachdev__canvas-mcp|mcp:_register_builtin_scanner_tools.fix_accessibility_issues:b892c62c1679|_register_builtin_scanner_tools.fix_accessibility_issues|src/canvas_mcp/tools/accessibility.py:297`: 80 → 36（-44）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_messaging_tools.send_peer_review_followup_campaign:a67107ee4d0f|register_educator_messaging_tools.send_peer_review_followup_campaign|src/canvas_mcp/tools/messaging.py:954`: 80 → 36（-44）
- `v2-vishalsachdev__canvas-mcp|mcp:register_admin_tools.list_groups:f0e8d68aad0a|register_admin_tools.list_groups|src/canvas_mcp/tools/admin_tools.py:58`: 70 → 28（-42）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_assignment_tools.list_peer_reviews:faf1a246340f|register_educator_assignment_tools.list_peer_reviews|src/canvas_mcp/tools/assignments.py:200`: 70 → 28（-42）
- `v2-vishalsachdev__canvas-mcp|mcp:register_content_migration_tools.create_content_migration:63bad521fd3c|register_content_migration_tools.create_content_migration|src/canvas_mcp/tools/content_migrations.py:258`: 70 → 30（-40）
- `v2-vishalsachdev__canvas-mcp|mcp:register_admin_tools.get_student_analytics:89ba78197753|register_admin_tools.get_student_analytics|src/canvas_mcp/tools/admin_tools.py:171`: 60 → 24（-36）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_assignment_tools.get_assignment_analytics:c821e1a2cfdb|register_educator_assignment_tools.get_assignment_analytics|src/canvas_mcp/tools/assignments.py:354`: 60 → 24（-36）
- `v2-vishalsachdev__canvas-mcp|mcp:register_peer_review_comment_tools.get_peer_review_comments:10426aecc6aa|register_peer_review_comment_tools.get_peer_review_comments|src/canvas_mcp/tools/peer_review_comments.py:73`: 60 → 24（-36）
- `v2-vishalsachdev__canvas-mcp|mcp:register_student_write_tools.submit_assignment:1c1ff93044db|register_student_write_tools.submit_assignment|src/canvas_mcp/tools/student_write.py:714`: 80 → 44（-36）
- `v2-vishalsachdev__canvas-mcp|mcp:register_content_migration_tools.get_content_migration_status:0bfa76b71464|register_content_migration_tools.get_content_migration_status|src/canvas_mcp/tools/content_migrations.py:386`: 50 → 20（-30）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_discussion_tools.bulk_delete_announcements:7f908d4b59bc|register_educator_discussion_tools.bulk_delete_announcements|src/canvas_mcp/tools/discussions.py:1290`: 50 → 20（-30）
- `v2-vishalsachdev__canvas-mcp|mcp:register_educator_discussion_tools.delete_announcements_by_criteria:98a727a962bc|register_educator_discussion_tools.delete_announcements_by_criteria|src/canvas_mcp/tools/discussions.py:1416`: 50 → 20（-30）
