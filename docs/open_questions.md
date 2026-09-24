# 学生の入力が要る事項

**実装側で判断できたものは `docs/decisions.md` へ移した。** ここに残るのは
「学生本人しか知らない情報が要る」か「外部の承認が要る」ものだけである。

最終更新 2026-09-20（O9 を追加、O3 / O4 に D24 の決定を注記）。

---

## O2. 第二ラベラーの候補

- **要る情報**: 候補 2 名の氏名・連絡先、裁定者（指導教員でよいか）。
- **なぜ要るか**: §8-2 が書面確約を要求し、§11-7 は「成功分岐（T3）と null 分岐
  （κ）の両方の critical path にあり代替が無い」と書いている。
- **暫定**: 確保できない場合の縮退（30 ツールに縮小 + 指導教員による裁定標本
  20 行 + test-retest で κ を代替 + inter-rater に依存する主張を全部落とす）を
  既定として事前登録する、という方針だけを置いてある。**依頼文は未送信。**

## O3. 開示プロトコル（大学の規程）

**2026-09-20 学生の決定（D24）: 指導教員の承認は不要。** 承認経路
（研究科 / 情報セキュリティ部門 / 産学連携）の部分は本問から外す。
**影響を受けるリポジトリへの開示そのもの**（`docs/disclosure.md` の内容と、
実 repo の file:line を含む evidence を公開 remote に置くことの扱い）は
承認とは別の問題なので残す。

- **要る情報**: 承認経路（研究科 / 情報セキュリティ部門 / 産学連携）と提出様式。
- **なぜ要るか**: §8-3。**これだけが C1（wild run）をブロックする。**
  建設はブロックしない。
- **暫定**: `docs/disclosure.md` は未作成。90 日 CVD の一般形で v1 を書くことは
  できるが、承認欄は空のままになる。

## O4. リポジトリの公開設定と push

**2026-09-20 学生の決定（D24）: 承認は不要。** また本問の「push していない」は
実態と食い違っている（`origin/main` に evidence 40 ファイルが既に載っている。
審査パネルの指摘、本人が `git ls-files evidence` で確認）。残るのは
「公開のままにするか、evidence を仮名化するか」だけである。

- **要る情報**: `https://github.com/s1300105/auth_gap.git` へ push してよいか、
  public か private か。
- **なぜ要るか**: `docs/cve_triage.csv` は脆弱版 ref を pin する。§8-3 の
  開示プロトコル承認前に public にすると、開示の時計と整合しない。
- **暫定**: **push していない。** コミットはローカルにだけある（数は `git rev-list --count HEAD`）。
  推奨は「private で作成し、C1（開示の 90 日時計の起点）まで private を維持」。

## O5. 低レベル MCP ハンドラと annotation の join（Def 6 に規則が無い）— **解決（prereg §2.9、D29 の帰結として実装）**

- **2026-09-20 追記（D28）**: 97 木で `dispatch_names` による join を探索的に入れても、
  明示 hint を持つユニットは 1/2533 のまま（`evidence/decl_census_run6/join_probe.json`）。
  この枠では O5 を直しても r_D は動かない。優先度を下げる。

- **状況**: Def 6 の join 規則は「エントリとは**ツール名文字列の完全一致**で join」。
  低レベル MCP（`@server.call_tool()`）のユニットは 1 つのハンドラが複数ツールを
  名前分岐で捌くので、ユニットに 1 つのツール名が無い（`tool_name=None`、
  `dispatch_names` に複数）。野外では `mastermind` の `workbench_read_mcp` が
  `list_tools` で `Tool(name=..., annotations=ToolAnnotations(readOnlyHint=True))` を
  返しているが、どのユニットにも結び付かない（`docs/f0a_checks.md` の annotation 節）。
- **決め方の候補**:
  (a) 仕様どおり「未 join 行」として報告するだけ（現状）。
  (b) ハンドラの分岐ごとにユニットを分け、各分岐をツール名で join する。
  (c) ハンドラ単位のまま、全 dispatch 名の上界の結び（最も弱い宣言。1 つでも無ければ `⊥`）。
- **なぜ実装側で決めないか**: (b) はユニットの定義（§5.1 の unit id、§3 の交差行の
  数え方）を変える。(c) は Def 6 に無い合成規則を足す。**どちらも F0a の標本を
  見た後に足すと測定集合で規則を選ぶことになる。**
- **暫定**: (a)。r_kind の分子に入らない。低レベル MCP の未 join 行の件数を報告する。

## O6. D19 で止めた後に残る既知の欠陥 K7（別名つき from-import）を直して run 7 を取るか

- **状況**: D19（レビューと修正の繰り返しを止める条件。4 回目のレビューの**前**に固定した）により、
  5 回目のレビューで確認された欠陥は直さずに報告することにした（`docs/decisions.md` D19 の「結果」）。
  そのうち **K7**（`from .net import fetch_url as http_get; http_get(url)` で木内の関数へ降りず、
  被呼び出しの効果行が全部消える）は、最初の解析器からある効果行の消失で、**F0a 標本の 32 木に
  構文上の候補がある**（上限値 693 箇所。到達は未確認）。run 6 で効果 0 件になっているユニットが
  実際にある（w-datawhalechina__video-devour の 5 ユニットすべてなど）。
- **決め方の候補**:
  (a) D19 どおり直さない。run 6 を K1〜K7 を明記して報告し、K7 の影響は感度分析（関門の数字ではない）で示す。
  (b) D19 を破って K7 を直し（テストは `tests/test_f0a_defects.py` 15 節にすでにある）、run 7 を報告に使う。
      **破ると決めたのが 5 回目のレビューと感度分析の結果を見た後である**ことを `docs/preregistration.md` の
      逸脱として書く。直した差分にはまたレビューが要り、止める条件を新たに決める必要がある。
  (c) (b) に加えて K1（改訂 5 の退行。標本の候補 0 件）も直す。
- **なぜ実装側で決めないか**: D19 は「関門の数字を好きな回で止めて選べないようにする」規則で、
  実装側が結果を見てから破ると規則の意味が無くなる。一方 K7 は効果サイト（関門の分母）と危険効果の
  件数を系統的に減らしているので、直さずに報告すると F0a の数字が何を測ったかが変わる。どちらを
  重く見るかは研究の主張の立て方の判断である。
- **暫定**: (a)。**感度分析**（D19 の「結果」。関門の数字ではない）: K7 だけを直すと、mcp_server の
  危険効果を持つユニットが 431 → 457、効果サイトが 444 → 460、`in_tree_resolution_ratio_sites` が
  33.6% → 32.6%（区間 [18.0%, 49.5%] で「境界」ではなくなる）。tool_package と app は変わらない。
  関門の点推定の判定（○ / ×）はどの母集団でも変わらない。

## O7. 事前登録した分母（`docs/preregistration.md`）を承認するか

- **2026-09-20 追記（D27）**: `r_prev` も分母で反転する。§2.7 (f) の分母（前リリースを
  持つ 16 木）では 88.1%、無条件（98 木）では 23.1%。§10 の 3 連言は事前登録の分母では
  不発火、併記の分母（validator 保有 = all_units、`r_prev` = 無条件）を 2 つとも採ると
  mcp_server と tool_package で発火する。**選択が判定を反転させる**ので実装側で確定しない。

- **要る情報**: 下の 3 点への可否。**学生の判断が要るのは、選択が
  §10 関門の合否を反転させる方向にあるからである**（実装側で黙って決めると
  「結果を見て分母を選んだ」と区別できない）。
- **背景**: 仕様書 §10 は `validator_holding_ratio` に閾値 5% を置きながら
  **分母を書いていない**（:1101 と :1143 の 2 行。どちらも分母の記述なし）。
  実装 `scripts/f0a.py:180` は全ユニット分母を採っているが根拠は未記録。
  run6 で分母を変えて測ると **18 セル中 16 セルが関門を通過し、落ちるのは
  最も分母が大きい `all_paths × all_units` の 2 セルだけ**
  （`.venv/bin/python scripts/denominators.py evidence/f0a_run6`）。
  公表済みの「validator 保有 4.4% / 3.3%、関門 ×」はその 1 通りの値である。

| 問い | 実装側の案 | 根拠 |
|---|---|---|
| (a) 主分母を `dangerous_fp_excluded × all_paths` にするか | **する** | 仕様書 §6 の指標表と §10 が D 層別存在率に同じ分母を明文で指定しており、`validator_holding_ratio` だけを外す根拠が仕様書に無い。危険効果を持たないユニットは validator を持つ動機が無く、分母に入れると「不要だから無い」と「必要なのに無い」が混ざる |
| (b) 固定した分母を run6 の判定に**遡及させない**か | **遡及させない** | 主分母は「run6 が × である」と知った後に選んだ。反転を「関門を通過した」の根拠に使わない。run6 の公表値と判定は据え置き、新分母の値は感度分析として報告する |
| (c) 論文で run6 の関門をどう書くか | **× と報告し、6 分母の感度分析を付ける** | (b) の帰結。「保留」と書く案もある |

