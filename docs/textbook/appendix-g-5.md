[← 付録 G-4 Anthropic](appendix-g-4.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-6 Google と AWS →](appendix-g-6.md)

---

# 付録 G-5 OpenAI（ChatGPT・Codex・Apps SDK・Agents SDK）

<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->

<a id="ag-5-0"></a>
## この分冊の資料の一覧

| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |
|---|---|---|---|---|
| [C05-01](#g-c05-openai-01) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 表示（印・名前）・その他 | [確認] |
| [C05-02](#g-c05-openai-02) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 確認を求める・作者への書き方の案内 | [確認] |
| [C05-03](#g-c05-openai-03) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 確認を求める・作者への書き方の案内 | [確認] |
| [C05-14](#g-c05-openai-14) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C05-15](#g-c05-openai-15) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C05-16](#g-c05-openai-16) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | その他 | [確認] |
| [C05-17](#g-c05-openai-17) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） | 公式の文書 | 宣言を検査する | [確認] |
| [C05-04](#g-c05-openai-04) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Company knowledge | 公式の文書 | ツールを絞る・隠す・作者への書き方の案内 | [確認] |
| [C05-05](#g-c05-openai-05) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準 | 規約・審査の指針 | 宣言を書くことを求める・宣言を検査する | [確認] |
| [C05-06](#g-c05-openai-06) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準 | 規約・審査の指針 | 規則（ポリシー）の条件に使う・その他 | [確認] |
| [C05-07](#g-c05-openai-07) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準 | 規約・審査の指針 | 作者への書き方の案内 | [確認] |
| [C05-08](#g-c05-openai-08) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準 | 規約・審査の指針 | その他 | [確認] |
| [C05-09](#g-c05-openai-09) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータルの検証 | 公式の文書 | 宣言を書くことを求める・宣言を検査する | [確認] |
| [C05-10](#g-c05-openai-10) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータルの検証 | 公式の文書 | 宣言を書くことを求める | [確認] |
| [C05-11](#g-c05-openai-11) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータル（Scan Tools） | 公式の文書 | 宣言を検査する・そのまま渡す・見せる | [確認] |
| [C05-12](#g-c05-openai-12) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 審査（却下理由） | 公式の文書 | 宣言を検査する・作者への書き方の案内 | [確認] |
| [C05-13](#g-c05-openai-13) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 審査（却下理由） | 公式の文書 | 作者への書き方の案内・宣言を検査する | [確認] |
| [C05-18](#g-c05-openai-18) | OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Claude Code plugin からの移行 | 公式の文書 | 作者への書き方の案内・確認を求める | [確認] |
| [C05-19](#g-c05-openai-19) | OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続） | クライアントの文書 | 確認を求める・宣言が無いときの扱い | [確認] |
| [C05-20](#g-c05-openai-20) | OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続） | クライアントの文書 | 確認を求める | [確認] |
| [C05-21](#g-c05-openai-21) | OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続） | クライアントの文書 | その他 | [確認] |
| [C05-23](#g-c05-openai-23) | OpenAI — OpenAI API — Responses API の remote MCP ツール（type: mcp） | 公式の文書 | 確認を求める・使わない・読まない | [確認] |
| [C05-24](#g-c05-openai-24) | OpenAI — OpenAI API — Responses API の remote MCP ツール（type: mcp） | 公式の文書 | 確認を省く（自動で許可）・確認を求める・ツールを絞る・隠す | [確認] |
| [C05-25](#g-c05-openai-25) | OpenAI — openai-python SDK（Responses API の型） | SDK のソースコード | そのまま渡す・見せる・確認を省く（自動で許可） | [確認] |
| [C05-26](#g-c05-openai-26) | OpenAI — openai-python SDK（Responses API の型） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C05-27](#g-c05-openai-27) | OpenAI — OpenAI Agents SDK（TypeScript）— Hosted MCP server tools | SDK の文書 | 確認を省く（自動で許可）・確認を求める・そのまま渡す・見せる | [確認] |
| [C05-28](#g-c05-openai-28) | OpenAI — OpenAI Agents SDK（TypeScript） | SDK のソースコード | そのまま渡す・見せる | [確認] |
| [C05-29](#g-c05-openai-29) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントの文書 | 確認を求める・確認を省く（自動で許可） | [確認] |
| [C05-34](#g-c05-openai-34) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い | [確認] |
| [C05-35](#g-c05-openai-35) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 規則（ポリシー）の条件に使う・確認を省く（自動で許可）・確認を求める | [確認] |
| [C05-36](#g-c05-openai-36) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 宣言が無いときの扱い | [確認] |
| [C05-37](#g-c05-openai-37) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 使わない・読まない | [確認] |
| [C05-38](#g-c05-openai-38) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 確認を求める | [確認] |
| [C05-39](#g-c05-openai-39) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 宣言が無いときの扱い・確認を求める | [確認] |
| [C05-42](#g-c05-openai-42) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | その他 | [確認] |
| [C05-43](#g-c05-openai-43) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） | クライアントのソースコード | 宣言が無いときの扱い・その他 | [確認] |
| [C05-30](#g-c05-openai-30) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — App Server プロトコル | クライアントの文書 | 確認を求める | [確認] |
| [C05-31](#g-c05-openai-31) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — MCP サーバー設定 | クライアントの文書 | 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う | [確認] |
| [C05-32](#g-c05-openai-32) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）設定 | クライアントの文書 | ツールを絞る・隠す・規則（ポリシー）の条件に使う | [確認] |
| [C05-33](#g-c05-openai-33) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（承認をレビュー用エージェントに回す） | クライアントの文書 | 確認を求める・危険度を付ける | [確認] |
| [C05-40](#g-c05-openai-40) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ） | クライアントのソースコード | ツールを絞る・隠す・宣言が無いときの扱い・規則（ポリシー）の条件に使う | [確認] |
| [C05-41](#g-c05-openai-41) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ） | クライアントのソースコード | ツールを絞る・隠す | [確認] |
| [C05-44](#g-c05-openai-44) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（guardian） | クライアントのソースコード | 危険度を付ける・そのまま渡す・見せる | [確認] |
| [C05-45](#g-c05-openai-45) | OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — trusted access（サイバー用途の資格情報文脈） | クライアントのソースコード | 規則（ポリシー）の条件に使う | [確認] |
| [C05-46](#g-c05-openai-46) | OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill（申請 JSON を作る Codex 用 skill） | 公式の文書 | 宣言を書くことを求める・宣言を検査する | [確認] |
| [C05-47](#g-c05-openai-47) | OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill | 公式の文書 | 宣言を検査する | [確認] |
| [C05-48](#g-c05-openai-48) | OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill | 公式の文書 | 宣言を検査する・作者への書き方の案内 | [確認] |
| [C05-49](#g-c05-openai-49) | OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C05-50](#g-c05-openai-50) | OpenAI — openai/skills — chatgpt-apps skill（.curated） | 公式の文書 | 作者への書き方の案内 | [確認] |
| [C05-51](#g-c05-openai-51) | OpenAI — ChatGPT / Codex の内蔵ブラウザ — Site tools（WebMCP） | クライアントの文書 | 信頼するなという注意 | [確認] |
| [C05-52](#g-c05-openai-52) | OpenAI — ChatGPT / Codex の内蔵ブラウザ — Site tools（WebMCP） | クライアントの文書 | 確認を求める・その他 | [確認] |
| [C05-53](#g-c05-openai-53) | OpenAI — ChatGPT（apps / コネクタの App permissions） | クライアントの文書 | 確認を省く（自動で許可）・確認を求める | [未確認] |

この分冊の資料は 52 件で、うち [確認] は 51 件、[確認（調査時のみ）] は 0 件。

<a id="ag-5-1"></a>
## 資料カード

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

<a id="g-c05-openai-01"></a>
#### C05-01 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Reference — Tool descriptor parameters > Annotations（developers.openai.com/plugins/reference）（公式の文書）
- **URL**: https://developers.openai.com/plugins/reference
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/reference#annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Reference > Tool descriptor parameters > Annotations (#annotations)
- **原文**:

> These hints only influence how ChatGPT or Codex frames the tool call to the user; servers must still enforce their own authorization logic.

- **日本語**: これらの hint は、ChatGPT や Codex がツール呼び出しをユーザーにどう見せるか（frame）にだけ影響する。サーバーは自分の認可ロジックを必ず実施しなければならない。
- **どう使っているか**: OpenAI の公式リファレンスが、4 つの hint の効果を「ChatGPT / Codex がツール呼び出しをユーザーにどう見せるか（frame）」に限定し、サーバーは自前の認可を必ず実施せよと書く。宣言はクライアント側の提示の入力であって、認可・強制の代わりにはならない、という OpenAI の立場。この文には「確認（confirmation）」の語は無い（確認に使うと書くのは 02・03）。
- **条件**: ChatGPT と Codex の両方が対象。どの hint の値がどの提示（確認ダイアログの有無など）に対応するかは、この文には書かれていない（不明。developer mode は 19〜21、Codex は 29〜41 を参照）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint ／ **使い方の分類**: 表示（印・名前）・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Reference > Tool descriptor parameters > Annotations」（取得 2026-10-02T22:11:23Z、sha256 b5b319f8e801…）
- **補足**: 同じ表で readOnlyHint / destructiveHint / openWorldHint は Required、idempotentHint は Optional と書かれている（表の列。Required の語そのものは tool で個別には照合していない）。表の前文は「To label a tool as "read-only," use the following ToolAnnotations fields」で、MCP 2025-11-25 の ToolAnnotations にリンクする。「見せ方にだけ影響する」という書き方は、Codex のコード（34: 宣言で承認の要否が決まる）や developer mode（19: readOnlyHint の無いツールは write 扱い）より弱い表現で、文書間で温度差がある。 【検証者】表のすぐ下のコード例は annotations: { readOnlyHint: true } だけを付けており（verify_quote.py: exact, 同じ #annotations 節）、表で Required とした destructiveHint / openWorldHint を省いている。表と例が食い違う。 usage から require_confirmation を外した（引用文は「frames the tool call」だけで、確認の要否には触れていない。過大）。usage_ja を直した。表の下のコード例が 3 つの Required のうち readOnlyHint しか付けていないことを notes に足した（tool で exact）。

<a id="g-c05-openai-02"></a>
#### C05-02 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Reference — Annotations 表の destructiveHint 行（公式の文書）
- **URL**: https://developers.openai.com/plugins/reference
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/reference#annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Reference > Tool descriptor parameters > Annotations (#annotations)
- **原文**:

> Declare that the tool may delete or overwrite user data so the host knows to elicit explicit approval first.

- **日本語**: （destructiveHint は）このツールがユーザーのデータを削除・上書きしうることを宣言し、ホストがまず明示的な承認を求められるようにする。
- **どう使っているか**: destructiveHint の目的を「ホストが事前に明示の承認を引き出すため」と定義する。destructiveHint:true → 承認要求、という使われ方を OpenAI が想定していることを示す。
- **条件**: 表の Required の列は、どの場面での必須か（ディレクトリ掲載時かどうか）を書いていない。ディレクトリ申請での必須は 05・09 による。承認を実際に出すかはホスト（ChatGPT / Codex）の実装と設定による。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 確認を求める・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Reference > Tool descriptor parameters > Annotations」（取得 2026-10-02T22:11:23Z、sha256 b5b319f8e801…）
- **補足**: 同じ表の readOnlyHint 行「Signal that the tool only retrieves or computes information and doesn't create, update, delete, or send data outside the conversation.」と openWorldHint 行の末尾「A bounded private account or workspace isn't open-world solely because it is externally hosted.」は、検証者が同じページで verify_quote.py を回して exact を得た（#annotations）。 conditions の「（ChatGPT ディレクトリ掲載時）」は表に書かれていない推測なので直した。notes の 2 行は検証者が tool で exact を確認した（finder は目視のみ）。

<a id="g-c05-openai-03"></a>
#### C05-03 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Build an MCP server — Tool annotations and elicitation（公式の文書）
- **URL**: https://developers.openai.com/plugins/build/mcp-server
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/build/mcp-server#tool-annotations-and-elicitation
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Build an MCP server > Tool annotations and elicitation (#tool-annotations-and-elicitation)
- **原文**:

> Annotations help ChatGPT and Codex choose appropriate confirmation and safety behavior. They do not replace authorization, validation, or confirmation in your server.

- **日本語**: annotations は、ChatGPT と Codex が適切な確認と安全上の振る舞いを選ぶのを助ける。サーバー側の認可・検証・確認の代わりにはならない。
- **どう使っているか**: 宣言が ChatGPT と Codex の「確認（confirmation）の選択」に使われると明言。同時に、サーバー側の認可・入力検証・確認を省いてよい理由にはならないとする。
- **条件**: ChatGPT と Codex。どの値でどの確認になるかは書かれていない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 確認を求める・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Build an MCP server > Tool annotations and elicitation」（取得 2026-10-02T22:11:25Z、sha256 ec17d6a13f13…）
- **補足**: 直前に「Set annotations according to actual behavior: readOnlyHint: true only when the tool cannot change state. destructiveHint: true when a tool can cause irreversible or difficult to reverse outcomes. openWorldHint: true when a tool accesses the public internet …」とある（宣言は実際の振る舞いに合わせよ、という著者向け指示）。

<a id="g-c05-openai-14"></a>
#### C05-14 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Optimize Metadata — Draft metadata that guides the model（公式の文書）
- **URL**: https://developers.openai.com/plugins/guides/optimize-metadata
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/guides/optimize-metadata#draft-metadata-that-guides-the-model
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Optimize Metadata > Draft metadata that guides the model (#draft-metadata-that-guides-the-model)
- **原文**:

> annotate `readOnlyHint: true` on tools that only retrieve or compute information and never create, update, delete, or send data outside the conversation.

- **日本語**: 情報を取得・計算するだけで、会話の外のデータを作成・更新・削除・送信しないツールには readOnlyHint: true を付ける。
- **どう使っているか**: ツールのメタデータ（モデルを導く情報）の一部として hint を付けるよう指示。著者向けの付け方の指針。
- **条件**: —
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Optimize Metadata > Draft metadata that guides the model」（取得 2026-10-02T22:11:23Z、sha256 a61bc3344b57…）
- **補足**: 同じ節：「Destructive hint: Annotate destructiveHint: false on tools that don't delete or overwrite user data.」「Open-world hint: …Use false for a tool limited to a bounded private account or workspace…」（tool 未照合）。tool が返した照合は loose（バッククォートの違い）。

<a id="g-c05-openai-15"></a>
#### C05-15 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Define tools — Plan safety annotations（openWorldHint）（公式の文書）
- **URL**: https://developers.openai.com/plugins/plan/tools
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plan/tools#plan-safety-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Define tools > Plan safety annotations (#plan-safety-annotations)
- **原文**:

> A bounded private account or workspace isn't open-world solely because it is externally hosted.

- **日本語**: 外部でホストされているというだけでは、境界のある私的なアカウントやワークスペースは open-world にならない。
- **どう使っているか**: openWorldHint の OpenAI 流の解釈：公開インターネットや不特定の外部主体に触れるなら true（読み取り専用の Web 検索も含む）、利用者のアカウント内に閉じるなら外部 SaaS でも false。
- **条件**: —
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Define tools > Plan safety annotations」（取得 2026-10-02T22:11:25Z、sha256 3780794193d7…）
- **補足**: 同節は MCP 2025-11-25 の ToolAnnotations を「canonical definitions, defaults, and interactions」として参照する。一方 OpenAI の plugins リポジトリの申請 skill（49）は openWorldHint を「公開状態や外部システムを変更しうるか」で定義しており、読み取りの Web 検索の扱いが文書間で食い違う。AuthGap の D3（openWorldHint:false の照合）では、どちらの定義を採るかで判定が変わる。

<a id="g-c05-openai-16"></a>
#### C05-16 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Define tools — Plan safety annotations（末尾）（公式の文書）
- **URL**: https://developers.openai.com/plugins/plan/tools
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plan/tools#plan-safety-annotations
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Define tools > Plan safety annotations (#plan-safety-annotations)
- **原文**:

> Annotations do not replace server-side authorization, input validation, or confirmation for consequential actions.

- **日本語**: annotations は、サーバー側の認可、入力検証、重大な操作での確認の代わりにはならない。
- **どう使っているか**: 宣言は強制ではない、という注意。
- **条件**: —
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Define tools > Plan safety annotations」（取得 2026-10-02T22:11:25Z、sha256 3780794193d7…）

<a id="g-c05-openai-17"></a>
#### C05-17 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載）

- **資料**: Connect and test your plugin — Check tool selection（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/connect-chatgpt
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/connect-chatgpt#check-tool-selection
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Connect and test your plugin > Test an MCP server (optional) > Check tool selection (#check-tool-selection)
- **原文**:

> For each request, record the selected tool, arguments, result, errors, and confirmation behavior. Rerun the set whenever you change tool names, descriptions, schemas, or annotations.

- **日本語**: 各リクエストについて、選ばれたツール、引数、結果、エラー、確認の振る舞いを記録する。ツール名・説明・スキーマ・annotations を変えたら、この評価セットを再実行する。
- **どう使っているか**: 開発者向けのテスト手順。評価セットで選ばれたツール・引数・結果・エラー・確認の振る舞いを記録し、ツール名・説明・スキーマ・annotations を変えたら取り直せ、と書く。annotations の変更が確認の振る舞いを変えるとは明記していない（並べて扱っているだけ）。
- **条件**: ChatGPT の developer mode で接続してテストするとき。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Connect and test your plugin > Test an MCP server (optional) > Check tool selection」（取得 2026-10-02T22:12:45Z、sha256 e3b60a99be9e…）
- **補足**: 同ページ上部（Inspect the MCP server）：MCP Inspector で「Verify schema validation, authentication errors, annotations, confirmation behavior, and the model-readable result.」（検証者が tool で exact を確認）。評価セットには「Write actions that require authorization or confirmation.」を含めよとある。 usage から require_confirmation を外した。引用文は annotations を変えたら評価を取り直せと言うだけで、annotations が確認を決めるとは書いていない（finder の『確認の振る舞いが変わりうるので』は推論）。notes の Inspector の文を tool で確認した。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Company knowledge

<a id="g-c05-openai-04"></a>
#### C05-04 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Company knowledge

- **資料**: Build an MCP server — Company knowledge compatibility（公式の文書）
- **URL**: https://developers.openai.com/plugins/build/mcp-server
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/build/mcp-server#company-knowledge-compatibility
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Build an MCP server > Company knowledge compatibility (#company-knowledge-compatibility)
- **原文**:

> Company knowledge can use read-only tools from your MCP server. To make a plugin eligible as a company knowledge source, implement the standard `search` and `fetch` tool input schemas and mark other read-only tools with `readOnlyHint: true`.

- **日本語**: Company knowledge は MCP サーバーの読み取り専用ツールを使える。plugin を company knowledge の情報源にするには、標準の search と fetch の入力スキーマを実装し、それ以外の読み取り専用ツールに readOnlyHint: true を付ける。
- **どう使っているか**: plugin が ChatGPT の company knowledge の情報源として認められる条件（eligibility）として、標準の search / fetch の実装と、それ以外の読み取り専用ツールへの readOnlyHint: true を求める。company knowledge が readOnlyHint でツールを選んでいると読めるが、選別の仕組みそのものは書かれていない（推論）。
- **条件**: ChatGPT の company knowledge（ワークスペースの社内知識検索）として使う場合のみ。readOnlyHint の無いツールが company knowledge で使われるかは書かれていない（文意からは使われないと読めるが、明記はない＝不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: ツールを絞る・隠す・作者への書き方の案内
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Build an MCP server > Company knowledge compatibility」（取得 2026-10-02T22:11:25Z、sha256 ec17d6a13f13…）
- **補足**: 宣言が嘘（readOnlyHint:true なのに書き込む）の場合の扱いは書かれていない。 usage_ja の「使ってよいツールの選別に使われる例」は言い過ぎ。文書が言うのは『情報源として認められる条件』で、選別の仕組みは書かれていない。推論である旨を明記した。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準

<a id="g-c05-openai-05"></a>
#### C05-05 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準

- **資料**: Plugin guidelines — MCP requirements > Tools > Correct annotation（規約・審査の指針）
- **URL**: https://developers.openai.com/plugins/plugin-guidelines
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plugin-guidelines#correct-annotation
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin guidelines > MCP requirements > Tools > Correct annotation (#correct-annotation)
- **原文**:

> Set `readOnlyHint`, `destructiveHint`, and `openWorldHint` to explicit boolean values (`true` or `false`) in each tool’s `annotations` object. Annotation justifications are no longer required. If our automated review flags an annotation issue, you can submit an appeal with clarification or additional information.

- **日本語**: readOnlyHint・destructiveHint・openWorldHint を、各ツールの annotations オブジェクトで明示的な真偽値（true か false）にすること。annotation の根拠説明（justification）はもう不要。自動審査が annotation の問題を指摘した場合は、説明や追加情報を添えて異議申し立てができる。
- **どう使っているか**: ChatGPT Directory に載せる plugin は 3 つの hint を明示の true/false で宣言する義務がある（省略・null は不可）。さらに「自動審査（automated review）」が annotation の問題を検出すると書かれており、宣言の妥当性を OpenAI 側で機械的に点検していることを示す。
- **条件**: ChatGPT Directory（公開ディレクトリ）に公開する plugin が対象。idempotentHint は要求されていない。自動審査が何を手がかりに annotation の誤りを判定するか（説明文・スキーマ・実行結果・コード）は書かれていない（不明）。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Plugin guidelines > MCP requirements > Tools > Correct annotation」（取得 2026-10-02T22:11:24Z、sha256 9de078e138b5…）
- **補足**: 文書間の矛盾：このページは「Annotation justifications are no longer required」とするが、Plugin submission errors（10）には justification_required、Remote MCP server review requirements（11）と submission-errors の最終申請要件には「a justification for each value」が残っている。どちらが現行かは不明（同日取得）。

<a id="g-c05-openai-06"></a>
#### C05-06 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準

- **資料**: Plugin guidelines — Correct annotation（末尾）（規約・審査の指針）
- **URL**: https://developers.openai.com/plugins/plugin-guidelines
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plugin-guidelines#correct-annotation
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin guidelines > MCP requirements > Tools > Correct annotation (#correct-annotation)
- **原文**:

> Annotations inform client safeguards; they do not grant permission or replace authentication, authorization and scope checks, input validation, or human confirmation for irreversible operations.

- **日本語**: annotations はクライアントの安全策に情報を与えるが、許可を与えるものではなく、認証、認可とスコープの確認、入力検証、取り消せない操作での人による確認の代わりにもならない。
- **どう使っているか**: 宣言の位置づけ：クライアントの安全策（確認など）への入力であり、権限付与ではない。宣言を信じて安全策を緩めるのはクライアント側、という前提を明示。
- **条件**: ChatGPT Directory 掲載 plugin。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 規則（ポリシー）の条件に使う・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Plugin guidelines > MCP requirements > Tools > Correct annotation」（取得 2026-10-02T22:11:24Z、sha256 9de078e138b5…）
- **補足**: 同じ節で destructiveHint は「irreversible sends or transactions」を Security & Privacy の『Prompt injection and write actions』に結びつけている。

<a id="g-c05-openai-07"></a>
#### C05-07 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準

- **資料**: Plugin guidelines — Correct annotation（destructiveHint の基準）（規約・審査の指針）
- **URL**: https://developers.openai.com/plugins/plugin-guidelines
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plugin-guidelines#correct-annotation
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin guidelines > MCP requirements > Tools > Correct annotation (#correct-annotation)
- **原文**:

> Use `false` only for additive writes without destructive or irreversible effects. Being able to undo an action does not, by itself, justify setting `destructiveHint` to `false`.

- **日本語**: （destructiveHint を）false にしてよいのは、破壊的・不可逆な効果の無い追加型の書き込みだけ。元に戻せるというだけでは destructiveHint を false にする理由にならない。
- **どう使っているか**: destructiveHint の付け方の基準。MCP 仕様の『additive updates のみなら false』を、取り消し可能性では正当化できないと厳しめに解釈している。
- **条件**: ChatGPT Directory 掲載 plugin。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Plugin guidelines > MCP requirements > Tools > Correct annotation」（取得 2026-10-02T22:11:24Z、sha256 9de078e138b5…）
- **補足**: 同じ箇所の readOnlyHint 基準：「Use false for external-state changes, persisting artifacts, starting stateful jobs or workflows, queuing work, or write-style outbound actions such as posting messages, sending emails, or uploading files.」（検証者が tool で exact を確認、#correct-annotation）。成果物の保存、ジョブやワークフローの開始、キューへの投入も readOnlyHint:false とする点は、AuthGap の D1 の判定基準と比べる価値がある。『ログの書き込み』はこのページには無く、app-review の却下理由（12）に出る。 notes の「ログ書き込み」はこのページ（plugin guidelines）には無い（app-review の 12 にある）ので直した。readOnlyHint 基準の文は tool で exact を確認した。

<a id="g-c05-openai-08"></a>
#### C05-08 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — ChatGPT Directory 掲載基準

- **資料**: Plugin guidelines — Plugin fundamentals > Safety > Fair play（規約・審査の指針）
- **URL**: https://developers.openai.com/plugins/plugin-guidelines
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/plugin-guidelines#fair-play
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin guidelines > Plugin fundamentals > Safety > Fair play (#fair-play)
- **原文**:

> Plugins must not include descriptions, titles, tool annotations, or other model-readable fields, at either the tool or plugin level, that manipulate how the model selects or uses other plugins or their tools

- **日本語**: plugin は、ツールや plugin の水準で、説明・タイトル・ツール annotations、その他モデルが読むフィールドに、他の plugin やそのツールをモデルがどう選び・使うかを操作する内容を含めてはならない。
- **どう使っているか**: tool annotations を「モデルが読むフィールド」と位置づけ、そこを使ったツール選択の誘導を掲載基準で禁止している。宣言がモデルの入力にもなるという前提。
- **条件**: ChatGPT Directory 掲載 plugin。
- **扱う宣言**: 宣言全般・title ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Plugin guidelines > Plugin fundamentals > Safety > Fair play」（取得 2026-10-02T22:11:24Z、sha256 9de078e138b5…）
- **補足**: annotations 自体の値の正しさではなく、悪用（他ツールの誘導）の禁止。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータルの検証

<a id="g-c05-openai-09"></a>
#### C05-09 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータルの検証

- **資料**: Plugin submission errors — MCP and review errors: annotations_required（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/submission-errors
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/submission-errors#mcp-and-review-errors
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin submission errors > Final directory submission > MCP and review errors (#mcp-and-review-errors)
- **原文**:

> Every MCP tool must set `readOnlyHint`, `openWorldHint`, and `destructiveHint` accurately.

- **日本語**: （annotations_required）すべての MCP ツールは readOnlyHint・openWorldHint・destructiveHint を正確に設定しなければならない。
- **どう使っているか**: 申請時のエラー名 annotations_required。3 つの hint が無いと公開ディレクトリへの申請が通らない（提出時の検証）。
- **条件**: 公開ディレクトリへ remote MCP 付き plugin を申請するとき。「accurately（正確に）」をどう検査するかは書かれていない（不明。表は有無の検証エラーの一覧）。
- **扱う宣言**: readOnlyHint・openWorldHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Plugin submission errors > Final directory submission > MCP and review errors」（取得 2026-10-02T22:11:24Z、sha256 ab27c9bce96e…）
- **補足**: 同ページの冒頭に「Errors block submission.」とあり（tool で exact）、このエラーが出ると申請できない。最終申請要件にも「Explicit readOnlyHint, openWorldHint, and destructiveHint values and a justification for each value on every MCP tool.」とある（tool で exact、#final-directory-submission）。 usage_ja の『申請が通らない』の根拠（Errors block submission.）を tool で確認して notes に足した。最終申請要件の文も tool で exact を確認した（finder は目視）。

<a id="g-c05-openai-10"></a>
#### C05-10 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータルの検証

- **資料**: Plugin submission errors — MCP and review errors: justification_required（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/submission-errors
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/submission-errors#mcp-and-review-errors
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Plugin submission errors > Final directory submission > MCP and review errors (#mcp-and-review-errors)
- **原文**:

> Every MCP tool annotation must include a justification for its read-only, open-world, or destructive behavior.

- **日本語**: （justification_required）MCP ツールの各 annotation には、読み取り専用・open-world・破壊的な振る舞いについての根拠説明を付けなければならない。
- **どう使っているか**: 宣言の値ごとに、人が読む根拠説明（justification）の提出を求める検証エラー。
- **条件**: 公開ディレクトリ申請時。
- **扱う宣言**: readOnlyHint・openWorldHint・destructiveHint ／ **使い方の分類**: 宣言を書くことを求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Plugin submission errors > Final directory submission > MCP and review errors」（取得 2026-10-02T22:11:24Z、sha256 ab27c9bce96e…）
- **補足**: Plugin guidelines（05）の「Annotation justifications are no longer required」と矛盾する。どちらが現行かは不明（2026-10-02 に両方取得）。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータル（Scan Tools）

<a id="g-c05-openai-11"></a>
#### C05-11 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 申請ポータル（Scan Tools）

- **資料**: Remote MCP server review requirements — Metadata stored during tool scanning（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/app-review
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/app-review#metadata-stored-during-tool-scanning
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Remote MCP server review requirements > Submit for review > Metadata stored during tool scanning (#metadata-stored-during-tool-scanning)
- **原文**:

> Your submission justifications should explain why those server-provided annotation values match each tool's behavior. They don't override the annotations. For example, if your server advertises `readOnlyHint: false`, describing the tool as “functionally read-only” in the justification doesn't make the tool read-only.

- **日本語**: 申請の根拠説明では、サーバーが返す annotation の値が各ツールの振る舞いに合う理由を説明すること。根拠説明は annotation を上書きしない。たとえばサーバーが readOnlyHint: false を返しているなら、根拠説明で「実質的に読み取り専用」と書いてもそのツールは読み取り専用にならない。
- **どう使っているか**: Scan Tools がサーバーの宣言をそのまま取り込みダッシュボードに表示し、審査ではサーバーが実際に返す値が正本になる（説明文で上書き不可）。修正はサーバー側の annotation を直して再スキャン。
- **条件**: 公開ディレクトリ申請時（ダッシュボードの Scan Tools）。
- **扱う宣言**: readOnlyHint・宣言全般 ／ **使い方の分類**: 宣言を検査する・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Remote MCP server review requirements > Submit for review > Metadata stored during tool scanning」（取得 2026-10-02T22:11:29Z、sha256 315772647129…）
- **補足**: 直前の文：「The dashboard displays the annotation values provided by your server.」（tool では照合していない）。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 審査（却下理由）

<a id="g-c05-openai-12"></a>
#### C05-12 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 審査（却下理由）

- **資料**: Remote MCP server review requirements — Review and approval FAQs（却下理由: Tool hint annotations do not appear to match the tool's behavior）（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/app-review
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/app-review#review-and-approval-faqs
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Remote MCP server review requirements > Review and approval > Review and approval FAQs (#review-and-approval-faqs)
- **原文**:

> Tool hint annotations do not appear to match the tool's behavior: readOnlyHint: Set to `true` if it strictly fetches/looks up/lists/retrieves data and does not modify anything.

- **日本語**: （却下理由）ツールの hint annotation がツールの振る舞いと合っていないように見える：readOnlyHint は、厳密にデータを取得・照会・一覧・検索するだけで何も変更しない場合に true にする。
- **どう使っているか**: 宣言と実際の振る舞いの不一致が、審査の『よくある却下理由』に挙がっている。OpenAI の審査が宣言の正しさを（方法は不明だが）振る舞いに照らして見ていることを示す。
- **条件**: 公開ディレクトリ審査。同ページの Reviews and checks は「We may perform automated scans or manual reviews …」（自動スキャンか人手の審査を行うことがある）と書くだけで、annotation の不一致をどう見つけるか（人手・自動・テスト実行・コード）は書かれていない（不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言を検査する・作者への書き方の案内
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Remote MCP server review requirements > Review and approval > Review and approval FAQs」（取得 2026-10-02T22:11:29Z、sha256 315772647129…）
- **補足**: 続く文「Set to false if the tool can create/update/delete anything, trigger actions (send emails/messages, run jobs, enqueue tasks, write logs, start workflows), or otherwise change state.」は検証者が tool で exact を確認した。AuthGap の主張（宣言と実効の照合）に最も近い OpenAI 側の運用記述。 usage_ja の『証拠』を弱めた。conditions に同ページの Reviews and checks（may perform automated scans or manual reviews、tool で exact）を足した。notes の続く文を tool で確認した。

<a id="g-c05-openai-13"></a>
#### C05-13 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — 審査（却下理由）

- **資料**: Remote MCP server review requirements — Review and approval FAQs（Destructive hint）（公式の文書）
- **URL**: https://developers.openai.com/plugins/deploy/app-review
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/deploy/app-review#review-and-approval-faqs
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Remote MCP server review requirements > Review and approval > Review and approval FAQs (#review-and-approval-faqs)
- **原文**:

> Set the destructive annotation to `true` if the tool can cause irreversible outcomes (deleting, overwriting, sending messages or transactions you can't undo, revoking access, or destructive admin actions), even in only select modes, through default parameters, or through indirect side effects.

- **日本語**: 取り消せない結果（削除、上書き、取り消せないメッセージや取引の送信、アクセスの取り消し、破壊的な管理操作）を起こしうるなら、一部のモードだけ、既定の引数経由、間接的な副作用経由であっても、destructive annotation を true にする。
- **どう使っているか**: destructiveHint の審査基準。『一部のモードだけ』『既定パラメータ経由』『間接的な副作用』でも true にせよ、という厳しめの基準（引数でモードが変わる万能ツールも対象）。
- **条件**: 公開ディレクトリ審査。
- **扱う宣言**: destructiveHint ／ **使い方の分類**: 作者への書き方の案内・宣言を検査する
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Remote MCP server review requirements > Review and approval > Review and approval FAQs」（取得 2026-10-02T22:11:29Z、sha256 315772647129…）
- **補足**: 同じ FAQ の openWorldHint 基準「openWorldHint: Set to true if the tool accesses the public internet or open-ended external entities. This includes read-only tools such as web search and write tools that post to public platforms, send messages to external recipients, publish content, push code, or submit forms.」と、続く「Set to false if the tool is limited to a bounded private account or workspace, even when that service is externally hosted.」がある（前者は検証者が tool で exact を確認）。 notes の openWorldHint 基準の文を tool で確認し、省略されていた『書き込み系（公開投稿・外部送信・push・フォーム送信）も true』の部分を補った。

### OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Claude Code plugin からの移行

<a id="g-c05-openai-18"></a>
#### C05-18 OpenAI — ChatGPT plugins / Apps SDK（ChatGPT・Codex 向け MCP サーバーの開発・掲載） — Claude Code plugin からの移行

- **資料**: Submit your Claude Code plugin to OpenAI — Prepare and submit the MCP server（公式の文書）
- **URL**: https://developers.openai.com/plugins/guides/submit-claude-plugin
- **書いてある見出しへ直接**: https://developers.openai.com/plugins/guides/submit-claude-plugin#prepare-and-submit-the-mcp-server
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Submit your Claude Code plugin to OpenAI > Submit a plugin with a remote MCP server > Prepare and submit the MCP server (#prepare-and-submit-the-mcp-server)
- **原文**:

> Add accurate tool schemas and safety annotations. Test that every tool connects, authenticates, returns the expected result shape, and requires the intended confirmation for write or destructive actions.

- **日本語**: 正確なツールスキーマと安全上の annotations を付ける。各ツールが接続・認証でき、期待した形の結果を返し、書き込みや破壊的操作では意図した確認を求めることをテストする。
- **どう使っているか**: Claude Code 向け plugin / コネクタを OpenAI に出すときの手順。safety annotations と『write / destructive 操作での確認』を対にしてテストさせる。
- **条件**: Claude Code の plugin・コネクタを OpenAI の plugin に変換して申請する場合。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 作者への書き方の案内・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Submit your Claude Code plugin to OpenAI > Submit a plugin with a remote MCP server > Prepare and submit the MCP server」（取得 2026-10-02T22:11:25Z、sha256 675e70bb6ed8…）

### OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続）

<a id="g-c05-openai-19"></a>
#### C05-19 OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続）

- **資料**: ChatGPT Developer mode — How to use > Reviewing and confirming tool calls（クライアントの文書）
- **URL**: https://developers.openai.com/api/docs/guides/developer-mode
- **書いてある見出しへ直接**: https://developers.openai.com/api/docs/guides/developer-mode#how-to-use
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: ChatGPT Developer mode > How to use (#how-to-use)
- **原文**:

> Read-only detection: We respect the `readOnlyHint` tool annotation (see MCP tool annotations). Tools without this hint are treated as write actions.

- **日本語**: 読み取り専用の判定：readOnlyHint ツール annotation を尊重する（MCP tool annotations を参照）。この hint が無いツールは書き込み操作として扱う。
- **どう使っているか**: ChatGPT（developer mode）は読み取り専用かどうかの判定に readOnlyHint を使い、hint が無いツールは write 扱いにする（欠落時は安全側）。write は既定で確認が必要（20）なので、readOnlyHint の有無が確認の有無を左右する。destructiveHint / openWorldHint を見るかは書かれていない。
- **条件**: ChatGPT の developer mode（Pro / Plus / Business / Enterprise / Education の Web）で作った developer-mode app。readOnlyHint:true のツールが確認なしで実行されると明記した文は無い（20 と合わせた推論。明記なし）。destructiveHint / openWorldHint を見るかは書かれていない（不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「ChatGPT Developer mode > How to use」（取得 2026-10-02T22:11:23Z、sha256 6445645e6803…）
- **補足**: tool の照合は loose（バッククォートとリンクの差）。リンク先は MCP の legacy/concepts/tools#available-tool-annotations。宣言が嘘（readOnlyHint:true で書き込む）だと確認なしで書き込みが通りうるが、その注意はこのページには無い。 usage_ja の「readOnlyHint だけで判定」は言い過ぎ（文書は readOnlyHint を尊重するとだけ書き、他の hint を見ないとは書いていない）。直した。

<a id="g-c05-openai-20"></a>
#### C05-20 OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続）

- **資料**: ChatGPT Developer mode — Reviewing and confirming tool calls（クライアントの文書）
- **URL**: https://developers.openai.com/api/docs/guides/developer-mode
- **書いてある見出しへ直接**: https://developers.openai.com/api/docs/guides/developer-mode#how-to-use
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: ChatGPT Developer mode > How to use (#how-to-use)
- **原文**:

> Write actions by default require confirmation. Carefully review the tool input which will be sent to a write action to ensure the behavior is as desired.

- **日本語**: 書き込み操作は既定で確認が必要。書き込み操作に送られるツール入力を注意深く見て、意図どおりの振る舞いになるか確かめること。
- **どう使っているか**: write 扱いのツール（19 により readOnlyHint の無いもの・false のもの）は既定で呼び出しごとに確認。
- **条件**: developer mode。『既定で』とあるが、既定を変える設定の名前はこのページには無い（20〜21 の記憶機能以外は不明）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「ChatGPT Developer mode > How to use」（取得 2026-10-02T22:11:23Z、sha256 6445645e6803…）
- **補足**: このページで hint の名前は 19 の文にだけ出る。

<a id="g-c05-openai-21"></a>
#### C05-21 OpenAI — ChatGPT Developer mode（任意の MCP サーバーを ChatGPT に接続）

- **資料**: ChatGPT Developer mode — Reviewing and confirming tool calls（承認の記憶）（クライアントの文書）
- **URL**: https://developers.openai.com/api/docs/guides/developer-mode
- **書いてある見出しへ直接**: https://developers.openai.com/api/docs/guides/developer-mode#how-to-use
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: ChatGPT Developer mode > How to use (#how-to-use)
- **原文**:

> You can choose to remember the approve or deny choice for a given tool for a conversation, which means it will apply that choice for the rest of that conversation.

- **日本語**: あるツールについて承認または拒否の選択を会話の間だけ記憶させることができ、その会話の残りではその選択が適用される。
- **どう使っているか**: write 扱いのツールの承認・拒否の選択を、その会話の間だけ記憶できる。承認を記憶すれば、その会話の残りでは確認なしで実行される（宣言とは別に、利用者の選択で確認が省かれる経路）。拒否を記憶すれば以後は拒否される。
- **条件**: developer mode。新しい会話と、同じ会話の再読み込みの後は、再び確認される（「New conversations will prompt for confirmation again. Refreshing the same conversation will also prompt for confirmation again on subsequent turns.」、検証者が tool で exact を確認）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「ChatGPT Developer mode > How to use」（取得 2026-10-02T22:11:23Z、sha256 6445645e6803…）
- **補足**: usage_ja の『以後は確認なしで実行』は承認を記憶したときだけなので直した。conditions の続く文を tool で確認した。

### OpenAI — OpenAI API — Responses API の remote MCP ツール（type: mcp）

<a id="g-c05-openai-23"></a>
#### C05-23 OpenAI — OpenAI API — Responses API の remote MCP ツール（type: mcp）

- **資料**: MCP servers（tools-connectors-mcp）— Approvals（公式の文書）
- **URL**: https://developers.openai.com/api/docs/guides/tools-connectors-mcp
- **書いてある見出しへ直接**: https://developers.openai.com/api/docs/guides/tools-connectors-mcp#approvals
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: MCP servers > How it works > Step 2: Calling tools > Approvals (#approvals)
- **原文**:

> By default, OpenAI will request your approval before any data is shared with a connector or remote MCP server.

- **日本語**: 既定では、コネクタや remote MCP サーバーにデータが共有される前に、OpenAI があなたの承認を求める。
- **どう使っているか**: Responses API の既定では、宣言に関係なくすべての MCP 呼び出しで承認要求（mcp_approval_request）が出る。つまり既定では annotations は承認の要否に効かない。宣言で承認を外すには、開発者が require_approval に read_only フィルタ（24）を書く必要がある。
- **条件**: Responses API の remote MCP / コネクタ。require_approval を 'never' にすると全ツールが承認なし（同じ Approvals 節「or set it to the value 'never' to skip approvals for all tools in that remote MCP server.」、tool で exact）。Realtime API の MCP ガイド（realtime-mcp）は require_approval を任意の項目として挙げるだけで、既定が承認ありかどうかは書いていない（finder の『Realtime API の MCP も同じ』は根拠なし）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「MCP servers > How it works > Step 2: Calling tools > Approvals」（取得 2026-10-02T22:11:22Z、sha256 5c106df74cca…）
- **補足**: このガイド本文には readOnlyHint / destructiveHint の語は無い（checked_no_mention）。mcp_list_tools の出力例ではツールごとに "annotations": null が返されている（宣言をそのまま透過する欄、26）。 conditions の『（および Realtime API の MCP）』は Realtime のガイドに既定の記載が無く根拠が無いので外した。usage の defaults_when_missing は『annotations 欠落時』の話ではないので ignored_or_not_used（既定では annotations が効かない）に替えた。'never' の文を tool で確認した。

<a id="g-c05-openai-24"></a>
#### C05-24 OpenAI — OpenAI API — Responses API の remote MCP ツール（type: mcp）

- **資料**: API reference — Create a model response > Body Parameters > tools > Mcp > allowed_tools / require_approval（McpToolFilter.read_only）（公式の文書）
- **URL**: https://developers.openai.com/api/reference/resources/responses/methods/create
- **照らし合わせた中身の URL**: https://developers.openai.com/api/reference/resources/responses/methods/create.md
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: lines 1614-1616（直前の見出し: ### Body Parameters）。同じ文が 24 か所に一致し、これは 1 件目（tools > Mcp > allowed_tools の read_only）
- **原文**:

> Indicates whether or not a tool modifies data or is read-only. If an MCP server is [annotated with `readOnlyHint`](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations-readonlyhint), it will match this filter.

- **日本語**: （read_only）ツールがデータを変更するか読み取り専用かを示す。MCP サーバーが readOnlyHint の annotation を付けていれば、このフィルタに一致する。
- **どう使っているか**: Responses API の MCP ツール設定で、allowed_tools（使えるツールの絞り込み）と require_approval.always / require_approval.never（承認の要否）に read_only フィルタを書ける。readOnlyHint を付けたツールがこのフィルタに一致するので、例えば require_approval: {never: {read_only: true}} で読み取り専用宣言のツールだけ承認なしにできる。宣言が OpenAI のサーバー側で承認・露出の判定に使われる一次資料。
- **条件**: 開発者が read_only フィルタを明示した場合のみ（既定は全呼び出しで承認、23）。readOnlyHint が無い・false のツールが read_only: false のフィルタに一致するかは書かれていない（不明）。判定は OpenAI 側（Responses API）が行う。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・24 か所、1614-1616 行（### Body Parameters）（取得 2026-10-02T22:11:23Z、sha256 e9c46fb7f7a2…）
- **補足**: public の HTML（https://developers.openai.com/api/reference/resources/responses/methods/create）でも、リンクを外した形の同文「Indicates whether or not a tool modifies data or is read-only. If an MCP server is annotated with readOnlyHint, it will match this filter.」が exact で 24 件一致した（検証者の再実行 2026-10-02T17:04:51Z、sha256=181ebe96da80、約 12MB。ディスクの空きが少ないため照合後にキャッシュから消した）。記録した quote は .md 版（リンク記法つき）で照合したもの。24 件はすべてこの create のページの中で、Body Parameters に 9 件・Returns に 15 件。どれも MCP ツール定義の allowed_tools / require_approval.always / require_approval.never の 3 か所の組（.md の 1614〜1616 行が allowed_tools、1690〜1692 行が always、1704〜1706 行が never）。リファレンスは require_approval の既定値を書いていない（既定は 23 のガイドによる）。リンク先は MCP 2025-06-18 の schema#toolannotations-readonlyhint。 notes の『24 件は他のエンドポイントのスキーマとの重複』は誤り。24 件はすべて create のページの中（Body Parameters 9 件、Returns 15 件。各 3 か所）。public HTML 版の照合を新しいキャッシュでやり直した。

### OpenAI — openai-python SDK（Responses API の型）

<a id="g-c05-openai-25"></a>
#### C05-25 OpenAI — openai-python SDK（Responses API の型）

- **資料**: src/openai/types/responses/tool.py — McpRequireApprovalMcpToolApprovalFilterNever（SDK のソースコード）
- **URL**: https://github.com/openai/openai-python/blob/e5de2e5656fb3d4fa70f050195382e6a4d59f806/src/openai/types/responses/tool.py#L80-L89
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/openai-python/e5de2e5656fb3d4fa70f050195382e6a4d59f806/src/openai/types/responses/tool.py
- **版**: commit e5de2e5656fb3d4fa70f050195382e6a4d59f806（2026-10-02 の HEAD）
- **書いてある場所**: lines 80-89
- **原文**:

```
class McpRequireApprovalMcpToolApprovalFilterNever(BaseModel):
    """A filter object to specify which tools are allowed."""

    read_only: Optional[bool] = None
    """Indicates whether or not a tool modifies data or is read-only.

    If an MCP server is
    [annotated with `readOnlyHint`](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations-readonlyhint),
    it will match this filter.
    """
```

- **日本語**: （承認不要フィルタ never の型）read_only: ツールがデータを変更するか読み取り専用かを示す。MCP サーバーが readOnlyHint の annotation を付けていれば、このフィルタに一致する。
- **どう使っているか**: 公式 Python SDK は read_only を API に渡す型を持つだけで、照合は API 側。require_approval.never.read_only=true で readOnlyHint 付きツールの承認を外せることが SDK の docstring にも書かれている。
- **条件**: Responses API の MCP ツール。SDK 自身は annotations を評価しない（OpenAPI から生成されたコード）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、80-89 行（# File generated from our OpenAPI spec by Castiron. See CONTRIBUTING.md for details.）（取得 2026-10-02T22:11:36Z、sha256 f59d24041703…）
- **補足**: 同ファイル 50〜56 行（McpAllowedToolsMcpToolFilter）と 68〜74 行（…FilterAlways）にも同じ docstring がある（目視）。

<a id="g-c05-openai-26"></a>
#### C05-26 OpenAI — openai-python SDK（Responses API の型）

- **資料**: src/openai/types/responses/response_output_item.py — McpListTools のツール定義（SDK のソースコード）
- **URL**: https://github.com/openai/openai-python/blob/e5de2e5656fb3d4fa70f050195382e6a4d59f806/src/openai/types/responses/response_output_item.py#L235-L236
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/openai-python/e5de2e5656fb3d4fa70f050195382e6a4d59f806/src/openai/types/responses/response_output_item.py
- **版**: commit e5de2e5656fb3d4fa70f050195382e6a4d59f806
- **書いてある場所**: lines 235-236
- **原文**:

```
annotations: Optional[object] = None
    """Additional annotations about the tool."""
```

- **日本語**: annotations: Optional[object] = None ／ ツールについての追加の annotations。
- **どう使っているか**: Responses API の mcp_list_tools 出力は、MCP サーバーが返した annotations を型づけせずに（object）開発者へ透過する。
- **条件**: Responses API の出力。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、235-236 行（# File generated from our OpenAPI spec by Castiron. See CONTRIBUTING.md for details.）（取得 2026-10-02T22:11:37Z、sha256 d23435cc32ba…）
- **補足**: ガイドの例（23 のページ）では "annotations": null。

### OpenAI — OpenAI Agents SDK（TypeScript）— Hosted MCP server tools

<a id="g-c05-openai-27"></a>
#### C05-27 OpenAI — OpenAI Agents SDK（TypeScript）— Hosted MCP server tools

- **資料**: Model Context Protocol (MCP) — Hosted MCP options reference（SDK の文書）
- **URL**: https://openai.github.io/openai-agents-js/guides/mcp/
- **書いてある見出しへ直接**: https://openai.github.io/openai-agents-js/guides/mcp/#hosted-mcp-options-reference
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Model Context Protocol (MCP) > 1. Hosted MCP server tools > Hosted MCP options reference (#hosted-mcp-options-reference)
- **原文**:

> The requireApproval object form accepts optional always and never entries. Each entry can select tools with toolNames or by their read-only annotation.

- **日本語**: requireApproval のオブジェクト形式は、任意の always と never の項目を受け付ける。各項目は toolNames か、ツールの読み取り専用 annotation でツールを選べる。
- **どう使っているか**: Hosted MCP（Responses API 側で実行される MCP）の承認ポリシーで、読み取り専用 annotation を選択条件に使える（24 の read_only フィルタをそのまま露出）。
- **条件**: Hosted MCP server tools（hostedMcpTool）のみ。ローカルの MCP サーバー（stdio / streamable HTTP）の承認条件に annotation が使われるとは書かれていない（ページ内に readOnlyHint の語は無い）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Model Context Protocol (MCP) > 1. Hosted MCP server tools > Hosted MCP options reference」（取得 2026-10-02T22:11:27Z、sha256 cdcd4703f5d3…）
- **補足**: Python 版 Agents SDK の MCP ページ（openai.github.io/openai-agents-python/mcp/）には annotation の語が無い（checked_no_mention）。Python 版のローカル MCP の require_approval はツール名だけで指定する。

### OpenAI — OpenAI Agents SDK（TypeScript）

<a id="g-c05-openai-28"></a>
#### C05-28 OpenAI — OpenAI Agents SDK（TypeScript）

- **資料**: packages/agents-core/src/utils/mcpApproval.ts — Hosted MCP の require_approval 正規化（SDK のソースコード）
- **URL**: https://github.com/openai/openai-agents-js/blob/58b08f846c28ef070118f628c4fb0e84d52ca110/packages/agents-core/src/utils/mcpApproval.ts#L74-L80
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/openai-agents-js/58b08f846c28ef070118f628c4fb0e84d52ca110/packages/agents-core/src/utils/mcpApproval.ts
- **版**: commit 58b08f846c28ef070118f628c4fb0e84d52ca110（2026-10-02 の HEAD）
- **書いてある場所**: lines 74-80
- **原文**:

```
  const readOnly = value.readOnly ?? value.read_only;
  if (typeof readOnly !== 'undefined') {
    if (typeof readOnly !== 'boolean') {
      throw invalidRequireApproval(`${path}.readOnly must be a boolean.`);
    }
    normalized.read_only = readOnly;
  }
```

- **日本語**: readOnly（または read_only）を読み、真偽値でなければエラー、真偽値なら read_only として API へ送る形に正規化する。
- **どう使っているか**: SDK は readOnly フィルタを Responses API の read_only に変換して渡すだけで、annotation の評価は API 側。
- **条件**: Hosted MCP のみ。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、74-80 行（取得 2026-10-02T22:11:36Z、sha256 9f734e11f9bb…）
- **補足**: packages/agents-core/src/mcp.ts（ローカル MCP）には readOnlyHint / destructiveHint / openWorldHint の語が無い（checked_no_mention）。mcp.ts の annotations フィールドは resource / resource template のもの。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

<a id="g-c05-openai-29"></a>
#### C05-29 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: Agent approvals & security — Sandbox and approvals（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/agent-approvals-security
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/agent-approvals-security#sandbox-and-approvals
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Agent approvals & security > Sandbox and approvals (#sandbox-and-approvals)
- **原文**:

> Destructive app/MCP tool calls always require approval when the tool advertises a destructive annotation (unless the tool advertises a read annotation, which takes priority).

- **日本語**: 破壊的な app / MCP ツール呼び出しは、そのツールが destructive annotation を広告していれば常に承認が必要（ただしツールが read annotation を広告していればそちらが優先）。
- **どう使っているか**: Codex は destructive annotation で承認を要求する、と公式ドキュメントが明記。ただし『read annotation が優先』と書いており、コード（34, 38）とは逆。
- **条件**: Codex の app（コネクタ）/ MCP ツール呼び出し。approval mode や approval_policy による例外（37）はこの文には無い。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 確認を求める・確認を省く（自動で許可）
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Agent approvals & security > Sandbox and approvals」（取得 2026-10-02T22:11:35Z、sha256 6160447f94d2…）
- **補足**: 【文書とコードの食い違い】pin したコード（commit ca466061）の requires_mcp_tool_approval は destructiveHint==true を最初に見て true を返し、readOnlyHint:true でも承認が必要（テスト approval_required_when_destructive_even_if_read_only_true, 38）。App Server のドキュメント（30）も「destructive は less-privileged な hint があっても常に承認」とコード側に一致する。『read が優先』が成り立つのは writes モード（35: readOnlyHint だけを見る）。直前の文：「Codex can also elicit approval for app (connector) tool calls that advertise side effects, even when the action isn't a shell command or file change.」

<a id="g-c05-openai-34"></a>
#### C05-34 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/core/src/mcp_tool_call.rs — requires_mcp_tool_approval（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs#L2463-L2480
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc（2026-10-02 の HEAD）
- **書いてある場所**: lines 2463-2480
- **原文**:

```
fn requires_mcp_tool_approval(annotations: Option<&ToolAnnotations>) -> bool {
    let destructive_hint = annotations.and_then(|annotations| annotations.destructive_hint);
    if destructive_hint == Some(true) {
        return true;
    }

    let read_only_hint = annotations
        .and_then(|annotations| annotations.read_only_hint)
        .unwrap_or(false);
    if read_only_hint {
        return false;
    }

    destructive_hint.unwrap_or(true)
        || annotations
            .and_then(|annotations| annotations.open_world_hint)
            .unwrap_or(true)
}
```

- **日本語**: destructive_hint が true なら承認必要。そうでなく read_only_hint が true なら承認不要。それ以外は、destructive_hint が無い（既定 true）か open_world_hint が無い／true なら承認必要。
- **どう使っているか**: Codex の auto モード（既定）での MCP ツール承認の判定式。(1) destructiveHint:true → 承認（readOnlyHint より優先）。(2) readOnlyHint:true → 承認なしで実行。(3) それ以外は destructiveHint:false かつ openWorldHint:false のときだけ承認なし。欠けた hint は MCP 仕様の既定（destructive=true, openWorld=true）で埋め、annotations が無ければ承認（安全側）。idempotentHint は使わない。
- **条件**: approval mode が auto（既定、36）のとき。次の場合はこの判定式を通らない：(a) strict auto-review が有効なときは annotation に関係なく毎回承認（レビュー）に回る（同ファイル 1512〜1527 行：if !strict_auto_review && !requires_mcp_tool_approval_for_mode(...)、tool で exact）。(b) approval mode が approve、または approval_policy=never かつ権限プロファイルが無効・外部・ディスク全体書き込み可のときは annotation を見ずに自動承認（37）。(c) 同じセッションで承認を記憶していれば確認なし（1536〜1541 行、目視）。prompt は常に承認、writes は readOnlyHint だけ（35）。app（コネクタ）と任意の MCP サーバーの両方に適用（approval_mode は app ならアプリ設定、それ以外は MCP サーバー設定から取る：同ファイル 215〜224 行、目視）。
- **扱う宣言**: destructiveHint・readOnlyHint・openWorldHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、2463-2480 行（取得 2026-10-02T22:11:37Z、sha256 ab767be40cb8…）
- **補足**: readOnlyHint:true と嘘の宣言をした書き込みツールは、auto モードでは確認なしで実行される（宣言が唯一の根拠）。ただしキャッシュされたカタログ由来のツールでは readOnlyHint が消される（43）。 conditions に strict auto-review（annotation で承認を省かない）と、セッション内の承認記憶の経路を足した（finder は approve / never の例外だけ）。1525 行を tool で exact 確認。

<a id="g-c05-openai-35"></a>
#### C05-35 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/core/src/mcp_tool_call.rs — requires_mcp_tool_approval_for_mode（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs#L2486-L2493
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 2486-2493
- **原文**:

```
    match approval_mode {
        AppToolApproval::Auto => requires_mcp_tool_approval(annotations),
        AppToolApproval::Prompt => true,
        AppToolApproval::Writes => !annotations
            .and_then(|annotations| annotations.read_only_hint)
            .unwrap_or(false),
        AppToolApproval::Approve => false,
    }
```

- **日本語**: モードごとの判定：Auto は annotation による判定式、Prompt は常に承認、Writes は readOnlyHint が true でなければ承認、Approve は承認しない。
- **どう使っているか**: 承認モード（auto / prompt / writes / approve）で annotation の使い方が変わる。writes は readOnlyHint だけを見る（destructiveHint:true でも readOnlyHint:true なら承認なし。テスト writes_mode_does_not_require_approval_for_read_only_tools で確認）。
- **条件**: モードは config.toml の default_tools_approval_mode / approval_mode（31）、app 設定、管理者の requirements で決まる。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う・確認を省く（自動で許可）・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、2486-2493 行（取得 2026-10-02T22:11:37Z、sha256 ab767be40cb8…）
- **補足**: Agent approvals & security（29）の『read annotation が優先』は writes モードの挙動とは一致する。

<a id="g-c05-openai-36"></a>
#### C05-36 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/config/src/mcp_types.rs — enum AppToolApproval（#[default] Auto）（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/config/src/mcp_types.rs#L28-L34
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/config/src/mcp_types.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 28-34
- **原文**:

```
pub enum AppToolApproval {
    #[default]
    Auto,
    Prompt,
    Writes,
    Approve,
}
```

- **日本語**: 承認モードの列挙。既定（#[default]）は Auto。ほかに Prompt、Writes、Approve。
- **どう使っているか**: 何も設定しなければ承認モードは Auto ＝ annotation による判定（34）が既定で効く。
- **条件**: MCP サーバー・ツールに approval_mode を設定していないとき（unwrap_or_default）。app（コネクタ）も設定が無ければ Auto（app_tool_policy.rs の unwrap_or(AppToolApproval::Auto)、目視）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い
- **確かさ**: [確認] 再照合 exact・1 か所、28-34 行（取得 2026-10-02T22:11:38Z、sha256 9e4f9013a9a9…）

<a id="g-c05-openai-37"></a>
#### C05-37 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/codex-mcp/src/mcp/mod.rs — mcp_permission_prompt_is_auto_approved（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/mcp/mod.rs#L96-L102
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/mcp/mod.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 96-102
- **原文**:

```
    if context.tool_approval_mode == Some(AppToolApproval::Approve) {
        return true;
    }

    if approval_policy != AskForApproval::Never {
        return false;
    }
```

- **日本語**: ツールの承認モードが Approve なら自動承認。approval_policy が Never でなければ自動承認しない（Never なら、権限プロファイルが無効・外部、またはディスク全体への書き込み権限があるときに自動承認：続く 104〜109 行）。
- **どう使っているか**: annotation の判定より前に評価される例外。approve モード、または approval_policy=never かつ full access のときは、宣言に関係なくすべての MCP 呼び出しが確認なしで通る。
- **条件**: maybe_request_mcp_tool_approval の冒頭で、strict auto-review でないときに評価（mcp_tool_call.rs 1500〜1522 行、目視）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 使わない・読まない
- **確かさ**: [確認] 再照合 exact・1 か所、96-102 行（取得 2026-10-02T22:11:36Z、sha256 a6778a6d2f2f…）

<a id="g-c05-openai-38"></a>
#### C05-38 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/core/src/mcp_tool_call_tests.rs — approval_required_when_destructive_even_if_read_only_true（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call_tests.rs#L392-L395
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call_tests.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 392-395
- **原文**:

```
fn approval_required_when_destructive_even_if_read_only_true() {
    let annotations = annotations(Some(true), Some(true), Some(true));
    assert_eq!(requires_mcp_tool_approval(Some(&annotations)), true);
}
```

- **日本語**: （テスト）readOnlyHint:true でも destructiveHint:true なら承認が必要。
- **どう使っているか**: auto モードでは destructiveHint:true が readOnlyHint:true より優先されることをテストで固定している（29 の文書と逆、30 と一致）。
- **条件**: auto モード（requires_mcp_tool_approval）。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、392-395 行（取得 2026-10-02T22:11:40Z、sha256 978c2f739703…）
- **補足**: annotations(read_only, destructive, open_world) の順の引数。

<a id="g-c05-openai-39"></a>
#### C05-39 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/core/src/mcp_tool_call_tests.rs — approval_required_when_annotations_are_absent（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call_tests.rs#L398-L400
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call_tests.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 398-400
- **原文**:

```
fn approval_required_when_annotations_are_absent() {
    assert_eq!(requires_mcp_tool_approval(/*annotations*/ None), true);
}
```

- **日本語**: （テスト）annotations が無ければ承認が必要。
- **どう使っているか**: 宣言が無いツールは承認対象（欠落時は安全側）。同ファイルの approval_not_required_when_read_only_and_other_hints_are_absent（403〜410 行、目視）では readOnlyHint:true だけで承認不要。
- **条件**: auto モード。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言が無いときの扱い・確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、398-400 行（取得 2026-10-02T22:11:40Z、sha256 978c2f739703…）

<a id="g-c05-openai-42"></a>
#### C05-42 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/core/src/tools/handlers/mcp.rs — supports_parallel_tool_calls（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/tools/handlers/mcp.rs#L148-L159
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/tools/handlers/mcp.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 148-159
- **原文**:

```
    fn supports_parallel_tool_calls(&self) -> bool {
        // Correctly implemented MCP servers should tolerate parallel calls to
        // tools that advertise themselves as read-only.
        self.tool_info.supports_parallel_tool_calls
            || self
                .tool_info
                .tool
                .annotations
                .as_ref()
                .and_then(|annotations| annotations.read_only_hint)
                .unwrap_or(false)
    }
```

- **日本語**: 正しく実装された MCP サーバーは、自分を読み取り専用と広告するツールへの並列呼び出しに耐えるはず。サーバーが並列呼び出しを許可しているか、ツールの readOnlyHint が true なら並列実行を許す。
- **どう使っているか**: readOnlyHint:true のツールは並列に呼ばれうる（承認とは別の使われ方）。宣言が嘘だと、書き込みツールが並列で走る。
- **条件**: Codex の全 MCP ツール。サーバー設定 supports_parallel_tool_calls でも有効になる。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: その他
- **確かさ**: [確認] 再照合 exact・1 か所、148-159 行（取得 2026-10-02T22:13:00Z、sha256 f52c5ea41ecd…）
- **補足**: 同ファイル 846〜870 行のテスト mcp_read_only_hint_supports_parallel_calls_without_server_opt_in / mcp_parallel_calls_require_read_only_hint_or_server_opt_in（目視）。

<a id="g-c05-openai-43"></a>
#### C05-43 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー）

- **資料**: codex-rs/codex-mcp/src/connection_manager/tool_catalog.rs — キャッシュ由来のツールの readOnlyHint を消す（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/connection_manager/tool_catalog.rs#L386-L390
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/connection_manager/tool_catalog.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 386-390
- **原文**:

```
                    if client.is_none()
                        && let Some(annotations) = tool.tool.annotations.as_mut()
                    {
                        annotations.read_only_hint = None;
                    }
```

- **日本語**: 準備完了のクライアントが無い（起動中でキャッシュのツール一覧を使う）とき、そのツールの read_only_hint を None にする。
- **どう使っているか**: 起動時キャッシュのカタログから出したツール（ready client が無いとき）では、モデルに見せるツール一覧で readOnlyHint を消す。ただし実際の呼び出しの準備（prepare_call_for_tool）では、ready client の現在のカタログから annotations を取り直す（同ファイル 469〜501 行。493〜494 行のコメント「taking schema, annotations, and approval metadata from the current catalog」、tool で exact）ので、この消去は承認判定（34）には効かない。並列実行の判定（42）のハンドラがどちらの tool_info から作られるかは追っていない（不明）。
- **条件**: MCP サーバーの起動が終わっていない、または catalog readiness で ready client が無いとき（同ファイル 340〜352 行、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 宣言が無いときの扱い・その他
- **確かさ**: [確認] 再照合 exact・1 か所、386-390 行（取得 2026-10-02T22:11:37Z、sha256 749ba9975ba5…）
- **補足**: destructiveHint / openWorldHint は消さない。消す理由はコードのコメントに無い（不明）。 finder の『その結果、承認判定（34）では read-only 扱いされず…古い宣言で確認が省かれるのを防ぐ』は誤り。呼び出し時は現在のカタログから annotations を取り直す（tool_catalog.rs 469〜501 行、コメントを tool で exact 確認）ので承認判定には効かない。並列実行への影響と消す目的は不明とした。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — App Server プロトコル

<a id="g-c05-openai-30"></a>
#### C05-30 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — App Server プロトコル

- **資料**: Codex App Server — Approvals > MCP tool-call approvals (apps)（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/app-server
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/app-server#mcp-tool-call-approvals-apps
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Codex App Server > Approvals > MCP tool-call approvals (apps) (#mcp-tool-call-approvals-apps)
- **原文**:

> Destructive tool annotations always trigger approval even when the tool also advertises less-privileged hints.

- **日本語**: 破壊的なツール annotation は、ツールがより弱い権限の hint を同時に広告していても、常に承認を発動する。
- **どう使っているか**: destructive の annotation は、より弱い権限の hint（readOnlyHint:true など）と同時でも、常に承認を発動する（コード 34・38 と一致）。副作用のある app ツール呼び出しでは、サーバーが tool/requestUserInput で Accept / Decline / Cancel の承認を求めることがある（may）。拒否・取り消しなら mcpToolCall はツールを実行せずエラーで終わる（同段落、tool で exact）。
- **条件**: Codex の app（コネクタ）ツール呼び出し、既定の auto モード。writes / approve モードや approval_policy=never（37）では成り立たない（コードより）。
- **扱う宣言**: destructiveHint・readOnlyHint ／ **使い方の分類**: 確認を求める
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Codex App Server > Approvals > MCP tool-call approvals (apps)」（取得 2026-10-02T22:11:30Z、sha256 8a542ad412c3…）
- **補足**: 29 の Agent approvals & security と矛盾。 usage_ja の『承認は tool/requestUserInput で…を出し』は原文が may（ことがある）なので直した。同段落の文を tool で確認した。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — MCP サーバー設定

<a id="g-c05-openai-31"></a>
#### C05-31 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — MCP サーバー設定

- **資料**: Model Context Protocol（Codex）— Configure with config.toml > Other configuration options（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/extend/mcp
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/extend/mcp#other-configuration-options
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Model Context Protocol > Use MCP-backed tools in ChatGPT web > Configure with config.toml > Other configuration options (#other-configuration-options)
- **原文**:

> Supported values are `auto`, `prompt`, `writes`, and `approve`. The `writes` mode prompts for tools that aren't marked read-only.

- **日本語**: （default_tools_approval_mode の）値は auto、prompt、writes、approve。writes モードは、読み取り専用と印の付いていないツールで確認を求める。
- **どう使っているか**: Codex の MCP サーバーごと / ツールごとの承認モード。writes は readOnlyHint だけで判定（読み取り専用の印があれば承認なし）。auto の中身はこのページには書かれていない（コード 34 で annotation による判定と確認）。
- **条件**: 利用者が config.toml の mcp_servers.<id>.default_tools_approval_mode / tools.<tool>.approval_mode を設定したとき。既定値は auto（コード 36）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 loose・1 か所、見出し「Model Context Protocol > Use MCP-backed tools in ChatGPT web > Configure with config.toml > Other configuration options」（取得 2026-10-02T22:11:26Z、sha256 d0635a44cc94…）
- **補足**: このページに readOnlyHint / destructiveHint の語は無い（checked_no_mention）。『marked read-only』が readOnlyHint を指すことはコード（35）で確認。tool の照合は loose。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）設定

<a id="g-c05-openai-32"></a>
#### C05-32 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）設定

- **資料**: Configuration Reference — config.toml（apps.<id>.destructive_enabled）（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/config-file/config-reference
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/config-file/config-reference#configtoml
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Configuration Reference > config.toml (#configtoml)
- **原文**:

> Allow or block tools in this app that advertise `destructive_hint = true`.

- **日本語**: （apps.<id>.destructive_enabled）この app の中で destructive_hint = true を広告するツールを許可するか遮断するか。
- **どう使っているか**: destructive_hint / open_world_hint の宣言で、app のツールを丸ごと使用禁止にできる設定（apps._default.* と apps.<id>.*）。宣言が利用者のポリシー規則の入力になる例。
- **条件**: Codex の apps（ChatGPT のコネクタ）だけ。任意の MCP サーバー（mcp_servers）には同じ設定は無い（コード 41 は CODEX_APPS サーバーにだけ適用）。ドキュメントは既定値を書いていない。コード（40、app_tool_policy.rs 221〜234 行）では未設定なら true（遮断しない）。hint が欠けたツールは true とみなされ、設定で遮断すると巻き込まれる（40）。ツール単位の enabled や app 単位の default_tools_enabled を指定すると、hint による遮断は評価されない（同関数 212〜218 行）。
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: ツールを絞る・隠す・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 loose・2 か所、見出し「Configuration Reference > config.toml」（取得 2026-10-02T22:11:57Z、sha256 398d8be0b243…）
- **補足**: count=2 は、同じキーが表と（狭い画面用の）カード表示の 2 回描かれているため（検証者が本文で確認）。同ページに「apps.<id>.open_world_enabled: Allow or block tools in this app that advertise open_world_hint = true.」「apps._default.destructive_enabled: Default allow/deny for app tools with destructive_hint = true.」がある（どちらも検証者が tool で exact、count=2）。apps._default.open_world_enabled も同様。 notes の『別のキーの重複と思われる』は誤り（同じキーの 2 回描画）。conditions の『既定は許可（true）』はドキュメントではなくコード由来なので出典を明記し、enabled 指定があると hint を見ない条件を足した。補足の 2 文を tool で確認した。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（承認をレビュー用エージェントに回す）

<a id="g-c05-openai-33"></a>
#### C05-33 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（承認をレビュー用エージェントに回す）

- **資料**: Auto-review — When it triggers（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/sandboxing/auto-review
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/sandboxing/auto-review#when-it-triggers
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Auto-review > When it triggers (#when-it-triggers)
- **原文**:

> MCP or app tool calls that require approval based on their tool annotations or configured approval mode.

- **日本語**: （auto-review の対象）ツール annotations または設定した承認モードにより承認が必要になる MCP / app ツール呼び出し。
- **どう使っているか**: annotation で承認が必要と判定された呼び出しは、approvals_reviewer=auto_review なら人ではなくレビュー用エージェントに回る。レビューの入力にも annotations（destructive / open_world / read_only の 3 つ）が渡る（コード 44）。
- **条件**: approvals_reviewer = "auto_review" のとき。auto-review は承認の担い手を替えるだけで権限を広げない（同ページ）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・危険度を付ける
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Auto-review > When it triggers」（取得 2026-10-02T22:11:29Z、sha256 496990febd1e…）

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）

<a id="g-c05-openai-40"></a>
#### C05-40 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）

- **資料**: codex-rs/connectors/src/app_tool_policy.rs — app ツールの有効判定（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/connectors/src/app_tool_policy.rs#L235-L238
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/connectors/src/app_tool_policy.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 235-238
- **原文**:

```
    let destructive_hint = input.destructive_hint.unwrap_or(true);
    let open_world_hint = input.open_world_hint.unwrap_or(true);
    let enabled =
        (destructive_enabled || !destructive_hint) && (open_world_enabled || !open_world_hint);
```

- **日本語**: destructive_hint と open_world_hint が無ければ true とみなす。destructive_enabled が false なら destructive なツールを、open_world_enabled が false なら open-world なツールを無効にする。
- **どう使っているか**: 利用者の destructive_enabled / open_world_enabled 設定（32）と宣言を組み合わせて app ツールを使用禁止にする。宣言が欠けたツールは destructive / open-world 扱い（安全側）。
- **条件**: Codex の apps（ChatGPT コネクタ、CODEX_APPS サーバー）だけ。既定は両設定とも true（遮断しない）。app 自体が無効なら無効、ツール単位・app 単位の enabled 指定があればそちらが優先（同関数 205〜218 行、目視）。
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: ツールを絞る・隠す・宣言が無いときの扱い・規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、235-238 行（取得 2026-10-02T22:12:05Z、sha256 a2fc8ab7b6fe…）

<a id="g-c05-openai-41"></a>
#### C05-41 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — apps（ChatGPT コネクタ）

- **資料**: codex-rs/core/src/mcp_tool_call.rs — app 設定で無効なツールの呼び出しを遮断（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs#L229
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/mcp_tool_call.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 229
- **原文**:

```
    if server == CODEX_APPS_MCP_SERVER_NAME && !app_tool_policy.enabled {
```

- **日本語**: サーバーが CODEX_APPS で、app ツールのポリシーが無効なら（呼び出しを飛ばす）。
- **どう使っているか**: 40 で無効になった app ツールは実行されず、「MCP tool call blocked by app configuration」というエラーで終わる（同ファイル 236 行、exact で照合済み：count=1, sha256=ab767be40cb8）。
- **条件**: CODEX_APPS サーバーのみ。
- **扱う宣言**: destructiveHint・openWorldHint ／ **使い方の分類**: ツールを絞る・隠す
- **確かさ**: [確認] 再照合 exact・1 か所、229 行（取得 2026-10-02T22:11:37Z、sha256 ab767be40cb8…）

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（guardian）

<a id="g-c05-openai-44"></a>
#### C05-44 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — Auto-review（guardian）

- **資料**: codex-rs/core/src/guardian/approval_request.rs — GuardianMcpAnnotations（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/guardian/approval_request.rs#L124-L131
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/core/src/guardian/approval_request.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 124-131
- **原文**:

```
pub(crate) struct GuardianMcpAnnotations {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub(crate) destructive_hint: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub(crate) open_world_hint: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub(crate) read_only_hint: Option<bool>,
}
```

- **日本語**: レビュー用エージェントに渡す MCP annotation の構造体：destructive_hint、open_world_hint、read_only_hint（無ければ省略）。
- **どう使っているか**: auto-review（33）では、承認要求の JSON に 3 つの hint を入れてレビュー用モデルに渡す（McpToolCallApprovalAction の annotations、同ファイル 197〜198 行・368〜380 行、目視）。宣言がモデルによるリスク判断の入力になる。idempotentHint と title は渡さない（title は tool_title として別に渡る）。
- **条件**: approvals_reviewer = auto_review のとき。
- **扱う宣言**: destructiveHint・openWorldHint・readOnlyHint ／ **使い方の分類**: 危険度を付ける・そのまま渡す・見せる
- **確かさ**: [確認] 再照合 exact・1 か所、124-131 行（取得 2026-10-02T22:11:34Z、sha256 6b1739073d32…）
- **補足**: レビュー用プロンプトで annotation をどう扱えと指示しているかは確認していない（不明）。

### OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — trusted access（サイバー用途の資格情報文脈）

<a id="g-c05-openai-45"></a>
#### C05-45 OpenAI — Codex（CLI / IDE / app。ChatGPT の apps＝コネクタと任意の MCP サーバー） — trusted access（サイバー用途の資格情報文脈）

- **資料**: codex-rs/codex-mcp/src/trusted_access.rs — add_trusted_access_context（クライアントのソースコード）
- **URL**: https://github.com/openai/codex/blob/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/trusted_access.rs#L55-L61
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/codex/ca466061d64f0b44f416135c7fd06aa7af850bbc/codex-rs/codex-mcp/src/trusted_access.rs
- **版**: commit ca466061d64f0b44f416135c7fd06aa7af850bbc
- **書いてある場所**: lines 55-61
- **原文**:

```
            && matches!(server.origin, Some(McpServerOrigin::Stdio))
            && tool
                .tool
                .annotations
                .as_ref()
                .and_then(|annotations| annotations.read_only_hint)
                == Some(true)
```

- **日本語**: サーバーの起点が stdio で、かつツールの read_only_hint が Some(true) のとき（だけ trusted access の文脈を付ける）。
- **どう使っているか**: cyber trusted access の entitlement を要求するツールに検証済みアクセス情報を付けるのは、ローカル stdio・plugin 由来・引数なし・readOnlyHint:true の条件をすべて満たすときだけ。宣言が機微な文脈を渡す条件の 1 つになっている。
- **条件**: plugin が提供するローカル stdio サーバーで、_meta に該当 entitlement を要求するツールのみ（38〜62 行、目視）。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 規則（ポリシー）の条件に使う
- **確かさ**: [確認] 再照合 exact・1 か所、55-61 行（取得 2026-10-02T22:11:44Z、sha256 9349f480faa0…）
- **補足**: ニッチな経路。readOnlyHint:true が嘘だと、書き込みツールにこの文脈が渡りうる。

### OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill（申請 JSON を作る Codex 用 skill）

<a id="g-c05-openai-46"></a>
#### C05-46 OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill（申請 JSON を作る Codex 用 skill）

- **資料**: chatgpt-app-submission/SKILL.md — Hint Rules（公式の文書）
- **URL**: https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md#L40
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/plugins/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md
- **版**: commit 5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f（2026-10-02 の HEAD）
- **書いてある場所**: lines 40（直前の見出し: ## Hint Rules）
- **原文**:

> ChatGPT Apps submissions require every tool to set all three hints explicitly. Missing or null hints are submission blockers, even if MCP clients may have protocol-level defaults.

- **日本語**: ChatGPT Apps の申請では、すべてのツールが 3 つの hint をすべて明示的に設定する必要がある。hint が欠けている・null なのは申請を止める問題で、MCP クライアントにプロトコル上の既定値があっても同じ。
- **どう使っているか**: MCP 仕様の既定値（欠落時の解釈）に頼ることを申請では認めない。この skill は欠落・null を見つけたら JSON 生成を止める。
- **条件**: ChatGPT Apps / plugin の申請 JSON を生成するとき。
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint ／ **使い方の分類**: 宣言を書くことを求める・宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、40 行（## Hint Rules）（取得 2026-10-02T22:11:45Z、sha256 c9b43ca8fe60…）
- **補足**: 同ファイル 42 行：hint が欠けている・実装と合わないときは、開発者の承認を得てからソースの hint を直す（目視）。

### OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill

<a id="g-c05-openai-47"></a>
#### C05-47 OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill

- **資料**: chatgpt-app-submission/SKILL.md — Workflow 5（公式の文書）
- **URL**: https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md#L16
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/plugins/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md
- **版**: commit 5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f
- **書いてある場所**: lines 16（直前の見出し: ## Workflow）
- **原文**:

> Compare tool annotations, tool names, tool descriptions, and CSP values against actual behavior. If any value is missing, stale, misleading, or inconsistent, ask the developer for approval before updating source.

- **日本語**: ツールの annotations・名前・説明・CSP の値を実際の振る舞いと比べる。欠けている・古い・誤解を招く・矛盾する値があれば、ソースを更新する前に開発者の承認を求める。
- **どう使っているか**: OpenAI が配布する申請用 skill が、開発者の手元の Codex（LLM エージェント）に、宣言（annotations）と実装の振る舞いをソースを読んで照合させる。AuthGap の静的照合と同じ問題設定の、OpenAI 公式の実践例。OpenAI 自身の審査がこの方法で行われるとは書かれていない。同じ skill は審査向けの『tool hint justifications』も生成する（17 行、tool で exact）。
- **条件**: 開発者が Codex でこの skill を使ったとき。判定は LLM のコード読解で、規則化された静的解析ではない。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する
- **確かさ**: [確認] 再照合 exact・1 か所、16 行（## Workflow）（取得 2026-10-02T22:11:45Z、sha256 c9b43ca8fe60…）
- **補足**: Workflow 3〜4（14〜15 行、目視）：宣言された readOnlyHint / openWorldHint / destructiveHint を全ツールで集め、各ツールの実装と呼び出す補助関数を読んで副作用を把握する。 usage_ja の『OpenAI 自身が…照合を行わせている』は、OpenAI 側の審査の方法と誤読されうるので、開発者の手元で動く skill だと明記した。17 行の justification 生成を tool で確認して足した（05・10 の justification の矛盾に関係する）。

<a id="g-c05-openai-48"></a>
#### C05-48 OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill

- **資料**: chatgpt-app-submission/SKILL.md — Workflow（名前から推測しない）（公式の文書）
- **URL**: https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md#L21
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/plugins/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md
- **版**: commit 5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f
- **書いてある場所**: lines 21（直前の見出し: ## Workflow）
- **原文**:

> Do not infer behavior from the tool name alone. Use the real tool implementation and declared annotations. If a tool calls into another module or API client, inspect enough of that path to know whether it reads, writes, deletes, sends, publishes, or changes external state.

- **日本語**: ツール名だけから振る舞いを推測しない。実際のツール実装と宣言された annotations を使う。ツールが別のモジュールや API クライアントを呼ぶなら、読み取り・書き込み・削除・送信・公開・外部状態の変更のどれをするか分かるところまでその経路を調べる。
- **どう使っているか**: 宣言の正しさは名前ではなく実装（呼び出し先まで）で判断せよ、という照合の方法論。
- **条件**: 同上。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 宣言を検査する・作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、21 行（## Workflow）（取得 2026-10-02T22:11:45Z、sha256 c9b43ca8fe60…）

<a id="g-c05-openai-49"></a>
#### C05-49 OpenAI — OpenAI plugins リポジトリ — chatgpt-app-submission skill

- **資料**: chatgpt-app-submission/SKILL.md — Hint Rules（openWorldHint）（公式の文書）
- **URL**: https://github.com/openai/plugins/blob/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md#L38
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/plugins/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/openai-developers/skills/chatgpt-app-submission/SKILL.md
- **版**: commit 5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f
- **書いてある場所**: lines 38（直前の見出し: ## Hint Rules）
- **原文**:

> `openWorldHint`: `true` if the tool can change publicly visible internet state or external third-party systems, such as sending emails or messages, posting/publishing content, creating public tickets/issues, pushing code/content, or submitting external forms. `false` if it only operates in closed/private systems.

- **日本語**: openWorldHint：メールやメッセージの送信、コンテンツの投稿・公開、公開チケットや issue の作成、コードやコンテンツの push、外部フォームの送信など、公開されたインターネットの状態や外部の第三者システムを変更しうるなら true。閉じた・私的なシステムの中だけで動くなら false。
- **どう使っているか**: openWorldHint を『外部状態を変えうるか』で定義している。developers.openai.com の文書（13, 15、Reference）は『公開インターネット・不特定の外部主体にアクセスするか（読み取りの Web 検索も true）』で定義しており、同じ OpenAI の中で定義が違う。
- **条件**: 同上。
- **扱う宣言**: openWorldHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、38 行（## Hint Rules）（取得 2026-10-02T22:11:45Z、sha256 c9b43ca8fe60…）
- **補足**: 同ファイル 34 行は「Use the Apps SDK review meanings:」（tool で exact）で、この定義を審査の意味として示しているが、現在の app-review の却下理由（13 の notes）は openWorldHint を『公開インターネットや不特定の外部主体にアクセスするか（読み取りの Web 検索も true）』で定義しており合わない。skill の定義が古い可能性がある（不明）。同ファイル 36〜37 行に readOnlyHint / destructiveHint の基準（目視）。openai/skills の chatgpt-apps skill（50）は idempotentHint にも触れる。 34 行の「Use the Apps SDK review meanings:」を tool で確認し、skill が自分の定義を審査の意味だとしているのに現行の審査文書と食い違う点を notes に足した。

### OpenAI — openai/skills — chatgpt-apps skill（.curated）

<a id="g-c05-openai-50"></a>
#### C05-50 OpenAI — openai/skills — chatgpt-apps skill（.curated）

- **資料**: skills/.curated/chatgpt-apps/SKILL.md — 1. Plan Tools Before Code（公式の文書）
- **URL**: https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/chatgpt-apps/SKILL.md#L129
- **照らし合わせた中身の URL**: https://raw.githubusercontent.com/openai/skills/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/chatgpt-apps/SKILL.md
- **版**: commit 49f948faa9258a0c61caceaf225e179651397431（2026-10-02 の HEAD）
- **書いてある場所**: lines 129（直前の見出し: ### 1. Plan Tools Before Code）
- **原文**:

> Set annotations accurately (`readOnlyHint`, `destructiveHint`, `openWorldHint`; add `idempotentHint` when true).

- **日本語**: annotations を正確に付ける（readOnlyHint、destructiveHint、openWorldHint。idempotentHint は true のときに加える）。
- **どう使っているか**: ChatGPT アプリを作る Codex skill の著者向け指示。idempotentHint は任意（true のときだけ）。
- **条件**: —
- **扱う宣言**: readOnlyHint・destructiveHint・openWorldHint・idempotentHint ／ **使い方の分類**: 作者への書き方の案内
- **確かさ**: [確認] 再照合 exact・1 か所、129 行（### 1. Plan Tools Before Code）（取得 2026-10-02T22:11:38Z、sha256 c3a13a659ce2…）
- **補足**: openai/plugins の plugins/openai-developers/skills/build-chatgpt-app/SKILL.md（commit 5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f）の 129 行にも同じ文がある（検証者が verify_quote.py で exact、count=1、sha256=b4ba5e0847e9、見出し ### 1. Plan Tools Before Code）。 notes の『GitHub code search の結果。tool では未照合』を、raw.githubusercontent.com の固定 commit で照合して exact を得たので書き換えた。

### OpenAI — ChatGPT / Codex の内蔵ブラウザ — Site tools（WebMCP）

<a id="g-c05-openai-51"></a>
#### C05-51 OpenAI — ChatGPT / Codex の内蔵ブラウザ — Site tools（WebMCP）

- **資料**: Site tools — Security and user controls（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/webmcp
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/webmcp#security-and-user-controls
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Site tools > Security and user controls (#security-and-user-controls)
- **原文**:

> Website-provided tool definitions and results are untrusted content. A tool's name or claim that it only reads data isn't proof of what it does.

- **日本語**: Web サイトが提供するツール定義と結果は信頼できない内容である。ツールの名前や『データを読むだけ』という主張は、それが実際に何をするかの証明にならない。
- **どう使っているか**: WebMCP（ページが document.modelContext.registerTool で登録するツール）について、読み取り専用の主張を信用しないと明言。同じページの登録例は annotations: { readOnlyHint: true } を使っている。
- **条件**: 内蔵ブラウザの Site tools（WebMCP）。MCP サーバーの annotations ではないが、同じ readOnlyHint を使う。
- **扱う宣言**: readOnlyHint ／ **使い方の分類**: 信頼するなという注意
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Site tools > Security and user controls」（取得 2026-10-02T22:11:33Z、sha256 3cfa320274ef…）

<a id="g-c05-openai-52"></a>
#### C05-52 OpenAI — ChatGPT / Codex の内蔵ブラウザ — Site tools（WebMCP）

- **資料**: Site tools — Security and user controls（安全レビュー）（クライアントの文書）
- **URL**: https://learn.chatgpt.com/docs/webmcp
- **書いてある見出しへ直接**: https://learn.chatgpt.com/docs/webmcp#security-and-user-controls
- **版**: 2026-10-02 取得（版表示なし）
- **書いてある場所**: Site tools > Security and user controls (#security-and-user-controls)
- **原文**:

> In the built-in browser, each tool invocation receives a safety review before it runs. Normal website-access and confirmation policies still apply, including for consequential actions such as sending messages, making purchases, deleting data, or changing permissions.

- **日本語**: 内蔵ブラウザでは、ツールの各呼び出しが実行前に安全レビューを受ける。メッセージ送信、購入、データ削除、権限変更のような重大な操作を含め、通常の Web サイトアクセスと確認のポリシーが引き続き適用される。
- **どう使っているか**: WebMCP ツールは、宣言に関係なく呼び出しごとに実行前の安全レビューを受け、重大な操作では通常の確認ポリシーが効く。宣言（readOnlyHint）でレビューや確認が省かれるとは書かれていない。安全レビューが annotation を入力に使うかは書かれていない（不明）。
- **条件**: 内蔵ブラウザ。レビューが annotation を入力に使うかは書かれていない（不明）。
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を求める・その他
- **確かさ**: [確認] 再照合 exact・1 か所、見出し「Site tools > Security and user controls」（取得 2026-10-02T22:11:33Z、sha256 3cfa320274ef…）
- **補足**: usage から risk_scoring を外した（安全レビューが annotation を入力にするかは書かれていない。finder 自身も conditions で不明としていた）。

### OpenAI — ChatGPT（apps / コネクタの App permissions）

<a id="g-c05-openai-53"></a>
#### C05-53 OpenAI — ChatGPT（apps / コネクタの App permissions）

- **資料**: Managing app permissions in ChatGPT（OpenAI Help Center 20001495）（クライアントの文書）
- **URL**: https://help.openai.com/en/articles/20001495-managing-app-permissions-in-chatgpt
- **版**: 未取得
- **書いてある場所**: 不明（本文を取得できず）
- **原文**:

> Managing app permissions in ChatGPT

- **日本語**: （記事タイトルのみ）ChatGPT でのアプリ権限の管理
- **どう使っているか**: WebSearch の要約によれば、権限の選択肢に Always ask / Allow read actions / Allow low-risk actions / Allow all actions、既定の Important actions（読み取りは自動、外部に意味のある影響・機微情報の露出・取り消し困難な操作は確認）がある。読み取りかどうかの判定に readOnlyHint を使うかは不明。
- **条件**: 不明
- **扱う宣言**: 宣言全般 ／ **使い方の分類**: 確認を省く（自動で許可）・確認を求める
- **確かさ**: [未確認] verify_quote.py（検証者が新しいキャッシュ vqcache_verify で再実行）: match=fetch_failed status=403 fetched_at=2026-10-02T17:01:14Z（finder と同じく取得できず）
- **補足**: learn.chatgpt.com の「Manage ChatGPT Space and shared pages」ページが、いつ確認を求めるかを決める approval settings の説明としてこの記事にリンクしている（llms-full.txt で目視）。 【検証者】2026-10-02T17:08Z に再試行したが同じく HTTP 403（cf-mitigated: challenge）。 再試行して取得できないことを確認（未確認のまま）。

---

[← 付録 G-4 Anthropic](appendix-g-4.md) ｜ [付録 G の表紙](appendix-g.md) ｜ [目次](README.md) ｜ [付録 G-6 Google と AWS →](appendix-g-6.md)
