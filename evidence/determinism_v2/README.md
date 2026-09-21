# 母集団 v2（87 木）の決定論チェック（`authgap scan --determinism 3`）

再現:

```bash
for t in $(python3 -c "import json; print(' '.join(x['name'] for x in json.load(open('evidence/population_v2/sample_v2_mcp.json'))['targets']))"); do
  .venv312/bin/python -m authgap scan corpus/$t --population mcp_server --determinism 3 > /dev/null 2> evidence/determinism_v2/$t.err \
    && echo "OK $t" || echo "FAIL $t rc=$?"
done | tee evidence/determinism_v2/results.txt
```

処理系 Python 3.12.3、解析器 235ae1e（scan の途中で解析器のコミットは変えていない。
決定論モードは 1 プロセス内で `run()` を 3 回回し、`determinism_signature`（`run_meta`
の経過時間を除いた manifest）のバイト一致を見る）。

## 結果（2026-09-21）

| 判定 | 木 | 内訳 |
|---|---|---|
| OK（3 回一致） | 85 | `results.txt` の `OK` 行。所要は 1 木あたり 1〜98 秒（3 回分） |
| FAIL rc=137 | 1 | `v2-david-li0406__meta-skill-evloving`（.py 36,900 ファイル、1.9 GB）。3 回分の index を 1 プロセスに持つと 16 GB のコンテナで OOM kill。**不一致ではなく未測定。** 1 回の scan（`evidence/f0a_v2_run2_budget900`、716 ユニット、608 秒）は完走する |
| FAIL rc=3（不一致） | 1 | `v2-xorbitsai__xagent`（352 ユニット）。差は **`units[0].notes` の `TRUNCATED(wall_clock)` の有無だけ**（1 回目にあり、2 回目に無い）。別プロセスで 3 回 scan した manifest は `run_meta.elapsed_s` 以外バイト一致 |

xagent の不一致の機構: `authgap/runner.py` はユニット 1 件の解析が `WALL_CLOCK_CAP`
秒を超えると `TRUNCATED(wall_clock)` を notes に付ける。1 プロセス内の 2 回目は
`analyze._SELF_FIELD_CACHE` / `gate._ATOM_INDEX_CACHE` が温まっているので同じユニットが
cap を超えず、note が消える。**解析結果（効果行・等級・判定）は 3 回とも同じ**で、
壁時計に依存する印だけが違う。壁時計 cap は設計上、決定論の対象外である（cap に
当たった件数は `truncations` として報告する）。

`.err` ファイル（コーパス由来の SyntaxWarning が大半）はコミットしない。
