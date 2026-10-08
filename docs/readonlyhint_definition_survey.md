# readOnlyHint の「環境」は何を指すか（仕様の一文より詳しい資料の調査）

調査日 2026-10-08。

**学生の問い**: 「仕様内の定義（`If true, the tool does not modify its environment.`）は短すぎでは？もっと説明したものが
あるのでは？調査して」

**この文書は調査の記録で、決定ではない。** 違反の定義（`docs/contradiction_principles.md` 原理 1-i-b）と手引き 15.1 の D1 の問い
は、ここから変えない。変えるかどうかを学生が決める必要があるものは `docs/open_questions.md` の O47 に置いた。

**前の調査との関係**: `docs/annotations_official_survey.md`（2026-10-02、宣言の位置づけと使われ方）と
`docs/incidental_writes_practice.md`（2026-09-29、ログ・キャッシュなど付随的な書き込みの扱い）の続き。この文書で新しく
足したのは、(1) 一文の定義ができるまでの経緯（PR #185 の草案）、(2) 削除された旧 docs の例、(3) 公式の参照サーバと SDK の
最近の判断、(4) 引数で振る舞いが変わるツールの扱い。

**確かさの印**（CLAUDE.md 規則 1）:
- **[確認]** 本記録者が原文を取得し、引用の文字列が原文にあることを `scripts/verify_quote.py` で確かめたもの（exact か loose）。
  Markdown・コメントの記号（`*` `-` `|` `///`）だけが違うものは「記号を除いて一致」と書く。git の commit は `git log` で確かめた。
- **[agent]** 調査の agent が読み手の中継（r.jina.ai）で原文と照合したと報告したもので、本記録者は照合していない。
  github.com の issue・PR のページは、本記録者の環境からは 403 で開けなかった。
- **[判断]** 資料に書いてあることではなく、本記録者の考え。事実として使わない。

引用は英語の原文のまま載せ、すぐ後に日本語の言い換えを付ける。元データ（241 件の候補、検証の結果、却下した 28 件の理由）は
`evidence/readonlyhint_definition/`。

---

## 1. 結論

1. **MCP の仕様は、readOnlyHint を一文でしか定義していない。** 2025-03-26 に入ってから今の draft まで、文は一字も変わって
   いない。「environment」の定義も、何をすれば変えたことになるかの一覧も、仕様のどこにも無い。**[確認]**
2. **最初の草案は、もっと具体的だった。** 2025-03 の PR #185 の草案は「書き込みや更新をせず、後のツール呼び出しから見える形で
   外部の状態（のちにサーバ側の状態）を変えない」と書いていた。2025-03-21 に「environment」の語に置き換わり、03-24 に今の
   一文になった。**語を変えた理由は PR のどこにも書かれていない（不明）。** 設計者は、意味の精密さより拡張しやすさを取ったと
   明言している。**[確認]**
3. **公式の補足資料は、用途と例を足すが、範囲は定義しない。** 旧 concepts ページ（2026-03-25 に削除）、公式ブログ
   （2026-03-16）、Interest Group の文書、公式 SDK の文書がそう。公式の文で一番踏み込んでいるのは C# SDK の docstring
   （「計算資源の使用を超える副作用を持たない。どのシステムでもデータを作成・更新・削除しない」）だが、AI が下書きし保守者が
   直した文である。**[確認]**
4. **公式の参照サーバは、プロセスのメモリの中の状態も数える方向に動いた。** sequentialthinking は 2026-03 に「メモリの中の
   蓄積は環境の副作用ではない」として readOnlyHint: true にされ（[agent]）、2026-10-04 に「メモリの履歴が増えるので true は
   誤り」として false に直された（[確認]）。**手引きの D76 の 2（メモリは数えない）と逆向きなので、O47 に置いた。**
5. **公式でない資料は、細部で割れている。** ログ（OpenAI は false、RFC 9110 はアクセスログを safe とする）、キャッシュ
   （Anthropic の旧ローカル提出ガイドは内部のキャッシュなら true でよい）、一時ファイル（同じガイドは「一時的な書き込みも
   数える」）、ローカルとリモート（AWS の aws-api サーバは「read-only はファイルシステムを指さない」）。**[確認]**
