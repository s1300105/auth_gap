# AuthGap の測定設計の方法論的先例（未解決の計数・事前登録・解析器凍結・修正コミット由来の再現率・単独評定・深さ 0 アブレーション）

調査日: 2026-10-12。検証水準は次の 3 段階で示す。

- ◎: 一次資料の全文（または該当節）を自分で読んだ
- ○: アブストラクト、または公式ページを読んだ
- △: 二次情報（検索エンジンの要約、引用元での言及）

**数値はすべて各論文の著者の主張で、こちらでは再現していない**（CLAUDE.md 規則 1）。PDF は repo の外の `/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad/methprec_dl/` に保存し、信頼できないデータとして扱った。成分の番号は次のとおり。

| 番号 | 成分 |
|---|---|
| 1 | 未解決の計数と理由語彙 |
| 2 | 三値目（unknown）の率の報告 |
| 3 | 事前登録・解析器凍結 |
| 4 | 開発者の修正コミットを再現率の正解にする |
| 5 | 単独評定と評定者内信頼性 |
| 6 | 深さ 0 アブレーション |
| D | 宣言と実効の照合という測定の型 |

---

## Q1. Python などの静的解析は、未解決の呼び出しや未知の呼び出し先の割合を測り、報告しているか。未解決の理由はどんな語彙で書かれているか

### Takeaway

「未健全（unsound）な箇所を明示し、評価対象への影響を評価せよ」という規範は、2015 年の soundiness manifesto 以来確立している。JavaScript の呼び出しグラフ研究では「% resolved call sites」が標準的な指標として使われている。一方、Python の呼び出しグラフ研究（PyCG、Jarvis）が報告するのは、手作りの正解に対する precision と recall、それに未対応機能の定性的な列挙までだった。**Python で、呼び出し地点や効果の単位の未解決率を主結果として報告した例は見つからなかった。** 理由の語彙はツールごとに固有で、共通の語彙はない。

### Cited Findings

