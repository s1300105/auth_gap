# 付随的な書き込み（裏方の書き込み）は実世界でどう扱われているか

調査日 2026-09-29。v4 の中間検証（D66）で、正 46 のうち 43 が裏方の書き込みだったことを受けて調べた。対象は初回の初期化・
キャッシュ・ログ・一時ファイル・IPC ファイル・トークンの保存。調べたのは、「読み取り専用」「副作用なし」と約束した操作の中の
こうした書き込みを、仕様・実装・研究がどう扱っているか。

**この文書は調査の記録で、決定ではない。** 違反の定義（`docs/contradiction_principles.md` §6、原理 1-i-b）は凍結済みで、
ここから変えない。重大度の列をどう定義するかは学生が決める（O44）。

**確かめ方**: 3 体の agent が一次資料を読み、逐語の引用と URL を返した。多くのサイトはプロキシで遮断されていたので、公式文書の
ソース（GitHub の raw）で読んだものが多い。確かさの印は次の 3 つ:
- **[確認]** 本記録者が原文を取得して、引用の文字列が原文にあることを確かめたもの。
- **[agent]** agent が原文を読んだと報告したもので、本記録者は照合していない。
- **[未確認]** 検索結果の抜粋だけ、または開けなかったもの。論文の数値などは使わない（CLAUDE.md 規則 1）。

---

## 1. 結論

1. **MCP の仕様は、付随的な書き込みについて何も言っていない。** "environment" の定義も例も無い。schema の全版・本文・
   公式ブログ（2026-03）・IG の憲章・SEP のどれにも、ログ・キャッシュ・一時ファイルの扱いは無かった。
2. **明示している数少ない資料は、互いに逆を向いている。**
   - 厳しい側（ログも違反）: OpenAI の ChatGPT Apps の提出ガイドは、"write logs" をする tool は `readOnlyHint: false`
     にせよと書く。**[確認]**
   - 緩い側（ログは違反でない）: HTTP の safe method（RFC 9110 §9.2.1）は、アクセスログへの追記を safe の範囲内と明記する。
     基準は「クライアントが要求しておらず、その責任を負わない」こと。**[確認]**
3. **古くからある分野（DB、言語、ファイルシステム、コンテナ）では「字義は厳しく、付随的な書き込みは基準を立てて許す」が
   多数派。** その基準は 6 種類に分かれ、どれか 1 つに合意されてはいない（§3 の表）。
4. **クライアントは、readOnlyHint を「確認なしで実行してよい」の印として使っている。** VS Code、Codex、Goose、Claude の
   connectors、GitHub Copilot coding agent、GitHub MCP server の read-only モードがそう。**書き込みの種類で区別する層は
   どこにも無い。**
5. **MCP の宣言を検証するツール（HintLint、mcp-sec-audit）も、付随的な書き込みを除外も格下げもしていない。** 読めた範囲では、
   裏方と本来の仕事を分けて数えた MCP の研究は見つからなかった（論文の本文は読めていないので「無い」とは言えない）。
6. **公式の参照サーバ自身の付け方も揃っていない。**
   - `git_status` は `readOnlyHint=True` だが、`git status` は既定で index を書き戻す（git の公式文書）。**[確認]**
   - sequentialthinking は内部の状態を貯めるのに readOnly と宣言していて、open の issue で誤りと指摘されている。**[agent]**

---

## 2. MCP の中

