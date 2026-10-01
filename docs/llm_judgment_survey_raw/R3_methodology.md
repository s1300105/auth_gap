# LLM を研究の判定・注釈に使う方法論の調査（妥当性・再現性・査読での扱い）

## 0. 結論

**判定に LLM を混ぜる使い方は、あなたの研究ではほぼ使えません。使えるのは、原ソースを読む補助としてだけです。** 補助として使っても、判定と記録は本人が行い、そのことを開示して記録を残すのが条件です。

| 使い方 | AuthGap で | 主な根拠 |
|---|---|---|
| A. 解析器の判定の層に LLM を入れる（例: 「不」を LLM に決めさせる） | **今回は使えない** | 解析器は analyzer-freeze-3 で凍結済み（`docs/decisions.md:3743` D66）。原理 2-a に反する（「b / c は測定を既知の向きに偏らせる」`docs/contradiction_principles.md:138`。LLM が決めると、偏る向きさえ分からない）。`scan --determinism 3`（CLAUDE.md:104）の決定論も崩れる。将来、別の腕として事前登録するなら可能 |
| B. 最終評価の正解ラベルを LLM に付けさせる、または LLM のラベルを主指標にする | **使えない** | §1 の「人の判断の置き換え」の must、§3 の NDSS'26 P2、§2・§3 のセキュリティ判定の不安定さ |
| C. LLM を 2 人目の判定者の代わりにして κ を出す | **代わりにならない**。「人と LLM の一致」として副次的に出すのは可 | 一致は妥当性の証明にならない（§1）。判定者が 1 人であることの正当化は別の論点 |
| D. 原ソースを読む補助（根拠の行を探させ、人が開いて確かめてから判定・記録） | **条件つきで使える** | P2 の理想の対策「full manual verification」に当たる。条件は §8 |
| E. 人の無作為標本と LLM の全件ラベルを PPI で合わせ、区間を狭める | 使えるが任意。主の結果にはしない。事前登録が要る | §7 |

確かさの記号: 高 = repo のコード・依存関係・本文を自分で読んだ / 中 = 第三者の逐語の抜き書き / 低 = 検索の要約のみ。

## 1. SE の実証研究で LLM を使うときのガイドライン

**実在を確認した。確かさ: 高（論文の原稿 repo を clone して読んだ）。**
- 題: "Guidelines for Empirical Studies in Software Engineering involving Large Language Models"。Baltes ほか 22 名。EMSE 2026、DOI 10.1007/s10664-026-10922-3。版 2026.09（2026-09-17 公開）。
- 出典は `CITATION.cff`（https://github.com/se-uhd/llm-guidelines-paper 、commit 2c0b382）。llm-guidelines.org は遮断されていたが、この repo の CLAUDE.md に "The paper is authoritative" とあるので、原稿 repo を正本として読んだ。
- clone の場所: `/tmp/claude-0/-home-user-auth-gap/9d8a4d2c-1b03-53cb-ba04-44a67affb095/scratchpad/llmjudge/methodology/llm-guidelines-website/llm-guidelines-paper/`。以下の行番号はこの repo のもの。
- 8 項目: "(1) declare LLM usage and role; (2) report model versions, configurations, and customizations; (3) document the system and prompt design … (4) report session traces … (5) use suitable baselines, benchmarks, and metrics; (6) include an open LLM as a baseline; (7) validate LLM outputs against human judgment; and (8) articulate limitations and mitigations"（CITATION.cff の abstract）。

注釈者（annotator）と判定者（judge）の役で何を報告せよと言っているか:

- **役の宣言（must）**
  - `_summary/matrix.tex:23-24`: "must declare the specific role assigned to the LLM (e.g., annotator, judge …)"
- **モデルの版・設定・日付（must）**
  - `_guidelines/02_…tex:23`: "must report … (1) the exact model or tool name and version, (2) all parameters they configured that affect output generation, (3) the date of study execution"
  - `matrix.tex:33`: 判定者・注釈者では "including temperature and other sampling parameters"
