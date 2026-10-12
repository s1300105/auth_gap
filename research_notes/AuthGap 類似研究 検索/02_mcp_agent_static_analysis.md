# MCP サーバ / エージェントツールのコード解析（効果・権限の推定、過剰権限の計測）— AuthGap との重なりの調査（2026-10-12 時点）

担当範囲：MCP サーバとエージェントツール（LangChain / LlamaIndex / CrewAI / OpenAI Agents SDK / smolagents など）のコードから、ツールが実際に持つ効果や権限（FS 書き込み・exec・ネットワーク・DB）を推定する研究とツール。過剰権限や最小権限の計測、ツールの副作用一般も含む。既出リスト（VIPER-MCP、MCP-BiFlow、AgentBound、DCIChecker、…、ReactAppScan）は除いた。

検証レベル：◎ = 一次資料の本文やソースを自分で読んだ（今回は arXiv HTML 本文の該当節を確認したもの）、○ = 要旨・README・公式ページ、△ = 二次情報。**数値はすべて著者の主張で、こちらでは検証していない**（CLAUDE.md 規則 1 による。転記するときは `verified_by_me = none` 相当として扱う）。

判定の語：「同一」/「大きく重なる」/「部分的に重なる」/「隣接」。

---

## Q1. MCP ツールやエージェントツールの効果・能力をコードから（静的またはハイブリッドで）推定する研究は他にあるか。Python で callee を追うものはあるか。未解決呼び出しを数えて報告するものはあるか

### Takeaway
「宣言（ToolAnnotations）と、コードから静的に推定した実効の効果を照合する」研究論文は、既出リスト以外では**見つからなかった**。いちばん近い新規論文は **AgentSecGraph（arXiv 2610.03014, 2026-10-02）** である。MCP/FastMCP と主要 6 フレームワークの入口を正規化し、Python の AST から sink（process / FS / network など）・ガード証拠・外部効果を決定論的に組み立て、解析器を凍結している。ただし解析は手続き内に限られ、宣言側（D）を読まない。このため M 側では大きく重なり、全体としては「部分的に重なる」。宣言側と実効側の照合をするのは、研究ではなく実務ツール（HintLint〔AuthGap の比較対象〕と M8ven〔商用の trust score〕）だけだった。

### Cited Findings

#### 項目別カード（A1 宣言側 / A2 効果側の方法 / A3 callee 追跡 / A4 Python / A5 未解決の扱い / A6 母集団と人手正解 / A7 決定論・LLM 判定なし / A8 事前登録・凍結 / A9 修正コミットで再現率）

| # | 項目（日付） | 検証 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **AgentSecGraph / AgentSecBench**（2610.03014, 2026-10-02, Hang Cui） | ◎ | なし | 静的（Python AST、TS/JS は字句的な逆向き追跡） | **追わない**（手続き内の逆向き依存の回復） | ○ | 「依存証拠を回復できた候補の割合」41.15% を報告（未解決率そのものではない） | 凍結した 67 repo（代表性なしと明記）。正解は再現で確かめた 22 挙動 | ○（グラフ構築に人手ラベルも LLM 判定も使わない） | 解析器の凍結あり。事前登録はなし | なし | **部分的に重なる**（M 側の sink・ガード・入口正規化は重なる。D との照合はない） |
| 2 | **Agent Approval Laundering**（2609.28586, 2026-09-23） | ◎ | 承認記録（ホスト承認オブジェクトの項目、判断時点のメタデータ） | 静的（マニフェスト・設定のパーサ）と、実行後の証拠（正解側） | ワークフロー展開（lifecycle hook、PEP 517、.mcp.json など）を追う。コードの callee は追わない | 一部（pyproject / PEP 517） | 「residual」として未カバーの効果を数える | 111 対、fixed-SHA の 11 実行、事前指定の holdout 17 | ○（決定論的パーサ） | **あり**（パーサの凍結と事前指定 holdout） | なし | **部分的に重なる**（「承認された記録と実際の効果の差」という構図と凍結の規律が近い。MCP サーバのコードは解析しない） |
| 3 | **SkillScope**（2605.05868 v3, 2026-09-10 更新） | ◎ | 自然言語（Skill のプロファイル・宣言目的） | 静的（AST）、LLM、動的リプレイ | 手続き内の data/control 依存のみ | ○（同梱スクリプト） | 記述なし | 68,312 Skills、人手ラベル 200 | ×（LLM 分類器が判定に入る） | なし | なし | **部分的に重なる**（「宣言目的とコード上の操作」を照合する骨格は同じ。対象が Skills で、判定に LLM を使う） |
| 4 | **MCPPrivacyDetector**（2606.21338, 2026-06-19） | ◎ | なし | 静的（CodeQL、規則照合、taint） | CodeQL の伝播（代入・引数・属性）。深さは明記なし | ○（ほか JS/TS/Java/Go） | 記述なし | 10,655 servers、陽性 200 件を手で確認 | 判定は規則ベース（LLM の記述なし） | なし | なし | **隣接**（`@mcp.tool` ハンドラを暗黙の sink / 入口に使う点だけが共通。対象はプライバシー流出） |
| 5 | **MCPacific**（2610.05319, 2026-10-04） | ◎ | ツール仕様の抽出（説明・シグネチャ）。annotations の照合はない | 静的（7 言語の AST、30 の登録パターン）＋ Semgrep。警告の分類に LLM を使う | 入口関数まで（ハンドラ参照を解決）。その先は追わない | ○ | 記述なし | 124,267 servers、1,328,233 tools | 抽出は決定論的。分類は LLM | なし | なし | **隣接**（多言語の「ツール入口の規則」として AuthGap の 14 規則と比べる価値はある） |
| 6 | **Same Name, Different Server**（2609.14119, 2026-09-12） | ◎ | レジストリの記述・パッケージ・endpoint の版間差分 | 静的（ガードつき正規表現、31 パターン） | なし | ○ | 記述なし | 21,643 servers / 72,606 版、人手ラベル 414（評価者 1 名） | ○ | 設定ファイル 1 つで全パラメータを固定して公開（事前登録ではない） | なし | **隣接**（前リリースとの比較は D 側の記述ドリフトのみで、効果は比べない） |
| 7 | **AgenTRIM**（2601.12449, EMNLP 2026 Findings） | ◎ | なし | 静的（ツール候補の列挙）＋ 動的検証 ＋ LLM | なし（「どのツールが存在するか」の復元） | ○ | 記述なし | AgentDojo | ×（実行時の判定に LLM judge） | なし | なし | **隣接** |
| 8 | **HintLint**（complira/hintlint、README の 2026-07 pilot 記載） | ○ | **構造化 annotations** | 静的（方式の詳細は README に記述なし） | 記述なし（「handler-scoped source evidence」） | ○（TS/JS も） | 記述なし。ハンドラ解決率は TS/JS 88%、Python 100% | pilot 20 repo / 1,160 tools | LLM の記述なし（`ml/` ディレクトリはある） | なし | なし | **大きく重なる**（既知の比較対象。今回の新事実は下の Findings に記載） |
| 9 | **M8ven Trust Score**（m8ven.ai、2026） | ○ | annotations の有無（source-side AST check） | 非公開（「Static analysis」の表示あり） | 非公開 | 非公開 | 非公開 | 登録サーバ多数（件数不明） | 不明 | なし | なし | **部分的に重なる**（hint の欠落を数え、ハンドラの挙動に合わせるよう勧める。照合の方式は非公開） |
| 10 | **MCPeek**（Fifth Elephant 2026 の発表提案、作者 Akash Sathish） | ○（提案ページ）/ △（ツール本体は未確認） | なし | 静的（AST、多段 taint。ts-morph らしい） | 記述なし | 不明（TS 主体とみられる） | 記述なし | 100+ servers、70 servers で 445 件 | ○（「no model」） | なし | なし | **隣接**（脆弱性 taint であり、宣言との照合はない） |

