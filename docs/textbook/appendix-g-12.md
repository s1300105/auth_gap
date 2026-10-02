[← 付録 G-11 WebMCP](appendix-g-11.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-13 記載が無かったページと届かなかったページ →](appendix-g-13.md)

---

# 付録 G-12 研究論文・標準・安全の指針

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-12-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C10-01](#g-c10-research-standards-01) | Haseeb Mohammed Afsar（個人研究者） — 論文: What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead | 論文 | その他 | [確認] |
| [C10-02](#g-c10-research-standards-02) | Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent–Tool Boundary | 論文 | 信頼するなという注意・その他 | [確認] |
| [C10-03](#g-c10-research-standards-03) | Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（注釈のレジストリ全数調査） | 論文 | その他 | [確認] |
| [C10-04](#g-c10-research-standards-04) | Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（宣言と実装の差） | 論文 | その他 | [確認] |
| [C10-05](#g-c10-research-standards-05) | Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI: From Foundations to Systems | 論文 | 確認を省く（自動で許可） | [確認] |
| [C10-06](#g-c10-research-standards-06) | Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI | 論文 | 確認を求める | [確認] |
| [C10-07](#g-c10-research-standards-07) | Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI（承認ゲートの設計 Q&A） | 論文 | 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う | [未確認] |
| [C10-08](#g-c10-research-standards-08) | Lin-Fa Lee, Yi-Yu Chang, Chia-Mu Yu, Kuo-Hui Yeh — 論文: WebMCP Tool Surface Poisoning: Runtime Manipulation Attacks on LLM Agents | 論文 | その他 | [確認] |
| [C10-09](#g-c10-research-standards-09) | Aarya Doshi, Yining Hong, Congying Xu, Eunsuk Kang, Alexandros Kapravelos, Christian Kästner（CMU ほか） — 論文: Towards Verifiably Safe Tool Use for LLM Agents（ICSE-NIER 2026） | 論文 | 信頼するなという注意・その他 | [確認] |
| [C10-10](#g-c10-research-standards-10) | Microsoft Research（Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem ほか） — 論文: Securing AI Agents with Information-Flow Control（FIDES） | 論文 | 信頼するなという注意・その他 | [確認] |
| [C10-11](#g-c10-research-standards-11) | Weibo Zhao, Jiahao Liu, Bonan Ruan, Shaofei Li, Zhenkai Liang（NUS / PKU） — 論文: When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation | 論文 | 信頼するなという注意 | [確認] |
| [C10-12](#g-c10-research-standards-12) | Yang Shi, Jiaheng Fu, Yihe Huang, Ruixiang Wu, Chengyao Sun, Kaifeng Huang — 論文: Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions | 論文 | その他 | [確認] |
| [C10-13](#g-c10-research-standards-13) | Arpan Kumar Mahapatra — 論文: Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration: A Controlled Multi-Model Study | 論文 | 規則（ポリシー）の条件に使う・その他 | [確認] |
| [C10-14](#g-c10-research-standards-14) | OWASP（MCP Top 10 プロジェクト。寄稿: Spring AI Playground の保守者 Jemin Huh） — OWASP MCP Top 10 — Recommended Control: Client-Side Tool Risk Gating for MCP Hosts | 標準・指針 | 危険度を付ける・規則（ポリシー）の条件に使う・ツールを絞る・隠す | [確認] |
| [C10-15](#g-c10-research-standards-15) | OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（床規則と欠落時の扱い） | 標準・指針 | 危険度を付ける・宣言が無いときの扱い | [確認] |
| [C10-16](#g-c10-research-standards-16) | OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（限界: 注釈は指紋に入らない） | 標準・指針 | その他 | [確認] |
| [C10-17](#g-c10-research-standards-17) | Coalition for Secure AI（CoSAI, OASIS Open Project）Workstream 4 — CoSAI ホワイトペーパー: Model Context Protocol (MCP) Security | 標準・指針 | 信頼するなという注意 | [確認] |
| [C10-18](#g-c10-research-standards-18) | Stacklok（MCP レジストリ／ゲートウェイの事業者）。筆者は CEO の Craig McLuckie — Stacklok ブログ: Tool annotations are becoming the risk vocabulary for agentic systems | 第三者の記事 | 宣言を検査する・規則（ポリシー）の条件に使う・確認を省く（自動で許可） | [確認] |
| [C10-19](#g-c10-research-standards-19) | Alexander Sklar（個人ブログ。本人の紹介では Microsoft の Principal Software Engineer） — ブログ: MCP Tool Annotations Are Not Security | 第三者の記事 | 確認を求める・確認を省く（自動で許可）・信頼するなという注意 | [確認] |
| [C10-20](#g-c10-research-standards-20) | Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement（注釈を信用せず実行時に強制するプロキシ） | 第三者の記事 | 規則（ポリシー）の条件に使う・その他 | [確認] |
| [C10-21](#g-c10-research-standards-21) | Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement — MEASUREMENT-REPORT（静的検出の否定的結果） | 第三者の記事 | 宣言を検査する | [確認] |
| [C10-22](#g-c10-research-standards-22) | mcp-glimpse（CrankingAI、MIT ライセンスの OSS） — mcp-glimpse Learn: Tool annotations explained — and why so few tools declare them | 第三者の記事 | 宣言を検査する | [確認] |
| [G3SP-01](#g-g3-standards-protocols-01) | Model Context Protocol（Server Card WG。SEP 著者 David Soria Parra ほか） — SEP-2127 MCP Server Cards（Extensions Track、PR #2127 のヘッド） | 仕様 | 使わない・読まない・その他 | [確認] |
| [G3SP-02](#g-g3-standards-protocols-02) | Model Context Protocol（Server Card WG） — SEP-2127 MCP Server Cards（PR #2127 のヘッド） | 仕様 | 使わない・読まない・信頼するなという注意 | [確認] |
| [G3SP-03](#g-g3-standards-protocols-03) | Model Context Protocol（Server Card WG、experimental extension） — experimental-ext-server-card（Server Card の TypeScript スキーマ／README） | 仕様 | 使わない・読まない | [確認] |
| [G3SP-04](#g-g3-standards-protocols-04) | Model Context Protocol（Server Card WG） — experimental-ext-server-card — Roadmap Priorities | 仕様 | その他 | [確認] |
| [G3SP-05](#g-g3-standards-protocols-05) | Model Context Protocol（公式ブログ） — MCP blog: Exploring the Future of MCP Transports（2025-12-19） | 公式ブログ | その他 | [確認] |
| [G3SP-06](#g-g3-standards-protocols-06) | Agent Client Protocol（Zed Industries ほか。ACP） — ACP 仕様 v1 — Tool Calls | 仕様 | 表示（印・名前）・使わない・読まない | [確認] |
| [G3SP-07](#g-g3-standards-protocols-07) | Agent Client Protocol（ACP） — ACP 仕様 v1 — Tool Calls / session/request_permission | 仕様 | 使わない・読まない・その他 | [確認] |
| [G3SP-08](#g-g3-standards-protocols-08) | Agent Client Protocol（ACP。RFD 著者 @benbrandt） — ACP RFD: Tool Call Name | 仕様 | 表示（印・名前） | [確認] |
| [G3SP-09](#g-g3-standards-protocols-09) | A2A Project（Linux Foundation。旧 Google 発） — Agent2Agent (A2A) Protocol Specification | 仕様 | 確認を求める・その他 | [確認] |
| [G3SP-10](#g-g3-standards-protocols-10) | AGNTCY（Linux Foundation の Agent 基盤プロジェクト。Cisco 発） — OASF（Open Agentic Schema Framework）— mcp_server_tool オブジェクト | 仕様 | その他 | [確認] |
| [G3SP-11](#g-g3-standards-protocols-11) | IETF（Independent Submission。著者 M. Gaikwad） — Internet-Draft: Proxy Modes for Agent-Tool Protocols（draft-gaikwad-agent-proxy-modes-00） | 標準・指針 | 規則（ポリシー）の条件に使う・宣言が無いときの扱い | [確認] |
| [G3SP-12](#g-g3-standards-protocols-12) | IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP Aggregation Protocol (MCP-AX)（draft-abbott-mcp-ax-00） | 標準・指針 | その他 | [確認] |
| [G3SP-13](#g-g3-standards-protocols-13) | IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP-AX（draft-abbott-mcp-ax-00） | 標準・指針 | 確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [G3SP-14](#g-g3-standards-protocols-14) | IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: Implementing the NAIM Framework over the Model Context Protocol（draft-feng-nmop-naim-mcp-00） | 標準・指針 | 使わない・読まない・その他 | [確認] |
| [G3SP-15](#g-g3-standards-protocols-15) | IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: draft-feng-nmop-naim-mcp-00 | 標準・指針 | その他 | [確認] |
| [G3SP-16](#g-g3-standards-protocols-16) | IETF（個人 draft。J. Rosenberg（Five9）, C. Jennings（Cisco）） — Internet-Draft: Framework, Use Cases and Requirements for AI Agent Protocols（draft-rosenberg-ai-protocols-00） | 標準・指針 | 宣言を書くことを求める・確認を求める | [確認] |
| [G3SP-17](#g-g3-standards-protocols-17) | IETF（個人 draft。G. Zeng（Huawei）ほか） — Internet-Draft: MCP for Network Management: Problem Statement, Use Cases, and Requirements（draft-zeng-nmrg-mcp-usecases-requirements-00） | 標準・指針 | 確認を求める | [確認] |
| [G3SP-18](#g-g3-standards-protocols-18) | IETF（RFC Editor。HTTP WG、R. Fielding ほか） — RFC 9110 HTTP Semantics（STD 97） | 標準・指針 | 表示（印・名前）・その他 | [確認] |
| [G3SP-19](#g-g3-standards-protocols-19) | IETF（RFC Editor。HTTP WG） — RFC 9110 HTTP Semantics | 標準・指針 | 信頼するなという注意・その他 | [確認] |
| [G3SP-20](#g-g3-standards-protocols-20) | OpenAI — GPT Actions（OpenAPI 拡張 x-openai-isConsequential） | 公式の文書 | 宣言が無いときの扱い・確認を求める・その他 | [確認] |
| [G3SP-21](#g-g3-standards-protocols-21) | OpenTelemetry（GenAI SIG） — semantic-conventions-genai issue #373（Proposal: tool risk attributes for execute_tool and MCP tool call telemetry） | issue / PR / 提案の下書き | 危険度を付ける・その他 | [未確認] |

この分冊の資料は 43 件で、うち [確認] は 41 件、[確認（調査時のみ）] は 0 件。

<a id="ag-12-1"></a>
## 資料カード

### Haseeb Mohammed Afsar（個人研究者） — 論文: What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead

<a id="g-c10-research-standards-01"></a>
#### C10-01 Haseeb Mohammed Afsar（個人研究者） — 論文: What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead

- **資料**: arXiv:2609.10962v1 §5.2 Safety annotations（論文）
- **URL**: https://arxiv.org/html/2609.10962v1#S5.SS2
- **照らし合わせた中身の URL**: https://arxiv.org/html/2609.10962v1
- **版**: arXiv:2609.10962v1（2026-09-10 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead > 5 RQ2: what the servers that do run look like > 5.2 Safety annotations（HTML の節 id は S5.SS2）
- **原文**:

> Optional annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint) tell an agent whether a tool is safe to call before calling it. Of the 194 included servers advertising at least one tool, 72 annotate every tool and 122 annotate none. 1,626 of 2,766 tools (58.8%) carry no annotations.

- **日本語**: 任意の注釈（readOnlyHint, destructiveHint, idempotentHint, openWorldHint）は、ツールを呼ぶ前に安全に呼べるかをエージェントに伝えるもの。ツールを 1 つ以上出す 194 サーバーのうち、72 は全ツールに注釈を付け、122 はどのツールにも付けていない。2,766 ツール中 1,626（58.8%）に注釈が無い。
- **どう使っているか**: 使い方そのものではなく、野外で注釈がどれだけ欠けているかの測定。注釈の目的を『呼ぶ前に安全かを伝える』と書いたうえで、無作為抽出では 58.8% のツールが無宣言だと報告する（宣言が無い＝クライアントは既定値か名前などで判断するしかない状況がどれだけ多いか、の根拠）。
- **条件**: 分母: 公式 MCP Registry の全数調査（2026-08-22 スナップショット）のうち、npm で公開・stdio を宣言・active のサーバー 7,258 件を枠にした無作為抽出 400 件（seed 20260819）。そのうち initialize が完了した 195 サーバー（48.8%）、ツールを 1 つ以上出す 194 サーバーの 2,766 ツール（論文 Table 1・§5.2）。リモート（HTTP）サーバーや npm 以外のパッケージは枠の外。手作業で選んだ 24 サーバーの枠では無宣言率 41.5%（論文は『低い方の数字を生態系の率として引用するな』と書く）。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「What a Random Draw from the MCP Registry Contains, and What Tool-Use Benchmarks Contain Instead > 5 RQ2: what the servers that do run look like > 5.2 Safety annotations」（取得 2026-10-02T22:11:21Z、sha256 1102be6fa84f…）
- **補足**: 論文の数値は著者の測定で、私は再現していない（CLAUDE.md 規則 1 の意味で未検証の統計）。サーバー単位では全付与か全無しの二極（部分付与 0/194、片側 95% 上限 1.53%）。注釈の『値が正しいか』は調べていない（有無だけ）。 条件の分母を訂正: 発見者は『公式 MCP Registry からの無作為抽出 400 件』と書いたが、枠は npm 公開・stdio 宣言・active の 7,258 件に限られる（x01a exact）。リモートサーバーを含む全レジストリの率ではない。

### Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent–Tool Boundary

<a id="g-c10-research-standards-02"></a>
#### C10-02 Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent–Tool Boundary

- **資料**: arXiv:2609.15397v1 §4（MCP の注釈についての段落）（論文）
- **URL**: https://arxiv.org/html/2609.15397v1#S4
- **照らし合わせた中身の URL**: https://arxiv.org/html/2609.15397v1
- **版**: arXiv:2609.15397v1（2026-09-14 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 4 Transactional Tool Contracts and Guarantee Boundaries（HTML の節 id は S4）
- **原文**:

> These are advisory boolean hints — unenforced, optional, and coarser than the capabilities of Table 2: idempotentHint marks a property but supplies no idempotency key, and no hint covers status resolution, compensation, staging, commutativity, or visibility.

- **日本語**: これらは助言的な真偽値のヒントで、強制されず、任意で、表 2 の能力より粗い。idempotentHint は性質を示すが冪等キーは与えず、状態の解決・補償・段階実行・可換性・可視性を表すヒントは無い。
- **どう使っているか**: 注釈を『強制されない・任意・粗い』助言として位置づけ、ワークフローの安全（再試行・補償・並行）に必要な契約は注釈では表せないと論じる。注釈を判断材料にする側への限界の指摘。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 4 Transactional Tool Contracts and Guarantee Boundaries」（取得 2026-10-02T22:11:21Z、sha256 a57906aa9b60…）
- **補足**: 本文の参照先は仕様 2025-03-26 版。論文の主題は取引的な契約（transactional contracts）で、注釈の真偽の検証はしていない。

### Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（注釈のレジストリ全数調査）

<a id="g-c10-research-standards-03"></a>
#### C10-03 Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（注釈のレジストリ全数調査）

- **資料**: arXiv:2609.15397v1 §5 What the Boundary Declares Today — Annotation fields are widely emitted（論文）
- **URL**: https://arxiv.org/html/2609.15397v1#S5
- **照らし合わせた中身の URL**: https://arxiv.org/html/2609.15397v1
- **版**: arXiv:2609.15397v1（2026-09-14 投稿）。成果物 https://github.com/flame-stream/mcp-annotation-census（HEAD 5c24643 を 2026-10-02 に確認）
- **書いてある場所**: 見出し経路（verify_quote.py）: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 5 What the Boundary Declares Today > Sampling and methodology.（HTML の節 id は S5）
- **原文**:

> At the wire level, 74.0% of tools serialize at least one field and 61.7% serialize all four. But a field being present says little about whether it was chosen: many values may originate in SDK defaults or server templates rather than deliberate declaration, and some carry no information even when set, since destructiveHint is inapplicable when readOnlyHint is true, a pairing that accounts for 52.8% of all tools.

- **日本語**: 通信上では 74.0% のツールが少なくとも 1 つのフィールドを出し、61.7% が 4 つ全部を出す。だがフィールドがあることは、それが選ばれた値かどうかをほとんど示さない。多くの値は意図した宣言ではなく SDK の既定値やサーバーの雛形から来ている可能性があり、readOnlyHint が true のとき destructiveHint は意味を持たない（この組が全ツールの 52.8%）。
- **どう使っているか**: 注釈の出現率の測定。値が SDK の既定値や雛形由来かもしれず、作者の意図した宣言とは限らない、という注意を明記している（宣言 D を『作者の主張』として読む研究にとっての妥当性の脅威）。
- **条件**: 分母: 2026-07-27 の公式 MCP Registry スナップショット（59,625 エントリ、18,688 サーバー）のうちリモート端点を持つ 9,234 対象へ匿名で tools/list。応答してツールを返した 4,838 サーバーの 98,291 ツール。stdio/パッケージのみのサーバーは対象外。ツールは 1 度も呼んでいない。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 5 What the Boundary Declares Today > Annotation fields are widely emitted.」（取得 2026-10-02T22:11:21Z、sha256 a57906aa9b60…）
- **補足**: 数値は著者の測定で未再現。最頻の組（read-only・非破壊・冪等・open-world）が 39.9%、注釈なしが 26.0%（同段落の次の小見出し、目視）。destructiveHint が実際に意味を持つ（read-only でない）のは 12.9%、破壊的と主張するのは 3.1%（§5 What the hints do not resolve、目視）。

### Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（宣言と実装の差）

<a id="g-c10-research-standards-04"></a>
#### C10-04 Artem Trofimov, Boris Novikov（AVIV Group ほか） — 論文: When Tool Calls Succeed but Workflows Fail（宣言と実装の差）

- **資料**: arXiv:2609.15397v1 §5 What the hints do not resolve（論文）
- **URL**: https://arxiv.org/html/2609.15397v1#S5
- **照らし合わせた中身の URL**: https://arxiv.org/html/2609.15397v1
- **版**: arXiv:2609.15397v1（2026-09-14 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 5 What the Boundary Declares Today > What the hints do not resolve.
- **原文**:

> The census reads the boundary as declared, not as implementations behave. Tools may enforce stronger semantics internally (deduplication, idempotency keys) than any annotation surfaces; that safety remains unusable to a runtime that only sees the interface, and measuring the gap requires implementation-level analysis [23].

- **日本語**: この調査は宣言どおりの境界を読むもので、実装がどう振る舞うかは読んでいない。ツールは注釈が表すより強い性質を内部で持つかもしれないが、インターフェースしか見ないランタイムにはその安全は使えない。その差を測るには実装レベルの解析が要る。
- **どう使っているか**: 宣言（注釈）と実装の振る舞いの差は宣言の調査では測れず、実装レベルの解析が要る、と書く。論文自身はその解析をしておらず、手がかりとして GitHub 上の MCP 実装のデータセット（[23]）を挙げるだけ。宣言と実効の照合（AuthGap の主題）が、この論文の範囲の外に置かれていることの記述。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent-Tool Boundary > 5 What the Boundary Declares Today > What the hints do not resolve.」（取得 2026-10-02T22:11:21Z、sha256 a57906aa9b60…）
- **補足**: [23] = Toeppe, Barrak, Ksontini『A large-scale dataset of MCP implementations on GitHub』arXiv:2607.10123（参考文献の並び順で 23 番目、x04a で題名を照合）。この [23] が宣言と実装の照合をしているかは未確認。 『未着手の課題として位置づける』は言い過ぎなので弱めた（論文は『解析が要る』と書き、データセット [23] を挙げるだけ）。[23] が何かを特定した。

### Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI: From Foundations to Systems

<a id="g-c10-research-standards-05"></a>
#### C10-05 Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI: From Foundations to Systems

- **資料**: arXiv:2606.24937v3 Chapter 23 MCP §23.5.3 Tool Annotations（readOnlyHint の説明）（論文）
- **URL**: https://arxiv.org/html/2606.24937v3#Ch23.S5.SS3
- **照らし合わせた中身の URL**: https://arxiv.org/html/2606.24937v3
- **版**: arXiv:2606.24937v3（version 1.4、2026-09-29 更新）
- **書いてある場所**: §23.5.3 Tool Annotations（HTML の節 id は Ch23.S5.SS3。verify_quote.py の見出し経路は『Part V Agentic AI > Chapter 23 Model Context Protocol (MCP) > 23.5 Tool Definition and Discovery > 23.5.2 Dynamic Tool Registration』と出るが、この巨大な文書では見出しの位置がずれる。本文上は 23.5.3 の中）
- **原文**:

> If true, the tool only reads data and has no side effects. Hosts may auto-approve read-only tools without user confirmation.

- **日本語**: true なら、ツールはデータを読むだけで副作用が無い。ホストは読み取り専用のツールを利用者の確認なしに自動承認してよい。
- **どう使っているか**: readOnlyHint: true のツールはホストが確認なしで自動承認してよい、と教える。この小節には『信頼できないサーバーの注釈は信用しない』という但し書きが無い（同じ章 23.6.1 は『サーバーは宣言した能力を正直に実装すると信頼される（条件付き信頼）』と書く）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Part V Agentic AI > Chapter 23 Model Context Protocol (MCP) > 23.5 Tool Definition and Discovery > 23.5.3 Tool Annotations」（取得 2026-10-02T22:11:21Z、sha256 db314856c499…）
- **補足**: 仕様の『untrusted unless from trusted servers』に当たる注意は、v3 の HTML 本文（svg の中は除く）に『trusted server』の語として 1 度も出ない（verify_quote.py で none、h05c）。23.6.1 は『サーバーは宣言した能力を正直に実装すると信頼される（条件付き信頼）』と書く。研究者・実装者向けの教科書なので、注釈→自動承認という読み方が広まる経路の例。別の表（目視）には Tool misuse の対策として『destructiveHint gates』とある。 同じ章の 23.6.2 User Consent はホストの責任として『Distinguishing between read-only and destructive operations (using annotations)』を挙げる（2 回目の検証者が exact で照合。ツールの見出し経路は 23.6.1 と出るが本文上は 23.6.2）。23.6.1 の原文は『Servers are trusted to implement their declared capabilities honestly, but the host should not blindly trust server-provided data.』（exact）。 但し書きの不在を、目視から『HTML 本文での照合 none』に強めた（svg 内は未確認のまま）。 【2 回目の検証者】23.6.1 の原文と 23.6.2 の『注釈で読み取りと破壊を区別する』を照合して notes に足した。解釈（may による自動承認の勧め）は過大ではない。

### Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI

<a id="g-c10-research-standards-06"></a>
#### C10-06 Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI

- **資料**: arXiv:2606.24937v3 §23.5.3 Tool Annotations（destructiveHint の説明）（論文）
- **URL**: https://arxiv.org/html/2606.24937v3#Ch23.S5.SS3
- **照らし合わせた中身の URL**: https://arxiv.org/html/2606.24937v3
- **版**: arXiv:2606.24937v3（version 1.4、2026-09-29 更新）
- **書いてある場所**: §23.5.3 Tool Annotations（Ch23.S5.SS3。verify_quote.py の見出し経路はずれて『Part V Agentic AI > Chapter 23 Model Context Protocol (MCP) > 23.5 Tool Definition and Discovery > 23.5.2 Dynamic Tool Registration』）
- **原文**:

> If true, the tool performs irreversible actions. Hosts should require explicit user confirmation.

- **日本語**: true なら、ツールは元に戻せない操作をする。ホストは利用者の明示の確認を求めるべき。
- **どう使っているか**: destructiveHint: true のツールは明示の確認を求めるべき、と教える。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Part V Agentic AI > Chapter 23 Model Context Protocol (MCP) > 23.5 Tool Definition and Discovery > 23.5.3 Tool Annotations」（取得 2026-10-02T22:11:21Z、sha256 db314856c499…）
- **補足**: 既定値（注釈が無いとき）についての記述はこの小節に無い（目視）。

### Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI（承認ゲートの設計 Q&A）

<a id="g-c10-research-standards-07"></a>
#### C10-07 Haggai Roitman（著者） — 論文（教科書型サーベイ）: The Hitchhiker's Guide to Agentic AI（承認ゲートの設計 Q&A）

- **資料**: arXiv:2606.24937v3 §29.29 付近 Q: How do you design approval gates for human-in-the-loop agent systems?（論文）
- **URL**: https://arxiv.org/pdf/2606.24937v3
- **版**: arXiv:2606.24937v3（version 1.4）
- **書いてある場所**: PDF p.674（HTML では節 Ch29.S29 の図（svg）の中）
- **原文**:

> Implementation: Tool annotations (MCP's destructiveHint and readOnlyHint) drive automatic gate assignment. Custom rules can override based on context.

- **日本語**: 実装: ツール注釈（MCP の destructiveHint と readOnlyHint）でゲート（自動承認・通知・停止の 3 段）を自動で割り当てる。文脈に応じた独自規則で上書きできる。
- **どう使っているか**: 承認ゲートの 3 段（自動承認／通知／停止）を注釈で自動的に割り当てる、という設計の勧め。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [未確認] 検証者の再実行 2 回目: none（verify_quote.py --batch, HTTP 200, 7734700 bytes, sha256 70baf8040cea…（1 回目と同じ）, fetched 2026-10-02T18:58:55Z, キャッシュ $S/vqcache_verify/c10_rerun）。 ／ none。PDF 版（none（verify_quote.py, HTTP 200, 7734700 bytes, sha256 70baf8040cea…, fetched 2026-10-02T17:41:57Z, 検証者の再実行 id e07））は行末のハイフン分割（『auto-』/『matic』）と『MCP'sdestructiveHint』の空白欠落で一致しない。HTML 版でも none（none（verify_quote.py, HTTP 200, 17606843 bytes, sha256 db314856c499…, fetched 2026-10-02T17:40:36Z, 検証者の再実行 id h07）。部分『drive automatic gate assignment』も none（h07b）＝この Q&A は svg の図の中にあり verify_quote.py が読まない）。同じ段落の末尾文 s_q07c『Custom rules can override based on context.』だけは PDF p.674 で exact（exact（verify_quote.py, HTTP 200, 7734700 bytes, sha256 70baf8040cea…, fetched 2026-10-02T17:41:57Z, 検証者の再実行 id s_q07c））。
- **補足**: ツールの照合規則では確認にできないので未確認のまま。発見者の抽出文（PDF p.674）を検証者も目視し、文言と 3 段（Auto-approve (no gate) / Notify (soft gate) / Block (hard gate)）の説明は一致した。解釈（注釈で 3 段のゲートを自動で割り当てる設計の勧め）は過大ではない。 【2 回目の検証者】この文は arXiv の HTML にも本文として入っている（要素 id Ch29.S29.p2.pic1.2.4、svg の foreignObject の中）。verify_quote.py は svg の中を本文として扱わないので none になる（ツールのコード 96・112 行の svg の扱い。生の HTML を grep して位置を確かめたのは検証者の目視で、ツールの照合ではない）。 未確認を維持（HTML・PDF とも再実行で none）。修復できる引用の形が無い（逐語で照合できる部分は末尾文だけで、使い方の主張を支えない）。 【2 回目の検証者】再実行でも none。未確認のまま。none の理由（svg の foreignObject の中）を特定して notes に書いた。

### Lin-Fa Lee, Yi-Yu Chang, Chia-Mu Yu, Kuo-Hui Yeh — 論文: WebMCP Tool Surface Poisoning: Runtime Manipulation Attacks on LLM Agents

<a id="g-c10-research-standards-08"></a>
#### C10-08 Lin-Fa Lee, Yi-Yu Chang, Chia-Mu Yu, Kuo-Hui Yeh — 論文: WebMCP Tool Surface Poisoning: Runtime Manipulation Attacks on LLM Agents

- **資料**: arXiv:2606.06387v1 §5.3 Field Level Effects and Composite Attacks（論文）
- **URL**: https://arxiv.org/html/2606.06387v1#S5.SS3
- **照らし合わせた中身の URL**: https://arxiv.org/html/2606.06387v1
- **版**: arXiv:2606.06387v1（2026-06-04 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: WebMCP Tool Surface Poisoning: Runtime Manipulation Attacks on LLM Agents > 5 Results > 5.3 Field Level Effects and Composite Attacks（節 id S5.SS3）
- **原文**:

> With only readOnlyHint=true, the average success rate across the three models is about 87%. This indicates that readOnlyHint is not a weak signal, but an effective standalone channel for influencing LLM agent tool selection.

- **日本語**: readOnlyHint=true だけを付けた場合、3 モデル平均の攻撃成功率は約 87%。readOnlyHint は弱い信号ではなく、LLM エージェントのツール選択に単独で効く経路である。
- **どう使っているか**: ホストの承認ではなく、LLM 自身が readOnlyHint を『安全な読み取り』の合図として読み、悪性ツールを選びやすくなる、という実験。著者は『単独で効く経路』と解釈するが、AB2 は名前の効果と交絡しており、別条件 C9 では 15% 未満。注釈がモデルの判断材料になりうる（偽の宣言が攻撃面になりうる）ことの例として扱う。
- **条件**: 対象は WebMCP（ブラウザの navigator.modelContext 系の提案）で、MCP サーバーそのものではない。モデルは GPT-5.4, Claude Opus 4.6, Gemini 2.5-flash。AB2（87%）は名前を audit_logger（企業の業務手順らしい名前）に固定したうえで readOnlyHint=true だけを足した条件。基準の AB0（0%）は別の中立な名前 diagnostic_probe なので、名前の効果と readOnlyHint の効果は切り分けられていない（論文の付録では名前だけの C7 が平均 39%、目視）。C9（名前 report_auditor・説明『Read only operation that checks data integrity.』・readOnlyHint: true）では平均 6%（表 6、目視）と、条件で大きく違う。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「WebMCP Tool Surface Poisoning: Runtime Manipulation Attacks on LLM Agents > 5 Results > 5.3 Field Level Effects and Composite Attacks」（取得 2026-10-02T22:11:22Z、sha256 e6d2d73f41e4…）
- **補足**: 数値は著者の測定で未再現。論文は WebMCP にツールの能力・データ範囲・送信先の宣言を求め、メタデータを『セキュリティ境界』として扱うよう提言する（§6、目視）。 発見者の『名前を中立にした C9』は誤り（C9 の名前は report_auditor で、控えめな説明も付く）。AB2 の 87% が名前 audit_logger との交絡であることを条件に足した。

### Aarya Doshi, Yining Hong, Congying Xu, Eunsuk Kang, Alexandros Kapravelos, Christian Kästner（CMU ほか） — 論文: Towards Verifiably Safe Tool Use for LLM Agents（ICSE-NIER 2026）

<a id="g-c10-research-standards-09"></a>
#### C10-09 Aarya Doshi, Yining Hong, Congying Xu, Eunsuk Kang, Alexandros Kapravelos, Christian Kästner（CMU ほか） — 論文: Towards Verifiably Safe Tool Use for LLM Agents（ICSE-NIER 2026）

- **資料**: arXiv:2601.08012v1 §4.3 Acquiring Structured Information Labels（論文）
- **URL**: https://arxiv.org/html/2601.08012v1#S4.SS3
- **照らし合わせた中身の URL**: https://arxiv.org/html/2601.08012v1
- **版**: arXiv:2601.08012v1（2026-01-12 投稿、ICSE-NIER '26 採択、DOI 10.1145/3786582.3786839）
- **書いてある場所**: 見出し経路（verify_quote.py）: Towards Verifiably Safe Tool Use for LLM Agents > 4. Vision: Task-Specific Agents with Guarantees > 4.3. Acquiring Structured Information Labels（節 id S4.SS3）
- **原文**:

> MCP defines the boundary where tools are declared and invoked, but it offers only minimal, optional annotations and advises treating tools as untrusted. Therefore, clients cannot reliably obtain labels, making it impossible to enforce SPECs at runtime.

- **日本語**: MCP はツールを宣言し呼び出す境界を定めるが、最小限で任意の注釈しかなく、ツールを信頼しないよう勧めている。そのためクライアントはラベルを確実に得られず、実行時に仕様（SPEC）を強制できない。
- **どう使っているか**: 現行の注釈は任意で信頼できないため、情報フロー制御などの実行時ポリシーの入力には使えない、と判断している。代わりに MCP の宣言を『任意のヒント』から『必須のキー・値タグ』（機密性・PII など）に広げる提案をする。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Towards Verifiably Safe Tool Use for LLM Agents > 4. Vision: Task-Specific Agents with Guarantees > 4.3. Acquiring Structured Information Labels」（取得 2026-10-02T22:11:20Z、sha256 67eaaabe8a90…）

### Microsoft Research（Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem ほか） — 論文: Securing AI Agents with Information-Flow Control（FIDES）

<a id="g-c10-research-standards-10"></a>
#### C10-10 Microsoft Research（Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem ほか） — 論文: Securing AI Agents with Information-Flow Control（FIDES）

- **資料**: arXiv:2505.23643v2 §4.1 Information-Flow Labels — Attaching labels to data（論文）
- **URL**: https://arxiv.org/html/2505.23643v2#S4.SS1
- **照らし合わせた中身の URL**: https://arxiv.org/html/2505.23643v2
- **版**: arXiv:2505.23643v2（2025-09-03 更新）
- **書いてある場所**: 見出し経路（verify_quote.py）: Securing AI Agents with Information-Flow Control > 4 Agents with Information Flow Control > 4.1 Information-Flow Labels > Attaching labels to data.（節 id S4.SS1）
- **原文**:

> Its latest version (2025-06-18) incorporates annotations in tool definitions (e.g., readOnlyHint, openWorldHint) for clients to understand and manage tool behavior. While these annotations are too coarse-grained and might not be reliable, they provide useful hints to construct trusted tool wrappers.

- **日本語**: MCP の最新版（2025-06-18）はツール定義に注釈（readOnlyHint, openWorldHint など）を入れ、クライアントがツールの振る舞いを理解し管理できるようにした。これらの注釈は粒度が粗く信頼できないかもしれないが、信頼できるツールラッパーを作るための有用なヒントになる。
- **どう使っているか**: 注釈は粒度が粗く信頼できないかもしれないが、情報フロー制御のための『信頼できるラッパー』を作る人への手がかりにはなる、と述べる。注釈を実行時のポリシーやラベルの入力にするとは書いていない（同じ節は『信頼できないツールには全て信頼できるラッパーを付ける』前提で、ラベルはラッパーが付ける）。
- **扱う宣言**: readOnlyHint・openWorldHint ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Securing AI Agents with Information-Flow Control > 4 Agents with Information Flow Control > 4.1 Information-Flow Labels > Attaching labels to data.」（取得 2026-10-02T22:11:20Z、sha256 8e9667e82e37…）
- **補足**: 注釈を実際にどう使ったか（実装）はこの段落には無い（目視）。 usage の policy_rule_input を外した（注釈は開発者がラッパーを作るときのヒントで、実行時の方針の入力ではない。直前の段落は信頼できるラッパーがラベルを付ける、と書く）。

### Weibo Zhao, Jiahao Liu, Bonan Ruan, Shaofei Li, Zhenkai Liang（NUS / PKU） — 論文: When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation

<a id="g-c10-research-standards-11"></a>
#### C10-11 Weibo Zhao, Jiahao Liu, Bonan Ruan, Shaofei Li, Zhenkai Liang（NUS / PKU） — 論文: When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation

- **資料**: arXiv:2509.24272v1 §3.2.4 Attack A4: Tool Metadata Poisoning（論文）
- **URL**: https://arxiv.org/html/2509.24272v1#S3.SS2.SSS4
- **照らし合わせた中身の URL**: https://arxiv.org/html/2509.24272v1
- **版**: arXiv:2509.24272v1（2025-09-29 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation > 3. MCP Server Attack Taxonomy > 3.2. Component-based Attack Taxonomy > 3.2.4. Attack A4: Tool Metadata Poisoning（節 id S3.SS2.SSS4）
- **原文**:

> A tool's name, description, input schema, and annotations are defined by the server and passed to the client. The MCP host may then selectively expose this metadata to the LLM.

- **日本語**: ツールの名前・説明・入力スキーマ・注釈はサーバーが決めてクライアントに渡す。MCP ホストはそのメタデータの一部を選んで LLM に見せることがある。
- **どう使っているか**: 注釈を、悪意あるサーバーが自由に書けるメタデータ（攻撃 A4『ツールメタデータ汚染』の対象）に含めている。LLM はメタデータの正しさを確かめられず、実装ではなく宣言で解釈する、と指摘。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation > 3. MCP Server Attack Taxonomy > 3.2. Component-based Attack Taxonomy > 3.2.4. Attack A4: Tool Metadata Poisoning」（取得 2026-10-02T22:11:20Z、sha256 d2a5ac9f5520…）
- **補足**: A4 の下位類型の例（選択誘導・情報の過剰収集）は名前・説明・スキーマが中心で、注釈固有の攻撃実験はこの節には無い（目視）。

### Yang Shi, Jiaheng Fu, Yihe Huang, Ruixiang Wu, Chengyao Sun, Kaifeng Huang — 論文: Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions

<a id="g-c10-research-standards-12"></a>
#### C10-12 Yang Shi, Jiaheng Fu, Yihe Huang, Ruixiang Wu, Chengyao Sun, Kaifeng Huang — 論文: Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions

- **資料**: arXiv:2607.07461v1 §3.2.2 Tool Schema Pattern（Table 1）（論文）
- **URL**: https://arxiv.org/html/2607.07461v1#S3.SS2.SSS2
- **照らし合わせた中身の URL**: https://arxiv.org/html/2607.07461v1
- **版**: arXiv:2607.07461v1（2026-07-08 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions > 3 MCP Vulnerabilities in Wild > 3.2 Metadata Characteristics (RQ1) > 3.2.2 Tool Schema Pattern（節 id S3.SS2.SSS2）
- **原文**:

> Only 160 tools use title, 234 use outputSchema, 325 use annotations, and 322 use execution; no tool uses icons. This suggests that MCP metadata is structurally complete at the minimum required level, but richer semantic fields are sparsely used.

- **日本語**: title を使うのは 160 ツール、outputSchema は 234、annotations は 325、execution は 322、icons は 0。MCP のメタデータは必須の最低限は揃っているが、意味の豊かな任意フィールドはまばらにしか使われていない。
- **どう使っているか**: 注釈の使用率の測定（1,856 ツール中 325 ＝約 17.5%）。人気のある（スター数上位から選んだ）100 の GitHub 上の MCP サーバーでも、注釈を出すツールは少数、という現状の記録。
- **条件**: 分母: GitHub を『MCP』『Model Context Protocol』で検索し、スター数順に並べて手で選んだ 100 の MCP サーバー・プロジェクトから、公式 Python SDK のクライアントで取った 1,856 ツール（§3.1、Table 1）。無作為抽出ではない。実行時にツール定義を作るプロジェクトは除外されている。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions > 3 MCP Vulnerabilities in Wild > 3.2 Metadata Characteristics (RQ1) > 3.2.2 Tool Schema Pattern」（取得 2026-10-02T22:11:21Z、sha256 0e9d94688432…）
- **補足**: 数値は著者の測定で未再現。比率 17.5% は私の計算（325/1856）。 発見者の『脆弱性の多いサーバー群では』は誤り。標本は脆弱性で選んだ集合ではなく、スター数上位から手で選んだ 100 プロジェクト（x12a / x12b exact）。条件の分母も具体化した。

### Arpan Kumar Mahapatra — 論文: Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration: A Controlled Multi-Model Study

<a id="g-c10-research-standards-13"></a>
#### C10-13 Arpan Kumar Mahapatra — 論文: Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration: A Controlled Multi-Model Study

- **資料**: arXiv:2609.01693v1 §2 Background and System Model（論文）
- **URL**: https://arxiv.org/html/2609.01693v1#S2
- **照らし合わせた中身の URL**: https://arxiv.org/html/2609.01693v1
- **版**: arXiv:2609.01693v1（2026-09-01 投稿）
- **書いてある場所**: 見出し経路（verify_quote.py）: Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration: A Controlled Multi-Model Study > 2 Background and System Model（節 id S2）
- **原文**:

> because the MCP fixture is the trusted local component we take its discovered annotations as ground truth for a tool's mutating status.

- **日本語**: （仕様は注釈を信頼できないとするが）この MCP の部品は信頼できる手元の部品なので、発見した注釈を、ツールが状態を変えるかどうかの正解として扱う。
- **どう使っているか**: 注釈（destructive / read-only）を『状態を変えるツールか』の正解ラベルとして使い、さらに実験ハーネスの止め具（is_mutating かつ未承認なら実行させない。モデル自身の要求では承認を常に false にする）の入力にも使う。根拠は『自分で作った信頼できる部品だから』で、仕様の『信頼できるサーバーなら注釈を使ってよい』に沿った使い方。
- **条件**: 自作のローカル fixture（MCP Python SDK mcp==2.0.0）に限る。同じ節で仕様の『should be considered untrusted, unless obtained from a trusted server』を引用している（x13c exact）。止め具は先行の研究で一度も実際の要求で作動していない（x13b exact）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Public-Sharing Labels and Verbatim Field Egress in an MCP-to-A2A Agent Configuration: A Controlled Multi-Model Study > 2 Background and System Model」（取得 2026-10-02T22:11:20Z、sha256 1fb91ea17e4d…）
- **補足**: 注釈が採点の正解ラベルだけでなく、ハーネスの実行停止の判定（is_mutating）にも使われていることを足した（x13a exact）。

### OWASP（MCP Top 10 プロジェクト。寄稿: Spring AI Playground の保守者 Jemin Huh） — OWASP MCP Top 10 — Recommended Control: Client-Side Tool Risk Gating for MCP Hosts

<a id="g-c10-research-standards-14"></a>
#### C10-14 OWASP（MCP Top 10 プロジェクト。寄稿: Spring AI Playground の保守者 Jemin Huh） — OWASP MCP Top 10 — Recommended Control: Client-Side Tool Risk Gating for MCP Hosts

- **資料**: Client-Side Tool Risk Gating — Mechanisms 1. Ordered risk scoring with floor overrides（標準・指針）
- **URL**: https://owasp.github.io/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating#1-ordered-risk-scoring-with-floor-overrides
- **照らし合わせた中身の URL**: https://owasp.org/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating
- **版**: OWASP/www-project-mcp-top-10@165fe0f（2026-07-29 のコミット。2025/recommended-controls/Client-Side-Tool-Risk-Gating.md 46 行）
- **書いてある場所**: 見出し経路（verify_quote.py）: Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Mechanisms > 1. Ordered risk scoring with floor overrides（owasp.org は owasp.github.io へ転送される）
- **原文**:

> External tools score from what the upstream declares: MCP tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint), a side-effect scope, a sends-user-data flag, and a documentation-quality penalty.

- **日本語**: 外部ツールは、上流（サーバー）が宣言したもので点数をつける: MCP のツール注釈（readOnlyHint, destructiveHint, idempotentHint, openWorldHint）、副作用の範囲、利用者データを送るかの印、説明の質による減点。
- **どう使っているか**: ホスト側で全ツールを L0〜L5 の危険度に格付けし、外部ツールの格付けの入力に注釈を使う。設定した上限を超えるツールは有効化を拒否し、モデルから隠す（承認の道も無い）。注釈が欠けている・曖昧なときは点数を上げる床規則がある（エントリ 15）。宣言で点数が下がるかはこの文書には書かれていないが、参照実装（Spring AI Playground の McpToolPublishRiskCalculator、HEAD 1feb4da）では readOnlyHint が true でないと +1（155 行）、idempotentHint が true だと −1（161 行）なので、readOnlyHint: true や idempotentHint: true を宣言すると点数が下がる。つまり偽の宣言で上限の下に入りうる（AuthGap が照合する D1・D4 が、この方式では実際に門の開閉に効く）。
- **条件**: ホスト側の推奨管理策（OWASP MCP Top 10 の Recommended Controls）。参照実装は Spring AI Playground（McpToolPublishRiskCalculator ほか）。上限・格付けはホストごとの設定。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 危険度を付ける・規則（ポリシー）の条件に使う・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Mechanisms > 1. Ordered risk scoring with floor overrides」（取得 2026-10-02T22:11:30Z、sha256 d67bb3cd3131…）
- **補足**: ローカルで作ったツールは宣言ではなく実際のサンドボックス設定から点数をつけ、外部ツールだけが宣言に頼る、と区別している（x14a exact）。OWASP MCP Top 10 の順位づけされた項目ではなく、参照実装（Spring AI Playground）の保守者が寄稿した推奨管理策（x14c exact）。格付けと上限はホストごとの方針（x14d exact）。 参照実装の確認（2 回目の検証者）: https://github.com/spring-ai-community/spring-ai-playground/blob/1feb4daf9e3c0f5878b71a8510845507ca5dc4bd/src/main/java/org/springaicommunity/playground/service/mcp/risk/McpToolPublishRiskCalculator.java#L153-L170 。『if (readOnly == null || !readOnly) score += 1;』（155 行）と『if (Boolean.TRUE.equals(idempotent)) score -= 1;』（161 行）を raw.githubusercontent.com の同じ commit で exact 照合（sha256 56110c496557…）。参照実装は文書が main を指すので、文書の時点（165fe0f, 2026-07-29）の実装と同じかは未確認。 発見者の『注釈は上げる方向に効く設計』は言い過ぎ（文書が言うのは欠落・曖昧なら上げる、だけ。宣言で下がるかは書かれていない）ので削った。寄稿者が参照実装の保守者であることを足した。 【2 回目の検証者】1 回目の『宣言で下がるかは書かれていない』は文書については正しいが、参照実装では readOnlyHint: true と idempotentHint: true が点数を下げることを照合して usage_ja と notes に足した。

### OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（床規則と欠落時の扱い）

<a id="g-c10-research-standards-15"></a>
#### C10-15 OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（床規則と欠落時の扱い）

- **資料**: Client-Side Tool Risk Gating — Mechanisms 1（Floor rules）（標準・指針）
- **URL**: https://owasp.github.io/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating#1-ordered-risk-scoring-with-floor-overrides
- **照らし合わせた中身の URL**: https://owasp.org/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating
- **版**: OWASP/www-project-mcp-top-10@165fe0f（48 行）
- **書いてある場所**: 見出し経路（verify_quote.py）: Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Mechanisms > 1. Ordered risk scoring with floor overrides
- **原文**:

> Floor rules short-circuit the arithmetic on known-dangerous signals: an irreversible verb in a tool name (delete_, drop_, purge_, wipe_), a destructive hint without an idempotent hint, or a remote unauthenticated server at an unknown host all pin the result to L5 regardless of the sum. Floors make the scoring resistant to gaming by omission: missing or vague metadata raises the score rather than lowering it.

- **日本語**: 床規則は、危険が分かっている信号で計算を打ち切る: ツール名の不可逆な動詞（delete_ など）、冪等ヒントの無い破壊的ヒント、未知のホストの認証なしリモートサーバーは、合計に関係なく L5（最高）に固定。床があるので『書かないこと』で点数をごまかせない。メタデータが無い・曖昧なら点数は上がり、下がらない。
- **どう使っているか**: destructiveHint があり idempotentHint が無いツールは最高危険度 L5 に固定。注釈が欠けている・曖昧なときは危険度を上げる（欠落を安全側に倒す）。
- **条件**: 文書だけでは『a destructive hint without an idempotent hint』の without が idempotentHint の欠落だけを指すのか false も含むのかは書かれていない。参照実装（McpToolPublishRiskCalculator、HEAD 1feb4da、198-200 行）は『destructiveHint が true かつ idempotentHint が true でない』（欠落も false も）で L5 に固定する（exact）。また参照実装では、説明も注釈も無いツールの床は L5 ではなく L4（204 行・127-128 行、exact）。『欠落は点数を上げる』の具体は、readOnlyHint が true でなければ +1、注釈が 1 つも無ければ文書品質の減点 +1（docPenalty、目視）。
- **扱う宣言**: destructiveHint・idempotentHint・宣言全般 ／ **使い方の分類**: 危険度を付ける・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Mechanisms > 1. Ordered risk scoring with floor overrides」（取得 2026-10-02T22:11:30Z、sha256 d67bb3cd3131…）
- **補足**: 参照実装の URL: https://github.com/spring-ai-community/spring-ai-playground/blob/1feb4daf9e3c0f5878b71a8510845507ca5dc4bd/src/main/java/org/springaicommunity/playground/service/mcp/risk/McpToolPublishRiskCalculator.java#L196-L205 。照合した行: 『if (Boolean.TRUE.equals(in.annotations().destructiveHint()) && !Boolean.TRUE.equals(in.annotations().idempotentHint())) { return FLOOR_DESTRUCTIVE_NON_IDEMPOTENT;』（198-200 行）、『if (noDescription && noAnnotations) return FLOOR_SEVERE_FAILURE;』（204 行）、『if (FLOOR_SEVERE_FAILURE.equals(floorTrigger)) { level = RiskLevel.L4;』（127-128 行）。文書の時点（165fe0f）の実装と同じかは未確認。 床規則の条件のあいまいさを conditions に足した。 【2 回目の検証者】1 回目が『不明』とした without の意味を参照実装で解決した（欠落も false も含む）。説明・注釈ともに無いときの床は L4 である点も足した。文書の主張自体は変えていない。

### OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（限界: 注釈は指紋に入らない）

<a id="g-c10-research-standards-16"></a>
#### C10-16 OWASP（MCP Top 10 プロジェクト） — OWASP MCP Top 10 — Client-Side Tool Risk Gating（限界: 注釈は指紋に入らない）

- **資料**: Client-Side Tool Risk Gating — Limitations（標準・指針）
- **URL**: https://owasp.github.io/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating#limitations
- **照らし合わせた中身の URL**: https://owasp.org/www-project-mcp-top-10/2025/recommended-controls/Client-Side-Tool-Risk-Gating
- **版**: OWASP/www-project-mcp-top-10@165fe0f（84 行）
- **書いてある場所**: 見出し経路（verify_quote.py）: Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Limitations
- **原文**:

> The fingerprint covers the declared interface (name, description, input schema); upstream annotations are not covered on the live path, so an annotation-only redefinition is a stated blind spot.

- **日本語**: 指紋（初回承認時のハッシュ）は宣言されたインターフェース（名前・説明・入力スキーマ）を覆う。上流の注釈は実行中の経路では覆われないので、注釈だけを書き換える再定義は明示された死角である。
- **どう使っているか**: 定義の改ざん検知（TOFU のピン留め）の対象から注釈が外れている、と限界として明記。注釈で危険度を決めるのに、注釈だけの書き換え（例: 後から readOnlyHint を true に変える）は検知されない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Recommended Control: Client-Side Tool Risk Gating for MCP Hosts > Limitations」（取得 2026-10-02T22:11:30Z、sha256 d67bb3cd3131…）

### Coalition for Secure AI（CoSAI, OASIS Open Project）Workstream 4 — CoSAI ホワイトペーパー: Model Context Protocol (MCP) Security

<a id="g-c10-research-standards-17"></a>
#### C10-17 Coalition for Secure AI（CoSAI, OASIS Open Project）Workstream 4 — CoSAI ホワイトペーパー: Model Context Protocol (MCP) Security

- **資料**: whitepapers/model-context-protocol-security.md §3.1.1 MCP Specific — 2. Tool Poisoning（標準・指針）
- **URL**: https://github.com/cosai-oasis/ws4-secure-design-agentic-systems/blob/4ef8a1c54cf12b357f7c25a190693332c4c27c1e/whitepapers/model-context-protocol-security.md#L240
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/cosai-oasis/ws4-secure-design-agentic-systems/4ef8a1c54cf12b357f7c25a190693332c4c27c1e/whitepapers/model-context-protocol-security.md
- **版**: version 2.0（2026-01-08 承認、2026-08-12 に MCP 2026-07-28 版向けに更新）、cosai-oasis/ws4-secure-design-agentic-systems@4ef8a1c
- **書いてある場所**: lines 240（### 3.1.1 MCP Specific）
- **原文**:

> As the MCP specification notes, 'descriptions of tool behavior such as annotations should be considered untrusted, unless obtained from a trusted server'

- **日本語**: MCP 仕様が書くとおり『注釈のようなツールの振る舞いの説明は、信頼できるサーバーから得たものでない限り信頼できないとみなすべき』。
- **どう使っているか**: 脅威『ツール汚染』の説明で、仕様の『注釈は信頼できない』を引き、検証していないサーバーにつなぐとツール汚染が現実の危険になる、と位置づける。注釈を使った制御の推奨はこの文書に無い（annotation の語は 2 か所。もう 1 か所の 292 行は x-mcp-header のスキーマ注釈で、ToolAnnotations ではない）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、240 行（### 3.1.1 MCP Specific）（取得 2026-10-02T22:11:33Z、sha256 cc023c87995f…）
- **補足**: 公開 PDF（https://www.coalitionforsecureai.org/wp-content/uploads/2026/03/model-context-protocol-security-1.pdf、『8 January 2026』版）にも同じ文がある（発見者の目視）。照合は GitHub の Markdown で行った。同じ文書の Human-in-the-loop の表は『破壊的・状態を変える操作は全て明示の確認（MUST）』とするが（486 行、x17b exact）、その判定に注釈を使うとは書かない。版の『2026-08-12 に更新』は 2 回目の検証者が『Last updated on 12 August 2026 for the MCP 2026-07-28 release.』として exact で照合した（14 行。front matter の 5-7 行にも last_updated: 12 August 2026 / version: 2.0）。 発見者の『annotation の語はこの 1 か所だけ』は誤り。292 行にも出る（x-mcp-header のスキーマ注釈で、ツール注釈ではないので結論は変わらない）。 【2 回目の検証者】版の日付を照合して notes の『確かめていない』を置き換えた。

### Stacklok（MCP レジストリ／ゲートウェイの事業者）。筆者は CEO の Craig McLuckie — Stacklok ブログ: Tool annotations are becoming the risk vocabulary for agentic systems

<a id="g-c10-research-standards-18"></a>
#### C10-18 Stacklok（MCP レジストリ／ゲートウェイの事業者）。筆者は CEO の Craig McLuckie — Stacklok ブログ: Tool annotations are becoming the risk vocabulary for agentic systems

- **資料**: Tool annotations are becoming the risk vocabulary for agentic systems. That matters more than it might seem. — The registry as trust broker（第三者の記事）
- **URL**: https://stacklok.com/blog/tool-annotations-are-becoming-the-risk-vocabulary-for-agentic-systems-that-matters-more-than-it-might-seem/
- **版**: 2026-04-02 公開（ページの日付表示『April 02, 2026』を exact で照合。JSON-LD の datePublished も 2026-04-02T14:40:01-07:00、目視）。本文の『a couple weeks ago』は 2026-03-16 の MCP ブログを指し、日付と矛盾しない。
- **書いてある場所**: 見出し経路（verify_quote.py）: Tool annotations are becoming the risk vocabulary for agentic systems. That matters more than it might seem.（『The registry as trust broker』の段落、目視）
- **原文**:

> The natural next step is to extend that vetting process to include annotation accuracy. When we evaluate an MCP server for inclusion in the registry, we can scrutinize the source code to confirm that the declared annotations match the actual behavior of the tools. A tool that claims readOnlyHint: true should be proven to not write to any external state.

- **日本語**: 次の段階は、審査に『注釈の正確さ』を含めること。レジストリに載せるサーバーを評価するとき、ソースコードを調べて、宣言された注釈がツールの実際の振る舞いに合うかを確かめられる。readOnlyHint: true を主張するツールは、外部の状態に書き込まないことが証明されるべき。
- **どう使っているか**: レジストリ（信頼の仲介者）がソースコードで注釈の正しさを審査し、審査済みサーバーの注釈だけを方針の入力として信頼する、という構想。例として『審査済みサーバーの読み取り専用ツールは自動承認できる』という方針を挙げ、未審査のサーバーは悲観的な既定値のまま、とする。
- **条件**: 本文の該当段落は構想の書き方（『natural next step』『we can scrutinize』）。一方、同じページの末尾の FAQ は現在形で『Stacklok’s vMCP gateway can apply access policies using annotation metadata as inputs, for example, auto-approving read-only tools from registry-verified servers ... When servers are deployed from Stacklok’s curated registry, annotation accuracy has been verified against source code』と書く（exact）。したがって『審査は実装済み』とベンダー自身は FAQ で主張しているが、本文は構想として書いており、審査の方法・範囲は書かれていない。第三者として確かめていない。未審査のサーバーは『pessimistic defaults』のまま（exact）。自動承認は審査済みサーバーの読み取り専用ツールについての方針の例。
- **扱う宣言**: readOnlyHint・openWorldHint ／ **使い方の分類**: 宣言を検査する・規則（ポリシー）の条件に使う・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool annotations are becoming the risk vocabulary for agentic systems. That matters more than it might seem.」（取得 2026-10-02T22:11:35Z、sha256 b2353ddd0cd4…）
- **補足**: 宣言と実装の照合（AuthGap の主題）を、ベンダーがレジストリ審査として行う構想を述べた一次の例。hints の openWorldHint は引用の直後の文（x18a）による。『can configure Stacklok to treat those annotations as policy inputs』（x18b）は製品の設定としての言い方。FAQ は審査済みと現在形で書く（conditions 参照）が、ベンダーの自己申告で、方法は書かれていない。 openWorldHint の根拠（引用の外の文）を照合して明記した。記事の時期の推定を直した（『数週間前』→『2 週間ほど前』）。 【2 回目の検証者】記事の日付は『ページから読めず』ではなく 2026-04-02（『April 02, 2026』exact）で、筆者は CEO の Craig McLuckie。FAQ が vMCP での自動承認と curated registry での照合済みを現在形で書くことを照合し、『構想・実装済みかは不明』を『本文は構想、FAQ はベンダーの自己申告で実装済みと主張』に直した。

### Alexander Sklar（個人ブログ。本人の紹介では Microsoft の Principal Software Engineer） — ブログ: MCP Tool Annotations Are Not Security

<a id="g-c10-research-standards-19"></a>
#### C10-19 Alexander Sklar（個人ブログ。本人の紹介では Microsoft の Principal Software Engineer） — ブログ: MCP Tool Annotations Are Not Security

- **資料**: MCP Tool Annotations Are Not Security — Annotations are UX, not policy（第三者の記事）
- **URL**: https://asklar.dev/ai/security/2026/03/23/mcp-tool-annotations-not-security#annotations-are-ux-not-policy
- **照らし合わせた中身の URL**: https://asklar.dev/ai/security/2026/03/23/mcp-tool-annotations-not-security
- **版**: 2026-03-23 公開
- **書いてある場所**: 見出し経路（verify_quote.py）: MCP Tool Annotations Are Not Security > Annotations are UX, not policy
- **原文**:

> If a tool says it's destructive, showing a confirmation dialog before running it is smart. If a tool says it's read-only, maybe you skip the confirmation. That's a better user experience.

- **日本語**: ツールが自分は破壊的だと言うなら、実行前に確認ダイアログを出すのは賢い。読み取り専用だと言うなら、確認を省いてもよいかもしれない。それはよりよい利用者体験だ。
- **どう使っているか**: 注釈は UX（確認ダイアログを出す／省く）には使ってよいが、方針（セキュリティ境界）ではない、と区別する。実効の制限はサンドボックス・ネットワーク隔離など実行環境で行うべきだと主張。
- **条件**: 自動承認は『maybe you skip the confirmation』という控えめな言い方で、UX の話としてだけ。方針（セキュリティ境界）としては使うな、が主張。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP Tool Annotations Are Not Security > Annotations are UX, not policy」（取得 2026-10-02T22:11:21Z、sha256 6cca70d774d9…）
- **補足**: Microsoft の公式見解ではない（個人ブログ）。注釈を足す SEP が 5 つ開いている、という記述もある（未確認の主張）。 auto_approve が『maybe』付きの UX の話であることを conditions に足した。

### Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement（注釈を信用せず実行時に強制するプロキシ）

<a id="g-c10-research-standards-20"></a>
#### C10-20 Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement（注釈を信用せず実行時に強制するプロキシ）

- **資料**: README.md — The problem / The approach（第三者の記事）
- **URL**: https://github.com/Mathis488/mcp-annotation-enforcement/blob/f3e8044d09b9f076b6a7c6dccaa898fe1ee85296/README.md#L12-L13
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Mathis488/mcp-annotation-enforcement/f3e8044d09b9f076b6a7c6dccaa898fe1ee85296/README.md
- **版**: Mathis488/mcp-annotation-enforcement@f3e8044（2026-10-02 の HEAD）
- **書いてある場所**: lines 12-13（## The problem）
- **原文**:

> Several major hosts nevertheless route their approval decision through exactly those declarations. If `readOnlyHint: true` is set, the user is not asked.

- **日本語**: （仕様は注釈を信頼しないよう求めるのに）いくつかの主要なホストは承認の判断をまさにその宣言で決めている。readOnlyHint: true なら利用者に尋ねない。
- **どう使っているか**: 宣言を検証するのではなく『本当にする』: 同じサーバーを 3 つの権限で起動し、readOnlyHint: true のツールは書き込み禁止の実体へ、readOnlyHint: true かつ openWorldHint: false はさらにネットワーク禁止の実体へ振り分ける（macOS sandbox-exec）。嘘の宣言はカーネルで失敗する。
- **条件**: macOS のみの試作。readOnlyHint: true だが openWorldHint: false を宣言しないツールは、ネットワークでの持ち出し経路が残る（README の Measured limits、目視）。
- **扱う宣言**: readOnlyHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認] 再照合 exact・1 か所、12-13 行（## The problem）（取得 2026-10-02T22:11:30Z、sha256 1b41328a156a…）
- **補足**: 『主要なホストが readOnlyHint で承認を省く』はこの README の主張で、どのホストかは書いていない（未確認）。npm パッケージ mcp-safe-proxy が『承認を回避するためにヒントを書き換える』と自称する、という記述も未確認（npm で確かめていない）。

### Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement — MEASUREMENT-REPORT（静的検出の否定的結果）

<a id="g-c10-research-standards-21"></a>
#### C10-21 Mathis488（GitHub 上の個人の研究プロトタイプ） — mcp-annotation-enforcement — MEASUREMENT-REPORT（静的検出の否定的結果）

- **資料**: MEASUREMENT-REPORT.md — A negative result worth reporting: static analysis cannot answer this（第三者の記事）
- **URL**: https://github.com/Mathis488/mcp-annotation-enforcement/blob/f3e8044d09b9f076b6a7c6dccaa898fe1ee85296/MEASUREMENT-REPORT.md#L89-L92
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/Mathis488/mcp-annotation-enforcement/f3e8044d09b9f076b6a7c6dccaa898fe1ee85296/MEASUREMENT-REPORT.md
- **版**: Mathis488/mcp-annotation-enforcement@f3e8044
- **書いてある場所**: lines 89-92（## A negative result worth reporting: static analysis cannot answer this）
- **原文**:

> The decisive result was the positive control: among tools explicitly marked `readOnlyHint: false` — the known writers — the pattern found **zero** write calls. A detector that cannot find writes in a tool that admits to writing cannot be trusted when it reports none elsewhere. I discarded the entire result.

- **日本語**: 決め手は陽性対照だった。readOnlyHint: false と明示された（書き込むと認めている）ツールで、パターンは書き込み呼び出しを 1 つも見つけなかった。書くと認めたツールの書き込みを見つけられない検出器は、他で『無い』と言っても信用できない。結果は全部捨てた。
- **どう使っているか**: readOnlyHint: true のツール本体に書き込み操作があるかをソースから探す静的検査を試み、語のパターン照合では偽陽性ばかりで、陽性対照（書くと宣言したツール）で書き込みを 0 件しか見つけられなかったため破棄した、という報告。宣言と実装の静的照合が素朴な方法では成り立たないことの実例。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、89-92 行（## A negative result worth reporting: static analysis cannot answer this）（取得 2026-10-02T22:12:54Z、sha256 4a8f4c2a4180…）
- **補足**: AuthGap（AST・効果の解析）とは手法が違う（ここは語のパターン照合）。同報告は『注釈の存在と論理的整合（read-only かつ destructive でない）を CI で確かめる静的検査はある』とも書く（65-68 行、目視）。

### mcp-glimpse（CrankingAI、MIT ライセンスの OSS） — mcp-glimpse Learn: Tool annotations explained — and why so few tools declare them

<a id="g-c10-research-standards-22"></a>
#### C10-22 mcp-glimpse（CrankingAI、MIT ライセンスの OSS） — mcp-glimpse Learn: Tool annotations explained — and why so few tools declare them

- **資料**: Tool annotations explained — The "shadow write" problem（第三者の記事）
- **URL**: https://www.mcpglimpse.com/learn/tool-annotations-explained/#the-shadow-write-problem
- **照らし合わせた中身の URL**: https://www.mcpglimpse.com/learn/tool-annotations-explained/
- **版**: 2026-06-20 公開
- **書いてある場所**: 見出し経路（verify_quote.py）: Tool annotations explained - and why so few tools declare them > The "shadow write" problem
- **原文**:

> mcp-glimpse calls these shadow writes and flags them by comparing each tool's declared hints against a word-boundary read of its own name and description.

- **日本語**: mcp-glimpse はこれを『隠れた書き込み（shadow writes）』と呼び、各ツールの宣言したヒントを、そのツール自身の名前と説明を単語境界で読んだものと比べて印を付ける。
- **どう使っているか**: 名前・説明が状態変更を示す（create_ / delete_ / set_ / send_ / submit_）のに readOnlyHint を宣言している、または何も宣言していないツールを検出する。照合の相手はコードではなく名前と説明。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool annotations explained - and why so few tools declare them > The "shadow write" problem」（取得 2026-10-02T22:11:41Z、sha256 c9d0f66bf9e3…）
- **補足**: 同じページは注釈の用途を『readOnlyHint → 安全に自動承認、destructiveHint → 明示の確認』と表で説明する（目視）。宣言 vs 名前・説明の照合で、宣言 vs コードの照合ではない。

### Model Context Protocol（Server Card WG。SEP 著者 David Soria Parra ほか） — SEP-2127 MCP Server Cards（Extensions Track、PR #2127 のヘッド）

<a id="g-g3-standards-protocols-01"></a>
#### G3SP-01 Model Context Protocol（Server Card WG。SEP 著者 David Soria Parra ほか） — SEP-2127 MCP Server Cards（Extensions Track、PR #2127 のヘッド）

- **資料**: SEP-2127: MCP Server Cards — Why Exclude Primitives?（仕様）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/5c8483d511d60ef1f8ded5160c5290fd8213d19e/seps/2127-mcp-server-cards.md#L111-L113
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/5c8483d511d60ef1f8ded5160c5290fd8213d19e/seps/2127-mcp-server-cards.md
- **版**: PR #2127 のヘッド commit 5c8483d511d60ef1f8ded5160c5290fd8213d19e（2026-08-24 の『Regenerate SEP docs』。main には未マージ。main の seps/2127-mcp-server-cards.md が 404 なのはこのため）。注意: この commit のファイル見出しは『Status: Final』と書くが、main の WG ページ（docs/community/working-groups/server-card.mdx、main db788e3）の表は Draft、WG のロードマップ（G3_standards_protocols-04 と同じ文書）は『[SEP-2127] is in review』。main には未マージ（main のパスは 404 を再確認）
- **書いてある場所**: L113（### Why Exclude Primitives?）
- **原文**:

> This specification intentionally omits primitive definitions (tools, resources, and prompts) from server cards. MCP servers are inherently dynamic: the primitives a server exposes can vary by authenticated user, session, configuration, feature flags, deployment state, and more.

- **日本語**: この仕様は、サーバーカードからプリミティブ（ツール・リソース・プロンプト）の定義を意図して外している。MCP サーバーは動的で、出すプリミティブは認証ユーザー・セッション・設定・機能フラグ・デプロイ状態などで変わるからだ。
- **どう使っているか**: 静的な Server Card（.well-known のカード）にはツールの一覧そのものを載せない。したがってカードには ToolAnnotations（readOnlyHint など）を載せる場所が無い。注釈は従来どおり接続後の tools/list で得る。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 exact・1 か所、113 行（### Why Exclude Primitives?）（取得 2026-10-02T22:11:36Z、sha256 b7691eee6daa…）
- **補足**: SEP-2127 は 2026-10-02 時点で PR のまま（main の docs/community/working-groups/server-card.mdx では Status Draft）。git ls-remote で refs/pull/2127/head = 5c8483d… を確認し、その commit から読んだ。同じ節に『A follow-on SEP should address the prerequisites … before primitive advertisement is added.』（同じ L113、照合ツールで exact）とあり、ツール（とその注釈）を静的に載せるのは後続の SEP に回されている。注釈の語（annotation / readOnlyHint）自体はこの SEP に出ない。 引用は exact で再確認。PR ヘッドの commit（2026-08-24『Regenerate SEP docs』）を git fetch で確かめた。ファイル見出しの Status: Final と WG ページの Draft の食い違いを version に追記（finder は Draft だけを書いていた）。usage_ja は SEP の範囲内なので据え置き。

### Model Context Protocol（Server Card WG） — SEP-2127 MCP Server Cards（PR #2127 のヘッド）

<a id="g-g3-standards-protocols-02"></a>
#### G3SP-02 Model Context Protocol（Server Card WG） — SEP-2127 MCP Server Cards（PR #2127 のヘッド）

- **資料**: SEP-2127: MCP Server Cards — Security Implications（仕様）
- **URL**: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/5c8483d511d60ef1f8ded5160c5290fd8213d19e/seps/2127-mcp-server-cards.md#L148
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/5c8483d511d60ef1f8ded5160c5290fd8213d19e/seps/2127-mcp-server-cards.md
- **版**: PR #2127 のヘッド commit 5c8483d511d60ef1f8ded5160c5290fd8213d19e（2026-08-24 の『Regenerate SEP docs』。main には未マージ。main の seps/2127-mcp-server-cards.md が 404 なのはこのため）。注意: この commit のファイル見出しは『Status: Final』と書くが、main の WG ページ（docs/community/working-groups/server-card.mdx、main db788e3）の表は Draft、WG のロードマップ（G3_standards_protocols-04 と同じ文書）は『[SEP-2127] is in review』。main には未マージ（main のパスは 404 を再確認）
- **書いてある場所**: L148（## Security Implications）
- **原文**:

> Cards deliberately exclude primitive definitions (tools, resources, prompts) so clients cannot trust a static manifest for access-control or safety decisions; primitives are always validated at runtime via standard list operations.

- **日本語**: カードはプリミティブ（ツール等）の定義をわざと含めない。クライアントが静的なマニフェストをアクセス制御や安全の判断に信用できないようにするためで、プリミティブは常に実行時の list 操作で確かめる。
- **どう使っているか**: 『静的なカードの中身をアクセス制御・安全判断に信用させない』ことを安全上の性質として明記（プリミティブはいつも実行時の list 操作で確かめる）。ToolAnnotations を名指ししておらず、実行時の tools/list に載る注釈を安全判断に使ってよいかについても何も言っていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、148 行（## Security Implications）（取得 2026-10-02T22:11:36Z、sha256 b7691eee6daa…）
- **補足**: この文は primitive 全体の話で、ToolAnnotations を名指ししていない（注釈を安全判断に使うこと自体の可否は述べていない）。静的カードの中身を安全判断の根拠にしない、という範囲の主張。 usage_ja の『ツールの性質（注釈を含む）による判断は、接続後の tools/list の結果に基づくべきという立場』は言い過ぎ。SEP は静的カードを安全判断の根拠にしないと言うだけで、実行時の注釈を信用してよいとも、注釈を判断に使えとも書いていない。そのように直した。同じ節に『because cards are advisory and clients verify their claims against live runtime metadata』とある。Status の食い違いは 01 と同じ。

### Model Context Protocol（Server Card WG、experimental extension） — experimental-ext-server-card（Server Card の TypeScript スキーマ／README）

<a id="g-g3-standards-protocols-03"></a>
#### G3SP-03 Model Context Protocol（Server Card WG、experimental extension） — experimental-ext-server-card（Server Card の TypeScript スキーマ／README）

- **資料**: MCP Server Cards (Experimental Extension) — What is a Server Card?（仕様）
- **URL**: https://github.com/modelcontextprotocol/experimental-ext-server-card/blob/526201bbc80231daa40ffcdecfc9da4e54e5dc93/README.md#L21
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-server-card/526201bbc80231daa40ffcdecfc9da4e54e5dc93/README.md
- **版**: commit 526201bbc80231daa40ffcdecfc9da4e54e5dc93（2026-08-12）
- **書いてある場所**: L21（## What is a Server Card?）
- **原文**:

> Server Cards intentionally omit primitive listings (tools, resources, prompts) — those remain subject to runtime listing via the protocol's standard list operations.

- **日本語**: Server Card はプリミティブの一覧（ツール等）を意図して省く。それらは引き続き実行時の list 操作で得る。
- **どう使っているか**: SEP-2127 の規範的な形式を持つ実験リポジトリでも、カードのスキーマにツール一覧（したがって注釈）は無い。schema.ts の ServerCard の欄は $schema / name / version / description / title / websiteUrl / repository / icons / remotes / _meta だけ。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、21 行（## What is a Server Card?）（取得 2026-10-02T22:11:33Z、sha256 35dae54c9104…）
- **補足**: schema.ts を annotations / readOnlyHint で照合して 0 件（checked_no_mention に記録）。tools の語は『They do not enumerate primitives (tools, resources, prompts)』のコメントと予約名の例にだけ出る。ベンダー固有の情報は _meta に入れられるので、注釈を _meta に独自に入れる余地は形式上ある（仕様はそれを定めていない＝不明）。 schema.ts L20-24 は、カードが宣言する欄（identity / transport / protocol versions）も『advisory, not authoritative』で、クライアントは『must not treat them as authoritative for security decisions』と書く。 引用は exact（ページの em dash は抽出で - になるが exact で一致）。ServerCard の欄の一覧に必須の $schema が抜けていたので足した。schema.ts のコメント（advisory, not authoritative / security decisions に使わない）を notes に足した。

### Model Context Protocol（Server Card WG） — experimental-ext-server-card — Roadmap Priorities

<a id="g-g3-standards-protocols-04"></a>
#### G3SP-04 Model Context Protocol（Server Card WG） — experimental-ext-server-card — Roadmap Priorities

- **資料**: Server Cards: Roadmap Priorities — 2. Describe what a server does（仕様）
- **URL**: https://github.com/modelcontextprotocol/experimental-ext-server-card/blob/526201bbc80231daa40ffcdecfc9da4e54e5dc93/docs/core-maintainer-roadmap.md#L17-L23
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/modelcontextprotocol/experimental-ext-server-card/526201bbc80231daa40ffcdecfc9da4e54e5dc93/docs/core-maintainer-roadmap.md
- **版**: commit 526201bbc80231daa40ffcdecfc9da4e54e5dc93（2026-08-12、『docs: add Server Card roadmap priorities (#47)』）
- **書いてある場所**: L22-23（## 2. Describe what a server does）
- **原文**:

> Primitives were deliberately removed from the card ([PR #19]); this track revisits adding them back for static discovery.

- **日本語**: プリミティブはカードから意図的に外された（PR #19）。この項目では、静的な発見のためにそれを戻すことを再検討する。
- **どう使っているか**: 静的カードにプリミティブ（ツール）を戻すことは、WG がコア・メンテナーのロードマップ向けに『優先順に』提案した 3 項目の 2 番目として再検討中（提案であって決定ではない）。戻す場合にツールの注釈を載せるかどうかは書かれていない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、22-23 行（## 2. Describe what a server does）（取得 2026-10-02T22:11:35Z、sha256 2eb51b9ab757…）
- **補足**: 同じ節の前文は『A card today says _where_ to connect but not _what_ the server can do.』と書き、tools/list や server/discover が認証の後ろにあることを理由に挙げる。注釈を名指しする記述は無い。PR #19 は github.com の HTML がブロックで読めない（git ls-remote で refs/pull/19/head = ee1f187… の存在だけ確認）。 文書は『The Server Card working group's proposed priorities for the core-maintainer roadmap … in priority order』で、WG の提案。『WG の優先度 2 番目』は正しいが、提案である旨を足した。同じ文書の 1 番目に『[SEP-2127] is in review』とあり、01/02 の Status の判断材料にもなる。

### Model Context Protocol（公式ブログ） — MCP blog: Exploring the Future of MCP Transports（2025-12-19）

<a id="g-g3-standards-protocols-05"></a>
#### G3SP-05 Model Context Protocol（公式ブログ） — MCP blog: Exploring the Future of MCP Transports（2025-12-19）

- **資料**: Exploring the Future of MCP Transports — Roadmap > Server Cards（公式ブログ）
- **URL**: https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/#server-cards
- **照らし合わせた中身の URL**: https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/
- **版**: 2025-12-19 の記事（取得 2026-10-02）
- **書いてある場所**: Exploring the Future of MCP Transports > Roadmap > Server Cards（#server-cards）
- **原文**:

> Server Cards enable clients to discover server capabilities, authentication requirements, and available primitives before establishing a connection. This unlocks use cases like autoconfiguration, automated discovery, static security validation, and reduced latency for UI hydration

- **日本語**: Server Card により、クライアントは接続前にサーバーの能力・認証要件・使えるプリミティブを知れる。これで自動設定、自動発見、静的なセキュリティ検証、UI 表示の遅延削減ができる。
- **どう使っているか**: 2025-12 の公式ブログでは、Server Card（当時は SEP-1649 の /.well-known/mcp.json 案。『We’re exploring the direction』と探索段階）で接続前に能力・認証要件・使えるプリミティブが分かるとし、その用途の一つに『静的なセキュリティ検証』を挙げていた。その後 SEP-2127 ではプリミティブがカードから外された（G3_standards_protocols-01〜04）。方針が変わった記録。静的なセキュリティ検証がプリミティブ（やその注釈）を材料にする想定だったかは、この文からは分からない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Exploring the Future of MCP Transports > Roadmap > Server Cards」（取得 2026-10-02T22:11:22Z、sha256 f11f8b735412…）
- **補足**: 記事中のリンクは issue #1649（SEP-1649、.well-known/mcp.json）。SEP-1649 本文は github.com の issue HTML がブロックで読めないため、ツールの注釈をカードに入れる案だったかは不明。静的セキュリティ検証に注釈を使う想定だったかもこの文からは分からない（注釈の語は出ない）。 usage_ja の『カードにプリミティブ（ツール）を載せて「静的なセキュリティ検証」に使うとしていた』は、カード全体の用途の列挙をプリミティブと結びつけた読み込み。用途はカード全体について並べられているだけなので直した。記事内のリンクが issue #1649 であることは HTML で確認。

### Agent Client Protocol（Zed Industries ほか。ACP） — ACP 仕様 v1 — Tool Calls

<a id="g-g3-standards-protocols-06"></a>
#### G3SP-06 Agent Client Protocol（Zed Industries ほか。ACP） — ACP 仕様 v1 — Tool Calls

- **資料**: Tool Calls — Creating（ToolKind）（仕様）
- **URL**: https://agentclientprotocol.com/protocol/v1/tool-calls#creating
- **照らし合わせた中身の URL**: https://agentclientprotocol.com/protocol/v1/tool-calls
- **版**: 公開サイト（取得 2026-10-02）。ソースは agentclientprotocol/agent-client-protocol commit 72580148bc45c5d43fc25d4242a8b20d417f156c の docs/protocol/v1/tool-calls.mdx L68
- **書いてある場所**: Tool Calls > Creating（#creating）
- **原文**:

> Tool kinds help Clients choose appropriate icons and optimize how they display tool execution progress.

- **日本語**: ツールの kind は、クライアントが適切なアイコンを選び、ツール実行の進み具合の表示を工夫するのに役立つ。
- **どう使っているか**: ACP の ToolKind（read / edit / delete / move / search / execute / think / fetch / switch_mode / other）は表示用の分類と定義されている。MCP の ToolAnnotations から kind を導く規定は仕様に無い（kind をどう決めるかはエージェント任せ）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 表示（印・名前）・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Calls > Creating」（取得 2026-10-02T22:11:20Z、sha256 211725e5450f…）
- **補足**: ACP 仕様（tool-calls.md と schema/v1/schema.json）を readOnlyHint / destructiveHint / ToolAnnotations で照合して 0 件（checked_no_mention）。schema.json の Annotations はコンテンツ（audience / priority）用で、ツールの注釈ではない。MCP 注釈→kind の対応は C07・G2 に記録された実装側（Claude Agent ACP、Gemini CLI など）にしか無い。v2 の tool-calls.mdx でも kind の説明は同じ文（L73）で、『Custom tool kinds MUST begin with _』が加わっただけ。

### Agent Client Protocol（ACP） — ACP 仕様 v1 — Tool Calls / session/request_permission

<a id="g-g3-standards-protocols-07"></a>
#### G3SP-07 Agent Client Protocol（ACP） — ACP 仕様 v1 — Tool Calls / session/request_permission

- **資料**: Tool Calls — Requesting Permission（仕様）
- **URL**: https://agentclientprotocol.com/protocol/v1/tool-calls#requesting-permission
- **照らし合わせた中身の URL**: https://agentclientprotocol.com/protocol/v1/tool-calls
- **版**: 公開サイト（取得 2026-10-02）。ソース commit 72580148bc45c5d43fc25d4242a8b20d417f156c の docs/protocol/v1/tool-calls.mdx L191
- **書いてある場所**: Tool Calls > Requesting Permission（#requesting-permission）
- **原文**:

> Clients MAY automatically allow or reject permission requests according to the user settings.

- **日本語**: クライアントは、ユーザーの設定に従って許可要求を自動で許可・拒否してよい。
- **どう使っているか**: 許可を求めるかどうかはエージェント側の判断（『The Agent MAY request permission』）、自動許可はクライアントのユーザー設定。どちらの判断にも MCP 注釈や kind を使えとも使うなとも書いていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Calls > Requesting Permission」（取得 2026-10-02T22:11:20Z、sha256 211725e5450f…）
- **補足**: ACP の permission 要求には toolCall（kind を含みうる）と options（allow_once / allow_always / reject_once / reject_always）が付く。注釈の扱いは仕様上の空白で、実装（エージェント）が MCP 注釈から決めているかは C07 / G2 の実装記録を見ること。

### Agent Client Protocol（ACP。RFD 著者 @benbrandt） — ACP RFD: Tool Call Name

<a id="g-g3-standards-protocols-08"></a>
#### G3SP-08 Agent Client Protocol（ACP。RFD 著者 @benbrandt） — ACP RFD: Tool Call Name

- **資料**: Tool Call Name — Status quo（仕様）
- **URL**: https://agentclientprotocol.com/rfds/tool-call-name#status-quo
- **照らし合わせた中身の URL**: https://agentclientprotocol.com/rfds/tool-call-name
- **版**: 公開サイト（取得 2026-10-02）。ソース commit 72580148bc45c5d43fc25d4242a8b20d417f156c の docs/rfds/tool-call-name.mdx。ACP の docs.json のナビでこの RFD は『Completed』の群にある
- **書いてある場所**: Tool Call Name > Status quo（#status-quo）
- **原文**:

> is a coarse presentation category, such as read or execute, that helps a Client choose an icon or other generic treatment.

- **日本語**: （kind は）read や execute のような粗い表示用の分類で、クライアントがアイコンなどの一般的な扱いを選ぶのに役立つ。
- **どう使っているか**: ACP 自身が kind を『粗い表示分類』と位置づけている。安全判断や自動承認の入力としての意味は仕様上与えられていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Tool Call Name > Status quo」（取得 2026-10-02T22:11:20Z、sha256 128440fb962a…）
- **補足**: 引用は原文『`kind` is a coarse presentation category, …』の `kind` の後から（HTML 化で backtick が消えるため主語を引用から外した）。 RFD（提案文書）の Status quo 節で、現行の kind の位置づけを述べた部分。docs.json で RFD が Completed の群にあることを version に足した。同じ RFD は name についても『ACP assigns no behavioral or authorization semantics to the spelling』と書く（kind ではなく name の話）。

### A2A Project（Linux Foundation。旧 Google 発） — Agent2Agent (A2A) Protocol Specification

<a id="g-g3-standards-protocols-09"></a>
#### G3SP-09 A2A Project（Linux Foundation。旧 Google 発） — Agent2Agent (A2A) Protocol Specification

- **資料**: A2A Specification — 7.6. In-Task Authorization（仕様）
- **URL**: https://a2a-protocol.org/latest/specification/#76-in-task-authorization
- **照らし合わせた中身の URL**: https://a2a-protocol.org/latest/specification/
- **版**: latest（取得 2026-10-02）。ソースは a2aproject/A2A commit 27860f6444aea9b27961fdf51a00a567ea59068f の docs/specification.md L1913
- **書いてある場所**: Agent2Agent (A2A) Protocol Specification > 7. Authentication and Authorization > 7.6. In-Task Authorization
- **原文**:

> An agent requiring human approval before a destructive action is taken

- **日本語**: （例）破壊的な操作の前に人間の承認を必要とするエージェント
- **どう使っているか**: A2A は『破壊的操作の前の人間の承認』を、タスク実行中の認可（In-Task Authorization）の例として挙げるだけ。承認の取り方はエージェントに任され（『such as via directly sending messages to a human』）、TASK_STATE_AUTH_REQUIRED でクライアントに委ねるのは『fallback path』。AgentSkill（a2a.proto）に操作の性質（read-only / destructive）を事前に宣言する欄は無い（extensions など拡張で載せる余地があるかは不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent2Agent (A2A) Protocol Specification¶ > 7. Authentication and Authorization¶ > 7.6. In-Task Authorization¶」（取得 2026-10-02T22:11:20Z、sha256 0e6a4625fb6a…）
- **補足**: 同じ節の『A2A provides the capability for agents to delegate the fulfillment of this authorization to the client via the TASK_STATE_AUTH_REQUIRED Task state.』も exact。AgentSkill（a2a.proto L436-453）の欄は id / name / description / tags / examples / input_modes / output_modes / security_requirements だけ（L451 の『// Security schemes necessary for this skill.』を exact で確認）。仕様ページ全体と a2a.proto を readOnlyHint / destructiveHint / idempotentHint / read-only / side effect（proto は readOnly / read_only / destructive / idempotent / side_effect）で照合して 0 件（checked_no_mention）。 usage_ja が『TASK_STATE_AUTH_REQUIRED で扱う』と言い切っていたが、仕様はこれを fallback path とし、人へ直接メッセージを送るなど他の手段も認める。直した。a2a.proto L436-453 の欄の一覧は一致。

### AGNTCY（Linux Foundation の Agent 基盤プロジェクト。Cisco 発） — OASF（Open Agentic Schema Framework）— mcp_server_tool オブジェクト

<a id="g-g3-standards-protocols-10"></a>
#### G3SP-10 AGNTCY（Linux Foundation の Agent 基盤プロジェクト。Cisco 発） — OASF（Open Agentic Schema Framework）— mcp_server_tool オブジェクト

- **資料**: OASF schema: objects/mcp_server_tool.json（仕様）
- **URL**: https://github.com/agntcy/oasf/blob/56f1bfb155d09d759a38be17cad8c640940bc692/schema/objects/mcp_server_tool.json#L22-L44
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/agntcy/oasf/56f1bfb155d09d759a38be17cad8c640940bc692/schema/objects/mcp_server_tool.json
- **版**: commit 56f1bfb155d09d759a38be17cad8c640940bc692（2026-09-29。schema/version.json は 1.2.0-dev）
- **書いてある場所**: L24（scopes の説明）、L35-38（read_only の項）
- **原文**:

> "read_only": { "caption": "Read-only", "description": "Tool does not modify the environment." },

- **日本語**: read_only: 表示名『Read-only』、説明『ツールは環境を変更しない』。
- **どう使っているか**: エージェントの記述スキーマ OASF（AGNTCY）の MCP レコード（mcp_data.tools → mcp_server_tool）は、ツールを name / title / description / scopes で記述し、scopes の列挙値 idempotent / destructive / read_only / external の説明文は MCP の 4 つの hint の定義とよく似ている。真偽値の hint ではなく『該当する性質を並べる』形で、既定値・信頼・MCP の hint からの写し方についての規定は無い。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、35-38 行（取得 2026-10-02T22:11:29Z、sha256 b4dd6dee43cb…）
- **補足**: L24 の『"description": "List of scopes in which the tool can perform an action.",』も exact。他の項の説明: idempotent『Tool produces the same result when run multiple times with the same input.』、destructive『Tool may perform destructive operations.』、external『Tool interacts with external entities.』。MCP の hint との対応はスキーマ中に明記されておらず、対応関係は私の読み（語と説明文の一致から）。MCP の『hint であり信頼できない』という但し書きは無い。scopes に何も無いことが『非破壊』を意味するのか『不明』を意味するのかも書かれていない（不明）。 usage から passthrough_or_expose を外した。スキーマは scopes の欄を定義するだけで、MCP の tools/list の注釈をそのまま写す（中継・公開する）という記述は repo 内に無い（commit 56f1bfb を git grep。mcp_server_tool を参照するのは dictionary.json と mcp_data.json だけ、readOnlyHint / destructiveHint は 0 件）。MCP の hint との対応は説明文の類似による読みである旨は notes のとおり。

### IETF（Independent Submission。著者 M. Gaikwad） — Internet-Draft: Proxy Modes for Agent-Tool Protocols（draft-gaikwad-agent-proxy-modes-00）

<a id="g-g3-standards-protocols-11"></a>
#### G3SP-11 IETF（Independent Submission。著者 M. Gaikwad） — Internet-Draft: Proxy Modes for Agent-Tool Protocols（draft-gaikwad-agent-proxy-modes-00）

- **資料**: draft-gaikwad-agent-proxy-modes-00 — 6.4 Layer 4: Resilience（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-gaikwad-agent-proxy-modes-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-gaikwad-agent-proxy-modes-00.txt
- **版**: -00（2026-08-13、期限 2027-02-14、Intended status: Standards Track、個人提出で WG 採択ではない）
- **書いてある場所**: L1181-1182（6.4 Layer 4: Resilience の Requirements、Page 21-22）
- **原文**:

> MUST NOT retry an INVOKE-METHOD that may have side effects unless the target is annotated idempotent.

- **日本語**: 副作用があり得る INVOKE-METHOD は、対象が idempotent と注釈されていない限り再試行してはならない。
- **どう使っているか**: プロキシの再試行可否を『idempotent と注釈されているか』で決める（注釈が無ければ再試行しない＝安全側の既定）。MCP の idempotentHint を名指ししてはいないが、プロトコル中立に書かれた同じ発想。
- **扱う宣言**: idempotentHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、1181-1182 行（取得 2026-10-02T22:11:39Z、sha256 099484401bdb…）
- **補足**: draft 全体を readOnlyHint / destructiveHint / idempotentHint / openWorldHint / ToolAnnotations で照合して 0 件。『annotated idempotent』が MCP の idempotentHint を指すのか、プロキシ独自の設定を指すのかは本文から不明。注釈を信用するかどうかの議論も無い。

### IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP Aggregation Protocol (MCP-AX)（draft-abbott-mcp-ax-00）

<a id="g-g3-standards-protocols-12"></a>
#### G3SP-12 IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP Aggregation Protocol (MCP-AX)（draft-abbott-mcp-ax-00）

- **資料**: draft-abbott-mcp-ax-00 — Terminology / 9. Capability Metadata（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-abbott-mcp-ax-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-abbott-mcp-ax-00.txt
- **版**: -00（2026-05-04、期限 2026-11-05、Intended status: Experimental）
- **書いてある場所**: L328-330（Terminology）。スキーマ本体は 9.1 Capability Annotation Schema（L735-750）
- **原文**:

> Capability Annotation: Metadata attached to a tool registration describing latency class, mutability, reversibility, and transport characteristics.

- **日本語**: Capability Annotation: ツールの登録に付けるメタデータで、遅延の区分・変更の有無・元に戻せるか・転送の性質を表す。
- **どう使っているか**: MCP の集約（アグリゲータ）用に、MCP の ToolAnnotations とは別の独自語彙の能力注釈（9.1: latency_class / consistency / mutable / reversible / idempotent / transport / auth_scope / cost_class / availability など。IANA 節で『x-mcpax-*』の注釈キーとして登録を求める）を定義する。readOnlyHint ≒ !mutable、destructiveHint ≒ !reversible に近い（この対応は検証者の読み）が、MCP の既存の注釈には言及しない。auth_scope は 10.2 で認可の範囲の制限に使われる。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、328-330 行（取得 2026-10-02T22:13:02Z、sha256 de238d628f8a…）
- **補足**: draft 全体を readOnlyHint / destructiveHint / idempotentHint / openWorldHint / ToolAnnotations で照合して 0 件。MCP の注釈との対応・重複の扱いは書かれていない（MCP 注釈の存在を前提にしていないように読める）。 org を Independent Submission に直した（ヘッダは『Independent Submission』）。語彙の一覧を 9.1 の実際の欄に合わせ、x-mcpax-* は IANA 節（14 (b)）の登録キーである旨を足した。

### IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP-AX（draft-abbott-mcp-ax-00）

<a id="g-g3-standards-protocols-13"></a>
#### G3SP-13 IETF（Independent Submission。著者 I. Abbott、SoftOboros） — Internet-Draft: MCP-AX（draft-abbott-mcp-ax-00）

- **資料**: draft-abbott-mcp-ax-00 — 11. Irreversibility and Safety Gates（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-abbott-mcp-ax-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-abbott-mcp-ax-00.txt
- **版**: -00（2026-05-04）
- **書いてある場所**: L828-831（11.3 Gate Enforcement）
- **原文**:

> An aggregator operating in "gated" mode MUST intercept tools/call requests targeting irreversible-mutable tools, return a "confirmation_required" response to the client (including tool name, arguments, capability annotation, and route)

- **日本語**: gated モードのアグリゲータは、元に戻せない変更系ツールへの tools/call を横取りし、クライアントに confirmation_required（ツール名・引数・能力注釈・経路を含む）を返さなければならない。
- **どう使っているか**: 独自の能力注釈（mutable / reversible）から『不可逆な変更系』を決め、ゲートで人の確認を要求する。宣言された注釈を確認要求の入力に使う点は MCP 注釈の典型的な使い方と同じ形。
- **条件**: アグリゲータが gated モードのときだけ。対象は reversible: false かつ mutable: true のツール（11.2 で x-mcpax-safety: irreversible_mutable と印を付ける。L822-824 も exact）。確認待ちは既定 300 秒で失効。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、828-831 行（取得 2026-10-02T22:13:02Z、sha256 de238d628f8a…）
- **補足**: 注釈は宣言（サーバー側の申告）で、検証の規定は無い。9.2 は『The aggregator MUST propagate capability annotations upstream without modification.』（L764-765、exact）と、中継で書き換えないことを求める（latency_class だけは上方修正を義務づける）。 org を Independent Submission に直した。conditions（gated モード、reversible:false かつ mutable:true、既定 300 秒）と 9.2 の引用は原文で確認。

### IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: Implementing the NAIM Framework over the Model Context Protocol（draft-feng-nmop-naim-mcp-00）

<a id="g-g3-standards-protocols-14"></a>
#### G3SP-14 IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: Implementing the NAIM Framework over the Model Context Protocol（draft-feng-nmop-naim-mcp-00）

- **資料**: draft-feng-nmop-naim-mcp-00 — 13.3 Semantic Expressiveness of Tool Descriptions（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-feng-nmop-naim-mcp-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-feng-nmop-naim-mcp-00.txt
- **版**: -00（2026-07-16、期限 2027-01-17、Informational）
- **書いてある場所**: L1307-1310（13.3）
- **原文**:

> The AI model is expected to infer operational semantics -- preconditions, side effects, idempotency, compensation logic, field constraints -- from these descriptions alone.

- **日本語**: AI モデルは、前提条件・副作用・冪等性・補償処理・項目の制約といった操作の意味を、（MCP ツールの自然文の）説明だけから推し量ることを期待されている。
- **どう使っているか**: MCP ツールの操作の意味（前提・副作用・冪等性・補償・項目の制約）は自然文の説明からしか分からない、と書く。MCP にはすでに副作用・冪等性の一部を表す ToolAnnotations（readOnlyHint / destructiveHint / idempotentHint。hint であって保証ではない）があるが、この draft はそれに触れない。前提・補償・項目の制約は MCP の注釈にも無いので、draft の指摘が全部的外れというわけではない（『注釈が見落とされている』は検証者側の解釈）。
- **扱う宣言**: 宣言全般・idempotentHint ／ **使い方の分類**: 使わない・読まない・その他
- **確かさ**: [確認] 再照合 exact・1 か所、1307-1310 行（取得 2026-10-02T22:11:39Z、sha256 656c5c1db91a…）
- **補足**: 直前の文『MCP Tool descriptions are natural language strings with no machine-processable semantic structure.』は PDF ではなくテキスト版で『machine-』の行末ハイフン分割があり照合ツールで none だったので引用に使っていない。draft 全体を readOnlyHint / destructiveHint / idempotentHint / openWorldHint / ToolAnnotations で照合して 0 件。 usage_ja の『注釈の存在が標準化の議論で見落とされている例』は、draft が挙げる 5 つの意味のうち MCP の注釈が覆うのは副作用・冪等性の一部だけなので、言い過ぎ。範囲を限って解釈である旨を書いた。draft 中の annotat の語は L205（YANG の意味注釈）と L1320 だけ。

### IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: draft-feng-nmop-naim-mcp-00

<a id="g-g3-standards-protocols-15"></a>
#### G3SP-15 IETF（NMOP 関連の個人 draft。著者 C. Feng） — Internet-Draft: draft-feng-nmop-naim-mcp-00

- **資料**: draft-feng-nmop-naim-mcp-00 — 13.3（提案）（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-feng-nmop-naim-mcp-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-feng-nmop-naim-mcp-00.txt
- **版**: -00（2026-07-16）
- **書いてある場所**: L1319-1321（13.3）
- **原文**:

> The community may wish to consider whether MCP Tool descriptions should support optional structured semantic annotations alongside natural language descriptions

- **日本語**: コミュニティは、MCP ツールの説明に、自然文と並べて任意の構造化された意味の注釈を持たせるべきか検討するとよいかもしれない。
- **どう使っているか**: 構造化された意味注釈（前提・副作用・冪等性など）を MCP に足す提案。既存の ToolAnnotations を拡張する形かどうかは書いていない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、1319-1321 行（取得 2026-10-02T22:11:39Z、sha256 656c5c1db91a…）
- **補足**: 提案の続きは『enabling Handlers that implement semantic validation to advertise their capabilities in machine-processable form』（行末ハイフン分割のため引用外）。

### IETF（個人 draft。J. Rosenberg（Five9）, C. Jennings（Cisco）） — Internet-Draft: Framework, Use Cases and Requirements for AI Agent Protocols（draft-rosenberg-ai-protocols-00）

<a id="g-g3-standards-protocols-16"></a>
#### G3SP-16 IETF（個人 draft。J. Rosenberg（Five9）, C. Jennings（Cisco）） — Internet-Draft: Framework, Use Cases and Requirements for AI Agent Protocols（draft-rosenberg-ai-protocols-00）

- **資料**: draft-rosenberg-ai-protocols-00 — 3.2.3 User Confirmation（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/draft-rosenberg-ai-protocols/
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-rosenberg-ai-protocols-00.txt
- **版**: -00（2025-05-05、期限 2025-11-06 で失効。Informational）
- **書いてある場所**: L846-849（3.2.3 User Confirmation）
- **原文**:

> This is a decision which can only be made by the API owner. Consequently, there is a need to annotate the APIs with ones that require confirmation.

- **日本語**: （どの API に確認が要るかは）API の所有者にしか決められない。だから、確認が必要な API に注釈を付ける必要がある。
- **どう使っているか**: 副作用のある API（作成・更新・削除）は、LLM の外で（プログラム的に）ユーザー確認を取るべきで、そのためにどれが確認要かを API 所有者が注釈する仕組みが要る、という要件。読み取り専用 API は低リスクとする。MCP の注釈を名指ししていない。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 宣言を書くことを求める・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、846-849 行（取得 2026-10-02T22:11:38Z、sha256 962a89196c6e…）
- **補足**: 失効した個人 draft で、標準ではない。宣言者（API 所有者）の注釈を信用する前提で書かれており、宣言が誤る・偽る可能性への議論は無い。MCP 注釈の語は 0 件。

### IETF（個人 draft。G. Zeng（Huawei）ほか） — Internet-Draft: MCP for Network Management: Problem Statement, Use Cases, and Requirements（draft-zeng-nmrg-mcp-usecases-requirements-00）

<a id="g-g3-standards-protocols-17"></a>
#### G3SP-17 IETF（個人 draft。G. Zeng（Huawei）ほか） — Internet-Draft: MCP for Network Management: Problem Statement, Use Cases, and Requirements（draft-zeng-nmrg-mcp-usecases-requirements-00）

- **資料**: draft-zeng-nmrg-mcp-usecases-requirements-00 — Functional Requirements（標準・指針）
- **URL**: https://datatracker.ietf.org/doc/html/draft-zeng-nmrg-mcp-usecases-requirements-00
- **照らし合わせた中身の URL**: https://www.ietf.org/archive/id/draft-zeng-nmrg-mcp-usecases-requirements-00.txt
- **版**: -00（2026-02、期限 2026-08-18 で 2026-10-02 時点では失効。Informational）
- **書いてある場所**: L244（4.1 の FR3）
- **原文**:

> FR3 – Safety Destructive operations require explicit user consent.

- **日本語**: FR3 安全性: 破壊的な操作には利用者の明示的な同意が必要。
- **どう使っているか**: MCP をネットワーク管理に使うときの要件として、破壊的操作の明示的同意を挙げる。どう破壊的と判定するか（destructiveHint を使うのか）は書いていない。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、244 行（取得 2026-10-02T22:11:55Z、sha256 d9ab3c9ca6b2…）
- **補足**: FR2 は『Tools and Resources MUST include human- and machine-readable metadata (e.g., descriptions, parameter schemas)』で、注釈は例に挙がっていない。 期限 2026-08-18 を過ぎているので version に『失効』を足した（finder は期限だけ書いていた）。FR2 の文は原文で確認。

### IETF（RFC Editor。HTTP WG、R. Fielding ほか） — RFC 9110 HTTP Semantics（STD 97）

<a id="g-g3-standards-protocols-18"></a>
#### G3SP-18 IETF（RFC Editor。HTTP WG、R. Fielding ほか） — RFC 9110 HTTP Semantics（STD 97）

- **資料**: RFC 9110 — 9.2.1. Safe Methods（標準・指針）
- **URL**: https://www.rfc-editor.org/rfc/rfc9110.html#name-safe-methods
- **照らし合わせた中身の URL**: https://www.rfc-editor.org/rfc/rfc9110.html
- **版**: RFC 9110（2022-06、Internet Standard）
- **書いてある場所**: HTTP Semantics > 9. Methods > 9.2. Common Method Properties > 9.2.1. Safe Methods
- **原文**:

> A user agent SHOULD distinguish between safe and unsafe methods when presenting potential actions to a user, such that the user can be made aware of an unsafe action before it is requested.

- **日本語**: ユーザーエージェントは、操作の候補を見せるとき安全なメソッドと安全でないメソッドを区別し、安全でない操作を要求する前に利用者が気づけるようにするべきだ。
- **どう使っているか**: （隣接プロトコルの先例）HTTP は『safe（本質的に読み取り専用）』『idempotent』をメソッドの性質として定義し（idempotent は 9.2.2）、UA は操作の候補を見せるとき safe と unsafe を区別して、利用者が安全でない操作に要求前に気づけるようにするべき（SHOULD）とする。確認を必須にするとは書いていない。MCP の readOnlyHint / idempotentHint と同じ発想の、標準化済みの前例。
- **扱う宣言**: readOnlyHint・idempotentHint ／ **使い方の分類**: 表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「HTTP Semantics > 9. Methods > 9.2. Common Method Properties > 9.2.1. Safe Methods」（取得 2026-10-02T22:11:42Z、sha256 d431760660ea…）
- **補足**: MCP 自体の記述ではない。対比のために記録（MCP の仕様が RFC 9110 を参照しているかは確認していない＝不明）。 同じ節の直前の文は、safe の区別により UA が『apply appropriate constraints on the automated use of unsafe methods when processing potentially untrusted content』できる、と書く（自動実行の制約の入力として使う例）。 usage から require_confirmation を外した。原文は『made aware of an unsafe action before it is requested』（知らせる）で、確認を要求するとは言っていない。直前の文（自動実行の制約）を notes に足した。

### IETF（RFC Editor。HTTP WG） — RFC 9110 HTTP Semantics

<a id="g-g3-standards-protocols-19"></a>
#### G3SP-19 IETF（RFC Editor。HTTP WG） — RFC 9110 HTTP Semantics

- **資料**: RFC 9110 — 9.2.1. Safe Methods（宣言と実装の分離）（標準・指針）
- **URL**: https://www.rfc-editor.org/rfc/rfc9110.html#name-safe-methods
- **照らし合わせた中身の URL**: https://www.rfc-editor.org/rfc/rfc9110.html
- **版**: RFC 9110（2022-06）
- **書いてある場所**: HTTP Semantics > 9. Methods > 9.2. Common Method Properties > 9.2.1. Safe Methods
- **原文**:

> This definition of safe methods does not prevent an implementation from including behavior that is potentially harmful, that is not entirely read-only, or that causes side effects while invoking a safe method.

- **日本語**: この safe の定義は、実装が safe なメソッドの処理中に、害になりうる・完全には読み取り専用でない・副作用を起こす振る舞いを含めることを妨げない。
- **どう使っているか**: （先例）『読み取り専用』はメソッドの意味として宣言されるが、実装が本当にそうかは保証されない、と HTTP 自身が明記している。MCP の『注釈は hint で信頼できない』と同じ構図で、宣言と実効の食い違いがありうることの標準上の前例。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「HTTP Semantics > 9. Methods > 9.2. Common Method Properties > 9.2.1. Safe Methods」（取得 2026-10-02T22:11:42Z、sha256 d431760660ea…）
- **補足**: 直後の文は『What is important, however, is that the client did not request that additional behavior and cannot be held accountable for it.』で、責任の所在（クライアントは求めていない副作用の責を負わない）を定める。MCP 注釈についての記述ではない。 notes の『L3825 以降』は HTML ページには行番号が無いので外した（文は照合ツールの文脈で直後にあることを確認）。内容の変更なし。

### OpenAI — GPT Actions（OpenAPI 拡張 x-openai-isConsequential）

<a id="g-g3-standards-protocols-20"></a>
#### G3SP-20 OpenAI — GPT Actions（OpenAPI 拡張 x-openai-isConsequential）

- **資料**: Production notes on GPT Actions — Consequential flag（公式の文書）
- **URL**: https://developers.openai.com/api/docs/actions/production#consequential-flag
- **照らし合わせた中身の URL**: https://platform.openai.com/docs/actions/production
- **版**: 取得 2026-10-02（platform.openai.com から developers.openai.com へ転送。Markdown 版 production.md の L65-67 でも exact）
- **書いてある場所**: Production notes on GPT Actions > Consequential flag
- **原文**:

> If the field isn't present, ChatGPT defaults all GET operations to false and all other operations to true

- **日本語**: この欄が無ければ、ChatGPT は GET の操作をすべて false（「常に許可」ボタンを出す側）、それ以外をすべて true（毎回確認し「常に許可」ボタンを出さない側）として扱う。
- **どう使っているか**: （隣接する宣言の先例）OpenAPI の操作ごとの真偽値 x-openai-isConsequential が true なら ChatGPT は毎回確認し『always allow』ボタンを出さない。false なら『always allow』ボタンを出す（利用者が選べば以後確認なし。自動では許可しない）。欄が無いときは HTTP メソッドから既定を決める（GET は false、それ以外は true）。MCP 注釈が無いときの既定（readOnlyHint=false など）と対比できる。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Production notes on GPT Actions > Consequential flag」（取得 2026-10-02T22:12:54Z、sha256 6de47da52ea1…）
- **補足**: 同じ節の『ChatGPT treats the operation as "must always prompt the user for confirmation before running" and don't show an "always allow" button』も exact。これは MCP ではなく GPT Actions（OpenAPI）の規約。宣言の真偽を検証する記述は無い（宣言をそのまま UI に使う）。C05 には MCP 側の OpenAI 文書が記録されている。 検証者の再取得では sha256 が finder の記録（8319e233754f…）と違った（6de47da52ea1…）。ページの動的部分の差と思われ、引用は exact のまま。 quote_ja の『false（確認不要側）』は誤り。原文は false で『always allow button を出す』とだけ言い、確認が出ないとは言っていない。直した。usage の auto_approve は、自動承認ではなく利用者が選ぶ『常に許可』なので外して other にした。

### OpenTelemetry（GenAI SIG） — semantic-conventions-genai issue #373（Proposal: tool risk attributes for execute_tool and MCP tool call telemetry）

<a id="g-g3-standards-protocols-21"></a>
#### G3SP-21 OpenTelemetry（GenAI SIG） — semantic-conventions-genai issue #373（Proposal: tool risk attributes for execute_tool and MCP tool call telemetry）

- **資料**: Proposal: tool risk attributes for execute_tool and MCP tool call telemetry（issue #373）（issue / PR / 提案の下書き）
- **URL**: https://github.com/open-telemetry/semantic-conventions-genai/issues/373
- **版**: 不明（issue。2026-10-02 時点の状態は読めない）
- **書いてある場所**: issue 本文（未取得）
- **原文**:

> Hosts that gate tool execution increasingly compute a risk posture per tool before exposing or invoking it: from enforced sandbox capabilities for local tools, or from declared annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint), side-effect scope, and provenance for MCP tools.

- **日本語**: ツール実行をゲートするホストは、ツールを見せる・呼ぶ前にツールごとの危険度を計算するようになっている。MCP ツールでは宣言された注釈（readOnlyHint など）・副作用の範囲・出所から計算する。
- **どう使っているか**: トレースにホストが評価したツールの危険度（注釈などから算出）を載せる属性を足す提案。採択されたかは不明。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 危険度を付ける・その他
- **確かさ**: [未確認] 未確認: github.com の issue HTML はこの環境でブロック（検証者の再試行 2026-10-02T22:07:14Z も HTTP 403）。引用は WebSearch の結果要約に出た文で、原文と一致するかは確かめていない。
- **補足**: 現行の semconv（commit e07f4ebacb08f56db8c4c882d117720333fbca04）の docs/gen-ai/mcp.md・registry の mcp.md・gen-ai-tool-definitions.json には注釈の語が無い（checked_no_mention）。自前の確認として、git ls-remote で取った PR ヘッド 339 本（refs/pull/*/head）を docs/ と model/ について readOnlyHint / destructiveHint / tool.risk / risk.level / annotations.read で git grep し 0 件だった（＝この提案を実装した PR は 2026-10-02 時点で見当たらない。ただし PR 本文や議論は見ていない）。 未確認のまま。再試行でも 403。usage（risk_scoring）は提案 issue の要約に基づくもので、採択・実装の証拠は無い（notes の PR ヘッド grep のとおり）。

---

[← 付録 G-11 WebMCP](appendix-g-11.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-13 記載が無かったページと届かなかったページ →](appendix-g-13.md)