- **温度 0 は保証にならない**
  - `02_…tex:74`: "Even with a temperature of 0, full determinism is rarely guaranteed"
  - `02_…tex:79`: "should not treat a temperature of 0 as a guarantee of reproducibility"
- **プロンプトの全文（must）**
  - `03_…tex:33-34`: "must report all prompts … The complete set must be made publicly available as supplementary material"
  - `matrix.tex:44`（判定者）: "must report the evaluation criteria, scales, and examples embedded in the prompt"
- **対話の記録（should）。Claude Code のような agent を使う場合は形式と版（must）**
  - `04_…tex:33`: "Where tool-native formats are used (e.g., Claude Code's session transcripts …), researchers must describe the file format and report the tool version."
  - v3 / v4 のように原ソースの確認を agent に分けたやり方はこれに当たる。
- **繰り返し（should）**
  - `05_…tex:54`: "Due to LLM non-determinism, researchers should repeat experiments …"
  - 同じ行で、LLM 判定者を繰り返し走らせたときは "should report the distribution of ratings per item"
- **open LLM の基準線（should）**
  - `06_…tex:79`: "For annotators and judges, researchers should compare annotation or judgment quality from open vs. commercial models"
- **人の判断の置き換え（条件つき must）**
  - `07_…tex:19`: "researchers must explain whether and how the replacement is justified … High inter-model agreement can reflect shared model biases … should additionally validate a sample against human experts"
- **判定者が 1 人のとき**（あなたの D67 の 4 に直接関わる）
  - `07_…tex:98`: "A single human judge is appropriate only when judgments depend on widely accepted theories and involve limited value conflict"
- **一致の閾値**
  - `07_…tex:38`: Krippendorff の "discarding data with α<0.667 … 0.667 ≤ α < 0.8 sufficient only for tentative conclusions … α ≥ 0.8 for reliable data"
- **標本の大きさの目安**
  - `07_…tex:47`: "related fields commonly use 100 comparisons without further justification"
- **限界の節（must）**
  - 判定者: `matrix.tex:94`: "must address measurement validity concerns, known biases such as position bias or verbosity bias"
  - 汚染: `08_…tex:42`: "researchers must discuss potential data leakage effects"
- **費用**
  - `08_…tex:93`: "Cost accounting tracks resource consumption by reporting tokens, service costs, or hardware specifications"。should 水準の緩和策として書かれている。
- **人の判断も悪くなりうる**
  - `_studytypes/01-05…tex:54`: "When LLM outputs are incorrect, they can negatively affect human judgment"
- **リダイレクトしてきたセキュリティ分野の調査も同じ方向**
  - NDSS'26 "Chasing Shadows: Pitfalls in LLM Security Research"（Evertz ほか）。確かさ: 高。artifact repo https://github.com/Dormant-Neurons/llm-pitfalls （commit 8ecb724）の `website/index.html` を読んだ。
  - 9 つの落とし穴のうち P2 Label Inaccuracy の推奨: "Disclose when labels or judgments come from LLMs. The ideal mitigation is full manual verification. If scale makes that infeasible, conduct a manual audit of a statistically meaningful subset with multiple annotators, reporting inter-annotator agreement and confidence intervals."
  - 同 abstract: "every paper contains at least one pitfall … only 15.7% of the present pitfalls were explicitly discussed"。対象は 72 本。

## 2. LLM を人の注釈者の代わり・追加として使った研究の結果

- **Ahmed, Devanbu, Treude, Pradel "Can LLMs Replace Manual Annotation of Software Engineering Artifacts?"**
  - MSR 2025、pp. 526-538、DOI 10.1109/MSR66628.2025.00086。実在の確かさ: 中（ガイドラインの bib と、検索結果の会議ページ）。
  - 内容（中、ガイドラインに残された逐語の抜き書き）:
    - "applying six state-of-the-art LLMs to ten annotation tasks from five datasets"
    - "we propose model-model agreement as a predictor of whether a given task is suitable for LLMs at all"
    - "replacing more than one human can inflate inter-rater agreement because model-model agreements are much higher"（`07_…tex:20`）
  - ガイドラインの評価（中、`07_…tex:57-61`）: 選別の閾値は "α>0.5"。"well below the levels generally considered acceptable"。"human-model agreement remained low on others"。
  - 課題の例として「メソッドの要約の正確さ」「コード変更が静的解析の警告を直すか」が挙がっている（低、検索の要約）。
  - **課題ごとの κ / α の数値は未確認**（本文を読めなかった）。
