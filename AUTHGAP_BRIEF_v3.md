# AuthGap — プロジェクト引き継ぎ資料（新規セッションの先頭に貼る）

> **新規プロジェクトの立ち上げ資料**。読み手は文脈を持たない新しいセッションを想定する。
> 前身プロジェクト（dispatch-taint）の成果物は**論文に書かない**。設計判断の前提としてのみ §1 に要約し、必要な事実は新規に測り直す（§6 F0c）。
> 作成 2026-09-08。第 3 版。第 2 版に対し 7 系統の強化と、各々への 2 系統の敵対的検証（正味便益・正確性）を通した。
> **§9 の未検証リストを第 1 週に必ず実施すること。** CVE の修正コミットは脆弱性 DB の記載を信用しない（§9-1。第 3 版で誤記載の実例を 4 件確定した）。

## 変更履歴 v3 → v3.1（新規セッション模擬の指摘 24 件を反映）

blocker 5 件: 前測スクリプトを `docs/authgap_staging/premeasure/` に救出しパスを明記（元は消えうる一時ディレクトリ）／交差行の定義を verdict 集合の比較に修正（旧定義は Def 7 の下で充足不能だった）／Def 6「層ごとに独立」と Def 7 の矛盾を解消し D_kind は INJECT を被覆しないと明記／D_kind の対象フィールドを 3 つに限定し `r_kind` の分子を再定義／F0c を A5 時点と B1 後の 2 回に分割。

major 12 件: validator 形状語彙を §6 F0a の 11 語に一本化（3 通りの語彙を統一し `Path.resolve` と `relative_to` の欠落を修正）／opaque を 8 分類に拡張し val 側とゲート側の語彙を分離／witness を欠いていた 4 語に追加し `self_granted` を格下げ属性として分離／執行表を B5 から B3 へ移動（strong-enum が B3b の分母に入るため）／§7.1 の 18.75 を 19.5 に訂正／§7.6 に第 3 週（D16–D20）を追加し A3 の学生週超過を解消／§9 を第 0〜3 週に広げ 13 項目に日を割り当て／held-out G16–G20 の出所を T1 修正版から F0a コーパスの無作為抽出へ変更（前者は設計汚染源）／`r_D` を和から和集合へ／`in_tree_resolution_ratio` と `dispatch_resolution_ratio` を別名に分離し opaque 関門から `remote` を除外／opaque 閾値 40% を固定し動かすのは分母定義のみに限定／母集団取得手段を 4 案の優先順で確定し重複除去単位を GitHub リポジトリに固定。

minor 7 件: 較正表の行数を 17 に統一／B3a の mutant (5) を下向き走査の語彙に書き直し (6)(7) の期待値を追加／脈拍 3 対を採点集合 8 対からに限定／§10 A5 行の条件と対処の対応を明示／非 DB `.execute()` の機械判定規則を追加／用語表の slot 参照を Def 3 に訂正／go/no-go 表の 4 セル行を表外へ。

---

## 変更履歴 v2 → v3

1. **枠組みの変更（学生決定、2026-09-08）**。新規性は主目的ではない。先行研究との重なりは許容し、貢献は**同一コーパス上での精度差**として述べる。§1.5 は新規性の弁護から**位置づけと比較の表**に変わり、各行の「反証条件」は「比較結果の報告様式」に変わった。頭出しの主張は**修正版側（fixed side）の精度**である。
2. **T1 の較正候補を 5 件（検証 0 件）から主較正 17 行 + B 群 8 行 + S 群 5 行に拡張**し、主較正の修正コミット SHA と親をクローン上で `git log -S` / `git show` により自分で確定した（SHA・diff 内容は一次確認済み、CVE / GHSA 番号と公開日は二次情報）。脆弱性 DB の fix commit 欄の誤りを 4 件、修正の存在しない CVE を 2 件確定。**選択ハイジャックに実 CVE 対が 1 件存在する**ことが判明（PraisonAI CVE-2026-44339）。ただし脆弱側の verdict は `GAP_SELECT` ではなく `UNKNOWN(opaque)`。3 対（A12/A16/A17）は Def 5 で等級が動かないため算入しない。**算入可能 11 対 / 5 プロジェクト。**
3. **Def 5 を実データで改訂**: weak 理由に `no_containment` / `no_symlink_resolution` / `prefix_no_boundary` / `fail_open` / `denylist_enum` / `regex_no_canon` / `validate_then_fetch` / `self_granted` を追加。strong-path の正規化子を 2 系統（symlink 解決子と字句正規化子）に分け、包含述語に `startswith(root + os.sep)` を、被演算子に `os.getcwd()` を追加。`strong-enum` を新設、`strong-eval` は**任意**（切り詰め順序の先頭）。
4. **Def 6 の D を 4 層に分解**（D_kind / D_dom / D_op / D_prev）。60 MCP サーバ 3155 エントリ・19 ツールパッケージ 1352 エントリの前測で、annotation 明示率と値域制約率を実測した。**D_dom は前測で母集団 0 のため定義のみ置き、実装は F0a 条件付き。** §10 の D 規則は母集団別・層別に分岐する形に変えた。
5. **支配判定（§2.5）と val エンジン（§2.6）を仕様化**。前身が実データで発火しなかった原因は「支配が無い」ではなく「判定前に保守フォールバックへ落ちる」ことだと前身コードの実行で確定。4 つの構造変更（下向き探索・CFG 支配・3 値・ゲート要約）と、受け入れ集合 G1–G15 を定義した。**支配は「評価される」ではなく「拒否側から効果に到達しない」で定義する。**
6. **選択セルは据え置き**。被覆漏れ（`Leak`）は verdict ではなく manifest 属性として導入し、格上げ条件を事前登録した。§10 の traced 率関門と SELECT 格下げ条項は撤回しない。
7. **§7 の合計が誤っていた**（表記 45、行の和は 47）。会計単位を「建設週」から「学生週」に変え、**34.0 学生週**の表に再構成した。算術は §7.3 に全て書いた。

---

## 0. 一行で

**エージェントのコードは、それ自体が暗黙の権限システムである。** AuthGap は、コードがモデルに実際に渡している権限（実効権限 M）を静的に推論し、宣言された権限（D）または明示ベースライン P0 を超える箇所を報告する。

**修論が守る一文**:

> Python の LLM エージェント（アプリ、ツールパッケージ、MCP サーバ）について、インストール前のパッケージ木のみを入力とする（venv も型環境も構築しない）静的解析で、**LLM を判定入力に使わず決定的に**、各危険効果の「発生を誰が決めるか（trig）」「各制御位置の値を誰が決めるか（val）」「どのゲートが**どの等級で**要求主体を引き上げるか（gate）」の三座標を推論し、実効権限 M が宣言権限 D を超える箇所を報告する。**同じ問題に取り組む先行手法（§1.5）と同一のコーパス上で、脆弱版・修正版の両側で報告タプルの変化を採点し、精度差を対ごとに報告する。** クラス 1a と 2 は公開 advisory の両側対で検証し、クラス 1b は原則として脆弱側のみを評価して両側率には数えない（ゲート導入型の修正がある対のみ両側）。選択ハイジャック（GAP_SELECT）は両側対が 1 件（PraisonAI CVE-2026-44339、脆弱側 verdict は `UNKNOWN(opaque)`）しか無いため、fixture・mutant・3 ケーススタディによる構造的評価を主とし、当該 1 対を補助として添える。

**頭出しの主張（head-to-head の測定量）**:

> 先行検出器は**脆弱版**を報告する（それが CVE を得る条件である）。しかし sanitizer の**存在**を見て**妥当性**を見ないので、**修正版を clear できない**か、脆弱版と修正版で同じ行を出す。AuthGap は連結経路上で validator を等級付ける（strong-path / strong-token / strong-enum / weak(reason)）ので、**両側タプル変化**を判定できる。したがって head-to-head の測定量は「同一の対集合に対する**両側通過率**」であり、脆弱版側の検出率ではない。
>
> **脆弱版側で先行手法と並び、修正版側で上回る結果は成功である。** これを明示的に事前登録する。逆に、ある先行手法が修正版側も clear できると分かった場合は**そう書いて引き分けを報告する**（§1.5 の各行の「比較結果の報告様式」）。

**残る新規性の主張**（本論文はこれらに依存しない。事実として述べるだけ）: 連結経路上の支配等級づけ、二重束（ラベル束 P と要求束 P^op）、D_kind / D_dom / D_op / D_prev の 4 層照合。

**null 時の代替主張**（F0 の語彙だけで書く。val エンジンとゲート採点器を必要としない）:

> Python の LLM 呼び出し可能ツール N 件について、独立ラベルと κ 付きで、(a) ユニットごとの危険効果 kind の真偽値と in-tree 解決率、(b) 構文的 validator 形状（語彙は §6 F0a が唯一の定義点。11 語）の分布と config atom の既定値、(c) 宣言（MCP annotations / ホスト承認リスト）の有無と矛盾率を測定し、CVE 対 n 件を対ごとに baseline と並べて報告する。

位置別の精度、opaque 率、mutant 判別率は**成功時の主張であり代替主張には含めない**。ゲート採点が月 6 の閾値を外した場合、mutant 判別率は「閾値」ではなく「測定値」として報告する。

---

## 1. 設計判断の背景（論文には書かない。§6 F0c で新規に測り直す）

前身プロジェクトは「呼び出し側の動的ディスパッチの壁を書き下して、無改変の Pysa に越えさせる」設計だった。実測の結果、4 条件の連言が実アプリで成立しないと分かった。

| 条件 | 破綻 |
|---|---|
| エンジンが壁を記録する | pyre の環境構築とコストで多数が解析に到達しない |
| stub 化された framework を越えて選択キーに LLM taint が届く | SDK が型消去された stub 境界で source が切れる |
| 候補本体が sink に到達する | ツール実行が別プロセスや HTTP の向こう側にある |
| ガードが無い | 無ガードのシェル実行は多くのアプリで**仕様**であり、報告しても「意図どおり」と返される |

AuthGap は 4 条件のうち 3 つを構造的に外す。source をツール引数と LLM 出力に置くので stub 境界を越える必要がない。解析開始点が callee 内なので壁も型環境も要らない。「ガードが無い」ではなく「宣言または P0 を超える」を判定するので仕様どおりのツールは分離される。

**外れない 1 条件**は「本体が別プロセスや HTTP の向こう」である。これは `remote` / `UNKNOWN` ラベルとして残る。**測定点は `remote` 率の報告値であって関門ではない**（下記の定義を参照）。

**2 つの解決率を区別する（同じ語を 2 つの量に使わない）**:
- **`in_tree_resolution_ratio` := `resolution.resolved / (resolved + opaque + remote)`**（**効果サイト**の解決率。§10 の A5 関門はこれ）。
- **`dispatch_resolution_ratio`**（`traced_ratio` と `registry_resolution_ratio` の 2 値。§6 F0c(i) はこれ）。
- **含意**: `in_tree_resolution_ratio ≥ 50%` と `opaque ≤ 40%` を同一分母で同時に課すと `remote ≤ 10%` を暗黙に要求してしまう。remote はこれより大きい見込みなので、**opaque の関門は `remote` を分母から除いた `opaque / (resolved + opaque)` で判定する**。`remote` 率は関門にせず報告値とする。

**この 4 条件は論文には書かない。** したがって callee 側への反転の正当化は、論文内では F0c の測定結果と先行研究で行う。§8 の指導教員合意でこの点を明示すること。

---

## 1.5 位置づけと比較（一次資料で検証済み。第 1 週は追認と更新のみ）

**本節は新規性の弁護ではない。** 学生の決定により、先行研究との重なりは許容する。本節の役割は 3 つ — (i) 比較対象を名指しすること、(ii) コーパスと ground truth を再利用できる先を特定すること、(iii) AuthGap がどの軸で**より正確**であると見込むかを軸ごとに書き、比較結果の報告様式を先に決めること。

**検証強度**: **◎** = 本文（PDF 抽出テキスト）を自分で読み原文を確認。**◎'** = 本文 HTML に対する自動要約に依拠し原文は未読。**○** = arXiv abstract / 公式ドキュメント / README を読んだ。**△** = 他論文の related work 経由（二次）。**◎' は ◎ ではない。** 本研究は「LLM を verdict 入力に使わない」ことを主張の一部にしているので、その主張を支える related work 自体を LLM 要約に依拠したまま提出しない。実例として mcp-sec-audit の最初の自動要約は「AST パターンマッチと意味的データフロー解析」と述べたが、PDF 原文は "TOML-driven keyword/regex matching" であり、要約が本節の判断を左右する方向に誤っていた。

**数値の出所規則**: 本節の表に現れる数値は全て引用元論文の自己申告値であり、本研究の測定ではない。本研究の閾値（§6・§10）と同じ土俵の量でもないので**比較の文脈で並べて書かない**（§9-5 の規則を related work にも適用）。各数値は `docs/related_work.md` に出所行（PDF の節番号または HTML の節）と `source_of_number`（paper / repo / both）とともに記録する。プレプリントの数値は改稿で変わるため版番号を添える。

**第 1 週の作業**: (a) **◎' の 5 行、なかでも DCIChecker と Semia と MCP-BiFlow の本文 PDF を自分で読み**、下表の差分欄を原文の節番号で裏づける。(b) △ 行の一次化。(c) 2026-09 以降の新規文献の追加。(d) MCP-BiFlow Table 3 と §6 較正対の突き合わせ（下記）。ゼロから調べ直すことではない。`docs/related_work.md` に本節をコピーし、以後は差分だけを更新する（列: `key, venue_or_arxiv, year, verified_level, one_line_what, delta_axis, comparison_outcome, source_of_number, last_checked`）。

### 1.5.1 最も近い 4 件（比較対象。ここを先に書く）

| 先行 | 何をするか（一次資料の記述） | 使い道（baseline / コーパス / GT） | AuthGap が精度で上回ると見込む軸 | 比較結果の報告様式 |
|---|---|---|---|---|
| **MCP-BiFlow / Unsafe by Flow** ◎'<br>arXiv 2605.07836（v1 2026-05-08） | MCP エコシステムの**双方向**データフロー解析。OSS 解析基盤 YASA（Ant Group）上に MCP 固有のエントリポイント復元・プロトコル固有 taint モデル・**手続き間**解析を実装。15,452 リポジトリ、確認済み 32 CVE 事例で recall 93.8%（30/32）。CodeQL 1/32・Semgrep 8/32・Snyk Code 10/32・MCPScan 11/32 を**ベースラインとして上回る**。**guard をモデル化する**: "strict allowlists, canonicalization followed by root-membership checks" で無効化される候補を落とす | **主 baseline。** 実装公開状況を第 1 週に確認。非公開なら**公表値との対ごと突き合わせ**に切り替える。Table 3 の 32 事例は**そのまま比較コーパス**になる（Python は 9 件） | **ゲートを二値（有効／無効）でしか扱わない。** `weak(reason)` の語彙も等級も無く、修正版で weak のまま残る対（A5 AutoGPT、A7 PraisonAI）を脆弱版と区別できない。宣言 D・承認割り込み（`req_occ`）・ツール選択（trig）の概念も無い | **両側通過率を対ごとに並べる。** MCP-BiFlow が修正版も clear できた対は「引き分け」として明記する。脆弱版側で AuthGap が劣る対があればそれも書く（AuthGap は Python 専用・木のみ入力なので不利な対がありうる） |
| **DCIChecker** ◎'<br>arXiv 2606.04769（2026-06-03） | MCP サーバのツール**記述文**と実装の不一致を検出。構造認識 AST 解析（手続き間深さ k=3）＋ Direct-Reverse-Arbitration の LLM 仲裁（Claude Sonnet 4.5、`claude-sonnet-4-5-20250929-thinking`、temperature 0）。2,214 サーバ・19,200 対。**annotation / readOnlyHint の語は本文に現れない**（宣言側は name + inputSchema + description のみ）。**実行はせず収集済み成果物に対する AST 解析のみ**（倫理節に "we did not execute third-party MCP tools against live systems"）。依存インストールの要否は本文に記載なし | **CONTRADICTION セルの比較対象。** 2,214 サーバのリストはコーパス候補 | **判定が LLM 仲裁で非決定的。** 引数位置のデータフロー、sanitizer のモデル化、承認割り込みを持たない | 同一ツール集合に対する CONTRADICTION 行を並べる。**決定性は §5.2 の 3 回一致で測り、精度とは別に報告する** |
| **Semia** ◎'<br>arXiv 2605.00314（2026-05-01） | エージェント skill を Skill Description Language（Datalog 事実基盤）に持ち上げ、11 検出器を到達可能性クエリとして走らせる。**Missing Human Gate**（5.2.1）と **Behavior Claim Contradiction**（Appendix B.3.3）を含む。事実基盤の合成は LLM の refinement ループ | **`req_occ` と CONTRADICTION の比較対象。** 13,728 skill のクロールは母集団の参考 | **コード本体を解析しない。** 入力は "a hybrid of YAML, code stubs, and natural-language prose" で、前処理は Markdown を連結する。コードは難読化・エンコード済みバイナリの marker としてしか見ない。effect / gate / trigger が**閉じた列挙**（本文が closed sets と明記）で、引数位置も validator 等級も無い | 承認割り込みの検出について、同一コーパスで行を並べる。**「Semia が gate を持つ」ことは認めたうえで、gate の等級づけの有無で比較する** |
| **mcp-sec-audit** ◎<br>arXiv 2603.21641（2026-03-23） | 題名が "Auditing MCP Servers for Over-Privileged Tool Capabilities"。実体は TOML ルールブック駆動の**キーワード/正規表現マッチ**＋ Docker/eBPF の動的 fuzzing。capability family へ写像し least-privilege 配備推奨を出す。本文が「**実行時の振る舞い**を意味的制約（parameter manipulation や tool sequence hijacking を含む）に照らして検証することは行わない」と明言 | **最も安価な baseline。** 実装は `nyit-vancouver/mcp-sec-audit` | データフローが無い（正規表現）。capability を列挙するだけで宣言との差を取らない | 正規表現ベースの capability 表だけで両側対がどこまで判別できるかを対ごとに出す。**判別できる対があればそれは AuthGap の当該対の価値を下げるので、そう書く** |

**較正対の重複について（第 1 週の最初の作業）**: MCP-BiFlow の Table 3（32 の確認済み事例）は、**Python の `mcp-server-git` の CVE を 4 件含む**（CVE-2025-68143 / 68144 / 68145、CVE-2026-27735、いずれも Filesystem Access）。ほかに Python では `mcp-atlassian`、`aws-mcp-server`、`mcp-server-data-exploration`、`mcp-kubernetes-server`（2 件）が入る。**§6 の較正対 A1–A3 はこの 4 件と同一である可能性が高い。** `docs/cve_triage.csv` に `also_in_biflow_table3` 列を足して対ごとに記録する。重複が確認された場合の扱い: (i) **held-out の汚染ではない**（held-out は月 6 凍結後の advisory に限る）。(ii) **§6 の合格条件 (ii)「Semgrep と Pysa が修正版を clear できない」は新規性を持たない** — MCP-BiFlow が同じ母集団で Semgrep 8/32・CodeQL 1/32 を公表済みだからである。(ii) の文言を「Semgrep / Pysa に加えて MCP-BiFlow の公表結果と対ごとに並べ、AuthGap が追加で示すものが (effect kind, position, gate grade, weak reason, exec mode) のタプル変化であることを明示する」に改める。

### 1.5.2 エージェント時代の静的解析（2025–2026）

| 先行 | 出典 | 何をするか | 差分の軸 | 比較結果の報告様式 |
|---|---|---|---|---|
| **TaintP2X** ◎ | ICSE 2026、DOI 10.1145/3744916.3773199。Pysa 上に約 3,500 行 | LLM 出力を taint source、危険 sink までの伝播を追う。sanitizer の妥当性判定は **DeepSeek-V3 による LLM 検証**。本文の gpt-engineer 事例は「prefix 検査が正規化の前に置かれるため traversal を防げない」= AuthGap の `weak(prefix_no_canon)` そのものだが、個別 case study に留まりカタログ化されていない | (i) **Pysa 依存＝pyre 環境が必要**（AuthGap の設計制約はここが理由）。(ii) sanitizer 判定が非決定的。(iii) 宣言 D を持たない | pyre 環境が立つ repo に限定して走らせ、両側対を対ごとに並べる。**環境が立たず走らせられなかった repo の件数も報告する**（これ自体が比較軸） |
| **AgentFlow** ◎' | arXiv 2607.01640（2026-07-02） | Agent Dependency Graph（agent / prompt / model / capability / memory / control policy を型付きノード）。5 フレームワーク、AgentZoo 5,399 プログラム。prompt→tool リスクを検出。FP 分析で「27 件の FP のうち 25 件は taint 経路自体は妥当で、**sink 意味論の誤り**が原因」と述べる。**成果物公開の記載は arXiv ページに無い** | (i) 宣言 D の概念が無い。(ii) **sink の粒度（引数位置）と含意が未分解** — AuthGap の「制御位置」がここを分ける。(iii) validator 等級・承認割り込みの支配判定を持たない | 同一 5 フレームワークに対し、prompt→tool 行を並べる。**AgentFlow が 5 フレームワークを覆う一方 AuthGap は MCP + ツールパッケージが主母集団なので、母集団の差を明示してから比較する** |
| **IAL-Scan** ○ | arXiv 2607.01641（2026-07-02） | 無限エージェントループの静的検出。Agent IR に正規化し Agentic Loop Dependence Graph を作る | 問題設定が違う（終端性 vs 権限）。ただし「フレームワーク意味論を IR に正規化しガード述語を保つ」機構は AuthGap の連結経路と同型 | 比較しない。**成果物が公開されていれば流用を検討する**（第 1 週の 5 分のチェック項目に留め、計画の分岐にはしない） |
| **Agent Audit** ◎' | arXiv 2603.22853（2026-03-24）。`HeadyZhang/agent-audit` | LangChain / CrewAI / AutoGen のデコレータを認識し**手続き内 taint** で `eval` / `subprocess.run` への到達を判定。限界節の原文「The current implementation is scoped to intra-procedural taint analysis; inter-procedural data flow across function boundaries is not tracked」。宣言照合は MCP 設定ファイル（配備側）のみ | 手続き内のみ。ツール作者の annotations もコード由来の実効権限も見ない。ゲート/承認割り込みの検出を持たない | **§6 の baseline に追加する。ただし合格条件の必須対象にはしない**（他人のツールが動かないことで自分の合否が決まるのを避ける）。項目 C3 の中で走らせ、**2 日で動かなければ落として「agent 特化 baseline は導入コストにより不成立」と報告する** |
| **Agentic Radar** ○ | OSS `splx-ai/agentic-radar`、論文なし | ワークフローを AST で可視化し OWASP LLM Top 10 に写像 | AgentFlow の第三者測定によれば 60 プロジェクト中 29 件で解析失敗、中央値でノード 2.5・辺 2 しか復元しない | 余力枠の最下位。**第 1 週に走らなければ落とす** |
| **agentic-guard** ○ | OSS `sanjaybk7/agentic-guard`、論文なし | YAML taxonomy でツールを source/sink 分類。README が「It analyzes tool _names_ and _agent architecture_, not what's inside tool function bodies.」「A function named `process()` whose body calls `smtplib.send()` is currently invisible to the tool」と明記。LangGraph `interrupt_before=` と OpenAI SDK `StopAtTools(...)` を承認チェックポイントとして認識 | 関数本体から効果を導かない。承認ゲートの語彙は Def 5 と重なるので**カタログの出発点として流用できる** | **名前ベース分類器を F0a の比較腕に入れる。** 名前だけで効果 precision ≥ 0.7 が出たら、AuthGap の効果解析の価値はその分下がるのでそう書く |
| **記述文スキャナ** ○ | `snyk/agent-scan`（旧 Invariant Labs `mcp-scan`）、arXiv 2602.03580（2026-02-03） | MCP クライアント設定とツールメタデータのみを読む。後者は 10,240 サーバに静的解析を適用し約 13% に不一致を報告 | コードから効果を導かない（メタデータのみ） | **13% を AuthGap の go/no-go 閾値と並べて書かない**（別の量。§9-5） |

### 1.5.3 権限推論の古典系譜（位置づけを一文で伝えるための行）

| 先行 | 出典 | AuthGap の上積み | 比較結果の報告様式 |
|---|---|---|---|
| **Koved, Pistoia, Kershenbaum** ○ | OOPSLA 2002、DOI 10.1145/583854.582452（access rights invocation graph） | 権限格子が**言語仕様として与えられている**前提に依存する。AuthGap では格子（P と P^op）を研究者が定義する必要があり、その定義自体が貢献の一部。主体が「コード」ではなく「モデル」 | 比較実験はしない。系譜の位置づけとしてのみ引用 |
| **Stowaway**（Felt ら）○ | CCS 2011 pp.627–638、DOI 10.1145/2046707.2046779 | **マニフェストが存在しない。** D が無い場合の明示ベースライン P0 を定義し、D の有無で行を分ける（§10 の D 規則）。API→権限の写像が公式には存在せず sink 表そのものが研究成果になる | 同上 |
| **PScout** ○ | CCS 2012 pp.217–228、DOI 10.1145/2382196.2382222 | AuthGap の sink 表 + proxy カタログは PScout の対応表に相当するが、**権威ある正解表が存在しない**。したがって表そのものを凍結（解析指紋、§6）して再現可能にする | 同上。**公式の「MCP 効果仕様」が公開されたら sink 表の構築は貢献でなくなる**ので、第 1 週と月 6 に MCP 仕様の更新を確認する |
| **Capslock** ○ / **Packj** ○ | `google/capslock` / `ossillate-inc/packj` | **引数位置を持たない**（capability の有無のみ）。Packj は主体（誰がその効果を起動するか）の概念を持たない | 引数位置なしの capability 表で両側対がどこまで判別できるかを対ごとに出す |
| **Mir**（Vasilakis ら）○ | CCS 2021、DOI 10.1145/3460120.3484535 | **「宣言が無いときに使われ方から既定権限を合成する」という発想は §10 の D 規則の分岐 3（`D := M` の合成 + drift 検出）と同一であり、D 保有率が低い場合の主張順序の先行例として引用する。** 差は、権限の主体が呼び出し側ライブラリではなくモデルであること、効果が引数値に依存すること | 分岐 3 に落ちた母集団については、Mir 型の合成を**採用**して報告する（比較ではなく踏襲） |

### 1.5.4 汎用 taint ツール（§6 の baseline 行と一対一で対応）

| 先行 | 出典 | 何をするか | 差分の軸 | 比較結果の報告様式 |
|---|---|---|---|---|
| **Semgrep CE の taint mode** ○ | 公式ドキュメント: "Semgrep Community Edition (CE) can only analyze interactions within a single function, also known as intraprocedural analysis." | source→sink の到達可能性 | 主体ラベル、理由付きゲート等級、宣言 D。連結経路は定義上 callee をまたぐ | **(a) source と sink が同一関数内にある行に限定した部分表**と **(b) 全行表**の 2 つに分けて報告する。**同じ source 設定の Semgrep が同じ両側対を通過したら、貢献は「ルールファイル」であり静的解析の新規性は主張しない**（この文言は v2 から変更なし） |
| **CodeQL `py/path-injection`** ○ | query help: 「First, normalize the path using `os.path.normpath` or `os.path.realpath` … Then check that the normalized path starts with the root folder. Note that the normalization step is important…」 | ユーザ制御パスの検証欠如 | **CodeQL は sanitizer を二値で扱う。** AuthGap は同じ構文要素を `strong-path` / `weak(prefix_no_canon)` / `weak(no_containment)` / `weak(no_symlink_resolution)` に等級分けする。**この query help の推奨文が `strong-path` 定義の一次的根拠であり、その否定形が weak 理由の定義になる** | パス系対（mcp-server-git、PraisonAI）で対ごとに並べる。**CodeQL の既定 sanitizer モデルで両側判別できたら、`strong-path` の等級づけは既存モデルの言い換えであるとそう書き、主張を `strong-token` 側に寄せる。** DB 構築を要するので余力扱いは維持 |
| **Pysa ModelQuery** ○ | pyre-check 0.9.25 | 型環境上の taint。TaintP2X の土台 | pyre 環境の構築コスト | **第 1 週末までに環境が立つ repo が 0 なら baseline から落とし「pyre 依存 baseline は環境コストにより不成立」と報告する** |

