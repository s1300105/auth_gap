# 先行研究（読んだ結果）

**この文書の規則。**

1. **一次資料（論文本体 / リポジトリ本体）を読んだ項目だけ「確認済み」と書く。**
   検索結果の要約や二次情報から書いた項目は **未検証** と明示する（CLAUDE.md 規則 1）。
2. **PDF 本体は repo に入れない。** 公開リポジトリなので著作物を配布することになる。
   置き場は `papers/`（`.gitignore` 済み）で、コミットするのはこの文書だけ。
3. 各項目に **出所**（どの節を読んだか）を書く。後から確認できるようにする。
4. **重なりは正直に書く。** 「うちの方が優れている」ではなく「何が同じで何が違うか」。

未記入の欄は `（未記入）` のまま残す。**埋まっていない欄を推測で埋めない。**

---

## 結論（2026-09-22、R2 と R3 を読んだ時点）

| # | 研究 | 主軸（宣言 D と実効 M の照合）と競合するか |
|---|---|---|
| R1 | HintLint | **する。直接の競合。** 比較対象に据える |
| R2 | AgentFlow | **しない。相補的。** 解析対象が違う（下記） |
| R3 | ReactAppScan | しない。**手法の型として引ける** |

**R2 は当初「グラフ化案と競合する」と見ていたが、一次資料を読んで**相補的**だと分かった。**
AgentFlow が解析するのは**エージェント プログラム（MCP を使う側）**で、MCP サーバの実装は
読まない。しかも論文の限界節が「ツール実装やライブラリ呼び出しの内部を推論する仕事には
ADG は使えず、points-to 解析と組み合わせる必要がある」と自ら書いている。**そこが AuthGap の
守備範囲である。**

したがって **O19 の判断は (c)「主軸を変えない」でよい**（ただし R1 の一次確認が残る）。

---

## 入手先

| # | 論文 / ツール | URL | 状態 |
|---|---|---|---|
| R1 | HintLint | https://github.com/complira/hintlint | ページのみ読了。**コード未読** |
| R2 | AgentFlow | https://arxiv.org/abs/2607.01640 | **PDF 読了**（学生が提供） |
| R3 | ReactAppScan | https://doi.org/10.1145/3658644.3670331 | **PDF 読了**（学生が提供） |
| 参考 | MCP 公式「Tool Annotations as Risk Vocabulary」 | https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ | 読了 |

この実行環境からは R2 / R3 とも egress proxy で遮断されており、直接は取得できない。

---

## R1. HintLint — MCP の注釈と実装の照合（**主軸と直接競合する**）

| 欄 | 内容 |
|---|---|
| 種別 | ツール（GitHub リポジトリ）。論文の有無は（未記入） |
| 読んだ範囲 | **README 相当のページのみ（2026-09-21、WebFetch）。コード本体は未読** |

### 確認済み（ページを読んだ）

- 目的は「annotation drift」の検出。宣言（`readOnlyHint` 等）と実装の食い違いを静的に見る。
- 対応言語は TypeScript / JavaScript / Python。
- 検出規則 6 種:
  `READONLY-001`（readOnly 宣言なのに書く）、`DESTRUCTIVE-001`（破壊的 API に
  `destructiveHint` が無い）、`OPEN-WORLD-001`（`openWorldHint=false` なのに外部通信）、
  `FLOW-PROCESS-001` / `FLOW-QUERY-001` / `FLOW-URL-001`。
- **「source-backed findings」に限り、metadata-only の検出を意図的に避ける設計。**

### 未検証（ページの記載を写しただけ）

- 20 リポジトリ 1,160 ツールで 23 件、精度 82%（2026 年 7 月の findings report とある）。
- handler resolution rate が TS/JS 88%、Python 100%。

### AuthGap との重なりと違い（**コードを読んでから確定する**）

| 論点 | HintLint | AuthGap | 差（未確定） |
|---|---|---|---|
| readOnly 違反 | `READONLY-001` | CONTRADICTION（readOnlyHint） | 同じ |
| destructive 違反 | `DESTRUCTIVE-001` | CONTRADICTION（destructiveHint、**削除型のみ** D32） | 追記型を除くかが差 |
| openWorld 違反 | `OPEN-WORLD-001` | **未実装** | 向こうが広い |
| 解決できない部分 | source-backed に限る（**落とす**） | opaque として残し率を報告（52.8%） | **ここが最大の差の候補** |
| 母集団 | 20 リポジトリの pilot | 宣言ありを 3,827 件列挙 → 87 木を SHA pin | 母集団の定義の有無 |
| 事前登録 | （未記入） | 分母・閾値を測定前に凍結、逸脱 11 件 | （未記入） |

