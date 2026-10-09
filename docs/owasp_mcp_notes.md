# OWASP の MCP 関連文書から AuthGap に使えるところ（2026-10-09、本記録者の調査。**決定ではない**）

**学生の問い**: 「OWASP MCP が公開されていると思うのでそれを読んで。そしてなにか使える部分があるかをおしえて」
（直前の話題: D と M のずれが脆弱性につながることを論文で示したい。）

この文書は読んだ記録で、決定ではない。解析器・手引き・事前登録の下書きは変えていない。元データは `evidence/owasp_mcp_20261009/`。

**確かさの印**:
- **[確認]** 本記録者が原文と照合した。Top 10 は `OWASP/www-project-mcp-top-10` @`165fe0f`（2026-07-29）の raw を `scripts/verify_quote.py`
  で照合（exact）。Cheat Sheet は公開ページを `verify_quote.py` で照合（exact）。
- **[確認・PDF]** genai.owasp.org の PDF は 2026-10-09 に本記録者の取得で 403 だった。調査の agent が同日に取得した PDF から、本記録者が
  pypdf で文字を取り出して照合した（空白と引用符だけを正規化。全件一致）。ページ番号は PDF のページ。
- **[agent]** 調査の agent が `verify_quote.py` で照合したと報告したもので、本記録者は照合し直していない（`evidence/owasp_mcp_20261009/adjacent_owasp_docs.json`）。

---

## 1. 読んだもの

| 文書 | 出す側 | 版・日付 | 状態 |
|---|---|---|---|
| **OWASP MCP Top 10**（MCP01〜MCP10 と推奨管理策 2 つ） | OWASP の project（`www-project-mcp-top-10`） | 「version [v0.1]」。ロードマップは「Phase 3 – Beta Release and Pilot Testing - We are here right now」 [確認] | **beta**。次の版は 2026 年 10 月の予定と書かれている |
| MCP Security Cheat Sheet ほか Cheat Sheet 6 つ | OWASP Cheat Sheet Series | 最終変更 2026-10-04 | 頻繁に書き換わる。引くときは取得日を添える |
| A Practical Guide for Secure MCP Server Development | OWASP GenAI Security Project | v1.0、2026-02 | PDF |
| A Practical Guide for Securely Using Third-Party MCP Servers 1.0 | 同 | 2025-10 | PDF |
| OWASP Top 10 for Agentic Applications 2026（ASI01〜ASI10） | 同 | 2025-12 | PDF |
| OWASP Top 10 for LLM Applications 2026 | 同 | 2026（PDF の表紙の日付は未記入） | PDF |

- Top 10 の MCP06 は、一覧のページ（`tab_top10.md`）では「Prompt Injection via Contextual Payloads」、本文と目次では「Intent Flow
  Subversion」と、名前が揃っていない [確認]。引くときは本文の名前と URL を使う。

## 2. 結論

1. **OWASP は「宣言（注釈）が偽・誤り」を、まだ独立した脆弱性の類として挙げていない。** Top 10 の本文に annotations の語は無い。推奨管理策
   「Client-Side Tool Risk Gating」と Cheat Sheet の 1 文（2026-10-04 に追加）にだけ出る [確認]。AuthGap の論文は、既存の類（MCP03・ASI02・
   ASI09・LLM03）に結びつけたうえで、**「宣言と実装の食い違い」という切り口を足す**と書ける。
2. **OWASP 自身が「説明と実際の振る舞いを照合せよ」と勧めている。** MCP サーバ開発ガイドの "Validate Descriptions vs. Behavior" と、
   最低限の基準のチェック項目 "Tool descriptions are validated against runtime behavior." [確認・PDF]。AuthGap は、このうち**機械が読む宣言
   （注釈）について、コードから静的に照合する**もの、と位置づけられる。ただし OWASP の対象は説明文（description）で、手段は手作業・
   版の固定・LLM・実行時。
3. **OWASP の推奨の多くは、ツールの性質（読むだけか、破壊的か、外に出るか）を知っていることを前提にしている。** 自動承認の段階づけ、
   破壊的な操作への人の確認、目的に合う操作だけを許す PDP、危険度の点数。その性質の入力に注釈を使えば、**宣言の誤りがそのまま
   これらの防御の誤りになる**。これが「ずれ → 脆弱性」の筋を OWASP の言葉で書く方法になる（ただし「注釈を入力に使う」と OWASP が
   書いているのは推奨管理策の危険度の点数だけ。ほかは AuthGap 側の推論として書く）。