- **暫定**: `docs/preregistration.md` を作成済み（初版 2026-09-20）。
  **上記 3 点は「実装側の案」として書いてあり、承認されるまで確定ではない。**
  否認する場合は `all_units` を主分母に据え置くか、別の分母を指定する。
- **関連**: `docs/decisions.md` D20。本件は D20 の (4) として記録した
  （決定ではなく「学生の承認待ちの案」として）。

---

## O8. Def 5 の条件 (ii) と root-equal が未実装。inline 形は一律 weak、helper 形は袋詰め採点（D21 / D25 の残り）

**2026-09-21（D36）: 等級づけを主張から降ろしたので、本項は「主張の穴」ではなく「道具の限界」になった。誤りの向き（false-clean）は変わらないので限界節と manifest の注記には残すが、直す優先度は下がる。**

- **要る情報**: 条件 (ii)・root-equal・inline 形の strong-path を実装するか、
  限界として本文に書くかの判断。**実装側では決められない**（月 6 のゲート語彙
  凍結と held-out の設計に関わる。実装するなら B3 の主語一致の上に載せる必要がある）。
- **背景**: D21 で strong-path を val の証拠で裏づけるようにしたが、裏づけられた
  のは Def 5 の条件 (i)（制御引数の root に symlink 解決子を通った canonical alias が
  存在する）だけである。D21 は同時に inline 形を囲み関数の本体全体で採点するように
  したが、その袋詰め採点が false-clean を 25 形入れたことが敵対的レビューで確定し、
  **D25 で撤回した**。現状:
  - **inline 形は一律 weak**（`gate.py: _grade_from_shape`）。Def 5 を inline で
    満たす形（`tests/test_value_grade.py` a1〜a3）も weak になる。
    **誤りの向きは false-dirty（安全側）**。野外での出現率は未測定。
  - **helper 形は本体の形状集合で採点**（`gate.py: _value_grade`）し、条件 (i) を
    `alias_facts` の root 一致で裏づける（D25 で全 root 要求）。条件 (ii)（包含述語が
    canonical alias **そのもの**に適用され、その述語が sink をゲートする）と
    root-equal（`ROOT_EQUAL_STEPS`、sink に届く値と検査された alias の差）は
    **未実装**。**誤りの向きは false-clean**。
- **なぜ実装できなかったか**: (ii) は「包含述語のどのオペランドが canonical
  alias か」を要求する。`ValResult.env` は最終 env なので canonical alias が
  callee の中にある形では残らず、`alias_facts` は root 粒度で**値の同一性を持たない**
  （派生値・別の値への `realpath` でも同じ root の行が立つ）。**較正対 A4
  （`mcp-server-git` の `git_add`）が手続き間の実例**で、`resolved =
  (repo_root / f).resolve()` は低レベル `call_tool` ハンドラから降りた先の関数の中に
  ある。root-equal を `canonicalised` 属性で見ようとするとこの対が落ち、
  `n_verdict_clearing_pairs_inject` が 1/7 → 0/7 に下がることを実測した（主指標の
  退行。D21 時と D21 レビュー時の 2 回）。
- **取りこぼす形（すべて false-clean、凍結済み）**:
  - `tests/test_d21_adversarial.py` **x01**: helper が root だけ `realpath` する b1 形に、
    ツール本体で無関係な `realpath(path)`（ログ用）を 1 行足すと strong-path に反転する。
    b1 を「直した」根拠は「root `path` の alias が無い」という偶発的性質だけである。
  - 同レビュー R15 / R21 の helper 変種（検証済みの `commonpath([path, base])` 形が
    デコイ 1 行で復活）、R16 の変種（commonpath 形・再束縛形・ループ形）。
  - **check-then-canonicalise**（R18: 検査の後に `realpath`）は「正規化はしているが
    検査には使わず」という従来の O8 の文言からは射程内と読めなかったが、同じ族である。
- **暫定**: 条件 (i) + 全 root + 領域一致で運用し、(ii) / root-equal / inline を限界
  として記録する。実装するなら、候補述語 1 つに対して「sink を支配する述語だけを
  採点に使う」「述語の被演算子が canonical alias の**値**であることを val の site
  つき事実で確かめる」「sink に届く値の root ⊆ 検査された値の root」を同時に入れ、
  期待値を先に置いて敵対的レビューを通す（D25「なぜ (B) 完全実装ではなく撤回か」）。

---

## O10. Def 5 の条件 (iii)（述語の他方の被演算子）が未実装

**2026-09-21（D36）: 等級づけを主張から降ろしたので、本項は「主張の穴」ではなく「道具の限界」になった。誤りの向き（false-clean）は変わらないので限界節と manifest の注記には残すが、直す優先度は下がる。**

- **要る情報**: 実装するか、限界として本文に書くかの判断。
- **背景**: `validators.py: ALLOWED_OPERANDS`（literal / config_root / os.getcwd）と
  `DOWNGRADES` の `tainted`（述語オペランドが MODEL）は**定義のみで参照 0 件**。
  `gate.py: _value_grade` は正規化子名と包含述語名の集合しか見ず、**オペランドを
  一切見ない**。包含 root 自体がモデル引数（`base = realpath(workspace)`）でも
  strong-path になる。`tests/test_d21_adversarial.py` **x03**（helper 形）に凍結
  （inline 形 r11 は D25 で inline が一律 weak になったため GAP に戻ったが、
  条件 (iii) を実装したからではない）。
- **誤りの向き**: **false-clean**。`workspace="/"`, `rel="etc/passwd"` で `..` 遍歴
  すら要らない。
- **記録が無かったこと**: D21 の決定文にも本ファイルにも無かった（規則 4 違反）。
  D21「結果」と D25 で記録した。
- **暫定案**: val は述語オペランドの `Prin` を既に持っている。`_value_grade` に
  「包含述語の他方の被演算子の root が MODEL なら `tainted` を当て strong にしない」
  を足す（安全側の変更なので敵対的レビューは要らないが、較正対を必ず測る）。

---

## O11. helper 経路の袋詰め採点（`_value_grade` は本体の形状集合しか見ない）

**2026-09-21（D36）: 等級づけを主張から降ろしたので、本項は「主張の穴」ではなく「道具の限界」になった。誤りの向き（false-clean）は変わらないので限界節と manifest の注記には残すが、直す優先度は下がる。**

- **要る情報**: O8 と同じ判断。O8 と一体で決める。
- **背景**: D21 レビューの M1 は inline に限らず、helper 経路 `gate.py: _value_grade`
  も同じ「正規化子の集合 × 包含述語の集合」である。helper の本体に `realpath` と
  境界つき `startswith` が**どこかに**あれば、適用対象も順序も支配も問わず
  strong-path になる。D25 は inline 側だけを撤回し、helper 側は条件 (i) の全 root
  裏づけ + 領域一致で運用している。
- **誤りの向き**: **false-clean**。x01（デコイ 1 行）がその実例。
- **なぜ helper 側を撤回しなかったか**: 較正対 A1 / A4 / A10 の修正側の strong-path
  はすべて helper 形（`_validate_path` 等）であり、helper 側を一律 weak にすると
  両側通過の分子（`docs/expected_tuples.json` の `grade → strong-path`）が全滅する。
  **これは「較正対を守るために false-clean を残している」ことに等しい**ので、
  隠さずここに書く。野外での x01 型の出現率は未測定。

---

## O9. 野外標本の pin が全件 `HEAD`（143/143）で、再取得の経路が無い

- **要る情報**: `trees.jsonl` の `commit_sha` で pin し直すか、消えた木をどう扱うか。
- **背景**: `docs/corpus_sample.json` の 143 件はすべて `ref: HEAD`。標本抽出から
  6 日で 2 repo が GitHub から消え（`archsec-emman/financial-orchestrator` と
  `bingstat/nexus`）、前者は run6 の tool_package の分母（85 ユニット）に入っている。
  D23 の `fetch_failed` 1 件はこの repo。**pin が `HEAD` である限り、run7 も較正対の
  再走も他人には再現できない。**
- **暫定案**: (a) `corpus_sample.json` の `ref` を `evidence/f0a_run6/trees.jsonl` の
  `commit_sha` に置き換える（run6 と同じ木を指すようにする）。(b) 消えた 2 木は
  分母の注記として残し、scratchpad に残る clone があるうちに bundle 化する。
  (c) `fetch_corpus.py` にリモート失敗時の bundle フォールバックを足す。
  **(a) は結果を変えない（同じ commit を指すだけ）ので実装側で進めてよいと
  考えるが、標本ファイルの書き換えなので学生の承認を待つ。**

---

---

## O12. 判別実験の判定規則が第 3 類型（CodeQL が両側とも報告）を想定していない。等級づけを章に立てるか — **解決（D36: 案 (β)。章に立てず道具として報告する）**

