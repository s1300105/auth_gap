# 追跡調査: bex.co の「508 servers / 612 privilege annotation mismatches」の出典と mcpscan-cli MCP013、道中で見つけた reachscan など

調査日 2026-10-12。検証の水準は次の 3 つで書く。◎ = 一次資料またはコードを自分で読んだ。○ = 要旨、README、公式ページを読んだ。△ = 二次資料（出典を示さずに引用しているブログなど）、または検索ツールの要約だけで本文を見ていないもの。数値はすべて**著者の主張**で、こちらでは検証していない。
WebFetch は本文を小さなモデルに抜き出させて返す仕組みなので、「」の引用もその抜き出しを経ている。論文やコメントに一字一句そのまま引くときは、原文で照合し直すこと。

---

## Lead 1: bex.co の「508 servers の調査で 612 件の privilege annotation mismatch」の出典は何か

### Takeaway
bex.co の記事（Dora Noda、2026-09-24）は確かに "A 2026 survey of 508 MCP servers surfaced 8,286 findings, including 612 "privilege annotation mismatches"" と書いている。ただし出典のリンクは無い。**元の調査は見つからなかった。** 状況証拠が最も多く重なるのは MCPSafe（mcpsafe.io、Truong Bui）である。MCPSafe 側が「508 servers」の数を出しており、`readOnlyHint` の誤ラベルを「組み合わせると書き込みに至る」という形で扱い、注釈の矛盾を検査する規則 MCP-200 も持っている。それでも「612」「8,286」「privilege annotation mismatch」の 3 つは MCPSafe のどのページにも見つからなかった。**AuthGap の関連研究には出典不明の数値として扱い、引用しないのが妥当である。**

### Cited Findings
**bex.co の記事そのもの（◎。本文は WebFetch で 2 回取った）**
- 著者は Dora Noda、日付は 2026-09-24、題は "Your MCP Deploy Tool's dry_run Flag Is a Suggestion, Not a Lock" — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- 該当の文: "A 2026 survey of 508 MCP servers surfaced 8,286 findings, including 612 "privilege annotation mismatches""。"Mislabeled tools are already endemic." で始まる段落にある — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- 同じ段落の次の文: "Every one of those 612 findings is a tool whose author presumably believed the annotation was doing something." — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- 運用者向けの節: "the survey averages more than one mismatch per server"。612 / 508 ≈ 1.20 なので、この記述とは整合する — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- 記事による「privilege annotation mismatch」の説明は、`readOnlyHint: true` と表示されたツールのうち、chain されると副作用を起こしうるもの。これは WebFetch の要約による言い換えで、原文の一字一句ではない — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- **調査には引用もリンクも付いていない。** 本文のリンクは `https://bex.co/glossary/mcp` と `https://github.com/bex-co/bex` の 2 つだけ。調査の名前や組織も書かれていない — [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)

