# MCP の「宣言」はどこにあり、どう使われているか（公式資料の調査）

調査日 2026-10-02。

**学生の問い**: 「宣言部分について、今回このプロジェクトで扱っているのはどのような立ち位置のもので、
どのように使われているのか？他の種類の宣言部分はあるのか？これらを公式から調査して」

**この文書は調査の記録で、決定ではない。** AuthGap の定義（`docs/contradiction_principles.md` など）はここから変えない。

**確かさの印**（CLAUDE.md 規則 1 に合わせる）:
- **[確認]** 本記録者が原文を取得し、引用した文字列が原文にあることを確かめたもの。版・行番号を付ける。
- **[未確認]** 検索結果の抜粋だけ、または原文を開けなかったもの。
- **[判断]** 資料に書いてあることではなく、本記録者の考え。事実として使わない。

引用は英語の原文のまま載せ、すぐ後に日本語の言い換えを付ける。

---

## 0. 読んだ資料

modelcontextprotocol.io と github.com の HTML はプロキシで遮断されていた。仕様は、仕様の repo のソース
（raw.githubusercontent.com と git）で読んだ。ブログは開けた。

| 資料 | 版 / commit | 取り方 |
|---|---|---|
| 仕様の repo `modelcontextprotocol/modelcontextprotocol` | main = `3098fe94caa1b9e0afaaa6d30e040b61d5802471`（`git ls-remote` で記録。sparse clone の HEAD も同じ） | raw と git clone |
| schema `schema/<版>/schema.ts` | 2024-11-05 / 2025-03-26 / 2025-06-18 / 2025-11-25 / 2026-07-28 / draft | raw |
| 仕様本文 `docs/specification/<版>/server/tools.mdx` ほか | 同じ 6 版。resources.mdx・basic/index.mdx・client/elicitation.mdx・changelog.mdx は必要な版だけ | raw と git |
| `docs/docs.json`（サイトの目次） | 同じ commit。33 行目に `"version": "Version 2026-07-28 (latest)"` | raw |
| SEP の原稿（main の `seps/`） | 同じ commit | git |
| SEP の原稿（PR の枝） | PR #2793 head `49f25cf`（2026-05-27）、#1913 head `f46d45e`（2026-01-29）、#1984 head `973bfe2`（2026-01-14）、#1862 head `c934643`（2026-02-03） | `git fetch origin pull/<n>/head` |
| 公式ブログ "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do"（2026-03-16） | https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ | curl（HTTP 200）。HTML から文字列を照合した |
| Python SDK `modelcontextprotocol/python-sdk` | main = `0b2fd3e`（2026-10-02、v2 系。最新タグ v2.2.0）と、v1 系の最後のタグ `v1.29.1` | git（blob は必要なものだけ取得） |
| TypeScript SDK `modelcontextprotocol/typescript-sdk` | main = `84804c2`（2026-10-02。`packages/server/package.json` の version は 2.2.0） | git |
| 本 repo の `docs/incidental_writes_practice.md` | 2026-09-29 の記録 | クライアントの使い方は、そこに付いている印のまま引く |

**注意**: 本 repo の `.venv` と `.venv312` には `mcp` パッケージが入っていなかった。SDK はインストール版ではなく、
git のソースで読んだ。

---

## 1. ToolAnnotations の位置づけ

### 1.1 どのオブジェクトの、どのメッセージに入っているか

- `ToolAnnotations` は **`Tool` オブジェクトの `annotations` 欄**に入る。
  `annotations?: ToolAnnotations;` **[確認: schema 2026-07-28 2012 行、2025-03-26 809 行]**
- `Tool` は **`tools/list` の結果（`ListToolsResult.tools`）**で、サーバからクライアントへ送られる。
  `tools: Tool[];` **[確認: schema 2026-07-28 1780 行]**
  - つまり宣言は「tool を呼ぶ前に、一覧として渡される静的な情報」。tool を呼んだ結果（`tools/call`）には付かない。
- 仕様本文の tools.mdx は、`annotations` を「tool のふるまいを表す任意の性質」と書くだけで、4 つの hint の
  中身は書いていない。中身は schema（schema.ts と、そこから作られる schema.mdx）にある。
  `- \`annotations\`: Optional properties describing tool behavior` **[確認: tools.mdx 2026-07-28 302 行]**
  （訳: 「annotations: tool のふるまいを表す、任意の性質」）

### 1.2 どの版で入ったか、版ごとに何が変わったか

| 版 | ToolAnnotations | 確かさ |
|---|---|---|
| 2024-11-05 | **無い。** `Tool` は `name` / `description` / `inputSchema` だけ（schema 687-702 行）。`readOnlyHint` の語は schema にも tools.mdx にも 0 回 | [確認] |
| 2025-03-26 | **ここで入った。** changelog: "Added comprehensive **tool annotations** for better describing tool behavior, like whether it is read-only or destructive (PR #185)"（訳:「tool のふるまい、たとえば読み取り専用か破壊的かを表すための tool annotations を加えた」） | [確認: changelog.mdx 2025-03-26 18-20 行。schema 728-779 行] |
| 2025-06-18 | 中身は同じ。`@category` の注記が増えただけ。`Tool` 側に `title`（BaseMetadata 経由）・`outputSchema`・`_meta` が増え、表示名の優先順 "Display name precedence order is: title, annotations.title, then name." が入った | [確認: schema 872-922 行・930-968 行・960 行] |
| 2025-11-25 | 文言の誤字だけ直った（"on the its environment" → "on its environment"）。`Tool` に `icons` と `execution`（`taskSupport`）が増えた | [確認: 両版の ToolAnnotations を diff。schema 1229-1241 行・1270 行] |
| 2026-07-28 | 中身は同じ。見出しの注記が `{@link Tool}` とバッククォート付きになっただけ。`Tool.execution` は消えた（tasks が拡張に移ったため。§3.1） | [確認: diff。schema 1900-1954 行] |
| draft | **2026-07-28 と同じ。** 2 つの schema.ts の差は、文書内リンクの版名（`/specification/2026-07-28/` → `/specification/draft/`）だけ | [確認: `diff` の出力は 4 か所のリンクだけ] |