**2026-09-21 学生の決定（D36）: 等級づけによる脆弱版 / 修正版の判別は主張から降ろす。**
根拠は母集団 v2 の実測（交差行の候補 5 行・2 プロジェクトで §3 の条件 3 行・3 プロジェクトに届かず、
trig が traced のユニットが 0.6% で §3 の「20% 未満なら SELECT を格下げする（撤回しない）」条項が発火）。
以下は決定前の記述として残す。

- **要る情報**: `docs/preregistration.md` §5.1 の (α)(β) のどちらを採るか。
  **実装側では決められない**（規則を書いた後に結果を見ており、どちらを採っても
  post-hoc の解釈になる。学生が決め、決めた理由と「結果を見た後の決定」であることを
  本文に書く）。
- **背景**: 判定規則（§5 #2）は「`C − C0` に A10 が残り、かつ CodeQL が A10 脆弱側を
  clear する → 章に立てる」「`C − C0 = ∅` または CodeQL が両側判別 → 降ろす」の
  二択で、CodeQL が**両側とも報告する**（修正を認識できない）場合を扱っていない。
  実測は後者（第 3 類型）で、前提 A10 ∈ C − C0 は成立している（D26）。
- **各案の含意**:
  - (α) 章に立てる: 主張は「二値の検証子モデル（C0）は脆弱側を clear し、既存の
    path-injection 検出（CodeQL、入口を揃えても）は修正を認識できない。等級づけだけが
    脆弱 = GAP / 修正 = clear を出す」。**根拠は較正対 1 対（A10）**で、`n = 1` を
    本文に書く。D24 の 3 段（B 段 = ゲート等級）を維持する。
  - (β) 降ろす: 等級づけは manifest 属性と fixture / mutant のカタログ
    （`tests/test_value_grade.py`、`tests/test_d21_adversarial.py`）として報告し、
    主張の章にしない。D24 の B 段を C 段（道具）に落とす。O8 / O10 / O11 の
    未実装（false-clean 側）が残っていることは (β) を支持する材料になる。
- **どちらでも必要なこと**: (b) の結果は (a) の分子の直し方に依存する
  （any-change のままなら C − C0 = ∅）。分子の照合が事前登録どおりであることを
  本文で示す（§5 #2 (a)、`d2b501a` → `654bca2` → `cf75fd7` → `b2b7c21` の順序）。

---

## O13. unit id が木の中で一意でない（Def 6 の join の前提が崩れる）

- **要る情報**: unit id の定義を変えるか（例: relpath を含める）、重複を数え方で
  扱うか（distinct-id 併記のまま）の判断。**id を変えると run1〜6 と較正対の全 unit
  行の id が変わる**ので、実装側で決めない。
- **背景**: `r_prev` run2 で 16 木中 4 木に重複（crewAI 321 ユニット / 312 id、
  fewsats 8 / 4、nuguard 186 / 109、ava 20 / 19）。同じ `framework:qualname:hash` を
  持つツールが複数回登録される形（tests / examples の複製、同名ツールの再定義）。
- **影響**: `r_prev` は重複込み 88.1% / distinct 87.5% で結論は変わらない。
  `GAP_DRIFT` の join 先は `DPrev.load` が同じ id の**最後の行**を採る実装で、
  どの複製と比べるかが定義されていない（**不明**）。D_prev 層の drift を主張に使う
  前に決める必要がある。
- **誤りの向き**: どちらとも言えない（join 率には効かないが drift の中身に効く）。

---

## O14. 宣言 D を持つ部分母集団をどう扱うか（第 2 の枠 / R2 の拡張）— **解決（D29: 母集団を宣言ありに変える）**

- **要る情報**: (a) OpenHands 型（app 枠組みの `ToolDefinition(annotations=ToolAnnotations(...))`）
  を R2 カタログに足すか、(b) 「明示の MCP annotation を持つ Python サーバ」を第 2 の枠
  として事前登録して抽出するか、(c) どちらもせず「この枠では宣言が無い」を第一の
  野外所見として書くか。**母集団の定義と Def 2 の変更なので実装側で決めない。**
- **背景**（D28、`docs/preregistration.md` §2.8 (d)）: 97 木の自前コードに本物の宣言が
  あるのは OpenHands（15 ツール定義）だけで、R2 カタログ外。MCP サーバ側の明示
  リテラルは 676 中 2。GitHub 全体では Python の呼び出し形宣言がファイル単位で枠の
  約 5%（参考値）、TypeScript が 2〜3 倍。
- **追記（§2.8 (e)）**: 星数上位の Python MCP サーバでは 9/29 = 31% が宣言を持つ。
  (b) の第 2 の枠は「`topic:mcp-server` / 星数 / 保守されている」のような
  repo 水準の枠で定義できる（`docs/population.md` の枠は import 文の file 水準）。
  **現在の枠が小規模・チュートリアル repo に偏っている**ことは、r_D だけでなく
  validator 保有・opaque 率・危険ユニット数のすべてに効くので、枠の再定義は
  r_D の問題として片づけない。
- **各案の含意**: (a) は D24 の「カタログは広げない」と逆で、app 母集団（8 木）だけに
  効く。(b) は「宣言する少数派で D と M の差を測る」研究になり、元の §0 の主張に
  最も近いが、標本抽出をやり直す（事後選択にならないよう抽出前に定義する）。
  (c) は D27 の枠選びと整合する。
- **誤りの向き**: (c) を選ぶと「宣言との差」の主張を、それが成立しうる少数派で試さずに
  降ろすことになる（主張を弱く見せる側）。(b) を選ぶと母集団の外から標本を選ぶので、
  結果は「宣言する少数派について」しか言えない（一般化を狭める側）。

---

## O15. `r_D` の分子の定義が実装内で食い違う（上界を動かす明示 53.3% / 明示 1 つでも 80.0%）— **解決（D32: 上界を動かす明示）**

- **要る情報**: 仕様書 §10 :1121〜1124 の `r_kind` の定義を、`D_kind ≠ ⊥`（上界を
  動かす明示: `readOnlyHint==true` / `destructiveHint==false`）と読むか、
  `openWorldHint==true` 単独の明示も含めるか。
- **背景**: `scripts/f0a.py:390` は前者、`authgap/dparse.py: parse_d_kind` の
  docstring は後者。旧枠では両方 0 で見えなかった。母集団 v2（D30）では
  547/1,027 = 53.3% と 822/1,027 = 80.0%。どちらでも §10 は分岐 1。
- **誤りの向き**: 分子の選び方で `r_D` が動くが、判定（分岐）は動かない。本文では
  両方を併記し、どちらを主にするかを決めてから固定する。

---

## O16. `destructiveHint==false` の宣言に対して、追記型の FS_WRITE を CONTRADICTION に数えるか — **解決（D32: 案 (a)、削除・上書き型だけ）**

- **要る情報**: Def 7 の CONTRADICTION の読み。`authgap/dparse.py: d_kind_from` は
  destructiveHint==false の上界に FS_WRITE（追記型）と DB を含めるが、
  `dparse.contradiction` は FS_WRITE を無条件に矛盾とする。
- **背景**: 母集団 v2 の full scan で CONTRADICTION 80 件のうち 32 件（12 木）が
  destructiveHint==false のみに反するもので、`shutil.rmtree` / `os.unlink` のような
  削除（矛盾として妥当）と、`mkdir` / `open(w)` のような追記型（上界の定義では
  宣言内）が混ざる（D31、`evidence/scan_v2_run1/contradictions.json`）。
- **案**: (a) 追記型と削除型を sink カタログで分け、削除型だけを矛盾に数える
  （sink 語彙の変更 = 凍結後の逸脱として記録）。(b) 現行どおり FS_WRITE 全部を
  矛盾に数え、上界の定義を FS_WRITE を含めない形に揃える。(c) 現行のまま、本文で
  32 件を「追記型を含む」と注記する。
- **誤りの向き**: (a)(b) で 32 件が減る側 / 増えない側に動く。手検証（D31 の次の
  作業）で削除型と追記型の内訳を出してから決める。

---

## O17. val 受け入れ fixture F1–F10 の初回採点: OpenManus の 3 件（F6/F7/F8）が false-clean 方向で未達 — **(c)(d)(e) は解決（D35）。(a)(b) は学生の入力待ち**

- **状態**: 期待値 `fixtures/val/expected.json`（仕様 §2.6 の表から転記、コミット
  5944a0b）を採点器 `tests/test_val_fixtures.py` で当てた初回の結果（2026-09-21）。
  74 項目中 48 通過・26 未達（xfail(strict) で固定）・F9/F10 は木が未取得で skip。
  F1–F4（較正対 A1 / A5）は**全項目通過**。F5 は EXEC 行・MODEL・roots が通り、
  負のアサート（INDIRECT 表から `multiprocessing.Process` を外しても clean にならない）
  も通る。
