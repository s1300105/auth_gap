[付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-2 SDK →](appendix-g-2.md)

---

# 付録 G-1 MCP の公式（仕様・スキーマ・公式サイト・ブログ・SEP・参照サーバ・Inspector）

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-1-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C01-01](#g-c01-mcp-official-01) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-07](#g-c01-mcp-official-07) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-09](#g-c01-mcp-official-09) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26 | リリースノート | その他 | [確認] |
| [C01-02](#g-c01-mcp-official-02) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-06-18 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-03](#g-c01-mcp-official-03) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-04](#g-c01-mcp-official-04) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-06](#g-c01-mcp-official-06) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 | 仕様 | 確認を求める | [確認] |
| [C01-08](#g-c01-mcp-official-08) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 | 仕様 | 信頼するなという注意 | [確認] |
| [C01-05](#g-c01-mcp-official-05) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification draft | 仕様 | 信頼するなという注意 | [確認] |
| [C01-10](#g-c01-mcp-official-10) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP schema 2025-03-26 (schema.ts) | 仕様 | 信頼するなという注意 | [確認] |
| [C01-11](#g-c01-mcp-official-11) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 (Schema Reference) | 仕様 | 信頼するなという注意 | [確認] |
| [C01-14](#g-c01-mcp-official-14) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 (Schema Reference) | 仕様 | 表示（印・名前） | [確認] |
| [C01-12](#g-c01-mcp-official-12) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 (Schema Reference) | 仕様 | 宣言が無いときの扱い | [確認] |
| [C01-13](#g-c01-mcp-official-13) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 (Schema Reference) | 仕様 | 宣言が無いときの扱い | [確認] |
| [C01-15](#g-c01-mcp-official-15) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25) | 公式の文書 | 信頼するなという注意・表示（印・名前） | [確認] |
| [C01-16](#g-c01-mcp-official-16) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25) | 公式の文書 | 確認を求める・表示（印・名前） | [確認] |
| [C01-17](#g-c01-mcp-official-17) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25) | 公式の文書 | 信頼するなという注意・作者への書き方の案内 | [確認] |
| [C01-18](#g-c01-mcp-official-18) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25) | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C01-19](#g-c01-mcp-official-19) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 宣言が無いときの扱い | [確認] |
| [C01-20](#g-c01-mcp-official-20) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 宣言が無いときの扱い・その他 | [確認] |
| [C01-21](#g-c01-mcp-official-21) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 確認を省く（自動で許可）・確認を求める | [確認] |
| [C01-22](#g-c01-mcp-official-22) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 信頼するなという注意・確認を省く（自動で許可） | [確認] |
| [C01-23](#g-c01-mcp-official-23) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 確認を省く（自動で許可）・確認を求める・その他 | [確認] |
| [C01-24](#g-c01-mcp-official-24) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | その他・規則（ポリシー）の条件に使う | [確認] |
| [C01-25](#g-c01-mcp-official-25) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | ツールを絞る・隠す・表示（印・名前） | [確認] |
| [C01-26](#g-c01-mcp-official-26) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 規則（ポリシー）の条件に使う | [確認] |
| [C01-27](#g-c01-mcp-official-27) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | その他 | [確認] |
| [C01-28](#g-c01-mcp-official-28) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 信頼するなという注意 | [確認] |
| [C01-29](#g-c01-mcp-official-29) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 作者への書き方の案内 | [確認] |
| [C01-30](#g-c01-mcp-official-30) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 信頼するなという注意・表示（印・名前） | [確認] |
| [C01-31](#g-c01-mcp-official-31) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 信頼するなという注意・その他 | [確認] |
| [C01-32](#g-c01-mcp-official-32) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | その他 | [確認] |
| [C01-33](#g-c01-mcp-official-33) | Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog | 公式ブログ | 確認を求める・確認を省く（自動で許可） | [確認] |
| [C01-34](#g-c01-mcp-official-34) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Tool Annotations Interest Group | 公式の文書 | その他 | [確認] |
| [C01-35](#g-c01-mcp-official-35) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Tool Annotations Interest Group | 公式の文書 | その他 | [確認] |
| [C01-36](#g-c01-mcp-official-36) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (docs) | 公式の文書 | 表示（印・名前） | [確認] |
| [C01-37](#g-c01-mcp-official-37) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (web client, main) | クライアントのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [C01-38](#g-c01-mcp-official-38) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v1 (1.0.2) | クライアントのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [C01-39](#g-c01-mcp-official-39) | Model Context Protocol project (reference servers) — Reference server: filesystem (TypeScript) | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C01-40](#g-c01-mcp-official-40) | Model Context Protocol project (reference servers) — Reference server: filesystem (README) | サーバの文書 | 作者への書き方の案内・表示（印・名前） | [確認] |
| [C01-41](#g-c01-mcp-official-41) | Model Context Protocol project (reference servers) — Reference server: git (Python) | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C01-42](#g-c01-mcp-official-42) | Model Context Protocol project (reference servers) — Reference server: memory (TypeScript) | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C01-43](#g-c01-mcp-official-43) | Model Context Protocol project (reference servers) — Reference server: time (Python) | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C01-44](#g-c01-mcp-official-44) | Model Context Protocol project (reference servers) — Reference server: sequentialthinking (TypeScript) | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C01-45](#g-c01-mcp-official-45) | Model Context Protocol project (reference servers) — Reference server: everything (TypeScript) | サーバの文書 | 作者への書き方の案内 | [確認] |
| [C01-46](#g-c01-mcp-official-46) | Model Context Protocol project (reference servers) — modelcontextprotocol/servers repo (agent instructions) | サーバの文書 | 作者への書き方の案内 | [確認] |
| [C01-47](#g-c01-mcp-official-47) | Model Context Protocol project (reference servers) — Reference server: fetch (Python) | サーバのソースコード | 宣言が無いときの扱い | [確認] |
| [C01-48](#g-c01-mcp-official-48) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1862 | issue / PR / 提案の下書き | 確認を求める | [確認] |
| [C01-49](#g-c01-mcp-official-49) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1862 | issue / PR / 提案の下書き | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C01-50](#g-c01-mcp-official-50) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1913 | issue / PR / 提案の下書き | 規則（ポリシー）の条件に使う・危険度を付ける | [確認] |
| [C01-51](#g-c01-mcp-official-51) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1913 | issue / PR / 提案の下書き | 確認を求める・その他 | [確認] |
| [C01-52](#g-c01-mcp-official-52) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1984 | issue / PR / 提案の下書き | 宣言が無いときの扱い・信頼するなという注意 | [確認] |
| [C01-53](#g-c01-mcp-official-53) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1984 | issue / PR / 提案の下書き | 危険度を付ける・確認を求める | [確認] |
| [C01-54](#g-c01-mcp-official-54) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2793 | issue / PR / 提案の下書き | 宣言が無いときの扱い・危険度を付ける・確認を求める | [確認] |
| [C01-55](#g-c01-mcp-official-55) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2793 | issue / PR / 提案の下書き | 危険度を付ける | [確認] |
| [C01-56](#g-c01-mcp-official-56) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1938 | issue / PR / 提案の下書き | 確認を求める・表示（印・名前） | [確認] |
| [C01-57](#g-c01-mcp-official-57) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2061 | issue / PR / 提案の下書き | 確認を求める・その他 | [確認] |
| [C01-58](#g-c01-mcp-official-58) | Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-3140 | issue / PR / 提案の下書き | 信頼するなという注意・宣言を検査する | [確認] |
| [C01-59](#g-c01-mcp-official-59) | Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations | 公式の文書 | 信頼するなという注意・宣言を検査する | [確認] |
| [C01-60](#g-c01-mcp-official-60) | Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (trust-annotations draft) | 公式の文書 | その他 | [確認] |
| [C01-61](#g-c01-mcp-official-61) | Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (action-metadata draft) | 公式の文書 | その他 | [確認] |

この分冊の資料は 61 件で、うち [確認] は 61 件、[確認（調査時のみ）] は 0 件。

<a id="ag-1-1"></a>
## 資料カード

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26

<a id="g-c01-mcp-official-01"></a>
#### C01-01 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26

- **資料**: Tools (Server Features) — specification 2025-03-26（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-03-26/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-03-26/server/tools#tool
- **版**: 2025-03-26
- **書いてある場所**: Tools > Data Types > Tool (#tool)
- **原文**:

> For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

- **日本語**: 信頼できるサーバから来たものでない限り、ツールの annotations は信頼できないものとして扱わなければならない（MUST）。
- **どう使っているか**: 仕様本体の規範文。クライアントは、信頼できるサーバ以外の annotations を信頼してはならない。自動承認・確認要否などに使ってよいかは『信頼できるサーバか』に条件づけられる。
- **条件**: 『trusted servers』から来た場合だけ信頼してよい。何を trusted とするか（判定方法・設定）は仕様に定義がない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Data Types > Tool」（取得 2026-10-02T22:09:33Z、sha256 3355a31ce601…）
- **補足**: annotations が初めて入った版。Tool 定義の節で `annotations: optional properties describing tool behavior` の直後に Warning として置かれる。 2024-11-05 版の tools ページには annotations の語が無い（checked_no_mention 参照）。

<a id="g-c01-mcp-official-07"></a>
#### C01-07 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26

- **資料**: Specification overview — Security and Trust & Safety / Tool Safety (2025-03-26)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-03-26
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-03-26#key-principles
- **版**: 2025-03-26
- **書いてある場所**: Specification > Security and Trust & Safety > Key Principles (#key-principles)
- **原文**:

> In particular, descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a trusted server.

- **日本語**: 特に、annotations のようなツールの振る舞いの説明は、信頼できるサーバから得たものでない限り、信頼できないものとみなすべきである。
- **どう使っているか**: 仕様の概要ページ（Key Principles の Tool Safety）。annotations は信頼できるサーバ由来でなければ untrusted。同じ箇条に『Hosts must obtain explicit user consent before invoking any tool』がある。
- **条件**: trusted server 由来なら別扱いの余地がある、という条件つき。trusted の定義は無い（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Specification > Security and Trust & Safety > Key Principles」（取得 2026-10-02T22:10:35Z、sha256 b4302178a5c0…）
- **補足**: 2025-03-26 で追加（commit f025054d『added language in Security and Trust & Safety section re trusting annotations』を git log で確認）。

<a id="g-c01-mcp-official-09"></a>
#### C01-09 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-03-26

- **資料**: Key Changes (changelog) — 2025-03-26（リリースノート）
- **URL**: https://modelcontextprotocol.io/specification/2025-03-26/changelog
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-03-26/changelog#major-changes
- **版**: 2025-03-26
- **書いてある場所**: Key Changes > Major changes (#major-changes)
- **原文**:

> Added comprehensive tool annotations for better describing tool behavior, like whether it is read-only or destructive

- **日本語**: ツールの振る舞い（読み取り専用か、破壊的か など）をよりよく記述するため、包括的なツール annotations を追加した。
- **どう使っているか**: annotations が導入された版と目的（振る舞いの記述）を示す変更履歴。使い方（自動承認など）は書かれていない。
- **扱う宣言**: 宣言全般・readOnlyHint・destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Key Changes > Major changes」（取得 2026-10-02T22:10:36Z、sha256 9ab8095a1ce2…）
- **補足**: PR #185 (modelcontextprotocol/specification) へのリンクつき。2025-06-18 / 2025-11-25 / 2026-07-28 の changelog には ToolAnnotations の変更が無い（checked_no_mention 参照）。2025-06-18 で Tool.title が追加され、annotations.title との表示優先順位が決まった（Schema Reference の Tool.annotations）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-06-18

<a id="g-c01-mcp-official-02"></a>
#### C01-02 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-06-18

- **資料**: Tools (Server Features) — specification 2025-06-18（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool
- **版**: 2025-06-18
- **書いてある場所**: Tools > Data Types > Tool (#tool)
- **原文**:

> For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

- **日本語**: 信頼できるサーバから来たものでない限り、ツールの annotations は信頼できないものとして扱わなければならない（MUST）。
- **どう使っているか**: 仕様本体の規範文。クライアントは、信頼できるサーバ以外の annotations を信頼してはならない。自動承認・確認要否などに使ってよいかは『信頼できるサーバか』に条件づけられる。
- **条件**: 『trusted servers』から来た場合だけ信頼してよい。何を trusted とするか（判定方法・設定）は仕様に定義がない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Data Types > Tool」（取得 2026-10-02T22:12:53Z、sha256 475df1a7bf1f…）
- **補足**: 2025-03-26 と同文。 2024-11-05 版の tools ページには annotations の語が無い（checked_no_mention 参照）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25

<a id="g-c01-mcp-official-03"></a>
#### C01-03 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25

- **資料**: Tools (Server Features) — specification 2025-11-25（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-11-25/server/tools#tool
- **版**: 2025-11-25
- **書いてある場所**: Tools > Data Types > Tool (#tool)
- **原文**:

> For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

- **日本語**: 信頼できるサーバから来たものでない限り、ツールの annotations は信頼できないものとして扱わなければならない（MUST）。
- **どう使っているか**: 仕様本体の規範文。クライアントは、信頼できるサーバ以外の annotations を信頼してはならない。自動承認・確認要否などに使ってよいかは『信頼できるサーバか』に条件づけられる。
- **条件**: 『trusted servers』から来た場合だけ信頼してよい。何を trusted とするか（判定方法・設定）は仕様に定義がない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Data Types > Tool」（取得 2026-10-02T22:11:30Z、sha256 e79ed710ae99…）
- **補足**: 2025-03-26 と同文（Warning ブロックの改行位置だけ違う）。 2024-11-05 版の tools ページには annotations の語が無い（checked_no_mention 参照）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28

<a id="g-c01-mcp-official-04"></a>
#### C01-04 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28

- **資料**: Tools (Server Features) — specification 2026-07-28（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2026-07-28/server/tools#tool
- **版**: 2026-07-28
- **書いてある場所**: Tools > Data Types > Tool (#tool)
- **原文**:

> For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

- **日本語**: 信頼できるサーバから来たものでない限り、ツールの annotations は信頼できないものとして扱わなければならない（MUST）。
- **どう使っているか**: 仕様本体の規範文。クライアントは、信頼できるサーバ以外の annotations を信頼してはならない。自動承認・確認要否などに使ってよいかは『信頼できるサーバか』に条件づけられる。
- **条件**: 『trusted servers』から来た場合だけ信頼してよい。何を trusted とするか（判定方法・設定）は仕様に定義がない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Data Types > Tool」（取得 2026-10-02T22:10:34Z、sha256 fd9d459a1428…）
- **補足**: 2026-07-28 版（現行の最新リリース版）でも同文。annotations の語彙・既定値も変更なし（schema.ts を目視で比較）。 2024-11-05 版の tools ページには annotations の語が無い（checked_no_mention 参照）。

<a id="g-c01-mcp-official-06"></a>
#### C01-06 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28

- **資料**: Tools — User Interaction Model (specification 2026-07-28)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2026-07-28/server/tools#user-interaction-model
- **版**: 2026-07-28
- **書いてある場所**: Tools > User Interaction Model (#user-interaction-model)
- **原文**:

> For trust & safety and security, there SHOULD always be a human in the loop with the ability to deny tool invocations.

- **日本語**: 安全とセキュリティのため、ツール呼び出しを拒否できる人間が常にループの中にいるべきである（SHOULD）。
- **どう使っているか**: ツール呼び出しの人間による確認（拒否できること）を一般に求める文。annotations による確認の省略・自動承認については何も書いていない。
- **条件**: 全ツール呼び出しが対象。annotations で条件を変えてよいとは書かれていない。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > User Interaction Model」（取得 2026-10-02T22:10:34Z、sha256 fd9d459a1428…）
- **補足**: この節自体は annotations に触れない（文脈として記録）。同じ Warning ブロックに『Present confirmation prompts to the user for operations』もある（目視）。2024-11-05〜draft の全版に同じ文がある（リポジトリの tools.mdx を grep で確認）。

<a id="g-c01-mcp-official-08"></a>
#### C01-08 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28

- **資料**: Specification overview — Security and Trust & Safety / Tool Safety (2026-07-28)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2026-07-28
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2026-07-28#key-principles
- **版**: 2026-07-28
- **書いてある場所**: Specification > Security and Trust & Safety > Key Principles (#key-principles)
- **原文**:

> In particular, descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a trusted server.

- **日本語**: 特に、annotations のようなツールの振る舞いの説明は、信頼できるサーバから得たものでない限り、信頼できないものとみなすべきである。
- **どう使っているか**: 仕様の概要ページ（Key Principles の Tool Safety）。annotations は信頼できるサーバ由来でなければ untrusted。同じ箇条に『Hosts must obtain explicit user consent before invoking any tool』がある。
- **条件**: trusted server 由来なら別扱いの余地がある、という条件つき。trusted の定義は無い（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Specification > Security and Trust & Safety > Key Principles」（取得 2026-10-02T22:10:36Z、sha256 3d257ea31b15…）
- **補足**: 2026-07-28 版でも同文（2025-06-18 / 2025-11-25 / draft の index.mdx も同文を grep で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification draft

<a id="g-c01-mcp-official-05"></a>
#### C01-05 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification draft

- **資料**: Tools (Server Features) — specification draft（仕様）
- **URL**: https://modelcontextprotocol.io/specification/draft/server/tools
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/draft/server/tools#tool
- **版**: draft
- **書いてある場所**: Tools > Data Types > Tool (#tool)
- **原文**:

> For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers.

- **日本語**: 信頼できるサーバから来たものでない限り、ツールの annotations は信頼できないものとして扱わなければならない（MUST）。
- **どう使っているか**: 仕様本体の規範文。クライアントは、信頼できるサーバ以外の annotations を信頼してはならない。自動承認・確認要否などに使ってよいかは『信頼できるサーバか』に条件づけられる。
- **条件**: 『trusted servers』から来た場合だけ信頼してよい。何を trusted とするか（判定方法・設定）は仕様に定義がない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Data Types > Tool」（取得 2026-10-02T22:10:35Z、sha256 553084d5b27c…）
- **補足**: draft でも同文。 2024-11-05 版の tools ページには annotations の語が無い（checked_no_mention 参照）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP schema 2025-03-26 (schema.ts)

<a id="g-c01-mcp-official-10"></a>
#### C01-10 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP schema 2025-03-26 (schema.ts)

- **資料**: schema/2025-03-26/schema.ts — ToolAnnotations doc comment（仕様）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/3098fe94caa1b9e0afaaa6d30e040b61d5802471/schema/2025-03-26/schema.ts#L727-L779
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/3098fe94caa1b9e0afaaa6d30e040b61d5802471/schema/2025-03-26/schema.ts
- **版**: 2025-03-26 (repo commit 3098fe9)
- **書いてある場所**: lines 734-735
- **原文**:

> Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers.

- **日本語**: クライアントは、信頼できないサーバから受け取った ToolAnnotations に基づいてツール使用の判断をしてはならない（should never）。
- **どう使っているか**: スキーマ（正本の TypeScript）の注記。ツール使用の判断（呼ぶか・確認を省くか等）に untrusted サーバの annotations を使うな、という意味。
- **条件**: untrusted サーバ由来のとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 loose・1 か所、734-735 行（取得 2026-10-02T22:10:36Z、sha256 bdc457208cb1…）
- **補足**: 2025-03-26 の公開 schema ページは 404（https://modelcontextprotocol.io/specification/2025-03-26/schema）なので raw の schema.ts で確認。同じ注記は 2025-06-18 / 2025-11-25 / 2026-07-28 / draft の schema.ts にもある（目視）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 (Schema Reference)

<a id="g-c01-mcp-official-11"></a>
#### C01-11 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 (Schema Reference)

- **資料**: Schema Reference — ToolAnnotations (2025-11-25)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-11-25/schema#toolannotations
- **照らし合わせた中身の URL**: https://modelcontextprotocol.io/specification/2025-11-25/schema
- **版**: 2025-11-25
- **書いてある場所**: Schema Reference > tools/list > ToolAnnotations (#toolannotations)
- **原文**:

> NOTE: all properties in ToolAnnotations are hints. They are not guaranteed to provide a faithful description of tool behavior (including descriptive properties like title). Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers.

- **日本語**: 注意：ToolAnnotations のすべての属性は『ヒント』である。ツールの振る舞いを正しく表すとは保証されない（title のような説明的な属性も含む）。クライアントは、信頼できないサーバから受け取った ToolAnnotations でツール使用の判断をしてはならない。
- **どう使っているか**: 全属性が hint であり正しさは保証されない、と明記。untrusted サーバ由来のものは判断に使わない。
- **条件**: untrusted サーバ由来のとき。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title・宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Schema Reference > tools/list > ToolAnnotations」（取得 2026-10-02T22:10:37Z、sha256 d08d1390a749…）
- **補足**: 1 回目の取得は TLS エラー（curl 35 SSL_ERROR_SYSCALL）で失敗、再試行で exact。

<a id="g-c01-mcp-official-14"></a>
#### C01-14 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2025-11-25 (Schema Reference)

- **資料**: Schema Reference — Tool.annotations (2025-11-25)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2025-11-25/schema#tool-annotations
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2025-11-25/schema#tool
- **照らし合わせた中身の URL**: https://modelcontextprotocol.io/specification/2025-11-25/schema
- **版**: 2025-11-25
- **書いてある場所**: Schema Reference > tools/list > Tool (#tool)
- **原文**:

> Display name precedence order is: title, annotations.title, then name.

- **日本語**: 表示名の優先順位は、title、annotations.title、name の順である。
- **どう使っているか**: annotations.title の使い道：UI の表示名。Tool.title が無ければ annotations.title、それも無ければ name を表示する。
- **条件**: Tool.title（2025-06-18 で追加）が無いとき annotations.title が使われる。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Schema Reference > tools/list > Tool」（取得 2026-10-02T22:10:37Z、sha256 d08d1390a749…）
- **補足**: 2025-06-18 / 2026-07-28 / draft の schema.ts にも同文（2026-07-28 はバッククォートつき）。BaseMetadata.title にも『except for Tool, where annotations.title should be given precedence over using name』とある（目視）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 (Schema Reference)

<a id="g-c01-mcp-official-12"></a>
#### C01-12 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 (Schema Reference)

- **資料**: Schema Reference — ToolAnnotations.destructiveHint (2026-07-28)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations-destructivehint
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations
- **照らし合わせた中身の URL**: https://modelcontextprotocol.io/specification/2026-07-28/schema
- **版**: 2026-07-28
- **書いてある場所**: Schema Reference > tools/list > ToolAnnotations (#toolannotations)
- **原文**:

> If true, the tool may perform destructive updates to its environment. If false, the tool performs only additive updates. (This property is meaningful only when readOnlyHint == false) Default: true

- **日本語**: true なら、ツールは環境に破壊的な更新をするかもしれない。false なら追加的な更新だけをする。（readOnlyHint == false のときだけ意味がある）既定値：true
- **どう使っているか**: 省略時の既定値の定義。destructiveHint を書かなければ『破壊的かもしれない』（true）とみなされる。readOnlyHint の既定は false。
- **条件**: destructiveHint は readOnlyHint == false のときだけ意味を持つ。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Schema Reference > tools/list > ToolAnnotations」（取得 2026-10-02T22:11:36Z、sha256 24f9363de2aa…）
- **補足**: 同じ schema ページの他の既定値：readOnlyHint 既定 false、idempotentHint 既定 false、openWorldHint 既定 true。2025-03-26 以降すべての版で同じ（schema.ts を目視比較）。

<a id="g-c01-mcp-official-13"></a>
#### C01-13 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Specification 2026-07-28 (Schema Reference)

- **資料**: Schema Reference — ToolAnnotations.openWorldHint (2026-07-28)（仕様）
- **URL**: https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations-openworldhint
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations
- **照らし合わせた中身の URL**: https://modelcontextprotocol.io/specification/2026-07-28/schema
- **版**: 2026-07-28
- **書いてある場所**: Schema Reference > tools/list > ToolAnnotations (#toolannotations)
- **原文**:

> If true, this tool may interact with an "open world" of external entities. If false, the tool's domain of interaction is closed. For example, the world of a web search tool is open, whereas that of a memory tool is not. Default: true

- **日本語**: true なら、このツールは外部の『開かれた世界』とやりとりするかもしれない。false なら、やりとりする範囲は閉じている。たとえば Web 検索ツールの世界は開いていて、メモリツールの世界は閉じている。既定値：true
- **どう使っているか**: openWorldHint の意味と既定値（true）。書かなければ『外部とやりとりするかもしれない』とみなされる。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Schema Reference > tools/list > ToolAnnotations」（取得 2026-10-02T22:11:36Z、sha256 24f9363de2aa…）
- **補足**: 『external』の範囲（社外か、マシン外か）は定義されていない。公式ブログ 2026-03-16 が『配置の文脈で変わる』と述べている。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25)

<a id="g-c01-mcp-official-15"></a>
#### C01-15 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25)

- **資料**: Concepts: Tools — Tool annotations (legacy docs page)（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx#L335-L337
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx
- **版**: commit e30f85cb (parent of 828bd471, which deleted the page on 2026-03-25)
- **書いてある場所**: lines 337 / ## Tool annotations
- **原文**:

> These annotations are hints that describe the nature and impact of a tool, but should not be relied upon for security decisions.

- **日本語**: これらの annotations はツールの性質と影響を説明するヒントだが、セキュリティ上の判断の根拠にしてはならない。
- **どう使っているか**: 旧 Concepts ページ。直前の文は『クライアントがツールをどう表示し管理するかを理解する助けになる』。表示・管理には使うが、セキュリティ判断には使うな、という立場。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、337 行（## Tool annotations）（取得 2026-10-02T22:12:04Z、sha256 539601b33a45…）
- **補足**: このページは公開サイトから削除済み。/docs/concepts/tools は現在 /specification/2026-07-28/server/tools へ、/legacy/concepts/tools は /specification/latest/server/tools へリダイレクト（docs.json と curl の 308 で確認）。2025-04-10 の commit 16fb5f10（Basil Hosmer『Add documentation for ToolAnnotations』）で追加。学生が開くのは GitHub の blob（commit 固定）。

<a id="g-c01-mcp-official-16"></a>
#### C01-16 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25)

- **資料**: Concepts: Tools — Purpose of tool annotations (legacy docs page)（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx#L339-L346
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx
- **版**: commit e30f85cb
- **書いてある場所**: lines 346 / ### Purpose of tool annotations
- **原文**:

> Assist in developing intuitive interfaces for tool approval

- **日本語**: ツール承認のための分かりやすい UI 作りを助ける
- **どう使っているか**: 旧ページが挙げた目的 4 つのうちの 4 番目。ほかは (1) モデルの文脈に影響しない UX 用情報、(2) ツールの分類・表示、(3) 副作用の伝達（L341-346）。承認 UI に使うことが想定されていた。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、346 行（### Purpose of tool annotations）（取得 2026-10-02T22:12:04Z、sha256 539601b33a45…）
- **補足**: 同じページの表で既定値（readOnlyHint false / destructiveHint true / idempotentHint false / openWorldHint true）と、TS・Python のサーバ実装例（annotations={readOnlyHint: True, openWorldHint: False}）も示していた（目視）。

<a id="g-c01-mcp-official-17"></a>
#### C01-17 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25)

- **資料**: Concepts: Tools — Best practices for tool annotations (legacy docs page)（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx#L484-L494
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx
- **版**: commit e30f85cb
- **書いてある場所**: lines 494 / ### Best practices for tool annotations
- **原文**:

> **Remember annotations are hints**: All properties in ToolAnnotations are hints and not guaranteed to provide a faithful description of tool behavior. Clients should never make security-critical decisions based solely on annotations.

- **日本語**: annotations はヒントだと覚えておくこと：ToolAnnotations の属性はすべてヒントで、ツールの振る舞いを正しく表すとは保証されない。クライアントは annotations だけを根拠にセキュリティ上重要な判断をしてはならない。
- **どう使っているか**: サーバ作者向けベストプラクティス 5 項目の最後。クライアントは annotations『だけで』セキュリティ上重要な判断をしてはならない。ただし同じページの冒頭（L337、#15）は『should not be relied upon for security decisions』と『solely』の限定なしで書いており、『他の情報と組み合わせれば可』とまでは言えない（同じページの中で強さが揺れている）。
- **条件**: 『solely（それだけで）』という限定つき。ただし同じページ L337 は限定なし（#15）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、494 行（### Best practices for tool annotations）（取得 2026-10-02T22:12:04Z、sha256 539601b33a45…）
- **補足**: 同じ節の 1 番目（L486、検証済み）：『Be accurate about side effects: Clearly indicate whether a tool modifies its environment and whether those modifications are destructive.』。ほか『Indicate idempotency properly』『Set appropriate open/closed world hints』（目視）。 usage_ja の『（他の情報と組み合わせるなら可、と読める）』を削除・修正：同じページ L337 が限定なしで『security decisions に頼るな』と書いており、この読みは同ページで支持されない。

<a id="g-c01-mcp-official-18"></a>
#### C01-18 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP docs (legacy Concepts: Tools, removed 2026-03-25)

- **資料**: Concepts: Tools — Best practices for tool annotations, item 1 (legacy docs page)（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx#L486
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/e30f85cb01f42905b1244f97f51c70a599533958/docs/legacy/concepts/tools.mdx
- **版**: commit e30f85cb
- **書いてある場所**: lines 486 / ### Best practices for tool annotations
- **原文**:

> **Be accurate about side effects**: Clearly indicate whether a tool modifies its environment and whether those modifications are destructive.

- **日本語**: 副作用について正確に：ツールが環境を変更するか、その変更が破壊的かをはっきり示すこと。
- **どう使っているか**: サーバ作者向け：readOnlyHint / destructiveHint を実際の副作用に合わせて正確に設定せよ。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、486 行（### Best practices for tool annotations）（取得 2026-10-02T22:12:04Z、sha256 539601b33a45…）
- **補足**: 宣言と実際の副作用の一致を作者の責任とする記述。検証の仕組みは書かれていない。

### Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

<a id="g-c01-mcp-official-19"></a>
#### C01-19 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-tool-annotations-are
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are (#what-tool-annotations-are)
- **原文**:

> The defaults are deliberately cautious: a tool with no annotations is assumed to be non-read-only, potentially destructive, non-idempotent, and open-world.

- **日本語**: 既定値はわざと慎重にしてある：annotations の無いツールは、読み取り専用でなく、破壊的かもしれず、冪等でなく、外部世界とやりとりする、とみなされる。
- **どう使っているか**: annotations が無いときの扱い：最悪を仮定する既定値（readOnly=false, destructive=true, idempotent=false, openWorld=true）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）

<a id="g-c01-mcp-official-20"></a>
#### C01-20 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-tool-annotations-are
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are (#what-tool-annotations-are)
- **原文**:

> Many servers ship without them, and clients vary in how strictly they honor the pessimistic defaults.

- **日本語**: 多くのサーバは annotations を付けずに配布されており、悲観的な既定値をどれだけ厳密に守るかはクライアントによってまちまちである。
- **どう使っているか**: 公式ブログ自身が、欠落が多いこと・クライアントが既定値を守る度合いがばらばらであることを認めている。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: どのクライアントがどう違うかの具体名・数値は書かれていない（不明）。

<a id="g-c01-mcp-official-21"></a>
#### C01-21 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-can-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do (#what-annotations-can-do)
- **原文**:

> A tool marked readOnlyHint: true from a trusted server might be auto-approved, while destructiveHint: true gets a confirmation step. A user asks their agent to clean up old files, the agent reaches for delete_file, and the client shows a dialog listing what's about to be deleted before anything happens. This is the most common use of annotations today.

- **日本語**: 信頼できるサーバからの readOnlyHint: true のツールは自動承認されうる。一方 destructiveHint: true なら確認の段階が入る。古いファイルの整理を頼むと、エージェントは delete_file を使おうとし、クライアントは実行前に削除対象を並べたダイアログを出す。これが今いちばん多い annotations の使い方である。
- **どう使っているか**: annotations の主な用途は確認ダイアログの制御。readOnlyHint:true → 自動承認の候補（trusted server のとき）、destructiveHint:true → 確認。
- **条件**: 自動承認は『from a trusted server』のとき、かつ『might be』（できる、であって義務ではない）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 見出し『What Annotations Can Do』の『Drive confirmation prompts.』の段落。どのクライアントがそうしているかの名前は無い。

<a id="g-c01-mcp-official-22"></a>
#### C01-22 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#2-does-it-need-trust-to-be-useful
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Questions for Evaluating New Annotations > 2. Does it need trust to be useful? (#2-does-it-need-trust-to-be-useful)
- **原文**:

> readOnlyHint from an untrusted server isn't actionable, because the decision it informs — whether to skip a confirmation — only makes sense if you believe the hint.

- **日本語**: 信頼できないサーバからの readOnlyHint は使いようがない。それが左右する判断（確認を省くかどうか）は、ヒントを信じる場合にしか意味がないからだ。
- **どう使っているか**: readOnlyHint の用途を『確認を省くかの判断』と明言し、untrusted サーバでは使えないとする。
- **条件**: untrusted サーバのとき使えない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Questions for Evaluating New Annotations > 2. Does it need trust to be useful?」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 節『2. Does it need trust to be useful?』。title は untrusted でも有用（最悪でも表示名が変になるだけ）と対比している。

<a id="g-c01-mcp-official-23"></a>
#### C01-23 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#1-what-client-behavior-does-it-enable
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/3098fe94caa1b9e0afaaa6d30e040b61d5802471/blog/content/posts/2026-03-16-tool-annotations.md
- **版**: 2026-03-16
- **書いてある場所**: lines 118 / ### 1. What client behavior does it enable?
- **原文**:

> | `idempotentHint: true`  | Safe to retry on failure                                             |

- **日本語**: idempotentHint: true → 失敗時に再試行してよい
- **どう使っているか**: 各ヒントに対応するクライアント動作の例の表：readOnlyHint:true → 確認ダイアログを省く、destructiveHint:true → 実行前に警告、idempotentHint:true → 失敗時に再試行してよい、openWorldHint:true → 出力の信頼できない内容を精査・信頼境界を越えたと印をつける。
- **条件**: 表の列名は『Example client behavior』で、例示であり規範ではない。readOnlyHint:true で確認を省くことは、同じブログの『2. Does it need trust to be useful?』（#22）で『untrusted サーバからの readOnlyHint は使いようがない』とされ、trusted server 由来のときに限られる。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、118 行（### 1. What client behavior does it enable?）（取得 2026-10-02T22:11:35Z、sha256 b75aa06bbcac…）
- **補足**: 表の 4 行のうち idempotentHint 行を引用（readOnlyHint 行『Skip the confirmation dialog』は L116、destructiveHint 行は L117、openWorldHint 行は L119）。引用は Markdown の表記（| 区切り）のため、ブログの Markdown 原稿（spec リポジトリ blog/content/posts/2026-03-16-tool-annotations.md, commit 3098fe9）で確認。公開 HTML にも同じ表がある（検証者が HTML で『Safe to retry on failure』『Each of the existing hints maps to at least one decision a client can make』を exact で確認、見出し #1-what-client-behavior-does-it-enable）。 notes の『HTML の表は抽出で崩れるため』は誤り（公開 HTML でも表の行の文は exact で見つかる）。anchored_url を公開ブログの見出し #1-what-client-behavior-does-it-enable に設定（HTML で確認）。conditions に『例示』と trusted server 条件（#22）を追加。

<a id="g-c01-mcp-official-24"></a>
#### C01-24 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-can-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do (#what-annotations-can-do)
- **原文**:

> In practice most clients still treat installation itself as the trust signal and don't distinguish further, so this is more of a design opportunity than a widely shipped feature.

- **日本語**: 実際には、ほとんどのクライアントはインストールしたこと自体を信頼の印として扱い、それ以上区別しない。だから（サーバごとに信頼の段階をつけるのは）広く出荷された機能というより設計上の可能性である。
- **どう使っているか**: 仕様の『trusted server』を実装上どう決めているか：多くのクライアントは『インストール済み＝信頼』としている、という公式ブログの観察。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 見出し『Enable graduated trust.』の段落。どのクライアントかの具体名・調査方法は無い（未検証の観察）。

<a id="g-c01-mcp-official-25"></a>
#### C01-25 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-can-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do (#what-annotations-can-do)
- **原文**:

> This is largely unexploited today: no MCP client lets users filter tools by annotation values, and none surface annotations as context in approval prompts. GitHub's read-only mode is the closest production analog, enabled by about 17% of users.

- **日本語**: これは今ほとんど活用されていない：annotations の値でツールを絞り込めるクライアントは無く、承認プロンプトに annotations を文脈として出すクライアントも無い。最も近い実例は GitHub の read-only モードで、利用者の約 17% が有効にしている。
- **どう使っているか**: 2026-03 時点の公式ブログの主張：annotations による絞り込み UI も、承認プロンプトでの annotations 表示も、どのクライアントにも無い。
- **条件**: 2026-03-16 時点の主張。否定の観察：usage の filter_or_hide_tools / display_label は『そうした使い方をするクライアントが無い』という記述であり、使われている証拠ではない。調査方法・対象クライアントは書かれていない。
- **扱う宣言**: 宣言全般・readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 『17%』は GitHub 側の数値の転記で、出典・分母は書かれていない。verified_by_me = none（未検証の統計）。『no MCP client』という全称の主張も調査方法の記載が無い。 conditions に、usage タグが『使われていない』という否定の主張であることを明記（集計で肯定の証拠として数えないため）。

<a id="g-c01-mcp-official-26"></a>
#### C01-26 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-can-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do (#what-annotations-can-do)
- **原文**:

> Annotations can be one input among several into a policy engine enforcing rules like "no destructive tools without approval" or "open-world tools are blocked in sessions that have accessed private data."

- **日本語**: annotations は、『承認なしに破壊的ツールを使わない』『私的データに触れたセッションでは open-world ツールを止める』のような規則を強制するポリシーエンジンへの、いくつかある入力の 1 つになりうる。
- **どう使っているか**: ポリシーエンジンへの入力（単独ではなく他の信号と突き合わせる）としての使い方の例。
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 直後の文：『The hints don't need to be perfectly trustworthy if the engine cross-references other signals.』（目視）。

<a id="g-c01-mcp-official-27"></a>
#### C01-27 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-can-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do (#what-annotations-can-do)
- **原文**:

> Developers building autonomous agents treat confirmations as friction and lean on sandboxing instead. Enterprise adopters want more annotations than currently exist.

- **日本語**: 自律エージェントを作る開発者は確認を邪魔ものとみなし、代わりにサンドボックスに頼る。企業の導入者は今より多くの annotations を求めている。
- **どう使っているか**: 採用が偏っている理由として、利用者が 2 つの陣営に分かれていると述べる。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 根拠となる調査は示されていない（観察）。

<a id="g-c01-mcp-official-28"></a>
#### C01-28 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-annotations-cant-do
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can't Do (#what-annotations-cant-do)
- **原文**:

> A server can claim readOnlyHint: true and delete your files anyway. This is why the spec says clients must treat annotations from untrusted servers as untrusted.

- **日本語**: サーバは readOnlyHint: true と主張しながらファイルを消すこともできる。だから仕様は、untrusted サーバからの annotations を untrusted として扱えと言っている。
- **どう使っているか**: 宣言と実際の振る舞いが食い違う（嘘をつく）可能性を明示。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Annotations Can't Do」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 見出し『What Annotations Can't Do』の『An untrusted server can lie.』。同じ節に『They aren't enforcement.』（保証が要るならネットワーク制御やサンドボックスで）もある（目視）。AuthGap の対象（宣言 vs 実効の食い違い）に直接関係する公式の記述。

<a id="g-c01-mcp-official-29"></a>
#### C01-29 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#where-this-is-heading
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Where This Is Heading (#where-this-is-heading)
- **原文**:

> If you're writing a server, set readOnlyHint: true on read-only tools, destructiveHint: false on additive operations, and openWorldHint: false on closed-domain tools.

- **日本語**: サーバを書くなら、読み取り専用ツールには readOnlyHint: true、追加だけの操作には destructiveHint: false、閉じた範囲のツールには openWorldHint: false を付けること。
- **どう使っているか**: サーバ作者向けの設定指針。既定値（悲観側）を打ち消す宣言を、当てはまるときに明示せよ。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Where This Is Heading」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: idempotentHint についての指針はこの文に無い。

<a id="g-c01-mcp-official-30"></a>
#### C01-30 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#where-this-is-heading
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Where This Is Heading (#where-this-is-heading)
- **原文**:

> If you're writing a client, treat annotations from untrusted servers as informational and lean on them for UX, but keep your actual safety guarantees in deterministic controls.

- **日本語**: クライアントを書くなら、untrusted サーバの annotations は参考情報として扱い UX に使え。ただし実際の安全の保証は決定的な仕組み（deterministic controls）に置け。
- **どう使っているか**: クライアント作者向け：untrusted 由来は表示・UX 用、安全は別の決定的な制御で。
- **条件**: untrusted サーバ由来のとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > Where This Is Heading」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）

<a id="g-c01-mcp-official-31"></a>
#### C01-31 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#how-we-got-here
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > How We Got Here (#how-we-got-here)
- **原文**:

> I think the information itself, if it could be trusted, would be very useful, but I wonder how a client makes use of this flag knowing that it's not trustable.

- **日本語**: 情報そのものは、信頼できるならとても有用だと思う。だが信頼できないと分かっているこのフラグを、クライアントがどう使うのかが疑問だ。
- **どう使っているか**: annotations 導入時（PR #185 のレビュー）の論点：信頼できないヒントをクライアントはどう使うのか。仕様は『全部 hint と呼び、既定で untrusted 扱い、重みづけはクライアントに任せる』という妥協に落ち着いた、とブログは書く。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > How We Got Here」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: MCP 共同作者 Justin Spahr-Summers のレビューコメントをブログが引用したもの。元の PR コメント（github.com/.../pull/185#discussion_r2010043988）は github.com が遮断されていて直接は確認できない（ブログ上の引用として確認）。

<a id="g-c01-mcp-official-32"></a>
#### C01-32 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#whats-open-now
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What's Open Now (#whats-open-now)
- **原文**:

> Five SEPs currently propose new annotations or closely related capabilities:

- **日本語**: 現在、5 つの SEP が新しい annotations か、それに近い機能を提案している：
- **どう使っているか**: 拡張提案の一覧（2026-03 時点）。#1913 Trust and Sensitivity Annotations（Draft）、#1984 Comprehensive Tool Annotations（Draft）、#1561 unsafeOutputHint、#1560 secretHint、#1487 trustedHint（いずれも Proposal）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What's Open Now」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 表の中身は Markdown 原稿で目視。#1487/#1560/#1561 は issue で、github.com 遮断と GitHub MCP の権限（s1300105/auth_gap のみ）のため本文は未確認（unreachable 参照）。

<a id="g-c01-mcp-official-33"></a>
#### C01-33 Model Context Protocol project (blog; authors Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)) — MCP official blog

- **資料**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do (MCP blog, 2026-03-16)（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- **書いてある見出しへ直接**: https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/#what-tool-annotations-are
- **版**: 2026-03-16
- **書いてある場所**: Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are (#what-tool-annotations-are)
- **原文**:

> The first three hints mostly answer a preflight question: should the client ask for confirmation before calling this tool?

- **日本語**: 最初の 3 つのヒント（readOnly / destructive / idempotent）は、おもに事前の問い、つまり『このツールを呼ぶ前に確認を求めるべきか』に答えるものだ。
- **どう使っているか**: readOnly/destructive/idempotent の主目的を『呼ぶ前の確認の要否』と位置づける。openWorldHint は呼んだ後（出力の信頼性）にも関わる、と続く。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do > What Tool Annotations Are」（取得 2026-10-02T22:12:43Z、sha256 82888044d831…）
- **補足**: 続く文で openWorldHint について『The safest posture is to treat anything a tool considers external as a potential source of untrusted content.』とある（目視）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Tool Annotations Interest Group

<a id="g-c01-mcp-official-34"></a>
#### C01-34 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Tool Annotations Interest Group

- **資料**: Tool Annotations Charter (Interest Group)（公式の文書）
- **URL**: https://modelcontextprotocol.io/community/interest-groups/tool-annotations
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/community/interest-groups/tool-annotations#in-scope
- **版**: charter 2026-04-20
- **書いてある場所**: Tool Annotations Charter > Scope > In Scope (#in-scope)
- **原文**:

> Assess whether the current set of tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) adequately serves server and client authors

- **日本語**: 今の tool annotations（readOnlyHint, destructiveHint, idempotentHint, openWorldHint）が、サーバ作者とクライアント作者の役に十分立っているかを評価する
- **どう使っているか**: 公式の Interest Group が既存 4 ヒントの十分さを評価対象にしている（拘束力のある仕様変更はしない、と範囲外に明記）。
- **条件**: IG は勧告のみ（Binding specification changes は Out of Scope）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations Charter > Scope > In Scope」（取得 2026-10-02T22:11:31Z、sha256 0c808a777f36…）
- **補足**: ファシリテータは GitHub（Sam Morrow）と OpenAI（Robert Reichel）。メンバーに Cloudflare, Microsoft, GitHub など。旧 URL /community/tool-annotations/charter は 308 でここへ転送。

<a id="g-c01-mcp-official-35"></a>
#### C01-35 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Tool Annotations Interest Group

- **資料**: Tool Annotations Charter — Open Questions（公式の文書）
- **URL**: https://modelcontextprotocol.io/community/interest-groups/tool-annotations#open-questions
- **照らし合わせた中身の URL**: https://modelcontextprotocol.io/community/interest-groups/tool-annotations
- **版**: charter 2026-04-20
- **書いてある場所**: Tool Annotations Charter > Discussion Topics > Open Questions (#open-questions)
- **原文**:

> How should annotations interact with trust, security, and human-in-the-loop requirements?

- **日本語**: annotations は、信頼・セキュリティ・人間の確認（human-in-the-loop）の要件とどう関わるべきか？
- **どう使っているか**: annotations と確認・信頼の関係は、公式 IG でも未解決の問いとして挙げられている。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations Charter > Discussion Topics > Open Questions」（取得 2026-10-02T22:11:31Z、sha256 0c808a777f36…）
- **補足**: 同じ節に『Should runtime annotations ... be added』『Should tool response annotations be added』もある（目視）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (docs)

<a id="g-c01-mcp-official-36"></a>
#### C01-36 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (docs)

- **資料**: MCP Inspector — Web client (docs 2026-07-28)（公式の文書）
- **URL**: https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/web
- **書いてある見出しへ直接**: https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/web#tools
- **版**: docs 2026-07-28
- **書いてある場所**: Web client > Tools (#tools)
- **原文**:

> Select a tool to see its description, its input schema rendered as a form, and its annotations.

- **日本語**: ツールを選ぶと、その説明、フォームとして描かれた入力スキーマ、そして annotations が見られる。
- **どう使っているか**: 公式の開発者ツール Inspector（Web client）のドキュメント：ツールを選ぶと annotations が表示される。このページは表示に触れるだけで、承認・確認・絞り込みについては何も書いていない（使わないことはページではなくコード #37 で確認）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Web client > Tools」（取得 2026-10-02T22:11:58Z、sha256 2aa8b63872dd…）
- **補足**: verify_quote.py は直前の見出しを Server Settings（#server-settings）と報告するが、HTML を目視すると文は h2 id="tools" の直後にある（ツールが見出しの文字を拾えていない）。/docs/tools/inspector/web はこの版付き URL へ 307 で転送（検証者も確認）。ページ自体には『v2』の語が無い。v2 とするのは repo main（package.json version 2.9.0、clients/web）との対応による推定。 usage_ja の『（表示のみ。承認・絞り込みには使わない）』はこのページには書かれていない（コードからの推論）ので、出典を分けて書き直し。location / anchored_url を #tools に修正（HTML で見出しの位置を確認）。product の『v2』はページに記載なしと明記。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (web client, main)

<a id="g-c01-mcp-official-37"></a>
#### C01-37 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v2 (web client, main)

- **資料**: clients/web/src/components/groups/ToolDetailPanel/ToolDetailPanel.tsx（クライアントのソースコード）
- **URL**: https://github.com/modelcontextprotocol/inspector/blob/ae865a19178ddf6f375780a02e9c77c4cf4da184/clients/web/src/components/groups/ToolDetailPanel/ToolDetailPanel.tsx#L200-L208
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/inspector/ae865a19178ddf6f375780a02e9c77c4cf4da184/clients/web/src/components/groups/ToolDetailPanel/ToolDetailPanel.tsx
- **版**: main @ ae865a1 (2026-09-30)
- **書いてある場所**: lines 200
- **原文**:

> function hasAnyAnnotation(annotations?: ToolAnnotations): boolean {

- **日本語**: annotations のどれかが（true として）立っているかを調べる関数
- **どう使っているか**: v2 Inspector はツール詳細の見出しに、値が truthy なヒントだけをバッジ（read-only / destructive / idempotent / open-world）で出す（L310-323）。annotations が無い・false のヒントはバッジが出ない。つまり仕様の既定値（destructive=true, openWorld=true）は表示に反映されない。
- **条件**: 明示的に true のヒントだけ表示。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、200 行（取得 2026-10-02T22:11:43Z、sha256 7ace317adeee…）
- **補足**: L315『{annotations.destructiveHint && (』も検証済み（exact, L315）。ラベルと色は clients/web/src/components/elements/AnnotationBadge/AnnotationBadge.tsx（readOnlyHint→緑、destructiveHint→赤 など、目視）。現行コードでは承認・確認ダイアログに使っていない（repo 全体を git grep：readOnlyHint / destructiveHint は AnnotationBadge と ToolDetailPanel のバッジ表示、fixtures / stories / docs / specification（設計文書）以外に出現なし。core/ にも出現なし）。ただし docs/inspector-roadmap-2026-h2.md（Status: Draft for WG review, revised 2026-09-17）L254 に『**Annotation-driven confirmation** before a `destructiveHint` call』（Confidence 🟢）が計画として載っている（verify_quote.py exact, L254, 見出し ### 3.4 Improved primitives）。計画であり未実装。v1 Inspector（tag 1.0.2）は既定値を『implied default』として表示していたので、v2 で既定値の表示が消えた（目視比較、#38）。 notes の grep 対象『clients/core』は存在しないパス（実際は repo 直下の core/ と clients/{cli,tui,web}）。検証者が repo 全体を grep し直し、表示以外の使用が無いことを確認。Inspector ロードマップ草案に destructiveHint 前の確認が計画として載っていることを追記（現行の『表示のみ』は正しいが、将来の計画がある）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v1 (1.0.2)

<a id="g-c01-mcp-official-38"></a>
#### C01-38 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — MCP Inspector v1 (1.0.2)

- **資料**: client/src/components/ToolsTab.tsx — AnnotationBadges（クライアントのソースコード）
- **URL**: https://github.com/modelcontextprotocol/inspector/blob/85abfd4a2840906cbd510c97e1facc50e9100099/client/src/components/ToolsTab.tsx#L96-L165
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/inspector/85abfd4a2840906cbd510c97e1facc50e9100099/client/src/components/ToolsTab.tsx
- **版**: tag 1.0.2 @ 85abfd4
- **書いてある場所**: lines 103
- **原文**:

> // Spec defaults: readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=true

- **日本語**: // 仕様の既定値：readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=true
- **どう使っているか**: v1 Inspector は 4 つのヒントを常に表示し、省略されたものは仕様の既定値で埋め、『implied default』として点線・半透明で、明示値は『explicitly set』として区別して表示していた（L103-157）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、103 行（取得 2026-10-02T22:11:35Z、sha256 07b2209df0d6…）
- **補足**: L113『const destructive = getValueAndImplied(annotations?.destructiveHint, true);』も検証済み（exact）。ツールチップ文言 L152（目視）。0.22.0 も同じコード（git grep）。表示のみで、呼び出しの確認・ブロックには使っていない（ToolsTab に confirm の語なし、目視）。

### Model Context Protocol project (reference servers) — Reference server: filesystem (TypeScript)

<a id="g-c01-mcp-official-39"></a>
#### C01-39 Model Context Protocol project (reference servers) — Reference server: filesystem (TypeScript)

- **資料**: src/filesystem/index.ts — write_file tool（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/filesystem/index.ts#L358-L373
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/filesystem/index.ts
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 371
- **原文**:

> annotations: { readOnlyHint: false, idempotentHint: true, destructiveHint: true, openWorldHint: false }

- **日本語**: write_file：読み取り専用でない、冪等、破壊的、閉じた世界
- **どう使っているか**: 公式参照サーバの設定例。読み取り系 10 ツール（read_file〔Deprecated〕, read_text_file, read_media_file, read_multiple_files, list_directory, list_directory_with_sizes, directory_tree, search_files, get_file_info, list_allowed_directories）は { readOnlyHint: true, openWorldHint: false }（L221 ほか）、create_directory は destructive:false / idempotent:true、edit_file・move_file は destructive:true / idempotent:false、write_file は destructive:true / idempotent:true。全ツール openWorldHint:false。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、371 行（取得 2026-10-02T22:11:36Z、sha256 bff21de612c5…）
- **補足**: 読み取り系は destructiveHint / idempotentHint を書かない（readOnlyHint:true のとき意味が無いため）。このページの quote は write_file の L371。 『読み取り系 9 ツール』を 10 に修正：コードでは read_file（title『Read File (Deprecated)』, L214-221）も readOnlyHint:true で登録されている。README の表（#40）は read_file を除く 9 行。

### Model Context Protocol project (reference servers) — Reference server: filesystem (README)

<a id="g-c01-mcp-official-40"></a>
#### C01-40 Model Context Protocol project (reference servers) — Reference server: filesystem (README)

- **資料**: src/filesystem/README.md — Tool annotations (MCP hints)（サーバの文書）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/filesystem/README.md#L182-L210
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/filesystem/README.md
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 189 / ### Tool annotations (MCP hints)
- **原文**:

> Highlight operations that may be **destructive** (overwriting or heavily mutating data).

- **日本語**: 破壊的かもしれない操作（上書き・大きな変更）を目立たせる（ことができるように annotations を付けている）。
- **どう使っているか**: 参照サーバ README が annotations を付ける目的を説明：read-only と書き込み可能を区別、再試行してよい書き込みを示す、破壊的操作を強調、外部世界に届かないことを示す。ツールごとの対応表あり。
- **扱う宣言**: readOnlyHint・idempotentHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、189 行（### Tool annotations (MCP hints)）（取得 2026-10-02T22:11:33Z、sha256 df276d57efc0…）
- **補足**: L210（検証済み）：『Every tool also sets `openWorldHint: false` — this server only accesses the local filesystem within its allowed directories, never an open or external world.』。README の表では create_directory の Notes に『Re‑creating the same dir is a no‑op』とある（目視）。

### Model Context Protocol project (reference servers) — Reference server: git (Python)

<a id="g-c01-mcp-official-41"></a>
#### C01-41 Model Context Protocol project (reference servers) — Reference server: git (Python)

- **資料**: src/git/src/mcp_server_git/server.py — list_tools()（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/git/src/mcp_server_git/server.py#L373-L383
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/git/src/mcp_server_git/server.py
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 374-381
- **原文**:

> name=GitTools.RESET, description="Unstages all staged changes", inputSchema=GitReset.model_json_schema(), annotations=ToolAnnotations( readOnlyHint=False, destructiveHint=True, idempotentHint=True, openWorldHint=False,

- **日本語**: git_reset（ステージした変更をすべて外す）：読み取り専用でない、破壊的、冪等、閉じた世界
- **どう使っているか**: Python 低レベル API（mcp.types.ToolAnnotations）で 4 ヒントをすべて明示する例。status/diff/log/show 等は readOnlyHint=True・destructiveHint=False・idempotentHint=True、commit/add/create_branch/checkout は readOnly=False・destructive=False、reset は destructive=True。全ツール openWorldHint=False。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、374-381 行（# Default number of context lines to show in diff output）（取得 2026-10-02T22:11:39Z、sha256 027d1158d3df…）
- **補足**: git_status（L308-315）も検証済み。git_checkout は destructiveHint=False（L410-414、目視）。作業木の未コミット変更を失いうるかは本調査の範囲外（判断しない）。

### Model Context Protocol project (reference servers) — Reference server: memory (TypeScript)

<a id="g-c01-mcp-official-42"></a>
#### C01-42 Model Context Protocol project (reference servers) — Reference server: memory (TypeScript)

- **資料**: src/memory/index.ts — delete_entities / delete_observations / delete_relations（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/memory/index.ts#L496-L513
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/memory/index.ts
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 507-512; lines 543-548; lines 578-583
- **原文**:

> annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true, openWorldHint: false, }

- **日本語**: 削除系：読み取り専用でない、破壊的、冪等、閉じた世界
- **どう使っているか**: このブロックは 3 か所（L507-512 delete_entities, L543-548 delete_observations, L578-583 delete_relations）。create_entities / create_relations / add_observations は destructive:false / idempotent:false、read_graph / search_nodes / open_nodes は readOnlyHint:true・destructive:false・idempotent:true。全ツール openWorldHint:false（仕様の例『memory tool は閉じた世界』と一致）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・3 か所、507-512 行（取得 2026-10-02T22:12:59Z、sha256 fa1d38913ecd…）
- **補足**: count=3。学生向け url は delete_entities（L496-513）。 usage_ja の『create_*』に add_observations（同じ値）を追加し、読み取り系の値を明記（コードで確認）。

### Model Context Protocol project (reference servers) — Reference server: time (Python)

<a id="g-c01-mcp-official-43"></a>
#### C01-43 Model Context Protocol project (reference servers) — Reference server: time (Python)

- **資料**: src/time/src/mcp_server_time/server.py — get_current_time / convert_time（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/time/src/mcp_server_time/server.py#L145-L150
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/time/src/mcp_server_time/server.py
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 145-150; lines 173-178
- **原文**:

> annotations=ToolAnnotations( readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False, ),

- **日本語**: 読み取り専用、破壊的でない、冪等、閉じた世界
- **どう使っているか**: 2 ツールとも同じ 4 値を明示（L173-178 も同じ、目視）。readOnlyHint=True でも destructive/idempotent を書いている。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・2 か所、145-150 行（取得 2026-10-02T22:11:36Z、sha256 629500285347…）
- **補足**: count=2（L145-150 get_current_time、L173-178 convert_time）。

### Model Context Protocol project (reference servers) — Reference server: sequentialthinking (TypeScript)

<a id="g-c01-mcp-official-44"></a>
#### C01-44 Model Context Protocol project (reference servers) — Reference server: sequentialthinking (TypeScript)

- **資料**: src/sequentialthinking/index.ts — sequentialthinking tool（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/sequentialthinking/index.ts#L95-L100
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/sequentialthinking/index.ts
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 95-100
- **原文**:

> annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false, },

- **日本語**: 読み取り専用、破壊的でない、冪等、閉じた世界
- **どう使っているか**: 思考の記録をサーバ内メモリに積むツールだが readOnlyHint: true, idempotentHint: true と宣言している。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、95-100 行（取得 2026-10-02T22:11:35Z、sha256 fab7b6e9817d…）
- **補足**: このツールは呼び出しごとにサーバ内の思考履歴へ追記する（lib.ts L60 の thoughtHistory.push、目視）ので、『環境を変更しない』『同じ引数で繰り返しても追加の効果なし』と言えるかは解釈による（不明。本調査では判定しない）。

### Model Context Protocol project (reference servers) — Reference server: everything (TypeScript)

<a id="g-c01-mcp-official-45"></a>
#### C01-45 Model Context Protocol project (reference servers) — Reference server: everything (TypeScript)

- **資料**: src/everything/docs/structure.md（サーバの文書）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/everything/docs/structure.md#L146
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/everything/docs/structure.md
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 146 / ### `tools/`
- **原文**:

> All tools in this server include tool-level annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`).

- **日本語**: このサーバのすべてのツールが、ツール単位の annotations（readOnlyHint, destructiveHint, idempotentHint, openWorldHint）を持つ。
- **どう使っているか**: テスト用の全機能サーバ。全ツールに 4 ヒントを付けている。例：echo / get-env は readOnly:true・openWorld:false、gzip-file-as-resource は readOnly:false・destructive:false・idempotent:true・openWorld:true（L50-55 検証済み）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、146 行（### `tools/`）（取得 2026-10-02T22:11:37Z、sha256 b1d90bc117d4…）
- **補足**: get-env（環境変数を返す）も readOnlyHint:true, openWorldHint:false（目視）。

### Model Context Protocol project (reference servers) — modelcontextprotocol/servers repo (agent instructions)

<a id="g-c01-mcp-official-46"></a>
#### C01-46 Model Context Protocol project (reference servers) — modelcontextprotocol/servers repo (agent instructions)

- **資料**: CLAUDE.md — Key Patterns（サーバの文書）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/CLAUDE.md#L102
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/CLAUDE.md
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 102 / ## Key Patterns
- **原文**:

> Tool annotations: set `readOnlyHint`, `idempotentHint`, `destructiveHint` per MCP spec

- **日本語**: ツールの annotations：MCP 仕様に従って readOnlyHint, idempotentHint, destructiveHint を設定する
- **どう使っているか**: 参照サーバ repo の貢献者（AI エージェント含む）向け規約：annotations を設定することがパターンとして求められている。openWorldHint はこの行に無い。
- **扱う宣言**: readOnlyHint・idempotentHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、102 行（## Key Patterns）（取得 2026-10-02T22:11:43Z、sha256 2e9238c6f126…）
- **補足**: 必須（MUST）とまでは書いていない。

### Model Context Protocol project (reference servers) — Reference server: fetch (Python)

<a id="g-c01-mcp-official-47"></a>
#### C01-47 Model Context Protocol project (reference servers) — Reference server: fetch (Python)

- **資料**: src/fetch/src/mcp_server_fetch/server.py — list_tools()（サーバのソースコード）
- **URL**: https://github.com/modelcontextprotocol/servers/blob/f46d9578190b476b3501923ea8977d899e8db2cb/src/fetch/src/mcp_server_fetch/server.py#L196-L206
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/servers/f46d9578190b476b3501923ea8977d899e8db2cb/src/fetch/src/mcp_server_fetch/server.py
- **版**: main @ f46d957 (2026-09-22)
- **書いてある場所**: lines 200-202
- **原文**:

> Tool( name="fetch", description="""Fetches a URL from the internet and optionally extracts its contents as markdown.

- **日本語**: fetch ツールの定義（インターネットから URL を取得する）。annotations の指定が無い。
- **どう使っているか**: 参照サーバ 7 つのうち fetch だけ annotations が無い（ファイル全体で annotations / readOnlyHint / openWorldHint が出現しない、checked_no_mention 参照）。よって仕様の既定値（readOnly=false, destructive=true, idempotent=false, openWorld=true）がそのまま適用される。
- **扱う宣言**:  ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、200-202 行（取得 2026-10-02T22:12:05Z、sha256 f66dc973126c…）
- **補足**: Tool(...) は name / description / inputSchema だけ（L200-205、目視）。openWorldHint の典型例（Web 取得）なのに宣言が無く、既定値 openWorld=true と結果的に一致、destructive=true（既定）は実際より悲観的。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1862

<a id="g-c01-mcp-official-48"></a>
#### C01-48 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1862

- **資料**: SEP-1862: Tool Resolution（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/c934643b241eccf380aba21b8c264a89c6341cbe/seps/1862-tool-resolution.md#L10-L12
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/c934643b241eccf380aba21b8c264a89c6341cbe/seps/1862-tool-resolution.md
- **版**: PR #1862 head c934643 (fetched via git pull/1862/head)
- **書いてある場所**: lines 12 / ## Abstract
- **原文**:

> Today, a file management tool must declare `destructiveHint: true` even though most calls are safe reads—causing users to click through warnings they learn to ignore.

- **日本語**: 今は、ファイル管理ツールはほとんどの呼び出しが安全な読み取りでも destructiveHint: true を宣言しなければならず、利用者は無視するようになった警告をクリックで通過させている。
- **どう使っているか**: 静的な destructiveHint:true がクライアントの確認ダイアログを引き起こしている（確認疲れ）という前提で、引数ごとに annotations を返す tools/resolve を提案。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、12 行（## Abstract）（取得 2026-10-02T22:11:37Z、sha256 483c502a0f8a…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。 同 SEP L23：resolve に失敗したら静的な（最悪ケースの）annotations に戻る。L637 以降の Trust Model で『Marking destructive operations as read-only』を悪意あるサーバの例に挙げる（目視）。IG の sep-disposition は『core に残す』としていた。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

<a id="g-c01-mcp-official-49"></a>
#### C01-49 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1862

- **資料**: SEP-1862: Tool Resolution — Tool Definition Extension（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/c934643b241eccf380aba21b8c264a89c6341cbe/seps/1862-tool-resolution.md#L174
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/c934643b241eccf380aba21b8c264a89c6341cbe/seps/1862-tool-resolution.md
- **版**: PR #1862 head c934643 (fetched via git pull/1862/head)
- **書いてある場所**: lines 174 / ### Tool Definition Extension
- **原文**:

> When `resolve: true`, the `annotations` field **SHOULD** represent the worst-case (most conservative) behavior across all possible arguments, providing a safe default when resolution is not supported or desired by the client.

- **日本語**: resolve: true のとき、annotations は、あり得るすべての引数での最悪（最も保守的な）振る舞いを表すべきである（SHOULD）。解決を使わないクライアントにとって安全な既定値になる。
- **どう使っているか**: 静的 annotations は引数の最悪ケースで宣言せよ、という作者向け指針（提案）。
- **扱う宣言**: 宣言全般・destructiveHint・readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、174 行（### Tool Definition Extension）（取得 2026-10-02T22:11:37Z、sha256 483c502a0f8a…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。 AuthGap の宣言照合（静的宣言 vs 全経路の効果）と同じ『最悪ケース』の読み方を、提案側が明文化している。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1913

<a id="g-c01-mcp-official-50"></a>
#### C01-50 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1913

- **資料**: SEP-1913: Trust and Sensitivity Annotations — Propagation Rules（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/f46d45ef8eb60ff3fb2f38651bd076097f9ccdf4/seps/1913-trust-and-sensitivity-annotations.md#L687-L692
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/f46d45ef8eb60ff3fb2f38651bd076097f9ccdf4/seps/1913-trust-and-sensitivity-annotations.md
- **版**: PR #1913 head f46d45e (fetched via git pull/1913/head)
- **書いてある場所**: lines 691 / #### Propagation Rules
- **原文**:

> **Boolean union**: If `openWorldHint` is ever true, it **MUST** persist for the session

- **日本語**: 論理和：openWorldHint が一度でも true になったら、そのセッションの間ずっと保持されなければならない（MUST）。
- **どう使っているか**: openWorldHint を結果・セッション単位の『汚染』印として伝播させる提案（tool 定義の静的な意味を拡張）。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、691 行（#### Propagation Rules）（取得 2026-10-02T22:11:33Z、sha256 c61a729cd07d…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：open。 同 SEP L187-199：openWorldHint は tool 静的／resolve 後／応答の 3 層で意味を持つとし、Web ページ・メール本文・GitHub issue 等を untrusted source の例に挙げる（目視）。共著者は GitHub と OpenAI。実験リポジトリ（trust-annotations 草案）では result 側の印を別名 untrusted に分けた。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

<a id="g-c01-mcp-official-51"></a>
#### C01-51 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1913

- **資料**: SEP-1913: Trust and Sensitivity Annotations — Motivation（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/f46d45ef8eb60ff3fb2f38651bd076097f9ccdf4/seps/1913-trust-and-sensitivity-annotations.md#L64-L66
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/f46d45ef8eb60ff3fb2f38651bd076097f9ccdf4/seps/1913-trust-and-sensitivity-annotations.md
- **版**: PR #1913 head f46d45e (fetched via git pull/1913/head)
- **書いてある場所**: lines 66 / ### The Problem with Undeclared Tool Actions
- **原文**:

> A tool that reads drafts and a tool that sends emails are indistinguishable (other than the most basic static Annotations), even though their security and privacy implications are radically different. Implementations fall back to heuristics or model inference to decide when to request user consent or block operations.

- **日本語**: 下書きを読むツールとメールを送るツールは（最も基本的な静的 annotations を除けば）区別できない。セキュリティとプライバシーへの影響はまるで違うのに。実装は、いつ利用者の同意を求めるか・操作を止めるかを、経験則やモデルの推論で決めている。
- **どう使っているか**: 現行 annotations だけでは同意要求・ブロックの判断に足りず、実装は経験則に頼っている、という現状認識。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、66 行（### The Problem with Undeclared Tool Actions）（取得 2026-10-02T22:11:33Z、sha256 c61a729cd07d…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：open。  doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1984

<a id="g-c01-mcp-official-52"></a>
#### C01-52 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1984

- **資料**: SEP-1984: Comprehensive Tool Annotations — Guidance for Clients（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/973bfe21828af55ce7017d0d1b5cf9a84f2d3e4e/seps/1984-comprehensive-tool-annotations.md#L217-L223
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/973bfe21828af55ce7017d0d1b5cf9a84f2d3e4e/seps/1984-comprehensive-tool-annotations.md
- **版**: PR #1984 head 973bfe2 (fetched via git pull/1984/head)
- **書いてある場所**: lines 220 / ### Guidance for Clients
- **原文**:

> Assume that a missing hint implies anything other than "no explicit claim"

- **日本語**: （してはならないこと）ヒントが無いことを『明示的な主張が無い』以外の意味だと仮定すること
- **どう使っているか**: 新ヒント（既定値 undefined）の欠落は『主張なし』として扱い、保守的に扱え、という提案。既存 4 ヒントの『悲観的既定値』とは別の扱い方。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、220 行（### Guidance for Clients）（取得 2026-10-02T22:11:35Z、sha256 959bdfb17323…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。 同じ箇条に『Make security-critical decisions based solely on these annotations』『Trust annotations from untrusted servers without independent verification』も禁止事項として並ぶ。直後：『In the absence of these hints, clients should fall back to their default behaviors and treat tools conservatively.』（目視）。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

<a id="g-c01-mcp-official-53"></a>
#### C01-53 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1984

- **資料**: SEP-1984: Comprehensive Tool Annotations — combining hints（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/973bfe21828af55ce7017d0d1b5cf9a84f2d3e4e/seps/1984-comprehensive-tool-annotations.md#L211-L215
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/973bfe21828af55ce7017d0d1b5cf9a84f2d3e4e/seps/1984-comprehensive-tool-annotations.md
- **版**: PR #1984 head 973bfe2 (fetched via git pull/1984/head)
- **書いてある場所**: lines 215 / ### Guidance for Clients
- **原文**:

> `reversibleHint: true` + `destructiveHint: false` → Lower risk, lighter confirmation flow

- **日本語**: reversibleHint: true と destructiveHint: false の組み合わせ → 低リスク、軽い確認フロー
- **どう使っているか**: ヒントの組み合わせでリスクを段階づけ、確認の強さを変える使い方の提案。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 危険度を付ける・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、215 行（### Guidance for Clients）（取得 2026-10-02T22:11:35Z、sha256 959bdfb17323…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。  doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2793

<a id="g-c01-mcp-official-54"></a>
#### C01-54 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2793

- **資料**: SEP-2793: Tool Risk Metadata — Default behaviour（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/49f25cf77e4ae087049e8c3871a1f42628cc7362/seps/2793-tool-risk-metadata.md#L141-L146
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/49f25cf77e4ae087049e8c3871a1f42628cc7362/seps/2793-tool-risk-metadata.md
- **版**: PR #2793 head 49f25cf (fetched via git pull/2793/head)
- **書いてある場所**: lines 143-146 / ### Default behaviour
- **原文**:

> When a client implements risk-aware policy and a tool is missing risk metadata, the client SHOULD default to its most-restrictive policy bucket (e.g. `riskLevel="critical"`, `approvalRecommendation="multi"`) until an operator explicitly classifies that tool.

- **日本語**: クライアントがリスクに応じた方針を実装していて、ツールにリスク情報が無いとき、運用者が明示的に分類するまで、最も厳しい方針の区分（例：riskLevel=critical、approvalRecommendation=multi）を既定にすべきである（SHOULD）。
- **どう使っているか**: ToolAnnotations に段階的リスク（riskLevel, approvalRecommendation など）を足す提案。欠落時は fail-closed。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・危険度を付ける・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、143-146 行（### Default behaviour）（取得 2026-10-02T22:11:35Z、sha256 a497452f5b2b…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：open。 同 SEP L149-158：宣言が無ければ名前・説明・入力スキーマから動詞ヒューリスティックで推論（get/list→read、delete/drop→delete 等）するリファレンス推論器を挙げる（目視）。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

<a id="g-c01-mcp-official-55"></a>
#### C01-55 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2793

- **資料**: SEP-2793: Tool Risk Metadata — Motivation（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/49f25cf77e4ae087049e8c3871a1f42628cc7362/seps/2793-tool-risk-metadata.md#L61-L63
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/49f25cf77e4ae087049e8c3871a1f42628cc7362/seps/2793-tool-risk-metadata.md
- **版**: PR #2793 head 49f25cf (fetched via git pull/2793/head)
- **書いてある場所**: lines 61-63 / ## Motivation
- **原文**:

> `destructiveHint` *almost* fills this gap but is binary: a tool that deletes one row and a tool that drops a whole namespace get the same flag.

- **日本語**: destructiveHint はこの穴を『ほぼ』埋めるが二値である。1 行を消すツールと名前空間ごと消すツールが同じ印になる。
- **どう使っているか**: 二値の destructiveHint では承認方針の段階づけに足りない、という問題提起。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、61-63 行（## Motivation）（取得 2026-10-02T22:11:35Z、sha256 a497452f5b2b…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：open。 Motivation で Claude Desktop, Cursor, Cline 等が独自の allowlist を持つと書くが、出典は示されていない（未検証の主張）。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1938

<a id="g-c01-mcp-official-56"></a>
#### C01-56 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-1938

- **資料**: SEP-1938: Add agencyHint tool annotation（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/32c763bce58cdaa0fb2e341783b0d836ca23c0de/seps/1938-agency-hint-tool-annotation.md#L15-L17
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/32c763bce58cdaa0fb2e341783b0d836ca23c0de/seps/1938-agency-hint-tool-annotation.md
- **版**: PR #1938 head 32c763b (fetched via git pull/1938/head)
- **書いてある場所**: lines 17 / ## Abstract
- **原文**:

> This hint lets clients differentiate agent-like tools from simple procedural ones, enabling better UX patterns (e.g., confirmation flows, progress UI, or monitoring) without changing the underlying protocol semantics.

- **日本語**: このヒントでクライアントは、エージェント的なツールと単純な手続き的ツールを区別でき、確認フロー・進捗 UI・監視などの UX を改善できる。
- **どう使っているか**: 新ヒント agencyHint の想定用途：確認フロー・進捗表示・監視。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、17 行（## Abstract）（取得 2026-10-02T22:12:59Z、sha256 16fd2e88f7e5…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。  doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2061

<a id="g-c01-mcp-official-57"></a>
#### C01-57 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-2061

- **資料**: SEP-2061: Action Security Metadata for MCP Tools — Abstract（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/0df4cb0f2788d484dcbfc9221fe99bdf815fc35b/seps/2061-action-security-metadat-for-tools.md#L12-L14
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/0df4cb0f2788d484dcbfc9221fe99bdf815fc35b/seps/2061-action-security-metadat-for-tools.md
- **版**: PR #2061 head 0df4cb0 (fetched via git pull/2061/head)
- **書いてある場所**: lines 14 / ## Abstract
- **原文**:

> Today, MCP provides limited means to distinguish between read-only tools and tools that send messages, modify data, or publish information externally. As a result, platforms rely on heuristics or model-based inference to determine when a tool invocation is sensitive or requires user consent.

- **日本語**: 今の MCP では、読み取り専用ツールと、メッセージ送信・データ変更・外部公開をするツールを区別する手段が限られている。そのためプラットフォームは、呼び出しが機微か・同意が要るかを経験則やモデルの推論で決めている。
- **どう使っているか**: 既存ヒントでは同意要求の判断に足りないという現状認識。入力の行き先・出力の出所・結果を宣言する Action Security Contract を提案。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、14 行（## Abstract）（取得 2026-10-02T22:11:33Z、sha256 227bac4393a9…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。 実験リポジトリ docs/sep-disposition.md L74（検証済み）：『closed 2026-06-13』で action-metadata 拡張に移行。著者は OpenAI の Robert Reichel。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-3140

<a id="g-c01-mcp-official-58"></a>
#### C01-58 Model Context Protocol project (modelcontextprotocol, Agentic AI Foundation) — SEP (proposal, not part of the spec) — SEP-3140

- **資料**: SEP-3140: Signed Capability Declarations & Trustworthy Trust Labels（issue / PR / 提案の下書き）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/b5d9a57f8e8c1e93ec84616da1afec3373dffbc6/seps/3140-MCP-Signed-Capability-Declarations-and-Trust-Labels.md#L53
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/b5d9a57f8e8c1e93ec84616da1afec3373dffbc6/seps/3140-MCP-Signed-Capability-Declarations-and-Trust-Labels.md
- **版**: PR #3140 head b5d9a57 (fetched via git pull/3140/head)
- **書いてある場所**: lines 53 / ### Why this belongs in the protocol, not the implementer
- **原文**:

> **Free-form `annotations` cannot back a security decision.** They are attacker-controlled and explicitly untrusted, so a host cannot use them to gate anything (reliance on them is [CWE-807](https://cwe.mitre.org/data/definitions/807.html)).

- **日本語**: 自由記述の annotations はセキュリティ判断の根拠にできない。攻撃者が操作でき、明示的に untrusted とされているので、ホストはそれで何かを通す・止めることができない（それに頼るのは CWE-807）。
- **どう使っているか**: annotations を門番に使うこと自体を CWE-807（信頼できない入力に基づくセキュリティ判断）とみなし、署名つきの trust ブロックで置き換える（補う）提案。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、53 行（### Why this belongs in the protocol, not the implementer）（取得 2026-10-02T22:11:43Z、sha256 e3c009327e94…）
- **補足**: 提案文書であり仕様ではない。PR の状態（GitHub MCP の検索結果、未確認）：closed。 同 SEP L27：仕様の『trusted server』要件は検証手段が無く実行不能だと指摘。L224：annotations の変更は『material』（再承認が要る変更）扱い（目視）。 doc_type を spec → issue_or_pr に変更：SEP は未マージの提案（PR の head commit を取得。SEP 本文の Status は Draft、main の seps/ にも無い）で、仕様の一部ではない。PR の open/closed は github.com が 403 のため引き続き未確認（SEP-2061 の closed 2026-06-13 だけは IG repo の docs/sep-disposition.md L74 で確認）。

### Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations

<a id="g-c01-mcp-official-59"></a>
#### C01-59 Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations

- **資料**: docs/trust-model.md — Annotations are claims, not guarantees（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/experimental-ext-tool-annotations/blob/fecace78a9552f70ba735d750fc3c4b190e20429/docs/trust-model.md#L22-L26
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-tool-annotations/fecace78a9552f70ba735d750fc3c4b190e20429/docs/trust-model.md
- **版**: main @ fecace7
- **書いてある場所**: lines 24-26 / ## Annotations are claims, not guarantees
- **原文**:

> A server that lies in its annotations is a server a registry can refuse to list and a host can refuse to trust — the same accountability model as any other declared capability.

- **日本語**: annotations で嘘をつくサーバは、レジストリが掲載を拒み、ホストが信頼を拒めるサーバである。ほかの宣言された機能と同じ説明責任のモデルだ。
- **どう使っているか**: annotations は主張であって保証ではない。信頼は生態系（レジストリ・ホスト・運用者）が検証することから生まれる、という IG の立場。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、24-26 行（## Annotations are claims, not guarantees）（取得 2026-10-02T22:11:38Z、sha256 6cf7d9e21764…）
- **補足**: README は『They do not represent official MCP specifications or recommendations.』と明記（L7、実験的な草案）。同ファイルに『defense in depth, not a single gate』（目視）。公式 Registry の server.json の schema（2025-12-11 / draft）と Registry About ページには annotations の語が無い（checked_no_mention）。レジストリが annotations を検証する仕組みは、これらの資料には見当たらない（資料の範囲での不在）。 notes の『レジストリ側の検証は現時点で仕組みが無い』を、確認した資料の範囲での不在に弱めた（schema と About ページに語が無いことは、検証の仕組みが無いことの証明ではない）。 doc_type は official_docs のままだが非規範（README L7）。

### Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (trust-annotations draft)

<a id="g-c01-mcp-official-60"></a>
#### C01-60 Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (trust-annotations draft)

- **資料**: specification/draft/trust-annotations.mdx — Relationship to existing *Hint annotations（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/experimental-ext-tool-annotations/blob/fecace78a9552f70ba735d750fc3c4b190e20429/specification/draft/trust-annotations.mdx#L153-L170
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-tool-annotations/fecace78a9552f70ba735d750fc3c4b190e20429/specification/draft/trust-annotations.mdx
- **版**: main @ fecace7
- **書いてある場所**: lines 159-162 / ### Relationship to existing `*Hint` annotations
- **原文**:

> `openWorldHint` is a property of the **tool definition** — "this tool reaches an open, attacker-influenceable world" (e.g. a web fetch). It is known at registration time and does not vary per call.

- **日本語**: openWorldHint はツール定義の性質で、『このツールは攻撃者が影響しうる開いた世界に届く』（例：Web 取得）という意味である。登録時に決まり、呼び出しごとに変わらない。
- **どう使っているか**: openWorldHint（ツール定義・静的）と結果単位の untrusted 印を区別する解釈。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、159-161 行（### Relationship to existing `*Hint` annotations）（取得 2026-10-02T22:11:35Z、sha256 3cc0123157d3…）
- **補足**: 続けて『openWorldHint が false のツールでも保存領域から読んだ untrusted データを返しうる』とする（目視）。 doc_type は official_docs のままだが、この repo の README は『official MCP specifications or recommendations ではない』と明記（L7）。org 欄の non-normative と合わせて読むこと。

### Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (action-metadata draft)

<a id="g-c01-mcp-official-61"></a>
#### C01-61 Model Context Protocol project — Tool Annotations IG experimental repo (non-normative) — experimental-ext-tool-annotations (action-metadata draft)

- **資料**: specification/draft/action-metadata.mdx — Relationship to existing annotations（公式の文書）
- **URL**: https://github.com/modelcontextprotocol/experimental-ext-tool-annotations/blob/fecace78a9552f70ba735d750fc3c4b190e20429/specification/draft/action-metadata.mdx#L105-L111
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-tool-annotations/fecace78a9552f70ba735d750fc3c4b190e20429/specification/draft/action-metadata.mdx
- **版**: main @ fecace7
- **書いてある場所**: lines 110-111 / ## Relationship to existing annotations
- **原文**:

> The IG will need to decide whether action metadata *supersedes* or *coexists with* the legacy hints before any graduation.

- **日本語**: IG は、正式化の前に、action metadata が既存のヒントを置き換えるのか共存するのかを決める必要がある。
- **どう使っているか**: 既存 4 ヒントを『legacy hints』と呼び、置き換えか共存かを未決とする。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、110-111 行（## Relationship to existing annotations）（取得 2026-10-02T22:12:58Z、sha256 985a052969d9…）
- **補足**: 同ファイル L28-34：既存ヒントは粗く、実行系はツール名やモデルの振る舞いからリスクを推測している（目視）。 doc_type は official_docs のままだが、この repo の README は『official MCP specifications or recommendations ではない』と明記（L7）。org 欄の non-normative と合わせて読むこと。

---

[付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-2 SDK →](appendix-g-2.md)
