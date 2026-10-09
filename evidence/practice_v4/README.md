# 判定の練習（v4 の開発用データ。矛・見落としの 11 件と、実態調査の形の 4 件）

最終評価の判定表と**同じ形**の練習用の表です（`scripts/final_sample.py` と `scripts/final_sheet.py` で作った。seed は使い捨て）。
v4 は最終評価から除いた開発用のデータなので、見てもかまいません（D66 の 3）。ただし、**この 11 件（P-M・P-C）は教科書・手引き・決定シートに答えかその手がかりが書かれているので、手引きの使い方を覚える練習には使えますが、1 件の時間（A2・B1）には使いません**。時間は `warmup_and_timing.md` の T の件で測ります（2026-10-09）。手引きは `docs/drafts/final_judging_guide_draft.md`（D76 を反映した版）。

| ファイル | 中身 |
|---|---|
| `contradiction.csv` | 矛 8 組（D1 5・D2 3）。`seq` の順に判定する |
| `miss.csv` | 見落とし 3 件（D1）。**解析器の出力は載せていない**（手引き 18.2: 出力を見る前に読む） |
| `practice_*_targets.json` | 抜き取りの出力（表の元）。見落としの分には解析器の数（`n_effects`）が入っているので、判定が終わるまで開かない |
| `analyzer_view/P-*.txt` | 1 件ごとの解析器の出力（`show_target.py` の出力を保存したもの。手元で走査しなくてよい）。見落とし（P-M）の分は、自分で読んで書き出してから開く |
| `path_view/P-C*.txt` | 矛の 1 件ごとに、本体から効果の行までの道筋に出てくる関数**だけ**を 1 つのファイルに並べたもの（`scripts/path_view.py`）。印: ▶ 次を呼ぶ行、★ 効果の行、? 条件の行。解析器の道筋をなぞった読む補助で、正しいとは限らない。見落とし（P-M）の分は作らない（出力を見る前に読むため） |
| `fetch_spec_practice.json` | 練習に要る v4 の 6 木だけの取得の指定 |
| `answers_v4_DO_NOT_OPEN_FIRST.md` | v4 のときの本記録者（AI）の判定。**全部終えてから**開く。正解ではない |
| `warmup_and_timing.md` | **実態調査の形の練習の手順**: 練習の練習（W-01）で手順をなぞり、本番と同じ条件で T-01（と T-02・T-03）の 1 件の時間を測る。1 件の判定の手順を段ごとに細かく書いた。**時間を測るならここから** |
| `survey_practice.csv` | その 4 件（W-01・T-01〜T-03）の表（実態調査の形。`t_` で始まる欄と `stopped_early` は練習だけの欄） |
| `survey_practice_targets.json` | T-01〜T-03 を選んだ名簿の抜き取りの列（解析器を使わない。seed は使い捨て） |
| `fetch_spec_survey_practice.json` | その 4 木の取得の指定 |
| `analyzer_view/W-01.txt`・`T-*.txt` | その 4 件の解析器の出力。**判定を終えてから**開く |
| `survey_answers_DO_NOT_OPEN_FIRST/` | その 4 件の参考の答え（件ごとのファイル）。**その件の判定を終えてから**、その件のファイルだけ開く。正解ではない |

## 準備（1 回だけ）

```bash
git pull
uv venv .venv --python 3.10 && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/fetch_corpus.py --spec evidence/practice_v4/fetch_spec_practice.json   # 練習の 6 木を corpus/ に取る
git restore docs/frame.csv docs/fetch_failures.md   # 取得の道具が書き換える記録のファイルを元に戻す（練習では使わない）
```

表は Excel・Numbers・Google スプレッドシートで開けます（BOM つきの UTF-8）。

## 矛の 1 行（手引き 第 13 節の手順 A〜H）

1. `unit_relpath:unit_lineno` を `corpus/<tree>/` の下で開く（ツールの本体）。
2. `locations`（効果の位置）まで本体からたどる。解析器が見た道筋は `analyzer_view/<pair_id>.txt` にある。
3. 2 つの問い（届くか・宣言に反するか）に答えて `verdict`（正 / 誤 / 不明）を決め、正なら `condition_type`・`write_target`、
   誤なら `error_class`（E1〜E9）、不明なら `unknown_reason` を書く。**`reachable`・`violates`・`condition` の欄は空のままでよい**
   （D83。2026-10-06 に書く欄を減らした。この CSV は前の形で作ったので欄が残っている）。条件の中身は `evidence` に「条件: …」と書く。
   D1 の正では、変える場所をツールの引数の値が一部でも決めるか（`はい` / `いいえ` / `決められない`）も決める（D84。この CSV には
   `target_by_arg` の欄が無いので `note` に「target_by_arg: はい」のように書く）。
4. `evidence` にたどったファイルと行を、`minutes` に分数を書く（手順 A から書き終わりまで。手引き 12.3）。

## 見落としの 1 行（手引き 18.2）

1. 解析器の出力を見ずに、本体から木の中の呼び出しを深さ 4 まで読む。
2. 宣言に反しうる動作を全部書き出す。
3. ここで初めて解析器の出力を見る（`analyzer_view/<pair_id>.txt`）。
4. `outcome` を 5 つから選ぶ（反する動作は無い / 解析器が不として出している / 見落とし / 見落とし（深さ 4 の外）/ 不明）。

## 終わったら

- 1 件ごとの `minutes` と、手引きで迷ったところ（節の番号）を教えてください。
- 答え合わせのファイルと比べ、食い違いが「手引きが曖昧だったから」なら、封の前に手引きを直します。
