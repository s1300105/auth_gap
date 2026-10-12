# 国内の発表・2026 年の会議プログラム・学位論文・グレー文献（arXiv 中心の検索では拾えない情報源）

調査日: 2026-10-12。検証の水準: ◎ = 一次資料の本文を自分で読んだ / ○ = 抄録・公式ページ・プログラムの項目 / △ = 二次情報。
数値はすべて**著者の主張で、こちらでは検証していない**（CLAUDE.md 規則 1）。「見つからなかった」は検索した範囲での話で、「存在しない」という意味ではない。
ダウンロードしたファイルは `/tmp/claude-0/.../scratchpad/` 以下にだけ置いた（リポジトリには置いていない）。

A1〜A8 の意味: (A1) 宣言側として何を読むか（構造化注釈 / 自然言語の説明 / なし）、(A2) 効果側の推定方法（静的 / 動的 / LLM）、(A3) 呼び先を辿るか、(A4) Python を対象にするか、(A5) 解決できない部分の扱い、(A6) 母集団と人手の正解、(A7) 決定的か、(A8) 事前登録や凍結があるか。

---

## 問 1: 国内会議（2025–2026）に、MCP の注釈やツールの宣言を実装と照合する研究はあるか

### Takeaway
国内で最も近いのは、早大 森研の**山崎・戸田・森「LLMエージェントのツール呼び出しログとOS監査ログの対応付けによる悪性MCPサーバの検知手法」**（IPSJ SPT 研究報告 2026-02-24、IEICE ICSS と連催で 2026-03-04 に発表）だった。「宣言外のリソースアクセスや副作用」を、プロキシで記録した**呼び出し要求**と**OS 監査ログ**を突き合わせて**動的に**検知するもので、問題意識は AuthGap と重なる。ただし宣言側は構造化注釈ではなく呼び出し要求であり、手法も動的なので、方法はほとんど重ならない。CSS2026（2026-10-19〜23、まだ開催前）には **2D1-1「安全なMCPレジストリのための検証フレームワークの提案と実証評価」（東京都市大）** があるが、公開されているのは題だけで、内容は確認できなかった。**構造化 `ToolAnnotations`（readOnlyHint など）をコードと照合する国内発表は、確認したプログラムとデータベースの範囲では見つからなかった。**

### Cited Findings

#### 関連の強い国内発表（A1〜A8 と判定）

