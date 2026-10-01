### 第 12 章

#### 演習 12-1（登録の形を見分ける）

本書の執筆時に、この作例（`pkg/notes.py` には `export_note`（4 行）・`read_note`（10 行）・`save`（15 行）・`tool_a`（21 行）・`tool_b`（26 行）を定義）を凍結版と同じ版の解析器にかけ、下の答えと一致することを確かめました。

| 関数 | ユニットか | qualname / tool_name | relpath:lineno | annotation_form と宣言 | registration |
|---|---|---|---|---|---|
| `export_note` | なる（呼び出しの形） | `export_note` / `export_note` | `pkg/notes.py:4` | `dict`、`destructiveHint: false`（D2） | `call`、`pkg/server.py:9` |
| `read_note` | なる（`add_tool`） | `read_note` / `read_note` | `pkg/notes.py:10` | `ToolAnnotations`、`readOnlyHint: true`（D1） | `call`、`pkg/server.py:10` |
| `save` | なる（**1 つだけ**） | `save` / `save` | `pkg/notes.py:15` | `dict`、`destructiveHint: true` | `call`、`pkg/server.py:11` |
| `tool_a`・`tool_b` | **ならない** | — | — | — | — |
| `show` | なる | `show` / `show` | `pkg/server.py:19` | `unreadable`（宣言は読めない） | なし |
| `ping` | なる | `ping` / `ping` | `pkg/server.py:24` | `absent`（`annotations=None`） | なし |
| `cleanup` | なる（入れ子） | `register.cleanup` / `toy_cleanup` | `pkg/server.py:30` | `dict`、`readOnlyHint: true`（D1） | なし |
| `register` | ならない | — | — | — | — |

解説:

- **`export_note`・`read_note`**: 呼び出しの形の登録（U40）なので、`relpath:lineno` は関数の定義（`notes.py`）、`registration` は登録の行（`server.py`）を指します。宣言は登録の行に書かれています。解析器は `export_note` の `open(path, "w")`（`notes.py:5`）を D2 の矛（理由 `fs_writeout_model_path`。書き先をモデルが決める書き出し）にしました。
- **`save`**: 同じ関数が 11 行と 12 行で 2 度登録されていますが、ユニットは 1 つです。宣言は 11 行の `destructiveHint: true` だけが残り、12 行の `save_preview`（`readOnlyHint: true`）の宣言は捨てられます。`save_preview` は「読むだけ」と宣言しながら `open(path, "w")` で書くので、本当は D1 に反しますが、矛は出ません。O42 の「U40 R7」として記録された、誤 clear の向きの限界です。
- **`tool_a`・`tool_b`**: ループ変数 `f` を通した登録は、`f` が何を指すかを厳密に解けないので採りません（O42、数え落とし）。この 2 つはどの判定の抜き取りにも入りません。
- **`show`**: `annotations=READ_ONLY` は変数なので、解析器は中身を読めず `unreadable` にします。宣言は照合されません（`READ_ONLY` の中身は `readOnlyHint=True` ですが）。
- **`ping`**: `annotations=None` は「宣言は無い」と読める明示なので `absent` です。
- **`cleanup`**: `register` の中の入れ子の定義なので、qualname は `register.cleanup`。`name=` があるので `tool_name` は `toy_cleanup`。`os.remove(path)`（32 行）は D1 の矛（理由 `fs_write`）になりました。

#### 演習 12-2（qualname で見つからないとき）

1. **見つからなかった理由**: このツールの関数 `dependency_graph` は、`register` という関数の**中**に定義されています（入れ子の定義）。だから manifest の qualname は `register.dependency_graph` で、`"dependency_graph"` という完全一致の検索には当たりません。
2. **探し方**:
   1. 判定表の行から `tree`・`unit_relpath`・`unit_lineno` を読む（`v4-ei-nakamura__rails-lens`、`src/rails_lens/tools/dependency_graph.py`、183）。
   2. manifest（v4 なら `evidence/scan_v2_v4_run1/v4-ei-nakamura__rails-lens.json`、最終評価なら `evidence/scan_v2_final_run1/<木>.json`）の `units` から、`unit.relpath` と `unit.lineno` が**両方**一致するものを選ぶ（12.10 節の道具か、手順書 6.5 節の道具）。
   3. 見つかったユニットの qualname が `register.dependency_graph`、`tool_name` が `rails_lens_dependency_graph` であることを確かめる。
   4. 原ソース `corpus/v4-ei-nakamura__rails-lens/src/rails_lens/tools/dependency_graph.py` の 183 行（`def` の行）と、その上の宣言（174〜182 行）を開く。
   5. それでも見つからなければ、relpath の書き方（`corpus/...` を付けていないか、区切りが `/` か）、行番号が `def` の行か、正しい manifest を開いているか、木の打ち切り（`truncations`・`summary.json`）を確かめる。
