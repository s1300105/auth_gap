[← 付録 G-3 Microsoft と GitHub](appendix-g-3.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-5 OpenAI →](appendix-g-5.md)

---

# 付録 G-4 Anthropic（Claude）

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-4-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C04-01](#g-c04-anthropic-01) | Anthropic — Claude Connectors Directory（コネクタ掲載審査） | 規約・審査の指針 | 宣言を書くことを求める・確認を省く（自動で許可）・確認を求める・作者への書き方の案内 | [確認] |
| [C04-06](#g-c04-anthropic-06) | Anthropic — Claude Connectors Directory（コネクタ掲載審査） | 規約・審査の指針 | 作者への書き方の案内・その他 | [確認] |
| [C04-02](#g-c04-anthropic-02) | Anthropic — Claude connectors（MCP サーバ作者向けドキュメント） | 公式の文書 | 宣言を書くことを求める・作者への書き方の案内・表示（印・名前）・その他 | [確認] |
| [C04-03](#g-c04-anthropic-03) | Anthropic — Claude Connectors Directory（申請ポータル） | 規約・審査の指針 | 宣言を書くことを求める・宣言を検査する | [確認] |
| [C04-04](#g-c04-anthropic-04) | Anthropic — Claude Connectors Directory（申請ポータル） | 規約・審査の指針 | 表示（印・名前）・宣言を検査する | [確認] |
| [C04-05](#g-c04-anthropic-05) | Anthropic — Claude Connectors Directory（申請要件） | 規約・審査の指針 | 宣言を書くことを求める | [確認] |
| [C04-07](#g-c04-anthropic-07) | Anthropic — Anthropic Software Directory（Connectors / Plugins） | 規約・審査の指針 | 宣言を書くことを求める | [確認] |
| [C04-08](#g-c04-anthropic-08) | Anthropic — Claude Cowork（Team / Enterprise プラン） | 公式の文書 | 規則（ポリシー）の条件に使う・確認を求める・宣言が無いときの扱い | [確認] |
| [C04-09](#g-c04-anthropic-09) | Anthropic — Claude Cowork | 公式の文書 | 確認を省く（自動で許可）・危険度を付ける | [確認] |
| [C04-10](#g-c04-anthropic-10) | Anthropic — Claude（claude.ai / Desktop / Mobile）コネクタ | 公式の文書 | 表示（印・名前）・規則（ポリシー）の条件に使う | [確認] |
| [C04-11](#g-c04-anthropic-11) | Anthropic — Claude Desktop（changelog の「3P」節＝第三者クラウド向けの Claude Desktop） | リリースノート | 確認を求める・表示（印・名前） | [確認] |
| [C04-12](#g-c04-anthropic-12) | Anthropic — Claude Desktop on 3P（第三者クラウド向け Claude Desktop、MDM / bootstrap 設定） | 公式の文書 | 確認を求める・表示（印・名前） | [確認] |
| [C04-13](#g-c04-anthropic-13) | Anthropic — Claude Agent SDK（Python / TypeScript） | SDK の文書 | その他 | [確認] |
| [C04-14](#g-c04-anthropic-14) | Anthropic — Claude Agent SDK（Python / TypeScript） | SDK の文書 | その他・宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C04-15](#g-c04-anthropic-15) | Anthropic — Claude Agent SDK（Python / TypeScript） | SDK の文書 | その他・宣言が無いときの扱い | [確認] |
| [C04-16](#g-c04-anthropic-16) | Anthropic — Claude Agent SDK（Python / TypeScript） | SDK の文書 | 使わない・読まない・宣言が無いときの扱い | [確認] |
| [C04-17](#g-c04-anthropic-17) | Anthropic — Claude Agent SDK（Python / TypeScript） | SDK の文書 | 作者への書き方の案内・その他 | [確認] |
| [C04-18](#g-c04-anthropic-18) | Anthropic — Claude Agent SDK（Python） | SDK の文書 | 宣言が無いときの扱い・作者への書き方の案内 | [確認] |
| [C04-36](#g-c04-anthropic-36) | Anthropic — Claude Agent SDK（Python） | SDK の文書 | 信頼するなという注意 | [確認] |
| [C04-19](#g-c04-anthropic-19) | Anthropic — Claude Agent SDK（TypeScript） | SDK の文書 | 宣言が無いときの扱い・そのまま渡す・見せる・作者への書き方の案内 | [確認] |
| [C04-37](#g-c04-anthropic-37) | Anthropic — Claude Agent SDK（TypeScript） | SDK の文書 | 信頼するなという注意 | [確認] |
| [C04-20](#g-c04-anthropic-20) | Anthropic — Claude Agent SDK（TypeScript）— mcpServerStatus() | SDK の文書 | そのまま渡す・見せる | [確認] |
| [C04-21](#g-c04-anthropic-21) | Anthropic — claude-agent-sdk-python（ソース） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C04-22](#g-c04-anthropic-22) | Anthropic — claude-agent-sdk-python（ソース） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C04-23](#g-c04-anthropic-23) | Anthropic — claude-agent-sdk-python（ソース） | SDK のソースコード | その他 | [確認] |
| [C04-24](#g-c04-anthropic-24) | Anthropic — claude-agent-sdk-python | リリースノート | その他 | [確認] |
| [C04-25](#g-c04-anthropic-25) | Anthropic — claude-agent-sdk-python | リリースノート | そのまま渡す・見せる・作者への書き方の案内 | [確認] |
| [C04-26](#g-c04-anthropic-26) | Anthropic — claude-agent-sdk-typescript | リリースノート | そのまま渡す・見せる・作者への書き方の案内 | [確認] |
| [C04-27](#g-c04-anthropic-27) | Anthropic — Claude Code（CLI） | クライアントの文書 | 確認を求める・作者への書き方の案内 | [確認] |
| [C04-28](#g-c04-anthropic-28) | Anthropic — Claude Code（CLI） | リリースノート | 表示（印・名前） | [確認] |
| [C04-29](#g-c04-anthropic-29) | Anthropic — Anthropic Engineering blog | 公式ブログ | 作者への書き方の案内 | [確認] |
| [C04-30](#g-c04-anthropic-30) | Agent Client Protocol project（agentclientprotocol。Anthropic ではない） — claude-agent-acp（Claude Agent SDK を ACP に橋渡しするアダプタ） | issue / PR / 提案の下書き | そのまま渡す・見せる | [未確認] |
| [C04-31](#g-c04-anthropic-31) | Anthropic（anthropics/claude-code の issue。投稿者は利用者で、Anthropic の見解ではない） — Claude Code（CLI） | issue / PR / 提案の下書き | 使わない・読まない | [未確認] |
| [C04-32](#g-c04-anthropic-32) | Anthropic（anthropics/claude-code の issue。利用者の報告） — Claude Code（CLI）plan mode | issue / PR / 提案の下書き | 確認を求める・その他 | [未確認] |
| [C04-33](#g-c04-anthropic-33) | Anthropic（anthropics/claude-ai-mcp の issue。利用者の報告） — Claude Desktop（Auto 権限モード、ローカル MCP サーバ） | issue / PR / 提案の下書き | 確認を求める | [未確認] |
| [C04-34](#g-c04-anthropic-34) | Anthropic（anthropics/claude-code の issue。利用者の要望） — Claude Desktop | issue / PR / 提案の下書き | 確認を省く（自動で許可）・確認を求める | [未確認] |
| [C04-35](#g-c04-anthropic-35) | coreConvention（第三者の MCP サーバ johnny-five の issue） — Claude Code plan mode（第三者からの観察） | 第三者の記事 | 確認を求める・宣言が無いときの扱い | [未確認] |

この分冊の資料は 37 件で、うち [確認] は 31 件、[確認（調査時のみ）] は 0 件。

<a id="ag-4-1"></a>
## 資料カード

### Anthropic — Claude Connectors Directory（コネクタ掲載審査）

<a id="g-c04-anthropic-01"></a>
#### C04-01 Anthropic — Claude Connectors Directory（コネクタ掲載審査）

- **資料**: Connector pre-submission checklist（claude.com/docs/connectors/building/review-criteria）（規約・審査の指針）
- **URL**: https://claude.com/docs/connectors/building/review-criteria
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/review-criteria#provide-tool-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connector pre-submission checklist > Design tools that pass review > Provide tool annotations (#provide-tool-annotations)
- **原文**:

> Every tool must include a title and the applicable hint: readOnlyHint: true for read-only tools, and destructiveHint: true for tools that modify or delete data. These determine auto-permissions in Claude. Read-only tools can run without per-call confirmation, and destructive tools always prompt.

- **日本語**: すべてのツールは title と該当する hint（読み取り専用なら readOnlyHint: true、データを変更・削除するなら destructiveHint: true）を含めなければならない。これらが Claude での自動許可を決める。読み取り専用ツールは呼び出しごとの確認なしで動けて、破壊的ツールは必ず確認を求める。
- **どう使っているか**: Anthropic のディレクトリ審査基準（申請前チェックリスト）。title と readOnlyHint / destructiveHint の宣言を必須とし、その値が Claude の「自動許可（auto-permissions）」を決めると書く：readOnlyHint:true のツールは呼び出しごとの確認なしで実行「できる（can）」、destructiveHint:true のツールは「必ず（always）」確認を求める。宣言を確認の要否に使うと Anthropic 自身が書いた一次資料。ただし書いてあるのは審査ガイドの中の説明で、どの製品・モードで効くかの仕様ではない。
- **条件**: ディレクトリ掲載を申請するリモート MCP コネクタが対象。「Claude」のどの面（claude.ai / Desktop / Cowork / Claude Code）で、どのモード・設定のときにこの自動許可が効くかは、このページには書かれていない（不明）。ユーザーや管理者の Always allow / Needs approval / Blocked 設定との優先関係も、このページには書かれていない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint・title ／ **使い方の分類**: 宣言を書くことを求める・確認を省く（自動で許可）・確認を求める・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connector pre-submission checklist > Design tools that pass review > Provide tool annotations」（取得 2026-10-02T22:11:21Z、sha256 d7924994b721…）
- **補足**: 同じ節「Design tools that pass review」には「Separate read and write tools」（C04_anthropic-06）がある。destructiveHint の説明「tools that modify or delete data」は MCP 仕様（destructiveHint は readOnlyHint=false のときだけ意味を持ち、破壊的でない追加的な更新は false）より広い。readOnlyHint:false・destructiveHint:false（破壊的でない書き込み）のツールがどう扱われるかは書かれていない（不明）。宣言が実装と違う場合（嘘の readOnlyHint）にどうなるかも書かれていない。必須の範囲の書き方は Anthropic のページ間で揃っていない：ここは「the applicable hint」、C04_anthropic-02 は「both」、C04_anthropic-03 / 05 は「readOnlyHint or destructiveHint」。 location / anchored_url を修正。verify_quote.py は文字の正規化（… → ...、ゼロ幅文字の削除）をした後の位置で見出し・行番号を引くため、正規化で長さが変わる文字が前にあると位置がずれる（このページでは ゼロ幅文字 15 個）。正規化前の位置に戻して引き直した結果（scratchpad の annot/v04/headfix.py・lines.py）を location に書いた。tool の生の出力は「Connector pre-submission checklist > Design tools that pass review > Reference API docs in custom query tools #reference-api-docs-in-custom-query-tools」。 正しい見出しの id はページの HTML に id="provide-tool-annotations" として 1 つあることを確認。 usage_ja の「呼び出しごとの確認なしで実行可」は原文の can（できる）どおりだが、「宣言が直接確認の要否に使われる」を製品仕様のように読める書き方だったので、審査ガイド内の説明であることを足した。notes の見出しの推定（#provide-tool-annotations）は引き直しで確定したのでnotes から外し、destructiveHint の定義が MCP 仕様より広いこと・必須範囲の表現がページ間で食い違うことを足した。

<a id="g-c04-anthropic-06"></a>
#### C04-06 Anthropic — Claude Connectors Directory（コネクタ掲載審査）

- **資料**: Connector pre-submission checklist — Separate read and write tools（規約・審査の指針）
- **URL**: https://claude.com/docs/connectors/building/review-criteria
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/review-criteria#separate-read-and-write-tools
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connector pre-submission checklist > Design tools that pass review > Separate read and write tools (#separate-read-and-write-tools)
- **原文**:

> A single tool that accepts both safe HTTP methods, such as GET, HEAD, and OPTIONS, and unsafe methods, such as POST, PUT, PATCH, and DELETE, is rejected.

- **日本語**: 安全な HTTP メソッド（GET, HEAD, OPTIONS など）と安全でないメソッド（POST, PUT, PATCH, DELETE など）の両方を受け付ける 1 つのツールは却下される。
- **どう使っているか**: 宣言そのものではなく「宣言が一つに決まるようにツールを分けよ」という審査規則。method 引数で読み書きを切り替える万能 api_request ツールは却下され、読み取り専用ツールと書き込みツールに分割を求める。readOnlyHint を 1 ツール 1 値で正しく付けられる前提を作る規則と読める。
- **条件**: ディレクトリ審査。説明文に安全/危険な操作を書き分けるだけでは不可（同節）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connector pre-submission checklist > Design tools that pass review > Separate read and write tools」（取得 2026-10-02T22:11:21Z、sha256 d7924994b721…）
- **補足**: 同節の次の文「Split a catch-all tool into a read-only tool and one or more write tools.」も verify_quote.py で exact（同じ取得）。引用文は hint 名を含まない。hints の readOnlyHint は同ページ「Provide tool annotations」（C04_anthropic-01）と組で読んだときの対応で、引用自体の語ではない。AuthGap の「HTTP メソッド」類の矛盾判定と直接対応する規則。

### Anthropic — Claude connectors（MCP サーバ作者向けドキュメント）

<a id="g-c04-anthropic-02"></a>
#### C04-02 Anthropic — Claude connectors（MCP サーバ作者向けドキュメント）

- **資料**: Model Context Protocol (MCP)（claude.com/docs/connectors/building/mcp）（公式の文書）
- **URL**: https://claude.com/docs/connectors/building/mcp
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/mcp#tool-hints
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Model Context Protocol (MCP) > Security model > Tool hints (#tool-hints)
- **原文**:

> All MCP tools must declare both of these annotations: readOnlyHint: the tool only reads data destructiveHint: the tool can modify or delete data Claude and users read these hints to understand what actions a tool can take.

- **日本語**: すべての MCP ツールは次の 2 つの annotations を両方宣言しなければならない：readOnlyHint（データを読むだけ）、destructiveHint（データを変更・削除しうる）。Claude と利用者は、ツールが何をしうるかを知るためにこの hint を読む。
- **どう使っているか**: Claude 向けコネクタを作る人への説明。readOnlyHint と destructiveHint の両方の宣言を「must」とする。用途は「Claude（モデル）と利用者が読む」——つまりモデルへの入力と人への表示。確認の要否への使用はこのページでは言っていない（C04_anthropic-01 が言う）。
- **条件**: 見出しは「Security model > Tool hints」（引き直しで確定）。対象はディレクトリ向けに限らず Claude 用コネクタ全般の書き方として書かれている。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める・作者への書き方の案内・表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > Security model > Tool hints」（取得 2026-10-02T22:11:21Z、sha256 f849f14e43a0…）
- **補足**: ここでの destructiveHint の説明は「the tool can modify or delete data」で、MCP 仕様（readOnlyHint=false のときだけ意味を持つ）より広い言い方。「both」を must とする点は、申請ページ（C04_anthropic-03 / 05 の「readOnlyHint or destructiveHint」）・審査基準（C04_anthropic-01 の「the applicable hint」）と食い違う。display_label は「users read these hints」からの読みで、どの画面に出すかはこのページに書かれていない（不明）。 location / anchored_url を修正。verify_quote.py は文字の正規化（… → ...、ゼロ幅文字の削除）をした後の位置で見出し・行番号を引くため、正規化で長さが変わる文字が前にあると位置がずれる（このページでは ゼロ幅文字 9 個）。正規化前の位置に戻して引き直した結果（scratchpad の annot/v04/headfix.py・lines.py）を location に書いた。tool の生の出力は「Model Context Protocol (MCP) > Security model > User control #user-control」。 正しい見出しの id はページの HTML に id="tool-hints" として 1 つあることを確認。 conditions / notes の見出し推定（llms-full.txt から）を、引き直しで確定した見出しに置き換え。ページ間の必須範囲の食い違いを notes に追加。

### Anthropic — Claude Connectors Directory（申請ポータル）

<a id="g-c04-anthropic-03"></a>
#### C04-03 Anthropic — Claude Connectors Directory（申請ポータル）

- **資料**: Submit a connector to the directory（claude.com/docs/connectors/building/submission）（規約・審査の指針）
- **URL**: https://claude.com/docs/connectors/building/submission
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/submission#pre-submission-checklist-for-connectors
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Submit a connector to the directory > Pre-submission checklist for connectors (#pre-submission-checklist-for-connectors)
- **原文**:

> Every tool has a title and a readOnlyHint or destructiveHint annotation: the portal flags tools that are missing them

- **日本語**: すべてのツールが title と、readOnlyHint か destructiveHint の annotation を持っていること：ポータルは、それが欠けているツールに印を付ける。
- **どう使っているか**: 申請前チェックリスト。開発者ポータルが title / readOnlyHint / destructiveHint の欠落を自動で検出して印を付ける（宣言の有無のリント）。値が実装と合っているかの検査ではない。
- **条件**: ディレクトリ申請時（developer portal）。値の正しさは人の審査（review criteria）で見るとされ、自動の照合があるかは書かれていない（不明）。
- **扱う宣言**: title・readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Submit a connector to the directory > Pre-submission checklist for connectors」（取得 2026-10-02T22:11:21Z、sha256 7f41858dbd81…）
- **補足**: 同ページ「Requirements for every connector」にも同趣旨の必須要件がある（C04_anthropic-05）。 解釈は原文どおり（変更なし）。「readOnlyHint or destructiveHint」は片方で足りる書き方で、C04_anthropic-02 の「both」と食い違う（02 の notes に記録）。

<a id="g-c04-anthropic-04"></a>
#### C04-04 Anthropic — Claude Connectors Directory（申請ポータル）

- **資料**: Submit a connector to the directory — Submit through the developer portal（Tools ステップ）（規約・審査の指針）
- **URL**: https://claude.com/docs/connectors/building/submission
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/submission#submit-through-the-developer-portal
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Submit a connector to the directory > Submit through the developer portal (#submit-through-the-developer-portal)
- **原文**:

> Your server's tools, prompts, and resources sync automatically from the connected server, grouped by whether their annotations declare them read-only or write. If any tools are flagged for missing titles or annotations, fix them on your server before submitting.

- **日本語**: サーバのツール・プロンプト・リソースは接続先から自動で同期され、annotations が読み取り専用と宣言しているか書き込みかで分けて表示される。title や annotations が欠けているとして印の付いたツールがあれば、申請前にサーバ側で直すこと。
- **どう使っているか**: ポータルは tools/list を同期し、annotations の宣言に基づいてツールを「read-only」と「write」に分けて表示する。欠落は印付けされ、申請前の修正を求める。宣言をそのまま分類ラベルに使う例。
- **条件**: 開発者ポータルの申請フロー（Connection → Tools → Listing …）の Tools ステップ。
- **扱う宣言**: readOnlyHint・title・宣言全般 ／ **使い方の分類**: 表示（印・名前）・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Submit a connector to the directory > Submit through the developer portal」（取得 2026-10-02T22:11:21Z、sha256 7f41858dbd81…）
- **補足**: tool の位置は「Submit through the developer portal」節。どの annotation の値で read-only/write に振り分けるか（readOnlyHint だけか、destructiveHint も見るか）は書かれていない（不明）。

### Anthropic — Claude Connectors Directory（申請要件）

<a id="g-c04-anthropic-05"></a>
#### C04-05 Anthropic — Claude Connectors Directory（申請要件）

- **資料**: Submit a connector to the directory — Requirements for every connector（規約・審査の指針）
- **URL**: https://claude.com/docs/connectors/building/submission
- **書いてある見出しへ直接**: https://claude.com/docs/connectors/building/submission#requirements-for-every-connector
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Submit a connector to the directory > Meet the submission requirements > Requirements for every connector (#requirements-for-every-connector)
- **原文**:

> Tool annotations: every tool includes a title and the applicable readOnlyHint or destructiveHint

- **日本語**: Tool annotations：すべてのツールが title と、該当する readOnlyHint または destructiveHint を含むこと。
- **どう使っているか**: ディレクトリ掲載の必須要件（Security / Authentication / Privacy / Documentation と並ぶ 5 項目の一つ）として annotations を挙げる。
- **条件**: ディレクトリに掲載されるすべての MCP コネクタ。
- **扱う宣言**: title・readOnlyHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Submit a connector to the directory > Meet the submission requirements > Requirements for every connector」（取得 2026-10-02T22:11:21Z、sha256 7f41858dbd81…）
- **補足**: 同じ節の前文：「Every connector in the directory must comply with the directory terms and meet a fixed set of security, annotation, authentication, privacy, and documentation requirements.」（検証者が verify_quote.py で exact を確認。tool の見出しは 「Choose where to submit your connector」だが、引き直すと「Meet the submission requirements」(#meet-the-submission-requirements)）。 notes の前文の引用は finder が「tool 未実行」としていたので検証者が実行し exact を確認した。

### Anthropic — Anthropic Software Directory（Connectors / Plugins）

<a id="g-c04-anthropic-07"></a>
#### C04-07 Anthropic — Anthropic Software Directory（Connectors / Plugins）

- **資料**: Anthropic Software Directory Policy（support.claude.com 13145358）（規約・審査の指針）
- **URL**: https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy
- **書いてある見出しへ直接**: https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy#h_9fdb5d0031
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: 5. Additional Requirements for Model Context Protocol Servers (#h_9fdb5d0031)
- **原文**:

> MCP servers must provide all applicable annotations for their tools, in particular readOnlyHint, destructiveHint, and title.

- **日本語**: MCP サーバは、ツールに該当するすべての annotations を付けなければならない。特に readOnlyHint、destructiveHint、title。
- **どう使っているか**: ディレクトリ掲載の規約（Policy）本体での義務づけ。リンク先は MCP 仕様 2025-11-25 の ToolAnnotations。用途（確認の要否など）はこの規約には書かれていない。
- **条件**: Anthropic Software Directory に掲載される MCP サーバ（節「5. Additional Requirements for Model Context Protocol Servers」の項目 E）。
- **扱う宣言**: readOnlyHint・destructiveHint・title・宣言全般 ／ **使い方の分類**: 宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「5. Additional Requirements for Model Context Protocol Servers」（取得 2026-10-02T22:11:38Z、sha256 e811f8dbf6ec…）
- **補足**: 公開ページは HTML（support.claude.com）。.md 版（URL 末尾 .md）でも同じ文を grep で確認（tool は HTML で実行）。 「リンク先は MCP 仕様 2025-11-25 の ToolAnnotations」を HTML で確認（href=https://modelcontextprotocol.io/specification/2025-11-25/schema#toolannotations）。変更なし。

### Anthropic — Claude Cowork（Team / Enterprise プラン）

<a id="g-c04-anthropic-08"></a>
#### C04-08 Anthropic — Claude Cowork（Team / Enterprise プラン）

- **資料**: Use Claude Cowork on Team and Enterprise plans（support.claude.com 13455879）— Connector tool approvals（公式の文書）
- **URL**: https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans
- **書いてある見出しへ直接**: https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans#h_1bd1fa754d
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Use Claude Cowork on Team and Enterprise plans > Admin controls > Connector tool approvals (#h_1bd1fa754d)
- **原文**:

> Read-only tools are exempt only when the connector annotates them as read-only. Most custom connectors don't annotate their tools, so every tool on those connectors is gated.

- **日本語**: 読み取り専用ツールが（この設定によるしばり＝書き込みツールにタスクごとの承認を課すこと）から外れるのは、コネクタがそれを読み取り専用とannotate しているときだけ。多くのカスタムコネクタはツールに annotation を付けていないので、そうしたコネクタのツールはすべてしばりの対象になる。
- **どう使っているか**: Cowork の組織設定「Allow "Always allow" for connector tools」（既定 off）が off のとき、書き込み可能なコネクタツールには「Allow for all tasks」が灰色になり、保存済みの always-allow も無視され、タスクごとの承認が要る。このしばりから外れるのは annotation でread-only と宣言されたツールだけ。宣言が無いと全ツールがしばりの対象（欠落時は安全側）。つまり annotation は「どのツールにこの承認のしばりを掛けるか」の判定に使われる。read-only と宣言したツールが確認なしで走るかどうかは、組織のツール方針・ロールの付与・利用者の Always allow / Needs approval の選択による（このページは自動承認するとは書いていない）。
- **条件**: Cowork、Team / Enterprise プラン、組織設定「Allow "Always allow" for connector tools」が off（既定）のとき。この設定が on なら書き込みツールにも Always allow が使える。Enterprise ではカスタムロールの付与と重なり、最も厳しい層が勝つ（ロールの付与ではこの設定を覆せない）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Use Claude Cowork on Team and Enterprise plans > Admin controls > Connector tool approvals」（取得 2026-10-02T22:11:40Z、sha256 d9e16d004429…）
- **補足**: 「annotates them as read-only」が readOnlyHint を指すかは明記なし（ほぼ確実だが語としては不明）。同じ設定の説明は support 13930452（Manage custom roles on Enterprise plans > Connector permissions > Cowork approval setting for write tools, #h_85bd7c30e9）：「Claude Cowork has a separate organization setting, Allow "Always allow" for connector tools, that gates write-capable connector tools.」（verify_quote.py exact）。同ページは、組織方針もロールの付与も「Always allow」でも、この設定が on になるまで書き込みツールはタスクごとに承認、と書く。宣言が嘘（readOnlyHint:true なのに書き込む）の場合、このしばりを抜けるので、利用者や組織が Always allow を選んでいれば承認なしで書き込みが走りうる——AuthGap の D1 の矛盾が実害に結びつく経路。 usage から auto_approve を外し policy_rule_input を足した。原文の「exempt」は「書き込みツールにタスクごとの承認を強いるしばりから外れる」という意味で（同節の前の箇条と support 13930452 の説明から）、read-only と宣言したツールを自動承認するとは書いていない。finder の usage_ja / quote_ja は「承認の免除」と読めて過大だった。

### Anthropic — Claude Cowork

<a id="g-c04-anthropic-09"></a>
#### C04-09 Anthropic — Claude Cowork

- **資料**: Get started with Claude Cowork（support.claude.com 13345190）— Choose how Claude checks with you（公式の文書）
- **URL**: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- **書いてある見出しへ直接**: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork#h_c274f6c9b5
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Get started with Claude Cowork > Choose how Claude checks with you (#h_c274f6c9b5)
- **原文**:

> Read-only tools are approved For write/delete tools, Claude decides

- **日本語**: （Auto モード × コネクタのツール権限「Always allow」の欄）読み取り専用ツールは承認される。書き込み／削除ツールは Claude が判断する。
- **どう使っているか**: Cowork のモード表。Auto（Automatically approve）モードで、ユーザーがツール権限を「Always allow」にしたとき：読み取り専用ツールはそのまま承認、書き込み／削除ツールは Claude の安全チェック（各操作を審査）に回る。読み取り専用か否かで自動承認と分類器審査が分かれる。
- **条件**: Cowork の Auto（Automatically approve）モードかつコネクタのツール権限が「Always allow」のときだけ。Auto でも「Needs approval」なら読み取り専用か否かに関係なく Claude が判断する。Manual モードでは Always allow なら承認、Needs approval なら確認、Blocked なら拒否で、読み取り専用か否かで分けない。Skip モードは Blocked 以外すべて承認。Team / Enterprise では管理者が Auto を無効にでき、書き込みツールにタスクごとの承認を課す設定（C04_anthropic-08）があると Always allow が効かないことがある（同ページの Note）。new Claude experience では選べるのは Auto と Manual（既定）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Get started with Claude Cowork > Choose how Claude checks with you」（取得 2026-10-02T22:11:46Z、sha256 e30f15ed7821…）
- **補足**: 引用は表のセル（HTML の <br> で 2 文に分かれる）。このページは「読み取り専用」の判定根拠を書かない（annotations の語は none、checked_no_mention 参照）。根拠は C04_anthropic-08（annotation で read-only と宣言されたもの）から推定。 解釈は原文どおり。conditions に「Auto でも Needs approval なら区別しない」「管理者設定で Always allow が効かないことがある」を足した。

### Anthropic — Claude（claude.ai / Desktop / Mobile）コネクタ

<a id="g-c04-anthropic-10"></a>
#### C04-10 Anthropic — Claude（claude.ai / Desktop / Mobile）コネクタ

- **資料**: Use connectors to extend Claude's capabilities（support.claude.com 11176164）— Restrict actions within connected services（公式の文書）
- **URL**: https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- **書いてある見出しへ直接**: https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities#h_9fa8289074
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Use connectors to extend Claude's capabilities > Connect a service on Team and Enterprise plans > Restrict actions within connected services (#h_9fa8289074)
- **原文**:

> The permissions will be categorized by type (for example, read-only tools, write/delete tools).

- **日本語**: 権限は種類ごとに分類される（たとえば、読み取り専用ツール、書き込み／削除ツール）。
- **どう使っているか**: Customize > Connectors の Tool permissions で、ツールが「read-only tools」「write/delete tools」の分類で表示され、分類単位または個別に Always allow / Needs approval / Blocked を選べる。分類がそのまま権限設定の単位になる。
- **条件**: Team / Enterprise の Owner が組織全体に掛ける「Restrict actions within connected services」の手順として書かれている（個人の利用者は上書きできない）。個人プランでも同じ分類が出るかはこのページからは不明。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 表示（印・名前）・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Use connectors to extend Claude's capabilities > Connect a service on Team and Enterprise plans > Restrict actions within connected services」（取得 2026-10-02T22:11:38Z、sha256 7a4e1afeee37…）
- **補足**: このページは分類の根拠（annotations）を書かない（checked_no_mention 参照）。開発者ポータルが「annotations が read-only か write かで分けて」表示する（C04_anthropic-04）ので、同じ根拠と推定されるが、利用者側 UI について明記した一次資料は見つからない（不明）。claude.com/docs/connectors/getting-started にも「choose Always allow, Needs approval, or Blocked for each group of tools or for a single tool」（verify_quote.py exact, #manage-or-disconnect-a-connector）。 conditions を明確化：この分類 UI は Team / Enterprise の Owner による組織全体の制限の手順として書かれている。

### Anthropic — Claude Desktop（changelog の「3P」節＝第三者クラウド向けの Claude Desktop）

<a id="g-c04-anthropic-11"></a>
#### C04-11 Anthropic — Claude Desktop（changelog の「3P」節＝第三者クラウド向けの Claude Desktop）

- **資料**: Cowork changelog（claude.com/docs/cowork/changelog）（リリースノート）
- **URL**: https://claude.com/docs/cowork/changelog
- **書いてある見出しへ直接**: https://claude.com/docs/cowork/changelog#page-title
- **版**: v2.9939.2（2026-09-24）
- **書いてある場所**: Changelog (#page-title)
- **原文**:

> Fixed read-only tools from managed and built-in MCP servers showing the approval warning meant for tools that can modify data; they now offer "Always allow" unless mcpPersistentAlwaysAllowEnabled is false.

- **日本語**: 管理（managed）や組み込みの MCP サーバの読み取り専用ツールに、データを変更しうるツール向けの承認警告が出ていた不具合を修正。これらは mcpPersistentAlwaysAllowEnabled が false でない限り「Always allow」を提示するようになった。
- **どう使っているか**: Desktop の承認プロンプトは、読み取り専用ツールには永続の「Always allow」を、データを変更しうるツールには警告つきの別の選択肢を出す。読み取り専用か否かで承認 UI の選択肢と警告表示が変わる。
- **条件**: v2.9939.2（2026-09-24）の「3P」節の項目。managed / built-in MCP サーバのツール。管理設定 mcpPersistentAlwaysAllowEnabled（既定 true）が false なら永続の Always allow は出ない。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Changelog」（取得 2026-10-02T22:11:21Z、sha256 54eac8775f67…）
- **補足**: tool の位置はページ先頭（#page-title）。版は llms-full.txt の <Update label="v2.9939.2" description="2026-09-24"> から。「read-only tools」の判定が annotations によるかは書かれていない（不明）。 llms-full.txt で、この項目が v2.9939.2 の「**3P**」節にあることを確認。product / conditions を 3P に限定した（finder は「Cowork / 3P」）。

### Anthropic — Claude Desktop on 3P（第三者クラウド向け Claude Desktop、MDM / bootstrap 設定）

<a id="g-c04-anthropic-12"></a>
#### C04-12 Anthropic — Claude Desktop on 3P（第三者クラウド向け Claude Desktop、MDM / bootstrap 設定）

- **資料**: Configuration reference — Connectors > MCP（claude.com/docs/third-party/claude-desktop/configuration）（公式の文書）
- **URL**: https://claude.com/docs/third-party/claude-desktop/configuration
- **書いてある見出しへ直接**: https://claude.com/docs/third-party/claude-desktop/configuration#mcp
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Configuration reference > Connectors > MCP (#mcp)
- **原文**:

> Tools not listed follow the user's choice: the prompt offers a persistent Always allow, except for tools that can modify data, which show a session-scoped Allow for this task alongside Allow for all tasks with a malicious-instruction warning.

- **日本語**: （toolPolicy に）載っていないツールは利用者の選択に従う：プロンプトは永続の Always allow を出すが、データを変更しうるツールは例外で、セッション限りの「Allow for this task」と「Allow for all tasks」を、悪意ある指示への警告つきで出す。
- **どう使っているか**: 管理者の toolPolicy（blocked / ask / allow をツール名で固定）が無いツールでは、データを変更しうるかどうかで承認プロンプトの選択肢が変わる（変更しうる→タスク単位の許可＋警告、そうでない→永続 Always allow）。toolPolicy はツール名で指定し、annotations は使わない。
- **条件**: managedMcpServers の toolPolicy に載っていないツール。mcpPersistentAlwaysAllowEnabled（既定 true、1.24012.9 で追加）が false なら永続の選択肢は隠れる（同ページ、verify_quote.py exact で確認）。Code タブでは blocked / ask だけが Claude Code の権限規則として渡る。 Code タブでは mcpPersistentAlwaysAllowEnabled は効かない（「Code tab: mcpPersistentAlwaysAllowEnabled has no effect.」verify_quote.py exact）。mcpPersistentAlwaysAllowEnabled の説明「Offer the persistent "Always allow" approval options for MCP tools. ... Defaults to true.」も exact で確認。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Configuration reference > Connectors > MCP」（取得 2026-10-02T22:11:21Z、sha256 651f82db3d92…）
- **補足**: 「tools that can modify data」の判定方法（annotations か）はこのページに書かれていない（不明）。 usage から policy_rule_input を外した。toolPolicy はツール名で引く規則で、annotations（データを変更しうるか）は入力にならない（finder 自身の usage_ja もそう書いている）。conditions に Code タブでは効かないことを足した。

### Anthropic — Claude Agent SDK（Python / TypeScript）

<a id="g-c04-anthropic-13"></a>
#### C04-13 Anthropic — Claude Agent SDK（Python / TypeScript）

- **資料**: How the agent loop works — Parallel tool execution（code.claude.com/docs/en/agent-sdk/agent-loop）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/agent-loop
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/agent-loop#parallel-tool-execution
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: How the agent loop works > Tool execution > Parallel tool execution (#parallel-tool-execution)
- **原文**:

> Read-only tools (like Read, Glob, Grep, and MCP tools marked as read-only) can run concurrently. Tools that modify state (like Edit, Write, and Bash) run sequentially to avoid conflicts.

- **日本語**: 読み取り専用ツール（Read, Glob, Grep、および読み取り専用と印を付けた MCP ツール）は並行して実行できる。状態を変えるツール（Edit, Write, Bash）は衝突を避けるため順に実行する。
- **どう使っているか**: readOnlyHint を「並列実行してよいか」の判定に使う（実行スケジューリング）。確認の要否ではない。MCP ツールにも適用されると明記。
- **条件**: Agent SDK（＝Claude Code をライブラリとして動かす）で、1 ターンに複数のツール呼び出しが来たとき。並列数の上限は環境変数 CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY（「Maximum number of read-only tools and subagents that can execute in parallel (default: 10)」、https://code.claude.com/docs/en/env-vars#variables、verify_quote.py exact）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「How the agent loop works > Tool execution > Parallel tool execution」（取得 2026-10-02T22:11:21Z、sha256 89df9b79e444…）
- **補足**: この文は「MCP tools marked as read-only」と書くだけで readOnlyHint の語は出さない（次の文が custom tool について readOnlyHint を名指す）。Claude Code の CLI 側ドキュメント（mcp / permissions / permission-modes）は readOnlyHint に触れない（checked_no_mention）。この並列化が対話型 CLI でも同じかは SDK ページからは断定できない（SDK は CLI を内部で動かすので同じと推定、不明）。宣言が嘘なら、書き込みツールが並列に走り競合しうる。 conditions の env-vars の記述は finder が「tool 未実行」だったので検証者が実行し exact を確認。MCP ツールについての文は readOnlyHint を名指ししていないことを notes に明記。

<a id="g-c04-anthropic-14"></a>
#### C04-14 Anthropic — Claude Agent SDK（Python / TypeScript）

- **資料**: How the agent loop works — Parallel tool execution（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/agent-loop
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/agent-loop#parallel-tool-execution
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: How the agent loop works > Tool execution > Parallel tool execution (#parallel-tool-execution)
- **原文**:

> Custom tools default to sequential execution. To enable parallel execution for a custom tool, set readOnlyHint in its annotations.

- **日本語**: カスタムツールの既定は順次実行。カスタムツールを並列実行させるには、その annotations に readOnlyHint を設定する。
- **どう使っているか**: 宣言が無い（readOnlyHint 未設定）ときの既定は「順次実行」＝安全側。並列にしたい作者は readOnlyHint を付ける。
- **条件**: SDK の in-process カスタムツール（create_sdk_mcp_server / createSdkMcpServer）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「How the agent loop works > Tool execution > Parallel tool execution」（取得 2026-10-02T22:11:21Z、sha256 89df9b79e444…）
- **補足**: 直後の文「Both the TypeScript and Python SDKs use this field name from the MCP SDK.」

<a id="g-c04-anthropic-15"></a>
#### C04-15 Anthropic — Claude Agent SDK（Python / TypeScript）

- **資料**: Give Claude custom tools — Add tool annotations（code.claude.com/docs/en/agent-sdk/custom-tools）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/custom-tools
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/custom-tools#add-tool-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Give Claude custom tools > Create a custom tool > Add tool annotations (#add-tool-annotations)
- **原文**:

> Tool does not modify its environment. Controls whether the tool can be called in parallel with other read-only tools.

- **日本語**: （readOnlyHint の行、既定 false）ツールは環境を変更しない。他の読み取り専用ツールと並列に呼べるかどうかを制御する。
- **どう使っているか**: hint ごとの効き目の表。readOnlyHint（既定 false）は、他の読み取り専用ツールと並列に呼べるかを制御する。この表で効き目が書かれているのはreadOnlyHint だけで、他の 3 つは「Informational only」（C04_anthropic-16）。確認の要否に使うとはこのページは書いていない。
- **条件**: Agent SDK のカスタムツール（tool() ヘルパ / @tool デコレータの annotations 引数）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Give Claude custom tools > Create a custom tool > Add tool annotations」（取得 2026-10-02T22:11:21Z、sha256 ca696bd3698b…）
- **補足**: 同ページ Quick reference 表「Let Claude call tools in parallel」の行：「Set readOnlyHint: true on tools with no side effects.」（verify_quote.py exact, #quick-reference）。 usage_ja の「唯一の効き目のある hint」を「この表で効き目が書かれているのは readOnlyHint だけ」に弱めた（ページが言うのは表の中の記述だけ）。notes の Quick reference の引用は再実行で exact（#quick-reference）。

<a id="g-c04-anthropic-16"></a>
#### C04-16 Anthropic — Claude Agent SDK（Python / TypeScript）

- **資料**: Give Claude custom tools — Add tool annotations（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/custom-tools
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/custom-tools#add-tool-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Give Claude custom tools > Create a custom tool > Add tool annotations (#add-tool-annotations)
- **原文**:

> destructiveHint true Tool may perform destructive updates. Informational only. idempotentHint false Repeated calls with the same arguments have no additional effect. Informational only. openWorldHint true Tool reaches systems outside your process. Informational only.

- **日本語**: destructiveHint（既定 true）：破壊的な更新をしうる。情報としてだけ。idempotentHint（既定 false）：同じ引数で繰り返しても追加の効果がない。情報としてだけ。openWorldHint（既定 true）：プロセスの外のシステムに届く。情報としてだけ。
- **どう使っているか**: destructiveHint / idempotentHint / openWorldHint は「Informational only」と書かれている——SDK の実行時の挙動（並列化など）を変えないという読み。既定値（true / false / true）も示す。
- **条件**: Agent SDK のカスタムツールについての記述。claude.ai / Cowork 側の扱い（C04_anthropic-01, 08）とは別。
- **扱う宣言**: destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: 使わない・読まない・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Give Claude custom tools > Create a custom tool > Add tool annotations」（取得 2026-10-02T22:11:21Z、sha256 ca696bd3698b…）
- **補足**: 表の行を空白で連結した文字列として HTML 本文に一致（exact）。「Informational only」は SDK（Claude Code）が実行時に使わないという意味で、モデルや他の MCP クライアントに渡るかは別（C04_anthropic-22：SDK は annotations を tools/list にそのまま載せる）。 「Informational only」は何に対して情報なのか（モデルか、表示か）を書いていない。usage_ja の「SDK の挙動を変えない」は読みであることを明記した。

<a id="g-c04-anthropic-17"></a>
#### C04-17 Anthropic — Claude Agent SDK（Python / TypeScript）

- **資料**: Give Claude custom tools — Add tool annotations（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/custom-tools
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/custom-tools#add-tool-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Give Claude custom tools > Create a custom tool > Add tool annotations (#add-tool-annotations)
- **原文**:

> Annotations are metadata, not enforcement. A tool marked readOnlyHint: true can still write to disk if that's what the handler does. Keep the annotation accurate to the handler.

- **日本語**: annotations はメタデータであって強制ではない。readOnlyHint: true と印を付けたツールでも、ハンドラがそうするならディスクに書き込める。annotation はハンドラの実際の動きに合わせておくこと。
- **どう使っているか**: 宣言は実装を縛らない（SDK は宣言と実装の一致を検査・強制しない）と明言し、作者に一致を保つよう求める。宣言と実装のずれ（AuthGap の対象）を SDK は防がない、という一次資料。
- **条件**: Agent SDK のカスタムツール。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 作者への書き方の案内・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Give Claude custom tools > Create a custom tool > Add tool annotations」（取得 2026-10-02T22:11:21Z、sha256 ca696bd3698b…）
- **補足**: Anthropic の文書の中で、宣言が実装を縛らないことを最もはっきり書いた箇所。

### Anthropic — Claude Agent SDK（Python）

<a id="g-c04-anthropic-18"></a>
#### C04-18 Anthropic — Claude Agent SDK（Python）

- **資料**: Agent SDK reference - Python — tool() > ToolAnnotations（code.claude.com/docs/en/agent-sdk/python）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/python
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/python#toolannotations
- **版**: 2026-10-02 取得（Python SDK 0.2.140 以降の記述を含む）
- **書いてある場所**: Agent SDK reference - Python > Functions > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> destructiveHint bool | None True If True, the tool may perform destructive updates (only meaningful when readOnlyHint is False)

- **日本語**: destructiveHint：bool | None、既定 True。True なら破壊的な更新をしうる（readOnlyHint が False のときだけ意味を持つ）。
- **どう使っているか**: Python SDK の ToolAnnotations の型と既定値（MCP 仕様どおり readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=True）。ToolAnnotations は mcp.types.ToolAnnotations を拡張し maxResultSizeChars を足し、camelCase / snake_case の両方を受ける。
- **条件**: Python Agent SDK。snake_case 名と型付き maxResultSizeChars は 0.2.140 以降（同節）。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent SDK reference - Python > Functions > tool() > ToolAnnotations」（取得 2026-10-02T22:11:22Z、sha256 13e5cd1618e4…）
- **補足**: 同じ表の readOnlyHint 行「readOnlyHint bool | None False If True, the tool does not modify its environment」も verify_quote.py exact。表の直前に「All fields are optional. Clients shouldn't rely on the hints for security decisions.」がある（検証者が verify_quote.py exact で確認。C04_anthropic-36 として別項目にした）。 同じ節の『Clients shouldn't rely on the hints for security decisions』が finder の記録から抜けていたので、notes に足し、別項目（36）にした。

<a id="g-c04-anthropic-36"></a>
#### C04-36 Anthropic — Claude Agent SDK（Python）

- **資料**: Agent SDK reference - Python — tool() > ToolAnnotations（code.claude.com/docs/en/agent-sdk/python）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/python
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/python#toolannotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Agent SDK reference - Python > Functions > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> All fields are optional. Clients shouldn't rely on the hints for security decisions.

- **日本語**: すべてのフィールドは任意。クライアントはセキュリティ上の判断をこの hint に頼るべきではない。
- **どう使っているか**: Python Agent SDK の公式リファレンスが、annotations をセキュリティ判断に使うなと注意する。C04_anthropic-17（metadata, not enforcement）と並ぶ、Anthropic 自身による「宣言を信用するな」の記述。一方で Cowork / ディレクトリ（C04_anthropic-01, 08）は宣言を承認の扱いに使っている。
- **条件**: Agent SDK のカスタムツール（@tool の annotations）についての記述。「Clients」が Claude Code 自身を含むかは書かれていない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent SDK reference - Python > Functions > tool() > ToolAnnotations」（取得 2026-10-02T22:11:22Z、sha256 13e5cd1618e4…）
- **補足**: ToolAnnotations の表の直前の文。MCP 仕様の「clients MUST consider tool annotations to be untrusted unless they come from trusted servers」に近いが、信頼できるサーバの例外は書いていない。 検証者が追加（finder の C04_anthropic-18 と同じ節にあるが記録から抜けていた）。

### Anthropic — Claude Agent SDK（TypeScript）

<a id="g-c04-anthropic-19"></a>
#### C04-19 Anthropic — Claude Agent SDK（TypeScript）

- **資料**: Agent SDK reference - TypeScript — tool() > ToolAnnotations（code.claude.com/docs/en/agent-sdk/typescript）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/typescript
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/typescript#toolannotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Agent SDK reference - TypeScript > Functions > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> destructiveHint boolean true If true, the tool may perform destructive updates (only meaningful when readOnlyHint is false)

- **日本語**: destructiveHint：boolean、既定 true。true なら破壊的な更新をしうる（readOnlyHint が false のときだけ意味を持つ）。
- **どう使っているか**: TypeScript SDK の ToolAnnotations の既定値。tool() の extras.annotations は「MCP の挙動 hint をクライアントに提供する」もの。
- **条件**: TypeScript Agent SDK の tool() の第 5 引数 extras。
- **扱う宣言**: destructiveHint・readOnlyHint・idempotentHint・openWorldHint ／ **使い方の分類**: 宣言が無いときの扱い・そのまま渡す・見せる・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent SDK reference - TypeScript > Functions > tool() > ToolAnnotations」（取得 2026-10-02T22:11:22Z、sha256 3945fc661699…）
- **補足**: 同ページ Parameters 表「annotations provides MCP behavioral hints to clients.」（verify_quote.py exact, #parameters-3）と readOnlyHint 行「readOnlyHint boolean false If true, the tool does not modify its environment」（exact）も確認。表の直前に「Defined in @modelcontextprotocol/sdk/types.js. All fields are optional hints; clients should not rely on them for security decisions.」がある（検証者が exact を確認。C04_anthropic-37 として別項目にした）。 同じ節の『clients should not rely on them for security decisions』が finder の記録から抜けていたので、notes に足し、別項目（37）にした。

<a id="g-c04-anthropic-37"></a>
#### C04-37 Anthropic — Claude Agent SDK（TypeScript）

- **資料**: Agent SDK reference - TypeScript — tool() > ToolAnnotations（code.claude.com/docs/en/agent-sdk/typescript）（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/typescript
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/typescript#toolannotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Agent SDK reference - TypeScript > Functions > tool() > ToolAnnotations (#toolannotations)
- **原文**:

> Defined in @modelcontextprotocol/sdk/types.js. All fields are optional hints; clients should not rely on them for security decisions.

- **日本語**: @modelcontextprotocol/sdk/types.js で定義。すべてのフィールドは任意の hint で、クライアントはセキュリティ上の判断にこれらを頼るべきではない。
- **どう使っているか**: TypeScript Agent SDK の公式リファレンスが、annotations をセキュリティ判断に使うなと注意する（Python 版 C04_anthropic-36 と同じ趣旨）。
- **条件**: TypeScript Agent SDK の tool() の extras.annotations。「clients」が Claude Code 自身を含むかは書かれていない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent SDK reference - TypeScript > Functions > tool() > ToolAnnotations」（取得 2026-10-02T22:11:22Z、sha256 3945fc661699…）
- **補足**: ToolAnnotations の見出しの直下の文。 検証者が追加（finder の C04_anthropic-19 と同じ節にあるが記録から抜けていた）。tool の見出しは「Parameters」(#parameters-3) を返したが、正規化による位置ずれ（C04_anthropic-01 の verifier_note 参照）で、引き直すと「ToolAnnotations」(#toolannotations)。

### Anthropic — Claude Agent SDK（TypeScript）— mcpServerStatus()

<a id="g-c04-anthropic-20"></a>
#### C04-20 Anthropic — Claude Agent SDK（TypeScript）— mcpServerStatus()

- **資料**: Agent SDK reference - TypeScript — McpServerStatus（SDK の文書）
- **URL**: https://code.claude.com/docs/en/agent-sdk/typescript
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/agent-sdk/typescript#mcpserverstatus
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Agent SDK reference - TypeScript > Other Types > McpServerStatus (#mcpserverstatus)
- **原文**:

> readOnly?: boolean; destructive?: boolean; openWorld?: boolean;

- **日本語**: （McpServerStatus.tools[].annotations の型）readOnly?: boolean; destructive?: boolean; openWorld?: boolean;
- **どう使っているか**: Claude Code が接続中 MCP サーバの状態を SDK アプリに返すとき、各ツールの annotations は readOnly / destructive / openWorld の 3 つの真偽値の形で渡る。idempotentHint と title はこの形に無い。
- **条件**: SDK の query.mcpServerStatus()。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent SDK reference - TypeScript > Other Types > McpServerStatus」（取得 2026-10-02T22:11:22Z、sha256 3945fc661699…）
- **補足**: readOnly ← readOnlyHint などの対応は名前からの推定で、ページは対応を書いていない（不明）。Python 版の McpServerStatus 表にも「Tools provided by this server, each with name, description, and annotations fields」（verify_quote.py exact, #mcpserverstatus）。Python SDK のソースでも同じ 3 フィールド（C04_anthropic-21）。 「hint を詰め直して渡す」は型からの推定なので、対応が書かれていないことを notes に明記した。

### Anthropic — claude-agent-sdk-python（ソース）

<a id="g-c04-anthropic-21"></a>
#### C04-21 Anthropic — claude-agent-sdk-python（ソース）

- **資料**: src/claude_agent_sdk/types.py — McpToolAnnotations（SDK のソースコード）
- **URL**: https://github.com/anthropics/claude-agent-sdk-python/blob/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/types.py#L712-L719
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/types.py
- **版**: commit bfb895c6ef46e095191938b4eda798a025957c09
- **書いてある場所**: lines 712-719（class McpToolAnnotations の docstring と本体。クラス定義は L711）
- **原文**:

```
"""Tool annotations as returned in MCP server status.

    Wire format uses camelCase field names (from CLI JSON output).
    """

    readOnly: bool
    destructive: bool
    openWorld: bool
```

- **日本語**: 「MCP サーバ状態で返されるツール annotations。通信形式は（CLI の JSON 出力に由来する）camelCase のフィールド名」 readOnly / destructive / openWorld の 3 つの bool。
- **どう使っているか**: Claude Code CLI が JSON で出す MCP サーバ状態のうち、ツールの annotations は readOnly / destructive / openWorld の 3 つ（idempotentHint・title は含まれない）。CLI が少なくともこの 3 hint を保持・公開している証拠。
- **条件**: get_mcp_status()（McpServerInfo.tools[].annotations）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、712-719 行（# output-only)）（取得 2026-10-02T22:11:29Z、sha256 b10544732807…）
- **補足**: verify は raw.githubusercontent.com の同 commit。クラス定義 class McpToolAnnotations(TypedDict, total=False) は L711。

<a id="g-c04-anthropic-22"></a>
#### C04-22 Anthropic — claude-agent-sdk-python（ソース）

- **資料**: src/claude_agent_sdk/__init__.py — tool() docstring（SDK のソースコード）
- **URL**: https://github.com/anthropics/claude-agent-sdk-python/blob/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/__init__.py#L275-L276
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/__init__.py
- **版**: commit bfb895c6ef46e095191938b4eda798a025957c09
- **書いてある場所**: lines 275-276（tool() の docstring の Args）
- **原文**:

```
annotations: Optional MCP tool annotations (hints such as
            ``readOnlyHint`` or ``destructiveHint``) advertised to Claude.
```

- **日本語**: annotations：任意の MCP ツール annotations（readOnlyHint や destructiveHint などの hint）で、Claude に知らされる。
- **どう使っているか**: @tool の annotations は tools/list の各ツールにそのまま載せられ（同ファイル L587 "annotations": tool_def.annotations,）、Claude（CLI とモデル）に届く。
- **条件**: in-process SDK MCP サーバ（create_sdk_mcp_server）。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、275-276 行（# The snake_case spelling of each hint, mapped to its wire (camelCase) name.）（取得 2026-10-02T22:11:59Z、sha256 0d18689948f2…）
- **補足**: L587 の行「"annotations": tool_def.annotations,」も verify_quote.py exact（同 commit）。 notes の L587「"annotations": tool_def.annotations,」を再実行で exact（line 587）。変更なし。

<a id="g-c04-anthropic-23"></a>
#### C04-23 Anthropic — claude-agent-sdk-python（ソース）

- **資料**: src/claude_agent_sdk/__init__.py — _build_meta のコメント（SDK のソースコード）
- **URL**: https://github.com/anthropics/claude-agent-sdk-python/blob/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/__init__.py#L434-L435
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/bfb895c6ef46e095191938b4eda798a025957c09/src/claude_agent_sdk/__init__.py
- **版**: commit bfb895c6ef46e095191938b4eda798a025957c09
- **書いてある場所**: lines 434-435（_build_meta のコメント）
- **原文**:

```
# Client-specific hints travel in _meta under namespaced keys because MCP
    # clients drop annotation fields they do not know.
```

- **日本語**: クライアント固有の hint は名前空間つきのキーで _meta に載せて運ぶ。MCP クライアントは知らない annotation フィールドを捨てるから。
- **どう使っているか**: Anthropic 固有の値（maxResultSizeChars）は annotations ではなく _meta["anthropic/maxResultSizeChars"] で送る。理由は、クライアント（Claude Code を含む）が未知の annotation フィールドを落とすため。Anthropic は独自の宣言を annotations に足さず _meta に置く方針。
- **条件**: SDK MCP サーバの tools/list 生成。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、434-435 行（# The snake_case spelling of each hint, mapped to its wire (camelCase) name.）（取得 2026-10-02T22:11:59Z、sha256 0d18689948f2…）
- **補足**: Claude Code CHANGELOG 2.1.91「Added MCP tool result persistence override via `_meta["anthropic/maxResultSizeChars"]` annotation (up to 500K)…」（verify_quote.py exact。行は 5364。tool は 5364-5365 と出すが、行番号のずれ（C04_anthropic-28 の verifier_note 参照）で、引用は 1 行）と対応。コメントが言うのは「MCP clients」一般で、Claude Code を名指ししてはいない（Claude Code が落とすことは C04_anthropic-24）。Claude Code の _meta["anthropic/requiresUserInteraction"]（C04_anthropic-27）も同じ方針。 notes の CHANGELOG 行番号を 5364-5365 → 5364 に修正。コメントは Claude Code を名指ししていないことを明記。

### Anthropic — claude-agent-sdk-python

<a id="g-c04-anthropic-24"></a>
#### C04-24 Anthropic — claude-agent-sdk-python

- **資料**: CHANGELOG.md — 0.1.55 Bug Fixes（リリースノート）
- **URL**: https://github.com/anthropics/claude-agent-sdk-python/blob/bfb895c6ef46e095191938b4eda798a025957c09/CHANGELOG.md#L868
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/bfb895c6ef46e095191938b4eda798a025957c09/CHANGELOG.md
- **版**: 0.1.55（CHANGELOG, commit bfb895c6ef46）
- **書いてある場所**: line 868 (直前の見出し: ## 0.1.55 > ### Bug Fixes)
- **原文**:

> Forward `maxResultSizeChars` from `ToolAnnotations` via `_meta` to bypass Zod annotation stripping in the CLI, fixing silent truncation of large MCP tool results (>50K chars)

- **日本語**: ToolAnnotations の maxResultSizeChars を _meta 経由で送るようにし、CLI の Zod による annotation の取り除きを回避した。これで大きな MCP ツール結果（5 万字超）が黙って切り詰められていた問題を直した。
- **どう使っているか**: SDK 側の記述によれば、当時の Claude Code CLI は annotations を Zod スキーマで検証し、スキーマに無いフィールド（ここでは maxResultSizeChars）を取り除いていた。拡張フィールドを annotations に置いても CLI に届かない実例。
- **条件**: Python Agent SDK 0.1.55 で入った修正（0.1.54 以前は maxResultSizeChars が落ちていた）。同じ 0.1.55 の節は同梱 CLI を 2.1.36 に上げたと書く。現行の CLI が今も同じように取り除くかは、CLI のソースが非公開で確かめられない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、868 行（### Bug Fixes）（取得 2026-10-02T22:11:33Z、sha256 662928ff6ef9…）
- **補足**: 「Zod annotation stripping in the CLI」は CLI 内部の挙動についての SDK 側の記述（CLI のソースは非公開で一次確認できない）。 conditions の「0.1.55 以前の挙動の修正」は 0.1.55 自体を含む書き方で誤り（0.1.55 で修正）。usage_ja の「MCP 標準の hint 以外は CLI に届かない」は一般化しすぎなので、当時の CLI で maxResultSizeChars が落ちていたという記述に絞った。location に版の見出し ## 0.1.55 を足した。

<a id="g-c04-anthropic-25"></a>
#### C04-25 Anthropic — claude-agent-sdk-python

- **資料**: CHANGELOG.md — 0.1.31 New Features（リリースノート）
- **URL**: https://github.com/anthropics/claude-agent-sdk-python/blob/bfb895c6ef46e095191938b4eda798a025957c09/CHANGELOG.md#L1102
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-python/bfb895c6ef46e095191938b4eda798a025957c09/CHANGELOG.md
- **版**: 0.1.31（CHANGELOG, commit bfb895c6ef46）
- **書いてある場所**: line 1102 (直前の見出し: ## 0.1.31 > ### New Features)
- **原文**:

> Added support for MCP tool annotations via the `@tool` decorator's new `annotations` parameter, allowing developers to specify metadata hints like `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`.

- **日本語**: @tool デコレータの新しい annotations 引数で MCP ツール annotations に対応し、readOnlyHint, destructiveHint, idempotentHint, openWorldHint などのメタデータ hint を指定できるようにした。
- **どう使っているか**: Python SDK で annotations を宣言できるようになった版。
- **条件**: Python Agent SDK 0.1.31 以降。
- **扱う宣言**: readOnlyHint・destructiveHint・idempotentHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、1102 行（### New Features）（取得 2026-10-02T22:11:33Z、sha256 662928ff6ef9…）
- **補足**: TypeScript SDK は 0.2.27（C04_anthropic-26）。 location に版の見出し ## 0.1.31 を足した。解釈は変更なし。

### Anthropic — claude-agent-sdk-typescript

<a id="g-c04-anthropic-26"></a>
#### C04-26 Anthropic — claude-agent-sdk-typescript

- **資料**: CHANGELOG.md — 0.2.27（リリースノート）
- **URL**: https://github.com/anthropics/claude-agent-sdk-typescript/blob/9d8cb9c1ae68672c343d75723440b73afe5b993c/CHANGELOG.md#L1323
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-agent-sdk-typescript/9d8cb9c1ae68672c343d75723440b73afe5b993c/CHANGELOG.md
- **版**: 0.2.27（CHANGELOG, commit 9d8cb9c1ae68）
- **書いてある場所**: line 1323 (直前の見出し: ## 0.2.27)
- **原文**:

> Added optional `annotations` support to the `tool()` helper function for specifying MCP tool hints (readOnlyHint, destructiveHint, openWorldHint, idempotentHint)

- **日本語**: tool() ヘルパに任意の annotations を追加し、MCP ツールの hint（readOnlyHint, destructiveHint, openWorldHint, idempotentHint）を指定できるようにした。
- **どう使っているか**: TypeScript SDK で annotations を宣言できるようになった版。
- **条件**: TypeScript Agent SDK 0.2.27 以降。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint ／ **使い方の分類**: そのまま渡す・見せる・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、1323 行（## 0.2.27）（取得 2026-10-02T22:11:32Z、sha256 8237245c0939…）
- **補足**: このリポジトリは README / CHANGELOG / examples だけで、SDK 本体のソースは npm パッケージ（@anthropic-ai/claude-agent-sdk）の minified コード。 location と url の行を 1323-1324 → 1323 に修正（引用は 1 行）。verify_quote.py は文字の正規化（… → ...、ゼロ幅文字の削除）をした後の位置で見出し・行番号を引くため、正規化で長さが変わる文字が前にあると位置がずれる（このページでは … が 1 個）。正規化前の位置に戻して引き直した結果（scratchpad の annot/v04/headfix.py・lines.py）を location に書いた。tool の生の出力は「lines 1323-1324」。

### Anthropic — Claude Code（CLI）

<a id="g-c04-anthropic-27"></a>
#### C04-27 Anthropic — Claude Code（CLI）

- **資料**: Connect Claude Code to tools via MCP — Require approval for a specific tool（code.claude.com/docs/en/mcp）（クライアントの文書）
- **URL**: https://code.claude.com/docs/en/mcp
- **書いてある見出しへ直接**: https://code.claude.com/docs/en/mcp#require-approval-for-a-specific-tool
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connect Claude Code to tools via MCP > Require approval for a specific tool (#require-approval-for-a-specific-tool)
- **原文**:

> If you're building an MCP server, you can mark a tool as requiring explicit approval on every call by setting _meta["anthropic/requiresUserInteraction"] to true in the tool's tools/list response entry.

- **日本語**: MCP サーバを作るなら、tools/list の各ツールの項目で _meta["anthropic/requiresUserInteraction"] を true にすると、そのツールを毎回の明示的な承認が必要なものにできる。
- **どう使っているか**: Claude Code で「毎回確認」を強制するサーバ側の宣言は ToolAnnotations（destructiveHint など）ではなく Anthropic 独自の _meta キー。acceptEdits / auto / bypassPermissions でも、allow ルールがあっても毎回プロンプトを出し、dontAsk では拒否。annotations ではない別の宣言経路として記録。
- **条件**: JSON の true のときだけ（他の値は無視）。Claude Code v2.1.199 以降（それより前は無視して通常の権限の流れ。「The anthropic/requiresUserInteraction annotation requires Claude Code v2.1.199 or later.」verify_quote.py exact）。--permission-prompt-tool での allow は deny に変換。Agent SDK の canUseTool は受け取って承認できる。
- **扱う宣言**:  ／ **使い方の分類**: 確認を求める・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect Claude Code to tools via MCP > Require approval for a specific tool」（取得 2026-10-02T22:12:43Z、sha256 436d7fb28e38…）
- **補足**: ToolAnnotations ではない（hints は空）。ただしページ自身はこれを「annotation」と呼んでいる（上の版の文）。同じ mcp ページに readOnlyHint / destructiveHint / openWorldHint / idempotentHint / "tool annotations" の語は無い（checked_no_mention、再実行でも none）。 location / anchored_url を修正。verify_quote.py は文字の正規化（… → ...、ゼロ幅文字の削除）をした後の位置で見出し・行番号を引くため、正規化で長さが変わる文字が前にあると位置がずれる（このページでは ゼロ幅文字 78 個）。正規化前の位置に戻して引き直した結果（scratchpad の annot/v04/headfix.py・lines.py）を location に書いた。tool の生の出力は「Connect Claude Code to tools via MCP > Tools with invalid input schemas #tools-with-invalid-input-schemas」。 正しい見出しの id はページの HTML に id="require-approval-for-a-specific-tool" として 1 つあることを確認。 conditions に必要な版（v2.1.199 以降）を足した。notes の見出し推定は引き直しで確定したので外した。

<a id="g-c04-anthropic-28"></a>
#### C04-28 Anthropic — Claude Code（CLI）

- **資料**: CHANGELOG.md — 1.0.44（リリースノート）
- **URL**: https://github.com/anthropics/claude-code/blob/52c76441cae91f6891e4712306bffb057ff6fec5/CHANGELOG.md#L7702
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/anthropics/claude-code/52c76441cae91f6891e4712306bffb057ff6fec5/CHANGELOG.md
- **版**: 1.0.44（CHANGELOG, commit 52c76441cae9）
- **書いてある場所**: line 7702 (直前の見出し: ## 1.0.44)
- **原文**:

> MCP: tool annotations and tool titles now display in /mcp view

- **日本語**: MCP：ツールの annotations とツールの title が /mcp 画面に表示されるようになった。
- **どう使っているか**: Claude Code は /mcp の画面でツールの annotations と title を利用者に表示する（表示用途）。承認や並列化に使うとはここでは言っていない。
- **条件**: 対話型 CLI の /mcp 画面。
- **扱う宣言**: 宣言全般・title ／ **使い方の分類**: 表示（印・名前）
- **確かさ**: [確認] 再照合 exact・1 か所、7702 行（## 1.0.44）（取得 2026-10-02T22:11:35Z、sha256 797d9c8136c1…）
- **補足**: 同じ文は https://code.claude.com/docs/en/changelog（HTML）でも verify_quote.py exact。Claude Code CHANGELOG（887KB）全体で readOnlyHint / destructiveHint の語は 0 件、annotations に触れるのはこの行と 2.1.91 の _meta 行だけ（grep, 2026-10-02）。 location と url の行を 7703 → 7702 に修正（grep -n でも 7702）。verify_quote.py は文字の正規化（… → ...、ゼロ幅文字の削除）をした後の位置で見出し・行番号を引くため、正規化で長さが変わる文字が前にあると位置がずれる（このページでは … などが 45 個）。正規化前の位置に戻して引き直した結果（scratchpad の annot/v04/headfix.py・lines.py）を location に書いた。tool の生の出力は「lines 7703」。 notes の「CHANGELOG 全体で readOnlyHint / destructiveHint 0 件、annotations に触れるのはこの行と 2.1.91 の行だけ」を grep で再確認（annotation の語はほかに L4031 の /plugin の "suggested for this directory" annotation があるが、ツールの annotations とは無関係）。

### Anthropic — Anthropic Engineering blog

<a id="g-c04-anthropic-29"></a>
#### C04-29 Anthropic — Anthropic Engineering blog

- **資料**: Writing effective tools for agents — with agents（公式ブログ）
- **URL**: https://www.anthropic.com/engineering/writing-tools-for-agents
- **書いてある見出しへ直接**: https://www.anthropic.com/engineering/writing-tools-for-agents#prompt-engineering-your-tool-descriptions
- **版**: 2025-09-11 公開（HTML 内の日付表示 "Sep 11, 2025" を grep で確認）。2026-10-02 取得
- **書いてある場所**: Writing effective tools for agents - with agents > Principles for writing effective tools > Prompt-engineering your tool descriptions (#prompt-engineering-your-tool-descriptions)
- **原文**:

> Lastly, if you're writing tools for an MCP server, tool annotations help disclose which tools require open-world access or make destructive changes.

- **日本語**: 最後に、MCP サーバ用のツールを書くなら、tool annotations は、どのツールが外の世界へのアクセスを要するか、どのツールが破壊的な変更をするかを明らかにするのに役立つ。
- **どう使っているか**: Anthropic の技術ブログでの作者向け助言。annotations は open-world アクセスと破壊的変更を「開示する」ためのもの、という位置づけ（クライアントが何に使うかは書かない）。
- **条件**: MCP サーバ向けツールを書く場合。
- **扱う宣言**: openWorldHint・destructiveHint・宣言全般 ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Writing effective tools for agents - with agents > Principles for writing effective tools > Prompt-engineering your tool descriptions」（取得 2026-10-02T22:11:40Z、sha256 78899c817700…）
- **補足**: readOnlyHint の語はこのページに無い（verify_quote.py none）。annotations に触れるのはこの 1 文だけ。 公開日 "Sep 11, 2025" を HTML で確認。解釈は変更なし。

### Agent Client Protocol project（agentclientprotocol。Anthropic ではない） — claude-agent-acp（Claude Agent SDK を ACP に橋渡しするアダプタ）

<a id="g-c04-anthropic-30"></a>
#### C04-30 Agent Client Protocol project（agentclientprotocol。Anthropic ではない） — claude-agent-acp（Claude Agent SDK を ACP に橋渡しするアダプタ）

- **資料**: Issue #1184: Forward MCP tool annotations (readOnly/destructive) on permission requests（issue / PR / 提案の下書き）
- **URL**: https://github.com/agentclientprotocol/claude-agent-acp/issues/1184
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> Forward MCP tool annotations (readOnly/destructive) on permission requests

- **日本語**: MCP ツールの annotations（readOnly / destructive）を権限要求に載せて転送する。
- **どう使っているか**: （検索要約による）Claude Code の query.mcpServerStatus() は tools[].annotations.{readOnly, destructive, openWorld} をサーバの hint から埋めて返すが、アダプタは session/request_permission に hint を載せていないので、ACP クライアント（Zed など）は読み取り専用と破壊的ツールを区別できない。_meta.claudeCode.mcpServer.annotations に真偽値だけ写す提案。宣言が無いツールでは省く。
- **条件**: ACP クライアント経由で Claude Agent SDK を使う場合。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: mcpServerStatus が readOnly / destructive / openWorld を返すこと自体は Anthropic の一次資料で確認済み（C04_anthropic-20, 21）。issue の提案が採用されたかは不明。検索要約は VS Code（readOnlyHint で確認を省く）と Codex（既定モードで read-only を自動承認）にも触れているが未確認。

### Anthropic（anthropics/claude-code の issue。投稿者は利用者で、Anthropic の見解ではない） — Claude Code（CLI）

<a id="g-c04-anthropic-31"></a>
#### C04-31 Anthropic（anthropics/claude-code の issue。投稿者は利用者で、Anthropic の見解ではない） — Claude Code（CLI）

- **資料**: Issue #87452: [FEATURE] Permission engine should process MCP ToolAnnotations hints (readOnlyHint, destructiveHint, etc.)（issue / PR / 提案の下書き）
- **URL**: https://github.com/anthropics/claude-code/issues/87452
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> [FEATURE] Permission engine should process MCP ToolAnnotations hints (readOnlyHint, destructiveHint, etc.)

- **日本語**: ［機能要望］権限エンジンは MCP の ToolAnnotations の hint（readOnlyHint, destructiveHint など）を処理すべき。
- **どう使っているか**: （タイトルから）投稿時点で Claude Code の権限エンジン（allow / ask の判定）は annotations を使っていない、という利用者側の認識。readOnlyHint:true を自動許可する要望。
- **条件**: 投稿時点の Claude Code。
- **扱う宣言**: readOnlyHint・destructiveHint ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: Claude Code の公式ドキュメント（permissions / permission-modes / mcp）にも annotations で許可が変わるという記述は無い（checked_no_mention）。ただし plan mode では readOnlyHint を見ているという別の報告がある（C04_anthropic-32, 35）。

### Anthropic（anthropics/claude-code の issue。利用者の報告） — Claude Code（CLI）plan mode

<a id="g-c04-anthropic-32"></a>
#### C04-32 Anthropic（anthropics/claude-code の issue。利用者の報告） — Claude Code（CLI）plan mode

- **資料**: Issue #78085: Read-only MCP tools blocked in plan mode (refiling #12368, closed by stale-bot, not reviewed)（issue / PR / 提案の下書き）
- **URL**: https://github.com/anthropics/claude-code/issues/78085
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> Read-only MCP tools blocked in plan mode (refiling #12368, closed by stale-bot, not reviewed)

- **日本語**: 読み取り専用の MCP ツールが plan mode でブロックされる（#12368 の再提出。stale-bot に閉じられ、審査されなかった）。
- **どう使っているか**: （検索要約による）MCP のツール定義は readOnlyHint を持ち Claude Code は別の用途でそれを読んでいるので、plan mode で readOnlyHint:true のツールを組み込みの読み取りツールと同様に自動許可してほしい、という要望。
- **条件**: Claude Code の plan mode。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: 「Claude Code already reads it for other things」は検索要約の言い回しで未確認。

### Anthropic（anthropics/claude-ai-mcp の issue。利用者の報告） — Claude Desktop（Auto 権限モード、ローカル MCP サーバ）

<a id="g-c04-anthropic-33"></a>
#### C04-33 Anthropic（anthropics/claude-ai-mcp の issue。利用者の報告） — Claude Desktop（Auto 権限モード、ローカル MCP サーバ）

- **資料**: Issue #1090: Auto permission mode still prompts for every call to read-only tools from local MCP servers (desktop app)（issue / PR / 提案の下書き）
- **URL**: https://github.com/anthropics/claude-ai-mcp/issues/1090
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> Auto permission mode still prompts for every call to read-only tools from local MCP servers (desktop app)

- **日本語**: Auto 権限モードでも、ローカル MCP サーバの読み取り専用ツールは呼び出しのたびに確認を求められる（デスクトップアプリ）。
- **どう使っているか**: （タイトルから）Desktop の Auto 権限モードで、ローカル MCP サーバの read-only ツールが呼び出しのたびに確認を求められるという報告。Cowork のドキュメント（C04_anthropic-09）が read-only の自動承認を書くのは「Auto かつツール権限が Always allow」のときだけなので、これが文書との食い違いかどうかはタイトルからは判断できない（不明）。
- **条件**: Claude Desktop、ローカル（stdio）MCP サーバ、Auto モード。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: anthropics/claude-ai-mcp は「Claude.ai の MCP 統合」の連絡用リポジトリ（README を raw で確認、commit 43dac3a1bc64。README に annotations の記述は無い）。 usage_ja の「ドキュメント上の挙動との食い違いと読める」は過大。09 の自動承認は Auto かつ Always allow の条件つきで、issue の設定は不明。

### Anthropic（anthropics/claude-code の issue。利用者の要望） — Claude Desktop

<a id="g-c04-anthropic-34"></a>
#### C04-34 Anthropic（anthropics/claude-code の issue。利用者の要望） — Claude Desktop

- **資料**: Issue #79734: [FEATURE] Claude Desktop: opt-in setting to auto-approve write/modifying MCP tools per server（issue / PR / 提案の下書き）
- **URL**: https://github.com/anthropics/claude-code/issues/79734
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> [FEATURE] Claude Desktop: opt-in setting to auto-approve write/modifying MCP tools per server

- **日本語**: ［機能要望］Claude Desktop：書き込み・変更をする MCP ツールをサーバ単位で自動承認できる、オプトインの設定。
- **どう使っているか**: （検索要約による）Desktop では read-only ツールは自動承認できるが write ツールはできず、全体・サーバ単位の設定も無い、という前提での要望。read-only か否かで承認可能性が分かれることの利用者側の観察。
- **条件**: Claude Desktop。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: 公式側の対応する記述：C04_anthropic-08, 11, 12（データを変更しうるツールは永続の Always allow が出ない／組織設定で制限）。

### coreConvention（第三者の MCP サーバ johnny-five の issue） — Claude Code plan mode（第三者からの観察）

<a id="g-c04-anthropic-35"></a>
#### C04-35 coreConvention（第三者の MCP サーバ johnny-five の issue） — Claude Code plan mode（第三者からの観察）

- **資料**: Issue #36: Read-only tools lack readOnlyHint, so Claude Code plan mode prompts for every call (even with an allow rule)（第三者の記事）
- **URL**: https://github.com/coreConvention/johnny-five/issues/36
- **版**: 2026（日付不明）
- **書いてある場所**: issue のタイトル（WebSearch 結果に出た文字列）
- **原文**:

> Read-only tools lack readOnlyHint, so Claude Code plan mode prompts for every call (even with an allow rule)

- **日本語**: 読み取り専用ツールに readOnlyHint が無いので、Claude Code の plan mode は（allow ルールがあっても）呼び出しのたびに確認を求める。
- **どう使っているか**: （検索要約による）Claude Code は MCP ツールの read-only 判定に annotations?.readOnlyHint（既定 false）を使い、plan mode では read-only でない MCP ツールを「Cannot call <tool> while in plan mode」という理由で確認に回し、この確認は allow ルールより先に返る。宣言が無いと全ツールが書き込み可能扱い。対応として同作者は PR #37 で readOnlyHint を付けた。
- **条件**: Claude Code の plan mode。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・宣言が無いときの扱い
- **確かさ**: [未確認] 未検証: github.com の issue HTML はこの環境でブロック（README 規定）。WebSearch（2026-10-02）の結果タイトルだけを見た。本文の主張は検索結果の要約で、一次確認していない。 （検証者 2026-10-02 再確認）ネットワーク設定の変更後も github.com の issue ページは HTTP 403 で、本文は 「GitHub access to this repository is not enabled for this session. Use add_repo to request access.」。api.github.com も 403。GitHub の MCP コネクタ（issue_read）も「repository ... is not configured for this session. Allowed repositories: s1300105/auth_gap」で拒否。リポジトリをセッションに足すのは利用者の判断なので行っていない。よって未確認のまま。
- **補足**: 第三者による観察（Claude Code の非公開実装について）。Claude Code の公式ドキュメントにこの挙動の記述は無い（permission-modes / permissions で readOnlyHint は none）。同種の対応 PR：mozilla/bugbug #6933「Mark MCP server tools as read-only」、rodlc/mcp-memory-service #2（いずれも検索結果タイトルのみ、未確認）。

---

[← 付録 G-3 Microsoft と GitHub](appendix-g-3.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-5 OpenAI →](appendix-g-5.md)
