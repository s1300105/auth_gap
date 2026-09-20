# r_prev run1（2026-09-20）— **手順 1 の選択に欠陥があった run。run2 が正**

- `docs/prev_releases.json`（`72bc952`）の選択で走らせた。`scripts/prev_releases.py` の
  `_run` が stdout と stderr を連結していたため、crewAI の「直前リリース」の日付に
  `git show` の gc 案内が入り、文字列比較で最大になって **v0.5.2（2024-02）** が
  選ばれていた（規則どおりなら 1.15.21、2026-09-09）。他の 15 木は変わらない
  （`docs/preregistration.md` §5 #6）。
- `trees.jsonl` の `prev_n_join` / `prev_n_join_dangerous` 列は**全木 0 で誤り**
  （`UnitReport.d_prev_joined` が probe 経路で立っていなかった。runner を直した）。
  `r_prev.json` の集計は `scripts/f0a.py: accumulate` が unit id の一致で数えた値で、
  こちらは正しい。
- 値（as-run、crewAI の選択が誤り）: `prev` 全体 64.2%（97/151、粗 58.8%）、
  app 8.3%、mcp_server 87.7%、tool_package 100%。`prev5` 全体 84.8%。
  **本文では run2 の値を使い、run1 は「選択の欠陥を直す前」として併記する。**