**まとめ**: 4 つの hint の定義・既定値・注記は、2025-03-26 から 2026-07-28 / draft まで**意味が変わっていない**。

### 1.3 欄と既定値（2026-07-28 の原文）

見出しの注記 **[確認: schema 2026-07-28 1903-1908 行。2025-03-26 は 730-735 行でほぼ同文]**:

> NOTE: all properties in `ToolAnnotations` are **hints**.
> They are not guaranteed to provide a faithful description of
> tool behavior (including descriptive properties like `title`).
>
> Clients should never make tool use decisions based on `ToolAnnotations`
> received from untrusted servers.

訳: 「ToolAnnotations の性質はすべて **ヒント**である。tool のふるまいを正しく表すとは保証されない（`title` の
ような説明用の性質も含む）。クライアントは、信頼できないサーバから受け取った ToolAnnotations で tool の使い方を
決めてはならない。」（"should never" なので、RFC 2119 の大文字の MUST ではない。）

| 欄 | 原文 | 訳 | 既定値 | 条件 | 行（2026-07-28） |
|---|---|---|---|---|---|
| `title` | "A human-readable title for the tool." | 人が読む tool の表題 | なし | — | 1914-1916 |
| `readOnlyHint` | "If true, the tool does not modify its environment." | true なら、tool は環境を変えない | `false` | — | 1919-1923 |
| `destructiveHint` | "If true, the tool may perform destructive updates to its environment. If false, the tool performs only additive updates." | true なら破壊的な更新をしうる。false なら追加だけの更新をする | `true` | "(This property is meaningful only when \`readOnlyHint == false\`)" | 1926-1933 |
| `idempotentHint` | "If true, calling the tool repeatedly with the same arguments will have no additional effect on its environment." | true なら、同じ引数で何度呼んでも環境に追加の効果がない | `false` | 同上（readOnlyHint == false のときだけ意味を持つ） | 1936-1943 |
| `openWorldHint` | "If true, this tool may interact with an "open world" of external entities. If false, the tool's domain of interaction is closed. For example, the world of a web search tool is open, whereas that of a memory tool is not." | true なら外の世界とやり取りしうる。false なら、やり取りの範囲は閉じている。web 検索は開いていて、memory tool は閉じている | `true` | — | 1946-1953 |

すべて **[確認]**。どの欄も省略できる（`?`）。

**既定値は「最悪を仮定する」向きになっている。** 何も書かない tool は「書き込む・破壊的・冪等でない・外とやり取りする」
と読まれる。ブログもそう説明している（§2.2）。

### 1.4 誰が書き、誰が読み、仕様は読む側に何を求めるか

- **書くのはサーバの作者。** `tools/list` の結果はサーバが返すもので、SDK では tool を登録するときに作者が渡す（§2.3）。
  仕様に「作者が書く」と一文で書いた箇所は見つけていない。ここは schema の構造（サーバが返す結果に入る）からの読み。
- **読むのはクライアント / ホスト。**
- **仕様が読む側に求めること**:
  - tools.mdx の警告（2025-03-26 から全版にある）:
    "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers."
    訳: 「安全のため、クライアントは、信頼できるサーバから来たものでない限り、tool annotations を信頼できないものとして扱わ
    **なければならない**（MUST）。」
    **[確認: tools.mdx 2025-03-26 188-189 行 / 2025-06-18 193-194 行 / 2025-11-25 213-214 行 / 2026-07-28 305-306 行 / draft 305-306 行]**
  - 同じページの「人が間に入る」原則（2024-11-05 から全版）:
    "For trust & safety and security, there **SHOULD** always be a human in the loop with the ability to deny tool invocations."
    訳: 「tool の呼び出しを拒否できる人が、常に間に入っている**べき**（SHOULD）。」
    続けて "Present confirmation prompts to the user for operations, to ensure a human is in the loop"
    （訳:「操作の前に確認を出す」） **[確認: tools.mdx 2026-07-28 33-41 行。2024-11-05 は 25・31 行]**
  - Security Considerations: "Clients **SHOULD**: Prompt for user confirmation on sensitive operations"
    （訳:「危ない操作では利用者に確認を求める**べき**」） **[確認: tools.mdx 2026-07-28 795-796 行]**
- **仕様が言っていないこと**: 「`readOnlyHint: true` なら確認を省いてよい」とは、どの版の仕様本文にも schema にも
  書かれていない **[確認: 6 版の tools.mdx と schema.ts を grep。tools.mdx に `readOnlyHint` の語は無い]**。
  「信頼できるサーバ」の決め方も仕様は定めていない（定義を見つけられなかった。→ §5）。