6. **引数で振る舞いが変わるツールの扱いは、仕様では決まっていない。** 「すべての引数での最悪の場合で宣言する」案はあるが、
   SEP-1862 も IG の PR #9 も採択されていない。OpenAI は「状態を変えられない（cannot）ときだけ true」、Anthropic と
   OpenAI は読みと書きを別のツールに分けさせる。**[確認]**

---

## 2. 仕様の文

| 何 | 原文 | 版 | 確かさ |
|---|---|---|---|
| readOnlyHint | `If true, the tool does not modify its environment.` `Default: false` | 2025-03-26・2025-06-18・2025-11-25・2026-07-28・draft で同じ。2024-11-05 には ToolAnnotations 自体が無い | [確認]（schema ページ、schema.ts） |
| ToolAnnotations 全体の注 | `NOTE: all properties in ToolAnnotations are hints. They are not guaranteed to provide a faithful description of tool behavior (including descriptive properties like title).` | 全版（2026-07-28 から書式だけ変わる） | [確認]（記号を除いて一致） |
| openWorldHint | `For example, the world of a web search tool is open, whereas that of a memory tool is not.` | 全版 | [確認] |

- 訳: readOnlyHint は「true なら、そのツールは自分の環境を変えない。既定値は false」。ToolAnnotations は「すべてヒントで、ツールの
  振る舞いを忠実に表すとは保証されない」。
- 仕様の Tools のページは `annotations: Optional properties describing tool behavior` と信頼の注意だけを書き、4 つのヒントの中身は
  schema に任せている（`docs/annotations_official_survey.md` §1.1）。
- ToolAnnotations の中で具体例があるのは openWorldHint だけ（Web 検索は開いた世界、メモリのツールは閉じた世界）。readOnlyHint には
  例が無い。
- 版の間で ToolAnnotations の文が変わったのは、idempotentHint の誤記「on the its environment」を直した 1 か所（commit `50671e92`、
  2025-10-02、Habib Lawal）と書式だけ。**[確認]**（commit は git で確かめた）

---

## 3. 一文ができるまで（PR #185、2025-03）

ToolAnnotations は PR #185（当時の repo 名は `modelcontextprotocol/specification`、2025-03-26 にマージ）で入った。草案の文は
次のように変わった。commit の文は raw で照合した（loose。行頭の `*` などの記号の差）。**[確認]**

| 日付 | commit | readOnly の説明 |
|---|---|---|
| 2025-03-04 | `6179891` | `If true, this tool does not perform writes or updates, or otherwise change external state in ways that would be visible in subsequent tool calls.` |
| 2025-03-15（commit 03-18） | `25c8e7c` | 同じ文の `external state` が `server-side state` になる |
| 2025-03-21 | `3a96a59` | 3 つの性質をまとめた effectHints の説明として `Describes the effects a tool may have on its environment.` が入る。「environment」の初出 |
| 2025-03-24 | `f025054` | 平らな真偽値に分けたとき、今の `If true, the tool does not modify its environment.` になる |

- 訳（最初の 2 つ）: 「true なら、このツールは書き込みや更新をせず、ほかの形でも、後のツール呼び出しから見える形で外部の
  （サーバ側の）状態を変えない」。範囲（外部 → サーバ側）と、判定の基準（後の呼び出しから見える変化か）がはっきり書かれていた。
- 3/21 の commit `3a96a59`（Basil Hosmer）のメッセージには、`🤖 Generated with [Claude Code]` の表示がある。**[確認]**（git）
  PR #185 は 2025-03-26 に merge commit `868b1fd6` で入った。**[確認]**（git）
  **なぜ「server-side state … visible in subsequent tool calls」を「environment」に変えたかは、PR の本文にもレビューにも
  見つからなかった。** [不明]

**設計者の発言**（PR #185 のレビュー。Wayback 2025-04-07 の写しで照合）**[確認]**:

- 作者（Basil Hosmer、`bhosmer-ant`。発言者は Wayback の写しの並びで確かめた）: `There's definitely an elephant in the room here, that clients will often want to know much more fine-grained and varietal operational information about the behavior of specific tools than we can provide in a universal schema.`
  — 訳: 「クライアントは、共通のスキーマで出せるよりずっと細かい動作の情報を知りたがる。それは分かっている問題だ」。