### 1.5.5 実行時強制（問題設定が異なるが審査で必ず問われる）

| 先行 | 出典 | 何をするか | AuthGap との関係 |
|---|---|---|---|
| **Progent** ○ | arXiv 2504.11703（v1 2025-04-16 / v2 2025-08-30 / v3 2026-05-14）。journal-ref 無し＝査読掲載未確認 | ツール名と引数に対する記号規則ポリシーを**実行時に LLM が生成**し、SMT で更新を検査 | **ポリシーが既に存在する（または実行時に生成できる）ことを前提にする。AuthGap はそのポリシーが無い/不完全であることを配備前に静的に示す。** 規則語彙（ツール名 × 引数制約）は D_op の受け皿として引用できる。**△ 旧版の題が異なるという記憶があるが arXiv abs は版ごとの題を表示しないので、v1 の PDF を取得するまで「改題された」とは書かない** |
| **PACT** ○ | arXiv 2605.11039（2026-05-11） | ツール引数に意味役割を割り当て、値の provenance を replanning を跨いで実行時に追跡 | **「引数位置ごとに主体を決める」粒度が `val(e): positions → P` と同一。** 実行時 provenance であって静的推論ではない。**引数位置の粒度が正しいことの独立した傍証**として引用する |
| **MTGuard** ◎' | arXiv 2607.25297（2026-07-28） | 事前の静的検査＋実行中の eBPF/Docker 監視＋事後の **declared vs observed** 照合。99 攻撃ケース（server 62 / host 26 / user 11）を対象に **240 件の危険なツール呼び出しのうち 116 件を検出 = 48.3%**（baseline: Tool Call Governance 8.3%、Tool Result Inspection 0.0%）、FP 平均 3.7% | 「宣言 vs 観測」を動的に行う最も近い研究。AuthGap は同じ問いを実行もサンドボックスも eBPF も使わず静的に扱う。**攻撃ケース集合が違うので直接比較はしない** |

### 1.5.6 AuthGap がより正確であると見込む軸（4 つ。各々に測定量と報告様式がある）

1. **修正版側（fixed side）**。先行 4 件のいずれも sanitizer を二値（存在 / 有効）で扱うか、判定を LLM に委ねる。AuthGap は連結経路上で等級を付けるので、**修正が weak のまま終わる対**（A5 AutoGPT: exec mode のみ変化、A7 PraisonAI: `realpath` は入ったが照合が素の `startswith`）を脆弱版と区別できる。**測定量 = 両側通過率**（§6 T1.5）。**報告様式 = 対ごとの並べ表。ある先行手法が修正版も clear できたらそう書く。**
2. **判定の決定性**。MCP-BiFlow を除く 3 件は LLM を判定経路に置く。**測定量 = §5.2 の 3 回一致**（バイト一致）。**報告様式 = 精度とは別軸として報告し、精度の代わりに使わない。**
3. **引数位置ごとの粒度**。AgentFlow が自ら FP の原因として挙げた「sink 意味論の誤り」は、`(effect kind, slot)` の分解で減らせる見込みがある。**測定量 = GAP_INJECT 適合率と false-strong 率。** **報告様式 = 位置粒度を潰した腕（全 slot を 1 つに畳む）との比較を §3 のアブレーションに追加してもよいが、必須にはしない。**
4. **機械可読な宣言との照合**。宣言 vs 実装を掲げる 3 件はいずれも自然言語 description か prose を宣言側に置く。AuthGap は `ToolAnnotations` とホスト承認リストと直前リリースの M（D_prev）を宣言側に置く。**動的には Airlock（OSS、MIT、dev.to 2025-08）が declared `readOnlyHint` を観測した振る舞いと突き合わせており、MTGuard も実行時に同じことをする。したがって正しい言い方は「静的にコードから反証した研究が本調査の範囲で見つからない」であって「誰も見ていない」ではない。** **測定量 = CONTRADICTION 精度と D 層別内訳。** **報告様式 = D 保有率が低ければ §10 の D 規則に従って主張順序を落とす。**

**月 6 の再走査**: 凍結時に本節の 4 軸を再走査し、埋まった軸を日付と出典つきで `docs/related_work.md` に記録する。**これは go/no-go ではなく主張順序の調整である**（「軸が空いているか」に測定手続きが無いので閾値にしない）。軸 1（修正版側）が先行手法にも達成された場合、その論文を主 baseline に据え、AuthGap の貢献を残る 3 軸に寄せて書き直す。

### 1.5.7 意図的に扱わなかったもの

- **LavaMoat / SES**: 一次資料未確認。Mir の行が同じ論点を担う。第 1 週に確認して価値があれば 1.5.3 に 1 行足す。
- **MCPTox**（arXiv 2508.14925、45 の実 MCP サーバに対する tool poisoning ベンチマーク）: 攻撃ベンチマークであり比較対象ではないが、**§6 のコーパス取得元および §9-6 の母集団規模確認の出発点として第 1 週に評価する**。
- **prompt injection 検出そのもの**（AgentDojo、LlamaFirewall、Llama Guard 等）: §4 の「原理的に除外」に該当。序論で 1 文だけ触れて除外理由（注入の成否ではなく権限の広さを測る）を書く。
- **`mcp-server-kubernetes` CVE-2026-46519**（npm、< 3.6.0、CWE-863）: `ALLOW_ONLY_READONLY_TOOLS` 等が発見層（`tools/list`）で強制され実行層（`tools/call`）で強制されない。**TypeScript なので対象外**だが、「宣言層と実行層の非対称」の最も明快な定義例として本節に引用する。
- **MCP annotations の CI テスト指南**（ベンダー記事、2026-07 ほか）: `tools/list` の出力を人手で決めた期待値と突き合わせるもので、**コード実装から annotation を反証するものではない**。軸 4 はこれらを排除しない。

## 1.6 参考文献

以下は全て 2026-09-08 に一次資料へアクセスして確認した。**arXiv 版のみの文献は査読を経ていないことを本文でも明記する。** 第 1 週に (a) 最新版番号と査読掲載の有無、(b) DOI の実在、を再確認する。

**査読付き**

- [TaintP2X] Junjie He, Shenao Wang, Yanjie Zhao, Xinyi Hou, Zhao Liu, Quanchen Zou, Haoyu Wang. "TaintP2X: Detecting Taint-Style Prompt-to-Anything Injection Vulnerabilities in LLM-Integrated Applications." ICSE 2026. DOI 10.1145/3744916.3773199. コード `security-pride/TaintP2X`.
- [Koved02] Koved, Pistoia, Kershenbaum. "Access Rights Analysis for Java." OOPSLA 2002, SIGPLAN Notices 37(11):359–372. DOI 10.1145/583854.582452.
- [Felt11] Felt, Chin, Hanna, Song, Wagner. "Android Permissions Demystified." CCS 2011, pp.627–638. DOI 10.1145/2046707.2046779.（Stowaway）
- [Au12] Au, Zhou, Huang, Lie. "PScout: Analyzing the Android Permission Specification." CCS 2012, pp.217–228. DOI 10.1145/2382196.2382222.
- [Mir21] Vasilakis, Staicu, Ntousakis, Kallas, Karel, DeHon, Pradel. "Preventing Dynamic Library Compromise on Node.js via RWX-Based Privilege Reduction." CCS 2021. DOI 10.1145/3460120.3484535.

**プレプリント（arXiv、査読未確認）**

- [MCP-BiFlow] Xinyi Hou, Yanjie Zhao, Haoyu Wang. "Unsafe by Flow: Uncovering Bidirectional Data-Flow Risks in MCP Ecosystem." arXiv:2605.07836（v1 2026-05-08）。**YASA 上に構築。CodeQL / Semgrep / Snyk Code / MCPScan は本論文のベースライン。**
- [Semia] Wen, Li, Liu, Shou, Chen, Tian, Feng. "Semia: Auditing Agent Skills via Constraint-Guided Representation Synthesis." arXiv:2605.00314（2026-05-01）.
- [DCIChecker] Yutao Shi ほか. "Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications." arXiv:2606.04769（2026-06-03）.
- [AgentFlow] Wang, Hou, Zhao, Cheng, Wang. "AgentFlow: Building Agent Dependency Graphs for Static Analysis of Agent Programs." arXiv:2607.01640（2026-07-02）.
- [IAL-Scan] Hou, Wang, Zhao, Wang. "When Agents Do Not Stop: Uncovering Infinite Agentic Loops in LLM Agents." arXiv:2607.01641（2026-07-02）.
- [AgentAudit] Zhang, Nian, Zhao (USC). "Agent Audit: A Security Analysis System for LLM Agent Applications." arXiv:2603.22853（2026-03-24）. `HeadyZhang/agent-audit`. **注: 検出規則数が論文 57 件・リポジトリ説明 51 件で食い違う。第 1 週にどちらかを確認して引用する。**
- [mcp-sec-audit] Huang, Huang, Milani Fard (NYIT Vancouver). "Auditing MCP Servers for Over-Privileged Tool Capabilities." arXiv:2603.21641（2026-03-23）. 5 ページ、投稿先未確定（ACM テンプレートの placeholder）。`nyit-vancouver/mcp-sec-audit`. **注: 論文の検出率 74.7% と README の "94.7% Coverage" が食い違う。**
- [MTGuard] He, Xie, Li, Ji. "Hybrid Analysis for Secure MCP Tool Use in LLM Agents." arXiv:2607.25297（2026-07-28）.
- [MisleadingDesc] Li ほか. "Don't believe everything you read: Understanding and Measuring MCP Behavior under Misleading Tool Descriptions." arXiv:2602.03580（2026-02-03）.
- [Progent] Shi, He, Wang, Li, Wu, Guo, Song. "Progent: Securing AI Agents with Privilege Control." arXiv:2504.11703.
- [PACT] Fan ほか. "The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck." arXiv:2605.11039（2026-05-11）.
- [MCPTox] "MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers." arXiv:2508.14925（2025）.

**ツール・仕様（論文なし）**: Semgrep 公式ドキュメント "Perform cross-file analysis"（CE は手続き内のみ）／ CodeQL query help `py/path-injection`（正規化 → 包含確認の順序）／ MCP 公式ブログ "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do"（2026-03-16、annotations は untrusted hint。Def 6 の一次的根拠）／ `google/capslock` ／ `ossillate-inc/packj` ／ `splx-ai/agentic-radar` ／ `sanjaybk7/agentic-guard` ／ `snyk/agent-scan` ／ Airlock（OSS、MIT、declared `readOnlyHint` を観測と突き合わせる動的ツール）。

---

## 2. 形式的コア

### Def 1: 主体ラベルと 2 つの束

**2 つの別の束を使う。実装で join 関数を共有してはならない。**

- **ラベル束 P**（`trig` と `val` が値を取る）: `USER ⊑ OP ⊑ MODEL`。ラベルの結合は MODEL 方向への join。
- **要求束 P^op**（`req_occ` と `req_val` が値を取る）: `MODEL < OP < USER`。人間の承認割り込みが最強、静的な運用者 allowlist はそれより弱く、ゲート無しが最弱。**ゲート無し = bottom = MODEL。**

確度 `{resolved, opaque(reason), remote}` を**直積で**持つ。**不確実性を P 側の第 4 の値として作らない**（`UNKNOWN` というラベル値は導入しない。判定不能は確度側に一本化する）。

**配備モード**: 既定は `USER ⊑ OP`（ローカル CLI、MCP サーバ）。`--hosted` では USER が P で MODEL に合流し、P^op で MODEL に落ちるので、ホスト承認リストは行を clear しなくなる。**主表は既定モードで報告し、`--hosted` は付録の感度分析 1 表のみ。月 3 の凍結に含める。** `--hosted` の唯一の実 CVE 対は Chainlit CVE-2026-45018（§6 の B3 行）。

**CONTENT ラベルは導入しない。** 静的には全ツール出力が LLM に戻るため常に真になり判別力がない。この決定により「vector store の内容が eval に届く」型の CVE は対象外になる。

### Def 2: MODEL ラベルの導入規則（出発点は 2 つだけ）

- **R1**: カタログ化した LLM 呼び出しの戻り値とその射影。`.content`、`.tool_calls[i].name`、`.tool_calls[i].args`、`.function.arguments`、structured output。
- **R2**: カタログ化したツールエントリのパラメータ。`@mcp.tool`、**低レベル MCP の 2 形**（v1 系の `@server.call_tool()` デコレータの name 分岐、v2 系の `Server(on_call_tool=...)` / `add_request_handler("tools/call", ...)`）、`@tool`、`BaseTool._run`、CrewAI `_run`、`@function_tool`、`@kernel_function`、agno、gptme `ToolSpec`。
  - **R2 の例外**: フレームワークが実行時に「このパラメータをモデルに見せない」ことを執行する機械可読な指定（例: Semantic Kernel の `Annotated[..., {"include_in_function_choices": False}]`）がある引数は `val = MODEL` としない。この例外は執行表と同じ時点（月 3）で凍結する。
  - MODEL ラベル付きセレクタから到達すれば `traced`、登録 API による仮定なら `assumed`。**両者の比率を必ず報告する。**

R1 と R2 は同一主体 MODEL の導入位置が 2 か所あるだけで、sink 表・ゲート採点・判定は共有する。

### Def 3: 効果と sink の 3 形態

`e = (kind, site, slots)`。kind と **slot 語彙**（月 3 の sink 語彙凍結に含む）:

| kind | slot |
|---|---|
| `EXEC` | `code_text` |
| `SPAWN` | `argv0`, `argv[i]`, `argv[*]`, `shell_string`, `cwd`, `env`, `stdin` |
| `FS_WRITE` | `path`, `content` |
| `FS_READ` | `path` |
| `NET` | `url.scheme`, `url.host`, `url.path`, `url.query`, `body`, `headers` |
| `DB` | `sql`, `params` |
| `DISPATCH` | `callee` |

**sink には 3 形態がある。**

- **(a) 直接**: sink 表にある解決済みの dotted callable。
- **(b) proxy**: 受け手の型がカタログ化された wrapper。**proxy カタログの各行は型だけでなく slot 束縛を持つ。** 書式 `受け手到達式 : 受け手型 { slot ← 由来 }`。由来は受け手を生んだコンストラクタの引数（位置 / キーワード）または定数。
  - `git.Repo(p).git.*` / `git.cmd.Git.*` → `SPAWN { argv0 ← "git", argv[*] ← *args, cwd ← p, shell ← False }`
  - SQLAlchemy `Connection`/`Session` の `.execute` / `.exec_driver_sql`、psycopg / sqlite3 cursor の `.execute` / `.executemany` → `DB { sql ← arg0, params ← arg1 }`
  - httpx / requests の `Client`/`Session` の `.get` / `.post` / `.request` → `NET { url ← arg0, body ← data|json }`（`httpx.Client(base_url=b)` は `{ url.base ← b }`）
  - paramiko `SSHClient.exec_command` → `SPAWN`
  - **slot 束縛が無いと較正対 A1（mcp-server-git の封じ込め）が成立しない。** 実コードは `repo = git.Repo(repo_path)` → `repo.git.checkout(branch_name)` であり、受け手の**型**だけを解決しても `cwd` に `repo_path` が載らない。
- **(c) pipe（新設）**: `X = subprocess.Popen(...)` / `asyncio.create_subprocess_shell(...)` / `create_subprocess_exec(...)` で得たハンドルの `X.stdin.write(v)` / `X.communicate(input=v)`。spawn が `shell=True` か argv0 がインタプリタ カタログ（`/bin/sh`, `/bin/bash`, `python*`, `node`, `psql`）に載るとき `EXEC(code_text=v)`、それ以外は `FS_WRITE(content=v)` 相当の情報行。
  - **導入根拠は構造的理由のみで、CVE の裏付けは無い。** OpenManus `Bash` は `_BashSession.command: str = "/bin/bash"` が定数 argv0 で、モデル値は spawn 後の `stdin.write` に入るため、2 形態では全 slot が OP になる。**CVE-2025-2733（GHSA-h76m-8w3j-mgpm）が名指しするのは `app/tool/python_execute.py` であって `bash.py` ではない。** 月 3 の sink 語彙凍結の時点で、この理由と CVE 由来でないことを併記して記録する。

**必要なライブラリ sink 行**（triage 表に「どの pair_id がどの行に依存するか」を記録する）: GitPython `repo.git.*` と `git.Repo().index.add`（proxy 対）、`StdioServerParameters`、pandas `eval`/`query`、sympy `parse_expr`/`sympify`、jinja2、SQLAlchemy `text`、`pathlib.Path.glob`、neo4j / arangodb ドライバの query 実行。

`WRITE_POLICY`（FS_WRITE の path がポリシーファイルに解決される場合）は**マニフェスト属性であり verdict を持たない**。

### Def 4: 効果の権限

- **`trig(e)`**: 効果の**発生**を支配する述語のラベル結び。制御辺は dispatch key（subscript / `.get` / `getattr` / 解決済みレジストリ上の match）とカタログ化したゲート述語に限定。一般分岐と `for tc in tool_calls` は除外（implicit flow の爆発を避ける）。DISPATCH 効果の候補集合の各被呼び出しは `trig := MODEL` を継承する。
- **`val(e): slots → P`**: 仕様は **§2.6** と `docs/val_design.md`。
- **探索方向**: R1/R2 が与える**ユニット入口から sink へ下向き**（呼び出し先を解決して降りる。呼び出し元集合の完全性は要求しない）。**深さ 3 はこの下向きの呼び出し深さ**であり、§2.5 の支配経路と同じ向き・同じ深さ規則を使って CFG と呼び出し解決の実装を共有する。
- **深さの数え方**: 木内ユーザ定義の被呼び出しにのみ加算する。**カタログ化ライブラリ呼び出し（`TRANSFER` 表）は深さを消費しない。間接 target 形（`INDIRECT`: `multiprocessing.Process` / `threading.Thread` / `functools.partial` / `Executor.submit` / `asyncio.to_thread` / `loop.run_in_executor`）は 1 段として数える。** 1 関数内では代入と文字列 / パス演算について無制限。深さ超過は `opaque(depth)`、木内で解決できない呼び出しは `opaque(unresolved)`。**決して drop しない。**
  - `INDIRECT` が無いと OpenManus `PythonExecute`（`multiprocessing.Process(target=self._run_code, args=(code, ...))` 越しに `exec`）が `opaque(unresolved)` になり、§10 の脈拍の負例期待が外れる。
- **下向き探索の残余仮定**: 完全性の要求は呼び出し元集合から **R1/R2 のユニット入口カタログ**へ移るだけである。カタログ外の呼び出し元（未収録フレームワークの route handler、CLI エントリ）からのみ到達する効果は取り落とす。測定点は §6 の traced/assumed 比率と F0c(i)。

### Def 5: ゲート（要求主体は 2 関数に分ける）

- `req_occ(e)` = e を**ゲートする**承認割り込みの要求主体の結び（ゲートの定義は §2.5.2）。承認割り込みの語彙: hook 登録、`confirm()`、`interrupt()`（LangGraph）、`input()`、agno の `requires_confirmation` / `requires_user_input` / `external_execution`、CrewAI Task の `human_input=True`、openai-agents の `needs_approval`、OpenHands agent-sdk の `ConfirmationPolicy.should_confirm`、PraisonAI の `@require_approval(risk_level=...)`。
  - **加えて、ディスパッチキー（セレクタ）そのものを主語とする allowlist / 拒否リストで e をゲートするものは `req_occ` を引き上げる**（等級は config atom 規則に従い、既定閉なら OP、既定開なら MODEL のまま）。値位置を主語とする allowlist は `req_val` 側に入る。**この一行が無いと、運用者 allowlist の背後にある全ツールが GAP_SELECT になる。**
- `req_val(e, p)` = （e をゲートする承認割り込み）∪（位置 p の**値検証**で e をゲートするもの）の結び。

**この 2 分割は必須。** 1 つにまとめると、無関係な引数への強い検証がツール全体の SELECT 判定を消す（型エラー）。

**支配は §2.5 の規則で評価する。1 本の経路の上では最強等級を採り（経路上のゲートは連言だから）、経路の集合では最弱等級を採る（攻撃者が最弱経路を選ぶから）。** 判定不能は真偽に潰さず 3 値 `OPAQUE(reason)` として伝播し、`NODOM > OPAQUE > DOM` の優先順で合成する（§2.5.5）。

**値検証の等級**:

- **strong-path** ⇔ 次の 3 つ。
  - (i) 制御引数の root について、**symlink 解決子**（`realpath` / `Path.resolve`）を通った canonical alias が存在する。**`normpath` / `abspath` は字句正規化子であり単独では (i) を満たさない**（weak 理由 `no_symlink_resolution`）。
  - (ii) 同じ root の canonical alias に**包含述語**（`commonpath` / `is_relative_to` / `Path.relative_to` を ValueError 捕捉で使う形 / **`startswith(root + os.sep)`（root が os.sep 終端に正規化されている形）** / 完全一致 allowlist / `urlparse().hostname` の allowlist 比較）が適用され、その述語が sink をゲートする。包含述語が一つも無ければ weak 理由 `no_containment`。
  - (iii) 述語の他方の被演算子が定数、config root、**または `os.getcwd()`**。
  - **root-equal 条件**: sink に届く値 v と検査された alias a は root-equal でなければならない。root-equal とは、v と a の差が (1) 恒等、(2) `canonicalised` を立てる正規化子の適用（向きは問わない）、(3) principal が OP かつリテラルである `Path.segs` / `Str.parts` 要素の追加、の合成のみで説明できることをいう。**検査点より後に MODEL ラベルの要素が v に追加されている場合は `weak(post_check_append)`。** この縛りが無いと `if base.resolve().is_relative_to(allowed): open(base / name)`（name が MODEL）が strong になってしまう。mcp-server-git の修正は v = `repo_path`、a = `repo_path.resolve()` で差が (2) のみなので、縛った後も strong-path で通る。
  - **`alias_mismatch` 属性**: 位置 p に届く値が「検査された別名そのもの」ではなく「同じ root の別の派生」であるとき true にする。現行の採点規則では strong-path のままとするが、理由欄に必ず残す（正規化不一致の一般形を後で区別できなくするため）。
- **strong-token** ⇔ メタ文字・フラグ拒否（`startswith('-')` 拒否、argv の `--` セパレータ）+ **存在検証**（値が既存の名前空間要素に解決されることの確認。`git rev_parse` 型）+ argv 実行（`shell=False`）。
- **strong-enum（新設）** ⇔ 制御位置の値が、Def 6 の**執行表で執行されると判定された**経路の `enum(S)` / `Literal[...]` / `Enum` サブクラス / `scalar(integer|number|boolean)` に束縛され、Def 6 の被覆規則を満たす。
  - **実装の帰属**: 執行表の判定器（登録 API の形状認識 + 版の確定規則）と被覆規則の判定器は **B3 の成果物であり B5 ではない**。strong-enum は B3b の false-strong 率の分母に入るので、B5（月 9.68）に置くと B3b（月 8.71）が等級 1 つ欠けた分母で判定される。**§7.2 で執行表を B5 から B3 へ移した（B3 6.5 → 6.75、B5 2.5 → 2.25。合計 34.0 は不変）。**
  - **D_dom パーサを書かない決定と矛盾しない**: 被覆規則は D_dom の値域語彙を**読む**ことを要求するが、D_dom 層として**集計する**ことは要求しない。読む側（strong-enum）は B3 で実装し、数える側（`r_dom`）は Def 6 の実装条件を満たすまで 0 のままとする。
  - **否定規則**: 執行表で「執行されない」と判定された経路の同一構文は strong にしない（それは D_dom である）。**執行表で `D_unknown` と判定された経路の値域制約も strong にせず D_dom にも数えない**（行は UNKNOWN として残す）。`format` / `bounded` / `length` / `pathlib.Path` 型 / URL 型は単独では strong にしない。
- **strong-eval（任意。既定では実装しない）** ⇔ 評価器呼び出しにおいて (i) グローバル名前空間から `__builtins__` が除去され、(ii) 名前解決が定数 allowlist に限定されるか AST が allowlist で検査され、(iii) パース前に危険構文の拒否語彙（`__import__` / `__builtins__` / `__subclasses__` / `__globals__` の類）が適用されている場合。
  - **必須ではない。** §6 の両側条件はタプルの変化で定義されるので、A15（qwed-mcp）は strong-eval が無くても「ゲート無し → weak(記号 allowlist + 拒否語彙)」の変化で両側判別できる。strong-eval が要るのは (a) 修正版の verdict を GAP_INJECT から外す場合と (b) false-strong 率の分母に `code_text` / `sql` 位置を入れる場合のみ。**§7.4 切り詰め順序の先頭に「(0) strong-eval を落とし code_text / sql 位置はゲートの真偽値のみ扱う」を置く。**
- いずれでもなければ `weak(reason)`。**理由の語彙（月 6 凍結）**: `first_token`、`prefix_no_canon`、`prefix_no_boundary`（正規化はしたが照合が素の `startswith`）、`no_containment`（正規化子はあるが包含述語が存在しない。witness は絶対パス `/etc/passwd`）、`no_symlink_resolution`（包含述語は境界的に正しいが `abspath`/`normpath` のみ。**witness はシンボリックリンクであり `<root>/../etc/passwd` ではない**）、`post_check_append`、`split_colon`、`no_dashdash`、`no_existence_check`、`no_dash_reject`、`fuzzy_name`、`docker_fallback`、`fail_open`、`denylist_enum`、`regex_no_canon`、`regex_denylist`、`validate_then_fetch`、`underscore_denylist`、`lexical_canon_only`。
- 判定不能は `unknown`。**`strong` は推定で出さない。**
- **否定規則**: `shlex.split` の存在だけでは strong に上げない（AutoGPT の実例が反例）。
- **fail-open 規則**: ゲート述語の関数が、例外・未認識入力・None 返却の経路で許可側の値を返す場合は `weak(fail_open)` とし strong に上げない。**ただし `fail_open` は両側判別には使えない**（Omnigent A17 は修正版も abstain=ALLOW のまま）。F0a の測定量および GAP 理由としてのみ使い、T1 の合格数には寄与させない。

**config atom の源は 4 種**: コンストラクタ kwarg、モジュール定数、`os.environ` 読み出し、CLI オプションの既定値（argparse の `dest`+`default`、click / typer の option 既定値）。既定値が None や開放値なら default-open で `req` は MODEL のまま。hook 登録チェーン、generator 越し、HTTP 越しは `opaque`。

**共通の格下げ（値検証に適用）**: 述語オペランドが MODEL なら `tainted`。**述語オペランド（ポリシー / 権限コンテキスト）が、そのゲートに支配される側のコードで局所的に構成されたリテラル由来オブジェクトである場合は `self_granted`**（`tainted` にも `config-conditional` にも当たらないが `req` を引き上げてはならない。doris-mcp-server CVE-2025-58337 の実例）。config atom 依存なら `config-conditional(atom, default)`。未解決なら `opaque`。`req = OP/USER` になるのは strong と既定閉の config-conditional のみ。**承認割り込みはゲートしていれば `req = USER`**（`--hosted` では引き上げにならない）。ゲート無し = bottom = MODEL。

**val とゲート採点の責務境界**: **val は等級を付けない。** `tokenised` / `quoted` / `canonicalised` / `joined` / `encoded` / `alias_mismatch` は属性として、正規化別名は `alias_facts` として記録するだけで、strong / weak の判定は本 Def のゲート採点器が単独で行う（等級の単一定義点）。**`dash_rejected` のような制御述語由来の事実は val の出力に含めない**（val は `ast.If` を値の合流にしか使わず支配判定を持たないので原理的に生成できない）。

### Def 5-b: 発生ゲートと被覆漏れ（**manifest 属性。第 1 年は verdict を持たない**）

`req_occ` を引き上げうるゲートのうち承認割り込み以外の形態を**発生ゲート** g として列挙し、manifest 属性として記録する。

