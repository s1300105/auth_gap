# 判定の層に LLM を混ぜる研究（一般の SE・セキュリティ）の調査報告

## 結論

- **判定の層（矛／不／何も出さない を決める所）に LLM を混ぜるのは、AuthGap では使えません。** 理由は 5 つで、詳しくは §5-1 に書きます。
  1. 凍結の約束に反する（D66、analyzer-freeze-3）。
  2. 再現できなくなる。D71 の理由 3（標準ライブラリだけで再現できる）と `--determinism 3` の点検が成り立たなくなります。
  3. 調べた研究のコードは、LLM が答えられないときや迷ったときに、件を黙って消すか偽陽性に倒しています。原理 2-a（不明として数える）と逆向きです。
  4. LLM で誤検知を刈ると、本物の矛も一定の割合で消えます。
  5. 測る対象の宣言そのものが自然言語で、サーバの作者が書けます。LLM はそれに引きずられうるので、測定が循環します（この点の根拠は弱い）。
- **使える余地は判定の外側に限られます。**
  - (1) 最終評価で原ソースを読む補助。手順書 0-9 で決めた範囲のとおりです。
  - (2) 見落としを探すための候補出し。判定は本人が行い、事前登録してから使います。
  - (3) 比較の相手。本人の判定を固めた後に LLM の判定を採点します。
  - (4) 関連研究との違いを示す材料。「不明を数える 3 値の決定的な解析」と「不明を消す LLM 併用の解析」の対比です。

## 1. 調べ方と制約

- arxiv.org・export.arxiv.org・proceedings.iclr.cc・www.cs.ucr.edu・aclanthology.org・haonan.me・*.github.io・dl.acm.org・usenix.org は curl でも WebFetch でも 403 で遮断されました（`CONNECT tunnel failed, response 403` / `EGRESS_BLOCKED`）。**論文の本文は 1 本も読めていません。**
- そのため一次資料は GitHub の repo（コード、プロンプト、README、公開された結果ファイル）です。clone の置き場所は `S=/tmp/claude-0/-home-user-auth-gap/9d8a4d2c-1b03-53cb-ba04-44a67affb095/scratchpad/llmjudge/` で、各 repo の commit は §6 の後に書きます。
- 論文に出る数値は、検索要約にしかないものを「低」とします。repo の結果ファイルから自分で数え直したものは §3 に「高」として分けて出します。

## 2. 研究ごとの表

### 2-1 repo のコードで確かめたもの

