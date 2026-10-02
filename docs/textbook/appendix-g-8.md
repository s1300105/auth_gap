[← 付録 G-7 エディタとコーディングエージェント](appendix-g-7.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-9 サーバの作者と、業務 SaaS のホスト →](appendix-g-9.md)

---

# 付録 G-8 エージェントの枠組み・利用者向けアプリ・モデルの API

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-8-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C08-01](#g-c08-frameworks-01) | n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能） | クライアントのソースコード | 規則（ポリシー）の条件に使う・確認を省く（自動で許可）・確認を求める | [確認] |
| [C08-02](#g-c08-frameworks-02) | n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能） | クライアントのソースコード | 宣言が無いときの扱い・危険度を付ける | [確認] |
| [C08-03](#g-c08-frameworks-03) | n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能） | クライアントのソースコード | 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い | [確認] |
| [C08-04](#g-c08-frameworks-04) | n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能） | クライアントのソースコード | ツールを絞る・隠す・確認を求める | [確認] |
| [C08-05](#g-c08-frameworks-05) | Mastra — Mastra (@mastra/mcp MCPClient) | SDK のソースコード | 宣言が無いときの扱い・そのまま渡す・見せる・信頼するなという注意 | [確認] |
| [C08-06](#g-c08-frameworks-06) | Mastra — Mastra (@mastra/mcp MCPClient) | SDK のソースコード | 確認を求める・確認を省く（自動で許可）・宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [C08-07](#g-c08-frameworks-07) | Vercel — AI SDK (@ai-sdk/mcp, MCP client) | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C08-08](#g-c08-frameworks-08) | Hugging Face — Hugging Face MCP Server (huggingface/hf-mcp-server) | サーバのソースコード | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C08-09](#g-c08-frameworks-09) | Hugging Face — Hugging Face MCP Server (huggingface/hf-mcp-server) | サーバのソースコード | 使わない・読まない・宣言が無いときの扱い | [確認] |
| [C08-10](#g-c08-frameworks-10) | Agno — Agno AgentOS（エージェントを MCP サーバーとして公開） | SDK のソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C08-11](#g-c08-frameworks-11) | Agno — Agno AgentOS（エージェントを MCP サーバーとして公開） | SDK のソースコード | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C08-12](#g-c08-frameworks-12) | Agno — Agno MCPTools（MCP クライアント） | SDK のソースコード | 使わない・読まない・確認を求める | [確認] |
| [C08-13](#g-c08-frameworks-13) | Microsoft — AutoGen (autogen-ext McpWorkbench) | SDK のソースコード | 使わない・読まない | [確認] |
| [C08-14](#g-c08-frameworks-14) | Cloudflare — Cloudflare Agents SDK（agents パッケージの MCP クライアント） | SDK のソースコード | 表示（印・名前）・使わない・読まない | [確認] |
| [C08-15](#g-c08-frameworks-15) | Cloudflare — Cloudflare Agents SDK（実験的 WebMCP アダプタ） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C08-16](#g-c08-frameworks-16) | Cloudflare — Cloudflare Agents SDK（docs: McpClient API） | SDK の文書 | 表示（印・名前） | [確認] |
| [C08-17](#g-c08-frameworks-17) | Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway) | ゲートウェイの文書 | 作者への書き方の案内 | [確認] |
| [C08-18](#g-c08-frameworks-18) | Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway) | ゲートウェイのソースコード | そのまま渡す・見せる | [確認] |
| [C08-19](#g-c08-frameworks-19) | Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway) | ゲートウェイのソースコード | 使わない・読まない・そのまま渡す・見せる | [確認] |
| [C08-20](#g-c08-frameworks-20) | Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway) | ゲートウェイのソースコード | 使わない・読まない | [確認] |
| [C08-21](#g-c08-frameworks-21) | Docker — Docker MCP CLI（docker mcp tools list） | ゲートウェイのソースコード | 表示（印・名前） | [確認] |
| [C08-22](#g-c08-frameworks-22) | LastMile AI — mcp-agent (lastmile-ai/mcp-agent) | SDK のソースコード | その他 | [確認] |
| [C08-23](#g-c08-frameworks-23) | BerriAI — LiteLLM（Responses API の MCP ツール一覧のストリーミング） | ゲートウェイのソースコード | 使わない・読まない・宣言が無いときの扱い | [確認] |
| [C08-24](#g-c08-frameworks-24) | mcp-use — mcp-use（TypeScript サーバー docs） | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C08-25](#g-c08-frameworks-25) | mcp-use — mcp-use（TypeScript サーバー docs） | SDK の文書 | 作者への書き方の案内 | [確認] |
| [C08-26](#g-c08-frameworks-26) | mcp-use — mcp-use（TypeScript クライアント: AI SDK アダプタ） | SDK のソースコード | そのまま渡す・見せる・表示（印・名前） | [確認] |
| [C08-27](#g-c08-frameworks-27) | LangChain4j — LangChain4j (langchain4j-mcp) | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C08-28](#g-c08-frameworks-28) | JetBrains — Koog (agents-mcp-server) | SDK のソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [C08-29](#g-c08-frameworks-29) | AG2 (ag2ai) — AG2（ag2.mcp: エージェントを MCP サーバーとして公開） | SDK の文書 | 作者への書き方の案内・確認を求める | [確認] |
| [C08-30](#g-c08-frameworks-30) | Pydantic — Pydantic AI Harness（MCP 連携の capability） | SDK のソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C08-31](#g-c08-frameworks-31) | Pydantic — Pydantic AI Harness（Notion capability） | SDK の文書 | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C08-32](#g-c08-frameworks-32) | Pydantic — Pydantic AI Harness（hosted MCP 連携の共通説明） | SDK の文書 | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C08-33](#g-c08-frameworks-33) | Pydantic — CLAI 2.0（pydantic_clai2: Pydantic AI の端末クライアント） | クライアントのソースコード | 信頼するなという注意・使わない・読まない | [確認] |
| [C08-34](#g-c08-frameworks-34) | Pydantic — Pydantic AI Harness（Day AI capability） | SDK の文書 | 宣言が無いときの扱い・その他 | [確認] |
| [C08-35](#g-c08-frameworks-35) | VoltAgent — VoltAgent (@voltagent/mcp-server) | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [G3CAMA-01](#g-g3-consumer-apps-model-apis-01) | Google — Gemini アプリ（消費者向け。Connected Apps の custom app = 任意の remote MCP サーバー、Gemini Spark でも使う） | 公式の文書 | 確認を求める | [確認] |
| [G3CAMA-02](#g-g3-consumer-apps-model-apis-02) | Google — Gemini Spark（Gemini アプリのエージェント機能。Connected Apps / custom app を使う） | 公式の文書 | 確認を求める | [確認] |
| [G3CAMA-03](#g-g3-consumer-apps-model-apis-03) | xAI（SpaceXAI） — xAI API の Remote MCP Tools（Responses API 互換・xAI native SDK・Speech to Speech API） | 公式の文書 | 使わない・読まない | [確認] |
| [G3CAMA-04](#g-g3-consumer-apps-model-apis-04) | xAI（SpaceXAI） — xAI API の Remote MCP Tools | 公式の文書 | ツールを絞る・隠す | [確認] |
| [G3CAMA-05](#g-g3-consumer-apps-model-apis-05) | xAI — xai-sdk-python（xAI 公式 Python SDK）の mcp() ツール | SDK のソースコード | ツールを絞る・隠す・使わない・読まない | [確認] |
| [G3CAMA-06](#g-g3-consumer-apps-model-apis-06) | xAI — Grok Build（xAI のコーディング CLI。grok コマンド）の Plan mode | 公式の文書 | 使わない・読まない | [確認] |
| [G3CAMA-07](#g-g3-consumer-apps-model-apis-07) | xAI — Grok Build の権限（Permissions） | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [G3CAMA-08](#g-g3-consumer-apps-model-apis-08) | xAI — Grok Bot（xAI のエージェント製品。ツール呼び出しの承認と Auto Review） | 公式の文書 | その他 | [確認] |
| [G3CAMA-09](#g-g3-consumer-apps-model-apis-09) | Groq — Groq API の Remote MCP（Responses API） | 公式の文書 | 宣言が無いときの扱い | [確認] |
| [G3CAMA-10](#g-g3-consumer-apps-model-apis-10) | Groq — Groq API の Remote MCP（Responses API） | 公式の文書 | 確認を求める | [確認] |
| [G3CAMA-11](#g-g3-consumer-apps-model-apis-11) | Google — google-genai（Python SDK, python-genai）の MCP ツール変換 | SDK のソースコード | 使わない・読まない | [確認] |
| [G3CAMA-12](#g-g3-consumer-apps-model-apis-12) | Google — google-genai（Python SDK）の自動関数呼び出し（MCP セッション） | SDK のソースコード | 使わない・読まない | [確認] |
| [G3CAMA-13](#g-g3-consumer-apps-model-apis-13) | Google — google-genai（JS/TS SDK, js-genai）の MCP ツール変換 | SDK のソースコード | 使わない・読まない | [確認] |
| [G3CAMA-14](#g-g3-consumer-apps-model-apis-14) | Google — Gemini API（generateContent）の SDK 内蔵 MCP 対応 | 公式の文書 | 使わない・読まない | [確認] |
| [G3CAMA-15](#g-g3-consumer-apps-model-apis-15) | Google — Gemini API Interactions API の Remote MCP（mcp_server ツール） | 公式の文書 | ツールを絞る・隠す | [確認] |
| [G3CAMA-16](#g-g3-consumer-apps-model-apis-16) | Google — Gemini API の managed agent（Antigravity agent）の Hooks | 公式の文書 | その他 | [確認] |
| [G3CAMA-17](#g-g3-consumer-apps-model-apis-17) | Anthropic — Claude Desktop（Cowork / Code タブ）の MCP 協調器：読み取り専用・破壊的の判定 | クライアントのソースコード | 宣言が無いときの扱い・危険度を付ける | [確認] |
| [G3CAMA-18](#g-g3-consumer-apps-model-apis-18) | Anthropic — Claude Desktop の MCP ツール呼び出しゲート（mcpToolCallGate） | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [G3CAMA-19](#g-g3-consumer-apps-model-apis-19) | Anthropic — Claude Desktop の Cowork セッション：auto モードの判定 | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [G3CAMA-20](#g-g3-consumer-apps-model-apis-20) | Anthropic — Claude Desktop の Code タブ（CCD）：auto モードの判定 | クライアントのソースコード | 使わない・読まない | [確認] |
| [G3CAMA-21](#g-g3-consumer-apps-model-apis-21) | Anthropic — Claude Desktop（Cowork）の auto モード：破壊的コネクタツールでは「常に許可」を使わない | クライアントのソースコード | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G3CAMA-22](#g-g3-consumer-apps-model-apis-22) | Anthropic — Claude Desktop（Cowork）の watcher（スケジュールタスクの監視）からの MCP 呼び出し | クライアントのソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [G3CAMA-23](#g-g3-consumer-apps-model-apis-23) | Anthropic — Claude Desktop（Cowork）の HTML アーティファクトから MCP ツールを呼ぶ橋（CoworkArtifacts.callMcpTool） | クライアントのソースコード | その他 | [確認] |
| [G3CAMA-24](#g-g3-consumer-apps-model-apis-24) | Anthropic — Claude Desktop（Cowork）の HTML アーティファクトの MCP 橋：破壊的ツールの確認 | クライアントのソースコード | 確認を求める | [確認] |
| [G3CAMA-25](#g-g3-consumer-apps-model-apis-25) | Anthropic — Claude Desktop のアーティファクトの host tools（ローカル MCP サーバーのツールをアーティファクトから呼ぶ）：確認が要るツールの判定 | クライアントのソースコード | 確認を求める・宣言が無いときの扱い | [確認] |
| [G3CAMA-26](#g-g3-consumer-apps-model-apis-26) | Anthropic — Claude Desktop のアーティファクトの host tools：確認の流れ | クライアントのソースコード | 確認を求める | [確認] |
| [G3CAMA-27](#g-g3-consumer-apps-model-apis-27) | Anthropic — Claude Desktop（3P 配備＝第三者クラウド向け）の直結 MCP のツール定義キャッシュ | クライアントのソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [G3CAMA-28](#g-g3-consumer-apps-model-apis-28) | Anthropic — Claude Desktop の組み込み MCP サーバー（built-in）の既定ポリシーの点検 | クライアントのソースコード | 宣言を検査する | [確認] |
| [G3CAMA-29](#g-g3-consumer-apps-model-apis-29) | Anthropic — Claude Desktop の組み込み MCP サーバーの点検：警告 | クライアントのソースコード | 宣言を検査する | [確認] |
| [G3CAMA-30](#g-g3-consumer-apps-model-apis-30) | Anthropic — Claude Desktop の組み込み Microsoft 365 MCP のテレメトリ | クライアントのソースコード | その他 | [確認] |
| [G3CAMA-31](#g-g3-consumer-apps-model-apis-31) | Anthropic — Claude Desktop が直結 MCP のツールを claude.ai 側へ通知する一覧 | クライアントのソースコード | そのまま渡す・見せる | [確認] |
| [G3CAMA-32](#g-g3-consumer-apps-model-apis-32) | Anthropic — Claude Desktop 画面側の MCP ツール承認の決定（Chat / Cowork 共通の承認状態） | クライアントのソースコード | 確認を求める・表示（印・名前） | [確認] |
| [G3CAMA-33](#g-g3-consumer-apps-model-apis-33) | Anthropic — Claude Desktop 画面側の MCP ツール承認：設定値 "readOnly" | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [G3CAMA-34](#g-g3-consumer-apps-model-apis-34) | Anthropic — Claude Desktop 画面側の承認：Cowork の書き込みツール警告 | クライアントのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [G3CAMA-35](#g-g3-consumer-apps-model-apis-35) | Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のツール一覧 | クライアントのソースコード | 表示（印・名前） | [確認] |
| [G3CAMA-36](#g-g3-consumer-apps-model-apis-36) | Anthropic — Claude Desktop 画面側：MCP ディレクトリへの申請フォーム（ツールの点検） | クライアントのソースコード | 宣言を書くことを求める・宣言を検査する | [確認] |
| [G3CAMA-37](#g-g3-consumer-apps-model-apis-37) | Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テスト | クライアントのソースコード | ツールを絞る・隠す・宣言を検査する | [確認] |
| [G3CAMA-38](#g-g3-consumer-apps-model-apis-38) | Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テストの注意書き | クライアントのソースコード | 信頼するなという注意・その他 | [確認] |
| [G3CAMA-39](#g-g3-consumer-apps-model-apis-39) | Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の「読み書き」申告と注釈の照合 | クライアントのソースコード | 宣言を検査する | [確認] |
| [G3CAMA-40](#g-g3-consumer-apps-model-apis-40) | Anthropic — Claude Desktop 画面側：アーティファクトの MCP ツール「監視（watch）」 | クライアントのソースコード | ツールを絞る・隠す | [確認] |
| [G3CAMA-41](#g-g3-consumer-apps-model-apis-41) | OpenRouter — @openrouter/agent（OpenRouter Agent SDK）の MCP ツール包み（@openrouter/mcp が再輸出） | SDK のソースコード | 使わない・読まない | [確認] |
| [G3CAMA-42](#g-g3-consumer-apps-model-apis-42) | Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のラベル | クライアントのソースコード | 表示（印・名前） | [確認] |
| [G3CAMA-43](#g-g3-consumer-apps-model-apis-43) | Anthropic — Claude Desktop 画面側：MCP ツール承認の設定の取りうる値 | クライアントのソースコード | 確認を省く（自動で許可）・規則（ポリシー）の条件に使う | [確認] |
| [G3CAMA-44](#g-g3-consumer-apps-model-apis-44) | Anthropic — Claude Desktop 画面側：破壊的ツールを既定で承認必須にする機能フラグ | クライアントのソースコード | 確認を求める | [確認] |
| [G3CAMA-45](#g-g3-consumer-apps-model-apis-45) | Anthropic — Claude Desktop 画面側（claude.ai と同じ設定画面と思われる）：コネクタの「Tool permissions」のツールの分け方 | クライアントのソースコード | 表示（印・名前） | [確認] |
| [G3CAMA-46](#g-g3-consumer-apps-model-apis-46) | Anthropic — Claude Desktop 画面側：管理者のコネクタ設定（tool policy）のツールの群 | クライアントのソースコード | 表示（印・名前）・規則（ポリシー）の条件に使う | [確認] |
| [G3CAMA-47](#g-g3-consumer-apps-model-apis-47) | Anthropic — Claude Desktop 画面側：Cowork の承認カード（書き込みツール警告が立ったときのボタン） | クライアントのソースコード | 表示（印・名前） | [確認] |

この分冊の資料は 82 件で、うち [確認] は 82 件、[確認（調査時のみ）] は 0 件。

<a id="ag-8-1"></a>
## 資料カード

### n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能）

<a id="g-c08-frameworks-01"></a>
#### C08-01 n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能）

- **資料**: packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts — classifyMcpTool（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts#L77-L83
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts
- **版**: n8n-io/n8n@bae7656（2026-10-02 の main）
- **書いてある場所**: lines 77-83
- **原文**:

> if (tool.annotations?.readOnlyHint === false || tool.annotations?.destructiveHint === true) { return 'write'; } if (tool.annotations?.readOnlyHint === true) { return 'read'; }

- **日本語**: readOnlyHint が false か destructiveHint が true なら「書き込み（write）」、readOnlyHint が true なら「読み取り（read）」に分類する。
- **どう使っているか**: 接続した MCP サーバーのツールを read / write の 2 区分に分け、区分ごとの許可（always_allow / require_approval / blocked）を当てる。注釈による判定はツール名による判定（85-87 行）より先に来るので、readOnlyHint: true を宣言したツールは名前が delete_… や send_… でも read に入る（destructiveHint: true を併記した場合だけ write）。既定設定（mcpRead: always_allow、C08_frameworks-03）では、宣言 D1 がそのまま承認なし実行の可否を決める実例（管理者が mcpRead を require_approval / blocked に変えれば別）。
- **条件**: n8n Instance AI が MCP サーバーのツールを読み込むとき。ツール名ごとの上書き（policy.tools）があればそれが先（94-96 行、目視）。サーバーごとの toolPermissions があればそれが既定より先（mcp-client-manager.ts 85 行、目視）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、77-83 行（取得 2026-10-02T22:11:36Z、sha256 c26f3881fd76…）
- **補足**: 公開 docs（docs.n8n.io の MCP Client Tool ほか）にはこの分類の説明が無い（checked_no_mention 参照）。機能の公開状況（一般提供か、どのプランか）は不明。製品名『Instance AI』はコードのパッケージ名（@n8n/instance-ai）による。　【検証者】注釈はサーバーの tools/list から取ったものがそのまま classifyMcpTool に渡る: packages/@n8n/agents/src/runtime/mcp/mcp-connection.ts `const descriptors: McpToolDescriptor[] = result.tools.map((tool) => ({ name: tool.name, ...(tool.annotations ? { annotations: tool.annotations } : {}), }));`（exact、164-167 行、検証者 id v_n8n_desc）。承認の包みは require_approval の一覧に入ったツールだけ（同ファイル `t.suspendSchema || !this.shouldRequireToolApproval(t, requireApproval) ? t : wrapToolForApproval(t, { requireApproval: true }),`、exact、175-177 行、検証者 id v_n8n_wrap）なので、always_allow の区分のツールは承認なしで実行される。 解釈は正しい。「自動実行に直結」は既定設定（mcpRead: always_allow）のときに限ると usage_ja に明記。注釈が tools/list 由来であることと、always_allow のツールは承認で包まれないことを、別ファイルの exact で notes に足した。

<a id="g-c08-frameworks-02"></a>
#### C08-02 n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能）

- **資料**: packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts — classifyMcpTool（名前による推定）（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts#L85-L87
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts
- **版**: n8n-io/n8n@bae7656
- **書いてある場所**: lines 85-87
- **原文**:

> if (hasWriteName) return 'write'; return segments.some((segment) => READ_SEGMENTS.has(segment)) ? 'read' : 'write';

- **日本語**: 名前に書き込み系の語があれば write。読み取り系の語があれば read。どちらも無ければ write。
- **どう使っているか**: readOnlyHint / destructiveHint で決まらないとき（注釈なし、または readOnlyHint 未設定かつ destructiveHint が true でない）は、ツール名を語に分けて READ_SEGMENTS（get, list, search, read …）と WRITE_SEGMENTS（delete, send, update, run …）で推定する（20-63 行に語の一覧、目視）。どちらにも当たらない名前は write（承認が要る側）に倒す。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、85-87 行（取得 2026-10-02T22:11:36Z、sha256 c26f3881fd76…）
- **補足**: 注意: readOnlyHint を省略し destructiveHint: false だけを書いたツールは注釈では決まらず、名前の推定に回る。

<a id="g-c08-frameworks-03"></a>
#### C08-03 n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能）

- **資料**: packages/@n8n/api-types/src/schemas/instance-ai.schema.ts — 既定の権限（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/api-types/src/schemas/instance-ai.schema.ts#L2371-L2372
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/api-types/src/schemas/instance-ai.schema.ts
- **版**: n8n-io/n8n@bae7656
- **書いてある場所**: lines 2371-2373
- **原文**:

> mcpRead: 'always_allow', mcpWrite: 'require_approval',

- **日本語**: MCP の読み取りツールは既定で「常に許可」、書き込みツールは既定で「承認が必要」。
- **どう使っているか**: 既定設定では、read に分類された MCP ツール（readOnlyHint: true を宣言したもの、または名前が読み取り系のもの）は人の承認なしで実行され、write は承認待ちになる。つまり readOnlyHint: true の宣言は既定で自動承認に直結する。
- **条件**: 管理者が mcpRead / mcpWrite の設定を変えていない既定状態。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、2371-2372 行（取得 2026-10-02T22:11:44Z、sha256 a27db6e360b5…）
- **補足**: DB 移行 packages/@n8n/db/src/migrations/common/1790758111050-MigrateMcpToolPermissions.ts 5 行の既定値 {"categories":{"read":"always_allow","write":"require_approval"}} も exact で確認（id q04c）。設定の読み出しは instance-ai-settings.service.ts 1250-1256 行 getMcpToolPermissions（目視）。　【検証者】設定の mcpRead / mcpWrite が区分 read / write の許可になる対応: packages/@n8n/instance-ai/src/mcp/mcp-client-manager.ts `categories: { read: mcpRead, write: mcpWrite },`（exact、202 行、検証者 id v_n8n_cat）。 解釈は正しい。設定値から区分への対応を exact で notes に足しただけ。

<a id="g-c08-frameworks-04"></a>
#### C08-04 n8n (n8n GmbH) — n8n Instance AI（n8n の AI アシスタントが MCP サーバーに接続する機能）

- **資料**: packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts — compileMcpToolPermissions（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts#L108-L114
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts
- **版**: n8n-io/n8n@bae7656
- **書いてある場所**: lines 108-114
- **原文**:

> const permission = resolveMcpToolPermission(policy, tool); if (permission === 'blocked') { blockedTools.push(tool.name); continue; } if (permission === 'require_approval') approvalTools.push(tool.name);

- **日本語**: ツールごとに許可を決め、blocked ならツール一覧から外し、require_approval なら承認が要るツールの一覧に入れる。
- **どう使っているか**: 区分（注釈から決まる read/write）に当てた許可が blocked のツールは除外（toolFilter: exclude）され、モデルに見えない。require_approval のツールは承認一覧に入る。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、108-114 行（取得 2026-10-02T22:11:36Z、sha256 c26f3881fd76…）
- **補足**: この関数は MCP クライアント接続時に呼ばれる: packages/@n8n/instance-ai/src/mcp/mcp-client-manager.ts 88 行 `configureTools: (tools) => compileMcpToolPermissions(toolPermissions, tools),`（exact、id q04b）。UI 向けの区分表示も classifyMcpTool を使う（cli/src/modules/instance-ai/mcp/instance-ai-mcp-registry.service.ts 71 行、目視）。

### Mastra — Mastra (@mastra/mcp MCPClient)

<a id="g-c08-frameworks-05"></a>
#### C08-05 Mastra — Mastra (@mastra/mcp MCPClient)

- **資料**: packages/mcp/src/client/types.ts — RequireToolApproval の引数 annotations の説明（SDK のソースコード）
- **URL**: https://github.com/mastra-ai/mastra/blob/b5a7bb1a7a06025fa4712e9db2a58e164d54fd30/packages/mcp/src/client/types.ts#L161-L165
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mastra-ai/mastra/b5a7bb1a7a06025fa4712e9db2a58e164d54fd30/packages/mcp/src/client/types.ts
- **版**: mastra-ai/mastra@b5a7bb1（2026-10-02）
- **書いてある場所**: lines 161-165
- **原文**:

> Spec defaults when a hint is omitted: `readOnlyHint: false`, * `destructiveHint: true`, `idempotentHint: false`, `openWorldHint: true`. * This field is `undefined` (not auto-defaulted) when the server omits * annotations entirely, so policies can distinguish "no annotations" from * "annotated as safe".

- **日本語**: ヒントが省略されたときの仕様上の既定値は readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true。サーバーが annotations をまったく出さないとき、このフィールドは既定値で埋めずに undefined のままにするので、方針の側で「注釈なし」と「安全と宣言された」を区別できる。
- **どう使っているか**: requireToolApproval に渡す関数へ、サーバーの注釈をそのまま（既定値で補わずに）渡す。欠落の扱いは利用者の関数に任せる。
- **条件**: 利用者が requireToolApproval に関数を渡したときだけ注釈が判断に使われる。requireToolApproval を省略した既定では、注釈に関係なく全ツールが承認なしで実行される（types.ts 249 行 「`false` or omitted: Tools run without approval (default).」）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、161-165 行（取得 2026-10-02T22:11:32Z、sha256 598f0ca9ffe5…）
- **補足**: 同じコメントの 155-160 行に「annotations are **hints**, not guarantees. Clients MUST consider them untrusted unless they come from a trusted server. Do not use annotations alone as a security boundary」（目視）。docs 側は C02_sdks-59 / -60 が確認済み。　【検証者】既定の記述 「`false` or omitted: Tools run without approval (default).」（exact、249 行、検証者 id v_mastra_default）。注釈は既定値で補わずに関数へ渡る: packages/mcp/src/client/client.ts `return serverApprovalFn({ toolName, args, ...ctx, annotations });`（exact、1404 行、検証者 id v_mastra_pass）。 conditions が空だった。既定（requireToolApproval 省略）では注釈に関係なく承認なしで実行されることを、exact の引用を添えて足した。

<a id="g-c08-frameworks-06"></a>
#### C08-06 Mastra — Mastra (@mastra/mcp MCPClient)

- **資料**: packages/mcp/src/client/types.ts — requireToolApproval の例（注釈による宣言的な承認）（SDK のソースコード）
- **URL**: https://github.com/mastra-ai/mastra/blob/b5a7bb1a7a06025fa4712e9db2a58e164d54fd30/packages/mcp/src/client/types.ts#L264-L273
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mastra-ai/mastra/b5a7bb1a7a06025fa4712e9db2a58e164d54fd30/packages/mcp/src/client/types.ts
- **版**: mastra-ai/mastra@b5a7bb1
- **書いてある場所**: lines 267-271
- **原文**:

> requireToolApproval: ({ annotations }) => { * // No annotations? Assume the worst (spec default: destructive). * if (!annotations) return true; * if (annotations.readOnlyHint) return false; * if (annotations.destructiveHint) return true;

- **日本語**: requireToolApproval: ({ annotations }) => {…} 注釈が無ければ最悪を仮定する（仕様の既定は破壊的）。注釈が無ければ承認を求める。readOnlyHint なら承認不要。destructiveHint なら承認を求める。
- **どう使っているか**: 注釈で承認要否を決める例。注釈なし→承認、readOnlyHint: true→自動実行、destructiveHint: true→承認。直前のコメントに「only sound for trusted servers」。
- **条件**: 利用者が requireToolApproval に関数を渡したとき（コード内の例。既定の挙動ではない）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）・宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、267-271 行（取得 2026-10-02T22:11:32Z、sha256 598f0ca9ffe5…）

### Vercel — AI SDK (@ai-sdk/mcp, MCP client)

<a id="g-c08-frameworks-07"></a>
#### C08-07 Vercel — AI SDK (@ai-sdk/mcp, MCP client)

- **資料**: packages/mcp/src/tool/mcp-client.ts — ツールの metadata に注釈を写す（SDK のソースコード）
- **URL**: https://github.com/vercel/ai/blob/5b8e63bad8209a8e86c1de8d352daaf3c14e2671/packages/mcp/src/tool/mcp-client.ts#L1193-L1201
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vercel/ai/5b8e63bad8209a8e86c1de8d352daaf3c14e2671/packages/mcp/src/tool/mcp-client.ts
- **版**: vercel/ai@5b8e63b（2026-10-01）
- **書いてある場所**: lines 1193-1201
- **原文**:

> ...(annotations != null ? { annotations: { ...(annotations.title != null ? { title: annotations.title } : {}), ...(annotations.readOnlyHint != null ? { readOnlyHint: annotations.readOnlyHint } : {}),

- **日本語**: annotations があれば、title・readOnlyHint（と続く destructiveHint・idempotentHint・openWorldHint）のうち値のあるものだけをツールの metadata.annotations に写す。
- **どう使っているか**: MCP クライアントは注釈を AI SDK のツール metadata に写すだけで、承認の判定はしない（承認は利用者の toolApproval / needsApproval に任せる）。値の無いヒントは写さないので、既定値は埋められない。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、1193-1201 行（取得 2026-10-02T22:11:38Z、sha256 e76d34cbd44a…）
- **補足**: title は title ?? annotations?.title（1177 行、目視）。docs 側の説明は C02_sdks-47〜49 が確認済み。

### Hugging Face — Hugging Face MCP Server (huggingface/hf-mcp-server)

<a id="g-c08-frameworks-08"></a>
#### C08-08 Hugging Face — Hugging Face MCP Server (huggingface/hf-mcp-server)

- **資料**: packages/app/src/server/utils/remote-tool-annotations.ts（サーバのソースコード）
- **URL**: https://github.com/huggingface/hf-mcp-server/blob/102aca92c1442cfd124021cf57d9ae46e8f3a3c8/packages/app/src/server/utils/remote-tool-annotations.ts#L1-L22
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/huggingface/hf-mcp-server/102aca92c1442cfd124021cf57d9ae46e8f3a3c8/packages/app/src/server/utils/remote-tool-annotations.ts
- **版**: huggingface/hf-mcp-server@102aca9（2026-10-02）
- **書いてある場所**: lines 2-5
- **原文**:

> Remote tools can execute arbitrary upstream behavior. Unless this server can * independently verify an upstream tool's guarantees, advertise the * conservative MCP defaults explicitly so clients can present suitable * confirmation UI.

- **日本語**: リモートのツールは上流で何でも実行しうる。上流ツールの保証をこのサーバーが独自に確かめられない限り、MCP の保守的な既定値を明示的に広告し、クライアントが適切な確認 UI を出せるようにする。
- **どう使っているか**: 中継するリモートツールには、上流の宣言を引き継がず、仕様の既定と同じ保守的な値（readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true）を明示して載せる。目的は、クライアントが適切な確認 UI を出せるようにすること（コメントは『Unless this server can independently verify an upstream tool's guarantees』と条件を付けるが、このコミットのコードは常に固定値で、検証して値を変える経路は無い）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、2-5 行（取得 2026-10-02T22:11:35Z、sha256 4b7c44760dd7…）
- **補足**: 値は同ファイル 16-22 行 `return { title, readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true, };`（exact、id q08b）。 usage_ja の「クライアントに確認を出させる」は言い過ぎ（原文は「so clients can present suitable confirmation UI」＝出せるように）。コメントの条件（独自に検証できない限り）と、コードには検証の経路が無いことを明記。

<a id="g-c08-frameworks-09"></a>
#### C08-09 Hugging Face — Hugging Face MCP Server (huggingface/hf-mcp-server)

- **資料**: packages/app/src/server/mcp-proxy.ts — 上流ツールの登録（サーバのソースコード）
- **URL**: https://github.com/huggingface/hf-mcp-server/blob/102aca92c1442cfd124021cf57d9ae46e8f3a3c8/packages/app/src/server/mcp-proxy.ts#L96-L102
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/huggingface/hf-mcp-server/102aca92c1442cfd124021cf57d9ae46e8f3a3c8/packages/app/src/server/mcp-proxy.ts
- **版**: huggingface/hf-mcp-server@102aca9
- **書いてある場所**: lines 96-102
- **原文**:

> server.registerTool( config.toolName, { title, description, inputSchema: z.object(schemaShape), annotations: createRemoteToolAnnotations(title),

- **日本語**: server.registerTool(config.toolName, { title, description, inputSchema: …, annotations: createRemoteToolAnnotations(title), … })
- **どう使っているか**: 上流（リモート MCP / Gradio Space）のツールを中継して登録するとき、annotations は常に createRemoteToolAnnotations(title) の固定値になる。上流が宣言した readOnlyHint などは引き継がない（このファイルで annotations の語はこの行と import だけ、grep で確認）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、96-102 行（取得 2026-10-02T22:11:42Z、sha256 b1db901cea99…）
- **補足**: Gradio エンドポイントの中継（gradio-endpoint-connector.ts 329 行 `annotations: createRemoteToolAnnotations(title),`、exact、id q09b）も同じ。HF 自身のツール（例 hf_whoami: readOnlyHint true, destructiveHint false）は個別に値を宣言している（mcp-server.ts 375-381 行、目視）。

### Agno — Agno AgentOS（エージェントを MCP サーバーとして公開）

<a id="g-c08-frameworks-10"></a>
#### C08-10 Agno — Agno AgentOS（エージェントを MCP サーバーとして公開）

- **資料**: libs/agno/agno/os/mcp.py — 組み込みツールの注釈を明示する理由（コメント）（SDK のソースコード）
- **URL**: https://github.com/agno-agi/agno/blob/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/os/mcp.py#L103-L107
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agno-agi/agno/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/os/mcp.py
- **版**: agno-agi/agno@3ca74c2（2026-10-02）
- **書いてある場所**: lines 103-107
- **原文**:

> All three of readOnlyHint/destructiveHint/openWorldHint are stated rather than left # implicit, here and on every built-in tool. An omitted hint is not "unknown" to a # client -- it falls back to a protocol default -- and a directory submission scan # rejects a tool that leaves any of the three unset, so a hint the server declines to # state is a hint someone else answers on its behalf.

- **日本語**: readOnlyHint / destructiveHint / openWorldHint の 3 つは、ここでも組み込みツールすべてでも、暗黙にせず明示する。省略したヒントはクライアントにとって「不明」ではなくプロトコルの既定値に落ちる。またディレクトリ申請時のスキャンは 3 つのどれかが未設定のツールを却下するので、サーバーが言わないヒントは他の誰かが代わりに答えることになる。
- **どう使っているか**: サーバー側の作者（Agno）の方針: 3 つのヒントを必ず明示する。コメントが挙げる理由は (1) 省略は既定値扱いになる (2) ディレクトリの申請スキャンが未設定を却下する、の 2 点。(2) は Agno のコメントの主張で、どのディレクトリかは書かれていない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、103-107 行（# All three of readOnlyHint/destructiveHint/openWorldHint are stated rather than left）（取得 2026-10-02T22:11:33Z、sha256 327506ab0f97…）
- **補足**: 『directory submission scan』がどのディレクトリかはコメントに書かれていない（OpenAI の ChatGPT アプリ審査の要件と合うが、ここでは不明。C05 の項を参照）。組み込みツールの値の例: 2363 行 readOnlyHint True / destructiveHint False / idempotentHint True / openWorldHint False（目視）。　【検証者】同じ主張が libs/agno/agno/tools/annotations.py 4-7 行にもある: 「Assistant marketplaces read them: a submission scan rejects tools that carry none, and reviewers test the claim against the tool's real behaviour, so a wrong hint is worse than a missing one.」（exact、4-7 行、検証者 id v_agno_market）。こちらも marketplace の名前は無い（不明）。 理由 (2)（申請スキャンが却下する）が Agno のコメントの主張で未検証であることを usage_ja に明記。同趣旨の別ファイルの記述を exact で notes に足した。

<a id="g-c08-frameworks-11"></a>
#### C08-11 Agno — Agno AgentOS（エージェントを MCP サーバーとして公開）

- **資料**: libs/agno/agno/os/mcp.py — 公開したエージェントの run ツールの既定注釈（SDK のソースコード）
- **URL**: https://github.com/agno-agi/agno/blob/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/os/mcp.py#L99-L117
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agno-agi/agno/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/os/mcp.py
- **版**: agno-agi/agno@3ca74c2
- **書いてある場所**: lines 113-117
- **原文**:

> _EXPOSED_COMPONENT_ANNOTATIONS: Dict[str, Any] = { "readOnlyHint": False, "destructiveHint": True, "openWorldHint": True, }

- **日本語**: _EXPOSED_COMPONENT_ANNOTATIONS = { readOnlyHint: False, destructiveHint: True, openWorldHint: True }
- **どう使っているか**: エージェント / チーム / ワークフローを MCP ツールとして公開するとき、既定で「読み取りでない・破壊的・外部に届く」と宣言する。理由（100-101 行）: 「A run is not read-only (it persists a session and may call side-effectful tools) and reaches beyond this server.」（exact、id q11）。
- **条件**: 公開する側が as_tool(annotations=...) で上書きしない場合。上書きはキーごとに既定へ重ね、値に None を渡すとそのキーを外せる（libs/agno/agno/tools/annotations.py 62-75 行 merge_tool_annotations。65-66 行「A key set to ``None`` in the overrides is REMOVED from the result rather than emitted as null」）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、113-117 行（# deployment. The config and session tools only read storage this deployment owns.）（取得 2026-10-02T22:11:33Z、sha256 327506ab0f97…）
- **補足**: 【検証者】上書きの規則の引用は exact、65-66 行、検証者 id v_agno_merge。 conditions を、上書きがキーごとであること・None でキーを外せることまで具体化（exact）。

### Agno — Agno MCPTools（MCP クライアント）

<a id="g-c08-frameworks-12"></a>
#### C08-12 Agno — Agno MCPTools（MCP クライアント）

- **資料**: libs/agno/agno/tools/mcp/mcp.py — ツールの登録（SDK のソースコード）
- **URL**: https://github.com/agno-agi/agno/blob/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/tools/mcp/mcp.py#L950
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agno-agi/agno/3ca74c272fa5017fae4fab234e988378c8f14c63/libs/agno/agno/tools/mcp/mcp.py
- **版**: agno-agi/agno@3ca74c2
- **書いてある場所**: lines 950
- **原文**:

> requires_confirmation=tool_name in self.requires_confirmation_tools,

- **日本語**: requires_confirmation = ツール名が self.requires_confirmation_tools に含まれるか
- **どう使っているか**: クライアント側の MCPTools は、確認（human-in-the-loop）の要否をツール名の一覧だけで決める。サーバーの注釈は使わない（このファイルに readOnlyHint / destructiveHint / ToolAnnotations の語は 0 件、checked_no_mention 参照）。同じ Agno でもサーバー側（AgentOS）は注釈を明示するが、クライアント側は読まない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、950 行（# Match the default bound on automatic discovery through fastmcp's Client.）（取得 2026-10-02T22:11:59Z、sha256 2c90826d299f…）

### Microsoft — AutoGen (autogen-ext McpWorkbench)

<a id="g-c08-frameworks-13"></a>
#### C08-13 Microsoft — AutoGen (autogen-ext McpWorkbench)

- **資料**: python/packages/autogen-ext/src/autogen_ext/tools/mcp/_workbench.py — list_tools（SDK のソースコード）
- **URL**: https://github.com/microsoft/autogen/blob/027ecf0a379bcc1d09956d46d12d44a3ad9cee14/python/packages/autogen-ext/src/autogen_ext/tools/mcp/_workbench.py#L306-L310
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/microsoft/autogen/027ecf0a379bcc1d09956d46d12d44a3ad9cee14/python/packages/autogen-ext/src/autogen_ext/tools/mcp/_workbench.py
- **版**: microsoft/autogen@027ecf0（2026-04-06 のコミット。2026-10-02 の git ls-remote でも HEAD のまま）
- **書いてある場所**: lines 306-310
- **原文**:

> tool_schema = ToolSchema( name=name, description=description, parameters=parameters, )

- **日本語**: tool_schema = ToolSchema(name=name, description=description, parameters=parameters)
- **どう使っているか**: McpWorkbench は MCP のツール一覧を AutoGen の ToolSchema（名前・説明・引数）に変えるとき annotations を捨てる。エージェント側は注釈を見られない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、306-310 行（取得 2026-10-02T22:11:35Z、sha256 fa06069fed60…）
- **補足**: autogen_ext/tools/mcp 以下で annotations を扱うのは _base.py 180 行のリソース内容の注釈（content annotations）だけで、ToolAnnotations ではない（grep で確認）。公開 docs も checked_no_mention。 解釈は正しい。version に、2026-10-02 時点でもこのコミットが HEAD であること（git ls-remote）を足しただけ。

### Cloudflare — Cloudflare Agents SDK（agents パッケージの MCP クライアント）

<a id="g-c08-frameworks-14"></a>
#### C08-14 Cloudflare — Cloudflare Agents SDK（agents パッケージの MCP クライアント）

- **資料**: packages/agents/src/mcp/client/index.ts — getAITools（SDK のソースコード）
- **URL**: https://github.com/cloudflare/agents/blob/3ddbd76cf0a21c46410563281bded36a2f56a911/packages/agents/src/mcp/client/index.ts#L2119
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cloudflare/agents/3ddbd76cf0a21c46410563281bded36a2f56a911/packages/agents/src/mcp/client/index.ts
- **版**: cloudflare/agents@3ddbd76（2026-10-02）
- **書いてある場所**: lines 2119
- **原文**:

> const title = tool.title ?? tool.annotations?.title;

- **日本語**: const title = tool.title ?? tool.annotations?.title;
- **どう使っているか**: MCP ツールを AI SDK のツールに変えるとき、注釈からは title だけを使う（tool.title が無いときの代わり）。readOnlyHint などは AI SDK ツールに渡さず、承認（needsApproval）にも使わない。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、2119 行（取得 2026-10-02T22:11:40Z、sha256 805a9fdc2352…）
- **補足**: 変換後のオブジェクトは description / title / execute だけ（2120-2125 行、目視）。

### Cloudflare — Cloudflare Agents SDK（実験的 WebMCP アダプタ）

<a id="g-c08-frameworks-15"></a>
#### C08-15 Cloudflare — Cloudflare Agents SDK（実験的 WebMCP アダプタ）

- **資料**: packages/agents/src/experimental/webmcp.ts（SDK のソースコード）
- **URL**: https://github.com/cloudflare/agents/blob/3ddbd76cf0a21c46410563281bded36a2f56a911/packages/agents/src/experimental/webmcp.ts#L216-L220
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cloudflare/agents/3ddbd76cf0a21c46410563281bded36a2f56a911/packages/agents/src/experimental/webmcp.ts
- **版**: cloudflare/agents@3ddbd76
- **書いてある場所**: lines 218-220
- **原文**:

> annotations: t.annotations ? { readOnlyHint: t.annotations.readOnlyHint } : undefined

- **日本語**: annotations があれば { readOnlyHint: t.annotations.readOnlyHint } だけを残す。
- **どう使っているか**: サーバーの MCP ツールをブラウザの WebMCP（navigator.modelContext.registerTool）に登録し直すとき、注釈は readOnlyHint だけを渡し、destructiveHint・idempotentHint・openWorldHint は落とす（WebMCP 側の型 ModelContextToolAnnotations が readOnlyHint しか持たない、67-69 行、目視）。
- **条件**: @experimental の WebMCP アダプタを使うとき。ファイル冒頭に「WARNING: EXPERIMENTAL — DO NOT USE IN PRODUCTION」（3 行）とあり、Chrome の navigator.modelContext（早期プレビュー）向け。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、218-220 行（取得 2026-10-02T22:11:32Z、sha256 e279ec63b3e7…）
- **補足**: 【検証者】警告文は exact、3 行、検証者 id v_cf_experimental。登録側（437-490 行 registerTools）でも annotations は readOnlyHint だけを渡す（目視）。 conditions に、本番で使うなという警告（exact）と対象が Chrome の早期プレビュー API であることを足した。

### Cloudflare — Cloudflare Agents SDK（docs: McpClient API）

<a id="g-c08-frameworks-16"></a>
#### C08-16 Cloudflare — Cloudflare Agents SDK（docs: McpClient API）

- **資料**: Agents docs — McpClient API: Get available tools（SDK の文書）
- **URL**: https://developers.cloudflare.com/agents/model-context-protocol/apis/client-api/#get-available-tools
- **照らし合わせた中身の URL**: https://developers.cloudflare.com/agents/model-context-protocol/apis/client-api/index.md
- **版**: developers.cloudflare.com（2026-10-02 取得）
- **書いてある場所**: lines 451（Markdown 見出し ### Get available tools）（一致 451 と 462 行の 2 か所）
- **原文**:

> console.log(`  Title: ${tool.title ?? tool.annotations?.title ?? tool.name}`);

- **日本語**: 表示用のタイトルは tool.title、無ければ tool.annotations?.title、それも無ければ tool.name。
- **どう使っているか**: docs の例で注釈から使うのは title だけ（表示名の代わり）。readOnlyHint などの使い方はこのページに無い。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・2 か所、451 行（### Get available tools）（取得 2026-10-02T22:11:23Z、sha256 6342cd23301e…）
- **補足**: fetched_url はページの Markdown 版（index.md、451 行と 462 行の 2 か所）。HTML 版で同じ節の文『Use listTools() to inspect the raw MCP catalog without preparing tools for an AI SDK model call』が exact（id q16h、見出し McpClient > Using MCP capabilities > Get available tools）。

### Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway)

<a id="g-c08-frameworks-17"></a>
#### C08-17 Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway)

- **資料**: docs/server-entry-spec.md — ToolAnnotations Object Structure（ゲートウェイの文書）
- **URL**: https://github.com/docker/mcp-gateway/blob/a34df45d4ec0e941a9853ad768c4f6cd818966b3/docs/server-entry-spec.md#L142-L149
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-gateway/a34df45d4ec0e941a9853ad768c4f6cd818966b3/docs/server-entry-spec.md
- **版**: docker/mcp-gateway@a34df45（2026-09-16）
- **書いてある場所**: lines 146（Markdown 見出し ### Tools Definition）
- **原文**:

> | `readOnlyHint` | boolean | No | Hint that the tool only reads data and does not modify state. |

- **日本語**: readOnlyHint は boolean、必須ではない。ツールがデータを読むだけで状態を変えないことのヒント。
- **どう使っているか**: Docker の MCP カタログの server エントリでは、ツールごとに annotations（title と 4 つのヒント）を書けるが、どれも Required: No（任意）。tools 配列は発見と文書化のためのもので、annotations は OCI カタログでだけ設定される。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、146 行（### Tools Definition）（取得 2026-10-02T22:12:57Z、sha256 1e202a3b0e54…）
- **補足**: 表の他の行: destructiveHint / idempotentHint / openWorldHint / title も Required No（目視）。Docker の公開 docs（docs.docker.com の MCP Toolkit / Gateway / Catalog）には注釈の語が無い（checked_no_mention）。　【検証者】同じ文書で、server の tools 配列自体が「Used for discovery and documentation.」とされる（120 行、exact、120 行、検証者 id v_docker_tools_doc）。annotations の行は「only set for OCI catalogs」（129 行、目視）。 tools 配列が「発見と文書化のため」であること（exact）と、annotations が OCI カタログに限ることを足した。

<a id="g-c08-frameworks-18"></a>
#### C08-18 Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway)

- **資料**: pkg/catalog/types.go — ToolAnnotations 型（ゲートウェイのソースコード）
- **URL**: https://github.com/docker/mcp-gateway/blob/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/catalog/types.go#L202-L208
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-gateway/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/catalog/types.go
- **版**: docker/mcp-gateway@a34df45
- **書いてある場所**: lines 202-204
- **原文**:

> type ToolAnnotations struct { Title string `json:"title,omitempty" yaml:"title,omitempty"` ReadOnlyHint *bool `json:"readOnlyHint,omitempty" yaml:"readOnlyHint,omitempty"`

- **日本語**: type ToolAnnotations struct { Title …; ReadOnlyHint *bool … }（ポインタなので「未設定」と false を区別できる）
- **どう使っているか**: カタログのツール定義に注釈を持てる型。ヒントは *bool で、書かれていなければ nil（既定値で埋めない）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、202-204 行（取得 2026-10-02T22:11:32Z、sha256 8d16cca7db97…）
- **補足**: Tool 構造体のコメント（139-142 行、目視）: 「These will only be set for oci catalogs (not legacy catalogs).」　【検証者】このリポジトリでカタログ側の ToolAnnotations を読むのは取り込み（pkg/catalog/import_spec.go 84 行）だけで、ゲートウェイの呼び出し処理やポリシーでは使わない（grep、HEAD a34df45）。表示側では `docker mcp server inspect` がカタログの tools JSON の annotations をそのまま JSON 出力に入れる（cmd/docker-mcp/server/inspect.go 45 行 「Annotations map[string]json.RawMessage `json:"annotations,omitempty"`」、exact、45 行、検証者 id v_docker_inspect）。 解釈は正しい。カタログの注釈がどこで読まれるか（取り込みと server inspect の出力だけ）を足した。

<a id="g-c08-frameworks-19"></a>
#### C08-19 Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway)

- **資料**: pkg/gateway/handlers.go — mcpServerToolHandler（ゲートウェイのソースコード）
- **URL**: https://github.com/docker/mcp-gateway/blob/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/gateway/handlers.go#L102
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-gateway/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/gateway/handlers.go
- **版**: docker/mcp-gateway@a34df45
- **書いてある場所**: lines 102
- **原文**:

> func (g *Gateway) mcpServerToolHandler(serverName string, server *mcp.Server, _ *mcp.ToolAnnotations, originalToolName string) mcp.ToolHandler {

- **日本語**: ツール呼び出しのハンドラは注釈を引数に受け取るが、名前を _ にして使わない。
- **どう使っているか**: ゲートウェイはツール呼び出しの処理で注釈を参照しない（引数を _ で捨てる）。一方、tools/list では上流のツールを丸ごとコピーし、名前に接頭辞を付け、入出力スキーマの方言を正規化する（tool_schema_dialect.go 29-31 行・68 行）。annotations には手を付けないので、クライアントへ素通しされる。例外として code mode の run_tools_with_javascript は title だけの注釈を持つ 1 つのツールで、包まれた個々のツールのヒントはクライアントに届かない（pkg/codemode/codemode.go 67-69 行）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、102 行（取得 2026-10-02T22:11:33Z、sha256 43f38987f475…）
- **補足**: 【検証者】スキーマ正規化 `tool.InputSchema = g.normalizeSchemaDialect(ctx, tool.InputSchema, serverName, "inputSchema", relayed)`（exact、68 行、検証者 id v_docker_normalize。PreserveToolSchemaDialect が真なら正規化もしない）。code mode の注釈 `Annotations: &mcp.ToolAnnotations{ Title: "Run tools with Javascript", },`（exact、67-69 行、検証者 id v_docker_codemode）。 「名前だけ変える」は不正確（入出力スキーマの方言も正規化する。ただし annotations は不変なので結論は同じ）。code mode では個々のツールのヒントがクライアントに届かない例外を足した（どちらも exact）。

<a id="g-c08-frameworks-20"></a>
#### C08-20 Docker — Docker MCP Gateway / MCP Toolkit (docker/mcp-gateway)

- **資料**: pkg/policy/policy.go — policy.Request（ゲートウェイのソースコード）
- **URL**: https://github.com/docker/mcp-gateway/blob/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/policy/policy.go#L43-L60
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-gateway/a34df45d4ec0e941a9853ad768c4f6cd818966b3/pkg/policy/policy.go
- **版**: docker/mcp-gateway@a34df45
- **書いてある場所**: lines 54-57
- **原文**:

> // Tool identifies the tool name for the request. Tool string `json:"tool,omitempty"` // Action identifies the action for the request. Action Action `json:"action,omitempty"`

- **日本語**: Tool はリクエストのツール名、Action はリクエストの動作。
- **どう使っているか**: ツール呼び出し前のポリシー判定（withInvokePolicy）にゲートウェイが渡す要求は catalog / working set / server / tool 名 / action などで、注釈の欄が無い。評価は Docker Desktop 側（DesktopClient、このリポジトリの外）が行うので、Desktop 側がカタログ名とツール名からカタログの注釈を引くかどうかは不明。ゲートウェイのコードの範囲では、注釈はポリシーの入力にならない。
- **条件**: ポリシー評価が働くのは Docker Desktop の中で動き、feature flag「MCPGovernance」が有効なときだけ。それ以外は NoopClient で全部許可（pkg/policy/policy.go 103-115 行）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、54-57 行（取得 2026-10-02T22:11:33Z、sha256 39313306e8d7…）
- **補足**: 組み立て側: pkg/gateway/configuration.go 282-288 行 `req := policy.Request{ Catalog: …, WorkingSet: …, Server: serverName, Tool: tool, Action: action, }`（exact、id q20b）。pkg/policy 以下に hint / annotation の語は 0 件（grep）。　【検証者】`if !desktop.IsRunningInDockerDesktop(ctx) { return NoopClient{} }`（exact、105-107 行、検証者 id v_docker_noop）、`enabled, err := desktop.CheckFeatureFlagIsEnabled(ctx, "MCPGovernance")`（exact、109 行、検証者 id v_docker_gov）。 「注釈はポリシーの入力にならない」は言い過ぎ。要求の構造体に欄が無いのは確かだが、評価は Docker Desktop 側（非公開）なので、そちらがカタログの注釈を引くかは不明と直した。ポリシーが働く条件（Docker Desktop 内で MCPGovernance フラグ有効）を exact で conditions に足した。

### Docker — Docker MCP CLI（docker mcp tools list）

<a id="g-c08-frameworks-21"></a>
#### C08-21 Docker — Docker MCP CLI（docker mcp tools list）

- **資料**: cmd/docker-mcp/tools/list.go — toolDescription（ゲートウェイのソースコード）
- **URL**: https://github.com/docker/mcp-gateway/blob/a34df45d4ec0e941a9853ad768c4f6cd818966b3/cmd/docker-mcp/tools/list.go#L108-L112
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-gateway/a34df45d4ec0e941a9853ad768c4f6cd818966b3/cmd/docker-mcp/tools/list.go
- **版**: docker/mcp-gateway@a34df45
- **書いてある場所**: lines 108-111
- **原文**:

> func toolDescription(tool *mcp.Tool) string { if tool.Annotations != nil && tool.Annotations.Title != "" { return tool.Annotations.Title }

- **日本語**: 注釈に title があればそれを説明として表示し、無ければ description の要約を使う。
- **どう使っているか**: CLI のツール一覧（docker mcp tools list）の説明欄に annotations.title を使う（title が無ければ description）。readOnlyHint などはこの一覧には出ない。ただし別のコマンド docker mcp server inspect は、カタログの tools JSON の annotations をそのまま JSON 出力に含める（inspect.go 45 行・31-33 行）ので、ヒントは利用者に見える形で出力される。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、108-111 行（取得 2026-10-02T22:11:36Z、sha256 c501a14ffa1e…）
- **補足**: 【検証者】inspect の型 「Annotations map[string]json.RawMessage `json:"annotations,omitempty"`」（exact、45 行、検証者 id v_docker_inspect）と JSON 出力 `func (s Info) ToJSON() ([]byte, error) { return json.MarshalIndent(s, "", "  ") }`（exact、31-33 行、検証者 id v_docker_inspect_json）。 「readOnlyHint などは表示にも使わない（cmd 以下で .Annotations を読むのはこの関数だけ）」は誤り。docker mcp server inspect は注釈を生の JSON のまま出力に含める（.Annotations を読まずに json.RawMessage で素通しするので grep に掛からなかった）。usage_ja を直した（exact）。

### LastMile AI — mcp-agent (lastmile-ai/mcp-agent)

<a id="g-c08-frameworks-22"></a>
#### C08-22 LastMile AI — mcp-agent (lastmile-ai/mcp-agent)

- **資料**: src/mcp_agent/agents/agent.py — list_tools のトレース属性（SDK のソースコード）
- **URL**: https://github.com/lastmile-ai/mcp-agent/blob/f62d849350816588b1c6294e7914bbe4d8b84072/src/mcp_agent/agents/agent.py#L641-L663
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/lastmile-ai/mcp-agent/f62d849350816588b1c6294e7914bbe4d8b84072/src/mcp_agent/agents/agent.py
- **版**: lastmile-ai/mcp-agent@f62d849（2026-01-25）
- **書いてある場所**: lines 651-663
- **原文**:

> if tool.annotations: for attr in [ "title", "readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint", ]: value = getattr(tool.annotations, attr, None) if value is not None: span.set_attribute( f"tool.{tool.name}.annotations.{attr}", value )

- **日本語**: ツールに annotations があれば、title と 4 つのヒントのうち値のあるものを、トレースの span 属性 tool.<名前>.annotations.<属性> として記録する。
- **どう使っているか**: 注釈は観測（OpenTelemetry のトレース）に記録するだけで、承認や絞り込みには使わない。
- **条件**: tracing が有効なとき（641-643 行 `if not self.context.tracing_enabled: return`、exact、id q22b）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、651-663 行（取得 2026-10-02T22:11:42Z、sha256 950210b6fb50…）

### BerriAI — LiteLLM（Responses API の MCP ツール一覧のストリーミング）

<a id="g-c08-frameworks-23"></a>
#### C08-23 BerriAI — LiteLLM（Responses API の MCP ツール一覧のストリーミング）

- **資料**: litellm/responses/mcp/mcp_streaming_iterator.py（ゲートウェイのソースコード）
- **URL**: https://github.com/BerriAI/litellm/blob/615ed7900f3bcfd09b324c38c5123eb6ed4769da/litellm/responses/mcp/mcp_streaming_iterator.py#L114-L123
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/BerriAI/litellm/615ed7900f3bcfd09b324c38c5123eb6ed4769da/litellm/responses/mcp/mcp_streaming_iterator.py
- **版**: BerriAI/litellm@615ed79（2026-10-02）
- **書いてある場所**: lines 117-119
- **原文**:

> "name": getattr(tool, "name", "unknown"), "description": getattr(tool, "description", ""), "annotations": {"read_only": False},

- **日本語**: OpenAI 形式の mcp_list_tools を作るとき、各ツールの annotations を一律に {"read_only": False} にする。
- **どう使っているか**: LiteLLM が Responses API の MCP ツール一覧（OpenAI の output_item 形式）を返すとき、上流サーバーの readOnlyHint を見ずに全ツールを read_only: False として出す。
- **条件**: LiteLLM の Responses API で litellm_proxy 経由の MCP ツールをストリーミングするとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、117-119 行（取得 2026-10-02T22:11:27Z、sha256 fc8128b6c676…）
- **補足**: LiteLLM の MCP Gateway docs（docs.litellm.ai/docs/mcp）には注釈の語が無い（checked_no_mention）。【検証者】発見者が『不明』とした他の経路: MCP ゲートウェイがサーバーごとのツールを集めるとき、上流の Tool を深いコピーして名前だけ変える（litellm/proxy/_experimental/mcp_server/result_conversion.py `def to_gateway_tool(tool: Tool, name: str) -> Tool: update: Final[_Renamed] = {"name": name} return tool.model_copy(deep=True, update=update)`、exact、118-120 行、検証者 id v_litellm_copy。呼び出し側 mcp_server_manager.py `prefixed_tools.append(to_gateway_tool(tool, prefixed_name if add_prefix else original_name))`、exact、5528 行、検証者 id v_litellm_prefixed）。この段階では注釈は残る。tools/list の最終応答（operations.py 以降のフィルタ類）まで注釈が残るかは追っていない（不明）。つまり同じ LiteLLM でも、MCP ゲートウェイの集約では注釈を保持し、Responses API のストリーミング一覧では一律 read_only: False にする。 発見者の「プロキシ本体に readOnlyHint 等は 0 件、別経路の素通しは不明」を更新。ゲートウェイの集約は Tool を model_copy(deep=True) で名前だけ変えるので注釈を保持する（exact 2 件）。語が 0 件なのは型ごとコピーするためで、捨てている証拠ではなかった。

### mcp-use — mcp-use（TypeScript サーバー docs）

<a id="g-c08-frameworks-24"></a>
#### C08-24 mcp-use — mcp-use（TypeScript サーバー docs）

- **資料**: mcp-use docs — Tools: Add tool annotations（SDK の文書）
- **URL**: https://docs.mcp-use.com/typescript/server/tools#add-tool-annotations
- **照らし合わせた中身の URL**: https://docs.mcp-use.com/typescript/server/tools
- **版**: docs.mcp-use.com（2026-10-02 取得）
- **書いてある場所**: Tools > Add tool annotations（ソース docs/typescript/server/tools.mdx 88 行、Markdown 見出し ## Add tool annotations の直後）
- **原文**:

> Tool annotations tell clients and models how risky a tool is. Set the main behavior hints explicitly, especially for tools exposed to ChatGPT or MCP catalogs.

- **日本語**: ツールの注釈は、そのツールがどれだけ危険かをクライアントとモデルに伝える。主な動作ヒントは明示的に設定すること。特に ChatGPT や MCP カタログに出すツールでは。
- **どう使っているか**: サーバー作者向けの指針: ヒントを明示する（例: readOnlyHint true / destructiveHint false / openWorldHint true）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Add tool annotations」（取得 2026-10-02T22:11:27Z、sha256 c84a9dfde1b5…）
- **補足**: ツールの見出し判定は『Tools > Describe inputs with Zod』（#describe-inputs-with-zod）だったが、ページ上では直前の見出し『Add tool annotations』の最初の段落（同じ節の q25 は Tools > Add tool annotations と判定）。url には #add-tool-annotations を付けた。source: mcp-use/mcp-use@bde3433 docs/typescript/server/tools.mdx 86-88 行（目視）。　【検証者】HTML 版ではツールの見出し判定が『Tools > Describe inputs with Zod』を返す（本文の並びは Add tool annotations の直後、文脈で確認）。ソース https://raw.githubusercontent.com/mcp-use/mcp-use/bde34336cb6cff3e10fb9c4b1d67850be57e6ad6/docs/typescript/server/tools.mdx でも同じ引用が exact（88 行、見出し ## Add tool annotations、検証者 id v_mcpuse_mdx）。location と anchored_url はソースの見出しに合わせた。 location を発見者の注記どおり Add tool annotations に確定（ソースの mdx で exact、88 行の直前の見出し）。HTML のツール判定（Describe inputs with Zod）は誤りで、anchored_url は #add-tool-annotations にした。

<a id="g-c08-frameworks-25"></a>
#### C08-25 mcp-use — mcp-use（TypeScript サーバー docs）

- **資料**: mcp-use docs — Tools: Add tool annotations（SDK の文書）
- **URL**: https://docs.mcp-use.com/typescript/server/tools#add-tool-annotations
- **照らし合わせた中身の URL**: https://docs.mcp-use.com/typescript/server/tools
- **版**: docs.mcp-use.com（2026-10-02 取得）
- **書いてある場所**: Tools > Add tool annotations (#add-tool-annotations)
- **原文**:

> Use readOnlyHint: false for tools that create, update, delete, send, purchase, deploy, or otherwise change state. Use destructiveHint: true when the change can remove data or is hard to undo.

- **日本語**: 作成・更新・削除・送信・購入・デプロイなど状態を変えるツールには readOnlyHint: false を使う。変更でデータが消えうる、または元に戻しにくいときは destructiveHint: true を使う。
- **どう使っているか**: どのヒントをいつ立てるかの具体的な基準。直後の文: idempotentHint は同じ呼び出しを繰り返しても 1 回と同じ効果のときだけ true（目視）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Add tool annotations」（取得 2026-10-02T22:11:27Z、sha256 c84a9dfde1b5…）

### mcp-use — mcp-use（TypeScript クライアント: AI SDK アダプタ）

<a id="g-c08-frameworks-26"></a>
#### C08-26 mcp-use — mcp-use（TypeScript クライアント: AI SDK アダプタ）

- **資料**: libraries/typescript/packages/client/src/adapters/ai-sdk.ts（SDK のソースコード）
- **URL**: https://github.com/mcp-use/mcp-use/blob/bde34336cb6cff3e10fb9c4b1d67850be57e6ad6/libraries/typescript/packages/client/src/adapters/ai-sdk.ts#L136-L172
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mcp-use/mcp-use/bde34336cb6cff3e10fb9c4b1d67850be57e6ad6/libraries/typescript/packages/client/src/adapters/ai-sdk.ts
- **版**: mcp-use/mcp-use@bde3433（2026-09-30）
- **書いてある場所**: lines 143-145（一致 143-145 と 168-170 行の 2 か所）
- **原文**:

> ...(mcpTool.annotations !== undefined ? { annotations: mcpTool.annotations } : {}),

- **日本語**: annotations が定義されていれば、そのまま annotations として載せる。
- **どう使っているか**: MCP ツールを AI SDK の dynamic tool に変えるとき、annotations を metadata とツール定義の両方にそのまま写す（143-145 行と 168-170 行の 2 か所）。title は title ?? annotations?.title（136 行、目視）。承認には使わない。
- **扱う宣言**: title・宣言全般 ／ **使い方の分類**: そのまま渡す・見せる・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・2 か所、143-145 行（取得 2026-10-02T22:11:35Z、sha256 d24ddf746ffe…）

### LangChain4j — LangChain4j (langchain4j-mcp)

<a id="g-c08-frameworks-27"></a>
#### C08-27 LangChain4j — LangChain4j (langchain4j-mcp)

- **資料**: langchain4j-mcp/src/main/java/dev/langchain4j/mcp/client/ToolSpecificationHelper.java — processMcpToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/langchain4j/langchain4j/blob/7d5a0bccb59c3153c656e458a36dea0a2d22cea3/langchain4j-mcp/src/main/java/dev/langchain4j/mcp/client/ToolSpecificationHelper.java#L406-L424
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/langchain4j/langchain4j/7d5a0bccb59c3153c656e458a36dea0a2d22cea3/langchain4j-mcp/src/main/java/dev/langchain4j/mcp/client/ToolSpecificationHelper.java
- **版**: langchain4j/langchain4j@7d5a0bc（2026-10-02）
- **書いてある場所**: lines 406-409
- **原文**:

> private static void processMcpToolAnnotations(Map<String, Object> annotations, ToolSpecification.Builder builder) { if (annotations.containsKey(DESTRUCTIVE_HINT)) { builder.addMetadata(DESTRUCTIVE_HINT, bool(annotations.get(DESTRUCTIVE_HINT))); }

- **日本語**: 注釈に destructiveHint があれば ToolSpecification の metadata に destructiveHint として加える（idempotentHint・openWorldHint・readOnlyHint も同様）。
- **どう使っているか**: MCP の注釈を LangChain4j の ToolSpecification.metadata() に写す。title は 'title-annotation' という別キーにする（McpToolMetadataKeys.java 16 行、目視）。承認などに使うコードはこの調査では見ていない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、406-409 行（取得 2026-10-02T22:11:34Z、sha256 9229bbdf7219…）
- **補足**: C02 の調査で LangChain4j の MCP チュートリアル docs には注釈の記述が無い（checked_no_mention）。コードでは写している。

### JetBrains — Koog (agents-mcp-server)

<a id="g-c08-frameworks-28"></a>
#### C08-28 JetBrains — Koog (agents-mcp-server)

- **資料**: agents/agents-mcp-server/src/commonMain/kotlin/ai/koog/agents/mcp/server/McpServer.kt — asSdkTool（SDK のソースコード）
- **URL**: https://github.com/JetBrains/koog/blob/16d83270f8a7f25358ae0165466f14e70416c428/agents/agents-mcp-server/src/commonMain/kotlin/ai/koog/agents/mcp/server/McpServer.kt#L199-L214
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/JetBrains/koog/16d83270f8a7f25358ae0165466f14e70416c428/agents/agents-mcp-server/src/commonMain/kotlin/ai/koog/agents/mcp/server/McpServer.kt
- **版**: JetBrains/koog@16d8327（2026-09-24）
- **書いてある場所**: lines 211-213
- **原文**:

> outputSchema = null, annotations = null, title = null,

- **日本語**: outputSchema = null, annotations = null, title = null
- **どう使っているか**: Koog のツールを MCP サーバーとして公開するとき、annotations は常に null（宣言しない）。仕様上は既定値（readOnlyHint: false, destructiveHint: true, idempotentHint: false, openWorldHint: true）として解釈されるが、実際にどう扱うかは受け取るクライアント次第。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、211-213 行（取得 2026-10-02T22:11:28Z、sha256 906ebcbaffb9…）
- **補足**: 「クライアントは仕様の既定値で扱うことになる」は言い過ぎ（既定値は仕様上の解釈で、クライアントの実装は様々）。usage_ja を直した。

### AG2 (ag2ai) — AG2（ag2.mcp: エージェントを MCP サーバーとして公開）

<a id="g-c08-frameworks-29"></a>
#### C08-29 AG2 (ag2ai) — AG2（ag2.mcp: エージェントを MCP サーバーとして公開）

- **資料**: AG2 docs — MCP-UI Resources: Serving a UI resource（SDK の文書）
- **URL**: https://docs.ag2.ai/docs/user-guide/tools/mcp_ui/#serving-a-ui-resource
- **照らし合わせた中身の URL**: https://docs.ag2.ai/docs/user-guide/tools/mcp_ui/
- **版**: docs.ag2.ai（2026-10-02 取得）
- **書いてある場所**: MCP-UI Resources > Serving a UI resource (#serving-a-ui-resource)
- **原文**:

> Optional title and annotations keyword arguments are advertised in tools/list; annotations takes mcp.types.ToolAnnotations behavior hints (readOnlyHint, destructiveHint, …) that hosts use to decide e.g. whether to confirm with the user before calling

- **日本語**: 任意の title と annotations の引数は tools/list で広告される。annotations は mcp.types.ToolAnnotations の動作ヒント（readOnlyHint, destructiveHint, …）を受け取り、ホストはこれを使って、たとえば呼び出し前に利用者に確認するかを決める。
- **どう使っているか**: サーバー作者向けの説明で、ホストが確認の要否に使うという期待を述べる（例 @mcp_tool(annotations=ToolAnnotations(readOnlyHint=True))）。AG2 自身のクライアント（MCPToolkit）は注釈を使わない（checked_no_mention）。
- **扱う宣言**: readOnlyHint・destructiveHint・title ／ **使い方の分類**: 作者への書き方の案内・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP-UI Resources > Serving a UI resource」（取得 2026-10-02T22:11:23Z、sha256 d17567a082dd…）
- **補足**: ソース website/docs/user-guide/tools/mcp_ui.mdx 55-56 行（ag2ai/ag2@2c967d0）でも exact（id q29s）。コードの docstring（ag2/mcp/tools.py 146-150 行・339-340 行、目視）も同じ説明。

### Pydantic — Pydantic AI Harness（MCP 連携の capability）

<a id="g-c08-frameworks-30"></a>
#### C08-30 Pydantic — Pydantic AI Harness（MCP 連携の capability）

- **資料**: src/pydantic_ai_harness/pydantic_ai_harness/_mcp.py — is_read_only（SDK のソースコード）
- **URL**: https://github.com/pydantic/pydantic-ai/blob/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/_mcp.py#L28-L34
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/pydantic/pydantic-ai/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/_mcp.py
- **版**: pydantic/pydantic-ai@6bc07cf（2026-10-01）
- **書いてある場所**: lines 28-34
- **原文**:

> def is_read_only(tool: ToolDefinition) -> bool: """Whether the server explicitly marks a tool read-only.""" match (tool.metadata or {}).get('annotations'): case {'readOnlyHint': True}: return True case _: return False

- **日本語**: サーバーがツールを明示的に読み取り専用と印付けしているか。annotations が {'readOnlyHint': True} に当たれば True、それ以外は False。
- **どう使っているか**: read_only=True の capability は、この関数で readOnlyHint: true のツールだけを残す。注釈なし・readOnlyHint 未設定は「読み取り専用でない」扱いで外される。常にこの注釈フィルタを使うのは Notion / Slack / Google Workspace / Logfire MCP / Pylon / Grain。GitHub / Linear / PostHog は既定ではサーバー側の読み取り専用モード（ヘッダや専用エンドポイント）を使い、利用者が client を渡したときだけこの注釈フィルタになる。
- **条件**: 各 capability の read_only=True のとき（既定は read_only: bool = False、notion/_capability.py 40 行ほか、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、28-34 行（取得 2026-10-02T22:11:37Z、sha256 7a28747889ce…）
- **補足**: 使用箇所（grep、6bc07cf）: notion/_capability.py 69 行、slack/_capability.py 68 行（exact、68 行、検証者 id v_pyd_slack）、google_workspace/_capability.py 94 行、logfire_mcp/_capability.py 83 行、pylon/_capability.py 108 行、grain/_capability.py 103 行（exact、103 行、検証者 id v_pyd_grain）。client を渡したときだけ: linear/_capability.py 66 行（`if self.client is not None:` の中、exact、66 行、検証者 id v_pyd_linear）、github/_capability.py 79 行、posthog/_capability.py 122 行。サーバー側モードの説明は HOSTED-INTEGRATIONS.md 99-100 行（exact、99-100 行、検証者 id v_pyd_server_mode）。 usage_ja の一覧に Linear が「注釈で絞る capability」として入っていたが、Linear（と GitHub / PostHog）は client を渡したときだけ注釈フィルタで、既定はサーバー側モード。Slack と Grain の使用箇所が notes から漏れていたので足した（exact）。

### Pydantic — Pydantic AI Harness（Notion capability）

<a id="g-c08-frameworks-31"></a>
#### C08-31 Pydantic — Pydantic AI Harness（Notion capability）

- **資料**: Pydantic AI docs — Harness: Notion, Tool selection and approval（SDK の文書）
- **URL**: https://pydantic.dev/docs/ai/harness/notion/#tool-selection-and-approval
- **照らし合わせた中身の URL**: https://pydantic.dev/docs/ai/harness/notion/
- **版**: pydantic.dev（2026-10-02 取得）
- **書いてある場所**: Notion > Tool selection and approval (#tool-selection-and-approval)
- **原文**:

> read_only=True keeps only the tools the server marks as read-only. If the server does not mark its read tools, this can leave none. The credential is still what controls access.

- **日本語**: read_only=True にすると、サーバーが読み取り専用と印付けしたツールだけを残す。サーバーが読み取りツールに印を付けていなければ、何も残らないことがある。アクセスを制御するのはあくまで資格情報。
- **どう使っているか**: 利用者向け docs での説明。注釈は絞り込みに使うが、権限の境界は資格情報（トークンのスコープ）だと明記。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Notion > Tool selection and approval」（取得 2026-10-02T22:11:38Z、sha256 006a311ea7fc…）
- **補足**: 同じ文が Google Workspace / Logfire MCP / Slack のページにもある（repo の docs/harness/*.md の grep）。

### Pydantic — Pydantic AI Harness（hosted MCP 連携の共通説明）

<a id="g-c08-frameworks-32"></a>
#### C08-32 Pydantic — Pydantic AI Harness（hosted MCP 連携の共通説明）

- **資料**: pydantic-ai-harness skill reference — HOSTED-INTEGRATIONS.md: read_only（SDK の文書）
- **URL**: https://github.com/pydantic/pydantic-ai/blob/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/.agents/skills/pydantic-ai-harness/references/HOSTED-INTEGRATIONS.md#L97-L106
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/pydantic/pydantic-ai/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_ai_harness/pydantic_ai_harness/.agents/skills/pydantic-ai-harness/references/HOSTED-INTEGRATIONS.md
- **版**: pydantic/pydantic-ai@6bc07cf
- **書いてある場所**: lines 101-103（Markdown 見出し ### `read_only`）
- **原文**:

> Keeps only tools whose MCP annotations set `readOnlyHint: true`. Unmarked tools are dropped, so a server that does not annotate can leave the agent with no tools.

- **日本語**: MCP の注釈で readOnlyHint: true のツールだけを残す。印の無いツールは落とされるので、注釈を付けないサーバーではエージェントにツールが 1 つも残らないことがある。
- **どう使っているか**: read_only の 2 方式: GitHub（X-MCP-Readonly ヘッダ）・Linear（/mcp/readonly）・PostHog（x-posthog-read-only）はサーバー側のモード、それ以外（と client を渡したとき）は注釈による絞り込み（99-103 行、目視）。直後に「read_only is not an access boundary. The token's scopes are.」（105 行、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、101-103 行（### `read_only`）（取得 2026-10-02T22:11:34Z、sha256 d2498b0b7734…）
- **補足**: 公開 docs の GitHub ページ: 「With a client, read_only=True keeps only the tools the server marks as read-only, instead of asking the server for read-only mode.」（https://pydantic.dev/docs/ai/harness/github/#connection-customization、exact、id q37）。この md はコーディングエージェント向けの skill の参照資料。　【検証者】99-100 行のサーバー側モードの文（exact、99-100 行、検証者 id v_pyd_server_mode）と 105 行「`read_only` is not an access boundary. The token's scopes are.」（exact、105 行、検証者 id v_pyd_boundary）も exact で確認した（発見者は目視）。 解釈は正しい。発見者が目視とした 2 文を exact で確認しただけ。

### Pydantic — CLAI 2.0（pydantic_clai2: Pydantic AI の端末クライアント）

<a id="g-c08-frameworks-33"></a>
#### C08-33 Pydantic — CLAI 2.0（pydantic_clai2: Pydantic AI の端末クライアント）

- **資料**: src/pydantic_clai2/pydantic_clai2/runtime/speculative_mode.py — _declarations（クライアントのソースコード）
- **URL**: https://github.com/pydantic/pydantic-ai/blob/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_clai2/pydantic_clai2/runtime/speculative_mode.py#L260-L276
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/pydantic/pydantic-ai/6bc07cf18b0641ea92343d8c589cfb922108b802/src/pydantic_clai2/pydantic_clai2/runtime/speculative_mode.py
- **版**: pydantic/pydantic-ai@6bc07cf
- **書いてある場所**: lines 263-265
- **原文**:

> Only a `SPECULATIVE_TOOLS` entry from its expected capability is declared read-only; every other tool's own `read_only` or MCP `readOnlyHint` claim is overridden, so the allowlist stays Code Puppy's rather than whatever a plugin or MCP server says about itself.

- **日本語**: SPECULATIVE_TOOLS に載っていて期待する capability から来たツールだけを読み取り専用と宣言する。他のツール自身の read_only や MCP の readOnlyHint の主張は上書きされ、許可リストはプラグインや MCP サーバーが自分について言うことではなく、こちらのものになる。
- **どう使っているか**: CodeMode の speculate='declared'（readOnlyHint を信じて先回り実行する機能、C02_sdks-58）を CLI で使うとき、MCP サーバーの readOnlyHint を信じない。信頼しないツールは readOnlyHint: False に書き換える（274-275 行 `if annotations and not trusted: metadata['annotations'] = {**annotations, 'readOnlyHint': False}`、exact、id q33b）。
- **条件**: CLAI 2.0 の speculative mode のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、263-265 行（取得 2026-10-02T22:13:00Z、sha256 13ddc9019471…）
- **補足**: 【検証者】ファイル冒頭「Speculative CodeMode wiring, ported from Code Puppy's `enable_speculative_code_mode`.」（exact、1 行、検証者 id v_clai_codepuppy）。引用中の『Code Puppy』は移植元の別プロジェクトで、許可リスト（SPECULATIVE_TOOLS）の出どころ。pydantic_clai2 の公開状況（リリース済みか）は不明。 解釈は正しい。引用に出る Code Puppy が移植元であることと、公開状況が不明であることを notes に足した。

### Pydantic — Pydantic AI Harness（Day AI capability）

<a id="g-c08-frameworks-34"></a>
#### C08-34 Pydantic — Pydantic AI Harness（Day AI capability）

- **資料**: Pydantic AI docs — Harness: Day AI, Tool selection and approval（SDK の文書）
- **URL**: https://pydantic.dev/docs/ai/harness/day-ai/#tool-selection-and-approval
- **照らし合わせた中身の URL**: https://pydantic.dev/docs/ai/harness/day-ai/
- **版**: pydantic.dev（2026-10-02 取得）
- **書いてある場所**: Day AI > Tool selection and approval (#tool-selection-and-approval)
- **原文**:

> Day AI's server does not mark any tool as read-only, so there is no read_only option: the agent gets every tool your tier and role allow, including ones that change CRM records and send notifications.

- **日本語**: Day AI のサーバーはどのツールも読み取り専用と印付けしないので、read_only オプションは無い。エージェントは、CRM レコードを変えたり通知を送ったりするものも含め、利用者のプランと役割が許すすべてのツールを得る。
- **どう使っているか**: サーバーが readOnlyHint を宣言しないと、注釈による読み取り専用の絞り込み自体が提供されない例（宣言の欠落が機能の欠落になる）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Day AI > Tool selection and approval」（取得 2026-10-02T22:11:30Z、sha256 34e25f50b751…）
- **補足**: 【検証者】『Day AI のサーバーはどのツールにも read-only の印を付けない』は Pydantic の docs の記述で、Day AI のサーバー側では確かめていない。 引用が Day AI ではなく Pydantic の docs の主張であることを notes に明記。

### VoltAgent — VoltAgent (@voltagent/mcp-server)

<a id="g-c08-frameworks-35"></a>
#### C08-35 VoltAgent — VoltAgent (@voltagent/mcp-server)

- **資料**: packages/mcp-server/src/adapters/tool.ts — toMcpTool（SDK のソースコード）
- **URL**: https://github.com/VoltAgent/voltagent/blob/72a46c76b4507e1f98b41d5050a92bd30587eb70/packages/mcp-server/src/adapters/tool.ts#L10-L30
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/VoltAgent/voltagent/72a46c76b4507e1f98b41d5050a92bd30587eb70/packages/mcp-server/src/adapters/tool.ts
- **版**: VoltAgent/voltagent@72a46c7（2026-09-27）
- **書いてある場所**: lines 23-26
- **原文**:

> annotations: { title: title ?? tool.name, ...tool.mcp?.annotations, },

- **日本語**: annotations: { title: title ?? tool.name, ...tool.mcp?.annotations }
- **どう使っているか**: VoltAgent のツールを MCP で公開するとき、作者がツール定義の mcp.annotations に書いたヒントをそのまま載せる。書かなければ title だけ（既定値は埋めない）。
- **扱う宣言**: title・宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、23-26 行（取得 2026-10-02T22:11:32Z、sha256 8b84e317afba…）
- **補足**: 【検証者】エージェントとワークフローを MCP ツールとして公開するときは、annotations に title しか入らない（packages/mcp-server/src/adapters/agent.ts 64-66 行 `annotations: { title: agent.name, },`、exact、64-66 行、検証者 id v_volt_agent。workflow.ts 62-64 行・225-227 行も title だけ、目視）。Agno（C08_frameworks-11）と違い、既定のヒントを付けない。 usage から author_guidance_how_to_set を外した（コードは作者が書いた値を載せるだけで、指針は述べていない）。エージェント / ワークフローの公開では title だけになることを exact で足した。

### Google — Gemini アプリ（消費者向け。Connected Apps の custom app = 任意の remote MCP サーバー、Gemini Spark でも使う）

<a id="g-g3-consumer-apps-model-apis-01"></a>
#### G3CAMA-01 Google — Gemini アプリ（消費者向け。Connected Apps の custom app = 任意の remote MCP サーバー、Gemini Spark でも使う）

- **資料**: Connect & manage custom apps for Gemini Apps（Gemini Apps Help）（公式の文書）
- **URL**: https://support.google.com/gemini/answer/17209137?hl=en
- **書いてある見出しへ直接**: https://support.google.com/gemini/answer/17209137?hl=en#risks
- **版**: ページの日付表示なし（2026-10-02 取得）
- **書いてある場所**: Connect & manage custom apps for Gemini Apps > Understand risks of connecting custom Connected Apps（#risks）
- **原文**:

> Currently, Gemini requires manual confirmation for any write actions, but Gemini can make mistakes.

- **日本語**: 現時点で、Gemini は書き込みの操作すべてに手動の確認を求める。ただし Gemini は間違えることがある。
- **どう使っているか**: 消費者向け Gemini アプリは custom MCP サーバーの「書き込みの操作」に毎回手動の確認を求める、とだけ書く。何を「書き込み」と判定するか（readOnlyHint / destructiveHint を見るのか、Gemini 自身が判断するのか）は書かれていない（不明）。
- **条件**: 個人の Google アカウント・18 歳以上・米国・英語・Keep Activity オン。custom app は Gemini ウェブ版で接続し、モバイル版でも使える。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect & manage custom apps for Gemini Apps > Understand risks of connecting custom Connected Apps」（取得 2026-10-02T22:11:36Z、sha256 c91ed65ae729…）
- **補足**: 同じページと Spark のページ（17094507, 17171264）で readOnlyHint / destructiveHint は none、annotation はページの script の中にだけ 1 件（本文には無い。checked_no_mention）。Gemini Enterprise（C06_google_aws-19/20）は「readOnlyHint があれば確認を省く」と書くが、消費者向けアプリについて同じ扱いかを書いた一次資料は見つからなかった。「Currently」とあるので将来変わりうる。

### Google — Gemini Spark（Gemini アプリのエージェント機能。Connected Apps / custom app を使う）

<a id="g-g3-consumer-apps-model-apis-02"></a>
#### G3CAMA-02 Google — Gemini Spark（Gemini アプリのエージェント機能。Connected Apps / custom app を使う）

- **資料**: Use Gemini Spark to manage your tasks & workflows in Gemini Apps（Gemini Apps Help）（公式の文書）
- **URL**: https://support.google.com/gemini/answer/17094507?hl=en
- **書いてある見出しへ直接**: https://support.google.com/gemini/answer/17094507?hl=en#risks_safety
- **版**: ページの日付表示なし（2026-10-02 取得）
- **書いてある場所**: Use Gemini Spark to manage your tasks & workflows in Gemini Apps > How Gemini Spark works with you to keep you & your info safe > Gemini can share your info with websites（#risks_safety）
- **原文**:

> Gemini is designed to ask for your review and confirmation before it completes certain actions, such as: Sending communications, modifying your data, making purchases, and submitting web forms.

- **日本語**: Gemini は、ある種の操作を終える前にあなたの確認を求めるよう作られている。たとえば、連絡を送る、データを変更する、購入する、ウェブのフォームを送信する。
- **どう使っているか**: Spark の確認は操作の種類（送信・データ変更・購入・フォーム送信）で書かれており、MCP の注釈との関係は書かれていない（不明）。
- **条件**: Gemini Spark 利用時。スケジュール実行中にオフラインだと止められない場合があるとも書く。 ページ自身が「Gemini can make mistakes」「Some tasks may require your confirmation」と留保を付ける（確認が必ず出る保証ではない）。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Use Gemini Spark to manage your tasks & workflows in Gemini Apps > How Gemini Spark works with you to keep you & your info safe > Gemini can share your info with websites」（取得 2026-10-02T22:12:08Z、sha256 48225b093469…）
- **補足**: 引用は箇条書きの 1 項目を含めて 1 文につないだもの（tool は空白の違いを無視して exact）。同ページは「Gemini can perform bulk actions on private tasks in Google Tasks without your confirmation」とも書く（Google 自身のサービスには確認なしの操作もある）。annotations の語は本文に無い（checked_no_mention）。 解釈の補足：同ページは別の節で「Some tasks may require your confirmation before Gemini completes them.」とも書き、確認は「designed to」（そう作られている）であって保証ではない。conditions を補った。

### xAI（SpaceXAI） — xAI API の Remote MCP Tools（Responses API 互換・xAI native SDK・Speech to Speech API）

<a id="g-g3-consumer-apps-model-apis-03"></a>
#### G3CAMA-03 xAI（SpaceXAI） — xAI API の Remote MCP Tools（Responses API 互換・xAI native SDK・Speech to Speech API）

- **資料**: Remote MCP Tools（公式の文書）
- **URL**: https://docs.x.ai/developers/tools/remote-mcp
- **照らし合わせた中身の URL**: https://docs.x.ai/developers/tools/remote-mcp.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 13 行目（## SDK Support）
- **原文**:

> The `require_approval` and `connector_id` parameters in the OpenAI Responses API are not currently supported.

- **日本語**: OpenAI Responses API の require_approval と connector_id の引数は、今のところ対応していない。
- **どう使っているか**: このページは OpenAI 互換の require_approval（と connector_id）は今のところ対応していないと書くだけで、ほかの承認（人の確認）の仕組みも書いていない。したがって、このページの範囲では、注釈を見て確認を切り替える場所は無い（xAI 側が今後どうするかは不明）。ページに readOnlyHint / annotations の語は無い（checked_no_mention）。
- **条件**: サーバー側実行の remote MCP（Streamable HTTP / SSE）。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（## SDK Support）（取得 2026-10-02T22:11:29Z、sha256 10e992ef4488…）
- **補足**: 公開 URL は JS 描画なので .md 版（https://docs.x.ai/developers/tools/remote-mcp.md）で照合。旧 URL https://docs.x.ai/docs/guides/tools/remote-mcp-tools は同ページへリダイレクト。WebSearch の要約は「送っても無視される」と書いていたが、その文はこのページに無い（未確認）。 usage_ja の「承認の仕組み自体を持たない」は言い過ぎなので、「このページは require_approval 未対応と書き、ほかの承認の仕組みも書いていない」に弱めた。

### xAI（SpaceXAI） — xAI API の Remote MCP Tools

<a id="g-g3-consumer-apps-model-apis-04"></a>
#### G3CAMA-04 xAI（SpaceXAI） — xAI API の Remote MCP Tools

- **資料**: Remote MCP Tools（公式の文書）
- **URL**: https://docs.x.ai/developers/tools/remote-mcp
- **照らし合わせた中身の URL**: https://docs.x.ai/developers/tools/remote-mcp.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 158 行目（## Tool Enablement and Access Control）
- **原文**:

> **Reduced Risk**: For example, restrict access to tools that only perform read-only operations to prevent the model from modifying data

- **日本語**: 危険を減らす：たとえば、読み取りだけを行うツールに限ってアクセスを許し、モデルがデータを変えないようにする。
- **どう使っているか**: 読み取り専用に絞る手段は、API 利用者が allowed_tools（native SDK では allowed_tool_names）にツール名を手で並べること。注釈から自動で絞る仕組みは書かれていない。
- **条件**: allowed_tools を指定しない場合はサーバーの全ツールがモデルに渡る（同ページ）。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、158 行（## Tool Enablement and Access Control）（取得 2026-10-02T22:11:29Z、sha256 10e992ef4488…）
- **補足**: どのツールが「read-only」かの判断は利用者まかせで、readOnlyHint には触れない。

### xAI — xai-sdk-python（xAI 公式 Python SDK）の mcp() ツール

<a id="g-g3-consumer-apps-model-apis-05"></a>
#### G3CAMA-05 xAI — xai-sdk-python（xAI 公式 Python SDK）の mcp() ツール

- **資料**: src/xai_sdk/tools.py（SDK のソースコード）
- **URL**: https://github.com/xai-org/xai-sdk-python/blob/1d9e1dffc9a0521ede0e6bc7f2b906177b940d34/src/xai_sdk/tools.py#L291-L322
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/xai-org/xai-sdk-python/1d9e1dffc9a0521ede0e6bc7f2b906177b940d34/src/xai_sdk/tools.py
- **版**: commit 1d9e1dffc9a0521ede0e6bc7f2b906177b940d34（HEAD, 2026-10-02）
- **書いてある場所**: 309 行目
- **原文**:

> allowed_tool_names: The names of the tools that the model is allowed to call. If empty, all tools are allowed.

- **日本語**: allowed_tool_names：モデルが呼んでよいツールの名前。空ならすべて許す。
- **どう使っているか**: mcp() の引数は server_url / server_label / server_description / allowed_tool_names / authorization / extra_headers だけで、承認や注釈に当たる引数は無い。リポジトリ全体でも readOnlyHint / destructiveHint は 0 件（grep）。
- **条件**: サーバー側ツール（agentic requests）として使う。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、309 行（取得 2026-10-02T22:13:01Z、sha256 296501690ec5…）
- **補足**: xai-sdk-ts（commit 674d8342…）も readOnlyHint / destructiveHint は 0 件（grep。annotations の語は生成型の別用途のみ）。

### xAI — Grok Build（xAI のコーディング CLI。grok コマンド）の Plan mode

<a id="g-g3-consumer-apps-model-apis-06"></a>
#### G3CAMA-06 xAI — Grok Build（xAI のコーディング CLI。grok コマンド）の Plan mode

- **資料**: Plan Mode（Grok Build docs）（公式の文書）
- **URL**: https://docs.x.ai/build/features/plan-mode
- **照らし合わせた中身の URL**: https://docs.x.ai/build/features/plan-mode.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 37 行目（## Caveats）
- **原文**:

> Only the session plan file may be edited until you approve. Other edit tools are rejected, including under auto or always-approve. Reads, bash, and MCP still follow [permission mode](/build/features/permissions).

- **日本語**: 承認するまで編集できるのはセッションの計画ファイルだけ。他の編集ツールは auto や always-approve でも拒否される。読み取り・bash・MCP は引き続き権限モードに従う。
- **どう使っているか**: Plan mode が止めるのは組み込みの編集ツールだけで、MCP ツールは読み取りか書き込みかに関係なく通常の権限モードで扱う、と明記。readOnlyHint を見て plan mode で通す／止めるという記述は無い。
- **条件**: Plan mode（/plan, Shift+Tab）。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、37 行（## Caveats）（取得 2026-10-02T22:11:35Z、sha256 f4a1a7ce7cc3…）
- **補足**: 公式 URL は https://docs.x.ai/build/features/plan-mode（.md で照合）。Grok CLI 1.0.46 の Linux バイナリ（https://x.ai/cli/grok-1.0.46-linux-x86_64.gz、展開後 sha256 41626a53292324140b92556b9d42ff5542e3dcd04aff85eafb8689dd4adb44fc）は Rust 製で、文字列 readOnlyHint / destructiveHint は rmcp 3.4.0 の ToolAnnotations 構造体（serde のフィールド名）としてだけ現れる。権限の判定がそれを読むかはストリップ済みバイナリから判定できない（不明）。

### xAI — Grok Build の権限（Permissions）

<a id="g-g3-consumer-apps-model-apis-07"></a>
#### G3CAMA-07 xAI — Grok Build の権限（Permissions）

- **資料**: Permissions（Grok Build docs）（公式の文書）
- **URL**: https://docs.x.ai/build/features/permissions
- **照らし合わせた中身の URL**: https://docs.x.ai/build/features/permissions.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 41 行目（## Allow and deny rules）
- **原文**:

> Supported filters include `Bash`, `Edit`, `Read`, `Grep`, `MCPTool`, `WebFetch`, and `WebSearch`. `deny` always wins over `allow`.

- **日本語**: 使えるフィルタは Bash, Edit, Read, Grep, MCPTool, WebFetch, WebSearch。deny は常に allow より優先。
- **どう使っているか**: MCP ツールの許可は MCPTool のパターン規則（名前）で書く。Auto モードは「分類器が安全なツールを自動承認」と書くが、その分類に注釈を使うかは書かれていない（不明）。注釈の語はページに無い。
- **条件**: Ask（既定）/ Auto（機能フラグ）/ Always-approve の 3 モード。
- **扱う宣言**:  ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、41 行（## Allow and deny rules）（取得 2026-10-02T22:11:28Z、sha256 c5bad5c416aa…）
- **補足**: 同じ表の Auto 行：「Classifier auto-approves safe tools; dangerous ones may still prompt」。Enterprise では Claude Code の managed-settings.json の許可規則と MCP 許可リストも読む（docs.x.ai/build/enterprise）。

### xAI — Grok Bot（xAI のエージェント製品。ツール呼び出しの承認と Auto Review）

<a id="g-g3-consumer-apps-model-apis-08"></a>
#### G3CAMA-08 xAI — Grok Bot（xAI のエージェント製品。ツール呼び出しの承認と Auto Review）

- **資料**: Approvals, security, and privacy（Grok Bot docs）（公式の文書）
- **URL**: https://docs.x.ai/grok-bot/approvals-security-and-privacy
- **照らし合わせた中身の URL**: https://docs.x.ai/grok-bot/approvals-security-and-privacy.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 62-64 行目（## Configure Auto Review）
- **原文**:

> Avoid broad rules such as “allow everything in the browser.” Websites and tool behavior change over time. Auto Review is model-based and should complement, not replace, least privilege and explicit approval boundaries.

- **日本語**: 「ブラウザの中なら何でも許可」のような広い規則は避ける。サイトやツールの振る舞いは時とともに変わる。Auto Review はモデルによる判定で、最小権限と明示的な承認の境界を補うもので、置き換えるものではない。
- **どう使っているか**: Grok Bot の承認はユーザーが書く Ask first / Allow automatically 規則と、モデルによる Auto Review。MCP の注釈を使うという記述は無い（checked_no_mention）。
- **条件**: Settings → General → Auto-review。チーム管理者が強制できる。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、62-64 行（## Configure Auto Review）（取得 2026-10-02T22:11:26Z、sha256 37a876b1ff2f…）
- **補足**: 同ページ：「Keep sending, publishing, purchasing, deletion, and production changes behind approval.」（利用者への勧め）。 このページには MCP の語が出ない（connectors と tool calls の話）。また同ページの privacy の節は「Cursor account」「Cursor Privacy Policy」など Cursor の規約を参照している（xAI の製品文書なのに Cursor を参照する理由は不明）。 notes に、このページは MCP に触れないこと、Cursor の規約を参照していることを足した（Auto Review が MCP ツールに効くかはこのページからは不明）。

### Groq — Groq API の Remote MCP（Responses API）

<a id="g-g3-consumer-apps-model-apis-09"></a>
#### G3CAMA-09 Groq — Groq API の Remote MCP（Responses API）

- **資料**: Remote Tools and Model Context Protocol (MCP)（GroqDocs）（公式の文書）
- **URL**: https://console.groq.com/docs/tool-use/remote-mcp
- **照らし合わせた中身の URL**: https://console.groq.com/docs/tool-use/remote-mcp.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 871 行目（### [Approvals Flow](#approvals-flow)）
- **原文**:

> You can also set `require_approval` to "never", which will cause the model to execute the tool call without human approval. This is the default behavior if `require_approval` is not set.

- **日本語**: require_approval を "never" にすると、モデルは人の承認なしにツールを実行する。require_approval を指定しないときもこれが既定の動き。
- **どう使っているか**: Groq の remote MCP は、require_approval を指定しなければ承認なしでツールを実行する（このページの記述）。承認の要否は注釈ではなく API 呼び出し側の require_approval で決まる。同ページは「OpenAI の remote MCP 仕様と完全互換」と書くが、OpenAI の文書（C05）の既定は承認あり側なので、既定値は互換でない（OpenAI 側の既定は C05 の記録による）。
- **条件**: require_approval 未指定のとき。
- **扱う宣言**:  ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、871 行（### [Approvals Flow](#approvals-flow)）（取得 2026-10-02T22:12:44Z、sha256 880e7a84cea5…）
- **補足**: ページに readOnlyHint / destructiveHint / annotation は無い（checked_no_mention）。公式 URL は https://console.groq.com/docs/tool-use/remote-mcp（.md で照合）。 「OpenAI の既定と逆」はこのページの記述ではなく C05 の OpenAI 文書との比較なので、出典を書き分けた。

<a id="g-g3-consumer-apps-model-apis-10"></a>
#### G3CAMA-10 Groq — Groq API の Remote MCP（Responses API）

- **資料**: Remote Tools and Model Context Protocol (MCP)（GroqDocs）（公式の文書）
- **URL**: https://console.groq.com/docs/tool-use/remote-mcp
- **照らし合わせた中身の URL**: https://console.groq.com/docs/tool-use/remote-mcp.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: 843 行目（### [Approvals Flow](#approvals-flow)）
- **原文**:

> If `require_approval` is set to "always", the Groq API will wait for human approval before executing the tool call.

- **日本語**: require_approval が "always" なら、Groq API はツールを実行する前に人の承認を待つ。
- **どう使っているか**: 承認は "always" / "never" の指定（例として挙がっているのはこの 2 値）で、ツールごとの性質（readOnlyHint など）で切り替える仕組みは書かれていない。
- **条件**: require_approval:"always" のとき mcp_approval_request を返し、mcp_approval_response で承認・拒否する。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、843 行（### [Approvals Flow](#approvals-flow)）（取得 2026-10-02T22:12:44Z、sha256 880e7a84cea5…）
- **補足**: 同ページの表：「require_approval: Whether human approval is required for the tool call (e.g. "never", "always")」。OpenAI の filter 形式（ツール名の always/never）に対応するかはこのページに書かれていない（不明）。MCP Connectors のページは「Google Workspace (read-only) connectors」と書き、例はすべて require_approval:"never"。ただし Google Calendar の必要 scope は calendar.events（読み書きの scope）で、Gmail / Drive だけが .readonly。 notes の「読み取り専用スコープの connector だけ」を訂正：Calendar の scope は calendar.events（readonly ではない）。

### Google — google-genai（Python SDK, python-genai）の MCP ツール変換

<a id="g-g3-consumer-apps-model-apis-11"></a>
#### G3CAMA-11 Google — google-genai（Python SDK, python-genai）の MCP ツール変換

- **資料**: google/genai/_mcp_utils.py: mcp_to_gemini_tool（SDK のソースコード）
- **URL**: https://github.com/googleapis/python-genai/blob/6d13650a0539a39a16e452d0e38c15a31b3b990d/google/genai/_mcp_utils.py#L48-L65
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleapis/python-genai/6d13650a0539a39a16e452d0e38c15a31b3b990d/google/genai/_mcp_utils.py
- **版**: commit 6d13650a0539a39a16e452d0e38c15a31b3b990d（HEAD, 2026-10-02）
- **書いてある場所**: 52-55 行目（# limitations under the License.）
- **原文**:

> function_declarations=[{ "name": tool.name, "description": tool.description, "parameters": types.Schema.from_json_schema(

- **日本語**: MCP ツールを Gemini の関数宣言に変換するとき、name・description・parameters（入力スキーマ）だけを写す。
- **どう使っているか**: MCP の annotations（readOnlyHint など）は FunctionDeclaration に写されず落ちる。リポジトリ全体で readOnlyHint / destructiveHint は 0 件（grep）。Agent Platform 用の変換（agent_platform_to_gemini_tool）も name / description / parameters_json_schema だけ。
- **条件**: Python SDK に mcp.ClientSession を tools として渡したとき（実験的機能）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、52-55 行（# limitations under the License.）（取得 2026-10-02T22:11:34Z、sha256 d65bdc66a38e…）
- **補足**: FunctionDeclaration には behavior（BLOCKING / NON_BLOCKING）の欄があるが、MCP 変換では設定しない。

### Google — google-genai（Python SDK）の自動関数呼び出し（MCP セッション）

<a id="g-g3-consumer-apps-model-apis-12"></a>
#### G3CAMA-12 Google — google-genai（Python SDK）の自動関数呼び出し（MCP セッション）

- **資料**: google/genai/_extra_utils.py（自動関数呼び出しのループ）（SDK のソースコード）
- **URL**: https://github.com/googleapis/python-genai/blob/6d13650a0539a39a16e452d0e38c15a31b3b990d/google/genai/_extra_utils.py#L405-L425
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleapis/python-genai/6d13650a0539a39a16e452d0e38c15a31b3b990d/google/genai/_extra_utils.py
- **版**: commit 6d13650a0539a39a16e452d0e38c15a31b3b990d（HEAD, 2026-10-02）
- **書いてある場所**: 415-418 行目（# limitations under the License.）
- **原文**:

> if isinstance(func, McpToGenAiToolAdapter): mcp_tool_response = await func.call_tool( types.FunctionCall(name=func_name, args=args) )

- **日本語**: 関数が MCP のアダプタなら、そのまま MCP セッションの call_tool を呼ぶ。
- **どう使っているか**: モデルが MCP ツールを呼ぶと、SDK は確認なしで call_tool を実行し結果をモデルに返す（自動関数呼び出し）。ツールの性質による区別は無い。止めるには automatic_function_calling.disable か maximum_remote_calls。
- **条件**: 自動関数呼び出しが有効（既定）で MCP セッションを tools に渡したとき。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、415-418 行（# limitations under the License.）（取得 2026-10-02T22:11:34Z、sha256 fdaa40dee4e3…）
- **補足**: McpToGenAiToolAdapter.call_tool（google/genai/_adapters.py L39-L52）は name と arguments を渡すだけ。

### Google — google-genai（JS/TS SDK, js-genai）の MCP ツール変換

<a id="g-g3-consumer-apps-model-apis-13"></a>
#### G3CAMA-13 Google — google-genai（JS/TS SDK, js-genai）の MCP ツール変換

- **資料**: src/_transformers.ts: mcpToGeminiTool（SDK のソースコード）
- **URL**: https://github.com/googleapis/js-genai/blob/f6b85db43db2cb88705f60af9c394fee308ac497/src/_transformers.ts#L728-L752
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleapis/js-genai/f6b85db43db2cb88705f60af9c394fee308ac497/src/_transformers.ts
- **版**: commit f6b85db43db2cb88705f60af9c394fee308ac497（HEAD, 2026-10-02）
- **書いてある場所**: 733-737 行目
- **原文**:

> const functionDeclaration: Record<string, unknown> = { name: mcpToolSchema['name'], description: mcpToolSchema['description'], parametersJsonSchema: mcpToolSchema['inputSchema'], };

- **日本語**: 関数宣言は name・description・parametersJsonSchema（inputSchema）から作る。
- **どう使っているか**: annotations は写されない（outputSchema は responseJsonSchema に写す。behavior は呼び出し側の config から）。src に readOnlyHint / destructiveHint は 0 件（grep。annotation の語は別機能のテキスト注釈だけ）。McpCallableTool.callTool（src/mcp/_mcp.ts）も確認なしで mcpClient.callTool を呼ぶ。
- **条件**: mcpToTool() で MCP クライアントを tools に渡したとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、733-737 行（取得 2026-10-02T22:11:33Z、sha256 1a6140179b2f…）

### Google — Gemini API（generateContent）の SDK 内蔵 MCP 対応

<a id="g-g3-consumer-apps-model-apis-14"></a>
#### G3CAMA-14 Google — Gemini API（generateContent）の SDK 内蔵 MCP 対応

- **資料**: Function calling with the Gemini API（generate-content 版）（公式の文書）
- **URL**: https://ai.google.dev/gemini-api/docs/generate-content/function-calling
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/ai.google.dev_gemini-api_docs_generate-content_function-calling.md.txt）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2026-10-02 取得（.md.txt 版）
- **書いてある場所**: 2689-2692 行目（## Model context protocol (MCP)）
- **原文**:

> When the model generates an MCP tool call, the Python and JavaScript client SDK can automatically execute the MCP tool and send the response back to the model in a subsequent request, continuing this loop until no more tool calls are made by the model.

- **日本語**: モデルが MCP ツールの呼び出しを生成すると、Python と JavaScript の SDK はその MCP ツールを自動で実行し、結果を次のリクエストでモデルに返す。モデルがツールを呼ばなくなるまでこれを続ける。
- **どう使っているか**: 公式文書も、MCP ツールを自動実行するループとして説明し、確認や注釈には触れない（checked_no_mention）。
- **条件**: 内蔵 MCP 対応は実験的（同ページ「Limitations with built-in MCP support」）。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、2689-2692 行（## Model context protocol (MCP)）（取得 2026-10-02T22:11:20Z、sha256 7bf56feaea36…）
- **補足**: verify_quote.py の UA（Chrome/124）だと ai.google.dev がログインへのリダイレクトを繰り返して取得できない（curl: (47)）。別の UA で取った .md.txt（https://ai.google.dev/gemini-api/docs/generate-content/function-calling.md.txt）を 127.0.0.1:8766 で配信して照合した（fetched_url はその一時 URL）。

### Google — Gemini API Interactions API の Remote MCP（mcp_server ツール）

<a id="g-g3-consumer-apps-model-apis-15"></a>
#### G3CAMA-15 Google — Gemini API Interactions API の Remote MCP（mcp_server ツール）

- **資料**: Function calling with the Gemini API（Remote MCP 節）（公式の文書）
- **URL**: https://ai.google.dev/gemini-api/docs/function-calling
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/ai.google.dev_gemini-api_docs_function-calling.md.txt）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2026-10-02 取得（.md.txt 版）
- **書いてある場所**: 3138 行目（## Remote MCP (Model Context Protocol)）
- **原文**:

> | `allowed_tools` | `array` | No | Restrict which tools from the server the agent may call. |

- **日本語**: allowed_tools（配列・任意）：サーバーのどのツールをエージェントが呼んでよいかを制限する。
- **どう使っているか**: mcp_server ツールの欄は type / name / url / headers / allowed_tools だけで、承認（require_approval 相当）の欄も注釈の扱いも無い。読み書きで絞るなら利用者がツール名で allowed_tools を書く。
- **条件**: Interactions API（Streamable HTTP のサーバーのみ）。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、3138 行（## Remote MCP (Model Context Protocol)）（取得 2026-10-02T22:11:20Z、sha256 039ec43e206d…）
- **補足**: 取得の事情は G3_consumer_apps_model_apis-14 と同じ（.md.txt を localhost で照合）。Antigravity agent のページ（antigravity-agent.md.txt）の mcp_server も同様に注釈・承認の記述なし（checked_no_mention）。python-genai の _gaos/types/interactions/mcpserver.py も allowed_tools / headers / name / url だけ。

### Google — Gemini API の managed agent（Antigravity agent）の Hooks

<a id="g-g3-consumer-apps-model-apis-16"></a>
#### G3CAMA-16 Google — Gemini API の managed agent（Antigravity agent）の Hooks

- **資料**: Hooks（Gemini API docs）（公式の文書）
- **URL**: https://ai.google.dev/gemini-api/docs/agent-hooks
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/ai.google.dev_gemini-api_docs_agent-hooks.md.txt）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2026-10-02 取得（.md.txt 版）
- **書いてある場所**: 1177 行目（## Limitations）
- **原文**:

> They do not fire for custom function calling (`function`) or external Model Context Protocol (`mcp_server`) tools handled outside the container.

- **日本語**: フックは、自前の関数呼び出し（function）や、コンテナの外で処理される外部の MCP（mcp_server）ツールでは発火しない。
- **どう使っているか**: サンドボックスのフック（破壊的なコマンドを止める例がある）は MCP ツールには効かない。MCP ツールの呼び出しを止める仕組みとして、注釈もフックも使われない。
- **条件**: Antigravity agent のリモートサンドボックス。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、1177 行（## Limitations）（取得 2026-10-02T22:11:20Z、sha256 9dba65b0c75f…）
- **補足**: 同ページ：フックが落ちた・時間切れ・解釈できない JSON のときは allow として続行する（失敗時は許可側）。取得の事情は -14 と同じ。

### Anthropic — Claude Desktop（Cowork / Code タブ）の MCP 協調器：読み取り専用・破壊的の判定

<a id="g-g3-consumer-apps-model-apis-17"></a>
#### G3CAMA-17 Anthropic — Claude Desktop（Cowork / Code タブ）の MCP 協調器：読み取り専用・破壊的の判定

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-CKt-cwRV.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-CKt-cwRV.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-CKt-cwRV.js。行番号は目安）
- **原文**:

> isRemoteToolDestructive(e,t){if(this.isLocalMcpServer(e))return this.localMcpManager.getConnectedServersInfo().find((t=>t.name===e))?.tools.find((e=>e.name===t))?.annotations?.destructiveHint;let n=this.findDirectMcpConnection(e);if(n){let e=n.tools.find((e=>e.name===t));return!e||e.annotations?.destructiveHint}

- **日本語**: isRemoteToolDestructive：ローカルサーバーならそのツールの annotations.destructiveHint をそのまま返す。直結（direct）の接続なら、ツールが一覧に無いときは true、あれば destructiveHint を返す。
- **どう使っているか**: 判定の土台。isRemoteToolReadOnly は readOnlyHint を、isRemoteToolDestructive は destructiveHint を返し、呼び出し側は「=== true」で比べる。したがって destructiveHint が未宣言のツールは「破壊的でない」側に入る（MCP 仕様の既定値 destructiveHint=true とは逆）。直結の接続で一覧に無いツールだけは破壊的扱い。readOnlyHint 未宣言は「読み取り専用でない」側（安全側）。
- **条件**: 対象はローカル MCP・直結（direct）の MCP・claude.ai 経由のコネクタ（proxyManager）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 d7f04a0117ef…）
- **補足**: 直後の isRemoteToolReadOnly：同じ 3 系統で annotations?.readOnlyHint を返し、直結で一覧に無ければ false。isDestructiveConnectorTool は「ローカルでない かつ isRemoteToolDestructive===true」（同ファイル）。 再現手順：公式 apt の Packages（https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-amd64/Packages）にある claude-desktop_2.9939.4_amd64.deb（SHA256 3cfddb23bf2911e05e27b4ed3856b8e795df94643b2c35b59deb317cf995bca0、取得したファイルと一致）を取り、`ar x` → `tar -xf data.tar.xz` → `npx @electron/asar extract usr/lib/claude-desktop/resources/app.asar out` で展開。展開したファイルを 127.0.0.1:8766 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。ファイルの sha256 は verify_result に記す）。ミニファイ済みなので関数名（eqn, yTr など）は版ごとに変わる。macOS / Windows 版は確かめていない（同じコードと思われるが不明）。C04 の未確認だった「downloads.claude.ai のルートが 403」は、版つきの apt プールの URL なら取得できた（Windows の Claude-<sha>.exe の経路は試していない）。

### Anthropic — Claude Desktop の MCP ツール呼び出しゲート（mcpToolCallGate）

<a id="g-g3-consumer-apps-model-apis-18"></a>
#### G3CAMA-18 Anthropic — Claude Desktop の MCP ツール呼び出しゲート（mcpToolCallGate）

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-CKt-cwRV.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-CKt-cwRV.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-CKt-cwRV.js。行番号は目安）
- **原文**:

> if(e.inAutoMode()&&e.isReadOnlyTool(n,r))return $(e.sessionId,c,"auto_read_only"),{behavior:"allow"}

- **日本語**: auto モード中で、読み取り専用のツールなら、"auto_read_only" と記録して許可する。
- **どう使っているか**: ゲート（ox）は順に：disallowedTools なら拒否 → 記録済みの許可（ledger）→（!t.Qg(c) のとき）allowedTools → ホストの常設許可 → 権限モードによる免除 → 「auto モード かつ readOnlyHint===true」なら確認なしで許可 → それ以外は canUseTool（承認の問い合わせ）。readOnlyHint:true を嘘で付けたツールは、auto モードではこのゲートで承認なしに通る（Claude Code 側の auto モードの分類器など、他の層がさらに止めるかはこのコードからは不明）。
- **条件**: inAutoMode() が真のとき（Cowork の auto 権限モード。-19）。Code タブでは常に偽（-20）。前段の条件 !t.Qg(c) の意味は不明（同じ関数の別の箇所で t.Qg(e) は "org_requires_approval" の原因に使われるので、組織が承認を必須にしたツールを除く条件と思われるが未確認）。ゲートは guardAndSealForSdk の第 2 引数が真のときだけ作られる（Cowork では `!g||pt`。g / pt の意味は不明）。対象は SDK に渡す MCP サーバー（sealForSdk）を通る呼び出し。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 d7f04a0117ef…）
- **補足**: isReadOnlyTool は guardAndSealForSdk で「(e,t)=>this.isRemoteToolReadOnly(e,t)===!0」として渡される（同ファイル）。C04_anthropic-09（Cowork のドキュメント「Read-only tools are approved」の判定根拠が不明）を、実装では readOnlyHint===true と裏づける。C04_anthropic-33（desktop の auto モードで read-only のローカル MCP ツールも毎回確認される、という issue）は、この版では Cowork の auto モードなら readOnlyHint:true のローカルツールも許可される経路がある（Code タブでは無い）。issue の時点の版の挙動は不明。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 usage_ja のゲートの順に、先頭の disallowedTools の拒否と ledger を足した。conditions に、ゲートが作られる条件（guardAndSealForSdk の第 2 引数）が不明であることを足した。

### Anthropic — Claude Desktop の Cowork セッション：auto モードの判定

<a id="g-g3-consumer-apps-model-apis-19"></a>
#### G3CAMA-19 Anthropic — Claude Desktop の Cowork セッション：auto モードの判定

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-vKHHEwY1.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-vKHHEwY1.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-vKHHEwY1.js。行番号は目安）
- **原文**:

> inAutoMode:()=>n()==="auto"

- **日本語**: inAutoMode は「セッションの権限モードが "auto"」。
- **どう使っているか**: Cowork のセッションでは、ゲート（-18）の inAutoMode が権限モード auto のとき真になる。つまり Cowork の auto モードでは、readOnlyHint:true の MCP ツールはこのゲートで承認なしに通る。
- **条件**: Cowork セッション、権限モード auto。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 0075df7fcc12…）
- **補足**: 同じ関数で bypassPermissions モードは modeWaivesAsking で全ツールの確認を省く（注釈と無関係）。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 検証者の追加確認：同ファイルの Bu() は「modeWaivesAsking: bypassPermissions のときだけ免除、inAutoMode: 権限モード auto」を返し、Cowork（lam_session_mcp の計測と同じ箇所）で guardAndSealForSdk(...,Bu(()=>r.getActiveSession(a))) として渡される（引用「function Bu(e){...inAutoMode:()=>n()==="auto"}}」を http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-vKHHEwY1.js で exact、sha256 0075df7fcc12098fd254fb7385f58b9031f3a64f85e8319c525d633e11322266）。 Cowork のセッションで使われていることを、呼び出し箇所（Bu の受け渡し）で確かめた。

### Anthropic — Claude Desktop の Code タブ（CCD）：auto モードの判定

<a id="g-g3-consumer-apps-model-apis-20"></a>
#### G3CAMA-20 Anthropic — Claude Desktop の Code タブ（CCD）：auto モードの判定

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-B9SZqsi8.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-B9SZqsi8.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-B9SZqsi8.js。行番号は目安）
- **原文**:

> modeWaivesAsking:(e,t)=>this.permissionBroker.mcpToolCallWaivedByMode(e,t,r),inAutoMode:()=>!1

- **日本語**: Code タブのセッションでは inAutoMode は常に偽。
- **どう使っているか**: Code タブでは、このゲートの「auto モードで readOnlyHint:true なら許可」の経路は使われない（Claude Code 本体の権限処理に任せる）。
- **条件**: Code タブ（Claude Code をデスクトップで動かすセッション）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 906cc2daab19…）
- **補足**: 同じ箇所の standingGrantCovers は、SSH 先ホストのコネクタツールについて offHostConnectorTool(...).readOnly（= isRemoteToolReadOnly===true）を常設許可の判定に渡す。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 Code タブの mcpToolCallWaivedByMode は、条件によって auto の分類器の判定（standDown==="classifier"）を返すので、Code タブの auto モードの扱いは注釈ではなく分類器による（同ファイル）。 notes に、Code タブの auto モードは分類器（mcpToolCallWaivedByMode）で扱われることを補足。

### Anthropic — Claude Desktop（Cowork）の auto モード：破壊的コネクタツールでは「常に許可」を使わない

<a id="g-g3-consumer-apps-model-apis-21"></a>
#### G3CAMA-21 Anthropic — Claude Desktop（Cowork）の auto モード：破壊的コネクタツールでは「常に許可」を使わない

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> function eqn(e){if(!e.gateEnabled||e.permissionMode!=="auto")return!1;let t=e.toolName.match(OKn);return t?e.isDestructiveConnectorTool(t[1],t[2]):!1}

- **日本語**: 機能ゲートが有効で権限モードが auto のとき、mcp__<サーバー>__<ツール> がローカルでない破壊的コネクタツールなら真を返す（＝常に許可の記録を上書きする）。
- **どう使っているか**: auto モードでは、destructiveHint:true のリモートのコネクタツールについて、利用者の「常に許可」を使わず判定し直す（呼び出し元の名前 shouldAutoModeOverrideAlwaysAllow、計測イベント lam_auto_mode_always_allow_overridden）。destructiveHint 未宣言のツールは対象外（-17 の比較が === true のため）。
- **条件**: 機能ゲート 4200321681 が有効、Cowork の権限モード auto、ローカルでない（コネクタ）ツール。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: 同じ判定は index.chunk-vKHHEwY1.js の規則キャッシュからの自動許可・スケジュール実行の自動許可でも使われる（t.iw(...)）。preflight の呼び出し元では、上書きすると判定を "allow" から "ask" に変える（`t="ask"`）。その "ask" が利用者への確認になるのか分類器に回るのかは、このコードだけでは不明。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 notes：上書き時に allow を ask に変えることを呼び出し元で確かめて書き足した。

### Anthropic — Claude Desktop（Cowork）の watcher（スケジュールタスクの監視）からの MCP 呼び出し

<a id="g-g3-consumer-apps-model-apis-22"></a>
#### G3CAMA-22 Anthropic — Claude Desktop（Cowork）の watcher（スケジュールタスクの監視）からの MCP 呼び出し

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> if(i.isRemoteToolDestructive(o,s)===!0)return r("rejected_policy",`Tool "${s}" is marked destructive, or its connector's tool list cannot confirm it is not, so it cannot run from a watcher.`);

- **日本語**: ツールが破壊的なら拒否：「ツール ${s} は破壊的と印が付いているか、コネクタのツール一覧で破壊的でないと確かめられないので、watcher からは実行できない」。
- **どう使っているか**: watcher（人がいない実行）からの呼び出しは destructiveHint:true のツールを拒否する。続けて管理ポリシーの blocked / ask、利用者が無効にしたツールも拒否。destructiveHint 未宣言のツールは拒否されない（読み取り専用の宣言も要求しない）。
- **条件**: watcher の mcpTools 許可リストに入っているツールのみ。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: メッセージの「cannot confirm it is not」は直結の接続で一覧に無いツール（-17 で true）を指す。index.chunk-vKHHEwY1.js のスケジュールタスク用サーバーには isMcpToolDestructive（解決できなければ破壊的扱い、できれば isRemoteToolDestructive）が渡される。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop（Cowork）の HTML アーティファクトから MCP ツールを呼ぶ橋（CoworkArtifacts.callMcpTool）

<a id="g-g3-consumer-apps-model-apis-23"></a>
#### G3CAMA-23 Anthropic — Claude Desktop（Cowork）の HTML アーティファクトから MCP ツールを呼ぶ橋（CoworkArtifacts.callMcpTool）

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> v=d.isRemoteToolReadOnly(g,_)===!0,y=d.isRemoteToolDestructive(g,_)===!0,b=await d.getManagedToolPolicy(g,_),x=b==="ask",S=Mgi(d,g,_),C=v&&b!=="ask"&&b!=="blocked"&&!S

- **日本語**: v は「読み取り専用か」、y は「破壊的か」、b は管理ポリシー。読み取り専用で、ポリシーが ask / blocked でなく、利用者が無効にしていなければ C（結果のキャッシュを使ってよい）。
- **どう使っているか**: アーティファクトからの呼び出しで、readOnlyHint:true のツールだけ結果をキャッシュし、有効期限（既定 5 分）内に同じ引数で呼ばれたらツールを呼ばずにキャッシュを返す。書き込みツールはキャッシュを使わない。
- **条件**: アーティファクトの mcp_tools 許可リストにあるツール。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: readOnlyHint:true を嘘で付けた書き込みツールは、2 回目以降の同じ呼び出しが実行されず、キャッシュの結果が返る（副作用が起きない側の食い違い）。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 キャッシュには有効期限がある：uhi(s,w,Kz()) の Kz は GrowthBook の機能 3229517805 の dataCacheTtlMs（既定 k2t=3e5 ミリ秒＝5 分。k2t の値は grep で確認）。引用「function Kz(){return Fx(Gz,"dataCacheTtlMs",k2t,O().int().min(0))}」は exact（sha256 82f679b6cae211ebe14333dbea7aa872aff395dd4cefaff85a7c03e044babf4b）。キャッシュの鍵は shi("mcp",ツール名,引数) で、アーティファクトごと。 キャッシュの有効期限（dataCacheTtlMs、既定 5 分）を足した。

### Anthropic — Claude Desktop（Cowork）の HTML アーティファクトの MCP 橋：破壊的ツールの確認

<a id="g-g3-consumer-apps-model-apis-24"></a>
#### G3CAMA-24 Anthropic — Claude Desktop（Cowork）の HTML アーティファクトの MCP 橋：破壊的ツールの確認

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> if(!x&&JRn()&&y){let e=n3.getAccountId(),r=n3.getOrgId();if(jmi(e,r,s,g,_))

- **日本語**: 管理ポリシーが ask でなく、機能が有効で、ツールが破壊的なら、記憶済みの許可が無ければ利用者に確認する。
- **どう使っているか**: アーティファクトからの呼び出しで、destructiveHint:true のツールは利用者の確認（「今後も許可」を記憶できる）を挟む。destructiveHint 未宣言のツールは、この経路では確認されない（管理ポリシー ask のときだけ callRemoteTool 側で確認）。
- **条件**: JRn() は GrowthBook の機能 3229517805 の mcpDestructiveConfirmEnabled（値が無ければ既定 true。引用「function JRn(){return Fx(Gz,"mcpDestructiveConfirmEnabled",!0,k())}」を exact、sha256 82f679b6cae211ebe14333dbea7aa872aff395dd4cefaff85a7c03e044babf4b）。管理ポリシーが ask でないとき。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: ログ文言：「[CoworkArtifacts] callMcpTool() destructive — prompting」。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 conditions の「機能フラグ JRn()（中身は不明）」を訂正：GrowthBook 設定 mcpDestructiveConfirmEnabled、既定 true。

### Anthropic — Claude Desktop のアーティファクトの host tools（ローカル MCP サーバーのツールをアーティファクトから呼ぶ）：確認が要るツールの判定

<a id="g-g3-consumer-apps-model-apis-25"></a>
#### G3CAMA-25 Anthropic — Claude Desktop のアーティファクトの host tools（ローカル MCP サーバーのツールをアーティファクトから呼ぶ）：確認が要るツールの判定

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> function yTr(e){let t=e.annotations;return t?.destructiveHint===!0||t?.readOnlyHint!==!0}

- **日本語**: destructiveHint が true、または readOnlyHint が true でないなら真（＝確認の対象）。
- **どう使っているか**: host tools では、readOnlyHint:true かつ destructiveHint が true でないツールだけが確認なしで走る。注釈が無いツールは確認の対象（安全側）。
- **条件**: アーティファクトの host tools 機能が有効なとき。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: 同じファイルで、アーティファクトへ渡すツール一覧（fTr）は annotations から readOnlyHint / destructiveHint の真偽値だけを残す。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop のアーティファクトの host tools：確認の流れ

<a id="g-g3-consumer-apps-model-apis-26"></a>
#### G3CAMA-26 Anthropic — Claude Desktop のアーティファクトの host tools：確認の流れ

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> if(yTr(d)){let t=()=>this.pane.isFocused===void 0?e.activation!==!1:this.pane.isFocused()&&e.activation===!0;

- **日本語**: yTr(d) が真なら、アーティファクトにフォーカスがあり利用者の操作直後であることを求める（その後 confirmDestructive で確認する）。
- **どう使っているか**: 書き込み扱いのツール（-25）は、利用者がアーティファクトを操作した直後でないと「This tool only runs right after you act in this Artifact」で断り、さらに確認ダイアログ（記憶済みの許可があれば省略）を出す。
- **条件**: host tools、yTr が真のツール。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop（3P 配備＝第三者クラウド向け）の直結 MCP のツール定義キャッシュ

<a id="g-g3-consumer-apps-model-apis-27"></a>
#### G3CAMA-27 Anthropic — Claude Desktop（3P 配備＝第三者クラウド向け）の直結 MCP のツール定義キャッシュ

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 13 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> function H3e(){return!mu()||W().type==="3p"}function U3e(e){let t={...e?.destructiveHint===!0&&{destructiveHint:!0},...e?.openWorldHint===!0&&{openWorldHint:!0}};return Object.keys(t).length>0?{annotations:t}:void 0}

- **日本語**: 3P 配備（または配備モード未初期化）なら、キャッシュに残す annotations は destructiveHint:true と openWorldHint:true だけ。
- **どう使っているか**: 未接続・再接続待ちのサーバーのために保存するツール定義（custom3p-mcp-schemas）から、3P では readOnlyHint を落とし、危険側の印だけ残す。キャッシュから復元したツールは読み取り専用とみなされない（安全側）。
- **条件**: H3e()：配備モード未初期化、または配備種別が 3p。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、13 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: C04_anthropic-11/12（3P の承認 UI は「データを変えうるツール」で選択肢を変える、判定根拠は不明）に関係する実装。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop の組み込み MCP サーバー（built-in）の既定ポリシーの点検

<a id="g-g3-consumer-apps-model-apis-28"></a>
#### G3CAMA-28 Anthropic — Claude Desktop の組み込み MCP サーバー（built-in）の既定ポリシーの点検

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DuaKZOPP.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DuaKZOPP.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 7 行目（ミニファイ済みの index.chunk-DuaKZOPP.js。行番号は目安）
- **原文**:

> for(let a of t){if(a.annotations?.readOnlyHint===!0||Object.hasOwn(i??{},a.name))continue;let t=Bs(e.toolPolicy,a.name);t===void 0?n.push(a.name)

- **日本語**: ツールごとに、readOnlyHint が true か既定の一覧にあれば飛ばす。そうでなく toolPolicy に無ければ「覆われていない」に入れる。
- **どう使っているか**: Anthropic 自身の組み込みサーバー（Microsoft 365 など）について、readOnlyHint:true でないツール＝書き込みツールとみなし、既定で ask の規則に覆われていないものを洗い出す（-29 で警告とテレメトリ）。
- **条件**: 組み込みサーバー（fc(e) が真のもの）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、7 行（取得 2026-10-02T22:11:20Z、sha256 82f679b6cae2…）
- **補足**: 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop の組み込み MCP サーバーの点検：警告

<a id="g-g3-consumer-apps-model-apis-29"></a>
#### G3CAMA-29 Anthropic — Claude Desktop の組み込み MCP サーバーの点検：警告

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DZqHLpeA.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DZqHLpeA.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-DZqHLpeA.js。行番号は目安）
- **原文**:

> e.JJ.warn(`[directMcp] built-in ${f.server} exposes write tools with no default-ask coverage: ${n.join(", ")}`)

- **日本語**: [directMcp] 組み込みの ${server} が、既定の ask で覆われていない書き込みツールを出している：${名前}
- **どう使っているか**: -28 の結果を警告ログとテレメトリ（builtin_unlisted_write_tools）に出す。ワイルドカードの allow でだけ事前許可された書き込みツールも別に警告（builtin_glob_allow_write_tools）。
- **条件**: 組み込みサーバーの接続時。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 62826acb27dd…）
- **補足**: 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop の組み込み Microsoft 365 MCP のテレメトリ

<a id="g-g3-consumer-apps-model-apis-30"></a>
#### G3CAMA-30 Anthropic — Claude Desktop の組み込み Microsoft 365 MCP のテレメトリ

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DZqHLpeA.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DZqHLpeA.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-DZqHLpeA.js。行番号は目安）
- **原文**:

> is_write:c?.annotations?.readOnlyHint!==!0

- **日本語**: is_write は「readOnlyHint が true でない」。
- **どう使っているか**: 呼び出しの計測（builtin_m365_call）で、書き込みかどうかを readOnlyHint から付ける（注釈なし＝書き込み扱い）。
- **条件**: office365-mcp の呼び出し時。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 62826acb27dd…）
- **補足**: 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop が直結 MCP のツールを claude.ai 側へ通知する一覧

<a id="g-g3-consumer-apps-model-apis-31"></a>
#### G3CAMA-31 Anthropic — Claude Desktop が直結 MCP のツールを claude.ai 側へ通知する一覧

- **資料**: Claude Desktop app.asar .vite/build/index.chunk-DSfNYObC.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_app.asar_.vite_build_index.chunk-DSfNYObC.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの index.chunk-DSfNYObC.js。行番号は目安）
- **原文**:

> "anthropic/readOnlyHint":l.annotations?.readOnlyHint??null,"anthropic/alwaysLoad":!0}}),i.push({name:c.name,hash:r.n(l)?void 0:d,read_only_hint:l.annotations?.readOnlyHint??null})

- **日本語**: 各ツールに _meta の "anthropic/readOnlyHint" と、一覧の read_only_hint として readOnlyHint（無ければ null）を付ける。
- **どう使っているか**: Desktop で接続した MCP サーバーのツールを（会話の）サーバー側へ announce するとき、readOnlyHint だけを写して渡す。受け取った側での使われ方は Desktop のコードからは分からない（不明）。
- **条件**: 直結（direct）の MCP サーバー。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 82c8ee77579e…）
- **補足**: index.chunk-BLCyCJ-Y.js のローカル / プラグインのサーバーでも同じく "anthropic/readOnlyHint" を付ける（同様の行）。 取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側の MCP ツール承認の決定（Chat / Cowork 共通の承認状態）

<a id="g-g3-consumer-apps-model-apis-32"></a>
#### G3CAMA-32 Anthropic — Claude Desktop 画面側の MCP ツール承認の決定（Chat / Cowork 共通の承認状態）

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-7-YM6Q2eRE.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-7-YM6Q2eRE.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 46 行目（ミニファイ済みの shared-7-YM6Q2eRE.js。行番号は目安）
- **原文**:

> if(e&&a?.annotations?.destructiveHint===!0)return{approvalRequired:!0,showAlwaysAllowed:!1,sessionGrantHonored:!1,persistentGrantsSuppressed:d,scheduledRunGrantsSuppressed:f,expandInputByDefault:v,alwaysAllowHiddenBy:"destructive_tools_gate"}

- **日本語**: 機能フラグが有効で destructiveHint が true なら、承認を必須にし「常に許可」を出さない（隠した理由は destructive_tools_gate）。
- **どう使っているか**: destructiveHint:true のツールは毎回承認、「常に許可」は表示しない（セッションの許可も使わない）。
- **条件**: 機能フラグ disable_destructive_mcp_tools_by_default が有効なとき（-44）。組織の管理ポリシー（blocked / allow / ask）と実効の上限（effectiveMaxPermission）の後、利用者の保存済み「常に許可」より先に評価されるので、destructiveHint:true のツールでは保存済みの「常に許可」も効かない。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:20Z、sha256 de41ad53567d…）
- **補足**: 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外）。claude.ai のウェブ画面と同じコードかは不明。再現手順：公式 apt の Packages（https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-amd64/Packages）にある claude-desktop_2.9939.4_amd64.deb（SHA256 3cfddb23bf2911e05e27b4ed3856b8e795df94643b2c35b59deb317cf995bca0、取得したファイルと一致）を取り、`ar x` → `tar -xf data.tar.xz` → `npx @electron/asar extract usr/lib/claude-desktop/resources/app.asar out` で展開。展開したファイルを 127.0.0.1:8766 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。ファイルの sha256 は verify_result に記す）。ミニファイ済みなので関数名（eqn, yTr など）は版ごとに変わる。macOS / Windows 版は確かめていない（同じコードと思われるが不明）。C04 の未確認だった「downloads.claude.ai のルートが 403」は、版つきの apt プールの URL なら取得できた（Windows の Claude-<sha>.exe の経路は試していない）。 評価の順（利用者の保存済み「常に許可」より先）を conditions に足した。

### Anthropic — Claude Desktop 画面側の MCP ツール承認：設定値 "readOnly"

<a id="g-g3-consumer-apps-model-apis-33"></a>
#### G3CAMA-33 Anthropic — Claude Desktop 画面側の MCP ツール承認：設定値 "readOnly"

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-7-YM6Q2eRE.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-7-YM6Q2eRE.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 46 行目（ミニファイ済みの shared-7-YM6Q2eRE.js。行番号は目安）
- **原文**:

> _==="never"&&y!==!1||_==="readOnly"&&a?.annotations?.readOnlyHint===!0&&y!==!1?{approvalRequired:!1,expandInputByDefault:v,coworkWriteToolWarning:g}

- **日本語**: 設定が "never"、または設定が "readOnly" で readOnlyHint が true なら、承認は不要。
- **どう使っているか**: ツール承認の設定（mcp_tool_approval_config）がサーバー／ツールに "readOnly" を指定していると、readOnlyHint:true のツールは承認なしで走る。
- **条件**: 設定 mcp_tool_approval_config の値が "readOnly" のサーバー / ツール。この設定は機能設定の一覧（shared-0 の名前リスト）に並んでおり、Anthropic 側の動的設定と思われるが、誰がどう設定するかは不明。 評価の順：組織の管理ポリシー → 実効の上限 → 破壊的ツールの門（-32）→ 組織が「常に許可」を無効にしている場合 → 設定 "always" → 利用者の保存済み「常に許可」→ 設定 "server" → 設定 "never" / "readOnly"。"readOnly" の免除は、それより前の条件に当たらず、利用者が「常に許可」を明示的に切っていない（y!==false）ときだけ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:20Z、sha256 de41ad53567d…）
- **補足**: 取りうる値は always / never / perChat / readOnly / server / defaultBlocked（-43）。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 評価の順と前提条件を conditions に足した。

### Anthropic — Claude Desktop 画面側の承認：Cowork の書き込みツール警告

<a id="g-g3-consumer-apps-model-apis-34"></a>
#### G3CAMA-34 Anthropic — Claude Desktop 画面側の承認：Cowork の書き込みツール警告

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-7-YM6Q2eRE.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-7-YM6Q2eRE.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 46 行目（ミニファイ済みの shared-7-YM6Q2eRE.js。行番号は目安）
- **原文**:

> let g=u==="cowork"&&a?.annotations?.readOnlyHint!==!0

- **日本語**: Cowork で、readOnlyHint が true でないツールには書き込みツールの警告を付ける。
- **どう使っているか**: Cowork の承認カードで、readOnlyHint:true でないツール（注釈なしも含む）に coworkWriteToolWarning を立てる。立つと、カードは危険の警告文（「Allowing this action comes with risks. ...」）を出し、「Always allow」の文言を「Allow for all tasks」に変え、常に許可を主ボタンにせず、「Allow for this task」（タスク内だけの許可）を出す（-47）。「常に許可」の選択肢そのものは消えない。承認が要るかどうか（approvalRequired）はこの印では変わらず、利用者が以前に保存した「常に許可」があれば書き込みツールでも確認なしになる（shared-7 の同じ関数）。
- **条件**: surface が cowork のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:20Z、sha256 de41ad53567d…）
- **補足**: C04_anthropic-12（3P ドキュメント「データを変えうるツールは session-scoped の Allow for this task と、悪意ある指示の警告」）の「データを変えうる」の判定が readOnlyHint によることを裏づける。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 usage_ja の「「常に許可」が提示されず」は誤り。画面の部品（c14f706e5）では文言が「Allow for all tasks」に変わり主ボタンでなくなるだけで、選択肢は残る（-47 の検証者注を参照）。

### Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のツール一覧

<a id="g-g3-consumer-apps-model-apis-35"></a>
#### G3CAMA-35 Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のツール一覧

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-13-3g2ILngu.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-13-3g2ILngu.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 4 行目（ミニファイ済みの shared-13-3g2ILngu.js。行番号は目安）
- **原文**:

> a=r.annotations?.readOnlyHint===!0?"readOnly":r.annotations?"write":void 0;t.push({name:r.name,displayName:r.displayName,accessKind:a,alreadyAllowed:!i.approvalRequired})

- **日本語**: readOnlyHint が true なら "readOnly"、annotations があれば "write"、無ければ未設定。それを accessKind として一覧に入れる。
- **どう使っているか**: Cowork で「Skip all approvals?」を出すとき、コネクタのツールを Read-only / Write/delete のラベル付きで並べる（書き込みを先頭に）。注釈が無いツールにはラベルが付かない。
- **条件**: Cowork の承認省略の確認画面。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、4 行（取得 2026-10-02T22:11:20Z、sha256 104a28bde3c3…）
- **補足**: ラベルの文言は caa47d26c-BX2mJOA0.js（-42）。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：MCP ディレクトリへの申請フォーム（ツールの点検）

<a id="g-g3-consumer-apps-model-apis-36"></a>
#### G3CAMA-36 Anthropic — Claude Desktop 画面側：MCP ディレクトリへの申請フォーム（ツールの点検）

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/cd9350303-Btr6jc6I.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_cd9350303-Btr6jc6I.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの cd9350303-Btr6jc6I.js。行番号は目安）
- **原文**:

> No annotations declared. Add a title and readOnlyHint, plus destructiveHint if the tool changes data. The directory's review criteria ask for these.

- **日本語**: 注釈が宣言されていない。title と readOnlyHint、データを変えるなら destructiveHint を加えて。ディレクトリの審査基準がこれらを求めている。
- **どう使っているか**: 申請フォームは接続したサーバーのツールを点検し、注釈が無い・title / readOnlyHint が無い・readOnlyHint が true でないのに destructiveHint が無いものに警告を出す。値が実装と合っているかは点検しない。
- **条件**: connectors directory への申請フォームで、接続したサーバーのツールを点検するとき（対象がリモートサーバーだけか、ローカル（MCPB）も含むかは、このコードからは確かめていない）。
- **扱う宣言**: title・readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 8d716f21f64b…）
- **補足**: 申請データには all_have_annotations / all_have_title / all_have_read_only_hint / all_have_destructive_hint_where_applicable を記録する（同ファイル）。C04 のポータルの記述（宣言の欠落に印を付ける）の実装に当たる。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 conditions の「ローカルサーバーは対象外」は確かめられなかったので不明に弱めた。

### Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テスト

<a id="g-g3-consumer-apps-model-apis-37"></a>
#### G3CAMA-37 Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テスト

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/cd9350303-Btr6jc6I.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_cd9350303-Btr6jc6I.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 45 行目（## Policy compliance）（ミニファイ済みの cd9350303-Btr6jc6I.js。行番号は目安）
- **原文**:

> Functional testing is disabled because no tools are marked readOnlyHint: true. Only read-only tools are eligible.

- **日本語**: readOnlyHint: true の印が付いたツールが無いので、機能テストは使えない。対象は読み取り専用のツールだけ。
- **どう使っているか**: 申請時の自動の機能テスト（実際にツールを呼ぶ）は readOnlyHint:true（かつ destructiveHint が true でない）のツールだけを呼ぶ。readOnlyHint を宣言していないツールがあるとテスト自体が無効になる。
- **条件**: 実験的な自動審査（auto-review）の機能テスト。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、45 行（## Policy compliance）（取得 2026-10-02T22:11:20Z、sha256 8d716f21f64b…）
- **補足**: 同ファイルの判定関数：「e.annotations?.readOnlyHint===!0&&e.annotations?.destructiveHint!==!0」。readOnlyHint:true を嘘で付けた書き込みツールは、このテストで実際に呼ばれうる（-38 の注意書きもそれを認める）。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 検証者の追加確認：テストが無効になる条件は w=!ne||C===0。ne は「ツールが 1 つ以上あり、すべてが boolean の readOnlyHint を宣言」（引用「ne=d(()=>b.length>0&&b.every(e=>typeof e.annotations?.readOnlyHint=="boolean"),[b])」が exact）、C は先頭 100 ツールのうち readOnlyHint===true かつ destructiveHint!==true の数。readOnlyHint を宣言しないツールが 1 つでもあると、別の文言「Functional testing is disabled because N tools do not declare annotations.readOnlyHint」で無効になる。 usage_ja の「readOnlyHint を宣言していないツールがあるとテスト自体が無効」は引用の文ではなく同ファイルの別の条件（ne）による。その条件を照合して notes に足した。

### Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テストの注意書き

<a id="g-g3-consumer-apps-model-apis-38"></a>
#### G3CAMA-38 Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の機能テストの注意書き

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/cd9350303-Btr6jc6I.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_cd9350303-Btr6jc6I.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 45 行目（## Policy compliance）（ミニファイ済みの cd9350303-Btr6jc6I.js。行番号は目安）
- **原文**:

> Tool annotations are self-reported by the server and not verified by Anthropic \u2014 connect a test account with representative data where possible. Write/destructive tools are never called.

- **日本語**: ツールの注釈はサーバーの自己申告で、Anthropic は確かめていない。可能なら代表的なデータを入れたテスト用アカウントをつなぐこと。書き込み・破壊的なツールは呼ばない。
- **どう使っているか**: Anthropic 自身が「注釈は自己申告で未検証」と明記したうえで、注釈を根拠に呼ぶツールを選ぶ。
- **条件**: 申請フォームの機能テスト。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、45 行（## Policy compliance）（取得 2026-10-02T22:11:20Z、sha256 8d716f21f64b…）
- **補足**: 文中の \u2014 はファイル中の文字どおり（エスケープのまま）。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の「読み書き」申告と注釈の照合

<a id="g-g3-consumer-apps-model-apis-39"></a>
#### G3CAMA-39 Anthropic — Claude Desktop 画面側：MCP ディレクトリ申請の「読み書き」申告と注釈の照合

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/ca00fcdfd-DcXim44m.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_ca00fcdfd-DcXim44m.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 2 行目（ミニファイ済みの ca00fcdfd-DcXim44m.js。行番号は目安）
- **原文**:

> Selected "Read only", but these tools are annotated as writing data (readOnlyHint=false or destructiveHint=true): ${n.join(", ")}.

- **日本語**: 「Read only」を選んだのに、これらのツールは書き込みと注釈されている（readOnlyHint=false か destructiveHint=true）：…
- **どう使っているか**: 申請者が選んだ読み書きの区分（read_only / write_only / read_write）と、ツールの注釈を突き合わせて食い違いを警告する（「Write only」なのに read-only の注釈があるツールも警告）。注釈と実装の照合ではなく、申告どうしの照合。
- **条件**: 申請フォームの Use cases の段。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、2 行（取得 2026-10-02T22:11:20Z、sha256 d16baf92cbbb…）
- **補足**: 注釈が無いツールは照合から外れる（t が偽なら数えない）。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：アーティファクトの MCP ツール「監視（watch）」

<a id="g-g3-consumer-apps-model-apis-40"></a>
#### G3CAMA-40 Anthropic — Claude Desktop 画面側：アーティファクトの MCP ツール「監視（watch）」

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/frame-shell-broker-BsN1xK1D.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_frame-shell-broker-BsN1xK1D.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 14 行目（ミニファイ済みの frame-shell-broker-BsN1xK1D.js。行番号は目安）
- **原文**:

> if(c?.track("granted"),Sg.get(l)?.byTool.get(u)?.readOnly===!1)return t({error:Q("bad_request","declared-write tools cannot be watched",l)});

- **日本語**: ツールの readOnly が false なら「宣言上書き込みのツールは監視できない」で拒否。
- **どう使っているか**: アーティファクトがツールを定期的に呼び直す watch は、readOnlyHint:false と明示したツールだけを拒む。注釈が無いツールは拒まれない。
- **条件**: アーティファクトの watch 機能。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、14 行（取得 2026-10-02T22:11:20Z、sha256 6a1fbb328563…）
- **補足**: 同ファイルで、ツール一覧を受けたときにも readOnly===false のツールの既存の watch を打ち切る。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### OpenRouter — @openrouter/agent（OpenRouter Agent SDK）の MCP ツール包み（@openrouter/mcp が再輸出）

<a id="g-g3-consumer-apps-model-apis-41"></a>
#### G3CAMA-41 OpenRouter — @openrouter/agent（OpenRouter Agent SDK）の MCP ツール包み（@openrouter/mcp が再輸出）

- **資料**: esm/mcp/tool-wrapper.js: wrapMcpTool（SDK のソースコード）
- **URL**: https://unpkg.com/@openrouter/agent@0.11.0/esm/mcp/tool-wrapper.js
- **版**: @openrouter/agent 0.11.0（npm latest, 2026-10-02）。@openrouter/mcp 1.1.1 は @openrouter/agent/mcp を再輸出するだけ
- **書いてある場所**: 115-123 行目
- **原文**:

> return markMcp(tool({ name, ...(def.description !== undefined && { description: def.description, }), inputSchema, ...(outputSchema !== undefined && { outputSchema, }),

- **日本語**: MCP ツールを Agent SDK のツールにするとき、name・description・inputSchema・outputSchema だけを使う。
- **どう使っているか**: annotations は写されず、requireApproval（Agent SDK の人の承認の仕組み）も注釈から設定しない。パッケージの JS に readOnlyHint / destructiveHint は 0 件、esm/mcp の中には annotations も 0 件（パッケージの他の箇所の annotations は応答の引用注釈など別用途）。
- **条件**: createMCPTools() で remote MCP サーバーをつないだとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、115-123 行（取得 2026-10-02T22:11:38Z、sha256 7e429ae7f01b…）
- **補足**: OpenRouter の文書（Agent SDK の MCP Tools / Tool Approval & State Persistence）も注釈に触れない。承認は tool() 定義の requireApproval で利用者が書く。 「annotations は 0 件」はパッケージ全体では誤り（引用の注釈など別用途で出る）。MCP の部分（esm/mcp）に限って 0 件と訂正。

### Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のラベル

<a id="g-g3-consumer-apps-model-apis-42"></a>
#### G3CAMA-42 Anthropic — Claude Desktop 画面側：Cowork の「承認をすべて省く」確認画面のラベル

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/caa47d26c-BX2mJOA0.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_caa47d26c-BX2mJOA0.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの caa47d26c-BX2mJOA0.js。行番号は目安）
- **原文**:

> e.accessKind==="readOnly"?i(E,{defaultMessage:"Read-only",id:"djNL6DWBKa"}):i(E,{defaultMessage:"Write/delete",id:"joY3552MvK"})

- **日本語**: accessKind が "readOnly" なら「Read-only」、そうでなければ「Write/delete」と表示する。
- **どう使っているか**: -35 の accessKind をラベルにする（Write/delete は危険色）。
- **条件**: Cowork の「Skip all approvals?」画面。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 40842411530e…）
- **補足**: 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：MCP ツール承認の設定の取りうる値

<a id="g-g3-consumer-apps-model-apis-43"></a>
#### G3CAMA-43 Anthropic — Claude Desktop 画面側：MCP ツール承認の設定の取りうる値

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-7-YM6Q2eRE.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-7-YM6Q2eRE.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 46 行目（ミニファイ済みの shared-7-YM6Q2eRE.js。行番号は目安）
- **原文**:

> var _M=u(["always","never","perChat","readOnly","server","defaultBlocked"])

- **日本語**: 承認設定の値は always / never / perChat / readOnly / server / defaultBlocked。
- **どう使っているか**: "readOnly" は readOnlyHint を見て承認を省く値（-33）。
- **条件**: mcp_tool_approval_config（-33 の注を参照）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:20Z、sha256 de41ad53567d…）
- **補足**: 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：破壊的ツールを既定で承認必須にする機能フラグ

<a id="g-g3-consumer-apps-model-apis-44"></a>
#### G3CAMA-44 Anthropic — Claude Desktop 画面側：破壊的ツールを既定で承認必須にする機能フラグ

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/shared-7-YM6Q2eRE.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_shared-7-YM6Q2eRE.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 46 行目（ミニファイ済みの shared-7-YM6Q2eRE.js。行番号は目安）
- **原文**:

> function UM(){return O("disable_destructive_mcp_tools_by_default")}

- **日本語**: 機能フラグ disable_destructive_mcp_tools_by_default を読む関数。
- **どう使っているか**: -32 の destructiveHint の門の有効・無効を決めるフラグ。既定値や配布状況は不明。
- **条件**: 機能フラグ。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:20Z、sha256 de41ad53567d…）
- **補足**: 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側（claude.ai と同じ設定画面と思われる）：コネクタの「Tool permissions」のツールの分け方

<a id="g-g3-consumer-apps-model-apis-45"></a>
#### G3CAMA-45 Anthropic — Claude Desktop 画面側（claude.ai と同じ設定画面と思われる）：コネクタの「Tool permissions」のツールの分け方

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/c0c27ee9a-DXf1L9Ql.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_c0c27ee9a-DXf1L9Ql.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの c0c27ee9a-DXf1L9Ql.js。行番号は目安）
- **原文**:

> function n(e){return e.annotations?.readOnlyHint===!0?"readOnly":e.annotations?"write":"unspecified"}

- **日本語**: readOnlyHint が true なら "readOnly"、annotations があれば "write"、無ければ "unspecified"。
- **どう使っているか**: コネクタのツール権限の画面は、ツールを readOnlyHint で「Read-only tools」「Write/delete tools」「Other tools（注釈なし）」に分けて並べる（ラベルは c4ac4d9d6 / c31521777。-46）。
- **条件**: コネクタ設定の Tool permissions（利用者）と、管理者のコネクタ設定（c31521777 は同じ分け方をその場で行う）。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 8afd0508aff7…）
- **補足**: C04_anthropic-10（「permissions will be categorized by type (for example, read-only tools, write/delete tools)」の根拠が不明）を、実装では readOnlyHint===true / 注釈あり / 注釈なし の 3 分類と裏づける。注釈があって readOnlyHint が無いツールも「Write/delete」に入る。 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 検証者の追加確認：利用者のコネクタ設定の「Tool permissions」の部品（c4ac4d9d6-PHptze-6.js）がこの関数を取り込み（「import{n as ve}from"./c0c27ee9a-DXf1L9Ql.js"」が exact）、Interactive tools（MCP Apps の UI を持つツール）を別に分けたうえで、readOnly / write があれば Read-only tools / Write/delete tools / Other tools の見出しで並べる。readOnly も write も無ければ見出しなしで全部を並べる。 使われている画面（c4ac4d9d6 の Tool permissions）を取り込み文で確かめた。

### Anthropic — Claude Desktop 画面側：管理者のコネクタ設定（tool policy）のツールの群

<a id="g-g3-consumer-apps-model-apis-46"></a>
#### G3CAMA-46 Anthropic — Claude Desktop 画面側：管理者のコネクタ設定（tool policy）のツールの群

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/c31521777-Bywdmh4d.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_c31521777-Bywdmh4d.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの c31521777-Bywdmh4d.js。行番号は目安）
- **原文**:

> var j=["readOnly","write","unspecified"],M=v({readOnly:{defaultMessage:"Read-only tools",id:"OoTYD4aZE3"},write:{defaultMessage:"Write/delete tools",id:"aPdrk6G8fY"},unspecified:{defaultMessage:"Other tools",id:"o1AEhi4IRc"}})

- **日本語**: 群は readOnly / write / unspecified で、表示名は「Read-only tools」「Write/delete tools」「Other tools」。
- **どう使っているか**: 組織の管理者がツールごとの上限（allow / ask / blocked）を設定する画面で、群分けに readOnlyHint を使う（同ファイルの k(e)：readOnlyHint===true→readOnly、注釈あり→write、なし→unspecified）。
- **条件**: 管理者のコネクタのツール方針（claudeai.admin_connectors.tool_policy_changed）。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 表示（印・名前）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 0a44a4d273f3…）
- **補足**: 画面側のコードは deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にある（app.asar の外。claude.ai のウェブ画面と同じコードかは不明）。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。

### Anthropic — Claude Desktop 画面側：Cowork の承認カード（書き込みツール警告が立ったときのボタン）

<a id="g-g3-consumer-apps-model-apis-47"></a>
#### G3CAMA-47 Anthropic — Claude Desktop 画面側：Cowork の承認カード（書き込みツール警告が立ったときのボタン）

- **資料**: Claude Desktop 同梱の画面側コード ion-dist/assets/v1/c14f706e5-DTtvYkuX.js（クライアントのソースコード）
- **URL**: https://downloads.claude.ai/claude-desktop/apt/stable/pool/main/c/claude-desktop/claude-desktop_2.9939.4_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8766/cd2.9939.4_ion-dist_assets_v1_c14f706e5-DTtvYkuX.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Claude Desktop 2.9939.4（Linux x64 .deb。Anthropic 公式 apt リポジトリ stable の最新版、2026-10-02 取得）
- **書いてある場所**: 1 行目（ミニファイ済みの c14f706e5-DTtvYkuX.js。行番号は目安）
- **原文**:

> X=g?void 0:A?.always,Z=g?s(T,{defaultMessage:"Allow for all tasks",id:"0xIGAXr2i7"}):X??s(T,{defaultMessage:"Always allow",id:"lr3QX/nctD"})

- **日本語**: 書き込みツール警告（g）が立っていれば、「常に許可」の文言を「Allow for all tasks」にする（立っていなければ「Always allow」）。
- **どう使っているか**: Cowork の承認カードは、readOnlyHint:true でないツール（-34 の coworkWriteToolWarning）について、常に許可の選択肢の文言を「Allow for all tasks」に変え、危険の警告文「Allowing this action comes with risks. Malicious instructions in files, emails, and web content could trick Claude into unintended actions.」を出し、常に許可を主ボタンにしない（pt の条件に !g）。「Allow for this task」は ca44d5dae の ze（coworkWriteToolWarning などが条件）で出る。常に許可の選択肢は消えないので、利用者が選べば書き込みツールでも以後の確認が省かれうる。
- **条件**: Cowork の承認カードで coworkWriteToolWarning が立ち、showAlwaysAllowed（組織設定などで決まる）が真のとき。shared-7 の coworkAlwaysAllowDisabledByOrg は、この版では定数 LM=!1（常に偽）から来る。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、1 行（取得 2026-10-02T22:11:20Z、sha256 cde2ca9b7daa…）
- **補足**: 追加の照合：警告文「Allowing this action comes with risks. Malicious instructions in files, emails, and web content could trick Claude into unintended actions.」は exact、主ボタンの条件「pt=Re(!!ge&&!O&&!m&&(ft||!Y&&!d&&!p&&!g&&!!u&&!v))」は exact（いずれも sha256 cde2ca9b7daad27c675fd7cfebc830bee98314e6b7a25acd598b6878617c9964）。c14f706e5-DTtvYkuX.js は deb の usr/lib/claude-desktop/resources/ion-dist/assets/v1/ にあるファイルを、検証者が 127.0.0.1:8766 の配信ディレクトリ（g3c/cd/srv）に同じ命名でコピーして照合した。C04_anthropic-08（Cowork：annotation で read-only と宣言されたツールだけがタスクごとの承認から外れる）とは、「書き込みツールは毎回確認、ただし常に許可を選べば省ける」という形で整合する。取得・展開・照合の手順は G3_consumer_apps_model_apis-17 の notes を参照（ミニファイ名は版ごとに変わる）。 元の引用「Zt=!!(!P&&!M&&Kt&&!qt&&L.coworkWriteToolWarning!==!0&&!Yt&&!qe&&zt(n,t))」（ca44d5dae、exact で一致）は、ki() に alwaysAllowOffered（常に許可を提示したかの記録）として渡す値で、画面の「常に許可」の表示そのもの（showAlwaysAllowed は Kt）を決めていなかった。画面の部品 c14f706e5 を読むと、coworkWriteToolWarning が立つと「Always allow」の文言が「Allow for all tasks」に変わり、警告文が出て、常に許可は主ボタンにならないが、選択肢としては残る。そのため引用をその箇所に差し替え、usage / usage_ja を訂正した（「「常に許可」を提示せず」は誤り）。

---

[← 付録 G-7 エディタとコーディングエージェント](appendix-g-7.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-9 サーバの作者と、業務 SaaS のホスト →](appendix-g-9.md)
