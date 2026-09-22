# 先行研究（読んだ結果をここに書く）

**この文書の規則。**

1. **一次資料（論文本体 / リポジトリ本体）を読んだ項目だけ「確認済み」と書く。**
   検索結果の要約や二次情報から書いた項目は **未検証** と明示する（CLAUDE.md 規則 1）。
2. **PDF 本体は repo に入れない。** 公開リポジトリなので著作物を配布することになる。
   置き場は `papers/`（`.gitignore` 済み）で、コミットするのはこの文書だけ。
3. 各項目に **出所**（どのページ / どの節を読んだか）を書く。後から確認できるようにする。
4. **重なりは正直に書く。** 「うちの方が優れている」ではなく「何が同じで何が違うか」。

未記入の欄は `（未記入）` のまま残す。**埋まっていない欄を推測で埋めない。**

---

## なぜ急ぐか

`docs/decisions.md` D36 で主張を「宣言 D と実効 M の照合」1 本に絞った。
その直後（2026-09-21）に、**主軸そのものを扱う先行研究**と、**代替案として検討した
グラフ化を扱う先行研究**が見つかった。どちらも 2026 年中頃のもので、主張の位置づけに
直接影響する。`docs/open_questions.md` O19。

---

## R1. HintLint — MCP の注釈と実装の照合（**主軸と直接競合する**）

| 欄 | 内容 |
|---|---|
| 出所 | https://github.com/complira/hintlint |
| 種別 | ツール（リポジトリ）。論文の有無は（未記入） |
| 読んだ範囲 | **README 相当のページのみ（2026-09-21、WebFetch）。コード本体は未読** |
| 状態 | **部分的に確認済み**（下の「確認済み」と「未検証」を分けて書く） |

### 確認済み（ページを読んだ）

- 目的は「annotation drift」の検出。宣言（`readOnlyHint` 等）と実装の食い違いを静的に見る。
- 対応言語は TypeScript / JavaScript / Python。
- 検出規則は 6 種類:
  `READONLY-001`（readOnly 宣言なのに書く）、`DESTRUCTIVE-001`（破壊的 API に
  `destructiveHint` が無い）、`OPEN-WORLD-001`（`openWorldHint=false` なのに外部通信）、
  `FLOW-PROCESS-001` / `FLOW-QUERY-001` / `FLOW-URL-001`（利用者入力が危険位置に届く）。
- 「source-backed findings」に限り、metadata-only の検出を意図的に避ける設計。

### 未検証（ページの記載を写しただけ。一次確認していない）

- 20 リポジトリ 1,160 ツールで 23 件、精度 82%（2026 年 7 月の findings report とある）。
- handler resolution rate が TS/JS 88%、Python 100%。

### AuthGap との重なりと違い（**要記入**）

| 論点 | HintLint | AuthGap | 差 |
|---|---|---|---|
| readOnly 違反の検出 | `READONLY-001` | CONTRADICTION（readOnlyHint） | （未記入） |
| destructive 違反 | `DESTRUCTIVE-001` | CONTRADICTION（destructiveHint、削除型のみ D32） | （未記入） |
| openWorld 違反 | `OPEN-WORLD-001` | **未実装** | （未記入） |
| 解決できない部分の扱い | source-backed に限る（落とす） | opaque として残し率を報告（52.8%） | （未記入） |
| 母集団 | 20 リポジトリの pilot | 宣言ありを 3,827 件列挙し 87 木を SHA pin | （未記入） |
| 事前登録 | （未記入） | 分母・閾値を測定前に凍結、逸脱 11 件を記録 | （未記入） |
| 削除型 / 追記型の区別 | （未記入） | あり（D32） | （未記入） |

### 読むときの問い

1. 規則の実装は AST か正規表現か。呼び出しをまたいで追うか（AuthGap は 3 段が最多）。
2. 「解決できなかった」ものをどう扱うか。**落とすなら分母から消えるので、率は報告できない。**
3. 評価の ground truth は誰がどう作ったか。82% の分母は何か。
4. 母集団の定義があるか。20 リポジトリの選び方。

---

## R2. AgentFlow — Agent Dependency Graph（**グラフ化案と競合する**）

| 欄 | 内容 |
|---|---|
| 出所 | arXiv 2607.01640（2026-07） |
| 読んだ範囲 | **未読。この環境から取得できない（egress proxy で遮断）** |
| 状態 | **未検証**（以下はすべて検索結果の要約） |

### 未検証（検索結果の要約。一次資料で確認すること）

- エージェントプログラムから依存関係を復元する静的解析の枠組み。
- Agent Dependency Graph のノードは agents / prompts / models / capabilities / states /
  policies。エッジは component-dependency / control-flow / data-flow。
- **MCP tool を扱う**とあり、`HostedMCPTool` が approval policy つきの MCP capability を
  作る、という記述がある。
- 比較対象は AGENT-WIZ と AGENTIC RADAR。1 プロジェクトあたり中央値 17 ノード 28 エッジ。

### 読むときの問い

1. **宣言（annotations）と実装の照合をやっているか。** ここが最重要。やっていなければ
   AuthGap の主軸とは競合しない（グラフ化案とだけ競合する）。
2. データフローの範囲。**サーバをまたぐ資源の同定**（別サーバの 2 つのツールが同じパスを
   触る）を扱うか。扱っていなければ、そこが空いている。
3. 解析の対象言語と、入口の認識方法（AuthGap の `ENTRY_RULES` に相当するもの）。
4. 評価の母集団と規模。
5. 限界として何を書いているか。

---

## R3. ReactAppScan — Component Graph（**手法の型として参考にした**）

| 欄 | 内容 |
|---|---|
| 出所 | CCS '24, pp. 585–599. doi:10.1145/3658644.3670331 |
| 読んだ範囲 | **未読。この環境から取得できない（egress proxy で遮断）** |
| 状態 | **未検証**（以下はすべて検索結果の要約） |

### 未検証（検索結果の要約。一次資料で確認すること）

- React の props / state を通る暗黙のデータフローを既存解析が追えない問題に対し、
  Component Graph を構成する。
- **同じオブジェクト実体は props でも state でも 1 ノードにし、複数のエッジを張る**。
- 実世界の React アプリで 61 件の zero-day を検出。

### 読むときの問い

1. 「1 実体 1 ノード」の対応付けをどう決めているか。**MCP に写すなら「同じ資源
   （パス / URL / テーブル）を 1 ノードにする」に相当する**ので、その判定方法が要る。
2. どこまでが手書きのカタログで、どこからが推論か。
3. 評価の ground truth の作り方（zero-day 61 件をどう検証したか）。

---

## まだ書いていないもの

- CodeQL / Semgrep / Pysa との位置づけ（`scripts/codeql_fair.py` の比較はあるが、
  この文書には未整理）。
- MCP 公式の立場（[Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)、
  2026-03）。**「annotations は tool の挙動を忠実に記述することが保証されない」と明記**
  している点は、この研究の動機の一次資料として使える。ページは読んだ（確認済み）。
- AGENT-WIZ / AGENTIC RADAR / AgentArmor / Agentproof / Agent Audit（AgentFlow の
  検索結果に併出。未確認）。
