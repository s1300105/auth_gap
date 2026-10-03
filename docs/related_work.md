# 先行研究（読んだ結果）

**この文書の規則。**

1. **一次資料（論文本体 / リポジトリ本体）を読んだ項目だけ「確認済み」と書く。**
   検索結果の要約や二次情報から書いた項目は **未検証** と明示する（CLAUDE.md 規則 1）。
2. **PDF 本体は repo に入れない。** 公開リポジトリなので著作物を配布することになる。
   置き場は `papers/`（`.gitignore` 済み）で、コミットするのはこの文書だけ。
3. 各項目に **出所**（どの節を読んだか）を書く。後から確認できるようにする。
4. **重なりは正直に書く。** 「うちの方が優れている」ではなく「何が同じで何が違うか」。

未記入の欄は `（未記入）` のまま残す。**埋まっていない欄を推測で埋めない。**

---

## 結論（2026-09-22、R1 / R2 / R3 とも一次資料を読んだ）

| # | 研究 | 主軸（宣言 D と実効 M の照合）と競合するか |
|---|---|---|
| R1 | HintLint | **最も近い。ただし問いが違う。** 向こうは主に「宣言が**無い**」を数え（65 件中 61 件）、こちらは「宣言が**あって反する**」を数える。**検出力で勝ったとは言えない**（比較可能な 4 件で 2 勝 2 敗。初回は 1 勝 3 敗で、**負けの 1 件が AuthGap の誤 clear だったので直した** — D43） |
| R2 | AgentFlow | **しない。相補的。** 解析対象が違う（下記） |
| R3 | ReactAppScan | しない。**手法の型として引ける** |

**R1 の差分は「解決できなかったものをどう扱うか」に尽きる。** HintLint の確度の語彙は
`source-backed` / `needs-review` の 2 語で、**未解決を表す語が無い**。正規表現に当たらなければ
分母からも消えるので、「宣言がどれだけ当てにならないか」という**率の問い**には答えられない。
AuthGap は `opaque(reason)` 8 語と `truncations` / `budget_skipped` で残し、率を報告する。

**R2 は当初「グラフ化案と競合する」と見ていたが、一次資料を読んで**相補的**だと分かった。**
AgentFlow が解析するのは**エージェント プログラム（MCP を使う側）**で、MCP サーバの実装は
読まない。しかも論文の限界節が「ツール実装やライブラリ呼び出しの内部を推論する仕事には
ADG は使えず、points-to 解析と組み合わせる必要がある」と自ら書いている。**そこが AuthGap の
守備範囲である。**

**O19 の判断は (a)「測定研究として立て直す」である**（2026-09-22、D40）。(c) ではない:
R1 が同じ現象を先に触っているので「初めて照合した」とは書けない。書けるのは
**母集団の定義・事前登録・未解決の率の報告**であり、それは (a) の内容そのものである。

---

## 2026-10-02 の調査 — 似た研究を 4 つの方向から読み直した

**元データ**: `evidence/related_work_20261002/`（`P1_mcp_declared_vs_actual.json` 15 件、`P2_mcp_static_analysis.json`
25 件、`T1_tools.json` 16 件、`D1_other_domains.json` 17 件）。各件に、比べる軸（何を解析するか・何と何を比べるか・
手法・呼び出し先を追うか・決められないものの扱い・評価の母集団と正解の付け方・凍結や事前登録）と、裏づけの引用を
付けた。引用は 4 つの担当がそれぞれ `scripts/verify_quote.py` で一次資料（論文の本文、commit を固定したソース）と
照らし合わせた。**最も近いもの（下の表の行）の引用 126 個は、本記録者が別のキャッシュで照らし合わせ直し、
126 個とも exact だった**（`recheck_by_recorder.json`）。論文の数値はすべて著者の主張で、本記録者は再現していない
（`verified_by_me = none`。CLAUDE.md 規則 1）。

### 一言で言うと

**「MCP の宣言（ToolAnnotations）の値を、サーバのコードの効果と照らし合わせ、矛盾の率を人の判定つきで測った
論文」は、調べた範囲では見つからなかった**（「無い」ではなく「見つからなかった」。arXiv の検索は題名と要旨しか
見ないので、本文だけで注釈を扱う論文は漏れうる）。近い仕事は 3 つの型に分かれ、どれも AuthGap と 1 点以上で違う。

1. **問いは同じだが、宣言が違う**: DCIChecker・MCPDiFF・SkillScope・SkillConsist は「**自然文の説明**」と
   コードを比べる。構造化された真偽の宣言（`readOnlyHint` など）は読まない。
2. **宣言は同じだが、解析が浅い・論文ではない**: HintLint・mcp-doctor は宣言とソースを比べるが、Python では
   呼び出し先を追わない。actlint などは名前・説明文としか比べない。
3. **解析は近いが、問いが違う**: MCP-BiFlow・VIPER-MCP は MCP サーバを手続き間で解析するが、目的は脆弱性で、
   宣言を読まない。

### 最も近いもの — 何が同じで、何が違うか