- 作者: `I think of the metric as being some kind of 80/20 rule where a property is informative enough, for enough tools, to warrant inclusion.`
  — 訳: 「入れる性質は、十分多くのツールについて十分役に立つか、という 80/20 の基準で選ぶ」。
- 作者（2025-03-24）: `In the presence of extensibility it feels like the ROI of the extra precision isn't high enough to offset the extra fussiness, …`
  — 訳: 「拡張できる以上、精密にする手間に見合う得は無い」。続けて `switched from the variant-type setup to simple boolean properties. The data model is less precise in a closed world …`（型で依存関係を表す形をやめ、単純な真偽値にした。閉じた世界では精密さが下がる）。
- 作者（2025-03-21、仕様本文に annotations の説明を足すかについて）: `I'm not sure if the aim is to be concise here and defer to the schema for the full definition, or we want to be completist, …`
  — 訳: 「本文は簡潔にして定義は schema に任せるのか、網羅的に書くのか分からないので、足さずにおいた」。**仕様本文の説明が短い
  直接の経緯。**
- 作者（openWorld について）: `My mental model for this is that it describes whether or not a tool operates in a closed environment - so e.g. a database tool would be false (as would the current filesystem tool), but an open web query tool would be true.`
  — 訳: 「閉じた環境で働くか。DB やファイルシステムのツールは閉じていて、Web の問い合わせは開いている」。作者が「environment」を
  「ツールが働く領域（DB・ファイルシステム）」の意味で使った例。**readOnly についての発言ではない。** [判断] readOnly の
  「its environment」も同じ意味で書かれたと読む手がかりにはなるが、根拠としては弱い。

**元になった要望**（issue #114、2024-12-13。Wayback で照合）**[確認]**:
- `a user might be happy with AI systems reading any of the data in their database, but not editing any of it without checking with them`
  — 訳: 「データベースのデータを読むのは任せてよいが、変えるときは確かめてほしい利用者がいる」。read-only の区別の原型。
- `A way for the server to easily respond with a more precise risk level for a given call` — 訳: 「呼び出しごとのリスクを返す
  仕組み」。**この案は採られず、注釈はツール単位の静的な宣言になった。** 引数で振る舞いが変わるツールの扱いが決まっていない背景。

---

## 4. 公式の補足資料（どれも規範ではない）

### 4.1 旧 concepts ページ（2025-04-10 に追加、2026-03-25 に削除）

`docs/legacy/concepts/tools.mdx`（commit `e30f85cb`）。今の URL は仕様の Tools ページへ転送され、内容は仕様に移されていない。
元は docs の PR #264（commit に Claude Code 生成の表示あり）を、作者が PR #316 で手直ししたもの。**[agent]**。下の引用は **[確認]**

- 目的: `3. Convey information about a tool's potential side effects` `4. Assist in developing intuitive interfaces for tool approval`
  — 訳: 「ツールの潜在的な副作用を伝える」「承認の UI を作る助けにする」。
- 表の readOnlyHint の行は `If true, indicates the tool does not modify its environment` で、仕様と同じ。
- 例（範囲の説明は無いが、線の引き方が分かる）:

| 例のツール | readOnlyHint | openWorldHint | ほか |
|---|---|---|---|
| `web_search`（`// A read-only search tool`） | true | true | 外の世界に問い合わせても read-only |
| Delete File | false | false | destructive: true、idempotent: true |
| Create Database Record | false | false | destructive: false（足すだけ） |
| Calculate Sum | true | false | 計算だけ |

- 心得: `**Be accurate about side effects**: Clearly indicate whether a tool modifies its environment and whether those modifications are destructive.`
  — 訳: 「副作用について正確に。環境を変えるか、それが破壊的かをはっきり示す」。どの副作用を数えるかは書かれていない。

### 4.2 公式ブログ "Tool Annotations as Risk Vocabulary"（2026-03-16）

Markdown の原稿（仕様の repo `0a11bf6`）で照合した。**[確認]**