- **Wang ほか "Can LLMs Replace Human Evaluators? An Empirical Study of LLM-as-a-Judge in Software Engineering"**（ISSTA 2025）
  - repo の実在と課題（コード翻訳・生成・要約）は高: https://github.com/BackOnTruck/llm-judge-empirical の README に "accepted by ISSTA 2025"。
  - 結果（低、検索の要約）: 出力に基づく方法で人との Pearson 相関が翻訳 81.32、生成 68.51。性能は課題に依存し "ranging from near-human to unusable"。
- **Lubos ほか**（RE 2024。Llama-2 で要求文の品質を判定）
  - ガイドラインの要約（中、`01-02…tex:26`）: "moderate agreement for simple requirements and poor agreement for more complex requirements"。
  - **複雑になるほど一致が下がる。**
- **Camporese, Massacci, Gong "LLMs for Qualitative Data Analysis Fail on Security-specific Comments in Human Experiments"**（ICPC 2026、DOI 10.1145/3794763.3798172）
  - 低、検索の要約。セキュリティ固有の 9 つのコードで改善は一様でなく "not sufficient to reliably replace a human annotator"。
- **一般の注釈**
  - Wang ほか（CHI 2024、中）: "they are often erroneous for complex or domain-specific tasks"
  - Baumann ほか "Large Language Model Hacking"（arXiv 2509.08825、低）: 37 の注釈課題・18 モデルで、最先端のモデルでも仮説の約 3 つに 1 つで誤った結論になった。モデルとプロンプトを選べば、ほぼどんな結論も有意にできる。

## 3. LLM-as-judge の既知の偏りと、セキュリティ判定での誤り

**一般の偏り**
- **位置・冗長さ・自己優遇**
  - Zheng ほか（MT-Bench）"position, verbosity, and self-enhancement biases, as well as limited reasoning ability"（低、検索）。
  - 位置の偏りは FairEval の README（高、https://raw.githubusercontent.com/i-Eval/FairEval/main/README.md ）: "We reveal that LLMs exhibit severe positional bias"。
- **自己の出力の優遇**
  - Panickssery ほか（NeurIPS 2024、中）: "an LLM evaluator scores its own outputs higher than others' while human annotators consider them of equal quality"
- **迎合（sycophancy）**
  - Sharma ほか（Anthropic、高。https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models の abstract）: "RLHF may also encourage model responses that match user beliefs over truthful responses, a behavior known as sycophancy … five state-of-the-art AI assistants consistently exhibit sycophancy"
- **書式・偽の引用への偏り**
  - Chen ほか（EMNLP 2024、中）: "even the cutting-edge judges possess considerable biases"
- **選択肢の順序とプロンプトの書式**
  - 選択肢を並べ替えると "13% to 75%" の差（Pezeshkpour、中）。
  - 書式だけで "up to 76 percentage points"（Sclar。ガイドライン `_scope/01_motivation.tex:24`、中）。
- **判定者を騙す改変**
  - He ほか "LLM-as-a-Judge for Software Engineering"（TOSEM、DOI 10.1145/3797276、中）: "These attacks subtly alter software artifacts to deceive the judge into accepting flawed or malicious code."

**セキュリティ判定**
- **SecLLMHolmes**（IEEE S&P 2024）
  - repo と会議名は高: https://github.com/saadullah01/SecLLMHolmes の README。
  - 結果（低、検索）: 回答が非決定的で、推論が誤っていて忠実でない。関数名・変数名を変えるなどしただけで、PaLM2 と GPT-4 がそれぞれ 26% と 17% の場合で誤答に転じる。
