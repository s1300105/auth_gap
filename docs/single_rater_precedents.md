# 判定者が 1 人の研究の先例と、その扱い方（調査記録）

調べた日: 2026-10-05。記録者: 本記録者（Claude）。`authgap/` は変えていない。

**引用はすべて `scripts/verify_quote.py` で原文と照らした。** 結果は
`evidence/single_rater_precedents/verify.json`（93 件。exact 88、fetch_failed 3、none 2。失敗も残してある）。
表の「確認 id」はこのファイルの `id` を指す。[確認] は exact か loose で一致したもの、[未確認] は検索の要約でしか見ていないもの。

---

## 結論

1. **判定者 1 人の設計は、上位の会場にも載っている。** 照合済みの 14 事例のうち 7 件は CORE の A* の会場
   （うち 4 件はセキュリティの 4 大会議）、4 件は A、3 件は arXiv のみだった。B 以下の会場の事例は今回集めていない。
2. **ただし上位の会場の事例は、ほぼすべて何かで補っている。** 他の著者が結果を点検・議論する（NDSS'24）、上の人の指導の下で
   行う（CCS'19）、決められないものを「uncertain」として外す（USENIX Sec'20）、一部を独立の判定者に見せる（ICSE'19）、
   最初に複数人で基準をそろえてから 1 人で続ける（TOSEM）。何も補わずに 1 人で数値の判定をした例は、上位の会場には見つからなかった。
   S&P'24 の 1 人のコーディングは、面接の質的分析で、方法論（reflexive TA）を理由に挙げている。AuthGap の判定とは種類が違う。
3. **方法論の指針は「条件つきで認める」と「複数人を求める」の両方がある。** ACM SIGSOFT の Empirical Standards は、
   1 人の判定を「理由を書けば可」とし、論争になりにくい判定・複数人が非現実的な場合を挙げる。一方で同じ標準のリポジトリ
   マイニングの項は手作業の注釈に複数人を求める。Baltes ほか（EMSE 2026）は「価値の衝突が小さいときだけ」1 人でよいとする。
4. **AuthGap に一番近いのは、道具の警告を 1 人が正誤判定した CryptoGuard（CCS'19）と CauSec（arXiv）、決められないものを
   外した PoliCheck（USENIX Sec'20）。** 時間をおいた同じ人の判定し直し（intra-rater）を使った先例は EMSE と ICSE に 1 件ずつある。
   ただし同じ人の一致は「時間による揺れ」しか測れず、判定者による偏りは測れない（McDonald ほかが Krippendorff を引いて
   区別している）。これは本記録者の読みも含む（下の「AuthGap に当てはめると」）。

**注意: この 14 事例は「1 人の判定の例」を探して集めたもの。** 上位の会場で 1 人の判定がどれくらいの割合あるかは、
ここからは言えない。

---

## 1. 調べ方

- 検索（WebSearch）で候補を拾い、原文（arXiv の HTML、著者・会議の PDF）を取って、判定者の数を書いた文を抜き出した。
- 抜き出した文を `verify_quote.py --batch` で原文と照合した。PDF から取った文には合字（ﬁ、ﬂ）や行末のハイフン（`inde- pendently`）が
  そのまま入っている。PDF の文字列がその形なので、その形で照合した（`F02_koc_ascii_first` は合字を普通の `fi` にした版で、
  一致しなかった記録）。
- 会場の水準は、CORE の順位表（portal.core.edu.au）と CSRankings の会場表（GitHub の `util/csrankings.py`）で確かめた。
  - 会議は **ICORE2026**、論文誌は **CORE2020**（CORE の論文誌の順位はこの版が最新として表示された）。
  - **どちらも今の順位で、論文が出た年の順位ではない。**
  - 「セキュリティの 4 大会議」（USENIX Security・CCS・NDSS・S&P）は通称。根拠として、CORE で 4 つとも A* であることと、
    CSRankings の会場表に 4 つとも載ることを照合した（`V_core_*`、`V_csr_*`）。