| 研究 | 年・会議 | LLM が担う段 | モデルと設定 | LLM の判断の検証方法 | 弱点（報告されたもの／コードで見たもの） | 根拠 | 確かさ |
|---|---|---|---|---|---|---|---|
| **IRIS** | 2025 ICLR（repo の bibtex `booktitle={International Conference on Learning Representations}`）。arXiv 2405.17238（README） | **(a) 仕様の推論**: 外部 API を source / sink / propagator に分類し、内部関数の引数を source に分類する。**(b) 候補の真偽判定**: CodeQL の経路 1 本ずつを `is_vulnerable` で判定して刈る | `gpt-4`→`gpt-4-0125-preview`、`gpt-3.5`→`gpt-3.5-turbo-0125` ほか、OSS モデル計 8 系統。OpenAI は `temperature 0, n 1, seed 345`。繰り返しや多数決はコードに無い | 正解は CWE-Bench-Java の「修正された関数」。**経路が修正関数を通れば TP とする代理指標**（recall@method）。8 LLM と CodeQL 単体を並べる。v2 で 50 CVE の手作業の source/sink 注釈を追加 | ① 応答が JSON として読めないと `{}` になり、`num_failure` に数えるだけで**警告から消える**。② 一度 FP とされた source / sink を共有する後続の経路は、LLM に聞かずに「脆弱でない」になる。③ プロンプトに「Assume that the intermediate path has no sanitizer.」 | `README.md:23`、`src/prompts.py:69-86`（76 行）、`src/models/gpt.py:9-15`、`src/modules/contextual_analysis_pipeline.py:292-324, 436-437, 737-742, 779`、`src/modules/evaluation_pipeline.py:203-235` | 高（コード）。論文本文は未読 |
| **LLift** | 2024 OOPSLA（第三者の一覧 `awesome_vd/docs/papers_archive.md:43`、DOI 10.1145/3649828） | **(b) 経路の到達判定**: 静的解析 UBITect が出した「未初期化の使用」の警告ごとに、初期化する関数と使用前の検査（postcondition）を LLM が抜き出し、`must_init / may_init` を判定する | 既定 `gpt-4-0314`、実験スクリプトは `gpt-4-0613`。**temperature=1.0**。`--max_round` で同じ件を繰り返し、`must_init` が変わると `stable=False` を記録する | 人がラベルした群（Cmp-40 = UBITect の真の 13 件と偽陽性 27 件など）と照合 | README に「the result may be slightly different due to the randomness of GPT-4」。定義が見つからない関数については「try to analysis with your expertise in Linux kernel」「…you could assume this function must init when it return 0」と指示しており、**不明を推測で埋めさせる** | `README.md:43,55`、`app/run.py:122-127,162`、`app/prompts/call_api.py:214-215,350,412`、`app/prompts/prompts.py:145-147,159` | 高（コード）。会議名は中 |
| **BugLens** | 2025 ASE（README の bibtex）。arXiv 2504.11711（README） | **(b) 候補の真偽判定と sanitizer の妥当性判定**: SecIA が悪用できるかを判定し、ConA が呼び出し連鎖上の検査・sanitizer を集めて「bug が消えたか」を判定する。必要なコードは LLM が要求して取りに行く | 既定 `o3-mini`、temperature 1.0、`--max_iters` で多数決（既定 1）。"uncertain" が出ると 1 回だけ追加で回す | 人のラベル（`demo/ground_truth.csv` の 125 行。`Y?`・`N?`・`?`・`skip` を含む）。README は「improve the precision by 7x」 | 1 つのプロンプトに矛盾する指示が並ぶ。SecIA は「All existing checks can be bypassed」「Ignore any security checks in the code」。ConA は「Base your analysis only on the provided code, not prior knowledge」と「For kernel-controlled conditions, determine reachability based on your knowledge」。デモの採点は LLM の失敗（`None`）を not_a_bug、"uncertain" を still_a_bug に寄せる | `README.md:3,13`、`prompt.pdf`（抽出 `$S/buglens_prompt.txt:18-22,55,122,212-213`）、`BugLens-Code/prompts/llm_analysis.py:21-61`、`run.py:30-31`、`demo/logic.py:56-69,141-145` | 高（コード・プロンプト）。精度は README の自己申告 |
| **LLMDFA** | 2024 NeurIPS（repo の説明） | **(c) 解析の代替**: 関数内のデータフローの要約を LLM が出す。あわせて source/sink の抽出器（コード）と経路条件の Z3 スクリプトを LLM に合成させる（決定的に動く道具を作らせる） | `gpt-3.5-turbo` / `gpt-4-turbo` / `gpt-4o-mini`、**temperature 0** | Juliet（関数名の good / bad で TP / FP を自動で決める）。アブレーション 3 つ（NoSynExt / NoCoT / **NoSynVal = SMT の代わりに LLM で経路を判定**）。end-to-end プロンプトの比較相手 | README に「To avoid the leakage of ground truth to LLMs, we obfuscate the code in the Juliet Test Suite.」（データ汚染への対処） | `README.md:94,117`、`src/run_llmdfa.py:254-312,442,526`、`src/prompt/flow/dep_flow_validator.json` | 高 |
| **LLMSAN** | 2024 EMNLP Findings（repo の説明） | **(c) LLM が検出**し、報告に書かせたデータフロー経路を性質に分解して、構文解析ベースの解析と LLM で検査する（**静的解析が LLM の主張を検査する逆向き**） | temperature 既定 0.0。検出用と検査用のモデルを別に指定 | Juliet 5 種、難読化で汚染に対処 | 本文未読。数値（precision 91.03% など）は検索要約のみ | `README.md:184`、`src/batchrun.py:26-52,187` | 設計は高、数値は低 |
| **RepoAudit** | 2025 ICML（README）。arXiv 2501.18160（README） | **(c)** LLM エージェントがデータフロー解析を担う。**(b)** 別の LLM（path validator）が経路条件を満たせるかを判定する | 既定 `claude-3.7`、temperature 既定 0.5 | 実プロジェクトで報告し、開発者が確認する（README「hundred of confirmed and fixed bugs」） | validator の応答から `Answer:` が取れないと `None` になり、**その経路を黙って捨てる**（`continue`） | `README.md:3,24-26`、`src/repoaudit.py:212`、`src/run_repoaudit.sh:7`、`src/prompt/Java/dfbscan/path_validator.json`、`src/agent/dfbscan.py:504-505,678-679` | 高 |
| **KNighter** | 2025 SOSP（README の bibtex）。arXiv 2503.09002（README） | **(a)** 修正パッチから Clang Static Analyzer の checker を LLM が合成する。checker 自体は決定的に動く。**(b)** 走査結果を LLM が triage し、NotABug とされた報告を使って checker を絞り込む | 既定 `o3-mini`、temperature 既定 1.0 | checker を「修正前で検出し、修正後で検出しない」で検証する（`_validate_checker_linux` の TP/TN）。新しい bug を報告して確認を得る | triage のプロンプトが「**If there is any uncertainty in the classification, err on the side of caution and classify it as a false positive**」。不明を偽陽性に倒し、それで checker の改訂を動かす | `README.md:139`、`prompt_template/check_report.md:30`、`src/model.py:23`、`src/checker_refine.py:1229`、`src/backends/csa.py`（`_validate_checker_linux`） | 高 |
| **ZeroFalse** | 2025 arXiv preprint（repo の bibtex `booktitle={arXiv preprint}`） | **(b) 誤検知の刈り込み**: CodeQL の警告を、CWE ごとの採点基準つきのプロンプトで「False Positive: Yes/No」に判定する | README によると 10 の LLM（GPT-5、Gemini 2.5 Pro、DeepSeek R1 など）。`default_temperature 0.0` | OWASP Benchmark（正解つき）と OpenVuln の 7 CVE・58 警告（True 23 / False 35） | 下位の項目「Sanitization Found?」だけ "Unsure" を許し、最終判定は 2 値。プロンプトに「Do not assume behavior of code that is not shown」 | `README.md:241`、`OpenVuln/prompt_templates/optimized/CWE-022.txt:7,58`、`OpenVuln/ground_truth.csv`、`OWASP/llm_api_handler.py:249` | 高（コード）。OpenVuln のラベル付けの手順は未確認 |
| **Tencent の産業調査**（Reducing False Positives in Static Bug Detection with LLMs） | ICSE 2026 SEIP（検索） | **(b)** 社内の静的解析 BPcheck が出した 433 警告（FP 328 / TP 105）を、素の LLM・各種プロンプト・LLM4SA・LLM4PFA（LLM + 静的解析）で判定する | `gpt-4o-mini`（第三者の中継 `openkey.cloud` 経由）、`deepseek-reasoner`（R1-0528）、`qwen3-235b-a22b`、`claude-opus-4-20250514`。**temperature の指定は無い**。1 回だけ回す | 正解は開発者の手作業レビュー（README:14「all the reported bug alarms would be manually reviewed by developers, with false alarms proceeding to a second-round manual validation」）。データは非公開で、label と判定だけの JSON を公開 | README が挙げる限界: 長い文脈、連鎖した制約、意味の理解不足。**自分で数え直すと、FP を消す代わりに真の bug も 12〜25% 消える（§3）** | `README.md:8,14,18,22,26`、`result/*/*/result.json`、`baseline/LLM-based/4-few-shot-prompt/run-few-shot-prompt.py:31-43` | 高（README・結果ファイル）。会議名は低 |
| **Vulnhalla**（CyberArk の実務ツール） | 研究論文ではない。ブログは未読 | **(b)** CodeQL の結果を LLM が 1337（真）/ 1007（偽）/ 7331（情報が足りない）に分類する | litellm 経由。README の例は `gpt-4o`、`LLM_TEMPERATURE=0.2`（推奨） | 評価は確認できず | コードは「"1337" → true, "1007" → false, **else → more**」。読めない応答も「情報が足りない」に落とす 3 値で、**AuthGap の「不」に最も近い** | `README.md:67,383`、`src/vulnhalla.py:17`、`src/llm/llm_analyzer.py:222-226` | 高（コード）。評価なし |
| **SecLLMHolmes** | 2024 IEEE S&P（README）。arXiv 2312.12575（README） | **評価研究**: LLM 単体で脆弱性を同定し推論できるか（(c) の評価）。採点にも LLM（GPT-4、のち GPT-4o）を使い、LLM が LLM を採点する | 決定性の実験: 6 プロンプト × temperature {0.0, 0.2} × **k=10 回** | 手作りの例と実 CVE。正解つき | UPDATES に次の記録がある。評価スクリプトの bug で公開後に表が変わった。CWE-22 の「修正版」の例がまだ脆弱で正解を直した。OpenAI の埋め込みモデル廃止で差し替えた。採点の LLM を GPT-4o に差し替えた。結論の「non-deterministic responses」という文言は検索要約でしか見ていない | `src/experiments.py:881-906`、`src/helper_functions.py:76`、`UPDATES.md:7,9,18` | 高（コード・UPDATES・結果ファイル）。結論の文言は低 |

