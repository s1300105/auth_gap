[← 付録 D — 第 3 部（第 9・10 章）](appendix-d-3.md) ｜ [目次](README.md) ｜ [付録 D — 第 5 部（第 21〜26 章） →](appendix-d-5.md)

---

# 付録 D 演習と確認問題の答え — 第 4 部（第 11〜20 章）

<a id="ad-4-1"></a>
## 第 11 章 全体の流れ の答え

### 演習 11-1（7 つの段階を当てはめる）

本書の執筆時に、この作例を凍結版と同じ版の解析器にかけて、下の答えと一致することを確かめました。

| 段階 | この例では |
|---|---|
| ① 入口を探す | `@mcp.tool(...)` の付いた `get_weather` がユニットになる。`_log` には印が無いのでユニットではない |
| ② 中をたどる | 本体の 17 行（`_log("asked: " + city)`）で `_log` に降りる（深さ 1）。`requests.get` は木の外のライブラリなので、中には降りない |
| ③ 効果を見つける | 16 行の `requests.get`（`NET`、メソッドは GET）と、`_log` の中の 10 行の `open(LOG_PATH, "a")`（`FS_WRITE`） |
| ④ 値を追いかける | GET の宛先のホスト（`api.example.com`）とパスは定数なので主体は `OP`。問い合わせの部分（`params={"q": city}`）は引数 `city` から来るので主体は `MODEL`。ログのファイルの場所は定数 `LOG_PATH` なので `OP` |
| ⑤ 宣言を読む | `readOnlyHint=True` → D1。`openWorldHint` は書かれていないので D3 は約束していない |
| ⑥ 照合する | GET は「安全」なメソッドなので D1 の内（[第 10 章](ch10.md)）。`open(..., "a")` はファイルの書き込みなので D1 の矛（理由 `fs_write`） |
| ⑦ 書き出す | 木の manifest に、ユニット・2 つの効果・行ごとの注記を書く |

ポイント:
- 「天気を調べるだけ」に見えるツールでも、ログのファイルに追記していれば、D1（読むだけ）に反します。ログへの追記が軽いかどうかは、正誤ではなく書き込み先のラベル（ログ）で表します（第 43・51 章）。
- 書き込み先が定数（`OP`）でも、D1 では矛です。D1 にとっては「誰が場所を決めたか」ではなく「書くかどうか」が問題だからです。
- この作例に `openWorldHint=False`（D3）も書かれていたら、定数の外部ホストへの GET は D3 の矛になります（[第 10 章](ch10.md) 10.11 節）。

### 演習 11-2（manifest の道しるべ）

1. 読むのをやめていないか → そのユニットの `cap_hits`（上限に当たった記録）。あわせて、木の `truncations` も見る。段階②の欄。
2. 書き込み先のパスを LLM が決められると考えているか → その効果の `slots` の `path` の `prin`（主体）。`MODEL` なら LLM が決める値から来ている。あわせて `prov`（確度）が `resolved` か `opaque` かも見る。段階④の欄。
3. 本体の何行目から道筋が始まるか → その効果の `entry_lineno`。道筋そのものは `witness_chain`。段階②の欄。
4. D2 について「不」としたか → その効果の位置の `rows[].notes` に `contradiction_unknown:D2:<理由>` があるか。段階⑥の欄。`verdicts` ではなく `notes` で読む。

### 演習 11-3（木と relpath）

開くファイルは `corpus/final-acme__notes-mcp/src/notes_mcp/tools/export.py` です。
`tree` の値の前に `corpus/` を付け、その後ろに `unit_relpath` をつなげます。

42 行には、ツールの関数の **`def` の行**（`def ...(` または `async def ...(`）があるはずです。
宣言（`@mcp.tool(annotations=...)`）は、その上の行にあります。
ただし、呼び出しの形の登録（`mcp.tool(...)(fn)`）なら、宣言は別の行（manifest の `registration` の行）にあります（[第 12 章](ch12.md)）。

### 演習 11-4（組を数える）

矛の組は **2 つ**です。

- 行 1 と行 2 は、site（`os.remove`）・kind（`FS_WRITE`）・宣言（D2）が同じなので、位置が 30 行と 55 行の 2 つあっても **1 組**です（`locations` に 2 つの位置が並ぶ）。
- 行 3 は site が `builtins.open` で違うので、**別の 1 組**です。
- 行 4 は `contradiction_unknown:D2:net_post` なので「不」です。矛の組には数えません（D2 の不の組として、不の中身の抜き取りの候補にはなる）。

### 確認問題 11-1

同時に進むのは ②（中をたどる）・③（効果を見つける）・④（値を追いかける）です。
解析器はツールの関数を 1 行ずつ読みながら、呼び出し・効果・値の出どころを同時に判断します。
解説の章の順番（③が[第 13 章](ch13.md)、④が[第 14 章](ch14.md)、②が[第 15 章](ch15.md)）が段階の番号と一致しないのは、「何を探すか」（効果と値）を先に学び、「どこまでたどるか」（深さと呼び出しの解決）を後で学ぶ方が分かりやすいからです。

### 確認問題 11-2

「不」かどうかは、その効果の行の `rows[].notes` に `contradiction_unknown:D1:<理由>` があるかで分かります。
「内」は manifest に書かれません。
その効果の行の `notes` に、D1 について `contradiction:D1` も `contradiction_unknown:D1:...` も無ければ、内です。
`verdicts` の `UNKNOWN` は付録の判定で、「不」とは別物なので、これで判断してはいけません（[第 8 章](ch08.md) 8.6 節）。

### 確認問題 11-3

「矛」は**解析器の主張**で、「この効果はこの宣言に反する」と解析器が判定表に従って言ったものです。
「正」は、**人が原ソースで確かめて**、その効果が本当にツールの呼び出しで到達し、かつ宣言に反すると認めたものです。
矛のうち、人が確かめて到達しない・反しないと分かったものは「誤」になります。

解析器の「不」は、「反するかどうかが静的に（動かさずに）決められない」という解析器の答えです。
人の「不明」は、「人が原ソースを読んで調べても決められない」という人の答えです。
解析器が不と言ったものでも、人が相手の API の文書などを調べれば「違反」「違反でない」と決まることがあります。

### 確認問題 11-4

学生が選んだ原理 2（静的に決まらない性質をどう扱うか）で、「a 不明とする」を選んだからです。
分からないものを「内」（問題なし）に数えると宣言違反の率が低く出て、危険を見落とす向きに偏ります。
「矛」に数えると高く出ます。
どちらに倒しても測定が既知の向きに偏るので、「不」として別に数え、件数を必ず報告します。
これは作業の約束（CLAUDE.md の規則 4）「解決できなかったものは『不明』として記録する。黙って安全側に倒さない」と同じ考えです。
（出典: `docs/contradiction_principles.md:60-66, 139`。）


---

<a id="ad-4-2"></a>
## 第 12 章 入口を見つける の答え

### 演習 12-1（登録の形を見分ける）

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

### 演習 12-2（qualname で見つからないとき）

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

### 演習 12-3（v4 の実物で、宣言と wrapper を確かめる）

1. manifest の `unit`: `relpath` は `src/texas_grocery_mcp/tools/coupon.py`、`lineno` は 331、`registration` は `{"form": "call", "relpath": "src/texas_grocery_mcp/server.py", "lineno": 182}`。
2. 宣言は `src/texas_grocery_mcp/server.py` の 182 行 `mcp.tool(annotations={"readOnlyHint": True})(coupon_clipped)` にあります。中身は `readOnlyHint: true`（D1、読むだけ）だけです。
3. `def` の行は `src/texas_grocery_mcp/tools/coupon.py` の 331 行 `async def coupon_clipped(`。その上の 330 行に `@ensure_session` があります。
4. `ensure_session` は `src/texas_grocery_mcp/auth/session.py` の 741 行で定義され、wrapper は 758 行です。wrapper は、本体（765 行の `return await func(*args, **kwargs)`）より先に、760 行で `auto_refresh_session_if_needed()` を呼び、ログインの期限が切れかけていれば自動でログインし直します。v4 の判定の記録（R16。本記録者の判定で論文には使わない）によると、その先でブラウザを使ってログインをし直し、認証の状態のファイルを上書きし、古い画面の写しのファイルを消します（条件つき）。
   解析器は、このデコレータの wrapper を呼び出しとしてたどりません（O42 の RC5、O43 の「デコレータの wrapper を呼び出しとしてたどらない」）。だから、この書き込み・削除には矛も不も出ず、v4 の判定では「見落とし」（原因はその他）とされました。
（出典: `evidence/population_v4/v4_judgments.json` の R16、`docs/open_questions.md:1167, 1194`。）

### 演習 12-4（低レベルの書き方）

1. **宣言**: 原ソースでは、`src/vision_mcp/server.py` の 50 行からの `COMPARE_TOOL = Tool(name="vision_compare_images", ...)` の中、73〜79 行の `annotations=ToolAnnotations(...)` です。manifest では、ユニット `handle_call_tool` の `unit.dispatch_annotations["vision_compare_images"]`（ツールごとの宣言のまとめは `D_kind_by_tool["vision_compare_images"]`）を見ます。
2. **どの分岐か**: ハンドラ（89 行）の中の 95 行 `elif params.name == "vision_compare_images":` の分岐です。その中の 97 行で `_compare_images(...)` を呼んでいるので、判定の対象の効果が `_compare_images` から先にあるかを、manifest の `witness_chain`・`entry_lineno`（97 行のはず）と原ソースで確かめます。manifest の `dispatch_join.attribution` で、その効果がどのツールに帰属されたかも見られます。
3. **snake_case が `readOnlyHint` として読まれる理由**: この木の `pyproject.toml` は `mcp[cli]>=2.0` と書いていて、解析器はこの木の MCP の SDK の版を 2.0 以上（`mcp_version` が `ge2`）と判断しました。決定 D64 の U38 で、SDK 2.x では snake_case の注釈（`read_only_hint` など）が `ToolAnnotations` の正式な属性名で、クライアントには `readOnlyHint` として届くので、宣言として読むと決めました（2.0 より前の版なら届かないので `D_malformed`、版が決まらなければ `D_unknown`）。詳しくは[第 16 章](ch16.md)。
（出典: `corpus/v4-itzfaisal__vision-mcp/pyproject.toml:9`、`evidence/scan_v2_v4_run1/v4-itzfaisal__vision-mcp.json` の `mcp_version`、`authgap/entries.py:2715-2726`、`docs/decisions.md:3590`。）

### 確認問題 12-1

ハンドラの関数を 1 つのユニットにし、その中の分岐（`if name == "x"`・`name in (...)`・辞書の見出し・`match` の `case`）から、ツールの名前の**候補**（`dispatch_names`）を集めます。
次に、木の中の `Tool(...)` を全部集め、その `name=` の文字列と候補の名前が**完全に一致する**ものを結び付けて、ツールごとの宣言（`dispatch_annotations`）にします。
効果は、どのツールの分岐（`name == "..."` の判定）の中にあるかを調べて、そのツールの宣言で照合します。どの分岐にも入らない効果は、結び付けたすべてのツールの宣言をまとめた「最も厳しい宣言」で照合します。
（出典: `authgap/entries.py:2607-2639, 2803-2850`、`authgap/analyze.py:645-670`。）

### 確認問題 12-2

qualname は「どの関数の中のどの関数か」を表す名前で、ファイルの場所を含みません。
そのため、別のファイルに同じ qualname のツールがあると、取り違えます（v4 の 88 木のうち 16 木にあった。mcp-atlassian の `add_comment` など）。
入れ子の定義では qualname に外側の名前が付く（`register.dependency_graph`）ので、関数の名前だけでは見つからないこともあります。
だから、`relpath` と `lineno` の**両方**で探します（手順書 6.5 節、D64 の U50）。`unit_id` にもファイルの場所が入っていないので、`unit_id` でも決まりません。

### 確認問題 12-3

- **宣言**: `registration` があるので、呼び出しの形の登録です。宣言は登録の行、つまり `src/pkg/server.py` の **40 行**にあります（`mcp.tool(annotations={"destructiveHint": False})(export_note)` のような行のはず）。
- **関数の本体**: `relpath` と `lineno` が関数の定義を指すので、`src/pkg/tools/notes.py` の **88 行**（`def export_note(` の行）から読みます。
- 88 行の上に、入口の印以外のデコレータがあれば、その wrapper も読みます（解析器はたどらないので）。

### 確認問題 12-4

`unreadable` は、`annotations=` を書いているのに、解析器がその中身を読めなかったユニットです。
`annotations=READ_ONLY` のような変数、`annotations=_annotations(readOnlyHint=True)` のような `ToolAnnotations` 以外の関数の呼び出し、`ToolAnnotations(**変数)` などが当たります（v4 で 151 ユニット）。

その宣言は、D1〜D4 の**どれとも照合されません**。
解析器は読めない宣言を「宣言なし」とも「読むだけ」とも決めず、「読めない」（`D_kind` の `unknown`）として残すからです。
効果が見つかっていても、矛も不も出ません。

`D_kind.explicit` が空なので、**見落としの抜き取りの対象にも入りません**（対象は「D1 か D2 を明示し、その宣言への矛が無いユニット」）。
ただし、`r_malformed`（D65）の分母「注釈を書いたユニット」には入ります（`annotation_form` が `ToolAnnotations` / `dict` / `unreadable`）。
（出典: `authgap/dparse.py:193-194`、`docs/final_evaluation_procedure.md:451-452`、`docs/preregistration.md:489`。）


---

<a id="ad-4-3"></a>
## 第 13 章 「効果」— 外の世界に触れる操作 の答え

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
「解析器の結果」はその走査の出力です。「人の判定」の見通しは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

### 演習 13-1（効果を見つける）

**(1) D1（`readOnlyHint=True`）の場合**

| 行 | 効果か | `kind` | `site` | `form` | D1 の解析器の結果 |
|---|---|---|---|---|---|
| 17 `total = len(name) * 2` | **効果ではない** | — | — | — | 関数の中の計算だけ |
| 18 `os.makedirs(...)` | 効果 | `FS_WRITE` | `os.makedirs` | `direct` | 矛（`fs_write`） |
| 19 `requests.get(...)` | 効果 | `NET` | `requests.get` | `direct` | 内（GET は安全なメソッド。注記なし） |
| 20 `tempfile.mkstemp()` | **効果ではない** | — | — | — | sink 表に無い（ただし実際には一時ファイルを作る） |
| 21 `open(tmp, "w")` | 効果 | `FS_WRITE` | `builtins.open` | `direct` | 矛（`fs_write`）。`destructive: true`、`fs_mode: "w"` |
| 22 `f.write(data)` | **別の効果ではない** | — | — | — | 書き込みは 21 行の `open` の効果に含まれる |
| 23 `shutil.copy(...)` | 効果 | `FS_WRITE` | `shutil.copy` | `direct` | 矛（`fs_write`） |
| 24 `os.remove(tmp)` | 効果 | `FS_WRITE` | `os.remove` | `direct` | 矛（`fs_write`） |
| 25 `logging.getLogger().info(...)` | **効果ではない** | — | — | — | `logging` は sink 表に無い。この作例ではファイルの出し口も設定していない |
| 26 `return data` | **効果ではない** | — | — | — | 戻り値は効果に入らない |

- 走査の出力では、19 行の `NET` の slot は `url.scheme`（`https`）・`url.host`（`example.com`）・`url.path`（`/api`）が `OP`、`url.query` が `MODEL` でした（13.8 節）。
- 21 行の `path` の slot は、主体 `OP`・確度 `opaque` でした。`tmp` は sink 表に無い `mkstemp` の戻り値なので、解析器は値を追い切れません（[第 14 章](ch14.md)）。
- 23 行の `path` の slot は、行き先の `os.path.join("/tmp/snap", name)` で、主体 `MODEL`・確度 `resolved` でした。`content` の slot が元の `tmp` です（13.8 節の「`shutil.copy(a, b)` の `path` は `b`」）。
- 20 行は効果に出ませんが、ディスクにファイルを 1 つ作ります。人が D1 を判定するなら、これも「環境を変える」書き込みです（13.7 節）。この作例では、ほかの行に矛が出ているので見落としの判定の対象にはなりませんが、矛の 1 件もないツールなら、見落とし（原因「語彙」）の候補になる形です。
- 25 行は、ログの出し口を何も設定していないので、`info` の記録はファイルに書かれません（[第 9 章](ch09.md) 9.5）。出し口が `FileHandler` などなら、解析器の出力に出ない書き込みになります。

