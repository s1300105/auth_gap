### 第 16 章

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
v4 の実物は `evidence/scan_v2_v4_run1/` の manifest と `contradictions.json` で確かめました。v4 の数字は論文に使いません（D66 の 5）。
「対象になりうるか」などの答えは、手順書と手引きの下書き（未承認）の規則に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

#### 演習 16-1（manifest の `D_kind` を読む）

**(1) 当たる宣言**

- (ア) ccr の `gcc_todo_delete`: **D4 だけ**。
  - `explicit` が空なので、D1（`explicit` の `readOnlyHint`）も D2（`explicit` の `destructiveHint`）も当たりません。`destructiveHint: true` と正直に書いているので、D2 の約束はしていません。
  - `closed_world` の欄が無い（= false）ので、D3 も当たりません。
  - `idempotent: true` が立っているので、D4 が当たります。`readOnlyHint` は明示の `false` で、`true` ではないので、D4 の条件を満たします。
- (イ) gemini の `gemini_list_models`: **D1 と D3**。
  - `explicit` に `readOnlyHint` があるので D1。
  - D1 があるので D2・D4 は当てません（`destructiveHint: false` と `idempotentHint: true` は `present_no_bound` に入り、`idempotent` も立っていません）。
  - `closed_world: true` なので D3。D3 は D1 と一緒でも当てます。

**(2) 道具の「明示された宣言:」の行**

- (ア): `[]`（空）。
- (イ): `['readOnlyHint']`。D3 は出ません。

どちらも、D3・D4 が「明示された宣言:」の行に出ない例です。D3・D4 は、manifest の `D_kind` の `closed_world`・`idempotent` か、「宣言:」の行（`annotations`）と原ソースから確かめます。

**(3) 矛盾していない理由**

`D_explicit` は `D_kind.explicit` の写しで、「上界を動かす明示」と `openWorldHint: true` の名前しか入りません。
D4（`idempotentHint: true`）は決して `explicit` に入らず、`idempotent` の欄に表れます。
どの宣言の組かは、`declarations` の欄（ここでは `["D4"]`）に書かれます。
ですから、「`D_explicit` が空」と「D4 の矛がある」は両立します。
この矛は、道筋 `_ensure_memory -> _init -> InitMixin.ensure_structure -> FileIOMixin._add_to_gitignore` の先の `open(..., 'a')`（`ccr/core/memory_pkg/memory_file_io.py:83`）で、理由は `fs_append` でした。

**(4) 見落としの抜き取りの対象**

- (ア): **対象になりません。** `explicit` に `readOnlyHint` も `destructiveHint` も無いからです（D1 も D2 も明示していない）。D4 だけのユニットは、見落としの抜き取りの対象外です。
- (イ): **対象になりえます。** `explicit` に `readOnlyHint` があり（D1 を明示）、行の注記に `contradiction` で始まるものが無い（D1 への矛が無い）からです。実際に抜き取られるかは、seed（乱数の種）を決めた抜き取りで決まります（第 47 章）。

#### 演習 16-2（`annotations` から `D_kind` を作る）

作例（`t_a`・`t_b`・`t_c`）を走査した結果と一致することを確かめてあります。

| | (1) `explicit` | (1) `present_no_bound` | (2) ほかの欄 | (3) 当たる宣言 |
|---|---|---|---|---|
| (ア) | `["destructiveHint"]` | `["idempotentHint", "readOnlyHint"]` | `upper` = `DB`・`FS_READ`・`FS_WRITE`・`NET`、`bottom: false`、`idempotent: true` | **D2・D4** |
| (イ) | `["readOnlyHint"]` | `["openWorldHint", "title"]` | `upper` = `FS_READ`・`NET`、`bottom: false`、`closed_world: true` | **D1・D3** |
| (ウ) | `["openWorldHint"]` | `["destructiveHint"]` | `bottom: true`（`upper` なし）、`open_world: true` | **なし** |

- (ア): `readOnlyHint: False` は `True` でないので `present_no_bound`。`readOnlyHint: True` が無いので、`destructiveHint: False` は `explicit` に入り（D2）、`idempotentHint: True` で `idempotent` が立ちます（D4）。
- (イ): `readOnlyHint: True` は `explicit`（D1）。`openWorldHint: False` は `present_no_bound` に入り、`closed_world` が立ちます（D3）。`title` は `present_no_bound`。
- (ウ): `destructiveHint: True` は約束しない側の値なので `present_no_bound`。`openWorldHint: True` は `explicit` に入りますが、上界は動かさず、D1〜D4 のどれでもありません。上界が無いので `bottom: true`。

**(4) 予想と、作例の結果**

