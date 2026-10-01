# 類似研究は解析器を自前で作っているか — 実装の土台の調査

調査日 2026-10-01。学生の問い（「本当に他の研究でも自前で行っているか」）に答えるため、3 体の agent に分けて調べた。
対象は MCP、エージェント・LLM アプリ、古典的な「宣言した権限と実際の動作」の研究。各研究の解析器の土台を一次資料で確かめた。
一次資料は論文本文、公開 repo の依存関係・import・README。D71 の理由づけを直すための記録である（下の §4）。

**確かさの印**:
- **高**: repo のコードや依存関係、または論文本文を読んだ（論文本文は第三者の GitHub 上のテキスト版を含む）。
- **中**: 第三者による逐語の抜き書き、または別の査読論文の記述。
- **低**: 検索結果の要約だけ。逐語ではない。

arxiv.org・ACM・USENIX などはプロキシで遮断され、**論文の PDF は 1 本も直接読めていない**。数値（例: 他研究の検出数）は
引用しない（CLAUDE.md 規則 1）。

**分類**:
- (1) 既存のパーサ（`ast`・Esprima・tree-sitter など）の上に解析を自作
- (2) 既存の解析基盤（CodeQL・Soot・WALA・Pysa・PyCG・Joern・Semgrep など）の上に作る
- (3) LLM で判定
- (4) 混合

---

## 1. MCP サーバのコードを解析する研究・道具（2025〜2026）

| 研究 | 土台 | 分類 | 確かさ |
|---|---|---|---|
| **VIPER-MCP**（arXiv 2605.21392） | **CodeQL**。MCP 固有の source・sink・sanitizer と、ツールハンドラへの写像（anchor query）を自作の QL 1,232 行で書く。悪用の確認は LLM エージェント | (2)+(3) | 中（第三者 SoK repo の §4 の逐語抜き書き） |
| **MCP-BiFlow**（arXiv 2605.07836） | 独自の「MCP-aware entrypoint recovery」と手続き間の伝播解析。LLM を補助に使う。パーサ・IR の土台は未確認 | (1) か (2) は未確認 + (3) | 中（要旨の写し） |
| **MCP-in-SoS**（arXiv 2603.10194） | **Joern**（自作の CPGQL）、CodeQL・Semgrep の既定パック | (2) | 高（artifact） |
| MCP at First Glance（arXiv 2506.13538） | SonarQube + mcp-scan | (2) | 低 |
| MCPInspect（arXiv 2510.16558） | Semgrep の既定規則 | (2) | 低 |
| antgroup/MCPScan | Semgrep + LLM | (2)+(3) | 高（`pyproject.toml`） |
| **HintLint** | 自作の正規表現（パーサなし）。Semgrep・CodeQL の結果を任意で取り込む | (1) に近い + 任意で (2) | 高（ソース） |
| MCP-SecLint（IWSPA 2026） | Acorn（JS パーサ）+ 自作の taint 解析 | (1) | 高（README・依存） |
| mcp-sec-audit（arXiv 2603.21641 と同一と推定） | 論文の時点では正規表現と動的監視。その後 `ast` と tree-sitter を追加 | (1) | 高（repo）／同一性は中 |
| arXiv 2602.03580 | tree-sitter + 自作 | (1) | 低 |
| DCIChecker（arXiv 2606.04769。宣言と実装の不一致） | 構造を使った静的な抽出 + **一致の判定は LLM** | (4) | 中（要旨の写し） |
| Parasites in the Toolchain、MCP Safety Audit、snyk agent-scan | ソースコードは解析しない（記述を LLM などで判定） | (3) | 高 |

**この系統は割れている。** 汎用基盤の上に作るもの（VIPER-MCP・MCP-in-SoS など）と、パーサの上に自作するもの
（MCP-SecLint・HintLint・mcp-sec-audit など）がある。

