# 判定の層に LLM を入れる MCP・エージェント解析の研究: 調査報告

調査日は 2026-10-01 です。`/home/user/auth_gap` のファイルは変更していません。作業ファイルはすべて次の場所に置きました。
`S=/tmp/claude-0/-home-user-auth-gap/9d8a4d2c-1b03-53cb-ba04-44a67affb095/scratchpad/llmjudge`

arxiv.org・zenodo.org・huggingface.co・semanticscholar はプロキシで 403 になりました。WebFetch でも arxiv は EGRESS_BLOCKED です。代わりに次を読みました。
- 自分で clone した repo のコード: MCPScan・TaintP2X・MalSkills・MCP-SEC・Cisco mcp-scanner・Semia
- 著者 repo の論文 PDF: MalSkills
- 第三者の GitHub repo に置かれた論文 PDF やテキストの写し: MCP-BiFlow・SemTaint・TRUSTDESC
- 第三者 SoK repo（azureice10/MCP_SoK）の逐語抜き書き

## 0. 結論

1. **「不」に当たるものを LLM で決めている研究はあります。** ただし「POST が相手の状態を変えるか」を LLM に決めさせ、宣言（readOnlyHint など）と照合する研究は、この調査の範囲では見つかりませんでした。近いのは次の 3 系統です。
   - (a) 記述と実装の意味が一致するかを LLM が判定する: DCIChecker、Cisco mcp-scanner の behavioral、TRUSTDESC
   - (b) 静的に決まらない source・operand・呼び出し辺を LLM が埋める: MCP-BiFlow の M2、MalSkills、SemTaint
   - (c) ガードや sanitizer が効いているかを LLM が裁定する: MCP-BiFlow の M3、TaintP2X、MCPScan
2. **LLM の判断を、部品として人手ラベルと照らした研究は確認できませんでした。** 報告されているのは次の 2 種類だけです。
   - 全体（end-to-end）の精度・再現率
   - LLM を外したときの件数の変化（アブレーション）

   同じ入力で何度か実行したときのぶれを報告した研究も見つかりません。Cisco は 100 回実行してぶれを測るスクリプトを持っていますが、結果は公開していません。
3. **「分からない」は、ほとんどの研究で「報告しない」側に倒されています。** これは AuthGap の原理 2（決まらないものは不明として数える）と規則 4（黙って安全側に倒さない）の逆です。例外は次の 2 つです。
   - MCP-BiFlow: LLM の出力に "uncertain" がある。ただし集計でどう数えたかは本文に書かれていない。
   - Cisco: 「エラーになった関数は safe ではない」と扱っている。
4. **使い道の判定（詳しくは §4）**

   | 使い方 | 判定 |
   |---|---|
   | 解析器の判定に入れる | 使えない |
   | D69 の不の抜き取りで、学生のラベルと比べる「別腕」にする（事前登録が前提） | 条件つきで使える |
   | 判定のとき原ソースを読む補助（0-9） | 使える。ただし別腕と同じ項目では使わない |
   | 関連研究の位置づけ（不明をどう扱うかの対比） | 使える |

## 1. 研究ごとの表