| 資料 | 付随的な書き込みへの言及 | 引用 |
|---|---|---|
| schema（2025-03-26 / draft / 2026-07-28） | 無し | "If true, the tool does not modify its environment." "Default: false"。注記 "all properties in ToolAnnotations are **hints**. They are not guaranteed to provide a faithful description of tool behavior" **[確認: draft]** |
| 仕様本文 server/tools.mdx | 無し | "clients MUST consider tool annotations to be untrusted unless they come from trusted servers." **[確認]**（2026-10-02 に本記録者が原文で照合: 仕様の repo（modelcontextprotocol/modelcontextprotocol、main 3098fe9）の `docs/specification/<版>/server/tools.mdx`。2025-03-26（188-189 行）・2025-06-18（193-194 行）・2025-11-25（213-214 行）・2026-07-28（305-306 行）・draft（305-306 行）のすべてにある。原文は "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers."（引用はその後半）。前は [agent]） |
| 公式ブログ "Tool Annotations as Risk Vocabulary"（2026-03-16） | 無し（logging / cache / temp / side effect の語は 0 回 **[確認]**） | 表 "`readOnlyHint: true` \| Skip the confirmation dialog" **[確認]**。"GitHub's read-only mode is the closest production analog, enabled by about 17% of users." **[確認]**（17% はブログの記載で、本記録者は検証していない） |
| PR #185（ToolAnnotations を入れた PR、2025-03） | 途中の案では観測できるかを基準にしていた | 中間案: "does not perform writes or updates, or otherwise change server-side state in ways that would be visible in subsequent tool calls." 最終文言は "does not modify its environment" に変わったが、変えた理由は見つからなかった **[agent。理由は不明]** |
| SEP-2793 "Tool Risk Metadata"（draft） | 「主作用の外の副作用」を宣言する欄を提案 | "Side effects the tool may produce beyond its primary action"。例にログ・キャッシュは無い **[agent]** |
| servers issue #4721（open） | プロセス内の状態を貯めるなら readOnly ではない、という指摘 | sequentialthinking について **[agent]** |

**作者向けの指針**

- OpenAI の ChatGPT Apps の提出ガイド **[確認]**（https://raw.githubusercontent.com/openai/plugins/main/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md）:
  - "`true` only when the tool strictly fetches, looks up, lists, retrieves, or computes data without changing state."
  - "`false` if it can create, update, delete, send, enqueue, run jobs, write logs, start workflows, or otherwise mutate state."
  - **ログの書き込みを明示的に「状態の変更」に入れている。** キャッシュ・一時ファイル・トークンの保存には触れていない。
- Anthropic Software Directory Policy **[agent]**: "MCP servers must provide all applicable annotations for their tools, in
  particular readOnlyHint, destructiveHint, and title." 付随的な書き込みには触れていない。

---

## 3. 古くからある分野の先例（許す基準で分けた）

どの分野でも「読み取り専用」は上の層の約束で、下の層の書き込みは何かの基準で許している。

| 基準 | 何を許すか | 先例と引用 |
|---|---|---|
| **A. 要求していない・責任を負わない** | ログ、課金 | RFC 9110 §9.2.1 **[確認]**: "What is important, however, is that the client did not request that additional behavior and cannot be held accountable for it. For example, most servers append request information to access log files ... and that is considered safe"。§9.2.2（冪等）: "a server is free to log each request separately" **[確認]** |
| **B. 他者から見えない** | 一時表 | MySQL の READ ONLY: "the transaction can still modify or lock temporary tables" **[未確認: 検索抜粋]**。Checker Framework `@SideEffectFree`: "Only the visible side effects are important." **[確認]** |
| **C. 論理（抽象）状態を変えない** | キャッシュ、メモ化 | C++ Core Guidelines Con.2: "A member function should be marked `const` unless it changes the object's observable state." **[確認]**。Rust `cell.rs`: "logically the operation is immutable, but e.g., caching forces the implementation to perform mutation" **[agent]**。PostgreSQL hot standby: "no changes occur to the data values themselves" **[agent]** |
| **D. 呼び出しの前からある状態に触れない** | 呼び出し中に作ったものへの書き込み | Checker Framework: "It is also allowed to modify newly created objects." **[確認]**。純粋性解析（Salcianu & Rinard の系統）: "a procedure is impure if its execution can potentially modify pre-existing state." **[agent: 二次資料 SAS 2011]** |
| **E. 決められた作業領域に閉じる** | 一時表、tmpfs、アプリ専用の領域 | PostgreSQL の READ ONLY は一時表への書き込みを許す **[agent]**。Docker `--read-only` と `--tmpfs /tmp` の併用例 **[agent]**。Android のアプリ専用の領域は権限が要らない **[agent]** |
| **F. 層が違う（メタデータ・補助ファイル）** | atime、SQLite の `-shm`、ジャーナル | PostgreSQL: "This is a high-level notion of read-only that does not prevent all writes to disk." **[確認]**。SQLite は `mode=ro` で開いても `-shm` / `-wal` を作る（agent が 3.45.1 で実測） **[agent]**。Linux の `read(2)` は atime を変える **[agent]** |