4. **OWASP は、版の固定・ハッシュ・説明文の検査では「最初から食い違っている宣言」を捕まえられないと認めている。** AuthGap はその隙間を
   埋める、と書ける。

## 3. 論文のどこに使えるか

### 3.1 脅威の道筋（「ずれ → 脆弱性」）

前の回答の 4 条件（① クライアントが宣言を信じて確認を省く ② 利用者以外がツールを呼ばせられる ③ 隠れた効果に害がある ④ 呼び出しの
値で対象が決まる）に、OWASP の文を当てる。

| 条件 | OWASP の文 | 出典 | 確かさ |
|---|---|---|---|
| ①（自動承認の運用がある） | "A graduated enforcement policy (audit, warn, block, escalate) permits low-consequence or easily reversible actions to auto-approve" | LLM Top 10 2026、LLM03 Excessive Agency、p.26 | [確認・PDF] |
| ①②③ を 1 つの例で | "Approved Tool misuse: A coding agent has a set of tools that are approved to auto-run because they pose supposedly no risk, including a ping tool."（続けて、そのツールを繰り返し呼ばせて DNS で持ち出す例） | Agentic Top 10 2026、ASI02 Tool Misuse、p.14 | [確認・PDF] |
| ①（読むだけと思わせる手口の名前） | "Consent laundering through “read-only” previews" | Agentic Top 10 2026、ASI09、p.35 | [確認・PDF]（対象は UI のプレビューで、注釈ではない。用語を借りる形で引く） |
| ②（取ってきた内容がツールの呼び出しを乗っ取る） | "subversion happens "in-flow": the model retrieves a resource that contains "hidden instructions" which override the original user intent." | Top 10 MCP06 | [確認] |
| ②④（ツールの引数は信用できない） | "Validate all inputs to MCP server tools — treat them as untrusted (they originate from LLM output influenced by potentially malicious context)." | MCP Security Cheat Sheet §5 | [agent] |
| ③（害の型） | "The agent uses its connected MCP tools to perform destructive or privileged actions (e.g., deleting repositories, modifying cloud config)." | Top 10 MCP06、Impact | [確認] |
| ④（引数が対象を選ぶ） | "File path operations accept unsanitized input, allowing directory traversal (../../../etc/passwd) or overwriting critical files." | Top 10 MCP05、checklist | [確認] |

### 3.2 「宣言に頼る認可は脆弱」の根拠

- Top 10 MCP07 の「脆弱な状態」のチェック項目: "Authorization decisions rely on client input or context hints rather than server-side checks" と
  "Access control checks rely solely on client-side enforcement" [確認]。注釈（仕様の語で hint）を見て確認を省くことは、前者に当たると書ける
  （当てはめは AuthGap 側の推論）。

### 3.3 AuthGap の位置づけ（OWASP の推奨を機械化するもの）

| OWASP の推奨 | 出典 | AuthGap との関係 | 確かさ |
|---|---|---|---|
| "Validate Descriptions vs. Behavior: Implement manual checks, tool pinning, and LLM scans to ensure a tool's advertised functionality (in its description) matches its actual code behavior during runtime." | MCP サーバ開発ガイド p.7 | 注釈について、この照合をコードから静的に行う | [確認・PDF] |
| "Flag any tool that attempts to perform actions (e.g., network writes) not mentioned in its description." | 同 p.7 | 矛（宣言に無い効果）はこれに当たる | [確認・PDF] |
| "Tool descriptions are validated against runtime behavior."（最低限の基準のチェック項目） | 同 p.14 | 注釈の部分について、この項目の確認材料になる | [確認・PDF] |
| "Review the full MCP code if available, and compare tool names to descriptions and code to identify any suspicious mismatches." | 第三者 MCP サーバの手引き p.7 | 導入前の審査に使える | [確認・PDF] |
| "No testing or contract verification exists that asserts semantic invariants (e.g., archive must not map to DELETE)."（脆弱な状態のチェック項目） | Top 10 MCP03 | 「readOnly なら書かない」という意味の不変条件をコードで確かめる、契約の検証にあたる | [確認] |
| "Encode semantic invariants as policy checks (e.g., using OPA/Rego): archive actions cannot map to HTTP DELETE unless explicitly approved." | Top 10 MCP03 | 同上（OWASP は CI と実行時の PDP で、AuthGap は静的） | [確認] |