---

## 2. 公式に、どう使われているか

### 2.1 仕様本文

§1.4 のとおり。仕様は「ヒント」「信頼できないサーバのものは信頼しない」と書く。一方で、何に使うかの具体例は
仕様本文には無い。具体例を書いているのは次のブログと SDK の文書。

### 2.2 公式ブログ "Tool Annotations as Risk Vocabulary"（2026-03-16）

著者: Ola Hungerford (Maintainer)、Sam Morrow (GitHub)、Luca Chang (AWS)。以下はすべて
**[確認: 2026-10-02 に取得した HTML に文字列があることを照合]**。

- 入った版: "Tool annotations shipped in the 2025-03-26 spec revision."（訳:「2025-03-26 の版で入った」）
- 性格: "Every property is a hint."（訳:「どの性質もヒントである」）
- 主な用途: "The first three hints mostly answer a preflight question: should the client ask for confirmation before calling this tool?"
  （訳:「最初の 3 つは主に『呼ぶ前に確認を求めるべきか』という事前の問いに答える」）
- openWorldHint は別扱い: "It's also the hint most sensitive to deployment context."
  （訳:「どこに置かれるかに最も左右されるヒントでもある」。何が「外」かは、社内網の外とも、その機械の外とも読める、と続く）
- 既定値: "The defaults are deliberately cautious"（訳:「既定値はわざと慎重にしてある」）。
  "Many servers ship without them, and clients vary in how strictly they honor the pessimistic defaults."
  （訳:「付けずに出すサーバが多く、悲観的な既定値をどこまで守るかはクライアントによってまちまち」）
- いちばん多い使い方: "A tool marked readOnlyHint: true from a trusted server might be auto-approved, while destructiveHint: true gets a confirmation step."
  ... "This is the most common use of annotations today."
  （訳:「信頼できるサーバの readOnlyHint: true の tool は自動で承認され、destructiveHint: true には確認が入る。
  これが今いちばん多い使い方」）
- ヒントごとのクライアントの動きの例（表）: `readOnlyHint: true` → "Skip the confirmation dialog"（確認を省く）、
  `destructiveHint: true` → "Show a warning before executing"、`idempotentHint: true` → "Safe to retry on failure"、
  `openWorldHint: true` → "Scrutinize output for untrusted content; flag a trust-boundary cross"
- できないこと: "An untrusted server can lie. A server can claim readOnlyHint: true and delete your files anyway."
  （訳:「信頼できないサーバは嘘をつける。readOnlyHint: true と言いながらファイルを消せる」）。
  "They aren't enforcement."（訳:「強制の仕組みではない」）
- 信頼が要るか: "readOnlyHint from an untrusted server isn't actionable"（訳:「信頼できないサーバの readOnlyHint は
  使いようがない」。確認を省くかの判断は、ヒントを信じるときだけ意味がある、と続く）
- `title` について: "title went in because it's just a display name with no trust implications."
  （訳:「title はただの表示名で、信頼の問題が無いので入った」）
- `Tool.execution` について: "taskHint was proposed as an annotation but landed as Tool.execution instead, on the grounds that execution metadata isn't really a behavioral hint."
  （訳:「taskHint は annotation として提案されたが、実行の情報はふるまいのヒントではないとして Tool.execution になった」）
- ヒントと契約: "If a proposal's value depends on the annotation being true, it's asking for a contract, and the right place for that is the authorization layer, the transport, or the runtime rather than ToolAnnotations."
  （訳:「宣言が正しいことに価値がかかるなら、それは契約の要求で、置き場所は ToolAnnotations ではなく認可・通信・実行時の層」）
- 今後: "whether any annotations should be evaluated at runtime rather than declared statically" を Interest Group の議題に挙げている。
- 作者への勧め: "set readOnlyHint: true on read-only tools, destructiveHint: false on additive operations, and openWorldHint: false on closed-domain tools."
  クライアントへの勧め: "keep your actual safety guarantees in deterministic controls."
- **数値の扱い**: ブログには "GitHub's read-only mode is the closest production analog, enabled by about 17% of users."
  とある。文字列は [確認] だが、**17% はブログの記載で、本記録者は検証していない**（出典の測り方も書かれていない）。

### 2.3 公式 SDK で作者がどう宣言するか

**Python SDK v1 系（タグ v1.29.1）**。本 repo のコーパスが主に使う書き方。
- `FastMCP.tool()` の引数に `annotations: ToolAnnotations | None = None` がある
  **[確認: `src/mcp/server/fastmcp/server.py` 450-457 行]**。書き方は `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))`。
- `ToolAnnotations` は camelCase の欄（`readOnlyHint` など）で、docstring は schema の注記と同文
  （"NOTE: all properties in ToolAnnotations are **hints**." ほか）。`model_config = ConfigDict(extra="allow")`
  **[確認: `src/mcp/types.py` 1247-1293 行]**。
  - [判断] `extra="allow"` なので、仕様に無い欄を足しても SDK は弾かない。

**Python SDK v2 系（main `0b2fd3e`）**。
- `FastMCP` は `MCPServer` に名前が変わり、欄は snake_case（`read_only_hint`）になった
  **[確認: `docs/migration.md` 20-21 行・645-662 行。`src/mcp-types/mcp_types/_types.py` 1365-1379 行]**。
