# 手検証の手引き

**この文書の目的**: 論文に書く数値と主張を、著者が自分の手で確かめられるようにする。
各節は「何を確かめるか」「どのコマンドで再現するか」「何と突き合わせるか」
「これが落ちたら何が言えなくなるか」の 4 つを持つ。

最終更新 2026-09-09。仕様の正本は `../AUTHGAP_BRIEF_v3.md`。

---

## 0. 準備

```bash
uv venv .venv --python 3.10
uv pip install --python .venv/bin/python -r requirements.txt
```

以後のコマンドは repo 直下で `.venv/bin/python` を使う。

**解析中核は標準ライブラリ `ast` のみ。** 解析対象の木に venv も型環境も作らない。
LLM は判定経路に一切入らない（`authgap/` に API 呼び出しは無い。`grep -r "openai\|anthropic\|http" authgap/` で確かめられる）。

---

## 1. 受け入れ条件（§2.5.6）— まずここを通す

### 1.1 B3a: 支配のみを問う 8 mutant を 8/8

```bash
.venv/bin/python scripts/check_gates.py
```

**確かめること**: 出力の `B3a 支配 mutant : 8/8`。8 件はどれも
「支配と判定してはならない形」であり、1 件でも `DOM` と出たら不合格。
m6 は `parse_failure` 行、m7 は `TRUNCATED` + `OPAQUE(cfg_cap)` 行が
出ることまで含めて合格条件である。

**手で読むもの**: `fixtures/dominance_mutants/m*.py` の docstring。
各 mutant が突く穴と、それが前身のどの欠陥に対応するかが書いてある。

### 1.2 B3b: 付録 G の G1–G15 を 3 つ組で 15/15

同じコマンドの `B3b 付録 G : 15/15`。一致を要求するのは
`(verdict, reason クラス, witness 行番号)` の 3 つ組であって真偽値ではない。

**期待値の出所を必ず自分で確かめること**:

- `fixtures/gates/expected.json` は `scripts/gen_expected.py` が生成する。
- 生成の入力は 2 つだけ — (a) `scripts/gen_expected.py` 内の手書き表
  （出所は仕様書 §2.5 付録 G の表）、(b) fixture 中の `# EFFECT` / `# WITNESS`
  マーカー（人が置いた位置）。
- **どちらも解析器の出力ではない。** `git log --oneline -- fixtures/gates/expected.json`
  で、期待値のコミットが採点器 `authgap/gate.py` のコミットより**前**にあることを
  確かめられる（§2.5.6 の要求順序）。

**1 件だけ、仕様書に無い値を私が導出した**: G12 の reason。付録 G は `NODOM` と
しか書いておらず reason クラスを書いていない。`deny_reaches_effect` を pin した
根拠は `expected.json` の `reason_note` にある。**ここは学生が追認すること。**

### 1.3 実装変異 15 件の生存 ≤ 2

```bash
.venv/bin/python scripts/mutation_test.py
```

**確かめること**: `生存 1/15`。前身の比較値は「56 テスト時代に 15 件中 9〜10 件が
生存」で、HEAD での生存数は未知（監査が変異試験を再実施していない）。

**生存 1 件（`no_finally_copies`）は隠していない。** 理由は
`docs/open_questions.md` の Q3 に書いた — `(G-i)∧(G-ii)` が先に同じ誤りを
捕まえるので、付録 G の 15 件では `finally` 複製の有無が 3 つ組を変えない。
生存数は**付録 G と支配 mutant の fixture テストだけ**で数える（§2.5.6 の定義）。
fixture 外の単体テストを足して見かけの生存数を下げてはならない。