- `readOnlyHint: Does the tool modify its environment?`（記号を除いて一致）— 一文を疑問形にしただけで、範囲は説明しない。
- `The first three hints mostly answer a preflight question: should the client ask for confirmation before calling this tool?`
  — 訳: 「最初の 3 つは、呼ぶ前に確認を求めるか、という問いに答える」。
- 表の readOnlyHint の行: `readOnlyHint: true` → `Skip the confirmation dialog`（記号を除いて一致）。
- 範囲の語が配置で変わると認めた文はあるが、**openWorldHint の「External」についてで、readOnlyHint の「environment」についてでは
  ない**: `"External" might mean anything outside a corporate network or anything beyond the local machine, depending on where the server runs.`
- `A server can claim readOnlyHint: true and delete your files anyway.` — ローカルのファイル削除は read-only でない、という例。
- サーバ作者への助言は `set readOnlyHint: true on read-only tools` で、循環していて基準にはならない。
- 未解決の問い: `whether any annotations should be evaluated at runtime rather than declared statically`（実行時に評価する注釈）。

### 4.3 Interest Group（Tool Annotations IG）

- 憲章（2026-04-20）は、既存の 4 つのヒントで足りるかを検討の対象にしている（`docs/annotations_official_survey.md` が既に引いた）。
- 実験の repo の草案（`fecace7`）は既存のヒントを「coarse（粗い）」「legacy」と呼ぶ: `MCP today treats all tool calls as equivalent at the protocol level beyond the coarse readOnlyHint / destructiveHint / idempotentHint / openWorldHint hints.` **[確認]**
- **引数への依存に一番はっきり答えているのは、未マージの PR #9（tool-resolution、head `5d1276f`、2026-08-20）。** **[確認]**
  - `A multi-action file tool may read, append, replace, or delete; its static ToolAnnotations must conservatively describe the most risky possibility, …`
    — 訳: 「読む・追記・置換・削除をするファイルのツールは、静的な注釈で最も危ない場合を表さなければならない」。
  - `Static annotations remain the conservative fallback. For every valid argument set: - readOnlyHint: true in tools/list means every resolution MUST also be read-only.`
    — 訳: 「tools/list の readOnlyHint: true は、すべての妥当な引数で read-only であることを意味する（MUST）」。
  - 同じ表で、ファイルの `read` は readOnlyHint: true、`append` は readOnlyHint: false・destructiveHint: false。
  - **規範ではない**（実験的な拡張の、マージ前の草案）。

### 4.4 SEP の草案（どれも採択されていない）

- SEP-1862（tool resolution、head `c934643`）: `the annotations field SHOULD represent the worst-case (most conservative) behavior across all possible arguments` — 訳: 「注釈はすべての引数での最悪の場合を表すべき」。**[確認]**
- PR #616（head `986918f`、2025-05-31。仕様の一文は変わっていないので、取り込まれていない）は、一文に説明を足す案だった: `This means the tool only reads or retrieves information without making any changes to data, files, or system state.` と、例 `readOnlyHint: true → search_database, get_weather, read_file` / `readOnlyHint: false → create_user, delete_file, send_email`。**仕様に入らなかった説明の実例。** **[確認]**
- PR #1884 の草案（採択されていない）: 同じ `github_api` ツールでも `GET /repos/:owner/:repo` は read-only、`POST …/issues` は追加、`DELETE` は破壊的。**[確認]**

### 4.5 公式 SDK の文書

| SDK | 文 | 足していること | 確かさ |
|---|---|---|---|
| Python（docs、`91941ed`） | `read_only_hint=True: this tool doesn't change anything.` | 「何も変えない」と最も広く言い換える | [確認]（記号を除いて一致） |
| TypeScript（docs、`b022522`） | メモリの中の配列を空にする `clear-catalog` を `readOnlyHint: false, destructiveHint: true, idempotentHint: true` にした例 | **プロセスのメモリの中の状態を変えるだけでも read-only でない**、という例。文章の定義ではない | [確認] |
| C#（`ToolAnnotations.cs`、`3338e88`） | `Read-only tools do not have side effects beyond computational resource usage. They don't create, update, or delete data in any system.` | 許される副作用は計算資源の使用だけ。対象は「どのシステムでも」 | [確認]（記号を除いて一致） |
| C# の由来 | PR #238 の第 1 commit `AI generated /// comment updates`（2025-04-08）。下書きは `(CPU, memory, etc.)` と書いていた | 上の文は AI が下書きし、保守者が直したもの | [確認] |
| FastMCP（PrefectHQ、公式でない） | `For tools that write to databases, send notifications, create/update/delete resources, or trigger workflows, omit readOnlyHint or set it to False.` | 通知の送信やワークフローの起動も read-only でない | [確認]（記号を除いて一致） |