**候補 1: MCPSafe（mcpsafe.io、Truong Bui）。最も近いが確定できない**
- Truong Bui が別の記事のコメント欄（2026-05-25 頃）で "the numbers from 508 servers paint a pretty clear picture of what's out there" と書き、"22% had hardcoded credentials"、"18% had tool descriptions written to influence agent behavior"、"14% had SSRF vectors" を挙げている。スキャンは MCPSafe（mcpsafe.io）で回したとしている。注釈や 612、8,286 には触れていない（○。コメントを WebFetch で読んだ）— [dev.to safemcp のコメント欄](https://dev.to/safemcp/how-i-built-a-directory-of-28577-mcp-servers-32m8)
- MCPSafe の「50+ servers」記事（Truong Bui、2026-05-13 頃）の D006 は "ReadOnlyHint mislabeling in dynamic toolset mode" である。"We found GitHub's official `github/github-mcp-server` sets `readOnlyHint: true` on several tools that, … can be combined to achieve write operations." と書き、さらに "creating a silent privilege escalation path." と続けている。ここで使われているのは**コードとの照合ではなく、ツールの組み合わせについての推論**である（○）— [dev.to](https://dev.to/truong_bui_eaec3f963bbe21/we-scanned-50-mcp-servers-and-found-high-severity-bugs-in-atlassian-github-cloudflare-and-3a42)
- MCPSafe の規則 MCP-200 は "Destructive Tool Annotation Mismatch"（HIGH、CWE-506）。検査は 2 つある。(1) 破壊的な名前（`/^(delete|remove|wipe|drop|purge|erase|wire_transfer|truncate)_/i`）を持つのに `destructiveHint: true` を付けていないもの。(2) `readOnlyHint: true` なのに、handler に `fs.unlink`、`os.remove`、SQL の `DELETE`/`DROP`/`TRUNCATE`、`method: DELETE` などの sink があるもの。範囲は "cross-statement taint analysis within the same file" で handler closure を見るとしている。頻度の数値は書かれていない（○）— [mcpsafe.io/threats/MCP-200](https://mcpsafe.io/threats/MCP-200)
- MCPSafe の手法ページによると、fast scan は静的解析、manifest、CVE の照合。deep scan はこれに taint-flow と "Five independent models from four different vendors vote on each tool handler" を加える。"A rule finding alone will flag a server; model votes adjust the score, not the verdict"。人手の確認は "Every new rule goes through a precision review" とあるだけで、実施者は書かれていない。508、8,286、"privilege annotation mismatch" はこのページに無い（○）— [mcpsafe.io/methodology](https://mcpsafe.io/methodology)
- MCPSafe の "State of MCP Security" は live のダッシュボードで、取得時点の表示は「7 packages / 49 findings」だった。508、612、8,286 は無い（○）— [mcpsafe.io/state-of-mcp-security](https://mcpsafe.io/state-of-mcp-security)
- MCPSafe の前の報告は "Across 448 packages, our scanners identified 5,210 distinct vulnerabilities"（約 11.6 件/package）。手法は静的解析と 5 LLM の合議。人手の検証は記述されていない。注釈、`readOnlyHint`、mismatch の語は出てこない（○）— [dev.to "We Scanned 448 MCP Servers"](https://dev.to/truong_bui_eaec3f963bbe21/we-scanned-448-mcp-servers-heres-what-we-found-28l1)

**候補ではなかったもの（数値が近いだけ）**
- AgentSeal（2026-03-14）は 1,808 servers で "8,282 total findings" を出している。8,286 ではない。"annotation"、"readOnlyHint"、"mismatch" は出てこない。手法は tools/list の列挙と記述の解析（regex、埋め込み、Claude Opus の分類）で、ソースコードは読んでいない（○）— [agentseal.org](https://agentseal.org/blog/mcp-server-security-findings)
- 検索要約によると、"518 officially registered MCP servers" と 38〜41% の無認証率を出す記事群がある。508 ではない（△）— [WebSearch の結果群、例: bonfy.ai](https://blog.bonfy.ai/mcp-security-statistics-2026-what-the-vulnerability-data-reveals-about-ai-agent-risk)
- ベンダーのドメインに絞った検索では、508 も 612 も出てこなかった。対象は astrix、backslash、pillar、noma、invariantlabs、snyk、trailofbits、equixly、knostic、docker、gitguardian、wiz、unit42。Wiz は「spec は annotations を untrusted と扱えと言っている」と書くだけで、測定はしていない（△。検索の要約）— [wiz.io briefing](https://www.wiz.io/blog/mcp-security-research-briefing)

### Inferences
- **出典を確定できない。** 508 という数、`readOnlyHint` を「組み合わせると書き込みになる」と見る枠組み、"privilege escalation" という言い回し、注釈の矛盾を検査する規則。この 4 つが MCPSafe と bex の記述の両方にそろうので、元は MCPSafe の 508 servers の batch である可能性が最も高い。ただしこれは推論である。8,286 / 508 ≈ 16.3 件/server で、MCPSafe の 448 packages の run（11.6 件/package）より多いが、batch が違えば矛盾はしない。かといって裏づけにもならない。
- bex.co は MCP の記事を数日おきに大量に出しており（2026-09-20、21、23、24 は 2 本、25 と続く）、この記事には出典が付いていない。**数値を AuthGap の論文で引くと、未検証の統計の孫引きになる**（CLAUDE.md の規則 1 に反する）。引くなら「出典不明」と明記するか、引かないこと。
- 元が MCPSafe だった場合の A1〜A8 は次のとおり。推論で、各項目の出所は上の Cited Findings。

| 項目 | 内容 |
|---|---|
| A1 宣言側 | 構造化注釈（`readOnlyHint` / `destructiveHint`）と、名前の regex |
| A2 効果側 | 静的な sink の照合と taint（同じファイル内）。deep scan では LLM 5 体の投票 |
| A3 呼び先 | 「同じファイル内の cross-statement taint」とだけ書かれている。ファイルをまたぐか、深さはいくつかは不明 |
| A4 Python | `@mcp.tool(...)` の記述はあるが、対応言語は明記されていない |
| A5 未解決 | 記述なし |
| A6 母集団と正解 | 508 servers の選び方は不明。人手の正解は記述なし。612 / 8,286 の内訳も不明 |
| A7 決定的か | LLM の投票が入る deep scan は非決定的でありうる |
| A8 事前登録・凍結 | 記述なし |

- 判定: **調査（612 / 508）は「判定不能（出典不明）」。** MCPSafe の MCP-200 規則として見るなら「部分的に重なる」。注釈と handler 内の sink を照合する点は同じだが、同じファイル内しか見ず、母集団での測定の設計と opaque の扱いが無い。

### Gaps
- **元の調査は見つからなかった**（存在しないとは言えない）。試したものを下に全部挙げる。
- WebSearch（extended はとくに注記しない）:
  1. `bex.co MCP 508 servers 612 annotation mismatches`
  2. `"508" MCP servers annotation mismatches survey`
  3. `"8,286 findings" MCP servers`
  4. `"privilege annotation" mismatch MCP readOnlyHint survey 2026`
  5. `"508 MCP servers"`
  6. `MCPSafe mcpsafe.io scanned 508 servers findings`
  7. `"612" "annotation" MCP servers mismatches readOnlyHint`
  8. `"MCP's First Year" 30 CVEs 500 server scans`
  9. `MCPSafe "State of MCP Security" report annotation mismatch`（standard）
  10. `"8286" OR "8,286" MCP security findings 508 servers report 2026`
  11. `MCP server scan "annotation mismatches" readOnlyHint side effects findings servers`
  12. `Truong Bui MCPSafe 508 servers readOnlyHint privilege annotation mismatches`
  13. `MCP servers survey readOnlyHint annotation mismatch 508 612`（allowed_domains は astrix.security、backslash.security、pillar.security、noma.security、invariantlabs.ai、snyk.io、trailofbits.com、blog.trailofbits.com、equixly.com、knostic.ai、docker.com、gitguardian.com、blog.gitguardian.com、wiz.io、unit42.paloaltonetworks.com）
- arXiv API（https://export.arxiv.org/api/query。検索対象はタイトルと要旨のメタデータだけ）: `all:"508 MCP servers"` 0 件、`all:"508" AND all:MCP AND all:servers` 0 件、`all:"tool annotations" AND all:MCP` 0 件、`all:"privilege annotation"` 0 件、`all:destructiveHint` 0 件、`all:"annotation mismatch" AND all:MCP` 0 件、`all:readOnlyHint` 1 件（2606.06387 WebMCP Tool Surface Poisoning。照合研究ではない）。最初は http で問い合わせて 0 件が返ったが、これは無効なので https で取り直した。
- WebFetch: bex.co の記事（2 回）、dev.to safemcp、dev.to の 448 の記事、dev.to の 50+ の記事、mcpsafe.io/methodology、mcpsafe.io/state-of-mcp-security、mcpsafe.io/threats/MCP-200、agentseal.org/blog/mcp-server-security-findings、cisoexpert.com（下の節）。**Medium "MCP's First Year: What 30 CVEs and 500 Server Scans Tell Us…"（https://medium.com/ai-security-hub/mcps-first-year-what-30-cves-and-500-server-scans-tell-us-about-ai-s-fastest-growing-attack-6d183fc9497f）は HTTP 403 で読めなかった。** 題が「500 server scans」で、時期も近いので、未確認の候補として残す。
- 検索の要約に "We've scanned 508 public MCP servers through MCPSafe (mcpsafe.io) — a pre-install scanner that runs static analysis … 23% had at least one critical finding." という文が出たが、**その文の URL は特定できなかった**（△。出所不明のまま）。
- ベンダーごとに個別のサイト内検索はしていない。上の 13 で 15 ドメインをまとめて絞っただけである。Pillar、Noma、Astrix、Unit 42 の個別の報告書（PDF）までは見ていない。
- 確定させる次の一手（未実施）: bex.co の著者に出典を問い合わせる。MCPSafe の公開ページ（ブログ、Twitter/X、LinkedIn）で "612" と "privilege" を探す。上の Medium の記事を別の経路（archive.org など）で読む。

---

## Lead 2: mcpscan-cli（glatinone/mcpscan）の MCP013「Misleading tool annotation」は何をしているか

### Takeaway
MCP013 は **regex による行の窓の照合**である。tool 定義の行から、次の tool 定義まで、または 40 行の上限までの生テキストを 1 つの「ブロック」とする。その中に 4 つの hint のキーがあるか、`readOnlyHint=True` または `destructiveHint=False` があるかを見て、exec / filesystem-write / network / SQL の regex と照合する。**呼び先は辿らない**（深さ 0。ファイルもまたがない）。未解決という概念は無く、helper の中の効果は黙って見落とされる。評価、論文、データセット、測定した不一致率はどれも無い。2026-07-14（v0.9.0）に追加され、それ以降このファイルは一度も変わっていない。判定は「部分的に重なる」。

### Cited Findings
**リポジトリと日付（◎。`git clone --no-checkout` で取り、`git log` と `git show` だけで読んだ。コードは実行していない）**
- 最初のコミットは `71c0903f120d54a27e0b8690e15a20882bcd479c`（2026-06-30、"Scaffold mcpscan: pyproject, README, LICENSE, package skeleton"）。HEAD は `86a3a072db925d2a0760709774f00ef9ccfdf1dc`（2026-09-27）。コミットは 72 で、glatinone が 70、Kiell Tampubolon が 2（runtime guard と MCP023。MCP013 には関わっていない） — [GitHub glatinone/mcpscan](https://github.com/glatinone/mcpscan)
- MCP013 を入れたコミットは `7c7fcbbbf7b60deeb15b9b80b733c1913e32e738`（2026-07-14 09:57 +0800、"feat: add MCP013, tool risk annotation missing or contradicted (v0.9.0)"。タグ v0.9.0 と同じコミット）。`mcpscan/rules/tool_annotations.py` を触ったコミットはこの 1 つだけで、`git diff 7c7fcbb HEAD -- mcpscan/rules/tool_annotations.py` は空である — [commit 7c7fcbb](https://github.com/glatinone/mcpscan/commit/7c7fcbbbf7b60deeb15b9b80b733c1913e32e738)
- PyPI の最初の公開は v0.19.0（`cbe03f17…`、2026-08-10、"Bump version to 0.19.0 for first PyPI release"）。そのあと v0.19.1 で package 名を `mcpscan-cli` に変えた（`bc34325…`、2026-08-10）。最新のタグは v0.20.0（`2149504b…`、2026-08-17）。`pyproject.toml` は `version = "0.20.0"`、`dependencies = []  # zero runtime dependencies — stdlib only`、`requires-python = ">=3.9"` — [pyproject.toml @86a3a07](https://github.com/glatinone/mcpscan/blob/86a3a072db925d2a0760709774f00ef9ccfdf1dc/pyproject.toml)

**規則の本体（◎。`mcpscan/rules/tool_annotations.py` @ `86a3a072db925d2a0760709774f00ef9ccfdf1dc`。`7c7fcbb` と同じ内容）**
- 方式を宣言した docstring（L22-30）: "Tool boundaries are approximated, not AST-derived (mcpscan is a zero-dependency, regex-based scanner): a "tool definition" is a Python `@x.tool(...)` decorator, a raw `mcp.types.Tool(name=...)` construction, or a JS/TS `registerTool(...)` / `.tool("name", ...)` call. Everything from that line up to the next tool definition (or a line cap, …) is the "block" searched for annotations and capabilities. This misses tools defined with unusual patterns … — false negatives, not false positives" — [L22-30](https://github.com/glatinone/mcpscan/blob/7c7fcbbbf7b60deeb15b9b80b733c1913e32e738/mcpscan/rules/tool_annotations.py#L22-L30)
- tool の開始の regex（L45-50）:
  ```python
  TOOL_DEF = re.compile(
      r"@\w[\w.]*\.tool\s*\("
      r"|\bTool\s*\(\s*name\s*="
      r"|\bregisterTool\s*\("
      r"|\.tool\s*\(\s*['\"]"
  )
  ```
- 宣言側（L53、L56-59）。安全だという主張として見るのは `readOnlyHint` true と `destructiveHint` false の 2 つだけで、`openWorldHint` と `idempotentHint` は「キーがあるか」の判定にしか使わない:
  ```python
  ANNOTATION_KEY = re.compile(r"\b(readOnlyHint|destructiveHint|idempotentHint|openWorldHint)\b")
  SAFE_CLAIM = re.compile(
      r"readOnlyHint['\"]?\s*[:=]\s*(?:True|true)"
      r"|destructiveHint['\"]?\s*[:=]\s*(?:False|false)"
  )
  ```
- 効果側（L64-95）は 4 種類の regex で、IGNORECASE を付けている。exec は `os.system|popen`、`subprocess.\w+`、`child_process`、`(execSync|spawnSync|spawn|exec)\s*\(`、`eval(`、`Function(`。filesystem-write は `open(…'w'|'a')`、`fs.writeFile|unlink|rm|appendFile`、`os.remove|unlink|rmdir`、`shutil.rmtree|move`。network は `requests.(get|post|put|delete|patch)(`、`urllib.request`、`http.client`、`fetch(`、`axios.*(`、`net.connect`、`socket.*(`。sql は次のとおり:
  ```python
  "sql": re.compile(
      r"\bcursor\.execute\s*\("
      r"|\.execute\s*\([^)]*(?:select|insert|update|delete)\b"
      r"|\bsqlite3\.connect\s*\(",
      re.IGNORECASE,
  ),
  ```
  — [L64-95](https://github.com/glatinone/mcpscan/blob/7c7fcbbbf7b60deeb15b9b80b733c1913e32e738/mcpscan/rules/tool_annotations.py#L64-L95)
- 窓と言語（L97-98）: `MAX_BLOCK_LINES = 40` と `SOURCE_EXTS = {".py", ".js", ".ts", ".mjs", ".cjs", ".tsx", ".jsx"}`
- 判定（L113-125）。ブロックの生テキストに対して `search` するだけである:
  ```python
  def_idxs = [i for i, line in enumerate(lines) if TOOL_DEF.search(line)]
  for pos, idx in enumerate(def_idxs):
      end = def_idxs[pos + 1] if pos + 1 < len(def_idxs) else len(lines)
      end = min(end, idx + MAX_BLOCK_LINES)
      block = "\n".join(lines[idx:end])
      caps = [name for name, pattern in CAPABILITIES.items() if pattern.search(block)]
      ...
      if SAFE_CLAIM.search(block):   # → HIGH "Tool annotation contradicts detected … capability"
      elif not ANNOTATION_KEY.search(block):   # → MEDIUM "… has no risk annotations"
  ```
  — [L108-148](https://github.com/glatinone/mcpscan/blob/7c7fcbbbf7b60deeb15b9b80b733c1913e32e738/mcpscan/rules/tool_annotations.py#L108-L148)

**評価と文書（◎。`CHANGELOG.md`、`README.md`、`tests/` @ HEAD）**
- CHANGELOG [0.9.0] - 2026-07-14: "Tool boundaries are a line-window heuristic … not AST-derived — mcpscan stays zero-dependency and regex-based, so this trades recall on unusual registration patterns for zero new false-positive surface." と "7 new tests (`TestToolAnnotationsRule`); 68 tests passing (was 61). Dogfood self-scan clean." — [CHANGELOG.md](https://github.com/glatinone/mcpscan/blob/86a3a072db925d2a0760709774f00ef9ccfdf1dc/CHANGELOG.md)
- 試験は、単体テスト 7 件（`tests/test_scanner.py` の `TestToolAnnotationsRule`、L190 以降）と fixture 2 つ（`tests/fixtures/vulnerable/server.py` の `delete_all` = 注釈なしの `shutil.rmtree`、`safe_looking_cleanup` = `readOnlyHint: True` の `os.remove`。`tests/fixtures/clean/server.py` の `destructiveHint: True`）だけである。README、CHANGELOG、`LINKEDIN_ANNOUNCEMENT.md` に `benchmark|evaluat|precision|recall|paper|arxiv|dataset` を grep したが、MCP013 の評価を指す記述は無かった — [tests/fixtures/vulnerable/server.py](https://github.com/glatinone/mcpscan/blob/86a3a072db925d2a0760709774f00ef9ccfdf1dc/tests/fixtures/vulnerable/server.py)
- README の規則表: "**MCP013** | 🏷️ Misleading tool annotation | Medium–High | MCP03:2025 | A tool with a detected exec/filesystem-write/network/SQL capability that declares no `readOnlyHint`/… at all, or claims `readOnlyHint: true`/`destructiveHint: false` while its own code calls that capability" — [README.md](https://github.com/glatinone/mcpscan/blob/86a3a072db925d2a0760709774f00ef9ccfdf1dc/README.md)
- 関連する修正: 2026-09-16 のコミット `4795a39` "fix(MCP001): stop flagging RegExp.exec() as command injection" が直したのは MCP001 だけで、MCP013 の exec の regex `\b(?:execSync|spawnSync|spawn|exec)\s*\(` はそのまま残っている — [commit 4795a39](https://github.com/glatinone/mcpscan/commit/4795a39572ee65070ed0c4a873bc8477fd2da17e)

### Inferences
- A1〜A8 は次のとおり。

| 項目 | 内容 |
|---|---|
| A1 宣言側 | 構造化注釈（`readOnlyHint` / `destructiveHint` の値、4 キーがあるかどうか）。値は regex で取るので、`annotations=READ_ONLY` のように別の場所の定数を参照していると取れない |
| A2 効果側 | 生テキストに対する regex（AST ではない）。窓は tool の行から次の tool 定義まで、最大 40 行 |
| A3 呼び先 | 辿らない。深さ 0 で、ファイルもまたがない |
| A4 Python | 対応する（`.py`）。JS/TS も同じ regex で見る |
| A5 未解決 | 概念が無い。helper の中の効果は黙って不検出になる。AuthGap の用語では false-clean で、率も出さない |
| A6 母集団・正解・率 | どれも無い。単体テスト 7 件と fixture だけ |
| A7 決定的か | 決定的（stdlib の regex だけ） |
| A8 事前登録・凍結 | 無い |

- **判定: 「部分的に重なる」。** 「構造化注釈とコードの能力の矛盾」という問いは同じである。違いは 3 点ある。(a) 呼び先を辿らず、行の窓の regex で見る。(b) opaque も率も無い。(c) 母集団での測定も人手の正解も無い。
- コードから推論される誤りの方向（推論で、実行しての確認はしていない）。
  - 誤検出の方向（spec の意味とのずれ）: network の regex は `requests.get(` を含み、それだけで `readOnlyHint: true` と矛盾すると判定する。spec の readOnly は「環境を変えない」の意味なので、GET だけを行う読み取りのツールが HIGH として出る。SQL も `sqlite3.connect(` や、動詞を見ない `cursor.execute(` で当たるので、SELECT だけのツールが矛盾として出る。
  - 誤検出の方向（窓の取り方）: 窓が次の tool 定義まで最大 40 行伸びるので、tool の直後に定義された無関係な関数やコメント、文字列の中の `open(…'w')` などが、その tool の能力として数えられる。JS の `regex.exec(` も exec として当たる（MCP001 だけ直してある）。
  - 見逃しの方向（false-clean）: helper 関数や別ファイルに書かれた効果、`Path.write_text`、`os.rename`、`httpx`、`aiohttp` は regex に無いので見えない。注釈を変数経由で渡すと「注釈なし」（MEDIUM）として報告され、矛盾（HIGH）としては出ない。
- 前の調査（06_japanese_and_2026_venues.md）では「README を読んだ、○」だったものを、今回コードを読んで ◎ に上げた。06 の Gaps にある「同じ関数内だけか、呼び先を辿るか、どの言語か」には、上の答えで足りる。

### Gaps
- MCP013 の誤検知率と見逃し率は、作者が測っていないので無い。こちらでも実行していない（データを信用しない方針に従い、コードは実行しない）。
- PyPI に公開された wheel の中身が git の HEAD と同じかは照合していない。
- GitHub Releases ページの日付は見ていない（GitHub MCP を使わない制約がある）。日付はタグが指すコミットの日付で代えた。

---

## 道中で見つけた他のツール・研究（除外リスト外）。注釈とコードを照合するもの、またはそれに近いもの

### Takeaway
**最重要は reachscan（vinmay/reachscan）である。** Python の MCP ツールについて、明示された ToolAnnotations（`readOnlyHint` / `openWorldHint` / `destructiveHint`）を、プロジェクト内の AST コールグラフ（ファイルをまたぎ、最大 8 hop）で到達できる効果と照合する。解決できなかったメソッド呼び出しの先は `unknown` として分けて扱う。`ANNOTATION_MISMATCH` が入ったのは 2026-10-05（v0.3.0）で、**今日の 1 週間前**である。AuthGap とは「大きく重なる」。母集団での測定の設計、注釈ごとの opaque の率、事前登録、人手の正解は持っていない。そのほかに見つかったのは、注釈の有無だけを数えた小さな scan と、事例の報告だけだった。

### Cited Findings
**reachscan（vinmay/reachscan。作者は Vinmay Nair）◎ コードを読んだ（`4f6509d812b3c40769ddce0ea0bee548bfe24e02` = v0.4.0、2026-10-07）**
- 最初のコミットは `fd0563746c34e25b76c289abda5cc11106c17fd8`（2026-02-21）。v0.1.0 は 2026-03-05、v0.2.0 は 2026-10-04、v0.3.0 は 2026-10-05、v0.4.0 は 2026-10-07。注釈の抽出は `784483e` "feat: extract MCP tool annotations from Python sources"（2026-10-04）、照合は `65c8ca6d7c24ee3feb98d2745e2a89acd0fef5de` "feat: ANNOTATION_MISMATCH for Python MCP tools (mcp-risk-mismatch)"（2026-10-05 13:22 -0400）で入った。PR #32 は同じ日に merge された — [PR #32](https://github.com/vinmay/reachscan/pull/32)、[commit 65c8ca6](https://github.com/vinmay/reachscan/commit/65c8ca6d7c24ee3feb98d2745e2a89acd0fef5de)
- 規則（`src/reachscan/analysis/annotation_mismatch.py` L9-16）: `readOnlyHint: true` に到達可能な WRITE / EXECUTE / DYNAMIC があれば high。`openWorldHint: false` に到達可能な外向きの HTTP / websocket / socket の connect があれば矛盾（literal の loopback は除く）。`destructiveHint: false` は、`readOnlyHint` が false のときに限り、到達可能な destructive WRITE（delete、move/rename、truncating write）があれば medium。`idempotentHint` は検査しない。v0.4.0 で openWorldHint の不一致は medium に下げられた（CHANGELOG）— [annotation_mismatch.py @4f6509d](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/analysis/annotation_mismatch.py)
- 明示された hint だけを見て、経路を必須にする（L22-26）: "Only explicit hints are checked. Defaulted hints are the spec's conservative values and claim nothing; unresolvable hints never produce findings. Every mismatch carries the call path from the tool's entry point to the contradicting sink, and a contradiction without such a path is not reported (module-level code, which runs on import, is not a tool call path)." — [L22-26](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/analysis/annotation_mismatch.py#L22-L26)
- 判定の核（L233-245）: `if ro.source == EXPLICIT and ro.value is True and capability in _READ_ONLY_CONTRADICTIONS: yield RULE_READ_ONLY, …`。`_READ_ONLY_CONTRADICTIONS = {"WRITE", "EXECUTE", "DYNAMIC"}`（L67）。EXECUTE は destructiveHint の矛盾には数えない（L18-20: "reachscan can't tell what a command does, and on the phase-3 corpus every EXECUTE hit was a harmless launch (V decision, 2026-10-05)"）— [L227-245](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/analysis/annotation_mismatch.py#L227-L245)
- 深さ（`src/reachscan/reachability.py` L64）: `TRAVERSAL_DEPTH = 8   # max call hops the BFS will follow`。lowlevel の分岐からは `_bfs(candidates[0], graph, TRAVERSAL_DEPTH - 1)` で辿る（annotation_mismatch.py L446）— [reachability.py](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/reachability.py#L64)
- コールグラフ（`src/reachscan/call_graph.py` L44-60）は 4 段で解決する。(1) 同じファイルの関数名、(2) ImportMap、(3) `self.attr()`、(4) import したモジュール名の `obj.attr()`。docstring には "Otherwise: unresolvable → edge dropped silently" とある。既知の限界として "Type-based method dispatch (obj.method() where obj is not self and is not a directly imported module) is not resolved."、"Dynamic calls (getattr, __import__, etc.) produce no edges."、"Star imports … are not resolved." を挙げている。`__init__.py` の再 export は 1 段だけ辿る — [call_graph.py](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/call_graph.py#L44-L60)
- 未解決の扱い（v0.4.0 の T8a。commit `d2b001d` "unresolved Python method calls make their targets unknown, not unreachable"）。README L73: "When reachable code makes such a call and the project defines a method with that name, findings in that method (and in what it calls) are reported as `unknown` rather than `unreachable`. **They can't produce an annotation mismatch and don't affect the exit code.**" CHANGELOG: "On the phase-3 corpus: 110 of 1,257 unreachable Python findings become unknown (7 repos)"。解決できない hint（プロジェクトの外から import したもの、helper で組み立てたもの）は飛ばし、`--explain` に一覧として出す — [README.md @4f6509d](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/README.md)
- lowlevel サーバの扱い: `types.Tool` を `call_tool` の `if name == <literal|同じファイルの定数|enum>` / `match name:` の分岐に結びつける。結びつかないツールは「no per-tool path and so no mismatch finding」。phase-3 corpus では、結びついたツールが 28 → 45、結びつかないものが 29 → 12（v0.3.1）— [CHANGELOG.md](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/CHANGELOG.md)
- 評価（PR #32 の本文。著者の主張。○）: "Phase-3 corpus: 38 repos plus the official git server" で 16 件の不一致が出た（read-only 15、closed-world 1）。15 件は 1 つのサーバ（read-only のツールが、ホストのアプリが動いていなければ起動する）から出たもの。第三者のサーバで "one confirmed true positive"（`openWorldHint: false` のツールがリモート API に POST していた。詳細は非公開）。precision の修正で、closed-world の FP 52 件（loopback の bridge の `connect()`）と destructiveHint の 9 件を除いた — [PR #32](https://github.com/vinmay/reachscan/pull/32)
- 能力検出器の精度（README "Precision"）: 10 の agent リポジトリ（AutoGPT、LangChain、LlamaIndex、CrewAI、OpenAI Agents SDK、Autogen、pydantic-ai、agentops、anthropic-cookbook、python-sdk）の "approximately 3,900 labeled findings" で、全体の FP 率は 0.47%。これは**不一致ではなく、能力の finding の FP 率**である（◎ README）— [README.md](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/README.md)
- AST だけを使い、LLM の呼び出しは無い（src を `openai|anthropic` で grep して、該当するのは framework を認識する文字列だけだった）。SARIF の rule id は `mcp-risk-mismatch` で、SEP-2793（`seps/2793-tool-risk-metadata.md`、walbis/modelcontextprotocol @49f25cf）の declared-vs-inferred の枠組みに従っている。SEP の `riskLevel` / `category` は spec に無いので検査しない（○ PR #32 の本文）— [PR #32](https://github.com/vinmay/reachscan/pull/32)

**MCPSafe MCP-200 "Destructive Tool Annotation Mismatch"（○）**: 内容は Lead 1 に書いた。名前の regex と、`readOnlyHint: true` × handler 内の destructive sink（同じファイル内の taint）を見る — [mcpsafe.io/threats/MCP-200](https://mcpsafe.io/threats/MCP-200)

**cisoexpert.com "MCP Tool Annotations: What My 16-Server Scan Found"（David O'Neil、2026-05-20 公開と書かれているが、scan は 2026-05-21 と書かれていて矛盾がある。○）**: 手で選んだ 16 の公開サーバに接続し、tools/list の定義に 4 つの hint が**あるかどうか**だけを見た。コード、記述、挙動とは照合していない。"The scanner flagged all 16, and one of those results is wrong."。10 回の反復で結果は同じだった。コードもデータも公開していない — [cisoexpert.com](https://cisoexpert.com/articles/mcp-annotation-gap-ecosystem-analysis/)

**事例の報告（△。検索の要約だけで、本文は読んでいない）**
- storytold/printcraft の issue #130 "fix(automation): file-writing tools advertise read-only MCP annotations"。`doc_export_data` など 3 つのツールが `readOnlyHint: true` なのにファイルを書く — [GitHub issue](https://github.com/storytold/printcraft/issues/130)
- mcpbundles.com の手法ページによると、名前、記述、schema、注釈を読み、ツールを実行せず、「read-only と表示された mutating verbs」を指摘する（コードは読まない）— [mcpbundles.com](https://www.mcpbundles.com/learn/mcp-security)

### Inferences
- reachscan の A1〜A8 は次のとおり。

| 項目 | 内容 |
|---|---|
| A1 宣言側 | 構造化注釈（明示されたものだけ。既定値は主張なしとして扱う。解決できない hint は飛ばして一覧に出す） |
| A2 効果側 | AST の能力検出器（WRITE / EXECUTE / DYNAMIC / SEND など） |
| A3 呼び先 | 辿る。プロジェクト内でファイルをまたぎ、BFS で最大 8 hop（AuthGap は 4） |
| A4 Python | 対応する（注釈の照合は Python だけ。TS は予定） |
| A5 未解決 | 未解決のメソッド呼び出しの先は finding ごとに `unknown`。**`unknown` は不一致を作らず、ツールまたは注釈ごとの opaque の率としても出さない。** 結びつかない lowlevel のツールは数（linked / unlinked）だけ報告する |
| A6 母集団・正解・率 | phase-3 corpus は 38 repos と official git server で、リストはリポジトリに無い。不一致は 16 件、確認済みの TP は 1 件（著者の主張）。不一致率や人手の正解の設計は無い |
| A7 決定的か | 決定的（AST だけで LLM を使わない） |
| A8 事前登録・凍結 | 無い。規則は corpus を見ながら調整している（"V decision, 2026-10-05"、precision の修正で FP を除いた） |

- **reachscan の判定: 「大きく重なる」。** Python で注釈と呼び先を辿った効果を照合し、未解決を分けて扱う点まで、AuthGap の核とほぼ同じ検査である。AuthGap に残る差分は 4 つある。(1) 母集団を事前登録して凍結した測定。(2) 注釈ごとの opaque の率の報告（reachscan の unknown は黙って「不一致なし」側に落ちる）。(3) 人手の正解と修正コミットからの再現率。(4) `idempotentHint` と SQL / HTTP メソッドの粒度での矛盾の判定（reachscan は WRITE / SEND の粒度）。**関連研究の節では「同時期の OSS ツール」として必ず挙げ、差分をこの 4 点で書くべきである**（推論）。
- reachscan は corpus を見ながら規則を調整しているので（EXECUTE を destructiveHint から外す、openWorldHint を medium に下げる）、その 16 件は事前に定義した検査の結果ではない。AuthGap の凍結と事前登録は、まさにこの点で差になる（推論）。
- MCPSafe MCP-200 は「部分的に重なる」。注釈と handler 内の sink を照合するが、同じファイル内だけを見る。母集団の数値も手法の詳細も公開されていない。
- cisoexpert の 16-server scan と mcpbundles は「隣接」で、宣言側の有無や名前だけを見ている。printcraft の issue と github-mcp-server の D006 は、AuthGap の野外の正例の候補（事例）になりうる。

### Gaps
- reachscan の phase-3 corpus の 38 repos の一覧、16 件の内訳、"confirmed true positive" の確認手順は公開されていない（PR では非公開としている）。
- reachscan で同じ tool の中に `reachable` の WRITE と `unknown` が混ざったとき、出力にツール単位の注記が付くかどうかは、JSON の schema（`docs/schema_v1.md`）まで読んでいないので未確認。
- SEP-2793（`seps/2793-tool-risk-metadata.md`。walbis/modelcontextprotocol の fork）は読んでいない。declared-vs-inferred の議論に測定のデータがあるかは不明。
- printcraft の issue、mcpbundles、daily.dev の "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do"（https://daily.dev/posts/tool-annotations-as-risk-vocabulary-what-hints-can-and-can-t-do-kc5gza150）は本文を読んでいない。
- arXiv 2606.04769（"Description-Code Inconsistency in Real-world MCP Servers"）は、前の notes（01）で DCIChecker として既知なので、ここでは扱わない。
