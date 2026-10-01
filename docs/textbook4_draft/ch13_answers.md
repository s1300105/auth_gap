### 第 13 章

この章の演習の作例は、本記録者（AI）が repo の外の作業用の場所に置き、凍結版の解析器 `analyzer-freeze-3`（`git diff analyzer-freeze-3 -- authgap/` が空であることを確かめたもの）で走査して、結果を確かめました（2026-10-01）。
「解析器の結果」はその走査の出力です。「人の判定」の見通しは、手引きの下書き（`docs/drafts/final_judging_guide_draft.md`。未承認）に沿った考え方の例で、最終評価の判定の正解ではありません。最終評価の判定は学生 1 人が行います（D70 の 3）。

#### 演習 13-1（効果を見つける）

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
- 21 行の `path` の slot は、主体 `OP`・確度 `opaque` でした。`tmp` は sink 表に無い `mkstemp` の戻り値なので、解析器は値を追い切れません（第 14 章）。
- 23 行の `path` の slot は、行き先の `os.path.join("/tmp/snap", name)` で、主体 `MODEL`・確度 `resolved` でした。`content` の slot が元の `tmp` です（13.8 節の「`shutil.copy(a, b)` の `path` は `b`」）。
- 20 行は効果に出ませんが、ディスクにファイルを 1 つ作ります。人が D1 を判定するなら、これも「環境を変える」書き込みです（13.7 節）。この作例では、ほかの行に矛が出ているので見落としの判定の対象にはなりませんが、矛の 1 件もないツールなら、見落とし（原因「語彙」）の候補になる形です。
- 25 行は、ログの出し口を何も設定していないので、`info` の記録はファイルに書かれません（第 9 章 9.5）。出し口が `FileHandler` などなら、解析器の出力に出ない書き込みになります。

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
- **23 行の `shutil.copy`** は、「正」になりそうです。行き先のファイル名 `name` をモデルが決めるので、`/tmp/snap` の中に前の呼び出しが作ったファイルなどがあれば、それを上書きできます（第 17 章で学ぶ原理 3-a。手引きの 15.2 の「書き出し: 書き先をモデルが決められるなら反する」）。
- 参考: 21 行（不 `fs_writeout`）は矛ではないので、矛の判定の対象ではありません。不の中身の判定（第 52 章）で当たったなら、書き先が作ったばかりの空の一時ファイルなので、「違反でない」と答える見通しです。

（出典: `docs/drafts/final_judging_guide_draft.md:327-347`、`:430`、`docs/open_questions.md:1061`）

#### 演習 13-2（`open(p, 'x')` と D2）

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
`'x'` は「新しく作る。同じ名前のファイルが既にあれば失敗する」モードです（第 9 章 9.3）。
だから、どの `path` を渡されても、呼び出しの前からあったファイルの中身を消したり上書きしたりすることはできません。
書き先をモデルが決めても同じです。既存のファイルを指せば、書く前に失敗するだけです。
手引きの D2 の表も「新しく作るだけ（`mkdir`、`open('x')`、…）→ 反しない」としています。
（出典: `docs/drafts/final_judging_guide_draft.md:333`、`docs/contradiction_principles.md:185`）

**(5)** `'a+'` なら、次のように変わります。

- (1): `destructive` が **`true`**、`fs_mode` が `"a+"`。`_mode_destructive` は `+` があれば `true` にするからです。
- (2): `_fs_class` は「書き出し」（`writeout`）を返します。書き先 `path` をモデルが選べるので、D2 は**矛**（`fs_writeout_model_path`）になります（本記録者の走査で確かめた）。`path` が定数なら不（`fs_writeout`）です。
- (4): 人の答えは変わりません。`'a+'` の書き込みは常にファイルの末尾に足されるので、前の中身は残ります（`truncate()` などで切り詰めていなければ）。解析器が矛を出しても、人の判定では「宣言に反しない」の**誤**になる見通しで、原因は **E8**（宣言に反しない）の見当です。13.10 節の「`'a+'` は D2 では書き出し扱い」が、この食い違いの理由です。
- 参考: D4 では `'a+'` も `a` を含むので矛（`fs_append`）になります。

#### 演習 13-3（`pipe:communicate` はファイルの書き込みか）

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
- (イ): **正**。D1 の問い「呼び出しの後に残る何かを変えるか」に対して、子が DB に行を足すので反します。`evidence` には、起動の行・流し込みの行と、「`sqlite3` は標準入力の SQL を実行する」ことを書きます。書き込み先の種類は「データベース」の見当です（第 51 章）。なお、`title` をそのまま SQL につないでいるので SQL の注入もできますが、それは宣言の正誤とは別の話なので、`note` に書くだけにします。
- (ウ): **正**。コードの実行（`EXEC`）は D1 に反すると決まっています（表 D41。手引きの 15.1）。しかも実行するコマンドをモデルが決めます。

**(4)** `pipe:communicate` は、子プロセスの**標準入力への書き込み**であって、それ自体はファイルの書き込みではありません。
解析器が `FS_WRITE` と記録するのは、「子が受け取ったもので書き込みをするかもしれない」という保守的な上界の情報行だからです（D61 の改訂）。
ファイルが変わるかどうかは、子が何者で、受け取ったものをどう使うかを調べて決めます（(ア) は変わらない、(イ) は変わる）。