| 仕事 | 種別 | 比べるもの | 呼び出し先 | 決められないもの | 評価 | AuthGap との関係 |
|---|---|---|---|---|---|---|
| **DCIChecker**（arXiv 2606.04769v1） | 論文（preprint） | **説明文**（名前・入力スキーマ・説明）とコード。分類に「Undeclared Side Effects」（状態の変更など） | AST で 4 つの登録の型から入口を見つけ、プロジェクト内を深さ 3 まで追う。外部ライブラリには入らず、json などは許可リストで刈る | **出力は一致 / 不一致だけ**。Direct と Reverse が割れると LLM（Claude Sonnet 4.5、温度 0）が仲裁する（実データで 38.25%）。動的な値は `[Dynamic Expression]` に置き換える。説明の無い 2,170 ツールは分母から外す | Python 2,214 サーバ。正解は予測で 200 / 200 に層別した 400 組を著者 2 人が独立に付け、第 3 の研究者が裁定。精度 96.00%・再現率 97.46%（層別した標本の上の値で、母集団の再現率ではない＝本記録者の読み） | **競合（宣言が違う）**。本文に `readOnlyHint`・`destructiveHint`・`annotation`・`ToolAnnotations` の語は 0 回（本記録者が同じページで陽性対照「Undeclared Side Effects」が exact になることも確かめた）。成果物の公開先は見つからなかった |
| **HintLint**（`complira/hintlint` 5a51f2a4、R1 と同じ commit。2026-10-02 も HEAD は同じ） | OSS ＋自己発表の報告書（`docs/Report_HintLint.pdf` 9 ページ。査読なし） | **宣言（D1〜D3）**とソース。D4 は読むが比べない | Python は行の正規表現で `@tool` を見つけ、本体を次の `def` で切る。**呼び出しを追わない**。TS / JS は同じファイルと相対 import の中で深さ 4 まで名前で追い、解決できない呼び出しは記録なしで飛ばす | ツール単位では `unknown_handler`・`metadata_only`・`unsupported_pattern` がある。**解決したハンドラの中の、解決できない効果・呼び出しを表す語は無い**。Python のハンドラは常に `"resolved"` | 星の数と登録所への掲載で選んだ 20 リポジトリ（「無作為ではない」と自分で書く）。報告書は「**この検証済みのパイロットでは、誤った宣言の値は 1 件も確かめられていない**」と書き、`readOnlyHint` の誤りの候補 2 件はどちらも誤検出だった | **競合（同じ問い、最も近い）**。違いは、呼び出し先を追うか・未解決の効果を残すか・母集団と人の判定で率を測るか |
| **mcp-doctor**（PyPI `mcp-server-lint` 0.12.13） | OSS | D1 だけ。ツール関数を `ast.unparse` で文字列に戻し、4 つの正規表現を当てる | この検査では追わない | 語彙なし | なし | 競合（狭い） |
| **OpenAI の申請用 skill** | 手順書（LLM への指示） | D1〜D3 と実装（呼び出し先を含む）を、開発者の手元の LLM に読ませる | LLM 任せ | 書かれていない | なし | 競合（規則も評価も無い） |
| **actlint / Airlock** | OSS | actlint は**名前・説明・スキーマ**からの推定と宣言、Airlock は**実行して観察**した効果と D1 | actlint はコードを読まない。Airlock は同梱の試験用サーバでしか観察できない | **両方とも未解決の語彙を持つ**（actlint `unassessed`、Airlock `not_tested`・`capability_absent` など） | 開発元の自己申告 | 相補（層が違う） |
| **MCP-BiFlow**（arXiv 2605.07836） | 論文 | 宣言とは比べない（脆弱性の双方向 taint） | 登録 10 種・振り分け 16 種の型で Python / JS / TS のツールの入口を復元し、手続き間で追う。LLM が裁定 | 未解決の語彙は見つからなかった。精度は「推定していない」と著者が書く | — | **手法が最も近い**。手で調べた Python 100 件のうち 32 件が「その他 / 混在」の登録で、入口の規則を多く持つ必要の外部の裏づけになる |
| **VIPER-MCP**（arXiv 2605.21392） | 論文 | 宣言とは比べない（CodeQL ＋ MCP 用の QL で taint、LLM と実行時のフックで実証） | CodeQL の手続き間 | 未解決の語彙は見つからなかった | 偽陰性の評価に使った 130 件のうち 67 件は自分の発見 | 手法の型。**特権の操作が目的のツールは脆弱とみなさず外す**ので、「`readOnlyHint: true` なのに書く」はそもそも対象外 |
| **SkillScope**（arXiv 2605.12875） | 論文 | エージェントの skill の**説明文（SKILL.md）**とコード（Joern の CPG ＋ LLM） | CPG の上で追う | `uncertain` を返す枠はあるが、**その率の報告は見つからなかった** | 4,556 件、不整合 9.4%、精度 84.8%・再現率 96.5% | 先例（隣の領域でほぼ同じ問い） |
| **SkillConsist**（arXiv 2608.07639） | 論文 | skill の説明とコード | — | Supported / Contradicted / **Unknown** の 3 状態で形式化。ただし**評価では Unknown を「所見なし」として陰性に潰す** | 633 件のベンチマークでの検出性能（母集団の率ではない） | 先例（判定の形が最も近い） |
| **Stowaway**（Felt ら、CCS 2011） | 論文 | Android の manifest の権限の宣言と、静的に求めた API の使用 | 静的 | **解決できない reflection を持つアプリを別の群にして数を出した**（900 中 105 件＝12%） | 偽陽性 7% は手で確かめた。偽陰性は測っていないと明記 | 先例。ただし Android は権限を**強制する**ので、矛盾は「宣言が広すぎる」側にしか出ない。AuthGap は強制されない宣言で、「宣言が狭すぎる」（危険な）側を数える |
| **PoliCheck**（Andow ら、USENIX Security 2020） | 論文 | プライバシーポリシーと、実際のデータの流れ | 動的な観測 | 宣言の側のあいまいさを ambiguous という別の類で数える（7.6%）。**実効の側で決められない流れは捨てる**。精度の評価から ambiguous と、判定者が迷った 27 件を外す | 人の判定 | 先例（一貫性のモデル） |
| **Checker Framework の Purity Checker** | 公式マニュアル | `@Pure`・`@SideEffectFree` の注記とコード | — | **既定では注記を信じて検査しない**。理由は偽陽性の多さ | — | 先例。「注記を信じる」状況が MCP のクライアントと同じ構造 |

ほかに読んだもの（詳細は元データ）: MCPDiFF（README とコードをサーバ単位で埋め込みの類似度で比べる。人の正解なし）、
説明文の smell の論文（2602.18914）、ToolGuardian（説明文とモック実行の効果の食い違いをポリシーに渡す。合成 16 ツール）、
AgentBound（FSE 2026。LLM がコードから権限の宣言を**新しく作って**強制する。既存の宣言の正しさは測らない）、
SandScope（2601.01241。能力のラベルと観測した外向き通信を 4 区分で数え、「観測が無いことは不在の証拠ではない」と明記）、
Agent Audit（デコレータ 12 型で入口を見つけるが手続き内だけ）、MCPZoo（既存のスキャナの警告の真陽性は 50% 未満と報告）、
宣言を数えた測定の論文 5 本（2609.10962・2609.15397・2607.07461・2601.08012・2606.06387。どれもコードとは照らさない）、
Cisco mcp-scanner（呼び出し先を 3 段まで追うが、比べるのは docstring と説明で、注釈の名前はテスト以外に 0 回。
指示文は「Uncertainty = No Flag」）、PScout、Lalaine・Koch ら・Arkalakis ら・ExtPrivA（ストアの自己申告と挙動。どれも
動的で、試せなかった単位は分母から外すか下限で書く）、Sălcianu と Rinard・JPure（純粋性の解析。外部のコードは保守的に
不純とみなす）、Respector（ICSE 2024。コードから仕様を作り OpenAPI と突き合わせる）、HTTP の意味の検査（2608.16239）、
GPT Actions の測定（IMC 2025。仕様とポリシーの照合で、`x-openai-isConsequential` もコードも扱わない）。

