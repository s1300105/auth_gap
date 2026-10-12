# 一般ソフトウェア（LLM エージェント外）で「宣言された副作用・権限・安全性」を実コードと静的に照合する研究 — AuthGap の位置づけのための先行研究調査

調査日 2026-10-12。凡例と前提（この節は見出しではなく前置き）:

- **検証水準**: ◎ = 一次資料の本文（該当節）を自分で読んだ（PDF は scratchpad に置いて `pdftotext` で読んだ。リポジトリには置いていない）／○ = 要旨・公式ページ・公式ドキュメントのみ（WebFetch の要約を含む）／△ = 二次資料（他論文の引用、セミナー要約、検索エンジンの要約）。
- **数値はすべて著者の主張で、こちらでは再現していない**（AuthGap の規則 1 に従い `verified_by_me = none` 扱い）。論文内で数値が食い違うものは両方を書いた。
- 依頼の「既出リスト」（Stowaway, PScout, Koved/Pistoia, Mir, Capslock, Packj, Sălcianu & Rinard, JPure, Checker Framework Purity Checker, Sahin & Arcuri, Respector, Rodríguez et al., PoliCheck, Lalaine, ExtPrivA）は再調査していない。比較の文脈で名前だけ出す。
- 各項目の A1〜A9 は依頼どおり: A1 宣言と強制の有無／A2 実効側の導出／A3 手続き間か・深さ／A4 言語／A5 未解決の扱いと率の報告／A6 母集団・正解・違反率／A7 決定論／A8 事前登録／A9 修正コミットを正解に使うか。判定は「同一／大きく重なる／部分的に重なる／隣接」。
- A8 について: PDF から取得した 22 本の本文テキスト（◎ の論文すべてと、Granite・ALPS・SACMAT 2022・Kechagia MSR 2014）を `pre-?regist|registered report` で grep し、**一致は 0 件**だった（どの論文も事前登録に触れていない）。以下の各項目の「A8: なし」はこの grep に基づく。本文を取得できなかったもの（○・△）は「不明」とした。

## 1. HTTP / API の意味論 — safe / idempotent の宣言と実装の不一致を静的に検出する研究

### Takeaway
既出（Sahin & Arcuri, Respector, Rodríguez et al.）以外では、「safe と宣言された入口（GET など）が状態を書き換える」ことを静的に検出して**母集団での違反率を出した学術研究は見つからなかった**。いちばん近いのは産業ツールの CodeQL クエリ `java/csrf-unprotected-request-type`（GET 系ハンドラから DB 更新への到達を call graph で探す。AuthGap の「readOnlyHint の入口から書き込み sink へ」と機構がほぼ同じ）だが、評価結果は公開されていない。冪等性では Flux（OSDI 2023）がサーバーレス関数の冪等性を検証している。ただし照合する「宣言」はなく、プラットフォームが暗黙に求める要件を検証している。gRPC の `idempotency_level` と GraphQL の query/mutation 区別を実装と照合する研究は見つからなかった。

### Cited Findings

