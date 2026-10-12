# 同一研究は見つからず、reachscan が「Python で唯一」を崩した

**AuthGap と完全に同じことをしている先行研究は、7 本のノートが調べた範囲では見つからなかった。** ここで「同じこと」とは、Python の MCP サーバについて ToolAnnotations の 4 つのヒントを、ツールの入口から呼び出し先まで静的・決定的に追った効果と照らし、解決できないものを `opaque(reason)` として率で出し、事前登録・解析器の凍結・人の判定・開発者の注釈修正コミットによる再現率で評価することを指す。調べた範囲は arXiv、2026 年の主要会議、国内の会議と学位論文、OSS とグレー文献である。ただし核の検査そのものには、もう並ばれている。最も近いのは OSS の **reachscan** である。2026-10-05 の v0.3.0 で `ANNOTATION_MISMATCH` を入れ、Python の MCP ツールで明示された `readOnlyHint` / `openWorldHint` / `destructiveHint` を、プロジェクト内のコールグラフ（最大 8 hop）で届く効果と照らすようになった。このため `docs/related_work.md`（2026-10-02/03）の「Python の MCP サーバについて、宣言を読み、呼び出し先まで追う静的な解析は、AuthGap のほかに見つからなかった」という文は、**前回の調査の 2〜3 日後に成り立たなくなった**。論文では CCS 2026 の **ContractGuard** が、MCP ツールの入口から手続き間でたどり、宣言と実装の食い違いを母集団で測るという同じ骨格を持つ。ただし宣言は自然言語の説明で、判定は LLM が行う。これに DCIChecker、HintLint、BIV、PrivLess、SkillScanner が続く。AuthGap が今も新しいと言えるのは個々の部品ではない。言えるのは 2 つで、1 つは **構造化された 4 つの副作用ヒント × Python の手続き間の静的解析 × opaque の率を主結果にすること × 事前登録した母集団と解析器の凍結 × 人の判定 × 注釈修正コミットによる再現率、という組み合わせ**である。もう 1 つは 3 つの細部で、`idempotentHint` の照合、注釈の修正を正解にすること、同じ解析器での深さ 0 アブレーションである。**ToolAnnotations の値をコードと照らした論文**は今も見つからない。98,291 ツールの census（arXiv 2609.15397）が「measuring the gap requires implementation-level analysis」と書いて残した空白を、AuthGap が埋めるという位置づけは使える。

表記について。確認の水準は各ノートの判定をそのまま写した。◎ は一次資料の本文やコードを読んだもの、○ は要旨・README・公式ページを読んだもの、△ は二次情報である。ノートの間で水準が違うものは両方を書いた。この報告書で水準を上げたものは無い。**論文と README の数値はすべて著者の主張で、こちらでは検証していない**（CLAUDE.md 規則 1、`verified_by_me = none` に当たる）。「見つからなかった」は検索した範囲での話で、「存在しない」の意味ではない。判定の語はノートと同じ 4 段（同一 / 大きく重なる / 部分的に重なる / 隣接）を使う。

## 最も近い 13 件のどれも、9 つの軸を全部はそろえていない

順位は、AuthGap の新規性の主張をどれだけ崩すかで付けた。具体的には、共有する軸の数、同じ MCP の領域かどうか、査読を経ているかを見た。表の後に読み方を書く。