**(2) D2（`destructiveHint=False`）の場合**

| 行 | 13.9 節の類 | D2 の解析器の結果 | 理由 |
|---|---|---|---|
| 18 `os.makedirs` | 追記（`append`） | 内 | `destructive=False` |
| 19 `requests.get` | （`NET`） | 内 | GET は安全なメソッド |
| 21 `open(tmp, "w")` | 書き出し（`writeout`） | 不（`fs_writeout`） | 書き先 `tmp` の主体は `OP` で、モデルが選べない |
| 23 `shutil.copy` | 書き出し（`writeout`） | 矛（`fs_writeout_model_path`） | 行き先の `path` の主体が `MODEL`・確度 `resolved` で、モデルが選べる |
| 24 `os.remove` | 消す・動かす・変える（`remove`） | 矛（`fs_remove`） | 書き出しの一覧に無い `destructive=True` |

本記録者が `destructiveHint=False` の同じ本体を走査した出力は、この表のとおりでした。

**(3) 「誤」になりそうなもの**

- **24 行の `os.remove(tmp)`**。消している `tmp` は、同じ呼び出しの 20 行で `mkstemp` が作った一時ファイルです。D2 の問いは「**呼び出しの前からあったもの**を消すか」なので、自分で作ったばかりのファイルを消すのは反しません。誤の原因は **E2**（同じ呼び出しで作った一時ファイル・ロックの後始末）の見当です。v3 の O41（`mkstemp` / atomic write の後始末）と同じ類です。
- **23 行の `shutil.copy`** は、「正」になりそうです。行き先のファイル名 `name` をモデルが決めるので、`/tmp/snap` の中に前の呼び出しが作ったファイルなどがあれば、それを上書きできます（[第 17 章](ch17.md)で学ぶ原理 3-a。手引きの 15.2 の「書き出し: 書き先をモデルが決められるなら反する」）。
- 参考: 21 行（不 `fs_writeout`）は矛ではないので、矛の判定の対象ではありません。不の中身の判定（[第 52 章](ch52.md)）で当たったなら、書き先が作ったばかりの空の一時ファイルなので、「違反でない」と答える見通しです。

（出典: `docs/drafts/final_judging_guide_draft.md:333-353`、`:436`、`docs/open_questions.md:1061`）

### 演習 13-2（`open(p, 'x')` と D2）

**(1)** `kind` は `FS_WRITE`、`destructive` は `false`、`fs_mode` は `"x"` です。
モード `'x'` は定数で `x` を含むので書き込み（`_mode_is_write`）、`w` も `+` も含まず `x` を含むので追記型（`_mode_destructive`）です。

**(2)** D2 の解析器の判定は**内**（行の注記なし）です。
`builtins.open` は書き出しの一覧に入っていますが、`open` の仲間で `destructive` が `false` なので、`_fs_class` は「追記」（`append`）を返し、D2 では内になります（判定表 §7.2 の「追記型: `open('a' / 'x')` → 内」）。
書き先 `path` をモデルが決めることは、**結果を変えません**。
「追記」の類では、書き先をモデルが選べるかを見る前に内が決まるからです（`_d2` は `append` なら `None` を返し、`_by_choice` に進まない）。
本記録者の走査でも、`path` の主体が `MODEL`・確度 `resolved` のまま、注記は付きませんでした。

**(3)**
- D1（`readOnlyHint=True`）: **矛**（`fs_write`）。D1 は `destructive` を見ず、`FS_WRITE` はすべて矛です。新しいファイルを作ることも「環境を変える」からです。
- D4（`idempotentHint=True`）: **内**。D4 が矛にするのは、`open` の仲間でモードが定数の `'a'` を含むときだけです。`'x'` は `a` を含みません。本記録者の走査でも注記は付きませんでした。

**(4)** 反しません。
`'x'` は「新しく作る。同じ名前のファイルが既にあれば失敗する」モードです（[第 9 章](ch09.md) 9.3）。
だから、どの `path` を渡されても、呼び出しの前からあったファイルの中身を消したり上書きしたりすることはできません。
書き先をモデルが決めても同じです。既存のファイルを指せば、書く前に失敗するだけです。
手引きの D2 の表も「新しく作るだけ（`mkdir`、`open('x')`、…）→ 反しない」としています。
（出典: `docs/drafts/final_judging_guide_draft.md:339`、`docs/contradiction_principles.md:185`）

**(5)** `'a+'` なら、次のように変わります。

- (1): `destructive` が **`true`**、`fs_mode` が `"a+"`。`_mode_destructive` は `+` があれば `true` にするからです。
- (2): `_fs_class` は「書き出し」（`writeout`）を返します。書き先 `path` をモデルが選べるので、D2 は**矛**（`fs_writeout_model_path`）になります（本記録者の走査で確かめた）。`path` が定数なら不（`fs_writeout`）です。
- (4): 人の答えは変わりません。`'a+'` の書き込みは常にファイルの末尾に足されるので、前の中身は残ります（`truncate()` などで切り詰めていなければ）。解析器が矛を出しても、人の判定では「宣言に反しない」の**誤**になる見通しで、原因は **E8**（宣言に反しない）の見当です。13.10 節の「`'a+'` は D2 では書き出し扱い」が、この食い違いの理由です。
- 参考: D4 では `'a+'` も `a` を含むので矛（`fs_append`）になります。

### 演習 13-3（`pipe:communicate` はファイルの書き込みか）

**(1) 解析器の結果**（本記録者の走査の出力）

| | `site` | `form` | `kind` | slot（主体） | D1 の解析器の結果 |
|---|---|---|---|---|---|
| (ア) `kubectl` | `pipe:communicate` | `pipe` | `FS_WRITE` | `content`（`OP`。値は定数の `None`） | 矛（`fs_write`） |
| (イ) `sqlite3` | `pipe:communicate` | `pipe` | `FS_WRITE` | `content`（`MODEL`） | 矛（`fs_write`） |
| (ウ) `sh` | `pipe:communicate` | `pipe` | **`EXEC`** | `code_text`（`MODEL`） | 矛（`exec`） |

- (ア)(イ): `kubectl` も `sqlite3` もインタプリタの一覧に無いので、`FS_WRITE`（`content`）の情報行になります。`destructive` は `null` です。(ア) は `input=None` でも効果が出ます。
- (ウ): `sh` はインタプリタの一覧に載っているので、`EXEC`（`code_text`）になります。
- どれも、子の起動（`subprocess.Popen`）が別に `SPAWN` の効果として出て、D1 では不（`spawn_command`。コマンドが定数で、意味が名前から分からない）でした。

**(2) ファイルの書き込みか**

- (ア): **書き込みではありません。** `input=None` なので、子の標準入力には何も流していません。子の `kubectl get pods` は、クラスタの状態を読んで表示するだけです。
- (イ): `communicate` そのものは、子の標準入力に SQL の文字列を流すだけです。しかし子の `sqlite3 notes.db` は、受け取った `INSERT` 文を実行して、`notes.db` という DB のファイルに行を足します。**子を通して、ファイル（DB）が変わります。**
- (ウ): 子の `sh` は、受け取った文字列をシェルのコマンドとして実行します。何をするかは `cmd` の中身しだいで、ファイルの書き込みも削除もできます。

**(3) 人の判定の見通し**

- (ア): **誤**。原因は **E5**（子プロセスの標準入力・パイプを書き込みと読んだ）の見当です。v3 の helm / kubectl（O41 の誤 4）と同じ形です。
- (イ): **正**。D1 の問い「呼び出しの後に残る何かを変えるか」に対して、子が DB に行を足すので反します。`evidence` には、起動の行・流し込みの行と、「`sqlite3` は標準入力の SQL を実行する」ことを書きます。書き込み先の種類は「データベース」の見当です（[第 51 章](ch51.md)）。なお、`title` をそのまま SQL につないでいるので SQL の注入もできますが、それは宣言の正誤とは別の話なので、`note` に書くだけにします。
- (ウ): **正**。コードの実行（`EXEC`）は D1 に反すると決まっています（表 D41。手引きの 15.1）。しかも実行するコマンドをモデルが決めます。

**(4)** `pipe:communicate` は、子プロセスの**標準入力への書き込み**であって、それ自体はファイルの書き込みではありません。
解析器が `FS_WRITE` と記録するのは、「子が受け取ったもので書き込みをするかもしれない」という保守的な上界の情報行だからです（D61 の改訂）。
ファイルが変わるかどうかは、子が何者で、受け取ったものをどう使うかを調べて決めます（(ア) は変わらない、(イ) は変わる）。

（出典: `docs/drafts/final_judging_guide_draft.md:121`、`:315-317`、`:330`、`:439`、`docs/open_questions.md:1068-1070`、`docs/decisions.md:3459-3466`）

### 演習 13-4（manifest の効果を読む）

**(1)** sqlite3 の接続の `execute` に当たる proxy の行は、受け手の型の候補として `sqlite3.Cursor`・`sqlite3.Connection`・`psycopg.Cursor`・`psycopg2.cursor` の 4 つをまとめて持っています。
解析器は site の名前を `sorted(row.recv_types)[0]`（候補をアルファベット順に並べた先頭）とメソッド名から作るので、`psycopg.Cursor.execute` になります。
実際の受け手の型（`sqlite3.Connection`）ではなく、行の候補の先頭が使われるのが理由です（`authgap/effects.py:755`、`authgap/catalog/sinks.py:504-510`）。

**(2)** 「誤」にはしません。
46 行目は、DB に SQL の命令を送る呼び出しで、manifest の `kind`（`DB`）と動作の種類が合っています。
手引きは「site 名のライブラリが違っていても、動作の種類（kind）が合っていれば判定には影響しない。その場合は `note` に書いておく」と決めています。
E4 は「受け手の型の読み違いで、動作の種類まで違う」ときだけです。
`note` には「site は psycopg と表示されるが sqlite3」と書きます。
（出典: `docs/drafts/final_judging_guide_draft.md:126-127`、`:438`）

**(3)**
- `sql`: 1 番目の引数の `"DELETE FROM notes WHERE id = ?"`。コードに直接書かれた定数（開発者が書いた値）なので、主体は `OP` です。
- `params`: 2 番目の引数の `(note_id,)`。モデルが決める引数 `note_id` から来ているので、主体は `MODEL` です（`roots` が `note_id`）。

同じ効果の中でも、slot ごとに値を決めた人が違います。命令の種類は開発者が決め、どの行を消すかはモデルが決めています（13.8 節）。

**(4)** 読むべきなのは **`sql_head` の `DELETE`** です。
`sub_kind` の `DB_WRITE` は「SQL が読み取りの語で始まらない」という意味しかなく、`BEGIN` や `PRAGMA` でも `DB_WRITE` になります（13.3 節。`authgap/effects.py` の `_sub_kind` のコメントは「`readOnlyHint` の矛盾判定にそのまま使ってはならない」と書いている）。
`sql_head` は、定数に読めた SQL の実際の先頭の語で、解析器の矛盾の判定もこちらを使っています。
ただし人の判定では、`sql_head` も手がかりにとどめ、原ソースの SQL そのものを読んで決めます。

**(5)** 反します。
`DELETE` は、呼び出しの前からあった行を消す命令です。
手引きの D2 の表は、DB の `DELETE` を「既存のものを消す・動かす・変える → 反する」に入れています。
`note_id` をモデルが決めるので、既にある行を指すことができます。
解析器の矛（`db_modify`）は**正**になる見通しで、書き込み先の種類は「データベース」の見当です。
（出典: `docs/drafts/final_judging_guide_draft.md:340`、`docs/contradiction_principles.md` §7.2 の DB の行）

### 確認問題 13-1

**受け手 `client` の型**（何のオブジェクトか）を知る必要があります。
`get` という名前のメソッドは世の中にいくらでもあるので、名前だけでは通信か決まりません。
`client` の型が proxy の sink 表の行の候補（`httpx.Client`・`httpx.AsyncClient`・`requests.Session`）のどれかだと分かって、初めて `NET` の効果になります。
型が分からなければ、解析器は**効果を出しません**（通信を見落としうる）。
本記録者が、型の分からない引数 `client` に `client.get(url)` を呼ぶ作例を走査すると、効果は 0 で、ユニットの `opaque_reasons` に `receiver` と `unresolved` が残りました（意味は[第 14 章](ch14.md)）。
受け手の型の知り方は[第 15 章](ch15.md)で学びます。

### 確認問題 13-2

| | `destructive` | 13.9 節の類 | D2 の解析器の結果 |
|---|---|---|---|
| (ア) `os.makedirs(d, exist_ok=True)` | `false` | 追記 | **内** |
| (イ) `os.replace(tmp, target)` | `true` | 消す・動かす・変える | **矛**（`fs_remove`） |
| (ウ) `Path(p).write_text(s)`（`p` は定数） | `true` | 書き出し | **不**（`fs_writeout`） |

- (イ): `os.replace` は書き出しの一覧に無い `destructive=True` の行なので、書き先によらず `fs_remove` の矛です。置き換えられる `target` の前の中身が消えるからです。
- (ウ): `write_text` は書き出しの一覧に入っています。書き先 `p` が定数で、モデルが選べないので不です（`p` をモデルが選べれば矛 `fs_writeout_model_path`）。
- 3 つとも、本記録者の作例の走査で確かめました。

### 確認問題 13-3

**D2 の矛を少なく数える向き**（見落とし、誤 clear の向き）に影響します。
HTTP の `DELETE` は相手の資源を消す操作で、D2 の矛盾の典型ですが、セッションの `.delete` は sink 表に無いので効果に出ず、矛になりません。
そのため、報告する D2 の矛の数は**下限**（本当の数はそれ以上かもしれない）になります。

それでも足さないのは、sink 表が仕様書の計画の「月 3」に**凍結**した語彙だからです。
凍結は「決めたものを後から変えない」約束で、結果を見た後に表を足すと、「都合のよい結果が出るように表を選んだ」ことと区別できなくなります。
そこで O39 として既知の限界に記録し、件数を併記する、という扱いにしています。
（出典: `docs/open_questions.md:1041-1049`）

### 確認問題 13-4

効果を **2 つ**（`FS_READ` と `FS_WRITE`）出します。

| 宣言 | 解析器の結果 |
|---|---|
| D1 | `FS_WRITE` の効果が **矛**（`fs_write`）。`FS_READ` の効果は内 |
| D2（`path` は定数） | **不**（`fs_unknown`）。`destructive` が `null` で「決まらない」の類になり、書き先をモデルが選べないから |
| D4 | **不**（`fs_mode_unknown`） |

理由: モードが読めないときに片方に決めると、「書くかもしれない」（または「読むだけかもしれない」）可能性が記録から消えるので、規則 4「解決できなかったものは不明として記録する。黙って安全側に倒さない」に従い、**clean に潰さず両方を出す**ためです（`authgap/effects.py:656-663`）。
3 つとも、本記録者の作例の走査で確かめました（D1 は書き先がモデルの値の作例で確かめた）。


---

<a id="ad-4-4"></a>
## 第 14 章 値を追いかける — 誰が決めた値か の答え

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
「解析器の答え」「slot の値」はその走査の出力です。
「人の読み」「人の判定」の見通しは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

### 演習 14-1（4 つの情報を予想する）

**(1)(2) 走査の結果**