- **Perry ほか**（CCS 2023）
  - repo の実在と会議名は高。
  - 結果（低）: AI を使った参加者は、より安全でないコードを書き、しかも安全だと思い込みやすかった。**人の過信の証拠。**

**MCP に固有の危険（推論。直接の文献は見つけていない）**
- 判定対象のコードには、LLM に読ませるための説明文（docstring・description）が入っている。
- この研究はまさに「宣言と実際の差」を測る。読み取り専用を名乗る文を LLM が信じれば、迎合や上の改変と同じ仕組みで「違反なし」に傾きうる。

## 4. 学会・出版社の方針

- **ACM Policy on Authorship（2026）**（中。ガイドラインの抜き書き `_guidelines/01_…tex:10`、`_scope/02_scope.tex:17`。bib 上の閲覧日は 2026-06-01）
  - "the specific use(s) of AI tools must be described in detail in the methods section of the Work"
  - "ACM no longer requires the disclosure … (as distinct from AI used in the conduct of the research itself"
  - **研究の遂行に使った AI は、方法の節に書く。**
- **ICSE 2027 Research Track**（中。第三者が集めた CFP 本文 https://github.com/doehyunbaek/sigsoft-das の `data/calls.csv`、2026-09-17 の snapshot）
  - ACM の旧い文面を引いている: "must be fully disclosed in the Work … in the Acknowledgements section"
  - IEEE: "shall be disclosed in the acknowledgements section"
  - "Submissions will be checked for hallucinated, fabricated, or unverifiable references."
- **FSE 2027 / ASE 2026**（中）: 同様に謝辞の節での開示。FSE は「ACM Policy on Authorship released September 16, 2025」と書いている。
- **食い違い（未解決）**: ACM の 2026 年の文面は方法の節、2027 年の CFP は謝辞の節。両方に書けば両方を満たせる。
- **ACM CCS 2026**（高。https://github.com/ACM-CCS-2026/CfP の `cfp.md:114-132`、commit 1934f9f）
  - 実質的な内容を生成した場合: "authors must include a dedicated 'Generative AI Usage' paragraph … explain how the authors validated the AI-generated content"
  - 幻覚の引用・捏造データは "desk rejected"。
- **USENIX Security '27・NDSS 2027・IEEE S&P 2027**（低、検索の要約）
  - いずれも利用は許し、開示と著者の責任を求めている。
  - 調べた範囲（すべて検索の要約）では、研究の測定器として AI を使う場合に触れた文言を見つけていない。

## 5. 再現性

- **クローズドなモデルは廃止される**（高。PyPI の anthropic 1.11.0 の `anthropic/resources/messages/messages.py:70-91` の `DEPRECATED_MODELS`）
  - 例: `"claude-3-opus-20240229": "January 5th, 2026"`、`"claude-sonnet-4-20250514": "June 15th, 2026"`、`"claude-sonnet-4-5": "November 30th, 2026"`。
  - 論文が出る頃には、判定に使ったモデルを呼べない可能性が高い。
- **seed も保証ではない**（高。openai 3.22.1 の `openai/types/chat/completion_create_params.py:267-273`）
  - "Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend."
- **温度 0 / 貪欲法でも非決定的**
  - ガイドライン `02_…tex:74-79`（高）。
  - Yuan ほか（NeurIPS 2025、中）: "greedy decoding does not guarantee deterministic outputs across different hardware and system configurations"
  - Atil ほか（中）。
  - Chen・Zaharia・Zou（中）: "the behavior of the "same" LLM service can change substantially in a relatively short amount of time"
- **ローカル実行の利点と限界**（高。vLLM の `docs/usage/reproducibility.md`、commit e12291d）
  - "vLLM does not guarantee the reproducibility of the results by default"
  - "only provides reproducibility when it runs on the same hardware and the same vLLM version"
  - ガイドライン `02_…tex:54`: ollama の tag と checksum を書けば、補足資料が "a true replication package" になる。