- SDK の保守者は、宣言が正しいかは作者の責任で SDK は確かめられない、という立場（python-sdk issue #2937、csharp-sdk issue #1454
  の `it's a fact about their code, not a hint`）。**[agent]**

### 4.6 公式の参照サーバとメンテナの判断

- **filesystem**（`5abed86`）: README の表で `write_file` は readOnlyHint: false。読み取り系は「Pure read」。**[確認]**
- **sequentialthinking**（呼ぶたびにメモリの中の思考の履歴が増えるツール）:
  - 2026-03-15、メンテナ（olaservo）のレビュー（servers PR #3534）: `the tool doesn't modify any external environment (files, network, DB). The in-process state accumulation (thoughtHistory, branches) is an implementation detail, not an environmental side effect in the MCP sense.`
    — 訳: 「外の環境（ファイル・ネットワーク・DB）を変えない。プロセスの中の状態の蓄積は実装の細部で、MCP の意味での環境への
    副作用ではない」。これで readOnlyHint: true にされた。**[agent]**
  - 2026-10-04、メンテナ（cliffhall）の commit `8a4139c`（v2/main。issue #4721 を閉じる）: `Every sequentialthinking call appends to the server's in-memory thoughtHistory (and branches) and returns a growing thoughtHistoryLength, so advertising readOnlyHint and idempotentHint as true was wrong: a client may skip a confirmation, or retry a call, on the strength of those hints.`
    — 訳: 「呼ぶたびにメモリの中の履歴が増えるので、readOnlyHint を true とするのは誤りだった。クライアントはこのヒントで確認を
    省いたり、再試行したりする」。v2/main のコードは readOnlyHint: false になっている。**[確認]**（git の commit・changeset・コード）
  - ただし main（`5abed86`、2026-10-04 00:01）のコードはまだ readOnlyHint: true。**[確認]**
  - `docs/incidental_writes_practice.md`（2026-09-29）は、この件を「open の issue」と書いた。その後に直された。
- **everything**（注釈の付け方の参照例にするとした servers PR #3246。2026-05-17 にマージ **[agent]**）: コードの値は次のとおり。**[確認]**
  （値は `5abed86` のコード。理由の文は PR の本文で、**[agent]**）

| ツール | readOnlyHint | PR の本文の理由 |
|---|---|---|
| `trigger-long-running-operation`（進捗の通知を送るだけ） | true | `Simulates work with progress, no lasting state change` |
| `toggle-simulated-logging`（サーバの中のログの設定を切り替える） | false | `Toggles server-side logging state (not idempotent)` |
| `trigger-elicitation-request`（クライアントに利用者への問い合わせを頼む） | false | `Triggers user-facing dialog via client` |
| `trigger-sampling-request`（クライアントに LLM の呼び出しを頼む） | false | `Triggers LLM inference (external API)` |
| `gzip-file-as-resource`（セッションのリソースを作る） | false | — |
| `simulate-research-query`（裏で動くタスクを作る） | false | — |

  - PR の本文は readOnlyHint を `true when the tool only returns data with no side effects` と説明する。**[agent]**
  - [判断] 基準は「後に残る状態の変化があるか」で、PR #185 の最初の草案（後の呼び出しから見える変化か）に近い。メモリの中の
    状態（ログの設定）も変化に数えている。

---

## 5. 公式でない資料（クライアント・プラットフォーム・標準）