### AuthGap が言えること・言えないこと（本記録者の読み。O19 の判断 (a) と同じ向き）

**言えないこと**

- 「宣言と実装の照合を初めてした」とは言えない。HintLint と mcp-doctor が先にある（宣言とソース）。説明文とコードの
  照合なら DCIChecker・MCPDiFF・SkillScope が先にある。
- 「検出力で勝る」とも言えない。HintLint とは比べられた事例が 4 件しかなく（R1 の (2)）、DCIChecker とは宣言が違うので
  並べられる数が無い。

**言えそうなこと**（論文に書く前に、上の表の原文を学生が自分で開いて確かめること）

1. **宣言の種類**: 構造化された 4 つの宣言（D1〜D4）を、ツール単位でコードの効果と照らし合わせる。読んだ論文の中で
   `ToolAnnotations` の値をコードと照らすものは見つからなかった。D4（`idempotentHint`）をコードや挙動と照らす道具は、
   論文・道具とも見つからなかった。
2. **深さと宣言の組**: Python で呼び出し先へ降りながら宣言と照らす静的な道具は見つからなかった（HintLint の Python と
   mcp-doctor は追わない。DCIChecker は追うが宣言を読まない）。
3. **決められないものを数える**: 近い仕事は、決められないものを ① 出力に持たない（DCIChecker・mcp-doctor）、
   ② 持つが評価で陰性に潰す（SkillConsist）、③ 持つが率を出さない（SkillScope）、④ 分母から捨てる（PoliCheck の
   実効の側、ストアの測定）のどれかだった。報告の主な結果として決められない単位の率を出したのは、読んだ中では
   Stowaway（解決できない reflection の群、12%）と PoliCheck（ただし**宣言の側**のあいまいさ ambiguous、7.6%）だけだった。
   実効の側（コードの側）で決められなかったものの率を出した仕事は見つからなかった。AuthGap の `opaque(reason)` と
   未決の率の報告は、この点で違うと言える。ただし読んだ範囲（4 つの元データの計 73 件。重なりあり）での話である。
4. **測定の作法**: 読んだ範囲のどれにも、解析器の凍結や事前登録の記載は見つからなかった。母集団を前もって決め、
   SHA を固定し、人が 1 件ずつ判定する点は、DCIChecker（既存のデータセットを使い、予測で層別した 400 組に正解を付ける）
   とも違う。
5. **向き**: Android の権限の研究は「宣言が広すぎる」を数える（宣言が強制されるため）。AuthGap は強制されない宣言で
   「宣言が狭すぎる」（利用者に確認を省かせる危険な側）を数える。付録 G で集めたクライアントの使われ方
   （`docs/textbook/appendix-g.md` 3.9 節）が、この向きの意味を裏づける。

### 次にすること（決定待ちではなく作業）

- **DCIChecker と同じサーバで AuthGap を走らせて重なりを見る**ことはできない（DCIChecker の成果物もデータの
  一覧も見つからなかった）。比較は手法と問いの水準でしか書けない。限界節に書く。
- MCP-BiFlow の 32 / 100（登録の型が「その他 / 混在」）は、AuthGap の入口の規則の必要を示す外部の数字として本文に
  引ける（著者の主張。本記録者は再現していない）。

### 呼び出し先を追うか — 本記録者が自分で確かめた（2026-10-03）

学生の問い「本当にほかの研究は関数の本体しか見ていないのか」に答えるため、担当の報告を使わずに確かめた。
道具はソースを読んだうえで実際に動かし、論文は呼び出しの扱いを書いた原文を `scripts/verify_quote.py` で照らし合わせ
直した（`recheck_interprocedural.json`、64 個のうち 63 個が exact / loose。JPure の 1 個は取得の失敗）。

**結論: 本体しか見ないのは、宣言を読む道具のうち HintLint の Python の経路と mcp-doctor だけだった。論文の多くは
呼び出し先を追う。** ただし、追う論文はどれも宣言（ToolAnnotations）を読まない。

#### 動かして確かめた（`evidence/related_work_20261002/depth_probe/`）

`server.py` に `readOnlyHint=True` のツールを 3 つ置いた: 本体で `open(destination, "w")` する `body_write`、
同じ書き込みを補助関数 `_save` に任せる `helper_write`、`os.remove` と `subprocess.run(["rm", "-rf", ...])` を補助関数
`_purge` に任せる `helper_purge`（`destructiveHint=False` も宣言）。

| 道具（版） | `body_write`（0 段） | `helper_write`（1 段） | `helper_purge`（1 段） |
|---|---|---|---|
| HintLint（5a51f2a4、Python） | 指摘（`false_readonly`） | **指摘なし**。`_save` の書き込みは「プロジェクト単位」の証拠として見つかるが、どのツールにも結びつかない | **指摘なし**（`subprocess` はプロジェクト単位の証拠、`os.remove` は規則に無く見つからない） |
| HintLint（同、TypeScript の同じ形 `server.ts`） | — | **指摘**（`typescript-local-callgraph`、道すじ `helper_write → save`、深さ 1） | — |
| mcp-doctor（HEAD 4def567、2026-10-02） | 指摘（`annotation_mismatch`、「own body contains ...」） | **指摘なし** | **指摘なし** |

ソースの上の理由:

- HintLint: Python のツールの範囲は、デコレータから次の `def` までの行（`src/extractors/python.js` 63〜73 行）。範囲の外
  の証拠をツールに結びつけ直す `reachableEvidenceByTool` は、`typescript` / `javascript` 以外を飛ばす
  （`src/evidence/typescript-reachability.js` 346 行）。外部の解析器（CodeQL・Semgrep・Bandit）の結果の取り込みも、
  報告の行がツールの範囲の中にあるときだけツールに結びつける（`src/evidence/tool-location.js`、
  `src/evidence/sarif-normalizer.js` 57〜62 行。データの流れの道すじ `trace` は保存するが、結びつけには使わない）。
  なお CLI に配線されている外部の解析器は Semgrep だけ（`src/cli.js`）。
- mcp-doctor: `_scan_for_mutation_signal(fn)` が `ast.unparse(fn)` に正規表現を当てる（`mcp_doctor/analyzer.py` 856〜871 行）。
  同じファイルに補助関数を 5 段までたどる仕組みがあるが、例外処理の有無の検査にしか使わない（918〜922 行）。

#### 論文と道具の一覧（原文で確かめた範囲）