| 研究 | LLM が担う判断 | 入力 → 出力 | モデル・設定 | 検証方法（人手との一致とアブレーション） | 報告された弱点・コードで見た問題 | 根拠 | 確かさ |
|---|---|---|---|---|---|---|---|
| **DCIChecker**（arXiv 2606.04769） | ツールの記述 D と実装 C が意味として一致するか。分類に Eff-SM（状態の変更）と Eff-DL（データの外部送信）を含む | 記述と code bundle（入口・深さ k=3 までの補助関数・危険 API）→ 一致か不一致、加えて類型 | Claude Sonnet 4.5 thinking、temperature 0（仕様書 93 行目。◎' つまり自動要約に依拠） | 逐語: "randomly selected and manually annotated 400 (D, C) pairs from the detection results, including 200 pairs predicted by DCIChecker as consistent and 200 predicted as inconsistent"。精度 96.00%・再現率 97.46%（D_real で 192/197）は LLM が作った要約が出所。DRA を外したアブレーションもあるが、数値は未入手。注釈者の人数と κ は未確認 | 逐語: "bidirectional query validation with judge-based reconciliation to mitigate LLM sycophancy and hallucinations"。DRA の中身は二次資料どうしで食い違う（§5）。決められなかったときの扱いは未確認 | `$S/mcp_sok/packets/yutao-2026-description-code-inconsistency-real-world.md`、`$S/thirdparty/cm_dci.md`、`AUTHGAP_BRIEF_v3.md:93` | 中（逐語の抜き書き）。数値は低 |
| **MCP-BiFlow**（arXiv 2605.07836） | M2: 候補の値が、局所の検証のあとも依頼者が制御できる値か（source の確定）。M3: 曖昧なガードが攻撃者の影響を消しているか | コード片・候補式・ツール名 → `"keep_as_source": true/false, "decision": "keep" \| "drop" \| "uncertain"` | "powered by the gpt-5.3-codex-medium API"（800 行）。土台は YASA（791 行） | 精度は出していない: "we report case-level detections and recall rather than precision"（836 行）。人手のレビュー集合 859 件の内訳は "424 are confirmed, 302 unresolved, and 133 rejected"（1083 行）。M2 を外すと確認済みが 424 → 324。M3 を外すと確認済みは 424 のまま、未解決 302 → 368、棄却 133 → 67（1094–1095 行）。LLM の裁定と人手の一致は測っていない | 限界節: "semantically ambiguous cases require LLM-assisted adjudication"（1150 行）。M3 の有無で同じ 859 件のラベルが変わるので、レビューのラベルの一部が LLM の出力から来ている可能性がある（私の推論） | `$S/thirdparty/polint_mcp-biflow-2026.txt`: 116–119、599–601、630–648、766–769、1076–1111 行 | 高（第三者 repo の PDF 写し。版は未確認） |
| **VIPER-MCP**（arXiv 2605.21392） | LLM は悪用プロンプトの生成と変異を担う（Proxy Agent と Analytical LLM の 2 役）。**真偽は実行の oracle が決める**（計装したサーバで sink に届いたか） | anchor した呼び出し連鎖・ツールのメタデータ → 自然文の PoC プロンプト | RQ4 が "different LLM assignments for the Proxy Agent and the Analytical LLM roles" を比べている。モデル名は未確認 | 良性の集合で "FPR = FP/(TN + FP)"。逐語は "false positive rate of 0% (vs."（ここで途切れる）。LLM が作った digest は 4.6% と書いており、食い違う | CodeQL の taint モデルの網羅に依存する（digest の記述） | `$S/mcp_sok/packets/pengyu-2026-viper-mcp-detecting-exploiting-taint.md`、`$S/thirdparty/fj_0522.md` | 中（役割の構成）。数値は低 |
| **TaintP2X**（ICSE 2026） | 次の 3 つ。(1) メソッドが LLM を呼んで出力を返すか。(2) 連鎖の先頭が LLM API の要求か。(3) 関数ごとに taint が有効か、sanitizer があるか | メソッド本体や Pysa の連鎖 → JSON（`is_llm_call`、`is_taint_valid`、`has_sanitizer`、`sanitizer_functions`）。脆弱性の種類別に方針をプロンプトへ埋め込む。例: ファイル書き込みは「パスと内容の両方を制御できなければ無効と判定せよ」 | `Pro/deepseek-ai/DeepSeek-V3` を SiliconFlow 経由、temperature 0、max_tokens 1024、json_object | 論文の評価は今回読んでいない（未確認） | **公開コードはこのままでは動かない。** `llm_client.py` は import の時点で `NameError: Dict`（実行して確認）。`chat_completion` というメソッドが無い。`chain_prompt` が未定義。失敗・解析不能・「最後の関数の位置が無効」のときは `"is_vulnerability": False`、つまり安全側に倒す | `Source_Identification/llm_client.py:5,8,27`、`confirm_source.py:13-24`、`LLM-assisted_Validation/ds_llm_fully_determine_mul.py:424-536,601,618,627,638`、`ds_llm_source_determine_mul.py:500-518` | 高（コード） |
| **antgroup/MCPScan** | 段 1: Semgrep の当たりから call_tool までの片を LLM が組み立てる。段 2: HIGH・LOW・No Risk の判定。記述の段: 記述 description が悪性か | 違反した片と全ソース → コード片。片 → `{"risk": "HIGH"\|"LOW"\|"No Risk", ...}` | `deepseek-chat`。temperature は指定なし | repo に評価は無い（論文は "coming soon"）。MCP-BiFlow の比較では 11/32 件を検出 | **方針がプロンプトに埋まっている。** "如果...通过POST请求处理后直接返回给LLM的逻辑，则 = LOW"、写入・查询・创建は状態を返すだけなので LOW。JSON の解析に失敗した記述は評価されずに消え、zip で項目がずれうる。50 行を超える片は捨てる。最初の HIGH で残りの評価を打ち切る | `src/mcpscan/core/llm_bridge.py:13,25-29`、`prompts/stage2_py.md:11,16,18`、`core/runner.py:60,213,222,225,292,328` | 高（コード） |
| **MalSkills**（ASE '26） | 抽出（"You are extracting evidence facts, not verdicts."）。operand の推論（"infers missing value flow from local context"）。最後の悪性判定（neuro reasoner） | 成果物・SSO・グラフ → スキーマに縛った JSON（確信度・行番号つき） | 論文では gpt-5.3-codex-medium（801 行）。repo の既定は `gpt-5.6-luna`、API の場合は temperature 0。応答は prompt_version つきでキャッシュする | ベンチマーク 100 悪性 / 100 良性。neuro reasoner を外すと F1 0.93 → 0.71、FPR 0.05 → 0.49。neuro extractor を外してもほぼ不変（933–937 行）。LLM を変えると F1 は 0.76–0.93（986–989 行）。野外: 2 人が独立に判定し、3 人目が裁定（1062 行）。κ と繰り返し実行のぶれは報告なし | 本文: "inherently less stable than symbolic matching"（590 行）。プロンプトは "If a symbolic operand cannot be resolved, preserve it explicitly as unknown"。README: ベースラインでは "errors remain non-malicious predictions" | `$S/ase25_malskills.pdf.txt`、`malskills/sdg/llm.py:25-56,220-300`、`malskills/reasoning/llm.py:28-100` | 高 |
| **Parasites / MCP-SEC**（IEEE S&P 2026、README による） | 記述だけから能力を 3 つ分類する: 外部の公開テキストを読む / 私的情報を読む / 外部へ送る | ツール JSON の記述 → CSV の yes/no ×3 | 既定は `deepseek-r1-250120`。temperature は指定なし。3 つの LLM の全員一致で決める（検索要約） | 人手との照合は未確認 | 行の形が崩れた出力は黙って捨てる。コードは読まない | `tool-analyzer/tools/classifier.py:14,32-41,62-77` | 高（コード）。投票は低 |
| **Cisco mcp-scanner behavioral**（新規） | docstring の主張と、データフロー解析が示す実際の動作との整合 | 入口・CFG・taint・深さ 3 までの呼び出し → `mismatch_detected` と 3 クラス・14 類型 | 既定は gpt-4o、temperature 0.1 | 評価データは 141 個で全部が悪性。出しているのは検出率（再現率）だけ。100 回実行のスクリプトはあるが結果は無い | "**When in doubt, don't flag**"、"Legitimate operations that match the documented purpose (API calls, file I/O, network requests)" は対象外。一方で "an errored function is not 'safe', just unknown" | `mcpscanner/data/prompts/code_alignment_threat_analysis_prompt.md:98,106-108,1330`、`config/constants.py:119-124`、`alignment_orchestrator.py:81-85`、`evals/README.md` | 高（コード） |
| **TRUSTDESC**（arXiv 2604.07536） | 到達しないコードの刈り込み、コードからの記述生成、実行ログを LLM 判定者が見て主張を確かめる | 最小のコード片 → 記述。記述 → 検証タスク → ログ → 判定 | Claude-4.5-Sonnet・Gemini-3-Flash・GPT-5.2・gpt-oss-120b、temperature 0.2 | 間接評価: 生成した記述を使ったエージェントのタスク成功率（実行の痕跡を人が見る）。記述の主張ごとのラベル照合は無い | 実行で確かめられない記述は "are discarded"（314 行付近）。到達しない分岐が残っていると、Claude でも機能を過大に書く | `$S/thirdparty/trustdesc.txt:34,294,314,361` | 高（第三者のテキスト写し） |
| **Semia**（arXiv 2605.00314） | skill の記述とコードから Datalog の事実（効果・トリガ）を合成する。検出は決定的な規則 | 準備した成果物 → `synthesized_facts.dl` と根拠のテキスト | 利用者が設定した LLM か、ホストのエージェント | 根拠のテキストを原文の行に字句で照合し、grounding の閾値 0.2 で切る（幻覚の検出用） | 論文の評価は未確認 | `docs/architecture.md:52-69`、`packages/semia-core/src/semia_core/evidence.py:22`、`checker.py:453` | 高（コード） |
| **No-Box MCPSEC**（arXiv 2609.10854） | メタデータだけから実装を推測し、データフローとリスクを出す（LLM を使うことは推定。要旨では未確認） | ツールのメタデータ → 間接プロンプト注入の仮説（ToC） | 未確認 | 人手の評価者が証拠を段階的に増やして確かめる: メタデータ → ソース → 実行。177 ツール中 95 件を脆弱と確認し、143 件の指摘で再現率 98.9%（要旨）。LLM のベースラインは 84.2% | 精度は出していない。94/143 = 66% は私の計算 | `$S/mcp_sok/packets/zehua-2026-no-box-vulnerability-analysis-description.md`、`$S/thirdparty/atr_nobox.yaml:57` | 中 |
| **SemTaint**（npm。MCP ではない参考例） | "defers to an LLM to resolve call edges that cannot be resolved statically"。source と sink の分類 | 解決できなかった呼び出し → 辺。CodeQL の節点に結べない事実は捨てる | GPT 系と Gemini 系 | 3 回実行して結果の和を取る（"taking the union of results across three executions"）。正確に一致しないものは 2 人で確認 | 意図どおりの機能を誤検出する（CLI のラッパがシェルに渡すなど） | `$S/thirdparty/polint_semtaint-taint-spec-2026.txt:22,579-592,1460-1494` | 高（第三者の PDF 写し） |
| MCPDiff（arXiv 2602.03580） | 記述とコードの一致を 4 段階で付ける（Full / Mostly / Partial / Rare） | tree-sitter の呼び出し連鎖 | 判定に LLM を使うかは未確認 | 未確認 | — | WebSearch、`$S/thirdparty/dv_dci.md:81` | 低 |

