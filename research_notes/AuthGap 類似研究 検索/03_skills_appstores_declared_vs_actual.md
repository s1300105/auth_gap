# MCP 隣接エコシステムにおける「宣言 vs 実際の振る舞い」の整合性研究（エージェントスキル / GPTs / 音声スキル / ブラウザ拡張 / ミニプログラム / IDE 拡張 / プライバシーラベル）

調査日: 2026-10-12。担当範囲: MCP 以外の隣接エコシステム。既知リスト（SkillScope "Do Skill Descriptions Tell the Truth?"、SkillConsist、Semia、GPT Actions IMC 2025、Lalaine、Koch et al.、Arkalakis et al.、PoliCheck、ExtPrivA、Picazo et al.、Stowaway、PScout、Mir）は再調査していない。新しい版が出ていないかだけ確かめた。

**表記の約束**
- 検証水準: ◎ = 一次資料の全文を自分で読んだ（全文 HTML/PDF を取得し、該当する節を読んだもの。論文全体の通読ではない）。○ = 要旨・公式ページ・arXiv API の abstract。△ = 二次資料（検索要約、第三者のまとめ）。
- 数値はすべて**著者の主張**で、こちらでは検証していない（CLAUDE.md 規則 1 の `verified_by_me = none` に当たる）。
- 判定の語彙: 「同一」/「大きく重なる」/「部分的に重なる」/「隣接」。
- A1 = 宣言の種類と、プラットフォームが強制するか。A2 = 実際の振る舞いの取り方。A3 = 手続き間解析か。A4 = 対象言語。A5 = 決定できない・解決できない事例の扱いと、その率を報告しているか。A6 = 母集団・人手の正解・矛盾率。A7 = 判定が決定論的か、LLM が入るか。A8 = 事前登録。A9 = 開発者の修正コミットを使うか。

---

## Q1. エージェントスキル（SKILL.md / allowed-tools / OpenClaw・ClawHub / Agent Plugins）: 2026-08〜10 の新しい研究で、宣言（メタデータ・権限）とコードを照合したものはあるか。散文ではなく構造化フラグを使うものはあるか

### Takeaway
既知リストに**入っていない**最近接の先行研究が 1 本ある。**BIV（arXiv 2605.11770、2026-05）**で、宣言側と実装側の能力集合を 29 能力の分類で集合比較し、Python は AST に基づく**手続き間** taint 解析で読む。OpenClaw の 49,943 スキルの 80.0% が宣言から逸脱すると報告している。AuthGap の「宣言 D と実効 M の照合」に構造が最も近く、必ず引用すべき。ただし宣言側は frontmatter と散文を LLM で抽出したもので、判定に LLM が入る。人手の正解は無く（LLM 判定パネルのみ）、未解決率は報告していない。
2026-08〜10 の新しい研究（SkillSpec、Scan the Skill/Govern the Action、After the Party、Scanning the Harness、SkillsMetric、ClosureBound、Packaged But Not Portable）は、いずれも**構造化された真偽フラグ**と効果を照合していない。宣言側は散文・文書中のコードブロック・allowed-tools の広さのどれかである。ただし「分類できなかったものは無害に分類されたものではない」と明言して失敗件数を数える研究（2609.12001）と、determinate な検出だけを主表に入れる研究（2609.07360）が出ており、AuthGap の `opaque(reason)` と未解決率の報告の方法論的な先例になる。

### Cited Findings

**(1) BIV — "Behavioral Integrity Verification for AI Agent Skills"（Wu, Li, Liu; arXiv 2605.11770v1, 2026-05-12）** 検証水準 ◎（arXiv HTML 全文の該当節）。**既知リスト外で最重要。**
- A1: 宣言側は「metadata（descriptions, YAML frontmatter, API schemas）」。決定論的パーサが「YAML frontmatter, tool.json, api.json, and SKILL.md headers」を読み、LLM が散文のメタデータを読む。両者の和集合を 29 能力・7 分類（Network, Filesystem, Process Execution, Environment, Encoding, Credential, Instruction-Level）に写す。強制について、論文は under-specification を "undisclosed privilege: capabilities exercised without user or platform authorization" と定義している（＝プラットフォームは強制しない前提）。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
- A2/A3/A4: 実装側は決定論的コード解析と LLM の命令解析の併用。原文: "a Python analyzer based on abstract-syntax-tree (AST) traversal supports inter-procedural taint analysis [25], tracing sources (environment variables, file reads, network responses) through transforms (e.g., base64.b64encode) to sinks"。JS/TS は正規表現、shell はリテラル照合で、どちらも "intra-file" である。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
- A5: 解決できない事例は**数えていない**。下限として扱うだけである。原文: "Dynamic dispatch and reflection escape AST-level extraction" / "the deviation count is a lower bound"。代わりに、逸脱 1 件ごとの確度を "137,221 (54.7%) HIGH code-backed, 41,443 (16.5%) MEDIUM instruction-backed, and 72,042 (28.7%) LOW unverifiable text-only" に分けて報告している（これは効果の未解決率ではなく、逸脱の根拠の強さ）。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
- A6: 母集団は OpenClaw レジストリの 49,943 スキル。"250,706 deviations from 39,933 of 49,943 skills (80.0%)"。うち under-specification（コードにあるが宣言に無い）は 135,187 件。正解は人手ではなく 3 モデルの LLM 判定パネルで、69 スキル（167 件の能力判定）を層化抽出し、"Capability precision is 84.4% under Opus 4.6 and 68.9% under 3-judge majority vote"。著者自身が "human-labeled gold at registry scale remains future work" と書いている。悪性スキル検出は 906 スキルで F1 0.946。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
- A7: 判定に LLM が入る（両側の抽出と根本原因の分類）。前提 (A3) として "LLM components are accessed at frozen weights with hash-versioned prompts" を置く。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
- A8/A9: 事前登録の記述なし。開発者の修正コミットも使っていない（全文を "preregist" と "commit" で grep して該当なし。ヒットは "architectural commitment" だけだった）。
- 判定: **「大きく重なる」**。インストール前に静的に、宣言集合と実装集合の差（undeclared = 宣言が狭すぎる側）を数え、Python は AST の手続き間解析で読む点が AuthGap と同じ骨格である。違うのは次の点。宣言が MCP `ToolAnnotations` の構造化真偽ヒントではなく frontmatter と散文の能力集合であること。LLM が判定に入ること。人手の正解と未解決率と事前登録が無いこと。