---

## 2. 事例の表

### 2.1 類の定義

- **(a)** 主な判定を 1 人がした（または各件を 1 人ずつが受け持った）。判定者間の一致の数値は出していない。
- **(b)** 1 人が大部分または残りを判定し、別の人が一部を判定して一致を確かめた（基準合わせの後に 1 人で続ける形を含む）。
- **(c)** 同じ人の時間をおいた判定し直し（intra-rater）を信頼性の確かめ方に使った。

### 2.2 一覧（照合済み 14 件）

| # | 論文 | 会場 | 種類 | 会場の水準（根拠） | 年 | 何を判定したか | 判定者の数 | 一致の確かめ方 | 類 | 確認 id | 印 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Ami, Moran, Poshyvanyk, Nadkarni "False negative - that one is going to kill you" | IEEE S&P | 会議 | A*（ICORE2026）、4 大会議 | 2024 | 開発者 20 人への面接の書き起こしのコーディング | **1 人**（single-coder） | 数値なし。方法論（reflexive TA）として 1 人を選んだと明記 | a | E01_* | [確認] |
| 2 | Rahaman ほか "CryptoGuard" | ACM CCS | 会議 | A*（ICORE2026）、4 大会議 | 2019 | 暗号 API の誤用の警告（Apache の 1,295 件）が真か偽か | **1 人**（2 年目の博士課程の学生 = 第 2 著者） | 数値なし。教員と第 1 著者の「close guidance」の下 | a | E02_* | [確認]（arXiv 版の脚注で照合） |
| 3 | Chen, Liu, Wu, Le, Chau "Towards Precise Reporting of Cryptographic Misuses" | NDSS | 会議 | A*（ICORE2026）、4 大会議 | 2024 | 暗号の誤用検出器の誤警報の原因の分析 | **検出器ごとに 1 人** | 数値なし。結果を他の著者が点検・議論 | a | E03_* | [確認] |
| 4 | Andow ほか "PoliCheck" | USENIX Security | 会議 | A*（ICORE2026）、4 大会議 | 2020 | データの流れ（180 件）がプライバシーポリシーに書かれているか | **3 人のうち 1 人**（"one-of-three authors"。各件を 1 人が見たと読める。本記録者の読み） | 数値なし。迷った 27 件を「uncertain」として精度の分母から外す。ambiguous な開示は評価に入れない | a | E04_* | [確認] |
| 5 | Rahman, Parnin, Williams "The Seven Sins" | ICSE | 会議 | A*（ICORE2026） | 2019 | IaC スクリプトの質的分析（565 時間）でセキュリティの臭いを導く | **1 人**（第 1 著者） | 臭いと CWE の対応づけだけ、著者でない 2 人が独立に確かめた | a | E05_* | [確認] |
| 6 | Charoenwet, Thongtanunam, Pham, Treude "An Empirical Study of Static Analysis Tools for Secure Code Review" | ISSTA | 会議 | A（ICORE2026） | 2024 | 静的解析の警告を CWE に対応づける | **主に 1 人**（第 1 著者） | 数値なし。経験 10 年超の第 3 著者が枠組みづくりと迷った警告に加わる | a | E07_* | [確認] |
| 7 | Khan ほか "CauSec" | arXiv のみ | arXiv | 水準なし（査読前） | 2026 | SAST の警告すべてが真か偽か | **1 人** | 数値なし。経験 15 年超の 2 人目が監督・点検。「この分野の大規模研究では 1 人の判定は普通」と書き、NDSS'24 と S&P'24 を引く | a | E12_* | [確認] |
| 8 | Koc, Wei, Foster, Carpuat, Porter "An Empirical Assessment of Machine Learning Approaches for Triaging Reports of a Java Static Analysis Tool" | ICST | 会議 | A（ICORE2026） | 2019 | FindSecBugs の報告が真か偽か（194 真・206 偽） | **大部分を 1 人**（第 1 著者） | 他の著者が無作為に選んだ一部を確かめた。件数と κ は書かれていない | b | E06_* | [確認] |
| 9 | Lin ほか "Leveraging Reviewer Experience in Code Review Comment Generation" | TOSEM | 論文誌 | A*（CORE2020） | 採録（arXiv の注記。年は未確認） | 生成したレビューコメントの注釈 | 基準合わせの後は **1 人**（第 1 著者が残り 1,100 件） | 2 人で回を重ね κ をそろえてから 1 人で続ける（1 回目で κ 0.86 の項目もある）。最後に第 2・第 5 著者が見直す | b | E08_* | [確認] |
| 10 | Galappaththi, Nadi, Treude "Does This Apply to Me?" | MSR | 会議 | A（ICORE2026） | 2022 | Stack Overflow の文に追加の文脈があるか | 試行の後は **各件 1 人**（残り 147 件を 3 人で分ける） | 試行 2 回は 3 人が同じ件を判定し Fleiss の κ | b | E09_* | [確認] |
| 11 | Majeed, Mahmoud, Nadi "An Empirical Study of Model Context Protocol Applications" | arXiv のみ | arXiv | 水準なし（査読前） | 2026 | MCP を使うアプリの分類（5 つの次元） | 50 件中、2 人で 29 件、**残り 20 件は 1 人** | 2 人分の 29 件で α 0.82（まとめた値） | b | E13_* | [確認] |
| 12 | Ryan ほか "Unveiling Malicious Logic" | arXiv のみ | arXiv | 水準なし（査読前） | 2025 | 悪性 Python パッケージのコード（悪性の指標の位置） | **1 人**（第 1 著者） | 第 1・第 2 著者が 37 件（標本の 10%）を独立に判定し κ を計算（値は未確認） | b | E14_* | [確認] |
| 13 | Liebel, Chakraborty "Ethical Issues in Empirical Studies using Student Subjects" | Empirical Software Engineering | 論文誌 | A（CORE2020） | 採録（arXiv の注記。年は未確認） | 文献の除外と情報の抽出 | **1 人**（第 1 著者） | 査読の後で足した: 第 2 著者が 10% を独立に判定（inter）、第 1 著者が約 20 か月後に除外をやり直す（intra、κ≈0.836） | c（b も） | E10_* | [確認] |
| 14 | Cummaudo, Vasa, Barnett, Grundy, Abdelrazek "Interpreting Cloud Computer Vision Pain-Points" | ICSE | 会議 | A*（ICORE2026） | 2020 | Stack Overflow の質問の分類 | 4 人で分担（第 1 著者が 475 件） | 第 1 著者が同じ 50 件を 2 回（2019-06-28 と 2019-08-09）判定（intra）。そのうえで他の判定者との inter | c | E11_* | [確認] |