| ツール | slot | 主体 | 確度（理由） | root | 形 | 解析器の答え |
|---|---|---|---|---|---|---|
| (ア) `thumbnail`（D1） | `argv0` | `OP` | `resolved` | 無し | `{"k": "Atom", "const": "convert"}` | 不（`spawn_command`） |
| (イ) `save_hashed`（D2） | `path` | `MODEL` | `opaque`（`unresolved`） | `name` | `Str`。部品は（`MODEL`・`opaque`・`Unknown`）と定数 `".txt"`（`OP`） | 不（`fs_writeout_model_path_opaque`） |
| (ウ) `save_deep`（D2） | `path` | `OP` | `opaque`（`depth`） | `name` | `{"k": "Unknown"}` | 不（`fs_writeout`） |

- (ア): `subprocess.run` の `argv0` は、列の最初の要素です（`*` を使っていないので、列の先頭が取られる）。定数 `"convert"` なので主体 `OP`。`argv[*]`（引数の列）は `src` を含むので主体 `MODEL`・root `src` でした。D1 の起動は、LLM がプログラムを選べなければ「不（コマンドの意味は名前から分からない）」です。
- (イ): `hashlib.md5(...)` は木の外の関数なので、戻り値は入力（`name`）の主体と root を引き継ぎ、確度は `opaque(unresolved)` になります（14.2 節・D44）。主体 `MODEL` で確度 `opaque` なので、「流れ込む」として `_opaque` の不です。
- (ウ): `save_deep`（深さ 0）→ `_a`（1）→ `_b`（2）→ `_c`（3）→ `_d`（4）→ `_e`（5）。`_e` が深さ 5 になるので、解析器は `_d` の中の `_e(x)` に降りず、戻り値を「主体 `OP`・確度 `opaque(depth)`・root は渡した引数のもの（`name`）」にしました（14.2 節）。ユニットの `cap_hits` は `["depth"]` でした。主体が `MODEL` でないので、`_choice` は「決めない」を返し、D2 の書き出しの行の「それ以外」の答え（不、`fs_writeout`）になりました。理由の名前に `_opaque` は付きません。

**(3) 人の読み**

- (ア): 起動されるプログラムは `convert` で、LLM は選べません。LLM が決めるのは入力のファイル `src` です。D1 に反するかは、次の問い「`convert` が何をするか」で決めます（[第 50 章](ch50.md)の SPAWN の問い）。ImageMagick の `convert` なら、`src` を読み `out.png` というファイルを書き出します。
- (イ): 書き先は `name` の md5 の 16 進表記 32 文字に `.txt` を付けた名前です。LLM の値は書き先に**流れ込みます**が、LLM は任意の場所を**選べません**（今いるディレクトリの、16 進の名前のファイルに限られる）。解析器の「流れ込むが、選べるとまでは読み切れない」は、この形に合っています。
- (ウ): 書き先は `"/srv/notes/" + name` で、LLM はファイル名を**選べます**（`../` を含めれば `/srv/notes` の外も指せます）。ところが解析器の主体は `OP` です。深さの上限で降りなかったからです。

(イ) と (ウ) を比べると、解析器の主体と人の読みが**逆向き**にずれています。
(イ) は解析器が `MODEL`（流れ込む）で、人の読みでも「選べない」。
(ウ) は解析器が `OP` なのに、人の読みでは「選べる」。
(ウ) の手がかりは、「主体が `OP` なのに root が `name` で、確度が `opaque(depth)`」という組み合わせと、ユニットの `cap_hits` の `depth` です。
この組み合わせを見たら、解析器が降りなかった関数（ここでは `_e`）を自分で読みます。

### 演習 14-2（slot の JSON を読む）

**(1)** 部品ごとに答えます。

- `base`（出発点）: 定数 `"/srv/exports"` で、主体 `OP`。開発者が決めた値です。
- `segs` の 1 つ目（つなぐ部品）: `req.filename` から来た値で、主体 `MODEL`。LLM が決めた値です。
- 全体: LLM の値が混ざっているので主体 `MODEL`。つまり「書き先のディレクトリは開発者、ファイル名は LLM が決める値」です。

**(2)** 読み切れていません。確度が `opaque`、理由が `unresolved` で、root が欄ごと（`req.filename`）ではなく引数全体（`req`）です。
原因は、`ExportReq` に `model_config = ConfigDict(str_strip_whitespace=True)`（文字列の欄の前後の空白を、構築時に取る設定）があることです。
解析器はこれを構築時のフックとみなし、`req` を欄に分けずに平らな 1 つの値として種を置きます。
そのため `req.filename` を読むと、値の表にもオブジェクトの記録にも無いので、主体と root を `req` から受け継ぎ、確度は `opaque(unresolved)` になります（14.8 節の場合 3、14.10 節の ④）。

**(3)** 走査の結果は、`path` と `content` のどちらの行も「不（`fs_writeout_model_path_opaque`）」でした。
`write_text` は書き出し（今あるものを上書きしうる）の類で、書き先の主体が `MODEL`・確度が `opaque` なので、「流れ込むが、選べるとまでは読み切れない」不です。

**(4)** 選べると言えます。
`str_strip_whitespace` は前後の空白を取るだけで、ファイル名の中身を絞りません。
だから、LLM は `/srv/exports` の下のファイル名を自由に決められます（`a/b.txt` のように下のディレクトリを含めたり、`../` で外に出たりもできます）。
解析器が「不」にしたのは、フックの中身を読まなかったからで、人は設定の意味を読めば決められます。
次は D2 の問い（呼び出しの前からあったファイルを上書きしうるか）に進みます（[第 50 章](ch50.md)）。

**(5)** `model_config` の行を消した版（フックの無い pydantic のモデル）を走査すると、`path` の slot は「主体 `MODEL`・確度 `resolved`・root `req.filename`」、`segs` の部品は `{"formal": "req.filename", "k": "Atom"}` になりました。
D2 の解析器の答えは、矛（`fs_writeout_model_path`）でした。
同じ動作のツールが、構築時の設定 1 行の有無で、不と矛に分かれます。

### 演習 14-3（`receiver` は何が起きたときに出るか）

**(1)** 走査の結果です。

| | ユニットの `receiver` | slot の `receiver` | 理由 |
|---|---|---|---|
| (ア) `r.text` | 無し | 無し | `r.text` は変数 `r` から属性 1 段の道筋なので、値の表のキーになる |
| (イ) `requests.get(...).text` | **有り** | 無し | 道筋の始まりが呼び出しの結果（ただの変数でない）なので道筋が `None`。`.text` の値も見つからない。ただし、戻り値を作る所なので通信の効果の slot（`url.*`）には関係しない（どれも `resolved`） |
| (ウ) `type(e).__name__` | **有り** | 無し | 同じく呼び出しの結果から属性をたどる。`os.remove` の `path` は定数 `"/tmp/x"`（`OP`・`resolved`）で関係しない |
| (エ) `o.a.b.c = name` | **有り** | **有り**（`["receiver", "unresolved"]`） | 属性 3 段への代入は記録されず `receiver`。読み戻しも 3 段なので `receiver` |
| (オ) `o.mid.inner.client.post(url)` | 無し | 無し | 3 段の道筋だが、各オブジェクトの記録（`fields`）をたどって値と型が見つかる。通信の proxy の効果（site `httpx.AsyncClient.post`）が出て、`url.host` は `MODEL`・`resolved`・root `url` |

(イ) と (ウ) は、v4 の gemini の `gemini_prompt` のユニットの `receiver` と同じ形です（gemini は 238 行の `type(e).__name__`）。

**(2)** (エ) の `path` は、「主体 `OP`・確度 `opaque`・理由 `["receiver", "unresolved"]`・root 無し」でした。
本当は `name`（LLM の値）を消すのに、主体も root も LLM の値を示していません。
代入が値の表に記録されなかったので、読み戻したときに `name` の情報が失われたのです。
判定のときは、**主体 `OP` で確度 `opaque` の slot を「LLM は関係ない」と読まない**ことが大事です。
理由に `receiver` があれば、原ソースで深い属性に何が代入されているかを確かめます。
（この作例は D1 なので、`FS_WRITE` は確度によらず矛（`fs_write`）でした。書き先を LLM が選べるかで答えが分かれる宣言では、答えが矛から不にずれます。）

**(3)** (オ) では、属性を 3 段たどっていて、`o.mid.inner.client` という道筋は値の表のキーになりません。
それでも `receiver` は付かず、受け手の型（`requests.Session` の類）も分かって通信の効果が出ました。
オブジェクトの記録（`fields`）をたどって値が見つかったからです。
つまり、「3 段たどった」こと自体でも、「型」のことでもなく、「値が見つかったかどうか」で `receiver` の有無が決まっています。
`receiver` は「深い道筋の先の値を、値の表からもほかの方法でも引けなかった」ときにだけ付きます。
(エ) のように型の話が出てこない代入でも付き、(オ) のように 3 段でも値が見つかれば付きません。
「受け手の型が分からなかった」という説明では、この 2 つの結果をどちらも説明できません。

### 演習 14-4（手順 B を練習する）

**(1)** 「打ち切り: []」から、解析器はこのユニットの途中で読むのをやめていない（深さの上限・要約の数の上限に達していない）ことが分かります。
「opaque: ['unresolved']」から、ユニットの解析中のどこかで、解決できない呼び出しや名前があったことが分かります。
けれども、それが**どこで**立ったか、対象の slot に関係するかは分かりません（ユニット全体の一覧なので）。
対象の slot は「確度=resolved」なので、この効果の判定に効く値は確かに読めています。

**(2)** `argv0` の slot が「主体=MODEL 確度=resolved」なので、`_choice` が「選べる」（`chosen`）を返し、D1 の起動の判定が矛（`spawn_model`）になりました。
`argv0` の slot には、`*cmd` で渡した列全体 `["wc", "-l", path]` が入っていると考えられます。
走査の JSON では、`argv0` の形は `Seq` で、要素は `"wc"`（`OP`）・`"-l"`（`OP`）・`path`（`MODEL`）でした。
解析器が `*` を展開せず、列全体を 1 番目の位置引数として扱う既知の限界（O42 の U26）です。

**(3)** 起動されるプログラムは、列の最初の要素の `wc` です（[第 9 章](ch09.md) 9.6 節: `*cmd` は要素を 1 つずつ別の引数として渡す）。
LLM は `wc` を選べません。LLM が決めるのは、数える対象のファイルの場所（`path`）だけです。

**(4)** 誤になりそうです。
`wc -l` は、ファイルを読んで行の数を数えて表示するだけのプログラムで、ファイルを書き換えません。
だから、この起動は「環境を変えない」とする D1 に反しない見込みです。
誤の原因の記号は、**E7**（LLM が決められないのに決められるとした）の候補です。
解析器が「LLM が起動するプログラムを選べる」としたのは、`*cmd` の扱いの限界によるもので、実際には選べないからです。
（実際の判定では、`wc` の文書で書き込みの機能が無いことを確かめ、`evidence` の欄に読んだ範囲を書きます。第 48・51 章。）

**(5)** 1 つずつ渡す版を走査すると、`argv0` は定数 `"wc"`（主体 `OP`・確度 `resolved`）、`argv[*]` は主体 `MODEL`・root `path` になりました。
D1 の解析器の答えは、不（`spawn_command`）でした。
Python の意味では同じ動作なのに、書き方だけで矛と不が分かれます。

### 確認問題 14-1

主体は `MODEL` です。`host`（LLM の値）が混ざっているからです。
形は `Str` で、部品は `"https://"`（`OP`）・`host`（`MODEL`）・`"/api"`（`OP`）です。
形から、「通信の方式（`https`）とパス（`/api`）は開発者が決めているが、**宛先のホストそのものを LLM が決める**」と分かります。
作例を走査すると、`requests.get("https://" + host + "/api")` の `url.host` の slot が、主体 `MODEL`・確度 `resolved`・root `host`・形 `Str`（上の 3 つの部品）でした。
宛先を LLM が選べるので、`openWorldHint: false`（D3）を宣言したツールなら、判定で問題になる形です（[第 17 章](ch17.md)）。

### 確認問題 14-2

深さの上限で、解析器が呼び出し先の関数に降りなかったと考えられます。
降りなかった呼び出しの戻り値は、「主体 `OP`・確度 `opaque(depth)`・root は渡した引数のもの」になります（14.2 節）。
root が `name` なので、LLM の値 `name` が、降りなかった関数に渡されています。
その関数の中で `name` がそのまま、または加工されて返っているなら、`path` には LLM の値が入ります。
だから、**「主体が `OP` だから LLM は関係ない」とは言えません**。
道具の出力の「打ち切り:」に `depth` があるかを確かめ、道筋の奥の、解析器が降りなかった関数を自分で読みます。

### 確認問題 14-3

`receiver` は、属性を読む（または属性に代入する）とき、その道筋が「属性 3 段以上」か「ただの変数から始まらない（呼び出しの結果・添字から始まる）」ために値の表のキーにならず、しかもほかの方法（モジュールやクラスの属性、オブジェクトの記録 `fields` など）でも値が見つからなかったときに付きます。
代入の場合は、値を記録せずに `receiver` を立てます。
`self.client` は、変数 `self` から属性 1 段の道筋なので、値の表のキーになります。
だから、`self.client` を読む所で `receiver` が付くことはありません（値が見つからなければ `unresolved` になります）。
受け手の型が分からないことそのものでは、`receiver` は付きません。

### 確認問題 14-4

- 判定で読む欄（値の側）: `prin`・`prov`・`prov_reasons`・`roots`・`shape`（slot ごと）、`resolution`・`resolution_reasons`（効果ごと）、`opaque_reasons`・`cap_hits`（ユニットごと）。
- 判定で読まない欄（ゲートの側）: `gate`・`gate_occ`・`gate_occ_by_effect`・`gate_verdict_counts`・`req_occ`・`req_val`・`grades` など。

ゲートの側の欄に出る `"req": "MODEL"` は、主体の `MODEL` とは**意味が違います**。
`req` は要求束（`MODEL < OP < USER`）の値で、「その効果を通すのに誰の許しが要るか」を表します。
ゲートが無ければ一番下の `MODEL` になるので、`"req": "MODEL"` は「ゲートが無い」という意味です。
主体の順序（`USER ⊑ OP ⊑ MODEL`）とは向きも意味も違い、仕様書と実装は 2 つを別物として、変換もしないと決めています（`authgap/ir.py:6-8`、`:79-93`、`AUTHGAP_BRIEF_v3.md:191-192`）。


---

<a id="ad-4-5"></a>
## 第 15 章 呼び出しをたどる — 深さ・解決・受け手の型 の答え

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
「解析器の結果」はその走査の出力です。
「人の判定」の答えは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）と決定（D67・D68・D70）に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

### 演習 15-1（深さの範囲を読む）

**(1) 深さ**

| 関数 | 深さ |
|---|---|
| `show_report`（本体） | 0 |
| `g1` | 1 |
| `g2` | 2 |
| `g3` | 3 |
| `g4` | 4 |
| `g5` | 5 |
| `g6` | 6 |

**(2) 読む範囲**

- 解析器が中身を読むのは、深さ 0〜4 の `show_report`・`g1`・`g2`・`g3`・`g4` です。
- `g4`（深さ 4）の 19 行で `g5` を呼ぶところで、降りた先の深さが 4 + 1 = 5 > 4 になるので、降りません。
- 「深さ 4 の外」にあるのは `g5`（深さ 5）と `g6`（深さ 6）です。

**(3) 解析器の出力（走査の結果）**

- `effects`: **0 件**。14 行の `os.remove` は深さ 5 の関数の中、10 行の `shutil.rmtree` は深さ 6 の関数の中で、どちらも読まれていません。深さ 0〜4 の関数には、効果がありません。
- `cap_hits`: `["depth"]`。`opaque_reasons` は `["depth"]` でした。
- D1 の矛: **無し**（行が 1 本も無い）。

このユニットは「D1 を明示していて、D1 への矛が無い」ので、見落としの抜き取りの対象になりえます。

**(4) 人の判定**