### 1.4 全テスト

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check .
```

---

## 2. 両側条件（§6 T1）— head-to-head の主指標

### 2.1 コーパスを pin する

```bash
.venv/bin/python scripts/fetch_corpus.py --spec docs/corpus_spec.json
cat docs/frame.csv
```

**確かめること**: `docs/frame.csv` の `commit_sha` 列が `ref` 列と前方一致する。
取得スクリプトは一致しなければ**失敗として記録する**（`docs/fetch_failures.md`）。

> この検査は飾りではない。最初の実装は浅い fetch が SHA を掴めずに
> 黙って default branch へ落ち、4 本すべてが同じ SHA になった。
> **pin が外れたことに気づかないまま「両側で差が出なかった」と書くのが
> 最悪の失敗であり、それを止めるための検査である。**

### 2.2 修正コミットを自分で特定する

**脆弱性 DB の fix commit 欄は使わない**（§9-1。誤記載の実例が 4 件確定している）。

```bash
C=corpus/_cache/modelcontextprotocol__servers
git -C $C log -S'relative_to' --oneline -- src/git      # A1
git -C $C diff 9e5d5b8e a37158bc -- src/git             # A1 の diff を目視
git -C $C diff d9c45477 9e5d5b8e -- src/git             # A2 の diff を目視
```

**確かめること**: 修正の実体（`validate_repo_path` の新設 / `startswith('-')` +
`rev_parse` の追加）が diff に見えること。`git log --grep='Merge commit from fork'`
が triage の第一手として効くこと（§6 T1.3-4(a)。ただしプロジェクト依存）。

### 2.3 両側を採点する

```bash
.venv/bin/python scripts/two_sided.py --spec docs/corpus_spec.json \
    --json evidence/w0/two_sided.json
```

**確かめること**:

- 効果サイトの同一性が `(kind, site, slot, witness_chain)` で取られていること。
  **呼び出し経路を落とすと変化が消える** — `git.Git.diff` は `git_diff` /
  `git_diff_staged` / `git_diff_unstaged` の 3 経路から到達し、検証子が付くのは
  `git_diff` だけである。経路を落とすと検証の無い兄弟経路が最弱として採られ、
  A2 の `git_diff` の変化が見えなくなる（実際に一度そうなった）。
- **verdict-clearing 数が必ず併記されていること**（§6 T1.1 の副次指標）。
  タプル変化のみで通過した対と区別せずに報告すると「修正を検出した」と誤読される。

### 2.4 現時点で一次確認できている対（7 対 / 4 プロジェクト）

| 対 | プロジェクト | 両側通過 | 変化した座標 | clearing 厳密 | clearing INJECT |
|---|---|---|---|---|---|
| A1 | mcp-server-git | ○ | `cwd`: 検証なし → `strong-path`（8 経路） | × | × |
| A2 | mcp-server-git | ○ | `argv[*]`: 検証なし → `strong-token`（2 経路） | × | × |
| A3 | mcp-server-git | ○ | `FS_WRITE(index.add)` 消滅 + `argv[*]` 主体 OP → MODEL | × | × |
| A4 | mcp-server-git | ○ | `argv[*]`: 検証なし → `strong-path` | × | **○** |
| A5 | AutoGPT | ○ | `exec_mode`: `True` → `config-conditional`（argv 行が増える） | × | × |
| A9+A10 | PraisonAI | ○ | `req_occ` MODEL → **USER**／`path`: `weak(no_symlink_resolution)` → `strong-path` | × | × |
| A18 | langroid | ○ | `sql`: 検証なし → `unknown`（sqlglot 文型 allowlist） | × | × |

**両側通過 7/7。verdict-clearing は厳密 0/7、INJECT 座標のみ 1/7。**

§6 T1.5 の合格条件との対応:

- (i) 修正コミット単位で **≥ 6 対** → **7 対で満たす**（A9 と A10 は同一修正
  コミットなので 1 対として数えている）
- (iii) **≥ 4 プロジェクト** → **4 プロジェクトで満たす**
  （mcp-server-git / AutoGPT / PraisonAI / langroid）
- PraisonAI 由来は 1 対なので上限 3 を満たす
- (ii) Semgrep / Pysa との突き合わせは**未実施**。§6 T1.5 の 3 条件のうち
  これだけが残っている

仕様書の期待タプルと**完全に一致した**のは 2 対:

- **A10**: `weak(no_symlink_resolution)` → `strong-path`
- **A5**: `(weak(first_token), shell=True)` → `(weak(first_token), argv 行が増える)`。
  修正側の `shell` は素の `False` ではなく `config-conditional` である
  （`validate_command` が `shell_command_control` に応じて `allow_shell` を返す）。
  §6 T1.1 が F3 で要求する「モードが確定しないときは 2 行出す」がここで働き、
  `shell_string` 行と `argv` 行の両方が出る。

**verdict-clearing が厳密版で 0 になる理由を本文に書くこと。**
`GAP_SELECT` は「モデルがそのツールを呼ぶかを決めており、承認割り込みも宣言も
無い」ことを言うので、**値検証を足しても消えない**。消えるのは承認割り込みを
足した対だけである。A9 は `@require_approval` で `req_occ` を USER へ上げるが、
同じ木の別経路に GAP が残るので対単位ではまだ clear にならない。
A5 は修正版も `weak(first_token)` のままなので規則 W により GAP_INJECT が残る
（仕様書が「修正版も weak のまま」と書いているとおり）。
**片方の数だけを書くと、SELECT 座標が常に残ることを隠すか、値検証の効果を
見落とすかのどちらかになる。**

再現:

```bash
.venv/bin/python scripts/fetch_corpus.py --spec docs/corpus_spec.json
.venv/bin/python scripts/two_sided.py --spec docs/corpus_spec.json \
    --json evidence/w0/two_sided.json