| 仕事 | 呼び出し先を追うか | 宣言（ToolAnnotations）を読むか |
|---|---|---|
| DCIChecker | **追う**。プロジェクト内を深さ k=3 まで（「we recursively follow intra-project calls up to depth k」「we set the depth k=3」）。外部ライブラリと許可リストで止める | 読まない（説明文と比べる） |
| MCPDiFF | **追う**。入口から呼び出しグラフを深さ優先でたどる（入口は MCP のツール登録ではなく、呼ばれない関数） | 読まない |
| VIPER-MCP | **追う**（「inter-procedural taint propagation」。CodeQL） | 読まない |
| MCP-BiFlow | **追う**（呼び出しグラフの上の双方向の手続き間 taint） | 読まない |
| MICRYSCOPE（暗号の誤用） | **追う**（大域の手続き間 Def–Use グラフ） | 読まない |
| Cisco mcp-scanner | **追う**。ファイルをまたいで最大 3 段 | 読まない（docstring と比べる） |
| SkillScope | **追う**。Joern の CPG からファイルをまたぐ辺を補ってグラフを作る（単位は skill 全体） | 読まない（SKILL.md と比べる） |
| Stowaway | **追う**。手続き内の解析に深さ 2 の手続き間解析を足す | （Android の権限の宣言を読む） |
| OpenAI の申請用 skill | **追うよう LLM に指示**（「inspect enough of that path」）。深さの決まり無し | 読む（D1〜D3） |
| HintLint | TypeScript / JavaScript は**追う**（深さ 4、同じファイルと相対 import の中だけ）。**Python は追わない** | 読む（D1〜D3） |
| mcp-doctor | **追わない** | 読む（D1 だけ） |
| Agent Audit | **追わない**（「inter-procedural data flow across function boundaries is not tracked」） | 読まない |
| mcp-sec-audit・名前や説明だけを見る道具（actlint・Tool Card Linter・toolfence など） | 追わない／コードを読まない | 読む（名前・説明と比べる）ものがある |
| SkillConsist | 本文に呼び出しをたどる記述は見つからなかった（不明） | 読まない |

#### 追う研究は、追った先で何をしているか（2026-10-03、本記録者が本文を読んだ）

「呼び出し先を追う」は同じでも、**追う目的が AuthGap と違う**。読んだ本文から（どれも arXiv の HTML / PDF の本文、
Cisco はソースの `docs/behavioral-scanning.md` と `mcpscanner/data/prompts/code_alignment_threat_analysis_prompt.md`、
f817899）:

| 仕事 | 追う目的 | 追った先で見るもの | 結論を出すのは |
|---|---|---|---|
| DCIChecker | 説明文と比べる材料を集める | 入口の関数・深さ 3 までの補助関数のコードと、危ない API の呼び出し（引数を解決できれば値も）を 1 つの束にまとめる | LLM（説明文と束を読み、分類の 7 つの下位類型で判定） |
| MCPDiFF | README と比べる材料を集める | 呼ばれない関数を入口とみなし、呼び出しの鎖ごとに LLM が機能を要約する | 埋め込みの類似度（README の機能をコードの機能がどれだけ覆うか） |
| VIPER-MCP | **攻撃者の入力が危ない操作に届くか**（taint） | ツールの引数（攻撃者が操れる値）が、コマンド実行・外向きの要求・ファイルのパスに、無害化されずに届く道 | CodeQL の警告を、LLM が作った攻撃の文と実行時のフックで実証 |
| MCP-BiFlow | **2 つの向きの危ない流れ**（taint） | ① 引数 → 危ない操作（コマンド・ファイル・DB・評価・外向き通信）、② 外から取った内容 → ツールの戻り値（モデルに返る） | 規則による解析。攻撃者が操れるか・防ぎが効くかが字面で決まらないときだけ LLM |
| Cisco mcp-scanner | 悪意のある挙動（サプライチェーン攻撃など）を見つける | ツールの引数の流れと、呼び出し先（ファイルをまたいで 3 段）の操作の全部を LLM に渡す（「No predefined "dangerous" operations - reports everything to LLM」） | LLM（docstring と挙動の食い違い・悪意の有無） |
| SkillScope | skill の説明（SKILL.md）に無い危ない挙動 | skill の全ファイルから危ない操作の節点を拾い、データ・制御の流れでつなぐ（入口から追うのではなく、skill のコード全体） | LLM（説明が覆わない操作・流れがあれば不整合） |
| MICRYSCOPE | 暗号の API の誤用 | 手続きをまたぐ Def–Use グラフで、鍵・乱数などの値の出どころ | 誤用の規則 |

**AuthGap との違いが出る点**（本記録者の読み。どの道具にも実際にはかけていない）:

1. **taint の解析（VIPER-MCP・MCP-BiFlow）は「誰の値が届くか」を見る。AuthGap は「その操作が起きうるか」を見る。**
   `readOnlyHint: true` のツールが、決まった場所（例 `~/.cache/history.json`）に検索の履歴を書くとき、パスは攻撃者が
   操れないので taint の解析は脆弱性として出さない。AuthGap にとっては、書き込みが起きうること自体が D1 の矛盾である
   （裏方の書き込みとしての扱いは人の判定、D68）。さらに VIPER-MCP は「特権の操作が目的のツール」（例: シェルを
   実行するツール）を脆弱とみなさないと明記する（II-B の Research scope）。
2. **Cisco は確信が無ければ指摘しない。** 指示文は分類ごとに「Uncertainty = No Flag」と書き、「Normal caching or state
   management is NOT manipulation」と書く。上の履歴の書き込みは、悪意が無いので指摘しない向きになる。なお指示文は
   「Function Metadata - Docstrings, decorators, and type annotations」を LLM に渡すので、`annotations=ToolAnnotations(...)`
   を書いたデコレータの文字は LLM の目に入りうる。ただし宣言と比べよという指示は無い。
3. **説明文と比べる仕事（DCIChecker・SkillScope）は、宣言とずれ方が逆になりうる。** 説明が「ノートを検索し、検索の履歴を
   保存する」と書いていれば、DCIChecker の基準では一致（Eff-SM の定義は「説明が読み取りだけを思わせるのに書く」）。
   同じツールに `readOnlyHint: true` があれば、AuthGap では矛盾。逆に説明が書き込みに触れず、宣言も無ければ、
   DCIChecker は不整合、AuthGap は対象外。
4. **DCIChecker の判定の段。** Direct と Reverse の 2 つの問いは点数で答え、点数 50 を「Ambiguous」と定める（付録の
   Listing 1・2）。しかし仲裁の答えは「Consistent」か「Inconsistent」の 2 つから選ばせる（Listing 3）。点数 50 がどちらの
   答えに変わるかは、本文にも手順（Algorithm 1）にも書かれていない（不明）。また、説明の側があいまいなことは
   「Func-Am」として**不整合の 1 つの類**に数える（決められないもの、としては数えない）。上の表の「出力は一致 / 不一致
   だけ」は最終の答えについて正しいが、この途中の段を書き足す。