| 形態 | 具体形 | 前測での保有率（60 MCP サーバ、構文的過大近似） |
|---|---|---|
| 露出ゲート | FastMCP 2.x `@mcp.tool(..., enabled=<expr>)`、3.0 以降の `mcp.disable(names=\|tags=)` / `mcp.enable(..., only=True)`、低レベル `list_tools` 内フィルタ | **0.0%**（`@mcp.tool(` は 2000 箇所あるが `enabled=` の実使用 0） |
| モードゲート | `read_only` / `dry_run` / `allow_write(s)` / `allow_dangerous_*` 等の真偽 config atom を条件とし危険効果をゲートする分岐 | 12.5% |
| 名前 allowlist ゲート | 効果をゲートする `x in ALLOWED` / `x not in DENIED`（accept 集合がリテラルで得られる場合のみ） | 4.0% |
| ポリシー呼び出しゲート | in-tree のユーザ定義関数の戻り値または送出例外が効果をゲートし、その関数が (i) 自身は危険効果を含まず (ii) MODEL 位置を引数に取る | 定義依存で 0〜37% |

`Cov(g)` = g が §2.5.2 の意味でゲートする効果集合、`Leak(g)` = 同一**副 kind**でありながら等級 g 以上のゲートにゲートされない効果集合。漏れ理由の語彙は 4 語（`parallel_entry` / `sibling_reach` / `default_open_atom` / `fail_open_init`）＋ `opaque`。

**kind 粒度の前提条件（格上げの必要条件）**: `Kind(g)` を Def 3 の粗い kind 語彙で取ると、read/write を区別しないゲートの被覆を kind 粒度で比べることになり、**正当な読み取り経路が全て `Leak` に落ちる**（doris 脆弱版では `.execute(` 94 箇所のうち auth_context を渡すのは 1 箇所で、差 93 件がそのまま `Leak`）。したがって `Leak` を verdict に使う前に、少なくとも `DB_READ`/`DB_WRITE`、`FS_READ`/`FS_WRITE`、`SPAWN_CONST_ARGV`/`SPAWN_MODEL_ARGV` の**副 kind**を定義し副 kind 一致を要求する。副 kind 拡張は月 3 の sink 語彙凍結に含める。

**規則 W-occ は採用しない（第 1 年）。** 規則 W と違い「別ユニット B にゲートがあるから当該ユニット A を GAP とする」というパッケージ全域の量化子を持ち込み、`unit id` 単位の manifest / diff モデル、「20 ツールあたり」の FP 予算会計、回帰の行単位期待値凍結のいずれとも整合しない。

**格上げ条件（事前登録。3 つ全て必要）**: (i) 副 kind 拡張後に、野外 60 サーバでの副 kind 一致 `Leak` 行の中央値が 1 パッケージあたり **≤ 3**。(ii) `Leak` 行の裁定適合率 **≥ 0.7**（ラベラー基準は「同一パッケージ内に同一副 kind の効果をゲートする pass-semantics ゲートが存在し、かつ当該効果はそれにも同等以上のゲートにもゲートされていない」を第二ラベラーが独立に確認できるか）。(iii) 両側 `Leak` 対が **≥ 1** 件（凍結後 advisory から取る）。**いずれかが外れたら格上げしない。** 格上げ後の verdict 名は `GAP_COVER` とし、**SELECT とは別セル**にする（SELECT の証人にはしない）。格上げ前は `leak_reason` は manifest 列であり SARIF にも FP 予算にも入らない。

### Def 6: 宣言権限 D（4 層。層ごとに宣言する対象の型が違う）

**D は 1 つの述語ではない。** 1 つの `D ⊭ e` にまとめると、無関係な引数への値域宣言がツール全体の SELECT 判定を消す（Def 5 の `req_occ` / `req_val` 分割と同じ型エラー）。

| 層 | 機械可読な源 | 宣言する型 | 実行時に執行されるか | Def 7 での作用 |
|---|---|---|---|---|
| **D_kind** | MCP annotations の**明示**フィールド | 効果 kind の上界 | されない（仕様が untrusted hint と明記） | SELECT / INJECT の被覆、CONTRADICTION |
| **D_dom** | **執行されない**機械可読な値域制約 | 制御位置 p の値域 | されない | **F0a で母集団が非空と確認された場合に限り**、位置 p の INJECT のみ被覆 |
| **D_op** | ホスト承認リスト、exposure ファイル、アプリ木の `permissions` | 要求主体 | host が執行 | 名前付きツールの req を引き上げる |
| **D_prev** | 直前リリースの M（unit id で join） | 差分の基準 | — | 新規行・拡大行のみを残す差分規則 |

#### D_kind（旧 D_author）

**MCP annotations**。フィールドは `title` / `readOnlyHint` / `destructiveHint` / `idempotentHint` / `openWorldHint` の 5 つ。既定値は `destructiveHint=true`、`openWorldHint=true`、`readOnlyHint=false`。`destructiveHint` と `idempotentHint` は `readOnlyHint==false` のときしか意味を持たない。**既定値による補完を禁止し、当該フィールドが明示的に存在する場合のみ D_kind とする。annotation の不在は「非破壊の宣言」ではない。** 一次的根拠は MCP 公式ブログ（2026-03-16、untrusted hint）。

規則: `readOnlyHint==true` 明示 → `D_kind = {FS_READ, NET}`（EXEC / SPAWN / FS_WRITE / DB(write) は宣言外）。`destructiveHint==false` 明示（かつ `readOnlyHint==false`）→ 破壊的 kind は宣言外、追記型の FS_WRITE と DB(insert) は宣言内。`openWorldHint==true` 明示 → NET の宛先が定数でないことの宣言であり P0 の private-range 制限のみを解除する（EXEC / SPAWN は解除しない）。5 フィールドのいずれも明示されていなければ `⊥`。

**上界を動かさないフィールドは D_kind を構成しない。** `title`（表示名。権限意味論を持たない）、`idempotentHint`（再実行可否であり効果 kind の上界ではない）、`readOnlyHint==false` 単独、`destructiveHint==true` 単独、`openWorldHint==false` 単独は、明示されていても `D_kind = ⊥` のままとする。これらは `D_layer_present` に「annotation あり・上界寄与なし」として記録し `r_kind` の分子には数えない。**したがって `r_kind` の分子は「`readOnlyHint==true` / `destructiveHint==false` / `openWorldHint==true` のいずれかを明示したユニット」であって「`annotations=` を持つユニット」ではない。** 前測の 25.0%（エントリ基準の annotation 明示率）は後者の定義なので `r_kind` の予測値としては使えない。F0a では両方の分子を出し、§10 の分岐判定には前者だけを使う。

**join 規則**: パッケージ内の全 `Tool(...)` / `types.Tool(...)` リテラルを集め、`name=` 文字列と `annotations=` のキーワードリテラルを読む。エントリとは**ツール名文字列の完全一致**で join する。join できない行は「未 join 行」として報告し D にも CONTRADICTION にも寄与させない。**パーサは `annotations=ToolAnnotations(...)` / `ToolAnnotations(**{...})` / 辞書リテラル `{...}` の 3 形を扱う**（前測でエントリ基準 1125 件中 727 件 = 64.6% が後 2 形だった）。読めない形は `D_unknown` とし `⊥` と混ぜない。**フィールド名は仕様の camelCase 表記に限る。** snake_case 表記（`read_only_hint` 等、前測で 21 エントリ）は `ToolAnnotations` に deserialize されず protocol に届かないので `D_malformed` として別行で報告する。仕様外の `category`（前測 684 箇所）も D ではない。

#### D_dom（**前測で母集団 0。定義のみ置き、実装は条件付き**）

**執行性規則（この層の唯一の正当化）**: 機械可読な値域制約は、フレームワークが実行時にそれを執行するなら**宣言ではなく値検証**であり Def 5（M 側）に属する。執行しないなら untrusted な自己申告であり D に属する。**同じ構文が登録経路と SDK 版で役割を変える。**

**執行表（一次資料で確認。月 3 で凍結し `docs/fingerprint.json` の D パーサ規則に含める）。判定は (1) 登録 API の形状 → (2) 版の確定可否 の順。版は二次的な証拠であり単独では使わない。**

| 登録経路（木の中の形） | 判定 | 一次資料（commit を必ず添える） |
|---|---|---|
| 高レベル `@mcp.tool`（公式 SDK `fastmcp`(v1) / `mcpserver`(v2)） | **執行される → Def 5 側** | v2.0.0b2 `2713b53` の `mcpserver/tools/base.py:152` が `fn_metadata.call_fn_with_arg_validation(...)`。v2.2.0 `9972c21` では当該 API は deprecated で経路は `base.py:149 validate_arguments` + `:176 call_fn`。v1.30.0 `8c2fa6e` では `fastmcp/tools/base.py:101` |
| サードパーティ `fastmcp`（jlowin） | **執行される → Def 5 側** | `e3fb4af` の `fastmcp/tools/function_tool.py:474` `type_adapter.validate_python(arguments, strict=strict)` |
| langchain `BaseTool`（`run` / `invoke` 経由） | **執行される → Def 5 側** | `langchain_core/tools/base.py:778 _parse_input` → `:834 input_args.model_validate` |
| **低レベル `@server.call_tool()` デコレータ形**（v1 API）+ 手書き `inputSchema` | **版が [1.10, 2.0) に確定できるときのみ執行される → Def 5 側。確定できなければ `D_unknown`** | `v1.10.0` で `def call_tool(self, *, validate_input: bool = True)` と `jsonschema.validate(...)` が導入。**`v1.9.0` / `v1.6.0` は `def call_tool(self):` で検証ゼロ。したがって「1.x なら執行される」と書いてはならない** |
| **低レベル `Server(on_call_tool=...)` 形**（v2 API）+ 手書き `inputSchema` | **執行されない → D_dom** | `2713b53`(v2.0.0b2) と `9972c21`(v2.2.0) の `lowlevel/server.py` に jsonschema の import が無く、`src/` 内の使用は client 側の **output** schema 検証のみ。**v2 の `lowlevel/server.py` に `def call_tool` は存在せず、ハンドラは `__init__` の `on_call_tool=` で渡される** |
| `tool._run(...)` を検証経路を通さず直接呼ぶ内部経路 | その呼び出しは OP 起動の経路であり、モデル面の分類を変えない | — |
| スキーマを動的に組む / 上のどれでもない | **`D_unknown`** | — |

**版の確定規則**: (1) `==X.Y.Z` / `~=X.Y` / 上限付き指定、または lock ファイル（`uv.lock` / `poetry.lock` / `Pipfile.lock`）の解決済み版があるときのみ「版が確定した」とする。(2) **`>=X.Y` だけの指定は版を確定しない**（`mcp>=1.2.0` は 1.2.0 も 2.2.0 も 1.30.0 も許す。PyPI の `mcp` 最新は 2.2.0）。(3) 版が確定しない低レベル経路は **API 形状**で決める（`@server.call_tool()` は v2 に存在しないので実行時は必ず < 2.0、`Server(on_call_tool=)` は必ず ≥ 2.0）。それでも [1.10, 2.0) か < 1.10 かが決まらなければ `D_unknown`。(4) **読めないものを既定で「執行あり」とも「執行なし」とも仮定しない。**

**D_dom の値域語彙**: `enum(S)` / `pattern(r)` / `format(f)` / `scalar(...)` / `bounded(min,max)` / `length(min,max)` / `⊤`。源は手書き `inputSchema`、pydantic `Field(...)`、型注釈（`Literal` / `Enum` / `constr` / `conint`）、`Path` / `HttpUrl` 等の型。

**被覆規則 `D_dom(u,p) ⊨ e@p`（これ以外では被覆しない）**: `enum(S)` は S が定数リテラルの有限集合で各要素が当該 sink 文法のメタ文字を含まないとき被覆。`scalar(integer|number|boolean)` は効果 view がシェル文字列 / 生パス / 生 URL / SQL 文のとき被覆。`pattern(r)` は r が `^...$` で錨付けされリテラルと有界量化子のみからなるときに限り被覆（判定できない r は `D_unknown`。決して被覆に数えない）。`format` / `bounded` / `length` / `Path` 型 / URL 型は**被覆しない**。**被覆判定の対象は Def 3 の制御位置に限る**（`limit` / `offset` に付いた `bounded` を数えない。この区別を落とすと前測で危険ユニットの D_dom 保有率が 6.1% → 28.6% に膨らむ）。

**実装条件**: 前測（付表 D-1）で `r_dom` として数えた 3 件はいずれも単一リポジトリの `@mcp.tool` デコレータ経路（= 執行表では Def 5 側）で、値域が付いた位置も `mode` / `response_format` / `cell_type` で Def 3 の制御位置ではない。**D_dom として観測された母集団は MCP サーバ 0/141、ツールパッケージ 0/191 である。** さらに危険効果の登録形内訳は decorator 129 / basetool 12 / **tool_literal 0** で、被覆語彙が集中する手書きスキーマ経路（14.4%）では危険効果が 1 件も解決できていない。**したがって Def 6 には定義・執行表・被覆規則を置くが、パーサは書かない。** 着手条件は「F0a が手続き間深さ 3 で低レベル経路の危険効果を解決したうえで、D_dom の母集団が非空（≥ 5 ユニット、かつ ≥ 2 リポジトリ）であることを示す」こと。満たさなければ D_dom は定義のみで凍結し `r_dom = 0` として報告する。

#### D_op（旧 D_operator）

`langchain::HumanInTheLoopMiddleware(interrupt_on=)`、`langgraph::graph.compile(interrupt_before=)`（公式に非推奨）、`openai-agents::FunctionTool.needs_approval`、`claude-agent-sdk::ClaudeAgentOptions.allowed_tools`、Claude Code `settings.json` の `permissions` の allow / ask / deny、運用者が供給する exposure ファイル。**in-tree の露出宣言**（FastMCP `enabled=` / `disable(names=|tags=)` / 低レベル `list_tools` フィルタ）もここに入れるが、`enabled=` の式が真偽 config atom に解決でき**かつ atom の既定が閉**のときのみ D として読む。既定が開なら `D ⊭ e` 側に倒す。解決できない式は `opaque`。**前測での in-tree 露出宣言の実使用は 0 件なので、§10 の D 保有率にこの経路を含めても効果は無いと見込む。含めるか否かは第 0 週に凍結する。**

**帰属規則**: 解析対象木の `.claude/settings.json` は、**その木がエージェントアプリ（T3-app 母集団）である場合にのみ** D_op である。MCP サーバ / ツールパッケージの木にあるそれは開発用の別エージェントの設定であり出荷物の宣言ではない（前測で 60 サーバ中 3 件・5 ファイルに `permissions` があり、いずれも開発用。**ただし 1 件は自リポジトリが出荷する MCP ツール名を allow しており、構文上は区別できない。したがって帰属は木の母集団で決め、内容では決めない**）。運用者が `--exposure <file>` で明示的に供給したものだけが例外なく D_op。

**agno の `requires_confirmation` / `requires_user_input` / `external_execution`、CrewAI Task の `human_input=True`、openai-agents の `needs_approval` は Def 5 の承認割り込み（M 側の `req_occ`）であって D ではない。** 二重計上しないこと（前測でツールパッケージ 1352 エントリ中 86 件 = 6.4% がこの語彙を持ち、D に数えると D 保有率が 0.0% から 6.4% に見かけ上跳ね上がる）。

#### D_prev（新設）

D_kind / D_dom / D_op がいずれも `⊥` のユニットについて、同一パッケージの直前リリース（または事前登録した基準リリース）の manifest を D とする: `D_prev(u) := M_{r-1}(u)`。

- **join**: unit id の完全一致のみ。qualified_name が一致し schema_hash が変わった行は `SCHEMA_CHANGED`、qualified_name が消えて別名が現れた行は `delete+add` であり **rename と新規追加を区別しない**（§5.2）。したがって D_prev は rename を跨いだ主張をしない。
- **差分規則**: `GAP_DRIFT(u, e) ⇔ e の kind が M_{r-1}(u) に無い、または制御位置 p の val が OP から MODEL になった、または req_occ / req_val の等級が下がった`。**行が増えないこと自体は verdict ではない。**
- **適用条件**: 静的に取得できるリリースが 2 本以上あること（前測で 60 サーバ中 54 件 = 90.0%）。
- **収量は小さい。** 前測（13 repo、約 5 リリース離れた 2 タグ、新版 1525 ユニット）で新規または変化したユニットは 82 件 = 5.4%、**効果 kind 自体の変化は 3 件 = 0.20%**。**行が 0 でも失敗ではなく「リリース間で実効権限は拡大していない」という測定結果として報告する。**

#### 層の優先順位と、宣言が無い場合

被覆は**層ごとに独立に**評価し、**弱い層が強い層の GAP を消してはならない**。D_kind が kind を宣言していても位置 p の値域が `⊤` なら `GAP_INJECT(e,p)` は消えない。逆に D_dom が位置 p を被覆しても `GAP_SELECT(e)` は消えない。

いずれの層も `⊥` ならベースライン **P0**: 「MODEL は EXEC / SPAWN / 正規化なしの FS_READ・FS_WRITE / private-range NET に届いてはならない」。

**記述文は D ではない。** `description=` / docstring / `Annotated[str, "..."]` の説明文はどの層にも入れない（前測で MCP サーバの引数保有エントリの 30.2% が「説明文はあるが機械可読な制約は 1 つも無い」状態で、これを D に数えると D 保有率が 5.4% → 35.6% に膨らむ）。**記述文の語彙による purpose extractor は verdict 入力に使わない。** Semantic Kernel の `@kernel_function(name=, description=)` は効果 kind も承認も宣言しないので D ではない（一次確認: `kernel_function_decorator.py:13-17` の引数は `func` / `name` / `description` のみ）。

### Def 7: 判定

| verdict | 条件 |
|---|---|
| `GAP_SELECT(e)` | `trig(e) = (MODEL, traced)` かつ `req_occ(e) = MODEL` かつ `D_kind ⊭ kind(e)` かつ `D_op ⊭ u`。**D_dom は SELECT を被覆しない** |
| `GAP_INJECT(e, p)` | `val(e)(p) = MODEL` かつ `req_val(e, p) = MODEL` かつ **`D_dom(u,p) ⊭ e@p` かつ `D_op ⊭ u`**。**D_kind は kind の上界しか宣言せず制御位置を宣言しないので INJECT を被覆しない**（Def 6「層ごとに独立」）。D_kind が当該 kind を宣言している場合は `D_layer_present ∋ kind` を行に記録するだけで verdict を変えない |
| `GAP_DRIFT(u, e)` | D_kind / D_dom / D_op がすべて `⊥` で、D_prev と join でき、Def 6 の差分規則に当たる |
| `CONTRADICTION(e)` | D_kind が `readOnlyHint==true` または `destructiveHint==false` を**明示**しているのに M に WRITE / EXEC がある |
| `INVENTORY(e)` | GAP 条件を満たすが、**当該 verdict を被覆する権限のある層**が当該効果 / 当該位置を宣言している（SELECT は D_kind または D_op、INJECT は D_dom または D_op、DRIFT は D_prev）。`covered_by ∈ {kind, dom, op, prev}` を必ず記録する。**「いずれかの層」ではない** |
| `UNKNOWN` | remote / opaque / 動的レジストリ / `D_unknown`。**決して clean にしない。** manifest では `resolution=opaque(reason)|remote` の行として、annotation patch では「未検証」として明示的に出力する |

**規則 W（weak validator は宣言に優先）**: 位置 p に `weak(reason)` の validator が存在すれば、P0・D_kind・D_dom に関係なく `D ⊭ e`。理由は、validator の存在自体がコードレベルの封じ込め宣言であり、宣言が 2 つ食い違う場合はコード側を採るため。**D_op（承認割り込みを host が執行する層）には優先しない。** この規則により、正しく annotation を付けたうえで弱い検証を持つツールは INVENTORY ではなく GAP になる。意図した動作であり報告量の主因である。**規則 W で GAP になった行の比率を指標に出す。**

**凍結済み rubric 1c**: 仕様として任意実行するツール（`PythonExecute` / `execute_command` / `run_code` / `shell` 等）は、**制御位置に validator が一つも無い場合に限り** INVENTORY 候補とし、運用者が exposure ファイルを供給した場合のみ INVENTORY にする。供給が無ければ P0 の下で GAP_INJECT。いずれかの制御位置に `weak(reason)` があれば規則 W が優先し GAP_INJECT。**同型のツールは CVE の有無に関わらず同じ verdict。第 0 週の作業はこの文の追認と記録であり再検討ではない。** 対象ツール名は `docs/rubric_1c.json` に凍結する。**修正が存在しない CVE（A6 AutoGPT CVE-2024-6091、B5 Upsonic CVE-2026-30625。両方とも第 3 版で一次確認済み）はこの rubric の議論の典拠として使う。**

**`assumed` の trig では SELECT 行は GAP ではなくマニフェスト行**（この規則は narrow しない）。これが無いと定数 argv の `subprocess.run(["git","status"])` が全部 GAP になる。

**FP 予算に数えるのは INJECT 行のみ。** `leak_reason` / `cov_gate` は manifest 属性なので予算外。将来 `GAP_COVER` を格上げする場合は**別建ての予算**（`GAP_COVER 件数 ≤ 3 / 20 ツール`）を報告値として先に測り、月 6 に編入可否を決める。

**全 GAP 行と全 INVENTORY 行に `covered_by` と `D_layer_present` の 2 列を必須にする。**

### 2.5 支配判定の設計（項目 B3。全仕様は `docs/dominance_design.md`）

#### 2.5.0 前身が発火しなかった理由 — 設計の出発点

前身の実ターゲット 33 件で guard-dominates 事象は 0 だった。原因は「実コードに支配ガードが無かった」ことではなく、**支配を判定する前に保守フォールバックへ落ちていた**ことである（監査 §1.5 finding F: 残った 2 件の TP はどちらも「未解決呼出元」と「深さ上限」のフォールバックだけで立っており、その 2 つを外すと 56 テスト緑のまま両フラグが消える）。**前身が測っていたのは「ガードの不在」ではなく「判定の不能」である。**

**測定の帰属**: 本節と付録 G の「前身の実測」列は前身リポジトリの **HEAD `18a61d9`**（99 テスト全緑）に対する実測である。`f7aced6` は 7 コミット前で、その間の `20aebd3`「Stage-2 detector v2」が `selection_guard.py` を 1037 行書き換えている。**この 2 版の差が作り直しの最強の論拠である**: 監査に応えて v2 は「`or` 連言」と「非 exit 本体」を一律に非支配へ倒し、その結果**旧版が正しく `DOM` と採点していた G2 と G4 が v2 では `NODOM` に落ちた**（両版で実測）。AST 兄弟文方式は穴を塞ぐたびに別の正しい形状を落とす — 収束せずに振動する。等級の弁別が乗る土台としては、誤り件数そのものより**この振動が致命的**である。

4 つの構造変更（G-mutant はこれを 1 つずつ pin する）:

| # | 変更 | 前身 | AuthGap |
|---|---|---|---|
| S1 | 探索の向き | sink から呼び出し元へ**上向き**（呼び出し元集合の完全性という解けない問題に落ちる） | R1/R2 のユニット入口から sink へ**下向き**。必要なのは呼び出し先の解決だけで Def 4 と機構を共有する |
| S2 | 支配の定義 | AST の「同一ブロック内の先行兄弟文」 | 関数ごとに構成した CFG 上の支配（例外辺・ループ辺・短絡辺を含む） |
| S3 | 値域 | 真偽 2 値（判定不能を「ガード無し」に潰す） | **3 値** `DOM(grade) / NODOM(reason) / OPAQUE(reason)` |
| S4 | ゲートの認め方 | 名前トークン一致のみ（述語を改名すると判定が反転する） | **カタログ名 ∧ ゲート要約**（拒否経路が raise/exit で終わることを木内で確認）。名前だけ一致は `OPAQUE(gate_name_only)` |

#### 2.5.1 CFG の構成（標準ライブラリ `ast` のみ）

関数ごとに `ENTRY` / `EXIT` / `EXC_EXIT` と、原則「文 1 個 = ノード 1 個」の有向グラフを作る。基本ブロック併合は行わない。`if` は test ノードから True/False 辺（**「body が全部 exit 文か」という構文条件は使わない**）。`while` / `for` は header からの進入辺・脱出辺・後退辺（`for` は 0 回実行があるのでループ本体内のゲートはループ外の後続をゲートしない）。`try` は body の各文から handler へ例外辺（保守側: `Constant` のみの代入以外はすべて送出しうる）。`with` は `ENTER(cm)` / `EXIT(cm)` の仮想ノード（`contextlib.suppress(E)` は body から出た例外辺を後続へ吸収する）。async は同一、`Expr(Await(Call))` も**ゲート文候補に含める**。内包表記 / genexp は合成した無名関数として別 CFG（`GeneratorExp` は即時消費される場合のみ合流、変数束縛されて関数外へ渡る場合は `OPAQUE(lazy_genexp)`）。`A and B` / `A or B` / `IfExp` / `NamedExpr` は式ノードの分岐へ脱糖する（これで `or` の極性と walrus が構文特例なしに出る）。`match` は `if` 連鎖へ脱糖。**1 関数 2000 CFG ノード超で `OPAQUE(cfg_cap)`**（§5.2 の cap 一覧と月 10 の指紋に含める）。

**唯一の例外は `finally`**。Python では finally は正常終了・例外・`return`・`break`・`continue` のどの脱出経路でも実行されるので、1 ノードで表すと支配関係が経路ごとに矛盾する（G12 の 1 ソース行は CFG 上 2 ノードになり、正常複製は「ゲートする」、例外複製は「ゲートしない」と互いに矛盾する）。したがって **finalbody は脱出種別ごとに複製する**。結果として 1 行が複数ノードを持つので: **効果の verdict はその効果行の全複製について計算し §2.5.5 の ⊓（最弱）を採る**。**witness には採用された複製の脱出種別を併記する**（`finally-copy(exc) @ L14`）。

**実装順は F0a（項目 A5、B3 より前に完了）で測った構文出現率で決める。** 出現率 1% 未満の構文行は実装せず `OPAQUE(unsupported_syntax)` に落とし、対応する G-mutant を受け入れ集合から外す（外した構文名と出現率を本文に書く）。`unsupported_syntax` を OPAQUE 語彙に加える。**これは opaque 率 ≤ 40% を押し上げる方向なので opaque 予算と競合する。**

#### 2.5.2 支配計算と「ゲートする」の定義

CFG の逆後行順を取り、Cooper–Harvey–Kennedy の反復 idom アルゴリズム（Cooper, Harvey, Kennedy, *A Simple, Fast Dominance Algorithm*, **Rice University CS TR-06-33870, 2006**, hdl:1911/96345）で支配木を作る。**採用理由は実装量とテスト量のみである。速度の優劣は主張しない**（CHK 原論文は実測で Lengauer–Tarjan より速いと述べるが、Georgiadis, Tarjan & Werneck, *Finding Dominators in Practice*, JGAA 10(1):69–94, 2006 は LT-simple と SNCA の方が安定して速いと報告しており決着していない）。**反証条件**: T3 の実行で支配計算が 1 ツールあたり中央値 0.5 秒を超えたら SNCA へ差し替える。

**支配だけではゲートにならない。** 支配は「ゲートが評価されること」しか言わず「拒否されたときに効果へ行かないこと」を言わない。監査 finding E が前身について指摘したのはまさにこの取り違えであり、**同じ取り違えを再生産しないために次の連言を「ゲートする」の定義とする**。

> ゲート `g` が効果 `d` を**ゲートする**（`gates(g, d)`）⇔ **(G-i)** `g` が `d` を支配する、かつ **(G-ii)** `g` の**拒否後継** `deny(g)` のどれからも、**`g` を通らずに** `d` へ到達できない。形式的には、CFG から節点 `g` を除いたグラフ `CFG∖{g}` において、すべての `s ∈ deny(g)` について `d ∉ Reach_{CFG∖{g}}(s)`。

`deny(g)`: 述語形は肯定センスなら false 辺の後継、否定センス（`is_denied` 等）なら true 辺の後継。送出形（A-a / A-b、`ENTER(cm)` を含む）はそのノードから出るすべての例外辺の後継。両方持つ場合は和集合。