3. **2 つ見つかったとき**: 判定表の `unit_relpath` と `unit_lineno` で選びます。mcp-atlassian なら、`src/mcp_atlassian/servers/jira.py:1232`（Jira）と `src/mcp_atlassian/servers/confluence.py:671`（Confluence）のどちらかです。qualname が同じでも、ファイルが違えば別のツールです（`mount` の `prefix` で、クライアントからは `jira_…` と `confluence_…` に分かれる）。
4. **qualname だけで探してはいけない理由**: 別のファイルに同じ qualname のツールがありうるからです（v4 の 88 木のうち 16 木）。qualname だけで探すと、片方の判定にもう片方のコードを読んでしまいます。手順書は「ユニットは relpath と行で探す（qualname だけだと、別のファイルにある同名のツールを取り違える。D64 / U50）」と定めています。U50 は、評価の道具の鍵にファイルの場所が無く、別のファイルの同じ名前のツールの矛が 1 件に潰れていた、という凍結前の添削の所見です（決定 D64 で、道具の鍵に relpath・lineno・宣言を足した）。
（出典: `docs/final_evaluation_procedure.md:496, 1445`、`docs/decisions.md:3575`。）

#### 演習 12-3（v4 の実物で、宣言と wrapper を確かめる）

1. manifest の `unit`: `relpath` は `src/texas_grocery_mcp/tools/coupon.py`、`lineno` は 331、`registration` は `{"form": "call", "relpath": "src/texas_grocery_mcp/server.py", "lineno": 182}`。
2. 宣言は `src/texas_grocery_mcp/server.py` の 182 行 `mcp.tool(annotations={"readOnlyHint": True})(coupon_clipped)` にあります。中身は `readOnlyHint: true`（D1、読むだけ）だけです。
3. `def` の行は `src/texas_grocery_mcp/tools/coupon.py` の 331 行 `async def coupon_clipped(`。その上の 330 行に `@ensure_session` があります。
4. `ensure_session` は `src/texas_grocery_mcp/auth/session.py` の 741 行で定義され、wrapper は 758 行です。wrapper は、本体（765 行の `return await func(*args, **kwargs)`）より先に、760 行で `auto_refresh_session_if_needed()` を呼び、ログインの期限が切れかけていれば自動でログインし直します。v4 の判定の記録（R16。本記録者の判定で論文には使わない）によると、その先でブラウザを使ってログインをし直し、認証の状態のファイルを上書きし、古い画面の写しのファイルを消します（条件つき）。
   解析器は、このデコレータの wrapper を呼び出しとしてたどりません（O42 の RC5、O43 の「デコレータの wrapper を呼び出しとしてたどらない」）。だから、この書き込み・削除には矛も不も出ず、v4 の判定では「見落とし」（原因はその他）とされました。
（出典: `evidence/population_v4/v4_judgments.json` の R16、`docs/open_questions.md:1167, 1194`。）

#### 演習 12-4（低レベルの書き方）