## 2. パターンの整理

**P1. LLM が候補を刈る（誤検知を減らす）。** TaintP2X、MCPScan の段 2、MCP-BiFlow の M3、MalSkills の neuro reasoner、Cisco がこれに当たります。外したときに動くのは FP・FPR・棄却の件数で、確認済みの件数はあまり動きません。
- MalSkills: FPR 0.05 → 0.49
- MCP-BiFlow の M3: 確認済みは 424 のまま

**P2. LLM が、静的に決まらない事実を埋める。** MCP-BiFlow の M2（source）、MalSkills の operand 推論、SemTaint（呼び出し辺）、TaintP2X（LLM 呼び出しの特定）がこれに当たります。外したときに動くのは被覆で、MCP-BiFlow の M2 を外すと確認済みが 100 件減ります。AuthGap の `opaque(unresolved)` に最も近い使い方です。

**P3. LLM が記述と実装の意味の一致を判定する。** DCIChecker、Cisco、TRUSTDESC がこれに当たります。Parasites と No-Box はコードを読まず、記述だけで判定します。

**P4. LLM は生成役で、真偽は実行の oracle が決める。** VIPER-MCP、TRUSTDESC の DynVer（ただし最後は LLM の判定者）がこれに当たります。

**P5. LLM が事実を出し、決定的な規則が判定する。根拠の行への照合で幻覚を落とす。** Semia、MalSkills（スキーマ・行番号・キャッシュ）がこれに当たります。

