# 判定の練習（v4 の開発用データ、11 件）

最終評価の判定表と**同じ形**の練習用の表です（`scripts/final_sample.py` と `scripts/final_sheet.py` で作った。seed は使い捨て）。
v4 は最終評価から除いた開発用のデータなので、見てもかまいません（D66 の 3）。手引きは `docs/drafts/final_judging_guide_draft.md`（D76 を反映した版）。

| ファイル | 中身 |
|---|---|
| `contradiction.csv` | 矛 8 組（D1 5・D2 3）。`seq` の順に判定する |
| `miss.csv` | 見落とし 3 件（D1）。**解析器の出力は載せていない**（手引き 18.2: 出力を見る前に読む） |
| `practice_*_targets.json` | 抜き取りの出力（表の元）。見落としの分には解析器の数（`n_effects`）が入っているので、判定が終わるまで開かない |
| `answers_v4_DO_NOT_OPEN_FIRST.md` | v4 のときの本記録者（AI）の判定。**全部終えてから**開く。正解ではない |

## 準備（1 回だけ）

```bash
git pull
uv venv .venv --python 3.10 && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/fetch_corpus.py --spec evidence/population_v4/fetch_spec.json   # v4 の原ソースを corpus/ に取る
```

表は Excel・Numbers・Google スプレッドシートで開けます（BOM つきの UTF-8）。

## 矛の 1 行（手引き 第 13 節の手順 A〜H）

1. `unit_relpath:unit_lineno` を `corpus/<tree>/` の下で開く（ツールの本体）。
2. `locations`（効果の位置）まで本体からたどる。解析器の道筋を見たいときは:
   `.venv/bin/python scripts/show_target.py evidence/scan_v2_v4_run1/<tree>.json <unit_relpath> <unit_lineno> <site>`
   （manifest は追跡していないので、無ければ v4 を走査し直す。手順書 6.8）
3. `reachable`（はい / いいえ / 不明）・`violates`・`verdict`（正 / 誤 / 不明）を決め、正なら `condition_type`・`write_target`、
   誤なら `error_class`（E1〜E9）、不明なら `unknown_reason` を書く。
4. `evidence` にたどったファイルと行を、`minutes` に分数を書く（手順 A から書き終わりまで。手引き 12.3）。

## 見落としの 1 行（手引き 18.2）

1. 解析器の出力を見ずに、本体から木の中の呼び出しを深さ 4 まで読む。
2. 宣言に反しうる動作を全部書き出す。
3. ここで初めて解析器の出力を見る（`show_target.py` を site なしで）。
4. `outcome` を 5 つから選ぶ（反する動作は無い / 解析器が不として出している / 見落とし / 見落とし（深さ 4 の外）/ 不明）。

## 終わったら

- 1 件ごとの `minutes` と、手引きで迷ったところ（節の番号）を教えてください。
- 答え合わせのファイルと比べ、食い違いが「手引きが曖昧だったから」なら、封の前に手引きを直します。