### 2-2 検索要約か第三者の一覧でしか確かめていないもの（repo が見つからないか、本文が読めない）

| 研究 | 年・会議 | LLM が担う段 | 内容（検索要約。逐語ではない） | 確かさ |
|---|---|---|---|---|
| LLM4SA（Wen ほか「Automatically Inspecting Thousands of Static Bug Warnings…」） | TOSEM 2024（検索） | (b) | 9,547 警告で precision 81.13%、recall 94.64%。Tencent の repo にプロンプトの再現がある（`baseline/LLM-based/5-llm4sa/run-llm4sa.py`、高） | 低 |
| LLM4PFA（arXiv 2506.10322、検索） | 不明 | (b) LLM エージェントが制約を推論し Z3 に渡す | 「filters out 72% to 96% of false positives … only missing 3 real bugs of 45」。Tencent の結果ファイルは高 | 低 |
| Sifting the Noise（arXiv 2601.22952） | ISSTA 2026（第三者の一覧 `awesome_vd/README.md:19`、中） | (b) エージェント | 「aggressive FP reduction can come at the cost of suppressing true vulnerabilities」。効き方は backbone と CWE に強く依存する | 低 |
| AdaTaint（arXiv 2511.04023） | 不明 | (a)+(b) | 「grounds model suggestions in program facts and constraint validation」 | 低 |
| MoCQ（arXiv 2504.16057） | 不明 | (a) 検出パターン（クエリ）を LLM が生成し、trace で検証する | 版によって題名が違う | 低 |
| Chapman・Rubio-González・Thakur「Interleaving Static Analysis and LLM Prompting」 | SOAP 2024（検索）。拡張版 STTT 2025 | (a) EESI と LLM を交互に呼んで、エラー仕様を推論する | — | 低 |
| ALIBI（arXiv 2607.24964。存在は `awesome_vd/arxiv.md:29` で中） | 不明 | LLM 検出器への**攻撃** | 「安全だ」と主張するコメントを足すだけで、4 系統の LLM 検出器で攻撃成功率が 90% を超える（comment trust prior） | 低 |
| Ahmed・Devanbu・Treude・Pradel「Can LLMs Replace Manual Annotation of SE Artifacts?」 | MSR 2025（検索） | 人の注釈を LLM で置き換える | 文脈の小さい演繹的な課題なら人 1 人を置き換えうる。**文脈の大きい課題では信頼できない**。モデル間の一致を、使ってよいかの予測に使う | 低 |

