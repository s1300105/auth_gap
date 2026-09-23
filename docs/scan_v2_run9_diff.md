# full scan の突き合わせ: `scan_v2_run7` → `scan_v2_run9`

再現: `python scripts/compare_scans.py evidence/scan_v2_run7 evidence/scan_v2_run9`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run7 | scan_v2_run9 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 5987 | 7462 | +1475 |
| 行 | 9576 | 11534 | +1958 |
| `CONTRADICTION` の行 | 178 | 178 | +0 |
| `GAP_INJECT` の行 | 1928 | 2204 | +276 |
| `GAP_SELECT` の行 | 246 | 246 | +0 |
| `UNKNOWN` の行 | 7288 | 9130 | +1842 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run7 | 85 |
| scan_v2_run9 | 85 |
| **増えた** | **0** |
| **消えた**（回帰の疑い） | **0** |

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run7 | scan_v2_run9 | 差 |
|---|---|---|---|
| `MODEL` / root あり | 3355 | 3631 | +276 |
| `OP` / root なし | 6150 | 7832 | +1682 |
| `OP` / root あり | 71 | 71 | +0 |

**「root はあるのに主体が OP」**（D44 が矛盾と呼んだ状態）: 71 → 71（+0）。

## 消えたユニット / 増えたユニット

消えた 0 / 増えた 0。

**ユニットが消えるのは入口の認識が変わったということなので、解析器の変更で起きたなら回帰である。** 1 件ずつ確かめる。


## 効果数が変わったユニット（上位 20）

変わったユニット: 411

- `v2-hbg1345__teamplay-talk|mcp:register.schedule_roadmap:1295d2835283|register.schedule_roadmap|src/teamplay_talk/tools/roadmap.py:1007`: 1 → 47（+46）
- `v2-hbg1345__teamplay-talk|mcp:register.decompose_roadmap:d6e4e20168fc|register.decompose_roadmap|src/teamplay_talk/tools/roadmap.py:1141`: 1 → 40（+39）
- `v2-redhat-ai-americas__memory-hub|mcp:memory:8613685544bf|memory|memory-hub-mcp/src/tools/memory.py:116`: 0 → 31（+31）
- `v2-hbg1345__teamplay-talk|mcp:register.send_form:3decefd7adfa|register.send_form|src/teamplay_talk/tools/feedback.py:823`: 9 → 34（+25）
- `v2-8dionysus__abyss-stack|mcp:build_server.kag_traverse:7c621c109c63|build_server.kag_traverse|mcp/services/aoa-kag-mcp/src/aoa_kag_mcp/server.py:136`: 0 → 23（+23）
- `v2-hbg1345__teamplay-talk|mcp:register.apply_daily_checkin:e6416d72fed4|register.apply_daily_checkin|src/teamplay_talk/tools/daily.py:704`: 9 → 31（+22）
- `v2-hbg1345__teamplay-talk|mcp:register.set_roles:d7a3916a0c3b|register.set_roles|src/teamplay_talk/tools/roles.py:649`: 3 → 25（+22）
- `v2-hbg1345__teamplay-talk|mcp:register.build_roadmap:68594933d1ed|register.build_roadmap|src/teamplay_talk/tools/roadmap.py:752`: 1 → 20（+19）
- `v2-tuttinator__fourex|mcp:register.submit_actions:02dcf0cf3076|register.submit_actions|backend/src/mcp_server/tools/gameplay.py:218`: 0 → 18（+18）
- `v2-hbg1345__teamplay-talk|mcp:register.daily_task_digest:aeb74320d064|register.daily_task_digest|src/teamplay_talk/tools/roadmap.py:1500`: 3 → 20（+17）
- `v2-hbg1345__teamplay-talk|mcp:register.add_task:f462e6c5ccd5|register.add_task|src/teamplay_talk/tools/roadmap.py:864`: 1 → 17（+16）
- `v2-hbg1345__teamplay-talk|mcp:register.daily_report:723c95e960a0|register.daily_report|src/teamplay_talk/tools/daily.py:743`: 5 → 21（+16）
- `v2-redhat-ai-americas__memory-hub|mcp:manage_project:0365e4099dd7|manage_project|memory-hub-mcp/src/tools/manage_project.py:65`: 0 → 16（+16）
- `v2-hbg1345__teamplay-talk|mcp:register.calendar_create_task_events:49d5ca30f17a|register.calendar_create_task_events|src/teamplay_talk/tools/calendar.py:254`: 7 → 21（+14）
- `v2-hbg1345__teamplay-talk|mcp:register.create_daily_checkin:8a0498aa9c73|register.create_daily_checkin|src/teamplay_talk/tools/daily.py:660`: 1 → 15（+14）
- `v2-redhat-ai-americas__memory-hub|mcp:register_session:b72c0a8f3bd7|register_session|memory-hub-mcp/src/tools/register_session.py:212`: 3 → 17（+14）
- `v2-tuttinator__fourex|mcp:register.create_game:1383806d9ec0|register.create_game|backend/src/mcp_server/tools/lifecycle.py:43`: 0 → 14（+14）
- `v2-hbg1345__teamplay-talk|mcp:register.update_task:030a9499d50f|register.update_task|src/teamplay_talk/tools/roadmap.py:949`: 1 → 14（+13）
- `v2-redhat-ai-americas__memory-hub|mcp:manage_graph:1d8deef2d07f|manage_graph|memory-hub-mcp/src/tools/manage_graph.py:69`: 0 → 13（+13）
- `v2-redhat-ai-americas__memory-hub|mcp:thread:0f3a4e143afb|thread|memory-hub-mcp/src/tools/thread.py:60`: 0 → 13（+13）