#### 前の記述の訂正

- 本記録者が会話の中で「宣言を読み、かつ呼び出し先まで追う、の両方を満たすものは AuthGap のほかに見つからなかった」
  と答えたのは**言い過ぎだった**。HintLint は TypeScript / JavaScript では両方を満たす（上の試験で確かめた）。
  OpenAI の申請用 skill も、LLM への指示としては両方を求める。正しくは「**Python の MCP サーバについて、宣言を読み、
  呼び出し先まで追う静的な解析は、AuthGap のほかに見つからなかった**」。上の節の「言えそうなこと」2 はこの言い方に
  なっている。
- 「呼び出し先を追うこと」自体は新しくない。DCIChecker（深さ 3）・Cisco（深さ 3）・Stowaway（深さ 2）・HintLint の
  TS / JS（深さ 4）など、多くの仕事がしている。AuthGap の違いとして言えるのは、追うことそのものではなく、
  **追った先の効果を宣言（D1〜D4）と照らすこと**と、**追い切れなかったところ（深さ・再帰・解決できない呼び出し）を
  `opaque` として数えること**である。

### R1 の訂正（2026-10-02。元の文は書き換えず、ここに書く）

1. **「HintLint には未解決を表す語彙が無い」は言い過ぎだった。** ツール単位の語彙（`unknown_handler`・`metadata_only`・
   `unsupported_pattern`・L1〜L4 の段、`behavior.confidence = "unknown"`）はある。**無いのは、解決したハンドラの中で
   解決できなかった効果・呼び出しを表す語**である（TS / JS の解決できない呼び出しは `continue` で記録なしに飛ばす。
   `src/evidence/typescript-reachability.js`）。AuthGap との差（率の問いに答えられるか）は変わらないが、論文では
   この粒度で書く。誤りの向き: HintLint を実際より粗く書いていた。
2. **「論文は見つかっていない」**: 査読つきの論文は今も見つからないが、repo の中に自己発表の報告書
   `docs/Report_HintLint.pdf`（9 ページ）がある。R1 では読んでいなかった。

---

## 入手先

| # | 論文 / ツール | URL | 状態 |
|---|---|---|---|
| R1 | HintLint | https://github.com/complira/hintlint | ページのみ読了。**コード未読** |
| R2 | AgentFlow | https://arxiv.org/abs/2607.01640 | **PDF 読了**（学生が提供） |
| R3 | ReactAppScan | https://doi.org/10.1145/3658644.3670331 | **PDF 読了**（学生が提供） |
| 参考 | MCP 公式「Tool Annotations as Risk Vocabulary」 | https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ | 読了 |

この実行環境からは R2 / R3 とも egress proxy で遮断されており、直接は取得できない。

---

## R1. HintLint — MCP の注釈と実装の照合（**主軸と最も近い。ただし問いが違う**）

| 欄 | 内容 |
|---|---|
| 種別 | ツール（GitHub リポジトリ）。**論文は見つかっていない**（repo 内に引用形式・arXiv 番号・`paper` 系ファイルなし） |
| 読んだ範囲 | **ソース本体**（`src/extractors/python.js` 143 行、`src/evidence/static-detector.js` 716 行、`src/coverage.js`、`src/index.js`）+ ページ。`5a51f2a4`（2026-09-11）、JavaScript / Node、8,626 行 |
| 実行 | 母集団 v2 の 87 木すべてで走らせた。`scripts/hintlint_compare.py` → `evidence/hintlint_run1/summary.json` |

### 確認済み（ソースを読んだ）

- 目的は「annotation drift」の検出。宣言（`readOnlyHint` 等）と実装の食い違いを静的に見る。
- 対応言語は TypeScript / JavaScript / Python。検出規則は 6 種
  （`READONLY-001` / `DESTRUCTIVE-001` / `OPEN-WORLD-001` / `FLOW-PROCESS-001` /
  `FLOW-QUERY-001` / `FLOW-FILESYSTEM-001`）。
- **Python 経路は AST ではなく行単位の正規表現である。** `src/extractors/python.js` の
  `startsToolDecorator = /@(?:\w+\.)?tool(?:\s*\(|\s*$)/`。`collectFunctionText` は次の
  `def` か次の `@tool` までの行を集めるので、`_analysis.text` は**そのツール関数の本体だけ**になる。
- **Python 側に到達解析は無い。** `src/evidence/typescript-reachability.js` は存在するが
  `python` の出現が 0 件。**呼び出しをまたがない。**
- sink は `static-detector.js` の **10 個の `SINK_RULES`** を本体テキストに正規表現で当てる。
  `scope: "project"` の規則だけ木全体の行に当て、その場合 `confidence: "needs-review"` を付ける。
- 確度の語彙は `"source-backed"` / `"needs-review"` の 2 語。**解決できなかったものを表す語は無い。**
- `handlers_resolved` は「デコレータからハンドラの本体を取り出せたか」の数であって、
  値や効果が解決できたかではない（`src/index.js:41`, `tool.handler?.confidence === "resolved"`）。

### 未検証（ページの記載を写しただけ。CLAUDE.md 規則 1）

- 20 リポジトリ 1,160 ツールで 23 件、精度 82%（2026 年 7 月の findings report とある）。
- handler resolution rate が TS/JS 88%、Python 100%。

### 実測 — 母集団 v2 の 87 木で両方を走らせた

再現: `.venv/bin/python scripts/hintlint_compare.py --hintlint <clone> --label run2 --authgap-scan evidence/scan_v2_run5`
（初回は run1 / `scan_v2_run4`。**HintLint 側の数値は 2 回とも同一**で、動いたのは AuthGap 側だけ）

| | HintLint | AuthGap（`evidence/scan_v2_run4`） |
|---|---|---|
| 入口 | ツール 13,083（`coverage_status`: supported 81 木 / unsupported_pattern 4 / not_mcp_server 2） | ユニット 2,231 |
| 実行 | `evidence/hintlint_run2`（`5a51f2a4`） | `evidence/scan_v2_run5`（`229f5a29`） |
| 検出 | finding 81（うち readOnly / destructive の **65**） | CONTRADICTION **85**（ユニット × (site, kind)、run5） |
| 木の重なり | **両方に出た木 2、HintLint だけ 5、AuthGap だけ 14** | |

**入口を揃えた比較ではない**（HintLint は自分でツールを抽出するので、同じ入口集合を渡す
手段が無い）。したがって件数の大小は比較にならない。**見るべきは「何が見えて何が見えないか」。**

