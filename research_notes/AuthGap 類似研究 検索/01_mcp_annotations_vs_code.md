# MCP ToolAnnotations（と他プロトコルの構造化された副作用ヒント）をコード・挙動と照合する先行研究（調査日 2026-10-12）

凡例と注意（全節共通）

- 確認の水準。◎ は一次資料の全文を自分で通読した。○ は要旨・README・公式ページを読んだ。全文 HTML を取得してキーワード検索し、該当節だけ読んだものも ○ にとどめた（通読していないので ◎ にはしない）。△ は二次情報（検索スニペット、他論文の関連研究、ブログの又引き）。
- 引用の出所。arXiv の引用は、arXiv HTML 全文を自分で取得・テキスト化した原文からの逐語引用。GitHub・ブログの引用は WebFetch（要約モデルを通す）が返した引用で、**原文と逐語照合していない**。
- 数値はすべて**著者の主張で、こちらでは未検証**（CLAUDE.md 規則 1 に従い `verified_by_me = none` 相当）。
- 軸の略号。A1 宣言側 / A2 実効側 / A3 callee を追うか・深さ / A4 Python 対応 / A5 未解決の扱いと未解決率の報告 / A6 母集団の定義・人手の正解・矛盾率 / A7 決定論で判定に LLM を使わない / A8 事前登録・解析器凍結 / A9 開発者の修正コミットで recall を測る。
- 判定は 「同一」/「大きく重なる」/「部分的に重なる」/「隣接」 の 4 段階。
- 既知リスト（HintLint, mcp-doctor, actlint, Airlock, DCIChecker 等）は調べ直していない。版が変わったもの、背後の論文、構図を変える事実だけを書いた。

---

## Q1. MCP ToolAnnotations の値をサーバーのコードと静的に照合するもの（Python・callee 追跡・母集団での矛盾率・人手の正解）は新たに見つかったか

### Takeaway
**AuthGap と「同一」のものは、2026-09-15〜10-12 の新着にも既知リストの外にも見つからなかった。** ToolAnnotations を Python のコードと照合し、callee を追い、定義した母集団で人手の正解つきの矛盾率を出す研究・ツールは、見た範囲には無い。新しく見つかった近いものは 2 方向に分かれる。(a) 宣言側だけを見るもの。hintgap は存在するかだけを見る。mcpindex と mcp-tool-drift は版の間の変化を見る。(b) 実効側だけを見るもの。MCPacific は入口を抽出する。FCD はソースから効果を要約する。AgentSecGraph は sink と guard を見る。両側を照合するものは、既知の HintLint と mcp-doctor が今も最も近い。

### Cited Findings

