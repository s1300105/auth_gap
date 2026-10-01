### 第 19 章

この章の演習と確認問題の manifest は、v4 の gemini の木（`evidence/scan_v2_v4_run1/v4-ankitdotgg__making-gemini-useful-with-claude.json`）、手順書の練習用のサーバ（`docs/final_evaluation_procedure.md:1189-1233` を写したもの）、本書の作例（`read_note`）です。
練習用のサーバと作例は、本記録者（AI）が repo の外の作業用の場所で、凍結版の解析器（`git diff analyzer-freeze-3 -- authgap/` が空の版）で走査し、結果を確かめました（2026-10-01）。
「解析器の答え」はその走査の出力です。
「人の判定」の答えは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）と手順書に沿った考え方の例で、最終評価の判定の正解ではありません。
最終評価の判定は学生 1 人が行い、AI（LLM）は使いません（D70 の 3）。
v4 の数は論文に使いません（D66 の 5）。

#### 演習 19-1（relpath と行からユニットを見つけ、注記から答える）

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

- `export_note` は、書き出し（`'w'`）の書き先 `path` が主体 `MODEL`・確度 `resolved`（LLM が選べる）なので、D2 の矛です（原理 3-a。第 17 章 17.7 節）。`D_layer_present:kind:FS_WRITE` と `select_manifest_only(assumed_trig)` は付録の注記で、答えには使いません。
- `list_notes` の行には、`contradiction` で始まる注記がありません。だから D1 の内です。41 行の SQL は `SELECT` で、読み取りです。site が `psycopg.Cursor.execute` と表示されるのは、解析器が sqlite3 の受け手の型を読み違えた表示ですが、kind（`DB`）は合っているので、判定には影響しません（手順書 20.1 節、手引きの下書き `:123-124`）。

#### 演習 19-2（`MODEL` なのに矛にならない）

**(1)**

- **解析器の規則の面**: D1 の SPAWN は、`argv0`（と `shell_string`）の slot を見て答えを決めます。「LLM が選べる」（矛、`spawn_model`）と言えるのは、主体が `MODEL` **かつ**確度が `resolved` のときだけです（原理 3 の「選べる」。`authgap/dparse.py:245-272` の `_choice`・`_by_choice`）。gemini の `argv0` は主体 `MODEL` でも確度が `opaque`（`unresolved`）なので、「流れ込むが、選べるとまでは読み切れない」として不（`spawn_model_opaque`）になります。
- **原ソースの実際の面**: `argv0` の slot には、`*full_cmd` の列全体が入っています（既知の限界 U26）。列の 3・5・7 番目に LLM の値（`prompt`・`model`）が混ざるので slot の主体は `MODEL` になりますが、**本当に起動されるプログラム**は列の 1 番目で、Windows の枝では `"cmd"`、それ以外の枝では `GEMINI_PATH`（`shutil.which("gemini")` の結果）です。どちらも LLM は選べません。つまり、原ソースで見ると「LLM が起動するプログラムを選べる」は成り立ちません。

**(2)**

- 違い: `git_log` の列 `["git", "log", name]` は、どの要素も確度 `resolved` で読めます。列全体が `argv0` に入る（U26）ので、主体は `name` の `MODEL`、確度は `resolved` になり、規則の上では「LLM が選べる」とされて矛（`spawn_model`）になりました。gemini は列の中に `opaque` の要素（`GEMINI_PATH` など）があったので、不にとどまりました。
- 人の判定: `git_log` で起動されるのは定数の `git` で、LLM が決めるのは `git log` に渡す引数だけです。だから「LLM が起動するプログラムを決められる」は成り立たず、誤になりうる組です。誤の原因の記号では、E7（モデルが決められないのに決められるとした）の候補です（第 14 章 14.10 節、第 51 章）。ただし、引数だけで `git` が環境を変えうるかなど、手順 F の問いは別に確かめます。

#### 演習 19-3（`contradictions.json` の行から組を数える）

**(1)** 組は **4 つ**です。
1 行の組の数は `declarations` の要素の数なので、1 + 2 + 1 = 4 です。
宣言ごとには、D1 が 1、D2 が 1、D3 が 1、D4 が 1 です。
行の数 `n` は 3 なので、行の数と組の数は一致しません。

**(2)** 影響しません。
組は（木, ユニット, site, kind, 宣言）で数えるので、同じ組の位置がいくつあっても 1 組です。
判定では、手順 G に従って `locations` の位置（10 行と 25 行）を読み、1 つでも「到達する かつ 宣言に反する」位置があれば正にします。
1 つ目で正が見つかれば止めてよく（止めたことを `note` に書く）、誤にするときは全部の位置を読みます。