- **実態**
  - Angermeir ほか（中）: ICSE / ASE 2024 の 85 本のうち artifact があり OpenAI を使ったのが 18 本、実行できたのが 5 本、"For none of the five studies, we were able to fully reproduce the results."
  - Evertz ほかの調査データ（高。`analysis/llm-pitfalls-data.csv` を私が集計）: 72 本中、P9 Model Ambiguity が Present 53 本、Partly 9 本。
- **open-weight と open-source の違い**（高。ガイドラインの CHANGELOG 2026.09）
  - "open-source LLMs are preferable because their training data can be checked for benchmark contamination"

## 6. データ汚染

- **NDSS'26 P3 の推奨**（高）
  - "For proprietary models, identify the training cutoff date and determine whether evaluation data … was publicly accessible beforehand. When exclusion cannot be ensured, probe for memorization … and discuss potential effects."
  - 72 本中 47 本に何らかの形で該当（私の集計）。
- **ガイドライン**（高）
  - `08_…tex:42`: 汚染の議論は must。
  - `05_…tex:187`: 学習データを公開しないモデルでは "human validation, curating new data, or refactoring existing data" を考える。
- **あなたの研究での意味（推論）**
  - 対象は GitHub で公開されている MCP サーバなので、学習データに入りうる。
  - 判定者として使う場合の主な害は「記憶にある別の版のコードを根拠として示す」ことになる。対策は、pin した SHA のファイルだけを渡し、人が行を開いて確かめること。
  - 「人と LLM の一致」を報告するなら、汚染で一致が膨らむ可能性を限界に書く。

## 7. 測定研究で判定に LLM を使うとき、査読を通すための最低条件

1. **LLM のラベルを主指標にしない。** 主は人の判定。P2 の "full manual verification" と、ガイドライン 07:19 による。
2. **開示する。** 方法の節に、役・目的・どの段階で使ったかを書く（ACM 2026）。加えて投稿先の様式に従う（CCS 型の段落、ICSE / FSE の謝辞）。
3. **モデル id・設定のすべて・実行日・使える範囲で fingerprint を記録する**（02:23 の must）。廃止日も記録する。
4. **プロンプトの全文と、応答の全文を補足資料で公開する**（03:33-34）。agent を使ったなら、記録の形式と道具の版も（04:33）。
5. **人のラベルとの一致を報告する**（matrix:64）。ただし IRR とは呼ばず、妥当性の証拠にもしない（07:19、07:70）。
6. **繰り返しの方針を事前に決める**（05:54）。LLM の出力をラベルとして使うなら、項目ごとの分布か多数決。
7. **判定者の偏りを限界に書く**（matrix:94）。位置・冗長さ・迎合、汚染（08:42）、プロンプトへの敏感さ。
8. **可能なら open-weight モデルを併用するか、ローカルで実行する**（06:79）。
9. **費用（トークン数）を記録する**（08:93）。
10. **事前登録で、使うモデルとプロンプトを結果を見る前に固定する。** "LLM hacking"（低）の結論、つまりモデルとプロンプトを後から選べば結論を操作できることへの対策になる。

## 8. AuthGap への当てはめ（0-9 の決定に向けて）

**現状**
- `docs/final_evaluation_procedure.md:212-218`（0-9）と `:1266-1267`（§21 の 6）は、既に D の線で書かれている。
- v4 では原ソースの確認を木ごとに agent に分けた（`docs/population_v4.md:15-16`、`:68`）。
- **記録に AI のモデル名・版が無い。** `docs/population_v3.md`、`docs/population_v4.md`、`evidence/population_v4/v4_judgments.json` を grep したが、claude / opus / sonnet / gpt / "model" は 0 件。
- v4 を論文で引くなら、この欠落は後から埋められないので限界に書く。