- **学生の入力が要るもの**:
  - (a) **仕様内の食い違い**: F2 は「`alias_facts` が空」、F7 は「`alias_facts +=
    (path, validate_path, Path())` — 正規化ではない」と、`Path()` の alias fact を
    片方は無し・片方は有りで期待している。実装は F7 側（`Path()` を非正規化の
    alias fact として出す。Def 5 の root-equal 判定にはこの表が要る）。F2 の「空」を
    「正規化子の alias fact が無い」と読む（D33）でよいか。**仕様書本体は直さない。**
  - (b) **未出力の欄**: 仕様の期待行にある `depth_used`（F5/F6）と `shape=Seq.tail`
    （F8/F9）は manifest に欄が無い。`witness_chain` の長さで `depth_used` は代替
    できるが、期待行の属性として出すか（manifest スキーマの変更 = 指紋の変更）。
  - (c)〜(e) は**解析器の未達**で、いずれも**行が出ない = false-clean 方向**
    （ユニット水準では opaque が残るので clean にはなっていない）。直すなら
    opaque → resolved の変更なので、D17 改訂 2 と同じ敵対的レビューを通す:
  - (c) **F6 `Bash.execute`**: `self._session: Optional[_BashSession] = None` と
    `self._session = _BashSession()` の合流で `Obj` と `None` の join が `Unknown` に
    落ち（`ir._shape_join` は kind が違えば Unknown）、`self._session.start()` /
    `.run()` の受け手型が消える。結果、`_BashSession.start` は末尾名解決 +
    opaque(unresolved) で `self.command`（クラス体既定値 `"/bin/bash"`）が読めず
    `shell_string = OP/Unknown`、`run` の `self._process.stdin.write(command...)`
    （`EXEC@pipe`）は出ない。**候補の規則**: メソッド呼び出しの受け手位置では
    `None` リテラルの分岐は呼び出しに到達しない（AttributeError）ので、
    `Obj ⊔ None` は `Obj` として受け手解決に使う。**反証条件**: 2 型以上の Obj の
    合流には適用しない（どちらの型かで sink が変わる）。
  - (d) **F7 `StrReplaceEditor.execute`**: `operator = self._get_operator()` は
    IfExp で `LocalFileOperator` / `SandboxFileOperator` の 2 型 `Obj`。
    `execute → str_replace/insert → operator.write_file → Path(path).write_text`
    が深さ 3（`MAX_DEPTH = 3`）で `cap_hits = depth` に当たり、FS_WRITE 行が 0。
    仕様の witness chain（`execute → operator.write_file → write_text`）は
    `create` 分岐（`execute` 直下、L139）のもので深さ 2 だが、それも出ていない
    （2 型受け手の分岐が未実装か、`self._local_operator` のクラス体 pydantic
    フィールド既定値 `LocalFileOperator()` の受け手が引けていないかは未切り分け）。
  - (e) **F8 `Crawl4aiTool.execute`**: `AsyncWebCrawler` は CTOR カタログにあり
    `async with ... as crawler` は `_bind` で束縛されるが、`crawler.arun(url=url,
    config=run_config)` の proxy sink（`recv_types = crawl4ai.AsyncWebCrawler`）が
    当たらず opaque(receiver)。`from crawl4ai import AsyncWebCrawler` が関数内の
    `try:` の中にある（`function_scope` は recurse=True で拾うはず）ので、
    `async with` の ctor 評価か `for url in valid_urls:` のループ内の受け手の
    widening のどちらかが原因（未切り分け）。
- **進捗（D35）**: (c)(d)(e) は解析器を直して行が出るようになった（敵対的レビュー 2 本、
  反証 13 形を直した後）。残るのは語彙の差と未出力（`tests/test_val_fixtures.py` の
  `KNOWN_UNMET`）と、D35 の「残る既知の限界」（別名、末尾名のクラス、継承、remote）。
- **誤りの向き**: (c)(d)(e) は効果行が出ない側（false-clean）。ただし 3 件とも
  ユニットに `opaque_reasons` が残るので「clean」ではなく「opaque」。§10 の脈拍の
  負例（OpenManus は GAP を出さない）は、行が無いことで成立しているのではなく
  opaque で成立していることになる。**この違いは本文に書く。**
- **付随の観察**: F5 の `PythonExecute.execute` に `_BashSession.start` の SPAWN 行が
  1 行混入する（`proc.start()`（`multiprocessing.Process.start`）が末尾名で
  `_BashSession.start` に解決され、opaque(unresolved) を合流して降りる。D17 改訂の
  「受け手型で裏付けられない解決は降りて opaque を合流」の帰結）。false-dirty 側。
  仕様の F5 は行数を縛っていないので採点には入れていない。

---

## O18. 効果行の上限 `EFFECT_ROW_CAP = 200`（仕様 §5.2）が適用されていない。呼び出し点ごとの複製で行数の指標が膨らむ

- **状態**: `authgap/ir.py: EFFECT_ROW_CAP = 200` は指紋（`report.py`）に書き出されるだけで、
  行の生成を止めていない。D35 の解析器で受け手型が解決するようになり、API ラッパ経由の
  NET 行が呼び出し経路ごとに複製されて 1 ユニット 294 行（canvas-mcp
  `get_my_peer_reviews_todo`）、1 木 4,467 行になった（`evidence/scan_v2_run4/summary.json`）。
  仕様 §2.6 は「行数を実際に抑えているのは §5.2 の cap」と書くが、抑えていない。
- **要る決定**: (a) cap を実装して超過を `opaque(cap)` の内訳として出す（仕様どおり。
  20% を超えたら深さを 2 に落とす規則も動く）。(b) 行を (site, slot, chain) で畳んで
  件数を別に持つ。(c) 現状のまま、行単位の指標（`verdict_rows`）を本文で使わず、ユニット
  単位（危険ユニット、CONTRADICTION のユニット × site）だけを使う。
- **誤りの向き**: 行単位の件数（GAP_INJECT 197 → 767）は複製で膨らんでおり、そのまま
  比較すると解析器の変更を過大に見せる（false-dirty 側の見かけ）。ユニット単位の数値
  （危険ユニット 1,027 → 1,169、CONTRADICTION 72 → 79）は複製の影響を受けない。

---

## O20. sink カタログの意味付けを「母集団の宣言が割れた API だけ」に絞るか

- **状況**: `docs/catalog_map.md`（D37）で、同じ API を呼ぶツールが readOnly と
  destructive の両方を明示している site が **20 / 41** あることが分かった。
  一方、核の主張（CONTRADICTION 79 件）が実際に使っている API は **13 種類**しかない。
- **案**: 「どの API がどの能力か」を人が 67 行書くのをやめ、**母集団の宣言が矛盾した
  API だけを裁定する**。矛盾の検出自体はオラクル不要で健全（少なくとも一方が誤っている）。
- **やってはいけないこと**: 多数決を真理に使う。`subprocess.run` は readOnly が
  12 対 3 で多数派になるが誤りである。**多数派が誤っていること自体が所見**であって、
  較正の材料ではない。
- **要る判断**: (a) この方式に切り替えるか、(b) 現行のカタログを維持し、割れている 20 件は
  所見として報告するだけにするか。**精度が下がるなら切り替えない**（学生の指示、2026-09-22）。
- **判断の前に要る測定**: 切り替えた場合に CONTRADICTION 79 件と較正 14 木の効果行が
  動かないかの突き合わせ。動くなら (b)。

---

## O21. `AST_NODE_CAP` で切られたファイルを分母からどう扱うか（`mcparmory/registry` が 1 木で 9,524 ツール）

- **状況**（D40 で HintLint と突き合わせて見つかった）: 母集団 v2 の `@tool` 系デコレータは
  **12,713 個**あるが、うち **9,816 個（77.2%）は `AST_NODE_CAP = 20,000` で切られたファイルの中**
  にある。AuthGap のユニットは 2,231 個。
- **ただしこれは 1 木の話である。** 9,524 個が `v2-mcparmory__registry` 1 本
  （生成された MCP サーバを 64 ファイルに集めた単一リポジトリ。`servers/close/server.py` は
  60,650 ノード、`servers/grafana/server.py` は 54,192 ノード）。
  **この 1 木を除くと 292 / 2,543 = 11.5%。**
- **打ち切りは黙って消えてはいない。** manifest の `truncations` に
  `{"cap": "ast_node_cap", "count": N, "relpath": ...}` として全件残る
  （母集団 v2 全体で 135 件 / 16 木）。CLAUDE.md 規則 4 は満たしている。
- **要る判断**: 率の分母をどれにするか。
  - (a) 木を単位にした率だけを報告し、ツール数の率は `truncations` を注記して出さない。
  - (b) `mcparmory/registry` を**外れ値として本文の分母から外す**（生成物の単一 repo で
    他の木と性質が違う）。外すなら**事前登録の逸脱として `docs/preregistration.md` に記録**する。
  - (c) `AST_NODE_CAP` を上げて取り直す。**測定後に cap を動かすことになるので、
    事前登録の逸脱になる。**しかも 60,650 ノードのファイルは解析時間が読めない。
- **誤りの向き**: (b)(c) はどちらも**結果を見てから母集団を動かす**方向で、CLAUDE.md 規則 5 に
  触れる。**(a) が既定である。** 動かすなら逸脱として明記する。