#### (1) そもそも問いが違う — 65 件のうち 61 件は「宣言が無い」ツール

HintLint の `DESTRUCTIVE-001` は **`destructiveHint` が**無い**ツールに対して発火する**。
実測で、比較可能な 65 件の `declared_annotations` は:

| 宣言 | 件数 |
|---|---|
| `{}`（**宣言なし**） | **61** |
| 宣言あり（AuthGap の CONTRADICTION と同じ問い） | **4** |

AuthGap の CONTRADICTION は**明示の宣言 D があってそれに反する**ことを要求する
（宣言の無いツールは INVENTORY 側の問い）。**したがって 61 件は同じ現象を数えていない。**
**真に比較できるのは 4 件だけである。**

#### (2) その 4 件の突き合わせ（AuthGap は **2 勝 2 敗**）

**2026-09-22 更新（run5、解析器 `229f5a29`）。** 初回の突き合わせ（run4）は **1 勝 3 敗**で、
負けの 1 件が AuthGap の誤 clear だった。**それを直した**（D43）ので 2 勝 2 敗になった。
**この表は「HintLint との突き合わせが AuthGap のバグを 1 件見つけた」という記録でもある。**

| 木 / ツール | HintLint | AuthGap（run4） | AuthGap（run5） | 差の原因（一次確認した） |
|---|---|---|---|---|
| `dddabtc/winremote-mcp` / `PlaySound` | DESTRUCTIVE-001（`subprocess.run(` 1 件） | **CONTRADICTION** | **CONTRADICTION** | **一致。**AuthGap は 4 効果（`open` / `subprocess.run` ×2 / `os.unlink`）を出しており、向こうは 1 件 |
| `rwheeler007/cohort` / `internal_web_fetch` | READONLY-001（`mkdir(`） | 効果 **0 件** | **CONTRADICTION + UNKNOWN** | **AuthGap の誤 clear だった（D43 で修正）。**`cohort_root = Path(__file__).resolve().parents[2]` → `cache_dir = cohort_root / …` → `cache_dir.mkdir(...)`。`Path(...).parent` / `.parents[n]` が受け手の Path 形を落とし、`pathlib.Path.mkdir` の sink 行に当たっていなかった |
| `letsgojh0810/godsaeng-salon` / `check_reminders` | READONLY-001（`UPDATE reminders SET`） | CONTRADICTION **なし** | CONTRADICTION **なし**（不変） | **設計差。**`dparse.contradiction` は `eff.kind in ("EXEC","SPAWN","FS_WRITE")` に限る（`DESTRUCTIVE_KINDS`、D32）。**`readOnlyHint:true` + DB 書き込みは AuthGap の CONTRADICTION に入らない**（`docs/contradiction_matrix.md` D1、O23 #1） |
| `mcparmory/registry` / `delete_snapshot_by_delete_key` | READONLY-001 | ユニット**そのものが無い** | 同左（不変） | **`AST_NODE_CAP` の打ち切り**（下記 (4)）。`servers/grafana/server.py` は 54,192 ノードで cap 20,000 を超え、`truncations` に記録されている |

**誤りの向きを明記する。** 2 行目は**誤 clear 方向**（危険を見落とす側）だった。
最小再現で原因を切り分けた: `Path("/tmp")/"x"`・`Path("/tmp").resolve()` は sink に当たり、
**`Path("/tmp/a/b").parent` だけが当たらなかった**。

**残る 2 敗はどちらもバグではない。** 1 つは表がまだ決めていないマス（O23 #1）、
1 つは cap による欠測（O21）で、**どちらも記録済みである。**

#### (3) HintLint が見ているのは関数本体の 0 段だけ

AuthGap が母集団 v2 で CONTRADICTION を出した起点 API は **13 種**。HintLint の **10 個**の
`SINK_RULES` を実際に node で当てると、当たりうるのは **4 種**
（`subprocess.run` / `shutil.rmtree` / `Path(...).mkdir(` / `open(...)`）。
残り 9 種（`os.unlink` / `os.remove` / `os.replace` / `os.chmod` / `os.makedirs` /
`Path.unlink` / `Path.write_text` / `Path.write_bytes` / `Path.open`）はどの規則にも当たらない。
**`open` も無条件ではない**: 規則は
`/\bopen\s*\([^)]*(?:destination|path|file|artifact)[^)]*["'](?:w|a|wb|ab)["']/i` で、
引数の字面に `destination|path|file|artifact` のいずれかが無いと当たらない
（`open(f, "w")` は当たらない）。

AuthGap の CONTRADICTION 効果 130 件の**呼び出し段数**:

| 中間フレーム数（`witness_chain` の長さ） | 件数 |
|---|---|
| **0（ツール関数の本体内）** | **4（3.1%）** |
| 1 | 27 |
| 2 | 39 |
| 3 | 57 |
| 4 | 3 |

**1 段以上が 126 件（96.9%）。** API 種で当たりうるのは 46 件（35.4%）だが、
**両方の条件（0 段 かつ 当たりうる API）を満たすのは 130 件中 3 件（2.3%）。**

`mcparmory/registry` の 48 件を目視すると、当たっている sink は
`DeleteCustomFieldActivityCustomFieldIdRequest(` のような **pydantic のリクエスト模型の
コンストラクタ**であって、削除そのものではない。実際の削除は
`_execute_tool_request(method="DELETE", ...)`（`servers/close/server.py:810` のモジュール水準の
補助関数）で、**ツール本体の外＝ 1 段降りた先にある**。
**判定は正しいが、根拠として挙げた行は削除ではない**（名前の一致で当たった）。

#### (4) 公平性のための自己申告 — AuthGap 側の打ち切り

| 木 | 事情 |
|---|---|
| `david-li0406/meta-skill-evloving` | **AuthGap は 180 秒の tree budget で打ち切られ、ユニット 0 件**（`budget_skipped: 716`、511.6 秒）。HintLint は比較可 12 件。**この木は比較として成立していない** |
| `mcparmory/registry` | `@mcp.tool` が 10,170 個。**うち 9,524 個（93.6%）が `AST_NODE_CAP`（20,000 ノード）で切られたファイルの中**にある（64 ファイル、`truncations` に記録）。AuthGap のユニットは 646 個 |

母集団 v2 全体では `@tool` 系デコレータ 12,713 個のうち **9,816 個（77.2%）が切られたファイル内**だが、
**その 9,524 個が `mcparmory/registry` 1 本**である。**この 1 木を除くと 292 / 2,543 = 11.5%。**
`mcparmory/registry` は生成された MCP サーバを集めた単一リポジトリで、母集団の他の木と性質が違う。
**分母の扱いは決まっていない**（`docs/open_questions.md` O21）。