- `outcome` は「**見落とし（深さ 4 の外）**」です（D68 の 2）。主の見落としの数には入れず、別に数えて併記します。
- 深さ 4 の中（`show_report`〜`g4`）には反する動作が無く、深さ 4 の外（`g5`）にだけあるので、手引きの下書き 18.3 の「深さ 4 の中に反する動作が無く、深さ 4 の外にだけあるなら『見落とし（深さ 4 の外）』」に当たります。
- `g6` の中まで探しに行く必要は**ありません**（「深さ 4 より奥を探しに行く必要はない」）。たまたま目に入ったなら、`note` に書いておきます。
- `cause` の欄の書き方は、手引きの下書きに「深さ 4 の外」の件について明記がありません。v4 の R04・R05（D68 の前の判定）は cause を「深さ」にしました。
- 根拠の例: `server.py:36 → :31 → :27 → :23 → :19 → :14 os.remove（g5、深さ 5）。条件なし`。

**(5) `g4` の本体に `os.remove(p + ".lock")` があったら**

- 解析器は深さ 4 の関数の中身を読むので、`g4` の `os.remove` は効果として**出ます**（鎖 `["g1", "g2", "g3", "g4"]`、深さ 4）。`os.remove` は sink なので、降りる必要がありません。
- D1 への矛（理由 `fs_write`）が付きます。`cap_hits` は、`g4` から `g5` を呼ぶところで止まるので、`["depth"]` のままです。
- 本書の作業用の場所で、この形に書き換えて走査し、そのとおりの出力（`FS_WRITE os.remove`、鎖 `['g1', 'g2', 'g3', 'g4']`、`contradiction:D1`）を確かめました。
- このユニットには D1 の矛があるので、**見落としの抜き取りの対象から外れます**（対象は「矛が 1 件も無いユニット」）。代わりに、矛の抜き取りに選ばれたら、手順 A〜H で判定します。届く（毎回、条件なし）、D1 に反する（ファイルを消す）ので、正の候補です。

### 演習 15-2（`witness_chain` から深さと道順を読む）

**(1)** 鎖の長さは 3（`Repo.save`・`Repo._flush`・`atomic_write`）なので、**深さ 3** です。

**(2)** 手順 D で開く順番:

1. `server.py` の 15 行（ツール `get_item` の定義）を開く。
2. `entry_lineno` の **`server.py` の 17 行**を見る。ここで `repo.save(...)` を呼んでいるはずです（鎖の 1 番目 `Repo.save`）。
3. `store.py` の `Repo.save` を開き、その中で `self._flush(...)` を呼ぶ行を探す（鎖の 2 番目）。
4. `Repo._flush` を開き、その中で `atomic_write(...)` を呼ぶ行を探す（鎖の 3 番目）。
5. `atomic_write` の中の、**`store.py` の 9 行**（`lineno`。`os.replace`）に着く。

各段で、呼び出しが本当にその関数に届くか（受け手 `repo` は何か）、途中に条件や先に抜ける `return` が無いかも見ます。
なお、この作例では `repo` はモジュールの一番上で `repo = Repo("/var/app/data")` と作ったオブジェクトです。

**(3)** 2 つ目の鎖は要素が 5 つですが、`<indirect>` は深さを消費しない印なので除きます。`_bg`・`Repo.save`・`Repo._flush`・`atomic_write` の 4 つで、**深さ 4** です。
`<indirect>` は、`INDIRECT` 表の形（別のスレッドやプロセスで関数を動かす書き方）を通ったことを示します。`entry_lineno` の 18 行で、`_bg` を直接呼ばずに、`asyncio.to_thread(_bg, key)` や `threading.Thread(target=_bg, ...)` のような形で動かしていると考えられます（作例の 18 行は `await asyncio.to_thread(_bg, key)` です）。

**(4)** 深さの上限が 3 なら:

- 1 つ目（深さ 3）: `Repo._flush`（深さ 2）から `atomic_write` に降りるとき、2 + 1 = 3 で 3 を超えないので降ります。深さ 3 の関数の中の `os.replace` は sink なので**出ます**。
- 2 つ目（深さ 4）: `Repo._flush`（深さ 3）から `atomic_write` に降りるとき、3 + 1 = 4 > 3 で降りません。**出ません**。
- 本書の作業用の場所で、深さの設定だけを 3 に変えて走らせ（`Options(max_depth=3)`）、1 つ目の道筋だけが出て、`cap_hits` が `["depth"]` になることを確かめました。深さ 4（凍結の設定）では 2 本とも出て、`cap_hits` は空でした。

### 演習 15-3（デコレータの中の書き込み）

**(1)** 走ります。
デコレータは下から順に掛かるので、まず `audit(get_weather)` で wrapper ができ、次に `mcp.tool(...)` が**その wrapper を**ツールとして登録します（[第 9 章](ch09.md) 9.8 の形 1）。
ツールが呼ばれると wrapper が走り、14 行で本体を呼ぶ前に、12〜13 行でログファイルに 1 行追記します。毎回、条件はありません。

**(2)** 解析器は 12 行の書き込みを**出しません**。任意のデコレータの wrapper を呼び出しとしてたどらないからです（O42 の RC5、U16）。
走査の結果、このツールの効果は 21 行の `requests.get`（`NET`）の 1 件だけで、D1 に対しては**内**（GET は安全なメソッド。行に `contradiction` の注記は無し）でした。
`D_kind.explicit` は `["readOnlyHint"]` で、D1 への矛が無いので、見落としの抜き取りの対象になりえます。

**(3)**

- `outcome`: **見落とし**。手引きの下書き 15.1 は、D1 の問い「環境を変えるか」で、ファイルの書き込み（ログを含む）を「反する」としています（原理 1-i-b）。12 行は `open(..., "a")` でファイルに追記するので、D1 に反します。解析器は矛も不も出していません。
- `cause`: **その他**（デコレータの wrapper の中）。
- 書き込み先の種類のラベル: **ログ**（D67 の 1 のラベル）。
- 条件の種類: なし（毎回）。
- wrapper の中の書き込みを「深さいくつ」と数えるかは、手順書・手引きの下書きに決まりがありません（未決）。`note` に自分の数え方を書いておきます。
- 根拠の例: `server.py:18-20 @mcp.tool の下の @audit → server.py:11 wrapper → server.py:12 open("/var/log/tool_audit.log", "a")。登録されるのは wrapper なので、毎回の呼び出しで走る`。

（出典: `docs/drafts/final_judging_guide_draft.md:309-315`（15.1）、`:473-475`（見落としの原因）、`docs/decisions.md:3767-3769`（D67 の 1 のラベル））

**(4)** `@audit` が上、`@mcp.tool(...)` が下なら、まず `mcp.tool(...)` が**本体の `get_weather` を**登録し、そのまま返します。次に `audit` が包みますが、包んだものは `get_weather` という名前に入るだけで、サーバに登録されたのは本体です。
ツールが呼ばれても、wrapper は**走りません**（[第 9 章](ch09.md) 9.8 の形 2。ただし MCP の SDK の `tool()` が関数をそのまま返すことは、本書では SDK のコードで確かめていない。[第 9 章](ch09.md)の確かめ方は、同じ働きの登録のデコレータを自作して動かしたもの）。
この形なら、12 行の書き込みはツールの呼び出しでは届かないので、見落としにはなりません。

### 演習 15-4（取り違えを見抜く）

**(1)** `entry_lineno` の **`server.py` の 22 行**で `_walk(graph, start)` を呼びます（鎖の 1 番目 `_walk`、深さ 1）。
`_walk` の中で、鎖の 2 番目 `Cache.set` を呼んでいる（と解析器が考えた）のは、**`server.py` の 8 行の `set()`** です。`_walk` の中に `set` という名前の呼び出しはこれしかありません。

**(2)** **本当は `Cache.set` ではありません。**
8 行の `set()` は、素の名前の呼び出しで、Python の組み込みの `set`（空の集合を作る）です。受け手のオブジェクトも無く、`Cache` のオブジェクトを作る行も `_walk` の中にありません。
確かめ方:

- 受け手の型（その変数に何が入っているか）を見る。`seen = set()` の `seen` は組み込みの集合で、14 行の `seen.add(node)` も組み込みの集合の `add` です。
- エディタの「定義へ移動」が `Cache.set` に飛んでも信じない（名前で当てていることがある）。
- `Cache.set` を本当に呼んでいる箇所を grep で全部探す（例: `grep -rn '\.set(' <木> --include='*.py'`）。このツールから届く別の道が無いことを確かめる。

**(3)** 判定は **誤**、原因は **E3**（名前だけの解決の誤り。呼び出し先の取り違え）です。
`evidence` の例: `server.py:22 _walk(...) → server.py:8 seen = set()。組み込みの set を解析器が末尾名で cache.py の Cache.set に結んだ。cache.py:9 の open(self.path, "w") はこのツールから届かない（grep で Cache.set の呼び出し元を確かめ、この木では <呼び出し元> だけ）`。
v4 の rails-lens（M04・M05）と同じ形です。

**(4)** D1（`readOnlyHint: true`）は、ファイルの書き込み（`FS_WRITE`）を、確度によらずすべて矛にするからです（判定表。[第 17 章](ch17.md)）。
`opaque(unresolved)` は矛を消す印ではなく、「この道筋は確かではないので、疑って確かめよ」という合図です。
なお、この作例の確度が `opaque` になったのは、`set()` に実引数が無く、書き込み先 `self.path` の値が分からなかったためです。15.7 節で見たとおり、素の名前の呼び出しをメソッドに結んだときは「末尾名だけ」の印が付かないので、書き込み先が定数なら確度は `resolved` のまま矛になります。

### 確認問題 15-1

- 候補が 1 つなら、その関数に**降ります**（効果を落とさないため。D17 の改訂）。
- 属性の呼び出し（`x.f()`）を、受け手の型の裏付けなしに末尾名だけで決めたときは、その先の効果の確度に **`opaque(unresolved)`** を合流します。ユニットの `opaque_reasons` にも `unresolved` が付きます。ただし、素の名前の呼び出し（`set()`）を木の中のメソッドに結んだときは、この印が付かないことがあります（15.7 節。本書の作例で確認）。
- 候補が 2 つ以上なら、**降りません**。戻り値は `opaque(unresolved)` になり、その呼び出しは `unresolved_in_tree_calls` に名前・ファイル・行・候補の数として記録されます（受け手が木の外の型だと分かっているときを除く）。この欄は判定には使いません（D61 の G5）。

### 確認問題 15-2

言えません。`cap_hits` に出るのは `depth` と `summary_cap` だけです。ほかに次を見ます。

- `opaque_reasons` の `recursion`: 再帰で 2 回目に降りなかった（`cap_hits` には入らない）。
- `unresolved_in_tree_calls`: 名前が木の中の定義に当たるのに、候補が 2 つ以上で降りなかった呼び出し。
- `opaque_reasons` の `unresolved`・`receiver`: どこかで呼び出し先や値を解決できなかった。
- ユニットの `notes` の `TRUNCATED(...)`（抜き取りの出力では `truncated`）: ユニットの解析そのものが打ち切られた（第 18・19 章）。

さらに、デコレータの wrapper・`@property`・`__enter__`・`__call__`・`lambda` のように、解析器が最初からたどらない形は、**どの欄にも印が出ません**。見落としの判定では、人がこれらを読みます（15.4 節）。

### 確認問題 15-3

D67 の 2 と手引きの下書き 14.4 に沿って決めます。設定ファイルの作成は D1 に反する動作（ファイルの作成）です。

| 場合 | 到達するか | 判定 | 補足 |
|---|---|---|---|
| (1) lifespan の `startup` の中で必ず済ませる | 到達しない | **誤、E1** | どの起動方法でも、ツールの受付より前に走る。ただし、lifespan が条件つき・失敗しうる、またはどこかで `_client = None` に戻すなら、届くので「到達する」になる（grep で確かめる） |
| (2) `main()` の中でだけ済ませる | 到達する | **正**（正になりうる） | `fastmcp run file.py:mcp` などで `main()` を通らずに起動できる。条件の種類は「**起動の方法**」（D68 の 1） |
| (3) どちらも無い | 到達する | **正** | 最初のツール呼び出しで `_connect()` が走る。条件の種類は「**初回**」（D68 の 1） |

どこで済ませるかを読み切れなければ、**不明**です。

### 確認問題 15-4

- 木の外のライブラリの中は読みません。**ライブラリの関数そのもの**が環境を変える（ファイルを書く・消す、DB を変える、相手の状態を変える通信をする、プロセスを起動する）ときに、呼んでいれば違反の候補として数えます。例: `requests.put`、`sqlite3` の `execute("DELETE …")`、`shutil.rmtree`。
- これは、解析器の **sink 表**と同じ考え方です。解析器も、木の外のライブラリには降りず、作用が分かっている関数だけを sink 表で効果として数えます。
- 人が気づけて解析器が気づけないのは、**sink 表に載っていない**ライブラリの関数の作用です。例: `tempfile.mkstemp()`（一時ファイルを作る）、`logging.FileHandler`・loguru の `logger.add(<パス>)`（ファイルへのログ）、`wave.open(..., "wb")`。解析器が何も出していなければ、見落としの原因は「語彙」です。
- もう 1 つ、木の外のライブラリが木の中の関数を呼び戻す形（コールバック。v4 の pronote）も、解析器には見えません。人はコールバックの中を読めますが、ライブラリが本当に呼ぶかを決められなければ「不明」にします。


---

<a id="ad-4-6"></a>
## 第 16 章 宣言を読む の答え

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
v4 の実物は `evidence/scan_v2_v4_run1/` の manifest と `contradictions.json` で確かめました。v4 の数字は論文に使いません（D66 の 5）。
「対象になりうるか」などの答えは、手順書と手引きの下書き（未承認）の規則に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

### 演習 16-1（manifest の `D_kind` を読む）

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
- (イ): **対象になりえます。** `explicit` に `readOnlyHint` があり（D1 を明示）、行の注記に `contradiction` で始まるものが無い（D1 への矛が無い）からです。実際に抜き取られるかは、seed（乱数の種）を決めた抜き取りで決まります（[第 47 章](ch47.md)）。

### 演習 16-2（`annotations` から `D_kind` を作る）

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

### 演習 16-3（`r_malformed` の主の分母）

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

### 演習 16-4（snake_case と版を予想する）

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

### 確認問題 16-1

**D1 だけ**として扱われます。

- SDK の説明文は、`destructiveHint` について「この項目は `readOnlyHint` が false のときだけ意味を持つ」と書いています。読むだけのツールに「壊すか」を問う意味は無く、D1 の判定表が書き込み全般をすでに見ています。
- `D_kind` では、`readOnlyHint: True` があると、`destructiveHint: False` は `explicit` に入らず `present_no_bound` に入ります。D2 は `explicit` の `destructiveHint` で当てるので、当たりません。上界も `readOnlyHint: true` の `{FS_READ, NET}` だけです。
- 実物では、gemini の `gemini_prompt`・`gemini_list_models` と bugasura の `bugasura_find_project_by_name` がこの形で、どれも D2 は当たっていません。

### 確認問題 16-2

**D3 は当たりません**（`explicit` だけからは、当たるとは言えません）。
`explicit` の `openWorldHint` は、`openWorldHint: true`（外の世界と関わる）を明示したことを表します。D3（`openWorldHint: false`）とは逆の申告です。
D3 が当たるかどうかは、`D_kind` の **`closed_world`** の欄で分かります。`closed_world: true` があれば D3 が当たり、欄が無ければ（false なら）当たりません。
このツールは `explicit` に `openWorldHint` があるので `openWorldHint: true` で、`closed_world` は立ちえません。当たる宣言は D1 だけです（bugasura の `bugasura_find_project_by_name`・gemini の `gemini_prompt` と同じ形）。

### 確認問題 16-3