- **今の扱い**: 未決。`docs/related_work.md` R1 節に両方の数（77.2% と 11.5%）を書いた。

---

## O22. `Path(...).parent` / `.parents[n]` が受け手の Path 形を落とし、FS の sink を落とす（**誤 clear**）— **解決（D43）**

- **状況**（D40 で HintLint と突き合わせて見つかった）:
  `v2-rwheeler007__cohort` の `internal_web_fetch`（`readOnlyHint: true`）は

  ```python
  cohort_root = Path(__file__).resolve().parents[2]
  cache_dir = cohort_root / "data" / "services" / "web_cache"
  cache_dir.mkdir(parents=True, exist_ok=True)   # ← FS_WRITE
  ```

  だが AuthGap の効果は **0 件**。HintLint は `READONLY-001` として検出している。
- **切り分け済み**（最小再現）: `Path("/tmp")/"x"`・`Path("/tmp").resolve()`・
  `(Path("/tmp")/"x").mkdir(...)` はいずれも `pathlib.Path.mkdir` の sink 行に当たる。
  **`Path("/tmp/a/b").parent` だけが当たらない。**
  `authgap/val/engine.py` の `_ev_Attribute` が、受け手が `Path` 形のときの属性参照
  （`.parent` / `.parents`）を扱わず `Unknown()` に落とすため、`effects.py` の
  `_receiver_typed_key` が `isinstance(ev.receiver.shape, Path)` で外れる。
- **誤りの向き**: **誤 clear（false-clean）。** 危険を見落とす側である。
  `opaque_reasons` に `receiver` は残るが**行が 1 本も出ない**ので、
  manifest の行の集計からは完全に消える。「不明として残す」が**ユニット水準にしか効いていない**。
- **直し方の候補**: `_ev_Attribute` で受け手が `Path` 形かつ属性が `parent` のとき、
  **主体・roots を保ったまま形だけ `Path` に戻し、確度に `opaque(unresolved)` を合流する**
  （`.parent` は末尾の seg を落とすので、元の segs をそのまま持たせるのは過大主張になる）。
  `.parents[n]` は `_ev_Subscript` 側も要る。
- **要る手続き**（CLAUDE.md）: これは **opaque → resolved 方向の変更**なので、
  (i) `scripts/diff_effects.py` で較正対 14 木の効果行を突き合わせ、
  (ii) 「resolved にしてよい根拠」を崩しに行く敵対的レビューを通す。
- **解決（2026-09-22、D43）**: `_ev_Attribute` で受け手が `Path` 形かつ属性が
  `parent` / `parents` のとき、**形だけ `Path` に保ち中身は何も引き継がない**値を返す
  （`_path_ancestor`）。`prin` と `roots` は保ち、`base` / `segs` / `tail` / `attrs` は
  落とし、確度に `opaque("unresolved")` を合流する。
  較正対 14 木で**消えた行 0 / 増えた行 13**（A5 の 2 木で 8 ずつ、A9 の 2 木で 5 ずつ。
  両側対称）。増えた 13 行は目視で全部本物だった。


## O23. 矛盾関係の表（`docs/contradiction_matrix.md`）で「決めが要る」と残した 5 マス

- **状況**: 宣言 D（MCP `ToolAnnotations` の 4 つ）と効果 sub_kind の矛盾関係を
  表として定義した（D41、`docs/contradiction_matrix.md`）。**仕様の文言から導けるマスは
  すべて埋めた**が、5 つだけ仕様の文言から一意に決まらないマスが残った。
  **決めるまでは報告しない**（黙ってどちらかに倒さない。CLAUDE.md 規則 4）。

| # | マス | 判断が要る点 | 母集団 v2 の件数 |
|---|---|---|---|
| 1 | `readOnlyHint:true` × `DB_WRITE(PRAGMA)` | 接続設定は「環境の変更」か。`PRAGMA journal_mode=WAL` は `-wal` ファイルを作るので**ファイルシステムは変わる**。`busy_timeout` は何も残さない | **54**（`journal_mode=WAL` 52 / `busy_timeout` 2） |
| 2 | `readOnlyHint:true` / `destructiveHint:false` × `NET`（`POST`/`PUT`/`DELETE`） | 仕様の `its environment` に**リモートの状態**を含めるか。含めないなら `openWorldHint` の領分になる | 9 + 57 |
| 3 | `destructiveHint:false` × `FS_WRITE`（mode が読めない） | **D32 は矛盾に倒している。**規則 4 に照らすと「不明」が正しい。D32 を見直すか | 0（母集団に該当なし） |
| 4 | `openWorldHint:false` の「外部ホスト」の定義 | private range / localhost / 環境変数由来のホストをどう扱うか | `NET` 効果 151 |
| 5 | `idempotentHint:true` | 片側判定（**非冪等の証拠**を探す）を実装するか、未対応と書くか | — |

- **誤りの向き**: #1 と #2 を「矛盾」に倒すと**誤警報**が増える（#1 の 54 件は
  1 つのプロジェクトの接続設定が繰り返し数えられているだけ）。「宣言内」に倒すと
  **誤 clear** になる。**どちらにも倒さず「決めていない」と書くのが現状の正解。**
- **先に要る作業**: #1 を決める前に、`_sub_kind` の `DB_WRITE` から `PRAGMA` /
  `BEGIN` / `COMMIT` / `ROLLBACK` を分ける（下の作業 B2）。分けずに
  `readOnlyHint:true` × `DB_WRITE` を矛盾にすると **101 件の誤警報**になる。

---


## O24. `WITH` を無条件に読み取りとするのは潜在的な誤 clear（母集団に 0 件）

- **状況**（D41 で表を書く作業が見つけた）: `authgap/effects.py: _sub_kind` の
  読み取り語の一覧に `WITH` がある。

  ```python
  return "DB_READ" if head in ("SELECT", "SHOW", "EXPLAIN", "DESCRIBE", "WITH") else "DB_WRITE"
  ```

  PostgreSQL などは `WITH x AS (...) INSERT INTO t ...` を書けるので、
  **書き込みが `DB_READ` になりうる**。
- **誤りの向き**: **誤 clear（false-clean）。** 危険を見落とす側である。
- **観測**: **母集団 v2（`evidence/scan_v2_run4`）に `WITH` で始まる SQL は 0 件。**
  したがって現時点で実害は出ていない。**「無い」ではなく「この標本では 0 件」。**
- **直さない理由**: 条件つきにする（本文に `INSERT` / `UPDATE` / `DELETE` の語があれば
  書き込みとする、など）と、**文字列リテラルや列名に含まれる語で誤警報を作る**。
  SQL を字句解析するのは sink カタログの役割を超える。
  **CLAUDE.md の「憶測で直さない」に従い、既知の限界として記録する。**
- **要る判断**: (a) 記録して直さない（現状）、(b) `WITH` を読み取り語の一覧から外す
  （`WITH ... SELECT` が `DB_WRITE` になる = 誤警報側に倒す）、(c) 簡易な字句解析を入れる。
  **`DB_WRITE` を矛盾判定に使う段階（O23 #1）で決める。**

---


## O25. 解決できない呼び出しの戻り値が主体を MODEL から OP に落とす（**誤 clear**）— **解決（D44）**

- **状況**（D43 の敵対的レビューが見つけた。O22 とは別の、**より広い**誤り）:

  ```python
  @mcp.tool()
  async def t(p: str) -> str:
      os.system("rm -rf " + str(p))      # shell_string の主体が OP になる
  ```

  最小再現で確かめた（`str()` を通さなければ MODEL のまま）:

  | 書き方 | `path` / `shell_string` の主体 |
  |---|---|
  | `os.makedirs(p)` | **MODEL**（正しい） |
  | `os.makedirs(f"{p}")` | **MODEL**（正しい） |
  | `os.makedirs(str(p))` | **OP**（誤り） |
  | `os.makedirs(os.fspath(p))` | **OP**（誤り） |
  | `os.system("rm -rf " + str(p))` | **OP**（誤り） |
  | `os.system("kill " + str(int(p)))` | **OP**（誤り） |

- **誤りの向き**: **誤 clear（false-clean）。** 主体が OP になると `GAP_INJECT` が立たない。
  **モデルが握っている shell_string が「運用者の値」として clear される。**
  確度は `opaque` なので行は残り `UNKNOWN` は立つが、**「モデルが握っている」という
  一番重要な情報が消える。**
- **原因（確定。`str` に限らない、もっと広い問題だった）**: `authgap/val/engine.py`
  `_ev_Call` の最後の fallback が

  ```python
  return Value(Prin.OP, opaque("unresolved"), Unknown(), frozenset(),
               frozenset().union(*[a.roots for a in args]) if args else frozenset())
  ```

  と、**root だけを引き継ぎ主体を `Prin.OP` に固定していた。**
  **root が「この値はツール引数 p 由来だ」と言っているのに主体が「運用者の値だ」と
  言うのは矛盾している。** `str` は一例にすぎず、**木の外のあらゆる関数**が同じ。
  さらに**キーワード引数と受け手は root にも入っていなかった**ので、
  `f(value=p)` と `p.unknown_method()` は root ごと消えていた（誤 clear が 3 通り）。