（出典: `docs/drafts/final_judging_guide_draft.md:118`、`:309-311`、`:324`、`:433`、`docs/open_questions.md:1068-1070`、`docs/decisions.md:3459-3466`）

#### 演習 13-4（manifest の効果を読む）

**(1)** sqlite3 の接続の `execute` に当たる proxy の行は、受け手の型の候補として `sqlite3.Cursor`・`sqlite3.Connection`・`psycopg.Cursor`・`psycopg2.cursor` の 4 つをまとめて持っています。
解析器は site の名前を `sorted(row.recv_types)[0]`（候補をアルファベット順に並べた先頭）とメソッド名から作るので、`psycopg.Cursor.execute` になります。
実際の受け手の型（`sqlite3.Connection`）ではなく、行の候補の先頭が使われるのが理由です（`authgap/effects.py:755`、`authgap/catalog/sinks.py:504-510`）。

**(2)** 「誤」にはしません。
46 行目は、DB に SQL の命令を送る呼び出しで、manifest の `kind`（`DB`）と動作の種類が合っています。
手引きは「site 名のライブラリが違っていても、動作の種類（kind）が合っていれば判定には影響しない。その場合は `note` に書いておく」と決めています。
E4 は「受け手の型の読み違いで、動作の種類まで違う」ときだけです。
`note` には「site は psycopg と表示されるが sqlite3」と書きます。
（出典: `docs/drafts/final_judging_guide_draft.md:123-124`、`:432`）

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
（出典: `docs/drafts/final_judging_guide_draft.md:334`、`docs/contradiction_principles.md` §7.2 の DB の行）

#### 確認問題 13-1

**受け手 `client` の型**（何のオブジェクトか）を知る必要があります。
`get` という名前のメソッドは世の中にいくらでもあるので、名前だけでは通信か決まりません。
`client` の型が proxy の sink 表の行の候補（`httpx.Client`・`httpx.AsyncClient`・`requests.Session`）のどれかだと分かって、初めて `NET` の効果になります。
型が分からなければ、解析器は**効果を出しません**（通信を見落としうる）。
本記録者が、型の分からない引数 `client` に `client.get(url)` を呼ぶ作例を走査すると、効果は 0 で、ユニットの `opaque_reasons` に `receiver` と `unresolved` が残りました（意味は第 14 章）。
受け手の型の知り方は第 15 章で学びます。

#### 確認問題 13-2

| | `destructive` | 13.9 節の類 | D2 の解析器の結果 |
|---|---|---|---|
| (ア) `os.makedirs(d, exist_ok=True)` | `false` | 追記 | **内** |
| (イ) `os.replace(tmp, target)` | `true` | 消す・動かす・変える | **矛**（`fs_remove`） |
| (ウ) `Path(p).write_text(s)`（`p` は定数） | `true` | 書き出し | **不**（`fs_writeout`） |

- (イ): `os.replace` は書き出しの一覧に無い `destructive=True` の行なので、書き先によらず `fs_remove` の矛です。置き換えられる `target` の前の中身が消えるからです。
- (ウ): `write_text` は書き出しの一覧に入っています。書き先 `p` が定数で、モデルが選べないので不です（`p` をモデルが選べれば矛 `fs_writeout_model_path`）。
- 3 つとも、本記録者の作例の走査で確かめました。

#### 確認問題 13-3

**D2 の矛を少なく数える向き**（見落とし、誤 clear の向き）に影響します。
HTTP の `DELETE` は相手の資源を消す操作で、D2 の矛盾の典型ですが、セッションの `.delete` は sink 表に無いので効果に出ず、矛になりません。
そのため、報告する D2 の矛の数は**下限**（本当の数はそれ以上かもしれない）になります。

それでも足さないのは、sink 表が仕様書の計画の「月 3」に**凍結**した語彙だからです。
凍結は「決めたものを後から変えない」約束で、結果を見た後に表を足すと、「都合のよい結果が出るように表を選んだ」ことと区別できなくなります。
そこで O39 として既知の限界に記録し、件数を併記する、という扱いにしています。
（出典: `docs/open_questions.md:1041-1049`）

#### 確認問題 13-4

効果を **2 つ**（`FS_READ` と `FS_WRITE`）出します。

| 宣言 | 解析器の結果 |
|---|---|
| D1 | `FS_WRITE` の効果が **矛**（`fs_write`）。`FS_READ` の効果は内 |
| D2（`path` は定数） | **不**（`fs_unknown`）。`destructive` が `null` で「決まらない」の類になり、書き先をモデルが選べないから |
| D4 | **不**（`fs_mode_unknown`） |

理由: モードが読めないときに片方に決めると、「書くかもしれない」（または「読むだけかもしれない」）可能性が記録から消えるので、規則 4「解決できなかったものは不明として記録する。黙って安全側に倒さない」に従い、**clean に潰さず両方を出す**ためです（`authgap/effects.py:656-663`）。
3 つとも、本記録者の作例の走査で確かめました（D1 は書き先がモデルの値の作例で確かめた）。