#### 新規 1: hintgap（jay-tank/hintgap）— ○（README、WebFetch 経由）
- 内容。Python の stdlib `ast` だけで書かれた静的スキャナ。FastMCP の `@mcp.tool` と、低水準の `types.Tool(...)`（`@app.call_tool` のディスパッチャの隣）を読む。annotation の**有無**と、名前の動詞による規則（create/update/delete/send/pay なのに `destructiveHint=True` も `readOnlyHint=False` も無い）を検査する — [hintgap README](https://github.com/jay-tank/hintgap)
- 値が正しいかは見ないと README 自身が書いている。「never whether the values are _correct_」「hintgap can't know your implementation, and by design never runs it」。`readOnlyHint=True` なのに実際は書き込むツールは「will pass」 — [hintgap README](https://github.com/jay-tank/hintgap)
- 評価の数値は無い（走査したサーバー数・精度・人手検証のどれも無い）。日付は見えなかった。コミットは 8、star は 0 — [hintgap README](https://github.com/jay-tank/hintgap)
- 軸。A1 構造化 annotation（有無だけ）/ A2 なし（効果の推定をしない）/ A3 なし / A4 Python / A5 記載なし / A6 なし / A7 LLM なし（決定論とは明記していない）/ A8 なし / A9 なし。
- **判定: 隣接。** 入口の認識（FastMCP デコレータ、低水準の `Tool`、stdlib `ast` だけを使う）は AuthGap と同じ発想だが、実効側 M を持たない。名前が「AuthGap」に似ているので、引用するときに取り違えないこと。

#### 新規 2: MCPacific（arXiv 2610.05319、v1 2026-10-04 / v2 2026-10-08）— ○（全文 HTML をキーワード検索）
- 17 のマーケットプレイスにある 124,267 サーバーから、7 言語で 1,328,233 個のツール仕様を静的に抽出した。全文中の `readOnlyHint` / `destructiveHint` / `ToolAnnotations` はどれも 0 件 — [arXiv 2610.05319](https://arxiv.org/abs/2610.05319)
- 入口の規則。原文 "This analysis yields 56 patterns spanning decorators and annotations, explicit registration calls, tool objects and builders, wrappers and factories, and low-level protocol handlers." / "For low-level protocol implementations, the analyzers link tool declarations to invocation-dispatch logic and follow branches selected by tool name to locate the corresponding entry functions." 抽出するのは `server_name, tool_name, description, signature, return` の 5 項目だけ — [arXiv 2610.05319 HTML](https://arxiv.org/html/2610.05319v2)
- Python は 47,939 サーバー・553,615 ツール。各ツールに Semgrep の警告を対応づけている（入力検証が 89.22%）— [arXiv 2610.05319 HTML](https://arxiv.org/html/2610.05319v2)
- 軸。A1 なし / A2 静的（入口の特定だけで、効果は推定しない）/ A3 入口の関数まで（低水準ハンドラはツール名による分岐を追う）/ A4 Python を含む 7 言語 / A5 記載を確認できず / A6 母集団は大きいが矛盾の概念が無い / A7 抽出は静的、分類は LLM / A8 なし / A9 なし。
- **判定: 隣接。** AuthGap の 14 の入口規則（低水準 `serve()` の中のハンドラを含む）にとって、比較すべき先行例になる（56 パターン・7 言語）。照合はしていない。

#### 新規 3: FCD — Formation-Consistent Dispatch（arXiv 2609.35088、2026-09-28）— ○（全文 HTML をキーワード検索）
- 公式ソースから「宣言された範囲内の効果」を**過大近似**で要約し、実行時のディスパッチで照合する。原文 "Reviewed profiles produce provenance-bound over-approximations of declared in-scope effects from official source." — [arXiv 2609.35088](https://arxiv.org/abs/2609.35088)
- callee の扱い。原文 "The call-site guard extracts callee identities from each declared handler region. It rejects identities outside the profile's reviewed inventory … Each rule produces an effect record, handler rejection, or UNKNOWN." — [arXiv 2609.35088 HTML](https://arxiv.org/html/2609.35088)
- 評価。原文 "Four profiles covered 32 official releases … A frozen 16-release expansion matched a separate source oracle. In a preregistered stock comparison, FCD completed all three pending calls …" 全文中の annotation / Hint はどちらも 0 件 — [arXiv 2609.35088 HTML](https://arxiv.org/html/2609.35088)
- 軸。A1 なし（宣言側は呼び出しのセキュリティ契約で、ToolAnnotations ではない）/ A2 静的（人がレビューした profile が規則を持つ）/ A3 handler の範囲にある callee の同一性を見る（深さの記載は見つけられず）/ A4 Python の記述が 10 か所 / A5 **UNKNOWN と reject を明示する** / A6 4 profile・32 リリース。人の目を通した profile が前提 / A7 LLM は使っていないように見える（未確認）/ A8 **preregistered・frozen と明記** / A9 なし（リリース間の変化は見る）。
- **判定: 隣接（方法論は部分的に重なる）。** ソースから効果を要約する、UNKNOWN を残す、事前登録と凍結、という手続きは AuthGap に近い。ただし annotation と照合しない。目的は実行時の権限で、測定ではない。

#### 新規 4: AgentSecGraph（arXiv 2610.03014、2026-10-02）— ○（全文 HTML をキーワード検索）
- エージェントの repo 67 本（11 エコシステム、37,542 ファイル）にある security-sensitive な操作 23,866 件について、source → operation の依存、guard の証拠、外部効果の意味を静的に集める — [arXiv 2610.03014](https://arxiv.org/abs/2610.03014)
- 限界の自己申告。原文 "Python analysis is not a complete whole-program interprocedural, alias, points-to, or symbolic analysis … Reflection, dynamic registration, metaprogramming, and deployment-dependent exposure or privilege may therefore produce incomplete evidence." repo は記録した Git commit で凍結し、LLM 5 体の panel は「pre-annotation and disagreement-based triage」だけに使う — [arXiv 2610.03014 HTML](https://arxiv.org/html/2610.03014)
- 軸。A1 なし / A2 静的 / A3 局所（完全な手続き間解析ではない）/ A4 Python と TS/JS / A5 不完全さを明記するが、未解決率の数値は確認できず / A6 参照集合は 13 repo・22 挙動 / A7 構築は決定論、トリアージに LLM / A8 commit で凍結 / A9 なし。
- **判定: 隣接。** sink に guard の証拠を足す設計と凍結の手続きは近いが、宣言側との照合が無い。

#### 新規 5: 「Do Skill Descriptions Tell the Truth?」（arXiv 2605.12875、2026-05-13。ツール名も **SkillScope**）— ○（全文 HTML をキーワード検索）
- 原文 "We study this description–implementation inconsistency by asking whether the implementation stays within the security-relevant scope declared in the description … SkillScope … constructs source-level security property graphs (SPGs) from implementations and performs LLM-assisted consistency checking." / "On 4,556 programmatic skills with double-blind human review, SkillScope achieves a precision of 84.8% and a recall of 96.5% … Confirmed inconsistency affects 9.4% of skills" — [arXiv 2605.12875](https://arxiv.org/abs/2605.12875)
- 全文中の call graph / interprocedural / callee はどれも 0 件 — [arXiv 2605.12875 HTML](https://arxiv.org/html/2605.12875)
- 軸。A1 自然言語の記述（SKILL.md）/ A2 静的（SPG）と LLM / A3 記述を見つけられず / A4 Python の言及は 2 件 / A5 記載を見つけられず / A6 **4,556 skill・二重盲検の人手レビュー・矛盾率 9.4%** / A7 判定に LLM を使う / A8 なし / A9 なし。
- **判定: 部分的に重なる。** 母集団・人手の正解・矛盾率という評価の形は AuthGap と同じ型。対象は skill で、宣言側は自然言語、判定は LLM。**注意:** 既知リストの「SkillScope」が arXiv 2605.05868（CCS 2026 の least-privilege 論文）を指すのか、この 2605.12875 を指すのかは名前だけでは区別できない。両方を記録した。

#### 新規 6: ToFu（arXiv 2610.13651、2026-10-09）— ○（要旨と全文のキーワード検索）
- 原文 "ToFu, a tool-aware framework that automatically derives semantic security checks for LLM tools from their existing metadata and a CWE-guided sanitizer corpus … We evaluated ToFu across 273 MCP servers containing 3405 tools and identified verified bugs … in 343 tools across 118 of the servers." 全文中の annotation 系の語は 0 件 — [arXiv 2610.13651](https://arxiv.org/abs/2610.13651)
- 軸。A1 文書化された入力の意味（自然言語とスキーマ）/ A2 動的（fuzzing）/ A3 該当なし / A4 記載を確認せず / A6 273 サーバー。bug は verified と書いている / A7 不明。
- **判定: 隣接。**「宣言と実際の食い違い」を、入力検証について動的に測る。

#### 新規 7: 宣言だけを検査する・外から観察するだけの小規模な実践（すべて照合はしない）
- **cisoexpert「MCP Tool Annotations: What My 16-Server Scan Found」**（David O'Neil、2026-05-20）— ○。`tools/list` を取って 4 つのヒントが**あるか**だけを見る。手で選んだ 16 サーバーのうち 15 で「No annotations found」。残る 1 件（filesystem）は著者自身が誤判定と認めている。原文 "It doesn't prove the scanner is right." — [cisoexpert](https://cisoexpert.com/articles/mcp-annotation-gap-ecosystem-analysis/)
- **sunpeak「Testing MCP Tool Annotations」**（Abe Wheeler、2026-07-22）— ○。`tools/list` に対するテストで、有無と型、内部の整合（read-only なのに destructive でないか）、名前の動詞の規則、手で書いた期待値表を見る。挙動との照合は手作業のチェックリストに残している。原文 "Naming tests are intentionally blunt." — [sunpeak](https://sunpeak.ai/blogs/testing-mcp-tool-annotations/)
- **achandra-security/mcp-audit** — ○。オフラインで構成の inventory を読む。規則 MCP-002 は "Tool marked `readOnlyHint`, or named like a read (`get_`, `list_`, `search_`), that holds write-capable scopes"。ソースコードは読まない（宣言どうしの照合で、annotation と OAuth scope を比べる）— [mcp-audit](https://github.com/achandra-security/mcp-audit)
- **Correctover CCS（dev.to、2026-07 頃、ベンダーの記事）** — ○（主張の中身は検証できない）。原文 "zero (0) frameworks validated tool declarations against actual behavior"。自社の CCS がそれを実行時にやると主張するが、独立した評価は無い — [dev.to/correctover_15](https://dev.to/correctover_15/mcp-protocol-security-why-the-readonlyhint-vulnerability-exposes-a-fundamental-flaw-in-ai-agent-4630)
- **maniaclab/af-mcp-platform issue #332**（2026-10-01）— ○。ブローカーの管理画面に「Annotation mismatches」の表がある。何と比べて不一致と判定するかは書かれていない — [issue #332](https://github.com/maniaclab/af-mcp-platform/issues/332)
- **判定: すべて隣接。**

#### 出所の分からない数値（要追跡）: 「508 サーバーの調査、612 件の privilege annotation mismatch」— △
- bex.co のブログ（Dora Noda、2026-09-24）が、出典なしで「A 2026 survey of 508 MCP servers surfaced 8,286 findings, including 612 'privilege annotation mismatches'」と書いている（chain すると副作用が起きる `readOnlyHint: true` のツールを指す）— [bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)
- 元の調査は見つからなかった。数字が近い AgentSeal の 1,808 サーバー走査（総 8,282 件）は別のデータで、annotation の区分も持たない — [AgentSeal](https://agentseal.org/blog/mcp-server-security-findings)

#### 既知のツールで構図が少し変わる事実（調べ直しはしていない。読んだ範囲だけ）
- **mcp-doctor（PyPI mcp-server-lint）**: read-only の検査はツールの「own body」だけを見るパターン照合で、"Heuristic, deliberately narrow"。関数の委譲の解決は "Python-only, name-based (not fully import-resolved or type-resolved), and only covers direct calls" で上限 5 hop。ツール検出の recall は「15,755 of 15,977 tools found across 805 real servers on 5 frameworks」。表示された最新版は v1.18.2。前例として `codebase-memory-mcp#2118`（15 ツール中 13 が destructive/read-only を誤っていた）を挙げる — ○ [mcp-doctor](https://github.com/vishalhabib99/mcp-doctor)
- **actlint**: 推定に使うのは name・description・input schema だけ（"It never calls a tool"）。31 サーバー・541 ツールのうち、4 サーバーで「ラベルがスキーマの示す能力を否定」していた。2 件は著者自身の手検証で落ちた — ○ [dev.to/formael](https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3)
- **Airlock（himanshu748/airlock-mcp）**: 宣言を**動的な probe** の観察と比べる。静的な検査は「can guide probes, but it cannot be the authority」として実装していない — ○ [dev.to/himanshu_748](https://dev.to/himanshu_748/your-mcp-server-says-it-is-read-only-who-checked-2mjk)
- **HintLint**: 20 repo のパイロットで 1,160 ツール、確認済みの annotation の問題 23 件、精度 82% — △（検索要約経由。README は今回読み直していない）[HintLint](https://github.com/complira/hintlint)

#### 既知の 2609.15397 に、AuthGap の位置づけに使える一文がある
- 98,291 ツール（公式 registry、2026-07-27 時点）の census を取ったうえで、原文 "The census reads the boundary as declared, not as implementations behave … measuring the gap requires implementation-level analysis [23]." と書く。[23] は Toeppe et al. の arXiv 2607.10123（GitHub 上の MCP 実装のデータセット。全文中の annotation は 0 件）で、宣言と実装の照合はしていない — [arXiv 2609.15397 HTML](https://arxiv.org/html/2609.15397)、[arXiv 2607.10123](https://arxiv.org/abs/2607.10123)
- 同じ論文の原文 "many values may originate in SDK defaults or server templates rather than deliberate declaration … We do not attribute measured values to author intent." — [arXiv 2609.15397 HTML](https://arxiv.org/html/2609.15397)

### Inferences
- 両側を照合する（D と M）ものは、新着でも既知のツール（HintLint、mcp-doctor）の域を出ていない。どちらも「own body」の範囲か、検査範囲の狭いパターン照合で、母集団・人手の正解・凍結を備えた論文は見つからなかった。AuthGap の差分は、手続き間の M（深さ 4）、引数位置の粒度、`opaque(reason)` と未解決率、事前登録した母集団、人手の実態調査、修正コミットによる recall の組み合わせにある。この主張は今回の検索範囲では崩れなかった。
- 2609.15397 は「implementation-level analysis が要る」と書いて終わっている。AuthGap はその空白を正面から埋める、と書ける（引用するときは原文の一文を使う）。
- MCPacific の 56 パターンは、AuthGap の入口規則 14 と比べるべき先行例になる。「入口規則は領域固有の貢献」と主張するなら、MCPacific との違い（入口の後で効果を推定するか）を書く必要がある。

### Gaps
- 「508 サーバー / 612 privilege annotation mismatches」の元の調査は見つからなかった。実在すれば母集団規模の矛盾件数になるので、最優先で追う。
- hintgap の作成日と PyPI での公開状況は確認できなかった。
- FCD が Python の MCP サーバーをどこまで対象にしているか（4 profile の中身）は通読していない。

---

## Q2. 既知の論文の改訂版（v2/v3）は annotations を読むようになったか

### Takeaway
**annotations を読むようになった改訂は見つからなかった。** 既知の 19 本の arXiv 最新版を API で確かめた。改訂があったのは No-Box（v2、2026-09-16）、VIPER-MCP（v2、2026-08-12）、AgentBound（v3、2026-04-24）、SkillScope 2605.05868（v3、2026-09-10）の 4 本で、どれも全文中に `readOnlyHint` / `destructiveHint` / `ToolAnnotations` は 0 件だった。DCIChecker・MCPDiFF・MCP-BiFlow・mcp-sec-audit・SkillConsist は v1 のまま。

### Cited Findings
- arXiv API の id_list で最新版を取った結果（取得日 2026-10-12）: 2606.04769 DCIChecker v1 / 2602.03580 MCPDiFF v1 / 2602.18914 v1 / 2609.10962 v1 / 2609.15397 v1 / 2607.07461 v1 / 2601.08012 v1 / 2606.06387 v1 / 2510.21236 AgentBound **v3（2026-04-24）** / 2607.21835 v1 / 2507.06250 v1 / 2603.21641 mcp-sec-audit v1 / 2609.10854 No-Box **v2（2026-09-16）** / 2605.21392 VIPER-MCP **v2（2026-08-12）** / 2605.07836 MCP-BiFlow v1 / 2607.25297 v1 / 2605.00314 Semia v1 / 2608.07639 SkillConsist v1 / 2607.01640 AgentFlow v1 — [arXiv API query](https://export.arxiv.org/api/query?id_list=2606.04769,2602.03580,2609.10854,2605.21392,2608.07639)
- SkillScope（arXiv 2605.05868）は **v3（2026-09-10）**、ACM CCS 2026 に採録（DOI 10.1145/3830454.3846588）。v3 の全文中で annotations は 0 件 — [arXiv 2605.05868v3](https://arxiv.org/abs/2605.05868)
- 全文 HTML のキーワード件数（自分で取得して数えた）: DCIChecker v1 は「annotation」0 件。No-Box v2 は「annotation」5 件で、すべて人手のラベル付けの意味（ToolAnnotations の意味ではない）。VIPER-MCP v2 は 0 件。SkillConsist v1 は 7 件で、すべてベンチマークのラベルの意味 — [DCIChecker HTML](https://arxiv.org/html/2606.04769v1)、[No-Box v2 HTML](https://arxiv.org/html/2609.10854v2)、[SkillConsist HTML](https://arxiv.org/html/2608.07639)

### Inferences
- 2026-10-12 の時点で、既知の論文の側から AuthGap の範囲（構造化 annotation と code の照合）へ寄ってきた動きは見えない。

### Gaps
- arXiv API が当日の差し替えを反映していない可能性がある（反映は通常 1 日遅れる）。
- 会議版（CCS・USENIX 等）のカメラレディが arXiv と別の内容になっていないかは確かめていない。

---

## Q3. HintLint / mcp-doctor / actlint / Airlock などの背後に論文・技術報告はあるか

### Takeaway
**背後の論文・プレプリント・技術報告は見つからなかった。** どれも README とブログ記事（dev.to 等）だけ。HintLint の README は「report」に言及するが、文書そのものは検索で出なかった。

### Cited Findings
- HintLint について、論文・プレプリント・技術報告は検索で見つからず、パイロットの数値は README にしか無い — △（検索要約）[HintLint](https://github.com/complira/hintlint)
- actlint は Formael の dev.to 記事（Dilan Srilal、7/26）だけ。原文 "Under-claiming a risk beats crying wolf, because a linter people stop believing is not worth running." — ○ [dev.to/formael](https://dev.to/formael/are-your-mcp-servers-safety-labels-honest-a-one-command-check-and-what-it-found-on-31-popular-1ml3)
- Airlock は dev.to 記事（Himanshu Kumar、8/30）だけで、論文の引用は無い。「airlock」という名の repo は無関係なものが 2 つある（PKusch/airlock、jewunetie/airlock）— ○ [dev.to/himanshu_748](https://dev.to/himanshu_748/your-mcp-server-says-it-is-read-only-who-checked-2mjk)、△ [PKusch/airlock](https://github.com/PKusch/airlock)
- mcp-doctor は README の中に「pass」ごとの開発記録があるだけで、日付は無く、論文は無い — ○ [mcp-doctor](https://github.com/vishalhabib99/mcp-doctor)

### Inferences
- 関連研究の節では、これらを「査読も技術報告も無い OSS」として扱うのが正確。数値（82% 等）は著者の README の主張として引く。

### Gaps
- OpenReview と Google Scholar は直接検索していない（下の検索ログを参照）。ワークショップの短報があっても拾えていない可能性がある。

---

## Q4. 他プロトコルの同等の構造化ヒント（OpenAI Apps SDK、GPT Actions、ADK、A2A、LangChain、Claude Code）をコードと照合しているものはあるか

### Takeaway
**照合しているものは見つからなかった。** ただし構図を変える事実が 1 つある。**OpenAI は Apps の審査で annotation の「automated review」を実施している**と公式に書いている。何と照合しているかは公開されていない。ほかのプロトコル（`x-openai-isConsequential`、ADK・A2A の agent card、LangChain の metadata、Claude Code の `allowed-tools`）については、コードと照合する研究・ツールは見つからなかった。

### Cited Findings
- OpenAI App submission guidelines の原文 "If our automated review flags an annotation issue, you can submit an appeal with clarification or additional information." / "Annotation justifications are no longer required." / "Being able to undo an action does not, by itself, justify setting `destructiveHint` to `false`." `idempotentHint` には触れていない。automated review が何と照合するかの記述は無い — ○ [OpenAI Apps SDK guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)
- 食い違い。検索要約は「Reviewers also expect a written justification for each hint」と述べていたが、公式ページの現行版は「no longer required」。**現行の公式ページを採る** — 公式は○ [guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)、要約は△ [OpenAI community](https://community.openai.com/t/clarification-needed-on-rejection-feedback-tool-annotations-and-developer-name-mismatch/1379402)
- OpenAI の審査で annotation を直した開発者の PR・issue（leadbay/mcp PR #272「every tool declares what it does and what it changes (OpenAI review)」、plugpressco/saddle issue #267 等）— △（検索スニペット）[leadbay PR #272](https://github.com/leadbay/mcp/pull/272)、[saddle #267](https://github.com/plugpressco/saddle/issues/267)
- GPT Actions の `x-openai-isConsequential` は、未設定なら GET は false・それ以外は true として扱われる、とフォーラムに書かれている（公式文書ではない）。照合ツールは見つからなかった — △ [OpenAI community](https://community.openai.com/t/how-to-stop-custom-gpt-displaying-confirm-deny-buttons/874551)
- 宣言フラグがどの実行経路からも読まれていなかった例。objectstack の PR が「declarative tool confirmation flag was read by no execution path」と報告している — △（検索スニペット）[objectstack PR #3740](https://github.com/objectstack-ai/objectstack/pull/3740/files)
- Google ADK・A2A。agent card は agent の定義から生成できるが、生成後に検証する記述は無い — ○ [Google Cloud Agent Registry docs](https://docs.cloud.google.com/agent-registry/register-custom-adk-agents)
- LangChain の `metadata` は callback に渡す追跡用で、副作用の宣言ではない — △ [LangChain reference](https://reference.langchain.com/python/langchain-core/tools/base/BaseTool/metadata)。Rust の `salvor-tools` は side-effect の分類を宣言して再試行の可否に使う — △ [docs.rs salvor-tools](https://docs.rs/salvor-tools/=0.5.2/)
- Claude Code の `/skill-doctor`（2.1.261、2026-09-04）は skill の使用状況とコンテキストのコストを監査するもので、宣言した権限と実際の挙動の照合ではない — △ [implicator.ai](https://www.implicator.ai/anthropic-claude-code-skill-doctor-context-audit/)
- MCP 公式の Tool Annotations Interest Group の repo（`experimental-ext-tool-annotations`）。SEP-2061 は「closed 2026-06-13 in favour of this extension」。草案は trust-annotations と action-metadata。annotation の正しさの測定は無く、out-of-scope の欄に「clients won't trust server self-attestation」とある — ○ [experimental-ext-tool-annotations](https://github.com/modelcontextprotocol/experimental-ext-tool-annotations)
- 2609.22573（Zero-Trust Authorization、2026-09-18）の「annotation」は自前の `@require_permissions`（RBAC）で、ToolAnnotations ではない。原文 "permission-filtered tool visibility kept consistent with per-tool invocation enforcement by a single declarative annotation" — ○ [arXiv 2609.22573](https://arxiv.org/abs/2609.22573)
- ContractGuard（arXiv 2606.18550、2026-06-17）。gate が読むツール契約（効果・リスクのラベル）の完全性を論じる。原文 "attestation budget should concentrate: the precondition/effect annotations, not the risk label." コードとの照合はせず、署名と attestation で守る — ○ [arXiv 2606.18550](https://arxiv.org/abs/2606.18550)

### Inferences
- OpenAI の automated review は**中身の公開されない競合**にあたる。関連研究では「プラットフォームの審査で automated review が行われているが、手法・精度は非公開」と正確に書くのが安全。AuthGap が公開の手続き（凍結・事前登録・人手の正解）で測ることの意味は、この対比で説明できる。
- OpenAI の審査で起きた修正（leadbay 等）は、AuthGap の 352 の修正コミットに混ざっている可能性がある。審査に促された修正が、ある方向（ヒントの欠落を埋める、名前に合わせる）に偏っていれば、recall の測定に選択の偏りが入る（未検証の推測）。

### Gaps
- OpenAI の automated review の手法（コードを見るのか、名前・説明だけか）は公開情報からは分からなかった。
- Google ADK の tool confirmation と A2A を単独で検索していない。ADK の `require_confirmation` の文書は読んでいない。

---

## Q5. 開発者が annotation を変えた・直したコミットをマイニングした研究、または採用状況と正しさを経時で測った研究はあるか

### Takeaway
**修正コミットをマイニングした論文は見つからなかった。** 経時の測定では、新たに 2 件見つかった。**宣言だけを経時に差分するもの**が mcpindex.ai の drift ledger（毎日）と vru123/mcp-tool-drift（20 サーバーのリリース間）で、どちらもコードとは照合しない。修正の個別例（PR・issue）は多く見つかった。多くは「欠けた readOnlyHint のせいでクライアントが承認を求める」問題への対処だった。

### Cited Findings
- **mcpindex.ai drift ledger**（Gautam Bharti）— ○。公開 registry を毎日クロールして、ツール契約の差分を記録する。2026-10-12 時点の数値は 31,465 ツール・3,455 サーバーが公開項目を変更（安全に関わる変更は 23,819）。**「1,936 tools flipped a read-only hint toward write, delete, or send」**。原文 "A contract-diff, not a safety verdict, and not prevention." — [mcpindex ledger](https://mcpindex.ai/ledger)
- mcpindex の方法。差分は決定論で "No LLM, no scoring you cannot trace"。別段の intent judge は LLM。挙動との照合（conformance probe）は "Built but not yet run on the public corpus"。DOI と凍結の記載は無い — ○ [mcpindex methodology](https://mcpindex.ai/methodology)
- mcpindex PR #228（2026-09-28 にマージ）。destructive 方向への変化 123 件の内訳は「55 tools changing a hint they already declared plus 68 tools labeling themselves for the first time」。対象は 18,748 の eligible サーバーで、そのうち 4,652 が変化 — ○ [PR #228](https://github.com/mcpindex-ai/mcpindex-web/pull/228)（ledger の 1,936 件とは集計の範囲が違う。どちらが新しいかは確かめていない）
- **vru123/mcp-tool-drift**（snapshot 2026-10-05）— ○。20 サーバー・181 リリースを `tools/list` だけで probe（"No tool is ever called."）。152 の区間のうち 108（71%）にエージェントから見える変化があった。**既に宣言されていたヒントの反転は 4 サーバーで 12 件（うち 10 件はリスクが上がる方向）、初めて宣言されたヒントは 458 件。** 12 件の反転はどれもリリースノートに書かれていなかった — [mcp-tool-drift](https://github.com/vru123/mcp-tool-drift)
- LiteLLM issue #44093。MCP ツールの pin が annotations と outputSchema を無視するので、readOnlyHint が destructive へ反転しても drift の警告が出ない — △（検索スニペット）[LiteLLM #44093](https://github.com/BerriAI/litellm/issues/44093)
- 修正の個別例（どれも △、検索スニペット）。gogcli-mcp PR #443「annotate tools truthfully and sync manifests」、github-mcp-server issue #2483「Audit and fix missing ReadOnlyHint annotations」、txn2/mcp-data-platform #1692「read-only tools ship without ReadOnlyHint, so strict MCP clients gate every read」、mcp-utils PR #267（`readOnlyHint` が false のとき既定値で destructive=true になって公開されていた）— [gogcli-mcp #443](https://github.com/chrischall/gogcli-mcp/pull/443)、[github-mcp-server #2483](https://github.com/github/github-mcp-server/issues/2483)、[txn2 #1692](https://github.com/txn2/mcp-data-platform/issues/1692)、[mcp-utils #267](https://github.com/chrischall/mcp-utils/pull/267)
- クライアント側が annotation を読めていない例。hermes-agent の複数の issue と PR が「mcp==2.0.0 では `ToolAnnotations` が `read_only_hint`（snake_case）で公開され、`getattr(annotations, "readOnlyHint", None)` が常に None になる」と報告している — △（issue の主張。SDK のソースは見ていない）[hermes-agent #132042](https://github.com/NousResearch/hermes-agent/issues/132042)、[PR #101998](https://github.com/NousResearch/hermes-agent/pull/101998)

### Inferences
- AuthGap の「前のリリースの効果」（宣言側の第 3 の源）と 352 の修正コミットの組み合わせに対して、mcpindex と mcp-tool-drift は**宣言どうしの経時差分**しか見ていない。「宣言の変化がコードの変化に裏づけられているか」は誰も測っていない。AuthGap の r_prev（前のリリースとの照合）は、ここで差を主張できる。
- 修正の個別例は「欠落 → 追加」と「既定値の罠」が多く、「偽の readOnlyHint=true → false」は少なく見える（件数を数えたわけではない）。AuthGap の recall セット 352 件の方向の内訳を報告しておくと、この偏りへの反論に備えられる。
- **AuthGap の宣言側の抽出への含意（要確認）。** issue の主張どおり Python SDK 2.x の `ToolAnnotations` が snake_case（`read_only_hint=`）で書かれるなら、camelCase のキーワードだけを読む宣言側の抽出は、SDK 2.x のサーバーの宣言を黙って「宣言なし」にしうる。これは宣言を取りこぼして矛盾を見逃す方向、つまり false-clean 側の誤りになる。解析器は凍結中なので直さず、確かめたうえで `docs/open_questions.md` の扱いにするのが規則に沿う（**未検証**。SDK のソースと AuthGap の抽出規則は今回見ていない）。

### Gaps
- annotation を修正したコミットを体系的にマイニングした論文は見つからなかった。
- mcpindex の ledger（1,936 件）と PR #228（123 件）の数値の関係（範囲・期間）は確認できなかった。
- 2609.14721（MCP の公開と採用の二次元研究）は全文中に annotation が 1 件（参考文献の中）しか無く、annotation の経時分析は含まない — ○ [arXiv 2609.14721](https://arxiv.org/abs/2609.14721)

---

## Q6. MCP の仕様議論（SEP・GitHub issue）に、annotation の正しさの研究を引用しているものはあるか

### Takeaway
**正しさの測定を引用した SEP・議論は見つからなかった。** 仕様は「信頼できるサーバー以外の annotation は untrusted」という立場のままで、議論は検証よりも語彙の拡張（trust、sensitivity、action-metadata）と attestation の方へ進んでいる。

### Cited Findings
- 仕様（2026-07-28 版）は、クライアントは信頼できるサーバー以外から得た annotation を untrusted とみなさなければならない（MUST）とする — △（検索要約）[MCP spec tools 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- SEP-1487（`trustedHint`）、SEP-1913（Trust and Sensitivity Annotations）、SEP-1862（Tool Resolution）。SEP-1862 についての maintainer のコメントは「tools/list で偽るサーバーは tools/resolve でも偽りうる」— △（検索要約）[SEP-1487](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1487)、[SEP-1913](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1913)、[SEP-1862](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1862)
- registry の Discussions に「attestation-reference field on server.json + verify-on-publish」の提案がある（2026-07-23、タイトルだけ確認）— △ [registry discussions](https://github.com/modelcontextprotocol/registry/discussions)
- Interest Group の repo には正しさの測定が無い（Q4 を参照）— ○ [experimental-ext-tool-annotations](https://github.com/modelcontextprotocol/experimental-ext-tool-annotations)

### Inferences
- 仕様側は「検証しない、信頼しない」で一貫しており、どれだけ間違っているかの数字を持っていない。AuthGap の実態調査（最大 200 ツールの人手判定）は、この議論に直接入る数字になりうる。

### Gaps
- modelcontextprotocol org の issue と discussions を全文検索してはいない（GitHub MCP を使わない制約。web 検索経由だけ）。

#### 検索ログ（実行したクエリと結果）
arXiv API（`export.arxiv.org/api/query`、submittedDate の降順）:
- `all:"readOnlyHint"` → 1 件（2606.06387、既知）
- `all:"destructiveHint"` → **0 件（見つからなかった）**
- `abs:"tool annotations" AND abs:MCP` → **0 件（見つからなかった）**
- `all:"idempotentHint" OR all:"openWorldHint"` → **0 件（見つからなかった）**
- `abs:annotations AND abs:"Model Context Protocol"` → 18 件。照合するものは無し（2609.22573 と 2604.05969 は全文で確認して無関係）
- `abs:"side effect" AND abs:MCP` → 10 件 / `abs:"static analysis" AND abs:"MCP server"` → 9 件（既知か隣接）/ `abs:declared AND abs:MCP AND abs:tool` → 24 件 / `abs:"MCP server"` の最新 100 件（総数 209）/ `all:SkillScope` → 3 件 / `abs:"agent skills" AND (inconsisten* OR mismatch OR undeclared)` → 9 件 / `abs:"over-privileged" AND (agent OR MCP)` → 12 件 / `abs:"read-only" AND abs:MCP` → 2 件（無関係）/ `abs:"tool metadata" AND (MCP OR agent)` → 19 件 / `abs:hints AND abs:"Model Context Protocol"` → 3 件 / `abs:MCP AND (consistency OR inconsistency OR mismatch)` → 205 件（2026-06 以降に絞って確認）/ `abs:"static analysis" AND (agent tool 系)` → 44 件 / `abs:"Apps SDK" OR "ChatGPT apps" OR "GPT Actions"` → 7 件で**関連なし** / `abs:effect AND tool AND declared AND agent` → 28 件
- 全文 HTML を取得し `readOnlyHint|destructiveHint|idempotentHint|openWorldHint|ToolAnnotations` を数えて **0 件だったもの**（照合する研究ではないことを確認した）: 2610.13651, 2610.05319v2, 2609.22573, 2604.05969, 2610.06966v2, 2606.05339v2, 2605.05868v3, 2605.12875, 2610.01349, 2609.31358, 2604.21477v2, 2607.14754, 2608.24017, 2606.20023v2, 2605.09163v3, 2607.11086, 2608.00150, 2603.22853, 2607.25635v2, 2610.13623, 2609.28585, 2609.14721, 2602.14281, 2609.10854v2, 2605.21392v2, 2608.07639, 2606.04769v1, 2609.35088, 2610.03014, 2606.18550, 2607.10123。ヒットがあったのは既知の 2609.15397 と 2609.10962 だけ。
- 要旨だけ見て関係が薄いと判断したもの（全文は見ていない）: 2609.23498 RAC, 2609.14631 IntentCap, 2608.21159 AID-Guard, 2609.38266 Janus, 2609.05920 ClosureBound, 2608.25322 Metis, 2610.00182, 2609.24161 MCP-GRANITE, 2608.20481 AEGIS, 2606.21071 CLAWAUDIT, 2608.00783。

Semantic Scholar API: 8 回すべて HTTP 429（rate limit）。**実施できなかった**（結果ゼロとは扱わない）。
DBLP API: bot 判定のページが返り、**実施できなかった**。

Web 検索（WebSearch）:
1. `"readOnlyHint" static analysis MCP server code mismatch` → hermes-agent の issue、OpenAgent #31、trace-mcp。照合する新しいツールは無し
2. `"destructiveHint" lint tool annotations verify implementation` → HintLint（既知）、gogcli PR、sunpeak
3. `MCP tool annotations wrong incorrect study … 2026` → cisoexpert（新規）、既知の論文。正しさの測定は**見つからなかった**
4. `"annotation drift" MCP tools` → mcpindex PR #228（新規）、af-mcp-platform #332
5. `MCP tool annotations "readOnlyHint" checker GitHub Action AST side effects September 2026` → HintLint だけ
6. `modelcontextprotocol SEP tool annotations trust … study incorrect hints` → SEP-1487/1913/1862。研究の引用は**見つからなかった**
7. `OpenAI Apps SDK tool annotations … review rejected incorrect annotations` → 審査の指針、開発者の修正例
8. `mcpindex drift report …` → ledger、mcp-tool-drift（新規）、LiteLLM #44093
9. `"x-openai-isConsequential" OR "require_confirmation" … static analysis` → 照合は**見つからなかった**
10. `LangChain tool metadata side effects static analysis … paper` → **見つからなかった**
11. `HintLint complira … paper OR preprint OR "technical report"` → 論文は**見つからなかった**
12. `actlint OR "airlock-mcp" OR "mcp-server-lint" …` → dev.to の 2 記事
13. `"tool annotations" MCP empirical study adoption …` → 既知の 2609.10962 / 2609.15397、greynewell の再現実験
14. `MCP server annotations verify source code "call graph" … Python open source` → **hintgap（新規）**
15. `modelcontextprotocol github discussion … attestation … registry vetting` → Interest Group の repo、attestation の提案
16. `Google ADK tool confirmation OR A2A agent card … static analysis` → 照合は**見つからなかった**
17. `"readOnlyHint" commits developers fixed annotations mining study` → マイニング研究は**見つからなかった**（個別の PR だけ）
18. `Claude Code skill "allowed-tools" declared vs actual …` → **見つからなかった**（/skill-doctor だけ）
19. `MCP "behavioral annotations" OR "tool hints" verification … October 2026` → 既知だけ
20. `MCP servers mislabeled readOnlyHint tools that write audit …` → bex.co（508 サーバーの又引き）、mcp-audit（新規）
21. `"tool annotations" MCP "static analysis" Python AST … subprocess open write requests` → **見つからなかった**
22. `"508 MCP servers" "8,286" findings "privilege annotation"` → bex.co だけ。元の調査は**見つからなかった**

実施していない検索（残りの穴）: Google Scholar の直接検索、OpenReview、Hacker News、PyPI と npm の全文検索、Trail of Bits / Wiz / Unit 42 / Docker / Socket の各ブログの個別検索、modelcontextprotocol org の issue の網羅（GitHub MCP を使わない制約による）。
