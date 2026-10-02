[← 付録 G-8 エージェントの枠組み・利用者向けアプリ・モデルの API](appendix-g-8.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-10 ゲートウェイ・実行基盤・宣言を検査する道具・登録所 →](appendix-g-10.md)

---

# 付録 G-9 サーバの作者と、業務 SaaS のホスト

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-9-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [G3VS-01](#g-g3-vendor-servers-01) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-02](#g-g3-vendor-servers-02) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [G3VS-03](#g-g3-vendor-servers-03) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバの文書 | ツールを絞る・隠す | [確認] |
| [G3VS-04](#g-g3-vendor-servers-04) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバのソースコード | そのまま渡す・見せる・宣言が無いときの扱い | [確認] |
| [G3VS-05](#g-g3-vendor-servers-05) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバのソースコード | 確認を求める・規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [G3VS-06](#g-g3-vendor-servers-06) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバの文書 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G3VS-07](#g-g3-vendor-servers-07) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバの文書 | 宣言を検査する・ツールを絞る・隠す | [確認] |
| [G3VS-08](#g-g3-vendor-servers-08) | Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go） | サーバの文書 | 作者への書き方の案内・宣言を書くことを求める | [確認] |
| [G3VS-09](#g-g3-vendor-servers-09) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバの文書 | そのまま渡す・見せる・その他 | [確認] |
| [G3VS-10](#g-g3-vendor-servers-10) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバの文書 | その他 | [確認] |
| [G3VS-11](#g-g3-vendor-servers-11) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバの文書 | 作者への書き方の案内 | [確認] |
| [G3VS-12](#g-g3-vendor-servers-12) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバのソースコード | その他 | [確認] |
| [G3VS-13](#g-g3-vendor-servers-13) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバのソースコード | 宣言が無いときの扱い・そのまま渡す・見せる・危険度を付ける | [確認] |
| [G3VS-14](#g-g3-vendor-servers-14) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | サーバのソースコード | 宣言が無いときの扱い・危険度を付ける | [確認] |
| [G3VS-15](#g-g3-vendor-servers-15) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | リリースノート | その他・宣言が無いときの扱い | [確認] |
| [G3VS-16](#g-g3-vendor-servers-16) | Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript） | リリースノート | その他 | [確認] |
| [G3VS-17](#g-g3-vendor-servers-17) | Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript） | サーバのソースコード | その他・ツールを絞る・隠す | [確認] |
| [G3VS-18](#g-g3-vendor-servers-18) | Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript） | サーバのソースコード | ツールを絞る・隠す・危険度を付ける | [確認] |
| [G3VS-19](#g-g3-vendor-servers-19) | Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript） | サーバのソースコード | 危険度を付ける・その他 | [確認] |
| [G3VS-20](#g-g3-vendor-servers-20) | Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript） | サーバの文書 | ツールを絞る・隠す | [確認] |
| [G3VS-21](#g-g3-vendor-servers-21) | SonarSource — SonarQube MCP Server（Java） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-22](#g-g3-vendor-servers-22) | SonarSource — SonarQube MCP Server（Java） | サーバのソースコード | その他 | [確認] |
| [G3VS-23](#g-g3-vendor-servers-23) | SonarSource — SonarQube MCP Server（Java） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-24](#g-g3-vendor-servers-24) | SonarSource — SonarQube MCP Server（Java） | サーバの文書 | ツールを絞る・隠す | [確認] |
| [G3VS-25](#g-g3-vendor-servers-25) | Buildkite — buildkite-mcp-server（Go） | サーバのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [G3VS-26](#g-g3-vendor-servers-26) | Buildkite — buildkite-mcp-server（Go） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-27](#g-g3-vendor-servers-27) | PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-28](#g-g3-vendor-servers-28) | PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript） | サーバのソースコード | 宣言が無いときの扱い・そのまま渡す・見せる | [確認] |
| [G3VS-29](#g-g3-vendor-servers-29) | PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript） | サーバのソースコード | その他 | [確認] |
| [G3VS-30](#g-g3-vendor-servers-30) | PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript） | サーバのソースコード | ツールを絞る・隠す・その他 | [確認] |
| [G3VS-31](#g-g3-vendor-servers-31) | LangChain — LangGraph Agent Server（langgraph-api 0.15.1）の /mcp エンドポイント | サーバのソースコード | その他 | [確認] |
| [G3VS-32](#g-g3-vendor-servers-32) | HashiCorp（IBM） — terraform-mcp-server（Go） | サーバのソースコード | その他・ツールを絞る・隠す | [確認] |
| [G3VS-33](#g-g3-vendor-servers-33) | HashiCorp（IBM） — terraform-mcp-server（Go） | サーバのソースコード | ツールを絞る・隠す | [確認] |
| [G3VS-34](#g-g3-vendor-servers-34) | HashiCorp（IBM） — terraform-mcp-server（Go） | サーバのソースコード | その他 | [確認] |
| [G3VS-35](#g-g3-vendor-servers-35) | HashiCorp（IBM） — terraform-mcp-server（Go） | サーバの文書 | ツールを絞る・隠す | [確認] |
| [G3VS-36](#g-g3-vendor-servers-36) | Netlify — Netlify MCP Server（netlify-mcp、TypeScript） | サーバのソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [G3VS-37](#g-g3-vendor-servers-37) | Netlify — Netlify MCP Server（netlify-mcp、TypeScript） | サーバのソースコード | その他 | [確認] |
| [G3VS-38](#g-g3-vendor-servers-38) | Okta（Auth0） — auth0-mcp-server（TypeScript） | サーバのソースコード | ツールを絞る・隠す・使わない・読まない | [確認] |
| [G3VS-39](#g-g3-vendor-servers-39) | dbt Labs — dbt-mcp（Python） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [G3VS-40](#g-g3-vendor-servers-40) | dbt Labs — dbt-mcp（Python） | サーバのソースコード | その他 | [確認] |
| [G3VS-41](#g-g3-vendor-servers-41) | Couchbase — mcp-server-couchbase（Python） | サーバのソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [G3VS-42](#g-g3-vendor-servers-42) | Couchbase — mcp-server-couchbase（Python） | サーバのソースコード | 使わない・読まない・ツールを絞る・隠す | [確認] |
| [G3VS-43](#g-g3-vendor-servers-43) | Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript） | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [G3VS-44](#g-g3-vendor-servers-44) | Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript） | サーバのソースコード | その他 | [確認] |
| [G3VS-45](#g-g3-vendor-servers-45) | Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript） | サーバのソースコード | その他 | [確認] |
| [G3VS-46](#g-g3-vendor-servers-46) | Microsoft（Azure） — AKS-MCP（Azure/aks-mcp、Go） | サーバのソースコード | その他 | [確認] |
| [G3VS-47](#g-g3-vendor-servers-47) | DigitalOcean — mcp-digitalocean（digitalocean-labs、Go） | サーバのソースコード | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [G3VS-48](#g-g3-vendor-servers-48) | Google Cloud — gke-mcp（GoogleCloudPlatform/gke-mcp、Go） | サーバのソースコード | その他 | [確認] |
| [G3VS-49](#g-g3-vendor-servers-49) | Docker — Docker Hub MCP Server（docker/hub-mcp、TypeScript） | サーバのソースコード | 表示（印・名前） | [確認] |
| [G3VS-50](#g-g3-vendor-servers-50) | Harness — Harness MCP Server（harness/mcp-server、TypeScript） | サーバのソースコード | 使わない・読まない | [確認] |
| [G3VS-51](#g-g3-vendor-servers-51) | monday.com — monday.com MCP（mondaycom/mcp、TypeScript） | サーバの文書 | 作者への書き方の案内 | [確認] |
| [G3VS-52](#g-g3-vendor-servers-52) | monday.com — monday.com MCP（mondaycom/mcp、TypeScript） | サーバのソースコード | 使わない・読まない・ツールを絞る・隠す | [確認] |
| [G3VS-53](#g-g3-vendor-servers-53) | Atlassian — Atlassian Rovo MCP Server（リモート、mcp.atlassian.com） | サーバの文書 | その他 | [確認] |
| [G3VS-54](#g-g3-vendor-servers-54) | Atlassian — Atlassian Rovo MCP Server（リモート、mcp.atlassian.com） | サーバの文書 | ツールを絞る・隠す | [確認] |
| [G3SH-01](#g-g3-saas-hosts-01) | Slack (Salesforce) — Slackbot MCP client — Slack Marketplace の掲載要件 | 規約・審査の指針 | 宣言を書くことを求める・表示（印・名前）・作者への書き方の案内 | [確認] |
| [G3SH-02](#g-g3-saas-hosts-02) | Slack (Salesforce) — Slackbot MCP client | クライアントの文書 | 宣言が無いときの扱い・確認を求める | [確認] |
| [G3SH-03](#g-g3-saas-hosts-03) | Slack (Salesforce) — Slackbot MCP client | クライアントの文書 | 確認を求める | [確認] |
| [G3SH-04](#g-g3-saas-hosts-04) | Slack (Salesforce) — Slackbot MCP client（MCP Apps / rich responses） | クライアントの文書 | 作者への書き方の案内 | [確認] |
| [G3SH-05](#g-g3-saas-hosts-05) | Slack (Salesforce) — slack-samples/bolt-python-examples（Slackbot MCP client 向けサンプル） | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [G3SH-06](#g-g3-saas-hosts-06) | Notion Labs — Notion Custom Agents（MCP connections） | クライアントの文書 | 表示（印・名前）・信頼するなという注意 | [確認] |
| [G3SH-07](#g-g3-saas-hosts-07) | Notion Labs — Notion Custom Agents（MCP connections） | クライアントの文書 | 確認を求める | [確認] |
| [G3SH-08](#g-g3-saas-hosts-08) | Notion Labs — Notion Custom Agents（MCP connections） | クライアントの文書 | 確認を求める・その他 | [確認] |
| [G3SH-09](#g-g3-saas-hosts-09) | Notion Labs — Notion Custom Agents（MCP connections） | クライアントの文書 | 確認を求める・確認を省く（自動で許可）・その他 | [確認] |
| [G3SH-10](#g-g3-saas-hosts-10) | Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー） | サーバの文書 | 作者への書き方の案内・その他 | [未確認] |
| [G3SH-11](#g-g3-saas-hosts-11) | Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー） | サーバの文書 | その他 | [未確認] |
| [G3SH-12](#g-g3-saas-hosts-12) | Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー） | サーバの文書 | 作者への書き方の案内・宣言が無いときの扱い | [未確認] |
| [G3SH-13](#g-g3-saas-hosts-13) | Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー） | サーバの文書 | 信頼するなという注意・その他 | [未確認] |
| [G3SH-14](#g-g3-saas-hosts-14) | Salesforce — Salesforce Hosted MCP Servers | 公式ブログ | 作者への書き方の案内 | [未確認] |
| [G3SH-15](#g-g3-saas-hosts-15) | Salesforce — Salesforce Hosted MCP Servers | 公式ブログ | 信頼するなという注意・その他 | [未確認] |
| [G3SH-16](#g-g3-saas-hosts-16) | Salesforce — Slackbot MCP client（Salesforce の解説ブログ） | 公式ブログ | 確認を求める・その他 | [確認] |
| [G3SH-17](#g-g3-saas-hosts-17) | Salesforce — Agentforce MCP client（API Catalog への MCP サーバー登録）— forcedotcom/sf-skills の agentforce-generate skill | クライアントの文書 | その他 | [確認] |
| [G3SH-18](#g-g3-saas-hosts-18) | Salesforce — Agentforce MCP client — forcedotcom/sf-skills の agentforce-generate skill | クライアントの文書 | 表示（印・名前）・その他 | [確認] |
| [G3SH-19](#g-g3-saas-hosts-19) | HubSpot — HubSpot Breeze agents の MCP client — HubSpot Marketplace の MCP サーバー掲載要件 | 規約・審査の指針 | 宣言を書くことを求める・宣言を検査する・その他 | [確認] |
| [G3SH-20](#g-g3-saas-hosts-20) | Make (Celonis) — Make MCP toolboxes（Make のシナリオを MCP ツールとして公開するサーバー側機能） | サーバの文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [G3SH-21](#g-g3-saas-hosts-21) | Dust (dust-tt) — Dust（業務向けエージェント SaaS、MCP クライアント。OSS） | クライアントのソースコード | 使わない・読まない・宣言が無いときの扱い・確認を求める | [確認] |
| [G3SH-22](#g-g3-saas-hosts-22) | Dust (dust-tt) — Dust（client-side MCP server） | クライアントのソースコード | 使わない・読まない・宣言が無いときの扱い・その他 | [確認] |
| [G3SH-23](#g-g3-saas-hosts-23) | Dust (dust-tt) — Dust（リモート MCP サーバーのツール設定フォーム） | クライアントのソースコード | 使わない・読まない・宣言が無いときの扱い・その他 | [確認] |
| [G3SH-24](#g-g3-saas-hosts-24) | Atlassian — Atlassian Rovo（外部 MCP サーバーへのクライアント。Read-only MCP integrations） | クライアントの文書 | その他 | [確認] |
| [G3SH-25](#g-g3-saas-hosts-25) | Zapier — AI by Zapier（旧 Zapier Agents）のツール — Require approval before running | クライアントの文書 | その他 | [確認] |
| [G3SH-26](#g-g3-saas-hosts-26) | Zapier — Zapier MCP Client（Zap から外部 MCP サーバーのツールを呼ぶ統合、beta） | クライアントの文書 | その他 | [確認] |
| [G3SH-27](#g-g3-saas-hosts-27) | HubSpot — HubSpot Breeze agents の MCP client（Connected apps のツール権限） | クライアントの文書 | 表示（印・名前）・その他 | [確認] |
| [G3SH-28](#g-g3-saas-hosts-28) | Glean — Glean Assistant / Glean Agents（MCP host） | クライアントの文書 | 確認を求める・その他 | [確認] |
| [G3SH-29](#g-g3-saas-hosts-29) | Langdock — Langdock（業務向け AI プラットフォーム、MCP integration） | クライアントの文書 | その他 | [確認] |
| [G3SH-30](#g-g3-saas-hosts-30) | Atlassian — Rovo Dev CLI（MCP クライアント機能を持つ開発エージェント） | クライアントの文書 | 宣言が無いときの扱い・その他 | [確認] |
| [G3SH-31](#g-g3-saas-hosts-31) | ServiceNow — ServiceNow AI Agents（AI Agent Studio。MCP client を含む）— Fluent SDK の手引き | クライアントの文書 | その他 | [確認] |

この分冊の資料は 85 件で、うち [確認] は 79 件、[確認（調査時のみ）] は 0 件。

<a id="ag-9-1"></a>
## 資料カード

### Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

<a id="g-g3-vendor-servers-01"></a>
#### G3VS-01 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: pkg/config/config.go（設定項目の定義）（サーバのソースコード）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/config/config.go#L411-L412
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/config/config.go
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/config/config.go L411-412
- **原文**:

```
ReadOnly:           opt("read_only", false).reload().desc("Expose only tools annotated readOnlyHint=true"),
DisableDestructive: opt("disable_destructive", false).reload().desc("Disable tools annotated destructiveHint=true"),
```

- **日本語**: 設定 read_only は「readOnlyHint=true と注釈されたツールだけを出す」、disable_destructive は「destructiveHint=true と注釈されたツールを無効にする」。
- **どう使っているか**: サーバー自身の運用モード（read_only / disable_destructive）を、各ツールの注釈で決める。注釈がそのまま公開範囲の選別キーになる。
- **条件**: 既定はどちらも false。TOML 設定 read_only = true / disable_destructive = true（旧 CLI フラグ --read-only / --disable-destructive は廃止、docs/configuration-changes.md）。reload 可能。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、411-412 行（取得 2026-10-02T22:11:33Z、sha256 686568559c9a…）
- **補足**: github-mcp-server / Azure MCP / Supabase と同じ型（注釈で一覧を絞る）。

<a id="g-g3-vendor-servers-02"></a>
#### G3VS-02 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: pkg/mcp/mcp.go: isToolApplicable（サーバのソースコード）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/mcp/mcp.go#L69-L75
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/mcp/mcp.go
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/mcp/mcp.go L69-75
- **原文**:

```
func (c *Configuration) isToolApplicable(tool api.ServerTool) bool {
if c.ReadOnly.Get() && !ptr.Deref(tool.Tool.Annotations.ReadOnlyHint, false) {
return false
}
if c.DisableDestructive.Get() && ptr.Deref(tool.Tool.Annotations.DestructiveHint, false) {
return false
}
```

- **日本語**: read_only が有効で、ReadOnlyHint が（無ければ false とみなして）true でないツールは除く。disable_destructive が有効で、DestructiveHint が（無ければ false とみなして）true のツールは除く。
- **どう使っているか**: 欠落の扱いが非対称: readOnlyHint 欠落 → 読み取り専用ではない扱い（read_only では隠れる＝安全側）。destructiveHint 欠落 → 破壊的ではない扱い（disable_destructive では残る＝仕様の既定 true とは逆）。
- **条件**: read_only=true または disable_destructive=true のとき。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、69-75 行（取得 2026-10-02T22:11:40Z、sha256 b598059e7b52…）
- **補足**: ptr.Deref(x, false) で nil を false に倒す。仕様の destructiveHint 既定は true なので、disable_destructive 下で注釈なしの書き込みツールは残る（不明: 全ツールが DestructiveHint を明示しているかは数えていない）。read_only の拒否は一覧から外すだけでなく呼び出しも unknown tool で拒否される（pkg/mcp/mcp_tools_test.go 66-67 行 TestReadOnlyBlocksWriteToolInvocation。verifier が同 commit の clone で目視、verify_quote 未実行）。 notes の「未照合の付記」（テスト名と挙動）を clone で目視確認し、行番号を付けた。

<a id="g-g3-vendor-servers-03"></a>
#### G3VS-03 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: docs/configuration.md（設定リファレンス）（サーバの文書）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/docs/configuration.md#L433-L434
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/docs/configuration.md
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: docs/configuration.md L433-434（見出し: ### Access Control）
- **原文**:

```
| `read_only` | boolean | `false` | When `true`, only exposes tools annotated with `readOnlyHint=true`. Prevents any write operations on the cluster. |
| `disable_destructive` | boolean | `false` | When `true`, disables tools annotated with `destructiveHint=true` (delete, update operations). Has no effect when `read_only` is `true`. |
```

- **日本語**: read_only: true なら readOnlyHint=true のツールだけを出し、クラスタへの書き込みを防ぐ。disable_destructive: true なら destructiveHint=true のツール（削除・更新）を無効にする。read_only が true のときは効果なし。
- **どう使っているか**: 利用者向け文書が、読み取り専用モードを「注釈で一覧を絞ること」として説明し、それで書き込みを防ぐと書く。
- **条件**: 既定 false。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、433-434 行（### Access Control）（取得 2026-10-02T22:12:56Z、sha256 c7376f77bbda…）
- **補足**: 「Prevents any write operations」は注釈が正しいことが前提（宣言と実効の照合はしない）。

<a id="g-g3-vendor-servers-04"></a>
#### G3VS-04 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: pkg/mcp/tools_gosdk.go（go-sdk への変換）（サーバのソースコード）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/mcp/tools_gosdk.go#L57-L63
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/mcp/tools_gosdk.go
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/mcp/tools_gosdk.go L57-63
- **原文**:

```
Annotations: &mcp.ToolAnnotations{
Title:           tool.Tool.Annotations.Title,
ReadOnlyHint:    ptr.Deref(tool.Tool.Annotations.ReadOnlyHint, false),
DestructiveHint: tool.Tool.Annotations.DestructiveHint,
IdempotentHint:  ptr.Deref(tool.Tool.Annotations.IdempotentHint, false),
OpenWorldHint:   tool.Tool.Annotations.OpenWorldHint,
},
```

- **日本語**: tools/list に出す注釈: ReadOnlyHint と IdempotentHint は無ければ false にして出す。DestructiveHint と OpenWorldHint は内部の値（nil 可）をそのまま出す。
- **どう使っているか**: 内部定義の注釈をクライアントへ公開する。go-sdk の型に合わせ readOnly / idempotent は欠落を false で明示、destructive / openWorld は欠落のまま渡す（欠落を仕様の既定 true で読むかは受け手のクライアント次第）。
- **条件**: すべてのツール（go-sdk 経路）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、57-63 行（取得 2026-10-02T22:11:34Z、sha256 ebe482d284b2…）
- **補足**: 「クライアント側で仕様の既定 true が効く」は言い過ぎ（受け手次第）なので弱めた。

<a id="g-g3-vendor-servers-05"></a>
#### G3VS-05 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: pkg/confirmation/match.go: MatchToolLevelRules（サーバのソースコード）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/confirmation/match.go#L24-L27
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/pkg/confirmation/match.go
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/confirmation/match.go L24-27
- **原文**:

```
if r.Destructive != nil {
if destructiveHint == nil || *r.Destructive != *destructiveHint {
continue
}
```

- **日本語**: 確認ルールに destructive が指定されているとき、ツールの destructiveHint が無い（nil）か値が違えば、そのルールは当たらない。
- **どう使っているか**: サーバー側の確認（elicitation）ルールの入力に destructiveHint を使う。注釈が無いツールには destructive=true のルールが当たらない（確認が出ない）。
- **条件**: confirmation_rules に destructive = true などを書いたとき。クライアントが elicitation 非対応なら confirmation_fallback（既定 "allow"）で素通り。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、24-27 行（取得 2026-10-02T22:11:32Z、sha256 e0c7dba4e8b0…）

<a id="g-g3-vendor-servers-06"></a>
#### G3VS-06 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: docs/configuration.md「Confirmation Rules」（サーバの文書）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/docs/configuration.md#L798-L799
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/docs/configuration.md
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: docs/configuration.md L798-799（見出し: ### Confirmation Rules）
- **原文**:

> - **Tool-level** — matches on tool name or `DestructiveHint` annotation. Fires once before the tool handler runs.

- **日本語**: ツール単位の確認ルールは、ツール名か DestructiveHint 注釈で当たり、ハンドラ実行前に 1 回出る。
- **どう使っているか**: 利用者が「破壊的と注釈されたツールは実行前に確認」をサーバー側で設定できる。
- **条件**: confirmation_rules を設定したとき。例として `destructive = true` / message = "Destructive operation." が載る。クライアントが elicitation 非対応なら confirmation_fallback（既定 "allow"＝警告ログだけで実行）。同じ節に明記。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、798 行（### Confirmation Rules）（取得 2026-10-02T22:12:56Z、sha256 c7376f77bbda…）
- **補足**: url のアンカーを道具の行番号 798-799 に合わせた。 同じ節にある confirmation_fallback の既定 "allow"（elicitation 非対応クライアントでは確認なしで実行）が conditions に無かったので足した。

<a id="g-g3-vendor-servers-07"></a>
#### G3VS-07 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: evals/README.md「Read-only suite」（サーバの文書）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/evals/README.md#L209-L214
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/evals/README.md
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: evals/README.md L209-214（見出し: ## Read-only suite (`core-readonly`)）
- **原文**:

```
Note this suite intentionally does **not** cover write-blocking itself:
whether `read_only=true` actually rejects a write attempt (as opposed to just
hiding write tools from the tool list) is a deterministic property of the
server, not of model behavior, so it's covered by
`TestReadOnlyBlocksWriteToolInvocation` in `pkg/mcp/mcp_tools_test.go` instead
```

- **日本語**: この評価スイートは書き込みの阻止そのものは見ない。read_only=true が（一覧から隠すだけでなく）書き込みの試みを実際に拒むかはサーバーの決定的な性質なので、TestReadOnlyBlocksWriteToolInvocation で確かめる。
- **どう使っているか**: 注釈ベースの読み取り専用モードが「隠す」だけでなく「呼び出しを拒む」ことを単体テストで保証している、と作者が明言する。
- **条件**: 開発者向け。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、209-213 行（## Read-only suite (`core-readonly`)）（取得 2026-10-02T22:11:32Z、sha256 4d6edba740eb…）
- **補足**: 同ファイル 202-207 行: core-readonly スイートの全タスクが toolsNotUsed に pods_exec 等を入れ、pods_exec は CRUD の書き込みではないが pkg/toolsets/core/pods.go で DestructiveHint: true と注釈されているから含める、と書く（verifier が clone で目視、verify_quote 未実行）。 url のアンカーを道具の行番号 209-214 に合わせた。 notes の付記を clone で目視し、行番号と内容を正した。

<a id="g-g3-vendor-servers-08"></a>
#### G3VS-08 Red Hat（containers org） — kubernetes-mcp-server（Kubernetes / OpenShift 用 MCP サーバー、Go）

- **資料**: .agents/skills/toolset-design/SKILL.md（コーディングエージェント向けの設計ガイド）（サーバの文書）
- **URL**: https://github.com/containers/kubernetes-mcp-server/blob/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/.agents/skills/toolset-design/SKILL.md#L211-L218
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/containers/kubernetes-mcp-server/26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40/.agents/skills/toolset-design/SKILL.md
- **版**: containers/kubernetes-mcp-server@26eaf54c2a67fd4ea42657a83e6fd22aca4ccb40（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: .agents/skills/toolset-design/SKILL.md L211-218（見出し: ### Tool annotations）
- **原文**:

> Every tool must set appropriate annotations:
>
> - `ReadOnlyHint: true` for diagnostic/query tools
> - `DestructiveHint: true` for tools that delete or modify resources
> - `IdempotentHint: true` if repeated calls with same args have no additional effect
> - `OpenWorldHint: true` if the tool interacts with a live cluster (most tools)

- **日本語**: すべてのツールは適切な注釈を付けること: 診断・照会は ReadOnlyHint: true、削除・変更は DestructiveHint: true、同じ引数で繰り返しても影響がなければ IdempotentHint: true、実クラスタと関わるなら OpenWorldHint: true（ほとんどのツール）。
- **どう使っているか**: 新しいツールを書く（AI）作者への設定基準。「delete or modify resources」を DestructiveHint: true とする。仕様は「追加的な更新だけなら false」なので、既存資源の変更を destructive 側に置くのは仕様の定義と整合的（finder の「仕様より広い」は撤回）。
- **条件**: リポジトリ内の作者向け指示。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、211-216 行（### Tool annotations）（取得 2026-10-02T22:11:36Z、sha256 adaa834ce8e4…）
- **補足**: pkg/mcp/mcp_tools_test.go 37 行に readOnly と destructive の両立を禁じる検査（"Tool %s is read-only and destructive, which is not allowed"）がある（verifier が clone で目視、verify_quote 未実行）。 url のアンカーを道具の行番号 211-218 に合わせた。 usage_ja の「modify を含めるのは仕様より広い」は誤り。仕様（destructiveHint=false は additive updates のみ）に照らすと変更は destructive 側で整合的なので直した。notes のテストを clone で確認。

### Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

<a id="g-g3-vendor-servers-09"></a>
#### G3VS-09 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: MobileBuildMCP docs「MCP Protocol Support」> Tool annotations（サーバの文書）
- **URL**: https://www.mobilebuildmcp.com/docs/mcp-protocol-support
- **書いてある見出しへ直接**: https://www.mobilebuildmcp.com/docs/mcp-protocol-support#tool-annotations
- **版**: 2026-10-02 取得（sha256 dd59423686db）
- **書いてある場所**: MCP Protocol Support > Tool annotations（#tool-annotations）
- **原文**:

> MobileBuildMCP includes tool annotations in the MCP tools/list response. These are client hints, not security boundaries.

- **日本語**: MobileBuildMCP は tools/list に注釈を含める。これはクライアントへのヒントで、セキュリティ境界ではない。
- **どう使っているか**: tools/list に注釈を載せると宣言しつつ、境界ではないと明記する。同じ節は「title, readOnlyHint, destructiveHint, openWorldHint を全ツールに付け、idempotentHint はどのツールにも付けていない」と書く。
- **条件**: すべてのツール。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Protocol Support > Tool annotations」（取得 2026-10-02T22:12:09Z、sha256 dd59423686db…）
- **補足**: タスクに挙がっていた https://www.xcodebuildmcp.com/docs/mcp-protocol-support は 2026-10-02 時点でトップページ https://www.mobilebuildmcp.com/ へリダイレクトされ、同名の文書は www.mobilebuildmcp.com 側にある（プロジェクト改名。GitHub も getsentry/XcodeBuildMCP → getsentry/MobileBuildMCP で同じ HEAD）。 文書は idempotentHint を付けていないと書くが、同 commit の manifests/tools/toggle_software_keyboard.yaml と toggle_connect_hardware_keyboard.yaml は idempotentHint: false を持つ（文書と実装の小さな食い違い。clone で目視）。 同じ節が「idempotentHint はどのツールにも付けていない」と明記するので hints から idempotentHint を外し、usage_ja を「全ツールに 4 つ」に正した。

<a id="g-g3-vendor-servers-10"></a>
#### G3VS-10 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: MobileBuildMCP docs「MCP Protocol Support」> Tool annotations（注釈ごとの表）（サーバの文書）
- **URL**: https://www.mobilebuildmcp.com/docs/mcp-protocol-support
- **書いてある見出しへ直接**: https://www.mobilebuildmcp.com/docs/mcp-protocol-support#tool-annotations
- **版**: 2026-10-02 取得（sha256 dd59423686db）
- **書いてある場所**: MCP Protocol Support > Tool annotations（#tool-annotations）
- **原文**:

> Read only tools can be treated as lower risk, and clients may reduce extra confirmations.

- **日本語**: （readOnlyHint の行）読み取り専用ツールは低リスクとして扱うことができ、クライアントは追加の確認を減らしてもよい。
- **どう使っているか**: 注釈を付ける理由を「準拠クライアントでは確認が減りうる」という利用者の得として説明する（can / may の書き方で、クライアントがそうすると断定はしていない）。
- **条件**: 準拠クライアントの場合。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Protocol Support > Tool annotations」（取得 2026-10-02T22:12:09Z、sha256 dd59423686db…）
- **補足**: 同じ表の destructiveHint 行は「Destructive tools can stay behind stronger confirmations.」、openWorldHint 行は「Clients can treat tools as local operations, not open world operations.」（同じ取得の本文で verifier が目視、verify_quote 未実行）。 quote_ja の「扱われ」は断定に寄りすぎ。原文は can / may なので「扱うことができ」「減らしてもよい」に直した。

<a id="g-g3-vendor-servers-11"></a>
#### G3VS-11 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: CLAUDE.md（作者・エージェント向けの規則）（サーバの文書）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CLAUDE.md#L26
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CLAUDE.md
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: CLAUDE.md L26（見出し: ## Tools）
- **原文**:

> - MCP `readOnlyHint` describes whether a tool mutates host/project state such as files, build artifacts, configuration, or external services. Simulator HID/UI actions that only tap, type, press, or gesture inside the simulator may remain `readOnlyHint: true`; do not flip them to `false` merely because app UI state changes.

- **日本語**: readOnlyHint は、ファイル・ビルド成果物・設定・外部サービスといったホスト／プロジェクトの状態を変えるかを表す。シミュレータ内でタップ・入力・ボタン・ジェスチャをするだけの UI 操作は readOnlyHint: true のままでよい。アプリの UI 状態が変わるというだけで false にしないこと。
- **どう使っているか**: 作者が readOnlyHint の「環境」の範囲を独自に狭めて定義する（シミュレータ内の状態変化は数えない）。仕様の「環境を変えない」より緩い解釈。
- **条件**: 同文が AGENTS.md 80 行にもある（未照合）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、26 行（## Tools）（取得 2026-10-02T22:12:01Z、sha256 65642ab97c48…）
- **補足**: AuthGap の観点では「宣言 D と実効 M の不一致」を作者が意図して許す例。

<a id="g-g3-vendor-servers-12"></a>
#### G3VS-12 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: manifests/tools/tap.yaml（ツール定義マニフェスト）（サーバのソースコード）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/manifests/tools/tap.yaml#L13-L17
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/manifests/tools/tap.yaml
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: manifests/tools/tap.yaml L13-17
- **原文**:

> annotations:
> title: Tap
> readOnlyHint: true
> destructiveHint: false
> openWorldHint: false

- **日本語**: tap（シミュレータ画面をタップする）ツールの注釈: readOnlyHint: true、destructiveHint: false、openWorldHint: false。
- **どう使っているか**: 上の規則どおり、画面操作ツールを読み取り専用と宣言している実例。
- **条件**: 同 HEAD の manifests/tools/*.yaml で readOnlyHint: true は tap / type_text / swipe / gesture / batch / button / drag / long_press / touch / key_press / key_sequence / set_sim_location / set_sim_appearance / sim_statusbar / open_sim / reset_sim_location / screenshot など 38 ファイル（verifier が clone で grep）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、13-17 行（取得 2026-10-02T22:11:31Z、sha256 c6f32a931882…）
- **補足**: batch の説明文は「visible settings switches that can be toggled」（アプリ画面上のスイッチのタップ）で、これはシミュレータ内の UI 操作なので CLAUDE.md の規則の範囲内。規則との境界で揉めうるのはむしろ set_sim_location / set_sim_appearance / sim_statusbar（シミュレータの設定を変える）で、規則の「configuration」に当たるかは不明。 finder の notes は batch を規則違反のように書いていたが、アプリ内スイッチのタップは規則の範囲内なので書き直した。readOnlyHint: true の一覧を clone の grep で更新。

<a id="g-g3-vendor-servers-13"></a>
#### G3VS-13 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: src/integrations/xcode-tools-bridge/registry.ts: buildBestEffortAnnotations（サーバのソースコード）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/src/integrations/xcode-tools-bridge/registry.ts#L145-L157
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/src/integrations/xcode-tools-bridge/registry.ts
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: src/integrations/xcode-tools-bridge/registry.ts L145-157
- **原文**:

```
function buildBestEffortAnnotations(tool: Tool, localName: string): ToolAnnotations {
const existing = (tool.annotations ?? {}) as ToolAnnotations;
const readOnlyHint = existing.readOnlyHint ?? inferReadOnlyHint(localName);
const destructiveHint = existing.destructiveHint ?? inferDestructiveHint(localName, readOnlyHint);
const openWorldHint = existing.openWorldHint ?? inferOpenWorldHint(localName);

return {
...existing,
readOnlyHint,
destructiveHint,
openWorldHint,
};
}
```

- **日本語**: 中継する Xcode IDE ツール（xcrun mcpbridge）の注釈は、ヒントごとに、上流が宣言していればその値を使い、無ければツール名から推定した値で埋める（readOnlyHint / destructiveHint / openWorldHint の 3 つ）。
- **どう使っているか**: 上流（Apple の Xcode MCP）が注釈を欠くとき、プロキシ側が名前から機械的に注釈を作って下流へ出す。
- **条件**: Xcode Tools Bridge を有効にしたとき。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、145-157 行（取得 2026-10-02T22:11:34Z、sha256 1142819ac08f…）
- **補足**: quote_ja を「ヒントごとに」補完する形に明確化（?? はフィールド単位）。

<a id="g-g3-vendor-servers-14"></a>
#### G3VS-14 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: src/integrations/xcode-tools-bridge/registry.ts: inferReadOnlyHint（サーバのソースコード）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/src/integrations/xcode-tools-bridge/registry.ts#L159-L174
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/src/integrations/xcode-tools-bridge/registry.ts
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: src/integrations/xcode-tools-bridge/registry.ts L159-174
- **原文**:

```
function inferReadOnlyHint(localToolName: string): boolean {
const name = localToolName.toLowerCase();

const readOnlyPrefixes = [
'xcode_tools_xcodelist',
'xcode_tools_xcodeglob',
'xcode_tools_xcodegrep',
'xcode_tools_xcoderead',
'xcode_tools_xcoderefreshcodeissuesinfile',
'xcode_tools_documentationsearch',
'xcode_tools_getbuildlog',
'xcode_tools_gettestlist',
];

return readOnlyPrefixes.some((p) => name.startsWith(p));
}
```

- **日本語**: ツール名（小文字化）が xcode_tools_xcodelist / xcodeglob / xcodegrep / xcoderead / … / gettestlist で始まれば readOnlyHint を true と推定する。それ以外は false。
- **どう使っているか**: 名前の接頭辞の許可リストで readOnlyHint を導く（推定）。直後の inferDestructiveHint は xcodedelete / xcodeclean / xcodeerase / xcoderemove を破壊的、inferOpenWorldHint は常に false。
- **条件**: 上流が注釈を出さないツールだけ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、159-174 行（取得 2026-10-02T22:11:34Z、sha256 1142819ac08f…）
- **補足**: 名前ベース推定なので、名前と挙動がずれれば注釈もずれる。inferDestructiveHint（同ファイル 176-188 行）は readOnly と推定したものを false、それ以外は xcodedelete / xcodeclean / xcodeerase / xcoderemove 接頭辞だけを true にするので、リストに無い書き込みツールは destructiveHint: false になる（仕様の既定 true より緩い側に倒す。clone で目視）。 推定の向きを追記: リスト外の書き込みツールは destructiveHint=false（仕様既定 true より楽観側）。

<a id="g-g3-vendor-servers-15"></a>
#### G3VS-15 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: CHANGELOG.md [2.3.1] Fixed（リリースノート）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CHANGELOG.md#L343
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CHANGELOG.md
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: CHANGELOG.md L343（見出し: ### Fixed）
- **原文**:

> - Fixed unnecessary tool confirmation prompts in MCP clients (such as Codex) that treat missing approval annotations as high-risk defaults ([#297](https://github.com/getsentry/XcodeBuildMCP/pull/297)).

- **日本語**: （修正）承認用の注釈が無いことを高リスクの既定とみなす MCP クライアント（Codex など）で、不要な確認が出ていたのを直した。
- **どう使っているか**: サーバー作者が注釈を付ける動機が「クライアントの確認プロンプトを減らすこと」だと示す。
- **条件**: v2.3.1。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: その他・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、343 行（### Fixed）（取得 2026-10-02T22:11:35Z、sha256 d4ce94cd8522…）
- **補足**: Codex が欠落を高リスク扱いすることの一次確認ではない（サーバー作者の記述）。#297 の中身は未確認（github.com は読めない）。

<a id="g-g3-vendor-servers-16"></a>
#### G3VS-16 Sentry（getsentry） — MobileBuildMCP（旧 XcodeBuildMCP。iOS/macOS ビルド用 MCP サーバー、TypeScript）

- **資料**: CHANGELOG.md [2.2.0] Changed（リリースノート）
- **URL**: https://github.com/getsentry/MobileBuildMCP/blob/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CHANGELOG.md#L441
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/getsentry/MobileBuildMCP/d13ff0c707b0681769cf31da0eb42c4f94ceafff/CHANGELOG.md
- **版**: getsentry/MobileBuildMCP@d13ff0c707b0681769cf31da0eb42c4f94ceafff（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: CHANGELOG.md L441（見出し: ### Changed）
- **原文**:

> - Tool annotations now more accurately classify operations, reducing unnecessary confirmation prompts in MCP clients that respect annotations ([#253](https://github.com/getsentry/XcodeBuildMCP/pull/253) by [@saschagordner](https://github.com/saschagordner)).

- **日本語**: 注釈がより正確に操作を分類するようになり、注釈を尊重するクライアントでの不要な確認が減った。
- **どう使っているか**: 注釈の変更をクライアントの確認回数の変化として説明する。
- **条件**: v2.2.0。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、441 行（### Changed）（取得 2026-10-02T22:11:35Z、sha256 d4ce94cd8522…）
- **補足**: 同 CHANGELOG 545 行（[2.0.0] 節）に「**MCP tool annotations**: All tools now include MCP-standard annotations (read-only vs. destructive, idempotent, etc.) for clients that support them.」（clone で目視、verify_quote 未実行）。 441 行は [2.2.0] 節（369-451 行）にあり [2.3.0] ではない。doc_title / conditions を直した。545 行の付記は [2.0.0] 節。

### Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript）

<a id="g-g3-vendor-servers-17"></a>
#### G3VS-17 Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript）

- **資料**: mcp/tools/definitions.ts（get_connection_string の定義）（サーバのソースコード）
- **URL**: https://github.com/neondatabase/mcp-server-neon/blob/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/definitions.ts#L169-L181
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neondatabase/mcp-server-neon/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/definitions.ts
- **版**: neondatabase/mcp-server-neon@00d82d4e5c925380fc077fe1932780035f564d8b（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: mcp/tools/definitions.ts L169-181
- **原文**:

```
// Not `readOnlySafe` despite `readOnlyHint: true`: the call mutates nothing,
// but the URI it returns embeds the branch owner role's password. That role
// is a `neon_superuser` member with `CREATEROLE`, and its password
// authenticates against the read-write compute no matter which endpoint
// host the URI names — so handing it to a read-only caller lets them leave
// the sandbox entirely and run DDL/DML directly.
readOnlySafe: false,
annotations: {
title: 'Get Connection String',
readOnlyHint: true,
destructiveHint: false,
idempotentHint: true,
openWorldHint: false,
```

- **日本語**: readOnlyHint: true なのに readOnlySafe にしない。呼び出し自体は何も変えないが、返す URI に強い権限（neon_superuser、CREATEROLE）のパスワードが入っており、読み取り専用の呼び出し元に渡すとサンドボックスを出て DDL/DML を直接実行できるから。
- **どう使っているか**: 読み取り専用モードの選別キーを readOnlyHint とは別の内部フラグ readOnlySafe にしている。readOnlyHint（環境を変えないか）と「読み取り専用の利用者に出してよいか」が別物だと作者自身が明記する。
- **条件**: Neon の read-only モード（?readonly=true、x-read-only ヘッダ、OAuth の read スコープ）のとき。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: その他・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、169-181 行（取得 2026-10-02T22:11:34Z、sha256 c5410b50cf71…）
- **補足**: 逆向きの例もある: run_sql / run_sql_transaction は readOnlyHint: false・destructiveHint: true だが readOnlySafe: true（read-only モードでは読み取りクエリだけ通す、README 176 行）。

<a id="g-g3-vendor-servers-18"></a>
#### G3VS-18 Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript）

- **資料**: mcp/tools/generated/adapt.ts: generatedReadOnlySafe（サーバのソースコード）
- **URL**: https://github.com/neondatabase/mcp-server-neon/blob/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/generated/adapt.ts#L136-L144
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neondatabase/mcp-server-neon/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/generated/adapt.ts
- **版**: neondatabase/mcp-server-neon@00d82d4e5c925380fc077fe1932780035f564d8b（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: mcp/tools/generated/adapt.ts L136-144
- **原文**:

```
function generatedReadOnlySafe(
toolId: GeneratedToolId,
tool: GeneratedNeonTool,
): boolean {
if (READ_ONLY_SAFE_TOOL_OVERRIDES.has(toolId)) {
return true;
}
return tool.metadata.method === 'GET' && !tool.requiresApproval;
}
```

- **日本語**: 自動生成ツールの readOnlySafe は、上書きリストにあれば true、そうでなければ HTTP メソッドが GET で承認不要のときだけ true。
- **どう使っているか**: Neon API の OpenAPI から生成したツールについて、読み取り専用モードに出すかを HTTP メソッドから機械的に決める（注釈は使わない）。
- **条件**: mcp/tools/generated のツール。上書きは logs.query のみ。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、136-144 行（取得 2026-10-02T22:11:36Z、sha256 a5d33a84b156…）

<a id="g-g3-vendor-servers-19"></a>
#### G3VS-19 Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript）

- **資料**: mcp/tools/generated/adapt.ts: generatedDestructiveHint（サーバのソースコード）
- **URL**: https://github.com/neondatabase/mcp-server-neon/blob/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/generated/adapt.ts#L206-L214
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neondatabase/mcp-server-neon/00d82d4e5c925380fc077fe1932780035f564d8b/mcp/tools/generated/adapt.ts
- **版**: neondatabase/mcp-server-neon@00d82d4e5c925380fc077fe1932780035f564d8b（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: mcp/tools/generated/adapt.ts L206-214
- **原文**:

```
function generatedDestructiveHint(
toolId: GeneratedToolId,
tool: GeneratedNeonTool,
): boolean {
const method = tool.metadata.method;
if (method === 'GET') return false;
if (method === 'DELETE' || method === 'PUT' || method === 'PATCH') {
return true;
}
```

- **日本語**: 自動生成ツールの destructiveHint: GET なら false、DELETE / PUT / PATCH なら true。それ以外（POST など）は、ツール ID の末尾が delete / remove / disable / restore / reset / revoke / suspend / restart / update で始まるか、指定リスト（branches.finalizeRestore など 5 件）にあれば true（引用の後の行）。
- **どう使っているか**: destructiveHint を HTTP メソッドと操作名から機械的に導く。ただし CREATE_TOOLS（projects.create / branches.create）は destructiveHint: false、logs.query は固定の注釈で、この関数を通らない。readOnlyHint は生成元の値をそのまま、idempotentHint は欠落なら readOnlySafe を使う（同ファイル 185 行）。
- **条件**: mcp/tools/generated のツール。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 危険度を付ける・その他
- **確かさ**: [確認] 再照合 exact・1 か所、206-214 行（取得 2026-10-02T22:11:36Z、sha256 a5d33a84b156…）
- **補足**: 「機械的に注釈を導く」型の実例。PUT/PATCH（既存資源の置換・変更）を destructive とするのは、仕様の「追加的な更新だけなら false」に照らして整合的。 quote_ja の POST の規則を正確化（ツール ID 末尾セグメントの接頭辞＋指定リスト）。CREATE_TOOLS / logs.query の例外を追記。「PUT/PATCH は仕様より広い」は仕様の定義と合わないので直した。

<a id="g-g3-vendor-servers-20"></a>
#### G3VS-20 Neon（Databricks 傘下） — Neon MCP Server（mcp.neon.tech、TypeScript）

- **資料**: README.md「Scopes and Read-Only Mode」（サーバの文書）
- **URL**: https://github.com/neondatabase/mcp-server-neon/blob/00d82d4e5c925380fc077fe1932780035f564d8b/README.md#L176
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/neondatabase/mcp-server-neon/00d82d4e5c925380fc077fe1932780035f564d8b/README.md
- **版**: neondatabase/mcp-server-neon@00d82d4e5c925380fc077fe1932780035f564d8b（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: README.md L176（見出し: ### Scopes and Read-Only Mode）
- **原文**:

> > **Note:** Read-only mode restricts which _tools_ are available. Further, the `run_sql` tool remains available only for read-only queries.

- **日本語**: （注）読み取り専用モードは使えるツールを制限する。さらに run_sql ツールは読み取りクエリにだけ使える。
- **どう使っているか**: 読み取り専用モードは一覧の絞り込みに加え、run_sql の中身（SQL）も実行時に制限する。
- **条件**: URL の ?readonly=true、OAuth の read スコープなど。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、176 行（### Scopes and Read-Only Mode）（取得 2026-10-02T22:12:05Z、sha256 a0da5ddac0dd…）
- **補足**: 注釈（readOnlyHint: false）だけでは run_sql の read-only モードでの扱いは分からない例。

### SonarSource — SonarQube MCP Server（Java）

<a id="g-g3-vendor-servers-21"></a>
#### G3VS-21 SonarSource — SonarQube MCP Server（Java）

- **資料**: SonarQubeMcpServer.java: filterForEnabledTools（サーバのソースコード）
- **URL**: https://github.com/SonarSource/sonarqube-mcp-server/blob/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/SonarQubeMcpServer.java#L569-L574
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/SonarSource/sonarqube-mcp-server/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/SonarQubeMcpServer.java
- **版**: SonarSource/sonarqube-mcp-server@50ff95db47aa72bc634d5aed45087954b2bb0f17（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: src/main/java/org/sonarsource/sonarqube/mcp/SonarQubeMcpServer.java L569-574
- **原文**:

```
private List<Tool> filterForEnabledTools(List<Tool> toolsToFilter) {
return toolsToFilter.stream()
.filter(tool -> tool.getCategories().stream().anyMatch(mcpConfiguration::isToolCategoryEnabled))
.filter(tool -> !mcpConfiguration.isReadOnlyMode() || tool.definition().annotations().readOnlyHint())
.toList();
}
```

- **日本語**: 有効なカテゴリに属し、かつ（read-only モードでなければ全部、read-only モードなら）readOnlyHint が true のツールだけを残す。
- **どう使っているか**: SONARQUBE_READ_ONLY=true で、readOnlyHint の無いツールを出さない。
- **条件**: 環境変数 SONARQUBE_READ_ONLY（既定 false）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、569-574 行（取得 2026-10-02T22:12:55Z、sha256 91bc07b70ab8…）

<a id="g-g3-vendor-servers-22"></a>
#### G3VS-22 SonarSource — SonarQube MCP Server（Java）

- **資料**: ToolDefinitionBuilder.java: build()（サーバのソースコード）
- **URL**: https://github.com/SonarSource/sonarqube-mcp-server/blob/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/tools/ToolDefinitionBuilder.java#L184-L190
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/SonarSource/sonarqube-mcp-server/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/tools/ToolDefinitionBuilder.java
- **版**: SonarSource/sonarqube-mcp-server@50ff95db47aa72bc634d5aed45087954b2bb0f17（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: src/main/java/org/sonarsource/sonarqube/mcp/tools/ToolDefinitionBuilder.java L184-190
- **原文**:

```
var toolAnnotations = new McpSchema.ToolAnnotations(
null,
isReadOnly,
false,
false,
true,
null);
```

- **日本語**: 注釈は ToolAnnotations(title なし, isReadOnly, destructive=false, idempotent=false, openWorld=true, …) で作る。
- **どう使っているか**: readOnlyHint だけがツールごと（setReadOnlyHint() を呼んだか）で、destructiveHint=false・idempotentHint=false・openWorldHint=true は全ツール共通の固定値。書き込みツール（課題の状態変更など）も destructiveHint: false を明示して出る。
- **条件**: ToolDefinitionBuilder で作る全ツール。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、184-190 行（取得 2026-10-02T22:11:31Z、sha256 a8c84804fc3e…）
- **補足**: LangGraph の「全ツール同じ注釈」ほどではないが、destructiveHint をツールごとに判断していない。

<a id="g-g3-vendor-servers-23"></a>
#### G3VS-23 SonarSource — SonarQube MCP Server（Java）

- **資料**: transport/PerRequestToolFilteringHandler.java: filterTools（サーバのソースコード）
- **URL**: https://github.com/SonarSource/sonarqube-mcp-server/blob/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/transport/PerRequestToolFilteringHandler.java#L121
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/SonarSource/sonarqube-mcp-server/50ff95db47aa72bc634d5aed45087954b2bb0f17/src/main/java/org/sonarsource/sonarqube/mcp/transport/PerRequestToolFilteringHandler.java
- **版**: SonarSource/sonarqube-mcp-server@50ff95db47aa72bc634d5aed45087954b2bb0f17（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: src/main/java/org/sonarsource/sonarqube/mcp/transport/PerRequestToolFilteringHandler.java L121
- **原文**:

> .filter(definition -> !readOnly || (definition.annotations() != null && definition.annotations().readOnlyHint()))

- **日本語**: リクエストの文脈で read-only が指定されていれば、注釈があり readOnlyHint が true の定義だけを残す。
- **どう使っているか**: Streamable HTTP では、クライアントがリクエストごとに SONARQUBE_READ_ONLY ヘッダで読み取り専用に狭められる（注釈が選別キー）。
- **条件**: HTTP トランスポートで SONARQUBE_READ_ONLY ヘッダが来たとき。サーバー起動時の制限を広げることはできない（同ファイルの Javadoc）。絞られたツールへの tools/call も METHOD_NOT_FOUND で拒否する（同 Javadoc）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、121 行（取得 2026-10-02T22:11:31Z、sha256 99fa29f8c582…）
- **補足**: 同ファイル Javadoc の「tools/call も許可外なら METHOD_NOT_FOUND」を追記（clone で目視）。

<a id="g-g3-vendor-servers-24"></a>
#### G3VS-24 SonarSource — SonarQube MCP Server（Java）

- **資料**: README.md 環境変数表 SONARQUBE_READ_ONLY（サーバの文書）
- **URL**: https://github.com/SonarSource/sonarqube-mcp-server/blob/50ff95db47aa72bc634d5aed45087954b2bb0f17/README.md#L589
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/SonarSource/sonarqube-mcp-server/50ff95db47aa72bc634d5aed45087954b2bb0f17/README.md
- **版**: SonarSource/sonarqube-mcp-server@50ff95db47aa72bc634d5aed45087954b2bb0f17（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: README.md L589（見出し: ### Selective Tool Enablement）
- **原文**:

> When set to `true`, enables read-only mode which disables all write operations (changing issue status for example). This filter is cumulative with `SONARQUBE_TOOLSETS` if both are set.

- **日本語**: true にすると読み取り専用モードになり、すべての書き込み操作（例: 課題の状態変更）を無効にする。SONARQUBE_TOOLSETS と併用すると両方が効く。
- **どう使っているか**: 利用者向けの説明。実装は readOnlyHint による選別（上の 2 件）。
- **条件**: 既定 false。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、589 行（### Selective Tool Enablement）（取得 2026-10-02T22:11:34Z、sha256 7927db609553…）

### Buildkite — buildkite-mcp-server（Go）

<a id="g-g3-vendor-servers-25"></a>
#### G3VS-25 Buildkite — buildkite-mcp-server（Go）

- **資料**: pkg/toolsets/toolsets.go: ToolDefinition.IsReadOnly（サーバのソースコード）
- **URL**: https://github.com/buildkite/buildkite-mcp-server/blob/9cda5062d0c9c199b1432550777ff622916802c8/pkg/toolsets/toolsets.go#L20-L26
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/buildkite/buildkite-mcp-server/9cda5062d0c9c199b1432550777ff622916802c8/pkg/toolsets/toolsets.go
- **版**: buildkite/buildkite-mcp-server@9cda5062d0c9c199b1432550777ff622916802c8（HEAD、コミット日 2026-10-01、2026-10-02 取得）
- **書いてある場所**: pkg/toolsets/toolsets.go L20-26
- **原文**:

```
// IsReadOnly returns true if the tool is read-only
func (td ToolDefinition) IsReadOnly() bool {
if td.Tool.Annotations == nil {
return false
}
return td.Tool.Annotations.ReadOnlyHint
}
```

- **日本語**: ツールが読み取り専用かは注釈の ReadOnlyHint で決める。注釈そのものが無ければ false（読み取り専用ではない）。
- **どう使っているか**: read-only モードの選別（GetReadOnlyTools）と、そのモードで必要な API トークンスコープの集計（GetRequiredScopes(…, readOnlyMode) が読み取り専用ツールの RequiredScopes だけを集める）にこの判定を使う。
- **条件**: BUILDKITE_READ_ONLY=true、または HTTP の X-Buildkite-Read-Only ヘッダ（pkg/server/handler.go）。ヘッダがあればその値（"true" 以外は false）がサーバー既定を上書きするので、SonarQube と違いヘッダで read-only を外すこともできる（handler.go 47-48 行、clone で目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、20-26 行（取得 2026-10-02T22:11:32Z、sha256 9702db452f80…）
- **補足**: スコープ自体は各ツールの手書き RequiredScopes で、注釈はどのツールのスコープを数えるかの選別に使われる（toolsets.go 200-228 行、clone で目視）。 「必要スコープも注釈から導く」は不正確（スコープは手書き、注釈はツールの選別だけ）なので直した。HTTP ヘッダが既定 true を false に戻せる点を追記。

<a id="g-g3-vendor-servers-26"></a>
#### G3VS-26 Buildkite — buildkite-mcp-server（Go）

- **資料**: internal/commands/stdio.go（CLI フラグ定義）（サーバのソースコード）
- **URL**: https://github.com/buildkite/buildkite-mcp-server/blob/9cda5062d0c9c199b1432550777ff622916802c8/internal/commands/stdio.go#L15
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/buildkite/buildkite-mcp-server/9cda5062d0c9c199b1432550777ff622916802c8/internal/commands/stdio.go
- **版**: buildkite/buildkite-mcp-server@9cda5062d0c9c199b1432550777ff622916802c8（HEAD、コミット日 2026-10-01、2026-10-02 取得）
- **書いてある場所**: internal/commands/stdio.go L15
- **原文**:

> ReadOnly        bool     `help:"Enable read-only mode, which filters out write operations from all toolsets." default:"false" env:"BUILDKITE_READ_ONLY"`

- **日本語**: read-only モードを有効にし、全ツールセットから書き込み操作を除く。既定 false、環境変数 BUILDKITE_READ_ONLY。
- **どう使っているか**: 利用者向けフラグの説明。実装は上の IsReadOnly（readOnlyHint）。
- **条件**: stdio / http 両方に同じフラグ。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、15 行（取得 2026-10-02T22:11:32Z、sha256 952931ca3f32…）

### PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript）

<a id="g-g3-vendor-servers-27"></a>
#### G3VS-27 PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript）

- **資料**: services/mcp/src/tools/toolDefinitions.ts（ツール一覧の絞り込み）（サーバのソースコード）
- **URL**: https://github.com/PostHog/posthog/blob/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/toolDefinitions.ts#L314-L317
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PostHog/posthog/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/toolDefinitions.ts
- **版**: PostHog/posthog@d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: services/mcp/src/tools/toolDefinitions.ts L314-317
- **原文**:

```
// In read-only mode, only expose tools annotated as read-only
if (readOnly) {
entries = entries.filter(([_, definition]) => definition.annotations.readOnlyHint === true)
}
```

- **日本語**: 読み取り専用モードでは readOnlyHint が true と注釈されたツールだけを出す。
- **どう使っているか**: x-posthog-read-only ヘッダまたは ?readonly= で、注釈による絞り込みを行う。
- **条件**: src/index.ts で x-posthog-read-only / readonly クエリが true または 1 のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、314-317 行（取得 2026-10-02T22:12:55Z、sha256 c3753c8588ea…）
- **補足**: PostHog MCP は旧 PostHog/mcp リポジトリから PostHog/posthog モノレポ services/mcp に移った（旧 README の記載）。

<a id="g-g3-vendor-servers-28"></a>
#### G3VS-28 PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript）

- **資料**: services/mcp/src/lib/gateway-tools.ts: annotationsFor（サーバのソースコード）
- **URL**: https://github.com/PostHog/posthog/blob/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/lib/gateway-tools.ts#L64-L75
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PostHog/posthog/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/lib/gateway-tools.ts
- **版**: PostHog/posthog@d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: services/mcp/src/lib/gateway-tools.ts L64-75
- **原文**:

```
function annotationsFor(tool: AvailableTool): Tool['annotations'] {
const declared = (tool.annotations ?? {}) as Record<string, unknown>
// Absent hints take the MCP spec's defaults, which are also the cautious reading:
// a tool is assumed destructive and non-read-only until it says otherwise. Inverting
// that would let a server that declares nothing look safer than one that does.
return {
destructiveHint: declared['destructiveHint'] !== false,
idempotentHint: declared['idempotentHint'] === true,
openWorldHint: declared['openWorldHint'] !== false,
readOnlyHint: declared['readOnlyHint'] === true,
}
}
```

- **日本語**: 接続した第三者 MCP サーバーのツールを中継するとき、欠けたヒントは仕様の既定（慎重な読み方）で埋める。何も宣言しないサーバーが宣言したサーバーより安全に見えてはいけないので、逆にはしない。
- **どう使っているか**: ゲートウェイとして上流の注釈を下流へ出す際、明示の false / true だけを信じ、欠落は destructive・openWorld・非 readOnly・非 idempotent にする。
- **条件**: PostHog に第三者 MCP サーバーを接続したとき。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、64-75 行（取得 2026-10-02T22:11:28Z、sha256 eb993a9bbf44…）
- **補足**: 同 commit の src/api/generated.ts 13854 行（API スキーマの説明）は、上流が宣言した注釈を「Advisory only — policy may escalate them, never loosen them.」と書く（clone で目視、verify_quote 未実行）。 関連する付記（注釈は助言のみ、ポリシーは強めるだけ）を notes に追加。

<a id="g-g3-vendor-servers-29"></a>
#### G3VS-29 PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript）

- **資料**: services/mcp/src/tools/exec.ts: EXEC_TOOL_ANNOTATIONS（サーバのソースコード）
- **URL**: https://github.com/PostHog/posthog/blob/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/exec.ts#L44-L54
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PostHog/posthog/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/exec.ts
- **版**: PostHog/posthog@d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: services/mcp/src/tools/exec.ts L44-54
- **原文**:

```
/** Advertised on `tools/list` and on the runtime Tool. OpenAI's plugin verifier
*  requires these three hints (plus idempotent) to be present, not just defined
*  on the handler side. `destructiveHint` stays false because every read goes
*  through `exec` too: Claude Code asks for approval on each call to a tool
*  marked destructive, even when the user set it to always allow. */
export const EXEC_TOOL_ANNOTATIONS = {
destructiveHint: false,
idempotentHint: false,
openWorldHint: true,
readOnlyHint: false,
} as const
```

- **日本語**: OpenAI のプラグイン検証は 4 つのヒントが tools/list に出ていることを求める。destructiveHint は false のままにする。読み取りもすべて exec を通るので、destructive と付けると Claude Code が（常に許可にしていても）毎回承認を求めるから。
- **どう使っているか**: 書き込みもできるメタツール exec に、クライアントの承認挙動を避ける目的で destructiveHint: false を付ける。注釈が実効ではなくクライアントの UX に合わせて決まる実例。
- **条件**: exec（PostHog の各操作を中継する単一ツール）。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、44-54 行（取得 2026-10-02T22:11:31Z、sha256 dbbdc8711201…）
- **補足**: Claude Code の挙動・OpenAI 検証の要件はサーバー作者の記述で、一次確認ではない。

<a id="g-g3-vendor-servers-30"></a>
#### G3VS-30 PostHog — PostHog MCP（PostHog モノレポ services/mcp、TypeScript）

- **資料**: services/mcp/src/tools/render-ui.ts: getRenderableToolNames（サーバのソースコード）
- **URL**: https://github.com/PostHog/posthog/blob/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/render-ui.ts#L31-L39
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/PostHog/posthog/d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e/services/mcp/src/tools/render-ui.ts
- **版**: PostHog/posthog@d9fbceacebd74e8cd397a8bdb1fe9b990fc7380e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: services/mcp/src/tools/render-ui.ts L31-39
- **原文**:

```
/**
* Names of the tools `render-ui` can render — those whose UI app exposes a reusable view.
* Restricted to read-only tools: `render-ui` is annotated read-only, so it must not be a
* back door for dispatching state-changing tools (e.g. `survey-launch`, `workflows-create`).
*/
export function getRenderableToolNames(allTools: Tool<ZodObjectAny>[]): string[] {
return allTools
.filter((tool) => tool.annotations.readOnlyHint && toDispatchableAppKey(tool) !== undefined)
.map((tool) => tool.name)
```

- **日本語**: render-ui が描画できるのは readOnlyHint の付いたツールだけ。render-ui 自身が read-only と注釈されているので、状態を変えるツール（survey-launch など）を呼ぶ裏口になってはいけない。
- **どう使っているか**: 自分の readOnlyHint: true を守るため、内部から呼び出せる先を readOnlyHint で絞る（注釈の推移的な整合をコードで保つ）。
- **条件**: render-ui ツール。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・その他
- **確かさ**: [確認] 再照合 exact・1 か所、31-39 行（取得 2026-10-02T22:11:34Z、sha256 5e721a100005…）

### LangChain — LangGraph Agent Server（langgraph-api 0.15.1）の /mcp エンドポイント

<a id="g-g3-vendor-servers-31"></a>
#### G3VS-31 LangChain — LangGraph Agent Server（langgraph-api 0.15.1）の /mcp エンドポイント

- **資料**: langgraph_api/api/mcp/_handlers.py（tools/list の生成）（サーバのソースコード）
- **URL**: https://files.pythonhosted.org/packages/ef/a8/b80341369c961e919d90eb67bd13cd142499ef190e5c37cf993e1e20677c/langgraph_api-0.15.1-py3-none-any.whl
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8767/langgraph_api/api/mcp/_handlers.py）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: langgraph-api 0.15.1（PyPI 最新、2026-10-02 取得）
- **書いてある場所**: langgraph_api/api/mcp/_handlers.py L303-308
- **原文**:

```
"annotations": {
"readOnlyHint": False,
"destructiveHint": False,
"idempotentHint": False,
"openWorldHint": True,
},
```

- **日本語**: 各アシスタント（グラフ）を MCP ツールにするとき、注釈は全ツールで固定: readOnlyHint False、destructiveHint False、idempotentHint False、openWorldHint True。
- **どう使っているか**: グラフが何をするかに関係なく、すべてのツールに destructiveHint: false を明示して出す。注釈がツールの実効を全く反映しない。
- **条件**: LangGraph Platform / LangSmith Agent Server の /mcp エンドポイント（自動で全アシスタントを公開）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、303-308 行（取得 2026-10-02T22:11:20Z、sha256 5619d7a25cf4…）
- **補足**: langgraph-api は GitHub に公開ソースが無く（Elastic-2.0 の配布物）、PyPI の wheel langgraph_api-0.15.1-py3-none-any.whl（sha256 d2ae79d92940ffd68c8ecfe714168d883c885c7f55a6017b530ad05d7cc06194、files.pythonhosted.org）を展開した _handlers.py（sha256 5619d7a25cf41c0f…）を 127.0.0.1:8767 で配信して照合した（fetched_url は一時 URL。学生は wheel を取って再現できる。inspector.pypi.io は JS チャレンジで読めなかった）。303-308 行。WebSearch で見つけた issue langchain-ai/langgraph#8952「annotations hardcoded identically for every tool」は github.com が読めないため未確認だが、0.15.1 のコードはその題どおり。

### HashiCorp（IBM） — terraform-mcp-server（Go）

<a id="g-g3-vendor-servers-32"></a>
#### G3VS-32 HashiCorp（IBM） — terraform-mcp-server（Go）

- **資料**: pkg/tools/factories.go（create_run の 2 版）（サーバのソースコード）
- **URL**: https://github.com/hashicorp/terraform-mcp-server/blob/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/tools/factories.go#L117-L122
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/hashicorp/terraform-mcp-server/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/tools/factories.go
- **版**: hashicorp/terraform-mcp-server@1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/tools/factories.go L117-122
- **原文**:

```
"create_run": func(logger *log.Logger, _ *server.MCPServer, tfOpsEnabled bool) server.ServerTool {
if tfOpsEnabled {
return tfeTools.CreateRun(logger)
}
return tfeTools.CreateRunSafe(logger)
},
```

- **日本語**: create_run は ENABLE_TF_OPERATIONS が有効なら CreateRun（destructiveHint: true、run_type に auto_approve / is_destroy を含む）、無効なら CreateRunSafe（destructiveHint: false、run_type は plan_and_apply / refresh_state / plan_only / allow_empty_apply）を登録する。
- **どう使っているか**: 同名ツールの入力スキーマと注釈を運用モードで差し替える。注釈で絞るのではなく、手書きの別定義で破壊的な版を出し分ける。
- **条件**: ENABLE_TF_OPERATIONS（既定 false）。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: その他・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、117-122 行（取得 2026-10-02T22:12:58Z、sha256 acae0cde2007…）
- **補足**: 2 版の注釈は pkg/tools/tfe/create_run.go 27-28 / 124-125 行（clone で目視）。Safe 版も plan_and_apply を残すので「破壊的な選択肢なし」とまでは言えない（apply に人の確認が要るかは HCP Terraform 側の設定次第で、未確認）。 Safe 版にも plan_and_apply が残るので「破壊的な選択肢なし」を run_type の列挙に置き換えた。注釈の行番号を clone で確認（124-125）。

<a id="g-g3-vendor-servers-33"></a>
#### G3VS-33 HashiCorp（IBM） — terraform-mcp-server（Go）

- **資料**: pkg/toolsets/registry.go: ToolDef（サーバのソースコード）
- **URL**: https://github.com/hashicorp/terraform-mcp-server/blob/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/toolsets/registry.go#L8-L13
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/hashicorp/terraform-mcp-server/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/toolsets/registry.go
- **版**: hashicorp/terraform-mcp-server@1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/toolsets/registry.go L8-13
- **原文**:

```
type ToolDef struct {
Name          string
Toolset       string
RequiresTFE   bool // needs an authenticated TFE/TFC session before it's registered
RequiresTFOps bool // additionally gated behind ENABLE_TF_OPERATIONS=true
}
```

- **日本語**: ツールの登録メタデータの唯一の正本。RequiresTFOps は ENABLE_TF_OPERATIONS=true のときだけ登録する印。
- **どう使っているか**: 破壊的ツールの出し分けは注釈ではなく手書きの RequiresTFOps フラグで行う。
- **条件**: ENABLE_TF_OPERATIONS=true で delete_project / delete_team / delete_workspace_safely / force_unlock_workspace / action_run が出る（同ファイル）。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、8-13 行（取得 2026-10-02T22:11:33Z、sha256 27c657218b4d…）
- **補足**: 注釈との不一致: delete_variable_in_variable_set・detach_variable_set_from_workspaces（DestructiveHint: true）と create_no_code_workspace（WithDestructiveHintAnnotation(true)）は RequiresTFOps が無く、既定で出る（registry.go 62/89/91 行、clone で目視）。 ゲート外の destructive ツールは 2 件ではなく 3 件（create_no_code_workspace も）なので notes を直した。

<a id="g-g3-vendor-servers-34"></a>
#### G3VS-34 HashiCorp（IBM） — terraform-mcp-server（Go）

- **資料**: pkg/mcp-official/tools/tfe/variable_set_variables_delete_tool.go（サーバのソースコード）
- **URL**: https://github.com/hashicorp/terraform-mcp-server/blob/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/mcp-official/tools/tfe/variable_set_variables_delete_tool.go#L35-L40
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/hashicorp/terraform-mcp-server/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/pkg/mcp-official/tools/tfe/variable_set_variables_delete_tool.go
- **版**: hashicorp/terraform-mcp-server@1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: pkg/mcp-official/tools/tfe/variable_set_variables_delete_tool.go L35-40
- **原文**:

```
Title:           "Delete a variable from a Terraform variable set",
OpenWorldHint:   jsonschema.Ptr(true),
ReadOnlyHint:    false,
DestructiveHint: jsonschema.Ptr(true),
},
}
```

- **日本語**: delete_variable_in_variable_set の注釈: OpenWorldHint true、ReadOnlyHint false、DestructiveHint true。
- **どう使っているか**: destructiveHint: true の削除ツールだが、ENABLE_TF_OPERATIONS のゲート（RequiresTFOps）の対象外。注釈と運用上の破壊的ゲートが別系統。
- **条件**: 公式 go-sdk 版の定義。
- **扱う宣言**: destructiveHint・readOnlyHint・openWorldHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、35-40 行（取得 2026-10-02T22:11:37Z、sha256 e5a2853cac32…）

<a id="g-g3-vendor-servers-35"></a>
#### G3VS-35 HashiCorp（IBM） — terraform-mcp-server（Go）

- **資料**: helm/terraform-mcp-server/README.md（サーバの文書）
- **URL**: https://github.com/hashicorp/terraform-mcp-server/blob/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/helm/terraform-mcp-server/README.md#L118
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/hashicorp/terraform-mcp-server/1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81/helm/terraform-mcp-server/README.md
- **版**: hashicorp/terraform-mcp-server@1d9a2e03a933e0fd00caffa1d4b8c18f9cec0a81（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: helm/terraform-mcp-server/README.md L118（見出し: ## Security notes）
- **原文**:

> - **Destructive tools are off by default.** `mcpServer.enableTfOperations` gates the tools that delete or force-unlock Terraform resources. Leave it `false` unless you specifically want those available.

- **日本語**: 破壊的ツールは既定で無効。mcpServer.enableTfOperations が、Terraform の資源を削除・強制解錠するツールを有効にする。
- **どう使っているか**: 「破壊的ツール」の範囲は注釈ではなく手書きリストで決まる。
- **条件**: Helm チャートの値 mcpServer.enableTfOperations（既定 false）。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、118 行（## Security notes）（取得 2026-10-02T22:11:34Z、sha256 85ef79e2948d…）

### Netlify — Netlify MCP Server（netlify-mcp、TypeScript）

<a id="g-g3-vendor-servers-36"></a>
#### G3VS-36 Netlify — Netlify MCP Server（netlify-mcp、TypeScript）

- **資料**: src/tools/tool-utils.ts: categorizeToolsByReadWrite（サーバのソースコード）
- **URL**: https://github.com/netlify/netlify-mcp/blob/84312229df2dc4a6a313b3a97816d9652a72c36a/src/tools/tool-utils.ts#L11-L13
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/netlify/netlify-mcp/84312229df2dc4a6a313b3a97816d9652a72c36a/src/tools/tool-utils.ts
- **版**: netlify/netlify-mcp@84312229df2dc4a6a313b3a97816d9652a72c36a（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: src/tools/tool-utils.ts L11-13
- **原文**:

```
export const categorizeToolsByReadWrite = (domainTools: DomainTool<any>[]) => {
const readOnlyTools = domainTools.filter(tool => tool.toolAnnotations.readOnlyHint === true);
const writeTools = domainTools.filter(tool => tool.toolAnnotations.readOnlyHint === false || tool.toolAnnotations.readOnlyHint === undefined);
```

- **日本語**: 領域ごとの操作を readOnlyHint が true のものと、false か未定義のもの（書き込み扱い）に分ける。
- **どう使っているか**: 操作単位の readOnlyHint で、領域ごとの「読み取り用」「書き込み用」の束ねツールに振り分ける。未定義は書き込み側。
- **条件**: すべての領域ツール。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、11-13 行（取得 2026-10-02T22:13:00Z、sha256 81dcee50468f…）

<a id="g-g3-vendor-servers-37"></a>
#### G3VS-37 Netlify — Netlify MCP Server（netlify-mcp、TypeScript）

- **資料**: src/tools/index.ts: registerDomainTools（verbose モードの個別登録）（サーバのソースコード）
- **URL**: https://github.com/netlify/netlify-mcp/blob/84312229df2dc4a6a313b3a97816d9652a72c36a/src/tools/index.ts#L105-L110
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/netlify/netlify-mcp/84312229df2dc4a6a313b3a97816d9652a72c36a/src/tools/index.ts
- **版**: netlify/netlify-mcp@84312229df2dc4a6a313b3a97816d9652a72c36a（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: src/tools/index.ts L105-110
- **原文**:

```
server.registerTool(toolName, {
description: toolDescription,
inputSchema: schemaShape,
annotations: {
readOnlyHint: operationType === 'read'
}
```

- **日本語**: verbose モードで操作ごとにツールを登録するとき、注釈は readOnlyHint: (読み取り用なら true) だけを付ける。束ねる通常モード（169 行）も同じ注釈。
- **どう使っているか**: 複数操作を 1 ツールに束ねても readOnlyHint が意味を保つよう、読みと書きを別ツールにする設計。destructiveHint 等は付けないので書き込み側は仕様の既定（破壊的）になる。
- **条件**: verbose モード（105-110 行）でも通常モード（束ねツール、165-170 行）でも同じ（clone で目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、105-110 行（取得 2026-10-02T22:11:39Z、sha256 41245433a443…）
- **補足**: 例外: design-import のツール（src/tools/design-import/import-claude-design.ts 381 / 418 行）は destructiveHint: false を明示する。 引用の 105-110 行は verbose モードの個別登録で、束ねツールではない。quote_ja / doc_title を直し、通常モードの同じ注釈（169 行）を clone で確認。

### Okta（Auth0） — auth0-mcp-server（TypeScript）

<a id="g-g3-vendor-servers-38"></a>
#### G3VS-38 Okta（Auth0） — auth0-mcp-server（TypeScript）

- **資料**: src/utils/tools.ts: filterToolsByReadOnly（サーバのソースコード）
- **URL**: https://github.com/auth0/auth0-mcp-server/blob/10390b40dc488fa4b582ba52ce861d33b518a86a/src/utils/tools.ts#L113-L117
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/auth0/auth0-mcp-server/10390b40dc488fa4b582ba52ce861d33b518a86a/src/utils/tools.ts
- **版**: auth0/auth0-mcp-server@10390b40dc488fa4b582ba52ce861d33b518a86a（HEAD、コミット日 2026-08-13、2026-10-02 取得）
- **書いてある場所**: src/utils/tools.ts L113-117
- **原文**:

```
function filterToolsByReadOnly(tools: Tool[]): Tool[] {
const readOnlyTools = tools.filter((tool) => tool._meta?.readOnly === true);
log(`Filtered to ${readOnlyTools.length} read-only tools`);
return readOnlyTools;
}
```

- **日本語**: --read-only のとき、_meta.readOnly が true のツールだけを残す。
- **どう使っているか**: 読み取り専用モードの選別キーは注釈 readOnlyHint ではなく独自の _meta.readOnly。各ツールは _meta.readOnly と annotations.readOnlyHint を別々に手書きしている（例 src/tools/actions.ts 49-58 行）。
- **条件**: CLI の --read-only（既定 false）。--tools より優先。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、113-117 行（取得 2026-10-02T22:11:32Z、sha256 fc785f7f5ef3…）
- **補足**: 2 つの値が食い違っても検出する仕組みは見当たらない（不明）。同 commit の src/tools/*.ts を verifier が簡易集計すると、_meta.readOnly: true の 10 件はすべて readOnlyHint: true、書き込み系 13 件は _meta.readOnly を持たず readOnlyHint: false（現時点では食い違いなし）。 現時点で 2 つの値が一致していることを clone の集計で追記。

### dbt Labs — dbt-mcp（Python）

<a id="g-g3-vendor-servers-39"></a>
#### G3VS-39 dbt Labs — dbt-mcp（Python）

- **資料**: src/dbt_mcp/tools/annotations.py: create_tool_annotations（サーバのソースコード）
- **URL**: https://github.com/dbt-labs/dbt-mcp/blob/8e7022bae4cc6a0dc6f708fe9d95de8ac952661e/src/dbt_mcp/tools/annotations.py#L4-L14
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/dbt-labs/dbt-mcp/8e7022bae4cc6a0dc6f708fe9d95de8ac952661e/src/dbt_mcp/tools/annotations.py
- **版**: dbt-labs/dbt-mcp@8e7022bae4cc6a0dc6f708fe9d95de8ac952661e（HEAD、コミット日 2026-10-01、2026-10-02 取得）
- **書いてある場所**: src/dbt_mcp/tools/annotations.py L4-14
- **原文**:

```
def create_tool_annotations(
title: str | None = None,
read_only_hint: bool = False,
destructive_hint: bool = True,
idempotent_hint: bool = False,
open_world_hint: bool = True,
) -> ToolAnnotations:
"""
Creates tool annotations. Defaults to the most cautious option,
i.e destructive, non-idempotent, and open-world.
Args:
```

- **日本語**: 注釈を作る関数の既定は最も慎重な値: read_only_hint=False、destructive_hint=True、idempotent_hint=False、open_world_hint=True。
- **どう使っているか**: 作者が書き忘れても慎重側の注釈が出るよう、ヘルパーの既定を仕様の既定に合わせる（Python サーバー）。
- **条件**: dbt-mcp の全ツール（definitions.py の dbt_mcp_tool も同じ既定）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、4-14 行（取得 2026-10-02T22:11:33Z、sha256 b49c11443058…）

<a id="g-g3-vendor-servers-40"></a>
#### G3VS-40 dbt Labs — dbt-mcp（Python）

- **資料**: src/dbt_mcp/dbt_cli/tools.py（dbt docs ツールの定義）（サーバのソースコード）
- **URL**: https://github.com/dbt-labs/dbt-mcp/blob/8e7022bae4cc6a0dc6f708fe9d95de8ac952661e/src/dbt_mcp/dbt_cli/tools.py#L453-L462
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/dbt-labs/dbt-mcp/8e7022bae4cc6a0dc6f708fe9d95de8ac952661e/src/dbt_mcp/dbt_cli/tools.py
- **版**: dbt-labs/dbt-mcp@8e7022bae4cc6a0dc6f708fe9d95de8ac952661e（HEAD、コミット日 2026-10-01、2026-10-02 取得）
- **書いてある場所**: src/dbt_mcp/dbt_cli/tools.py L453-462
- **原文**:

```
ToolDefinition(
fn=docs,
title="dbt docs",
description=get_prompt("dbt_cli/docs"),
annotations=create_tool_annotations(
title="dbt docs",
read_only_hint=True,
destructive_hint=False,
idempotent_hint=True,
),
```

- **日本語**: dbt docs ツールは read_only_hint=True、destructive_hint=False、idempotent_hint=True。
- **どう使っているか**: 実体は `dbt docs generate`（同ファイル 203-204 行）。dbt の一般的な挙動として target/ に catalog.json などを書き出し、ウェアハウスへメタデータ照会をする（この挙動はこのリポジトリの引用では確認していない）。readOnlyHint の「環境を変えない」とずれうる宣言、というのは解釈。
- **条件**: dbt CLI ツールセット有効時。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、453-462 行（取得 2026-10-02T22:11:32Z、sha256 670dd17470d1…）
- **補足**: 作者がローカル生成物を「環境」に含めない意図かは不明。dbt compile / dbt parse / dbt list / dbt show も read_only_hint=True（同ファイル 448 / 471 / 482 / 515 行、clone で目視）。 target/ への書き出しは dbt の一般知識でソースに書かれていないため、そう明記して解釈と分けた。

### Couchbase — mcp-server-couchbase（Python）

<a id="g-g3-vendor-servers-41"></a>
#### G3VS-41 Couchbase — mcp-server-couchbase（Python）

- **資料**: src/cb_mcp/tools/operational/__init__.py: TOOL_ANNOTATIONS（サーバのソースコード）
- **URL**: https://github.com/couchbase-ecosystem/mcp-server-couchbase/blob/df5d9ceb013f57143171f65ec3ba033ace06aa9a/src/cb_mcp/tools/operational/__init__.py#L173
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/couchbase-ecosystem/mcp-server-couchbase/df5d9ceb013f57143171f65ec3ba033ace06aa9a/src/cb_mcp/tools/operational/__init__.py
- **版**: couchbase-ecosystem/mcp-server-couchbase@df5d9ceb013f57143171f65ec3ba033ace06aa9a（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: src/cb_mcp/tools/operational/__init__.py L173（見出し: # Tool annotations for MCP clients (readOnlyHint, destructiveHint, etc.)）
- **原文**:

> "run_sql_plus_plus_query": ToolAnnotations(),

- **日本語**: SQL++ を実行する run_sql_plus_plus_query の注釈は空（ToolAnnotations()）。
- **どう使っているか**: 何でも実行できるクエリツールにヒントを付けず、仕様の既定（非 readOnly・破壊的）に任せる。
- **条件**: 常に（注釈は固定）。実行時の書き込み阻止は read_only_mode または書き込みスコープ欠如（lacks_write_scope）のとき（tools/operational/query.py 162-175 行）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、173 行（# Tool annotations for MCP clients (readOnlyHint, destructiveHint, etc.)）（取得 2026-10-02T22:11:36Z、sha256 b920bd46df21…）
- **補足**: KV 書き込みツールも upsert / insert / replace は ToolAnnotations(idempotentHint=True) だけ、delete は destructiveHint=True を付ける（同ファイル、clone で目視）。 conditions の「常に」を補足し、実行時阻止の条件（read_only_mode / 書き込みスコープ欠如）を追記。

<a id="g-g3-vendor-servers-42"></a>
#### G3VS-42 Couchbase — mcp-server-couchbase（Python）

- **資料**: src/cb_mcp/tools/operational/__init__.py: TOOL_SET（read_only 側）（サーバのソースコード）
- **URL**: https://github.com/couchbase-ecosystem/mcp-server-couchbase/blob/df5d9ceb013f57143171f65ec3ba033ace06aa9a/src/cb_mcp/tools/operational/__init__.py#L110
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/couchbase-ecosystem/mcp-server-couchbase/df5d9ceb013f57143171f65ec3ba033ace06aa9a/src/cb_mcp/tools/operational/__init__.py
- **版**: couchbase-ecosystem/mcp-server-couchbase@df5d9ceb013f57143171f65ec3ba033ace06aa9a（HEAD、コミット日 2026-09-30、2026-10-02 取得）
- **書いてある場所**: src/cb_mcp/tools/operational/__init__.py L110（見出し: # new code, and see cb_mcp.core.spec for why the inventory is declared as data.）
- **原文**:

> run_sql_plus_plus_query,  # Write protection handled at runtime via read_only_mode

- **日本語**: run_sql_plus_plus_query は read_only 側のリストに入っており、書き込みの防止は read_only_mode で実行時に行う。
- **どう使っているか**: 読み取り専用モードの選別は注釈ではなく TOOL_SET の read_only / write の手書きリスト。クエリツールは注釈では非 readOnly だが、モード上は読み取り側に置き、SQL の文の種類（dql / utility）で実行時に止める（tools/operational/query.py）。
- **条件**: READ_ONLY_MODE（CLI の read_only_mode）。run_sql_plus_plus_query の書き込み阻止は read_only_mode または書き込みスコープ欠如のとき、文の種類が dql_statement / utility_statement だけなら通す（query.py 91・117・175 行）。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、110 行（# new code, and see cb_mcp.core.spec for why the inventory is declared as data.）（取得 2026-10-02T22:11:36Z、sha256 b920bd46df21…）
- **補足**: Python サーバーで、注釈・モード用リスト・実行時検査の 3 つが別々に保守されている。 実行時阻止の条件に書き込みスコープ欠如を追加し、通す文の種類を正確化（clone で目視）。

### Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript）

<a id="g-g3-vendor-servers-43"></a>
#### G3VS-43 Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript）

- **資料**: packages/EXAMPLE-MCP-PROVIDER/src/tools/example_tool.ts（提供者向けの手本）（サーバのソースコード）
- **URL**: https://github.com/salesforcecli/mcp/blob/204591906fe23aecfdf06086259767b95ad30b17/packages/EXAMPLE-MCP-PROVIDER/src/tools/example_tool.ts#L59-L61
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/salesforcecli/mcp/204591906fe23aecfdf06086259767b95ad30b17/packages/EXAMPLE-MCP-PROVIDER/src/tools/example_tool.ts
- **版**: salesforcecli/mcp@204591906fe23aecfdf06086259767b95ad30b17（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: packages/EXAMPLE-MCP-PROVIDER/src/tools/example_tool.ts L59-61
- **原文**:

```
annotations: {
readOnlyHint: true,
},
```

- **日本語**: 手本ツールの設定は annotations: { readOnlyHint: true }。
- **どう使っているか**: 新しいツール提供者が写す雛形に readOnlyHint だけを入れている。サーバー本体（packages/mcp/src/sf-mcp-server.ts の registerTool）は注釈を SDK に渡すだけで、読み取り専用モード等の選別には使わない（ローカル clone の grep）。
- **条件**: Salesforce DX MCP の提供者パッケージ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、59-61 行（取得 2026-10-02T22:11:45Z、sha256 936fd961e62b…）

<a id="g-g3-vendor-servers-44"></a>
#### G3VS-44 Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript）

- **資料**: packages/mcp-provider-dx-core/src/tools/deploy_metadata.ts（サーバのソースコード）
- **URL**: https://github.com/salesforcecli/mcp/blob/204591906fe23aecfdf06086259767b95ad30b17/packages/mcp-provider-dx-core/src/tools/deploy_metadata.ts#L122-L125
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/salesforcecli/mcp/204591906fe23aecfdf06086259767b95ad30b17/packages/mcp-provider-dx-core/src/tools/deploy_metadata.ts
- **版**: salesforcecli/mcp@204591906fe23aecfdf06086259767b95ad30b17（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: packages/mcp-provider-dx-core/src/tools/deploy_metadata.ts L122-125
- **原文**:

```
annotations: {
destructiveHint: true,
openWorldHint: false,
},
```

- **日本語**: deploy_metadata の注釈: destructiveHint: true、openWorldHint: false。
- **どう使っているか**: 組織（リモートの Salesforce）へ配備するツールを openWorldHint: false とする。一方 assign_permission_set は openWorldHint: true、DevOps 系は「Calls Salesforce DevOps Center API」で true。openWorldHint の基準が提供者間で揃っていない。
- **条件**: —
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、122-125 行（取得 2026-10-02T22:11:38Z、sha256 d8af2db4b1ae…）

<a id="g-g3-vendor-servers-45"></a>
#### G3VS-45 Salesforce — Salesforce DX MCP Server（salesforcecli/mcp、TypeScript）

- **資料**: packages/mcp-provider-dx-core/src/tools/run_soql_query.ts（サーバのソースコード）
- **URL**: https://github.com/salesforcecli/mcp/blob/204591906fe23aecfdf06086259767b95ad30b17/packages/mcp-provider-dx-core/src/tools/run_soql_query.ts#L70-L73
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/salesforcecli/mcp/204591906fe23aecfdf06086259767b95ad30b17/packages/mcp-provider-dx-core/src/tools/run_soql_query.ts
- **版**: salesforcecli/mcp@204591906fe23aecfdf06086259767b95ad30b17（HEAD、コミット日 2026-09-23、2026-10-02 取得）
- **書いてある場所**: packages/mcp-provider-dx-core/src/tools/run_soql_query.ts L70-73
- **原文**:

```
annotations: {
openWorldHint: false,
readOnlyHint: true,
},
```

- **日本語**: run_soql_query の注釈: openWorldHint: false、readOnlyHint: true。
- **どう使っているか**: リモート組織への SOQL 照会を読み取り専用・閉じた世界と宣言する例。
- **条件**: —
- **扱う宣言**: readOnlyHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、70-73 行（取得 2026-10-02T22:12:06Z、sha256 0ff53cbe2a56…）

### Microsoft（Azure） — AKS-MCP（Azure/aks-mcp、Go）

<a id="g-g3-vendor-servers-46"></a>
#### G3VS-46 Microsoft（Azure） — AKS-MCP（Azure/aks-mcp、Go）

- **資料**: internal/components/azaks/registry.go: RegisterAzAksOperations（サーバのソースコード）
- **URL**: https://github.com/Azure/aks-mcp/blob/279efd929a0a7b09adcbc74e4771c0f65583b9a6/internal/components/azaks/registry.go#L103-L106
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Azure/aks-mcp/279efd929a0a7b09adcbc74e4771c0f65583b9a6/internal/components/azaks/registry.go
- **版**: Azure/aks-mcp@279efd929a0a7b09adcbc74e4771c0f65583b9a6（HEAD、コミット日 2026-09-01、2026-10-02 取得）
- **書いてある場所**: internal/components/azaks/registry.go L103-106
- **原文**:

> return mcp.NewTool("az_aks_operations",
> mcp.WithDescription(description),
> mcp.WithTitleAnnotation("AKS Operations"),
> mcp.WithDestructiveHintAnnotation(true),

- **日本語**: az_aks_operations ツールは常に DestructiveHint: true で登録される（説明文だけが access level で変わる）。
- **どう使っているか**: リスク段階は --access-level（readonly / readwrite / admin）で操作ごとに判定し（GetOperationAccessLevel）、注釈はツール単位で固定。readonly で起動しても注釈は変わらない。
- **条件**: --access-level の値によらない。
- **扱う宣言**: destructiveHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、103-106 行（取得 2026-10-02T22:11:58Z、sha256 435f7532e22e…）
- **補足**: README の「What `--access-level` is and is not」節は --access-level を「誤操作を減らすガードレールで、悪意ある呼び出し元に対するセキュリティ境界ではない」と書く（README 62-69 行、clone で目視）。az_aks_operations は access level によらず server.go 298-299 行で登録される。 README の付記と、access level によらず登録されることを clone で確認。

### DigitalOcean — mcp-digitalocean（digitalocean-labs、Go）

<a id="g-g3-vendor-servers-47"></a>
#### G3VS-47 DigitalOcean — mcp-digitalocean（digitalocean-labs、Go）

- **資料**: pkg/registry/common/annotations.go: hints.apply（サーバのソースコード）
- **URL**: https://github.com/digitalocean-labs/mcp-digitalocean/blob/e0d2ef6ae87cbce3164e60b7c95b65004db5156a/pkg/registry/common/annotations.go#L71-L79
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/digitalocean-labs/mcp-digitalocean/e0d2ef6ae87cbce3164e60b7c95b65004db5156a/pkg/registry/common/annotations.go
- **版**: digitalocean-labs/mcp-digitalocean@e0d2ef6ae87cbce3164e60b7c95b65004db5156a（HEAD、コミット日 2026-10-01、2026-10-02 取得）
- **書いてある場所**: pkg/registry/common/annotations.go L71-79
- **原文**:

```
// apply sets the four MCP tool hint annotations on t (overriding the mcp-go
// library defaults, which assume the worst case: not read-only, destructive,
// not idempotent) and stashes the registry metadata under t.Meta. The
// permission is derived 1:1 from the tool name (droplet-get ->
// tools.digitalocean.droplet_get).
func (h hints) apply(t *mcp.Tool) {
mcp.WithReadOnlyHintAnnotation(h.readOnly)(t)
mcp.WithDestructiveHintAnnotation(h.destructive)(t)
mcp.WithIdempotentHintAnnotation(h.idempotent)(t)
```

- **日本語**: 4 つのヒントを必ず明示して、最悪側を仮定する mcp-go の既定（非 readOnly・破壊的・非冪等）を上書きする。あわせて _meta に権限名（ツール名から 1 対 1）などを入れる。
- **どう使っているか**: 作者は HintsRead / HintsCreate / HintsAction / HintsToggle / HintsDelete / HintsReplace の型（プロファイル）から選ぶ方式で、ツールごとに真偽値を手書きしない。
- **条件**: mcp-digitalocean の全ツール。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、71-79 行（取得 2026-10-02T22:11:33Z、sha256 caaaf27534ac…）
- **補足**: 同ファイル 20-25 行のコメント: 承認のゲート（high-risk は承認が要る）は注釈ではなく _meta の registry メタデータ risk（WithRisk でツールごとに設定）で決まる、と書く。注釈は 4 ヒント、承認は risk、と別系統（clone で目視）。 同ファイルのコメントにある「承認ゲートは risk（_meta）で決まる」を notes に追記。

### Google Cloud — gke-mcp（GoogleCloudPlatform/gke-mcp、Go）

<a id="g-g3-vendor-servers-48"></a>
#### G3VS-48 Google Cloud — gke-mcp（GoogleCloudPlatform/gke-mcp、Go）

- **資料**: pkg/tools/cluster/tools.go（get_kubeconfig の定義）（サーバのソースコード）
- **URL**: https://github.com/GoogleCloudPlatform/gke-mcp/blob/eb340d0587cb508495a14ecb6fe5a0e2a03547b9/pkg/tools/cluster/tools.go#L72-L77
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/GoogleCloudPlatform/gke-mcp/eb340d0587cb508495a14ecb6fe5a0e2a03547b9/pkg/tools/cluster/tools.go
- **版**: GoogleCloudPlatform/gke-mcp@eb340d0587cb508495a14ecb6fe5a0e2a03547b9（HEAD、コミット日 2026-09-28、2026-10-02 取得）
- **書いてある場所**: pkg/tools/cluster/tools.go L72-77
- **原文**:

```
registry.RegisterTool(s, h.c, &mcp.Tool{
Name:        "get_kubeconfig",
Description: "Get the kubeconfig for a GKE cluster by calling the GKE API and extracting necessary details (clusterCaCertificate and endpoint). This tool appends/updates the kubeconfig in ~/.kube/config.",
Annotations: &mcp.ToolAnnotations{
// ReadOnlyHint is removed because this tool now performs a write operation.
},
```

- **日本語**: get_kubeconfig の注釈は空。コメント: このツールは書き込みをするようになったので ReadOnlyHint を外した。
- **どう使っているか**: ツールの挙動変更（~/.kube/config への追記）に合わせて readOnlyHint を外した、宣言の保守の実例。
- **条件**: —
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、72-77 行（取得 2026-10-02T22:11:58Z、sha256 5bdd9f087942…）

### Docker — Docker Hub MCP Server（docker/hub-mcp、TypeScript）

<a id="g-g3-vendor-servers-49"></a>
#### G3VS-49 Docker — Docker Hub MCP Server（docker/hub-mcp、TypeScript）

- **資料**: src/repos.ts（createRepository の登録）（サーバのソースコード）
- **URL**: https://github.com/docker/hub-mcp/blob/4c01b635d5239192e5d1b5e0f659a6d224a44ab6/src/repos.ts#L296-L301
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/hub-mcp/4c01b635d5239192e5d1b5e0f659a6d224a44ab6/src/repos.ts
- **版**: docker/hub-mcp@4c01b635d5239192e5d1b5e0f659a6d224a44ab6（HEAD、コミット日 2026-08-27、2026-10-02 取得）
- **書いてある場所**: src/repos.ts L296-301
- **原文**:

```
inputSchema: CreateRepositoryRequest.shape,
outputSchema: Repository.shape,
annotations: {
title: 'Create Repository in namespace',
},
title: 'Create a repository in organisation (namespace) or personal namespace',
```

- **日本語**: リポジトリ作成ツールの annotations は title だけ。
- **どう使っているか**: Docker Hub MCP は（ローカル clone の grep で）readOnlyHint / destructiveHint を一切付けず、title だけを注釈に入れる。書き込みツールも仕様の既定に任せる。
- **条件**: —
- **扱う宣言**: title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、296-301 行（取得 2026-10-02T22:11:33Z、sha256 a9fc57166da3…）

### Harness — Harness MCP Server（harness/mcp-server、TypeScript）

<a id="g-g3-vendor-servers-50"></a>
#### G3VS-50 Harness — Harness MCP Server（harness/mcp-server、TypeScript）

- **資料**: src/registry/index.ts: dispatch（サーバのソースコード）
- **URL**: https://github.com/harness/mcp-server/blob/b3344bc894f725af17ebdb9bd526ab6e5602c62a/src/registry/index.ts#L397-L399
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/harness/mcp-server/b3344bc894f725af17ebdb9bd526ab6e5602c62a/src/registry/index.ts
- **版**: harness/mcp-server@b3344bc894f725af17ebdb9bd526ab6e5602c62a（HEAD、コミット日 2026-09-29、2026-10-02 取得）
- **書いてある場所**: src/registry/index.ts L397-399
- **原文**:

```
if (this.config.HARNESS_READ_ONLY && !Registry.READ_OPERATIONS.has(operation)) {
throw new Error(`Read-only mode is enabled (HARNESS_READ_ONLY=true). "${operation}" operations are not allowed.`);
}
```

- **日本語**: HARNESS_READ_ONLY が有効で、操作名が list / get 以外なら「Read-only mode is enabled」で拒否する。
- **どう使っているか**: 読み取り専用モードは注釈ではなく操作名（list / get）で実行時に判定する。harness_execute のアクションは各アクションの operationPolicy.risk が "read" かで判定（同ファイル 456 行、harness-execute.ts 243 行）。書き込みツール（harness_update など、readOnlyHint: false）は一覧から隠されず、呼ぶとエラーになる。
- **条件**: HARNESS_READ_ONLY=true（既定 false）。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、397-399 行（取得 2026-10-02T22:11:31Z、sha256 ece94dea841d…）
- **補足**: HARNESS_READ_ONLY が一覧を絞らず実行時拒否だけであること、execute は risk で判定することを clone で確認して追記。

### monday.com — monday.com MCP（mondaycom/mcp、TypeScript）

<a id="g-g3-vendor-servers-51"></a>
#### G3VS-51 monday.com — monday.com MCP（mondaycom/mcp、TypeScript）

- **資料**: packages/agent-toolkit/CLAUDE.md（作者向け手順）（サーバの文書）
- **URL**: https://github.com/mondaycom/mcp/blob/d0b22c72147217c2d506ca0611a43fc1a919cc2e/packages/agent-toolkit/CLAUDE.md#L56
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mondaycom/mcp/d0b22c72147217c2d506ca0611a43fc1a919cc2e/packages/agent-toolkit/CLAUDE.md
- **版**: mondaycom/mcp@d0b22c72147217c2d506ca0611a43fc1a919cc2e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: packages/agent-toolkit/CLAUDE.md L56（見出し: ### Adding a New Platform API Tool）
- **原文**:

> 5. Set `name` (snake_case), `type`, and `annotations` via `createMondayApiAnnotations()` (sets `openWorldHint: true`). Annotation fields: `title`, `readOnlyHint` (true for READ), `destructiveHint` (true if deletes data), `idempotentHint` (true if repeated calls are safe)

- **日本語**: 新しいツールでは name・type・annotations を設定する。readOnlyHint は READ 型なら true、destructiveHint はデータを消すなら true、idempotentHint は繰り返しても安全なら true。
- **どう使っているか**: 注釈を内部のツール型（READ / WRITE）と揃えるよう作者に指示する。
- **条件**: monday.com agent-toolkit。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、56 行（### Adding a New Platform API Tool）（取得 2026-10-02T22:12:59Z、sha256 2c5d0f2faa0c…）

<a id="g-g3-vendor-servers-52"></a>
#### G3VS-52 monday.com — monday.com MCP（mondaycom/mcp、TypeScript）

- **資料**: packages/agent-toolkit/src/utils/tools/tools-filtering.utils.ts（サーバのソースコード）
- **URL**: https://github.com/mondaycom/mcp/blob/d0b22c72147217c2d506ca0611a43fc1a919cc2e/packages/agent-toolkit/src/utils/tools/tools-filtering.utils.ts#L35-L37
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mondaycom/mcp/d0b22c72147217c2d506ca0611a43fc1a919cc2e/packages/agent-toolkit/src/utils/tools/tools-filtering.utils.ts
- **版**: mondaycom/mcp@d0b22c72147217c2d506ca0611a43fc1a919cc2e（HEAD、コミット日 2026-10-02、2026-10-02 取得）
- **書いてある場所**: packages/agent-toolkit/src/utils/tools/tools-filtering.utils.ts L35-37
- **原文**:

```
if (config.readOnlyMode) {
shouldFilter = shouldFilter || toolInstance.type !== ToolType.READ;
}
```

- **日本語**: readOnlyMode のとき、ツールの type が READ でなければ除く。
- **どう使っているか**: --read-only（-ro）の選別キーは注釈ではなく内部の ToolType。readOnlyHint は作者の手で type と揃える約束（上の項目）。
- **条件**: monday-api-mcp の --read-only。
- **扱う宣言**:  ／ **使い方の分類**: 使わない・読まない・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、35-37 行（取得 2026-10-02T22:11:35Z、sha256 8d8bef991594…）

### Atlassian — Atlassian Rovo MCP Server（リモート、mcp.atlassian.com）

<a id="g-g3-vendor-servers-53"></a>
#### G3VS-53 Atlassian — Atlassian Rovo MCP Server（リモート、mcp.atlassian.com）

- **資料**: Atlassian Developer「Supported tools」> How the server exposes tools（サーバの文書）
- **URL**: https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/
- **書いてある見出しへ直接**: https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/#how-the-server-exposes-tools
- **版**: 2026-10-02 取得（finder 時 sha256 22a7724525bf、検証時 sha256 01569ae9501a。動的ページで本文が変わる。ページ表示の Last updated Sep 30, 2026）
- **書いてある場所**: Supported tools > How the server exposes tools（#how-the-server-exposes-tools）
- **原文**:

> invoked with executeRead, executeWrite, or executeDestructive depending on the operation's risk tier

- **日本語**: 遅延ツールは discover で見つけ、操作のリスク段階に応じて executeRead / executeWrite / executeDestructive で呼ぶ。
- **どう使っているか**: リスク段階（読み・書き・破壊）を注釈ではなく「呼び出し口のツールを 3 つに分ける」ことで表す。各 execute ツールにどの注釈が付くかは文書に無い（不明）。
- **条件**: リモート Rovo MCP Server の遅延ツール方式（ページ中のフラット一覧 URL は https://mcp.atlassian.com/v2/mcp?tools=all）。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Supported tools > How the server exposes tools」（取得 2026-10-02T22:11:22Z、sha256 cd1f203106e5…）
- **補足**: 同ページの Common tools 表は executeRead / executeWrite / executeDestructive を「Execution pathways for deferred tools, with agent-level confirmation」と書く（具体的に何が確認するかは書かれていない）。同じページで readOnlyHint / destructiveHint は none（checked_no_mention）。 再取得で sha256 が 22a7724525bf → 01569ae9501a に変わった（引用は exact のまま）。version を更新。 「v2」はページの URL に出るだけなので conditions を言い換えた。agent-level confirmation の文言を正確に引いた。

<a id="g-g3-vendor-servers-54"></a>
#### G3VS-54 Atlassian — Atlassian Rovo MCP Server（リモート、mcp.atlassian.com）

- **資料**: Atlassian Developer「Supported tools」（冒頭）（サーバの文書）
- **URL**: https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/
- **書いてある見出しへ直接**: https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/#supported-tools
- **版**: 2026-10-02 取得（finder 時 sha256 22a7724525bf、検証時 sha256 01569ae9501a。動的ページで本文が変わる。ページ表示の Last updated Sep 30, 2026）
- **書いてある場所**: Supported tools（#supported-tools）
- **原文**:

> Each tool belongs to a permission group, and each group bundles one or more tools by intent - for example, read, write, search, delete, or manage.

- **日本語**: 各ツールは権限グループに属し、グループは意図ごと（読み・書き・検索・削除・管理）にツールを束ねる。
- **どう使っているか**: 組織管理者は権限グループ単位で許可・取り消しをし、各ツールは親グループのアクセスを引き継ぐ。使えるツールは認証方式・スコープ・有効な権限グループ・アプリのアクセスで決まる。これらと MCP 注釈の関係はページに書かれていない。
- **条件**: 管理者が有効にした権限グループ、認証方式（OAuth 2.1 / API トークン）、アプリのアクセスによって使えるツールが変わる。
- **扱う宣言**:  ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Supported tools」（取得 2026-10-02T22:11:22Z、sha256 cd1f203106e5…）
- **補足**: 再取得で sha256 が 22a7724525bf → 01569ae9501a に変わった（引用は exact のまま）。version を更新。 ページに「読み取り専用の切り替え」という記述は無いので usage_ja から外し、ページの記述どおりに直した。

### Slack (Salesforce) — Slackbot MCP client — Slack Marketplace の掲載要件

<a id="g-g3-saas-hosts-01"></a>
#### G3SH-01 Slack (Salesforce) — Slackbot MCP client — Slack Marketplace の掲載要件

- **資料**: Distributing apps with MCP servers on the Slack Marketplace（規約・審査の指針）
- **URL**: https://docs.slack.dev/ai/slackbot-mcp-client/distributing/
- **書いてある見出しへ直接**: https://docs.slack.dev/ai/slackbot-mcp-client/distributing/#mcp-client
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Distributing apps with MCP servers on the Slack Marketplace > Submission > MCP client（#mcp-client）
- **原文**:

> DO set the readOnlyHint annotation on every tool. This value directly controls how your tool is categorized (read vs. write) in the Slackbot UI and how it's presented to users.

- **日本語**: すべてのツールに readOnlyHint 注釈を付けよ。この値が、Slackbot の画面でツールが読み取り / 書き込みのどちらに分類されるか、利用者にどう見せるかを直接決める。
- **どう使っているか**: Slack Marketplace に MCP サーバー付きアプリを出す要件（Submission > MCP client の ✅ DO）として、全ツールに readOnlyHint を付けることを求める。値は Slackbot UI での read / write の分類と利用者への見せ方を直接決めると書く。
- **条件**: Slack Marketplace に提出する、mcp:connect スコープを持つアプリの MCP サーバー。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を書くことを求める・表示（印・名前）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Distributing apps with MCP servers on the Slack Marketplace > Submission > MCP client」（取得 2026-10-02T22:11:28Z、sha256 940e0e114027…）
- **補足**: 引用は ✅ の絵文字の後ろから。同じ節で『曖昧・誤解を招くツール名や説明は却下の理由になる』（DON'T）とあるが、readOnlyHint の値が正しいかを審査で確かめるとは書いていない（検証の有無は不明）。Pre-submission checklist 自体には readOnlyHint の項目は無く、『human-readable titles, accurate descriptions, and input schemas』だけ。

### Slack (Salesforce) — Slackbot MCP client

<a id="g-g3-saas-hosts-02"></a>
#### G3SH-02 Slack (Salesforce) — Slackbot MCP client

- **資料**: Connecting an MCP server to the Slackbot MCP Client（クライアントの文書）
- **URL**: https://docs.slack.dev/ai/slackbot-mcp-client/
- **書いてある見出しへ直接**: https://docs.slack.dev/ai/slackbot-mcp-client/#slackbot-failed-to-load-tools
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connecting an MCP server to the Slackbot MCP Client > Using Slackbot > Troubleshooting > Slackbot failed to load tools（#slackbot-failed-to-load-tools）
- **原文**:

> The tools may be unclassified and default to write classification. Ensure your tools include proper descriptions and classification metadata so that read-only tools execute without additional unnecessary confirmation prompts.

- **日本語**: ツールが分類されていないと、書き込みとして扱われることがある。読み取り専用のツールが余計な確認なしに実行されるよう、説明と分類のメタデータを付けておくこと。
- **どう使っているか**: Troubleshooting で、ツールが分類されていないと write 分類に倒れ（既定）、それが『ツールを見つけるが呼ばない』原因になりうる（may）、と書く。分類のメタデータを付ければ read-only のツールは『追加の不要な確認』なしに実行される、と書くが、03 では第三者ツールは read でも呼び出しごとに許可が要るので、確認が全く出ない（自動承認）とまでは言えない。分類のメタデータが readOnlyHint であることは 01（Marketplace 要件）による推論。
- **条件**: Troubleshooting の『Slackbot discovers but does not invoke tools』の項。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connecting an MCP server to the Slackbot MCP Client > Using Slackbot > Troubleshooting > Slackbot discovers but does not invoke tools」（取得 2026-10-02T22:11:25Z、sha256 fdebd62ef9f5…）
- **補足**: 『classification metadata』とだけ書き、readOnlyHint の名は出さない（01 と合わせて readOnlyHint と読むのは推論）。同じページの 03 は『第三者のツールは read も write も呼び出しごとに利用者の許可が要る』と書いており、read-only なら確認なしで実行されるのかは 03 と食い違う（Allow once / Always allow の選択と組み合わせた挙動は不明）。location はツールの見出し推定で『Slackbot failed to load tools』と出たが、本文上は次の小見出し『Slackbot discovers but does not invoke tools』の下にある。 usage から auto_approve を外した。原文は『additional unnecessary confirmation prompts』を避けると書くだけで、03 の『第三者ツールは read も write も呼び出しごとに許可』と合わせると、read-only でも 1 回の許可（Allow once / Always allow）は残る読み方ができる。確認なしで自動実行されると読むのは過大。

<a id="g-g3-saas-hosts-03"></a>
#### G3SH-03 Slack (Salesforce) — Slackbot MCP client

- **資料**: Connecting an MCP server to the Slackbot MCP Client（クライアントの文書）
- **URL**: https://docs.slack.dev/ai/slackbot-mcp-client/
- **書いてある見出しへ直接**: https://docs.slack.dev/ai/slackbot-mcp-client/#have-slackbot-use-a-tool
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connecting an MCP server to the Slackbot MCP Client > Using Slackbot > Have Slackbot use a tool（#have-slackbot-use-a-tool）
- **原文**:

> If the tool is from a third-party, the user must explicitly authorize each tool call, both read and write, before Slackbot executes it.

- **日本語**: ツールが第三者のものなら、利用者は読み取りでも書き込みでも、Slackbot が実行する前に各呼び出しを明示的に許可しなければならない。
- **どう使っているか**: 第三者の MCP ツールは read / write を問わず呼び出しごとに許可（Allow once / Always allow / Deny）を求める、と書く。read-only の分類が確認を省くかどうかについて、02 と食い違う記述。
- **条件**: 第三者（third-party）のツール。利用者は『Always allow』で以後の確認を省ける。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connecting an MCP server to the Slackbot MCP Client > Using Slackbot > Have Slackbot use a tool」（取得 2026-10-02T22:11:25Z、sha256 fdebd62ef9f5…）
- **補足**: hints は read / write の分類（01 によれば readOnlyHint）に関わるため付けたが、この文自体は注釈の名を出さない。02 との関係（read-only は確認なしか、毎回許可か）は不明。Salesforce のブログ（16）は『write と delete のツールは操作ごとに確認、GA 版は既定で read-only を有効にする』と書いている。

### Slack (Salesforce) — Slackbot MCP client（MCP Apps / rich responses）

<a id="g-g3-saas-hosts-04"></a>
#### G3SH-04 Slack (Salesforce) — Slackbot MCP client（MCP Apps / rich responses）

- **資料**: Returning rich responses to the Slackbot MCP Client（クライアントの文書）
- **URL**: https://docs.slack.dev/ai/slackbot-mcp-client/returning-rich-responses
- **書いてある見出しへ直接**: https://docs.slack.dev/ai/slackbot-mcp-client/returning-rich-responses/#mcp-server-no-auth
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Returning rich responses to the Slackbot MCP Client > MCP Apps > Integration types > MCP server example（#mcp-server-no-auth）
- **原文**:

> The tool uses the readOnlyHint annotation to indicate it doesn't modify any state, and returns structuredContent so the UI resource can render the roll visually.

- **日本語**: このツールは readOnlyHint 注釈で、状態を変更しないことを示している。また structuredContent を返し、UI リソースが出目を絵として描けるようにしている。
- **どう使っているか**: Slack の公式サンプル（サイコロのツール）で readOnlyHint を付ける例を示す。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Returning rich responses to the Slackbot MCP Client > MCP Apps > Integration types > MCP server example」（取得 2026-10-02T22:11:32Z、sha256 7854c57bd912…）
- **補足**: サンプルの実コードは 05（bolt-python-examples）。ページの .md 版（https://docs.slack.dev/ai/slackbot-mcp-client.md）にも JS 版で annotations: { readOnlyHint: true } の例が 2 件ある（get_profile_card, roll_dice。grep で確認、ツール照合はしていない）。 quote_ja が引用の後半（structuredContent）を訳していなかったので補った。

### Slack (Salesforce) — slack-samples/bolt-python-examples（Slackbot MCP client 向けサンプル）

<a id="g-g3-saas-hosts-05"></a>
#### G3SH-05 Slack (Salesforce) — slack-samples/bolt-python-examples（Slackbot MCP client 向けサンプル）

- **資料**: ai/slackbot-mcp-client/rich-responses/mcp-apps/src/app.py（サーバのソースコード）
- **URL**: https://github.com/slack-samples/bolt-python-examples/blob/3e3d09194cd67bd6c560b3fb9af038badce7a73d/ai/slackbot-mcp-client/rich-responses/mcp-apps/src/app.py#L29-L33
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/slack-samples/bolt-python-examples/3e3d09194cd67bd6c560b3fb9af038badce7a73d/ai/slackbot-mcp-client/rich-responses/mcp-apps/src/app.py
- **版**: commit 3e3d091（2026-10-02 の HEAD）
- **書いてある場所**: app.py L33（roll_dice ツール定義 L29-L33 の中）
- **原文**:

```
    annotations=ToolAnnotations(read_only_hint=True),
```

- **日本語**: ツール定義の注釈として read_only_hint=True（readOnlyHint: true）を付ける。
- **どう使っているか**: Slack 公式サンプルの roll_dice ツール（L29-L33）が ToolAnnotations(read_only_hint=True) を宣言。乱数を返すだけで状態を変えないので、宣言は実態に合っている。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、33 行（取得 2026-10-02T22:11:34Z、sha256 f0b3f88502de…）
- **補足**: 同じ repo の no-auth/app.py と slack-identity/app.py には annotation の語は無かった（curl + grep）。引用はインデント込みの 1 行。

### Notion Labs — Notion Custom Agents（MCP connections）

<a id="g-g3-saas-hosts-06"></a>
#### G3SH-06 Notion Labs — Notion Custom Agents（MCP connections）

- **資料**: Security best practices for agent connections（クライアントの文書）
- **URL**: https://www.notion.com/help/security-best-practices-for-agent-connections
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Security best practices for Agent connections > Adding connections
- **原文**:

> Servers can classify their own tools with annotations like "read-only," "destructive," or "open-world," but Notion hasn't verified custom servers for accuracy and completeness. Notion displays these attributes in the Agent settings.

- **日本語**: サーバーは自分のツールに『read-only』『destructive』『open-world』のような注釈を付けて分類できるが、Notion はカスタムサーバーについてその正確さと完全さを検証していない。Notion はこれらの属性を Agent の設定画面に表示する。
- **どう使っているか**: 注釈（read-only / destructive / open-world）を Agent settings に表示する。カスタム MCP サーバーの注釈は Notion が検証していない、と明言。
- **条件**: ワークスペース所有者がカスタム MCP サーバーを有効にした場合（Settings → Notion AI でリモート URL を入れる）。組み込みのサーバーは『より詳しく見る』とあるが注釈の検証については書いていない。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Security best practices for Agent connections > Adding connections」（取得 2026-10-02T22:11:40Z、sha256 9014b8b0b79f…）
- **補足**: 『検証していない』と明言する数少ない一次資料。idempotentHint の扱いは書いていない。 有効化の手順はページで食い違う。このページは『ワークスペース所有者が Settings → Notion AI でリモート URL を入れる』、08/09 のページは『ワークスペース管理者が Settings → Connections の Manage タブで Enable custom MCP servers をオンにし、エージェントの Tools & Access から Custom MCP server を追加』と書く。 notes に、カスタム MCP サーバーの有効化手順が 2 つのページで違う点を追記（conditions は本ページの記述どおり）。

<a id="g-g3-saas-hosts-07"></a>
#### G3SH-07 Notion Labs — Notion Custom Agents（MCP connections）

- **資料**: Security best practices for agent connections（クライアントの文書）
- **URL**: https://www.notion.com/help/security-best-practices-for-agent-connections
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Security best practices for Agent connections > Managing the risk of connections
- **原文**:

> Notion defaults to requesting human confirmation for tool calls on all non-read-only tools. Use this setting whenever possible to keep a human in the loop.

- **日本語**: Notion は既定で、read-only でないすべてのツールの呼び出しに人の確認を求める。できるだけこの設定を使い、人を介在させること。
- **どう使っているか**: read-only でないツールは既定で人の確認が要る。裏返して『read-only のツールは既定で確認なし』と読める（auto_approve はこの含意による。read ツールの既定が Run automatically であるとは 08/09 のページにも明記が無い）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Security best practices for Agent connections > Managing the risk of connections」（取得 2026-10-02T22:11:40Z、sha256 9014b8b0b79f…）
- **補足**: 何をもって『read-only』とするか（readOnlyHint か、名前か、Notion 側の分類か）はこの文では書いていない。06 の『注釈を表示する』と合わせると readOnlyHint によると読めるが推論。注釈の無いツールの扱い（仕様の既定では readOnlyHint=false → 確認あり）も明記なし（不明）。MCP connections のページ（08, 09）にも annotation / readOnlyHint の語は本文に無い（script_only のみ。checked_no_mention 参照）。 auto_approve が原文の直接の記述ではなく含意である旨を usage_ja に明記。08/09 のページは Run automatically を『read ツールに向く』と書くだけで、read ツールの既定値は書いていない。 【本記録者の点検（2026-10-02）】原文が言うのは「read-only でないツールは既定で確認」まで。read-only なら確認なしで走るとは書いていないので、使い方の分類から「確認を省く」を外した。

<a id="g-g3-saas-hosts-08"></a>
#### G3SH-08 Notion Labs — Notion Custom Agents（MCP connections）

- **資料**: MCP connections for Custom Agents（クライアントの文書）
- **URL**: https://www.notion.com/help/mcp-connections-for-custom-agents
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: MCP connections for Custom Agents > Managing available tools
- **原文**:

> Write tools (ex: create, update, delete, send, post) make changes to data in external systems. By default, these require confirmation before the agent executes the action.

- **日本語**: 書き込みツール（作成・更新・削除・送信・投稿など）は外部システムのデータを変える。既定では、エージェントが実行する前に確認が要る。
- **どう使っているか**: read / write のツールに分け、write ツールは既定で確認（Always ask）。分け方の根拠（注釈か動詞名か）は書いていない。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP connections for Custom Agents > Managing available tools」（取得 2026-10-02T22:11:38Z、sha256 b8505661a2c2…）
- **補足**: 動詞の例（search, fetch / create, delete ...）で説明しており、分類が readOnlyHint によるとは書いていない（不明）。06 は注釈を Agent settings に表示すると書く。このページの本文には annotation / readOnlyHint の語は無い（checked_no_mention）。

<a id="g-g3-saas-hosts-09"></a>
#### G3SH-09 Notion Labs — Notion Custom Agents（MCP connections）

- **資料**: MCP connections for Custom Agents（クライアントの文書）
- **URL**: https://www.notion.com/help/mcp-connections-for-custom-agents
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: MCP connections for Custom Agents > Managing available tools
- **原文**:

> Always ask requires a user to approve or cancel an action before it executes. This is the default setting for write tools (create, update, delete, send) to prevent unintended changes. Always allow permanently approves all tools from a server and removes future confirmation prompts.

- **日本語**: 『Always ask』は実行前に利用者の承認か取り消しを求める。これが書き込みツールの既定。『Always allow』はサーバーのすべてのツールを恒久的に承認し、以後の確認を出さない。
- **どう使っているか**: ツールごとに Run automatically / Always ask を選べ、write ツールの既定は Always ask。Always allow はサーバー単位で全ツールの確認を消す。
- **条件**: ツール設定を変えられるのは MCP 接続を認証した本人だけ（同ページの注記）。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP connections for Custom Agents > Managing available tools」（取得 2026-10-02T22:11:38Z、sha256 b8505661a2c2…）
- **補足**: Always allow はサーバー単位なので、read-only と分類されたかどうかに関わらず確認が消える。分類の根拠は不明（08 と同じ）。

### Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー）

<a id="g-g3-saas-hosts-10"></a>
#### G3SH-10 Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー）

- **資料**: General Best Practices（Hosted MCP Servers Developer Guide）（サーバの文書）
- **URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.html
- **照らし合わせた中身の URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.md
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: General Best Practices > Signal Tool Behavior with Annotations（.md 版の L17）
- **原文**:

> MCP tools support an `annotations` object with four boolean hints that tell clients how the tool behaves: `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`. Well-behaved clients use these to present appropriate UX—auto-executing read-only tools and requiring confirmation for destructive ones.

- **日本語**: MCP ツールは 4 つの真偽値ヒント（readOnlyHint, destructiveHint, idempotentHint, openWorldHint）を持つ annotations オブジェクトを持てる。行儀のよいクライアントはこれを使い、read-only のツールは自動実行し、destructive なツールには確認を求める。
- **どう使っているか**: サーバー作者向けに、クライアント側の典型的な使い方（read-only は自動実行、destructive は確認）を説明する。これは『行儀のよいクライアント』一般についての Salesforce の説明で、特定のクライアントの挙動を述べたものではない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（.md 版・HTML 版とも、2026-10-02T21:39Z）。curl 既定 UA で取得した公式 .md 版の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では developer.salesforce.com が HTTP 403 で照合できないため 未確認。検証者が 2026-10-02 21:40Z 頃に curl の既定 UA で公式ページの .md 版（fetched_url）を直接取得でき（HTTP 200、HTML 版も 200）、引用はその本文と python の部分文字列検索で完全一致（第三者の r.jina.ai に頼らない形に差し替え）。 fetched_url を r.jina.ai（第三者の変換サービス）から公式の .md 版に変更。location を .md 版の行番号（L17、見出し『Signal Tool Behavior with Annotations』）に更新。ツール照合は依然 403 のため 未確認のまま。

<a id="g-g3-saas-hosts-11"></a>
#### G3SH-11 Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー）

- **資料**: General Best Practices（Hosted MCP Servers Developer Guide）（サーバの文書）
- **URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.html
- **照らし合わせた中身の URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.md
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: General Best Practices > Signal Tool Behavior with Annotations（.md 版の L19）
- **原文**:

> Platform tools ship with accurate annotation values. Read operations like SOQL queries and schema lookups are marked `readOnlyHint: true`; delete operations are marked `destructiveHint: true`.

- **日本語**: プラットフォーム標準のツールは正確な注釈の値で出荷される。SOQL クエリやスキーマ参照のような読み取りは readOnlyHint: true、削除操作は destructiveHint: true が付いている。
- **どう使っているか**: Salesforce 自身が標準ツールに注釈を付けており、それが『正確』だと主張する（主張のみ、検証方法は書いていない）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（.md 版・HTML 版とも、2026-10-02T21:39Z）。curl 既定 UA で取得した公式 .md 版の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では developer.salesforce.com が HTTP 403 で照合できないため 未確認。検証者が 2026-10-02 21:40Z 頃に curl の既定 UA で公式ページの .md 版（fetched_url）を直接取得でき（HTTP 200、HTML 版も 200）、引用はその本文と python の部分文字列検索で完全一致（第三者の r.jina.ai に頼らない形に差し替え）。 『accurate』の根拠（テストや審査）は書かれていない。 fetched_url を r.jina.ai（第三者の変換サービス）から公式の .md 版に変更。location を .md 版の行番号（L19、見出し『Signal Tool Behavior with Annotations』）に更新。ツール照合は依然 403 のため 未確認のまま。

<a id="g-g3-saas-hosts-12"></a>
#### G3SH-12 Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー）

- **資料**: General Best Practices（Hosted MCP Servers Developer Guide）（サーバの文書）
- **URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.html
- **照らし合わせた中身の URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.md
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: General Best Practices > Signal Tool Behavior with Annotations（.md 版の L21）
- **原文**:

> For custom tools backed by Flows, Apex, or REST endpoints, set annotations explicitly. The spec defaults are conservative—a tool with no annotations is assumed potentially destructive and open-world. This means a custom query tool that omits `readOnlyHint: true` will trigger unnecessary "are you sure?" prompts in clients that respect annotations.

- **日本語**: Flow・Apex・REST で作るカスタムツールには注釈を明示的に付けよ。仕様の既定値は保守的で、注釈の無いツールは破壊的かつ open-world とみなされる。だから readOnlyHint: true を省いたクエリ用ツールは、注釈を尊重するクライアントで不要な確認を出させる。
- **どう使っているか**: カスタムツールの作者に注釈の明示を求め、注釈が無いときは仕様の既定（destructive かつ open-world）で扱われる、と説明。続く文で、読むだけのツールは readOnlyHint: true と destructiveHint: false、削除や取り消せない変更をするツールは destructiveHint: true を最低限付けよ、と書く。
- **条件**: Flows / Apex / REST endpoints を元にしたカスタム MCP ツール。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（.md 版・HTML 版とも、2026-10-02T21:39Z）。curl 既定 UA で取得した公式 .md 版の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では developer.salesforce.com が HTTP 403 で照合できないため 未確認。検証者が 2026-10-02 21:40Z 頃に curl の既定 UA で公式ページの .md 版（fetched_url）を直接取得でき（HTTP 200、HTML 版も 200）、引用はその本文と python の部分文字列検索で完全一致（第三者の r.jina.ai に頼らない形に差し替え）。 ブログ（14）のスクリーンショットの alt text『Screenshot of MCP tool annotation configuration』（検証者が公式ブログの HTML で grep 確認）から、カスタムツールの注釈を Setup 画面で設定する UI があると見られる（help.salesforce.com の該当記事は JS 描画で本文を取得できず未確認）。 fetched_url を r.jina.ai（第三者の変換サービス）から公式の .md 版に変更。location を .md 版の行番号（L21、見出し『Signal Tool Behavior with Annotations』）に更新。ツール照合は依然 403 のため 未確認のまま。 引用中の “are you sure?” の曲がった引用符を .md 版の表記（直線の "）に合わせた（HTML 版は曲がった引用符）。

<a id="g-g3-saas-hosts-13"></a>
#### G3SH-13 Salesforce — Salesforce Hosted MCP Servers（Salesforce が運営する MCP サーバー）

- **資料**: General Best Practices（Hosted MCP Servers Developer Guide）（サーバの文書）
- **URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.html
- **照らし合わせた中身の URL**: https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/general-best-practices.md
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: General Best Practices > Signal Tool Behavior with Annotations（.md 版の L23）
- **原文**:

> Annotations are hints, not enforcement. Not all clients read or respect them. They complement—but do not replace—the access control and human-in-the-loop strategies described above.

- **日本語**: 注釈はヒントであって強制ではない。すべてのクライアントが読む・尊重するわけではない。アクセス制御や人の介在の代わりにはならず、補うだけ。
- **どう使っているか**: 注釈は強制力を持たないので、アクセス制御（per-user 認可）と human-in-the-loop を置き換えない、と注意する。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（.md 版・HTML 版とも、2026-10-02T21:39Z）。curl 既定 UA で取得した公式 .md 版の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では developer.salesforce.com が HTTP 403 で照合できないため 未確認。検証者が 2026-10-02 21:40Z 頃に curl の既定 UA で公式ページの .md 版（fetched_url）を直接取得でき（HTTP 200、HTML 版も 200）、引用はその本文と python の部分文字列検索で完全一致（第三者の r.jina.ai に頼らない形に差し替え）。 fetched_url を r.jina.ai（第三者の変換サービス）から公式の .md 版に変更。location を .md 版の行番号（L23、見出し『Signal Tool Behavior with Annotations』）に更新。ツール照合は依然 403 のため 未確認のまま。

### Salesforce — Salesforce Hosted MCP Servers

<a id="g-g3-saas-hosts-14"></a>
#### G3SH-14 Salesforce — Salesforce Hosted MCP Servers

- **資料**: How to Secure Salesforce Hosted MCP Servers（Salesforce Developers Blog, 2026-06）（公式ブログ）
- **URL**: https://developer.salesforce.com/blogs/2026/06/how-to-secure-salesforce-hosted-mcp-servers
- **版**: 2026-06-30 公開（ページの datePublished）、2026-10-02 取得
- **書いてある場所**: How to Secure Salesforce Hosted MCP Servers > Annotate MCP tools
- **原文**:

> Doing so lets agents know how they should use the tools. For example, should the agent ask the user for confirmation when running potentially destructive operations, such as deleting a record, or whether a tool can safely be run multiple times.

- **日本語**: こうすると、エージェントはツールをどう使うべきかが分かる。たとえば、レコード削除のような破壊的になりうる操作の前に利用者へ確認すべきか、ツールを何度実行しても安全か。
- **どう使っているか**: Hosted MCP のカスタムツールに注釈を付けることを『セキュリティ対策ではないがベストプラクティス』として勧め、確認の要否（destructive）と再実行の安全性（idempotent）の手がかりになると説明。
- **扱う宣言**: destructiveHint・idempotentHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（2026-10-02T21:39Z）。curl 既定 UA で取得した公式ブログ HTML の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では HTTP 403 で照合できず 未確認。検証者が curl の既定 UA で公式ブログの HTML を直接取得でき（HTTP 200）、タグを除いた本文で引用と完全一致を確認。 直前の文は『While not strictly a security measure, it’s a best practice to annotate MCP tools that you expose to provide hints about their behavior.』（『annotate MCP tools』は help.salesforce.com の platform.api_catalog_create_custom_salesforce_mcp_servers へのリンク）。 hints（destructiveHint / idempotentHint）は文中の『破壊的になりうる操作』『何度実行しても安全か』からの対応づけで、文自体は注釈の名を出さない。 fetched_url を r.jina.ai から公式ブログ URL に変更（curl 既定 UA で 200、本文で完全一致）。location を見出し名に、version を公開日（datePublished 2026-06-30）に更新。ツール照合は依然 403 のため 未確認のまま。 notes に hints が推論である旨を追記。

<a id="g-g3-saas-hosts-15"></a>
#### G3SH-15 Salesforce — Salesforce Hosted MCP Servers

- **資料**: How to Secure Salesforce Hosted MCP Servers（Salesforce Developers Blog, 2026-06）（公式ブログ）
- **URL**: https://developer.salesforce.com/blogs/2026/06/how-to-secure-salesforce-hosted-mcp-servers
- **版**: 2026-06-30 公開（ページの datePublished）、2026-10-02 取得
- **書いてある場所**: How to Secure Salesforce Hosted MCP Servers > Annotate MCP tools
- **原文**:

> is optional on the client side and these may not be enforced by all agents.

- **日本語**: （MCP ツール注釈のサポートは）クライアント側では任意で、すべてのエージェントが強制するとは限らない。
- **どう使っているか**: 注釈を付けても、クライアントが守るとは限らないと注意する。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [未確認] verify_quote.py: match=fetch_failed status=403（2026-10-02T21:39Z）。curl 既定 UA で取得した公式ブログ HTML の本文で完全一致を手元確認。
- **補足**: verify_quote.py（ブラウザ UA）では HTTP 403 で照合できず 未確認。検証者が curl の既定 UA で公式ブログの HTML を直接取得でき（HTTP 200）、タグを除いた本文で引用と完全一致を確認。 15 の引用は文の後半。前半は『Note: Support for MCP tool annotations』（リンク文字列）で、リンクは MCP 仕様 2025-06-18 の ToolAnnotations。 fetched_url を r.jina.ai から公式ブログ URL に変更（curl 既定 UA で 200、本文で完全一致）。location を見出し名に、version を公開日（datePublished 2026-06-30）に更新。ツール照合は依然 403 のため 未確認のまま。

### Salesforce — Slackbot MCP client（Salesforce の解説ブログ）

<a id="g-g3-saas-hosts-16"></a>
#### G3SH-16 Salesforce — Slackbot MCP client（Salesforce の解説ブログ）

- **資料**: 3 Ways to Connect Agentforce Agents and Slackbot to External MCP Servers（公式ブログ）
- **URL**: https://www.salesforce.com/blog/connect-agentforce-external-mcp-servers/
- **書いてある見出しへ直接**: https://www.salesforce.com/blog/connect-agentforce-external-mcp-servers/?bc=OTH#h-control-the-tools-that-slackbot-can-use
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: 3 Ways to Connect Agentforce Agents and Slackbot to External MCP Servers > Option 2: Connect Slackbot directly to external MCP servers > Control the tools that Slackbot can use（#h-control-the-tools-that-slackbot-can-use）
- **原文**:

> Write and delete tools require explicit, per-action user confirmation before Slackbot proceeds, and the current GA release activates read-only by default, so design any workflow that needs Slackbot to take action assuming a confirmation step is required.

- **日本語**: 書き込みと削除のツールは、Slackbot が進める前に操作ごとの明示的な利用者確認が要る。現在の GA 版は既定で read-only を有効にするので、Slackbot に操作させるワークフローは確認の段階がある前提で設計すること。
- **どう使っているか**: Slackbot は write / delete ツールを操作ごとに確認し、GA 版は既定で read-only（のツール）を有効にする、と説明。分類の根拠は書いていないが、Slack Marketplace 要件（01）では readOnlyHint が read / write の分類を直接決める。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「3 Ways to Connect Agentforce Agents and Slackbot to External MCP Servers > Option 2: Connect Slackbot directly to external MCP servers > Control the tools that Slackbot can use」（取得 2026-10-02T22:13:03Z、sha256 bec2a8b0ba2f…）
- **補足**: 『activates read-only by default』が『read-only ツールだけを既定で有効化』の意味か、別の意味かは文面からは確定できない（不明）。Agentforce 側（Option 1）は Agent Builder でエージェントごと・ツールごとに渡すツールを選ぶと書くだけで、注釈には触れていない。 本文で annotation の語は出ない（検証者が HTML 本文を検索）。Salesforce（Slack の親会社）の公式ブログで、Slack の製品文書ではない。

### Salesforce — Agentforce MCP client（API Catalog への MCP サーバー登録）— forcedotcom/sf-skills の agentforce-generate skill

<a id="g-g3-saas-hosts-17"></a>
#### G3SH-17 Salesforce — Agentforce MCP client（API Catalog への MCP サーバー登録）— forcedotcom/sf-skills の agentforce-generate skill

- **資料**: mcp-management-reference.md（MCP Server Management Reference）（クライアントの文書）
- **URL**: https://github.com/forcedotcom/sf-skills/blob/d4a9aa448c7b743c1f1da41f41aa9723a6621232/skills/agentforce-generate/references/mcp-management-reference.md#L648-L652
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/forcedotcom/sf-skills/d4a9aa448c7b743c1f1da41f41aa9723a6621232/skills/agentforce-generate/references/mcp-management-reference.md
- **版**: forcedotcom/sf-skills commit d4a9aa4（2026-09-25）
- **書いてある場所**: mcp-management-reference.md L650-651（### sf agent mcp fetch）
- **原文**:

> Observed assets do NOT include `inputSchema`, `outputSchema`, or `annotations` —

- **日本語**: （sf agent mcp fetch で）観測した資産には inputSchema・outputSchema・annotations が含まれない。
- **どう使っているか**: AI エージェント向け skill の参照文書が、Agentforce の MCP 登録（sf agent mcp fetch）で観測した資産に annotations が含まれなかったと記録する。Agentforce の実行時に注釈を無視するかどうかは書いていない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、650 行（### sf agent mcp fetch）（取得 2026-10-02T22:11:33Z、sha256 a7835036c255…）
- **補足**: Salesforce 公式の skill（developer.salesforce.com/docs/ai/agentforce/guide/mcp.html から『MCP for Agentforce skill』としてリンク）。引用は L650 の行末から続く文の前半で、続きは『those fields were not returned by the live server. Do not rely on them being present.』。Agentforce の実行時に注釈で確認を出すかどうかは書いていない（不明）。同 skill の actions-reference.md では Agentforce のアクション確認は require_user_confirmation（既定 False）で、known-issues.md では Agent Script ではそれが実行時に効かない既知の問題が書かれている（grep で確認、ツール照合はしていない）。 同じファイルの ### Tool Metadata Fields（L896-899）は annotations を『custom metadata』とし、よくある例として category, rateLimit, cost, latency, destructive, requiresAuth を挙げる（MCP 標準の readOnlyHint 等ではない独自の名前。verify_quote.py で exact 確認）。 usage から ignored_or_not_used を外した。fetch の応答に annotations が無かったという観測であって、Agentforce が注釈を読まない・使わないとは書いていない。doc_type は client_docs のままだが、これは製品文書ではなく AI コーディングエージェント用 skill の参照文書（forcedotcom 組織）である点に注意。L898 の独自 annotations 名を notes に追記。

### Salesforce — Agentforce MCP client — forcedotcom/sf-skills の agentforce-generate skill

<a id="g-g3-saas-hosts-18"></a>
#### G3SH-18 Salesforce — Agentforce MCP client — forcedotcom/sf-skills の agentforce-generate skill

- **資料**: mcp-management-reference.md — 4. Fetch and Whitelist Assets (Interactive Tool Approval)（クライアントの文書）
- **URL**: https://github.com/forcedotcom/sf-skills/blob/d4a9aa448c7b743c1f1da41f41aa9723a6621232/skills/agentforce-generate/references/mcp-management-reference.md#L153-L208
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/forcedotcom/sf-skills/d4a9aa448c7b743c1f1da41f41aa9723a6621232/skills/agentforce-generate/references/mcp-management-reference.md
- **版**: forcedotcom/sf-skills commit d4a9aa4（2026-09-25）
- **書いてある場所**: mcp-management-reference.md L179-180（### 4. Fetch and Whitelist Assets (Interactive Tool Approval)）
- **原文**:

> a. **Display tool metadata clearly** (only render schema/annotations fields

- **日本語**: ツールのメタデータをはっきり表示する（スキーマや注釈の欄は、サーバーが実際に返したときだけ表示する）。
- **どう使っているか**: skill が AI エージェントに指示する対話手順で、管理者がツールを 1 件ずつ許可リストに入れる際、注釈があれば表示し（無ければ『None』）、ACTIVATE するかを人に聞く。同じファイルの ### Recommended Warnings（L955-967）には、破壊的なツールを有効にする前の CAUTION 表示の例があり、そこに Annotations: {"destructive": true, "scope": "all_records"}（MCP 標準ではない独自のキー）が示される。注釈を自動の許可・確認の判断に使うとは書いていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、179 行（### 4. Fetch and Whitelist Assets (Interactive Tool Approval)）（取得 2026-10-02T22:11:33Z、sha256 a7835036c255…）
- **補足**: 引用は L179 から L180 への折り返しの前半（L180 は『if the server actually returned them — they are often absent):』）。L174-L175 にも『annotations are NOT guaranteed to be present』とある。 これは Agentforce 製品の画面の挙動ではなく、skill（AI コーディングエージェント向けの手順書）が CLI を使って行う手順。L962-964 の警告例は verify_quote.py で exact 確認。 usage_ja の『見せるだけ』を修正：同じファイルの Recommended Warnings に、destructive の注釈（独自キー）を伴う有効化前の警告例がある。製品の挙動ではなく skill の手順である点を notes に明記。

### HubSpot — HubSpot Breeze agents の MCP client — HubSpot Marketplace の MCP サーバー掲載要件

<a id="g-g3-saas-hosts-19"></a>
#### G3SH-19 HubSpot — HubSpot Breeze agents の MCP client — HubSpot Marketplace の MCP サーバー掲載要件

- **資料**: MCP server listing requirements（規約・審査の指針）
- **URL**: https://developers.hubspot.com/docs/apps/developer-platform/list-apps/mcp-server-listing-requirements
- **書いてある見出しへ直接**: https://developers.hubspot.com/docs/apps/developer-platform/list-apps/mcp-server-listing-requirements#mcptools
- **版**: ページ表示『Last modified on September 10, 2026』、2026-10-02 取得
- **書いてある場所**: MCP server listing requirements > Listing requirements > MCP listing fields > mcpTools（#mcptools）
- **原文**:

> must accurately reflect what the tool can do with HubSpot or external data: any tool that can create, update, or delete data must be marked "write". "readOnly" is reserved for tools that never mutate data. When in doubt, use "write".

- **日本語**: （mcpTools の accessType は）HubSpot や外部のデータに対してツールができることを正確に反映しなければならない。データを作成・更新・削除できるツールは『write』。『readOnly』はデータを決して変えないツールだけ。迷ったら『write』。
- **どう使っているか**: MCP の ToolAnnotations ではなく、HubSpot 独自の掲載メタデータ mcpTools[].accessType（readOnly / write）を宣言させる。Ecosystem Quality チームが審査し（初回フィードバック 10 営業日以内）、迷えば write にせよと保守側を指示。
- **条件**: HubSpot Marketplace に MCP サーバー component 付きの standalone app を出す場合。第三者が他社の MCP サーバーへのコネクタを作ることは現在不可。
- **扱う宣言**:  ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP server listing requirements > Listing requirements > MCP listing fields > mcpTools」（取得 2026-10-02T22:11:25Z、sha256 caa2b0eb64c6…）
- **補足**: readOnlyHint と同じ意味の宣言を、サーバーの tools/list とは別の場所（app の project 設定）に二重に書かせる設計。readOnlyHint との対応づけや食い違いの確認は書いていない（不明）。ページには readOnlyHint / annotation / destructiveHint の語は無い（checked_no_mention）。.md 版（同 URL + .md）でも同文を確認（grep）。 提出後は Ecosystem Quality チームが component を審査し、初回フィードバックを 10 営業日以内に返すとある（同ページ『Submitting your MCP component for approval』）。accessType の正しさをどう確かめるか（実際に呼ぶか等）は書いていない。 version をページの最終更新日に更新。verification_or_lint は『EQ の審査対象の要件』という意味で残すが、accessType の検証方法は書かれていない旨を notes に追記。

### Make (Celonis) — Make MCP toolboxes（Make のシナリオを MCP ツールとして公開するサーバー側機能）

<a id="g-g3-saas-hosts-20"></a>
#### G3SH-20 Make (Celonis) — Make MCP toolboxes（Make のシナリオを MCP ツールとして公開するサーバー側機能）

- **資料**: MCP toolboxes（サーバの文書）
- **URL**: https://help.make.com/mcp-toolboxes
- **書いてある見出しへ直接**: https://help.make.com/mcp-toolboxes#configure-tools
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: MCP toolboxes > Manage your MCP toolbox > Configure tools（#configure-tools）
- **原文**:

> Select Read only and Read & write as tool annotations. In MCP clients that support them, annotations help clients understand how cautious to be with a tool, such as asking for permission before running it. By default, tools are Read & write.

- **日本語**: Behavior で『Read only』か『Read & write』をツール注釈として選ぶ。対応する MCP クライアントでは、注釈はツールをどれだけ慎重に扱うか（実行前に許可を求めるなど）の判断に使われる。既定ではツールは『Read & write』。
- **どう使っているか**: 注釈をコードではなく Make の UI で人が選ぶ。既定は Read & write（読み取り専用と宣言しない）。続く文で『データを読むだけなら Read only にせよ、クライアントがツールを速く実行できる』と書く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP toolboxes > Manage your MCP toolbox > Configure tools」（取得 2026-10-02T22:11:26Z、sha256 40301344eaa4…）
- **補足**: UI の『Read only』が tools/list でどの注釈（readOnlyHint: true か、destructiveHint も出すか）に写るかはページに書いていない（readOnlyHint への対応は推論）。宣言とシナリオの実際の動作の一致を Make が確かめるとは書いていない。Make が MCP クライアントになる側（apps.make.com/mcp-client）は注釈に触れていない（checked_no_mention）。.md 版は HTML 実体参照が混じるので HTML 版で照合。

### Dust (dust-tt) — Dust（業務向けエージェント SaaS、MCP クライアント。OSS）

<a id="g-g3-saas-hosts-21"></a>
#### G3SH-21 Dust (dust-tt) — Dust（業務向けエージェント SaaS、MCP クライアント。OSS）

- **資料**: front/lib/actions/constants.ts（MCP ツールの stake level）（クライアントのソースコード）
- **URL**: https://github.com/dust-tt/dust/blob/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/lib/actions/constants.ts#L44-L56
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/dust-tt/dust/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/lib/actions/constants.ts
- **版**: dust-tt/dust commit c5bb06b（2026-10-02 の HEAD）
- **書いてある場所**: front/lib/actions/constants.ts L54（stake level の定義 L44-L56 の中）
- **原文**:

> export const FALLBACK_MCP_TOOL_STAKE_LEVEL = "high" as const;

- **日本語**: MCP ツールの stake level の既定（フォールバック）は 'high'（毎回承認）。
- **どう使っているか**: Dust は確認の要否を MCP 注釈ではなく独自の stake level（high / medium / low / never_ask）で決める。管理者が設定していないリモート MCP サーバーのツールは 'high'（毎回の明示承認）に倒す。readOnlyHint を付けても確認は省かれない。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、54 行（取得 2026-10-02T22:12:00Z、sha256 2309fdbc9a37…）
- **補足**: GitHub コード検索（repo:dust-tt/dust、default branch の索引）で readOnlyHint・destructiveHint が出るのは sdks/js/src/raw_mcp_types.ts（型定義）の 1 ファイルだけ（finder の記録。検証者の sparse clone は front/ のみで、front/ では 4 つのヒント名は 0 件を git grep で確認）。front/lib/actions/mcp_metadata.ts L910-925 の extractMetadataFromTools は tools/list の各ツールから name, description, inputSchema, _meta だけを取り出し、annotations は捨てる（L911 を verify_quote.py で exact 確認）。stake の意味は front/lib/actions/tool_status.ts L37-42 のコメントによる：never_ask = 自動承認、low = 承認を求め『次から自動承認』を許す、medium = 引数値の組み合わせごとに承認、high = 毎回承認、未設定 = 既定（default tools は never_ask、その他は high）（L40 を verify_quote.py で exact 確認）。既知のリモートサーバーは URL ごとのプリセット（23）で上書きされる。 notes の stake の意味を訂正：medium は『エージェントごと』ではなく『引数値の組み合わせごと』（tool_status.ts L40 のコメント）。WebSearch 要約に頼っていた部分をコードのコメントに差し替え、extractMetadataFromTools が annotations を捨てる点（L910-925）を追記。

### Dust (dust-tt) — Dust（client-side MCP server）

<a id="g-g3-saas-hosts-22"></a>
#### G3SH-22 Dust (dust-tt) — Dust（client-side MCP server）

- **資料**: front/lib/actions/mcp_actions.ts（client-side MCP サーバーのツール一覧）（クライアントのソースコード）
- **URL**: https://github.com/dust-tt/dust/blob/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/lib/actions/mcp_actions.ts#L1413-L1426
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/dust-tt/dust/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/lib/actions/mcp_actions.ts
- **版**: dust-tt/dust commit c5bb06b
- **書いてある場所**: front/lib/actions/mcp_actions.ts L1424（client-side サーバーのツール一覧 L1413-L1426 の中）
- **原文**:

> dustMeta?.stake ?? DEFAULT_CLIENT_SIDE_MCP_TOOL_STAKE_LEVEL,

- **日本語**: stake level は、ツールの _meta.dust.stake があればそれ、無ければ client-side の既定値（'low'）。
- **どう使っているか**: 利用者の手元で動く client-side MCP サーバーでは、ツールが _meta の独自名前空間（dust.stake）で自己申告した stake をそのまま使い、無ければ 'low'。標準の ToolAnnotations は見ず、ベンダー独自の _meta を信じる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、1424 行（取得 2026-10-02T22:11:31Z、sha256 66bc1884aea1…）
- **補足**: getDustToolMeta（front/lib/actions/mcp_metadata.ts L878-）は _meta.dust の stake / displayLabels / editableArguments / argumentsRequiringApproval / timeoutMs を読む。サーバー側（リモート）の既定 'high'（21）と逆向きの既定である点に注意。 stake 'low' は『承認を求め、次から自動承認を許す』（tool_status.ts L39）であり、確認なしではない。 notes に 'low' の意味（初回は承認を求める）を追記。

### Dust (dust-tt) — Dust（リモート MCP サーバーのツール設定フォーム）

<a id="g-g3-saas-hosts-23"></a>
#### G3SH-23 Dust (dust-tt) — Dust（リモート MCP サーバーのツール設定フォーム）

- **資料**: front/components/actions/mcp/forms/mcpServerFormSchema.ts（getDefaultToolStakeLevel）（クライアントのソースコード）
- **URL**: https://github.com/dust-tt/dust/blob/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/components/actions/mcp/forms/mcpServerFormSchema.ts#L80-L93
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/dust-tt/dust/c5bb06bd7b9c025c1fc3aa130ffca3965c4b547a/front/components/actions/mcp/forms/mcpServerFormSchema.ts
- **版**: dust-tt/dust commit c5bb06b
- **書いてある場所**: front/components/actions/mcp/forms/mcpServerFormSchema.ts L86（getDefaultToolStakeLevel L80-L93 の中）
- **原文**:

> getDefaultRemoteMCPServerByURL(server.url)?.toolStakes?.[toolName] ??

- **日本語**: リモートサーバーのツールの既定 stake は、URL ごとに Dust が持つプリセットの toolStakes があればそれ、無ければフォールバック（'high'）。
- **どう使っているか**: 既知のリモート MCP サーバー（URL で判定）には Dust 側でツールごとの stake を手書きしたプリセットがあり、それ以外は high。サーバーの注釈ではなくクライアント側の一覧で危険度を決める。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、86 行（取得 2026-10-02T22:11:34Z、sha256 fc1e17db542e…）
- **補足**: プリセットの中身（getDefaultRemoteMCPServerByURL の一覧）は未確認。

### Atlassian — Atlassian Rovo（外部 MCP サーバーへのクライアント。Read-only MCP integrations）

<a id="g-g3-saas-hosts-24"></a>
#### G3SH-24 Atlassian — Atlassian Rovo（外部 MCP サーバーへのクライアント。Read-only MCP integrations）

- **資料**: Understand read-only MCP integrations（クライアントの文書）
- **URL**: https://support.atlassian.com/organization-administration/docs/understand-read-only-mcp-integrations/
- **書いてある見出しへ直接**: https://support.atlassian.com/organization-administration/docs/understand-read-only-mcp-integrations/#How-does-data-access-work
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Understand read-only MCP integrations > How does data access work?（#How-does-data-access-work）
- **原文**:

> By default, these integrations are read-only. You, as an admin, need to explicitly grant write access.

- **日本語**: 既定ではこれらの連携は読み取り専用。書き込みの権限は管理者が明示的に与える必要がある。
- **どう使っているか**: Rovo の既成の MCP 連携（GitHub, Sentry, New Relic, Notion など）は既定で read-only、write は管理者が明示的に許可する。どのツールが read / write かの判定根拠（MCP 注釈か Atlassian 側の分類か）は書いていない。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Understand read-only MCP integrations > How does data access work?」（取得 2026-10-02T22:13:02Z、sha256 a98f64da5b51…）
- **補足**: ページに readOnlyHint / destructiveHint の語は無く、annotation は script_only（表示テキスト外）だけ（checked_no_mention）。分類の根拠は不明。管理者はツールごとに有効 / 無効を切り替えられる（Configure tools for an external MCP server）。利用者向けには、第三者ツールへデータを送る前に承認を求める（Rovo Dev and MCP のページ）。

### Zapier — AI by Zapier（旧 Zapier Agents）のツール — Require approval before running

<a id="g-g3-saas-hosts-25"></a>
#### G3SH-25 Zapier — AI by Zapier（旧 Zapier Agents）のツール — Require approval before running

- **資料**: Add tools to your AI by Zapier step（クライアントの文書）
- **URL**: https://help.zapier.com/hc/en-us/articles/45863491098893-Add-tools-to-your-AI-by-Zapier-step
- **書いてある見出しへ直接**: https://help.zapier.com/hc/en-us/articles/45863491098893-Add-tools-to-your-AI-by-Zapier-step#h_01SETAPPROVALMODE
- **版**: 記事の更新日 2026-10-01
- **書いてある場所**: Add tools to your AI by Zapier step > 3. Add tools to your step > Require approval for a tool（#h_01SETAPPROVALMODE）
- **原文**:

> When you add or edit a tool, toggle on Require approval before running to pause the run and ask for your approval before AI by Zapier uses that tool. This toggle is off by default, so the tool runs without interruption unless you turn it on.

- **日本語**: ツールを追加・編集するとき『Require approval before running』をオンにすると、そのツールを使う前に実行を止めて承認を求める。この切り替えは既定でオフで、オンにしない限りツールは止まらずに実行される。
- **どう使っているか**: 承認の要否はツールごとの手動の切り替えで、既定はオフ（確認なし）。read / write の区別は利用者が判断して設定するよう勧めるだけで、注釈から既定を決めるとは書いていない。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Add tools to your AI by Zapier step > 3. Add tools to your step > Require approval for a tool」（取得 2026-10-02T22:11:32Z、sha256 f3e4aed0c981…）
- **補足**: ツールは Zapier の App action（MCP Client アプリの Run Tool なども App action として使える）。ページに readOnlyHint / annotation / destructiveHint の語は無い（checked_no_mention）。注釈を参照しているかは不明（少なくとも既定はツールの性質によらずオフ）。

### Zapier — Zapier MCP Client（Zap から外部 MCP サーバーのツールを呼ぶ統合、beta）

<a id="g-g3-saas-hosts-26"></a>
#### G3SH-26 Zapier — Zapier MCP Client（Zap から外部 MCP サーバーのツールを呼ぶ統合、beta）

- **資料**: Connect remote MCP servers to Zapier using MCP Client（クライアントの文書）
- **URL**: https://help.zapier.com/hc/en-us/articles/38777069364109-Connect-remote-MCP-servers-to-Zapier-using-MCP-Client
- **書いてある見出しへ直接**: https://help.zapier.com/hc/en-us/articles/38777069364109-Connect-remote-MCP-servers-to-Zapier-using-MCP-Client#h_01K2H8VYAAHTYXVT6NKDA4WNHV
- **版**: 記事の更新日 2026-08-21
- **書いてある場所**: Connect remote MCP servers to Zapier using MCP Client > Available triggers, searches, and actions > Searches（#h_01K2H8VYAAHTYXVT6NKDA4WNHV）
- **原文**:

> Run Read-Only Tool - Run a read-only tool, returning one or more results.

- **日本語**: Run Read-Only Tool — 読み取り専用のツールを実行し、1 件以上の結果を返す。
- **どう使っているか**: read-only のツールだけを Search（Run Read-Only Tool）やポーリングのトリガー（New Tool Result）に使い、それ以外は Action（Run Tool）。何をもって read-only とするか（readOnlyHint か）は書いていない。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect remote MCP servers to Zapier using MCP Client > Available triggers, searches, and actions > Searches」（取得 2026-10-02T22:11:29Z、sha256 19473b281d6a…）
- **補足**: トリガーは read-only ツールを繰り返し呼ぶ（ポーリング）ので、分類を readOnlyHint に頼っているなら、偽って readOnlyHint: true を付けたツールが繰り返し副作用を起こしうる。ただし判定根拠は不明。ページに annotation / readOnlyHint の語は無い（checked_no_mention）。

### HubSpot — HubSpot Breeze agents の MCP client（Connected apps のツール権限）

<a id="g-g3-saas-hosts-27"></a>
#### G3SH-27 HubSpot — HubSpot Breeze agents の MCP client（Connected apps のツール権限）

- **資料**: Connect apps to HubSpot's AI agents（クライアントの文書）
- **URL**: https://knowledge.hubspot.com/integrations/customize-breeze-agents-with-hubspot-mcp-client
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connect apps to HubSpot's AI agents > Configure connector permissions
- **原文**:

> Review the available read-only and write tools the app has access to.

- **日本語**: アプリが使える読み取り専用ツールと書き込みツールを確認する。
- **どう使っているか**: ツールを Read-only と Write の区分で表示し、ツールごと（または区分ごと一括）に Always allow / Ask permission / Never allow を設定する。区分の根拠は書いていない。
- **扱う宣言**:  ／ **使い方の分類**: 表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect apps to HubSpot's AI agents > Configure connector permissions」（取得 2026-10-02T22:11:29Z、sha256 fdf0d60bd280…）
- **補足**: Marketplace 掲載アプリでは mcpTools[].accessType（19）が区分の出どころと考えられるが、このページは根拠を書いていない（推論・不明）。既定の権限も書いていない。annotation / readOnlyHint の語は無い（checked_no_mention）。

### Glean — Glean Assistant / Glean Agents（MCP host）

<a id="g-g3-saas-hosts-28"></a>
#### G3SH-28 Glean — Glean Assistant / Glean Agents（MCP host）

- **資料**: Connect remote MCP servers to Glean（クライアントの文書）
- **URL**: https://docs.glean.com/administration/tools/connect-remote-mcp-servers-to-glean
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connect remote MCP servers to Glean
- **原文**:

> Users can engage with connected MCP servers through Glean Assistant and Glean Agents, with human‑in‑the‑loop experiences for write tools.

- **日本語**: 利用者は Glean Assistant と Glean Agents から接続済みの MCP サーバーを使え、書き込みツールには人を介在させる体験がある。
- **どう使っているか**: write ツールには human-in-the-loop（確認）がある、と書く。リモート MCP サーバーのツールが read か write かをどう決めるか（注釈か）は書いていない。
- **条件**: Glean は remote MCP サーバーを Glean（Assistant）では完全サポート、agents では beta サポートと書く（同ページの note）。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect remote MCP servers to Glean」（取得 2026-10-02T22:11:26Z、sha256 da2eca715d06…）
- **補足**: 関連ページ『Allowing in-line execution of write tools』は、管理者が『Run without user confirmation』を Yes にし、エージェント作成者が step ごとに opt-in し、さらにエンドユーザーが同意すれば、対応する write ツールを確認なしで実行できると書く（Known limitations：カスタムツールは対象外、supported write tools のみ。remote MCP のツールが対象に入るかは書いていない＝不明）。どちらのページにも annotation / readOnlyHint の語は無い（checked_no_mention）。分類の根拠は不明。 conditions に agents では beta である点を追記。関連ページの in-line 実行にはエンドユーザーの同意も要る点と、remote MCP ツールが対象か不明な点を notes に補った。

### Langdock — Langdock（業務向け AI プラットフォーム、MCP integration）

<a id="g-g3-saas-hosts-29"></a>
#### G3SH-29 Langdock — Langdock（業務向け AI プラットフォーム、MCP integration）

- **資料**: Model Context Protocol (MCP)（クライアントの文書）
- **URL**: https://docs.langdock.com/en/using-langdock/guides/integrations/mcp/mcp
- **書いてある見出しへ直接**: https://docs.langdock.com/en/using-langdock/guides/integrations/mcp/mcp#tool-integration
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Model Context Protocol (MCP) > Langdock MCP Key Features > Tool Integration（#tool-integration）
- **原文**:

> Confirmation: Newly saved tools and resources do not require confirmation before execution by default. You can enable confirmation per tool after saving if you need a confirmation step.

- **日本語**: 確認: 新しく保存したツールとリソースは、既定では実行前の確認が要らない。確認の段階が必要なら、保存後にツールごとに確認を有効にできる。
- **どう使っているか**: MCP ツールは既定で確認なし。確認はツールごとに手動で有効にする。注釈には触れていない。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > Langdock MCP Key Features > Tool Integration」（取得 2026-10-02T22:11:27Z、sha256 b0d50da69bd9…）
- **補足**: annotation / readOnlyHint / destructiveHint の語はページに無い（checked_no_mention）。注釈が無い（仕様の既定では destructive とみなされる）ツールでも確認なしで動く設定が既定、ということになる（注釈を読んでいないと断定はできない）。

### Atlassian — Rovo Dev CLI（MCP クライアント機能を持つ開発エージェント）

<a id="g-g3-saas-hosts-30"></a>
#### G3SH-30 Atlassian — Rovo Dev CLI（MCP クライアント機能を持つ開発エージェント）

- **資料**: Manage Rovo Dev CLI settings（クライアントの文書）
- **URL**: https://support.atlassian.com/rovo/docs/manage-rovo-dev-cli-settings/
- **書いてある見出しへ直接**: https://support.atlassian.com/rovo/docs/manage-rovo-dev-cli-settings/#Tools
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Manage Rovo Dev CLI settings > Configuration options > Tools（#Tools）
- **原文**:

> # Default permission for tools not explicitly listed (default: "ask")

- **日本語**: 明示的に列挙していないツールの既定の権限（既定: ask）。
- **どう使っているか**: toolPermissions はツール名ごとに allow / ask / deny を書き、列挙のないツールは ask（確認）。この既定は注釈の有無と関係なく、ツール名が設定に載っているかで決まる。MCP ツールにも同じ設定が効くかはこの節に明記が無い（推論）。注釈で既定を変えるとは書いていない。
- **扱う宣言**:  ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Manage Rovo Dev CLI settings > Configuration options > Tools」（取得 2026-10-02T22:11:38Z、sha256 bb31e48db3e6…）
- **補足**: 設定例は組み込みツール（open_files: allow, delete_file: ask など）と Atlassian ツール（getJiraIssue: allow, createJiraIssue: ask）を名前で列挙。Connect to an MCP server / Use tools のページも含め annotation / readOnlyHint の語は無い（checked_no_mention）。 usage_ja を明確化：defaults_when_missing は『設定に列挙が無いツール』の既定で、注釈が無いときの扱いではない。MCP ツールへの適用はページに明記なし。

### ServiceNow — ServiceNow AI Agents（AI Agent Studio。MCP client を含む）— Fluent SDK の手引き

<a id="g-g3-saas-hosts-31"></a>
#### G3SH-31 ServiceNow — ServiceNow AI Agents（AI Agent Studio。MCP client を含む）— Fluent SDK の手引き

- **資料**: Building AI Agents — Tools Guide（ServiceNow SDK docs 4.13.0）（クライアントの文書）
- **URL**: https://servicenow.github.io/sdk/guides/building-ai-agents-tools-guide
- **書いてある見出しへ直接**: https://servicenow.github.io/sdk/guides/building-ai-agents-tools-guide#execution-mode-and-display
- **版**: SDK docs Latest (4.13.0)、2026-10-02 取得
- **書いてある場所**: Building AI Agents - Tools Guide > Execution Mode and Display（#execution-mode-and-display）
- **原文**:

> Each tool has its own executionMode that overrides the agent-level setting for that specific tool. Default: "autopilot".

- **日本語**: 各ツールは自分の executionMode を持ち、エージェント全体の設定を上書きする。既定は『autopilot』。
- **どう使っているか**: 確認（copilot = 監督付き）か自動（autopilot）かはツールごとに作者が設定し、既定は autopilot（確認なし）。表で『CRUD lookup は autopilot、create / update / delete は copilot』と人が選ぶ指針を示す。注釈には触れていない。
- **扱う宣言**:  ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Building AI Agents - Tools Guide > Execution Mode and Display > executionMode (copilot vs autopilot)」（取得 2026-10-02T22:11:38Z、sha256 7e8edfd8147f…）
- **補足**: この手引きは CRUD / script / OOB / RAG ツールが対象で、MCP ツールの executionMode の既定や注釈の扱いは書いていない（不明）。ServiceNow の MCP 関係の公開情報（community 記事）は AI Control Tower でのサーバー単位の承認を書くが、ツール注釈には触れていない（checked_no_mention）。

---

[← 付録 G-8 エージェントの枠組み・利用者向けアプリ・モデルの API](appendix-g-8.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-10 ゲートウェイ・実行基盤・宣言を検査する道具・登録所 →](appendix-g-10.md)