#### [1-1] CodeQL クエリ `java/csrf-unprotected-request-type`（GitHub, 産業ツール）— 検証 ○
- 出典: [CodeQL query help](https://codeql.github.com/codeql-query-help/java/java-csrf-unprotected-request-type); [ライブラリ CsrfUnprotectedRequestTypeQuery.qll](https://codeql.github.com/codeql-standard-libraries/java/semmle/code/java/security/CsrfUnprotectedRequestTypeQuery.qll/module.CsrfUnprotectedRequestTypeQuery.html)
- A1 宣言: ハンドラの HTTP メソッド（GET 等）。ヘルプページは「safe HTTP request methods (such as GET) should only perform read-only operations」と書く。宣言は意味論上の約束にすぎず、強制はない。Spring は unsafe メソッドにだけ既定の CSRF 保護をかけ、Stapler は POST にだけかける ([help](https://codeql.github.com/codeql-query-help/java/java-csrf-unprotected-request-type))。
- A2 実効: `DatabaseUpdateMethod`（「A method that updates a database.」）を状態変更とみなす。`unprotectedStateChange` は「Holds if `source` is an unprotected request handler that may change an application's state.」と定義されている ([qll](https://codeql.github.com/codeql-standard-libraries/java/semmle/code/java/security/CsrfUnprotectedRequestTypeQuery.qll/module.CsrfUnprotectedRequestTypeQuery.html))。
- A3: モジュールは `CallGraph`（「call graph paths」）を持ち、`relevantEdge` が経路の辺を返す。ハンドラからの手続き間到達とみられるが、深さの上限は確認できなかった ([qll](https://codeql.github.com/codeql-standard-libraries/java/semmle/code/java/security/CsrfUnprotectedRequestTypeQuery.qll/module.CsrfUnprotectedRequestTypeQuery.html))。
- A4: Java（Spring / Stapler のみ）([help](https://codeql.github.com/codeql-query-help/java/java-csrf-unprotected-request-type))。
- A5: 記載なし。
- A6: 公開された評価はない。メタデータは precision = medium、security severity 8.8、CWE-352 ([help](https://codeql.github.com/codeql-query-help/java/java-csrf-unprotected-request-type))。
- A7: CodeQL は決定的な Datalog 評価（一般論。このクエリ固有の記述はない）。A8: 該当なし（ツール）。A9: なし。
- **判定: 「部分的に重なる」** — 「safe と宣言された入口から書き込み効果に到達する」という照合の形は AuthGap の readOnlyHint 照合と同じ。違いは、宣言が HTTP メソッド 1 種類だけであること、CSRF という脆弱性の枠で書かれていること、母集団での測定がないこと。

#### [1-2] Flux — Ding et al., "Automated Verification of Idempotence for Stateful Serverless Applications"（OSDI 2023）— 検証 ◎
- 出典: [PDF](https://www.usenix.org/system/files/osdi23-ding.pdf)
- A1 宣言: 明示的な注釈はない。リトライ前提のプラットフォームが関数に冪等性を暗黙に要求する（「such a retry-based approach requires functions to be idempotent」）([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))。
- A2 実効: 「idempotence consistency」を定義し、関数ごとの rely/guarantee 推論とシンボリック実行で冪等性違反の操作を特定する ([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))。
- A3: 手続き間。合成的に証明する（「compositional proof techniques」）。
- A4: Java のみ（「Flux currently supports only Java applications」）。状態は NoSQL の key-value DB に限ると仮定している ([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))。
- A5: 「sound but incomplete」。扱えない無限ループは advisor 側に回して全部ログを取る。未対応の率は報告されていない ([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))。
- A6: 27 アプリ（79 関数）。「Flux has successfully identified previously unknown issues in 12 applications. Developers have confirmed 8 issues.」([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))
- A7: 検証器なので決定的とみられる（明記はない）。A8: なし。A9: なし（開発者の確認を使う）。
- **判定: 「隣接」** — idempotentHint に対応する性質を静的に検証した最も強い先行例。ただし宣言との照合ではなく、要件そのものを検証している。

#### [1-3] Deemon — Pellegrino et al., "Deemon: Detecting CSRF with Dynamic Analysis and Property Graphs"（CCS 2017）— 検証 ◎（該当節）
- 出典: [arXiv 1708.08786](https://arxiv.org/abs/1708.08786)
- A1: 宣言側はない（HTTP メソッドの区別はしない。本文テキストに「GET」は 0 回しか出てこない）。A2: 動的トレースから property graph を作り、状態遷移につながる HTTP 要求（state-changing request）をグラフ走査で取り出す ([arXiv](https://arxiv.org/abs/1708.08786))。A4: PHP。A6: 「Deemon with 10 popular open source web applications. Our experiments uncovered 14 previously unknown CSRF vulnerabilities」([arXiv](https://arxiv.org/abs/1708.08786))。A7〜A9: 動的、事前登録なし、修正コミットなし。
- **判定: 「隣接」** — 「どの要求が状態を変えるか」を実効側として推定した例だが、動的で、宣言と照合しない。

#### [1-4] APIdemic — Goplani, "APIdemic: Verifying Idempotency of REST API Clients"（POPL 2025 Student Research Competition ポスター）— 検証 ○
- 出典: [POPL 2025 SRC](https://popl25.sigplan.org/details/POPL-2025-student-research-competition/17/APIdemic-Verifying-Idempotency-of-REST-API-Clients)
- REST クライアントプログラムの冪等性を、状態遷移としてモデル化した静的解析で検証すると要旨にある。評価は「will be evaluated」で、数値はない ([POPL SRC](https://popl25.sigplan.org/details/POPL-2025-student-research-competition/17/APIdemic-Verifying-Idempotency-of-REST-API-Clients))。
- **判定: 「隣接」**（ポスター段階。宣言との照合はしない）。

#### 参照のみ: gRPC / protobuf の `idempotency_level`
- protobuf の `MethodOptions.IdempotencyLevel` は `IDEMPOTENCY_UNKNOWN` / `NO_SIDE_EFFECTS` / `IDEMPOTENT` を持つ宣言で、実装を検査する仕組みは仕様にない ([protobuf.dev](https://protobuf.dev/reference/java/api-docs/com/google/protobuf/DescriptorProtos.MethodOptions.IdempotencyLevel.html))。この宣言を実装と照合する静的検査器や研究は見つからなかった。

### Inferences
- 「safe 宣言の入口 → 書き込み sink」という照合は、産業 SAST では既知の検査になっている（CodeQL のクエリ。Spring 向けには [Semgrep のルール](https://registry.semgrep.dev/rule/java.spring.security.unrestricted-request-mapping.unrestricted-request-mapping) や [Xygeni の検出器](https://detectors.xygeni.io/xydocs/sast/detectors/java/java.unrestricted_request_mapping.html) もある。後 2 者は検索結果の要約による。△）。AuthGap が readOnlyHint の照合を新規の仕組みとして主張するのは危うい。主張できるのは、(a) MCP のツール入口の規則（`ENTRY_RULES`）、(b) 4 種類の hint を同時に扱うこと、(c) 母集団での測定と opaque の会計、のほうだろう。
- HTTP の safe/idempotent の宣言は「メソッド名」という構文的な宣言で、宣言の誤りが CSRF などの具体的な攻撃に結びつく。MCP の hint はクライアントが UI の確認省略などに使いうる助言であり、誤りの帰結が別の経路をたどる。この点は比較表で分けて書く価値がある。

### Gaps
- 「GET/HEAD が状態を書き換える」ことを母集団（例: GitHub 上の Spring/Django/Rails アプリ）で静的に測った論文は見つからなかった（クエリ: `static detection state-changing GET requests web application HTTP safe method violation`、結果は実務記事だけ）。
- GraphQL の Query フィールドに副作用がある（mutation を query に置いた）ことを静的に検出する研究は見つからなかった（クエリ: `GraphQL query resolver side effects static analysis mutation in query detection paper`。見つかったのはコスト解析、動的テスト（GraphQLer）、実務チェックリストだけ）。
- OpenAPI の `readOnly` や `x-` 拡張を実装と照合する研究は、既出の Respector 以外に見つからなかった。RESTRuler（ICSA 2024）は OpenAPI 文書だけを検査し、コードとは照合しない（検索結果の要約による。△）。
- CodeQL クエリの適合率・再現率を測った公開評価は見つからなかった。

## 2. 宣言された純粋性・不変性・スレッド安全性 — 開発者の注釈はどれくらい間違っているか

### Takeaway
`@Pure` / `@SideEffectFree` / Kotlin・JetBrains の `@Contract(pure=true)` / C# の `[Pure]` / `@CheckReturnValue` / Python の `functools.cache` について、**開発者が書いた純粋性注釈の誤り率を測った研究は見つからなかった**。一方、隣接する性質（ロック規律、スレッド安全性、型）では「助言的な（強制されない）注釈を静的に検査すると、開発者の注釈はかなりの割合で間違っている」という実証がある。最も強いのは Ernst et al.（ICSE 2016）で、`@GuardedBy` を書いた全プログラムに誤った注釈があり、programmer-written の precision は 19–100%、recall は 6–84% だった。Python の型注釈では MyPy で型が通るリポジトリが 15% しかない（DLS 2020）。

### Cited Findings

#### [2-1] Ernst, Lovato, Macedonio, Spoto, Thaine, "Locking discipline inference and checking"（ICSE 2016）— 検証 ◎
- 出典: [PDF](https://homes.cs.washington.edu/~mernst/pubs/locking-inference-checking-icse2016.pdf)
- A1 宣言: JCIP の `@GuardedBy` / `@Holding`。もともと文書化の慣習で、ツールの裏付けはない。論文は JCIP の仕様自体が曖昧で、どの解釈でもデータ競合を許すと指摘している（「every interpretation of it permits data races」）。GitHub に「about 35,000 uses of the annotation in 7,000 files」がある ([PDF](https://homes.cs.washington.edu/~mernst/pubs/locking-inference-checking-icse2016.pdf))。
- A2 実効: 抽象解釈（Julia）による推論と、型検査（Lock Checker）による検査の 2 系統。両者は別人が書きコードを共有しないので、一致が実装の正しさの傍証になる、と論文は書く ([PDF](https://homes.cs.washington.edu/~mernst/pubs/locking-inference-checking-icse2016.pdf))。
- A3: 手続き間（creation-points 解析で値の同一性を近似する）。A4: Java。
- A5: 健全性を主張する（「the first tools that can soundly infer and check a locking discipline for Java」）。未解決の率は報告されていない。
- A6: OSS 15 本。開発者が注釈を書いていたのは 5 本。正解集合（goal set）は「we manually analyzed every annotation written by the programmer or inferred by Julia」で手作業で作った。結論は「programmers often make mistakes (precision 19–100%, recall 6–84%): they write locking-discipline specifications that their programs do not follow, and they fail to write ones that their programs do follow.」また「In every program where programmers documented a locking discipline, they wrote incorrect annotations」([PDF](https://homes.cs.washington.edu/~mernst/pubs/locking-inference-checking-icse2016.pdf))。
- A7: 決定的な静的解析。A8: なし。A9: なし（手作業の正解集合）。
- **判定: 「部分的に重なる」** — 「強制されない開発者の宣言」を「静的に推定した実効」と照合し、宣言の precision/recall を測った点が AuthGap の問いと同型。性質（ロック）と規模（15 本）が違う。「宣言の誤り」と「宣言の欠落」を両方数えた設計は AuthGap の両側比較の先例として引用できる。

#### [2-2] RacerD — Blackshear, Gorogiannis, O'Hearn, Sergey, "RacerD: Compositional Static Race Detection"（OOPSLA 2018）— 検証 ◎
- 出典: [PDF](https://research.facebook.com/file/236160615092435/RacerD-Compositional-Static-Race-Detection.pdf)
- A1 宣言: `@ThreadSafe`（とその別名）。論文の解釈は「Any non-private method m of C can be safely called in parallel with all other non-private methods of C and its subclasses, including m itself.」。`@ThreadSafe` は並行文脈で使われる証拠の 1 つとして扱われ、ロック使用などからも並行文脈を推論する ([PDF](https://research.facebook.com/file/236160615092435/RacerD-Compositional-Static-Race-Detection.pdf))。
- A2/A3: 合成的な手続き間抽象解釈（ロック数、スレッド、所有権のドメイン）。A4: Java。
- A5: 「minimizing false positives」を優先する設計で、健全性より高確度の報告を選んでいる。未解決の扱いの率は報告されていない。
- A6: Facebook に配備。「over 2500 concurrency issues it has flagged have been fixed by engineers before reaching production」「The fix rate over the last six months was 50%.」([PDF](https://research.facebook.com/file/236160615092435/RacerD-Compositional-Static-Race-Detection.pdf))
- A7: 決定的。A8: なし。A9: 開発者の修正率を有効性の指標に使っている（修正コミットを正解の分母にはしていない）。
- **判定: 「隣接」** — 宣言（`@ThreadSafe`）を照合の起点にするが、宣言の正誤そのものの率は出していない。

#### [2-3] Rudra — Bae, Kim, Askar, Lim, Kim, "RUDRA: Finding Memory Safety Bugs in Rust at the Ecosystem Scale"（SOSP 2021）— 検証 ◎
- 出典: [PDF](https://taesoo.kim/pubs/2021/bae:rudra.pdf)
- A1 宣言: `unsafe impl Send/Sync`。開発者がスレッド安全性を宣言し、コンパイラはそれを信用する（検査しない）。例は CVE-2020-35905（futures の `MappedMutexGuard` の Send/Sync 境界の誤り）([PDF](https://taesoo.kim/pubs/2021/bae:rudra.pdf))。
- A2: Send/Sync Variance（SV）検査器が、ジェネリック型の Send/Sync 境界と API の振る舞い（`&T` を渡すか `T` を移すか等）の食い違いを HIR/MIR 上で見る。A4: Rust。
- A5: precision を high/med/low の 3 段で調整できる。報告の偽陽性率は段ごとに出しているが、未解決の率は出していない。
- A6: crates.io の全 43k パッケージ（2020-07-04 時点）を 6.5 時間で走査した。SV は high で 367 件報告・178 バグ（48.5%）、low で 1,176 件・308 バグ（26.2%）。全体では 264 件の新規バグ、76 件の CVE、112 件の RustSec advisory ([PDF](https://taesoo.kim/pubs/2021/bae:rudra.pdf))。
- A7: 決定的。A8: なし。A9: なし（手作業トリアージと報告による）。
- **判定: 「隣接」** — 「コンパイラが信用する安全性の宣言」を生態系全体で照合した先例。母集団全数の走査、精度段階ごとの真陽性率の報告という評価の形は AuthGap の参考になる。性質は副作用ではない。

#### [2-4] Eyolfson & Lam, "C++ const and Immutability: An Empirical Study of Writes-Through-const"（ECOOP 2016）— 検証 ◎（要旨・序論）
- 出典: [LIPIcs](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2016.8)
- A1: C++ の `const`（言語が一部強制するが、`mutable` やキャストで迂回できる）。A2: **動的**ツール ConstSanitizer が「dynamically verifies a stricter form of immutability than that defined in C++」。A6: ベンチマーク 7 本で 17 の書き込みの類型を見つけ、「Over half of these seem unnecessary to us.」([LIPIcs](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2016.8))。成果物ページの要旨は 8 本としていて、本数が食い違う（検索結果の要約による。△ — [DARTS 成果物](https://drops.dagstuhl.de/entities/document/10.4230/DARTS.2.1.3)）。
- **判定: 「隣接」**（動的。宣言は部分的に強制される）。

#### [2-5] Rak-amnouykit, McCrevan, Milanova, Hirzel, Dolby, "Python 3 Types in the Wild: A Tale of Two Type Systems"（DLS 2020）— 検証 ◎
- 出典: [PDF](https://www.cs.rpi.edu/~milanova/docs/dls2020.pdf)
- A1: PEP 484 の型注釈（実行時には強制されない助言的な宣言）。A2: MyPy と PyType で静的に検査する。A4: Python。
- A5: 解析できないリポジトリ（malformed 195 本）は除いたうえでフラグで対処している。
- A6: GitHub の 70,826 リポジトリのうち型注釈があるのは 2,678 本。「Only 318, or 15%, of the 2,678 repositories are type correct in MyPy」。エラーは計 41,607 件で、import 以外が 22,556 件。手作業で分類したエラーのうち MyPy の約 49% は偽陽性 ([PDF](https://www.cs.rpi.edu/~milanova/docs/dls2020.pdf))。
- A7: 決定的。A8: なし。A9: なし。
- **判定: 「隣接」** — 助言的な宣言を Python の母集団で静的に照合した先例。「宣言は書かれていても、検査すると大半が通らない」という知見は AuthGap の動機づけに使える。ただし偽陽性が約半分ある点も併記すべき。

#### 参照のみ（研究が見つからなかったもの）
- JetBrains `@Contract(pure = true)`: 公式文書は「The pure attribute is intended for methods that do not change the state of their objects, but just return a new value」と書き、「Result of method call ignored」インスペクションのヒントになりうるとする ([IntelliJ IDEA 2017.1 Help](https://www.jetbrains.com/help/idea/2017.1/contract-annotations.html))。誤用率の研究は見つからなかった。
- Solidity の `view`/`pure`: コンパイラが強制するが、inline assembly で迂回されうる。Chaliasos らの OOPSLA 2022 は、inline assembly がソース水準の静的解析器の効果を大きく制限すると要旨で述べる（検索結果の要約による。△ — [UCL Discovery](https://discovery.ucl.ac.uk/id/eprint/10182353/)）。`view` 違反の検出器を母集団で測った研究は見つからなかった。

### Inferences
- 「強制されない宣言は間違っている」という一般命題には、ロック（[2-1]）、型（[2-5]）、コメント（[4-2]）、文書（[4-1]）で実証がある。AuthGap は「MCP の hint も同じ性質を持つ」と位置づけられる。ただし純粋性・副作用の注釈そのものの誤り率を測った先行研究は見つからなかった。主張の余地はあるが、検索の網羅性には限界がある（Gaps 参照）。
- [2-1] の「programmer-written の precision と recall を、手作業の goal set に対して別々に出す」という評価の形は、AuthGap の「宣言 D の誤り」と「宣言の欠落」を分けて数える設計とほぼ同じ。比較の土台として引用するのがよい。

### Gaps
- `@Pure`・`@SideEffectFree`・C# の `[Pure]`・Kotlin の `@Contract(pure=true)`・`@CheckReturnValue`・`functools.cache`（不純関数のキャッシュ）の誤用率の実証研究は見つからなかった（クエリ: `empirical study developer purity annotations incorrect @Pure ...`、`Kotlin @Contract pure=true ... OR "functools.cache" impure ...`、`Code Contracts [Pure] attribute unchecked purity misuse ...`）。Code Contracts 周辺では Schiller et al.（Code Contracts の利用調査）、Estler et al.「Contracts in Practice」、ContractOk の修論が見つかったが、`[Pure]` には特化していない（検索結果の要約による。△）。
- ReIm/ReImInfer（OOPSLA 2012）などの純粋性推論研究が、開発者の既存注釈と比較しているかは確認していない（未検索）。

## 3. クラウド / インフラ / プラットフォームの権限 — 宣言された権限とコードから推定した必要権限の照合

### Takeaway
最も近い系統で、先行研究は多く新しい。**PrivLess（arXiv 2607.02875, 2026）は AuthGap と手法の骨格がほぼ同じ**で、関数の入口ごとに call graph を作り、コードから必要な操作を静的に取り出して、宣言（`serverless.yml` の IAM 文）と集合差を取る。Python を含む 789 アプリで測定している。EPScan（S&P 2025）は Kubernetes の RBAC について同じことを Go のコード（CodeQL）＋LLM で行う。SmartThings（S&P 2016）、Chrome 拡張（IJIS 2022）、COPES（2012）も同じ形の先例。**ただし宣言側がどれも「強制される権限」なので、測れるのは過大宣言（over-privilege）の方向だけ**になる。PrivLess は設計上「宣言は機能する」と仮定し、宣言にない推定権限を捨てる。AuthGap の中心である「宣言のほうが安全側に嘘をつく」方向（readOnlyHint=true なのに書く）は、この系統では原理的に見えない。

### Cited Findings

#### [3-1] PrivLess — Yeboah-Duako & Datta, "Permissions on the Loose: Measuring Overprivilege in Real-World Serverless Applications"（arXiv 2607.02875v2, 2026-09-08 改訂, 査読前）— 検証 ◎
- 出典: [arXiv](https://arxiv.org/abs/2607.02875)
- A1 宣言: Serverless Framework の設定ファイルに書かれた IAM 文（`iamRoleStatements`）。AWS IAM が強制する。グローバル（全関数共通）か関数ごとかを区別する ([arXiv](https://arxiv.org/abs/2607.02875))。
- A2 実効: 「a static policy analysis framework that extracts function-to-resource interactions from application source code, derives an interaction-permission mapping, and reconciles inferred interactions with declared policies to quantify overprivilege.」SDK のメソッドを IAM アクションに写す知識ベースを 6 つの戦略（命名規則、docstring の regex、Smithy の注釈、ヒューリスティック、Authorization Reference、managed policies）の重み付き投票で作る ([arXiv](https://arxiv.org/abs/2607.02875))。
- A3: 「for each function, we construct a call graph to identify dependent functions and modules, ensuring that privileges required by such functions or inter-procedural calls are properly attributed to the entry function」。深さの上限は書かれていない。実装は CodeQL ([arXiv](https://arxiv.org/abs/2607.02875))。
- A4: JavaScript/TypeScript 622、Python 151、Go 16 アプリ ([arXiv](https://arxiv.org/abs/2607.02875))。
- A5 未解決: (i) リソース ID が解決できなければ環境変数名などを残す（「by preserving unresolved environment variables in the policy」）。(ii) **Pass 1 で「Any permission in R_f not covered by Ĝ_f is evicted」とし、「This bounds the inferred set strictly by developer intent, given the assumption that developer-defined permissions are functional」と書く**。(iii) Pass 2 で「To recover implicit permissions that are opaque to static analysis」と、宣言側の権限を条件つきで必要集合に戻す。(iv) 限界として、third-party SDK ラッパー（例 dynamoose）と、SDK を通らない直接 HTTP 呼び出しを取り逃すと明記している。**未解決の率は報告していない**。解析パイプラインが完走しなかったアプリは 886 本中 97 本（10.95%）で、これは除外した ([arXiv](https://arxiv.org/abs/2607.02875))。
- A6: 3,363 アプリのデータセットから 789 アプリ・1,293 関数。「47.7% of applications carry excess permissions with a significant privilege reduction potential of 99.65%」。正解は 5 アプリの機能試験（LocalStack と実 AWS で縮小ポリシーを適用して呼び出す、負の対照つき）で、「PrivLess preserved baseline functionality in 29/31 (94%) functions on LocalStack and 21/31 (68%) functions on AWS」([arXiv](https://arxiv.org/abs/2607.02875))。**論文内の食い違い**: 序論は「an average of 418.75 permissions while requiring only 1.55」、§7.2 は「The mean granted was 683.37 versus 2.40 required (285×)」と書いている ([arXiv](https://arxiv.org/abs/2607.02875))。
- A7: CodeQL ＋ Python。LLM は使っていない。決定論の明記はない。A8: なし。A9: なし。
- **判定: 「大きく重なる」** — 「入口ごとの call graph → 静的に推定した必要集合 ↔ 宣言集合の差 → 野外母集団での率」という骨格は AuthGap と同じ。違いは 3 点。(1) 宣言が強制される権限なので、照合が「宣言 ⊇ 必要」を前提にし、過小宣言を構造上捨てている。(2) 未解決を率として数えず、宣言から補う。(3) 事前登録・凍結・修正コミットがない。**AuthGap は必ず引用し、この 3 点で差を書くべき**。

#### [3-2] EPScan — Gu, Tan, Zhang, Gao, Yang, "EPScan: Automated Detection of Excessive RBAC Permissions in Kubernetes Applications"（IEEE S&P 2025）— 検証: 論文の数値は △、コードは ◎
- 出典: [IEEE Xplore](https://ieeexplore.ieee.org/document/11023379/)（本文は取得できなかった）; [SNU セミナー要約](https://mmlab.snu.ac.kr/community/seminar/2025-08-27-epscan-automated-detection-of-excessive-rbac-permissions-in-kubernetes-applications); [GitHub seclab-fudan/EPScan](https://github.com/seclab-fudan/EPScan)（commit `ca258dfd`, 2025-05-14 を scratchpad に clone して読んだ）
- A1 宣言: Pod の設定にある RBAC（ServiceAccount / ClusterRole）。Kubernetes が強制する ([SNU](https://mmlab.snu.ac.kr/community/seminar/2025-08-27-epscan-automated-detection-of-excessive-rbac-permissions-in-kubernetes-applications))。
- A2 実効: 「pod-oriented program analysis」で各 Pod のプログラムが行うリソースアクセスを特定し、設定の権限と比べる ([SNU](https://mmlab.snu.ac.kr/community/seminar/2025-08-27-epscan-automated-detection-of-excessive-rbac-permissions-in-kubernetes-applications))。コードでは CodeQL（`--language=go`）で client-go / lister / informer の API 呼び出し点を取り出している ([GitHub](https://github.com/seclab-fudan/EPScan))。
- A3: 未確認（論文本文を読めていない）。A4: Go。
- A5: 未確認。
- A6: CNCF の第三者アプリ 108 本。50 アプリの 106 Pod で未知の悪用可能な過剰権限を見つけ、precision 94.6%、CVE 9 件 ([SNU](https://mmlab.snu.ac.kr/community/seminar/2025-08-27-epscan-automated-detection-of-excessive-rbac-permissions-in-kubernetes-applications))。（△: セミナー要約の数値で、一次資料では未確認）
- A7: **非決定的な部品がある**。コンテナイメージの起動スクリプトから実行ファイルの位置を探す `_list_paths_by_llm` が `openai_helper.completion_with_type(prompt, resp_type=list, temperature=0.6)` を呼ぶ（規則ベースの抽出と併用）([GitHub](https://github.com/seclab-fudan/EPScan))。A8: 不明。A9: 不明。
- **判定: 「部分的に重なる」** — 宣言（RBAC）と静的に推定した API 利用の照合で、骨格は同じ。宣言は強制され、方向は過剰だけ。Pod とソースの対応づけに LLM（temperature 0.6）を使う点で、AuthGap の「判定に LLM を入れない決定論」と対照になる。

#### [3-3] Yang et al., "Take Over the Whole Cluster: Attacking Kubernetes via Excessive Permissions of Third-party Applications"（CCS 2023）— 検証 ◎
- 出典: [PDF](https://www.cs.wm.edu/~smherwig/readings/papers/23-ccs-kubernetes_excessive_permissions.pdf)
- A1: 第三者アプリの RBAC。A2: **コードからの必要権限の推定はしていない**。手順は「(1) installing each third-party app manually, (2) identifying critical applications automatically, and (3) launching attacks manually.」。重要な DaemonSet／コンポーネントの権限をスクリプトで走査し、攻撃は手で実行した ([PDF](https://www.cs.wm.edu/~smherwig/readings/papers/23-ccs-kubernetes_excessive_permissions.pdf))。
- A6: 「51 of 153 (33.3%) CNCF projects have potential security risks」。報告した 51 件のうち 32 件が応答し、「10 of them confirm our reports and fix their source code, and 8 CVEs are assigned」([PDF](https://www.cs.wm.edu/~smherwig/readings/papers/23-ccs-kubernetes_excessive_permissions.pdf))。
- A9: 修正の具体例として「OpenFeature removed the unnecessary "update" verb」などを挙げる。修正は事後の確認に使っているだけで、正解の分母ではない ([PDF](https://www.cs.wm.edu/~smherwig/readings/papers/23-ccs-kubernetes_excessive_permissions.pdf))。
- **判定: 「隣接」**（攻撃可能性の研究で、宣言と実効の照合はしない）。

#### [3-4] Fernandes, Jung, Prakash, "Security Analysis of Emerging Smart Home Applications"（IEEE S&P 2016, SmartThings）— 検証 ◎
- 出典: [PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf); [Microsoft Research ページ](https://www.microsoft.com/en-us/research/publication/security-analysis-emerging-smart-home-applications/)
- A1 宣言: SmartApp が要求する capability（プラットフォームが強制する）。
- A2 実効: Groovy のソースを静的に解析し、使っている command / attribute を集める。「For each SmartApp, we compute the difference between the set of requested commands and attributes and the set of used commands and attributes.」capability の完全な一覧は、非公開の REST エンドポイントに 64 個の骨組みデバイスハンドラを問い合わせて得た ([PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf))。
- A4: Groovy。バイトコード解析は「Groovy's extremely dynamic nature」のため断念した（「The Groovy compiler converts every direct method call into a reflective one.」）([PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf))。
- A5 未解決: **動的メソッド呼び出しを検出したら手作業解析に回す**（「Our tool flags a SmartApp for manual analysis when it detects dynamic method invocation. 26 SmartApps were flagged as such.」）。同名の独自メソッドも 7 本を手作業に回した。そのうえで「our analysis is conservative and elects to mark SmartApps as not overprivileged if it cannot determine reliably whether overprivilege exists」([PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf))。**判定できないものは違反なし側に倒す**（AuthGap の規則 4 とは逆の扱い）。
- A6: 499 SmartApp。Table IV は coarse-grained capability による過剰が 276（55%）、coarse binding が 213（43%）。本文は「over 42%」と書いていて、表と 1 ポイント食い違う。偽陽性率は「24 apps were marked as overprivileged, representing a false positive rate of 4.8%」([PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf))。
- A7: 静的解析は決定的とみられる。A8: なし。A9: なし。
- **判定: 「部分的に重なる」** — 宣言と使用の集合差を母集団で測り、動的呼び出し（未解決）を数えて手作業に回した点が AuthGap の opaque の扱いに最も近い先例。ただし未解決は最終的に「違反なし」へ倒している。

#### [3-5] Picazo-Sanchez, Ortiz-Martin, Schneider, Sabelfeld, "Are Chrome extensions compliant with the spirit of least privilege?"（International Journal of Information Security 21(6), 2022）— 検証 ◎
- 出典: [PDF](https://www.cse.chalmers.se/~andrei/ijis22.pdf); [DOI](https://doi.org/10.1007/s10207-022-00610-w)
- A1 宣言: manifest の `permissions` / `optional_permissions`（ブラウザが強制）。A2 実効: Esprima の AST で `chrome.*` の API 呼び出しを取り出し（別名代入 `var aux = chrome; ...` も再構成する）、HTML は正規表現で見る。「Definition 2 An extension is overprivileged when there is at least one permission in its manifest file whose API is not defined in the source code of the extension at installation time.」([PDF](https://www.cse.chalmers.se/~andrei/ijis22.pdf))
- A3: 手続き間の到達は見ていない（API 名の出現で判定している）。A4: JavaScript。
- A5: 「our analysis does not consider complex forms of obfuscation, external code execution, or extensions that use code generation functions like eval() and setTimeout().」**未解決は黙って範囲外にしている**（率は出していない）([PDF](https://www.cse.chalmers.se/~andrei/ijis22.pdf))。
- A6: 136,018 のブラウザ拡張のうち SoLP 準拠は 55,548（40.8%、Table 4）。underprivileged は 8.5%。**論文内の食い違い**: 要旨は 39.8%、序論は 37.8%、表は 40.8% ([PDF](https://www.cse.chalmers.se/~andrei/ijis22.pdf))。正解との突き合わせはない。
- A7: 決定的。A8: なし。A9: なし。
- **判定: 「部分的に重なる」** — 宣言と使用の照合を 13 万本規模で行った。ただし解析は構文的な出現で、未解決（eval 等）は除外し、正解の検証がない。

#### [3-6] COPES — Bartel, Klein, Monperrus, Le Traon, "Automatically Securing Permission-Based Software by Reducing the Attack Surface: An Application to Android"（ASE 2012 / arXiv TR 1206.5829）— 検証 ◎（TR 版）
- 出典: [arXiv 1206.5829](https://arxiv.org/abs/1206.5829)
- A1: AndroidManifest の宣言権限（強制される）。A2: フレームワークの入口ごとの call graph（Soot/Spark, context-insensitive）から権限チェックへの到達を求めて API→権限の写像を作り、アプリが呼ぶ API から必要権限を出す。「the permission gap as the difference between the declared permissions and the required permission」([arXiv](https://arxiv.org/abs/1206.5829))。
- A6: 「We evaluate our approach on 742+679 Android applications and we show that 94+35 applications suffer from a permission gap.」予備調査では「There are 7/82 applications that declare CAMERA while not using it」とし、manifest を書き換えて再実行し偽陽性を確かめた ([arXiv](https://arxiv.org/abs/1206.5829))。
- **判定: 「部分的に重なる」**（Stowaway・PScout と同系統の代表として 1 件だけ挙げる。過大宣言の方向のみ）。

#### [3-7] Koishybayev et al., "Characterizing the Security of GitHub CI Workflows"（USENIX Security 2022）— 検証 ◎
- 出典: [PDF](https://par.nsf.gov/servlets/purl/10426381); [USENIX](https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev)
- A1: workflow の `permissions:`。A2: **コードからの必要権限の推定ではない**。99.8% という数字は、既定が write で、宣言がほとんど書かれていないことから来ている。「only 0.2% of all workflows (900/447K) use the permissions field ... even in these 900 workflows, only 62% of them set the permission to the desired read-only.」([PDF](https://par.nsf.gov/servlets/purl/10426381))
- A6: 447,238 workflow、213,854 リポジトリ。「99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository.」([PDF](https://par.nsf.gov/servlets/purl/10426381))
- **判定: 「隣接」** — 頻繁に引用されるが、宣言と実効の照合ではなく「宣言の不在」の測定。Granite（[3-10]）はこの 99.8% を「overprivileged」の根拠として引いている。

#### [3-8] Palo Alto Networks Unit 42 / Prisma Cloud, "Third-Party GitHub Actions: Effects of an Opt-Out Permission Model"（ブログ, 2023-08-16, Yaron Avital）— 検証 ○（査読なし）
- 出典: [ブログ](https://www.paloaltonetworks.com/blog/cloud-security/github-actions-opt-out-permissions-model.md)
- A2: 社内ツール PiPER が「performing static code analysis on the actions' code」で GitHub API 呼び出しを権限に写す。人気上位 1,000 個の action を対象にした ([ブログ](https://www.paloaltonetworks.com/blog/cloud-security/github-actions-opt-out-permissions-model.md))。
- A6: スター上位 2,000 プロジェクト（約 6,000 workflow、1,045 action）。「93%」のリポジトリが過剰に許可した workflow を少なくとも 1 本持つ。権限を書かない 80% のうち 86% が過剰、粒度を指定した側でも 36% が過剰 ([ブログ](https://www.paloaltonetworks.com/blog/cloud-security/github-actions-opt-out-permissions-model.md))。
- **判定: 「部分的に重なる」**（静的な宣言と実効の照合を母集団で行っているが、ベンダーのブログで、方法の詳細と正解の検証が公開されていない）。

#### [3-9] Decap — Hasan, Ghavamnia, Polychronakis, "Decap: Deprivileging Programs by Reducing Their Capabilities"（RAID 2022）— 検証 ◎（要旨・序論）
- 出典: [PDF](https://par.nsf.gov/servlets/purl/10422548)
- 「a binary code analysis tool that automatically deprivileges programs by identifying the subset of capabilities they require based on the system calls they may invoke」。setuid（＝全特権の宣言）に対し、必要な capability を syscall から推定する。A6: Ubuntu の setuid プログラム 201 本で、半数が 16 未満の capability で足り、69% が CAP_SYS_ADMIN を避けられる ([PDF](https://par.nsf.gov/servlets/purl/10422548))。
- **判定: 「隣接」**（宣言は「全部」なので照合というより最小化）。

#### [3-10] Granite — Moazen, Ahmadian, Balliu, "Granite: Granular Runtime Enforcement for GitHub Actions Permissions"（arXiv 2512.11602, 2025-12）— 検証 ◎（該当節）
- 出典: [arXiv](https://arxiv.org/abs/2512.11602)
- 実行時のプロキシで step 単位に強制する。静的解析による最小権限推定（StepSecurity の knowledge base）には「suffer by the lack of contextual information」と否定的 ([arXiv](https://arxiv.org/abs/2512.11602))。A6: 500 workflow（12,916 job）。要旨は「52.7% of the jobs can be protected」、序論は「overprivileged jobs are prevalent (46.6%)」と書く（指標が異なるとみられる）([arXiv](https://arxiv.org/abs/2512.11602))。
- **判定: 「隣接」**（動的な強制）。

#### 参照のみ
- ALPS（arXiv 2603.25393）: サーバーレス向けの静的解析と fine-tuned LLM で最小権限を抽出・強制する。8,322 関数で抽出の coverage 94.8%。宣言との差の測定ではなく生成と強制 ([arXiv](https://arxiv.org/abs/2603.25393))。判定「隣接」。
- Dunlap, Enck, Reaves, "A Study of Application Sandbox Policies in Linux"（SACMAT 2022）: Flatpak と Snap の両方にある 283 アプリについて、2 つのストアのポリシー同士を比べた（コードとは照合しない）。「we frequently found policy mismatches」([PDF](https://par.nsf.gov/servlets/purl/10356733))。判定「隣接」。
- Kubernetes Operator の cross-namespace 参照（arXiv 2507.03387、NDSS 2026 とされる）は「necessary permissions ... may still be exploited」と、最小化後も残る危険を扱う（検索結果の要約による。△ — [arXiv](https://arxiv.org/html/2507.03387v2)）。

### Inferences
- 骨格（API→権限の写像 ＋ 静的な呼び出し抽出 ＋ 宣言との集合差 ＋ 野外の率）は 2011 年の Stowaway から 2026 年の PrivLess まで続く確立した系統。**AuthGap はこの骨格そのものを新規性にできない**。
- **方向の非対称**: 宣言が強制される系統では、宣言が少なすぎると動かなくなり、すぐ直される。だから測られるのは過大宣言だけになる。PrivLess の Pass 1 はそれを前提として明文化している ([arXiv](https://arxiv.org/abs/2607.02875))。MCP の ToolAnnotations は強制されないので、「安全側への嘘」（readOnlyHint=true で書く、destructiveHint=false で削除する）が残り続けうる。AuthGap の新規性はこの「助言的な宣言の過小申告方向」にある、と整理するのが最も防御しやすい。
- **未解決の扱いの分類**（読んだ範囲）: (a) 黙って範囲外にする（Chrome 拡張の eval 等）、(b) 手作業に回したうえで違反なし側に倒す（SmartThings）、(c) 宣言から補う（PrivLess の Pass 2）、(d) 解析失敗をデータセットから除く（PrivLess 10.95%、DLS 2020 の malformed 195 本）。**ユニットごとの未解決率を主要な指標として報告した例は、読んだ範囲では見つからなかった**。AuthGap の `opaque(reason)` と率の報告は差別化点として書ける（網羅性の限界を併記すること）。
- **決定論**: 近年の 2 件（EPScan, ALPS）はパイプラインの一部に LLM を入れている。EPScan は temperature 0.6 ([GitHub](https://github.com/seclab-fudan/EPScan))。「判定に LLM を入れない」は対比として明示する価値がある。

### Gaps
- EPScan の本文（手続き間の深さ、未解決の扱い、precision の算出法）は取得できなかった（IEEE Xplore と computer.org は本文なし、Fudan のページは 404 / 接続リセット）。数値はセミナー要約（△）。
- Axplorer（USENIX Security 2016）・Dynamo（NDSS 2021）など Android の権限写像の後続は、検索で一次資料が出なかったので扱っていない（クエリ: `Axplorer Android permission specification over-privileged apps USENIX Security 2016 Dynamo NDSS 2021`）。
- Deno の権限や WASI capability を静的に推定して宣言と比べる研究は見つからなかった。npm には manifest と `require` から権限を推定する arXiv 2103.05769 がある（検索結果の要約による。△ — [arXiv](https://arxiv.org/pdf/2103.05769)）。Deno の攻撃研究（"Welcome to Jurassic Park", NDSS 2025）は推定ツールではない（△ — [Thinkst](https://citation.thinkst.com/talk/95791)）。
- Docker や Linux の capability の宣言とコンテナ内コードを照合する研究は Decap 以外に見つからなかった。Slack アプリの OAuth スコープの過剰を測った学術研究も見つからなかった（クエリ: `Slack apps OAuth scopes over-privileged static analysis measurement ...`）。
- AWS Lambda の最小権限について Gill（Waterloo 修論, 2020）は実験的な探索法で「the vast majority of policies are over-privileged」とした（検索結果の要約による。△ — [UWSpace](https://uwspace.uwaterloo.ca/handle/10012/16586)）。

## 4. ドキュメント・コメントと実装の不一致（副作用・例外・制約）

### Takeaway
「文書やコメントが宣言する振る舞い」と「静的に推定した実装の振る舞い」を照合し、母集団で不一致の数を出した先例はある。最も構造が近いのは Rubio-González & Liblit（PASTE 2010）で、man ページが宣言するエラーコードと、52 のファイルシステムの実装から手続き間解析（WPDS）で求めた実際のエラーコードを照合した。iComment（SOSP 2007）は「不一致はバグか悪いコメントのどちらか」という両側の解釈を最初に明示した。ただし**「副作用がない」と書いた docstring を実装と照合する研究は見つからなかった**。

### Cited Findings

#### [4-1] Rubio-González & Liblit, "Expect the Unexpected: Error Code Mismatches Between Documentation and the Real World"（PASTE 2010）— 検証 ◎
- 出典: [論文ページ](https://pages.cs.wisc.edu/~liblit/paste-2010/)（PDF もここから取得）
- A1 宣言: Linux の man ページ（v2.39）が各 syscall について列挙するエラーコード（文書なので強制されない）。
- A2 実効: 「We use static program analysis to identify the error codes returned by system calls across 52 file systems」。A3: 手続き間のデータフロー解析を weighted pushdown system で行う（keywords: 「interprocedural dataflow analysis, weighted pushdown systems」）([論文](https://pages.cs.wisc.edu/~liblit/paste-2010/))。
- A4: C（Linux カーネル）。
- A5: 偽陽性の可能性を明記している。「It is also possible that implementation and documentation are both correct, but that our analysis claims an error code can be returned when it actually cannot.」率は出していない ([論文](https://pages.cs.wisc.edu/~liblit/paste-2010/))。
- A6: 42 の syscall × 52 のファイルシステム。重複除去後で「1,784 undocumented error-code instances」。除去しなければ 4,565 件 ([論文](https://pages.cs.wisc.edu/~liblit/paste-2010/))。正解との突き合わせはない。
- 両側の解釈: 多くのファイルシステムが同じ未文書コードを返すなら文書の不足、少数だけなら実装の誤り、と分けている（「When many file systems return the same undocumented error for a given system call, this hints that the documentation may be incomplete」）([論文](https://pages.cs.wisc.edu/~liblit/paste-2010/))。
- A7: 決定的。A8: なし。A9: なし。
- **判定: 「部分的に重なる」** — 「入口（syscall）ごとに、宣言（文書）と手続き間で推定した実効を照合し、母集団で数える」という形が AuthGap と同型。宣言の対象は副作用ではなくエラーコード。

#### [4-2] iComment — Tan, Yuan, Krishna, Zhou, "/* iComment: Bugs or Bad Comments? */"（SOSP 2007）— 検証 ◎（要旨・評価）
- 出典: [PDF](https://www.cs.purdue.edu/homes/lintan/publications/icomment_sosp07.pdf)
- A1 宣言: 自然言語コメントに書かれた規則（例「caller must hold lock X」）。A2: NLP と機械学習で規則を抽出し、静的解析（フロー非依存のポインタ別名解析を含む）でコードと照合する ([PDF](https://www.cs.purdue.edu/homes/lintan/publications/icomment_sosp07.pdf))。A4: C/C++（Linux, Mozilla, Wine, Apache）。
- A6: 「extracts 1832 rules from comments with 90.8-100% accuracy and detects 60 comment-code inconsistencies, 33 new bugs and 27 bad comments ... Nineteen of them (12 bugs and 7 bad comments) have already been confirmed by the corresponding developers」。偽陽性率 38.8% ([PDF](https://www.cs.purdue.edu/homes/lintan/publications/icomment_sosp07.pdf))。
- A7: 規則抽出は学習モデルに依存する。A8: なし。A9: なし（開発者の確認）。
- **判定: 「部分的に重なる」** — 宣言（コメント）と実装の不一致を「実装のバグ」と「宣言の誤り」の両方として扱った先例。AuthGap が矛盾を「宣言が嘘」か「実装が想定外」かの両側で記述するときの引用先になる。

#### [4-3] DRONE — Zhou, Gu, Chen, Huang, Panichella, Gall, "Analyzing APIs documentation and code to detect directive defects"（ICSE 2017）／TSE 版 "Automatic detection and repair recommendation of directive defects in Java API documentation"— 検証 ○
- 出典: [Middlesex リポジトリ](https://repository.mdx.ac.uk/item/87050); [TSE 版 PDF](https://srv-clst-301-data66.zhaw.ch/bitstream/11475/17312/1/tse18.pdf)
- A1: Javadoc の引数制約と例外宣言。A2: プログラム理解、NLP、一階論理の制約ソルバで照合する。A4: Java（JDK 1.8）。A6: 約 2,000 の API 利用制約から 1,158 件の欠陥ディレクティブを検出し、precision 81.6%、recall 82.0%（検索結果に出た要旨による）([Middlesex](https://repository.mdx.ac.uk/item/87050))。
- **判定: 「隣接」**（制約・例外の文書と実装の照合。副作用は対象外）。

#### [4-4] Kechagia, Fragkoulis, Louridas, Spinellis, "The exception handling riddle: An empirical study on the Android API"（JSS 142, 2018）— 検証 ○
- 出典: [TU Delft ページ](https://serg.ewi.tudelft.nl/publications/the-exception-handling-riddle-an-empirical-study-on-the-android-api)
- 要旨（検索結果に出たもの）: Android API の 10 版（14–23）と 3,539 アプリを静的に解析し、コードが投げうる例外と文書の例外の食い違いを探した。901,274 件のクラッシュと照合し、静的解析で見つかる未文書例外の約 10% がクラッシュとして現れた ([TU Delft](https://serg.ewi.tudelft.nl/publications/the-exception-handling-riddle-an-empirical-study-on-the-android-api))。
- **判定: 「隣接」** — 外部の観測（クラッシュ）で静的照合の結果を裏づける手順は参考になる。

### Inferences
- 文書と実装の照合の系統は、宣言を「機械可読な宣言」に限らない点で AuthGap より広い。AuthGap の宣言（ToolAnnotations）は機械可読な真偽値なので、NLP の誤差（iComment の 38.8%、DRONE の 81.6%）が入らない。この点は AuthGap の測定上の利点として書ける。
- [4-1] の「多くの実装が同じ食い違いを示せば文書が悪い、少数なら実装が悪い」という推論は、MCP で SDK やテンプレートに由来する系統的な誤宣言を見分けるのに転用できる可能性がある（推論。検証していない）。

### Gaps
- 「This function has no side effects」「read-only」と書いた docstring やコメントを実装と照合する研究は見つからなかった。
- 機械学習で Just-In-Time にコメントの陳腐化を検出する系統（Panthaplackel et al. AAAI 2021、Liu et al. TSE 2021、CCISolver、DocPrism arXiv 2511.00215 など）は今回は読んでいない。副作用を対象にしたものは検索に出なかった。
- `@tComment`（ICST 2012）は Wen et al.（[5-2]）の関連研究節で「detects inconsistencies between Javadoc comments related to null values and exceptions」と紹介されているが、一次資料は読んでいない（△ — [Wen et al.](https://www.inf.usi.ch/faculty/lanza/PUBS/P/Wen2019a.pdf)）。

## 5. 開発者の修正コミット（権限の削除、注釈の訂正）を recall の正解に使った研究

### Takeaway
**宣言の修正コミットを静的検査器の recall の分母（正解集合）に使った研究は、読んだ範囲では見つからなかった**。近いのは次の 3 つの型である。(a) 静的ツールを全コミットに当てて問題の導入と消失を追う（Scoccia et al. SCAM 2019。ただし「修正」の判定がツール自身の出力に依存する）。(b) キーワードで集めた修正コミットを手で読み、分類体系を作る（Wen et al. ICPC 2019）。(c) 報告後の開発者の修正・確認を precision の傍証に使う（Yang et al. CCS 2023、RacerD の修正率 50%、Flux の 8 件確認、iComment の 19 件確認）。AuthGap の「アノテーション修正コミットでの recall」はこれらと設計が違い、差別化点として書ける（網羅性の限界は Gaps に書く）。

### Cited Findings

#### [5-1] Scoccia, Peruma, Pujols, Malavolta, Krutz, "Permission Issues in Open-source Android Apps: An Exploratory Study"（SCAM 2019）— 検証 ◎（同内容の博士論文 第 6 章で読んだ）
- 出典: [Scoccia 博士論文 PDF（GSSI）](https://iris.gssi.it/bitstream/20.500.12571/9688/1/2019_Scoccia.pdf)
- A1: AndroidManifest の権限（over / under-permission）と、実行時権限の使い方の smell（missing check, multiple requests in proximity）。
- A2: 既存の静的ツール M-Perm と P-Lint を履歴の各コミットに当てた。「we used them to analyze all 502,907 commits belonging to the 574 apps in our dataset」([PDF](https://iris.gssi.it/bitstream/20.500.12571/9688/1/2019_Scoccia.pdf))。
- ツールの妥当性確認: 10 本の合成アプリで「obtained a value of 1.00 for both precision and recall. Although largely elementary」と自ら限界を認めている ([PDF](https://iris.gssi.it/bitstream/20.500.12571/9688/1/2019_Scoccia.pdf))。
- A6: 「about 50% of examined apps exhibit at least one PRI, with over-permissions being the most recurrent one」。大半は数日で直るが、数年残るものもある ([PDF](https://iris.gssi.it/bitstream/20.500.12571/9688/1/2019_Scoccia.pdf))。
- A9: コミット履歴を使うが、**修正はツールの警告が消えたことで定義され、検査器の recall の正解にはしていない**。
- **判定: 「隣接」** — 「宣言の誤りが導入され直されるまでをコミット単位で追う」設計は、AuthGap の修正コミット収集の先行例として引用すべき。

#### [5-2] Wen, Nagy, Bavota, Lanza, "A Large-Scale Empirical Study on Code-Comment Inconsistencies"（ICPC 2019）— 検証 ◎
- 出典: [PDF](https://www.inf.usi.ch/faculty/lanza/PUBS/P/Wen2019a.pdf)
- 「mining 1.3 Billion AST-level changes from the complete history of 1,500 systems. Moreover, we manually analyzed 500 commits to define a taxonomy of code-comment inconsistencies fixed by developers.」500 件は「identified, via a keywords-matching mechanism, as likely related to the fixing of code-comment inconsistencies」([PDF](https://www.inf.usi.ch/faculty/lanza/PUBS/P/Wen2019a.pdf))。
- A9: 修正コミットを**分類体系づくりの材料**に使っていて、検出器の recall の分母ではない。
- **判定: 「隣接」**。

#### 横断: 修正や確認を評価に使った例（上の各項目から）
- Yang et al. CCS 2023: 報告した 51 件のうち 10 件が修正（例: OpenFeature の不要な「update」動詞の削除）([PDF](https://www.cs.wm.edu/~smherwig/readings/papers/23-ccs-kubernetes_excessive_permissions.pdf))。
- RacerD: 「The fix rate over the last six months was 50%.」修正率には「tax」があり（偽陽性がなくても約 30% は直されない）、と論じている ([PDF](https://research.facebook.com/file/236160615092435/RacerD-Compositional-Static-Race-Detection.pdf))。
- Flux: 12 件中 8 件を開発者が確認 ([PDF](https://www.usenix.org/system/files/osdi23-ding.pdf))。iComment: 60 件中 19 件を確認 ([PDF](https://www.cs.purdue.edu/homes/lintan/publications/icomment_sosp07.pdf))。
- Granite が引く GitHub Security Lab の actions-permissions（Monitor and Advisor）は、実行時に実際に使われた権限を観測して提案する動的ツールで、修正コミットを正解にはしていない ([Granite](https://arxiv.org/abs/2512.11602))。

### 全項目の判定一覧（25 件）

| ID | 研究 | 年・会議 | 宣言（強制） | 実効の導出 | 言語 | 判定 | 検証 |
|---|---|---|---|---|---|---|---|
| 3-1 | PrivLess | arXiv 2026 | IAM 文（強制） | CodeQL・call graph・SDK→権限 KB | JS/TS, Python, Go | 大きく重なる | ◎ |
| 1-1 | CodeQL `java/csrf-unprotected-request-type` | ツール | HTTP メソッド（助言） | GET ハンドラ→DB 更新の到達 | Java | 部分的に重なる | ○ |
| 2-1 | Ernst et al. locking | ICSE 2016 | `@GuardedBy`（助言） | 抽象解釈＋型検査 | Java | 部分的に重なる | ◎ |
| 3-2 | EPScan | S&P 2025 | RBAC（強制） | CodeQL（Go）＋LLM | Go | 部分的に重なる | △/コード◎ |
| 3-4 | SmartThings（Fernandes et al.） | S&P 2016 | capability（強制） | Groovy の静的解析 | Groovy | 部分的に重なる | ◎ |
| 3-5 | Chrome 拡張 SoLP | IJIS 2022 | manifest（強制） | AST での API 出現 | JS | 部分的に重なる | ◎ |
| 3-6 | COPES | ASE 2012 | manifest（強制） | Spark call graph | Java/Dalvik | 部分的に重なる | ◎ |
| 3-8 | Unit 42 PiPER | ブログ 2023 | `permissions:`（強制） | action コードの静的解析 | JS ほか | 部分的に重なる | ○ |
| 4-1 | Rubio-González & Liblit | PASTE 2010 | man ページ（文書） | WPDS による手続き間解析 | C | 部分的に重なる | ◎ |
| 4-2 | iComment | SOSP 2007 | コメント規則（文書） | NLP＋静的解析 | C/C++ | 部分的に重なる | ◎ |
| 1-2 | Flux | OSDI 2023 | （暗黙の冪等性要件） | 合成的検証 | Java | 隣接 | ◎ |
| 1-3 | Deemon | CCS 2017 | なし | 動的トレース | PHP | 隣接 | ◎ |
| 1-4 | APIdemic | POPL 2025 SRC | なし | 静的（状態遷移） | — | 隣接 | ○ |
| 2-2 | RacerD | OOPSLA 2018 | `@ThreadSafe`（助言） | 合成的抽象解釈 | Java | 隣接 | ◎ |
| 2-3 | Rudra | SOSP 2021 | `unsafe impl Send/Sync`（信用される） | HIR/MIR 解析 | Rust | 隣接 | ◎ |
| 2-4 | Eyolfson & Lam | ECOOP 2016 | `const`（一部強制） | 動的 | C++ | 隣接 | ◎ |
| 2-5 | Python 3 Types in the Wild | DLS 2020 | 型注釈（助言） | MyPy/PyType | Python | 隣接 | ◎ |
| 3-3 | Yang et al. K8s | CCS 2023 | RBAC（強制） | 手作業の攻撃 | — | 隣接 | ◎ |
| 3-7 | Koishybayev et al. | USENIX Sec 2022 | `permissions:`（強制） | 宣言の有無だけ | YAML | 隣接 | ◎ |
| 3-9 | Decap | RAID 2022 | setuid（全特権） | バイナリの syscall 解析 | バイナリ | 隣接 | ◎ |
| 3-10 | Granite | arXiv 2025 | `permissions:`（強制） | 実行時プロキシ | JS/composite | 隣接 | ◎ |
| 4-3 | DRONE | ICSE 2017 / TSE | Javadoc 制約 | NLP＋制約ソルバ | Java | 隣接 | ○ |
| 4-4 | Kechagia et al. | JSS 2018 | 例外の文書 | 静的解析＋クラッシュ | Java | 隣接 | ○ |
| 5-1 | Scoccia et al. | SCAM 2019 | manifest 権限 | M-Perm / P-Lint を全コミットに | Java | 隣接 | ◎ |
| 5-2 | Wen et al. | ICPC 2019 | コメント | AST 差分＋手作業 | Java | 隣接 | ◎ |

**「同一」と判定した研究はない**（AuthGap と同じく「助言的な副作用の宣言」×「実効の静的推定」×「事前登録・凍結・修正コミットでの recall」を備えた研究は見つからなかった）。

### Inferences
- 系統全体で見ると、AuthGap の主張として最も防御しやすい組み合わせは次の 4 点である。(1) 宣言が**強制されない真偽値の hint** で、**過小申告（安全側への嘘）方向**を測る（強制される権限の系統では構造上測れない。PrivLess の Pass 1 が根拠）。(2) 未解決を `opaque(reason)` として**率を主要な指標**にする（読んだ先例は除外・違反なしへの倒し込み・宣言からの補完のどれか）。(3) **事前登録と解析器の凍結**（取得した 22 本の本文に事前登録の語はない）。(4) **宣言の修正コミットを recall の正解に使う**（読んだ範囲に先例はない）。
- 逆に「宣言と実効の照合」「入口ごとの手続き間解析」「野外母集団での違反率」それぞれは先例が多い（Stowaway → COPES → SmartThings → Chrome 拡張 → PrivLess / EPScan、PASTE 2010）。この 3 つを単独で新規性として書くと反論される。
- 先例の多くに論文内の数値の食い違いがある（PrivLess: 418.75/1.55 と 683.37/2.40、Chrome 拡張: 39.8% / 37.8% / 40.8%、SmartThings: 42% と 43%、Granite: 52.7% と 46.6%）。引用時は表の値を採り、食い違いを併記するのが安全。

### Gaps
- 調査の範囲: 学術検索 API（Semantic Scholar, DBLP）は使えなかった（DBLP の API は JSON 以外を返した）。主に Web 検索と一次資料の PDF に頼った。ACM DL・IEEE Xplore の本文は取得できなかった（EPScan）。したがって「見つからなかった」は「この検索手順では見つからなかった」の意味である。
- Android の権限の変遷研究（Wei et al. ACSAC 2012「Permission evolution in the Android ecosystem」、Taylor & Martinovic 2016「Quantifying Permission-Creep in the Google Play Store」、Calciati らのリリース単位の研究）は検索結果に出たが、一次資料は読んでいない（△ — [arXiv 1606.01708](https://arxiv.org/abs/1606.01708v2); [NJIT](https://researchwith.njit.edu/en/publications/permission-evolution-in-the-android-ecosystem/)）。いずれも追加方向（permission creep）が中心と要約されていて、削除コミットを正解に使うものではなさそう。
- GitHub Actions の `permissions:` を絞る PR の受け入れ率や、それを正解に使った研究は見つからなかった（クエリ: `study pull requests restricting GitHub Actions workflow permissions acceptance ...`）。
- iOS の privacy manifest（required reason API）の宣言と実使用を照合する学術研究は見つからなかった（クエリ: `iOS privacy manifest required reason API declared vs used static analysis apps study 2025`）。プライバシー系は既出（Lalaine 等）の担当範囲でもある。

### 実行した検索クエリ（全件。結果の要点つき）
1. `"Locking discipline inference and checking" GuardedBy annotations programmers incorrect` → ICSE 2016 を発見
2. `Eyolfson Lam "writes-through-const" empirical study` → **見つからなかった**（無関係な結果のみ。13 で発見）
3. `Kubernetes third-party applications excessive permissions RBAC CCS 2023` → CCS 2023、EPScan、KubeKeeper
4. `static analysis least-privilege IAM policy AWS Lambda over-privileged functions paper` → PrivLess、ALPS、Gill 修論
5. `GitHub Actions GITHUB_TOKEN permissions over-privileged workflows empirical study least privilege` → Granite、Unit 42
6. `Decap deprivileging programs Linux capabilities static analysis RAID` → Decap
7. `"error code mismatches between documentation and the real world"` → **見つからなかった**（完全一致では出ず、27 で発見）
8. `static analysis idempotence serverless functions non-idempotent detection` → Flux
9. `"C++ const and immutability" writes through const ECOOP 2016` → ECOOP 2016
10. `Rudra SOSP 2021 Send Sync variance unsafe impl crates bugs found` → Rudra
11. `COPES Bartel permission gap Android static analysis declared permissions` → COPES
12. `Rubio-González Liblit error codes documentation Linux file systems static analysis man pages` → EIO（FAST 2008）等。PASTE 2010 は**見つからなかった**
13. `"directive defects" API documentation code static analysis Zhou ICSE 2017` → DRONE
14. `static detection state-changing GET requests web application HTTP safe method violation` → **見つからなかった**（学術研究なし。実務記事のみ）
15. `EPScan excessive RBAC permissions Kubernetes applications IEEE S&P 2025 pdf static analysis LLM` → Fudan の紹介ページ（PDF なし）、OperTraitor（Unit 42, LLM）
16. `Koishybayev "Characterizing the Security of GitHub CI Workflows" overprivileged permissions` → USENIX Sec 2022
17. `RacerD compositional static race detection @ThreadSafe annotation classes OOPSLA 2018` → RacerD
18. `Wen "A large-scale empirical study on code-comment inconsistencies" ICPC 2019 commits` → Wen et al.
19. `Rubio-González Liblit "Expect the unexpected" error code documentation PASTE` → **見つからなかった**
20. `Kechagia Spinellis "Undocumented and unchecked" exceptions Android API static analysis` → MSR 2014、JSS 2018
21. `empirical study developer purity annotations incorrect @Pure side-effect-free methods verification Java` → **見つからなかった**（JPure 等のツール論文のみ）
22. `Solidity view function modifies state inline assembly detector study smart contracts "view" violation` → **見つからなかった**（OOPSLA 2022 の inline assembly 研究と監査報告のみ）
23. `gRPC idempotency_level NO_SIDE_EFFECTS static analysis verify implementation` → **見つからなかった**（APIdemic のみ）
24. `GraphQL query resolver side effects static analysis mutation in query detection paper` → **見つからなかった**
25. `Axplorer Android permission specification over-privileged apps USENIX Security 2016 Dynamo NDSS 2021` → **見つからなかった**（Stowaway と Droidtector が出た）
26. `browser extension overprivileged permissions static analysis manifest unused permissions measurement` → IJIS 2022、arXiv 1403.3235
27. `Rubio-González Liblit 2010 documentation error codes mismatch Linux file system system calls manual pages static analysis` → PASTE 2010
28. `Android apps permission removal commits empirical study overprivilege evolution developers fix unnecessary permissions` → Scoccia（無題で）、Taylor & Martinovic、Wei et al.
29. `"Python 3 types in the wild" type annotations checked mypy errors DLS 2020` → DLS 2020
30. `"Permission Issues in Open-source Android Apps" exploratory study 574 repositories` → SCAM 2019
31. `"EPScan" Kubernetes "pod-oriented program analysis" excessive permissions results applications CVE`（extended）→ IEEE Xplore、GitHub
32. `Node.js Deno permission model static analysis infer required permissions npm packages least privilege paper` → Mir（既出）、arXiv 2103.05769、Deno NDSS 2025。Deno の静的推定は**見つからなかった**
33. `static analysis OpenAPI specification versus implementation inconsistency detection REST API code paper` → Respector（既出）、RESTRuler、OASQuali。新しいものは**見つからなかった**
34. `Kotlin @Contract pure=true annotation wrong side effect IntelliJ inspection study OR "functools.cache" impure function misuse detection` → **見つからなかった**（IntelliJ の文書のみ）
35. `Kubernetes operators RBAC over-privileged static analysis Go client calls compare ClusterRole measurement 2024 2025` → Breaking the Bulkhead（NDSS 2026）、BadRobot、OperTraitor
36. `iComment "bugs or bad comments" SOSP 2007 lock-related rules comments static analysis` → iComment
37. `Flatpak sandbox permissions over-privileged applications manifest empirical study static analysis` → SACMAT 2022
38. `Chrome extensions least privilege compliance 39.8% International Journal of Information Security 2022 permissions` → IJIS 2022
39. `"exception handling riddle" Android API static analysis undocumented exceptions mismatch Kechagia JSS 2018` → JSS 2018
40. `Deemon CSRF dynamic analysis property graphs state-changing HTTP requests GET CCS 2017` → Deemon
41. `SmartThings SmartApps overprivileged 55% static analysis capabilities "Security Analysis of Emerging Smart Home Applications"` → S&P 2016
42. `Slack apps OAuth scopes over-privileged static analysis measurement third-party apps workspace` → **見つからなかった**
43. `study pull requests restricting GitHub Actions workflow permissions acceptance developers token permissions hardening empirical` → **見つからなかった**（Unit 42 のみ）
44. `Code Contracts [Pure] attribute unchecked purity misuse empirical study C# contracts in practice` → **見つからなかった**（Contracts in Practice、Schiller et al. は `[Pure]` に特化しない）
45. `CodeQL java/csrf-unprotected-request-type state-changing action GET request query` → CodeQL のヘルプとライブラリ
46. `iOS privacy manifest required reason API declared vs used static analysis apps study 2025` → **見つからなかった**
- そのほかの取得: DBLP 検索 API を 3 回試したが JSON が返らず失敗した。EPScan の Fudan ページは WebFetch で 404、curl で接続リセット。IEEE Xplore と computer.org は本文が空。EPScan の GitHub リポジトリは scratchpad に clone して読んだ（実行はしていない）。
