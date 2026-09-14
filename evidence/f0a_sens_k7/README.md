# evidence/f0a_sens_k7 — 既知の欠陥 K7 の感度分析（関門の数字ではない）

**これは報告に使う run ではない。** `docs/decisions.md` D19 の「結果」にある、K7（別名つき from-import で
木内の関数へ降りない）の影響を見積もるための証拠である。関門の数字は run 6（`evidence/f0a_run6`）を使う。

- **解析器**: 150e06a を `git archive` で取り出し、`sensitivity_patch.diff`（3 行）だけを当てたもの。
  **このパッチはコミットしていない。** archive で走らせたので `f0a.json` の `run_meta.analyzer_commit` と
  `analyzer_dirty` は null。`authgap/` のほかのファイルは 150e06a と同一（全ファイルを `cmp` で確かめた）。
- **標本・上限・処理系**: run 6 と同じ（`sample_sha256` c8a3ffb4…、上限 mcp_server 60 / tool_package 30 / app 8、
  Python 3.12.13）。
- **パッチの確認**: 走らせる前に、別名ありの 2 形（相対 / 絶対 import）の fixture で NET 行が出ること、
  別名なしの対照の出力が変わらないことを確かめた（`tests/test_f0a_defects.py` の
  `test_known_aliased_from_import_descends_into_in_tree_function` と同じ形）。

## 再現

```bash
git archive 150e06a | tar -x -C <dir>
cd <dir> && patch -p1 < <repo>/evidence/f0a_sens_k7/sensitivity_patch.diff
ln -s <repo>/corpus <dir>/corpus
<repo>/.venv312/bin/python -u scripts/f0a.py --sample docs/corpus_sample.json --label sens_alias
# 出力は <dir>/evidence/f0a_sens_alias/（この directory の 3 ファイルと同じ内容になる）
```

## 比べ方

```bash
python scripts/lost_units.py evidence/f0a_run6 evidence/f0a_sens_k7   # 危険効果から外れた 0 / 新たに 26（mcp_server）
```

`f0a.json` の `populations.mcp_server` を run 6 と並べる。変わるのは mcp_server だけで、tool_package と app は
全指標が同一。
