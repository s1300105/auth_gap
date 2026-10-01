# 判定の層に LLM を混ぜる研究：4 報告の統合と、AuthGap で使えるかの判断

**表記**
- 出典は、報告（R1〜R4）が挙げた URL・ファイル・行をそのまま書いています。
- 確かさの印も各報告のものを引き継ぎます。
  - 高: repo のコード、依存関係、論文本文を報告者が自分で読んだ。
  - 中: 第三者の逐語の抜き書き。
  - 低: 検索の要約だけ。
- R4 が repo の中で確かめた事実は、すべて高です。
- 【統合】と付けたものは、この統合で付けた分類や推論です。報告にある事実を組み合わせる以上のことは言っていません。
- `$S` は `/tmp/claude-0/-home-user-auth-gap/9d8a4d2c-1b03-53cb-ba04-44a67affb095/scratchpad/llmjudge` を指します。

## 0. 結論

**解析器の判定（矛 / 不 / 何も出さない）に LLM を混ぜるのは、使えません。** 4 報告とも同じ結論です（R1 §5-1、R2 §4(A)、R3 §0 の A、R4 §0 の (i)）。主な理由は 4 つです。
- 凍結 D66 に反します（`docs/decisions.md:3743` を R1 が、`:3749` を R4 が引いています）。
- 仕様書の「LLM を判定入力に使わず決定的に」（`AUTHGAP_BRIEF_v3.md:36`）に反します。
- D71 の理由 3「標準ライブラリだけで再現できる」（`docs/decisions.md:3850-3870`）が成り立たなくなります。
- 先行研究の LLM 判定は、不明を黙って消すか、どちらかに倒しています。これは原理 2 と規則 4 の逆です。

**使えるのは判定の外側だけです。**
- 判定者が原ソースを読むときの補助。0-9 にすでにある線で、4 報告とも「可」です。
- 「不」を後段で分ける別腕。事前登録したうえで別の列に出し、主指標は変えません。R1・R2・R4 が「条件つきで可」としています。
- 語彙の見落としの候補出しと、手引きの曖昧さの検出。どちらも条件つきで可です。手引きのほうは、データを見る前に限ります。
- 2 人目の判定者の代わりにはなりません（全報告）。
- LLM だけのベースラインと、記述・宣言・実装の三者照合は、今後の課題です。

**時期の制約（R4、高）。** 事前登録の最終評価の節（§2.12）はまだ書かれていません（`docs/final_evaluation_procedure.md:264`）。LLM をどこかで使うなら、最終評価のデータを見る前の今が、書き込める最後の機会です。

採るかどうかは学生が新しく決めることで、決めたら `decisions.md` に記録します（R2 §4(B)）。

---

## 1. 文献の要約

### 1-1 LLM をどこに置いているか

