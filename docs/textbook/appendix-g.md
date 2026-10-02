[← 付録 F 判定の言葉の対照表](appendix-f.md) ｜ [目次](README.md) ｜ [付録 G-1 →](appendix-g-1.md)

---

# 付録 G 宣言の使われ方の資料集

<a id="ag-1"></a>
## この付録の使い方

### 一言で言うと

ツールの宣言（ToolAnnotations。`readOnlyHint` などの 4 つの印）が、**実際の製品の中で何に使われているか**を、原文つきで集めた資料集です。
資料は 820 件あり、分野ごとに 12 の分冊（[付録 G-1](appendix-g-1.md)〜[付録 G-12](appendix-g-12.md)）に「カード」として並べました。
記載が見つからなかったページと、読めなかったページは [付録 G-13](appendix-g-13.md) にまとめました。
この表紙のページは、その 820 件から分かったことを、カードへのリンクつきで短くまとめたものです。

### なぜ判定する人がこれを読むのか

この研究の 4 つの宣言は、次のとおりです（[第 4 章](ch04.md)）。

| 記号 | 宣言 | やさしい言い換え |
|---|---|---|
| D1 | `readOnlyHint: true` | このツールは読むだけで、何も変えません |
| D2 | `destructiveHint: false` | 変えることはあっても、壊す（消す・上書きする）ことはしません |
| D3 | `openWorldHint: false` | 外の世界（インターネットなど）とはやりとりしません |
| D4 | `idempotentHint: true` | 同じ呼び出しを何回しても、1 回と同じ結果です |

宣言は、MCP の仕様の上では「ヒント（目安）」です。
仕様自身が「信頼できるサーバのものでなければ信じるな」と書いています。
それでも、いくつかの製品は、宣言を見て**利用者への確認を省きます**。
たとえば「読むだけです」と宣言したツールを、確認の画面を出さずに動かす製品があります。

ここで「確認を省く」とは、ツールを動かす前に利用者へ「実行してよいですか」と聞く画面（確認の画面）を出さないことです。
「自動で許可する」「自動承認」とも言います。

もし宣言がうそ（間違い）なら、利用者が知らないうちに書き込みが起きます。
AuthGap は、その宣言が実装と合っているかを、ソースコードから確かめる道具です。
この付録は、**宣言の間違いが、どの製品のどの条件で、どんな結果につながりうるか**を、判定する人が原文で確かめるためのものです。
判定そのもの（1 件ずつの正 / 誤）には使いません。判定の基準は、コードと宣言の関係だけです（[第 4 章](ch04.md) 4.6 節）。
この付録は、研究の動機と、論文で違反の意味を説明するときの根拠に使います。

### たとえ話 — 宅配便の送り状の「品名」欄

宅配便を出すとき、送り状の「品名」欄に、送る人が自分で「書類」「衣類」と書きます。
運ぶ会社は、多くの場合、箱を開けずにその欄を信じて、扱い方（ていねいに運ぶか、急ぐか）を決めます。
会社によっては「品名が『書類』なら確認なしで受け付ける」窓口もあれば、「品名に関係なく中身を聞く」窓口もあります。
欄が空いているときに「危ない物かもしれない」と扱う窓口もあれば、「普通の荷物」として通してしまう窓口もあります。

ツールの宣言は、この「品名」欄に当たります。書くのはツールの作者で、読むのは AI のアプリ（クライアント）です。
この付録は、「どの窓口が、品名欄をどう扱っているか」を、窓口ごとの規則の原文で集めたものです。
AuthGap は、箱の中身（ソースコード）と品名欄が合っているかを確かめる係です。

### 言葉の確認

この付録でよく使う言葉を、先に決めておきます。

| 言葉 | 意味 |
|---|---|
| クライアント・ホスト | ツールを呼び出す側の AI のアプリ。VS Code や Claude Desktop など。この付録では区別せずに使います |
| サーバ | ツールを提供する側のプログラム。宣言を書くのはサーバの作者です |
| SDK | サーバやクライアントを作るための部品集（ライブラリ） |
| ゲートウェイ | クライアントとサーバの間に立って、通信を中継する装置。会社の受付のように、通してよい呼び出しを決めることがあります |
| レジストリ・ディレクトリ | サーバを登録して一覧にする場所。アプリストアのようなもの |
| 既定値 | 何も書かなかったときに使われる値。MCP の仕様では `readOnlyHint` false、`destructiveHint` true、`idempotentHint` false、`openWorldHint` true です |
| 宣言が無いと止める向き（fail-safe） | 宣言が無いツールを「危ないかもしれない」として、確認を求めたり止めたりする扱い |
| 宣言が無いと通してしまう向き（fail-open） | 宣言が無いツールを「危なくない」として、確認なしで通してしまう扱い |
| リンター | ソースコードや設定の書き方の誤りを機械的に指摘する道具 |

### どう調べたか

調査は 2026-10-02 に行いました。進め方は次のとおりです。

1. **分野を 20 に分けました。** MCP の公式、SDK、Microsoft と GitHub、Anthropic、OpenAI、Google と AWS、エディタ、枠組み、サーバの作者、ゲートウェイ、検査の道具、登録所、WebMCP、研究と標準などです。
2. **3 回に分けて集めました。** 1 回目で大きな分野を調べ、2 回目と 3 回目で、まだ見ていない製品（閉じたクライアント、ゲートウェイ、アジアのエージェント、業務アプリなど）を足しました。
3. **分野ごとに、集める担当と、別の点検の担当を置きました。** 点検の担当は、集める担当とは別に原文を取り直し、解釈が言い過ぎていないかを直しました。
4. **引用の文字列を機械で照らし合わせました。** `scripts/verify_quote.py` で原文を取り寄せ、カードの「原文」の文字列が、その原文の中に本当にあるかを確かめました。
5. **2026-10-02 に、[確認] の全件（793 件）を取り直して照らし合わせ直しました。** 774 件が一致しました。一致しなかった 19 件は、どれも配布物を展開して手元の一時 URL で照らし合わせたもので、その URL が無くなったためです。この 19 件は [確認（調査時のみ）] として分けました（[確認] のままにはしていません）。

カードは `scripts/build_annotations_appendix.py` が `evidence/annotations_usage/sources.json` から機械的に作っています。引用を手で書き写していないので、写し間違いは入りません。カードの分冊は手で直さないでください。

### カードの読み方

1 枚のカードは、1 つの資料の 1 か所の記述です。欄は次のとおりです。

| 欄 | 書いてあること |
|---|---|
| 資料 | 資料の題と種類（仕様・公式の文書・ソースコードなど） |
| URL | 資料の場所 |
| 書いてある見出しへ直接 | その記述がある見出しへ直接飛ぶ URL（取れたものだけ）。配布物を展開して照らし合わせたカードでは、代わりに「照らし合わせた中身」の欄があります |
| 版 | 調べた版。ソースコードならコミット、製品なら版番号、文書なら取得日 |
| 書いてある場所 | 見出しの道すじ、または行番号 |
| 原文 | 引用。機械で照らし合わせた文字列そのもの |
| 日本語 | 原文の日本語訳 |
| どう使っているか | その製品が宣言を何に使っているかの読み。点検の担当が言い過ぎを直したあとの文 |
| 条件 | その使い方が成り立つモード・設定・版など。**ここを読み飛ばさないでください** |
| 扱う宣言 ／ 使い方の分類 | どの宣言の話か、使い方の 14 分類のどれか |
| 確かさ | 次の節の 3 つの印と、照らし合わせの記録 |
| 補足 | 関連する別の箇所、点検の担当の追記、分からなかったこと |