### 2.3 判定者の数を書いた原文（英語）

各行は `verify.json` で exact に一致した。

1. Ami ほか（S&P 2024）
   - "We chose a single-coder approach, which is considered “good practice for reflexive TA”, as it helps interpretation, or “meaning-making”, from data"
   - "One of the authors systematically transcribed the audio records while anonymizing the text."
   - URL: https://arxiv.org/html/2307.16325v3 （会場は https://amitsealami.com/false-negatives-kill/ の "IEEE Symposium on Security and Privacy 2024"）
2. CryptoGuard（CCS 2019）
   - "the manual confirmation of alerts was conducted by a second-year Ph.D. student with a prior Master degree in cybersecurity (the second author), under the close guidance of a professor and a senior Ph.D. student (the first author)"
   - "manually analyzing 1,295 Apache alerts and confirming 1,277 true positives (98.61% precision)"
   - URL: https://arxiv.org/pdf/1806.06881 （arXiv 版。会場は https://experts.arizona.edu/en/publications/cryptoguard-high-precision-detection-of-cryptographic-vulnerabili/ の "CCS 2019 - Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security"）
3. Chen ほか（NDSS 2024）
   - "The root cause analysis for each detector is conducted inde- pendently by one of the authors, and the analyzed results are checked and discussed by the other authors."
   - URL: https://www.ndss-symposium.org/wp-content/uploads/2024-1032-paper.pdf