### 次に確認すること

1. 呼び出しをまたいで追うか（AuthGap は CONTRADICTION の 57 件が 3 段降下）。
2. **解決できなかったものを落とすなら、分母から消えるので率は報告できない。** ここを確認する。
3. 82% の分母と ground truth の作り方。
4. 20 リポジトリの選び方（母集団の定義があるか）。

---

## R2. AgentFlow — Agent Dependency Graph（**相補的。競合しない**）

| 欄 | 内容 |
|---|---|
| 書誌 | Shenao Wang, Xinyi Hou, Yanjie Zhao, Xiao Cheng, Haoyu Wang（華中科技大学 / Macquarie 大学）。arXiv:2607.01640v1 [cs.SE]、2026-07-02 |
| 読んだ範囲 | **全 12 ページの本文**（Abstract / §I / §II / §III / §IV-A,B,C / §V 冒頭 / §VI 限界 / §VII）。評価の表は未精読 |

### 確認済み

**解析対象は「エージェント プログラム」= MCP を使う側のコード。** 論文の scope
（§II-A）は「agent frameworks で書かれた agent program」で、**Claude Code のような
エージェント製品と低コード エージェントは明示的に除外**している。MCP サーバの実装は
対象外である。

**ADG の定義**（§IV-A）。`ADG_P = ⟨ACDG_P, ACFG_P, ADFG_P⟩`（component dependency /
control flow / data flow）。ノード集合は `V = A ⊎ I ⊎ M ⊎ C ⊎ S ⊎ G`
（agent / prompt / model / capability / state / policy）。

**MCP の扱い**（§IV-B、Fig.4）。クライアント側の `HostedMCPTool(...)` を読んで
`MCPDef` ノードと `BindMCP` 辺を作る。承認方針は `BranchIf(ApprovalPolicy, SendEmail)`
として ACFG の条件分岐になる。**つまり MCP ツールは「URL つきのノード」であって、
その中身は読まない。**

**注釈（`readOnlyHint` 等）は扱っていない。** 本文全体で `readOnlyHint` /
`destructiveHint` / `openWorldHint` / `annotation` の出現は **0 件**（全文検索で確認）。
**宣言と実装の照合という問いは立てていない。**

**応用は 2 つ**（§IV-C）。Agent BOM 生成（ACDG を辿って各エージェントの構成要素を集める）と、
prompt-to-tool risk 検出（`P2T(P) = {(p,a,c) | (p,a)∈R_pa, (a,c)∈R_ac, (a,c)∈E_arg}`。
prompt 由来のデータが特権 capability の**引数**に届くか）。**これは prompt injection の
到達性であって、宣言との照合ではない。**

**評価**。AgentZoo = GitHub から 5 フレームワークの import を code search で集め、fork と
archive を除き、フレームワーク構造の無いものを落として **5,399 プロジェクト**
（LangChain/LangGraph 3,823、CrewAI 947、OpenAI Agents SDK 442、LlamaIndex 146、
Semantic Kernel 41）。default branch の最新スナップショット。prompt-to-tool risk を
**238 件**検出。フレームワーク構造は 5 フレームワークで **143 構造**をモデル化。Python のみ。

### **限界節が AuthGap の位置を決めている**（§VI、著者の言葉）

> ADG captures high-level framework semantics and **does not replace low-level program
> dependency analysis. For tasks that require reasoning inside tool implementations or
> library calls**, ADG can be combined with points-to analysis to track the full taint
> propagation paths.

**「ツール実装の内部を推論する仕事」= AuthGap の守備範囲**であり、著者自身が ADG では
できないと書いている。したがって両者は相補的で、AuthGap は「AgentFlow が名指しした穴を
埋める側」として位置づけられる。

他の限界も 4 つ挙げている。過大近似による偽陽性、**フレームワーク API の慣習に従わない
自作構造には効かない**（AuthGap の `ENTRY_RULES` と同じ問題。引用できる）、Python と
5 フレームワークのみ、フレームワークの変化に追随する必要。

### AuthGap との対比（本文に書ける形）