**`CFG∖{g}` の除去は必須である。** 除去しないと G10（ループ内 `continue` の allowlist）で `continue → header →（次の反復）→ 効果` が拒否辺からの到達路に見え、正しいループ allowlist を誤って NODOM にする。

`(G-i)` は満たすが `(G-ii)` を満たさないゲートは `NODOM(deny_reaches_effect)` として **witness 付きで manifest に残す**（「ゲートは在るが握り潰されている」は報告価値が最も高い行である）。

**後支配は `finally` 合流の検出（G12）にのみ使う。** 「`EXC_EXIT` や exit 文が効果を後支配しないことの検査」では G1 の穴（失敗辺が log してから return する形）を判定できない — 後支配は*効果の*性質を見ており*ゲートの拒否辺の行き先*を見ていない。

*測定（この節の規則が pin されている根拠）*: 付録 G の手続き内 12 件に対し、`ast` から CFG を組み CHK で支配を計算したうえで、後支配版と `(G-i)∧(G-ii)` 版を**無調整で**適用した。後支配版は **G6（except が承認例外を握り潰す）と G9（`contextlib.suppress` が吸収する）を `DOM` と採点する** — 本設計が潰すために存在する誤 clear の方向そのものである。`(G-i)∧(G-ii)` 版は 12 件中 11 件が期待どおりで、唯一の不一致 G11 は §2.5.3 の主語一致が決める案件である。**したがって §2.5.2 ＋ §2.5.3 で 12/12。**

#### 2.5.3 ゲート述語の認識（承認 A と値検証 V を別に認識する）

**評価順は (1) 主語一致 → (2) ゲート認識（A-a/A-b/A-c）→ (3) 支配。**

**A（承認割り込み、`req_occ`）**: A-a カタログに `raises` と記録された呼び出し。A-b **ゲート要約** — 呼び出し先が木内で解決でき（深さ 2 まで）、その CFG 上で「拒否側の出口がすべて `raise` / `sys.exit` / `os._exit`」であることを確認できる（**呼び出し先が `@contextlib.contextmanager` の生成器である場合は「`yield` より前の拒否経路の出口がすべて raise / exit」を確認する**）。A-c 戻り値が分岐条件として使われ、その分岐が §2.5.2 の意味で効果をゲートする。**名前だけカタログに一致し A-a/A-b/A-c のどれも取れない場合は `OPAQUE(gate_name_only)`。推定で A にしない。**

**V（値検証、`req_val`）**: Def 5 の等級をそのまま使う。CFG 側の追加要件は「その述語が効果をゲートすること」。

**主語一致（V にのみ課す）**: ゲートしていても、述語のオペランドが当該効果の**当該制御位置**の値と同一の値、または前向き def-use でその値から導かれる値でなければ `req_val` を引き上げない。**主語一致に失敗した述語は、呼び出し先が木内で解決できるか否かに関わらず `NODOM(non_binding_gate)` に落ちる**（`OPAQUE(gate_name_only)` にはしない。主語不一致は呼び出し先本体を見なくても決まるから）。A には課さない（承認は位置ではなく効果の発生に対する承認であるため）。

#### 2.5.4 手続き間合成と reason 語彙

経路の起点はユニット入口。同一のツール本体に複数のユニット入口から到達できる場合、**入口ごとに別の行**として採点する（G14）。ディスパッチキーが定数辞書リテラル・`if/elif` 連鎖・`match` へ解決できる場合は候補集合を展開し各候補を別経路とする。解決できない場合は `OPAQUE(dynamic_registry)`。深さ超過は `OPAQUE(depth)`、循環は `OPAQUE(cycle)`。**いずれも決して drop しない**（前身は候補 0 の wall を `continue` で無言に捨てていた）。

**reason 語彙は 2 系統ある。受け入れ条件が「reason クラス一致」を要求する以上、両方を凍結する。**

| 系統 | 語彙 |
|---|---|
| `OPAQUE(...)` | `unresolved` / `depth` / `dynamic_registry` / `lazy_genexp` / `cfg_cap` / `gate_name_only` / `cycle` / `unsupported_syntax`（8 種） |
| `NODOM(...)` | `no_gate` / `deny_reaches_effect` / `non_binding_gate` / `alt_entry`（4 種） |

**語彙外の理由を新設してはならない。**

#### 2.5.5 最弱等級（不動点として計算する）

P^op の順序は `MODEL < OP < USER`。1 本の経路の上では最強（⊔）、経路の集合では最弱（⊓）。**ループがあると経路集合は無限（G10 自身がループを含む）なので、経路を列挙せず前向きデータフローの最小不動点として計算する。**

```
in[n]  = ⊓_{p ∈ pred(n)} out[p]          （ENTRY では bottom = MODEL）
out[n] = in[n] ⊔ ( grade(n) if gates(n, e) else bottom )
req(e) = ⊓_{c ∈ Copies(e)} in[c]
```

`gates(n, e)` は §2.5.2 の `(G-i)∧(G-ii)`。`Copies(e)` は §2.5.1 の `finally` 複製。**MFP = MOP の根拠**: P^op は鎖なので分配束であり、遷移関数が `λx. x ⊔ k` の形で ⊓ 上に分配する。ゲートがどこにも無い経路では ⊔ が bottom のまま残るので `req = MODEL`。

3 値の合成の優先順は **`NODOM > OPAQUE > DOM`**。OPAQUE を NODOM に潰すと前身の幻の TP が再生産され、DOM に潰すと無言の false-clean（G13）になる。**どちらも禁止する。** この優先順は実装で共有関数にする。

#### 2.5.6 受け入れ条件

- **B3a（B3 の 1.5 学生週時点）= 支配のみを問う 8 mutant を 8/8 撃破。** 8 件は前身の監査が名指しで記録した破れ方から採り `fixtures/dominance_mutants/` に凍結する: (1) `ok = confirm(name)` の束縛のみで無条件 dispatch、(2) `if trusted or confirm(name):`（`or` の極性）、(3) `if not is_allowed(name): tool.run()`（極性逆）、(4) 無関係な関数の `human_in_the_loop=False`（file-level gate の誤検出）、(5) **別モジュールの同名クラスにゲートがあり、当該ユニットの連結経路上には無い形**（前身は呼出元を上向きに辿ってクラス名だけで一致させ誤って clear した。AuthGap は入口から sink へ下向きに辿るので「呼出元一致」という概念自体を持たない。この mutant は下向き走査が同名クラスに引きずられないことを試す）、(6) parse 失敗ファイルの黙殺、(7) node/深さ cap 到達での黙示 clear、(8) ガード偽側の分岐に dispatch がある形。**(1)–(5) と (8) は「非支配と判定されるべき形」であり、1 件でも支配と判定したら不合格。(6) と (7) は支配規則ではなくハーネスの性質を突くので、期待値は「非支配」に加えて該当行（`parse_failure` / `TRUNCATED` + `OPAQUE(cfg_cap)`）が出力されることであり、行が出なければ不合格とする。**
- **B3b（完了時）= 付録 G の G1–G15 を 15/15。** 一致を要求するのは `(verdict, reason クラス, witness 行番号)` の 3 つ組であり真偽値だけではない。期待値は `fixtures/gates/expected.json` に**実装着手前に**コミットして凍結する。
- **実装のミューテーション試験**: 支配判定の実装に 15 個の変異（支配規則の反転、例外辺の削除、`CFG∖{g}` の除去、3 値の潰し、主語一致の削除、finally 複製の抑止、深さ上限の緩和、キャップ記録の削除など）を入れ `fixtures/gates/` のテストで**生存 ≤ 2**。比較対象として記録する前身の数字は「**56 テスト時代の実装変異 15 件中 9〜10 件が生存**（監査 §1.5 stage2-guard-5）」であり、監査応答でテストは 99 件に増えたが監査自身が変異試験を再実施していないため **HEAD での生存数は未知**である。
- **「15 mutant」の語は 2 つの別物を指していた。** 解析対象スニペットを **G-mutant**、実装に入れる変異を**実装変異**と呼び分ける。
- **`≤ 2` にも下記の野外発火率 `≥ 5%` にも経験的根拠は無い。事前に固定することだけが根拠であると本文に明記する**（§3 の交差行 ≥ 3 と同じ扱い）。
- **15/15 は「野外で発火する」ことを意味しない。** リスク 6 が消えるのは §10 の野外支配発火率の行を通ったときだけである。
- **held-out G16–G20**: 出所は **F0a コーパス（60 サーバ + 30 パッケージ）から seed 付き無作為抽出した、T1 のどの対にも含まれないリポジトリのゲート文**を最小化して 1 件ずつ取る。**T1 の修正版は使わない** — A7–A18 の修正版は本作業で weak 理由語彙を導出した出所そのものであり（`prefix_no_boundary` は A7 から、`no_symlink_resolution` は A10 から。§6 T1.4）、そこから取ったゲート文は定義上 held-out にならない。抽出 seed と候補列挙スクリプトは月 6 の語彙凍結と同時にコミットし、最小化の実行は凍結後に行う。**設計者が形を選んでいないこと（seed 固定の無作為抽出）が汚染の無さの根拠であり、出所が実コードであること自体は根拠にならない。** 第二ラベラーの時間も消費しない。**合否条件に入れず測定値としてのみ報告する。**

#### 付録 G: G-mutant 15 件（`fixtures/gates/`。第 0 週に移し、本表は要約のみ残す）

共通前置き `fixtures/gates/_prelude.py`（すべて木内で解決できる）: `ApprovalDenied` 例外、`ALLOWED_TOOLS = {"git_log","git_show"}`（モジュール定数・既定閉）、`confirm(name)`（A 真偽形）、`require_approval(name)`（A raise 形）、`is_allowed(name)`（V allowlist）、`TOOLS` 辞書、および **`class Gateway`**（`default_tool`、`is_allowed(self,name)`、`@contextlib.contextmanager require_approval(self,name)`、`plugins = _load_plugins()`（木内解決不能））。囲み関数は注記が無い限りユニット入口とする。**唯一の例外は G14 の `run_shell` で、これは R2 のカタログ化エントリではないのでユニット入口として数えない。**

| id | 突く穴 | 期待 | 前身の実測（HEAD `18a61d9`） | 誤りの向き |
|---|---|---|---|---|
| G1 | exit 前に 1 文（`_is_exit_body` の全 exit 要求） | `DOM(OP)` | `NODOM`（"non-exit body"） | 誤 FN |
| G2 | `or` の失敗連言 | `DOM(USER)` | `NODOM`（"`or` disjunct"）**[f7aced6 では `DOM`]** | 誤 FN（v2 で退行） |
| G3 | `await` した承認割り込みの裸文 | `DOM(USER)` | `NODOM`（seen にすら出ない） | 誤 FN |
| G4 | walrus を含む test | `DOM(USER)` | `NODOM`**[f7aced6 では `DOM`]** | 誤 FN（v2 で退行） |
| G5 | try/except でパス検証が再送出 | `DOM(strong-path→OP)` | `NODOM` | 誤 FN |
| G6 | 承認の例外が except で握り潰される | `NODOM(deny_reaches_effect)` | `NODOM` | 一致（回帰固定） |
| G7 | 内包表記の `if` フィルタ | `DOM(OP)` | `NODOM` | 誤 FN |
| G8 | CM 形の承認ゲート（`Gateway.require_approval`、木内解決可） | `DOM(USER)` | `NODOM` | 誤 FN |
| G9 | `contextlib.suppress` が承認を吸収 | `NODOM(deny_reaches_effect)` | `NODOM` | 一致（回帰固定） |
| G10 | ループ内 `continue` の allowlist | `DOM(OP, config-conditional 既定閉)` | `DOM` | 一致（回帰固定） |
| G11 | 主語不一致（`Gateway.is_allowed(self.default_tool)`） | `NODOM(non_binding_gate)` | **`DOM`** | **誤 clear（不健全）** |
| G12 | 効果が `finally` 側にある | `NODOM` | `NODOM` | 一致（回帰固定） |
| G13 | 木内で解決できないレジストリ（`Gateway.plugins.get(name)`） | `OPAQUE(dynamic_registry)` → UNKNOWN 行 | **未実測（コード読解からの推定）**。付録どおりのスニペットを `guard_dominance` に直接通すと `NODOM`。「無言に捨てる」は `analyze_target` の `if not lowered.get(wid): continue` に `skipped.append` が無いことからの推定。**第 1 週に links.json を手で作って端から端まで通し実測に置き換える** | **誤 clean（不健全）と推定** |
| G14 | 第 2 のユニット入口（無ガード）。`llm_loop` に**カタログ化 LLM 呼び出し（R1）を置くのは必須**（無いと trig が assumed になり期待 `GAP_SELECT` が原理的に出ない） | `NODOM(alt_entry)` → `GAP_SELECT` | **`guarded=True`（clear）** | **誤 clear（不健全）** |
| G15 | 最弱等級 / `req_occ` と `req_val` の分離 | `req_occ=OP`, `req_val(argv)=weak(no_dashdash)` → `GAP_INJECT`（規則 W） | **`guarded=True`（clear）** | **誤 clear（不健全）** |

前身が誤るのは **HEAD で 15 件中 11 件**（`f7aced6` では 9 件）、うち 4 件（G11/G13/G14/G15）は誤って clear ないし clean する不健全方向。一致する 4 件は回帰固定として残す。**この列は設計判断の背景であり論文には書かない。**

### 2.6 val エンジン（項目 B2。全仕様は `docs/val_design.md`）

Def 4 の `val` の実体。実装は `authgap/val/`、標準ライブラリ `ast` のみ、venv も型環境も使わない。要点のみここに記す。

- **値は三つ組 `Prin × Prov × Shape` に属性表と root 集合を添えたもの。** `Prin = {USER, OP, MODEL}`（Def 1 のラベル束）、`Prov = {resolved, opaque(r), remote}`（Def 1 の確度。**Prin 側に `UNKNOWN` を作らない**）。`Shape = Atom | Str(parts, tail) | Argv | Seq | Map | Path(base, segs, tail) | Obj(classes, fields) | Unknown`。
- **`Roots`** = その値が由来する MODEL 導入点（R1/R2）の集合。ユニット解析は位置行と別に **canonical-alias 表** `(root, site, transform)` を出す（`transform` ∈ realpath / `Path.resolve` / normpath+abspath / `urlparse.hostname` / `shlex.split` / `str.split→[0]` / `Path()` ほか）。**この表が Def 5 strong-path の前提である。**
- **`Obj` は型だけでなく `fields` を持つ**（カタログ化コンストラクタの実引数と、解析済みメソッドが `self.<name>` へ書いた値）。**ライブラリ コンストラクタ カタログ**（月 3 凍結）が `git.Repo(path→field "working_dir")`、`subprocess.Popen/asyncio.create_subprocess_*(argv0, shell → field "spawn")`、`sqlite3.connect(database)`、`httpx.Client(base_url)` を持つ。
- **heap のキーは受け手アクセスパス**（`"self"` 固定ではなく `"self._session"` のような深さ 2 までのパス）。読みと書きで同一のキー体系を使う。それ以上は `opaque(receiver)`。**これが無いと F6（OpenManus `Bash` の `self._session._process.stdin.write`）が出ない。**
- **文順の前向き走査。`ast.walk` は使わない**（BFS で文順を保証せず def-use に使えない。前身の `reaches_sink` / `_last_assign_rhs` がこれを使っており流用できない直接の理由）。ループは 2 周固定点 + widening。**`K = 16` は 5 種すべて（`Seq.elems` / `Map.entries` / `Str.parts` / `Argv.elems` / `Path.segs`）に適用する** — `cmd = cmd + " " + a` のループ内文字列構築が母集団で頻出し、`Seq`/`Map` だけを畳む widening では 2 周で安定しないため。**反証条件**: 較正 3 対と負例集合の実行で 2 周目と 3 周目の env がバイト一致しないユニットが 1 件でも出たら 3 周に上げるか当該ループ本体を `opaque(loop)` に落とす（3 周目を回して比較するデバッグ フラグを最初から入れる）。
- **入口仮引数の shape は注釈から種付ける**（`list[T]` → `Seq([], tail=MODEL)`、`dict[...]` → `Map`、その他 → `Atom(formal=Param(i))`）。注釈は文字列として読むだけで型環境は構築しない。**注釈由来の shape を使った位置は `shape_from = annotation` を記録し、注釈が嘘だった場合の FP を切り分けられるようにする。**
- **opaque は 8 分類**（`depth` / `unresolved` / `receiver` / `recursion` / `dynamic` / `cap` / **`loop`**（2 周固定点が安定しなかったループ本体） / **`context`**（ゲート条件が呼び出し元引数に依存し文脈非依存サマリでは決まらない形））。`remote` は別軸。**決して drop しない。決して clean に潰さない。決して MODEL に切り上げない。**
- **val 側の opaque 8 語とゲート側の `OPAQUE` 8 語は別語彙である。** 同じ語（`depth` / `unresolved`）が両方に現れるが、前者は値の解決に、後者は支配の判定に付く。manifest では `resolution` 列と `gate.reason` 列に分けて出し、混ぜて集計しない。
- **複雑度**: 関数サマリは `(関数, 受け手クラス)` で記憶化するので**解析コスト**は `O(Σ_{f∈F} n_f · K)` で深さに線形。**指数項は解析ではなく出力側に現れる** — 効果行は呼び出し点ごとに複製されるので `O(b^d)` になりうる。行数を実際に抑えているのは §5.2 の「出力効果行 200」cap である。**この cap に当たった率（`opaque(cap)` の内訳）を §6 の指標に出し、20% を超えたら深さを 2 に落とす。**
- **cap の予備計測（較正ではない）**: 前身ツリーの `.py` 4,340 ファイルで、ファイルあたり AST ノード数は中央値 206 / p95 2,945 / 最大 23,698、関数あたり中央値 54 / p95 298 / p99 643 / 最大 8,042。§5.2 の 20,000 ノード cap に当たるのは **3 ファイル（0.069%）**。**このコーパスは 85% が vendored pyre-check であってエージェントツール群ではないので、cap の較正根拠ではなく「桁が合っている」ことの smoke test にすぎない。** `K` と `SUMMARY_CAP=200` は第 1 週の probe（MCP サーバ 60 件）で確定し月 10 の指紋に凍結する。
- **文脈感度の限界（本文の限界節に書く）**: サマリは記憶化により**文脈非依存**である。「同一の効果サイトが呼び出し文脈によってゲート述語の真偽を変える」形（ゲート条件が呼び出し元から渡される引数に依存する形）は原理的に捉えられない。実例: doris-mcp-server `5923cc1^` の `utils/db.py:84 if self.security_manager and auth_context:` は同一サイトをゲートするが、`analysis_tools.py:384,393` と `schema_extractor.py:1150` は `auth_context` を省略 / `None` で渡す。**該当形は `opaque(context)` として出力し、決して clean にしない。**

#### 受け入れ fixture（10 件。期待行を行単位で `fixtures/val/expected.json` に pin する）

| # | 由来 | status | 期待行の要点 | この fixture が守るもの |
|---|---|---|---|---|
| F1 | 較正 A1 修正側 | 一次確認済み | `SPAWN@proxy(git.cmd.Git.checkout)`: `argv0=OP/lit="git"`、`argv[*]=MODEL/roots={branch_name}`、**`cwd=MODEL/canonicalised=false/roots={repo_path}`**、`alias_facts += (repo_path, validate_repo_path, Path.resolve)` | **root 集合と alias 表、および proxy カタログの ctor 引数 slot 束縛**。実コードは `repo = git.Repo(repo_path)` → `repo.git.checkout(...)` なので、型だけの解決では `cwd` が出ず Def 5(i) が付く先が無くなる |
| F2 | 較正 A1 脆弱側 | 一次確認済み（`9e5d5b8` は `a37158b` の祖先なので実 ref で成立） | F1 と**同一の位置行**、`alias_facts` が空 | 両側条件のタプル差が `alias_facts` の有無だけで表現できること |
| F3 | 較正 A5 修正側 | 一次確認済み | **`SPAWN@direct` を 2 行**出す（`shell` が `config-conditional` のとき slot 束縛が確定しないので `shell_string` 行と `argv[*]` 行の両方）。`exec_mode.shell = config-conditional(shell_command_control, default="allowlist")`。`alias_facts += (command_line, site, shlex.split→[0])` | 戻り値タプルの unpack、`IfExp` の join、`shlex.split` と `shell=` の相互作用、config atom |
| F4 | 較正 A5 脆弱側 | **未確定（合成 mutant）**。第 1 週に `git log -S` で確定するまで較正対として数えない | 位置行は F3 と同じ MODEL、`tokenised=false`、`exec_mode.shell = OP/lit=True`、alias transform が `str.split→[0]` | §9-2「修正がゲートを strong にしない対」— 差分が exec_mode と tokenised だけであることを行で示す |
| F5 | 負例 OpenManus `PythonExecute` | 一次確認済み | `EXEC@direct`: `code_text = MODEL/roots={code}/depth_used=1(INDIRECT)`。**負のアサート**: `INDIRECT` 表から `multiprocessing.Process` を外すと `opaque(unresolved)` になり **clean にはならない** | 間接 target 形。**`opaque` を clean に潰す退行を検出する唯一のテストなので必ず残す** |
| F6 | 負例 OpenManus `Bash` | 一次確認済み | 2 行。`SPAWN@direct`: `argv0=OP/lit="/bin/bash"`、`shell=OP/lit=True`。`EXEC@pipe`: `code_text=MODEL/roots={command}/**depth_used=1**` | **sink の第 3 形態 `pipe`、および heap の受け手アクセスパス**（`_BashSession.start` が `self._process` に書き `run` が読み、`Bash.execute` から見ればどちらも `self._session` の属性） |
| F7 | 負例 OpenManus `StrReplaceEditor` | 一次確認済み | 2 行。`FS_WRITE@direct(Path.write_text)` × 2（受け手 2 型は **witness の分岐**として分ける）。`witness_chain` に `execute → operator.write_file(LocalFileOperator) → Path(path).write_text`。片方は `resolution=remote`。`alias_facts += (path, validate_path, Path())` — **正規化ではない** | pydantic クラスレベル フィールド受け手、2 型受け手を 2 行に分けること、`remote` が行単位であること。**weak 理由 `absolute_only` / `existence_only` / `no_containment` を追加する根拠** |
| F8 | 負例 OpenManus `crawl4ai` | 一次確認済み | `NET@proxy(AsyncWebCrawler.arun)`: `url.host = MODEL/shape=Seq.tail/roots={urls}` | ループ内 append → 2 周固定点で `tail` に確定、**`ast.If` 文の `join_env`**（実コード 85–88 行は `if/else` **文**であって `IfExp` ではない）、`async with` のコンストラクタ型付け、キーワード引数束縛 |
| F9 | T3 代表 agno `ShellTools` | 一次確認済み | `SPAWN@direct`: `argv[*] = MODEL/roots={args}`、`argv0 = MODEL/shape=Seq.tail`、`cwd = config-atom(base_dir, default=None)/default-open`、`shell = OP/lit=False` | `__init__` kwarg 由来の config atom、リスト丸ごとが argv になる形、**注釈由来 shape の種付け** |
| F10 | 負例 定数ホストの HTTP ツール | **未確定**（木が未取得。第 1 週に checkout して URL 構築式を読んでから pin する） | `NET@direct`: `url.scheme=OP`、`url.host=OP/lit="restapi.amap.com"`、`url.path=OP`、`url.query=MODEL/roots={city}` | URL slot 分割規則。`url.host` が OP になることが「定数ホストの HTTP ツール → GAP 0」の唯一の機構 |

**URL の slot 分割規則（falsifiable な形で書く）**: `NET` の url 位置の値が `Str(parts)` で parts[0] がリテラルであり、そのリテラルが `://` を含みかつ `://` の後に `/`, `?`, `#` のいずれかを含むとき、`url.scheme` と `url.host` はそのリテラルから切り出し `principal = OP` とする。parts[0] が非リテラル、または権威部の終端がリテラル内に無いときは `url.host = 当該 part の principal`。**反証条件**: 較正/負例集合でこの規則が host を OP と誤ったケースが 1 件でも出たら「リテラル権威部でも `@` を含めば MODEL」に強化する。

---

## 3. 正直な限界（序論に書く）

**これは「一つの解析」ではない。「三つの別々に計算される座標の上の一つの判定」である。** trig、val、gate は伝播機構を共有しない。

統一の**唯一の証拠**は事前登録した**交差行数**。

- **測定手続き**: 3 腕のアブレーション。腕 A = trig を計算し val を全位置で OP に固定。腕 B = val を計算し trig を全て assumed に固定。腕 C = 完全版。**ゲートは 3 腕とも入っている。** 3 腕は**同一バイナリのフラグ違い**であること（別実装なら不合格）。3 腕の完全な verdict 表を evidence に残す。
- **行の verdict は集合である**: (unit id, effect, position) の行に対して出力された全 verdict の集合 `V(row) ⊆ {GAP_SELECT, GAP_INJECT, GAP_DRIFT, CONTRADICTION, INVENTORY, UNKNOWN}` を行の verdict とする。
- **交差行 = `V_C(row) ≠ V_A(row)` かつ `V_C(row) ≠ V_B(row)` を満たす行。** Def 7 では SELECT は trig にのみ、INJECT は val にのみ依存するので、**この条件を満たすのは同一行が SELECT 系と INJECT 系の verdict を同時に持つ場合に限る**。すなわち「MODEL セレクタから traced で到達されるユニット入口の下に、MODEL 値が weak validator しか通らない制御位置がある」形である。**これが統一の唯一の証拠形である。**
- **数える正当な形は 1 つのみ**（上記の同時保有形）。**第 3 版が挙げていた (i) callee の `confirm()` が SELECT を clear する / (ii) caller の承認 hook が `req_val` を引き上げる、は交差行ではない** — それぞれ腕 B のみ・腕 A のみとしか差が出ないので定義上 0 行になる。両者は `docs/intersection_rows.md` に「単一座標のゲート寄与」として**別表**で報告する。
- **`Leak`（Def 5-b）だけで説明できる行と `OPAQUE` 行は数えない。D だけで説明できる行も除く。**
- **閾値**: 交差行 **≥ 3**、かつ 3 行が**異なるプロジェクト由来**（**PraisonAI 全体を 1 プロジェクトとして数える**）。fixture 由来と自作ケーススタディ由来は数えない。1〜2 行なら「統一の証拠は逸話的」と書き、0 なら統一主張を取り下げて三部品として報告する。**閾値 3 に経験的根拠は無く、事前に固定することだけが根拠であると本文に明記する。**

**SELECT 座標の野外評価が成立しない可能性**: MCP サーバでは dispatch が framework 内にあるので trig は常に `assumed` になり、SELECT は原理的に発火しない。したがって野外母集団を MCP サーバだけにすると交差行は fixture と自作ケーススタディからしか出ない。対策は §6 の T3-app（第二母集団）。**traced 率が 20% 未満なら SELECT の野外評価は成立しないので、その時点で SELECT は fixture + ケーススタディのみの構造的主張に格下げする。この条項は撤回しない。**

**発生権限の第 2 の証人の探索（属性として）**: SELECT が主張しているのは「効果の発生権限が MODEL にある」ことであって「in-tree の dispatch を追跡できる」ことではない。原理的には Def 5-b の `Leak(g)` がこの主張の第 2 の証人になりうる。**しかし第 1 年時点でこれを verdict に格上げできる証拠は無い。** (a) 野外の発生ゲート保有率が構文的過大近似で 14.5%（露出ゲートは 0.0%、形態 4 の運用定義次第で 0〜41.5% を動く）、(b) kind 粒度では正当な読み取り経路が全て漏れになる、(c) 一次資料で確認した候補 5 件のいずれも両側 `Leak` 対にならない（詳細は §6 の S 群）。格上げ条件は Def 5-b に事前登録した。

---

## 4. カバー範囲