- **探索的にしていた理由**（D56）: D3・D4 の規則は、開発用のデータ（v2）の結果（run11 の件数）を見た後で作りました。結果を見て作った規則で同じデータを測ると、甘い結果になりうるので、D1・D2 と分けて「探索的」としました。
- **理由が無くなったわけ**（D62）: D60 で、論文の評価は学生が v2・v3 を含まない新しいデータで行うと決まりました。D3・D4 の規則も解析器の凍結に入り、評価のデータを見る前に固定されています。新しいデータから見れば、D1〜D4 の規則はどれも「見る前に決まっている」ので、「先に決めたか」の差がありません。「結果を見た後に作った」は、別の新しいデータで確かめれば解消する事情で、主と副を分ける理由にはなりません。
- **変えなかったもの**: 判定表（§7.3・§7.4）の規則、件数、古い記録（D56、逸脱 #19、run13〜run20 の表の「探索的」の語）、仕様書。変えたのは呼び方（位置づけ）と、集計の見出し・説明文の語、添削の範囲（D3・D4 の判定を探す回を足した）だけです。逸脱 #24 として記録されています。

### 確認問題 16-4

- **未決だった理由**: D70 の 4 と手順書は、M_d を「宣言 d を明示した（`D_kind.explicit`）ユニットを 1 つ以上持つ木」と書いていました。D1・D2 はこれで正しく数えられますが、D3 は `closed_world`、D4 は `idempotent` の欄に表れ、`explicit` には入りません。D3・D4 をどの欄で数えるかを、どの文書も決めていませんでした。
- **文字どおりに数えると**:
  - D3: `explicit` の `openWorldHint` は `openWorldHint: true` なので、**D3 とは逆の申告をした木**を数えてしまいます。v4 では、文字どおりの数え方で 39 木、本当の D3（`closed_world` を持つ木）で 40 木と数は近いのに、重なりは 22 木だけでした。
  - D4: `idempotentHint` は決して `explicit` に入らないので、**M_d がいつも 0** になり、割合が計算できません（v4 でも 0 木。`idempotent` を持つ木は 23）。
- **封の前に決める理由**: 分母を結果を見てから選べると、都合のよい割合が出る数え方を選べてしまいます。この研究は分母を値を見る前に決めて書き残す約束をしています（CLAUDE.md の規則 3、事前登録 §2.10 の「値を見てから主分母を替えない」）。また、決まらないまま集計すると、文字どおりに数えて意味の無い値を出すか、事前登録に無い数え方を黙って使うかのどちらかになります。どちらも避けるため、未決として記録し（[第 46 章](ch46.md)の一覧）、封の前に学生が決めることにしました。
- **D73 の 3 での決定**（2026-10-03）: M_d は矛の判定と同じ条件で数える。D1 = `D_kind.explicit` に `readOnlyHint`、D2 = `explicit` に `destructiveHint`、D3 = `D_kind.closed_world`、D4 = `D_kind.idempotent`。D1・D2 は変わらない（`docs/decisions.md:4016-4018`）。v4 の数え方なら、D3 は 40 木、D4 は 23 木になります（v4 の数は論文に使わない）。

（2026-10-03 の D73 で決まったので答えを直した）


---

<a id="ad-4-7"></a>
## 第 17 章 食い違いの判定 — 4 つの原理と判定表 の答え

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめた版）で走査して、結果を確かめました（2026-10-01）。
「解析器の答え」はその走査の出力です。
作例の DB の site は、manifest では `psycopg.Cursor.execute` と表示されます（受け手の型の読み違いの表示。kind は `DB` のままで、判定には影響しない）。
「人の判定」の答えは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）と手順書に沿った考え方の例で、最終評価の判定の正解ではありません。
最終評価の判定は学生 1 人が行い、AI（LLM）には判定させません（AI は、コードについての事実を調べる補助にだけ使えます。D70 の 3）。

### 演習 17-1（D1 の判定表を引く）

**(1) 解析器の答え（走査の結果）**

| 効果 | 注記 | 答え | 判定表の行 |
|---|---|---|---|
| (ア) `open("/tmp/audit.log", "a")` | `contradiction:D1`・`contradiction_reason:D1:fs_write` | **矛** | FS_WRITE はすべて矛（`docs/contradiction_principles.md:166`） |
| (イ) `PRAGMA foreign_keys=ON` | なし | 内 | 接続単位（`:169`） |
| (ウ) `PRAGMA journal_mode=WAL` | `contradiction:D1`・`contradiction_reason:D1:db_persistent` | **矛** | DB に残る設定（1-i-b、`:168`） |
| (エ) `requests.post(定数, ...)` | `contradiction_unknown:D1:net_post` | **不** | `POST`（`:175`） |
| (オ) `subprocess.run(["helm", "list"], ...)` | `contradiction_unknown:D1:spawn_command` | **不** | コマンドが定数（`:165`） |
| (カ) `subprocess.run(cmd, shell=True, ...)`（`cmd` は引数） | `contradiction:D1`・`contradiction_reason:D1:spawn_model` | **矛** | コマンドを LLM が選べる（3-a、`:165`） |
| (キ) `"SELECT ... '" + title + "'"`（`title` は引数） | `contradiction:D1`・`contradiction_reason:D1:db_model_sql` | **矛** | SQL を LLM が選べる（3-a、§9.4 の 2、`:318-335`） |
| (ク) `ATTACH DATABASE 'other.db' AS other` | `contradiction_unknown:D1:db_unknown_statement` | **不** | 分類に無い先頭の語（`:171`、`:245`） |

(キ) は、先頭が `SELECT` なので一見読むだけですが、`title` は文字列の連結だけで文に入るので「選べる」（主体 `MODEL`・確度 `resolved`）です。
LLM が `title` に引用符と別の文を入れれば、`DELETE` などを書き足せます。
だから、能力として読む原理 3-a で矛です。

**(2) 不になるものについて、人が調べること（考え方の例）**

- **(エ) `POST`**: 相手の API の意味を調べます（手順書 `docs/final_evaluation_procedure.md:1001`）。相手の文書や API の名前（この作例では `/query`）から、「作成・更新・削除」なら反する、「照会」（検索の API・RPC の読み取り）なら反しない、分からなければ不明です。名前だけで決めず、文書で確かめられるなら確かめます。
- **(オ) 定数のコマンド**: そのコマンドが実際に何をするかを調べます（同 `:984`）。`helm` の文書で `list` のサブコマンドが何をするかを確かめ、一覧を表示するだけで何も変えないと確かめられれば反しない、環境を変えるなら反する、分からなければ不明です。
- **(ク) `ATTACH`**: 判定表は `ATTACH` を「無ければファイルを作る」として分類の外（不）に置いています（`docs/contradiction_principles.md:245`）。人は、`other.db` が呼び出しの前からありうるか、無いときにファイルが作られて呼び出しの後に残るかを調べ、D1 の問い「呼び出しの後に残る何かを変えるか」で決めます。決められなければ不明です。

**(3) ログの書き込みを「反する」と答える理由**

判定の基準は、採った原理を字義どおりに当てることです（手引きの下書き `:54-59`）。
原理 1-i-b により、呼び出しを越えて残るものはすべて環境で、ログファイルに 1 行増えれば、それは残ります。
だから「たかがログ」と感じても、宣言に反します（届くなら正）。
軽い・重いの違いは、正誤ではなく、正の件に付ける**書き込み先の種類のラベル**（この例ならログ）で表します（D67 の 1。第 43・51 章）。

### 演習 17-2（D2 の書き出し）

**(1)** 解析器の答えは**矛**、理由は `fs_writeout_model_path` です（走査で `contradiction:D2`・`contradiction_reason:D2:fs_writeout_model_path` を確かめた）。
`open(path, "w")` は書き出し（`_fs_class` の `writeout`）で、書き先 `path` を LLM が選べます。
原理 3-a により、LLM は既存のファイルを指して上書きできる（壊せる）ので、「追加の更新だけ」の約束に反することが**できる**、と読みます（判定表 `docs/contradiction_principles.md:187`）。

**(2)** 解析器の答えは**不**、理由は `fs_writeout` です（走査で `contradiction_unknown:D2:fs_writeout` を確かめた）。
書き先は定数で、LLM は決めません。
新しく作るなら足すだけ、すでにあれば上書きで、どちらかは動かすまで分からないので、原理 2-a により不です。

**(3)** 解析器の答えは**矛**、理由は `fs_writeout_model_path` です（走査で確かめた）。
文字列の連結は解析器がモデリングしている操作なので、確度は `resolved` のままで、「選べる」です。
LLM は `name` を変えることで、`/srv/out/` の下の既存のファイルを指せます。

**(4)** 解析器の答えは**内**で、判定の注記は出ません（走査で確かめた）。
`'a'`（追記）は前の中身を壊さない「足す型」なので、書き先を LLM が選べても、D2 では内です（判定表 `:185`）。

**(5)** 人は、書き先 `/tmp/report.txt` に**呼び出しの前からファイルがありうるか**を調べます（手順書 `:1008`）。
この作例では、毎回同じ名前のファイルに `'w'` で書きます。
2 回目の呼び出しから見ると、1 回目が書いたファイルは「呼び出しの前からあったもの」で、それを上書きします。
だから、手順書の「毎回同じファイルを上書きするなら反する」に当たり、「反する」と考えられます。
呼び出しごとに新しい名前（時刻や乱数を入れた名前など）で書くなら、反しません。
どちらとも決められなければ、不明です。
（この作例は解析器が不にした組なので、最終評価では、不の中身の判定（手引きの 18A 節）の対象として、違反 / 違反でない / 不明を付ける形になります。）

### 演習 17-3（D4 の `INSERT`）

**(1)** 解析器の答えは**不**、理由は `db_nonidempotent_statement` です（走査で `contradiction_unknown:D4:db_nonidempotent_statement` を確かめた）。
`INSERT` が冪等かどうかは、表に一意制約があるか（2 回目が失敗・無視されるか、行が増えるか）で決まります。
解析器はスキーマ（表の定義）を見ないので、静的には決まらず、原理 2-a で不です（判定表 `docs/contradiction_principles.md:222`）。
D4 には原理 3 を当てないので、LLM の値かどうかも関係しません。

**(2)**（考え方の例）`id` は `AUTOINCREMENT` で毎回新しい番号になり、`msg` には一意制約がありません。
同じ `msg` で 2 回呼ぶと、行が 2 つになります。
2 回目が 1 回目の後の状態をさらに変えるので、D4 に**反する**と考えられます（手順書 `:1045`「行が増えるなら反する」）。
ほかの問い（このツールの呼び出しで本当に届くか）も、手順どおりに確かめます。

**(3)** 解析器の答えは、(1) と同じく**不**（`db_nonidempotent_statement`）です（走査で確かめた。解析器は先頭の語 `INSERT` だけを見る）。
人の判定（考え方の例）では、`name` が主キー（一意）で、`OR IGNORE` により同じ `name` の 2 回目は無視されます。
2 回目は状態を変えないので、D4 に**反しない**と考えられます（手順書 `:1045`「一意制約で 2 回目が失敗・無視されるなら反しない」）。

**(4)** 走査で確かめた結果は次のとおりです。

| ツールの宣言 | 解析器の答え |
|---|---|
| `readOnlyHint=True` | D1 の**矛**（`db_modify`）。`INSERT` はデータの変更だから |
| `destructiveHint=False, idempotentHint=True` | D2 は**内**（`INSERT` は足すだけ）、D4 は**不**（`db_nonidempotent_statement`） |

同じ `INSERT` でも、宣言によって矛・内・不の 3 通りに分かれます。
なお、`readOnlyHint=True, idempotentHint=True` の両方を書いたツールでは、D4 は当てず（`readOnlyHint: true` があるため）、D1 の矛だけが出ました。

### 演習 17-4（定数の外部ホストへの `GET` を D1 と D3 で）

**(1)** 走査で確かめた結果は次のとおりです。

| ツール | 宣言 | 解析器の答え |
|---|---|---|
| A | `readOnlyHint=True` | D1 は**内**（判定の注記なし） |
| B | `openWorldHint=False` | D3 の**矛**（`contradiction:D3`・`contradiction_reason:D3:net_external_host`） |
| C | `readOnlyHint=True, openWorldHint=False` | D1 は**内**、D3 の**矛**（`net_external_host`） |

**(2)** `readOnlyHint` が問うのは「変えるか」、`openWorldHint` が問うのは「外と関わるか」で、別の軸です（原理 1-ii の理由。`docs/contradiction_principles.md:138`）。
`GET` は HTTP の約束（RFC 9110）で安全なメソッドで、相手を変えることを頼まないので、D1（変えない）には反しません。
一方、宛先 `api.example.com` は定数の外部ホストなので、外の世界と関わり、D3（関わる範囲が閉じている）には反します（`:207`）。
仕様自身も、Web 検索のツールを「読み取りで、かつ開いた世界と関わる」例として挙げています（`:29-30`）。

**(3)** 解析器の答えは**内**です（走査で確かめた）。
`127.0.0.1` は loopback（`127.0.0.0/8`）で、解析器の手元の網に入るからです（`authgap/dparse.py:293-301`、判定表 `:206`）。

**(4)** 解析器の答えは**不**、理由は `net_host_unknown` です（走査で `contradiction_unknown:D3:net_host_unknown` を確かめた）。
宛先は運用者が起動のときに渡す環境変数で決まり、コードからは決まらないからです（判定表 `:209`、原理 2-a）。
人の判定（考え方の例）では、手順書の「宛先が運用者の設定で決まる」の行に従い、設定の既定値や文書を見ます（手順書 `:1030`）。
この作例の既定値は外部のホスト `https://api.example.com` なので、文書が別のことを言っていなければ、「外部を想定している」として**反する**と考えられます。
文書でローカルの相手を想定していれば反しない、分からなければ不明です。
（D3 の不は、最終評価では件数と理由だけを数え、中身の判定はしません。D69 の 4。この問いは、矛の判定や見落としの判定で同じ形に出会ったときの考え方の練習です。）

### 確認問題 17-1

解析器の答えは**不**で、理由は `net_post` です。
2 つの原理から来ています。
原理 1-ii-b（通信相手の状態も環境に含める）により、相手を変えるかどうかを判定する必要が生まれます。
けれども `POST` が相手を変えるかは相手のサーバの意味しだいで（検索の問い合わせにも `POST` を使う）、静的には決まらないので、原理 2-a により不です（`docs/contradiction_principles.md:55-56, 175`）。
人の判定では、**相手の API の意味**を調べます。
相手の文書や API の名前から「作成・更新・削除」なら反する、「照会」なら反しない、分からなければ不明です（手順書 `docs/final_evaluation_procedure.md:1001`）。

### 確認問題 17-2

冪等性は「**同じ引数で**繰り返したとき、2 回目以降に追加の効果が無い」という性質です。
LLM が SQL やコマンドを選べるとしても、繰り返しの間はずっと同じ値で、その値が冪等かどうかはその意味によります。
引数が取りうる値の範囲（能力）は関係しないので、D4 には原理 3 を当てません（`docs/contradiction_principles.md:153-155`）。

`idempotentHint=True` のツールが引数を連結した SQL を実行すると、解析器の答えは**不**で、理由は `db_sql_model` です（`authgap/dparse.py:538-539`。演習の作例 `"SELECT * FROM t WHERE " + sql` で `contradiction_unknown:D4:db_sql_model` を確かめた）。
同じ文を `readOnlyHint=True` のツールが実行すると、連結が「選べる」（主体 `MODEL`・確度 `resolved`）なら、注入で任意の文を書けるので**矛**、理由は `db_model_sql` です（§9.4 の 2）。
連結の途中にモデリングしていない関数が入って「流れ込む」だけなら、接頭辞が変更の文でない限り**不**（`db_sql_model_opaque`）です。

### 確認問題 17-3

**D1 の不 171 → 76**: 1-ii-a（リモートの状態を含めない）では、D1・D2 の `net_` で始まる理由を内として扱います。
v4 の D1 の不の組のうち、NET の理由だけを持つ組が 95 組（`net_post` 78、`net_method_unknown` 17）あり、それが内に移りました（171 − 95 = 76）。