**厳しい側の先例**（付随的な書き込みも違反とする）:
- PostgreSQL の READ ONLY は、一時でないシーケンスの `nextval()` を禁じる。共有の状態なら、カウンタ 1 つの増分でも違反になる **[agent]**。
- PostgreSQL の hot standby は、利用者には一時表への書き込みも許さない **[agent]**。
- Haskell の `Debug.Trace` は、ログの出力を参照透過性の違反と明記したうえで、デバッグ用途に限って容認する **[agent]**。
- GraphQL の query は、文言上は副作用なし **[agent]**。

**定義と検査器を分ける先例**（AuthGap の立場に最も近い）:
- Checker Framework は、`@SideEffectFree` の**定義**ではキャッシュを許すが、**検査器**は保守的に拒む。
  "In particular, a method that caches its result will be rejected." **[確認]**
- 純粋性解析も、遅延初期化とキャッシュを impure と報告すると書かれている **[agent]**。
- ESC/Java2（Cok & Kiniry 2004）は、キャッシュやデバッグログのような benevolent な副作用の解釈が "not yet available" だと書く **[agent]**。
  **単一の合意された基準は無い。**

---

## 4. AI エージェントとクライアントは readOnlyHint をどう使うか

**MCP の readOnlyHint を、確認なしで実行してよいかの判断に使うもの**:

| クライアント | 使い方 | 確かさ |
|---|---|---|
| VS Code（Copilot のエージェントモード） | "tools marked with `readOnlyHint: true` in their annotations will be allowed to run without requiring user confirmation."（v1.100 のリリースノート） | [確認] |
| OpenAI Codex CLI | `requires_mcp_tool_approval`: `destructiveHint == Some(true)` なら承認、`readOnlyHint` が true なら `return false`（承認なし） | [確認: codex-rs/core/src/mcp_tool_call.rs] |
| Goose | readOnly と注釈された tool を SmartApprove で許可する | [agent] |
| Claude の connectors | "Read-only tools can run without per-call confirmation, and destructive tools always prompt." | [agent] |
| GitHub Copilot coding agent | "auto-approves tool calls only when the underlying tool is annotated with `ReadOnlyHint: true`"（issue #2483） | [agent] |
| GitHub MCP server の read-only モード | どの tool を出すかを `ReadOnlyHint` だけで決める | [agent] |
| Gemini CLI | 既定では自動承認しない。plan mode に入れるかと、利用者が書く policy の照合に使う | [agent] |
| Claude Code | 公式文書に readOnlyHint の記述が無い。第三者の報告は食い違う | [未確認] |

**自前の「読み取り専用」の定義は 3 系統**:
1. **OS の水準で書き込みを全部禁じる**: Codex のシェルの read-only サンドボックスは、書き込み可能な領域が空で /tmp も不可 **[agent]**。
2. **作業領域だけ許す**（基準 E）:
   - Claude Code のサンドボックスは、利用者ごとの temp ディレクトリへの書き込みを既定で許す **[agent]**。
   - Gemini CLI の plan mode は、自分の `plans/` への `.md` の書き込みを許す **[agent]**。
3. **構文や名前で判定し、中の書き込みは見ない**:
   - Claude Code の読み取り専用コマンドの一覧。
   - Cline は `git status` を read-only、`npm test` を safe と呼ぶ。
   - どちらも [agent]。`git status` が index を書くことは §1 のとおり。

**MCP のツールでは、クライアントは宣言をそのまま信じる。** 宣言が正しいかを確かめる層は無い。一方で仕様とブログは、
信頼できないサーバの注釈を信じるなと書いている。

---

## 5. 研究と検証ツール

- **HintLint**（complira/hintlint）**[agent]**:
  - `READONLY-001`（"Says `readOnlyHint=true`, source shows writes"）は一律 High で、書き込み先による段階は無い。
  - `writeFile` / `mkdir` / `open(..., 'w'|'a')` を一律に拾い、tmp / log / cache を除く規則は見当たらない。
  - 自分たちのパイロットについて "No confirmed wrong-annotation value appears in this validated pilot after manual review." と書く。**[確認]**