| クラス | 扱い | 機構 | 備考 |
|---|---|---|---|
| 1a 引数 → exec / path / SQL / HTTP | **両側評価** | R2 + val + gate | 主要な較正対（§6 の A1–A4、A7–A10、A15） |
| 1b LLM 出力をコード / クエリとして実行 | **原則として脆弱側のみ**。ゲート導入型の修正がある対は両側評価 | R1 + code_text / sql 位置 | 両側候補: A14 / A18（Langroid のグラフ DB と SQL）、B8（llama-index `safe_eval`）。片側 pin: B1（agno、修正で `eval` が消えるので**修正版を GAP 0 の負例 pin に使う**） |
| 1c 仕様として任意実行するツール | 対象 | 同上 | **凍結済み rubric 1c**（Def 7）。典拠は A6 と B5（修正が存在しない CVE、2 件とも一次確認済み） |
| 2 構造的に弱いゲート | **両側評価** | strong 3 系統 + weak カタログ | A5、A12–A13、A16–A17 |
| 2′ ゲート述語が汚染 | **測定現象 + 実 CVE 候補 1 件** | `tainted` / **`self_granted`** 格下げ | OpenHands agent-sdk の `security_risk`、CrewAI の fuzzy match。**doris-mcp-server CVE-2025-58337（2025 年 ID = 設計汚染なし）が `self_granted` の実 CVE 候補**（§6 の S1′） |
| 2″ sandbox fallback | 対 1 件 | ゲートされない局所 exec 経路 | Docker 不在時のローカル実行 |
| 選択（dispatch 証人） | **構造的評価が主**。実 CVE 対 1 件を補助に添える | trig traced + 連結経路の支配 | fixture、mutant、**3 ケーススタディ = gptme / SuperAGI（RESTRICTED）/ OpenHands-sdk**。比較の型は「出荷されている承認リスト vs 本ツールが合成した承認リスト」。**実 CVE 対 = A11（PraisonAI CVE-2026-44339、`selector-narrowing`）。ただし脆弱側の候補集合は `globals()` と `__main__` で静的に解決できないので Def 7 により脆弱側 verdict は `GAP_SELECT` ではなく `UNKNOWN(resolution=opaque)` である。A11 が示すのは「AuthGap が選択ハイジャックを GAP として名指しできる」ことではなく「UNKNOWN 行が実 CVE の上で発火し、修正で消える」ことである。この限定つきで書けば §11-6 に対する数少ない実データの反例になる。過剰に書くと審査で崩れる** |
| 選択（被覆漏れ） | **manifest 属性のみ**（verdict なし） | 発生ゲートの `Cov` / `Leak` | 格上げ条件は Def 5-b |
| 3 設定ファイル自己書き換え | 付録（属性のみ） | WRITE_POLICY 属性 | 主張しない |
| 4 間接注入 → 流出 | 付録（集合事実のみ） | read 集合 × MODEL 宛先 NET 集合 | 主張しない |
| 5 一般 web / デシリアライズ | **除外** | — | MODEL 主体が存在しない |
| 宣言矛盾 | D_kind が明示されている場合のみ | M vs annotations | **前測での明示率はエントリ基準 25.0%（camelCase のみ）、リポジトリのマクロ平均 25.5%、annotation 保有 repo 14/43。危険効果ユニット基準は分母の取り方で 39.7%〜11.4% に動くので前測では確定しない。脚注化の閾値は「F0a での、効果検出器の偽陽性クラスを除いた危険効果ユニット基準 10% 未満」とし、エントリ加重でも粗い分母でも判断しない** |

**クラス 3 と 4 は実装 0 週。** 既存の manifest 行から無料で読める範囲だけを付録に載せ、追加実装が必要と判明した時点で落とす。

**原理的に除外**: 一般分岐の制御依存、sandbox 内部の完全性、TypeScript、ホスト型クローズドエージェント、prompt injection そのものの検出。

---

## 5. ツールの実装

### 5.0 リポジトリ

- **Repo**: `~/Project/research/Master_Project/authgap`（新規 git repo、空から）
- **Python 3.10+**。解析中核は標準ライブラリの `ast` のみ。ハーネスでは `requests` 等を許可。依存は `requirements.txt` に固定。**解析対象の木には venv も型環境も作らない。**
- **レイアウト**: `authgap/`、`docs/`、`corpus/`（gitignore、`scripts/fetch_corpus.py` が生成）、`fixtures/`、`evidence/`（gitignore）、`tests/`、`scripts/premeasure/`
- **CLI**: `python -m authgap scan <path>` / `probe <path>`

### 5.1 成果物の形式

- `docs/cve_triage.csv` の列: `pair_id, cve_ids, ghsa_ids, repo, vuln_ref, fixed_ref, fix_commits, advisory_published, class, principal, two_sided, disappearance_reason, expected_tuple_change, required_sink_rows, weak_reason_needed, db_field_wrong, also_in_biflow_table3, verified_against, notes`
  - **`principal` 列が無いと、MODEL 主体を持たない対（Chainlit は USER 由来、PraisonAI `--mcp` は OP 由来）を混入させる。**
  - **`disappearance_reason` は 1 コミット 1 値ではなく (effect, position) 単位の値**として定義し、CSV では `;` 区切りの複数値を許す。両側成功の判定は「受理される理由が当該効果サイトに少なくとも 1 つあること」。根拠: A4 の修正コミット `0588ec09` は "bump vulnerable deps; harden git_add" で `dependency-bump`（N/A）と `normalisation-add`（○）が同居する。
  - **`advisory_published` は GitHub Advisory DB の `published_at` を採る**（CVE-2026-44339 は GitHub Advisory DB 2026-05-04、NVD 2026-05-08、reviewed 2026-05-11 と 3 つの日付がある。held-out を「月 6 凍結後に公開された advisory」で定義する以上、どの日付かを CSV のヘッダコメントに明記しなければ held-out 境界が反証不能になる）。
- `evidence/<run_id>/probe.json` のキー: `corpus_id, n_units, n_units_with_dangerous_effect, n_effects_by_kind, resolution{resolved,opaque,remote}, resolution_by_cause{depth,unresolved,receiver,recursion,dynamic,cap,loop,context}, rubric1c{n_units,n_units_without_validator}, registry_resolution_ratio, n_units_with_validator, validator_shapes, n_units_with_D_kind, n_units_with_D_dom_covering, n_units_with_D_op, n_units_with_D_prev_join, d_layer_unknown{enforcement,pattern,annotation_form}, enforcement_path_counts, dep_pin_resolvable{exact,lockfile,lower_bound_only,unreadable}, effect_fp_audit{db_only,db_only_non_db_execute}, traced_ratio, parse_failures, truncations`
  - **`traced_ratio` は A5（F0a）の run では `null` とし、その run には二度と書き込まない。** traced 率は B1 完了後に **新しい `run_id` で probe を再実行**して得る（F0a は最初の run、traced 率は 2 回目の run から報告し、両方を evidence に残す）。**凍結済み run ディレクトリを後から書き換えない。**
- `evidence/<run_id>/` にはこのほか `manifest.json`、`results.sarif`、`fingerprint.json`、`stdout.log` を置く。加えて `fixtures/gates/expected.json`、`fixtures/val/expected.json`、`fixtures/dominance_mutants/`、実装変異の生存表、`docs/verification_log.csv` を成果物一覧に含める。**これ以外は evidence に数えない。**
- `docs/manifest.schema.json`（JSON Schema）を manifest の採点前に書く。**gate 欄は真偽ではなく `(3 値 verdict, grade, reason, witness 行)` になるので、schema を先に更新する。**

### 5.2 manifest とその他

**manifest 行**: ユニットごとに `(effect kind, site, form(direct|proxy|pipe), slots→principal, trig(traced|assumed), req_occ, req_val, gate(DOM|NODOM|OPAQUE)+grade+reason+witness行, resolution, covered_by, D_layer_present, cov_gate, gate_default, leak_reason, leak_scope, shape_from, alias_mismatch)`。

**SARIF**: witness 付き。**witness テンプレートは weak 理由ごとに全部決める。**

| reason | witness |
|---|---|
| `first_token` | `ls; …` |
| `split_colon` | `allowed.com:@evil` |
| `prefix_no_canon` | `<allowed_root>/../etc/passwd` |
| `prefix_no_boundary` | `<root>_evil/x`（`root` の兄弟で前置一致する名前） |
| `no_containment` | 絶対パス `/etc/passwd` |
| `no_symlink_resolution` | `<root>/link → /etc`（**シンボリックリンク。`../` ではない**） |
| `no_dashdash` / `no_dash_reject` | `--upload-pack=touch /tmp/x` のようなフラグ様のファイル名 |
| `fuzzy_name` | allowlist 名から 1 編集距離の名前 |
| `docker_fallback` | 同じ argv を docker 不在で実行しローカル分岐を示す |
| `post_check_append` | 検査後に MODEL 要素が連結される箇所（`base` を検査し `base / name` を開く形。値ではなく行を示す） |
| `no_existence_check` | 名前空間に存在しない値（存在しないブランチ名 / リビジョン） |
| `underscore_denylist` | 拒否語彙に載っていない dunder（`__class__` 経由の到達など） |
| `lexical_canon_only` | シンボリックリンク（`no_symlink_resolution` と同形。両者の差は包含述語の有無であって witness ではない） |
| `fail_open` | ゲートが未認識と判定する入力（未知のラッパ、`bash -lc` 等） |
| `denylist_enum` / `regex_denylist` | 拒否語彙に載っていない同義構文 |
| `regex_no_canon` | 引用識別子 / インラインコメント / スキーマ修飾 |
| `validate_then_fetch` | 検証を通す初期 URL からのリダイレクト先 |
| `self_granted` | ゲート述語が読む権限コンテキストを局所で構成している箇所（値ではなく行を示す） |

**`self_granted` は weak 理由語彙（19 語）ではなく共通の格下げ属性である。** 本表には載せるが manifest では `weak_reason` 列ではなく `downgrade` 列に出し、Def 5 の 19 語の凍結対象には含めない。

witness は effect view が shell 文字列 / 生パス / 生 URL のときのみ出力する。argv モードの SPAWN には `no_dashdash` witness は出すが `first_token` witness は出さない。

**annotation patch**: CONTRADICTION 行の直列化のみ。**ポリシー emitter は作らない。**

**unit id**: `framework:qualified_name:schema_hash`。`schema_hash` = 静的に得られる入力スキーマの正規化 JSON の sha256 先頭 12 桁。**ファイル移動には安定。rename とスキーマ変更は diff で delete+add として現れる。したがって D_prev は rename を跨いだ drift 主張をしない。**

**決定論**: ソート済み走査。**cap は 1 ファイルあたり AST ノード 20000 と出力効果行 200 のいずれか先に当たる方、壁時計 10 秒、`K=16`（コンテナ / 文字列 / パスの要素上限）、`SUMMARY_CAP=200`（1 ユニットあたりサマリ数）、1 関数 2000 CFG ノード。** cap に当たったら `TRUNCATED` 行を 1 本出し、ファイル名・当たった cap・件数を記録する。cap は月 10 の指紋に含み以後変更しない。parse 失敗は行として出す。

**3 回一致の定義**: manifest から volatile ブロック（実行時刻、経過時間、絶対パス）を除き、キーをソートして再直列化したうえでのバイト一致。volatile はトップレベルの `run_meta` に閉じ込める。不一致はユニット id と最初に異なる JSON ポインタで報告する。

**主ユーザ**: Python MCP サーバ / ツールパッケージの**保守者**。第二: ホスト設定を D として入力できるアプリ運用者。**採用の主張はしない。**

---

## 6. 評価設計

### F0 — 床（最優先。2 段に分ける）

**F0a（真の床、支配判定に依存しない）**: ユニットごとの危険効果 kind の真偽値、**構文的 validator 形状**（下の語彙定義を参照）、config atom と既定値、annotation の有無、**ゲート述語の存在（支配判定なし）**。

**構文的 validator 形状の語彙（本節が唯一の定義点。月 3 凍結。§0 と §10 はここを参照し語彙を再掲しない）**: `realpath`（`os.path.realpath` / `Path.resolve`）、`lexical_canon`（`normpath` / `abspath`）、`containment`（`commonpath` / `is_relative_to` / `Path.relative_to`）、`prefix`（`startswith`）、`urlparse`（`urlparse` / `urlsplit` / `.hostname`）、`shlex_split`、`shlex_quote`、`shlex_join`、`split`、`ctor_path`（`Path(...)`）、`exists`（`os.path.exists` / `Path.exists` / `rev_parse` 型の存在検証）。**11 語。**（第 3 版は §0 で 7 語、§6 で 8 語、§10 で別の 8 語と 3 通りに書き、しかも 3 つとも `Path.resolve` と `relative_to` を欠いていた。A1 の修正版はその 2 つだけで構成されるので、旧語彙では脈拍が A1 を判別できない。）

母集団は 60 MCP サーバ + 30 ツールパッケージ、**機械抽出。人手照合は無作為 20 ユニットの抜き取りのみ**（第 2 版は F0a 行に「二重ラベル」、標本設計に「機械抽出、人手ラベルなし」と書いており矛盾していた。人手の二重ラベルは T3-tool の 60 ツールにのみ課す）。

**F0a に追加する 5 次元**（すべて機械抽出）: (i) D_kind の明示フィールド集合（辞書アンパック形と snake_case 別名を含む）、(ii) D_dom の値域語彙と被覆判定の結果（制御位置に限る）、(iii) 執行表による経路判定と依存版の可読性（`dep_pin_resolvable`）、(iv) `.claude/settings.json` / exposure ファイルの有無と帰属、(v) 静的に取得できるリリース数と unit id の join 率。加えて **(vi) §2.5.1 の CFG 構文の出現率**（実装順を決めるため）と **(vii) 発生ゲート保有率の 4 形態別内訳**。

**F0b**: F0a + ゲートの支配判定。支配判定の完成後。

**F0c（前身の 4 条件を新規に測る、null 時の第 3 章）**: 母集団は **60 サーバ + 8 アプリ**（§7.3 で T3-app を 15 → 8 に切り詰めた変更を反映）。**2 回に分けて測る。**
- **F0c-1（A5 の run で測る）**: (iii) ツール本体が別プロセス / HTTP の向こうにある率 = `resolution.remote`、(iv) 無ガードのシェル実行が仕様である率。**(iv) はユニット行を要するので probe.json に集計キー `rubric1c{n_units, n_units_without_validator}` を追加する。** manifest.json は B5 の成果物なので A5 の時点では使えない。
- **F0c-2（B1 完了後の 2 回目の probe run で測る）**: (i) dispatch キーが in-tree で解決する率（`traced_ratio` + `registry_resolution_ratio`）。**F0c の完成は B1 完了時点である。**
- **(ii) framework 境界で型が消える率は AuthGap では測定不能**（型環境を構築しないため）。**別の量を (ii) の名前で報告してはならない。** §1 が F0c に負わせている callee 側反転の正当化は (i)+(iii) と §1.5 で行う。
- **(i)(iii)(iv) は probe.json の既存キー（+ 上記 `rubric1c`）のみから導出でき、新規の解析器コードが 0 行、集計スクリプトが 60 行以下であること。**

**負の結果章を論文に載せないので、null 時の論文は F0 + T1 の対ごと表 + F0c の 3 部品で審査に耐える厚みが要る。F0 の標本（60+30）と次元数はこの前提で決めており、縮小は不可。**

### 標本設計（1 つに統一する）

**解析と labelling の単位はツールであってサーバではない。**

- F0 は 60 MCP サーバ + 30 ツールパッケージを効果 / validator / annotation の水準で覆う（機械抽出）。
- **T3-tool**: 同じ 60 サーバのツールから seeded random で 60 ツール（1 サーバあたり最大 2）。この 60 ツールを 4 次元で二重ラベルする。
- **T3-app**: in-tree dispatch を持つエージェントアプリを第二母集団として seeded random で選ぶ。**§7.4 の切り詰め順序 (1) を前倒し適用して 8 件とする**（§7.2）。**traced 率を先に測る**（§3）。
- probe（項目 A5）は同じコーパスで走らせる。別抽出にしない。
- **LLM baseline は削除した**（§7.3）。「固定プロンプトの LLM レビューより優れる」は主張しない。審査で問われたときの答は精度ではなく出力形式（決定性・witness・宣言照合）の違いである。

### T1: 両側対（CVE 対 / GHSA のみ / advisory 無しを分けて数える）

**ペアは修正コミット単位で数える。ID 単位では数えない。** 同一の修正コミットが複数の advisory を閉じる場合（A9 と A10）は **1 対**として数え、行は 2 本残す。

#### T1.1 両側条件の定義

「修正版で報告しない」ではなく、**「報告される (effect kind, site, position, val 主体, gate grade, weak reason, req_occ, req_val, exec mode, DISPATCH 候補集合の resolution) のタプルが、修正版で事前登録どおりに変化する」**。

> **両側成功に数えるのは、脆弱版と修正版の両方に同一の効果サイトが存在し、変化が (effect kind | val 主体 | gate grade・reason | req_occ | req_val | exec mode | DISPATCH 候補集合の resolution) のいずれかで起きた対に限る。**

`effect kind` を座標に入れるのは A3（`FS_WRITE` → `SPAWN`）が自分の定義で落ちないようにするためである。

**消滅理由の語彙（月 6 凍結）と採点上の扱い**

| 消滅理由 | 内容 | 両側成功に数えるか |
|---|---|---|
| `validator-add` | 制御位置に値検証が追加された | ○ |
| `normalisation-add` | 正規化子または境界述語が追加・強化された | ○ |
| `approval-add` | 承認割り込みが効果をゲートするようになった（`req_occ` 引き上げ） | ○ |
| `selector-narrowing` | DISPATCH の候補集合が動的解決から宣言集合に縮んだ | ○（SELECT 対のみ） |
| `principal-demotion` | 制御位置の値の出所が MODEL/USER から config atom に移った | ○ |
| `exec-mode-change` | ゲート等級は不変で実行モードだけが変わった（`shell=True` → argv） | ○ |
| `sink-substitution` | 効果サイトは残り sink 行が別の行に変わった | ○（両版の sink 行が sink 表にあり、かつ kind か val 主体が変わる場合のみ） |
| `denylist-broadening` | 拒否語彙・拒否正規表現の網羅範囲だけが広がった | **×（N/A）。等級も理由も不変なので Def 5 では判別不能** |
| `parser-coverage` | ゲート述語は不変で、シェル/SQL パーサが解ける表記が増えた | **×（N/A）。Def 5 は述語の形状を採点しパーサの網羅率を採点しない** |
| `redirect-rescope` | 検証子は不変で適用回数・適用点だけが変わった（1 回 → hop ごと） | **×（N/A）。`allow_redirects` の意味論はモデル化しない** |
| `tool-delete` / `feature-removal` | 効果サイトそのものが消えた | ×（N/A。負例 pin に使う） |
| `dependency-bump` | 依存更新のみ | ×（N/A） |
| `sink-removal` | 効果 kind が消えた | ×（N/A。修正版を GAP 0 の負例 pin にする） |
| `no-fix` | 修正コミットが存在しない | ×（片側のみ。rubric 1c の典拠に使う） |

各対について**期待タプルを採点前に `docs/cve_triage.csv` の `expected_tuple_change` 欄に凍結する**。

**この改訂の位置づけ**: 消滅理由の語彙拡張と効果サイト条件は、**解析器がまだ 1 行も出力していない着工前の時点で行った改訂であり、採点結果を見て緩めたものではない。** 事前登録文書に改訂日と改訂前（validator 追加 / 正規化追加 / 承認割り込み追加の 3 者限定）・改訂後の文言を両方残す。緩めた実質的理由は 1 つで、**選択の修正は原理的に validator 追加ではありえず、3 者限定は SELECT の両側対を定義上ゼロにしていた**ことである。

**副次指標（必須）**: 両側通過対のうち、**修正版で verdict が GAP から外れる対の数（verdict-clearing 数）を必ず併記する。** タプル変化のみで通過した対（A5 の exec-mode-change、A7 の weak→weak）と区別せずに報告すると「修正を検出した」と誤読される。規則 W がある以上、weak が残る修正版は GAP のままである。

#### T1.2 較正対（修正コミットを自分で確定済み）

`vuln_ref` / `fixed_ref` は、**advisory の記載を信用せず**、公開クローン上で `git log -S<識別子> -- <path>` と `git show` により当該 validator に触れたコミットを特定し、その親を脆弱側 ref としたものである。`fixed_ref` はすべて実物の diff を目視確認した。**SHA・diff の内容・`db_field_wrong` は一次確認済み。CVE / GHSA 番号・公開日は二次情報（ローカル保存の GitHub Advisory API / OSV JSON）であり、第 1 週に advisory ページで再確認する**（例外: GHSA-gmjg-hv98-qggq と GHSA-g84q-54hf-36rg は一次資料で確認済み）。

**主較正（MODEL 主体・効果サイトが両版に存在・受理される消滅理由）**

| id | 対象 | advisory | vuln_ref → fixed_ref | class | 消滅理由 | 期待タプル変化 |
|---|---|---|---|---|---|---|
| A1 | mcp-server-git `repo_path` 封じ込め | CVE-2025-68145 | `9e5d5b8e` → `a37158bc` | 1a | normalisation-add | `weak(prefix_no_canon)` → `strong-path`（`resolve` + `relative_to` を ValueError 捕捉）。**ゲートは `call_tool` ディスパッチャに置かれる**ので連結経路の支配判定を直接試験する |
| A2 | mcp-server-git フラグ混入（CWE-88） | CVE-2025-68144 | `d9c45477` → `9e5d5b8e` | 1a | validator-add | `weak(no_dash_reject)` → `strong-token`（`startswith('-')` 拒否 + `repo.rev_parse` 存在検証） |
| A3 | mcp-server-git `git_add` 木外パス | CVE-2026-27735 | `dcb47d2d` → `db960508` | 1a | sink-substitution | `FS_WRITE(index.add, gate 無し)` → `SPAWN(argv0="git", shell=False, "--" あり)`。**proxy 行が無いと修正版が無言になる** |
| A4 | mcp-server-git `git_add` 後追い硬化 | 無（2026-06-14） | `275175cd` → `0588ec09` | 1a | dependency-bump;normalisation-add | `strong-token` → `strong-token + strong-path`。**1 コミットに N/A 理由と ○ 理由が同居する実例** |
| A5 | AutoGPT シェル allowlist 先頭単語 | CVE-2024-1881 | `1f1e8c9f` → `5090f55e` | 2 | exec-mode-change | `(weak(first_token), SPAWN(shell=True))` → `(weak(first_token), SPAWN(shell=False, argv))`。**修正版も weak のまま** |
| A7 | PraisonAI `FileTools._validate_path` | CVE-2026-35615 | `3e29936e` → `d80bff2d` | 1a | normalisation-add | **`weak(no_containment)`**（`'..'` 検査は生きているが包含述語が存在せず、絶対パス `/etc/passwd` が通る）→ `weak(prefix_no_boundary)`（`realpath` は入ったが照合が `absolute.startswith(os.getcwd())`） |
| A8 | 同上の後追い | 無 | `d80bff2d` → `66932746` | 1a | normalisation-add | `weak(prefix_no_boundary)` → `strong-path`（`commonpath(...) == cwd`）。**PraisonAI 上限により算入しない**（親は `142db6c5`。`d80bff2d..66932746` は 85 コミット離れている） |
| A9 | PraisonAI `ast_grep_rewrite` に承認欠落 | CVE-2026-55530 | `9991e00f` → `2f9677ab` | 選択/承認欠落 | approval-add | `req_occ(SPAWN("sg … --update-all"))` : `MODEL` → `USER`（`@require_approval(risk_level="high")` 付与）。**唯一の検証済み approval-add 対** |
| A10 | PraisonAI `is_path_within_directory` の symlink | CVE-2026-55540 | `9991e00f` → `2f9677ab` | 1a | normalisation-add | **`weak(no_symlink_resolution)`**（`abspath` + `root+os.sep` 前置。境界は正しいがシンボリックリンクで脱出）→ `strong-path`（`realpath` + 同一述語）。**A9 と同一修正コミットなので A9 と 1 対** |
| A11 | PraisonAI `ToolExecutionMixin.execute_tool` の名前解決 | CVE-2026-44339（**一次確認済み**。CWE-470、≤4.6.36 → 4.6.37） | `7a7df247` → `0cec9fd1` | **選択ハイジャック** | selector-narrowing | `DISPATCH(callee)` の候補集合が `declared ∪ registry ∪ globals() ∪ __main__`（`resolution=opaque`, `trig=(MODEL, traced)`, `req_occ=MODEL`）→ `declared ∪ registry`（`resolution=resolved`）。**脆弱側 verdict は `UNKNOWN(opaque)`**（§4 の注） |
| A12 | Langroid SQL ブロックリスト網羅漏れ | CVE-2026-50180 / GHSA-pmch-g965-grmr | `56e2756e` → `00b7dd7b` | 2 | **denylist-broadening** | **等級・理由とも `weak(denylist_enum)` のまま。両側採点に数えない（N/A）**（per-name → family regex の拡張） |
| A13 | Langroid ブロックリスト正規表現回避 | CVE-2026-54760 / GHSA-6xc5-4r68-67fc | `6e8e7b2b` → `59b73487` | 2 | normalisation-add | `weak(regex_no_canon)` → `weak(denylist_enum)`（sqlglot AST 走査による正規化後照合。**修正版も denylist であり strong ではない**）。**`sqlglot` を Def 5 の正規化子カタログに載せた場合に限り算入する** |
| A14 | Langroid Neo4j/Arango 検証欠如 | CVE-2026-55615 / GHSA-2pq5-3q89-j7cc（**修正コミット本文が Advisory 行で明記**） | `deb79824` → `5a3097d9` | 1b | validator-add | ゲート無し（bottom = MODEL）→ `config-conditional(allow_dangerous_operations, default=False)` + `cypher_validator`/`aql_validator`。**1b でゲート導入型、かつ既定閉 config atom の実例** |
| A15 | qwed-mcp `verify_math_expression` | CVE-2026-55546 / GHSA-mw6r-2hvm-4rp2（コミット本文が GHSA を明記） | `54ac6826` → `362e6189` | 1a | validator-add | `EXEC(code_text)` ゲート無し → `weak(記号 allowlist + 拒否語彙)`（`__builtins__` 剥奪）。**strong-eval を実装した場合のみ `strong-eval`。実装しなくても両側判別できる** |
| A16 | crewai-tools リダイレクト先 SSRF | CVE-2026-62240 | `b6fbe078` → `5d4851ea` | 2 | **redirect-rescope** | **脆弱版も `validate_url(website_url)` が `requests.get` をゲートしている。修正版は `safe_get` 経由で同じ `validate_url` を hop ごとに呼ぶだけで Def 5 の等級は不変。両側採点に数えない（N/A）** |
| A17 | Omnigent シェルポリシ parser の fail-open | CVE-2026-62676 | `7ca0cca3` → `1a05b7b1` | 2 | **parser-coverage** | **修正コミット本文が "This is parser broadening, not a blanket abstain->deny … must keep abstaining on non-git/gh commands" と明言しており、修正版も abstain=ALLOW のまま。両側とも `weak(fail_open)`。両側採点に数えない（N/A）** |
| A18 | Langroid SQLChatAgent が LLM 生成 SQL を無検証実行 | CVE-2026-25879 / GHSA-mxfr-6hcw-j9rq | `763d5cba` → `60933b48` | 1b/2 | validator-add | ゲート無し（bottom = MODEL）→ sqlglot による文型 allowlist（既定 SELECT のみ）。**`sqlglot` 不在時は fail-closed** で A17 の `fail_open` に対する自然な負例対照になる。件名が CVE 番号を明記。tag `0.63.0~1` |

**片側・除外・要検証（B 群）**

