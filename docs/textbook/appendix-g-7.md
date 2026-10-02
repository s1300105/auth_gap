[← 付録 G-6 Google と AWS](appendix-g-6.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-8 エージェントの枠組み・利用者向けアプリ・モデルの API →](appendix-g-8.md)

---

# 付録 G-7 エディタとコーディングエージェント

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-7-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C07-01](#g-c07-ide-agents-01) | AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionInspector | クライアントのソースコード | 確認を省く（自動で許可）・規則（ポリシー）の条件に使う | [確認] |
| [C07-02](#g-c07-ide-agents-02) | AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — SmartApprove の判定順 | クライアントのソースコード | 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [C07-03](#g-c07-ide-agents-03) | AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionManager | クライアントのソースコード | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [C07-04](#g-c07-ide-agents-04) | n8n — n8n（Instance AI の MCP ツール権限） | クライアントのソースコード | 規則（ポリシー）の条件に使う・宣言が無いときの扱い・危険度を付ける | [確認] |
| [C07-05](#g-c07-ide-agents-05) | n8n — n8n（Instance AI の MCP ツール権限） — 既定値 | クライアントのソースコード | 確認を省く（自動で許可）・確認を求める | [確認] |
| [C07-06](#g-c07-ide-agents-06) | Docker — Docker Agent（docker/cagent） — safety ラベル | クライアントのソースコード | 危険度を付ける・規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C07-07](#g-c07-ide-agents-07) | Docker — Docker Agent（docker/cagent） — (モード × ラベル) 承認表 | クライアントのソースコード | 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [C07-08](#g-c07-ide-agents-08) | Docker — Docker Agent（docker/cagent） — legacy 既定の自動承認 | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [C07-09](#g-c07-ide-agents-09) | Docker — Docker Agent（docker/cagent） — 読み取り専用ツールセット | クライアントのソースコード | ツールを絞る・隠す | [確認] |
| [C07-10](#g-c07-ide-agents-10) | Docker — Docker Agent（docker/cagent） — ACP のツール種別 | クライアントのソースコード | 表示（印・名前） | [確認] |
| [C07-11](#g-c07-ide-agents-11) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode | クライアントの文書 | 危険度を付ける・信頼するなという注意・そのまま渡す・見せる | [確認] |
| [C07-12](#g-c07-ide-agents-12) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode 分類器プロンプト | クライアントのソースコード | 信頼するなという注意・危険度を付ける | [確認] |
| [C07-13](#g-c07-ide-agents-13) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 接続断後の安全な再送（設計文書） | クライアントの文書 | その他・規則（ポリシー）の条件に使う | [確認] |
| [C07-14](#g-c07-ide-agents-14) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 注釈が無いときの再送 | クライアントの文書 | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C07-15](#g-c07-ide-agents-15) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — canSafelyReplay | クライアントのソースコード | その他・規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [C07-16](#g-c07-ide-agents-16) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — ツール種別（Kind） | クライアントのソースコード | その他・表示（印・名前） | [確認] |
| [C07-17](#g-c07-ide-agents-17) | Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 並列実行してよい種別 | クライアントのソースコード | その他 | [確認] |
| [C07-18](#g-c07-ide-agents-18) | OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — security_risk の付与 | SDK のソースコード | 危険度を付ける | [確認] |
| [C07-19](#g-c07-ide-agents-19) | OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — read-only ツールのリスク | SDK のソースコード | 危険度を付ける・その他 | [確認] |
| [C07-20](#g-c07-ide-agents-20) | OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — MCP 注釈の取り込み | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C07-21](#g-c07-ide-agents-21) | Cognition (Devin / 旧 Windsurf) — Devin CLI | リリースノート | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [C07-22](#g-c07-ide-agents-22) | Cursor (Anysphere) — Cursor Origin MCP サーバー（Cursor 自身が出す MCP サーバー） | サーバの文書 | その他 | [確認] |
| [C07-23](#g-c07-ide-agents-23) | Cursor (Anysphere) — Cursor TypeScript SDK（local.customTools） | SDK の文書 | そのまま渡す・見せる・使わない・読まない | [確認] |
| [C07-24](#g-c07-ide-agents-24) | Cursor (Anysphere) — Cursor SDK（changelog） | リリースノート | そのまま渡す・見せる・使わない・読まない | [確認] |
| [C07-25](#g-c07-ide-agents-25) | Cline Bot Inc. — Cline SDK（ClineCore / CLI。sdk/packages/core） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-26](#g-c07-ide-agents-26) | Cline Bot Inc. — Cline VS Code 拡張（apps/vscode） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-27](#g-c07-ide-agents-27) | Roo Code Inc. — Roo Code（VS Code 拡張） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-28](#g-c07-ide-agents-28) | Kilo Code — Kilo Code（packages/opencode。OpenCode 派生） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-29](#g-c07-ide-agents-29) | Anomaly (SST) — OpenCode（anomalyco/opencode、旧 sst/opencode） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-30](#g-c07-ide-agents-30) | Continue Dev, Inc. — Continue（VS Code / JetBrains 拡張） | クライアントのソースコード | 使わない・読まない・宣言が無いときの扱い | [確認] |
| [C07-31](#g-c07-ide-agents-31) | Continue Dev, Inc. — Continue — Plan モードのツール選択 | クライアントのソースコード | 使わない・読まない・その他 | [確認] |
| [C07-32](#g-c07-ide-agents-32) | LibreChat — LibreChat（packages/api の MCP） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-33](#g-c07-ide-agents-33) | Open WebUI — Open WebUI（backend の MCP クライアント） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C07-34](#g-c07-ide-agents-34) | Warp — Warp（ターミナルの Agent Mode） | クライアントのソースコード | 使わない・読まない | [確認] |
| [G2CCM-01](#g-g2-closed-clients-missing-01) | Anthropic — Claude Code（CLI）2.1.287 — MCP ツールの包み（実装） | クライアントのソースコード | 宣言が無いときの扱い・規則（ポリシー）の条件に使う・その他 | [確認（調査時のみ）] |
| [G2CCM-02](#g-g2-closed-clients-missing-02) | Anthropic — Claude Code（CLI）2.1.287 — MCP ツールの包み（実装） | クライアントのソースコード | 宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認（調査時のみ）] |
| [G2CCM-03](#g-g2-closed-clients-missing-03) | Anthropic — Claude Code（CLI）2.1.287 — plan mode の許可判定（実装） | クライアントのソースコード | 確認を求める・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-04](#g-g2-closed-clients-missing-04) | Anthropic — Claude Code（CLI）2.1.287 — plan mode の許可判定（実装） | クライアントのソースコード | 確認を求める | [確認（調査時のみ）] |
| [G2CCM-05](#g-g2-closed-clients-missing-05) | Anthropic — Claude Code（CLI）2.1.287 — ツール呼び出しの並列化（実装） | クライアントのソースコード | その他 | [確認（調査時のみ）] |
| [G2CCM-06](#g-g2-closed-clients-missing-06) | Anthropic — Claude Code（CLI）2.1.287 — plan mode（承認待ちの間に plan mode に入ったとき） | クライアントのソースコード | その他・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-07](#g-g2-closed-clients-missing-07) | Anthropic — Claude Code（CLI）2.1.287 — 権限の提案（組み込みスキル fewer-permission-prompts と思われるプロンプト） | クライアントのソースコード | 信頼するなという注意・使わない・読まない | [確認（調査時のみ）] |
| [G2CCM-08](#g-g2-closed-clients-missing-08) | Anthropic — Claude Code（CLI）2.1.287 — auto mode（機能フラグつき） | クライアントのソースコード | 規則（ポリシー）の条件に使う・危険度を付ける | [確認（調査時のみ）] |
| [G2CCM-09](#g-g2-closed-clients-missing-09) | GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— 許可サービス | クライアントのソースコード | 確認を省く（自動で許可） | [確認] |
| [G2CCM-10](#g-g2-closed-clients-missing-10) | GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— MCP ツール一覧の取り込み | クライアントのソースコード | そのまま渡す・見せる・規則（ポリシー）の条件に使う | [確認] |
| [G2CCM-11](#g-g2-closed-clients-missing-11) | GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— ACP の許可要求 | クライアントのソースコード | 表示（印・名前）・その他 | [確認] |
| [G2CCM-12](#g-g2-closed-clients-missing-12) | Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（toolAllowlistMode "reads"） | クライアントのソースコード | 確認を省く（自動で許可）・ツールを絞る・隠す・宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認（調査時のみ）] |
| [G2CCM-13](#g-g2-closed-clients-missing-13) | Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（無効化の判定） | クライアントのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-14](#g-g2-closed-clients-missing-14) | Cursor (Anysphere) — Cursor 3.23.12 — ツールの読み / 書きの分類（利用者のトグル・表示） | クライアントのソースコード | 表示（印・名前）・ツールを絞る・隠す・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-15](#g-g2-closed-clients-missing-15) | Cursor (Anysphere) — Cursor 3.23.12 — Smart mode（分類器による自動実行） | クライアントのソースコード | 危険度を付ける・そのまま渡す・見せる | [確認（調査時のみ）] |
| [G2CCM-16](#g-g2-closed-clients-missing-16) | Cursor (Anysphere) — Cursor 3.23.12 — 独自の注釈キー cursor/requiresConfirmation | クライアントのソースコード | 確認を求める・その他 | [確認（調査時のみ）] |
| [G2CCM-17](#g-g2-closed-clients-missing-17) | Cognition — Devin CLI 3000.10.48（Devin Desktop 3.10.48 に同梱）— 制限モードでの MCP 呼び出し | クライアントのソースコード | ツールを絞る・隠す・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-18](#g-g2-closed-clients-missing-18) | Cognition — Devin Desktop 3.10.48 — ACP サーバーの MCP ツール一覧の表示 | クライアントのソースコード | 表示（印・名前）・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G2CCM-19](#g-g2-closed-clients-missing-19) | Cognition — Devin Desktop 3.10.48 — 拡張機能からバックエンドへのツール定義 | クライアントのソースコード | そのまま渡す・見せる | [確認（調査時のみ）] |
| [G2CCM-20](#g-g2-closed-clients-missing-20) | Google — Google Antigravity（2.0 / IDE / CLI）— MCP の権限 | クライアントの文書 | 確認を求める・使わない・読まない | [確認] |
| [G2CCM-21](#g-g2-closed-clients-missing-21) | Google — Antigravity SDK（Python, google-antigravity）— safe_defaults ポリシー | SDK のソースコード | 使わない・読まない・確認を求める | [確認] |
| [G2CCM-22](#g-g2-closed-clients-missing-22) | Google — Google Antigravity IDE 1.23.2 — language server（Go バイナリ） | クライアントのソースコード | そのまま渡す・見せる | [確認（調査時のみ）] |
| [G2CCM-23](#g-g2-closed-clients-missing-23) | Google — Google Cloud Data Agent Kit（Antigravity 等の IDE 拡張）— MCP 利用の制御 | 公式の文書 | 規則（ポリシー）の条件に使う | [確認] |
| [G2CCM-24](#g-g2-closed-clients-missing-24) | Mistral AI — Mistral Vibe（Vibe Code CLI, OSS）— ツール権限の既定 | クライアントのソースコード | 確認を求める・使わない・読まない | [確認] |
| [G2CCM-25](#g-g2-closed-clients-missing-25) | Mistral AI — Mistral Vibe（Vibe Code）— エージェントごとの承認 | クライアントの文書 | 使わない・読まない・その他 | [確認] |
| [G2CCM-26](#g-g2-closed-clients-missing-26) | Mistral AI — Mistral Vibe Work（旧 Le Chat のコネクタ）— 関数ごとの許可 | クライアントの文書 | 表示（印・名前） | [確認] |
| [G2CCM-27](#g-g2-closed-clients-missing-27) | Mistral AI — Mistral Studio（API）Connectors — 人の確認 | 公式の文書 | 使わない・読まない・確認を求める | [確認] |
| [G2CCM-28](#g-g2-closed-clients-missing-28) | Mistral AI — Mistral Studio（API）Connectors — ツール一覧 API | 公式の文書 | そのまま渡す・見せる | [確認] |
| [G2CCM-29](#g-g2-closed-clients-missing-29) | Perplexity — Perplexity Agent API — mcp ツール | 公式の文書 | 使わない・読まない・その他 | [確認] |
| [G2CCM-30](#g-g2-closed-clients-missing-30) | Zed Industries — Zed（ネイティブエージェント）— MCP ツールの種類 | クライアントのソースコード | 使わない・読まない | [確認] |
| [G2CCM-31](#g-g2-closed-clients-missing-31) | Zed Industries — Zed（ネイティブエージェント）— MCP ツールの承認 | クライアントのソースコード | 確認を求める・使わない・読まない | [確認] |
| [G2CCM-32](#g-g2-closed-clients-missing-32) | JetBrains — Junie（IDE プラグイン / CLI）— Action Allowlist | クライアントの文書 | 確認を求める・使わない・読まない | [確認] |
| [G2CCM-33](#g-g2-closed-clients-missing-33) | JetBrains — Junie CLI — Command approval | クライアントの文書 | 確認を求める・使わない・読まない | [確認] |
| [G2CCM-34](#g-g2-closed-clients-missing-34) | Anthropic — Claude Code（CLI）2.1.287 — auto mode の許可判定（MCP サーバーポリシーの ask ルール） | クライアントのソースコード | 規則（ポリシー）の条件に使う・宣言が無いときの扱い・危険度を付ける | [確認（調査時のみ）] |
| [G2CCM-35](#g-g2-closed-clients-missing-35) | Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（reads モード）による確認の省略 | クライアントのソースコード | 確認を省く（自動で許可）・規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認（調査時のみ）] |
| [G3AA-01](#g-g3-asia-agents-01) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP（in-process サーバー） | SDK の文書 | その他・表示（印・名前）・そのまま渡す・見せる | [確認] |
| [G3AA-02](#g-g3-asia-agents-02) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP | SDK の文書 | 表示（印・名前）・そのまま渡す・見せる | [確認] |
| [G3AA-03](#g-g3-asia-agents-03) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP | SDK の文書 | 表示（印・名前）・そのまま渡す・見せる | [確認] |
| [G3AA-04](#g-g3-asia-agents-04) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP | SDK の文書 | 使わない・読まない・信頼するなという注意 | [確認] |
| [G3AA-05](#g-g3-asia-agents-05) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP | SDK の文書 | 使わない・読まない | [確認] |
| [G3AA-06](#g-g3-asia-agents-06) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP | SDK の文書 | 作者への書き方の案内 | [確認] |
| [G3AA-07](#g-g3-asia-agents-07) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール） | SDK の文書 | そのまま渡す・見せる | [確認] |
| [G3AA-08](#g-g3-asia-agents-08) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール） | SDK の文書 | 使わない・読まない | [確認] |
| [G3AA-09](#g-g3-asia-agents-09) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール） | SDK の文書 | 作者への書き方の案内・使わない・読まない | [確認] |
| [G3AA-10](#g-g3-asia-agents-10) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — TypeScript 参照 | SDK の文書 | その他・使わない・読まない | [確認] |
| [G3AA-11](#g-g3-asia-agents-11) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — TypeScript 参照 | SDK の文書 | 使わない・読まない | [確認] |
| [G3AA-12](#g-g3-asia-agents-12) | Alibaba Cloud（Qoder CN。旧 通義灵码 Lingma の中国版） — Qoder CLI CN / Qoder Agent SDK — SDK MCP（中国語版） | SDK の文書 | 使わない・読まない・信頼するなという注意 | [確認] |
| [G3AA-13](#g-g3-asia-agents-13) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— MCP ツールの auto モード分類器入力 | クライアントのソースコード | 使わない・読まない | [確認] |
| [G3AA-14](#g-g3-asia-agents-14) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— /mcp のツール一覧の印 | クライアントのソースコード | 表示（印・名前） | [確認] |
| [G3AA-15](#g-g3-asia-agents-15) | Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— 外部 MCP ツールの発見 | クライアントのソースコード | その他 | [確認] |
| [G3AA-16](#g-g3-asia-agents-16) | Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review） | クライアントのソースコード | そのまま渡す・見せる・危険度を付ける | [確認] |
| [G3AA-17](#g-g3-asia-agents-17) | Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review） | クライアントのソースコード | 危険度を付ける | [確認] |
| [G3AA-18](#g-g3-asia-agents-18) | Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review） | クライアントのソースコード | 危険度を付ける・そのまま渡す・見せる | [確認] |
| [G3AA-19](#g-g3-asia-agents-19) | Moonshot AI — Kimi Code（MoonshotAI/kimi-code。TypeScript 版。旧 kimi-cli の後継） | クライアントのソースコード | 使わない・読まない | [確認] |
| [G3AA-20](#g-g3-asia-agents-20) | iFlow（iflow-ai。Alibaba 系の心流） — iFlow CLI（npm @iflow-ai/iflow-cli 0.5.19。Gemini CLI 系） | クライアントのソースコード | 使わない・読まない・確認を求める | [確認] |
| [G3AA-21](#g-g3-asia-agents-21) | Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope。エージェント枠組み、MCP クライアントを含む） | SDK のソースコード | 確認を省く（自動で許可）・宣言が無いときの扱い | [確認] |
| [G3AA-22](#g-g3-asia-agents-22) | Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope） | SDK のソースコード | 確認を省く（自動で許可）・確認を求める | [確認] |
| [G3AA-23](#g-g3-asia-agents-23) | Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— 許可エンジン | SDK のソースコード | 確認を省く（自動で許可）・規則（ポリシー）の条件に使う | [確認] |
| [G3AA-24](#g-g3-asia-agents-24) | Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— workspace のゲートウェイ経由ツール | SDK のソースコード | 確認を省く（自動で許可）・規則（ポリシー）の条件に使う | [確認] |
| [G3AA-25](#g-g3-asia-agents-25) | ByteDance（CloudWeGo） — Eino（cloudwego/eino-ext。Go のエージェント枠組みの MCP ツール部品 officialmcp） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [G3AA-26](#g-g3-asia-agents-26) | ByteDance — DeerFlow（bytedance/deer-flow）— 同梱の業務連携 MCP サーバー（HubSpot など） | サーバのソースコード | 作者への書き方の案内 | [確認] |

この分冊の資料は 95 件で、うち [確認] は 76 件、[確認（調査時のみ）] は 19 件。

<a id="ag-7-1"></a>
## 資料カード

### AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionInspector

<a id="g-c07-ide-agents-01"></a>
#### C07-01 AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionInspector

- **資料**: crates/goose/src/permission/permission_inspector.rs: apply_tool_annotations（クライアントのソースコード）
- **URL**: https://github.com/aaif-goose/goose/blob/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/permission/permission_inspector.rs#L52-L64
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aaif-goose/goose/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/permission/permission_inspector.rs
- **版**: commit 591edd47cf2cfea4957d720c607cf2a4def8673d（aaif-goose/goose の 2026-10-02 時点の HEAD）
- **書いてある場所**: L52-64
- **原文**:

```
    pub fn apply_tool_annotations(&self, tools: &[Tool]) {
        let mut readonly_annotated = HashSet::new();
        for tool in tools {
            let Some(anns) = &tool.annotations else {
                continue;
            };
            if anns.read_only_hint == Some(true) {
                readonly_annotated.insert(tool.name.to_string());
            }
        }
        *self.readonly_tools.write().unwrap() = readonly_annotated;
        self.permission_manager.apply_tool_annotations(tools);
    }
```

- **日本語**: ツール一覧を受け取るたびに、annotations の read_only_hint が true のツール名だけを「読み取り専用」の集合に入れ、残りは PermissionManager に渡す。
- **どう使っているか**: goose は MCP サーバーが宣言した readOnlyHint:true をそのまま集合に登録し、SmartApprove モードで承認なしに通す判定（C07_ide_agents-02）の材料にする。宣言の真偽は確かめない。
- **条件**: 集合はエージェントごと。値が明示の true のときだけ登録（None・false は登録しない）。この集合が承認に効くのは利用者が Smart Approve モードを選んだときだけ。goose の既定は Autonomous（Auto）モードで、そこでは注釈に関係なく全ツールが許可される（goose 文書『Autonomous Mode is applied by default.』goose Permission Modes > Permission Modes、検証者が verify_quote.py で exact）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、52-64 行（取得 2026-10-02T22:12:55Z、sha256 c9944a12742c…）
- **補足**: 同ファイルの 50〜51 行のコメント: readonly_tools is per-agent ... write-annotated tools are cached globally via PermissionManager（03）。 conditions に「既定は Autonomous モードで、注釈が効くのは Smart Approve を選んだときだけ」を足した（文書の引用を tool で exact 照合: match=exact count=1 sha256=dc4849e438f7 goose Permission Modes > Permission Modes）。

### AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — SmartApprove の判定順

<a id="g-c07-ide-agents-02"></a>
#### C07-02 AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — SmartApprove の判定順

- **資料**: crates/goose/src/permission/permission_inspector.rs: inspect()（クライアントのソースコード）
- **URL**: https://github.com/aaif-goose/goose/blob/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/permission/permission_inspector.rs#L162-L193
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aaif-goose/goose/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/permission/permission_inspector.rs
- **版**: commit 591edd47cf2cfea4957d720c607cf2a4def8673d（aaif-goose/goose の 2026-10-02 時点の HEAD）
- **書いてある場所**: L162-193
- **原文**:

```
                    GooseMode::Approve | GooseMode::SmartApprove => {
                        // 1. Check user-defined permission first
                        if let Some(level) = permission_manager.get_user_permission(tool_name) {
                            match level {
                                PermissionLevel::AlwaysAllow => InspectionAction::Allow,
                                PermissionLevel::NeverAllow => InspectionAction::Deny,
                                PermissionLevel::AskBefore => {
                                    InspectionAction::RequireApproval(None)
                                }
                            }
                        // 2. Check for a read-only annotation in SmartApprove mode
                        } else if goose_mode == GooseMode::SmartApprove
                            && self.is_readonly_annotated_tool(tool_name)
                        {
                            InspectionAction::Allow
                        // 3. Special case for extension management
                        } else if tool_name == MANAGE_EXTENSIONS_TOOL_NAME_COMPLETE {
                            InspectionAction::RequireApproval(Some(
                                "Extension management requires approval for security".to_string(),
                            ))
                        // 4. Defer to LLM detection (SmartApprove, uncached or legacy cached allow)
                        } else if goose_mode == GooseMode::SmartApprove
                            && matches!(
                                permission_manager.get_smart_approve_permission(tool_name),
                                None | Some(PermissionLevel::AlwaysAllow)
                            )
                        {
                            llm_detect_candidates.push(request);
                            continue;
                        // 5. Default: require approval for unknown tools
                        } else {
                            InspectionAction::RequireApproval(None)
```

- **日本語**: Approve / SmartApprove モードでは、1) ユーザーが設定した権限を先に見る、2) SmartApprove なら read-only 注釈つきツールを許可、3) 拡張管理ツールは承認必須、4) SmartApprove でまだ決まっていないものは LLM の判定に回す、5) それ以外は承認を求める。
- **どう使っているか**: Smart Approve モードでは、利用者のツール別設定が無ければ、readOnlyHint:true の宣言だけで permission inspector が確認なしの Allow を返す（宣言の真偽は確かめない）。ただし security など他の inspector が RequireApproval / Deny を返せば、その判定が優先される（tool_inspection.rs 253〜256 行: Allow は他の判定を上書きしない）。宣言が無いツールは LLM による read-only 判定（detect_read_only_requests）に回り、readOnlyHint:false のツールは AskBefore（03）で確認になる。Approve モードでは注釈は使われず承認を求める。Auto モードは全部許可、Chat モードはツールを使わない。
- **条件**: GooseMode::SmartApprove のときだけ注釈が効く。goose の既定は Autonomous（Auto）モード（文書『Autonomous Mode is applied by default.』exact）なので、Smart Approve は利用者が選んだときだけ。permission.yaml などのユーザー設定（get_user_permission）が最優先。拡張管理ツールは例外で常に承認。permission inspector 以外の inspector の結果は上書きとして後から当てられる（permission_inspector.rs 116 行『Apply security and other inspector results as overrides』）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、162-193 行（取得 2026-10-02T22:12:55Z、sha256 c9944a12742c…）
- **補足**: 公開文書（goose-docs.ai の goose-permissions）は「LLM が read/write を分類する」とだけ書き、annotations には触れない（checked_no_mention 参照）。文書とコードで説明がずれている。 usage_ja と conditions を直した。(1) 既定は Autonomous で Smart Approve は選んだときだけ（goose 文書、match=exact count=1 sha256=dc4849e438f7 goose Permission Modes > Permission Modes）。(2) 「確認なしに実行される」は permission inspector の判定で、他の inspector（security など）が確認・拒否を返せばそちらが勝つ（tool_inspection.rs match=exact count=1 sha256=291072d02fdd L253-256、permission_inspector.rs match=exact count=1 sha256=c9944a12742c L116）。finder の書き方は自動承認を無条件に読めた。

### AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionManager

<a id="g-c07-ide-agents-03"></a>
#### C07-03 AAIF (Agentic AI Foundation) / Block — goose（AAIF / 旧 Block。CLI・Desktop） — PermissionManager

- **資料**: crates/goose/src/config/permission.rs: PermissionManager::apply_tool_annotations（クライアントのソースコード）
- **URL**: https://github.com/aaif-goose/goose/blob/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/config/permission.rs#L91-L107
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/aaif-goose/goose/591edd47cf2cfea4957d720c607cf2a4def8673d/crates/goose/src/config/permission.rs
- **版**: commit 591edd47cf2cfea4957d720c607cf2a4def8673d（aaif-goose/goose の 2026-10-02 時点の HEAD）
- **書いてある場所**: L91-107
- **原文**:

```
    pub fn apply_tool_annotations(&self, tools: &[Tool]) {
        let mut write_annotated = Vec::new();
        for tool in tools {
            let Some(anns) = &tool.annotations else {
                continue;
            };
            if anns.read_only_hint == Some(false) {
                write_annotated.push(tool.name.to_string());
            }
        }
        if !write_annotated.is_empty() {
            self.bulk_update_smart_approve_permissions(
                &write_annotated,
                PermissionLevel::AskBefore,
            );
        }
    }
```

- **日本語**: annotations の read_only_hint が明示的に false のツール名を集め、SmartApprove 用の権限表で「実行前に確認（AskBefore）」に一括で書き込む。
- **どう使っているか**: readOnlyHint:false を宣言したツールは、Smart Approve の権限キャッシュに AskBefore（毎回確認）として書き込まれる。宣言が無いツール（None）はこの処理の対象外。利用者のツール別設定（get_user_permission）があればそちらが先に効く（02 の判定順 1）。
- **条件**: SmartApprove 用の権限表（SMART_APPROVE_PERMISSION）への書き込み。always_allow / ask_before / never_allow の既存登録をいったん消してから AskBefore を入れる（109〜116 行）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、91-107 行（取得 2026-10-02T22:11:35Z、sha256 5f57b0fbb777…）
- **補足**: 「AskBefore に固定される」を弱めた。キャッシュへの書き込みであり、利用者のツール別設定が先に判定される（permission_inspector.rs 164〜171 行、目視）。

### n8n — n8n（Instance AI の MCP ツール権限）

<a id="g-c07-ide-agents-04"></a>
#### C07-04 n8n — n8n（Instance AI の MCP ツール権限）

- **資料**: packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts: classifyMcpTool（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts#L73-L88
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/ai-utilities/src/agent-config/mcp-tool-permissions.ts
- **版**: commit bae76563474e488421653d8ca0744feb5e99c957（n8n-io/n8n の 2026-10-02 時点の HEAD）
- **書いてある場所**: L73-88
- **原文**:

```
export function classifyMcpTool(tool: McpToolDescriptor): McpToolCategory {
	const segments = toolNameSegments(tool.name);
	const hasWriteName = segments.some((segment) => WRITE_SEGMENTS.has(segment));

	if (tool.annotations?.readOnlyHint === false || tool.annotations?.destructiveHint === true) {
		return 'write';
	}

	if (tool.annotations?.readOnlyHint === true) {
		return 'read';
	}

	if (hasWriteName) return 'write';

	return segments.some((segment) => READ_SEGMENTS.has(segment)) ? 'read' : 'write';
}
```

- **日本語**: readOnlyHint が false か destructiveHint が true なら「書き込み」、readOnlyHint が true なら「読み取り」。注釈が無いときはツール名の語（create, delete など／get, list など）で決め、どちらでもなければ「書き込み」にする。
- **どう使っているか**: n8n は MCP ツールを read / write の 2 類に分け、類ごとの権限（always_allow / require_approval / blocked）を当てる。分類は注釈を名前より優先し、readOnlyHint:true だけで read 類になる。注釈が無いときは名前で推測し、決まらなければ安全側の write。
- **条件**: ツール名ごとの個別設定（policy.tools[tool.name]）があればそちらが優先（resolveMcpToolPermission）。blocked はツール一覧から除外、require_approval は承認リストへ（compileMcpToolPermissions）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、73-88 行（取得 2026-10-02T22:11:36Z、sha256 c26f3881fd76…）
- **補足**: この関数を Instance AI の MCP クライアントが使うことを検証者が tool で照合した: packages/@n8n/instance-ai/src/mcp/mcp-client-manager.ts の 『configureTools: (tools) => compileMcpToolPermissions(toolPermissions, tools),』（match=exact count=1 sha256=a82b93bd186f L88）と、外部 MCP の既定の権限を 『categories: { read: mcpRead, write: mcpWrite },』（match=exact count=1 sha256=a82b93bd186f L202）で作る箇所。n8n の MCP Client Tool ノードの文書には注釈の記述なし（checked_no_mention）。 finder が「目視のみ、tool で照合していない」とした Instance AI 側の利用箇所（mcp-client-manager.ts 88 行・202 行）を tool で exact 照合し、notes を書き換えた。

### n8n — n8n（Instance AI の MCP ツール権限） — 既定値

<a id="g-c07-ide-agents-05"></a>
#### C07-05 n8n — n8n（Instance AI の MCP ツール権限） — 既定値

- **資料**: packages/@n8n/api-types/src/schemas/instance-ai.schema.ts: DEFAULT_INSTANCE_AI_PERMISSIONS（クライアントのソースコード）
- **URL**: https://github.com/n8n-io/n8n/blob/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/api-types/src/schemas/instance-ai.schema.ts#L2371-L2372
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/n8n-io/n8n/bae76563474e488421653d8ca0744feb5e99c957/packages/@n8n/api-types/src/schemas/instance-ai.schema.ts
- **版**: commit bae76563474e488421653d8ca0744feb5e99c957（n8n-io/n8n の 2026-10-02 時点の HEAD）
- **書いてある場所**: L2371-2372（tool の報告は L2371-2373。開始行は一致、終了行の数え方が違う。引用は L2371-2372 の行そのもの）
- **原文**:

> 	mcpRead: 'always_allow',
> 	mcpWrite: 'require_approval',

- **日本語**: 既定では、MCP の読み取りツールは常に許可、書き込みツールは承認が必要。
- **どう使っているか**: C07_ide_agents-04 の分類と組み合わせると、既定設定（ツール名ごとの個別設定なし）では、readOnlyHint:true と宣言し destructiveHint:true を宣言していない MCP ツールは承認なしで実行される。注釈が無いツールも、名前が read 系の語（get・list・search など）を含み write 系の語を含まなければ read 類になり、同じく承認なしになる。
- **条件**: Instance AI の権限設定の既定値。利用者が mcpRead / mcpWrite を変更できる（instance-ai.schema.ts 2342〜2343 行の enum: always_allow / require_approval / blocked）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、2371-2372 行（取得 2026-10-02T22:11:44Z、sha256 a27db6e360b5…）
- **補足**: usage_ja に「個別設定が無いとき」の条件と、注釈なしでも名前の推測で read 類になれば既定で承認なしになること（mcp-tool-permissions.ts 81〜87 行、04 の引用の範囲内）を足した。

### Docker — Docker Agent（docker/cagent） — safety ラベル

<a id="g-c07-ide-agents-06"></a>
#### C07-06 Docker — Docker Agent（docker/cagent） — safety ラベル

- **資料**: pkg/safety/safety.go: LabelForHints（クライアントのソースコード）
- **URL**: https://github.com/docker/cagent/blob/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/safety/safety.go#L114-L125
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/cagent/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/safety/safety.go
- **版**: commit 5517a597150afefa6e0d441f1d9893db4ed712ad（docker/cagent の 2026-10-02 時点の HEAD）
- **書いてある場所**: L114-125
- **原文**:

```
// LabelForHints maps MCP annotation hints onto a label. DestructiveHint
// wins over ReadOnlyHint; neither yields [ClassUnknown].
func LabelForHints(readOnlyHint, destructiveHint bool) Label {
	switch {
	case destructiveHint:
		return Label{Class: ClassDestructive, Origin: OriginAnnotation, BlastRadius: "high"}
	case readOnlyHint:
		return Label{Class: ClassSafe, Origin: OriginAnnotation, BlastRadius: "safe"}
	default:
		return Label{Class: ClassUnknown, Origin: OriginAnnotation}
	}
}
```

- **日本語**: MCP の注釈をラベルに変える。destructiveHint があれば「破壊的」（影響大）、readOnlyHint があれば「安全」、どちらも無ければ「不明」。destructiveHint が readOnlyHint より優先。
- **どう使っているか**: シェル以外のツールの安全ラベルは MCP 注釈だけで決まる。ラベルの由来（OriginAnnotation）も記録され、後段の承認表（C07_ide_agents-07・08）の入力になる。注釈なしは ClassUnknown。
- **条件**: shell / run_background_job はコマンド文字列の分類器で判定し、注釈は使わない（LabelToolCall）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 危険度を付ける・規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、114-125 行（取得 2026-10-02T22:12:00Z、sha256 79fda5914eab…）
- **補足**: ラベル付けの呼び出し元（pkg/runtime/toolexec/dispatcher.go 354〜355 行）は『destructive := c.tool.Annotations.DestructiveHint != nil && *c.tool.Annotations.DestructiveHint』で、destructiveHint が未指定なら false として渡す（match=exact count=1 sha256=510d3686d0de L354-355）。MCP 仕様の既定値（destructiveHint=true）とは違い、readOnlyHint:false で destructiveHint 未指定のツールは destructive ではなく unknown になる。 destructiveHint が未指定のとき false 扱い（仕様の既定 true と違う）であることを notes に足した（dispatcher.go を tool で exact 照合）。

### Docker — Docker Agent（docker/cagent） — (モード × ラベル) 承認表

<a id="g-c07-ide-agents-07"></a>
#### C07-07 Docker — Docker Agent（docker/cagent） — (モード × ラベル) 承認表

- **資料**: pkg/runtime/toolexec/permissions.go: applyMode のコメント（クライアントのソースコード）
- **URL**: https://github.com/docker/cagent/blob/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/runtime/toolexec/permissions.go#L113-L129
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/cagent/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/runtime/toolexec/permissions.go
- **版**: commit 5517a597150afefa6e0d441f1d9893db4ed712ad（docker/cagent の 2026-10-02 時点の HEAD）
- **書いてある場所**: L113-129
- **原文**:

```
// applyMode implements the (mode × label) → verdict table:
//
//	              safe     destructive   unknown
//	strict        ask      ask           ask
//	balanced      ALLOW    ask           ask
//	restricted    ALLOW    DENY          DENY
//	autonomous    ALLOW    ALLOW         ALLOW
//	"" (legacy)   ask*     ask           ask
//
// (*) the legacy default — a session whose mode was never explicitly
// chosen — additionally auto-approves annotation-safe (read-only
// hinted) calls, but only AFTER the default pre_tool_use hook chain
// has had its turn; see the dispatcher's approveAndRun. That keeps the
// pre-modes contract: hooks can veto read-only calls, and read-only
// tools never prompt. Restricted is the fail-closed profile for
// unattended runs: it never prompts, denying whatever it would not
// allow. Unrecognised modes are treated as strict so an invalid value
```

- **日本語**: モードとラベルの表: strict は全部確認、balanced は安全なら許可・他は確認、restricted は安全なら許可・他は拒否、autonomous は全部許可、未選択（legacy）は全部確認（ただし注釈で安全なものは後で自動承認）。
- **どう使っているか**: 注釈から ClassSafe（readOnlyHint:true で、destructiveHint:true ではない）と付いたツールは、balanced と restricted モードでは確認なしに実行される。restricted では unknown（注釈なし・readOnlyHint:false で destructiveHint 未指定を含む）と destructive は拒否される。autonomous は全部許可、strict は全部確認。
- **条件**: 判定順は dispatcher.go のコメント『Order: input transforms → mandatory guards → legacy preempt hooks → permission rules / safety mode → legacy approval hooks → user confirmation.』（match=exact count=1 sha256=510d3686d0de L444-446）。permission checker（セッション／チームの allow・deny 規則）が先に判定し、決まらないときにこの表に落ちる（同ファイル 95〜110 行）。不明なモードは strict 扱い。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、113-129 行（取得 2026-10-02T22:11:34Z、sha256 a0a44ee81796…）
- **補足**: usage_ja で ClassSafe の条件（destructiveHint:true が無いこと）と unknown の中身を明記。conditions に、表より前に mandatory guards などが効く判定順を足した（tool で exact）。

### Docker — Docker Agent（docker/cagent） — legacy 既定の自動承認

<a id="g-c07-ide-agents-08"></a>
#### C07-08 Docker — Docker Agent（docker/cagent） — legacy 既定の自動承認

- **資料**: pkg/runtime/toolexec/permissions.go: legacyReadOnlyAutoApprove（クライアントのソースコード）
- **URL**: https://github.com/docker/cagent/blob/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/runtime/toolexec/permissions.go#L152-L159
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/cagent/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/runtime/toolexec/permissions.go
- **版**: commit 5517a597150afefa6e0d441f1d9893db4ed712ad（docker/cagent の 2026-10-02 時点の HEAD）
- **書いてある場所**: L152-159
- **原文**:

```
// legacyReadOnlyAutoApprove reports whether the legacy default mode
// auto-approves this call: no mode was ever chosen and the tool
// advertises itself read-only via annotations. Classifier-derived
// safety deliberately does not qualify — the legacy default predates
// the classifier and must not widen.
func legacyReadOnlyAutoApprove(mode session.SafetyPolicy, label safety.Label) bool {
	return mode == "" && label.Class == safety.ClassSafe && label.Origin == safety.OriginAnnotation
}
```

- **日本語**: モードを一度も選んでいないセッションでは、注釈で read-only と宣言したツールを自動承認する。分類器由来の「安全」は対象外。
- **どう使っているか**: safety モード導入前からの約束として、モード未選択の既定では readOnlyHint の宣言だけで承認なしに実行される（pre_tool_use フックの後）。
- **条件**: mode == ""（未選択）かつラベルが注釈由来の ClassSafe のとき。pre_tool_use フック連鎖の後に評価される（フックは拒否できる）。明示の Strict ではこの経路を通らない（dispatcher.go 483〜490 行のコメントと分岐、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、152-159 行（取得 2026-10-02T22:11:34Z、sha256 a0a44ee81796…）
- **補足**: conditions の行番号を 481〜490 から 483〜490 に直し、フックの後で評価されることを足した。

### Docker — Docker Agent（docker/cagent） — 読み取り専用ツールセット

<a id="g-c07-ide-agents-09"></a>
#### C07-09 Docker — Docker Agent（docker/cagent） — 読み取り専用ツールセット

- **資料**: pkg/tools/description.go: FilterReadOnly（クライアントのソースコード）
- **URL**: https://github.com/docker/cagent/blob/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/tools/description.go#L48-L59
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/cagent/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/tools/description.go
- **版**: commit 5517a597150afefa6e0d441f1d9893db4ed712ad（docker/cagent の 2026-10-02 時点の HEAD）
- **書いてある場所**: L48-59
- **原文**:

```
// FilterReadOnly returns only the tools whose annotations carry a read-only
// hint. It is used to enforce read-only toolsets and read-only agents: every
// mutating tool is dropped so it can neither be listed nor called.
func FilterReadOnly(toolList []Tool) []Tool {
	var filtered []Tool
	for _, tool := range toolList {
		if tool.Annotations.ReadOnlyHint {
			filtered = append(filtered, tool)
		}
	}
	return filtered
}
```

- **日本語**: 注釈に read-only の印があるツールだけを残す。読み取り専用のツールセットやエージェントで使い、書き換えるツールは一覧からも呼び出しからも外す。
- **どう使っているか**: 「読み取り専用エージェント」は宣言（readOnlyHint）だけを根拠にツールを絞る。宣言が偽ならそのまま通る。
- **条件**: read-only を指定したツールセット／エージェントのとき（呼び出し元: pkg/teamloader/readonly.go）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、48-59 行（取得 2026-10-02T22:11:30Z、sha256 4abb18c83f27…）
- **補足**: destructiveHint は見ない（L54 は ReadOnlyHint だけを見る）ので、readOnlyHint:true と destructiveHint:true を同時に宣言したツールも read-only ツールセットに残る（検証者の目視）。 destructiveHint を見ないことを notes に足した（解釈の訂正ではなく補足）。

### Docker — Docker Agent（docker/cagent） — ACP のツール種別

<a id="g-c07-ide-agents-10"></a>
#### C07-10 Docker — Docker Agent（docker/cagent） — ACP のツール種別

- **資料**: pkg/acp/toolcall.go: ツール種別の決定（クライアントのソースコード）
- **URL**: https://github.com/docker/cagent/blob/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/acp/toolcall.go#L130-L134
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/docker/cagent/5517a597150afefa6e0d441f1d9893db4ed712ad/pkg/acp/toolcall.go
- **版**: commit 5517a597150afefa6e0d441f1d9893db4ed712ad（docker/cagent の 2026-10-02 時点の HEAD）
- **書いてある場所**: L130-134
- **原文**:

```
	default:
		if tool.Annotations.ReadOnlyHint {
			return acp.ToolKindRead
		}
		return acp.ToolKindOther
```

- **日本語**: 名前で決まらないツールは、readOnlyHint があれば ACP の「read」種別、無ければ「other」にする。
- **どう使っているか**: ACP（Agent Client Protocol）でエディタに渡すツール種別（表示）に readOnlyHint を使う。ただし名前の接頭辞の規則が先で、readOnlyHint はどの規則にも当たらないツールにだけ効く。
- **条件**: determineToolKind（L89『// determineToolKind maps tool names and annotations to ACP tool kinds.』、match=exact count=1 sha256=879749cfc171 L89）は、read_ / get_ / list_ → Read、edit_ / write_ / update_ / create_ / add_ → Edit、delete_ / remove_ → Delete、search_ / find_ → Search、fetch / http_ → Fetch、shell / run_ / exec_ / stop_ → Execute などの名前の規則を先に当てる（L92〜128、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、130-134 行（取得 2026-10-02T22:11:41Z、sha256 879749cfc171…）
- **補足**: 名前の規則が注釈より先に当たること（default 分岐でだけ readOnlyHint を見る）を usage_ja と conditions に足した。

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode

<a id="g-c07-ide-agents-11"></a>
#### C07-11 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode

- **資料**: docs/users/features/auto-mode.md（Limitations）（クライアントの文書）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/docs/users/features/auto-mode.md#L292-L296
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/docs/users/features/auto-mode.md
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc（docs/users/features/auto-mode.md）
- **書いてある場所**: L292-296 (## Limitations)
- **原文**:

```
every call from a server that is not marked `trust: true` goes to the
  classifier with the server name, the tool name, the server's
  self-reported annotations (`readOnlyHint` / `destructiveHint` /
  `idempotentHint` / `openWorldHint`) and a bounded copy of the
  arguments. The classifier is told the annotations are unverified.
```

- **日本語**: trust: true でないサーバーからの呼び出しは、サーバー名・ツール名・サーバー自己申告の注釈 4 種・引数の写しといっしょに分類器へ送られる。分類器には注釈が未検証だと伝える。
- **どう使っているか**: auto mode では、trust: true でないサーバーの MCP ツール呼び出しはすべて LLM 分類器に回り、サーバーの自己申告の注釈（4 つの hint）も渡されるが、分類器には「注釈は未検証」と伝えられる。「注釈だけで許可しない」は分類器プロンプト（12）の文。trust: true のサーバーの扱いはこの文からは直接は分からない（下の conditions）。
- **条件**: auto mode のとき。mcp__* ツールは高速許可リストに入らない。permissions.allow に mcp__server__tool を書けば分類器を迂回。trust: true のサーバーは、信頼済みフォルダなら既定の権限が allow になる（packages/core/src/tools/mcp-tool.ts 390〜394 行、match=exact count=1 sha256=ba31a98c212b L390-394）ので、分類器を通らず実行されるとみられる（auto mode との組み合わせは未照合）。permissions.autoMode.mcp.forwardArguments: false にすると分類器には名前だけが渡る。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 危険度を付ける・信頼するなという注意・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、292-296 行（## Limitations）（取得 2026-10-02T22:11:39Z、sha256 b922bf1c816b…）
- **補足**: 公開 URL は GitHub 上の Markdown（qwen-code の docs サイトの同ページは未確認）。 usage_ja の「承認の根拠にはならない」はこの引用（『The classifier is told the annotations are unverified.』）より強いので、12 の文に帰属させた。「trust: true のサーバーは分類器を通らない」は文書の『not marked trust: true』からの推論なので、コードの既定権限（tool で exact）を根拠に足し、auto mode での確認は未照合と書いた。

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode 分類器プロンプト

<a id="g-c07-ide-agents-12"></a>
#### C07-12 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — auto mode 分類器プロンプト

- **資料**: packages/core/src/permissions/classifier-prompts/system-prompt.ts（クライアントのソースコード）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/permissions/classifier-prompts/system-prompt.ts#L109
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/permissions/classifier-prompts/system-prompt.ts
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc
- **書いてある場所**: L109
- **原文**:

> `annotations` (readOnlyHint / destructiveHint / idempotentHint / openWorldHint) are self-reported by the server and unverified — they may raise suspicion but never justify allowing an action on their own.

- **日本語**: 注釈はサーバーの自己申告で未検証。疑いを強めることはあっても、それだけで実行を許す理由にはならない。
- **どう使っているか**: 分類器への指示で、注釈を「疑いを増やす方向にだけ使い、減らす方向には使わない」と明記している。敵対的・不具合のあるサーバーは何にでも readOnlyHint を付けられる、とコード中のコメント（107 行）も述べる。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 信頼するなという注意・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、109 行（取得 2026-10-02T22:11:32Z、sha256 f58ba29f0155…）

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 接続断後の安全な再送（設計文書）

<a id="g-c07-ide-agents-13"></a>
#### C07-13 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 接続断後の安全な再送（設計文書）

- **資料**: docs/design/mcp-safe-replay.md（Replay policy）（クライアントの文書）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/docs/design/mcp-safe-replay.md#L14
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/docs/design/mcp-safe-replay.md
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc
- **書いてある場所**: L14 (## Replay policy)
- **原文**:

> - The tool declares `idempotentHint: true`, or declares `readOnlyHint: true` without `destructiveHint: true` or `idempotentHint: false`.

- **日本語**: ツールが idempotentHint: true を宣言している、または readOnlyHint: true を宣言し、かつ destructiveHint: true も idempotentHint: false も宣言していない場合（に限り自動再送する）。
- **どう使っているか**: 接続が切れた tools/call を自動で再送してよいかを、注釈で決める。承認ではなく「再実行の安全性」に idempotentHint を使う珍しい例。矛盾する注釈（readOnly かつ destructive など）は安全とみなさない。
- **条件**: 接続断と分類された失敗、サーバーが trust: true、ワークスペースが信頼済み、の全部を満たすとき。再接続後の新しいツール定義にも同じ確認をする。
- **扱う宣言**: idempotentHint・readOnlyHint・destructiveHint ／ **使い方の分類**: その他・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、14 行（## Replay policy）（取得 2026-10-02T22:11:31Z、sha256 4f2b6e5f129b…）

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 注釈が無いときの再送

<a id="g-c07-ide-agents-14"></a>
#### C07-14 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 注釈が無いときの再送

- **資料**: docs/design/mcp-safe-replay.md（Compatibility）（クライアントの文書）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/docs/design/mcp-safe-replay.md#L30
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/docs/design/mcp-safe-replay.md
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc
- **書いてある場所**: L30 (## Compatibility)
- **原文**:

> Tools without annotations no longer receive transparent connection-loss replay, even when an older Qwen Code release retried them. Servers that want replay must provide accurate annotations, and administrators must opt into server trust in a trusted workspace.

- **日本語**: 注釈の無いツールは、接続断のときの自動再送を受けなくなった（古い版では再送していても）。再送してほしいサーバーは正確な注釈を出し、管理者は信頼済みワークスペースでサーバーを trust にする必要がある。
- **どう使っているか**: 注釈なし＝既定どおり非冪等とみなし、自動再送しない（安全側）。サーバー作者に正確な注釈を求めている。
- **扱う宣言**: idempotentHint・readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、30 行（## Compatibility）（取得 2026-10-02T22:11:31Z、sha256 4f2b6e5f129b…）

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — canSafelyReplay

<a id="g-c07-ide-agents-15"></a>
#### C07-15 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — canSafelyReplay

- **資料**: packages/core/src/tools/mcp-tool.ts: canSafelyReplay（クライアントのソースコード）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/mcp-tool.ts#L553-L574
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/mcp-tool.ts
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc（QwenLM/qwen-code の 2026-10-02 時点の HEAD）
- **書いてある場所**: L553-574
- **原文**:

```
  private canSafelyReplay(): boolean {
    if (
      this.trust !== true ||
      this.cliConfig?.isTrustedFolder() !== true ||
      !this.annotations
    ) {
      return false;
    }

    if (
      this.annotations.readOnlyHint === true &&
      (this.annotations.destructiveHint === true ||
        this.annotations.idempotentHint === false)
    ) {
      return false;
    }

    return (
      this.annotations.idempotentHint === true ||
      this.annotations.readOnlyHint === true
    );
  }
```

- **日本語**: trust でない・信頼済みフォルダでない・注釈が無い、なら再送しない。readOnlyHint が true でも destructiveHint true か idempotentHint false があれば再送しない。idempotentHint true か readOnlyHint true なら再送してよい。
- **どう使っているか**: C07_ide_agents-13 の設計文書どおりの実装。注釈は「自動再実行」の可否の入力。
- **条件**: MCP 呼び出しが接続断で失敗したとき（execute 内の再接続処理）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: その他・規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、553-574 行（取得 2026-10-02T22:11:58Z、sha256 ba31a98c212b…）

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — ツール種別（Kind）

<a id="g-c07-ide-agents-16"></a>
#### C07-16 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — ツール種別（Kind）

- **資料**: packages/core/src/tools/mcp-tool.ts: DiscoveredMCPTool のコンストラクタ（クライアントのソースコード）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/mcp-tool.ts#L1198
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/mcp-tool.ts
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc（QwenLM/qwen-code の 2026-10-02 時点の HEAD）
- **書いてある場所**: L1198
- **原文**:

```
      annotations?.readOnlyHint === true ? Kind.Read : Kind.Other,
```

- **日本語**: readOnlyHint が true なら種別を Read、それ以外は Other にする。
- **どう使っているか**: MCP ツールの内部種別（Kind）を readOnlyHint で決める。Kind.Read はスケジューラで並列実行してよい種別として扱われる（C07_ide_agents-17、検証者が呼び出し側を照合）。Kind が承認判断に使われるかは確認していない（不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、1198 行（取得 2026-10-02T22:11:58Z、sha256 ba31a98c212b…）
- **補足**: 17 の呼び出し側（スケジューラ）を検証者が照合したので usage_ja を合わせた。

### Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 並列実行してよい種別

<a id="g-c07-ide-agents-17"></a>
#### C07-17 Alibaba Qwen (QwenLM) — Qwen Code（QwenLM/qwen-code） — 並列実行してよい種別

- **資料**: packages/core/src/tools/tools.ts: CONCURRENCY_SAFE_KINDS（クライアントのソースコード）
- **URL**: https://github.com/QwenLM/qwen-code/blob/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/tools.ts#L1314-L1323
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/QwenLM/qwen-code/c15dd268c013742506f2e1cdf043926fa75442bc/packages/core/src/tools/tools.ts
- **版**: commit c15dd268c013742506f2e1cdf043926fa75442bc（QwenLM/qwen-code の 2026-10-02 時点の HEAD）
- **書いてある場所**: L1314-1323（tool の報告は L1314-1325。開始行は一致、終了行の数え方が違う。引用は L1314-1323 の行そのもの）
- **原文**:

```
/**
 * Tool kinds that are safe to execute concurrently (pure reads, no writes).
 * Kind.Think is excluded because some Think tools write to disk
 * (e.g., save_memory, todo_write).
 */
export const CONCURRENCY_SAFE_KINDS: ReadonlySet<Kind> = new Set([
  Kind.Read,
  Kind.Search,
  Kind.Fetch,
]);
```

- **日本語**: 並列に実行して安全なツール種別（純粋な読み取りで書き込みなし）は Read・Search・Fetch。
- **どう使っているか**: C07_ide_agents-16 と合わせると、readOnlyHint:true を宣言した MCP ツールは「並列実行して安全」として扱われ、連続する同種の呼び出しが並列のバッチにまとめられる。宣言が偽なら書き込みが並列に走りうる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、1314-1323 行（取得 2026-10-02T22:11:28Z、sha256 421090a89233…）
- **補足**: 呼び出し側を検証者が照合: packages/core/src/core/coreToolScheduler.ts の isToolCallConcurrencySafe が『  if (kind === undefined) return false;\n  return CONCURRENCY_SAFE_KINDS.has(kind);』（match=exact count=1 sha256=6ab24d276950 L1535-1536）で判定し、partitionByConcurrencySafety が連続する safe な呼び出しを 1 つの並列バッチにする（1552〜1582 行、目視）。 finder が「照合していない」とした呼び出し側（coreToolScheduler.ts）を tool で exact 照合し、notes と usage_ja を書き換えた。

### OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — security_risk の付与

<a id="g-c07-ide-agents-18"></a>
#### C07-18 OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — security_risk の付与

- **資料**: openhands-sdk/openhands/sdk/tool/tool.py: _get_tool_schema（SDK のソースコード）
- **URL**: https://github.com/OpenHands/software-agent-sdk/blob/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/tool/tool.py#L717-L722
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/OpenHands/software-agent-sdk/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/tool/tool.py
- **版**: commit bec71283c15b8e4fce5a20e4758115725d938c59（OpenHands/software-agent-sdk の 2026-10-02 時点の HEAD）
- **書いてある場所**: L717-722（tool の報告は L717-724。開始行は一致、終了行の数え方が違う。引用は L717-722 の行そのもの）
- **原文**:

```
        # Apply security risk enhancement if enabled
        add_security_risk_prediction = add_security_risk_prediction and (
            self.annotations is None or (not self.annotations.readOnlyHint)
        )
        if add_security_risk_prediction:
            action_type = create_action_type_with_risk(action_type)
```

- **日本語**: セキュリティリスク予測を付ける設定のとき、annotations が無いか readOnlyHint が true でないツールにだけ security_risk 欄を足す。
- **どう使っているか**: readOnlyHint:true のツールは、LLM に「この呼び出しのリスク」を答えさせる欄（security_risk）を付けない。注釈なしのツールには付ける。
- **条件**: Agent は LLM 呼び出しで常に add_security_risk_prediction=True を渡す（agent/agent.py 793 行と 1005 行、match=exact count=2 sha256=6a24d0cf275b L793）ので、readOnlyHint:true でないツールには常に security_risk 欄が付く。ただしその値が使われるのは security analyzer が設定されたときだけ（agent.py 1186〜1187 行『When no security analyzer is configured, ignore any security_risk field』、match=exact count=1 sha256=6a24d0cf275b L1186-1187）。MCP ツール用の同じ判定が openhands-sdk/openhands/sdk/mcp/tool.py 458〜460 行にもある（目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、717-722 行（# a separate lock keeps schema building off the action-type critical section.）（取得 2026-10-02T22:11:58Z、sha256 b810003d596a…）
- **補足**: conditions の「add_security_risk_prediction が有効なとき（セキュリティ解析器の利用時）」は誤り。Agent は常に True で呼ぶ（tool で exact、count=2）。解析器の有無で変わるのは値が使われるかどうか。

### OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — read-only ツールのリスク

<a id="g-c07-ide-agents-19"></a>
#### C07-19 OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — read-only ツールのリスク

- **資料**: openhands-sdk/openhands/sdk/agent/agent.py: _extract_security_risk（SDK のソースコード）
- **URL**: https://github.com/OpenHands/software-agent-sdk/blob/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/agent/agent.py#L1182-L1184
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/OpenHands/software-agent-sdk/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/agent/agent.py
- **版**: commit bec71283c15b8e4fce5a20e4758115725d938c59（OpenHands/software-agent-sdk の 2026-10-02 時点の HEAD）
- **書いてある場所**: L1182-1184 (# SystemPromptEvent must appear within this prefix (at index 0 or 1).)
- **原文**:

```
        # Tool is marked as read-only so security risk can be ignored
        if read_only_tool:
            return risk.SecurityRisk.UNKNOWN
```

- **日本語**: read-only と印のあるツールは、セキュリティリスクを無視して UNKNOWN を返す。
- **どう使っているか**: readOnlyHint:true のツールは LLM のリスク申告を読まず、行動のリスクは UNKNOWN になる（呼び出し元は 1380〜1384 行で tool.annotations.readOnlyHint を渡す）。これは自動承認ではない。SDK の既定の confirmation policy は NeverConfirm（conversation/state.py 123 行）で、既定では注釈に関係なく全部確認なしで走る。利用者が ConfirmRisky と LLMSecurityAnalyzer（action.security_risk をそのまま返す）を設定した場合、confirm_unknown の既定 True により read-only ツールは UNKNOWN として確認対象になり、LLM が LOW と申告した非 read-only ツールより確認されやすい。confirm_unknown=False にすると readOnlyHint:true のツールは確認なしで走る。
- **条件**: 確認するかどうかは会話の confirmation policy（NeverConfirm / AlwaysConfirm / ConfirmRisky）と state.security_analyzer による。確認判定は state.security_analyzer.analyze_pending_actions のリスクを使い、解析器が無ければ全部 UNKNOWN（agent.py 1152〜1162 行、match=exact count=1 sha256=6a24d0cf275b L1152-1153）。LLMSecurityAnalyzer は『return action.security_risk』（security/llm_analyzer.py 29 行、match=exact count=1 sha256=c1bed53498f3 L29）。他の解析器が独自に評価する場合は不明。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 危険度を付ける・その他
- **確かさ**: [確認] 再照合 exact・1 か所、1182-1184 行（# SystemPromptEvent must appear within this prefix (at index 0 or 1).）（取得 2026-10-02T22:11:39Z、sha256 6a24d0cf275b…）
- **補足**: 補助照合（検証者）: conversation/state.py の『    confirmation_policy: ConfirmationPolicyBase = NeverConfirm()』は https://raw.githubusercontent.com/OpenHands/software-agent-sdk/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/conversation/state.py の L123 で match=exact count=1 sha256=7e488ee6cb48（2026-10-02T17:21:39Z）。confirmation_policy.py の『class ConfirmRisky(ConfirmationPolicyBase):\n    threshold: SecurityRisk = SecurityRisk.HIGH\n    confirm_unknown: bool = True』は match=exact count=1 sha256=6ecac839fa37 L43-45（finder の照合を再現）。 finder が「不明」とした SDK の既定 policy を確かめた: NeverConfirm（state.py L123、tool で exact）。既定では注釈は確認の有無に影響しない。また確認判定は解析器経由（LLMSecurityAnalyzer は LLM 申告をそのまま返す）なので、UNKNOWN になるのはこの解析器のときと明記し、confirm_unknown の値で結果が逆になることを足した。

### OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — MCP 注釈の取り込み

<a id="g-c07-ide-agents-20"></a>
#### C07-20 OpenHands (All Hands AI) — OpenHands Software Agent SDK（OpenHands/software-agent-sdk） — MCP 注釈の取り込み

- **資料**: openhands-sdk/openhands/sdk/mcp/tool.py: MCPToolDefinition.create（SDK のソースコード）
- **URL**: https://github.com/OpenHands/software-agent-sdk/blob/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/mcp/tool.py#L392-L398
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/OpenHands/software-agent-sdk/bec71283c15b8e4fce5a20e4758115725d938c59/openhands-sdk/openhands/sdk/mcp/tool.py
- **版**: commit bec71283c15b8e4fce5a20e4758115725d938c59（OpenHands/software-agent-sdk の 2026-10-02 時点の HEAD）
- **書いてある場所**: L392-398 (# calls can validate concurrently through the parallel tool executor.)
- **原文**:

```
            annotations = (
                ToolAnnotations.model_validate(
                    mcp_tool.annotations.model_dump(exclude_none=True, by_alias=True)
                )
                if mcp_tool.annotations
                else None
            )
```

- **日本語**: MCP ツールに annotations があれば SDK の ToolAnnotations に写し、無ければ None にする。
- **どう使っているか**: MCP サーバーの宣言を SDK のツール定義にそのまま持ち込む（C07_ide_agents-18・19 の判定の入力になる）。SDK 側の ToolAnnotations の既定値は readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=True（tool.py 229〜247 行、目視）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、392-398 行（# calls can validate concurrently through the parallel tool executor.）（取得 2026-10-02T22:11:32Z、sha256 44a93746b9bb…）
- **補足**: OpenHands 本体の Web アプリ（OpenHands/OpenHands @ a8c8fb3）では、自前のクライアントツール定義に注釈を書く箇所と test しか見つからず、MCP 注釈を判断に使う箇所は見つからなかった（checked_no_mention）。

### Cognition (Devin / 旧 Windsurf) — Devin CLI

<a id="g-c07-ide-agents-21"></a>
#### C07-21 Cognition (Devin / 旧 Windsurf) — Devin CLI

- **資料**: Devin CLI Changelog (Stable) — v3000.3.22 (July 29, 2026) > Changed（リリースノート）
- **URL**: https://docs.devin.ai/cli/changelog/stable
- **書いてある見出しへ直接**: https://docs.devin.ai/cli/changelog/stable#changed-8
- **版**: v3000.3.22（July 29, 2026）
- **書いてある場所**: Changelog (Stable) > Changed (#changed-8)
- **原文**:

> Plan mode now allows read-only MCP tools (those annotated `readOnlyHint: true`) plus listing MCP servers, tools, and resources, so the agent can gather context while planning.

- **日本語**: Plan モードで、read-only の MCP ツール（readOnlyHint: true と注釈されたもの）と、MCP サーバー・ツール・リソースの一覧取得を使えるようにした。計画中に文脈を集めるため。
- **どう使っているか**: Devin CLI の Plan モードは、宣言 readOnlyHint:true の MCP ツールだけを許可する（それ以外の MCP ツールは使えない）。Plan モードでの確認の要否はこの文からは分からない。
- **条件**: Plan モードのとき。後の v3000.4.16（August 10, 2026）の changelog に『Plan mode now uses the normal permission system, and “always allow” choices appear only when they can take effect.』（match=exact count=1 sha256=c1c718ca59a7 Changelog (Stable) > Changed、#changed-7）とあり、その後も readOnlyHint:true の MCP ツールだけに絞る挙動が続いているかは不明。Devin のドキュメント全体（docs.devin.ai/llms-full.txt）で readOnlyHint が出るのはこの changelog の 1 か所だけ（検証者の grep）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Changelog (Stable) > Changed」（取得 2026-10-02T22:11:27Z、sha256 d55262050313…）
- **補足**: Devin CLI の permissions ページ（docs.devin.ai/cli/reference/permissions）と Windsurf/Devin Desktop の Cascade MCP ページには注釈の記述なし（checked_no_mention）。docs.windsurf.com は docs.devin.ai にリダイレクトされる。 conditions の v3000.4.16 の文を tool で exact 照合して引用を正確にし、llms-full.txt 全体でも readOnlyHint は changelog だけであることを足した。版（v3000.3.22, July 29, 2026）は本文の版見出しの並びで確認。

### Cursor (Anysphere) — Cursor Origin MCP サーバー（Cursor 自身が出す MCP サーバー）

<a id="g-c07-ide-agents-22"></a>
#### C07-22 Cursor (Anysphere) — Cursor Origin MCP サーバー（Cursor 自身が出す MCP サーバー）

- **資料**: Origin MCP > Confirmation（cursor.com/docs/api/origin/mcp）（サーバの文書）
- **URL**: https://cursor.com/docs/api/origin/mcp
- **書いてある見出しへ直接**: https://cursor.com/docs/api/origin/mcp#confirmation
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Origin MCP > Confirmation (#confirmation)
- **原文**:

> Tools that are destructive or hard to undo, such as merging a pull request or dismissing a review, set `_meta["cursor/requiresConfirmation"]: true` in `tools/list`. Cursor clients show an approval prompt before every call to such a tool. Other MCP clients can use the same flag, or the standard `destructiveHint` annotation, to decide when to ask the user.

- **日本語**: 破壊的または元に戻しにくいツール（PR のマージ、レビューの却下など）は tools/list で _meta["cursor/requiresConfirmation"]: true を付ける。Cursor のクライアントはそのツールを呼ぶたびに承認を求める。他の MCP クライアントは同じ印か、標準の destructiveHint 注釈を使って、いつユーザーに聞くかを決めてよい。
- **どう使っているか**: Cursor 自身のサーバー（Origin MCP）の文書が、Cursor のクライアントは Cursor 独自の _meta["cursor/requiresConfirmation"] が付いたツールで毎回承認を出す、と書く。destructiveHint は「他の MCP クライアント」が確認の要否を決めるのに使える選択肢として挙げるだけ。Cursor のクライアントが destructiveHint を見るかどうかは、この文からは分からない（不明）。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 loose・2 か所、見出し「Origin MCP > Confirmation」（取得 2026-10-02T22:11:23Z、sha256 590063d851fc…）
- **補足**: Cursor 本体の MCP 文書（cursor.com/docs/mcp）は「既定で MCP ツールの使用前に承認を求める」「ツール許可リスト」を書くが、注釈には触れない（checked_no_mention）。WebSearch では「Cursor の Ask モードは readOnlyHint のツールだけ呼べる」とする第三者の issue（realloon/RimSage #9）があったが、Cursor の一次資料では確認できなかった（未確認）。 usage_ja の「標準の destructiveHint ではなく…決めている」は過大（文書は Cursor が destructiveHint を使わないとは書いていない）なので直し、usage から require_confirmation を外した（destructiveHint による確認は他クライアント向けの提案で、Cursor の挙動ではない）。このページに readOnlyHint は無い（tool で none）。

### Cursor (Anysphere) — Cursor TypeScript SDK（local.customTools）

<a id="g-c07-ide-agents-23"></a>
#### C07-23 Cursor (Anysphere) — Cursor TypeScript SDK（local.customTools）

- **資料**: Cursor TypeScript SDK > Custom tools > Tool definition（SDK の文書）
- **URL**: https://cursor.com/docs/sdk/typescript
- **書いてある見出しへ直接**: https://cursor.com/docs/sdk/typescript#tool-definition
- **版**: 2026-10-02 取得（SDK 1.0.31 以降）
- **書いてある場所**: Cursor TypeScript SDK > Custom tools > Tool definition (#tool-definition)
- **原文**:

> MCP tool annotations (`title`, `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) passed through to the model. Descriptive hints only; nothing in the SDK enforces them.

- **日本語**: MCP ツール注釈（title, readOnlyHint, destructiveHint, idempotentHint, openWorldHint）はモデルにそのまま渡す。説明のための hint だけで、SDK はそれを強制しない。
- **どう使っているか**: Cursor SDK は自作ツール（local.customTools）の注釈をモデルに渡すが、「記述的なヒントにすぎず、SDK の中では何も強制しない」と明言する。
- **条件**: TypeScript の local agent の customTools のみ。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる・使わない・読まない
- **確かさ**: [確認] 再照合 loose・2 か所、見出し「Cursor TypeScript SDK > Custom tools > Tool definition」（取得 2026-10-02T22:11:23Z、sha256 e125de7a4f90…）
- **補足**: usage_ja を原文（Descriptive hints only; nothing in the SDK enforces them）に合わせて直訳寄りにした（「承認・制限には使わない」は原文より具体的すぎる）。

### Cursor (Anysphere) — Cursor SDK（changelog）

<a id="g-c07-ide-agents-24"></a>
#### C07-24 Cursor (Anysphere) — Cursor SDK（changelog）

- **資料**: SDK Changelog > 1.0.31（リリースノート）
- **URL**: https://cursor.com/docs/sdk/changelog
- **書いてある見出しへ直接**: https://cursor.com/docs/sdk/changelog#sep-3-2026
- **版**: SDK 1.0.31
- **書いてある場所**: SDK Changelog > 1.0.31 (#sep-3-2026)
- **原文**:

> `annotations` on a `local.customTools` entry passes MCP tool annotations (`title`, `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) through to the model. They are descriptive hints only; the SDK does not enforce them.

- **日本語**: local.customTools の項目に annotations を書くと、MCP ツール注釈をモデルに渡す。説明のための hint だけで、SDK は強制しない。
- **どう使っているか**: C07_ide_agents-23 と同じ内容（注釈はモデルに渡すだけの記述的なヒントで、SDK は強制しない）を、機能追加時の changelog でも明言している。
- **条件**: TypeScript のみ（同じ changelog 項目の続きの文）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる・使わない・読まない
- **確かさ**: [確認] 再照合 loose・2 か所、見出し「SDK Changelog > 1.0.31」（取得 2026-10-02T22:11:24Z、sha256 c6fbdb7d6691…）
- **補足**: 23 に合わせて usage_ja を直訳寄りにした。

### Cline Bot Inc. — Cline SDK（ClineCore / CLI。sdk/packages/core）

<a id="g-c07-ide-agents-25"></a>
#### C07-25 Cline Bot Inc. — Cline SDK（ClineCore / CLI。sdk/packages/core）

- **資料**: sdk/packages/core/src/extensions/mcp/client.ts: listTools（クライアントのソースコード）
- **URL**: https://github.com/cline/cline/blob/c269dbb7f97256d53d4aedabb6c245b9ec54b1b6/sdk/packages/core/src/extensions/mcp/client.ts#L765-L774
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cline/cline/c269dbb7f97256d53d4aedabb6c245b9ec54b1b6/sdk/packages/core/src/extensions/mcp/client.ts
- **版**: commit c269dbb7f97256d53d4aedabb6c245b9ec54b1b6（cline/cline の 2026-10-02 時点の HEAD）
- **書いてある場所**: L765-774
- **原文**:

```
			return result.tools.map((tool) => ({
				name: tool.name,
				description: tool.description,
				inputSchema:
					tool.inputSchema &&
					typeof tool.inputSchema === "object" &&
					!Array.isArray(tool.inputSchema)
						? tool.inputSchema
						: {},
			}));
```

- **日本語**: tools/list の結果から name・description・inputSchema だけを取り出して返す。
- **どう使っているか**: Cline の新しい SDK 系（CLI・ClineCore）では MCP の annotations はツール記述子に写されず捨てられる（McpToolDescriptor 型にも annotations が無い: types.ts 3〜7 行、目視）。承認は toolPolicies（名前ごとの autoApprove）で決まり、未指定は「有効かつ自動承認」（docs.cline.bot の Permission Handling）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、765-774 行（取得 2026-10-02T22:11:32Z、sha256 4d8919d49000…）
- **補足**: 同ファイル 352〜378 行のもう一つの listTools 実装も同じく 3 項目だけを写す（目視、検証者も確認）。未指定のツールの既定は検証者が照合: https://docs.cline.bot/sdk/guides/permission-handling.md の『Tool names not listed in `toolPolicies` default to enabled and auto-approved, so set policies explicitly for tools that need review.』（match=exact count=1 sha256=13a16d05c6bc L9。公開 HTML https://docs.cline.bot/sdk/guides/permission-handling でも loose）。GitHub code search でも cline/cline に readOnlyHint は 0 件。 usage_ja が根拠にしていた docs.cline.bot の文（未指定は有効かつ自動承認）を tool で照合し、notes に引用と場所を足した。

### Cline Bot Inc. — Cline VS Code 拡張（apps/vscode）

<a id="g-c07-ide-agents-26"></a>
#### C07-26 Cline Bot Inc. — Cline VS Code 拡張（apps/vscode）

- **資料**: apps/vscode/src/services/mcp/McpHub.ts: fetchToolsList（クライアントのソースコード）
- **URL**: https://github.com/cline/cline/blob/c269dbb7f97256d53d4aedabb6c245b9ec54b1b6/apps/vscode/src/services/mcp/McpHub.ts#L888-L898
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cline/cline/c269dbb7f97256d53d4aedabb6c245b9ec54b1b6/apps/vscode/src/services/mcp/McpHub.ts
- **版**: commit c269dbb7f97256d53d4aedabb6c245b9ec54b1b6（cline/cline の 2026-10-02 時点の HEAD）
- **書いてある場所**: L888-898
- **原文**:

```
			// Get autoApprove settings
			const settingsPath = await getMcpSettingsFilePathHelper(await this.getSettingsDirectoryPath())
			const content = await fs.readFile(settingsPath, "utf-8")
			const config = JSON.parse(content)
			const autoApproveConfig = config.mcpServers[serverName]?.autoApprove || []

			// Mark tools as always allowed based on settings
			const tools = (response?.tools || []).map((tool) => ({
				...tool,
				autoApprove: autoApproveConfig.includes(tool.name),
			}))
```

- **日本語**: 設定ファイルの mcpServers[サーバー名].autoApprove（ツール名の配列）を読み、ツール名がそこに含まれるかで「常に許可」を付ける。
- **どう使っているか**: Cline の VS Code 拡張では、MCP ツールの自動承認は利用者が設定したツール名の一覧だけで決まり、注釈は使われない（tool オブジェクトは ...tool で注釈を含んだまま保持されるが、McpTool 型（shared/mcp.ts）に annotations 欄は無く、判断に使う箇所も無い）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、888-898 行（取得 2026-10-02T22:11:32Z、sha256 4c7163cb4ae2…）
- **補足**: リポジトリ全体（c269dbb）で readOnlyHint / destructiveHint などの語は 0 件（ローカル grep）。文書（docs.cline.bot）も注釈に触れない。

### Roo Code Inc. — Roo Code（VS Code 拡張）

<a id="g-c07-ide-agents-27"></a>
#### C07-27 Roo Code Inc. — Roo Code（VS Code 拡張）

- **資料**: src/services/mcp/McpHub.ts: fetchToolsList（クライアントのソースコード）
- **URL**: https://github.com/RooCodeInc/Roo-Code/blob/b867ec9145750d0ae1ff7f02d35406e9bf2a0b16/src/services/mcp/McpHub.ts#L1023-L1031
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/RooCodeInc/Roo-Code/b867ec9145750d0ae1ff7f02d35406e9bf2a0b16/src/services/mcp/McpHub.ts
- **版**: commit b867ec9145750d0ae1ff7f02d35406e9bf2a0b16（RooCodeInc/Roo-Code の 2026-10-02 時点の HEAD）
- **書いてある場所**: L1023-1031
- **原文**:

```
			// Check if wildcard "*" is in the alwaysAllow config
			const hasWildcard = alwaysAllowConfig.includes("*")

			// Mark tools as always allowed and enabled for prompt based on settings
			const tools = (response?.tools || []).map((tool) => ({
				...tool,
				alwaysAllow: hasWildcard || alwaysAllowConfig.includes(tool.name),
				enabledForPrompt: !disabledToolsList.includes(tool.name),
			}))
```

- **日本語**: alwaysAllow 設定に "*" があるか、ツール名が含まれていれば「常に許可」。プロンプトに出すかは無効化リストで決める。
- **どう使っているか**: Roo Code の自動承認はツール名（またはワイルドカード）の一覧だけで決まり、注釈は使われない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、1023-1031 行（取得 2026-10-02T22:11:31Z、sha256 322dfa749a97…）
- **補足**: src / packages/types / webview-ui の .ts/.tsx 1230 ファイル（b867ec9）を grep して readOnlyHint などの語は 0 件。

### Kilo Code — Kilo Code（packages/opencode。OpenCode 派生）

<a id="g-c07-ide-agents-28"></a>
#### C07-28 Kilo Code — Kilo Code（packages/opencode。OpenCode 派生）

- **資料**: packages/opencode/src/mcp/catalog.ts: convertTool（クライアントのソースコード）
- **URL**: https://github.com/Kilo-Org/kilocode/blob/78f82b976a0b81201d85df9d4934e4d20d9a4617/packages/opencode/src/mcp/catalog.ts#L50-L52
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Kilo-Org/kilocode/78f82b976a0b81201d85df9d4934e4d20d9a4617/packages/opencode/src/mcp/catalog.ts
- **版**: commit 78f82b976a0b81201d85df9d4934e4d20d9a4617（Kilo-Org/kilocode の 2026-10-02 時点の HEAD）
- **書いてある場所**: L50-52
- **原文**:

```
  return dynamicTool({
    description: mcpTool.description ?? "",
    inputSchema: jsonSchema(inputSchema),
```

- **日本語**: MCP ツールをモデル用ツールに変換するとき、description と inputSchema だけを使う。
- **どう使っているか**: Kilo Code（OpenCode 由来のコア）は MCP 注釈をツールに写さない。権限はツール名パターンの permission 設定で決まる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、50-52 行（取得 2026-10-02T22:11:31Z、sha256 90183d03bb2c…）
- **補足**: Kilo-Org/kilocode @ 78f82b9 の .ts/.tsx/.go/.py 5855 ファイルを grep して readOnlyHint などの語は 0 件。kilo.ai の MCP 文書にも記述なし。

### Anomaly (SST) — OpenCode（anomalyco/opencode、旧 sst/opencode）

<a id="g-c07-ide-agents-29"></a>
#### C07-29 Anomaly (SST) — OpenCode（anomalyco/opencode、旧 sst/opencode）

- **資料**: packages/opencode/src/mcp/catalog.ts: convertTool（クライアントのソースコード）
- **URL**: https://github.com/anomalyco/opencode/blob/1ddb0873aee50d209d1a8d7f91b89c5daf692d49/packages/opencode/src/mcp/catalog.ts#L50-L52
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anomalyco/opencode/1ddb0873aee50d209d1a8d7f91b89c5daf692d49/packages/opencode/src/mcp/catalog.ts
- **版**: commit 1ddb0873aee50d209d1a8d7f91b89c5daf692d49（anomalyco/opencode の 2026-10-02 時点の HEAD）
- **書いてある場所**: L50-52
- **原文**:

```
  return dynamicTool({
    description: mcpTool.description ?? "",
    inputSchema: jsonSchema(inputSchema),
```

- **日本語**: MCP ツールをモデル用ツールに変換するとき、description と inputSchema だけを使う。
- **どう使っているか**: OpenCode は MCP 注釈をツールに写さず、承認判断にも使わない（permissions はツール名のパターンで allow / ask / deny）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、50-52 行（取得 2026-10-02T22:11:40Z、sha256 1123ce304cd6…）
- **補足**: sparse 取得した 3122 ファイル中 3077 ファイル（ディスク不足で一部欠落）を grep して readOnlyHint などの語は 0 件。opencode.ai の mcp-servers / permissions ページにも記述なし。

### Continue Dev, Inc. — Continue（VS Code / JetBrains 拡張）

<a id="g-c07-ide-agents-30"></a>
#### C07-30 Continue Dev, Inc. — Continue（VS Code / JetBrains 拡張）

- **資料**: core/config/profile/doLoadConfig.ts: MCP ツールの組み立て（クライアントのソースコード）
- **URL**: https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/profile/doLoadConfig.ts#L213-L226
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/continuedev/continue/5522c6f44ca0ac3528b37244818fbfa39b5af470/core/config/profile/doLoadConfig.ts
- **版**: commit 5522c6f44ca0ac3528b37244818fbfa39b5af470（continuedev/continue の 2026-10-02 時点の HEAD）
- **書いてある場所**: L213-226
- **原文**:

```
      const serverTools: Tool[] = server.tools.map((tool) => ({
        displayTitle: server.name + " " + tool.name,
        function: {
          description: tool.description,
          name: getMCPToolName(server, tool),
          parameters: tool.inputSchema,
        },
        faviconUrl: server.faviconUrl,
        readonly: false,
        type: "function" as const,
        uri: encodeMCPToolUri(server.id, tool.name),
        group: server.name,
        originalFunctionName: tool.name,
        mcpMeta: tool._meta,
```

- **日本語**: 接続済み MCP サーバーのツールを Continue のツールに変換するとき、readonly を一律 false にする（説明・パラメータ・_meta は写すが annotations は写さない）。
- **どう使っているか**: Continue は MCP ツールを宣言に関係なくすべて「読み取り専用でない」として扱う。readOnlyHint:true も使われない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、213-226 行（取得 2026-10-02T22:12:00Z、sha256 017c5c42cdb8…）
- **補足**: Continue の readonly は組み込みツールの自動承認（streamNormalInput.ts 336〜340 行）と Plan モードの絞り込み（C07_ide_agents-31）に使われるが、どちらも組み込みグループに限られる。

### Continue Dev, Inc. — Continue — Plan モードのツール選択

<a id="g-c07-ide-agents-31"></a>
#### C07-31 Continue Dev, Inc. — Continue — Plan モードのツール選択

- **資料**: gui/src/redux/selectors/selectActiveTools.ts（クライアントのソースコード）
- **URL**: https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/selectors/selectActiveTools.ts#L27-L31
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/continuedev/continue/5522c6f44ca0ac3528b37244818fbfa39b5af470/gui/src/redux/selectors/selectActiveTools.ts
- **版**: commit 5522c6f44ca0ac3528b37244818fbfa39b5af470（continuedev/continue の 2026-10-02 時点の HEAD）
- **書いてある場所**: L27-31
- **原文**:

```
      if (mode === "plan") {
        return enabledTools.filter(
          (t) => t.group !== BUILT_IN_GROUP_NAME || t.readonly,
        );
      }
```

- **日本語**: Plan モードでは、組み込みグループのツールは readonly のものだけ残し、組み込み以外（MCP など）のツールはそのまま残す。
- **どう使っているか**: Continue の Plan モードは MCP ツールを読み取り専用かどうかで絞らない（注釈も readonly も見ない）ので、書き込み系の MCP ツールも Plan モードで使える。
- **条件**: mode === "plan" のとき。ツールごとの policy が disabled のものは別途除外。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 exact・1 か所、27-31 行（取得 2026-10-02T22:11:30Z、sha256 80c9f3994a8a…）

### LibreChat — LibreChat（packages/api の MCP）

<a id="g-c07-ide-agents-32"></a>
#### C07-32 LibreChat — LibreChat（packages/api の MCP）

- **資料**: packages/api/src/mcp/tools.ts: MCPToolInput / formatMCPServerTools（クライアントのソースコード）
- **URL**: https://github.com/danny-avila/LibreChat/blob/f10b1d91f1eee3a2c82d5247bf620351486b7c1b/packages/api/src/mcp/tools.ts#L15
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/danny-avila/LibreChat/f10b1d91f1eee3a2c82d5247bf620351486b7c1b/packages/api/src/mcp/tools.ts
- **版**: commit f10b1d91f1eee3a2c82d5247bf620351486b7c1b（danny-avila/LibreChat の 2026-10-02 時点の HEAD）
- **書いてある場所**: L15
- **原文**:

> export type MCPToolInput = Pick<Tool, 'name' | 'description'> & Partial<Pick<Tool, 'inputSchema'>>;

- **日本語**: MCP ツールの入力型は name・description・inputSchema だけを取り出したもの。
- **どう使っているか**: LibreChat は MCP ツールを LLM の関数定義に変換する段階で annotations を持たない型にし、使わない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、15 行（取得 2026-10-02T22:12:56Z、sha256 832c727e2897…）
- **補足**: MCP 関係の 300 ファイル（f10b1d9）を grep して readOnlyHint などの語は 0 件。www.librechat.ai/docs/features/mcp にも記述なし。

### Open WebUI — Open WebUI（backend の MCP クライアント）

<a id="g-c07-ide-agents-33"></a>
#### C07-33 Open WebUI — Open WebUI（backend の MCP クライアント）

- **資料**: backend/open_webui/utils/mcp/client.py: list_tool_specs（クライアントのソースコード）
- **URL**: https://github.com/open-webui/open-webui/blob/8bd8b4fac5e059578ac0c74b3c18d11139f88b7d/backend/open_webui/utils/mcp/client.py#L102-L111
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/open-webui/open-webui/8bd8b4fac5e059578ac0c74b3c18d11139f88b7d/backend/open_webui/utils/mcp/client.py
- **版**: commit 8bd8b4fac5e059578ac0c74b3c18d11139f88b7d（open-webui/open-webui の 2026-10-02 時点の HEAD）
- **書いてある場所**: L102-111
- **原文**:

```
        for tool in tools:
            name = tool.name
            description = tool.description

            inputSchema = tool.inputSchema

            # TODO: handle outputSchema if needed
            outputSchema = getattr(tool, 'outputSchema', None)

            tool_specs.append({'name': name, 'description': description, 'parameters': inputSchema})
```

- **日本語**: 各ツールの name・description・inputSchema（parameters として）だけを tool_specs に入れる。outputSchema は TODO。
- **どう使っているか**: Open WebUI は MCP 注釈を tool spec に写さず、使わない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、102-111 行（取得 2026-10-02T22:11:36Z、sha256 f46c5e7e01cf…）
- **補足**: backend の mcp / tools / middleware 系 9 ファイル（8bd8b4f）を grep してツール注釈の語は 0 件（"annotations" はチャット応答の URL 注釈や from __future__ だけ）。

### Warp — Warp（ターミナルの Agent Mode）

<a id="g-c07-ide-agents-34"></a>
#### C07-34 Warp — Warp（ターミナルの Agent Mode）

- **資料**: app/src/ai/blocklist/permissions.rs: can_use_mcp_server（クライアントのソースコード）
- **URL**: https://github.com/warpdotdev/warp/blob/38b2c55e4ed2cd9a19fc66e13e323d976446ca40/app/src/ai/blocklist/permissions.rs#L863-L874
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/warpdotdev/warp/38b2c55e4ed2cd9a19fc66e13e323d976446ca40/app/src/ai/blocklist/permissions.rs
- **版**: commit 38b2c55e4ed2cd9a19fc66e13e323d976446ca40（warpdotdev/warp の 2026-10-02 時点の HEAD）
- **書いてある場所**: L863-874
- **原文**:

```
        let allowlisted = uuid_of_mcp_server
            .is_some_and(|uid| self.get_mcp_allowlist(ctx, terminal_view_id).contains(&uid));
        let denylisted = uuid_of_mcp_server
            .is_some_and(|uid| self.get_mcp_denylist(ctx, terminal_view_id).contains(&uid));

        match self.get_mcp_permissions_setting(ctx, terminal_view_id) {
            ActionPermission::AgentDecides | ActionPermission::Unknown => {
                allowlisted && !denylisted
            }
            ActionPermission::AlwaysAllow => !denylisted,
            ActionPermission::AlwaysAsk => allowlisted && !denylisted,
        }
```

- **日本語**: MCP サーバーが許可リストにあり拒否リストに無いか、と MCP 権限設定（Agent が決める／常に許可／常に確認）の組み合わせで、自動実行してよいかを決める。
- **どう使っているか**: Warp の MCP ツール自動実行はサーバー単位の allowlist / denylist と設定だけで決まり、ツールの注釈は使わない。「Agent decides」でも allowlist にないサーバーは自動実行しない。
- **条件**: 会話が「すべて自動実行」なら常に true（856〜861 行）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、863-874 行（取得 2026-10-02T22:11:35Z、sha256 db25b586d34e…）
- **補足**: MCP・権限関係の Rust 91 ファイル（38b2c55）を grep して read_only_hint などの語は 0 件。docs.warp.dev の MCP ページにも記述なし。

### Anthropic — Claude Code（CLI）2.1.287 — MCP ツールの包み（実装）

<a id="g-g2-closed-clients-missing-01"></a>
#### G2CCM-01 Anthropic — Claude Code（CLI）2.1.287 — MCP ツールの包み（実装）

- **資料**: Claude Code ネイティブバイナリ内の JS バンドル（MCP ツール定義を Tool に包む部分）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: @anthropic-ai/claude-code-linux-x64 2.1.287（npm latest, 2026-10-02）
- **書いてある場所**: ファイル内の改行で区切った 1437179 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> isConcurrencySafe(){return X.mayOverlap||(U.annotations?.readOnlyHint??!1)},isReadOnly(){return U.annotations?.readOnlyHint??!1},readOnlyHint:U.annotations?.readOnlyHint

- **日本語**: MCP ツールの「並列に走らせてよいか」と「読み取り専用か」は annotations.readOnlyHint で決める。readOnlyHint が無いときは false（読み取り専用ではない・並列化しない）。
- **どう使っているか**: readOnlyHint を内部の isReadOnly / isConcurrencySafe にそのまま写す。欠落は false（安全側）。宣言の真偽は確かめない。
- **条件**: すべての MCP ツール（サーバーの種類によらない）。mayOverlap は別の内部フラグで、立っていれば readOnlyHint に関係なく並列可。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 同じ形の定義がバンドル内に 2 か所ある（変数名 U/X と v/ae。別の実行経路用と思われるが、どちらが対話 CLI かは不明）。C04_anthropic-13/14（SDK 文書の「read-only の MCP ツールは並列に走る」）をバイナリで裏づける。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 検証者の追記: 同じバイナリで readOnlyHint を読む所はほかに、(a) 利用統計のイベントに readOnlyHint を載せる所（`...e.readOnlyHint!==void 0&&{readOnlyHint:e.readOnlyHint}`、目視）、(b) 組み込みの管理コネクタ（github / microsoft365）の BUILTIN_DEFAULT_TOOL_POLICY に対して「ポリシーで覆われていないツール」を数える関数 g$ が readOnlyHint===true のツールを数えない所（目視。その結果の使い道は不明）、(c) 組み込みの Claude Design 用クライアント（02 の検証者メモ）がある。mayOverlap は $tn(e,U.name,ye) で決まる値で、中身は調べていない。 notes に、同じバイナリ内のほかの readOnlyHint の読み取り（利用統計・管理コネクタのポリシー網羅チェック・Claude Design）を追記した。用途の主張は変えていない。

<a id="g-g2-closed-clients-missing-02"></a>
#### G2CCM-02 Anthropic — Claude Code（CLI）2.1.287 — MCP ツールの包み（実装）

- **資料**: 同上（isDestructive / isOpenWorld）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1437179 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> isDestructive(){return U.annotations?.destructiveHint??!1},isOpenWorld(){return U.annotations?.openWorldHint??!1}

- **日本語**: destructiveHint と openWorldHint も内部の isDestructive / isOpenWorld に写す。どちらも欠落は false。
- **どう使っているか**: destructiveHint・openWorldHint の欠落を false（破壊的でない・閉じた世界）として扱う。仕様の既定（destructiveHint 既定 true、openWorldHint 既定 true）とは逆。その結果、auto mode では destructiveHint を宣言しないツールが「破壊的でない」側に入り、MCP サーバーポリシーの ask ルールが確認として強制されなくなる（34）。
- **条件**: isDestructive は少なくとも次で使われる: (1) auto mode で、MCP サーバーポリシー（source mcpServerPolicy）の ask ルールで確認になった呼び出しを、確認のまま止めるか auto mode の判定へ進めるか（機能フラグなしの既定経路。G2_closed_clients_missing-34）、(2) 機能フラグつきの経路（08 の cVt / gVo、既定 off）、(3) /mcp の表示・SDK の mcpServerStatus・Claude Code 自身が出す注釈（destructiveHint:true のときだけ載せる）。
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 MCP 仕様では destructiveHint・openWorldHint の既定値は true。Claude Code は欠落を false にするので、宣言の無いツールは「破壊的でない」側に数えられる（どの判断に効くかは 08 を参照）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 検証者の追記: 欠落を false にするのは汎用の MCP ツールの包み（On 関数と、同形の 2 か所目）だけ。同じバイナリの組み込み Claude Design クライアントは、サーバーが返す操作一覧の注釈を 『y=c.annotations?.readOnlyHint??i?.readOnly??!1,v=c.annotations?.destructiveHint??i?.destructive??!0』（verify_quote.py exact、1434042 行目）で読み、destructiveHint の欠落を true（仕様どおり）にし、組み込み表があればより厳しい側に寄せる。 発見者の conditions「isDestructive が効くのは機能フラグつきの経路（08）と表示だけ」は誤り。auto mode の既定経路（機能フラグなし）でも、mcpServerPolicy の ask ルールを確認として強制するかの判定に isDestructive を使う（新規 34 として引用を照合）。欠落 = false なので、宣言の無いツールは確認が外れる側に入る。conditions・usage_ja を直し、Claude Design クライアントは欠落を true にすることを notes に足した。

### Anthropic — Claude Code（CLI）2.1.287 — plan mode の許可判定（実装）

<a id="g-g2-closed-clients-missing-03"></a>
#### G2CCM-03 Anthropic — Claude Code（CLI）2.1.287 — plan mode の許可判定（実装）

- **資料**: 同バイナリ内の許可判定関数（plan mode の MCP ツール）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1407060 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> pe(r).mode==="plan"&&FVo(e,r)&&!e.isReadOnly(Fe)&&j.behavior==="passthrough"&&!nle(lm(e),Fe))j={behavior:"ask",message:`Cannot call ${e.name} while in plan mode.`,decisionReason:{type:"mode",mode:"plan"}}

- **日本語**: plan mode で、MCP ツール（FVo は mcpInfo があれば真）の isReadOnly が偽、かつツール自身の確認が passthrough なら、「plan mode 中は X を呼べません」という ask（確認）に変える。
- **どう使っているか**: plan mode では readOnlyHint が true でない MCP ツール（欠落・false）を、ツール自身の判定が passthrough なら「plan mode 中は呼べない」という確認（ask）に変える。readOnlyHint:true のツールにはこの確認は付かず、通常の許可の流れ（allow ルール、無ければ通常の確認）に進む。この関数の中に注釈だけで自動承認する分岐は無い。ただし auto mode が有効な状態の plan（Aa("plan") が真）では、通常の確認は auto mode の判定（分類器など）に回るので、readOnlyHint:true のツールは確認なしで走りうる。readOnlyHint の無いツールは auto mode でも plan_mode_floor として確認に戻る。
- **条件**: plan mode のときだけ。nle() が真の一部の組み込み名は除外。ツール自身の checkPermissions が passthrough 以外（allow/deny/ask）を返したときは適用されない。 auto mode が有効な plan では、この ask は分類器では外れない（fallback 理由 plan_mode_floor）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 補助の照合: 『function FVo(e,n){if(e.mcpInfo)return!0;』も exact（ファイル内の改行で区切った 1407060 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安））。C04_anthropic-32 / 35（issue 78085・johnny-five #36。「plan mode で readOnlyHint の無い MCP ツールが毎回確認になる」）の報告をバイナリで裏づける。issue 自体は github.com が 403 のため引き続き未確認。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 usage_ja の「自動承認にはならない」は言い過ぎ。auto mode が有効な plan（関数 Aa は mode==="auto" か、plan かつ auto が有効のとき真）では、通常の確認が auto mode の判定へ回るため、readOnlyHint:true のツールは確認なしで走りうる。注釈だけで承認する分岐が無いことは正しいので、その形に書き直した。

<a id="g-g2-closed-clients-missing-04"></a>
#### G2CCM-04 Anthropic — Claude Code（CLI）2.1.287 — plan mode の許可判定（実装）

- **資料**: 同関数の後段（allow ルールより前に返る）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1407060 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> if(j?.behavior==="ask"&&(Ce||xe||!Ee&&(qu(j.decisionReason)||j.decisionReason?.type==="sandboxOverride"||CVt(j.decisionReason))))return j;

- **日本語**: 判定が ask で、理由が plan mode（CVt）などなら、その ask をそのまま返す。この行は allow ルール（Fre）を見る行より前にある。
- **どう使っているか**: readOnlyHint が無い MCP ツールは、plan mode では利用者が allow ルールを書いても確認が出る（bypass 系の Ee が真のときを除く）。
- **条件**: Ee（bypassPermissions、または bypass が使える状態の mode）が偽のとき。ツール全体の ask ルール・deny ルールはこれより前に評価される。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 補助の照合: 『function CVt(e){return e?.type==="mode"&&e.mode==="plan"}』も exact。allow ルールを見る Fre(pe(r),e) はこの return の後にある（同じ関数内、目視）。johnny-five #36 の「allow ルールがあっても毎回確認」は、この順序と合う。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Anthropic — Claude Code（CLI）2.1.287 — ツール呼び出しの並列化（実装）

<a id="g-g2-closed-clients-missing-05"></a>
#### G2CCM-05 Anthropic — Claude Code（CLI）2.1.287 — ツール呼び出しの並列化（実装）

- **資料**: 同バイナリ内のツール呼び出しの束ね（partition）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1412159 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> if(S&&r.at(-1)?.isConcurrencySafe)r.at(-1).blocks.push(g);else r.push({isConcurrencySafe:S,blocks:[g]});

- **日本語**: 続けて来たツール呼び出しのうち、isConcurrencySafe が真のものは同じ束に入れて並列に走らせる。偽のものは 1 件ずつ別の束になる。
- **どう使っているか**: MCP ツールでは isConcurrencySafe = readOnlyHint ?? false（01）なので、readOnlyHint:true の宣言が並列実行の条件になる。欠落は順次実行。
- **条件**: 同じ応答の中で連続する呼び出しだけを束ねる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 宣言が嘘（書き込むのに readOnlyHint:true）なら書き込みが並列に走り競合しうる。許可（確認の要否）とは別の効果。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Anthropic — Claude Code（CLI）2.1.287 — plan mode（承認待ちの間に plan mode に入ったとき）

<a id="g-g2-closed-clients-missing-06"></a>
#### G2CCM-06 Anthropic — Claude Code（CLI）2.1.287 — plan mode（承認待ちの間に plan mode に入ったとき）

- **資料**: 同バイナリ内のメッセージ文字列 plan_mode.entered_while_asking（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1431642 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> This session entered plan mode while the approval was pending; a state-changing ${e} call is not approved from plan mode.

- **日本語**: 承認を待っている間にセッションが plan mode に入った。状態を変える呼び出しは plan mode からは承認しない。
- **どう使っているか**: 承認待ちの間に plan mode に入ったとき、e.isReadOnly(入力) が偽なら、その呼び出しを late_refusal（拒否）にする。e が MCP ツールなら isReadOnly = readOnlyHint ?? false（01）なので、readOnlyHint の無い・false のツールは拒否、true なら拒否されない。確認ではなく拒否である。
- **条件**: 承認待ちの最中に plan mode へ切り替わった場合で、さらに `!(U?kn:Fr&&K)` が真のとき（U・kn・Fr・K の意味は未解明）。このコードは ask_id・wire 名・host を扱う、承認を待って順に流す呼び出し経路の中にあり、どの種類のツール呼び出しがこの経路を通るか（MCP ツール全般か、ホスト経由の呼び出しだけか）は不明。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 拒否の条件 `if(!$t)return{kind:"late_refusal",...}`（$t=e.isReadOnly(Mt)）はこの文字列の参照元で目視（道具での照合はメッセージ文字列のみ）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 usage の require_confirmation は誤り（確認ではなく late_refusal＝拒否）。other に変えた。参照元のコード（`if(!(U?kn:Fr&&K)&&pe(a).mode==="plan"){…$t=e.isReadOnly(Mt)…if(!$t)return{kind:"late_refusal",…}}`）を検証者も目視し、追加の条件と、どの呼び出し経路かが不明であることを conditions に書いた。

### Anthropic — Claude Code（CLI）2.1.287 — 権限の提案（組み込みスキル fewer-permission-prompts と思われるプロンプト）

<a id="g-g2-closed-clients-missing-07"></a>
#### G2CCM-07 Anthropic — Claude Code（CLI）2.1.287 — 権限の提案（組み込みスキル fewer-permission-prompts と思われるプロンプト）

- **資料**: 同バイナリ内のスキル用プロンプト（allow ルールの提案手順）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1415483 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）（直前の Markdown 見出し: ## Check 9 — pre-approve frequently denied read-only commands）
- **原文**:

> the MCP readOnlyHint annotation is a server-supplied hint and isn't recorded in transcripts, so judge from semantics, conservatively

- **日本語**: MCP の readOnlyHint はサーバーが申告するヒントで、記録（transcript）にも残らない。だから意味（名前と説明）から保守的に判断せよ。
- **どう使っているか**: Anthropic 自身のプロンプトが、allow ルールを提案するときに readOnlyHint を根拠にしないよう指示する。理由は 2 つ書かれている: サーバーが申告するヒントであること、記録（transcript）に残らないこと。さらに「名前も説明もサーバーが選ぶ文字列なので get_ の接頭辞は読み取り専用の保証ではない」と書く。
- **条件**: 拒否された呼び出しを集計して allow ルールを提案する手順の中（Read-only only の項）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・使わない・読まない
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 バイナリ内では `\`readOnlyHint\`` のようにバッククォートがエスケープされているため loose 一致（記号の差だけ）。どのスキルかはプロンプト文面からの推定（「propose permission allow rules … so they stop costing a prompt」）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 道具の出力で、この文が「## Check 9 — pre-approve frequently denied read-only commands」という Markdown 見出しの下にあると分かったので location に入れた。usage_ja に、根拠にしない理由が「自己申告」と「記録に残らない」の 2 つであることを足した。

### Anthropic — Claude Code（CLI）2.1.287 — auto mode（機能フラグつき）

<a id="g-g2-closed-clients-missing-08"></a>
#### G2CCM-08 Anthropic — Claude Code（CLI）2.1.287 — auto mode（機能フラグつき）

- **資料**: 同バイナリ内の auto mode 判定の補助関数（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1407058 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> function cVt(e,n,r,s){return e?.source==="mcpServerPolicy"&&Aa(s)&&(n.isDestructive?.(r)??!1)&&C("tengu_cowork_auto_mode_include_allowed_write_mcp",!1)}

- **日本語**: allow ルールの出どころが mcpServerPolicy（MCP サーバー設定に付いたツールポリシー）で、auto mode で、ツールが isDestructive（destructiveHint）で、機能フラグ tengu_cowork_auto_mode_include_allowed_write_mcp が立っているときに真。
- **どう使っているか**: auto mode では、destructiveHint:true の MCP ツールについて、mcpServerPolicy の allow ルールをそのまま使わず確認・分類器の判定に回すかどうかの条件に使う（機能フラグが既定 false なので、既定では効かない）。ただし、これとは別に、mcpServerPolicy の ask ルールの扱いでは機能フラグなしで isDestructive を使う（34）。
- **条件**: auto mode（Aa）かつ機能フラグ（既定値 !1 = false）。同じ所に tengu_remote_auto_mode_include_destructive_mcp / tengu_modular_mochi（どちらも既定 false）を条件にする gVo もある。mcpServerPolicy のルールは、scope が "dynamic" の MCP サーバー設定から作られる（関数 jYo。目視。実行時にホストや SDK から渡されるサーバー設定と思われる）。「組織のポリシー」かどうかはコードからは断定できない。destructiveHint の欠落は false（02）なので、宣言の無いツールはこの経路に入らない。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・危険度を付ける
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 機能フラグはサーバー側で切り替わりうる（実際の値は不明）。Cowork 向けの名前だが同じバイナリにある。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 「mcpServerPolicy（組織の MCP ポリシー）」は根拠が無い。コードでは scope が dynamic の MCP サーバー設定から作られるルール（表示名は "MCP server policy"）なので書き直した。「既定では効かない」は cVt についてだけ正しく、isDestructive 全体では既定経路でも使われる（34）ことを足した。

### GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— 許可サービス

<a id="g-g2-closed-clients-missing-09"></a>
#### G2CCM-09 GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— 許可サービス

- **資料**: @github/copilot@1.0.63 app.js: 許可サービス（i2t）の onMCP（クライアントのソースコード）
- **URL**: https://unpkg.com/@github/copilot@1.0.63/app.js
- **版**: @github/copilot 1.0.63（2026-06-16）
- **書いてある場所**: ファイル内の改行で区切った 144 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> if(B.readOnly)return{kind:"approved"};if(m)return{kind:"approved"};if(F.permissionsHasMcpApproval(

- **日本語**: MCP ツールの許可要求で、deny ルールに当たらず、要求の readOnly が真なら、そのまま「承認」を返す（利用者に聞かない）。
- **どう使っているか**: readOnlyHint:true の MCP ツールは、deny ルールに当たらなければ確認なしで走る。欠落・false のツールは --allow-all-tools（approveAllToolPermissionRequests）・保存済みの承認ルール・利用者への確認に回る。
- **条件**: deny ルール（permissionsMatchingMcpRules）が先に効く。パスのコンテンツ除外・パス許可は MCP の要求には掛からない（パスを集める関数で onMCP:B=>[] なので空）。m（approveAllToolPermissionRequests）は readOnly の判定の後。ツール側で requestRequired のときだけこの許可サービスを通る（loadTools の callback）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、144 行（取得 2026-10-02T22:11:38Z、sha256 4e546b0f9bd7…）
- **補足**: @github/copilot@1.0.63（2026-06-16 公開。JS バンドル app.js を npm に直接含む最後の正式版。プレリリース 1.0.64-0 まで同形式。1.0.64-1 以降の npm パッケージは 13KB のローダだけで、本体は各 OS 用の Node SEA バイナリ @github/copilot-linux-x64）。unpkg から app.js（9,904,363 bytes）を直接取って照合。同じ形の分岐（`<x>.readOnly)return{kind:"approved"}`）は 0.0.400 の index.js、1.0.6・1.0.35・1.0.45・1.0.55 の app.js にもあることを grep で確認（道具では未照合。1.0.20 は取得タイムアウトで不明）。 文書（C03_microsoft_github-19:『All MCP tool invocations require explicit permission. This applies even to read-only operations on external services.』）と実装が食い違う。現行 1.0.91 では許可の処理が Rust 製のネイティブモジュール prebuilds/linux-x64/runtime.node に移っており、JS（app.js）には ToolAnnotations のスキーマ 1 か所しか残っていない（grep）。1.0.91 で同じ自動承認が続くかは不明（コンパイル済みのため照合できない）。 検証者の追記: 『onMCP:B=>[],onRead:B=>[B.path]』も exact（144 行目）。検証者も unpkg から 1.0.55 の app.js・0.0.400 の index.js・1.0.6 の app.js を取り、`<x>.readOnly)return{kind:"approved"}` の形を grep で確かめた（M.readOnly / g.readOnly / C.readOnly。道具では未照合）。1.0.91 の埋め込み app.js（SEA の gzip 資産を展開、7,593,700 bytes）には readOnlyHint が 1 個（Zod スキーマ）だけで、`readOnly)return{kind:"approved"}` と `onMCP:async` は 0 件（grep）。 「コンテンツ除外に当たらなければ」は誤り。コンテンツ除外とパス許可はパスを持つ要求だけに掛かり、MCP の要求のパス一覧は常に空。usage_ja・conditions を直した。古い版の grep は検証者も一部（1.0.55・0.0.400・1.0.6）を再確認した。

### GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— MCP ツール一覧の取り込み

<a id="g-g2-closed-clients-missing-10"></a>
#### G2CCM-10 GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— MCP ツール一覧の取り込み

- **資料**: @github/copilot@1.0.63 app.js: getServerTools / ツール登録（クライアントのソースコード）
- **URL**: https://unpkg.com/@github/copilot@1.0.63/app.js
- **版**: 1.0.63
- **書いてある場所**: ファイル内の改行で区切った 1692 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> input_schema:YMe(f.inputSchema),readOnly:x?.readOnlyHint

- **日本語**: サーバーの tools/list の annotations から readOnlyHint を取り出し、ツールの readOnly に入れる。
- **どう使っているか**: サーバーの自己申告 readOnlyHint を、そのまま許可要求の readOnly（09）に渡す。title も表示名に使う（x?.title）。
- **条件**: 既定の GitHub サーバー（isDefaultServer）では listTools() を呼ばず同梱の manifest の annotations を使う。他のサーバーは tools/list の値。
- **扱う宣言**: readOnlyHint・title ／ **使い方の分類**: そのまま渡す・見せる・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、1692 行（## Additional Focus Instructions）（取得 2026-10-02T22:11:38Z、sha256 4e546b0f9bd7…）
- **補足**: @github/copilot@1.0.63（2026-06-16 公開。JS バンドル app.js を npm に直接含む最後の正式版。プレリリース 1.0.64-0 まで同形式。1.0.64-1 以降の npm パッケージは 13KB のローダだけで、本体は各 OS 用の Node SEA バイナリ @github/copilot-linux-x64）。unpkg から app.js（9,904,363 bytes）を直接取って照合。同じ形の分岐（`<x>.readOnly)return{kind:"approved"}`）は 0.0.400 の index.js、1.0.6・1.0.35・1.0.45・1.0.55 の app.js にもあることを grep で確認（道具では未照合。1.0.20 は取得タイムアウトで不明）。 補助の照合: 許可要求を作る『toolTitle:b,args:p,readOnly:!!u.readOnly})』も exact（ファイル内の改行で区切った 1697 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安））。readOnly は !!（真偽化）されるので欠落は false。

### GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— ACP の許可要求

<a id="g-g2-closed-clients-missing-11"></a>
#### G2CCM-11 GitHub — GitHub Copilot CLI（1.0.63 の JS 実装）— ACP の許可要求

- **資料**: @github/copilot@1.0.63 app.js: ACP 向けの許可要求の変換（クライアントのソースコード）
- **URL**: https://unpkg.com/@github/copilot@1.0.63/app.js
- **版**: 1.0.63
- **書いてある場所**: ファイル内の改行で区切った 5249 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> kind:n.readOnly?"read":"other"

- **日本語**: ACP（エディタ連携）に送る許可要求では、MCP ツールの readOnly が真なら kind を "read"、そうでなければ "other" にする。
- **どう使っているか**: 式としては readOnly を ACP の ToolKind（read / other）に写す。しかし同じ版で ACP の許可要求を作る gze は、mcp の要求を {toolCallId, kind:"mcp", serverName, toolName, toolTitle, args} に作り直して渡し、readOnly を落とす。さらに許可サービス i2t は readOnly の MCP 呼び出しを利用者に聞く前に承認する（09）。このため、1.0.63 で ACP クライアントに kind:"read" の MCP 許可要求が届く経路は見つからなかった（実際には常に "other" になると考えられる）。
- **条件**: Copilot CLI を ACP サーバーとして使うとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、5249 行（## Step 6: Save the Report）（取得 2026-10-02T22:11:38Z、sha256 4e546b0f9bd7…）
- **補足**: @github/copilot@1.0.63（2026-06-16 公開。JS バンドル app.js を npm に直接含む最後の正式版。プレリリース 1.0.64-0 まで同形式。1.0.64-1 以降の npm パッケージは 13KB のローダだけで、本体は各 OS 用の Node SEA バイナリ @github/copilot-linux-x64）。unpkg から app.js（9,904,363 bytes）を直接取って照合。同じ形の分岐（`<x>.readOnly)return{kind:"approved"}`）は 0.0.400 の index.js、1.0.6・1.0.35・1.0.45・1.0.55 の app.js にもあることを grep で確認（道具では未照合。1.0.20 は取得タイムアウトで不明）。 検証者の照合: 『case"mcp":return Zj(t)({toolCallId:e.toolCallId,kind:"mcp",serverName:e.serverName,toolName:e.toolName,toolTitle:e.toolTitle,args:e.args??null});』exact（5249 行目）。mze の呼び出し元は Zj・ALi・_Li の 3 つだけ（grep）。 発見者の「readOnlyHint を ACP の表示・判断材料にする」は言い過ぎ。ACP 経路の gze が readOnly を落とすので、kind:"read" は実際には出ない（死んだ分岐）と考えられる。usage・usage_ja を直した。

### Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（toolAllowlistMode "reads"）

<a id="g-g2-closed-clients-missing-12"></a>
#### G2CCM-12 Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（toolAllowlistMode "reads"）

- **資料**: workbench.desktop.main.js: mcp-tool-annotations.ts / admin-mcp-policy.ts（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_workbench.desktop.main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Cursor 3.23.12（commit 2d29876d…）
- **書いてある場所**: ファイル内の改行で区切った 8766 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> case"reads":return Igv(t.annotations)

- **日本語**: 管理者の許可リストのモードが "reads" のとき、ツールが許されるかは annotations で決める（Igv）。
- **どう使っているか**: チーム管理者が allowedMcpServers の toolAllowlistMode を "reads" にすると、readOnlyHint:true かつ destructiveHint が true でないツール（declared_read）だけが使え、それ以外（宣言なしを含む）は "disabledByAdmin" になる（13）。さらに同じ reads ポリシーは管理者の MCP 許可リストとしても働き、declared_read のツールはエージェント側の shouldBlockMcp で「ALLOWED (in admin MCP allowlist)」となって確認なしで走る（35）。つまり reads モードのサーバーのツールは、宣言が read なら自動実行、そうでなければ無効、のどちらかになる。
- **条件**: 管理者設定（adminSettingsService の allowedMcpConfiguration）で reads モードを選んだサーバーだけ。all / custom（名前で指定）では注釈を見ない。 自動実行の側は、エージェント（cursor-agent-exec）の permissions-service で、チームの MCP ツール制御（getMcpToolControls。管理者設定 allowedMcpConfiguration から作られる）が有効なとき。explicit deny が先に効く。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・ツールを絞る・隠す・宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Cursor 3.23.12（product.json の commit 2d29876d567da1607532b23bbf2cd5ddbca496f0。https://cursor.com/api/download?platform=linux-x64&releaseTrack=stable が 2026-10-02 に返した stable）の .deb を展開し、usr/share/cursor/resources/app/ 以下のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。ミニファイ名は版ごとに変わる。 補助の照合: 『function Igv(e){return e===void 0||e.destructiveHint===!0?!1:e.readOnlyHint===!0}』（判定関数。annotations が無ければ false、destructiveHint:true なら false、readOnlyHint===true のときだけ true）も exact（ファイル内の改行で区切った 8766 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安））。Cursor の公開文書（cursor.com/docs/mcp、C07 の checked_no_mention）は注釈に触れないが「Tool allowlists restrict which tools from an approved server can run automatically」と書く。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 用途が足りなかった。reads モードは無効化だけでなく、declared_read のツールを管理者の許可リストに入れて確認なしで実行させる（新規 35 として照合）。usage に auto_approve を足し、usage_ja・conditions を直した。

### Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（無効化の判定）

<a id="g-g2-closed-clients-missing-13"></a>
#### G2CCM-13 Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（無効化の判定）

- **資料**: workbench.desktop.main.js: makeToolDisabledChecker（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_workbench.desktop.main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 3.23.12
- **書いてある場所**: ファイル内の改行で区切った 8767 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> if(o!==void 0){const a=Pmo(o);a.mode!=="all"&&(s=(c,l)=>!jgv(a,{name:c,annotations:l}))}return(a,c)=>{if(s?.(a,c))return"disabledByAdmin"

- **日本語**: サーバーに管理者ポリシーがあり、モードが all 以外なら、そのポリシーに合わないツール（reads モードなら宣言上 read でないもの）を "disabledByAdmin"（管理者により無効）にする。
- **どう使っているか**: 注釈の無いツールは reads モードでは無効化される（欠落時は使えない側）。宣言が嘘なら書き込みツールが「read」として通る。
- **条件**: 管理者ポリシーがあるサーバーだけ。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Cursor 3.23.12（product.json の commit 2d29876d567da1607532b23bbf2cd5ddbca496f0。https://cursor.com/api/download?platform=linux-x64&releaseTrack=stable が 2026-10-02 に返した stable）の .deb を展開し、usr/share/cursor/resources/app/ 以下のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。ミニファイ名は版ごとに変わる。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Cursor (Anysphere) — Cursor 3.23.12 — ツールの読み / 書きの分類（利用者のトグル・表示）

<a id="g-g2-closed-clients-missing-14"></a>
#### G2CCM-14 Cursor (Anysphere) — Cursor 3.23.12 — ツールの読み / 書きの分類（利用者のトグル・表示）

- **資料**: workbench.desktop.main.js: ufv / fZd / a9p（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_workbench.desktop.main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 3.23.12
- **書いてある場所**: ファイル内の改行で区切った 8766 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> function ufv(e){return RXd(e)?"declared_read":e?.readOnlyHint===!1||e?.destructiveHint===!0?"write":"unannotated"}

- **日本語**: ツールを 3 つに分ける: 宣言上の読み取り（declared_read）、書き込み（readOnlyHint:false か destructiveHint:true）、注釈なし（unannotated）。
- **どう使っているか**: 利用者側の「reads / writes」ごとのオン・オフ（off / custom）では、declared_read だけが reads で、unannotated は writes に入る（14b）。設定画面でもツールを reads / writes に分けて並べる（a9p）。
- **条件**: 利用者が MCP サーバーごとに reads / writes のグループを off にしたとき、そのグループのツールは "disabledByUser"。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 表示（印・名前）・ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Cursor 3.23.12（product.json の commit 2d29876d567da1607532b23bbf2cd5ddbca496f0。https://cursor.com/api/download?platform=linux-x64&releaseTrack=stable が 2026-10-02 に返した stable）の .deb を展開し、usr/share/cursor/resources/app/ 以下のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。ミニファイ名は版ごとに変わる。 補助の照合: 『function fZd(e){return ufv(e)==="declared_read"?"reads":"writes"}』も exact（ファイル内の改行で区切った 8766 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安））。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Cursor (Anysphere) — Cursor 3.23.12 — Smart mode（分類器による自動実行）

<a id="g-g2-closed-clients-missing-15"></a>
#### G2CCM-15 Cursor (Anysphere) — Cursor 3.23.12 — Smart mode（分類器による自動実行）

- **資料**: extensions/cursor-agent-exec/dist/main.js: MCP 呼び出しの前処理（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_cursor-agent-exec_main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 3.23.12
- **書いてある場所**: ファイル内の改行で区切った 5 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> input_schema_json:U.slice(0,12e3),...void 0===L?{}:{annotations:L}

- **日本語**: Smart mode の分類器に渡すツール定義の情報に、説明・入力スキーマと並べて annotations も入れる。
- **どう使っているか**: サーバーの自己申告 annotations を、自動実行してよいかを決める分類器（LLM と思われる）への入力に含める。分類器が注釈をどう重みづけるかは不明。
- **条件**: Smart mode（smartModeClassifierMode）が有効なとき。annotations を含む toolDefinitionMetadata は approvalProvider（m）があるときだけ作られる。その前に MCP の allowlist precheck（annotationsJson を渡す）があり、許可リストに入っていれば分類器は呼ばれない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 危険度を付ける・そのまま渡す・見せる
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Cursor 3.23.12（product.json の commit 2d29876d567da1607532b23bbf2cd5ddbca496f0。https://cursor.com/api/download?platform=linux-x64&releaseTrack=stable が 2026-10-02 に返した stable）の .deb を展開し、usr/share/cursor/resources/app/ 以下のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。ミニファイ名は版ごとに変わる。 同じ関数で allowlist の事前照会 `new eL.cME({providerIdentifier:ne,toolName:i.toolName,toolCallId:R.toolCallId,annotationsJson:M?.annotationsJson})` にも annotations を渡す（目視）。その照会先の判定は不明。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 検証者の追記: 同じファイルの permissions-service に、annotationsJson から注釈を読んで許可リスト判定をする isMcpFullyAllowlisted があり、チームの reads ポリシーでは declared_read を許可リスト入りとする（35）。precheck（eL.ODj）の照会先がこれかは確かめていない（推定）。 conditions に「annotations が分類器に渡るのは approvalProvider があるときだけ」「precheck で許可リスト入りなら分類器を呼ばない」を足し、precheck が注釈を使いうる（35）ことを notes に足した。

### Cursor (Anysphere) — Cursor 3.23.12 — 独自の注釈キー cursor/requiresConfirmation

<a id="g-g2-closed-clients-missing-16"></a>
#### G2CCM-16 Cursor (Anysphere) — Cursor 3.23.12 — 独自の注釈キー cursor/requiresConfirmation

- **資料**: extensions/cursor-agent-exec/dist/main.js（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_cursor-agent-exec_main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 3.23.12
- **書いてある場所**: ファイル内の改行で区切った 5 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> void 0!==K?ue.smartModeApproval=K:!c||J||(0,dH.cB)(L)||(ue.skipApproval=!0)

- **日本語**: 分類器の結果（K）があればそれを使う。無ければ、Smart mode が有効で、allowlist に無く、注釈に cursor/requiresConfirmation が無いときに限り、通常の承認を省く（skipApproval）。
- **どう使っているか**: ToolAnnotations に Cursor 独自のキー "cursor/requiresConfirmation": true を書くと、Smart mode でも承認を省かない。標準の 4 hint ではなく独自キー。
- **条件**: Smart mode の経路だけ。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Cursor 3.23.12（product.json の commit 2d29876d567da1607532b23bbf2cd5ddbca496f0。https://cursor.com/api/download?platform=linux-x64&releaseTrack=stable が 2026-10-02 に返した stable）の .deb を展開し、usr/share/cursor/resources/app/ 以下のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。ミニファイ名は版ごとに変わる。 補助の照合: キー名『const n="cursor/requiresConfirmation"』も exact（ファイル内の改行で区切った 5 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安））。この値は annotations からだけ写される（cursor-local-agent-runtime の sK 関数で、4 hint と title に加えて TI キーを annotationsJson に入れる。目視）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Cognition — Devin CLI 3000.10.48（Devin Desktop 3.10.48 に同梱）— 制限モードでの MCP 呼び出し

<a id="g-g2-closed-clients-missing-17"></a>
#### G2CCM-17 Cognition — Devin CLI 3000.10.48（Devin Desktop 3.10.48 に同梱）— 制限モードでの MCP 呼び出し

- **資料**: Devin CLI バイナリ（toolbox/src/tools/mcp/call_tool.rs 由来のメッセージ）（クライアントのソースコード）
- **URL**: https://windsurf-stable.codeiumdata.com/linux-x64/stable/fcf7ba39e6150055fad817f8716385b4d320d46d/Devin-linux-x64-3.10.48.tar.gz
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/devin-desktop-3.10.48_devin-cli）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: devin 3000.10.48 (fcf7ba39)（`devin --version` の出力）
- **書いてある場所**: ファイル内の改行で区切った 547334 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> is currently unavailable: only tools annotated as read-only (readOnlyHint) can be called in the current mode.

- **日本語**: （MCP ツール X はサーバー Y で）今は使えない。今のモードでは、read-only と注記（readOnlyHint）されたツールしか呼べない。
- **どう使っているか**: ある制限モードでは、readOnlyHint:true の MCP ツールだけ呼べ、宣言の無いツールは拒否される。モードは同梱の changelog から Plan mode と推定されるが、同じく読み取り専用の Ask mode（/ask）の可能性もある。
- **条件**: 「current mode」が何かはバイナリからは断定できない。同梱 docs/changelog/stable.mdx に「Plan mode now allows read-only MCP tools (those annotated `readOnlyHint: true`)…」（C07_ide_agents-21 と同じ文、道具での照合は C07 で済み）。 同じ changelog（検証者が tarball から取り直して確認）は、より新しい項目で「Plan mode now uses the normal permission system」とも書く。Ask mode も「Ask and Plan modes can now use the read-only `webfetch` and `notebook_read` tools」のように読み取り専用の道具の組を共有している。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Devin Desktop（旧 Windsurf）3.10.48 / productVersion 1.126.0 / commit fcf7ba39（https://windsurf-stable.codeiumdata.com/api/update/linux-x64/stable/latest が 2026-10-02 に返した版。tarball sha256 98e394baeefc8755…）を展開し、中のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。 Rust の静的バイナリ（184,820,200 bytes, sha256 460e37d4…）。メッセージの直前の文字列が toolbox/src/tools/mcp/call_tool.rs。C07 の検証者が「v3000.4.16 で Plan モードが通常の権限に変わり、readOnlyHint の絞り込みが今も続くかは不明」とした点について、現行 3000.10.48 にもこの拒否メッセージが残っていることを示す（どのモードで使われるかは不明のまま）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 「current mode」を Plan と推定する根拠は changelog だけで、Ask mode も読み取り専用のモードとして存在する（changelog の /ask の項）。usage_ja・conditions に候補として足した。

### Cognition — Devin Desktop 3.10.48 — ACP サーバーの MCP ツール一覧の表示

<a id="g-g2-closed-clients-missing-18"></a>
#### G2CCM-18 Cognition — Devin Desktop 3.10.48 — ACP サーバーの MCP ツール一覧の表示

- **資料**: out/vs/workbench/windsurf-chat-client/index.js（クライアントのソースコード）
- **URL**: https://windsurf-stable.codeiumdata.com/linux-x64/stable/fcf7ba39e6150055fad817f8716385b4d320d46d/Devin-linux-x64-3.10.48.tar.gz
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/devin-desktop-3.10.48_windsurf-chat-client_index.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Devin Desktop 3.10.48
- **書いてある場所**: ファイル内の改行で区切った 18459 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> let s=r.filter(e=>!0===e.readOnlyHint),l=r.filter(e=>!0!==e.readOnlyHint)

- **日本語**: ツールを readOnlyHint が true のものと、それ以外に分ける（画面の節の見出しは "Read-only" と "Write"）。
- **どう使っているか**: 設定画面で MCP ツールを「Read-only」「Write」に分けて並べる。宣言の無いツールは Write 側。承認への効果はこのコードからは不明。
- **条件**: ACP サーバー（fetchAcpServerTools）のツール一覧の表示。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 表示（印・名前）・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Devin Desktop（旧 Windsurf）3.10.48 / productVersion 1.126.0 / commit fcf7ba39（https://windsurf-stable.codeiumdata.com/api/update/linux-x64/stable/latest が 2026-10-02 に返した版。tarball sha256 98e394baeefc8755…）を展開し、中のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。 補助の照合: 『function iQ3(e){return"object"==typeof e&&null!==e&&!0===e.readOnlyHint}』も exact。節見出し sectionTitle:"Read-only" / "Write" は同じ関数内で目視。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Cognition — Devin Desktop 3.10.48 — 拡張機能からバックエンドへのツール定義

<a id="g-g2-closed-clients-missing-19"></a>
#### G2CCM-19 Cognition — Devin Desktop 3.10.48 — 拡張機能からバックエンドへのツール定義

- **資料**: extensions/windsurf/dist/extension.js: exa.chat_pb.ChatToolDefinition（クライアントのソースコード）
- **URL**: https://windsurf-stable.codeiumdata.com/linux-x64/stable/fcf7ba39e6150055fad817f8716385b4d320d46d/Devin-linux-x64-3.10.48.tar.gz
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/devin-desktop-3.10.48_windsurf_extension.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Devin Desktop 3.10.48
- **書いてある場所**: ファイル内の改行で区切った 2 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> serverName="";readOnlyHint;computerUseConfig;

- **日本語**: バックエンドに送るツール定義（protobuf の ChatToolDefinition）に readOnlyHint の欄がある。
- **どう使っているか**: readOnlyHint をサーバー側（Cascade / Devin のバックエンド）へ渡す欄がある。バックエンドでの使い道は不明。
- **条件**: —
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: Devin Desktop（旧 Windsurf）3.10.48 / productVersion 1.126.0 / commit fcf7ba39（https://windsurf-stable.codeiumdata.com/api/update/linux-x64/stable/latest が 2026-10-02 に返した版。tarball sha256 98e394baeefc8755…）を展開し、中のファイルを 127.0.0.1:8765 で配信して照合（fetched_url は一時 URL）。 公開文書 docs.windsurf.com/windsurf/cascade/mcp は注釈に触れない（C07 の checked_no_mention）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Google — Google Antigravity（2.0 / IDE / CLI）— MCP の権限

<a id="g-g2-closed-clients-missing-20"></a>
#### G2CCM-20 Google — Google Antigravity（2.0 / IDE / CLI）— MCP の権限

- **資料**: MCP | Google Antigravity Docs（クライアントの文書）
- **URL**: https://antigravity.google/docs/mcp
- **書いてある見出しへ直接**: https://antigravity.google/docs/mcp#mcp-permissions-and-access-control
- **版**: 2026-10-02 取得
- **書いてある場所**: Model Context Protocol (MCP) > MCP permissions and access control（#mcp-permissions-and-access-control）
- **原文**:

> By default, unconfigured MCP tools run in Ask mode, requiring your approval before execution.

- **日本語**: 既定では、設定していない MCP ツールは Ask モードで動き、実行前にあなたの承認が要る。
- **どう使っているか**: MCP ツールの既定は一律に Ask。許可は mcp(server/tool)・mcp(server/*)・mcp(*) の名前パターンで書く。注釈による例外はページに書かれていない（readOnlyHint・destructiveHint・annotations は none）。
- **条件**: ポリシーで allow を書いていないツール。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > MCP permissions and access control」（取得 2026-10-02T22:11:20Z、sha256 669311a0ac3a…）
- **補足**: Antigravity の公開文書（Starlight 製、HTML を直接取得）。 同じ節の続き: 「mcp(server/tool) : Matches a specific tool on a specific server. mcp(server/*) … mcp(*) …」。/docs/permissions・/docs/cli/commands/permissions の本文はほぼナビゲーションだけで、注釈の語は none（checked_no_mention）。

### Google — Antigravity SDK（Python, google-antigravity）— safe_defaults ポリシー

<a id="g-g2-closed-clients-missing-21"></a>
#### G2CCM-21 Google — Antigravity SDK（Python, google-antigravity）— safe_defaults ポリシー

- **資料**: google/antigravity/hooks/policy.py: safe_defaults（SDK のソースコード）
- **URL**: https://github.com/google-antigravity/antigravity-sdk-python/blob/12f9a4c3becf487302dc799b0f59054f01f3ddb9/google/antigravity/hooks/policy.py#L472-L477
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/google-antigravity/antigravity-sdk-python/12f9a4c3becf487302dc799b0f59054f01f3ddb9/google/antigravity/hooks/policy.py
- **版**: commit 12f9a4c3becf487302dc799b0f59054f01f3ddb9（2026-10-02 の HEAD。PyPI 最新は 0.1.20）
- **書いてある場所**: L472-477
- **原文**:

```
read_only_tools = list(types.BuiltinTools.read_only()) + list(
      types.BuiltinTools.deprecated()
  )
  return [allow(t.value) for t in read_only_tools] + [
      ask_user("*", handler=handler)
  ]
```

- **日本語**: 「読み取り専用」は SDK の組み込みツールの固定リスト（view_file など）で、それだけ allow。他は全部 ask_user（利用者に聞く）。
- **どう使っているか**: SDK の「read-only は許可」の read-only は組み込みツール名の固定表で、MCP の readOnlyHint ではない。MCP ツールは宣言に関係なく ask_user に落ちる。
- **条件**: safe_defaults を使ったとき。リポジトリ全体（google/ 以下の .py）で readOnlyHint / read_only_hint / destructiveHint は 0 件（grep）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、472-477 行（# ---------------------------------------------------------------------------）（取得 2026-10-02T22:11:37Z、sha256 7e0a1100db7c…）
- **補足**: 文書側の対応: 『By default, custom Python functions and standard read-only tools are allowed, while high-risk system operations (such as executing shell commands using run_command ) require explicit permission or policy rules.』（https://antigravity.google/docs/sdk/policies, Safety policies and permissions（#safety-policies-and-permissions）, match=loose。文中の空白の差で loose）。BuiltinTools.read_only() は VIEW_FILE / READ_URL_CONTENT / SCHEDULE / FINISH（types.py, 目視）。

### Google — Google Antigravity IDE 1.23.2 — language server（Go バイナリ）

<a id="g-g2-closed-clients-missing-22"></a>
#### G2CCM-22 Google — Google Antigravity IDE 1.23.2 — language server（Go バイナリ）

- **資料**: resources/app/extensions/antigravity/bin/language_server_linux_x64（クライアントのソースコード）
- **URL**: https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/1.23.2-4781536860569600/linux-x64/Antigravity.tar.gz
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/antigravity-1.23.2_language_server_linux_x64）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: Antigravity IDE 1.23.2（https://antigravity.google/download/linux が 2026-10-02 に示した stable）。VS Code 1.107.0 系
- **書いてある場所**: ファイル内の改行で区切った 11250 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> v1internal_go_proto.(*ToolAnnotations).GetReadOnlyHint

- **日本語**: 内部 API（google.internal.cloud.code.v1internal）の protobuf に ToolAnnotations 型と GetReadOnlyHint がある。
- **どう使っているか**: エージェント本体（Go）が ToolAnnotations を扱う型を持つことだけが分かる。承認・表示に使うかはコンパイル済みのため不明。
- **条件**: —
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: tarball（228,662,083 bytes）を展開し、language_server_linux_x64（134,458,808 bytes, sha256 4b23f0a2949f…）を 127.0.0.1:8765 で配信して照合。readOnlyHint を含む文字列は 6 個だけで、すべて protobuf / JSON のタグ。文書（20）は MCP ツールの既定を一律 Ask と書くので、注釈による例外は無いと推定されるが、確かめられない（不明）。現行の Antigravity 2.0 / CLI は調べていない。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。

### Google — Google Cloud Data Agent Kit（Antigravity 等の IDE 拡張）— MCP 利用の制御

<a id="g-g2-closed-clients-missing-23"></a>
#### G2CCM-23 Google — Google Cloud Data Agent Kit（Antigravity 等の IDE 拡張）— MCP 利用の制御

- **資料**: Use MCP servers | Data Agent Kit（公式の文書）
- **URL**: https://docs.cloud.google.com/data-cloud-extension/antigravity/use-mcp-servers
- **書いてある見出しへ直接**: https://docs.cloud.google.com/data-agent-kit/use-mcp-servers#control-mcp-use-iam
- **版**: 2026-10-02 取得（最終 URL https://docs.cloud.google.com/data-agent-kit/use-mcp-servers）
- **書いてある場所**: Use MCP servers Stay organized with collections Save and categorize content based on your preferences. > Optional security and safety configurations > Control MCP use with IAM policies（#control-mcp-use-iam）
- **原文**:

> Tool properties like the read-only attribute.

- **日本語**: （IAM の deny / allow ポリシーで）ツールの性質、たとえば read-only の属性に基づいて許可・拒否できる。
- **どう使っているか**: クライアント（Antigravity）ではなく Google Cloud 側（MCP サーバー側の IAM）で、ツールの read-only 属性を条件にする。
- **条件**: Google Cloud / Google のマネージド MCP サーバーを使うとき。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Use MCP servers Stay organized with collections Save and categorize content based on your preferences. > Optional security and safety configurations > Control MCP use with IAM policies」（取得 2026-10-02T22:11:24Z、sha256 d617dba727e4…）
- **補足**: 属性の正体（tool.isReadOnly）と「注記が無ければ false」は C06_google_aws-13〜15（IAM の文書）を参照。このページ自体は readOnlyHint / annotations の語を使わない（checked_no_mention）。 再実行で sha256 が ed3af15b36b0 に変わった（発見者は b2de91805ed7。ページの動的部分の差と思われる）。引用・位置は同じ。

### Mistral AI — Mistral Vibe（Vibe Code CLI, OSS）— ツール権限の既定

<a id="g-g2-closed-clients-missing-24"></a>
#### G2CCM-24 Mistral AI — Mistral Vibe（Vibe Code CLI, OSS）— ツール権限の既定

- **資料**: vibe/core/tools/base.py: BaseToolConfig（クライアントのソースコード）
- **URL**: https://github.com/mistralai/mistral-vibe/blob/7c19608af06f6c61d63f8f7a5c3430da73fba2ab/vibe/core/tools/base.py#L144
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/mistralai/mistral-vibe/7c19608af06f6c61d63f8f7a5c3430da73fba2ab/vibe/core/tools/base.py
- **版**: commit 7c19608af06f6c61d63f8f7a5c3430da73fba2ab（2026-10-02 の HEAD）
- **書いてある場所**: L144
- **原文**:

> permission: ToolPermission = ToolPermission.ASK

- **日本語**: ツール設定の権限の既定値は ASK（毎回確認）。
- **どう使っているか**: MCP ツール（vibe/core/tools/mcp/tools.py の MCPHttpProxyTool / MCPStdioProxyTool は BaseToolConfig を使う）も既定は ASK。リポジトリ全体（Python と Rust の harness・cli-rust）で readOnlyHint / read_only_hint / destructiveHint は 0 件（grep）で、注釈は読まない。
- **条件**: default エージェント。plan エージェントの上書きは組み込みの write_file / edit を never にするだけ（vibe/core/agents/models.py）。auto-approve は bypass_tool_permissions。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、144 行（取得 2026-10-02T22:11:35Z、sha256 70d706fa373a…）
- **補足**: Smart Approve エージェントはモデルの分類器でツール呼び出しを判定するが、分類器への入力に MCP 注釈を渡すコードは無い（grep 0 件）。

### Mistral AI — Mistral Vibe（Vibe Code）— エージェントごとの承認

<a id="g-g2-closed-clients-missing-25"></a>
#### G2CCM-25 Mistral AI — Mistral Vibe（Vibe Code）— エージェントごとの承認

- **資料**: Safety, approvals, and permissions | Mistral Docs（クライアントの文書）
- **URL**: https://docs.mistral.ai/vibe/code/safety-approvals-permissions
- **照らし合わせた中身の URL**: https://docs.mistral.ai/vibe/code/safety-approvals-permissions.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: L32（直前の Markdown 見出し: # Safety, approvals, and permissions）
- **原文**:

> In **programmatic mode** (`vibe --prompt …`), Vibe falls back to `auto-approve` when `--agent` is not provided

- **日本語**: プログラムから使うモード（vibe --prompt …）では、--agent を指定しないと auto-approve（全部自動承認）に落ちる。
- **どう使っているか**: 非対話の既定は全ツール自動承認なので、MCP ツールは宣言に関係なく確認なしで走る。対話の既定（default）は「Asks before running any tool」。
- **条件**: programmatic mode で --agent なし。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 exact・1 か所、32 行（# Safety, approvals, and permissions）（取得 2026-10-02T22:11:24Z、sha256 07b5f30e4798…）
- **補足**: 補助の照合: plan エージェントの行『| `plan` | Read-only. Auto-approves safe read tools, blocks edits and commands. |』も exact（L27（直前の Markdown 見出し: # Safety, approvals, and permissions））。「safe read tools」が何かは文書に無い。コード（24）では組み込みツールの設定で決まり、MCP の注釈は使わない。ページに readOnlyHint / destructiveHint / annotations は none。

### Mistral AI — Mistral Vibe Work（旧 Le Chat のコネクタ）— 関数ごとの許可

<a id="g-g2-closed-clients-missing-26"></a>
#### G2CCM-26 Mistral AI — Mistral Vibe Work（旧 Le Chat のコネクタ）— 関数ごとの許可

- **資料**: Safety and approvals | Mistral Docs (Vibe Work)（クライアントの文書）
- **URL**: https://docs.mistral.ai/vibe/work/safety-and-approvals
- **照らし合わせた中身の URL**: https://docs.mistral.ai/vibe/work/safety-and-approvals.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: L54（直前の Markdown 見出し: # Safety and approvals）
- **原文**:

> - **Read-only tools**: tools that retrieve information (get, list, search). Lower risk and usually safe to pre-authorize.

- **日本語**: Read-only のツール: 情報を取ってくるだけ（get, list, search）。危険は低く、たいてい事前に許可してよい。
- **どう使っているか**: コネクタの関数を「Interactive」と「Read-only」の 2 群に分けて表示し、Read-only の事前許可（Always allow）を勧める。分け方の根拠（MCP の readOnlyHint か、名前か、Mistral の手作業か）は書かれていない（不明）。
- **条件**: Always allow のトグルは関数ごと（利用者ごとか組織ごとかはページに書かれていない）。既定では外部システムに触れる操作は確認。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、54 行（# Safety and approvals）（取得 2026-10-02T22:11:27Z、sha256 d666f33e5341…）
- **補足**: 補助の照合: 『Before Work performs an action that touches an external system, it **stops and asks for your approval**. This applies to anything that creates, modifies, sends, posts, or deletes.』も exact（L14（直前の Markdown 見出し: # Safety and approvals））。旧 URL https://docs.mistral.ai/le-chat/knowledge-integrations/connectors は https://docs.mistral.ai/vibe/work/connectors に転送される。ページに readOnlyHint / destructiveHint / annotations は none。 conditions の「利用者ごと」はページに無い（ページは関数ごとのトグルとだけ書く）ので直した。

### Mistral AI — Mistral Studio（API）Connectors — 人の確認

<a id="g-g2-closed-clients-missing-27"></a>
#### G2CCM-27 Mistral AI — Mistral Studio（API）Connectors — 人の確認

- **資料**: Human-in-the-loop | Mistral Docs (Studio Connectors)（公式の文書）
- **URL**: https://docs.mistral.ai/studio/connectors/confirmation
- **照らし合わせた中身の URL**: https://docs.mistral.ai/studio/connectors/confirmation.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: L22（直前の Markdown 見出し: # Human-in-the-loop）
- **原文**:

> Add `requires_confirmation` to the `tool_configuration` of any Connector or built-in tool, and list the tool names that require approval:

- **日本語**: コネクタや組み込みツールの tool_configuration に requires_confirmation を足し、承認が要るツールの名前を並べる。
- **どう使っているか**: API での確認の要否は、開発者がツール名で明示する。MCP の注釈から自動では決めない（ページに readOnlyHint / annotations は none）。
- **条件**: Conversations API でコネクタを使うとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、22 行（# Human-in-the-loop）（取得 2026-10-02T22:11:26Z、sha256 faf909aab5bf…）
- **補足**: conversations.md も「requires_confirmation」だけを案内（L236）。

### Mistral AI — Mistral Studio（API）Connectors — ツール一覧 API

<a id="g-g2-closed-clients-missing-28"></a>
#### G2CCM-28 Mistral AI — Mistral Studio（API）Connectors — ツール一覧 API

- **資料**: Managing Connectors | Mistral Docs（公式の文書）
- **URL**: https://docs.mistral.ai/studio/connectors/management
- **照らし合わせた中身の URL**: https://docs.mistral.ai/studio/connectors/management.md
- **版**: 2026-10-02 取得（.md 版）
- **書いてある場所**: L460（直前の Markdown 見出し: # With pretty output (simplified schema with only name, description, and inputSchema)）
- **原文**:

> | `pretty` | `false` | Return a simplified payload with only `name`, `description`, `annotations`, and a compact `inputSchema`. |

- **日本語**: pretty=true にすると、name・description・annotations・小さくした inputSchema だけの簡略版を返す。
- **どう使っているか**: コネクタのツール一覧 API は MCP サーバーの annotations をそのまま返す（簡略版でも残す）。Studio 自身が承認に使うとは書かれていない。
- **条件**: GET /v1/connectors/{id}/tools。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、460 行（# With pretty output (simplified schema with only name, description, and inputSchema)）（取得 2026-10-02T22:11:25Z、sha256 96496d359341…）
- **補足**: —

### Perplexity — Perplexity Agent API — mcp ツール

<a id="g-g2-closed-clients-missing-29"></a>
#### G2CCM-29 Perplexity — Perplexity Agent API — mcp ツール

- **資料**: MCP - Perplexity (Agent API tools)（公式の文書）
- **URL**: https://docs.perplexity.ai/docs/agent-api/tools/mcp
- **書いてある見出しへ直接**: https://docs.perplexity.ai/docs/agent-api/tools/mcp#risks-and-safety
- **版**: 2026-10-02 取得
- **書いてある場所**: MCP > Risks and safety（#risks-and-safety）
- **原文**:

> Agent API does not support MCP approvals yet . Every MCP tool call auto-runs, so only connect MCP servers and expose tools that you trust to run without an approval step.

- **日本語**: Agent API はまだ MCP の承認に対応していない。MCP ツールの呼び出しはすべて自動で走るので、承認なしで走らせてよいと信頼できるサーバーとツールだけをつなぐこと。
- **どう使っているか**: 承認の仕組みそのものが無い。注釈の有無・値に関係なく全部素通しで実行。読み取り専用への絞り込みは利用者が allowed_tools・読み取り専用トークン等で行う。
- **条件**: Agent API の mcp ツール（OpenAI Responses MCP 互換）。require_approval は無視される（同ページ Limitations の表）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「MCP > Risks and safety」（取得 2026-10-02T22:11:26Z、sha256 7f5e75fce1f6…）
- **補足**: 補助の照合: 『For servers with write or admin actions, prefer read-only server modes, read-only tokens, or a small allowlist of read-only tools.』も exact（同じ節）。ページに readOnlyHint / destructiveHint は none（annotations は応答例の別物だけ）。Perplexity の Mac アプリのローカル / リモート MCP（Help Center 11502712）は 403 で取れず不明。

### Zed Industries — Zed（ネイティブエージェント）— MCP ツールの種類

<a id="g-g2-closed-clients-missing-30"></a>
#### G2CCM-30 Zed Industries — Zed（ネイティブエージェント）— MCP ツールの種類

- **資料**: crates/agent/src/tools/context_server_registry.rs: ContextServerTool::kind（クライアントのソースコード）
- **URL**: https://github.com/zed-industries/zed/blob/c83abe7d0e060de08db386fbf86f7e95bfe6cb09/crates/agent/src/tools/context_server_registry.rs#L313-L315
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/zed-industries/zed/c83abe7d0e060de08db386fbf86f7e95bfe6cb09/crates/agent/src/tools/context_server_registry.rs
- **版**: commit c83abe7d0e060de08db386fbf86f7e95bfe6cb09（2026-10-02 の HEAD）
- **書いてある場所**: L313-315
- **原文**:

```
    fn kind(&self) -> acp::ToolKind {
        acp::ToolKind::Other
    }
```

- **日本語**: MCP（context server）のツールの種類は、注釈に関係なく常に Other（その他）。
- **どう使っているか**: Zed は ToolAnnotations を型として受け取る（crates/context_server/src/types.rs L541-557）が、エージェント側では使わない。readOnlyHint:true でも Read 種別にならない。
- **条件**: Zed 自身のエージェント（外部 ACP エージェントではない）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、313-315 行（取得 2026-10-02T22:11:37Z、sha256 7b18ef3ef9b9…）
- **補足**: crates/ 以下（context_server・agent・agent_ui・acp_thread・agent_settings・project を sparse checkout）で `.annotations` を読むのは listener.rs（Zed が MCP サーバーとして自分のツールに None を付ける側）だけ。C07 の「型定義と listener の 2 件」の照合結果。

### Zed Industries — Zed（ネイティブエージェント）— MCP ツールの承認

<a id="g-g2-closed-clients-missing-31"></a>
#### G2CCM-31 Zed Industries — Zed（ネイティブエージェント）— MCP ツールの承認

- **資料**: crates/agent/src/tools/context_server_registry.rs: ContextServerTool::run（クライアントのソースコード）
- **URL**: https://github.com/zed-industries/zed/blob/c83abe7d0e060de08db386fbf86f7e95bfe6cb09/crates/agent/src/tools/context_server_registry.rs#L350
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/zed-industries/zed/c83abe7d0e060de08db386fbf86f7e95bfe6cb09/crates/agent/src/tools/context_server_registry.rs
- **版**: c83abe7d
- **書いてある場所**: L350
- **原文**:

> event_stream.authorize_third_party_tool(initial_title, tool_id, display_name, cx);

- **日本語**: MCP ツールを走らせる前に、毎回「第三者ツールの承認」を求める（ツール ID と名前だけを渡す）。
- **どう使っているか**: 承認の要否は設定（tool_permissions の always_allow / always_deny と、承認画面の「Always for X MCP tool」）だけで決まり、注釈は渡されない。
- **条件**: authorize_third_party_tool（crates/agent/src/thread.rs L5810〜）の中で設定を見て、許可済みなら聞かない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、350 行（取得 2026-10-02T22:11:37Z、sha256 7b18ef3ef9b9…）
- **補足**: Zed の文書（zed.dev/docs/ai/mcp・tool-permissions）は注釈に触れない（C07 の checked_no_mention）。

### JetBrains — Junie（IDE プラグイン / CLI）— Action Allowlist

<a id="g-g2-closed-clients-missing-32"></a>
#### G2CCM-32 JetBrains — Junie（IDE プラグイン / CLI）— Action Allowlist

- **資料**: Action Allowlist | Junie Documentation（クライアントの文書）
- **URL**: https://junie.jetbrains.com/docs/action-allowlist.html
- **書いてある見出しへ直接**: https://junie.jetbrains.com/docs/action-allowlist.html#Action-Allowlist.md
- **版**: 2026-10-02 取得
- **書いてある場所**: Action Allowlist（#Action-Allowlist.md）
- **原文**:

> By default, Junie requires user approval for running terminal commands, MCP tools, and other types of actions that are considered to be sensitive by the coding agent.

- **日本語**: 既定では、Junie はターミナルコマンド、MCP ツール、そのほか危険とみなす操作の実行に、利用者の承認を求める。
- **どう使っているか**: MCP ツールは一律に承認対象。Allowlist の規則はツール名で書く。注釈による例外は書かれていない（readOnlyHint / destructiveHint / annotations は none）。
- **条件**: 既定。Always allow で Action Allowlist に入れれば以後は確認なし。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Action Allowlist」（取得 2026-10-02T22:11:28Z、sha256 99cae717159e…）
- **補足**: C07 は www.jetbrains.com/help/junie/action-allowlist.html を checked_no_mention に記録済み。こちらは新しい junie.jetbrains.com のページで、肯定の記述（MCP は既定で承認）を引用した。実装（JVM / 配布バイナリ）は調べていない。

### JetBrains — Junie CLI — Command approval

<a id="g-g2-closed-clients-missing-33"></a>
#### G2CCM-33 JetBrains — Junie CLI — Command approval

- **資料**: Quickstart | Junie Documentation（クライアントの文書）
- **URL**: https://junie.jetbrains.com/docs/junie-cli.html
- **書いてある見出しへ直接**: https://junie.jetbrains.com/docs/junie-cli.html#command-approval
- **版**: 2026-10-02 取得
- **書いてある場所**: Quickstart > Command approval（#command-approval）
- **原文**:

> For running potentially sensitive actions, such as executing most of the terminal commands, editing files outside the project, or invoking MCP tools, Junie CLI will ask for approval from the user.

- **日本語**: 危険になりうる操作（多くのターミナルコマンド、プロジェクト外のファイル編集、MCP ツールの呼び出し）では、Junie CLI は利用者に承認を求める。
- **どう使っているか**: MCP ツールの呼び出しは注釈に関係なく承認対象（ページに注釈の語は none）。
- **条件**: 既定。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Quickstart > Command approval」（取得 2026-10-02T22:11:29Z、sha256 b3d6b55bea92…）
- **補足**: npm の @jetbrains/junie（3110.7.0）はインストーラだけで本体のコードは含まない。

### Anthropic — Claude Code（CLI）2.1.287 — auto mode の許可判定（MCP サーバーポリシーの ask ルール）

<a id="g-g2-closed-clients-missing-34"></a>
#### G2CCM-34 Anthropic — Claude Code（CLI）2.1.287 — auto mode の許可判定（MCP サーバーポリシーの ask ルール）

- **資料**: 同バイナリ内の auto mode の許可判定（EVo 関数内、fallback_to_ask の条件）（クライアントのソースコード）
- **URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code-linux-x64/v/2.1.287
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/claude-code-linux-x64-2.1.287_claude）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 2.1.287
- **書いてある場所**: ファイル内の改行で区切った 1407058 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> Xt=nzn(_e.decisionReason)||_e.matchedAskRule?.source==="mcpServerPolicy",un=gVo(Xt,e,n,Ce),rn=Bt&&!qe&&!(Xt&&(!(e.isDestructive?.(n)??!1)||un))

- **日本語**: 確認の理由が mcpServerPolicy の ask ルール（Xt）で、ツールの isDestructive が偽（または機能フラグの un が真）なら、rn は偽になり、ask ルールによる確認の強制（fallback 理由 "ask_rule"）にはならない。
- **どう使っているか**: auto mode では、MCP サーバーポリシーの ask ルールで確認になった呼び出しでも、destructiveHint が true でなければ（false または欠落）確認を強制せず、auto mode の判定（分類器などの後段）に進める。destructiveHint:true のときだけ確認に戻す。欠落は false（02）なので、宣言の無いツールは確認が外れる側に入る。
- **条件**: auto mode（Aa: mode が auto、または auto が有効な plan）の分岐の中だけ。ルールの source が mcpServerPolicy の ask ルールのときだけ（利用者の settings の ask ルールなど、ほかの出どころの ask ルールは従来どおり確認になる）。後段の判定で許可されるかは分類器などしだい（ここでは自動承認とは言えない）。un（gVo）は機能フラグ（既定 false）で、立てば destructiveHint:true でも後段に進む。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い・危険度を付ける
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: 検証者が追加した項目。補助の照合（いずれも exact）: 『function nzn(e){return e?.type==="rule"&&e.rule.ruleBehavior==="ask"&&e.rule.source==="mcpServerPolicy"}』（1407060 行目）、『reason:b(ht||It?"safety_check":rn?"ask_rule":Qt?"plan_mode_floor":"org_ask_ceiling")』（1407058 行目、rn が真のとき確認に戻す理由名）、『alwaysAskRules:{...e.alwaysAskRules,...s.length>0&&{mcpServerPolicy:s}}』（1396797 行目。scope が dynamic のサーバー設定から mcpServerPolicy の ask ルールを作る関数 jYo）。利用統計には mcpServerAskOverride として un が載る（目視）。npm @anthropic-ai/claude-code-linux-x64@2.1.287（tarball https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.287.tgz, shasum 06e41844f998ce7cb51ac61b12b209fafe6e5528, integrity sha512-Q31ekN28viVjgfDuZKXUR5vxIBgUYoLGe+cRmjx/f01omqFDMi6IrgmcK5pWMnRbu/cjsTA/zO+bVES5oY3XUg==）を展開した Bun コンパイル済みバイナリ package/claude（244,317,368 bytes, sha256 3920489a5109cff5…）。unpkg は 500（大きすぎ）で直接取れないので、展開したファイルを 127.0.0.1:8765 で配信して verify_quote.py にかけた（fetched_url はその一時 URL。学生は tarball を取って `grep -a` で再現できる）。JS バンドルが平文で埋め込まれている。ミニファイ名（U, X, FVo など）は版ごとに変わる。 検証者が追加。02・08 の「isDestructive は機能フラグつきの経路だけ」という記述への反証として、既定経路で destructiveHint（欠落 = false）を使う箇所を照合した。

### Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（reads モード）による確認の省略

<a id="g-g2-closed-clients-missing-35"></a>
#### G2CCM-35 Cursor (Anysphere) — Cursor 3.23.12 — 管理者の MCP 許可リスト（reads モード）による確認の省略

- **資料**: extensions/cursor-agent-exec/dist/main.js: permissions-service の isMcpInTeamAllowlist / shouldBlockMcp（クライアントのソースコード）
- **URL**: https://downloads.cursor.com/production/2d29876d567da1607532b23bbf2cd5ddbca496fe/linux/x64/deb/amd64/deb/cursor_3.23.12_amd64.deb
- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL （http://127.0.0.1:8765/cursor-3.23.12_cursor-agent-exec_main.js）で配って照らし合わせた。配布物の取り方は「補足」を見る。
- **版**: 3.23.12
- **書いてある場所**: ファイル内の改行で区切った 5 行目（tool の lines 値。ミニファイ済み / バイナリなので行番号は目安）
- **原文**:

> const s=this.findTeamMcpServerPolicy(e,t);return void 0!==s&&"reads"===s.mode&&(0,rc.rh)(s,{name:r,annotations:n})

- **日本語**: サーバーに当たるチームのポリシーが "reads" モードなら、ツールの注釈が declared_read（readOnlyHint:true かつ destructiveHint が true でない）のときに「チームの許可リストに入っている」とする。
- **どう使っているか**: チームの MCP ツール制御が有効で、サーバーの toolAllowlistMode が "reads" なら、declared_read の MCP ツールは shouldBlockMcp で「ALLOWED (in admin MCP allowlist)」となり、承認なしで走る。注釈の無いツールは許可リスト外で、ワークベンチ側では disabledByAdmin（12・13）。宣言の真偽は確かめない。
- **条件**: チームの管理者設定 allowedMcpConfiguration があり、getMcpToolControls が enabled を返すとき（このときは利用者自身の allow リストではなくチームの許可リストを見る）。explicit deny（利用者の deny）が先に効く。Smart mode の経路でも同じ isMcpInTeamAllowlist で承認要否を決める。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。
- **補足**: 検証者が追加した項目。補助の照合（いずれも exact、5 行目）: 『shouldBlockMcp: ALLOWED (in admin MCP allowlist)』、『case"reads":return(0,n.NY)(t.annotations)』、『function i(e){return void 0!==e&&(!0!==e.destructiveHint&&!0===e.readOnlyHint)}』（NY の定義）。getMcpToolControls が管理者設定から {enabled:!0, mcpToolAllowlist, serverPolicies} を作ることは目視。同じ関数で、"all" モードのサーバーは `<server>:*` が許可リストに入り、全ツールが注釈に関係なく承認なしになる（目視）。 検証者の独立確認（2026-10-02）: 配布物を配布元から取り直して展開し、照合した各ファイルの sha256 が発見者の値と一致した（Claude Code: npm tarball の sha1 06e41844… が npm の shasum と一致、package/claude の sha256 3920489a5109…。Cursor: downloads.cursor.com の .deb（207,998,356 bytes）から workbench.desktop.main.js 87cd7ca0b620… / cursor-agent-exec main.js 9703f940d086…、product.json の commit は 2d29876d…96f0（ダウンロード URL の 96fe とは末尾が違う）。Devin: tarball sha256 98e394baeefc8755…、devin 460e37d44673…、`devin --version` = devin 3000.10.48 (fcf7ba39)。Antigravity: language_server_linux_x64 4b23f0a2949f…、product.json ideVersion 1.23.2）。 検証者が追加。12 の reads モードが「無効化」だけでなく「宣言 read のツールの自動実行」にも使われることを照合した。

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP（in-process サーバー）

<a id="g-g3-asia-agents-01"></a>
#### G3AA-01 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP（in-process サーバー）

- **資料**: MCP Integration — Annotations Actually Consumed（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#annotations-actually-consumed
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed (#annotations-actually-consumed)
- **原文**:

> Read-only tools can run concurrently (no mutual blocking within a batch); the TUI tool details render a [read-only] badge

- **日本語**: 読み取り専用のツールは並行して実行できる（同じ回の呼び出しの中でたがいに待たない）。TUI のツール詳細に [read-only] の印が出る。
- **どう使っているか**: readOnlyHint: true のツールは同じ回のツール呼び出しの中で並行実行の対象になり、TUI に [read-only] の印が出る。ホストには MCP の状態問い合わせで annotations.readOnly（Hint を外した名前）として返る。承認には使わない（04）。
- **条件**: SDK の in-process MCP サーバー（createSdkMcpServer / @tool）の文書。外部 MCP サーバーについてはこのページには書かれていないが、qodercli 1.1.65 のコードでは外部 MCP ツールの発見時にも readOnlyHint===true を読み取り専用の値として持ち（15）、ツールの基底クラスが『isConcurrencySafe(A){return this.isReadOnly}』、MCP ツールのクラスが『get isReadOnly(){return void 0!==this._isReadOnly?this._isReadOnly:super.isReadOnly}』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:34Z sha256=fbb5ea617e68、L14）なので、外部 MCP ツールでも readOnlyHint: true は並行実行の可否に効く。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・表示（印・名前）・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）
- **補足**: 表の 1 行目。表の列名 'Host-side reads as' は annotations.readOnly。 conditions の『外部 MCP には分からない』を、コードで並行実行の経路を確かめた結果に置き換えた。

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

<a id="g-g3-asia-agents-02"></a>
#### G3AA-02 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

- **資料**: MCP Integration — Annotations Actually Consumed（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#annotations-actually-consumed
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed (#annotations-actually-consumed)
- **原文**:

> Declares the tool performs destructive operations. The TUI renders a [destructive] badge in tool details

- **日本語**: ツールが破壊的な操作をすると宣言する。TUI のツール詳細に [destructive] の印が出る。
- **どう使っているか**: destructiveHint: true は TUI の [destructive] の印だけ。ホストには annotations.destructive として返る。確認を増やす・止める働きはない（04・11）。
- **条件**: SDK の in-process MCP サーバーの文書。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 表示（印・名前）・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）

<a id="g-g3-asia-agents-03"></a>
#### G3AA-03 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

- **資料**: MCP Integration — Annotations Actually Consumed（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#annotations-actually-consumed
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed (#annotations-actually-consumed)
- **原文**:

> Declares the tool reaches the outside world (web search, third-party APIs). The TUI tool details render an [open-world] badge

- **日本語**: ツールが外の世界（Web 検索、他社の API）に届くと宣言する。TUI のツール詳細に [open-world] の印が出る。
- **どう使っているか**: openWorldHint: true は TUI の [open-world] の印だけ。ホストには annotations.openWorld として返る。
- **条件**: SDK の in-process MCP サーバーの文書。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 表示（印・名前）・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）

<a id="g-g3-asia-agents-04"></a>
#### G3AA-04 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

- **資料**: MCP Integration — Annotations Actually Consumed（警告の段落）（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#annotations-actually-consumed
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed (#annotations-actually-consumed)
- **原文**:

> These three fields do not affect auto-mode permission decisions. The CLI treats server-declared annotations as unverifiable hints (servers can freely under-/over-declare) and keeps them out of the permission pipeline to avoid endorsing self-description.

- **日本語**: この 3 つの欄は auto モードの許可の判断に影響しない。CLI はサーバーが自分で宣言した注釈を確かめようのないヒントとして扱い（サーバーは少なくも多くも自由に宣言できる）、自己申告を裏書きしないように、許可の判断の流れには入れない。
- **どう使っているか**: 注釈を許可の判断から意図して外していると明言する一次資料。理由は「サーバーの自己申告は検証できない（過少・過大申告が自由）ので裏書きしない」。強制的に拒否したいときはツールの許可リストか hooks を使え、注釈はホスト側の識別と TUI 表示だけ、と続く。
- **条件**: 対象は auto モードの許可判断（permission pipeline）。並行実行（01）と表示（02・03）には使う。qodercli 本体の auto モード分類器の入力にも注釈が入っていないことをコード（13）で確かめた。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 使わない・読まない・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）
- **補足**: AuthGap の主張（宣言は未検証の自己申告）と同じ立場をクライアント側が文書で取っている珍しい例。同じ文は Qoder CN（中国版）の文書にもある（12）。ただし同じ SDK の Tools ページ（07）は『permissions にも使いうる』と書いており、文書の間で揺れがある。

<a id="g-g3-asia-agents-05"></a>
#### G3AA-05 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

- **資料**: MCP Integration — Annotations Actually Consumed（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#annotations-actually-consumed
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed (#annotations-actually-consumed)
- **原文**:

> idempotentHint and title are currently not consumed by the SDK—passing them won't error, but the SDK neither consumes nor echoes them to the host.

- **日本語**: idempotentHint と title は今は SDK が使わない。渡してもエラーにはならないが、SDK は使わず、ホストにも返さない。
- **どう使っているか**: idempotentHint と title は受け取るだけで捨てる（ホストの状態問い合わせにも出ない）。必要ならアプリ側で対応表を持て、と続く。
- **条件**: Qoder Agent SDK の現在版（2026-10-02 取得時点）。
- **扱う宣言**: idempotentHint・title ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > In-Process Server (Recommended) > Full signatures > Annotations Actually Consumed」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）
- **補足**: Python の参照にも『idempotentHint is not currently echoed in the status tool list.』とある（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:49:58Z sha256=04f9e3001b4b、https://docs.qoder.com/cli/sdk/references-python#mcp-status-tool-information）。 notes の Python 参照の補足を検証して『未照合』を外した。

<a id="g-g3-asia-agents-06"></a>
#### G3AA-06 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI / Qoder Agent SDK — SDK MCP

- **資料**: MCP Integration — Best Practices（4 番）（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/mcp#best-practices
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: MCP Integration > Best Practices (#best-practices)
- **原文**:

> Prefer read-only + readOnlyHint: be careful with writes; pair them with the permission callback or hooks for double confirmation.

- **日本語**: 読み取り専用＋readOnlyHint を優先する。書き込みは慎重に。書き込みには許可のコールバックか hooks を組み合わせて二重に確認する。
- **どう使っているか**: ツールを書く人への指針。読み取りのツールには readOnlyHint を付け、書き込みは注釈ではなく許可コールバック・hooks で確認せよ、という分担。
- **条件**: SDK の in-process ツールを書く人向け。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Integration > Best Practices」（取得 2026-10-02T22:11:28Z、sha256 5ddc6680c35e…）

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール）

<a id="g-g3-asia-agents-07"></a>
#### G3AA-07 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール）

- **資料**: Tools — Configure Tool Metadata（annotations の説明）（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/tools
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/tools#configure-tool-metadata
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: Tools > Custom Tool Integration Steps > Step 1: Create the tool > Configure Tool Metadata (#configure-tool-metadata)
- **原文**:

> annotations carry MCP tool annotations. The SDK puts them on the MCP tool definition, and the CLI can use them for scheduling, permissions, or status display.

- **日本語**: annotations は MCP のツール注釈を運ぶ。SDK はそれを MCP のツール定義に載せ、CLI はスケジューリング、許可、状態表示に使える。
- **どう使っているか**: SDK は注釈をツール定義にそのまま載せる。『許可（permissions）にも使える』と書くが、同じ SDK の MCP ページ（04）は『auto モードの許可判断には入れない』と書いており、食い違う。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Custom Tool Integration Steps > Step 1: Create the tool > Configure Tool Metadata」（取得 2026-10-02T22:11:29Z、sha256 d60256b511af…）
- **補足**: 文書間の不一致。同じページの別の段（08・09）は『注釈は許可設定の代わりにならない』『readOnlyHint は許可のスイッチではない』と書くので、全体としては許可に使わない側に寄る。どちらが実装どおりかは、auto モードの分類器の入力（13）からは 04 が正しいとみられるが、ほかの許可の段（allow/deny 規則など）で注釈を読む箇所が無いかは未照合（不明）。 verify_quote.py は見出しを『Configure Input Parameters』と返したが、取得した HTML（RSC のデータ）では引用の段落は h4『Configure Tool Metadata』（id=configure-tool-metadata）の直後にあり、ページの表示上もこの見出しの下。道具の見出し割り当ての誤りとみて location / anchored_url を直した。

<a id="g-g3-asia-agents-08"></a>
#### G3AA-08 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール）

- **資料**: Tools — Configure Tool Metadata（表の注）（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/tools
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/tools#configure-tool-metadata
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: Tools > Custom Tool Integration Steps > Step 1: Create the tool > Configure Tool Metadata (#configure-tool-metadata)
- **原文**:

> Note: these fields do not replace permission configuration. Whether a tool may run is still decided by tools, allow/deny rules, the permission mode, the permission callback, and hooks.

- **日本語**: 注意: これらの欄は許可の設定の代わりにならない。ツールを走らせてよいかは、tools、allow/deny 規則、許可モード、許可コールバック、hooks で決まる。
- **どう使っているか**: 注釈（title・readOnlyHint・destructiveHint・openWorldHint）では実行の可否は決まらない、と明記。
- **扱う宣言**: title・readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Custom Tool Integration Steps > Step 1: Create the tool > Configure Tool Metadata」（取得 2026-10-02T22:11:29Z、sha256 d60256b511af…）
- **補足**: 状態問い合わせでは readOnly / destructive / openWorld という CLI 側の名前で返ることも同じ段に書かれている。

<a id="g-g3-asia-agents-09"></a>
#### G3AA-09 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — Tools（カスタムツール）

- **資料**: Tools — Common Pitfalls（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/tools
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/tools#common-pitfalls
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: Tools > Common Pitfalls (#common-pitfalls)
- **原文**:

> readOnlyHint is tool metadata and a scheduling hint, not a permission switch. Whether execution is allowed is still determined by permission configuration.

- **日本語**: readOnlyHint はツールのメタデータで、スケジューリングのヒントであり、許可のスイッチではない。実行してよいかは許可の設定で決まる。
- **どう使っているか**: ツール作者向けの『Common Pitfalls（よくある落とし穴）』の節で、readOnlyHint はメタデータとスケジューリングのヒントであって許可のスイッチではない、実行の可否は許可の設定で決まると注意する。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tools > Common Pitfalls」（取得 2026-10-02T22:11:29Z、sha256 d60256b511af…）
- **補足**: usage_ja が原文に無い言い回し（『readOnlyHint を付ければ承認が要らなくなる』）を引用符で示していたので、原文どおりの説明に直した。

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — TypeScript 参照

<a id="g-g3-asia-agents-10"></a>
#### G3AA-10 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — TypeScript 参照

- **資料**: SDK References - TypeScript — ToolAnnotations（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/references-typescript
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/references-typescript#toolannotations
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: SDK References - TypeScript > Types > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> Current observable effect: read-only tools can be eligible for concurrent execution within the same batch of tool calls; this is not a permission switch

- **日本語**: 今見える効果: 読み取り専用のツールは同じ回のツール呼び出しの中で並行実行の対象になりうる。許可のスイッチではない。
- **どう使っているか**: 型の参照でも、readOnlyHint の今見える効果は『同じ回のツール呼び出しの中で並行実行の対象になりうる』ことで、許可のスイッチではないと書く。TS の ToolAnnotations 型には idempotentHint が無い（title・readOnlyHint・destructiveHint・openWorldHint の 4 つ）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「SDK References - TypeScript > Types > tool() > ToolAnnotations」（取得 2026-10-02T22:11:33Z、sha256 521666693a3e…）
- **補足**: Python の参照（references-python#toolannotations）も同じ趣旨: 『The observable effect today is that read-only tools are eligible for concurrent execution』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:49:58Z sha256=04f9e3001b4b、https://docs.qoder.com/cli/sdk/references-python#toolannotations）。表の直後の段に『These fields are metadata and scheduling hints, not permission switches.』とも書かれている。 usage_ja の『並行実行だけ』を原文の『can be eligible』に合わせて弱めた。notes の Python 参照を検証して『未照合』を外した。

<a id="g-g3-asia-agents-11"></a>
#### G3AA-11 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder Agent SDK — TypeScript 参照

- **資料**: SDK References - TypeScript — ToolAnnotations（destructiveHint の行）（SDK の文書）
- **URL**: https://docs.qoder.com/cli/sdk/references-typescript
- **書いてある見出しへ直接**: https://docs.qoder.com/cli/sdk/references-typescript#toolannotations
- **版**: docs.qoder.com（Mintlify）。2026-10-02 取得
- **書いてある場所**: SDK References - TypeScript > Types > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> Risk metadata; currently does not automatically block an authorized tool execution

- **日本語**: 危険度のメタデータ。今は、許可されたツールの実行を自動で止めることはない。
- **どう使っているか**: destructiveHint: true でも、すでに許可されている実行は止まらない。openWorldHint の行も『External-interaction metadata; currently does not automatically block an authorized tool execution』と同じ趣旨。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「SDK References - TypeScript > Types > tool() > ToolAnnotations」（取得 2026-10-02T22:11:33Z、sha256 521666693a3e…）
- **補足**: 引用は destructiveHint の行。表の openWorldHint の行は同じ語句を含むので count=1 はこの行だけを指す（openWorldHint の行の文は『External-interaction metadata; ...』で始まる）。

### Alibaba Cloud（Qoder CN。旧 通義灵码 Lingma の中国版） — Qoder CLI CN / Qoder Agent SDK — SDK MCP（中国語版）

<a id="g-g3-asia-agents-12"></a>
#### G3AA-12 Alibaba Cloud（Qoder CN。旧 通義灵码 Lingma の中国版） — Qoder CLI CN / Qoder Agent SDK — SDK MCP（中国語版）

- **資料**: MCP 集成 — annotations 实际支持（SDK の文書）
- **URL**: https://docs.qoder.cn/cli/sdk/mcp
- **書いてある見出しへ直接**: https://docs.qoder.cn/cli/sdk/mcp#annotations-实际支持
- **版**: docs.qoder.cn。2026-10-02 取得
- **書いてある場所**: MCP 集成 > In-Process Server（推荐） > 完整签名 > annotations 实际支持 (#annotations-实际支持)
- **原文**:

> 这三个字段不会影响 auto 模式的权限决策。CLI 把 server 自声明的 annotation 视为不可验证的提示信息（server 可以随意 under-/over-declare），不会把它们带进权限管线，以免变相替 server 的自我标榜背书。

- **日本語**: この 3 つの欄は auto モードの許可判断に影響しない。CLI はサーバーが自分で宣言した注釈を検証できないヒントとして扱い（サーバーは過少にも過大にも宣言できる）、許可の流れに入れない。サーバーの自己宣伝を間接的に裏書きしないためである。
- **どう使っているか**: 04 と同じ方針の中国語版。中国国内向けの Qoder CN（Lingma の改名後）でも、注釈を許可判断から外すと明言している。
- **条件**: auto モードの許可判断について。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 使わない・読まない・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP 集成 > In-Process Server（推荐） > 完整签名 > annotations 实际支持」（取得 2026-10-02T22:11:28Z、sha256 b3070328f3dc…）
- **補足**: help.aliyun.com の Qoder CN 系列の llms.txt（https://help.aliyun.com/zh/lingma/llms.txt）に『原通义灵码 Lingma 已更名。』とある（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:51:04Z sha256=c608dc4e733a、L10）。同じファイルの冒頭は『Qoder CN 系列（原灵码企业版）』。同じ節の表（並行実行・[read-only] などの印）と次の段落（idempotentHint・title を使わない旨）も英語版と同じ内容。 notes の llms.txt の所在が不正確（help.aliyun.com/llms.txt には無く、/zh/lingma/llms.txt にある）だったので URL を特定して検証した。HTML ページに対する『189〜191 行』『197 行』という行番号は意味を持たないので外した。

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— MCP ツールの auto モード分類器入力

<a id="g-g3-asia-agents-13"></a>
#### G3AA-13 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— MCP ツールの auto モード分類器入力

- **資料**: bundle/qodercli.js（minify 済み）— MCP ツールクラスの toClassifierInput（クライアントのソースコード）
- **URL**: https://unpkg.com/@qoder-ai/qodercli@1.1.65/bundle/qodercli.js
- **版**: npm @qoder-ai/qodercli@1.1.65（unpkg 経由、minify 済みバンドル 33 MB）
- **書いてある場所**: L14
- **原文**:

> toClassifierInput(A){let e;try{e=JSON.stringify(A).slice(0,2e3)}catch{e="[unserializable arguments]"}return{mcp_server:this.serverName,mcp_tool:this.serverToolName,description:this.description?.slice(0,500),arguments:e}}

- **日本語**: MCP ツールを分類器に渡すときの入力は、サーバー名・ツール名・説明（500 字まで）・引数（2000 字まで）だけ。
- **どう使っているか**: auto モードの分類器に渡る MCP ツールの情報に注釈が含まれない。04（『許可の流れに入れない』）をコードで裏づける。
- **条件**: auto モードの LLM 分類器への入力。同じクラスの isDestructive（destructiveHint===true）・isOpenWorld（openWorldHint===true）は、バンドルのテキスト検索では委譲用のラッパーと状態の返送（annotations.destructive / openWorld）からしか呼ばれておらず、許可の段（allow/deny 規則・hooks・許可モード）からの参照は見つからなかった。ただし minify 済みで名前が変わりうるので網羅ではない（不明として残す）。readOnlyHint の文字列はバンドル中 4 か所（MCP SDK の zod スキーマ、ツール発見、状態の返送）だけ。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、14 行（取得 2026-10-02T22:11:47Z、sha256 fbb5ea617e68…）
- **補足**: 1 行が非常に長い minify 済みコード。同じクラスに isDestructive（destructiveHint===true）・isOpenWorld（openWorldHint===true）もあるが、それらの呼び出し側が許可に効くかは未照合。 conditions に、分類器以外の段で注釈を読む箇所を検証者が追加で探した結果を足した（見つからず、網羅ではない）。

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— /mcp のツール一覧の印

<a id="g-g3-asia-agents-14"></a>
#### G3AA-14 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— /mcp のツール一覧の印

- **資料**: bundle/qodercli.js（minify 済み）— ツール一覧の印を作る関数（クライアントのソースコード）
- **URL**: https://unpkg.com/@qoder-ai/qodercli@1.1.65/bundle/qodercli.js
- **版**: npm @qoder-ai/qodercli@1.1.65（unpkg 経由）
- **書いてある場所**: L347
- **原文**:

> r=!0===n?.destructiveHint,o=!0===n?.openWorldHint;return i&&e.push("read-only"),r&&e.push("destructive"),o&&e.push("open-world"),e}

- **日本語**: destructiveHint が true、openWorldHint が true のとき、それぞれ『destructive』『open-world』の印を付ける（isReadOnly なら『read-only』）。
- **どう使っているか**: TUI（MCP のツール一覧）で read-only / destructive / open-world の印を付けるコード。文書 01〜03 の表示の記述を裏づける。
- **条件**: 値が厳密に true のときだけ印が付く（!0===...）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、347 行（取得 2026-10-02T22:11:47Z、sha256 fbb5ea617e68…）

### Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— 外部 MCP ツールの発見

<a id="g-g3-asia-agents-15"></a>
#### G3AA-15 Alibaba（Qoder。旧 Lingma の国際版の後継） — Qoder CLI（npm @qoder-ai/qodercli 1.1.65）— 外部 MCP ツールの発見

- **資料**: bundle/qodercli.js（minify 済み）— listTools の結果からツールを作る箇所（クライアントのソースコード）
- **URL**: https://unpkg.com/@qoder-ai/qodercli@1.1.65/bundle/qodercli.js
- **版**: npm @qoder-ai/qodercli@1.1.65（unpkg 経由）
- **書いてある場所**: L268
- **原文**:

> g=t.annotations,c=!0===g?.readOnlyHint

- **日本語**: ツールの annotations を取り出し、readOnlyHint が true かどうかを読み取り専用の印として持つ。
- **どう使っているか**: 外部 MCP サーバーのツールを発見するとき、readOnlyHint===true を読み取り専用の値としてツールに持たせる（注釈の残りも渡す）。この値は並行実行の可否（isConcurrencySafe）と TUI の印に使われる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、268 行（取得 2026-10-02T22:11:47Z、sha256 fbb5ea617e68…）
- **補足**: この読み取り専用の値は並行実行の判断につながる: 基底クラスの『isConcurrencySafe(A){return this.isReadOnly}』と MCP ツールクラスの『get isReadOnly(){return void 0!==this._isReadOnly?this._isReadOnly:super.isReadOnly}』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:34Z sha256=fbb5ea617e68、L14）。MCP ツールの kind は常に "other"。isReadOnly はバンドル中 13 か所で、並行実行・TUI の印・状態の返送にだけ使われ、許可の段からの参照はテキスト検索では見つからなかった（minify のため完全ではない）。 notes の『呼び出し側は未照合』を、isConcurrencySafe → isReadOnly の経路を確かめた結果に置き換えた（追加の引用 2 つを verify_quote.py で exact 確認）。

### Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review）

<a id="g-g3-asia-agents-16"></a>
#### G3AA-16 Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review）

- **資料**: dist-server/types/node/tools/tool-risk-review/protocol.d.ts — McpToolIdentity（クライアントのソースコード）
- **URL**: https://unpkg.com/@tencent-ai/codebuddy-code@2.161.1/dist-server/types/node/tools/tool-risk-review/protocol.d.ts
- **版**: npm @tencent-ai/codebuddy-code@2.161.1（unpkg 経由）
- **書いてある場所**: L27-31
- **原文**:

```
    annotations?: {
        readOnlyHint?: boolean;
        destructiveHint?: boolean;
        openWorldHint?: boolean;
    };
```

- **日本語**: MCP ツールの身元（McpToolIdentity）に、任意で annotations（readOnlyHint・destructiveHint・openWorldHint の 3 つ）を持つ。
- **どう使っているか**: 危険度レビュー（LLM のレビュー役）に渡す MCP ツールの身元の型に、注釈 3 つを入れる欄がある。idempotentHint と title は入らない。実装（17・18）では真偽値のものだけ写す。
- **条件**: モデル行動レビュー（modelBehaviorReviewEnabled）が有効なとき（既定は無効、18 の conditions）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、27-31 行（取得 2026-10-02T22:11:40Z、sha256 2af8bc0a4637…）
- **補足**: 型の宣言ファイル（.d.ts）。同じ型の hostConnectionId には『Host 配置的连接实例身份，不接受 MCP 返回值覆盖。』（ホストが設定した接続の身元で、MCP の返り値では上書きしない。verify_quote.py: match=exact count=1、L23）という注釈がある。 notes の hostConnectionId の注釈の引用を verify_quote.py で検証し（exact、L23）、その結果を書き添えた。

<a id="g-g3-asia-agents-17"></a>
#### G3AA-17 Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review）

- **資料**: dist/codebuddy.js（minify 済み）— mcp_projector_effectTags（クライアントのソースコード）
- **URL**: https://unpkg.com/@tencent-ai/codebuddy-code@2.161.1/dist/codebuddy.js
- **版**: npm @tencent-ai/codebuddy-code@2.161.1（unpkg 経由、minify 済み 25 MB）
- **書いてある場所**: L2412
- **原文**:

> function mcp_projector_effectTags(eA){let el=eA.annotations?.openWorldHint===!0?["network_access"]:[];

- **日本語**: ツールの注釈で openWorldHint が true なら、効果の札に『network_access』を付ける。そうでなければ札なし。
- **どう使っているか**: LLM レビュー役に渡す『行為の写像』で、openWorldHint===true の MCP ツールに network_access の効果札を付ける。readOnlyHint・destructiveHint からは札を作らない（そのまま注釈として渡すだけ、18）。
- **条件**: モデル行動レビューが有効なとき（既定は無効、18）。特定の 2 ツール（agent_mail_upload_attachment・workbuddy_sites_deploy、接続 connector-proxy）には data_egress も付く（注釈とは無関係）。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、2412 行（## Verification）（取得 2026-10-02T22:12:08Z、sha256 2ffc5ebdd24c…）
- **補足**: 組み込みツールでは WebFetch / WebSearch に network_access と data_egress を付ける（『createToolActionProjection("WebFetch",["network_access","data_egress"]』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=2ffc5ebdd24c、L2412）。openWorldHint の MCP ツールは組み込みの Web 取得と同じ『ネットワーク到達』の札になる（data_egress は付かない）。openWorldHint が false・未指定なら札は無く、readOnlyHint・destructiveHint は札にならない。札は LLM レビュー役への入力で、レビューは承認を外さない（18）。 notes の WebFetch / WebSearch の札の主張を検証した引用を足し、レビューが承認を外さないこと（18）への参照を足した。

<a id="g-g3-asia-agents-18"></a>
#### G3AA-18 Tencent（腾讯云 CodeBuddy） — CodeBuddy Code（npm @tencent-ai/codebuddy-code 2.161.1）— ツール危険度レビュー（tool-risk-review）

- **資料**: dist/codebuddy.js（minify 済み）— projectMcpToolAction（クライアントのソースコード）
- **URL**: https://unpkg.com/@tencent-ai/codebuddy-code@2.161.1/dist/codebuddy.js
- **版**: npm @tencent-ai/codebuddy-code@2.161.1（unpkg 経由）
- **書いてある場所**: L2412
- **原文**:

> classifierInput:"Review the bounded MCP action evidence in mcpEvidence.",mcpEvidence:{hostConnectionId:eA.identity.hostConnectionId,serverName:eA.identity.serverName,annotations:eg,parameters:el}

- **日本語**: 分類器への入力は『mcpEvidence の中の、上限付きの MCP 行為の証拠を見よ』で、mcpEvidence には接続の身元・サーバー名・注釈・引数（上限付き）が入る。
- **どう使っているか**: モデル行動レビューが有効なとき、MCP ツール呼び出しを LLM のレビュー役に回す『行為の写像』に、サーバーが申告した注釈（真偽値のもの）をそのまま証拠として入れる。ただし reviewMcpPermission の戻り値は『return e_||"ask"===el.hostDisposition}』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=2ffc5ebdd24c、L2410）で、e_ は通常の承認要否（needsApproval か ask の下限）。つまりレビューは元々承認が要る呼び出しの承認を外さず、元々許可される呼び出しに ask を足すか、hostDisposition=deny で止めるだけ。注釈が影響しうるのは『許可される呼び出しを格上げするかどうか』で、注釈によって確認が省かれる道はこの関数には無い。レビュー役のプロンプトが注釈をどう扱うか（信用するか）は見つけられなかった（不明）。
- **条件**: モデル行動レビューの既定は無効: 同じファイルに『Object.freeze({modelBehaviorReviewEnabled:!1,riskContentProtectionEnabled:!1,assistedApprovalMode:"manual",sandboxAssistedApprovalMode:"manual"})』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=2ffc5ebdd24c、L910）。reviewMcpPermission は『if(!el||!ec||!el.isModelBehaviorReviewEnabled(em))return eg||eh;』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=2ffc5ebdd24c、L2410）で、無効なら通常の承認要否（needsApproval か ask の下限）に戻る。子セッション・チーム・バックグラウンドでもレビューは走らない。deny 規則や hooks の拒否はレビューより先に効く。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 危険度を付ける・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、2412 行（## Verification）（取得 2026-10-02T22:12:08Z、sha256 2ffc5ebdd24c…）
- **補足**: 注釈の写し取りは createMcpToolIdentity（『..."boolean"==typeof ec?.readOnlyHint?{readOnlyHint:ec.readOnlyHint}:{}, ...』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=2ffc5ebdd24c、L2410）で、真偽値のものだけを写し、idempotentHint と title は落とす。CodeBuddy の公開文書（checked_no_mention）にはこの仕組みの注釈の記述は無い。 usage_ja の『LLM レビュー役が allow / block を判断する』は、レビューが承認を省きうるように読めて過大。周辺のコードを読み、戻り値が『基準の承認要否 OR レビューの ask』で、レビューは承認を外さない（足すか止めるだけ）ことを追記した。assistedApprovalMode（既定 manual）を変えたときの別経路は未照合。

### Moonshot AI — Kimi Code（MoonshotAI/kimi-code。TypeScript 版。旧 kimi-cli の後継）

<a id="g-g3-asia-agents-19"></a>
#### G3AA-19 Moonshot AI — Kimi Code（MoonshotAI/kimi-code。TypeScript 版。旧 kimi-cli の後継）

- **資料**: packages/agent-core-v2/src/mcpCore/client-shared.ts — toMcpToolDefinition（クライアントのソースコード）
- **URL**: https://github.com/MoonshotAI/kimi-code/blob/21406fb4c805cc8c715e6d1f16ad3fb5f25f4fe3/packages/agent-core-v2/src/mcpCore/client-shared.ts#L68-L74
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/MoonshotAI/kimi-code/21406fb4c805cc8c715e6d1f16ad3fb5f25f4fe3/packages/agent-core-v2/src/mcpCore/client-shared.ts
- **版**: commit 21406fb4c805cc8c715e6d1f16ad3fb5f25f4fe3
- **書いてある場所**: L68-74
- **原文**:

```
export function toMcpToolDefinition(tool: SdkListedTool): MCPToolDefinition {
  return {
    name: tool.name,
    description: tool.description ?? '',
    inputSchema: tool.inputSchema,
  };
}
```

- **日本語**: MCP の listTools の結果から、名前・説明・入力スキーマの 3 つだけを取り出してツール定義を作る。
- **どう使っているか**: MCP サーバーが申告した annotations は、ツール一覧を受け取った最初の段で捨てられる。型 MCPToolDefinition（types.ts L28-32）も name・description・inputSchema だけ。承認は名前の規則で決まる（mcp.ts の『approvalRule: qualifiedName』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:50:08Z sha256=cd5347d10f7e、L41）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、68-74 行（取得 2026-10-02T22:11:31Z、sha256 bfb4875594ec…）
- **補足**: リポジトリ全体（pinned clone）を readOnlyHint・destructiveHint・openWorldHint・idempotentHint で grep して 0 件（annotations の出現は OpenAI Responses の出力注釈など無関係のものだけ）。文書側の否定は checked_no_mention を参照。旧 kimi-cli（Python）は C07 で記載なしと記録済み。 検証者の確認: toMcpToolDefinition は stdio / http / sse の 3 つのクライアント（client-stdio.ts L113、client-http.ts L105、client-sse.ts L105）の listTools の結果すべてに使われる。 toMcpToolDefinition が 3 種のクライアントすべての listTools に使われることを pinned clone で確かめて notes に足した。approvalRule の引用は再検証で L41。

### iFlow（iflow-ai。Alibaba 系の心流） — iFlow CLI（npm @iflow-ai/iflow-cli 0.5.19。Gemini CLI 系）

<a id="g-g3-asia-agents-20"></a>
#### G3AA-20 iFlow（iflow-ai。Alibaba 系の心流） — iFlow CLI（npm @iflow-ai/iflow-cli 0.5.19。Gemini CLI 系）

- **資料**: bundle/iflow.js（minify 済み）— MCP ツールクラスの shouldConfirmExecute（クライアントのソースコード）
- **URL**: https://unpkg.com/@iflow-ai/iflow-cli@0.5.19/bundle/iflow.js
- **版**: npm @iflow-ai/iflow-cli@0.5.19（unpkg 経由、minify 済み 14 MB）
- **書いてある場所**: L1061
- **原文**:

> async shouldConfirmExecute(e,r){let n=this.serverName,o=`${this.serverName}.${this.serverToolName}`;return this.trust||t.allowlist.has(n)||t.allowlist.has(o)?!1:{type:"mcp"

- **日本語**: MCP ツールの実行前確認は、サーバーが trust のとき、またはサーバー名かサーバー名.ツール名が許可リストにあるときだけ省く。それ以外は確認を出す。
- **どう使っているか**: 確認の要否は trust 設定と、その場で『常に許可』を選んで入るリストだけで決まり、注釈は見ない。MCP ツールの種別は常に Other（『super(c??B2n(n),`${n} (${r} MCP Server)`,o,Mi.Hammer,Fi.Other,...)』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:43Z sha256=3bc5c8873d4e）。バンドル中の readOnlyHint は MCP SDK の zod スキーマ定義の 1 か所だけ。
- **条件**: mcpServers の trust: true（『`trust` (boolean, optional): Trust this server and bypass all tool call confirmations.』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:50:08Z sha256=d358442a3201、docs_en/configuration/settings.md L333）なら全ツールの確認を省く。--yolo はすべて自動承認。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、1061 行（# UNIT ${r} ${I$e(e.descriptor.unit)}`:"",a=`# TYPE ${r} ${PHo(e)}`,u="";switch(n){case Oq.DataPointType.SUM:case Oq.DataPointType.GAUGE:{u=e.dataPoints.map(c=>this._serializeSingularDataPoint(r,e,c)).join("");break}case Oq.DataPointType.HISTOGRAM:{u=e.dataPoints.map(c=>this._serializeHistogramDataPoint(r,e,c)).join("");break}default:RHo.diag.error(`Unrecognizable DataPointType: ${n} for metric "${r}"`)}return`${o}${s}）（取得 2026-10-02T22:11:39Z、sha256 3bc5c8873d4e…）
- **補足**: iflow-ai/iflow-cli の GitHub リポジトリ（commit 4642808afbc6580ac117d930f6c64ac0d84955c7）は文書とインストーラだけで、本体はバンドルで配布。文書にも注釈の記述は無い（checked_no_mention）。 文書（settings.md L304）の autoAccept は『Controls whether the CLI automatically accepts and executes tool calls that are considered safe (such as read-only operations) without requiring explicit user confirmation.』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:50:08Z sha256=d358442a3201）と書くが、バンドル 0.5.19 には autoAccept という文字列が無い（大文字小文字を無視した一致は showAutoAcceptIndicator の表示用 2 か所だけ）。設定が今も効くかは不明。いずれにしても MCP ツールの確認の要否に注釈は使われない。 notes の『autoAccept との関係は未照合』を調べ、文書の設定名がバンドルに見当たらないことを記録した。

### Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope。エージェント枠組み、MCP クライアントを含む）

<a id="g-g3-asia-agents-21"></a>
#### G3AA-21 Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope。エージェント枠組み、MCP クライアントを含む）

- **資料**: src/agentscope/tool/_adapters.py — MCP ツールのアダプタ（SDK のソースコード）
- **URL**: https://github.com/agentscope-ai/agentscope/blob/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/tool/_adapters.py#L271-L274
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agentscope-ai/agentscope/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/tool/_adapters.py
- **版**: commit 72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6
- **書いてある場所**: L271-274
- **原文**:

```
        # Extract is_read_only from MCP tool annotations
        self.is_read_only = False
        if tool.annotations and hasattr(tool.annotations, "readOnlyHint"):
            self.is_read_only = tool.annotations.readOnlyHint or False
```

- **日本語**: MCP ツールの注釈から is_read_only を取り出す。既定は False で、annotations に readOnlyHint があればその値（無ければ False）にする。
- **どう使っているか**: サーバーが申告した readOnlyHint をそのままツールの is_read_only にする。注釈が無い・readOnlyHint が None のときは False（読み取り専用ではない）扱い。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、271-274 行（# -*- coding: utf-8 -*-）（取得 2026-10-02T22:11:31Z、sha256 7db851e89e3c…）
- **補足**: この値が許可に直結する（22・23）。

### Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）

<a id="g-g3-asia-agents-22"></a>
#### G3AA-22 Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）

- **資料**: src/agentscope/tool/_adapters.py — MCP ツールの check_permissions（SDK のソースコード）
- **URL**: https://github.com/agentscope-ai/agentscope/blob/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/tool/_adapters.py#L307-L315
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agentscope-ai/agentscope/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/tool/_adapters.py
- **版**: commit 72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6
- **書いてある場所**: L307-315
- **原文**:

```
        if self.is_read_only:
            return PermissionDecision(
                behavior=PermissionBehavior.ALLOW,
                message="This is a read-only MCP tool. Allowing execution.",
            )
        return PermissionDecision(
            behavior=PermissionBehavior.ASK,
            message="MCP tools must be explicitly allowed by the user.",
        )
```

- **日本語**: 読み取り専用なら『読み取り専用の MCP ツールなので実行を許可』として ALLOW を返す。そうでなければ『MCP ツールは利用者が明示的に許可する必要がある』として ASK を返す。
- **どう使っているか**: readOnlyHint: true の MCP ツールは確認なしで許可、それ以外は確認を求める。サーバーの自己申告だけで承認を省く実装。
- **条件**: 許可エンジンでは deny 規則と ask 規則がこれより先に効く（23 の conditions）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、307-315 行（# -*- coding: utf-8 -*-）（取得 2026-10-02T22:11:31Z、sha256 7db851e89e3c…）
- **補足**: docstring は『Default implementation allows all operations.』と書くが、実際のコードは readOnly 以外 ASK で、docstring と食い違う。

### Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— 許可エンジン

<a id="g-g3-asia-agents-23"></a>
#### G3AA-23 Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— 許可エンジン

- **資料**: src/agentscope/permission/_engine.py — _check_read_only_fast_path（SDK のソースコード）
- **URL**: https://github.com/agentscope-ai/agentscope/blob/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/permission/_engine.py#L666-L667
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agentscope-ai/agentscope/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/permission/_engine.py
- **版**: commit 72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6
- **書いてある場所**: L666-667
- **原文**:

```
        A read-only invocation has no side effects, so it is auto-allowed
        in every :class:`PermissionMode`.
```

- **日本語**: 読み取り専用の呼び出しは副作用が無いので、どの許可モードでも自動で許可する。
- **どう使っているか**: tool.check_read_only()（既定は is_read_only を返す。MCP ツールでは readOnlyHint 由来）が True なら、すべての許可モードで ALLOW。readOnlyHint: true を申告した MCP ツールは、許可規則が無くても確認なしで走る。
- **条件**: 評価順は ACCEPT_EDITS の docstring で『1. Deny rules → DENY / 2. Ask rules → ASK (with suggestions) / 3. :meth:`ToolBase.check_read_only` → True → ALLOW (fast path)』（verify_quote.py: 3 行目は match=exact count=1 status=200 fetched_at=2026-10-02T21:44:44Z sha256=9142e0ecf173、L308-310）。つまり利用者が書いた deny / ask 規則は readOnlyHint より強い。EXPLORE モード（読み取りだけのモード）でも read-only は許可、それ以外は DENY（『ALLOW for read-only invocations, DENY otherwise.』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:44:44Z sha256=9142e0ecf173、L245）。この許可エンジンは既定のエージェントで使われる: agent/_agent.py の『self._engine = PermissionEngine(self.state.permission_context)』（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:50:09Z sha256=d91d264c21a0、L193）、既定の許可モードは『mode: PermissionMode = PermissionMode.DEFAULT』（permission/_context.py、verify_quote.py: match=exact count=1 sha256=7d1d09dfc6a5、L31）。middleware の on_check_permission で差し替えうる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、666-667 行（# -*- coding: utf-8 -*-）（取得 2026-10-02T22:11:32Z、sha256 9142e0ecf173…）
- **補足**: docstring によると、以前は DEFAULT と DONT_ASK に read-only の近道が無く、全モードにそろえた経緯がある。 conditions の EXPLORE の『未照合の補足』を検証した。許可エンジンが既定のエージェントで使われること・既定モードが DEFAULT であることを足した。

### Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— workspace のゲートウェイ経由ツール

<a id="g-g3-asia-agents-24"></a>
#### G3AA-24 Alibaba（Tongyi Lab / AgentScope） — AgentScope（agentscope-ai/agentscope）— workspace のゲートウェイ経由ツール

- **資料**: src/agentscope/workspace/_gateway_client.py — ゲートウェイ経由の MCP ツール（SDK のソースコード）
- **URL**: https://github.com/agentscope-ai/agentscope/blob/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/workspace/_gateway_client.py#L89-L90
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agentscope-ai/agentscope/72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6/src/agentscope/workspace/_gateway_client.py
- **版**: commit 72f3f6fa0b2fc38b8517f408ab616f0f2bd229e6
- **書いてある場所**: L89-90
- **原文**:

```
``annotations.readOnlyHint`` drives the permission
                policy.
```

- **日本語**: annotations.readOnlyHint が許可の方針を決める。
- **どう使っているか**: ゲートウェイから受け取った上流 MCP ツールでも、readOnlyHint が許可の方針を決めると docstring に明記。実装も L114-116 で is_read_only に写し、L129 で分岐する（アダプタと同じ形）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、89-90 行（# ── tool ───────────────────────────────────────────────────────────）（取得 2026-10-02T22:11:39Z、sha256 3bd37503c8db…）

### ByteDance（CloudWeGo） — Eino（cloudwego/eino-ext。Go のエージェント枠組みの MCP ツール部品 officialmcp）

<a id="g-g3-asia-agents-25"></a>
#### G3AA-25 ByteDance（CloudWeGo） — Eino（cloudwego/eino-ext。Go のエージェント枠組みの MCP ツール部品 officialmcp）

- **資料**: components/tool/mcp/officialmcp/mcp.go — ToolInfo.Extra への注釈の写し（SDK のソースコード）
- **URL**: https://github.com/cloudwego/eino-ext/blob/3603a39473c3e7b2aa3bfc11216487c94b8c7fd9/components/tool/mcp/officialmcp/mcp.go#L413-L415
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cloudwego/eino-ext/3603a39473c3e7b2aa3bfc11216487c94b8c7fd9/components/tool/mcp/officialmcp/mcp.go
- **版**: commit 3603a39473c3e7b2aa3bfc11216487c94b8c7fd9
- **書いてある場所**: L413-415
- **原文**:

```
	if t.Annotations != nil {
		extra[ExtraMCPAnnotations] = projectAnnotations(t.Annotations)
	}
```

- **日本語**: MCP ツールに注釈があれば、projectAnnotations で写した結果を extra の『mcp.annotations』に入れる。
- **どう使っているか**: この部品（officialmcp）は注釈を判断に使わず、アプリ側が読めるよう ToolInfo の Extra（キー mcp.annotations）に写すだけ。eino-ext のほかの箇所で mcp.annotations を読むところは無い（eino 本体のリポジトリは未照合）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、413-415 行（取得 2026-10-02T22:11:30Z、sha256 57fae68e1f77…）
- **補足**: projectAnnotations（L435-453）は Go SDK の型どおり、readOnlyHint と idempotentHint が bool（ポインタでない）なので true のときだけ入れる（『if a.IdempotentHint { ret["idempotentHint"] = a.IdempotentHint }』、verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:03:35Z sha256=57fae68e1f77、L440-442）。false と未指定が区別できず、写した先では『キーが無い』になる。destructiveHint と openWorldHint はポインタなので false も写る。 usage_ja の『枠組みは』を、確かめた範囲（eino-ext の officialmcp 部品）に絞った。

### ByteDance — DeerFlow（bytedance/deer-flow）— 同梱の業務連携 MCP サーバー（HubSpot など）

<a id="g-g3-asia-agents-26"></a>
#### G3AA-26 ByteDance — DeerFlow（bytedance/deer-flow）— 同梱の業務連携 MCP サーバー（HubSpot など）

- **資料**: backend/packages/harness/deerflow/capabilities/business.py（サーバのソースコード）
- **URL**: https://github.com/bytedance/deer-flow/blob/8cd7aef5789cfda758a83985e02edf8a63d6233f/backend/packages/harness/deerflow/capabilities/business.py#L156-L157
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/bytedance/deer-flow/8cd7aef5789cfda758a83985e02edf8a63d6233f/backend/packages/harness/deerflow/capabilities/business.py
- **版**: commit 8cd7aef5789cfda758a83985e02edf8a63d6233f
- **書いてある場所**: L156-157
- **原文**:

```
@server.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True))
        async def create_contact(
```

- **日本語**: HubSpot の連絡先を作るツールに、readOnlyHint=False・destructiveHint=False・idempotentHint=False・openWorldHint=True を付けている。
- **どう使っているか**: サーバー作者（ByteDance）が注釈を書いている実例。読み取りの get_companies には readOnlyHint=True, destructiveHint=False, openWorldHint=True（verify_quote.py: match=exact count=1 status=200 fetched_at=2026-10-02T21:03:36Z sha256=8208e08fc092、L151-152）、書き込みの create_contact / send_message には readOnlyHint=False, idempotentHint=False を明示し、説明文でも『不確かな書き込みを再試行しない』と書く。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、156-157 行（取得 2026-10-02T22:11:40Z、sha256 8208e08fc092…）
- **補足**: DeerFlow 側の MCP クライアント（deerflow/mcp/client.py）は注釈を読まない（checked_no_mention）。サーバー作者としての付け方の例であり、クライアントがそれを使う例ではない。

---

[← 付録 G-6 Google と AWS](appendix-g-6.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-8 エージェントの枠組み・利用者向けアプリ・モデルの API →](appendix-g-8.md)
