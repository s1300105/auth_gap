# 深さの上限の感度分析（O29）

再現: `python scripts/depth_sensitivity.py evidence/scan_v2_depth3_sens evidence/scan_v2_depth4_sens evidence/scan_v2_depth5_sens`

**解析器の `MAX_DEPTH` は 3 のまま**（`authgap/ir.py`）。各 run は `scripts/scan_v2.py --max-depth` で `Options.max_depth` だけを変えた。基準は先頭の run。

## 件数

| 項目 | `scan_v2_depth3_sens` | `scan_v2_depth4_sens` | `scan_v2_depth5_sens` |
|---|---|---|---|
| `max_depth` | 3 | 4 | 5 |
| 解析器の commit | d6dfb80 | 1f60e82 | 0a40486 |
| ユニット | 2231 | 2231 | 2231 |
| 効果（生の件数） | 7503 | 11500 | 17694 |
| 効果の位置（一意） | 3185 | 4050 | 4228 |
| 効果の経路（一意） | 4273 | 5924 | 7586 |
| 　DB | 1741 | 2490 | 2989 |
| 　FS_READ | 258 | 519 | 634 |
| 　FS_WRITE | 326 | 2340 | 3899 |
| 　NET | 5051 | 6011 | 10029 |
| 　SPAWN | 127 | 140 | 143 |
| `db_unresolved`（一意） | 569（181） | 532（178） | 495（170） |
| **DB 未解決率** | 24.6% | 17.6% | 14.2% |
| `GAP_INJECT`（一意な位置） | 994 | 1108 | 1145 |
| CONTRADICTION（ユニット × site × kind） | 85 | 146 | 193 |
| `CONTRADICTION` の行 | 178 | 1061 | 2184 |
| `GAP_INJECT` の行 | 2236 | 2760 | 3327 |
| `GAP_SELECT` の行 | 246 | 522 | 778 |
| `UNKNOWN` の行 | 9193 | 13274 | 20807 |
| 深さの上限に当たったユニット | 1642 | 805 | 696 |

## 基準との集合差（**消えた側が回帰**）

| 比較 | 消えたユニット | 増えたユニット | 消えた効果の位置 | 増えた効果の位置 | 消えた経路 | 増えた経路 | 消えた `GAP_INJECT` | 増えた `GAP_INJECT` | 消えた CONTRADICTION | 増えた CONTRADICTION |
|---|---|---|---|---|---|---|---|---|---|---|
| `scan_v2_depth3_sens` → `scan_v2_depth4_sens` | 0 | 0 | 0 | 865 | 0 | 1651 | 0 | 114 | 0 | 61 |
| `scan_v2_depth3_sens` → `scan_v2_depth5_sens` | 0 | 0 | 0 | 1043 | 0 | 3313 | 0 | 151 | 0 | 108 |

### CONTRADICTION の差（`scan_v2_depth3_sens` → `scan_v2_depth4_sens`）

- 増えた: `v2-artyomzemlyak__tg-note` / `convert_document_from_content` / `FS_WRITE@shutil.rmtree`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.agent_fetch_and_polish_youtube_tool` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.mkdir`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.unlink`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_action_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_actions` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_node_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_nodes` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameter_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameters` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_type` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_services` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_message_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_type` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topics` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_for_duration` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_once` / `FS_WRITE@builtins.open`
- 増えた: `v2-rwheeler007__cohort` / `browser_action` / `SPAWN@subprocess.run`
- 増えた: `v2-rwheeler007__cohort` / `cohort_compiled_discussion` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_create_channel` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_discussion` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_meeting_start` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_post` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `condense_channel` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `post_message` / `FS_WRITE@pathlib.Path.write_text`

### CONTRADICTION の差（`scan_v2_depth3_sens` → `scan_v2_depth5_sens`）