```

**残り 18 行の対は `docs/cve_triage.csv` で `verified_by_me = none`、すなわち
仕様書からの転記であって未検証である。論文に数として書く前に、2.1〜2.3 を
その対に対して実行すること。**

### 2.5 仕様書と食い違った 2 点（**論文に書く前に決める**）

一次確認の結果、仕様書 §6 T1.2 の期待タプルの**脆弱側**が 2 件とも誤っていた。

| 対 | 仕様書の脆弱側 | 一次確認した実際 | 影響 |
|---|---|---|---|
| A1 | `weak(prefix_no_canon)` | **検証子が 1 つも無い**（`Path(arguments["repo_path"])` が直接 `git.Repo` へ） | 消滅理由は `normalisation-add` 単独ではなく `validator-add`。両側判別可能性は成立するので T1 の算入数は変わらない |
| A2 | `weak(no_dash_reject)` | **検証子が 1 つも無い** | 同上。加えて仕様書は `git_checkout` しか挙げていないが `git_diff` も同じ修正を受けている |

`docs/cve_triage.csv` は `expected_tuple_change`（訂正後）と
`spec_expected_tuple_change`（仕様書の値）を**両方**持つ。
**仕様書の値を黙って書き換えていない。**

### 2.6 Semgrep OSS baseline との対ごと突き合わせ（§6 T1.5 (ii)）

```bash
.venv/bin/semgrep --config baselines/semgrep_authgap_source.yaml \
    --json --quiet fixtures/semgrep_boundary/   # §8-4 の機能境界の実測
