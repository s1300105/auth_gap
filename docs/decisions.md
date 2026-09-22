# 決定した事項（根拠つき）

仕様書 `AUTHGAP_BRIEF_v3.md` の記述と実データが食い違った点、および仕様書が
決めていなかった点について、**実装側で判断して確定させた**内容を残す。
後から追認できるように、どの証拠でそう決めたかを必ず書く。

**仕様書本体は書き換えていない。** 仕様書は設計の記録として残し、
食い違いはここと `docs/cve_triage.csv` に併記する。

最終更新 2026-09-22（D39 を追加）。

---

## D39. 先行研究 2 本を読了。**AgentFlow は競合せず相補的**。主軸は変えない（O19 の (c)）

### 何をしたか

学生が R2（AgentFlow）と R3（ReactAppScan）の PDF を提供したので読んだ（この実行環境は
arxiv.org と著者サイトを egress proxy で遮断している）。読んだ結果は
`docs/related_work.md`。**読んだ節を明記し、未精読の節は未精読と書いた。**

### 判断: 主張を変えない

D36 で絞った「宣言 D と実効 M の照合」を主軸のまま維持する（O19 の選択肢 (c)）。
根拠は次の 2 点。

**1. AgentFlow は解析対象が違う。** 対象は「エージェント プログラム」= MCP を**使う側**の
コードで、論文の scope はエージェント製品と低コード エージェントを明示的に除外している。
MCP ツールはクライアント側の `HostedMCPTool(...)` から作る `MCPDef` ノードであって、
**サーバの実装は読まない。** 注釈（`readOnlyHint` / `destructiveHint` / `openWorldHint` /
`annotation`）の出現は本文で **0 件**（全文検索で確認）。宣言と実装の照合という問いを
立てていない。危険の定義も違い、AgentFlow は「prompt 由来のデータが特権 capability の
引数に届くか」（prompt injection の到達性）である。

**2. AgentFlow の限界節が AuthGap の位置を名指ししている。** 著者の言葉:
「ADG は高水準のフレームワーク意味論を捉えるものであり、低水準のプログラム依存解析を
置き換えない。**ツール実装やライブラリ呼び出しの内部を推論する仕事**には points-to 解析と
組み合わせる必要がある」。**その「内部」が AuthGap の守備範囲である。**

したがって当初「グラフ化案と競合する」と見ていた評価は**誤り**で、正しくは**相補的**である。
グラフ化そのものを追わない判断（D36 の帰結）は変わらないが、理由が変わる。
「先を越された」のではなく「別の層の話」である。

### R3 から引けるもの（手法の型）

ReactAppScan の Component Graph は、(a) **別名のオブジェクトを 1 ノードにする**
（親の state と子の prop は 1 ノード）、(b) **キーで境界を越える**（DB のキー、ルート名で
クライアント / サーバ / DB を結ぶ）、(c) 抽象解釈で構築し抽象領域がグラフそのもの、
という骨子。**(a)(b) は「同じ資源を触る複数ツールを 1 ノードにする」= サーバをまたぐ
合成のリスクに写せる。** 将来この方向に進むなら引く先になる。

評価の設計も引ける。**大規模ラベルなしで偽陽性率、小規模ラベルありで偽陰性率**という
2 データセット構成で、AuthGap の較正対（CVE）と母集団 v2 は同じ構成である。

### 残っていること

**R1（HintLint）のコード読解。** 主軸と直接競合する唯一の研究で、ここだけ未確定。
最重要の確認点は「**解決できなかったものをどう扱うか**」。落としているなら分母から
消えるので率を報告できず、そこが AuthGap との差分になる。ページには
「source-backed findings に限り metadata-only の検出を避ける」とあるが、実装は未確認。

### 誤りの向き

**当初の評価（R2 が競合する）は、検索結果の要約だけで判断したことによる誤りだった。**
一次資料を読むまで位置づけを確定しないという O19 の方針が正しく働いた。
逆に、もし要約のまま「先を越された」と結論していれば、主軸を不要に変更していた。

---

## D38. 先行研究の PDF は repo に入れず、読んだ結果だけを `docs/related_work.md` に残す

### 決めたこと

先行研究 3 本（O19）を記録する手順を固定する。

1. **PDF 本体はコミットしない。** `origin` は公開リポジトリ（`github.com/s1300105/auth_gap`）
   なので、論文 PDF を置くと著作物の再配布になる。置き場は `papers/` で、`.gitignore` 済み。
2. **コミットするのは `docs/related_work.md` だけ**（自分の言葉で書いた要約と、AuthGap との
   重なり・違いの表）。引用は必要最小限の短い語句に留める。
3. **一次資料を読んだ項目と、検索結果から書いた項目を分けて書く**（CLAUDE.md 規則 1）。
   後者は「未検証」と明示する。埋まっていない欄は `（未記入）` のまま残し、推測で埋めない。
4. **出所を書く**（どのページ / どの節を読んだか）。

### PDF をこの実行環境に届ける経路（3 通り。上から推奨順）

| # | 経路 | 長所 | 短所 |
|---|---|---|---|
| 1 | チャットに PDF を添付する | repo が汚れない。履歴に残らない | 添付が大きいと分割が要る |
| 2 | `papers/` に置いて**使い捨てブランチ**で push し、読んだら破棄する | 確実 | 一時的にせよ公開 repo の履歴に載る。**推奨しない** |
| 3 | 要点（abstract / 手法の節 / 評価の表 / limitations）を本文として貼る | 著作物を配布しない | 手間がかかる。読み落としが出る |

**経路 2 を採る場合も、作業ブランチ（`claude/...`）には決して混ぜない。**

### この環境から直接取得できない理由

`yinzhicao.org` / `arxiv.org` / `semanticscholar.org` / `alphaxiv.org` は実行環境の
egress proxy で遮断されている（2026-09-21 に確認。`EGRESS_BLOCKED`）。
到達できたのは `github.com` と `blog.modelcontextprotocol.io` のみ。
**「調べたが見つからなかった」ではなく「この環境から読めなかった」**と区別して記録する。

---

## D37. 事前定義の地図を作り、核（2 種類 + 自己申告）と付録（降ろした主張）を分ける。**解析器は変えない**

### 学生の問い（2026-09-22、チャット）

「まとまりがないと感じるのは事前定義の部分。危険な呼び出し、値の変換、間接呼び出し、
検証子の形、弱い検証の理由、わからない理由。こんなに多くの種類を事前に定義する部分だ」。
続けて「減らして精度が下がるならそのままでよい」「その事前定義は一般に知られているもので
簡単に書けるのか、自分で一から考える必要があるものか」。

### 決めたこと

**解析器と語彙は一切変えない**（精度を動かさないため）。**説明の構造だけ**を直し、
`scripts/catalog_map.py` と `docs/catalog_map.md` で再現できる形にした。

1. 表を**役割**で 3 つに分ける。核 = 「宣言 D と実効 M の照合」に要るもの。
   付録 = D36 で降ろした主張（等級づけ / ゲート / SELECT）のもの。索引 = 派生。
2. 表を**出所**で分ける。転記 = Python と主要ライブラリの常識で、既存の静的解析器も
   同等の表を持つもの。領域固有 = この研究で決めたもの。engine = 解析器の自己申告。
3. **役割と出所の分類は判断であって測定ではない**ことを script と文書の両方に明記する。
   分類を変えるときはこの節も直す。

### 測った値（2026-09-22、`evidence/scan_v2_run4`）

| 役割 | 表 | 行 |
|---|---|---|
| 核 | 22 | 243 |
| 付録（降ろした主張） | 30 | 200 |
| 索引（派生） | 8 | 119 |

核 243 行の出所: **転記 172 / この研究で決めた 53 / 解析器の自己申告 16 / 記録 2**。

**核の主張が実際に使っている行**（CONTRADICTION 79 件から逆に数えた）:

- 関係した API は **13 種類**（`DIRECT_SINKS` 67 行のうち）。`PROXY_SINKS` 16 行と
  `PIPE_SINKS` 2 行は **1 件も使われていない**。
- 効果の形は全部 `direct`。呼び出しの降下は 3 段が 57、2 段が 39、1 段が 27、同じ関数内が 4。
- 13 種類は `builtins.open` / `os.chmod` / `os.makedirs` / `os.remove` / `os.replace` /
  `os.unlink` / `pathlib.Path.{mkdir,open,unlink,write_bytes,write_text}` /
  `shutil.rmtree` / `subprocess.run`。**ファイルを書く・消す系と、プロセスを起こす系だけ。**

### 学生の問いへの答え

**「自分で一から考える必要があったか」への答え: ほとんどは転記である。** 危険な呼び出し
（`subprocess.run` / `builtins.eval` / `shutil.rmtree` / `httpx.get`）、値の変換
（`realpath` / `Path.resolve` / `shlex.quote` / `urlparse`）、間接呼び出し
（`multiprocessing.Process` / `Thread` / `partial` / `submit`）、ライブラリ ctor
（`sqlite3.connect` / `httpx.Client` / `git.Repo`）は Python の常識で、既存ツールも
同等の表を持つ。**量はあるが難しさは無い。**

**一から考えたのは `ENTRY_RULES`（ツールの入口 14 形）**である。`@mcp.tool` / 低レベル
MCP の 2 形 / langchain の `@tool` と `_run` / crewai `_run` / openai-agents
`@function_tool` / semantic-kernel `@kernel_function` / agno `Toolkit` / gptme
`ToolSpec` / autogpt `@command` / langroid `ToolMessage`。**既存の静的解析はどの枠組みの
入口も知らないので代替が無く、これが領域固有の貢献の中心である。** これに削除型 / 追記型の
印（D32）と、kind から宣言の上界への対応（`READ_ONLY_UPPER` ほか）が加わる。

**一番「自作」だったのは検証子の形 12 と弱い検証の理由 22**（`no_dashdash` /
`prefix_no_boundary` / `validate_then_fetch` など。文献に無い）で、**これは D36 で
降ろした主張のものである。** 「種類が多い」と感じた原因の中心はすでに核から外れている。

### 副産物: 母集団の宣言が割れている API

同じ API を呼ぶツールで readOnly と destructive の明示が両方現れる site が、
3 ユニット以上から呼ばれる site のうち **20 / 41** ある。`os.unlink` を
`readOnlyHint` つきで呼ぶツールが 6、`subprocess.run` を `readOnlyHint` つきで呼ぶ
ツールが 12 ある。

**多数決を真理として使ってはならない。** `subprocess.run` は readOnly が多数派になるが、
プロセス起動が読み取り専用であるはずがない。この表が言えるのは「少なくとも一方が誤っている」
までで、正解を決める材料ではない。**「宣言が割れた API だけを人が裁定し、カタログの
意味付けをそこに絞る」案の下見であり、採否は未決**（`docs/open_questions.md` O20）。

なお会話中に口頭で「12 種類」と述べたが、条件を揃えて数え直すと **20 種類**である
（`readOnly` と `destructive` の両方が現れる、という条件。script が唯一の定義点）。

### 変えないこと

コード、語彙、閾値、事前登録は一切動かしていない。`docs/catalog_map.md` は説明のための
地図であって、解析の入力ではない。

---

## D36. 主張を「宣言 D と実効 M の照合」1 本に絞る。3 座標の統合（脆弱版 / 修正版の判別）は主張から降ろす

### 学生の決定（2026-09-21、チャット）

**「下の行は必要ない。」** 下の行とは、下表の 2 行目を指す。

| # | 主張 | 使う機構 | 決定 |
|---|---|---|---|
| 1 | 宣言 D と実効 M が食い違う | 効果 kind の検出と D のパースだけ | **主軸にする** |
| 2 | 3 座標（trig / val / gate）の統合で脆弱版と修正版を判別する | trig + val + gate 全部 | **主張から降ろす** |

これは `docs/open_questions.md` O12 の案 (β)（等級づけを章に立てず、manifest 属性と
fixture / mutant のカタログとして報告する）の採択にあたる。D24 の 3 段のうち
**B 段（ゲート等級）を C 段（道具）に落とす**。

### 根拠（この決定より前に測った値）

仕様書 §3 は「これは一つの解析ではない。三つの別々に計算される座標の上の一つの判定である」と
自ら書き、統一の**唯一の証拠**として交差行を事前登録している。母集団 v2（宣言を持つ
MCP サーバ 87 木、`evidence/scan_v2_run4`）で測ると次のとおりで、**事前登録の条件を
2 つとも満たさない**。

| 項目 | 実測 | §3 の条件 |
|---|---|---|
| 交差行の候補（SELECT 系と INJECT 系を同時に持つ行。ユニット × site × slot） | 5 | 3 以上 |
| その由来プロジェクト数 | 2（`fanfan-de/anybox`、`ariffazil/wealth`） | 3 以上 |
| trig が `traced` のユニット | 14 / 2,231 = **0.6%** | 20% 以上 |

**3 行目の条項は仕様書が「撤回しない」と書いたものである**: 「traced 率が 20% 未満なら
SELECT の野外評価は成立しないので、その時点で SELECT は fixture + ケーススタディのみの
構造的主張に格下げする」。実測 0.6% なのでこの条項は発火する。MCP サーバは dispatch が
フレームワーク内にあるため木の中で「モデルがこのツールを選んだ」を追跡できない。
これは実装の不足ではなく構造的な事実で、母集団を宣言ありに変えた D29 の帰結として固定である。

旧枠での交差行は 12 行あったが全部 1 プロジェクト（mcp-server-git）由来で、D10 で
すでに不合格だった。母集団 v2 で 2 プロジェクトに増えたが届いていない。

**なお上の交差行の数は「同一行が SELECT 系と INJECT 系を同時に持つ」という §3 の特徴づけで
数えたものであって、3 腕アブレーション（`scripts/ablation.py`）を回した値ではない。**
§3 は両者が一致すると書いているが、本決定を数値で裏づけるなら腕 A / B / C を回して
確かめる必要がある。**降ろす決定には不利に働かない**（腕を回して増えることはあっても、
プロジェクト数が 2 から 3 に増える保証は無い）ので、この決定の前提としては 2 プロジェクトを採る。

### 主軸に残るもの

母集団 v2 の full scan で CONTRADICTION が 79 件（16 木、`evidence/scan_v2_run4/contradictions.json`）。
`authgap/verdict.py: _contradiction_of` は D_kind の上界と効果の kind を比べるだけで、
**gate の等級も val の主体も使わない**。したがって主軸の主張は下の機構だけで立つ。

- Def 2 の R2（ツール入口のカタログ）
- 効果 kind の検出（sink カタログ、7 kind）と slot 束縛
- D のパース（`readOnlyHint` / `destructiveHint` / `openWorldHint` → 上界）
- Def 7 の CONTRADICTION（効果ごと、削除・上書き型のみ。D32）
- 測定規律（決定論、事前登録、opaque を clean に潰さない、両側の分母併記）

### 変わること

1. **O12 は解決**（案 (β) を採択）。
2. **O8 / O10 / O11**（Def 5 の条件 (ii)(iii) と袋詰め採点の未実装）は、**主張の穴では
   なくなり、道具の限界の記述に変わる**。false-clean 方向であることは変わらないので、
   限界節と manifest の注記には残す。**直す優先度は下がる。**
3. **D10 の分岐**（低レベル MCP サーバを標本に足すか、§3 の格下げ分岐に入るか）は
   **格下げ分岐を採る**で確定。標本を作り直さない。
4. **判別実験（両側較正 T1、`two_sided.py` の腕 C / C0、CodeQL 比較）は主軸から外れ、
   道具の妥当性確認として報告する**。較正対そのものは「解析器が実在の CVE の効果行を
   正しく出すか」の検査として残る（これは主軸にも要る）。
5. **§10 の validator 保有の関門**は、等級づけを章に立てないので「この研究を続けるか」の
   関門としての役割が薄くなる。数値は併記のまま残す（O7 の承認とは独立）。

### 変えないこと

**コードは消さない。** gate / val の機構は GAP_INJECT 行と manifest の属性を出し続け、
fixture と mutant のカタログ（`tests/test_value_grade.py`、`tests/test_d21_adversarial.py`、
`fixtures/dominance_mutants`、`fixtures/gates`）も回帰試験として残す。**消すと、後から
「なぜその設計を降ろしたか」を示す材料が無くなる。**

### 逸脱であること

**この決定は事前登録した主張を、結果を見た後に降ろすものである。**
`docs/preregistration.md` §5 に逸脱 #11 として記録した。降ろす方向（主張を弱める側）で
あり、通らなかった条件を後から緩める向きではない。

---

## D35. val エンジンの受け手型の修正（F6/F7/F8）と敵対的レビュー: 7 規則、反証 13 形、直した後の残る限界

### 何を直したか（551f23e → 38531e7）

O17 (c)(d)(e) の 3 件（OpenManus Bash / StrReplaceEditor / crawl4ai で効果行が出ない、
false-clean 方向）を直すために、val エンジンに次の規則を入れた。**いずれも
opaque → resolved の向きの変更**なので、CLAUDE.md の約束どおり敵対的レビューを通した。

| 規則 | 内容 | 直した取りこぼし |
|---|---|---|
| (a) | `Obj ⊔ None` リテラル → `Obj`（`Atom.none` で None リテラルを「定数不明」と区別） | `Optional[_BashSession] = None` との合流で受け手型が消えていた |
| (b) | 木内クラスの構築時にクラス体の既定値を `Obj.fields` に入れ、`__init__` で上書き | `command: str = "/bin/bash"` が読めなかった |
| (c) | 型で裏付けられた降下の後、被呼び出しの `self.<f>` 書き込みを受け手の経路と fields に戻す | `_BashSession.start` の `self._process` を `run` が読めず EXEC@pipe が出なかった |
| (d) | 受け手が 2 型以上の `Obj` で各型に候補が 1 つずつあれば全候補へ型を絞って降りる | `operator.write_file` が Local / Sandbox の 2 型で opaque のままだった |
| (e) | `str.encode` / `bytes.decode` を内容不変の TRANSFER に | `command.encode()` で MODEL と root が落ちていた |
| (f) | sink の `A(pos, kw=)`: 位置に無ければ仮引数名のキーワードで引く | crawl4ai `arun(url=...)` の slot が空で行が出なかった |
| (g) | 常にシェル経由の SPAWN sink に `exec_mode.shell = OP/True/implicit` | `create_subprocess_shell` に shell の記録が無かった |

### 敵対的レビューの結果（2 本、読み取り専用の agent、反証木 24 本）

規則 (a)(f) は反証なし。(g) は等級・判定の変化なし（併せて既存の穴が 1 つ見つかった: proxy の
SPAWN に一律 `const False` を付けていたため paramiko `exec_command` のシェル文字列の
検証子が strong-token に上がっていた。直した）。**(b)(c)(d)(e) で false-clean が 13 形**:

- (b) 既定値が、エンジンに見えない MODEL の書き込みを覆い隠す: 呼び出し側の `r.cmd = cmd`
  （env の鍵と `Obj.fields` が別の記憶）、`super().__init__(cmd)`（未解決）、`__init__` が深さ /
  再帰 / cap で走らなかったとき、別名 `b = a` 経由の書き込み。import 時の構築の効果行が
  ツールに付く（false-dirty）。
- (c) 書き戻しが上書きだった: 条件つき書き込み `if flag: self.cmd = "ls"` が MODEL を OP に、
  分割降下の候補間で最後の候補が勝ちクラス名の並び順で答えが変わる、`Obj ⊔ Obj` の合流が
  fields を全部落とし（ループ 2 周目で MODEL → OP）。
- (d) 候補の無い型の経路が無言で落ちる（`<=`）、末尾名で別モジュールの同名クラスへ降りる、
  絞った型で書き戻すと 2 型目以降の経路が消える。