4. PoliCheck（USENIX Security 2020）
   - "For validation, one-of-three au- thors began by reading through the sentences that were ex- tracted from each privacy policy to ensure correctness of policy statement extraction."
   - "If it is not apparent and there is any uncertainty, we mark the ﬂow as “uncertain” to avoid bias. Note that we marked 27 ﬂows as uncertain"
   - "Note that we do not evaluate ambiguous disclosures, as attempting to resolve ambiguity injects annotator bias into the evaluation."
   - "Our dataset consists of 180 data ﬂows across 166 apps."
   - URL: https://www.usenix.org/system/files/sec20-andow.pdf
5. The Seven Sins（ICSE 2019）
   - "The ﬁrst author conducted the qualita- tive analysis."
   - "We mitigate this limitation by recruiting two independent raters who are not authors of the paper."
   - "Our qualitative analysis process to identify seven security smells took 565 hours."
   - URL: https://akondrahman.github.io/files/papers/icse19_slic.pdf （会場は https://neverworkintheory.org/2021/11/23/security-smells-in-infrastructure-as-code-scripts.html の "Proc. International Conference on Software Engineering (ICSE), 2019"）
6. Charoenwet ほか（ISSTA 2024）
   - "The mapping process is conducted primarily by the first author."
   - "the third author, who has over 10 years of experience in software security testing, joined the first author to establish the foundational framework and assisted with ambiguous warnings encountered along the process."
   - URL: https://arxiv.org/html/2407.12241v1 （会場は arXiv の注記 "Accepted by ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA) 2024"）
7. CauSec（arXiv）
   - "One author manually validated these alerts to label them as true or false positives, using the alert description, the offending line of code, and the surrounding source-code context"
   - "While single-researcher extraction and labeling are common in large-scale studies in this area"
   - "To mitigate this risk, a second researcher with more than fifteen years of experience in vulnerability analysis reviewed the extracted assumptions, supervised the labeling process, and independently reviewed the causal modeling decisions, results, and findings."
   - "This process, which took approximately 4.5 person-months"
   - URL: https://arxiv.org/html/2608.18876
8. Koc ほか（ICST 2019）
   - "The ﬁrst author performed most of the labeling work while other authors veriﬁed a random selection of labelings."
   - "resulting in 194 true and 206 false positives as ground-truth"
   - URL: https://www.cs.tufts.edu/~jfoster/papers/icst19.pdf （会場は https://sites.google.com/cs.umd.edu/ukoc/home の "2019 12th IEEE Conference on Software Testing, Validation and Verification (ICST)"）
9. Lin ほか（TOSEM）
   - "the first author annotated the remaining 1,100 comments independently. Finally, the annotations were reviewed by the second and fifth authors."
   - "Given that near perfect agreement was achieved, we omitted the second round and the first author performed the annotations on the remaining sampled comments."
   - "The annotators reached 93% agreement with a Cohen’s kappa of 0.86 (near perfect agreement) in the first round."
   - URL: https://arxiv.org/html/2409.10959
10. Galappaththi ほか（MSR 2022）
    - "In the first round, three authors annotate the same 30 threads."
    - "We then distribute the remaining 147 among the three authors to review individually."
    - URL: https://arxiv.org/pdf/2204.00110
11. Majeed ほか（arXiv。MCP）
    - "Two authors independently labeled 29 of the 50 repositories across all five MCPAppTax dimensions"
    - "one author then labeled the remaining 20 repositories using the refined criteria."
    - URL: https://arxiv.org/html/2607.25635