- **実例（母集団 v2）**: `v2-dddabtc__winremote-mcp` の `Notification` は
  `xml_escape(title)` を通してから PowerShell の here-string に入れる。
  here-string は `$(...)` を展開するので XML エスケープでは防げないが、
  `xml_escape` が未解決なので **`argv[*]` の主体が OP になり注入が clear されていた。**
- **要る判断**: (a) `TRANSFERS` に `str` / `int` / `float` / `bytes` / `os.fspath` /
  `repr` などの値変換の行を足す（**sink 語彙ではなく transfer 表。月 3 の凍結の対象か
  要確認**）。(b) より広く「解決できない呼び出しの戻り値は引数の主体を join する」に
  変える（**過大近似で誤警報が増える。危険**）。
- **なぜ (b) が危険か**: 無関係な関数（`len(p)`、`hash(p)`、`os.path.exists(p)`）の
  戻り値まで MODEL になる。**(a) の方が安全で、既存の設計にも合う。**
- **影響範囲は未測定。** 母集団 v2 で `str(` を通る効果が何件あるかは数えていない。
  **直す前に数える**（変更前後の両方を出すため）。
- **解決（2026-09-22、D44）**: fallback の主体を `_prin_all(contributors)` にし、
  `contributors` を**位置引数 + キーワード引数 + 受け手**にした（root も同じ集合から取る）。
  **入力に MODEL が無ければ `_prin_all` は `Prin.OP` を返す**ので、
  `uuid.uuid4()` / `time.time()` / `os.path.f("lit")` は OP のままである。
  較正対 14 木で**消えた行 0 / 増えた行 0 / slot 変化 68、全部 OP → MODEL の向き**
  （逆向き 0）。対ごとに対称。

---


## O26. §3 の交差行が run5 で合格条件を満たした（**誤り。D46 で訂正**）— **解決（D46: 案 (a)。D36 は降ろしたまま）**

**以下の「状況」は誤った数え方に基づく。決着（D46）は下にある。元の記述は
CLAUDE.md 規則 6 に従って残す。**

- ~~**状況**: D36（2026-09-21）は §3 の統一主張を「**交差行 5 行 / 2 プロジェクト**で
  合格条件（3 行以上・3 プロジェクト以上）を満たさない」ことを根拠に降ろした。
  解析器を直した run5 で数え直すと **15 行 / 5 プロジェクト**になり、**条件を満たす。**~~

| | run4（D36 の根拠） | run5 | §3 の条件 |
|---|---|---|---|
| 交差行の候補 | 5 | **15** | 3 以上 |
| 由来プロジェクト数 | 2 | **5** | 3 以上 |
| `trig = traced` | 14 / 2,231 = 0.6% | 14 / 2,231 = **0.6%（不変）** | 20% 以上 |

- **増えた理由**: D44 が主体を直したことで `GAP_INJECT` が増え（一意な位置で 363 → 733）、
  同一行が SELECT 系と INJECT 系を同時に持つ組み合わせが増えた。
  **コーパスが変わったのではなく、解析器の感度が上がった。**
- **重要な観察**: したがって §3 の交差行の数は**コーパスの性質ではなく解析器の精度の関数**
  である。「統一の唯一の証拠」として事前登録された指標が、解析器の誤 clear を直すだけで
  3 倍になった。**この指標が何を測っているのかを本文で論じる必要がある。**
- **ただし格下げ条項は依然として発火している。** `trig = traced` は 0.6% で 20% を
  大きく下回り、§3 は「traced 率が 20% 未満なら SELECT の野外評価は成立しないので、
  その時点で SELECT は構造的主張に格下げする。**この条項は撤回しない**」と書いている。
- **要る判断**:
  - (a) **降ろしたままにする（既定）。** 格下げ条項が非撤回であること、および
    「結果が動いたから主張を戻す」のは CLAUDE.md 規則 5 が禁じる形であることによる。
    run5 の数値は両方記録する。
  - (b) 交差行の条件は満たしたとして統一主張を戻す。**その場合、D36 を撤回した理由と、
    格下げ条項との関係を本文で説明する義務が生じる。**
  - (c) 3 腕アブレーション（`scripts/ablation.py`）を実際に回して、
    特徴づけによる「候補」ではなく腕の値で数え直してから決める。
- **誤りの向き**: (b) は**主張を過大にする方向**である。数値が有利に動いたときだけ
  事前登録の判断を巻き戻すのは、事前登録の意味を失わせる。
  **私（この記録者）の推奨は (a)。** ただし**学生の判断事項**である。
### 決着（2026-09-23、D46）— **前提が誤っていた**

**この項目の前提「run5 で 15 行 / 5 プロジェクトになった」は誤りだった。**
`scripts/intersection_rows.py` が §3 の除外規則（仕様書 553 行目
「`Leak` だけで説明できる行と `OPAQUE` 行は数えない」）を実装していなかった。

| | run4 | run5 |
|---|---|---|
| 除外なし（誤った数え方） | 5 行 / 2 プロジェクト | 15 行 / 5 プロジェクト |
| **§3 どおり（`UNKNOWN` を持つ行を除外）** | **1 行 / 1 プロジェクト** | **1 行 / 1 プロジェクト** |

**run4 と run5 で完全に同一の 1 行で、D43 / D44 は交差行をまったく動かしていない。**
除外を落とすと**解析器が未解決を正直に報告するほど交差行が増える**逆さまの指標になる。

**したがって案 (a)。判断事項ではない。** D36 が降ろした根拠は正しい数え方でも成り立ち、
しかも run4 の真の値（1 行 / 1 プロジェクト）は D36 が引用した値より条件から遠い。
格下げ条項（`traced` 0.6%）も発火したままである。**D36 の結論は不変、引用値のみ訂正。**

残る 1 行（`v2-ariffazil__wealth` / `wealth_fx_rate` / `url.query`）は本物で、
`trig` が MODEL / **traced**、`UNKNOWN` を持たない。§3 の文言では
「1〜2 行なら『統一の証拠は逸話的』と書く」に当たる。

---


## O27. snake_case の注釈が `D_malformed` として記録されない — **実装は解決（D48）。`r_malformed` の分母だけ学生の判断待ち**

- **状況**（D47 の点検で発見）: 仕様書 322 行目は
  「snake_case 表記（`read_only_hint` 等）は `ToolAnnotations` に deserialize されず
  protocol に届かないので **`D_malformed` として別行で報告する**」と定めている。
  **実装されていない。**
  - `authgap/entries.py: _read_annotations` は snake_case を集めて返すが、
    **デコレータ経路（`entries.py:403`）が `_malformed` を捨てている。**
  - `ToolLiteral.malformed_fields` はどこからも読まれていない。
  - `DKind.malformed` を設定する箇所が無く、**構造的に常に空**。
- **母集団 v2 の実数**: `read_only_hint` 195 / `destructive_hint` 174 /
  `idempotent_hint` 159 / `open_world_hint` 46 = **574 箇所 / 11 木**。
  manifest に `malformed` が出ているユニットは **0**。
  **仕様の前測は「21 エントリ」だったが、実際には桁違いに多い。**
- **誤りの向き**: 誤 clear ではない（snake_case は正しく上界を動かさない）。
  **失われているのは測定である。**「読み取り専用のつもりで宣言したが protocol に
  届いていない」という具体的な失敗形が、**注釈なしのツールと区別できていない。**
  これは「宣言はどれだけ当てにならないか」という本研究の問いに直接効く。
- **直し方**: `entries.py:403` で `_malformed` を `Unit` に載せ、`d_kind_from` に渡して
  `DKind.malformed` を立てる。**manifest の出力が変わるので full scan の取り直しが要る。**
- **要る判断**: 本文で `r_malformed`（snake_case を書いたツールの率）を報告するか。
  **報告するなら分母の定義が要る**（CLAUDE.md 規則 3）: 注釈を書いたツール全体か、
  宣言ありユニット全体か。
### 解決（2026-09-23、D48）と、残る判断

**実装は直した。** `Unit.malformed_fields` を足し、デコレータ経路・join した
`Tool(...)` リテラル・低レベル経路の 3 経路から載せ、`parse_d_kind` で
`DKind.malformed` に合流する。**上界にも `explicit` にも入れない**ので verdict は不変
（較正対 14 木で 0/0/0、run5 → run6 で全項目一致）。

母集団 v2（`evidence/scan_v2_run6`）の実測:

| 項目 | 値 |
|---|---|
| `malformed` を持つユニット | **130 / 2,231 = 5.8%** |
| うち有効な宣言が 1 つも無い | **124** |
| 何らかの注釈を書いたユニット | 1,602 |
| 木 | 9 / 87 |
| **綴りが正しければ CONTRADICTION** | **2 件**（目視確認済み。85 → 87 になりうる） |

**残る判断 — `r_malformed` の分母（CLAUDE.md 規則 3）:**