- (e) 受け手主語の TRANSFER が木内の `Codec.encode` を横取りし、その中の sink 行が丸ごと
  消える（`split` / `strip` 等の既存の穴と同じ機構）。

**すべて直した**（38531e7 のコミットメッセージに 1 件ずつ）。要点: 書き戻しは合流、降りる前に
経路書き込みを fields に載せる、`Obj ⊔ Obj` は fields を名前ごとに合流、`super()` を解決、
既定値の確度に「走らなかった理由」を合流、分割は全型一致 + 同名クラスが一意のときだけ、
TRANSFER は木内メソッドを横取りしない。反証木 24 本で false-clean 0（d4 は opaque に戻る）。

### 残る既知の限界（本文の限界節に書く）

1. **別名**: `b = a` の単純な別名は同一オブジェクトで追うが、コンテナ / 引数 / 戻り値経由の
   別名は追わない（前からの限界）。
2. **`Obj.classes` は末尾名**でモジュールを持たない。同名クラスが木に 2 つ以上あるときは
   分割降下しない（opaque のまま）ことで誤降下を避ける。単一型の解決も末尾名なので、同名
   クラスの取り違えは前からある（`_class_family`）。
3. **継承メソッド**は分割降下の対象外（候補が基底にあると「各型に 1 つ」が成り立たない）。
4. **remote クライアントの sink カタログが無い**ので F7 の sandbox 側（`resolution=remote`
   の行）は出ない。
5. 経路非感応: `except` 側の `WebSearchResult(link=None)` のような dead な経路にも行が出る
   （A18 の NET 2 行に `OP/resolved` の変種が加わった。false-dirty 側）。

### 較正対と fixture

- `diff_effects --before 967cab1` 較正 14 木: 行 0 消失 / 0 増加、slot 変化は A18 の上記 2 行のみ。
- `tests/test_val_fixtures.py`: F6 EXEC@pipe（code_text=MODEL/{command}）、F7 FS_WRITE
  （path=MODEL/{path}）、F8 NET（url.host=MODEL/{urls}）の 11 項目が XPASS → 印を外した。
  残る未達 14 項目は語彙の差（`argv0` / `shell_string`、呼び出し点ごとの複製、witness_chain
  に入口を含めない）と未出力（`depth_used`、`Seq.tail`、remote 行）。
- 副産物: OpenManus StrReplaceEditor の `view` が `find {path} -maxdepth 2 ...` を
  `create_subprocess_shell` に渡す SPAWN 行（shell_string=MODEL/{path}）が出る。

### 母集団 v2 の取り直し（解析器 38531e7）

prereg §5 #10 の逸脱として、変更前（235ae1e 系: run1 / run2 / scan run3）と変更後を併記する。
budget は §2.1 の 180 s（run1 と同じ。飛ばしたユニット 716 も同じ 1 木）。

| 指標（mcp_server、87 木） | 変更前 | 変更後（38531e7） |
|---|---|---|
| ユニット / 危険ユニット | 2,231 / 1,027 | 2,231 / **1,169**（+142、外れた 0。6 木、うち canvas-mcp +86、cohort +51） |
| validator 保有（主分母） | 3.51% × | 4.11%（48/1,169）×。木単位 95% 区間 [1.4%, 12.4%]（境界） |
| validator 保有（all_units） | 3.77% × | 3.77% ×（分子 84 は同じ。区間 [1.9%, 7.2%] 境界） |
| validator 保有（dangerous_non_net） | 18.3% ○（34/186） | 17.4% ○（34/196） |
| in_tree_resolution_ratio（サイト） | 21.7% × | 22.5% × |
| opaque 率（主 slot、サイト） | 54.7% × | 52.8% × |
| r_D（上界を動かす明示 / 危険ユニット） | 53.3% | 51.1%（分岐 1 のまま） |
| full scan: CONTRADICTION（ユニット × site） | 72（16 木） | **79**（16 木。増分 7 はすべて cohort `TaskStore._save_tasks` → `Path.write_text`。消えた 0） |
| full scan: 行数 / GAP_INJECT 行 | 4,804 / 197 | 9,492 / 767（**行は呼び出し経路ごとに複製され cap が効いていない**。O18。ユニット単位で比較する） |

読み: 変更はユニット単位では「危険ユニットが 142 増え（API ラッパ / 状態ファイルの
書き込みが解決した）、validator 保有は分子が増えず分母が増えた」向きで、関門の合否は
どれも変わらない。CONTRADICTION は 7 件増え、手検証の候補表
（`evidence/scan_v2_run4/contradictions.json`）を更新した。`contradictions_review.csv`
（72 行、学生の手作業用）は run3 のまま残し、増分 7 行は同じ木・同じ site なので
run4 の JSON から足す。

---

## D34. 母集団 v2 の tree budget 900 s 再走と決定論チェック: validator 関門は 1 木で動く、決定論は 85/87

### 結果（2026-09-21、解析器 235ae1e、Python 3.12.3）

**再走（`evidence/f0a_v2_run2_budget900`、`--tree-budget 900`）。** run1（180 s）で
飛ばした 716 ユニットは**すべて 1 木** `david-li0406/meta-skill-evloving`（.py 36,900
ファイル、1.9 GB のスキル集。716 ユニットを 608 秒で完走）のもので、他の 86 木は
run1 とユニット単位で同一（`scripts/lost_units.py`: 外れた 0 / 新たに危険 166、
木別の差は当該 1 木のみ）。

| 指標（mcp_server、87 木） | run1（180 s） | run2（900 s） | run2 から当該 1 木を除く |
|---|---|---|---|
| ユニット / 危険ユニット | 2,231 / 1,027 | 2,947 / 1,193 | 2,231 / 1,027 |
| validator 保有（主分母 dangerous_fp_excluded × all_paths） | 3.51% × | **8.38% ○** | 3.51% × |
| 同、木単位ブートストラップ 95% 区間 | [1.1%, 14.3%] 境界 | [1.5%, 26.7%] 境界 | — |
| validator 保有（all_units） | 3.77% × | 6.11% ○（区間 [2.2%, 10.3%] 境界） | — |
| validator 保有（dangerous_non_net） | 18.3% ○ | 30.3% ○ | — |
| in_tree_resolution_ratio（サイト） | 21.7% × | 27.4% × | — |
| opaque 率（主 slot、サイト） | 54.7% × | 50.9% × | — |
| §10 の分岐 | 1 | 1（r_D 46.5%） | — |

当該 1 木の危険ユニット 166 件のうち validator 保有は 64 件（38.6%）で、母集団の他の
木（3.5%）と桁が違う。この木は「36,000 のスキル」を生成した集合で、同じ雛形の
スクリプトが大量に並ぶ（同型のユニットが分母を占める）。

### 決めたこと

1. **主結果は事前登録の手続き（budget 180 s、run1）のまま**とし、900 s 再走は感度分析
   として併記する（`docs/population_v2_vs_v1.md` の表、preregistration §5 #8）。
   「関門を通る値」を見てから主結果を差し替えることはしない。
2. **validator 保有の合否は点推定で主張しない。** 両 run とも木単位の区間が閾値 5% を
   跨ぐ（D18 の規則）。本文には「1 木で合否が入れ替わる」ことをそのまま書く。
3. r_D は 53.3% → 46.5% に下がる（当該 1 木の 166 危険ユニットは明示宣言が少ない）が
   分岐 1 のまま。**r_D も 1 木の重みで動く**ので、木単位の区間を併記する。
4. tree budget の cap に当たったユニット数は run ごとに必ず報告する（run1 は 716、
   run2 は 0）。「budget で飛ばした = ランダムな欠損」ではないことがこの 1 木で
   確定した（欠損は木の大きさに相関し、木は同型ユニットの塊）。

**決定論（`evidence/determinism_v2`）。** 87 木のうち 85 木で 3 回バイト一致。
残り 2 木は不一致ではない: 当該の巨大木は 3 回分の index を 1 プロセスに持つと
OOM kill（rc=137、未測定）、`xorbitsai/xagent` は `units[0].notes` の
`TRUNCATED(wall_clock)`（`WALL_CLOCK_CAP = 10 s`）の有無だけが違い（1 回目は cache が
冷えていて cap 超え）、効果行・等級・判定は同じ。別プロセス 3 回では `elapsed_s`
以外バイト一致。**壁時計 cap の印は決定論の対象外**（cap 件数として報告する）。
決定論の主張は「壁時計の印を除いた manifest」に限ることを本文の限界節に書く。

---

## D33. val 受け入れ fixture F1–F10 の期待値の写し方（仕様の表 → manifest の語彙）

### 決めたこと

`fixtures/val/expected.json` は仕様 §2.6 の表を行単位に転記したもので、**採点器より
先にコミットした**（5944a0b、規則 5）。転記で語彙を写した箇所と、仕様の記載が
互いに食い違う箇所の読み方を決めた。**仕様書本体は書き換えない。**

1. **site 名は sink カタログの dotted 名**（仕様の `git.cmd.Git.checkout` は
   `git.Git.checkout`、pipe 形は `pipe:<method>`）。同じ sink を指す名前の違いで
   あり、期待の内容は変えていない。
2. **root 名は R2 導入点の名前**。低レベル MCP は `arguments["<key>"]`（CLAUDE.md
   「主語一致は root で取る」）。仕様の `roots={branch_name}` はその略記と読む。
3. **F2「`alias_facts` が空」は「正規化子の alias fact が無い」と読む。** F7 が
   `Path()`（正規化ではない）の alias fact を期待行に含めているので、字面どおり
   「配列が空」だと F2 と F7 が両立しない。両方を別項目（`alias_facts_empty_literal`
   / `alias_facts_canonical_absent_for_root`）にして採点し、前者は xfail で残す
   （O17 (a)）。
4. **F4 は実 commit で成立する。** 仕様は「未確定（合成 mutant）」と書くが、
   `docs/cve_triage.csv` A5 で脆弱側 1f1e8c9f / 修正側 5090f55e を `git log -S` で
   一次確認済み。仕様の記載は status に残した。
5. **F7 の `Path()` の site は実コードで採る。** 仕様は `validate_path` と書くが、
   3309bf4e では `Path(path)` は `execute` の中（`await self.validate_path(command,
   Path(path), operator)`）。期待は `in_function = execute`、仕様の値は `_reading` に残す。
6. **F5–F8 は入口を手で組む。** R2 カタログに OpenManus `BaseTool.execute` は無く
   （D17「直さない 3」）、`authgap scan` ではユニット 0 件。F5–F8 は val エンジンの
   受け入れ fixture なので、採点器が `Unit` を組んで `analyze_unit_f0a` に通す。
   入口認識の是非は採点しない。
7. **F9 / F10 は木が未取得なので skip**（xfail ではない: 未測定であって未達ではない）。
   期待行だけ pin した。

### 初回採点の結果（2026-09-21）

74 項目中 48 通過・26 未達。F1–F4 は全項目通過、F5 は EXEC 行と負のアサートが通過。
未達は F2 の字面の空（上記 3）、`depth_used` の未出力、F6/F7/F8 の 3 件（いずれも
行が出ない false-clean 方向。ユニットは opaque で clean ではない）。診断と候補の
規則は O17。**未達を直す変更は opaque → resolved なので、D17 改訂 2 と同じ敵対的
レビューを通してから入れる。** 採点器は未達を `KNOWN_UNMET` に xfail(strict) で
固定し、XPASS になったら印を外す。

---

## D32. O15 / O16 の学生の決定: `r_D` の分子は上界を動かす明示、追記型の FS_WRITE は矛盾に数えない

### 学生の決定（2026-09-20、チャット）

- **O15**: `r_D` の分子は「上界を動かす明示」（`readOnlyHint==true` /
  `destructiveHint==false`）。母集団 v2 では 53.3%。`openWorldHint==true` 単独の
  明示（80.0%）は「annotation を書く習慣の普及率」として併記する。
  実装（`scripts/f0a.py`）はこのままで、`dparse.parse_d_kind` の docstring を
  実装に合わせて直す。
- **O16**: sink カタログで**削除・上書き型**と**追記型**の FS_WRITE を分け、
  `destructiveHint==false` の宣言に対しては削除・上書き型だけを CONTRADICTION に
  数える（`readOnlyHint==true` に対しては従来どおり FS_WRITE 全部）。

### 規則（実装より先に書く。`docs/preregistration.md` §5 #7 に逸脱として記録）

- sink 表の FS_WRITE 行に属性 `destructive` を足す（**kind / slot の語彙は変えない**）:
  - 削除・上書き型（True）: `os.remove` / `os.unlink` / `os.rmdir` / `os.rename` /
    `os.replace` / `os.chmod` / `shutil.rmtree` / `shutil.copy*` / `shutil.move` /
    `shutil.unpack_archive` / `pathlib.Path.unlink` / `pathlib.Path.write_text` /
    `pathlib.Path.write_bytes`
  - 追記型（False）: `os.mkdir` / `os.makedirs` / `os.symlink` / `pathlib.Path.mkdir`
  - mode 依存（`open` / `io.open` / `pathlib.Path.open`）: mode に `w` または `+` を
    含めば True、`a` / `x` だけなら False、**mode が読めなければ True 扱い**
    （推定で clean にしない。false-dirty 側）。
- CONTRADICTION: `readOnlyHint==true` の明示 → EXEC / SPAWN / FS_WRITE のすべて。
  `destructiveHint==false` の明示（readOnly は明示していない）→ EXEC / SPAWN、
  および `destructive` が False **でない** FS_WRITE。
- **これは結果（D31 の 32 件）を見た後の定義変更**である。母集団 v2 の
  CONTRADICTION を数え直し、変更前（80 件）と変更後を併記する。
- 期待値は `fixtures/destructive_sinks` に実装より先に置く。

### 結果（同日、`evidence/scan_v2_run3/`。変更前 = `scan_v2_run1`、途中 = `scan_v2_run2`）

| | 変更前（run1） | sink 属性のみ（run2） | 効果ごと + sink 属性（run3、確定） |
|---|---|---|---|
| CONTRADICTION 行 | 202 | 195 | **142** |
| ユニット × (site, kind) | 80（16 木） | 78 | **72（16 木）** |
| うち readOnlyHint に反する | 48（8 木） | 48 | 48（不変） |
| うち destructiveHint==false のみに反する | 32 | 30 | **24**（rmtree 3 / unlink 3 / remove 1 / replace 2 / chmod 1 / open(w) 4 / Path.open 1 / write_text 2 / write_bytes 3 / subprocess.run 4） |

追記型（`mkdir` 6 / `makedirs` 1 / `open('a')` 1）の 8 件が矛盾から外れ、残りはすべて
削除・上書き型（`destructive=True`）か mode 不明（`open` 0 件）か SPAWN。
UNKNOWN / GAP_INJECT / GAP_SELECT は不変（2,549 / 197 / 232）。
手検証の候補表は `evidence/scan_v2_run3/contradictions.json`。

---

## D31. 母集団 v2 の full scan と `r_prev`: 宣言との差は CONTRADICTION に現れる（16/87 木）

- **いつ**: 2026-09-20。D30 の 87 木で full scan（`evidence/scan_v2_run1/`）と
  `r_prev`（`docs/prev_releases_v2.json` を先にコミット、`evidence/r_prev_v2_run1/`）。
- **full scan**（行 4,804）: UNKNOWN 2,549 / GAP_SELECT 232 / GAP_INJECT 197 /
  **CONTRADICTION 202** / INVENTORY 0。tree budget（180 s）で飛ばしたユニット 716
  （xagent 等の大きな木。分母に効くので本文に書く）。
  - **INVENTORY が 0、GAP_SELECT が 5 木だけ**なのは設計どおり: FastMCP デコレータ形
    （2,205/2,231 ユニット）は木内に MODEL セレクタの dispatch が無く `trig = assumed`
    なので、SELECT 座標は manifest 行にしかならない（`verdict.py:191`、仕様書 §3）。
    **宣言を持つ母集団では、宣言 D と実効 M の差は SELECT 座標ではなく
    CONTRADICTION（明示宣言に反する WRITE / EXEC / SPAWN）と、INJECT 行の
    `D_layer_present` に現れる。** これは主張の書き方を決める所見である。
  - CONTRADICTION はユニット × (site, kind) で 80 件・16 木
    （`evidence/scan_v2_run1/contradictions.json`、手検証の候補表）:
    readOnlyHint==true に反する書き込み / 実行 48 件（8 木、FS_WRITE 35 / SPAWN 13）、
    destructiveHint==false のみに反するもの 32 件（12 木。`shutil.rmtree` /
    `os.unlink` / `os.remove` のような削除も、`mkdir` / `open(w)` のような追記型も含む）。
- **定義の食い違い（O16）**: `dparse.d_kind_from` は destructiveHint==false の上界に
  FS_WRITE（追記型）を**含める**が、`dparse.contradiction` は FS_WRITE を無条件に
  矛盾とする。追記型の書き込みを矛盾に数えるかで 32 件が動く。実装側で寄せない。
- **`r_prev`（34 木 = 直前リリースを持つ 39.1%。旧枠 13.3%）**: 危険ユニットで
  **93.9%（169/180）**、粗 91.7%、5 リリース前 65.6%。無条件（87 木の危険ユニット
  1,027 を分母）で 16.5%。D_prev 層の適用可能性は旧枠の約 3 倍。
- **§10 の 3 連言（母集団 v2）**: `r_D` 53.3%（偽）、`r_prev` 93.9%（偽）、validator
  保有 3.5%（主分母で**真**）→ 不発火。ただし validator 保有の関門（≥ 5%）は
  6 分母すべてで × なので、§10 A5 の対処（クラス 2 は T1+T2 のみ）が**この母集団では
  発動する**。旧枠では主分母で通過していたので、母集団の変更で関門の合否が
  入れ替わった。**O7 の分母選択は v2 では合否を動かさない**（全分母 ×）。
- **旧枠との比較（本文の主表の候補）**:

| | 母集団 v2（宣言あり） | 旧枠 run6 |
|---|---|---|
| r_D（上界を動かす明示） | 53.3% | 0.0% |
| §10 分岐 | 1 | 3 |
| validator 保有（主分母） | 3.5% × | 12.1% ○ |
| 直前リリースを持つ木 | 39.1% | 13.3% |
| r_prev（適用木内） | 93.9% | 88.1% |
| CONTRADICTION を持つ木 | 16/87 | 0 |

- **次に決めること**: O15（r_D の分子）、O16（追記型 FS_WRITE を矛盾に数えるか）。
  **次の作業**: CONTRADICTION 80 件の手検証（`docs/verification_guide.md` の手順で
  本人が行う。これが最初の再現数値になる）、tree budget を上げた再走（716 ユニット）、
  full scan の決定論 3 回一致。

---

## D30. 母集団 v2（宣言を持つ Python MCP サーバ）の最初の run: r_D = 53.3%、分岐 1

- **いつ**: 2026-09-20。枠は `docs/population_v2.md` に列挙前に、抽出は `e29a8c8` に
  測定前にコミットした。解析器は O5 の join（`dec05fc`）を含む。
- **標本**: 母集団 3,827 repo（列挙 4,211、除外後）から seed 20260920 で 100 件、
  取得 100 / 失敗 0、取得後条件（宣言ファイルが `mcp` / `fastmcp` を import）で
  **87 木**（13 木は宣言はあるが MCP サーバでない）。仕様書の関門 ≥ 300 は母集団
  規模で通過。
- **結果**（`evidence/f0a_v2_run1/`、`docs/f0a_v2_run1.md`。旧枠 run6 を右に）:

| 指標（mcp_server） | v2_run1（宣言あり、87 木） | run6（旧枠、60 木） |
|---|---|---|
| ユニット / 危険ユニット | 2,231 / 1,027 | 1,669 / 431 |
| annotation 保有ユニット | 1,603（71.8%） | 1 |
| **`r_D`（上界を動かす明示、危険ユニット分母）** | **53.3%（547/1,027）** | 0.0% |
| 明示フィールドを 1 つでも持つ危険ユニット（`openWorldHint` 単独を含む） | 80.0%（822/1,027） | 0.0% |
| §10 の分岐 | **分岐 1**（thesis sentence を維持） | 分岐 3 |
| validator 保有（主分母 dangerous_fp_excluded × all_paths） | 3.51%（36/1,027）× | 12.06% ○ |
| validator 保有（all_units × all_paths） | 3.77% × | 4.43% × |
| `in_tree_resolution_ratio`（サイト） | 21.7% × | 19.3% × |
| opaque 率（主 slot、サイト） | 54.7% × | 45.3% × |
| ユニット 0 件の木 | 7/87 | — |
| 低レベルハンドラの join | 4 ユニット、55 ツール、明示 0 | — |

- **読み**:
  1. 宣言を持つ母集団では「宣言 D と実効 M の差」に主語がある（危険ユニットの
     半分以上が上界を明示）。§10 の規則どおり **分岐 1** に入り、旧枠の分岐 3 と
     母集団で分かれる。**この差は主張の主な所見**として両方を並べて書く。
  2. **validator 保有は旧枠より低い**（主分母で 3.5% 対 12.1%）。「宣言する成熟した
     サーバは検証子も丁寧」という選択効果の懸念は、この標本では**逆**だった
     （宣言はあるが値検証は少ない）。関門 ≥ 5% は 6 分母すべてで ×。
  3. opaque 率と in-tree 解決率は旧枠と同程度に悪い。解析器の解決限界は母集団で
     変わらない。
  4. 明示宣言の内訳: readOnlyHint 858、openWorldHint 778、destructiveHint 178
     （ユニット延べ）。低レベル形はこの標本では 6 ユニットと少なく、O5 の join は
     4 ユニット 55 ツールに効いたが明示宣言は 0（`title` 等のみ）。
- **見つけた定義の食い違い（O15）**: `scripts/f0a.py` の `n_d_kind` は
  `D_kind ≠ ⊥`（上界を動かす明示 = readOnlyHint==true / destructiveHint==false）で
  数えるが、`dparse.parse_d_kind` の docstring は「openWorldHint==true の明示」も
  分子に含めると書く。値は 53.3% と 80.0% で、どちらでも分岐 1。実装側で
  どちらかに寄せない（仕様書 §10 :1121 の文言と照らして学生が決める）。
- **次**: 同じ 87 木で full scan（verdict・covered_by の層別内訳）、`r_prev`
  （§2.7 の手順を v2 に当てる）、旧枠との比較表を本文用に固定する。

---

## D29. 母集団を「宣言を持つ Python MCP サーバ」に変える（学生の決定）

### 学生の決定（2026-09-20、チャット）

1. **母集団は宣言（MCP ToolAnnotations）のあるものだけにする。**
2. 宣言を持つプロジェクトの比率は論文に明記すべきだが、**今回は気にしなくてよい**
   （比率の推定は主目的ではない。§2.8 (e) の値を「参考値」として書く）。

### 経緯（post-hoc であることを先に書く）

D28 / §2.8 の全数調査で、旧枠（`docs/population.md`、import 文の code search）の
標本 97 木には宣言が事実上無く（明示リテラル 2/676）、一方で星数上位の Python
MCP サーバでは 9/29 = 31% が宣言を持つことが分かった。**母集団の変更は r_D = 0.0%
を見た後の決定**であり、`docs/preregistration.md` §0 の告知に加える。旧枠の結果
（run1〜6、r_prev、判別実験）は捨てず、「long tail には宣言が無い」という対照として
報告する。

### 決定の帰結

- **新しい枠を、列挙する前に `docs/population_v2.md` に事前登録する**（列挙の
  手段・除外規則・pin・抽出の seed）。列挙後に規則を変えない。
- 元の §0 の主張（宣言 D と実効 M の差）は、この母集団では主語を持つ。§10 の
  分岐は新母集団で改めて測った r_D で決める（宣言を条件に選ぶので r_D は定義上
  高いが、D_kind の「明示」条件（`readOnlyHint==true` 等）を満たすかは別なので
  100% にはならない）。
- **O5（低レベルハンドラと宣言の join）が必須になる。** 成熟したサーバは低レベル形
  `Tool(name=..., annotations=...)` + `call_tool` の分岐で書かれることが多い。
  規則を先に事前登録し、期待値を先に置いて実装する。
- 選択効果を本文に書く: 「宣言を持つ」で選ぶと検証子も丁寧な repo に偏りうる。
  結果は「宣言する Python MCP サーバについて」の主張であり、生態系全体には
  一般化しない。
- O14 はこの決定で閉じる（(b) を採用）。

---

## D28. 宣言 D の全数調査: r_D = 0 は「パーサの見落とし」ではなく「カタログの範囲と枠の性質」

- **いつ**: 2026-09-20。学生の指摘（「まず D の宣言があるものの総数を調査すべきでは」）
  を受け、数え方を §2.8 に**先に**書いてから数えた。
- **結果**（`docs/preregistration.md` §2.8 (d)、`evidence/decl_census_run6/`）:
  - 97 木の自前コード（src）で MCP annotation の語が出る木は 5。事前登録の規則は
    `parser_recall_defect` を返したが、目視分類では「認識する形を読み損ねた」例は無く、
    (i) OpenHands の `ToolDefinition(annotations=ToolAnnotations(...))` = R2 カタログ外の
    枠組みの本物の宣言、(ii) mastermind の低レベルサーバ = O5（名前 join 不能）、
    (iii) 間接形 / 変換器 / 消費者。
  - `Tool(...)` リテラル 676 中、明示 hint を持つのは 2（1 は同梱 SDK のテスト）。
    O5 の join 規則を入れても明示宣言ユニットは 1/2533（探索的）。
  - GitHub 全体（参考値）: Python の呼び出し形宣言はファイル単位で枠の約 5%、
    TypeScript の hint 語は Python の 2〜3 倍。
- **決定**:
  1. run6 の r_D = 0.0% は据え置く（D20 と同じ。再測定は規則を変えた run として足す）。
  2. **「宣言が無い」の書き方を限定する**: 「GitHub code search 由来の公開 Python
     MCP サーバの、R2 カタログが認識する入口には、明示の MCP annotation が事実上無い
     （明示リテラル 2/676、自前コードでは 1 件）」。「野外に宣言が無い」とは書かない。
  3. OpenHands 型（app 枠組みの `ToolDefinition`）を R2 に足すか、宣言を持つ
     部分母集団を第 2 の枠として事前登録するかは **O14（学生）**。どちらも Def 2 /
     母集団定義の変更なので実装側で決めない。
  4. O5（低レベルハンドラの join）は、直しても r_D を動かさないことが分かったので
     優先度を下げる（記録は残す）。
  5. **追記（同日、§2.8 (e)）**: 星数上位の Python MCP サーバ（`topic:mcp-server`、
     SDK を除く 29 repo）では **9/29 = 31%** が `ToolAnnotations` を使う。
     宣言は存在し、成熟したサーバでは珍しくない。r_D = 0.0% は「宣言が無い」
     ではなく **標本の枠（import 文の code search）が小規模 / チュートリアルの
     repo に偏っている**ことの帰結である。母集団の定義（`docs/population.md`）
     の再検討が O14 に加わる。
- **誤りの向き**: 調査前の r_D = 0.0% は「宣言との差が測れない」方向の値で、
  パーサの見落としがあれば主張を**不当に弱く**していたことになる。調査の結果、
  見落としは R2 の範囲外にしか無く、r_D の値は枠の性質として立つ。ただし
  D27 の「仕様書の規則が指す枠」の議論は「この枠では」という限定を付けて読む。

---

## D27. `r_prev` を測った（run2）。§10 の「方向を疑う 3 連言」は事前登録の分母では不発火

- **いつ**: 2026-09-20。手順は §2.7 に測定前に事前登録し（`173a626`）、タグの選択は
  測定前にコミットした（`72bc952`、訂正 `5725099`。訂正は実装の欠陥で規則は不変、
  §5 #6）。run1（as-run、crewAI の選択が誤り）と run2（訂正後）の両方を残す。
- **値（run2、`evidence/r_prev_run2/r_prev.json`）**。分母は §2.7 (f)（手順 1 で
  `ok` の 16 木の危険ユニット。粗 = 全ユニット）:

| | 木 | `r_prev`（危険） | 粗（全ユニット） | distinct-id（危険 / 粗） |
|---|---|---|---|---|
| app | 7 | 83.3%（40/48） | 82.8%（356/430） | — |
| mcp_server | 8 | 87.7%（71/81） | 94.4%（368/390） | — |
| tool_package | 1 | 100%（22/22） | 100%（186/186） | — |
| **全体（直前）** | 16 | **88.1%（133/151）** | 90.5%（910/1006） | 87.5%（126/144）/ 89.5%（819/915） |
| 全体（5 リリース前、感度） | 16 | 85.4%（129/151） | 89.5%（900/1006） | 84.7%（122/144）/ 88.4%（809/915） |

  run1（as-run）は全体 64.2%、app 8.3%（crewAI の「直前」が 2024 年のタグだった
  ため）。**訂正で app が 8.3% → 83.3% に動いた**。訂正は規則の適用誤りの修正で、
  規則を値を見て変えたのではない（§5 #6 に両方の値を記録）。
- **併記（§3 の規則。事前登録した分母ではない値）**:
  - 無条件（run6 の 98 木すべてを分母にし、前リリースの無い木を join 不可と数える）:
    危険 133/577 = **23.1%**、全ユニット 910/2621 = 34.7%。§2.7 (f) は 0〜1 本の木を
    分母に入れないと定めているのでこれは主値ではないが、**D_prev 層が適用できる木が
    16/98 しかない**（D23）ことを示す値として本文に併記する。
  - 接頭辞つきタグを「直前」に選んだ木 3/16（autogen `python-v0.7.5`、mammothsdk
    `cli-v1.0.8`、ava `android-v0.4.2`）。§2.7 (i) の monorepo の限界に当たる可能性が
    あるが、同じ履歴の別サブパッケージのタグかは確認していない（不明）。
- **unit id が木の中で一意でない**（O13）: 4/16 木で重複（crewAI 321 ユニット / 312 id、
  fewsats 8 / 4、nuguard 186 / 109、ava 20 / 19）。Def 6 の「unit id の完全一致」は
  一意性を前提にしているが、同じ qualname + 同じ本体ハッシュのツールが複数回
  登録される（tests / examples の複製、同名ツールの再定義）。join の値は重複を
  含めても distinct にしても 0.2 ポイント差で結論は変わらないが、`GAP_DRIFT` の
  join 先（`DPrev.load` は同じ id の最後の行を採る）は定義されていない。

### §10 の「方向そのものを疑うべき条件」（仕様書 :1143）の判定

> 両母集団で `r_D < 5%` **かつ** `r_prev < 50%` **かつ** validator 保有 < 5%

| 成分 | 事前登録の分母での値 | 判定 | 別の分母（併記） |
|---|---|---|---|
| `r_D < 5%` | run6: 0.0%（3 母集団とも。`r_kind` / `r_op` / `r_dom` すべて 0） | **真** | 分母によらず 0 |
| `r_prev < 50%` | run2: 全体 88.1%、app 83.3%、mcp_server 87.7%、tool_package 100% | **偽** | 無条件 23.1% なら真 |
| validator 保有 < 5% | 主分母（dangerous_fp_excluded × all_paths、§2.2）: 12.06% / 11.34% / 22.45% | **偽** | all_units × all_paths: 4.43% / 3.26% / 6.50%（mcp_server と tool_package で真） |

**事前登録した分母では 3 連言は不発火**（`r_prev` と validator 保有の 2 成分が偽）。
**併記の分母を 2 つとも採った場合に限り**、mcp_server と tool_package で発火する
（app は validator 保有 6.50% で不発火）。分母の選択は O7（学生の承認待ち）であり、
**選択が判定を反転させる方向にある**ので、実装側で確定しない（D20 と同じ扱い）。

### 仕様書自身の規則が指す枠（D24 の「仕様書の規則で枠を選ぶ」の結果）

- `r_D = 0.0%` → §10 の**分岐 3**（3 母集団とも）: 「宣言との差」を主張から外し、
  P0 と D_prev（`GAP_DRIFT`）に主張順序を移す。
- D_prev は `r_prev ≥ 50%` を満たすので分岐 3 の fallback として**使える**が、
  **使える木は 16/98**（mcp_server 8/60 = 13.3%、tool_package 1/30、app 7/8）。
  仕様書の前測 90.0%（未追試の値）との食い違いは D23 のとおり。
- したがって仕様書の規則どおりに読むと: 主張は「M の推論 + P0 との差」を主、
  「D_prev との差」を 16 木の副とし、「D（annotation / D_op）との差」は主張から外す。
  D24 の 3 段（A 段 = val / sink / 入口 / 決定論 / 測定規律、B 段 = ゲート等級、
  C 段 = D パーサ）で言えば、**C 段は道具に降り、B 段は O12 の判断待ち**。
- **これは仕様書の規則の適用結果であって、枠の最終決定ではない。** 決定は学生が
  行う（O7 の分母、O12 の等級づけ、O13 の unit id）。

### 結果（手続き）

- run2 の木ごとの join 数は runner の `d_prev_joined` と一致（assert）。
- `UnitReport.d_prev_joined` が probe 経路で立たない欠陥（D22 の残り）を直し、
  `tests/test_d_prev.py` に回帰を足した。

---

## D26. 判別実験 (a)(b)(c) の結果を記録し、事前登録した判定規則を当てた（規則は決定不能）

- **いつ**: 2026-09-20。3 実験の判定規則は `docs/preregistration.md` §5 #2 に
  **結果を見る前に**書いた（#4 の公平な比較も結果を見る前に規則を書いた）。
  結果は同 §5.1。
- **結果の要点**: (a) 事前登録照合 7/8（A18 の転記誤りを直せば 8/8、§5 #5）、
  逆向き・無関係な変化は不通過。(b) **C − C0 = {A10}**（事前登録照合・座標一致）、
  any-change では ∅。(c) CodeQL は既定 source で 3 対とも被覆せず、入口を揃えても
  A1 / A4 は sink 未被覆、**A10 は両側とも報告**（第 3 類型）。
- **規則の適用**: 前提（A10 ∈ C − C0）は成立、枝 1（CodeQL が脆弱側を clear）も
  枝 2（C − C0 = ∅ または両側判別）も不成立。**第 3 類型を規則が想定しておらず
  決定不能。** post-hoc の読み (α)(β) を §5.1 に併記し、決定は O12 に置く。
  **実装側で (α) を採らない**（採ると「結果を見てから規則を解釈した」ことになる）。
- **手続き上の所見**: (b) の結果は (a) の分子の直し方に依存する。any-change の
  ままなら C − C0 = ∅ で規則の枝 2 が成立し、等級づけは降りていた。分子の照合は
  #2 (a) で C0 を回す前に事前登録し、期待表（`d2b501a`）も C0 の実装（`654bca2`）
  より先に置いたので、順序は守られている。ただし **D25 で inline 採点を撤回した
  ことで fixture 水準の C − C0 は {b1, b2} → {a1, a2, a3, b1, b2, b3} に動いた**
  （§5 #3）。較正対水準の C − C0 = {A10} は撤回の前後で変わらない（撤回前の探針を
  §5 #3 に記録）。
- **公平な比較の限界**: 入口を揃えても CodeQL の sink 集合（`open` / `os.*` /
  `Path.resolve` など）は AuthGap の sink カタログ（`git.Git.*` の `cwd` / argv、
  `subprocess` の argv）と違う。A1 / A4 で CodeQL が報告した数件は修正で足した
  `.resolve()` 自身が sink として出たもので、**修正を足すと報告が増える**。
  sink も揃えた比較は行っていない（sink を揃えると CodeQL の path-injection では
  なく AuthGap の再実装になる）。
- **仕様書は書き換えていない。** §1.5.4 に第 4 類型が無いことは #2 に、第 3 類型を
  規則が扱っていないことは §5.1 に記録した。

---

## D25. D21 の inline 採点を撤回し、裏づけを全 root に、strong-path をパス領域に限る

- **いつ決めたか（正直に書く）: D21 の敵対的レビューの結果（29 件の false-clean）を
  見た後。** 修正の動機は post-hoc だが、期待値（`tests/test_d21_adversarial.py`、
  `fe620c6`）は修正より先にコミットした（規則 5）。
- **事実**: D21「結果」節のとおり。false-clean 29 件、うち 25 件が D21 由来。
  凍結済みの受け入れ関門は 1 件も捕まえていない。

### 決定

1. **変更 A（`gate.py: _grade_inline`）を撤回する。** inline 形（ツール本体に直接
   書かれた述語）は `_grade_from_shape` の単一形状採点に戻し、weak 止まりにする。
   Def 5 を inline で満たす形（`tests/test_value_grade.py` A 群 a1〜a3）は再び
   strong-path にならない。**この誤りの向きは false-dirty（安全側）**であり、
   `xfail(strict=True)` に戻して O8 に統合した。
2. **`analyze.py: _strong_path_backed` を「制御値の MODEL root すべて」に
   canonical alias を要求する形にする**（M2）。D21 の「どれか 1 つ」は、
   `join(real, name)` のように検証済み引数と未検証引数が合流した値で検証済み側の
   裏づけを未検証側に移していた（R10 / R12 / R17 / R19、§3-3 / §3-4）。
3. **`sinks.py: PATH_DOMAIN_SLOTS`（`path` / `cwd` / `argv0` / `argv[i]` /
   `argv[*]`）を定義し、それ以外の位置の strong-path は `req_val` を動かさない**
   （M3）。落とす先は `unknown`。weak 理由語彙（22 語、月 6 凍結）に「領域不一致」
   の語は無く、凍結後に語彙を足さない（`docs/preregistration.md` §5 に逸脱として
   足さずに済む選択）。`strong-token` が効果側（argv 実行か）を確かめるのと同じ
   非対称を埋めた。`argv[*]` を含めるのは較正対 A4（`git_add` の `argv[*]` が
   strong-path）のためで、要素がパスでありうる位置は残す。
4. **直せない形は未解決として記録する**: 条件 (ii)・root-equal・inline の strong
   （O8、拡張）、条件 (iii)（O10、新設）、helper 本体の袋詰め採点と値の同一性を
   見ない裏づけ（O11、新設）。同テストの x01 / x03 が xfail で凍結している。

### なぜ (B) 完全実装ではなく撤回か

レビューの「出す条件」は二択だった: (A) 撤回、(B) 決定文どおりの完全実装
（root-equal・条件 (ii)・領域一致・全 root）。(B) は候補述語 1 つに対して
「その述語が sink を支配し、canonical alias そのものに当たり、他方の被演算子が
定数で、sink に届く値が root-equal」を val の値の同一性で確かめる設計を要する。
現在の `alias_facts` は root 粒度で値の同一性を持たず（R15）、`_value_grade` は
集合しか受け取らず適用順序を表現できず（R18）、レビューの実測では root-equal を
`canonicalised` 属性で取ると較正対 A4（手続き間の形）の INJECT clearing が
1/7 → 0/7 に退行する。**設計をやり直す間、false-clean を出荷し続けない**ために
安全側へ戻す。(B) は改めて期待値を先に置き、敵対的レビューを通してから入れる。