全体に共通する観察は次の 5 点です。
- **方針がプロンプトの文に埋まっていて、感度分析が無い。** 例: MCPScan の「POST は LOW」、TaintP2X の「パスと内容の両方を制御できなければ無効」、Cisco の「迷ったら出さない」。AuthGap は同じ種類の選択を `contradiction_principles.md` §6 に明示し、感度分析もしています。対比として書けます。
- **決められなかった率を報告した研究は無い。** 「分からない」が率として出てこない設計です。
- **人の判定でも決まらないものが多い。** MCP-BiFlow の人手レビューでも 859 件中 302 件（35%）が未解決でした。AuthGap が不と「不明」を数える設計の傍証になります。
- **正解ラベルを LLM に作らせた研究は、今回確かめた範囲では無い。** 最終確認は全員が人手です。
  - MalSkills: 2 人が判定し 1 人が裁定
  - DCIChecker: 400 件を手で注釈
  - MCP-BiFlow: 開示のための人手レビュー
  - No-Box: 人の評価者
  - SemTaint: 2 人で確認
- **モデルによる差が大きい。** MalSkills では LLM を替えると F1 が 0.76–0.93 に動き、再現率は 0.70–0.95 に動きます。

## 3. AuthGap の「不」の理由ごとの対応

数は v4 の `evidence/population_v4/contradiction_by_decl_v4_run1.md` から取りました。

