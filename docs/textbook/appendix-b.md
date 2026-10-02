[← 付録 A 用語集（登場順）](appendix-a.md) ｜ [目次](README.md) ｜ [付録 C 決定の年表 →](appendix-c.md)

---

# 付録 B ファイルの地図

<a id="ab-1"></a>
## この付録の使い方

### 一言で言うと

repo（`/home/user/auth_gap`）の中の、この研究で読むファイルの一覧です。**どこに何があり、最終評価のどの場面で開くか**を、役割ごとにまとめました。2026-10-01 に、ここに書いたファイルが実在することを `ls` で確かめました。最終評価で新しく作るファイル（まだ無いもの）は、B.10 に分けて書きました。

### たとえ話 — 建物の案内図

大きな病院の入り口には案内図があります。「受付は 1 階」「検査室は 2 階」「薬局は 1 階の奥」と、目的ごとに場所が書いてあります。初めて来た人も、案内図を見れば迷いません。この付録は、repo の案内図です。

### 小さな例 — 1 行の読み方

| ファイル | 中身 | いつ開くか | 本文 |
|---|---|---|---|
| `docs/drafts/final_judging_guide_draft.md` | 判定の手引きの下書き（709 行、下書き・未承認） | 承認の前に読む。承認後は `docs/final_judging_guide.md` を開く | 第 48〜52 章 |

この行は、「判定の手引きの下書きは `docs/drafts/` にある。今は下書きなので、学生が承認したら正本の場所に移る。判定の規則は第 48〜52 章で説明している」と読みます。

### 一歩ずつ — 欄の意味

- **ファイル**: repo の根からの相対パス。末尾が `/` ならディレクトリ。
- **中身**: そのファイルに何が書いてあるか。行数は 2026-10-01 の時点の `wc -l` の値。
- **いつ開くか**: 最終評価の段階（[第 45 章](ch45.md)）のどこで使うか。
- **本文**: そのファイルを説明した章。

### なぜ役割ごとに並べたのか

ファイルを名前の順に並べると、`docs/` の下だけで 86 の項目（2026-10-01）が並び、どれが大事か分かりません。この研究では、文書に「偉さ」の順があります（[第 0 章](ch00.md)）。正本 → 決定の記録 → 手順書 → この教科書、です。役割ごとに並べると、この順が見えます。

### よくある誤解・つまずき

- **原典の「教科書 第 N 章」をこの本の章番号で読む**: 決定の記録や手順書などの原典が「教科書 第 N 章」と書くときは、**第 3 版の章番号**です。第 3 版は `docs/textbook_v3.md` に残してあります。この本（第 4 版、`docs/textbook/`）の番号への読み替えは、前付けの対応表で行います。
- **manifest が git にあると思う**: 木ごとの manifest は大きいので git では追いません（`.gitignore`）。`summary.json` と `contradictions.json` は追います。
- **`docs/fingerprint.json` の `freeze.tag` を信じる**: その欄は `analyzer-freeze-2` と書いてありますが、正しいタグは `analyzer-freeze-3` です（逸脱 #26）。
- **`corpus/` に最終評価の木があると思う**: 2026-10-01 の時点の `corpus/` には、較正対・v2・v3・v4 などの木（512 項目）しかありません。最終評価の木は段階 4 で取得します。

### 手作業ではどう使うか

判定の最中に開くのは、主に次の 4 つです。

1. 判定の手引き（正本。B.1）
2. 判定表の CSV と、その組の manifest（B.10・B.6）
3. 原ソース `corpus/<木>/`（B.6）
4. 原理と判定表 `docs/contradiction_principles.md`（B.1）

### この節のまとめ

- 役割ごとに、どこに何があるかを書いた案内図。2026-10-01 に実在を確かめた。
- 最終評価で新しく作るファイルは B.10 に分けた。
- 第 3 版は `docs/textbook_v3.md`（原典の「教科書 第 N 章」はこの版の番号）。manifest は git で追わない。`freeze.tag` の欄は古い。

---

<a id="ab-2"></a>
## B.1 正本と規則の文書 — 判定で従うもの

