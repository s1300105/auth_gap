# r_prev run2（2026-09-20）— 訂正後の選択（`docs/prev_releases.json`、`5725099`）での測定

- `docs/preregistration.md` §2.7 の手順 2〜5。`scripts/r_prev.py --label run2`。
  木ごとの join 列は集計と同じ規則（unit id の完全一致）で数え、runner の
  `d_prev_joined` と一致することを assert した。
- `prev/` `prev5/` `current/` は各木の manifest（`authgap.report.manifest_json`、`full=False`）。
- 値: `docs/decisions.md` D27、`docs/preregistration.md` §5.1。
- 既知の限界: unit id が木の中で一意でない木が 4/16（crewAI 321 → 312、fewsats 8 → 4、
  nuguard 186 → 109、ava 20 → 19）。distinct-id で数え直した値を併記した（O13）。
