[← 付録 G-9 サーバの作者と、業務 SaaS のホスト](appendix-g-9.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-11 WebMCP →](appendix-g-11.md)

---

# 付録 G-10 ゲートウェイ・実行基盤・宣言を検査する道具・登録所

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-10-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C09-01](#g-c09-servers-gateways-security-01) | Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— 開発者向け文書 | サーバの文書 | 宣言を書くことを求める・作者への書き方の案内・宣言を検査する | [確認] |
| [C09-02](#g-c09-servers-gateways-security-02) | Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp） | サーバのソースコード | 宣言を検査する・宣言を書くことを求める | [確認] |
| [C09-03](#g-c09-servers-gateways-security-03) | Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— execute_sentry_tool | サーバのソースコード | 作者への書き方の案内・その他 | [確認] |
| [C09-04](#g-c09-servers-gateways-security-04) | Supabase — Supabase MCP server（supabase-community/supabase-mcp） | サーバのソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [C09-05](#g-c09-servers-gateways-security-05) | Supabase — Supabase MCP server（supabase-community/supabase-mcp） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [C09-06](#g-c09-servers-gateways-security-06) | Supabase — Supabase MCP server（supabase-community/supabase-mcp）— execute_sql | サーバのソースコード | 作者への書き方の案内・その他 | [確認] |
| [C09-07](#g-c09-servers-gateways-security-07) | Supabase — Supabase MCP server（supabase-community/supabase-mcp）— 開発者向け文書 | サーバの文書 | その他 | [確認] |
| [C09-08](#g-c09-servers-gateways-security-08) | Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— 実装手引き | サーバの文書 | 作者への書き方の案内 | [確認] |
| [C09-09](#g-c09-servers-gateways-security-09) | Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— Workers Bindings の d1_database_query | サーバのソースコード | その他 | [確認] |
| [C09-10](#g-c09-servers-gateways-security-10) | Grafana Labs — Grafana MCP server（grafana/mcp-grafana）— query_sql | サーバのソースコード | 作者への書き方の案内・その他 | [確認] |
| [C09-11](#g-c09-servers-gateways-security-11) | Grafana Labs — Grafana MCP server（grafana/mcp-grafana） | サーバのソースコード | 宣言を検査する・宣言を書くことを求める | [確認] |
| [C09-12](#g-c09-servers-gateways-security-12) | MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server） | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C09-13](#g-c09-servers-gateways-security-13) | MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server）— read-only モード | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [C09-14](#g-c09-servers-gateways-security-14) | Neo4j（neo4j-contrib, Neo4j Labs） — mcp-neo4j-cypher（neo4j-contrib/mcp-neo4j、Python / FastMCP） | サーバのソースコード | 作者への書き方の案内・その他 | [確認] |
| [C09-15](#g-c09-servers-gateways-security-15) | Neo4j（neo4j-contrib, Neo4j Labs） — mcp-neo4j-cypher（neo4j-contrib/mcp-neo4j、Python / FastMCP） | サーバのソースコード | ツールを絞る・隠す・作者への書き方の案内 | [確認] |
| [C09-16](#g-c09-servers-gateways-security-16) | Notion — Notion MCP server（makenotion/notion-mcp-server、OpenAPI から自動生成） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C09-17](#g-c09-servers-gateways-security-17) | Stripe — @stripe/mcp（stripe/ai の tools/typescript/src/modelcontextprotocol、mcp.stripe.com への中継） | サーバのソースコード | 使わない・読まない | [確認] |
| [C09-18](#g-c09-servers-gateways-security-18) | Pomerium — Pomerium — 設定 API を MCP ツールとして公開する部分（pkg/mcp/configapi） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C09-19](#g-c09-servers-gateways-security-19) | Elastic — Kibana Agent Builder（elastic/kibana）— 自社ツールのレビュー基準 | サーバの文書 | 作者への書き方の案内・確認を求める・宣言を書くことを求める | [確認] |
| [C09-20](#g-c09-servers-gateways-security-20) | Elastic — Kibana Agent Builder（elastic/kibana） | サーバのソースコード | 作者への書き方の案内・その他 | [確認] |
| [C09-21](#g-c09-servers-gateways-security-21) | Stacklok — ToolHive（MCP サーバーの実行・プロキシ）— Cedar 認可 | ゲートウェイの文書 | 規則（ポリシー）の条件に使う・そのまま渡す・見せる | [確認] |
| [C09-22](#g-c09-servers-gateways-security-22) | Stacklok — ToolHive — Cedar 認可 | ゲートウェイの文書 | 宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [C09-23](#g-c09-servers-gateways-security-23) | Stacklok — ToolHive — Cedar 認可（Safe tools プロファイル） | ゲートウェイの文書 | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C09-24](#g-c09-servers-gateways-security-24) | Stacklok — ToolHive（stacklok/toolhive）— 認可の注釈の型 | ゲートウェイのソースコード | 規則（ポリシー）の条件に使う・信頼するなという注意 | [確認] |
| [C09-25](#g-c09-servers-gateways-security-25) | Stacklok — ToolHive Virtual MCP（vMCP）— 複合ツール | ゲートウェイのソースコード | 宣言が無いときの扱い・宣言を検査する・その他 | [確認] |
| [C09-26](#g-c09-servers-gateways-security-26) | Stacklok — ToolHive Virtual MCP（vMCP）— ツールの上書き | ゲートウェイのソースコード | そのまま渡す・見せる・その他 | [確認] |
| [C09-27](#g-c09-servers-gateways-security-27) | Speakeasy — Speakeasy MCP gateway / Gram — ツール呼び出しごとの RBAC | 公式ブログ | 規則（ポリシー）の条件に使う | [確認] |
| [C09-28](#g-c09-servers-gateways-security-28) | Speakeasy — Speakeasy MCP gateway / Gram — 管理者が記録する注釈 | 公式ブログ | 信頼するなという注意・その他 | [確認] |
| [C09-29](#g-c09-servers-gateways-security-29) | Speakeasy — Gram（speakeasy-api/gram） | ゲートウェイのソースコード | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C09-30](#g-c09-servers-gateways-security-30) | Speakeasy — Gram（speakeasy-api/gram） | ゲートウェイのソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C09-31](#g-c09-servers-gateways-security-31) | Speakeasy — Gram（speakeasy-api/gram）— リスクポリシーの MCP 範囲 | ゲートウェイのソースコード | 危険度を付ける・規則（ポリシー）の条件に使う | [確認] |
| [C09-32](#g-c09-servers-gateways-security-32) | IBM — ContextForge（IBM/mcp-context-forge、MCP ゲートウェイ） | ゲートウェイの文書 | その他・そのまま渡す・見せる | [確認] |
| [C09-33](#g-c09-servers-gateways-security-33) | IBM — ContextForge（IBM/mcp-context-forge） | ゲートウェイの文書 | 作者への書き方の案内 | [確認] |
| [C09-34](#g-c09-servers-gateways-security-34) | MetaMCP（metatool-ai） — MetaMCP（MCP の集約・ゲートウェイ） | ゲートウェイの文書 | その他・そのまま渡す・見せる | [確認] |
| [C09-35](#g-c09-servers-gateways-security-35) | Docker — Docker MCP Catalog（docker/mcp-registry のカタログ生成） | ゲートウェイのソースコード | そのまま渡す・見せる | [確認] |
| [C09-36](#g-c09-servers-gateways-security-36) | Complira — HintLint（complira/hintlint） | 検査の道具の文書 | 宣言を検査する | [確認] |
| [C09-37](#g-c09-servers-gateways-security-37) | Complira — HintLint — Finding Reference | 検査の道具の文書 | 宣言を検査する | [確認] |
| [C09-38](#g-c09-servers-gateways-security-38) | Complira — HintLint — Finding Reference | 検査の道具の文書 | 宣言を検査する・宣言が無いときの扱い | [確認] |
| [C09-39](#g-c09-servers-gateways-security-39) | Complira — HintLint — Registry Artifact | 検査の道具の文書 | 宣言を検査する・その他 | [確認] |
| [C09-40](#g-c09-servers-gateways-security-40) | mcpcheck（個人開発 rajanaggarwal11） — mcpcheck | 検査の道具の文書 | 宣言を検査する・宣言が無いときの扱い | [確認] |
| [C09-41](#g-c09-servers-gateways-security-41) | Nova-Hunting（Nova Proximity） — Nova Proximity（MCP サーバーの調査ツール） | 検査の道具のソースコード | 表示（印・名前） | [確認] |
| [C09-42](#g-c09-servers-gateways-security-42) | Glama — Glama（MCP ディレクトリ・レジストリ） | 公式の文書 | そのまま渡す・見せる・その他 | [確認] |
| [C09-43](#g-c09-servers-gateways-security-43) | Glama — Tool Definition Quality Score（glama-ai/tool-definition-quality-score） | 公式の文書 | 危険度を付ける・宣言を検査する | [確認] |
| [C09-44](#g-c09-servers-gateways-security-44) | Smithery — Smithery Connect API | 公式の文書 | そのまま渡す・見せる | [確認] |
| [G2GP-01](#g-g2-gateways-platforms-01) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | 公式の文書 | そのまま渡す・見せる・その他 | [確認] |
| [G2GP-02](#g-g2-gateways-platforms-02) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | 公式の文書 | 作者への書き方の案内・その他 | [確認] |
| [G2GP-03](#g-g2-gateways-platforms-03) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | 公式の文書 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G2GP-04](#g-g2-gateways-platforms-04) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | 公式の文書 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G2GP-05](#g-g2-gateways-platforms-05) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [G2GP-06](#g-g2-gateways-platforms-06) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） | リリースノート | その他・そのまま渡す・見せる | [確認] |
| [G2GP-07](#g-g2-gateways-platforms-07) | TrueFoundry — TrueFoundry Agent Platform（TrueForge のマネージド版） | 公式の文書 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G2GP-08](#g-g2-gateways-platforms-08) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools | SDK の文書 | 確認を求める・確認を省く（自動で許可） | [確認] |
| [G2GP-09](#g-g2-gateways-platforms-09) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools | SDK の文書 | 宣言が無いときの扱い・確認を省く（自動で許可） | [確認] |
| [G2GP-10](#g-g2-gateways-platforms-10) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools | SDK の文書 | 宣言が無いときの扱い・確認を省く（自動で許可） | [確認] |
| [G2GP-11](#g-g2-gateways-platforms-11) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — @write / @destructive 選択子の解決 | SDK のソースコード | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [G2GP-12](#g-g2-gateways-platforms-12) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認の既定値 | SDK のソースコード | 宣言が無いときの扱い・確認を求める | [確認] |
| [G2GP-13](#g-g2-gateways-platforms-13) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — Code Mode の破壊的ツール拒否 | SDK のソースコード | 宣言が無いときの扱い・ツールを絞る・隠す | [確認] |
| [G2GP-14](#g-g2-gateways-platforms-14) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — Code Mode の破壊的ツール拒否 | SDK のソースコード | ツールを絞る・隠す・確認を求める | [確認] |
| [G2GP-15](#g-g2-gateways-platforms-15) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認既定値の変遷 | リリースノート | 宣言が無いときの扱い・確認を求める | [確認] |
| [G2GP-16](#g-g2-gateways-platforms-16) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認既定値の変遷 | リリースノート | 宣言が無いときの扱い・確認を求める | [確認] |
| [G2GP-17](#g-g2-gateways-platforms-17) | TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge UI — ツール選択画面の分類 | クライアントのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [G2GP-18](#g-g2-gateways-platforms-18) | TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） × Databricks managed MCP | 公式ブログ | 規則（ポリシー）の条件に使う・確認を求める | [確認] |
| [G2GP-19](#g-g2-gateways-platforms-19) | Zuplo — Zuplo MCP Gateway — capability filtering（projection） | 公式の文書 | その他・そのまま渡す・見せる | [確認] |
| [G2GP-20](#g-g2-gateways-platforms-20) | Zuplo — Zuplo MCP Gateway — capability filtering（projection） | 公式の文書 | そのまま渡す・見せる・宣言が無いときの扱い | [確認] |
| [G2GP-21](#g-g2-gateways-platforms-21) | Zuplo — Zuplo MCP Gateway — mcp-capability-filter-inbound ポリシー | 公式の文書 | そのまま渡す・見せる・その他 | [確認] |
| [G2GP-22](#g-g2-gateways-platforms-22) | Zuplo — Zuplo MCP Server handler（OpenAPI ルートを MCP ツールとして公開） | 公式の文書 | 作者への書き方の案内 | [確認] |
| [G2GP-23](#g-g2-gateways-platforms-23) | agentic-community（AWS 系 OSS） — MCP Gateway & Registry（agentic-community/mcp-gateway-registry） | サーバのソースコード | 使わない・読まない | [確認] |
| [G2GP-50](#g-g2-gateways-platforms-50) | agentic-community（AWS 系 OSS） — MCP Gateway & Registry（agentic-community/mcp-gateway-registry） | issue / PR / 提案の下書き | 使わない・読まない | [未確認] |
| [G2GP-24](#g-g2-gateways-platforms-24) | Permit.io — Permit MCP Gateway | 公式の文書 | 使わない・読まない・危険度を付ける | [確認] |
| [G2GP-25](#g-g2-gateways-platforms-25) | Permit.io — Permit MCP Gateway | 公式の文書 | 宣言が無いときの扱い・確認を省く（自動で許可） | [確認] |
| [G2GP-26](#g-g2-gateways-platforms-26) | Permit.io — Permit MCP Gateway — Consent Service | 公式の文書 | 使わない・読まない・表示（印・名前） | [確認] |
| [G2GP-27](#g-g2-gateways-platforms-27) | Google Cloud — Apigee API hub リモート MCP サーバー（apihub.googleapis.com） | 公式の文書 | 表示（印・名前） | [確認] |
| [G2GP-28](#g-g2-gateways-platforms-28) | DataHub（Acryl Data） — DataHub MCP Server | 公式の文書 | 作者への書き方の案内・確認を求める | [確認] |
| [G2GP-29](#g-g2-gateways-platforms-29) | DataHub（Acryl Data） — DataHub MCP Server — 変更系ツール | 公式の文書 | 確認を求める・作者への書き方の案内 | [確認] |
| [G2GP-30](#g-g2-gateways-platforms-30) | LangGenius — Dify（ローコード基盤）の MCP ツール取り込み | クライアントのソースコード | 表示（印・名前）・使わない・読まない | [確認] |
| [G2GP-31](#g-g2-gateways-platforms-31) | LangGenius — Dify — 同梱の MCP 型定義 | クライアントのソースコード | 使わない・読まない・信頼するなという注意 | [確認] |
| [G2GP-32](#g-g2-gateways-platforms-32) | Arcade.dev — Arcade MCP server framework（arcade_mcp_server）— ToolMetadata | SDK の文書 | 作者への書き方の案内・そのまま渡す・見せる | [確認] |
| [G2GP-33](#g-g2-gateways-platforms-33) | Arcade.dev — Arcade — ToolMetadata の利用者（ポリシーエンジン） | SDK の文書 | 規則（ポリシー）の条件に使う・確認を求める・ツールを絞る・隠す | [確認] |
| [G2GP-34](#g-g2-gateways-platforms-34) | Arcade.dev — Arcade — ToolMetadata の矛盾検査 | SDK の文書 | 宣言を検査する | [確認] |
| [G2GP-35](#g-g2-gateways-platforms-35) | Arcade.dev — Arcade — ToolMetadata の矛盾検査 | SDK の文書 | 宣言を検査する | [確認] |
| [G2GP-36](#g-g2-gateways-platforms-36) | Arcade.dev — Arcade — ToolMetadata の MCP 揃えフラグ | SDK の文書 | 作者への書き方の案内 | [確認] |
| [G2GP-37](#g-g2-gateways-platforms-37) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy（mcpproxy-go）— DeriveCallWith | 公式ブログ | 宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [G2GP-38](#g-g2-gateways-platforms-38) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — intent validation | 公式ブログ | 規則（ポリシー）の条件に使う・宣言を検査する | [確認] |
| [G2GP-39](#g-g2-gateways-platforms-39) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — quarantine（ツール変更の検出） | 公式ブログ | 使わない・読まない | [確認] |
| [G2GP-40](#g-g2-gateways-platforms-40) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — DeriveCallWith（現行コード） | サーバのソースコード | 宣言が無いときの扱い・確認を省く（自動で許可） | [確認] |
| [G2GP-41](#g-g2-gateways-platforms-41) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — DeriveCallWith（現行コード） | サーバのソースコード | 宣言が無いときの扱い | [確認] |
| [G2GP-42](#g-g2-gateways-platforms-42) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — direct モードの権限判定 | サーバのソースコード | 規則（ポリシー）の条件に使う・ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [G2GP-43](#g-g2-gateways-platforms-43) | MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — AnnotationTier（プロファイルの tier） | サーバのソースコード | 宣言が無いときの扱い・危険度を付ける | [確認] |
| [G2GP-44](#g-g2-gateways-platforms-44) | Workato — Workato Enterprise MCP（MCP Server 作成 UX） | リリースノート | 作者への書き方の案内・確認を求める・確認を省く（自動で許可） | [確認] |
| [G2GP-45](#g-g2-gateways-platforms-45) | Workato — Workato Enterprise MCP（MCP Server 作成 UX） | リリースノート | 作者への書き方の案内 | [確認] |
| [G2GP-46](#g-g2-gateways-platforms-46) | Composio — Composio Tool Router セッション — 振る舞いタグ | 公式の文書 | ツールを絞る・隠す・その他 | [確認] |
| [G2GP-47](#g-g2-gateways-platforms-47) | Composio — Composio Tool Router セッション — 振る舞いタグ | 公式の文書 | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [G2GP-48](#g-g2-gateways-platforms-48) | Composio — Composio Tool Router セッション — 振る舞いタグ | 公式の文書 | ツールを絞る・隠す | [確認] |
| [G2GP-49](#g-g2-gateways-platforms-49) | TrueFoundry / TrueForge — TrueForge — Code Mode の破壊的ツール拒否 | issue / PR / 提案の下書き | 宣言が無いときの扱い | [未確認] |
| [G2GP-51](#g-g2-gateways-platforms-51) | Greenhat Security — GreenGateway（MCP ゲートウェイ） | issue / PR / 提案の下書き | 使わない・読まない・そのまま渡す・見せる | [未確認] |
| [G2VL-01](#g-g2-verifiers-linters-01) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（npm。tools/list を読む静的リンター）— dev.to の紹介記事 | 公式ブログ | 宣言を検査する | [確認] |
| [G2VL-02](#g-g2-verifiers-linters-02) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（導出は宣言を見ない） | 公式ブログ | 宣言を検査する・使わない・読まない | [確認] |
| [G2VL-03](#g-g2-verifiers-linters-03) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（31 サーバーの結果。数値は未検証） | 公式ブログ | 宣言を検査する | [確認] |
| [G2VL-04](#g-g2-verifiers-linters-04) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（手続き） | 公式ブログ | 宣言を検査する | [確認] |
| [G2VL-05](#g-g2-verifiers-linters-05) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（判定できないツールの扱い） | 公式ブログ | 宣言を検査する | [確認] |
| [G2VL-06](#g-g2-verifiers-linters-06) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（自分の誤検出） | 公式ブログ | 宣言を検査する | [確認] |
| [G2VL-07](#g-g2-verifiers-linters-07) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（formael/actlint）— 導出エンジン | 検査の道具のソースコード | 宣言を検査する・使わない・読まない | [確認] |
| [G2VL-08](#g-g2-verifiers-linters-08) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 設計文書（分類段階: destructiveHint:false の扱い） | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-09](#g-g2-verifiers-linters-09) | Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 評価の床（eval/thresholds.json） | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-10](#g-g2-verifiers-linters-10) | vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-server-lint / mcp-doctor（PyPI 0.12.13）— README の検査一覧 | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-11](#g-g2-verifiers-linters-11) | vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — analyzer.py（変異の手がかりの検出） | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-12](#g-g2-verifiers-linters-12) | vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — 実行時ゲート（check_tool_registration） | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-13](#g-g2-verifiers-linters-13) | inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter（PyPI mcp-tool-card-linter 1.0.0）— 危険分類 | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-14](#g-g2-verifiers-linters-14) | inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter — 注釈の矛盾規則 | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-15](#g-g2-verifiers-linters-15) | cejor6（個人開発。npm mcpconform） — mcpconform — 規則 tool/destructive-needs-annotation | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-16](#g-g2-verifiers-linters-16) | hahahahahahahahah6（個人開発。mcp-lint） — mcp-lint（設計リンター）— 規則 destructive-no-confirm | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-17](#g-g2-verifiers-linters-17) | superintelligenceco（mcp-lint） — mcp-lint（MCP サーバーの採点）— capability/missing-annotations | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-18](#g-g2-verifiers-linters-18) | antonsoo（個人開発。mcplint） — mcplint — safety/missing-annotations | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-19](#g-g2-verifiers-linters-19) | DLeibner（個人開発。mcp-surface-lint） — mcp-surface-lint — annotations-missing-hints | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-20](#g-g2-verifiers-linters-20) | StudioMeyer（studiomeyer-io） — mcp-protocol-conformance — annotations 監査スイート | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-21](#g-g2-verifiers-linters-21) | AgentPostmortem（MCP-audit） — MCP-audit — MCP004 readOnlyHint の不一致 | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-22](#g-g2-verifiers-linters-22) | arijitgupta42（個人開発。PyPI mcp-toolgauge 0.1.0） — mcp-toolgauge — MCP040 destructiveHint の欠落 | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-23](#g-g2-verifiers-linters-23) | vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-fuzz（同じ作者の実行型の検査） | 検査の道具のソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [G2VL-24](#g-g2-verifiers-linters-24) | vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-reality-check（同じ作者の実行型の検査） | 検査の道具のソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [G2VL-25](#g-g2-verifiers-linters-25) | himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — dev.to の紹介記事 | 第三者の記事 | 宣言を検査する・確認を求める | [確認] |
| [G2VL-26](#g-g2-verifiers-linters-26) | himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — 検出器（annotation_divergence） | 検査の道具のソースコード | 宣言を検査する | [確認] |
| [G2VL-27](#g-g2-verifiers-linters-27) | himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — README（証拠モード） | 検査の道具の文書 | 宣言を検査する | [確認] |
| [G2VL-28](#g-g2-verifiers-linters-28) | sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations | 第三者の記事 | 宣言を検査する・作者への書き方の案内 | [確認] |
| [G2VL-29](#g-g2-verifiers-linters-29) | sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations（方針表との照合） | 第三者の記事 | 宣言を検査する | [確認] |
| [G2VL-30](#g-g2-verifiers-linters-30) | sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Claude Connector Directory Submission | 第三者の記事 | 宣言を書くことを求める・宣言を検査する | [確認] |
| [G2VL-31](#g-g2-verifiers-linters-31) | bex（bex.co。エージェント向けクラウドの事業者。筆者 Dora Noda） — bex ブログ — dry_run と注釈 | 第三者の記事 | 信頼するなという注意・宣言を検査する | [確認] |
| [G2RM-01](#g-g2-registries-marketplaces-01) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 信頼するなという注意・その他 | [確認] |
| [G2RM-02](#g-g2-registries-marketplaces-02) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | そのまま渡す・見せる | [確認] |
| [G2RM-03](#g-g2-registries-marketplaces-03) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 表示（印・名前） | [確認] |
| [G2RM-04](#g-g2-registries-marketplaces-04) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認] |
| [G2RM-05](#g-g2-registries-marketplaces-05) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [G2RM-06](#g-g2-registries-marketplaces-06) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [G2RM-07](#g-g2-registries-marketplaces-07) | Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール） | サーバのソースコード | 表示（印・名前） | [確認] |
| [G2RM-08](#g-g2-registries-marketplaces-08) | Smithery — Smithery Registry API（GET /servers/{qualifiedName}） | 公式の文書 | 使わない・読まない | [確認] |
| [G2RM-09](#g-g2-registries-marketplaces-09) | Smithery — Smithery（ウェブのサーバー詳細ページ smithery.ai/servers/<name>） | 第三者の記事 | そのまま渡す・見せる | [確認] |
| [G2RM-10](#g-g2-registries-marketplaces-10) | Kong — Kong AI Gateway — AI MCP Proxy プラグイン（REST API を MCP ツールに変換） | 公式の文書 | 作者への書き方の案内 | [確認] |
| [G2RM-11](#g-g2-registries-marketplaces-11) | Kong — Kong AI Gateway — AI MCP Proxy プラグイン（設定スキーマ 3.16） | ゲートウェイの文書 | 作者への書き方の案内・そのまま渡す・見せる | [確認] |
| [G2RM-12](#g-g2-registries-marketplaces-12) | AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部） | 第三者の記事 | 確認を省く（自動で許可）・その他 | [確認] |
| [G2RM-13](#g-g2-registries-marketplaces-13) | AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部） | 第三者の記事 | 確認を省く（自動で許可） | [確認] |
| [G2RM-14](#g-g2-registries-marketplaces-14) | AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部） | 公式の文書 | その他 | [確認] |
| [G2RM-15](#g-g2-registries-marketplaces-15) | CorpusIQ（第三者） — MCP Directory Submission Guide - 2026（第三者のディレクトリ掲載ガイド） | 第三者の記事 | その他 | [確認] |
| [G2RM-16](#g-g2-registries-marketplaces-16) | ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む） | クライアントのソースコード | 規則（ポリシー）の条件に使う・確認を求める・危険度を付ける | [確認] |
| [G2RM-17](#g-g2-registries-marketplaces-17) | ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む） | クライアントのソースコード | 確認を省く（自動で許可）・危険度を付ける | [確認] |
| [G2RM-18](#g-g2-registries-marketplaces-18) | ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む） | クライアントのソースコード | 宣言が無いときの扱い | [確認] |
| [G2RM-19](#g-g2-registries-marketplaces-19) | ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む） | クライアントのソースコード | 危険度を付ける・宣言が無いときの扱い | [確認] |

この分冊の資料は 145 件で、うち [確認] は 142 件、[確認（調査時のみ）] は 0 件。

<a id="ag-10-1"></a>
## 資料カード

### Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— 開発者向け文書

<a id="g-c09-servers-gateways-security-01"></a>
#### C09-01 Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— 開発者向け文書

- **資料**: docs/contributing/adding-tools.md「Safety Annotations」（サーバの文書）
- **URL**: https://github.com/getsentry/sentry-mcp/blob/9358775eda6e312483453d6ec308d7f4f5f78245/docs/contributing/adding-tools.md#L102-L106
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/sentry-mcp/9358775eda6e312483453d6ec308d7f4f5f78245/docs/contributing/adding-tools.md
- **版**: commit 9358775eda6e312483453d6ec308d7f4f5f78245（getsentry/sentry-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L102-106（直前の見出し: ### Safety Annotations）
- **原文**:

```
**REQUIRED**: Every tool must declare `readOnlyHint`, `destructiveHint`, and
`openWorldHint` explicitly (each `true` or `false`, never omitted). This is
enforced at compile time (the `annotations` type requires them) and by
`tools.test.ts`, because filters and confirmation gates depend on these hints;
an absent hint is a silent gap.
```

- **日本語**: すべてのツールは readOnlyHint・destructiveHint・openWorldHint を true か false で必ず明示すること（省略しない）。型（コンパイル時）と tools.test.ts で強制している。フィルタや確認の関門がこれらのヒントに頼るので、ヒントが無いと気づかれない穴になる。
- **どう使っているか**: サーバー作者（Sentry）が自社のツール全部に readOnlyHint・destructiveHint・openWorldHint の明示（true か false）を義務づけ、型とテスト（02）で強制する。理由は「フィルタや確認の関門（confirmation gates）がこれらのヒントに頼るから」（どこのフィルタ・関門かは書かれていない）。idempotentHint は任意（同じ節 L112）。
- **条件**: Sentry MCP リポジトリの内部規則（他のサーバーへの要求ではない）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を書くことを求める・作者への書き方の案内・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、102-106 行（### Safety Annotations）（取得 2026-10-02T22:11:37Z、sha256 543299f3359b…）
- **補足**: 同じ節に「Read-only tools must set `destructiveHint: false` (not leave it undefined).」とあり、読み取り・作成・更新の 3 つの型を例示する（更新は readOnlyHint:false, destructiveHint:true, idempotentHint:true）。packages/mcp-core/src/tools/types.ts L96-97 のコメント「tool declares its safety posture explicitly. Filters and confirmation gates rely on these; an undefined hint is a silent gap.」も verify_quote.py で exact（同じ commit）。 言い過ぎを修正: 原文は「filters and confirmation gates depend on these hints」で、それがクライアント側のものとは書いていない。usage_ja の「クライアント側の」を削除。

### Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）

<a id="g-c09-servers-gateways-security-02"></a>
#### C09-02 Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）

- **資料**: packages/mcp-core/src/tools/tools.test.ts「all tools declare complete MCP safety annotations」（サーバのソースコード）
- **URL**: https://github.com/getsentry/sentry-mcp/blob/9358775eda6e312483453d6ec308d7f4f5f78245/packages/mcp-core/src/tools/tools.test.ts#L62-L85
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/sentry-mcp/9358775eda6e312483453d6ec308d7f4f5f78245/packages/mcp-core/src/tools/tools.test.ts
- **版**: commit 9358775eda6e312483453d6ec308d7f4f5f78245（getsentry/sentry-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L62-85
- **原文**:

```
test("all tools declare complete MCP safety annotations", () => {
  for (const tool of Object.values(tools.default)) {
    // Every tool must declare readOnlyHint, destructiveHint, and openWorldHint
    // explicitly (true or false, never undefined). Filters and confirmation
    // gates rely on these, so an absent hint is a silent gap.
    assert(
      typeof tool.annotations.readOnlyHint === "boolean",
      `${tool.name} must define readOnlyHint (true or false, not undefined)`,
    );
    assert(
      typeof tool.annotations.destructiveHint === "boolean",
      `${tool.name} must define destructiveHint (true or false, not undefined)`,
    );
    assert(
      typeof tool.annotations.openWorldHint === "boolean",
      `${tool.name} must define openWorldHint (true or false, not undefined)`,
    );
    assert(
      !(
        tool.annotations.readOnlyHint === true &&
        tool.annotations.destructiveHint === true
      ),
      `${tool.name} cannot be both read-only and destructive`,
    );
```

- **日本語**: 全ツールについて、readOnlyHint・destructiveHint・openWorldHint が boolean であること（未定義でないこと）と、readOnlyHint と destructiveHint が同時に true でないことをテストで確かめる。
- **どう使っているか**: 宣言の「有無」と「read-only かつ destructive という矛盾」だけを機械的に検査する。宣言がコードの実際の動作と合っているかは検査しない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する・宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、62-85 行（取得 2026-10-02T22:11:33Z、sha256 5ade3f1774c9…）
- **補足**: 01 の規則を実装しているテスト。

### Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— execute_sentry_tool

<a id="g-c09-servers-gateways-security-03"></a>
#### C09-03 Sentry (Functional Software, Inc.) — Sentry MCP server（getsentry/sentry-mcp）— execute_sentry_tool

- **資料**: packages/mcp-core/src/tools/special/execute-tool.ts（サーバのソースコード）
- **URL**: https://github.com/getsentry/sentry-mcp/blob/9358775eda6e312483453d6ec308d7f4f5f78245/packages/mcp-core/src/tools/special/execute-tool.ts#L116-L120
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/sentry-mcp/9358775eda6e312483453d6ec308d7f4f5f78245/packages/mcp-core/src/tools/special/execute-tool.ts
- **版**: commit 9358775eda6e312483453d6ec308d7f4f5f78245（getsentry/sentry-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L116-120
- **原文**:

```
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      openWorldHint: true,
    },
```

- **日本語**: execute_sentry_tool（カタログ内の任意のツールを名前で実行する中継用のツール）の注釈を readOnlyHint:false・destructiveHint:true・openWorldHint:true にしている。
- **どう使っているか**: 他のツールを名前で代わりに実行する中継用ツール execute_sentry_tool に、readOnlyHint:false・destructiveHint:true・openWorldHint:true を付けている実例。カタログに書き込み系のツールもあるので破壊的側に寄せたと考えられるが、理由はソースに書かれていない（推測）。中のツールそれぞれの注釈は search_sentry_tools の結果（annotations 欄）で返す。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、116-120 行（取得 2026-10-02T22:12:57Z、sha256 19e990d7466c…）
- **補足**: name: "execute_sentry_tool" は同ファイル L82。search_sentry_tools 自体は readOnlyHint:true, destructiveHint:false, openWorldHint:false（search-tools.ts L101-105、照合はしていない）。 言い過ぎを修正: ソースには destructiveHint:true にした理由のコメントが無い。「いちばん危ない側に宣言する、という付け方」は推測なので推測と明記。search_sentry_tools の出力スキーマ（toolAnnotationsOutputSchema, search-tools.ts L13-18, L31）で対象ツールごとの注釈を返すことは目視で確認。

### Supabase — Supabase MCP server（supabase-community/supabase-mcp）

<a id="g-c09-servers-gateways-security-04"></a>
#### C09-04 Supabase — Supabase MCP server（supabase-community/supabase-mcp）

- **資料**: packages/mcp-server-supabase/src/tools/tool-schemas.ts: writeToolSet（サーバのソースコード）
- **URL**: https://github.com/supabase-community/supabase-mcp/blob/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/tools/tool-schemas.ts#L148-L161
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/supabase-community/supabase-mcp/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/tools/tool-schemas.ts
- **版**: commit 4602ee9ebf025611741cc127cee2a3c6a4f73854（supabase-community/supabase-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L148-161
- **原文**:

```
/**
 * Tools excluded entirely in read-only mode.
 * Derived from tool defs: any tool with `readOnlyHint: false` and no
 * `readOnlyBehavior: 'adapt'` annotation.
 */
export const writeToolSet = new Set(
  Object.entries(supabaseMcpToolSchemas)
    .filter(
      ([, entry]) =>
        entry.annotations.readOnlyHint === false &&
        entry.readOnlyBehavior !== 'adapt'
    )
    .map(([name]) => name)
);
```

- **日本語**: 読み取り専用モードで完全に外すツールの集合。ツール定義のうち readOnlyHint:false で、readOnlyBehavior:'adapt' でないものから自動で作る。
- **どう使っているか**: サーバー自身が、自分で書いた readOnlyHint の宣言を使って、read_only モードで出さないツールを決める（宣言が実際の絞り込みの入力になる）。
- **条件**: サーバーを read_only=true で動かすとき（ホスト版は URL パラメータ）。createToolSchemas({readOnly:true}) も同じ集合で除外する（同ファイル L279）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、148-161 行（取得 2026-10-02T22:12:06Z、sha256 3914e58a67d1…）
- **補足**: 宣言を書き間違えると（書き込むツールに readOnlyHint:true）read_only モードでも残る、という依存関係になる。実行時の二重の守りは 05 の notes を参照。 [verifier] conditions の「ホスト版は URL パラメータ」は Supabase 文書の read_only=true（「Execute all queries as a read-only Postgres user」exact, #configuration-options）で確認。

<a id="g-c09-servers-gateways-security-05"></a>
#### C09-05 Supabase — Supabase MCP server（supabase-community/supabase-mcp）

- **資料**: packages/mcp-server-supabase/src/server.ts（read-only 時のツール隠し）（サーバのソースコード）
- **URL**: https://github.com/supabase-community/supabase-mcp/blob/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/server.ts#L325-L331
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/supabase-community/supabase-mcp/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/server.ts
- **版**: commit 4602ee9ebf025611741cc127cee2a3c6a4f73854（supabase-community/supabase-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L325-331
- **原文**:

```
      if (readOnly) {
        for (const [name, tool] of Object.entries(tools)) {
          if (writeToolSet.has(name)) {
            tools[name] = { ...tool, hidden: true };
          }
        }
      }
```

- **日本語**: read-only のときは、writeToolSet に入るツールをすべて hidden: true にする。
- **どう使っているか**: readOnlyHint:false から作った集合（04）のツールを tools/list から隠す。
- **条件**: readOnly が true のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、325-331 行（取得 2026-10-02T22:11:45Z、sha256 a97deaa8ef5a…）
- **補足**: util.ts L13 の hidden の説明は「If true, excludes the tool from `tools/list` while keeping it callable via `tools/call`.」（exact）。つまり隠すだけでは呼び出しは止まらないが、書き込みツールは実行時にも readOnly を確かめる（例: database-operation-tools.ts L393「throw new Error('Cannot apply migration in read-only mode.');」exact）。

### Supabase — Supabase MCP server（supabase-community/supabase-mcp）— execute_sql

<a id="g-c09-servers-gateways-security-06"></a>
#### C09-06 Supabase — Supabase MCP server（supabase-community/supabase-mcp）— execute_sql

- **資料**: packages/mcp-server-supabase/src/tools/database-operation-tools.ts: execute_sql（サーバのソースコード）
- **URL**: https://github.com/supabase-community/supabase-mcp/blob/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/tools/database-operation-tools.ts#L453-L458
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/supabase-community/supabase-mcp/4602ee9ebf025611741cc127cee2a3c6a4f73854/packages/mcp-server-supabase/src/tools/database-operation-tools.ts
- **版**: commit 4602ee9ebf025611741cc127cee2a3c6a4f73854（supabase-community/supabase-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L453-458
- **原文**:

```
    execute_sql: injectableTool({
      ...databaseToolDefs.execute_sql,
      annotations: {
        ...databaseToolDefs.execute_sql.annotations,
        readOnlyHint: readOnly ?? false,
      },
```

- **日本語**: execute_sql の注釈を、read-only モードなら readOnlyHint:true、そうでなければ false に切り替える。
- **どう使っているか**: 宣言をサーバーの設定に合わせて動的に変える例。read-only モードでは SQL を read_only: readOnly で実行し（同ファイル L512-515）、公開文書は「read-only の Postgres ユーザーで実行」と説明する（checked_no_mention の Supabase 文書）。宣言の裏に実行側（DB 権限）の強制がある。
- **条件**: read_only=true のときだけ readOnlyHint:true。既定の定義は readOnlyHint:false, destructiveHint:true, idempotentHint:false, openWorldHint:true（L199-207）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、453-458 行（取得 2026-10-02T22:11:39Z、sha256 3dc02440b684…）
- **補足**: execute_sql は readOnlyBehavior:'adapt'（read-only モードでも残して振る舞いを変える）なので 04 の除外集合には入らない。

### Supabase — Supabase MCP server（supabase-community/supabase-mcp）— 開発者向け文書

<a id="g-c09-servers-gateways-security-07"></a>
#### C09-07 Supabase — Supabase MCP server（supabase-community/supabase-mcp）— 開発者向け文書

- **資料**: CONTRIBUTING.md「Breaking changes」（サーバの文書）
- **URL**: https://github.com/supabase-community/supabase-mcp/blob/4602ee9ebf025611741cc127cee2a3c6a4f73854/CONTRIBUTING.md#L190-L194
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/supabase-community/supabase-mcp/4602ee9ebf025611741cc127cee2a3c6a4f73854/CONTRIBUTING.md
- **版**: commit 4602ee9ebf025611741cc127cee2a3c6a4f73854（supabase-community/supabase-mcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L190-194（直前の見出し: ## Breaking changes）
- **原文**:

> ChatGPT snapshots MCP metadata during plugin submission. Several fields are frozen for published ChatGPT users until a new plugin version is published, including:
>
> - Tool list, names, titles, and descriptions
> - Input and output schemas
> - Tool annotations

- **日本語**: ChatGPT はプラグイン提出時に MCP のメタデータを写し取る。新しい版を出すまで、公開済みの ChatGPT 利用者向けには、ツール一覧・名前・タイトル・説明、入出力スキーマ、ツール注釈などが固定される。
- **どう使っているか**: サーバー作者が、注釈を「tools/list の公開 API 契約の一部」として扱っている。ChatGPT 向けには提出時点で凍結されるので、注釈を直しても再提出まで反映されない。Claude Connectors にはこの制約がない、と同じ節に書く。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、190-194 行（## Breaking changes）（取得 2026-10-02T22:11:37Z、sha256 81d69a741aac…）
- **補足**: OpenAI 側の一次資料（Apps SDK の submission 文書）は C05 の範囲。ここでは Supabase の記述として記録。

### Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— 実装手引き

<a id="g-c09-servers-gateways-security-08"></a>
#### C09-08 Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— 実装手引き

- **資料**: implementation-guides/tools.md「Best practices」（サーバの文書）
- **URL**: https://github.com/cloudflare/mcp-server-cloudflare/blob/ab883e51663df955316ec3191afb5b718bf4b54c/implementation-guides/tools.md#L118-L118
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cloudflare/mcp-server-cloudflare/ab883e51663df955316ec3191afb5b718bf4b54c/implementation-guides/tools.md
- **版**: commit ab883e51663df955316ec3191afb5b718bf4b54c（cloudflare/mcp-server-cloudflare の 2026-10-02 時点の HEAD）
- **書いてある場所**: L118（直前の見出し: ## Best practices）
- **原文**:

> - Mark read-only or destructive behavior accurately with tool annotations.

- **日本語**: 読み取り専用か破壊的かを、ツール注釈で正確に示すこと。
- **どう使っているか**: Cloudflare の MCP サーバー群の実装手引き。「正確に付ける」とだけ書き、何をもって正確とするかの基準や検査は書かない。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、118 行（## Best practices）（取得 2026-10-02T22:12:00Z、sha256 9a06cde0cb3d…）
- **補足**: 同ファイルのテンプレート例は annotations: { title: 'Human-readable tool title', readOnlyHint: true }（L46-49）。

### Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— Workers Bindings の d1_database_query

<a id="g-c09-servers-gateways-security-09"></a>
#### C09-09 Cloudflare — Cloudflare MCP servers（cloudflare/mcp-server-cloudflare）— Workers Bindings の d1_database_query

- **資料**: apps/workers-bindings/src/tools/d1.tools.ts（サーバのソースコード）
- **URL**: https://github.com/cloudflare/mcp-server-cloudflare/blob/ab883e51663df955316ec3191afb5b718bf4b54c/apps/workers-bindings/src/tools/d1.tools.ts#L193-L206
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cloudflare/mcp-server-cloudflare/ab883e51663df955316ec3191afb5b718bf4b54c/apps/workers-bindings/src/tools/d1.tools.ts
- **版**: commit ab883e51663df955316ec3191afb5b718bf4b54c（cloudflare/mcp-server-cloudflare の 2026-10-02 時点の HEAD）
- **書いてある場所**: L193-206
- **原文**:

```
	context.accountTool(
		'd1_database_query',
		{
			description: 'Query a D1 database in your Cloudflare account',
			inputSchema: z.object({
				database_id: z.string(),
				sql: D1DatabaseQuerySqlParam,
				params: D1DatabaseQueryParamsParam.nullable(),
			}),
			annotations: {
				title: 'Query D1 database',
				readOnlyHint: false,
				destructiveHint: false,
			},
```

- **日本語**: d1_database_query（D1 データベースに SQL をそのまま流すツール）の注釈を readOnlyHint:false・destructiveHint:false にしている。
- **どう使っているか**: 任意の SQL を受けるツールを「破壊的でない」と宣言している実例。Grafana の query_sql（10、destructiveHint:true）と判断が逆で、08 の「正確に付ける」という手引きがあっても、任意文を受けるツールの付け方はサーバーごとに揺れる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、193-206 行（取得 2026-10-02T22:11:34Z、sha256 a6eedff3268d…）
- **補足**: 本体は client.d1.database.query(database_id, {account_id, sql, params}) を呼ぶだけで（L208-216）、このファイルには SQL の種類の検査が無い。削除ツール d1_database_delete は readOnlyHint:false, destructiveHint:true（L119-121、exact）。宣言が誤りかどうかの判定は本調査ではしない。 [verifier] openWorldHint・idempotentHint は未宣言。 補足のみ: この定義は openWorldHint と idempotentHint を書いていない（仕様の既定では openWorld=true, idempotent=false）。

### Grafana Labs — Grafana MCP server（grafana/mcp-grafana）— query_sql

<a id="g-c09-servers-gateways-security-10"></a>
#### C09-10 Grafana Labs — Grafana MCP server（grafana/mcp-grafana）— query_sql

- **資料**: tools/sql_tools.go: QuerySQL（サーバのソースコード）
- **URL**: https://github.com/grafana/mcp-grafana/blob/dd1c00d316fa315f60c0bf36974f229a3209a541/tools/sql_tools.go#L273-L277
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/grafana/mcp-grafana/dd1c00d316fa315f60c0bf36974f229a3209a541/tools/sql_tools.go
- **版**: commit dd1c00d316fa315f60c0bf36974f229a3209a541（grafana/mcp-grafana の 2026-10-02 時点の HEAD）
- **書いてある場所**: L273-277
- **原文**:

> 	mcpgrafana.WithTitleAnnotation("Query SQL"),
> 	mcpgrafana.WithIdempotentHintAnnotation(false),
> 	mcpgrafana.WithReadOnlyHintAnnotation(false),
> 	mcpgrafana.WithDestructiveHintAnnotation(true),
> 	mcpgrafana.WithOpenWorldHintAnnotation(false),

- **日本語**: query_sql の注釈: タイトル「Query SQL」、idempotentHint:false、readOnlyHint:false、destructiveHint:true、openWorldHint:false。
- **どう使っているか**: 任意の SQL を素通しするツールを破壊的と宣言する例（09 の Cloudflare と逆）。
- **扱う宣言**: title・idempotentHint・readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、273-277 行（取得 2026-10-02T22:11:35Z、sha256 f1850849f8c9…）
- **補足**: ツール名は L261-262（var QuerySQL = mcpgrafana.MustTool("query_sql", …)）。--disable-write を付けると既定では登録されず、--enable-query（または --enable-write-tools=query_sql）で戻せる。その flag の説明（cmd/mcp-grafana/main.go L231）に「They pass the query through unfiltered, so they can mutate data if the datasource credentials permit it」（exact）。--disable-write は注釈を読むのではなく、ツール群ごとの登録フラグで実装されている。 表現を明確化: 「--disable-write の既定では登録されず」は曖昧なので「--disable-write を付けると既定では登録されない」に直した。main.go L231 の引用は再照合で exact。

### Grafana Labs — Grafana MCP server（grafana/mcp-grafana）

<a id="g-c09-servers-gateways-security-11"></a>
#### C09-11 Grafana Labs — Grafana MCP server（grafana/mcp-grafana）

- **資料**: cmd/mcp-grafana/annotations_test.go: TestAllToolsDeclareAnnotationHints（サーバのソースコード）
- **URL**: https://github.com/grafana/mcp-grafana/blob/dd1c00d316fa315f60c0bf36974f229a3209a541/cmd/mcp-grafana/annotations_test.go#L43-L79
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/grafana/mcp-grafana/dd1c00d316fa315f60c0bf36974f229a3209a541/cmd/mcp-grafana/annotations_test.go
- **版**: commit dd1c00d316fa315f60c0bf36974f229a3209a541（grafana/mcp-grafana の 2026-10-02 時点の HEAD）
- **書いてある場所**: L43-79
- **原文**:

```
// TestAllToolsDeclareAnnotationHints asserts that every tool exposed by the
// server explicitly sets the three MCP tool annotations readOnlyHint,
// destructiveHint and openWorldHint.
func TestAllToolsDeclareAnnotationHints(t *testing.T) {
	for _, disableWrite := range []bool{false, true} {
		name := "write-enabled"
		if disableWrite {
			name = "write-disabled"
		}
		t.Run(name, func(t *testing.T) {
			var violations []string
			for _, tool := range listAllTools(t, disableWrite) {
				ann := tool.Annotations
				if ann == nil {
					violations = append(violations, fmt.Sprintf("%s: missing annotations", tool.Name))
					continue
				}
				var missing []string
				// go-sdk limitation: ReadOnlyHint and IdempotentHint are bool,
				// so zero-value false is indistinguishable from "not set".
				// We rely on the ann != nil check above (every tool must call
				// at least one With*Annotation) and the conflict check below
				// to catch mis-labelled tools. DestructiveHint and OpenWorldHint
				// are *bool, so nil detection still works for those.
				if ann.DestructiveHint == nil {
					missing = append(missing, "destructiveHint")
				}
				if ann.OpenWorldHint == nil {
					missing = append(missing, "openWorldHint")
				}
				if len(missing) > 0 {
					violations = append(violations, fmt.Sprintf("%s: missing %s", tool.Name, strings.Join(missing, ", ")))
					continue
				}
				if ann.ReadOnlyHint && *ann.DestructiveHint {
					violations = append(violations, fmt.Sprintf("%s: readOnlyHint=true conflicts with destructiveHint=true", tool.Name))
				}
```

- **日本語**: すべてのツールが readOnlyHint・destructiveHint・openWorldHint を明示しているかを確かめるテスト。go-sdk では ReadOnlyHint と IdempotentHint が bool なので、false と「未設定」を区別できない。そこで注釈オブジェクトがあることと、readOnlyHint=true と destructiveHint=true の矛盾を確かめる。
- **どう使っているか**: 書き込み有効・無効の両方の構成で tools/list を取り、注釈オブジェクトの有無、destructiveHint・openWorldHint の明示、readOnlyHint=true と destructiveHint=true の矛盾を検査する。go-sdk の型では ReadOnlyHint・IdempotentHint が bool なので、サーバー内部では false と「未設定」を区別できない、とコメントで認めている（readOnlyHint の明示そのものは検査できない）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint ／ **使い方の分類**: 宣言を検査する・宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、43-79 行（取得 2026-10-02T22:11:42Z、sha256 a42800f04fd9…）
- **補足**: AuthGap への含意: go-sdk v1.8.0（Grafana・Pomerium が使用）の ToolAnnotations は ReadOnlyHint / IdempotentHint が omitempty なしの bool（https://github.com/modelcontextprotocol/go-sdk/blob/v1.8.0/mcp/protocol.go#L1978-L1988）なので、go-sdk 製サーバーの tools/list には作者が書いていなくても readOnlyHint:false・idempotentHint:false が必ず出る。「宣言あり」を JSON 上の有無で数えると go-sdk 製サーバーは過大に数えられる。仕様の既定値も false なので意味は変わらない。 誤りを修正: 「readOnlyHint:false は JSON に出ない／未設定と同じに見える」は誤り。Grafana が使う go-sdk v1.8.0（go.mod L19, exact）では ReadOnlyHint と IdempotentHint は omitempty の無い bool（protocol.go L1988 `ReadOnlyHint bool `json:"readOnlyHint"``・L1978、exact）なので、作者が書かなくても JSON には常に readOnlyHint:false / idempotentHint:false が出る。区別できないのはサーバー内部（Go の値）で、クライアントから見ると「未設定」が「明示の false」に化ける、が正しい。

### MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server）

<a id="g-c09-servers-gateways-security-12"></a>
#### C09-12 MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server）

- **資料**: packages/core/src/toolBase.ts: ToolBase.annotations（サーバのソースコード）
- **URL**: https://github.com/mongodb-js/mongodb-mcp-server/blob/b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d/packages/core/src/toolBase.ts#L462-L489
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mongodb-js/mongodb-mcp-server/b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d/packages/core/src/toolBase.ts
- **版**: commit b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d（mongodb-js/mongodb-mcp-server の 2026-10-02 時点の HEAD）
- **書いてある場所**: L462-489
- **原文**:

```
    public get annotations(): ToolAnnotations {
        const annotations: ToolAnnotations = {
            title: this.name,
            openWorldHint: true,
        };

        switch (this.operationType) {
            case "read":
            case "metadata":
            case "connect":
                annotations.readOnlyHint = true;
                annotations.destructiveHint = false;
                break;
            case "delete":
            case "update":
                annotations.readOnlyHint = false;
                annotations.destructiveHint = true;
                break;
            case "create":
                annotations.destructiveHint = false;
                annotations.readOnlyHint = false;
                break;
            default:
                break;
        }

        return annotations;
    }
```

- **日本語**: 注釈は title（ツール名）と openWorldHint:true を基本に、操作の種類（operationType）から決める。read・metadata・connect は readOnlyHint:true / destructiveHint:false、delete・update は readOnlyHint:false / destructiveHint:true、create は両方 false。
- **どう使っているか**: ツールごとに手で書かず、内部の分類（operationType）から機械的に導く。同じ分類が --readOnly モードの登録判定（13）にも使われるので、宣言とサーバー側の強制が同じ源を持つ。
- **扱う宣言**: title・readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、462-489 行（取得 2026-10-02T22:11:36Z、sha256 4d736eac2c59…）
- **補足**: idempotentHint は付けない。update を destructiveHint:true にする（Pomerium の Update* は破壊的でない、18 と逆）。

### MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server）— read-only モード

<a id="g-c09-servers-gateways-security-13"></a>
#### C09-13 MongoDB — MongoDB MCP server（mongodb-js/mongodb-mcp-server）— read-only モード

- **資料**: packages/core/src/toolBase.ts: verifyAllowed（サーバのソースコード）
- **URL**: https://github.com/mongodb-js/mongodb-mcp-server/blob/b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d/packages/core/src/toolBase.ts#L842-L855
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mongodb-js/mongodb-mcp-server/b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d/packages/core/src/toolBase.ts
- **版**: commit b5c4bb42e743a2d4c4fc950d1e236ce9c31c6f6d（mongodb-js/mongodb-mcp-server の 2026-10-02 時点の HEAD）
- **書いてある場所**: L842-855
- **原文**:

```
    // Checks if a tool is allowed to run based on the config
    protected verifyAllowed(): boolean {
        let errorClarification: string | undefined;

        // Check read-only mode first
        if (this.server.config.readOnly && !["read", "metadata", "connect"].includes(this.operationType)) {
            errorClarification = `read-only mode is enabled, its operation type, \`${this.operationType}\`,`;
        } else if (this.server.config.disabledTools.includes(this.category)) {
            errorClarification = `its category, \`${this.category}\`,`;
        } else if (this.server.config.disabledTools.includes(this.operationType)) {
            errorClarification = `its operation type, \`${this.operationType}\`,`;
        } else if (this.server.config.disabledTools.includes(this.name)) {
            errorClarification = `it`;
        }
```

- **日本語**: 設定に基づいてツールを動かしてよいか確かめる。まず read-only モードなら、operationType が read・metadata・connect 以外のツールを外す。次に disabledTools にカテゴリ・操作種別・名前が入っていれば外す。
- **どう使っているか**: サーバー側の read-only モード。注釈そのものは読まないが、注釈（12）と同じ operationType で判断するので、結果として readOnlyHint:true のツールだけが残る。
- **条件**: config.readOnly が true のとき（register() の最初で verifyAllowed() を呼び、false なら登録しない、L743-746）。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、842-855 行（取得 2026-10-02T22:11:36Z、sha256 4d736eac2c59…）

### Neo4j（neo4j-contrib, Neo4j Labs） — mcp-neo4j-cypher（neo4j-contrib/mcp-neo4j、Python / FastMCP）

<a id="g-c09-servers-gateways-security-14"></a>
#### C09-14 Neo4j（neo4j-contrib, Neo4j Labs） — mcp-neo4j-cypher（neo4j-contrib/mcp-neo4j、Python / FastMCP）

- **資料**: servers/mcp-neo4j-cypher/src/mcp_neo4j_cypher/server.py: read_neo4j_cypher（サーバのソースコード）
- **URL**: https://github.com/neo4j-contrib/mcp-neo4j/blob/1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7/servers/mcp-neo4j-cypher/src/mcp_neo4j_cypher/server.py#L178-L197
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neo4j-contrib/mcp-neo4j/1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7/servers/mcp-neo4j-cypher/src/mcp_neo4j_cypher/server.py
- **版**: commit 1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7（neo4j-contrib/mcp-neo4j の 2026-10-02 時点の HEAD）
- **書いてある場所**: L178-197
- **原文**:

```
    @mcp.tool(
        name=namespace_prefix + "read_neo4j_cypher",
        annotations=ToolAnnotations(
            title="Read Neo4j Cypher",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
        ),
    )
    async def read_neo4j_cypher(
        query: str = Field(..., description="The Cypher query to execute."),
        params: dict[str, Any] = Field(
            dict(), description="The parameters to pass to the Cypher query."
        ),
    ) -> list[ToolResult]:
        """Execute a read Cypher query on the neo4j database."""

        if await _is_write_query(query, neo4j_driver, database):
            raise ValueError("Only MATCH queries are allowed for read-query")
```

- **日本語**: read_neo4j_cypher を readOnlyHint=True・destructiveHint=False・idempotentHint=True・openWorldHint=True と宣言し、実行前に _is_write_query で書き込みクエリかを調べ、書き込みなら ValueError にする。
- **どう使っているか**: Python サーバーで、readOnlyHint:true の宣言を実行前の検査（EXPLAIN の query_type）で裏づける例。宣言と実装を合わせる仕組みがサーバーの中にある。ただし query_type "s"（スキーマ書き込み）は "w" を含まないのでこの検査では通る（限界）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、178-197 行（取得 2026-10-02T22:11:38Z、sha256 b0103b1949e5…）
- **補足**: _is_write_query（L31-39）は EXPLAIN を付けて実行し、summary.query_type に 'w' が含まれれば書き込みとみなす（L38-39「# query_type is 'r', 'w', 'rw', or 's'; anything containing 'w' is a write」exact）。AuthGap の D1（readOnlyHint:true）の照合でいえば、この関数が宣言を守る検証にあたる。 補足（限界）: _is_write_query は EXPLAIN の query_type に "w" が含まれるかだけを見る（L38-39、exact）。コメント自身が挙げる "s"（スキーマ書き込み）は "w" を含まないので、この検査では書き込みと判定されない。実行は routing_control=RoutingControl.READ（L204）でも行うが、サーバー側がそれで書き込みを拒むかはここでは確かめていない（不明）。「宣言を守る仕組みがある」は正しいが、完全な検証とまでは言えない。

<a id="g-c09-servers-gateways-security-15"></a>
#### C09-15 Neo4j（neo4j-contrib, Neo4j Labs） — mcp-neo4j-cypher（neo4j-contrib/mcp-neo4j、Python / FastMCP）

- **資料**: server.py: write_neo4j_cypher（サーバのソースコード）
- **URL**: https://github.com/neo4j-contrib/mcp-neo4j/blob/1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7/servers/mcp-neo4j-cypher/src/mcp_neo4j_cypher/server.py#L227-L237
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neo4j-contrib/mcp-neo4j/1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7/servers/mcp-neo4j-cypher/src/mcp_neo4j_cypher/server.py
- **版**: commit 1c7ad0793b5f06b42b9c44f855c23eb2064c3bb7（neo4j-contrib/mcp-neo4j の 2026-10-02 時点の HEAD）
- **書いてある場所**: L227-237
- **原文**:

```
    @mcp.tool(
        name=namespace_prefix + "write_neo4j_cypher",
        annotations=ToolAnnotations(
            title="Write Neo4j Cypher",
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
            openWorldHint=True,
        ),
        enabled=allow_writes,
    )
```

- **日本語**: write_neo4j_cypher を readOnlyHint=False・destructiveHint=True・idempotentHint=False・openWorldHint=True と宣言し、enabled=allow_writes（read_only でないとき）のときだけ有効にする。
- **どう使っているか**: read_only 設定のとき書き込みツールを無効にする。判断は注釈ではなく設定値 allow_writes = not read_only（L56）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: ツールを絞る・隠す・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、227-237 行（取得 2026-10-02T22:11:38Z、sha256 b0103b1949e5…）
- **補足**: 書き込みツール側も _is_write_query が偽なら「Only write queries are allowed for write-query」で拒否（L246-247）。

### Notion — Notion MCP server（makenotion/notion-mcp-server、OpenAPI から自動生成）

<a id="g-c09-servers-gateways-security-16"></a>
#### C09-16 Notion — Notion MCP server（makenotion/notion-mcp-server、OpenAPI から自動生成）

- **資料**: src/openapi-mcp-server/mcp/proxy.ts（サーバのソースコード）
- **URL**: https://github.com/makenotion/notion-mcp-server/blob/730ae781ba28beeaf0865025a3f2ed4c25ea2387/src/openapi-mcp-server/mcp/proxy.ts#L173-L187
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/makenotion/notion-mcp-server/730ae781ba28beeaf0865025a3f2ed4c25ea2387/src/openapi-mcp-server/mcp/proxy.ts
- **版**: commit 730ae781ba28beeaf0865025a3f2ed4c25ea2387（makenotion/notion-mcp-server の 2026-10-02 時点の HEAD）
- **書いてある場所**: L173-187
- **原文**:

```
          // Look up the HTTP method to determine annotations
          const operation = this.openApiLookup[toolNameWithMethod];
          const httpMethod = operation?.method?.toLowerCase();
          const isReadOnly = httpMethod === 'get';

          tools.push({
            name: truncatedToolName,
            description: method.description,
            inputSchema: method.inputSchema as Tool['inputSchema'],
            annotations: {
              title: this.operationIdToTitle(method.name),
              ...(isReadOnly
                ? { readOnlyHint: true }
                : { destructiveHint: true }),
            },
```

- **日本語**: OpenAPI の HTTP メソッドを見て注釈を決める。GET なら readOnlyHint:true、それ以外は destructiveHint:true。タイトルは operationId から作る。
- **どう使っているか**: OpenAPI から自動生成するツールに、HTTP メソッドだけで注釈を付ける。GET 以外（POST・PATCH・DELETE など）は一律に破壊的と宣言される。読み取りでも POST を使う操作があれば破壊的と宣言される（保守的な側）。
- **扱う宣言**: title・readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、173-187 行（取得 2026-10-02T22:11:36Z、sha256 9cd280d1d870…）
- **補足**: Notion のホスト版 MCP の公開文書（developers.notion.com）には注釈の記述が無い（checked_no_mention）。 [verifier] GET 以外・メソッド不明はどちらも destructiveHint:true。 補足: GET のツールには destructiveHint:false を付けず、GET 以外には readOnlyHint を付けない（どちらも仕様の既定に任せる）。HTTP メソッドが引けない（operation が無い）ときも isReadOnly=false なので destructiveHint:true 側に倒れる（L174-176、exact）。

### Stripe — @stripe/mcp（stripe/ai の tools/typescript/src/modelcontextprotocol、mcp.stripe.com への中継）

<a id="g-c09-servers-gateways-security-17"></a>
#### C09-17 Stripe — @stripe/mcp（stripe/ai の tools/typescript/src/modelcontextprotocol、mcp.stripe.com への中継）

- **資料**: toolkit.ts: registerProxyTool（サーバのソースコード）
- **URL**: https://github.com/stripe/ai/blob/27db051dba7cee2e13d2dbf6d65939cf412f5b3c/tools/typescript/src/modelcontextprotocol/toolkit.ts#L58-L69
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/stripe/ai/27db051dba7cee2e13d2dbf6d65939cf412f5b3c/tools/typescript/src/modelcontextprotocol/toolkit.ts
- **版**: commit 27db051dba7cee2e13d2dbf6d65939cf412f5b3c（stripe/ai の 2026-10-02 時点の HEAD）
- **書いてある場所**: L58-69
- **原文**:

```
  /**
   * Register a tool that proxies execution to mcp.stripe.com
   */
  private registerProxyTool(remoteTool: McpTool): void {
    // Convert JSON Schema to Zod shape for MCP SDK tool registration
    // This properly handles the 'required' field and type validation
    const zodShape = jsonSchemaToZodShape(remoteTool.inputSchema);

    this.tool(
      remoteTool.name,
      remoteTool.description || remoteTool.name,
      zodShape,
```

- **日本語**: mcp.stripe.com のツールを中継として登録するとき、名前・説明・入力スキーマ（Zod に変換）だけを this.tool(...) に渡す。
- **どう使っているか**: ローカルの @stripe/mcp はリモートのツール定義を登録し直すが、annotations を渡していない（this.tool の名前・説明・スキーマ・関数の形）。リモートが注釈を宣言していても、この経路ではクライアントに届かない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、58-69 行（取得 2026-10-02T22:11:37Z、sha256 f1184efb74c3…）
- **補足**: リモートの mcp.stripe.com 自体が注釈を付けているかは不明（今回は調べていない）。Stripe はツールの権限を Restricted API Key（RAK）で制御すると README に書く（checked_no_mention の Stripe README）。

### Pomerium — Pomerium — 設定 API を MCP ツールとして公開する部分（pkg/mcp/configapi）

<a id="g-c09-servers-gateways-security-18"></a>
#### C09-18 Pomerium — Pomerium — 設定 API を MCP ツールとして公開する部分（pkg/mcp/configapi）

- **資料**: pkg/mcp/configapi/annotations.go: annotationsForMethod（サーバのソースコード）
- **URL**: https://github.com/pomerium/pomerium/blob/046c6c391af48e1418fa8836d42a55abc09d9532/pkg/mcp/configapi/annotations.go#L9-L44
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/pomerium/pomerium/046c6c391af48e1418fa8836d42a55abc09d9532/pkg/mcp/configapi/annotations.go
- **版**: commit 046c6c391af48e1418fa8836d42a55abc09d9532（pomerium/pomerium の 2026-10-02 時点の HEAD）
- **書いてある場所**: L9-44
- **原文**:

```
// annotationsForMethod returns MCP tool annotations based on the RPC method name prefix.
// The naming convention in ConfigService is consistent:
//   - Get*, List* → read-only
//   - Create*     → additive (not destructive)
//   - Update*     → idempotent mutation (not destructive)
//   - Delete*     → destructive, idempotent
func annotationsForMethod(methodName string) *mcp.ToolAnnotations {
	switch {
	case strings.HasPrefix(methodName, "Get"), strings.HasPrefix(methodName, "List"):
		return &mcp.ToolAnnotations{
			ReadOnlyHint:  true,
			OpenWorldHint: new(false),
		}
	case strings.HasPrefix(methodName, "Create"):
		return &mcp.ToolAnnotations{
			DestructiveHint: new(false),
			OpenWorldHint:   new(false),
		}
	case strings.HasPrefix(methodName, "Update"):
		return &mcp.ToolAnnotations{
			DestructiveHint: new(false),
			IdempotentHint:  true,
			OpenWorldHint:   new(false),
		}
	case strings.HasPrefix(methodName, "Delete"):
		return &mcp.ToolAnnotations{
			DestructiveHint: new(true),
			IdempotentHint:  true,
			OpenWorldHint:   new(false),
		}
	default:
		return &mcp.ToolAnnotations{
			DestructiveHint: new(true),
			OpenWorldHint:   new(false),
		}
	}
```

- **日本語**: RPC メソッド名の接頭辞で注釈を決める。Get*/List* は読み取り専用、Create* は追加のみ（破壊的でない）、Update* は冪等な変更（破壊的でない）、Delete* は破壊的で冪等、それ以外は破壊的。openWorldHint はすべて false。
- **どう使っているか**: 名前の規約から注釈を機械的に決める例。知らない接頭辞は destructiveHint:true（保守的な既定）。Update* を「破壊的でない」とする判断は MongoDB（update は破壊的、12）と逆。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、9-44 行（取得 2026-10-02T22:12:05Z、sha256 6ac6514f8377…）
- **補足**: Pomerium のゲートウェイとしての MCP 認可（PPL の mcp_tool）はツール名で許可を決め、注釈は使わない（checked_no_mention の Pomerium 文書）。

### Elastic — Kibana Agent Builder（elastic/kibana）— 自社ツールのレビュー基準

<a id="g-c09-servers-gateways-security-19"></a>
#### C09-19 Elastic — Kibana Agent Builder（elastic/kibana）— 自社ツールのレビュー基準

- **資料**: .agents/skills/agent-builder-tool-review/references/common-issues.md「Destructive Operations (C5)」（サーバの文書）
- **URL**: https://github.com/elastic/kibana/blob/cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93/.agents/skills/agent-builder-tool-review/references/common-issues.md#L50-L61
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/elastic/kibana/cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93/.agents/skills/agent-builder-tool-review/references/common-issues.md
- **版**: commit cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93（elastic/kibana の 2026-10-02 時点の HEAD）
- **書いてある場所**: L50-61（直前の見出し: ## Destructive Operations (C5)）
- **原文**:

> **MCP bypasses confirmation dialogs ([#147](https://github.com/elastic/agentic-interface-program/issues/147)):** Streams write tools had
> confirmation dialogs in the Agent Builder UI, but MCP calls bypassed them
> entirely. Without `annotations.destructiveHint: true`, MCP hosts had no signal
> to gate the call.
>
> **What the review should catch:** Destructive tools must set
> `annotations.destructiveHint: true` and `confirmation.askUser` to `'always'`.
> Using `'once'` is permitted but should be flagged as a warning — `once` reuses
> the first confirmation for all subsequent calls to the same tool in a
> conversation, which can silently authorize deletes of different resources. Both
> annotation and confirmation signals are needed — annotations for MCP hosts,
> confirmation for 1P UI.

- **日本語**: MCP では確認ダイアログが飛ばされた（#147）。Streams の書き込みツールは Agent Builder の画面では確認が出たが、MCP 呼び出しでは全く出なかった。annotations.destructiveHint:true が無いと、MCP ホストには呼び出しを止める手がかりがない。レビューでは、破壊的ツールに destructiveHint:true と confirmation.askUser:'always' の両方があるかを見る。注釈は MCP ホスト向け、confirmation は自社 UI 向けで、両方要る。
- **どう使っているか**: Elastic が実際の不具合（MCP 経由だと自社 UI の確認ダイアログが出なかった）を受けて、「destructiveHint:true が無いと MCP ホストには呼び出しを止める手がかりが無い」として、破壊的ツールに destructiveHint:true と confirmation.askUser:'always' の両方を求めるレビュー基準にした。注釈は MCP ホスト向け、confirmation は自社（1P）UI 向け。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 作者への書き方の案内・確認を求める・宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、50-61 行（## Destructive Operations (C5)）（取得 2026-10-02T22:11:33Z、sha256 9839db7175a3…）
- **補足**: 同ファイル L120-121「Missing or inaccurate annotation fields, especially `readOnlyHint`/`destructiveHint` conflicts.」（exact、MCP Annotations (Q6)、注釈なしで出荷した例 #111）。L65-68 は読み取りと書き込みを 1 つのツールにまとめると readOnlyHint:true と destructiveHint:true を両立できないので分ける、という指摘（#114）。 言い過ぎを修正: 原文は「Without annotations.destructiveHint: true, MCP hosts had no signal to gate the call.」で、「ホストの確認は destructiveHint に頼るしかない」とまでは言っていない。参照されている issue #147 は elastic/agentic-interface-program のもので、本調査では見られない（未確認）。

### Elastic — Kibana Agent Builder（elastic/kibana）

<a id="g-c09-servers-gateways-security-20"></a>
#### C09-20 Elastic — Kibana Agent Builder（elastic/kibana）

- **資料**: x-pack/platform/plugins/shared/agent_builder/server/services/tools/builtin/converter.ts（サーバのソースコード）
- **URL**: https://github.com/elastic/kibana/blob/cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93/x-pack/platform/plugins/shared/agent_builder/server/services/tools/builtin/converter.ts#L112-L129
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/elastic/kibana/cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93/x-pack/platform/plugins/shared/agent_builder/server/services/tools/builtin/converter.ts
- **版**: commit cb9c664ae1dc21f9dcb14d3b9c39862dfad9fe93（elastic/kibana の 2026-10-02 時点の HEAD）
- **書いてある場所**: L112-129
- **原文**:

```
const READ_ONLY_DEFAULTS: Omit<McpToolAnnotations, 'title'> = {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: false,
};

const DESTRUCTIVE_DEFAULTS: Omit<McpToolAnnotations, 'title'> = {
  readOnlyHint: false,
  destructiveHint: true,
  idempotentHint: false,
  openWorldHint: true,
};

const getDefaultAnnotationsForToolType = (tool: StaticToolRegistration): McpToolAnnotations => {
  const defaults = tool.type === ToolType.workflow ? DESTRUCTIVE_DEFAULTS : READ_ONLY_DEFAULTS;
  return { title: tool.id, ...defaults };
};
```

- **日本語**: 既定の注釈: 読み取り用は readOnlyHint:true・destructiveHint:false・idempotentHint:true・openWorldHint:false、破壊用は readOnlyHint:false・destructiveHint:true・idempotentHint:false・openWorldHint:true。型が workflow なら破壊用、それ以外なら読み取り用を付ける（title はツール id）。
- **どう使っているか**: builtin 以外の型で静的に登録したツールには、ツールの型だけから注釈を付ける（workflow は破壊的側、それ以外は読み取り側）。builtin 型は各定義の tool.annotations を使う。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、112-129 行（取得 2026-10-02T22:11:36Z、sha256 b1c489accc14…）
- **補足**: builtin のツールは各定義の tool.annotations をそのまま使う（L55）。「それ以外の型」にどの ToolType が入るかは不明（列挙を確かめていない）。Elastic の公開文書（Agent Builder の MCP server）には注釈の記述が無い（checked_no_mention）。 誤りを修正: 既定値は「作者が注釈を書かないとき」に付くのではない。builtin 型の登録は tool.annotations をそのまま使い（L55、exact）、builtin 以外の型の静的登録には常に型から決めた既定値を付ける（L96 `annotations: getDefaultAnnotationsForToolType(tool),`、exact。この分岐では作者の注釈を読まない）。

### Stacklok — ToolHive（MCP サーバーの実行・プロキシ）— Cedar 認可

<a id="g-c09-servers-gateways-security-21"></a>
#### C09-21 Stacklok — ToolHive（MCP サーバーの実行・プロキシ）— Cedar 認可

- **資料**: Authorization policy reference「Tool annotation attributes」（ゲートウェイの文書）
- **URL**: https://docs.stacklok.com/toolhive/reference/authz-policy-reference
- **書いてある見出しへ直接**: https://docs.stacklok.com/toolhive/reference/authz-policy-reference#tool-annotation-attributes
- **版**: 2026-10-02 取得（sha256=4364b2496272）
- **書いてある場所**: Authorization policy reference > Tool annotation attributes
- **原文**:

> ToolHive caches these annotations from tools/list responses and makes them available as resource attributes during tools/call authorization.

- **日本語**: ToolHive は tools/list の応答から注釈を保存しておき、tools/call の認可のときにリソースの属性として使えるようにする。
- **どう使っているか**: ゲートウェイ（ToolHive のプロキシ）が、上流サーバーの注釈を Cedar ポリシーの入力（resource.readOnlyHint など）にする。属性になるのはサーバーが値を設定したときだけ。
- **条件**: Cedar 認可を有効にしたとき。HTTP PDP 認可では context.mcp.annotations.* に入る（24）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Authorization policy reference > Tool annotation attributes」（取得 2026-10-02T22:11:28Z、sha256 4364b2496272…）

### Stacklok — ToolHive — Cedar 認可

<a id="g-c09-servers-gateways-security-22"></a>
#### C09-22 Stacklok — ToolHive — Cedar 認可

- **資料**: Cedar policies「Tool annotation policies」（ゲートウェイの文書）
- **URL**: https://docs.stacklok.com/toolhive/concepts/cedar-policies
- **書いてある見出しへ直接**: https://docs.stacklok.com/toolhive/concepts/cedar-policies#tool-annotation-policies
- **版**: 2026-10-02 取得（sha256=b7ac4551522d）
- **書いてある場所**: Cedar policies > Tool annotation policies
- **原文**:

> Always use Cedar's has operator to check for an annotation before accessing it, otherwise a missing attribute causes a Cedar evaluation error that ToolHive treats as a deny.

- **日本語**: 注釈を読む前に必ず Cedar の has 演算子で有無を確かめること。確かめないと、属性が無いときに Cedar の評価エラーになり、ToolHive はそれを拒否として扱う。
- **どう使っているか**: 注釈が無いツールの扱い: 属性が無い → 評価エラー → 拒否（fail-closed）。has で確かめる permit 規則では、注釈の無いツールはその規則に当たらない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Cedar policies > Tool annotation policies」（取得 2026-10-02T22:11:27Z、sha256 b7ac4551522d…）
- **補足**: 同ページの例「Block destructive tools for non-admin users」（exact, #allow-non-destructive-closed-world-tools の次の例）: destructiveHint==true なら admin 以外を forbid。

### Stacklok — ToolHive — Cedar 認可（Safe tools プロファイル）

<a id="g-c09-servers-gateways-security-23"></a>
#### C09-23 Stacklok — ToolHive — Cedar 認可（Safe tools プロファイル）

- **資料**: Cedar policies「Real-world policy profiles > Safe tools profile」（ゲートウェイの文書）
- **URL**: https://docs.stacklok.com/toolhive/concepts/cedar-policies
- **書いてある見出しへ直接**: https://docs.stacklok.com/toolhive/concepts/cedar-policies#safe-tools-profile
- **版**: 2026-10-02 取得（sha256=b7ac4551522d）
- **書いてある場所**: Cedar policies > Real-world policy profiles > Safe tools profile
- **原文**:

> Tools that omit all annotation attributes are denied under this profile, preserving a conservative default-deny posture. Only tools that explicitly declare safe annotations are allowed.

- **日本語**: このプロファイルでは、注釈を何も付けていないツールは拒否され、保守的な既定拒否が保たれる。安全な注釈を明示したツールだけが許可される。
- **どう使っているか**: Safe tools プロファイル: readOnlyHint==true のツール、または destructiveHint==false かつ openWorldHint==false のツールの呼び出しだけを許可する。注釈の宣言がそのまま「実行してよいか」の条件になる（宣言が正しいかは確かめない）。
- **条件**: 運用者が Cedar 認可を有効にし、この Safe tools profile（authz-safe-tools.yaml の例）を設定したとき。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Cedar policies > Real-world policy profiles > Safe tools profile」（取得 2026-10-02T22:11:27Z、sha256 b7ac4551522d…）
- **補足**: 同じページの Tool allowlist profile（#tool-allowlist-profile）に「This is the most explicit approach and doesn't depend on MCP servers setting annotations correctly」（exact）とあり、注釈に頼る方式はサーバーの宣言が正しいことに依存する、と文書自身が認めている。 conditions を追加: Safe tools profile は文書が示す例のポリシーで、運用者がこの設定を入れたときだけ働く（ToolHive の既定の動作ではない）。

### Stacklok — ToolHive（stacklok/toolhive）— 認可の注釈の型

<a id="g-c09-servers-gateways-security-24"></a>
#### C09-24 Stacklok — ToolHive（stacklok/toolhive）— 認可の注釈の型

- **資料**: pkg/authz/authorizers/annotations.go: ToolAnnotations（ゲートウェイのソースコード）
- **URL**: https://github.com/stacklok/toolhive/blob/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/authz/authorizers/annotations.go#L8-L27
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/stacklok/toolhive/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/authz/authorizers/annotations.go
- **版**: commit 3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c（stacklok/toolhive の 2026-10-02 時点の HEAD）
- **書いてある場所**: L8-27
- **原文**:

```
// ToolAnnotations holds MCP tool annotation hints that inform authorization
// decisions. The fields match the MCP specification's tool annotation schema.
// Pointer types are used so callers can distinguish "not set" (nil) from
// an explicit false value.
//
// # Trust Boundary
//
// Annotations MUST be sourced from the server-side tool registry (the MCP
// tools/list response), NOT from the client's tools/call request body.
// Allowing clients to supply their own annotations would let a malicious
// caller set readOnlyHint=true on a destructive tool and bypass policies
// that rely on annotations.
//
// # Authorizer Exposure Paths
//
// The two authorizer implementations expose annotations at different
// locations so that policy authors can reference them:
//
//   - Cedar authorizer: flat on the resource entity — e.g. resource.readOnlyHint
//   - HTTP PDP authorizer: nested in the PORC context — context.mcp.annotations.readOnlyHint
```

- **日本語**: 認可の判断に使う注釈。注釈は必ずサーバー側のツール登録（tools/list の応答）から取ること。クライアントの tools/call 本文から取ってはいけない。そうしないと悪意ある呼び出し側が破壊的なツールに readOnlyHint=true を付けて、注釈に頼るポリシーをすり抜けられる。Cedar では resource.readOnlyHint、HTTP PDP では context.mcp.annotations.readOnlyHint として見せる。
- **どう使っているか**: 信頼の境界: クライアントが申告する注釈は信用せず、サーバーの tools/list の値だけを使う。ただしサーバー自身の宣言が正しいかは確かめない（境界はクライアントとゲートウェイの間だけ）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、8-27 行（取得 2026-10-02T22:12:06Z、sha256 91b7675e7234…）
- **補足**: pointer 型で「未設定（nil）」と明示の false を区別する（L10-11）。

### Stacklok — ToolHive Virtual MCP（vMCP）— 複合ツール

<a id="g-c09-servers-gateways-security-25"></a>
#### C09-25 Stacklok — ToolHive Virtual MCP（vMCP）— 複合ツール

- **資料**: pkg/vmcp/config/config.go: CompositeToolConfig.Annotations（ゲートウェイのソースコード）
- **URL**: https://github.com/stacklok/toolhive/blob/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/vmcp/config/config.go#L877-L893
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/stacklok/toolhive/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/vmcp/config/config.go
- **版**: commit 3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c（stacklok/toolhive の 2026-10-02 時点の HEAD）
- **書いてある場所**: L877-893
- **原文**:

```
	// Annotations declares MCP tool annotations for the composite tool.
	//
	// Annotation derivation runs at ADVERTISE TIME (when tools/list is served
	// and the backend tools are aggregated), not at CRD admission — thv vmcp
	// validate does NOT check annotation contradictions. The derived floor is
	// fail-closed: when the workflow has one or more tool steps the floor is
	// always non-nil, and any step whose annotations are nil/unknown taints the
	// floor conservatively (readOnly=false, destructive=true, openWorld=true).
	// A workflow with no tool steps (e.g. only elicitation) has no floor.
	//
	// When nil, annotations are derived from the annotations of the backend tools
	// referenced by the workflow's steps (e.g. readOnlyHint is true only when every
	// step tool is read-only). When set, the values are an explicit author
	// declaration merged over the derived floor — subject to a safety-floor
	// guardrail that drops the composite tool (with a warning naming the offending
	// step tools) if an explicit hint would make the tool look safer than its
	// steps allow.
```

- **日本語**: 複合ツールの注釈は tools/list を返す時点で導く（CRD 受け入れ時ではなく、thv vmcp validate は矛盾を検査しない）。導いた下限は fail-closed で、手順にツールが 1 つでもあれば下限は必ずあり、注釈が無い・不明な手順ツールがあると下限を保守側（readOnly=false, destructive=true, openWorld=true）にする。指定が無ければ手順のツールの注釈から導く（readOnlyHint は全手順が read-only のときだけ true）。指定があれば下限に重ねるが、手順より安全に見せる値なら、その複合ツールを外す（警告つき）。
- **どう使っているか**: 複数のツールを組み合わせた仮想ツールの宣言を、部品の宣言から合成する。注釈が無い部品は危ない側として扱い、作者が部品より安全な宣言を書くとツールごと出さない。宣言どうしの整合を機械的に保つ（ただし部品の宣言そのものの真偽は確かめない）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・宣言を検査する・その他
- **確かさ**: [確認] 再照合 exact・1 か所、877-893 行（取得 2026-10-02T22:11:35Z、sha256 8464910878f6…）

### Stacklok — ToolHive Virtual MCP（vMCP）— ツールの上書き

<a id="g-c09-servers-gateways-security-26"></a>
#### C09-26 Stacklok — ToolHive Virtual MCP（vMCP）— ツールの上書き

- **資料**: pkg/vmcp/config/config.go: ToolOverride（ゲートウェイのソースコード）
- **URL**: https://github.com/stacklok/toolhive/blob/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/vmcp/config/config.go#L674-L690
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/stacklok/toolhive/3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c/pkg/vmcp/config/config.go
- **版**: commit 3ca3c8f71152ad6e109dbb881be13ceb17a2cf3c（stacklok/toolhive の 2026-10-02 時点の HEAD）
- **書いてある場所**: L674-690
- **原文**:

```
// ToolOverride defines tool name, description, and annotation overrides.
// +kubebuilder:object:generate=true
// +gendoc
type ToolOverride struct {
	// Name is the new tool name (for renaming).
	// +optional
	Name string `json:"name,omitempty" yaml:"name,omitempty"`

	// Description is the new tool description.
	// +optional
	Description string `json:"description,omitempty" yaml:"description,omitempty"`

	// Annotations overrides specific tool annotation fields.
	// Only specified fields are overridden; others pass through from the backend.
	// +optional
	Annotations *ToolAnnotationsOverride `json:"annotations,omitempty" yaml:"annotations,omitempty"`
}
```

- **日本語**: ツールの名前・説明・注釈の上書き。注釈は指定した項目だけを上書きし、ほかは上流（backend）の値をそのまま通す。
- **どう使っているか**: ゲートウェイの運用者が上流サーバーの注釈を項目ごとに書き換えられる。クライアントや認可が見る注釈が、上流サーバーの宣言ではなく運用者の設定になりうる。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる・その他
- **確かさ**: [確認] 再照合 exact・1 か所、674-690 行（取得 2026-10-02T22:11:35Z、sha256 8464910878f6…）
- **補足**: ToolAnnotationsOverride のコメント（L638-639）「All fields use pointers so nil means "don't override" while zero values (empty string, false) mean "explicitly set to this value."」（exact）。上書き後の値が 21-23 の Cedar 認可の入力にもなるかは不明（確かめていない）。

### Speakeasy — Speakeasy MCP gateway / Gram — ツール呼び出しごとの RBAC

<a id="g-c09-servers-gateways-security-27"></a>
#### C09-27 Speakeasy — Speakeasy MCP gateway / Gram — ツール呼び出しごとの RBAC

- **資料**: In Depth: Speakeasy vs MintMCP（Speakeasy 公式ブログ）（公式ブログ）
- **URL**: https://www.speakeasy.com/blog/speakeasy-vs-mintmcp
- **書いてある見出しへ直接**: https://www.speakeasy.com/blog/speakeasy-vs-mintmcp#how-is-rbac-enforced-on-a-single-tool-call
- **版**: 2026-10-02 取得（sha256=977221749afa）
- **書いてある場所**: In Depth: Speakeasy vs MintMCP > Part 2: Governance > How is RBAC enforced on a single tool call?
- **原文**:

> each tool call then passes a second check that carries the tool name and the tool's disposition, derived at call time from its MCP annotations

- **日本語**: 各ツール呼び出しは 2 段目の検査を通る。検査にはツール名と、呼び出し時に MCP 注釈から導いたツールの disposition（read_only・destructive・idempotent・open_world）が載る。
- **どう使っているか**: RBAC の grant の selector に disposition を書ける。例えばサポート担当には請求サーバーの read_only のツールだけを許し（get_invoice は成功、create_refund は拒否）、サーバー側は変えなくてよい。注釈が役割ごとの許可の入力になる。
- **条件**: Speakeasy のゲートウェイ経由の呼び出し。拒否規則は別の段で評価され、常に許可より強い。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「In Depth: Speakeasy vs MintMCP > Part 2: Governance > How is RBAC enforced on a single tool call?」（取得 2026-10-02T22:11:39Z、sha256 977221749afa…）
- **補足**: 自社製品の比較記事（MintMCP との比較）。disposition の導き方は 29（優先順 read_only > destructive > idempotent > open_world）。 [verifier] 同記事の「Destructive tool detection reads the destructiveHint annotation on MCP tools ...」（exact, https://www.speakeasy.com/blog/speakeasy-vs-mintmcp#how-does-each-platform-inspect-tool-definitions-and-tool-calls）。 注意を追加: 自社製品の比較記事（マーケティング）。同じ記事の別の節に「Destructive tool detection reads the destructiveHint annotation on MCP tools and also recognizes destructive CLI patterns such as rm -rf, git push --force, and DROP TABLE in shell commands and tool arguments.」（exact, #how-does-each-platform-inspect-tool-definitions-and-tool-calls）があり、リスクポリシーの破壊的ツール検出も destructiveHint を読むと書く。

### Speakeasy — Speakeasy MCP gateway / Gram — 管理者が記録する注釈

<a id="g-c09-servers-gateways-security-28"></a>
#### C09-28 Speakeasy — Speakeasy MCP gateway / Gram — 管理者が記録する注釈

- **資料**: In Depth: Speakeasy vs MintMCP（Speakeasy 公式ブログ）（公式ブログ）
- **URL**: https://www.speakeasy.com/blog/speakeasy-vs-mintmcp
- **書いてある見出しへ直接**: https://www.speakeasy.com/blog/speakeasy-vs-mintmcp#how-is-rbac-enforced-on-a-single-tool-call
- **版**: 2026-10-02 取得（sha256=977221749afa）
- **書いてある場所**: In Depth: Speakeasy vs MintMCP > Part 2: Governance > How is RBAC enforced on a single tool call?
- **原文**:

> For remote servers, an admin-recorded annotation overrides whatever the vendor publishes, so a vendor cannot quietly flip a tool from read-only to destructive.

- **日本語**: リモートサーバーについては、管理者が記録した注釈が、ベンダーの公開する注釈より優先する。だからベンダーが黙ってツールを read-only から destructive に変えることはできない。
- **どう使っているか**: 上流ベンダーの注釈を信用しきらず、管理者が固定した注釈で RBAC を判定する。ベンダー側の宣言の変更（ドリフト）への対策。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「In Depth: Speakeasy vs MintMCP > Part 2: Governance > How is RBAC enforced on a single tool call?」（取得 2026-10-02T22:11:39Z、sha256 977221749afa…）
- **補足**: Gram の実装では管理者が記録するツールメタデータ（read_only_hint など）を DB に保存し、変更時に disposition のキャッシュを捨てる（server/internal/mcpservers/toolmetadata.go L530-543、L570 のコメントは verify_quote.py で exact）。「ベンダー注釈より優先」の順序そのものは未照合。 注意を追加: 出典は Speakeasy 自身の製品比較記事（マーケティング）で、製品文書ではない。Gram のコードには「Tool metadata backs disposition-aware RBAC for remote-backed servers.」（server/internal/mcpservers/toolmetadata.go L570、exact）と disposition キャッシュの破棄があり、管理者の記録が RBAC に使われることは裏づくが、「ベンダーの注釈より優先する」マージの順序はコードで確かめていない（不明）。

### Speakeasy — Gram（speakeasy-api/gram）

<a id="g-c09-servers-gateways-security-29"></a>
#### C09-29 Speakeasy — Gram（speakeasy-api/gram）

- **資料**: server/internal/conv/tools.go: DispositionFromAnnotations（ゲートウェイのソースコード）
- **URL**: https://github.com/speakeasy-api/gram/blob/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/internal/conv/tools.go#L391-L407
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/speakeasy-api/gram/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/internal/conv/tools.go
- **版**: commit cf3bdc773ae083d06563f93736a410bbd47c1e3e（speakeasy-api/gram の 2026-10-02 時点の HEAD）
- **書いてある場所**: L391-407
- **原文**:

```
// DispositionFromAnnotations derives a single disposition string from tool
// annotation hints. Priority: read_only > destructive > idempotent > open_world.
// Returns empty string when no hints are set or annotations is nil.
func DispositionFromAnnotations(a *types.ToolAnnotations) string {
	if a == nil {
		return ""
	}
	switch {
	case a.ReadOnlyHint != nil && *a.ReadOnlyHint:
		return "read_only"
	case a.DestructiveHint != nil && *a.DestructiveHint:
		return "destructive"
	case a.IdempotentHint != nil && *a.IdempotentHint:
		return "idempotent"
	case a.OpenWorldHint != nil && *a.OpenWorldHint:
		return "open_world"
	default:
```

- **日本語**: 注釈のヒントから disposition を 1 つ導く。優先順は read_only > destructive > idempotent > open_world。ヒントが何も無いか注釈が nil なら空文字を返す。
- **どう使っているか**: RBAC の判定に使う 1 つの値に注釈をまとめる。readOnlyHint:true なら destructiveHint:true が同時にあっても read_only になる。注釈が無いツールは disposition が空で、read_only の grant には当たらない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、391-407 行（取得 2026-10-02T22:11:37Z、sha256 1b6be1f3d683…）
- **補足**: コード上、矛盾した宣言（readOnlyHint と destructiveHint が両方 true）は read_only 側（許可が広い側）に倒れる。 [verifier] DispositionFromAnnotations は nil のヒントを false と同じに扱い、仕様の既定値（destructive=true, openWorld=true）を使わない。destructiveHint を省いたツールは "destructive" に分類されない。 重要な補足: destructiveHint を書かないツール（仕様の既定では destructive=true）は disposition が "destructive" にならない（readOnly でなければ idempotent / open_world / 空になる）。"destructive" を対象にした deny 規則は、destructiveHint を省いたツールに当たらない。仕様の既定値は使っていない。

<a id="g-c09-servers-gateways-security-30"></a>
#### C09-30 Speakeasy — Gram（speakeasy-api/gram）

- **資料**: server/internal/mcp/toolfilter/selection.go: AnnotationsMatch（ゲートウェイのソースコード）
- **URL**: https://github.com/speakeasy-api/gram/blob/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/internal/mcp/toolfilter/selection.go#L323-L354
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/speakeasy-api/gram/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/internal/mcp/toolfilter/selection.go
- **版**: commit cf3bdc773ae083d06563f93736a410bbd47c1e3e（speakeasy-api/gram の 2026-10-02 時点の HEAD）
- **書いてある場所**: L323-354
- **原文**:

```
// AnnotationsMatch reports whether any of the given annotation values has
// its raw hint explicitly true on the tool. Nil and false hints are
// identical (fail closed). Deliberately NOT the priority-collapsed
// disposition used by RBAC: a tool carrying readOnlyHint and idempotentHint
// matches either value.
func AnnotationsMatch(annotations *types.ToolAnnotations, values []string) bool {
	if annotations == nil || len(values) == 0 {
		return false
	}
	hintTrue := func(hint *bool) bool { return hint != nil && *hint }
	for _, value := range values {
		switch value {
		case AnnotationReadOnly, "readOnlyHint":
			if hintTrue(annotations.ReadOnlyHint) {
				return true
			}
		case AnnotationDestructive, "destructiveHint":
			if hintTrue(annotations.DestructiveHint) {
				return true
			}
		case AnnotationIdempotent, "idempotentHint":
			if hintTrue(annotations.IdempotentHint) {
				return true
			}
		case AnnotationOpenWorld, "openWorldHint":
			if hintTrue(annotations.OpenWorldHint) {
				return true
			}
		}
	}
	return false
}
```

- **日本語**: 指定した注釈名のどれかについて、ツールのヒントが明示的に true なら一致とする。nil と false は同じ扱い（fail closed）。RBAC の優先順でまとめた disposition とは意図的に違い、readOnlyHint と idempotentHint を両方持つツールはどちらの値にも一致する。
- **どう使っているか**: セッションのツール選択（live annotation grant）とリスクポリシーの範囲指定（31）で使う。ヒントが明示的に true のときだけ一致し、未設定は false と同じ（仕様の既定値は使わない）。allow の grant では許可が広がらない側だが、リスクポリシーを destructiveHint で絞ると、destructiveHint を省いたツールはポリシーが掛からない側に倒れる。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、323-354 行（取得 2026-10-02T22:11:37Z、sha256 85531946f957…）
- **補足**: FilterToolsBySelection（L357-358）「passes iff an allow entry includes it by name or a live annotation grant matches its declared hints.」（exact）。 言い過ぎを修正: 「未設定は一致しない」は allow の grant にとっては安全側だが、31 のリスクポリシーの範囲を tool_annotations=["destructiveHint"] で絞ると、destructiveHint を省いたツール（仕様の既定では破壊的）はそのポリシーの対象から外れる（検査が掛からない側）。どちらに倒れるかは使い道で逆になる。

### Speakeasy — Gram（speakeasy-api/gram）— リスクポリシーの MCP 範囲

<a id="g-c09-servers-gateways-security-31"></a>
#### C09-31 Speakeasy — Gram（speakeasy-api/gram）— リスクポリシーの MCP 範囲

- **資料**: server/design/shared/risk.go: RiskMCPScope（ゲートウェイのソースコード）
- **URL**: https://github.com/speakeasy-api/gram/blob/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/design/shared/risk.go#L143-L155
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/speakeasy-api/gram/cf3bdc773ae083d06563f93736a410bbd47c1e3e/server/design/shared/risk.go
- **版**: commit cf3bdc773ae083d06563f93736a410bbd47c1e3e（speakeasy-api/gram の 2026-10-02 時点の HEAD）
- **書いてある場所**: L143-155
- **原文**:

```
var RiskMCPScope = Type("RiskMCPScope", func() {
	Meta("struct:pkg:path", "types")

	Attribute("all_servers", Boolean, "Apply to every MCP server, including servers added later.", func() {
		Default(false)
	})
	Attribute("tool_annotations", ArrayOf(String, func() {
		Enum("destructiveHint", "readOnlyHint", "idempotentHint", "openWorldHint")
	}), "Tool annotation hints matched by the policy-level rule. Empty matches all tools.")
	Attribute("servers", ArrayOf(RiskMCPServerScope), "Selected MCP servers and gateways, or custom per-server tool overrides when all_servers is true.")

	Required("servers")
})
```

- **日本語**: リスクポリシーを MCP のツール通信に限る範囲。tool_annotations（destructiveHint・readOnlyHint・idempotentHint・openWorldHint の列挙）で、ポリシー単位の規則に当てるツールを注釈で選ぶ。空ならすべてのツール。
- **どう使っているか**: リスクポリシー（プロンプトインジェクション検出など）を、例えば destructiveHint:true のツールの通信だけに当てる、といった範囲指定に注釈を使う。tool_annotations が空ならすべてのツールが対象。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 危険度を付ける・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、143-155 行（取得 2026-10-02T22:11:36Z、sha256 60c2dd5bdf30…）
- **補足**: 一致の判定は 30 の AnnotationsMatch（server/internal/risk/policycore/types.go L88-93 の toolRuleMatches から呼ぶ、exact）。tool_annotations に未知の注釈名があるとポリシーの範囲は fail-closed（failClosedMCPScope、同 L237-241、exact）。未設定のヒントは一致しないので、destructiveHint を省いたツールには destructiveHint で絞ったポリシーが掛からない（30 の verifier_note）。 notes のパスを修正: policycore/types.go は server/internal/risk/policycore/types.go（toolRuleMatches L88-93、未知の注釈名で failClosedMCPScope を返すのは L237-241。どちらも verify_quote.py で exact）。usage_ja の「プロンプトで判定するもの」は不正確（リスクポリシーには発見的な検出器と LLM 判定がある）なので外した。

### IBM — ContextForge（IBM/mcp-context-forge、MCP ゲートウェイ）

<a id="g-c09-servers-gateways-security-32"></a>
#### C09-32 IBM — ContextForge（IBM/mcp-context-forge、MCP ゲートウェイ）

- **資料**: Tool Annotations「Gateway-Discovered Tools」（ゲートウェイの文書）
- **URL**: https://ibm.github.io/mcp-context-forge/using/tool-annotations/
- **書いてある見出しへ直接**: https://ibm.github.io/mcp-context-forge/using/tool-annotations/#gateway-discovered-tools
- **版**: 2026-10-02 取得（sha256=e668ea176e2e）
- **書いてある場所**: Tool Annotations¶ > Gateway-Discovered Tools¶
- **原文**:

> When registering MCP servers via /gateways, tools are automatically discovered. To add annotations:

- **日本語**: /gateways で MCP サーバーを登録すると、ツールは自動で見つかる。（その見つかったツールに）注釈を付けるには、次のようにする。
- **どう使っているか**: 運用者が Admin UI や API（PUT /tools/{id}）で、上流から自動で見つけたツールに注釈を付け直せる。付け直した値がクライアントに出るなら、クライアントが見る注釈は上流サーバーの宣言ではなく運用者の設定になる（ページに明記は無く推測）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations¶ > Gateway-Discovered Tools¶」（取得 2026-10-02T22:12:52Z、sha256 e668ea176e2e…）
- **補足**: ページ冒頭（#tool-annotations）は「Tool annotations provide metadata hints about tool behavior, helping clients and UIs make informed decisions about how to present and use tools.」（exact）。ゲートウェイ自身が注釈で許可・拒否を決めるという記述はこのページに無い。「Integration with Clients」節は、警告ダイアログ・自動再試行・read-only の結果のキャッシュにクライアントが使う、と一般論を書く（出典なし）。 補足: 上書きした注釈がゲートウェイの tools/list でクライアントにそのまま出るかは、このページに明記が無い（「Setting Annotations via Admin UI」節と PUT /tools/{id} の例があるだけ）。usage_ja の後半は推測と明記。同ページの「Integration with Clients」節「Many MCP clients use annotations to:」（exact, #integration-with-clients）は出典の無い一般論。

### IBM — ContextForge（IBM/mcp-context-forge）

<a id="g-c09-servers-gateways-security-33"></a>
#### C09-33 IBM — ContextForge（IBM/mcp-context-forge）

- **資料**: Tool Annotations「Best Practices > 1. Be Conservative with Safety Hints」（ゲートウェイの文書）
- **URL**: https://ibm.github.io/mcp-context-forge/using/tool-annotations/
- **書いてある見出しへ直接**: https://ibm.github.io/mcp-context-forge/using/tool-annotations/#1-be-conservative-with-safety-hints
- **版**: 2026-10-02 取得（sha256=e668ea176e2e）
- **書いてある場所**: Tool Annotations¶ > Best Practices¶ > 1. Be Conservative with Safety Hints¶
- **原文**:

> Default to destructiveHint: true if uncertain

- **日本語**: 迷ったら destructiveHint:true を既定にする。
- **どう使っているか**: 安全側に倒す付け方の指針。同じ節に「Only set readOnlyHint: true for genuinely safe operations」（exact）。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Annotations¶ > Best Practices¶ > 1. Be Conservative with Safety Hints¶」（取得 2026-10-02T22:12:52Z、sha256 e668ea176e2e…）
- **補足**: 冪等についても「本当に何度呼んでも安全なときだけ」と書く。

### MetaMCP（metatool-ai） — MetaMCP（MCP の集約・ゲートウェイ）

<a id="g-c09-servers-gateways-security-34"></a>
#### C09-34 MetaMCP（metatool-ai） — MetaMCP（MCP の集約・ゲートウェイ）

- **資料**: README.md「Tool Overrides & Annotations」（ゲートウェイの文書）
- **URL**: https://github.com/metatool-ai/metamcp/blob/ff4ff2de9d25453c52dcc7be32680b30700a6012/README.md#L148-L152
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/metatool-ai/metamcp/ff4ff2de9d25453c52dcc7be32680b30700a6012/README.md
- **版**: commit ff4ff2de9d25453c52dcc7be32680b30700a6012（metatool-ai/metamcp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L148-152（直前の見出し: ### ✏️ **Tool Overrides & Annotations**）
- **原文**:

```
### ✏️ **Tool Overrides & Annotations**
- Open a namespace → **Tools** tab to see every tool coming from connected MCP servers.
- Each saved tool can be expanded and edited inline: update the display **name/title/description** or provide a JSON blob with namespace-specific annotations (for example `{ "annotations": { "readOnlyHint": false } }`).
- Badges in the table ("Overridden", "Annotations") show which tools currently have custom metadata. Hover them to read a tooltip describing what was overridden.
- Annotation overrides are merged with whatever the upstream MCP server returns, so you can safely add custom UI hints without losing provider metadata.
```

- **日本語**: 名前空間の Tools タブで、つながった MCP サーバーから来る全ツールを見られる。保存したツールは、表示名・タイトル・説明を変えたり、名前空間ごとの注釈の JSON（例: {"annotations":{"readOnlyHint":false}}）を付けたりできる。表のバッジで上書きの有無を示す。注釈の上書きは上流の値とマージされる。
- **どう使っているか**: 集約ゲートウェイが、名前空間ごとに運用者が注釈を上書きすることを許す（上流の値とマージ）。管理画面のバッジで上書きの有無を示す。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: その他・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、148-152 行（### ✏️ **Tool Overrides & Annotations**）（取得 2026-10-02T22:11:38Z、sha256 2576fbb0ef96…）
- **補足**: 例は readOnlyHint:false への上書き（より保守的な向き）だが、true にする上書きを制限するとは書いていない（不明）。 usage を修正: display_label を外した。表のバッジ（Overridden / Annotations）は管理画面で「上書きがあるか」を示すもので、ヒントの値をラベルとして見せる用途ではない。README は注釈の上書きを「custom UI hints」と呼んでいる。

### Docker — Docker MCP Catalog（docker/mcp-registry のカタログ生成）

<a id="g-c09-servers-gateways-security-35"></a>
#### C09-35 Docker — Docker MCP Catalog（docker/mcp-registry のカタログ生成）

- **資料**: internal/mcp/helper.go（tools/list の結果をカタログに写す）（ゲートウェイのソースコード）
- **URL**: https://github.com/docker/mcp-registry/blob/49b643ce3fc73e6ee80bb962719b6e2990e3d397/internal/mcp/helper.go#L152-L169
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/mcp-registry/49b643ce3fc73e6ee80bb962719b6e2990e3d397/internal/mcp/helper.go
- **版**: commit 49b643ce3fc73e6ee80bb962719b6e2990e3d397（docker/mcp-registry の 2026-10-02 時点の HEAD）
- **書いてある場所**: L152-169
- **原文**:

```
		// Annotations
		var annotations *ToolAnnotations
		if tool.Annotations != (mcp.ToolAnnotation{}) {
			annotations = &ToolAnnotations{
				Title:           tool.Annotations.Title,
				ReadOnlyHint:    tool.Annotations.ReadOnlyHint,
				DestructiveHint: tool.Annotations.DestructiveHint,
				IdempotentHint:  tool.Annotations.IdempotentHint,
				OpenWorldHint:   tool.Annotations.OpenWorldHint,
			}
		}

		list = append(list, Tool{
			Name:        tool.Name,
			Description: removeArgs(tool.Description),
			Arguments:   arguments,
			Annotations: annotations,
		})
```

- **日本語**: カタログを作るとき、サーバーの tools/list で得たツールの注釈（title と 4 つのヒント）を、全部が空でなければカタログのツール項目に写す。
- **どう使っているか**: Docker MCP Catalog の生成ツールが、実サーバーから取った注釈をカタログに記録する。ただし使っている mcp-go v0.25.0 の型も、カタログ側の型（types.go L58-64）も bool + omitempty なので、false の値はカタログに残らない（readOnlyHint:false・destructiveHint:false・openWorldHint:false は「未設定」と同じになる）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・2 か所、152-169 行（取得 2026-10-02T22:11:41Z、sha256 1f7b1aa75a78…）
- **補足**: count=2: 同じ写しのコードが helper.go の別の関数（L290-307）にもある。types.go L58-64 の ToolAnnotations（ReadOnlyHint bool `json:"readOnlyHint,omitempty"` など）も exact。destructiveHint:false や openWorldHint:false が落ちると、仕様の既定（destructive=true, openWorld=true）に戻るので保守的な側に変わる。レジストリのコードなので doc_type は gateway_code とした。Docker MCP Gateway 側での使われ方は C08 を参照。 補足: false が落ちるのはカタログの型の前から。docker/mcp-registry は mark3labs/mcp-go v0.25.0（go.mod L9、exact）を使い、その ToolAnnotation 自体が `ReadOnlyHint bool `json:"readOnlyHint,omitempty"``（mcp/tools.go L137、exact）。サーバーが destructiveHint を省いた場合（仕様の既定は true）も Go では false になり、カタログでは省略される（=既定 true に戻る）ので、結果は「省略」と「false」が同じになる。

### Complira — HintLint（complira/hintlint）

<a id="g-c09-servers-gateways-security-36"></a>
#### C09-36 Complira — HintLint（complira/hintlint）

- **資料**: README.md（検査の道具の文書）
- **URL**: https://github.com/complira/hintlint/blob/5a51f2a43a4875c5297f29b4f2ac4ee26c6e8c37/README.md#L15-L17
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/complira/hintlint/5a51f2a43a4875c5297f29b4f2ac4ee26c6e8c37/README.md
- **版**: commit 5a51f2a43a4875c5297f29b4f2ac4ee26c6e8c37（complira/hintlint の 2026-10-02 時点の HEAD）
- **書いてある場所**: L15-17
- **原文**:

> MCP servers use tool annotations — `readOnlyHint`, `destructiveHint`, and `openWorldHint` — to help agents decide when a person should approve an action. HintLint checks whether those hints match the code behind each tool.
>
> It reads the source code, detects what each tool actually does, and reports where annotations don't match behavior. A tool that calls `iam.delete_access_key()` but omits `destructiveHint` means the agent skips confirmation on an irreversible action.

- **日本語**: MCP サーバーは readOnlyHint・destructiveHint・openWorldHint で、人の承認が要るかをエージェントが決める手助けをする。HintLint はそのヒントが各ツールのコードと合っているかを調べる。ソースを読んで各ツールが実際に何をするかを見つけ、注釈と動作の食い違いを報告する。iam.delete_access_key() を呼ぶのに destructiveHint を付けていないツールでは、取り返しのつかない操作で確認が飛ばされる。
- **どう使っているか**: 宣言と実装を照合する静的解析ツール（AuthGap と同じ方向）。TypeScript/JavaScript/Python を対象に 10 種類の sink を検出して宣言と比べ、端末・JSON・SARIF・Registry artifact で出す。CI では「ハンドラに結びついたソース上の証拠」がある所見だけで失敗させ、メタデータだけの推測では止めない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、15-17 行（取得 2026-10-02T22:11:32Z、sha256 b55ff701f13f…）
- **補足**: README の「20 リポジトリの試行で 1,160 ツールを解析し、23 件の注釈の問題を 82% の精度で確認」という数値は Complira 自身の報告で、本調査では検証していない（verified_by_me = none）。complira.ai 本体は 502 で届かなかった（unreachable）。 [verifier] 「destructiveHint を省くとエージェントが確認を飛ばす」は Complira の主張で、クライアントの挙動の一次資料ではない（仕様の既定では省略は destructive=true）。 注意を追加: 「the agent skips confirmation」はツール作者（Complira）によるクライアント挙動の主張で、クライアント側の一次資料ではない。usage_ja の 10 種類の sink・出力形式・CI の方針は同 README L88-103 で目視確認。

### Complira — HintLint — Finding Reference

<a id="g-c09-servers-gateways-security-37"></a>
#### C09-37 Complira — HintLint — Finding Reference

- **資料**: Finding Reference「HINTLINT-READONLY-001」（検査の道具の文書）
- **URL**: https://complira.gitbook.io/complira-docs/finding-reference
- **書いてある見出しへ直接**: https://complira.gitbook.io/complira-docs/finding-reference#hintlint-readonly-001
- **版**: 2026-10-02 取得（sha256=710f121b4950）
- **書いてある場所**: Finding Reference > Annotation Drift Findings > HINTLINT-READONLY-001
- **原文**:

> Tool declares readOnlyHint=true but source evidence shows state mutation, external side effect, or process execution.

- **日本語**: readOnlyHint=true と宣言しているのに、ソースに状態の変更・外部への副作用・プロセス実行の証拠がある。
- **どう使っているか**: 偽の read-only（AuthGap の D1 と同じ種類の矛盾）を High として報告し、readOnlyHint:false に直すよう勧める。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Finding Reference > Annotation Drift Findings > HINTLINT-READONLY-001」（取得 2026-10-02T22:11:24Z、sha256 710f121b4950…）
- **補足**: OPEN-WORLD-001（Medium）は openWorldHint=false と宣言しつつ外部の副作用・ネットワーク・プロセス実行に届く場合。

<a id="g-c09-servers-gateways-security-38"></a>
#### C09-38 Complira — HintLint — Finding Reference

- **資料**: Finding Reference「HINTLINT-DESTRUCTIVE-001」（検査の道具の文書）
- **URL**: https://complira.gitbook.io/complira-docs/finding-reference
- **書いてある見出しへ直接**: https://complira.gitbook.io/complira-docs/finding-reference#hintlint-destructive-001
- **版**: 2026-10-02 取得（sha256=710f121b4950）
- **書いてある場所**: Finding Reference > Annotation Drift Findings > HINTLINT-DESTRUCTIVE-001
- **原文**:

> Tool reaches destructive or process-execution evidence but does not declare destructiveHint=true.

- **日本語**: 破壊的な操作かプロセス実行の証拠に届くのに、destructiveHint=true を宣言していない。
- **どう使っているか**: 破壊的操作かプロセス実行の証拠がソースにあるのに destructiveHint=true を宣言していない（未宣言または false）ツールを High の所見にする（type: missing_or_false_destructive_hint）。仕様の既定値（未宣言なら destructive 扱い）に頼らず、明示を求める。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 宣言を検査する・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Finding Reference > Annotation Drift Findings > HINTLINT-DESTRUCTIVE-001」（取得 2026-10-02T22:11:24Z、sha256 710f121b4950…）
- **補足**: 言い過ぎを修正: 「destructiveHint を書いていないこと自体を所見にする」は誤り。所見になるのは、ソース上で破壊的操作かプロセス実行の証拠に届くツールが destructiveHint=true を宣言していないとき（未宣言または false）だけ。

### Complira — HintLint — Registry Artifact

<a id="g-c09-servers-gateways-security-39"></a>
#### C09-39 Complira — HintLint — Registry Artifact

- **資料**: Registry Artifact「Ingestion Guidance」（検査の道具の文書）
- **URL**: https://complira.gitbook.io/complira-docs/registry-artifact
- **書いてある見出しへ直接**: https://complira.gitbook.io/complira-docs/registry-artifact#ingestion-guidance
- **版**: 2026-10-02 取得（sha256=9f967731e673）
- **書いてある場所**: Registry Artifact > Ingestion Guidance
- **原文**:

> Registries should treat source-backed findings as review evidence, not automatic enforcement.

- **日本語**: レジストリは、ソースに裏づけられた所見を「レビューの証拠」として扱うべきで、自動的な強制には使うべきでない。
- **どう使っているか**: HintLint の出力を MCP レジストリ・ゲートウェイ・ガバナンス基盤が取り込むための形式。所見を該当ツールの近くに表示し、suggested_annotations で修正を助ける。メタデータだけのスキャンを証明とみなさない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Registry Artifact > Ingestion Guidance」（取得 2026-10-02T22:11:28Z、sha256 9f967731e673…）
- **補足**: 同ページ冒頭「They are not a trust score.」（exact）。

### mcpcheck（個人開発 rajanaggarwal11） — mcpcheck

<a id="g-c09-servers-gateways-security-40"></a>
#### C09-40 mcpcheck（個人開発 rajanaggarwal11） — mcpcheck

- **資料**: README.md「What it checks」（検査の道具の文書）
- **URL**: https://github.com/rajanaggarwal11/mcpcheck/blob/c330726d432c59e2900b2a9396b3ddb7761243c8/README.md#L47-L53
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/rajanaggarwal11/mcpcheck/c330726d432c59e2900b2a9396b3ddb7761243c8/README.md
- **版**: commit c330726d432c59e2900b2a9396b3ddb7761243c8（rajanaggarwal11/mcpcheck の 2026-10-02 時点の HEAD）
- **書いてある場所**: L47-53（直前の見出し: ## What it checks）
- **原文**:

> | `annotation-honesty`  | error        | A tool named like a delete or a write that claims `readOnlyHint: true` — the client skips confirmation on the strength of that. Or `readOnlyHint` and `destructiveHint` both true.                                                                                                                                                                                                                                                           |
> | `schema-validity`     | error / warn | An input schema that requires properties it doesn't define, leaves a parameter untyped, or declares no properties at all.                                                                                                                                                                                                                                                                                                                    |
> | `missing-annotations` | warn         | No `readOnlyHint` / `destructiveHint`, so a client can't tell whether to ask the human first.                                                                                                                                                                                                                                                                                                                                                |
>
> `mcpcheck --list-rules` prints the same table. The annotation and over-broad rules are heuristics and say so: they exist to make a person look, not to convict.

- **日本語**: annotation-honesty（error）: 削除や書き込みのような名前なのに readOnlyHint:true を名乗るツール（クライアントはそれを根拠に確認を飛ばす）、または readOnlyHint と destructiveHint が両方 true。missing-annotations（warn）: readOnlyHint / destructiveHint が無く、クライアントが人に確認すべきか判断できない。注釈と over-broad の規則は発見的なもので、人に見てもらうためにあり、断定するためではない。
- **どう使っているか**: ツールを呼ばずに tools/list の定義だけを見て、名前と注釈の食い違いや注釈の欠落を検出するリンター（コードは読まない）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を検査する・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、47-51 行（## What it checks）（取得 2026-10-02T22:11:36Z、sha256 0ee3ebdb2315…）
- **補足**: README の実測表（L95-96）に next-devtools-mcp 0.4.0 について「no tool declares `readOnlyHint` or `destructiveHint`, so a client cannot tell which to confirm」（exact）。 [verifier] README L15「It never calls a tool.** Every check is over what the server advertises.」（exact）のとおり、tools/list の定義だけを見る。 注意を追加: 「the client skips confirmation on the strength of that」はツール作者の主張で、特定のクライアントの一次資料ではない。

### Nova-Hunting（Nova Proximity） — Nova Proximity（MCP サーバーの調査ツール）

<a id="g-c09-servers-gateways-security-41"></a>
#### C09-41 Nova-Hunting（Nova Proximity） — Nova Proximity（MCP サーバーの調査ツール）

- **資料**: novaprox.py（ツール一覧の表示）（検査の道具のソースコード）
- **URL**: https://github.com/Nova-Hunting/nova-proximity/blob/d7521742dd8d25efee9b75f9fff2e7c8e8774cdb/novaprox.py#L477-L490
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Nova-Hunting/nova-proximity/d7521742dd8d25efee9b75f9fff2e7c8e8774cdb/novaprox.py
- **版**: commit d7521742dd8d25efee9b75f9fff2e7c8e8774cdb（Nova-Hunting/nova-proximity の 2026-10-02 時点の HEAD）
- **書いてある場所**: L477-490
- **原文**:

```
                # Display security annotations if present (MCP Spec 2025-11-25)
                if tool.get("annotations"):
                    annotations = tool["annotations"]
                    hints = []
                    if annotations.get("readOnlyHint"):
                        hints.append(f"{GREEN}read-only{RESET}")
                    if annotations.get("destructiveHint"):
                        hints.append(f"{RED}destructive{RESET}")
                    if not annotations.get("idempotentHint"):
                        hints.append(f"{YELLOW}non-idempotent{RESET}")
                    if annotations.get("openWorldHint"):
                        hints.append(f"{CYAN}external-access{RESET}")
                    if hints:
                        print(f"   {CYAN}Security Hints:{RESET} {', '.join(hints)}")
```

- **日本語**: 注釈があれば「Security Hints」として表示する。readOnlyHint→read-only（緑）、destructiveHint→destructive（赤）、idempotentHint が真でなければ non-idempotent（黄）、openWorldHint→external-access（水色）。
- **どう使っているか**: 宣言をそのまま色付きのラベルで見せる（真偽は確かめない）。idempotentHint が無いときは non-idempotent と表示するが、destructiveHint・openWorldHint が無いときは何も表示しない（仕様の既定 true を反映しない）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、477-490 行（取得 2026-10-02T22:11:30Z、sha256 7fdaca5b922d…）
- **補足**: 補足: 表示は注釈オブジェクトが空でないときだけ。destructiveHint・openWorldHint は値が真のときだけ表示し、省略は表示しない（仕様の既定は true なのに出ない）。一方 idempotentHint は省略でも non-idempotent と出る（既定 false と一致）。仕様の既定値の扱いが項目ごとに揃っていない。

### Glama — Glama（MCP ディレクトリ・レジストリ）

<a id="g-c09-servers-gateways-security-42"></a>
#### C09-42 Glama — Glama（MCP ディレクトリ・レジストリ）

- **資料**: How Glama indexes the MCP ecosystem「1.4 Protocol introspection」（公式の文書）
- **URL**: https://glama.ai/mcp/methodology
- **版**: 2026-10-02 取得（sha256=a9c6993faeb4）
- **書いてある場所**: How Glama indexes the MCP ecosystem > 1. Open-source MCP servers > 1.4 Protocol introspection
- **原文**:

> The complete JSON Schema for every tool, resource, and prompt is captured – including MCP annotation hints (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) – and stored as the authoritative description of the server's declared capabilities.

- **日本語**: 各ツール・リソース・プロンプトの JSON Schema を、MCP の注釈ヒント（readOnlyHint・destructiveHint・idempotentHint・openWorldHint）を含めて取り込み、サーバーが宣言した能力の正式な記述として保存する。
- **どう使っているか**: ディレクトリがサンドボックスでサーバーを動かして tools/list を取り、注釈を含む定義を「宣言された能力の正式な記述」として保存する。同じ方法論の行動解析（1.5）は syscall・ネットワークを観測し「declared capability set に要らない認証情報パスへのアクセス」などを探すが、注釈の値と照合するかは書かれていない（不明）。
- **条件**: オープンソースのサーバーはサンドボックスで起動して取得。コネクタ（リモート）は定期的に introspection（2.x 節）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「How Glama indexes the MCP ecosystem > 1. Open-source MCP servers > 1.4 Protocol introspection」（取得 2026-10-02T22:11:29Z、sha256 89ab66a7eb66…）
- **補足**: 見出しに id が無く anchored_url なし。注釈は TDQS（43）の採点にも使う。 言い過ぎを修正: 1.5 Behavioural analysis は「Access to credential paths not required by the declared capability set」（exact）を探すと書き、この「宣言された能力」は 1.4 で保存したもの（注釈を含む）を指すように読める。ただし注釈（readOnlyHint など）と観測を照合するとは明記していない（不明）。

### Glama — Tool Definition Quality Score（glama-ai/tool-definition-quality-score）

<a id="g-c09-servers-gateways-security-43"></a>
#### C09-43 Glama — Tool Definition Quality Score（glama-ai/tool-definition-quality-score）

- **資料**: README.md「The six dimensions」（公式の文書）
- **URL**: https://github.com/glama-ai/tool-definition-quality-score/blob/b9881b0cfec88969e42672c92544487ca191a992/README.md#L182-L182
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/glama-ai/tool-definition-quality-score/b9881b0cfec88969e42672c92544487ca191a992/README.md
- **版**: commit b9881b0cfec88969e42672c92544487ca191a992（glama-ai/tool-definition-quality-score の 2026-10-02 時点の HEAD）
- **書いてある場所**: L182（直前の見出し: #### The six dimensions）
- **原文**:

> - **Behavioral Transparency**: graded relative to annotations. When annotations exist, the bar is lower: the description earns credit for adding context annotations cannot carry (what gets destroyed, auth requirements, rate limits). Without annotations, the description carries the full disclosure burden. A description that **contradicts** its annotations scores 1 and raises the `Annotation Contradiction` flag.

- **日本語**: 「振る舞いの透明性」は注釈と比べて採点する。注釈があれば基準は下がり、説明は注釈では運べない情報（何が消えるか、認証、レート制限）を足せば点になる。注釈が無ければ説明が開示の負担をすべて負う。注釈と矛盾する説明は 1 点になり、Annotation Contradiction のフラグが立つ。
- **どう使っているか**: ディレクトリの品質スコア（TDQS）が、注釈を説明文の採点の前提に使い、説明と注釈の矛盾を LLM に判定させてフラグにする。注釈と実装（コード）の照合はしない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 危険度を付ける・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、182 行（#### The six dimensions）（取得 2026-10-02T22:11:34Z、sha256 3df9d731cb06…）
- **補足**: 同 README L333「TDQS scores definitions, not behavior.」（exact）。L111 で annotationValues（未宣言なら null）を決定的な信号として取る（exact）。

### Smithery — Smithery Connect API

<a id="g-c09-servers-gateways-security-44"></a>
#### C09-44 Smithery — Smithery Connect API

- **資料**: Get tool（API reference、OpenAPI の応答スキーマ）（公式の文書）
- **URL**: https://smithery.ai/docs/api-reference/connect/get-tool
- **照らし合わせた中身の URL**: https://smithery.ai/docs/api-reference/connect/get-tool.md
- **版**: 2026-10-02 取得（sha256=3b915018414b）
- **書いてある場所**: L163-166（直前の見出し: ## OpenAPI）
- **原文**:

```
readOnlyHint:
              type: boolean
            destructiveHint:
              type: boolean
```

- **日本語**: Get tool の応答スキーマの annotations に、readOnlyHint（boolean）と destructiveHint（boolean）がある（ほかに title・idempotentHint・openWorldHint）。
- **どう使っているか**: Smithery の Connect API は接続先サーバーのツールを返すとき注釈も返す（スキーマ上）。Smithery が注釈で何かを判定するという記述は文書（llms-full.txt）に無い。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、163-166 行（## OpenAPI）（取得 2026-10-02T22:11:46Z、sha256 3b915018414b…）
- **補足**: 公開ページ（HTML）の url と、照合した .md（Mintlify の Markdown 版）を分けて記録。Smithery の品質スコアに注釈の配点がある、という話は第三者記事（dev.to など、配点が 7 点・20 点と食い違う）だけで、一次資料は見つからず未確認（unreachable 参照）。

### TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

<a id="g-g2-gateways-platforms-01"></a>
#### G2GP-01 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: MCP Tool Management（公式の文書）
- **URL**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-management
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-management#edit-tool-description-and-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: MCP Tool Management > Edit tool description and annotations (#edit-tool-description-and-annotations)
- **原文**:

> sets readOnlyHint or destructiveHint for clients that respect MCP tool annotations

- **日本語**: （Edit Tool の「MCP Tool Annotations」欄で None / Read-only / Destructive を選ぶと）MCP のツール注釈を尊重するクライアント向けに readOnlyHint か destructiveHint を設定する。
- **どう使っているか**: ゲートウェイの管理者がツールごとに注釈を上書きし、上書き後の値をクライアントに見せる（サーバー作者の宣言でなく管理者の宣言になる）。
- **条件**: 管理者が Remote / TrueFoundry-managed MCP サーバーの Tools タブで Edit Tool を開いたとき
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: そのまま渡す・見せる・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Management > Edit tool description and annotations」（取得 2026-10-02T22:11:41Z、sha256 2532bf595f2c…）
- **補足**: 選択肢は None / Read-only / Destructive の 3 つだけで、idempotentHint / openWorldHint / title は UI から設定できない。None を選んだときに上流の値を消すのか素通しにするのかは文書に書かれていない（不明）。Reset to Default で上書きを外せる。

<a id="g-g2-gateways-platforms-02"></a>
#### G2GP-02 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: MCP Tool Management（公式の文書）
- **URL**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-management
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-management#when-to-use
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Tool Management > When to use (#when-to-use)
- **原文**:

> Improve LLM tool selection - override upstream descriptions or mark tools as read-only or destructive.

- **日本語**: LLM のツール選択を良くする：上流の説明文を上書きしたり、ツールを read-only または destructive と印を付けたりする。
- **どう使っているか**: 注釈の上書きを「LLM のツール選択を良くする」用途として案内している（安全のためでなく選択の手がかりとして）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Management > When to use」（取得 2026-10-02T22:11:41Z、sha256 2532bf595f2c…）
- **補足**: 「When to use」節の 1 項目。同じ節に「破壊的な書き込みツールを隠す」用途は別項目（有効/無効の切り替え）として書かれている。

<a id="g-g2-gateways-platforms-03"></a>
#### G2GP-03 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: MCP Tool Approvals（公式の文書）
- **URL**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval#approval-scope
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Tool Approvals > Approval scope (#approval-scope)
- **原文**:

> Tools the MCP server marks as destructive (destructiveHint: true)

- **日本語**: （approval_scope: destructive が承認の対象にするのは）MCP サーバーが destructive と印を付けたツール（destructiveHint: true）。
- **どう使っているか**: 承認ポリシーの scope に destructive があり、destructiveHint:true のツールをまとめて人の承認待ちにする。
- **条件**: 管理者が AI Gateway → Policies → MCP Tool Approval でポリシーを作り、approval_scope: destructive を選んだとき
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Approvals > Approval scope」（取得 2026-10-02T22:11:55Z、sha256 cfe1d63e5c04…）
- **補足**: scope は named / destructive / all の 3 つ。readOnlyHint を条件にする scope は無い。destructiveHint が欠けている（未宣言）ツールは destructive に入らないと読めるが、仕様の既定値（true）を当てはめるかは文書に書かれていない（不明。TrueForge 側のコードは === true の比較で欠落を false 扱い、#11 参照）。ゲートウェイが比較に使う値が上流の値か管理者の上書き（#01）後の値かも書かれていない（不明）。

<a id="g-g2-gateways-platforms-04"></a>
#### G2GP-04 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: MCP Tool Approvals（公式の文書）
- **URL**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval#frequently-asked-questions
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Tool Approvals > Frequently asked questions (#frequently-asked-questions)
- **原文**:

> Tools the MCP server annotates with destructiveHint: true. Use approval_scope: destructive to require approval for all of them without listing each name.

- **日本語**: （destructive なツールとは）MCP サーバーが destructiveHint: true と注釈したツール。approval_scope: destructive を使えば、名前を 1 つずつ並べずに、その全部に承認を求められる。
- **どう使っているか**: destructiveHint:true を「名前を並べずに承認対象をまとめる」ための選択子として使う。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Approvals > Frequently asked questions」（取得 2026-10-02T22:11:55Z、sha256 cfe1d63e5c04…）
- **補足**: FAQ「What counts as a destructive tool?」の答え。#03 と同じ規則を言い直したもの。

<a id="g-g2-gateways-platforms-05"></a>
#### G2GP-05 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: MCP Tool Approvals（公式の文書）
- **URL**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/ai-gateway/mcp/mcp-tool-approval#approval-scope
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Tool Approvals > Approval scope (#approval-scope)
- **原文**:

> When more than one scope could apply to the same tool, the gateway picks the most specific match, in this order:

- **日本語**: 同じツールに複数の scope が当てはまるときは、ゲートウェイは最も具体的なものを選ぶ。順番は（named > destructive > all）。
- **どう使っているか**: 名前指定の規則が destructiveHint による規則より優先する。名前で指定すれば注釈の有無に関係なく承認対象にできる。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Approvals > Approval scope」（取得 2026-10-02T22:11:55Z、sha256 cfe1d63e5c04…）
- **補足**: 引用の直後に「named > destructive > all」と「So a named rule for multiply overrides a broader destructive or all-tools rule for that tool.」が続く。有効期間（validity）は最も厳しいものが勝つ（Once > 短い時間 > 長い時間）。

<a id="g-g2-gateways-platforms-06"></a>
#### G2GP-06 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway）

- **資料**: Deprecation of MCP tool_settings — 26th October, 2026（リリースノート）
- **URL**: https://www.truefoundry.com/docs/change-announcements/deprecation-of-mcp-tool-settings
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/change-announcements/deprecation-of-mcp-tool-settings#what-is-changing
- **版**: 告知 2026-08-26、tool_settings の削除予定 2026-10-26
- **書いてある場所**: Deprecation of MCP tool_settings - 26th October, 2026 > What Is Changing (#what-is-changing)
- **原文**:

> Per-tool description and annotation overrides

- **日本語**: （tool_metadata の目的は）ツールごとの説明文と注釈の上書き。
- **どう使っているか**: マニフェスト（GitOps / Terraform / PUT /v1/mcp）でもツールごとの注釈を上書きできる。旧 tool_settings の annotations は保存時に tool_metadata へ変換される。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: その他・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Deprecation of MCP tool_settings - 26th October, 2026 > What Is Changing」（取得 2026-10-02T22:12:09Z、sha256 ccec6f8c0ecb…）
- **補足**: 移行例は tool_metadata: search: annotations: readOnlyHint: true。旧 tool_settings は無効化（disabled: true）だけを表す denylist で、新しい tool_policy は enable_tools_by_default: false による allowlist も表せる。OpenAPI MCP サーバーは対象外。 対象は Remote / Stdio / TrueFoundry-managed の MCP サーバーのマニフェスト（UI の Tools タブだけを使う人は対応不要）。 notes に対象のサーバー種別（Stdio を含む）を補った。

### TrueFoundry — TrueFoundry Agent Platform（TrueForge のマネージド版）

<a id="g-g2-gateways-platforms-07"></a>
#### G2GP-07 TrueFoundry — TrueFoundry Agent Platform（TrueForge のマネージド版）

- **資料**: What TrueFoundry Adds on Top of TrueForge（公式の文書）
- **URL**: https://www.truefoundry.com/docs/agent-platform/agent-harness/what-truefoundry-adds
- **書いてある見出しへ直接**: https://www.truefoundry.com/docs/agent-platform/agent-harness/what-truefoundry-adds#mcp-servers
- **版**: 2026-10-02 取得
- **書いてある場所**: What TrueFoundry Adds on Top of TrueForge > Deep gateway integration > MCP servers (#mcp-servers)
- **原文**:

> Tools flagged as destructive at the gateway automatically pause for human approval in every agent, rather than each agent having to declare its own approval policy.

- **日本語**: ゲートウェイで destructive と印を付けたツールは、すべてのエージェントで自動的に人の承認待ちになる。エージェントごとに承認ポリシーを宣言する必要はない。
- **どう使っているか**: ゲートウェイで destructive と印を付けたツールを、組織全体の方針として全エージェントで人の承認待ちにする、と製品紹介ページが述べる（印が MCP 注釈 destructiveHint を指すかはこのページでは明示されていない）。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「What TrueFoundry Adds on Top of TrueForge > Deep gateway integration > MCP servers」（取得 2026-10-02T22:11:39Z、sha256 09f87dbfdf8f…）
- **補足**: 製品の紹介・比較ページ（マーケティング寄り）。同じページの比較表は、Claude Managed Agents を「Per-tool permission_policy declared in each agent JSON (default always_ask). Forgetting to set it on a sensitive tool means it runs without confirmation.」、LangSmith Managed Deep Agents を「missed entries mean no approval gate」と書く。これは TrueFoundry による競合製品の説明で、Claude 側の記述は「既定 always_ask」と「付け忘れると確認なしで動く」が同じ文の中で食い違っており、競合製品の挙動の根拠には使えない。TrueFoundry 側でも、印の無いツールは destructive scope に入らない（#03, #04）。「flagged as destructive at the gateway」が上流の destructiveHint を含むのか管理者の上書き（#01）だけかは、このページでは区別されていない（不明）。 usage_ja が「注釈」と断定していたのを、ページの言い方（flagged as destructive at the gateway）に合わせて弱めた。比較表は競合についての TrueFoundry の主張で、Claude Managed Agents の説明が文中で自己矛盾している点を notes に明記した。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools

<a id="g-g2-gateways-platforms-08"></a>
#### G2GP-08 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools

- **資料**: Create an Agent（trueforge.dev）（SDK の文書）
- **URL**: https://trueforge.dev/create-agent/overview
- **書いてある見出しへ直接**: https://trueforge.dev/create-agent/overview#what’s-in-an-agent
- **版**: 2026-10-02 取得（版表示なし。記述の既定値は commit 5b7abb6 のコード #12 と一致）
- **書いてある場所**: Create an Agent > What's in an agent (#what’s-in-an-agent)
- **原文**:

> By default, the agent asks for approval before tools the MCP server marks as write or destructive

- **日本語**: 既定では、エージェントは MCP サーバーが write または destructive と印を付けたツールの前に承認を求める。
- **どう使っているか**: 既定（require_approval_for_tools = ["@write","@destructive"]）で、write / destructive と注釈されたツールだけ承認を求め、read-only のツールは承認なしで動かす。
- **条件**: 既定設定のとき。UI の盾アイコンや API の require_approval_for_tools で変更できる
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Create an Agent > What's in an agent」（取得 2026-10-02T22:11:41Z、sha256 0819bcca474e…）
- **補足**: 引用の直後に「(require_approval_for_tools defaults to ["@write", "@destructive"]). Read-only tools run on their own.」が続く。@write = readOnlyHint === false かつ destructiveHint !== true、@destructive = destructiveHint === true（#11 のコード）。 同じページの UI 説明では、Select MCP Tools の各ツールの盾アイコンで承認を切り替え、Other Actions / Destructive Actions の見出しに「Approval required」スイッチがある。承認は chat UI の Allow / Deny で行う。 version の「TrueForge 0.3.0 系」はページに表示が無いので、コードとの一致として書き直した。

<a id="g-g2-gateways-platforms-09"></a>
#### G2GP-09 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools

- **資料**: Create an Agent（trueforge.dev）（SDK の文書）
- **URL**: https://trueforge.dev/create-agent/overview
- **書いてある見出しへ直接**: https://trueforge.dev/create-agent/overview#what’s-in-an-agent
- **版**: 2026-10-02 取得
- **書いてある場所**: Create an Agent > What's in an agent (#what’s-in-an-agent)
- **原文**:

> @write and @destructive only match tools the MCP server has labeled. Many servers skip labels, so those tools run without asking — even if they change data.

- **日本語**: @write と @destructive は、MCP サーバーが印を付けたツールにしか当たらない。印を付けないサーバーが多いので、そうしたツールはデータを変えるものでも承認なしで動く。
- **どう使っているか**: 注釈が欠けたツールは承認の対象外になり、データを変えるツールでも承認なしで動くと、文書自身が注意書きで認めている（「fail-open」はこちらの言い方）。対策は名前で列挙するか @all にすること。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Create an Agent > What's in an agent」（取得 2026-10-02T22:11:41Z、sha256 0819bcca474e…）
- **補足**: 欠落時に承認なしになることを公式文書が明記している例。仕様の既定値（readOnlyHint 既定 false、destructiveHint 既定 true）を当てはめれば未宣言ツールは destructive に当たるが、TrueForge はその既定を当てはめていない（仕様はクライアントに既定の適用を義務づけてはいない）。 「fail-open」は原文の語ではないことと、仕様の既定値の適用は義務ではないことを明記した。

<a id="g-g2-gateways-platforms-10"></a>
#### G2GP-10 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — エージェント定義の require_approval_for_tools

- **資料**: Create an Agent（trueforge.dev） — mcp_servers の表（SDK の文書）
- **URL**: https://trueforge.dev/create-agent/overview
- **書いてある見出しへ直接**: https://trueforge.dev/create-agent/overview#mcp_servers
- **版**: 2026-10-02 取得
- **書いてある場所**: Create an Agent > Create an agent via the API > mcp_servers (#mcp_servers)
- **原文**:

> Unlabeled tools (and tools marked read-only) are not covered by @write / @destructive, so they run without an approval pause. Gate them by name, or use @all.

- **日本語**: 印の無いツール（と read-only と印を付けたツール）は @write / @destructive に入らないので、承認待ちなしで動く。名前で指定するか @all を使う。
- **どう使っているか**: 未宣言ツールと readOnlyHint:true のツールを同じ扱い（承認なし）にする。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Create an Agent > Create an agent via the API > mcp_servers」（取得 2026-10-02T22:11:41Z、sha256 0819bcca474e…）
- **補足**: API リファレンス側の記述。#09 と同じ内容を設定表の下で繰り返している。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — @write / @destructive 選択子の解決

<a id="g-g2-gateways-platforms-11"></a>
#### G2GP-11 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — @write / @destructive 選択子の解決

- **資料**: packages/trueforge-core/src/core/mcp/toolSelectors.ts（SDK のソースコード）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/mcp/toolSelectors.ts#L38-L44
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/mcp/toolSelectors.ts
- **版**: commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea
- **書いてある場所**: packages/trueforge-core/src/core/mcp/toolSelectors.ts L38-44
- **原文**:

```
function isWrite(annotations?: ToolAnnotations): boolean {
  return annotations?.readOnlyHint === false && annotations.destructiveHint !== true;
}

function isDestructive(annotations?: ToolAnnotations): boolean {
  return annotations?.destructiveHint === true;
}
```

- **日本語**: isWrite は readOnlyHint が false と明示され、かつ destructiveHint が true でないとき真。isDestructive は destructiveHint が true のときだけ真。
- **どう使っているか**: 承認選択子を注釈で解決する。=== true / === false の厳密比較なので、注釈が無い（undefined）ツールは write にも destructive にも当たらない。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、38-44 行（取得 2026-10-02T22:11:38Z、sha256 7ca46f43336f…）
- **補足**: readOnlyHint:false で destructiveHint 未宣言のツールは @write（destructive ではない）。仕様の既定 destructiveHint=true は使われていない。同じファイルの L28 に既定 DEFAULT_REQUIRE_APPROVAL_FOR_TOOLS = [@write, @destructive]（#12）。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認の既定値

<a id="g-g2-gateways-platforms-12"></a>
#### G2GP-12 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認の既定値

- **資料**: packages/trueforge-core/src/core/mcp/toolSelectors.ts（SDK のソースコード）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/mcp/toolSelectors.ts#L28
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/mcp/toolSelectors.ts
- **版**: commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea
- **書いてある場所**: packages/trueforge-core/src/core/mcp/toolSelectors.ts L28
- **原文**:

> export const DEFAULT_REQUIRE_APPROVAL_FOR_TOOLS: string[] = [TOOL_TAG_WRITE, TOOL_TAG_DESTRUCTIVE];

- **日本語**: require_approval_for_tools の既定値は [@write, @destructive]。
- **どう使っているか**: 既定で承認を求めるのは注釈で write / destructive と分かるツールだけ。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、28 行（取得 2026-10-02T22:11:38Z、sha256 7ca46f43336f…）
- **補足**: #15/#16 の CHANGELOG のとおり、この既定は 0.2.0 系（0.2.0-rc の段階から）で @destructive のみに狭められ、0.3.0 で @write + @destructive に戻された。0.2.0 の項は「Migrate mounts still carrying the old @write+@destructive default」とも書き、それ以前の既定も @write + @destructive だった。 変遷の説明を CHANGELOG の版見出しに合わせて補った（551b6a8 は 0.2.0-rc 系の節にもある）。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — Code Mode の破壊的ツール拒否

<a id="g-g2-gateways-platforms-13"></a>
#### G2GP-13 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — Code Mode の破壊的ツール拒否

- **資料**: packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py（サンドボックス内 MCP クライアント）（SDK のソースコード）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py#L224-L227
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py
- **版**: commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea
- **書いてある場所**: packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py L224-227
- **原文**:

```
def _is_destructive(tool: Tool) -> bool:
    annotations = tool.annotations
    if annotations is None:
        return False
```

- **日本語**: _is_destructive は、ツールの annotations が None なら False を返す。
- **どう使っているか**: Code Mode（サンドボックスのスクリプトから MCP ツールを直接呼ぶ）では destructive なツールの呼び出しを拒むが、注釈の無いツールは destructive でないと判定して通す（fail-open）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、224-227 行（# Approvals are always enabled (Sandbox always injects TFY_ENABLE_AGENT_APPROVALS=true).）（取得 2026-10-02T22:11:41Z、sha256 354ca81751dd…）
- **補足**: 同じ関数の L235 は `return bool(destructive) or (not read_only and read_only is not None)` で、readOnlyHint:false と明示されたツールも destructive 扱い（拒否）にする。annotations があってもどちらのヒントも無ければ拒否しない。つまり Code Mode の門は「readOnlyHint:false または destructiveHint:true なら拒否、注釈なし・ヒントなしなら許可」。この門は _enable_agent_approvals（環境変数 TFY_ENABLE_AGENT_APPROVALS、既定 "true"、Sandbox.ts が常に true を注入）が真のときだけ働く（L70, L273-274）。issue #318（WebSearch の題名で見ただけ、#49）がこの挙動を指していると思われる。 門が働く条件（TFY_ENABLE_AGENT_APPROVALS）と、ヒントの無い annotations も通ることを notes に補った。

<a id="g-g2-gateways-platforms-14"></a>
#### G2GP-14 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — Code Mode の破壊的ツール拒否

- **資料**: packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py（SDK のソースコード）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py#L243
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py
- **版**: commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea
- **書いてある場所**: packages/trueforge-core/src/core/sandbox/scripts/mcp_client.py L243
- **原文**:

> is destructive and cannot be called in Code Mode;

- **日本語**: （エラー文）…は destructive なので Code Mode では呼べない。承認フローを通るように直接呼ぶこと。
- **どう使っているか**: 注釈で destructive と判定したツールをスクリプトからは呼ばせず、直接のツール呼び出し（承認フローあり）に回す。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、243 行（# Approvals are always enabled (Sandbox always injects TFY_ENABLE_AGENT_APPROVALS=true).）（取得 2026-10-02T22:11:41Z、sha256 354ca81751dd…）
- **補足**: L242-244 の RuntimeError の文言の一部。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認既定値の変遷

<a id="g-g2-gateways-platforms-15"></a>
#### G2GP-15 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認既定値の変遷

- **資料**: packages/trueforge/CHANGELOG.md — 0.3.0（リリースノート）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge/CHANGELOG.md#L12
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge/CHANGELOG.md
- **版**: 0.3.0（commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea の CHANGELOG）
- **書いてある場所**: packages/trueforge/CHANGELOG.md L12
- **原文**:

> Default MCP tool approval to `@write` and `@destructive` again. Unlabeled tools still run without a pause unless named or covered by `@all`.

- **日本語**: MCP ツール承認の既定を @write と @destructive に戻す。印の無いツールは、名前で指定するか @all で覆わない限り、引き続き承認待ちなしで動く。
- **どう使っているか**: 未宣言ツールは承認なしで動くことをリリースノートでも明記。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、12 行（### Patch Changes）（取得 2026-10-02T22:11:37Z、sha256 4d94ead47ff9…）
- **補足**: 変更 33cbe52。同じ文が trueforge-core / trueforge-sdk / trueforge-ui の CHANGELOG にもある。WebSearch で見た PR #895「Restore default MCP tool approval to write and destructive」（github.com なので未確認）がこの変更に当たると思われる。

<a id="g-g2-gateways-platforms-16"></a>
#### G2GP-16 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge — 承認既定値の変遷

- **資料**: packages/trueforge/CHANGELOG.md — 0.2.0（リリースノート）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge/CHANGELOG.md#L145
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge/CHANGELOG.md
- **版**: 0.2.0（commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea の CHANGELOG）
- **書いてある場所**: packages/trueforge/CHANGELOG.md L145
- **原文**:

> Default MCP tool approval to `@destructive` only. Selecting Other/read-only tools clears approval; selecting destructive tools keeps it on.

- **日本語**: MCP ツール承認の既定を @destructive だけにする。Other / read-only のツールを選ぶと承認が外れ、destructive のツールを選ぶと承認が残る。
- **どう使っているか**: 0.2.0 の一時期は、readOnlyHint:false の書き込みツールも既定では承認なしだった。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・2 か所、145 行（### Patch Changes）（取得 2026-10-02T22:11:37Z、sha256 4d94ead47ff9…）
- **補足**: 変更 551b6a8。0.3.0 で #15 のとおり戻された。

### TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge UI — ツール選択画面の分類

<a id="g-g2-gateways-platforms-17"></a>
#### G2GP-17 TrueFoundry / TrueForge（OSS エージェント実行基盤 truefoundry/trueforge） — TrueForge UI — ツール選択画面の分類

- **資料**: packages/trueforge-ui/src/atoms/draft/mcpToolSections.ts（クライアントのソースコード）
- **URL**: https://github.com/truefoundry/trueforge/blob/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-ui/src/atoms/draft/mcpToolSections.ts#L24-L26
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/truefoundry/trueforge/5b7abb645a7074d4ec1cbcf858e8d7aef195bcea/packages/trueforge-ui/src/atoms/draft/mcpToolSections.ts
- **版**: commit 5b7abb645a7074d4ec1cbcf858e8d7aef195bcea
- **書いてある場所**: packages/trueforge-ui/src/atoms/draft/mcpToolSections.ts L24-26
- **原文**:

```
  if (annotations?.readOnlyHint === true) return 'read-only';
  if (annotations?.destructiveHint === true) return 'destructive';
  return 'others';
```

- **日本語**: readOnlyHint が true なら「read-only」節、destructiveHint が true なら「destructive」節、それ以外は「others」節に入れる。
- **どう使っているか**: エージェント作成画面でツールを Read-only / Destructive / Other の見出しに分けて表示する。注釈の無いツールは Other に入る。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、24-26 行（取得 2026-10-02T22:13:01Z、sha256 7cb4ccc751e9…）
- **補足**: readOnlyHint と destructiveHint が両方 true のツールは read-only 節に入る（packages/trueforge-ui/test/atoms/draft/mcpToolSections.test.ts の 'both' の例）。readOnlyHint:false だけのツールも others 節に入る。文書（#08）では「Approval required」スイッチがあるのは Other Actions / Destructive Actions の見出しで、read-only の見出しには書かれていない。 「各見出しに Approval required スイッチ」は誤り。文書では Other / Destructive の 2 見出しだけなので直した。テストのパスを補った。

### TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） × Databricks managed MCP

<a id="g-g2-gateways-platforms-18"></a>
#### G2GP-18 TrueFoundry — TrueFoundry AI Gateway（MCP Gateway） × Databricks managed MCP

- **資料**: Databricks MCP Server: Tools, Setup, and Governing Agent Access（TrueFoundry ブログ）（公式ブログ）
- **URL**: https://www.truefoundry.com/blog/databricks-mcp-server
- **版**: 2026-09-17 公開（ページ表示）、2026-10-02 取得
- **書いてある場所**: Databricks MCP Server: Tools, Setup, and Governing Agent Access > Scoping tools before you ship
- **原文**:

> Mark Genie read-only and SQL and Python destructive, and the policies below gate a whole class without naming every tool.

- **日本語**: Genie を read-only、SQL と Python を destructive と印を付ければ、下のポリシーで、ツールを 1 つずつ名前で並べずに種類ごとまとめて止められる。
- **どう使っているか**: ゲートウェイ（TrueFoundry）の管理者が Edit Tool で注釈を付け、その注釈を destructive scope の承認ポリシーに使う運用を勧めている。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Databricks MCP Server: Tools, Setup, and Governing Agent Access > Scoping tools before you ship」（取得 2026-10-02T22:11:40Z、sha256 e4dce45cd4d0…）
- **補足**: 自社製品の解説ブログ。上流（Databricks managed MCP）がツール注釈を出しているかどうかには触れていない。同じ記事は SQL と Python のエンドポイントには all scope も「defensible」とし、「For UC functions, annotate the writers Destructive and use destructive.」と書く。承認ポリシーはコンソールで Beta 表示。Databricks 自身の文書は注釈に触れていない（checked_no_mention 参照）。 usage_ja の「上流の注釈に頼らず」は記事に書かれていない推測なので外した。公開日を補った。

### Zuplo — Zuplo MCP Gateway — capability filtering（projection）

<a id="g-g2-gateways-platforms-19"></a>
#### G2GP-19 Zuplo — Zuplo MCP Gateway — capability filtering（projection）

- **資料**: Capability filtering（公式の文書）
- **URL**: https://zuplo.com/docs/mcp-gateway/capability-filtering
- **書いてある見出しへ直接**: https://zuplo.com/docs/mcp-gateway/capability-filtering#projections
- **版**: 2026-10-02 取得
- **書いてある場所**: Capability filtering > Projections (#projections)
- **原文**:

> Projections let the gateway rewrite the description for clarity, override tool annotations like destructiveHint or readOnlyHint, attach _meta fields that downstream middleware reads

- **日本語**: projection により、ゲートウェイは説明文を分かりやすく書き換えたり、destructiveHint や readOnlyHint のようなツール注釈を上書きしたり、下流のミドルウェアが読む _meta を付けたりできる。
- **どう使っているか**: ゲートウェイが上流の注釈を書き換えてクライアントに出す。クライアントが見る注釈はサーバー作者でなくゲートウェイ設定者の宣言になりうる。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: その他・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Capability filtering > Projections」（取得 2026-10-02T22:13:03Z、sha256 4db645ab510e…）
- **補足**: 上書きは tools/list の応答に対して行われる。inputSchema / outputSchema は書き換えられない。ゲートウェイ自身が注釈で承認や遮断を決める記述はない（遮断は allow-list で行う）。 検証者の 1 回目の取得は curl (35) Connection reset で失敗。再取得で exact を確認した。

<a id="g-g2-gateways-platforms-20"></a>
#### G2GP-20 Zuplo — Zuplo MCP Gateway — capability filtering（projection）

- **資料**: Capability filtering（公式の文書）
- **URL**: https://zuplo.com/docs/mcp-gateway/capability-filtering
- **書いてある見出しへ直接**: https://zuplo.com/docs/mcp-gateway/capability-filtering#projections
- **版**: 2026-10-02 取得
- **書いてある場所**: Capability filtering > Projections (#projections)
- **原文**:

> Annotation and _meta overrides are deep-merged with the upstream values: fields the projection specifies win, fields it doesn't specify pass through.

- **日本語**: 注釈と _meta の上書きは上流の値と深くマージされる。projection が指定した項目が勝ち、指定しない項目はそのまま通る。
- **どう使っているか**: projection で書かなかった注釈項目は上流の値を素通しにする。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Capability filtering > Projections」（取得 2026-10-02T22:13:03Z、sha256 4db645ab510e…）
- **補足**: 上流が注釈を出していない場合に何かを補う記述はない（指定しなければ欠落のまま）。 検証者の 1 回目の取得は curl (35) Connection reset で失敗。再取得で exact を確認した。

### Zuplo — Zuplo MCP Gateway — mcp-capability-filter-inbound ポリシー

<a id="g-g2-gateways-platforms-21"></a>
#### G2GP-21 Zuplo — Zuplo MCP Gateway — mcp-capability-filter-inbound ポリシー

- **資料**: MCP Capability Filter Policy（公式の文書）
- **URL**: https://zuplo.com/docs/policies/mcp-capability-filter-inbound
- **書いてある見出しへ直接**: https://zuplo.com/docs/policies/mcp-capability-filter-inbound#overview
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Capability Filter Policy > Overview (#overview)
- **原文**:

> can override the downstream-facing description, merge annotations for tools, and merge _meta for future metadata such as role hints.

- **日本語**: （projection オブジェクトは）下流に見せる description を上書きでき、ツールの annotations をマージでき、将来の役割ヒントなどのために _meta をマージできる。
- **どう使っているか**: ポリシー設定でツールの注釈をマージ上書きする。設定例は create_invoice に destructiveHint: false を付けるもの。
- **扱う宣言**: 宣言全般・destructiveHint ／ **使い方の分類**: そのまま渡す・見せる・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Capability Filter Policy > Overview」（取得 2026-10-02T22:11:40Z、sha256 9382637c2405…）
- **補足**: 例の create_invoice は『会計担当向けに請求書を作る』ツールで、ゲートウェイ側で destructiveHint:false と宣言している。

### Zuplo — Zuplo MCP Server handler（OpenAPI ルートを MCP ツールとして公開）

<a id="g-g2-gateways-platforms-22"></a>
#### G2GP-22 Zuplo — Zuplo MCP Server handler（OpenAPI ルートを MCP ツールとして公開）

- **資料**: MCP Server Tools（公式の文書）
- **URL**: https://zuplo.com/docs/mcp-server/tools
- **書いてある見出しへ直接**: https://zuplo.com/docs/mcp-server/tools#route-configuration
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Server Tools > Configuration > Route Configuration (#route-configuration)
- **原文**:

> readOnlyHint (boolean: optional) - Hint that the tool is read-only.

- **日本語**: readOnlyHint（boolean、任意）— ツールが読み取り専用であるというヒント。
- **どう使っているか**: OpenAPI のルートに x-zuplo-route.mcp.annotations を書いて 5 つの注釈を宣言できる（任意）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Server Tools > Configuration > Route Configuration」（取得 2026-10-02T22:11:40Z、sha256 9b1c4f9163fa…）
- **補足**: 同じ箇所で destructiveHint を「Hint that the tool has mutating side effects」と説明しており、仕様の「destructive（非加法的）な更新」より広い意味で書いている。HTTP メソッド（GET など）から注釈を自動で付けるという記述は無い（不明）。

### agentic-community（AWS 系 OSS） — MCP Gateway & Registry（agentic-community/mcp-gateway-registry）

<a id="g-g2-gateways-platforms-23"></a>
#### G2GP-23 agentic-community（AWS 系 OSS） — MCP Gateway & Registry（agentic-community/mcp-gateway-registry）

- **資料**: registry/core/mcp_client.py — _extract_tool_details（サーバのソースコード）
- **URL**: https://github.com/agentic-community/mcp-gateway-registry/blob/7c82c0fe9d764a7aea44ed56658d3be8f5cd895d/registry/core/mcp_client.py#L638-L645
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agentic-community/mcp-gateway-registry/7c82c0fe9d764a7aea44ed56658d3be8f5cd895d/registry/core/mcp_client.py
- **版**: commit 7c82c0fe9d764a7aea44ed56658d3be8f5cd895d
- **書いてある場所**: registry/core/mcp_client.py L638-645
- **原文**:

```
            tool_details_list.append(
                {
                    "name": tool_name,
                    "description": tool_desc or "",
                    "parsed_description": parsed_desc,
                    "schema": tool_schema,
                }
            )
```

- **日本語**: ツールごとに name / description / parsed_description / schema だけを保存用の辞書に入れる。
- **どう使っているか**: レジストリ（制御面）が上流から取ったツール一覧を保存するとき annotations を落とす。レジストリの在庫・検索・UI に載るツール定義から注釈が消える。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、638-645 行（# MCP Client imports）（取得 2026-10-02T22:11:31Z、sha256 19b7024ceeca…）
- **補足**: _extract_tool_details（L574 から）の末尾。リポジトリ全体（tests を含む）で readOnlyHint / destructiveHint / read_only_hint / destructive_hint を grep しても 0 件。README によればゲートウェイ（データ面）は nginx のリバースプロキシで、tools/call はレジストリの Python を通らない。MCP クライアントがゲートウェイ経由で直接 tools/list を受け取る場合に注釈が残るかは、このコードからは分からない（不明）。WebSearch で見た issue #1818（未確認、#50）と一致する。 注釈が落ちるのは保存された在庫（制御面）で、nginx 経由のデータ面の tools/list については不明なので、usage_ja と notes を限定した。

<a id="g-g2-gateways-platforms-50"></a>
#### G2GP-50 agentic-community（AWS 系 OSS） — MCP Gateway & Registry（agentic-community/mcp-gateway-registry）

- **資料**: Issue #1818: Stored tool lists drop MCP tool annotations and miss schema changes（issue / PR / 提案の下書き）
- **URL**: https://github.com/agentic-community/mcp-gateway-registry/issues/1818
- **版**: 不明（WebSearch 結果の題名のみ）
- **書いてある場所**: issue 題名
- **原文**:

> Stored tool lists drop MCP tool annotations and miss schema changes

- **日本語**: 保存されたツール一覧は MCP のツール注釈を落とし、スキーマの変化も見逃す。
- **どう使っているか**: レジストリが注釈を保存しないことが issue として報告されている。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [未確認] github.com の issue ページは取得不可。WebSearch（2026-10-02）の結果題名で見ただけ。
- **補足**: commit 7c82c0f のコード（#23）で、保存する項目が name / description / parsed_description / schema だけであることを確認済み。issue が閉じたか・修正予定かは不明。 github.com の issue は検証者も読めなかった（GitHub MCP ツールもこの repo を許可していない）。未確認のまま。

### Permit.io — Permit MCP Gateway

<a id="g-g2-gateways-platforms-24"></a>
#### G2GP-24 Permit.io — Permit MCP Gateway

- **資料**: Getting started with Permit MCP Gateway — Trust level reference（公式の文書）
- **URL**: https://docs.permit.io/permit-mcp-gateway/guide/
- **書いてある見出しへ直接**: https://docs.permit.io/permit-mcp-gateway/guide/#authentication-methods
- **版**: 2026-10-02 取得
- **書いてある場所**: Getting started with Permit MCP Gateway > Configure how users sign in (#authentication-methods)
- **原文**:

> During import, the gateway assigns each tool a trust level by matching keywords anywhere in the tool name. You can override the level for any tool.

- **日本語**: 取り込みのとき、ゲートウェイはツール名のどこかに含まれるキーワードで、各ツールに信頼レベルを割り当てる。どのツールでもレベルを上書きできる。
- **どう使っているか**: ツールの危険度（low=読み取り / medium=書き込み / high=破壊）を MCP 注釈ではなくツール名のキーワードで決める。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Getting started with Permit MCP Gateway > Trust level reference」（取得 2026-10-02T22:12:51Z、sha256 3e3d0e6e114c…）
- **補足**: 同じページと consent-service ページで readOnlyHint / destructiveHint / tool annotations / annotations は 0 件（checked_no_mention）。medium のキーワードは create, write, update, set, modify, edit, put など、high は delete, remove, destroy, drop など。取り込み時に管理者がツールごとにレベルを変えたり、ツールを無効にしたりできる。エージェントが呼べるのは同意時のレベル以下のツールで、そのレベルは管理者が決めた上限（max trust level）を超えない。検証ツールの見出しは『Configure how users sign in』(#authentication-methods) と出たが、ページ上で引用は見出し『Trust level reference』の直後にある（#25 の検証では #trust-level-reference と出る）。 notes の「実効レベルは同意レベルと上限の小さい方」を、ページの言い方（上限までの範囲で同意時に選ぶ）に直した。

<a id="g-g2-gateways-platforms-25"></a>
#### G2GP-25 Permit.io — Permit MCP Gateway

- **資料**: Getting started with Permit MCP Gateway — Trust level reference（表）（公式の文書）
- **URL**: https://docs.permit.io/permit-mcp-gateway/guide/
- **書いてある見出しへ直接**: https://docs.permit.io/permit-mcp-gateway/guide/#trust-level-reference
- **版**: 2026-10-02 取得
- **書いてある場所**: Getting started with Permit MCP Gateway > Trust level reference (#trust-level-reference)
- **原文**:

> Default for tools not matching medium or high patterns

- **日本語**: （Low のレベルは）medium や high のパターンに当たらないツールの既定。
- **どう使っているか**: 名前のキーワードに当たらないツールは Low（読み取り操作扱い）になり、最も低い信頼レベルで同意したエージェントでも呼べる。名前で分類する方式で、当たらないものを最も緩い側に入れる（fail-open 側というのはこちらの解釈）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Getting started with Permit MCP Gateway > Trust level reference」（取得 2026-10-02T22:12:51Z、sha256 3e3d0e6e114c…）
- **補足**: 表の Low 行の『Naming patterns』欄。Low 行の『Includes』欄は「Read-only operations (default)」。 「fail-open」がこちらの解釈であることを明記した。

### Permit.io — Permit MCP Gateway — Consent Service

<a id="g-g2-gateways-platforms-26"></a>
#### G2GP-26 Permit.io — Permit MCP Gateway — Consent Service

- **資料**: How the consent flow works — Tool discovery（公式の文書）
- **URL**: https://docs.permit.io/permit-mcp-gateway/consent-service/
- **書いてある見出しへ直接**: https://docs.permit.io/permit-mcp-gateway/consent-service/#tool-discovery
- **版**: 2026-10-02 取得
- **書いてある場所**: How the consent flow works > What the Consent Service does behind the screens > Tool discovery (#tool-discovery)
- **原文**:

> The consent screen assigns each tool a trust level by the keywords in the tool name

- **日本語**: 同意画面は、ツール名のキーワードで各ツールに信頼レベルを割り当てる（管理者が取り込み時に見るのと同じ分類）。
- **どう使っているか**: ユーザーに見せる同意画面の Allowed / Denied 表示も名前ベースの分類による。注釈は使わない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「How the consent flow works > What the Consent Service does behind the screens > Tool discovery」（取得 2026-10-02T22:11:32Z、sha256 ebb2b5ef40a1…）
- **補足**: Dynamic MCPs で追加したサーバーでは、ユーザーが上限までツールごとにレベルを変えられる。

### Google Cloud — Apigee API hub リモート MCP サーバー（apihub.googleapis.com）

<a id="g-g2-gateways-platforms-27"></a>
#### G2GP-27 Google Cloud — Apigee API hub リモート MCP サーバー（apihub.googleapis.com）

- **資料**: MCP Tools Reference: apihub.googleapis.com — delete_api（公式の文書）
- **URL**: https://docs.cloud.google.com/apigee/docs/reference/apis/apihub/mcp/tools_list/delete_api
- **書いてある見出しへ直接**: https://docs.cloud.google.com/apigee/docs/reference/apis/apihub/mcp/tools_list/delete_api#tool-annotations
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Tools Reference: apihub.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Tool Annotations (#tool-annotations)
- **原文**:

> Destructive Hint: ✅ | Idempotent Hint: ✅ | Read Only Hint: ❌ | Open World Hint: ❌

- **日本語**: ツール注釈：Destructive Hint ✅ | Idempotent Hint ✅ | Read Only Hint ❌ | Open World Hint ❌
- **どう使っているか**: Google のマネージド MCP サーバー（Apigee API hub）の参照ページは、ツールごとに 4 つの注釈を表で示す（delete_api は destructive かつ idempotent）。
- **扱う宣言**: destructiveHint・idempotentHint・readOnlyHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tools Reference: apihub.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Tool Annotations」（取得 2026-10-02T22:11:24Z、sha256 68b386810363…）
- **補足**: Apigee 本体の『API を MCP ツールとして公開する』機能の文書（manage-mcp-tool-access / overview）には注釈の記述がない（checked_no_mention）。Google Cloud の MCP 参照ページの共通形式は C06 で扱っている可能性があるので重複に注意。 このページは注釈の値を表示しているだけで、宣言を必須とする記述は無い。 usage の required_to_declare は根拠が無いので外した（参照ページは値を表示するだけ）。

### DataHub（Acryl Data） — DataHub MCP Server

<a id="g-g2-gateways-platforms-28"></a>
#### G2GP-28 DataHub（Acryl Data） — DataHub MCP Server

- **資料**: DataHub MCP Server — Tools（公式の文書）
- **URL**: https://docs.datahub.com/docs/features/feature-guides/mcp
- **書いてある見出しへ直接**: https://docs.datahub.com/docs/features/feature-guides/mcp#tools
- **版**: 2026-10-02 取得
- **書いてある場所**: DataHub MCP Server > Tools (#tools)
- **原文**:

> so compatible clients (e.g. Claude) can surface which tools modify catalog state and prompt for confirmation accordingly.

- **日本語**: （全ツールに MCP 標準のヒント readOnlyHint, destructiveHint, idempotentHint を付けているので）対応するクライアント（例：Claude）は、どのツールがカタログの状態を変えるかを示し、それに応じて確認を求められる。
- **どう使っているか**: データ基盤のマネージド/OSS MCP サーバーが、全ツールに注釈を付けたと宣言し、確認 UI への利用を想定している。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: 作者への書き方の案内・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「DataHub MCP Server > Tools」（取得 2026-10-02T22:11:24Z、sha256 01160ecbef1c…）
- **補足**: 引用の直前は「All tools are annotated with MCP-standard hints (readOnlyHint, destructiveHint, idempotentHint)」。openWorldHint は挙げていない。 確認を求めるかどうかを決めるのはクライアント側で、DataHub はその利用を想定しているだけ。 require_confirmation はサーバー作者の想定であることを notes に補った。

### DataHub（Acryl Data） — DataHub MCP Server — 変更系ツール

<a id="g-g2-gateways-platforms-29"></a>
#### G2GP-29 DataHub（Acryl Data） — DataHub MCP Server — 変更系ツール

- **資料**: DataHub MCP Server — Mutation Tools（公式の文書）
- **URL**: https://docs.datahub.com/docs/features/feature-guides/mcp
- **書いてある見出しへ直接**: https://docs.datahub.com/docs/features/feature-guides/mcp#mutation-tools
- **版**: 2026-10-02 取得
- **書いてある場所**: DataHub MCP Server > Tools > Mutation Tools (#mutation-tools)
- **原文**:

> so MCP clients can require confirmation before invoking them.

- **日本語**: （変更系の各ツールには readOnlyHint: false を付けているので）MCP クライアントは呼ぶ前に確認を求められる。
- **どう使っているか**: 変更系ツールに readOnlyHint:false を明示し、確認の手がかりにさせる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「DataHub MCP Server > Tools > Mutation Tools」（取得 2026-10-02T22:11:24Z、sha256 01160ecbef1c…）
- **補足**: 変更系ツールは TOOLS_IS_MUTATION_ENABLED=true のときだけ有効になる（引用の直前）。

### LangGenius — Dify（ローコード基盤）の MCP ツール取り込み

<a id="g-g2-gateways-platforms-30"></a>
#### G2GP-30 LangGenius — Dify（ローコード基盤）の MCP ツール取り込み

- **資料**: api/core/tools/mcp_tool/provider.py（クライアントのソースコード）
- **URL**: https://github.com/langgenius/dify/blob/4b89972f552c7a1ad7c4eaaae47dfe669020de94/api/core/tools/mcp_tool/provider.py#L77-L78
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/langgenius/dify/4b89972f552c7a1ad7c4eaaae47dfe669020de94/api/core/tools/mcp_tool/provider.py
- **版**: commit 4b89972f552c7a1ad7c4eaaae47dfe669020de94
- **書いてある場所**: api/core/tools/mcp_tool/provider.py L77-78
- **原文**:

```
                    label=I18nObject(
                        en_US=remote_mcp_tool.title or remote_mcp_tool.name,
```

- **日本語**: 表示ラベルには、サーバーの Tool.title（無ければ name）を使う。
- **どう使っているか**: Dify は MCP ツールを自前の ToolEntity に変換するとき、トップレベルの title だけを使い、annotations（annotations.title や各ヒント）は写さない。
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、77-78 行（取得 2026-10-02T22:11:34Z、sha256 6f6b8f7a7d0a…）
- **補足**: 変換箇所（L63-93）が使う上流の項目は name / title / description / inputSchema / outputSchema だけ。RemoteMCPTool は core.mcp.types.Tool で annotations フィールドを持つ（types.py L848）が、変換では読まれない。commit 4b89972 の api/ と web/ を grep すると readOnlyHint / destructiveHint / ToolAnnotations を含むのは api/core/mcp/types.py だけ。Dify の MCP 文書にも注釈の記述はない（checked_no_mention）。types.py の docstring（L212 付近）は annotations.title を name より優先するよう書くが、Dify はトップレベルの title だけを使う。 型が annotations を受け取っていること（ただし変換で捨てる）を補い、grep の範囲を手元の clone で確かめた結果に直した。

### LangGenius — Dify — 同梱の MCP 型定義

<a id="g-g2-gateways-platforms-31"></a>
#### G2GP-31 LangGenius — Dify — 同梱の MCP 型定義

- **資料**: api/core/mcp/types.py — ToolAnnotations（クライアントのソースコード）
- **URL**: https://github.com/langgenius/dify/blob/4b89972f552c7a1ad7c4eaaae47dfe669020de94/api/core/mcp/types.py#L796-L797
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/langgenius/dify/4b89972f552c7a1ad7c4eaaae47dfe669020de94/api/core/mcp/types.py
- **版**: commit 4b89972f552c7a1ad7c4eaaae47dfe669020de94
- **書いてある場所**: api/core/mcp/types.py L796-797
- **原文**:

```
    Clients should never make tool use decisions based on ToolAnnotations
    received from untrusted servers.
```

- **日本語**: クライアントは、信頼できないサーバーから受け取った ToolAnnotations を根拠にツール使用を決めてはならない。
- **どう使っているか**: Dify は仕様の型（readOnlyHint など）と注意書きを写して持っているが、#30 のとおりツール実行・承認には使っていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、796-797 行（# """DEPRECATED: Content is deprecated, you should use ContentBlock directly."""）（取得 2026-10-02T22:11:35Z、sha256 e14e78bf6acd…）
- **補足**: 仕様の docstring をそのまま写したもの。Dify 独自の方針ではない。

### Arcade.dev — Arcade MCP server framework（arcade_mcp_server）— ToolMetadata

<a id="g-g2-gateways-platforms-32"></a>
#### G2GP-32 Arcade.dev — Arcade MCP server framework（arcade_mcp_server）— ToolMetadata

- **資料**: Add metadata to your tools（SDK の文書）
- **URL**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata
- **書いてある見出しへ直接**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata#what-is-toolmetadata
- **版**: 2026-10-02 取得
- **書いてある場所**: Add metadata to your tools > What is ToolMetadata? (#what-is-toolmetadata)
- **原文**:

> These are projected to MCP annotations ( readOnlyHint , destructiveHint , etc.) for MCP clients.

- **日本語**: （Behavior 軸の）操作（CRUD）と安全フラグは、MCP クライアント向けに MCP 注釈（readOnlyHint, destructiveHint など）へ写される。
- **どう使っているか**: 作者は Behavior（operations と read_only / destructive / idempotent / open_world）を書き、それが MCP 注釈に投影される。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Add metadata to your tools > What is ToolMetadata?」（取得 2026-10-02T22:11:25Z、sha256 5eb252a9f0f7…）
- **補足**: 対応表は read_only→readOnlyHint, destructive→destructiveHint, idempotent→idempotentHint, open_world→openWorldHint。フラグの既定値は read_only=False, destructive=True, idempotent=False, open_world=True（仕様の既定と同じ）。

### Arcade.dev — Arcade — ToolMetadata の利用者（ポリシーエンジン）

<a id="g-g2-gateways-platforms-33"></a>
#### G2GP-33 Arcade.dev — Arcade — ToolMetadata の利用者（ポリシーエンジン）

- **資料**: Add metadata to your tools（SDK の文書）
- **URL**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata
- **書いてある見出しへ直接**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata#what-is-toolmetadata
- **版**: 2026-10-02 取得
- **書いてある場所**: Add metadata to your tools > What is ToolMetadata? (#what-is-toolmetadata)
- **原文**:

> Behavior enables rules like “require human approval for DELETE operations” or “only allow read-only tools in this gateway.”

- **日本語**: Behavior は「DELETE 操作には人の承認を求める」や「このゲートウェイでは読み取り専用のツールだけ許す」のような規則を可能にする。
- **どう使っているか**: ToolMetadata の Behavior を、ポリシーエンジンの規則（承認・読み取り専用ゲートウェイ）の入力として想定している。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を求める・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Add metadata to your tools > What is ToolMetadata?」（取得 2026-10-02T22:11:25Z、sha256 5eb252a9f0f7…）
- **補足**: メタデータを使う 3 つの仕組み（Tool selection / Policy engines / MCP clients）の 2 つ目。Arcade のゲートウェイが実際にこの規則を実装しているかは、このページだけでは分からない（不明）。

### Arcade.dev — Arcade — ToolMetadata の矛盾検査

<a id="g-g2-gateways-platforms-34"></a>
#### G2GP-34 Arcade.dev — Arcade — ToolMetadata の矛盾検査

- **資料**: Add metadata to your tools — Validation（SDK の文書）
- **URL**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata
- **書いてある見出しへ直接**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata#validation
- **版**: 2026-10-02 取得
- **書いてある場所**: Add metadata to your tools > Validation (#validation)
- **原文**:

> By default, ToolMetadata validates for logical contradictions when your server starts.

- **日本語**: 既定では、ToolMetadata はサーバー起動時に論理的な矛盾を検査する。
- **どう使っているか**: 宣言どうしの矛盾（操作の種類と read_only / destructive / open_world の組み合わせ）を起動時に例外にする。コードとの照合ではなく宣言内の整合検査。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Add metadata to your tools > Validation」（取得 2026-10-02T22:11:25Z、sha256 5eb252a9f0f7…）
- **補足**: 検査項目：変更系の操作 + read_only=True、OPAQUE 操作 + read_only=True、DELETE 操作 + destructive=False、ServiceDomain あり + open_world=False。strict=False で無効にできる。AuthGap の D1/D2/D3 と同じ方向の矛盾を『宣言の中だけで』見ている点が関係する。

<a id="g-g2-gateways-platforms-35"></a>
#### G2GP-35 Arcade.dev — Arcade — ToolMetadata の矛盾検査

- **資料**: Add metadata to your tools — Validation（表）（SDK の文書）
- **URL**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata
- **書いてある見出しへ直接**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata#validation
- **版**: 2026-10-02 取得
- **書いてある場所**: Add metadata to your tools > Validation (#validation)
- **原文**:

> Can’t be read-only if it creates, updates, or deletes

- **日本語**: （変更系の操作 + read_only=True は矛盾：）作成・更新・削除をするなら読み取り専用にはなれない。
- **どう使っているか**: operations に CREATE/UPDATE/DELETE を持つツールが read_only=True（→ readOnlyHint:true）を宣言すると起動時に弾く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Add metadata to your tools > Validation」（取得 2026-10-02T22:11:25Z、sha256 5eb252a9f0f7…）
- **補足**: 表の 1 行目の『Why it’s a contradiction』欄。

### Arcade.dev — Arcade — ToolMetadata の MCP 揃えフラグ

<a id="g-g2-gateways-platforms-36"></a>
#### G2GP-36 Arcade.dev — Arcade — ToolMetadata の MCP 揃えフラグ

- **資料**: Add metadata to your tools — Behavior > MCP-aligned flags（SDK の文書）
- **URL**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata
- **書いてある見出しへ直接**: https://docs.arcade.dev/en/build/create-tools/tool-basics/add-tool-metadata#mcp-aligned-flags
- **版**: 2026-10-02 取得
- **書いてある場所**: Add metadata to your tools > Behavior > MCP-aligned flags (#mcp-aligned-flags)
- **原文**:

> These four booleans are projected directly to MCP tool annotations. Always specify all four for production metadata.

- **日本語**: この 4 つの真偽値はそのまま MCP ツール注釈に投影される。本番用のメタデータでは 4 つとも必ず指定すること。
- **どう使っているか**: 作者に 4 つのヒントを全部明示するよう求める。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Add metadata to your tools > Behavior > MCP-aligned flags」（取得 2026-10-02T22:11:25Z、sha256 5eb252a9f0f7…）

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy（mcpproxy-go）— DeriveCallWith

<a id="g-g2-gateways-platforms-37"></a>
#### G2GP-37 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy（mcpproxy-go）— DeriveCallWith

- **資料**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing（2026-03-13）（公式ブログ）
- **URL**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/
- **書いてある見出しへ直接**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/#the-derivecallwith-system
- **版**: 2026-03-13 の記事
- **書いてある場所**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > How MCPProxy Handles Annotations > The DeriveCallWith System (#the-derivecallwith-system)
- **原文**:

> A tool with no annotations gets call_tool_write (not read-only, so it might modify things, but not explicitly destructive).

- **日本語**: 注釈の無いツールは call_tool_write になる（読み取り専用ではないので変更するかもしれないが、明示的に destructive ではない）。
- **どう使っているか**: 注釈から呼び出しの種類（call_tool_read / write / destructive）を決め、エージェントトークンの権限に結びつける。記事では欠落時は write としている。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > How MCPProxy Handles Annotations > The DeriveCallWith System」（取得 2026-10-02T22:11:36Z、sha256 ce8591fd0025…）
- **補足**: 記事の記述は現在のコードと食い違う：commit 7b96899 の DeriveCallWith は注釈なしを call_tool_read（safe default）にする（#40, #41）。direct モードの権限判定（requiredPermissionForDirectTool, #42）と code execution の tierForAnnotations も同じ関数を使うので、現行コードでは、スコープ付きエージェントトークンを使うとき、注釈の無いツールは read 権限だけのトークンでも呼べると読める。記事の『Annotation State』表でも readOnlyHint: false (or absent) → call_tool_write と書いている。現行の挙動の根拠はコード。記事はプロジェクト自身のサイト（mcpproxy.app）のもの。 権限判定が効くのはスコープ付きエージェントトークンの場合であることを補った。

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — intent validation

<a id="g-g2-gateways-platforms-38"></a>
#### G2GP-38 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — intent validation

- **資料**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing（公式ブログ）
- **URL**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/
- **書いてある見出しへ直接**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/#intent-validation
- **版**: 2026-03-13 の記事
- **書いてある場所**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > How MCPProxy Handles Annotations > Intent Validation (#intent-validation)
- **原文**:

> In strict mode, a mismatch — calling a destructive tool via call_tool_read , for example — is blocked.

- **日本語**: strict モードでは、食い違い（たとえば destructive なツールを call_tool_read で呼ぶこと）は遮断される。
- **どう使っているか**: エージェントが選んだ呼び出し種類とサーバーの注釈を照合し、strict モードなら不一致を遮断する。
- **条件**: strict モードのとき
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言を検査する
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > How MCPProxy Handles Annotations > Intent Validation」（取得 2026-10-02T22:11:36Z、sha256 ce8591fd0025…）
- **補足**: コード（internal/contracts/intent.go ValidateAgainstServerAnnotations, L163-198）では、call_tool_destructive で呼べば検査しない。annotations が nil なら検査しない（return nil）。検査するのは destructiveHint:true のツールを read / write で呼んだ場合だけで、strict でなければエラーを返さない（呼び出し側が警告を出すとコメントにある）。write で read-only ツールを呼ぶのは許可。 notes にコードの行範囲と destructive で呼んだときは検査しないことを補った。

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — quarantine（ツール変更の検出）

<a id="g-g2-gateways-platforms-39"></a>
#### G2GP-39 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — quarantine（ツール変更の検出）

- **資料**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing — Current Gaps（公式ブログ）
- **URL**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/
- **書いてある見出しへ直接**: https://mcpproxy.app/blog/2026-03-13-mcpproxy-tool-annotations-routing/#current-gaps-and-planned-work
- **版**: 2026-03-13 の記事
- **書いてある場所**: Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > Current Gaps and Planned Work (#current-gaps-and-planned-work)
- **原文**:

> When MCPProxy quarantines a new server’s tools for review, the hash that detects schema changes does not include annotation values.

- **日本語**: MCPProxy が新しいサーバーのツールを確認のために隔離するとき、スキーマの変化を検出するハッシュには注釈の値が含まれない。
- **どう使っているか**: ツール定義の変化検出（rug-pull 対策）で注釈を見ていない、と自ら限界として書いている。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Deep Dive: How MCPProxy Uses MCP Tool Annotations for Smarter Routing > Current Gaps and Planned Work」（取得 2026-10-02T22:11:36Z、sha256 ce8591fd0025…）
- **補足**: 記事は続けて「A server could change its tools from read-only to destructive without triggering re-quarantine. This is a known gap that will be addressed.」と書く。現行コードで直ったかは確かめていない（不明）。同じ節で idempotentHint と openWorldHint は『取得するが経路決定に使わない』とも書く。

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — DeriveCallWith（現行コード）

<a id="g-g2-gateways-platforms-40"></a>
#### G2GP-40 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — DeriveCallWith（現行コード）

- **資料**: internal/contracts/intent.go（サーバのソースコード）
- **URL**: https://github.com/smart-mcp-proxy/mcpproxy-go/blob/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/intent.go#L207
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/smart-mcp-proxy/mcpproxy-go/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/intent.go
- **版**: commit 7b96899f9a6bf924661a6fb36abbad2c75a75c02
- **書いてある場所**: internal/contracts/intent.go L207
- **原文**:

> //  4. No hints / nil annotations → call_tool_read (safe default)

- **日本語**: 4. ヒントが無い / annotations が nil → call_tool_read（安全な既定）
- **どう使っているか**: 注釈の無いツールの呼び出し種類を read にする。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、207 行（取得 2026-10-02T22:11:37Z、sha256 455415843569…）
- **補足**: 優先順は destructiveHint=true → destructive、readOnlyHint=false → write、readOnlyHint=true → read、それ以外 → read。ブログ（#37）の『欠落時は write』と食い違う。

<a id="g-g2-gateways-platforms-41"></a>
#### G2GP-41 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — DeriveCallWith（現行コード）

- **資料**: internal/contracts/intent.go（サーバのソースコード）
- **URL**: https://github.com/smart-mcp-proxy/mcpproxy-go/blob/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/intent.go#L223-L224
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/smart-mcp-proxy/mcpproxy-go/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/intent.go
- **版**: commit 7b96899f9a6bf924661a6fb36abbad2c75a75c02
- **書いてある場所**: internal/contracts/intent.go L223-224
- **原文**:

> 	// No annotations, or annotations without any hints set:
> 	// Default to read as the safest option. Most tools are read-only

- **日本語**: 注釈が無いか、どのヒントも設定されていないとき：最も安全な選択として read を既定にする。ほとんどのツールは読み取り専用だから。
- **どう使っているか**: 『ほとんどのツールは読み取り専用』という経験則で、欠落を read に倒している。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、223-224 行（取得 2026-10-02T22:11:37Z、sha256 455415843569…）
- **補足**: 続く行は「(search, query, list, get, fetch, check, view, find operations). LLMs should analyze tool descriptions to select write/destructive when appropriate.」。

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — direct モードの権限判定

<a id="g-g2-gateways-platforms-42"></a>
#### G2GP-42 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — direct モードの権限判定

- **資料**: internal/server/mcp_direct_scope.go（サーバのソースコード）
- **URL**: https://github.com/smart-mcp-proxy/mcpproxy-go/blob/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/server/mcp_direct_scope.go#L340-L341
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/smart-mcp-proxy/mcpproxy-go/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/server/mcp_direct_scope.go
- **版**: commit 7b96899f9a6bf924661a6fb36abbad2c75a75c02
- **書いてある場所**: internal/server/mcp_direct_scope.go L340-341
- **原文**:

```
func requiredPermissionForDirectTool(annotations *config.ToolAnnotations) string {
	return contracts.ToolVariantToOperationType[contracts.DeriveCallWith(annotations)]
```

- **日本語**: direct ツールが必要とするエージェントトークンの権限を、注釈から DeriveCallWith で求める。
- **どう使っているか**: エージェントトークンの権限（read / write / destructive）の判定と、ツール一覧の絞り込みに注釈を使う。注釈なし → read 権限で足りる。
- **条件**: スコープ付きエージェントトークンを使うとき、または有効なプロファイルがあるとき（filterDirectModeToolsForAuth のコメント）
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、340-341 行（取得 2026-10-02T22:13:00Z、sha256 d46daebab9ee…）
- **補足**: 直前のコメント（L334-339）は『call 時の認可と同じ写像を使うので、発見時の絞り込みと実行時の強制がずれない』。code execution 側（mcp_code_execution.go tierForAnnotations）も同じ写像を使い、ツールが見つからない（found=false）ときだけ destructive に倒す。 絞り込み（filterDirectModeToolsForAuth）が働くのは、スコープ付きエージェントトークンのときと、プロファイルが有効なときだけ（L344-345 のコメント）。 権限判定が働く条件（スコープ付きトークン / プロファイル）を conditions に補った。

### MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — AnnotationTier（プロファイルの tier）

<a id="g-g2-gateways-platforms-43"></a>
#### G2GP-43 MCPProxy（smart-mcp-proxy、OSS） — MCPProxy — AnnotationTier（プロファイルの tier）

- **資料**: internal/contracts/tier.go（サーバのソースコード）
- **URL**: https://github.com/smart-mcp-proxy/mcpproxy-go/blob/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/tier.go#L38-L39
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/smart-mcp-proxy/mcpproxy-go/7b96899f9a6bf924661a6fb36abbad2c75a75c02/internal/contracts/tier.go
- **版**: commit 7b96899f9a6bf924661a6fb36abbad2c75a75c02
- **書いてある場所**: internal/contracts/tier.go L38-39
- **原文**:

> // picking which call_tool_* variant to use — AnnotationTier never guesses:
> // an unannotated tool is TierUnannotated, not TierRead.

- **日本語**: （DeriveCallWith は）どの call_tool_* を使うか選ぶとき…AnnotationTier は推測しない：注釈の無いツールは TierUnannotated であって TierRead ではない。
- **どう使っているか**: 同じ製品の中に、欠落を read とする写像（DeriveCallWith）と、欠落を『未注釈』として別に扱う写像（AnnotationTier）が並存している。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、38-39 行（取得 2026-10-02T22:11:40Z、sha256 019e7856917c…）
- **補足**: 引用はコメントの一部（L38-39）。直前の行で『This is deliberately distinct from DeriveCallWith (Spec 018 call-variant routing), which defaults an unannotated tool to "read" for safety』と明記。profile/policy.go の IntrinsicTier は、ツールが見つからないときだけ TierDestructive に倒す。TierUnannotated が最終的に許可・拒否のどちらになるかはプロファイルの設定次第（不明）。

### Workato — Workato Enterprise MCP（MCP Server 作成 UX）

<a id="g-g2-gateways-platforms-44"></a>
#### G2GP-44 Workato — Workato Enterprise MCP（MCP Server 作成 UX）

- **資料**: Product Scoop - July 2026（リリースノート）
- **URL**: https://www.workato.com/product-hub/product-scoop-july-2026/
- **版**: 2026-07 の製品アップデート（ページの日付表示は Aug 2026）
- **書いてある場所**: Product Scoop - July 2026 > MCP Gateway > Tool Annotation Support: Clearer Titles and Behavior Hints for MCP Tools
- **原文**:

> Let AI agents use these hints to decide how to act, for example proceeding without confirmation on read-only tools, or pausing for approval on tools marked destructive.

- **日本語**: AI エージェントはこのヒントで振る舞いを決められる。たとえば read-only のツールは確認なしで進め、destructive と印の付いたツールでは承認のために止まる。
- **どう使っているか**: Workato の MCP サーバー作成画面で注釈を宣言できるようになり、エージェントがそれを使って確認の省略や承認待ちを決められる、と書く（決めるのはエージェント・クライアント側で、Workato が強制するとは書いていない）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 作者への書き方の案内・確認を求める・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Product Scoop - July 2026 > MCP Gateway > Tool Annotation Support: Clearer Titles and Behavior Hints for MCP Tools」（取得 2026-10-02T22:11:40Z、sha256 150cc8a910bb…）
- **補足**: Workato 自身のゲートウェイが注釈で承認を強制するとは書いていない。同じ項に『Behavior annotations also give security and compliance reviewers ... a standard way to assess how a tool behaves before it's approved or invoked』。 ページの日付と、判断する主体がエージェント側であることを明記した。

<a id="g-g2-gateways-platforms-45"></a>
#### G2GP-45 Workato — Workato Enterprise MCP（MCP Server 作成 UX）

- **資料**: Product Scoop - July 2026（リリースノート）
- **URL**: https://www.workato.com/product-hub/product-scoop-july-2026/
- **版**: 2026-07
- **書いてある場所**: Product Scoop - July 2026 > MCP Gateway > Tool Annotation Support: Clearer Titles and Behavior Hints for MCP Tools
- **原文**:

> Declare whether a tool performs destructive updates (destructiveHint), only reads data (readonlyHint), is safe to call repeatedly with the same arguments (idempotentHint), or interacts with an open-world domain like the public web (openWorldHint).

- **日本語**: ツールが destructive な更新をするか（destructiveHint）、データを読むだけか（readonlyHint）、同じ引数で何度呼んでも安全か（idempotentHint）、公開 Web のような開いた領域とやりとりするか（openWorldHint）を宣言する。
- **どう使っているか**: Workato の MCP サーバー作成 UI に 4 つのヒント欄と、name と別の表示用 Tool Title 欄が加わった。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Product Scoop - July 2026 > MCP Gateway > Tool Annotation Support: Clearer Titles and Behavior Hints for MCP Tools」（取得 2026-10-02T22:11:40Z、sha256 150cc8a910bb…）
- **補足**: 原文の綴りは readonlyHint（小文字の o）。表示用 title を name と分けたのは『表示名を変えるとクライアントの呼び出しが壊れる』問題への対処。 「Tool Title」がトップレベルの Tool.title として出るのか annotations.title として出るのかは書かれていない（不明）。tools/list で readOnlyHint と正しい綴りで出るかも確かめていない（不明）。 title の出る位置と readonlyHint の綴りの実際は不明と補った。

### Composio — Composio Tool Router セッション — 振る舞いタグ

<a id="g-g2-gateways-platforms-46"></a>
#### G2GP-46 Composio — Composio Tool Router セッション — 振る舞いタグ

- **資料**: Configuring Sessions — Filtering tools by tags（公式の文書）
- **URL**: https://docs.composio.dev/docs/configuring-sessions
- **書いてある見出しへ直接**: https://docs.composio.dev/docs/configuring-sessions#filtering-tools-by-tags
- **版**: 2026-10-02 取得
- **書いてある場所**: Configuring Sessions > Filtering tools by tags (#filtering-tools-by-tags)
- **原文**:

> `readOnlyHint` comes from the server's annotations; every other tool is classified into `createHint`, `updateHint` or `destructiveHint` when the toolkit is synced.

- **日本語**: （MCP を裏に持つ toolkit では）readOnlyHint はサーバーの注釈から取る。それ以外のツールは、toolkit の同期のときに createHint / updateHint / destructiveHint のどれかに分類される。
- **どう使っているか**: MCP 由来のツールでは readOnlyHint は上流の注釈から取り、それ以外のツールは toolkit の同期のときに Composio が createHint / updateHint / destructiveHint に分類する。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・その他
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Configuring Sessions > Filtering tools by tags」（取得 2026-10-02T22:11:25Z、sha256 2c43afe5ed0e…）
- **補足**: Composio 独自のタグ語彙は readOnlyHint / createHint / updateHint / destructiveHint の 4 つ（createHint / updateHint は MCP 仕様に無い）。Composio 自身のツールにも同じ名前のタグが付くが、それは MCP サーバーの宣言ではなく Composio の分類。idempotentHint / openWorldHint も受け付けるが『一部のツールしか持たないのでアクセス制御には 4 つを使え』と書く。分類の方法（モデルか規則か）と、分類で上流の destructiveHint を使うかは書かれていない（不明）。同期前の toolkit は「may carry only the server's annotations」とある。 「destructiveHint は上流の値ではなく Composio の分類」は言い過ぎ（上流値を分類に使うかは書かれていない）なので弱めた。

<a id="g-g2-gateways-platforms-47"></a>
#### G2GP-47 Composio — Composio Tool Router セッション — 振る舞いタグ

- **資料**: Configuring Sessions — Filtering tools by tags（公式の文書）
- **URL**: https://docs.composio.dev/docs/configuring-sessions
- **書いてある見出しへ直接**: https://docs.composio.dev/docs/configuring-sessions#filtering-tools-by-tags
- **版**: 2026-10-02 取得
- **書いてある場所**: Configuring Sessions > Filtering tools by tags (#filtering-tools-by-tags)
- **原文**:

> an `enable` filter hides any tool without a matching tag.

- **日本語**: enable フィルターは、一致するタグを持たないツールを隠す。
- **どう使っているか**: タグの欠けたツールは enable 型のフィルターでは見えなくなる（fail-closed）。disable 型（例：destructiveHint を無効）でタグが欠けたツールがどうなるかは書かれていない（残ると推測できるが未確認）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Configuring Sessions > Filtering tools by tags」（取得 2026-10-02T22:11:25Z、sha256 2c43afe5ed0e…）
- **補足**: 直前の文は「A toolkit not synced since classification was added may carry only the server's annotations」で、引用はこの「同期前の toolkit」の文脈の中にある。 disable 型の扱いは推測であることを明確にした。

<a id="g-g2-gateways-platforms-48"></a>
#### G2GP-48 Composio — Composio Tool Router セッション — 振る舞いタグ

- **資料**: Configuring Sessions — Filtering tools by tags（公式の文書）
- **URL**: https://docs.composio.dev/docs/configuring-sessions
- **書いてある見出しへ直接**: https://docs.composio.dev/docs/configuring-sessions#filtering-tools-by-tags
- **版**: 2026-10-02 取得
- **書いてある場所**: Configuring Sessions > Filtering tools by tags (#filtering-tools-by-tags)
- **原文**:

> Tools carry behavior tags that you can filter on. Every tool carries at least one of these four:

- **日本語**: ツールは絞り込みに使える振る舞いタグを持つ。どのツールも次の 4 つの少なくとも 1 つを持つ。
- **どう使っているか**: セッション作成時に tags=["readOnlyHint"] や {enable, disable: ["destructiveHint"]} でツールを絞り込む。toolkit ごとの上書きもできる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Configuring Sessions > Filtering tools by tags」（取得 2026-10-02T22:11:25Z、sha256 2c43afe5ed0e…）
- **補足**: 例：全体は readOnlyHint のみ、GitHub は destructiveHint 以外すべて、Gmail は readOnlyHint のみ。「Every tool carries at least one of these four」は、同じ節の「同期前の toolkit はサーバーの注釈だけを持つことがある」（#47）と緩く食い違う。タグは Composio の語彙で、Composio 自身のツールについては MCP サーバーの宣言ではない（#46）。 「どのツールも 4 つのどれかを持つ」と同期前の例外が食い違う点と、タグが MCP の宣言とは限らない点を補った。

### TrueFoundry / TrueForge — TrueForge — Code Mode の破壊的ツール拒否

<a id="g-g2-gateways-platforms-49"></a>
#### G2GP-49 TrueFoundry / TrueForge — TrueForge — Code Mode の破壊的ツール拒否

- **資料**: Issue #318: Code Mode destructive-tool gate fails open on unannotated tools (and errors on annotated ones with mcp >=2.0)（issue / PR / 提案の下書き）
- **URL**: https://github.com/truefoundry/trueforge/issues/318
- **版**: 不明（WebSearch 結果の題名のみ）
- **書いてある場所**: issue 題名
- **原文**:

> Code Mode destructive-tool gate fails open on unannotated tools (and errors on annotated ones with mcp >=2.0)

- **日本語**: Code Mode の破壊的ツールの門は、注釈の無いツールで fail-open になる（mcp >= 2.0 では注釈付きツールでエラーになる）。
- **どう使っているか**: 注釈の欠落で門が開く問題が issue として報告されている。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [未確認] github.com の issue ページは取得不可。WebSearch（2026-10-02）の結果題名で見ただけ。
- **補足**: 現行コード（#13, commit 5b7abb6）では annotations が None なら _is_destructive は False のままで、題名の前半の挙動は残っていると読める。後半（mcp >= 2.0 で注釈付きツールがエラー）は、現行コードが getattr で snake_case（destructive_hint）を先に見て camelCase に落ちる形になっており、対処済みの可能性があるが確かめていない（不明）。タスク文にある PR #832 は WebSearch で見つからず未確認。docs（#09, #10）と CHANGELOG（#15）は承認の選択子について同じ欠落時の挙動を書いている。GitHub MCP ツールでの読み取りもこの session では許可されていなかった。 題名の後半について、現行コードの getattr の形から対処済みの可能性を補った（未確認のまま）。

### Greenhat Security — GreenGateway（MCP ゲートウェイ）

<a id="g-g2-gateways-platforms-51"></a>
#### G2GP-51 Greenhat Security — GreenGateway（MCP ゲートウェイ）

- **資料**: Issue #368: [Feature]: Pass MCP tool annotations (readOnlyHint etc.) through the gateway-owned /mcp endpoint（issue / PR / 提案の下書き）
- **URL**: https://github.com/Greenhat-Security/GreenGateway/issues/368
- **版**: 不明
- **書いてある場所**: issue 題名
- **原文**:

> Pass MCP tool annotations (readOnlyHint etc.) through the gateway-owned /mcp endpoint

- **日本語**: ゲートウェイ自身の /mcp エンドポイントでも MCP ツール注釈（readOnlyHint など）を素通しにしてほしい。
- **どう使っているか**: ゲートウェイが注釈を落としている（name / description / inputSchema だけを出す）という報告。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 使わない・読まない・そのまま渡す・見せる
- **確かさ**: [未確認] github.com の issue ページは取得不可。WebSearch（2026-10-02）の結果題名と要約で見ただけ。
- **補足**: WebSearch の要約では『gateway-owned /mcp の tools は name, description, inputSchema だけで annotations が全種で落ちる』『注釈を承認の合図に使うホスト（readOnlyHint:true を即実行し他を承認待ちにする）で問題になる』とあるが、モデル要約なので内容は未確認。 github.com の issue は検証者も読めなかった（GitHub MCP ツールもこの repo を許可していない）。未確認のまま。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（npm。tools/list を読む静的リンター）— dev.to の紹介記事

<a id="g-g2-verifiers-linters-01"></a>
#### G2VL-01 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（npm。tools/list を読む静的リンター）— dev.to の紹介記事

- **資料**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers)（公式ブログ）
- **URL**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3
- **書いてある見出しへ直接**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3#why-the-drift-matters
- **版**: 2026-07-26 公開（dev.to API の published_at）。canonical は formael.com/blog/mcp-ecosystem-audit
- **書いてある場所**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > Why the drift matters
- **原文**:

> It reads what a server advertises over tools/list, works out what each tool most likely does from the name, description, and input schema, and reports where that disagrees with what the tool declares. It never calls a tool.

- **日本語**: サーバーが tools/list で公開する内容を読み、名前・説明・入力スキーマから各ツールが何をしそうかを推定し、それが宣言と食い違うところを報告する。ツールは一度も呼ばない。
- **どう使っているか**: 照合の種類は (a) 名前・説明・入力スキーマからの発見的推定。ソースコードは読まず、ツールも呼ばない（tools/list を取るために stdio サーバーを起動するか HTTP サーバーに接続はする。--capture で保存した一覧を --manifest でオフライン再検査もできる）。記事が例に出す宣言は readOnlyHint / destructiveHint / openWorldHint（D1・D2・D3 に当たる）で、それを tools/list 上の他の項目から推定した効果と比べる。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > Why the drift matters」（取得 2026-10-02T22:11:23Z、sha256 a9c6db0f16ab…）
- **補足**: 開発元自身による紹介（一次資料だが自社製品の宣伝）。dev.to の本文は API（/api/articles/formael/...）でも取得して読んだ。D4 idempotentHint は記事の 3 つの hint に入っていない（repo の README は 4 つ全部を挙げるが、比較の側面は destructiveness / external reach / reversibility の 3 つ。G2_verifiers_linters の repo 項目を参照）。 doc_type を third_party から official_blog に直した。dev.to の記事は Formael 自身の投稿で、本文に『Originally published at formael.com』とある（開発元のブログの転載）。 usage_ja の『実行もしない』を正確にした（ツールは呼ばないが、tools/list を取るためにサーバーは起動・接続する。記事の Ways to point it at a server の節）。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（導出は宣言を見ない）

<a id="g-g2-verifiers-linters-02"></a>
#### G2VL-02 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（導出は宣言を見ない）

- **資料**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers)（公式ブログ）
- **URL**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3
- **書いてある見出しへ直接**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3#how-it-decides
- **版**: 2026-07-26 公開
- **書いてある場所**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > How it decides
- **原文**:

> It doesn't look at your annotations while deriving. The derivation step reads only the name, description, and input schema.

- **日本語**: 導出の間は注釈を見ない。導出の段階が読むのは名前・説明・入力スキーマだけ。
- **どう使っているか**: 効果の推定に宣言を入力として使わない（宣言は監査される側）。宣言を書き換えて判定を有利にすることはできない、という設計。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > How it decides」（取得 2026-10-02T22:11:23Z、sha256 a9c6db0f16ab…）
- **補足**: 同じ節の『Where signals conflict or are missing, the result resolves toward concern with lowered confidence.』も verify_quote.py で exact（how-it-decides）。記事は uncertain を「失敗にしない結果」として扱うとも書く。 doc_type を third_party から official_blog に直した。dev.to の記事は Formael 自身の投稿で、本文に『Originally published at formael.com』とある（開発元のブログの転載）。 notes の補足引用を検証済み（exact）に更新した。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（31 サーバーの結果。数値は未検証）

<a id="g-g2-verifiers-linters-03"></a>
#### G2VL-03 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — dev.to の紹介記事（31 サーバーの結果。数値は未検証）

- **資料**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers)（公式ブログ）
- **URL**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3
- **書いてある見出しへ直接**: https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3#why-the-drift-matters
- **版**: 2026-07-26 公開
- **書いてある場所**: Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > Why the drift matters
- **原文**:

> We pointed it at 541 tools across 31 widely used servers, including official ones from Stripe, GitHub, Microsoft, Google, MongoDB, and PayPal. Eleven came back completely clean. Four carry a label that denies something the tool's own schema says it can do.

- **日本語**: 31 の広く使われるサーバーの 541 ツールにかけた。11 はまったく問題なし。4 つは、ツール自身のスキーマができると言っていることを否定する宣言を持っていた。
- **どう使っているか**: 宣言とスキーマ等の不一致を野外のサーバーで数えた結果（開発元の主張）。分母は『31 サーバー / 541 ツール』、判定はソースではなく tools/list の内容に対するもの。
- **条件**: 数値（31 / 541 / 11 / 4）は開発元の自己申告で、本調査では検証していない（verified_by_me = none）。手順と分母の詳細は formael.com の記事（同カテゴリの別項目）に書かれている。
- **扱う宣言**: readOnlyHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Are your MCP server's safety labels honest? A one-command check (and what it found on 31 popular servers) > Why the drift matters」（取得 2026-10-02T22:11:23Z、sha256 a9c6db0f16ab…）
- **補足**: 引用が記事中にあることだけを確認した。数値の正しさは未検証。 doc_type を third_party から official_blog に直した。dev.to の記事は Formael 自身の投稿で、本文に『Originally published at formael.com』とある（開発元のブログの転載）。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（手続き）

<a id="g-g2-verifiers-linters-04"></a>
#### G2VL-04 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（手続き）

- **資料**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers.（公式ブログ）
- **URL**: https://formael.com/blog/mcp-ecosystem-audit
- **書いてある見出しへ直接**: https://formael.com/blog/mcp-ecosystem-audit#what-we-checked
- **版**: 2026-07-19 付。actlint 0.2.0・verified 2026-07-15 と表に記載
- **書いてある場所**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > What we checked
- **原文**:

> We ran actlint against each one — including the servers that need an API key or an auth header to start — and read every finding by hand against the server's own tool declarations before writing anything up.

- **日本語**: それぞれのサーバーに actlint をかけ（API キーや認証ヘッダが要るものも含む）、書く前にすべての指摘を、サーバー自身のツール宣言と手で照らし合わせた。
- **どう使っているか**: 記事が書く手検証の基準は『サーバー自身のツール宣言』（tools/list の名前・説明・スキーマ・注釈）で、ソースコードや実行結果と照らしたとは書いていない。判定（High）も「ツール自身の定義（スキーマ）ができると言っていることを宣言が否定する」形で述べられ、AuthGap の M（実装の効果）とは比べていない。ただし Cloudflare の search について「現在の設計ではサンドボックスが API 仕様のメモリ上の写しにしか触れない」と、記述子の外の知識にも触れている（その知識の出所は書かれていない）。
- **条件**: 対象は Stripe・PayPal・GitHub・Microsoft・Google・MongoDB・Sentry・Shopify・HubSpot・Supabase・Notion・Firecrawl・Brave の公式サーバー、参照サーバー、いくつかのコミュニティ製、Linear・Cloudflare・DeepWiki・Hugging Face・Microsoft Learn のホスト型（記事の記載）。選び方の基準（無作為抽出か等）は書かれていない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > What we checked」（取得 2026-10-02T22:11:25Z、sha256 9763a88ab0fe…）
- **補足**: 数値（31 サーバー / 541 ツール / Clean 11 / High 4）は未検証。記事の表では High = 4（firecrawl-mcp, @stripe/mcp, Cloudflare, Linear）。 usage_ja の『ソースコードや実行結果ではない』は記事に無い断定だったので、「記事はソースや実行と照らしたとは書いていない」に弱め、Cloudflare の段落で記述子外の知識に触れている点を補った。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（判定できないツールの扱い）

<a id="g-g2-verifiers-linters-05"></a>
#### G2VL-05 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（判定できないツールの扱い）

- **資料**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers.（公式ブログ）
- **URL**: https://formael.com/blog/mcp-ecosystem-audit
- **書いてある見出しへ直接**: https://formael.com/blog/mcp-ecosystem-audit#what-we-checked
- **版**: 2026-07-19 付
- **書いてある場所**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > What we checked
- **原文**:

> when actlint finds no risk signal it recognizes in a tool, it reports that tool as not assessable rather than silently passing it.

- **日本語**: actlint が知っている危険の手がかりをツールに見つけられないときは、黙って合格にせず『判定できない』と報告する。
- **どう使っているか**: 手がかりが無いツールは『判定不能』で、清浄とは数えない（記事は『clean の評価は判定できたツールがすべて宣言と一致した意味で、全ツールが判定できたわけではない』と続ける）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > What we checked」（取得 2026-10-02T22:11:25Z、sha256 9763a88ab0fe…）
- **補足**: 判定不能のツール数は記事の表に出ていない（分母の内訳は不明）。 usage から defaults_when_missing を外した。引用は「道具が危険の手がかりを見つけられないツール」の扱いで、注釈が欠けたときの既定値の話ではない（注釈の欠落については同記事の別の段落『The MCP spec tells clients to assume the worst when a hint is absent』が述べる）。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（自分の誤検出）

<a id="g-g2-verifiers-linters-06"></a>
#### G2VL-06 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 31 サーバー監査の記事（自分の誤検出）

- **資料**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers.（公式ブログ）
- **URL**: https://formael.com/blog/mcp-ecosystem-audit
- **書いてある見出しへ直接**: https://formael.com/blog/mcp-ecosystem-audit#the-four-wrong-labels
- **版**: 2026-07-19 付
- **書いてある場所**: MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > The four wrong labels
- **原文**:

> actlint flagged four Linear tools, and only two survived our hand review.

- **日本語**: actlint は Linear の 4 つのツールを指摘したが、手の確認に残ったのは 2 つだけだった。
- **どう使っているか**: スキーマ上の URL 欄から openWorldHint:false の矛盾を推す規則が、URL をデータとして保存するだけのツール（save_issue）や自社資産の参照（create_attachment_from_upload）で誤検出した例。スキーマの形だけでは『外に出るか』が決まらないことの実例。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Safety Labels Run on the Honor System. We Checked 31 Popular Servers. > The four wrong labels」（取得 2026-10-02T22:11:25Z、sha256 9763a88ab0fe…）
- **補足**: 記事は『The scorecard above counts all eight raw findings, and this paragraph is the review that half of them didn't survive.』と書く（verify_quote.py で exact）。スコアカードの表は等級（Clean / Low / High）だけで件数の列が無く、8 件の内訳（どのサーバーの何件か）は記事から再構成できない。また Linear の等級 High は手の確認で残った 2 件（get_diff, get_diff_threads）に基づくと読めるが、表がどちらの数で等級を付けたかは不明。 notes の『表の件数は手の確認前の生の指摘数を含む（表の数字と確認後の数字が異なる）』は過大だった。表には件数が無いので、内訳は再構成できない、に直した。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（formael/actlint）— 導出エンジン

<a id="g-g2-verifiers-linters-07"></a>
#### G2VL-07 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint（formael/actlint）— 導出エンジン

- **資料**: packages/core/src/derive/derive.ts（検査の道具のソースコード）
- **URL**: https://github.com/formael/actlint/blob/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/packages/core/src/derive/derive.ts#L9-L11
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/formael/actlint/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/packages/core/src/derive/derive.ts
- **版**: commit d7aba1a（2026-08-09、npm actlint 0.3.0 系の README）
- **書いてある場所**: packages/core/src/derive/derive.ts の 9 行目
- **原文**:

> It is declaration-blind: `tool.annotations` is never read here.

- **日本語**: 宣言を見ない設計: ここでは tool.annotations を一度も読まない。
- **どう使っているか**: コードの上でも、効果の推定（derive）は name・description・inputSchema の 3 つの抽出器だけを呼ぶ。宣言は後段の classify で比べる対象。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、9 行（取得 2026-10-02T22:11:41Z、sha256 18d70301ac2c…）
- **補足**: 同じファイル L28 に『Intentionally absent: an annotation extractor. Derivation must not read `tool.annotations`.』。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 設計文書（分類段階: destructiveHint:false の扱い）

<a id="g-g2-verifiers-linters-08"></a>
#### G2VL-08 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 設計文書（分類段階: destructiveHint:false の扱い）

- **資料**: docs/architecture/04-analysis-pipeline.md — Stage 3: Classification（検査の道具の文書）
- **URL**: https://github.com/formael/actlint/blob/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/docs/architecture/04-analysis-pipeline.md#L100-L105
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/formael/actlint/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/docs/architecture/04-analysis-pipeline.md
- **版**: commit d7aba1a
- **書いてある場所**: docs/architecture/04-analysis-pipeline.md — Stage 3: Classification の 103-105 行目（直前の見出し: ## Stage 3: Classification）
- **原文**:

> A `destructiveHint: false` on a mutating tool is only under-declared when the mutation is corroborated as irrecoverable; a reversible toggle honestly declaring itself non-destructive is consistent, not dishonest.

- **日本語**: 書き換えをするツールの destructiveHint:false は、その変更が取り返しのつかないものだと裏づけられたときだけ過少申告とする。元に戻せる切り替えが非破壊と申告するのは正直で、嘘ではない。
- **どう使っているか**: D2（destructiveHint:false）の照合は『破壊的か』の推定が irrecoverable と裏づけられた場合に限る。比べる側面は destructiveness（readOnlyHint と destructiveHint）、external reach（openWorldHint）、reversibility（対応する hint なし）の 3 つで、idempotentHint（D4）は比較の対象に挙がっていない。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、103-105 行（## Stage 3: Classification）（取得 2026-10-02T22:11:33Z、sha256 033e7b7021a0…）
- **補足**: 同じ節で『Silence cannot accuse』（手がかりが無い unknown は明示の宣言と矛盾にしない）と書き、宣言が欠けた hint は MCP 仕様の既定値で補って比べる（『each hint resolved against its MCP spec default when absent』）。なお packages/vocabulary/data/mcp-mapping.json は idempotentHint にも raisesVerdict: true の対応を置く（30 行目、exact）が、この commit の packages/core/src/classify/classify.ts は比べる側面を『destructiveness, external reach, reversibility』の 3 つとしており（5 行目、exact）、idempotentHint の照合は実装されていない。 notes に、語彙の対応表（mcp-mapping.json）は idempotentHint を判定に使うと書く一方、分類の実装は 3 側面だけ、という食い違いを補った（どちらも commit 固定の raw で exact）。

### Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 評価の床（eval/thresholds.json）

<a id="g-g2-verifiers-linters-09"></a>
#### G2VL-09 Formael（formael/actlint の開発元。同社は MCP 向けの商用製品も出している） — actlint — 評価の床（eval/thresholds.json）

- **資料**: eval/thresholds.json（検査の道具のソースコード）
- **URL**: https://github.com/formael/actlint/blob/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/eval/thresholds.json#L4
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/formael/actlint/d7aba1a0fe8ecfd444b808681c1d1aae7b8c46de/eval/thresholds.json
- **版**: commit d7aba1a
- **書いてある場所**: eval/thresholds.json の 4 行目
- **原文**:

> Current basis (2026-07-15, corpus = 9 servers / 96 tools): 12 TP / 0 FP / 3 FN => precision 100.0%, recall 80.0%, F0.5 95.2%

- **日本語**: 現在の根拠（2026-07-15、コーパス = 9 サーバー / 96 ツール）: 真陽性 12 / 偽陽性 0 / 偽陰性 3 → 適合率 100.0%、再現率 80.0%、F0.5 95.2%。
- **どう使っているか**: 開発元自身の精度測定。分母は 9 サーバー / 96 ツールのラベル付きコーパス（eval/corpus/*）で、31 サーバーの監査とは別。ラベルの根拠の種類を手で数えると source-inspection 92・behavioral-inference 4（本調査が labels.json を数えた値）。
- **条件**: 数値は開発元の自己申告で未検証（verified_by_me = none）。同じ notes は『three positives are synthetic regression guards (behavioral-inference provenance)』と書く。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、4 行（取得 2026-10-02T22:11:33Z、sha256 e245ec077ad4…）
- **補足**: eval/README.md は『A precision figure computed against manifest-only labels is self-confirming』として、ラベルにソースの読解などの根拠を求めている。つまり評価のラベルはソースに基づくが、道具そのものはソースを読まない。

### vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-server-lint / mcp-doctor（PyPI 0.12.13）— README の検査一覧

<a id="g-g2-verifiers-linters-10"></a>
#### G2VL-10 vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-server-lint / mcp-doctor（PyPI 0.12.13）— README の検査一覧

- **資料**: README.md — Read-only annotation mismatch（検査の道具の文書）
- **URL**: https://github.com/vishalhabib99/mcp-doctor/blob/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/README.md#L172
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vishalhabib99/mcp-doctor/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/README.md
- **版**: commit d55702d（pyproject の version 0.12.13。PyPI の sdist 0.12.13 の analyzer.py は repo と同一であることを diff で確かめた）
- **書いてある場所**: README.md — Read-only annotation mismatch の 172 行目（直前の見出し: ## Security checks）
- **原文**:

> A tool declaring `annotations=ToolAnnotations(read_only_hint=True)` (Python/FastMCP decorator style only, for now) whose own body contains a raw SQL mutation verb, a file opened in write/append mode, a filesystem deletion call, or a mutating call on a recognizable HTTP client

- **日本語**: annotations=ToolAnnotations(read_only_hint=True) と宣言したツール（今は Python / FastMCP のデコレータ形式だけ）で、自分の本体に生の SQL の更新語、書き込み・追記モードで開くファイル、ファイル削除の呼び出し、見分けのつく HTTP クライアントの更新系呼び出しがあるもの。
- **どう使っているか**: 照合の種類は (b) ソースの静的解析（ただし関数本体の文字列に対する正規表現）。扱うのは D1（readOnlyHint:true）だけ。D2〜D4 の宣言と実装の照合はない。
- **条件**: 対象は FastMCP の @mcp.tool(annotations=ToolAnnotations(...)) 形式だけ（README の記載）。README 自身が『Heuristic, deliberately narrow』と書く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、172 行（## Security checks）（取得 2026-10-02T22:11:37Z、sha256 b1eb94264ecc…）
- **補足**: 本調査で見つけた中で、宣言を『ソースコード』と照合する道具は、これと HintLint（C09 で収録済み）の 2 つ。Cisco mcp-scanner のコード整合性分析（C09 で収録済み）は LLM による判定。

### vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — analyzer.py（変異の手がかりの検出）

<a id="g-g2-verifiers-linters-11"></a>
#### G2VL-11 vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — analyzer.py（変異の手がかりの検出）

- **資料**: mcp_doctor/analyzer.py — _scan_for_mutation_signal（検査の道具のソースコード）
- **URL**: https://github.com/vishalhabib99/mcp-doctor/blob/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/mcp_doctor/analyzer.py#L856-L872
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vishalhabib99/mcp-doctor/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/mcp_doctor/analyzer.py
- **版**: commit d55702d（0.12.13）
- **書いてある場所**: mcp_doctor/analyzer.py — _scan_for_mutation_signal の 866 行目
- **原文**:

> body_text = ast.unparse(fn)

- **日本語**: body_text = ast.unparse(fn)（ツール関数の AST を文字列に戻し、それに正規表現をかける）
- **どう使っているか**: ast.unparse(fn) でツール関数の定義全体（デコレータ・docstring・入れ子の関数定義を含む。コメントは消える）を文字列に戻し、4 種の正規表現（SQL の INSERT INTO / UPDATE … SET / DELETE FROM / DROP TABLE / ALTER TABLE、open(…, 'w'/'a' 等)、os.remove / os.unlink / os.rmdir / shutil.rmtree、(requests|httpx|client|session).(post|put|delete|patch)( ）を当てる。呼び出し先の関数へは降りない（手続き間の解析なし）。受け手の型推論もなく、変数名が client / session などのときだけ HTTP の更新とみなす。docstring に SQL の更新文が書いてあるだけでも当たりうる（本調査のコード読解）。当たると annotation_mismatch を severity warning・category security で出し、文言は『Heuristic — worth a human look, not confirmed.』。
- **条件**: 宣言の読み取りは _find_fastmcp_tools の中だけで、デコレータが呼び出し形（@<…>.tool(…)）のとき、その annotations= が関数呼び出し（ToolAnnotations(...) など）で、read_only_hint / readOnlyHint がリテラルの True の場合に限る（L1074-1078 の _kwarg_call と _kwarg_bool）。dict リテラル・変数経由の注釈、括弧なしの @mcp.tool、README が対応を謳う参照形（mcp.tool(fn)、mcp.add_tool(fn)、Tool.from_function(fn, ...)）や TypeScript / Go のツールには、この照合が掛からない（declared_read_only を渡すのはこの経路だけ。本調査のコード読解）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、866 行（# than signal. A hit here means "worth a human look", not a confirmed bug.）（取得 2026-10-02T22:11:45Z、sha256 a1a954e46b2e…）
- **補足**: コメント（L842-855）は『A hit here means "worth a human look", not a confirmed bug.』と書き、.save()/.commit() は誤検出が多いので除いたと説明する。D1 を Python ソースと照合する既存 OSS として AuthGap と比べる価値がある（本カテゴリ内では唯一。C09 の HintLint も宣言とソースを照合する）。 『ツール関数そのものの本体だけ』は不正確（ast.unparse(fn) はデコレータと docstring も含む）なので直し、重大度（warning）と、参照形・TS/Go に照合が掛からない条件を補った。notes の『唯一の既存 OSS 実装』は C09 の HintLint と矛盾するので弱めた。

### vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — 実行時ゲート（check_tool_registration）

<a id="g-g2-verifiers-linters-12"></a>
#### G2VL-12 vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-doctor — 実行時ゲート（check_tool_registration）

- **資料**: README.md — runtime gate（検査の道具の文書）
- **URL**: https://github.com/vishalhabib99/mcp-doctor/blob/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/README.md#L132
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vishalhabib99/mcp-doctor/d55702d8ba7066e039e2bb1ca15184b3d4aa2e0f/README.md
- **版**: commit d55702d（0.12.13）
- **書いてある場所**: README.md の 132 行目（直前の見出し: ## Runtime gate — the same two checks, applied to live `tools/list` metadata）
- **原文**:

> an agent discovering tools at runtime has no access to server source, only what the server declares about itself.

- **日本語**: 実行時にツールを見つけるエージェントはサーバーのソースを見られず、サーバーが自分について宣言したことしか分からない。
- **どう使っているか**: tools/list のメタデータだけを受ける実行時版では、D1 と実装の照合はできないと明言。できるのは説明の質と、注釈同士の内部整合（readOnlyHint:true と destructiveHint:true の同時指定）だけ。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、132 行（# tools = (await session.list_tools()).tools, from your own client）（取得 2026-10-02T22:11:37Z、sha256 b1eb94264ecc…）
- **補足**: 同 README L134: 静的版は readOnlyHint:true と destructiveHint の『存在』で矛盾とするが、実行時版は destructiveHint が true のときだけにした（server-memory で 9 件の誤検出が出たため）。 location の見出しを直した。verify_quote.py が返した『# tools = …』はコードブロック内のコメントで、本当の直前の見出しは 118 行目の ## Runtime gate。

### inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter（PyPI mcp-tool-card-linter 1.0.0）— 危険分類

<a id="g-g2-verifiers-linters-13"></a>
#### G2VL-13 inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter（PyPI mcp-tool-card-linter 1.0.0）— 危険分類

- **資料**: src/mcp_tool_card_linter/lint.py — _risk_categories（検査の道具のソースコード）
- **URL**: https://github.com/inostarlin-passion/MCP-Tool-Card-Linter/blob/75de0634d6e281bd36c3f083286fd59fbbdca7a7/src/mcp_tool_card_linter/lint.py#L2082-L2103
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/inostarlin-passion/MCP-Tool-Card-Linter/75de0634d6e281bd36c3f083286fd59fbbdca7a7/src/mcp_tool_card_linter/lint.py
- **版**: commit 75de063（PyPI 1.0.0、2026-07-15。sdist の lint.py は repo と同一であることを diff で確かめた）
- **書いてある場所**: src/mcp_tool_card_linter/lint.py — _risk_categories の 2095 行目
- **原文**:

> tool.annotations.get("readOnlyHint") is True

- **日本語**: tool.annotations.get("readOnlyHint") is True（readOnlyHint が true か、説明に read-only 等の語があれば、名前に出ていない write / financial / network の分類を捨てる）
- **どう使っているか**: 照合の種類は (a) 名前・説明・メタデータ文字列の正規表現（RISK_PATTERNS）。効果の推定そのものが宣言を入力に使う: readOnlyHint:true を宣言するか、説明に read-only / does not modify / do not (modify|write|delete) の語があると、名前に出ていない write / financial / network の分類を捨てる（L2094-2102）。destructive（delete / remove / drop …）と code_execution（shell / command / sql …）の分類は捨てない。そのため D1 の矛盾（ANNOTATION_CONFLICT_READ_ONLY）が出るのは、名前に write / financial / network の語があるか、名前・説明・メタデータに destructive か code_execution の語があるときに限られる。D3 の矛盾（network 分類で openWorldHint:false）も、readOnlyHint:true を併せて宣言すると名前に network の語があるときだけになる（本調査のコード読解）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、2095 行（取得 2026-10-02T22:12:03Z、sha256 c418d09c9894…）
- **補足**: actlint の『宣言を見ない導出』と逆の設計。L2094-2102。 usage_ja の『名前に書き込み語がある場合にほぼ限られる』は誤り。捨てるのは write / financial / network だけで、説明文の destructive・code_execution の語は残り D1 の矛盾を起こす。説明に read-only 等と書くだけでも同じ扱いになる点も補った。

### inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter — 注釈の矛盾規則

<a id="g-g2-verifiers-linters-14"></a>
#### G2VL-14 inostarlin-passion（個人開発。PyPI 名 mcp-tool-card-linter） — MCP Tool Card Linter — 注釈の矛盾規則

- **資料**: src/mcp_tool_card_linter/lint.py — _check_annotations（検査の道具のソースコード）
- **URL**: https://github.com/inostarlin-passion/MCP-Tool-Card-Linter/blob/75de0634d6e281bd36c3f083286fd59fbbdca7a7/src/mcp_tool_card_linter/lint.py#L1990-L2033
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/inostarlin-passion/MCP-Tool-Card-Linter/75de0634d6e281bd36c3f083286fd59fbbdca7a7/src/mcp_tool_card_linter/lint.py
- **版**: commit 75de063（1.0.0）
- **書いてある場所**: src/mcp_tool_card_linter/lint.py — _check_annotations の 1996 行目
- **原文**:

> message="Tool appears to have side effects but is annotated as read-only.",

- **日本語**: ツールに副作用がありそうなのに read-only と注釈されている。
- **どう使っているか**: 規則: ANNOTATION_CONFLICT_READ_ONLY（D1、error）、DESTRUCTIVE_HINT_MISSING（destructive と推定され destructiveHint が true でない、warning。D2 の false 宣言もここに入る）、ANNOTATION_CONFLICT_OPEN_WORLD（network 分類で openWorldHint:false、D3、warning）、READ_ONLY_HINT_RECOMMENDED（info）、readOnlyHint と destructiveHint の同時 true（error）。D4 idempotentHint は型（bool か）だけを見る。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、1996 行（取得 2026-10-02T22:12:03Z、sha256 c418d09c9894…）
- **補足**: L200 に『Side-effect, schema, and prompt-injection checks are static heuristics; they reduce review effort but do not prove runtime safety.』。入力は静的な tools JSON・mcp.json・stdio / Streamable HTTP のサーバー（README 9 行目『Input sources: …』は verify_quote.py で exact）。src/ を grep すると送る要求は tools/list だけで tools/call は 0 件（commit 75de063）なので、ツールは呼ばない。 notes の『未照合』だった入力源とツールを呼ばない点を、README の exact とコードの grep で確かめた。

### cejor6（個人開発。npm mcpconform） — mcpconform — 規則 tool/destructive-needs-annotation

<a id="g-g2-verifiers-linters-15"></a>
#### G2VL-15 cejor6（個人開発。npm mcpconform） — mcpconform — 規則 tool/destructive-needs-annotation

- **資料**: src/rules.mjs（検査の道具のソースコード）
- **URL**: https://github.com/cejor6/mcpconform/blob/86f07c9e511cb7cfe03c298eeff83d049bddb01e/src/rules.mjs#L56-L63
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cejor6/mcpconform/86f07c9e511cb7cfe03c298eeff83d049bddb01e/src/rules.mjs
- **版**: commit 86f07c9
- **書いてある場所**: src/rules.mjs の 59 行目
- **原文**:

> const ok = a && (typeof a.destructiveHint === "boolean" || a.readOnlyHint === true);

- **日本語**: 注釈があって、destructiveHint が真偽値で書かれているか readOnlyHint が true なら合格。
- **どう使っているか**: 照合の種類は (a) 名前の動詞の正規表現（MUTATING）。更新系の名前のツールに注釈が欠けているかだけを見る。値の正しさは見ないので、更新系の名前で readOnlyHint:true や destructiveHint:false を宣言しても合格になる（D1・D2 の嘘は通る）。ほかに readOnlyHint と destructiveHint の同時 true を tool/annotations-consistency で指摘。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、59 行（取得 2026-10-02T22:11:34Z、sha256 01b9df5f9c3f…）
- **補足**: README L10 は『intentionally not a security scanner and not a live conformance tester』と書き、対象は形と移植性（静的・オフライン）。

### hahahahahahahahah6（個人開発。mcp-lint） — mcp-lint（設計リンター）— 規則 destructive-no-confirm

<a id="g-g2-verifiers-linters-16"></a>
#### G2VL-16 hahahahahahahahah6（個人開発。mcp-lint） — mcp-lint（設計リンター）— 規則 destructive-no-confirm

- **資料**: mcp_lint.py（検査の道具のソースコード）
- **URL**: https://github.com/hahahahahahahahah6/mcp-lint/blob/40f41f3590a0092c6ff4ba56d6e3112a1c00fcc2/mcp_lint.py#L108-L118
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/hahahahahahahahah6/mcp-lint/40f41f3590a0092c6ff4ba56d6e3112a1c00fcc2/mcp_lint.py
- **版**: commit 40f41f3
- **書いてある場所**: mcp_lint.py の 115 行目
- **原文**:

> if tokens & DESTRUCTIVE_TOKENS and destructive_hint is None:

- **日本語**: 名前の語に破壊的な語があり、かつ destructiveHint が宣言されていないときだけ（説明に確認の語が無ければ）指摘する。
- **どう使っているか**: (a) 名前の語による発見的規則。コメント（L109-111）は destructiveHint が true でも false でも『作者の宣言を尊重して』名前の規則を飛ばすと書く。つまり D2（destructiveHint:false）は検査されず、宣言すると指摘が消える。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、115 行（# ---------------------------------------------------------------------------）（取得 2026-10-02T22:12:03Z、sha256 c0b907f7ab19…）
- **補足**: リポジトリの説明『unconfirmed destructive tools』はこの規則のこと。 usage から passthrough_or_expose を外した。この規則は宣言を下流へ渡すのではなく、宣言があると名前の規則を飛ばす（宣言を信用して指摘を消す）もの。その点は usage_ja に書かれている。

### superintelligenceco（mcp-lint） — mcp-lint（MCP サーバーの採点）— capability/missing-annotations

<a id="g-g2-verifiers-linters-17"></a>
#### G2VL-17 superintelligenceco（mcp-lint） — mcp-lint（MCP サーバーの採点）— capability/missing-annotations

- **資料**: src/rules/capability.ts（検査の道具のソースコード）
- **URL**: https://github.com/superintelligenceco/mcp-lint/blob/2c9f6ffb9b7f6a400ce3811236ecf871fe9e7629/src/rules/capability.ts#L180-L205
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/superintelligenceco/mcp-lint/2c9f6ffb9b7f6a400ce3811236ecf871fe9e7629/src/rules/capability.ts
- **版**: commit 2c9f6ff
- **書いてある場所**: src/rules/capability.ts の 192 行目
- **原文**:

> message: "Tool name suggests it changes state, but it declares readOnlyHint: true.",

- **日本語**: ツール名は状態を変えそうなのに readOnlyHint:true を宣言している。
- **どう使っているか**: (a) 名前の語（先頭が読み動詞でなく、破壊的な動詞を含む）と D1 の照合。両方未設定なら設定を促す。別規則 capability/unconstrained-network は URL 引数を見て、openWorldHint:true の宣言があるときは文言を変える（D3 の false との矛盾は検出しない）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、192 行（取得 2026-10-02T22:11:35Z、sha256 6604c586e4b4…）
- **補足**: 規則 capability/missing-annotations の既定の重大度は info だが、引用の矛盾（名前が更新系で readOnlyHint:true）は severity: "warning" を明示して出す（L190）。注釈が両方未設定の場合だけが既定の info。 notes の『既定の重大度は info』は D1 の矛盾の指摘には当たらない（コードで warning を明示）ので直した。

### antonsoo（個人開発。mcplint） — mcplint — safety/missing-annotations

<a id="g-g2-verifiers-linters-18"></a>
#### G2VL-18 antonsoo（個人開発。mcplint） — mcplint — safety/missing-annotations

- **資料**: docs/rules/safety-missing-annotations.md（検査の道具の文書）
- **URL**: https://github.com/antonsoo/mcplint/blob/cee2edc1691564465b2adc19e85963b108854c6d/docs/rules/safety-missing-annotations.md#L5-L7
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/antonsoo/mcplint/cee2edc1691564465b2adc19e85963b108854c6d/docs/rules/safety-missing-annotations.md
- **版**: commit cee2edc
- **書いてある場所**: docs/rules/safety-missing-annotations.md の 7 行目（直前の見出し: # safety/missing-annotations）
- **原文**:

> but its `annotations` object is missing, or has neither `destructiveHint` nor `readOnlyHint` set.

- **日本語**: （破壊的に聞こえる語幹を名前か説明に含むのに）annotations が無いか、destructiveHint も readOnlyHint も設定されていない。
- **どう使っているか**: (a) 名前・説明の語幹による『宣言の欠落』の検査だけ。宣言された値が実装と合うか（D1〜D4 の嘘）は見ない。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、7 行（# safety/missing-annotations）（取得 2026-10-02T22:12:56Z、sha256 4d91421d981e…）
- **補足**: 同じ文書は『Per spec, unset hints default to `readOnlyHint: false, destructiveHint: true`, which *is* the safe default — but only if the client actually enforces that default rather than treating "unset" as "don't ask."』と書く（後半を verify_quote.py で exact、15 行目）。既定の重大度は warning。 notes の補足引用を検証済みにした。

### DLeibner（個人開発。mcp-surface-lint） — mcp-surface-lint — annotations-missing-hints

<a id="g-g2-verifiers-linters-19"></a>
#### G2VL-19 DLeibner（個人開発。mcp-surface-lint） — mcp-surface-lint — annotations-missing-hints

- **資料**: packages/core/docs/rules.md（検査の道具の文書）
- **URL**: https://github.com/DLeibner/mcp-surface-lint/blob/e900db2333c51183b32edb3f458cb10bd82f0852/packages/core/docs/rules.md#L41
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/DLeibner/mcp-surface-lint/e900db2333c51183b32edb3f458cb10bd82f0852/packages/core/docs/rules.md
- **版**: commit e900db2
- **書いてある場所**: packages/core/docs/rules.md の 41 行目（直前の見出し: ### annotations/missing-hints）
- **原文**:

> Prose like "confirm with the user first" is invisible to that machinery.

- **日本語**: 『まずユーザーに確認して』のような説明文は、その仕組み（確認を出すかを決める機械）には見えない。
- **どう使っているか**: (a) 名前の更新系動詞（create_ / delete_ / cancel_ …）で、readOnlyHint も destructiveHint も無いものを warn。値の正しさは見ない。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、41 行（### annotations/missing-hints）（取得 2026-10-02T22:11:30Z、sha256 6cdcd69652c4…）
- **補足**: 同じ行の前半『A tool with a mutating verb (`create_`, `delete_`, `cancel_`, …) declares neither `readOnlyHint` nor `destructiveHint`.』。repo の data/results/ に実サーバー（例: grafana 2026-09-03）の結果を置いている。

### StudioMeyer（studiomeyer-io） — mcp-protocol-conformance — annotations 監査スイート

<a id="g-g2-verifiers-linters-20"></a>
#### G2VL-20 StudioMeyer（studiomeyer-io） — mcp-protocol-conformance — annotations 監査スイート

- **資料**: src/specs/annotations-rules.ts（検査の道具のソースコード）
- **URL**: https://github.com/studiomeyer-io/mcp-protocol-conformance/blob/4d9fcb529d9493f3d9f699c16bdbac5b045b56e3/src/specs/annotations-rules.ts#L40-L48
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/studiomeyer-io/mcp-protocol-conformance/4d9fcb529d9493f3d9f699c16bdbac5b045b56e3/src/specs/annotations-rules.ts
- **版**: commit 4d9fcb5
- **書いてある場所**: src/specs/annotations-rules.ts の 46 行目
- **原文**:

> message: `Tool name '${name}' suggests a destructive action but destructiveHint is not set to true.`,

- **日本語**: ツール名は破壊的な操作を示すのに destructiveHint が true になっていない。
- **どう使っているか**: 実サーバーに接続する適合性テストの一部だが、注釈の検査は (a) 名前の正規表現: 破壊語を含む名前で destructiveHint が true でない（D2 の false も含む）→ warn、読み動詞で始まる名前で readOnlyHint:false → warn、readOnlyHint と destructiveHint の同時 true → fail（suites/annotations.ts で不合格の結果になる）。前の 2 つは警告で不合格にしない。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、46 行（取得 2026-10-02T22:11:38Z、sha256 247ab9d9ef47…）
- **補足**: 注釈の規則は tools/list の記述子だけを見る。同じパッケージの smoke スイート（src/suites/smoke.ts）は全ツールを 1 回ずつ tools/call するが、注釈を参照せず、呼ぶ対象の選別にも使わない（ファイル中に annotation / Hint の語が 0 件）。 usage_ja の『いずれも警告で不合格にはしない』は誤り。同時 true は severity "fail"（L63）で、スイートは fail の結果を出す。L6 のコメントは最初の規則についての記述。smoke スイートが注釈を見ずに全ツールを呼ぶ点も補った。

### AgentPostmortem（MCP-audit） — MCP-audit — MCP004 readOnlyHint の不一致

<a id="g-g2-verifiers-linters-21"></a>
#### G2VL-21 AgentPostmortem（MCP-audit） — MCP-audit — MCP004 readOnlyHint の不一致

- **資料**: src/rules/permissions.ts（検査の道具のソースコード）
- **URL**: https://github.com/AgentPostmortem/MCP-audit/blob/b35301fc8e5737b6de8736df480d6e56663f413f/src/rules/permissions.ts#L97-L128
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/AgentPostmortem/MCP-audit/b35301fc8e5737b6de8736df480d6e56663f413f/src/rules/permissions.ts
- **版**: commit b35301f
- **書いてある場所**: src/rules/permissions.ts の 106 行目
- **原文**:

> "A tool that mutates or deletes state must not advertise readOnlyHint, which clients use to auto-approve safe reads.",

- **日本語**: 状態を変えたり消したりするツールは readOnlyHint を掲げてはならない。クライアントはそれで安全な読み取りを自動承認するから。
- **どう使っているか**: (a) 名前と説明の文字列に書き込み・破壊の動詞があり、readOnlyHint:true を宣言したツールを high で指摘（D1 だけ）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、106 行（取得 2026-10-02T22:11:32Z、sha256 d499f0b95d62…）
- **補足**: WebSearch の結果に、この規則を足した PR『feat: add MCP004 for readOnlyHint vs write-verb tools』（#48）が出た（github.com の PR ページはこの環境では開けないため未確認）。 規則の説明にある『clients use to auto-approve safe reads』は道具の作者の一般化で、特定のクライアントの挙動の根拠にはならない。 notes に、引用中の「クライアントは自動承認に使う」は作者の一般化だと補った。

### arijitgupta42（個人開発。PyPI mcp-toolgauge 0.1.0） — mcp-toolgauge — MCP040 destructiveHint の欠落

<a id="g-g2-verifiers-linters-22"></a>
#### G2VL-22 arijitgupta42（個人開発。PyPI mcp-toolgauge 0.1.0） — mcp-toolgauge — MCP040 destructiveHint の欠落

- **資料**: docs/rules/MCP040.md（検査の道具の文書）
- **URL**: https://github.com/arijitgupta42/mcp-toolgauge/blob/5908b7a61108371cdb52d9bcc617c66c1cbf5b2a/docs/rules/MCP040.md#L16-L20
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/arijitgupta42/mcp-toolgauge/5908b7a61108371cdb52d9bcc617c66c1cbf5b2a/docs/rules/MCP040.md
- **版**: commit 5908b7a（PyPI 0.1.0）
- **書いてある場所**: docs/rules/MCP040.md の 18 行目（直前の見出し: ## Triggers when）
- **原文**:

> `destructiveHint` is unset (the server said nothing, as distinct from saying `false`)

- **日本語**: destructiveHint が未設定（サーバーが何も言っていない。false と言ったのとは区別する）
- **どう使っているか**: (a) 名前・説明の語による『欠落』の検査（MCP040 destructive / MCP041 read-only / MCP042 idempotentHint）。destructiveHint:false と明示すれば MCP040 は出ない（D2 の嘘は見ない）。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、18 行（## Triggers when）（取得 2026-10-02T22:11:31Z、sha256 7e26bc50e0b4…）
- **補足**: lint/rules/annotations.py の 3 規則はいずれも『未設定（_unset）』が条件。 MCP040 の既定の重大度は error（文書冒頭）。 notes に重大度を補った。

### vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-fuzz（同じ作者の実行型の検査）

<a id="g-g2-verifiers-linters-23"></a>
#### G2VL-23 vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-fuzz（同じ作者の実行型の検査）

- **資料**: mcp_fuzz/engine.py（モジュールの docstring）（検査の道具のソースコード）
- **URL**: https://github.com/vishalhabib99/mcp-fuzz/blob/8970405872331b051f86fc74ef2dea22bccb9e17/mcp_fuzz/engine.py#L6-L13
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vishalhabib99/mcp-fuzz/8970405872331b051f86fc74ef2dea22bccb9e17/mcp_fuzz/engine.py
- **版**: commit 8970405
- **書いてある場所**: mcp_fuzz/engine.py（モジュールの docstring） の 6-7 行目
- **原文**:

> Safety: a tool that isn't explicitly annotated `readOnlyHint: true` is skipped by default.

- **日本語**: 安全のため: 明示的に readOnlyHint:true と注釈されていないツールは、既定では飛ばす。
- **どう使っているか**: (c) 実行する道具だが、宣言を検証せずに『呼んでよいか』の判定に使う。既定では readOnlyHint:true のツールだけを呼ぶ（include_destructive=True で全部）。D1 が嘘なら、ファズが書き込みツールを実データに対して呼ぶことになる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、6-7 行（取得 2026-10-02T22:11:39Z、sha256 86e23d7d3632…）
- **補足**: L290-294 の _is_read_only は注釈が無ければ False、readOnlyHint（read_only_hint）がリテラルの True のときだけ True。飛ばしたツールは skip_reason『not annotated readOnlyHint=true (use include_destructive to test anyway)』で記録される（L680-684）。CLI では --include-destructive。 引用が文の途中で切れていたので、文の終わりまで（2 行）に直して exact を確かめた。usage の auto_approve を policy_rule_input に替えた: 人の承認を省く流れではなく、検査の道具が「どのツールを実際に呼ぶか」を readOnlyHint で選ぶ使い方なので。

### vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-reality-check（同じ作者の実行型の検査）

<a id="g-g2-verifiers-linters-24"></a>
#### G2VL-24 vishalhabib99（個人開発。PyPI 名 mcp-server-lint、コマンド名 mcp-doctor） — mcp-reality-check（同じ作者の実行型の検査）

- **資料**: mcp_reality_check/engine.py（モジュールの docstring）（検査の道具のソースコード）
- **URL**: https://github.com/vishalhabib99/mcp-reality-check/blob/8105567b18530410e33c76a8a61740fe24cec0cc/mcp_reality_check/engine.py#L15-L18
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/vishalhabib99/mcp-reality-check/8105567b18530410e33c76a8a61740fe24cec0cc/mcp_reality_check/engine.py
- **版**: commit 8105567
- **書いてある場所**: mcp_reality_check/engine.py（モジュールの docstring） の 15-16 行目
- **原文**:

> Safety: same default as mcp-fuzz — only `readOnlyHint: true` tools are called unless `--include-destructive` is passed.

- **日本語**: 安全のため: mcp-fuzz と同じ既定 — --include-destructive を渡さない限り、readOnlyHint:true のツールだけを呼ぶ。
- **どう使っているか**: (c) 実際に tools/call して応答の中身を確かめる道具だが、D1 の宣言は検証せず、呼ぶ対象の選別に信用する。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、15-16 行（取得 2026-10-02T22:12:06Z、sha256 0b3129c989fa…）
- **補足**: CLI の --include-destructive の説明（cli.py L20）も同じ。 引用が文の途中で切れていたので、文の終わりまで（2 行）に直して exact を確かめた。usage の auto_approve を policy_rule_input に替えた: 人の承認を省く流れではなく、検査の道具が「どのツールを実際に呼ぶか」を readOnlyHint で選ぶ使い方なので。

### himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — dev.to の紹介記事

<a id="g-g2-verifiers-linters-25"></a>
#### G2VL-25 himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — dev.to の紹介記事

- **資料**: Your MCP Server Says It Is Read-Only. Who Checked?（第三者の記事）
- **URL**: https://dev.to/himanshu_748/your-mcp-server-says-it-is-read-only-who-checked-2mjk
- **書いてある見出しへ直接**: https://dev.to/himanshu_748/your-mcp-server-says-it-is-read-only-who-checked-2mjk#the-gap
- **版**: 2026-08-30 公開（dev.to API の published_at）
- **書いてある場所**: Your MCP Server Says It Is Read-Only. Who Checked? > The gap
- **原文**:

> Airlock opens a case, inventories the declared tools, exercises them under a capped budget and compares the declaration with its observations.

- **日本語**: Airlock は案件を開き、宣言されたツールを一覧にし、上限つきの予算で実際に動かし、宣言と観察を比べる。
- **どう使っているか**: (c) 実行と観察による照合。readOnlyHint:true のツールでファイル書き込み・状態変更を観察したら食い違い（証拠）とする。証拠を見た人が Block / Approve selected / Approve all を選び、許可した案件には強制するプロキシを指す接続設定を出す。許可していないツールの呼び出しはプロキシが拒む（MCP error -32001）。承認を毎回求めるツールの最小集合には、宣言上敏感なツール（readOnlyHint が true でない、または destructiveHint が true）も入る（approval.py。repo 項目を参照）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Your MCP Server Says It Is Read-Only. Who Checked? > The gap」（取得 2026-10-02T22:11:22Z、sha256 94918cac5df0…）
- **補足**: 作者自身の紹介。記事の数値（制御された不正直なフィクスチャで 36 検査中 7 件・仕込んだ 5 つの挙動すべて、正直なフィクスチャで 0 件）は自作フィクスチャ上の結果で未検証。外部サーバー（ContextFirewall）では 6 ツールとも注釈が無かった、とも書く。 usage_ja を記事に合わせて具体化した（人が Block / Approve を選ぶ。承認の要否は宣言にも依存する）。

### himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — 検出器（annotation_divergence）

<a id="g-g2-verifiers-linters-26"></a>
#### G2VL-26 himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — 検出器（annotation_divergence）

- **資料**: airlock/detectors.py（検査の道具のソースコード）
- **URL**: https://github.com/himanshu748/airlock-mcp/blob/8ed02c0aa5405cd155445191dcc03de4847c57c3/airlock/detectors.py#L108-L125
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/himanshu748/airlock-mcp/8ed02c0aa5405cd155445191dcc03de4847c57c3/airlock/detectors.py
- **版**: commit 8ed02c0
- **書いてある場所**: airlock/detectors.py の 122 行目
- **原文**:

> f"{event.tool} claimed read-only behavior, but Airlock observed "

- **日本語**: （ツール名）は読み取り専用だと言ったが、Airlock は（ファイル書き込み / 状態変更）を観察した。
- **どう使っているか**: 条件は readOnlyHint が true で、観察した事象が FILESYSTEM_WRITE か STATE_CHANGE（_STATE_CHANGING_EVENTS、L28-31）。判定は BLOCK・証拠の強さ DIRECT。扱うのは D1 だけ（destructiveHint / openWorldHint / idempotentHint の宣言との照合は無い。外への通信は宣言ではなく運用者の許可ホストと比べる）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、122 行（取得 2026-10-02T22:11:34Z、sha256 bf26514d223c…）
- **補足**: approval.py（L18-23、exact）は readOnlyHint が true でないか destructiveHint が true のツールを『宣言上敏感』として承認の最小集合に入れる。逆に言えば、readOnlyHint:true（destructiveHint が true でない）で、指摘も sensor_failed も無く、未検査の理由が capability_absent だけのツールは、最小集合に入らない（capability_absent は「証拠モードの開示された限界」として承認の門にしない、とコメント）。つまり transcript_only で検査した第三者サーバーでは、D1 の宣言が照合されないまま承認の門を外す側に働きうる（本調査のコード読解。運用者は手で承認対象に足せる）。 notes に、承認の最小集合が readOnlyHint:true の宣言を信用し、capability_absent の未検査を門にしない点を補った（コード読解）。

### himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — README（証拠モード）

<a id="g-g2-verifiers-linters-27"></a>
#### G2VL-27 himanshu748（個人開発。Airlock / airlock-mcp） — Airlock — README（証拠モード）

- **資料**: README.md — Evidence modes（検査の道具の文書）
- **URL**: https://github.com/himanshu748/airlock-mcp/blob/8ed02c0aa5405cd155445191dcc03de4847c57c3/README.md#L222-L246
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/himanshu748/airlock-mcp/8ed02c0aa5405cd155445191dcc03de4847c57c3/README.md
- **版**: commit 8ed02c0
- **書いてある場所**: README.md — Evidence modes の 230-233 行目（直前の見出し: ## Evidence modes）
- **原文**:

> For an arbitrary remote server, MCP traffic does not reveal server-side network or filesystem activity, so `transcript_only` is the honest mode and Airlock records those checks as `not_tested` rather than as clean observations.

- **日本語**: 任意のリモートサーバーでは、MCP の通信からサーバー側のネットワークやファイルの動きは見えない。だから transcript_only が正直なモードで、Airlock はそれらの検査を『清浄』ではなく『未検査』と記録する。
- **どう使っているか**: 実行型の照合（annotation_divergence）が効くのは、ファイル・通信のセンサーを持つ controlled_fixture（同梱のフィクスチャ）だけ。monitored_remote は README の表で『Reserved for an operator-supplied trusted sensor integration』（予約）とされる。普通の第三者サーバーは transcript_only で、D1 の照合は not_tested（capability_absent）になる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、230-233 行（## Evidence modes）（取得 2026-10-02T22:11:34Z、sha256 7826884fff4d…）
- **補足**: 実行で宣言を確かめる方式の限界（観察手段が無いと判定できない）を道具自身が明記している例。 usage_ja の『運用者が用意する monitored_remote』は、README では予約（Reserved、228 行目 exact）なので、その旨に直した。

### sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations

<a id="g-g2-verifiers-linters-28"></a>
#### G2VL-28 sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations

- **資料**: Testing MCP Tool Annotations: Validate readOnlyHint, destructiveHint, and openWorldHint for ChatGPT and Claude (July 2026)（第三者の記事）
- **URL**: https://sunpeak.ai/blogs/testing-mcp-tool-annotations/
- **書いてある見出しへ直接**: https://sunpeak.ai/blogs/testing-mcp-tool-annotations/#test-the-protocol-output-not-just-source-files
- **版**: 2026-07-22 付
- **書いてある場所**: Testing MCP Tool Annotations: Validate readOnlyHint, destructiveHint, and openWorldHint for ChatGPT and Claude (July 2026) > Test the Protocol Output, Not Just Source Files
- **原文**:

> Source-level tests are useful, but the host only sees tools/list. Your CI should verify the MCP descriptor that ChatGPT, Claude, or another host will actually read.

- **日本語**: ソースの段階のテストも役に立つが、ホストが見るのは tools/list だけ。CI では ChatGPT や Claude などのホストが実際に読む MCP の記述子を確かめるべきだ。
- **どう使っているか**: テストフレームワーク（sunpeak/test の mcp フィクスチャ）で tools/list を取り、注釈の有無・型、注釈同士の整合を検査する方法の解説。検査の対象は宣言の『公開形』で、実装の効果ではない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 宣言を検査する・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Testing MCP Tool Annotations: Validate readOnlyHint, destructiveHint, and openWorldHint for ChatGPT and Claude (July 2026) > Test the Protocol Output, Not Just Source Files」（取得 2026-10-02T22:11:41Z、sha256 9fc69b93bed9…）
- **補足**: 第三者（製品の宣伝を含む）の使い方の主張として記録する。製品の挙動の根拠にはしない。

### sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations（方針表との照合）

<a id="g-g2-verifiers-linters-29"></a>
#### G2VL-29 sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Testing MCP Tool Annotations（方針表との照合）

- **資料**: Testing MCP Tool Annotations (July 2026)（第三者の記事）
- **URL**: https://sunpeak.ai/blogs/testing-mcp-tool-annotations/
- **書いてある見出しへ直接**: https://sunpeak.ai/blogs/testing-mcp-tool-annotations/#test-for-contradictions
- **版**: 2026-07-22 付
- **書いてある場所**: Testing MCP Tool Annotations: Validate readOnlyHint, destructiveHint, and openWorldHint for ChatGPT and Claude (July 2026) > Test for Contradictions
- **原文**:

> Naming tests are intentionally blunt. They catch common drift, but they should not be your only policy.

- **日本語**: 名前によるテストはわざと大ざっぱにしてある。よくあるずれは拾うが、それだけを方針にしてはいけない。
- **どう使っているか**: 勧める照合は 2 段: (1) 名前の接頭辞（fetch_/send_/post_ … → openWorldHint:true）の発見的規則、(2) 人が書いた期待値の表（expectedAnnotations）と実サーバーの tools/list を toMatchObject で突き合わせる。どちらも宣言を『人の方針』と比べるもので、コードの効果とは比べない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Testing MCP Tool Annotations: Validate readOnlyHint, destructiveHint, and openWorldHint for ChatGPT and Claude (July 2026) > Test for Contradictions」（取得 2026-10-02T22:11:41Z、sha256 9fc69b93bed9…）
- **補足**: 記事の例では readOnlyHint:true なら destructiveHint は false、idempotentHint は true であることを期待する（D4 の宣言を D1 から機械的に要求する例）。

### sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Claude Connector Directory Submission

<a id="g-g2-verifiers-linters-30"></a>
#### G2VL-30 sunpeak（MCP Apps のフレームワーク・テスト基盤の事業者。筆者 Abe Wheeler） — sunpeak ブログ — Claude Connector Directory Submission

- **資料**: Claude Connector Directory Submission: Requirements, Annotations, and How to Pass Review (August 2026)（第三者の記事）
- **URL**: https://sunpeak.ai/blogs/claude-connector-directory-submission/
- **書いてある見出しへ直接**: https://sunpeak.ai/blogs/claude-connector-directory-submission/#make-tool-metadata-pass-the-first-scan
- **版**: 2026-08-13 付
- **書いてある場所**: Claude Connector Directory Submission: Requirements, Annotations, and How to Pass Review (August 2026) > Make Tool Metadata Pass the First Scan
- **原文**:

> The portal reads your live tools/list response and groups tools by their annotations. Missing titles and safety hints appear before you can submit.

- **日本語**: ポータルは稼働中の tools/list の応答を読み、ツールを注釈ごとにまとめる。title や安全の hint が欠けていると、提出前に表示される。
- **どう使っているか**: Claude のディレクトリ提出の審査が注釈の『有無』を機械で見る、という第三者の説明。値が実装と合うかの機械的照合については書かれていない（提出チェックリストに『Read-only and destructive annotations match actual behavior』とあるが、これは作者が自分で確かめる項目）。
- **扱う宣言**: readOnlyHint・destructiveHint・title ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Claude Connector Directory Submission: Requirements, Annotations, and How to Pass Review (August 2026) > Make Tool Metadata Pass the First Scan」（取得 2026-10-02T22:11:38Z、sha256 1aa2b68094ff…）
- **補足**: 第三者の説明で、Anthropic の一次資料ではない（Anthropic の review-criteria は C04 の範囲）。WebSearch の要約に出た『Missing annotations cause about 30% of Connectors Directory rejections』は、この記事の本文からは見つからなかった（別の記事の可能性。未確認）。 同じ記事は『The portal can read metadata; it cannot prove a handler matches it.』（add-an-automated-metadata-gate）と、公開後は『add, change, or remove tools by deploying the server, with no resubmission and no scheduled re-review』（after-you-submit）とも書く（どちらも verify_quote.py で exact。第三者の説明で Anthropic の一次資料ではない）。 notes に、ポータルは宣言と実装の一致を確かめられないこと、公開後の注釈の変更は再審査されないこと（いずれも第三者の主張、exact）を補った。

### bex（bex.co。エージェント向けクラウドの事業者。筆者 Dora Noda） — bex ブログ — dry_run と注釈

<a id="g-g2-verifiers-linters-31"></a>
#### G2VL-31 bex（bex.co。エージェント向けクラウドの事業者。筆者 Dora Noda） — bex ブログ — dry_run と注釈

- **資料**: Your MCP Deploy Tool's dry_run Flag Is a Suggestion, Not a Lock（第三者の記事）
- **URL**: https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap
- **書いてある見出しへ直接**: https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap#what-changes-for-operators
- **版**: 2026-09-24 付
- **書いてある場所**: Your MCP Deploy Tool's dry_run Flag Is a Suggestion, Not a Lock > What changes for operators
- **原文**:

> Audit your annotations separately, as UX copy: fix the readOnlyHint labels that lie (the survey averages more than one mismatch per server), but stop treating the fix as a security control.

- **日本語**: 注釈は UX の文言として別に監査せよ。嘘をつく readOnlyHint は直せ（調査では 1 サーバーあたり平均 1 件を超える不一致）。ただし、直すことを安全の制御とみなすのはやめよ。
- **どう使っているか**: 注釈の監査（宣言の正しさ）は UX の品質の問題で、安全の制御はサーバー側（dry_run・環境・テナントを呼び手に決めさせない）に置け、という主張。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Your MCP Deploy Tool's dry_run Flag Is a Suggestion, Not a Lock > What changes for operators」（取得 2026-10-02T22:11:22Z、sha256 ff7b55c4a644…）
- **補足**: 第三者の主張。記事中の『A 2026 survey of 508 MCP servers surfaced 8,286 findings, including 612 "privilege annotation mismatches"』は出典のリンクが無く、本調査では元の調査を特定できなかった（数値は未検証、出典不明）。 再取得で sha256 が変わった（動的なページ）。引用は exact のまま。

### Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

<a id="g-g2-registries-marketplaces-01"></a>
#### G2RM-01 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: McpToolAnnotations.java（登録簿に保存するツール注釈の型）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/api/src/main/java/com/alibaba/nacos/api/ai/model/mcp/McpToolAnnotations.java#L19-L27
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/api/src/main/java/com/alibaba/nacos/api/ai/model/mcp/McpToolAnnotations.java
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: McpToolAnnotations.java L25-L26（クラスの Javadoc。L19-L27）
- **原文**:

> Clients should never make tool use decisions based on ToolAnnotations * received from untrusted servers.

- **日本語**: クライアントは、信頼できないサーバーから受け取った ToolAnnotations にもとづいてツールの使い方を決めてはならない。
- **どう使っているか**: 登録簿の型の説明（Javadoc）に、仕様の『注釈はヒントにすぎず、信頼できないサーバーの注釈でツールの使い方を決めるな』という注意をそのまま写している。Javadoc 自体は登録簿が注釈をどう使うかは書いていない。GitHub コード検索（default branch の索引）では readOnlyHint / getReadOnlyHint が出るのはこの型・テスト・コンソール UI・locale だけで、サーバー側で注釈を検証や判断に使う箇所は見つからなかった（検索の範囲で）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、25-26 行（取得 2026-10-02T22:11:31Z、sha256 216fce46a6c5…）
- **補足**: Javadoc の文面は MCP 仕様（schema.ts の ToolAnnotations）の注意書きとほぼ同じ。登録簿が保存する注釈の出どころ（サーバー作者か、コンソールで手入力した管理者か）は区別していない（型にその欄がない）。 usage_ja の『登録簿自身が注釈を検証したり判断に使ったりはしない』は引用からは言えない（引用はクライアントへの注意の写し）。GitHub コード検索（repo:alibaba/nacos, readOnlyHint 11 件 / getReadOnlyHint 2 件）の範囲での不在と書き換えた。索引は default branch で、pin した commit そのものではない。

<a id="g-g2-registries-marketplaces-02"></a>
#### G2RM-02 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: McpToolAnnotations.java（登録簿に保存するツール注釈の型）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/api/src/main/java/com/alibaba/nacos/api/ai/model/mcp/McpToolAnnotations.java#L31-L64
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/api/src/main/java/com/alibaba/nacos/api/ai/model/mcp/McpToolAnnotations.java
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: McpToolAnnotations.java L41（フィールド定義 L31-L64）
- **原文**:

> private Boolean readOnlyHint;

- **日本語**: private Boolean readOnlyHint;（読み取り専用ヒントを Boolean 型で持つ。null＝未宣言を表せる）
- **どう使っているか**: 登録簿（レジストリ）が MCP サーバーのツール定義（McpTool の annotations 欄、McpTool.java L47）と一緒に title と 4 つのヒントを保存する。値はラッパー型 Boolean なので『未宣言（null）』と『false』を区別して保持できる。どの API で外部に返すか・null をどう直列化するかは確かめていない（不明）。
- **扱う宣言**: title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、41 行（取得 2026-10-02T22:11:31Z、sha256 216fce46a6c5…）
- **補足**: 同じ型に destructiveHint（L49）・idempotentHint（L57）・openWorldHint（L64）があり、destructiveHint と idempotentHint の Javadoc には『readOnlyHint == false のときだけ意味がある』と仕様どおりに書かれている（L46, L54）。Nacos はこれまでの final_*.json / find_G2_*.json に出ていない。 『API で配る』は型定義からは言えないので『保存する』に弱め、配信経路と null の直列化は不明とした。McpTool.java（同 commit）に annotations 欄があることは raw で確認。

<a id="g-g2-registries-marketplaces-03"></a>
#### G2RM-03 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: ToolDetail.tsx（新コンソールのツール詳細表示）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/pages/newMcpServer/tool-manager/ToolDetail.tsx#L107-L126
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/pages/newMcpServer/tool-manager/ToolDetail.tsx
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: console-ui-next/src/pages/newMcpServer/tool-manager/ToolDetail.tsx L120（Annotations 節 L107-L126。表示条件 L28-L34）
- **原文**:

> .filter(([, val]) => val !== undefined)

- **日本語**: 値が undefined（未宣言）のヒントは一覧から外す。
- **どう使っているか**: 登録簿の管理画面でツールの注釈を『Read-Only / Destructive Action / Idempotent / Open World』の行として表示する。true はチェック印、false はバツ印。宣言されていないヒントは行ごと出さない（仕様の既定値を補って見せることはしない）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、120 行（取得 2026-10-02T22:12:55Z、sha256 79484a182eca…）
- **補足**: 4 つとも未宣言なら Annotations 節そのものを出さない（L29-L34 の hasAnnotations）。新コンソールのツール一覧（console-ui-next/src/components/ai/mcp/McpToolList.tsx L643-L662）も同じ作りで、こちらは title も出す。表示は利用者（管理者）向けの情報で、承認や絞り込みには使っていない（コード上でそれらの判定に使う箇所は見つからない＝ grep の範囲で）。

<a id="g-g2-registries-marketplaces-04"></a>
#### G2RM-04 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: ShowTools.js（旧コンソールのツール表示）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui/src/pages/AI/McpDetail/ShowTools.js#L596-L648
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui/src/pages/AI/McpDetail/ShowTools.js
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: console-ui/src/pages/AI/McpDetail/ShowTools.js L628（Annotations 表示 L596-L648）
- **原文**:

> tool.annotations.destructiveHint ? 'red' : 'green'

- **日本語**: destructiveHint が真なら赤、そうでなければ（未宣言を含めて）緑で表示する。
- **どう使っているか**: 旧コンソールは annotations オブジェクトがあれば 4 つのヒントを必ず Yes / No で表示する。値が無いヒントも『No』と出るため、destructiveHint 未宣言のツールが緑の『Destructive: No』、openWorldHint 未宣言が『Open World: No』に見える。仕様の既定値（未宣言なら destructive=true, openWorld=true）と逆向きの見せ方。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、628 行（取得 2026-10-02T22:11:32Z、sha256 d50be670e4ea…）
- **補足**: 誤 clear（安全側でない）方向の表示上の既定。readOnlyHint の未宣言 → No は仕様の既定（false）と一致する。annotations オブジェクト自体が無いツールでは節ごと表示しない（L597）。新コンソール（ToolDetail.tsx）では未宣言を表示しないよう変わっている。

<a id="g-g2-registries-marketplaces-05"></a>
#### G2RM-05 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: ToolEditorDialog.tsx（新コンソールのツール編集。登録簿への手入力）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/pages/newMcpServer/tool-manager/ToolEditorDialog.tsx#L141-L146
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/pages/newMcpServer/tool-manager/ToolEditorDialog.tsx
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: console-ui-next/src/pages/newMcpServer/tool-manager/ToolEditorDialog.tsx L143-L146（初期値 L66-L69, L90-L93）
- **原文**:

> if (readOnlyHint) annotations.readOnlyHint = true; if (destructiveHint) annotations.destructiveHint = true; if (idempotentHint) annotations.idempotentHint = true; if (openWorldHint) annotations.openWorldHint = true;

- **日本語**: チェックが入ったヒントだけを true として書き込む（チェックなし＝ false は書き込まず、キーごと省く）。
- **どう使っているか**: 管理者が新コンソールでツールを登録・編集するとき、ヒントはスイッチ（新規の初期値はすべてオフ）で入力する。保存時は true のものだけを書き、false は省略する（どれも true でなく title も空なら annotations 自体を付けない、L156）。そのため destructiveHint:false や openWorldHint:false を明示して登録できない。仕様の既定に従うクライアントは、これを未宣言として destructive=true, openWorld=true と読む。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、143-146 行（取得 2026-10-02T22:11:31Z、sha256 914b6cb71652…）
- **補足**: 既存ツールを開くと `tool.annotations?.destructiveHint || false` で読み込む（L91）ので、上流が destructiveHint:false を明示していたツールでも、この画面で保存し直すと false が消えて『未宣言』になる（コードからの推論。実機では未確認）。方向としては保守側（クライアントは destructive とみなす）に倒れる。 新コンソールの編集画面は、旧コンソールと違って readOnlyHint がオンでも destructiveHint / idempotentHint を無効にしない（L297-L309 は 4 つを同じスイッチで並べるだけ）。 『チェックボックス』は実際は Switch 部品なので直した。『受け取ったクライアントは仕様の既定で読む』はクライアントの挙動の断定なので『仕様の既定に従うクライアントは』に弱めた。annotations が空なら省く点（L156）と readOnly 時に他の欄を無効にしない点を追記。

<a id="g-g2-registries-marketplaces-06"></a>
#### G2RM-06 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: AnnotationsEditor.js（旧コンソールのツール注釈エディタ）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui/src/pages/AI/McpDetail/CreateTools/AnnotationsEditor.js#L15-L135
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui/src/pages/AI/McpDetail/CreateTools/AnnotationsEditor.js
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: console-ui/src/pages/AI/McpDetail/CreateTools/AnnotationsEditor.js L74（初期値 L18-L26、readOnly 時の無効化 L78, L103）
- **原文**:

> help={locale?.destructiveHintHelp || 'If true, the tool may perform destructive updates (Default: true)'}

- **日本語**: Destructive 欄の説明：『true なら、このツールは破壊的な更新をするかもしれない（既定：true）』。
- **どう使っているか**: 旧コンソールは仕様の既定値（readOnly=false, destructive=true, idempotent=false, openWorld=true）を初期値に入れ、各欄の説明に既定値を書く。readOnlyHint を Yes にすると destructiveHint と idempotentHint の入力を無効にする（仕様の『readOnlyHint == false のときだけ意味がある』に沿う）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、74 行（取得 2026-10-02T22:11:32Z、sha256 582a97dc3a45…）
- **補足**: 新コンソール（ToolEditorDialog.tsx、G2_registries_marketplaces-05）は初期値がすべて false で false を書かない、と既定の扱いが旧コンソールと食い違う。旧コンソールの保存側（CreateTools/index.js）は、既存ツールを開くとき未宣言を仕様の既定で埋め（L205-L208、例 `destructiveHint: annotations?.destructiveHint ?? true`）、保存時は undefined でない値を false も含めて書く（L292-L313）。旧コンソールの locale（console-ui/src/locales/en-US.js, zh-CN.js）には destructiveHintHelp のキーが無いので、この英語の既定文がそのまま説明として出る。どちらの UI が使われるかは Nacos の版・設定による（不明）。 旧コンソールの保存ロジック（index.js L205-L208 / L292-L313。L206 を verify_quote.py で exact 確認）と、help 文が locale に無く既定文がそのまま出ることを確かめて notes に追記。usage_ja の内容は正しい。

<a id="g-g2-registries-marketplaces-07"></a>
#### G2RM-07 Alibaba（Nacos プロジェクト） — Nacos MCP Registry（Nacos 3.x の AI / MCP サーバー管理。公式 MCP Registry API 互換の登録簿とコンソール）

- **資料**: en-US.json（新コンソールの英語ラベル）（サーバのソースコード）
- **URL**: https://github.com/alibaba/nacos/blob/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/locales/en-US.json#L605-L630
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/alibaba/nacos/1b6309f5086c163a1ff9c0469fabd4494ec09093/console-ui-next/src/locales/en-US.json
- **版**: alibaba/nacos commit 1b6309f（2026-10-02 の HEAD）
- **書いてある場所**: console-ui-next/src/locales/en-US.json L623-L626（mcp.* のラベル L605-L630）
- **原文**:

> "readOnlyHint": "Read-Only", "readOnlyHintDesc": "Whether this tool only performs read operations", "destructiveHint": "Destructive Action", "destructiveHintDesc": "Whether this tool may perform destructive operations",

- **日本語**: readOnlyHint の表示名は『Read-Only』で説明は『このツールが読み取り操作だけを行うか』。destructiveHint の表示名は『Destructive Action』で説明は『このツールが破壊的な操作をするかもしれないか』。
- **どう使っているか**: 登録簿の画面でヒントに付ける人間向けの名前と説明。idempotentHint は『Idempotent』、openWorldHint は『Open World』（L627-L630）。名前はツール詳細・一覧の表示に、説明（…Desc）は編集画面のスイッチの下に出る（ToolEditorDialog.tsx L305-L306）。旧コンソールと違い、説明文に既定値は書かれていない。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、623-626 行（取得 2026-10-02T22:11:35Z、sha256 f781f8053059…）
- **補足**: 中国語ラベル（console-ui-next/src/locales/zh-CN.json L623 以降、readOnlyHint は『只读提示』）も同じキーで定義されている（verifier が verify_quote.py で exact 確認）。 zh-CN.json の本文を照合した（未照合→確認）。説明文がどこに出るか（編集画面）と、既定値が書かれていない点を usage_ja に追記。

### Smithery — Smithery Registry API（GET /servers/{qualifiedName}）

<a id="g-g2-registries-marketplaces-08"></a>
#### G2RM-08 Smithery — Smithery Registry API（GET /servers/{qualifiedName}）

- **資料**: Get a server（API リファレンス、OpenAPI）（公式の文書）
- **URL**: https://smithery.ai/docs/api-reference/servers/get-a-server
- **照らし合わせた中身の URL**: https://smithery.ai/docs/api-reference/servers/get-a-server.md
- **版**: 2026-10-02 取得（.md 版。版表示なし）
- **書いてある場所**: get-a-server.md L223-L228（## OpenAPI 内の components.schemas.ServerTool）
- **原文**:

> required: - name - description - inputSchema additionalProperties: false id: ServerTool

- **日本語**: ServerTool の必須項目は name・description・inputSchema で、それ以外の項目は許さない（additionalProperties: false）。
- **どう使っているか**: Smithery の登録簿 API が返すツールの型に annotations の欄が無い（name / description / inputSchema / outputSchema のみ、追加の項目も禁止）。登録簿 API を経由すると注釈は落ちる。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、223-228 行（## OpenAPI）（取得 2026-10-02T22:11:39Z、sha256 e5bdfc136b09…）
- **補足**: 実データでも同じ：registry.smithery.ai/servers/notion を 2026-10-02 に取得すると、tools 14 件はどれも name / description / inputSchema だけで annotations が無い（linear 25 件・exa 2 件も同じ）。一方、同じサーバーの Smithery のウェブページのデータには annotations が入っている（次の項目）。C09_servers_gateways_security-44 は別の API（Connect の get-tool）で、そちらとは別物。 （verifier が 2026-10-02T20:3x に registry.smithery.ai/servers/notion を再取得：tools 14 件のキーは description / inputSchema / name だけ。） verifier の batch 実行では smithery.ai への接続が SSL エラー（curl 35）で失敗したが、単独の再実行で exact（L223-L228, ## OpenAPI）を確認。API 実データも再取得して notes の主張を確認した。

### Smithery — Smithery（ウェブのサーバー詳細ページ smithery.ai/servers/<name>）

<a id="g-g2-registries-marketplaces-09"></a>
#### G2RM-09 Smithery — Smithery（ウェブのサーバー詳細ページ smithery.ai/servers/<name>）

- **資料**: Notion — Smithery サーバー詳細ページ（第三者の記事）
- **URL**: https://smithery.ai/servers/notion
- **照らし合わせた中身の URL**: https://smithery.ai/server/notion
- **版**: 2026-10-02 取得
- **書いてある場所**: ページのデータ（<script> の中。本文テキストには無い）
- **原文**:

> "annotations":{"readOnlyHint":true,"openWorldHint":true,"idempotentHint":true,"destructiveHint":false}

- **日本語**: notion-search ツールの注釈として readOnlyHint=true, openWorldHint=true, idempotentHint=true, destructiveHint=false がページのデータに入っている。
- **どう使っているか**: Smithery のウェブのサーバーページ（ブラウザ向け HTML）は、各ツールの注釈（notion-search なら readOnlyHint=true, openWorldHint=true, idempotentHint=true, destructiveHint=false）をページのデータに持っている。この値がサーバーの tools/list から取り込んだものかは照合していない（不明）。画面にバッジとして描くかどうかは JavaScript で描画されるため curl では確かめられない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 script_only・1 か所（取得 2026-10-02T22:12:07Z、sha256 bf1887f34176…）
- **補足**: ページのデータ（script）の中にだけある。doc_type は製品の画面そのもの（文書ではない）で、選べる型に合うものが無いため third_party とした（Smithery 自身のページで、第三者の記事ではない）。第三者記事（linklyhq）の『Smithery and Cursor render them as badges』の一次資料はここでは得られない（描画を見られないため）。linear のページでも annotations（readOnlyHint, idempotentHint）が入っている。 ページのデータ（script）の中にだけある。notion のページでは 14 ツールすべてに 4 つのヒントが入っている（notion-update-page と notion-update-data-source が destructiveHint=true）。同じ URL を User-Agent なしの curl で取ると、エージェント向けの Markdown 版（2341 bytes、『## Tools (14)』の一覧）が返り、そこには注釈が無い。 『サーバーの tools/list の注釈をそのまま持っている』は出どころを照合していないので弱めた。URL は /server/notion → /servers/notion へ転送。ブラウザ UA の HTML にだけ注釈があり、UA なしで返る Markdown 版には無いことを確かめて追記。

### Kong — Kong AI Gateway — AI MCP Proxy プラグイン（REST API を MCP ツールに変換）

<a id="g-g2-registries-marketplaces-10"></a>
#### G2RM-10 Kong — Kong AI Gateway — AI MCP Proxy プラグイン（REST API を MCP ツールに変換）

- **資料**: Secure Internal MCP Gateway（cookbook）（公式の文書）
- **URL**: https://developer.konghq.com/cookbooks/secure-internal-mcp-gateway/
- **書いてある見出しへ直接**: https://developer.konghq.com/cookbooks/secure-internal-mcp-gateway/#configuration-details
- **版**: 2026-10-02 取得（ソース Kong/developer.konghq.com commit 068fd86 の app/_cookbooks/secure-internal-mcp-gateway.md L445）
- **書いてある場所**: Secure Internal MCP Gateway > How it works > AI MCP Proxy: REST-to-MCP conversion > Configuration details (#configuration-details)
- **原文**:

> annotations: MCP hints like read_only_hint and destructive_hint that help agents understand the tool’s behavior.

- **日本語**: annotations：read_only_hint や destructive_hint のような MCP のヒント。エージェントがツールの振る舞いを理解するのを助ける。
- **どう使っているか**: ゲートウェイの設定者が REST エンドポイントごとに read_only_hint / destructive_hint / title を書き、プラグインがそれを MCP の tools/list の annotations（readOnlyHint など）として出す。例では GET は read_only_hint: true、注文取消・在庫補充・顧客連絡先更新（POST/PUT）は destructive_hint: true。
- **扱う宣言**: readOnlyHint・destructiveHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Secure Internal MCP Gateway > How it works > AI MCP Proxy: REST-to-MCP conversion, tool aggregation, and ACL enforcement > Configuration details」（取得 2026-10-02T22:11:24Z、sha256 47900367a0a5…）
- **補足**: 宣言するのはサーバー作者でなくゲートウェイの設定者。同じページの例（ソース L937-L941）で tools/list の結果が readOnlyHint: true / destructiveHint: true として返る様子を示す。ゲートウェイ自身が注釈をアクセス制御に使う記述は無く、制御は acl（Consumer Group）で別に行う。C09 の checked_no_mention は AI MCP Proxy プラグインの文書ページ（developer.konghq.com/plugins/ai-mcp-proxy/）で語が無かったという記録で、この cookbook とスキーマ（次の項目）は別ページ。

### Kong — Kong AI Gateway — AI MCP Proxy プラグイン（設定スキーマ 3.16）

<a id="g-g2-registries-marketplaces-11"></a>
#### G2RM-11 Kong — Kong AI Gateway — AI MCP Proxy プラグイン（設定スキーマ 3.16）

- **資料**: AiMcpProxy.json（プラグイン設定の JSON スキーマ）（ゲートウェイの文書）
- **URL**: https://github.com/Kong/developer.konghq.com/blob/068fd86de44d2e1f2cc8ef2c92a06af5ed04484d/app/_schemas/gateway/plugins/3.16/AiMcpProxy.json#L541-L544
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Kong/developer.konghq.com/068fd86de44d2e1f2cc8ef2c92a06af5ed04484d/app/_schemas/gateway/plugins/3.16/AiMcpProxy.json
- **版**: Kong/developer.konghq.com commit 068fd86（Gateway 3.16 のスキーマ。3.10〜3.15 と AI Gateway policies 版にも同じ欄がある＝コード検索の結果）
- **書いてある場所**: app/_schemas/gateway/plugins/3.16/AiMcpProxy.json L541-L544（config.tools[].annotations）
- **原文**:

> "read_only_hint": { "description": "If true, the tool does not modify its environment", "type": "boolean" },

- **日本語**: read_only_hint：true なら、このツールは環境を変更しない。型は boolean。
- **どう使っているか**: プラグイン設定の tools[].annotations に destructive_hint / idempotent_hint / open_world_hint / read_only_hint / title を書ける。説明文は MCP 仕様の文言を短くしたもの。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、541-544 行（取得 2026-10-02T22:11:34Z、sha256 f9a39c279dae…）
- **補足**: 既定値はスキーマに書かれていない（不明）。Konnect の Catalog の MCP サーバー（API モデル CatalogMCPToolAnnotations、terraform-provider-konnect commit 4cecc82 の internal/sdk/models/shared/catalogmcptoolannotations.go L10-L19）にも同じ 5 項目がある（verifier が L19 の ReadOnlyHint 欄を verify_quote.py で exact 確認）。Konnect の MCP Registry 文書（developer.konghq.com/catalog/mcp-registry/）には語が無い（checked_no_mention）。 notes の terraform-provider-konnect の主張を verify_quote.py で照合した（L19 exact）。

### AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部）

<a id="g-g2-registries-marketplaces-12"></a>
#### G2RM-12 AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部）

- **資料**: arm-soc-migration/POWER.md（Arm 提供の power）（第三者の記事）
- **URL**: https://github.com/kirodotdev/powers/blob/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/arm-soc-migration/POWER.md#L89-L108
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/kirodotdev/powers/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/arm-soc-migration/POWER.md
- **版**: kirodotdev/powers commit fd30937
- **書いてある場所**: arm-soc-migration/POWER.md L107（mcp.json の例 L80-L93、説明 L96-L108）
- **原文**:

> - `autoApprove`: Tools that don't require user confirmation (safe read-only operations)

- **日本語**: autoApprove：ユーザーの確認が要らないツール（安全な読み取り専用の操作）。
- **どう使っているか**: Arm 作の power は、mcp.json の autoApprove にツール名（knowledge_base_search, sysreport_instructions）を並べ、それを『ユーザーの確認が要らない（安全な読み取り専用の操作）』と説明する。読み取り専用かどうかの判断は power の作者が名前の一覧で表しており、MCP の注釈には触れていない。Kiro 本体が別途 readOnlyHint を見るかはこの文書からは分からない（不明）。
- **扱う宣言**:  ／ **使い方の分類**: 確認を省く（自動で許可）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、107 行（# Test Docker is running）（取得 2026-10-02T22:11:32Z、sha256 2843834cab29…）
- **補足**: 同じ設定が power 本体の arm-soc-migration/mcp.json にも入っている。kirodotdev/powers（commit fd30937）の 31 の power のうち 12 の mcp.json に autoApprove があり、repo 全体で readOnlyHint の語は 0 件（verifier の grep）。Kiro の power 提出要件（kiro.dev/powers/submit）にも注釈の要件は無い（checked_no_mention）。doc_type は power 作者（Arm）の文書なので third_party とした。 『キュレーションされた power は…』と 1 件の例から一般化していた点、『サーバーの readOnlyHint は参照しない』と Kiro 本体の挙動を断定していた点を直した（文書は注釈に触れていないだけ）。repo 内の autoApprove の数と readOnlyHint 0 件を確かめて notes に追記。

<a id="g-g2-registries-marketplaces-13"></a>
#### G2RM-13 AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部）

- **資料**: stackgen/mcp.json（StackGen の power）（第三者の記事）
- **URL**: https://github.com/kirodotdev/powers/blob/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/stackgen/mcp.json#L12-L48
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/kirodotdev/powers/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/stackgen/mcp.json
- **版**: kirodotdev/powers commit fd30937
- **書いてある場所**: stackgen/mcp.json L23-L24（autoApprove 配列 L12-L48。destroy_deployment は L37）
- **原文**:

> "update_resource", "delete_resource",

- **日本語**: 自動承認の一覧に update_resource と delete_resource が入っている。
- **どう使っているか**: 登録簿に載った StackGen の power が、autoApprove に 35 個のツール名を並べている。その中には名前から見て変更・削除をするツール（update_resource, delete_resource, delete_env_profile, destroy_deployment, restore_snapshot, push-appstack-to-git など）も入っている。自動承認は注釈とは別の、作者が書いた名前の一覧で決まる。
- **扱う宣言**:  ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、23-24 行（取得 2026-10-02T22:11:38Z、sha256 bbf8436c5574…）
- **補足**: 各ツールが実際に破壊的か、StackGen のサーバーがどんな注釈を出すかは確かめていない（不明）。同じ repo の aws-agentcore/mcp.json（L7-L13）も manage_agentcore_runtime / manage_agentcore_gateway を autoApprove にしている。Kiro が power の autoApprove を利用者の確認なしにそのまま効かせるかは Kiro の文書で確かめていない（不明。C06 の Kiro の checked_no_mention を参照）。 『35 ツールすべて』はサーバーの全ツール数を確かめていないので『35 個のツール名』に直した（L13-L47 で 35 個）。『宣言（注釈）にも名前の意味にもよらず』は言い過ぎなので弱めた。

<a id="g-g2-registries-marketplaces-14"></a>
#### G2RM-14 AWS（Kiro） — Kiro powers 登録簿（kirodotdev/powers。kiro.dev/powers に載る power の一部）

- **資料**: power-builder/skills/migrate-plugin/SKILL.md（power を Agent Plugins 形式へ移す手順）（公式の文書）
- **URL**: https://github.com/kirodotdev/powers/blob/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/power-builder/skills/migrate-plugin/SKILL.md#L385-L390
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/kirodotdev/powers/fd309373c5fa99d33e9d578ff777ea8aac93ce9c/power-builder/skills/migrate-plugin/SKILL.md
- **版**: kirodotdev/powers commit fd30937
- **書いてある場所**: power-builder/skills/migrate-plugin/SKILL.md L389（### Issue: mcp.json has fields not in the spec。同じ指示が L244-L254 にも）
- **原文**:

> Remove Kiro-specific fields (`disabled`, `autoApprove`, `disabledTools`) from mcp.json. These have no equivalent in the plugin format.

- **日本語**: Kiro 固有の項目（disabled, autoApprove, disabledTools）を mcp.json から消す。これらはプラグイン形式に対応する項目が無い。
- **どう使っているか**: Kiro チームが書いた移行手順（migrate-plugin スキル）は、power を Agent Plugins 形式に移すとき mcp.json から autoApprove を消すよう指示する。そのため名前による自動承認はプラグイン形式には運べない。移した後に自動承認を何で決めるか（注釈を使うのか）は書かれていない（不明）。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、389 行（### Issue: mcp.json has fields not in the spec）（取得 2026-10-02T22:11:34Z、sha256 eb6af4d46646…）
- **補足**: kiro.dev/powers/submit は『Agent Plugins format で作って提出せよ』と求めている（2026-10-02 取得）。 主語を『Kiro が移すと』から、Kiro チーム作の移行手順（metadata.author: Kiro Team）が power 作者に指示する、に直した。

### CorpusIQ（第三者） — MCP Directory Submission Guide - 2026（第三者のディレクトリ掲載ガイド）

<a id="g-g2-registries-marketplaces-15"></a>
#### G2RM-15 CorpusIQ（第三者） — MCP Directory Submission Guide - 2026（第三者のディレクトリ掲載ガイド）

- **資料**: MCP Directory Submission Guide - 2026（第三者の記事）
- **URL**: https://www.corpusiq.io/docs/hermes/mcp/directories/submission-guide-2026
- **書いてある見出しへ直接**: https://www.corpusiq.io/docs/hermes/mcp/directories/submission-guide-2026#what-makes-a-listing-stick
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP Directory Submission Guide - 2026 > What makes a listing stick (#what-makes-a-listing-stick)
- **原文**:

> Read-only posture. Servers with readOnlyHint annotations are easier to approve and safer to recommend.

- **日本語**: 読み取り専用の姿勢。readOnlyHint 注釈を付けたサーバーは承認されやすく、推薦もしやすい。
- **どう使っているか**: 第三者のガイドが『readOnlyHint があるとディレクトリで承認されやすい』と書いている。どのディレクトリの規則かは示していない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Directory Submission Guide - 2026¶ > What makes a listing stick¶」（取得 2026-10-02T22:11:42Z、sha256 a7176acd24af…）
- **補足**: 一次資料の裏付けなし。この調査で確かめたディレクトリ（Cline Marketplace・GitHub MCP Registry・Cursor Marketplace・Kiro powers・Gemini CLI 拡張ギャラリー・LobeHub・mcpmarket.com・mcp.directory・Smithery の公開文書）の掲載要件には注釈の要件が無かった（checked_no_mention）。注釈を要件にしているのは既に記録済みの Anthropic Connectors Directory（C04）と OpenAI の Apps 提出（C05）。WebSearch の要約が言う『Cline の掲載に title / readOnlyHint / destructiveHint / openWorldHint が必須』『Smithery と Cursor がバッジ表示』の出どころは linklyhq.com の記事と見られるが、取得できなかった（unreachable）。

### ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む）

<a id="g-g2-registries-marketplaces-16"></a>
#### G2RM-16 ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む）

- **資料**: config.py（MCP 呼び出しの審査モード）（クライアントのソースコード）
- **URL**: https://github.com/modelscope/leapflow/blob/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/config.py#L146-L155
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelscope/leapflow/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/config.py
- **版**: modelscope/leapflow commit 401f1c2（README の最新は v0.2.0, 2026-09-15）
- **書いてある場所**: src/leapflow/config.py L149（モードの説明 L146-L155）
- **原文**:

> #   mutating_only -- assess every tool that does not declare readOnlyHint (default)

- **日本語**: mutating_only（既定）：readOnlyHint を宣言していないツールはすべて審査する。
- **どう使っているか**: MCP 呼び出しの審査モードは 3 つ。mutating_only（既定）は readOnlyHint を宣言しないツールを全部審査、always は宣言された読み取りも含めて全部を審査・監査、off は審査なし（プロセスごとに 1 回だけ記録）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を求める・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、149 行（# Directory creation is owned by PathLayout/ProfileLayout.）（取得 2026-10-02T22:11:33Z、sha256 d2865d8d371e…）
- **補足**: カテゴリ（レジストリ）外の追加。ModelScope 系のクライアントで、他の final_*.json に出ていない。実装（src/leapflow/cli/context.py L916-L917）では、既定の mutating_only のとき readOnlyHint を宣言したツールは審査器（orchestrator）を通らずにそのまま許可される。設定キーは mcp.approval_mode（環境変数 LEAPFLOW_MCP_APPROVAL_MODE でも指定でき、不正な値は mutating_only に戻す、config.py L1230-L1238）。 mutating_only で宣言された読み取りが審査そのものを飛ばすこと（context.py L916-L917、verify_quote.py で exact 確認）を notes に追記。

<a id="g-g2-registries-marketplaces-17"></a>
#### G2RM-17 ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む）

- **資料**: config.py（MCP 呼び出しの審査モード）（クライアントのソースコード）
- **URL**: https://github.com/modelscope/leapflow/blob/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/config.py#L152-L155
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelscope/leapflow/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/config.py
- **版**: modelscope/leapflow commit 401f1c2（README の最新は v0.2.0, 2026-09-15）
- **書いてある場所**: src/leapflow/config.py L153-L155
- **原文**:

> A declared # read is assessed LOW and auto-allowed on risk, so the practical difference between # the first two modes is audit coverage rather than prompt frequency.

- **日本語**: 宣言された読み取りは LOW と評価され、リスクの点で自動許可される。そのため 2 つのモードの実際の違いは、確認の回数ではなく監査の範囲である。
- **どう使っているか**: readOnlyHint: true を宣言したツールは確認を出さずに実行される。既定の mutating_only では審査そのものを飛ばし（cli/context.py L916-L917）、always では審査してリスク LOW（score 0.25、security/risk.py L492-L494）となり、利用者の方針ルールが先に当たらない限り policy.py L67 で ALLOW（low_risk）になる。サーバー自身の宣言をそのまま信じる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、153-155 行（# Directory creation is owned by PathLayout/ProfileLayout.）（取得 2026-10-02T22:11:33Z、sha256 d2865d8d371e…）
- **補足**: security/risk.py L477-L482 は、これを『プラグインの宣言を信じるのと同じく、サーバー自身の契約として尊重する』と理由づけている（G2_registries_marketplaces-19）。allow_permanent（利用者が一度だけ信頼を表明する）も別にある（L484 以降）。 引用の『LOW と評価され自動許可』は always モードで審査に回ったときの話で、既定の mutating_only では評価も監査もされない。 引用（config.py のコメント）だけだと『審査して LOW → 自動許可』に読めるが、既定モードでは審査器を通らない。両モードの経路をコードで確かめ（context.py L916-L917、risk.py L492-L494、policy.py L67 を verify_quote.py で exact）usage_ja を直した。

<a id="g-g2-registries-marketplaces-18"></a>
#### G2RM-18 ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む）

- **資料**: mcp_manager.py（_read_only_hint）（クライアントのソースコード）
- **URL**: https://github.com/modelscope/leapflow/blob/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/platform/mcp_manager.py#L45-L59
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelscope/leapflow/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/platform/mcp_manager.py
- **版**: modelscope/leapflow commit 401f1c2（README の最新は v0.2.0, 2026-09-15）
- **書いてある場所**: src/leapflow/platform/mcp_manager.py L50-L51（関数 L45-L59）
- **原文**:

> Absence yields the guarded answer, never the permissive one.

- **日本語**: （注釈が）無いときは守りの側の答えを返し、許す側の答えは決して返さない。
- **どう使っているか**: annotations が無い・readOnlyHint が無い・true 以外のときは read_only=False として扱う（`return hint is True`）。dict 形式の注釈にも対応する。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、50-51 行（# Copyright (c) Alibaba, Inc. and its affiliates.）（取得 2026-10-02T22:11:36Z、sha256 55d975bf404b…）
- **補足**: McpToolSchema.read_only の既定も False（L70-L76）。read_only が True のツールは、ツール定義のメタデータで risk_level=read_only, requires_approval=False になり、False のツールは risk_level=external, requires_approval=True, effect_scope=external, mutates_state=True になる（L96-L112）。 read_only の値が下流のメタデータにどう効くか（mcp_manager.py L96-L112）を確かめて notes に追記。

<a id="g-g2-registries-marketplaces-19"></a>
#### G2RM-19 ModelScope（Alibaba） — LeapFlow（modelscope/leapflow。エージェント枠組み、MCP クライアントを含む）

- **資料**: risk.py（MCP 呼び出しのリスク評価）（クライアントのソースコード）
- **URL**: https://github.com/modelscope/leapflow/blob/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/security/risk.py#L477-L486
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelscope/leapflow/401f1c23f3359a34a1d0767caa63bea8f852b6b5/src/leapflow/security/risk.py
- **版**: modelscope/leapflow commit 401f1c2（README の最新は v0.2.0, 2026-09-15）
- **書いてある場所**: src/leapflow/security/risk.py L482（説明 L477-L486）
- **原文**:

> Absence of the hint is not a claim of read-only, so it stays at the higher tier.

- **日本語**: ヒントが無いことは読み取り専用の主張ではないので、高い段階のままにする。
- **どう使っているか**: リスク評価で、readOnlyHint を宣言したサーバーのツールは読み取りとして低い段階に、宣言の無いツールは高い段階に置く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 危険度を付ける・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、482 行（# Copyright (c) Alibaba, Inc. and its affiliates.）（取得 2026-10-02T22:11:39Z、sha256 de775deaf0dd…）
- **補足**: L479-L481 は、宣言された読み取りを書き込み扱いすると文書検索まで確認待ちになって使えなくなる、という理由で宣言を尊重すると書く。宣言が偽（実際は書き込む）の場合の扱いは書かれていない。 宣言の無いツールは HIGH（score 0.7、reasons mcp_tool_undeclared_effect）となり、方針では ASK（確認）に回る。確認の既定の選択肢は deny（orchestrator.py L146）。ただし Guardian（LLM）が先に自動で決めることがある（orchestrator.py L129-L130）。 宣言なしのツールの行き先（HIGH → ASK、既定の選択肢 deny、Guardian の自動判定）をコードで確かめて notes に追記。

---

[← 付録 G-9 サーバの作者と、業務 SaaS のホスト](appendix-g-9.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-11 WebMCP →](appendix-g-11.md)