12. Ryan ほか（arXiv）
    - "The first author then manually examined the raw code and wrote free-form descriptions of the malicious logic."
    - "the first and second authors independently annotated a randomly selected subset of 37 packages (10% of the sample)."
    - URL: https://arxiv.org/html/2512.12559v1
13. Liebel, Chakraborty（EMSE）
    - "Initially, we did not perform any reliability checks, as we deemed the exclusion and extraction process to be comparably objective."
    - "However, in a first revision of this paper we added inter-rater and intra-rater reliability checks in a post-study fashion."
    - "Additionally, the first author re-did his exclusion approximately 20 months after the original process."
    - "For voluntariness, the lower agreement was due to the first author being inconsistent in the original extraction"
    - URL: https://arxiv.org/html/2102.13387
14. Cummaudo ほか（ICSE 2020）
    - "Firstly, intra-rater agreement by the first author was conducted twice on 28 June 2019 and 9 August 2019."
    - "475 posts were classified by the first author and three other research assistants"
    - URL: https://arxiv.org/pdf/2001.10130

### 2.4 会場の水準で分けると

| 水準 | 件数 | 事例 | 主な判定に 2 人目の一致の数値があるか |
|---|---|---|---|
| A* / 4 大会議 | 7 | S&P'24（1）、CCS'19（2）、NDSS'24（3）、USENIX Sec'20（4）、ICSE'19（5）、TOSEM（9）、ICSE'20（14） | 数値があるのは TOSEM（基準合わせの κ）と ICSE'20（intra と inter）だけ。4 大会議の 4 件は**どれも数値なし** |
| A | 4 | ICST'19（8）、ISSTA'24（6）、MSR'22（10）、EMSE（13） | ICST は件数・κ なし。ISSTA は数値なし。MSR と EMSE は数値あり |
| B 以下 | 0 | （今回は集めていない） | — |
| ワークショップ / arXiv のみ | 3 | CauSec（7）、MCP アプリ（11）、悪性パッケージ（12） | 11 と 12 は数値あり。7 は数値なし |

**読み取れること（本記録者の読み）:**

- 1 人の判定は下位の会場だけのものではない。4 大会議の 4 件はどれも、主な判定の一致を数値で示していない。
- ただし、その 4 件はどれも何かで補っている。数値の代わりに、他の著者の点検・議論（3）、上の人の指導（2）、決められないものの
  除外（4）、質的研究の方法論の理由（1）を書いている。
- ソフトウェア工学の会場（ICSE・TOSEM・MSR・EMSE）では、基準合わせの κ や intra-rater の数値を添える例が多い。
  EMSE の 13 は、数値を**査読の後で足した**と自分で書いている（"in a first revision of this paper"）。審査者が求めたと読めるが、
  原文はそこまで書いていない。
- **採録されたことは、審査者が 1 人の判定を良しとした証拠にはならない。** 限界として受け入れた可能性もある。

### 2.5 AuthGap に近い先例（related_work.md に載っているもの）で、判定者の数を確かめた結果

| 先例 | 判定者の数 | 原文 | 印 |
|---|---|---|---|
| Stowaway（Felt ほか、CCS 2011） | **書かれていない**。"We then manually analyzed each overprivilege warning to attribute it to either tool error (i.e., a false positive) or developer error." と主語は "we" だけ | https://people.eecs.berkeley.edu/~daw/papers/androidperm-ccs11.pdf （`X01_*`） | [確認]（数が書かれていないことを確認） |
| PoliCheck（Andow ほか、USENIX Sec 2020） | 3 人のうち 1 人（上の表の 4） | 同上 | [確認] |
| HintLint の報告書（査読なし） | **人の数は書かれていない**。"Every finding was then re-verified against source automatically" と、自動の再確認を書く。"Five findings did not survive review." とあるが、誰が見たかは書かれていない | https://raw.githubusercontent.com/complira/hintlint/5a51f2a43a4875c5297f29b4f2ac4ee26c6e8c37/docs/Report_HintLint.pdf （`X02_*`） | [確認]（数が書かれていないことを確認） |