**D を採る場合に足すとよい手順**（根拠は §1〜§6）
1. **順序**: 人が先に AI を見ずに判定して記録する。その後で AI に同じ組を渡す（人の判断が悪くなりうる、01-05:54）。
   - AI を見て変えた場合は、変える前と後の両方のラベルを残し、どちらを主にするかは事前登録で決める。
   - 変えた件数と向き（正 → 誤、誤 → 正 など）を報告する。
2. **AI に渡さないもの**: 宣言（hint の値）と解析器の答え（矛 / 不）。迎合と先入観を避けるため。
   - 問いは「このツール関数から届きうる書き込み・削除・起動・通信を file:line で列挙せよ」だけにする。
   - コードの中の description は消せないので、「AI が『読み取り専用』と言ったこと」は証拠に数えない。
3. **渡すのは pin した SHA の木のファイルだけ。** AI に repo を取りに行かせない（§6）。
4. **記録**: プロンプトと応答の全文、モデル id、日時、設定、トークン数を `evidence/` の下に置く。
5. **見直しの偏りに注意する**: AI が違うと言った件だけを見直すと、AI の偏った向きに直りやすい。§21 の 5 の、無作為 10% の再判定と組み合わせる。
6. **判定者 1 人の正当化**: 07:98 の「広く受け入れられた理論 + 価値の衝突が少ない」に当たると論じる（判定規則 D67 / D68 を文書化してある）。補うのは §21 の 5 の一致率で、LLM との一致では補えない。

**E（PPI）を使う場合**
- PPI は、少数の正解ラベル付きデータと多数のラベル無しデータから母数を推定し、"tighter confidence intervals" を出す枠組み（高。https://github.com/aangelopoulos/ppi_py の README、commit 3d1f0c6）。
- 条件は、人のラベルが同じ母集団からの無作為標本であること。seed で抜いているあなたの設計は満たせる。
- ただし手間と、査読者への説明の負担が増える。使うなら副次の結果としてだけ出し、モデルとプロンプトは事前に固定する。

## 確かめられなかったもの

- **Ahmed ほか MSR 2025** の本文と、課題ごとの κ / α の数値。software-lab.org、arxiv.org、research.ibm.com、2025.msrconf.org が遮断され、GitHub に複製も無かった。
- **Wang ほか ISSTA 2025** の本文の数値（arxiv が遮断。数値は検索の要約のみ）。
- 次の本文（いずれも遮断。内容は検索の要約か、ガイドラインの抜き書きのみ）:
  - Zheng ほか（MT-Bench）
  - SecLLMHolmes
  - Perry ほか
  - Baumann ほか
  - Camporese ほか
  - He ほか（TOSEM）
  - Chen・Zaharia・Zou
  - Yuan ほか
  - Atil ほか
  - Angermeir ほか
- **ACM Policy on Authorship の原文**（acm.org が遮断）。2026 年の文面（方法の節）と、2027 年の CFP が引く文面（謝辞の節）の食い違いは解消できていない。
- **ICSE / FSE の CFP 原文**（conf.researchr.org が遮断。第三者が集めた本文のみ）。
- **USENIX Security '27、NDSS 2027、IEEE S&P 2027 の原文**（usenix.org、ndss-symposium.org、ieee-security.org が遮断）。
- **OpenAI のモデル廃止ページと Anthropic の docs**（遮断。SDK のコードだけで確かめた）。Thinking Machines のブログ（遮断）。
- **ollama issue #5321**（この session の GitHub の許可の外）。
- **学生の所属大学の生成 AI 規程**（大学が分からない）。
- **v3 / v4 で使った AI のモデル名・版・日付**（repo の記録に無い）。

手元の clone は `/tmp/claude-0/-home-user-auth-gap/9d8a4d2c-1b03-53cb-ba04-44a67affb095/scratchpad/llmjudge/methodology/` にあります（`llm-guidelines-website/`、`llm-pitfalls/`、`ccs26cfp/`、`llm-judge-empirical/`、`sdk/`、`sigsoft_calls.csv`）。`/home/user/auth_gap` のファイルは変更していません。