### 結論 — 競合だが、問いと分母が違う

| 論点 | HintLint | AuthGap |
|---|---|---|
| 主に数えているもの | **宣言が無い**ツールの危険（65 件中 61 件） | **宣言があって反する**ツール（CONTRADICTION） |
| 解析 | Python は行単位の正規表現。**本体 0 段のみ、呼び出しを追わない** | AST + 値解析。**CONTRADICTION の 96.9% は 1〜4 段降下** |
| 解決できないもの | **語彙が無い。** 正規表現に当たらなければ何も残らない（率を報告できない） | `opaque(reason)` 8 語 + `truncations` + `budget_skipped` で残し、率を報告する（52.8%） |
| 母集団 | 20 リポジトリの pilot（選び方は未検証） | 宣言ありを 3,827 件列挙 → 87 木を SHA pin、事前登録 |
| 範囲 | `openWorldHint` と flow 規則 5 種を持つ | `openWorldHint` 未実装。DB / NET は CONTRADICTION に入れない |
| 目的 | CI に載せる linter。精度優先で不確かなものを落とす | 測定研究。落とさずに率で報告する |

**この突き合わせは AuthGap のバグを 1 件見つけた。** `readOnlyHint: true` のツールの
`mkdir` が効果行を 1 本も出していなかった（`Path(...).parents[n]` が受け手の Path 形を
落とす。D43 で修正、母集団全体で CONTRADICTION が 79 → 85 になった）。
**先行研究との突き合わせを「位置づけの説明」で終わらせず、実際に走らせた価値はここにある。**

**「解決できなかったものをどう扱うか」が最大の差である**（`docs/open_questions.md` O19 の
最重要の確認点だった）。**HintLint には未解決を表す語彙が無く、正規表現に当たらなければ
分母からも消える。** したがって「MCP サーバの宣言がどれだけ当てにならないか」という
**率の問い**には答えられない。AuthGap の位置づけは「同じ現象を linter でなく**測定**として
やる」であり、**検出力で勝ったという主張はできない**（上の (2) は 4 件中 1 勝 3 敗）。

### この比較の限界（本文の限界節に書く）

1. **HintLint の TS / JS 経路は見ていない。** そちらには到達解析があり、母集団 v2 が
   Python の MCP サーバだけなので設計全体の評価になっていない。
2. **入口を揃えていない。** `scripts/codeql_fair.py` と違い、HintLint に同じ入口集合を
   渡す手段が無い。件数の大小は比較にならない。
3. **比較できた事例が 4 件しかない。** この標本で優劣は言えない。

## R2. AgentFlow — Agent Dependency Graph（**相補的。競合しない**）

| 欄 | 内容 |
|---|---|
| 書誌 | Shenao Wang, Xinyi Hou, Yanjie Zhao, Xiao Cheng, Haoyu Wang（華中科技大学 / Macquarie 大学）。arXiv:2607.01640v1 [cs.SE]、2026-07-02 |
| 読んだ範囲 | **全 12 ページの本文**（Abstract / §I / §II / §III / §IV-A,B,C / §V 冒頭 / §VI 限界 / §VII）。評価の表は未精読 |

### 確認済み

**解析対象は「エージェント プログラム」= MCP を使う側のコード。** 論文の scope
（§II-A）は「agent frameworks で書かれた agent program」で、**Claude Code のような
エージェント製品と低コード エージェントは明示的に除外**している。MCP サーバの実装は
対象外である。

**ADG の定義**（§IV-A）。`ADG_P = ⟨ACDG_P, ACFG_P, ADFG_P⟩`（component dependency /
control flow / data flow）。ノード集合は `V = A ⊎ I ⊎ M ⊎ C ⊎ S ⊎ G`
（agent / prompt / model / capability / state / policy）。

**MCP の扱い**（§IV-B、Fig.4）。クライアント側の `HostedMCPTool(...)` を読んで
`MCPDef` ノードと `BindMCP` 辺を作る。承認方針は `BranchIf(ApprovalPolicy, SendEmail)`
として ACFG の条件分岐になる。**つまり MCP ツールは「URL つきのノード」であって、
その中身は読まない。**

**注釈（`readOnlyHint` 等）は扱っていない。** 本文全体で `readOnlyHint` /
`destructiveHint` / `openWorldHint` / `annotation` の出現は **0 件**（全文検索で確認）。
**宣言と実装の照合という問いは立てていない。**

**応用は 2 つ**（§IV-C）。Agent BOM 生成（ACDG を辿って各エージェントの構成要素を集める）と、
prompt-to-tool risk 検出（`P2T(P) = {(p,a,c) | (p,a)∈R_pa, (a,c)∈R_ac, (a,c)∈E_arg}`。
prompt 由来のデータが特権 capability の**引数**に届くか）。**これは prompt injection の
到達性であって、宣言との照合ではない。**

**評価**。AgentZoo = GitHub から 5 フレームワークの import を code search で集め、fork と
archive を除き、フレームワーク構造の無いものを落として **5,399 プロジェクト**
（LangChain/LangGraph 3,823、CrewAI 947、OpenAI Agents SDK 442、LlamaIndex 146、
Semantic Kernel 41）。default branch の最新スナップショット。prompt-to-tool risk を
**238 件**検出。フレームワーク構造は 5 フレームワークで **143 構造**をモデル化。Python のみ。

### **限界節が AuthGap の位置を決めている**（§VI、著者の言葉）

> ADG captures high-level framework semantics and **does not replace low-level program
> dependency analysis. For tasks that require reasoning inside tool implementations or
> library calls**, ADG can be combined with points-to analysis to track the full taint
> propagation paths.

**「ツール実装の内部を推論する仕事」= AuthGap の守備範囲**であり、著者自身が ADG では
できないと書いている。したがって両者は相補的で、AuthGap は「AgentFlow が名指しした穴を
埋める側」として位置づけられる。

他の限界も 4 つ挙げている。過大近似による偽陽性、**フレームワーク API の慣習に従わない
自作構造には効かない**（AuthGap の `ENTRY_RULES` と同じ問題。引用できる）、Python と
5 フレームワークのみ、フレームワークの変化に追随する必要。

### AuthGap との対比（本文に書ける形）