- 作者向けの例 **[確認: `docs_src/tools/tutorial005.py`]**:
  `@mcp.tool(title="Search the catalog", annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False))`
- 説明 **[確認: `docs/servers/tools.md` 152-159 行]**:
  "`annotations` are behavioural **hints** for the client" / "`read_only_hint=True`: this tool doesn't change anything." /
  "The spec defines both only for non-read-only tools" /
  "A well-behaved client uses them to decide things like *"do I need to ask the user before running this?"*. They are hints, not security. Never rely on a client honouring them."
  （訳:「行儀のよいクライアントは『実行前に利用者に聞くか』の判断に使う。ヒントであって安全の仕組みではない。
  クライアントが守ると当てにしてはいけない」）
- 通信では camelCase のまま: "The JSON wire format is unchanged — traffic the SDK sends still uses camelCase via Pydantic aliases"、
  "The models accept both spellings at construction time" **[確認: `docs/migration.md` 289 行・331 行]**。
  AuthGap の `authgap/entries.py` はすでに snake_case の鍵を読む（2657-2724 行付近。D64 / U38）。

**TypeScript SDK（main `84804c2`）** **[確認: `docs/servers/tools.md` 195-223 行]**:
- `server.registerTool('clear-catalog', { title, description, annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true } }, handler)`
- "Annotations never change how the SDK runs the tool — clients use them to decide what to put in front of the end user: a host can auto-approve a read-only tool and require confirmation before a destructive one."
  （訳:「annotations は SDK の tool の動かし方を変えない。クライアントが利用者に何を見せるかの判断に使う。
  ホストは読み取り専用の tool を自動承認し、破壊的な tool の前で確認を求められる」）

**[判断] まとめ**: SDK は宣言を**そのまま一覧に載せるだけ**で、宣言とコードが合っているかは確かめない
（TypeScript SDK は「実行を変えない」と明言。Python SDK の文書に照合の記述は見つからなかった）。

### 2.4 クライアントの使い方（本 repo の既存調査から）

`docs/incidental_writes_practice.md` **§4**（依頼文では §3 とあったが、クライアントの表は §4 にある）の印のまま引く。
ここでは調べ直していない。

| クライアント | 使い方 | 同文書の印 |
|---|---|---|
| VS Code（Copilot のエージェントモード） | "tools marked with `readOnlyHint: true` in their annotations will be allowed to run without requiring user confirmation."（v1.100 のリリースノート） | [確認] |
| OpenAI Codex CLI | `readOnlyHint` が true なら承認なし、`destructiveHint == Some(true)` なら承認 | [確認: codex-rs/core/src/mcp_tool_call.rs] |
| Goose / Claude の connectors / GitHub Copilot coding agent / GitHub MCP server の read-only モード / Gemini CLI | 自動承認や表示の切り替えに使う | [agent]（本記録者は照合していない） |
| Claude Code | 公式文書に記述が無い | [未確認] |

**つまり**: 仕様は「ヒント」「信頼しない」と書くが、少なくとも 2 つのクライアントは `readOnlyHint: true` を
**確認を省く理由**に使っている（確かめたのは VS Code と Codex の 2 つ）。

---

## 3. 他の種類の「宣言」（サーバやクライアントが自分で名乗る情報）

ここでいう「宣言」は、「相手が自己申告し、受け手が検証せずに受け取る情報」のこと。
「AuthGap のようにコードと照合できるか」の列は、すべて **[判断]**（本記録者の考え）である。

### 3.1 Tool の他の欄（2026-07-28）

`export interface Tool extends BaseMetadata, Icons`（schema 1973 行）**[確認]**。

- **`name` / `title`**（BaseMetadata、954-969 行）。`title` は "Intended for UI and end-user contexts"（UI と利用者向け）。
  `Tool.title` は 2025-06-18 から。`annotations.title` との優先順は "Display name precedence order is: `title`, `annotations.title`, then `name`."
  **[確認: 2010 行]**。ふるまいの主張ではない。
- **`description`**: "This can be used by clients to improve the LLM's understanding of available tools. It can be thought of like a "hint" to the model."
  （訳:「LLM の理解を助けるのに使える。モデルへの『ヒント』と考えてよい」）**[確認: 1974-1978 行]**。
  自然文なので、ふるまいの主張を含むことがある（「ファイルを読むだけ」など）が、形は決まっていない。
- **`inputSchema`**: 引数の JSON Schema。必須（2026-07-28 から JSON Schema 2020-12 の語を何でも使える。SEP-2106）**[確認: 1981-1997 行、changelog 2026-07-28 Minor 10]**。
  宣言だが、ふるまい（環境を変えるか）の主張ではなく、受け付ける入力の形の主張。
- **`x-mcp-header`**（2026-07-28 で入った。SEP-2243）: `inputSchema` の性質の中に置き、その引数の値を
  HTTP ヘッダ `Mcp-Param-{name}` に写させる **[確認: schema 1990-1993 行、tools.mdx 334-368 行、changelog 2026-07-28 Minor 4]**。
  - クライアント側の検査がある: "Clients using the Streamable HTTP transport **MUST** reject tool definitions where any `x-mcp-header` value violates these constraints."
    （訳:「制約に反する x-mcp-header を持つ tool 定義は、クライアントが**弾かなければならない**」）**[確認: tools.mdx 362-363 行]**。
  - 作者への注意: "Server developers **SHOULD NOT** mark sensitive parameters (passwords, API keys, tokens, PII) with `x-mcp-header`"
    **[確認: tools.mdx 399-400 行]**。
  - [判断] **形の検査はクライアントがするが、検査するのは「書式」で「ふるまい」ではない。** ふるまいの主張でもない。