### 3.4 既存の対策では捕まらないこと（限界の議論と補完）

- "This detects metadata changes, not changes to server code or behavior behind an unchanged definition; tool annotations are hints, not
  enforcement." — MCP Security Cheat Sheet §2 [確認]
- "Pinning does not stop a payload shipped in the pinned version or tool-description poisoning that leaves the version unchanged." — LLM Top 10
  2026、LLM01、p.15 [確認・PDF]
- "a matching fingerprint shows only that the *declared interface* is unchanged, not that backend behavior is" — 推奨管理策 Client-Side Tool
  Risk Gating [確認]

### 3.5 注釈を使う推奨管理策（これ自体が AuthGap の動機になる）

推奨管理策「Client-Side Tool Risk Gating」は、外部のツールの危険度を注釈から付ける [確認]。

- "External tools** score from what the upstream declares: MCP tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)"
- "The model never sees a tool above the ceiling, which turns the risk level from advice into an access-control decision."
- 限界として自分で書いている: "upstream annotations are not covered on the live path, so an annotation-only redefinition is a stated blind spot."
- 欠けた宣言には強い（"missing or vague metadata raises the score rather than lowering it"）が、**偽の宣言（readOnlyHint: true と言いながら
  書く）には弱い**。付録 G のカードも、参照実装で readOnlyHint: true を宣言すると点数が下がると読んでいる（C10-14）。

### 3.6 害の分類と用語

- 「権限の内側での誤用」: ASI02 は "the agent operates within its authorized privileges but applies a legitimate tool in an unsafe or unintended
  way" と定義する [agent]。注釈の誤りによる被害（新しい権限を得るのではなく、確認が省かれた既存のツールを使わせる）はこれに当たる。
  権限の昇格（ASI03）ではない。
- 読むためのツールが書き込みもできる例: LLM Top 10 2026 の LLM03 と 2025 年版の LLM06 に、SELECT 以外の権限も持つ ID で DB に
  つなぐ「読むための拡張」の例がある [agent]。OWASP の論点は DB の権限の付けすぎで、宣言の誤りではない。
- D4（idempotentHint）に対応する文: "Make high-impact actions idempotent where possible and require explicit duplicate confirmation when
  idempotency is not possible." — AI Agent Security Cheat Sheet [agent]

## 4. 使うときの注意（[判断]）

1. **Top 10 は beta（v0.1）**。項目の名前や番号が変わりうる（MCP06 は既に 2 つの名前がある）。論文では URL・commit・取得日を添え、
   「beta 版の項目」と書く。
2. **OWASP の多くの文は説明文（description）や攻撃者による改ざんを想定している。** AuthGap が見るのは構造化された宣言（注釈）で、
   改ざんが無くても最初から食い違っている場合。この違いを毎回書く。OWASP が注釈について言った、と書かない。
3. **「注釈を見て確認を省く」と OWASP 自身が書いた文は無い**（推奨管理策の危険度の点数を除く）。①の直接の根拠は、MCP の公式ブログ
   （2026-03-16、"A tool marked readOnlyHint: true from a trusted server might be auto-approved"）と、`docs/annotations_security_decisions.md`
   の製品の調査。OWASP の文は「自動承認の運用がある」「確認は操作の性質で決めよ」という一般論として使う。
4. 深刻度の付け方: ASI02 は OWASP AIVSS の "Agentic AI Tool Misuse" に対応すると書いている [agent]。開示のときの分類に使えるかもしれないが、
   AIVSS の本文と採点の方法は読んでいない（不明）。
5. 関連ツール: OWASP の文書は MCP-Scan・Semgrep MCP Scanner などを挙げる。どれも説明文の汚染・依存関係・資格情報を見るもので、注釈と
   コードの照合には触れていない、と OWASP の説明からは読める [agent]。各ツールが本当に照合しないかは、原典で確かめてから書く。