## 3. 公開された結果ファイルから自分で数え直した数字（確かさ 高）

1. **温度 0 でも答えは揺れる**（SecLLMHolmes `results/determinism/*.json`）
   - 分母は 6 プロンプト × 4 ファイル = 24 マスで、各マス 10 回。10 回の yes/no が一致しなかったマスを数えました。
   - temperature 0.0: `gpt-4` 6/24、`gpt-4o-2024-11-20` 6/24、chat-bison 1/24、codellama-7b 1/24、starchat 1/24、ほかは 0/24。
   - temperature 0.2: gpt-4o 10/24、gpt-4 5/24。
   - 注意: `pred` は別の LLM（GPT-4 系、temperature 0）が回答文から抜き出した値なので、揺れには抜き出し側の揺れも含まれます。
2. **誤検知を刈ると本物も消える**（Tencent `result/{GPT,claude,deepseek,qwen-v3}/*/result.json`。分母は FP 328、TP 105）
   - LLM4PFA の FP 除去率と TP 保持率: GPT 98.2% / 75.2%、Claude 94.2% / 87.6%、DeepSeek 94.8% / 85.7%、Qwen 98.2% / 79.0%。真の bug 105 件のうち **13〜26 件が消えています**。README:18 の「eliminates 94%–98% of false positives … while maintaining high recall」の後半は、数字では 75〜88% です。
   - 比較の手法（`baseline/LLM-based/*/*/`、項目は `detect_result`。解析できない応答は除去にも保持にも数えていない）では、**同じ素のプロンプトでも、FP 除去率はモデルによって 26.2%〜52.4% に割れます。** few-shot では解析できない応答が最大 15/433 ありました。