**(3)** D1 と D3 の両方に反しているので、`readOnlyHint: true`（D1）と `openWorldHint: false`（D3）を書いていたと考えられます。
D1 では HTTP の `PUT` が矛（`net_modify`）、D3 では外部のホスト（定数の外部ホスト、または LLM が決める宛先）との通信が矛です（第 17 章 17.6・17.8 節）。
`D_explicit` は `D_kind.explicit` の写しなので、`["readOnlyHint"]` が入っていそうです。
D3 の印（`closed_world`）は `D_explicit` には入りません。
（`openWorldHint: true` を書いていれば `explicit` に `openWorldHint` が入りますが、そのときは D3 が効かないので、この行の `declarations` に D3 は並びません。）

**(4)** この抜粋からは分かりません。
`contradictions.json` には矛の組しか載らないので、不の組は 0 とも何組とも言えません。
不の組を数えるには、manifest の行の `contradiction_unknown:` の注記を読みます（`scripts/contradiction_by_decl.py` の数え方）。

#### 演習 19-4（`show_target.py` の出力を読む）

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
人が判定するなら、決まったファイル `LOG` に記録のために追記し、ツールの動作では読み返さない（この作例のコードには読み返しが無い）ので、書き込み先の種類は「**ログ**」になりそうです（第 51 章。手引きの下書き 16.1 節の順 4）。
ただし、読み返しが木のどこにも無いことは、判定のときに確かめます。

#### 確認問題 19-1

- `unit_relpath`（と `unit_lineno`）は、**ツールの関数の定義の場所**です。手順 B で manifest のユニットを探す鍵に使い、手順 D でたどり始めるときに開きます。
- `locations` の中の `relpath`（と `lineno`）は、**効果の場所**です。手順 C で開いて「本当にその操作か」を確かめる行です。
- 2 つが同じファイルのこともあります（gemini ではどちらも `server.py`）が、別のファイルのことも多いので、取り違えないようにします。

#### 確認問題 19-2

D1 について**矛**です。
`notes` に `contradiction:D1` と `contradiction_reason:D1:fs_write` があるからです（理由は `fs_write`）。
`verdicts` の `UNKNOWN` は付録の印で、「この行の効果か slot のどこかに、読み切れない所（`opaque`）がある」という意味です（`authgap/verdict.py:180-181`）。
核の「不」は `notes` の `contradiction_unknown:` にしか現れないので、`UNKNOWN` があっても不とは読みません。
これは gemini の `pipe:communicate` の行と同じ形です（19.6 節）。

#### 確認問題 19-3

9.3 節の表に沿って確かめると、記録しなければならないことは次のとおりです。

1. **`final-c__z` が `analysis_failed`**: `ok` 以外の木なので、木と例外（`RecursionError: ...`）を書き出します。取り直さず、V1 頑健性に書きます（手順書のトラブルの表 `:1438`）。
2. **`final-b__y` の `budget_skipped: 4`**: 時間上限で 4 ユニットを打ち切っています。木と、その木の `elapsed_s`（180.4 秒）を書き出します。取り直しません。打ち切られた 4 ユニットは manifest の `units` に入っていないので、「効果が無かった」とは読みません。
3. **`final-b__y` の `n_parse_failures: 1`**: parse に失敗したファイルの数として報告します。
4. **`final-b__y` の `n_truncations: 2`**: `ast_node_cap` などで打ち切ったファイルの数として報告します。

確かめて問題が無いもの:

- `implementation_sha256_combined` は `35606ba9…01cb` で、指紋（`docs/fingerprint.json`）と一致します。
- `authgap_dirty` は `false`、`max_depth` は 4 です。
- `python` は `3.12.3` です（9.3 節の表には無いが、確かめておくとよい。19.11 節の本書の提案）。

使ってはいけないもの: `verdict_rows` の `CONTRADICTION: 5120` は行の数で、矛の件数（組の数）ではありません。矛の件数は `contradictions.json` の `declarations` から数えます。

#### 確認問題 19-4

- **写す欄**: `tree`、`site`、`reasons`、`locations`、`decl`、`unit_lineno`
- **書く欄**: `verdict`、`condition_type`、`evidence`、`write_target`、`minutes`、`violates`

写す欄は抜き取りの出力（候補表と manifest の注記）から機械が埋め、判定の途中で変えません。
書く欄は、判定者が手順 E〜H で埋めます（`write_target` は正のとき、D3 では通信先の種類）。