- **`outputSchema`**: `structuredContent` の形の JSON Schema。2025-06-18 から **[確認: 2026-07-28 1999-2005 行]**。
  [判断] 出力の形の主張。実行時の検証は仕様に書かれている（Security Considerations の `$ref` 解決の要件、tools.mdx 799-801 行）。
- **`icons`**（2025-11-25 から、SEP-973）: 表示用の画像。"Treat icon metadata and icon bytes as untrusted inputs"
  （訳:「アイコンの情報も中身も、信頼できない入力として扱う」）**[確認: basic/index.mdx 2026-07-28 477 行。schema 885-947 行]**。
- **`execution.taskSupport`**（**2025-11-25 だけ**）: `"forbidden"`（既定）/ `"optional"` / `"required"`。
  tool が task として実行できるかの宣言 **[確認: schema 2025-11-25 1229-1241 行・1270 行、tools.mdx 2025-11-25 209-210 行]**。
  **2026-07-28 の schema に `ToolExecution` は無い**（`execution` の語は schema に 0 回）**[確認]**。tasks は拡張
  `io.modelcontextprotocol/tasks` に移った（changelog 2026-07-28 Major 6、SEP-2663 "Status: Final"）**[確認]**。
  SEP-2663 は tool 単位の `execution.taskSupport` を「壊れやすい握手」の一部として挙げている（29 行）**[確認]**。
  拡張の中で tool 単位の宣言が残るかは、読んだ範囲では見つけていない（→ §5）。
- **`_meta`**（Tool には 2025-06-18 から）: 名前空間つきの任意の鍵。鍵の書式の規則だけがある（schema 34-54 行）**[確認]**。
  ブログは「1 つの組織がサーバとクライアントの両方を持つなら `_meta` でよい。ただし既製のクライアントは知らない鍵を読まない」と書く **[確認]**。

### 3.2 Resource / 中身のブロックの `Annotations`（ToolAnnotations とは別物）

- 型 `Annotations`（2026-07-28 2266-2303 行）: `audience`（`"user"` / `"assistant"` の配列）、`priority`（0〜1）、`lastModified`（ISO 8601）**[確認]**。
  - 説明: "Optional annotations for the client. The client can use annotations to inform how objects are used or displayed"
    （訳:「クライアントが、物の使い方や見せ方を決めるのに使える」）。
  - resources.mdx: "Resources, resource templates and content blocks support optional annotations that provide hints to clients about how to use or display the resource"
    **[確認: resources.mdx 2026-07-28 338 行]**。
  - 付く先: Resource、ResourceTemplate、tool の結果の中身（text / image / resource link / embedded resource など）。**Tool そのものには付かない。**
- 版の変化: 2024-11-05 では `Annotated` 型で `audience` と `priority` だけ（schema 2024-11-05 816-842 行）。
  `lastModified` は 2025-06-18 から **[確認: 各版の schema を grep]**。
- [判断] 名前は似ているが、**ふるまい（環境を変えるか）の主張ではない。** 表示と優先度のための情報。
  `lastModified` は事実の主張だが、コードではなくデータの性質。

### 3.3 Prompt の宣言

- `Prompt`（`name` / `title` / `description` / `icons` / `arguments` / `_meta`）と `PromptArgument`（`name` / `title` / `description` / `required`）
  **[確認: schema 2026-07-28 1659-1692 行]**。
- [判断] 引数の形と説明だけで、ふるまいの主張ではない。prompt はテンプレートで、それ自体は環境を変えない。

### 3.4 能力（capabilities）

- `ServerCapabilities`: `experimental` / `logging`（2026-07-28 で非推奨）/ `completions` / `prompts.listChanged` /
  `resources.subscribe`・`resources.listChanged` / `tools.listChanged` / `extensions` **[確認: schema 2026-07-28 793-883 行]**。
  - 例: `tools.listChanged` は "Whether this server supports notifications for changes to the tool list."（867 行）
- `ClientCapabilities`: `experimental` / `roots`（非推奨）/ `sampling`（非推奨。`context`・`tools`）/ `elicitation`（`form`・`url`）/ `extensions`
  **[確認: 716-786 行]**。
- 渡し方が 2026-07-28 で変わった: `initialize` の握手が無くなり、サーバの能力は `server/discover` の結果で、
  クライアントの能力は**毎回のリクエストの `_meta`**（`io.modelcontextprotocol/clientCapabilities`）で渡す
  **[確認: changelog 2026-07-28 Major 2-3、schema 655-697 行・92-98 行]**。2025-11-25 以前は `initialize` の結果
  （`InitializeResult.capabilities`）**[確認: schema 2025-03-26 184 行]**。
- 信頼の文言: サーバ側に "A server **MUST NOT** rely on capabilities the client has not declared."
  （訳:「クライアントが宣言していない能力に頼ってはならない」）**[確認: basic/index.mdx 2026-07-28 387 行]**。
  能力の宣言が「正しいか」を疑えという文言は見つけていない。
- [判断] 「その機能の通知やメソッドに応える」というプロトコル上の約束。tool のふるまいの主張ではない。
  原理上は、サーバのコードが対応するハンドラを登録しているかで照合できそうだが、AuthGap の問い（環境を変えるか）とは別。