3. **検出数はモデルで動く**（IRIS `iclr-2025-results/*.csv`。121 行の中で Recall>0 の CVE 数）
   - CodeQL 27 に対して、IRIS は GPT-4 55、Llama3-70B 54、DeepSeekCoder-7B 52、GPT-3.5 47、Gemma2-27B 45（評価できた行は 98 のみ）、DeepSeekCoder-33B 42、Llama3-8B 41。
   - 検索要約にある「27 → 55」とは合います。分母（120 か 121 か）の食い違いは解消していません。

## 4. パターンの整理

### 4-1 LLM をどこに置くか

数え方は「1 つの研究が複数の段に置くときは重複して数える」です。抽出は体系的なものではなく、私が探した範囲です。

- **(b) 後段（候補を判定する・刈る）: 12 件。** IRIS、LLift、BugLens、RepoAudit の validator、KNighter の triage、ZeroFalse、Tencent、Vulnhalla、LLM4SA、LLM4PFA、Sifting、AdaTaint。**最も多い置き方です。**
- **(a) 前段（仕様・語彙・検出器を作る）: 6 件。** IRIS、LLMDFA の抽出器の合成、KNighter、AdaTaint、MoCQ、Chapman ほか。
  - LLM が作ったもの（仕様、checker、クエリ、抽出器）を**決定的な手段で検証してから固定し**、実行時の判定は決定的に保つ型です。
  - 検証の例: KNighter は修正前後のコードで、IRIS は CodeQL 自身の仕様との突き合わせ（`src/evaluate_spec_against_codeql.py`）で、LLMDFA は手書きの抽出器との比較で確かめています。
- **(c) 解析の代替: 3 件**（LLMDFA、LLMSAN、RepoAudit）と、その評価研究 1 件（SecLLMHolmes）。

### 4-2 後段に置いたとき、検出の主張（精度・再現率）が LLM の判断に依存することをどう扱っているか

- **正解を LLM の外に置く。** 種類は 4 つありました。
  - 合成ベンチマーク: Juliet（LLMDFA、LLMSAN）、OWASP（ZeroFalse）。
  - CVE の修正位置という代理指標: IRIS。
  - 開発者や研究者の手作業のラベル: Tencent、BugLens、LLift。
  - 新しい bug を保守者が確認したもの: KNighter、RepoAudit、LLift。この場合、精度は報告した分にしか言えず、再現率は分かりません。
- **LLM を変数として掃引する。** IRIS は 8 LLM、ZeroFalse は 10、Tencent は 4、LLMDFA は 3 でした。モデルへの依存を**示してはいるが、取り除いてはいない**ことになります。数字はモデルごとの値として報告されています。
- **LLM の段を LLM でない手段に置き換えるアブレーション。** LLMDFA の NoSynVal（SMT 対 LLM）、IRIS 対 CodeQL 単体。
- **データ汚染への対処。** LLMDFA と LLMSAN は難読化しています。
- **繰り返しはまれです。**
  - LLift は temperature 1.0 で繰り返し、`stable` に印を付けます。BugLens は多数決ができますが、既定は 1 回です。SecLLMHolmes は 10 回です。
  - ほかは temperature 0 で 1 回（IRIS、LLMDFA、ZeroFalse）か、temperature 1.0 で 1 回（KNighter、BugLens の既定）です。Tencent は temperature を指定していません。
  - §3-1 のとおり、temperature 0 でも答えは揺れます。