| id | 対象 | 扱い |
|---|---|---|
| A6 | AutoGPT `/bin/./whoami` denylist 回避（CVE-2024-6091） | **修正なし**（一次確認: GHSA-g84q-54hf-36rg が "Patched versions: None"、HEAD の `code_executor.py` も `shlex.split(cmd)[0]` のまま）。両側対に数えない。rubric 1c の典拠 |
| B1 | agno `eval(field_type)`（CVE-2026-35002、`ea35f135` → `cbf67552`） | 片側 1b。修正版は `eval` が消えるので `sink-removal`。**修正版を「GAP 0」の負例 pin に使う** |
| B2 | PraisonAI `list_files` の glob（CVE-2026-40152、`26e8f5ba` → `245a2d11`） | 両側可。ただし DB 誤り例（下記） |
| B3 | Chainlit MCP stdio（CVE-2026-45018 / CVE-2026-45019、`b8506a47` → `0565fd0e`） | `fullCommand` は**クライアント（USER）由来で MODEL 主体ではない**ため既定モードでは対象外。**`--hosted` 感度分析の唯一の実 CVE 対**。修正は `principal-demotion` |
| B4 | PraisonAI `--mcp` コマンド注入（CVE-2026-34935 / CVE-2026-41497） | `--mcp` は CLI 引数 = OP 由来。**除外（`no_MODEL_principal`）**。`StdioServerParameters` 行の実装確認にのみ使う |
| B5 | Upsonic MCP allowlist 回避（CVE-2026-30625） | **修正なし**。advisory が指す `855053f` は 25 ファイル 4831 挿入の機能追加コミット |
| B6 | browser-use `domain.split(':')[0]`（CVE-2025-47241） | **第 2 版の「0.1.44 は存在しない」は誤り。** `git rev-parse 0.1.44` = `751b0435`（2025-05-02）で tag は実在し、0.1.45 の祖先で、`context.py` の `split(':')` を**まだ含む**。PyPI にのみ 0.1.44 が無い。**git ref で pin する本表では `vuln_ref = 0.1.44`** |
| B7 | LangChain file-search middleware（CVE-2026-55443、`dcaf7795`） | 第 1 週に検証。advisory 本文が「path-segment 境界のない prefix 比較」を明記しており `prefix_no_boundary` の 2 例目 |
| B8 | llama-index `safe_eval` 迂回（CVE-2024-3098 / CVE-2024-3271） | 第 1 週に検証。`strong-eval` を実装しない場合でも「ゲート無し → weak(underscore_denylist)」で両側判別できるかを確認する |
| S1′ | doris-mcp-server（CVE-2025-58337 / GHSA-m35w-xx8c-6xc7、`5923cc1^` → `5923cc1`） | **クラス 2′（`self_granted`）の候補。SELECT の対ではない。** 一次読解の結果、MCP 経路（`tools_manager:1372` → `schema_extractor:1456` → `query_executor:539` → `db.py:745`）は `auth_context` を渡したままゲート `db.py:84` に到達しており、`Leak(g) = ∅`。実際の欠陥は MCP 経路が `MockAuthContext`（`permissions=["read_data","execute_query"]`）を自作してゲート述語の被演算子を自己付与すること。修正はこれを実 `AuthContext(roles=["read_only_user"])` に置換し、`config.security.enable_security_check`（`config.py:86` 既定 `True` = 既定閉）下の前置検査を挿入する。**両版とも同じ拒否語彙検証器を通るので、`self_granted` を Def 5 に足さなければタプルが変化しない。反証条件 F-5: 第 1 週に `self_granted` を入れても両版のタプルが同一なら本対は両側対から落とし、クラス 2′ の動機付け例としてのみ引用する。** また `@mcp.tool` 入口から DB sink まで**手続き間 10 ホップ**あり Def 4 の深さ 3 では届かない |
| S2 | mcp-neo4j-cypher（CVE-2026-35402 / GHSA-x3cv-r3g3-fpg9、`4d3454d^` → `4d3454d`） | **INJECT 側の予備候補。** 脆弱側は `read_neo4j_cypher` が `ToolAnnotations(readOnlyHint=True, destructiveHint=False)` を明示しながら `_is_write_query` の正規表現否定（`\b(MERGE\|CREATE\|INSERT\|SET\|DELETE\|REMOVE\|ADD)\b`）だけで `DB(sql=MODEL)` に到達 → `GAP_INJECT(sql)=weak(regex_denylist)` ＋ `CONTRADICTION`。修正は判定を DB への `EXPLAIN` に移すので `opaque(remote)`。**strong にはならない**（AutoGPT と同型）。`read_only` の既定は両版とも `False` なので被覆漏れ側は両側にならない |
| S3–S5 | mcp-memory-service CVE-2026-49291 / aws-api-mcp-server CVE-2026-16584 / praisonai CVE-2026-57142 | いずれも被覆漏れの動機付け例。S3 のゲートは FastAPI の DI 引数既定値（`Depends(require_write_access)`）で Def 5-b の 4 形態に当たらず、入口が REST ルートで R2 ではないので `Cov(g) = ∅`。S4 は単一ゲートの既定開放で `config-conditional(default=open)` として扱える（**SELECT ではなく `req_occ` 側**）。S5 は YAML 駆動で AST の射程外。**§1.5.7 と序論の動機付けにのみ使う** |

#### T1.3 検証で判明した事実（§9 の根拠をここに固定する）

1. **脆弱性 DB の fix commit 欄が誤っている実例（4 件、いずれも一次確認済み）**
   - AutoGPT CVE-2024-1881: DB 記載 `26324f29` は `.env.template` の 4 行変更。実際の修正は `5090f55e`（PR #6903, 2024-02-27）。**2 名の検証者の見解相違はこれで確定した。**
   - AutoGPT CVE-2024-6091: DB 記載 `ef691359` は docs 2 行の追加。修正ではない。
   - mcp-server-git CVE-2026-27735: DB/advisory は merge commit `862e717` を指すが、実体は `db960508`（`862e717` の第 2 親の祖先であることを確認）。
   - PraisonAI CVE-2026-40152: DB は `1.5.128` を patched とするが、タグ `v4.5.128` の `list_files` は `pattern` 未検証のまま。実際の validator は 12 日後の機能コミット `245a2d11` に入る。
2. **修正が存在しない CVE（2 件）**: AutoGPT CVE-2024-6091、Upsonic CVE-2026-30625。rubric 1c の議論に使う。
3. **修正がゲートを strong にしない対（2 件）**: A5（実行モードのみ変化）、A7（`realpath` は入ったが照合が素の `startswith` のまま）。**両側条件をタプルの変化で定義している理由がこれである。**
4. **修正コミットの探索ヒューリスティック（3 つ）**: (a) mcp-server-git・Langroid・Chainlit ではセキュリティ修正が単一親の `"Merge commit from fork"` として着地する（GitHub の private fork 運用）。`git log --grep='Merge commit from fork'` を triage の第一手にする。**ただしプロジェクト依存**（実測: mcp-servers 2 / langroid 6 / chainlit 1 / autogpt 17 / **praisonai 0 / crewai 0 / agno 0**）。(b) **PraisonAI では逆に、修正が `"Release vX.Y.Z"` という無関係な変更を多数含む squash コミットに埋まる**ので、必ず `-S` でファイルとシンボルを絞る。(c) **Langroid では修正コミットが patched tag のちょうど 1 つ前に着地する**（`git describe --tags --contains` が `0.63.0~1` / `0.64.0~1` / `0.65.1~1` / `0.65.5~1` を返す）。`git log -S` と併用して ref を相互検証する。
5. **advisory の「公開日」は 1 つではない**。CVE-2026-44339 は GitHub Advisory DB 2026-05-04 / NVD 2026-05-08 / reviewed 2026-05-11。**本表は GitHub Advisory DB の `published_at` を採る**（§5.1）。
6. **browser-use 0.1.44 は git tag としては存在する**（`751b0435`、2025-05-02、0.1.45 の祖先、脆弱コードを含む）。PyPI にのみ無い。第 2 版の記述は誤りだった。
7. **修正コミットの実在確認と、両側判別可能性の確認は別作業である。** 第 2 版は 3 対（A12・A16・A17）を、Def 5 が等級を動かせないにもかかわらず両側成功に数えていた。いずれも「修正コミットは実在し diff も正しい」が「AuthGap の座標では脆弱版と修正版が同一タプルになる」型である。**triage の各行で後者を独立に検査する手順を第 1 週に組み込む。**

#### T1.4 母集団の偏りに対する上限

検証済み較正対のうち 5 対（A7–A11）が単一プロジェクト（MervinPraison/PraisonAI）由来で、そのコミットの相当数が AI エージェントによる自動生成である。

- **T1 の合格数に算入する PraisonAI 由来の対は、あらかじめ A11・A9(+A10)・A7 の 3 対に固定する。A8 は表に残して算入しない。**（採点後に選べる形にすると事後選択になる。）**上限 3 に経験的根拠は無く、事前に固定することだけが根拠であると本文に明記する**（§3 の交差行閾値 3 と同じ扱い）。
- **§3 の交差行の「異なるプロジェクト由来」は、PraisonAI 全体を 1 プロジェクトとして数える。**
- A7–A18 はいずれも 2026 年の ID または非 CVE の後追いコミットであり、**本作業で弱理由語彙・`self_granted`・`strong-eval` を導出する際に参照している。したがって全て設計汚染済み較正である。held-out 層は依然として空であり、月 6 のカタログ凍結後に公開された advisory でのみ埋める。** 較正対を増やしたことで held-out 層の空白が相対的に目立つようになった点は本文に書く。

#### T1.5 合格条件（事前登録、3 つとも必要）

- (i) 修正コミット単位で **≥ 6 対**が両側通過する。**算入可能な検証済み候補は 11 対**（内訳: mcp-server-git 4〔A1–A4〕、AutoGPT 1〔A5〕、PraisonAI 3〔A7・A9+A10・A11。上限適用後〕、Langroid 2〔A14・A18〕、qwed-mcp 1〔A15〕）。**A12・A16・A17 は等級不変のため算入しない。A13 は sqlglot を正規化子カタログに載せた場合のみ +1。A8 は PraisonAI 上限で算入しない。** 余裕は 5 対。
  - **内訳を必ず併記する: CVE 付き 10 対、advisory 無しの後追い硬化 1 対（A4）。「CVE 対 11 件」とは書かない。**
  - **注**: 第 2 版は「較正候補 5 対」、本作業の中間版は「検証済み 13 対」としたが、いずれも再導出できない。11 対は A12/A16/A17 の除外と A18 の追加を反映した再導出値である。
- (ii) そのうち **≥ 2 対**で、同一 source 設定の Semgrep OSS と Pysa ModelQuery が修正版を clear できない。**加えて MCP-BiFlow の公表結果と対ごとに並べ、AuthGap が追加で示すものが (effect kind, position, gate grade, weak reason, exec mode) のタプル変化であることを明示する**（§1.5.1）。(ii) を満たす対が 0 なら「貢献は source 設定の提案であり静的解析の新規性は主張しない」と本文に書く。
- (iii) 通過対が **≥ 4 プロジェクト**にまたがる。1〜2 プロジェクトに偏った場合は「較正はプロジェクト特異的である」と本文に明記し、野外評価の結論に較正結果を引き継がない。

#### T1.6 採点集合と予備集合（費用制御）

検証済み対のうち、**pin 済み checkout を作り項目 C1 の回帰母集団に常駐させるのは採点集合 8 対のみ**とする。

- **採点集合**: A1, A2, A3, A5, A7, A9(+A10), A11, A15（4 プロジェクト、合格条件 6 に対し余裕 2）。
- **予備集合**（`docs/cve_triage.csv` に SHA と期待タプル付きで残すが、pin と行単位の期待値凍結には入れない）: A18, A14, A4, A13（条件付き）, A8（上限で算入不可）。
- **事前登録した補充順序**: A18 → A14 → A4 → A13。合格条件 (iii) のプロジェクト数を優先するため A18（Langroid、5 番目のプロジェクト）を先頭に置く。
- 理由: 対 1 件につき木が 2 本。回帰母集団に常駐すると項目 C1 と D1 が対数に比例して増える。

### T2: mutant

**較正 mutant と held-out mutant を分けて報告する。**

- 較正: 前身の diffbench 由来のものは**設計汚染済み**として扱う（弱理由の語彙が Def 5 と同じ）。
- held-out: **生成器のコード（B4）は月 6 のゲート語彙凍結の前にコミットし、生成の実行は凍結後に行う。** langchain-community / crewai-tools のパス系・シェル系から新規生成する非 CVE 由来 mutant のみ。
- 操作: realpath 除去、startswith 化、`split()[0]`、`--` 除去、shell=True、Docker fallback 追加、**`commonpath`/`relative_to` を `startswith` に落とす（`prefix_no_boundary` 生成）**、**ゲート関数の未認識入力経路を許可側に落とす（`fail_open` 生成）**、**検査対象の別名と sink 引数をずらす（`post_check_append` / root-equal 条件の試験）**。各 ≥ 3。

### Baseline と合格条件

- **Semgrep OSS の taint rule**（デコレータ付きツールのパラメータと LLM 戻り値を source に）。**CE は手続き内 taint のみ。** 比較は (a) source と sink が同一関数内にある行に限定した部分表と (b) 全行表の 2 つに分ける。
- **MCP-BiFlow**（arXiv 2605.07836）。実装が公開されていればそれを走らせ、公開されていなければ**公表値との対ごと突き合わせ**に切り替える。**Semgrep OSS だけを baseline にすると、MCP-BiFlow が既に公表した「Semgrep 8/32・CodeQL 1/32」を再発見するだけになる。**
- **Agent Audit**（arXiv 2603.22853、`HeadyZhang/agent-audit`）。**合格条件 (ii) の必須対象にはしない**（他人のツールが動かないだけで自分の合否が落ちるのを避ける）。項目 C3 の中で走らせ、**2 日で動かなければ落として「agent 特化 baseline は導入コストにより不成立」と報告する**。
- **Pysa ModelQuery**: pyre 環境の構築に成功した repo のみ。第 0 週に 1 fixture で 0.9.25 の構文を検証し、**D13（第 2 週の 3 日目）までに環境が立つ repo が 0 なら baseline から落として「pyre 依存 baseline は環境コストにより不成立」と報告する**（第 3 版の「第 1 週末（D13）」は週の数え方の誤り）。
- 宣言のみを見るスキャナ、**および agentic-guard 型の名前ベース分類器**（F0a の比較腕として）。
- **LLM baseline は行わない**（§7.3）。
- CodeQL / AgentFlow / Agentic Radar は**余力**。第 1 週に走らなければ落とす。Agentic Radar の優先度は最下位（AgentFlow の第三者測定で 60 中 29 件が解析失敗）。

### 指標（定義を全て固定する）

| 指標 | 定義 | 閾値 |
|---|---|---|
| **両側通過率（head-to-head の主指標）** | 同一の対集合に対し、脆弱版と修正版でタプルが事前登録どおりに変化した対の割合。**AuthGap と各 baseline について同じ対集合で計算する** | 報告値。§10 の T1 合格条件で判定する |
| verdict-clearing 数 | 両側通過対のうち修正版で verdict が GAP から外れる対の数 | 報告値（必須併記） |
| mutant 判別率 | (原版, mutant) 対のうち原版を報告せず mutant を報告した対の割合 | ≥ 0.8 |
| false-strong 率 | `count(strong と採点 かつ 裁定ラベルは weak or none) / count(strong と採点)` | < 5% |
| 効果 precision | 裁定ラベルに対する (unit, effect kind) 行の `TP/(TP+FP)` | ≥ 0.7 |
| verdict 適合率 | 野外 60 ツールでの verdict のラベラー基準適合率 | GAP_INJECT で ≥ 0.7 |
| GAP_INJECT 件数 | 裁定済み偽陽性の件数 | ≤ 3 / 20 ツール（**副次指標**） |
| opaque 率 | **主 slot 7 種**（`code_text`/`argv0`/`argv[*]`/`shell_string`/`path`/`url.host`/`sql`）に限定した `opaque な制御位置 / (resolved + opaque な制御位置)`。**省略された既定引数の slot は分母に入れない。`remote` は分母に入れない**（別行の報告値）。粗い分母（全 slot）の値も必ず併記する | **≤ 40%。この閾値は月 3 で置き直さない。** 動かすのは分母の定義だけで、その定義は D5 に確定させ `docs/budget.md` に記録する。40% に経験的根拠は無く、事前に固定することだけが根拠である（§3 の交差行 ≥ 3、§2.5.6 の生存 ≤ 2 と同じ扱い） |
| OPAQUE 内訳 | §2.5.4 の 8 語彙の件数比。**合計と `NODOM` 件数を必ず並記する** | 報告値 |
| 支配発火率 | (a) 発生水準 = `req_occ > MODEL の危険効果 / 全危険効果`、(b) 値水準 = `req_val > MODEL の制御位置 / 危険効果の全制御位置`。**T3-tool と T3-app を分けて出す** | §10 参照 |
| 発生ゲート保有率 | `\|{P ∈ 60 MCP サーバ : 発生ゲート ≥ 1}\| / 60`。**4 形態それぞれの内訳を必ず併記する** | 報告値（合計値だけでは形態 4 の運用定義に支配される） |
| D 層別存在率 | `r_kind` / `r_dom` / `r_op` / `r_prev`、母集団別。**分母は危険効果を持つユニットで、効果検出器の偽陽性クラス（非 DB の `.execute()` 等）を除いた値と粗い値の両方を出す** | §10 の D 規則 |
| 交差行数 | §3 の 3 腕アブレーション | ≥ 3、異なるプロジェクト |

このほか: 効果の resolution rate、trig の traced/assumed 比率、CONTRADICTION 精度、規則 W による GAP 行の比率、**全 GAP 行の層別 `covered_by` 内訳**、決定論の 3 回一致、venv 構築なしでの解析成功率、コスト（秒/ツール）、副 kind 一致 `Leak` 行数の分布。

**ラベリングは 4 次元**: 効果 kind、制御引数、ゲート等級、verdict。次元別 κ。集合値の行は κ ではなく Jaccard。裁定は第二ラベラー、同点は第一著者。AI アシスタントは κ に含めない。**slot 語彙の拡張（SPAWN 3→7、NET 2→6）でラベリング項目数が増えるので、第 1 週の probe で「60 ツールあたりの実在制御位置数」を測り、20〜40h に収まらなければラベリング対象を主 slot 7 種に限定し、残りの slot は manifest 属性としてのみ出力して κ に数えないと事前登録する。**

### 凍結

- **月 3**: sink 語彙（直接 + proxy + pipe、slot 語彙、**副 kind**）、ライブラリ コンストラクタ カタログ、ラベル規則、標本フレームと seed、rubric 1c、配備モード、**執行表**（登録経路 × SDK 版 → 執行するか。確認した版と commit を記録）、R2 の例外。
- **月 6**: **ゲート語彙**（Def 5 の weak 理由語彙、strong の定義、config atom の 4 源、§2.5.4 の OPAQUE/NODOM の 2 系統、消滅理由の語彙、ゲート要約カタログ）と較正 mutant corpus。**採点器 B3b の完成（月 8 頃）を待たない** — 語彙は Def 5 に既に完全に書き下されており、**語彙が較正 mutant を通過するよう調整された後に凍結すると held-out 層の意味が失われる**。月 6 時点で `docs/fingerprint.json` の語彙ブロックのみを先行凍結してコミットしタグを打つ。同時に held-out mutant 生成器（B4）をコミットする。**較正 15 mutant は設計汚染済み較正なので凍結対象ではない。** B3b の実装過程で語彙の変更が必要になった場合は、変更内容・理由・日付を `docs/preregistration.md` に**逸脱**として記録し、held-out の結果はその逸脱を明示したうえで報告する。**held-out advisory の窓の起点は月 6。**
- **月 10**: **解析指紋**。`docs/fingerprint.json` に sink 表、R1/R2 カタログ、ゲート述語カタログ、weak 理由語彙、cap と深さ（`K`、`SUMMARY_CAP`、CFG ノード cap）、D パーサ規則と執行表の sha256、凍結時の git commit を入れる。凍結 = コミットしてタグを打つこと。凍結後の実行は指紋を evidence に書き、不一致は held-out 結果を無効にする。

**held-out は月 10 の凍結後に 1 回だけ。** evidence ディレクトリをコミットしてから数字を読む。

**月 6 の再走査（go/no-go ではない）**: §1.5.6 の 4 軸を再走査し、埋まった軸を日付と出典つきで `docs/related_work.md` に記録する。軸 1（修正版側）が先行手法にも達成されたら、その論文を主 baseline に据え貢献を残る 3 軸に寄せて書き直す。

---

## 7. 計画

### 7.0 会計単位の変更（この節が §7 の他のすべてを規定する）

**第 2 版の表は合計が誤っていた。** 行を足すと 45 ではなく **47** であり、実効 34 週に対する超過は 11 週ではなく **13 週**だった。

より重大なのは会計単位である。第 2 版は「建設週」を数えていたが、前身リポジトリの git 記録は構築が週単位の作業ではないことを示す。

| 実測（前身リポジトリ、一次記録） | 値 |
|---|---|
| `selection_guard.py`（2,910 行）の初出コミット | 2026-09-01（`bd21b5e`）、**1 日** |
| 検出器 + `scale/` + `diffbench/` の中核（7,210 行） | 2026-09-01〜09-02 の **2 暦日**、16 コミット |
| プロジェクト全体 | 2026-06-26〜2026-09-08、41 コミット、**コミットのある日は 8 日**（稼働の下限であり稼働日数の測定ではない） |
| その成果物への 2026-09-03 の外部監査（HEAD `f7aced6`） | 指摘 **99 件**、うち major **34 件** |
| 監査応答（〜2026-09-08）後に §9.2 の未了表に残った行 | **9 行**（10 行中「実施」は 1 行のみ。ただし残る 9 行のうち 1 行は「追加の作業は無い」と明記された整理なので、作業として未了なのは 8 件） |
| 同じ監査時点の `guard_dominance` | 56 テスト緑のまま自前 mutant **15 件中 10 件が生存**（監査 付録 A #34）。**監査後にテストは 56 → 99 に増えたが監査自身が変異試験を再実施していないので現在の生存数は未知** |

**結論**: 週を消費しているのは書くことではない。**仕様を書くこと、受け入れテストを設計すること、出力を原ソースに当てて検証すること、監査に応答して再発行すること**である。したがって以下の表の単位を**学生週**（学生本人の手が塞がる週）に変える。AI アシスタントの構築時間は学生週には計上しない。

**カレンダーについての明示的仮定**: AI 構築日を学生週に計上しないということは、その日がカレンダーからも消えるという意味ではない。前身の実測（7,210 行 / 2 暦日）を外挿すると項目あたり 2〜3 日、建設 11 項目で 5 カレンダー週前後を AI 構築が占める。§7.5 の写像はこれを「学生が次項目の仕様を書いている期間と重なる」として計上していない。**重ならないと分かった時点（ある項目で AI の完成待ちのために学生が 3 日以上手空きになった時点）で §7.4 を 1 段適用する。**

### 7.1 検証負荷則（事前登録。反証条件つき）

各項目の学生週は 3 成分の和として見積もる。

1. **仕様（学生のみ、代行不可）**: 入力・出力・受け入れテストを AI に投げる**前に**書き切る。書けていない項目は AI に投げてはならない。
2. **構築（AI）**: 学生週 0。ただし **AI を並行に走らせられる項目数の上限は、学生が仕様を書き終えた項目数**である。
3. **検証（学生）**: **主張が依存する解析器コード 1,000 行あたり 1.0 学生週。** 中身は次の 4 つに限定し、これ以外を検証と呼ばない。(a) 受け入れ fixture の全行を手で読み期待値と突き合わせる。(b) 野外出力から無作為 20 行を取り**原ソースに当たって**照合する。(c) 決定論 3 回一致。(d) 直前までの受け入れ fixture 全部の回帰。

**1.0 週/kLOC の位置づけ（導出値ではなく予算）**: 前身の記録から導出したものではない。**導出できないことが要点である。** 確認できるのは (a) 7,210 行が 2 暦日に着地した、(b) 1 回の監査が指摘 99 件・major 34 件を出した、(c) 応答後も未了表に 9 行が残った、の 3 つだけである。**人手の検証時間そのものは前身に記録が無く `週/kLOC` の実績値は算出できない。** また 2026-08-31 の `d16d060`（multi-agent review の適用）が示すとおり 2026-09-03 の監査は最初の査読ではない。したがって「前身の検証負荷は 0.11 週/kLOC だった」とは書かない。1.0 は**その状態を繰り返さないために置く上限つき予算**であり、閾値の恣意性は交差行 ≥ 3 と同種の弱点として本文にそう書く。

**測定手続き**: A4 の実施中、学生は検証 (a)-(d) に費やした時間を `docs/verification_log.csv`（列 `item, date, hours, activity(a|b|c|d)`）に日次で記録する。分母は当該項目の `authgap/` 配下の非テスト追加行数（生成物と fixture を除く）。A4 完了時に `hours/40 / (lines/1000)` を計算して事前登録文書に追記する。

**反証条件**: A4 完了時点（月 3 前後）で **1.5 週/kLOC を超えていたら §7.4 を 1 段適用する**（超過を D1 で吸収しない）。0.5 を下回っていたら余剰は D1 に積み増すだけで、落とした項目を復活させない（復活させると凍結済みの事前登録が動く）。

**見積もり行数**（前身の同等部品からの外挿。A4 完了時に実測して更新する）: A4 効果層 ~1,800 行、B1 trig ~900、B2 val ~1,600、B3 ゲート採点器（B3a 支配 ~700 + B3b 採点 ~1,000）、B5 出力層 ~900 = **~6,900 行 → 検証だけで 6.9 学生週**。下表でこの 5 項目に付けた **19.5 学生週**（A4 3.0 + B1 2.0 + B2 5.5 + B3 6.5 + B5 2.5）のうち 6.9 が検証、残る **12.6** が仕様記述・受け入れテスト設計・修正ループである。**（この 19.5 は執行表を B3 へ移す前の値。移動後も B3 6.75 + B5 2.25 = 9.0 で合計は不変。）**

### 7.2 34.0 学生週の表

各行は「成果物」「受け入れテスト」「担当」を持つ。**受け入れテストが書けない行は項目として認めない。**

**Q1 — 床（合計 7.75）**

| ID | 項目 | 成果物 | 受け入れテスト | 担当 | 学生週 |
|---|---|---|---|---|---|
| A0 | 第 0 週（§8） | `docs/advisor_request_v1.md`、`docs/labeling_degradation.md`、`docs/disclosure.md`、`docs/toolchain.md`、`docs/rubric_1c.json`、`docs/budget.md` | rubric_1c.json がコミットされ、3 通が送信済み。semgrep の手続き内境界を自前 fixture で実測済み | 学生 | 1.0 |
| A1 | 先行研究の追認 | `docs/related_work.md`（§1.5 をコピーし差分管理） | **◎' の 5 行（DCIChecker / Semia / MCP-BiFlow / AgentFlow / MTGuard）の本文 PDF を自分で読み、差分欄を節番号で裏づける。** これを通過するまで解析器の実装（A4 以降）へ進まない | 学生 | **0.25** |
| A2 | repo 基盤 | パッケージ骨格、`pytest` + `ruff` の CI、決定論テストハーネス、`scripts/fetch_corpus.py`、`scripts/premeasure/`（前測スクリプトの移植） | CI 緑。空入力に対して manifest が 3 回バイト一致 | AI 構築 / 学生検証 | 0.5 |
| A3 | CVE triage + pin + コーパス取得 | `docs/cve_triage.csv`（A1–A18 + B 群 + S 群）、`docs/expected_tuples.md`、`docs/pins.json`、`docs/population.md`、`docs/sampling.md`、`corpus/`（採点集合 16 木 + 標本 98 木 + ケーススタディ 3 木）、`fixtures/negatives/` | 修正コミット単位で両側採点可能な対 **≥ 6、かつ ≥ 4 プロジェクト、かつ単一プロジェクト由来は最大 3 対**。全 ref が `git rev-parse` で解決。**各行で「両側判別可能性」を独立に検査済み**（T1.3-7） | 学生（一次資料照合は代行不可） | **2.25** |
| A4 | 効果層 + 抽出器 | `authgap/effects.py`（直接 + proxy + pipe、slot 束縛、受け手推論）、`authgap/entries.py`（R2 カタログ、低レベル 2 形）、`python -m authgap probe` | (i) Def 3 の必要ライブラリ sink 行すべてに fixture、(ii) 採点集合の脆弱側で当該効果行が出る、(iii) 20 行無作為照合で効果 kind の誤りが 0、(iv) 3 回一致 | AI / 学生（検証則 1.8 週） | 3.0 |
| A5 | F0a 実行 + F0c | `evidence/<run>/probe.json`（98 木 = 60 サーバ + 30 パッケージ + 8 アプリ。**F0a の分母は 60+30**）、`docs/f0a.md`、`docs/f0c.md` | probe.json が §5.1 の全キーを持つ（`traced_ratio` は `null`。**この run には二度と書き込まない**）。**`docs/f0c.md` に F0c-1 の 2 比率 +「(ii) は測定不能（理由付き）」がある。(i) と F0c 完成は B1 の後**。新規解析器コード 0 行、集計スクリプト 60 行以下 | 学生（機械抽出。**二重ラベルは行わない**。20 ユニットの抜き取り照合のみ） | **0.75** |