- (ア) `os.remove(path)`: **D2 の矛**（理由 `fs_remove`）。消すのは壊す変更です。D4 では内（消した後にもう一度消しても状態は同じ）なので、D4 の行は出ません。作例 `t_a` の結果と一致しました。
- (イ) 定数の外部ホストへの `requests.get`: **D3 の矛**（理由 `net_external_host`）。外と関わらないと約束したのに、外部のホストと通信しています。D1 では、GET で読むだけの通信は内なので、D1 の行は出ません。作例 `t_b` の結果と一致しました（slot `url.host` などの行に `contradiction:D3`）。
- (ウ) `os.remove(path)`: **矛は出ません。** 当たる宣言が無いからです。作例 `t_c` には `contradiction` の注記が 1 つもありませんでした。

#### 演習 16-3（`r_malformed` の主の分母）

| | `annotation_form` | 主の分母 | 理由 |
|---|---|---|---|
| (a) | `ToolAnnotations` | **入る** | §2.11 の 3 つの値の 1 つ |
| (b) | （欄なし） | 入らない | `annotations=` を書いていない。snake_case の誤りは起こりえない |
| (c) | `unreadable` | **入る** | 変数で渡した形は `unreadable`。中身は読めないが、注釈を書いたことは確かで、§2.11 は `unreadable` を主の分母に入れている |
| (d) | `dict` | **入る** | 辞書で書いた形。キーが snake_case でも、形は `dict` |
| (e) | `absent` | 入らない | 「宣言は無い」と明示した形。§2.11 の 3 つの値に入っていない |
| (f) | `unpack` | 入らない | §2.11 の一覧にもスクリプトの `ANNOTATED_FORMS` にも `unpack` が無い（意図か書き落としかは原典に書かれていない。本文 16.9 節） |

主の分母に入るのは **(a)・(c)・(d)** です。

**(2) (d) は分子に入るか**

- 版が 2.0 以上（`ge2`）: **入りません。** `read_only_hint` は `readOnlyHint` に写されて宣言として読まれ（D1）、`malformed` は空です。
- 版が 2.0 より前（`lt2`）: **入ります。** `D_kind.malformed` に `read_only_hint` が入ります。
- 版が決まらない（`unknown`）: **入りません。** `undetermined_fields` に入り、`D_kind.unknown: true` になります。分子ではなく、「版が決まらない snake_case」の件数（併記）に数えられます。

#### 演習 16-4（snake_case と版を予想する）

作例の 3 つの木を走査し、その manifest を 1 つのディレクトリにまとめて `scripts/r_malformed.py` を当てた結果と一致することを確かめてあります。

**(1) 版**

- 木 A: **`lt2`**。根拠は `lt2:spec:requirements.txt:fastmcp>=2.10,<3`。`from fastmcp import FastMCP` は import の印の表に無いので、依存の記載で決まります。`fastmcp` の指定の上限（`<3`）が 4 より前なので、2.0 より前の印です。
- 木 B: **`ge2`**。根拠は `ge2:import:server.py:mcp.server.mcpserver`。
- 木 C: **`unknown`**。根拠に `ge2:import:server.py:mcp.server.mcpserver` と `lt2:import:server.py:mcp.server.fastmcp` の両方があり、両方の向きの印があるので決めません。

**(2) ユニットごと**

| ユニット | `annotations` | `D_kind` の主な欄 | D1 の矛 |
|---|---|---|---|
| 木 A `clean` | `{}` | `bottom: true`、`explicit: []`、`malformed: ["read_only_hint"]` | 出ない |
| 木 A `clean2` | `{"readOnlyHint": false}` | `bottom: true`、`explicit: []`、`present_no_bound: ["readOnlyHint"]`、`malformed: ["read_only_hint"]` | 出ない |
| 木 B `clean` | `{"readOnlyHint": true}` | `bottom: false`、`explicit: ["readOnlyHint"]`、`upper` = `FS_READ`・`NET` | **出る**（`fs_write`） |
| 木 C `clean` | `{}` | `bottom: true`、`explicit: []`、`unknown: true`（`undetermined_fields: ["read_only_hint"]`） | 出ない |

木 A の `clean2` では、camelCase の `readOnlyHint: False` が残り、snake_case の `read_only_hint` は `malformed` に入ります。1.x では snake_case が無視されるので、届く宣言は `readOnlyHint: false` だけです。

**(3) `r_malformed.py` の出力**

| 欄 | 値 | 理由 |
|---|---|---|
| `n_units` | 4 | 木 A の 2、木 B の 1、木 C の 1 |
| `n_annotated_units` | 4 | どれも `annotation_form` が `dict` |
| `n_malformed_units` | 2 | 木 A の 2 つ |
| `r_malformed_annotated` | 0.5 | 2 / 4 |
| `n_trees_malformed` | 1 | 木 A だけ |
| `n_undetermined_units` | 1 | 木 C の `clean` |
| `n_trees_undetermined` | 1 | 木 C だけ |