### 4-3 コードで見た範囲で、扱えていないこと

- **失敗が黙って「bug でない」になります。** IRIS（`{}` で消える）、RepoAudit（`None` で `continue`）、BugLens のデモの採点（`None` を not_a_bug）がそうでした。例外は Vulnhalla で、失敗を「情報が足りない」に落とします。
- **不明を 2 値に潰します。**
  - KNighter は不明を偽陽性に倒します。ZeroFalse の最終判定は 2 値です。IRIS には「不明」の欄がありません。
  - LLift は、分からない関数を規約で推測させます。BugLens には "uncertain" がありますが、採点では bug の側に寄せます。
- **偽陽性を減らす向きの最適化が、本物を消します**（§3-2）。
- 論文本文の指標の定義は読めていないので、「本文で不明の件数を別に報告しているか」は確認できていません。

## 5. AuthGap で使えるか

### 5-1 判定の層（矛／不／何も出さない）に混ぜる: 使えない

1. **凍結の約束。** D66「結果を見て解析器を変えない」（`docs/decisions.md:3743`）と analyzer-freeze-3 に反します。今から LLM の層を足すと、中間検証 v4 の結果を見た後に解析器を変えることになります。
2. **再現性。** D71 の理由 3「標準ライブラリだけで再現できる」（`docs/decisions.md:3850-3870`）と、`scan --determinism 3` の点検が成り立たなくなります。根拠は次の 3 つです。
   - temperature 0 でも 10 回の答えが揃わないマスが gpt-4 で 6/24 ありました（§3-1）。
   - モデルの廃止で手順を差し替えた実例があります（SecLLMHolmes `UPDATES.md:18`）。
   - 評価用の LLM を差し替えた実例もあります（`UPDATES.md:7`）。
3. **原理 2-a と逆向き。** AuthGap は「静的に決まらないものは不明として数え、件数を必ず併記する」（`docs/contradiction_principles.md:60-68,130-140`、CLAUDE.md の規則 4）と決めています。
   - 調べたコードは、不明を偽陽性に倒すか（KNighter）、失敗を黙って消しています（IRIS、RepoAudit）。
   - LLM に「不」を引き取らせると、事実上 2-b か 2-c に、**しかもモデルごとに違う向きで**倒すことになります。
4. **主指標がモデルの性質になる。**
   - AuthGap は「宣言がどれだけ当てにならないか」の率を測る研究です（D40）。
   - LLM を判定に入れると、率がモデル・プロンプト・温度で動きます。同じプロンプトでも FP 除去率は 26〜52% に割れ、検出数は 41〜55 に割れました（§3-2・§3-3）。
   - 刈れば本物の矛も 12〜25% 消えます（§3-2）。v4 の矛の精度 76.7%（1 木を除くと 36.4%）を LLM で上げようとすると、この取引に入ります。
5. **測る対象が自然言語で、作者が書ける。**
   - 宣言（ToolAnnotations）、説明文、docstring は MCP サーバの作者が書きます。安全だと主張するコメントで LLM 検出器が 90% 超の率で欺かれたという報告があります（ALIBI。検索要約で低）。
   - IRIS のプロンプトにも README の要約が入っています（`src/prompts.py:53-57`）。
   - 「宣言を信じてよいか」を、宣言を読んだ LLM に判定させると循環します。

### 5-2 使える余地（判定の外側）と条件

1. **最終評価で原ソースを読む補助（手順書 0-9）。** 既に決めた範囲のまま使えます（`docs/final_evaluation_procedure.md:212-217,1266-1267`）。
   - 追加の注意: Ahmed ほか（低）によると、文脈の大きい課題では LLM は信頼できません。AuthGap の判定は複数ファイルを読む文脈の大きい課題です。
   - したがって **AI を 2 人目の判定者の代わりにせず、AI との一致率を「判定者間一致」として報告しないこと**を、事前登録に書くとよいです。