| ファイル | 中身 | いつ開くか | 本文 |
|---|---|---|---|
| `docs/drafts/prereg_2_12_draft.md` | 事前登録 §2.12（最終評価）の下書き（131 行、下書き・未承認）。D67〜D70 を写したもの。【確認】2 点と【保留】がある | 封の前に承認する。承認後は `docs/preregistration.md` の §2.12 に写す | 第 22・46・47 章 |
| `docs/drafts/final_judging_guide_draft.md` | 判定の手引きの下書き（709 行、下書き・未承認）。手順書の第 11〜22 節を写し、D67〜D70 と合わない 5 点を直したもの | 封の前に承認する。承認後は `docs/final_judging_guide.md` に移す | 第 48〜52 章、[付録 E](appendix-e.md) |
| `docs/contradiction_principles.md` | 矛盾の判定の原理（§1〜§5 の選択肢、§6 学生の選択、§7 判定表、§9 直し方の規則） | 判定の最中に §7 を開いておく（手引き 12.1） | 第 17・28 章 |
| `docs/preregistration.md` | 事前登録（667 行）。§2 分母、§2.11 `r_malformed`、§5 逸脱の記録（#1〜#26） | 封のときに §2.12 を足す。手引きで決まらない事例は §5 に書く | [第 22 章](ch22.md) |
| `AUTHGAP_BRIEF_v3.md` | 仕様書（1,210 行）。正本として残し、書き換えない（`CLAUDE.md` 規則 6） | 決定の根拠をたどるとき | 第 8・22 章 |
| `CLAUDE.md` | 作業の約束（規則 1〜6、語彙の定義点、落とし穴、手順） | 規則を確かめるとき | 第 0・22 章 |

表の読み方: 上の 2 行は、今は下書きで、承認と封の後に正本になります。3 行目の判定表（§7）は、判定の基準の出どころです（手引き 11.3）。

---

<a id="ab-3"></a>
## B.2 決定・未決・手順の記録

| ファイル | 中身 | いつ開くか | 本文 |
|---|---|---|---|
| `docs/decisions.md` | 決定の記録 D1〜D71（3,973 行）。D71 の訂正と、D70 の 3 の改訂（2026-10-02）を含む。並びは番号順ではない（D39〜D20、D1〜D16、D19〜D17、D40〜D71 の順） | 規則の理由を確かめるとき | [第 46 章](ch46.md)、[付録 C](appendix-c.md) |
| `docs/open_questions.md` | 未決事項と既知の限界 O1〜O46（1,368 行）。O2 保留、O41〜O43 既知の限界、O44 解決、O45 の 4 が残る、O46 記録 | 解析器の誤りを見つけたとき（限界として書く） | 第 42・46 章 |
| `docs/final_evaluation_procedure.md` | 最終評価の手順書（1,501 行）。段階 0〜9 の地図。第 11〜22 節が手引きの元、第 23〜28 節が集計・論文・チェックリスト | 段階ごとに、何をするかを確かめるとき | 第 45〜47・55 章 |
| `docs/verification_guide.md` | 手検証の入口 | 走査の結果を手で確かめるとき | [第 23 章](ch23.md) |
| `docs/review_plan.md` | 最終凍結前の添削の計画（先にコミット）と進行の記録 | 添削の経緯を確かめるとき | [第 36 章](ch36.md) |
| `docs/review_triage.md` | 添削の所見 151 件を 55 単位にまとめた採否の表 | 同上 | 第 36・42 章 |
| `docs/rule_implementation_audit.md` | 事前登録した規則が実装されているかの点検（D47） | — | [第 23 章](ch23.md) |
| `RESUME.md` | 経緯の記録（参考程度） | — | — |

---

<a id="ab-4"></a>
## B.3 データの定義と標本

| ファイル | 中身 | いつ開くか | 本文 |
|---|---|---|---|
| `docs/population_v2.md` | 母集団 v2 の定義と結果（開発用、87 木） | v2 の数字を確かめるとき | 第 25・40 章 |
| `docs/population_v3.md` | 母集団 v3 の定義と結果（開発用の中間確認、91 木） | v3 の数字を確かめるとき | 第 34・40 章 |
| `docs/population_v4.md` | 母集団 v4 の規則（走査の前にコミット）と結果（凍結版の中間検証、88 木。130 行） | v4 の数字と判定の練習のとき | 第 37・40 章 |
| `docs/corpus_sample_v2.json`・`docs/corpus_sample_v3.json`・`docs/corpus_sample_v4.json` | v2・v3・v4 の repo の一覧。最終評価から除く | 段階 3 の除外に使う | 第 25・47 章 |
| `evidence/population_v2/enumeration.jsonl` | 2026-09-20 の列挙の生データ（枠の元） | 段階 3 で枠として使う | 第 25・47 章 |
| `evidence/population_v2/` | v2 の列挙・取得・取得後の条件の記録（`enumeration.json`、`fetch_result.json`、`post_fetch_check.json`、`sample_v2_mcp.json` など） | — | [第 25 章](ch25.md) |
| `evidence/population_v3/` | v3 の判定の記録（`v2_judgments.json`、`v3_miss_judgments.json`、`v3_miss_recheck_freeze3.json` など） | — | 第 34・41 章 |
| `evidence/population_v4/` | v4 の判定の記録（`v4_judgments.json`、`v4_judge_targets.json`、`v4_miss_targets.json`、`contradiction_by_decl_v4_run1.md` など） | 判定の練習（v4 の判定を見ずに判定してから比べる） | 第 37・53・54 章 |
| `docs/corpus_spec.json` | 較正対の取り出す版の指定 | 両側比較のとき | [第 31 章](ch31.md) |
| `docs/expected_tuples.json` | 較正対の事前登録の期待（採点器より先にコミット） | — | [第 31 章](ch31.md) |