---

## 3. 方法論の指針

### 3.1 条件つきで 1 人を認めるもの

**ACM SIGSOFT Empirical Standards の「Inter-Rater Reliability and Agreement」の補遺**
（https://www2.sigsoft.org/EmpiricalStandards/docs/supplements 、`G01_*`）[確認]

- "There is no universal rule to determine when two or more raters are necessary."
- 考える点として、次の 2 つを挙げる。
  - "Controversiality: the more potentially controversial the judgment, the more we need multiple raters"
  - "Practicality: the less practical it is to have multiple raters, the more reasonable a single-rater design becomes"
  - 同じ箇所の例: 先に決めた演繹的なコード表を当てはめるのは、複数人でも実行しやすい側に置かれている
    （"multiple raters applying an a priori, deductive coding scheme to some artifacts is more practical than multiple raters inductively coding 2000 pages of interview transcripts"、`G01_sigsoft_irr_deductive`）。
- 必須の項目（Essential）: "provides reasonable justification for using a single rater"（または複数人の手続きと一致の数値）。
- 審査者がしてはいけない批判（Invalid Criticisms）:
  - "Criticizing use of a single rater where multiple raters would be impractical or inconsistent with the study's underlying philosophy."
  - "Criticizing use of a single rater when the data is such that there is no reason to suspect different raters would reach different conclusions."

**Baltes ほか "Guidelines for Empirical Studies in Software Engineering involving Large Language Models"（EMSE 2026）**
（原稿の repo、commit 2c0b382 の `_guidelines/07_use-human-validation-for-llm-outputs.tex`、`G03_*`）[確認]

- "A single human judge is appropriate only when judgments depend on widely accepted theories and involve limited value conflict (e.g., tagging method names containing abbreviations)."
- 複数人で基準をそろえた後なら 1 人で続けてよい: "Once this target is reached and sustained for two to three groups, it is permissible to continue with a single rater."
  （target は直前の文 "The goal is to reach a target IRA or IRR (e.g., Krippendorff's $\alpha>0.8$), indicating sufficient decision rules." の一致の目標。`G03_baltes_target`）
- この指針は LLM を使う研究のためのもの。人の判定の部分を一般の手作業の判定に当てはめるのは、本記録者の外挿。

**McDonald, Schoenebeck, Forte "Reliability and Inter-rater Reliability in Qualitative Research"（PACM HCI、CSCW 2019）**
（NSF の公開版 https://par.nsf.gov/servlets/purl/10176357 、`G04_*`）[確認]

- IRR が意味を持たない場合: "Pragmatic examples include when developing codes is part of the process, when there is a single researcher, when researchers are embedded in the research context, where analysis is driven by participants’ own interpretations of their data, or when coding requires little interpretation."
- 信頼性の種類として、Krippendorff の分け方を引く: 判定者の間の再現性とは別に "stability or consistency of a single coder’s use of codes over time"。
  → 同じ人の判定し直しが測るのはこちら（安定性）で、判定者の間の再現性ではない。

### 3.2 複数人を求めるもの（反対側の指針）

**SIGSOFT Empirical Standards の Repository Mining の標準**（https://www2.sigsoft.org/EmpiricalStandards/docs/standards 、`G02_*`）[確認]

- 必須の項目（Essential Attributes）の中に: "if manual annotations are carried out: uses multiple annotators; reports the number of annotators"
- 同じ標準群の IRR の補遺は 1 人を条件つきで認めるので、**標準の中で強さが違う**。リポジトリマイニングとして書く論文では、
  審査者がこちらを当ててくる可能性がある（本記録者の読み）。