### 誤りの向きの収支

| | D21 前 | D21 | D25 |
|---|---|---|---|
| inline で Def 5 を満たす形（a1〜a3） | false-dirty | 正 | **false-dirty** |
| inline の退行 25 形 | 正（GAP） | **false-clean** | 正（GAP） |
| helper の root 和 / 領域漏れ（x02 / x04 / x05 / x06） | **false-clean** | **false-clean** | 正（GAP） |
| helper のデコイ（x01）/ 条件 (iii)（x03） | **false-clean** | **false-clean** | **false-clean**（O8 / O10 / O11 に記録） |

### 結果

- `tests/test_d21_adversarial.py`: 30 形が XPASS（印を外した）、x01 / x03 は xfail のまま、
  対照 3 形（helper 基準形の `path` / `argv[*]` / `cwd`）は strong-path のまま。
- `tests/test_value_grade.py`: A 群 6 件が xfail（false-dirty に戻る）、B / C 群は不変。
  C0 の fixture 期待は {b1, b2} → {a1, a2, a3, b1, b2, b3}（`docs/preregistration.md`
  §5 #3）。
- 受け入れ関門: `check_gates.py` 23/23 OK（B3a 8/8・B3b 15/15）、変異 生存 1/15、
  `pytest tests/` 全通過。
- 較正対（`scripts/two_sided.py`、腕 C）: any-change 8/8（CVE 単位。木の対は 7、A9 と A10 が corpus を共有）、厳密（全 GAP 解消）0/8、INJECT 座標 1/8（A4）。**D25 前（`654bca2`）と同一。** 較正対の修正側の strong-path はすべて helper 形（A1 `cwd`、A4 `argv[*]`、A10 `path`）なので inline 採点の撤回は効かず、パス領域の位置なので領域検査も効かない（対照 c01〜c03 と同じ）。事前登録照合の 3 列は判別実験 (a) の実装（次のコミット）で出す
- 腕 C0（判別実験 (b)）: any-change は C と同じ 8/8。**A10 の `path` 3 位置は C0 で `req_val` が OP → OP（脆弱側も OP）になり、変化は `grade weak → strong-path` だけになる**（事前登録した期待は `req_val MODEL → OP` を含むので、事前登録照合では C0 で落ちる = A10 ∈ C − C0）。A1 / A4 は脆弱側に検証子が無いので C0 で何も変わらず C − C0 に入らない。A18 は C0 で `req_val MODEL → OP`（weak な文型 allowlist を C0 が OP に潰す）になるが `GAP_INJECT` は残る。撤回前の探針（§5 #3 の記録）と同じ結論
- `scripts/diff_effects.py --before fe620c6`（14 木）: 14 木すべて 行数不変、消えた 0 / 増えた 0 / slot 変化 0（A1〜A4 各 9 行、A5 22 行、A9 121 行、A18 18 行）。等級の変更は効果行を動かさない（動かしてはいけない）

---

## D24. 枠組みは今は変えない。判別実験と `r_prev` の後に仕様書自身の規則で選ぶ

### 学生の決定（2026-09-20、チャット）

1. **指導教員の承認は不要。** 仕様書 §8-1(b) の「設問の変更の書面受理」、
   `docs/open_questions.md` O3 の承認経路、O4 の push 可否は**承認の側面が消える**。
   影響を受けるリポジトリへの**開示**（O3 の本体）は承認とは別の問題なので残す。
2. **研究アイデア自体の変更を厭わない。ただし核は残したい。**

### 経緯（**post-hoc であることを先に書く**）

run6・D23（D_prev 適用 16/98）・`evidence/w0/two_sided.json` を見た後に、
枠組み変更 4 案（α 権限合成器 / β 検証子の等級づけ / γ 測定研究 / δ 運用者の宣言）
と現状維持の反対案を立て、3 審査員（査読者 / 指導教員役 / 懐疑的同業者）に
採点させた。**この検討は事前登録した判定手続き（§10 の 3 連言）を踏む前に
結果を見て行ったもので、post-hoc である。** `docs/preregistration.md` §0 に告知した。

### 審査の結論

| 案 | 合計 / 60 | 防御性（3 名） |
|---|---|---|
| γ 測定研究 | 40 | 10 |
| β′ 検証子の等級づけ | 36 | 9 |
| 反対案（現状維持） | 33 | 6 |
| α 権限合成器 | 30 | 6 |
| δ 運用者の宣言 | 29 | 6 |

**査読に耐える骨格は γ か β′ にしか無い**（防御性で 3 名一致）。
α（val を核に）は査読者が最低点: 「落とすのは最も試験の厚い部品（gate）で、
残すのは最も試験の薄い部品（val）」。懐疑者が実測で裏づけた —
**`fixtures/val` が存在せず**（核の部品で `CLAUDE.md` 規則 5 が破られている）、
A1 脆弱側の `git.Git.log` / `git.Git.branch` の `argv[*]` は原ソースで
`arguments.get(...)` 由来（MODEL）なのに manifest では `prin=OP / opaque / roots=None`。
UNKNOWN 行にはなるので false-clean ではないが**主体ラベルが誤っている**。

**反対案が正しかった点（3 名が認めた）**: 「方向を疑う条件」の 3 連言は未発火
（`r_prev` は未測定、validator 保有は主分母で通過、D20 が遡及を禁じている）。
**今枠を変えると、事前登録した判定手続きを踏む前に結果を見て動いたことになる。**

### 決定

**今は枠を選ばない。** 順番:

1. **手続きの逸脱を記録・修正する**（本コミット）。採点集合の逸脱
   （`preregistration.md` §5 #1）、`cve_triage.csv` の列ずれ（A1 / A14。
   **A1 の `verified_by_me` は本当は `sha+diff+two_sided` なのに `unchecked` に
   読めていた** — 検証済みの対が未検証に見える方向の誤り）、標本 pin（O9）。
2. **既存 14 較正木での判別実験 3 つ**（`preregistration.md` §5 #2 に判定規則を
   先に書いた）。野外 run は不要。
3. **`r_prev` を 16 木で測る**（§2.7 の手順 2〜5）。
4. §10 の 3 連言を完成させ、**仕様書自身の規則で**枠を選ぶ。
   成立し区間が閾値を跨がない → 測定研究（γ 主・β′ 従）。不成立または境界 →
   枠は変えず β′ 主・γ 従。**run7 を見てから枠を選ぶと post-hoc が 2 回重なる。**

### 「核として残す部品」の 3 段（審査員 3 名の `best_combination` が収束した形）

- **A 段（どの結果でも残る）**: val の位置ごとの主体・root・alias_facts と確度束、
  sink カタログ + slot 語彙 + effects、R1/R2 入口カタログと unit id（relpath + 行を
  キーに含めることを条件に）、決定性の基盤、測定の規律一式。
- **B 段（判別実験で主張の強さを決める）**: gate の等級づけ（weak 22 理由 + witness、
  支配判定）、`two_sided.py` + `cve_triage.csv`（較正表として）、`ARMS` の腕機構
  （C0 を足して T ⊂ S ⊂ C0 ⊂ C の梯子に）。
- **C 段（測定値として残す）**: D_kind / D_op / D_prev のパーサ（宣言の存在率の計測器）、
  `trig.mode` を manifest 属性に。
- **降ろす（5 案・3 審査員が一致）**: GAP_SELECT の野外主張、交差行「統一」主張、
  GAP_DRIFT の主張、`--hosted`、先行手法の自己申告値との数値比較、
  「同一コーパスで精度差」の一文（CodeQL との対ごと表に置換）。

### 全案が見落としていたもののうち、記録しておくべきもの

- **効果の確度と slot の確度の混同。** 「危険ユニット 577」という分母自体が
  名前一致の効果（`opaque(unresolved)` を合流したもの）を含む。全効果行 resolved は
  144/577、1 行も resolved でないものは 349/577（審査パネルの再計算。本人未追試）。
- **NET が `DANGEROUS_KINDS` と verdict の両方で無条件。** 300/577 が NET のみで、
  577 を分母にする全指標が NET の扱いで動く。仕様書の P0 は private-range 限定。
  **verdict の問題ではなく分母の定義として先に固定し、込み / 除きの 2 分母を
  `preregistration.md` に足す**（未実施）。
- **`opaque(unresolved)` が 2 つの意味を混ぜている**（木外の呼び先 / 木内だが
  受け手型不明）。`resolution_by_cause` に分離が無い。
- **人間がまだ 1 つの数字も再現していない**（`verification_log.csv` 無し、
  **59/59** コミットが Claude 共著。本人が `git log` で確認）。

### 仕様書は書き換えていない

§6 T1.6 の採点集合、§8-1(b) の書面、§10 の分岐はそのまま残す。
逸脱と決定は本項と `preregistration.md` §0 / §5 に置いた（`CLAUDE.md` 規則 6）。

---

## D23. リリースタグを持つ野外の木は 16/98（仕様書の前測 90.0% と食い違う）

**事前登録（`docs/preregistration.md` §2.7、コミット `173a626`）を先に固定し、
その規則をそのまま適用した結果である。** 値を見てから規則を決めていない。
出力は `docs/prev_releases.json`（測定より先にコミット）。

### 実測（`scripts/prev_releases.py --run evidence/f0a_run6`）

| status | 件数 | 分母に入れるか（§2.7 (f)） |
|---|---|---|
| `ok`（直前リリースを決められた） | **16** | 入れる |
| `single_release`（リリースタグ 1 本） | 6 | 入れない |
| `no_release_tag`（リリースタグ 0 本） | **75** | 入れない |
| `fetch_failed` | 1 | 入れない |

母集団別の `ok`: **mcp_server 8/60 = 13.3%**、tool_package 1/30 = 3.3%、app 7/8 = 87.5%。

### 仕様書との食い違い（**実データを採り、仕様書の値も残す**。`CLAUDE.md` 規則 6）

仕様書 Def 6 の D_prev 節は適用条件について
「**静的に取得できるリリースが 2 本以上あること（前測で 60 サーバ中 54 件 = 90.0%）**」
と書いている。本 repo の実測は **8/60 = 13.3%** で、**6.8 倍の開き**がある。

**仕様書の値は書き換えない**（§7.5 の設計の記録として残す）。本文では実測値を
採り、前測の 90.0% と併記して差の理由を書く。

### 規則が原因ではないことの確認（**これが本項の要点**）

| 切り分け | 件数 |
|---|---|
| タグが**1 本も無い**木 | **76** |
| タグはあるが §2.7 (c) の規則で release 0 本になった木 | **0** |

**(c) の規則は 1 本もタグを落としていない。** 事前登録の時点で
「プレリリース語 `pre` の部分一致が `prefetch-1.0` のような名前を誤除外しうる」
というリスクを記録していたが、**実データでは発現しなかった**。
したがって規則を緩めても `ok` は増えない。低いのは規則のせいではなく
**母集団の性質である**。

### 差の理由（**仮説。未検証**）

`docs/population.md` が記録しているとおり、本 repo の標本フレームは
**GitHub code search**（`"from mcp.server" language:Python` 等）であって
**PyPI 逆依存ではない**。同文書は「したがって母集団の定義は『PyPI 上の
`mcp` / `fastmcp` 依存者』ではなく**『公開 Python MCP サーバ』**である。
この差を本文に明記すること」と書いている。

PyPI 由来の母集団は**定義上リリースを持つ**。GitHub code search 由来の母集団は
「import 文が一致する公開リポジトリ」なので、タグを打たない個人リポジトリが
大量に入る。**前測の 90.0% が PyPI 由来の母集団で得た値なら、この差は母集団
定義の差で説明できる。** ただし前測のフレームがどちらだったかは本 repo からは
確認できない（前測スクリプトは `scripts/premeasure/` にあるが、フレームの
取得手段の記録が無い）。**未検証の仮説として記録する。**

### 研究への影響（**測定前に書く**）

`r_prev` の値はまだ測っていない。**ただし値がいくつであれ、以下は確定である:**

1. **D_prev が宣言層として使えるのは最大でも 16/98 = 16.3% の木**である。
   `r_prev` が 100% でもこの上限は動かない。
2. **`tool_package` は `ok` が 1 木しかない。** 母集団として `r_prev` を語れない。
3. 仕様書 §10 の分岐 3（`r_D < 5%` → P0 と D_prev に主張順序を移す）は
   run6 で 3 母集団すべてに適用される。**その fallback の片方（D_prev）が
   野外の 84% で使えない**ことになる。

**1〜3 は `r_prev` の閾値判定とは別の事実である。** §10 の `r_prev ≥ 50%` は
「適用できる木の中での join 率」であって「適用できる木の割合」ではない。
両方を報告する（§2.7 (f) の記録先がそれである）。

### 既知の限界の発現（§2.7 (i)）

monorepo で別サブパッケージのタグが選ばれる形が **2 件**出た:
`w-edgemetric__mammothsdk` の `cli-v1.0.8`、`w-zhiyuan-zhang0206__ava` の
`android-v0.4.2`。事前登録どおり**タグ名でサブパッケージを判定する規則は
入れない**（リポジトリごとの命名規約に依存し、標本を見て調整することになる）。
件数をここに記録する。

一方、接頭辞つきタグを含める判断（§2.7 (c)）は野外でも効いた:
`w-microsoft__autogen` の直前リリースは `python-v0.7.5` で、素朴な
`^v?\d+\.\d+` なら落ちていた。

### `fetch_failed` の 1 件

`archsec-emman/financial-orchestrator` が clone できない。これは
**標本抽出から 6 日で GitHub から消えた 2 件のうちの 1 件**であり、
野外標本の pin が全件 `HEAD` である問題（`docs/open_questions.md` O9 で扱う）
の実害が測定に現れた最初の例である。

---

## D22. D_prev 層の配線を通す（`r_prev` は測れない状態だった）

**本項は「直すと決めた」記録である。期待値は `tests/test_d_prev.py` に
修正より先にコミットした**（`CLAUDE.md` 規則 5）。結果は末尾の「結果」に追記する。

### 事実

仕様書 §10 の「**方向そのものを疑うべき条件**」は 3 つの連言である:

> 両母集団で `r_D < 5%` **かつ** `r_prev < 50%` **かつ** validator 保有 < 5%

`r_D` と validator 保有は run1〜6 で測られているが、**`r_prev` はどの run にも
出ていない**。理由は配線が 3 か所切れているからで、値が悪かったのではなく
**原理的に測れない状態だった**。

| # | 場所 | 状態 |
|---|---|---|
| 1 | `dparse.py: DPrev.load` | `units[i]["unit_id"]` を引くが、manifest の unit id は `units[i]["unit"]["unit_id"]` にある。自分の `scan` 出力を `--prev-manifest` に渡すと `KeyError: 'unit_id'` で落ちる |
| 2 | `report.py: probe_json` | `n_units_with_D_prev_join` が `0` の決め打ち |
| 3 | `scripts/f0a.py` | `r_prev` が存在しない（`grep -c r_prev` が 0） |

**1 は「自分の出力を自分で読めない」という形なので、この層は一度も通って
いない。** `grep -rn prev_manifest scripts/ tests/` の該当も 0 件だった。

### なぜ重いか

§10 は `r_prev ≥ 50%` のときのみ D_prev を主張に使うと定めており、分岐 3
（`r_D < 5%`）に落ちた母集団の fallback がここに乗っている。run6 は 3 母集団
すべてが分岐 3 なので、**fallback が成立するかどうかが未判定のままである**。

仕様書の前測では「静的に取得できるリリースが 2 本以上ある」のが 60 サーバ中
54 件 = 90.0%（**仕様書の値。本 repo では未追試**）なので、分母は十分あると
見込まれる。測っていないのは取得の問題ではなく実装の問題である。

### 決定

1. `DPrev.load` の join キーを manifest の実構造に合わせる。
2. `n_units_with_D_prev_join` を実際の join 数にする。
3. `r_prev` を `scripts/f0a.py` の `PopStats` に足し、§10 の他の率と**同じ分母**
   （`docs/preregistration.md` §2.2 の `dangerous_fp_excluded`）で出す。
   併記規則（§3）も同じく適用する。
4. そのうえで 2 リリースを取得して野外で測る。**取得手順と分母は
   `docs/preregistration.md` に先に書く**（後から分母を選べないようにする）。

**1〜3 は実装の修正であり、値を動かす意図は無い。** 現在の `r_prev` は
「未測定」であって「0」ではない。修正後に初めて値が出るので、
**その値を見てから分母や閾値を動かさない。**

### 結果（2026-09-20）

配線 3 か所を直した。**値を動かす修正ではない**（`r_prev` は未測定 → 測定可能に
変わっただけで、他の指標には触れていない）。

| # | 直した所 | 内容 |
|---|---|---|
| 1 | `dparse.py: DPrev.load` | join キーを `units[i]["unit"]["unit_id"]` に。id を取れない行は黙って捨てず `skipped` に数える（分母が静かに縮むのを防ぐ） |
| 2 | `analyze.py` / `report.py` | `UnitReport.d_prev_joined` を足し、`n_units_with_D_prev_join` を実数に。危険ユニット限定の値も併記 |
| 3 | `scripts/f0a.py` | `r_prev` / `r_prev_crude` を `PopStats` に追加 |

**`None`（未測定）と `0.0` を区別する設計にした。** 前リリースを 1 本も供給して
いない run では `r_prev` は `None` を返す。`0.0` を返すと「測っていない」が
「join 率 0%」に化け、§10 の「方向そのものを疑うべき条件」の 3 つ目が
**誤って成立する**。同じ理由で、前リリースを取得できなかった木は `r_prev` の
分母に入れない（取得の失敗が join の失敗に化けるため）。取得できた木の数は
`n_trees_with_prev` に別に出し、Def 6 の適用条件として報告する。

分母は `docs/preregistration.md` §2.2 の主分母（危険効果を持つユニット）に揃え、
粗い分母の値も併記する（同 §3）。**§10 の他の率と同じ分母である。**

**規則 5 の手続きについて正直に書く。** 項目 1〜2 の期待値は先行コミット
`910459a` に入れた。**項目 3（`r_prev`）はテストとコードが同一コミットである。**
1〜2 と違い既存の壊れた機能ではなく新規の測定なので、先に凍結すべき期待値が
存在しなかった。期待は §10 の定義と preregistration.md §2.2 から書いている。

検証: pytest 全通過、ruff 通過、B3a 8/8・B3b 15/15、変異生存 1/15、
`--determinism 3` が 3 回バイト一致、`diff_effects` で較正 4 木の効果行が
消えた 0 / 増えた 0 / slot 変化 0、manifest schema 検証も通過。

**野外の測定はこれから。** 2 リリースの取得手順と分母は
`docs/preregistration.md` に先に書く（後から分母を選べないようにする）。

---

## D21. Def 5 の値検証等級を 1 経路に統一する（両方向の誤りを直す）

**本項は「直すと決めた」記録である。期待値は `tests/test_value_grade.py` に
修正より先にコミットした**（`CLAUDE.md` 規則 5）。結果は末尾の「結果」に追記する。

### 事実（8 ケースで再現。`tests/test_value_grade.py` の fixture）

同一の Def 5 strong-path 条件を満たす検証子が、**書いた場所で等級が変わる**。