---

<a id="ab-5"></a>
## B.4 解析器 `authgap/`（凍結 `analyzer-freeze-3`。変えない）

| ファイル | 中身 | 本文 |
|---|---|---|
| `authgap/` | 解析器の本体。標準ライブラリ `ast` だけで書かれている | 第 7・11 章 |
| `authgap/catalog/entries.py` | 入口の規則 `ENTRY_RULES`（14 規則。核） | [第 12 章](ch12.md) |
| `authgap/catalog/sinks.py` | sink 表と `SLOTS`（7 kind。核）、`PATH_DOMAIN_SLOTS`（付録） | [第 13 章](ch13.md) |
| `authgap/catalog/statements.py` | SQL 文・HTTP メソッド・ファイル書き込みの分類（核。D56） | [第 17 章](ch17.md) |
| `authgap/catalog/transfers.py` | 値の変換の一覧 | [第 14 章](ch14.md) |
| `authgap/catalog/validators.py` | validator の形・weak 理由・格下げ属性などの語彙（付録） | [第 8 章](ch08.md) |
| `authgap/ir.py` | 共通の型と語彙。`MAX_DEPTH = 4`、`VAL_OPAQUE_REASONS`（8 語。核）、ゲート側の語彙（付録） | 第 14・15 章 |
| `authgap/val/engine.py` | val エンジン（値の追跡と呼び出しの解決） | 第 14・15 章 |
| `authgap/dparse.py` | 宣言の読み取り（`D_kind`）と、local の網の定義 | 第 10・16 章 |
| `authgap/verdict.py` | 矛・不の注記（`contradiction:`・`contradiction_reason:`・`contradiction_unknown:`）を付ける | 第 17・18 章 |
| `authgap/effects.py` | 効果の検出（sink の当てはめ、`sub_kind`） | [第 13 章](ch13.md) |
| `authgap/gate.py`・`authgap/dominance.py`・`authgap/cfgbuild.py` | ゲートと支配の判定（付録の仕組み） | [第 23 章](ch23.md) |
| `authgap/report.py` | manifest の書き出しと仕様書の指紋（`fingerprint()`） | 第 18・33 章 |
| `authgap/runner.py` | 走査の実行（時間上限 `max_tree_seconds`、前処理の打ち切り） | [第 27 章](ch27.md) |
| `docs/fingerprint.json` | 凍結の記録（結合 sha256 35606ba9…、根拠の run は `scan_v2_run24`）。`freeze.tag` の欄は `analyzer-freeze-2` と書いてあるが正しくは `analyzer-freeze-3` | 第 22・33・36 章 |

表の読み方: 判定では、解析器のファイルを開く必要はふつうありません。解析器の誤りを疑って確かめたいときだけ、該当のファイルを読みます。**読んでも直しません**（凍結。誤りは `docs/open_questions.md` に限界として書く）。

---

<a id="ab-6"></a>
## B.5 道具 `scripts/`