例として、VS Code のカード [C03-01](appendix-g-3.md#g-c03-microsoft-github-01) を開いてみてください。
「原文」は "The confirmation dialog will be shown for all tools that are not marked with the readOnlyHint annotation." です。
「どう使っているか」は「`readOnlyHint` が付いたツールは確認の画面を出さずに走る」です。
ところが「条件」を読むと、「サーバが sandbox で動いているときは注釈に関係なく確認なし」「設定でそのツールを自動承認の対象から外すと、`readOnlyHint` が真でも確認が出る」「権限のレベルを Allow all にしたときなどは全ツール確認なし」という例外が書いてあります。
「補足」には、利用者向けの別のページは `readOnlyHint` の確認省略を書いていない、という文書の不揃いが書いてあります。
このように、**原文 → どう使っているか → 条件 → 補足** の順に読むと、言い過ぎを避けられます。

### 確かさの 3 つの印

| 印 | 意味 | 使い方 |
|---|---|---|
| **[確認]** | 引用の文字列が原文にあることを `scripts/verify_quote.py` で照らし合わせ、2026-10-02 に取り直して照らし合わせ直したもの | 原文の記述として使えます。ただし「どう使っているか」の欄は読みなので、論文に書くときは原文を自分で開いてください |
| **[確認（調査時のみ）]** | 配布物（Claude Code の CLI のバイナリ、Copilot CLI の現行版、Cursor、Devin Desktop、Antigravity など）を展開して、調査のときに照らし合わせたもの。19 件。展開したファイルを手元の一時 URL で配っていたので、2026-10-02 の取り直しはしていません | 「その版の配布物の中にこの文字列があった」ことの記録です。再現の手順は各カードの補足にあります。使うときは文中で「調査時のみ」と書きます |
| **[未確認]** | 照らし合わせられなかったもの。github.com の issue（このセッションでは github.com のページが読めなかった）、検索結果の題名だけ見たもの、配信元が照合の道具を拒んだものなど | 事実として使いません。「そういう報告がある」という手がかりにとどめます |

付録 G-1〜G-12 の 820 件の内訳は、[確認] 774 件、[確認（調査時のみ）] 19 件、[未確認] 27 件です（分母は 820 件）。

### この資料集の限界

1. **無作為に選んだ標本ではありません。** 調べる担当が「宣言を使っていそうな製品」「よく使われる製品」を選んで集めた、便宜的な集まりです。だから、**件数を「全製品の何割が」という割合に直してはいけません。** この付録で件数を書くときは、分母（何件のうちか）を必ず書き、それがこの調査の集まりの中の数だと書きます。
2. **「記載が無い」は、そのページに無いという意味だけです。** [付録 G-13](appendix-g-13.md) の 514 ページは、調べた語がそのページに見つからなかったものです。その製品が宣言を使わないことの証拠ではありません。別のページやソースコードに書かれていることがあります。
3. **閉じたソースの製品の動きは、配布物から読んだものです。** Claude Code、Cursor、Devin Desktop などは、配布物を展開して中の JavaScript などを読みました。ミニファイ（短い名前への置き換え）されているので、関数の名前は版ごとに変わり、読みには推測が混じります。カードの「条件」と「補足」に、分からなかった部分が書いてあります。
4. **GitHub の issue はほぼ [未確認] です。** このセッションでは github.com のページが読めませんでした。issue の題名を検索で見ただけのものは [未確認] です。
5. **文書とコードが食い違うことがあります。** 2 つの例があります。
   - GitHub Copilot CLI の文書は「読み取り専用の操作でも、MCP ツールの実行には明示の許可が要る」と書きます（[C03-19](appendix-g-3.md#g-c03-microsoft-github-19)）。しかし 1.0.63 の実装は、deny の規則に当たらなければ `readOnlyHint: true` のツールを確認なしで承認します（[G2CCM-09](appendix-g-7.md#g-g2-closed-clients-missing-09)）。現行の 1.0.91 で同じかは不明です（同じカードの補足）。
   - Codex の文書は「破壊的の印があれば承認を求める。ただし読み取りの印のほうが優先」と書きます（[C05-29](appendix-g-5.md#g-c05-openai-29)）。しかしコードは `destructiveHint: true` を先に見て承認を求め、テストでもそれを固定しています（[C05-34](appendix-g-5.md#g-c05-openai-34)・[C05-38](appendix-g-5.md#g-c05-openai-38)）。App Server の文書はコードと一致します（[C05-30](appendix-g-5.md#g-c05-openai-30)）。
   - ほかに、VS Code の利用者向けの文書が確認の省略を書いていない（[C03-01](appendix-g-3.md#g-c03-microsoft-github-01) の補足）など、同じ会社の文書どうしが揃っていない例もあります。
6. **版で変わります。** どのカードにも「版」の欄があります。たとえば Devin CLI の Plan モードは、ある版で「`readOnlyHint: true` の MCP ツールだけ使える」と書かれ、後の版で「通常の権限の仕組みを使う」に変わりました。今も同じ絞り込みが続くかは不明です（[C07-21](appendix-g-7.md#g-c07-ide-agents-21)）。論文で使うときは、カードの版と日付を一緒に書きます。

### 第 4 章 4.5 節の表との関係

[第 4 章](ch04.md) 4.5 節の表は 2026-09-29 の調査で、[agent] や [未確認] の行がありました。この付録の調査で分かったことを、対応させておきます（第 4 章の表はそのまま残し、4.5 節の終わりにこの付録への案内を足しました）。

| 第 4 章の行 | この付録で分かったこと |
|---|---|
| VS Code [確認] | 同じ。例外の条件（sandbox、設定、Allow all など）が増えました（[C03-01](appendix-g-3.md#g-c03-microsoft-github-01)・[C03-06](appendix-g-3.md#g-c03-microsoft-github-06)） |
| Codex CLI [確認] | `destructiveHint: true` が `readOnlyHint` より優先すること、どちらでもないときは `destructiveHint: false` かつ `openWorldHint: false` なら承認なしになること、注釈が無ければ承認を求めることが分かりました（[C05-34](appendix-g-5.md#g-c05-openai-34)・[C05-39](appendix-g-5.md#g-c05-openai-39)） |
| Goose [agent] | [確認] になりました。ただし確認を省くのは、利用者が Smart Approve モードを選んだときだけです。既定の Autonomous モードは注釈に関係なく全部許可です（[C07-01](appendix-g-7.md#g-c07-ide-agents-01)・[C07-02](appendix-g-7.md#g-c07-ide-agents-02)） |
| Claude の connectors [agent] | 審査の基準のページで [確認] になりました（[C04-01](appendix-g-4.md#g-c04-anthropic-01)）。ただし、どの製品のどのモードで効くかは、そのページには書かれていません |
| GitHub Copilot coding agent [agent] | この調査のカードでは裏づけられませんでした。cloud agent（旧 coding agent）は許可リストに書いたツールを承認なしで使い、注釈を使うかは不明です（[C03-18](appendix-g-3.md#g-c03-microsoft-github-18)） |
| GitHub MCP server の read-only モード [agent] | [確認] になりました（[C03-12](appendix-g-3.md#g-c03-microsoft-github-12)・[C03-13](appendix-g-3.md#g-c03-microsoft-github-13)） |
| Gemini CLI [agent] | [確認] になりました。既定のモードでは注釈で自動許可しません（[C06-01](appendix-g-6.md#g-c06-google-aws-01)・[C06-04](appendix-g-6.md#g-c06-google-aws-04)） |
| Claude Code [未確認] | 公式の文書には今も記述がありません。配布物の実装からは plan mode などでの使い方が分かりました。ただし [確認（調査時のみ）] です（[G2CCM-03](appendix-g-7.md#g-g2-closed-clients-missing-03)） |

### この節のまとめ

- 820 件の資料をカードにし、分冊 G-1〜G-12 に置いた。記載が無い / 読めなかったページは G-13。
- カードは「原文 → どう使っているか → 条件 → 補足」の順に読む。条件を読み飛ばさない。
- 印は [確認]・[確認（調査時のみ）]・[未確認] の 3 つ。[未確認] は事実として使わない。
- 便宜的な集まりなので、件数を全体の割合に直さない。版と日付を一緒に書く。

---

<a id="ag-2"></a>
## 全体の地図

次の表は、分冊ごとの資料の数と、使い方の分類ごとの資料の数です。`scripts/build_annotations_appendix.py` が `evidence/annotations_usage/` から自動で作ります（手で直しません）。
分類の数は、1 つの資料に複数の分類が付くので、足しても資料の数になりません。また、この調査で集めた資料の中での数で、製品全体の割合ではありません。

<!-- BEGIN GENERATED（scripts/build_annotations_appendix.py が作る。手で直さない） -->

| 分冊 | 分野 | 資料 | うち [確認] | うち [確認（調査時のみ）] |
|---|---|---|---|---|
| [G-1](appendix-g-1.md) | MCP の公式（仕様・スキーマ・公式サイト・ブログ・SEP・参照サーバ・Inspector） | 61 | 61 | 0 |
| [G-2](appendix-g-2.md) | SDK（サーバを作る道具と、クライアント側のライブラリ） | 63 | 63 | 0 |
| [G-3](appendix-g-3.md) | Microsoft と GitHub | 44 | 42 | 0 |
| [G-4](appendix-g-4.md) | Anthropic（Claude） | 37 | 31 | 0 |
| [G-5](appendix-g-5.md) | OpenAI（ChatGPT・Codex・Apps SDK・Agents SDK） | 52 | 51 | 0 |
| [G-6](appendix-g-6.md) | Google と AWS | 67 | 63 | 0 |
| [G-7](appendix-g-7.md) | エディタとコーディングエージェント | 95 | 76 | 19 |
| [G-8](appendix-g-8.md) | エージェントの枠組み・利用者向けアプリ・モデルの API | 82 | 82 | 0 |
| [G-9](appendix-g-9.md) | サーバの作者と、業務 SaaS のホスト | 85 | 79 | 0 |
| [G-10](appendix-g-10.md) | ゲートウェイ・実行基盤・宣言を検査する道具・登録所 | 145 | 142 | 0 |
| [G-11](appendix-g-11.md) | WebMCP（ブラウザがページのツールを AI に渡す仕組み） | 46 | 43 | 0 |
| [G-12](appendix-g-12.md) | 研究論文・標準・安全の指針 | 43 | 41 | 0 |
| [G-13](appendix-g-13.md) | 記載が無かったページ / 届かなかったページ | 514 / 129 | — | — |
| | **計（G-1〜G-12）** | **820** | **774** | **19** |

使い方の分類ごとの資料の数（1 つの資料に複数の分類が付くので、足しても資料の数にならない）:

| 使い方の分類 | 資料の数 |
|---|---|
| その他 | 176 |
| 宣言が無いときの扱い | 170 |
| 作者への書き方の案内 | 141 |
| 確認を求める | 133 |
| 使わない・読まない | 92 |
| 規則（ポリシー）の条件に使う | 90 |
| ツールを絞る・隠す | 86 |
| そのまま渡す・見せる | 84 |
| 表示（印・名前） | 74 |
| 信頼するなという注意 | 71 |
| 確認を省く（自動で許可） | 71 |
| 宣言を検査する | 68 |
| 危険度を付ける | 35 |
| 宣言を書くことを求める | 25 |

<!-- END GENERATED -->

---

<a id="ag-3"></a>
## 分かったこと

ここが、この付録の芯です。小見出しの番号（3.1 など）は、分冊の番号（G-1 など）とは別です。
どの文にも、裏づけのカードを付けました。[確認（調査時のみ）] と [未確認] のカードに頼るときは、その文の中に印を書きました。
「本書の読み」と書いた部分は、カードの事実から本記録者が引き出した解釈で、調査で見つけた事実ではありません。

### 3.1 仕様と MCP 公式の立場

#### 一言で言うと

MCP の公式は、宣言を「ヒント」とし、「信頼できるサーバ以外のものは信じるな」と決めています。
一方で公式ブログは、最もよくある使い方を「確認の画面を出すか省くかの制御」だと書いています。
どのサーバが「信頼できる」のかは、どこにも定義されていません。

#### 公式の文書が書いていること

| 文書 | 書いていること | カード |
|---|---|---|
| 仕様（2025-03-26・2025-06-18・2025-11-25・2026-07-28・draft の全版） | 「信頼できるサーバから来たものでない限り、クライアントは注釈を信頼できないものとして扱わなければならない（MUST）」。宣言が入った 2025-03-26 版から最新の版まで同じ文です。「信頼できるサーバ」の決め方は定義されていません（不明） | [C01-01](appendix-g-1.md#g-c01-mcp-official-01)〜[C01-05](appendix-g-1.md#g-c01-mcp-official-05) |
| 仕様の概要（Key Principles） | 注釈のような振る舞いの説明は、信頼できるサーバ由来でなければ信頼できないとみなすべき | [C01-07](appendix-g-1.md#g-c01-mcp-official-07)・[C01-08](appendix-g-1.md#g-c01-mcp-official-08) |
| schema の注記 | 注釈の項目はすべてヒントで、振る舞いを忠実に表す保証は無い。信頼できないサーバの注釈でツールの使い方を決めるべきでない | [C01-10](appendix-g-1.md#g-c01-mcp-official-10)・[C01-11](appendix-g-1.md#g-c01-mcp-official-11) |
| schema の既定値 | `destructiveHint` の既定は true、`openWorldHint` の既定は true（`readOnlyHint` は false、`idempotentHint` は false）。どれも約束しない側です | [C01-12](appendix-g-1.md#g-c01-mcp-official-12)・[C01-13](appendix-g-1.md#g-c01-mcp-official-13) |
| 仕様（人の確認） | 「拒否できる人が常にループの中にいるべき（SHOULD）」。注釈で確認を省いてよいとは書いていません | [C01-06](appendix-g-1.md#g-c01-mcp-official-06) |
| 旧 Concepts ページ（2026-03-25 に削除） | 注釈はセキュリティの判断に頼るべきでない。目的の 1 つに「承認の画面を作る助け」を挙げていた | [C01-15](appendix-g-1.md#g-c01-mcp-official-15)・[C01-16](appendix-g-1.md#g-c01-mcp-official-16)・[C01-17](appendix-g-1.md#g-c01-mcp-official-17) |

#### 公式ブログ（2026-03-16）が書いていること

- 注釈の**最もよくある使い方は確認の画面の制御**だと書きます。信頼できるサーバの `readOnlyHint: true` は自動承認されうる（might be）、`destructiveHint: true` は確認を出す、という例です（[C01-21](appendix-g-1.md#g-c01-mcp-official-21)・[C01-33](appendix-g-1.md#g-c01-mcp-official-33)）。
- 例の表では、`readOnlyHint: true` は「確認の画面を省く」、`idempotentHint: true` は「失敗したら再試行してよい」、`openWorldHint: true` は「出力を信頼できない内容として扱う」です。ただし列の名前は「クライアントの動きの例」で、規則ではありません（[C01-23](appendix-g-1.md#g-c01-mcp-official-23)）。
- 信頼できないサーバの `readOnlyHint` は使いようがない、と書きます。確認を省くかの判断は、ヒントを信じるときにしか意味が無いからです（[C01-22](appendix-g-1.md#g-c01-mcp-official-22)）。
- 「サーバは `readOnlyHint: true` と言いながらファイルを消すこともできる」と、宣言のうそを名指しします（[C01-28](appendix-g-1.md#g-c01-mcp-official-28)）。
- 多くのクライアントは「インストールしたこと」を信頼の印にしている、という観察も書きます。調べ方は書かれていません（[C01-24](appendix-g-1.md#g-c01-mcp-official-24)）。
- 既定値（約束しない側）を守る度合いはクライアントでばらばらだ、と認めています（[C01-20](appendix-g-1.md#g-c01-mcp-official-20)）。
- 「注釈で絞り込めるクライアントも、承認の画面に注釈を出すクライアントも無い」とも書きます。これはブログの主張で、調べ方は書かれていません。一緒に出てくる「17%」という数字も出典と分母が書かれておらず、本記録者は検証していません（[C01-25](appendix-g-1.md#g-c01-mcp-official-25)）。なお、ブログより後の版ですが、3.2 節には、利用者や管理者の設定で注釈によってツールを絞り込める製品も載っています（Cursor 3.23.12 の reads / writes の切り替え。[確認（調査時のみ）]。[G2CCM-14](appendix-g-7.md#g-g2-closed-clients-missing-14)）。

#### 公式の部品

- **参照サーバ**: 公式の参照サーバ 7 つのうち 6 つが注釈を書き、fetch だけが書いていません（[C01-39](appendix-g-1.md#g-c01-mcp-official-39)〜[C01-43](appendix-g-1.md#g-c01-mcp-official-43)・[C01-47](appendix-g-1.md#g-c01-mcp-official-47)）。sequentialthinking は、呼ぶたびにサーバの中の履歴に書き足すのに `readOnlyHint: true` と `idempotentHint: true` を宣言しています。これを宣言違反と見るかは解釈が分かれます（不明。[C01-44](appendix-g-1.md#g-c01-mcp-official-44)）。
- **Inspector（公式の開発者向けの道具）**: 注釈は表示だけに使います。v2 は値が真のヒントだけを印にし、既定値（destructive true など）は表示に出ません。v1 は書かれていないヒントを既定値で埋めて「implied」と区別して表示していました（[C01-36](appendix-g-1.md#g-c01-mcp-official-36)・[C01-37](appendix-g-1.md#g-c01-mcp-official-37)・[C01-38](appendix-g-1.md#g-c01-mcp-official-38)）。
- **公式レジストリ・MCPB・適合性テスト**: server.json の schema、MCPB の manifest、適合性テストには、注釈の欄も検査もありませんでした（[付録 G-13](appendix-g-13.md) の MCP 公式の行。[C01-59](appendix-g-1.md#g-c01-mcp-official-59) の補足も同じことを書きます）。

#### 提案（まだ仕様ではないもの）

公式の Interest Group（関心をもつ人の集まり）は、今の 4 つのヒントで足りるか、注釈と信頼・人の確認の関係をどうするかを、まだ答えの出ていない問いとして挙げています（[C01-34](appendix-g-1.md#g-c01-mcp-official-34)・[C01-35](appendix-g-1.md#g-c01-mcp-official-35)）。
実験のリポジトリは「注釈でうそをつくサーバは、レジストリが載せない・ホストが信頼しない、という責任の仕組みで扱う」という立場を書き、既存の 4 つを「legacy hints」と呼んでいます（[C01-59](appendix-g-1.md#g-c01-mcp-official-59)・[C01-61](appendix-g-1.md#g-c01-mcp-official-61)）。
SEP（仕様の変更の提案）には、静的な `destructiveHint: true` が確認の画面を出させすぎて利用者が警告を読まなくなる問題（[C01-48](appendix-g-1.md#g-c01-mcp-official-48)）、危険度の情報が無いツールは最も厳しく扱えという提案（[C01-54](appendix-g-1.md#g-c01-mcp-official-54)）、注釈を門番に使うこと自体を「信頼できない入力に基づくセキュリティ判断」（CWE-807）とみなす提案（[C01-58](appendix-g-1.md#g-c01-mcp-official-58)）があります。どれも提案で、仕様ではありません。

#### この小節のまとめ

公式は「ヒント・信じるな・既定は約束しない側」で一貫していますが、「信頼できるサーバ」の定義は無く、ブログは確認の省略を主な使い道として示しています。公式の登録所や適合性テストは、宣言を検査していません。

---

### 3.2 クライアントは宣言で何をするか

#### 一言で言うと

製品ごとに大きく違います。
`readOnlyHint: true` を見て確認を省く製品があります。ただし多くは、特定のモードや設定のときだけです。
宣言をまったく読まない製品も多くあります。
宣言を、絞り込みや止める方向（制限の方向）にだけ使う製品もあります。

#### 表の読み方

列の意味は次のとおりです。

- **確認を省くか（条件）**: 宣言を見て、確認なしで動かすことがあるか。あるなら、どのモード・設定のときか。
- **確認を求める・隠す**: 宣言を見て、確認を求める・止める・一覧から隠すことがあるか。
- **宣言が無いとき**: 注釈が無い（または該当のヒントが無い）ツールをどう扱うか。
- 「—」はカードに記述が無いこと、「不明」はカードが「分からない」と書いていることです。

表に挙げた製品は、この調査で見つけたものだけです。全製品の標本ではありません。

#### 表 1 — 大手のホスト（Microsoft・GitHub・Anthropic・OpenAI・Google）

| 製品 | 確認を省くか（条件） | 確認を求める・隠す | 宣言が無いとき | カード |
|---|---|---|---|---|
| VS Code（Copilot のエージェントモード） | 省く。`readOnlyHint` が真なら実行前の確認を出さない。例外: sandbox のサーバは注釈に関係なく確認なし、設定でそのツールを自動承認の対象から外すと確認が出る、Allow all・Autopilot では全ツール確認なし | `openWorldHint` が真なら、結果を会話に入れる前の事後確認の対象 | 確認を出す | [C03-01](appendix-g-3.md#g-c03-microsoft-github-01) [C03-03](appendix-g-3.md#g-c03-microsoft-github-03) [C03-05](appendix-g-3.md#g-c03-microsoft-github-05) [C03-06](appendix-g-3.md#g-c03-microsoft-github-06) [C03-04](appendix-g-3.md#g-c03-microsoft-github-04) [C03-07](appendix-g-3.md#g-c03-microsoft-github-07) |
| Microsoft 365 Copilot（宣言型エージェントの MCP プラグイン） | 省く。最初の接続の確認の後は、`readOnlyHint: true` のツールは確認なし | MCP Apps では 4 つのうち `readOnlyHint` だけを扱う | 不明（ページに明記なし） | [C03-30](appendix-g-3.md#g-c03-microsoft-github-30) [C03-31](appendix-g-3.md#g-c03-microsoft-github-31) |
| GitHub Copilot code review | （確認ではなく絞り込み）`readOnlyHint: true` のツールだけを使う | それ以外を除外 | 除外 | [C03-16](appendix-g-3.md#g-c03-microsoft-github-16) [C03-17](appendix-g-3.md#g-c03-microsoft-github-17) |
| GitHub Copilot cloud agent | 許可リストに書いたツールは承認なしで使う。注釈を使うかは不明 | — | 不明 | [C03-18](appendix-g-3.md#g-c03-microsoft-github-18) |
| GitHub Copilot CLI（文書） | 読み取り専用でも明示の許可が要る、と書く（起動時のフラグで事前に許可する道は別にある） | — | — | [C03-19](appendix-g-3.md#g-c03-microsoft-github-19) |
| GitHub Copilot CLI（1.0.63 の実装） | 省く。deny の規則に当たらなければ `readOnlyHint: true` を確認なしで承認 | — | 保存済みの承認か、利用者への確認 | [G2CCM-09](appendix-g-7.md#g-g2-closed-clients-missing-09) [G2CCM-10](appendix-g-7.md#g-g2-closed-clients-missing-10) |
| Claude Code CLI（2.1.287 の実装。[確認（調査時のみ）]） | plan mode の判定の関数には、注釈だけで自動承認する分岐は無い。既定のモードで注釈が確認を省くかは、カードからは不明 | plan mode では `readOnlyHint` が true でない MCP ツールを確認に回す（allow の規則より先） | `readOnlyHint`・`destructiveHint`・`openWorldHint` とも false として扱う。後の 2 つは仕様の既定値と逆 | [G2CCM-01](appendix-g-7.md#g-g2-closed-clients-missing-01) [G2CCM-02](appendix-g-7.md#g-g2-closed-clients-missing-02) [G2CCM-03](appendix-g-7.md#g-g2-closed-clients-missing-03) [G2CCM-04](appendix-g-7.md#g-g2-closed-clients-missing-04) |
| Claude Code CLI（文書） | 注釈で許可が変わるとは書いていない。毎回の確認を強制するのは独自の `_meta["anthropic/requiresUserInteraction"]`（v2.1.199 以降） | `/mcp` の画面に注釈を表示 | — | [C04-27](appendix-g-4.md#g-c04-anthropic-27) [C04-28](appendix-g-4.md#g-c04-anthropic-28) |
| Claude Desktop・Cowork（2.9939.4 の実装） | 省く。Cowork の auto モードでは `readOnlyHint === true` のツールを承認なしで通す（Code タブでは使わない）。承認の設定が "readOnly" のサーバでも省く（この設定を誰がどう決めるかは不明） | `destructiveHint === true` のツールは、auto モードで「常に許可」を使わず判定し直す、watcher（人のいない実行）からの呼び出しを拒否、アーティファクトからの呼び出しで確認を挟む | `readOnlyHint` が無ければ書き込み扱い（止める向き）。`destructiveHint` が無ければ破壊的でない扱い（通してしまう向き） | [G3CAMA-17](appendix-g-8.md#g-g3-consumer-apps-model-apis-17) [G3CAMA-18](appendix-g-8.md#g-g3-consumer-apps-model-apis-18) [G3CAMA-19](appendix-g-8.md#g-g3-consumer-apps-model-apis-19) [G3CAMA-20](appendix-g-8.md#g-g3-consumer-apps-model-apis-20) [G3CAMA-21](appendix-g-8.md#g-g3-consumer-apps-model-apis-21) [G3CAMA-22](appendix-g-8.md#g-g3-consumer-apps-model-apis-22) [G3CAMA-24](appendix-g-8.md#g-g3-consumer-apps-model-apis-24) [G3CAMA-33](appendix-g-8.md#g-g3-consumer-apps-model-apis-33) |
| Cowork（文書） | Auto モードかつツールの権限が Always allow のとき、読み取り専用ツールは承認。組織の設定が off のとき、read-only と宣言されたツールだけが「タスクごとの承認」のしばりから外れる | 書き込みツールはタスクごとの承認 | 宣言が無いと全ツールがしばりの対象 | [C04-08](appendix-g-4.md#g-c04-anthropic-08) [C04-09](appendix-g-4.md#g-c04-anthropic-09) |
| Claude Agent SDK | 確認には使わない。`readOnlyHint` は並列に実行してよいかだけを決める。ほかの 3 つは「Informational only」 | — | 順に（並列にせず）実行 | [C04-13](appendix-g-4.md#g-c04-anthropic-13) [C04-14](appendix-g-4.md#g-c04-anthropic-14) [C04-15](appendix-g-4.md#g-c04-anthropic-15) [C04-16](appendix-g-4.md#g-c04-anthropic-16) |
| ChatGPT の developer mode | `readOnlyHint` で読み取りかを判定する。読み取りが確認なしで走るとはページに明記が無い（書き込みの確認と合わせた推論） | 書き込み扱いのツールは既定で確認 | 書き込み扱い | [C05-19](appendix-g-5.md#g-c05-openai-19) [C05-20](appendix-g-5.md#g-c05-openai-20) [C05-21](appendix-g-5.md#g-c05-openai-21) |
| ChatGPT・Codex（Apps の Reference） | ヒントは呼び出しの見せ方にだけ影響し、認可の代わりにならない、と書く | — | — | [C05-01](appendix-g-5.md#g-c05-openai-01) [C05-03](appendix-g-5.md#g-c05-openai-03) |
| Codex（auto モード。既定） | 省く。`readOnlyHint: true` なら承認なし。読み取り専用でなくても `destructiveHint: false` かつ `openWorldHint: false` なら承認なし | `destructiveHint: true` は `readOnlyHint` より優先して承認 | 欠けたヒントは true として扱い、注釈が無ければ承認 | [C05-34](appendix-g-5.md#g-c05-openai-34) [C05-36](appendix-g-5.md#g-c05-openai-36) [C05-38](appendix-g-5.md#g-c05-openai-38) [C05-39](appendix-g-5.md#g-c05-openai-39) |
| Codex（ほかのモード） | writes モードは `readOnlyHint` だけを見る。approve モードや、条件つきの approval_policy=never は宣言を見ずに通す。strict auto-review では宣言で承認を省かない | prompt モードは常に承認 | — | [C05-31](appendix-g-5.md#g-c05-openai-31) [C05-35](appendix-g-5.md#g-c05-openai-35) [C05-37](appendix-g-5.md#g-c05-openai-37) |
| Codex（apps＝ChatGPT のコネクタ） | — | 利用者の設定で、`destructive_hint`・`open_world_hint` が true のツールを使えなくできる（既定は許可） | 欠けたヒントは true として扱う | [C05-32](appendix-g-5.md#g-c05-openai-32) [C05-40](appendix-g-5.md#g-c05-openai-40) [C05-41](appendix-g-5.md#g-c05-openai-41) |
| OpenAI Responses API | 既定では全呼び出しで承認。開発者が承認の設定に read_only の条件を書くと、`readOnlyHint` 付きのツールを承認なしにできる | — | — | [C05-23](appendix-g-5.md#g-c05-openai-23) [C05-24](appendix-g-5.md#g-c05-openai-24) |
| Gemini CLI | 既定のモードでは注釈で自動許可しない。利用者が規則を足したときと、実験的なブラウザエージェントの `readOnlyHint` のツールだけ自動許可 | Plan Mode では `readOnlyHint = true` の MCP ツールだけを確認つきで使え、それ以外は拒否してモデルから隠す | Plan Mode では拒否 | [C06-01](appendix-g-6.md#g-c06-google-aws-01) [C06-02](appendix-g-6.md#g-c06-google-aws-02) [C06-04](appendix-g-6.md#g-c06-google-aws-04) [C06-05](appendix-g-6.md#g-c06-google-aws-05) [C06-07](appendix-g-6.md#g-c06-google-aws-07) [C06-10](appendix-g-6.md#g-c06-google-aws-10) |
| Gemini Enterprise（カスタム MCP の actions） | 省く。`readOnlyHint` を付けたツールは確認を飛ばす | `destructiveHint` を付ければ既定の確認のまま | 全部確認 | [C06-19](appendix-g-6.md#g-c06-google-aws-19) [C06-20](appendix-g-6.md#g-c06-google-aws-20) |
| Gemini アプリ（消費者向け） | 不明 | 書き込みの操作は手動の確認。何を書き込みとみなすかは不明 | 不明 | [G3CAMA-01](appendix-g-8.md#g-g3-consumer-apps-model-apis-01) |
| Google Cloud のマネージド MCP サーバ（IAM） | — | 管理者が deny のポリシーを付けると、「読み取り専用と注記されていない」ツールの呼び出しを拒否 | 拒否側（属性が無ければ false） | [C06-13](appendix-g-6.md#g-c06-google-aws-13) [C06-14](appendix-g-6.md#g-c06-google-aws-14) [C06-15](appendix-g-6.md#g-c06-google-aws-15) |
| Gemini Enterprise Agent Platform の Agent Gateway | 4 つの属性を IAM の条件に使える。値はサーバに聞かず、登録簿に登録した toolspec.json から引く | 例: 書き込みツールを 403 で止める | 例の式では読み取り専用の値が無いと許可しない | [C06-21](appendix-g-6.md#g-c06-google-aws-21) [C06-22](appendix-g-6.md#g-c06-google-aws-22) [C06-23](appendix-g-6.md#g-c06-google-aws-23) [C06-25](appendix-g-6.md#g-c06-google-aws-25) |

#### 表 2 — エディタとコーディングエージェント

| 製品 | 確認を省くか（条件） | 確認を求める・隠す | 宣言が無いとき | カード |
|---|---|---|---|---|
| Cursor（3.23.12 の実装。[確認（調査時のみ）]） | 管理者が許可リストを reads モードにすると、`readOnlyHint: true` かつ `destructiveHint` が true でないツールは確認なしで走る。Smart mode の分類器（自動実行してよいかを決める仕組み）に注釈を渡す | reads モードではそれ以外を無効にする。独自のキー `cursor/requiresConfirmation` があれば承認を省かない | 「注釈なし」として書き込み側。reads モードでは無効 | [G2CCM-12](appendix-g-7.md#g-g2-closed-clients-missing-12) [G2CCM-13](appendix-g-7.md#g-g2-closed-clients-missing-13) [G2CCM-14](appendix-g-7.md#g-g2-closed-clients-missing-14) [G2CCM-15](appendix-g-7.md#g-g2-closed-clients-missing-15) [G2CCM-16](appendix-g-7.md#g-g2-closed-clients-missing-16) [G2CCM-35](appendix-g-7.md#g-g2-closed-clients-missing-35) |
| Cursor（公開文書・SDK） | SDK は注釈をモデルに渡すだけで、何も強制しないと書く | 自社の Origin MCP は独自の `_meta` で毎回承認 | — | [C07-22](appendix-g-7.md#g-c07-ide-agents-22) [C07-23](appendix-g-7.md#g-c07-ide-agents-23) |
| goose | 利用者が Smart Approve モードを選んだときだけ、`readOnlyHint: true` を承認なしにする（ほかの検査の確認・拒否には負ける）。既定の Autonomous モードは注釈に関係なく全部許可 | `readOnlyHint: false` は毎回確認 | LLM の判定に回る | [C07-01](appendix-g-7.md#g-c07-ide-agents-01) [C07-02](appendix-g-7.md#g-c07-ide-agents-02) [C07-03](appendix-g-7.md#g-c07-ide-agents-03) |
| Devin CLI | v3000.3.22 の changelog: Plan モードは `readOnlyHint: true` の MCP ツールだけを許可。後の版で今も続くかは不明 | — | Plan モードでは使えない | [C07-21](appendix-g-7.md#g-c07-ide-agents-21) |
| Devin Desktop（3.10.48 の実装。[確認（調査時のみ）]） | — | ある制限モードでは `readOnlyHint` のツールだけ呼べる。設定画面で Read-only / Write に分けて表示 | Write 側。制限モードでは呼べない | [G2CCM-17](appendix-g-7.md#g-g2-closed-clients-missing-17) [G2CCM-18](appendix-g-7.md#g-g2-closed-clients-missing-18) |
| Docker Agent（cagent） | balanced と restricted のモードでは、`readOnlyHint: true`（かつ `destructiveHint` が true でない）のツールは確認なし。モードを選んでいない既定でも宣言だけで自動承認 | restricted では注釈の無いツールと破壊的なツールを拒否 | 「不明」の分類。`destructiveHint` が書かれていなければ false として扱う | [C07-06](appendix-g-7.md#g-c07-ide-agents-06) [C07-07](appendix-g-7.md#g-c07-ide-agents-07) [C07-08](appendix-g-7.md#g-c07-ide-agents-08) [C07-09](appendix-g-7.md#g-c07-ide-agents-09) |
| Qwen Code | auto mode の分類器に注釈を渡すが、「注釈だけで許可しない」と指示している | 接続が切れた呼び出しを自動で送り直してよいかを、`idempotentHint` などで決める | 送り直さない | [C07-11](appendix-g-7.md#g-c07-ide-agents-11) [C07-12](appendix-g-7.md#g-c07-ide-agents-12) [C07-13](appendix-g-7.md#g-c07-ide-agents-13) [C07-14](appendix-g-7.md#g-c07-ide-agents-14) |
| OpenHands SDK | 既定（NeverConfirm）では注釈は確認に関係しない | 設定によっては、読み取り専用のツールのリスクが「不明」になり、確認の対象になる | — | [C07-18](appendix-g-7.md#g-c07-ide-agents-18) [C07-19](appendix-g-7.md#g-c07-ide-agents-19) |
| Qoder CLI | 許可の判断から意図して外す。`readOnlyHint` は並行実行と表示の印だけ | — | — | [G3AA-01](appendix-g-7.md#g-g3-asia-agents-01) [G3AA-04](appendix-g-7.md#g-g3-asia-agents-04) [G3AA-13](appendix-g-7.md#g-g3-asia-agents-13) |
| CodeBuddy Code | 注釈で確認が省かれる道は無い（LLM のレビューは既定で無効。有効でも確認を足すだけ） | レビューに注釈を証拠として渡す | — | [G3AA-16](appendix-g-7.md#g-g3-asia-agents-16) [G3AA-17](appendix-g-7.md#g-g3-asia-agents-17) [G3AA-18](appendix-g-7.md#g-g3-asia-agents-18) |
| Zed | 使わない。承認は設定とツール名だけ | — | — | [G2CCM-30](appendix-g-7.md#g-g2-closed-clients-missing-30) [G2CCM-31](appendix-g-7.md#g-g2-closed-clients-missing-31) |
| JetBrains Junie | 使わない。MCP ツールは一律に承認の対象 | — | — | [G2CCM-32](appendix-g-7.md#g-g2-closed-clients-missing-32) [G2CCM-33](appendix-g-7.md#g-g2-closed-clients-missing-33) |
| Google Antigravity | 使わない。MCP ツールの既定は一律に Ask、許可は名前のパターン | — | — | [G2CCM-20](appendix-g-7.md#g-g2-closed-clients-missing-20) [G2CCM-21](appendix-g-7.md#g-g2-closed-clients-missing-21) |
| Mistral Vibe | 読まない。対話の既定は ASK、非対話の既定は全部自動承認 | — | — | [G2CCM-24](appendix-g-7.md#g-g2-closed-clients-missing-24) [G2CCM-25](appendix-g-7.md#g-g2-closed-clients-missing-25) |
| Kimi Code・iFlow CLI | 使わない（一覧を受け取る段で捨てる／trust の設定と許可リストだけ） | — | — | [G3AA-19](appendix-g-7.md#g-g3-asia-agents-19) [G3AA-20](appendix-g-7.md#g-g3-asia-agents-20) |
| Cline・Roo Code・Kilo Code・OpenCode・Continue・LibreChat・Open WebUI・Warp | 使わない。自動承認は名前の一覧や設定で決まる | — | Continue は MCP ツールを宣言に関係なく読み取り専用でないとして扱う | [C07-25](appendix-g-7.md#g-c07-ide-agents-25) [C07-26](appendix-g-7.md#g-c07-ide-agents-26) [C07-27](appendix-g-7.md#g-c07-ide-agents-27) [C07-28](appendix-g-7.md#g-c07-ide-agents-28) [C07-29](appendix-g-7.md#g-c07-ide-agents-29) [C07-30](appendix-g-7.md#g-c07-ide-agents-30) [C07-32](appendix-g-7.md#g-c07-ide-agents-32) [C07-33](appendix-g-7.md#g-c07-ide-agents-33) [C07-34](appendix-g-7.md#g-c07-ide-agents-34) |
| Amazon Q Developer CLI | 文書は「承認の前に注釈を見よ」と書くが、オープンソース版の実装は注釈を写さない | — | — | [C06-60](appendix-g-6.md#g-c06-google-aws-60) [C06-62](appendix-g-6.md#g-c06-google-aws-62) |
| Grok Build（xAI） | 文書に注釈の記述が無い。plan mode でも MCP ツールは通常の権限に従う | — | — | [G3CAMA-06](appendix-g-8.md#g-g3-consumer-apps-model-apis-06) [G3CAMA-07](appendix-g-8.md#g-g3-consumer-apps-model-apis-07) |

#### 表 3 — 業務アプリ・自動化の基盤・枠組み・モデルの API

| 製品 | 確認を省くか（条件） | 確認を求める・隠す | 宣言が無いとき | カード |
|---|---|---|---|---|
| n8n（Instance AI） | 既定の設定（read 類は always_allow）では、read に分類されたツールは承認なし。`readOnlyHint: true` は名前より優先して read になる | write 類は承認待ち、blocked は一覧から除外 | 名前で推定し、決まらなければ write | [C07-04](appendix-g-7.md#g-c07-ide-agents-04) [C07-05](appendix-g-7.md#g-c07-ide-agents-05) [C08-01](appendix-g-8.md#g-c08-frameworks-01) [C08-02](appendix-g-8.md#g-c08-frameworks-02) [C08-03](appendix-g-8.md#g-c08-frameworks-03) [C08-04](appendix-g-8.md#g-c08-frameworks-04) |
| AgentScope | 省く。`readOnlyHint: true` の MCP ツールは、すべての許可モードで確認なし（利用者の deny・ask の規則が先） | それ以外は確認 | 読み取り専用でない扱い | [G3AA-21](appendix-g-7.md#g-g3-asia-agents-21) [G3AA-22](appendix-g-7.md#g-g3-asia-agents-22) [G3AA-23](appendix-g-7.md#g-g3-asia-agents-23) [G3AA-24](appendix-g-7.md#g-g3-asia-agents-24) |
| LeapFlow（ModelScope） | 既定のモードでは、`readOnlyHint` を宣言したツールは審査を通さずに許可 | 宣言の無いツールは高いリスクとして確認 | 確認 | [G2RM-16](appendix-g-10.md#g-g2-registries-marketplaces-16) [G2RM-17](appendix-g-10.md#g-g2-registries-marketplaces-17) [G2RM-18](appendix-g-10.md#g-g2-registries-marketplaces-18) [G2RM-19](appendix-g-10.md#g-g2-registries-marketplaces-19) |
| TrueForge | 既定では、注釈で write・destructive と分かるツールだけ承認を求め、読み取り専用は承認なし | — | 承認なしで動く（文書自身が明記） | [G2GP-08](appendix-g-10.md#g-g2-gateways-platforms-08) [G2GP-09](appendix-g-10.md#g-g2-gateways-platforms-09) [G2GP-10](appendix-g-10.md#g-g2-gateways-platforms-10) [G2GP-11](appendix-g-10.md#g-g2-gateways-platforms-11) |
| TrueFoundry AI Gateway | — | 管理者が承認の範囲を destructive にすると、`destructiveHint: true` のツールを承認待ちにする | 文書に書かれていない（不明） | [G2GP-03](appendix-g-10.md#g-g2-gateways-platforms-03) [G2GP-04](appendix-g-10.md#g-g2-gateways-platforms-04) |
| Slack（Slackbot） | 「分類のメタデータを付ければ read-only のツールは追加の不要な確認なしに動く」と書く一方、「第三者のツールは読みも書きも呼び出しごとに許可」とも書く（食い違い。不明） | 読み / 書きの分類は `readOnlyHint` の値で決まる | 書き込みに分類 | [G3SH-01](appendix-g-9.md#g-g3-saas-hosts-01) [G3SH-02](appendix-g-9.md#g-g3-saas-hosts-02) [G3SH-03](appendix-g-9.md#g-g3-saas-hosts-03) |
| Notion（Custom Agents） | 文書は「read-only でないツールには既定で確認」と書く。read-only が確認なしだというのは、その裏返しの読み | 書き込みツールは既定で Always ask。注釈は設定画面に表示し、Notion は検証していないと明言 | 不明 | [G3SH-06](appendix-g-9.md#g-g3-saas-hosts-06) [G3SH-07](appendix-g-9.md#g-g3-saas-hosts-07) [G3SH-08](appendix-g-9.md#g-g3-saas-hosts-08) |
| Dust | 使わない。独自の「stake」で決める | リモートのツールは既定で毎回承認 | — | [G3SH-21](appendix-g-9.md#g-g3-saas-hosts-21) [G3SH-23](appendix-g-9.md#g-g3-saas-hosts-23) |
| HubSpot・Atlassian Rovo・Zapier・Langdock・Glean・ServiceNow | 文書に注釈の語が無い。読み / 書きの区分を持つ製品もあるが、区分の根拠は書かれていない（不明） | — | Zapier と Langdock は承認の既定がオフ、ServiceNow の手引きは既定が autopilot | [G3SH-27](appendix-g-9.md#g-g3-saas-hosts-27) [G3SH-24](appendix-g-9.md#g-g3-saas-hosts-24) [G3SH-25](appendix-g-9.md#g-g3-saas-hosts-25) [G3SH-29](appendix-g-9.md#g-g3-saas-hosts-29) [G3SH-28](appendix-g-9.md#g-g3-saas-hosts-28) [G3SH-31](appendix-g-9.md#g-g3-saas-hosts-31) |
| Vercel AI SDK | SDK 自身は注釈を承認に変えない。文書の例は `readOnlyHint === true` だけ自動、それ以外は承認 | — | 例では承認 | [C02-47](appendix-g-2.md#g-c02-sdks-47) [C02-49](appendix-g-2.md#g-c02-sdks-49) [C08-07](appendix-g-8.md#g-c08-frameworks-07) |
| Mastra | 既定（承認の関数を渡さない）では注釈に関係なく全部承認なし。関数を書けば注釈を判断に使える | 例: `destructiveHint` なら承認 | 例: 注釈が無ければ承認 | [C02-59](appendix-g-2.md#g-c02-sdks-59) [C02-60](appendix-g-2.md#g-c02-sdks-60) [C08-05](appendix-g-8.md#g-c08-frameworks-05) [C08-06](appendix-g-8.md#g-c08-frameworks-06) |
| TanStack AI | 既定では全ツール承認なし。自分で信頼すると決めたサーバでだけ、ヒントで確認を緩めてよいと書く | 例の絞り込みは `readOnlyHint === true` だけをモデルに見せる | 例では見せない | [C02-53](appendix-g-2.md#g-c02-sdks-53) [C02-54](appendix-g-2.md#g-c02-sdks-54) [C02-55](appendix-g-2.md#g-c02-sdks-55) |
| LangChain | アダプタは注釈を写すだけ。文書の例は `destructive_hint` で人の承認を求める | — | 例は欠落を「破壊的でない」として扱う | [C02-50](appendix-g-2.md#g-c02-sdks-50) [C02-51](appendix-g-2.md#g-c02-sdks-51) [C02-52](appendix-g-2.md#g-c02-sdks-52) |
| Pydantic AI | 承認には使わない。先回りの実行（speculate）の対象選びに `readOnlyHint` を使う。harness の read_only=True は `readOnlyHint: true` のツールだけを残す | — | 絞り込みでは外す | [C02-58](appendix-g-2.md#g-c02-sdks-58) [C08-30](appendix-g-8.md#g-c08-frameworks-30) [C08-32](appendix-g-8.md#g-c08-frameworks-32) |
| AutoGen・Agno（クライアント）・Cloudflare Agents SDK・Google ADK・Strands・google-genai・OpenRouter | 使わない、または渡すだけ | — | — | [C08-13](appendix-g-8.md#g-c08-frameworks-13) [C08-12](appendix-g-8.md#g-c08-frameworks-12) [C08-14](appendix-g-8.md#g-c08-frameworks-14) [C06-41](appendix-g-6.md#g-c06-google-aws-41) [C06-45](appendix-g-6.md#g-c06-google-aws-45) [G3CAMA-11](appendix-g-8.md#g-g3-consumer-apps-model-apis-11) [G3CAMA-41](appendix-g-8.md#g-g3-consumer-apps-model-apis-41) |
| OpenAI Agents SDK | Hosted MCP（Responses API 側で動く）では読み取り専用の条件を API に渡すだけ。ローカルの MCP サーバの承認の条件に注釈を使うとは書いていない | — | — | [C05-27](appendix-g-5.md#g-c05-openai-27) [C05-28](appendix-g-5.md#g-c05-openai-28) |
| xAI・Groq・Perplexity の API・Mistral Studio | 注釈で確認を切り替える仕組みは書かれていない。Groq は承認の既定が「never」、Perplexity は承認の仕組み自体が無い | — | — | [G3CAMA-03](appendix-g-8.md#g-g3-consumer-apps-model-apis-03) [G3CAMA-09](appendix-g-8.md#g-g3-consumer-apps-model-apis-09) [G2CCM-29](appendix-g-7.md#g-g2-closed-clients-missing-29) [G2CCM-27](appendix-g-7.md#g-g2-closed-clients-missing-27) |

#### 表から読めるパターン

表の中には、おおよそ 4 つの型が見えます。数は数えません（便宜的な集まりなので、数えても全体の割合にはならないためです）。

1. **`readOnlyHint: true` で確認を省く型。** VS Code、Microsoft 365 Copilot、Copilot CLI（1.0.63）、Codex、Gemini Enterprise、Cowork の auto モード、n8n、AgentScope、LeapFlow、Docker Agent、TrueForge などです。ただし、**多くはモードや設定の条件つき**です。goose は Smart Approve を選んだときだけ、Cowork は auto モードのときだけ、Cursor は管理者が reads モードにしたときだけ（[確認（調査時のみ）]）です（[C07-02](appendix-g-7.md#g-c07-ide-agents-02)・[G3CAMA-18](appendix-g-8.md#g-g3-consumer-apps-model-apis-18)・[G2CCM-35](appendix-g-7.md#g-g2-closed-clients-missing-35)）。
2. **宣言で絞り込む・隠す型。** Copilot code review、Gemini CLI の Plan Mode、Devin CLI の Plan モード、各種のサーバの read-only モードです（[C03-16](appendix-g-3.md#g-c03-microsoft-github-16)・[C06-04](appendix-g-6.md#g-c06-google-aws-04)・[C07-21](appendix-g-7.md#g-c07-ide-agents-21)・3.6 節）。この型でも、`readOnlyHint: true` のうそは絞り込みをすり抜けます（[C03-16](appendix-g-3.md#g-c03-microsoft-github-16) の補足）。
3. **宣言を読まない型。** Zed、Junie、Antigravity、Mistral Vibe、Kimi Code、Cline などです。Qoder は「サーバの自己申告は検証できないので、許可の判断に入れない」と理由まで書いています（[G3AA-04](appendix-g-7.md#g-g3-asia-agents-04)）。
4. **制限の方向にだけ使う型。** Qwen Code は分類器に「注釈は疑いを増やす方向にだけ使え」と指示し（[C07-12](appendix-g-7.md#g-c07-ide-agents-12)）、Microsoft Agent Framework の FIDES は「注釈は制限を強める方向にしか効かない」と設計しています（[C03-37](appendix-g-3.md#g-c03-microsoft-github-37)）。

また、エージェントの枠組み（Vercel、Mastra、TanStack など）は、**既定では注釈で何もせず**、文書に「こう書けば注釈で承認を決められる」という例を載せるだけです（[C02-49](appendix-g-2.md#g-c02-sdks-49)・[C08-05](appendix-g-8.md#g-c08-frameworks-05)・[C02-54](appendix-g-2.md#g-c02-sdks-54)）。
同じ製品の中でも、`readOnlyHint` は確認に使い、`destructiveHint` は別の門にだけ使う、というように宣言ごとに扱いが違います（[G3CAMA-18](appendix-g-8.md#g-g3-consumer-apps-model-apis-18)・[G3CAMA-22](appendix-g-8.md#g-g3-consumer-apps-model-apis-22)）。

#### この小節のまとめ

確認を省く製品は実在しますが、ほとんどがモード・設定の条件つきです。読まない製品も、制限の方向にだけ使う製品もあります。「クライアントは宣言で確認を省く」と一言でまとめず、製品・版・モードを添えて書きます。

---

### 3.3 宣言が無いときの扱いは製品で逆を向く

#### 一言で言うと

仕様の既定値は「約束しない側」です。`destructiveHint` を書かなければ「壊すかもしれない」です。
ところが、`destructiveHint === true`（値がちょうど true のときだけ真）のように比べる実装では、**書いていないツールが「壊さない」側に入ります。**
宣言が無いときに止める製品と、通してしまう製品が、両方あります。

#### 小さな例 — `=== true` の比べ方

JavaScript の `x === true` は、「x がちょうど true のときだけ真」です。x が書かれていない（undefined）ときは偽になります。
だから「`destructiveHint === true` なら確認する」と書くと、`destructiveHint` を書いていないツールは確認されません。
仕様の既定値（書いていなければ true）を当てはめれば確認されるはずのツールが、通ってしまいます。
これが「宣言が無いと通してしまう向き」（fail-open）です。

#### 表 — 宣言が無いときの向き

| 向き | 製品と扱い | カード |
|---|---|---|
| 止める向き（fail-safe） | VS Code: `readOnlyHint` が無ければ確認 | [C03-05](appendix-g-3.md#g-c03-microsoft-github-05) [C03-06](appendix-g-3.md#g-c03-microsoft-github-06) |
| 止める向き | Codex: 欠けたヒントは true とみなし、注釈が無ければ承認 | [C05-34](appendix-g-5.md#g-c05-openai-34) [C05-39](appendix-g-5.md#g-c05-openai-39) [C05-40](appendix-g-5.md#g-c05-openai-40) |
| 止める向き | ChatGPT の developer mode: ヒントが無ければ書き込み扱い | [C05-19](appendix-g-5.md#g-c05-openai-19) |
| 止める向き | Gemini Enterprise: 既定で全部確認。Gemini CLI の Plan Mode: 拒否 | [C06-19](appendix-g-6.md#g-c06-google-aws-19) [C06-05](appendix-g-6.md#g-c06-google-aws-05) |
| 止める向き | Google Cloud の IAM: 属性が無ければ false として拒否側 | [C06-15](appendix-g-6.md#g-c06-google-aws-15) |
| 止める向き | Slack: 分類が無ければ書き込み | [G3SH-02](appendix-g-9.md#g-g3-saas-hosts-02) |
| 止める向き | Copilot code review: 除外 | [C03-16](appendix-g-3.md#g-c03-microsoft-github-16) |
| 止める向き | ToolHive（ゲートウェイ）: 注釈が無いと規則の評価が誤りになり拒否。Safe tools のプロファイルは注釈なしを拒否 | [C09-22](appendix-g-10.md#g-c09-servers-gateways-security-22) [C09-23](appendix-g-10.md#g-c09-servers-gateways-security-23) |
| 止める向き | Hugging Face の MCP サーバ: 中継するツールに、仕様の既定と同じ保守的な値を明示して載せる | [C08-08](appendix-g-8.md#g-c08-frameworks-08) |
| 止める向き | PostHog（中継）・LeapFlow・Claude Agent SDK（並列にしない）・Qwen Code（送り直さない） | [G3VS-28](appendix-g-9.md#g-g3-vendor-servers-28) [G2RM-18](appendix-g-10.md#g-g2-registries-marketplaces-18) [C04-14](appendix-g-4.md#g-c04-anthropic-14) [C07-14](appendix-g-7.md#g-c07-ide-agents-14) |
| 通してしまう向き（fail-open） | Claude Desktop: `destructiveHint` を `=== true` で比べるので、書いていないツールは破壊的でない扱い。watcher からの実行やアーティファクトからの確認をすり抜ける | [G3CAMA-17](appendix-g-8.md#g-g3-consumer-apps-model-apis-17) [G3CAMA-22](appendix-g-8.md#g-g3-consumer-apps-model-apis-22) [G3CAMA-24](appendix-g-8.md#g-g3-consumer-apps-model-apis-24) |
| 通してしまう向き | Claude Code CLI 2.1.287: `destructiveHint`・`openWorldHint` が無ければ false。auto mode では MCP サーバのポリシーの ask の規則でも確認を強制しない側に入る（[確認（調査時のみ）]） | [G2CCM-02](appendix-g-7.md#g-g2-closed-clients-missing-02) [G2CCM-34](appendix-g-7.md#g-g2-closed-clients-missing-34) |
| 通してしまう向き | TrueForge: 注釈の無いツールは承認なしで動くと、文書・CHANGELOG・コードで明記。Code Mode の門も注釈が無ければ通す | [G2GP-09](appendix-g-10.md#g-g2-gateways-platforms-09) [G2GP-11](appendix-g-10.md#g-g2-gateways-platforms-11) [G2GP-13](appendix-g-10.md#g-g2-gateways-platforms-13) [G2GP-15](appendix-g-10.md#g-g2-gateways-platforms-15) |
| 通してしまう向き | LangChain の文書の例: `destructive_hint` が無ければ False（破壊的でない）として承認なし | [C02-51](appendix-g-2.md#g-c02-sdks-51) |
| 通してしまう向き | Docker Agent: `destructiveHint` が書かれていなければ false として渡す | [C07-06](appendix-g-7.md#g-c07-ide-agents-06) |
| 通してしまう向き | kubernetes-mcp-server: `disable_destructive` のモードで、`destructiveHint` が無いツールは残る。確認の規則も当たらない | [G3VS-02](appendix-g-9.md#g-g3-vendor-servers-02) [G3VS-05](appendix-g-9.md#g-g3-vendor-servers-05) |
| 通してしまう向き | Gemini CLI のポリシー: 値をちょうど比べるので、`destructiveHint = true` の規則は書いていないツールに当たらない（カードの記録者のコードの読み） | [C06-06](appendix-g-6.md#g-c06-google-aws-06) |
| 通してしまう向き | Speakeasy Gram: 書いていないヒントは false と同じ。破壊的なツールにだけ掛けるリスクの規則は、書いていないツールに掛からない | [C09-29](appendix-g-10.md#g-c09-servers-gateways-security-29) [C09-30](appendix-g-10.md#g-c09-servers-gateways-security-30) |
| 通してしまう向き | MCPProxy: 現行のコードは注釈なしを「読み取り」に倒す（ブログは「書き込み」と書いていて食い違う） | [G2GP-37](appendix-g-10.md#g-g2-gateways-platforms-37) [G2GP-40](appendix-g-10.md#g-g2-gateways-platforms-40) [G2GP-41](appendix-g-10.md#g-g2-gateways-platforms-41) |
| 通してしまう向き | n8n: 注釈が無くても、名前が読み取り系なら既定で承認なし | [C07-05](appendix-g-7.md#g-c07-ide-agents-05) [C08-02](appendix-g-8.md#g-c08-frameworks-02) |
| 通してしまう向き | Permit（ゲートウェイ）: 名前のキーワードに当たらなければ最も低い「読み取り」レベル | [G2GP-25](appendix-g-10.md#g-g2-gateways-platforms-25) |
| 通してしまう向き | MCP Toolbox: 読み取り専用モードでも、`readOnlyHint` が無いツールは隠さず警告だけ（書き込みは DB 側で止める設計） | [C06-35](appendix-g-6.md#g-c06-google-aws-35) [C06-36](appendix-g-6.md#g-c06-google-aws-36) |
| 見せ方が逆 | Nacos の旧管理画面: 書いていない `destructiveHint` を緑の「No」と表示 | [G2RM-04](appendix-g-10.md#g-g2-registries-marketplaces-04) |

同じ製品の中で向きが分かれることもあります。Claude Desktop は `readOnlyHint` が無ければ止める向き、`destructiveHint` が無ければ通してしまう向きです（[G3CAMA-17](appendix-g-8.md#g-g3-consumer-apps-model-apis-17)）。kubernetes-mcp-server も同じ非対称です（[G3VS-02](appendix-g-9.md#g-g3-vendor-servers-02)）。MCPProxy は、欠落を「読み取り」とする写し方と「未注釈」とする写し方を、同じ製品の中に両方持っています（[G2GP-43](appendix-g-10.md#g-g2-gateways-platforms-43)）。

#### 仕様との関係

仕様は既定値を決めていますが、公式ブログは「既定値をどこまで守るかはクライアントでばらばら」と認めています（[C01-20](appendix-g-1.md#g-c01-mcp-official-20)）。
TrueForge のカードの補足は、仕様がクライアントに既定値の適用を義務づけてはいない、と書いています（[G2GP-09](appendix-g-10.md#g-g2-gateways-platforms-09)）。
なお WebMCP（3.7 節）の注釈は、既定値が 4 つとも false で、MCP とは向きが違います（[G2W-01](appendix-g-11.md#g-g2-webmcp-01)）。

#### この小節のまとめ

「宣言が無いツールは仕様の既定値で慎重に扱われる」とは言えません。`=== true` の比べ方で、書いていない `destructiveHint` が「壊さない」側に入る実装が、大手のホストにもあります（[G3CAMA-17](appendix-g-8.md#g-g3-consumer-apps-model-apis-17)）。

---

### 3.4 送られてくる値が作者の宣言とは限らない

#### 一言で言うと

クライアントが受け取る注釈の値は、作者が書いた値とは限りません。
SDK が既定値を埋めて送ることがあります。ゲートウェイや登録所が書き換えたり落としたりすることがあります。
サーバの側でも、HTTP のメソッドや名前から機械的に値を決めることがあります。

#### SDK が埋める値

「ワイヤー」とは、サーバとクライアントの間を実際に流れるデータのことです。

| SDK | 作者が書かなかったヒントはどう送られるか | カード |
|---|---|---|
| Python・TypeScript・Java・Kotlin・C#・Swift・PHP・Rust の公式 SDK | 送らない（既定値を埋めない） | [C02-03](appendix-g-2.md#g-c02-sdks-03) [C02-18](appendix-g-2.md#g-c02-sdks-18) [C02-19](appendix-g-2.md#g-c02-sdks-19) [C02-24](appendix-g-2.md#g-c02-sdks-24) [C02-28](appendix-g-2.md#g-c02-sdks-28) [C02-37](appendix-g-2.md#g-c02-sdks-37) [C02-41](appendix-g-2.md#g-c02-sdks-41) [C02-36](appendix-g-2.md#g-c02-sdks-36) |
| Go の公式 SDK（v1.7.0 以降） | ToolAnnotations を付けたツールでは、`readOnlyHint`・`idempotentHint` を書かなくても false を送る（false と未設定を区別できない） | [C02-30](appendix-g-2.md#g-c02-sdks-30) [C02-31](appendix-g-2.md#g-c02-sdks-31) |
| Spring AI（@McpTool） | 作者が何も書かなくても 4 つとも既定値を明示して送る（Java の注釈の言語仕様からの推論） | [C02-20](appendix-g-2.md#g-c02-sdks-20) [C02-21](appendix-g-2.md#g-c02-sdks-21) |
| mcp-go（NewTool） | 4 つとも既定値を明示して送る | [C02-33](appendix-g-2.md#g-c02-sdks-33) |
| Ruby・Quarkus | 一部でも宣言すると、残りを既定値で埋めて送る（Quarkus は何も宣言しなければ送らない） | [C02-39](appendix-g-2.md#g-c02-sdks-39) [C02-45](appendix-g-2.md#g-c02-sdks-45) [C02-46](appendix-g-2.md#g-c02-sdks-46) |
| FastMCP の ResourcesAsTools | 変換で作るツールに `readOnlyHint=True` を自動で付ける | [C02-13](appendix-g-2.md#g-c02-sdks-13) |

ある論文も、ワイヤーの上で注釈を出しているツールの多くは SDK の既定値や雛形から来ているかもしれず、作者が選んだ値とは限らない、と注意しています（論文の記載。本記録者は検証していない。[C10-03](appendix-g-12.md#g-c10-research-standards-03)）。

#### ゲートウェイ・登録所が書き換える・落とす

| 何が起きるか | 製品 | カード |
|---|---|---|
| 運用者が注釈を書き換えて、クライアントに見せる | TrueFoundry、Zuplo（例は請求書を作るツールに `destructiveHint: false`）、ToolHive の vMCP、MetaMCP、IBM ContextForge、Speakeasy Gram（管理者の値がベンダーの値より優先）、Kong（設定者が REST の窓口ごとに書く） | [G2GP-01](appendix-g-10.md#g-g2-gateways-platforms-01) [G2GP-21](appendix-g-10.md#g-g2-gateways-platforms-21) [C09-26](appendix-g-10.md#g-c09-servers-gateways-security-26) [C09-34](appendix-g-10.md#g-c09-servers-gateways-security-34) [C09-32](appendix-g-10.md#g-c09-servers-gateways-security-32) [C09-28](appendix-g-10.md#g-c09-servers-gateways-security-28) [G2RM-10](appendix-g-10.md#g-g2-registries-marketplaces-10) |
| 管理者が登録簿に書いた値で判定する | Google の Agent Gateway（toolspec.json） | [C06-24](appendix-g-6.md#g-c06-google-aws-24) |
| false が落ちて「未設定」と同じになる | Docker の MCP カタログの生成 | [C09-35](appendix-g-10.md#g-c09-servers-gateways-security-35) |
| false を書けない | Nacos の新しい管理画面（true だけを保存） | [G2RM-05](appendix-g-10.md#g-g2-registries-marketplaces-05) |
| 注釈を落とす | Stripe のローカル中継、mcp-gateway-registry、Smithery の Registry API、Dify、Cloudflare の WebMCP アダプタ（`readOnlyHint` 以外）、Eino（Go の型で false が消える） | [C09-17](appendix-g-10.md#g-c09-servers-gateways-security-17) [G2GP-23](appendix-g-10.md#g-g2-gateways-platforms-23) [G2RM-08](appendix-g-10.md#g-g2-registries-marketplaces-08) [G2GP-30](appendix-g-10.md#g-g2-gateways-platforms-30) [C08-15](appendix-g-8.md#g-c08-frameworks-15) [G3AA-25](appendix-g-7.md#g-g3-asia-agents-25) |
| 一律の値にする | LiteLLM（全ツール read_only: False）、Hugging Face（中継は固定の保守的な値） | [C08-23](appendix-g-8.md#g-c08-frameworks-23) [C08-09](appendix-g-8.md#g-c08-frameworks-09) |
| 上流の値の一部だけを使い、残りを付け直す | Composio（`readOnlyHint` だけ上流から取り、破壊的かは自前で分類） | [G2GP-46](appendix-g-10.md#g-g2-gateways-platforms-46) |
| 提出時点の値で固まる | ChatGPT への提出（再提出まで反映されない、とサーバ作者が書く）、M365 の manifest への写し | [C09-07](appendix-g-10.md#g-c09-servers-gateways-security-07) [C03-35](appendix-g-3.md#g-c03-microsoft-github-35) |

#### サーバが機械的に決める

| 決め方 | 製品 | カード |
|---|---|---|
| HTTP のメソッドから | Azure App Service の組み込み MCP（GET は読み取り専用）、Notion の MCP サーバ（GET 以外は全部破壊的）、Neon | [C03-40](appendix-g-3.md#g-c03-microsoft-github-40) [C09-16](appendix-g-10.md#g-c09-servers-gateways-security-16) [G3VS-19](appendix-g-9.md#g-g3-vendor-servers-19) |
| 内部の操作の種類から | MongoDB、MCP Toolbox、Playwright（読み取り以外は全部破壊的、`openWorldHint` は常に true）、Kibana | [C09-12](appendix-g-10.md#g-c09-servers-gateways-security-12) [C06-31](appendix-g-6.md#g-c06-google-aws-31) [C03-21](appendix-g-3.md#g-c03-microsoft-github-21) [C09-20](appendix-g-10.md#g-c09-servers-gateways-security-20) |
| 名前の接頭辞から | Pomerium、MobileBuildMCP（上流の Xcode のツールに注釈が無いとき） | [C09-18](appendix-g-10.md#g-c09-servers-gateways-security-18) [G3VS-14](appendix-g-9.md#g-g3-vendor-servers-14) |
| 定型（プリセット）から選ぶ | Azure DevOps、AWS Transform、DigitalOcean、dbt-mcp（補助の関数の既定値が仕様の既定値） | [C03-29](appendix-g-3.md#g-c03-microsoft-github-29) [C06-57](appendix-g-6.md#g-c06-google-aws-57) [G3VS-47](appendix-g-9.md#g-g3-vendor-servers-47) [G3VS-39](appendix-g-9.md#g-g3-vendor-servers-39) |
| 全ツール同じ値 | LangGraph の /mcp（全部 `destructiveHint: false`）、SonarQube（`destructiveHint` 以下は固定） | [G3VS-31](appendix-g-9.md#g-g3-vendor-servers-31) [G3VS-22](appendix-g-9.md#g-g3-vendor-servers-22) |
| 設定で切り替える | AWS API MCP Server（環境変数で `readOnlyHint` が変わる）、Supabase の execute_sql、BigQuery の書き込みモード | [C06-54](appendix-g-6.md#g-c06-google-aws-54) [C09-06](appendix-g-10.md#g-c09-servers-gateways-security-06) [C06-38](appendix-g-6.md#g-c06-google-aws-38) |

さらに、**クライアントの動きに合わせて値を決める**例もあります。PostHog は書き込みもできるツールに、クライアントの承認を避けるために `destructiveHint: false` を付けたとコードに書いています（[G3VS-29](appendix-g-9.md#g-g3-vendor-servers-29)）。MobileBuildMCP は、注釈の変更の動機を「確認のプロンプトを減らすこと」と CHANGELOG に書き、シミュレータの中の操作を読み取り専用とする独自の規則を決めています（[G3VS-15](appendix-g-9.md#g-g3-vendor-servers-15)・[G3VS-16](appendix-g-9.md#g-g3-vendor-servers-16)・[G3VS-11](appendix-g-9.md#g-g3-vendor-servers-11)）。

#### 「宣言している」の数え方への影響

ワイヤーの上で注釈を集めて「宣言しているツールの割合」を数えると、SDK が埋めた値やゲートウェイが書いた値も「宣言」に数えてしまいます（[C02-21](appendix-g-2.md#g-c02-sdks-21)・[C02-30](appendix-g-2.md#g-c02-sdks-30)・[C10-03](appendix-g-12.md#g-c10-research-standards-03)）。
逆に、作者が書いた false が途中で落ちて「未宣言」に見えることもあります（[C09-35](appendix-g-10.md#g-c09-servers-gateways-security-35)・[G2RM-05](appendix-g-10.md#g-g2-registries-marketplaces-05)）。

**本書の読み**: AuthGap は、ワイヤーの値ではなく Python のソースコードを読み、作者がどの値を書いたかを見ます。だから、SDK が送る既定値（たとえば Go の SDK の false）には惑わされません。Python の公式 SDK は書かれていないヒントを送らないので（[C02-03](appendix-g-2.md#g-c02-sdks-03)）、ソースに書いた値とワイヤーの値の差は小さいはずです。ただし、Python のサーバでも、補助の関数の既定値（dbt-mcp。[G3VS-39](appendix-g-9.md#g-g3-vendor-servers-39)）、変換で自動で付く値（FastMCP の ResourcesAsTools。[C02-13](appendix-g-2.md#g-c02-sdks-13)）、公開のときに付ける既定の値（Agno。[C08-11](appendix-g-8.md#g-c08-frameworks-11)）のように、作者が 1 つずつ書いたわけではない値がソースの中にあります。AuthGap がこれらを「明示した宣言」と数えるかは、この付録では確かめていません（不明）。また、ゲートウェイの運用者が書き換えた値は、AuthGap の測る対象（サーバのソース）の外です。

#### この小節のまとめ

受け取った注釈は「作者の約束」とは限りません。SDK・ゲートウェイ・登録所・機械的な付け方が間に入ります。ワイヤーで数えた割合を、作者の宣言の割合として読まないでください。

---

### 3.5 宣言を書くことを求めるところ

#### 一言で言うと

ディレクトリ（掲載の窓口）の中には、宣言を書くことを掲載の条件にしているところがあります。
しかし、**書いた値が実装と合っているかを機械で確かめる**と書いているところは、カードの中には見つかりませんでした（ほとんどは「不明」）。

#### 掲載の窓口

| 窓口 | 求めること | 値を実装と照らし合わせるか | カード |
|---|---|---|---|
| Anthropic の Connectors Directory | 全ツールに title と `readOnlyHint` / `destructiveHint`。ただし範囲の書き方がページで揃っていない（「both」「どちらか」「当てはまるもの」） | ポータルは欠落に印を付ける。値の正しさの自動の照合は書かれていない（不明）。読み書きを 1 つのツールで切り替える万能のツールは却下 | [C04-01](appendix-g-4.md#g-c04-anthropic-01) [C04-02](appendix-g-4.md#g-c04-anthropic-02) [C04-03](appendix-g-4.md#g-c04-anthropic-03) [C04-05](appendix-g-4.md#g-c04-anthropic-05) [C04-06](appendix-g-4.md#g-c04-anthropic-06) [C04-07](appendix-g-4.md#g-c04-anthropic-07) |
| 同（Claude Desktop の申請フォームの実装） | 注釈の欠落を警告。申請者が選んだ「読み取り専用」などの区分と注釈が食い違えば警告 | 申告どうしの照合で、実装との照合ではない。機能テストは `readOnlyHint: true` のツールだけを実際に呼び、「注釈は自己申告で Anthropic は確かめていない」と画面に書く | [G3CAMA-36](appendix-g-8.md#g-g3-consumer-apps-model-apis-36) [G3CAMA-39](appendix-g-8.md#g-g3-consumer-apps-model-apis-39) [G3CAMA-37](appendix-g-8.md#g-g3-consumer-apps-model-apis-37) [G3CAMA-38](appendix-g-8.md#g-g3-consumer-apps-model-apis-38) |
| OpenAI の ChatGPT Directory（Apps の提出） | 3 つのヒントを明示の true / false で。欠けると提出が止まる | 「宣言が振る舞いと合わない」は、よくある却下の理由に挙がる。どう見つけるかは「自動のスキャンか人の審査を行うことがある」以上は書かれていない（不明）。値ごとの根拠の説明が要るかは文書の間で食い違う | [C05-05](appendix-g-5.md#g-c05-openai-05) [C05-09](appendix-g-5.md#g-c05-openai-09) [C05-10](appendix-g-5.md#g-c05-openai-10) [C05-11](appendix-g-5.md#g-c05-openai-11) [C05-12](appendix-g-5.md#g-c05-openai-12) [C05-13](appendix-g-5.md#g-c05-openai-13) |
| Slack Marketplace | 全ツールに `readOnlyHint` | 値を審査で確かめるとは書いていない（不明） | [G3SH-01](appendix-g-9.md#g-g3-saas-hosts-01) |
| Microsoft 365 Copilot の federated connector | 全ツールに title と `readOnlyHint` が付いていることの申告 | 申告を検査するか、値の正しさまで見るかは書かれていない（不明） | [C03-32](appendix-g-3.md#g-c03-microsoft-github-32) [C03-33](appendix-g-3.md#g-c03-microsoft-github-33) |
| HubSpot Marketplace | MCP の注釈ではなく、独自の `accessType`（readOnly / write）を別の場所に書かせる。迷えば write | 品質のチームが審査すると書く。MCP の注釈との対応は不明 | [G3SH-19](appendix-g-9.md#g-g3-saas-hosts-19) |
| 公式 MCP レジストリ・GitHub MCP Registry・Cline Marketplace など | 掲載の要件に注釈は無い | — | [付録 G-13](appendix-g-13.md)・[C01-59](appendix-g-1.md#g-c01-mcp-official-59) |

ある第三者のガイドは「`readOnlyHint` があると掲載が通りやすい」と書いていますが、どの窓口の規則かは示されず、裏づけはありません（[G2RM-15](appendix-g-10.md#g-g2-registries-marketplaces-15)）。

#### 自分のサーバで宣言を強制する作者

| サーバ | 強制のしかた | 値の正しさ | カード |
|---|---|---|---|
| github-mcp-server | 全ツールの登録で `ReadOnlyHint` の明示を、ソースの構文の検査（テスト）で強制。理由は「未設定の false が、読むだけの操作に余計な承認を出させるから」 | 書いてあるかだけを見る | [C03-14](appendix-g-3.md#g-c03-microsoft-github-14) |
| Sentry の MCP サーバ | 3 つのヒントの明示を型とテストで強制。理由は「絞り込みや確認の門がヒントに頼るから」 | 有無と「read-only かつ destructive」の矛盾だけ | [C09-01](appendix-g-10.md#g-c09-servers-gateways-security-01) [C09-02](appendix-g-10.md#g-c09-servers-gateways-security-02) |
| Grafana の MCP サーバ | 3 つのヒントの明示をテストで強制 | 有無と矛盾だけ。Go の型のため `readOnlyHint` の明示そのものは検査できないとコメントで認める | [C09-11](appendix-g-10.md#g-c09-servers-gateways-security-11) |
| Azure DevOps の MCP サーバ | 注釈の表に無いツールの登録で、起動時に例外 | 表引きの有無だけ | [C03-29](appendix-g-3.md#g-c03-microsoft-github-29) |
| kubernetes-mcp-server | 作者への規則として全ツールに注釈を求める | 規則の文書 | [G3VS-08](appendix-g-9.md#g-g3-vendor-servers-08) |
| Elastic（Kibana） | MCP 経由で確認の画面が飛ばされた不具合を受けて、破壊的なツールに `destructiveHint: true` を求めるレビューの基準にした | レビュー | [C09-19](appendix-g-10.md#g-c09-servers-gateways-security-19) |

#### この小節のまとめ

宣言を「書くこと」を求める窓口と作者はありますが、カードで確かめた範囲では、値を実装と照らし合わせると書いた窓口はありません。OpenAI は不一致を却下の理由に挙げますが、見つけ方は不明です。

---

### 3.6 宣言と実装を照らし合わせるもの

#### 一言で言うと

宣言と実装を照らし合わせる道具や取り組みは、いくつかあります。
しかし、**多くは名前・説明文・スキーマと比べる**もので、ソースコードの効果と比べるものは少数です。
ソースコードと比べるものも、対象の宣言や言語が限られています。

#### 何と何を比べるか

| 道具・取り組み | 比べるもの | 扱う宣言 | 限界・注意 | カード |
|---|---|---|---|---|
| HintLint（Complira） | 宣言とソースコード（TypeScript・JavaScript・Python。10 種類の sink＝効果の行き先を探す） | 偽の read-only（D1 に当たる）、`openWorldHint=false` なのに外へ届く（D3 に当たる）、破壊の証拠があるのに `destructiveHint=true` が無い | 所見は「自動の強制ではなくレビューの証拠」として扱えと自分で書く。README の数字（1,160 ツール、精度 82% など）は開発元の報告で、本記録者は検証していない。呼び出し先へどこまで降りるかはカードに無い（不明） | [C09-36](appendix-g-10.md#g-c09-servers-gateways-security-36) [C09-37](appendix-g-10.md#g-c09-servers-gateways-security-37) [C09-38](appendix-g-10.md#g-c09-servers-gateways-security-38) [C09-39](appendix-g-10.md#g-c09-servers-gateways-security-39) |
| mcp-doctor（PyPI mcp-server-lint 0.12.13） | 宣言と Python のソース（関数の定義全体を文字列に戻し、4 種類の正規表現を当てる） | D1 だけ | FastMCP のデコレータの形だけ。呼び出し先へ降りない。作者自身が「人が見る価値がある、であって確定のバグではない」と書く。実行時版は照合できないと明言 | [G2VL-10](appendix-g-10.md#g-g2-verifiers-linters-10) [G2VL-11](appendix-g-10.md#g-g2-verifiers-linters-11) [G2VL-12](appendix-g-10.md#g-g2-verifiers-linters-12) |
| OpenAI の申請用 skill | 宣言と実装（呼び出し先まで）を、開発者の手元の Codex（LLM）に読ませる | 3 つのヒント | 規則化された解析ではなく LLM の読み。OpenAI 自身の審査の方法とは書かれていない | [C05-46](appendix-g-5.md#g-c05-openai-46) [C05-47](appendix-g-5.md#g-c05-openai-47) [C05-48](appendix-g-5.md#g-c05-openai-48) |
| Stacklok（レジストリ） | 掲載の審査でソースを読んで注釈の正しさを確かめる | 宣言全般 | 本文は構想の書き方、FAQ は「検証済み」と現在形。方法と範囲は書かれず、第三者として確かめていない | [C10-18](appendix-g-12.md#g-c10-research-standards-18) |
| Airlock | ツールを実際に呼んで観察し、宣言と比べる | D1 だけ | 観察できるのは同梱のフィクスチャ（試験用のサーバ）だけ。普通の第三者のサーバでは「未検査」になる | [G2VL-25](appendix-g-10.md#g-g2-verifiers-linters-25) [G2VL-26](appendix-g-10.md#g-g2-verifiers-linters-26) [G2VL-27](appendix-g-10.md#g-g2-verifiers-linters-27) |
| actlint | 宣言と、名前・説明文・入力スキーマからの推定（ソースは読まない） | D1・D2（取り返しがつかないと裏づけられたときだけ）・D3。D4 は比べない | 31 サーバ・541 ツールの監査や精度の数字は開発元の報告で、本記録者は検証していない | [G2VL-01](appendix-g-10.md#g-g2-verifiers-linters-01) [G2VL-02](appendix-g-10.md#g-g2-verifiers-linters-02) [G2VL-03](appendix-g-10.md#g-g2-verifiers-linters-03) [G2VL-08](appendix-g-10.md#g-g2-verifiers-linters-08) [G2VL-09](appendix-g-10.md#g-g2-verifiers-linters-09) |
| MCP Tool Card Linter・mcpcheck・mcp-glimpse・MCP-audit など | 名前・説明文と宣言 | 主に D1 | コードを読まない | [G2VL-13](appendix-g-10.md#g-g2-verifiers-linters-13) [G2VL-14](appendix-g-10.md#g-g2-verifiers-linters-14) [C09-40](appendix-g-10.md#g-c09-servers-gateways-security-40) [C10-22](appendix-g-12.md#g-c10-research-standards-22) [G2VL-21](appendix-g-10.md#g-g2-verifiers-linters-21) |
| mcpconform・mcplint・mcp-surface-lint・mcp-toolgauge など | 宣言が「有るか」だけ | — | `destructiveHint: false` と書けば指摘が消えるものがある（D2 のうそが、かえって指摘を消す） | [G2VL-15](appendix-g-10.md#g-g2-verifiers-linters-15) [G2VL-16](appendix-g-10.md#g-g2-verifiers-linters-16) [G2VL-18](appendix-g-10.md#g-g2-verifiers-linters-18) [G2VL-19](appendix-g-10.md#g-g2-verifiers-linters-19) [G2VL-22](appendix-g-10.md#g-g2-verifiers-linters-22) |
| Glama（ディレクトリ） | 説明文と注釈の矛盾を LLM に判定させて採点 | 宣言全般 | 「定義を採点し、振る舞いは採点しない」と自分で書く | [C09-42](appendix-g-10.md#g-c09-servers-gateways-security-42) [C09-43](appendix-g-10.md#g-c09-servers-gateways-security-43) |
| Arcade・MCPProxy | 宣言の中の矛盾（例: 作成する操作なのに read_only）、エージェントの選んだ呼び方と宣言の不一致 | 宣言全般 | コードとは比べない | [G2GP-34](appendix-g-10.md#g-g2-gateways-platforms-34) [G2GP-35](appendix-g-10.md#g-g2-gateways-platforms-35) [G2GP-38](appendix-g-10.md#g-g2-gateways-platforms-38) |
| Neo4j の MCP サーバ・Supabase・PostHog | 自分のサーバの中で、自分の宣言を守る（Neo4j は実行前に問い合わせの種類を調べて書き込みを拒否、Supabase は read-only の DB ユーザーで実行、PostHog は読み取り専用のツールから呼べる先を絞る） | D1 | 自分のサーバだけ。Neo4j の検査にはすり抜ける種類がある | [C09-14](appendix-g-10.md#g-c09-servers-gateways-security-14) [C09-15](appendix-g-10.md#g-c09-servers-gateways-security-15) [C09-04](appendix-g-10.md#g-c09-servers-gateways-security-04) [C09-06](appendix-g-10.md#g-c09-servers-gateways-security-06) [G3VS-30](appendix-g-9.md#g-g3-vendor-servers-30) |
| mcp-annotation-enforcement | 照らし合わせず、宣言どおりに OS の sandbox で実行を縛る | D1・D3 | macOS の試作。同じ作者がソースの語のパターンで調べる静的な検査を試し、書くと宣言したツールで書き込みを 1 件も見つけられず捨てた、と報告 | [C10-20](appendix-g-12.md#g-c10-research-standards-20) [C10-21](appendix-g-12.md#g-c10-research-standards-21) |
| mcp-fuzz・mcp-reality-check | （照らし合わせではない）`readOnlyHint: true` を信じて、呼んでよいツールを選ぶ | D1 | D1 がうそなら、書き込みのツールを実データで呼ぶ | [G2VL-23](appendix-g-10.md#g-g2-verifiers-linters-23) [G2VL-24](appendix-g-10.md#g-g2-verifiers-linters-24) |

論文では、ある測定の論文が「宣言と実装の振る舞いの差は宣言の調査では測れず、実装の水準の解析が要る」と書き、自分ではその解析をしていません（[C10-04](appendix-g-12.md#g-c10-research-standards-04)）。
説明文とコードの食い違いを調べる論文（MCPDiFF・DCIChecker）は、本文に `readOnlyHint` などの語が無く、ToolAnnotations を扱っていません（[付録 G-13](appendix-g-13.md) の論文の行）。Cisco の mcp-scanner のコード整合性の分析の指示文にも、注釈の語はありませんでした（同じく G-13）。

#### AuthGap の新しさについて（本書の読み）

**本書の読み**: カードから言えることは次のとおりです。

- 「宣言をソースコードと照らし合わせる」という考え自体は、AuthGap だけのものではありません。HintLint（[C09-36](appendix-g-10.md#g-c09-servers-gateways-security-36)）と mcp-doctor（[G2VL-10](appendix-g-10.md#g-g2-verifiers-linters-10)）は、宣言をソースと比べます。論文で「初めて」と書くことはできません。
- カードで確かめた範囲では、mcp-doctor は D1 だけ・正規表現・呼び出し先へ降りない、という作りです（[G2VL-11](appendix-g-10.md#g-g2-verifiers-linters-11)）。HintLint は D1・D3 と `destructiveHint` の欠落を扱いますが、解析の深さはカードに無く不明です（[C09-37](appendix-g-10.md#g-c09-servers-gateways-security-37)・[C09-38](appendix-g-10.md#g-c09-servers-gateways-security-38)）。D4（`idempotentHint: true`）をコードと照らし合わせる道具は、カードの中には見つかりませんでした。ただし「見つからなかった」は「無い」ではありません。
- 違いを主張するなら、カードで確かめた範囲（HintLint は README と所見の一覧、mcp-doctor はコード）と並べて、扱う宣言・解析の方法・決められないものの扱いを具体的に比べる必要があります。HintLint の精度の数字は開発元の報告で、AuthGap の数字と並べて比べることはできません（[C09-36](appendix-g-10.md#g-c09-servers-gateways-security-36)）。

#### この小節のまとめ

照らし合わせの多くは名前・説明文・スキーマとの比較で、ソースとの比較は少数で範囲が限られます。AuthGap は先行の道具（HintLint・mcp-doctor）と並べて位置づけます（本書の読み）。

---

### 3.7 WebMCP — ブラウザのページが出すツールの宣言

#### 一言で言うと

WebMCP は、ブラウザの中のページが、AI にツールを渡す仕組みの草案です（W3C の Community Group の草案）。
注釈の語彙が MCP と違い、既定値は 4 つとも false です。

#### 語彙と既定値

| WebMCP の注釈 | 意味 | MCP との関係 | カード |
|---|---|---|---|
| `readOnlyHint`（既定 false） | 状態を変えず読むだけ | MCP と同じ名前 | [G2W-01](appendix-g-11.md#g-g2-webmcp-01) [G2W-02](appendix-g-11.md#g-g2-webmcp-02) |
| `untrustedContentHint`（既定 false） | 返す内容が信頼できない（利用者の投稿など） | MCP に無い。出力の側の印 | [G2W-03](appendix-g-11.md#g-g2-webmcp-03) [G2W-06](appendix-g-11.md#g-g2-webmcp-06) |
| `consequentialHint`（既定 false） | 重大・現実世界・取り消せない行為（航空券の予約、送金など） | MCP の `destructiveHint` に近いが、既定は false | [G2W-04](appendix-g-11.md#g-g2-webmcp-04) [G2W-07](appendix-g-11.md#g-g2-webmcp-07) |
| `debugging`（既定 false） | 開発者向けのツール | MCP に無い | [G2W-05](appendix-g-11.md#g-g2-webmcp-05) [G2W-17](appendix-g-11.md#g-g2-webmcp-17) |

MCP の `destructiveHint`・`idempotentHint`・`openWorldHint` はありません（[G2W-01](appendix-g-11.md#g-g2-webmcp-01)）。
既定値が false なので、何も書かないツールは「読み取り専用ではない」かつ「重大でもない」になります。確認を出すかどうかを、草案は決めていません（[G2W-09](appendix-g-11.md#g-g2-webmcp-09)）。

#### 使い方の記述

- 草案の書き方は規範ではなく（MUST・SHOULD が無い）、`consequentialHint` があれば確認を必須に「できる」、`untrustedContentHint` があれば出力を消毒・区切りなどで隔離「できる」と書くだけです（[G2W-06](appendix-g-11.md#g-g2-webmcp-06)・[G2W-07](appendix-g-11.md#g-g2-webmcp-07)・[G2W-09](appendix-g-11.md#g-g2-webmcp-09)）。
- 草案自身が「宣言した意図が実際の振る舞いと一致する保証は無い」と書いています（[G2W-08](appendix-g-11.md#g-g2-webmcp-08)）。自己評価の票は「`readOnlyHint` によってエージェントが確認を省くことがある」と認めています（[G2W-10](appendix-g-11.md#g-g2-webmcp-10)）。
- Chrome の文書は、エージェントの作者に「`readOnlyHint` か説明文がはっきり示さない限り、状態を変えると仮定せよ」と求めます（[G2W-19](appendix-g-11.md#g-g2-webmcp-19)）。
- Chrome が例として示す拡張は、注釈を常に信頼します。`readOnlyHint: true` なら確認なし、それ以外は確認（設定で切れる）、`consequentialHint: true` は常に確認です（[G2W-21](appendix-g-11.md#g-g2-webmcp-21)・[G2W-22](appendix-g-11.md#g-g2-webmcp-22)・[G2W-23](appendix-g-11.md#g-g2-webmcp-23)・[G2W-26](appendix-g-11.md#g-g2-webmcp-26)）。同じ README が「ページは有害なツールを読み取り専用と書くこともできる」と限界を書いています（[G2W-25](appendix-g-11.md#g-g2-webmcp-25)）。
- Chromium の実装は、4 つの値を検証せずに写し（[G2W-27](appendix-g-11.md#g-g2-webmcp-27)）、モデルへ送るページの内容の形式には `readOnly` しかありません（[G2W-28](appendix-g-11.md#g-g2-webmcp-28)・[G2W-29](appendix-g-11.md#g-g2-webmcp-29)）。
- OpenAI の内蔵ブラウザは「読み取り専用という主張は証拠にならない」と書き、呼び出しごとに安全のレビューをします（[C05-51](appendix-g-5.md#g-c05-openai-51)・[C05-52](appendix-g-5.md#g-c05-openai-52)）。

#### MCP への橋渡し

WebMCP のツールを MCP のツールとして中継する道具では、ページの自己申告がそのまま MCP の `readOnlyHint` になることがあります。

| 橋渡し | 写し方 | カード |
|---|---|---|
| Playwright MCP | `readOnlyHint` = ページの readOnly、`destructiveHint` = その否定、`openWorldHint` = 常に true。重大・信頼できない内容の印は説明文の前置きとしてだけ伝える | [C03-22](appendix-g-3.md#g-c03-microsoft-github-22) [G2W-35](appendix-g-11.md#g-g2-webmcp-35) |
| MCP-B | `untrustedContentHint` だけ落とし、`readOnlyHint` はそのまま渡す | [G2W-36](appendix-g-11.md#g-g2-webmcp-36) [G2W-37](appendix-g-11.md#g-g2-webmcp-37) |
| Cloudflare Agents SDK（実験的） | 逆向き（MCP → WebMCP）で、`readOnlyHint` だけを渡す | [C08-15](appendix-g-8.md#g-c08-frameworks-15) |
| chrome-devtools-mcp | 汎用の実行ツール 1 つにまとめ、その `readOnlyHint` を false に固定。ページの注釈は文字としてモデルに見せるだけ | [G2W-33](appendix-g-11.md#g-g2-webmcp-33) [G2W-34](appendix-g-11.md#g-g2-webmcp-34) |

**本書の読み**: Playwright や MCP-B のような橋渡しを、`readOnlyHint` で確認を省くクライアントにつなぐと、ブラウザのページの自己申告だけで確認が省かれる経路になりえます。Playwright のカードの補足も同じ考察を書いています（[C03-22](appendix-g-3.md#g-c03-microsoft-github-22)）。ただし実害は確かめていません。WebMCP は AuthGap の測定の対象（Python の MCP サーバ）の外です。

#### この小節のまとめ

WebMCP は語彙も既定値も MCP と違い、使い方を規範で決めていません。橋渡しを通ると、ページの自己申告が MCP の宣言として届くことがあります。

---

### 3.8 研究・標準・公的な指針

#### 一言で言うと

注釈を正面から扱う論文は少なく、数字はどれも論文の記載で、本記録者は検証していません。
標準や公的な指針の多くは、注釈に触れていません。

#### 論文の数字（論文の記載。本記録者は検証していない）

| 論文 | 記載 | 分母 | カード |
|---|---|---|---|
| arXiv:2609.10962 | 無作為に選んだサーバのツールのうち 58.8% が注釈を出していない。サーバごとに「全部付けるか、全く付けないか」に分かれる | 公式レジストリのうち npm・stdio・active の 7,258 件から無作為に 400 件を選び、ツールを 1 つ以上出した 194 サーバの 2,766 ツール | [C10-01](appendix-g-12.md#g-c10-research-standards-01) |
| arXiv:2609.15397 | ワイヤーの上で 74.0% のツールが少なくとも 1 つの項目を出し、61.7% が 4 つとも出す。ただし多くは SDK の既定値や雛形から来ているかもしれない | リモートの窓口を持つ対象に問い合わせ、ツールを返した 4,838 サーバの 98,291 ツール | [C10-03](appendix-g-12.md#g-c10-research-standards-03) |
| arXiv:2607.07461 | 1,856 ツールのうち 325 が注釈を使う（17.5% はカードの記録者の計算） | スター数の順に手で選んだ GitHub の 100 プロジェクト（無作為ではない） | [C10-12](appendix-g-12.md#g-c10-research-standards-12) |
| arXiv:2606.06387 | WebMCP で `readOnlyHint=true` を足すだけで、悪性のツールが選ばれる率が平均約 87%。ただし名前の効果と分けられておらず、別の条件では平均 6% | 3 つのモデルでの実験条件 | [C10-08](appendix-g-12.md#g-c10-research-standards-08) |

ほかに、注釈は任意で信頼できないので実行時のポリシーには使えないとして、必須のタグを提案する論文（[C10-09](appendix-g-12.md#g-c10-research-standards-09)）、粗く信頼できないかもしれないが安全な包み（ラッパー）を作る人の手がかりにはなる、とする Microsoft Research の論文（[C10-10](appendix-g-12.md#g-c10-research-standards-10)）、注釈を悪意あるサーバが自由に書けるメタデータに含める論文（[C10-11](appendix-g-12.md#g-c10-research-standards-11)）、自分で作った信頼できる部品だから注釈を正解のラベルに使う論文（[C10-13](appendix-g-12.md#g-c10-research-standards-13)）があります。
教科書型のサーベイは「`readOnlyHint: true` ならホストは確認なしで自動承認してよい」と、信頼の但し書きなしに教えています（[C10-05](appendix-g-12.md#g-c10-research-standards-05)・[C10-06](appendix-g-12.md#g-c10-research-standards-06)）。同じ本の承認の門の設計の Q&A は [未確認] です（[C10-07](appendix-g-12.md#g-c10-research-standards-07)）。

#### 標準・安全の指針

- **OWASP MCP Top 10 の推奨管理策（Client-Side Tool Risk Gating）**: ホストが全ツールを危険度で格付けし、外部のツールの格付けに注釈を使います。上限を超えるツールはモデルから隠します。`destructiveHint` があって `idempotentHint` が無いツールは最高の危険度に固定し、注釈が欠けていれば点数を上げます（[C10-14](appendix-g-12.md#g-c10-research-standards-14)・[C10-15](appendix-g-12.md#g-c10-research-standards-15)）。参照実装では `readOnlyHint: true` や `idempotentHint: true` を宣言すると点数が下がるので、偽の宣言で上限の下に入りうる、とカードの記録者が読んでいます（[C10-14](appendix-g-12.md#g-c10-research-standards-14)）。また、改ざんの検知の指紋に注釈が入らないことを、限界として書いています（[C10-16](appendix-g-12.md#g-c10-research-standards-16)）。
- **CoSAI の MCP の白書**: 仕様の「注釈は信頼できない」を引いて、ツールの汚染の文脈に置くだけです（[C10-17](appendix-g-12.md#g-c10-research-standards-17)）。
- **隣接する仕組み**: ACP（エディタとエージェントの間の取り決め）の ToolKind は「表示のための粗い分類」と定義され、MCP の注釈との対応は決められていません（[G3SP-06](appendix-g-12.md#g-g3-standards-protocols-06)・[G3SP-08](appendix-g-12.md#g-g3-standards-protocols-08)）。A2A には読み取り専用・破壊的を宣言する欄がありません（[G3SP-09](appendix-g-12.md#g-g3-standards-protocols-09)）。OASF の scopes は 4 つのヒントに似た列挙を持ちます（[G3SP-10](appendix-g-12.md#g-g3-standards-protocols-10)）。MCP の Server Card の提案は、静的なカードにツールの一覧を載せず、カードの中身を安全の判断に使わせない、としています（[G3SP-01](appendix-g-12.md#g-g3-standards-protocols-01)・[G3SP-02](appendix-g-12.md#g-g3-standards-protocols-02)）。
- **先例**: RFC 9110（HTTP）は safe・idempotent をメソッドの性質として決め、「safe なメソッドでも、実装が副作用を持つことは妨げない」と、宣言と実際の分離を明記しています（[G3SP-18](appendix-g-12.md#g-g3-standards-protocols-18)・[G3SP-19](appendix-g-12.md#g-g3-standards-protocols-19)）。OpenAI の GPT Actions の `x-openai-isConsequential` は、欄が無ければ GET を「重大でない」、それ以外を「重大」とする既定を持ちます（[G3SP-20](appendix-g-12.md#g-g3-standards-protocols-20)）。IETF の個人の草案には、独自の語彙で同じこと（取り消せない変更の確認、冪等でなければ再試行しない）をするものがあります（[G3SP-11](appendix-g-12.md#g-g3-standards-protocols-11)・[G3SP-13](appendix-g-12.md#g-g3-standards-protocols-13)）。
- **公的な指針**: OWASP の Cheat Sheet、NIST CAISI の文書、Five Eyes の共同の指針、NCSC-UK、シンガポールの IMDA などのページには、調べた語（annotation・readOnlyHint など）が見つかりませんでした。行は [付録 G-13](appendix-g-13.md) の「記載が無かったページ」にあります。NSA の文書などは配信元に拒否されて読めず、何も言えません（不明。G-13 の「届かなかったページ」）。

#### この小節のまとめ

論文の数字は論文の記載で、分母がそれぞれ違い、本記録者は検証していません。標準の側で注釈を門に使うと書くのは、カードの中では OWASP の推奨管理策だけでした。

---

### 3.9 AuthGap にとっての意味（本書の読み）

この小節は全体が**本書の読み**です。カードの事実をつないで、「宣言が間違っていたら、何が起きうるか」の経路を並べます。どの経路も、カードの条件（モード・設定・版）のときだけ成り立ちます。実害を確かめたものではありません。

#### D1（`readOnlyHint: true`）がうそのとき — 確認なしで書き込みが走る経路

| 経路 | 条件 | カード |
|---|---|---|
| VS Code が実行前の確認を出さない | sandbox でないサーバ、設定で除外していないツール | [C03-06](appendix-g-3.md#g-c03-microsoft-github-06) |
| Microsoft 365 Copilot が初回の後は確認しない | 宣言型エージェントの MCP プラグイン | [C03-30](appendix-g-3.md#g-c03-microsoft-github-30) |
| Copilot CLI が確認なしで承認 | 1.0.63 の実装、deny の規則に当たらない | [G2CCM-09](appendix-g-7.md#g-g2-closed-clients-missing-09) |
| Codex が承認なしで実行 | auto モード（既定）・writes モード | [C05-34](appendix-g-5.md#g-c05-openai-34) [C05-35](appendix-g-5.md#g-c05-openai-35) |
| Gemini Enterprise が確認を飛ばす | カスタム MCP の actions | [C06-20](appendix-g-6.md#g-c06-google-aws-20) |
| Cowork が承認なしで通す | auto モード。承認の設定 "readOnly" のサーバでも | [G3CAMA-18](appendix-g-8.md#g-g3-consumer-apps-model-apis-18) [G3CAMA-33](appendix-g-8.md#g-g3-consumer-apps-model-apis-33) |
| Cowork の「タスクごとの承認」のしばりから外れる | 組織の設定が off。利用者が Always allow を選べば確認なしになりうる | [C04-08](appendix-g-4.md#g-c04-anthropic-08) |
| goose・n8n・AgentScope・LeapFlow・Docker Agent・TrueForge が確認なしで実行 | それぞれのモード・既定の設定 | [C07-02](appendix-g-7.md#g-c07-ide-agents-02) [C08-03](appendix-g-8.md#g-c08-frameworks-03) [G3AA-23](appendix-g-7.md#g-g3-asia-agents-23) [G2RM-17](appendix-g-10.md#g-g2-registries-marketplaces-17) [C07-07](appendix-g-7.md#g-c07-ide-agents-07) [G2GP-08](appendix-g-10.md#g-g2-gateways-platforms-08) |
| Cursor が確認なしで実行 | 管理者の reads モード（[確認（調査時のみ）]） | [G2CCM-35](appendix-g-7.md#g-g2-closed-clients-missing-35) |
| 読み取り専用の絞り込みをすり抜ける | Copilot code review、Gemini CLI の Plan Mode、AWS のプロキシの read-only モード、Google Cloud の IAM の deny ポリシー | [C03-16](appendix-g-3.md#g-c03-microsoft-github-16) [C06-04](appendix-g-6.md#g-c06-google-aws-04) [C06-48](appendix-g-6.md#g-c06-google-aws-48) [C06-14](appendix-g-6.md#g-c06-google-aws-14) |
| 書き込みが並列に走る | Claude Agent SDK、Codex、Qwen Code、Qoder | [C04-13](appendix-g-4.md#g-c04-anthropic-13) [C05-42](appendix-g-5.md#g-c05-openai-42) [C07-17](appendix-g-7.md#g-c07-ide-agents-17) [G3AA-01](appendix-g-7.md#g-g3-asia-agents-01) |
| 2 回目の呼び出しが実行されず、結果の写しが返る | Claude Desktop のアーティファクトからの呼び出し | [G3CAMA-23](appendix-g-8.md#g-g3-consumer-apps-model-apis-23) |
| 審査の機能テストで実際に呼ばれる | Claude Desktop の申請フォーム | [G3CAMA-37](appendix-g-8.md#g-g3-consumer-apps-model-apis-37) |
| 危険度の点数が下がって門を通る | OWASP の推奨管理策の参照実装 | [C10-14](appendix-g-12.md#g-c10-research-standards-14) |

この表が、第 4 章 4.5 節の結論（クライアントは `readOnlyHint: true` を見て呼び出しごとの確認を省くことがある）を、製品と条件つきで裏づけます。

#### D2（`destructiveHint: false`）がうそ、または `destructiveHint` が無いとき — 門をすり抜ける経路

AuthGap の D2 は、`destructiveHint: false` と**明示した**宣言だけです（[第 4 章](ch04.md) 4.4 節）。ただし `=== true` で比べる製品では、書いていないことも false と同じ結果になります（3.3 節）。

| 経路 | 条件 | カード |
|---|---|---|
| Codex が承認なしで実行 | auto モードで、`destructiveHint: false` かつ `openWorldHint: false`（D2 と D3 の両方） | [C05-34](appendix-g-5.md#g-c05-openai-34) |
| ToolHive の Safe tools が許可 | `destructiveHint == false` かつ `openWorldHint == false` | [C09-23](appendix-g-10.md#g-c09-servers-gateways-security-23) |
| Claude Desktop の watcher（人のいない実行）が拒否しない | `destructiveHint` が true でない | [G3CAMA-22](appendix-g-8.md#g-g3-consumer-apps-model-apis-22) |
| Claude Desktop のアーティファクトからの呼び出しで確認が挟まらない | 同上 | [G3CAMA-24](appendix-g-8.md#g-g3-consumer-apps-model-apis-24) |
| Claude Code の auto mode で、サーバのポリシーの ask の規則が確認を強制しない | 同上（[確認（調査時のみ）]） | [G2CCM-34](appendix-g-7.md#g-g2-closed-clients-missing-34) |
| 承認待ちにならない | TrueFoundry の destructive の範囲、TrueForge の既定 | [G2GP-03](appendix-g-10.md#g-g2-gateways-platforms-03) [G2GP-11](appendix-g-10.md#g-g2-gateways-platforms-11) |
| 破壊的なツールを無効にするモードで残る | kubernetes-mcp-server、Codex の apps の destructive_enabled | [G3VS-02](appendix-g-9.md#g-g3-vendor-servers-02) [C05-40](appendix-g-5.md#g-c05-openai-40) |
| 掲載の検査や名前の検査の指摘が消える | `destructiveHint: false` を書けば指摘しないリンター | [G2VL-16](appendix-g-10.md#g-g2-verifiers-linters-16) [G2VL-22](appendix-g-10.md#g-g2-verifiers-linters-22) |

#### D3（`openWorldHint`）と D4（`idempotentHint`）を使う製品

`readOnlyHint` に比べて、この 2 つを判断に使う製品はカードの中で少数でした（数は便宜的な集まりの中のことなので数えません）。

| 宣言 | 使う製品 | 何に使うか | カード |
|---|---|---|---|
| `openWorldHint` | VS Code | true なら結果の事後確認の対象 | [C03-04](appendix-g-3.md#g-c03-microsoft-github-04) [C03-07](appendix-g-3.md#g-c03-microsoft-github-07) |
| `openWorldHint` | Codex | auto モードの承認の条件（`destructiveHint: false` と組で）、apps の遮断 | [C05-34](appendix-g-5.md#g-c05-openai-34) [C05-40](appendix-g-5.md#g-c05-openai-40) |
| `openWorldHint` | ToolHive | Safe tools の条件 | [C09-23](appendix-g-10.md#g-c09-servers-gateways-security-23) |
| `openWorldHint` | Microsoft Agent Framework（FIDES） | true の出力を「信頼できない」とする。制限の方向だけ | [C03-38](appendix-g-3.md#g-c03-microsoft-github-38) |
| `openWorldHint` | CodeBuddy Code | LLM のレビューに「ネットワークに触れる」の札を付ける（レビューは既定で無効） | [G3AA-17](appendix-g-7.md#g-g3-asia-agents-17) |
| `openWorldHint` | Google の Agent Gateway | IAM の条件の属性 | [C06-21](appendix-g-6.md#g-c06-google-aws-21) |
| `idempotentHint` | Qwen Code | 接続が切れた呼び出しを自動で送り直してよいか | [C07-13](appendix-g-7.md#g-c07-ide-agents-13) [C07-15](appendix-g-7.md#g-c07-ide-agents-15) |
| `idempotentHint` | OWASP の推奨管理策 | 危険度の点数（true なら下がる。`destructiveHint` があって `idempotentHint` が無ければ最高の危険度） | [C10-14](appendix-g-12.md#g-c10-research-standards-14) [C10-15](appendix-g-12.md#g-c10-research-standards-15) |
| `idempotentHint` | Google の Agent Gateway | IAM の条件の属性 | [C06-21](appendix-g-6.md#g-c06-google-aws-21) |

逆に、使わないと明記した例もあります。Codex の承認の判定は `idempotentHint` を使いません（[C05-34](appendix-g-5.md#g-c05-openai-34)）。Claude Agent SDK は 3 つを「Informational only」とします（[C04-16](appendix-g-4.md#g-c04-anthropic-16)）。Pydantic AI は「冪等な削除も削除だ」として、先回りの実行に `idempotentHint` を数えません（[C02-58](appendix-g-2.md#g-c02-sdks-58)）。Qoder は `idempotentHint` を受け取るだけで使いません（[G3AA-05](appendix-g-7.md#g-g3-asia-agents-05)）。Microsoft 365 Copilot の MCP Apps は `readOnlyHint` 以外を扱いません（[C03-31](appendix-g-3.md#g-c03-microsoft-github-31)）。

**読み**: D1 の違反は、確認の省略・並列化・キャッシュなど、多くの経路で「起きうる」と言えます。D2 は、`destructiveHint` を門に使う製品で門をすり抜ける経路があります。D3 と D4 は、使う製品が少なく、使い方も製品ごとに違います（事後確認・再試行・点数）。論文で D3・D4 の違反の意味を書くときは、この表の製品と条件を名指しし、「多くのクライアントで確認が省かれる」とは書きません。

---

<a id="ag-4"></a>
## よくある誤解

- **誤解: 「宣言は守られている（誰かが検査している）」**
  検査されていません。仕様は「ヒント」とし（[C01-11](appendix-g-1.md#g-c01-mcp-official-11)）、Anthropic の申請画面も「注釈は自己申告で確かめていない」と書き（[G3CAMA-38](appendix-g-8.md#g-g3-consumer-apps-model-apis-38)）、Notion も「検証していない」と明言します（[G3SH-06](appendix-g-9.md#g-g3-saas-hosts-06)）。掲載の窓口も、値を実装と照らし合わせるとは書いていません（3.5 節）。
- **誤解: 「全クライアントが `readOnlyHint: true` で確認を省く」**
  省く製品はありますが、多くはモード・設定の条件つきです。読まない製品（Zed、Junie、Qoder など）も、制限の方向にだけ使う製品もあります（3.2 節）。
- **誤解: 「`destructiveHint` を書かなければ、仕様どおり『破壊的かもしれない』として慎重に扱われる」**
  `=== true` で比べる実装では、書いていないツールは「破壊的でない」側に入ります（[G3CAMA-17](appendix-g-8.md#g-g3-consumer-apps-model-apis-17)・[G2GP-11](appendix-g-10.md#g-g2-gateways-platforms-11)・[C02-51](appendix-g-2.md#g-c02-sdks-51)）。
- **誤解: 「SDK が送った false は、作者が書いた宣言だ」**
  Go の公式 SDK は、作者が書かなくても `readOnlyHint: false` を送ります（[C02-30](appendix-g-2.md#g-c02-sdks-30)）。Spring AI や mcp-go は 4 つとも既定値を送ります（[C02-21](appendix-g-2.md#g-c02-sdks-21)・[C02-33](appendix-g-2.md#g-c02-sdks-33)）。ゲートウェイが書き換えることもあります（3.4 節）。
- **誤解: 「G-13 に載っている（記載が無い）なら、その製品は宣言を使わない」**
  そのページに書かれていないだけです。たとえば Claude Code の公式の文書には記述がありませんが、配布物の実装は plan mode で `readOnlyHint` を使っています（[確認（調査時のみ）]。[G2CCM-03](appendix-g-7.md#g-g2-closed-clients-missing-03)）。
- **誤解: 「文書に書いてあれば、実装もそうなっている」**
  Copilot CLI（[C03-19](appendix-g-3.md#g-c03-microsoft-github-19) と [G2CCM-09](appendix-g-7.md#g-g2-closed-clients-missing-09)）や Codex（[C05-29](appendix-g-5.md#g-c05-openai-29) と [C05-34](appendix-g-5.md#g-c05-openai-34)）のように、文書とコードが逆のことがあります。
- **誤解: 「論文やブログの数字は、この付録で確かめた事実だ」**
  数字はどれも論文・ブログ・開発元の記載で、本記録者は検証していません（3.8 節、[C01-25](appendix-g-1.md#g-c01-mcp-official-25)・[C09-36](appendix-g-10.md#g-c09-servers-gateways-security-36)）。分母もそれぞれ違います。
- **誤解: 「宣言をソースと照らし合わせるのは AuthGap が初めて」**
  HintLint や mcp-doctor が先にあります（3.6 節）。違いを言うなら具体的に比べます。

---

<a id="ag-5"></a>
## この付録のまとめ

- 2026-10-02 の調査で、宣言の使われ方の資料 820 件をカードにした（[確認] 774 件・[確認（調査時のみ）] 19 件・[未確認] 27 件）。便宜的な集まりなので、件数を全体の割合にしない。
- MCP の公式は「ヒント・信頼できないサーバのものは信じるな・既定値は約束しない側」。一方で公式ブログは確認の省略を最もよくある使い方として示す。「信頼できるサーバ」の定義は無い。
- `readOnlyHint: true` で確認を省く製品は実在する（VS Code、Codex、Cowork の auto モードなど）。ただし多くはモード・設定・版の条件つきで、読まない製品も多い。
- 宣言が無いときの扱いは製品で逆を向く。`=== true` の比べ方で、書いていない `destructiveHint` が「壊さない」側に入る実装がある。
- 受け取る注釈は作者の宣言とは限らない。SDK の既定値、ゲートウェイの書き換え、機械的な付け方が間に入る。AuthGap はソースを読むのでワイヤーの既定値には惑わされない（本書の読み）。
- 宣言を書くことを求める窓口はあるが、値を実装と照らし合わせると書いたところはカードの中に無い。
- 宣言とソースを照らし合わせる先行の道具（HintLint・mcp-doctor）がある。AuthGap はそれらと並べて位置づける（本書の読み）。
- WebMCP は語彙も既定値も MCP と違い、橋渡しを通るとページの自己申告が MCP の宣言として届くことがある。
- D1 のうそは確認の省略・並列化などに、D2 のうそは破壊的な門のすり抜けにつながる経路がある。D3・D4 を使う製品は少数（本書の読み）。
- 論文で使うときは、カードの原文を自分で開き、版・日付・条件を添えて書く。

---

[← 付録 F 判定の言葉の対照表](appendix-f.md) ｜ [目次](README.md) ｜ [付録 G-1 →](appendix-g-1.md)
