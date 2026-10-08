# 注釈（ToolAnnotations）が安全の判断に使われている実例の調査

調査日 2026-10-08。

**学生の問い**: 「Annotation はセキュリティ上の判断として利用されるべきではないと公式から明言されていますが、
セキュリティ上の判断として利用されている実例はないかを調査して」

**この文書は調査の記録で、決定ではない。** AuthGap の定義（`docs/contradiction_principles.md`）・判定・
凍結（`analyzer-freeze-3`）には触れない。解析器も変えていない。

**出発点**: 使われ方の資料集はすでにある（[付録 G](textbook/appendix-g.md)、2026-10-02、820 件）。付録 G は
「どの製品が注釈で何をするか」を集めたが、「**実害は確かめていません**」と書いている（3.9 節）。
この文書は、付録 G に無い次の 3 つを新たに調べ、付録 G の結論と合わせて問いに答える。

1. 実際に起きたこと — 脆弱性の記録（CVE・GHSA）、報奨金の報告、攻撃の実証、ベンダーの回答（§3）
2. GitHub の issue / PR での議論と、それで変わったふるまい（§3.5）
3. 注釈で制御を緩める製品が、仕様の言う「信頼できるサーバ」に絞っているか（§4）

**確かさの印**（CLAUDE.md 規則 1。`docs/annotations_official_survey.md` と同じ印に 1 つ足した）:

| 印 | 意味 |
|---|---|
| **[確認]** | `scripts/verify_quote.py` で原文を取り寄せ、引用が exact / loose で一致したもの。または git で SHA を固定して読んだコード（repo@SHA path:行） |
| **[確認（調査時のみ）]** | 付録 G の印のまま（配布物を展開して照合したもの）。この文書では取り直していない |
| **[WebFetch]** | github.com のページ（issue・PR の本文やコメント）を WebFetch で読んだもの。github.com は curl に 403 を返すので `verify_quote.py` が使えない。WebFetch は小さなモデルの要約を通すので、**文字列は照合していない** |
| **[未確認]** | 検索結果の抜粋だけ、またはページを開けなかったもの。事実として使わない |
| **[判断]** | 資料に書いてあることではなく、本記録者の考え |

**調べ方**: 本記録者が脆弱性 DB を照合し（§3.1）、AI の調査担当 3 つ（研究・ブログ、GitHub の議論、信頼の条件）に
分けて集めた。担当の報告のうち、この文書の結論を支える引用は本記録者が `verify_quote.py` または git で取り直した
（§7）。数は、この調査で選んだ便宜的な集まりの中の数で、**製品全体の割合ではない**（付録 G の限界 1 と同じ）。

---

## 0. 結論

1. **実例は多数ある。** 注釈で安全の制御を緩める製品は、次の 5 つの形で実在する（§2。どれも付録 G のカードで [確認]）。
   - 確認の省略（`readOnlyHint: true` なら利用者に聞かずに実行）: VS Code、Codex、Microsoft 365 Copilot、Gemini Enterprise、Claude Cowork の auto モード など
   - 制限モード・読み取り専用モードの門: Gemini CLI の Plan Mode、Copilot code review、Claude Code の plan mode など
   - アクセス制御の規則の条件: Google Cloud のマネージド MCP サーバの IAM、Gemini Enterprise の Agent Gateway、ToolHive など
   - 人のいない実行の門: Claude Desktop の watcher、TrueForge の Code Mode
   - 危険度の点数: OWASP MCP Top 10 の推奨管理策
2. **ただし「公式に反している」と一言では言えない。** 仕様が禁じるのは「**信頼できないサーバ**の注釈」で使うことだけで、
   「信頼できるサーバ」の定義は仕様に無い（§1.2）。この調査で調べた 27 製品のうち、
   - **16** は、受け入れたどのサーバの注釈でも同じように制御を緩める。注釈のための別の信頼の確認は無い（多くは「設定した＝信頼した」）
   - **9** は、管理者が選んだサーバ・自社のサーバ・登録簿の値に絞る
   - **2** は不明
   （§4。分母は 27、便宜的な選び方）。公式ブログの観察「多くのクライアントはインストールそのものを信頼の印にしている」と合う。
3. **実害の公開記録は見つからなかった。** うその注釈のせいで、確認なしの書き込み・削除が実際に起きたという公開の記録は 0 件。
   注釈を名指しした CVE も 0 件。悪性パッケージが注釈でうそをついた記録も 0 件（§3.1・§3.8）。見つかった最も強い記録は次の 4 つ。
   - **Dynatrace の MCP サーバの GHSA-pqh8-p93p-2rx7**（GitHub がレビュー済み）: 影響の節が「`readOnlyHint: true` の tool は一部のクライアントが自動承認する。注入でそこが任意の DQL の入口になる」と書く。注釈による自動承認を**脅威の前提**に置いた advisory（§3.2）
   - **DBHub の CVE-2026-61788**: `readOnlyHint: true` を宣言した `execute_sql` が、実際には書き込めた（0.22.5 のソースを git で確認）。ただし advisory は注釈に触れていない（§3.3）
   - **Gemini CLI の Plan Mode** を Google の報奨金（VRP）に報告し「Won't Fix / Infeasible」で閉じられた、と報告者が GitHub の issue に書いている（[WebFetch]。§3.4）
   - 隣のプロトコル ACP の **CVE-2026-32898**（OpenClaw）: 自己申告の tool の種類（`kind`）で自動承認していたのを、修正で「許可の根拠にしない」に変えた（§3.2）
4. [判断] AuthGap の動機は「**被害が出ている**」ではなく「**宣言だけで確認が省かれる経路が、多くの製品に実在し、その経路で宣言を確かめる層がどこにも無い**」と書くのが正確。DBHub の CVE は、宣言と実際が食い違った tool が実在した例として引けるが、AuthGap の対象（Python）の外である（§5）。

---

## 1. 「安全の判断に使う」とは — この文書の定義

### 1.1 制御を「緩める」向きと「締める」向き

この文書では、注釈の値によって次のどれかが変わることを「安全の判断に使う」と呼ぶ。