| ファイル | 中身 | 最終評価での使い方 | 本文 |
|---|---|---|---|
| `scripts/sample_population_v2.py` | 抽出と pin（`--exclude`・`--prefix`） | 段階 3（抽出の書き方は未決。[第 46 章](ch46.md) (9)） | [第 47 章](ch47.md) |
| `scripts/fetch_corpus.py` | pin の SHA どおりに取得する | 段階 4 | [第 47 章](ch47.md) |
| `scripts/check_population_v2.py` | 取得後の条件 | 段階 4 | [第 47 章](ch47.md) |
| `scripts/scan_v2.py` | 母集団をまとめて走査する（`--require-fingerprint`） | 段階 5（1 回だけ） | 第 18・47 章 |
| `scripts/contradiction_by_decl.py` | 宣言ごとの矛 / 不と感度分析 | 段階 6・8 | 第 17・55 章 |
| `scripts/r_malformed.py` | `r_malformed` の集計（§2.11） | 段階 8 | 第 16・55 章 |
| `scripts/depth_sensitivity.py` | 深さの感度分析の集計 | 段階 5（深さ 3・5 の件数） | 第 27・55 章 |
| `scripts/v3_judge_sample.py`・`scripts/v3_miss_sample.py` | v3 の矛・見落としの抜き取り（一様に 60 件・30 件） | 新しい抜き取りの道具の土台 | 第 34・47 章 |
| `scripts/compare_scans.py`・`scripts/diff_effects.py`・`scripts/lost_units.py` | 2 つの run の突き合わせ | 最終評価では使わない（取り直さない） | [第 23 章](ch23.md) |
| `scripts/two_sided.py` | 較正対の両側比較 | — | [第 31 章](ch31.md) |
| `scripts/codeql_fair.py` | 入口を揃えた CodeQL との比較 | 論文の比較（D71） | [第 26 章](ch26.md) |
| `scripts/freeze_analyzer.py` | 凍結の記録（`docs/fingerprint.json`）を書く | — | [第 33 章](ch33.md) |
| `scripts/check_gates.py`・`scripts/mutation_test.py` | B3a 8/8・B3b 15/15 と、変異試験 | 段階 2（環境の試験） | 第 23・47 章 |

---

<a id="ab-7"></a>
## B.6 走査の結果と原ソース

| ファイル | 中身 | いつ開くか | 本文 |
|---|---|---|---|
| `corpus/` | 取得した木（原ソース）。git では追わない。2026-10-01 の時点で 512 項目（較正対・v2・v3・v4 など。v4 は `v4-` で始まる 99 項目） | 判定で原ソースを読むとき（最終評価の木は段階 4 で取得） | 第 11・47 章 |
| `evidence/scan_v2_run24/` | 最終凍結（`analyzer-freeze-3`）の根拠の run（v2） | — | 第 36・40 章 |
| `evidence/scan_v2_run20/` | 添削の前の v2 の run | — | 第 36・40 章 |
| `evidence/scan_v2_v4_run1/` | v4 の走査（88 木）。`summary.json`・`contradictions.json` は git にあり、木ごとの manifest（`v4-*.json`）は追わない | 判定の練習で manifest を開く | 第 19・37・54 章 |
| `evidence/scan_v2_v3_run1/`・`evidence/scan_v2_v3_run2/` | v3 の走査 | — | [第 34 章](ch34.md) |
| `evidence/scan_v2_depth{3,4,5}_sens/` | 深さの感度分析（D53） | — | [第 27 章](ch27.md) |
| `evidence/review/` | 添削の所見・検証・敵対的レビューの記録 | — | [第 36 章](ch36.md) |
| `docs/scan_v2_run<N>_diff.md` | 取り直しの突き合わせ（run5〜run24 のうち 15 本） | — | [第 23 章](ch23.md) |
| `docs/contradiction_by_decl.md` | 宣言ごとの矛 / 不と感度分析（最新の run） | — | 第 17・40 章 |
| `docs/depth_sensitivity.md` | 深さの感度分析の表 | — | [第 27 章](ch27.md) |

---

<a id="ab-8"></a>
## B.7 テストと期待値

| ファイル | 中身 | 本文 |
|---|---|---|
| `tests/` | テスト（`.py` のファイル 53 本。反例のテストを含む）。`.venv/bin/python -m pytest tests/ -q` | [第 23 章](ch23.md) |
| `fixtures/gates/`・`fixtures/dominance_mutants/` | B3b（付録 G の 15 問）と B3a（支配の 8 つの変異）の入力と期待値 | [第 23 章](ch23.md) |
| `fixtures/val/` | val の受け入れ fixture F1〜F10 と期待値（採点器より先にコミット） | [第 14 章](ch14.md) |
| `fixtures/entries/`・`fixtures/destructive_sinks/`・`fixtures/dispatch_join/`・`fixtures/semgrep_boundary/` | 入口・破壊的な sink・ディスパッチ・Semgrep の境界の fixture | 第 12・13 章 |