**(J1) 山崎 惣大・戸田 宇亮・森 達哉（早稲田大学／理研 AIP／NICT）「LLMエージェントのツール呼び出しログとOS監査ログの対応付けによる悪性MCPサーバの検知手法」** — 検証 ○（抄録のみ。本文は研究会の会員限定）
- 書誌: 情報処理学会 研究報告 SPT, 2026-SPT-62, No.63, pp.1–8, 2026-02-24 — [IPSJ 電子図書館](https://ipsj.ixsq.nii.ac.jp/records/2007264)。IEICE ICSS と IPSJ SPT の連催で 2026-03-04 に沖縄県立美術館・博物館で発表（ICSS2025-139） — [IEICE 技報 講演検索 (2025 年度, "MCP")](https://ken.ieice.org/ken/search/index.php?instsoc=&tgid=&year=23&region=&pskey=MCP&ps1=1&ps2=1&ps3=1&ps4=1&ps5=1&search_mode=&pnum=0&psize=4&psort=0&submit_public_schedule_paper=%E8%AC%9B%E6%BC%94%E6%A4%9C%E7%B4%A2)
- 抄録（原文どおり）: 「悪性MCPサーバは正当なツールを装い，宣言外のリソースアクセスや副作用（以下，悪性挙動）を混入させうる」「ローカルのファイルシステム操作を伴うツールを対象として，MCPクライアント・サーバ間に配置したプロキシで記録したツール呼び出しの要求内容を宣言情報とし，OS監査ログ上の実行痕跡と呼び出し単位で対応付ける」「21件のシナリオによる評価の結果，Precision 1.00，Recall 0.81，F1スコア0.90」「アクセス先パス自体には不一致が生じないケースにおいて3件の見逃し」 — [IPSJ](https://ipsj.ixsq.nii.ac.jp/records/2007264)
- A1: ツール呼び出しの**要求内容**（引数）を「宣言情報」とみなす。構造化注釈を読むかどうかは抄録に書かれていない。/ A2: **動的**（OS 監査ログ）。/ A3: 実行時の観測なので、呼び先の静的解析にはあたらない。/ A4: 抄録に記載なし。/ A5: 記載なし（限界として、パスの不一致として現れない攻撃を見逃すことを明記している）。/ A6: 21 件の作成シナリオで、野外の母集団ではない。/ A7: 抄録に LLM の記述はなく、照合は規則的とみられるが不明。/ A8: 記載なし。
- **判定: 部分的に重なる** — 「宣言と実効の乖離を副作用として捉える」という概念は共通する。違いは三つあり、宣言側が呼び出し要求であって注釈ではないこと、インストール前の静的解析ではなく実行時の動的検知であること、悪性サーバの検知を目的としていること。修士論文では**国内の先行研究として必ず引用し、対比を書くべき一件**。

**(J2) 浦川 太良・中村 徹（東京都市大学大学院 総合理工学研究科 情報専攻）「安全なMCPレジストリのための検証フレームワークの提案と実証評価」CSS2026 2D1-1（セッション 2D1「AIサプライチェーンの脅威」）** — 検証 ○（プログラムの題のみ）
- 出典: [CSS2026 プログラム](https://www.iwsec.org/css/2026/program.html)。CSS2026 は 2026-10-19〜23 にアクトシティ浜松で開催 — [CSS2026](https://www.iwsec.org/css/2026/)
- 抄録はプログラムページに載っていない。IPSJ 電子図書館に「コンピュータセキュリティシンポジウム2026」で検索をかけたが、2026 年の論文集の記録は出てこなかった（2025 年と 2024 年の分だけ）— [IPSJ API 検索](https://ipsj.ixsq.nii.ac.jp/api/records/?q=%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%82%BF%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E3%82%B7%E3%83%B3%E3%83%9D%E3%82%B8%E3%82%A6%E3%83%A02026)
- A1〜A8: **すべて不明**。
- **判定: 不明（題だけでは判定できない）** — 「MCP レジストリへの登録時の検証」なので、インストール前に検査するという点で AuthGap と重なる可能性がある。**開催後（10/19 以降）に予稿を読む必要がある**（下の Gaps を参照）。

**(J3) 青柳 龍太（Science Tokyo）・范 優美（奈良先端大）・李 家隆（早大）・鄭 顕志（Science Tokyo）「オープンソースLLMエージェントフレームワークにおける権限管理メカニズムの実証調査」** — 検証 ○（抄録）
- 書誌: IPSJ 研究報告 SE、2026-07-15 — [IPSJ](https://ipsj.ixsq.nii.ac.jp/records/2010573)。IEICE では SS2026-17 / KBSE2026-17 — [IEICE 技報 講演検索 (2026 年度)](https://ken.ieice.org/ken/search/index.php?instsoc=&tgid=&year=24&region=&pskey=%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88&ps1=1&ps2=1&ps3=1&ps4=1&ps5=1&search_mode=&pnum=0&psize=4&psort=0&submit_public_schedule_paper=%E8%AC%9B%E6%BC%94%E6%A4%9C%E7%B4%A2)
- 抄録: 2026 年 4 月時点で広く使われている 10 件の OSS エージェントフレームワークを対象に、OWASP Agentic AI Threats and Mitigations v1.1 に基づいて 20 軸から 10 軸に絞った評価軸で「ソースコードと公式ドキュメントの静的分析」を行った。結果は「承認履歴の永続化，フレームワーク全体に及ぶリソース制限，マルチエージェント構成における権限伝播制御は限定的」— [IPSJ](https://ipsj.ixsq.nii.ac.jp/records/2010573)
- A1: なし（フレームワークの機構を調べるもので、ツールの宣言は扱わない）/ A2: 人手による静的な調査とみられる / A3〜A5: 該当しない / A6: 10 フレームワーク / A7・A8: 記載なし。
- **判定: 隣接** — 対象はエージェント側（クライアント・フレームワーク）の権限機構で、MCP サーバの宣言と実装の照合ではない。

#### 確認したプログラムと検索（関連する発表がなかったものを含む）

- **CSS2026 本会議プログラム**（`paper-title` 356 件。MWS / OWS / AWS などのワークショップ枠を含む）: 題に MCP を含む発表は **1 件（2D1-1）**。AI エージェント関連は 1E2 セッション「AIエージェントへの攻撃」（三菱電機による脅威モデリング・Control-State Poisoning・ツール利用型エージェントのレッドチーミング、KDDI 総研、筑波大のハニーポット）や 2D1-5「Agentic AI構築ミドルウェアの構造的脆弱性」（東京電機大）などがあるが、**注釈とコードの照合は見つからなかった** — [CSS2026 プログラム](https://www.iwsec.org/css/2026/program.html)
- **CSS2026 デモ・ポスター**（DP 約 60 件）: MCP を題に含む発表は 0 件。DP-16「AIエージェントシステム向け自動リスクアセスメント」（三菱電機）が隣接する程度 — [CSS2026 demo](https://www.iwsec.org/css/2026/demo.html)
- **CSS2025 プログラム**（番号つき発表約 272 件）: MCP / Model Context Protocol を題に含む発表は **0 件**。エージェント関連は 3A4-3「エージェントアンプ攻撃」、1A1-2「Supervisor型LLMエージェントによるPythonパッケージの…解析」など — [CSS2025 プログラム](https://www.iwsec.org/css/2025/program.html)（WebFetch で抽出）
- **SCIS2026**（2026-01-26〜30）: プログラムは約 405 件で、題と「Web要約」を全文検索しても **MCP の語は 0 件**。ポスターも MCP は 0 件。エージェント関連は 2Z1-4「Self-Attentionを用いたAI AgentのIndirect Prompt Injection攻撃に対する動的防御」（NTT）など — [SCIS2026 プログラム](https://www.iwsec.org/scis/2026/program.html)、[SCIS2026 ポスター](https://www.iwsec.org/scis/2026/poster.html)
- **IPSJ 電子図書館**（WEKO API で "MCP"、"MCPサーバ"、"ツール呼び出し"、"AIエージェント"、"LLMエージェント"、"エージェント 権限"、"ツール記述"、"記述と実装"、"宣言と実装"、"副作用 静的解析"、"エージェント 最小権限" などを検索し、2025-06 以降に絞った）: セキュリティ系（CSEC / SPT）と SE 系で関係するのは J1 と J3 だけだった。CSEC / SPT の 2026-07-06 の回は「LLMエージェントを用いたバイナリ解析…」「LiveCVEBench-Lite」など、MCP の注釈とは関係しない — [IPSJ API 検索 "MCP"](https://ipsj.ixsq.nii.ac.jp/api/records/?q=MCP&size=100&sort=-createdate)
- **ソフトウェアエンジニアリングシンポジウム SES2026**（論文集は 2026-09-03 に公開）: 電子図書館で見えるエージェント関連は「対話型AIエージェントツール利用に関する潜在的課題の探索的検討：Claude導入組織を対象とした事例分析」（利用ログとインタビュー）、「AEGIS」「VibeGuard」など。**MCP の注釈やツール宣言の照合は見つからなかった** — [IPSJ records/2011745](https://ipsj.ixsq.nii.ac.jp/records/2011745)
- **情報処理学会 第88回全国大会**（2026 年 3 月。プログラム 8 ページから約 1,591 件を解析）: MCP を題に含むのは 4 件で、2L-03「Model Context Protocolに基づくAI駆動型モバイルUIテスト自動化…」（明大）、**4L-04「MCPサーバーにおけるツール選択精度と引数生成の正確性に関する研究」（早大 今村・岸）**、5ZD-01「マルチMCPサーバによる…イベント推薦」（お茶大）、5ZK-03「静的解析を統合した MCP と AI コーディングエージェントによるWebアクセシビリティエラー自動修正」（東洋大）。**どれもセキュリティや注釈の照合を扱っていない** — [第88回全国大会 プログラム（program2）](https://www.ipsj.or.jp/event/taikai/88/WEB/html/program/program2.html)、[program4](https://www.ipsj.or.jp/event/taikai/88/WEB/html/program/program4.html)、[program8](https://www.ipsj.or.jp/event/taikai/88/WEB/html/program/program8.html)
- **FIT2026**（2026-09-02〜04。約 1,469 件を解析）: MCP を題に含むのは B-009「Octagon Tester: GraphRAG and MCP-enabled Automated Agentic Web testing」（九大）と E-057「AIエージェント活用フロントDXにおけるマルチユーザ対応MCPサーバの開発」（日立）。F-013「LLMにおけるツール呼び出しの誤り蓄積による呼び出し精度改善」（芝浦工大）は隣接するが、セキュリティは扱っていない — [FIT2026 プログラム B](https://www.ipsj.or.jp/event/fit/fit2026/abstract/data/html/program/b.html)、[E](https://www.ipsj.or.jp/event/fit/fit2026/abstract/data/html/program/e.html)、[F](https://www.ipsj.or.jp/event/fit/fit2026/abstract/data/html/program/f.html)
- **日本ソフトウェア科学会 第43回大会（JSSST2026）**: プログラムページに MCP の語は 0 件 — [JSSST2026 プログラム](https://jssst2026.wordpress.com/program/)
- **IEICE 技報**（講演検索で "MCP"）: 2025 年度の MCP の題は 5 件で、NS が 2 件（tool 選択・MCP キャッシュ、NTT・東大）、ICM/LOIS の招待講演 1 件、**ICSS の 1 件（= J1）**、SC の 1 件（富士通「…個別リモートMCPサーバと共通ファイルサーバを用いたファイル管理手法」）。2026 年度（これまで）は 2 件で、どちらもセキュリティ以外 — [IEICE 講演検索 2025 年度](https://ken.ieice.org/ken/search/index.php?instsoc=&tgid=&year=23&region=&pskey=MCP&ps1=1&ps2=1&ps3=1&ps4=1&ps5=1&search_mode=&pnum=0&psize=4&psort=0&submit_public_schedule_paper=%E8%AC%9B%E6%BC%94%E6%A4%9C%E7%B4%A2)。エージェント関連でセキュリティを扱うのは「脆弱性検知から修正までを行うAIエージェントの実態調査」（NTT, IA2026-5 / ICSS2026-5）、「AIブラウザエージェントを用いたIoT機器管理画面への攻撃可能性評価」（横国大, ISEC2026-66 ほか）など — [IEICE 講演検索 2026 年度 "エージェント"](https://ken.ieice.org/ken/search/index.php?instsoc=&tgid=&year=24&region=&pskey=%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88&ps1=1&ps2=1&ps3=1&ps4=1&ps5=1&search_mode=&pnum=0&psize=4&psort=0&submit_public_schedule_paper=%E8%AC%9B%E6%BC%94%E6%A4%9C%E7%B4%A2)
- **J-STAGE**（検索 API。"Model Context Protocol"、"MCPサーバ"、"MCP セキュリティ"、"MCP ツール" を 2025 年以降で検索）: 出てきたのは応用研究だけだった（JSAI2026「MCP ツール呼び出し最適化におけるモデル強度の影響分析」、TogoMCP、土木・防災・IR への適用など）。セキュリティ系では IEICE Fundamentals Review の解説「生成AI・エージェントセキュリティ最前線」（披田野 清良, KDDI総研, Vol.20 No.1, 2026-07-01）があるが、**MCP には触れていない** — [J-STAGE 検索 API](https://api.jstage.jst.go.jp/searchapi/do?service=3&text=Model%20Context%20Protocol&pubyearfrom=2025)、[JSAI2026 2E1-GS-5b-02](https://www.jstage.jst.go.jp/article/pjsai/JSAI2026/0/JSAI2026_2E1GS5b02/_article/-char/ja/)、[Fundamentals Review](https://www.jstage.jst.go.jp/article/essfr/20/1/20_6/_article/-char/ja/)
- **IPSJ 論文誌・JIP・IEICE 論文誌**: CiNii と IPSJ の検索で MCP のセキュリティを扱う論文誌論文は見つからなかった。IEICE Trans. Inf. & Syst.（2026-09）に「An Interoperable IoT Service Platform for Supporting the Development of LLM Agents」があるが、セキュリティの論文ではない — [CiNii Research](https://cir.nii.ac.jp/crid/1390590912421328384)

### Inferences
- 国内で「宣言と実効の乖離」を MCP について扱ったのは、確認できた範囲では J1（動的・悪性検知）だけだった。**構造化注釈を、インストール前の静的解析でコードと照合し、野外の母集団で測る**研究は国内では見つからなかった。修士論文の新規性の主張として「国内では J1 が動的、AuthGap が静的」と対比を書くのが自然だと考える（推論）。
- J1 の限界（パスに不一致が現れない書き込みを見逃す）は、静的解析で「書き込みの効果があるのに readOnlyHint=true」を判定する AuthGap と補完的に書ける（推論）。
- J2 は題だけからは判断できないが、早大森研（J1）と東京都市大中村研（J2）は、国内で MCP サーバの検証を扱っている研究室として追跡しておく価値がある（推論）。

### Gaps
- **J2（CSS2026 2D1-1）の内容は不明。** CSS2026 は 2026-10-19 からで、予稿は電子図書館にまだ載っていない。開催後に IPSJ 電子図書館（CSS2026 論文集）で抄録と本文を確認し、A1（注釈を読むか）と A2（静的か動的か）を埋める必要がある。
- J1 の本文は研究会の会員限定のため読めていない。A4（言語）、A5、A7 は不明のまま。
- IEICE 技報の講演検索は 1 ページ分しか取得しておらず、"エージェント" のヒットは件数が多いため、ページ送り先を見落とした可能性がある。"MCP" のヒットは少数で、全件を見たと判断した。
- 全国大会と FIT の件数は、こちらの HTML 解析（番号パターンでの分割）による概数で、公式の件数ではない。
- MWS2026 / OWS2026 / AWS2026 のワークショップ独自の LT・企画（CSS 本会議プログラム外のもの）は確認していない。

---

## 問 2: 国内の学位論文（修士論文・博士論文）に MCP や LLM エージェントのツールのセキュリティを扱ったものはあるか

### Takeaway
CiNii Research（博士論文の検索と、全データ源・IRDB を指定した検索）では、MCP や LLM エージェントのツールのセキュリティを扱う国内の学位論文は**見つからなかった**。修士論文は機関リポジトリに公開されない場合が多いので、「見つからなかった」ことは不在を意味しない。

### Cited Findings
- CiNii Research 博士論文 OpenSearch: "Model Context Protocol" は 2 件ヒットしたが無関係（行動認識、衛星通信）。"LLMエージェント"、"AIエージェント セキュリティ"、"プロンプトインジェクション"、"大規模言語モデル 静的解析"、"LLM agent security" は 0 件だった — [CiNii dissertations "Model Context Protocol"](https://cir.nii.ac.jp/opensearch/dissertations?q=Model%20Context%20Protocol&format=json)
- 同じく "大規模言語モデル セキュリティ" は 1 件で、MAI Trong Khang「自然言語処理および大規模言語モデルのサイバーセキュリティへの応用」（博士論文）。MCP や注釈は扱っていない（題からの判断）— [CiNii](https://cir.nii.ac.jp/crid/1910025098814622208)
- CiNii Research の全文献検索（2025 年以降、IRDB を含む）で "Model Context Protocol"、"MCP サーバ"、"MCPサーバー" を検索すると、技術誌の記事（Software Design、Interface、日経コンピュータ）、書籍、応用研究（大学 IR、土木、図書館業務）、紀要（流通科学大学論集「Model Context Protocolを用いた戦略の適応と進化－囚人のジレンマ選手権－」）が出てきたが、**学位論文は出てこなかった** — [CiNii 全検索](https://cir.nii.ac.jp/opensearch/all?q=Model%20Context%20Protocol&format=json&from=2025)、[流通科学大学論集](https://cir.nii.ac.jp/crid/1050870696491787776)
- IRDB（irdb.nii.ac.jp）の検索ページは HTTP 403 を返し、直接は検索できなかった（CiNii 経由の IRDB 収録分だけを見た）。

### Inferences
- J2（浦川 太良、東京都市大 中村研）は CSS2026 のプログラムで筆頭に「◎」が付いており、所属が大学院なので学生発表と見られる。J1（山崎 惣大、早大 森研）の筆頭が学生かどうかは確認していない。どちらも 2026 年度（2027 年 2〜3 月）の卒業論文・修士論文として同じ主題がまとまる可能性がある（推論）。
- J3 の Science Tokyo 鄭研も、エージェントの権限という隣接主題で学位論文が出る可能性がある（推論）。

### Gaps
- 各大学の修士論文の題目一覧（研究室ページ、学科の発表会プログラム）は、今回は網羅的には調べていない。特に早稲田大学（森研）、東京都市大学（中村研）、東京科学大学（鄭研）、横浜国立大学（吉岡研）の 2025〜2026 年度の修論・卒論の題目は未確認。
- 2025 年度（2026 年 3 月）修了の修士論文は、リポジトリへの登録に時間差があるため、まだ収録されていない可能性がある。

---

## 問 3: 2026 年の国際会議プログラム・採択論文（arXiv に出ていないもの）に重なる研究はあるか

### Takeaway
最も重要な発見は **ContractGuard（CCS 2026、Penn State）** で、MCP ツールの「開発者が書いた説明」と「実装」の意味的な契約を、到達可能性に基づく静的スライス（Tree-sitter）と LLM による相互照合で監査する。arXiv では見つからず、著者のホームページで本文 PDF が公開されている。宣言側が**自然言語**で、判定に **LLM** を使う点で AuthGap とは異なるが、「ツール入口からの手続き間スライス」と「宣言と実装の照合」という骨格は同じで、修士論文の関連研究として**必ず対比が要る**。ほかに確認した会議（USENIX Sec 26、S&P 26、NDSS 26、ICSE 26、FSE 26、ISSTA 26、ASE 26、MSR 26、ACSAC 26、SANER 26）では、**構造化注釈とコードの照合は見つからなかった**。ICSE 2027（通知は 2026-10-20）、S&P 2027、NDSS 2027 はまだ採択一覧が出ていない。

### Cited Findings

#### (I1) ContractGuard: Auditing Semantic Contracts of MCP Tools for Security Violations — CCS 2026 — 検証 ◎（著者が公開した PDF の要旨、§1、§4.1〜4.3、§5 の設定、§5.1、関連研究、限界の節を読んだ。全文の精読ではない）
- 著者: Hengkai Ye, Zhechang Zhang, Ruibo Lu, Jinyuan Jia, Hong Hu（The Pennsylvania State University）。CCS '26（2026-11-15〜19, The Hague）、DOI 10.1145/3830454.3846789 — [CCS 2026 accepted papers](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html)、[Hong Hu ホームページ](https://huhong789.github.io/)、[PDF](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 要旨: 「An MCP tool exposes two semantic views of the same functionality: a developer-provided description … and an implementation」「ContractGuard combines reachability-aware static analysis with LLM-based cross-view reasoning」「3,586 MCP tools from 1,000 real-world MCP servers … uncovers 116 security issues … 21 misleading descriptions, 29 … potentially malicious code, and 66 unsafe implementations」（著者の主張）— [PDF](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 本文の例: 「a tool described as supporting read-only SQL queries violates the contract if its implementation permits arbitrary query execution」。readOnly の概念を**自然言語の説明**の側で扱っている — [PDF §1](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 方法（§4.1）: `@mcp.tool()`、`mcp.add_tool()`、`server.tool`、`server.RegisterTool`、`@mcp.list_tools()/call_tool()`、`setRequestHandler()` からツールの入口を特定する（Python と TypeScript、宣言的登録とディスパッチ型の両方）。Tree-sitter の AST から関数の呼び出し関係を復元し、入口から深さ優先で辿る。ライブラリや組み込み関数は呼び出し箇所を記録するだけで展開しない。スライスは平均 126 行で、サーバ全体の平均は 3,700 行 — [PDF §4.1](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 方法（§4.2〜4.3）: スライスを LLM が要約して「コードに基づく説明」を作り、未解決のシンボルは LLM が `grep_code`、`read_file`、`list_dir` で探して symbol-resolution memory に蓄える。説明を原子的な主張に分解して実装の動作と対応づけ、LLM の判定器が clean / instruction injection / misleading description / potentially malicious code / unsafe implementation の 5 つに分類する — [PDF §4.2–4.3](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 評価の設定（§5）: MCP.so から有効な 5,263 サーバを集め、無作為に 1,000 サーバを抽出し、1 サーバにつき最大 5 ツール。ツールの発見は「unsorted os.walk and retains the first five registration matches」（ファイルシステムの走査順に依存する）。既定の LLM は GLM-5.1 で温度 0.2。比較に GPT-5.4、Gemini-3.1-pro、Qwen-3.5-122B を使う — [PDF §5](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 人手の正解: 野外で報告されたものは全件を人手で確認した（適合率の側）。100 サーバ・311 ツールの部分集合を人手で監査し、18 件の違反をラベル付けして、ContractGuard の P=0.824、R=0.778 を、A.I.G.、MCPScan と比べている（著者の主張）— [PDF Table 3](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 限界（著者による）: 「AST-based slicing may miss call relationships obscured by complex indirection in dynamic languages such as Python and JavaScript … can cause errors in both directions」。関連研究では MCPDiFF を「the closest work to ours」としている。成果物は github.com/psu-security-universe/contractguard — [PDF §7, App.A](https://huhong789.github.io/papers/ye:contractguard.pdf)
- 本文中に "annotation"、"readOnlyHint"、"destructiveHint"、"hint" の語は見つからなかった（PDF をテキスト化して検索した）。
- A1: **自然言語の説明**（`tools/list` の description）。構造化注釈は読まない。/ A2: **静的なスライス＋LLM による要約と判定**。/ A3: **辿る**（プロジェクト内の呼び先を DFS で展開する。深さの上限は書かれていない）。/ A4: **Python と TypeScript**。/ A5: 未解決シンボルは **LLM に追加検索させて埋める**。opaque として残して率を報告することはしていない（読んだ範囲では見当たらない）。/ A6: MCP.so から無作為に 1,000 サーバ・3,586 ツール。人手の正解は 311 ツール中 18 件と、報告の全件確認。開発者が修正したコミットを使った再現率の測定は見当たらない。/ A7: **決定的ではない**（LLM、温度 0.2、走査順に依存したツール抽出）。/ A8: 事前登録・凍結の記述はない。
- **判定: 大きく重なる（問題設定と骨格）** — MCP ツールの入口から手続き間スライスを取り、「宣言」と「実装」の食い違いを、母集団で測るという骨格は AuthGap と同じ。違いは、AuthGap が差分として掲げる 5 点（構造化注釈を読む / LLM を判定に使わず決定的 / opaque を残してその率を出す / 事前登録と解析器の凍結 / 修正コミットからの再現率）が**すべて ContractGuard には無い**こと。そのため、関連研究では「同じ問いを、自然言語の宣言と LLM 判定で解いたもの」として明確に対比するのがよい。

#### (I2) 隣接する採択論文・発表（○ = 公式プログラムの題、または公式詳細ページ）
- **ICSE 2026 NIER "Towards Verifiably Safe Tool Use for LLM Agents"**（Doshi, Hong, Xu, Kang, Kapravelos, Kästner）: STPA でハザードを導き、MCP を拡張して「capabilities, confidentiality, trust level」の構造化ラベルを付け、データフローとツール列に対する強制可能な仕様にする — [ICSE 2026 NIER 詳細](https://conf.researchr.org/details/icse-2026/icse-2026-nier/41/Towards-Verifiably-Safe-Tool-Use-for-LLM-Agents)、[arXiv 2601.08012](https://arxiv.org/abs/2601.08012)。A1: 構造化ラベル（提案するもので、既存の ToolAnnotations ではない）/ A2: 実行時の強制 / コードとの照合はない。**判定: 隣接**（宣言を強化して強制する側で、宣言が正しいかの検証はしない）。
- **MSR 2026 Data and Tool Showcase "A Large-Scale Dataset of MCP Implementations on GitHub"**（Toeppe, Barrak, Ksontini）: 3,238 候補から 2,297 プロジェクトを検証済みとして JSONL で公開。標本の人手確認で適合率 83%（著者の主張）。Python と TypeScript が多い — [MSR 2026 詳細](https://2026.msrconf.org/details/msr-2026-data-and-tool-showcase-track/8/A-Large-Scale-Dataset-of-MCP-Implementations-on-GitHub)、[arXiv 2607.10123](https://arxiv.org/pdf/2607.10123)。**判定: 隣接**（母集団の取り方の比較対象）。
- **IEEE S&P 2026 "Towards Automating Data Access Permissions in AI Agents"**（Wu, Yang, Roesner, Kohno, Zhang, Iqbal）: 205 人のユーザ調査と、権限判断を予測する ML 補助（著者の主張で 85.1%）— [S&P 2026 accepted](https://sp2026.ieee-security.org/accepted-papers.html)、[arXiv 2511.17959](https://arxiv.org/abs/2511.17959)。**判定: 隣接**。
- **IEEE S&P 2026 "Cosseter: GitHub Actions Permission Reduction Using Demand-Driven Static Analysis"**: 題からは、宣言された権限と静的に必要とされる権限を比べ、過剰な権限を削る研究と読める（題のみ確認）— [S&P 2026 accepted](https://sp2026.ieee-security.org/accepted-papers.html)。**判定: 隣接**（他の領域で「宣言された権限と静的解析で求めた必要権限の照合」をしている類例。Android の過剰権限研究と並べて、方法論の系譜として引用できる可能性がある）。
- **IEEE S&P 2026 "Parasites in the Toolchain: A Large-Scale Analysis of Attacks on the MCP Ecosystem"**: 題のみ確認 — [S&P 2026 accepted](https://sp2026.ieee-security.org/accepted-papers.html)。arXiv の "Mind Your Server: A Systematic Study of Parasitic Toolchain Attacks on the MCP Ecosystem"（2509.06572）と同じ研究の可能性があるが、**同一かどうかは確認していない** — [arXiv 2509.06572](https://arxiv.org/abs/2509.06572v2)（△）。**判定: 隣接**（攻撃側）。
- **CCS 2026**: ContractGuard のほかに、"SkillScope"（既知）、"MetaMancer: Practical Tool Selection Attacks against LLM Agents"、"Governing AI Agent with Capability and Delegation Chain"、"zkAgent" — [CCS 2026 accepted](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html)。**判定: 隣接**（題のみ）。
- **ACSAC 2026**: "The Devil's Whisper to Agents: Unveiling and Formalizing Training-Free Backdoor Attacks Across the MCP-Enabled Agent Execution Lifecycle"、"SkillMutator"、"zk-Mandate"、"Know Your Agent" — [ACSAC 2026 papers](https://www.acsac.org/2026/program/papers/)。**判定: 隣接**（攻撃と認可）。
- **NDSS 2026**: "Les Dissonances: Cross-Tool Harvesting and Polluting in Pool-of-Tools Empowered LLM Agents"、"Prompt Injection Attack to Tool Selection in LLM Agents"、"The Dark Side of Flexibility: Detecting Risky Permission Chaining Attacks in Serverless Applications" — [NDSS 2026 accepted](https://www.ndss-symposium.org/ndss2026/accepted-papers/)。**判定: 隣接**。
- **USENIX Security 2026**（technical sessions から 377 題を抽出）: **題に MCP を含む論文は 0 件**。MCP の語が出てくるのは基調講演 "When AI Stops Answering and Starts Acting" の概要（"MCP as a shared supply-chain attack surface"）だけ。隣接するものに "AttriGuard"、"\"Do Not Mention This to the User\": Detecting and Understanding Malicious Agent Skills in the Wild"、"Breaking the Lethal Trifecta"、"Raising the Flag: Detecting Missing Permission Controls in Mini-Program APIs" — [USENIX Sec 26 technical sessions](https://www.usenix.org/conference/usenixsecurity26/technical-sessions)
- **FSE 2026**（444 題）: MCP の題は 1 件で、"Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions"（Hou ら、サーベイ）。AgentBound（既知）も載っている — [FSE 2026 research papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers)
- **ISSTA 2026**（210 題）: MCP の題は 0 件。"Datura: Progressive Red Teaming Testing for Tool Invocation Chain in LLM Agents"、"LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle" が隣接する — [ISSTA 2026](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers)
- **ASE 2026**（research track 441 題）: MCP の題は 0 件。"MalSkills: Detecting Malicious Skills in the Agentic Supply Chain via Neuro-symbolic Reasoning"、"How Your Credentials Are Leaked by LLM Agent Skills"、"Specifying the Delegated-Autonomy Boundary: Requirements Engineering for Agentic AI"、"RefineAct" が隣接する — [ASE 2026 research track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)
- **ICSE 2026**（research track ページの 673 題）: MCP の題は 0 件。"AgentSpec: Customizable Runtime Enforcement…"、"TraceCaps: Inline Provenance and Risk Enforcement for Agentic Software Engineering" が隣接する — [ICSE 2026 research track](https://conf.researchr.org/track/icse-2026/icse-2026-research-track)
- **MSR 2026**（175 題）: MCP の題は上の dataset の 1 件 — [MSR 2026 technical papers](https://conf.researchr.org/track/msr-2026/msr-2026-technical-papers)
- **SANER 2026**（140 題）: MCP の題は 0 件 — [SANER 2026](https://conf.researchr.org/track/saner-2026/saner-2026-papers)

#### (I3) 2026 年秋に公開された査読前の投稿（OpenReview、○ = 抄録）
- **ICLR 2027 投稿 "CPI: Contextual Prompt Injection against MCP Server Scanners"**: 「LLM-based MCP Server scanners … analyze … README files, tool descriptions, and code comments」。悪意あるメンテナが「修正済み」と主張する文脈を置くと、実装を変えなくても、三つの LLM 系スキャナのそれぞれで、ベースラインで陽性だったリポジトリの半数超で少なくとも 1 件の本物の発見が抑え込まれた（372 サーバ、うち 45 件は脆弱性が確認済み。著者の主張）— [OpenReview](https://openreview.net/forum?id=7TImfQIpSU)。**判定: 隣接**。ただし AuthGap の「判定に LLM を使わない」設計（宣言側として読むのは構造化注釈だけで、README やコメントは判定に入らない）を正当化する根拠として**引用価値が高い**。ContractGuard のような LLM 照合系への具体的な脅威にもなる。
- **ICLR 2027 投稿 "What Drives LLM Tool Selection in MCP? A Factor-Level Analysis Through Controlled Metadata Interventions"**: 367,174 の MCP ツールのメタデータを分析し、パラメータスキーマの違いが選択に最も効くと報告（著者の主張）— [OpenReview](https://openreview.net/forum?id=XwILZacNxz)。**判定: 隣接**。
- **ICLR 2027 投稿 "ProbeID: Verifying MCP Tool Identity for LLM Agents under Registry Drift"**: 説明文ではなく、プローブへの応答でツールの同一性を確かめる。「Over eleven weeks, 7 of 59 real tools changed responses despite version pins」（著者の主張）— [OpenReview](https://openreview.net/forum?id=FuarZrC0Ob)。**判定: 隣接**。
- ICML 2026 Position Track "Position: Trustworthy Model Context Protocol Enables Responsible Agentic AI!"（題のみ）— [OpenReview](https://openreview.net/forum?id=02sR3qKGMd)。KI 2026 AI4SE Workshop "Managing the Risks of Adopting the Model Context Protocol"（題のみ）— [OpenReview](https://openreview.net/forum?id=CzfHFuBKOD)

#### (I4) 採択一覧がまだ出ていない、または到達できなかった会議
- **ICSE 2027**: 投稿は 1 サイクルで、Notification は **2026-10-20**。今日（10-12）時点で採択一覧はない — [ICSE 2027 research track](https://conf.researchr.org/track/icse-2027/icse-2027-research-track)
- **IEEE S&P 2027**: accepted-papers ページはナビゲーションだけで、論文は載っていない — [S&P 2027](https://sp2027.ieee-security.org/accepted-papers.html)
- **NDSS 2027**: トップページに採択一覧へのリンクはない（`/ndss2027/accepted-papers/` は 2017 年のページに転送され、`accepted-papers-summer/` は 404）— [NDSS 2027](https://www.ndss-symposium.org/ndss2027/)
- **RAID 2026、ESORICS 2026、AsiaCCS 2026、EuroS&P 2026**: 推測した URL は 404 / 403 / タイムアウトで、採択一覧に**到達できなかった**。Web 検索でも MCP の採択論文は見つからなかった。
- **DBLP**（ボット確認ページ）と **Semantic Scholar API**（HTTP 429）は今回使えず、会議の横断検索はそれぞれの公式ページに頼った。

### Inferences
- arXiv にない（少なくとも検索で見つからない）、査読済みのトップ会議の論文として、ContractGuard は修士論文の関連研究の中心に据えるべき一件だと考える（推論）。AuthGap の差分は、ContractGuard の限界の節（Python や JS の間接呼び出しでスライスが欠け、誤りが両方向に出る）と、CPI（LLM 系スキャナが文脈の主張に引きずられる）によって、**外部から裏付けられる**形で書ける（推論）。
- ContractGuard の野外評価はツールの抽出が `os.walk` の走査順に依存し、LLM の温度も 0.2 なので、再実行で同じ結果になる保証がない。AuthGap の「SHA を固定した母集団・決定論・凍結」との対比点として具体的に書ける（推論。著者は再現性を主題にしていない）。
- 2026 年の SE / セキュリティ会議の採択題目で「構造化 ToolAnnotations とコードの照合」を正面から扱うものは見つからなかった。ただし ICSE 2027 の通知（10/20）と CCS 2026 の開催（11 月）の前後で状況が変わりうる（推論）。

### Gaps
- ContractGuard は「深さの上限」「未解決率」「言語別の内訳（Python が何割か）」を本文で確認しきれていない（読んでいない節がある）。成果物（github.com/psu-security-universe/contractguard）は GitHub MCP ツールを使わない制約があるため確認していない。
- Cosseter（S&P 2026）、"Governing AI Agent with Capability and Delegation Chain"（CCS 2026）、"Parasites in the Toolchain"（S&P 2026）は題しか見ていない。
- ICSE 2027 の採択一覧（10/20 以降）、NDSS 2027 の夏サイクル、S&P 2027 の第 1 サイクル、RAID / ESORICS / AsiaCCS / EuroS&P 2026 の採択一覧は未確認。
- NeurIPS 2026 / COLM 2026 / ACL 2026 のエージェント安全性ワークショップの採択一覧は、OpenReview の検索（ICLR 2027 の枠と全体の語検索）以外は見ていない。OpenReview の個別ノート API はチャレンジ（403）で拒否された。
- 検索の途中で、既知リストにない arXiv 候補が出てきたが、本文は未確認（arXiv 担当の班に回すべきもの）: FlowGuard（2607.14754、動的プローブ＋意味解析）、"Mitigating Taint-Style Vulnerabilities in MCP Servers via Security-Aware Tool Descriptions"（2607.07461、題のみ）、"Compatibility at a Cost: … MCP Clause-Compliance Vulnerabilities"（2603.10163、題のみ）、MCP-in-SoS（2603.10194、静的解析で CWE を検出）。

---

## 問 4: グレー文献（企業・団体の報告、技術ブログ、ツール）に、MCP の注釈の正しさをコードに照らして測ったものはあるか

### Takeaway
構造化注釈とコードの能力の矛盾を規則として持つ OSS スキャナ **mcpscan-cli（glatinone/mcpscan）の MCP013「Misleading tool annotation」** を見つけた。ただし評価や母集団での測定は示されていない。企業の報告（TrendAI / トレンドマイクロ、IPA / JPCERT）や国内の技術ブログでは、**注釈の正しさを母集団で測ったものは見つからなかった**。MCP 公式ブログ（2026-03-16）は注釈を「hint, not a guarantee」とし、検証の手段は示していない。

### Cited Findings
- **mcpscan-cli（PyPI、作者 glatinone、v0.19.1 は 2026-08-10、v0.20.0 は 2026-08-17）** — 検証 ○（PyPI に載った README を読んだ。コードは読んでいない）
  - MCP013「Misleading tool annotation」: 「A tool with a detected exec/filesystem-write/network/SQL capability that declares no `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint` at all, or claims `readOnlyHint: true`/`destructiveHint: false` while its own code calls that capability」。ロードマップには「Rule for MCP `ToolAnnotations` … missing or contradicted (MCP013, v0.9.0)」とある — [PyPI mcpscan-cli](https://pypi.org/project/mcpscan-cli/)、[GitHub glatinone/mcpscan](https://github.com/glatinone/mcpscan)
  - 「zero dependencies, zero network calls」、SARIF を出力する。テストは脆弱な fixture と clean な fixture で回している — [PyPI](https://pypi.org/project/mcpscan-cli/)
  - A1: **構造化注釈**（4 つの hint すべて）/ A2: 静的（規則ベース。具体的な方法は README に書かれていない）/ A3: 「its own code」とあり、呼び先を辿るかは不明 / A4: ツール自体は Python 製。対象言語は README では不明（Node の例もある）/ A5: 記載なし / A6: 母集団での評価も人手の正解もない / A7: 規則ベースなので決定的とみられる（推定）/ A8: なし。
  - **判定: 部分的に重なる** — 検査の定義は AuthGap の核とほぼ同じ（注釈が無い、または能力と矛盾する場合を指摘する）。ただし手続き間の到達、opaque の扱い、母集団での測定、精度の評価がない。HintLint や mcp-doctor（既知）と同じく「ツールとしての先行実装」に分類して引用すべきもの。
- **MCP 公式ブログ "Tool annotations"（2026-03-16、Ola Hungerford, Sam Morrow (GitHub), Luca Chang (AWS)）**: 「annotations are not guaranteed to faithfully describe tool behavior」「A server can claim `readOnlyHint: true` and delete your files anyway.」「They aren't enforcement.」。GitHub の read-only モードは約 17% のユーザが有効にしていると記載（著者の主張）。**注釈をコードや挙動と照合するツールや手法には触れていない** — [MCP blog](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)
- **TrendAI Research（トレンドマイクロ）「外部公開 MCP サーバの最新状況」（2026-04-28、Alfredo Oliveira, David Fiser。日本語訳あり）**: 外部公開された MCP サーバは 1,467 件（前回は 492 件）。「19,000件超の MCP サーバのソースコードを分析した結果、その半数近く（48%）が、安全性に欠ける .env ファイルや平文の JSON 構成にシークレットを保管することを推奨」（著者の主張）。**注釈とツールの説明の照合はない** — [TrendAI 日本語版](https://www.trendaisecurity.com/ja/resources-insights/deep-research/update-on-exposed-mcp-servers-the-threat-widens-to-the-cloud)
- **DevelopersIO（クラスメソッド）、著者 Yutaka Inoue（英訳版の表記。漢字は未確認）、GitHub MCP の Read-only モードの検証記事（2026-07-27）**: GitHub MCP サーバでは各ツールが `ReadOnlyHint` を宣言し、`IsReadOnly()` と `isToolEnabled` が read-only モードの**フィルタとして注釈を使っている**ことをコードの抜粋で示し、書き込みツール 1 つ（`create_repository`）が「unknown tool」で拒否されることを確認した。一方で、英訳版には "the concern that AI could use write tools if there were an implementation mistake cannot be fully dismissed" とも書かれている（日本語原文の文言は未確認）。すべてのツールについて注釈が正しいかは**検証していない** — [DevelopersIO（日本語原文）](https://dev.classmethod.jp/articles/github-mcp-read-only-mode-verification/)、[英訳版](https://dev.classmethod.jp/en/articles/github-mcp-read-only-mode-verification/)（英訳版を経由して確認、○）
- **lilting channel（いけさん）「MCPサーバー50件をスキャンした脆弱性監査」（2026-04-06）**: DEV Community の Atlas Whoff による 50 サーバのスキャン（MCP Security Scanner、22 規則）を紹介。入力検証の欠如 61%、コマンドインジェクションのリスク 43% など（元記事の主張の孫引き）。**注釈には触れていない** — [lilting.ch](https://lilting.ch/articles/mcp-server-50-scan-vulnerability-audit)（△）
- **azukiazusa「MCP のツールアノテーションでユーザーにヒントを提供する」**: 注釈は「あくまでヒントであり、MCP サーバーがツールの動作を保証するものではありません」と解説している。測定はしていない — [azukiazusa.dev](https://azukiazusa.dev/blog/mcp-tool-annotations)（○）
- **IPA / JPCERT/CC**: Web 検索では、MCP サーバのツール権限や注釈を扱う 2026 年の調査報告は見つからなかった。IPA の「情報セキュリティ10大脅威 2026」で AI 利用をめぐるリスクが初めて選ばれた、という報道はある — [ScanNetSecurity IPA 記事一覧 2026-02](https://scan.netsecurity.ne.jp/special/178/202602/%E7%8B%AC%E7%AB%8B%E8%A1%8C%E6%94%BF%E6%B3%95%E4%BA%BA+%E6%83%85%E5%A0%B1%E5%87%A6%E7%90%86%E6%8E%A8%E9%80%B2%E6%A9%9F%E6%A7%8B+%EF%BC%88IPA%EF%BC%89)（△）
- **技術誌**（Software Design 2026-04「Webサービス企業のためのMCPサーバー設計ガイド：AIの行動モデルと制約を意識したツール設計」、日経コンピュータ連載「MCPに考慮すべき3つのリスク」2026-04-02 など）: 題からは設計やリスクの解説で、測定ではないと判断した（本文は未読）— [CiNii（Software Design）](https://cir.nii.ac.jp/opensearch/all?q=MCP%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC&format=json&from=2025)、[CiNii（日経コンピュータ）](https://cir.nii.ac.jp/crid/1520589375755895040)

### Inferences
- GitHub 公式の MCP サーバが `ReadOnlyHint` を**サーバ側の強制（read-only モードのフィルタ）に使っている**という DevelopersIO の観察は、「注釈の誤りは UX の問題にとどまらず、権限の境界を直接左右する」という AuthGap の動機づけの具体例として使える（推論。一次確認は GitHub のコードで行うべき）。
- mcpscan-cli の MCP013 のように、同じ検査を規則として持つ実務ツールが 2026 年に増えている。AuthGap の学術的な差分は「検査の定義」ではなく「母集団での測定の設計（opaque の率、凍結、事前登録、人手の正解、修正コミットからの再現率）」に置くのが妥当だと考える（推論）。

### Gaps
- Trail of Bits、Wiz、Palo Alto Unit 42、Docker、Microsoft、Google、NTT、日立、富士通、LAC の各ブログを社ごとに個別検索することはしていない（横断的な Web 検索 2 回だけ）。注釈とコードの照合を母集団で測った企業の報告は、その範囲では見つからなかった。
- mcpscan-cli の MCP013 の実装（同じ関数内だけか、呼び先を辿るか、どの言語か）と誤検知率は未確認。GitHub のリポジトリは、GitHub MCP ツールを使わない制約のため、Web 経由でもまだ読んでいない。
- 日本語の技術誌記事（Software Design、日経コンピュータ）は本文を読んでいない。