| 論点 | AgentFlow | AuthGap |
|---|---|---|
| 解析対象 | エージェント プログラム（MCP を**使う**側） | MCP サーバ（ツールを**実装する**側） |
| MCP ツール | URL つきのノード。中身は読まない | 本体を読み、効果 kind を出す |
| 宣言（注釈） | 扱わない（出現 0 件） | 主軸 |
| 危険の定義 | prompt が特権 capability の引数に届く | 宣言の上界に反する効果がある |
| 母集団 | AgentZoo 5,399（フレームワーク import で収集） | 宣言あり 3,827 → 87 木を SHA pin |
| 承認方針 | クライアント側の `ApprovalPolicy` を分岐として持つ | サーバ側の承認割り込み（付録、D36 で降ろした） |

---

## R3. ReactAppScan — Component Graph（**手法の型として引ける**）

| 欄 | 内容 |
|---|---|
| 書誌 | Zhiyong Guo, Mingqing Kang（Johns Hopkins）, V.N. Venkatakrishnan, Rigel Gjomemo（UIC）, Yinzhi Cao（Johns Hopkins）. CCS '24, Salt Lake City, 2024-10-14〜18, 15 ページ. doi:10.1145/3658644.3670331 |
| 読んだ範囲 | Abstract / §1 / §2 の Key Idea / §6.1 評価の設計。**手法の詳細（§3〜§5）と評価の表は未精読** |

**検索結果の書誌は正しかった**（著者 5 名の順序も一致）。

### 確認済み

**問題設定。** React の props / state を通るデータフローを既存解析が追えない。JSX を扱えるのは
CodeQL だけだが、**コンポーネントをまたぐ React Data Flow を追えない**。

**Component Graph（CoG）の骨子**（§2 Key Idea）。

1. コンポーネントを親子関係に従ってノードにし、**state と props をそのコンポーネント
   ノードの下のノードにする**。
2. **別名のオブジェクトは同じ 1 ノードにする。** 例: `BlogDetail` の `content` state と
   `BlogContent` の `content` prop は 1 ノード。React の意味論（親の state が変われば子の
   prop も変わる）に従うから。
3. **クライアント / サーバとデータベースの依存は「キー」で結ぶ。** DB の `content` キー、
   ルータの `/getBlog` とクライアントの fetch を共通のキーで対応づけて CoG に注記する。
4. 構築は**抽象解釈**で、抽象領域がグラフそのもの。JSX の静的構造から始めて React と
   同じ更新手続きをモデル化する。

**CoG は ODG / CPG と相補的で組み合わせられる**と明記している（置き換えではない）。

**評価の設計**（§6.1）。データセットを 2 つ用意する。

- **大規模・ラベルなし**（GitHub と NPM から収集）→ 偽陽性率（FDR）の評価に使う。
- **小規模・ラベルあり**（CVE 付きの歴史的に脆弱なアプリ）→ 偽陰性率（FNR）の評価に使う。

zero-day の認定は 3 条件で、(ii) 手検索で CVE や既存データセットに無いこと、
(iii) **手作業の exploit で検証**すること。61 件を検出し、6 件が修正、2 件が承認された。

### AuthGap に引ける点

1. **「別名は 1 ノード」を資源に写す。** MCP では「同じパス / URL / テーブルを触る複数の
   ツールを 1 ノードにする」に相当する。**サーバをまたぐ合成のリスク**を表すのに要る考え方。
2. **キーで結ぶ**という具体的な機構。ReactAppScan は DB キーとルート名で境界を越えた。
   MCP なら**正規化したパス / ホスト名 / テーブル名**が同じ役割を果たしうる。
3. **評価の 2 データセット構成。** 大規模ラベルなしで偽陽性、小規模ラベルありで偽陰性。
   AuthGap の較正対（CVE）と母集団 v2 は同じ構成なので、設計の正当化に引ける。

---

## 参考: MCP 公式の立場（読了）

[Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)（2026-03）。

- 仕様は「**annotations は tool の挙動を忠実に記述することが保証されず、信頼できる
  サーバ由来でない限りクライアントは信頼できないものとして扱わねばならない**」と明記。
- 「ツールのリスクはセッション内の他の何があるかに依存する」（組み合わせリスク）とも書く。

**この研究の動機の一次資料として使える。** 「宣言が当てにならない」ことは公式に認知済みで、
残る問いは「**実際にどれだけ当てにならないか**」である。これは測定研究の問いである。

---

## まだ書いていないもの

- **R1 のコード読解**（最優先。主軸と直接競合する唯一の研究）。
- CodeQL / Semgrep / Pysa との位置づけ（`scripts/codeql_fair.py` の比較はあるが未整理）。
- AgentFlow が比較対象にした AGENT-WIZ / AGENTIC RADAR。
- AgentFlow の引用にある MCP 関連（MCPTox ほか）、AgentArmor / Agentproof / Agent Audit。