- **[◎] Livshits, Sridharan, Smaragdakis, Lhoták, Amaral, Chang, Guyer, Khedker, Møller, Vardoulakis, "In Defense of Soundiness: A Manifesto", CACM 58(2), 2015**（成分 1、2）
  - 共同体への呼びかけ: "We issue a call to the community to identify clearly the nature and extent of unsoundness in static analyses. Currently, in published papers, sources of unsoundness often lurk in the shadows, with caveats only mentioned in an off-hand manner in an implementation or evaluation section."
  - 結論部: "Papers involving soundy analyses should both explain the general implications of their unsoundness and evaluate the implications for the benchmarks being analyzed."
  - "It really does not help the reader for the analysis' author to declare that their analysis is sound modulo features X and Y, only to discover that these features are present in just about every real-life program!"
  - 出典: [著者版 PDF](https://yanniss.github.io/Soundiness-CACM.pdf)、[CU Boulder の書誌ページ](https://plv.colorado.edu/papers/soundiness-cacm15.html)
- **[◎] Laursen, Xu, Møller, "Reducing Static Analysis Unsoundness with Approximate Interpretation", PLDI 2024（Jelly、JavaScript）**（成分 1、6 に近い）
  - 指標の定義: "Percentage of resolved call sites. A call site is considered resolved if the analysis found at least one call edge for it. ... so this metric gives an indication of the analysis recall [Feldthaus et al. 2013]."
  - 141 の Node.js プロジェクトで "17.7% more resolved call sites" と報告している（著者の主張）。
  - 文字列などプリミティブへのメソッド呼び出しは "count as unresolved in this metric, which partly explains the remaining gap to 100%" と明記している。
  - **JS の呼び出しグラフ研究では、解決率は 2013 年以来の定番指標である。**
  - 出典: [論文 PDF](https://www.cs.au.dk/~amoeller/papers/approx/paper.pdf)
- **[◎] Salis, Sotiropoulos, Louridas, Spinellis, Mitropoulos, "PyCG: Practical Call Graph Generation in Python", ICSE 2021**（成分 1、6）
  - 未対応機能を定性的に列挙している（理由語彙に相当）。
    - "Our analysis does not fully support all of Python's features. First, we ignore code generation schemes, such as calls to the eval built-ins."
    - "attribute calls that depend on a specific built-in type (e.g., list.append()) are not resolved, while the effects of functions such as getattr and setattr are ignored. Third, we can only analyze modules for which their source code has been provided."
  - 評価は手作りの正解に対する precision と recall だった（"on average, 69.9% of all call edges are successfully retrieved"）。**呼び出し地点ごとの未解決率は出していない。**
  - 出典: [arXiv 2103.00587](https://arxiv.org/abs/2103.00587)
- **[◎ 部分] Huang et al., "JARVIS: Scalable and Precise Application-Centered Call Graph Construction for Python", arXiv 2305.05949 (v5, 2024)**（成分 1）
  - micro-benchmark で健全（sound）か完全（complete）かを件数で数えている。例: "In terms of soundness, PyCG generates call graphs that are sound for 126 programs. The rest 12 unsound cases span ..."
  - ここでも単位はプログラムや辺の数で、未解決率の報告ではない。
  - 出典: [arXiv 2305.05949](https://arxiv.org/abs/2305.05949)
- **[◎ 部分] Monat, Ouadjaout, Miné, "Value and Allocation Sensitivity in Static Python Analyses", SOAP 2020**（成分 1、2）
  - "our analysis strives to be sound for Python programs that do not include recursive functions, the eval and super statements, metaclasses, nor asynchronous operators. It detects all uses of these unsupported features and reports them as unsoundness alarms."
  - **Python 解析器が未対応構文の使用を「unsoundness alarm」として全数報告する設計の先例である。** AuthGap の `opaque(reason)` に最も近い。
  - 出典: [HAL hal-02876667](https://hal.sorbonne-universite.fr/hal-02876667/document)
- **[○] Pysa（Meta）公式ドキュメント "Obscure models"**（成分 1。語彙の先例）
  - "When Pysa does not have enough information about a function or method, it will make basic assumptions about its behavior." これを "obscure model" と呼ぶ。
  - 適用されるのは、呼び出し先が分からない場合（例: 引数 `f` の呼び出し）と、型スタブや C/C++ バインディングの場合。
  - 引数から戻り値へ taint を通す（TITO）と仮定する。流れには `tito-broadening` と `via:obscure:model` という feature が付く。
  - **未解決の件数を数える公式オプションは、このページには記載がなかった。**
  - 出典: [pyre-check.org/docs/pysa-advanced](https://pyre-check.org/docs/pysa-advanced/)
- **[◎ 部分] Gu, Yan, Yao, "PyFlow: An Inter-procedural Static Analysis Framework for Python", arXiv 2608.07026 (2026)**（成分 1、2 の反例）
  - "a timeout is recorded as no detection rather than as a partial result."
  - **打ち切りを「不検出」に畳む実例で、AuthGap の扱いと正反対である**（false-clean 方向に畳む）。
  - 出典: [arXiv 2608.07026](https://arxiv.org/abs/2608.07026)
- **[○] Reif, Kübler, Eichberg, Helm, Mezini, "Judge: identifying, understanding, and evaluating sources of unsoundness in call graphs", ISSTA 2019（Java）**（成分 1）
  - 目的の一つに "to determine the prevalence of language features and APIs that affect soundness in modern Java Bytecode" を挙げている。
  - 出典: OpenAlex で取得したアブストラクト（DOI [10.1145/3293882.3330555](https://doi.org/10.1145/3293882.3330555)）
- **[○] Sui, Dietrich, Tahir, Fourtounis, "On the recall of static call graph construction in practice", ICSE 2020（Java）**（成分 1）
  - 31 本の Java プログラムで、動的実行を oracle にして recall を測った。"investigated which language features lead to static analysis false negatives."
  - 出典: DOI [10.1145/3377811.3380441](https://doi.org/10.1145/3377811.3380441)（OpenAlex 経由のアブストラクト）
- **[○] Chakraborty, Olivares, Sridharan, Hassanshahi, "Automatic Root Cause Quantification for Missing Edges in JavaScript Call Graphs", ECOOP 2022**（成分 1。理由語彙の定量化）
  - "dynamic property accesses were the most common root cause of missed edges across the benchmarks"
  - 出典: [arXiv 2205.06780](https://arxiv.org/abs/2205.06780)
- **[○] Åkerblom, Stendahl, Tumlin, Wrigstad, "Tracing dynamic features in Python programs", MSR 2014**（成分 1 の背景）
  - トレースを使って、型付けの難しい組み込み機能（動的コード生成など）の実行時使用を収集した。
  - 出典: DOI [10.1145/2597073.2597103](https://doi.org/10.1145/2597073.2597103)（OpenAlex のアブストラクト）
- **[△] Holkner & Harland, "Evaluating the dynamic behaviour of Python applications", ACSC 2009**
  - 24 本の Python プログラムで、動的な振る舞いの多くは起動時に起きると報告している（検索要約）。
  - 出典: [CRPIT abstract](https://crpit.scem.westernsydney.edu.au/abstracts/CRPITV91Holkner.html)
- **[○] Bouzenia, Krishan, Pradel, "DyPyBench", FSE 2024**（成分 1）
  - 動的な呼び出しグラフと静的なものを比較し、"exposes and quantifies limitations of existing call graph construction techniques for Python" と述べている。
  - 出典: [arXiv 2403.00539](https://arxiv.org/abs/2403.00539)
- **[△] Jin et al., "PyAnalyzer", ICSE 2024**
  - 動的機能（"object changes, first-class citizens, varying call sites, and library dependencies"）を課題として挙げ、7 ツールと比較している（検索要約）。
  - 出典: [ICSE 2024 ページ](https://conf.researchr.org/details/icse-2024/icse-2024-research-track/233/PyAnalyzer-An-Effective-and-Practical-Approach-for-Dependency-Extraction-from-Python)

### Inferences

- **「未解決を数えて主結果として出す」は、思想として新規とは言えない。** soundiness manifesto（2015）の呼びかけへの準拠と位置づけるのが正確である。
- 新規と言いうるのは、次の組み合わせの具体性に限られる。
  - Python の木で
  - 呼び出し地点ではなく、効果の判定の単位で
  - 固定した 8 理由と、打ち切り・時間予算の記録として
  - 宣言と実効を照合するときの三値目として報告する
- 未解決の扱いの最も近い先例は、Monat らの「全数を unsoundness alarm として報告する」設計と、Pysa の obscure model である。前者は全数報告、後者は TITO の仮定と feature のタグ付けを行う。
- Jelly の「resolved」は「辺が 1 本以上ある」という定義なので、AuthGap の opaque（値と効果の単位）とは分母が違う。比較するときは分母の定義を併記する必要がある（CLAUDE.md 規則 3）。
- PyFlow の「timeout は不検出」は、AuthGap が避けている扱いの最新の実例として対比に使える。

### Gaps

- 「On the Unsoundness of Static Analysis for Python」という題の論文は見つからなかった（検索 2）。
- Scalpel（arXiv 2202.11840）の本文には、`unresolv|unknown|unsound|dynamic feature` の語はヒットしなかった。
- HeaderGen と PyAnalyzer は全文を確認しておらず、未解決率を報告しているかは不明。
- Pysa や Pyre に、未解決の callee を数える公式の機能があるかは確認できなかった。
- Åkerblom らと Holkner らの具体的な数値は取得していない。

---

## Q2. 「unknown／判定不能」を第三の判定として扱い、その率を報告している研究

### Takeaway

ソフトウェア検証の競技会（SV-COMP）では、Unknown は制度化された第三の判定で 0 点と数えられ、timeout も Unknown に含まれる。測定研究では、宣言と実効の照合の古典である Felt et al.（CCS 2011）が、未解決のリフレクションを含むアプリを別群として報告している。Gao et al.（ICSE 2017）は、時間予算を超えたものを unknown ラベルとして記録した。**三値目は確立した手法で、AuthGap の三値は SV-COMP と同じ型をしている。**

### Cited Findings

- **[◎] Beyer, "Reliable and Reproducible Competition Results with BenchExec and Witnesses (Report on SV-COMP 2016)", TACAS 2016**（成分 2）
  - Unknown の定義: "Unknown: The tool cannot decide the problem, or terminates abnormally, or exhausts the computing resources time or memory (i.e., the competition candidate does not succeed in computing an answer True or False)."
  - 時間超過の扱い: "the answer is set to 'timeout' (and interpreted as Unknown)."
  - 採点表: "Unknown 0 Failure to compute verification result"。誤った True は −32、誤った False は −16。
  - 出典: [SoSy-Lab PDF](https://www.sosy-lab.org/research/pub/2016-TACAS.Reliable_and_Reproducible_Competition_Results_with_BenchExec_and_Witnesses.pdf)
  - 2025 年の採点も「unchanged」と、主催者のスライドにある（△、[TACAS25 スライド](https://www.sosy-lab.org/research/prs/2025-05-05_TACAS25_SV-COMP_DirkJan.pdf)、検索要約経由）。
- **[◎] Felt, Chin, Hanna, Song, Wagner, "Android Permissions Demystified", CCS 2011（Stowaway）**（成分 2、D、3、5。**Q7 の同一設計リスク**）
  - "Stowaway was unable to resolve some applications' reflective calls, which might lead to a higher false positive rate in those applications. Consequently, we discuss applications with unresolved reflective calls separately from other applications."
  - "Stowaway was able to handle all reflective calls for 795 of the 900 applications"
  - Table 3 は、警告率をリフレクションの状況別に示している（著者の主張）。

    | 群 | 警告のあるアプリ / 全アプリ | 警告率 |
    |---|---|---|
    | Reflection, failures | 56/105 | 53% |
    | Reflection, no failures | 151/440 | 34% |
    | No reflection | 109/355 | 31% |

  - 出典: [CCS'11 PDF（講義サイトのミラー）](https://comp97109.doc.ic.ac.uk/reading/felt_ccs_11.pdf)
- **[◎] Gao, Bird, Barr, "To Type or Not to Type: Quantifying Detectable Bugs in JavaScript", ICSE 2017**（成分 2、4、5）
  - 1 件あたりの作業時間を 10 分に制限した。"We, however, could not always decide whether a bug is ts-detectable within 10 minutes, leaving 18 unknown."
  - "Let U denote unknown, D detectable, and D̄ undetectable."
  - "In discussing unknowns, we learned that each of us independently had categorized a bug as unknown when we thought it was detectable, but could not show it, before we ran out of time."
  - **最終的には時間制限なしで unknown 18 件をすべて解消した。この点は AuthGap と違う（AuthGap は unknown を残す）。**
  - 出典: [著者版 PDF（講義サイトのミラー）](https://janvitek.org/events/NEU/7575/pubs/no-type.pdf)、[UCL Discovery](https://discovery-pp.ucl.ac.uk/id/eprint/10064729)
- **[◎] Laursen et al. PLDI 2024**（Q1 参照）
  - 解決率を主要な指標の一つにしている（成分 1、2）。
- **[◎ 部分] Xiao et al., "Lalaine: Measuring and Characterizing Non-Compliance of Apple Privacy Labels", USENIX Security 2023**（D、5）
  - 宣言（プライバシーラベル）とデータフローを照合する研究。"we could not fully run all 366,685 iOS apps we collected" と書き、5,102 本を解析した。
  - **解析不能なアプリを三値目として率で報告しているかは、本文の grep では確認できなかった。**
  - 出典: [arXiv 2206.06274](https://arxiv.org/abs/2206.06274)、[USENIX ページ](https://www.usenix.org/conference/usenixsecurity23/presentation/xiaoyue)
- **[◎ 部分] PyFlow（2026）**
  - timeout を不検出として数える（Q1 の反例）。

### Inferences

- AuthGap の三値（矛盾、整合、opaque）は、SV-COMP の FALSE / TRUE / UNKNOWN と同じ型である。timeout を Unknown に含める点も SV-COMP と同じなので、**「三値目を立てる」こと自体は新規ではない。**
- **宣言と実効を照合する測定で、未解決を別群として扱った先例は Felt et al. 2011 である。** これは必ず引用すべきである。
  - Felt は、未解決群で警告率が高い（53% 対 31〜34%）ことを「誤検出が増えうる」方向として扱った。
  - AuthGap は opaque を finding として扱わないので、この偏りへの対処の仕方が異なる。この違いは、差分として説明できる。
- Gao の unknown は人の判定の時間切れで、後に解消された。AuthGap の opaque は解析器の判定不能で、残される。どちらも「時間予算と unknown を記録する」点は共通している。

### Gaps

- Android の解析研究（DroidRA などのリフレクション解決研究や、FlowDroid 系の比較研究）が、解析不能や timeout のアプリの率を三値目として報告しているかは、全文で確認していない。
- プライバシーラベル研究で「untestable」の率を報告する例は見つけられなかった（検索 23）。

---

## Q3. ソフトウェア工学やセキュリティの測定における事前登録・Registered Reports。閾値を事前登録し、評価データを見る前に解析器を凍結した静的解析の評価はあるか

### Takeaway

SE では、Registered Reports（RR）が MSR 2020 で導入され、MSR、ICSME、ESEM と、EMSE、TOSEM で定着している。ACM SIGSOFT の Empirical Standards にも RR の基準がある。セキュリティ寄りでは、FUZZING ワークショップ（NDSS 併設、2022 年から）が、fuzzer の評価に 2 段階の事前登録型の出版を運用している。

**静的解析ツールの評価や、静的解析を使った測定研究で、事前登録した例は見つからなかった。** 解析器の凍結にも、文献上の直接の先例は見つからなかった。近いのは次の 3 つである。

- Arp et al. の「test snooping」を落とし穴とする指摘
- Felt et al. が開発用に 24 アプリを取り置いた手続き
- 競技会で検証器をアーカイブとして提出する慣行

### Cited Findings

- **[◎] Ernst & Baldassarre, "Registered Reports in Software Engineering", EMSE 2023**（成分 3）
  - "In software engineering research, registered reports were first introduced in the International Conference on Mining Software Repositories (MSR) in 2020. They are now established in three conferences and two pre-eminent journals, including this one (EMSE)."
  - "This preregistration commits the researchers to a particular analysis path and data selection, ahead of seeing the actual data."
  - "To date (late 2022) six papers have successfully been published as completed Stage 2 reviews in EMSE, and 16 more are under Stage 2 review at EMSE."
  - 表 1 は MSR 2020〜2022、ICSME 2020〜2021、ESEM 2021〜2022 の Stage 1 と Stage 2 の件数を示している。
  - 出典: [arXiv 2302.03649](https://arxiv.org/abs/2302.03649)
- **[◎] ACM SIGSOFT Empirical Standards, "Registered Reports" 基準**（成分 3）
  - 適用範囲: "This standard applies to positivist, confirmatory (i.e. hypothesis-testing) studies with tightly-scoped analysis approaches. Pre-registering interpretivist, qualitative or exploratory research remains controversial."
  - RR2 の必須項目: "EITHER: adheres precisely to the registered procedures OR: thoroughly justifies all deviations and explains how they affect the final analysis." "deviations, if any, are _not_ justified based on the data" "clearly designates as exploratory any unregistered post hoc analyses"
  - アンチパターン: "postdictive deviations from RR1 plan; i.e., changes made knowing how they would affect the outcome of the study"、"Pre-registrations that are not verifiably committed prior to data collection, e.g. not time-stamped."
  - 出典: [GitHub raw: docs/supplements/RegisteredReports.md](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/RegisteredReports.md)
- **[○] First International Fuzzing Workshop (FUZZING 2022) CfP（NDSS 併設）**（成分 3。ツール評価の事前登録）
  - "Phase 1 in a 2-phase preregistration-based publication process"
  - 審査は "explicitly not based on the strength of the (preliminary) results" で、方法の "soundness and reproducibility" を見る。
  - 出典: [NDSS 2022 CfP](https://www.ndss-symposium.org/ndss2022/cfp-fuzzing-workshop/)
  - 2026 年版は ACM TOSEM との 2 段階方式だという（△、[FUZZING 2026 CfP](https://www.ndss-symposium.org/ndss2026/submissions/cfp-fuzzing/)、検索要約経由）。
  - Registered Report の例として、FuzzBench の coverage 評価がある（△、[RUB の業績ページ](https://softsec.rub.de/publications/fuzzing2026-the-things-that-count/)）。
- **[○] Cockburn, Gutwin, Dix, "HARK No More: On the Preregistration of CHI Experiments", CHI 2018**（成分 3）
  - "When experimental intentions are preregistered, reviewers and readers can be confident that experimental evidence in support of reported hypotheses is not the result of HARKing"
  - 出典: DOI [10.1145/3173574.3173715](https://doi.org/10.1145/3173574.3173715)（OpenAlex のアブストラクト）
- **[◎] Arp et al., "Dos and Don'ts of Machine Learning in Computer Security", USENIX Security 2022**（成分 3。凍結の論理的な根拠）
  - P3 Data Snooping: "Test snooping occurs when the test set is used for experiments before the final evaluation. This includes preparatory work to identify useful features, parameters, and learning algorithms."
  - 30 本の論文を調べた結果、P3 は "57% present"（著者の主張）。
  - **機械学習の話だが、「評価データを見ながら解析器の規則を直すこと」は同じ構造の誤りである。**
  - 出典: [arXiv 2010.09470](https://arxiv.org/abs/2010.09470)
- **[◎] Felt et al. CCS 2011**（成分 3 に近い）
  - "We set aside 24 randomly selected applications for tool testing and training, leaving 940 for analysis."
  - 開発用と評価用の分離はしているが、解析器の凍結や事前登録の記述はない。
- **[◎ 部分] SV-COMP 2016 の報告**
  - 構成要素として "(d) Verifier Archives"（"The verifiers are provided in an archive ..."）を挙げている。**提出締切後の凍結の規程そのものは読んでいない。**
- **[○] MSR 2026 の Registered Reports のプログラム**
  - "Automated Testing of Task-based Chatbots: How Far Are We?" など、ツールの有効性評価が RR として発表されている。
  - 出典: [MSR 2026 RR track](https://2026.msrconf.org/track/msr-2026-registered-reports)
  - arXiv にも、ツールや技術を評価する RR がある（○、arXiv の題名一覧）。
    - "TENSURE: Fuzzing Sparse Tensor Compilers (Registered Report)"（2026、[2603.18372](https://arxiv.org/abs/2603.18372)）
    - "Local Software Buildability across Java Versions (Registered Report)"（2024、[2408.11544](https://arxiv.org/abs/2408.11544)）
- **[△] Groß（Newcastle）らの OSF 事前登録**
  - サイバーセキュリティのユーザー研究を対象にしたメタ研究（統計的検出力、PPV、出版バイアス）を事前登録している（検索要約）。
  - 出典: [Newcastle CASCADE pre-registrations](https://research.ncl.ac.uk/cascade/outputs/evidence-basedmethods/pre-registrations/)

### Inferences

- **事前登録そのものは、SE で 6 年の実績がある確立した手法である。** fuzzing の評価でも 2022 年から運用されている。新規性の主張は「静的解析による野外測定（宣言と実効の照合）への適用」に限定すべきである。
- **静的解析の評価や測定の RR は、今回の検索では 1 件も見つからなかった。** これは「適用例として珍しい」とは言えるが、「初」と書くには網羅的な確認が足りない。
- Empirical Standards の RR 基準は、AuthGap の運用を評価する外部基準としてそのまま使える。
  - 「逸脱をデータに基づいて正当化しない」は、CLAUDE.md の凍結規則と、逸脱ログ #26 に対応する。
  - 「タイムスタンプのない事前登録はアンチパターン」は、期待値ファイルを先にコミットする運用と、git tag による凍結に対応する。
  - 「未登録の事後分析は exploratory と明示」も同様に使える。
  - 一方、この基準は confirmatory な研究を想定しているので、AuthGap の探索的な部分（理由の内訳や事例分析）は exploratory と明示する必要がある。
- 解析器の凍結（git tag と fingerprint）は、Arp の test snooping 回避を静的解析器に移したものと説明できる。git tag と fingerprint という実装の形は先例が見つからなかった。ただしこれは技術的な実装で、方法論上の新規性としては弱い。

### Gaps

- 「SoK: preregistration in security research」に当たる文献は見つからなかった（検索 14）。
- USENIX Security、IEEE S&P、CCS、NDSS の本会議に、事前登録の枠があるかは確認できなかった。
- 「registered report」と「static analysis」の組み合わせは、arXiv API とウェブ検索の両方で 0 件だった（検索 24、arXiv 検索 a〜e）。
- SV-COMP で検証器が凍結される時期（ベンチマーク公開との前後関係）の規程は読んでいない。

---

## Q4. 開発者の修正コミットを、静的チェッカーの再現率の正解に使う研究

### Takeaway

**修正済みの欠陥を正解にして、静的チェッカーの再現率を測るのは標準的な手法である。** 2012 年の Thung et al. 以来、少なくとも 9 件の先行例を確認した。しかしすべて「バグや脆弱性の修正」を正解にしている。**「宣言（注釈）の修正」コミットを正解にして、宣言と実効の不一致を検出する器の再現率を測った例は見つからなかった。**

### Cited Findings

- **[○] Thung, Lucia, Lo, Jiang, Rahman, Devanbu, "To what extent could we detect field defects?", ASE 2012**（拡張版は Automated Software Engineering 22(4), 2015）（成分 4）
  - "we perform an empirical study that investigates the effectiveness of state-of-the-art static bug finding tools on hundreds of reported and fixed defects extracted from three open source programs: Lucene, Rhino, and AspectJ."
  - "Different from past studies that are concerned with the numbers of false positives produced by such tools, we address an orthogonal issue on the numbers of false negatives."
  - 出典: DOI [10.1145/2351676.2351685](https://doi.org/10.1145/2351676.2351685)（OpenAlex のアブストラクト）、[SMU のページ](https://ink.library.smu.edu.sg/sis_research/2435)
- **[◎] Gao, Bird, Barr, ICSE 2017**（成分 4、2、5）
  - "and check out the code just prior to the fix. We manually add type annotations to the buggy code and test whether Flow and TypeScript report an error on the buggy code"
  - 400 件の公開バグを使った。両ツールとも約 15% を検出したという（著者の主張）。
  - 出典: [PDF](https://janvitek.org/events/NEU/7575/pubs/no-type.pdf)
- **[◎] Khan, Chen, Varró, McIntosh, "An Empirical Study of Type-Related Defects in Python Projects", IEEE TSE 48(8), 2022（2021 年に先行公開）**（成分 4。**Python での直系の先例**）
  - "Inspired by the work of Gao et al. on type-related defects in JavaScript, we add type annotations to test whether mypy detects an error that would have helped developers to avoid real defects. We observe that 15% of the defects could have been prevented by mypy."
  - 公開済みの欠陥に限ることの限界を自分で書いている: "Our evaluation is conducted on fixed public defects. This number is likely to be higher for private defects observed during development"
  - 出典: [著者版 PDF](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf)
- **[○] Habib & Pradel, "How Many of All Bugs Do We Find? A Study of Static Bug Detectors", ASE 2018**（成分 4）
  - "studying the results of applying three widely used static bug detectors to an extended version of the Defects4J dataset that consists of 15 Java projects with 594 known bugs. To decide which of these bugs the tools detect, we use a novel methodology that combines an automatic analysis of warnings and bugs with a manual validation of each candidate of a detected bug."
  - 結論の一つは "current bug detectors miss the large majority of the studied bugs"。
  - 出典: DOI [10.1145/3238147.3238213](https://doi.org/10.1145/3238147.3238213)（OpenAlex のアブストラクト）
  - 公式リポジトリは、非公式版の Defects4J（PR #112）を使ったと注記している（◎、[sola-da/StaticBugCheckers README](https://github.com/sola-da/StaticBugCheckers)）。
- **[○] Tomassi & Rubio-González, "On the Real-World Effectiveness of Static Bug Detectors at Finding Null Pointer Exceptions", ASE 2021**（成分 4）
  - 102 件の実際の NPE を使った。"the tools under study only find 30 out of 102 bugs (29.4%)"。
  - 出典: DOI [10.1109/ASE51524.2021.9678535](https://doi.org/10.1109/ASE51524.2021.9678535)（Semantic Scholar のアブストラクト）
- **[◎ 部分] Lipp, Banescu, Pretschner, "An Empirical Study on the Effectiveness of Static C Code Analyzers for Vulnerability Detection", ISSTA 2022**（成分 4）
  - 192 件の CVE を正解にした。"state-of-the-art tools miss in-between 47% and 80% of the vulnerabilities"。
  - パッチの位置（fault）と発現の位置（error）がずれる問題を、指標として扱っている。
  - 出典: [TUM mediaTUM PDF](https://mediatum.ub.tum.de/doc/1659728/1659728.pdf)
- **[○] Li et al., "Comparison and Evaluation on Static Application Security Testing (SAST) Tools for Java", ESEC/FSE 2023**（成分 4）
  - "only 12.7% of real-world vulnerabilities can be detected by the selected tools"
  - 出典: DOI [10.1145/3611643.3616262](https://doi.org/10.1145/3611643.3616262)（Semantic Scholar のアブストラクト）
- **[○] Charoenwet, Thongtanunam, Pham, Treude, "An Empirical Study of Static Analysis Tools for Secure Code Review", ISSTA 2024**（成分 4。修正ではなく脆弱性を混入させたコミット）
  - "319 real-world vulnerabilities from 815 vulnerability-contributing commits (VCCs) in 92 C and C++ projects ... 22% of VCCs remain undetected due to limitations of SAST rules."
  - 出典: [arXiv 2407.12241](https://arxiv.org/abs/2407.12241)
- **[△] Liu, Wang, Liu, Li, "An empirical study on static application security testing (SAST) tools for Python", ICSE 2026**（成分 4、6 に近い）
  - PyFlow の論文は、この研究を次のように説明している（[arXiv 2608.07026](https://arxiv.org/abs/2608.07026) 経由）。
    - 108 件の CVE と 62 プロジェクトから成る実データのベンチマーク
    - パッチ前を recall、パッチ後を偽陽性に使う方法論
  - データセット: PySASTBench。原論文は読んでいない。
- **[△] Di Grazia & Pradel, "The Evolution of Type Annotations in Python: An Empirical Study", ESEC/FSE 2022**（成分 4 の隣接）
  - 型注釈の変更を大規模に採掘した研究だが、注釈の修正を再現率の正解には使っていない（検索要約）。
  - 出典: [FSE 2022 ページ](https://2022.esec-fse.org/details/fse-2022-research-papers/36/The-Evolution-of-Type-Annotations-in-Python-An-Empirical-Study)

### Inferences

- **「開発者の修正を正解にした再現率」は、AuthGap の新規性として主張できない。** Thung（2012）、Gao（2017）、Habib & Pradel（2018）、Khan（2021、Python）が直系の先例である。
- 新規と言いうるのは、正解の種類である。すなわち「宣言（ToolAnnotations）を実効に合わせて直したコミット」を正解にする点である。
  - Gao と Khan は、研究者がバグ版に注釈を「足して」型検査器に掛けた。宣言側を研究者が作っている。
  - AuthGap は、開発者自身が宣言を直した記録を使う。向きが逆なので、この差は明示する価値がある。
- 先行研究が書いている脅威は、そのまま AuthGap の脅威の節に使える。
  - 公開済みの欠陥しか見ていないので、下限になる（Gao、Khan）
  - 修正に無関係な変更が混ざる（tangled fix、Gao）
  - 検出したかどうかの照合基準（Habib の「自動照合と人手の検証」、Lipp の fault と error のずれ）

### Gaps

- CVEfixes や BigVul を SAST の再現率の正解に使った研究は、今回は確認していない。
- 「annotation fix commit」や「型ヒントの修正コミット」を検出器の正解にした研究は、見つからなかった（Di Grazia & Pradel は記述的な研究）。
- Habib & Pradel の本文の数値は読めていない。ACM DL は 403 だった。

---

## Q5. SE やセキュリティの測定での単独評定と評定者内信頼性。受け入れられている先例と批判

### Takeaway

ACM SIGSOFT の Empirical Standards は、正当化があれば単独評定を明示的に許容している。Kitchenham & Charters（2007）は、単独研究者（博士学生）に test-retest（後日、無作為標本を再判定すること）を推奨している。**AuthGap の「10% を 2 週間以上空けて再判定する」は、この推奨の直系である。**

ただし評定者内信頼性を実際に測る研究は稀である。また Empirical Standards のリポジトリマイニング基準は、人手の注釈に複数のアノテータを求めている。このため単独評定には正当化が必須になる。

### Cited Findings

- **[◎] Empirical Standards, "Inter-Rater Reliability and Agreement" 補遺**（成分 5）
  - "There is no universal rule to determine when two or more raters are necessary."
  - "Practicality: the less practical it is to have multiple raters, the more reasonable a single-rater design becomes"
  - 必須項目: "EITHER: provides reasonable justification for using a single rater"。脚注 4 は正当化の例として "the ratings are uncontroversial; multiple raters would be impractical; ..." を挙げる。
  - 不当な批判の例: "Criticizing use of a single rater where multiple raters would be impractical ..." "Criticizing use of a single rater when the data is such that there is no reason to suspect different raters would reach different conclusions."
  - 出典: [GitHub raw: InterRaterReliabilityAndAgreement.md](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/InterRaterReliabilityAndAgreement.md)
- **[◎] Empirical Standards, "Repository Mining" 基準**（成分 5。**批判側の根拠**）
  - 必須項目: "if manual annotations are carried out: uses multiple annotators; reports the number of annotators ... assesses inter-rater reliability"
  - **AuthGap の precision の判定は、この「manual annotations」に当たると読まれうる。**
  - 出典: [GitHub raw: RepositoryMining.md](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/standards/RepositoryMining.md)
- **[◎] Kitchenham & Charters, "Guidelines for performing Systematic Literature Reviews in Software Engineering", EBSE-2007-01 v2.3**（成分 5。**最も直接的な先例**）
  - 研究の選定: "A single researcher (such as a PhD student) should consider discussing included and excluded papers with their advisor, an expert panel or other researchers. Alternatively, individual researchers can apply a test-retest approach, and re-evaluate a random sample of the primary studies found after initial screening to check the consistency of their inclusion/exclusion decisions."
  - データ抽出: "For single researchers such as PhD students, other checking techniques must be used. ... Alternatively, a test-retest process can be used where the researcher performs a second extraction from a random selection of primary studies to check data extraction consistency."
  - 出典: [EBSE-2007-01 PDF](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf)
- **[◎] Gao, Bird, Barr, ICSE 2017**（成分 5。主評定者 1 名と較正の型）
  - "Our main results rest on an assessment of our corpus of 400 buggy versions of JavaScript projects conducted by one of the authors. To help him calibrate, all authors assessed a subset of the bugs."
  - 手順は、20 件で較正したあと 80 件を独立に判定して一致度を出すもの（"full agreement among all authors for 86.4% of the issues"、AC1 を使用）。
- **[◎ 部分] Harvey, Koenecke, Kizilcec, "Data Annotation as Measurement", arXiv 2608.07297 (2026, preprint)**（成分 5。稀であることの根拠）
  - "it is rare to assess test-retest reliability (also referred to as intra-rater reliability)"
  - 次の一文は Abercrombie et al. 2025 からの孫引きなので、数値は △: "Abercrombie et al. (2025) recently found that, of more than 80,000 papers in the ACL Anthology, just 56 of them (0.07%) report measuring test-retest reliability."
  - 出典: [arXiv 2608.07297](https://arxiv.org/abs/2608.07297)
- **[○] McDonald, Schoenebeck, Forte, "Reliability and Inter-rater Reliability in Qualitative Research", PACM HCI (CSCW) 2019**（成分 5）
  - "IRR is rare, occurring in around 1/9 of qualitative papers"
  - "should I calculate IRR?" に答えるための指針を示している。
  - 出典: DOI [10.1145/3359174](https://doi.org/10.1145/3359174)（OpenAlex のアブストラクト）
- **[◎ 部分] Felt et al. CCS 2011**（成分 5）
  - 無作為に選んだ 40 アプリの警告を手で分析した。"We then manually analyzed each overprivilege warning to attribute it to either tool error (i.e., a false positive) or developer error."
  - 誤検出率は 7%（著者の主張）。評定者の人数と一致度の記述は、読んだ範囲にはなかった。
- **[◎ 部分] Lalaine（USENIX Sec 2023）**
  - 学習データの注釈では "four annotators labeled 2,958 pieces of traffic ... achieved 0.923 agreement"。宣言と実効の照合の研究でも、複数アノテータの例がある。

### Inferences

- AuthGap の単独評定と 10% の再判定は、次の 2 つを引けば正当化の枠組みに乗る。
  - Kitchenham & Charters の test-retest
  - Empirical Standards の単独評定の正当化（「論争の少ない判定」「複数評定者は非現実的」）
- 予想される反論は、RepositoryMining 基準の「uses multiple annotators」である。これには次のように答えられる。
  - precision の判定は、事前に定めた判定規則（演繹的な符号化）による。
  - 判定の根拠となる行（diff）を公開する。
  - 評定者内の一致度を報告する。
- Gao の「主評定者 1 名と、全著者による部分標本の較正」は、評定者間の一致度を部分的に足す折衷案の先例である。共著者や指導教員が無作為標本を判定できるなら、Kitchenham も第一案として挙げている。
- 評定者内信頼性を実測する研究は少ない（ACL では 0.07%、孫引き）。**「単独評定に評定者内信頼性を付ける」ことは珍しいが、新規の方法ではない。**

### Gaps

- 静的解析の警告の precision を単独評定し、評定者内 κ を報告した SE の論文は見つからなかった（検索 15）。
- 再判定の間隔（2 週間以上）について、SE の規範値は見つからなかった。
  - 「忘れる程度の間隔を置く」という助言は、質的研究の解説サイトにしかなかった（△）。
  - 権威ある出典ではないので、引用には使えない。

---

## Q6. 深さ 0（関数本体のみ）と手続き間解析を比べて、検出の再現率を測った実験

### Takeaway

**静的解析で「呼び出しの深さ 0 と深さ k」を明示的に切り替えるアブレーションを行い、実データで再現率を比べた研究は見つからなかった。** 近いのは次の 3 種類である。

- 手続き間の追跡をしないツールとするツールの比較（PyCG と Pyan）
- 関数単位の検出器が手続き間の脆弱性に弱いことの測定（Li et al. ICSE 2024）
- パターン系とテイント系の SAST の比較（PyFlow、ICSE 2026）

深さの上限 4 については、Joern の既定値が 4 だという記述が見つかった。

### Cited Findings

- **[◎] PyCG（ICSE 2021）**（成分 6）
  - Pyan の recall が低い理由: "it does not track the inter-procedural flow of functions, which is the reason why it has low recall. ... Pyan ignores such calls which in turn leads to a 7.6% recall."
  - これは同じ条件でのアブレーションではなく、別のツールどうしの比較である。
- **[○] Li, Wang, Zou, Li, Zhang, Xu, Zhang, Jin, "On the Effectiveness of Function-Level Vulnerability Detectors for Inter-Procedural Vulnerabilities", ICSE 2024**（成分 6）
  - "(i) inter-procedural vulnerabilities are prevalent with an average of 2.8 inter-procedural layers; and (ii) function-level vulnerability detectors are much less effective in detecting to-be-patched functions of inter-procedural vulnerabilities than detecting their counterparts of intra-procedural vulnerabilities."
  - ただし対象は深層学習の検出器である。
  - 出典: [arXiv 2401.09767](https://arxiv.org/abs/2401.09767)
- **[◎ 部分] Team Atlanta, "ATLANTIS" 技術報告（AIxCC 優勝、arXiv 2509.14589）**（成分 6。深さ上限の根拠）
  - "Joern's default call depth limit is four, which is not practical. Attempts to increase this depth resulted in excessive resource consumption, leading to timeouts or out-of-memory errors in most cases."
  - 出典: [arXiv 2509.14589](https://arxiv.org/abs/2509.14589)
- **[◎ 部分] PyFlow（2026）**（成分 6）
  - 8 ツールを "pattern- and heuristic-based category"（DevSkim、Dlint、Bandit、Bearer、Semgrep）と "production grade interprocedural taint trackers"（CodeQL、Pysa、Snyk）に分けて比較した。
  - ICSE 2026 の研究のベンチマークを使っている。**ツールの種類の比較であり、深さのアブレーションではない。**
- **[◎] Laursen et al. PLDI 2024**
  - 近似解釈の有無で、解決率、到達可能な関数、recall を比べた（36 プロジェクトで recall 75.9% → 88.1%、著者の主張）。
  - **機能の有無のアブレーションとして、同じ型の先例である。**
- **[△] Smaragdakis, Bravenboer, Lhoták, "Pick Your Contexts Well", POPL 2011**、および文脈感度の後続研究
  - ポインタ解析では、文脈の深さを変えて precision の指標を比べるのが定番である（検索要約）。
  - ただしこれは文脈の深さであって、呼び出しの深さや再現率ではない。
  - 出典: [PDF](https://plg.uwaterloo.ca/~olhotak/pubs/popl11b.pdf)（未読）

### Inferences

- 深さ 0 のアブレーションは、「手続き間の効果推論が宣言照合の再現率に何件寄与するか」を同じ解析器の中で測る点で、比較的珍しい実験になりうる。
- ただし「パターン系とテイント系のツール比較（PyFlow、ICSE 2026）や、PyCG と Pyan の比較で実質的に分かっている」という反論が予想される。**同じ解析器の中で深さだけを変えている**ことを強調する必要がある。
- 深さ上限 4 が Joern の既定値と一致することは、根拠の一つとして引用できる。ただし ATLANTIS は「not practical」と評しているので、引用は慎重にすべきである。

### Gaps

- 「call depth」「depth 0」「ablation」「recall」の組み合わせでは、該当する研究はなかった（検索 17、33）。
- Bandit（手続き内）と Pysa や CodeQL（手続き間）を、同じ実データの CVE で比べた数値は、ICSE 2026 の原論文を読んでいないので未確認である。

---

## Q7. 複数の成分を組み合わせた先行研究（「同じ設計」のリスク）と総括

### Takeaway

**3 成分以上を組み合わせた先行研究は 2 件確認した。**

- **Felt et al. CCS 2011（Stowaway）**: 宣言と実効の照合、未解決の別群での報告、開発用の取り置き、手作業による precision の評価
- **Gao et al. ICSE 2017**: 修正コミットを正解にした再現率、unknown ラベルと時間予算、主評定者 1 名と較正

**事前登録、解析器の凍結、未解決率を主結果にすること、修正コミット由来の再現率の 4 つ以上を揃えた研究は見つからなかった。** MCP の注釈については、注釈語彙の使用を数えた 2026 年の論文（コードの解析ではない）があった。

### Cited Findings

- **[◎] Felt et al. CCS 2011 — 同一設計リスク：高**（D、2、3 に近い、5）
  - 宣言と実効の照合: "We compare that set to the permissions actually requested by the application. If the application requests more permissions, then it is overprivileged."
  - 未解決の別群報告、24 アプリの取り置き、40 アプリの手作業による分析（いずれも上で引用）。
  - **欠けている成分**: 事前登録、解析器の凍結、修正コミット由来の再現率（"We did not quantify Stowaway's false negative rate"）、評定者内信頼性。
- **[◎] Gao et al. ICSE 2017 — 同一設計リスク：中**（4、2、5）
  - 宣言と実効の照合ではない。型検査器による検出可能性を測る研究である。
  - 事前登録はない。ツールの版は固定している（Flow 0.30、TypeScript 2.0）が、凍結を手続きとして宣言してはいない。
- **[◎] Khan et al. TSE 2022 — 同一設計リスク：中**（4。Python）
  - Gao の Python 版。
- **[○] Gorla, Tavecchia, Gross, Zeller, "Checking app behavior against app descriptions", ICSE 2014（CHABADA）**（D）
  - "How do we know a program does what it claims to do?" 説明文の話題と API の使用を照合し、外れ値を検出した。
  - 方法論の成分 1〜6 には該当しない。
  - 出典: DOI [10.1145/2568225.2568276](https://doi.org/10.1145/2568225.2568276)
- **[◎ 部分] Lalaine（USENIX Sec 2023）**（D、5）
  - 宣言（プライバシーラベル）と実効（データフロー）の照合。
  - precision は 89.33%、recall は 60.6%（著者の主張）で、正解は人手で作っている。
  - 事前登録はない。未解決率の報告は確認できなかった。
- **[◎ 部分] Trofimov & Novikov, "When Tool Calls Succeed but Workflows Fail: Anomalies at the Agent–Tool Boundary", arXiv 2609.15397 (2026)**（D の隣接。MCP）
  - "measuring the use of the standard annotation vocabulary across 98,291 tools exposed by registered Model Context Protocol (MCP) servers"
  - 注釈が使われているかどうかを数えた研究で、コードとの照合ではない。成分 1〜6 は持たない。
- **[○] FUZZING ワークショップの RR**（3）
  - ツールの評価に事前登録を使うが、静的解析ではない。

### Inferences

**総括表**（判定は今回の検索範囲での判断）

| 成分 | 判定 | 根拠（代表） |
|---|---|---|
| 1. 未解決を数え、理由つきで報告する | **規範として確立し、JS の指標としては標準。Python のセキュリティ測定で主結果にする例は見つからない** | Soundiness 2015、Jelly（% resolved, Feldthaus 2013）、Monat 2020（unsoundness alarms）、Pysa（obscure model）、PyCG（定性的列挙のみ） |
| 2. unknown を三値目にして率を出す | **検証分野では標準。測定研究では稀だが先例がある** | SV-COMP（Unknown 0 点、timeout は Unknown）、Felt 2011（未解決群の分離）、Gao 2017（unknown と時間予算） |
| 3a. 事前登録 | **SE では標準（2020 年以降）。静的解析の測定への適用は見つからない** | Ernst & Baldassarre 2023、Empirical Standards RR、FUZZING RR（2022〜） |
| 3b. 評価前の解析器凍結 | **原理は確立（test snooping の回避）。凍結の手続き（tag と fingerprint）の先例は見つからない** | Arp 2022 P3、Felt 2011（24 アプリの取り置き）、SV-COMP の検証器アーカイブ（規程は未読） |
| 4. 修正コミットを再現率の正解にする | **標準** | Thung 2012/2015、Gao 2017、Habib & Pradel 2018、Khan 2022、Tomassi 2021、Lipp 2022、Li 2023、Charoenwet 2024、Liu 2026。**注釈（宣言）の修正を正解にした例は見つからない** |
| 5. 単独評定と評定者内信頼性 | **正当化つきで許容されている。test-retest は単独研究者に推奨されているが、実践は稀** | Empirical Standards IRR 補遺、Kitchenham & Charters 2007、Harvey 2026（ACL 0.07% は孫引き）。反論の根拠は Empirical Standards の Repository Mining 基準 |
| 6. 深さ 0 アブレーション | **明示的な先例は見つからない（稀）** | PyCG と Pyan、Li ICSE 2024、PyFlow のツール類型比較、Joern の既定深さ 4 |
| 組み合わせ | **3 成分までの組み合わせはある（Felt、Gao）。4 成分以上は見つからない** | 上記 |

**AuthGap の新規性の書き方への示唆**

- 各成分を「新しい方法」と書くのは避け、「既存の規範（soundiness、RR、test-retest、修正コミット由来の再現率）を、宣言と実効を照合する静的測定の一つの設計に束ねた」と書くのが安全である。
- 成分単位で新規と言えそうなのは、次の 3 点だけである。
  - 注釈の修正コミットを正解にすること
  - 同じ解析器の中での深さ 0 アブレーション
  - Python での理由別の opaque 率を主結果にすること

**必ず引用すべき先例**

- Felt 2011（同型の設計）
- Soundiness 2015
- SV-COMP の Unknown
- Gao 2017 と Khan 2022
- Habib & Pradel 2018
- Ernst & Baldassarre 2023 と Empirical Standards
- Kitchenham & Charters 2007
- Arp 2022

### Gaps

- 検索は英語中心で、ACM DL と IEEE Xplore の全文検索は使えなかった（403）。Semantic Scholar API も大半が 429 で、引用網の追跡はできていない。「見つからなかった」は網羅的な否定ではない。
- MCP に特有の類似研究（静的解析による注釈の照合）は、ほかの調査担当の範囲として深追いしていない。

#### 検索ログ（実行順。「見つからなかった」も記録）

**WebSearch（standard）**

| # | クエリ | 結果 |
|---|---|---|
| 1 | `PyCG practical call graph generation Python unresolved calls precision recall` | PyCG を発見。未解決率の内訳はなし |
| 2 | `"On the Unsoundness of Static Analysis for Python" dynamic features` | **該当題名は見つからなかった**。Monat 2020 を発見 |
| 3 | `Habib Pradel "How many of all bugs do we find" static bug detectors Defects4J` | リポジトリのみ |
| 4 | `registered reports software engineering MSR ESEM Ernst Baldassarre` | 発見 |
| 5 | `soundiness manifesto "In defense of soundiness" Livshits CACM 2015` | 発見 |
| 6 | `Python call graph unresolved call sites fraction "dynamic features" empirical study Åkerblom` | **未解決率を報告した研究は見つからなかった** |
| 7 | `Thung Lo Jiang "To what extent could we detect field defects" static bug finders` | 発見 |
| 8 | `Laursen Xu Møller "Reducing Static Analysis Unsoundness with Approximate Interpretation" zero callees call sites` | 発見 |
| 9 | `Pysa obscure models unknown callee taint-in-taint-out documentation` | 発見 |
| 10 | `Felt "Android permissions demystified" Stowaway reflection resolved percentage overprivileged` | 発見（リフレクションの記述は PDF で確認） |
| 11 | `FUZZING workshop registered reports NDSS stage 1 stage 2 fuzzer evaluation` | 発見 |
| 12 | `Gao Bird Barr "To type or not to type" quantifying detectable bugs JavaScript fixed bugs 15%` | 発見 |
| 13 | `Khan Chen Mondal "empirical study of type-related defects in Python projects" mypy detect` | 発見（著者名を誤って入れており、正しくは Khan, Chen, Varró, McIntosh） |
| 14 | `preregistration computer security research measurement studies position paper` | **セキュリティの事前登録の SoK は見つからなかった** |
| 15 | `"intra-rater" reliability software engineering manual labeling single annotator re-labeled weeks later` | **SE での評定者内信頼性の実測例は見つからなかった** |
| 16 | `Lipp Banescu Pretschner "empirical study on the effectiveness of static C code analyzers for vulnerability detection" ISSTA 2022 real-world vulnerabilities` | 発見 |
| 17 | `intraprocedural versus interprocedural static analysis ablation detection recall vulnerabilities "intra-procedural" baseline comparison` | **直接のアブレーションは見つからなかった** |
| 18 | `Holkner Harland "Evaluating the dynamic behaviour of Python applications" ACSC 2009` | 発見 |
| 19 | `ACM SIGSOFT Empirical Standards inter-rater reliability "not always" qualitative single coder` | McDonald 2019 を発見。基準の本文は raw ファイルで取得 |
| 20 | `PyAnalyzer dependency extraction Python ICSE 2024 dynamic features possible dependencies evaluation` | 要約のみ |
| 21 | `SV-COMP verdict unknown scoring "unknown" result counted competition report Beyer` | 発見 |
| 22 | `Di Grazia Pradel "evolution of type annotations in Python" commits FSE 2022` | 要約のみ |
| 23 | `privacy label code consistency static analysis apps "could not be analyzed" inconclusive Lalaine USENIX Security 2023` | **解析不能の扱いは見つからなかった** |
| 24 | `"registered report" static analysis tool warnings empirical study MSR EMSE` | **見つからなかった** |
| 25 | `MCP server tool annotations readOnlyHint destructiveHint mismatch static analysis measurement study` | arXiv 2609.15397（注釈の使用状況の調査のみ） |
| 26 | `Cockburn Gutwin Dix "HARK no more" preregistration CHI experiments` | 発見 |
| 27 | `static analysis evaluation "held-out" projects "development set" tuned checker evaluated unseen projects avoid overfitting rules` | **凍結や取り置きの直接の先例は見つからなかった** |
| 28 | `Bandit intraprocedural vs CodeQL Pysa interprocedural Python vulnerability detection comparison recall study` | PyFlow 2026 を発見 |
| 29 | `"How Many of All Bugs Do We Find" Habib Pradel abstract "594" bugs detectors find` | **アブストラクトは見つからず**、OpenAlex で取得 |
| 30 | `Åkerblom Stendahl Tumlin Wrigstad "Tracing dynamic features in Python programs" abstract eval exec getattr usage` | **見つからず**、OpenAlex で取得 |
| 31 | `Kitchenham Charters 2007 guidelines systematic literature reviews single researcher "test-retest" data extraction PhD students` | 発見（PDF で確認） |
| 32 | `Arp "Dos and Don'ts of Machine Learning in Computer Security" data snooping pitfall test set tuning` | 発見 |
| 33 | `"call depth" limit ablation static analysis recall "depth 0" OR "depth of 0" interprocedural taint evaluation vulnerabilities found` | **深さ 0 のアブレーションは見つからなかった**。ATLANTIS と Chakraborty 2022 を発見 |
| 34 | `Smaragdakis Bravenboer Lhoták "Pick your contexts well" context-insensitive vs context-sensitive precision metrics comparison` | 要約のみ |

**arXiv API**

| # | クエリ | 結果 |
|---|---|---|
| a | `ti:"registered reports"` | Ernst & Baldassarre、TENSURE（RR）、Java buildability（RR）などを発見 |
| b | `ti:jarvis AND ti:"call graph"` | 0 件 |
| c | `ti:scalpel` | 2202.11840 |
| d | `ti:headergen` | 0 件 |
| e | `ti:pyanalyzer` | 0 件 |
| f | `ti:"call graph" AND ti:python` | PyCG、Jarvis、LLM の研究 |
| g | `ti:"static bug detectors"` | 0 件 |
| h | `abs:"registered report" AND abs:"static analysis"` | **0 件** |
| i | `abs:"pre-registered" AND abs:"static analysis"` | **0 件** |
| j | `abs:"preregistration" AND cat:cs.CR` | **0 件** |
| k | `abs:"registered report" AND cat:cs.CR` | 無関係な 1 件 |
| l | `abs:MCP AND abs:annotations AND abs:static` | 無関係 |
| m | `ti:registered AND ti:report AND abs:static AND abs:analysis` | **0 件** |
| n | `ti:registered AND ti:report AND abs:vulnerab` | **0 件** |
| o | `abs:preregistered AND abs:analyzer` | 無関係 |

**そのほかの取得経路**

- Semantic Scholar API: タイトル検索 18 件のうち、半数以上が HTTP 429 で失敗した。
- OpenAlex API（DOI 指定）: 9 件のアブストラクトを取得した（Habib、Thung ×2、Åkerblom、Sui、CHABADA、HARK、Qiu、McDonald）。タイトル検索 4 件は 429 で失敗した。
- WebFetch:
  - CACM の全文、ACM DL、MSR 2026 の RR ページの募集要項部分: 403 または取得できなかった。
  - SMU の Thung のページ: 空だった。
