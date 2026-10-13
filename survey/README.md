# 実態調査（survey）

D1（`readOnlyHint: true`）を宣言した MCP のツールを無作為に選び、人が読んで、宣言に反する動作（呼んだ後に何かが残る動作）に届くかを
判定する。結果は **実態の数**（違反の割合）と、**解析器の再現率**の正解（ground truth）に使う（D82・D94）。精度は別に、AuthGap の矛を
無作為抽出して人が確かめて出す（事前登録の下書き (f)）。

## ファイル

| ファイル | 中身 |
|---|---|
| `PROTOCOL.md` | **判定の規則**。判定はこれだけを見て行う。何を判定するか・起点と読む範囲・届くか・sink・木の外の関数の決め方・答え・記録・AI・道具・封の前に決めること（仮の扱いと規則の無い点の一覧） |
| `prompts/1_library.txt` | プロンプト 1: 木の外の関数が何をするか |
| `prompts/2_explain.txt`・`prompts/2_followup.txt` | プロンプト 2: コード解説と、続けての質問 |
| `prompts/3_case.txt`・`prompts/3_followup.txt` | プロンプト 3: 件の答え（参考。人が判定した後）と、AI が求めたファイルを渡す続き |

道具は repo の `scripts/` にある（`survey_roster.py`: 名簿と抜き取り、`check_survey_practice.py`: 表の確かめ。本番は `--sheet <配った表>`）。決定は
`docs/decisions.md`（D82〜D95）、未決は `docs/open_questions.md`（O48・O49・O50）の 1 か所に書く。練習の手順書は
`archive/practice_survey_manual/` に記録として残した（今の決まりは `PROTOCOL.md`）。

## 流れ

1. **封の前に決める**: `PROTOCOL.md` の 10 節（仮の扱い・規則の無い点・そのほかの未決。答えを変えるもの）と、本番の準備（O49: 枠の `--keep`、名簿を作る Python の版、本番の
   判定表など）。
2. **封をする**: 事前登録と `PROTOCOL.md` を確定し、日付を入れてコミットする。日付が抜き取りの種 seed ⑦（`YYYYMMDD7`）になる。
3. **枠を pin し、取得し、名簿を作る**（解析器を使わない）:
   `scripts/sample_population_v2.py --all` → 取得と取得後の条件・重複の除去 → `scripts/survey_roster.py build`。
4. **抜き取る**: `scripts/survey_roster.py sample <名簿> --seed <封の日付>7 --n <件数> --out <列>`。**判定の前に列をコミットする**。
5. **判定する**: 列の順に、`PROTOCOL.md` のとおり。表には名簿の 9 欄 ＋ `outcome`・`evidence` だけ。AI を使ったら、1 件 1 ファイルの
   ログを残す（`PROTOCOL.md` の 8 節）。全部終えるまで AuthGap の出力を見ない。
6. **突き合わせる**: 全部終えてから、AuthGap（と比べる相手）の出力と突き合わせて再現率を出す。

件数は 200（D94）。200 が判定できた件か抜き取る件かは未決（O50 の 1）。