* (a) **全ユニット** 130 / 2,231 = **5.8%**
* (b) **何らかの注釈を書いたユニット** 130 / 1,602 = **8.1%**

**(b) の方が「注釈を書こうとした人がどれだけ間違えるか」を表す**が、分母に
`title` だけのユニットも入る。**本文で率を報告する前に決めること。**
両方の値は上の表にあるので、決めたら片方を主、もう片方を併記にする。

---

## O28. `db_unresolved` が記録されずに消える — **解決（D49）。ただし記録した結果 O29 が見えた**

- **状況**（D47 の点検で発見）: 仕様書 1118 行目は
  「解決できない `.execute()` は **`db_unresolved` として記録し**、危険効果に数えない
  （`effect_fp_audit.db_only_non_db_execute` の分子）」と定めている。

  `authgap/effects.py:558-562` は

  ```python
  db_rule = db_execute_rule(...)
  if db_rule != "db":
      return None          # ← 効果ごと捨てる
  ```

  で、**「危険効果に数えない」は満たすが「記録する」を満たさない。**
  `authgap/report.py:169` の `elif e.db_rule == "db_unresolved":` は**到達不能**で、
  `effect_fp_audit.db_only_non_db_execute` は**構造的に常に 0**。
- **誤りの向き**: 仕様が要求した FP 監査の分子が常に 0 になるので、
  **「DB の判定に曖昧さは無かった」と読める出力を出している。**
  受け手型が解決できない `.execute()` は黙って消えており、
  **その中に本物の DB 書き込みがあっても分からない。**
  CLAUDE.md 規則 4（黙って安全側に倒さない）に反する。
- **直し方**: `return None` の前に件数を記録する経路を作る。
  効果として出すかどうかは仕様どおり「出さない」のままでよい。
  **落とした件数を出力に載せる**のが要点（D46 の `n_excluded_opaque` と同じ形）。
- **影響の大きさは未測定。** 落としているので manifest から数えられない。
  **直したときに初めて分かる。**
### 解決（2026-09-23、D49）

**D47 の記述を訂正する。**`if db_rule != "db": return None` は**到達不能な死んだコード**
だった（DB の proxy 行の受け手型はすべて `DB_RECEIVER_TYPES` の部分集合なので、
そこに入る時点で受け手は解決できている）。型が分からない `.execute()` は
proxy 行に一致せず、**痕跡なく消えていた。**

`EffectExtractor.on_call` に `_note_db_unresolved` を足して記録するようにした。
**効果は作らない**（仕様の「数えない」を維持）。verdict は不変
（較正対 14 木 0/0/0、run6 → run7 で全項目一致）。

母集団 v2（`evidence/scan_v2_run7`）: **2,078 件 / 482 ユニット / 19 木**（一意な位置 332）。
DB 効果 230 件に対して**未解決率 90.0%**。→ **O29 へ。**

---


## O29. DB 効果の受け手型が解決できず、SQL 呼び出しの大半を落としている（誤 clear）— **部分的に解決（D50 / D51）。未解決率 90.0% → 24.6%。深さの感度分析は D53（学生の判断待ち: 深さ 3 / 4 / 5）**

- **状況**（D49 で `db_unresolved` を記録した結果、初めて見えた）:
  母集団 v2 で **`.execute()` の 2,078 件（一意な位置 332）が受け手型を解決できず
  DB 効果になっていない。** DB 効果として出ているのは 230 件で、**未解決率 90.0%**。
- **抜き取り 20 件のうち 15 件（75%）が本物の SQL 呼び出しだった**（仕様書 1118 行目が
  求める FP 監査）。一意な位置 332 件を決定論的に並べ等間隔で 20 件を取った。

  ```python
  cur.execute("UPDATE users SET kakao_access_token = %s, ...")     # psycopg
  result = await self.session.execute(select(Game).where(...))     # SQLAlchemy
  db().execute("SELECT * FROM events WHERE session_id = ? ...")    # sqlite3
  ```

  DB でなかった 5 件は Google API クライアントの `.execute()`（Drive 2 / Calendar 1 /
  Gmail 1）と Redis の `pipe.execute()` 1。
- **誤りの向き**: **誤 clear。** 母集団の DB 書き込みの大半が効果として出ていない。
  **規則そのものは仕様どおりに働いている**（解決できないものを DB 効果に数えない）。
  問題は**受け手型の解決力**である。
- **落としている形**（受け手の型が 2,066 件で不明）:
  - `with c.cursor() as cur:` — `with` 文の別名束縛から型が追えない
  - `self.conn` / `self.session` — インスタンス属性の型
  - `db()` — 関数の戻り値の型
- **要る判断**:
  - (a) **受け手型の解決を広げる**（`with` 束縛、`self.<attr>`、木内の
    `sqlite3.connect()` / `psycopg.connect()` の戻り値を追う）。
    **解決率を上げる変更なので CLAUDE.md の敵対的レビューが要る。**
  - (b) **広げず、未解決率 90.0% を限界として報告する。**
    `docs/contradiction_matrix.md` の D1 × DB のマスは「分母が 10 分の 1」と注記する。
  - (c) `.execute()` の受け手が SQL 文字列リテラルを第 1 引数に取るなら DB とみなす
    （**構文的な緩和**。Google API の `.execute()` は引数を取らないので分かれる）。
- **(c) は魅力的だが危険**: SQL に見える文字列を渡す非 DB の API があれば誤警報になる。
  **やるなら fixture で反証を集めてから。**
- **この項目は D1 × DB のマス（O23 #1）より先に決める必要がある。** 分母が
  10 分の 1 のままで率を報告すると、**「DB の矛盾はほとんど無い」と読める。**
### 部分的な解決（2026-09-23、D50。学生の決定は案 (a)）

呼び出し形の型遷移（`CALL_TYPE_TRANSITIONS`）、psycopg 系の CTOR、仮引数の型注釈の 3 つを
直した。**未解決率 90.0% → 26.2%、DB 効果 230 → 1,705。** 消えたユニット・CONTRADICTION・
`GAP_INJECT` はいずれも 0。新しく出た DB 効果の抜き取り 20 件は**すべて本物**。

**残り（`db_unresolved` 605 件、一意 205）の抜き取り 20 件: 本物の SQL 14 / Google API 6。**
まだ 7 割が本物の SQL で、残っている書き方は

- `self._conn` / `self.conn` — `__init__` で `sqlite3.connect(...)` を代入しても、
  ツールからメソッドに降りる経路で `self` の型が付かない
- `db()` / `self._connect()` — 木内の補助関数の戻り値（降下の深さや名前解決で落ちている
  可能性。未確認）
- **注釈の無い** `session` / `conn` 仮引数

**要る判断**: 続けて広げるか、ここで止めて残りを限界として報告するか。
続けるなら同じく敵対的レビューが要る。止めるなら「DB 効果の未解決率 26.2%（一意 205 か所、
抜き取りで 7 割が本物の SQL）」を本文の限界節に書く。
→ **学生の決定は「続ける」（2026-09-23）。D51 へ。**

### その 2（2026-09-23、D51）— **残りの 92.4% は深さの上限**

`Cls(...).m()` / `@contextmanager` / 戻り値の注釈の 3 つを直した。未解決率 26.2% → **24.6%**。
回帰 0。DB 以外の新しい効果 5 件（SPAWN 4 / NET 1）もすべて本物。

**残り 569 件のうち 526 件（92.4%）は、深さの上限（`MAX_DEPTH = 3`）に当たったユニットの
中にある。** 実験（解析器は変えず `Options(max_depth=5)` で 1 木ずつ）で因果を確かめた:
`teamplay-talk` 154 → 24、`cohort` 64 → 13（DB 効果 0 → 312）。所要時間はほぼ変わらない。

**要る判断（学生）**:

- (a) **`MAX_DEPTH` を上げる**（例: 3 → 5）。**事前登録した上限**（解析指紋の `caps`）なので
  逸脱として記録する。**DB に限らず全 kind・全判定が動く**（CONTRADICTION も増えうる）。
  2 木では所要時間がほぼ変わらなかったが、**母集団全体の費用は未測定**
  （`david-li0406` はすでに 180 秒の tree budget で打ち切られている）。
  上げるなら先に `max_depth` 別の感度分析を全木で取り、費用と増分を見てから決めるのが安全。
- (b) **上げない。**「DB 効果の未解決率 24.6%、うち 92.4% は深さ 3 の上限による」を
  限界として報告する。**上限そのものは `cap_hits` に記録されているので、黙って落として
  いるのではない。**

**深さと無関係に残る形（`dejavu`、94 件）**: `@property` と、フレームワークが渡す値の
注釈付き代入（`db: DejavuDB = ctx.request_context.lifespan_state["db"]`）。
どちらも DB を超えた一般的な変更なので未着手。

### その 3（2026-09-24、D53）— 全木の感度分析（深さ 3 / 4 / 5）

学生の決定「上げる前に全木で感度分析をする」に従って測った。**解析器は変えていない。**
詳細は `docs/decisions.md` D53、表は `docs/depth_sensitivity.md`。