### 3.5 実装の名乗り（serverInfo / clientInfo、`Implementation`）

- `Implementation`: `name` / `title` / `version` / `description` / `websiteUrl` / `icons` **[確認: schema 2026-07-28 976-997 行]**。
- 2026-07-28 では結果の `_meta` の `io.modelcontextprotocol/serverInfo`、リクエストの `_meta` の `io.modelcontextprotocol/clientInfo` で渡す。
- 信頼の文言（**仕様の中でいちばんはっきりした「自己申告」の文**）:
  "The value is self-reported by the server and is not verified by the protocol. It is intended for display, logging, and debugging. Clients SHOULD NOT use it to change their behavior, and SHOULD NOT rely on it for security decisions."
  （訳:「値はサーバの自己申告で、プロトコルは検証しない。表示・ログ・デバッグ用。クライアントはこれでふるまいを
  変える**べきでなく**、安全の判断に頼る**べきでない**」）**[確認: schema 2026-07-28 146-157 行。clientInfo は 79-90 行。basic/index.mdx 404-410 行]**
- tools.mdx: "The server `name` (from `serverInfo`) is not guaranteed to be unique across servers and **SHOULD NOT** be relied upon for disambiguation." **[確認: 328-329 行]**
- [判断] 身元の主張で、ふるまいの主張ではない。

### 3.6 instructions（サーバからの自然文の案内）

- 2026-07-28: `DiscoverResult.instructions` "Natural-language guidance describing the server and its features. This can be used by clients to improve an LLM's understanding of available tools (e.g., by including it in a system prompt)."
  **[確認: schema 689-696 行]**。2024-11-05 から 2025-11-25 では `InitializeResult.instructions`（2025-03-26 は 187-192 行、"It can be thought of like a "hint" to the model."）**[確認]**。
- ブログは annotations の話の中で "We made the same point about server instructions: don't rely on soft signals for things that need to be hard guarantees."
  （訳:「server instructions でも同じことを言った。固い保証が要ることに柔らかい信号を頼るな」）と書く **[確認]**。
- [判断] 自然文。ふるまいの主張を含みうるが、形が決まっていないので機械的な照合には向かない。

### 3.7 elicitation / sampling の宣言

- クライアントは `elicitation`（`form` / `url`）や `sampling` の能力を宣言する（§3.4）。
- サーバへの決まり: "Servers **MUST NOT** use form mode elicitation to request sensitive information such as passwords, API keys, access tokens, or payment credentials"
  **[確認: client/elicitation.mdx 2026-07-28 30-31 行]**。
- 2026-07-28 で sampling / roots / logging は非推奨（SEP-2577）、サーバからクライアントへのリクエストは
  multi round-trip requests（`InputRequiredResult`）に置き換わった **[確認: changelog 2026-07-28 Major 7・Deprecated 1]**。
- [判断] ふるまいの宣言ではなく、能力と使い方の決まり。「form mode で秘密を求めない」はサーバのコードで原理上は
  照合できそうだが、要求する値が「秘密か」は意味の判断になる。

### 3.8 提案中のもの（**仕様には入っていない**）

**どれも 2026-07-28 / draft の schema には入っていない。** draft の `ToolAnnotations` は 5 欄のまま **[確認: §1.2 の diff]**。
main の `seps/` にも無い（PR の枝にだけある）**[確認]**。PR が今 open か closed かは、GitHub の API が使えず **不明**。

| SEP | 名前 | 原稿の Status | 何を足すか | 確かさ |
|---|---|---|---|---|
| **#2793** | Tool Risk Metadata | "Draft"（Created 2026-05-27、Sponsor "_seeking_"） | `ToolAnnotations` に `riskLevel`（low〜critical）・`category`（read / observe / mutate / delete / destroy / utility）・`blastRadius`・`reversibility`・`sideEffects`（自由な文字列の配列）・`approvalRecommendation`・`minTrustLevel`（1〜5）を足す | [確認: PR head `49f25cf` の `seps/2793-tool-risk-metadata.md` 3-16 行・80-134 行] |
| #1913 | Trust and Sensitivity Annotations | "Draft"（Created 2025-06-11、Sponsor @dend。GitHub と OpenAI の人が著者） | `maliciousActivityHint`・`attribution`・`inputMetadata`（`destination` / `sensitivity` / `outcomes`）・`returnMetadata`（`source` / `sensitivity`）。結果にも annotation を付ける | [確認: PR head `f46d45e` 1-8 行・143-184 行・202-264 行] |
| #1984 | Comprehensive Tool Annotations for Enhanced Governance and UX | "Draft"（Created 2025-12-15、Sponsor "None (seeking sponsor)"） | `aiProcessingHint`・`slowExecutionHint`・`resourceIntensiveHint`・`sensitiveDataHint`・`privilegedAccessHint`・`reversibleHint` | [確認: PR head `973bfe2` 1-12 行] |
| #1862 | Tool Resolution | "Draft"（Created 2025-11-21） | `tools/resolve` で、**引数ごとに** annotation を問い合わせる | [確認: PR head `c934643` 1-12 行] |
| #1561 / #1560 / #1487 | unsafeOutputHint / secretHint / trustedHint | ブログの表では "Proposal" | — | [未確認]（PR の ref が無く、issue は API で開けなかった。ブログの表だけ） |