| 出どころ | 文 | 足していること | 確かさ |
|---|---|---|---|
| OpenAI 審査の FAQ（app-review） | `Set to false if the tool can create/update/delete anything, trigger actions (send emails/messages, run jobs, enqueue tasks, write logs, start workflows), or otherwise change state.` | **ログを書くなら false**。「can」なので、変えうる引数が 1 つでもあれば false と読める | [確認] |
| OpenAI plugin-guidelines | `Use false for external-state changes, persisting artifacts, starting stateful jobs or workflows, queuing work, or write-style outbound actions such as posting messages, sending emails, or uploading files.` | 成果物の保存・キュー投入・外への送信も false | [確認] |
| OpenAI build/mcp-server | `readOnlyHint: true only when the tool cannot change state.` | 「変えられない」ときだけ true（最悪の場合で読む） | [確認] |
| OpenAI 旧版（2025-12、Wayback） | `does not change anything outside of ChatGPT` | 範囲を「ChatGPT の外」としていた（のちに書き換え） | [確認] |
| Anthropic 旧ローカル提出ガイド（2026-03、Wayback。今は削除） | `Creates temp files destructiveHint: true Even temporary writes count` と `Caches internally only readOnlyHint: true Internal optimization OK` | **一時ファイルは数える、内部のキャッシュだけなら read-only でよい。** 「内部」がメモリだけかディスクも含むかは書かれていない | [確認] |
| Anthropic 旧リモート提出ガイド（2026-04、Wayback） | `destructiveHint: true - For tools that modify data or have side effects` | 副作用一般を read-only でない側に入れる | [確認] |
| Anthropic 現行の審査基準（connectors） | `Read-only tools can run without per-call confirmation, and destructive tools always prompt.` と `Split a catch-all tool into a read-only tool and one or more write tools.` | 用途（確認の省略）と、引数で読み書きが変わるツールを分けさせる規則。旧ガイドの一時ファイル・キャッシュの表は引き継がれていない | [確認] |
| Claude Agent SDK | `A tool marked readOnlyHint: true can still write to disk if that’s what the handler does. Keep the annotation accurate to the handler.` | **ローカルのディスクへの書き込みは readOnlyHint: true と食い違う**、という前提 | [確認] |
| AWS Labs aws-api-mcp-server README | `"Read-Only" only refers to the API classification, not the file system, that is such "read-only" actions can still write to the file system if necessary or upon user request.` | **範囲を遠隔の API に限り、ローカルのファイルを除く**。上の Claude Agent SDK と逆 | [確認] |
| Google MCP Toolbox | `Tool only reads data, no modifications to the environment.` | 一文の言い換え | [確認] |
| RFC 9110 §9.2.1（HTTP の safe method。MCP ではない） | `most servers append request information to access log files … and that is considered safe` | **アクセスログへの追記は safe**。基準は「クライアントが求めておらず、責任を負わない」こと | [確認] |
| RFC 9110 §9.2.1 | `When a resource is constructed such that parameters within the target URI have the effect of selecting an action, it is the resource owner's responsibility to ensure that the action is consistent with the request method semantics.` | 引数で操作を選べるなら、宣言と食い違わないようにするのは提供者の責任 | [確認] |
| aident.ai のブログ（2026-09） | `If any accepted input can do that, a blanket read-only annotation is misleading unless the server splits the behavior into separate tools or constrains the schema.` | 受け付ける入力の 1 つでも状態を変えうれば read-only は誤り。リモートのキャッシュの更新も変化に数える | [確認] |

---

## 6. 論点ごとの食い違い

| 論点 | 数える側（read-only でない） | 数えない側（read-only でよい） | 仕様 |
|---|---|---|---|
| ローカルのファイル | Claude Agent SDK、filesystem サーバ、公式ブログの例、旧 docs の Delete File | AWS aws-api（read-only は API の分類だけ） | 決めていない |
| ログ | OpenAI（write logs → false） | RFC 9110（アクセスログは safe） | 決めていない |
| キャッシュ | aident（リモートのキャッシュの更新） | Anthropic 旧ローカルガイド（内部のキャッシュだけなら可） | 決めていない |
| 一時ファイル | Anthropic 旧ローカルガイド（一時的な書き込みも数える） | （この調査では確かめられた資料が無い。`docs/incidental_writes_practice.md` §3 の MySQL の一時表は [未確認]） | 決めていない |
| プロセスのメモリ | TS SDK の例、everything、sequentialthinking の修正（2026-10-04） | sequentialthinking の 2026-03 の判断 **[agent]**（PR #185 の草案の「後の呼び出しから見えるか」は、どちらにも読める） | 決めていない |
| プロトコルの中のやり取り | everything（elicitation・sampling は false） | everything（進捗の通知は true）、TS SDK の例（ログの通知を送るツール `multi-greet` が true **[agent]**） | 決めていない |
| 外への読み取り（GET） | — | 旧 docs の web_search、PR #1884 の github_api の GET | 決めていない（外と関わることは openWorldHint で表す） |
| 引数で変わる | OpenAI「cannot」、SEP-1862・IG PR #9 の最悪の場合、aident | — | 決めていない（両案とも未採択） |