| ケース | 形 | 修正前の等級 | 修正前の verdict | Def 5 の期待 | 誤りの向き |
|---|---|---|---|---|---|
| a1 | inline `realpath` + `commonpath` | `weak(no_symlink_resolution)` | GAP_INJECT | `strong-path` | **false-dirty** |
| a2 | inline `Path.resolve` + `is_relative_to` | `weak(no_symlink_resolution)` | GAP_INJECT | `strong-path` | **false-dirty** |
| a3 | inline `realpath` + `startswith(base+os.sep)` | `weak(prefix_no_canon)` | GAP_INJECT | `strong-path` | **false-dirty** |
| b1 | helper が `realpath(root)` だけ通し、検査対象も sink も生の `path` | **`strong-path`** | **なし** | `weak(no_symlink_resolution)` | **false-clean** |
| b2 | `join(realpath(ROOT), path)` | `weak(prefix_no_canon)` | GAP_INJECT | weak | 正しい |
| b3 | 正規化した値を使わず生の値を sink へ | `weak(prefix_no_canon)` | GAP_INJECT | weak | 正しい |
| c1 | 検証なし | `None` | GAP_INJECT | `None` | 正しい |
| c2 | 付録 G `_prelude.validate_path` と同じヘルパー形 | `strong-path` | なし | `strong-path` | 正しい |

**b1 が最も重い。** `_validate_root_only` は `os.path.realpath(root)` しか通さず
`os.path.commonpath([path, base])` で**生の `path`** を照合するので
`/srv/data/../../etc/passwd` がそのまま通るが、現行の解析器はこれを clear する。

### 原因

Def 5 が 1 つなのに、実装が**互いに矛盾する 2 つの近似**になっている。

1. **inline 経路** `gate.py: _call_candidate` は形状 1 つを
   `_grade_from_shape` に渡し、docstring どおり「単独で strong にはしない」ので
   **構造的に weak 止まり**。囲み関数の本体をまとめて採点する経路が無い。
2. **helper 経路** `gate.py: _value_grade` は本体に現れた正規化子名の集合
   （`_transform_names`）と包含述語名の集合（`_containment_forms`）の**積**だけで
   strong-path を返す。どの値に適用されたかを見ない。
3. `analyze.py: _grade_of` は `value_grade.startswith("strong")` なら即 return し、
   `Value.attrs` も `ValResult.alias_facts` も参照しない。
   `validators.py: strong_path_requirements` と `ROOT_EQUAL_STEPS` は
   **定義のみで呼び出し元が 0 件**である。

**val は既に必要な証拠を出している。** `TRANSFERS` は symlink 解決子に
`canon_class="symlink"` と `attrs=("canonicalised",)` を持ち、
`engine.py` は `(root, site, transform)` を `alias_facts` に記録している。
**gate 側がそれを読んでいないだけである。**

### 決定

**strong-path を返す前に val の証拠で裏づける。** 判定を 1 か所に集約する:

* 条件 1（canonical alias の存在）= `alias_facts` に
  `root ∈ value.roots` かつ symlink 系 transform の行があること。
* root-equal = sink に届く値そのものが `canonicalised` 属性を持つこと。

この 2 条件は 8 ケースすべてを正しく分離する（b1 は canon 属性を持たず、
b2 は root `path` の alias を持たない）。**symlink 系 transform の集合は
`TRANSFERS` の `canon_class == "symlink"` から導出し、新しい語彙を作らない。**

inline 経路は `_grade_from_shape` をやめ、囲み関数の本体に対して helper 経路と
同じ採点を行う。**inline を strong に到達可能にするのは false-clean 方向の変更
なので**（`CLAUDE.md`）、上の 2 条件による裏づけと敵対的レビューを必須とする。

### 結果（2026-09-20 追記。**方向 = false-clean の退行**）

- 修正コミット `d745cb2` で A 群 8/8 が XPASS になり、凍結済みの受け入れ関門
  （B3a 8/8・B3b 15/15・変異 1/15・two_sided 7/7・厳密 0/7・INJECT 1/7・
  `diff_effects` 14 木 0/0/0）は**すべて通過した**。
- しかし `CLAUDE.md` の規則（opaque → resolved / weak → strong 方向の変更は敵対的
  レビューを通す）に従って行った敵対的レビュー（2026-09-20、94 エージェント、
  3 レンズ = 再現 / 攻撃成立 / D21 由来）で、**実際に木の外を読める・任意コマンドが
  動くのに `verdicts` が空になる false-clean を 29 件**確認した。うち **25 件は
  D21 が新たに入れた退行**（修正前は `GAP_INJECT`）、4 件は D21 以前からある
  helper 経路の欠陥。全件を `tests/test_d21_adversarial.py` に凍結した（`fe620c6`）。
- 機構は 4 つ（詳細は同テストの docstring）: **M1** `_grade_inline` の袋詰め採点
  （囲み関数の本体全体を `ast.walk` で集め、CFG も支配も主語も適用順序も見ない）、
  **M2** `_strong_path_backed` の存在量化（root の「どれか 1 つ」）、**M3** 領域不一致
  （パス包含の等級が `shell_string` / `sql` / `code_text` / `url.host` を clear）、
  **M4** 死んだ語彙（`ROOT_EQUAL_STEPS` / `ALLOWED_OPERANDS` / `post_check_append` の
  参照 0 件）。
- **上の「決定」が挙げた裏づけ 2 条件のうち実装したのは条件 1 だけ**で、root-equal
  （条件 2）は未実装のまま出荷していた。`_grade_inline` の docstring 自身が「片方だけを
  入れてはならない」と書いた状態そのものである。決定文と実装の食い違いを、
  受け入れ関門は 1 件も捕まえなかった。
- 条件 (iii) の未実装は本項にも `docs/open_questions.md` にも記録が無かった
  （規則 4 違反。黙って clear 側に倒していた）。
- **処置は D25**（変更 A の撤回 + M2 の全 root 要求 + M3 の領域検査）。
  b1 の修正（条件 1 の裏づけ）は残すが、その成立根拠は「root `path` の alias が
  無い」という偶発的な性質であり、同じ root への無関係な `realpath` 1 行で反転する
  （同テスト x01、O8 / O11）。**D21 が「直した」と記録した範囲は実際より狭い。**

---

## D20. `validator_holding_ratio` の分母を `docs/preregistration.md` で固定した（遡及させない）

- **いつ決めたか（正直に書く）: run6 の点推定と区間を見た後。** さらに
  「分母を変えると関門が反転する」ことを実測した後である。D18 と同じく、
  この順序を隠さずに書く。
- **事実**: 仕様書 §10 は `validator_holding_ratio` に閾値 5% を置くが
  **分母を書いていない**（:1101、:1143）。実装 `scripts/f0a.py:180` は
  `n_with_validator / n_units`（全ユニット）を採るが、根拠はどこにも無い。
  一方、仕様書 §6 の指標表は D 層別存在率について
  「分母は危険効果を持つユニットで、偽陽性クラスを除いた値と粗い値の両方を出す」、
  §10 は「分母はすべて危険効果を持つユニットであり、ツール全体ではない」と明記する。
  **`validator_holding_ratio` だけがこの原則の外にある。**
- **実測（`.venv/bin/python scripts/denominators.py evidence/f0a_run6`）**:
  ユニット分母 3 種 × パス分母 2 種 × 母集団 3 = 18 セルのうち、
  **関門 ≥5% に落ちるのは 2 セルだけ**（`all_paths × all_units` の mcp_server 4.43%、
  tool_package 3.26%）。残る 16 セルは通過する。公表済みの「関門 ×」は
  **最も分母が大きい 1 通りで計算した値**である。

**決定:**

1. **解析器の修正を先に行う。** 等級づけ（strong-path 判定）が両方向に壊れている
   間は validator の数を数え直しても意味が無い。修正の内容は別途。
2. **両側通過率の分子**（`expected_tuple_change` との照合が無い）は分母の問題では
   ないが同類型なので、同じ時期に手当てする。
3. **標本の拡大は (1)(2) の後。** 壊れた物差しで木を増やさない。
4. **分母の定義を `docs/preregistration.md` に固定した。** 主分母は
   `dangerous_fp_excluded × all_paths`、6 通りすべてを併記する。
   **ただしこれは「実装側の案」であり、学生の承認待ちである**
   （`docs/open_questions.md` O7）。選択が関門の合否を反転させる方向にあるので、
   実装側で黙って確定させない。

**遡及させない理由（この決定が判定を有利にしない理由）:**

主分母 `dangerous_fp_excluded` の根拠は仕様書の明文の原則であって観測値ではない。
しかし**選択が関門を × → ○ に反転させると知った後の選択**である以上、
その反転を「関門を通過した」という主張に使ってはならない。したがって:

- run6 の関門判定は公表済みのまま据え置く。`docs/f0a.md` / `docs/f0a_ci.md` /
  `docs/f0a_run*.md` の数値と判定は**書き換えない**。
- 新分母での値は「分母を変えるとこうなる」という**感度分析**として報告する。
- 関門の再判定は、preregistration.md のコミット後・(1)〜(3) の後に取る run で行う。
- §10 A5 の対処（validator 保有 < 5% → クラス 2 は T1+T2 のみ）は
  **その再判定まで保留**。run6 の × を根拠にクラス 2 を落とさないし、
  新分母の ○ を根拠に維持するとも主張しない。

**仕様書は書き換えていない。** §10 が分母を書いていないという事実はそのまま残し、
埋めた内容を preregistration.md に置いた（`CLAUDE.md` 規則 6）。

---

## D1. 語彙を拡張した（形状 11→12、weak 理由 19→22）

**月 6 の凍結前なので逸脱ではない。** 凍結後に動かす場合は
`docs/preregistration.md` に逸脱として記録すること。
実装の記録は `authgap/catalog/validators.py: VOCABULARY_REVISIONS`。

| 追加 | 何 | なぜ |
|---|---|---|
| 形状 | `absolute`（`os.path.isabs` / `Path.is_absolute`） | §2.6 の fixture F7 が `absolute_only` を weak 理由として要求しているのに、絶対パス検査を形状として数える語が無かった |
| weak | `absolute_only` | 同上。絶対パス検査だけの検証子が `unknown`（判定不能）に落ち、weak と区別できなかった |
| weak | `existence_only` | 同上（F7 が名指ししている） |
| weak | `statement_type_only` | **A18（langroid）で実際に当たった。** 修正は `sqlglot.parse` で正規化してから**文型**の allowlist を掛ける。値そのものは自由な SQL のままなので strong ではなく、拒否リストでもないので `denylist_enum` でもない。既存語彙のどれにも当たらず `unknown` になっていた |

witness も同時に足した（`WITNESS_TEMPLATES` は全 weak 理由を覆う。テストで固定）。

**Def 5 が「19 語」と書いている箇所は、この改訂後は 22 語として読む。**

## D2. 付録 G の G12 の reason は `deny_reaches_effect`

- 仕様書の付録 G は G12 の期待を `NODOM` とだけ書き、reason クラスを書いていない。
  §2.5.6 B3b は 3 つ組一致を要求するので空にできない。
- **導出**: 承認の拒否辺は `finally(exc)` 複製へ入り、その複製が効果そのものなので
  `d ∈ Reach(s)` が成り立つ。
- あわせて、実装変異 `no_finally_copies` が生存する件も確定させた:
  - 付録 G の 15 件は `finally` 複製の有無を判別しない（G12 で効果行に対応する
    CFG ノードは 2 個対 1 個になるが、3 つ組は一致する）。`(G-i)∧(G-ii)` が
    先に同じ誤りを捕まえるため。
  - **生存数は 1/15 のまま報告する。** §2.5.6 の定義どおり、生存数は付録 G と
    支配 mutant の fixture テストだけで数える。
  - ただし複製の性質そのものは `tests/test_cfg_structure.py` で構造的に固定した。
    **この単体テストは生存数の計算に入れない**（入れると定義が変わる）。

## D3. §8-7: in-tree の露出宣言を D_op に**含める**

- Def 6 の D_op 節の条件をそのまま課す — `enabled=` の式が真偽 config atom に
  解決でき、**かつ atom の既定が閉**のときのみ D として読む。既定が開なら
  `D ⊭ e` 側に倒し、解決できない式は `opaque` として記録して**どちらにも数えない**。
- 前測の実使用は 0 件なので数値影響は無い見込みだが、§8-7 は「含めるか否かを
  先に決める」ことを要求しているので既定を明示した。
- 実装: `authgap/dparse.py: INCLUDE_IN_TREE_EXPOSURE = True` と
  `in_tree_exposure` / `exposure_as_d_op`。

## D4. A1 / A2 の期待タプルは測定値を採る

- 一次確認の結果、仕様書 §6 T1.2 の**脆弱側**が 2 件とも誤っていた。

  | 対 | 仕様書 | 一次確認した実際 |
  |---|---|---|
  | A1 | `weak(prefix_no_canon)` | **検証子が 1 つも無い**（`Path(arguments["repo_path"])` が直接 `git.Repo` へ） |
  | A2 | `weak(no_dash_reject)` | **検証子が 1 つも無い**。さらに仕様書は `git_checkout` しか挙げていないが `git_diff` も同じ修正を受けている |

- **`docs/cve_triage.csv` の `expected_tuple_change` を採点前の凍結値とする。**
  仕様書の値は同じ行の `spec_expected_tuple_change` に残す（監査用）。
- 両側判別可能性は変わらず成立するので §6 T1.5 の算入数は動かない。
  消滅理由は A1 が `normalisation-add` 単独ではなく `validator-add` を含む。

## D5. セレクタ（`req_occ` の主語）の運用定義

Def 5 は「ディスパッチキー（セレクタ）そのものを主語とする allowlist」としか
書いていないので、機械的な決め方を次で確定した。

1. 被呼び出しが `Subscript`（`TOOLS[name](args)`）なら添字がセレクタ。
2. ユニット本体で dispatch キーの位置に現れる式（`REGISTRY[x]` / `X.get(x)` /
   `if x == "..."` / `match x:`）の名前を val の env で root へ写す。
3. どちらも取れなければ、ユニット入口の仮引数のうち効果の実引数に現れないもの。

3 は暫定だが、G11（主語不一致 → `non_binding_gate`）と G15（`dispatch(name, argstr)`
から `git_log(argstr)` を直接呼ぶ形で `name` がセレクタ）の両方を満たす最小の規則である。

## D6. 主語一致は root で取る

- `Value.roots`（MODEL 導入点の集合）を主語一致の照合に使う。root は名前の
  書き換え（`safe = validate_path(path)`）を跨いで保たれるので AST 名の一致より正確。
- 添字は root を精緻化する（`arguments["repo_path"]` と `arguments["target"]` を
  同じ root に潰さない）。**潰すと片方への検証が他方の位置に付く**（Def 5 が
  禁じている型エラーが主語一致をすり抜ける）。
- 付録 G のハーネスだけは名前一致に落ちる（val を走らせずゲート層だけを試す
  ためで、期待値は 15/15 で通っている）。

## D7. §8-1 の (d)（SELECT 格下げ分岐）は承認を要さない

§3 と §10 が「この条項は撤回しない」と書いているので、指導教員の合意事項では
なく**仕様内規則**として扱う。拒否分岐は作らない。

## D8. config atom は 4 源すべてを読む

Def 5 の 4 源（コンストラクタ kwarg / モジュール定数 / `os.environ` /
CLI オプションの既定値）を `authgap/atoms.py` で実装した。

- **同じ名前で既定値が食い違うときは解決しない**（`AMBIGUOUS`）。推定で片方を
  採ると既定閉と既定開を取り違え、`req` を誤って引き上げる（false-clean 方向）。
- pydantic の `Field(default=...)` は読むが `default_factory=` は読まない
  （値が静的に決まらない）。

## D9. 低レベル MCP の `trig` は `traced`（測定）

仕様書 §3 / §10 は「MCP サーバでは dispatch が framework 内にあるので trig は
常に `assumed`」と書くが、**低レベル経路では `traced` になる**。

| 登録形 | trig | 測定した木 |
|---|---|---|
| 低レベル `@server.call_tool()` | **traced** | mcp-server-git（3/3 ユニット） |
| 高レベル `@mcp.tool` | assumed | langroid 同梱の MCP fixture |
| `@command(名前, 説明, {スキーマ})` | assumed | AutoGPT |
| `tools=[f, g]` の裸の関数 | assumed | PraisonAI |
| `ToolMessage` 派生 + 同名ハンドラ | assumed | langroid |

影響:

- §3 の「MCP サーバだけにすると交差行は fixture からしか出ない」は
  **高レベル経路についてのみ正しい**。
- §10 の B1 関門「T3-app の traced 率 ≥ 20%」は、低レベル MCP サーバ自体が
  traced ユニットを供給するので T3-app に頼らず満たせる可能性がある。
- **`traced_ratio` は母集団別（低レベル / 高レベル / ツールパッケージ）に出す。**
  1 つに平均するとこの構造差が消える。

## D10. 交差行は低レベル MCP からしか出ない → §3 は現時点で不合格

- 4 プロジェクト 7 木で測って交差行 12 行、**すべて mcp-server-git 由来 = 1
  プロジェクト**。§3 は「3 行が異なるプロジェクト由来」を要求するので不合格。
- AutoGPT が 0 行なのは**正しい**。ディスパッチは
  `agent.command_registry.get_command(command_name)` で `self.commands` は
  実行時に埋まる辞書なので、Def 4 の `OPAQUE(dynamic_registry)` に当たる。
  推定で候補を埋めてはならない。
- **決定**: 高レベル登録形をいくら足しても交差行は増えないので、C1 の標本設計で
  **低レベル MCP サーバを意図的に含める**か、§3 の「統一の証拠は逸話的」／
  「三部品として報告する」分岐に入るかを、**標本抽出の前に**決める。
  抽出後に決めると事後選択になる。

## D11. `verdict-clearing` は 2 通り出す

§6 T1.1 の副次指標は「修正版で verdict が GAP から外れる対の数」だが、
実データでは厳密版がほぼ常に 0 になる。理由は `GAP_SELECT` が
「モデルがそのツールを呼ぶかを決めており、承認割り込みも宣言も無い」ことを
言うので**値検証を足しても消えない**から。

したがって次の 2 つを**必ず並べて**出す（`scripts/two_sided.py`）。

- `pair_cleared`（厳密）: 変化した経路に GAP が一切残らない
- `pair_cleared_inject`: 変化した経路に `GAP_INJECT` が残らない

**片方だけを書くと、SELECT 座標が常に残ることを隠すか、値検証の効果を
見落とすかのどちらかになる。**

## D12. R2 カタログに 4 形を追加した

較正対がそれ無しでは入口 0 件になるので、Def 2 の R2 カタログを拡張した。

| 追加 | 形 | 必要だった対 |
|---|---|---|
| `autogpt` | `@command(名前, 説明, {スキーマ}, ...)` | A5 |
| `langroid` | `ToolMessage` 派生の `request` と同名のハンドラ | A18 |
| `tools-list` | `tools=[f, g]` / `tools=["f","g"]` / `def get_*_tools(): return [f, g]` | A9 |
| （既存の精密化） | `@command` のスキーマ辞書のキーに無い仮引数は MODEL としない | A5（`agent` を MODEL にしない） |

**限界（2026-09-14 追記）: `tools-list` 形は呼び出しの `tools=[...]` キーワードを
すべて手がかりにするので、登録ではない呼び出しも拾う。** 野外の w-giak__mnemo-lite は
`logger.info("...registered", tools=["get_indexing_errors", ...])` とログにツール名を並べて
おり、これが入口の手がかりになった。そこに並ぶのが本当に登録済みのツールなら被害は
重複だけ（同じ関数が `mcp` と `tools-list` の 2 ユニットになる欠陥。修正待ちで
`tests/test_f0a_defects.py` 12 節に固定）だが、無関係な関数名を並べれば誤った入口になる。
呼び出し先を Agent / Crew などに限る案は、F0a の標本を見た後にカタログを絞ることになるので
採らず、この広さを限界として報告する。