- 増えた: `v2-artyomzemlyak__tg-note` / `convert_document_from_content` / `FS_WRITE@shutil.rmtree`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.agent_fetch_and_polish_youtube_tool` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.agent_polish_transcript_tool` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.mkdir`
- 増えた: `v2-berkay2002__yt-scribe` / `create_mcp_server.fetch_youtube_transcript_tool` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-innovatehubph__innovatehub-ai-platform` / `send_message` / `SPAWN@git.Git.describe`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheFrontendActsOnTheMarker.test_a_login_that_does_not_help_stops_after_one_retry.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `TestTheRepairRunsForReal.test_a_replay_that_runs_long_does_not_hang_the_client.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `_owner_that_fails_with.scrape` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_employees` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_posts` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_posts` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_profile` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.get_company_profile` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_company_tools.search_companies` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_feed_tools.get_feed` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_feed_tools.get_feed` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_job_details` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_saved_jobs` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.get_saved_jobs` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.search_jobs` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_job_tools.search_jobs` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_messaging_tools.get_inbox` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_my_profile` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_person_profile` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_person_profile` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.get_sidebar_profiles` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_person_tools.search_people` / `FS_WRITE@shutil.move`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.chmod`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.replace`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@os.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-kaistenberg__mcp-linkedin` / `register_post_tools.search_posts` / `FS_WRITE@shutil.move`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_action_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_action_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_actions` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_action_tools.get_actions` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_node_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_node_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_nodes` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_node_tools.get_nodes` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameter` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameter_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameter_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameters` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.get_parameters` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_parameter_tools.has_parameter` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_type` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_service_type` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_services` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_service_tools.get_services` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_message_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_message_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_details` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_details` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_type` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topic_type` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topics` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.get_topics` / `FS_WRITE@os.makedirs`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_for_duration` / `FS_WRITE@builtins.open`
- 増えた: `v2-lara-unb__ros-mcp-ur3-antigravity` / `register_topic_tools.subscribe_once` / `FS_WRITE@builtins.open`
- 増えた: `v2-rwheeler007__cohort` / `browser_action` / `SPAWN@subprocess.run`
- 増えた: `v2-rwheeler007__cohort` / `cohort_compiled_discussion` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_create_channel` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_discussion` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_generate_briefing` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_meeting_start` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `cohort_post` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `condense_channel` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-rwheeler007__cohort` / `post_message` / `FS_WRITE@pathlib.Path.write_text`
- 増えた: `v2-yahoojp-marketing__ly-ads-mcp-server` / `read_display_report` / `FS_WRITE@pathlib.Path.unlink`
- 増えた: `v2-yahoojp-marketing__ly-ads-mcp-server` / `read_search_report` / `FS_WRITE@pathlib.Path.unlink`

## 費用

| 項目 | `scan_v2_depth3_sens` | `scan_v2_depth4_sens` | `scan_v2_depth5_sens` |
|---|---|---|---|
| 所要時間の合計（秒） | 918.7 | 1037.8 | 1019.8 |
| tree budget で打ち切られた木 | v2-david-li0406__meta-skill-evloving | v2-david-li0406__meta-skill-evloving | v2-david-li0406__meta-skill-evloving |
| 失敗した木 | 0 | 0 | 0 |

### 所要時間が大きい木（基準の上位と、どれかの run で 30 秒以上）

| 木 | `scan_v2_depth3_sens` | `scan_v2_depth4_sens` | `scan_v2_depth5_sens` |
|---|---|---|---|
| `v2-david-li0406__meta-skill-evloving` | 547.5（打ち切り） | 615.8（打ち切り） | 557.4（打ち切り） |
| `v2-mcparmory__registry` | 78.6 | 85.9 | 81.8 |
| `v2-xorbitsai__xagent` | 74.0 | 76.5 | 75.7 |
| `v2-vishalsachdev__canvas-mcp` | 24.2 | 47.7 | 74.9 |

## 木ごとの効果の増減（基準との差が大きい順、上位 20）

| 木 | `scan_v2_depth3_sens` | `scan_v2_depth4_sens` | `scan_v2_depth5_sens` |
|---|---|---|---|
| `v2-xorbitsai__xagent` | 772 | 1138 | 1160 |
| `v2-rwheeler007__cohort` | 112 | 232 | 240 |
| `v2-kaistenberg__mcp-linkedin` | 24 | 108 | 144 |
| `v2-hbg1345__teamplay-talk` | 382 | 484 | 494 |
| `v2-benjaminwalkerbond__auto_grocer` | 51 | 62 | 98 |
| `v2-lara-unb__ros-mcp-ur3-antigravity` | 5 | 23 | 41 |
| `v2-vishalsachdev__canvas-mcp` | 479 | 505 | 505 |
| `v2-elewa-git__odoo-mcp-server` | 7 | 25 | 25 |
| `v2-constripacity__claude-replay` | 16 | 32 | 33 |
| `v2-artyomzemlyak__tg-note` | 66 | 80 | 83 |
| `v2-malkreide__swiss-environment-mcp` | 0 | 16 | 16 |
| `v2-fbratten__agentspool` | 40 | 54 | 55 |
| `v2-redhat-ai-americas__memory-hub` | 83 | 94 | 96 |
| `v2-rahmanef63__cowork-kit-setup` | 8 | 8 | 21 |
| `v2-oldmangrizzz__hughmkiii` | 15 | 26 | 27 |
| `v2-eromang__researches` | 5 | 11 | 14 |
| `v2-berkay2002__yt-scribe` | 0 | 4 | 8 |
| `v2-napjon__mcp-cdp` | 4 | 7 | 11 |
| `v2-ariffazil__wealth` | 17 | 18 | 24 |
| `v2-nan-fe__agents` | 5 | 9 | 10 |