**McDonald ほか（同上）** — IRR が役に立つ場合: "which might include ensuring consistency across multiple coders, for applying existing codebooks, and when researchers aim to report quantitative results."
→ 既存のコード表を当てはめ、量的な結果を出す研究は、IRR が役に立つ側に入る。

**Evertz ほか "Chasing Shadows"（NDSS 2026）**（artifact repo、commit 8ecb724 の `website/index.html`、`G05_*`）[確認]

- LLM が付けたラベルについての推奨: "If scale makes that infeasible, conduct a manual audit of a statistically meaningful subset with multiple annotators, reporting inter-annotator agreement and confidence intervals."
- 対象は LLM のラベル。人 1 人のラベルに直接当てはまる文ではない。

---

## 4. AuthGap に当てはめると（ここからは本記録者の読み）

### 4.1 AuthGap の判定の形

- 解析器の出した矛（CONTRADICTION）を、学生 1 人が真か偽か判定する（D67 の 4）。判定の手引きは判定の前にコミットする。
- 判定の根拠（ファイルと行）を全件公開する。決められないものは「不明」として理由を書く。
- 一致の確認は D73 の 1: seed ⑥ の 10% を、2 人目がいればその人が、いなければ 2 週間以上あけて学生が判定し直す
  （`docs/final_evaluation_procedure.md` 21 の 5）。

### 4.2 一番近い形

1. **CryptoGuard（CCS'19）と CauSec（arXiv）**: 静的解析の警告を 1 人が真か偽か判定した。AuthGap と課題の形が同じ。
   どちらも数値の一致は出さず、指導・監督する人がいたと書く。
2. **PoliCheck（USENIX Sec'20）**: 宣言（ポリシー）と実際の動作の一致を、1 人ずつが判定した。迷ったものを "uncertain" として
   分母から外し、外した数（27）を書いた。AuthGap の「不明」の扱いとよく似ている。ただし AuthGap は不明を外して黙らず、別に数える。
3. **Liebel, Chakraborty（EMSE）と Cummaudo ほか（ICSE'20）**: 同じ人の判定し直し（intra-rater）。AuthGap の D73 の 1 の
   「2 人目がいないとき」と同じ形。EMSE の方は約 20 か月あけ、食い違いの原因（第 1 著者の不一致）を書いて該当の項目を全部やり直した。
   **AuthGap は食い違っても元の判定を直さず報告する**（21 の 5）ので、この点は違う。

### 4.3 指針に照らすと

- **論争になりにくいか（SIGSOFT の Controversiality、Baltes の value conflict）**: AuthGap の判定には記録された価値の衝突がある
  （`docs/llm_judgment_survey.md` §2.4 の指摘、D67 の 1）。原理（`docs/contradiction_principles.md`）を先に固めて、判定を
  「手引きの当てはめ」に近づけたことは、論争を減らす根拠として書ける。ただし Baltes の基準を満たすとまでは言えない。
- **複数人が非現実的か（Practicality）**: 先に決めた手引きの当てはめは、SIGSOFT の例では「複数人でも実行しやすい」側に入る。
  「2 人目を用意できない」理由は、手引きの性質ではなく人の手配の事情として正直に書くのがよい。
- **量的な結果を出すか（McDonald）**: AuthGap は精度という数を出すので、IRR が役に立つ側に入る。審査者がここを突く可能性は高い。
- **intra-rater で示せること・示せないこと**: 判定し直しは、同じ人が同じ手引きで同じ結論に着くか（安定性）を示す。
  判定者による偏り（再現性）は示せない。`docs/final_evaluation_procedure.md` の 21 の 5 にも同じことが書いてあり、先例の読み方と合う。

### 4.4 論文での書き方の案（英語。案であって、決定は学生）