| | 深さ 3（現行） | 深さ 4 | 深さ 5 |
|---|---|---|---|
| DB 未解決率 | 24.6% | 17.6% | 14.2% |
| CONTRADICTION | 85 | 146 | 193 |
| 所要時間（86 木、単独） | 396 秒 | 424 秒 | 490 秒 |
| 消えたもの | — | 0 | 0 |

増えた CONTRADICTION 108 件を全件原典で確かめた: **本物 63 / 遠隔の応答次第 28 /
規則どおりだが意味は非破壊 12 / 誤検出 5**。別に、増えた効果の経路の 26%（深さ 4）が
末尾名の誤解決の連鎖（xagent の `logger.error` → テストファイル内のクラス）だった
（`UNKNOWN` の行に出る）。

**要る判断（学生）**:

- (a) **`MAX_DEPTH` を 4 に上げる。** 増分の大半（位置 +865 / CONTRADICTION +61）を取り、
  時間は +7%。誤検出 5 件はすべてここで出る。
- (b) **5 に上げる。** さらに位置 +178 / CONTRADICTION +47（誤検出は 0、本物 28・遠隔次第 15・
  非破壊 4）。時間は +24%（`canvas-mcp` が 3.2 倍）。
- (c) **3 のまま。** D53 の数字を限界節に書く（「深さ 3 では DB の未解決 24.6%。深さ 5 なら
  CONTRADICTION が 2.3 倍になり、増分の 58% は手検証で本物」）。

どれを選んでも、**事前登録した上限の変更は `docs/preregistration.md` に逸脱として記録する**
（(c) なら記録は要らない）。また (a) / (b) で主指標を出し直すなら、深さ 3 の値も併記する。

---


## O19. 先行研究 3 本が主軸と競合する可能性 — **解決（D40: 3 本とも一次資料を読んだ。判断は (a)「測定研究として立て直す」）**

**2026-09-22 追記（D39）**: 学生が PDF を提供し、R2（AgentFlow）と R3（ReactAppScan）を読了。
**R2 は競合しない。** 解析対象がエージェント プログラム（MCP を使う側）で、MCP サーバの実装は
読まない。注釈（`readOnlyHint` 等）の出現は本文 0 件。しかも限界節が「ツール実装の内部を
推論する仕事には ADG は使えない」と自ら書いており、そこが AuthGap の守備範囲である。
**R3 は手法の型として引ける**（別名を 1 ノードにする、キーで境界を越える、評価の 2 データセット構成）。
**残るのは R1（HintLint）のコード読解のみ。** 詳細は `docs/related_work.md`。

以下は 2026-09-21 の記述（PDF を読む前）。

- **状況**: D36 で主張を「宣言 D と実効 M の照合」1 本に絞った直後（2026-09-21）に、
  次の 3 本が見つかった。`docs/related_work.md` に読む欄を作ってある。
  - **HintLint**（https://github.com/complira/hintlint）: **主軸そのもの**。MCP の注釈と
    実装の食い違いを静的に検出する。Python 対応。ページは読んだ（規則 6 種、
    source-backed に限る設計）。評価値（20 リポジトリ 1,160 ツール、精度 82%）は**未検証**。
  - **AgentFlow**（arXiv 2607.01640、2026-07）: エージェント依存グラフ。MCP capability を
    扱うとある。**代替案として検討したグラフ化はここで埋まっている可能性**。**未読**。
  - **ReactAppScan**（CCS '24）: 手法の型として参考にした論文。**未読**。
- **なぜこの環境で読めないか**: `yinzhicao.org` / `arxiv.org` / `semanticscholar.org` は
  この実行環境の egress proxy で遮断されている。**学生の手元の PDF が要る**（手順は
  `docs/related_work.md` 冒頭と D38）。
- **要る判断**: 一次資料を読んだうえで、(a) 測定研究として立て直す（母集団の定義・
  事前登録・opaque の率の報告が差分になる）、(b) 主軸を変える、(c) 変えない、のどれか。
- **それまでやらないこと**: 主張の書き方を確定させる作業（本文の構成、限界節の文言）。
  **入口カタログの網羅性と CONTRADICTION の手検証は、どの結論でも価値が変わらないので
  先に進めてよい。**
  → **2026-09-22: R2 / R3 が片付いたので、この制約は R1 にだけ残る。**
- **誤りの向き**: 先行研究を見落としたまま書くと、貢献の主張が過大になる（是正不能な誤り）。

### 決着（2026-09-22、D40）

**R1 もソースを読み、母集団 v2 の 87 木で実際に走らせた**（`evidence/hintlint_run1/`）。
判断は **(a)「測定研究として立て直す」**。(c)「変えない」ではない。

* HintLint の比較可能な finding 65 件のうち **61 件は宣言が無いツール**で、AuthGap の
  CONTRADICTION（宣言があって反する）とは別の現象。**真に比較できたのは 4 件で、1 勝 3 敗。**
* 差分は **「解決できなかったものをどう扱うか」**。HintLint の確度の語彙は 2 語で、
  未解決を表す語が無い。正規表現に当たらなければ分母からも消えるので、
  **率の問いには答えられない。** ここが AuthGap の位置である。
* **「初めて照合した」とは書けない。** 書けるのは母集団の定義・事前登録・未解決の率の報告。
* **副産物として AuthGap の誤 clear が 1 件見つかった** → O22。分母の問題が 1 件 → O21。

この項目で止めていた「主張の書き方を確定させる作業」は**解禁**である。

---

## 参考: 質問ではなく作業として残っているもの

- **較正対の検証**: `docs/cve_triage.csv` の 25 行のうち一次確認できたのは
  7 対（A1–A5、A9+A10、A18）。残り 18 行は `verified_by_me = none` で
  **仕様書からの転記であって未検証**。手順は
  `docs/verification_guide.md` の 2.1〜2.3。
- **§6 T1.5 (ii)**: Semgrep OSS / Pysa との対ごと突き合わせが未実施。
  合格条件 3 つのうちこれだけが残っている。
- **§3 の交差行**: **決着（D36）**。母集団 v2 でも 5 行 / 2 プロジェクトで不合格
  （旧枠は 12 行 / 1 プロジェクト）。D10 の二択は**格下げ分岐**を採り、標本は作り直さない。
  残る作業は、この数を 3 腕アブレーション（`scripts/ablation.py`）で裏づけて
  `docs/intersection_rows.md` に残すことだけ。
- **§9 の未検証リスト 13 項目**: 1〜5・9〜13 は較正対の検証と重なる。
  6（母集団規模 ≥ 300）は通過済み（`docs/population.md`）。7（先行研究の一次資料）と
  8（Semgrep の機能境界）は未着手。
- **§2.6 の val 受け入れ fixture F1–F10**: 期待値 `fixtures/val/expected.json` と
  採点器 `tests/test_val_fixtures.py` を作った（O17）。残る作業は F9（agno 本体
  `libs/agno/agno/tools/shell.py` の取得と SHA の pin）と F10（`restapi.amap.com` を
  叩くツールの repo の選定 — 仕様書は名指ししていない）。
- **`_sub_kind` の DB 分類のバグ 2 件**（D41 で表を書く作業が見つけた。`SUB_KINDS` の
  語彙には触れず、`authgap/effects.py: _sub_kind` の分類規則だけの修正）:
  - **B1**: `head = text.strip().split(" ", 1)[0]` が `" "` だけで切るので、
    `"\n  SELECT\n    id, ..."` のような**改行で始まる複数行 SQL** が `"SELECT\n"` になり、
    読み取り語の一覧に当たらず `DB_WRITE` になる。母集団 v2 で 2 件。
    **向きは誤警報（false-positive）。** `split()`（空白全般）にすれば直る。
  - **B2**: 読み取り語の一覧に無ければ `DB_WRITE` なので、`PRAGMA`（接続設定）と
    `BEGIN` / `COMMIT` / `ROLLBACK`（トランザクション制御）がデータの書き込みと
    同じ sub_kind になる。母集団 v2 で `PRAGMA` 101 / `BEGIN` 1 / `COMMIT` 2 /
    `ROLLBACK` 1。**O23 #1 を決める前にこれを直す。**
- **「不明」を verdict として出す経路**（規則 4。**向きは誤 clear**）: 母集団 v2 で
  **833 件**が黙って落ちている（`NET` のメソッドが実行時引数 832 件 =
  `httpx.AsyncClient.request(method, …)` ほか、SQL が読めない 1 件）。
  `docs/contradiction_matrix.md` §7 の手順 3。**矛盾を増やすことより先に効く。**
- **カタログ外のツールの形**（D17「直さない 3」）: llama-index
  `FunctionTool.from_defaults` / `QueryEngineTool`、SuperAGI `_execute`、OpenManus
  `BaseTool.execute`、OpenHands `ToolDefinition`、claude_agent_sdk `tool(...)` など。
  広げるなら月 10 の指紋凍結前に、**F0a 標本の外の根拠**（公式文書）で行う。