2. **見落としを探す候補出し。** D71 の「CodeQL を見落とし探しの補助に」と同じ扱いにします。
   - LLM が影響するのは「人が見る候補の集合」だけで、ラベルは本人が付けます。
   - 条件: 事前登録、モデル名と版、プロンプト、回数を固定して書くこと。見落としの推定は「どの探索器の和集合に対してか」を明記すること。
3. **比較の相手（LLM 判定器の腕）。** LLMDFA の end-to-end の比較相手と同じ考え方です。
   - 本人の判定を**固めて記録した後に**、同じ件で LLM に「宣言に反するか」を答えさせ、本人の判定に対して採点します。先に見ると本人の判定が引きずられます。
   - 「LLM で判定すると不明が消え、本物も消える」ことを AuthGap のデータで示せる可能性があります。ただし費用、版の固定、繰り返し（最低でも数回と一致率）が要ります。主指標とは別の探索的な分析にします。
4. **関連研究の節。** 「(b) に LLM を置く研究は多いが、失敗や迷いを黙って消すか偽陽性に倒す。AuthGap は決定的な 3 値で、不明を理由つきで数える」という対比は、上の表のコードの行で根拠を示せます。
   - (a) の型（LLM で語彙の候補を出し、人が採否を決めて凍結する）は、AuthGap の手作りの語彙表と同じ位置にあたります。今回は凍結済みなので、**将来の作業**として書くのが妥当です。

## 6. 確かめられなかったもの

- **論文本文はすべて未確認**（遮断のため）。具体的には次のとおりです。
  - IRIS の FDR の定義と分母（120 か 121 か）。
  - LLift の precision 50% と新規 bug 13 件。
  - LLMDFA の 87.10% / 80.77%、LLMSAN の 91.03% / 74.00%。
  - BugLens の「7x」の算出方法。
  - ZeroFalse の OpenVuln のラベル付けの手順と、論文中の数値。
  - Tencent 論文の会議名と、本文の recall の定義。
- 論文で「不明」を別に報告しているか、繰り返しの回数を本文に書いているか（コードで見た範囲しか言えない）。
- LLM4SA、LLM4PFA、Sifting the Noise、AdaTaint、MoCQ、Chapman ほか、ALIBI、Ahmed ほか、CleanVul（データセットの脆弱性ラベルを LLM で付け直す研究。本文で扱わなかった）の内容。repo が見つからないか読めず、検索要約のみです（低）。
- LLM4SA の原典の repo（zenodo は遮断）。
- IRIS や LLift が固定したモデル版（`gpt-4-0125-preview`、`gpt-4-0314`、`gpt-4-0613` など）が今も使えるかどうか。
- BugLens のデモの `EXCLUDED_IDS` を FP 扱いにする理由（`demo/logic.py:36-39,136-137`）。
- Vulnhalla の評価とブログ（cyberark.com は遮断）。

repo の置き場所と commit（`$S` は §1 のパス）:
- `$S/iris-sast_iris`（3a12f45。v1 の枝も取得）
- `$S/seclab-ucr_LLift`（2e112e5）
- `$S/seclab-ucr_BugLens`（c9b1195）、`$S/seclab-ucr_BugLens-Code`（e95265e）、`$S/buglens_prompt.txt`
- `$S/chengpeng-wang_LLMDFA`（fca6387）、`$S/chengpeng-wang_LLMSAN`（54d2256）
- `$S/PurCL_RepoAudit`（160f5bc）
- `$S/ise-uiuc_KNighter`（f4e834b）
- `$S/mhsniranmanesh_ZeroFalse`（3ca00e4）
- `$S/LLM4SFPR_static-bug-false-positives-reduction-in-practice`（586e1ee）
- `$S/cyberark_Vulnhalla`（791ef8d）
- `$S/ai4cloudops_SecLLMHolmes`（9421928）
- `$S/awesome_vd`（4a8f36c）

`/home/user/auth_gap` のファイルは変更していません。