- AuthGap に一番近い 2 本の手法論文（MCP 固有の入口と taint を扱う）でも分かれる。
  - VIPER-MCP は CodeQL + MCP 専用のクエリ。
  - MCP-BiFlow は独自の枠組み。要旨は既存の解析器について "unsafe data flows that existing analyzers handle poorly" と書き、
    理由に「MCP サーバの登録・振り分けの形が多様」「MCP 固有の taint の意味が要る」を挙げる（中）。
- 大規模な測定（センサス）型は、既製のツールをそのまま当てる傾向がある。ただし問いは一般の脆弱性で、宣言との照合ではない。

## 2. エージェント・LLM アプリを解析する研究

| 研究 | 土台 | 分類 | 確かさ |
|---|---|---|---|
| **TaintP2X**（ICSE 2026） | **Pysa / Pyre** で伝播。LLM SDK の stub（`.pyi`）と `.pysa` を自作。source の特定は自作の `ast` + LLM | (4)：(2) Pysa が主 | 高（repo の README とコード） |
| **LLMSmith**（CCS 2024） | **PyCG** の呼び出しグラフ + 自作の連鎖抽出。README に "bugs in pycg" とある | (2)+(1) | 高（repo）／会議名は中 |
| **AgentFlow**（arXiv 2607.01640） | 事実の抽出は **YASA**（Ant Group の多言語 taint 解析）。その上に自作の ADG とフレームワークの意味のレジストリ | (2)+(1) | 低（検索要約。本文未読） |
| IAL-Scan（arXiv 2607.01641） | Python で実装し、AST から自作の IR | (1) | 低 |
| **Agent Audit**（arXiv 2603.22853） | **標準ライブラリの `ast`**（"AST-only: Uses Python stdlib `ast` module, no external dependencies"）。関数の中だけの taint | (1) | 高（repo） |
| Agentic Radar | 標準の `ast` + フレームワーク別のパーサ | (1) | 高（repo） |

**傾向**: 手続き間の深い taint が要るものは既存の基盤に乗る（TaintP2X・LLMSmith・AgentFlow）。構造の取り出しや規則の照合が
主のものは `ast` で自作する（Agent Audit・Agentic Radar）。**どちらでも、フレームワーク固有の意味（stub・レジストリ・
入口の規則）は自分で書いている。** 同じ研究室でも論文ごとに土台を変えている（HUST の研究室は TaintP2X で Pysa、AgentFlow で
YASA、MalSkills で Semgrep。中）。

## 3. 古典:「宣言した権限と実際の動作」と能力の推論

| 研究 | 土台 | 分類 | 確かさ |
|---|---|---|---|
| **PScout**（CCS 2012） | **Soot** は事実の抽出だけに使い、呼び出しグラフと到達解析は自作（Perl） | (2)+(1) | 高（本文のテキスト版） |
| **COPES**（ASE 2012） | **Soot**（CHA / Spark）+ 自作 約 2.1 万行 | (2) | 高（著者 repo） |
| **Axplorer**（USENIX Sec 2016） | **WALA** + 自作 約 15 kLOC。"our approach is equally applicable to other analysis frameworks such as Soot" | (2) | 高（本文のテキスト版） |
| ARCADE（CCS 2018） | WALA | (2) | 中 |
| Stowaway（CCS 2011） | 権限の対応表は動的テスト。アプリ側は逆アセンブラの出力を自前で読む | (1)+動的 | 中 |
| **Mir**（CCS 2021） | **Google Closure Compiler** の pass として実装 | (2) | 高（repo） |
| **Capslock**（Google、Go） | **golang.org/x/tools**（SSA・呼び出しグラフ）+ 関数から能力への自作の対応表 | (2) | 高（repo） |
| **DoubleX**（CCS 2021、ブラウザ拡張） | **Esprima**（構文解析だけ）+ 自作の制御・データ・ポインタ解析 | (1) | 高（repo） |
| Ferreira ら（ICSE 2021、npm の権限） | Esprima + 自作の AST 走査 | (1) | 高（repo） |
| **MalOSS**（NDSS 2021）/ **Packj** | API の抽出は自作（Python は標準の `ast`）。MalOSS は taint だけ既存（PyT・FlowDroid など） | (1)+(2) | 高（repo） |
| Bandit | 標準の `ast` + プラグイン | (1) | 高（repo） |
| Carlini ら（USENIX Sec 2012、Chrome 拡張） | 解析器を作らず手作業と grep（商用ツールと VEX を試し、文字列の追跡の限界で使わなかった） | — | 高（本文のテキスト版） |