- **mcp-sec-audit**（nyit-vancouver）**[agent]**: `file_write` を能力として重みづけて数える。注釈との照合はしない。
  付随的な書き込みは区別しない。
- **論文**: arXiv の本文はどれも開けなかった **[未確認]**。検索に出たものの中に、宣言と実装の不一致を測るもの
  （"Description-Code Inconsistency in Real-world MCP Servers"、分類に "Undeclared Side Effects" があると要約される）がある。
  重大度の尺度や付随的な書き込みの扱いは不明。**本文を読むまで比較に使わない**（`docs/related_work.md` の「まだ書いていないもの」に足す）。
- **静的解析の重大度の付け方**:
  - CodeQL は `@security-severity`（0.0〜10.0）をクエリ単位で付ける **[agent]**。
  - Semgrep は likelihood × impact × confidence をルール単位で付ける **[agent]**。
  - どちらも「無害な書き込み」という類は持たない。

---

## 6. AuthGap への含意（提案。決めるのは学生）

1. **違反の定義は今のままで先例がある。** 字義で数えて、付随的な書き込みも矛にするのは、Checker Framework や純粋性解析と同じ
   「保守的な検査器」の立場。OpenAI の提出ガイド（ログも false）とも一致する。凍結したので変えない。
2. **重大度の列は、先例の基準を借りれば事前に定義できる。** 候補（どれを使うかは学生が決める）:
   - (i) **要求されたか**（基準 A）: tool の説明・引数から、その書き込みを呼び出し側が求めたと読めるか。例: mcp-aws の
     `output_file` は求めた書き込みなので本来の動作。キャッシュは求めていない。
   - (ii) **呼び出しの前からある状態に触れるか**（基準 D）: 同じ呼び出しで作って消した一時ファイルは触れない。前の呼び出しが
     残した応答ファイルの削除は触れる。
   - (iii) **tool 専用の作業領域に閉じるか**（基準 E）: `~/.cache/<tool>`、tool 専用のディレクトリ。利用者のファイルや
     共有の資格情報は閉じない。
   - (iv) **観測できるか**（基準 B / C）: 後の呼び出しや他のプロセスから結果が変わって見えるか。PR #185 の中間案の基準。
3. **重大度が大事な理由は、MCP の使われ方にある。** クライアントは readOnlyHint を見て確認を省くので、効くのは
   「確認なしで何が起きうるか」。RFC 9110 の基準（要求しておらず責任を負わない）はまさにこの状況の基準で、裏方の書き込みを
   「違反だが、確認を省いても利用者の責任にならない側」に置く根拠になる。ただしトークンの保存や共有の IPC ファイルのように、
   基準によって判定が割れるものがある（A なら許容、B / C なら違反）。**割れたものは黙って片方に倒さず、不明として数える**
   （規則 4）。
4. **報告の形の提案**: 矛の件数を「本来の動作」と「裏方」（基準ごとの内訳つき）に分けて出す。合算の精度だけを出さない。
   基準の定義と判定手順は、最終評価の結果を見る前に `docs/preregistration.md` と教科書 第 38 章に書く。

---

## 7. 確かめられなかったもの

- modelcontextprotocol.io、developers.openai.com（Apps SDK の本体の文書）、cursor.com、arxiv.org、rfc-editor.org などは
  プロキシで遮断されていた。RFC 9110 は httpwg/http-core の XML 原稿で読んだ（文言は同じ）。
- PR #185 で文言を変えた理由。GitHub が畳んだコメントは読めていない。
- Claude Code が MCP の readOnlyHint を権限の判定に使うか。Cursor・Windsurf の挙動。
- MCP の不一致を測る論文の本文（数値・分類・重大度の尺度）。
- MySQL の READ ONLY と一時表、GCP roles/viewer、AWS ReadOnlyAccess の公式の説明文（検索抜粋か第三者のミラーだけ）。
- 「付随的な書き込みを理由に readOnlyHint を議論した issue」は sequentialthinking の #4721 以外に見つからなかった。
  探し方に漏れがある可能性は残る。