**D1 の矛 323 → 322**: D1 の矛の組のうち、`net_method_model` の理由だけを持つ 1 組が、内に移りました。

**1-i-a の行が同じだった理由**: 1-i-a は理由 `db_persistent` を内として扱います。
v4 で D1 の `db_persistent` の理由を持つ 15 組は、どれも `db_modify` の理由も持っていたので、`db_persistent` を外しても矛のまま残りました。
D2 の不の `db_persistent` の 2 組も、`db_modify` で矛になっている組の中にあったので、件数は動きませんでした。
1 つの組が複数の理由を持ちうることが、ここに表れています。

（上の組の動きは、本書の執筆時に `scripts/contradiction_by_decl.py` の数え方で v4 の manifest から数えて確かめた。表の値は `evidence/population_v4/contradiction_by_decl_v4_run1.md:56-66`。v4 の数は論文には使わない。D66 の 5）

### 確認問題 17-4

**違い**: 解析器の「不」は、「プログラムを動かさず、木の中のコードだけからは決められない」という意味です。
人の「不明」は、「人が原ソースを読み、調べられる範囲で調べても決められない」という意味です。
人は、解析器が読まないもの（相手の API の文書、起動するプログラムの中身、ファイルが前からありうるか、表のスキーマなど）を調べてよいので、解析器の不の多くは、人には決められます。

**不明にしてよいとき**: 調べれば分かるものを不明にしてはいけません。
目安は、**20〜30 分調べても決められなければ不明**にし、理由を書くことです（手引きの下書き `:534-535`）。
典型は、書き先・宛先・コマンドが木の外のライブラリの戻り値や実行時の外部の状態で決まり読み切れないとき、`POST` の先の意味が文書にもコードにも無いとき、起動の方法・初期化の場所が読み切れないとき、動的な呼び出しで呼び出し先が決まらないとき、です（同 `:537-542`）。

**答えの言葉**:

| 場面 | 人の答え |
|---|---|
| 矛の判定 | 正 / 誤 / 不明 |
| 不の中身の判定 | 違反 / 違反でない / 不明 |
| 見落としの判定 | 反する動作は無い / 解析器が不として出している / 見落とし / 見落とし（深さ 4 の外）/ 不明 |

（出典: `docs/final_evaluation_procedure.md:100-101`、`docs/drafts/final_judging_guide_draft.md:527-531`、`docs/drafts/prereg_2_12_draft.md:119`）


---

<a id="ad-4-8"></a>
## 第 18 章 出力の読み方 — manifest・組・summary の答え

この章の演習の作例（`archive_report`、`final-acme__notes-mcp`、`final-acme__big-mcp` など）は、説明のために本記録者（AI）が作ったもので、実在の木ではありません。
実物の数（v4 の 481 行、2,707 行など）は、`evidence/scan_v2_v4_run1/` の `summary.json`・`contradictions.json`・manifest を本記録者が読んで確かめたものです。v4 の数字は論文に使いません（D66 の 5）。
答えは、手順書と手引きの下書き（未承認）の規則に沿った考え方の例です。最終評価の判定は学生 1 人が行います（D70 の 3）。

### 演習 18-1（行から組を数える）

**(1) 組と、それぞれの答え**

組は (木, ユニット, site, kind, 宣言) です。このツールの site・kind は `builtins.open`・`FS_WRITE` と `requests.post`・`NET` の 2 通りで、宣言は D2 と D4 の 2 つなので、組は 2 × 2 = **4 組**です。

| 組 | 組の中の行と注記 | 組の答え |
|---|---|---|
| (`archive_report`, `builtins.open`, `FS_WRITE`, D2) | 行 1 に D2 の矛、行 2 に D2 の不、行 3 に D2 の注記なし | **矛**（矛の行が 1 つでもあれば矛） |
| (`archive_report`, `builtins.open`, `FS_WRITE`, D4) | 行 3 に D4 の矛。行 1・2 には D4 の注記なし | **矛** |
| (`archive_report`, `requests.post`, `NET`, D2) | 行 4・5 に D2 の不 | **不**（理由 `net_post`） |
| (`archive_report`, `requests.post`, `NET`, D4) | 行 4・5 に D4 の不 | **不**（理由 `net_nonidempotent_method`） |

考え方:

- 組の答えは、組の中のどれか 1 行にでもその宣言の矛があれば矛、矛が無くて不があれば不、どちらも無ければ内です（18.8 節。`scripts/contradiction_by_decl.py:78`）。
- 行 2 は D2 の不ですが、同じ組に行 1 の矛があるので、組は矛です（ccr の `gcc_todos` と同じ形）。
- 行 3 は D2 について注記がありません。追記（`'a'`）は D2 では内だからです（[第 17 章](ch17.md)の判定表）。内は書かれません。
- 行 4 と行 5 は、同じ効果の slot 違い（`url.host` と `url.path`）なので、同じ組の 2 行です。

**(2) `contradictions.json` の行**

**1 行**だけです。

- `contradictions.json` は、`verdicts` に `CONTRADICTION` がある行だけを拾います。行 1 と行 3 がそれにあたり、どちらも (`archive_report`, `builtins.open`, `FS_WRITE`) なので、1 行にまとまります。
- `requests.post` の組は不だけなので、行は出ません。
- `declarations`: `["D2", "D4"]`（全部の位置の和）。
- `locations`: `report.py:40`（`declarations` は `["D2"]`）と `util.py:12`（`["D4"]`）の 2 つ。行 2 の `report.py:55` は不の位置なので**並びません**。
- 代表の `relpath`・`lineno`: (relpath, lineno) の対の最小なので、`report.py`・40（文字の並びで `report.py` が `util.py` より前）。

この 1 行から、組は `declarations` の数の 2 つ（D2 の組と D4 の組）できます。(1) の矛の 2 組と一致します。

**(3) 判定の対象になりうる組**

- **矛の判定（精度）**: 矛の 2 組、(`builtins.open`, `FS_WRITE`, D2) と (`builtins.open`, `FS_WRITE`, D4)。D69 は、宣言ごとに矛の出た木から抜き取り、各木から最大 3 件を選びます。D3・D4 も同じ規則です。D2 の組を判定するときは `report.py:40`、D4 の組を判定するときは `util.py:12` を開きます。
- **不の中身の判定**: D1・D2 の不の組だけが対象なので、(`requests.post`, `NET`, D2) だけです。(`requests.post`, `NET`, D4) は、D4 の不なので件数と理由を数えるだけで、判定しません（D69 の 4）。行 2 の `fs_writeout` は、組が矛なので不の組にはなりません。
- どちらも、実際に選ばれるかは抜き取りの seed で決まります。「対象になりうる」と「選ばれる」は別です。

**(4) `verdict_rows` に足す数**

`CONTRADICTION` を持つ行は行 1 と行 3 の **2 行**なので、2 を足します。
この例では、たまたま矛の組の数（2）と同じになりました。
けれども意味は違います。`verdict_rows` は行の数で、slot が 2 つある効果や、道筋が何本もある効果では、行の数は組の数よりずっと多くなります（v4 では 2,707 行に対して 481 組）。

### 演習 18-2（`declarations` に宣言が 2 つ）

**(1) 組の数**

`declarations` が `["D1", "D2"]` なので、**2 組**です。

- (`final-acme__notes-mcp`, `handle_call_tool`, `builtins.open`, `FS_WRITE`, D1)
- (`final-acme__notes-mcp`, `handle_call_tool`, `builtins.open`, `FS_WRITE`, D2)

組の数 = `declarations` の数です（18.9 節）。

**(2) 開く位置**

位置ごとの `declarations` を見て、その組の宣言を含む位置だけを開きます。

- D1 の組: `server.py:120` と `store.py:40`。
- D2 の組: `server.py:188` と `store.py:40`。

`store.py:40` は両方の組に入ります。どちらの組でも、その組の宣言の問い（D1 なら「環境を変えるか」、D2 なら「追加の更新だけか」）で別々に判定します。

**(3) 位置の数と組の数**

変わりません。位置がいくつあっても、宣言ごとに 1 組です。
複数の位置がある組は、手順 G のとおり、1 つでも「到達する かつ 宣言に反する」位置があれば正です。

**(4) D1 と D2 が並ぶユニット**

[第 16 章](ch16.md)の当て方では、D2 は「`readOnlyHint: true` が**無い**とき」だけ当て、D1 は「`readOnlyHint: true` がある」ときに当てます。
1 つの宣言の中で、この 2 つは同時に成り立ちません。だから、ふつうのデコレータで登録したツール（宣言が 1 つ）では、D1 と D2 が同じユニットに当たることはありません。

並びうるのは、**低レベルの書き方のハンドラ**（`handle_call_tool` のように、1 つのハンドラが名前で分岐して複数のツールを受け持つユニット）だと考えられます。
このとき解析器は、効果ごとに、その効果を受け持つツールの宣言で照らします（[第 16 章](ch16.md) 16.5 節の「低レベルの書き方のハンドラ」）。
ある位置は `readOnlyHint: true` のツールの分岐（D1）、別の位置は `destructiveHint: false` のツールの分岐（D2）で照らされれば、1 行に D1 と D2 が並びえます。
なお、v2・v3・v4 の `contradictions.json` には、D1 と D2 が同じ行に並んだ例はありませんでした（本書の執筆時に確かめた。並んでいたのは D2 と D3、D1 と D3 だけ）。これは作例で、仕組みの上でありうる形です。

### 演習 18-3（`verdicts` に `UNKNOWN` がある行は核の不か）

**(1) 核の答え**

| 行 | 核の答え | 根拠 |
|---|---|---|
| (ア) | 矛でも不でもない | `contradiction` で始まる注記が無い |
| (イ) | **D1 の矛**（理由 `db_modify`） | `contradiction:D1` と `contradiction_reason:D1:db_modify` |
| (ウ) | **D2 の不**（`net_post`）と **D4 の不**（`net_nonidempotent_method`） | `contradiction_unknown:` が 2 つ |
| (エ) | **D1 の不**（`spawn_model_opaque`） | `contradiction_unknown:D1:spawn_model_opaque` |

`select_manifest_only(assumed_trig)` は付録の注記で、核の答えには関係ありません。

**(2) 取り違える行**

「`UNKNOWN` がある行を不として数える」と、

- (ア) を不と数えてしまいます（本当は矛でも不でもない）。
- (イ) を不と数えてしまいます（本当は矛）。
- (ウ) を数え落とします（`verdicts` が空なのに、本当は D2 と D4 の不）。

正しく数えられるのは (エ) だけで、それも「たまたま」です。
v4 の全部の行で見ても、不の注記を持つ 3,763 行のうち 863 行は `UNKNOWN` を持たず、矛の 2,707 行のうち 2,382 行は `UNKNOWN` を持っていました（18.5 節）。
不は `notes` の `contradiction_unknown:` で数えます。

**(3) (ア) の行の核の答え**

この行だけからは決まりません。
`contradiction` で始まる注記が無いことは、「どの宣言についても矛でも不でもない」という意味です。
そのユニットの `D_kind` を見て、

- 照らす宣言（D1〜D4 のどれか）があれば、その宣言については**内**です。
- 照らす宣言が 1 つも無ければ（`explicit` が空で、`closed_world`・`idempotent` も無い）、そもそも照合の外です。

内は書かれないので、「何も書かれていない」の意味は `D_kind` と合わせて決まります（18.3・18.5 節）。

### 演習 18-4（`summary.json` と manifest から打ち切りを読む）

**(1) 全部解析されたか**

**されていません。** `budget_skipped` が 45 なので、時間上限で 45 ユニットを解析していません。
`status: ok` は、木の解析が例外で止まらず、manifest を書けたという印で、時間上限で飛ばしても `ok` になります（18.10 節。v2 の run24 の meta-skill-evloving は `ok` で 716 ユニットを飛ばしていた）。`status` だけで判断してはいけません。

**(2) 2 つの置き場所**

- `summary.json`: この木の `budget_skipped` が 45。
- manifest: `truncations` の `{"cap": "tree_budget", "count": 45, "relpath": ""}`。

どちらも 45 で、合っています。2 か所は同じ 1 つの値（`tree_budget_skipped`）から書かれるので、合うはずです（18.11 節）。
cap の名前が `tree_budget` なので、ユニットを順に解析している途中で上限を超えたと分かります（前処理の段階で超えていれば `tree_budget_prep`）。

**(3) `ast_node_cap` のファイルの数**

**3 ファイル**（`big/models.py`・`big/schemas.py`・`big/tables.py`）です。
`n_truncations` の 4 は、manifest の `truncations` の要素の数で、`ast_node_cap` の 3 つと、時間上限の 1 つ（`relpath` が空）を合わせた数です。
手順書 9.3 の表は `n_truncations` を「`ast_node_cap` などで打ち切ったファイルの数」と書いていますが、時間上限の打ち切りがある木では、ファイルの数は 4 − 1 = 3 です（18.10 節）。
なお、`n_parse_failures` の 2 は別の数で、parse に失敗したファイルが 2 つあるという意味です（`truncations` には入らず、manifest の `parse_failures` に並ぶ）。

**(4) 180 秒を超えた理由**

解析器が時計を見るのは、ユニットを見つけた直後と、次のユニットの解析に移るときだけです（`authgap/runner.py:88, 130`）。
1 つのユニットの解析を始めたら途中では止めないので、上限を超えたことに気づくのは、そのユニットを解析し終えて次へ移るときです。
さらに、manifest を書き終えるまでの時間も `elapsed_s` に入ります。
そのため、木の `elapsed_s` は 180 秒を超えることがあります。

**(5) 打ち切られた 45 ユニットの扱い**

- **見落としの抜き取りの対象にはなりません。** 時間上限で飛ばしたユニットは manifest の `units` に入らない（`authgap/runner.py:133` の `continue`）ので、抜き取りの道具から見えません。矛・不の抜き取りにも出てきません。
- **V1 頑健性の報告**: 時間上限の打ち切りがあった木として、木の名前、飛ばしたユニットの数（45）、所要時間（236.5 秒）を書きます（手順書 9.3・23.1）。走らせたマシンと日時の記録も添えます。
- **取り直しません。** 手順書は「打ち切りがあっても取り直さない。件数を報告に書く」「遅いマシンなら、走らせる前に速いマシンを選ぶ（走らせた後に選び直さない）」と書いています。

（出典: 手順書は `docs/final_evaluation_procedure.md:657-671`（9.3）、`:1327-1330`（23.1）、`:1451`（困ったとき））

### 確認問題 18-1

- `effects` の要素: **少なくとも 3 つ**並びえます。同じ位置の効果でも、道筋ごとに `entry_lineno` や `witness_chain` の違う要素が並ぶからです（18.4 節の bugasura の例）。中身が全部同じ要素が重なって、もっと多くなることもあります（teamplay-talk の例）。
- 組: **1 組**です。組は (木, ユニット, site, kind, 宣言) で、道筋の本数では増えません。効く宣言は D1 だけ（`readOnlyHint: true` があるので D2・D4 は当てず、`openWorldHint: false` も無いので D3 も無い）なので、(木, ツール, `os.remove`, `FS_WRITE`, D1) の 1 組です。
- 「件」と言うときは、何の単位で数えたか（ここでは組）を必ず添えます（`CLAUDE.md` の規則 3）。

### 確認問題 18-2

**`contradictions.json` の系統**（`declarations` の数の合計、または `scripts/contradiction_by_decl.py` の宣言ごとの矛の数）を書きます。v4 なら 481 組（D1 323・D2 155・D3 0・D4 3）です。

理由: `verdict_rows` の 2,707 は `CONTRADICTION` を持つ**行**の数で、行は slot ごと・道筋ごと・位置ごとに増えます。判定の単位は組なので、組の数で書きます。また D1〜D4 は宣言ごとに報告し、合算しません（D62）。

添える単位: 「組 = (木, ユニット, site, kind, 宣言)」。宣言ごとの数として書きます。

（v4 の数字は論文に使いません。ここでは数え方の例です。）

### 確認問題 18-3

**どれも当たりません。**