SEP-2793 の中で AuthGap に近い点（引用はすべて [確認: 同じファイル]）:
- `sideEffects`: "Side effects the tool may produce beyond its primary action, for compliance/audit reporting. Open vocabulary; common values: `"state_loss"`, `"downtime"`, `"cost"`, `"external_notification"`, `"data_exfiltration"`, `"privilege_change"`."（111-117 行）
  - 本 repo の `docs/incidental_writes_practice.md` §2 はこの引用を [agent] としていた。**今回原文で照合したので [確認] にできる**（文言は同じ）。
- 推論: "consumers without server-declared metadata can **infer** them from the tool's name, description, and input schema."（151-153 行）。
  参照実装は動詞による規則（`get|list|describe` → read など）（153-160 行）。
  - [判断] これは**名前・説明・スキーマ（＝宣言側）から推す**方法で、AuthGap のように**コードの効果から推す**ものではない。
- 安全上の注意: "A malicious server can declare low risk for a high-risk tool. Clients SHOULD NOT trust server-declared metadata blindly when the server isn't authenticated/curated."（222-224 行）

SEP-1984 の注意: "All annotations in this proposal are **hints only** and MUST NOT be relied upon for security decisions."（450 行）**[確認]**。

### 3.9 宣言の種類の一覧

「照合」の列は **[判断]**。「○」= コードの静的解析で原理上は照合の対象になりうる、「△」= 一部だけ・意味の判断が要る、「×」= ふるまいの主張でない。

| 宣言 | 定義の場所（2026-07-28） | 入った版 | 欄 | ふるまいの主張か | 信頼についての文言 | 照合 |
|---|---|---|---|---|---|---|
| **ToolAnnotations の 4 hint** | `Tool.annotations`（1912-1954 行） | 2025-03-26 | readOnly / destructive / idempotent / openWorld | **はい**（環境を変えるか・破壊か・冪等か・外とやり取りするか） | "hints"、"should never make tool use decisions ... from untrusted servers"、"MUST consider ... untrusted" | **○（AuthGap の対象）** |
| ToolAnnotations.title | 同 1914-1916 行 | 2025-03-26 | 文字列 | いいえ（表示名） | 注記に "including descriptive properties like `title`" | × |
| Tool.title / name | BaseMetadata（954-969 行） | name は最初から、title は 2025-06-18 | 文字列 | いいえ | 特に無し | × |
| Tool.description | 1974-1978 行 | 最初から | 自然文 | 含みうる（形は自由） | "like a "hint" to the model" | △ |
| Tool.inputSchema | 1981-1997 行 | 最初から | JSON Schema | 入力の形 | 実行時の検証の要件あり | △（形の主張） |
| x-mcp-header | inputSchema の中（1990 行、tools.mdx 334-368 行） | 2026-07-28 | ヘッダ名 | いいえ（通信の写し） | クライアントは書式違反を **MUST reject** | ×（書式は検査される） |
| Tool.outputSchema | 1999-2005 行 | 2025-06-18 | JSON Schema | 出力の形 | 検証の要件あり | △ |
| Tool.icons / Icon | 885-947 行 | 2025-11-25 | URI・MIME・大きさ・theme | いいえ | "Treat icon metadata and icon bytes as untrusted inputs" | × |
| Tool.execution.taskSupport | 2025-11-25 の 1229-1241 行（2026-07-28 には無い） | 2025-11-25 のみ | forbidden / optional / required | 実行の仕方（ブログは「ふるまいのヒントではない」） | 特に無し | △ |
| Tool._meta | 2014 行 | 2025-06-18 | 名前空間つきの任意の鍵 | 中身しだい | 鍵の書式だけ | 中身しだい |
| Resource / content の Annotations | 2266-2303 行 | audience・priority は 2024-11-05、lastModified は 2025-06-18 | audience / priority / lastModified | いいえ（表示・優先度） | "provide hints to clients" | × |
| Prompt / PromptArgument | 1659-1692 行 | 最初から（title は 2025-06-18） | name / title / description / required | いいえ | 特に無し | × |
| ServerCapabilities | 793-883 行（server/discover で渡す） | 最初から（中身は版ごとに増減） | tools.listChanged など | プロトコル上の約束 | 疑えという文言は見つけていない | △（別の問い） |
| ClientCapabilities | 716-786 行（毎回の `_meta`） | 最初から | elicitation / sampling など | クライアントの約束 | "server MUST NOT rely on capabilities the client has not declared" | × |
| serverInfo / clientInfo（Implementation） | 976-997 行、`_meta` 146-157 行・79-90 行 | 最初から（2026-07-28 で `_meta` へ） | name / version / description など | いいえ（身元） | "self-reported ... not verified ... SHOULD NOT rely on it for security decisions" | × |
| instructions | DiscoverResult 689-696 行 | 2024-11-05 から（InitializeResult） | 自然文 | 含みうる | "like a "hint" to the model"（2025-03-26） | △ |
| SEP-2793 Tool Risk Metadata | PR の枝だけ | 未採用（Draft） | riskLevel など 7 欄 | はい（等級・範囲・可逆性・副作用） | "SHOULD NOT trust server-declared metadata blindly" | ○ の候補（sideEffects・reversibility など） |
| SEP-1913 / 1984 / 1862 | PR の枝だけ | 未採用（Draft） | §3.8 | はい（多くは） | "hints only" など | 一部 ○ の候補 |

