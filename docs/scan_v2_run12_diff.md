# full scan の突き合わせ: `scan_v2_run11` → `scan_v2_run12`

再現: `python scripts/compare_scans.py evidence/scan_v2_run11 evidence/scan_v2_run12`

**変更の前後を両方出す**（CLAUDE.md の約束）。この表の値は逸脱として
`docs/preregistration.md` に記録する。

## 全体

| 項目 | scan_v2_run11 | scan_v2_run12 | 差 |
|---|---|---|---|
| ユニット（manifest の生の件数） | 2231 | 2231 | +0 |
| ユニット（比較の鍵で数えたもの） | 2231 | 2231 | +0 |
| 効果 | 11500 | 11500 | +0 |
| 行 | 16406 | 16406 | +0 |
| `CONTRADICTION` の行 | 1061 | 1217 | +156 |
| `GAP_INJECT` の行 | 2760 | 2760 | +0 |
| `GAP_SELECT` の行 | 522 | 522 | +0 |
| `UNKNOWN` の行 | 13274 | 13274 | +0 |

## CONTRADICTION（ユニット × site × kind）

| | 件数 |
|---|---|
| scan_v2_run11 | 146 |
| scan_v2_run12 | 178 |
| **増えた** | **32** |
| **消えた**（回帰の疑い） | **0** |

### 増えた CONTRADICTION

- `v2-hbg1345__teamplay-talk` / `install.room_manage` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.add_task` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.apply_daily_checkin` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.assign_roles` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.calendar_create_room_event` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.calendar_create_task_events` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.create_daily_checkin` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.create_poll` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.create_room` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.daily_report` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.daily_task_digest` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.decompose_roadmap` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.finalize_roles` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.gather_locations` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.gather_opinions` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.gather_task_opinions` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.get_poll_results` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.join_room` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.member_tasks` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.notify_room` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.restore_room` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.room_dashboard` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.rooms` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.schedule_meeting` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.schedule_roadmap` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.send_form` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.set_roles` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.switch_room` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.update_task` / `DB@psycopg.Cursor.execute`
- `v2-hbg1345__teamplay-talk` / `register.view_roadmap` / `DB@psycopg.Cursor.execute`
- `v2-zelladir__asquared-mcp` / `build_mcp.coord_ack` / `DB@psycopg.Cursor.execute`
- `v2-zelladir__asquared-mcp` / `build_mcp.coord_post` / `DB@psycopg.Cursor.execute`

## slot の主体（D44 が直した箇所）

| 主体 / root | scan_v2_run11 | scan_v2_run12 | 差 |
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

