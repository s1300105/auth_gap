# full scan の突き合わせ: `scan_v2_run10` → `scan_v2_run11`

再現: `python scripts/compare_scans.py evidence/scan_v2_run10 evidence/scan_v2_run11`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run10 | scan_v2_run11 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 7503 | 11500 | +3997 |
| 行 | 11611 | 16406 | +4795 |
| `CONTRADICTION` の行 | 178 | 1061 | +883 |
| `GAP_INJECT` の行 | 2236 | 2760 | +524 |
| `GAP_SELECT` の行 | 246 | 522 | +276 |
| `UNKNOWN` の行 | 9193 | 13274 | +4081 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run10 | 85 |
| scan_v2_run11 | 146 |
| **増えた** | **61** |
| **消えた**（回帰の疑い） | **0** |

### 増えた CONTRADICTION

- `v2-artyomzemlyak__tg-note` / `convert_document_from_content` / `FS_WRITE@shutil.rmtree`
- `v2-berkay2002__yt-scribe` / `create_mcp_server.agent_fetch_and_polish_youtube_tool` / `FS_WRITE@pathlib.Path.write_text`
- `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.mkdir`
- `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.write_text`
- `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.unlink`
- `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.chmod`
- `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.replace`
- `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.unlink`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_action_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_actions` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_node_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_nodes` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameter_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameters` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_type` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_services` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_message_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_details` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_type` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topics` / `FS_WRITE@os.makedirs`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_for_duration` / `FS_WRITE@builtins.open`
- `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_once` / `FS_WRITE@builtins.open`
- `v2-rwheeler007__cohort` / `browser_action` / `SPAWN@subprocess.run`
- `v2-rwheeler007__cohort` / `cohort_compiled_discussion` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_create_channel` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_discussion` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_meeting_start` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `cohort_post` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `condense_channel` / `FS_WRITE@pathlib.Path.write_text`
- `v2-rwheeler007__cohort` / `post_message` / `FS_WRITE@pathlib.Path.write_text`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run10 | scan_v2_run11 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 3664 | 4196 | +532 |
| `OP` / root なし | 7876 | 12171 | +4295 |
| `OP` / root あり | 71 | 39 | -32 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 71 → 39（-32）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 565

- `v2-constripacity__claude-replay|mcp-lowlevel-v1:call_tool:7071a54a23fa|call_tool|claude_replay/server.py:445`: 74 → 306（+232）
- `v2-redhat-ai-americas__memory-hub|mcp:memory:8613685544bf|memory|memory-hub-mcp/src/tools/memory.py:116`: 31 → 125（+94）
- `v2-kaistenberg__mcp-linkedin|mcp:register_person_tools.connect_with_person:6ef971ce1710|register_person_tools.connect_with_person|linkedin_mcp_server/tools/person.py:194`: 0 → 88（+88）
- `v2-kaistenberg__mcp-linkedin|mcp:register_messaging_tools.get_conversation:82013656691a|register_messaging_tools.get_conversation|linkedin_mcp_server/tools/messaging.py:86`: 0 → 84（+84）
- `v2-kaistenberg__mcp-linkedin|mcp:register_person_tools.get_person_profile:ccc7c3da8496|register_person_tools.get_person_profile|linkedin_mcp_server/tools/person.py:38`: 8 → 88（+80）
- `v2-kaistenberg__mcp-linkedin|mcp:register_company_tools.get_company_profile:127afff78dac|register_company_tools.get_company_profile|linkedin_mcp_server/tools/company.py:40`: 8 → 80（+72）
- `v2-artyomzemlyak__tg-note|mcp:sync_docling_models:fc0eed7a68e5|sync_docling_models|docker/docling-mcp/app/tg_docling/server.py:111`: 25 → 89（+64）
- `v2-kaistenberg__mcp-linkedin|mcp:register_job_tools.get_saved_jobs:b2d3e5b90c6b|register_job_tools.get_saved_jobs|linkedin_mcp_server/tools/job.py:160`: 8 → 72（+64）
- `v2-kaistenberg__mcp-linkedin|mcp:register_job_tools.search_jobs:3717cf6e2b15|register_job_tools.search_jobs|linkedin_mcp_server/tools/job.py:80`: 8 → 72（+64）
- `v2-kaistenberg__mcp-linkedin|mcp:register_person_tools.get_my_profile:7994d53359ee|register_person_tools.get_my_profile|linkedin_mcp_server/tools/person.py:316`: 0 → 64（+64）
- `v2-rwheeler007__cohort|mcp:cohort_compiled_discussion:e3082790faba|cohort_compiled_discussion|cohort/mcp/server.py:1950`: 6 → 69（+63）
- `v2-kaistenberg__mcp-linkedin|mcp:register_company_tools.get_company_employees:13d87b0705a8|register_company_tools.get_company_employees|linkedin_mcp_server/tools/company.py:223`: 0 → 60（+60）
- `v2-kaistenberg__mcp-linkedin|mcp:register_company_tools.search_companies:b73824907a3c|register_company_tools.search_companies|linkedin_mcp_server/tools/company.py:176`: 0 → 60（+60）
- `v2-kaistenberg__mcp-linkedin|mcp:register_job_tools.get_job_details:6508ec65dd3f|register_job_tools.get_job_details|linkedin_mcp_server/tools/job.py:33`: 0 → 60（+60）
- `v2-kaistenberg__mcp-linkedin|mcp:register_person_tools.search_people:adb883be07f3|register_person_tools.search_people|linkedin_mcp_server/tools/person.py:111`: 0 → 60（+60）
- `v2-kaistenberg__mcp-linkedin|mcp:register_post_tools.search_posts:3c52fe2e7747|register_post_tools.search_posts|linkedin_mcp_server/tools/post.py:39`: 0 → 60（+60）
- `v2-vishalsachdev__canvas-mcp|mcp:register_peer_review_comment_tools.extract_peer_review_dataset:467f097c958c|register_peer_review_comment_tools.extract_peer_review_dataset|src/canvas_mcp/tools/peer_review_comments.py:204`: 23 → 83（+60）
- `v2-kaistenberg__mcp-linkedin|mcp:TestAnAlreadyShapedToolErrorPassesThrough.test_the_cause_reaches_a_middleware_at_a_real_tool_catch_site.failing_tool:d36d5fd42096|TestAnAlreadyShapedToolErrorPassesThrough.test_the_cause_reaches_a_middleware_at_a_real_tool_catch_site.failing_tool|tests/test_error_handler.py:360`: 0 → 56（+56）
- `v2-kaistenberg__mcp-linkedin|mcp:TestTheMarkerSurvivesTheHop.test_the_marker_is_found_through_the_wrapping_tool_error.scrape:d36d5fd42096|TestTheMarkerSurvivesTheHop.test_the_marker_is_found_through_the_wrapping_tool_error.scrape|tests/test_daemon_auth.py:166`: 0 → 56（+56）
- `v2-kaistenberg__mcp-linkedin|mcp:register_company_tools.get_company_posts:75de92f434ea|register_company_tools.get_company_posts|linkedin_mcp_server/tools/company.py:108`: 4 → 60（+56）