| 置き場所 | 一般の SE・セキュリティ（R1） | MCP・エージェント（R2） | 型の特徴 |
|---|---|---|---|
| **(a) 前段**：仕様・語彙・検出器を作る | IRIS：外部 API を source / sink / propagator に分類する（高）。KNighter：修正パッチから Clang Static Analyzer の checker を合成する（高）。LLMDFA：source/sink の抽出器と経路条件の Z3 スクリプトを合成する（高）。AdaTaint・MoCQ・Chapman ほか（低） | Semia：記述とコードから Datalog の事実を合成し、検出は決定的な規則で行う（高、`docs/architecture.md:52-69`）。MalSkills の抽出の段："You are extracting evidence facts, not verdicts."（高） | LLM が作ったものを**決定的な手段で検証してから固定し**、実行時の判定は決定的なまま保つ（R1 §4-1）。検証の例は下に書きます |
| **(b) 後段**：候補の真偽判定・刈り込み | R1 が数えた範囲で**最多の 12 件**。高：IRIS、LLift、BugLens、RepoAudit の validator、KNighter の triage、ZeroFalse、Tencent の産業調査、Vulnhalla。低：LLM4SA、LLM4PFA、Sifting the Noise、AdaTaint | R2 の P1。TaintP2X（sanitizer と taint の有効性）、MCPScan の段 2（HIGH / LOW / No Risk）、MCP-BiFlow の M3（曖昧なガード）、MalSkills の neuro reasoner、Cisco mcp-scanner。すべて高 | LLM の段を外すと、動くのは FP・棄却の件数です。確認済みの件数はあまり動きません（R2 P1）。例：MalSkills は FPR 0.05 → 0.49、MCP-BiFlow の M3 は確認済み 424 のまま |
| **(c) 解析の代替** | LLMDFA（関数内データフローの要約）。LLMSAN（LLM が検出し、静的解析がその主張を検査する逆向き）。RepoAudit（エージェントがデータフロー解析を担う）。いずれも高。評価研究として SecLLMHolmes（高） | — | — |
| (c') 静的に決まらない事実だけを埋める | — | R2 の P2。MCP-BiFlow の M2（source の確定）、MalSkills の operand 推論、SemTaint（"defers to an LLM to resolve call edges that cannot be resolved statically"、高・第三者の写し）、TaintP2X（LLM 呼び出しの特定） | 外すと被覆が落ちます（MCP-BiFlow の M2 で確認済み 424 → 324）。R2 は AuthGap の `opaque(unresolved)` に**最も近い使い方**としています |
| **(d) 意味の照合**（記述とコード） | — | R2 の P3。DCIChecker（記述 D と実装 C の一致。分類に Eff-SM＝状態の変更、Eff-DL＝外部送信を含む。中、数値は低）。Cisco behavioral（docstring と実際の動作、高）。TRUSTDESC（コードから記述を作り、実行ログで確かめる、高・写し）。MCPDiff（判定に LLM を使うか未確認、低）。記述だけで判定するもの：Parasites/MCP-SEC（高）、No-Box MCPSEC（中、LLM を使うかは推定） | — |
| （別の型）LLM は生成役で、真偽は実行の oracle が決める | — | R2 の P4。VIPER-MCP（中）、TRUSTDESC の DynVer（ただし最後は LLM の判定者） | — |

(a) の検証の例（R1 §4-1）：
- KNighter は、修正前で検出し、修正後で検出しないことで checker を確かめます。
- IRIS は CodeQL の仕様と突き合わせます（`src/evaluate_spec_against_codeql.py`）。
- LLMDFA は手書きの抽出器と比べます。
- Semia は根拠のテキストを原文の行に字句で照合し、grounding の閾値 0.2 で切ります（`semia_core/evidence.py:22`）。

**宣言と照合した研究は見つかっていません。** 「POST が相手の状態を変えるか」を LLM に決めさせ、宣言（readOnlyHint など）と照合する研究は、R2 の調査の範囲では見つかりませんでした（R2 §0-1）。最も近いのは DCIChecker の Eff-SM です（R2 §3）。

### 1-2 LLM の判断をどう検証しているか

**正解を LLM の外に置いています**（R1 §4-2、R2 §2）。
- **合成ベンチマーク**：LLMDFA と LLMSAN は Juliet、ZeroFalse は OWASP Benchmark を使います（高）。
- **CVE の修正位置という代理指標**：IRIS は、経路が修正された関数を通れば TP とします（高）。
- **人手のラベル**（高）：
  - Tencent：開発者の手作業レビューで、README:14 に "all the reported bug alarms would be manually reviewed by developers"。
  - BugLens：`demo/ground_truth.csv` の 125 行。`Y?`・`N?`・`?`・`skip` を含みます。
  - LLift：Cmp-40。
- **保守者の確認**：KNighter、RepoAudit、LLift。この形では精度は報告した分にしか言えず、再現率は分かりません（R1）。
- **MCP 側も最終確認は全員が人手です**（R2 §2）。
  - MalSkills：2 人が独立に判定し、3 人目が裁定（1062 行、高）。
  - DCIChecker：400 組を手で注釈（中）。
  - MCP-BiFlow：開示のための人手レビュー。
  - No-Box：人の評価者（中）。
  - SemTaint：2 人で確認（高・写し）。

**人手との一致**
- **MCP の範囲では、部品としての照合が無いか、確かめられていません**（R2 §0-2）。報告されているのは、全体（end-to-end）の精度・再現率と、アブレーションの 2 種類だけです。MCP-BiFlow は、LLM の裁定と人手の一致を測っていません。
- **DCIChecker の 400 組は層別の標本です。** ツール自身の予測で 200 組ずつに分けて取っています。全体の 19,200 組に重みを戻すと、母集団の再現率はおよそ 81% です（報告値は 97.46%）。これは R2 の計算で、元の数値は確かさ低です。注釈者の人数と κ は未確認です。
- **一般の注釈の研究**（R3 §2）：
  - Ahmed ほか（MSR 2025）："we propose model-model agreement as a predictor of whether a given task is suitable for LLMs at all"（中）。文脈の大きい課題では信頼できないという結論（低）。ガイドラインはその選別の閾値 α>0.5 を "well below the levels generally considered acceptable" と評しています（中、`07_…tex:57-61`）。
  - Wang ほか（ISSTA 2025）："ranging from near-human to unusable"（低）。
  - Lubos ほか（RE 2024）："moderate agreement for simple requirements and poor agreement for more complex requirements"（中）。
  - Camporese ほか（ICPC 2026）：セキュリティ固有のコードについて "not sufficient to reliably replace a human annotator"（低）。

**アブレーション**
- LLMDFA の NoSynVal は、SMT の代わりに LLM で経路を判定する設定です（高）。
- IRIS 対 CodeQL 単体（R1 が結果の CSV から数え直し、高）：Recall>0 の CVE 数は CodeQL 27 に対し、IRIS は GPT-4 で 55 です。分母が 120 か 121 かは解消していません。
- MalSkills（933–937 行、高）：neuro reasoner を外すと F1 0.93 → 0.71、FPR 0.05 → 0.49。neuro extractor を外してもほぼ変わりません。
- MCP-BiFlow（1094–1095 行、高・写し）：
  - M2 を外すと、確認済みが 424 → 324。
  - M3 を外すと、確認済みは 424 のまま、未解決 302 → 368、棄却 133 → 67。
- DCIChecker の DRA のアブレーションは、数値を入手できていません。

**モデルを変数として掃引しています。** IRIS は 8、ZeroFalse は 10、Tencent は 4、LLMDFA は 3 のモデルです。MalSkills は LLM を替えると F1 が 0.76–0.93、再現率が 0.70–0.95 の幅で動きます。R1 の評価は「モデルへの依存を**示してはいるが、取り除いてはいない**」です。

**繰り返しはまれです**（R1 §4-2、R2）。
- LLift：temperature 1.0 で繰り返し、答えが変わると `stable=False` を付けます。
- BugLens：多数決はできますが、既定は 1 回です。
- SecLLMHolmes：10 回。
- SemTaint：3 回の結果の和を取ります。
- Cisco：100 回実行するスクリプトはありますが、結果は公開されていません（高）。
- ほかは 1 回だけです。temperature 0 で 1 回（IRIS、LLMDFA、ZeroFalse）、1.0 で 1 回（KNighter、BugLens の既定）。Tencent は temperature を指定していません。

**データ汚染への対処**：LLMDFA の README に "To avoid the leakage of ground truth to LLMs, we obfuscate the code in the Juliet Test Suite." とあります（高）。LLMSAN も難読化しています。

### 1-3 報告された弱点と、コードで見つかった弱点

**1. 失敗や迷いを、黙って「問題なし」として扱う**（すべて高）
- IRIS：応答が JSON として読めないと `{}` になり、`num_failure` に数えるだけで警告から消えます（`src/modules/contextual_analysis_pipeline.py:292-324` ほか）。
- RepoAudit：`Answer:` が取れないと `None` になり、`continue` で捨てます（`src/agent/dfbscan.py:504-505,678-679`）。
- BugLens のデモの採点：`None` を not_a_bug にします（`demo/logic.py:56-69,141-145`）。
- TaintP2X：失敗や解析不能は `"is_vulnerability": False` にします。
- MCPScan：
  - JSON の解析に失敗した記述は評価されずに消えます。
  - 50 行を超える片は捨てます。
  - 最初の HIGH で残りの評価を打ち切ります。
- MCP-SEC：形の崩れた行を捨てます。
- TRUSTDESC：実行で確かめられない記述は "are discarded"（高・写し）。
- Cisco："When in doubt, don't flag"。

**2. 不明を 2 値に潰すか、どちらかに倒す**（高）
- KNighter：「If there is any uncertainty in the classification, err on the side of caution and classify it as a false positive」（`prompt_template/check_report.md:30`）。その判定で checker の改訂を動かしています。
- ZeroFalse：最終判定は 2 値です。
- IRIS：「不明」の欄がありません。
- LLift：定義が見つからない関数について "try to analysis with your expertise in Linux kernel" と指示し、推測で埋めさせます。
- BugLens："uncertain" が出ても、採点では bug の側に寄せます。

**3. 例外：不明を保つ設計**（高）
- Vulnhalla：`"1337"` を真、`"1007"` を偽、それ以外を「情報が足りない」にする 3 値です（`src/llm/llm_analyzer.py:222-226`）。R1 は、AuthGap の「不」に最も近いとしています。ただし評価はありません。
- MalSkills：プロンプトに "If a symbolic operand cannot be resolved, preserve it explicitly as unknown"。
- Cisco："an errored function is not 'safe', just unknown"。
- MCP-BiFlow："uncertain" を出力に持っています。ただし集計でどう数えたかは本文に書かれていません。

**4. 決められなかった率を報告した研究はありません**（R2）。一方で、人の判定でも決まらないものは多く、MCP-BiFlow の人手レビューでは 859 件中 302 件（35%）が未解決でした。AuthGap が不明を数える設計の傍証になります。

**5. 方針がプロンプトの文に埋まっていて、感度分析がありません**（R2、高）
- MCPScan："如果...通过POST请求处理后直接返回给LLM的逻辑，则 = LOW"（`prompts/stage2_py.md:11,16,18`）。
- TaintP2X：「パスと内容の両方を制御できなければ無効と判定せよ」。
- IRIS："Assume that the intermediate path has no sanitizer."（`src/prompts.py:76`）。
- BugLens：同じプロンプトの中に食い違う指示があります。"Ignore any security checks in the code"、"Base your analysis only on the provided code, not prior knowledge"、そして "determine reachability based on your knowledge" です。

**6. 誤検知を刈ると、本物も消えます**
- Tencent の結果ファイルを R1 が数え直しました（高）。LLM4PFA は FP を 94.2〜98.2% 除去しますが、TP の保持は 75.2〜87.6% です。真の bug 105 件のうち 13〜26 件が消えています。README:18 は "while maintaining high recall" と書いています。
- Sifting the Noise："aggressive FP reduction can come at the cost of suppressing true vulnerabilities"（低）。

**7. 答えが揺れます（非決定性）**
- SecLLMHolmes の `results/determinism/*.json`（高）：
  - temperature 0 でも、10 回の答えが揃わないマスが gpt-4 で 6/24、gpt-4o-2024-11-20 で 6/24 ありました。
  - temperature 0.2 では gpt-4o が 10/24 です。
  - この揺れには、回答文から答えを抜き出す LLM 側の揺れも含まれます。
- LLift の README："the result may be slightly different due to the randomness of GPT-4"。
- MalSkills の本文："inherently less stable than symbolic matching"。

**8. 結果がモデルで大きく動きます**（高）
- Tencent：同じ素のプロンプトでも、FP 除去率は 26.2〜52.4% に割れます。
- IRIS：検出数は 41〜55 に割れます。
- MalSkills：F1 は 0.76〜0.93 です。

**9. 保守と再現性**（高）
- SecLLMHolmes の `UPDATES.md:7,9,18` に、次の記録があります。
  - 評価スクリプトの bug で、公開後に表が変わった。
  - CWE-22 の「修正版」の例がまだ脆弱で、正解を直した。
  - 埋め込みモデルの廃止で差し替えた。
  - 採点の LLM を GPT-4o に差し替えた。
- TaintP2X の公開コードは、import の時点で `NameError: Dict` になります（R2 が実行して確認）。

**10. 欺かれやすい**
- ALIBI：「安全だ」と主張するコメントを足すだけで、攻撃成功率が 90% を超えます（低）。
- He ほか（TOSEM）："These attacks subtly alter software artifacts to deceive the judge…"（中）。
- DCIChecker 自身が "…to mitigate LLM sycophancy and hallucinations" と書いています（中）。

**11. LLM の要約そのものが誤ります。** VIPER-MCP の FPR は、本文の逐語では "0% (vs." ですが、LLM が作った要約では 4.6% です（R2 §5）。

### 1-4 方法論の文献が求めること（R3）

**Baltes ほかのガイドライン**（EMSE 2026、高。原稿の repo を読んでいます）
- must（必須）：
  - LLM の役を宣言する（`matrix.tex:23-24`）。
  - モデル名と版、出力に効くパラメタのすべて、実行日を書く（`02_…tex:23`）。
  - プロンプトの全文を公開する（`03_…tex:33-34`）。
  - 判定者として使うなら、プロンプトに入れた評価基準・尺度・例を書く（`matrix.tex:44`）。
  - 人の判断を置き換えるなら、なぜ正当かを説明し、標本を人の専門家で検証する（`07_…tex:19`。"High inter-model agreement can reflect shared model biases"）。
  - 限界の節で偏り（`matrix.tex:94`）と汚染（`08_…tex:42`）を論じる。
- should（推奨）：繰り返す（`05_…tex:54`）、open なモデルと比べる（`06_…tex:79`）、費用を書く（`08_…tex:93`）。
- 温度 0 について："should not treat a temperature of 0 as a guarantee of reproducibility"（`02_…tex:79`）。
- 判定者が 1 人のとき："A single human judge is appropriate only when judgments depend on widely accepted theories and involve limited value conflict"（`07_…tex:98`）。
- 人の判断も悪くなります："When LLM outputs are incorrect, they can negatively affect human judgment"（`_studytypes/01-05…tex:54`）。

**NDSS'26 "Chasing Shadows"**（Evertz ほか、高）
- P2 の推奨："Disclose when labels or judgments come from LLMs. The ideal mitigation is full manual verification."
- 調べた 72 本の全部に、少なくとも 1 つの落とし穴があります。
- R3 の集計では、P9 Model Ambiguity が 53 本で「該当」、9 本で「一部該当」でした。

**学会の方針**
- ACM の 2026 年の文面は「方法の節に書く」です（中）。一方、ICSE 2027 の CFP は「謝辞の節」です（中）。この食い違いは解消していません。
- CCS 2026 は 'Generative AI Usage' の段落を求めています（高）。

**再現性**
- anthropic SDK の `DEPRECATED_MODELS` に `"claude-sonnet-4-5": "November 30th, 2026"` があります（高）。
- openai の seed："Determinism is not guaranteed"（高）。
- vLLM："only provides reproducibility when it runs on the same hardware and the same vLLM version"（高）。
- Angermeir ほか：OpenAI を使い artifact がある 18 本のうち、実行できたのは 5 本で、"For none of the five studies, we were able to fully reproduce the results."（中）。

---

## 2. AuthGap での使い道の候補

### 一覧

| # | 候補 | 差し込む箇所 | 今回の論文に |
|---|---|---|---|
| 1 | 解析器の判定層に入れる（不を解かせる・矛を刈る） | 解析器の中 | **使えない** |
| 2 | 「不」を後段で分類する（とくに net_post などの意味の判断） | 解析器の外の後段（別腕） | **今回**。副次の探索的分析として、§2.12 に先に書けた場合だけ |
| 3 | 判定者が原ソースを読む補助（0-9） | 判定の補助 | **今回は補助のみ** |
| 4 | 2 人目の判定者の代わり | 評価 | **使えない**。参考の一致率なら補助のみ |
| 5 | 語彙の見落とし候補の発見 | 外の後段（見落とし探し） | **今回は補助のみ**。解析器に足すのは今後の課題 |
| 6 | LLM だけで矛を判定するベースライン | 評価の比較腕 | **今後の課題** |
| 7 | 記述（description）・宣言（annotation）・実装の三者照合 | 解析器の外の新しい測定 | **今後の課題** |
| 8 | 判定の手引きの曖昧さの検出 | 判定の補助（段階 1〜2） | **今回は補助のみ**（データを見る前に限る） |
| 9 | PPI で区間を狭める | 評価の統計 | **今後の課題**。今回入れるなら副次として |

---

### 候補 1. 解析器の判定層に LLM を入れる

- **何をするか**：解析器が出した「不」を LLM に解かせて、矛か「何も出さない」に変えます。または、矛を LLM で刈って精度を上げます。
- **差し込む箇所**：解析器の中（`authgap/`、段階 5）。
- **期待できる研究価値**：
  - 小さいです。LLM で不を解いた結果は、既に出している感度分析の上限と下限の間にある 3 つ目の点にすぎず、その点の正しさを測った先行研究はありません（R2 §4(A)）。上限は「不を矛に倒す」で D1 494・D2 412、下限は D1 323・D2 155 です（`evidence/population_v4/contradiction_by_decl_v4_run1.md:60,63`）。
  - 矛を刈ると本物の矛も消えます。Tencent の数字では 12〜25% です（R1 §3-2、高）。v4 の矛の精度 76.7%（1 木を除くと 36.4%）を LLM で上げようとすると、この取引に入ります（R1 §5-1-4）。
- **文献上の先例**：(b) の型の大多数（§1-1）。
- **repo の約束とのぶつかり**：
  - **凍結 D66**：ぶつかります（`docs/decisions.md:3743` / `:3749`、`docs/final_evaluation_procedure.md:13`「最終評価のどの段階でも `authgap/` を変えない」、`CLAUDE.md:82-83`）。仕様書も「LLM を判定入力に使わず決定的に」（`AUTHGAP_BRIEF_v3.md:36`）、「本研究は「LLM を verdict 入力に使わない」ことを主張の一部にしている」（`:82`）と書いています。ここで LLM を混ぜると、自分で立てた比較の軸を失います（R4）。
  - **規則 4**：ぶつかります。先行研究の LLM 判定は、不明を消すか倒します（§1-3 の 1・2）。解決率を上げる向きの変更は誤 clear を作りやすいとも書かれています（`CLAUDE.md:76-77`）。
  - **規則 5・事前登録**：走査の後に解析器を変えることは禁止です（`final_evaluation_procedure.md:327`）。
  - **再現性**：`scan --determinism 3` と D71 の理由 3 が成り立たなくなります（R1、R3）。
- **今回の論文に**：**使えない。**

### 候補 2. 「不」を後段で分類する（別腕）

- **何をするか**：解析器が出した不の組について、LLM に `{反する / 反しない / 不明}` を根拠の行つきで答えさせ、主の不とは別の列に記録します（R2 §4(B)）。
  - 【統合】迎合を減らす形もあります。宣言の値を渡さずに効果の事実だけを問い（例：「この POST は相手の状態を変えるか」）、宣言との照合は決定的な規則で行います。R2 の P5（LLM が事実を出し、決定的な規則が判定する。Semia、MalSkills）と、R3 §8-2（AI に宣言の値と解析器の答えを渡さない）を組み合わせたものです。
- **差し込む箇所**：解析器の外の後段（段階 7〜8）。
  - 正解には 0-14 で人が判定する 100 組を使えます（`final_evaluation_procedure.md:250-255`）。これは D69 の不の抜き取り（D1・D2 で各 50 組）に当たります（R2）。
- **期待できる研究価値**：
  - 査読で「なぜ不を LLM で解かないのか」と聞かれたとき、データで答えられます（R2）。
  - 「LLM で判定すると不明が消え、本物も消える」ことを AuthGap のデータで示せる可能性があります（R1 §5-2-3）。
  - 宣言との照合で POST の意味を LLM に決めさせた研究は、R2 の範囲では見つかっていません。
  - 対象は「意」の類に絞るべきです（R4 の分類、判断）。
    - 意が主の理由：`net_post`（D1 78・D2 93）、`net_nonidempotent_method`（D4 67）、D3 の `spawn_command`（42）。
    - 実か定が主の理由：`fs_writeout`（D2 121）、`net_host_unknown`（22）、`db_persistent`（2）。実の類は LLM でも決まらず、定の類は LLM に決めさせてはいけません。
    - `_opaque` の理由は意味の問題ではなく、値の追跡の限界です（`authgap/ir.py:126-137`）。
  - v4 の事例のうち、R01（`v4_judgments.json:1166`）、R08（`:1264`）、R29（`:1558`）の POST の意味は「LLM に向く」とされています。一方 M00（`:74`）は「意味の読みが表から外れる」危険な例です（R4、判断）。
- **文献上の先例**：
  - R2 の P2：MCP-BiFlow の M2、MalSkills の operand 推論、SemTaint、TaintP2X。
  - 不明を保つ 3 値：Vulnhalla（R1）、MalSkills。
  - **部品の判断を人手と照らした先例はありません**（R2）。
- **repo の約束とのぶつかり**：
  - **凍結**：ぶつかりません。manifest と原ソースを読むだけです（R4）。
  - **規則 4**：**主の「不」を置き換えるとぶつかります**（`CLAUDE.md:13`、`docs/contradiction_principles.md:139`「b / c は測定を既知の向きに偏らせる。不明の件数は必ず併記」、`docs/decisions.md:3861`）。別の列にすればぶつかりません。LLM が「不明」と答えたもの、3 回の答えが食い違ったものは不として数えます（R2）。
  - **規則 5・事前登録**：**§2.12 に先に書くことが必須です**（R4）。
    - 登録する項目：モデル ID（日付つき）、temperature、プロンプトの全文（コミットのハッシュ）、入力、出力の形式、3 回実行で食い違えば不明とする規則（R2）。
    - 先行研究に課した「3 回一致」の決定性の測り方を、自分の腕にも課すのが筋です（R4。`AUTHGAP_BRIEF_v3.md:93,140`）。
    - 後から足すなら事後の分析として明記します（`final_evaluation_procedure.md:1346`）。
    - 可能なら open-weight のモデルかローカル実行を併用し、ollama なら tag と checksum を書きます（R3。ガイドライン `06_…tex:79`、`02_…tex:54`）。
    - 生の応答は全部保存します（R2。MalSkills のキャッシュ方式が参考になります）。
  - **判定者 1 人**：学生は LLM の出力を見ずにラベルを付けます。0-9 の読み補助を、この腕と同じ項目には使いません（R2）。κ は「学生と LLM の一致」と書き、評定者間一致とは書きません（R2）。
  - **0-9**：範囲外です。0-9 は判定の補助の話です（R4）。所属先の規程は確かめる必要があります（R2）。
  - **D60**：「評価データを本記録者が一度も見ない」（`docs/decisions.md:3400`）に、別腕の LLM が当たるかは定義されていません。学生の解釈が要ります（R4）。
- **費用**：100 組 × 3 回で小さいです（R2）。
- **今回の論文に**：**今回**。ただし副次の探索的分析として出し、主指標（矛・不の件数、精度）は変えません。§2.12 に先に書けた場合に限ります。

### 候補 3. 判定者が原ソースを読む補助（0-9）

- **何をするか**：LLM に根拠の行、呼び出し元、起動の順序（lifespan か `main()` か）を探させ、学生がその行を開いて確かめてから判定・記録します。書き込み先の種類・誤の原因・条件の種類のラベル案（16・17・14.3 節）もここに入ります（R4。迷えば「その他・不明」、`:1051`）。
- **差し込む箇所**：判定の補助（段階 7）。
- **期待できる研究価値**：
  - 判定の手間を減らすことです。ただし、どれだけ減るかは測っていません（R4）。
  - v4 の誤の大半は起動時の初期化（M01〜M03、M07、M06、R15）で、「読」の類です。読む補助に向いていて、規則は 14.4 で決まっています（R4、判断）。
  - R3 によると、これは P2 の理想の対策 "full manual verification" に当たります。
- **文献上の先例**：MCP 側の研究でも、最終判定はすべて人手です（R2 §2）。NDSS'26 の P2（R3、高）。
- **repo の約束とのぶつかり**：
  - **凍結・規則 4**：ぶつかりません。
  - **事前登録**：使う範囲を事前登録し、論文で開示します（`final_evaluation_procedure.md:216,1354,1378`）。
  - **判定者 1 人**：判定は本人が行います（`:214`）。「AI の結論をそのまま記録しない」（`:1266-1267`）。
  - **0-9**：この項目そのものです。大学の規程を確かめる必要があります（`:216`）。
  - **R3 §8 が足すとよいとする手順**：
    1. 学生が先に、AI を見ずに判定して記録します。AI を見て変えた場合は、変える前と後の両方と、変えた向きを残します。
    2. AI には宣言の値と解析器の答えを渡しません。問いは「届きうる書き込み・削除・起動・通信を file:line で列挙せよ」だけにします。コードの中の description が「読み取り専用」と言うことは、証拠に数えません。
    3. pin した SHA のファイルだけを渡します。
    4. プロンプトと応答の全文、モデル id、日時、設定、トークン数を `evidence/` の下に置きます。
    5. AI が違うと言った件だけを見直すと、AI の偏りの向きに直りやすくなります。§21 の 5 の無作為 10% の再判定と組み合わせます。
  - **見落としの判定**は、解析器の出力を見る前に行います（`:167,1093`）。LLM の要約も同じように判定を引っぱるので、最初の読みは自分で行います（R4、判断）。
  - **候補 2 と同じ項目には使いません**（R2）。
  - **D60 の「本記録者」に読む補助の LLM が含まれるか**は未定義で、学生の解釈が要ります（R4）。
  - **v3・v4 の記録には AI のモデル名・版がありません**（R3 が grep して 0 件）。v4 を論文で引くなら、限界に書きます。
- **今回の論文に**：**今回は補助のみ。**

### 候補 4. 2 人目の判定者の代わり

- **何をするか**：LLM の判定と学生の判定の一致（κ）を「判定者間一致」として出します。
- **差し込む箇所**：評価。
- **期待できる研究価値**：見かけの上では D67 の 4（判定者が 1 人）の弱点を補えます。しかし妥当性の証拠にはなりません（R3 §0 の C）。
- **文献上の先例**：
  - Ahmed ほか："replacing more than one human can inflate inter-rater agreement because model-model agreements are much higher"（中）。文脈の大きい課題では信頼できません（低）。
  - ガイドラインの `07_…tex:19`「High inter-model agreement can reflect shared model biases」（高）。
  - Lubos ほか：複雑になるほど一致が下がります（中）。
- **repo の約束とのぶつかり**：
  - **判定者 1 人**：ぶつかります。`docs/decisions.md:3784` に「判定者間の一致（κ）に依存する主張はしない」、`:3786` に「将来 2 人目を用意できたら追加の検証として足す」とあります。
  - 判定者が 1 人であることの正当化は、ガイドライン 07:98（広く受け入れられた理論があり、価値の衝突が少ない）で論じます。補うのは §21 の 5 の一致率で、LLM との一致では補えません（R3 §8-6）。
  - 候補 3 と同じ LLM を使うと、人と独立になりません（R4、判断）。
  - **0-9** はこの使い方を想定していません（R4）。
  - 「AI を 2 人目の代わりにせず、AI との一致率を判定者間一致として報告しない」ことを事前登録に書くとよいです（R1 §5-2-1）。
- **今回の論文に**：代わりとしては**使えない。**「学生と LLM の一致」を参考の値として出すなら、事前登録して**補助のみ**です（R3、R4）。

### 候補 5. 語彙の見落とし候補の発見

- **何をするか**：v4 の見落とし（loguru の `logger.add`、`wave.open`、ORM の `add/commit` など）のような、語彙表に無い効果を持つ API の候補を LLM に挙げさせます。採るかどうかと、見落としかどうかの判定は学生が行います。
- **差し込む箇所**：解析器の外の見落とし探しです。解析器には足しません。
- **期待できる研究価値**：見落としを探す網を広げます。ただし見落としの推定は「どの探索器の和集合に対してか」を明記する必要があります（R1 §5-2-2）。
- **文献上の先例**：(a) の型です。IRIS の仕様推論、KNighter、MoCQ（低）、Chapman ほか（低）。LLM が作ったものを決定的な手段で検証してから固定します（R1 §4-1）。
- **repo の約束とのぶつかり**：
  - **凍結**：解析器に足すとぶつかります（`CLAUDE.md:46`、`docs/open_questions.md:1041` の O39、`:1193`・`:1197` の O43）。
  - **規則 4**：見落としを数える側なので、向きは安全です（R4）。
  - **事前登録**：見落とし判定の補助にするなら事前登録が要ります。扱いは `docs/decisions.md:3870` の CodeQL 案と同じです（R4、R1）。モデル名と版、プロンプト、回数を固定して書きます（R1）。
  - **判定者 1 人**：判定は本人が行います。
- **今回の論文に**：候補出しとしては**今回は補助のみ**。語彙として解析器に入れるのは**今後の課題**です（R1 §5-2-4）。

### 候補 6. LLM だけで矛を判定するベースライン（比較実験）

- **何をするか**：同じユニットについて、LLM に「宣言に反するか」を答えさせ、学生の判定で採点します。LLMDFA の end-to-end の比較相手と同じ考え方です（R1 §5-2-3）。
- **差し込む箇所**：評価の比較腕。
- **期待できる研究価値**：決定的な 3 値の解析と、不明を消す LLM の判定を、同じデータで対比できます。
- **文献上の先例**：
  - LLMDFA の end-to-end のプロンプトとの比較（高）。
  - SecLLMHolmes（LLM 単体の評価、高）。
  - IRIS 対 CodeQL 単体（高）。
  - No-Box の LLM ベースライン 84.2%（中）。
- **repo の約束とのぶつかり**：
  - **凍結**：ぶつかりません。
  - **仕様書が一度削ったもの**です（`AUTHGAP_BRIEF_v3.md:678`「LLM baseline は削除した」、`:951`、`:814`、`:1060`）。仕様書は、審査での答えを「精度ではなく出力形式（決定性・witness・宣言照合）の違い」と決めています（`:678`）。復活させるなら仕様書は書き換えず、`decisions.md` に書いて事前登録します（R4）。
  - **判定者 1 人**：正解づくりの判定が増えます。R4 は見込み 170〜380 時間として `final_evaluation_procedure.md:1419` を引いています。ただしこれが上乗せ分か最終評価全体の時間かは、R4 の書き方からは読み取れません。
  - **検証の偏り**：正解の標本は AuthGap の出力から抜きます（矛の抜き取りと、矛の無いユニット）。LLM だけが出した矛は標本に入らないので、LLM の精度を測るには別の判定が要ります（R4、判断）。
  - **順序**：学生の判定を固めて記録した後に LLM の判定を出します。先に見ると引きずられます（R1）。
- **今回の論文に**：**今後の課題。**今回入れるなら、主指標とは別の探索的分析で、事前登録が前提です（R1）。

### 候補 7. 記述・宣言・実装の三者照合

- **何をするか**：description（自然言語の主張）を LLM に読ませ、annotation（D1〜D4）と、静的に推論した効果の三者を突き合わせます。
- **差し込む箇所**：解析器の外の、新しい測定です。
- **期待できる研究価値**：
  - 先行研究の (d) は、記述と実装の 2 者の照合です（DCIChecker、Cisco、TRUSTDESC）。AuthGap は機械可読な宣言を使います（R2 §3）。
  - 4 つの報告のどれも、三者を照合した研究を挙げていません。ただし、無いことを確かめたわけではありません。
- **文献上の先例**：
  - DCIChecker：Eff-SM・Eff-DL（中、数値は低）。
  - Cisco："Legitimate operations that match the documented purpose (API calls, file I/O, network requests)" は対象外にしています（高）。
  - TRUSTDESC：到達しない分岐が残っていると、Claude でも機能を過大に書きます（高・写し）。
  - Parasites、No-Box：記述だけで判定します。
- **repo の約束とのぶつかり**：
  - **循環**：測る対象の宣言と説明文は、サーバの作者が書けます。それを読んだ LLM に「宣言を信じてよいか」を判定させると循環します（R1 §5-1-5。根拠は弱いと R1 自身が書いています。ALIBI は低）。読み取り専用を名乗る文を LLM が信じれば、迎合と同じ仕組みで「違反なし」に傾きえます（R3 §3、推論）。
  - **凍結と事前登録**：今回の事前登録と凍結の範囲の外にある、新しい主張です。
- **今回の論文に**：**今後の課題。**

### 候補 8. 判定の手引きの曖昧さの検出

- **何をするか**：判定の手引きを LLM に読ませ、規則が当てはまらない箇所や、二通りに読める箇所を挙げさせます。手引きを直すかどうかは学生が決めます。
- **差し込む箇所**：判定の補助（段階 1〜2）。
- **期待できる研究価値**：
  - 判定がぶれる元を、データを見る前に減らせます。
  - v4 では、定の類が後から手引きで決着した例があります。R19 のログの書き込みは、`final_evaluation_procedure.md:966,700-702` で決着しました。M58 の一時ファイルのように、記録者が確認を求めた例もあります（R4）。
- **文献上の先例**：4 報告に直接の先例はありません。
- **repo の約束とのぶつかり**：
  - **凍結・規則 4**：ぶつかりません。
  - **事前登録**：**データを見る前に限ります**（`final_evaluation_procedure.md:508`「段階 1 に戻って手引きを直す」、途中で変えないこと `:1275`）。
  - **判定者 1 人**：規則を決めるのは学生です。定の類（何を「環境」に含めるか）を LLM に決めさせてはいけません。実世界でも割れています（`docs/open_questions.md:1232-1233`）。
  - 練習（6.8）で AI の v4 の判定を使って答え合わせをするときは、食い違いを手引きの穴として扱い、AI 側を正しいとみなしません（R4、判断。`:501-508`）。
- **今回の論文に**：**今回は補助のみ**（データを見る前だけ）。

### 候補 9. PPI で区間を狭める

- **何をするか**：人が付けた無作為標本のラベルと、LLM が全件に付けたラベルを PPI で合わせ、母数の区間を狭めます（R3 §0 の E、§8）。PPI は "tighter confidence intervals" を出す枠組みです（ppi_py の README、高）。
- **差し込む箇所**：評価の統計（副次）。
- **期待できる研究価値**：区間を狭められます。条件は、人のラベルが同じ母集団からの無作為標本であることで、seed で抜く今の設計は満たせます（R3）。
- **repo の約束とのぶつかり**：
  - モデルとプロンプトを事前に固定する必要があります。
  - 手間と、査読者への説明の負担が増えます。
  - 主の結果にはしません（R3）。
- **今回の論文に**：**今後の課題**。今回入れるなら、副次として事前登録したうえでです。

### 付記：関連研究の節（LLM を使うことではなく、文献の使い方）

- 不明の扱いの対比表は、確かさ高の材料だけで書けます（R2 §4(D)、R1 §5-2-4）。
  - Cisco "When in doubt, don't flag"
  - TaintP2X：失敗すると False
  - MCPScan：解析に失敗したものが黙って脱落する
  - TRUSTDESC：検証できない記述を破棄する
  - KNighter：迷ったら偽陽性に倒す
  - IRIS・RepoAudit：失敗した件が消える
  - MalSkills・Vulnhalla：unknown を保つ
- **仕様書との食い違い**（R2 §5-1）：
  - `AUTHGAP_BRIEF_v3.md:140` は「MCP-BiFlow を除く 3 件は LLM を判定経路に置く」と書いています。しかし MCP-BiFlow の本文では、M2 と M3 で LLM が候補の採否を決めています（766–769 行 "deferred to LLM-based adjudication"）。
  - 規則 6 に従い、仕様書は書き換えず、`decisions.md` か `open_questions.md` に記録する候補です。
  - 仕様書はこの点を先行研究との差としているので（`:82`）、関連研究の節の書き方に影響します。
- **LLM で関連研究を要約するとき**は、「LLM 要約に依拠したまま提出しない」（`AUTHGAP_BRIEF_v3.md:82`、R4）を守ります。VIPER-MCP の FPR の食い違い（0% と 4.6%）が実例です（R2 §5-5）。

---

## 3. 使えなさそうな理由と、どの候補に効くか

| 理由 | 中身と根拠 | 強く効く候補 | 弱く効く候補（対策で抑えられる） |
|---|---|---|---|
| **非決定性** | temperature 0 でも、10 回の答えが揃わないマスが gpt-4 で 6/24（SecLLMHolmes、R1 §3-1、高）。ガイドライン "Even with a temperature of 0, full determinism is rarely guaranteed"（`02_…tex:74`、高）。openai の seed は "Determinism is not guaranteed"（高）。`scan --determinism 3` と両立しない | 1、9 | 2・4・6（3 回実行して食い違いは不明、分布を報告）。3・5・8（人が行を確かめる） |
| **再現性**（モデルの廃止、版の固定） | anthropic SDK の `DEPRECATED_MODELS`（`claude-sonnet-4-5` は 2026-11-30、高）。SecLLMHolmes はモデルの廃止で差し替えた（`UPDATES.md:18`、高）。Angermeir ほか：実行できた 5 本のどれも完全には再現できず（中）。D71 の理由 3（`docs/decisions.md:3850-3870`）。主指標がモデルの性質になる。同じプロンプトでも FP 除去率は 26〜52%、検出数は 41〜55 に割れる（R1 §3、高） | 1、6、9 | 2（生の応答を全部保存、open-weight の併用）。3（v3・v4 の記録にモデル名が無い。R3） |
| **データ汚染** | 対象は GitHub で公開されている MCP サーバで、学習データに入りうる（R3 §6、推論）。害は、記憶にある別の版のコードを根拠に示すことと、人と LLM の一致が膨らむこと。汚染の議論は must（ガイドライン `08_…tex:42`、高）。NDSS'26 の P3（高）。LLMDFA は難読化で対処（高） | 4、6 | 2（一致を報告するなら限界に書く）。3（pin した SHA のファイルだけを渡す） |
| **迎合、宣言への引きずられ** | Sharma ほか "five state-of-the-art AI assistants consistently exhibit sycophancy"（高）。ALIBI：安全だと主張するコメントで 90% 超（低）。He ほか（TOSEM、中）。DCIChecker 自身が sycophancy の緩和を書いている（中）。測る対象（宣言・説明文）を作者が書ける（R1 §5-1-5、R3 §3、推論） | 7、6 | 2（宣言の値を渡さず事実だけ問う【統合】）。3（宣言と解析器の答えを渡さない。R3 §8-2）。4 |
| **費用** | トークン数か費用を記録する（ガイドライン `08_…tex:93`、should）。候補 2 は 100 組 × 3 回で小さい（R2）。候補 6 は正解づくりの判定が増える（170〜380 時間の見込みを R4 が引用。上乗せ分かどうかは不明） | 6 | 2、9 |
| **凍結・事前登録とのぶつかり** | D66 と analyzer-freeze-3。走査後の変更は禁止（`final_evaluation_procedure.md:327`）。§2.12 は未記入（`:264`）。モデルとプロンプトを後から選べば、ほぼどんな結論も有意にできる（Baumann ほか "LLM hacking"、低） | 1、5（解析器に足す場合） | 2・4・6・9（事前登録しなければ事後の分析扱い）。8（データを見る前に限る） |
| **判定者 1 人の研究で、LLM の判断を正解に使う循環** | 正解は学生 1 人の判定。LLM のラベルを主にしない（NDSS'26 P2、ガイドライン `07_…tex:19`、高）。κ に依存する主張はしない（`docs/decisions.md:3784`）。補助と比較腕に同じ LLM を使うと独立でなくなる（R4、判断）。LLM の誤りで人の判断が悪くなる（ガイドライン `01-05…tex:54`、高。Perry ほか、低）。練習 6.8 で AI に合わせてしまう危険（R4）。MCP-BiFlow でも、M3 の有無で同じ 859 件のラベルが変わり、レビューのラベルの一部が LLM の出力から来ている可能性がある（R2、推論） | 4 | 2（学生は LLM の出力を見ずにラベル）。3（先に自分で判定）。8 |
| **（追加）不明を消す設計の傾向** | 先行研究のコードは、失敗や迷いを黙って消すか、どちらかに倒す（§1-3 の 1・2、高）。原理 2-a・規則 4 と逆向き | 1 | 2（LLM の「不明」と食い違いを不として数える） |
| **（追加）刈ると本物も消える** | LLM4PFA は TP を 12〜25% 失う（R1 §3-2、高）。Sifting the Noise（低） | 1（矛を刈る場合） | 6 |
| **（追加）文脈の大きい課題では信頼できない** | Ahmed ほか（低）、Lubos ほか（中）、Wang ほか CHI 2024 "they are often erroneous for complex or domain-specific tasks"（中）。AuthGap の判定は複数のファイルを読む課題（R1 §5-2-1） | 4 | 2、3、6 |
| **（追加）LLM でも決まらない類と、決めさせてはいけない類** | 実の類（木の外、運用者の設定：R07、R11、R25）は LLM でも決まらない。定の類（`db_persistent`、一時ファイル、ログ）は原理 §6 と D67 が決める（R4、判断） | 2（対象を意の類に絞らないと） | 8 |

---

## 4. 報告の間の食い違い

1. D66 の行番号は、R1 が `docs/decisions.md:3743`、R4 が `:3749`（凍結）を引いています。同じ決定の別の行かどうかは確かめていません。
2. 「LLM の判断を部品として人手と照らした研究は無い」（R2）は、MCP・エージェントの範囲での話です。R1 の BugLens・Tencent・LLift は、LLM の判定そのものを人手のラベルと照らしています。範囲の違いで、矛盾ではありません。
3. 「正解ラベルを LLM に作らせた研究は無い」（R2）に対し、SecLLMHolmes は採点に LLM を使っています（R1、高）。これも範囲の違いです。
4. LLM の使用の開示先が食い違っています。ACM の 2026 年の文面は方法の節、ICSE 2027 の CFP は謝辞の節です（R3、中）。両方に書けば両方を満たせます。
5. VIPER-MCP の FPR は、本文の逐語では "0% (vs."、LLM が作った要約では 4.6% です（R2）。

---

## 5. 確かめられなかったもの

**論文の本文**（遮断のため。R1 では 1 本も読めていません）
- IRIS：FDR の定義と分母（120 か 121 か）。
- LLift：precision 50% と新規 bug 13 件。
- LLMDFA の 87.10% / 80.77%、LLMSAN の 91.03% / 74.00%。
- BugLens の「7x」の算出方法。
- ZeroFalse：OpenVuln のラベル付けの手順。
- Tencent の論文：会議名と recall の定義。
- 本文で「不明」を別に報告しているか、繰り返しの回数を書いているか。
- 検索の要約しか無いもの（低）：LLM4SA、LLM4PFA、Sifting the Noise、AdaTaint、MoCQ、Chapman ほか、ALIBI、CleanVul。LLM4SA の原典の repo（zenodo は遮断）。
- Ahmed ほかの本文と、課題ごとの κ / α。Wang ほか（ISSTA 2025）の数値。
- 本文が読めていないもの：Zheng ほか（MT-Bench）、SecLLMHolmes、Perry ほか、Baumann ほか、Camporese ほか、He ほか、Chen・Zaharia・Zou、Yuan ほか、Atil ほか、Angermeir ほか。

**MCP 系**
- DCIChecker の本文：DRA の中身（二次資料どうしで食い違う）、モデルと temperature、注釈者の数と κ、DRA のアブレーションの数値、決められなかったときの扱い。
- MCP-BiFlow："uncertain" を集計でどう数えたか。M3 のプロンプト（Zenodo は遮断）。第三者の写しの版。
- VIPER-MCP：使ったモデル、Analytical LLM が何を判断するか、FPR の正しい値。
- TaintP2X：論文側の評価（LLM 検証の精度、アブレーション、人手との一致）。
- Parasites：3 モデルの全員一致投票と、人手での検証の有無。
- MCPDiff と No-Box が判定に LLM を使うか。
- Semia の論文での評価。AgentFlow・MTGuard・MCP-in-SoS が LLM を判定に使うか。
- TRUSTDESC・SemTaint・MCP-BiFlow の写しと原本との照合。
- Cisco の 100 回実行の結果（スクリプトはあるが結果は非公開）。
- Tencent AI-Infra-Guard の MCP 走査のプロンプトと評価。

**道具・方針**
- IRIS・LLift が固定したモデルの版が、今も使えるかどうか。
- BugLens のデモの `EXCLUDED_IDS` を FP 扱いにする理由。
- Vulnhalla の評価とブログ。
- ACM Policy on Authorship の原文。ICSE / FSE の CFP の原文。USENIX Security '27・NDSS 2027・IEEE S&P 2027 の原文。
- OpenAI のモデル廃止のページと Anthropic の docs。ollama の issue #5321。
- 学生の所属大学の生成 AI の規程。0-9 の条件（`final_evaluation_procedure.md:216`）を満たせるかが、これで決まります。

**repo の中**（R4 の範囲）
- v3・v4 で使った AI のモデル名・版・日付（記録に無い）。
- LLM が不の各理由にどれだけ正しく答えるか（測っていない）。
- 理由の和が不の件数を超える組の、重なりの実数。
- `spawn_command` の定数コマンドの例は、git で追っていない manifest から拾ったもので、走査し直さないと再現できません。
- D60 の「本記録者」に、読む補助や別腕の LLM が含まれるか（定義が無い）。
- LLM の補助で判定時間がどれだけ減るか。
- `docs/incidental_writes_practice.md` は直接読んでいません（O44 の要約を通して参照）。

**統合で残った不明**
- 候補 6 の「170〜380 時間」が、LLM ベースラインの上乗せ分なのか、最終評価全体の見込みなのか（R4 の書き方からは読み取れません）。

**参照した報告の作業場所**
- R1 / R2 の clone：`$S/` の下
- R3：`$S/methodology/`
- R4：`/home/user/auth_gap`（変更なし）

この統合では、`/home/user/auth_gap` と `$S` のどちらのファイルも作っても変えてもいません。