---

<a id="ab-9"></a>
## B.8 調査と比較の文書

| ファイル | 中身 | 本文 |
|---|---|---|
| `docs/incidental_writes_practice.md` | 裏方の書き込みの実世界の扱いの調査（確かさの印 [確認]・[agent]・[未確認] の定義もここ） | 第 4・43 章 |
| `docs/llm_judgment_survey.md` | 判定に LLM を混ぜる研究の調査（7 体の agent。候補 0〜9 と付記） | [第 26 章](ch26.md) |
| `docs/implementation_base_survey.md` | 30 余りの研究の実装の土台の調査（D71 の訂正の根拠） | [第 26 章](ch26.md) |
| `docs/related_work.md` | 先行研究（HintLint・AgentFlow・ReactAppScan など）を読んだ結果。「まだ書いていないもの」に比較の作業が残る | 第 6・26 章 |
| `docs/contradiction_matrix.md` | 矛盾関係の表（D41。原理の文書の前身） | [第 28 章](ch28.md) |
| `docs/catalog_map.md` | 事前定義の地図（核と付録。D37） | [第 8 章](ch08.md) |
| `docs/annotations_official_survey.md` | 宣言（ToolAnnotations）の公式の位置づけと、ほかの種類の宣言の調査（2026-10-02） | [付録 G](appendix-g.md) |
| `evidence/annotations_usage/` | 宣言の使われ方の調査の元データ（`sources.json`: 資料 820 件・記載が無かったページ・届かなかったページ、`recheck.json`: 2026-10-02 の照らし合わせ直し） | [付録 G](appendix-g.md) |
| `scripts/verify_quote.py` | 引用が URL の原文に本当にあるかを文字列で照らし合わせ、場所（見出し・行・ページ）を返す | [付録 G](appendix-g.md) |
| `scripts/build_annotations_appendix.py` | 調査の元データから付録 G-1〜G-13 のカードと表紙の集計を作る（手で直さない） | [付録 G](appendix-g.md) |

---

<a id="ab-10"></a>
## B.9 教科書の原稿

| ファイル | 中身 | 本文 |
|---|---|---|
| `docs/textbook/` | この本（教科書 第 4 版。1 章 1 ファイル。`README.md` が表紙と目次） | — |
| `docs/textbook_v3.md` | 教科書 第 3 版（2,736 行、2026-09-29）。原典の「教科書 第 N 章」はこの版の番号 | 前付けの対応表 |

---

<a id="ab-11"></a>
## B.10 最終評価で新しく作るファイル（2026-10-01 の時点では無い）

| ファイル（予定の名前） | 中身 | いつ作るか | 本文 |
|---|---|---|---|
| `docs/final_judging_guide.md` | 判定の手引きの正本（下書きを承認して移す） | 段階 1（§2.12 と同じコミットで封をする） | 第 22・47 章 |
| `docs/preregistration.md` の §2.12 | 最終評価の事前登録の正本 | 段階 1 | 第 22・47 章 |
| `scripts/show_target.py`（例の名前） | 1 組の情報を manifest から 1 画面に出す道具（手順書 6.5 節に最小の形） | 段階 2 | 第 19・47 章 |
| 矛・見落とし・不の抜き取りの道具 | 宣言ごとに最大 200 木・1 木 3 件、200 木・1 木 1 件、D1・D2 で各 50 木・1 木 1 組 | 段階 2 | [第 47 章](ch47.md) |
| 判定表の雛形（CSV） | 抜き取りの出力に、空の判定の欄を足したもの | 段階 2・6 | 第 19・48 章 |
| 木を単位にした集計と bootstrap の道具、中身の重複の除去の道具 | 手順書 第 23 節の計算、D70 の 6 | 段階 2 | 第 39・47・55 章 |
| `evidence/population_final/` | 最終評価の標本・判定の記録（`.gitignore` に例外を足して追跡する） | 段階 3 以降 | [第 47 章](ch47.md) |
| `evidence/scan_v2_final_run1/` | 最終評価の走査の結果（木ごとの manifest は追わない） | 段階 5 | [第 47 章](ch47.md) |

表の読み方: どれも手順書が名前や中身を示している予定のファイルで、まだ存在しません。名前は手順書の例に従いますが、作るときに変えてもかまいません（変えたら記録に書く）。

---

[← 付録 A 用語集（登場順）](appendix-a.md) ｜ [目次](README.md) ｜ [付録 C 決定の年表 →](appendix-c.md)
