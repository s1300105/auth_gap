[← 付録 G-1 MCP の公式](appendix-g-1.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-3 Microsoft と GitHub →](appendix-g-3.md)

---

# 付録 G-2 SDK（サーバを作る道具と、クライアント側のライブラリ）

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-2-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C02-01](#g-c02-sdks-01) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (MCPServer) | SDK の文書 | 作者への書き方の案内・確認を求める・信頼するなという注意 | [確認] |
| [C02-02](#g-c02-sdks-02) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (MCPServer) | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C02-03](#g-c02-sdks-03) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (mcp_types) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-04](#g-c02-sdks-04) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (FastMCP) | SDK のソースコード | 作者への書き方の案内 | [確認] |
| [C02-05](#g-c02-sdks-05) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (client) | SDK の文書 | 表示（印・名前） | [確認] |
| [C02-06](#g-c02-sdks-06) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (examples) | SDK のソースコード | 表示（印・名前）・作者への書き方の案内 | [確認] |
| [C02-07](#g-c02-sdks-07) | Prefect (FastMCP) — FastMCP (standalone, gofastmcp.com) | SDK の文書 | 確認を省く（自動で許可）・表示（印・名前）・作者への書き方の案内 | [確認] |
| [C02-08](#g-c02-sdks-08) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C02-09](#g-c02-sdks-09) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C02-10](#g-c02-sdks-10) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 確認を省く（自動で許可） | [確認] |
| [C02-11](#g-c02-sdks-11) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 信頼するなという注意・作者への書き方の案内 | [確認] |
| [C02-12](#g-c02-sdks-12) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [C02-13](#g-c02-sdks-13) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 確認を省く（自動で許可）・その他 | [確認] |
| [C02-14](#g-c02-sdks-14) | Prefect (FastMCP) — FastMCP (standalone) | SDK の文書 | 確認を省く（自動で許可）・作者への書き方の案内 | [確認] |
| [C02-15](#g-c02-sdks-15) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 | SDK の文書 | 使わない・読まない・確認を省く（自動で許可）・確認を求める | [確認] |
| [C02-16](#g-c02-sdks-16) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (examples/cli-client) | SDK の文書 | 確認を求める・信頼するなという注意 | [確認] |
| [C02-17](#g-c02-sdks-17) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v1.x | SDK の文書 | 表示（印・名前） | [確認] |
| [C02-18](#g-c02-sdks-18) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (core-internal) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-19](#g-c02-sdks-19) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Java SDK | SDK のソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [C02-20](#g-c02-sdks-20) | Spring (VMware/Broadcom) — Spring AI MCP annotations (@McpTool) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-21](#g-c02-sdks-21) | Spring (VMware/Broadcom) — Spring AI MCP annotations (tool provider) | SDK のソースコード | 宣言が無いときの扱い・そのまま渡す・見せる | [確認] |
| [C02-22](#g-c02-sdks-22) | Spring (VMware/Broadcom) — Spring AI MCP annotations | SDK の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C02-23](#g-c02-sdks-23) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Kotlin SDK | SDK のソースコード | 表示（印・名前） | [確認] |
| [C02-24](#g-c02-sdks-24) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Kotlin SDK | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-25](#g-c02-sdks-25) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET) | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C02-26](#g-c02-sdks-26) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET) | SDK の文書 | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C02-27](#g-c02-sdks-27) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-28](#g-c02-sdks-28) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-29](#g-c02-sdks-29) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (client) | SDK のソースコード | 表示（印・名前） | [確認] |
| [C02-30](#g-c02-sdks-30) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-31](#g-c02-sdks-31) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk) | SDK の文書 | 宣言が無いときの扱い・その他 | [確認] |
| [C02-32](#g-c02-sdks-32) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk) | SDK の文書 | その他・宣言が無いときの扱い | [確認] |
| [C02-33](#g-c02-sdks-33) | mark3labs (mcp-go) — mcp-go (mark3labs) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-34](#g-c02-sdks-34) | mark3labs (mcp-go) — mcp-go (mark3labs) | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C02-35](#g-c02-sdks-35) | mark3labs (mcp-go) — mcp-go (mark3labs) | SDK の文書 | 表示（印・名前） | [確認] |
| [C02-36](#g-c02-sdks-36) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Rust SDK (rmcp) | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-37](#g-c02-sdks-37) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Swift SDK | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-38](#g-c02-sdks-38) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Ruby SDK | SDK の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C02-39](#g-c02-sdks-39) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Ruby SDK | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-40](#g-c02-sdks-40) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C02-41](#g-c02-sdks-41) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-42](#g-c02-sdks-42) | Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK | SDK のソースコード | 表示（印・名前） | [確認] |
| [C02-43](#g-c02-sdks-43) | Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server | SDK の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C02-44](#g-c02-sdks-44) | Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server | SDK の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C02-45](#g-c02-sdks-45) | Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-46](#g-c02-sdks-46) | Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server | SDK のソースコード | 宣言が無いときの扱い | [確認] |
| [C02-47](#g-c02-sdks-47) | Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client) | クライアントの文書 | そのまま渡す・見せる・信頼するなという注意 | [確認] |
| [C02-48](#g-c02-sdks-48) | Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client) | クライアントの文書 | そのまま渡す・見せる | [確認] |
| [C02-49](#g-c02-sdks-49) | Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client) | クライアントの文書 | 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [C02-50](#g-c02-sdks-50) | LangChain — LangChain (langchain.mcp / langchain-mcp-adapters) | クライアントの文書 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [C02-51](#g-c02-sdks-51) | LangChain — LangChain (langchain.mcp / langchain-mcp-adapters) | クライアントの文書 | 宣言が無いときの扱い・確認を求める | [確認] |
| [C02-52](#g-c02-sdks-52) | LangChain — langchain-mcp-adapters | クライアントのソースコード | そのまま渡す・見せる | [確認] |
| [C02-53](#g-c02-sdks-53) | TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp) | クライアントの文書 | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C02-54](#g-c02-sdks-54) | TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp) | クライアントの文書 | 使わない・読まない | [確認] |
| [C02-55](#g-c02-sdks-55) | TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp) | クライアントの文書 | 信頼するなという注意・表示（印・名前）・確認を省く（自動で許可） | [確認] |
| [C02-56](#g-c02-sdks-56) | TanStack (TanStack AI) — TanStack AI (MCP server: serveMcp) | SDK の文書 | 作者への書き方の案内・確認を求める | [確認] |
| [C02-57](#g-c02-sdks-57) | Pydantic (Pydantic AI) — Pydantic AI (MCP client) | クライアントの文書 | そのまま渡す・見せる・ツールを絞る・隠す | [確認] |
| [C02-58](#g-c02-sdks-58) | Pydantic (Pydantic AI) — Pydantic AI Harness (CodeMode) | クライアントの文書 | 規則（ポリシー）の条件に使う・その他 | [確認] |
| [C02-59](#g-c02-sdks-59) | Mastra — Mastra (@mastra/mcp MCPClient) | クライアントの文書 | 規則（ポリシー）の条件に使う・確認を求める | [確認] |
| [C02-60](#g-c02-sdks-60) | Mastra — Mastra (@mastra/mcp MCPClient) | クライアントの文書 | 信頼するなという注意・確認を省く（自動で許可） | [確認] |
| [C02-61](#g-c02-sdks-61) | Mastra — Mastra (createTool, MCPServer) | SDK の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C02-62](#g-c02-sdks-62) | Basement Studio (xmcp) — xmcp (TypeScript MCP framework) | SDK の文書 | 作者への書き方の案内・使わない・読まない | [確認] |
| [C02-63](#g-c02-sdks-63) | Basement Studio (xmcp) — xmcp (TypeScript MCP framework) | SDK の文書 | 作者への書き方の案内 | [確認] |

この分冊の資料は 63 件で、うち [確認] は 63 件、[確認（調査時のみ）] は 0 件。

<a id="ag-2-1"></a>
## 資料カード

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (MCPServer)

<a id="g-c02-sdks-01"></a>
#### C02-01 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (MCPServer)

- **資料**: Tools (Python SDK docs, main/v2)（SDK の文書）
- **URL**: https://py.sdk.modelcontextprotocol.io/servers/tools/
- **書いてある見出しへ直接**: https://py.sdk.modelcontextprotocol.io/servers/tools/#names-titles-and-annotations
- **版**: main (v2) docs, 2026-10-02 取得
- **書いてある場所**: Tools > Names, titles, and annotations
- **原文**:

> A well-behaved client uses them to decide things like "do I need to ask the user before running this?". They are hints, not security. Never rely on a client honouring them.

- **日本語**: 行儀のよいクライアントは、これらを「実行の前にユーザーに聞くべきか」を決めるのに使う。これはヒントであってセキュリティではない。クライアントが守ってくれると当てにしてはいけない。
- **どう使っているか**: SDK の作者向け説明。annotations はクライアントへのヒントで、行儀のよいクライアントは「実行前にユーザーに聞くべきか」の判断に使う（と docs が説明）。ヒントであってセキュリティではなく、クライアントが守ると当てにするなと明記。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・確認を求める・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Names, titles, and annotations」（取得 2026-10-02T22:11:29Z、sha256 d469245f7568…）
- **補足**: 宣言のしかたは @mcp.tool(title=..., annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False))（docs_src/tools/tutorial005.py）。v2 では Python 側の属性名は snake_case（read_only_hint など）で、wire 上は camelCase の alias。 usage_ja から「SDK 自体は実行を変えない」を外した（このページには書かれていない）。なお検証者が src を grep した範囲（commit c54075c）では、ヒント 4 種を読む処理は型定義以外に無い。

<a id="g-c02-sdks-02"></a>
#### C02-02 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (MCPServer)

- **資料**: Tools (Python SDK docs, main/v2)（SDK の文書）
- **URL**: https://py.sdk.modelcontextprotocol.io/servers/tools/
- **書いてある見出しへ直接**: https://py.sdk.modelcontextprotocol.io/servers/tools/#names-titles-and-annotations
- **版**: main (v2) docs, 2026-10-02 取得
- **書いてある場所**: Tools > Names, titles, and annotations
- **原文**:

> The other two, destructive_hint and idempotent_hint, describe a tool that writes: may it delete something, and is calling it twice the same as calling it once? The spec defines both only for non-read-only tools, so they would say nothing on search_books.

- **日本語**: 残りの二つ destructive_hint と idempotent_hint は「書き込む」ツールを説明するもの（何かを消しうるか、二回呼んでも一回と同じか）。仕様はこの二つを読み取り専用でないツールにだけ定義しているので、search_books では何も言わない。
- **どう使っているか**: 作者への設定ガイド。read-only のツールには destructive/idempotent を付けても意味がない、と説明。
- **扱う宣言**: destructiveHint・idempotentHint・readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Names, titles, and annotations」（取得 2026-10-02T22:11:29Z、sha256 d469245f7568…）

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (mcp_types)

<a id="g-c02-sdks-03"></a>
#### C02-03 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (mcp_types)

- **資料**: mcp_types/_types.py: class ToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/python-sdk/blob/c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d/src/mcp-types/mcp_types/_types.py#L1379-L1383
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d/src/mcp-types/mcp_types/_types.py
- **版**: commit c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d
- **書いてある場所**: src/mcp-types/mcp_types/_types.py lines 1379-1383
- **原文**:

> read_only_hint: bool | None = None """ If true, the tool does not modify its environment. Default: false """

- **日本語**: read_only_hint は bool か None で、既定値は None。説明文には「true ならツールは環境を変えない。Default: false」とある。
- **どう使っているか**: SDK は未指定のヒントを None のままにし、仕様の既定値（readOnly=false, destructive=true, idempotent=false, openWorld=true）を埋めない。既定値は docstring に書かれているだけで、解釈は受け手（クライアント）に任される。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、1379-1383 行（# in the request/notification unions below, so they are never dispatched.）（取得 2026-10-02T22:11:35Z、sha256 0d07007bf505…）
- **補足**: 同じクラス（1365-1408 行）で destructive_hint / idempotent_hint / open_world_hint も `bool | None = None`。クラス docstring（1372-1373 行）に仕様の文言「Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers.」を写している（同じツールで exact 一致を確認済み, id c03b）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (FastMCP)

<a id="g-c02-sdks-04"></a>
#### C02-04 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (FastMCP)

- **資料**: mcp/server/fastmcp/server.py: FastMCP.add_tool() / FastMCP.tool() の docstring（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/python-sdk/blob/52e64ddb9f8f897bcb74de0bc9417f820af35a59/src/mcp/server/fastmcp/server.py#L434
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/52e64ddb9f8f897bcb74de0bc9417f820af35a59/src/mcp/server/fastmcp/server.py
- **版**: commit 52e64ddb9f8f897bcb74de0bc9417f820af35a59
- **書いてある場所**: src/mcp/server/fastmcp/server.py lines 434（add_tool の docstring）。同じ文が 482 行（tool の docstring）にもある（ツールの一致は 2 件）
- **原文**:

> annotations: Optional ToolAnnotations providing additional tool information

- **日本語**: annotations 引数: ツールについての追加情報を与える、任意の ToolAnnotations。
- **どう使っているか**: v1 の FastMCP では @mcp.tool(annotations=ToolAnnotations(...)) で宣言する。docstring は「追加情報」とだけ書き、ヒントの意味や使われ方は説明しない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・2 か所、434 行（取得 2026-10-02T22:11:39Z、sha256 1b1c8cd4f6e3…）
- **補足**: v1.x ブランチ（52e64dd）の README.md と公開 docs の server ページには readOnlyHint / ToolAnnotations の語が無い（checked_no_mention 参照）。v1 の型 mcp/types.py の ToolAnnotations も `readOnlyHint: bool | None = None`（1262 行, id c04b で exact 確認）で既定値を埋めない。 434 行は FastMCP.tool() ではなく add_tool() の docstring だった。doc_title と location を直した（tool() 側は 482 行）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (client)

<a id="g-c02-sdks-05"></a>
#### C02-05 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v1.x (client)

- **資料**: Writing MCP Clients > Client Display Utilities (Python SDK v1 docs)（SDK の文書）
- **URL**: https://py.sdk.modelcontextprotocol.io/v1/client/
- **書いてある見出しへ直接**: https://py.sdk.modelcontextprotocol.io/v1/client/#client-display-utilities
- **版**: v1 docs, 2026-10-02 取得
- **書いてある場所**: Writing MCP Clients > Client Display Utilities
- **原文**:

> For tools: title > annotations.title > name

- **日本語**: ツールの表示名の優先順位は title > annotations.title > name。
- **どう使っているか**: クライアント側の補助関数 get_display_name() が annotations.title を表示名の第 2 候補として読む。SDK が annotations を読む数少ない箇所（ヒント 4 種は読まない）。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Writing MCP Clients > Client Display Utilities」（取得 2026-10-02T22:11:30Z、sha256 9bda543c597a…）
- **補足**: 実装は src/mcp/shared/metadata_utils.py（v1.x 52e64dd の 38-39 行で `return obj.annotations.title` を exact 確認, id c05。main/v2 にも同じ関数がある）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (examples)

<a id="g-c02-sdks-06"></a>
#### C02-06 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Python SDK v2 (examples)

- **資料**: examples/stories/tools/README.md（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/python-sdk/blob/c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d/examples/stories/tools/README.md#L5-L7
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d/examples/stories/tools/README.md
- **版**: commit c54075ccb8793e9b0d37f0c9e2c58dfd0256c23d
- **書いてある場所**: examples/stories/tools/README.md lines 5-7
- **原文**:

> `ToolAnnotations` carries behavioural hints (`readOnlyHint`, `idempotentHint`) the host can show to users.

- **日本語**: ToolAnnotations は、ホストがユーザーに見せられる振る舞いのヒント（readOnlyHint, idempotentHint）を運ぶ。
- **どう使っているか**: 公式サンプルの説明。ヒントは「ホストがユーザーに見せるもの」と位置づけている。
- **扱う宣言**: readOnlyHint・idempotentHint ／ **使い方の分類**: 表示（印・名前）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、5-7 行（# tools）（取得 2026-10-02T22:12:59Z、sha256 cdbf9e4a387c…）

### Prefect (FastMCP) — FastMCP (standalone, gofastmcp.com)

<a id="g-c02-sdks-07"></a>
#### C02-07 Prefect (FastMCP) — FastMCP (standalone, gofastmcp.com)

- **資料**: Tools > MCP Annotations > Using Annotation Hints（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools
- **書いてある見出しへ直接**: https://gofastmcp.com/servers/tools#mcp-annotations
- **版**: gofastmcp.com 現行 docs, 2026-10-02 取得
- **書いてある場所**: Tools > MCP Annotations
- **原文**:

> MCP clients like Claude and ChatGPT use annotation hints to determine when to skip confirmation prompts and how to present tools to users. The most commonly used hint is readOnlyHint, which signals that a tool only reads data without making changes.

- **日本語**: Claude や ChatGPT などの MCP クライアントは、確認の問い合わせを省くかどうかと、ツールをユーザーにどう見せるかを決めるのに、注釈のヒントを使う。いちばんよく使われるのは readOnlyHint で、ツールがデータを読むだけで変更しないことを示す。
- **どう使っているか**: FastMCP の docs が作者向けに「Claude や ChatGPT のような MCP クライアントは annotation hints を使って、確認を省くか・ツールをどう見せるかを決める。最もよく使われるのは readOnlyHint」と説明し、読み取り専用ツールへの付与を勧める。Claude / ChatGPT の一次資料ではない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・表示（印・名前）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > MCP Annotations > Using Annotation Hints」（取得 2026-10-02T22:11:29Z、sha256 239ad8b41524…）
- **補足**: これは FastMCP 側の主張で、Claude / ChatGPT の挙動そのものはこの資料では確かめていない。同じ節の続きに「Read-only tools improve user experience by: Skipping confirmation prompts for safe operations / Allowing broader access without security concerns / Enabling more aggressive batching and caching」とある。 ツールの見出し判定は「Tools > MCP Annotations」（#mcp-annotations）だが、見た目では直後の h3「Using Annotation Hints」の最初の段落にある（同じ節の次の文は #using-annotation-hints で exact 一致を確認）。usage_ja を原文に寄せた（原文は「annotation hints で確認の省略と見せ方を決める。最もよく使われるのが readOnlyHint」）。

### Prefect (FastMCP) — FastMCP (standalone)

<a id="g-c02-sdks-08"></a>
#### C02-08 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: docs/servers/tools.mdx (MCP Annotations の表)（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools#mcp-annotations
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PrefectHQ/fastmcp/d7a3c93877fae50919bdf9e06274220f04cbc6e6/docs/servers/tools.mdx
- **版**: commit d7a3c93877fae50919bdf9e06274220f04cbc6e6
- **書いてある場所**: docs/servers/tools.mdx line 966 (## MCP Annotations の表)
- **原文**:

> | `readOnlyHint` | boolean | false | Indicates if the tool only reads without making changes |

- **日本語**: readOnlyHint は boolean、既定値 false、ツールが変更せずに読むだけかを示す。
- **どう使っているか**: FastMCP の docs は仕様と同じ既定値（readOnly=false, destructive=true, idempotent=false, openWorld=true）を表で示す。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、966 行（## MCP Annotations）（取得 2026-10-02T22:11:31Z、sha256 9268bb2cae83…）
- **補足**: fetched_url は GitHub のソース（commit d7a3c93877fae50919bdf9e06274220f04cbc6e6）。表の他の行: destructiveHint=true, idempotentHint=false, openWorldHint=true。FastMCP のコード（fastmcp_slim/）を grep した範囲では、これらの既定値をワイヤーに埋める処理は見つからなかった（resources_as_tools 変換を除く）ので、表は『受け手が解釈する仕様の既定値』の説明と読める（不明点: 実行時に確かめてはいない）。

<a id="g-c02-sdks-09"></a>
#### C02-09 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: docs/servers/tools.mdx (Using Annotation Hints)（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools#using-annotation-hints
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PrefectHQ/fastmcp/d7a3c93877fae50919bdf9e06274220f04cbc6e6/docs/servers/tools.mdx
- **版**: commit d7a3c93877fae50919bdf9e06274220f04cbc6e6
- **書いてある場所**: docs/servers/tools.mdx line 1018 (## MCP Annotations > ### Using Annotation Hints)
- **原文**:

> For tools that write to databases, send notifications, create/update/delete resources, or trigger workflows, omit `readOnlyHint` or set it to `False`. Use `destructiveHint=True` for operations that cannot be undone.

- **日本語**: DB への書き込み・通知の送信・リソースの作成/更新/削除・ワークフローの起動をするツールでは、readOnlyHint を省くか False にする。取り消せない操作には destructiveHint=True を使う。
- **どう使っているか**: 作者向けの設定方針。書き込み系は readOnlyHint を付けない、取り消せない操作は destructiveHint=True。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、1018 行（# Write operations - no readOnlyHint）（取得 2026-10-02T22:11:31Z、sha256 9268bb2cae83…）
- **補足**: ツールの md_heading は「# Write operations - no readOnlyHint」と出るが、これはコード例の中の Python のコメントで見出しではない。location（### Using Annotation Hints の 1018 行）はそのままでよい。

<a id="g-c02-sdks-10"></a>
#### C02-10 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: Tools > MCP Annotations > Using Annotation Hints（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools
- **書いてある見出しへ直接**: https://gofastmcp.com/servers/tools#using-annotation-hints
- **版**: gofastmcp.com 現行 docs, 2026-10-02 取得
- **書いてある場所**: Tools > MCP Annotations > Using Annotation Hints
- **原文**:

> ChatGPT: Skips confirmation prompts for read-only tools in Chat mode

- **日本語**: ChatGPT: Chat モードでは、読み取り専用ツールの確認の問い合わせを省く。
- **どう使っているか**: クライアント別の挙動として、ChatGPT が Chat モードで readOnlyHint のツールの確認を省くと説明（FastMCP 側の記述）。
- **条件**: ChatGPT の Chat モードのみ（FastMCP docs の記述）
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > MCP Annotations > Using Annotation Hints」（取得 2026-10-02T22:11:29Z、sha256 239ad8b41524…）
- **補足**: 同じ箇所に「Claude: Uses hints to understand tool safety profiles and make better execution decisions」ともある。ChatGPT / Claude の一次資料ではない。

<a id="g-c02-sdks-11"></a>
#### C02-11 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: Tools > MCP Annotations（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools
- **書いてある見出しへ直接**: https://gofastmcp.com/servers/tools#mcp-annotations
- **版**: gofastmcp.com 現行 docs, 2026-10-02 取得
- **書いてある場所**: Tools > MCP Annotations
- **原文**:

> Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and safety controls, but won't enforce security boundaries on their own.

- **日本語**: 注釈はよりよいユーザー体験に役立つが、助言としてのヒントとして扱うべき。クライアントが適切な UI や安全の制御を出すのを助けるが、それだけでセキュリティ境界を強制するものではない。
- **どう使っているか**: ヒントはセキュリティ境界ではないと注意し、実際の振る舞いを正確に表すよう作者に求める。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > MCP Annotations」（取得 2026-10-02T22:11:29Z、sha256 239ad8b41524…）
- **補足**: 直後の文: 「Always focus on making your annotations accurately represent what your tool actually does.」

<a id="g-c02-sdks-12"></a>
#### C02-12 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: docs/servers/tools.mdx (Decorator Arguments: title)（SDK の文書）
- **URL**: https://gofastmcp.com/servers/tools
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PrefectHQ/fastmcp/d7a3c93877fae50919bdf9e06274220f04cbc6e6/docs/servers/tools.mdx
- **版**: commit d7a3c93877fae50919bdf9e06274220f04cbc6e6
- **書いてある場所**: lines 77 (### Decorator Arguments)
- **原文**:

> If omitted, FastMCP falls back to `annotations.title` when present, then to a title derived from the tool's name (e.g. `find_products` becomes "Find Products") — some MCP clients drop tools that have no title at all.

- **日本語**: （title を）省くと、FastMCP はあれば annotations.title を使い、無ければツール名から作った題（find_products → "Find Products"）を使う。題の無いツールを捨てる MCP クライアントもある。
- **どう使っているか**: SDK が title を自動で補う。annotations.title を表示名の候補として読む。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、77 行（### Decorator Arguments）（取得 2026-10-02T22:11:31Z、sha256 9268bb2cae83…）

<a id="g-c02-sdks-13"></a>
#### C02-13 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: Resources as Tools > Basic Usage（SDK の文書）
- **URL**: https://gofastmcp.com/servers/transforms/resources-as-tools
- **書いてある見出しへ直接**: https://gofastmcp.com/servers/transforms/resources-as-tools#basic-usage
- **版**: gofastmcp.com 現行 docs, 2026-10-02 取得
- **書いてある場所**: Resources as Tools > Basic Usage
- **原文**:

> Both generated tools are annotated with readOnlyHint=True, since they only read data. Clients that respect tool annotations (like Cursor) can use this to auto-confirm these tool calls without prompting the user.

- **日本語**: 生成される二つのツールには readOnlyHint=True が付く（データを読むだけなので）。ツール注釈を尊重するクライアント（Cursor など）は、これを使ってユーザーに聞かずに自動で確認できる。
- **どう使っているか**: SDK の変換機能（ResourcesAsTools）が生成する list_resources / read_resource に readOnlyHint=True を自動で付ける。「注釈を尊重するクライアント（Cursor など）はこれを使って確認なしで自動承認できる（can）」は FastMCP 側の説明で、Cursor の一次資料ではない。
- **条件**: ResourcesAsTools 変換を server に適用したとき。自動承認は「注釈を尊重するクライアント」の場合とだけ書かれている（can。どのクライアントが既定でそうするかは不明）
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Resources as Tools > Basic Usage」（取得 2026-10-02T22:13:23Z、sha256 f7c6aa14cca6…）
- **補足**: コードでは fastmcp_slim/fastmcp/server/transforms/resources_as_tools.py 35 行 `_DEFAULT_ANNOTATIONS = ToolAnnotations(read_only_hint=True)`（commit d7a3c93877fae50919bdf9e06274220f04cbc6e6, id c09b で exact 確認）を list_resources / read_resource の両ツールに渡す。 原文は「can use this to auto-confirm」で可能性の記述。usage_ja の「Cursor が自動確認に使う」を「使える（can）」に弱め、conditions を足した。

<a id="g-c02-sdks-14"></a>
#### C02-14 Prefect (FastMCP) — FastMCP (standalone)

- **資料**: docs/integrations/chatgpt.mdx (Skip Confirmations)（SDK の文書）
- **URL**: https://gofastmcp.com/integrations/chatgpt
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PrefectHQ/fastmcp/d7a3c93877fae50919bdf9e06274220f04cbc6e6/docs/integrations/chatgpt.mdx
- **版**: commit d7a3c93877fae50919bdf9e06274220f04cbc6e6
- **書いてある場所**: lines 95 (### Skip Confirmations)
- **原文**:

> Use `annotations=ToolAnnotations(readOnlyHint=True)` to skip confirmation prompts for read-only tools:

- **日本語**: 読み取り専用ツールの確認の問い合わせを省くには annotations=ToolAnnotations(readOnlyHint=True) を使う。
- **どう使っているか**: FastMCP の ChatGPT 連携ガイドが、確認を省くために readOnlyHint=True を付けるよう勧める（ChatGPT の挙動についての FastMCP 側の記述で、OpenAI の一次資料ではない）。
- **条件**: FastMCP の ChatGPT 連携ガイドの説明。ChatGPT の Developer Mode を有効にし、各チャットでコネクタを有効にした場合の話（同じページの手順）。注釈なしのツールは「may ask for confirmation」
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、95 行（### Skip Confirmations）（取得 2026-10-02T22:11:30Z、sha256 2232e0a3d32b…）
- **補足**: 同じコード例の 105 行に `@mcp.tool()  # No annotation - ChatGPT may ask for confirmation`（id c10b で exact 確認）。注釈が無いときは確認が出うる、という説明。 前後の文脈は ChatGPT の Developer Mode での接続手順。conditions を足し、第三者の記述であることを usage_ja に明記した。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2

<a id="g-c02-sdks-15"></a>
#### C02-15 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2

- **資料**: Tools > Annotate the tool (TS SDK v2 docs)（SDK の文書）
- **URL**: https://ts.sdk.modelcontextprotocol.io/v2/servers/tools
- **書いてある見出しへ直接**: https://ts.sdk.modelcontextprotocol.io/v2/servers/tools#annotate-the-tool
- **版**: v2 docs, 2026-10-02 取得
- **書いてある場所**: Tools > Annotate the tool
- **原文**:

> Annotations never change how the SDK runs the tool — clients use them to decide what to put in front of the end user: a host can auto-approve a read-only tool and require confirmation before a destructive one.

- **日本語**: 注釈は SDK がツールを実行するしかたを決して変えない。クライアントは、エンドユーザーに何を見せるかを決めるのに使う。ホストは読み取り専用ツールを自動承認し、破壊的ツールの前に確認を求めることができる。
- **どう使っているか**: SDK（サーバ側）は注釈を実行に使わない。使い道としてホストの自動承認 / 確認を例に挙げる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない・確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Annotate the tool」（取得 2026-10-02T22:13:02Z、sha256 01d84d00fab1…）
- **補足**: 宣言は server.registerTool(name, { title, description, annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true } }, handler)。Recap に「title and annotations describe the tool to clients and never change execution.」（GitHub docs/servers/tools.md 223 行, commit 84804c22e45a662675a198f853b7f00063838a8d, id c14b で exact 確認）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (examples/cli-client)

<a id="g-c02-sdks-16"></a>
#### C02-16 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (examples/cli-client)

- **資料**: examples/cli-client/README.md (Design notes)（SDK の文書）
- **URL**: https://github.com/modelcontextprotocol/typescript-sdk/blob/84804c22e45a662675a198f853b7f00063838a8d/examples/cli-client/README.md#L155-L156
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/84804c22e45a662675a198f853b7f00063838a8d/examples/cli-client/README.md
- **版**: commit 84804c22e45a662675a198f853b7f00063838a8d
- **書いてある場所**: lines 155-156 (## Design notes)
- **原文**:

> An unattended host must add a consent policy — confirm destructive or side-effecting calls, or keep a per-server allowlist — and should treat tool annotations (`readOnlyHint`, `destructiveHint`) as UX hints, never as a security boundary.

- **日本語**: 無人で動くホストは同意の方針を足さなければならない（破壊的・副作用のある呼び出しは確認する、またはサーバごとの許可リストを持つ）。そしてツール注釈（readOnlyHint, destructiveHint）は UX のヒントとして扱い、決してセキュリティ境界にしない。
- **どう使っているか**: 公式サンプルクライアントは実行を門番しない（対話で人が見ているため）。無人ホストには確認や許可リストが要り、注釈は UX ヒントに留めよと注意。
- **条件**: サンプル CLI クライアント自体は gate しない（対話ユーザーが見ている前提）
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、155 行（## Design notes）（取得 2026-10-02T22:11:37Z、sha256 d92a32c7afd1…）
- **補足**: url に行番号のアンカーを足した（ツールの行番号と一致）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v1.x

<a id="g-c02-sdks-17"></a>
#### C02-17 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v1.x

- **資料**: docs/server.md > Display names and metadata (v1.x)（SDK の文書）
- **URL**: https://github.com/modelcontextprotocol/typescript-sdk/blob/727075b5bbeb77fbea22041b36b72a73042160fa/docs/server.md#L499
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/727075b5bbeb77fbea22041b36b72a73042160fa/docs/server.md
- **版**: commit 727075b5bbeb77fbea22041b36b72a73042160fa (v1.x branch)
- **書いてある場所**: lines 499 (### Display names and metadata)
- **原文**:

> Tools, resources and prompts support a `title` field for human‑readable names. Older APIs can also attach `annotations.title`. To compute the correct display name on the client, use:

- **日本語**: ツール・リソース・プロンプトは人が読む名前の title を持てる。古い API では annotations.title も付けられる。クライアントで正しい表示名を計算するには、次を使う（getDisplayName）。
- **どう使っているか**: v1 docs で注釈に触れるのは annotations.title の表示名だけ。ヒント 4 種の説明は無い（checked_no_mention 参照）。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、499 行（### Display names and metadata）（取得 2026-10-02T22:11:44Z、sha256 df75daf48870…）
- **補足**: getDisplayName の実装（v1.x src/shared/metadataUtils.ts 13-26 行、目視）は title → annotations.title → name の順。 url に行番号のアンカーを足した（ツールの行番号と一致）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (core-internal)

<a id="g-c02-sdks-18"></a>
#### C02-18 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP TypeScript SDK v2 (core-internal)

- **資料**: packages/core-internal/src/wire/rev2026-07-28/buildSchemas.ts（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/typescript-sdk/blob/84804c22e45a662675a198f853b7f00063838a8d/packages/core-internal/src/wire/rev2026-07-28/buildSchemas.ts#L470-L478
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/84804c22e45a662675a198f853b7f00063838a8d/packages/core-internal/src/wire/rev2026-07-28/buildSchemas.ts
- **版**: commit 84804c22e45a662675a198f853b7f00063838a8d
- **書いてある場所**: packages/core-internal/src/wire/rev2026-07-28/buildSchemas.ts lines 470-478
- **原文**:

> const ToolAnnotationsSchema = z.object({ title: z.string().optional(), readOnlyHint: z.boolean().optional(), destructiveHint: z.boolean().optional(), idempotentHint: z.boolean().optional(), openWorldHint: z.boolean().optional() });

- **日本語**: ToolAnnotationsSchema は title と 4 つのヒントをすべて任意（optional）で定義する。
- **どう使っているか**: TS SDK はヒントを任意項目として受け渡すだけで、既定値を埋めない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、470-476 行（取得 2026-10-02T22:12:05Z、sha256 6cedebbb13ce…）
- **補足**: v1.x の src/types.ts（1329 行付近）でも readOnlyHint: z.boolean().optional() で同じ（grep で確認、ツール照合はしていない）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Java SDK

<a id="g-c02-sdks-19"></a>
#### C02-19 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Java SDK

- **資料**: mcp-core/.../spec/McpSchema.java: record ToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/java-sdk/blob/1cf7903935ac6a99ea8920b4ce85a43e4f1d0689/mcp-core/src/main/java/io/modelcontextprotocol/spec/McpSchema.java#L2772-L2780
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/java-sdk/1cf7903935ac6a99ea8920b4ce85a43e4f1d0689/mcp-core/src/main/java/io/modelcontextprotocol/spec/McpSchema.java
- **版**: commit 1cf7903935ac6a99ea8920b4ce85a43e4f1d0689
- **書いてある場所**: mcp-core/src/main/java/io/modelcontextprotocol/spec/McpSchema.java lines 2772-2780
- **原文**:

> @JsonInclude(JsonInclude.Include.NON_ABSENT) @JsonIgnoreProperties(ignoreUnknown = true) public record ToolAnnotations( // @formatter:off @JsonProperty("title")  String title, @JsonProperty("readOnlyHint")   Boolean readOnlyHint, @JsonProperty("destructiveHint") Boolean destructiveHint, @JsonProperty("idempotentHint") Boolean idempotentHint, @JsonProperty("openWorldHint") Boolean openWorldHint, @JsonProperty("returnDirect") Boolean returnDirect) { // @formatter:on

- **日本語**: ToolAnnotations のレコードは @JsonInclude(NON_ABSENT)（null の項目は出さない）付きで、title と 4 つのヒントを Boolean（null を許す型）で持ち、加えて仕様に無い returnDirect という項目を持つ。
- **どう使っているか**: Java SDK はヒントを null 可の Boolean で持ち（未指定は null、@JsonInclude NON_ABSENT で省かれる）、既定値を埋めない。仕様外の拡張項目 returnDirect がある。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、2772-2780 行（取得 2026-10-02T22:11:37Z、sha256 f8e95f0b3b55…）
- **補足**: 2774 行から始まる record の直前の javadoc に仕様の「Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers.」を写している（grep で確認）。公開 docs の server ページには注釈の説明が無い（checked_no_mention 参照）。returnDirect の意味はこの資料には書かれていない（不明）。 元の引用（2779-2780 行、openWorldHint と returnDirect の 2 行）は exact で一致したが、usage_ja の「@JsonInclude NON_ABSENT で省かれる」「Boolean で持つ」を支えていなかったので、引用を 2772-2780 行（NON_ABSENT の注釈からレコードの頭まで）に広げて照合し直した（exact）。

### Spring (VMware/Broadcom) — Spring AI MCP annotations (@McpTool)

<a id="g-c02-sdks-20"></a>
#### C02-20 Spring (VMware/Broadcom) — Spring AI MCP annotations (@McpTool)

- **資料**: mcp/mcp-annotations/.../annotation/McpTool.java（SDK のソースコード）
- **URL**: https://github.com/spring-projects/spring-ai/blob/46d05c2fdbab52f6ef04207abe19b12687a47453/mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/McpTool.java#L52
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/spring-projects/spring-ai/46d05c2fdbab52f6ef04207abe19b12687a47453/mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/McpTool.java
- **版**: commit 46d05c2fdbab52f6ef04207abe19b12687a47453
- **書いてある場所**: mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/McpTool.java lines 52
- **原文**:

> McpAnnotations annotations() default @McpAnnotations;

- **日本語**: @McpTool の annotations 要素の既定値は @McpAnnotations（空の注釈 = すべて既定値）。
- **どう使っているか**: Java の注釈要素は null にできないので、@McpTool を付けたツールには常に McpAnnotations があり、その既定値（readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=true）がそのまま使われる。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、52 行（取得 2026-10-02T22:11:45Z、sha256 3c9e7d9875a3…）
- **補足**: 既定値は同ファイル 96 行 `boolean readOnlyHint() default false;`（id c16b で exact 確認）、104 行 destructiveHint default true、112 行 idempotentHint default false、119 行 openWorldHint default true。同じ定義は spring-ai-community/mcp-annotations（commit 422bd28）にもある。

### Spring (VMware/Broadcom) — Spring AI MCP annotations (tool provider)

<a id="g-c02-sdks-21"></a>
#### C02-21 Spring (VMware/Broadcom) — Spring AI MCP annotations (tool provider)

- **資料**: mcp/mcp-annotations/.../provider/tool/SyncMcpToolProvider.java（SDK のソースコード）
- **URL**: https://github.com/spring-projects/spring-ai/blob/46d05c2fdbab52f6ef04207abe19b12687a47453/mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/provider/tool/SyncMcpToolProvider.java#L93-L98
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/spring-projects/spring-ai/46d05c2fdbab52f6ef04207abe19b12687a47453/mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/provider/tool/SyncMcpToolProvider.java
- **版**: commit 46d05c2fdbab52f6ef04207abe19b12687a47453
- **書いてある場所**: mcp/mcp-annotations/src/main/java/org/springframework/ai/mcp/annotation/provider/tool/SyncMcpToolProvider.java lines 93-98
- **原文**:

> if (toolJavaAnnotation.annotations() != null) { var toolAnnotations = toolJavaAnnotation.annotations(); toolBuilder.annotations(McpSchema.ToolAnnotations.builder() .title(toolAnnotations.title()) .readOnlyHint(toolAnnotations.readOnlyHint()) .destructiveHint(toolAnnotations.destructiveHint())

- **日本語**: @McpTool の annotations() が null でなければ、title と各ヒントの値をそのまま McpSchema.ToolAnnotations に組み立てて Tool に付ける。
- **どう使っているか**: Spring AI のサーバは、作者が何も書かなくても 4 つのヒントを既定値で明示して tools/list に載せる（推論: 注釈要素は null にならないため条件は常に真）。作者が宣言したかどうかはワイヤー上で区別できない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、93-98 行（取得 2026-10-02T22:11:39Z、sha256 1e5c7ad4ea68…）
- **補足**: Async / SyncStateless / AsyncStateless の各 provider も同じ形（grep で確認）。『常に明示される』は Java の注釈の言語仕様からの推論で、実行して tools/list を見たわけではない。対照: Quarkus は既定値を無視し、宣言したときだけ載せる（C02_sdks の Quarkus の項）。

### Spring (VMware/Broadcom) — Spring AI MCP annotations

<a id="g-c02-sdks-22"></a>
#### C02-22 Spring (VMware/Broadcom) — Spring AI MCP annotations

- **資料**: MCP Server Annotations > @McpTool > Tool Annotations (Hints)（SDK の文書）
- **URL**: https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html
- **書いてある見出しへ直接**: https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_tool_annotations_hints
- **版**: Spring AI reference (current), 2026-10-02 取得
- **書いてある場所**: MCP Server Annotations > Server Annotations > @McpTool > Tool Annotations (Hints)
- **原文**:

> readOnlyHint false If true , the tool does not modify its environment. destructiveHint true If true , the tool may perform destructive updates (meaningful only when readOnlyHint == false ).

- **日本語**: readOnlyHint の既定値は false（true ならツールは環境を変えない）。destructiveHint の既定値は true（true ならツールは破壊的な更新をしうる。readOnlyHint == false のときだけ意味を持つ）。
- **どう使っているか**: Spring AI の docs は @McpTool.McpAnnotations の既定値を表で示す（表のセルを空白でつないだ形で照合）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「MCP Server Annotations > Server Annotations > @McpTool > Tool Annotations (Hints)」（取得 2026-10-02T22:12:51Z、sha256 bf246cd128e9…）
- **補足**: loose 一致（表のセルの区切りと空白の違い）。表には idempotentHint=false, openWorldHint=true, title="" も並ぶ。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Kotlin SDK

<a id="g-c02-sdks-23"></a>
#### C02-23 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Kotlin SDK

- **資料**: kotlin-sdk-core/.../types/tools.kt: ToolAnnotations (KDoc)（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/kotlin-sdk/blob/382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd/kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt#L147-L148
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/kotlin-sdk/382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd/kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt
- **版**: commit 382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd
- **書いてある場所**: kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt lines 147-148
- **原文**:

> @property title A human-readable title for the tool. * Takes precedence over [Tool.title] and [Tool.name] for display purposes.

- **日本語**: title はツールの人が読む題。表示では Tool.title と Tool.name より優先される。
- **どう使っているか**: Kotlin SDK の KDoc は annotations.title を Tool.title より優先すると書く。Python（get_display_name）・TS v1（getDisplayName）・C#（McpClientTool.Title）・mcp-go docs・TanStack の順序（Tool.title > annotations.title > name。mcp-go docs はこれを仕様の順序だとする）と逆で、食い違い。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、147-148 行（取得 2026-10-02T22:12:04Z、sha256 6d18c7150e21…）
- **補足**: KDoc の記述だけで、Kotlin SDK に表示名を計算する関数があるかは確かめていない（不明）。同じ KDoc に仕様の Default（readOnly false, destructive true, idempotent false, openWorld true）と「Clients should NEVER make tool use decisions based on ToolAnnotations received from untrusted servers.」がある。

<a id="g-c02-sdks-24"></a>
#### C02-24 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Kotlin SDK

- **資料**: kotlin-sdk-core/.../types/tools.kt: data class ToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/kotlin-sdk/blob/382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd/kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt#L167-L173
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/kotlin-sdk/382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd/kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt
- **版**: commit 382e27b0ee5bfd3dad89c9fbc34fff1984e16ecd
- **書いてある場所**: kotlin-sdk-core/src/commonMain/kotlin/io/modelcontextprotocol/kotlin/sdk/types/tools.kt lines 167-173
- **原文**:

> public data class ToolAnnotations( val title: String? = null, val readOnlyHint: Boolean? = null, val destructiveHint: Boolean? = null, val idempotentHint: Boolean? = null, val openWorldHint: Boolean? = null, )

- **日本語**: ToolAnnotations の各項目は null 可で、既定値は null。
- **どう使っているか**: Kotlin SDK は未指定のヒントを null で持ち、仕様の既定値を埋めない。McpJson は explicitNulls = false なので null の項目はワイヤーに出ない（送られない）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、167-173 行（取得 2026-10-02T22:12:04Z、sha256 6d18c7150e21…）
- **補足**: README には ToolAnnotations / readOnlyHint の語が無い（checked_no_mention 参照）。 usage_ja の「null のまま送り」は不正確だった（null を値として送るように読める）。kotlin-sdk-core/.../types/jsonUtils.kt 22-25 行「encodeDefaults = true isLenient = true classDiscriminatorMode = ClassDiscriminatorMode.NONE explicitNulls = false」を同じ commit の raw で exact 照合した。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET)

<a id="g-c02-sdks-25"></a>
#### C02-25 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET)

- **資料**: Class McpServerToolAttribute > Properties > ReadOnly > Remarks (API reference v1)（SDK の文書）
- **URL**: https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Server.McpServerToolAttribute.html
- **書いてある見出しへ直接**: https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Server.McpServerToolAttribute.html#ModelContextProtocol_Server_McpServerToolAttribute_ReadOnly_remarks
- **版**: csharp.sdk.modelcontextprotocol.io v1 API docs, 2026-10-02 取得
- **書いてある場所**: Class McpServerToolAttribute > Properties > ReadOnly > Remarks
- **原文**:

> Read-only tools do not have side effects beyond computational resource usage. They don't create, update, or delete data in any system.

- **日本語**: 読み取り専用ツールには、計算資源の使用を超える副作用が無い。どのシステムでもデータを作成・更新・削除しない。
- **どう使っているか**: C# SDK は [McpServerTool(ReadOnly = true, Destructive = ..., Idempotent = ..., OpenWorld = ...)] の属性で宣言し、ReadOnly の意味を『どのシステムのデータも作成・更新・削除しない』と強めに説明する。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Class McpServerToolAttribute > Properties > ReadOnly > Remarks」（取得 2026-10-02T22:11:23Z、sha256 f9a1cb2ee2d4…）
- **補足**: 概念 docs の tools ページ（v1 公開版と main の docs/concepts/tools/tools.md）には ReadOnly / Destructive / readOnlyHint の語が無い（checked_no_mention 参照）。説明は API リファレンスにだけある。

<a id="g-c02-sdks-26"></a>
#### C02-26 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET)

- **資料**: Class McpServerToolAttribute > Properties > Destructive (API reference v1)（SDK の文書）
- **URL**: https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Server.McpServerToolAttribute.html
- **書いてある見出しへ直接**: https://csharp.sdk.modelcontextprotocol.io/v1/api/ModelContextProtocol.Server.McpServerToolAttribute.html#ModelContextProtocol_Server_McpServerToolAttribute_Destructive
- **版**: csharp.sdk.modelcontextprotocol.io v1 API docs, 2026-10-02 取得
- **書いてある場所**: Class McpServerToolAttribute > Properties > Destructive > Property Value
- **原文**:

> if the tool might perform destructive updates to its environment. false if the tool performs only additive updates. The default is true.

- **日本語**: （true なら）ツールは環境を破壊的に更新しうる。false なら追加の更新だけをする。既定値は true。
- **どう使っているか**: 属性プロパティの getter の既定値を仕様に合わせて説明（Destructive=true, Idempotent=false, OpenWorld=true, ReadOnly=false）。ただしこれは読み出したときの値で、作者が設定しなかったヒントはワイヤーに載らない（C02_sdks-27 / 28）。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Class McpServerToolAttribute > Properties > Destructive > Property Value」（取得 2026-10-02T22:11:23Z、sha256 f9a1cb2ee2d4…）
- **補足**: 「既定値は true」だけだと C# が destructiveHint:true を送ると誤読されうるので、usage_ja に 27/28 の結論を足した。根拠: AIFunctionMcpServerTool.cs 134-138 行「if (options.Title is not null || options.Idempotent is not null || options.Destructive is not null || options.OpenWorld is not null || options.ReadOnly is not null)」を commit c40ee04 の raw で exact 照合（API docs は v1 版、ソースは main の HEAD なので版はずれうる）。

<a id="g-c02-sdks-27"></a>
#### C02-27 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET)

- **資料**: src/ModelContextProtocol.Core/Server/McpServerToolAttribute.cs（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/csharp-sdk/blob/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Server/McpServerToolAttribute.cs#L249-L253
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/csharp-sdk/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Server/McpServerToolAttribute.cs
- **版**: commit c40ee044fd415c70da5176c749cb5ef02f2b59f6
- **書いてある場所**: src/ModelContextProtocol.Core/Server/McpServerToolAttribute.cs lines 249-253
- **原文**:

> public bool ReadOnly { get => _readOnly ?? ReadOnlyDefault; set => _readOnly = value; }

- **日本語**: ReadOnly プロパティは、設定されていなければ既定値（false）を返し、設定されれば内部の null 可の欄に値を入れる。
- **どう使っているか**: 読み出すと仕様の既定値が見えるが、内部では『未設定』を null で区別している。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、249-253 行（取得 2026-10-02T22:12:04Z、sha256 0bc6101e8fdd…）
- **補足**: 既定値の定数は 150-153 行（DestructiveDefault = true, IdempotentDefault = false, OpenWorldDefault = true, ReadOnlyDefault = false; id c18b で exact 確認）。155 行のコメント「Nullable backing fields so we can distinguish」。

<a id="g-c02-sdks-28"></a>
#### C02-28 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (ModelContextProtocol for .NET)

- **資料**: src/ModelContextProtocol.Core/Server/AIFunctionMcpServerTool.cs: DeriveOptions（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/csharp-sdk/blob/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Server/AIFunctionMcpServerTool.cs#L185-L188
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/csharp-sdk/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Server/AIFunctionMcpServerTool.cs
- **版**: commit c40ee044fd415c70da5176c749cb5ef02f2b59f6
- **書いてある場所**: src/ModelContextProtocol.Core/Server/AIFunctionMcpServerTool.cs lines 185-188
- **原文**:

> if (toolAttr._readOnly is bool readOnly) { newOptions.ReadOnly ??= readOnly; }

- **日本語**: 属性で ReadOnly が実際に設定されているとき（内部の欄が bool のとき）だけ、その値をツールのオプションに写す。
- **どう使っているか**: 作者が明示したヒントだけが tools/list に載り、未設定のものは null（省略）になる。getter の既定値はワイヤーに出ない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、185-188 行（取得 2026-10-02T22:11:36Z、sha256 4c620f48a1ab…）
- **補足**: 同じファイル 133-150 行（ツール照合はしていない、目視）で、Title / Idempotent / Destructive / OpenWorld / ReadOnly のどれかが null でないときだけ tool.Annotations を作り、各ヒントは options の値（null 可）をそのまま入れている。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (client)

<a id="g-c02-sdks-29"></a>
#### C02-29 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP C# SDK (client)

- **資料**: src/ModelContextProtocol.Core/Client/McpClientTool.cs（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/csharp-sdk/blob/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Client/McpClientTool.cs#L107
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/csharp-sdk/c40ee044fd415c70da5176c749cb5ef02f2b59f6/src/ModelContextProtocol.Core/Client/McpClientTool.cs
- **版**: commit c40ee044fd415c70da5176c749cb5ef02f2b59f6
- **書いてある場所**: src/ModelContextProtocol.Core/Client/McpClientTool.cs lines 107
- **原文**:

> public string? Title => ProtocolTool.Title ?? ProtocolTool.Annotations?.Title;

- **日本語**: クライアント側の McpClientTool.Title は、ツールの Title が無ければ Annotations.Title を返す。
- **どう使っているか**: C# のクライアント側でも annotations.title を表示名の代わりに読む。ヒント 4 種をクライアント側で使う処理は grep した範囲では見つからなかった。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、107 行（取得 2026-10-02T22:11:43Z、sha256 f631aa8aa399…）

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk)

<a id="g-c02-sdks-30"></a>
#### C02-30 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk)

- **資料**: mcp/protocol.go: type ToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/go-sdk/blob/53effc04ea258b9ee618886702e03abc4306a160/mcp/protocol.go#L2085-L2088
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/go-sdk/53effc04ea258b9ee618886702e03abc4306a160/mcp/protocol.go
- **版**: commit 53effc04ea258b9ee618886702e03abc4306a160
- **書いてある場所**: mcp/protocol.go lines 2085-2088
- **原文**:

> // If true, the tool does not modify its environment. // // Default: false ReadOnlyHint bool `json:"readOnlyHint"`

- **日本語**: true ならツールは環境を変えない。既定値 false。ReadOnlyHint は（ポインタでない）bool で、JSON に readOnlyHint として出る。
- **どう使っているか**: Go SDK では ReadOnlyHint と IdempotentHint が素の bool なので、ToolAnnotations を付けたツールでは、作者が書かなくても false が明示的に送られる（未設定と false を区別できない）。DestructiveHint と OpenWorldHint は *bool + omitempty で省略可。ToolAnnotations を付けないツールは annotations ごと送られない。
- **条件**: Tool.Annotations（*ToolAnnotations, omitempty）を設定したときだけ。MCPGODEBUG=hintomitempty=1 で、false を省く以前の動きに戻る（1.7.0 で追加、1.9.0 で削除予定）
- **扱う宣言**: readOnlyHint・idempotentHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、2085-2088 行（取得 2026-10-02T22:11:36Z、sha256 d8c3b380adda…）
- **補足**: 2078 行 `IdempotentHint bool `json:"idempotentHint"``、2071 行と 2084 行は *bool + omitempty（目視）。 「注釈を付けると」の条件を conditions に明記した。根拠: protocol.go 2002 行「Annotations *ToolAnnotations `json:"annotations,omitempty"`」と 2095-2096 行（MCPGODEBUG=hintomitempty=1 の説明）を同じ commit の raw で exact 照合。mcp/ の他のファイルに Annotations を自動で付ける処理は grep で見つからなかった。

<a id="g-c02-sdks-31"></a>
#### C02-31 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk)

- **資料**: Backwards compatibility and MCPGODEBUG > MCPGODEBUG history > 1.7.0（SDK の文書）
- **URL**: https://go.sdk.modelcontextprotocol.io/mcpgodebug/
- **書いてある見出しへ直接**: https://go.sdk.modelcontextprotocol.io/mcpgodebug/#170
- **版**: go.sdk.modelcontextprotocol.io, 2026-10-02 取得
- **書いてある場所**: Backwards compatibility and MCPGODEBUG¶ > MCPGODEBUG history¶ > 1.7.0¶
- **原文**:

> The default behavior was changed to always serialize these fields, since their Go types are bare bool (not *bool) and omitting false made it indistinguishable from unset.

- **日本語**: 既定の動きを変えて、これらの項目（ReadOnlyHint, IdempotentHint）を常に出すようにした。Go の型が素の bool（*bool でない）なので、false を省くと未設定と区別できなかったため。
- **どう使っているか**: v1.7.0 から、ToolAnnotations を付けたツールでは readOnlyHint:false / idempotentHint:false を常に送る（作者が書かなくても）。MCPGODEBUG=hintomitempty=1 で以前の（false を省く）動きに戻せる（この設定は 1.9.0 で削除予定）。
- **条件**: Tool.Annotations を設定したツールに限る（C02_sdks-30）
- **扱う宣言**: readOnlyHint・idempotentHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Backwards compatibility and MCPGODEBUG¶ > MCPGODEBUG history¶ > 1.7.0¶」（取得 2026-10-02T22:11:29Z、sha256 63620dd49463…）
- **補足**: 「常に送る」は ToolAnnotations を付けたツールの話（Tool.Annotations は *ToolAnnotations + omitempty）。usage_ja と conditions に限定を足した。

<a id="g-c02-sdks-32"></a>
#### C02-32 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Go SDK (modelcontextprotocol/go-sdk)

- **資料**: Rough edges: API decisions to reconsider for v2（SDK の文書）
- **URL**: https://go.sdk.modelcontextprotocol.io/rough_edges/
- **書いてある見出しへ直接**: https://go.sdk.modelcontextprotocol.io/rough_edges/#rough-edges-api-decisions-to-reconsider-for-v2
- **版**: go.sdk.modelcontextprotocol.io, 2026-10-02 取得
- **書いてある場所**: Rough edges: API decisions to reconsider for v2¶
- **原文**:

> Different MCP clients have different requirements, and some of them require all fields to be explicitly set to either true or false.

- **日本語**: MCP クライアントによって要求が違い、すべての項目を true か false で明示することを求めるクライアントもある。
- **どう使っているか**: SDK の保守者が、ToolAnnotations は全項目 *bool にすべきだったと反省し、全ヒントの明示を要求するクライアントがあると記録している。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Rough edges: API decisions to reconsider for v2¶」（取得 2026-10-02T22:11:35Z、sha256 ff57e9f4217c…）
- **補足**: 直前の文: 「ToolAnnotations (mcp/protocol.go) should have all fields typed as *bool for full control to define what is being sent over the wire.」どのクライアントかは書かれていない（不明）。Go SDK の server docs の Tools 節には注釈の説明が無い（checked_no_mention 参照）。

### mark3labs (mcp-go) — mcp-go (mark3labs)

<a id="g-c02-sdks-33"></a>
#### C02-33 mark3labs (mcp-go) — mcp-go (mark3labs)

- **資料**: mcp/tools.go: NewTool（SDK のソースコード）
- **URL**: https://github.com/mark3labs/mcp-go/blob/d74db509452d46e0521fe43b9e3dfa77350e8b0a/mcp/tools.go#L1019-L1025
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mark3labs/mcp-go/d74db509452d46e0521fe43b9e3dfa77350e8b0a/mcp/tools.go
- **版**: commit d74db509452d46e0521fe43b9e3dfa77350e8b0a
- **書いてある場所**: mcp/tools.go lines 1019-1025
- **原文**:

> Annotations: ToolAnnotation{ Title: "", ReadOnlyHint: ToBoolPtr(false), DestructiveHint: ToBoolPtr(true), IdempotentHint: ToBoolPtr(false), OpenWorldHint: ToBoolPtr(true), },

- **日本語**: NewTool は、作者が何も指定しなくても Annotations に ReadOnlyHint=false, DestructiveHint=true, IdempotentHint=false, OpenWorldHint=true を入れる。
- **どう使っているか**: mcp-go の NewTool で作るツールは、仕様の既定値が 4 つとも明示されて送られる。作者が宣言したかは区別できない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、1019-1025 行（取得 2026-10-02T22:12:03Z、sha256 c1f6de078e48…）
- **補足**: 作者は mcp.WithReadOnlyHintAnnotation(true) / WithDestructiveHintAnnotation / WithIdempotentHintAnnotation / WithOpenWorldHintAnnotation / WithTitleAnnotation で上書きする（1183 行 `func WithReadOnlyHintAnnotation(value bool) ToolOption {` を id c20b で exact 確認）。Tool.MarshalJSON は annotations を常に出す（727 行、目視）。NewToolWithRawSchema は既定値を入れない（1042-1050 行、目視）ので空の annotations になる。

<a id="g-c02-sdks-34"></a>
#### C02-34 mark3labs (mcp-go) — mcp-go (mark3labs)

- **資料**: Implementing Tools > Tool Annotations (mcp-go.dev)（SDK の文書）
- **URL**: https://mcp-go.dev/servers/tools
- **版**: mcp-go.dev, 2026-10-02 取得
- **書いてある場所**: Implementing Tools > Tool Annotations
- **原文**:

> Provide hints to help LLMs use your tools effectively:

- **日本語**: LLM がツールをうまく使えるようにヒントを与えよう。
- **どう使っているか**: docs の『Tool Annotations』節は「LLM がツールをうまく使う助けになるヒントを与えよ」という一文だけで、続くコード例にはヒントを付ける関数が出てこない（説明の欠落）。クライアントの承認・表示への言及も無い。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Implementing Tools > Tool Annotations」（取得 2026-10-02T22:11:33Z、sha256 fffeba43f0e0…）
- **補足**: 続くコード例（GitHub www/docs/pages/servers/tools.mdx 1088-1112 行, commit d74db509452d46e0521fe43b9e3dfa77350e8b0a, 目視）は mcp.NewTool に WithDescription / WithString / WithNumber / WithArray だけを渡し、With*HintAnnotation を使っていない。このページには WithReadOnlyHintAnnotation / readOnlyHint の語が無い（checked_no_mention）。 原文はヒントを「LLM のため」と位置づけている点を usage_ja に足した。

<a id="g-c02-sdks-35"></a>
#### C02-35 mark3labs (mcp-go) — mcp-go (mark3labs)

- **資料**: Implementing Tools > Tool Definition > Display Title (mcp-go.dev)（SDK の文書）
- **URL**: https://mcp-go.dev/servers/tools
- **版**: mcp-go.dev, 2026-10-02 取得
- **書いてある場所**: Implementing Tools > Tool Definition > Display Title
- **原文**:

> Per the MCP spec, clients should resolve the display label in this order: Title (the top-level field set by WithToolTitle) Annotations.Title (legacy hint set by WithTitleAnnotation, see Tool Annotations) Name

- **日本語**: MCP 仕様に従い、クライアントは表示名を次の順で決めるべき: Title（WithToolTitle で付けるトップレベルの項目）→ Annotations.Title（WithTitleAnnotation で付ける古いヒント）→ Name。
- **どう使っているか**: mcp-go の docs は『MCP 仕様に従い』クライアントは Title > Annotations.Title > Name の順で表示名を決めるべきだと書く。annotations.title は古いヒントの扱い。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Implementing Tools > Tool Definition > Display Title」（取得 2026-10-02T22:11:33Z、sha256 fffeba43f0e0…）
- **補足**: 元の引用（リストの 2 項目め）は exact で一致したが、usage_ja の「Title > Annotations.Title > Name の順」を引用だけでは示せなかったので、前の文と 3 項目を含む形に広げて照合し直した（exact、見出しは同じ）。仕様側の順序は schema/2025-06-18/schema.ts 960 行「Display name precedence order is: title, annotations.title, then name.」で exact 確認（modelcontextprotocol commit 3098fe9）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Rust SDK (rmcp)

<a id="g-c02-sdks-36"></a>
#### C02-36 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Rust SDK (rmcp)

- **資料**: crates/rmcp/src/model/tool.rs: impl ToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/rust-sdk/blob/ae2f9c9b45a2c98d24ee345406e79f507c9f9282/crates/rmcp/src/model/tool.rs#L150-L153
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/rust-sdk/ae2f9c9b45a2c98d24ee345406e79f507c9f9282/crates/rmcp/src/model/tool.rs
- **版**: commit ae2f9c9b45a2c98d24ee345406e79f507c9f9282
- **書いてある場所**: crates/rmcp/src/model/tool.rs lines 150-153
- **原文**:

> /// If not set, defaults to true. pub fn is_destructive(&self) -> bool { self.destructive_hint.unwrap_or(true) }

- **日本語**: 設定されていなければ true とみなす。is_destructive() は destructive_hint が無いとき true を返す。
- **どう使っているか**: rmcp は ToolAnnotations に補助関数 is_destructive()（未設定→true）と is_idempotent()（未設定→false）を用意し、仕様の既定値を関数の中に書いている。readOnly / openWorld 用の同様の関数は無い。SDK 自身の中ではこれらの関数を呼ぶ箇所は無い（grep）ので、既定値を適用するかは使う側しだい。
- **扱う宣言**: destructiveHint・idempotentHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、150-153 行（取得 2026-10-02T22:11:35Z、sha256 5251faf90659…）
- **補足**: フィールドは Option<bool> で skip_serializing_if = Option::is_none（未設定は送らない）。宣言は #[tool(annotations(title = ..., read_only_hint = true))] マクロか ToolAnnotations::new().read_only(true) などのビルダー。マクロの説明（crates/rmcp-macros/src/lib.rs 26 行）は annotations を『Additional tool information. Defaults to None.』とする（id c21b で exact 確認）。README には ToolAnnotations / read_only_hint の語が無い（checked_no_mention）。 「受け手用の補助関数で既定値を適用する」は言い過ぎだった。検証者が repo（commit ae2f9c9）を grep したところ is_destructive() / is_idempotent() の呼び出しは無い。is_idempotent の定義（155-158 行）も raw で exact 照合した。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Swift SDK

<a id="g-c02-sdks-37"></a>
#### C02-37 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Swift SDK

- **資料**: Sources/MCP/Server/Tools.swift: Tool.Annotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/swift-sdk/blob/a0ae212ebf6eab5f754c3129608bc5557637e605/Sources/MCP/Server/Tools.swift#L61-L64
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/swift-sdk/a0ae212ebf6eab5f754c3129608bc5557637e605/Sources/MCP/Server/Tools.swift
- **版**: commit a0ae212ebf6eab5f754c3129608bc5557637e605
- **書いてある場所**: Sources/MCP/Server/Tools.swift lines 61-64
- **原文**:

> /// If true, the tool does not modify its environment. /// /// When unspecified, the implicit default is `false`. public var readOnlyHint: Bool?

- **日本語**: true ならツールは環境を変えない。指定されないときの暗黙の既定値は false。readOnlyHint は Bool?（nil 可）。
- **どう使っているか**: Swift SDK は未指定を nil のまま持ち、既定値は説明にだけ書く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、61-64 行（取得 2026-10-02T22:11:36Z、sha256 79c4fc037144…）
- **補足**: annotations が空（全項目 nil）なら Tool のエンコードで annotations 自体を出さない（298-300 行 `if !annotations.isEmpty { ... }`、id c22b で exact 確認）。README には annotations の語が無い（checked_no_mention）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Ruby SDK

<a id="g-c02-sdks-38"></a>
#### C02-38 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Ruby SDK

- **資料**: Tools > Tool Annotations (ruby.sdk.modelcontextprotocol.io)（SDK の文書）
- **URL**: https://ruby.sdk.modelcontextprotocol.io/server/tools/
- **書いてある見出しへ直接**: https://ruby.sdk.modelcontextprotocol.io/server/tools/#tool-annotations
- **版**: Ruby SDK docs, 2026-10-02 取得
- **書いてある場所**: Tools > Tool Annotations
- **原文**:

> destructive_hint: Indicates if the tool performs destructive operations. Defaults to true

- **日本語**: destructive_hint: ツールが破壊的な操作をするかを示す。既定値は true。
- **どう使っているか**: Ruby SDK は annotations クラスメソッドか define(annotations: {...}) で宣言し、既定値を docs に書く。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Tool Annotations」（取得 2026-10-02T22:11:38Z、sha256 306c388f4412…）
- **補足**: 同じ節: idempotent_hint 既定 false、open_world_hint 既定 true、read_only_hint 既定 false。『This Tool Annotations feature is supported starting from protocol_version: 2025-03-26』。

<a id="g-c02-sdks-39"></a>
#### C02-39 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP Ruby SDK

- **資料**: lib/mcp/tool/annotations.rb: MCP::Tool::Annotations（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/ruby-sdk/blob/73d6da3f21b65455f4d9527e511e5061ffecb779/lib/mcp/tool/annotations.rb#L8
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/ruby-sdk/73d6da3f21b65455f4d9527e511e5061ffecb779/lib/mcp/tool/annotations.rb
- **版**: commit 73d6da3f21b65455f4d9527e511e5061ffecb779
- **書いてある場所**: lib/mcp/tool/annotations.rb lines 8
- **原文**:

> def initialize(destructive_hint: true, idempotent_hint: false, open_world_hint: true, read_only_hint: false, title: nil)

- **日本語**: Annotations の初期化の既定値は destructive_hint: true, idempotent_hint: false, open_world_hint: true, read_only_hint: false, title: nil。
- **どう使っているか**: 作者が annotations を一部でも宣言すると、残りのヒントは既定値で埋まり、to_h（.compact は nil だけ除く）で 4 つとも明示されて送られる。annotations を宣言しなければ送られない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、8 行（# frozen_string_literal: true）（取得 2026-10-02T22:11:36Z、sha256 4e2a53d22196…）
- **補足**: lib/mcp/tool.rb 32 行 `annotations: annotations_value&.to_h`、45 行で既定は nil（目視）。

### Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK

<a id="g-c02-sdks-40"></a>
#### C02-40 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK

- **資料**: Tools > Parameters (php.sdk.modelcontextprotocol.io)（SDK の文書）
- **URL**: https://php.sdk.modelcontextprotocol.io/servers/tools/
- **書いてある見出しへ直接**: https://php.sdk.modelcontextprotocol.io/servers/tools/#parameters
- **版**: PHP SDK docs, 2026-10-02 取得
- **書いてある場所**: Tools > Parameters
- **原文**:

> annotations (optional): ToolAnnotations object for additional metadata.

- **日本語**: annotations（任意）: 追加のメタデータのための ToolAnnotations オブジェクト。
- **どう使っているか**: PHP SDK の docs は #[McpTool(annotations: new ToolAnnotations(...))] を受け付けると書くだけで、ヒントの意味や使われ方を説明しない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Parameters」（取得 2026-10-02T22:11:34Z、sha256 2653e7bb90f9…）
- **補足**: 同じページに readOnlyHint / destructiveHint の語は無い（checked_no_mention）。

<a id="g-c02-sdks-41"></a>
#### C02-41 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK

- **資料**: src/Schema/ToolAnnotations.php（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/php-sdk/blob/3175614b63b10f8c6a9bdd2e946177dfb14cdfe3/src/Schema/ToolAnnotations.php#L81-L83
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/php-sdk/3175614b63b10f8c6a9bdd2e946177dfb14cdfe3/src/Schema/ToolAnnotations.php
- **版**: commit 3175614b63b10f8c6a9bdd2e946177dfb14cdfe3
- **書いてある場所**: src/Schema/ToolAnnotations.php lines 81-83
- **原文**:

> if (null !== $this->readOnlyHint) { $data['readOnlyHint'] = $this->readOnlyHint; }

- **日本語**: readOnlyHint が null でないときだけ、JSON に readOnlyHint を入れる。
- **どう使っているか**: PHP SDK は未指定のヒントを送らない（既定値を埋めない）。fromArray では bool でない値を例外にする。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、81-83 行（取得 2026-10-02T22:11:36Z、sha256 8de06f7f34ba…）

<a id="g-c02-sdks-42"></a>
#### C02-42 Model Context Protocol（GitHub の modelcontextprotocol org の公式 SDK） — MCP PHP SDK

- **資料**: src/Schema/ToolAnnotations.php (constructor の @param)（SDK のソースコード）
- **URL**: https://github.com/modelcontextprotocol/php-sdk/blob/3175614b63b10f8c6a9bdd2e946177dfb14cdfe3/src/Schema/ToolAnnotations.php#L33
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/php-sdk/3175614b63b10f8c6a9bdd2e946177dfb14cdfe3/src/Schema/ToolAnnotations.php
- **版**: commit 3175614b63b10f8c6a9bdd2e946177dfb14cdfe3
- **書いてある場所**: src/Schema/ToolAnnotations.php lines 33
- **原文**:

> a human-readable title for the tool — deprecated for display in favor of `Mcp\Schema\Tool::$title` per MCP spec revision 2025-06-18; retained for backward compatibility

- **日本語**: （annotations の title は）ツールの人が読む題。MCP 仕様 2025-06-18 に従い表示用としては Tool::$title に置き換えられて非推奨。後方互換のために残す。
- **どう使っているか**: PHP SDK の docblock は annotations.title を「表示用には Tool::$title に置き換えられて非推奨（仕様 2025-06-18 による）、後方互換のために残す」と書く。なお仕様 2025-06-18 の schema は「deprecated」とは書かず、表示名の順序を title → annotations.title → name と定めている（非推奨というのは PHP SDK 側の言い方）。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、33 行（取得 2026-10-02T22:11:36Z、sha256 8de06f7f34ba…）
- **補足**: 仕様が非推奨と明言しているように読めたので補った。schema/2025-06-18/schema.ts 960 行「Display name precedence order is: title, annotations.title, then name.」（modelcontextprotocol commit 3098fe9）を exact 照合。同じ schema に deprecat の語は無い（grep）。

### Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server

<a id="g-c02-sdks-43"></a>
#### C02-43 Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server

- **資料**: MCP Annotations > Tool Annotations > readOnlyHint（SDK の文書）
- **URL**: https://docs.quarkiverse.io/quarkus-mcp-server/dev/reference-annotations.html
- **書いてある見出しへ直接**: https://docs.quarkiverse.io/quarkus-mcp-server/dev/reference-annotations.html#_readonlyhint
- **版**: docs.quarkiverse.io dev, 2026-10-02 取得
- **書いてある場所**: MCP Annotations > Tool Annotations > readOnlyHint
- **原文**:

> The default value is false, indicating that the tool may perform write operations.

- **日本語**: 既定値は false で、ツールが書き込みをしうることを表す。
- **どう使っているか**: @Tool(annotations = @Annotations(readOnlyHint = true)) で宣言。読む・検索するツールで true にするよう説明。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Annotations > Tool Annotations > readOnlyHint」（取得 2026-10-02T22:11:26Z、sha256 35315c15f5b6…）
- **補足**: 直前の文: 「Set this annotation to true when the tool does not modify its environment (e.g., read operations, queries, searches).」

<a id="g-c02-sdks-44"></a>
#### C02-44 Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server

- **資料**: MCP Annotations > Tool Annotations > destructiveHint（SDK の文書）
- **URL**: https://docs.quarkiverse.io/quarkus-mcp-server/dev/reference-annotations.html
- **書いてある見出しへ直接**: https://docs.quarkiverse.io/quarkus-mcp-server/dev/reference-annotations.html#_destructivehint
- **版**: docs.quarkiverse.io dev, 2026-10-02 取得
- **書いてある場所**: MCP Annotations > Tool Annotations > destructiveHint
- **原文**:

> Set this annotation to false when the tool performs only additive updates (e.g., creating new files, appending to logs). The default value is true.

- **日本語**: ツールが追加の更新だけをする（新しいファイルを作る、ログに追記するなど）ときは false にする。既定値は true。
- **どう使っているか**: 追加だけの書き込みは destructiveHint=false、と具体例つきで作者に説明。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Annotations > Tool Annotations > destructiveHint」（取得 2026-10-02T22:11:26Z、sha256 35315c15f5b6…）

<a id="g-c02-sdks-45"></a>
#### C02-45 Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server

- **資料**: core/runtime/.../server/Tool.java: annotations()（SDK のソースコード）
- **URL**: https://github.com/quarkiverse/quarkus-mcp-server/blob/a2addbe2f6bf96a73aafd91d8f2af883537be73f/core/runtime/src/main/java/io/quarkiverse/mcp/server/Tool.java#L82-L83
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/quarkiverse/quarkus-mcp-server/a2addbe2f6bf96a73aafd91d8f2af883537be73f/core/runtime/src/main/java/io/quarkiverse/mcp/server/Tool.java
- **版**: commit a2addbe2f6bf96a73aafd91d8f2af883537be73f
- **書いてある場所**: core/runtime/src/main/java/io/quarkiverse/mcp/server/Tool.java lines 82-83
- **原文**:

> Note that the default value of this annotation member is ignored. In other words, the annotations have to be declared * explicitly in order to be included in Tool metadata.

- **日本語**: この注釈要素の既定値は無視される。つまり、ツールのメタデータに入れるには annotations を明示的に宣言しなければならない。
- **どう使っているか**: Quarkus は宣言していないツールに注釈を付けない（Spring AI と逆）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、82-83 行（取得 2026-10-02T22:11:37Z、sha256 65f5e2061145…）

<a id="g-c02-sdks-46"></a>
#### C02-46 Quarkiverse (Quarkus MCP Server) — Quarkus MCP Server

- **資料**: core/deployment/.../McpServerProcessor.java（SDK のソースコード）
- **URL**: https://github.com/quarkiverse/quarkus-mcp-server/blob/a2addbe2f6bf96a73aafd91d8f2af883537be73f/core/deployment/src/main/java/io/quarkiverse/mcp/server/deployment/McpServerProcessor.java#L446-L447
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/quarkiverse/quarkus-mcp-server/a2addbe2f6bf96a73aafd91d8f2af883537be73f/core/deployment/src/main/java/io/quarkiverse/mcp/server/deployment/McpServerProcessor.java
- **版**: commit a2addbe2f6bf96a73aafd91d8f2af883537be73f
- **書いてある場所**: core/deployment/src/main/java/io/quarkiverse/mcp/server/deployment/McpServerProcessor.java lines 446-447
- **原文**:

> readOnlyHintValue != null ? readOnlyHintValue.asBoolean() : false, destructiveHintValue != null ? destructiveHintValue.asBoolean() : true,

- **日本語**: readOnlyHint が書かれていなければ false、destructiveHint が書かれていなければ true を入れる。
- **どう使っているか**: annotations を宣言したときは、書かなかったヒントを仕様の既定値（readOnly false, destructive true, idempotent false, openWorld true）で埋めて送る。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、446-447 行（取得 2026-10-02T22:11:36Z、sha256 a63cfe471822…）
- **補足**: 448-449 行で idempotentHint→false、openWorldHint→true も同様（目視）。

### Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client)

<a id="g-c02-sdks-47"></a>
#### C02-47 Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client)

- **資料**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval（クライアントの文書）
- **URL**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
- **書いてある見出しへ直接**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools#tool-annotations-and-approval
- **版**: ai-sdk.dev current docs, 2026-10-02 取得
- **書いてある場所**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval
- **原文**:

> Annotations are untrusted, server-provided hints. The MCP client does not turn them into an approval policy automatically.

- **日本語**: 注釈は信用できない、サーバが出すヒント。MCP クライアントは自動では承認の方針に変えない。
- **どう使っているか**: クライアント SDK は注釈を露出するだけで、承認の方針はアプリが決める。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval」（取得 2026-10-02T22:11:20Z、sha256 e2ee820329a0…）
- **補足**: 直後の文: 「Applications should combine them with deterministic controls such as tool allowlists, scoped credentials, and their own toolApproval policy.」

<a id="g-c02-sdks-48"></a>
#### C02-48 Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client)

- **資料**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval（クライアントの文書）
- **URL**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
- **書いてある見出しへ直接**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools#tool-annotations-and-approval
- **版**: ai-sdk.dev current docs, 2026-10-02 取得
- **書いてある場所**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval
- **原文**:

> The MCP client exposes these annotations on each tool's metadata.annotations and on the resulting tool call's toolMetadata.annotations.

- **日本語**: MCP クライアントは注釈を、各ツールの metadata.annotations と、ツール呼び出しの toolMetadata.annotations に出す。
- **どう使っているか**: 注釈をアプリ側で読める場所を定める。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval」（取得 2026-10-02T22:11:20Z、sha256 e2ee820329a0…）

<a id="g-c02-sdks-49"></a>
#### C02-49 Vercel (AI SDK) — AI SDK (@ai-sdk/mcp, MCP client)

- **資料**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval（クライアントの文書）
- **URL**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
- **書いてある見出しへ直接**: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools#tool-annotations-and-approval
- **版**: ai-sdk.dev current docs, 2026-10-02 取得
- **書いてある場所**: Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval
- **原文**:

> The following conservative policy allows tools to run automatically only when the server explicitly marks them as read-only. Tools with readOnlyHint: false or no readOnlyHint require user approval:

- **日本語**: 次の保守的な方針は、サーバが明示的に読み取り専用と示したツールだけを自動で走らせる。readOnlyHint が false か、readOnlyHint が無いツールはユーザーの承認を要する。
- **どう使っているか**: docs の例: toolApproval で readOnlyHint === true なら承認不要、それ以外（無い場合も）は承認。destructiveHint === true は承認理由の文言に使う。
- **条件**: アプリが toolApproval にこの方針を書いた場合（SDK の既定ではない）
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > Using MCP Tools > Tool Annotations and Approval」（取得 2026-10-02T22:11:20Z、sha256 e2ee820329a0…）
- **補足**: 例の後に『The read-only tool executes immediately. The destructive and unannotated tools prompt for approval』とある（examples/mcp の tool-annotations サンプル）。

### LangChain — LangChain (langchain.mcp / langchain-mcp-adapters)

<a id="g-c02-sdks-50"></a>
#### C02-50 LangChain — LangChain (langchain.mcp / langchain-mcp-adapters)

- **資料**: Tools > Human-in-the-loop (docs.langchain.com, Markdown 版)（クライアントの文書）
- **URL**: https://docs.langchain.com/oss/python/langchain/mcp/tools
- **照らし合わせた中身の URL**: https://docs.langchain.com/oss/python/langchain/mcp/tools.md
- **版**: docs.langchain.com current, 2026-10-02 取得
- **書いてある場所**: lines 196 (## Human-in-the-loop)
- **原文**:

> Reading annotations lets you gate a tool based on what the server declares about it, rather than hardcoding tool names.

- **日本語**: 注釈を読めば、ツール名を決め打ちせずに、サーバがツールについて宣言した内容で門番できる。
- **どう使っているか**: docs の例: destructive_hint を読み、HumanInTheLoopMiddleware の when 述語で承認を要求する。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、196 行（## Human-in-the-loop）（取得 2026-10-02T22:11:25Z、sha256 f0e164c7a9c4…）
- **補足**: HTML 版（https://docs.langchain.com/oss/python/langchain/mcp/tools）でも続きの文「The MCP annotation classifies the tool and LangChain's human-in-the-loop middleware enforces the approval policy.」を含めて exact 一致（id l32、ツールの見出し判定は Tools > Tool metadata）。

<a id="g-c02-sdks-51"></a>
#### C02-51 LangChain — LangChain (langchain.mcp / langchain-mcp-adapters)

- **資料**: Tools > Tool metadata (docs.langchain.com, Markdown 版のコード例)（クライアントの文書）
- **URL**: https://docs.langchain.com/oss/python/langchain/mcp/tools#tool-metadata
- **照らし合わせた中身の URL**: https://docs.langchain.com/oss/python/langchain/mcp/tools.md
- **版**: docs.langchain.com current, 2026-10-02 取得
- **書いてある場所**: lines 186-191（## Tool metadata の節のコード例。同じ is_destructive は ## Human-in-the-loop の例にもある）
- **原文**:

> Chain `.get` with defaults so a tool missing any nested field returns # False rather than raising. annotations = ( (tool.metadata or {}).get("mcp", {}).get("tool", {}).get("annotations", {}) ) return annotations.get("destructive_hint", False)

- **日本語**: 入れ子の項目が欠けたツールでは例外ではなく False を返すよう、.get を既定値つきでつなぐ。…annotations.get("destructive_hint", False) を返す。
- **どう使っているか**: docs の例は destructive_hint が無いツールを『破壊的でない』（False）として扱い、承認なしで通す。仕様の既定値（destructiveHint 未指定 = true）と逆向きで、誤って通す（fail-open）方向。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、186-191 行（# }）（取得 2026-10-02T22:11:25Z、sha256 f0e164c7a9c4…）
- **補足**: 仕様との食い違いはこの調査の解釈（仕様は destructiveHint の既定値を true とする）。LangChain の docs 自身はこの点に触れていない。

### LangChain — langchain-mcp-adapters

<a id="g-c02-sdks-52"></a>
#### C02-52 LangChain — langchain-mcp-adapters

- **資料**: langchain_mcp_adapters/tools.py: convert_mcp_tool_to_langchain_tool（クライアントのソースコード）
- **URL**: https://github.com/langchain-ai/langchain-mcp-adapters/blob/52a4535f3eb4b98f386836e4d9b8c4cadf99afca/langchain_mcp_adapters/tools.py#L511
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/52a4535f3eb4b98f386836e4d9b8c4cadf99afca/langchain_mcp_adapters/tools.py
- **版**: commit 52a4535f3eb4b98f386836e4d9b8c4cadf99afca
- **書いてある場所**: langchain_mcp_adapters/tools.py lines 511
- **原文**:

> base = tool.annotations.model_dump() if tool.annotations is not None else {}

- **日本語**: MCP ツールに annotations があれば model_dump() した辞書を、LangChain ツールの metadata の土台にする。
- **どう使っているか**: アダプタは注釈を LangChain ツールの metadata に平らに写すだけで、自分では使わない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、511 行（# Conditional type based on langgraph availability）（取得 2026-10-02T22:12:58Z、sha256 8111a65e5deb…）
- **補足**: 同じファイル 570 行の docstring: 「Tool annotations are returned as part of the tool metadata object.」（目視）。docs.langchain.com の新しい langchain.mcp では metadata['mcp']['tool']['annotations'] に入る（d32c の例）。

### TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp)

<a id="g-c02-sdks-53"></a>
#### C02-53 TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp)

- **資料**: MCP Server Tools > Limit and Gate Tools（クライアントの文書）
- **URL**: https://tanstack.com/ai/latest/docs/tools/mcp
- **書いてある見出しへ直接**: https://tanstack.com/ai/latest/docs/tools/mcp#limit-and-gate-tools
- **版**: tanstack.com/ai latest, 2026-10-02 取得
- **書いてある場所**: MCP Server Tools > Limit and Gate Tools
- **原文**:

> A tool with no annotations does not pass this filter.

- **日本語**: annotations の無いツールはこのフィルタを通らない。
- **どう使っているか**: toolFilter: (tool) => tool.annotations?.readOnlyHint === true の例。注釈の無いツールはモデルに見せない。
- **条件**: アプリが toolFilter にこの述語を書いた場合
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Server Tools > Limit and Gate Tools」（取得 2026-10-02T22:11:40Z、sha256 fd07474a5c7e…）
- **補足**: 続きの文: 「On a server that you do not trust, filter by name. You control the names, and the server controls the hints」。needsApproval: (tool) => !(serverIsTrusted && tool.annotations?.readOnlyHint === true) の例もある（GitHub docs/tools/mcp.md 467-469 行、目視）。

<a id="g-c02-sdks-54"></a>
#### C02-54 TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp)

- **資料**: docs/tools/mcp.md > Limit and Gate Tools（クライアントの文書）
- **URL**: https://tanstack.com/ai/latest/docs/tools/mcp#limit-and-gate-tools
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/TanStack/ai/d31e4ebb91d736476fef5ad2bd8b65234632d439/docs/tools/mcp.md
- **版**: commit d31e4ebb91d736476fef5ad2bd8b65234632d439
- **書いてある場所**: lines 420 (## Limit and Gate Tools)
- **原文**:

> By default, the model gets every tool that the server lists, and each tool runs without approval.

- **日本語**: 既定では、モデルはサーバが出すツールをすべて受け取り、どのツールも承認なしで走る。
- **どう使っているか**: SDK の既定は注釈で何もしない（toolFilter と needsApproval はどちらも既定でオフ）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、420 行（## Limit and Gate Tools）（取得 2026-10-02T22:11:39Z、sha256 0917386c7436…）

<a id="g-c02-sdks-55"></a>
#### C02-55 TanStack (TanStack AI) — TanStack AI (@tanstack/ai-mcp)

- **資料**: MCP Server Tools > Tool Titles & Annotations（クライアントの文書）
- **URL**: https://tanstack.com/ai/latest/docs/tools/mcp
- **書いてある見出しへ直接**: https://tanstack.com/ai/latest/docs/tools/mcp#tool-titles-annotations
- **版**: tanstack.com/ai latest, 2026-10-02 取得
- **書いてある場所**: MCP Server Tools > Tool Titles & Annotations
- **原文**:

> On a server you have independently established as trusted, a hint may relax a confirmation step, as above; everywhere else, treat annotations as display labels and recommendations only — surface readOnlyHint as a badge (see the UI example below) rather than acting on it.

- **日本語**: 独立に信頼を確かめたサーバでは、ヒントで確認の手順をゆるめてよい。それ以外では、注釈は表示用のラベルと推奨としてだけ扱い、readOnlyHint は動作に使わずバッジとして見せる。
- **どう使っているか**: 信頼したサーバでだけ readOnlyHint で承認を省いてよく、それ以外はバッジ表示に留めよ、という指針。
- **条件**: アプリが独自に（サーバの申告ではなく設定で）信頼すると決めたサーバに限り、ヒントで確認を緩めてよい（may）。それ以外では表示ラベル・推奨に留める
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・表示（印・名前）・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Server Tools > Tool Titles & Annotations」（取得 2026-10-02T22:11:40Z、sha256 fd07474a5c7e…）
- **補足**: 同じ節の太字: 「Annotations are advisory, never a security boundary.」（id d33d で exact 確認）。title は tool.title → annotations.title → name の順で metadata.mcp.title に入る。 conditions が空だったので「独立に信頼を確立したサーバに限る」を足した。notes の title の順序（tool.title → annotations.title → name）は docs/tools/mcp.md 317 行を raw で exact 照合し、実装 packages/ai-mcp/src/tools.ts 50 行 `def.title ?? def.annotations?.title ?? def.name` も目視で確認。

### TanStack (TanStack AI) — TanStack AI (MCP server: serveMcp)

<a id="g-c02-sdks-56"></a>
#### C02-56 TanStack (TanStack AI) — TanStack AI (MCP server: serveMcp)

- **資料**: docs/mcp/server.md > Tell the host what a tool does（SDK の文書）
- **URL**: https://github.com/TanStack/ai/blob/d31e4ebb91d736476fef5ad2bd8b65234632d439/docs/mcp/server.md#L117
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/TanStack/ai/d31e4ebb91d736476fef5ad2bd8b65234632d439/docs/mcp/server.md
- **版**: commit d31e4ebb91d736476fef5ad2bd8b65234632d439
- **書いてある場所**: lines 117 (## Tell the host what a tool does)
- **原文**:

> A host asks the user before it runs a tool, unless the tool says it only reads. Set `metadata.title` and `metadata.annotations` on the tool definition.

- **日本語**: ホストは、ツールが読むだけだと言わない限り、実行の前にユーザーに聞く。ツール定義に metadata.title と metadata.annotations を付けよ。
- **どう使っているか**: サーバ作者に、読むだけのツールには readOnlyHint を付けるよう勧める（ホストの一般的な挙動としての主張）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、117 行（## Tell the host what a tool does）（取得 2026-10-02T22:11:31Z、sha256 455363e4cdca…）
- **補足**: ホストの挙動は TanStack 側の一般化で、特定ホストの資料ではない。 url に行番号のアンカーを足した（ツールの行番号と一致）。

### Pydantic (Pydantic AI) — Pydantic AI (MCP client)

<a id="g-c02-sdks-57"></a>
#### C02-57 Pydantic (Pydantic AI) — Pydantic AI (MCP client)

- **資料**: Client > Tool metadata (Pydantic AI docs)（クライアントの文書）
- **URL**: https://ai.pydantic.dev/mcp/client/
- **書いてある見出しへ直接**: https://pydantic.dev/docs/ai/mcp/client/#tool-metadata
- **版**: ai.pydantic.dev → pydantic.dev/docs/ai, 2026-10-02 取得
- **書いてある場所**: Client > Tool metadata
- **原文**:

> The meta and annotations fields can be found on the metadata dict on the ToolDefinition object that's passed to filter functions

- **日本語**: meta と annotations は、フィルタ関数に渡される ToolDefinition の metadata 辞書に入っている。
- **どう使っているか**: 注釈をツールのフィルタ（FilteredToolset）の材料として露出する。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Client > Tool metadata」（取得 2026-10-02T22:11:20Z、sha256 1a7b56cf8567…）
- **補足**: 取得時に https://pydantic.dev/docs/ai/mcp/client/ へリダイレクト。コードは pydantic_ai_slim/pydantic_ai/mcp.py 1315 行 `'annotations': mcp_tool.annotations.model_dump(by_alias=True) if mcp_tool.annotations else None,`（commit 6bc07cf18b0641ea92343d8c589cfb922108b802, id c34b で exact 確認）で camelCase のまま入る。

### Pydantic (Pydantic AI) — Pydantic AI Harness (CodeMode)

<a id="g-c02-sdks-58"></a>
#### C02-58 Pydantic (Pydantic AI) — Pydantic AI Harness (CodeMode)

- **資料**: src/pydantic_ai_harness/.../code_mode/README.md > Choose tools that are safe to run early（クライアントの文書）
- **URL**: https://github.com/pydantic/pydantic-ai/blob/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/code_mode/README.md#L363-L366
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/pydantic/pydantic-ai/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/code_mode/README.md
- **版**: commit 6bc07cf18b0641ea92343d8c589cfb922108b802
- **書いてある場所**: lines 363-366 (### Choose tools that are safe to run early)
- **原文**:

> Instead of naming tools, pass `speculate='declared'` to trust what the tools say about themselves: tools marked `Tool(..., metadata={'read_only': True})`, and MCP tools whose server publishes the `readOnlyHint` annotation. Idempotence is not enough, an idempotent delete still deletes, so `idempotent` declarations do not count.

- **日本語**: ツール名を並べる代わりに speculate='declared' を渡すと、ツール自身の申告を信じる（metadata={'read_only': True} の Tool と、サーバが readOnlyHint を出す MCP ツール）。冪等だけでは足りない（冪等な削除も削除する）ので、idempotent の申告は数えない。
- **どう使っているか**: CodeMode の先行実行（speculation: スニペットが実際に呼ぶ前にツール呼び出しを先に走らせ、使われなければ捨てる）の対象を選ぶ根拠に readOnlyHint を使う。idempotentHint は根拠にしない。ユーザー承認を省く話ではない。
- **条件**: speculate='declared' を指定したときだけ
- **扱う宣言**: readOnlyHint・idempotentHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認] 再照合 exact・1 か所、363-366 行（### Choose tools that are safe to run early）（取得 2026-10-02T22:11:40Z、sha256 f5458ba0e875…）
- **補足**: 実装は _speculation.py 244 行 `declared.get('annotations', {}).get('readOnlyHint')`（目視）。README の続き: 「A declaration is the tool author's claim, not a proof」。 usage から auto_approve を外し other にした（先行実行は承認の自動化ではなく、モデルが使わないかもしれない呼び出しを先に走らせる仕組み）。実装 _speculation.py 244 行「return bool(declared.get('read_only') or declared.get('annotations', {}).get('readOnlyHint'))」を commit 6bc07cf の raw で exact 照合（readOnlyHint が真のときだけ）。

### Mastra — Mastra (@mastra/mcp MCPClient)

<a id="g-c02-sdks-59"></a>
#### C02-59 Mastra — Mastra (@mastra/mcp MCPClient)

- **資料**: MCPClient > Constructor > requireToolApproval（クライアントの文書）
- **URL**: https://mastra.ai/reference/tools/mcp-client
- **書いてある見出しへ直接**: https://mastra.ai/reference/tools/mcp-client#constructor
- **版**: mastra.ai reference, 2026-10-02 取得
- **書いてある場所**: MCPClient > ConstructorDirect link to Constructor > requireToolApproval?:
- **原文**:

> When set to a function, the function is called with the tool name, arguments, request context, and any tool annotations advertised by the server to dynamically decide whether approval is needed.

- **日本語**: （requireToolApproval に）関数を渡すと、ツール名・引数・リクエストの文脈・サーバが出したツール注釈を受け取り、承認が要るかを動的に決める。
- **どう使っているか**: 承認判定の関数の入力に注釈を渡す。既定で注釈から何かを決めるわけではない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCPClient > ConstructorDirect link to Constructor > requireToolApproval?:」（取得 2026-10-02T22:11:29Z、sha256 3805ecf4bcd2…）
- **補足**: 注釈は listTools() / listToolsets() の tool.mcp.annotations にも出る。tool.title はサーバの title、無ければ annotations.title。

<a id="g-c02-sdks-60"></a>
#### C02-60 Mastra — Mastra (@mastra/mcp MCPClient)

- **資料**: MCPClient > Tool approval > Use tool annotations from a trusted server（クライアントの文書）
- **URL**: https://mastra.ai/reference/tools/mcp-client
- **書いてある見出しへ直接**: https://mastra.ai/reference/tools/mcp-client#use-tool-annotations-from-a-trusted-server
- **版**: mastra.ai reference, 2026-10-02 取得
- **書いてある場所**: MCPClient > Tool approvalDirect link to Tool approval > Use tool annotations from a trusted serverDirect link to Use tool annotations from a trusted server
- **原文**:

> Annotations are advisory hints and provide no security boundary. A malicious or buggy server can claim a tool is read-only when it isn't. Only use annotations to relax approval requirements for servers you trust.

- **日本語**: 注釈は助言のヒントで、セキュリティ境界にならない。悪意のある・バグのあるサーバは、読み取り専用でないツールを読み取り専用と言える。注釈で承認の要件をゆるめるのは、信頼するサーバに限れ。
- **どう使っているか**: 例: readOnlyHint なら承認不要、destructiveHint なら承認、その他も承認。信頼するサーバでのみ。
- **条件**: アプリが requireToolApproval にこの関数を書いた場合（SDK の既定ではない）で、信頼するサーバに限る（docs の指示）
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 信頼するなという注意・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCPClient > Tool approvalDirect link to Tool approval > Use tool annotations from a trusted serverDirect link to Use tool annotations from a trusted server」（取得 2026-10-02T22:11:29Z、sha256 3805ecf4bcd2…）
- **補足**: 注釈で承認を決めるのは docs の例の関数をアプリが書いたときだけなので、conditions に足した。

### Mastra — Mastra (createTool, MCPServer)

<a id="g-c02-sdks-61"></a>
#### C02-61 Mastra — Mastra (createTool, MCPServer)

- **資料**: createTool() > MCP tool annotations（SDK の文書）
- **URL**: https://mastra.ai/reference/tools/create-tool
- **書いてある見出しへ直接**: https://mastra.ai/reference/tools/create-tool#mcp-tool-annotations
- **版**: mastra.ai reference, 2026-10-02 取得
- **書いてある場所**: createTool() > MCP tool annotationsDirect link to MCP tool annotations > title?:
- **原文**:

> readOnlyHint ?: boolean If true, the tool does not modify its environment. This hint indicates the tool only reads data and has no side effects. Defaults to false.

- **日本語**: readOnlyHint?: boolean。true ならツールは環境を変えない。このヒントはツールがデータを読むだけで副作用が無いことを示す。既定値は false。
- **どう使っているか**: Mastra でサーバとして公開するツールは createTool({ mcp: { annotations: {...} } }) で宣言する。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「createTool() > MCP tool annotationsDirect link to MCP tool annotations > title?:」（取得 2026-10-02T22:11:27Z、sha256 60c4c40d155d…）
- **補足**: loose 一致（項目名と型の区切りの違い）。

### Basement Studio (xmcp) — xmcp (TypeScript MCP framework)

<a id="g-c02-sdks-62"></a>
#### C02-62 Basement Studio (xmcp) — xmcp (TypeScript MCP framework)

- **資料**: Tools > Metadata > Annotations (xmcp.dev)（SDK の文書）
- **URL**: https://xmcp.dev/docs/core-concepts/tools
- **書いてある見出しへ直接**: https://xmcp.dev/docs/core-concepts/tools#annotations
- **版**: xmcp.dev, 2026-10-02 取得
- **書いてある場所**: Tools > Metadata > Annotations
- **原文**:

> These hints are advisory only. LLMs may use them to make better decisions about when and how to call your tools, but they don't enforce any behavior.

- **日本語**: これらのヒントは助言だけ。LLM はいつ・どう呼ぶかの判断に使うかもしれないが、何の振る舞いも強制しない。
- **どう使っているか**: export const metadata = { annotations: {...} } で宣言。ヒントは助言にすぎず、LLM が呼び方の判断に使うかもしれない（may）が、何も強制しないと説明。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 作者への書き方の案内・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Metadata > Annotations」（取得 2026-10-02T22:11:41Z、sha256 bba3a01648aa…）
- **補足**: 原文は「LLMs may use them」で、ヒントを LLM 向けと位置づけている点を usage_ja に足した。

<a id="g-c02-sdks-63"></a>
#### C02-63 Basement Studio (xmcp) — xmcp (TypeScript MCP framework)

- **資料**: Tools > Metadata > Annotations のコード例（xmcp.dev, Markdown 版）（SDK の文書）
- **URL**: https://xmcp.dev/docs/core-concepts/tools#annotations
- **照らし合わせた中身の URL**: https://xmcp.dev/docs/core-concepts/tools.md
- **版**: xmcp.dev, 2026-10-02 取得
- **書いてある場所**: lines 151-152 (### Annotations)
- **原文**:

> // Tool doesn't modify its environment (safe to retry) readOnlyHint: true,

- **日本語**: // ツールは環境を変えない（再試行しても安全） readOnlyHint: true,
- **どう使っているか**: docs の例は題が "Create New Task" のツールに readOnlyHint: true と destructiveHint: false を付け、コメントで『環境を変えない（再試行しても安全）』と書く。作成するツールを読み取り専用とする、宣言と振る舞いが合わない手本。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、190-191 行（### Annotations）（取得 2026-10-02T22:11:48Z、sha256 288e98aa6ed9…）
- **補足**: 同じコード例の 149 行 `title: "Create New Task",` も exact で確認（id d38b）。『作成するツールに readOnlyHint を付けるのは誤り』はこの調査の解釈。

---

[← 付録 G-1 MCP の公式](appendix-g-1.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-3 Microsoft と GitHub →](appendix-g-3.md)