---

## 7. AuthGap への含意（[判断]。決めるのは学生）

1. **手引き 15.1 の D1 の問い（ファイル・DB・相手のサーバの状態・残る設定。メモリは入れない）は、どの資料にもそのまま書かれた
   基準ではない。** 仕様の一文をこの研究で操作できるようにした定義で、論文ではそう書く（「仕様は environment を定義していない。
   本研究は 15.1 の範囲で判定した」）。根拠には §2 と §3 の事実を引ける。
2. **キャッシュ・ログ・一時ファイルを数えるのは、厳しい側に立つ選択。** 支える資料（OpenAI、Claude Agent SDK、公式ブログの
   ファイル削除の例、Anthropic 旧ガイドの一時ファイル）も、逆の資料（Anthropic 旧ガイドの内部のキャッシュ、RFC 9110 のログ。
   PR #185 の草案の「後の呼び出しから見えるか」も、読み返さないログは数えない側に読める）もある。原理 1-i-b は凍結済みなので変えない。この食い違いには、
   `write_target` のラベルと D84 の層別（重い書き込み先だけの数）で答える設計になっている。論文の脅威の節に、両方の資料を書く。
   - 例: 前に見た geocode の例（`~/.geo_cache/` への JSON の書き込み）は、手引きでは正（キャッシュ・状態の保存）。Anthropic 旧ガイドの
     「内部のキャッシュだけなら可」を「ディスクのキャッシュも含む」と読めば、read-only のままでよいことになる。
3. **プロセスのメモリを数えないのは、緩い側に立つ選択で、公式の参照サーバの最新の判断（2026-10-04）と逆向き。** D76 の 2 は
   学生が選んだ決定で、手引きはまだ封をしていない。保つか変えるかを O47 に置いた。どちらでも、解析器（凍結）はメモリの中の
   状態を効果として出さないので、主の数（矛の精度）は変わらない。変わるのは、実態調査と見落としの判定で人が「違反」と書くかどうか。
4. **引数の扱い（手引き 14.3「届きうるなら到達する」）は、最悪の場合で読む案と同じ向き。** SEP-1862・IG PR #9・OpenAI の
   「cannot」・RFC 9110 の「提供者の責任」を、手引きの読み方の傍証として引ける。ただし MCP の規範ではない（草案と他社の文書）。
5. **関連研究**: 宣言とコードの食い違いを主な失敗として名指しした文書がある（Google の issue #440 の「manifest drift」**[agent]**、
   SEP-3140 の草案 **[agent]**）。`docs/related_work.md` に足すかは論文を書くときに決める。

---

## 8. 確かめられなかったもの

- **「server-side state … visible in subsequent tool calls」を「environment」に変えた理由。** PR #185 の本文・レビュー・commit の
  メッセージに見つからなかった。[不明]
- github.com の issue・PR のページ（servers #3534・#3246・#3572・#3401・#4721、python-sdk #2937、csharp-sdk #1454、仕様 #440）は、
  本記録者の環境から 403 で開けなかった。agent が読み手の中継で照合した報告だけがある（**[agent]**）。値やコードで確かめられる
  ものはコードで確かめた（§4.6）。
- Anthropic の旧提出ガイドは、今の URL が 404 か移転の案内で、Wayback の写しでだけ確かめた。「Caches internally only」の
  「internally」がメモリだけかディスクも含むかは、原文から決まらない。[不明]
- 調査の agent が出した候補 241 件のうち 28 件は、検証役が「引用が主張を支えない」などとして却下した（理由は
  `evidence/readonlyhint_definition/sources.json` の `rejected`）。この文書はそれを使っていない。