（全ユニットでの率 `r_malformed_all_units` も 0.5、`n_trees` は 3 でした。）

**(4) 木 B が実際には 1.x で動いていたら**

1.x では `read_only_hint` はクライアントに届きません。
けれども解析器は、木 B を `ge2` と判定して D1 として読み、`os.remove` に D1 の矛を出しています。
つまり、クライアントが受け取っていない約束を「破った」と数えることになり、**誤警報の向き**の誤りです。
（逆に、2.x で動く木を `lt2` と読み違えると、届いている約束が照合されず、あるはずの矛が消える**誤 clear の向き**の誤りになります。）

#### 確認問題 16-1

**D1 だけ**として扱われます。

- SDK の説明文は、`destructiveHint` について「この項目は `readOnlyHint` が false のときだけ意味を持つ」と書いています。読むだけのツールに「壊すか」を問う意味は無く、D1 の判定表が書き込み全般をすでに見ています。
- `D_kind` では、`readOnlyHint: True` があると、`destructiveHint: False` は `explicit` に入らず `present_no_bound` に入ります。D2 は `explicit` の `destructiveHint` で当てるので、当たりません。上界も `readOnlyHint: true` の `{FS_READ, NET}` だけです。
- 実物では、gemini の `gemini_prompt`・`gemini_list_models` と bugasura の `bugasura_find_project_by_name` がこの形で、どれも D2 は当たっていません。

#### 確認問題 16-2

**D3 は当たりません**（`explicit` だけからは、当たるとは言えません）。
`explicit` の `openWorldHint` は、`openWorldHint: true`（外の世界と関わる）を明示したことを表します。D3（`openWorldHint: false`）とは逆の申告です。
D3 が当たるかどうかは、`D_kind` の **`closed_world`** の欄で分かります。`closed_world: true` があれば D3 が当たり、欄が無ければ（false なら）当たりません。
このツールは `explicit` に `openWorldHint` があるので `openWorldHint: true` で、`closed_world` は立ちえません。当たる宣言は D1 だけです（bugasura の `bugasura_find_project_by_name`・gemini の `gemini_prompt` と同じ形）。

#### 確認問題 16-3

- **探索的にしていた理由**（D56）: D3・D4 の規則は、開発用のデータ（v2）の結果（run11 の件数）を見た後で作りました。結果を見て作った規則で同じデータを測ると、甘い結果になりうるので、D1・D2 と分けて「探索的」としました。
- **理由が無くなったわけ**（D62）: D60 で、論文の評価は学生が v2・v3 を含まない新しいデータで行うと決まりました。D3・D4 の規則も解析器の凍結に入り、評価のデータを見る前に固定されています。新しいデータから見れば、D1〜D4 の規則はどれも「見る前に決まっている」ので、「先に決めたか」の差がありません。「結果を見た後に作った」は、別の新しいデータで確かめれば解消する事情で、主と副を分ける理由にはなりません。
- **変えなかったもの**: 判定表（§7.3・§7.4）の規則、件数、古い記録（D56、逸脱 #19、run13〜run20 の表の「探索的」の語）、仕様書。変えたのは呼び方（位置づけ）と、集計の見出し・説明文の語、添削の範囲（D3・D4 の判定を探す回を足した）だけです。逸脱 #24 として記録されています。

#### 確認問題 16-4

- **未決の理由**: D70 の 4 と手順書は、M_d を「宣言 d を明示した（`D_kind.explicit`）ユニットを 1 つ以上持つ木」と書いています。D1・D2 はこれで正しく数えられますが、D3 は `closed_world`、D4 は `idempotent` の欄に表れ、`explicit` には入りません。D3・D4 をどの欄で数えるかを、どの文書も決めていません。
- **文字どおりに数えると**:
  - D3: `explicit` の `openWorldHint` は `openWorldHint: true` なので、**D3 とは逆の申告をした木**を数えてしまいます。v4 では、文字どおりの数え方で 39 木、本当の D3（`closed_world` を持つ木）で 40 木と数は近いのに、重なりは 22 木だけでした。
  - D4: `idempotentHint` は決して `explicit` に入らないので、**M_d がいつも 0** になり、割合が計算できません（v4 でも 0 木。`idempotent` を持つ木は 23）。
- **封の前に決める理由**: 分母を結果を見てから選べると、都合のよい割合が出る数え方を選べてしまいます。この研究は分母を値を見る前に決めて書き残す約束をしています（CLAUDE.md の規則 3、事前登録 §2.10 の「値を見てから主分母を替えない」）。また、決まらないまま集計すると、文字どおりに数えて意味の無い値を出すか、事前登録に無い数え方を黙って使うかのどちらかになります。どちらも避けるため、未決として記録し（第 46 章の一覧）、封の前に学生が決めます。
