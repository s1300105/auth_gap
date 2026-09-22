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

## 結論（2026-09-22、R1 / R2 / R3 とも一次資料を読んだ）

| # | 研究 | 主軸（宣言 D と実効 M の照合）と競合するか |
|---|---|---|
| R1 | HintLint | **最も近い。ただし問いが違う。** 向こうは主に「宣言が**無い**」を数え（65 件中 61 件）、こちらは「宣言が**あって反する**」を数える。**検出力で勝ったとは言えない**（比較可能な 4 件で 1 勝 3 敗） |
| R2 | AgentFlow | **しない。相補的。** 解析対象が違う（下記） |
| R3 | ReactAppScan | しない。**手法の型として引ける** |

**R1 の差分は「解決できなかったものをどう扱うか」に尽きる。** HintLint の確度の語彙は
`source-backed` / `needs-review` の 2 語で、**未解決を表す語が無い**。正規表現に当たらなければ
分母からも消えるので、「宣言がどれだけ当てにならないか」という**率の問い**には答えられない。
AuthGap は `opaque(reason)` 8 語と `truncations` / `budget_skipped` で残し、率を報告する。

**R2 は当初「グラフ化案と競合する」と見ていたが、一次資料を読んで**相補的**だと分かった。**
AgentFlow が解析するのは**エージェント プログラム（MCP を使う側）**で、MCP サーバの実装は
読まない。しかも論文の限界節が「ツール実装やライブラリ呼び出しの内部を推論する仕事には
ADG は使えず、points-to 解析と組み合わせる必要がある」と自ら書いている。**そこが AuthGap の
守備範囲である。**

**O19 の判断は (a)「測定研究として立て直す」である**（2026-09-22、D40）。(c) ではない:
R1 が同じ現象を先に触っているので「初めて照合した」とは書けない。書けるのは
**母集団の定義・事前登録・未解決の率の報告**であり、それは (a) の内容そのものである。

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

## R1. HintLint — MCP の注釈と実装の照合（**主軸と最も近い。ただし問いが違う**）

| 欄 | 内容 |
|---|---|
| 種別 | ツール（GitHub リポジトリ）。**論文は見つかっていない**（repo 内に引用形式・arXiv 番号・`paper` 系ファイルなし） |
| 読んだ範囲 | **ソース本体**（`src/extractors/python.js` 143 行、`src/evidence/static-detector.js` 716 行、`src/coverage.js`、`src/index.js`）+ ページ。`5a51f2a4`（2026-09-11）、JavaScript / Node、8,626 行 |
| 実行 | 母集団 v2 の 87 木すべてで走らせた。`scripts/hintlint_compare.py` → `evidence/hintlint_run1/summary.json` |

### 確認済み（ソースを読んだ）

- 目的は「annotation drift」の検出。宣言（`readOnlyHint` 等）と実装の食い違いを静的に見る。
- 対応言語は TypeScript / JavaScript / Python。検出規則は 6 種
  （`READONLY-001` / `DESTRUCTIVE-001` / `OPEN-WORLD-001` / `FLOW-PROCESS-001` /
  `FLOW-QUERY-001` / `FLOW-FILESYSTEM-001`）。
- **Python 経路は AST ではなく行単位の正規表現である。** `src/extractors/python.js` の
  `startsToolDecorator = /@(?:\w+\.)?tool(?:\s*\(|\s*$)/`。`collectFunctionText` は次の
  `def` か次の `@tool` までの行を集めるので、`_analysis.text` は**そのツール関数の本体だけ**になる。
- **Python 側に到達解析は無い。** `src/evidence/typescript-reachability.js` は存在するが
  `python` の出現が 0 件。**呼び出しをまたがない。**
- sink は `static-detector.js` の **10 個の `SINK_RULES`** を本体テキストに正規表現で当てる。
  `scope: "project"` の規則だけ木全体の行に当て、その場合 `confidence: "needs-review"` を付ける。
- 確度の語彙は `"source-backed"` / `"needs-review"` の 2 語。**解決できなかったものを表す語は無い。**
- `handlers_resolved` は「デコレータからハンドラの本体を取り出せたか」の数であって、
  値や効果が解決できたかではない（`src/index.js:41`, `tool.handler?.confidence === "resolved"`）。

### 未検証（ページの記載を写しただけ。CLAUDE.md 規則 1）

- 20 リポジトリ 1,160 ツールで 23 件、精度 82%（2026 年 7 月の findings report とある）。
- handler resolution rate が TS/JS 88%、Python 100%。

### 実測 — 母集団 v2 の 87 木で両方を走らせた

再現: `.venv/bin/python scripts/hintlint_compare.py --hintlint <clone> --label run1`

