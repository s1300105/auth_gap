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

## O12. 判別実験の判定規則が第 3 類型（CodeQL が両側とも報告）を想定していない。等級づけを章に立てるか

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

## O15. `r_D` の分子の定義が実装内で食い違う（上界を動かす明示 53.3% / 明示 1 つでも 80.0%）

- **要る情報**: 仕様書 §10 :1121〜1124 の `r_kind` の定義を、`D_kind ≠ ⊥`（上界を
  動かす明示: `readOnlyHint==true` / `destructiveHint==false`）と読むか、
  `openWorldHint==true` 単独の明示も含めるか。
- **背景**: `scripts/f0a.py:390` は前者、`authgap/dparse.py: parse_d_kind` の
  docstring は後者。旧枠では両方 0 で見えなかった。母集団 v2（D30）では
  547/1,027 = 53.3% と 822/1,027 = 80.0%。どちらでも §10 は分岐 1。
- **誤りの向き**: 分子の選び方で `r_D` が動くが、判定（分岐）は動かない。本文では
  両方を併記し、どちらを主にするかを決めてから固定する。

---

## O16. `destructiveHint==false` の宣言に対して、追記型の FS_WRITE を CONTRADICTION に数えるか

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

## 参考: 質問ではなく作業として残っているもの

- **較正対の検証**: `docs/cve_triage.csv` の 25 行のうち一次確認できたのは
  7 対（A1–A5、A9+A10、A18）。残り 18 行は `verified_by_me = none` で
  **仕様書からの転記であって未検証**。手順は
  `docs/verification_guide.md` の 2.1〜2.3。
- **§6 T1.5 (ii)**: Semgrep OSS / Pysa との対ごと突き合わせが未実施。
  合格条件 3 つのうちこれだけが残っている。
- **§3 の交差行**: 12 行 / 1 プロジェクトで不合格。低レベル MCP サーバを
  あと 2 プロジェクト足すか、§3 の格下げ分岐に入るかを C1 の標本抽出**前**に
  決める（`docs/decisions.md` D10）。
- **§9 の未検証リスト 13 項目**: 1〜5・9〜13 は較正対の検証と重なる。
  6（母集団規模 ≥ 300）は通過済み（`docs/population.md`）。7（先行研究の一次資料）と
  8（Semgrep の機能境界）は未着手。
- **§2.6 の val 受け入れ fixture F1–F10（`fixtures/val/expected.json`）が未作成。**
  F5–F8 は `FoundationAgents/OpenManus` の `app/tool/` が出所（コーパスに取得済み、
  commit 3309bf4e）。期待行は仕様の表から先に pin し、採点器より先にコミットする。
- **カタログ外のツールの形**（D17「直さない 3」）: llama-index
  `FunctionTool.from_defaults` / `QueryEngineTool`、SuperAGI `_execute`、OpenManus
  `BaseTool.execute`、OpenHands `ToolDefinition`、claude_agent_sdk `tool(...)` など。
  広げるなら月 10 の指紋凍結前に、**F0a 標本の外の根拠**（公式文書）で行う。