| 論点 | AgentFlow | AuthGap |
|---|---|---|
| 解析対象 | エージェント プログラム（MCP を**使う**側） | MCP サーバ（ツールを**実装する**側） |
| MCP ツール | URL つきのノード。中身は読まない | 本体を読み、効果 kind を出す |
| 宣言（注釈） | 扱わない（出現 0 件） | 主軸 |
| 危険の定義 | prompt が特権 capability の引数に届く | 宣言の上界に反する効果がある |
| 母集団 | AgentZoo 5,399（フレームワーク import で収集） | 宣言あり 3,827 → 87 木を SHA pin |
| 承認方針 | クライアント側の `ApprovalPolicy` を分岐として持つ | サーバ側の承認割り込み（付録、D36 で降ろした） |

---

## R3. ReactAppScan — Component Graph（**手法の型として引ける**）

| 欄 | 内容 |
|---|---|
| 書誌 | Zhiyong Guo, Mingqing Kang（Johns Hopkins）, V.N. Venkatakrishnan, Rigel Gjomemo（UIC）, Yinzhi Cao（Johns Hopkins）. CCS '24, Salt Lake City, 2024-10-14〜18, 15 ページ. doi:10.1145/3658644.3670331 |
| 読んだ範囲 | Abstract / §1 / §2 の Key Idea / §6.1 評価の設計。**手法の詳細（§3〜§5）と評価の表は未精読** |

**検索結果の書誌は正しかった**（著者 5 名の順序も一致）。

### 確認済み

**問題設定。** React の props / state を通るデータフローを既存解析が追えない。JSX を扱えるのは
CodeQL だけだが、**コンポーネントをまたぐ React Data Flow を追えない**。

**Component Graph（CoG）の骨子**（§2 Key Idea）。

1. コンポーネントを親子関係に従ってノードにし、**state と props をそのコンポーネント
   ノードの下のノードにする**。
2. **別名のオブジェクトは同じ 1 ノードにする。** 例: `BlogDetail` の `content` state と
   `BlogContent` の `content` prop は 1 ノード。React の意味論（親の state が変われば子の
   prop も変わる）に従うから。
3. **クライアント / サーバとデータベースの依存は「キー」で結ぶ。** DB の `content` キー、
   ルータの `/getBlog` とクライアントの fetch を共通のキーで対応づけて CoG に注記する。
4. 構築は**抽象解釈**で、抽象領域がグラフそのもの。JSX の静的構造から始めて React と
   同じ更新手続きをモデル化する。

**CoG は ODG / CPG と相補的で組み合わせられる**と明記している（置き換えではない）。

**評価の設計**（§6.1）。データセットを 2 つ用意する。

- **大規模・ラベルなし**（GitHub と NPM から収集）→ 偽陽性率（FDR）の評価に使う。
- **小規模・ラベルあり**（CVE 付きの歴史的に脆弱なアプリ）→ 偽陰性率（FNR）の評価に使う。

zero-day の認定は 3 条件で、(ii) 手検索で CVE や既存データセットに無いこと、
(iii) **手作業の exploit で検証**すること。61 件を検出し、6 件が修正、2 件が承認された。

### AuthGap に引ける点

1. **「別名は 1 ノード」を資源に写す。** MCP では「同じパス / URL / テーブルを触る複数の
   ツールを 1 ノードにする」に相当する。**サーバをまたぐ合成のリスク**を表すのに要る考え方。
2. **キーで結ぶ**という具体的な機構。ReactAppScan は DB キーとルート名で境界を越えた。
   MCP なら**正規化したパス / ホスト名 / テーブル名**が同じ役割を果たしうる。
3. **評価の 2 データセット構成。** 大規模ラベルなしで偽陽性、小規模ラベルありで偽陰性。
   AuthGap の較正対（CVE）と母集団 v2 は同じ構成なので、設計の正当化に引ける。

---

## 参考: MCP 公式の立場（読了）

[Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)（2026-03）。

- 仕様は「**annotations は tool の挙動を忠実に記述することが保証されず、信頼できる
  サーバ由来でない限りクライアントは信頼できないものとして扱わねばならない**」と明記。
- 「ツールのリスクはセッション内の他の何があるかに依存する」（組み合わせリスク）とも書く。

**この研究の動機の一次資料として使える。** 「宣言が当てにならない」ことは公式に認知済みで、
残る問いは「**実際にどれだけ当てにならないか**」である。これは測定研究の問いである。

---

## まだ書いていないもの

- **（2026-10-02 に一部解決: 査読つきの論文は見つからず、自己発表の報告書がある。上の節）HintLint の論文の有無。** repo 内に引用形式・arXiv 番号・`paper` 系ファイルが無く、
  この実行環境からは検索できなかった（**「無い」ではなく「確かめられなかった」**）。
  学会発表や preprint があるなら比較の書き方が変わる。
- **HintLint の TS / JS 経路**（到達解析つき）の評価。母集団 v2 が Python だけなので未評価。
- CodeQL / Semgrep / Pysa との位置づけ（`scripts/codeql_fair.py` の比較はあるが未整理）。
- AgentFlow が比較対象にした AGENT-WIZ / AGENTIC RADAR。
- AgentFlow の引用にある MCP 関連（MCPTox ほか）、AgentArmor / Agentproof / Agent Audit。
- **MCP の宣言と実装の不一致を測る論文**（検索で見つけたが本文未読。`docs/incidental_writes_practice.md` §5）。とくに
  "Description-Code Inconsistency in Real-world MCP Servers"（分類に "Undeclared Side Effects" があると要約される）は、
  主軸と最も近い可能性がある。数値は未検証なので引用しない。
- **先行研究の LLM 判定が「決められないもの」をどう扱うかの対比表**（`docs/llm_judgment_survey.md` §2.3、§3 の付記）。
  差別化の芯（未解決を数える）を LLM 時代の研究に広げる材料。各セルは学生が commit を固定した原典で確かめてから載せる。
  プロンプトの指示（例: Cisco の "When in doubt, don't flag"）と、評価で確かめた挙動を書き分ける。
- **（2026-10-02 に解決: 見ない。本文に語が 0 回。上の節）DCIChecker が annotation（readOnlyHint など）を見るか**（仕様書でも ◎'）。差別化の軸 4 に効くので最優先で確かめる。
- **（2026-10-02 に本文を読んだ。上の節）VIPER-MCP**（arXiv 2605.21392、CodeQL + MCP 専用の QL）と **MCP-BiFlow**（arXiv 2605.07836）の本文。どちらも
  AuthGap に最も近い MCP の手法論文で、本文は未読（プロキシで遮断）。類似研究の実装の土台は `docs/implementation_base_survey.md`。
- 付随的な書き込みの扱いの先例（RFC 9110 の safe method、Checker Framework `@SideEffectFree`、observational purity）は
  `docs/incidental_writes_practice.md` §3。