**Q2 — 三座標（合計 17.0）**

| ID | 項目 | 成果物 | 受け入れテスト | 担当 | 学生週 |
|---|---|---|---|---|---|
| B1 | trig | `authgap/trig.py`（R1/R2、AST レジストリ解決、traced/assumed） | fixture 12 件で区別が正しい。T3-app で `traced_ratio` を算出（**新 run_id で probe を再実行**） | AI / 学生 | 2.0 |
| B2 | val v0 → 脈拍 → v1 | `authgap/val/`（§2.6、`docs/val_design.md`）。10 fixture | **v0 の受け入れ = 脈拍**（§10、3.5 週時点）。v1 = 負例 pin 集合に対して行単位で事前登録どおり + opaque ≤ 40% | AI / 学生 | **5.5**（v0 3.5 + v1 2.0。脈拍不合格なら v1 の 2.0 を D1 へ返す） |
| B4 | held-out mutant 生成器 | `scripts/gen_mutants.py`（9 操作、各 ≥ 3） | **生成器のコードは B3 の開始前（累積 15.75 学生週、月 6.2）にコミットする。** 採点器の実装を見てから生成器を書くと held-out にならないので、この順序は入れ替えてはならない。**実行はゲート語彙凍結後** | 学生 | 0.5 |
| B3 | 支配判定 + ゲート採点（旧項目 3 と 8 を統合） | `authgap/gate.py`（§2.5 の全仕様 + Def 5 の等級・config atom・`Cov`/`Leak` 属性 + **Def 6 の執行表判定器と被覆規則判定器**） | **B3a（1.5 週時点）= 支配のみを問う 8 mutant を 8/8 撃破。B3b（完了時）= 付録 G の G1–G15 を `(verdict, reason クラス, witness 行)` の 3 つ組で 15/15、実装変異 15 件の生存 ≤ 2、false-strong < 5%** | AI / 学生 | **6.75**（B3a 1.5 + B3b 5.25） |
| B5 | 出力層 + D パーサ | `manifest.json`、`docs/manifest.schema.json`、`results.sarif`、annotation patch、**D_kind / D_op / D_prev の 3 層パーサ**（執行表は B3 へ移動。D_dom パーサは書かない）、unit id | 98 木で 3 回一致。manifest が schema に validate。§5.2 の全 weak 理由に witness が出る。**D_kind パーサが 3 形 + camelCase 限定で動く** | AI / 学生 | **2.25** |

**Q3 — 評価（合計 6.25）**

| ID | 項目 | 成果物 | 受け入れテスト | 担当 | 学生週 |
|---|---|---|---|---|---|
| C1 | wild run + regression + 3 腕アブレーション | `evidence/wild/`、`evidence/ablation/{A,B,C}/`、`docs/intersection_rows.md` | 3 回一致、GAP_INJECT 適合率 ≥ 0.7、opaque ≤ 40%。**腕 A/B は腕 C と同一バイナリのフラグ違いであること** | AI 実行 / 学生検証 | **2.5**（T3-app 8 件） |
| C2 | ラベリング 60 ツール × 4 次元 + 裁定 | `docs/labels.csv`、次元別 κ、集合値行は Jaccard | 第 2 ラベラーの独立ラベルが揃い裁定手続きが記録されている。AI は κ に含めない | 学生 + 第 2 ラベラー（別途 20〜40h） | 1.0 |
| C3 | baseline | Semgrep OSS ルール 2 本（部分表 + 全行表）、MCP-BiFlow の公表値との対ごと突き合わせ、Agent Audit（2 日で動かなければ落とす）、宣言のみスキャナ、名前ベース分類器 | 採点集合 8 対に対して両側通過率の表が出る | AI / 学生 | **0.5** |
| C4 | ケーススタディ 3 件（gptme / SuperAGI / OpenHands-sdk） | `docs/case_*.md` | 「出荷されている承認リスト vs 本ツールが合成した承認リスト」の差分表が 3 件ともある | 学生 | 1.0 |
| C5 | 事前登録文書 + 開示対応 | `docs/preregistration.md`（月 3 / 6 / 10 の凍結時に追記）、開示レポート | 各凍結時点で追記済み。90 日時計の起点と終点が記録されている | 学生 | **0.25** |
| C6 | held-out 実行（月 10 指紋凍結後に 1 回） | `evidence/heldout/` | 実行前に evidence をコミット。指紋一致を確認してから数字を読む | 学生 | 1.0 |

**バッファ（合計 3.0）**

| ID | 項目 | 根拠 | 学生週 |
|---|---|---|---|
| D1 | 監査・再発行 | 前身の実測（1 回の建設バーストに対し指摘 99 / major 34 / 未了 9）。**切り詰め順序の最後に置き、最初には落とさない** | 2.0 |
| D2 | 指導教員応答・再提出 | A0 の 3 通の返答待ち。A1/A2/A4 は返答に依存しないので並行に進む | 1.0 |

| | **合計** | **34.0** |
|---|---|---|

### 7.3 算術（3 段階。すべて再導出できる形で書く）

**段階 1 — 第 2 版の表の実際の和は 47 である**（表記の 45 は中間版から持ち越された陳腐な数値。原典 `CONCEPT_REDESIGN_..._AUTHGAP.md` の表は 40 で自己整合しており、第 2 版が追加した 5 行（-1=2, -2=1, 4c=1, 18=2, 19=1 = +7）で 47 になる）。

**段階 2 — 再構成で −13.0（47 → 34.0）。** 旧項目と新項目を 1 対 1 で対応させる。

| 旧項目（週） | 新項目（学生週） | 差 | 消える主張 |
|---|---|---|---|
| -1 リポジトリ基盤（2、scale ハーネス移植を含む） | A2 (0.5) | **−1.5** | 数百規模走査。もともと主張していない。venv も型環境も作らないので再試行・再開の機構が要らず、逐次ランナー 60 行で足りる |
| -2 先行研究（1） | A1 (0.5) | **−0.5** | なし。AI が候補収集と要約案を出し、学生は該当節の照合に集中する |
| 2 probe(1) + 4a F0a(2) + 5 sink/entry(2) + 4c F0c(1) = 6 | A4 (3.0) + A5 (1.0) | **−2.0** | なし。probe.json のキーは F0a の測定次元の部分集合。**F0a の 90 木二重ラベル廃止は矛盾の解消である**（F0a 行は「二重ラベル」、標本設計は「機械抽出、人手ラベルなし」と書いていた）。**A4 は旧項目 5 の 2 週から 3.0 へ増やしている**（proxy 受け手推論とエントリ発見が前身に存在せず検証則で 1.8 週が要る） |
| 3 支配判定(4) + 8 ゲート採点(4) = 8 | B3 (6.0) | **−2.0** | なし。両者は同一の連結経路走査であり受け入れテストも同一の対象を採点する。**ただし支配部分（B3a）は val の後ろに置く**（B3a は脈拍の前ではなく後。脈拍のタプルは §10 で構文的 validator 形状に置き換えたので支配を必要としない） |
| 6 val（6） | B2 (5.0) | **−1.0** | v1 の作り込み 1 週。opaque ≤ 40% を外した場合の再試行余地が減る |
| 7 trig（3） | B1 (2.0) | **−1.0** | **「30 wall 人手ラベルで辺 P/R」を落とす。** trig については traced/assumed 比率と fixture 12 件の正誤のみを報告し、辺の P/R は主張しない |
| 10 mutant corpus（1） | B4 (0.5) | **−0.5** | なし。**これも矛盾の解消である**（旧表は「月 6 凍結より前に完了」、T2 は「held-out は凍結後に新規生成」と書いていた）。較正 mutant は B3 の成果物、生成器コードは凍結前、生成の実行は凍結後、と 3 つに分ける |
| 9 出力層（3） | B5 (2.0) | **−1.0** | なし。witness テンプレートと unit id の式は §5.2 で凍結済み、決定論テストは A2 の CI に入る |
| 11 wild run(2) + 14 アブレーション(2) = 4 | C1 (3.0) | **−1.0** | **diff モードのケーススタディを落とす**（旧切り詰め順序 (1) の先行適用）。リリース間 drift と CI 用途は主張しない。**ただし D_prev（`GAP_DRIFT`）の測定は B5 に残る** |
| 13 baseline（2） | C3 (1.0) | **−1.0** | **LLM baseline を落とす。**「固定プロンプトの LLM レビューより優れる」を主張しない |
| 17 事前登録 + 開示（1） | C5 (0.5) | **−0.5** | なし |
| 18 指導教員バッファ（2） | D2 (1.0) | **−1.0** | なし。A1/A2/A4 は返答に依存しないので待ち時間は学生週を消費しない（旧計画の 2 週は二重計上だった） |
| 0(1) / 1(2) / 12(1) / 15(1) / 16(2) / 19(1) = 8 | A0 1.0 / A3 2.0 / C2 1.0 / C4 1.0 / D1 2.0 / C6 1.0 = 8.0 | **0** | なし。**ケーススタディは 3 件のまま維持する**（SuperAGI は B3 が作る config atom 4 源を野外の出荷物に対して行使する唯一のケーススタディであり、落とすと config-conditional の外部証拠が 0 になる。削減も 0 週） |
| | **計** | **−13.0** | 47 − 13.0 = **34.0** |

**段階 3 — 7 改善の増分 +1.75、および補償の削減 −1.75。**

| 増分 | 週 | 理由 |
|---|---|---|
| A3 2.0 → **2.25** | +0.25 | select-cell 由来の S1′（doris）と S2（neo4j）の triage、および 25 行に増えた CSV の一次再確認 |
| B2 5.0 → **5.5** | +0.5 | proxy カタログの ctor 引数 slot 束縛（F1 に必須）、heap の受け手アクセスパス（F6 に必須）、`K` の 5 shape 適用 |
| B3 6.0 → **6.5** | +0.5 | Def 5 の weak 理由語彙の拡張（8 → 19 語）と witness テンプレート、`Cov`/`Leak` 属性の集合計算、`self_granted` 格下げ |
| B5 2.0 → **2.5** | +0.5 | D の 3 層パーサ（D_kind の 3 形 + camelCase 限定、D_op の帰属規則、D_prev の join）と執行表。**D_dom パーサは書かない** |
| **小計** | **+1.75** | 34.0 → 35.75 |

| 削減 | 週 | 理由 |
|---|---|---|
| A1 0.5 → **0.25** | −0.25 | §1.5 の調査が済んでおり、第 1 週は ◎' 5 行の PDF 精読と追認のみ（**+1 週の増額要求は却下した**。実施済みの作業に週を足すのは超過を悪化させるだけである） |
| A5 1.0 → **0.75** | −0.25 | 前測スクリプト（`scan.py` / `lowlevel.py` / `drift2.py` / `stats.py`、計 578 行）が存在し `scripts/premeasure/` へ移植するだけである |
| C1 3.0 → **2.5** | −0.5 | **切り詰め順序 (1) の前倒し適用: T3-app 15 → 8。** SELECT の野外評価は成立しない可能性が高い |
| C3 1.0 → **0.5** | −0.5 | **切り詰め順序 (5) の前倒し適用**: baseline を Semgrep 部分表 + 全行表 + MCP-BiFlow の公表値突き合わせに絞る。Agent Audit は 2 日 time-box |
| C5 0.5 → **0.25** | −0.25 | 事前登録文書は月 3 / 6 / 10 の凍結時に増分で書く |
| **小計** | **−1.75** | 35.75 → **34.0** |

**総合**: 47 −13.0 +1.75 −1.75 = **34.0 学生週**（実効 46 週 − 執筆 12 週 = 34 週にちょうど一致する）。**超過は 0 である。ただしこれは切り詰め順序 (1) と (5) を先に使い切った結果であり、余裕が消えたということでもある。** D1 の 2.0 は残してある。

### 7.4 切り詰め順序（34 週をさらに超えた場合、この順に落とす）

0. **strong-eval を実装しない**（`code_text` / `sql` 位置はゲートの真偽値のみ扱う）。0 週の節約だが B3 の受け入れ条件を軽くする。
1. **T3-app 8 → 4**（(1) は既に 15 → 8 まで適用済み）。
2. T3-tool 60 → 30（κ の n が減る。比率と信頼区間は n ≥ 25 の規則により 30 でも維持できる）。
3. ケーススタディ 3 → 1（gptme を残す）。
4. B2 の v1 を打ち切り真偽値 fallback（脈拍で自動的に決まる。§10）。
5. baseline を Semgrep 部分表のみに縮小（全行表を落とす。T1 合格条件 (ii) は部分表で判定する）。
6. **主語一致を落とす**（G11 を受け入れ集合から外し、「ゲートするが無関係な述語を誤って clear する」を限界として本文に明記）。
7. D1 監査バッファ 2 → 1（**最後**。ここに手を付ける時点で品質の主張を下げる）。

**切り詰め順序から項目を外すときは必ず同順位の代替を 1 つ繰り上げる。**

### 7.5 四半期と凍結時点

**係数**: 実効 46 週 = カレンダー 18 か月なので 1 学生週 = 18/46 = **0.391 カレンダー月**。34 学生週 + 執筆 12 効力週 = 46 効力週 = 18 か月でちょうど閉じる。

| 時点 | 累積学生週 | カレンダー月 |
|---|---|---|
| A4 完了（**月 3 凍結: sink 語彙 / 執行表 / 副 kind / rubric 1c / 配備モード**） | 7.00 | 月 2.74 |
| A5 完了（**F0a 成立**） | 7.75 | 月 3.03 |
| B1 完了（`traced_ratio` を新 run で算出） | 9.75 | 月 3.81 |
| B2 v0 完了（**脈拍**） | 13.25 | 月 5.18 |
| B2 v1 完了 | 15.25 | 月 5.97 |
| B4 生成器コミット（**月 6 凍結: ゲート語彙。held-out 窓の起点**） | 15.75 | **月 6.16** |
| B3a（支配 8 mutant 8/8） | 17.25 | 月 6.75 |
| B3b 完了（G1–G15 を 15/15） | 22.25 | 月 8.71 |
| B5 完了（**月 10 凍結: 解析指紋**） | 24.75 | 月 9.68 |
| C1 完了（wild run。開示の 90 日時計の起点） | 27.25 | 月 10.66 |
| C6（held-out 1 回） | 31.00 | 月 12.13 |
| D 完了 → 執筆開始 | 34.00 | 月 13.30 |

**月 6 の凍結は動かさない。** 凍結するのはゲート**語彙**であり Def 5 に既に完全に書き下されているので、採点器 B3b（月 8.7）の完成を待つ必要はない。**語彙が較正 mutant を通過するよう調整された後に凍結すると held-out 層の意味が失われる。** B3b で語彙の変更が必要になったら逸脱として記録する。

**開示の時計**: C1（月 10.66）が起点なので 90 日時計は月 13.7 に切れる。これは執筆期間と重なる。C5 の 0.25 学生週を Q4 に置き、執筆 12 週の内側に確保する。

### 7.6 第 0〜3 週の日次計画（D1–D15 + D16–D20）

**§7.6 が覆うのは A0（1.0）+ A1（0.25）+ A2 の学生分（0.5）+ A3 の前半（1.25）= 3.0 学生週である。** A3 の残り 1.0 学生週（S 群の一次読解、負例集合の行単位 pin の仕上げ、`docs/expected_tuples.md` の全行確定、pyre 環境の 5 木試行、執行表の版分布計数、annotation パーサの形カバレッジ確認）は **D16–D20（第 3 週）**に置く。第 3 版は A3 の 2.25 週全部を D8–D15 の 8 営業日に詰めており、下の規則が第 1 週で発火してしまう。**§7.5 の累積学生週（A4 完了 = 7.00 = 月 2.74）は変わらない** — A4 の着手が暦で 4 週目になるだけで学生週会計は不変である。

各日の「成果物」はその日の終わりにディスクに存在していなければならないファイルである。存在しない日があった時点で、その週の残りを翌週へ送らず、**その日の成果物を落とすか §7.4 を 1 段適用する**。

**§1.5 の「これを書く前に実装へ進まない」は解析器の実装（A4 以降）を縛る規則であり、repo 骨格・取得スクリプト・決定論ハーネス（A2）は D7 の前に着手してよい。**

**第 0 週**

| 日 | 学生 | AI | その日の終わりに存在するもの |
|---|---|---|---|
| D1 | 指導教員宛の 1 枚（(a) 解析単位を callee 側へ反転してよいか、(b) null 時に**研究設問が変わる**ことを含めて F0 を論文として認めるか、(c) 拒否分岐、(d) **SELECT が野外で発火しない場合の格下げ分岐を先に受理いただく**）を書いて送付 | 空 repo に骨格を生成 | `docs/advisor_request_v1.md` + 送信記録、repo 初回コミット |
| D2 | 第 2 ラベラー候補 2 名に依頼文を送付。離脱時の縮退設計を書く | `scripts/fetch_corpus.py` の骨格 | `docs/labeling_degradation.md`、依頼文 2 通の送信記録 |
| D3 | 開示プロトコルを書き大学と教員へ承認依頼 | 決定論テストハーネス | `docs/disclosure.md` v1 + 送信記録、`tests/test_determinism.py`（空入力で緑） |
| D4 | semgrep OSS を導入し**手続き内 taint のみ**という境界を自前 fixture で実測。§8-4 の Pysa 疎通 fixture で `pyre analyze --no-verify` を実行 | fixture 生成、ログ整形 | `docs/toolchain.md`、`fixtures/semgrep_boundary/`、`fixtures/pysa_check/`、`evidence/w0/pysa_check.log` |
| D5 | rubric 1c の**追認と記録**（再検討ではない）。配備モード既定と CONTENT の扱いを記録。自分のカレンダーで ~32 週控除の根拠を確認 | 候補ツール名の grep | `docs/rubric_1c.json`（コミット）、`docs/triage_notes.md`、`docs/budget.md` |

**第 1 週**

| 日 | 学生 | AI | その日の終わりに存在するもの |
|---|---|---|---|
| D6 | **◎' の 5 行（DCIChecker / Semia / MCP-BiFlow / AgentFlow / MTGuard）の本文 PDF を取得して読む。** §1.5 の差分欄を節番号で裏づける | PDF 取得と抽出 | `docs/related_work.md`（検証強度を ◎ に更新した 5 行） |
| D7 | **MCP-BiFlow Table 3 の 32 事例と §6 採点集合の突き合わせ。** `also_in_biflow_table3` 列を埋める。§1.5.1 の比較結果の報告様式を確定。**この日を通過するまで解析器の実装に進まない** | Table 3 の抽出 | `docs/related_work.md` 完成、`docs/cve_triage.csv` の当該列 |
| D8 | §9-6: PyPI の `mcp` / `fastmcp` 逆依存を取得し重複除去して件数を出す。**300 未満なら母集団を framework のツールパッケージへ切り替える**（コーパス取得の前に決める） | `scripts/fetch_frame.py` | `docs/population.md`（件数・取得日・判定）、`docs/frame.json` |
| D9 | **CVE / GHSA 番号・公開日・affected 範囲の一次再確認**（§6 の A 群 **17 行**（A1–A5・A7–A18）+ B 群）。`advisory_published` は GitHub Advisory DB の `published_at` に統一 | advisory ページの取得 | `docs/cve_triage.csv` の ID 欄が一次確認済みになる |
| D10 | **各行の「両側判別可能性」の独立検査**（T1.3-7）。A12 / A16 / A17 の N/A 判定を自分の目で追認し、A13 の条件（sqlglot をカタログに載せるか）を決める。B6（browser-use 0.1.44）、B7（LangChain）、B8（llama-index）を検証 | 該当 diff の抽出 | `docs/cve_triage.csv` の `two_sided` / `disappearance_reason` / `expected_tuple_change` が全行埋まる |

**第 2 週**

| 日 | 学生 | AI | その日の終わりに存在するもの |
|---|---|---|---|
| D11 | S1′（doris）を読み、`self_granted` を Def 5 に入れても両版のタプルが変化するかを判定（反証条件 F-5）。S2（neo4j）を INJECT 側の予備候補として pin | クローンと diff 抽出 | `docs/cve_triage.csv` の S 群、`docs/expected_tuples.md` |
| D12 | **go/no-go: 修正コミット単位で ≥ 6 対、≥ 4 プロジェクト、単一プロジェクト最大 3 対。** 採点集合 8 対と補充順序を凍結 | — | `docs/cve_triage.csv` 完成、go/no-go 判定文、`docs/scored_set.md` |
| D13 | pin スクリプトを検証（採点集合 8 対 × 2 版 + ケーススタディ 3 木が `git rev-parse` で解決するか）。**D4 の `pysa_check` 結果と採点集合 5 木での pyre 環境構築を試し、立つ repo が 0 なら Pysa を baseline から落として `docs/toolchain.md` に記録する** | `scripts/fetch_corpus.py` 完成 | `docs/pins.json`、`corpus/` に 16 木 + ケーススタディ 3 木、CI 緑、`docs/toolchain.md` の追記 |
| D14 | 標本抽出: 60 MCP サーバ + 30 ツールパッケージ + 8 アプリを**固定 seed**で抽出し取得。取得失敗を件数として記録（黙って落とさない）。**sparse パターンに `/**/*.txt` と `/**/*.lock` を含め、`requirements*.txt` と lock ファイルが実際に落ちてくることを 1 repo で確認する**（前測のコーパスはこれらを 1 件も含まないまま「依存版を読んだ」と書いていた）。**repo ごとの commit SHA を `docs/frame.csv` に記録し、解析実行の前後で detached HEAD が残らないことを確認する** | 取得実行、失敗ログ整形 | `docs/sampling.md`、`docs/frame.csv`、`corpus/` 98 木、`docs/fetch_failures.md` |
| D15 | 負例集合の pin: 定数ホストの HTTP ツール群（GAP 0）と by-design の exec/spawn/fs-write ツール（kind 別件数一致）を**行単位で**書く。F10 の木を checkout して URL 構築式を読み期待行を確定。これが B2 の脈拍の判定材料になる | 候補列挙 | `fixtures/negatives/`、`docs/expected_negatives.md`、`fixtures/val/expected.json` の F10 行 |

---

## 8. 第 0 週（実装より先）

1. **指導教員の合意を書面で**。(a) 解析単位を callee 側に反転してよいか。(b) **null 時には研究設問そのものが「Python エージェントにおけるモデル実効権限の測定」に変わることを明示したうえで、F0 を論文として認めるか。方法の変更ではなく設問の変更として書面で受理を得る。** (c) 拒否分岐（「論文 = F0 + trig の計算 + SELECT のケーススタディ。val は真偽値の到達判定。1b の行は落とす」）。(d) **SELECT が野外で発火しない場合の格下げ分岐（§3、§10）を先に受理いただく。**
   - **枠組みについての説明**（合意文書に 1 段落）: 新規性は主目的ではない。§1.5 の 4 件は比較対象であり、貢献は同一コーパス上での**精度差**、とくに**修正版側**の精度である。制御依存（決定 2）は `GAP_SELECT` セルがそのまま担い、`Leak` は manifest 属性であって SELECT の代替ではない。
2. **第二ラベラーの書面確約**（氏名、20〜40 時間）。**予備ラベラー 1 名も同時に確保するか、離脱時の縮退設計（30 ツールに縮小し、指導教員による裁定標本 20 行で信頼性を代替）を第 0 週に書く。**
3. **責任ある開示プロトコル**の文書化。private report と public PR の振り分け、90 日タイムライン、CVE 申請経路、修正前に伏せる範囲、大学と教員の承認。**wild run の前に必須。**
4. **ツールチェーン**。semgrep OSS を導入し**機能境界（OSS は手続き内 taint のみ）を確認**。PyPI 逆依存の取得手段と標本 seed。Docker。**LLM baseline の予算は不要（削除した）。**
   - **Pysa の疎通確認（critical path ではない）**: `fixtures/pysa_check/` に 2 ファイルの対象、`taint.config`、`models.pysa`（`ModelQuery(name="tool_params", find="functions", where=[Decorator(fully_qualified_name.matches("tool"))], model=[Parameters(TaintSource[ModelTaint])])`）を置き `pip install pyre-check==0.9.25 && pyre analyze --no-verify`。合格条件は issue が 1 件出ること。
5. **rubric 1c の追認と記録**（Def 7 に確定文がある。再検討ではない）。
6. **配備モードの既定と CONTENT の扱い**を triage 表に記録する。
7. **D_op に in-tree の露出宣言（`enabled=` ほか）を含めるかを凍結する。** 前測の実使用は 0 件なので効果は無いと見込むが、含める / 含めないを先に決める。

**項目 1〜3 は第 0 週に開始するが、ブロックするのは項目 3（開示）だけで、それも wild run（C1）をブロックするのであって建設はブロックしない。** 第二ラベラーが確保できなければ、同一 60 ツールを 2 週間空けて再ラベルする test-retest 信頼性で κ を代替し、事前登録にその置換を書き、inter-rater に依存する主張を全て落とす。

---

## 9. 第 0〜3 週に必ず検証すること（各項目に §7.6 の日を明記する）

**第 1 週に完結できるのはコーパスを必要としない項目だけである。** 10〜12 はコーパス取得（D14）の後、13 は前身リポジトリだけで完結するので第 0 週に置く。日割り: 1 → D9–D10 / 2 → D10 / 3 → D10 / 4 → D9 / 5 → D6–D7 / 6 → **D8（コーパス取得の前。§10 の最初の関門）** / 7 → D6–D7 / 8 → D4 / 9 → D9 / **10（執行表の一次確認・対象コーパスの版分布）→ D16** / **11（annotation パーサの形カバレッジ）→ D17** / 12（コーパス取得パターン）→ D14 / **13（G13 の前身実測）→ D5**。

1. **脆弱性 DB の fix commit 欄は使わない。** 第 3 版で誤記載の実例を 4 件、修正が存在しない CVE を 2 件確定した（§6 T1.3）。**advisory 本文の記述する修正内容から `git log -S` / `git log -p` で当該コミットを自分で特定し、その parent を脆弱側 ref とする。** AutoGPT の見解相違は `5090f55e` で確定済み。
2. **修正が「ゲートを strong にしない」対がある**（A5、A7）。だから両側条件を「タプルの変化」で定義している。各対の期待タプルを採点前に事前登録する。
3. **修正が存在しない CVE がある**（A6、B5）。両側対に数えられない。rubric 1c の典拠に使う。
4. **バージョン番号の実在**。PyPI と git tag の**両方**で確認する。tag 命名が `<name>-vX.Y.Z` 形式の場合がある（mcp-neo4j-cypher）。**PyPI に無くても git tag は存在する場合がある**（browser-use 0.1.44。第 2 版の「存在しない」は誤り）。
5. **外部統計は引用しない**。§1.5 の全数値は引用元の自己申告であり、AuthGap の閾値と同じ土俵の量ではない。**2602.03580 の 13%、DCIChecker の 9.93%、MCP-BiFlow の recall 93.8% を go/no-go 閾値と並べて書かない。**
6. **Python MCP サーバの重複除去後の母集団規模（手段は D4 に確定し D8 に実行する）。**
   - 取得手段は次の順に試し、**最初に 300 件以上を返した手段を採用して手段名・取得日・クエリを `docs/population.md` に記録する**: (1) libraries.io の dependents（`pypi/mcp`、`pypi/fastmcp`）、(2) PyPI 公開 BigQuery `distribution_metadata.requires_dist` の検索、(3) GitHub code search（`"from mcp.server" language:Python`、`"@mcp.tool" language:Python`）、(4) 公開レジストリ（`modelcontextprotocol/servers`、Smithery、PulseMCP）の Python 行。**(3)(4) は PyPI 逆依存ではないので、採用した場合は母集団の定義が「PyPI 上の `mcp`/`fastmcp` 依存者」から「公開 Python MCP サーバ」に変わることを明記する。**
   - **重複除去の単位は GitHub リポジトリ（`owner/name` を小文字化）とする。** 1 リポジトリが複数の PyPI プロジェクト / 複数サーバを出荷していても 1 件。（前測は 1 リポジトリが 3155 エントリ中 1029 を占めており、エントリ単位で数えると母集団規模を過大に見せる。）リポジトリ URL が取れない配布物は別カウントで報告し 300 の判定には含めない。
   - **300 未満のときの切り替え先を先に固定する**: 母集団を LangChain / CrewAI / agno / llama-index / openai-agents のツールパッケージに切り替え、T3-tool の 60 ツールもそこから抽出する。切り替えても §10 の D 規則は母集団別に適用する。
