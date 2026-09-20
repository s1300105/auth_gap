# 公平な CodeQL 比較（`docs/preregistration.md` §5 #4）

- CodeQL CLI 2.20.0 bundle、`codeql/python-queries` 1.3.4。データベースは
  `codeql database create --language=python --source-root=corpus/<tree>`。
- `default_summary.json`: 既定の `py/path-injection`（source = remote flow source）。
- `fair_summary.json`: `scripts/codeql/AuthGapPathInjection.ql`（source = AuthGap が
  入口と認識したユニットの仮引数。`entry_units_A1_A4_A9.json` から
  `scripts/codeql_fair.py gen` で生成）。sink / sanitizer / 伝播は CodeQL のまま。
- 実行日 2026-09-20。木は `docs/corpus_spec.json` の A1 / A4 / A9（A10 は A9 と共有）。
- 判定（4 類型）と決定は `docs/preregistration.md` §5 #4 と `docs/decisions.md` D26。