**スキーマ辞書による除外は名前のブラックリストより強い根拠である**
（フレームワークが機械可読に「モデルが埋める引数」を宣言しているため）。
`@click.command()` と末尾名が同じなので、位置引数 3 個と第 1 引数が文字列定数で
あることを構造条件にして分けた。

## D13. Semgrep baseline は強化してから比べる

- **弱い baseline は AuthGap を実際より良く見せる。** 最初のルールは
  R2 デコレータの引数しか source にしておらず、mcp-server-git のような
  低レベル経路で所見 0 になっていた（比較が成立しない）。
- 強化した内容: 低レベル MCP ハンドラの `arguments` を source に追加、
  GitPython の proxy 形を sink に追加、過剰一致していた `$S.run(...)` を削除。
- **結果は変わらなかった**（AuthGap 7/7、Semgrep 0/7）。強化前後で同じ結論に
  なったこと自体が、結論が baseline の弱さに依存していないことの根拠になる。
- **増減を分けて報告する。** 「所見の集合が変わったか」だけで数えると、
  修正でコードが増えて所見が増えた対（A9）が「両側通過」になり、baseline が
  修正を検出したように見える。`two_sided_pass_by_disappearance` を主指標にする。
- §6 T1.5 (ii) は Semgrep と Pysa の両方を要求する。**Pysa は未実施**
  （pyre 環境の構築が要る）。§6 は「D13 までに環境が立つ repo が 0 なら
  baseline から落として『pyre 依存 baseline は環境コストにより不成立』と
  報告する」としている。

## D14. F0a は「直す前の解析器」で 1 回測り、直したら run を分けて両方出す

**状況。** 野外 3 木の煙試験で効果サイトが 21/21 `opaque` になった。原因の候補は
モジュール大域の名前（`github_client = GitHubClient(...)` のような木内の束縛）を
val エンジンが読まず `opaque(unresolved)` にしていること。Def 4 は
`opaque(unresolved)` を「**木内で解決できない**呼び出し」に限っており、
config atom の源にモジュール定数を数えている（§2.3）ので、仕様より弱い実装である
可能性が高い。一方で §10 は `in_tree_resolution_ratio < 50%` なら母集団を
切り替えると定めており、**実装の弱さが母集団の性質として報告されうる。**

**決定。**

1. **run 1 = `authgap/` が commit `9c2bb11` と同一の解析器で F0a を測る。**
   実行時の HEAD は `730c948`（スクリプトと文書だけが違う。
   `git diff 9c2bb11 730c948 -- authgap` は空）で、これが
   `evidence/f0a/f0a.json` の `run_meta.analyzer_commit` に入っている。
   関門の判定はまず run 1 で出す。
2. run 1 のユニット行を**読む前に**、検証標本の抽出手続き
   `scripts/sample_f0a_checks.py`（seed 20260914、6 層、効果サイトは
   (木, relpath, lineno, kind) で重複除去）をコミットする。検証対象を結果を
   見てから選ばないため。
3. 標本の各件を原ソースに当てて「木内で解決できるのに opaque」「本当に
   解決できない」などに分類し、**解析器の欠陥として数えたものだけ**を直す。
   直したら run 2 を取り、**run 1 と run 2 を commit で区別して両方報告する**。
   関門を通すために直したと読まれうるので、片方だけを出さない。
4. **ゲート語彙（weak 理由・strong の定義・OPAQUE/NODOM）には触らない。**
   held-out G16–G20 は F0a コーパスから seed 付きで抽出する規定（§2.5.7）なので、
   F0a の木を見てゲート語彙を動かすと held-out が汚れる。val エンジンの名前解決は
   ゲート語彙ではない。
5. 検証標本の分類は**機械による事前点検であり C2 のラベルではない。**
   論文に載せる検証は学生が `docs/verification_guide.md` の手順で行う。

## D15. §10 の解決率・opaque 率は「効果サイト」単位で判定し、行単位を併記する

**決めた時点: 野外 run 1 の結果を 1 件も見る前**（煙試験 3 木のみ）。

- **食い違い。** §1 は `in_tree_resolution_ratio` を「**効果サイト**の解決率」と
  書くが、実装（`report.py` の probe と `f0a.py`）は**効果行**を数えていた。
  効果行は呼び出し経路ごとに複製される（§2.6「指数項は出力側に現れる」）。
  煙試験では 1 サイト（`github_client.py:82`）に 21 行が集中しており、行で数えると
  そのサイト 1 つの確度が母集団の率をほぼ決める。
- **決定。** 関門の判定は仕様の文言どおりサイト単位（(木, relpath, lineno, kind)
  で重複除去）で行う。opaque 率も同じくサイト × slot 単位。**行単位の値も必ず
  併記する**（`f0a.json` の `*_sites` と無印の両方）。
- **同一サイトに異なる確度の行があるとき**は `prov_merge` と同じ
  `opaque > remote > resolved` で合流する。**1 経路でも opaque ならそのサイトは
  opaque**（resolved を優先すると無言の false-clean になる）。
- **この決定は結果を見る前に固定したので、結果によって行 / サイトを選び直さない。**

## D16. 野外 run 2 以降は解析器を Python 3.12 で走らせる（run 1 の 3.10 は残す）

- **状況。** run 1 の parse 失敗 91 ファイルのうち 67 件は PEP 695（`type X = ...`、
  `def f[T]`）と PEP 701（f-string 内の同種引用符）で、**解析器を 3.10 で走らせて
  いるから読めない**だけだった（`uv python find 3.12` の 3.12.13 で再 parse すると
  全件 parse できる。`evidence/f0a/parse_failures.json` の `parses_in_newer_python`）。
  野外の MCP サーバは新しい Python で書かれていることが多く、この損失は偏りを持つ
  （新しいコードほど落ちる）。
- **仕様との関係。** §5.3 は「**Python 3.10+**」であり、3.12 で走らせるのは仕様内。
  前身の実測が 3.10.12 だったのは前身の事情。
- **3.12 に替えても較正結果が変わらないことを確かめた**（2026-09-14、`authgap/` は
  commit `9c2bb11` と同一）:

  | 確認 | 3.10.12 | 3.12.13 |
  |---|---|---|
  | B3a 支配 mutant | 8/8 | 8/8 |
  | B3b 付録 G | 15/15 | 15/15 |
  | 実装変異の生存 | 1/15 | 1/15（同じ `no_finally_copies`） |
  | pytest | 70 passed | 70 passed（`-W error::DeprecationWarning`） |
  | 両側条件 | 7/7、厳密 0/7、INJECT 1/7 | 同じ |
  | `scan corpus/A1__fixed` の 4 出力 | — | volatile を除いてバイト同一 |

- **決定。** run 2 以降は `.venv312`（`uv venv .venv312 --python 3.12`）で走らせ、
  `run_meta.python` に版を記録する。**run 1（3.10）はそのまま残し、run 2 と並べる。**
  run 1 と run 2 の差には「解析器の修正」と「処理系の変更」が混ざるので、
  **処理系だけを替えた run（解析器は run 1 と同一）も取って差を分解する。**
- **3.12 でも読めない 18 件**（雛形 5、壊れたファイル 13）は parse 失敗として残る。

## D19. レビューと修正の繰り返しを止める条件（F0a に使う解析器の凍結）

- **いつ決めたか: 4 回目のレビュー（ea35672 の差分）を走らせる前。** 結果を見て条件を
  選び直さないため、ここに先に書く。
- **状況。** F0a run 1 の後の解析器の修正は、敵対的レビューのたびに新しい欠陥が見つかった
  （1 回目: 確認 8、2 回目: 確認 5、3 回目: 確認 6。棄却はいずれも 0）。多くは「解決を
  増やす修正」が作った false-clean で、深刻度は回を追って下がっているが 0 にはなっていない。
  止める規則が無いと、関門の数字を好きな回で止めて選べてしまう。
- **決定。**
  1. **凍結の条件:** 直前の修正の差分だけを対象にしたレビューで、**false-clean・効果行の
     消失・クラッシュの向きの確認済み指摘が 0 件**になったら、その解析器を F0a の報告に使う
     版として凍結し、`fingerprint` とタグを付ける。
  2. **精度の損失（誤警報の向き、opaque を増やす向き）の指摘は凍結を妨げない。** 限界として
     件数と形を記録し、報告の前には直さない（直すと解決を増やす変更になり、再びレビューが要る）。
  3. **上限:** 4 回目のレビューで上の向きの指摘が確認されたら、テストを先に固定して直し、
     その差分だけを 5 回目のレビューにかける。**5 回目でもなお確認されたら、繰り返しを止め、
     残った指摘を向きと件数つきで既知の欠陥として報告する**（直した版の run は取るが、
     その版を「欠陥が無い」とは書かない）。
  4. **各回の run を残す。** run 2〜5 はそれぞれ、どの指摘で中間状態になったかを
     `docs/f0a_runs.md` と `verification_guide.md` §3.2 に書く。関門の数字は凍結した版の run の
     ものだけを使い、区間（D18）を併記する。
- **この規則の限界。** 敵対的レビューで指摘が 0 件でも欠陥が無いことは示せない。凍結は
  「この手続きで見つからなかった」ことの記録であり、論文にもそう書く。

### D19 の結果（2026-09-14）: 凍結しない。150e06a（run 6）を、既知の欠陥を明記して報告に使う

- **4 回目のレビュー**（ea35672 の差分、`wf_0befeae9-69c`）: 確認 6・棄却 0、6 件すべて凍結を妨げる向き。
  D19(3) により、テストを先に固定して直した（D17 改訂 5、150e06a）。
- **5 回目のレビュー**（170a7b2..150e06a、`wf_bca6c11f-6f1`、3 観点）: 指摘 4・確認 4・棄却 0。
  4 件すべてが凍結を妨げる向き（false-clean 1、効果行の消失 3。うち 2 件は同じ欠陥 K1 を 2 観点が
  独立に指摘）。精度の観点（run 5 と HEAD の実データ比較）は指摘 0。
- **D19(3) により繰り返しをここで止め、直さない。** `scripts/freeze_f0a.py` は走らせない（確認済み指摘が
  0 でないときは exit 3 で拒む設計）。タグも打たない。run 6 は「この手続きで欠陥が見つからなかった版」
  ではなく、**「5 回目のレビューで下の既知の欠陥が確認された版」**として報告する。

**既知の欠陥**（`tests/test_f0a_defects.py` 15 節の `KNOWN` 印。直したら XPASS で知らせる）:

| id | 形 | 向き | いつから | 出所 | F0a 標本 98 木の構文上の候補 |
|---|---|---|---|---|---|
| K1 | spawn の argv0 がモジュール水準のリスト、または shell= が `global` で書き換えられる名前のとき、`_pipe` が判定できないのに FS_WRITE の側だけを出し、pipe 書き込みの EXEC(code_text) 行が消える | 効果行の消失 | 改訂 5 の退行（170a7b2 は EXEC） | 5 回目（2 観点が独立に指摘、検証者が再現） | 0 |
| K2 | 関数内の `global run_command` と入れ子 def で書き換えられる名前を、モジュール直下の安全な def に resolved で決め打ちする | false-clean | 改訂 5 の退行（170a7b2 は行 0 / opaque） | 5 回目（検証者が再現） | 0 |
| K3 | 同じく関数内の `global run_command; run_command = f`（代入） | false-clean | 改訂 5 より前 | 5 回目の指摘者が件数上限の外として挙げた形。150e06a と 170a7b2 を自分で走らせて再現 | 0 |
| K4 | メソッドの中の入れ子 def と同名の、モジュール直下の def に決め打ちする（入れ子 def に classname が付き候補から外れる） | false-clean | 改訂 5 より前 | 同上 | 0 |
| K5 | 囲む関数の局所 import と同名の、モジュール直下の def に決め打ちする | false-clean | 改訂 5 より前 | 同上 | 0 |
| K6 | 3 段入れ子のモジュール水準 dict の要素に tool が書き込む URL が、`_opaque_deep` の深さ上限（2）を超えて url.host = OP / resolved になる | false-clean | 改訂 5 より前 | 同上 | 0 |
| K7 | 別名つき from-import（`from .net import fetch_url as http_get; http_get(url)`）で木内の関数へ降りず、被呼び出しの効果行が全部消える。import 表は `pkg.net.fetch_url` を正しく引くが、定義を探す名前に呼び出し式の局所の別名を使う（`_resolve_in_tree` の `last`） | 効果行の消失 | 最初の解析器の commit から（検証者が 04e5f9b / 0662b39 / 170a7b2 / 150e06a で確認） | 5 回目（検証者が再現） | **32 木・693 箇所**（mcp_server 23 木 469、tool_package 5 木 86、app 4 木 138） |

候補の数え方は `scripts/scan_known_defect_forms.py`（構文だけの走査。K1〜K6 は検証用の 7 fixture をすべて検出し、
K7 は別名ありの 2 形を検出して別名なしの対照を検出しないことを確かめてから標本に当てた）。**K7 の数は、
テスト・スクリプトを含み、ユニットから到達するかを見ていない上限値である。** K1 / K2 は改訂 5 で出力が
変わる形なので、run 5 と run 6 のバイト一致とも整合する。

**K7 は run 6 の数字に効いている。** 検証者は、run 6 で w-datawhalechina__video-devour の 5 ユニットすべてと
w-saiyandev17__agent-sentinel の 23 ユニット中 21 が効果 0 件であり、別名の元の名前で定義を引く実験パッチ
（コミットしない）でそれらに FS_READ / DB / NET の行が現れることを示した。影響の大きさは下の感度分析で
見積もるが、**感度分析の数字は関門の数字として使わない**（D19 の順序を守る）。K7 を直して run 7 を取るかは
D19 を破る判断になるので、学生に委ねる（`docs/open_questions.md` O6）。

**K7 の感度分析（関門の数字ではない）:** 150e06a の `git archive` に 3 行の実験パッチ（呼び出し式の局所の別名では
なく、import 表が指す元の名前で定義を引く。`evidence/f0a_sens_k7/sensitivity_patch.diff`。**コミットしない**）を
当て、run 6 と同じ標本・上限・処理系（3.12.13）で F0a を取った（`evidence/f0a_sens_k7/`。archive なので
`analyzer_commit` は null。`authgap/` の差がこのパッチだけであることは 150e06a の全ファイルとの `cmp` で確かめた）。
走らせる前に、パッチが別名あり 2 形の fixture で NET 行を出し、別名なしの対照を変えないことを確かめた。

| mcp_server（60 木） | run 6 | 感度分析 |
|---|---|---|
| 危険効果を持つユニット（偽陽性クラス除外） | 431 | 457（+26。すべて効果 0 件だったユニット） |
| 効果サイト / 効果行 | 444 / 1251 | 460 / 1405 |
| `in_tree_resolution_ratio_sites`（関門 ≥ 50%） | 33.6% [18.6%, 51.3%] ×（境界） | 32.6% [18.0%, 49.5%] ×（区間も閾値の下） |
| `opaque_ratio_primary_slots_sites`（関門 ≤ 40%） | 43.5% [20.8%, 68.0%] ×（境界） | 44.1% [22.2%, 68.1%] ×（境界） |
| `validator_holding_ratio`（関門 ≥ 5%） | 4.4% [2.4%, 7.4%] ×（境界） | 4.4% [2.4%, 7.4%] ×（境界） |

- 変わったのは mcp_server の 6 木・47 ユニット行だけで、tool_package と app は全指標が同一。効果行の消失 0、
  危険効果から外れたユニット 0（`lost_units.py evidence/f0a_run6 evidence/f0a_sens_k7`、およびユニットの重複キーを
  考慮した行単位の突き合わせの両方で確かめた）。
- 構文上の候補（mcp_server 23 木）より実際に変わった木（6 木）が少ないのは、候補にユニットから到達しない
  呼び出し（テスト・スクリプト・CLI）が多いため。
- **K7 は mcp_server の効果サイトを 16（感度分析の 3.5%）少なく数え、危険効果を持つユニットを 26（同 5.7%）
  見落としていた。** 関門の判定（点推定の ○ / ×）は変わらないが、解決率の区間は「境界」から「閾値の下」に移る。
  **run 6 の数字を書くときはこの表を併記する。**
- 区間は `scripts/f0a_ci.py` の `per_tree` / `bootstrap`（seed 20260914、2000 回）を感度分析の証拠に当てて求めた
  （`docs/f0a_ci.md` には入れていない。関門の表と混ぜないため）。

**別に見つかった記録事項:** run 6 の `units.jsonl` には、(母集団, 木, `unit_id`) が同じで中身の違う行が
194 キー・234 行ある（例: w-eggressive__mcp-build の `mcp:get_weather:985793b628ca` が 3 行）。`unit_id` は
木の中で一意ではない。キーで辞書を作る突き合わせは重複行を潰すので、上の突き合わせは位置を揃えて行ごとに
比べ直した。`scripts/lost_units.py` はユニットを (母集団, 木, `unit_id`, relpath, 入口の行) で識別しており、
このキーでは run 6 と感度分析の証拠のどちらにも衝突が 0 件なので、`lost_units.py` の結果はこの重複の影響を
受けない。**`unit_id` 単独で行を突き合わせる新しいスクリプトを書くときは、relpath と行をキーに含める。**

**手続きの限界として書くこと:** 確認件数は 8 → 5 → 6 → 6 → 4 で、0 に近づかなかった。回ごとの指摘の多くは
直前の修正が作った退行だったが、K7 のように**最初からあって影響の大きい欠陥が 5 回目で初めて見つかった。**
各回のレビューは直前の差分に焦点を当てたので、差分の外にある欠陥を系統的には拾わない。

## D18. §10 関門の率には木単位のブートストラップ区間を併記する（判定は点推定のまま）

- **いつ決めたか（正直に書く）: run 2 の点推定を見た後。** run 2 で mcp_server の
  `in_tree_resolution_ratio_sites` が 51.0%（閾値 50% の 1 pt 上）、tool_package が
  49.5%（0.5 pt 下）になった。60 木 / 30 木の標本で、サイトは木に集まる（1 木に数十
  サイト）ので、この差を合否として読める精度が無い。
- **決定。** `scripts/f0a_ci.py` で、抽出単位の**木**を復元抽出するクラスタ・
  ブートストラップ（seed 20260914、2000 回、パーセンタイル 95%）の区間を付ける。
  **関門の判定規則（§10 の点推定と閾値）は変えない。** 区間が閾値を跨ぐものは
  「境界」と書き、**点推定だけで「関門を通過した」「通過しなかった」と主張しない。**
- **この決定が判定を有利にしない理由。** 区間は判定を変えず、「○」を「境界」に
  格下げする方向にしか働かない。区間を見て閾値や分母を選び直すことはしない。
- run 1 / run1py312 / run 2 すべてに同じ手続きを当てる（`docs/f0a_ci.md`）。
- **run 2 の `run_meta`**: `analyzer_commit` は実行終了時の HEAD（`d6b608c`）だが、
  `authgap/` は `0662b39` と同一（間のコミットはスクリプトと文書だけ）。標本は
  訂正前（`b3aa2c8` の `corpus_sample.json`。run 2 は開始時に読み込んだ後で標本を
  引き直した）。run 2 以降は `sample_sha256` で内容を記録する。

## D17. 事前点検の所見のうち「直すもの」と「直さないもの」

根拠: `docs/f0a_checks.md`（`evidence/f0a/check_results.json`）。**点検者の
analyzer_wrong をそのまま欠陥と読まない。** 仕様の定義に照らして振り分けた。

**直す（仕様がすでに要求している挙動、またはカタログにある形の取りこぼし）:**