7. **先行研究の一次資料**（§1.5 の ◎' 5 行の PDF 精読と、MCP-BiFlow Table 3 との突き合わせ）。
8. **Semgrep の版と機能境界。**
9. **advisory の「修正バージョン」からリリース準備コミットを掴む実例を確認済み**: `mcp-neo4j-cypher` は advisory が「0.6.0 で修正」と書くが、0.6.0 の準備コミットは `dbc01ba (cypher - prep v0.6.0 #283)`（CHANGELOG / Dockerfile / README / pyproject / uv.lock のみ）で修正内容を含まない。実際の修正は `4d3454d (#281)`。§9-1 の手順が実在の対で必要になることの確認済み事例。
10. **執行表の一次確認**。対象コーパスで実際に使われている `mcp` / `fastmcp` の版と**登録 API の形状**を数え、各版のソースで入力検証の有無を自分で確認する。**`mcp` の入力検証は v1.10.0 で導入されたので「1.x なら執行される」と書いてはならない。** 確認した版と commit を `docs/fingerprint.json` に記録する。
11. **annotation パーサの形カバレッジ**。`ToolAnnotations(...)` / `ToolAnnotations(**{...})` / 辞書リテラルの 3 形を fixture ではなくコーパス上で確認する。読めない形は `D_unknown`。
12. **コーパス取得パターンの検証**。sparse パターンに `/**/*.txt` と `/**/*.lock` を含め、`requirements*.txt` / `uv.lock` / `poetry.lock` が実際に落ちてくることを 1 repo で確認する。**前測のコーパスはこれらを 1 件も含まないまま「依存版を読んだ」と書いていた。** repo ごとの commit SHA を `docs/frame.csv` に記録する。
13. **G13 の前身挙動の実測**（§2.5 付録 G。現在は推定）。links.json を手で作って前身を端から端まで通す。

**検証済みで再確認不要**: フレームワークのデコレータ名・基底クラス名・ゲート機構名、MCP `ToolAnnotations` の 5 フィールドと既定値、MCP 公式ブログ 2026-03-16 の untrusted hint 記述、標準ライブラリ API、前身リポジトリの資産パスとシンボル位置、**§6 の A 群 17 行のうち一次確認済みの 15 対の SHA と親と diff 内容**（残り 2 行は D9 で確認する）、**mcp / fastmcp / langchain の執行有無（ローカル checkout で確認済み。ただし対象コーパスでの版分布は未測定）**。

---

## 10. go / no-go（計画項目 ID で表す）

| 時点 | 合格条件 | 外れたとき |
|---|---|---|
| **A3 の途中（D8、コーパス取得の前）** | Python MCP サーバの重複除去後の母集団 ≥ 300 | 母集団を framework のツールパッケージに切り替える。**この関門だけは A5 まで待てない**（待つと 98 木を取り直すことになる） |
| **A3 の後（D12）** | 修正コミット単位で両側採点可能な較正対 **≥ 6、かつ ≥ 4 プロジェクト、かつ単一プロジェクト由来は最大 3 対**（算入可能 11 対 / 5 プロジェクトから数える） | 予備候補（A13、B2、B6–B8、S2）を triage。なお足りなければ F0 測定研究を主結果に |
| **A5 の後** | `in_tree_resolution_ratio` ≥ 50%（§1 の定義）；validator 保有ツール ≥ 5%；**D 層別存在率 `r_kind` / `r_dom` / `r_op` / `r_prev` を母集団別（MCP サーバ / ツールパッケージ）に測る**；**発生ゲート保有率を 4 形態別に測る（報告値）**；T3-app の traced 率は B1 の後 | **条件と対処の対応**: `in_tree_resolution_ratio` < 50% → **母集団をツールパッケージへ切り替える**（MCP サーバに絞っても `remote` は下がらない。§3 は逆に MCP サーバだけにすると SELECT が発火しないと書いている）／ validator 保有 < 5% → クラス 2 は T1+T2 のみ／ D 層別存在率 → **下記の D 規則**／ 発生ゲート保有率と traced 率は報告値であり関門ではない |
| **B1 の後** | **T3-app の traced 率 ≥ 20%** | **SELECT を fixture + ケーススタディのみの構造的主張に格下げする。この条項は撤回しない。** `traced_ratio` は trig が無ければ計算できないので、この関門を A5 に置かない |
| **B2 の中間点（v0 完了、月 5.2）＝脈拍** | 較正 3 対のうち **≥ 2** で、**`(制御位置, その位置の val 主体, その位置に結び付いた構文的 validator 形状, exec mode)` の 4 つ組が事前登録どおりに変化する**。加えて D15 で pin した負例集合に対して事前登録どおりの出力 | val を真偽値の到達判定に戻し、自前部分をゲート採点と manifest に限定。v1 の 2.0 学生週は D1 へ返す |

**脈拍タプルの根拠**: 完全タプル（§6 T1.1）は gate grade を含むが、等級を出す採点器は B3b で脈拍より後にある。一方 `(制御位置の主体, exec mode)` の 2 つ組まで削ると**脈拍が原理的に不成立になる** — 較正対のうち exec mode が変わるのは A5 だけで、A1（`Path.resolve` + `relative_to` 追加）も B6（browser-use）も val 主体は修正後も MODEL のままだからである。**そこで gate grade と weak reason は外したまま「構文的 validator 形状」を戻す。** 形状（語彙は §6 F0a の 11 語。ここで再掲しない）は F0a が支配判定なしに抽出する量で B3 を必要としない。**形状を位置に結び付けることだけが val を必要とし、それがまさに脈拍で試したい能力である。** これで A1・A2・A5・B6 の 4 対が判別可能になる。**較正 3 対は採点集合 8 対（A1, A2, A3, A5, A7, A9(+A10), A11, A15）の中から採る**（B6 は採点集合外なので脈拍に使うと 9 対目の木を §6 T1.6 の回帰母集団に入れることになり衝突する。**B6 を使いたい場合は T1.6 を先に改訂する**）。D9–D12 で期待 4 つ組を pin し、各対が 4 つ組だけで判別可能かを CSV の列として記録する（判別不能な対しか残らないなら脈拍の対を選び直す）。**§2.6 の K=16 反証条件が参照する「較正 3 対」も同じ 3 対を指す。**

| **B3a（B3 の 1.5 学生週時点、月 6.8 見込み、遅くとも月 7）** | 支配のみを問う 8 mutant を **8/8** 撃破 | B3 を打ち切り、F0a + F0c + T1 の対ごと表を代替主張として確定させる。**この関門を月 7 より後に置かない**（後ろにずらすと執筆 12 週が守れない） |
| **B3b（完了時、月 8.7）** | 付録 G の G1–G15 を `(verdict, reason クラス, witness 行)` の 3 つ組で **15/15**、**実装変異 15 件の生存 ≤ 2**、false-strong < 5%、mutant 判別率 ≥ 0.8、効果 precision ≥ 0.7 | 測定研究へ縮小。**語彙の凍結は月 6 に済んでいるので、ここでの不合格は凍結の変更を意味しない** |
| **B4 の位置** | 較正 15 mutant は **B3 の成果物**。held-out mutant の**生成器コードは月 6 の語彙凍結の前（累積 15.75、月 6.2）にコミットし、生成の実行は凍結後**に行う | — |
| **C1 の後** | 決定論 3 回一致（98 木）、GAP_INJECT 適合率 ≥ 0.7、opaque ≤ 40%（主 slot 限定の値を併記） | diff モードを落とし CI の主張を撤回。**決定論テスト自体は A2 の CI に入っているので、ここで新規に作るものはない** |
| **C1 の後（野外支配発火率）** | (a) 発生水準 = `req_occ > MODEL の危険効果 / 全危険効果`、(b) 値水準 = `req_val > MODEL の制御位置 / 危険効果の全制御位置`。**T3-tool と T3-app を分けて出す。合格は (a)(b) のいずれかがどちらかの母集団で ≥ 5%** | 全て 5% 未満なら「支配判定は野外で発火しない」と本文に書き、ゲート等級に依存する主張（strong 3 系統、false-strong 率、規則 W による GAP 比率）を fixture・T1・T2 に限定する。gate は野外では「OPAQUE と NODOM の内訳」だけを報告する。**5% に経験的根拠は無く事前に固定することだけが根拠であると本文に明記する** |
| **C1 の直後** | 開示の 90 日時計を起動し起点日を記録 | — |

**D 規則（thesis sentence の生死。母集団別に別々に適用する）**

測る率を先に定義する。**分母はすべて危険効果を持つユニットであり、ツール全体ではない。さらに効果検出器の偽陽性クラス（非 DB の `.execute()` 等。前測では危険 141 件中 62 件がこれ）を除いた分母と粗い分母の両方で出す。**

**「非 DB の `.execute()`」の機械判定規則（型環境なしで決める。D5 に確定し月 3 に凍結する）**: 受け手が Def 3 の proxy カタログの DB 受け手型に**局所代入で解決できる**場合のみ DB 効果とする。解決できない `.execute()` は `db_unresolved` として記録し、**危険効果に数えない**（`effect_fp_audit.db_only_non_db_execute` の分子）。A5 は機械抽出なので人手分類は行わず、20 ユニットの抜き取り照合でこの規則の誤り率だけを報告する。

- `r_kind` := **`readOnlyHint==true` / `destructiveHint==false` / `openWorldHint==true` のいずれかを明示したユニットの割合**（`annotations=` 保有率ではない。Def 6 の「上界を動かさないフィールド」規則を参照）。
- `r_dom` := 少なくとも 1 つの制御位置が Def 6 の被覆規則を満たす D_dom を持つユニットの割合。**前測では両母集団とも 0。**
- `r_op` := 運用者が exposure ファイル / ホスト承認リストを供給したユニットの割合（供給が無ければ 0）。
- `r_prev` := 直前リリースと unit id で join できたユニットの割合。
- **`r_D`** := `D_kind ≠ ⊥` または `D_op ≠ ⊥` のいずれかを満たすユニットの割合（**和ではなく和集合**。両層を持つユニットは 1 回だけ数える。`r_kind + r_op` という書き方は誤りなので使わない）。
- **分岐 1（`r_D ≥ 20%`）に落ちても `GAP_INJECT` の件数は変わらない**（D_kind は INJECT を被覆しないため）。`r_D` が動かすのは SELECT・CONTRADICTION・INVENTORY の内訳だけである。**この非対称を全表に明記する。****`r_dom` は測って別行で報告するが、Def 6 の実装条件（母集団 ≥ 5 ユニット・≥ 2 リポジトリ）を満たすまで `r_D` に加算しない。**

分岐:

1. **`r_D ≥ 20%`** — thesis sentence を維持。ただし本文と全表で **`covered_by` の層別内訳を必須**にし「D」と一語で書かない。
2. **`5% ≤ r_D < 20%`** — 「M を推論し、宣言が存在する箇所では D との差を、存在しない箇所では明示ベースライン P0 との差を報告する」に書き換え、D 由来行と P0 由来行を全表で分ける。
3. **`r_D < 5%`** — その母集団については「宣言との差」を主張から外し、**P0 と D_prev（`GAP_DRIFT`）に主張順序を移す**（Mir 型の合成の踏襲。§1.5.3）。D_prev は `r_prev ≥ 50%` のときのみ主張に使い、それ未満なら P0 のみ。**この分岐に落ちた母集団があれば、項目 C1 に D_prev の 2 リリース実行を +1.0 学生週で追加する（§7.4 を 1 段適用して捻出する）。**
4. **母集団ごとに違う分岐に落ちることを最初から許す。** 事前登録に明記する。

**前測に基づく予測（第 0 週に記録し F0a で追試する）**: MCP サーバ母集団の `r_kind` は分母の取り方で **39.7%（粗い分母 141）〜17.6%（DB 偽陽性を除く 68）〜11.4%（EXEC/SPAWN/FS_WRITE 限定 35）** と動き、`r_dom` は 0.0%。**したがって分岐 1 と分岐 2 のどちらにも落ちうる。前測から分岐を予言しない。** ツールパッケージ母集団はどの取り方でも `r_kind = r_dom = 0.0%` で分岐 3 に落ちる。**前測は AuthGap の val エンジンを持たない粗い近似（効果はエントリ本体内のみ、制御位置は構文的同居で近似、手続き間解決なし、star 順フレーム、1 リポジトリが 3155 エントリ中 1029 を占める）であり、F0a の結果で置き換える。食い違ったら F0a を採る。**

**反証条件（4 つとも事前登録する）**

- **(F1)** 月 3 と月 10 の凍結時に執行表を再確認し、(i) 版が `==` / lockfile で確定するリポジトリ、(ii) その版が低レベル経路で入力検証を持たない、(iii) その経路で危険効果が解決する — の 3 つが同時に成り立つユニットが 5 件未満なら **D_dom 層は実装せず `r_dom = 0` として報告する**。
- **(F2)** F0a で `r_kind` が、**偽陽性クラスを除いた分母**で 20% 未満なら分岐 2 または 3 に落とす。**粗い分母 141 での値では判断しない。**
- **(F3)** wild run で `GAP_DRIFT` が 0 行なら D_prev を主張から外し「リリース間で実効権限の拡大は観測されなかった」という測定結果としてのみ報告する（前測での効果 kind 変化率は 0.20% = 3/1525 なので 0 行は十分ありうる）。
- **(F5)** 第 1 週に `self_granted` を Def 5 に入れても S1′（doris）の両版のタプルが同一なら、本対は両側対から落としクラス 2′ の動機付け例としてのみ引用する。

**方向そのものを疑うべき条件**: 両母集団で `r_D < 5%` **かつ** `r_prev < 50%` **かつ** validator 保有ツールが 5% 未満なら、この方向の現場価値は inventory 生成に縮む。その場合は代替主張の測定研究として設計し直す。**annotation 明示率の単独閾値は使わない**（層が 4 つある以上 1 層の率で方向を判断しない）。

---

## 11. 既知のリスク

1. **母集団によって D の層が違う。** ツールパッケージ母集団では D は 0（0/191）であり、MCP サーバ母集団でも D を支えるのは効果 kind の annotation だけで値域制約ではない。**D_dom 層は前測では母集団が 0 であり（観測された 3 件はいずれも実行時に執行される高レベル経路 = Def 5 側）、実装は F0a の条件付きである**（Def 6、反証条件 F1）。形式的コアは変えない。対処は §10 の D 規則。
2. **選択セルの ground truth**。dispatch 証人（`GAP_SELECT`）の実 CVE 対は 1 件（A11）だが、**脆弱側の候補集合は `globals()` と `__main__` で静的に解決できないので verdict は `UNKNOWN(opaque)` であり `GAP_SELECT` ではない。** MCP サーバでは trig が常に assumed なので野外で発火しないことも変わらない。**この穴は塞がっていない。** 被覆漏れ（`Leak`）は SELECT の代替ではなく別の主張であり、第 1 年は manifest 属性に留める。残る危険は 4 つ — (a) 発生ゲート保有率が低ければ発火しない、(b) 発生ゲートを 1 つ持つパッケージでは同一 kind の残り全サイトが漏れ扱いになり批評 2.6 と同じ爆発が別の入口から再発する、(c) 規則 W-occ は正当な非対称（運用者専用 CLI、移行スクリプト）を偽陽性にする（doris の良性メタデータ経路がその実例）、(d) ゲート条件が呼び出し元の引数に依存する形は文脈非依存計算では捉えられない。
3. **交差行数の閾値 3 に経験的根拠が無い。** 事前に固定することだけが根拠。**`≤ 2`（実装変異）、`≥ 5%`（野外発火率）、`≥ 15%`（発生ゲート保有率の参考値）、PraisonAI 上限 3 も同じ扱いである。**
4. **val エンジンが 0% 構築済み**で critical path。§2.6 で仕様化し 10 fixture で pin したが、**F4 と F10 は未確定**であり、`docs/val_design.md` の部品別見積もり（旧「建設週」単位で v0 8.5 / 全仕様 14.5）は本計画の学生週会計とは別単位である。**AI が v0 をカレンダー上の余裕内に出せなければ月 5.2 の脈拍でそれが露見し、v1 の 2.0 が D1 へ返る。**
5. **超過は 0 だが余裕も 0 である。** §7.3 のとおり、34.0 に収めるために切り詰め順序 (1) と (5) を先に使い切った。D1 の 2.0 は残してある。**前身では建設のたびに同程度の監査・再発行コストが発生した（1 回の建設バーストに対し指摘 99 / major 34 / 未了 9）。** 検証負荷則（§7.1）の実測が 1.5 週/kLOC を超えたら §7.4 を 1 段適用する。**実効 46 週という数字自体が未検証の見積もりであり、D5 の `docs/budget.md` で 40 週だと判明した場合は §7.4 を 2〜3 段まとめて適用することになる。**
6. **支配判別が実データで発火した実績が無い。** 前身の実装では実ターゲット 33 件で guard-dominates 事象が 0 だった。**監査 finding F により、残った 2 件の TP はどちらも保守フォールバックだけで立っており、両方を外すと 56 テスト緑のまま両フラグが消えることが確認されている。すなわち前身が測っていたのは「ガードの不在」ではなく「判定の不能」である。** §2.5 の 4 つの構造変更はこの診断に対する応答であり、G1–G15 はその 1 つずつを pin する。前身を実測すると HEAD で 15 件中 11 件が誤り、うち 4 件は誤って clear / clean する不健全方向だった。**さらに `f7aced6` → HEAD で G2 と G4 の判定が逆向きに変わっており、AST 兄弟文方式は穴を塞ぐたびに別の正しい形状を落とす。** **ただし 15/15 撃破は野外での発火を意味しない。** リスク 6 が消えるのは §10 の野外支配発火率の行を通ったときだけであり、T2 の結果を報告するときは必ずこの発火率と OPAQUE 内訳を隣に置く。**`Leak` も同じ支配判定機構の上に載っているので、リスク 6 が実現すれば同時に死ぬ。** 前身がこの機構に費やした週数は記録に残っていないので数字を書かない。
7. **第二ラベラーの離脱**。成功分岐（T3）と null 分岐（κ）の両方の critical path にあり代替が無い。§8-2 の縮退設計を第 0 週に書く。**slot 語彙の拡張でラベリング項目数が増えるので、20〜40h に収まらなければ主 slot 7 種に限定する**（§6）。
8. **同時期の競合研究**。TaintP2X（ICSE 2026）/ MCP-BiFlow（2026-05）/ AgentFlow（2026-07）/ IAL-Scan（2026-07）は同一グループ（Hou / Zhao / Wang ら）が **10 か月で 4 本**出しており、うち MCP-BiFlow は既に AuthGap の較正対（mcp-server-git、Python）を含むベンチマークを公開している。**枠組みの変更によりこれは存立の脅威ではなくなったが、比較対象が動く速度は速い。** 対処は月 6 の凍結時に §1.5 を再走査し、埋まった軸を主張から外して残りに寄せること。
9. **較正対の偏りと汚染**。算入可能 11 対のうち PraisonAI が上限適用後で 3 対、mcp-server-git が 4 対を占める。PraisonAI のコミットの相当数は AI エージェントによる自動生成であり、修正の質と意図が人手のものと異なる可能性がある。**A7–A18 は全て設計汚染済み較正であり、held-out 層は空である。** 月 6 凍結後に MODEL 主体を持つ advisory が出ない可能性は排除できない。
10. **前測の再現性**。付表 D-1（§6 に相当する前測数値）のうち「依存版」と「低レベル経路の join」の 2 系統は、コーパスが `requirements*.txt` と lock ファイルを含まず、repo ごとの commit SHA も記録されていないため**現時点で再現できない**。論文本文へは F0a の値のみを引用し、前測は「設計判断のための粗い前測」として付録に置く。

---

## 12. 用語

| 用語 | 意味 |
|---|---|
| 実効権限 M | コードが実際にモデルへ渡している権限。trig / val / gate から推論する |
| 宣言権限 D | 4 層。D_kind（MCP annotations、untrusted hint、効果 kind の上界）/ D_dom（執行されない機械可読な値域制約。前測で母集団 0）/ D_op（ホスト承認リスト・exposure・アプリ木の permissions。host が執行）/ D_prev（直前リリースの M）。無ければベースライン P0 |
| 執行性規則 | 実行時に執行される制約は Def 5 の値検証（M 側）、執行されない制約は Def 6 の宣言（D 側）。同じ構文が登録経路と SDK 版で役割を変える |
| trig | 効果の発生を誰が決めるか。制御依存。ツール選択 |
| val | 各制御位置の値を誰が決めるか。データ依存。**等級は付けない（属性のみ記録する）** |
| gate | 要求主体を引き上げる承認割り込み（`req_occ`）または値検証（`req_val`） |
| 制御位置 / slot | sink の引数のうち危険性を決める位置。**Def 3（§2）の kind 別 slot 語彙**（§2.5 は支配判定の節であり slot 語彙を含まない） |
| 発生ゲート | `req_occ` を引き上げうるゲートのうち承認割り込み以外の 4 形態。**第 1 年は manifest 属性で verdict を持たない** |
| `Cov` / `Leak` | g がゲートする効果集合 / 同一副 kind でありながら等級 g 以上のゲートにゲートされない効果集合。属性。格上げ条件は Def 5-b |
| pass-semantics 支配 | 「g が評価される」ではなく「g の拒否側から効果へ到達できない」こと。§2.5.2 の `(G-i)∧(G-ii)` |
| 3 値支配 | `DOM(grade) / NODOM(reason) / OPAQUE(reason)`。合成の優先順は `NODOM > OPAQUE > DOM` |
| 連結経路 | selector → dispatch → callee → sink。**ユニット入口から下向きに歩く** |
| 両側条件 | 脆弱版と修正版の両方に同一の効果サイトが存在し、報告タプルが事前登録どおりに変化すること（§6 T1.1） |
| 両側通過率 | head-to-head の主指標。同一の対集合に対する両側条件の充足率を AuthGap と各 baseline で計算する |
| verdict-clearing 数 | 両側通過対のうち修正版で verdict が GAP から外れる対の数。必ず併記する |
| 規則 W | weak validator は宣言に優先する（Def 7）。**規則 W-occ は採用しない** |
| G-mutant / 実装変異 | 付録 G の解析対象スニペット 15 件 / 支配判定の実装に入れる 15 個の変異。**別物** |
| F0a / F0b / F0c | 支配判定なしの床 / 支配判定入り / 4 条件の新規測定（(ii) は測定不能） |
| 解析指紋 | `docs/fingerprint.json`。§6 の凍結を参照 |
| opaque | 解決できなかった呼び出しや位置。**決して clean にしない** |
| 学生週 | 学生本人の手が塞がる週（仕様 + 検証 + 修正ループ）。AI の構築時間は含まない（§7.0） |

---

## 13. 参照できる既存資産（前身リポジトリ、任意）

前身は `~/Project/research/Master_Project/dispatch-taint-system`。**論文には使わない**が、次は書き直すより流用が速い。**追試するときは commit ではなく sha256 で pin すること**（実測は commit `18a61d9`、`selection_guard.py` の sha256 `484c65a7…`、2910 行、Python 3.10.12 に対して行った。`f7aced6` ではない）。

| 資産 | パス / シンボル | 判定 |
|---|---|---|
| ソース索引 | `selection_guard.py` の `SourceIndex._parse` / `_build_module_map` / `file_defs` / `imports` / `resolve_module_path`（:387–474） | **そのまま流用**。sorted walk による決定論、parse 失敗の記録、import 表。**ただし `imports()` は `ast.walk(tree)` でモジュール全体を舐めるため関数ローカル `import` も平坦な表に混ざりスコープを無視する。val では `(モジュール, 関数)` 粒度に拡張する** |
| sink 弁別規則 | `match_sink` + `SINKS`（:168 / :247） | **半分流用**。`_dbish_receiver` の全単語一致、`_urlish_expr`、alias / from-import 解決は価値がある。**戻り値がラベル文字列 1 個で slot 束縛が無く proxy / pipe 形態も無いので `(kind, {slot → セレクタ}, form)` を返す表に書き換える（新規）** |
| 受け手推論 | `_ctor_class`(:548) / `_self_attr_ctor`(:582) / `_factory_returns`(:617) | **そのまま流用**。`_self_attr_ctor` はクラス体のフィールド既定値と `__init__` の両方を見る。`_factory_returns` は `IfExp` の両枝を返す。**ただし 3 関数とも `(file, classname)` しか返さず ctor の引数値を返さないので、`Obj.fields` の束縛は新規実装である** |
| 引数整列 | `_func_params`(:1152) / `_qualname`(:183) / `_str_const` | **流用** |
| `_last_assign_rhs`(:1111) | — | **流用しない**（`ast.walk` 順で「行番号が最大の代入」を採るだけで分岐・ループ・スコープを無視する）。val の `Env` が置き換える。proxy 受け手型付けのフォールバックとしてのみ残してよい |
| `reaches_sink`(:635) | — | **流用しない**。理由 4 つ: (1) 真偽値で値も位置も持たない、(2) 最初の sink で `return` するので全効果を列挙できない、(3) `find_method` が同一ファイル内の同名メソッドを無条件に採る、(4) `ast.walk(fn)` で文順を無視する |
| **ガード判定** | `stmt_is_guard` / `guard_dominance`(:1741) / `interproc_guard`(:2282) | **流用禁止。** 既知の major 欠陥（AST 兄弟文による擬似支配、`_is_exit_body` の全 exit 要求、`or` の極性、名前トークンのみのゲート認識、上向き呼出元探索の保守フォールバック、真偽 2 値による OPAQUE の潰し、候補 0 の wall の無言破棄）。§2.5 の仕様で新規に書く。**参照してよいのは反例集合としてのみ**（付録 G の「前身の実測」列） |
| LLM 呼び出しカタログ | `llm_call_methods` 収集 | R1 の出発点 |
| 大規模走査ハーネス | `scale/` | **移植しない。** AuthGap は venv も型環境も作らないので再試行・再開の機構は不要。逐次ランナー 60 行で置き換える（§7.3） |
| フレームワーク判定 | `spec.presets.json` の 11 プリセット | **エントリ発見は新規に書く**（CrewAI / agno / 低レベル MCP の 2 形 / LangGraph / gptme は未収録） |
| ガード mutant コーパス | `diffbench/` | T2 の出発点。**設計汚染済み較正として扱う。** held-out mutant は月 6 凍結後に新規生成する。**両者を混ぜて 1 つの判別率を出さない。この規則は付録 G の G-mutant にも及ぶ** |
| 前測スクリプト | **本 repo の `scripts/premeasure/`**（`scan.py` / `lowlevel.py` / `drift2.py` / `stats.py` / `drift.sh`、計 591 行）。**2026-09-09 に移送済みで sha256 は `scripts/premeasure/PROVENANCE.md` と照合して一致を確認した。D1 の移送作業は完了しており、§13 の代償条項（前測数値の削除と A5 の 1.0 復帰）は発火しない。** 前測コーパスは commit SHA が無く**再現できない**ので、数値を取り直す場合はフレームを引き直して測り直す |
| 前測の再現不能部分 | 依存版の集計、低レベル経路の join | **スクリプトが保存されておらず現時点で再現できない。** `deps.py` と `driftdiff.py` として明文化し F0a の一部として実行する |

**流用してはいけないもの**: lowering パス、`engine_walls.py`、`links.py`、`anchoring.py`、cond_A / cond_B の対照実験、`links.json` を ground truth として使うこと（到達不能リンクを約半分含む）。