#### 各項目の根拠（引用は原文）

- **AgentSecGraph（2610.03014）。** 入口の正規化について："The current implementation supports representative constructs from MCP/FastMCP, LangChain, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel, and LlamaIndex." 解析の局所性について："For Python, dependency recovery is AST-based and follows local parameters, assignments, definitions, and reassignments." / "The current analysis is intentionally local. Python analysis is not a complete whole-program interprocedural, alias, points-to, or symbolic analysis". 効果の割り当て："An abstract effect involving a process, filesystem, network, browser, or external service, deterministically assigned from the operation category." ガード証拠："allowlists, fixed-argument or argument-vector command construction, schema or syntax validation, authentication checks, path restrictions, sandboxing, and resource limits." 凍結："the current full-corpus analysis uses the later scanner version frozen before corpus-wide characterization" / "Graph construction uses neither human security labels nor model-generated judgments". 規模：67 repo・11 エコシステム・37,542 ファイル、候補 23,866、依存証拠 9,821（41.15%）、ガード証拠 3,075（12.88%）、held-out 9 件で参照文脈の 91.1% を保持（著者の主張）— [arXiv 2610.03014](https://arxiv.org/abs/2610.03014)
- **Agent Approval Laundering（2609.28586）。** 問題の定義："the durable record names the entry invocation but omits effects exercised by its workflow." 凍結の規律："Parser v1.0 was frozen before the controlled cohort … froze v1.1, the evaluation protocol, source hashes, rule hashes, and all B predictions before any confirmatory execution." パーサが読むもの："package.json, pyproject.toml, Cargo.toml and build.rs, Dockerfile instructions, VS Code task JSONC, MCP configuration, Git hooks, and referenced shell or PowerShell scripts." 結果：holdout で macro recall 0.926 / precision 0.941、residual が 10 から 3 に減少（著者の主張）。MCP は 6 つの効果クラスの 1 つ（"MCP denotes a client-observed protocol capability"）として扱うだけで、サーバ実装は解析しない — [arXiv 2609.28586](https://arxiv.org/abs/2609.28586)
- **SkillScope（2605.05868 v3）。** "It parses the script into an abstract syntax tree (AST) to extract operation-level behaviors (e.g., function calls). SkillScope then performs lightweight intra-procedural data-flow and control-dependence analysis". 判定に LLM を使う："SkillScope leverages an LLM classifier to determine whether the node should be filtered out because it aligns with the declared Skill profile". F1 94.53%、68,312 Skills のうち 6,590 件を過剰権限と判定（著者の主張）— [arXiv 2605.05868](https://arxiv.org/abs/2605.05868)
- **MCPPrivacyDetector（2606.21338）。** "MCPPrivacyDetector uses CodeQL to convert source code from different languages into a queryable program representation." / "protocol-specific implicit sinks (e.g., @mcp.tool handlers)". 精度：陽性と判定した 200 servers を手で確認し 192 件が真、偽陽性率 4.0%。"we observed no instances of false negatives"（陽性サンプルだけから偽陰性なしと述べており、再現率の根拠にはならない）— [arXiv 2606.21338](https://arxiv.org/abs/2606.21338)
- **MCPacific（2610.05319）。** "We develop language-specific static analyzers that recognize these patterns in abstract syntax trees (ASTs) … resolve the associated handler, callback, or method reference to an entry function". 警告の付与："we apply 755 Semgrep rules … to each tool's entry-point function and use an LLM (deepseek-flash) to map the resulting alerts" — [arXiv 2610.05319](https://arxiv.org/abs/2610.05319)
- **Same Name, Different Server（2609.14119）。** "Each pattern is a guarded regular expression rather than a bare keyword match". 全体の精度は 0.56。"51.1% of multi-version servers changed what they advertise between versions, 40.6% did so silently". ソースから 69,027 のツール宣言を回収（著者の主張）— [arXiv 2609.14119](https://arxiv.org/abs/2609.14119)
- **AgenTRIM（2601.12449）。** "Deterministic code analysis enumerates candidate tools; a validator then generates per-tool probes, executes the agent and verifies existence from traces." 静的な復元の限界について："static reconstruction alone cannot confirm which tools are actually reachable by the agent or whether their descriptions match observed behavior." — [arXiv 2601.12449](https://arxiv.org/abs/2601.12449)
- **HintLint（新事実：AuthGap の比較対象の現状）。** README に "It reads the source code, detects what each tool actually does, and reports where annotations don't match behavior." とある。規則は READONLY-001 / DESTRUCTIVE-001 / OPEN-WORLD-001 / FLOW-PROCESS-001 / FLOW-QUERY-001 / FLOW-URL-001 / FLOW-FILESYSTEM-001 / FLOW-CONNECTION-001。2026-07 の pilot は 20 repo・1,160 tools で、確定した注釈問題 23 件、precision 82%（20 件は destructiveHint の欠落）。ハンドラ解決率は TS/JS 88%、Python 100%。Releases 欄は空 — [GitHub complira/hintlint](https://github.com/complira/hintlint)
- **M8ven。** cpp-mcp の PR #68（2026-10-03）によると、M8ven は "performs a source-side AST check" を行い、`ANNOTATIONS.<profile>` の間接参照を解決しないため "24/24 tools missing one or more hints" と報告した — [cpp-mcp PR #68](https://github.com/CHOCEK-RB/cpp-mcp/pull/68)。リスティングページは "30/30 tools missing one or more hints" と表示し、hint を "explicit true/false values that match the handler's actual behaviour" に設定するよう勧める。"Static analysis found nothing flowing your secrets to unexpected places" の表示もあるが、方式は公開されていない — [M8ven listing (sigrank-mcp)](https://m8ven.ai/mcp/sunrisesillneversee-sigrank-mcp-10knhz)
- **MCPeek。** "multi-pass taint tracking from tool inputs to dangerous sinks, mapped to the OWASP MCP Top 10" / "Fully offline, no model, no cloud, no per-scan cost." / "445 real findings across 70 servers"（2026-06-25 の発表提案）— [Hasgeek: Before the agent calls exec](https://hasgeek.com/fifthelephant/fifthelephant-2026-call-for-submissions/sub/before-the-agent-calls-exec-source-level-findings-7d2mtQtEZou3HW6cXpPZh2)
- **ソース側スキャナが annotations を読み落とす実例（2026-09〜10）。** cpp-mcp PR #68 は hint を定数経由で与えていたため M8ven に読まれず、literal に書き直して対応した — [PR #68](https://github.com/CHOCEK-RB/cpp-mcp/pull/68)。ragdbman PR #1 は、汎用ファクトリが 1 つの関数に見え、hint が計算値だったために解析器から見えなかった件を、明示的な宣言と literal に直した — [ragdbman PR #1](https://github.com/bmihalik/ragdbman/pull/1)
- **宣言と実効が食い違う実例。** totem の issue #3004 によると、`verify_execution` が readOnlyHint: true なのに、spawn した lint が `.totem/` 配下に書き込む — [mmnto-ai/totem #3004](https://github.com/mmnto-ai/totem/issues/3004)

### Inferences
- **2026-10-12 時点で「同一」の研究は見つからなかった。** AuthGap の組み合わせを全部満たすものは既出リスト外にない。その組み合わせは、ToolAnnotations とホスト承認と前リリースを宣言側とし、Python の手続き間解析（深さ ≤ 4、引数位置ごと、制御主体あり）で実効側を出し、opaque 率を報告し、事前登録と凍結で評価するというもの。
- **AgentSecGraph は M 側の先行・並行研究として必ず引用すべき。** 差は 3 点ある。(i) 手続き間を追わない、(ii) D 側（annotations）と照合しない、(iii) ガードの十分性を判定しない（"may_guard"）。AuthGap は「主語一致を root で取る」「`startswith` の境界正規化を前の文から読む」まで踏み込んでいるので、ガード等級（付録）の差別化はここで説明できる。ただし AgentSecGraph も解析器を凍結しているので、凍結を AuthGap 独自の新規性として書くことはできない。
- **Approval Laundering は「ホスト承認リスト」を D 側に含める AuthGap の構図と概念上重なる。** 凍結と事前指定の評価規律も近い。比較の単位（ワークフローの展開源と、MCP サーバのコード）が違うので、関連研究で構図の違いを一文で書けば足りる。
- **ソース側の annotation 読み取りの脆さ**（定数経由、ファクトリ生成、計算値）が実務でも問題になっている（M8ven / ragdbman）。AuthGap が宣言側をどう取るか（AST の literal か、wire の `tools/list` か）を明記しておく価値がある。

### Gaps
- AgentSecGraph の補遺（supplementary：対応する構文族と照合規則）は読んでいない。入口規則の数を AuthGap の 14 規則と照らし合わせるには補遺の確認が要る。
- HintLint の解析方式（AST か正規表現か、callee を追うか）は README に書かれていない。ソースは読んでいない（比較実験の側で確認すべき）。
- M8ven の採点方式は公開されていない（"how we score" のページは見つからなかった）。
- MCPeek の GitHub（iamakash-06/MCPeek）は開いていない。

---

## Q2. エージェントツールのコードから最小権限のポリシーやマニフェストを生成・検査する研究（AgentBound 型）。2026-08 以降に新しいものはあるか

### Takeaway
2026-08 以降に出た最小権限の研究は、**実行時の強制か学習によるもの**ばかりで、コードからマニフェストを静的に生成するものは**見つからなかった**。例として IntentCap、RAC、ACLE-MCP、PACE、APEX、Pincer、Task-Conditioned Least-Privilege Learning がある。コードを読んで最小権限を扱う新しいものは Skills 側の SkillScope（v3 2026-09）だけで、MCP サーバについては AgentBound（既出）以降の後続を確認できなかった。

### Cited Findings
- **Task-Conditioned Least-Privilege Learning（2608.18351, 2026-08-18）。** 4B モデルを post-training して過剰権限の誤りを 4.56% から 0.79% に減らした。"predefined task-specific sufficient-authority envelopes" は人が事前に定義する。○、**隣接** — [arXiv 2608.18351](https://arxiv.org/abs/2608.18351)
- **IntentCap（2609.14631, AgenticOS 2026）。** "IntentCap uses an LLM to generate short-lived leases from these sources, validated by a deterministic checker before any side effect commits". 能力の源の 1 つに tool schemas を使う。○、**隣接** — [arXiv 2609.14631](https://arxiv.org/abs/2609.14631)
- **RAC: Runtime Authorization Consistency Checking（2609.23498）。** ワークフロー単位の "authorization drift" を実行時に検出する。○、**隣接** — [arXiv 2609.23498](https://arxiv.org/abs/2609.23498)
- **ACLE-MCP（2609.02690）。** 呼び出し単位の capability lease と provider 側の Execution Gate。○、**隣接** — [arXiv 2609.02690](https://arxiv.org/abs/2609.02690)
- **PACE（2610.01349）。** "capability and effect verification checks schema-defined effects against authority compiled from the authenticated request"。効果は schema での定義が前提で、コードからは推定しない。○、**隣接** — [arXiv 2610.01349](https://arxiv.org/abs/2610.01349)
- **APEX（2610.06966）。** 実行境界での認可契約。○、**隣接** — [arXiv 2610.06966](https://arxiv.org/abs/2610.06966)
- **Pincer（2610.02569）。** digital twin がユーザ固有の最小権限を学習する。○、**隣接** — [arXiv 2610.02569](https://arxiv.org/abs/2610.02569)
- **MiniScope（2512.11147 v2, 2026-10-06 更新）。** "MiniScope further uncovers six overprivileged connector configurations in ChatGPT and Claude." ○、**隣接** — [arXiv 2512.11147](https://arxiv.org/abs/2512.11147)
- **skilder（2609.28693）。** ロール単位の能力配布と、単一 MCP サーバでの強制。○、**隣接** — [arXiv 2609.28693](https://arxiv.org/abs/2609.28693)
- **SkillGuard（2606.03024）。** Skill マニフェストの権限分類（1,260 Skills で保護対象の 99.93% を覆う）。○、**隣接** — [arXiv 2606.03024](https://arxiv.org/abs/2606.03024)
- **Capability Gates Are Not Authorization（2606.28679）。** pin した commit の LangChain/LangGraph、LlamaIndex、Stripe Agent Toolkit を点検し、"none provides a deterministic fail-closed per-call value authorization gate by default"。○、**隣接**（フレームワークの既定の挙動を監査するもので、ツールの効果推定ではない）— [arXiv 2606.28679](https://arxiv.org/abs/2606.28679)
- **ToolPrivBench（2606.20023）と FORTIS（2605.09163）。** LLM が高権限のツールや Skill を選んでしまう傾向のベンチマーク。○、**隣接** — [arXiv 2606.20023](https://arxiv.org/abs/2606.20023), [arXiv 2605.09163](https://arxiv.org/abs/2605.09163)
- **既出項目の版更新（2026-09-01 以降）。** 既出の arXiv 28 件を API で確かめたところ、更新があったのは **MCPTox v2（2508.14925, 2026-09-29）** だけだった。その他（VIPER-MCP v2 は 2026-08-12、AgentBound v3 は 2026-04-24 で FSE 2026 掲載、MCPInspect は DSN 2026 採録で 2026-04-27 版）は 9 月以降の更新なし — [arXiv API id_list による確認](https://export.arxiv.org/api/query?id_list=2508.14925,2510.21236,2605.21392,2510.16558)

### Inferences
- 最小権限の研究は「実行時の強制」と「LLM の選択傾向」に集中しており、**インストール前にコードから効果を推定し、宣言と突き合わせる** AuthGap の位置は空いたままである。AuthGap は強制機構を提案しないので、これらとは役割が補完的だと書ける。
- PACE や IntentCap は効果の情報源に「schema / annotations」を使う。宣言が誤っているとこれらの防御が効かないことは、AuthGap の動機として引用できる（論理的な帰結。著者がそう述べてはいない）。

### Gaps
- AgentBound の後続（同じ著者によるマニフェスト自動生成）は見つからなかった。著者ページは確認していない。
- OpenReview（ICLR 2027 投稿）は検索していない。

---

## Q3. 既出リストにない MCP サーバの大規模計測（副作用・危険 API・権限）、特に 2026-08〜10 の arXiv（cs.CR / cs.SE）

### Takeaway
2026-09 以降の MCP の計測は**宣言側（wire の annotations、レジストリの記述）の計測**が中心である。注目すべきものは 4 本ある。98,291 tools の annotation census（2609.15397）、seed つき無作為抽出の 400 servers（2609.10962）、版間ドリフト（2609.14119、2608.00997 / mcpindex）、ツール単位の地図 MCPacific（2610.05319）。どれも**宣言と実装挙動の差は測っていない**。census の著者自身が "measuring the gap requires implementation-level analysis" と書いており、AuthGap の問いを直接裏づける。

### Cited Findings
- **When Tool Calls Succeed but Workflows Fail（2609.15397, 2026-09-14, Trofimov & Novikov）◎ 隣接。** 公式レジストリの snapshot（2026-07-27）から、到達できた remote 4,838 servers・98,291 tools の annotations を収集。"No tool was called."。"74.0% of tools serialize at least one field and 61.7% serialize all four"。最頻のシグネチャ（read-only, non-destructive, idempotent, open-world）が 39.9%、注釈なしが 26.0%。"destructiveHint … is set on 65.8% of all tools … just 12.9% of tools carry an applicable classification, and only 3.1% assert an actual destructive operation." 限界の明記："The census reads the boundary as declared, not as implementations behave. … measuring the gap requires implementation-level analysis"。成果物は flame-stream/mcp-annotation-census — [arXiv 2609.15397](https://arxiv.org/abs/2609.15397)
- **What a Random Draw from the MCP Registry Contains（2609.10962, 2026-09-10, 単著）◎ 隣接。** 24,135 servers のレジストリから、公開 seed で npm/stdio の 400 servers を無作為抽出し、wire で probe した。初期化に成功したのは 48.8%。"1,626 of 2,766 tools (58.8%) carry no annotations. The curated frame gave 41.5%. Curation therefore flatters this figure by 17.3 points"。"194 of 194 servers in this sample are all-or-nothing" — [arXiv 2609.10962](https://arxiv.org/abs/2609.10962)
- **Same Name, Different Server（2609.14119）◎ 隣接。** Q1 のカード 6 を参照。精度で補正した高深刻度の有病率は約 7.6%。サイレントドリフトがあると高深刻度の所見のオッズ比が 2.96 になる（著者の主張）— [arXiv 2609.14119](https://arxiv.org/abs/2609.14119)
- **Registry Descriptions Go Stale Unevenly（2608.00997 v2, 単著 Gautam Bharti）と mcpindex Drift Report ○ 隣接。** レジストリを 120 回観測（88.6 日、19,099 servers）。v2 は "corrects five claims found by re-running the paper against its own deposited artifact" — [arXiv 2608.00997](https://arxiv.org/abs/2608.00997)。関連サイト mcpindex は remote servers の `tools/list` を毎日 diff し、23 snapshots（2026-06-09〜07-19）で安全に関わる変化 2,503 件（291 servers）を記録した。`annotation-flip-to-destructive` は 123 件で、うち 68 件が初めて注釈をつけたもの、55 件が既存の hint を変更したもの。"behavior changes under an unchanged contract are outside its definition"（WebFetch による要約）。データは Zenodo 10.5281/zenodo.21449150 — [mcpindex.ai/drift](https://mcpindex.ai/drift), [mcpindex PR #228](https://github.com/mcpindex-ai/mcpindex-web/pull/228)
- **MCPacific（2610.05319）◎ 隣接。** 17 マーケットから 124,267 servers・1,328,233 tools を集め、Semgrep の警告を受けたツールは 1.56% — [arXiv 2610.05319](https://arxiv.org/abs/2610.05319)
- **MCPPrivacyDetector（2606.21338）◎ 隣接。** 10,655 servers で、プライバシー流出の率はどの言語でも 10% を超え、最大は Java の 19.1%（本文 "peaking at 19.1% in Java"）— [arXiv 2606.21338](https://arxiv.org/abs/2606.21338)
- **ToFu（2610.13651, 2026-10-09）○ 隣接。** 273 MCP servers・3,405 tools を、metadata から導いた意味的検査と fuzzing で調べた。**数値が食い違っている**：コメント欄は "253 verified semantic security bugs in 118 servers"、要旨は "verified bugs corresponding to CWE weakness classes in 343 tools across 118 of the servers"。付録に "the verbatim LLM prompts" があるので、LLM を使っている — [arXiv 2610.13651](https://arxiv.org/abs/2610.13651)
- **No-Box Vulnerability Analysis / MCPSEC（2609.10854）○ 隣接。** ツールの metadata だけから IPI 脆弱性の仮説を立てる。20 servers・177 tools で 95 件の脆弱性を人手で確認し、そのうち 94 件を予測した — [arXiv 2609.10854](https://arxiv.org/abs/2609.10854)
- **Parasites in the Toolchain / MCP-Sec（2509.06572, IEEE S&P 2026）◎ 隣接（取りこぼしていた既存研究）。** 「Description Collector / Tool Description Extractor」が記述からツールを分類する。12,230 tools のうち 1,062（8.7%）が攻撃に使えるとする — [arXiv 2509.06572](https://arxiv.org/abs/2509.06572)
- **How are AI agents used?（Stein, 2603.23802）◎ 隣接（取りこぼしていた既存研究）。** 177,436 tools を LLM のプロンプトで perception / reasoning / action に分類した。"the share of 'action' tools rose from 27% to 65% of total usage"。本文の付録に "Prompt for direct impact classification" がある — [arXiv 2603.23802](https://arxiv.org/abs/2603.23802)
- **A Large-Scale Dataset of MCP Implementations on GitHub（Toeppe et al., 2607.10123）○ 隣接。** 検証済みの 2,297 MCP プロジェクト、人手レビューで precision 83%。census（2609.15397）が実装レベル解析の文献 [23] として引いている — [arXiv 2607.10123](https://arxiv.org/abs/2607.10123)
- **Scanning the Harness（2609.07360 v3）○ 隣接。** 3,171 repo の設定を調べ、MCP パッケージ宣言の pin がないものが 9.8%。v3 で "corrected counts" — [arXiv 2609.07360](https://arxiv.org/abs/2609.07360)
- **CLAWAUDIT（2606.21071）○ 隣接。** OpenClaw の advisory 446 件を時系列で 229（規則導出用）と 217（held-out）に分け、Semgrep の recall を 21.7% から 66.8% に上げた。**時系列での分割による規則の汎化評価**は、AuthGap の CVE 対や凍結の設計と方法論上の比較点になる — [arXiv 2606.21071](https://arxiv.org/abs/2606.21071)
- **A Two-Dimensional Study of MCP（2609.14721）○ 隣接。** 802 本の論文と 33,319 repo。"nearly all repositories (93.7%) use MCP as an enabling technology" — [arXiv 2609.14721](https://arxiv.org/abs/2609.14721)
- **"67,057 servers" の出典の確認。** Exposed by Design（既出）が "Li and Gao" として引く 67,057 件の静的計測は、MCPInspect（2510.16558, DSN 2026, 既出）と同じ規模で、新規の研究ではないとみられる（帰属は Exposed by Design の記述だけからの推定）— [Web 検索結果（Exposed by Design / 2510.16558）](https://arxiv.org/html/2510.16558v2)

### Inferences
- 9 月以降の計測研究は**宣言側の欠落とドリフト**を定量化しており、「宣言が実装と一致しているか」は誰も測っていない（census 自身が "implementation-level analysis" を将来の課題としている）。AuthGap はこの穴を正面から埋める位置にある。新規性の主張を「宣言の欠落率」ではなく「宣言と実効の矛盾率」に置けば衝突しない。
- 2609.10962 の「curated な母集団は注釈の欠落率を 17.3 pt よく見せる」という結果は、AuthGap の母集団 v2（宣言あり、D29）の選択バイアスを議論するときにそのまま関わる。宣言のある母集団に限ると、ecosystem 全体の率としては引用できない。
- mcpindex の「`annotation-flip-to-destructive` 123 件のうち 68 件は初めての注釈づけ」は、AuthGap が 352 件の開発者の注釈修正コミットで再現率を見る設計に対して、wire 側の独立した参照データになりうる（版の対応はとれていない）。

### Gaps
- census（2609.15397）の成果物リポジトリの中身（ツール単位のデータ、`tools/list` の生ログ）は確認していない。
- mcpindex のデータで「サーバ名 → GitHub ソース」の対応がとれるかは未確認。
- CCS 2026 / USENIX Security 2026 / NDSS 2027 / ACSAC 2026 / RAID 2026 / ASE 2026 / ICSE 2027 の採録リストは、Web 検索では**見つからなかった**（公式の program ページは直接開いていない）。

---

## Q4. LLM エージェントの「ツールの副作用」一般（副作用の分類、undo / rollback、read-only と write の別、コードからのリスク採点）

### Takeaway
副作用を扱う研究は、**効果クラスを人が宣言するか実行時に観測する**前提のものばかりで、コードから read/write を自動分類するものは**見つからなかった**。2609.15397 と LIMBO（2609.29095）は「annotations の語彙では副作用の意味論（冪等キー、補償）を表せない」ことを示しており、AuthGap にとっては背景になる。

### Cited Findings
- **2609.15397（再掲）。** 外部効果の異常 8 類型のカタログと、annotations の表現力の表（A1〜A8 の能力のうち "Limited: idempotence hint only" 1 つを除き "No"）— [arXiv 2609.15397](https://arxiv.org/abs/2609.15397)
- **Where Does Exactly-Once Live? / LIMBO（2609.29095, 2026-09-24）○ 隣接。** 決定論的な sandbox で 25,930 episodes。"offering an idempotency key on every write … lowers the duplicate rate from 28% to 4%" — [arXiv 2609.29095](https://arxiv.org/abs/2609.29095)
- **Atomix（2602.14849）○ 隣接。** 効果クラス（reversible / bufferable / irreversible）で決済する。"prevents correctly classified irreversible actions from leaking"。分類は呼び出しごとに宣言される前提 — [arXiv 2602.14849](https://arxiv.org/abs/2602.14849)
- **Bonded Recourse（2609.01939）、Crab（2604.28138）、ACRFence（2603.20625）○ 隣接。** 補償、checkpoint/restore、rollback 攻撃（タイトルと要旨リストから判断。本文未読）— [arXiv 2609.01939](https://arxiv.org/abs/2609.01939), [arXiv 2604.28138](https://arxiv.org/abs/2604.28138), [arXiv 2603.20625](https://arxiv.org/abs/2603.20625)
- **Tracking Capabilities for Safer Agents（Odersky ほか, 2603.00991）○ 隣接。** エージェントに Scala 3 の capture checking でコードを書かせ、"local purity" を型で強制する。既存ツールの効果は推定しない — [arXiv 2603.00991](https://arxiv.org/abs/2603.00991)
- **Stein（2603.23802）。** perception / reasoning / action の分類は LLM による（Q3 を参照）— [arXiv 2603.23802](https://arxiv.org/abs/2603.23802)
- **実務側の観察。** Web 検索の範囲では、read-only / reversible / external / high-risk の 4 段階分類は人が当てはめる運用指針として出てくるだけで、自動化はされていなかった — [MindStudio blog](https://www.mindstudio.ai/blog/classify-ai-agent-actions-by-risk)

### Inferences
- 副作用を扱う研究は「効果クラスが正しく与えられている」ことを前提にしている（Atomix の "correctly classified"）。その前提を、宣言とコードの照合で点検する手段として AuthGap を位置づけられる。

### Gaps
- undo / rollback 系の論文本文（Crab、ACRFence、Bonded Recourse）は読んでいない。コードからの分類が含まれていないことは要旨だけからの判断。

---

## Q5. TypeScript / JavaScript の MCP サーバを解析し、annotations と比べるもの

### Takeaway
**TS/JS で annotations と実効の効果を照合する研究論文は見つからなかった。** TS/JS を含む実務ツールとしては **HintLint**（TS/JS/Python、既知）と **M8ven**（言語不明、方式非公開）がある。wire レベルでは **mcp-tools-lint** が注釈の欠落と矛盾（例：readOnlyHint と destructiveHint がともに true）を検査する。研究では MCPacific（7 言語の入口抽出）と AgentSecGraph（TS/JS は字句的な追跡）が TS を扱うが、どちらも annotations と照合しない。

### Cited Findings
- HintLint：README に "TypeScript, JavaScript, and Python" への対応と、ハンドラ解決率（TS/JS 88%、Python 100%）がある — [GitHub complira/hintlint](https://github.com/complira/hintlint)
- mcp-tools-lint："Lint MCP tool schemas and annotations before clients reject them: … missing or contradictory annotations in tools/list, over stdio, Streamable HTTP or a JSON file."（リポジトリの説明文。△：検索結果の表示のみ）— [GitHub basitalisandhu/mcp-tools-lint](https://github.com/basitalisandhu/mcp-tools-lint)
- AgentSecGraph："For TypeScript and JavaScript, the current implementation performs syntax-aware lexical backward tracing … more conservative than the Python engine" — [arXiv 2610.03014](https://arxiv.org/abs/2610.03014)
- MCPacific："Python and TypeScript account for 76.1% of MCP servers in these seven languages and contribute the majority of extracted tools (84.0%)." — [arXiv 2610.05319](https://arxiv.org/abs/2610.05319)
- MCPPrivacyDetector：JS/TS/Java/Go も CodeQL で扱う — [arXiv 2606.21338](https://arxiv.org/abs/2606.21338)
- 実務の課題：alpaca-mcp-server の issue #127 は、生成された 58 tools に hint がなく、cancel_all_orders などが read に見えるという報告で、HTTP メソッドから hint を導く修正案を出している — [alpacahq/alpaca-mcp-server #127](https://github.com/alpacahq/alpaca-mcp-server/issues/127)。WeKnora の issue #4088 は read-only のツールが全部 destructiveHint=true になっていた件 — [Tencent/WeKnora #4088](https://github.com/Tencent/WeKnora/issues/4088)

### Inferences
- AuthGap が Python だけを扱うのは限界として明記すべきである。ただし、TS で同じことをする研究論文が出ていない（見つからなかった）ので、新規性は損なわれない。HintLint の TS 対応と比べるときは、AuthGap の比較が Python の部分集合に限られることを書く必要がある。

### Gaps
- npm の MCP サーバを対象とした「宣言と実効」の研究は見つからなかった。中国語圏の会議や査読中の論文までは探せていない。

---

## Q6. MCP ツールに副作用の正解や annotation の正否ラベルをつけたベンチマーク・データセット

### Takeaway
**annotation の正否（readOnlyHint が正しいか）を正解ラベルとして持つ公開データセットは見つからなかった。** 近いものは 3 つある。HintLint の pilot（20 repo・1,160 tools・確定 23 件。データが公開されているかは不明）、mcpindex の wire での注釈フリップの記録（Zenodo）、DynamicMCPBench（効果で採点する benchmark。注釈は扱わない）。

### Cited Findings
- HintLint の pilot（2026-07）：23 件の注釈問題、precision 82%、偽陽性 5 件を確認 — [GitHub complira/hintlint](https://github.com/complira/hintlint)
- mcpindex Drift Report Edition v1（Zenodo 10.5281/zenodo.21449150, CC-BY-4.0）：`annotation-flip-to-destructive` 123 件 — [mcpindex.ai/drift](https://mcpindex.ai/drift)
- DynamicMCPBench（2607.20531）：121 の live MCP servers と 750 タスクで、効果ベースの採点。minefields（してはいけない効果）を持つ — [arXiv 2607.20531](https://arxiv.org/abs/2607.20531)
- MCP-Atlas（2602.00933）は "focuses exclusively on read-only operations" で、書き込みを除外している — [arXiv 2602.00933](https://arxiv.org/abs/2602.00933)
- annotation census の成果物（flame-stream/mcp-annotation-census）は宣言の分布だけで、正否は持たない — [arXiv 2609.15397](https://arxiv.org/abs/2609.15397)
- SkillScope の 200 Skills（過剰権限 100 / 正常 100）は Skills が対象で、MCP の annotations ではない — [arXiv 2605.05868](https://arxiv.org/abs/2605.05868)

### Inferences
- AuthGap の人手判定（矛盾の判定と、≤200 tools の調査）と 352 件の修正コミットは、公開されれば「annotation の正否の正解」として最初期のデータセットになりうる。HintLint の pilot と重なる repo があれば、比較の材料になる。

### Gaps

#### 実行した検索（結果なしも含む）
- **arXiv API**（sortBy=submittedDate、降順）
  1. `abs:"MCP server" AND abs:"static analysis"`（9 件。新規は 2606.21338 と 2608.23763）
  2. `abs:"Model Context Protocol" AND abs:privilege`（23 件）
  3. `abs:"side effect" AND abs:agent AND abs:tool`（50 件）
  4. `abs:"least privilege" AND abs:agent`（40 件）
  5. `abs:MCP AND abs:annotation AND abs:tool`（2609.15397 と 2609.10962 を発見）
  6. `abs:readOnlyHint OR abs:destructiveHint OR abs:"tool annotations"`（5 件。**関係するものは見つからなかった**）
  7. `abs:"MCP servers" AND abs:measurement`
  8. `abs:"MCP" AND abs:permission AND abs:code`（2609.28586 を発見）
  9. `abs:"MCP" AND abs:taint`
  10. `abs:"agent" AND abs:"static analysis" AND abs:tool AND abs:Python`
  11. `abs:"Model Context Protocol"`（新しい順に 300 件）と `abs:MCP AND abs:server AND (cat:cs.CR OR cat:cs.SE)`（新しい順に 300 件）。2026-08-25 以降で絞って全タイトルを目視
  12. `abs:tool AND abs:"side effects" AND (abs:classif* OR abs:undo OR abs:rollback OR abs:reversib*)`
  13. `(abs:LangChain OR abs:LlamaIndex OR abs:CrewAI OR abs:smolagents OR abs:"Agents SDK") AND (abs:"static analysis" OR abs:permission OR abs:privilege)`（**関係するものは見つからなかった**）
  14. `abs:MCP AND (abs:TypeScript OR abs:JavaScript OR abs:npm) AND abs:security`（3 件。**関係するものは見つからなかった**）
  15. `abs:"tool risk" OR (abs:"risk score" AND abs:"agent tool")`
  16. `abs:"over-privilege" OR abs:overprivilege OR abs:"over-privileged"`
  17. `au:Gao AND abs:MCP AND abs:registry` / `abs:MCP AND abs:registry AND abs:vulnerab*`（0 件）/ `abs:"tool definitions" AND abs:MCP`
  18. `(abs:"LLM agent" OR abs:"agentic") AND abs:"static analysis" AND (abs:tool OR abs:tools)`（2610.03014 を発見）
  19. `abs:"tool implementation" AND (abs:description OR abs:documentation) AND abs:inconsisten*`（**0 件**）
  20. `abs:MCP AND (abs:"call graph" OR abs:interprocedural OR abs:"inter-procedural")`
  21. 既出 28 件の id_list で版を確認（9 月以降に更新があったのは MCPTox v2 のみ）
- **WebSearch**
  - `readOnlyHint destructiveHint mismatch MCP server code analysis`
  - `static analysis MCP servers capabilities side effects paper 2026`
  - `CCS 2026 accepted papers Model Context Protocol`（**採録リストは見つからなかった**）
  - `MCP tool annotations linter infer readOnlyHint from source code GitHub`
  - `USENIX Security 2026 accepted papers MCP server tool analysis`（**採録リストは見つからなかった**）
  - `NDSS 2027 MCP agent tool static analysis paper`（**見つからなかった**）
  - `M8ven MCP server scanner score badge annotations`
  - `MCPeek MCP server static taint scanner OWASP MCP Top 10`
  - `ICSE 2027 accepted papers MCP servers empirical`（**見つからなかった**）
  - `ASE 2026 research papers Model Context Protocol server analysis`（**見つからなかった**）
  - `benchmark dataset MCP tools ground truth side effects annotation correctness readOnlyHint`（**annotation の正否のデータセットは見つからなかった**）
  - `"67,057" MCP registry entries static pattern matching tool definitions safety category`（MCPInspect に帰着）
  - `"annotation drift" MCP tools static analysis`
  - `LLM agent tools classify read-only vs mutating side effects automatically from code undo rollback 2026`
- **WebFetch**：Hasgeek の MCPeek 提案、cpp-mcp PR #68、M8ven のリスティング、HintLint の README、mcpindex PR #228、mcpindex.ai/drift
- **失敗したもの（未実行として扱う）**：Semantic Scholar API の 4 クエリ（"MCP tool annotations static analysis side effects"、"least privilege manifest MCP server code analysis"、"agent tool side effect inference static analysis Python"、"MCP server capability inference permission"）はすべて **HTTP 429** で結果なし。DBLP API は bot 検査ページが返り、実行できなかった。
- **探していない場所**：OpenReview（ICLR 2027 投稿）、ACSAC 2026 / RAID 2026 / ISSTA 2026 / FSE 2026 の公式 program ページ、Google Scholar、中国語圏の論文。
- **読んでいないもの**：PDF は 1 本もダウンロードしていない（本文は arXiv HTML を scratchpad で読んだ）。2608.23763 TrustShiftProbe、2609.18217、2610.04378 COPEX など、攻撃や評価が主眼の新着は要旨だけで「隣接以下」と判断した。
