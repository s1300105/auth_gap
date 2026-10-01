### 第 18 章

この章の演習の作例（`archive_report`、`final-acme__notes-mcp`、`final-acme__big-mcp` など）は、説明のために本記録者（AI）が作ったもので、実在の木ではありません。
実物の数（v4 の 481 行、2,707 行など）は、`evidence/scan_v2_v4_run1/` の `summary.json`・`contradictions.json`・manifest を本記録者が読んで確かめたものです。v4 の数字は論文に使いません（D66 の 5）。
答えは、手順書と手引きの下書き（未承認）の規則に沿った考え方の例です。最終評価の判定は学生 1 人が行います（D70 の 3）。

#### 演習 18-1（行から組を数える）

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
- 行 3 は D2 について注記がありません。追記（`'a'`）は D2 では内だからです（第 17 章の判定表）。内は書かれません。
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

#### 演習 18-2（`declarations` に宣言が 2 つ）

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

第 16 章の当て方では、D2 は「`readOnlyHint: true` が**無い**とき」だけ当て、D1 は「`readOnlyHint: true` がある」ときに当てます。
1 つの宣言の中で、この 2 つは同時に成り立ちません。だから、ふつうのデコレータで登録したツール（宣言が 1 つ）では、D1 と D2 が同じユニットに当たることはありません。

並びうるのは、**低レベルの書き方のハンドラ**（`handle_call_tool` のように、1 つのハンドラが名前で分岐して複数のツールを受け持つユニット）だと考えられます。
このとき解析器は、効果ごとに、その効果を受け持つツールの宣言で照らします（第 16 章 16.5 節の「低レベルの書き方のハンドラ」）。
ある位置は `readOnlyHint: true` のツールの分岐（D1）、別の位置は `destructiveHint: false` のツールの分岐（D2）で照らされれば、1 行に D1 と D2 が並びえます。
なお、v2・v3・v4 の `contradictions.json` には、D1 と D2 が同じ行に並んだ例はありませんでした（本書の執筆時に確かめた。並んでいたのは D2 と D3、D1 と D3 だけ）。これは作例で、仕組みの上でありうる形です。

#### 演習 18-3（`verdicts` に `UNKNOWN` がある行は核の不か）

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

#### 演習 18-4（`summary.json` と manifest から打ち切りを読む）

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

（出典: 手順書は `docs/final_evaluation_procedure.md:646-660`（9.3）、`:1315-1318`（23.1）、`:1439`（困ったとき））

#### 確認問題 18-1

- `effects` の要素: **少なくとも 3 つ**並びえます。同じ位置の効果でも、道筋ごとに `entry_lineno` や `witness_chain` の違う要素が並ぶからです（18.4 節の bugasura の例）。中身が全部同じ要素が重なって、もっと多くなることもあります（teamplay-talk の例）。
- 組: **1 組**です。組は (木, ユニット, site, kind, 宣言) で、道筋の本数では増えません。効く宣言は D1 だけ（`readOnlyHint: true` があるので D2・D4 は当てず、`openWorldHint: false` も無いので D3 も無い）なので、(木, ツール, `os.remove`, `FS_WRITE`, D1) の 1 組です。
- 「件」と言うときは、何の単位で数えたか（ここでは組）を必ず添えます（`CLAUDE.md` の規則 3）。

#### 確認問題 18-2

**`contradictions.json` の系統**（`declarations` の数の合計、または `scripts/contradiction_by_decl.py` の宣言ごとの矛の数）を書きます。v4 なら 481 組（D1 323・D2 155・D3 0・D4 3）です。

理由: `verdict_rows` の 2,707 は `CONTRADICTION` を持つ**行**の数で、行は slot ごと・道筋ごと・位置ごとに増えます。判定の単位は組なので、組の数で書きます。また D1〜D4 は宣言ごとに報告し、合算しません（D62）。

添える単位: 「組 = (木, ユニット, site, kind, 宣言)」。宣言ごとの数として書きます。

（v4 の数字は論文に使いません。ここでは数え方の例です。）

#### 確認問題 18-3

**どれも当たりません。**

- `explicit` に `readOnlyHint` が無いので、D1 ではありません。`readOnlyHint` は `present_no_bound` に入っているので、`readOnlyHint` を true 以外の値（ふつうは `false`）で明示したと読めます。
- `explicit` に `destructiveHint` が無いので、D2 ではありません。
- `explicit` の `openWorldHint` は `openWorldHint: true`（外の世界と関わる、という申告。`open_world: true` もそれを表す）で、D3（`openWorldHint: false`）の逆です。`closed_world` の欄が無いので、D3 ではありません。
- `idempotent` の欄が無いので、D4 ではありません。

`bottom: true`（上界が無い）であることとも合っています。このユニットは、D1〜D4 のどれでも照合されません。

#### 確認問題 18-4

**見るところ**: そのユニットの `rows` の、各行の **`notes`** の中の **`contradiction_unknown:D2:<理由>`** という注記です。その組（同じ site・kind）のどれかの行にこの注記があり、`contradiction:D2` の注記がどの行にも無ければ、その組は D2 の不です。理由のコード（`net_post` など）も、注記の 3 つ目の部分で分かります。

**`contradictions.json` で足りない理由**: `contradictions.json` は、`verdicts` に `CONTRADICTION` がある行だけを拾って作るので、不の行が入っていません（`scripts/scan_v2.py:59-61`）。不の組は、manifest の注記から作ります（`scripts/contradiction_by_decl.py` の `load_reasons`）。手順書 6.3 は不の抜き取りの対象を「`contradictions.json` の不の行」と書いていますが、実データと食い違っています（未決。18.9 節）。

**`verdicts` の `UNKNOWN` で足りない理由**: `UNKNOWN` は「その行の効果や slot の値の確度が `resolved` でない」という付録の判定で、宣言に反するかとは関係ありません。v4 では、矛の行にも `UNKNOWN` が付き（2,382 行）、不の行の一部（863 行）には `UNKNOWN` がありませんでした。さらに `UNKNOWN` は宣言の名前を持たないので、D2 の不かどうかも分かりません。
