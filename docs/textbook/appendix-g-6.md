[← 付録 G-5 OpenAI](appendix-g-5.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-7 エディタとコーディングエージェント →](appendix-g-7.md)

---

# 付録 G-6 Google と AWS

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-6-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C06-01](#g-c06-google-aws-01) | Google — Gemini CLI — ポリシーエンジン（TOML ルール） | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [C06-02](#g-c06-google-aws-02) | Google — Gemini CLI — Plan Mode | 公式の文書 | 確認を求める・規則（ポリシー）の条件に使う・確認を省く（自動で許可） | [確認] |
| [C06-03](#g-c06-google-aws-03) | Google — Gemini CLI — Plan Mode | 公式の文書 | ツールを絞る・隠す | [確認] |
| [C06-64](#g-c06-google-aws-64) | Google — Gemini CLI — Plan Mode | issue / PR / 提案の下書き | 信頼するなという注意 | [未確認] |
| [C06-04](#g-c06-google-aws-04) | Google — Gemini CLI — 組み込み Plan Mode ポリシー（plan.toml） | クライアントのソースコード | 確認を求める・ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [C06-05](#g-c06-google-aws-05) | Google — Gemini CLI — 組み込み Plan Mode ポリシー（plan.toml） | クライアントのソースコード | 宣言が無いときの扱い・ツールを絞る・隠す | [確認] |
| [C06-06](#g-c06-google-aws-06) | Google — Gemini CLI — ポリシーエンジン実装 | クライアントのソースコード | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C06-07](#g-c06-google-aws-07) | Google — Gemini CLI — ポリシーエンジン実装 | クライアントのソースコード | ツールを絞る・隠す | [確認] |
| [C06-08](#g-c06-google-aws-08) | Google — Gemini CLI — MCP クライアント | クライアントのソースコード | そのまま渡す・見せる | [確認] |
| [C06-09](#g-c06-google-aws-09) | Google — Gemini CLI — ツール実行前のポリシー判定 | クライアントのソースコード | 規則（ポリシー）の条件に使う | [確認] |
| [C06-10](#g-c06-google-aws-10) | Google — Gemini CLI — ブラウザエージェント（実験的） | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [C06-11](#g-c06-google-aws-11) | Google — Gemini CLI — 確認バス（message bus） | クライアントのソースコード | 信頼するなという注意・その他 | [確認] |
| [C06-12](#g-c06-google-aws-12) | Google — Gemini CLI — リリースノート | リリースノート | 規則（ポリシー）の条件に使う | [確認] |
| [C06-13](#g-c06-google-aws-13) | Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [C06-14](#g-c06-google-aws-14) | Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM | 公式の文書 | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C06-15](#g-c06-google-aws-15) | Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM | 公式の文書 | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C06-16](#g-c06-google-aws-16) | Google — Google の MCP サーバー参照ドキュメント（Developer Knowledge MCP ほか共通の説明） | 公式の文書 | 信頼するなという注意・確認を求める・表示（印・名前） | [確認] |
| [C06-17](#g-c06-google-aws-17) | Google Cloud — Cloud Run リモート MCP サーバー（run.googleapis.com） | 公式の文書 | 表示（印・名前） | [確認] |
| [C06-18](#g-c06-google-aws-18) | Google Cloud — gcloud リモート MCP サーバー（cloudcli.googleapis.com） | 公式の文書 | 表示（印・名前） | [確認] |
| [C06-19](#g-c06-google-aws-19) | Google Cloud — Gemini Enterprise — カスタム MCP サーバーのデータストア（actions） | 公式の文書 | 確認を求める・宣言が無いときの扱い | [確認] |
| [C06-20](#g-c06-google-aws-20) | Google Cloud — Gemini Enterprise — カスタム MCP サーバーのデータストア（actions） | 公式の文書 | 確認を省く（自動で許可）・作者への書き方の案内 | [確認] |
| [C06-21](#g-c06-google-aws-21) | Google Cloud — Gemini Enterprise Agent Platform — Agent Gateway の IAM ポリシー | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [C06-22](#g-c06-google-aws-22) | Google Cloud — Gemini Enterprise Agent Platform — Agent Gateway の IAM ポリシー | 公式の文書 | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C06-23](#g-c06-google-aws-23) | Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab） | 公式ブログ | 規則（ポリシー）の条件に使う | [確認] |
| [C06-24](#g-c06-google-aws-24) | Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab） | 公式ブログ | 規則（ポリシー）の条件に使う・その他 | [確認] |
| [C06-25](#g-c06-google-aws-25) | Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab） | 公式ブログ | 規則（ポリシー）の条件に使う | [確認] |
| [C06-26](#g-c06-google-aws-26) | Google Cloud — Agent Registry — MCP サーバー登録（tool spec の JSON） | 公式の文書 | 作者への書き方の案内・宣言が無いときの扱い | [確認] |
| [C06-27](#g-c06-google-aws-27) | Google Cloud — Agent Registry — MCP サーバー登録 | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C06-28](#g-c06-google-aws-28) | Google Cloud — Agent Registry MCP サーバー（agentregistry.googleapis.com） | 公式の文書 | そのまま渡す・見せる・宣言が無いときの扱い | [確認] |
| [C06-29](#g-c06-google-aws-29) | Google Cloud — Cloud API Registry — McpTool 型（クライアントライブラリ参照） | SDK の文書 | その他 | [確認] |
| [C06-30](#g-c06-google-aws-30) | Google — MCP Toolbox for Databases（googleapis/genai-toolbox） | サーバの文書 | 作者への書き方の案内 | [確認] |
| [C06-31](#g-c06-google-aws-31) | Google — MCP Toolbox for Databases | サーバの文書 | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C06-35](#g-c06-google-aws-35) | Google — MCP Toolbox for Databases | サーバのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C06-36](#g-c06-google-aws-36) | Google — MCP Toolbox for Databases | サーバのソースコード | 宣言を検査する・作者への書き方の案内 | [確認] |
| [C06-32](#g-c06-google-aws-32) | Google — MCP Toolbox for Databases — 読み取り専用モード | サーバの文書 | 確認を省く（自動で許可）・作者への書き方の案内 | [確認] |
| [C06-33](#g-c06-google-aws-33) | Google — MCP Toolbox for Databases — 読み取り専用モード | サーバの文書 | ツールを絞る・隠す | [確認] |
| [C06-34](#g-c06-google-aws-34) | Google — MCP Toolbox for Databases — 読み取り専用モード | サーバの文書 | 信頼するなという注意 | [確認] |
| [C06-37](#g-c06-google-aws-37) | Google — MCP Toolbox for Databases — BigQuery | サーバの文書 | ツールを絞る・隠す・宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C06-38](#g-c06-google-aws-38) | Google — MCP Toolbox for Databases — BigQuery ソース | サーバの文書 | その他・ツールを絞る・隠す | [確認] |
| [C06-39](#g-c06-google-aws-39) | Google — Agent Development Kit（ADK, Python）— ADK ツールを MCP ツールに変換 | SDK のソースコード | 使わない・読まない・宣言が無いときの扱い | [確認] |
| [C06-40](#g-c06-google-aws-40) | Google — Google Analytics MCP サーバー（googleanalytics/google-analytics-mcp） | サーバのソースコード | 使わない・読まない | [確認] |
| [C06-41](#g-c06-google-aws-41) | Google — Agent Development Kit（ADK, Python）— MCP クライアント（McpTool） | SDK のソースコード | 使わない・読まない | [確認] |
| [C06-42](#g-c06-google-aws-42) | Google — Agent Development Kit（ADK, Go）— Agent Registry クライアント | SDK のソースコード | 宣言が無いときの扱い・そのまま渡す・見せる | [確認] |
| [C06-43](#g-c06-google-aws-43) | Google（adk.dev に掲載。対象は ClickHouse のサーバー） — ADK ドキュメント — ClickHouse Cloud MCP 連携ページ | 公式の文書 | その他 | [確認] |
| [C06-44](#g-c06-google-aws-44) | Google（Firebase） — Firebase MCP サーバー（firebase-tools の src/mcp） | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C06-45](#g-c06-google-aws-45) | AWS（Strands Agents） — Strands Agents SDK（Python） | SDK のソースコード | 信頼するなという注意・宣言が無いときの扱い・そのまま渡す・見せる | [確認] |
| [C06-46](#g-c06-google-aws-46) | AWS（Strands Agents） — Strands Agents SDK（Python）— MCP ツール | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C06-47](#g-c06-google-aws-47) | AWS（Strands Agents） — Strands Agents SDK（TypeScript） | SDK のソースコード | 信頼するなという注意・そのまま渡す・見せる | [確認] |
| [C06-48](#g-c06-google-aws-48) | AWS — MCP Proxy for AWS（mcp-proxy-for-aws）— --read-only | ゲートウェイのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C06-49](#g-c06-google-aws-49) | AWS — MCP Proxy for AWS — --read-only | ゲートウェイのソースコード | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [C06-50](#g-c06-google-aws-50) | AWS — MCP Proxy for AWS — リリースノート | リリースノート | ツールを絞る・隠す | [確認] |
| [C06-51](#g-c06-google-aws-51) | AWS — Amazon EKS マネージド MCP サーバー（プロキシ経由の設定） | 公式の文書 | ツールを絞る・隠す | [確認] |
| [C06-52](#g-c06-google-aws-52) | AWS — MCP Proxy for AWS — CLI ヘルプ | ゲートウェイのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認] |
| [C06-53](#g-c06-google-aws-53) | AWS — MCP Proxy for AWS — 一般提供の告知 | 公式ブログ | ツールを絞る・隠す | [確認] |
| [C06-54](#g-c06-google-aws-54) | AWS（awslabs） — AWS API MCP Server（awslabs/mcp の aws-api-mcp-server） | サーバのソースコード | その他・作者への書き方の案内 | [確認] |
| [C06-55](#g-c06-google-aws-55) | AWS（awslabs） — AWS API MCP Server — README | サーバの文書 | その他 | [確認] |
| [C06-56](#g-c06-google-aws-56) | AWS（awslabs） — CloudWatch Application Signals MCP Server（dynamic instrumentation ツール群） | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C06-57](#g-c06-google-aws-57) | AWS（awslabs） — AWS Transform MCP Server | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C06-58](#g-c06-google-aws-58) | AWS（awslabs） — Amazon Redshift MCP Server | サーバのソースコード | 作者への書き方の案内 | [確認] |
| [C06-59](#g-c06-google-aws-59) | AWS — Amazon Bedrock AgentCore Gateway | 公式ブログ | そのまま渡す・見せる | [確認] |
| [C06-60](#g-c06-google-aws-60) | AWS — Amazon Q Developer CLI — MCP のセキュリティ | 公式の文書 | その他 | [確認] |
| [C06-61](#g-c06-google-aws-61) | AWS — Amazon Q Developer — MCP の説明 | 公式の文書 | その他 | [確認] |
| [C06-62](#g-c06-google-aws-62) | AWS — Amazon Q Developer CLI（オープンソース版） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C06-63](#g-c06-google-aws-63) | AWS — AWS Prescriptive Guidance — MCP strategies | 規約・審査の指針 | 作者への書き方の案内 | [確認] |
| [C06-65](#g-c06-google-aws-65) | Google — Google Security Operations MCP（google/mcp-security の secops-mcp） | issue / PR / 提案の下書き | 確認を求める・作者への書き方の案内 | [未確認] |
| [C06-66](#g-c06-google-aws-66) | Google — Google Analytics MCP サーバー | issue / PR / 提案の下書き | 作者への書き方の案内 | [未確認] |
| [C06-67](#g-c06-google-aws-67) | AWS（awslabs） — mcp-lambda-handler（awslabs/mcp） | issue / PR / 提案の下書き | その他 | [未確認] |

この分冊の資料は 67 件で、うち [確認] は 63 件、[確認（調査時のみ）] は 0 件。

<a id="ag-6-1"></a>
## 資料カード

### Google — Gemini CLI — ポリシーエンジン（TOML ルール）

<a id="g-c06-google-aws-01"></a>
#### C06-01 Google — Gemini CLI — ポリシーエンジン（TOML ルール）

- **資料**: Policy engine（TOML rule schema）（公式の文書）
- **URL**: https://geminicli.com/docs/reference/policy-engine/
- **書いてある見出しへ直接**: https://geminicli.com/docs/reference/policy-engine/#toml-rule-schema
- **版**: 2026-10-02 取得（geminicli.com。版表示なし。ソースは google-gemini/gemini-cli @ fb972b2f の docs/）
- **書いてある場所**: Policy engine > Configuration > TOML rule schema (#toml-rule-schema)
- **原文**:

> # (Optional) Metadata hints provided by the tool. A rule matches if all # key-value pairs provided here are present in the tool's annotations. toolAnnotations = { readOnlyHint = true }

- **日本語**: （任意）ツールが出すメタデータのヒント。ここに書いたキーと値の組がすべてツールの annotations にあれば、そのルールが当たる。toolAnnotations = { readOnlyHint = true }
- **どう使っているか**: Gemini CLI のポリシールール（allow / deny / ask_user を決める TOML）に toolAnnotations という条件欄があり、MCP ツールの annotations の値でルールを当てる。宣言そのものがポリシーの入力になる。
- **条件**: ルールを書くのは利用者・管理者。既定の組み込みポリシーで toolAnnotations を使うのは Plan Mode 用の plan.toml だけ（packages/core/src/policy/policies/*.toml を grep。read-only.toml / write.toml / yolo.toml 等には無い）。つまり既定（default モード）では annotations で自動許可はされない。同じ MCP サーバーに trust: true を付けると確認が全部飛ぶ（同じ docs の mcp-server ページ、verify 済み: "trust (boolean): When true, bypasses all tool call confirmations for this server (default: false)"）。 ただし trust の allow ルール（TRUSTED_MCP_SERVER_PRIORITY）は modes: nonPlanModes で作られるので、Plan Mode では trust でも確認・拒否は飛ばない（packages/core/src/policy/config.ts @ fb972b2f を curl で目視、引用は未照合）。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Policy engine > Configuration > TOML rule schema」（取得 2026-10-02T22:12:51Z、sha256 e109a72b19e1…）
- **補足**: HTML の code block 内のコメント行なので、# を含めた形で照合した（exact）。.md 版（https://geminicli.com/docs/reference/policy-engine.md）でも 305-307 行で exact。 組み込みポリシー 9 ファイル（agents / conseca / discovered / non-interactive / plan / read-only / sandbox-default / write / yolo）を pin で取得し、toolAnnotations・readOnlyHint を含むのは plan.toml だけであることを再確認。trust が Plan Mode では効かない点を conditions に追記（trust で「確認が全部飛ぶ」は Plan Mode 以外に限る）。

### Google — Gemini CLI — Plan Mode

<a id="g-c06-google-aws-02"></a>
#### C06-02 Google — Gemini CLI — Plan Mode

- **資料**: Plan Mode（Example: Automatically approve read-only MCP tools）（公式の文書）
- **URL**: https://geminicli.com/docs/cli/plan-mode/
- **書いてある見出しへ直接**: https://geminicli.com/docs/cli/plan-mode/#example-automatically-approve-read-only-mcp-tools
- **版**: 2026-10-02 取得（geminicli.com。版表示なし。ソースは google-gemini/gemini-cli @ fb972b2f の docs/）
- **書いてある場所**: Plan Mode > Customization and best practices > Custom policies > Example: Automatically approve read-only MCP tools (#example-automatically-approve-read-only-mcp-tools)
- **原文**:

> By default, read-only MCP tools require user confirmation in Plan Mode. You can use toolAnnotations and the mcpName wildcard to customize this behavior for your specific environment.

- **日本語**: 既定では、Plan Mode で読み取り専用の MCP ツールを使うにはユーザーの確認が要る。toolAnnotations と mcpName のワイルドカードで、この動きを自分の環境に合わせて変えられる。
- **どう使っているか**: Plan Mode（読み取り専用の計画モード）では readOnlyHint:true の MCP ツールだけが「確認つきで」使える。利用者が toolAnnotations = { readOnlyHint = true }、decision = "allow"、modes = ["plan"] のルールを足すと、確認なしの自動許可にできる（例の TOML がページにある）。
- **条件**: Plan Mode のときだけ。自動許可は利用者が ~/.gemini/policies/ にルールを足した場合だけ（既定は ask_user）。非対話（non-interactive）では ask_user は deny になる（plan.toml のコメント）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Plan Mode > Customization and best practices > Custom policies > Example: Automatically approve read-only MCP tools」（取得 2026-10-02T22:11:32Z、sha256 21b1f15bb62e…）
- **補足**: 「read-only MCP tools」が何で判定されるかはこの文には書かれていないが、組み込みの plan.toml（C06_google_aws-04）で readOnlyHint = true の一致だと分かる。サーバーが申告した readOnlyHint を検証せずに使うことを問題にした issue #28548 がある（C06_google_aws-64, 未確認）。

<a id="g-c06-google-aws-03"></a>
#### C06-03 Google — Gemini CLI — Plan Mode

- **資料**: Plan Mode（Available tools 一覧）（公式の文書）
- **URL**: https://geminicli.com/docs/cli/plan-mode/
- **書いてある見出しへ直接**: https://geminicli.com/docs/cli/plan-mode/#tool-restrictions
- **版**: 2026-10-02 取得（geminicli.com。版表示なし。ソースは google-gemini/gemini-cli @ fb972b2f の docs/）
- **書いてある場所**: Plan Mode > Tool Restrictions (#tool-restrictions)
- **原文**:

> Read-only MCP tools (for example, github_read_issue, postgres_read_schema) and core MCP resource tools (list_mcp_resources, read_mcp_resource) are allowed.

- **日本語**: 読み取り専用の MCP ツール（例: github_read_issue、postgres_read_schema）と、核となる MCP リソースツール（list_mcp_resources、read_mcp_resource）は使ってよい。
- **どう使っているか**: Plan Mode で使えるツールの一覧に「読み取り専用の MCP ツール」が入る。読み取り専用でない MCP ツールは Plan Mode では使えない（一覧に無く、組み込みルールで deny）。
- **条件**: Plan Mode のときだけ。ここでの「allowed」は確認なしの意味ではなく、C06_google_aws-02 / C06_google_aws-04 のとおり ask_user（確認つき）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Plan Mode > Tool Restrictions」（取得 2026-10-02T22:11:32Z、sha256 21b1f15bb62e…）
- **補足**: 判定に readOnlyHint を使うことはこのページの別の節（C06_google_aws-02）と plan.toml（C06_google_aws-04）から分かる。

<a id="g-c06-google-aws-64"></a>
#### C06-64 Google — Gemini CLI — Plan Mode

- **資料**: Plan Mode: the read-only restriction for MCP tools depends on an unverified, server-controlled annotation · Issue #28548 · google-gemini/gemini-cli（issue / PR / 提案の下書き）
- **URL**: https://github.com/google-gemini/gemini-cli/issues/28548
- **版**: 不明（2026-10-02 の WebSearch 結果）
- **書いてある場所**: 不明（本文未取得）
- **原文**:

> Plan Mode: the read-only restriction for MCP tools depends on an unverified, server-controlled annotation

- **日本語**: Plan Mode: MCP ツールの読み取り専用の制限が、検証されていない、サーバーが決める annotation に頼っている
- **どう使っているか**: Plan Mode の制限（C06_google_aws-04）が MCP サーバーの自己申告の readOnlyHint に依存する、という指摘の issue。WebSearch の要約では「悪意あるサーバーが破壊的ツールに readOnlyHint:true を付ければ Plan Mode で提示される」趣旨。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [未確認] 未実施: github.com の HTML はこの環境でブロック（2026-10-02 も 403）。quote は WebSearch 結果のタイトル。
- **補足**: WebSearch の結果タイトルだけ（2026-10-02）。github.com はこの環境でブロックのため本文・状態（open / closed）・対応は未確認。

### Google — Gemini CLI — 組み込み Plan Mode ポリシー（plan.toml）

<a id="g-c06-google-aws-04"></a>
#### C06-04 Google — Gemini CLI — 組み込み Plan Mode ポリシー（plan.toml）

- **資料**: packages/core/src/policy/policies/plan.toml（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policies/plan.toml#L83-L92
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policies/plan.toml
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 83-92
- **原文**:

```
# Explicitly allowed tools in Plan Mode (interactive: ask user, non-interactive: deny)
# Priority 50 overrides the catch-all (40) and also ensures we override default tier ALLOW rules (e.g. from read-only.toml).

[[rule]]
toolName = "*"
mcpName = "*"
toolAnnotations = { readOnlyHint = true }
decision = "ask_user"
priority = 50
modes = ["plan"]
```

- **日本語**: Plan Mode で明示的に許すツール（対話時はユーザーに確認、非対話時は拒否）。優先度 50 は全体拒否（40）より強い。すべての MCP サーバーのすべてのツールのうち、annotations が readOnlyHint = true のものは ask_user（確認する）、Plan Mode に限る。
- **どう使っているか**: 組み込みポリシーそのもの。Plan Mode では、readOnlyHint = true を宣言した MCP ツールだけが「ユーザー確認つきで実行可」に引き上げられる。宣言の値がそのまま実行可否の分かれ目。
- **条件**: modes = ["plan"]、interactive = true（ファイル内の次の行）。非対話モードでは deny。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、83-92 行（# Explicitly allowed tools in Plan Mode (interactive: ask user, non-interactive: deny)）（取得 2026-10-02T22:11:34Z、sha256 cbc98437f7a0…）
- **補足**: 次の entry（C06_google_aws-05）の全体拒否ルール（priority 40）と組で読む。annotations の値は MCP サーバーの自己申告で、検証はしない（mcp-client.ts でそのまま渡す、C06_google_aws-08）。

<a id="g-c06-google-aws-05"></a>
#### C06-05 Google — Gemini CLI — 組み込み Plan Mode ポリシー（plan.toml）

- **資料**: packages/core/src/policy/policies/plan.toml（Catch-All）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policies/plan.toml#L74-L80
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policies/plan.toml
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 74-80
- **原文**:

```
# Catch-All: Deny everything by default in Plan mode.

[[rule]]
toolName = "*"
decision = "deny"
priority = 40
modes = ["plan"]
```

- **日本語**: 全体のとりで: Plan Mode では既定ですべてを拒否する。（toolName = "*"、decision = "deny"、priority = 40、modes = ["plan"]）
- **どう使っているか**: annotations が無い、または readOnlyHint が true でない MCP ツールは、C06_google_aws-04 のルールに当たらずこの全体拒否に落ちる。宣言が無いときは「書き込みかもしれない」として Plan Mode から締め出す（安全側の既定）。
- **条件**: Plan Mode のときだけ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、74-80 行（# Catch-All: Deny everything by default in Plan mode.）（取得 2026-10-02T22:11:34Z、sha256 cbc98437f7a0…）
- **補足**: policy-engine.ts の照合（C06_google_aws-06）は値の厳密一致なので、readOnlyHint が無い・false・"true"（文字列）のどれでも C06_google_aws-04 に当たらない。 検証者補足: settings 由来の allow（trust=true のサーバー＝user 層 4.2、allowed リスト＝4.1 など）は config.ts で modes: nonPlanModes が付くので、Plan Mode の全体拒否（1.040）を上書きしない。Plan Mode で annotations 以外の経路で MCP ツールが通るのは、利用者・管理者が modes に plan を含むルールを足したときだけ（コードからの読み）。 trust 等の設定由来ルールが Plan Mode に効かないことを config.ts で確かめ、notes に追記（主張を補強）。

### Google — Gemini CLI — ポリシーエンジン実装

<a id="g-c06-google-aws-06"></a>
#### C06-06 Google — Gemini CLI — ポリシーエンジン実装

- **資料**: packages/core/src/policy/policy-engine.ts（ruleMatches）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policy-engine.ts#L202-L212
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policy-engine.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 202-212
- **原文**:

```
  // Check annotations if specified
  if (rule.toolAnnotations) {
    if (!toolAnnotations) {
      return false;
    }
    for (const [key, value] of Object.entries(rule.toolAnnotations)) {
      if (toolAnnotations[key] !== value) {
        return false;
      }
    }
  }
```

- **日本語**: （ルールに annotations の条件があれば調べる）ツールに annotations が無ければ当たらない。ルールに書いた各キーについて、ツールの annotations の値が違えば当たらない。
- **どう使っているか**: toolAnnotations 条件の照合規則。キーごとに !== で厳密に比べ、annotations が無いツールは annotations 条件つきのルールに一切当たらない。
- **条件**: toolAnnotations を書いたルールだけに効く。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、202-212 行（取得 2026-10-02T22:11:33Z、sha256 3b7118ceadaa…）
- **補足**: MCP の既定値（destructiveHint 省略時 true など）を補わない。だから toolAnnotations = { destructiveHint = true } のルールは、destructiveHint を省略した（仕様上は true 扱いの）ツールには当たらない。これは本調査の読み（コードから）で、ドキュメントには書かれていない。

<a id="g-c06-google-aws-07"></a>
#### C06-07 Google — Gemini CLI — ポリシーエンジン実装

- **資料**: packages/core/src/policy/policy-engine.ts（getExcludedTools の説明）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policy-engine.ts#L1030-L1035
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/policy/policy-engine.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 1030-1035
- **原文**:

```
   * Get tools that are effectively denied by the current rules.
   * This takes into account:
   * 1. Global rules (no argsPattern)
   * 2. Priority order (higher priority wins)
   * 3. Non-interactive mode (ASK_USER becomes DENY)
   * 4. Annotation-based rules (when toolMetadata is provided)
```

- **日本語**: 今のルールで実質的に拒否されるツールを求める。考えに入れるのは: 1. 全体ルール（argsPattern なし） 2. 優先度の順 3. 非対話モード（ASK_USER は DENY になる） 4. annotations にもとづくルール（toolMetadata が渡されたとき）
- **どう使っているか**: annotations にもとづくルールで無条件に deny になるツールは、tool-registry.ts（buildToolMetadata → getExcludeTools）でモデルに渡すツール一覧から外される。つまり Plan Mode では readOnlyHint:true でない MCP ツールはモデルから見えなくなる。
- **条件**: toolMetadata が渡されたとき（tool-registry.ts の getActiveTools は渡している）。同じ関数のコメント: toolMetadata が無いときは annotations 条件つきルールを飛ばす（conservative fallback）。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、1030-1035 行（取得 2026-10-02T22:11:33Z、sha256 3b7118ceadaa…）
- **補足**: tool-registry.ts の buildToolMetadata は tool.toolAnnotations をコピーし、MCP ツールには _serverName を足して渡す（同じ commit で確認、引用は未照合）。

### Google — Gemini CLI — MCP クライアント

<a id="g-c06-google-aws-08"></a>
#### C06-08 Google — Gemini CLI — MCP クライアント

- **資料**: packages/core/src/tools/mcp-client.ts（ツール発見）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/tools/mcp-client.ts#L1366-L1368
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/tools/mcp-client.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 1366-1368
- **原文**:

```
        // Extract annotations from the tool definition
        const annotations = toolDef.annotations;
        const isReadOnly = annotations?.readOnlyHint === true;
```

- **日本語**: ツール定義から annotations を取り出す。isReadOnly は readOnlyHint === true のときだけ真。
- **どう使っているか**: MCP サーバーの tools/list の annotations を検証せずにそのまま DiscoveredMCPTool に持たせ（toolAnnotations）、ポリシー照合に使う。readOnlyHint は真偽値 true のときだけ読み取り専用とみなす。
- **条件**: すべての MCP サーバー。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、1366-1368 行（取得 2026-10-02T22:11:35Z、sha256 99ca252a52e8…）
- **補足**: isReadOnly（DiscoveredMCPTool の getter）を読む箇所は packages/ 以下の grep では見つからなかった（tools.ts の既定 getter と上書きだけ）。実際に効くのは toolAnnotations 経由のポリシー照合（C06_google_aws-04, C06_google_aws-06, C06_google_aws-09）。

### Google — Gemini CLI — ツール実行前のポリシー判定

<a id="g-c06-google-aws-09"></a>
#### C06-09 Google — Gemini CLI — ツール実行前のポリシー判定

- **資料**: packages/core/src/scheduler/policy.ts（checkPolicy）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/scheduler/policy.ts#L63-L72
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/scheduler/policy.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 63-72
- **原文**:

```
  const toolAnnotations = toolCall.tool.toolAnnotations;

  const result = await config
    .getPolicyEngine()
    .check(
      { name: toolCall.request.name, args: toolCall.request.args },
      serverName,
      toolAnnotations,
      subagent,
    );
```

- **日本語**: ツールの toolAnnotations を取り、ツール名・引数・サーバー名・annotations・サブエージェント名をポリシーエンジンの check に渡す。
- **どう使っているか**: ツール呼び出しのたびに、そのツールの annotations がポリシー判定（allow / deny / ask_user）の入力になる。
- **条件**: すべてのツール呼び出し。ACP 経由（packages/cli/src/acp/acpSession.ts）も同じ形で annotations を渡す（grep で確認、引用は未照合）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、63-72 行（取得 2026-10-02T22:11:42Z、sha256 b299bc6f2a24…）

### Google — Gemini CLI — ブラウザエージェント（実験的）

<a id="g-c06-google-aws-10"></a>
#### C06-10 Google — Gemini CLI — ブラウザエージェント（実験的）

- **資料**: packages/core/src/agents/browser/browserAgentFactory.ts（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/agents/browser/browserAgentFactory.ts#L136-L139
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/agents/browser/browserAgentFactory.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 136-139
- **原文**:

```
      // Reduce noise for read-only tools in default mode
      const readOnlyTools = (await browserManager.getDiscoveredTools())
        .filter((t) => !!t.annotations?.readOnlyHint)
        .map((t) => t.name);
```

- **日本語**: 既定モードで読み取り専用ツールの確認の手間を減らす。ブラウザ用に見つけたツールのうち annotations.readOnlyHint が真のものの名前を集める。
- **どう使っているか**: ブラウザエージェントが使う MCP ツールのうち readOnlyHint が真のものに allow ルールを足し、既定モードでも確認なしで実行させる（take_snapshot / take_screenshot も名前で allow）。
- **条件**: 実験的なブラウザエージェントを使うときだけ（changelog v0.31.0 で導入）。そのブラウザ用 MCP サーバーのツールに限る。同じ関数で、設定 confirmSensitiveActions のとき upload_file / evaluate_script は ask_user にする。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、136-139 行（取得 2026-10-02T22:12:57Z、sha256 9552f7cbe361…）
- **補足**: 判定は !!readOnlyHint（真偽値に変換）なので、他の箇所の === true より緩い（"true" 文字列なども真になる）。コードからの読み。

### Google — Gemini CLI — 確認バス（message bus）

<a id="g-c06-google-aws-11"></a>
#### C06-11 Google — Gemini CLI — 確認バス（message bus）

- **資料**: packages/core/src/confirmation-bus/message-bus.ts（derive）（クライアントのソースコード）
- **URL**: https://github.com/google-gemini/gemini-cli/blob/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/confirmation-bus/message-bus.ts#L57-L59
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-gemini/gemini-cli/fb972b2f87fe7d5b06d37eac711490162d98de2c/packages/core/src/confirmation-bus/message-bus.ts
- **版**: google-gemini/gemini-cli @ fb972b2f87fe7d5b06d37eac711490162d98de2c（package.json: 0.64.0-nightly.20260929）
- **書いてある場所**: lines 57-59
- **原文**:

```
        // Sanitization for untrusted callers:
        // 1. Remove forcedDecision to prevent policy bypass.
        // 2. Remove metadata (serverName, toolAnnotations, details) to prevent spoofing.
```

- **日本語**: 信頼できない呼び出し元への消毒: 1. ポリシーのすり抜けを防ぐため forcedDecision を消す。2. なりすましを防ぐためメタデータ（serverName、toolAnnotations、details）を消す。
- **どう使っているか**: サブエージェントから来る確認要求では toolAnnotations を消してから判定する。annotations がポリシーの入力なので、サブエージェントが「readOnlyHint:true」を偽って書き込みを通すのを防ぐ。
- **条件**: derive() で作る（サブエージェント用の）バスだけ。MCP サーバー自身の申告は検証しない（C06_google_aws-08）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、57-59 行（取得 2026-10-02T22:11:33Z、sha256 7afa83730696…）
- **補足**: 守っているのは「バス上の偽の annotations」で、「サーバーの嘘の annotations」ではない点に注意。

### Google — Gemini CLI — リリースノート

<a id="g-c06-google-aws-12"></a>
#### C06-12 Google — Gemini CLI — リリースノート

- **資料**: Gemini CLI changelog（Announcements: v0.31.0 - 2026-02-27）（リリースノート）
- **URL**: https://geminicli.com/docs/changelogs/
- **書いてある見出しへ直接**: https://geminicli.com/docs/changelogs/#announcements-v0310---2026-02-27
- **版**: v0.31.0（2026-02-27）。2026-10-02 取得
- **書いてある場所**: Gemini CLI release notes > Announcements: v0.31.0 - 2026-02-27 (#announcements-v0310---2026-02-27)
- **原文**:

> Policy Engine Updates: The policy engine now supports project-level policies, MCP server wildcards, and tool annotation matching

- **日本語**: ポリシーエンジンの更新: プロジェクト単位のポリシー、MCP サーバーのワイルドカード、ツール annotations の照合に対応した。
- **どう使っているか**: annotations をポリシー条件に使う機能が v0.31.0（2026-02-27）で入ったことの記録。
- **条件**: v0.31.0 以降。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Gemini CLI release notes > Announcements: v0.31.0 - 2026-02-27」（取得 2026-10-02T22:11:28Z、sha256 d0a1ff8b5c95…）
- **補足**: 本文中の PR 番号は #18682 と #20024（github.com はブロックのため PR 本文は未確認）。

### Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM

<a id="g-c06-google-aws-13"></a>
#### C06-13 Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM

- **資料**: Control MCP use with Identity and Access Management（IAM deny policy attributes）（公式の文書）
- **URL**: https://docs.cloud.google.com/mcp/control-mcp-use-iam
- **書いてある見出しへ直接**: https://docs.cloud.google.com/mcp/control-mcp-use-iam#deny-policy-attributes
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: Control MCP use with Identity and Access Management > IAM deny policy attributes (#deny-policy-attributes)
- **原文**:

> tool.isReadOnly: a resource attribute that indicates whether the invoked tool only reads data.

- **日本語**: tool.isReadOnly: 呼ばれたツールがデータを読むだけかどうかを示すリソース属性。
- **どう使っているか**: Google Cloud の MCP サーバーへの tools/call を IAM deny ポリシーで止める条件に、ツールが読み取り専用かどうか（tool.isReadOnly）を使える。サーバー側（Google の IAM）で強制される。
- **条件**: Google Cloud の MCP サーバー（BigQuery など Google が運営するもの）だけ。ページに「Google Cloud 以外の MCP サーバーには IAM は使えない」とある。 同じページの「IAM allow policy attributes」には tool.isReadOnly が無い（deny ポリシーでだけ使える属性）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Control MCP use with Identity and Access Management Stay organized with collections Save and categorize content based on your preferences. > IAM deny policy attributes」（取得 2026-10-02T22:11:25Z、sha256 a351ca67750d…）
- **補足**: isReadOnly が MCP の readOnlyHint から来ることは、同じページの「annotated as read-only」（C06_google_aws-14）と各ツールの参照ページの Tool Annotations 表（C06_google_aws-17）からの読み。値を誰が決めるか（Google の各サービス）は明記なし。 allow ポリシーの属性表に tool.isReadOnly が無いことを conditions に追記（deny 専用）。

<a id="g-c06-google-aws-14"></a>
#### C06-14 Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM

- **資料**: Control MCP use with Identity and Access Management（Deny read-write MCP tool use）（公式の文書）
- **URL**: https://docs.cloud.google.com/mcp/control-mcp-use-iam
- **書いてある見出しへ直接**: https://docs.cloud.google.com/mcp/control-mcp-use-iam#deny_read-write_mcp_tool_use
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: Control MCP use with Identity and Access Management > Example IAM deny policies > Deny read-write MCP tool use (#deny_read-write_mcp_tool_use)
- **原文**:

> After the policy is applied to a Google Cloud project, when an MCP client makes a tool call to a tool that isn't annotated as read-only, the request fails and an HTTP client error is returned. Note: When an MCP client calls tools/list, a list of all tools is returned, including read-write tools.

- **日本語**: このポリシーをプロジェクトに付けると、MCP クライアントが読み取り専用と注記（annotate）されていないツールを呼んだとき、要求は失敗し HTTP のクライアントエラーが返る。注: tools/list では読み書きツールも含め全ツールが返る。
- **どう使っているか**: 「読み取り専用と注記されていない」ツールの呼び出しを IAM で拒否する。注記が無いツールも拒否側（getAttribute の既定値 false）。一覧からは隠さない（呼び出し時に拒否）。
- **条件**: 管理者が IAM deny ポリシー（組織・フォルダ・プロジェクト）を付けたときだけ。Google Cloud の MCP サーバーだけ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Control MCP use with Identity and Access Management Stay organized with collections Save and categorize content based on your preferences. > Example IAM deny policies > Deny read-write MCP tool use」（取得 2026-10-02T22:11:25Z、sha256 a351ca67750d…）
- **補足**: 宣言はサーバー（Google）自身のもので、利用者が付け替えるものではない。対照: Agent Gateway では管理者が toolspec.json で付けられる（C06_google_aws-24）。

<a id="g-c06-google-aws-15"></a>
#### C06-15 Google Cloud — Google Cloud リモート（マネージド）MCP サーバー — IAM

- **資料**: Prevent read-write MCP tool use（公式の文書）
- **URL**: https://docs.cloud.google.com/mcp/prevent-read-write-tool-use
- **書いてある見出しへ直接**: https://docs.cloud.google.com/mcp/prevent-read-write-tool-use#prevent-read-write-tool-use
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: Prevent read-write MCP tool use > Prevent read-write tool use (#prevent-read-write-tool-use)
- **原文**:

> "expression" : "api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false"

- **日本語**: 条件式: api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false（isReadOnly が無ければ false とみなし、false なら拒否）
- **どう使っているか**: 読み書きツールを止める deny ポリシーの式。属性が無いときの既定値を false にしているので、読み取り専用の宣言が無いツールは書き込みツールとして止められる。
- **条件**: 同上（Google Cloud の MCP サーバー、deny ポリシー適用時）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Prevent read-write MCP tool use Stay organized with collections Save and categorize content based on your preferences. > Prevent read-write tool use」（取得 2026-10-02T22:11:25Z、sha256 4546963cf0fb…）
- **補足**: match=loose（JSON の引用符・空白の差）。同じページ冒頭: "Identity and Access Management (IAM) deny policies let you restrict Model Context Protocol (MCP) tools to read-only actions, preventing AI applications from modifying or deleting resources."（verify 済み exact）。

### Google — Google の MCP サーバー参照ドキュメント（Developer Knowledge MCP ほか共通の説明）

<a id="g-c06-google-aws-16"></a>
#### C06-16 Google — Google の MCP サーバー参照ドキュメント（Developer Knowledge MCP ほか共通の説明）

- **資料**: MCP Tools Reference: developerknowledge.googleapis.com — search_documents（Tool Annotations）（公式の文書）
- **URL**: https://developers.google.com/knowledge/reference/mcp/tools_list/search_documents
- **書いてある見出しへ直接**: https://developers.google.com/knowledge/reference/mcp/tools_list/search_documents#tool-annotations
- **版**: 2026-10-02 取得（developers.google.com。版表示なし）
- **書いてある場所**: MCP Tools Reference: developerknowledge.googleapis.com > Output Schema > Tool Annotations (#tool-annotations)
- **原文**:

> Tool annotations are sent to MCP clients to describe the basic risk of a given tool. Most clients treat these hints as untrusted, but they can be used to decide when a confirmation prompt might be sent to a user.

- **日本語**: ツールの annotations は、そのツールの基本的な危険度を説明するために MCP クライアントへ送られる。多くのクライアントはこれらのヒントを信頼できないものとして扱うが、ユーザーに確認を出すかどうかを決めるのには使える。
- **どう使っているか**: Google が自社の MCP サーバーの参照ページに載せる共通の説明。annotations は「信頼できないヒント」だが確認ダイアログの判断に使える、という立場。各ツールの頁に ✅/❌ の表で 4 つの hint を表示する。
- **条件**: Google が公開する MCP サーバーのツール参照ページ（同じ段落が docs.cloud.google.com の agentregistry の get_mcp_server ページにもある）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 信頼するなという注意・確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tools Reference: developerknowledge.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Tool Annotations」（取得 2026-10-02T22:11:25Z、sha256 b6365e5c4d89…）
- **補足**: 同じ段落で既定値も書く: readOnlyHint 既定 false、destructiveHint 既定 true、idempotentHint 既定 false。

### Google Cloud — Cloud Run リモート MCP サーバー（run.googleapis.com）

<a id="g-c06-google-aws-17"></a>
#### C06-17 Google Cloud — Cloud Run リモート MCP サーバー（run.googleapis.com）

- **資料**: MCP Tools Reference: run.googleapis.com — list_services（Tool Annotations）（公式の文書）
- **URL**: https://docs.cloud.google.com/run/docs/reference/mcp/tools_list/list_services
- **書いてある見出しへ直接**: https://docs.cloud.google.com/run/docs/reference/mcp/tools_list/list_services#tool-annotations
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: MCP Tools Reference: run.googleapis.com > Output Schema > Tool Annotations (#tool-annotations)
- **原文**:

> Destructive Hint: ❌ | Idempotent Hint: ❌ | Read Only Hint: ✅ | Open World Hint: ❌

- **日本語**: 破壊的ヒント: ✕ | 冪等ヒント: ✕ | 読み取り専用ヒント: ✓ | 外部世界ヒント: ✕
- **どう使っているか**: Google 自身のマネージド MCP サーバーが各ツールに付けた宣言を、ドキュメントの表で人に見せる。IAM の tool.isReadOnly（C06_google_aws-13）の値の元と考えられる。
- **条件**: list_services ツール。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tools Reference: run.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Tool Annotations」（取得 2026-10-02T22:11:27Z、sha256 2dd3ee7f47e1…）
- **補足**: 一覧系ツールなのに idempotentHint は ❌。readOnlyHint:true のとき idempotentHint は仕様上意味を持たない（meaningful only when readOnlyHint == false）ので矛盾ではない。

### Google Cloud — gcloud リモート MCP サーバー（cloudcli.googleapis.com）

<a id="g-c06-google-aws-18"></a>
#### C06-18 Google Cloud — gcloud リモート MCP サーバー（cloudcli.googleapis.com）

- **資料**: MCP Tools Reference: cloudcli.googleapis.com — run_gcloud_command（Tool Annotations）（公式の文書）
- **URL**: https://docs.cloud.google.com/sdk/reference/mcp/tools_list/run_gcloud_command
- **書いてある見出しへ直接**: https://docs.cloud.google.com/sdk/reference/mcp/tools_list/run_gcloud_command#tool-annotations
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: MCP Tools Reference: cloudcli.googleapis.com > Output Schema > Tool Annotations (#tool-annotations)
- **原文**:

> Destructive Hint: ✅ | Idempotent Hint: ❌ | Read Only Hint: ❌ | Open World Hint: ❌

- **日本語**: 破壊的ヒント: ✓ | 冪等ヒント: ✕ | 読み取り専用ヒント: ✕ | 外部世界ヒント: ✕
- **どう使っているか**: 任意の gcloud コマンドを実行するツール（ページの説明: "It is NOT restricted to read-only commands."）は readOnlyHint:false・destructiveHint:true と宣言（読み取りのコマンドでも書き込み側）。IAM の読み取り専用 deny ポリシー（C06_google_aws-14）が cloudcli.googleapis.com にも効くなら、このツールは丸ごと止まる（推測。cloudcli が IAM の MCP 属性の対象かはこのページにも IAM のページにも書かれていない）。
- **条件**: run_gcloud_command ツール。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tools Reference: cloudcli.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Tool Annotations」（取得 2026-10-02T22:11:25Z、sha256 54394bb828d2…）
- **補足**: 引数次第で読みにも書きにもなる汎用ツールに、最悪側の宣言を付けた例。openWorldHint は ❌（Google Cloud 内の操作とみなす）。 「IAM 下で丸ごと止まる」は推測であることを明記（対象サービスかどうかの記述なし）。ツール説明の "NOT restricted to read-only commands" を確認。

### Google Cloud — Gemini Enterprise — カスタム MCP サーバーのデータストア（actions）

<a id="g-c06-google-aws-19"></a>
#### C06-19 Google Cloud — Gemini Enterprise — カスタム MCP サーバーのデータストア（actions）

- **資料**: Set up your custom MCP server data store（Configure annotations to skip user confirmation）（公式の文書）
- **URL**: https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server
- **書いてある見出しへ直接**: https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server#configure_annotations_to_skip_user_confirmation
- **版**: 2026-10-02 取得（docs.cloud.google.com。ページ末尾の表示: Last updated 2026-09-30 UTC）
- **書いてある場所**: Set up your custom MCP server data store > Enable actions > Configure annotations to skip user confirmation (#configure_annotations_to_skip_user_confirmation)
- **原文**:

> When tools from your MCP server are imported as actions into the Gemini Enterprise data store, Gemini Enterprise checks their tool annotations to determine if user confirmation is required. By default, all calls to any action require confirmation from the user, because Gemini Enterprise assumes that any operation is potentially destructive and can mutate data.

- **日本語**: MCP サーバーのツールを Gemini Enterprise のデータストアに actions として取り込むとき、Gemini Enterprise はツールの annotations を見てユーザー確認が要るかを決める。既定ではどの action の呼び出しにも確認が要る。どんな操作も破壊的でデータを変えうるとみなすからだ。
- **どう使っているか**: Gemini Enterprise は取り込み時に annotations を読み、確認の要否を決める。宣言が無ければ全部確認（破壊的とみなす）。
- **条件**: Gemini Enterprise のカスタム MCP サーバー・データストアの actions。宣言を変えたら Reload custom actions が要る（同じ節）。 actions は既定で全部オフで、管理者が選んで有効化する（同じページ「Enable actions」、最大 100 個）。annotations は取り込み時（tools/list）に読まれる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Set up your custom MCP server data store Stay organized with collections Save and categorize content based on your preferences. > Enable actions > Configure annotations to skip user confirmation」（取得 2026-10-02T22:12:47Z、sha256 585df83d541b…）
- **補足**: version にページの最終更新日を追記。actions が既定オフで取り込み時に annotations を読む点を conditions に追記。

<a id="g-c06-google-aws-20"></a>
#### C06-20 Google Cloud — Gemini Enterprise — カスタム MCP サーバーのデータストア（actions）

- **資料**: Set up your custom MCP server data store（Configure annotations to skip user confirmation）（公式の文書）
- **URL**: https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server
- **書いてある見出しへ直接**: https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server#configure_annotations_to_skip_user_confirmation
- **版**: 2026-10-02 取得（docs.cloud.google.com。ページ末尾の表示: Last updated 2026-09-30 UTC）
- **書いてある場所**: Set up your custom MCP server data store > Enable actions > Configure annotations to skip user confirmation (#configure_annotations_to_skip_user_confirmation)
- **原文**:

> readOnlyHint: Add this annotation to your tool definition if the operation is non-destructive and only reads data. The tool execution bypasses user confirmation. destructiveHint: Explicitly use this annotation if the tool modifies data. This maintains the default confirmation behavior.

- **日本語**: readOnlyHint: 操作が破壊的でなくデータを読むだけなら、ツール定義にこの annotation を付ける。そのツールの実行はユーザー確認を飛ばす。destructiveHint: ツールがデータを変えるならこの annotation を明示する。既定の確認の動きが保たれる。
- **どう使っているか**: readOnlyHint:true を付けたツールは確認なしで実行される（自動許可）。サーバー作者への書き方の指示つき（例: @mcp.tool(annotations={"destructiveHint": False, "readOnlyHint": True})）。
- **条件**: 同上。宣言はサーバー作者の自己申告で、検証の記述は無い。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Set up your custom MCP server data store Stay organized with collections Save and categorize content based on your preferences. > Enable actions > Configure annotations to skip user confirmation」（取得 2026-10-02T22:12:47Z、sha256 585df83d541b…）
- **補足**: readOnlyHint:true と destructiveHint が両方あるときなどの優先関係は書かれていない（不明）。 version にページの最終更新日を追記。

### Google Cloud — Gemini Enterprise Agent Platform — Agent Gateway の IAM ポリシー

<a id="g-c06-google-aws-21"></a>
#### C06-21 Google Cloud — Gemini Enterprise Agent Platform — Agent Gateway の IAM ポリシー

- **資料**: IAM policies overview（Policy components）（公式の文書）
- **URL**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/iam-overview
- **書いてある見出しへ直接**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/iam-overview#policy-components
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: IAM policies overview > Policy components (#policy-components)
- **原文**:

> iap.googleapis.com/mcp.tool.isReadOnly iap.googleapis.com/mcp.tool.isDestructive iap.googleapis.com/mcp.tool.isIdempotent iap.googleapis.com/mcp.tool.isOpenWorld Boolean flags indicating the type of operation.

- **日本語**: iap.googleapis.com/mcp.tool.isReadOnly、isDestructive、isIdempotent、isOpenWorld: 操作の種類を示す真偽値のフラグ。
- **どう使っているか**: Agent Gateway（エージェントの外向き通信の関所）で、MCP ツールの 4 つの hint を IAM の条件式（CEL）の属性として使える。例: api.getAttribute('iap.googleapis.com/mcp.tool.isReadOnly', false) == true。
- **条件**: Agent Gateway を通る MCP 通信で、IAM allow / deny ポリシーを書いたとき。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「IAM policies overview Stay organized with collections Save and categorize content based on your preferences. > Policy components」（取得 2026-10-02T22:11:30Z、sha256 fa2e12391ca8…）
- **補足**: 値の出どころは Agent Registry に登録した toolspec.json（C06_google_aws-23）。

<a id="g-c06-google-aws-22"></a>
#### C06-22 Google Cloud — Gemini Enterprise Agent Platform — Agent Gateway の IAM ポリシー

- **資料**: Configure IAM agent policies（Create an IAM allow policy using IAP）（公式の文書）
- **URL**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/configure-iam-policies
- **書いてある見出しへ直接**: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/configure-iam-policies#gcloud_2
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: Configure IAM agent policies > Create an IAM allow policy using IAP > gcloud (#gcloud_2)
- **原文**:

> "expression": "api.getAttribute('iap.googleapis.com/mcp.toolName', '') == 'GitHubTool' && api.getAttribute('iap.googleapis.com/mcp.tool.isReadOnly', false) == true && api.getAttribute('iap.googleapis.com/request.auth.type', '') == 'MCP'"

- **日本語**: 条件式の例: ツール名が GitHubTool で、かつ isReadOnly が true（無ければ false）で、かつ認証の種類が MCP のときだけ許可する。
- **どう使っているか**: Agent Gateway の IAM allow ポリシーの例。条件は「ツール名が GitHubTool」かつ「isReadOnly が true」かつ「認証種別が MCP」で、ページの説明は "allows a DIY agent read-only access to a tool called GitHubTool"（条件のタイトルは "Allow AE Agent Read-Only Egress to GitHub MCP server"）。isReadOnly の既定値を false にしているので、宣言（登録簿の値）が無いツールは許可されない。
- **条件**: Agent Gateway 経由の外向き通信（egress）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Configure IAM agent policies Stay organized with collections Save and categorize content based on your preferences. > Create an IAM allow policy using IAP > gcloud」（取得 2026-10-02T22:11:26Z、sha256 0f1c418f7475…）
- **補足**: 発見者の usage_ja「GitHub MCP サーバーの読み取り専用ツールだけを許す」は不正確。式は toolName == 'GitHubTool' の 1 ツールに限ったうえで isReadOnly を要求する。ページの文言に合わせて直した。

### Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab）

<a id="g-c06-google-aws-23"></a>
#### C06-23 Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab）

- **資料**: Agent Gateway egress from Agent Runtime to external MCP（MCP protocol inspection）（公式ブログ）
- **URL**: https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp
- **書いてある見出しへ直接**: https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp#mcp-protocol-inspection
- **版**: 2026-10-02 取得（codelabs.developers.google.com。版表示なし）
- **書いてある場所**: Agent Gateway egress from Agent Runtime to external MCP > MCP protocol inspection (#mcp-protocol-inspection)
- **原文**:

> Attributes like iap.googleapis.com/mcp.tool.isReadOnly and mcp.tool.isDestructive are not usually sent in each request body. Instead, these are annotations (metadata) associated with the tool. So when Agent Gateway extracts the toolName from the body, it looks up the tool definition and associated properties from Agent Registry, where the toolspec.json content was registered.

- **日本語**: iap.googleapis.com/mcp.tool.isReadOnly や mcp.tool.isDestructive のような属性は、ふつう要求の本文には入っていない。これらはツールに付いた annotations（メタデータ）だ。Agent Gateway は本文からツール名を取り出すと、Agent Registry（toolspec.json を登録した所）からツール定義と属性を引く。
- **どう使っているか**: IAM の判定に使う hint は、呼び出しのたびにサーバーに聞くのではなく、Agent Registry に登録した宣言から引く。
- **条件**: Agent Gateway + Agent Registry に MCP サーバーを登録した場合。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent Gateway egress from Agent Runtime to external MCP > MCP protocol inspection」（取得 2026-10-02T22:11:22Z、sha256 03dbfa7128c0…）
- **補足**: codelab は Google 公式の手順書（doc_type は近いものとして official_blog を選んだ）。登録後にサーバーの実際の annotations が変わったときの扱いは書かれていない（不明）。

<a id="g-c06-google-aws-24"></a>
#### C06-24 Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab）

- **資料**: Agent Gateway egress from Agent Runtime to external MCP（Create MCP server toolspec）（公式ブログ）
- **URL**: https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp
- **書いてある見出しへ直接**: https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp#create-mcp-server-toolspec
- **版**: 2026-10-02 取得（codelabs.developers.google.com。版表示なし）
- **書いてある場所**: Agent Gateway egress from Agent Runtime to external MCP > Create MCP server toolspec (#create-mcp-server-toolspec)
- **原文**:

> The governance annotations like isReadOnly, isDestructive, isIdempotent, and isOpenWorld are optional extension metadata. Security admins can set these annotations in the toolspec.json file before registering the MCP server in Agent Registry.

- **日本語**: isReadOnly、isDestructive、isIdempotent、isOpenWorld のような統制用の annotations は任意の拡張メタデータだ。セキュリティ管理者は、MCP サーバーを Agent Registry に登録する前に toolspec.json の中でこれらを設定できる。
- **どう使っているか**: 宣言をサーバー作者ではなく管理者が付ける（または書き換える）道がある。オープンソースや他社の MCP サーバーは annotations を持たないことが多い、と同じ段落で書く。
- **条件**: Agent Registry に登録する toolspec.json。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent Gateway egress from Agent Runtime to external MCP > Create MCP server toolspec」（取得 2026-10-02T22:11:22Z、sha256 03dbfa7128c0…）
- **補足**: toolspec.json での名前は isReadOnly など（MCP の readOnlyHint とは別名）。管理者が付けた値と実装が食い違ったときの検証は書かれていない。

<a id="g-c06-google-aws-25"></a>
#### C06-25 Google — Gemini Enterprise Agent Platform — Agent Gateway（codelab）

- **資料**: Governing agentic workloads with Agent Gateway on Gemini Enterprise Agent Platform（Use case 2 - Conditional grant (CEL) scoped to a specific MCP server）（公式ブログ）
- **URL**: https://codelabs.developers.google.com/cloudnet-agent-gateway
- **書いてある見出しへ直接**: https://codelabs.developers.google.com/cloudnet-agent-gateway#use-case-2-—-conditional-grant-cel-scoped-to-a-specific-mcp-server
- **版**: 2026-10-02 取得（codelabs.developers.google.com。版表示なし）
- **書いてある場所**: Governing agentic workloads with Agent Gateway on Gemini Enterprise Agent Platform > Use case 2 - Conditional grant (CEL) scoped to a specific MCP server (#use-case-2-—-conditional-grant-cel-scoped-to-a-specific-mcp-server)
- **原文**:

> After this runs, write tools on corporate-email return 403 PermissionDenied from IAP REQUEST_AUTHZ; read-only tools continue to work.

- **日本語**: これを実行すると、corporate-email の書き込みツールは IAP REQUEST_AUTHZ から 403 PermissionDenied を返す。読み取り専用ツールはそのまま動く。
- **どう使っているか**: isReadOnly 条件つきの IAM 付与で、書き込みツールの呼び出しを関所（IAP）で 403 にする実演。
- **条件**: isReadOnly == true（または toolName が空）を条件にした IAM 付与をしたとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Governing agentic workloads with Agent Gateway on Gemini Enterprise Agent Platform > Use case 2 - Conditional grant (CEL) scoped to a specific MCP server」（取得 2026-10-02T22:11:22Z、sha256 565e5db025fc…）

### Google Cloud — Agent Registry — MCP サーバー登録（tool spec の JSON）

<a id="g-c06-google-aws-26"></a>
#### C06-26 Google Cloud — Agent Registry — MCP サーバー登録（tool spec の JSON）

- **資料**: JSON schemas（MCP tool schema > Field definitions）（公式の文書）
- **URL**: https://docs.cloud.google.com/agent-registry/json-schemas
- **書いてある見出しへ直接**: https://docs.cloud.google.com/agent-registry/json-schemas#field_definitions
- **版**: 2026-10-02 取得（docs.cloud.google.com。ページ末尾の表示: Last updated 2026-09-30 UTC）
- **書いてある場所**: JSON schemas > MCP tool schema > Field definitions (#field_definitions)
- **原文**:

> annotations: Behavioral hints that guide how orchestrator agents interact with the tool:

- **日本語**: annotations: オーケストレーター（指揮役）エージェントがそのツールとどう関わるかを導く、振る舞いのヒント:
- **どう使っているか**: Agent Registry に登録する tool spec の annotations の定義。続けて既定値を書く: readOnlyHint 既定 false、destructiveHint 既定 true、idempotentHint 既定 false、openWorldHint 既定 true。
- **条件**: Agent Registry に MCP サーバーを手で登録するとき（tools/list と同じ形の JSON、10 KB まで）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「JSON schemas Stay organized with collections Save and categorize content based on your preferences. > MCP tool schema > Field definitions」（取得 2026-10-02T22:11:26Z、sha256 6bbe25c56405…）
- **補足**: 登録された値が Agent Gateway の IAM 属性になる（C06_google_aws-23）。 version にページの最終更新日を追記。

### Google Cloud — Agent Registry — MCP サーバー登録

<a id="g-c06-google-aws-27"></a>
#### C06-27 Google Cloud — Agent Registry — MCP サーバー登録

- **資料**: Register MCP servers（Prepare your tool specification）（公式の文書）
- **URL**: https://docs.cloud.google.com/agent-registry/register-mcp-servers
- **書いてある見出しへ直接**: https://docs.cloud.google.com/agent-registry/register-mcp-servers#prepare-tool-spec
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: Register MCP servers > Register external MCP servers > Prepare your tool specification (#prepare-tool-spec)
- **原文**:

> "annotations" : { "title" : "Get Customer Info" , "readOnlyHint" : true , "idempotentHint" : true }

- **日本語**: 例: "annotations": { "title": "Get Customer Info", "readOnlyHint": true, "idempotentHint": true }
- **どう使っているか**: 登録例で、顧客情報の取得ツールに readOnlyHint:true、チケット作成ツールに destructiveHint:true・idempotentHint:false・openWorldHint:true を付ける。
- **条件**: 外部 MCP サーバーの手動登録。
- **扱う宣言**: readOnlyHint・idempotentHint・title・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Register MCP servers Stay organized with collections Save and categorize content based on your preferences. > Register external MCP servers > Prepare your tool specification」（取得 2026-10-02T22:11:25Z、sha256 41632927487e…）
- **補足**: match=loose（JSON の空白・引用符の差）。例のチケット作成（追加だけの操作）に destructiveHint:true を付けており、仕様の「destructive = 既存を壊す更新」より広い使い方。

### Google Cloud — Agent Registry MCP サーバー（agentregistry.googleapis.com）

<a id="g-c06-google-aws-28"></a>
#### C06-28 Google Cloud — Agent Registry MCP サーバー（agentregistry.googleapis.com）

- **資料**: MCP Tools Reference: agentregistry.googleapis.com — get_mcp_server（Output Schema > Annotations）（公式の文書）
- **URL**: https://docs.cloud.google.com/agent-registry/reference/mcp/tools_list/get_mcp_server
- **書いてある見出しへ直接**: https://docs.cloud.google.com/agent-registry/reference/mcp/tools_list/get_mcp_server#annotations
- **版**: 2026-10-02 取得（docs.cloud.google.com。版表示なし）
- **書いてある場所**: MCP Tools Reference: agentregistry.googleapis.com > Output Schema > Annotations (#annotations)
- **原文**:

> destructiveHint boolean Output only. If true, the tool may perform destructive updates to its environment. If false, the tool performs only additive updates. NOTE: This property is meaningful only when read_only_hint == false Default: true

- **日本語**: destructiveHint（真偽値、出力専用）: true ならツールは環境を破壊的に更新しうる。false なら追加の更新だけ。注: readOnlyHint == false のときだけ意味がある。既定: true
- **どう使っているか**: Agent Registry は登録された MCP サーバーの各ツールの annotations を保持し、API の出力でそのまま返す（他のエージェントが登録簿から読める）。
- **条件**: Agent Registry に登録済みのサーバー。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tools Reference: agentregistry.googleapis.com Stay organized with collections Save and categorize content based on your preferences. > Output Schema > Annotations」（取得 2026-10-02T22:11:26Z、sha256 19c1c9c986f3…）
- **補足**: このページ自体も Google のマネージド MCP サーバーのツール参照で、末尾の表は Read Only Hint ✅。

### Google Cloud — Cloud API Registry — McpTool 型（クライアントライブラリ参照）

<a id="g-c06-google-aws-29"></a>
#### C06-29 Google Cloud — Cloud API Registry — McpTool 型（クライアントライブラリ参照）

- **資料**: Google Cloud Api Registry V1 Client - Class McpTool (0.2.3)（SDK の文書）
- **URL**: https://docs.cloud.google.com/php/docs/reference/cloud-apiregistry/latest/V1.McpTool
- **書いてある見出しへ直接**: https://docs.cloud.google.com/php/docs/reference/cloud-apiregistry/latest/V1.McpTool#_Google_Cloud_ApiRegistry_V1_McpTool____construct__
- **版**: google-cloud-apiregistry（PHP）0.2.3 の参照。2026-10-02 取得
- **書いてある場所**: Google Cloud Api Registry V1 Client - Class McpTool (0.2.3) > Methods > __construct (#_Google_Cloud_ApiRegistry_V1_McpTool____construct__)
- **原文**:

> Annotations or tags to facilitate semantic search across tools ("semantic tags") are not in the MVP scope. When implemented, the first set of supported annotations will likely be the standard, predefined annotations from the open-source MCP spec.

- **日本語**: ツール横断の意味検索を助ける annotations やタグ（「semantic tags」）は MVP の範囲外。実装するときは、最初に対応する annotations はおそらくオープンソースの MCP 仕様の標準のものになる。
- **どう使っているか**: Cloud API Registry の McpTool には、開発者が任意に入れる key-value の annotations 欄がある。説明文は「ツール横断の意味検索のための annotations / tags（"semantic tags"）は MVP の範囲外」とし、実装されたときに最初に対応する annotations は「おそらく」MCP 標準のもの（title・readOnlyHint・destructiveHint・idempotentHint・openWorldHint）だと書く。annotations を確認・許可などの判断に使うという記述は無い。
- **条件**: API Registry の McpTool リソース。
- **扱う宣言**: 宣言全般・readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・3 か所、見出し「Google Cloud Api Registry V1 Client - Class McpTool (0.2.3) Stay organized with collections Save and categorize content based on your preferences. > Methods > __construct」（取得 2026-10-02T22:11:27Z、sha256 9eeca750055b…）
- **補足**: count=3（同じ文がページ内に 3 回）。Agent Registry（C06_google_aws-26）とは別製品。 発見者の「annotations の使い道はまだ MVP の範囲外」は言い過ぎ。範囲外とされているのは「意味検索のための annotations / tags」で、標準の 5 つへの対応は「likely」（予定の推測）。usage_ja と quote_ja を原文に合わせて直した。

### Google — MCP Toolbox for Databases（googleapis/genai-toolbox）

<a id="g-c06-google-aws-30"></a>
#### C06-30 Google — MCP Toolbox for Databases（googleapis/genai-toolbox）

- **資料**: Tools（Tool Annotations）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/documentation/configuration/tools/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/documentation/configuration/tools/#tool-annotations
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: Tools > Tool Annotations (#tool-annotations)
- **原文**:

> Tool annotations provide semantic metadata that helps MCP clients understand tool behavior. These hints enable clients to make better decisions about tool usage and provide appropriate user experiences.

- **日本語**: ツールの annotations は、MCP クライアントがツールの振る舞いを理解するための意味のメタデータを与える。これらのヒントで、クライアントはツールの使い方についてより良い判断をし、適切な利用体験を出せる。
- **どう使っているか**: Google の DB 用 MCP サーバーが、YAML のツール設定で annotations を書けるようにし、その目的をクライアントの判断材料と説明する。
- **条件**: tools.yaml のツール定義。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Tool Annotations」（取得 2026-10-02T22:11:28Z、sha256 e0c8798affa6…）
- **補足**: 同じ節の表: readOnlyHint 既定 false、destructiveHint 既定 true、idempotentHint 既定 false、openWorldHint 既定 true。

### Google — MCP Toolbox for Databases

<a id="g-c06-google-aws-31"></a>
#### C06-31 Google — MCP Toolbox for Databases

- **資料**: Tools（Tool Annotations > Default Annotations）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/documentation/configuration/tools/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/documentation/configuration/tools/#default-annotations
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: Tools > Tool Annotations > Default Annotations (#default-annotations)
- **原文**:

> Write operations (insert, update, delete): destructiveHint: true, readOnlyHint: false

- **日本語**: 書き込み操作（insert、update、delete）: destructiveHint: true、readOnlyHint: false
- **どう使っているか**: 設定で annotations を書かないとき、Toolbox は操作の種類から既定の宣言を付ける。読み取り（find、aggregate、list）は readOnlyHint: true（verify 済み: "Read operations (find, aggregate, list): readOnlyHint: true"）、書き込みは destructiveHint: true・readOnlyHint: false。
- **条件**: ツールの種類（type）ごとの既定。直前の文: "If not specified, tools use sensible defaults based on their operation type:"（verify 済み）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Tool Annotations > Default Annotations」（取得 2026-10-02T22:11:28Z、sha256 e0c8798affa6…）
- **補足**: 既定はツールの種類（例 mongodb-find-one）で決まり、実際の SQL 文などは見ない。コード側の部品は internal/tools/tools.go の NewReadOnlyAnnotations / NewDestructiveAnnotations / NewWriteAnnotations。

<a id="g-c06-google-aws-35"></a>
#### C06-35 Google — MCP Toolbox for Databases

- **資料**: internal/tools/tools.go（ShouldSuppress）（サーバのソースコード）
- **URL**: https://github.com/googleapis/genai-toolbox/blob/912189f6c842fdf8fc6ceb7d7a556cf9fa05286b/internal/tools/tools.go#L304-L306
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleapis/genai-toolbox/912189f6c842fdf8fc6ceb7d7a556cf9fa05286b/internal/tools/tools.go
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: lines 304-306
- **原文**:

```
// By default, if the source is read-only and the tool's ReadOnlyHint is explicitly false,
// the tool is suppressed. Unannotated tools (ReadOnlyHint == nil) or read-only tools
// (ReadOnlyHint == true) are not suppressed.
```

- **日本語**: 既定では、ソースが読み取り専用で、ツールの ReadOnlyHint が明示的に false なら、そのツールを隠す。注記の無いツール（ReadOnlyHint == nil）や読み取り専用ツール（ReadOnlyHint == true）は隠さない。
- **どう使っているか**: サーバー側で readOnlyHint を見てツールを登録から外す。宣言が無い（nil）ツールは「隠さない」側に倒す（MCP の既定 false とは逆向きの扱い。代わりに警告 C06_google_aws-36 を出す）。
- **条件**: データソースが IsReadOnly() のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、304-306 行（取得 2026-10-02T22:12:57Z、sha256 f6b98b4d80a1…）
- **補足**: 宣言無し = 公開のまま、なので、宣言の無い書き込みツールは読み取り専用モードでも見える。実際の書き込みは DB 側のロック（Pillar 1）で止まる、という設計。

<a id="g-c06-google-aws-36"></a>
#### C06-36 Google — MCP Toolbox for Databases

- **資料**: internal/tools/tools.go（ShouldSuppress の警告文）（サーバのソースコード）
- **URL**: https://github.com/googleapis/genai-toolbox/blob/912189f6c842fdf8fc6ceb7d7a556cf9fa05286b/internal/tools/tools.go#L327
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleapis/genai-toolbox/912189f6c842fdf8fc6ceb7d7a556cf9fa05286b/internal/tools/tools.go
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: lines 327
- **原文**:

> Tool %q lacks ReadOnlyHint annotation; executing this tool may fail if it attempts write operations. If this tool is meant to be read-only, please add 'readOnlyHint: true' to its annotations. Otherwise, add 'readOnlyHint: false' to suppress it in read-only mode and save agent context window.

- **日本語**: ツール %q には ReadOnlyHint の注記が無い。書き込みをしようとすると、このツールの実行は失敗しうる。読み取り専用のつもりなら annotations に 'readOnlyHint: true' を足して。そうでないなら 'readOnlyHint: false' を足せば、読み取り専用モードで隠されてエージェントの文脈を節約できる。
- **どう使っているか**: 起動時、読み取り専用ソースに付いたツールに readOnlyHint が無いと警告を出し、作者に宣言を足すよう促す（宣言漏れの点検）。
- **条件**: データソースが読み取り専用のときだけ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、327 行（取得 2026-10-02T22:12:57Z、sha256 f6b98b4d80a1…）

### Google — MCP Toolbox for Databases — 読み取り専用モード

<a id="g-c06-google-aws-32"></a>
#### C06-32 Google — MCP Toolbox for Databases — 読み取り専用モード

- **資料**: Read-Only Tools（Pillar 3: Dynamic MCP Manifest Annotations）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/#pillar-3-dynamic-mcp-manifest-annotations
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: Read-Only Tools > The Three Pillars of Read-Only Defense > Pillar 3: Dynamic MCP Manifest Annotations (#pillar-3-dynamic-mcp-manifest-annotations)
- **原文**:

> This signal informs MCP clients (e.g., Claude Desktop, Cursor, or custom agent orchestrators) that invoking the tool produces zero side effects, allowing clients to safely auto-execute read queries without requiring manual human confirmation dialogs.

- **日本語**: この信号は、MCP クライアント（例: Claude Desktop、Cursor、自作のオーケストレーター）に、そのツールを呼んでも副作用がゼロだと伝える。それでクライアントは、人の手動確認ダイアログなしに読み取りの問い合わせを安全に自動実行できる。
- **どう使っているか**: サーバー側が、readOnlyHint:true を出す目的を「クライアントの自動実行（確認なし）」と明言。読み取り専用モードでは露出する DB ツールすべてが readOnlyHint:true を出す。
- **条件**: ソースに readOnly: true（または prebuilt で *_READONLY=true）を設定したとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Read-Only Tools > The Three Pillars of Read-Only Defense > Pillar 3: Dynamic MCP Manifest Annotations」（取得 2026-10-02T22:12:53Z、sha256 d9ba80eb903a…）
- **補足**: Toolbox は宣言の裏付けとして DB エンジン側のロック（Pillar 1）を置く。同じページで「Client Hints」だけでは足りないとも書く（C06_google_aws-34）。クライアント名の挙動はサーバー側の主張で、各クライアントの一次資料ではない。 検証者補足: ページは「読み取り専用モードでは露出するツールすべてが readOnlyHint: true を出す」と書くが、コードの ShouldSuppress（C06_google_aws-35/36）は readOnlyHint が無い（nil）ツールを隠さず警告だけ出す。宣言の無いツールにモード中 true を補うかは未確認（不明）なので、「すべて」がコードでも成り立つとは言えない。 文書の「all exposed database tools advertise readOnlyHint: true」とコード（宣言なしツールは残る）の食い違いを notes に追記。

<a id="g-c06-google-aws-33"></a>
#### C06-33 Google — MCP Toolbox for Databases — 読み取り専用モード

- **資料**: Read-Only Tools（Pillar 2: Tool Suppression）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/#pillar-2-tool-suppression
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: Read-Only Tools > The Three Pillars of Read-Only Defense > Pillar 2: Tool Suppression (#pillar-2-tool-suppression)
- **原文**:

> When read-only mode is active, MCP Toolbox automatically prunes write tools from the registered tools catalog and tool groups. The agent never sees tools it is not permitted to execute.

- **日本語**: 読み取り専用モードが有効なとき、MCP Toolbox は登録されたツール一覧とツールグループから書き込みツールを自動で取り除く。エージェントは実行を許されないツールを見ない。
- **どう使っているか**: サーバー自身が readOnlyHint を見て、読み取り専用モードでは書き込みツールを公開しない（判定は C06_google_aws-35 のコード）。
- **条件**: データソースが読み取り専用のとき（readOnly: true、prebuilt は *_READONLY=true）。同じページの対応表に載るエンジンは Cloud SQL (PostgreSQL)・AlloyDB (PostgreSQL)・Cloud SQL (MySQL)・BigQuery の 4 つ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Read-Only Tools > The Three Pillars of Read-Only Defense > Pillar 2: Tool Suppression」（取得 2026-10-02T22:12:53Z、sha256 d9ba80eb903a…）
- **補足**: 対応エンジン（ページの表の 4 つ）を conditions に追記。

<a id="g-c06-google-aws-34"></a>
#### C06-34 Google — MCP Toolbox for Databases — 読み取り専用モード

- **資料**: Read-Only Tools（Overview）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/documentation/configuration/security/read-only/#overview
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: Read-Only Tools > Overview (#overview)
- **原文**:

> Security is enforced at the lowest level (the database engine itself), while performance and token efficiency are optimized at the highest level (the MCP protocol manifest).

- **日本語**: 安全性はいちばん下の層（データベースのエンジンそのもの）で強制し、性能とトークンの節約はいちばん上の層（MCP のツール一覧＝manifest）で最適化する。
- **どう使っているか**: Toolbox は読み取り専用の安全性を DB エンジン側（Pillar 1）で強制し、MCP の annotations（manifest の readOnlyHint, Pillar 3）は性能・トークン節約の層だと位置づける。宣言を安全境界にしない、というサーバー側の立場。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Read-Only Tools > Overview」（取得 2026-10-02T22:12:53Z、sha256 d9ba80eb903a…）
- **補足**: 引用を差し替えた（発見者の引用: "Prompt Guardrails & Client Hints: Prompting an agent "Please only run SELECT queries; never execute DELETE" treats a probabilistic language model as a deterministic security boundary." は同じページの「Why "Soft Locks" Fail in Production」節で exact 一致するが、本文はプロンプトの話だけで、"Client Hints" は小見出しの語にしか出ない。MCP annotations のことかも不明）。新しい引用は同じページの Overview。なお Pillar 3 の節では readOnlyHint:true でクライアントが確認なしに自動実行できると書く（C06_google_aws-32）ので、「安全は DB、annotations は効率と UX」という分担。 引用を Overview の文に差し替え（元の引用は「Client Hints」が見出しの語だけで、annotations を安全境界にしないという主張の根拠として弱い）。location・anchored_url・quote_ja・usage_ja・notes を更新。 doc_title と hints も差し替え後の節に合わせた。

### Google — MCP Toolbox for Databases — BigQuery

<a id="g-c06-google-aws-37"></a>
#### C06-37 Google — MCP Toolbox for Databases — BigQuery

- **資料**: bigquery-sql（Read-Only Mode）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/integrations/bigquery/tools/bigquery-sql/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/integrations/bigquery/tools/bigquery-sql/#about
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: bigquery-sql > About (#about)
- **原文**:

> bigquery-sql tools default to write-capable annotations (readOnlyHint: false) and are automatically suppressed from registration during server startup to protect data integrity and optimize agent context window. To keep a pre-defined read-only query active in read-only mode, explicitly annotate the tool with readOnlyHint: true.

- **日本語**: bigquery-sql ツールは既定で書き込み可能の annotations（readOnlyHint: false）になり、サーバー起動時に登録から自動で外される。データを守り、エージェントの文脈を節約するためだ。読み取り専用モードで事前定義の読み取りクエリを使い続けたいなら、そのツールに readOnlyHint: true を明示する。
- **どう使っているか**: SQL を事前に書くツールは中身に関係なく既定 readOnlyHint:false。読み取り専用モードでは隠れるので、作者が readOnlyHint:true を明示して残す。宣言が公開の有無を決める。
- **条件**: BigQuery ソースが readOnly: true（または writeMode: blocked / protected）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「bigquery-sql > About」（取得 2026-10-02T22:11:30Z、sha256 798ce6b3e26f…）
- **補足**: 検証者が修正: bigquery-sql のページ自体には dryRun や「SELECT 以外を拒否」の記述は無い（"dryRun" "SELECT statements" で照合して none）。read-only ページ（Pillar 1）は BigQuery では dryRun で SELECT 以外を拒否すると書く一方、BigQuery source のページは protected モードについて "For tools like bigquery-sql, bigquery-forecast, and bigquery-analyze-contribution, the writeMode restrictions do not apply" と書く。作者が SELECT でない文に readOnlyHint:true を付けたときに止まるかは、文書間で一致した記述が無い（不明）。 発見者の notes「dryRun で止まる、というのがページの主張」は出典の取り違え（このページには無い）。source ページの例外（protected モードでは bigquery-sql に writeMode の制限が掛からない）を添えて不明とした。

### Google — MCP Toolbox for Databases — BigQuery ソース

<a id="g-c06-google-aws-38"></a>
#### C06-38 Google — MCP Toolbox for Databases — BigQuery ソース

- **資料**: BigQuery source（writeMode）（サーバの文書）
- **URL**: https://mcp-toolbox.dev/integrations/bigquery/source/
- **書いてある見出しへ直接**: https://mcp-toolbox.dev/integrations/bigquery/source/#reference
- **版**: googleapis/genai-toolbox @ 912189f6c842fdf8fc6ceb7d7a556cf9fa05286b（docs は 2026-10-02 に mcp-toolbox.dev から取得）
- **書いてある場所**: BigQuery Source > Reference (#reference)
- **原文**:

> blocked: Enforces strict read-only mode, coordinating with MCP read-only annotations and tool suppression (suppresses write-capable tools during registration, while dynamic tools like bigquery-execute-sql dynamically report readOnlyHint: true), and allows only SELECT statements for execution.

- **日本語**: blocked: 厳格な読み取り専用モードにする。MCP の読み取り専用 annotations とツールの隠しを連動させ（書き込みできるツールは登録時に外し、bigquery-execute-sql のような動的ツールは動的に readOnlyHint: true を報告する）、SELECT 文だけ実行を許す。
- **どう使っているか**: 同じツール（任意 SQL を実行する bigquery-execute-sql）でも、設定 writeMode によって readOnlyHint の宣言が変わる。宣言が実装の固定的な性質ではなく、設定で切り替わる例。
- **条件**: writeMode: blocked（readOnly: true の既定）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「BigQuery Source > Reference」（取得 2026-10-02T22:11:30Z、sha256 42866dd3168f…）
- **補足**: bigquery-execute-sql のページの表では、readOnly:false・writeMode:allowed のとき annotations は「Default / none」。 検証者補足（bigquery-execute-sql のページで照合、readOnlyHint で exact count=2）: 表は readOnly:true・writeMode:protected のときも "readOnlyHint: true" とし、同じ行で「書き込みはセッションの一時データセットにだけ許す（CREATE TEMP TABLE など）」と書く。宣言（readOnlyHint:true）のまま一時領域への書き込みがありうる例。 execute-sql の表（Default / none）を照合して確認。protected モードでも readOnlyHint:true のまま一時データセットに書けることを notes に追記。

### Google — Agent Development Kit（ADK, Python）— ADK ツールを MCP ツールに変換

<a id="g-c06-google-aws-39"></a>
#### C06-39 Google — Agent Development Kit（ADK, Python）— ADK ツールを MCP ツールに変換

- **資料**: src/google/adk/tools/mcp_tool/conversion_utils.py（adk_to_mcp_tool_type）（SDK のソースコード）
- **URL**: https://github.com/google/adk-python/blob/539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8/src/google/adk/tools/mcp_tool/conversion_utils.py#L56-L60
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google/adk-python/539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8/src/google/adk/tools/mcp_tool/conversion_utils.py
- **版**: google/adk-python @ 539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8
- **書いてある場所**: lines 56-60
- **原文**:

```
  return mcp_types.Tool(
      name=tool.name,
      description=tool.description,
      inputSchema=input_schema,
  )
```

- **日本語**: mcp_types.Tool を name、description、inputSchema だけで作って返す。
- **どう使っているか**: ADK のツールを MCP サーバーとして公開するための変換関数は name・description・inputSchema だけを写し、annotations を付けない。これで作ったサーバーのツールは全部「宣言なし」になる（仕様上の既定値は readOnlyHint=false・destructiveHint=true・openWorldHint=true。実際にどう扱うかはクライアント次第で、例えば Toolbox の隠し判定は宣言なしを隠さない側に倒す）。
- **条件**: adk_to_mcp_tool_type を使って MCP サーバーを作る場合（例: Google Analytics MCP、C06_google_aws-40）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、56-60 行（# limitations under the License.）（取得 2026-10-02T22:11:31Z、sha256 1fbdd4ea2053…）
- **補足**: ADK の MCP クライアント側（McpTool / McpToolset）も annotations を読まない（checked_no_mention に記録）。確認の要否は require_confirmation の設定で決める（C06_google_aws-41）。 「クライアントは既定値で扱う」は一般化しすぎなので、仕様の既定値とクライアントごとの差に言い換えた。

### Google — Google Analytics MCP サーバー（googleanalytics/google-analytics-mcp）

<a id="g-c06-google-aws-40"></a>
#### C06-40 Google — Google Analytics MCP サーバー（googleanalytics/google-analytics-mcp）

- **資料**: analytics_mcp/coordinator.py（サーバのソースコード）
- **URL**: https://github.com/googleanalytics/google-analytics-mcp/blob/a8ca729d4a8fa99bffe87962c17c0539c6aa9da7/analytics_mcp/coordinator.py#L92
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/googleanalytics/google-analytics-mcp/a8ca729d4a8fa99bffe87962c17c0539c6aa9da7/analytics_mcp/coordinator.py
- **版**: googleanalytics/google-analytics-mcp @ a8ca729d4a8fa99bffe87962c17c0539c6aa9da7
- **書いてある場所**: lines 92
- **原文**:

> mcp_tools = [adk_to_mcp_tool_type(tool) for tool in tools]

- **日本語**: mcp_tools = ツール一覧の各ツールを adk_to_mcp_tool_type で変換したもの
- **どう使っているか**: Google 公式の Analytics MCP サーバーは、すべて読み取り系（get_* / list_* / run_*_report）なのに、ADK の変換関数（C06_google_aws-39）で作るため annotations が付かない。Gemini Enterprise や Gemini CLI Plan Mode のように annotations で確認や可否を決めるクライアントでは、読み取りでも書き込み扱いになる。
- **条件**: pinned commit 時点。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、92 行（# Instantiate the ADK tools）（取得 2026-10-02T22:11:37Z、sha256 ef85c52177b9…）
- **補足**: 読み取り専用の annotations を足す PR #209 があると WebSearch で見た（C06_google_aws-66, 未確認）が、この commit の main には入っていない（grep で readOnlyHint / ToolAnnotations なし）。ツールが読み取り系だというのは関数名からの読み。

### Google — Agent Development Kit（ADK, Python）— MCP クライアント（McpTool）

<a id="g-c06-google-aws-41"></a>
#### C06-41 Google — Agent Development Kit（ADK, Python）— MCP クライアント（McpTool）

- **資料**: src/google/adk/tools/mcp_tool/mcp_tool.py（McpTool.__init__ の docstring）（SDK のソースコード）
- **URL**: https://github.com/google/adk-python/blob/539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8/src/google/adk/tools/mcp_tool/mcp_tool.py#L316-L319
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google/adk-python/539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8/src/google/adk/tools/mcp_tool/mcp_tool.py
- **版**: google/adk-python @ 539a0d071c4fe6b8bd3ae9bda3a53e14ea80aeb8
- **書いてある場所**: lines 316-319
- **原文**:

```
        require_confirmation: Whether this tool requires confirmation. A boolean
          or a callable that takes the function's arguments and returns a
          boolean. If the callable returns True, the tool will require
          confirmation from the user.
```

- **日本語**: require_confirmation: このツールに確認が要るか。真偽値か、関数の引数を受けて真偽値を返す関数。関数が True を返せば、そのツールはユーザーの確認を求める。
- **どう使っているか**: ADK で MCP ツールに確認を付けるのは、開発者が McpToolset / McpTool に渡す require_confirmation（既定 False）で、サーバーの annotations ではない。McpTool はサーバーのツール定義から name・description・inputSchema・outputSchema・_meta だけを読む（grep）。
- **条件**: ADK Python の McpToolset 経由で MCP ツールを使うとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、316-319 行（# name -- so the walk below must not descend into them.）（取得 2026-10-02T22:11:34Z、sha256 d6020347afc4…）
- **補足**: ADK Java の AbstractMcpTool は annotations() の getter を持つが、src/main 以下で呼ぶ箇所は grep で見つからなかった（google/adk-java @ c8b1de6a）。

### Google — Agent Development Kit（ADK, Go）— Agent Registry クライアント

<a id="g-c06-google-aws-42"></a>
#### C06-42 Google — Agent Development Kit（ADK, Go）— Agent Registry クライアント

- **資料**: agentregistry/types.go（Annotations 型）（SDK のソースコード）
- **URL**: https://github.com/google/adk-go/blob/b531451670a2c544610f8d614d2e13b56cf6cad5/agentregistry/types.go#L87-L89
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google/adk-go/b531451670a2c544610f8d614d2e13b56cf6cad5/agentregistry/types.go
- **版**: google/adk-go @ b531451670a2c544610f8d614d2e13b56cf6cad5
- **書いてある場所**: lines 87-89
- **原文**:

> // Annotations are behavioral hints for a [Tool]. Absent hints carry API-side
> // defaults (DestructiveHint and OpenWorldHint default to true), so a zero-value
> // false here can mean "unset" rather than an explicit false.

- **日本語**: Annotations はツールの振る舞いのヒント。無いヒントは API 側の既定値を持つ（DestructiveHint と OpenWorldHint の既定は true）。だから、ここでのゼロ値の false は、明示の false ではなく「未設定」の意味でありうる。
- **どう使っているか**: Agent Registry から読んだ annotations を bool（omitempty）で持つため、「未設定」と「明示 false」を区別できないとコメントで認めている。destructiveHint の未設定（既定 true）が false に化けうる。
- **条件**: ADK Go の agentregistry パッケージで登録簿のツール情報を読むとき。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint・title ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、87-89 行（取得 2026-10-02T22:12:02Z、sha256 199f803b3c0f…）
- **補足**: このフィールドを判断に使う箇所は grep では見つからなかった。

### Google（adk.dev に掲載。対象は ClickHouse のサーバー） — ADK ドキュメント — ClickHouse Cloud MCP 連携ページ

<a id="g-c06-google-aws-43"></a>
#### C06-43 Google（adk.dev に掲載。対象は ClickHouse のサーバー） — ADK ドキュメント — ClickHouse Cloud MCP 連携ページ

- **資料**: ClickHouse Cloud MCP tool for ADK（Safety）（公式の文書）
- **URL**: https://adk.dev/integrations/clickhouse/
- **書いてある見出しへ直接**: https://adk.dev/integrations/clickhouse/#safety
- **版**: 2026-10-02 取得（adk.dev。版表示なし）
- **書いてある場所**: ClickHouse Cloud MCP tool for ADK > Safety (#safety)
- **原文**:

> All tools exposed by the remote MCP server are read-only. Each tool is annotated with readOnlyHint: true in its MCP metadata. No tool can modify data, alter service configuration, or perform any destructive operation.

- **日本語**: リモート MCP サーバーが出すツールはすべて読み取り専用だ。各ツールは MCP のメタデータで readOnlyHint: true と注記されている。データの変更、サービス設定の変更、破壊的な操作ができるツールは無い。
- **どう使っているか**: ADK 公式サイトの連携ページで、他社サーバーの安全性を readOnlyHint:true の宣言で説明する。宣言が安全性の説明（読者への約束）に使われている例。
- **条件**: ClickHouse のリモート MCP サーバー。ローカル版は既定で読み取り専用、書き込みは CLICKHOUSE_ALLOW_WRITE_ACCESS=true が要る（同じ節）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「ClickHouse Cloud MCP tool for ADK¶ > Safety¶」（取得 2026-10-02T22:11:20Z、sha256 554feeb7eb99…）
- **補足**: adk.dev は google.github.io/adk-docs からの転送先。ページに執筆者の表示は無く、記述が ClickHouse 社によるものかは不明（発見者は「記述の主体 ClickHouse」としていたが根拠が無い）。Google が宣言を検証したとは書かれていない。同じ節: "The run_select_query tool only permits SELECT statements." org の「ClickHouse（記述の主体）」はページから裏づけられないので外し、執筆者は不明とした。

### Google（Firebase） — Firebase MCP サーバー（firebase-tools の src/mcp）

<a id="g-c06-google-aws-44"></a>
#### C06-44 Google（Firebase） — Firebase MCP サーバー（firebase-tools の src/mcp）

- **資料**: src/mcp/tool.ts（ServerTool の annotations 型）（サーバのソースコード）
- **URL**: https://github.com/firebase/firebase-tools/blob/04a8b861422918a44341340c224d710a7b350147/src/mcp/tool.ts#L32-L39
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/firebase/firebase-tools/04a8b861422918a44341340c224d710a7b350147/src/mcp/tool.ts
- **版**: firebase/firebase-tools @ 04a8b861422918a44341340c224d710a7b350147
- **書いてある場所**: lines 32-39
- **原文**:

```
      // If this tool modifies data or not.
      readOnlyHint?: boolean;

      // this tool can destroy data.
      destructiveHint?: boolean;

      // this tool is safe to run multiple times.
      idempotentHint?: boolean;
```

- **日本語**: （readOnlyHint）このツールがデータを変えるかどうか。（destructiveHint）このツールはデータを壊しうる。（idempotentHint）このツールは何度実行しても安全。
- **どう使っているか**: Firebase の公式 MCP サーバーは各ツールに annotations を書く作法をコード内コメントで定める（openWorldHint は「インターネットなど外へつながるなら true、プロジェクト内だけなら false」）。
- **条件**: サーバー側の宣言。消費側の処理は src/mcp 内に無い（index.ts で tools/list にそのまま載せるだけ）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、32-39 行（取得 2026-10-02T22:12:57Z、sha256 86f38ef8584f…）
- **補足**: 件数（自分で数えた、手続きつき）: src/mcp/tools 以下の .ts（*.spec.ts と index.ts を除く）40 ファイルのうち、readOnlyHint を含むファイルは 33。ファイル単位でありツール単位ではない。idempotentHint のコメント「safe to run multiple times」は仕様の「同じ引数で繰り返しても追加の効果なし」より緩い。

### AWS（Strands Agents） — Strands Agents SDK（Python）

<a id="g-c06-google-aws-45"></a>
#### C06-45 AWS（Strands Agents） — Strands Agents SDK（Python）

- **資料**: strands-py/src/strands/types/tools.py（ToolSpec.annotations の説明）（SDK のソースコード）
- **URL**: https://github.com/strands-agents/sdk-python/blob/583196634a3e7a73fb58cdd764de6028c167beeb/strands-py/src/strands/types/tools.py#L43-L45
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/strands-agents/sdk-python/583196634a3e7a73fb58cdd764de6028c167beeb/strands-py/src/strands/types/tools.py
- **版**: strands-agents/sdk-python @ 583196634a3e7a73fb58cdd764de6028c167beeb（monorepo: strands-py / strands-ts）
- **書いてある場所**: lines 43-45
- **原文**:

```
            Annotations are untrusted hints from the tool provider, not
            guarantees; consumers such as permission layers must not treat them
            as a security boundary. A missing key means unknown, not False:
```

- **日本語**: annotations はツール提供者からの信頼できないヒントで、保証ではない。権限の層などの利用者は、これを安全境界として扱ってはならない。キーが無いのは「不明」であって False ではない。
- **どう使っているか**: Strands は MCP ツールの annotations を ToolSpec に載せるが、安全境界に使うなと型の説明で明言。続けて仕様の既定値（destructiveHint・openWorldHint は無ければ true、readOnlyHint・idempotentHint は無ければ false）を書く。
- **条件**: MCP 由来のツールだけ（MCP 以外のツールにはこのフィールドが無い）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint ／ **使い方の分類**: 信頼するなという注意・宣言が無いときの扱い・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、43-45 行（取得 2026-10-02T22:11:40Z、sha256 bd4454869694…）
- **補足**: 同じ説明の最後に「This field is not sent to model provider APIs.」とある。SDK 内で annotations を判断に使う箇所は grep で見つからなかった（harness-py / harness-ts も同様）。

### AWS（Strands Agents） — Strands Agents SDK（Python）— MCP ツール

<a id="g-c06-google-aws-46"></a>
#### C06-46 AWS（Strands Agents） — Strands Agents SDK（Python）— MCP ツール

- **資料**: strands-py/src/strands/tools/mcp/mcp_agent_tool.py（tool_spec）（SDK のソースコード）
- **URL**: https://github.com/strands-agents/sdk-python/blob/583196634a3e7a73fb58cdd764de6028c167beeb/strands-py/src/strands/tools/mcp/mcp_agent_tool.py#L89-L90
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/strands-agents/sdk-python/583196634a3e7a73fb58cdd764de6028c167beeb/strands-py/src/strands/tools/mcp/mcp_agent_tool.py
- **版**: strands-agents/sdk-python @ 583196634a3e7a73fb58cdd764de6028c167beeb（monorepo: strands-py / strands-ts）
- **書いてある場所**: lines 89-90
- **原文**:

```
        # Pass annotations through opaquely: per MCP spec they are untrusted hints,
        # and the annotation vocabulary is still evolving (SEP-1984, SEP-1913).
```

- **日本語**: annotations は中身を解釈せずにそのまま通す。MCP 仕様ではこれは信頼できないヒントで、annotation の語彙もまだ変わっている途中だから（SEP-1984、SEP-1913）。
- **どう使っているか**: MCP サーバーの annotations を camelCase のまま ToolSpec に写すだけで、Strands 自身は使わない。空の annotations は無いのと同じ扱い。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、89-90 行（取得 2026-10-02T22:11:37Z、sha256 1dab5b616f00…）

### AWS（Strands Agents） — Strands Agents SDK（TypeScript）

<a id="g-c06-google-aws-47"></a>
#### C06-47 AWS（Strands Agents） — Strands Agents SDK（TypeScript）

- **資料**: strands-ts/src/tools/types.ts（ToolSpec.annotations）（SDK のソースコード）
- **URL**: https://github.com/strands-agents/sdk-python/blob/583196634a3e7a73fb58cdd764de6028c167beeb/strands-ts/src/tools/types.ts#L37-L39
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/strands-agents/sdk-python/583196634a3e7a73fb58cdd764de6028c167beeb/strands-ts/src/tools/types.ts
- **版**: strands-agents/sdk-python @ 583196634a3e7a73fb58cdd764de6028c167beeb（monorepo: strands-py / strands-ts）
- **書いてある場所**: lines 37-39
- **原文**:

```
   * Untrusted tool-behavior hints (e.g. MCP `readOnlyHint`, `destructiveHint`); never a security boundary.
   *
   * Not sent to model provider APIs.
```

- **日本語**: 信頼できないツールの振る舞いのヒント（例: MCP の readOnlyHint、destructiveHint）。決して安全境界ではない。モデル提供者の API には送らない。
- **どう使っているか**: TypeScript 版も同じ立場。mcp/client.ts は MCP SDK が認めるキー（title と 4 つの hint）だけを通す（未知のキーは SDK が先に捨てる、とコメント）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 信頼するなという注意・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、37-39 行（取得 2026-10-02T22:13:01Z、sha256 80f3333ed2e7…）

### AWS — MCP Proxy for AWS（mcp-proxy-for-aws）— --read-only

<a id="g-c06-google-aws-48"></a>
#### C06-48 AWS — MCP Proxy for AWS（mcp-proxy-for-aws）— --read-only

- **資料**: mcp_proxy_for_aws/middleware/tool_filter.py（on_list_tools）（ゲートウェイのソースコード）
- **URL**: https://github.com/aws/mcp-proxy-for-aws/blob/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/middleware/tool_filter.py#L50-L53
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aws/mcp-proxy-for-aws/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/middleware/tool_filter.py
- **版**: aws/mcp-proxy-for-aws @ 43569c7e99fabeaa3786d7fa106691a40ee59faa（CHANGELOG 最新 v1.7.0, 2026-09-15）
- **書いてある場所**: lines 50-53
- **原文**:

```
            # Skip the tools with no readOnlyHint=True annotation
            read_only_hint = getattr(annotations, 'readOnlyHint', False)
            if not read_only_hint:
                # Skip tools that don't have readOnlyHint=True
```

- **日本語**: readOnlyHint=True の注記が無いツールは飛ばす。annotations の readOnlyHint（無ければ False）が真でなければ、そのツールは一覧に入れない。
- **どう使っているか**: AWS 公式のローカルプロキシ（SigV4 で AWS の MCP サーバーにつなぐ）で --read-only を付けると、上流サーバーの readOnlyHint が True のツールだけをクライアントに見せる。宣言が無いツールは隠す。
- **条件**: --read-only を付けたときだけ（既定 False）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、50-53 行（# limitations under the License.）（取得 2026-10-02T22:11:59Z、sha256 899dd24d3648…）
- **補足**: 判定は上流サーバーの自己申告そのまま。EKS / ECS などの AWS マネージド MCP サーバーの手順で使う（C06_google_aws-51）。

### AWS — MCP Proxy for AWS — --read-only

<a id="g-c06-google-aws-49"></a>
#### C06-49 AWS — MCP Proxy for AWS — --read-only

- **資料**: mcp_proxy_for_aws/middleware/tool_filter.py（on_call_tool）（ゲートウェイのソースコード）
- **URL**: https://github.com/aws/mcp-proxy-for-aws/blob/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/middleware/tool_filter.py#L84-L87
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aws/mcp-proxy-for-aws/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/middleware/tool_filter.py
- **版**: aws/mcp-proxy-for-aws @ 43569c7e99fabeaa3786d7fa106691a40ee59faa（CHANGELOG 最新 v1.7.0, 2026-09-15）
- **書いてある場所**: lines 84-87
- **原文**:

```
            if not getattr(tool.annotations, 'readOnlyHint', False):
                raise ToolError(
                    f'Tool {context.message.name!r} is not available in read-only mode.'
                )
```

- **日本語**: ツールの annotations の readOnlyHint が真でなければ、「読み取り専用モードではこのツールは使えない」というエラーにする。
- **どう使っているか**: 一覧から隠すだけでなく、tools/call の時点でも readOnlyHint を確かめて拒否する。上流でツールが引けないときは「読み取り専用の確認ができない」エラーにして通さない（同じ関数）。
- **条件**: --read-only のときだけ。しかも on_call_tool の検査は `if context.fastmcp_context:` の中にあり、FastMCP の context が無い呼び出しでは検査せずに通す（同じ関数、70 行目。どの経路で context が無くなるかは不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、84-87 行（# limitations under the License.）（取得 2026-10-02T22:11:59Z、sha256 899dd24d3648…）
- **補足**: この呼び出し時の強制は v1.6.4 で入った（C06_google_aws-50）。それより前は一覧から隠すだけで、名前を知っていれば呼べたと読める（CHANGELOG からの読み）。 呼び出し時の拒否が fastmcp_context の有無に条件づけられていることを conditions に追記。

### AWS — MCP Proxy for AWS — リリースノート

<a id="g-c06-google-aws-50"></a>
#### C06-50 AWS — MCP Proxy for AWS — リリースノート

- **資料**: CHANGELOG.md（v1.6.4 (2026-07-20) > Fixed）（リリースノート）
- **URL**: https://github.com/aws/mcp-proxy-for-aws/blob/43569c7e99fabeaa3786d7fa106691a40ee59faa/CHANGELOG.md#L45
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aws/mcp-proxy-for-aws/43569c7e99fabeaa3786d7fa106691a40ee59faa/CHANGELOG.md
- **版**: aws/mcp-proxy-for-aws @ 43569c7e99fabeaa3786d7fa106691a40ee59faa（CHANGELOG 最新 v1.7.0, 2026-09-15）
- **書いてある場所**: lines 45（直前の見出し: ### Fixed）
- **原文**:

> - enforce read-only mode on tools/call requests (#350)

- **日本語**: tools/call の要求にも読み取り専用モードを強制する（#350）
- **どう使っているか**: --read-only が一覧のフィルタだけだった不具合を、呼び出し時の拒否で塞いだ修正の記録。
- **条件**: v1.6.4 以降。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、45 行（### Fixed）（取得 2026-10-02T22:11:40Z、sha256 8a3df368a0c6…）
- **補足**: 行 45 は見出し「## v1.6.4 (2026-07-20)」（38 行）の下の Fixed 節。PR #350 の本文は github.com ブロックのため未確認。

### AWS — Amazon EKS マネージド MCP サーバー（プロキシ経由の設定）

<a id="g-c06-google-aws-51"></a>
#### C06-51 AWS — Amazon EKS マネージド MCP サーバー（プロキシ経由の設定）

- **資料**: Amazon EKS MCP Server Configuration Reference（Arguments: --read-only）（公式の文書）
- **URL**: https://docs.aws.amazon.com/eks/latest/userguide/eks-mcp-tool-configurations.html
- **書いてある見出しへ直接**: https://docs.aws.amazon.com/eks/latest/userguide/eks-mcp-tool-configurations.html#_arguments
- **版**: 2026-10-02 取得（docs.aws.amazon.com/eks。版表示なし）
- **書いてある場所**: Amazon EKS MCP Server Configuration Reference > Arguments (#_arguments)
- **原文**:

> Disable tools which may require write permissions (tools which DO NOT require write permissions are annotated with readOnlyHint=true). By default, all tools are enabled.

- **日本語**: 書き込み権限が要るかもしれないツールを無効にする（書き込み権限が要らないツールには readOnlyHint=true が付いている）。既定ではすべてのツールが有効。
- **どう使っているか**: AWS の公式ドキュメントが、--read-only の意味を「readOnlyHint=true でないツールを無効にする」と説明。宣言がツールの公開範囲を決める。
- **条件**: mcp-proxy-for-aws に --read-only を付けたとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Amazon EKS MCP Server Configuration Reference > Arguments」（取得 2026-10-02T22:11:25Z、sha256 322a71102617…）
- **補足**: EKS 側は別に IAM で分ける: "eks-mcp:CallReadOnlyTool is required for usage of read-only tools and eks-mcp:CallPrivilegedTool is required for usage of full access (write) tools."（同じページ、verify 済み exact）。IAM の読み取り／書き込みの分類が readOnlyHint と同じ基準かは書かれていない（不明）。

### AWS — MCP Proxy for AWS — CLI ヘルプ

<a id="g-c06-google-aws-52"></a>
#### C06-52 AWS — MCP Proxy for AWS — CLI ヘルプ

- **資料**: mcp_proxy_for_aws/cli.py（--read-only の help）（ゲートウェイのソースコード）
- **URL**: https://github.com/aws/mcp-proxy-for-aws/blob/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/cli.py#L135
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aws/mcp-proxy-for-aws/43569c7e99fabeaa3786d7fa106691a40ee59faa/mcp_proxy_for_aws/cli.py
- **版**: aws/mcp-proxy-for-aws @ 43569c7e99fabeaa3786d7fa106691a40ee59faa（CHANGELOG 最新 v1.7.0, 2026-09-15）
- **書いてある場所**: lines 135
- **原文**:

> help='Disable tools which may require write permissions (readOnlyHint True or unknown)',

- **日本語**: 書き込み権限が要るかもしれないツールを無効にする（readOnlyHint が True、または不明）
- **どう使っているか**: ヘルプ文。括弧の中の言い方があいまいだが、実装（C06_google_aws-48）は「readOnlyHint が True でない（False または不明）ツールを無効にする」。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、135 行（# limitations under the License.）（取得 2026-10-02T22:11:33Z、sha256 20a51787319a…）
- **補足**: ヘルプの括弧書きは字面だと「True か不明のツールを無効にする」とも読め、実装と逆に見える。誤解を招く表記と判断（本調査の読み）。

### AWS — MCP Proxy for AWS — 一般提供の告知

<a id="g-c06-google-aws-53"></a>
#### C06-53 AWS — MCP Proxy for AWS — 一般提供の告知

- **資料**: The Model Context Protocol (MCP) Proxy for AWS is now generally available（What's New）（公式ブログ）
- **URL**: https://aws.amazon.com/about-aws/whats-new/2025/10/model-context-protocol-proxy-available/
- **版**: 2025-10（What's New の URL の年月）。2026-10-02 取得
- **書いてある場所**: The Model Context Protocol (MCP) Proxy for AWS is now generally available
- **原文**:

> The MCP Proxy for AWS includes safety controls such as read-only mode to prevent unintended changes, configurable retry logic for reliability, and logging for troubleshooting.

- **日本語**: MCP Proxy for AWS には、意図しない変更を防ぐ読み取り専用モード、信頼性のための再試行設定、障害対応のためのログなどの安全策がある。
- **どう使っているか**: AWS の公式告知で、読み取り専用モード（実装は readOnlyHint による絞り込み、C06_google_aws-48）を安全策として紹介。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「The Model Context Protocol (MCP) Proxy for AWS is now generally available」（取得 2026-10-02T22:11:21Z、sha256 fe00470a112e…）
- **補足**: 告知文には readOnlyHint の語は無い。仕組みの対応はコードと README からの読み。 検証者補足: 告知は 2025-10、参照しているコードは 2026-09 の pin（v1.7.0 の時点）。告知の時点で read-only mode が readOnlyHint で判定していたかは確認していない（不明）。 告知の日付とコードの pin の時期のずれを notes に追記。

### AWS（awslabs） — AWS API MCP Server（awslabs/mcp の aws-api-mcp-server）

<a id="g-c06-google-aws-54"></a>
#### C06-54 AWS（awslabs） — AWS API MCP Server（awslabs/mcp の aws-api-mcp-server）

- **資料**: awslabs/aws_api_mcp_server/server.py（call_aws の annotations）（サーバのソースコード）
- **URL**: https://github.com/awslabs/mcp/blob/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-api-mcp-server/awslabs/aws_api_mcp_server/server.py#L242-L247
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/awslabs/mcp/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-api-mcp-server/awslabs/aws_api_mcp_server/server.py
- **版**: awslabs/mcp @ 6864d7bd21286bf2982b3386ec08eb53da9281e8
- **書いてある場所**: lines 242-247
- **原文**:

```
    annotations=ToolAnnotations(
        title='Execute AWS CLI commands',
        readOnlyHint=READ_OPERATIONS_ONLY_MODE,
        destructiveHint=not READ_OPERATIONS_ONLY_MODE,
        openWorldHint=True,
    ),
```

- **日本語**: annotations: title='Execute AWS CLI commands'、readOnlyHint=（環境変数 READ_OPERATIONS_ONLY のモード）、destructiveHint=（そのモードの否定）、openWorldHint=True
- **どう使っているか**: 任意の AWS CLI を実行する 1 つのツールの宣言を、起動時の設定 READ_OPERATIONS_ONLY（既定 "false"）で切り替える。true なら readOnlyHint:true・destructiveHint:false になり、readOnlyHint を見るクライアントやゲートウェイ（例: Gemini Enterprise の確認省略、mcp-proxy-for-aws の --read-only）からは読み取りツールに見える（どの製品と組むかで効き方は変わる）。
- **条件**: READ_OPERATIONS_ONLY=true のとき readOnlyHint:true。既定は readOnlyHint:false・destructiveHint:true。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・title ／ **使い方の分類**: その他・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、242-247 行（# limitations under the License.）（取得 2026-10-02T22:11:32Z、sha256 e12ef7f18300…）
- **補足**: サーバーは READ_OPERATIONS_ONLY のとき、IAM の Service Authorization Reference で Access level が Write でない操作だけを通す（README）。ただし「読み取り」は API の分類で、ファイルへの書き込みはありうる（C06_google_aws-55）。CHANGELOG の「## [0.2.0] - 2025-07-29」の Changed に「Tool annotations (#915)」（grep で確認、引用は未照合）。 検証者補足: README の環境変数の表は "Only operations where the **Access level** column is not `Write` will be allowed" と書く（Service Authorization Reference の Access level には Write のほか Permissions management・Tagging もある）。字面どおりなら権限変更やタグ付けも READ_OPERATIONS_ONLY で通りうるが、同じ README の別の箇所は「known read-only actions のリストと照合する」と書く。実装でどちらか（宣言 readOnlyHint:true と実効のずれがあるか）は未確認（不明）。 「クライアントの自動許可やプロキシの --read-only を通る」を、どの製品と組むかによると言い換え。README の Access level の書き方による宣言と実効のずれの可能性を不明として追記。

### AWS（awslabs） — AWS API MCP Server — README

<a id="g-c06-google-aws-55"></a>
#### C06-55 AWS（awslabs） — AWS API MCP Server — README

- **資料**: src/aws-api-mcp-server/README.md（Security Considerations）（サーバの文書）
- **URL**: https://github.com/awslabs/mcp/blob/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-api-mcp-server/README.md#L273
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/awslabs/mcp/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-api-mcp-server/README.md
- **版**: awslabs/mcp @ 6864d7bd21286bf2982b3386ec08eb53da9281e8
- **書いてある場所**: lines 273（直前の見出し: ### 🔑 Credential Management and Access Control）
- **原文**:

> "Read-Only" only refers to the API classification, not the file system, that is such "read-only" actions can still write to the file system if necessary or upon user request.

- **日本語**: 「読み取り専用」は API の分類のことで、ファイルシステムのことではない。つまり「読み取り専用」の操作でも、必要なときやユーザーが求めたときにはファイルシステムへ書き込みうる。
- **どう使っているか**: READ_OPERATIONS_ONLY のとき call_aws は readOnlyHint:true を宣言する（C06_google_aws-54）が、README はそのモードでもローカルのファイル書き込みがありうると書く。宣言（環境を変えない）と実効（ファイルを書く）がずれうることを作者自身が書いた例。
- **条件**: READ_OPERATIONS_ONLY=true のとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、273 行（### 🔑 Credential Management and Access Control）（取得 2026-10-02T22:11:29Z、sha256 5a1a7d4a1d90…）
- **補足**: 同じ段落で「IAM の権限が主で最も信頼できる統制」とも書く。

### AWS（awslabs） — CloudWatch Application Signals MCP Server（dynamic instrumentation ツール群）

<a id="g-c06-google-aws-56"></a>
#### C06-56 AWS（awslabs） — CloudWatch Application Signals MCP Server（dynamic instrumentation ツール群）

- **資料**: dynamic_instrumentation/registration.py（register_tools の docstring）（サーバのソースコード）
- **URL**: https://github.com/awslabs/mcp/blob/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/cloudwatch-applicationsignals-mcp-server/awslabs/cloudwatch_applicationsignals_mcp_server/dynamic_instrumentation/registration.py#L35-L37
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/awslabs/mcp/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/cloudwatch-applicationsignals-mcp-server/awslabs/cloudwatch_applicationsignals_mcp_server/dynamic_instrumentation/registration.py
- **版**: awslabs/mcp @ 6864d7bd21286bf2982b3386ec08eb53da9281e8
- **書いてある場所**: lines 35-37
- **原文**:

```
    Tools carry MCP annotations so clients can distinguish read-only queries
    from state-changing operations (and warn before destructive bulk deletes).
    Every tool sets ``openWorldHint=True`` because each one calls the AWS API.
```

- **日本語**: ツールには MCP の annotations を付ける。クライアントが読み取りの問い合わせと状態を変える操作を見分けられるように（そして破壊的な一括削除の前に警告できるように）。どのツールも AWS API を呼ぶので openWorldHint=True にする。
- **どう使っているか**: サーバー作者が annotations を付ける目的（クライアントでの区別と警告）を書いた例。AWS API を呼ぶものは openWorldHint=True という基準。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、35-37 行（# limitations under the License.）（取得 2026-10-02T22:12:56Z、sha256 24fe9cdebf01…）
- **補足**: 対照: redshift-mcp-server も AWS を読むだけのツールに open_world_hint=True（C06_google_aws-58）。

### AWS（awslabs） — AWS Transform MCP Server

<a id="g-c06-google-aws-57"></a>
#### C06-57 AWS（awslabs） — AWS Transform MCP Server

- **資料**: awslabs/aws_transform_mcp_server/tool_utils.py（annotations の定型）（サーバのソースコード）
- **URL**: https://github.com/awslabs/mcp/blob/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-transform-mcp-server/awslabs/aws_transform_mcp_server/tool_utils.py#L26-L30
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/awslabs/mcp/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/aws-transform-mcp-server/awslabs/aws_transform_mcp_server/tool_utils.py
- **版**: awslabs/mcp @ 6864d7bd21286bf2982b3386ec08eb53da9281e8
- **書いてある場所**: lines 26-30
- **原文**:

```
READ_ONLY: Dict[str, bool] = {
    'readOnlyHint': True,
    'destructiveHint': False,
    'idempotentHint': True,
}
```

- **日本語**: READ_ONLY の定型: readOnlyHint=True、destructiveHint=False、idempotentHint=True
- **どう使っているか**: 操作の種類ごとに annotations の定型（READ_ONLY / CREATE / MUTATE / DELETE / DELETE_IDEMPOTENT / SUBMIT / SUBMIT_IDEMPOTENT）を用意し、ツール登録で使い回す。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、26-30 行（# ── MCP tool annotations ─────────────────────────────────────────────────）（取得 2026-10-02T22:11:35Z、sha256 ff137b76a18c…）
- **補足**: CREATE は readOnlyHint=False・destructiveHint=False・idempotentHint=True、SUBMIT は destructiveHint=True（同じファイル）。openWorldHint はどの定型にも無い（仕様の既定 true のまま）。 定型の一覧に SUBMIT_IDEMPOTENT（同じファイル 62-66 行）が抜けていたので足した。

### AWS（awslabs） — Amazon Redshift MCP Server

<a id="g-c06-google-aws-58"></a>
#### C06-58 AWS（awslabs） — Amazon Redshift MCP Server

- **資料**: awslabs/redshift_mcp_server/server.py（_read_only_annotations）（サーバのソースコード）
- **URL**: https://github.com/awslabs/mcp/blob/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/redshift-mcp-server/awslabs/redshift_mcp_server/server.py#L141-L149
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/awslabs/mcp/6864d7bd21286bf2982b3386ec08eb53da9281e8/src/redshift-mcp-server/awslabs/redshift_mcp_server/server.py
- **版**: awslabs/mcp @ 6864d7bd21286bf2982b3386ec08eb53da9281e8
- **書いてある場所**: lines 141-149
- **原文**:

```
def _read_only_annotations(title: str) -> ToolAnnotations:
    """Return annotations for tools that only read the caller's AWS environment."""
    return ToolAnnotations(
        title=title,
        read_only_hint=True,
        destructive_hint=False,
        idempotent_hint=True,
        open_world_hint=True,
    )
```

- **日本語**: 呼び出し元の AWS 環境を読むだけのツールの annotations を返す: title、read_only_hint=True、destructive_hint=False、idempotent_hint=True、open_world_hint=True
- **どう使っているか**: 読み取りツール用の annotations を 1 つの関数にまとめる作法。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、141-149 行（### Connection Guidelines）（取得 2026-10-02T22:11:31Z、sha256 cd39064eaf71…）
- **補足**: 件数（自分で数えた、手続きつき）: awslabs/mcp の src/*-mcp-server（61 個）のうち、tests/ を除く .py に MCP の ToolAnnotations / readOnlyHint 等を書くのは 6 個（aws-api, aws-appsync, aws-pricing, aws-transform, cloudwatch-applicationsignals, redshift）。grep の語は readOnlyHint|destructiveHint|idempotentHint|openWorldHint|read_only_hint|destructive_hint|ToolAnnotations|annotations=、ecs の annotations=None と eks の Kubernetes の annotations は手で除いた。多くのサーバーは --allow-write や --readonly のような起動フラグで書き込みを制御する。 検証者の再確認: GitHub のコード検索（default branch、tests を除く .py）で ToolAnnotations / readOnlyHint / read_only_hint を含むファイルのサーバーは、aws-appsync・aws-api・aws-pricing・redshift・cloudwatch-applicationsignals・aws-transform の 6 つで、発見者の数と一致（pin ではなく検索時点の default branch、分母 61 は再計算していない）。 宣言を書くサーバー 6 個をコード検索で再確認（分子のみ）。

### AWS — Amazon Bedrock AgentCore Gateway

<a id="g-c06-google-aws-59"></a>
#### C06-59 AWS — Amazon Bedrock AgentCore Gateway

- **資料**: Extending MCP support for Amazon Bedrock AgentCore Gateway（AWS Machine Learning Blog）（公式ブログ）
- **URL**: https://aws.amazon.com/blogs/machine-learning/extending-mcp-support-for-amazon-bedrock-agentcore-gateway-2/
- **版**: 2026-06-01 公開（ページの datetime）。2026-10-02 取得
- **書いてある場所**: Extending MCP support for Amazon Bedrock AgentCore Gateway > Surface your MCP server primitives through a single gateway
- **原文**:

> Tool definitions in MCP include an optional outputSchema for defining expected output structure and annotations describing behavioral properties such as whether a tool is read-only or destructive, alongside the standard name, icons, description, and inputSchema.

- **日本語**: MCP のツール定義には、出力の形を決める任意の outputSchema と、ツールが読み取り専用か破壊的かなどの振る舞いを示す annotations がある。標準の name、icons、description、inputSchema と並ぶ。
- **どう使っているか**: AgentCore Gateway が対応する MCP のツール定義に annotations が含まれる、という説明。Gateway が annotations を使って何かを決める（許可・拒否）という記述は無い。
- **条件**: どのターゲット種別（MCP サーバー / Lambda / OpenAPI など）で annotations が通るかは書かれていない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Extending MCP support for Amazon Bedrock AgentCore Gateway > Surface your MCP server primitives through a single gateway」（取得 2026-10-02T22:11:21Z、sha256 41b5a124acb9…）
- **補足**: AgentCore の API リファレンス ToolDefinition（Lambda などの静的ツール定義）のフィールドは description / inputSchema / name / outputSchema だけで annotations が無い（checked_no_mention）。AgentCore の Gateway・Policy（Cedar）・Registry のドキュメントにも annotations の語は無かった（checked_no_mention）。 検証者補足: 同じ節で、既定の listing mode では tools/list を MCP サーバーに聞かずキャッシュから返し、キャッシュは CreateGatewayTarget / UpdateGatewayTarget / SynchronizeGatewayTargets のときだけ更新すると書く。上流の annotations が変わってもキャッシュ更新までは古い値が出ると読める（推測）。 tools/list のキャッシュの記述（annotations の鮮度に関わる）を notes に追記。

### AWS — Amazon Q Developer CLI — MCP のセキュリティ

<a id="g-c06-google-aws-60"></a>
#### C06-60 AWS — Amazon Q Developer CLI — MCP のセキュリティ

- **資料**: MCP security（Security considerations）（公式の文書）
- **URL**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-security.html
- **書いてある見出しへ直接**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-security.html#command-line-mcp-security-considerations
- **版**: 2026-10-02 取得（docs.aws.amazon.com/amazonq。版表示なし）
- **書いてある場所**: MCP security > Security considerations (#command-line-mcp-security-considerations)
- **原文**:

> Review tool descriptions and annotations before approving

- **日本語**: 承認する前に、ツールの説明と annotations を確認する
- **どう使っているか**: 利用者向けの注意として「承認前に annotations を見よ」と書く。ただし Q CLI（オープンソース版）のコードは annotations を保持しない（C06_google_aws-62）。
- **条件**: Amazon Q Developer CLI。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP security > Security considerations」（取得 2026-10-02T22:11:30Z、sha256 c7c6a1f43979…）
- **補足**: Q Developer CLI は Kiro CLI（クローズドソース）に移行済み（リポジトリの README）。Kiro のドキュメントにも annotations の語は無い（checked_no_mention）。

### AWS — Amazon Q Developer — MCP の説明

<a id="g-c06-google-aws-61"></a>
#### C06-61 AWS — Amazon Q Developer — MCP の説明

- **資料**: Using MCP with Amazon Q Developer（Core MCP concepts > Tools）（公式の文書）
- **URL**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/qdev-mcp.html
- **書いてある見出しへ直接**: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/qdev-mcp.html#command-line-mcp-concepts-tools
- **版**: 2026-10-02 取得（docs.aws.amazon.com/amazonq。版表示なし）
- **書いてある場所**: Using MCP with Amazon Q Developer > Core MCP concepts > Tools (#command-line-mcp-concepts-tools)
- **原文**:

> optional annotations about the tool's behavior

- **日本語**: ツールの振る舞いについての任意の annotations
- **どう使っているか**: MCP のツールが annotations を持てるという概念説明だけ。Q Developer がそれをどう使うかは書かれていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Using MCP with Amazon Q Developer > Core MCP concepts > Tools」（取得 2026-10-02T22:12:46Z、sha256 a90d8f1f393a…）
- **補足**: IDE 版の許可は per-tool の Ask / Always allow / Deny（mcp-ide ページ、verify 済み exact）で、annotations に触れない。

### AWS — Amazon Q Developer CLI（オープンソース版）

<a id="g-c06-google-aws-62"></a>
#### C06-62 AWS — Amazon Q Developer CLI（オープンソース版）

- **資料**: crates/chat-cli/src/cli/chat/tools/mod.rs（ToolSpec 構造体）（クライアントのソースコード）
- **URL**: https://github.com/aws/amazon-q-developer-cli/blob/15cc8f3cd18c4272925ce1c7053268eedff1ea0a/crates/chat-cli/src/cli/chat/tools/mod.rs#L257-L264
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aws/amazon-q-developer-cli/15cc8f3cd18c4272925ce1c7053268eedff1ea0a/crates/chat-cli/src/cli/chat/tools/mod.rs
- **版**: aws/amazon-q-developer-cli @ 15cc8f3cd18c4272925ce1c7053268eedff1ea0a（README: 保守終了、Kiro CLI へ移行）
- **書いてある場所**: lines 257-264
- **原文**:

```
pub struct ToolSpec {
    pub name: String,
    pub description: String,
    #[serde(alias = "inputSchema")]
    pub input_schema: InputSchema,
    #[serde(skip_serializing, default = "tool_origin")]
    pub tool_origin: ToolOrigin,
}
```

- **日本語**: ToolSpec 構造体のフィールドは name、description、input_schema（inputSchema の別名）、tool_origin だけ。
- **どう使っているか**: tools/list の結果はいったん rmcp（Rust の MCP SDK）の Tool 型で受け取るが、内部の ToolSpec（name・description・input_schema・tool_origin だけ）に写すときに annotations を写さない（crates/chat-cli/src/cli/chat/tool_manager.rs 1482-1490 行、pin を curl で目視・verify_quote.py では未照合）。以後の許可は allowedTools / trust の名前ベースで、annotations は使われない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、257-264 行（取得 2026-10-02T22:11:32Z、sha256 cfb47977f54a…）
- **補足**: crates/ 以下の .rs で readOnlyHint / read_only_hint / ToolAnnotations / .annotations を grep して 0 件（annotation の語は chat-cli-ui の別概念 1 件だけ）。ドキュメント（C06_google_aws-60）の「annotations を見よ」と実装が噛み合わない。 検証者補足: 受け取りは crates/chat-cli/src/mcp_client/client.rs の paginated_fetch!（content_type: rmcp::model::Tool, service_method: list_tools）。ToolSpec の doc コメントは「model に送るツール定義（BedrockToolSpecification に対応）」。 発見者の「読み込む型に annotations の欄が無く、デシリアライズ時に捨てられる」は不正確。rmcp の Tool で受け取った後、ToolSpec へ写す段階で落ちる。usage_ja を直した。

### AWS — AWS Prescriptive Guidance — MCP strategies

<a id="g-c06-google-aws-63"></a>
#### C06-63 AWS — AWS Prescriptive Guidance — MCP strategies

- **資料**: Tool definitions（Tool specification approach）（規約・審査の指針）
- **URL**: https://docs.aws.amazon.com/prescriptive-guidance/latest/mcp-strategies/mcp-tool-strategy-definitions.html
- **書いてある見出しへ直接**: https://docs.aws.amazon.com/prescriptive-guidance/latest/mcp-strategies/mcp-tool-strategy-definitions.html#mcp-tool-strategy-definitions-spec-approach
- **版**: 2026-10-02 取得（docs.aws.amazon.com/prescriptive-guidance。版表示なし）
- **書いてある場所**: Tool definitions > Tool specification approach (#mcp-tool-strategy-definitions-spec-approach)
- **原文**:

> Every tool should define these fields at a minimum and optionally provide a title and annotations, which are optional hints about tool behavior.

- **日本語**: どのツールも最低限これらのフィールド（name、description、inputSchema、outputSchema）を定義し、任意で title と annotations（ツールの振る舞いについての任意のヒント）を付けるべきだ。
- **どう使っているか**: AWS の設計指針は annotations を「任意のヒント」とだけ書き、何に使われるか・どう決めるかは書かない。（発見者の「読み書きの分離はツールや MCP サーバーを分けることで勧める（別の節）」は検証者は照合していない。）
- **扱う宣言**: 宣言全般・title ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool definitions > Tool specification approach」（取得 2026-10-02T22:11:24Z、sha256 0d18dd2ec03b…）
- **補足**: PDF 版（mcp-strategies.pdf）の 19 ページ相当。 別の節の主張は未照合と明記。

### Google — Google Security Operations MCP（google/mcp-security の secops-mcp）

<a id="g-c06-google-aws-65"></a>
#### C06-65 Google — Google Security Operations MCP（google/mcp-security の secops-mcp）

- **資料**: [secops-mcp] Add FastMCP tool annotations (readOnlyHint, destructiveHint) for safety hints and execution confirmations · Issue #320 · google/mcp-security（issue / PR / 提案の下書き）
- **URL**: https://github.com/google/mcp-security/issues/320
- **版**: 不明（2026-10-02 の WebSearch 結果）
- **書いてある場所**: 不明（本文未取得）
- **原文**:

> [secops-mcp] Add FastMCP tool annotations (readOnlyHint, destructiveHint) for safety hints and execution confirmations

- **日本語**: [secops-mcp] 安全のヒントと実行確認のために FastMCP のツール annotations（readOnlyHint、destructiveHint）を足す
- **どう使っているか**: Google の公式セキュリティ MCP サーバーに annotations が無いことへの改善要望。WebSearch の要約では「Gemini CLI、ADK、Claude、Cursor などが安全判断に annotations を使う」と主張。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を求める・作者への書き方の案内
- **確かさ**: [未確認] 未実施: github.com の HTML はこの環境でブロック（2026-10-02 も 403）。quote は WebSearch 結果のタイトル。
- **補足**: WebSearch の結果タイトルだけ。pinned commit 9885ec68 の server/ 以下に readOnlyHint / ToolAnnotations / annotations= は grep で 0 件（checked_no_mention）。issue の状態は未確認。

### Google — Google Analytics MCP サーバー

<a id="g-c06-google-aws-66"></a>
#### C06-66 Google — Google Analytics MCP サーバー

- **資料**: feat: add read-only MCP tool annotations by conorbronsdon · Pull Request #209 · googleanalytics/google-analytics-mcp（issue / PR / 提案の下書き）
- **URL**: https://github.com/googleanalytics/google-analytics-mcp/pull/209
- **版**: 不明（2026-10-02 の WebSearch 結果）
- **書いてある場所**: 不明（本文未取得）
- **原文**:

> feat: add read-only MCP tool annotations

- **日本語**: 機能: 読み取り専用の MCP ツール annotations を足す
- **どう使っているか**: Analytics MCP（全ツール読み取り系）に読み取り専用の annotations を足す外部 PR。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [未確認] 未実施: github.com の HTML はこの環境でブロック（2026-10-02 も 403）。quote は WebSearch 結果のタイトル。
- **補足**: WebSearch の結果タイトルだけ。pinned commit a8ca729d の main には入っていない（C06_google_aws-40）。マージ状態は未確認。

### AWS（awslabs） — mcp-lambda-handler（awslabs/mcp）

<a id="g-c06-google-aws-67"></a>
#### C06-67 AWS（awslabs） — mcp-lambda-handler（awslabs/mcp）

- **資料**: mcp-lambda-handler: Add support for MCP tool annotations · Issue #671 · awslabs/mcp（issue / PR / 提案の下書き）
- **URL**: https://github.com/awslabs/mcp/issues/671
- **版**: 不明（2026-10-02 の WebSearch 結果）
- **書いてある場所**: 不明（本文未取得）
- **原文**:

> mcp-lambda-handler: Add support for MCP tool annotations

- **日本語**: mcp-lambda-handler: MCP ツールの annotations に対応してほしい
- **どう使っているか**: Lambda で MCP サーバーを動かす AWS の部品が annotations を出せない、という要望。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [未確認] 未実施: github.com の HTML はこの環境でブロック（2026-10-02 も 403）。quote は WebSearch 結果のタイトル。
- **補足**: WebSearch の結果タイトルだけ。pinned commit 6864d7bd の mcp_lambda_handler.py に annotation の語は 0 件（checked_no_mention、verify_quote.py で none）。状態は未確認。

---

[← 付録 G-5 OpenAI](appendix-g-5.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-7 エディタとコーディングエージェント →](appendix-g-7.md)