- `explicit` に `readOnlyHint` が無いので、D1 ではありません。`readOnlyHint` は `present_no_bound` に入っているので、`readOnlyHint` を true 以外の値（ふつうは `false`）で明示したと読めます。
- `explicit` に `destructiveHint` が無いので、D2 ではありません。
- `explicit` の `openWorldHint` は `openWorldHint: true`（外の世界と関わる、という申告。`open_world: true` もそれを表す）で、D3（`openWorldHint: false`）の逆です。`closed_world` の欄が無いので、D3 ではありません。
- `idempotent` の欄が無いので、D4 ではありません。

`bottom: true`（上界が無い）であることとも合っています。このユニットは、D1〜D4 のどれでも照合されません。

### 確認問題 18-4

**見るところ**: そのユニットの `rows` の、各行の **`notes`** の中の **`contradiction_unknown:D2:<理由>`** という注記です。その組（同じ site・kind）のどれかの行にこの注記があり、`contradiction:D2` の注記がどの行にも無ければ、その組は D2 の不です。理由のコード（`net_post` など）も、注記の 3 つ目の部分で分かります。

**`contradictions.json` で足りない理由**: `contradictions.json` は、`verdicts` に `CONTRADICTION` がある行だけを拾って作るので、不の行が入っていません（`scripts/scan_v2.py:59-61`）。不の組は、manifest の注記から作ります（`scripts/contradiction_by_decl.py` の `load_reasons`）。手順書 6.3 は不の抜き取りの対象を「`contradictions.json` の不の行」と書いていますが、実データと食い違っています（未決。18.9 節）。

**`verdicts` の `UNKNOWN` で足りない理由**: `UNKNOWN` は「その行の効果や slot の値の確度が `resolved` でない」という付録の判定で、宣言に反するかとは関係ありません。v4 では、矛の行にも `UNKNOWN` が付き（2,382 行）、不の行の一部（863 行）には `UNKNOWN` がありませんでした。さらに `UNKNOWN` は宣言の名前を持たないので、D2 の不かどうかも分かりません。


---

<a id="ad-4-9"></a>
## 第 19 章 実物の manifest を読む — 1 ユニットを欄ごとに の答え

この章の演習と確認問題の manifest は、v4 の gemini の木（`evidence/scan_v2_v4_run1/v4-ankitdotgg__making-gemini-useful-with-claude.json`）、手順書の練習用のサーバ（`docs/final_evaluation_procedure.md:1200-1244` を写したもの）、本書の作例（`read_note`）です。
練習用のサーバと作例は、本記録者（AI）が repo の外の作業用の場所で、凍結版の解析器（`git diff analyzer-freeze-3 -- authgap/` が空の版）で走査し、結果を確かめました（2026-10-01）。
「解析器の答え」はその走査の出力です。
「人の判定」の答えは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）と手順書に沿った考え方の例で、最終評価の判定の正解ではありません。
最終評価の判定は学生 1 人が行い、AI（LLM）には判定させません（AI は、コードについての事実を調べる補助にだけ使えます。D70 の 3）。
v4 の数は論文に使いません（D66 の 5）。

### 演習 19-1（relpath と行からユニットを見つけ、注記から答える）

**(1)**

- 開くユニット: manifest の `units` の **2 番目**（`units[1]`）です。1 番目は 309 行の `gemini_list_models` です。探し方は、`unit.relpath == "server.py"` かつ `unit.lineno == 251` で、並び順には頼りません（19.2 節）。
- 読む欄:
  1. `D_kind.explicit` に `readOnlyHint` があること（D1 が効く）。
  2. `effects` のうち `site == "asyncio.create_subprocess_exec"` で `kind == "SPAWN"` の効果（195 行）。
  3. `rows` のうち、同じ site・kind・位置の行（`argv0`・`argv[*]`・`cwd`・`env` の 4 本）の `notes` で、`contradiction` で始まるもの。
- 答え: 4 本の行のどれにも `contradiction:D1` は無く、`contradiction_unknown:D1:spawn_model_opaque` があります。だから、この組は D1 の**不**で、理由コードは `spawn_model_opaque` です（19.6・19.8 節）。
- `verdicts` の `UNKNOWN` は付録の印なので、答えの根拠にしません。

**(2)** 載っていません。
`contradictions.json` は、行の `verdicts` に `CONTRADICTION` がある行だけを拾って作る**矛の候補表**です（`scripts/scan_v2.py:60`）。
この組は不なので、拾われません。
gemini の木から載っているのは、`pipe:communicate` の D1 の矛の 1 行だけです（`rows[0]`）。

**(3)**

| ユニット | 効く宣言 | 組 | 解析器の答え | 理由コード |
|---|---|---|---|---|
| `export_note` | D2（`explicit` に `destructiveHint`） | (`builtins.open`, `FS_WRITE`, D2) | **矛** | `fs_writeout_model_path` |
| `list_notes` | D1（`explicit` に `readOnlyHint`） | (`psycopg.Cursor.execute`, `DB`, D1) | **内** | なし（判定の注記が無い） |

- `export_note` は、書き出し（`'w'`）の書き先 `path` が主体 `MODEL`・確度 `resolved`（LLM が選べる）なので、D2 の矛です（原理 3-a。[第 17 章](ch17.md) 17.7 節）。`D_layer_present:kind:FS_WRITE` と `select_manifest_only(assumed_trig)` は付録の注記で、答えには使いません。
- `list_notes` の行には、`contradiction` で始まる注記がありません。だから D1 の内です。41 行の SQL は `SELECT` で、読み取りです。site が `psycopg.Cursor.execute` と表示されるのは、解析器が sqlite3 の受け手の型を読み違えた表示ですが、kind（`DB`）は合っているので、判定には影響しません（手順書 20.1 節、手引きの下書き `:123-124`）。

### 演習 19-2（`MODEL` なのに矛にならない）

**(1)**

- **解析器の規則の面**: D1 の SPAWN は、`argv0`（と `shell_string`）の slot を見て答えを決めます。「LLM が選べる」（矛、`spawn_model`）と言えるのは、主体が `MODEL` **かつ**確度が `resolved` のときだけです（原理 3 の「選べる」。`authgap/dparse.py:245-272` の `_choice`・`_by_choice`）。gemini の `argv0` は主体 `MODEL` でも確度が `opaque`（`unresolved`）なので、「流れ込むが、選べるとまでは読み切れない」として不（`spawn_model_opaque`）になります。
- **原ソースの実際の面**: `argv0` の slot には、`*full_cmd` の列全体が入っています（既知の限界 U26）。列の 3・5・7 番目に LLM の値（`prompt`・`model`）が混ざるので slot の主体は `MODEL` になりますが、**本当に起動されるプログラム**は列の 1 番目で、Windows の枝では `"cmd"`、それ以外の枝では `GEMINI_PATH`（`shutil.which("gemini")` の結果）です。どちらも LLM は選べません。つまり、原ソースで見ると「LLM が起動するプログラムを選べる」は成り立ちません。

**(2)**

- 違い: `git_log` の列 `["git", "log", name]` は、どの要素も確度 `resolved` で読めます。列全体が `argv0` に入る（U26）ので、主体は `name` の `MODEL`、確度は `resolved` になり、規則の上では「LLM が選べる」とされて矛（`spawn_model`）になりました。gemini は列の中に `opaque` の要素（`GEMINI_PATH` など）があったので、不にとどまりました。
- 人の判定: `git_log` で起動されるのは定数の `git` で、LLM が決めるのは `git log` に渡す引数だけです。だから「LLM が起動するプログラムを決められる」は成り立たず、誤になりうる組です。誤の原因の記号では、E7（モデルが決められないのに決められるとした）の候補です（[第 14 章](ch14.md) 14.10 節、[第 51 章](ch51.md)）。ただし、引数だけで `git` が環境を変えうるかなど、手順 F の問いは別に確かめます。

### 演習 19-3（`contradictions.json` の行から組を数える）

**(1)** 組は **4 つ**です。
1 行の組の数は `declarations` の要素の数なので、1 + 2 + 1 = 4 です。
宣言ごとには、D1 が 1、D2 が 1、D3 が 1、D4 が 1 です。
行の数 `n` は 3 なので、行の数と組の数は一致しません。

**(2)** 影響しません。
組は（木, ユニット, site, kind, 宣言）で数えるので、同じ組の位置がいくつあっても 1 組です。
判定では、手順 G に従って `locations` の位置（10 行と 25 行）を読み、1 つでも「到達する かつ 宣言に反する」位置があれば正にします。
1 つ目で正が見つかれば止めてよく（止めたことを `note` に書く）、誤にするときは全部の位置を読みます。

**(3)** D1 と D3 の両方に反しているので、`readOnlyHint: true`（D1）と `openWorldHint: false`（D3）を書いていたと考えられます。
D1 では HTTP の `PUT` が矛（`net_modify`）、D3 では外部のホスト（定数の外部ホスト、または LLM が決める宛先）との通信が矛です（[第 17 章](ch17.md) 17.6・17.8 節）。
`D_explicit` は `D_kind.explicit` の写しなので、`["readOnlyHint"]` が入っていそうです。
D3 の印（`closed_world`）は `D_explicit` には入りません。
（`openWorldHint: true` を書いていれば `explicit` に `openWorldHint` が入りますが、そのときは D3 が効かないので、この行の `declarations` に D3 は並びません。）

**(4)** この抜粋からは分かりません。
`contradictions.json` には矛の組しか載らないので、不の組は 0 とも何組とも言えません。
不の組を数えるには、manifest の行の `contradiction_unknown:` の注記を読みます（`scripts/contradiction_by_decl.py` の数え方）。

### 演習 19-4（`show_target.py` の出力を読む）

**(1)** 組の kind は `FS_WRITE` なので、次の行を読みます。

- 1〜2 行目（ツール・宣言・打ち切り・opaque）。
- `---- 効果 FS_WRITE builtins.open server.py:13` と、その下の「入口の呼び出し行」「slot path」の 2 行。
- `行 server.py:13 path ['contradiction:D1', 'contradiction_reason:D1:fs_write']`。

読み飛ばすのは、`---- 効果 FS_READ builtins.open server.py:11` とその下の 2 行、`行 server.py:11 path []` です。
道具は site だけで絞り、kind では絞らないので、同じ `builtins.open` の読み取りの効果も出てしまいます（19.10 節の癖 1）。

**(2)**

- 「入口の呼び出し行: 13」は効果の `entry_lineno` から来ます。効果がツールの本体の中にあるので、本体の中で道が始まる行は効果の行そのもの（13 行）です。
- 「道筋: (本体の中)」は、効果の `witness_chain` の欄が無い（空の）ときに道具が出す表示です。効果が本体の中（深さ 0）にあることを意味します。解析器の失敗ではありません（手順書 `:1444`）。

**(3)** 11 行の `FS_READ` の行には、`contradiction` で始まる注記が 1 つも無い、という意味です。
つまり、この効果は D1 について**内**（宣言の範囲内）です。
D1 の判定表では、ファイルの読み取りは反しません。

**(4)** D1 の判定表では、`FS_WRITE` はすべて矛で、書き先や中身を誰が決めたか（主体）を問わないからです（理由 `fs_write`。原理 1-i-b により、呼び出しを越えて残るものはすべて環境）。
主体が効くのは、D1 の SPAWN や D2 の書き出しなどの、判定表で「選べるか」を問う行だけです。
人が判定するなら、決まったファイル `LOG` に記録のために追記し、ツールの動作では読み返さない（この作例のコードには読み返しが無い）ので、書き込み先の種類は「**ログ**」になりそうです（[第 51 章](ch51.md)。手引きの下書き 16.1 節の順 4）。
ただし、読み返しが木のどこにも無いことは、判定のときに確かめます。

### 確認問題 19-1

- `unit_relpath`（と `unit_lineno`）は、**ツールの関数の定義の場所**です。手順 B で manifest のユニットを探す鍵に使い、手順 D でたどり始めるときに開きます。
- `locations` の中の `relpath`（と `lineno`）は、**効果の場所**です。手順 C で開いて「本当にその操作か」を確かめる行です。
- 2 つが同じファイルのこともあります（gemini ではどちらも `server.py`）が、別のファイルのことも多いので、取り違えないようにします。

### 確認問題 19-2

D1 について**矛**です。
`notes` に `contradiction:D1` と `contradiction_reason:D1:fs_write` があるからです（理由は `fs_write`）。
`verdicts` の `UNKNOWN` は付録の印で、「この行の効果か slot のどこかに、読み切れない所（`opaque`）がある」という意味です（`authgap/verdict.py:180-181`）。
核の「不」は `notes` の `contradiction_unknown:` にしか現れないので、`UNKNOWN` があっても不とは読みません。
これは gemini の `pipe:communicate` の行と同じ形です（19.6 節）。

### 確認問題 19-3

9.3 節の表に沿って確かめると、記録しなければならないことは次のとおりです。

1. **`final-c__z` が `analysis_failed`**: `ok` 以外の木なので、木と例外（`RecursionError: ...`）を書き出します。取り直さず、V1 頑健性に書きます（手順書のトラブルの表 `:1438`）。
2. **`final-b__y` の `budget_skipped: 4`**: 時間上限で 4 ユニットを打ち切っています。木と、その木の `elapsed_s`（180.4 秒）を書き出します。取り直しません。打ち切られた 4 ユニットは manifest の `units` に入っていないので、「効果が無かった」とは読みません。
3. **`final-b__y` の `n_parse_failures: 1`**: parse に失敗したファイルの数として報告します。
4. **`final-b__y` の `n_truncations: 2`**: そのまま「打ち切ったファイルが 2 つ」とは読みません。
   `n_truncations` は manifest の外側の `truncations` の長さで、この木は `budget_skipped: 4` なので、時間上限の記録（`cap` が `tree_budget`、前処理で打ち切ったなら `tree_budget_prep`）の 1 件が入っています。
   だから、ファイルごとの打ち切り（`ast_node_cap` など）は 2 − 1 = 1 つです（19.11 節「逆向きの注意」、`scripts/scan_v2.py:274`、`authgap/report.py:279-284`）。
   報告の数を書くときは、`final-b__y` の manifest の `truncations` を開き、`cap` ごとに数え分けて確かめます。
   手順書 9.3 節の表は `n_truncations` を「`ast_node_cap` などで打ち切ったファイルの数」と書いていますが、この 1 件の分は書いていません。

確かめて問題が無いもの:

- `implementation_sha256_combined` は `35606ba9…01cb` で、指紋（`docs/fingerprint.json`）と一致します。
- `authgap_dirty` は `false`、`max_depth` は 4 です。
- `python` は `3.12.3` です（9.3 節の表には無いが、確かめておくとよい。19.11 節の本書の提案）。

使ってはいけないもの: `verdict_rows` の `CONTRADICTION: 5120` は行の数で、矛の件数（組の数）ではありません。矛の件数は `contradictions.json` の `declarations` から数えます。

### 確認問題 19-4

- **写す欄**: `tree`、`site`、`reasons`、`locations`、`decl`、`unit_lineno`
- **書く欄**: `verdict`、`condition_type`、`evidence`、`write_target`、`minutes`、`error_class`

写す欄は抜き取りの出力（候補表と manifest の注記）から機械が埋め、判定の途中で変えません。
書く欄は、判定者が手順 E〜H で埋めます。
どの欄を書くかは判定ごとに決まっています（D83。2026-10-06 に欄を減らした）。
`verdict`・`evidence`・`minutes` はどの判定でも書き、`condition_type` と `write_target` は正のとき（`write_target` は D3 では通信先の種類）、`error_class` は誤のときに書きます。


---

<a id="ad-4-10"></a>
## 第 20 章 通しの例 — 1 つのツールを最初から最後まで追う の答え