| 所見 | 誤りの向き | 仕様の根拠 |
|---|---|---|
| `list.append` 等を受け手への書き込みとして扱わない（RES[7]） | **false-clean** | §2.6「決して clean に潰さない」 |
| 受け手型が付かず sink を落とす: 局所変数の `Path`、callee クラスの `__init__` で束縛した `self` フィールド、木内関数の戻り値注釈、クロージャ変数（NOE[1,4,6,10,11]） | **false-clean** | §2.6 の heap / Obj.fields / 受け手アクセスパス |
| 受け手型なしで末尾名が唯一の関数へ解決する（EFF[6]） | false-alarm | Def 4「木内で解決できない呼び出しは `opaque(unresolved)`」。**直し方を改訂（下記）** |
| URL slot 分割規則が未実装（OPQ 9 件） | precision loss | §2.6 の URL 分割規則（falsifiable な形で書かれている） |
| モジュール大域の名前を読まない（OPQ 8 件） | precision loss | Def 4（木内で解決できる）、§2.3 の config atom の源 |
| `os.environ` 読み出しを config として扱わない（OPQ 4 件） | precision loss | §2.3 の config atom の源 4 種 |
| BOM 付きファイルを parse 失敗にする（6 件） | false-clean（ユニットが消える） | §5.2 |
| `@mcp.tool(annotations=...)` を読まない、明示の `annotations=None` を unreadable にする | D の過小評価 / `D_unknown` の過大 | Def 6（3 形のパーサ、読めない形だけが `D_unknown`） |
| AutoGPT `@command` の名前 list 形・キーワード形、`tools=[...]` の入れ子関数 | false-clean（ユニットが消える） | R2 カタログにある形（D12） |

**直さない:**

1. **VAL 層の 13 件（`split` / `Path()` / 正規化の `startswith` を形状と数える）。**
   §6 F0a の validator 形状は**構文的**であり、語彙（月 3 凍結、11 語）に `split` と
   `ctor_path` を含む。点検プロンプトは「拒否の形で使われているか」を基準にしたので
   仕様より厳しい。**解析器は仕様どおりである。** この 13/20 は「構文的形状の保有が
   実際の検証の保有を表さない率」という**妥当性の注記**として本文に書く
   （§10 の「validator 保有 ≥ 5%」はこの構文的な量で判定する。定義は動かさない）。
2. **unit id の衝突**（同じツールが 5 ファイルに複製）。§5.1 は unit id を
   `framework:qualified_name:schema_hash` と定義し「ファイル移動に安定」を意図している。
   複製されたサーバが同じ id になるのは定義どおり。
3. **カタログに無いツールの形**（llama-index `FunctionTool.from_defaults`、SuperAGI の
   `_execute`、OpenHands の `ToolDefinition` など）。**F0a の標本を見てカタログを
   広げると測定集合で調整することになる。** 取りこぼしとして件数を報告する
   （ユニット 0 件の木 26 本中 9 本 + 混在 2 本）。カタログの拡張は月 10 の指紋凍結前に、
   標本外の根拠（フレームワークの公式文書）で行う。
4. **3.12 構文**は D16（処理系の変更）で扱い、解析器の修正とは分けて報告する。

**改訂（2026-09-14、較正対の差分による）: 末尾名だけの解決は「やめる」のではなく
「opaque にする」。** 最初は受け手型の無いメソッド呼び出しを解決しない（降りない）
ように直したが、較正対 A9 / A18 の効果行を直す前後で突き合わせたところ、**真の経路が
消えていた**:

- A18（langroid）`LanceDocChatAgent.query_plan` → `self.vecdb.compute_from_docs` の
  `compile` / `eval`（`vecdb: LanceDB` は `VectorStore` の派生で、受け手型が推論できない
  だけ）
- A9（PraisonAI）`acp_*` → `ActionOrchestrator.apply_plan` → `_apply_step` の `subprocess.run`
- A9 `stt` → `AudioAgent.transcribe` の `open`

一方で消えて正しかったのはテストの模擬クラス 1 件（`MockSpeechResponse.stream_to_file`）
だけだった。**効果を落とすのは false-clean で、EFF[6] の false-alarm より重い**（§2.6
「決して drop しない」）。したがって: 末尾名で一意に決まるなら降りて効果を出すが、その
経路の上の行の確度に `opaque(unresolved)` を合流する（resolved と数えない）。EFF[6] は
「resolved の誤った効果」から「opaque の効果」に変わる。この改訂は
`tests/test_f0a_defects.py` の `test_untyped_receiver_by_name_hop_*` が固定する。

**同じ差分で見つけた退行（直した）:** `append` を受け手への書き込みとして扱うように
したことで、`cmd = ["sg", ...]; if f: cmd.append(x)` の分岐合流が長さの違う列の join に
なり、`_shape_join` が要素を全部捨てて argv0 のリテラル `"sg"` が列全体（MODEL）に
なっていた（A9 `ast_grep_rewrite`）。共通の先頭を要素ごとに join し、はみ出しを tail に
畳むようにした（`test_branch_join_keeps_argv0_literal`）。

**改訂 2（2026-09-14、0662b39 の敵対的レビューによる）: D17 の修正そのものが
false-clean を 5 系統作っていた。** 観点別の点検者 4 名が指摘し、独立の検証者が最小
fixture で再現した 8 件（棄却 0）と、検証者が見つけた変形を、すべて修正より先に
`tests/test_f0a_defects.py` に固定してから直した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| モジュール水準の束縛 | 直下の代入だけを join したので、関数内の `global X; X = model`、別ツールの `SETTINGS["k"] = model`、入れ子関数が掴む同名の外側局所変数を見落とし、**定数の OP / resolved** にした（以前は opaque） | false-clean（verdict が消える） | 関数内で束縛・`global` 宣言される名前、どこかで変更される名前、他モジュールから `m.NAME = ...` と書かれる名前は読まない（`_WriteScan`、`_tree_attr_writes`） |
| `os.environ` | env を見る前に config 値へ短絡したので、同じ関数で書いた MODEL の読み戻しが OP になり、別モジュールの書き込みも無視した | false-clean（MODEL → OP） | 読み戻しに env の書き込みを含める。木内のどこかで非定数を書き込むなら環境変数を config とみなさず opaque |
| URL 分割（テンプレート） | `"%s://%s/api" % (...)` / `"https://{}/x".format(...)` のプレースホルダを host のリテラルとして切り出した | false-clean（MODEL の host を OP） | scheme / host の文字列に `%` `{` `}` があれば分割しない |
| URL 分割（非リテラル枝） | `f"{prefix}{host}/v1"`（prefix は scheme だけ）で url.host を prefix にした | false-clean | 直後が `/?#` で始まるリテラルのときだけ分割する |
| 木内クラスの構築 | 外部 import（`requests.sessions`）を末尾成分一致で木内の `sessions.py` と取り違え、基底（`pydantic.BaseModel`）を名前だけで木内の同名クラスと取り違えて `__init__` を実行した | false-alarm（到達しない resolved の効果） | import 名と木内モジュールの dotted 名が一致するか `.<import 名>` で終わるときだけ採る（`resolve_module_strict`）。基底もクラスのモジュールの import 表で厳密に引く |

**精度の代償（書いておく）:** 木内で非定数を `os.environ` に書き込む木では、すべての
環境変数の読み出しが opaque に戻る（`main()` で CLI 引数を書き込むだけの木も含む）。
モジュール水準の名前も、同名の局所変数がどこかの関数にあるだけで読まなくなる。
**どちらも resolved を opaque に戻す向きで、clean を作らない。**

**どうして最初に見落としたか:** D17 の修正は「解決できるのに opaque」を減らす向きの
変更で、較正対の受け入れテストも効果行の突き合わせも「消える」側を見ていた。
**opaque → resolved に変わった行が正しく resolved かは、突き合わせだけでは分からない**
（`diff_effects.py` は「slot 変化」として出すが、向きの判断は読む人に任せている）。
解決率を上げる変更は、敵対的レビューで「resolved にしてよい根拠」を 1 件ずつ崩しに
行く必要がある。

**改訂 3（2026-09-14、854f71b の 2 回目の敵対的レビューと run 3 による）: 改訂 2 の直し方が
効きすぎて効果行を落とし、残っていた false-clean もあった。** 3 観点（残る false-clean /
クラッシュ・性能・決定論 / 効きすぎ）の点検で 5 件を確認（棄却 0）。run 3 の突き合わせで
1 件を自分で見つけた。すべて修正より先に `tests/test_f0a_defects.py` の 10・11 節に固定した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| 変更されるモジュール水準のオブジェクト | 改訂 2 が `conn.row_factory = ...` / `session.headers.update(...)` を「書き込み」とみなして名前を読まなくしたので、受け手の型が消え **DB / NET の効果行ごと消えた** | false-clean（drop） | 再束縛（関数内の束縛・`global`・`m.NAME = ...`・`globals()` / `vars()` / `exec`）だけを「読まない」にし、**コンテナ / オブジェクトは常に型と主体を保ったまま確度を opaque に落とす**（`_opaque_deep`）。別名・補助関数経由の変更（`c = CONFIG; c[k] = ...`、`_put(d, k, v)`）もこれで resolved の定数にならない |
| 相対 import の基底 | import 表が相対の点を捨てるので、厳密化で `from .base import BaseTool` を同じパッケージの `base` と区別できず、基底の `__init__` の `self.conn` 経由の効果が消えた | false-clean（drop） | `SourceIndex.resolve_import_module`: 同じパッケージの `<pkg>.<name>` を先に、無ければ厳密な絶対解決。`from . import X` は親パッケージ |
| TRANSFER 表の実引数 | 変換が subject（受け手 / 第 0 引数）の主体しか採らず、`"ls {d}".format(d=d)` / `os.path.join("/data", name)` / `urljoin(base, url)` / `tpl.replace("H", host)` の MODEL を捨てた（改訂 2 以前からの欠陥。改訂 2 の `.format` の修正は**テストが弱くて効いていないのを見逃した**） | false-clean（MODEL → OP） | subject 以外の実引数の主体・確度・root を結果に入れる。非リテラルの実引数が混ざる文字列変換は形を捨てる（テンプレートのリテラルを host として切り出させない） |
| `os.environ` の別名 | `env = os.environ; env["K"] = cmd` を書き込みとして検出しなかった | false-clean | `os.environ` を名前に束縛する形を書き込みとみなす（複製 `dict(os.environ)` / `.copy()` / `{**os.environ}` は除く） |
| 再帰の走査 | 木全体を走査する再帰の NodeVisitor が、無関係なファイルの深い式（550 項の連結）で RecursionError を出し、**木 1 本の出力を全部落とした** | クラッシュ（全ユニットが消える） | 明示的なスタックで走査する（`_iter_nodes`） |
| 同名関数による解決の喪失（run 3 で発見） | `import spotify_api as sp; sp.get_followed_artists(...)` を末尾名だけで木全体から引いていたので、BOM を直して parse できるようになった別ファイルの同名関数と衝突し、NET 効果が 6 ユニットで消えた | false-clean（drop） | import 表で指したモジュール / 同じモジュールの定義を先に引く（`_pinned_function`）。末尾名の木全体検索はその後 |

**確認:** 較正対 A9 / A18 の効果行を 854f71b と突き合わせて消えた行 0、w-jitz10__spotify_mcp は
0 → 40 行。受け入れ（B3a 8/8、B3b 15/15、実装変異の生存 1/15、両側 7/7 で変化サイトは
evidence/w0 と同一）と決定論は不変。

**改訂 4（2026-09-14、8f24cbd の 3 回目の敵対的レビュー（確認 6・棄却 0）と run 3 / run 4 の
突き合わせによる）:** すべて修正より先に `tests/test_f0a_defects.py` 12・13 節と 11 節の追加に固定した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| `_pinned_function` の一意判定 | `lookup_function(name, module)` が索引の setdefault で最初の定義 1 件しか返さず、`@overload` のスタブ・再定義・if / else の def・import を上書きするローカル def で最初の定義に決め打ちした | false-clean（opaque → resolved） | 全定義で一意性を判定し、同名の入れ子 def・import・モジュール水準の代入があるときも pin しない |
| 入れ子ハンドラの素の名前 | `serve()` の中のハンドラが呼ぶ `prepare(...)` を、外側の `serve.prepare` ではなくモジュール直下の同名 def に決め打ちした | false-clean | 同じモジュールに同名の入れ子 def があれば pin しない |
| `"*"`（`exec` / `globals()` / `vars()`）で名前を読まない | 改訂 3 がモジュール全体の名前を読まない側に倒したので、オブジェクトの受け手の型が消え NET / DB の効果行が丸ごと消えた（2 観点が独立に指摘） | false-clean（drop、改訂 3 の退行） | 書き込みがある名前も「読まない」ではなく、**型と主体を保って確度を opaque に落とす** |
| val エンジンの再帰 | tool が読む 550 項の連結式で `_eval` の再帰が RecursionError を出し、木 1 本の出力を全部落とした（854f71b から残存） | クラッシュ | 左結合の `+` の連鎖を反復で畳む。runner がユニット単位で RecursionError を捕まえ `TRUNCATED(recursion)` として残す |
| 定数ホストの `.format` | 改訂 3 が非リテラル実引数の混ざる文字列の形を丸ごと捨てたので、`"https://api.github.com/repos/{}".format(x)` の host が MODEL になった（f 文字列では OP） | 精度の損失（誤警報） | テンプレートの最初のプレースホルダより前のリテラルを part として保つ |
| 同じ関数の 2 ユニット（run 3 で発見） | `@mcp.tool()` で登録した入れ子関数の名前をログの `tools=[...]` に並べる形で、同じ関数が `mcp` と `tools-list` の 2 ユニットになった | 過大計上 | tools-list の候補がすでにほかの規則のユニットならユニットにしない |

**確認:** 較正対の効果行は 8f24cbd と比べて消えた行 0。w-giak__mnemo-lite の 42 行の消失は
すべて重複していた `tools-list:` ユニットの行で、同じ qualname / 経路 / サイトの `mcp:` ユニットの
行が残っていることを機械的に確かめた。

**記録する限界（新たに受け入れたもの）:** `os.environ` を関数に渡してその中で書き換える形、
`setattr(sys.modules[...], ...)` による再束縛は見ない。モジュール水準のコンテナ / オブジェクトは
書き込みの有無にかかわらず opaque になる（resolved → opaque の向きで clean を作らない）。
相対 import の判定は「同じパッケージに同名モジュールがあればそれ」で、絶対 import が
同名の兄弟モジュールと衝突する木では誤りうる。

**改訂 5（2026-09-14、ea35672 の 4 回目の敵対的レビュー（確認 6・棄却 0。6 件すべて false-clean /
効果行の消失の向き）による）:** 6 件は下の 4 系統に重なる（URL 分割の件は 3 観点が独立に指摘した）。
**D19 の凍結条件を満たさない**ので、D19(3) に従い、すべて修正より先に `tests/test_f0a_defects.py`
14 節に固定し（xfail 17 件。「連結で作った Str」の形はレビューの指摘には無く、再現の途中で自分で
見つけた同じ系統の形）、直した差分だけを 5 回目のレビューにかける。**5 回目が最後の繰り返しである。**

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| opaque の値の定数を URL 分割がリテラルとして読む | 改訂 4 の `_opaque_deep` が Atom の定数と Str の part の確度を残し、`_split_url` がその定数から url.scheme / url.host = OP / resolved を作った。`global` / `exec(..., globals())` / 読む側の再束縛で MODEL が書き換えるベース URL の host が resolved の定数になり、行の確度も resolved になった | false-clean（opaque → resolved。"*" 形と import 形は MODEL → OP も。改訂 4 の退行） | `Value.const` / `is_literal()` は**確度が resolved の値の定数しか返さない**。`_opaque_deep` は Str の part にも opaque を合流する（`_make_str` が part を平らに展開するので、外側だけでは足りない） |
| `shell=` / `open` の mode | `_exec_mode` / `_mode_is_write` が再束縛される名前の opaque な定数（False / "r"）をリテラルとして読み、shell=True 側の SPAWN 行と FS_WRITE 行が消えた | 効果行の消失（改訂 4 の退行） | 同上（定数を読めなくなるので「判定できない」側に回り、両方の行を出す） |
| 差し替えられる dict の URL テンプレート | tool が `ENDPOINTS[name] = tmpl` で差し替える要素（opaque）の `.format(q)` で、改訂 4 のテンプレート先頭の part が確度を捨てて host = OP / resolved を作った。`ENDPOINTS[k] + q` の形は 8f24cbd の時点から同じ | false-clean（`.format` は改訂 4 の退行、`+` は既存） | 同上 |
| 同名の定義による効果行の消失 | `_pinned_function` がモジュール内の同名の def を、呼び出し位置から見えない入れ子 def（別の関数の中）まで数えて pin をやめ、末尾名の木全体検索も 2 候補で降りなかった。if / else の 2 つの def、import した名前と読む側の無関係な入れ子 def、`helpers.run_command(...)` と helper 側の入れ子 def でも同じ。helper の中の SPAWN 行が丸ごと消えた | 効果行の消失（改訂 4 の退行） | **呼び出し位置から見える定義だけを数える**（`_visible_defs`: モジュール直下の def と、素の名前の呼び出しなら呼び出し行を囲む関数の中の def）。見える定義が複数ある、または同じ名前が import / 代入でも束縛されるときは、**全候補へ降りて戻り値を join し、行と戻り値を opaque にする**（1 つを選ぶと他方の行が消え、降りなければ全部消える） |

**警報の向きの判定は、確度に関係なく形の定数を読む:** `_is_policy_path`（方針ファイルへの書き込み
`write_policy`）と `sep.join` の受け手の型判定は `shape.const` を読む。`Value.const` の変更で
再束縛されうる方針ファイルのパスへの書き込みを見落とさないため。

**記録する限界（新たに受け入れたもの）:**
- モジュール水準のリスト / dict の要素（改訂 4 から、書き込みの有無にかかわらず opaque）の定数も
  リテラルとして読まなくなる。`CMD = ["ls", "-la"]` の argv0 は副 kind `SPAWN_CONST_ARGV` にならない
  （resolved → opaque の向き。精度の損失）。
  **訂正（5 回目のレビューによる）:** ここには当初「pipe の argv0 の判定にも使わない（精度の損失）」とも
  書いたが、**向きの判断が誤りだった。** `_pipe` は判定できないときに FS_WRITE の側だけを出すので、
  argv0 / shell が opaque の値だと pipe 書き込みの **EXEC(code_text) 行が消える**（効果行の消失）。
  D19 の「結果」の既知の欠陥 K1。
- 見える同名の定義が複数ある呼び出しは、全候補の効果を opaque で出す（どれが効くかを決めない。
  使われない分岐の行は誤警報になりうる）。
- 呼び出し関数自身の局所 def と同名の呼び出し（`func.id in scope.local_bindings`）は、従来どおり
  pin を引かず末尾名の木全体検索に回る。