1. **宣言**: 原ソースでは、`src/vision_mcp/server.py` の 50 行からの `COMPARE_TOOL = Tool(name="vision_compare_images", ...)` の中、73〜79 行の `annotations=ToolAnnotations(...)` です。manifest では、ユニット `handle_call_tool` の `unit.dispatch_annotations["vision_compare_images"]`（ツールごとの宣言のまとめは `D_kind_by_tool["vision_compare_images"]`）を見ます。
2. **どの分岐か**: ハンドラ（89 行）の中の 95 行 `elif params.name == "vision_compare_images":` の分岐です。その中の 97 行で `_compare_images(...)` を呼んでいるので、判定の対象の効果が `_compare_images` から先にあるかを、manifest の `witness_chain`・`entry_lineno`（97 行のはず）と原ソースで確かめます。manifest の `dispatch_join.attribution` で、その効果がどのツールに帰属されたかも見られます。
3. **snake_case が `readOnlyHint` として読まれる理由**: この木の `pyproject.toml` は `mcp[cli]>=2.0` と書いていて、解析器はこの木の MCP の SDK の版を 2.0 以上（`mcp_version` が `ge2`）と判断しました。決定 D64 の U38 で、SDK 2.x では snake_case の注釈（`read_only_hint` など）が `ToolAnnotations` の正式な属性名で、クライアントには `readOnlyHint` として届くので、宣言として読むと決めました（2.0 より前の版なら届かないので `D_malformed`、版が決まらなければ `D_unknown`）。詳しくは第 16 章。
（出典: `corpus/v4-itzfaisal__vision-mcp/pyproject.toml:9`、`evidence/scan_v2_v4_run1/v4-itzfaisal__vision-mcp.json` の `mcp_version`、`authgap/entries.py:2715-2726`、`docs/decisions.md:3590`。）

#### 確認問題 12-1

ハンドラの関数を 1 つのユニットにし、その中の分岐（`if name == "x"`・`name in (...)`・辞書の見出し・`match` の `case`）から、ツールの名前の**候補**（`dispatch_names`）を集めます。
次に、木の中の `Tool(...)` を全部集め、その `name=` の文字列と候補の名前が**完全に一致する**ものを結び付けて、ツールごとの宣言（`dispatch_annotations`）にします。
効果は、どのツールの分岐（`name == "..."` の判定）の中にあるかを調べて、そのツールの宣言で照合します。どの分岐にも入らない効果は、結び付けたすべてのツールの宣言をまとめた「最も厳しい宣言」で照合します。
（出典: `authgap/entries.py:2607-2639, 2803-2850`、`authgap/analyze.py:645-670`。）

#### 確認問題 12-2

qualname は「どの関数の中のどの関数か」を表す名前で、ファイルの場所を含みません。
そのため、別のファイルに同じ qualname のツールがあると、取り違えます（v4 の 88 木のうち 16 木にあった。mcp-atlassian の `add_comment` など）。
入れ子の定義では qualname に外側の名前が付く（`register.dependency_graph`）ので、関数の名前だけでは見つからないこともあります。
だから、`relpath` と `lineno` の**両方**で探します（手順書 6.5 節、D64 の U50）。`unit_id` にもファイルの場所が入っていないので、`unit_id` でも決まりません。

#### 確認問題 12-3

- **宣言**: `registration` があるので、呼び出しの形の登録です。宣言は登録の行、つまり `src/pkg/server.py` の **40 行**にあります（`mcp.tool(annotations={"destructiveHint": False})(export_note)` のような行のはず）。
- **関数の本体**: `relpath` と `lineno` が関数の定義を指すので、`src/pkg/tools/notes.py` の **88 行**（`def export_note(` の行）から読みます。
- 88 行の上に、入口の印以外のデコレータがあれば、その wrapper も読みます（解析器はたどらないので）。

#### 確認問題 12-4

`unreadable` は、`annotations=` を書いているのに、解析器がその中身を読めなかったユニットです。
`annotations=READ_ONLY` のような変数、`annotations=_annotations(readOnlyHint=True)` のような `ToolAnnotations` 以外の関数の呼び出し、`ToolAnnotations(**変数)` などが当たります（v4 で 151 ユニット）。

その宣言は、D1〜D4 の**どれとも照合されません**。
解析器は読めない宣言を「宣言なし」とも「読むだけ」とも決めず、「読めない」（`D_kind` の `unknown`）として残すからです。
効果が見つかっていても、矛も不も出ません。

`D_kind.explicit` が空なので、**見落としの抜き取りの対象にも入りません**（対象は「D1 か D2 を明示し、その宣言への矛が無いユニット」）。
ただし、`r_malformed`（D65）の分母「注釈を書いたユニット」には入ります（`annotation_form` が `ToolAnnotations` / `dict` / `unreadable`）。
（出典: `authgap/dparse.py:193-194`、`docs/final_evaluation_procedure.md:441-442`、`docs/preregistration.md:489`。）