この章の演習と確認問題は、本書の作例（`school` パッケージの `list_courses`）と、その変種、v2 の木 `v2-jsyzlbw__bbwatch` を使います。
作例と変種は、本記録者（AI）が repo の外の作業用の場所で、凍結版の解析器（`git diff analyzer-freeze-3 -- authgap/` が空の版）にかけ、結果を確かめました（2026-10-01）。
bbwatch は、pin した版（`docs/corpus_sample_v2.json:536-538`）を作業用の場所で、深さ 4 と深さ 3 で走査し直しました。
「解析器の答え」は、その走査の出力です。
「人の判定」の答えは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）と手順書に沿った考え方の例で、最終評価の判定の正解ではありません。
最終評価の判定は学生 1 人が行い、AI（LLM）には判定させません（AI は、コードについての事実を調べる補助にだけ使えます。D70 の 3）。
v2 は開発用のデータで、論文には使いません。

### 演習 20-1（条件の種類）

**(1)** 変わりません。答えは「**はい**（到達する）」です。

- 到達するかの問いは、「そのツールが呼ばれたとき、その効果が起きる実行の道が 1 つでもあるか」で、毎回起きる必要はありません（手引きの下書き 14.1 節、`:225-227`）。
- 変種でも、その利用者のセッションのファイルがまだ無いとき（たとえば初めての利用者で `list_courses` を呼んだとき）は、13 行の `load_session` が `None` を返し、14 行の `if` の中の 16 行に入り、33 行に届きます。
- 解析器の出力も、元の題材と同じでした（20.15 節）。解析器は、届く道がありうるかを見るだけで、その道の条件を記録しません。

**(2)**

- `condition_type`: `初回`
- 条件の中身は、`evidence` の文末に「条件: …。」として書きます（D83。前の形の `condition` の欄はありません）。例:「条件: その利用者（引数 `user`）のセッションのファイル `/var/app/sessions/<user>.json` がまだ無く、`load_session` が `None` を返すとき（`auth.py:22-23`）。」

考え方:

- 手引きの下書きの 14.3 節の表で、`初回` は「初回だけ・キャッシュが無いときだけ（ツールの道筋の中で `if not os.path.exists(d): os.makedirs(d)`）」です（`:250`）。この変種のファイルは、ツールが**自分で**最初の呼び出しのときに作り、その後は（同じ利用者なら）ファイルがあるので保存しません。表の例の形にいちばん近いので、本書は `初回` と読みます。
- ただし、別の読み方もありえます。表の `外部の状態` の例にも「ファイルが無いとき」があります（`:252`）。また、引数 `user` はモデルが決めるので、モデルがまだ保存の無い名前を渡せば、いつでも届きます（`引数` と読む余地）。
- 3 つの読み方のどれでも、(B) に数え (C) に数えない点は同じです（どれも運用者が決めない条件）。だから主の数と (B)(C) は変わりません。変わるのは条件の種類の内訳だけです。
- 手引きの下書きには、こうした「どの種類にも読める」ときに 1 つを選ぶ決まりがありません。判定の途中なら、選んだ種類を書き、ほかの読み方を `note` に書いておきます。練習の段階で気づいたなら、手引きを承認する前に学生が決める点として書き留めます（手順書 6.8 の 4、`docs/final_evaluation_procedure.md:549-550`）。

**(3)**

| 数 | 数えるか | 理由 |
|---|---|---|
| 主の数 (A) | **数える** | 主の数は条件を問わない |
| 併記 (B) | **数える** | 運用者が決める条件（運用者の設定・起動の方法）ではない |
| 併記 (C) | **数えない** | (C) は条件なしで届くものだけ。この組は `初回` の条件つき |

（出典: `docs/drafts/final_judging_guide_draft.md:247-265`（14.3）、`docs/decisions.md:3796-3804`（D68 の 1））

**(4)** どちらも変わりません。

- `verdict`: `正`。到達し、D1 に反する（保存したファイルは呼び出しの後も残る）。
- `write_target`: `キャッシュ・状態の保存`。ツールの動作のために自分で保存し、13 行で読み返す点は同じです。

元の題材との違いは、`condition_type`（`なし` → `初回`）と、`evidence` の条件の書き方（文末の「条件: …」を含む）だけです。

### 演習 20-2（この題材の `evidence` を自分で書く）

**(1)** 解答の例（組 1、`auth.py:31`）:

> `server.py:7`（`readOnlyHint: True`）。`server.py:10`（`list_courses` の本体が `do_login(user)` を毎回呼ぶ。`do_login` は `server.py:2` の `from .auth import login as do_login` で `auth.login`）→ `auth.py:16`（`login` が `save_session(user, data)` を呼ぶ。14 行の `if` は 15 行だけを守り、16 行は守らない）→ `auth.py:31` `open(tmp, "w")`（`tmp` は `/var/app/sessions/<user>.json.tmp`。モード `w` で作って書く）。毎回到達する。D1 では、一時ファイルでもファイルの作成・書き込みは呼び出しの外の環境を変える（このファイルは 33 行で本物のセッションのファイルになり、次の呼び出しの `auth.py:13` で読み返される）。

部品の確かめ:

| 部品 | 解答の例の中の所 |
|---|---|
| 1 宣言の行 | `server.py:7` |
| 2 入口の行 | `server.py:10` |
| 3 名前の対応 | `server.py:2` の別名つきの import |
| 4 途中の段と条件 | `auth.py:16`、14 行の `if` の範囲 |
| 5 効果の行と中身 | `auth.py:31` `open(tmp, "w")`、書き先とモード |
| 6 到達の条件 | 「毎回到達する」 |
| 7 反する理由 | 一時ファイルでも D1 では反する。中身は残り、読み返される |

あわせて `note` に、書き込み先の種類が境界の事例（一時ファイルか、キャッシュ・状態の保存か。20.15 節）であることと、自分が選んだ種類とその理由を書きます。
判定の途中で決められなければ、手引きの下書きの決まりで「その他・不明」にし、事例を `note` に書きます（`:408-409`）。

**(2)** 解答の例（変種の組 2、`auth.py:33`）:

> `server.py:7`（`readOnlyHint: True`）。`server.py:10`（本体が `do_login(user)` を毎回呼ぶ。`server.py:2` の別名つきの import で `auth.login`）→ `auth.py:13-16`（13 行の `load_session(user)` が、`auth.py:22-23` でファイルが無ければ `None` を返す。14 行の `if data is None:` の中の 16 行で `save_session(user, data)` を呼ぶ）→ `auth.py:33` `os.replace(tmp, path)`（`path` は `/var/app/sessions/<user>.json`）。その利用者のセッションのファイルがまだ無いとき（初回）に到達する。保存したファイルは次の呼び出しの `auth.py:13` で読み返される。

書き換えた所:

- 途中の段の説明を、「14 行の `if` は 16 行を守らない」から「16 行は 14 行の `if` の**中**」に変え、`if` が真になる条件（`auth.py:22-23` でファイルが無いと `None`）の行を足した。
- 到達の条件を、「毎回到達する」から「ファイルがまだ無いとき（初回）に到達する」に変えた。

条件を `evidence` に書いておくと、`condition_type` の欄の値（`初回`）の根拠を、第三者が行で確かめられます。

**(3)** 20.14 節の悪い例の 3（関数の名前だけで、ファイルと行が無い）に近く、4（効果の行だけ）の性質も持ちます。

欠けているもの:

- ファイルの名前（「33 行」がどのファイルか分からない）。
- 宣言の行、入口の行（`server.py:10`）、別名の対応（`do_login` → `login`）。
- 途中の段の行と、14 行の `if` が 16 行を守らないこと（毎回届く理由）。
- `os.replace` が何を何で置き換えるか、なぜ D1 に反するか（呼び出しの後に残る）。

直し方: (1) の組 2 版、つまり 20.13 節・20.14 節の良い例の形にします。

### 演習 20-3（解析器が site を psycopg と表示していたら）

**(1)** 変わりません。判定は**正**のままです。

- 判定するのはコードの動作で、解析器の説明ではありません。解析器の出した理由（site の名前や注記）が間違っていても、2 つの問いの答えが「はい」なら正です（`docs/final_evaluation_procedure.md:735-736`、`docs/drafts/final_judging_guide_draft.md:53-54`）。
- site の名前は違いますが、**動作の種類（kind）は `DB` で合っています**。手順 C の決まりでは、この場合は判定に影響しません（`docs/drafts/final_judging_guide_draft.md:126-127`）。
- 問い 1: 10 行で `login` が毎回 `save_session` を呼ぶので、16 行に毎回届きます（条件 `なし`）。
- 問い 2: 16 行の `INSERT OR REPLACE` は DB の行を足すか置き換えます。DB の中身は呼び出しの後も残るので、D1 の問い「呼び出しの後に残る何かを変えるか」に「はい」です（手引きの下書きの D1 の表で「DB のデータ・スキーマの変更 → 反する」）。

**(2)** 解答の例:

> site は `psycopg.Cursor.execute` と表示されるが、実際は `auth.py:15` の `sqlite3.connect(...)` の接続の `execute`。kind（DB）は合っているので判定には影響しない。

site の名前の違いは、解析器の受け手の型の読み違いで、論文の限界の材料になるので、気づいたら書き残します。

**(3)** `データベース` です。元の題材（`キャッシュ・状態の保存`）とは違います。

- 書き込み先の種類は、16.1 節の 8 つを**上から順に**当て、最初に当てはまったものを付けます。
- 順 2 の「データベース」（DB の行・スキーマ・残る設定を変える）に当てはまるので、順 6 の「キャッシュ・状態の保存」まで行きません。
- 手引きの下書きの境界の例にも、「SQLite のキャッシュ DB への書き込み → データベース（順 2 が順 6 より先）」があります（`docs/drafts/final_judging_guide_draft.md:412`）。
- このように、判定（正）が同じでも、ラベルは書き込みの先の種類で変わります。

**(4)** **1 組**です。

- 組は（木, ユニット, site, kind, 宣言）で数え、slot ごとの行の数では数えません。
- 2 本の行（`params` と `sql`）は、同じ site（`psycopg.Cursor.execute`）・同じ kind（`DB`）・同じ位置（16 行）で、宣言も D1 です。
- 実際に、候補表を作る関数をこの manifest に当てると、1 行（`declarations` は `["D1"]`、`locations` は 1 か所）になりました。
- 解析器は、効果ごとに 1 回判定表を引き、その結果をその効果のすべての slot の行に付けます（[第 19 章](ch19.md)）。だから 2 本の行に同じ注記が付きます。

**(5)** 解析器の答えは**内**になり、人が判定する組はできません。

- `SELECT` は読み取りなので、D1 の解析器の判定表では宣言の範囲内です。実際にかけると、16 行の 2 本の行（`params`・`sql`）には `contradiction` で始まる注記が付きませんでした。site の表示は同じく `psycopg.Cursor.execute` でした。
- 候補表は矛の行だけを拾うので、この効果は候補表に載らず、矛の判定の対象（組）にはなりません。
- もしこのツールに D1 の矛が 1 つも無ければ、見落としの抜き取りの対象（D1 を明示し、D1 への矛が 1 件も無いユニット）にはなりえます。そのときは[第 52 章](ch52.md)の見落としの手順で、解析器の出力を見る前にコードを読みます。

### 演習 20-4（深さと見落とし）

**(1)** **誤 clear** の向きです。本当は宣言に反する書き込み（セッションの保存）があるのに、解析器がそれを矛として出していません（[第 21 章](ch21.md)）。

**(2)** **なりません**。

- 深さ 3 の結果でも、`list_courses` には D1 の矛（`os.chmod` の組）が 1 件あります。
- 見落としの抜き取りの対象は「その宣言への矛が 1 件も無いユニット」なので、このユニットは対象から外れます（`docs/final_evaluation_procedure.md:451-452`）。
- つまり、矛のあるユニットの中で見えなくなった**別の**書き込みは、見落としの数にも入りません。矛の判定では `os.chmod` の組だけが判定されます。
- 木の単位の主の数字（本当の矛が 1 件以上あった木）は、`os.chmod` の組が正と判定されれば、この見えなくなった書き込みの影響を受けません。ただし、ユニットの中で何が見えなくなったかは、どの数字にも現れません。深さの感度分析（深さ 3・5 での矛の件数。事前登録の下書きの (c)）は、こうした変化を件数で示すためのものです。

**(3)** 「**見落とし（深さ 4 の外）**」として別に記録し、主の見落としの数には入れず、併記します（D68 の 2）。
深さ 4 より奥を探しに行く必要はありません（読む範囲は深さ 4 まで）。
理由: 普通の見落としに数えると、数が判定者の読んだ深さで変わります。「反する動作は無い」にすると、知っている違反を安全側に倒すことになります（CLAUDE.md 規則 4）。
（出典: `docs/decisions.md:3805-3808`（D68 の 2）、`docs/drafts/final_judging_guide_draft.md:482-490`（18.3））

### 確認問題 20-1

書き先は 29 行の `f"{SESSION_DIR}/{user}.json"` で、つなぐ部品の 1 つが、ツールの引数 `user` です。
`user` は LLM がツールを呼ぶときに渡す値なので、主体は `MODEL` です（20.2 節で付けた印が、`login` → `save_session` と運ばれてきます）。
値をつないで合わせるとき、主体は順序の上の方（`USER ⊑ OP ⊑ MODEL` の `MODEL` の側）を採ります（[第 14 章](ch14.md)、`authgap/ir.py:65-71` の `prin_join`）。
フォルダの名前（`/var/app/sessions`）・`/`・`.json` は `OP` ですが、1 つでも `MODEL` の部品が混ざれば、全体は `MODEL` になります。
全体としては「書き先の名前の一部を LLM が決められる」値だからです。root は `user` です。

### 確認問題 20-2

| | 誰の答えか | 何を意味するか |
|---|---|---|
| 矛 | 解析器 | 解析器の判定表で、効果と宣言の組み合わせが「宣言に反する」に当たった |
| 正 | 人 | 人が原ソースで確かめ、「到達する」と「宣言に反する」の両方が成り立った。解析器の矛は当たっていた |

解析器が矛を出し、人が誤と判定したときは、**解析器の誤警報**が起きたことを意味します。
その矛の効果は、ツールの呼び出しでは届かない（例: 起動時の初期化の中だけ）か、届いても宣言に反しない（例: D2 で、同じ呼び出しで自分が作った一時ファイルを消すだけ）のどちらかです。
誤の原因は E1〜E9 で記録し、集計で「誤の原因の内訳」として報告します（[第 51 章](ch51.md)）。

### 確認問題 20-3

**(1)** **不明**です（5 行の判定表の 5 行目）。
黙って正や誤に倒しません（CLAUDE.md 規則 4）。`unknown_reason` に、決められない理由を書きます。

**(2)** 必要ありません。判定は**誤**（原因: 到達しない）です（5 行の判定表の 2 行目。「—」は答えなくてよいの印）。
起きない効果は、宣言を破りようがないからです。誤の原因（E1 や E6 など）を `error_class` に書きます。

### 確認問題 20-4

24 行の `open(path)` は、モードを書いていないので読み取りで、kind は `FS_READ` です。
D1 の解析器の判定表で `FS_READ` は宣言の範囲内（内）なので、行に `contradiction` で始まる注記が付かず、候補表に載りません。
さらに、組は（木, ユニット, site, kind, 宣言）で数えるので、kind が `FS_READ` の 24 行は、kind が `FS_WRITE` の 31 行（組 1）とも同じ組になりません。

`show_target.py` は、渡された site だけで効果と行を絞り、kind では絞りません（`docs/final_evaluation_procedure.md:472-493` のコードの 473 行と 480 行で、`e["site"] != site` と `r["site"] == site` だけを見ている）。
だから、`builtins.open` を渡すと、同じ site の 24 行の読み取りの効果と、注記が空の 24 行の行も出力されます。
組 1 を判定するときは、kind が `FS_WRITE` の効果と、`contradiction` の注記がある行だけを読みます。


---

---

[← 付録 D — 第 3 部（第 9・10 章）](appendix-d-3.md) ｜ [目次](README.md) ｜ [付録 D — 第 5 部（第 21〜26 章） →](appendix-d-5.md)