.venv/bin/python scripts/baseline_semgrep.py --json evidence/w0/baseline_semgrep.json
```

**まず機能境界を自分で実測する**（§8-4）。`fixtures/semgrep_boundary/` は
2 本だけで、`intra.py`（source と sink が同一関数）は報告され、
`inter.py`（別関数）は**報告されない**。Semgrep CE が手続き内 taint のみで
あることの、自分の手による確認である。

結果:

| 対 | AuthGap | Semgrep（消滅あり） | 備考 |
|---|---|---|---|
| A1 A2 A3 A4 | ○ | × | 所見が両側で同一 |
| A5 | ○ | × | 所見が両側で同一 |
| A9+A10 | ○ | × | 修正側で所見が**増えた**だけ |
| A18 | ○ | × | 所見が両側で同一 |

**AuthGap 7/7、Semgrep 0/7。**

「変化あり」（増減どちらでも通過とする baseline に最も有利な読み方）でも
1/7 で、その 1 件（A9）は**修正でコードが増えて所見が増えた**だけである。
**増減を分けずに報告すると baseline が修正を検出したように見える。**

なぜ Semgrep が修正版を clear できないかは A1 で目に見える。Semgrep は
`git.Repo(repo_path)` の行を**両側とも**報告する。修正版が入れた
`validate_repo_path` は**別関数**なので、手続き内 taint では見えない。
**これが §1.5.6 の軸 1（修正版側の精度）そのものである。**

公平性のために baseline は次まで強化してある。**弱い baseline は
AuthGap を実際より良く見せる。**

- 低レベル MCP ハンドラの `arguments` も source にした
- GitPython の proxy 形（`$R.git.$M(...)` / `$R.index.add(...)`）を sink に足した
- 過剰一致していた `$S.run(...)`（`subprocess.run` にも当たる）は外した。
  **受け手の型を絞れないので過剰一致か取りこぼしかのどちらかになる** — これ自体が
  比較点であり、AuthGap は proxy カタログで受け手型と slot 束縛を持つ

未実施: **Pysa ModelQuery**。pyre 環境の構築が要る（§6 は「D13 までに環境が
立つ repo が 0 なら baseline から落として『pyre 依存 baseline は環境コストにより
不成立』と報告する」と書いている）。

副産物: PraisonAI の 2 ファイルを semgrep が parse できない
（`reproduce_issue_878_simple.py` / `test_all_optimizations.py`）。
**AuthGap は同じ木で parse 失敗 5 件を記録しており、どちらも黙って落として
いない。** 件数が違うのは対象ファイル集合と parser の差である。

---

## 3. F0a（床）— 支配判定に依存しない測定

```bash
.venv/bin/python -m authgap probe corpus/A1__fixed --population mcp_server
```

**確かめること**（§5.1 が列挙する全キーが出ること）:

- `traced_ratio` が `null` であること。**A5 の run では `null` とし、その run には
  二度と書き込まない。** traced 率は B1 完了後に**新しい `run_id` で probe を
  再実行**して得る（`--with-traced-ratio`）。
- `resolution` と `resolution_by_cause` の合計が合うこと。opaque を clean に
  潰していないこと。
- `parse_failures` と `truncations` が空でなければ、その件数が母集団の分母に
  反映されていること。**黙って落としていないこと。**
- `dep_pin_resolvable` が `>=` だけの指定を `lower_bound_only` に分類し、
  `exact` に混ぜていないこと（Def 6 の版の確定規則 2）。

**分母の定義を必ず添えること**（§10）:

- `in_tree_resolution_ratio` = `resolved / (resolved + opaque + remote)`（効果サイト）
- `opaque_ratio_primary_slots` = 主 slot 7 種に限定した
  `opaque / (resolved + opaque)`。**`remote` は分母に入れない。**
  粗い分母（全 slot）の値も `opaque_ratio_all_slots` に併記される。

### 3.1 野外標本での F0a（§6 標本設計 / §10 の A5 関門）

```bash
.venv/bin/python scripts/fetch_frame.py                  # MCP サーバ母集団（2299 件）
.venv/bin/python scripts/fetch_frame.py --method toolpkg # ツールパッケージ母集団（2722 件）
.venv/bin/python scripts/sample_corpus.py               # seed 20260909（動かさない）
.venv/bin/python scripts/fetch_corpus.py --spec docs/corpus_sample.json --jobs 6
.venv/bin/python -u scripts/f0a.py --sample docs/corpus_sample.json
```

**確かめること:**

1. **標本が seed で再現すること。** `sample_corpus.py` を再実行して
   `docs/corpus_sample.json` の差分が出ないこと（`sampled_at` は `sampling.md` にしか無い）。
2. **pin が SHA で一致していること。** `docs/frame.csv` の `commit_sha` と
   `evidence/f0a/trees.jsonl` の `commit_sha` が木ごとに一致すること。
3. **母集団ごとの上限は「取得できた木を抽出順に先頭から」数えている。**
   `trees.jsonl` の `status=missing` は枠を消費せず繰り上げ、
   `status=analysis_failed` は繰り上げずに残る（道具の失敗を隠さない）。
4. **分母を 2 通り見る。** 効果行は呼び出し経路ごとに複製されるので、
   `in_tree_resolution_ratio`（行単位。実装どおり）と
   `in_tree_resolution_ratio_sites`（(木, relpath, lineno, kind) で重複除去。
   §1 の「効果サイト」の文言どおり）の両方が出る。**差が大きい母集団では
   少数のサイトに行が集中している**ので、論文にはどちらの分母かを必ず書く。
5. **`run_meta.analyzer_commit` を控える。** 野外データを見た後で解析器を直した
   場合は run を分けて両方を報告する（`docs/decisions.md` D14）。
6. **1 件ずつ辿る。** `evidence/f0a/units.jsonl` はユニット 1 行で、効果ごとに
   `relpath:lineno`、`resolution` とその理由、slot ごとの確度を持つ。
   `scripts/sample_f0a_checks.py` が seed 20260914 で 6 層（opaque / resolved の
   効果サイト、危険効果あり、効果なし、validator 形状あり、`D_kind` あり）から
   検証標本を抜くので、その各件を原ソース（`corpus/<木>/<relpath>`）で読み、
   解析器の主張が正しいかを確かめる。**機械による事前点検の分類は
   `evidence/f0a/check_results.json` にあるが、それは C2 のラベルではない。**

---

## 4. 決定論（§5.2）

```bash
.venv/bin/python -m authgap scan corpus/A1__fixed --determinism 3 > /dev/null
```

**確かめること**: `決定論: 3 回バイト一致`。比較は manifest から volatile ブロック
（`run_meta`: 実行時刻・経過時間・絶対パス）を除き、キーをソートして再直列化した
うえでのバイト一致（§5.2 の定義）。

`authgap/report.py` の `strip_volatile` / `determinism_signature` が実装。
**volatile がトップレベルの `run_meta` に閉じ込められていること**を目で確かめる。

---

## 5. 語彙の凍結が実装レベルで守られていること

```bash
.venv/bin/python -m pytest tests/test_vocabulary.py -q
.venv/bin/python -m authgap fingerprint
```

**確かめること**:

- validator 形状 **12 語**、weak 理由 **22 語**、ゲート側 OPAQUE 8 語、
  NODOM 4 語、val 側 opaque 8 語。**語彙外の理由は構築時に例外になる**
  （`DomResult(DomKind.NODOM, "made_up_reason")` が `ValueError`）。
- 仕様書は 11 語 / 19 語と書く。**月 6 の凍結前に拡張した**（`docs/decisions.md` D1）。
  改訂の日付と理由は `VOCABULARY_REVISIONS` にあり、テストで空でないことを固定
  している。
- `self_granted` が weak 理由語彙に**入っていない**こと（格下げ属性である）。
- 指紋の `sha256` が sink 表・R1/R2 カタログ・ゲート語彙・執行表の 4 つに
  分かれていること。月 10 の凍結ではこの値をコミットしてタグを打つ。

F7 が挙げる `absolute_only` / `existence_only` は Def 5 の 19 語に無かったので
**足した**。A18 で当たった「正規化後の文型 allowlist」にも語が無かったので
`statement_type_only` を足した。いずれも `docs/decisions.md` D1。

---

## 6. 出力を原ソースに当てて照合する（§7.1 の検証 (b)）

```bash
.venv/bin/python -m authgap scan corpus/A1__fixed --sarif /tmp/a1.sarif > /tmp/a1.json
```

**手順**:

1. `/tmp/a1.json` の `units[].effects[]` から無作為に 20 行取る。
2. 各行の `relpath` と `lineno` を開き、`kind` と `site` が合っているか見る。
3. `slots` の `prin` が正しいか見る。`MODEL` はツール引数（R2）か LLM 戻り値（R1）から
   来ていなければならない。`roots` にその出所が入っている。
4. `witness_chain` が入口からその効果までの呼び出し経路になっているか見る。
5. `entry_lineno` が**入口ユニットの中の呼び出し行**を指しているか見る
   （`lineno` は効果そのものの行で、別ファイルでありうる）。

`docs/verification_log.csv` に `item, date, hours, activity(a|b|c|d)` を日次で
記録する（§7.1 の測定手続き）。

---

## 7. この系が今できないこと（限界。**論文の限界節にそのまま書ける**）

| 事項 | 状態 | 出所 |
|---|---|---|
| D_dom パーサ | **書いていない。** `r_dom = 0` として報告する | Def 6 の実装条件。前測で母集団 0（MCP サーバ 0/141、ツールパッケージ 0/191） |
| strong-eval | **実装していない**（既定）。`code_text` / `sql` 位置はゲートの真偽値のみ | §7.4 切り詰め順序の (0) |
| 文脈感度 | サマリは記憶化により**文脈非依存**。ゲート条件が呼び出し元引数に依存する形は捉えられない | §2.6 の限界節。該当形は `opaque(context)` として出力し **clean にしない** |
| `remote` の判定 | 受け手型が `REMOTE_RECEIVER_TYPES`（3 型）のときだけ。**狭く取っている** | `authgap/effects.py`。広げるときは F0c(iii) の定義も同時に直す |
| 呼び出し元の完全性 | 要求しない。カタログ外の呼び出し元からのみ到達する効果は**取り落とす** | Def 4 の残余仮定。測定点は traced/assumed 比率と F0c(i) |
| セレクタの運用定義 | 暫定。val の `Value.roots` に置き換える予定 | `docs/open_questions.md` Q4 |
| §8 項目 7（in-tree 露出宣言を D_op に含めるか） | **未凍結。** 既定では含めない | `docs/open_questions.md` Q6 |

---

## 8. 「これが落ちたら何が言えなくなるか」の対応表

| 落ちるもの | 言えなくなること | 仕様書の分岐 |
|---|---|---|
| B3a が 8/8 でない | 支配判定に依存する主張すべて | §10: B3 を打ち切り F0a + F0c + T1 の対ごと表を代替主張に |
| B3b が 15/15 でない | ゲート等級の主張 | §10: 測定研究へ縮小。語彙の凍結は月 6 に済んでいるので凍結の変更は意味しない |
| 実装変異の生存 > 2 | 「テストが性質を守っている」という主張 | §2.5.6 |
| 両側通過が 6 対未満 | head-to-head の主指標 | §10 D12: 予備候補を triage。なお足りなければ F0 測定研究を主結果に |
| 決定論 3 回一致が崩れる | 「LLM を判定入力に使わず決定的」という主張の半分 | §5.2 |
| `in_tree_resolution_ratio` < 50% | 効果サイトの解決率 | §10 A5 後: 母集団をツールパッケージへ切り替える |
| `opaque_ratio_primary_slots` > 40% | opaque 予算 | §10 C1 後。**閾値 40% は動かさない。動かすのは分母の定義だけ** |
| T3-app の traced 率 < 20% | SELECT の野外評価 | §10 B1 後: fixture + ケーススタディのみの構造的主張に格下げ。**この条項は撤回しない** |
| 野外支配発火率が (a)(b) とも 5% 未満 | strong 3 系統・false-strong 率・規則 W の比率 | §10 C1 後: fixture・T1・T2 に限定 |