| 型 | 何が変わるか | 注釈がうそのとき何が起きうるか |
|---|---|---|
| A 確認の省略 | 利用者への「実行してよいか」の確認を出すか | 書き込む tool が確認なしで走る |
| B 制限モードの門 | Plan Mode や read-only モードで、その tool を使えるか | 書き込む tool が制限モードの中で使える |
| C 規則の条件 | IAM・ゲートウェイ・ポリシーの許可 / 拒否 | 書き込む tool が拒否の規則をすり抜ける |
| D 無人の実行の門 | 人のいない実行（スケジュール・スクリプト）から呼べるか | 破壊的な tool が無人で走る |
| E 危険度の点数 | tool の危険度の格付け（上限を超えたら隠す） | 危険な tool が上限の下に入る |

ここまでは**緩める向き**（宣言が「安全」と言うと制御が弱まる）。うその宣言が効くのはこの向きである。

**締める向き**（宣言が「危険」と言うと制御が強まるだけで、宣言が無くても既定は変わらない）は、仕様の注意と矛盾しない使い方で、
この文書では「安全の判断に使う実例」に数えない。例: Qwen Code は分類器に「注釈は疑いを増やす方向にだけ使え」と指示する
（[C07-12](textbook/appendix-g-7.md#g-c07-ide-agents-12)）。Microsoft Agent Framework の FIDES は「制限の方向にしか効かない」設計
（[C03-37](textbook/appendix-g-3.md#g-c03-microsoft-github-37)）。

ただし `destructiveHint: true` で確認を足す使い方は、`=== true` で比べると「書いていない」が「壊さない」側に入り、
緩める向きと同じことが起きる（付録 G 3.3 節）。この場合は D2（`destructiveHint` の欠落・false）が効く。

### 1.2 公式は何を言っているか

公式の文言は 3 つあり、強さが違う。どれも付録 G の [確認] のカード。

| 文書 | 原文 | 強さ |
|---|---|---|
| 仕様 tools ページ（2025-03-26 から全版） | "For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers." | MUST。ただし「信頼できるサーバから来たものでなければ」の条件つき（[C01-01](textbook/appendix-g-1.md#g-c01-mcp-official-01)） |
| schema の注記 | "Clients should never make tool use decisions based on ToolAnnotations received from untrusted servers." | 小文字の should never。これも「信頼できないサーバから」の条件つき（[C01-11](textbook/appendix-g-1.md#g-c01-mcp-official-11)） |
| 旧 Concepts ページ（2026-03-25 に削除） | "These annotations are hints that describe the nature and impact of a tool, but should not be relied upon for security decisions." | 条件なしの「安全の判断に頼るべきでない」。**今は公開されていない**（[C01-15](textbook/appendix-g-1.md#g-c01-mcp-official-15)） |

学生の問いの「セキュリティ上の判断として利用されるべきではない」に最も近い文は、**削除された旧 Concepts ページ**のもの。
今の仕様は「信頼できないサーバのものは信じるな」と条件つきで言い、「信頼できるサーバ」を定義していない。
公式ブログ（2026-03-16）は、信頼できるサーバの `readOnlyHint: true` を自動承認に使うことを
"This is the most common use of annotations today." と書き（[C01-21](textbook/appendix-g-1.md#g-c01-mcp-official-21)）、
"In practice most clients still treat installation itself as the trust signal" とも書く（[C01-24](textbook/appendix-g-1.md#g-c01-mcp-official-24)）。

[判断] したがって「公式に反する使い方か」は、製品が**どのサーバを信頼できるとみなしているか**で決まる。§4 はそれを調べた。

---

## 2. 実例 — 付録 G のカードから、型ごとに

付録 G の表（3.2 節・3.9 節）を、§1.1 の型で並べ直した。代表だけを載せる。条件（モード・設定・版）はカードの「条件」の欄が正で、
ここでは短く書く。印はすべてカードのまま。

### 型 A 確認の省略

| 製品 | 条件 | カード |
|---|---|---|
| VS Code（Copilot のエージェントモード） | `readOnlyHint` が真なら実行前の確認を作らない。既定で有効 | [C03-06](textbook/appendix-g-3.md#g-c03-microsoft-github-06) [確認] |
| Microsoft 365 Copilot（宣言型エージェントの MCP プラグイン） | 初回の接続の確認の後は確認なし | [C03-30](textbook/appendix-g-3.md#g-c03-microsoft-github-30) [確認] |
| OpenAI Codex | auto モード（既定）で `readOnlyHint: true`、または `destructiveHint: false` かつ `openWorldHint: false` なら承認なし | [C05-34](textbook/appendix-g-5.md#g-c05-openai-34) [確認] |
| GitHub Copilot CLI 1.0.63 | deny の規則に当たらなければ `readOnlyHint: true` を承認（文書は逆のことを書く） | [G2CCM-09](textbook/appendix-g-7.md#g-g2-closed-clients-missing-09) [確認]、[C03-19](textbook/appendix-g-3.md#g-c03-microsoft-github-19) |
| Gemini Enterprise（カスタム MCP の actions） | `readOnlyHint` を付けたツールは確認を飛ばす | [C06-20](textbook/appendix-g-6.md#g-c06-google-aws-20) [確認] |
| Claude Desktop・Cowork | auto モードで `readOnlyHint === true` を承認なしで通す | [G3CAMA-18](textbook/appendix-g-8.md#g-g3-consumer-apps-model-apis-18) [確認]、[C04-08](textbook/appendix-g-4.md#g-c04-anthropic-08) |
| goose・Docker Agent・n8n・AgentScope・LeapFlow・TrueForge | それぞれのモード・既定の設定で `readOnlyHint: true` を確認なし | [C07-02](textbook/appendix-g-7.md#g-c07-ide-agents-02) [C07-07](textbook/appendix-g-7.md#g-c07-ide-agents-07) [C08-03](textbook/appendix-g-8.md#g-c08-frameworks-03) [G3AA-23](textbook/appendix-g-7.md#g-g3-asia-agents-23) [G2RM-17](textbook/appendix-g-10.md#g-g2-registries-marketplaces-17) [G2GP-08](textbook/appendix-g-10.md#g-g2-gateways-platforms-08) |
| Cursor 3.23.12 | 管理者が reads モードにしたとき | [G2CCM-35](textbook/appendix-g-7.md#g-g2-closed-clients-missing-35) [確認（調査時のみ）] |
| OpenAI Responses API | 開発者が `require_approval` に read_only の条件を書いたとき | [C05-24](textbook/appendix-g-5.md#g-c05-openai-24) [確認] |

### 型 B 制限モード・読み取り専用モードの門

| 製品 | 条件 | カード |
|---|---|---|
| Gemini CLI の Plan Mode | `readOnlyHint = true` の MCP ツールだけを「確認つきで実行可」に上げ、それ以外は拒否 | [C06-04](textbook/appendix-g-6.md#g-c06-google-aws-04) [確認] |
| GitHub Copilot code review | `readOnlyHint: true` のツールだけを使う | [C03-16](textbook/appendix-g-3.md#g-c03-microsoft-github-16) [確認] |
| Claude Code（plan mode） | `readOnlyHint` が true でない MCP ツールを「plan mode では呼べない」の確認に回す | [G2CCM-03](textbook/appendix-g-7.md#g-g2-closed-clients-missing-03) [確認（調査時のみ）] |
| Devin CLI の Plan モード | v3000.3.22 の changelog で `readOnlyHint: true` だけ許可。今も続くかは不明 | [C07-21](textbook/appendix-g-7.md#g-c07-ide-agents-21) [確認] |
| MCP Proxy for AWS の `--read-only` | 上流の `readOnlyHint` が True のツールだけを見せる（v1.6.4 で呼び出し時の拒否も足した） | [C06-48](textbook/appendix-g-6.md#g-c06-google-aws-48) [確認] |
| Pydantic AI Harness の `read_only` | `readOnlyHint: true` のツールだけを残す | [C08-32](textbook/appendix-g-8.md#g-c08-frameworks-32) [確認] |

### 型 C 規則の条件（IAM・ゲートウェイ）

| 製品 | 条件 | カード |
|---|---|---|
| Google Cloud のマネージド MCP サーバ | 管理者の deny ポリシーで「読み取り専用と注記されていない」ツールの呼び出しを拒否 | [C06-14](textbook/appendix-g-6.md#g-c06-google-aws-14) [確認] |
| Gemini Enterprise Agent Platform の Agent Gateway | 4 つのヒントを IAM の条件式に使う。値は登録簿の toolspec.json から引く | [C06-21](textbook/appendix-g-6.md#g-c06-google-aws-21) [C06-24](textbook/appendix-g-6.md#g-c06-google-aws-24) [確認] |
| ToolHive の Safe tools | `readOnlyHint == true`、または `destructiveHint == false` かつ `openWorldHint == false` だけ許可 | [C09-23](textbook/appendix-g-10.md#g-c09-servers-gateways-security-23) [確認] |
| TrueFoundry AI Gateway | 承認の範囲を destructive にすると `destructiveHint: true` だけ承認待ち | [G2GP-03](textbook/appendix-g-10.md#g-g2-gateways-platforms-03) [確認] |
| kubernetes-mcp-server（自分のツール） | `disable_destructive` で `destructiveHint` のツールを外す（欠落は残る） | [G3VS-02](textbook/appendix-g-9.md#g-g3-vendor-servers-02) [確認] |

### 型 D 無人の実行の門

| 製品 | 条件 | カード |
|---|---|---|
| Claude Desktop（Cowork）の watcher | 人のいない実行からは `destructiveHint: true` を拒否。書いていないツールは通る | [G3CAMA-22](textbook/appendix-g-8.md#g-g3-consumer-apps-model-apis-22) [確認] |
| Claude Desktop のアーティファクトからの呼び出し | `destructiveHint: true` だけ確認を挟む | [G3CAMA-24](textbook/appendix-g-8.md#g-g3-consumer-apps-model-apis-24) [確認] |
| TrueForge の Code Mode | 破壊的なツールを拒否。注釈が無ければ通す | [G2GP-13](textbook/appendix-g-10.md#g-g2-gateways-platforms-13) [確認] |

### 型 E 危険度の点数

| 製品 | 条件 | カード |
|---|---|---|
| OWASP MCP Top 10 の推奨管理策（Client-Side Tool Risk Gating） | 外部のツールの危険度を注釈から付け、上限を超えたら隠す | [C10-14](textbook/appendix-g-12.md#g-c10-research-standards-14) [確認] |

**この節のまとめ**: 学生の問いへの答えは「ある」。型 A が最も多い。ただし多くはモード・設定・版の条件つきで（付録 G 3.2 節）、
宣言を読まない製品も多い（Zed、JetBrains Junie、Qoder など）。

---

## 3. 実際に起きたこと — 脆弱性・報告・実証・議論

### 3.1 脆弱性 DB の照合（本記録者、2026-10-08）

記録は `evidence/annotations_security/db_search.json`。

| DB | 探し方 | 結果 |
|---|---|---|
| NVD（CVE） | API の `keywordSearch` で `readOnlyHint`・`destructiveHint`・`openWorldHint`・`idempotentHint`・"read-only hint"・"MCP annotations"・"tool annotation MCP" | **すべて 0 件** |
| NVD | "tool annotations"・"MCP annotation"・"MCP auto-approve" | 8 件、すべて無関係（Argo CD・CVAT・Java の注釈・OAuth など） |
| NVD | "MCP read-only tool" | 7 件。うち 3 件が「宣言の上では読み取り専用の MCP ツールが書き込めた」CVE（§3.3） |
| OSV（npm・PyPI・Go・crates.io・Maven・NuGet の全件、277,797 ファイル、2026-10-08T08:05Z 取得） | ヒント名・`ToolAnnotations`・"tool annotation" の grep | **3 件**。関係するのは Dynatrace の 2 件（§3.2）。mobile-mcp の 1 件は引用したコードに `destructiveHint: true` が出るだけ |
| OSV の悪性パッケージ（MAL-） | 同じ grep | **0 件** |
| GitHub Advisory Database（検索の画面。担当が確認） | reviewed で `readOnlyHint` | 2 件（Dynatrace）。unreviewed で `readOnlyHint` は 0 件 [WebFetch] |

**読み方の注意**: NVD の `keywordSearch` は CVE の説明文だけを探す。Microsoft などの CVE は説明文が短く仕組みの語が出ないので、
0 件は「DB の説明文に語が無い」という意味にとどまり、「そういう脆弱性が無い」ことの証拠ではない。

### 3.2 注釈（または同じ役割の自己申告）を名指しした advisory・CVE

**(1) GHSA-pqh8-p93p-2rx7 — Dynatrace の MCP サーバ、`readOnlyHint: true` の tool への DQL の注入**

- 対象: npm `@dynatrace-oss/dynatrace-mcp-server` 2.1.1 より前。2.1.1 で修正（修正コミット `15d3546c`、2026-07-14）。
  GitHub のレビュー 2026-07-31、Moderate、CWE-943。CVE は無い。
- 何が起きるか: 読み取りの tool（`list_problems` など）の引数がそのまま DQL に入るので、注入で任意の DQL を走らせられる。
  advisory は影響を次のように書く。
  > "The affected tools are annotated `readOnlyHint: true`, which some MCP clients treat as a signal to auto-approve. The injection turns a "safe" read tool into an arbitrary-DQL surface."
  > "the marginal impact is the auto-approval pathway and the broken tool contract, not privilege escalation."

  **[確認: https://api.osv.dev/v1/vulns/GHSA-pqh8-p93p-2rx7、exact、2026-10-08]**
- 本記録者が確かめたこと: 修正の直前（`35db4695`）の `src/index.ts` で、`list_vulnerabilities`・`list_problems`・`find_entity_by_name`・
  `get_kubernetes_events`・`list_exceptions` は `readOnlyHint: true`、任意の DQL を走らせる `execute_dql` は `readOnlyHint: false`
  （402・479・551・705・1052・1317 行の登録の直後）**[確認: git]**。
- [判断] 作者は「任意の DQL は確認させ、範囲を絞った読み取りは確認なしにさせる」という線を、`readOnlyHint` で引いていた。
  注入はその線を越える。ここで注釈は**うそではない**（DQL は読むだけ）。破れたのは「確認なしで通る範囲」の約束である。
  AuthGap の D1 の判定では、この tool は矛盾にならない（§5）。
- どのクライアントで試したかは advisory に無い（"some MCP clients" とだけ書く）。

**(2) GHSA-pc2w-4mq8-32qw — 同じサーバ、`create_dynatrace_notebook` に人の承認の門が無かった**

- 1.8.7 で修正。GitHub のレビュー 2026-07-29、Low、CWE-862。問題の中心はサーバ自身の承認（elicitation）の欠落で、
  クライアントの注釈の扱いではない。advisory のコードの注記に次の 1 行がある。
  > "// No destructiveHint annotation."

  **[確認: https://api.osv.dev/v1/vulns/GHSA-pc2w-4mq8-32qw、exact]**
- 修正コミット `2851d3ce`（2026-06-08、"feat: add human approval gate to `create_dynatrace_notebook` tool (#529)"）は、
  承認の門と一緒に `destructiveHint: true` と `idempotentHint: false` を足した **[確認: git、`src/index.ts` の差分]**。
  ベンダーが注釈の欠落も直すべき点に含めた例。

**(3) CVE-2026-32898 / GHSA-7jx5-9fjg-hp4m — OpenClaw の ACP クライアント（MCP ではなく隣のプロトコル）**

- npm `openclaw` 2026.2.22-2 まで。2026.2.23 で修正。ACP（エディタとエージェントの間の取り決め）の、エージェントが自己申告する
  tool の種類（`toolCall.kind`）を見て自動承認していた。
  > "The OpenClaw ACP client could auto-approve tool calls based on untrusted metadata and permissive name heuristics."
  > "Require trusted core tool IDs for auto-approval and ignore untrusted `toolCall.kind` as an authorization source."

  **[確認: https://api.osv.dev/v1/vulns/GHSA-7jx5-9fjg-hp4m、exact]**。NVD の説明文 "auto-approves tool calls based on untrusted toolCall.kind metadata and permissive name heuristics" **[確認: NVD API、exact]**。
- [判断] MCP の注釈ではないが、「自己申告の分類で自動承認 → CVE → 修正で許可の根拠から外す」という、学生の問いと同じ形の一連が、
  CVE として記録された唯一の例。
- 関連（担当の推論。本記録者は試していない）: Docker Agent は `readOnlyHint` を ACP の `ToolKindRead` に写す
  （[C07-10](textbook/appendix-g-7.md#g-c07-ide-agents-10)）。したがって MCP の注釈が ACP の `kind: "read"` になる経路はある。
  その経路が OpenClaw の自動承認に届いた記録は見つかっていない。

### 3.3 「宣言の上では読み取り専用」の MCP ツールが書き込めた CVE

NVD の "MCP read-only tool" の検索で見つけた。**注釈を付けていたかは、本記録者が脆弱な版のソースを git で読んで確かめた。**

| CVE | 製品 | 読み取り専用の宣言のしかた | 注釈 | 根拠 |
|---|---|---|---|---|
| **CVE-2026-61788**（GHSA-mwwr-p57h-56pf） | DBHub（bytebase/dbhub、TypeScript）0.22.5 以前、0.22.6 で修正 | 設定 `readonly = true` の `execute_sql` | **`readOnlyHint: true`**（設定の値から計算） | bytebase/dbhub@`d65c6b42`（version 0.22.5）`src/utils/tool-metadata.ts` 147・150-151 行 `const isReadonly = executeOptions.readonly === true;` / `readOnlyHint: isReadonly,` / `destructiveHint: !isReadonly,` **[確認: git]** |
| CVE-2026-48774（GHSA-7wh6-2vcc-gcm4） | ProxySQL の GenAI/MCP `run_sql_readonly`、3.0.9 で修正 | tool の名前と文書 | **なし** | sysown/proxysql 修正 `e32b7fd5` の親 `f4fd5e4c` で `lib`・`include`・`plugins` に `readOnlyHint` 0 件 **[確認: git]** |
| CVE-2026-18954（GHSA-j694-4m5j-w8hc） | AWS Labs DocumentDB MCP Server の `aggregate`、1.0.12 で修正 | サーバの read-only モード | **なし** | awslabs/mcp 修正 `9480a33c` の親 `e596a8b9` で `src/documentdb-mcp-server/awslabs` に `readOnlyHint`・`ToolAnnotations` 0 件。`server.py` 72 行 `mcp.tool(name='aggregate')(aggregate)` **[確認: git]** |

DBHub の CVE の説明: "setting `readonly = true` on the `execute_sql` tool does not make the connection read-only. ... The only thing left enforcing read-only is a classifier that inspects the first keyword of each statement. Any `SELECT` that writes or has side effects through a function call passes it."
（NVD の記録を `evidence/annotations_security/nvd_CVE-2026-61788.json` に保存）。

- [判断] DBHub は、**`readOnlyHint: true` を名乗った tool が実際には書き込めた**、CVE の付いた実例である。宣言（D1）と実効が食い違った。
  この tool を `readOnlyHint` で確認を省くクライアント（§2 の型 A）につなげば、書き込みが確認なしで通りえた。ただしそれが起きた記録は無く、
  advisory も注釈に触れていない（GHSA の本文を grep して 0 件）。本記録者は試していない。
- [判断] 3 件とも「読み取り専用を、キーワードの分類やモードの検査という**自前の検査**で守ろうとして、すり抜けられた」形である。
  宣言を注釈で出していたのは DBHub だけだった。
- 参考: mcp-memory-service の CVE-2026-49291（OAuth の read の範囲で書き込み・削除の tool を呼べた）は、サーバが注釈を持っているが、
  修正の権限の検査は注釈ではなく名前の一覧（`_WRITE_TOOLS = frozenset({"store_memory", "delete_memory"})`）で書いた
  （doobidoo/mcp-memory-service v10.65.3、`src/mcp_memory_service/web/api/mcp.py` 27 行 **[確認: git]**）。

### 3.4 報奨金の報告・研究者の報告・挙動の試験

| 何 | 対象 | 状態 | 印 |
|---|---|---|---|
| Google VRP b/524448710 | Gemini CLI 0.45.1 の Plan Mode が、サーバの申告する `readOnlyHint` を信じて MCP ツールを通す | 報告者が GitHub の issue #28548 に "Reported to Google VRP as b/524448710 (closed Won't Fix / Infeasible, P2 / S4)." と書く。"The confirmation prompt still fires, so this is not silent execution." とも書く。VRP の記録そのものは公開されていないので、「Won't Fix」は報告者の記載 | [WebFetch] |
| MCPSafe の「D006」 | github/github-mcp-server が、動的 toolset のモードで組み合わせると書き込みにつながる tool に `readOnlyHint: true` を付けている、という主張 | "Reported to GitHub's security team under coordinated 30-day disclosure." と書くが、GitHub の回答は公開されていない。所見は LLM の判定による走査から | 記事の引用 [確認: dev.to、exact] |
| Akav Labs | 破壊的な操作をする tool に `destructiveHint: false` が付いていた例が複数ある、という主張 | 対象のベンダー名も CVE も書かない。"When the disclosure windows close — beginning in July 2026 — we will publish the full technical details" と書くが、2026-10-08 の時点で続きの記事は見つからない | [確認: dev.to、exact / loose] |
| Outflank "MCP Beyond the Spec"（2026-09-30） | Codex と Claude Code の承認の挙動を試した記事 | ページが 403 で読めない。検索の抜粋に "None of the modes we tested skips approval just because a tool has readOnlyHint=true." と "Claude Code uses readOnlyHint in two places: the plan-mode permission check and the decision to run tool calls in parallel." がある。抜粋だけでは、1 つめの文がどの製品のどのモードの話かを確定できない。付録 G のカード（Codex は [C05-34](textbook/appendix-g-5.md#g-c05-openai-34)、Claude Code は [G2CCM-03](textbook/appendix-g-7.md#g-g2-closed-clients-missing-03)）と合うかは確かめられない | [未確認] |

MCPSafe の主張の裏: github-mcp-server v0.5.0 の `enable_toolset` には `ReadOnlyHint: true` があり、理由のコメントは
"// Not modifying GitHub data so no need to show a warning"
**[確認: raw.githubusercontent.com/github/github-mcp-server/v0.5.0/pkg/github/dynamic_tools.go、exact]**。
[判断] `enable_toolset` は公開する tool の集合を変えるが、GitHub のデータは書かない。「権限の昇格」という主張の裏づけは弱い。
ただし「警告を出さないために値を選ぶ」作者の考えが、コードのコメントにそのまま書かれている例である（§3.6）。

### 3.5 GitHub の issue・PR での議論

**未記入（2026-10-08）。** GitHub の issue・PR を読む担当の報告がまだ届いていない。届きしだい、この節を埋める別のコミットを足す。
それまでは、Gemini CLI の #28548 と VRP の件（§3.4、[WebFetch]）だけが GitHub 上の記録として入っている。

### 3.6 作者が「確認を出させないため」に値を選んだ例

型 A の製品があることで、サーバの作者の側が値の選び方を変えている。どれも書き込みを隠す悪意の例ではなく、
「確認の出すぎ」を避ける動機の例である。

| サーバ | 書いてあること | 印 |
|---|---|---|
| PostHog の MCP | 書き込みもできるメタツール `exec` に `destructiveHint: false`。理由は「Claude Code が destructive の tool を毎回確認する」から | [G3VS-29](textbook/appendix-g-9.md#g-g3-vendor-servers-29) [確認] |
| MobileBuildMCP（旧 XcodeBuildMCP） | CHANGELOG: "Fixed unnecessary tool confirmation prompts in MCP clients (such as Codex) that treat missing approval annotations as high-risk defaults" | [G3VS-15](textbook/appendix-g-9.md#g-g3-vendor-servers-15) [確認] |
| github-mcp-server | `enable_toolset` に `ReadOnlyHint: true`、コメント "Not modifying GitHub data so no need to show a warning" | §3.4 [確認] |
| GitLab 19.3（MR !231431、2026-08-06 マージ） | 自社の MCP ツールの事前承認の一覧を、各ツールの `readOnlyHint` から作るように変えた: "This derives the list from each tool's own `readOnlyHint` annotation instead" | [確認: gitlab.com の API、exact] |

[判断] GitLab は自社のサーバの注釈を自社のクライアント側の判断に使うので、仕様の「信頼できるサーバ」の範囲に入る使い方と読める。

### 3.7 指針・解説の書き方

| 出典 | 書いてあること | 印 |
|---|---|---|
| Embrace The Red（Johann Rehberger、2025-11-25） | 妥協案として注釈での門を勧めつつ、限界も書く: "A possible trade off could be to have readOnly tools auto-approve, but require HITL for all tools with an annotation of destructiveHint or openWorldHint." / "But even readOnly tools can have side-effects, like data leakage by the way, so automatic tool invocation is often exploitable." | [確認: exact] |
| Wiz Research Briefing（2025-04-17） | "It's easy to imagine an enforcement mechanism for these currently untrusted hints." | [確認: exact] |
| OWASP MCP Security Cheat Sheet | "tool annotations are hints, not enforcement"（付録 G の調査では語が見つからなかったページ。今回は一致した） | [確認: exact] |
| Harmonic Security の Cowork の手引き | "Do not rely on read-only auto-permissions; most custom connectors do not set the annotations that drive them." | [確認: exact] |

### 3.8 探して見つからなかったもの

「見つからなかった」は「無い」ではない。探した範囲を書く（担当の報告から。本記録者は個々のページを取り直していない）。

- **CVE・GHSA**: §3.1 のとおり。注釈の CVE は 0。
- **悪性パッケージ**: OSV の MCP に関係する MAL- の記録（担当の数え方で 110 件）に、注釈・read-only・`destructiveHint` の語は 0。
  Postmark-MCP、mcp-runcommand-server などの悪性パッケージの解説記事にも注釈の話は無い。
- **事故の一覧**: vulnerablemcp.info、AuthZed の MCP の事故年表、Docker の "MCP Horror Stories"、UpGuard ほか 10 以上の一覧に、注釈の語は 0。
  AI Incident Database は JavaScript で描くページで確かめられなかった（不明）。
- **セキュリティ企業の研究記事**: HiddenLayer、Snyk、Unit 42、CyberArk、Invariant、Trail of Bits、Check Point、Tenable、Pluto Security ほかに、
  注釈を使った攻撃の記事は無かった。
- **論文**: arXiv の 12 本ほどを grep したが、注釈のうそを実際の製品で試した論文は無かった。付録 G の arXiv:2606.06387
  （WebMCP で `readOnlyHint=true` を足すと悪性のツールが選ばれやすくなる、という実験）は、確認の省略ではなくモデルのツール選びの話。
- **学会**: Black Hat USA 2026・DEF CON 34・USENIX Security・CCS・IEEE S&P・NDSS 2026 で、注釈の講演・論文は見つからなかった。
- **報奨金**: HackerOne・huntr・MSRC・OpenAI・Anthropic で、注釈の公開の報告は見つからなかった（huntr の報告は既定で非公開）。
- **読めなかったもの（不明）**: NSA の "MCP Security Design Considerations"（403）、Akamai の記事（403）、Outflank の記事（403）。

---

## 4. 「信頼できるサーバ」に絞っているか — 27 製品

§1.2 のとおり、仕様の禁止は「信頼できないサーバ」の注釈に限られる。そこで、注釈で制御を緩める製品が、
**その緩め方をどのサーバに当てはめるか**を調べた（担当が 2026-10-08 にソース・文書を確かめ、本記録者が VS Code・Codex・Gemini CLI の
コードを取り直した）。照合の記録は `evidence/annotations_security/trust_gating_vqlog.txt`。

**分け方の定義**:
- 「絞らない」= 製品が受け入れた（設定・インストールした）サーバなら、どれの注釈でも同じように緩める。注釈のための別の信頼の確認が無い。
- 「絞る」= 管理者が選んだサーバ、自社のサーバ、登録簿の値など、注釈を当てはめる範囲を別の手段で狭める。
- サーバを受け入れるときの確認（ワークスペースの信頼など）は、注釈の扱いを変えないので「絞る」に数えない。

### 4.1 表

| # | 製品（確かめた版） | 緩める制御 | 信頼の条件 | 既定 | 分け方 |
|---|---|---|---|---|---|
| 1 | VS Code（vscode@`3a7c8e0`） | 実行前の確認 | 利用者・拡張・プラグインの設定のサーバは確認なしに `Trusted`。ワークスペースの設定はワークスペースの信頼に従う。他のアプリの設定から見つけたサーバだけ「信頼して起動するか」を聞く | 有効 | 絞らない |
| 2 | Microsoft 365 Copilot | 初回の後の確認 | プラグインごとに 1 回の利用者の同意。その後は全 `readOnlyHint` ツールが確認なし | 有効 | 絞らない |
| 3 | GitHub Copilot CLI 1.0.63 | 承認 | 注釈の段では deny の規則だけを見る。文書の信頼のレベルの表はここで使われない。既定の GitHub のサーバの注釈は、クライアントに同梱した一覧から取る | 有効 | 絞らない |
| 4 | OpenAI Codex（openai/codex@`ea27864`） | 承認（auto・writes モード） | どの MCP サーバにも当てはめる。プロジェクトの設定は信頼したプロジェクトだけ。管理者は requirements.toml で許可リストを強制できる | 有効（auto） | 絞らない |
| 5 | OpenAI Responses API | 承認 | 開発者がサーバごとに明示で書く。文書は「信頼が持てたら」と条件にするが、強制はしない | 無効 | 絞る |
| 6 | ChatGPT の developer mode | 書き込みの確認（裏返しの読み） | 利用者が developer mode を有効にすると、任意の MCP サーバのアプリに当てはまる。文書のページは 2026-10-08 に 404（2026-10-04 の Wayback で照合） | 無効 | 絞らない |
| 7 | Gemini Enterprise | 確認 | 管理者が組織ポリシーを上書きし、actions を有効にしたものだけ | 管理者が有効にしたもので有効 | 絞る |
| 8 | Gemini CLI（gemini-cli@`44d764e`） | Plan Mode での可否 | Plan Mode の規則は `mcpName = "*"`（全サーバ）。ブラウザエージェントの自動許可は同梱の chrome-devtools-mcp だけ | Plan Mode で有効 | 絞らない（Plan Mode） |
| 9 | Claude Desktop・Cowork | auto モードの承認 | "Auto mode applies to all of your existing connectors, plugins, ..." | auto は選んだとき | 絞らない |
| 10 | Claude Code 2.1.293 | plan mode の強制の確認からの除外 | どの MCP ツールにも当てはめる | plan mode で有効 | 絞らない |
| 11 | Docker Agent（docker/cagent@`dd39af0`） | 自動承認 | どの toolset にも。エージェントの設定は URL や OCI の登録所からも来る | 有効（モード未選択でも） | 絞らない |
| 12 | goose（goose@`9560429`） | Smart Approve の許可 | 既定でどのサーバもインストールできる。管理者の許可リストは任意 | Smart Approve を選んだとき | 絞らない |
| 13 | n8n Instance AI（n8n@`727f2a7`） | read 類の承認なし | 外部のサーバは運用者の環境変数でだけ。利用者の接続は n8n の登録簿のサーバだけ。注釈の値はサーバから来る | 有効 | 絞る |
| 14 | AgentScope（agentscope@`48c4b9c`） | 全モードで許可 | 開発者が組み込んだどのサーバにも | 有効 | 絞らない |
| 15 | LeapFlow（leapflow@`401f1c2`） | 審査の省略 | どのサーバにも。コードのコメントは宣言を「サーバ自身の約束」として扱う | 有効 | 絞らない |
| 16 | TrueForge（trueforge@`6b42368`） | 承認の一時停止なし | Settings → Connectors に登録したサーバ。誰が登録できるかは不明 | 有効 | 絞らない |
| 17 | TrueFoundry AI Gateway | destructive の承認の範囲 | テナントの管理者だけがポリシーを作る。管理者が注釈を上書きできる | 無効 | 絞る |
| 18 | Cursor 3.23.12 | reads モードで確認なし | 管理者がサーバごとに reads モードを選ぶ | 無効 | 絞る |
| 19 | Devin CLI / Desktop | Plan モードでの許可 | 不明（後の版で「通常の権限の仕組み」に変わったと書く） | 不明 | 絞らない（現状は不明） |
| 20 | Google Cloud のマネージド MCP サーバ（IAM） | deny ポリシーの例外 | "You can't use IAM to control access to non-Google Cloud MCP servers." = 自社のサーバだけ | 無効 | 絞る |
| 21 | Agent Gateway | IAM の条件 | 値はサーバではなく、セキュリティの管理者が登録した toolspec.json から | 無効 | 絞る |
| 22 | ToolHive の Safe tools | Cedar の許可 | 運用者が選ぶ。値は上流のサーバの tools/list から（クライアントが付けた値は拒否） | 無効 | 絞らない |
| 23 | Slack（Slackbot） | 確認かもしれない | 文書が自己矛盾（読み取りは確認なし / 第三者のツールは読みも書きも毎回許可） | 不明 | 不明 |
| 24 | Notion の Custom Agents | 読み取りの自動実行 | カスタムのサーバはワークスペースの管理者が有効にする。読み / 書きの区分が注釈から来るかは不明 | — | 不明 |
| 25 | OWASP の推奨管理策 | 危険度の点数 | ツールの点数は上流の申告から。サーバには別に「カタログの信頼」の軸がある（組み合わせ方は不明） | 運用者の方針 | 絞らない |
| 26 | Pydantic AI Harness の `read_only`（pydantic-ai@`f55bb8a`） | 絞り込み | 既定はベンダーのホストする窓口。開発者が client を渡すとどのサーバにも | 無効（選ぶもの） | 絞る |
| 27 | GitHub Copilot code review | 絞り込み | リポジトリの管理者が設定したサーバ | 常に | 絞る |

### 4.2 まとめ（分母 27）

- **絞らない: 16**（1・2・3・4・6・8・9・10・11・12・14・15・16・19・22・25）
  - 既定で有効: 8（VS Code、M365 Copilot、Copilot CLI、Codex、Docker Agent、AgentScope、LeapFlow、TrueForge）
  - 利用者が選ぶモードで有効: 6（Cowork の auto、goose の Smart Approve、Gemini CLI の Plan Mode、Claude Code の plan mode、ChatGPT の developer mode、Devin の Plan）
  - 運用者が選ぶ方針: 2（ToolHive、OWASP）
- **絞る: 9**（5・7・13・17・18・20・21・26・27）
- **不明: 2**（Slack、Notion）

「信頼」の実際の意味:
- ほとんどは「**設定した・インストールした＝信頼した**」。VS Code は利用者が設定したサーバを確認なしに `Trusted` にする
  （`src/vs/workbench/contrib/mcp/common/discovery/installedMcpServersDiscovery.ts` 136 行 `trustBehavior: McpServerTrust.Kind.Trusted,`
  **[確認: git、vscode@3a7c8e0]**）。
- リポジトリと一緒に来る設定は、ワークスペース・フォルダの信頼で止める製品が多い（VS Code、Copilot CLI、Codex、Claude Code、Gemini CLI）。
  これは「サーバを入れてよいか」の確認で、注釈の扱いは変えない。
- **注釈の値の出どころそのものを変える**のは少数: Agent Gateway（管理者の登録簿）、Google Cloud の IAM（自社のサーバだけ）、
  TrueFoundry（管理者の上書き）、Copilot CLI の既定のサーバ（同梱の一覧）。残りは、どのサーバを入れるかを絞るだけで、値はサーバの自己申告のまま。
- 注釈が「検証されていない」とはっきり書くのは 27 のうち **Notion だけ**（"Notion hasn't verified custom servers for accuracy and completeness."
  **[確認]**）。一部・間接に書くのは OpenAI の文書、ToolHive、Pydantic AI、OWASP、LeapFlow のコードのコメント。

[判断] 「絞らない」16 製品は、公式ブログの「インストールを信頼の印にしている」に当たる。これが仕様の MUST に反するかは
「信頼できるサーバ」の定義しだいで、仕様は定義していないので、**違反と断定はしない**。正確な言い方は
「仕様の条件（信頼できるサーバ）を、ほとんどの製品は『利用者が入れたサーバ』と読み、その中で注釈を確かめる手段を持たない」。

### 4.3 付録 G から変わったこと・直したこと

付録 G のカードは生成物なので直さない（付録 G の約束）。ここに記録だけ残す。

1. **VS Code の信頼の確認は、利用者が設定したサーバには出ない**（上のとおり。`nativeMcpDiscoveryAbstract.ts` 156 行の
   `TrustedOnNonce` は他のアプリの設定から見つけたサーバだけ）**[確認: git]**。
2. **Gemini CLI に `general.plan.trustReadOnlyHint` は無い**: gemini-cli@`44d764e`（2026-10-07）の設定・文書・ポリシーで 0 件 **[確認: git]**。
   同名の PR は GitHub の検索に出るが、取り込まれていない（§3.5）。
3. **ChatGPT の developer mode のページは 2026-10-08 に 404**。カード C05-19〜21 の引用は 2026-10-04 の Wayback で照合し直した（担当）。
4. **Copilot CLI 1.0.63 は、既定の GitHub のサーバの注釈を、そのサーバの tools/list ではなくクライアントに同梱した一覧から取る**（担当、`app.js` 1692 行）。
5. **Claude Code 2.1.293**（カードの 2.1.287 より新しい）でも plan mode の検査は同じ（担当がバイナリを grep。`verify_quote.py` は通していない）。
6. Gemini CLI のフォルダの信頼は、コードでは既定で有効（`settingsSchema.ts` 1920-1921 行）だが、`docs/cli/trusted-folders.md` 10 行は
   "disabled by default" と書く（文書とコードの食い違い。担当 **[確認]**）。

---

## 5. AuthGap にとっての意味（本記録者の判断）

この節は全体が **[判断]**。

1. **動機の書き方**: 「注釈が安全の判断に使われている」は、製品と版を名指しして言える（§2・§4）。
   「その結果、被害が出ている」は言えない（§3.8）。論文では「宣言だけで確認が省かれる経路が多くの製品に実在し、
   宣言を確かめる層がどこにも無い。だから宣言の正しさを外から測る意味がある」と書くのが正確。
2. **DBHub の CVE は D1 の実例として引ける**。`readOnlyHint: true` を名乗った tool が書き込めた。ただし
   - TypeScript のサーバで、AuthGap の対象（Python）の外。
   - 値は設定から計算されている（`readOnlyHint: isReadonly`）。AuthGap の入口の規則がこの形（変数で渡す注釈）をどう扱うかは、
     Python の同じ形の例で確かめていない（不明）。
   - 書き込めた理由は SQL の分類のすり抜けで、コードの効果の静的解析で見える種類の矛盾か（SQL 文の中身に依存する）は、
     `docs/contradiction_principles.md` §7 の SQL の類の規則で判断することになる。この文書では判定しない。
3. **Dynatrace の advisory は、AuthGap が捕まえない種類の問題を示す**。注釈は正しい（読むだけ）が、注入で「確認なしで通る範囲」が広がる。
   D1 の判定は「環境を変えるか」なので、この tool は矛盾にならない。限界節に「宣言が正しくても、自動承認の経路は注入の影響を広げる」と書ける。
4. **「絞らない」16 製品の数は、論文の動機の数字として使わない**。便宜的な 27 製品の中の数で、全製品の割合ではない。使うなら
   「調べた 27 製品のうち 16」と分母と選び方を添える。
5. **作者が確認を避けるために値を選ぶ例**（§3.6）は、宣言が「実効の記述」ではなく「クライアントの UX への合わせ」で決まることがある、
   という観察の裏づけになる。AuthGap の判定は作者の動機を問わない（コードと宣言の関係だけ）ので、判定には使わない。

---

## 6. 確かめられなかったもの（不明）

- **Gemini CLI の VRP の結果**（「Won't Fix / Infeasible」）は報告者の記載だけ。VRP の記録は公開されていない。
- **MCPSafe・Akav Labs の報告の結果**。ベンダーの回答も CVE も公開されていない。Akav Labs が約束した詳細の記事は 2026-10-08 時点で見つからない。
- **Outflank の記事の本文**（403）。検索の抜粋だけ。
- **DBHub の `readOnlyHint: true` の tool が、確認を省くクライアントで実際に確認なしに書き込んだか**。試していない。
- 付録 G と同じく、**「信頼できるサーバ」の仕様上の定義**は無い。
- §4 の不明: M365 の管理者による配布の承認、TrueForge で誰がサーバを登録できるか、n8n の登録簿が注釈を審査するか、
  Devin の Plan モードが今も注釈で絞るか、Slack の実際の挙動、Notion の読み / 書きの区分の根拠、Copilot CLI 1.0.93
  （ネイティブのモジュールに移っていて読んでいない）。Claude Desktop と Cursor は付録 G のカードの配布物に頼り、取り直していない。
- GitHub Advisory Database の unreviewed の記録は、OSV の一括の取得に入らないので grep していない（検索の画面で `readOnlyHint` は 0 件 [WebFetch]）。
- AI Incident Database（JavaScript で描くページ）、NSA の文書（403）。

---

## 7. 照合の記録

| ファイル | 中身 |
|---|---|
| `evidence/annotations_security/db_search.json` | NVD・OSV の探し方・件数・当たった記録、git で確かめたコミット |
| `evidence/annotations_security/osv_hits/*.json` | OSV の記録の写し（Dynatrace 2 件、mobile-mcp、DBHub、mcp-memory-service） |
| `evidence/annotations_security/nvd_CVE-*.json` | §3.3 の CVE の NVD の記録 |
| `evidence/annotations_security/trust_gating_vqlog.txt` | §4 の担当の `verify_quote.py` の結果（83 行、すべて exact / loose） |

本記録者が 2026-10-08 に取り直した引用（`verify_quote.py`）:
- api.osv.dev の GHSA-pqh8-p93p-2rx7（2 文）・GHSA-pc2w-4mq8-32qw（1 文）・GHSA-7jx5-9fjg-hp4m（2 文）: すべて exact
- NVD API の CVE-2026-32898（1 文）: exact
- raw.githubusercontent.com の github-mcp-server v0.5.0 `dynamic_tools.go`（1 文）: exact
- gitlab.com の API の MR 231431（1 文）: exact
- wiz.io・harmonic.security・cheatsheetseries.owasp.org・embracethered.com（各 1〜2 文）: exact
- dev.to の MCPSafe（1 文）: exact。Akav Labs（2 文）: exact 1・loose 1

本記録者が git で読んだコード: dynatrace-oss/dynatrace-mcp `2851d3ce`・`15d3546c` とその親、bytebase/dbhub `d65c6b42`・`872bb338`、
sysown/proxysql `f4fd5e4c`、awslabs/mcp `e596a8b9`・`9480a33c`、doobidoo/mcp-memory-service `0a04f0b`（v10.65.3）、
microsoft/vscode `3a7c8e0`（担当の clone を点検）、openai/codex `ea27864`（同）、google-gemini/gemini-cli `44d764e`（同）。