**確認（修正の commit の時点）:** テスト 177 件が `.venv`（3.10）と `.venv312`（3.12）の両方で通る
（14 節の 17 件は、未修正の 56f61c5 / 170a7b2 を worktree に取り出して走らせると xfail）。
受け入れ B3a 8/8、B3b 15/15、実装変異の生存 1/15、決定論（A1__fixed / A9__vuln で 3 回バイト一致）は
不変。両側 7/7 で、**変化した経路・判定・verdict-clearing は `evidence/w0/two_sided.json` と同一**。
違うのは不変の経路の数 `n_unchanged_paths` だけで、3 対で増えた（対 1: 10 → 12、対 5: 13 → 14、
対 6: 23 → 55）。**これは改訂 5 によるものではない**: 170a7b2 を `git archive` で取り出して同じ手続きで
走らせると（`authgap` がその展開先から import されることを確かめた）すでに 12 / 14 / 55 で、
170a7b2 と 150e06a の出力 JSON の違いは木の絶対パス（`vuln_root` / `fixed_root`）だけだった。
w0 の後、改訂 2〜4 のどこで増えたかは切り分けていない（不明。変化した経路と判定は同一なので、
T1 の主指標には効かない）。
較正対 14 木の `diff_effects.py --before 170a7b2 --after 150e06a`: 消えた行 0・増えた行 0。slot 変化は
A9 の 86 件（両側 43 件ずつ、`BasicSkillMutator` の経路）で、**すべて行の確度の理由が
`opaque(unresolved)` → `opaque(depth+unresolved)` になっただけ**（主体・確度の種類の変化 0）。
野外: run 6（150e06a、Python 3.12）の `units.jsonl` / `trees.jsonl` は run 5 と**バイト一致**
（改訂 5 が直した形は標本の 98 木に無かった。関門の数字も区間も run 5 と同じ）。

**フレームの誤り（直す。結果とは独立の事実誤認）:** `APP_FRAME` の
`OpenManus/OpenManus` は RL 用の openmanus_rl で、選定根拠に書いた「§2.6 の負例
F5/F6/F7 の出所」（FoundationAgents 版 `app/tool/python_execute.py` ほか）ではない。
選定根拠が偽なので、根拠どおりの repo に置き換える。**置き換えは結果を見て選び
直したのではなく、名前の取り違えの訂正である**が、run 1 には誤った repo が入って
いることを run 1 の表の注記に残す。

**訂正後の `FoundationAgents/OpenManus`（3309bf4e）もユニット 0 件である。** ツールは
`class PythonExecute(BaseTool)` の `async def execute(...)` 形で、Def 2 の R2 カタログ
（`@mcp.tool`、低レベル MCP 2 形、`@tool`、`BaseTool._run`、CrewAI `_run`、
`@function_tool`、`@kernel_function`、agno、gptme `ToolSpec`）に `execute` は無い。
§2.6 の F5–F8 は **val エンジンの受け入れ fixture**（関数本体の値の解析）であって、
OpenManus を R2 の入口として認識することを要求していない。**上の「直さない 3」に
従いカタログは広げず、アプリ母集団のカタログ外の形の取りこぼしとして数える。**
（F1–F10 の fixture `fixtures/val/expected.json` 自体はまだ作っていない。
`docs/open_questions.md` の作業一覧に置いた。）

---

## D40（2026-09-22）HintLint（R1）を一次資料で確認し、O19 の判断を (a) にする

**きっかけ**: O19 の 3 本のうち R1 だけが未確認で、しかも**主軸そのものに最も近い**。
`complira/hintlint`（`5a51f2a4`、2026-09-11、JavaScript / Node、8,626 行）を clone して
ソースを読み、母集団 v2 の 87 木すべてで実際に走らせた
（`scripts/hintlint_compare.py` → `evidence/hintlint_run1/summary.json`）。
詳細と再現手順は `docs/related_work.md` の R1 節。

### 一次確認した事実（**ページの記載ではなくソースと実行結果**）

1. **Python 経路は AST ではなく行単位の正規表現。** `src/extractors/python.js` の
   `startsToolDecorator = /@(?:\w+\.)?tool(?:\s*\(|\s*$)/`。`collectFunctionText` は
   次の `def` / `@tool` までを集めるので、判定に使うテキストは**そのツール関数の本体だけ**。
2. **Python 側に到達解析は無い。** `src/evidence/typescript-reachability.js` に
   `python` の出現が 0 件。**呼び出しを追わない。**
3. sink は 10 個の `SINK_RULES`。確度の語彙は `source-backed` / `needs-review` の 2 語で、
   **未解決を表す語が無い**。`handlers_resolved` は「デコレータから本体を取り出せたか」の数で、
   値や効果が解決できたかではない（`src/index.js:41`）。

### 実測（母集団 v2 の 87 木、`evidence/scan_v2_run4` と対比）

* HintLint: ツール 13,083 / finding 81（readOnly + destructive の**比較可 65**）。
* AuthGap: ユニット 2,231 / CONTRADICTION 79。
* **木の重なりはほぼ無い**（両方 2、HintLint だけ 5、AuthGap だけ 14）。

**比較可 65 件のうち 61 件は `declared_annotations` が `{}`、つまり宣言が無いツールである。**
HintLint の `DESTRUCTIVE-001` は `destructiveHint` が**無い**ことで発火する。AuthGap の
CONTRADICTION は明示の宣言 D に**反する**ことを要求する。**したがって 61 件は同じ現象を
数えていない。真に比較できるのは 4 件だけ。**

### その 4 件で AuthGap は 1 勝 3 敗。**負けの 3 件の原因を一次確認した**

| ツール | AuthGap の結果 | 原因 |
|---|---|---|
| `winremote-mcp` / `PlaySound` | **一致**（効果は AuthGap の方が多い） | — |
| `godsaeng-salon` / `check_reminders` | CONTRADICTION 出ず | **設計差。**`verdict.py` の CONTRADICTION は `eff.kind in ("EXEC","SPAWN","FS_WRITE")` に限る（`DESTRUCTIVE_KINDS`、D32）。`readOnlyHint:true` + DB 書き込みは対象外 |
| `cohort` / `internal_web_fetch` | 効果 0 件 | **誤 clear（false-clean）。**`Path(...).parent` / `.parents[n]` が受け手の Path 形を落とし、`pathlib.Path.mkdir` の sink 行に当たらない。**`opaque_reasons` に `receiver` は残るが行が 1 本も出ない** |
| `mcparmory/registry` / `delete_snapshot_by_delete_key` | ユニット無し | **`AST_NODE_CAP`（20,000）の打ち切り。**`servers/grafana/server.py` は 54,192 ノード。`truncations` に記録あり |

**誤りの向きを明記する。** 3 件目は**誤 clear 方向**（危険を見落とす側）である。
最小再現で切り分けた: `Path("/tmp")/"x"` と `Path("/tmp").resolve()` は sink に当たり、
**`Path("/tmp/a/b").parent` だけが当たらない**（`authgap/val/engine.py` の `_ev_Attribute` が
Path 形の属性を `Unknown()` に落とす）。`docs/open_questions.md` O22 に置き、別途直す。
**この commit では解析器を触っていない。**

### 段数の分布（HintLint が構造上届かない範囲）

AuthGap の CONTRADICTION 効果 130 件の中間フレーム数（`witness_chain` の長さ）:
0 段 **4 件（3.1%）** / 1 段 27 / 2 段 39 / 3 段 57 / 4 段 3。
API 種で HintLint の正規表現が当たりうるのは 46 件（35.4%）だが、
**0 段 かつ 当たりうるのは 3 件（2.3%）だけ。**

`mcparmory/registry` の 48 件を目視すると、当たっている sink は
`DeleteCustomFieldActivityCustomFieldIdRequest(` のような **pydantic のリクエスト模型の
コンストラクタ**であり、実際の削除は `_execute_tool_request(method="DELETE", ...)`
（`servers/close/server.py:810` のモジュール水準の補助関数、**ツール本体の外**）にある。
**判定は正しいが、根拠として挙げた行は削除ではない。**

### 公平性のための自己申告（AuthGap 側の不利ではなく、**AuthGap 側の欠測**）

* `david-li0406/meta-skill-evloving` は AuthGap が 180 秒の tree budget で打ち切られ
  **ユニット 0 件**（`budget_skipped: 716`、511.6 秒）。HintLint は比較可 12 件。
  **この木は比較として成立していない。**
* 母集団 v2 の `@tool` 系デコレータ 12,713 個のうち **9,816 個（77.2%）が `AST_NODE_CAP` で
  切られたファイルの中**にある。ただし**その 9,524 個が `mcparmory/registry` 1 本**で、
  この 1 木を除くと 292 / 2,543 = **11.5%**。分母の扱いは O21 に置いた。

### 決定

1. **O19 の判断は (a)「測定研究として立て直す」。** (c)「変えない」ではない。
   R1 が同じ現象を先に触っているので「初めて照合した」とは書けない。
   書けるのは**母集団の定義・事前登録・未解決の率の報告**であり、それは (a) の内容である。
2. **検出力で勝ったという主張はしない。** 比較可能な 4 件で 1 勝 3 敗であり、
   この標本で優劣は言えない。R1 節にそう書いた。
3. **比較の限界を 3 つ本文の限界節に持つ**（TS/JS 経路を見ていない / 入口を揃えていない /
   比較できた事例が 4 件しかない）。
4. **HintLint の論文の有無は「確かめられなかった」と書く。**「無い」とは書かない
   （この環境から検索できない。CLAUDE.md 規則 4）。

**これは先行研究の記録であって、解析器・語彙・事前登録の変更ではない。**
`git diff authgap/` は空である。

---

## D41（2026-09-22）矛盾関係を表として定義する（`docs/contradiction_matrix.md`）。**判定器より先に書く**

**きっかけ（学生の指摘）**: 「全部を網羅することはできないのは知っている。しかし
**宣言のパターンには限りがある**。それなら、宣言のパターンをもとに、実装がどう食い違って
いれば危険かを網羅できるのでは？」

**この指摘は正しい。** 一次資料で確認した:

* MCP の `ToolAnnotations` が持つ挙動の主張は **4 つだけ**（`title` は表示名）。
* **2025-06-18 / 2025-11-25 / draft の 3 版で 1 文字も違わない**
  （`schema/<版>/schema.ts` を取得して比較）。
* **制約を作るのは 4 つの値だけ**（`readOnlyHint:true` / `destructiveHint:false` /
  `openWorldHint:false` / `idempotentHint:true`）。
  仕様の既定値は 4 つとも許容側なので、**不在に既定値を補っても上界は動かない**。
  `dparse.py` が既定値補完を禁じているのは保守性ではなく**仕様からの帰結**であり、
  この文は本文の設計節に書ける（今回初めて一次資料で裏づけた）。

**したがって「定義の網羅」は達成可能で、検証可能である。** 主張を 2 層に分ける:

| 層 | 主張 | 崩れ方 |
|---|---|---|
| 定義 | MCP 仕様の 4 注釈すべてについて矛盾関係を定義した | 仕様が 5 つ目の注釈を足したときだけ |
| 検出 | その定義を静的に判定した率を報告する | 崩れない（測定結果） |

**HintLint（R1）との差がここで言語化できる。** 向こうは 10 個の正規表現を持つが
**仕様を持たない**ので、「なぜその 10 個か」「他に何があるか」に答えられない（D40）。

### 表を書いた結果、当初の見立てが 3 つとも外れた

**この commit の主要な成果はこれである。**

| 当初（実装前に立てた見積もり） | 表を埋めた結果 |
|---|---|
| 「上界の外の効果が 205 件あり、うち 127 件は確実な見逃し」 | **確実な見逃しは 0 件。**すべて「まだ決めていないマス」だった |
| 「`contradiction()` が `dk.covers(kind)` を使えば直る」 | **直らない。**`kind` 粒度で使うと `readOnlyHint:true` + `DB_READ` の **72 件が偽陽性**になる。上界は sub_kind 粒度で書く必要がある |
| 「網羅できていないことが問題」 | **問題は「不明を黙って落としている」833 件の方。**規則 4 違反で、向きは**誤 clear** |

**誤りの向きを明記する。** 私（この作業）は**見逃しの件数を過大に見積もっていた**。
効果の `kind` だけを見て数えたためで、SQL の中身まで見ると:

* `readOnlyHint:true` + `DB_WRITE` の **54 件はすべて `PRAGMA`**
  （`journal_mode=WAL` 52 / `busy_timeout` 2）。接続設定であってデータの変更ではない。
  **1 つのプロジェクトの同じ行が繰り返し数えられているだけ。**
* `destructiveHint:false` + `DB_WRITE` の **9 件はすべて `INSERT`**。
  追記なので**宣言内が正しく、現行の挙動が正しい**。

**表を先に書かずに実装を触っていたら、`upper` をそのまま使って偽陽性を 72 件作り、
`PRAGMA` を 101 件警告していた。** CLAUDE.md 規則 5（期待値は採点器より先に）の
実例として記録する。

### 表を書く作業そのものが見つけた解析器のバグ 2 件（**直していない**）

`authgap/effects.py: _sub_kind` の DB 分類。**`SUB_KINDS` の語彙（月 3 凍結）には触れない。**

* **B1**: `text.strip().split(" ", 1)[0]` が `" "` だけで切るので、改行で始まる複数行 SQL が
  `"SELECT\n"` になり `DB_WRITE` に落ちる。母集団 v2 で 2 件。**向きは誤警報。**
* **B2**: 読み取り語の一覧に無ければ `DB_WRITE` なので、`PRAGMA` / `BEGIN` / `COMMIT` /
  `ROLLBACK` がデータの書き込みと同じ sub_kind になる（`PRAGMA` 101 / ほか 4）。
  **O23 #1 を決める前にこれを直す。** 直さずに `readOnlyHint:true` × `DB_WRITE` を
  矛盾にすると 101 件の誤警報になる。

### 決定

1. **`docs/contradiction_matrix.md` を仕様として先にコミットする。**
   この commit では**解析器を一切触らない**（`git diff authgap/` は空）。
2. **仕様の文言から一意に決まらない 5 マスは「決めていない」と書き、報告しない。**
   → `docs/open_questions.md` O23。**黙ってどちらかに倒さない**（規則 4）。
3. **実装の順序は「矛盾を増やす」より「不明を報告する」が先**
   （833 件、向きは誤 clear）。表の §7 に順序を書いた。
4. 実装に入るときは**変更の前後で件数を両方出し**、
   `docs/preregistration.md` に逸脱として記録する。

**本文に書く一文**: 「表が完全なのは**定義**であって**検出**ではない。」

---

## D42（2026-09-22）D41 の表が見つけた `_sub_kind` の問題 3 件のうち、B1 だけを直す

**D41 で矛盾関係の表を書いたとき、`authgap/effects.py: _sub_kind` の DB 分類に
問題が 3 件見つかった。3 件とも向きが違うので、扱いを分ける。**

### B1（直した）— 改行で始まる `SELECT` が `DB_WRITE` になる

```python
head = text.strip().split(" ", 1)[0].upper()      # 旧
parts = text.split(None, 1); head = parts[0].upper()   # 新
```

`" "` だけで切るので `"\n        SELECT\n            id::text, ..."` は
`strip()` 後も `head == "SELECT\n"` になり、読み取り語の一覧に当たらず `DB_WRITE` に
落ちていた。母集団 v2（`evidence/scan_v2_run4`）で **2 件**。どちらも
`v2-deploylabs429__agent-langchain-fastapi` の複数行 SQL で、**宣言なしのユニットなので
verdict には出ていない**（`sub_kind` は現在どの verdict にも使われていない。
`Leak` の等級づけ用に定義されたもので、D36 で等級づけを降ろした）。

**誤りの向きは誤警報（false-positive）。** 読み取りを書き込みとして記録していた。

**併せて、空白だけの SQL を `DB_WRITE` ではなく `None`（不明）にした。**
旧実装は `"".strip().split(" ",1)[0] == ""` から `DB_WRITE` にしていた。
**規則 4（解決できなかったものは不明として記録する。黙って安全側に倒さない）に反する。**
母集団 v2 に該当 0 件なので観測は変わらない。

### B2（直さない）— `DB_WRITE` は「データを変更する」の意味ではない

`_sub_kind` の `DB_WRITE` の定義は「**読み取り語で始まらない**」であり、
`PRAGMA`（接続設定）も `BEGIN` / `COMMIT` / `ROLLBACK`（トランザクション制御）も入る。
母集団 v2 で `PRAGMA` 101 / `COMMIT` 2 / `BEGIN` 1 / `ROLLBACK` 1 = **105 件**。

**元の用途では正しい。** 仕様書 §297 が `sub_kind` を要求した理由は
「ゲートが読み経路を覆うかを kind 粒度で比べると正当な読み取りが全て `Leak` に落ちる」で、
そこでは `PRAGMA` が読み取りでないのは正しい。

**したがって `SUB_KINDS`（月 3 の sink 語彙凍結の対象）は変えない。**
代わりに `_sub_kind` に注記を入れ、`docs/contradiction_matrix.md` §5 と §7 に
**「表を実装するとき `DB_WRITE` をそのまま『変更』として使ってはならない。
使うと `PRAGMA` 105 件が誤警報になる」**と書いた。

**当初 D41 のコミットでは「B2 はバグなので直す」と書いたが、これは誤りだった。**
`_sub_kind` の用途を確かめずに「名前が意味と合っていない」ことをバグと呼んでいた。
**名前と用途の乖離であって、実装の誤りではない。** D41 の記述をこの決定で訂正する。

### B3（直さない。記録する）— `WITH` を無条件に読み取りとするのは潜在的な誤 clear

`WITH x AS (...) INSERT INTO t ...` は書き込みだが、読み取り語の一覧に `WITH` が
あるので `DB_READ` になる。**向きは誤 clear。**

**母集団 v2 に `WITH` で始まる SQL は 0 件。**「無い」ではなく「この標本では 0 件」。
条件つきにすると文字列リテラルや列名に含まれる語で誤警報を作るので、
**憶測で直さず既知の限界として記録する**（`docs/open_questions.md` O24）。
`DB_WRITE` を矛盾判定に使う段階（O23 #1）で決める。

### 確認（CLAUDE.md の手続き）

* **`scripts/diff_effects.py --before 3d4d0a1` を較正対 14 木で実行 →
  14 木すべて「消えた 0 / 増えた 0 / slot 変化 0」。**
  **ただしこれは修正が効いたことの証拠にならない。** 較正対に複数行 SQL の DB 効果が
  無いので、そもそもこの経路を通っていない。**効いたことは
  `tests/test_db_sub_kind.py` の回帰テストで確かめた**（B1 の 9 例が `DB_READ` になる。
  修正前の `split(" ", 1)` だと改行で始まる 6 例が `DB_WRITE` になる）。
* `scripts/check_gates.py`: **B3a 8/8、B3b 15/15**（不変）。
* `pytest tests/ -q`: **全通過**（xfail は既知のまま、失敗 0）。
* `scripts/mutation_test.py`: **生存 1/15**（受け入れ条件 ≤ 2。生存は
  `no_finally_copies` で D35 と同じ。不変）。
* `ruff check .`: 通過。

### 回帰テストで「直さないと決めたこと」も固定した

`tests/test_db_sub_kind.py` は B1 の期待値だけでなく、**B2 と B3 を「直さないと決めた」
ことも固定している**。`PRAGMA` / `BEGIN` / `COMMIT` / `ROLLBACK` が `DB_WRITE` のままで
あること、`WITH x AS (...) INSERT INTO ...` が `DB_READ` になることをテストに書いた。

**期待どおりに間違っていることをテストに書くのは、正しさの主張ではない。**
後から黙って挙動が変わるのを防ぐためであり、B3 のテストには
「**これは既知の誤り（誤 clear 方向）であって期待する挙動ではない**」と明記した。
* **母集団 v2 の再スキャンはしていない。** 変わるのは manifest の `sub_kind` 欄 2 件だけで、
  `sub_kind` はどの verdict にも使われていないため、`scan_v2_run4` の判定の数字
  （CONTRADICTION 130 効果ほか）は変わらない。**表の件数の出典は run4 のままでよい。**
  次に full scan を取り直すときに `sub_kind` の 2 件が直る。