| 不の理由 | 件数 | LLM で決めている近い研究 | 検証のされ方 |
|---|---|---|---|
| `net_post`、`net_nonidempotent_method` | D1 78 / D2 93 / D4 67 | 宣言との照合に直接使った研究は見つからない。MCPScan は別の問い（間接プロンプト注入）で POST を一律 LOW とプロンプトに埋め込む。Cisco は記述どおりのネットワーク要求を対象外にする。DCIChecker の Eff-SM が最も近い | どれも部品としての検証は無い |
| `spawn_command`、`spawn_model_opaque` | D1 64+14 / D3 42+12 ほか | MalSkills の neuro reasoner。論文は `curl \| bash` について "depends on contextual factors such as the source being fetched" と書く。MCP-BiFlow の M3 は検証のあとシェルが悪用できないかを裁くが、コマンドが何をするかは判定しない | end-to-end の評価だけ |
| `fs_writeout`、`db_sql_unreadable` | D2 121 ほか | TaintP2X の種類別プロンプト（書き込みは制御の範囲で判定）。MalSkills の operand 推論 | なし。TaintP2X は公開コードが動かない |
| 記述と実装の意味 | （AuthGap は機械可読な宣言を使う） | DCIChecker、Cisco、TRUSTDESC | DCIChecker の注釈 400 件だけ（下の注意を参照） |

**DCIChecker の 400 件の注意（私の計算。元の数値は確かさ低）。** 400 件は、ツール自身の予測で 200 件ずつに層を分けて取っています。全体（19,200 組、そのうち 9.93% が「不一致」と予測）に重みを戻すと、見積もりは次のようになります。
- 見落とし ≈ 17,293 × 5/200 ≈ 432
- 真陽性 ≈ 1,907 × 192/200 ≈ 1,831
- 母集団の再現率 ≈ 81%（報告値は 97.46%）

層別に抜き取った標本では、重みを戻さない再現率は高めに出ます。AuthGap の見落としの抜き取り（D69 系）でも同じ点に注意が要ります。

## 4. あなたの研究で使えそうか

**(A) 解析器の判定に LLM を入れる: 使えません。** 理由は次の 4 つです。
- 凍結（`analyzer-freeze-3`、D66）に反します。
- 仕様書の主張「LLM を判定入力に使わず決定的に」（`AUTHGAP_BRIEF_v3.md:36`）と §7.3（LLM のベースラインを削除）に反します。
- 調べた設計の多くは「分からない」を「出さない」に変えます。原理 2 と規則 4 の逆です。
- LLM で不を解決した結果は、既に出している感度分析の上下限の間にある 3 つ目の点にすぎません。上限は「不を矛に倒す」で D1 494・D2 412、下限は「宣言内に倒す」で D1 323・D2 155 です。しかもその点の正しさを測った先行研究はありません。

**(B) D69 の不の抜き取り（D1・D2 で各 50 組）に対する「LLM 腕」: 条件つきで使えます。** 査読で「なぜ不を LLM で解かないのか」と聞かれたら、データで答えられます。費用は小さく、100 組 × 3 回です。条件は次のとおりです。
- **学生がラベルを付ける前に事前登録する。** 登録する項目: モデル ID（日付つき）、temperature、プロンプトの全文（コミットのハッシュ）、入力（学生が見るのと同じ根拠）、出力 `{反する / 反しない / 不明}` と根拠の行、3 回実行して食い違ったら不明、不明は不として数える。
- **学生は LLM の出力を見ずにラベルを付ける。** 0-9 で AI の読み補助を使うなら、不の項目には使わないでください。混ざると比較できなくなります。
- **報告の書き方。** 3×3 の一致表と、LLM が「解決した」割合を出します。κ は「学生と LLM の一致」と書き、評定者間一致とは書かないでください（2 人目の判定者の代わりにはなりません）。主指標（矛・不の件数、精度）は変えず、探索的な結果として出します。
- **生の応答を全部保存する。** MalSkills のキャッシュ方式が参考になります。モデルの更新で再現できなくなるからです。
- 所属先の生成 AI の規程（0-9）を確かめてください。