**傾向**:
- 成熟した言語水準の基盤がある言語（Java の Soot / WALA、Go の x/tools、JS の Closure）では、その基盤を使う。
- 基盤が乏しい言語（JS・Python）では、**「既存のパーサ + 自作の解析」**が標準の形（DoubleX・Ferreira・Packj・Bandit）。
- 基盤の上に作っても、精度が問題になる箇所（入口、IPC、非同期）は毎回自作で、そこが論文の貢献として書かれる（Axplorer の
  15 kLOC、PScout の自作の呼び出しグラフ）。
- **API から権限・能力への対応表は、例外なく自作。** どの研究でも、ここが研究の中身。

---

## 4. 結論と、D71 の理由づけの訂正

**前回（D71）の「新しい分野では自前の解析が多い」は単純化しすぎていた。** 正しくは次の 3 層に分けて言う。

1. **言語の水準（パーサ・中間表現・呼び出しグラフ）**: 成熟した基盤があれば使うのが一般的。Python には CodeQL・Pysa・PyCG・
   Joern があり、MCP やエージェントの研究でも使われている（VIPER-MCP・TaintP2X・LLMSmith・MCP-in-SoS）。一方、
   `ast` などのパーサの上に自作するものも同じくらいある（Agent Audit・MCP-SecLint・HintLint・DoubleX・Packj）。
   **どちらも普通で、多数派は無い。**
2. **分野固有の部分（入口の規則、API と効果・権限の対応表、宣言の読み取り）**: **例外なく自作。** 基盤の上に作った研究も、
   ここは自分で書く（VIPER-MCP の 1,232 行の QL、TaintP2X の stub、PScout の対応表）。
3. **AuthGap の位置**: 標準の `ast`（既存のパーサ）の上に、2 の分野固有の部分と、1 の呼び出しの解決も自作した。「既存の
   パーサ + 自作の解析」の系譜（DoubleX・Packj・Agent Audit）と同じ形。

**したがって論文では「みんな自前だから」とは書けない。** 自前を選んだ理由は、AuthGap 自身の事情で示す必要がある。

- 前身の研究で、無改変の Pysa の上の設計が成り立たなかった（`AUTHGAP_BRIEF_v3.md` §1。pyre の環境が立たない、SDK の
  stub の境界で taint が切れる）。TaintP2X が LLM SDK の stub を 30 個以上自作して Pysa を通したこととも合う。
- 研究の問いは「宣言がどれだけ当てにならないか」という率なので、解析できなかったものを理由つきで数える必要がある
  （`opaque(reason)`、D40）。
- 標準ライブラリだけなので、凍結した版と Python の版が揃えば誰でも同じ結果を出せる。

**査読で最も突かれやすいのは VIPER-MCP（CodeQL + MCP 専用のクエリ）との対比**。「なぜ CodeQL にクエリを足さなかったか」に
答えられるようにする。手元にある材料は、入口を揃えた CodeQL との比較（`scripts/codeql_fair.py`、D26 の (c)）。
VIPER-MCP は本文が読めていないので、比較は本文を読んでから書く。

## 5. 確かめられなかったもの

- 論文の PDF は 1 本も直接読めていない（arxiv.org・ACM・USENIX がプロキシで遮断）。上の「中」「低」はその影響。
- MCP-BiFlow の解析の土台（独自の IR か、既存の基盤か）。公開 repo は見つからない。
- AgentFlow が YASA を使うことは検索要約だけ。
- VIPER-MCP の引用は第三者の抜き書きで、原本と照合していない。会議名も未確認。
- ARCADE・Stowaway・VEX・Koved らの土台の細部（中〜低）。