| | HintLint | AuthGap（`evidence/scan_v2_run4`） |
|---|---|---|
| 入口 | ツール 13,083（`coverage_status`: supported 81 木 / unsupported_pattern 4 / not_mcp_server 2） | ユニット 2,231 |
| 検出 | finding 81（うち readOnly / destructive の **65**） | CONTRADICTION 79（ユニット × (site, kind)） |
| 木の重なり | **両方に出た木 2、HintLint だけ 5、AuthGap だけ 14** | |

**入口を揃えた比較ではない**（HintLint は自分でツールを抽出するので、同じ入口集合を渡す
手段が無い）。したがって件数の大小は比較にならない。**見るべきは「何が見えて何が見えないか」。**

#### (1) そもそも問いが違う — 65 件のうち 61 件は「宣言が無い」ツール

HintLint の `DESTRUCTIVE-001` は **`destructiveHint` が**無い**ツールに対して発火する**。
実測で、比較可能な 65 件の `declared_annotations` は:

| 宣言 | 件数 |
|---|---|
| `{}`（**宣言なし**） | **61** |
| 宣言あり（AuthGap の CONTRADICTION と同じ問い） | **4** |

AuthGap の CONTRADICTION は**明示の宣言 D があってそれに反する**ことを要求する
（宣言の無いツールは INVENTORY 側の問い）。**したがって 61 件は同じ現象を数えていない。**
**真に比較できるのは 4 件だけである。**

#### (2) その 4 件の突き合わせ（AuthGap は 1 勝 3 敗）

| 木 / ツール | HintLint | AuthGap | 差の原因（一次確認した） |
|---|---|---|---|
| `dddabtc/winremote-mcp` / `PlaySound` | DESTRUCTIVE-001（`subprocess.run(` 1 件） | **CONTRADICTION**（`open` FS_WRITE / `subprocess.run` SPAWN ×2 / `os.unlink` FS_WRITE の 4 効果） | **一致。**AuthGap の方が効果を多く出している |
| `letsgojh0810/godsaeng-salon` / `check_reminders` | READONLY-001（`UPDATE reminders SET`） | CONTRADICTION **なし**（DB 効果 7 件は出ているが GAP_INJECT / UNKNOWN のみ） | **設計差。**`verdict.py` の CONTRADICTION は `eff.kind in ("EXEC","SPAWN","FS_WRITE")` に限る（`DESTRUCTIVE_KINDS`、D32）。**`readOnlyHint:true` + DB 書き込みは AuthGap の CONTRADICTION に入らない** |
| `rwheeler007/cohort` / `internal_web_fetch` | READONLY-001（`mkdir(`） | 効果 **0 件** | **AuthGap の誤 clear（false-clean）。**`cohort_root = Path(__file__).resolve().parents[2]` → `cache_dir = cohort_root / ... ` → `cache_dir.mkdir(...)`。`Path(...).parent` / `.parents[n]` が受け手の Path 形を落とすため `pathlib.Path.mkdir` の sink 行に当たらない。**`opaque_reasons` に `receiver` は残るが行が 1 本も出ない** |
| `mcparmory/registry` / `delete_snapshot_by_delete_key` | READONLY-001 | ユニット**そのものが無い** | **`AST_NODE_CAP` の打ち切り**（下記 (4)）。`servers/grafana/server.py` は 54,192 ノードで cap 20,000 を超え、`truncations` に記録されている |

**誤りの向きを明記する。**(3 行目) は**誤 clear 方向**（危険を見落とす側）である。
最小再現で原因を切り分けた: `Path("/tmp")/"x"`・`Path("/tmp").resolve()` は sink に当たり、
**`Path("/tmp/a/b").parent` だけが当たらない**。`docs/open_questions.md` の作業一覧に置いた。

#### (3) HintLint が見ているのは関数本体の 0 段だけ

AuthGap が母集団 v2 で CONTRADICTION を出した起点 API は **13 種**。HintLint の **10 個**の
`SINK_RULES` を実際に node で当てると、当たりうるのは **4 種**
（`subprocess.run` / `shutil.rmtree` / `Path(...).mkdir(` / `open(...)`）。
残り 9 種（`os.unlink` / `os.remove` / `os.replace` / `os.chmod` / `os.makedirs` /
`Path.unlink` / `Path.write_text` / `Path.write_bytes` / `Path.open`）はどの規則にも当たらない。
**`open` も無条件ではない**: 規則は
`/\bopen\s*\([^)]*(?:destination|path|file|artifact)[^)]*["'](?:w|a|wb|ab)["']/i` で、
引数の字面に `destination|path|file|artifact` のいずれかが無いと当たらない
（`open(f, "w")` は当たらない）。

AuthGap の CONTRADICTION 効果 130 件の**呼び出し段数**:

| 中間フレーム数（`witness_chain` の長さ） | 件数 |
|---|---|
| **0（ツール関数の本体内）** | **4（3.1%）** |
| 1 | 27 |
| 2 | 39 |
| 3 | 57 |
| 4 | 3 |