これは新しい決定なので、採るかどうかは学生が決め、`decisions.md` に記録する話です。

**(C) 判定で原ソースを読む補助（0-9）: 使えます。** 先行研究でも最終判定はすべて人手で、手順書 21-6 の運用（AI の結論をそのまま記録せず、根拠の行を自分で開く）と合っています。ただし (B) と同じ項目には使わないでください。

**(D) 関連研究と位置づけ: 使えます。** 「不明をどう扱うか」の対比表が書けます。材料は確かさ高のものだけで揃います。
- Cisco: "When in doubt, don't flag"
- TaintP2X: 失敗すると False
- MCPScan: 解析失敗が黙って脱落する
- TRUSTDESC: 検証できない記述を破棄する
- MCP-BiFlow: "uncertain" の出力はあるが、集計での扱いは書かれていない
- MalSkills: unknown を保持する

## 5. 既存の記録との食い違い

CLAUDE.md の規則 6 に従い、仕様書は書き換えず、`decisions.md` または `open_questions.md` に記録する候補として挙げます。

1. 仕様書 140 行目の「MCP-BiFlow を除く 3 件は LLM を判定経路に置く」は、本文と合いません。本文は M2（source）と M3（ガード）で LLM が候補の採否を決めます（766–769 行の "deferred to LLM-based adjudication"）。M2 を外すと確認済みが 100 件減ります。
2. `implementation_base_survey.md` §5 で未確認としていた「MCP-BiFlow の土台」は YASA です（791 行）。成果物は "available at https://doi.org/10.5281/zenodo.19335837"（145 行）とありますが、Zenodo は遮断されていて中身は見ていません。
3. VIPER-MCP の「QL 1,232 行」は逐語で確認しました（中）。LLM の役割は Proxy Agent と Analytical LLM の 2 つで、悪用の確認は oracle がします。
4. DRA の中身の説明は二次資料どうしで食い違います。
   - 「一致を問う直接の質問と、不一致を問う逆の質問。食い違ったら裁定」: cemini23、WebSearch、codex-blog
   - 「記述から機能を予測し、コードから推定し、比べる」: CMander02（LLM が作った要約）

   本文を読むまで中身は書かないのが安全です。
5. LLM が作った要約は間違えることがあります。VIPER の FPR は逐語では "0% (vs."、digest では 4.6% です。仕様書の ◎' への警戒が裏づけられます。

## 6. 確かめられなかったもの

- **DCIChecker の本文。** 次は LLM の要約か WebSearch が出所で、確かさは低です: DRA のプロンプトの文面、モデルと temperature、注釈者の数と κ、DRA のアブレーションの数値、決められなかったときの扱い。
- **MCP-BiFlow。** "uncertain" を集計でどう数えたか（本文に記述なし）。M3 のプロンプト（成果物は Zenodo で遮断）。第三者の PDF 写しの版（v1 か後の版か）。
- **VIPER-MCP。** 使ったモデル。Analytical LLM が何を判断するか。FPR の正しい値（0% か 4.6% か）。
- **TaintP2X の論文側の評価。** LLM 検証の精度、アブレーション、人手ラベルとの一致。今回はコードだけ読みました。
- **Parasites。** 3 モデルの全員一致投票（検索要約のみ）と、人手での検証の有無。
- **MCPDiff が判定に LLM を使うか。** No-Box MCPSEC が LLM を使うか（推定のみ）。
- **Semia の論文での評価。** AgentFlow・MTGuard・MCP-in-SoS が LLM を判定に使うか。
- **TRUSTDESC・SemTaint・MCP-BiFlow の写しと原本との照合。** どれも第三者 repo の写しです。
- **Cisco の 100 回実行の結果。** スクリプトはありますが、結果は公開されていません。
- **Tencent AI-Infra-Guard の MCP 走査のプロンプトと評価。** README しか読んでいません。