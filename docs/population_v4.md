# 母集団 v4: 凍結版の中間検証（**解析器は変えない**）

**抽出・取得・走査の前に書く**（2026-09-29）。書いた後で規則を変えない。変えるなら `docs/preregistration.md` §5 に
逸脱として記録する。決定は `docs/decisions.md` D66。

## 役割

- **中間検証**（学生の依頼、2026-09-29）。凍結した解析器 `analyzer-freeze-3` が、まだ誰も見ていないデータでどう振る舞うかを、
  本記録者が確かめて学生に報告する。**論文の評価ではない。論文の評価は、学生が別の新しいデータで手動で行う（D60）。**
- **結果を見て解析器を変えない。** `authgap/`（入口の規則・sink の語彙・判定の表 `catalog/statements.py` を含む）も、
  `docs/contradiction_principles.md` の原理と判定表も変えない。見つかった誤り・見落としは、直さずに `docs/open_questions.md` に
  限界（O43）として書くだけにする。v3（D60 / D61）との違いはここ: v3 は凍結の前の開発用データで、欠陥を直してよかった。
- **v4 の repo は学生の最終評価のデータに含めない**（v2・v3 と同じ。本記録者が結果を見たデータなので）。除く一覧は
  `docs/corpus_sample_v2.json`・`docs/corpus_sample_v3.json`・`docs/corpus_sample_v4.json`。
- 判定は本記録者 1 人が行う（中間検証なので二重判定はしない）。原ソースの確認は木ごとに agent に分けてよいが、根拠の
  ファイルと行を本記録者が見直して採る（v3 と同じ）。

## 枠と抽出（v2 / v3 と同じ枠。v2 と v3 の抽出分を除く）

- 枠: `docs/population_v2.md` の列挙（2026-09-20、`evidence/population_v2/enumeration.jsonl`）と、v2 / v3 と同じ抽出スクリプトの
  母集団（3,764 repo。枠の数の食い違いは O40）。**列挙はやり直さない**（v3 と比べられるように枠を同じにする）。
- 除外: v2 の 100 と v3 の 100（取得後に除いたものを含む全部）。
- 抽出: 残りから **seed = 20260929** で **100 件**を無作為抽出（`scripts/sample_population_v2.py --exclude docs/corpus_sample_v2.json
  --exclude docs/corpus_sample_v3.json --seed 20260929 --prefix v4`）。除外で減った分は補充しない。
- pin: 抽出時の `git ls-remote <url> HEAD` の SHA で固定し `docs/corpus_sample_v4.json` に書く。**この pin を取得・走査より先に
  コミットする。**
- 取得後の条件（v2 / v3 と同じ）: 宣言ファイルが `mcp` / `fastmcp` を import しないもの、宣言ファイルが見つからないもの、
  取得できないものは件数を出して除く（`scripts/check_population_v2.py`）。

## 走査

- 解析器: **`analyzer-freeze-3`（9dc3bc3）**。走査の前に次の 2 つを確かめ、どちらかが満たされなければ走らせない:
  `git diff analyzer-freeze-3 -- authgap/` が空、`authgap/` の結合 sha256 が `docs/fingerprint.json` の
  `implementation_sha256_combined`（35606ba9…）と一致。
- `scripts/scan_v2.py --sample <v4 の MCP サーバの標本> --label v4_run1 --require-fingerprint docs/fingerprint.json`
  （Python 3.12、tree budget 180 s、深さ 4。v2 / v3 と同じ設定）。**走査は 1 回だけ**（取り直すのは、道具の故障で走査が
  途中で止まったときだけ。そのときは理由を書く）。

## 確かめること（手続きと分母。v3 と同じ。D62 に合わせて宣言ごとに出す）

- **V1 頑健性**: parse 失敗・tree budget で打ち切った木（manifest の `tree_budget` の件数）・例外で落ちた木を全件列挙し、原因を
  1 件ずつ書く。分母は走査した木の数。マシンの速さで打ち切りが変わりうるので（D64 の追記）、打ち切った木の所要時間も書く。
- **V2 CONTRADICTION の精度**: 単位は (木, ユニット, site, kind, 宣言)。**D1 / D2 の矛は全件**判定する（60 件を超えたら
  `scripts/v3_judge_sample.py` の固定の seed で 60 件を抜き取り、抜き取りと明記する）。D3 / D4 の矛は別に 30 件まで。
  判定は原ソースを読み、`docs/contradiction_principles.md` §6 の採った原理で:
  - **正**: その経路は実行時に到達し、その動作は宣言に反する。
  - **誤**: 到達しない / 動作が宣言に反しない / 解析器が読み違えた（原因の分類を書く）。
  - **不明**: 静的に決められない（理由を書く。黙って正・誤に倒さない）。
  分母は判定した件数。宣言ごとに正 / 誤 / 不明の件数と、誤の原因の内訳を出す。**正には重大度の列を付ける**: ツール本来の動作か、
  裏側・補助的な書き込み（初回の初期化・ログ・キャッシュ・一時ファイル・条件つき）か（教科書 第 38 章の手引きの下書きを兼ねる）。
- **V3 見落としの抜き取り**: D1 か D2 を明示し、その宣言に対する矛が 1 件も出ていないユニットから `scripts/v3_miss_sample.py` の
  固定の seed で **30 件**を抜き取る。ツールの本体と木の中の呼び出し先を深さ 4 まで読み、宣言に反する動作があるかを判定する:
  解析器が不として出している / **見落とし（誤 clear）** / 反する動作は無い / 不明。見落としは「深さ・呼び出しの解決・受け手の型・
  語彙・その他」に分類する。分母は 30（足りなければ全数）。
- **V4 不**: 宣言ごとの件数と理由の内訳だけを出す（判定しない）。`scripts/contradiction_by_decl.py`。
- **V5 `r_malformed`**: `scripts/r_malformed.py`（§2.11 の定義）の値を出す（開発用の値として。論文には使わない）。

## 報告

- 学生に報告し、`docs/population_v4.md` の末尾に結果を書く。v3（`analyzer-freeze-1`、精度 81.7%）と並べてよいが、
  **版もデータも違うので「改善」「悪化」とは書かない**（v3 の欠陥の一部は凍結の前に直したが、v4 はその効果の測定ではない）。
- 誤と見落としは O43 に限界として書く。解析器・原理・判定表・語彙は変えない。