**1 段以上が 126 件（96.9%）。** API 種で当たりうるのは 46 件（35.4%）だが、
**両方の条件（0 段 かつ 当たりうる API）を満たすのは 130 件中 3 件（2.3%）。**

`mcparmory/registry` の 48 件を目視すると、当たっている sink は
`DeleteCustomFieldActivityCustomFieldIdRequest(` のような **pydantic のリクエスト模型の
コンストラクタ**であって、削除そのものではない。実際の削除は
`_execute_tool_request(method="DELETE", ...)`（`servers/close/server.py:810` のモジュール水準の
補助関数）で、**ツール本体の外＝ 1 段降りた先にある**。
**判定は正しいが、根拠として挙げた行は削除ではない**（名前の一致で当たった）。

#### (4) 公平性のための自己申告 — AuthGap 側の打ち切り

| 木 | 事情 |
|---|---|
| `david-li0406/meta-skill-evloving` | **AuthGap は 180 秒の tree budget で打ち切られ、ユニット 0 件**（`budget_skipped: 716`、511.6 秒）。HintLint は比較可 12 件。**この木は比較として成立していない** |
| `mcparmory/registry` | `@mcp.tool` が 10,170 個。**うち 9,524 個（93.6%）が `AST_NODE_CAP`（20,000 ノード）で切られたファイルの中**にある（64 ファイル、`truncations` に記録）。AuthGap のユニットは 646 個 |

母集団 v2 全体では `@tool` 系デコレータ 12,713 個のうち **9,816 個（77.2%）が切られたファイル内**だが、
**その 9,524 個が `mcparmory/registry` 1 本**である。**この 1 木を除くと 292 / 2,543 = 11.5%。**
`mcparmory/registry` は生成された MCP サーバを集めた単一リポジトリで、母集団の他の木と性質が違う。
**分母の扱いは決まっていない**（`docs/open_questions.md` O21）。

### 結論 — 競合だが、問いと分母が違う

| 論点 | HintLint | AuthGap |
|---|---|---|
| 主に数えているもの | **宣言が無い**ツールの危険（65 件中 61 件） | **宣言があって反する**ツール（CONTRADICTION） |
| 解析 | Python は行単位の正規表現。**本体 0 段のみ、呼び出しを追わない** | AST + 値解析。**CONTRADICTION の 96.9% は 1〜4 段降下** |
| 解決できないもの | **語彙が無い。** 正規表現に当たらなければ何も残らない（率を報告できない） | `opaque(reason)` 8 語 + `truncations` + `budget_skipped` で残し、率を報告する（52.8%） |
| 母集団 | 20 リポジトリの pilot（選び方は未検証） | 宣言ありを 3,827 件列挙 → 87 木を SHA pin、事前登録 |
| 範囲 | `openWorldHint` と flow 規則 5 種を持つ | `openWorldHint` 未実装。DB / NET は CONTRADICTION に入れない |
| 目的 | CI に載せる linter。精度優先で不確かなものを落とす | 測定研究。落とさずに率で報告する |

**「解決できなかったものをどう扱うか」が最大の差である**（`docs/open_questions.md` O19 の
最重要の確認点だった）。**HintLint には未解決を表す語彙が無く、正規表現に当たらなければ
分母からも消える。** したがって「MCP サーバの宣言がどれだけ当てにならないか」という
**率の問い**には答えられない。AuthGap の位置づけは「同じ現象を linter でなく**測定**として
やる」であり、**検出力で勝ったという主張はできない**（上の (2) は 4 件中 1 勝 3 敗）。

### この比較の限界（本文の限界節に書く）

1. **HintLint の TS / JS 経路は見ていない。** そちらには到達解析があり、母集団 v2 が
   Python の MCP サーバだけなので設計全体の評価になっていない。
2. **入口を揃えていない。** `scripts/codeql_fair.py` と違い、HintLint に同じ入口集合を
   渡す手段が無い。件数の大小は比較にならない。
3. **比較できた事例が 4 件しかない。** この標本で優劣は言えない。

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

- **HintLint の論文の有無。** repo 内に引用形式・arXiv 番号・`paper` 系ファイルが無く、
  この実行環境からは検索できなかった（**「無い」ではなく「確かめられなかった」**）。
  学会発表や preprint があるなら比較の書き方が変わる。
- **HintLint の TS / JS 経路**（到達解析つき）の評価。母集団 v2 が Python だけなので未評価。
- CodeQL / Semgrep / Pysa との位置づけ（`scripts/codeql_fair.py` の比較はあるが未整理）。
- AgentFlow が比較対象にした AGENT-WIZ / AGENTIC RADAR。
- AgentFlow の引用にある MCP 関連（MCPTox ほか）、AgentArmor / Agentproof / Agent Audit。