> All judgments were made by a single rater (the first author), using a judging guide committed before any judgment
> (commit `<hash>`). A second rater was not available; following the ACM SIGSOFT Empirical Standards, we state this as a
> limitation and justify it as follows: (i) the guide fixes the decision rules in advance, (ii) every judgment is
> released with the file and line that support it, and (iii) items the rater could not decide are reported as
> "unknown" rather than dropped. To estimate rater stability, the rater re-judged a random 10% of the items at least
> two weeks later without seeing the original labels; we report agreement and κ. This measures intra-rater stability,
> not inter-rater reproducibility, and disagreements were reported without changing the original labels.

- 先例として引くなら: 1 人の判定は CryptoGuard（CCS'19）・NDSS'24 の Chen ほか、宣言と動作の照合の判定は PoliCheck（USENIX Sec'20）、
  intra-rater は Liebel, Chakraborty（EMSE）と Cummaudo ほか（ICSE'20）。
- 2 人目を段階 6 までに用意できるなら、Baltes の手順（複数人で数回 α > 0.8 をそろえてから 1 人で続ける）と、TOSEM の Lin ほか・
  MSR の Galappaththi ほかの形が使える。これは 1 人だけの判定より、指針に照らして強い。

---

## 5. 確かめられなかったもの

- **McDonald ほかの ACM DL の版**: `dl.acm.org` は 403 で取れなかった（`F01_mcdonald_acm_dl`）。NSF の公開版で照合した。
  NSF の版はページの見出しに別の論文誌の名前が残っている（"ACM Trans. Graph., Vol. X, No. X, Article X. Publication date: November 2019."、`G04_mcdonald_header`）。採録原稿と読める。出版版と文言が同じかは未確認。
- **SIGSOFT の IRR の補遺の GitHub の原稿**: `raw.githubusercontent.com` の推測したパスは 404（`F05_sigsoft_irr_rawgithub`）。
  公開のサイトのページで照合した。どの版のページかは記録していない（取得日時と sha256 は `verify.json` にある）。
- **PolicyLint（USENIX Sec 2019）で誰が 510 件の矛盾を確かめたか**: PDF に "one of the authors" は見つからなかった（`F04_policylint_who`）。
  判定者の数は不明。
- **Stowaway の古い URL**（`android-ccs11.pdf`）は 404（`F03_stowaway_old_url`）。`androidperm-ccs11.pdf` で照合した。
- **CryptoGuard の出版版**: 照合したのは arXiv 版の脚注。CCS の出版版に同じ脚注があるかは未確認（ACM DL が 403）。
- **Lin ほか（TOSEM）と Liebel, Chakraborty（EMSE）の出版年**: arXiv の注記で採録だけ確かめた。巻・号・年は未確認。
- **Ryan ほか の κ の値**: 計算したとは書いてあるが、値の位置を見つけていない。
- **Ami ほかの "single-coder approach" の根拠 [19]**（reflexive TA の文献）は開いていない。
- **検索の要約でしか見ていない候補**（数に入れていない）[未確認]:
  - "Secure Software Engineering in the Financial Services"（arXiv 2104.03476）: 「質的分析の大部分を第 1 著者が行い、第 2・第 3 著者が見直した」と要約に出た。
  - "Managing Security Issues in Software Containers"（arXiv 2504.07707）: 「第 1 著者が全書き起こしをコーディングし、第 2 著者が確かめた」と要約に出た。
  - "Privacy Engineering in the Wild"（arXiv 2211.08916）: 「基準合わせの後、第 1 著者が残り 27 件の書き起こしをコーディングし、IRR は計算しなかった」と要約に出た。
  - 自己承認の技術的負債（SATD）の研究（Potdar & Shihab ICSME 2014 など）: 第 1 著者が分類し、独立の判定者が統計的に有意な標本を確かめた、という形がよく引かれるが、原文は取れていない。
- **B 以下の会場の事例**: 探していない。「1 人の判定は下位の会場に多い」とも「少ない」とも、この記録からは言えない。
- **上位の会場での 1 人の判定の割合**: 測っていない（上の結論の注意を参照）。