| 順位 | 仕事（種別・時期） | 水準 | 宣言側 | 効果側 | 呼び出し先 | Python | 未解決の扱い | 母集団・人の正解 | 決定論 | 事前登録・凍結 | 修正コミットの再現率 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | **AuthGap**（参考） | — | ToolAnnotations の 4 ヒント（D1〜D4）、前のリリース（r_prev） | 静的。効果 kind と slot、引数位置ごと | 手続き間、深さ ≤4 | ○ | `opaque(reason)` 8 語、率を主結果に | 事前登録した母集団 v2、人の判定 | ○ | 事前登録、`analyzer-freeze-3` | 352 件（D79） | — |
| 1 | [reachscan](https://github.com/vinmay/reachscan)（OSS、v0.3.0 = 2026-10-05） | ◎ コード / 評価は ○ | 明示された readOnly・openWorld・destructive。idempotent は見ない | AST の能力検出（WRITE / EXECUTE / DYNAMIC / 外向き接続） | プロジェクト内を BFS、最大 8 hop | ○ | 未解決のメソッド呼び出し先は `unknown`。不一致を作らず、率も出さない | 38 repo ＋公式 git サーバで不一致 16 件、確認済み TP 1 件（著者） | ○ | なし（corpus を見ながら規則を調整） | なし | 大きく重なる |
| 2 | [ContractGuard](https://huhong789.github.io/papers/ye:contractguard.pdf)（CCS 2026、Ye ら） | ◎（主要節） | 自然言語の説明 | Tree-sitter のスライス ＋ LLM の要約 | 入口から DFS（上限の記載なし） | ○（TS も） | 未解決のシンボルは LLM が探して埋める | 無作為の 1,000 サーバ・3,586 ツール。311 ツールを人手で監査（著者） | ×（LLM、温度 0.2、走査順に依存） | なし | なし | 大きく重なる（問いと骨格） |
| 3 | [DCIChecker](https://arxiv.org/html/2606.04769v1)（arXiv 2606.04769、前回の調査） | 前回は引用を照合済み / 今回 ○ | 説明文（名前・スキーマ・説明） | AST ＋ LLM の仲裁 | プロジェクト内、深さ 3 | ○ | 出力は一致 / 不一致だけ | Python 2,214 サーバ。層別した 400 組を 2 人が付け、第 3 者が裁定（著者） | ×（LLM の仲裁） | なし | なし | 部分的に重なる |
| 4 | [HintLint](https://github.com/complira/hintlint)（OSS、前回の R1） | 前回ソースを確認 / 今回 ○・△ | readOnly・destructive・openWorld | 静的な規則 | Python は本体だけ（TS/JS は深さ 4） | ○ | 解決したハンドラの中の未解決を表す語が無い | 20 repo のパイロット、23 件・精度 82%（著者） | ○（LLM の記述なし） | なし | なし | 大きく重なる |
| 5 | [BIV](https://arxiv.org/html/2605.11770v1)（arXiv 2605.11770、スキル） | ◎ | frontmatter と散文の能力集合（LLM 抽出を含む） | Python AST の手続き間 taint ＋ LLM | 手続き間（深さは不明） | ○ | 数えない（下限として扱い、確度を 3 段に分ける） | 49,943 スキル、80.0% が逸脱。正解は LLM パネル（著者） | × | なし | なし | 大きく重なる |
| 6 | [PrivLess](https://arxiv.org/abs/2607.02875)（arXiv 2607.02875、サーバーレス） | ◎ | IAM 文（**強制される**） | CodeQL ＋ SDK→権限の知識ベース | 入口ごとの call graph | ○（151 アプリ） | 宣言から補う。完走しない 10.95% は除外 | 789 アプリ、47.7% が過剰。機能試験は 5 アプリ（著者） | ○ | なし | なし | 大きく重なる（ただし過大宣言の側だけ） |
| 7 | [SkillScanner](https://par.nsf.gov/servlets/purl/10527328)（CCS 2023、Alexa） | ◎ | manifest の自己申告 yes/no と権限 | CodeQL の taint | 明記なし | ○（JS も） | 率の報告なし | GitHub の 2,451 スキル。99/126 が過小申告。100 件で P 90%・R 87%（著者） | ○ | なし | なし | 大きく重なる（古典） |
| 8 | [mcpscan-cli MCP013](https://github.com/glatinone/mcpscan)（OSS、2026-07-14） | ◎ コード（06 では ○） | readOnly=true と destructive=false の値、4 キーの有無 | 生テキストの正規表現 | 深さ 0（最大 40 行の窓） | ○（JS/TS も） | 概念が無い | なし（単体テスト 7 件だけ） | ○ | なし | なし | 部分的に重なる |
| 9 | [MCPSafe MCP-200](https://mcpsafe.io/threats/MCP-200)（スキャナの規則） | ○ | readOnly・destructive と名前の正規表現 | sink の照合と同一ファイル内の taint（deep scan は LLM 5 体の投票） | 同一ファイル内 | 不明 | 記載なし | 非公開 | 一部 × | なし | なし | 部分的に重なる |
| 10 | [AgentSecGraph](https://arxiv.org/abs/2610.03014)（arXiv 2610.03014） | ◎（02）/ ○（01） | なし | Python AST の sink とガードの証拠 | 手続き内 | ○ | 依存の証拠を回復できた割合 41.15% | 凍結した 67 repo、参照は 22 挙動（著者） | ○ | **解析器の凍結**（事前登録はなし） | なし | 部分的に重なる（効果側） |
| 11 | [Agent Approval Laundering](https://arxiv.org/abs/2609.28586)（arXiv 2609.28586） | ◎ | ホストの承認記録 | 決定論的なパーサ ＋ 実行後の証拠 | ワークフローの展開を追う | 一部 | residual を数える | 111 対、事前指定の holdout 17（著者） | ○ | **パーサの凍結と事前指定の holdout** | なし | 部分的に重なる（構図と規律） |
| 12 | [Stowaway](https://comp97109.doc.ic.ac.uk/reading/felt_ccs_11.pdf)（Felt ら、CCS 2011） | ◎ | Android の権限（**強制される**） | 静的な API の使用 | 深さ 2 | — | 未解決の reflection を持つ群を別に報告（105/900） | 940 アプリ、40 件を手で分析（著者） | ○ | 開発用に 24 アプリを取り置き | なし（偽陰性は測っていない） | 同一設計のリスク高（方法論） |
| 13 | [山崎・戸田・森](https://ipsj.ixsq.nii.ac.jp/records/2007264)（IPSJ SPT、2026-02） | ○（抄録） | 呼び出し要求の内容 | 動的（OS の監査ログ） | 該当せず | 不明 | 記載なし | 作成した 21 シナリオ、P 1.00・R 0.81（著者） | 不明 | なし | なし | 部分的に重なる（国内） |

表を縦に読むと、二つの型があることが分かる。**道具は検査を共有し、論文は評価を共有している。両方を共有するものは無い。** reachscan、HintLint、mcpscan-cli、MCPSafe は AuthGap と同じ構造化ヒントを読む。しかし母集団での率、人の正解、凍結、修正コミットの再現率のどれも持たない。ContractGuard、DCIChecker、BIV は母集団と人手（または LLM）の正解で率を出す。しかし構造化ヒントを読まず、判定に LLM を使う。AgentSecGraph、Approval Laundering、Stowaway は凍結・取り置き・未解決の群の別扱いといった作法を持つが、ToolAnnotations とは照らさない。「修正コミットの再現率」の列は、AuthGap 以外の 13 行すべてで「なし」である。

## reachscan は 10 月 5 日に核の検査を実装し、前回調査の一文を崩した

reachscan の最初のコミットは 2026-02-21 にさかのぼる。注釈の抽出は 2026-10-04 に入り、照合（`ANNOTATION_MISMATCH`、SARIF の rule id は `mcp-risk-mismatch`）は 2026-10-05 に PR #32 で merge された。その 2 日後の 2026-10-07 に v0.4.0 が出ている（[PR #32](https://github.com/vinmay/reachscan/pull/32)、[commit 65c8ca6](https://github.com/vinmay/reachscan/commit/65c8ca6d7c24ee3feb98d2745e2a89acd0fef5de)）。規則は 3 つある。1 つ目は、**`readOnlyHint: true` のツールから WRITE / EXECUTE / DYNAMIC に届けば high** とするもの。2 つ目は、`openWorldHint: false` のツールから外向きの HTTP / websocket / socket の接続に届けば不一致とするもの（literal の loopback は除き、v0.4.0 で medium に下げた）。3 つ目は、`destructiveHint: false` を、`readOnlyHint` が false のときに限り、削除・移動・切り詰めの書き込みに届けば medium とするもの。**`idempotentHint` は検査しない**。また EXECUTE は destructive の矛盾に数えない。理由は「on the phase-3 corpus every EXECUTE hit was a harmless launch (V decision, 2026-10-05)」と書かれている（[annotation_mismatch.py @4f6509d](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/analysis/annotation_mismatch.py)）。調べるのは明示されたヒントだけで、既定値のヒントは「claim nothing」として扱う。不一致にはツールの入口から sink までの経路を必須にしている。探索の深さは `TRAVERSAL_DEPTH = 8` である（[reachability.py L64](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/reachability.py#L64)）。低水準のサーバについては、`types.Tool` を `call_tool` の中の `if name == …` や `match name:` の分岐に結びつける。AST だけで動き、LLM は呼ばない。

**AuthGap との差が最もはっきり出るのは、解決できないものの扱いである。** コールグラフは 4 段で名前を解決する。どれにも当たらない辺について、docstring は「unresolvable → edge dropped silently」と書いている（[call_graph.py](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/src/reachscan/call_graph.py#L44-L60)）。v0.4.0 では、解決できないメソッド呼び出しの先にある finding を `unknown` に分けるようになった。ただし README は「They can't produce an annotation mismatch and don't affect the exit code.」と書き、CHANGELOG が報告するのは「110 of 1,257 unreachable Python findings become unknown (7 repos)」という件数だけである（[README](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/README.md)、[CHANGELOG](https://github.com/vinmay/reachscan/blob/4f6509d812b3c40769ddce0ea0bee548bfe24e02/CHANGELOG.md)）。判定の水準で見ると、`unknown` は「不一致なし」の側に落ちる。これは CLAUDE.md 規則 4 が禁じる「黙って安全側に倒す」扱いにあたる。前回の調査が R1 について「差分は『解決できなかったものをどう扱うか』に尽きる」と書いた構図は、reachscan にもそのまま当てはまる。

評価は弱い。PR #32 の本文によれば、phase-3 corpus（38 repo と公式の git サーバ）で不一致が 16 件出た。内訳は read-only が 15 件、closed-world が 1 件で、15 件は 1 つのサーバから出ている。第三者のサーバで「one confirmed true positive」があったという（`openWorldHint: false` のツールがリモート API に POST していた。詳細は非公開）。precision の修正として、closed-world の FP 52 件と destructive の 9 件を除いている（[PR #32](https://github.com/vinmay/reachscan/pull/32)、○、著者の主張）。README にある FP 率 0.47%（約 3,900 件のラベル）は能力の finding についての値で、**不一致の精度ではない**。corpus の一覧は公開されていない。さらに、規則を corpus を見ながら調整している（EXECUTE を外す、openWorld を medium に下げる）ので、その 16 件は事前に定めた検査の結果ではない。**AuthGap の凍結と事前登録が差になるのは、まさにこの点である。**

学生がすることは三つある。一つ目に、関連研究の節で reachscan を「同時期の OSS ツール」として必ず挙げ、前回の一文が崩れたことを書く。二つ目に、残る差を四点で書く。(1) 事前登録して凍結した母集団での測定、(2) 注釈ごとの opaque の率、(3) 人の正解と修正コミットからの再現率、(4) `idempotentHint` の照合と、SQL 文・HTTP メソッド・引数位置の粒度での判定（reachscan は WRITE / SEND の粒度）である。三つ目は比較の手順である。検出力を比べるなら、まず HintLint と mcp-doctor にしたのと同じく `evidence/related_work_20261002/depth_probe/` で動かす。D79 の 352 件に当てるなら、D80 と同じく「見つけた」と数える規則を走らせる前に決定として書く。凍結の後に足す比較は `docs/preregistration.md` に逸脱または exploratory として記録する。走らせる前に「勝る」とは書かない。

## 論文は同じ問いを、自然言語の宣言と LLM の判定で解いている

### MCP の論文では、照合するものは説明文を読み、注釈を読むものは照合しない

ContractGuard（Penn State、CCS 2026、DOI 10.1145/3830454.3846789）は、査読を経た論文の中で最も近い。MCP ツールの「developer-provided description」と「implementation」を二つの見方として扱う。入口は `@mcp.tool()`、`mcp.add_tool()`、`server.tool`、`server.RegisterTool`、`@mcp.list_tools()/call_tool()`、`setRequestHandler()` から特定する。そこから Tree-sitter の AST で呼び出しを深さ優先にたどり、LLM が要約と照合を行う。評価は MCP.so から無作為に選んだ 1,000 サーバ・3,586 ツールで、116 件の問題を見つけたとしている。311 ツールを人手で監査した部分集合では P=0.824、R=0.778 だった（[ContractGuard PDF](https://huhong789.github.io/papers/ye:contractguard.pdf)、◎ 主要節、著者の主張）。本文には「a tool described as supporting read-only SQL queries」という例があるが、read-only は**自然言語の説明の側**で扱っている。"annotation" や "readOnlyHint" の語は本文に無い。著者自身が限界として「AST-based slicing may miss call relationships obscured by complex indirection in dynamic languages such as Python and JavaScript … can cause errors in both directions」と書いている。既定の LLM は温度 0.2 の GLM-5.1 で、ツールの発見は `os.walk` の走査順に依存する。**同名の別論文に注意すること。** arXiv 2606.18550 の ContractGuard は、ゲートが読むツール契約を署名と attestation で守る研究で、コードとは照合しない（[arXiv 2606.18550](https://arxiv.org/abs/2606.18550)、○）。ICLR 2027 への投稿 CPI は、LLM 系の MCP スキャナが「修正済み」という文脈の主張に引きずられることを示した。ベースラインで陽性だったリポジトリの半数超で、本物の発見が抑え込まれたという（[OpenReview CPI](https://openreview.net/forum?id=7TImfQIpSU)、○、著者の主張）。AuthGap が判定に LLM を入れない理由を、外部から裏づける材料になる。

前回の調査で最も近い論文とされた DCIChecker は v1 のままで、注釈の語は本文に 0 件である（[DCIChecker HTML](https://arxiv.org/html/2606.04769v1)、[arXiv API](https://export.arxiv.org/api/query?id_list=2606.04769,2602.03580,2609.10854,2605.21392,2608.07639)、○）。ノート 01 が確かめた既知の 19 本で改訂されたのは、No-Box v2、VIPER-MCP v2、AgentBound v3、SkillScope（2605.05868）v3 の 4 本である（ノート 02 はほかに MCPTox v2 を確認した）。どれも ToolAnnotations を読むようにはなっていない。arXiv API で `destructiveHint` を検索すると 0 件だった。全文 HTML を取得して注釈の語を数えた 30 本あまりでも、ヒットは 2 本だけだった。その 2 本はどちらも宣言だけを測る研究である。1 本は 98,291 ツールの census で、「The census reads the boundary as declared, not as implementations behave … measuring the gap requires implementation-level analysis」と書く（[arXiv 2609.15397](https://arxiv.org/html/2609.15397)、◎）。もう 1 本は registry から seed つきで無作為に抽出した 400 サーバの研究である。ツールの 58.8% が注釈を持たず、curated な母集団はこの率を **17.3 ポイント良く見せる**と報告している（[arXiv 2609.10962](https://arxiv.org/abs/2609.10962)、◎、著者の主張）。後者は、AuthGap の母集団 v2（宣言あり、D29）を生態系全体の率として読めない理由として、そのまま関わる。

効果の側だけを見る研究も 2026 年秋に増えた。AgentSecGraph は MCP/FastMCP と 6 つのフレームワークの入口を正規化し、sink とガードの証拠を決定論的に組み立てる。解析器も凍結している。ただし解析は手続き内に限られ、「Python analysis is not a complete whole-program interprocedural … analysis」と明記している（[arXiv 2610.03014](https://arxiv.org/abs/2610.03014)）。MCPacific は 7 言語で **56 の登録パターン**を使い、124,267 サーバから 1,328,233 ツールの入口を抽出する（56 はノート 01 の原文引用による。ノート 02 は「30 の登録パターン」と書いており、食い違う）。取り出すのは 5 項目だけで、効果は推定しない（[arXiv 2610.05319](https://arxiv.org/html/2610.05319v2)、◎（02）/ ○（01））。FCD は公式のソースから効果を過大近似で要約し、UNKNOWN と reject を明示する。評価では「preregistered stock comparison」と「frozen 16-release expansion」を使っているが、注釈とは照らさない（[arXiv 2609.35088](https://arxiv.org/html/2609.35088)、○）。宣言を経時に比べる側には mcpindex がある。「1,936 tools flipped a read-only hint toward write, delete, or send」と数えつつ、自らを「A contract-diff, not a safety verdict」と位置づけている（[mcpindex ledger](https://mcpindex.ai/ledger)、○）。もう 1 つの mcp-tool-drift は、既に宣言されていたヒントの反転を 4 サーバで 12 件見つけ、どれもリリースノートに無かったとする（[mcp-tool-drift](https://github.com/vru123/mcp-tool-drift)、○）。どちらも宣言どうしの差分で、**宣言の変化がコードの変化に裏づけられているか（AuthGap の r_prev）は誰も測っていない**。OpenAI は Apps の審査で annotation の「automated review」をしていると公式に書いているが、何と照らしているかは公開していない（[OpenAI Apps SDK guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)、○）。M8ven も「source-side AST check」を行うが、方式は非公開である（[cpp-mcp PR #68](https://github.com/CHOCEK-RB/cpp-mcp/pull/68)、○）。bex.co のブログにある「508 サーバで 612 件の privilege annotation mismatch」は、元の調査が見つからなかった（[bex.co](https://bex.co/blog/2026/09/24/mcp-annotations-server-authoritative-dry-run-gap)、△）。**出典不明の数値なので引用しない**。

### スキルでは、同じ問いがすでに 5 万件の規模で測られている

BIV は、スキルの宣言（frontmatter・tool.json・散文）を 29 の能力に写し、実装の能力集合と比べる。Python は「AST traversal supports inter-procedural taint analysis」で読む。OpenClaw の 49,943 スキルの 80.0% が宣言から逸脱したと報告している。逸脱は 250,706 件で、うち 135,187 件はコードにあって宣言に無い側だった（[arXiv 2605.11770](https://arxiv.org/html/2605.11770v1)、◎、著者の主張）。ただし正解は LLM 3 体のパネルで、著者自身が「human-labeled gold at registry scale remains future work」と書く。解決できないものは「the deviation count is a lower bound」として扱い、率は出さない。**「SkillScope」という名の論文は 2 本あり、別物である。** arXiv 2605.12875（He ら、「Do Skill Descriptions Tell the Truth?」）は SKILL.md の説明と実装の不整合を扱う。4,556 スキルを二重盲検の人手で確かめ、P 84.8%・R 96.5%、不整合は 9.4% と報告している（[arXiv 2605.12875](https://arxiv.org/abs/2605.12875)、○）。前回の related_work.md の SkillScope の行はこちらを指す。arXiv 2605.05868（Wu, Nan ら、CCS 2026、v3 2026-09-10）は最小権限の強制の研究である。LLM の分類器を使い、68,312 スキルのうち 6,590 件を過剰権限と判定した（[arXiv 2605.05868](https://arxiv.org/abs/2605.05868)、◎（02）/ ○（03））。照らす相手は、ノート 02 では宣言されたスキルのプロファイル、ノート 03 ではユーザのタスクと読んでいる。方法の作法として最も引く価値があるのは Scan the Skill である。全てのコマンドを必ずどこかに写す決定論的なリゾルバを使い、自分の計測器の欠陥について「A block that failed to classify is not a block that classified as harmless」と書いて、失敗の件数を毎回の結果に並べている（[arXiv 2609.12001](https://arxiv.org/html/2609.12001v1)、◎）。

国内では、早大の山崎・戸田・森が「宣言外のリソースアクセスや副作用」を検知している。プロキシで記録した呼び出し要求と OS の監査ログを、呼び出し単位で対応づける**動的な**手法で、21 のシナリオで P 1.00・R 0.81 と報告している（[IPSJ 電子図書館](https://ipsj.ixsq.nii.ac.jp/records/2007264)、○）。CSS2026 の 2D1-1「安全なMCPレジストリのための検証フレームワークの提案と実証評価」（東京都市大）は、題しか公開されていない（[CSS2026 プログラム](https://www.iwsec.org/css/2026/program.html)）。**構造化された注釈を、インストール前の静的解析でコードと照らす国内の発表は見つからなかった。**

## エージェントの外では、同じ骨格が 2011 年から逆の向きを測ってきた

「入口ごとの call graph → 静的に推定した必要集合 ↔ 宣言集合 → 野外の率」という骨格には長い系譜がある。Stowaway（2011）、[COPES](https://arxiv.org/abs/1206.5829)（2012）、SmartThings（2016）、[Chrome 拡張の SoLP](https://www.cse.chalmers.se/~andrei/ijis22.pdf)（2022）、[EPScan](https://github.com/seclab-fudan/EPScan)（2025。対応づけの一部に温度 0.6 の LLM を使う）を経て、PrivLess（2026）まで続く。**AuthGap はこの骨格そのものを新規性にできない。** PrivLess は入口ごとに call graph を作って必要な IAM アクションを推定し、宣言と照らす。789 アプリの 47.7% に過剰な権限があったとする（[arXiv 2607.02875](https://arxiv.org/abs/2607.02875)、◎、著者の主張）。ただしその Pass 1 は、宣言に無い推定権限を捨てる。理由は「This bounds the inferred set strictly by developer intent, given the assumption that developer-defined permissions are functional」である。宣言が強制される系統では、宣言が狭すぎるとプログラムが動かなくなるので、過小宣言は構造上見えない。AuthGap の「安全側への嘘」（`readOnlyHint: true` なのに書く）は、ここでは原理的に測れない。とはいえ、**強制されない宣言の過小申告を測った先例はある。** SkillScanner は Alexa の manifest にある自己申告の yes/no を CodeQL の taint と照らした。データ収集があり、申告欄を選んでいた 126 件のうち、99 件が「個人情報を使わない」と申告していたと報告している（[SkillScanner PDF](https://par.nsf.gov/servlets/purl/10527328)、◎）。BIV もスキルで同じ向きを数えている。したがって AuthGap が言えるのは、「副作用のヒントについて、MCP で、この向きを初めて母集団で測った」までである。

助言的な宣言がどれだけ間違っているかについては、Ernst ら（ICSE 2016）が最も直接の先例である。`@GuardedBy` を書いた全てのプログラムに誤った注釈があり、開発者の注釈は precision 19–100%、recall 6–84% だったと報告している（[Ernst ら PDF](https://homes.cs.washington.edu/~mernst/pubs/locking-inference-checking-icse2016.pdf)、◎）。一方、`@Pure`、Kotlin の `@Contract(pure=true)`、C# の `[Pure]` について、誤用率を測った研究は見つからなかった。照合の仕組みだけを見れば、CodeQL のクエリ `java/csrf-unprotected-request-type` がすでに同じことをしている。GET 系のハンドラから DB 更新への到達を call graph で探すもので、readOnlyHint の照合と同じ機構である。ただし評価は公開されていない（[CodeQL query help](https://codeql.github.com/codeql-query-help/java/java-csrf-unprotected-request-type)、○）。Rubio-González と Liblit（PASTE 2010）は、man ページが宣言するエラーコードを、52 のファイルシステムの実装から手続き間解析で求めた値と照らした。そのうえで「多くの実装が同じ食い違いを示すなら文書が悪い」と読み分けている（[PASTE 2010](https://pages.cs.wisc.edu/~liblit/paste-2010/)、◎）。この読み分けは、SDK の既定値やテンプレートに由来する系統的な誤宣言を見分けるのに転用できそうだ（推論）。冪等性については、Flux（OSDI 2023）が冪等性を合成的に検証している。ただし照らす宣言は無く、プラットフォームが暗黙に求める要件を検証するものである（[Flux PDF](https://www.usenix.org/system/files/osdi23-ding.pdf)、◎）。gRPC の `idempotency_level` を実装と照らす検査器も見つからなかった（[protobuf.dev](https://protobuf.dev/reference/java/api-docs/com/google/protobuf/DescriptorProtos.MethodOptions.IdempotencyLevel.html)）。`idempotentHint` の照合が空白として残るのは、この系譜全体を見ても同じである。

この系統で解決できないものの扱いは、4 つに分かれる。(a) 黙って範囲外にする（Chrome 拡張の eval）。(b) 手作業に回したうえで違反なしに倒す。SmartThings は動的呼び出しのある 26 アプリを手作業に回し、「elects to mark SmartApps as not overprivileged if it cannot determine」と書いている（[SmartThings PDF](https://comp97109.doc.ic.ac.uk/reading/fernandes_sp16_smarthome.pdf)、◎）。(c) 宣言から補う（PrivLess の Pass 2）。(d) 解析に失敗したものを除外する。**ユニットごとの未解決率を主な指標にした例は、読んだ範囲では見つからなかった。**

## 測定の作法は部品ごとに先例があり、新しいのは束ね方と 3 つの細部だ

方法論のノートの結論ははっきりしている。どの部品も単独では新しくない。安全な書き方は「既存の規範（soundiness、Registered Reports、test-retest、修正コミット由来の再現率）を、宣言と実効を照らす静的な測定の一つの設計に束ねた」である。

| 部品 | 先例の状況 | 代表 | AuthGap が言えること |
|---|---|---|---|
| 未解決を理由つきで数える | 規範は 2015 年に確立。JS では解決率が定番の指標。Python で効果の単位の率を主結果にした例は見つからない | [Soundiness manifesto](https://yanniss.github.io/Soundiness-CACM.pdf)、[Jelly](https://www.cs.au.dk/~amoeller/papers/approx/paper.pdf)、[Monat ら 2020](https://hal.sorbonne-universite.fr/hal-02876667/document)（未対応構文を unsoundness alarm として全数報告）、[PyCG](https://arxiv.org/abs/2103.00587)（定性的な列挙だけ）、[PyFlow](https://arxiv.org/abs/2608.07026)（timeout を不検出に畳む反例） | 規範への準拠として書き、新しいのは「Python・効果の単位・8 理由」の具体性に限る |
| 三値目 unknown の率 | 検証の分野では標準。測定研究にも先例がある | [SV-COMP](https://www.sosy-lab.org/research/pub/2016-TACAS.Reliable_and_Reproducible_Competition_Results_with_BenchExec_and_Witnesses.pdf)（Unknown は 0 点、timeout も Unknown）、[Stowaway](https://comp97109.doc.ic.ac.uk/reading/felt_ccs_11.pdf)（未解決群の警告率 53% と 31〜34%）、[Gao ら 2017](https://janvitek.org/events/NEU/7575/pubs/no-type.pdf)（unknown 18 件は後に解消） | 新しくない。unknown を最後まで残す点が Gao と違う |
| 事前登録 | SE では 2020 年から標準。静的解析の測定に使った例は見つからない | [Ernst & Baldassarre 2023](https://arxiv.org/abs/2302.03649)、[Empirical Standards RR](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/RegisteredReports.md)、[FUZZING 2022](https://www.ndss-symposium.org/ndss2022/cfp-fuzzing-workshop/) | 「適用例として珍しい」までは言える。「初」とは書かない |
| 評価前の解析器の凍結 | 原理は確立している。近い実践を今回 3 件見つけた | [Arp ら 2022](https://arxiv.org/abs/2010.09470)（test snooping）、FCD、Approval Laundering、AgentSecGraph | 凍結そのものは新しくない |
| 修正コミットを再現率の正解にする | 2012 年から標準 | [Thung ら 2012](https://doi.org/10.1145/2351676.2351685)、Gao 2017、[Habib & Pradel 2018](https://doi.org/10.1145/3238147.3238213)、[Khan ら 2022](https://rebels.cs.uwaterloo.ca/papers/tse2021_khan.pdf)（Python） | **宣言（注釈）の修正**を正解にした例は見つからない |
| 単独の評定と test-retest | 正当化があれば許容される。ただし実践は稀 | [Empirical Standards IRR](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/supplements/InterRaterReliabilityAndAgreement.md)、[Kitchenham & Charters 2007](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf)。反論の根拠は [Repository Mining 基準](https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/standards/RepositoryMining.md) | 新しくない。正当化の枠組みには乗る |
| 深さ 0 のアブレーション | 明示的な先例は見つからない | PyCG 対 Pyan（別ツールどうし）、[Li ら ICSE 2024](https://arxiv.org/abs/2401.09767)、[ATLANTIS](https://arxiv.org/abs/2509.14589)（Joern の既定の深さは 4。ただし「not practical」と評する） | 「同じ解析器の中で深さだけを変える」と強調すれば言える |

ノート 05 は、3 つ以上の部品を組み合わせた先例として 2 件を挙げた。Stowaway（宣言と実効の照合、未解決群の別扱い、開発用の取り置き、手作業の precision）と Gao ら（修正コミット由来の再現率、unknown と時間予算、主評定者 1 名と較正）である。ノート 01 の FCD（UNKNOWN の明示、事前登録、凍結）も同じ程度にそろえているが、注釈とは照らさない。**事前登録・解析器の凍結・未解決率を主結果にすること・修正コミット由来の再現率のうち、4 つ以上をそろえた研究は見つからなかった。** Empirical Standards の RR 基準は、AuthGap の運用を外から評価する物差しとしてそのまま使える。たとえば「deviations, if any, are _not_ justified based on the data」は凍結の規則と逸脱 #26 に、「Pre-registrations that are not verifiably committed prior to data collection, e.g. not time-stamped」は期待値ファイルを採点器より先にコミットする運用と git tag に対応する。ただしこの基準は confirmatory な研究を想定している。理由の内訳や事例の分析は exploratory と明示する必要がある。

## related_work.md の 10 の文のうち 2 つが崩れ、2 つは狭めて書き直す

前回の調査（`docs/related_work.md`、2026-10-02/03、73 件）の主張を、今回の結果で一つずつ判定し直した。「崩れた」は、前回の時点では正しかったが、その後に見つかったもので成り立たなくなったという意味である。

| related_work.md の文（行） | 判定 | 理由 |
|---|---|---|
| 「宣言と実装の照合を初めてした」とは言えない（97–98） | **保たれる（さらに強まる）** | HintLint・mcp-doctor に加え、reachscan・mcpscan-cli MCP013・MCPSafe MCP-200・M8ven が見つかった |
| 「検出力で勝る」とも言えない（99–100） | **保たれる** | 比較の相手が増えた。reachscan とはまだ比べていない |
| 読んだ論文の中で `ToolAnnotations` の値をコードと照らすものは見つからなかった（104–105） | **保たれる（論文に限る）** | ContractGuard は説明文を読む。全文のキーワードを数えた 30 本あまりでヒットは 2 本だけで、どちらも宣言だけを測る |
| D4（`idempotentHint`）を照らす道具は論文・道具とも見つからなかった（105–106） | **保たれる** | reachscan は検査しない。mcpscan-cli はキーの有無だけを見る。MCPSafe は 2 ヒントだけ |
| Python で呼び出し先へ降りながら宣言と照らす静的な道具は見つからなかった。訂正後の「Python の MCP サーバについて…AuthGap のほかに見つからなかった」も同じ（107–108、219–223） | **崩れた** | reachscan v0.3.0（2026-10-05）がこれをする。前回の調査の 2〜3 日後のこと |
| 実効の側で決められなかったものの率を出した仕事は見つからなかった（109–114） | **保たれるが、狭めて書く** | reachscan の `unknown` は件数だけ。Scan the Skill は失敗の件数を併記する。Monat は全数を alarm にする。Jelly（JS）は解決率を指標にする。規範は soundiness manifesto にある |
| 解析器の凍結や事前登録の記載は見つからなかった（115–117） | **崩れた（新規性の根拠としては）** | FCD（preregistered・frozen）、Approval Laundering（パーサの凍結と事前指定の holdout）、AgentSecGraph（解析器の凍結）。どれも ToolAnnotations とは照らさないので、組み合わせとしては保たれる |
| 向き: 強制されない宣言で「狭すぎる」側を数える（118–120） | **弱まった** | SkillScanner（99/126）と BIV（過小申告 135,187 件）が、別の宣言で同じ向きを測っている。副作用ヒントと MCP に限れば保たれる |
| 呼び出し先を追うこと自体は新しくない（224–227） | **保たれる（強まる）** | ContractGuard（DFS）、PrivLess（call graph）、reachscan（8 hop） |
| R1 の差分は「解決できなかったものをどう扱うか」に尽きる（24–27） | **保たれ、reachscan にも当てはまる** | reachscan の `unknown` は不一致を作らない |

今回の検索で崩れなかったものを、新しいと言える主張として並べ直すと次のとおりである。

| まだ新しいと言えること | 根拠（見つからなかった範囲） | 書くときの注意 |
|---|---|---|
| 9 つの軸の組み合わせ全体 | 7 本のノートすべて | 部品ごとに先例を引いたうえで、「束ねた」と書く |
| ToolAnnotations の値をコードと照らした**論文** | arXiv API、30 本あまりの全文、2026 年の会議の題目 | 道具が先にあることを併記する。census の一文を引く |
| `idempotentHint` の照合 | 上の 4 行目、Flux、gRPC | D79 の 352 件のうち D4 は 78 件 |
| **注釈の修正コミット**を再現率の正解にする | 方法論の先例 9 件は、どれもバグか脆弱性の修正 | 再現率の手法そのものは標準だと書く。Gao と Khan では研究者が宣言を足したが、AuthGap では開発者が宣言を直した、という向きの違いを書く |
| Python で、効果の単位の `opaque(reason)` 率を主結果にする | Python の呼び出しグラフ研究は precision/recall か、定性的な列挙だけ | soundiness への準拠として書く |
| 同じ解析器の中での深さ 0 のアブレーション | 明示的な先例は無い | 別のツールどうしの比較とは違うと書く |
| 宣言の変化がコードの変化に裏づけられているか（r_prev） | mcpindex と mcp-tool-drift は宣言どうしの差分だけ | — |
| 強制されない**副作用ヒント**の過小申告を、MCP の母集団で測る | PrivLess の Pass 1 が示すとおり、強制される系統では構造上測れない | SkillScanner と BIV の先例を併記する |

逆に、もう新しいとは書けないものがある。宣言と実装の照合そのもの、Python で宣言を読んで呼び出し先まで追う静的な検査、「safe と宣言した入口から書き込み sink に届くか」を見る仕組み（CodeQL がある）、入口から手続き間でたどって宣言と実装の食い違いを母集団で測る骨格（ContractGuard と DCIChecker）、凍結や事前登録を単体でしていること、三値目、修正コミット由来の再現率、単独の評定と test-retest、そして領域を問わない「強制されない宣言の過小申告」である。CLAUDE.md が「領域固有の貢献の中心」とする 14 の入口規則（`ENTRY_RULES`）にも注意が要る。入口の規則を持つこと自体には、すでに並ぶものがある。MCPacific の 56 パターン、ContractGuard の入口の一覧（低水準の `list_tools/call_tool` を含む）、reachscan の低水準ハンドラの結びつけ、それに FastMCP と低水準の `Tool` を読む hintgap（[hintgap](https://github.com/jay-tank/hintgap)、○）である。したがって貢献は、「入口規則が効果の推定と opaque の会計につながること」と書く必要がある。MCP-BiFlow が手で調べた Python 100 件のうち 32 件が「その他 / 混在」の登録だったこと（前回の調査、著者の主張）は、規則を多く持つ必要を外から裏づける数字として引ける。

ノート 01 は、mcp Python SDK 2.x が snake_case の `read_only_hint` を使うため false-clean を招くかもしれない、というリスクを挙げていた。**これは既に扱われており、未解決のリスクではない。** `authgap/entries.py` の 2657〜2724 行（D64 / U38）が、`read_only_hint` / `destructive_hint` / `idempotent_hint` / `open_world_hint` を camelCase に写している。写し方は mcp の主版で条件づけてあり、2.0 以上なら宣言、2.0 未満なら malformed、決まらなければ D_unknown とする。ただし比べる側の道具にはこの扱いが無いことがある。mcpscan-cli の `ANNOTATION_KEY` は camelCase の 4 語しか見ないので、SDK 2.x のサーバの宣言を「注釈なし」として読むはずである（コードからの推論で、動かしてはいない）。道具を比べるときは、この差を限界に書く。

## 10 月下旬に CSS2026 と ICSE 2027 の結果を読み直す

追うべきものは 13 件ある。日付で決まるもの（CSS2026、ICSE 2027、CCS 2026、S&P・NDSS 2027）、到達できなかった情報源、未読の細部の 3 種類に分かれる。

| 何を | いつ・どこで | なぜ |
|---|---|---|
| CSS2026 2D1-1 浦川・中村（東京都市大）「安全なMCPレジストリのための検証フレームワークの提案と実証評価」 | 開催（2026-10-19〜23）の後、IPSJ 電子図書館の CSS2026 論文集 | 題だけで A1〜A8 がすべて不明。登録時の検証なら、AuthGap と同じインストール前の検査になりうる |
| ICSE 2027 の採択一覧 | 通知 2026-10-20 以降（[ICSE 2027](https://conf.researchr.org/track/icse-2027/icse-2027-research-track)） | 投稿は 1 サイクル。MCP の宣言照合が載る可能性がある |
| CCS 2026 本会議と ContractGuard の成果物 | 2026-11-15〜19、github.com/psu-security-universe/contractguard | 深さの上限、未解決率、Python の割合を確かめていない |
| reachscan の新しい版 | 随時（10-04〜10-07 に 3 版が出た） | TS への対応や `unknown` の扱いが変わりうる。phase-3 corpus の一覧は非公開 |
| 山崎・戸田・森の本文 | 研究会の会員限定。図書館経由で取得する | A4・A5・A7 が不明。国内の先行研究として必ず引く |
| S&P 2027・NDSS 2027 の採択一覧 | 未掲載（[S&P 2027](https://sp2027.ieee-security.org/accepted-papers.html)、[NDSS 2027](https://www.ndss-symposium.org/ndss2027/)） | — |
| RAID・ESORICS・AsiaCCS・EuroS&P 2026 の採択一覧 | 到達できなかった（404 / 403 / timeout） | — |
| DBLP・Semantic Scholar・Google Scholar・ACM DL・IEEE Xplore | HTTP 429、bot 判定、403、または未実施 | 引用網をたどれていない |
| 「508 サーバ・612 件」の出典 | bex.co の著者に問い合わせる。Medium の「500 Server Scans」の記事（403）を別の経路で読む | 出典が分かるまで引用しない |
| SEP-2793（declared-vs-inferred の risk metadata、walbis/modelcontextprotocol の fork） | 未読 | reachscan が従う枠組み。仕様の側に測定データがあるか分からない |
| OpenAI Apps の automated review の手法 | 公開情報なし | 中身の見えない競合として書く |
| 修士論文の題目（早大 森研、東京都市大 中村研、東京科学大 鄭研、横国大 吉岡研） | 2027 年 2〜3 月 | 同じ主題の学位論文が出うる |
| 細部（BIV の付録 G、AgentSecGraph の補遺、EPScan の本文、S&P 2026 の Cosseter、hintgap の作成日、M8ven の採点方式） | — | 深さ・入口規則・方式の比較に要る |

## 検索は 7 方向に広いが、学術データベースの横断は塞がれていた

7 本のノートは、それぞれ次の範囲を受け持った。(01) MCP の注釈とコードの照合、それに他のプロトコルの同等のヒント。(02) MCP とエージェントのツールの静的解析。(03) スキル、アプリストア、音声アシスタント、ブラウザ拡張、ミニプログラム、IDE 拡張、プライバシーラベル。(04) 一般ソフトウェアで宣言された副作用・権限・安全性。(05) 方法論の先例。(06) 国内の会議、2026 年の国際会議のプログラム、学位論文、グレー文献。(07) 「612 件」の出典と、mcpscan-cli・reachscan の追跡。手段としては、arXiv API の検索を数十回（新しい順）、全文 HTML の注釈語の計数を 30 本あまり、Web 検索をノートの記録で 140 回を超えて行った。公式プログラムは、CSS2026（356 題）・CSS2025・SCIS2026・情処全国大会・FIT2026・JSSST2026・IEICE 技報、USENIX Security 2026（377 題）・S&P 2026・NDSS 2026・CCS 2026・ACSAC 2026・ICSE 2026（673 題）・FSE 2026・ISSTA 2026・ASE 2026・MSR 2026・SANER 2026 を見た。国内の検索は IPSJ 電子図書館・J-STAGE・CiNii で行い、OpenReview は ICLR 2027 の枠を見た。コードを読んだのは mcpscan・reachscan・EPScan の 3 つである。前回の 73 件は調べ直さず、版が変わったかだけを確かめた。

限界ははっきりしている。Semantic Scholar の API はすべて HTTP 429 で、DBLP は bot 判定のページを返した。ACM DL と IEEE Xplore は 403 か本文なしだった。このため引用網はたどれていない。Google Scholar、OpenReview の ICLR 2027 以外の枠、PyPI と npm の全文、ベンダーのブログの個別検索、中国語圏の文献、modelcontextprotocol org の issue の網羅は実施していない。arXiv API は題名と要旨しか見ないので、本文だけで注釈に触れる論文は、全文を取った 30 本あまりの外では漏れうる。GitHub やブログからの引用の一部は、要約モデルを通した WebFetch の出力で、原文と一字一句は照合していない（ノート 01・07）。会議のカメラレディ版と arXiv 版の違いも確かめていない。したがって、この報告書の「見つからなかった」は、すべて「この手順では見つからなかった」と読むこと。

## 結論

この 1 週間で起きたことは、**検査が道具として安くなった**ということである。reachscan は注釈の抽出から照合までを 2 日のうちに入れ、mcpscan-cli は 40 行の正規表現の窓で同じ問いに答え、MCPSafe も同じ規則を持つ。M8ven も、方式は非公開ながら注釈を検査している。こうなると、論文の価値は検査の定義ではなく、測定の設計に移る。何件の宣言が反しているか。そのうちどれだけが決められないか。その数字が、データを見る前に決めた手続きで出たものか。reachscan 自身の履歴が、この点をよく示している。corpus を見た後で EXECUTE を destructive から外し、openWorld を medium に下げた。その結果の「16 件」は、凍結しなかった測定がどう揺れるかの生きた例であり、AuthGap の凍結と事前登録の意味を説明する材料になる。

審査で最も問われやすいのは、ContractGuard との対比だろう。「なぜ自然言語の宣言と LLM で解かないのか」という問いである。答えは三つの外部の材料で組み立てられる。ContractGuard 自身が書いた「errors in both directions」、CPI が示した LLM 系スキャナの抑え込まれやすさ、そして構造化ヒントが機械可読な真偽値で、NLP の誤差が入らないことである。もう一つの脅威である reachscan は、同じ 352 件と同じ depth_probe で走らせれば比較に変えられる。ただしそれは、D80 と同じく走らせる前に決定として書いたときに限る。
