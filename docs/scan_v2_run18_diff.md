# full scan の突き合わせ: `scan_v2_run16` → `scan_v2_run18`

再現: `python scripts/compare_scans.py evidence/scan_v2_run16 evidence/scan_v2_run18`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run16 | scan_v2_run18 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 7915 | 8254 | +339 |
| 行 | 12952 | 16109 | +3157 |
| `CONTRADICTION` の行 | 1263 | 1279 | +16 |
| `GAP_INJECT` の行 | 1705 | 2290 | +585 |
| `GAP_SELECT` の行 | 492 | 496 | +4 |
| `UNKNOWN` の行 | 9221 | 14066 | +4845 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run16 | 189 |
| scan_v2_run18 | 189 |
| **増えた** | **0** |
| **消えた**（回帰の疑い） | **0** |

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run16 | scan_v2_run18 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 2298 | 2887 | +589 |
| `OP` / root なし | 10615 | 13179 | +2564 |
| `OP` / root あり | 39 | 43 | +4 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 39 → 43（+4）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 176

- `v2-xorbitsai__xagent|mcp:slack_search_messages:04d5b09fb0f6|slack_search_messages|src/xagent/web/tools/mcp/slack.py:911`: 0 → 12（+12）
- `v2-xorbitsai__xagent|mcp:jira_transition_issue:580c60c62729|jira_transition_issue|src/xagent/web/tools/mcp/jira.py:495`: 0 → 10（+10）
- `v2-xorbitsai__xagent|mcp:slack_upload_file:e6487563446e|slack_upload_file|src/xagent/web/tools/mcp/slack.py:1151`: 2 → 10（+8）
- `v2-xorbitsai__xagent|mcp:github_create_branch:f2238369bb55|github_create_branch|src/xagent/web/tools/mcp/github.py:1174`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_add_reaction:c0d6aa4bcc00|slack_add_reaction|src/xagent/web/tools/mcp/slack.py:1123`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_get_channel_history:2ea43e2c896b|slack_get_channel_history|src/xagent/web/tools/mcp/slack.py:651`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_get_channel_info:065969e108b6|slack_get_channel_info|src/xagent/web/tools/mcp/slack.py:784`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_get_thread_replies:f81e37b029f1|slack_get_thread_replies|src/xagent/web/tools/mcp/slack.py:730`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_join_channel:065969e108b6|slack_join_channel|src/xagent/web/tools/mcp/slack.py:457`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:slack_remove_reaction:c0d6aa4bcc00|slack_remove_reaction|src/xagent/web/tools/mcp/slack.py:1141`: 0 → 6（+6）
- `v2-xorbitsai__xagent|mcp:outlook_create_event:2271d1a0b554|outlook_create_event|src/xagent/web/tools/mcp/outlook.py:749`: 0 → 5（+5）
- `v2-xorbitsai__xagent|mcp:github_list_issues:6be90d8df2e2|github_list_issues|src/xagent/web/tools/mcp/github.py:765`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:intercom_add_internal_note:969f9b6ae40b|intercom_add_internal_note|src/xagent/web/tools/mcp/intercom.py:313`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:intercom_close_conversation:bf19afb85164|intercom_close_conversation|src/xagent/web/tools/mcp/intercom.py:338`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:intercom_reply_to_conversation:969f9b6ae40b|intercom_reply_to_conversation|src/xagent/web/tools/mcp/intercom.py:289`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:jira_add_comment:d2d7d5b9320e|jira_add_comment|src/xagent/web/tools/mcp/jira.py:589`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:jira_create_issue:f34e97f934de|jira_create_issue|src/xagent/web/tools/mcp/jira.py:367`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:jira_get_issue:bc2100f857e9|jira_get_issue|src/xagent/web/tools/mcp/jira.py:352`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:jira_list_comments:8e5b6040de40|jira_list_comments|src/xagent/web/tools/mcp/jira.py:553`: 0 → 4（+4）
- `v2-xorbitsai__xagent|mcp:jira_list_projects:2481941471c1|jira_list_projects|src/xagent/web/tools/mcp/jira.py:267`: 0 → 4（+4）