**(2) "Scan the Skill, Govern the Action: Composing Registry Verdicts with Runtime Consequence Control"（Taneja, Weber; arXiv 2609.12001v1, 2026-09-10）** ◎（HTML 全文の該当節）
- A1: 宣言は SKILL.md 文書中のコードブロック（散文の文書。構造化フラグではない）。A2: 実際の振る舞いは、ライブのエージェントがサンドボックスで実行したコマンド（動的）を、決定論的なリゾルバで 33 種の「consequence class」に写して得る。— [arXiv 2609.12001](https://arxiv.org/html/2609.12001v1)
- A6: 66,192 の ClawHub スキル版が対象。"of 144 commands a live agent executed in a sandbox while following real skill documentation, 34.7% carried a consequence class absent from that document"。別の測定として、全スキャナが clean と判定した 705 スキルが CIS 2.7 / NIST CM-11 で禁止される操作を指示しており、手作業で 100 件を監査して "92% precision" と報告している。— [arXiv 2609.12001](https://arxiv.org/abs/2609.12001)
- A5（AuthGap に最も効く点）: リゾルバを全域関数にして、どの述語にも合わないコマンドを汎用の `shell_exec` に落とす。原文: "a command matching no predicate resolves to the generic shell_exec rather than to nothing, so no input path fails open"。さらに自分の計測器の欠陥として次を書いている: "Errors were being silently discarded … A block that failed to classify is not a block that classified as harmless, and the two were being pooled over an unknown denominator. Both scripts now run without --fail-open and report the failure count alongside every result."。難読化ベンチマーク 64 件では "ours resolves 52%"。— [arXiv 2609.12001](https://arxiv.org/html/2609.12001v1)
- A7: "a deterministic resolver with no model in the decision path"。統計の書き方も慎重で、"Ten clean approvals cannot exclude a true failure rate of 25.9% at 95% confidence" と書く。A8/A9: 事前登録なし、修正コミットなし（記述なし）。
- 判定: **「部分的に重なる」**。宣言（文書）と実際（実行された効果の類）の照合で、決定論的な判定・fail-open の禁止・失敗件数の明示という方法論の原則は AuthGap の `opaque(reason)` と同じ向きである。ただし実際の振る舞いは動的に取り、宣言は構造化フラグではなく、静的な手続き間解析もしない。

**(3) SkillSpec — "Intent-Masked Specification Reasoning for Agent Skill Correctness"（Zhang et al.; arXiv 2609.06052v1, 2026-09-05）** ○
- A1: 宣言された意図（description / instructions）から ExpectSpec を導く。A2: コード側の FactSpec を推論する（LLM）。候補はサンドボックスで検証する。A6: "On 515 real-world skills … SkillSpec identified 763 manually confirmed defects across 239 skills, achieving 61.2% precision"。著者は "Most defects arise at the boundaries between declared intent and implementation" と書く。A7: LLM が判定に入る。A3/A5/A8/A9: 要旨に記述なし。— [arXiv 2609.06052](https://arxiv.org/abs/2609.06052)
- 判定: **「部分的に重なる」**（宣言意図と実装の不一致。ただし LLM の仕様推論で、散文が対象）。

**(4) PL-HCL — "Cross-Layer Misalignment Detection in Agent Skills"（Zhang et al.; arXiv 2607.10534, KDD 2026 Workshop）** ○
- メタデータ・手順・資源の層の間の不一致（"inconsistencies between a skill's description and its true behavior"）を、LLM ベースの対照学習で検出する。264,000 超のスキルと人手で検証した challenge set を使い、Macro-F1 は 0.87–0.89。静的解析ではない。— [arXiv 2607.10534](https://arxiv.org/abs/2607.10534)
- 判定: **「部分的に重なる」**（問題設定は同じ「記述 vs 真の振る舞い」。手法は LLM 分類器）。

**(5) "After the Party: Growth, Governance, and Security Scanning in the OpenClaw Agent Skill Ecosystem"（Xiong, Zhang; arXiv 2609.17274v2, APSEC 2026 採録）** ○
- 宣言と実際の照合ではない。"85.06% of the readable skills carry privilege evidence"、"the three security scanners disagreed on 23,702 of the 61,990 skills they all cover. After human adjudication, weighted scanner sensitivity against the reference standard ranged from 21.67% to 61.06%"。— [arXiv 2609.17274](https://arxiv.org/abs/2609.17274)
- 判定: **「隣接」**。人手裁定を基準にすると、既存のスキャナの感度が低いことを示す根拠として引用できる。

**(6) "Scanning the Harness: Configuration Exposures in AI Coding-Agent Supply Chains"（Kapner et al.; arXiv 2609.07360v3, 2026-09-25 改訂）** ◎（該当節）
- A1: 構造化された宣言（SKILL.md の `allowed-tools`、settings の許可、MCP パッケージ宣言）の**広さ**を数える。コードと照合はしない。原文: "Skill tool preapproval. 101 setups (3.8%) and 19 collections (3.7%) contain broad allowed-tools entries"。Claude Code では "The field adds preapproval rather than restricting the available tool set"。— [arXiv 2609.07360](https://arxiv.org/html/2609.07360v3)
- A5: 規則の採用条件は "at least 50 determinate findings, at least 97% mechanical agreement"。determinate でない検出は主表に入れない。A6: 3,171 リポジトリ。A7: 決定論的解析、機械的な再導出、モデル支援の裁定、人手レビューの組み合わせ。A8: 原文で否定している: "These are descriptive selection rules, not calibrated deployment guarantees or a preregistered test of a detector"。さらに "Historical label corrections and rule selection were performed on the same corpus. … False negatives and residual false positives are unknown"。母集団は "Input repository commits, scanner commits, and output records are pinned"（コミットで pin）。— [arXiv 2609.07360](https://arxiv.org/html/2609.07360v3)
- 判定: **「隣接」**。構造化宣言を扱うが、宣言そのものの広さだけを見ていて、実効と照合しない。事前登録が無く、同じコーパスで規則を選んだことを自分で認めている点は、AuthGap の凍結手続きとの対比として引用する価値がある。

**(7) SkillsMetric（Chen et al.; arXiv 2608.08468v1, 2026-08-09）** ◎（該当節）
- 5 段の静的スコアリングで、第 5 段が "capability mismatch"（宣言した SKILL.md の能力とコードの照合。ネットワークとファイルシステム）。原文で、この段の重みを最低にした理由を "metadata declarations are inconsistent across the benign corpus and yield a noisier per-stage signal" と書いている。Python/Bash/JS/Ruby に正規表現を 50 個以上使う。"host destruction attacks … evade all five stages (0% detection)"。— [arXiv 2608.08468](https://arxiv.org/html/2608.08468v1)
- 判定: **「隣接」**（悪性検出が目的で、宣言照合はその一要素にすぎない）。

**(8) ClosureBound（Zhu, Wang; arXiv 2609.05920v1, 2026-09-05）** ○ — 公開スキル 549 件の字句監査。"no root declares a frontmatter dependencies field"、"21 of 526 roots with bundled files name every non-manifest path verbatim"。原文の "metadata non-authority" を性質として証明する参照モニタの提案である。— [arXiv 2609.05920](https://arxiv.org/abs/2609.05920) 判定: **「隣接」**。

**(9) "Packaged, But Not Portable"（Sahu; arXiv 2609.23809v1, 2026-09-20）** ○ — Agent Plugins v1.0.0（2026-07-24）への準拠を調べた。68,072 バンドルのうち "Only 6.2% validate"。"40.2% would load while the specification obliges the client to discard fields their authors wrote, mostly declarations of what the plugin ships"。— [arXiv 2609.23809](https://arxiv.org/abs/2609.23809) 判定: **「隣接」**（宣言の形式への準拠であって、振る舞いではない）。

**(10) その他（照合ではない、背景）** ○
- "Agent Skills in the Wild"（arXiv 2601.10338）: 31,132 スキルで "26.1% of skills contain at least one vulnerability"。静的解析と LLM の併用で "86.7% precision and 82.5% recall"。— [arXiv 2601.10338](https://arxiv.org/abs/2601.10338) 判定: 隣接。
- "SkillScope: Toward Fine-Grained Least-Privilege Enforcement for Agent Skills"（Wu, Nan et al.; arXiv 2605.05868v3, 2026-09-10 改訂）: 宣言ではなく**ユーザのタスク**に照らした過剰権限。"validates 6,590 of 68,312 valid real-world Skills as exhibiting over-privileged behaviors"。— [arXiv 2605.05868](https://arxiv.org/abs/2605.05868) 判定: 隣接。**注意: 既知リストの "SkillScope"（He et al., "Do Skill Descriptions Tell the Truth?", arXiv 2605.12875。本文中で 33 回 "SkillScope" と名乗る）とは別の論文で、名前だけが同じ。** 引用時に取り違えないこと。
- HarnessSecurity-Bench（arXiv 2610.07639, 2026-10-06）: "allowed tools or commands can leave unauthorized operations reachable through alternative execution paths"。— [arXiv 2610.07639](https://arxiv.org/abs/2610.07639) 判定: 隣接（許可宣言が実効を縛らない例）。
- TrustProbe（arXiv 2609.39065）: エージェント実装のソースで、スキル入力から危険な操作までの source-to-sink 経路を探す。11 エージェントで 104 件。— [arXiv 2609.39065](https://arxiv.org/abs/2609.39065) 判定: 隣接。

**既知項目の新しい版**: arXiv API で 2026-10-12 時点の版を確かめた。SkillConsist 2608.07639 は v1、Semia 2605.00314 は v1、"Do Skill Descriptions Tell the Truth?" 2605.12875 は v1 で、いずれも改訂なし。— [arXiv API](https://export.arxiv.org/api/query?id_list=2605.12875,2608.07639,2605.00314)

### Inferences
- 2026 年のスキル研究は「散文やメタデータの宣言」対「コードや命令」の照合に収束しつつある。**MCP `ToolAnnotations` のような、プロトコルが定める構造化真偽ヒント**（readOnly/destructive/openWorld/idempotent）を、強制されない自己申告として扱って効果と照合する研究は、スキル分野では見つからなかった。AuthGap の新規性は「構造化フラグ × 効果の種類（書き込み/exec/ネットワーク/DB）× 手続き間の静的解析 × 未解決率の報告 × 事前登録 × 人手の正解 × 修正コミットによる recall」の組み合わせに置ける。
- BIV の "80.0%" や "LOW unverifiable text-only 28.7%" と AuthGap の数値を並べるときは、分母（スキル単位か逸脱単位か）と、宣言の取り方（LLM 抽出を含む）が違うことを必ず書く必要がある（CLAUDE.md 規則 3）。
- Scan the Skill（2609.12001）の「fail-open の禁止」「失敗件数の併記」と、Scanning the Harness（2609.07360）の「determinate な検出だけを数える」「事前登録ではないと自認」は、AuthGap の方法論の節で対比に使える。

### Gaps
- BIV の Python 解析器の手続き間の深さ、受け手型の推論、未解決呼び出しの件数は、本文の該当節に記述が無く確認できなかった（付録 G のパターン一覧までは読んでいない）。
- 2026-08〜10 に、Codex skills・Cursor rules・Claude Code plugin hooks に特化して宣言と振る舞いを照合した研究は見つからなかった。
- SkillSpec、PL-HCL、After the Party は要旨しか読んでいない（○）。未解決事例の扱いは未確認。

---

## Q2. GPTs / ChatGPT plugins / GPT Actions / Apps SDK: `x-openai-isConsequential` や Apps SDK の annotations をバックエンドの振る舞いと照合した研究はあるか。LLM アプリストアで宣言と振る舞いを比べた研究は何を比べたか

### Takeaway
`x-openai-isConsequential` と Apps SDK の `readOnlyHint`/`destructiveHint`/`openWorldHint` を**バックエンドのコードや振る舞いと照合した研究は見つからなかった**（standard と extended の検索、arXiv API で確認）。公式文書は、これらが提示（確認プロンプト）を変えるだけで強制ではないと明言している。LLM アプリストアの研究（Hou et al.）が比べたのは、「説明文 vs 指示文（どちらも自然言語）」と「Action スキーマのデータ型 vs ストアのプライバシーポリシー（どちらも宣言）」で、コードではない。

### Cited Findings
- **OpenAI 公式: `x-openai-isConsequential`** ○ — "If the field isn't present, ChatGPT defaults all GET operations to `false` and all other operations to `true`."。true のときは毎回確認を求めて "always allow" を出さない。false のときは "always allow" を出す。— [OpenAI Actions production docs](https://developers.openai.com/api/docs/actions/production)（旧 URL は platform.openai.com/docs/actions/production から 301 で移った）
- **OpenAI 公式: Apps SDK の tool annotations** ○ — readOnlyHint・destructiveHint・openWorldHint は Required、idempotentHint は Optional。ヒントは "only influence how ChatGPT or Codex frames the tool call to the user" であり、"servers must still enforce their own authorization logic"。readOnlyHint の定義は "Signal that the tool only retrieves or computes information and doesn't create, update, delete, or send data … outside the conversation"。— [Apps SDK Reference](https://developers.openai.com/apps-sdk/reference)（WebFetch の要約を通した引用なので、原文の字句は要再確認）
- **Hou, Zhao, Wang "On the (In)Security of LLM App Stores"（arXiv 2407.08422v2）** ◎（HTML 全文の該当節）
  - A1: 説明文（自然言語、強制なし）と、Action スキーマ（OpenAPI、宣言）。A2: 指示文と説明文の一致度を LLM に採点させる。Action スキーマのデータ型をストアのプライバシーポリシー（Polisis で抽出）と比べる。A3: 該当なし（コードを解析しない）。A6: 6 ストアの 786,036 アプリ。"35.31% of the 42,892 examined LLM apps had inconsistencies between descriptions and instructions"、要旨では "15,146 apps had misleading descriptions, 1,366 collected sensitive personal information against their privacy policies"。A5: "If the tool fails to produce a correct output, it attempts the check up to three times. Persistent errors are flagged for external review." — 失敗は外部レビューに回すが、その件数は確認できなかった。A7: LLM が判定に入る。A8/A9: なし。— [arXiv 2407.08422](https://arxiv.org/html/2407.08422v2)
  - 判定: **「隣接」**（照合しているのは宣言同士、または散文同士で、効果を実装から推論していない）。
- **Iqbal, Kohno, Roesner "LLM Platform Security: Applying a Systematic Evaluation Framework to OpenAI's ChatGPT Plugins"（AIES 2024; arXiv 2309.10254）** ○ — 攻撃分類を作り、plugin エコシステムに当てはめて "We uncover plugins that concretely demonstrate the potential for the types of issues that we outline"。照合率の測定ではない。— [arXiv 2309.10254](https://arxiv.org/abs/2309.10254) 判定: 隣接。
- **Yan et al. "Exploring ChatGPT App Ecosystem: Distribution, Deployment and Security"（ASE 2024; arXiv 2408.14357）** ○ — "We also identify severe flaws in the authentication and user data protection for third-party app APIs"。宣言と振る舞いの照合ではない。— [arXiv 2408.14357](https://arxiv.org/abs/2408.14357) 判定: 隣接。
- **Rodriguez et al. "Towards Safer Chatbots: Automated Policy Compliance Evaluation of Custom GPTs"（arXiv 2502.01436v3）** ○ — ブラックボックスの対話と LLM-as-a-judge を使い、判定器を人手注釈の正解で検証して F1 0.975。782 GPTs で "58.7% … exhibit at least one policy-violating response"。比べているのは利用ポリシーと振る舞いで、開発者の宣言ではない。— [arXiv 2502.01436](https://arxiv.org/abs/2502.01436) 判定: 隣接。
- **Wei et al. "Privacy and Security Threat for OpenAI GPTs"（arXiv 2506.04036）** ○ — "738 custom GPTs collect user conversational information, and identified 8 GPTs exhibiting data access behaviors that are unnecessary for their intended functionalities"。— [arXiv 2506.04036](https://arxiv.org/abs/2506.04036) 判定: 隣接。

### Inferences
- `isConsequential`（GET 以外は既定 true）と Apps SDK の annotations は、MCP `ToolAnnotations` と同じく「強制されない自己申告が UI の確認だけを変える」構造である。AuthGap の結果は、この 2 つにも当てはまる外的妥当性の議論として書ける（ただし実測は無い）。特に `isConsequential: false` を付けた POST/DELETE 操作が書き込みをする事例は、AuthGap の「宣言が狭すぎる」方向そのものだが、測定した研究は見つからなかった。
- Hou et al. の「説明 vs 指示」35.31% は散文同士の不一致なので、AuthGap の矛盾率と並べてはいけない。

### Gaps
- ChatGPT Apps（Apps SDK, 2025-10 以降）の公開アプリについて、annotations を集計した研究、あるいはバックエンドと照合した研究は見つからなかった（標準検索 "ChatGPT apps SDK readOnlyHint annotation measurement study" と arXiv の "tool annotations OR readOnlyHint OR destructiveHint" で、ヒットは WebMCP の攻撃論文 2606.06387 だけ）。
- GPT Actions のバックエンドはソースが公開されていないことが多く、静的照合の母集団を作れないことが研究の空白の原因かもしれない（推測。根拠は無い）。

---

## Q3. 音声アシスタントスキル（Alexa / Google Assistant）: 何と何を比べたか。テストできない・決定できない事例をどう扱ったか

### Takeaway
最も AuthGap に近い古典は **SkillScanner（CCS 2023）** である。スキルの manifest にある**開発者の自己申告の yes/no**（データを集めるか）と、manifest の permissions を、ソースコードの静的 taint 解析（CodeQL）と照合している。データ収集のあるスキルで選択肢を選んでいた 126 件のうち、99 件が「個人情報を使わない」と申告していた（宣言が狭すぎる向き）。ほかの音声スキル研究（SkillExplorer、SkillDetective、Lentzsch、Dangerous Skills Got Certified、SkillVet）は、動的な対話テストか、権限とプライバシーポリシーの照合で、コードの静的解析ではない。テストできない事例の率を体系的に報告したものは見つからなかった。

### Cited Findings
- **SkillScanner（Liao, Cheng, Cai; CCS 2023）** ◎（NSF PAR の PDF 全文の該当節）
  - A1: 2 種類の宣言がある。(a) skill manifest の `permissions`（Alexa の権限。利用には権限の付与が要る）。(b) 提出時の自己申告。原文: "Amazon asks developers whether their skills collect user data before submission and developers can select yes or no by themselves. The answers will be stored in the skill manifest file"（manifest の `privacyAndCompliance` 内。強制されない構造化フラグ）。— [SkillScanner PDF (NSF PAR)](https://par.nsf.gov/servlets/purl/10527328)
  - A2/A3/A4: 静的解析。原文: "we use the CodeQL tool [8] that supports multiple programming languages to track data flows"。taint の source はスロット値と permission API、sink は DB と音声出力。対象は "the back-end code is written in JavaScript or Python"。手続き間かどうかは論文に明記が無い（CodeQL のデータフローは一般に手続き間だが、論文の主張ではない）。— [SkillScanner PDF](https://par.nsf.gov/servlets/purl/10527328)
  - A6: GitHub のオープンソーススキル 2,451 件。"1,328 different types of policy violations among 786 skills"。照合の結果は 3 つ。"There are 42 skills that request for permissions but don't use them. There are also 18 skills that get permission data without requesting for permissions." と "There are 126 skills with data collection in our dataset making a selection, in which 99 skills claim not using personal info while only 27 developers correctly select they use personal info."。性能は "we manually checked all the detected results … randomly selected 100 skills from our dataset and manually labeled them … overall 90% precision and 87% recall"。— [SkillScanner PDF](https://par.nsf.gov/servlets/purl/10527328)
  - A5: 解析できなかったものの率は報告していない。偽陰性の原因の一つとして、呼び出し名の検査で "The false negatives are mainly due to the failure to read the skill file with errors" と書くだけである。A7: CodeQL とキーワードによる決定論的な判定で、LLM は使わない。A8: なし。A9: 修正コミットは使っていない（公開版との対照で "4 policy-violating skills have been published on the skills store without fixing them" と書く）。
  - 判定: **「大きく重なる」**（古典の中で最も近い）。強制されない構造化の自己申告フラグを、ソースの静的解析と照合して「狭すぎる申告」（99/126）を数えた。違いは、対象がデータ収集であって副作用（書き込み/exec）ではないこと、母集団が小さく GitHub 由来であること、未解決率と事前登録が無いこと。
- **SkillExplorer（Guo, Lin, Li, Chen; USENIX Security 2020）** ○ — "grammar-based techniques including utterance extraction" で対話的に探索する動的手法。"28,904 skills from the Amazon market and 1,897 actions from the Google market"。"1,141 skills request users' private information without following developer specifications"、"68 skills continue to eavesdrop"。— [USENIX Sec 2020](https://www.usenix.org/conference/usenixsecurity20/presentation/guo) 判定: **隣接**（規約 vs 動的な振る舞い）。
- **SkillDetective（Young, Liao, Cheng, Hu, Deng; USENIX Security 2022）** ○ — 動的な対話テストで "52 different policy requirements" への適合を見る。"we tested 54,055 Amazon Alexa skills and 5,583 Google Assistant actions"、"6,079 skills and 175 actions violating at least one policy requirement"。— [USENIX Sec 2022](https://www.usenix.org/conference/usenixsecurity22/presentation/young) 判定: **隣接**。
- **Lentzsch et al. "Hey Alexa, is this Skill Safe?"（NDSS 2021）** ○ — 90,194 スキル。審査の限界として "make backend code changes after approval to coax users into revealing unwanted information"。"around 23.3% of such skills do not fully disclose the data types associated with the permissions requested"（権限 vs プライバシーポリシー）。— [NDSS 2021](https://www.ndss-symposium.org/ndss-paper/hey-alexa-is-this-skill-safe-taking-a-closer-look-at-the-alexa-skill-ecosystem/) 判定: **隣接**。「承認後にバックエンドが変わる」という指摘は、AuthGap がインストール前のソースを SHA で固定して解析する理由（rug-pull 型の変化）の先例として引ける。
- **Cheng et al. "Dangerous Skills Got Certified"（CCS 2020, DOI 10.1145/3372297.3423339）** △（検索要約経由） — 規約違反のスキル 234 件と Google actions 381 件を提出し、Alexa の 234 件はすべて認定されたと報告。— [UB Research Connect](https://researchconnect.buffalo.edu/en/publications/dangerous-skills-got-certified-measuring-the-trustworthiness-of-s/) 判定: **隣接**（審査が宣言を検証しない根拠）。
- **SkillVet（Edu, Ferrer-Aran, Such, Suarez-Tangil; IEEE TDSC 短縮版、arXiv 2103.02637v2）** ◎（該当節）/○ — 199,295 スキル。権限（Alexa の API で強制される）とプライバシーポリシー（散文）の traceability を complete / partial / broken の 3 値で付ける。"around 43% of the skills (and 50% of the developers) that request these permissions follow bad privacy practices"。ML/NLP を使い "generates high-accuracy prediction sets"。コードは解析しない。— [arXiv 2103.02637](https://arxiv.org/html/2103.02637v2) 判定: **隣接**。
- **Liao et al. "Measuring the Effectiveness of Privacy Policies for Voice Assistant Applications"（ACSAC 2020; arXiv 2007.14570）** ○ — 64,720 の Alexa スキルと 2,201 の Google actions のプライバシーポリシーの質。— [arXiv 2007.14570](https://arxiv.org/abs/2007.14570) 判定: 隣接。

### Inferences
- SkillScanner の「99/126 が個人情報不使用と申告」は、**強制されない構造化フラグは狭い側（安全側の自己申告）に偏る**という AuthGap の作業仮説の、別領域での先例として引用できる。ただし分母は「データ収集があり、かつ申告欄を埋めたスキル」で、母集団は GitHub 公開のものに偏っている。
- 同じ論文の「42 件は権限を要求して使わない」（過剰）と「18 件は要求せずに使う」（過少）は、強制される権限では過剰の側が多いという Stowaway 型の傾向と矛盾しない（推論）。

### Gaps
- SkillExplorer と SkillDetective が、探索できなかったスキル（対話が途切れたもの、認証が必要なもの）を何件除外したかは、要旨からは確認できなかった（全文は未読）。
- SkillScanner が CodeQL の解析に失敗したリポジトリの数は、該当節には書かれていなかった。

---

## Q4. ブラウザ拡張: 古典的な過剰権限研究と MV3 以降の研究は、静的か動的か。解決できないコードをどう扱ったか

### Takeaway
古典の Felt, Greenwood, Wagner（WebApps 2011）は、拡張のソース（遠隔から読み込むスクリプトを含む）を文字列で検索して「要求したが使わない」browser manager を数え、1,000 件中 14.7% が過剰権限と報告した。**名前が文字列連結で組み立てられて検索で見つからない事例**（"book"+"marks"）は、15 件の無作為標本を見て「証拠なし」と処理しており、決定できない事例の扱いの古い先例になる。VEX（2010）は、eval に流れる非定数文字列を無視するので健全ではないと明記している。権限は強制されるので、どの研究も過剰（over）の向きを測っている。MV3 以降に、未解決率を報告する静的な過剰権限研究は見つからなかった。

### Cited Findings
- **Felt, Greenwood, Wagner "The Effectiveness of Application Permissions"（USENIX WebApps 2011）** ◎（PDF の該当節）
  - A1: Chrome の manifest の権限（強制される）。A2: 静的な文字列検索。原文: "We search their source code (including remotely sourced scripts) for references to their requested browser managers. 14.7% of the 1000 extensions are overprivileged by this measure"。A5: 原文: "It is possible for an extension to name a browser manager without explicitly including the name as a string (e.g., "book"+"marks"); we examined a random sample of 15 overprivileged extensions and found no evidence of developers doing this."。さらに "Our text search has a small number of false positives; e.g., we found three extensions that only contain references to browser managers in remotely sourced scripts"。ドメイン権限は手作業で調べ、50 件中 web データにアクセスする 41 件のうち 7 件が過剰。A7: 決定論的。A8/A9: なし。— [WebApps 2011 PDF](https://people.eecs.berkeley.edu/~daw/papers/perms-webapps11.pdf)
  - 判定: **「隣接」**（強制される権限で過剰の向き。文字列検索だけで手続き間解析はしない）。それでも「解決できない名前の構成を標本で潰す」手続きの古い先例として引用する価値がある。
- **Carlini, Felt, Wagner "An Evaluation of the Google Chrome Extension Security Architecture"（USENIX Security 2012）** ○ — "performed a security review of 100 Chrome extensions and found 70 vulnerabilities across 40 extensions"。isolated worlds・privilege separation・権限の有効性を評価し、"banning HTTP scripts and inline scripts would prevent 47 of the 50 most severe vulnerabilities"。宣言と振る舞いの照合ではない。— [USENIX Sec 2012](https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/carlini) 判定: **隣接**。
- **Bandhakavi et al. VEX（USENIX Security 2010）** ◎（PDF の該当節） — "high-precision, context-sensitive, flow-sensitive static analysis" で Firefox 拡張の情報フローを追う。健全性について原文で "… statically known but subject to eval are essentially ignored, and this causes our tool to be unsound"（PDF の抽出テキストでは文の主語が段組みで切れていて、何が無視されるのかの字句は取れなかった。続く文は "In most correct extensions, an eval-ed statement is dynamically chosen from a set of constant-strings or taken from trusted sources"）。目的は脆弱性検出で、宣言との照合ではない。— [VEX PDF](https://www.usenix.org/legacy/events/sec10/tech/full_papers/Bandhakavi.pdf) 判定: **隣接**。
- **Guha, Fredrikson, Livshits, Swamy "Verified Security for Browser Extensions"（IEEE S&P 2011, IBEX）** ○ — ポリシーを Datalog で宣言させ、"a static check for policy compliance" で検証する。17 の拡張を実装・検証した。逆向きの設計で、宣言を検証可能にして強制する。— [Guha IBEX page](https://people.cs.umass.edu/~arjun/main/papers/2011-guha-oakland.html) 判定: **隣接**。宣言を検証可能にする方向の対案として、議論の節で触れられる。
- **Pantelaios, Kapravelos "Manifest V3 Unveiled"（arXiv 2404.08310）** ○ — 517 件の悪性拡張を動的に実行して "a 87.8% removal of APIs related to malicious behavior"。PoC の改変後に "290 (56%) … retain their capability to conduct harmful activities"。— [arXiv 2404.08310](https://arxiv.org/abs/2404.08310) 判定: 隣接。
- **Hsu, Tran, Fass "What is in the Chrome Web Store?"（AsiaCCS 2024; arXiv 2406.12710）** ○ — 照合ではない（保守されていない状況と Security-Noteworthy Extensions を扱う）。— [arXiv 2406.12710](https://arxiv.org/abs/2406.12710) 判定: 隣接。
- （既知の Picazo et al. について新しい事実は無い。検索要約では 39.8% が least privilege 準拠、8.5% が underprivileged と出たが、これは既知の項目。△ — [research.chalmers.se](https://research.chalmers.se/en/publication/532102)）

### Inferences
- ブラウザ拡張の系譜は、強制される権限が対象なので「過剰」を測り、静的解析は文字列検索か健全でない情報フロー解析である。AuthGap の「強制されない宣言で、狭すぎる側を測る」という向きの対比として使える（Felt 2011 = 強制あり → over、SkillScanner = 強制なしの自己申告 → under）。

### Gaps
- MV3 以降（2023–2026）に、権限宣言と使用を静的に照合し、解決できない API 参照の率を報告した研究は見つからなかった。SBSEG 2025 の 287 件の監査は検索スニペットでしか見ておらず（△、[cin.ufpe.br PDF](https://www.cin.ufpe.br/~amb4/assets/sbseg2025_1.pdf)）、方法は未確認。
- Chrome Web Store の "Privacy practices" 表示を、コードの静的解析で検証した研究は、既知の ExtPrivA（動的なトラフィック）以外に見つからなかった。

---

## Q5. ミニプログラム（WeChat / Alipay / TikTok / Telegram Mini Apps）: 宣言（プライバシーポリシー・権限・プライバシー指引）とコードを照合した研究、未解決率の報告

### Takeaway
WeChat ミニプログラムでは、JS の taint 解析と**プライバシーポリシー（散文）**を照合する研究が多い（MiniDetector で 89.4% 不一致、MiniScope で過剰収集 5.7%・過大申告 33.4%、SPOChecker で 19.47%）。**構造化された宣言**（app.json の `requiredPrivateInfos` や「用户隐私保护指引」）をコードと照合した研究は見つからなかった。MiniScope は、静的解析だけでは非標準構造のアプリで偽陰性が出ること（正解集合の 1.3% が該当し、静的のみの偽陰性率は約 11.0%）を報告しているが、ポピュレーション全体の未解決率は報告していない。2026-08 には Telegram Mini Apps の動的な研究（TeleGapper）が出た。

### Cited Findings
- **MiniDetector — "Do as You Say: Consistency Detection of Data Practice in Program Code and Privacy Policy in Mini-App"（Wang et al.; arXiv 2302.13860）** ○
  - A1: プライバシーポリシー（散文。プラットフォームは中身を強制しない）。A2/A4: "we first customize a taint analysis method based on data entity dependency network to adapt to the characteristics of the JavaScript language in the mini-apps"（静的）。A6: "We crawl 100,000 mini-apps … extract 2,998 with a privacy policy. Among them, only 318 meet the consistency requirements, 2,680 are inconsistent, and the proportion of inconsistencies is as high as 89.4%"。A3/A5/A8/A9: 要旨に記述なし。— [arXiv 2302.13860](https://arxiv.org/abs/2302.13860)
  - 版の食い違い（△）: 検索要約によると、学術誌版（IEEE TSE とされる）は「3,369 件中 11 件だけが一致、99.7% 不一致」と、arXiv 版と違う値を出しているという。こちらでは未確認。— [WebSearch 要約が示した arXiv/学術誌版](https://arxiv.org/pdf/2302.13860)
  - 判定: **「部分的に重なる」**（静的 taint と宣言の照合で母集団の不一致率を出している。宣言は散文で、効果ではなくデータの実践）。
- **MiniScope（Wang et al.; ACM TOSEM; arXiv 2401.03218v3）** ◎（HTML 全文の該当節）
  - A1: プライバシーポリシー（GPT-3.5-Turbo で抽出）。WeChat のガイドラインにも触れる。A2: 静的解析（MiniApp Dependency Graph）に、UI を自動で探索して subpackage を動的に読み込む処理を組み合わせたハイブリッド。"cross-package callback control flow resolution"。A6: "over 120K MiniApps"、"5.7% of the MiniApps are secretly over-collecting private data, and 33.4% of the MiniApps overclaim the data they actually collect"。正解は 100 件の MiniApp を研究者 3 人が操作して作り、"99.2% precision, 95.6% recall"。開示は "2,282 developers, receiving 44 acknowledgments"。— [arXiv 2401.03218](https://arxiv.org/html/2401.03218v3)
  - A5: 原文: "Certain MiniApps, developed using third-party multi-end frameworks … may not have a standard page structure after unpacking. This situation, affecting around 1.3% of our ground truth dataset, contributes to an approximately 11.0% false negative rate in static-only analysis."。全体の未解決率は報告していない。違反の内訳は "Redundant Disclosure (13.1% of all cases) significantly outweighs Omitted Disclosure (1.1%)"（過大申告が多い）。A7: LLM が判定に入る（ポリシー側）。A8/A9: なし。— [arXiv 2401.03218](https://arxiv.org/html/2401.03218v3)
  - 判定: **「部分的に重なる」**。
- **SPOChecker — "Understanding Privacy Over-collection in WeChat Sub-app Ecosystem"（Zhang et al.; arXiv 2306.08391）** ○ — 5,521 のサブアプリ。"Among 2,511 sub-apps that provide privacy policies, 489 (19.47%) of them contain SPO"。— [arXiv 2306.08391](https://arxiv.org/abs/2306.08391) 判定: **部分的に重なる**（宣言は散文）。
- **TeleGapper（Ferrari, Ceccato, Verderame; arXiv 2608.13390, 2026-08-13）** ○（新しい） — ブラックボックスの動的ネットワーク解析。278 の Telegram Mini Apps。"59.4% contact at least one undisclosed third party, 78.8% rely exclusively on Telegram's default privacy policy"。— [arXiv 2608.13390](https://arxiv.org/abs/2608.13390) 判定: **隣接**。
- **"A Small Leak Will Sink Many Ships"（Zhang et al.; arXiv 2205.15202）** ○ — 9 つのホストアプリ、2,580 超の API で権限管理の脆弱性 6 類型。照合率の研究ではない。— [arXiv 2205.15202](https://arxiv.org/abs/2205.15202) 判定: 隣接。
- **"A Hybrid Security Framework for Mini-Programs"（arXiv 2608.25877, 2026-08）** ○ — UI 適合（YOLOv8）と mitmproxy。宣言との照合ではない。— [arXiv 2608.25877](https://arxiv.org/abs/2608.25877) 判定: 隣接。

### Inferences
- ミニプログラムの研究で「過大申告（over-claim）」が多いのは、テンプレートのプライバシーポリシーの流用によるとみられる（MiniDetector の著者も "the straightforward use of templates" を挙げている — [arXiv 2302.13860](https://arxiv.org/abs/2302.13860)）。AuthGap では annotations が省略可能で、既定値の扱いが方向を左右しうるので、「既定値・未記入」を宣言の値と分けて数える必要がある（推論）。

### Gaps
- WeChat の `requiredPrivateInfos`（app.json の構造化宣言。対象 API は宣言しないと実行時に失敗するとされる）と、隐私保护指引（2023 年以降）について、宣言と実際の API 使用を照合した研究は見つからなかった（extended 検索 "WeChat mini program requiredPrivateInfos privacy guide declaration actual API usage measurement study"。この field の強制挙動そのものも公式文書では未確認）。
- Alipay・TikTok（抖音）のミニプログラムに特化した宣言照合の研究は見つからなかった。
- MiniDetector の学術誌版の数値は一次資料で確認していない。

---

## Q6. VS Code / IDE 拡張、Copilot 拡張、npm/PyPI の能力宣言

### Takeaway
VS Code の `package.json` には、**開発者の自己申告の構造化フラグ** `capabilities.untrustedWorkspaces.supported`（true / false / "limited"）がある。Edirimannage et al. は true の拡張を 542 件数えたが、**フラグとコードの振る舞いを照合した研究は見つからなかった**。UntrustIDE（NDSS 2024）は CodeQL の taint 解析で脆弱性を探すが、「ユーザが restricted mode を無効にした」と仮定していて、フラグは評価していない。npm では Ferreira et al.（ICSE 2021）が manifest に権限を宣言させる設計を提案し、静的に除外できないアクセスに動的検査を挿入する（未解決を保守的に扱う先例）。Copilot 拡張の研究は見つからなかった。

### Cited Findings
- **Edirimannage et al. "Developers Are Victims Too: A Comprehensive Analysis of The VS Code Extension Ecosystem"（arXiv 2411.07479）** ◎（HTML 全文の該当節）
  - A1: `capabilities.untrustedWorkspaces.supported`。原文: "Given that this is a flag the developer voluntarily sets, a malicious developer can set it to true so that the malicious extensions can still be active in the restricted mode of the VS Code. Our testing found 542 extensions with the property set as true."。VS Code 全体について "The absence of any sort of permission in VS Code keeps developers completely in the dark about extension's execution."。A2: 静的（manifest と API 使用）と動的（計装した VS Code と mitmproxy）。A6: 52,880 拡張、要旨によると 5.6% に不審な振る舞い。フラグとコードの照合率は出していない。— [arXiv 2411.07479](https://arxiv.org/html/2411.07479v1)
  - 判定: **「隣接」**。ただし、強制されない構造化自己申告フラグが存在するのに照合されていない領域として、AuthGap の手法を広げる先（将来研究）に挙げられる。
- **Lin et al. "UntrustIDE: Exploiting Weaknesses in VS Code Extensions"（NDSS 2024）** ◎（PDF の該当節） — CodeQL で taint の source と sink を定義し、"25,402 extensions had JavaScript or TypeScript code" を解析。要旨で "21 extensions with verified proof of concept exploits"。前提として "(3) Disabled Restricted Mode: The user explicitly disabled the restricted mode after cloning a potentially untrusted repository." を置くので、宣言（ワークスペース信頼への対応）と振る舞いの照合はしていない。PoC で確認できなかった事例は "we could not confirm proof of concepts" のように個別に書いている。— [NDSS 2024 PDF](https://www.ndss-symposium.org/wp-content/uploads/2024-73-paper.pdf) 判定: **「隣接」**。
- **Ferreira, Jia, Sunshine, Kästner "Containing Malicious Package Updates in npm with a Lightweight Permission System"（ICSE 2021; arXiv 2103.05769）** ◎（PDF の該当節） — 提案は "Package owners are expected to manually declare required permissions in the package's manifest file before publishing"。強制は静的解析と動的検査の併用で、原文は "Since we cannot fully statically reason about property access in JavaScript, we combine static analysis with selected dynamic checks … insert dynamic checks for every property access for which we cannot statically exclude that it may access a restricted property"。評価は "31.9% of all npm packages can be protected by our design"。— [arXiv 2103.05769](https://arxiv.org/pdf/2103.05769v1) 判定: **「隣接」**（宣言を強制する仕組みの提案で、既存の宣言と振る舞いの不一致の測定ではない）。
- （既知の Mir、CCS 2021 について新しい事実は無い。）

### Inferences
- VS Code の `untrustedWorkspaces.supported: true` は「信頼されないワークスペースでも安全に動く」という自己申告で、読み取りだけのつもりの宣言が実は exec を含む、という AuthGap と同じ型の矛盾が起こりうる。照合研究が見当たらないので、AuthGap の議論の節で「同型の未検証フラグ」の例として挙げられる（推論。実測は無い）。

### Gaps
- GitHub Copilot Extensions について、宣言と振る舞いを照合した研究は見つからなかった（arXiv の "Copilot AND extension* AND security" は 0 件）。
- PyPI の能力宣言の提案（manifest で権限を宣言させるもの）は、本調査の範囲では見つからなかった。

---

## Q7. HarmonyOS / Android のプライバシーラベル（既知の Lalaine・Koch・Arkalakis 以外で新しく出たもの）

### Takeaway
HarmonyOS（AppGallery）のプライバシーラベルを**コード**と照合した研究は見つからなかった。2026 年の TU Wien の修士論文は、同じアプリについて AppGallery と Google Play の**ラベル同士**を比べ、平均一致度 55.22% と報告している。ArkTS の静的解析基盤（ArkAnalyzer）は出ているが、ラベル照合への応用は見つからなかった。

### Cited Findings
- **Wagner "Mining and verification of mobile app store privacy labels: a comparative study of Huawei AppGallery and Google Play Store"（TU Wien Diplomarbeit, 2026; 指導 Lindorfer）** ○ — 約 80,064 の Huawei アプリと 112,814 の Google Play アプリから、店舗をまたぐ 2,839 組を作り、比較できる 1,527 組で "average data item match score … 55.22%"、完全一致は 32 組（2.10%）、"69.55% show discrepancies in both directions"。コードによる検証は（ページ上では）していない。— [TU Wien repositum](https://repositum.tuwien.at/handle/20.500.12708/229415) 判定: **隣接**（宣言同士の比較）。
- **ArkAnalyzer（ICSE-SEIP 2025; arXiv 2501.05798）** △（検索要約） — OpenHarmony/ArkTS の静的解析基盤で、"privacy leaks detection" などの解析器を作れるという。ラベル照合そのものではない。— [ICSE 2025 SEIP](https://conf.researchr.org/details/icse-2025/icse-2025-software-engineering-in-practice/28/ArkAnalyzer-The-Static-Analysis-Framework-for-OpenHarmony) 判定: 隣接。
- **Pan, Ge, Sun "A First Look at Privacy Risks of Android Task-executable Voice Assistant Applications"（APSEC 2025; arXiv 2509.23680）** ○ — 10 の VA アプリについて "cross-check their privacy declarations across six sources, including privacy labels, policies, and manifest files … reveal widespread inconsistencies"。— [arXiv 2509.23680](https://arxiv.org/abs/2509.23680) 判定: 隣接。
- **Pan et al. "SoK: From Generation to Consumption of Privacy Documents in Software Systems"（NDSS 2027 採録; arXiv 2608.12511）** ○ — 2010–2025 の論文 290 本の SoK。今後の方向として "LLM-based unified policy-code analysis" を挙げる。— [arXiv 2608.12511](https://arxiv.org/abs/2608.12511) 判定: 隣接（文献地図として使える）。

### Inferences
- プライバシーラベルの系譜（Lalaine など）は「データの種類」の宣言で、AuthGap の「副作用の種類」の宣言とは対象が違う。それでも、強制されないラベルという点では同じ構造なので、関連研究の節では 1 段落でまとめれば足りる（推論）。

### Gaps
- HarmonyOS NEXT の権限宣言（module.json5 の requestPermissions）と ArkTS コードの使用を照合した研究は見つからなかった。

---

## Q8. 横断: AuthGap が必ず引用すべきもの、重複しない点、検索の記録

### Takeaway
必ず引用すべきものは 3 本。(1) **BIV（2605.11770）**: 宣言集合と実装集合の差を、Python の AST 手続き間解析で数える最近接の先行研究。(2) **SkillScanner（CCS 2023）**: 強制されない構造化の自己申告フラグとソースの静的解析の照合で、99/126 が狭すぎる申告。(3) **Scan the Skill（2609.12001）**: 決定論的な判定と fail-open の禁止、失敗件数の明示。ここまで見た範囲で、①構造化された真偽の副作用ヒント、②手続き間の静的解析、③未解決（opaque）率の報告、④事前登録と凍結、⑤人手の正解、⑥開発者の修正コミットによる recall、の**すべてを満たす研究は見つからなかった**。どの先行研究も、③④⑥のどれかを欠く。

### Cited Findings
- 未解決・決定不能の扱いの比較（各研究の原文は上の節を参照）:
  - BIV: 下限として扱い、率は出さない。逸脱の確度を 3 段に分ける（28.7% は LOW unverifiable）。— [arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)
  - Scan the Skill: 分類できなかったものを無害と合算しない。失敗件数を併記し、未知の入力は `shell_exec` に落とす（全域関数）。— [arXiv 2609.12001](https://arxiv.org/html/2609.12001v1)
  - Scanning the Harness: determinate な検出の数を規則の採用条件にし、事前登録ではないと自認。— [arXiv 2609.07360](https://arxiv.org/html/2609.07360v3)
  - Felt 2011: 文字列連結による名前を 15 件の標本で確かめた。— [WebApps 2011](https://people.eecs.berkeley.edu/~daw/papers/perms-webapps11.pdf)
  - VEX: eval の非定数を無視し、健全でないと明記。— [VEX](https://www.usenix.org/legacy/events/sec10/tech/full_papers/Bandhakavi.pdf)
  - Ferreira: 静的に除外できないアクセスには動的検査を挿入（保守側に倒す）。— [arXiv 2103.05769](https://arxiv.org/pdf/2103.05769v1)
  - MiniScope: 非標準構造による偽陰性を正解集合で見積もる（1.3% → 約 11.0% FN）。— [arXiv 2401.03218](https://arxiv.org/html/2401.03218v3)
  - Hou et al.: 失敗したら 3 回まで再試行し、残りは外部レビューに回す。— [arXiv 2407.08422](https://arxiv.org/html/2407.08422v2)
- 判定の一覧（新規分）:

| 研究 | 年 / 会議 | 宣言（強制） | 実際の取り方 | 手続き間 | 未解決率 | 人手の正解 | LLM が判定に入る | 事前登録 | 修正コミット | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| BIV 2605.11770 | 2026-05 arXiv | frontmatter と散文の能力（強制なし） | 静的（Py AST taint）と LLM | Py のみ手続き間 | 無し（下限と確度 3 段） | 無し（LLM パネル） | 入る | 無し | 無し | 大きく重なる |
| SkillScanner | CCS 2023 | manifest の yes/no と permissions（申告は強制なし） | 静的（CodeQL） | 明記なし | 無し | 有り（100 件、P90/R87） | 入らない | 無し | 無し | 大きく重なる |
| Scan the Skill 2609.12001 | 2026-09 arXiv | SKILL.md 文書（強制なし） | 動的と決定論的リゾルバ | 該当せず | 失敗件数を併記 | 手作業 100 件の監査 | 入らない | 無し | 無し | 部分的に重なる |
| SkillSpec 2609.06052 | 2026-09 arXiv | 記述・指示（散文） | LLM 推論とサンドボックス | 不明 | 不明 | 手動確認 | 入る | 無し | 無し | 部分的に重なる |
| PL-HCL 2607.10534 | KDD-W 2026 | メタデータ（散文） | LLM 対照学習 | 該当せず | 不明 | challenge set | 入る | 無し | 無し | 部分的に重なる |
| MiniDetector 2302.13860 | arXiv / TSE | プライバシーポリシー | 静的 JS taint | 不明 | 不明 | 不明 | 不明 | 無し | 無し | 部分的に重なる |
| MiniScope 2401.03218 | TOSEM | プライバシーポリシー | 静的と動的 | callback 解決 | 正解集合での FN 見積り | 有り（100 件） | 入る（ポリシー側） | 無し | 無し | 部分的に重なる |
| Scanning the Harness 2609.07360 | 2026-09 arXiv | allowed-tools など（構造化） | 宣言だけ | 該当せず | determinate のみ | 人手レビュー | 一部入る | 無し（明言） | 無し（ただし commit pin） | 隣接 |
| Felt 2011 | WebApps | manifest 権限（強制あり） | 文字列検索 | 無し | 標本 15 件 | 手作業 50 件 | 入らない | 無し | 無し | 隣接 |
| Edirimannage 2411.07479 | arXiv | untrustedWorkspaces（強制なし） | 静的と動的 | — | — | — | — | 無し | 無し | 隣接 |

（表の「不明」は、要旨・該当節に記述が無く確認できなかったもの。黙って「無し」にしていない。）

### Inferences
- **向きの対比**（推論）: 強制される宣言（Chrome の権限、Felt 2011）では過剰が測られる。強制されない自己申告（Alexa の申告、SkillScanner の 99/126。スキル、BIV の under-spec 135,187 / 250,706 ≈ 54%）では狭すぎる側が目立つ。散文のポリシー（MiniScope）では過大申告が多い。AuthGap の「強制されないので狭すぎる側を測る」という主張を支える周辺の証拠になるが、分母と単位が揃っていないので、数値を直接並べてはいけない。
- **差別化の書き方**: 「静的・決定論的・手続き間・構造化フラグ」の組み合わせで最も近いのは SkillScanner（データ収集、CodeQL）と BIV（能力集合、Python AST）。AuthGap は、(a) 副作用の真偽ヒント（readOnly/destructive/openWorld/idempotent）を対象にすること、(b) `opaque(reason)` の率を主指標と並べて出すこと、(c) 事前登録と解析器の凍結、(d) 修正コミットによる recall で区別できる。

### Gaps

#### 見つからなかったもの（まとめ）
- `x-openai-isConsequential` や Apps SDK の annotations を照合した研究。
- WeChat の `requiredPrivateInfos` / 隐私保护指引と、コードの照合。
- VS Code の `untrustedWorkspaces` フラグと、コードの照合。
- HarmonyOS のラベルや権限と、ArkTS コードの照合。
- Copilot Extensions の研究。
- 事前登録した宣言照合研究（どの領域でも）。
- 開発者の修正コミットを recall の基準に使った宣言照合研究（どの領域でも）。

#### 実行した検索クエリ（結果つき）
WebSearch:
1. "agent skills declared permissions vs actual code behavior static analysis arXiv 2026"（extended）→ BIV、SkillsMetric、SkillGuard など。
2. "x-openai-isConsequential GPT Actions consequential flag study" → フォーラムのみ。**研究は見つからなかった**。
3. "WeChat mini-program privacy declaration inconsistency static analysis" → MiniDetector、MiniScope。
4. "\"On the (In)Security of LLM App Stores\" Hou" → Hou et al.
5. "ChatGPT apps SDK readOnlyHint annotation measurement study apps declared"（extended）→ 実務記事と GitHub issue のみ。**研究は見つからなかった**。
6. "Alexa skill permission static analysis back-end code SkillDetective SkillExplorer undeclared data collection" → SkillScanner、SKILLPOV、Lentzsch。
7. "Chrome extension privacy practices disclosure vs actual data collection measurement Chrome Web Store labels" → ExtPrivA（既知）のみ。新規は見つからなかった。
8. "HarmonyOS app privacy label inconsistency ArkTS static analysis" → Wagner の修士論文、ArkAnalyzer。**コードとの照合研究は見つからなかった**。
9. "VS Code extensions security empirical study capabilities untrusted workspace declaration vs behavior" → Edirimannage、UntrustIDE。
10. "WeChat mini program requiredPrivateInfos privacy guide declaration actual API usage measurement study"（extended）→ **照合研究は見つからなかった**（周辺の研究のみ）。
11. "Felt Greenwood Wagner \"The Effectiveness of Application Permissions\" Chrome extensions overprivileged" → Felt 2011。
12. "Iqbal Kaafar ChatGPT plugins systematic evaluation framework AIES 2024 manifest description" → Iqbal, Kohno, Roesner（著者名の "Kaafar" はこちらの誤記で、正しくは Kohno と Roesner）、Yan et al.
13. "GPT Actions OpenAPI schemas large-scale analysis \"isConsequential\" OR \"consequential\" custom GPTs measurement arXiv"（extended）→ 2506.04036、2505.08148、2405.10547。**isConsequential を測った研究は見つからなかった**。
14. "overprivileged Chrome extensions static analysis unused permissions Manifest V3 empirical study 2025" → **MV3 の静的過剰権限研究は見つからなかった**（SBSEG 2025 は △）。
15. "Ferreira \"Containing Malicious Package Updates in npm with a Lightweight Permission System\" permissions manifest analysis" → Ferreira ICSE 2021。
16. "\"Dangerous Skills Got Certified\" CCS 2020 …" → Cheng et al.（△）。
17. "Guha Fredrikson Livshits Swamy \"Verified Security for Browser Extensions\" IBEX Fine policy Datalog" → IBEX。

arXiv API（search_query、新しい順）:
- `abs:skills AND abs:declared AND (abs:code OR abs:behavior)` → SkillConsist、SkillSpec、Packaged But Not Portable、Scanning the Harness など。
- `abs:"agent skills" AND (abs:manifest OR abs:permission OR abs:metadata)` → BIV、SkillGuard、SkillScope (2605.05868)、ClosureBound、Skill Constellations、After the Party など。
- `abs:"tool annotations" OR abs:readOnlyHint OR abs:destructiveHint` → WebMCP 2606.06387 のみ（照合研究は**見つからなかった**）。
- `abs:"mini-program" AND abs:privacy` → 2402.07367 のみ。
- `abs:"privacy label" AND (abs:HarmonyOS OR abs:"data safety" OR abs:inconsistenc*)` → 既知の系譜のみ。
- `abs:"GPT Store" OR (abs:GPTs AND abs:actions AND abs:privacy)` → 2502.01436 など。
- `abs:"mini-program" OR abs:"miniapp" OR abs:"mini-app"` → TeleGapper、TENET、2608.25877。
- `abs:"browser extension" AND (abs:permission OR abs:overprivilege OR abs:"over-privileged")` → 新規の関連なし。
- `abs:npm AND abs:permission AND (abs:manifest OR abs:capabilit*)` → **0 件**。
- `abs:"privacy label" OR abs:"privacy labels"` → SoK 2608.12511 など。
- `abs:extension AND abs:Chrome AND (abs:"privacy practices" OR abs:disclos* OR abs:"Manifest V3")` → 2404.08310、2406.12710。
- `abs:skill AND (abs:Alexa OR abs:"voice assistant") AND (abs:permission OR abs:"privacy policy")` → SkillVet、2007.14570。
- `ti:"Dangerous Skills Got Certified"` → **0 件**（arXiv に無い）。
- `abs:"VS Code" AND abs:extension*` → **0 件**（表記ゆれ）。`abs:VSCode AND abs:extension` → 2412.00707 など（宣言照合は**見つからなかった**）。
- `abs:"Copilot" AND abs:extension* AND abs:security` → **0 件**。
- `abs:"Open VSX" OR (abs:IDE AND abs:extensions AND abs:malicious)` → 関連なし。
- `abs:"SKILL.md"`、`abs:"allowed-tools" OR abs:"allowed_tools"`、`abs:ClawHub OR abs:OpenClaw`、`abs:"description-implementation" OR abs:"declared behavior" OR abs:"undeclared capabilit*"`（2026-07 以降）→ Scan the Skill、TrustProbe、HarnessSecurity-Bench、Pretext など。最後のクエリは関連 **0 件**。

取得した全文（すべて scratchpad の dl03/ に保存し、リポジトリには置いていない）: arXiv HTML の 2605.11770、2605.12875（名前の確認だけ）、2608.08468、2609.07360、2609.12001、2407.08422、2401.03218、2411.07479、2103.02637、2506.04036。PDF の SkillScanner（NSF PAR 10527328）、SKILLPOV（NSF PAR 10576267、冒頭だけ）、UntrustIDE（NDSS）、Felt 2011、VEX、Ferreira 2021。