---

## 4. AuthGap はどこを扱い、どこを扱わないか

### 4.1 扱うもの

- **ToolAnnotations の 4 つの hint の「安全側の値」だけ**: D1 `readOnlyHint: true`、D2 `destructiveHint: false`、
  D3 `openWorldHint: false`、D4 `idempotentHint: true`。宣言ごとに分けて報告する
  （`docs/contradiction_principles.md` 141 行、§7.1〜7.4。D62）。
- D2 と D4 は「`readOnlyHint: true` が無いとき」に見る（同 §7.2・§7.4）。これは仕様の
  "(This property is meaningful only when \`readOnlyHint == false\`)" と同じ向き **[確認: schema 2026-07-28 1929・1939 行]**。
- 書き方の揺れ: v1 の `readOnlyHint=`、v2 の `read_only_hint=` の両方を読む（`authgap/entries.py`）。

### 4.2 扱わないもの

- `title`（表示名でふるまいの主張ではない。ブログも "no trust implications" と書く）。
- 危険側の値（`readOnlyHint: false`、`destructiveHint: true`、`openWorldHint: true`）だけの明示。仕様の既定値と同じなので、
  宣言としては何も約束していない。`authgap/dparse.py` の `d_kind_from` も「上界を動かさない」として D_kind に入れない（183-190 行）。
- §3 のほかの宣言（description、inputSchema、x-mcp-header、outputSchema、icons、execution、`_meta`、Resource の Annotations、
  Prompt、capabilities、serverInfo、instructions）。どれも「環境を変えるか」の主張ではないか、形が決まっていない。
- 提案中の欄（SEP-2793 の `sideEffects` など）。仕様に入っていない。

### 4.3 この位置がなぜ大事か

1. **宣言はヒントだと仕様が言っている。** "all properties in ToolAnnotations are **hints**"、"clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers"（§1.3・§1.4）。
2. **それでも、確認を省く理由に使われている。** ブログは「`readOnlyHint: true` → Skip the confirmation dialog」を例に挙げ、
   自動承認を "the most common use of annotations today" と書く（§2.2）。VS Code と Codex は `readOnlyHint: true` で確認を省く（§2.4 [確認]）。
   SDK の文書も「ホストは読み取り専用の tool を自動承認できる」と書く（§2.3）。
3. **宣言とコードが合っているかを確かめる層は、仕様にも SDK にも無い。** 仕様は「信頼できるサーバ」かどうかに判断を預ける
   （決め方は定めていない）。ブログは "An untrusted server can lie." と書き、宣言が正しいことが要るなら「契約」で、
   ToolAnnotations の外に置けと言う。
4. [判断] したがって AuthGap が見ているのは、**「ヒントのはずの宣言が、実際には許可（確認を省く）に使われている」**
   ところの隙間である。4 つの hint は、仕様の中で唯一「tool が環境に何をするか」を決まった形（真偽値）で名乗る欄なので、
   コードの効果と照合できる。他の宣言は、ふるまいの主張でないか（title・icons・capabilities・serverInfo）、
   形が自由（description・instructions）。
5. [判断] 注意点: 仕様の文言は短く、境界がはっきりしない。たとえば `readOnlyHint` は "does not modify its environment" だけで、
   「環境」にログやキャッシュが入るかは書かれていない（`docs/incidental_writes_practice.md` §2）。`openWorldHint` は
   ブログ自身が「置かれる場所に左右される」と書く。AuthGap の判定規則は仕様の文言そのものではなく、本 repo が決めた読み方
   （`docs/contradiction_principles.md`）であることを、論文では分けて書く必要がある。

---

## 5. 確かめられなかったもの（不明）

- **modelcontextprotocol.io の公開ページそのもの**は開けなかった。仕様はすべて repo のソース（mdx / ts）で読んだ。
  公開ページとソースが同じ文かは、ソースから作られる前提で読んでいて、公開ページでは照合していない。
- **SEP の PR が今 open か closed か merged か**（#2793、#1913、#1984、#1862）。GitHub の API は「この session では使えない」と
  返された。分かるのは PR の枝の原稿の Status 欄（どれも "Draft"）と、main の `seps/` に無いことだけ。
- **SEP #1487 / #1560 / #1561** の原文。PR の ref が無く（issue だと思われるが確かめていない）、ブログの表でしか見ていない。
- **Tool Annotations Interest Group の現状**（ブログでは "forming"）。
- **tasks 拡張（SEP-2663）で、tool 単位の「task として動けるか」の宣言が残るか。** 2026-07-28 の core schema から
  `Tool.execution` が消えたことは確かめたが、拡張側の定義は全部は読んでいない。
- **「信頼できるサーバ」の定義。** 仕様の tools.mdx・schema・basic/index.mdx の範囲では見つけていない。
- 仕様に「サーバの作者が annotations を書く」と一文で書いた箇所。構造からの読みで、明文は見つけていない。
- ブログの「約 17%」の出典と測り方（ブログに書かれていない）。
- `.venv` / `.venv312` に `mcp` が入っていないので、インストール版の SDK の挙動は試していない（ソースだけ読んだ）。
- 小さな食い違いの記録: SEP-2663 の原稿（17 行・949 行）は「`2026-06-30` specification」と書くが、目次と changelog の版名は
  `2026-07-28`。原稿を書いた時点の仮の版名かもしれないが、理由は確かめていない。
