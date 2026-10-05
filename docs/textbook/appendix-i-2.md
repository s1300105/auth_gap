[← 前](appendix-i-1.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-3.md)

---

# 付録 I-2 誤になる例 — 解析器の指摘が外れる形と誤の原因 E1〜E9

**この分冊の答えは、本書の答え（本記録者の判定）です。** 最終評価の判定は、学生が手引きで行います。

<a id="ai-2-0"></a>
## この分冊で学ぶこと

この分冊は、解析器が**矛**（宣言に反する、という指摘）を出したのに、正しい判定は**誤**になる例を集めました。
誤とは、解析器の指摘が外れていた、という判定です（手引き 11.2）。
誤にしたときは、外れた理由を**誤の原因**（E1〜E9）として `error_class` 欄に書きます（手引き 17）。

誤になる道は 2 つあります（手引き 11.2 の表）。

- **問い 1 が「いいえ」**: 効果の行は、ツールの呼び出しでは実行されない（到達しない）。E1・E3・E4・E6 がこちらです。
- **問い 2 が「いいえ」**: 実行はされるが、宣言には反しない。E2・E5・E7・E8 がこちらです。

E9 は「その他」です。迷ったら E9 にして説明を書きます（手引き 17 の結び）。

**例の作り方**: どの例も、この分冊のために作った小さな FastMCP のサーバ（作った例）です。凍結版の解析器（`analyzer-freeze-3`）で
実際に走査し、判定表の行は本物の出力から写しました（本書の試験）。走査の前に `git diff analyzer-freeze-3 -- authgap/` が
空であることを確かめました。コードの左の数字は行番号です。写して使うときは消してください。

**解析器がなぜ外したか**も、例ごとに `authgap/` の `ファイル:行` で書きます。これは判定の材料ではありません。
判定するのはコードの動作で、解析器の説明ではないからです（手引き 11.2）。仕組みを知ると、似た形を見つけやすくなります。

**記録の書き方の約束**（手引き 手順 H の「書き方の既定」、D76）:

- 11.2 の表の「—」の欄は空欄にします。到達しないときは `violates` を空欄にします。
- `condition_type`・`condition` は、到達するときだけ書きます。
- 誤の原因が E3・E4 なら `reachable` は `いいえ`、E5 なら `violates` は `いいえ` にします。
- `write_target` は正のときだけ付けます。誤には付けません。
- `evidence` は木の根からの相対の `ファイル:行` で書きます。表では、空欄を「（空）」と書きます。

**この分冊の地図**:

| 誤の原因 | 例 |
|---|---|
| E1 起動時の初期化 | [I-2.1](#ai-2-1)（lifespan）・[I-2.2](#ai-2-2)（読み込み時）。対比 [I-2.3](#ai-2-3)（`main()` なら正） |
| E2 同じ呼び出しの一時ファイル・ロック（D2） | [I-2.4](#ai-2-4)・[I-2.5](#ai-2-5) |
| E3 名前だけの解決の誤り | [I-2.6](#ai-2-6) |
| E4 受け手の型の読み違いで kind まで違う | [I-2.7](#ai-2-7)（凍結版では作れなかった。説明だけ） |
| E5 子プロセスへのパイプ | [I-2.8](#ai-2-8) |
| E6 到達しない（E1 以外） | [I-2.9](#ai-2-9)（定数で閉じた枝）・[I-2.10](#ai-2-10)（必ず先に抜ける） |
| E7 モデルが決められないのに決められるとした | [I-2.11](#ai-2-11) |
| E8 宣言に反しない（E2 以外） | [I-2.12](#ai-2-12)〜[I-2.16](#ai-2-16) |
| E9 その他（語彙・定義の差） | [I-2.17](#ai-2-17) |

関係する章: [第 49 章](ch49.md)（到達するかの決め方）、[第 50 章](ch50.md)（宣言に反するかの決め方）、
[第 51 章](ch51.md)（誤の原因 E1〜E9 の説明）。

---

<a id="ai-2-1"></a>
### I-2.1 lifespan で済ませる初期化（宣言 D1 / 判定: 誤 E1 / 一度だけの初期化はどこで先に済むかを見る）

**コード**（作った例）

```
 1  import os
 2  import sqlite3
 3  from contextlib import asynccontextmanager
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  DATA_DIR = os.path.expanduser("~/.notes_mcp")
 9  DB_PATH = os.path.join(DATA_DIR, "notes.db")
10  _conn = None
11
12
13  def _get_conn():
14      global _conn
15      if _conn is None:
16          os.makedirs(DATA_DIR, exist_ok=True)
17          _conn = sqlite3.connect(DB_PATH)
18          _conn.execute("CREATE TABLE IF NOT EXISTS notes (title TEXT, body TEXT)")
19      return _conn
20
21
22  @asynccontextmanager
23  async def app_lifespan(server):
24      _get_conn()
25      yield
26
27
28  mcp = FastMCP("notes", lifespan=app_lifespan)
29
30
31  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
32  def find_note(title: str) -> str:
33      """Find a note by title."""
34      row = _get_conn().execute("SELECT body FROM notes WHERE title = ?", (title,)).fetchone()
35      return row[0] if row else "not found"
```

**判定表の行**（解析器の出力。本書の試験。ツール `find_note`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:16` |
| D1 | `psycopg.Cursor.execute` | `DB` | `db_modify` | `server.py:18` |

2 組あります。下では 1 行目の組（`os.makedirs`）を判定します。2 行目の組も同じ理由で誤 E1 です
（site は `psycopg` と表示されますが、使っているのは `sqlite3` です。kind の `DB` は合っているので、判定には影響しません。手引き 手順 C）。
道筋（`witness_chain`）は `_get_conn`、入口の呼び出し行（`entry_lineno`）は 34 です。

**解析器がなぜ指摘したか**: 解析器は、ツールの道筋の `_get_conn()` に降り、15 行の `if` の両方の枝を読みます。
`if` の条件を定数として評価するのは、リテラルなどの限られた形だけです（`authgap/val/engine.py:2731-2735`。モジュール水準の名前は入らない）。
モジュール水準の `_conn` が起動時に入っていることは見ません（`authgap/val/engine.py:334-353`）。
lifespan の本体の効果は、ツールには付けません（`authgap/entry_seed.py:20-21`）。けれども、ツール自身が `_get_conn()` を呼ぶので、その中の効果が付きます。

**問い 1: 届くか**

- 道筋: `server.py:34`（`_get_conn()` を呼ぶ）→ `server.py:15`（`if _conn is None:`）→ `server.py:16`（`os.makedirs`）。
- 通る条件: `_conn is None`（一度だけの初期化の守り。手引き 手順 D の 4）。
- この初期化を先に済ませる場所を探します。28 行で `FastMCP(..., lifespan=app_lifespan)` と渡し、24 行の lifespan の中で `_get_conn()` を呼んでいます。
  lifespan は、どの起動方法でも、ツールの受付より前に必ず走ります（手引き 14.4 の表の lifespan の行）。
- lifespan が**必ず**済ませるかも見ます（手引き 14.4 の見分け方）。24 行に条件は無く、例外で抜けたらサーバの受付は始まりません。
- 済ませた後に `_conn = None` に戻す文が無いかを grep で確かめます。代入は 10 行だけです。
- 答え: **いいえ**（到達しない）。

**問い 2: 宣言に反するか** — 到達しないので問いません（11.2 の表の「—」）。参考までに、もし届けば 15.1 の FS_WRITE の行で反します。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | いいえ |
| condition_type | （空） |
| condition | （空） |
| violates | （空） |
| write_target | （空） |
| error_class | `E1: lifespan の app_lifespan（server.py:22-25）が起動時に _get_conn() を済ませ、_conn が入るので、ツールの呼び出しでは server.py:15 の if が偽になり :16 に来ない` |
| unknown_reason | （空） |
| evidence | `server.py:34 find_note が _get_conn() を呼ぶ → server.py:15 if _conn is None → server.py:16 os.makedirs。server.py:28 FastMCP(..., lifespan=app_lifespan) → server.py:24 で無条件に _get_conn() を済ませる。_conn への代入は server.py:10・:17 だけで、None に戻す文は無い` |

**この例で学ぶこと**: lifespan の中で必ず済む初期化は、ツールの呼び出しでは届かない（E1）。
**同じ初期化が `main()` の中だけなら答えが変わり**、到達する（[I-2.3](#ai-2-3)）。lifespan の中でも条件つき（環境変数が `1` のときだけ）なら、
既定の起動では最初の呼び出しで届く（[自分で判定してみる 問 1](#ai-2-y)）。

---

<a id="ai-2-2"></a>
### I-2.2 読み込み時に済ませる初期化（宣言 D1 / 判定: 誤 E1 / モジュールの一番上の文は import で走る）

**コード**（作った例）

```
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  INDEX_DIR = os.path.join(os.path.dirname(__file__), "index")
 8  _index = None
 9
10
11  def _load_index():
12      global _index
13      if _index is None:
14          os.makedirs(INDEX_DIR, exist_ok=True)
15          path = os.path.join(INDEX_DIR, "terms.json")
16          if not os.path.exists(path):
17              with open(path, "w") as fh:
18                  json.dump({}, fh)
19          with open(path) as fh:
20              _index = json.load(fh)
21      return _index
22
23
24  _load_index()
25  mcp = FastMCP("glossary")
26
27
28  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
29  def lookup_term(term: str) -> str:
30      """Look up a glossary term."""
31      return _load_index().get(term, "unknown term")
```

**判定表の行**（解析器の出力。本書の試験。ツール `lookup_term`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:14` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:17` |

下では 2 行目の組（`builtins.open`）を判定します。1 行目の組も同じ理由で誤 E1 です。道筋は `_load_index`、入口の呼び出し行は 31 です。

**解析器がなぜ指摘したか**: [I-2.1](#ai-2-1) と同じです。13 行の `if _index is None:` を定数として評価できず
（`authgap/val/engine.py:2731-2735`）、両方の枝を読みます。24 行の読み込み時の呼び出しで `_index` が入ることは見ません。

**問い 1: 届くか**

- 道筋: `server.py:31` → `server.py:13`（`if _index is None:`）→ `server.py:16`（`if not os.path.exists(path):`）→ `server.py:17`（`open(path, "w")`）。
- 24 行はモジュールの一番上の文です。モジュールを import した時点で `_load_index()` が走り、`_index` に辞書が入ります。
  `fastmcp run server.py:mcp` のように `main()` を通らない起動でも、モジュールの読み込みは必ず起きます。
- 手引き 14.4 の表の「モジュールの読み込み時」の行です。`_index` を `None` に戻す文も無い（代入は 8 行と 20 行だけ）。
- 答え: **いいえ**。

**問い 2: 宣言に反するか** — 到達しないので問いません。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | いいえ |
| condition_type | （空） |
| condition | （空） |
| violates | （空） |
| write_target | （空） |
| error_class | `E1: モジュールの読み込み時（server.py:24）に _load_index() が走り _index が入るので、ツールの呼び出しでは server.py:13 の if が偽になり :17 に来ない` |
| unknown_reason | （空） |
| evidence | `server.py:31 lookup_term → _load_index() → server.py:13 if _index is None → :16 → :17 open(path, "w")。server.py:24 のモジュールの一番上の _load_index() が import 時に済ませる。_index への代入は :8・:20 だけ` |

**この例で学ぶこと**: 「一度だけ」の守りを見たら、守りの外で先に呼ぶ場所（lifespan・モジュールの一番上・`main()`）を grep で探す。
**24 行が無く、`main()` の中で呼ぶだけなら答えが変わる**（次の [I-2.3](#ai-2-3)）。

---

<a id="ai-2-3"></a>
### I-2.3 対比: `main()` の中だけで済ませる初期化（宣言 D1 / 判定: 正 / 起動の方法で届く）

この分冊で唯一の正の例です。[I-2.2](#ai-2-2) と 1 か所だけ違い、E1 との境目を見るために置きました。

**コード**（作った例。[I-2.2](#ai-2-2) の 24 行を消し、`main()` を足したもの）

```
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  INDEX_DIR = os.path.join(os.path.dirname(__file__), "index")
 8  _index = None
 9
10
11  def _load_index():
12      global _index
13      if _index is None:
14          os.makedirs(INDEX_DIR, exist_ok=True)
15          path = os.path.join(INDEX_DIR, "terms.json")
16          if not os.path.exists(path):
17              with open(path, "w") as fh:
18                  json.dump({}, fh)
19          with open(path) as fh:
20              _index = json.load(fh)
21      return _index
22
23
24  mcp = FastMCP("glossary")
25
26
27  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
28  def lookup_term(term: str) -> str:
29      """Look up a glossary term."""
30      return _load_index().get(term, "unknown term")
31
32
33  def main():
34      _load_index()
35      mcp.run()
36
37
38  if __name__ == "__main__":
39      main()
```

**判定表の行**（解析器の出力。本書の試験。ツール `lookup_term`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:14` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:17` |

解析器の出力は [I-2.2](#ai-2-2) と同じです。解析器は、初期化をどこで先に済ませるかを見ていません。下では 2 行目の組を判定します。

**問い 1: 届くか**

- 道筋: `server.py:30` → `server.py:13` → `server.py:16` → `server.py:17`。
- 先に済ませる場所は、34 行の `main()` の中だけです。24 行の `mcp` はモジュールの一番上にあるので、`fastmcp run server.py:mcp` のように
  `main()` を通らずに起動できます。そのときは最初の呼び出しで 13 行の `if` が真になり、17 行まで届きます（手引き 14.4 の表の `main()` の行）。
- 条件の種類: `起動の方法`（手引き 14.3）。17 行には「`terms.json` が無いとき」という初回の条件も重なりますが、
  手引き 14.3 は「`起動の方法` の位置の効果が最初の呼び出しでだけ起きるときは、`初回` を重ねずに `起動の方法` だけを書く」と決めています（D76）。
- 答え: **はい**（条件つき）。

**問い 2: 宣言に反するか** — 17 行は `open(path, "w")` でファイルを作ります。15.1 の表の「ファイルの書き込み・作成…（`FS_WRITE` すべて）」の行です。
答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| reachable | はい |
| condition_type | `起動の方法` |
| condition | `main() を通らない起動（fastmcp run server.py:mcp など）で、最初の呼び出しのとき` |
| violates | はい |
| write_target | `キャッシュ・状態の保存`（作ったファイルを :19-20 で読み返す。16.1 の順 6） |
| error_class | （空） |
| unknown_reason | （空） |
| evidence | `server.py:30 lookup_term → _load_index() → server.py:13 if _index is None（main() を通らない起動では最初の呼び出しで真）→ :16 if not os.path.exists(path) → :17 open(path, "w")。先に済ませるのは server.py:34 の main() の中だけ` |

**この例で学ぶこと**: 同じ初期化でも、`main()` の中だけなら「到達する」（正になりうる）、lifespan・読み込み時なら「到達しない」（E1）。
解析器はこの区別をしないので、解析器に有利な側（この例）と不利な側（[I-2.1](#ai-2-1)・[I-2.2](#ai-2-2)）の両方が出ます（手引き 14.4 の結び）。
`起動の方法` は運用者が決める条件なので、(B)・(C) には数えません（手引き 14.3 の表）。

---

<a id="ai-2-4"></a>
### I-2.4 同じ呼び出しで作って消す一時ファイル（宣言 D2 / 判定: 誤 E2 / D2 は「呼び出しの前からあったもの」を問う）

**コード**（作った例）

```
 1  import os
 2  import subprocess
 3  import tempfile
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("lint")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
12  def lint_snippet(code: str) -> str:
13      """Lint a Python snippet and return the report."""
14      fd, tmp = tempfile.mkstemp(suffix=".py")
15      try:
16          with os.fdopen(fd, "w") as fh:
17              fh.write(code)
18          out = subprocess.run(["pyflakes", tmp], capture_output=True, text=True)
19          return out.stdout or "no problems"
20      finally:
21          os.remove(tmp)
```

**判定表の行**（解析器の出力。本書の試験。ツール `lint_snippet`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.remove` | `FS_WRITE` | `fs_remove` | `server.py:21` |

（同じツールには、18 行の `subprocess.run` に D2 の**不**（`spawn_command`）も出ています。不は矛の判定表には載らないので、ここでは判定しません。）

**解析器がなぜ指摘したか**: `os.remove` は「既存のものを消す」型の sink です（`authgap/catalog/sinks.py:363` の `destructive=True`）。
D2 の規則はこれを `fs_remove` の矛にします（`authgap/dparse.py:355-370` の `_fs_class`、`:409`）。消す物が**同じ呼び出しで作った物か**は見ていません。

**問い 1: 届くか**

- 道筋: 本体の中です。14 行で一時ファイルを作り、20 行の `finally` で 21 行が必ず走ります。
- 答え: **はい**（条件なし）。手引き 14.5「同じ呼び出しの中で作って消すものは、到達はする」。

**問い 2: 宣言に反するか**

- D2 の問いは「呼び出しの前からあったものを消す・上書きする・変えるか」です（手引き 15.2）。
- 21 行が消す `tmp` は、14 行の `mkstemp` がこの呼び出しで新しく作ったファイルです。呼び出しの前には無かった物です。
- 15.2 の迷いやすい形「同じ呼び出しで自分が作った一時ファイル・ロックファイルを消す → 反しない（誤、E2）」に当たります。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E2: server.py:21 が消すのは、同じ呼び出しの :14 で mkstemp が作った一時ファイル tmp` |
| unknown_reason | （空） |
| evidence | `server.py:14 tempfile.mkstemp で新しい一時ファイルを作る → :16-17 code を書く → :18 pyflakes に渡す → :21 finally で os.remove(tmp)。tmp は :14 の戻り値だけ` |

**この例で学ぶこと**: 同じコードでも、**宣言が D1（読み取り専用）なら答えが変わり、正**になる（15.1: 一時ファイルの作成・削除も環境の変更。
[自分で判定してみる 問 3](#ai-2-y)）。D2 なら誤 E2。また、21 行が**前の呼び出しが残したファイル**を消すのなら、D2 でも反する（15.2）。

---

<a id="ai-2-5"></a>
### I-2.5 ロックファイルと、途中で止まった前の呼び出しの残り物（宣言 D2 / 判定: 誤 E2 / D76 の規則）

**コード**（作った例）

```
 1  import os
 2  import time
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("reports")
 8  STATE_DIR = os.path.expanduser("~/.reports_mcp")
 9  LOCK = os.path.join(STATE_DIR, "build.lock")
10
11
12  def _acquire():
13      os.makedirs(STATE_DIR, exist_ok=True)
14      if os.path.exists(LOCK) and time.time() - os.path.getmtime(LOCK) > 600:
15          os.remove(LOCK)  # 前の呼び出しが途中で止まって残したロック
16      with open(LOCK, "x") as fh:
17          fh.write(str(os.getpid()))
18
19
20  def _release():
21      os.remove(LOCK)
22
23
24  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
25  def build_report(month: str) -> str:
26      """Build the monthly report text."""
27      _acquire()
28      try:
29          return f"report for {month}"
30      finally:
31          _release()
```

**判定表の行**（解析器の出力。本書の試験。ツール `build_report`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.remove` | `FS_WRITE` | `fs_remove` | `server.py:15`, `server.py:21` |

1 組に 2 つの位置があります。15 行の道筋は `_acquire`（入口 27 行）、21 行の道筋は `_release`（入口 31 行）です。
16 行の `open(LOCK, "x")` は矛になっていません。解析器は `'x'` を追加型（新しく作るだけ）と読みます（`authgap/effects.py:298-318`）。

**解析器がなぜ指摘したか**: [I-2.4](#ai-2-4) と同じです。`os.remove` は消す型で、消す物の出どころは見ません。

**問い 1: 届くか**

- 21 行: `server.py:31`（`finally`）→ `server.py:21`。毎回届きます。
- 15 行: `server.py:27` → `server.py:14`（ロックが残っていて 600 秒より古いとき）→ `server.py:15`。条件つきで届きます。
- 答え: **はい**（どちらの位置も）。

**問い 2: 宣言に反するか**（手順 G: 誤にするときは全部の位置を読む）

- 21 行: 消すのは、同じ呼び出しの 16 行で作ったロックです。15.2「同じ呼び出しで自分が作った…ロックファイルを消す → 反しない（誤、E2）」。
- 15 行: 消すのは、**前の呼び出しが途中で止まって残した**ロックです。一見「前の呼び出しが残したファイルを消す → 反する」に見えます。
  けれども 15.2 は D76 で次の行を足しています。「毎回作って消すロック・一時ファイルを、前の呼び出しが途中で止まって残していたとき:
  ふつうの流れで決める（反しない、誤 E2）。途中で止まった後の残り物は異常時のもので、上の『前の呼び出しが残したファイル』には入れない」。
  このロックは、ふつうの流れでは 21 行で消える物です。
- 2 つの位置とも反しないので、組は**反しない**。答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E2: server.py:21 は同じ呼び出しの :16 で作ったロックを消す。:15 は前の呼び出しが途中で止まって残したロックで、ふつうの流れで決める（15.2、D76）` |
| unknown_reason | （空） |
| evidence | `server.py:27 _acquire → :16 open(LOCK, "x") でロックを作る → server.py:31 finally で _release → :21 os.remove(LOCK)。:15 の os.remove は :14 で 600 秒より古いロックが残っているときだけで、ロックを作るのは :16 だけ（grep "LOCK"）` |

**この例で学ぶこと**: 毎回作って消すロックは、途中で止まった前の呼び出しの残りを消しても誤 E2（D76）。
**消す物が、前の呼び出しが正常に残したもの（前回の出力ファイルなど）なら答えが変わり、反する**（15.2）。
手順 G のとおり、`note` には「:15 と :21 の両方を読み、どちらも E2」と書いておきます。

---

<a id="ai-2-6"></a>
### I-2.6 組み込みの `set()` を木の中の `CacheManager.set` と取り違える（宣言 D1 / 判定: 誤 E3 / 道筋の段を開いて受け手を確かめる）

**コード**（作った例。v4 の rails-lens（M04）と同じ形を、小さく作り直したもの）

```
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("deps")
 8  CACHE_DIR = os.path.expanduser("~/.deps_cache")
 9
10
11  class CacheManager:
12      def __init__(self, root):
13          self.root = root
14
15      def get(self, key):
16          p = os.path.join(self.root, key + ".json")
17          if os.path.exists(p):
18              with open(p) as fh:
19                  return json.load(fh)
20          return None
21
22      def set(self, key, value):
23          os.makedirs(self.root, exist_ok=True)
24          with open(os.path.join(self.root, key + ".json"), "w") as fh:
25              json.dump(value, fh)
26
27
28  GRAPH = {"app": ["lib", "util"], "lib": ["util"], "util": []}
29
30
31  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
32  def dependency_graph(root: str) -> str:
33      """Return all modules reachable from root."""
34      visited: set[str] = set()
35      stack = [root]
36      while stack:
37          mod = stack.pop()
38          if mod in visited:
39              continue
40          visited.add(mod)
41          stack.extend(GRAPH.get(mod, []))
42      return json.dumps(sorted(visited))
```

**判定表の行**（解析器の出力。本書の試験。ツール `dependency_graph`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:23` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:24` |

どちらの組も道筋は `CacheManager.set`、入口の呼び出し行は 34 です。下では 2 行目の組を判定します。1 行目も同じ理由で誤 E3 です。
（41 行の `GRAPH.get` も `CacheManager.get` に結ばれ、18 行の読み取りが付いています。読み取りは D1 の矛にならないので表に出ません。）

**解析器がなぜ指摘したか**: 解析器は、呼び出しの末尾の名前（`set`）で木の中の定義を引きます（`authgap/val/engine.py:988`）。
`set()` は属性の呼び出しではないので、まず関数を探し、無ければメソッドの候補を残します（`:1005-1007`）。
候補が `CacheManager.set` の 1 つだけなので、それに降ります。受け手の型で裏付けられない解決でも、真の経路を消さないために降りるのが
解析器の方針です（D17 の改訂。`:1036-1046` の注釈）。この例の効果の確度（`resolution`）は opaque と記録されましたが、
D1 の規則は確度を問わず `FS_WRITE` を `fs_write` の矛にします（`authgap/dparse.py:379-380`）。

**問い 1: 届くか**

- 入口の呼び出し行 34 を開きます。`visited: set[str] = set()` は、Python の組み込みの `set` 型の空の集合を作るだけです。
- `CacheManager` の実体を作る文（`CacheManager(`）を grep で探すと、木の中にありません。22〜25 行の `set` メソッドは、どの道筋からも呼ばれません。
- 手引き 手順 C の「組み込みの `set()`…を、木の中の同名のメソッド（`CacheManager.set` など）と取り違えていないか」に当たります。
- 答え: **いいえ**。

**問い 2: 宣言に反するか** — 到達しないので問いません。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | いいえ |
| condition_type | （空） |
| condition | （空） |
| violates | （空） |
| write_target | （空） |
| error_class | `E3: server.py:34 の set() は組み込みの set 型で、木の中の CacheManager.set（:22）は呼ばれない` |
| unknown_reason | （空） |
| evidence | `server.py:34 visited: set[str] = set()（組み込みの set）。witness_chain の CacheManager.set（server.py:22-25）は、木の中に CacheManager( の文が無く、どこからも呼ばれない（grep "CacheManager"）` |

**この例で学ぶこと**: 道筋の段は、名前ではなく受け手（何の物か）で確かめる。エディタの「定義へ移動」も名前で当てることがある（手引き 12.2）。
**ツールが `cache = CacheManager(CACHE_DIR)` を作って `cache.set(root, result)` と呼んでいたら答えが変わり、到達する（正になりうる）。**
組み込みの `dict.update` を木の中の同名メソッドと取り違える形は [自分で判定してみる 問 2](#ai-2-y) で。

---

<a id="ai-2-7"></a>
### I-2.7 E4 について — 凍結版の解析器では作れなかった類（例ではなく説明）

E4 は「受け手の型の読み違いで、**動作の種類（kind）まで違う**」誤です（手引き 17）。
site の名前（ライブラリの名前）だけが違って kind が合っているなら、E4 にしません（手引き 手順 C。[I-2.1](#ai-2-1) の `psycopg` の表示がその例）。

本書は、E4 の形を凍結版の解析器で作ろうとしましたが、作れませんでした。試した形は次のとおりです（本書の試験）。

```
（vfs.py）
 1  _FILES: dict[str, str] = {}
 2
 3
 4  class Path:
 5      """メモリの中だけの小さなファイルの入れ物（下書きのプレビュー用）。"""
 6
 7      def __init__(self, name):
 8          self.name = name
 9
10      def write_text(self, text):
11          _FILES[self.name] = text
12
13      def read_text(self):
14          return _FILES.get(self.name, "")

（server.py）
 1  from mcp.server.fastmcp import FastMCP
 2  from mcp.types import ToolAnnotations
 3
 4  from vfs import Path
 5
 6  mcp = FastMCP("preview")
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
10  def preview_markdown(title: str, body: str) -> str:
11      """Render a markdown preview."""
12      page = Path("preview.md")
13      page.write_text(f"# {title}\n\n{body}\n")
14      return page.read_text()
```

木の中の `Path`（メモリの入れ物）を、標準ライブラリの `pathlib.Path`（ファイル）と取り違えれば E4 になる形です。
解析器は `preview_markdown` に**何の行も出しませんでした**（矛も不も無し）。import の表で `vfs.Path` に結んでいます。
[第 51 章 51.11](ch51.md#s51-12) でも、受け手を取り違えさせる作例を 10 の形で試し、どれも効果を出さなかったと報告しています。

**判定でどう使うか**: E4 は v3・v4 でも出ていません。出会ったら、手順 C で受け手がどこで作られた何の物かをたどり、
「ライブラリが違い、kind も違い、実際の動作が宣言に反しない」ときだけ E4 にします。
kind は違うが実際の動作も宣言に反する形は、手引きで決まっていません（[第 51 章 51.11](ch51.md#s51-12) の「未決」。出会ったら 22 節）。

---

<a id="ai-2-8"></a>
### I-2.8 ファイルを変えない子プロセスへのパイプ（宣言 D1 / 判定: 誤 E5 / 子の動作を全部見る）

**コード**（作った例）

```
 1  import subprocess
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("textutil")
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
10  def count_words(text: str) -> str:
11      """Count the words in a text."""
12      proc = subprocess.Popen(["wc", "-w"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
13      out, _ = proc.communicate(input=text)
14      return out.strip()
```

**判定表の行**（解析器の出力。本書の試験。ツール `count_words`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `pipe:communicate` | `FS_WRITE` | `fs_write` | `server.py:13` |

（12 行の `subprocess.Popen` には D1 の不（`spawn_command`）が出ています。ここでは判定しません。）

**解析器がなぜ指摘したか**: `Popen` の物に対する `communicate(input=…)` を、子プロセスへの書き込みとして記録します。
シェル経由でもインタプリタでもなければ、kind を `FS_WRITE` にします（`authgap/effects.py:803-860` の `_pipe`、とくに `:844-847`）。
D1 は `FS_WRITE` をすべて `fs_write` の矛にします（`authgap/dparse.py:379-380`）。

**問い 1: 届くか** — 13 行は本体の中で、条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- 手順 C: `pipe:communicate` は子プロセスの標準入力への書き込みで、ファイルの書き込みとは限りません。
- 15.1 の迷いやすい形「子プロセスの標準入力への書き込み: それ自体はファイルを変えない。子プロセスがそれを受けて何をするかで決める」。
  pipe の組では、子の動作は全部数えます（D76）。
- 子は `wc -w` で、引数は定数です。`wc` は入力を読み、数を標準出力に書くだけです。POSIX の `wc` の仕様の OUTPUT FILES は「None」です
  （<https://pubs.opengroup.org/onlinepubs/9799919799/utilities/wc.html> を開いて確かめた。手引き 19 の「公式の文書かソースを自分で開けたとき」）。
- 子は環境を変えません。答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E5: server.py:13 は子プロセス wc -w の標準入力に text を流すだけ。wc は数を標準出力に書くだけで、ファイルを変えない` |
| unknown_reason | （空） |
| evidence | `server.py:12 Popen(["wc", "-w"], stdin=PIPE, stdout=PIPE) → :13 communicate(input=text) → :14 標準出力の数を返す。wc の OUTPUT FILES は None（https://pubs.opengroup.org/onlinepubs/9799919799/utilities/wc.html）` |

**この例で学ぶこと**: パイプの組は、子が何をするかで決める。
**子が `tee -a <ファイル>` のように受け取った内容をファイルに足すなら答えが変わり、正**（[自分で判定してみる 問 6](#ai-2-y)）。
子が一時ファイルに書くだけでも、D1 では反する（v4 の M59 は最終評価の規則では正。手引き 20.2）。

---

<a id="ai-2-9"></a>
### I-2.9 定数で閉じた枝 `if DEBUG:`（宣言 D1 / 判定: 誤 E6 / 運用者が書き換える設定かを見分ける）

**コード**（作った例）

```
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("weather")
 8  DEBUG = False
 9  DUMP_DIR = "/tmp/weather_debug"
10
11
12  def _fetch(city):
13      return {"city": city, "temp": 21}
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def get_weather(city: str) -> str:
18      """Return the current weather for a city."""
19      data = _fetch(city)
20      if DEBUG:
21          os.makedirs(DUMP_DIR, exist_ok=True)
22          with open(os.path.join(DUMP_DIR, "last.json"), "w") as fh:
23              json.dump(data, fh)
24      return json.dumps(data)
```

**判定表の行**（解析器の出力。本書の試験。ツール `get_weather`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:21` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:22` |

下では 2 行目の組を判定します。1 行目も同じ理由で誤 E6 です。

**解析器がなぜ指摘したか**: 解析器は、条件が定数で決まる `if` では取られる枝だけを読みます（`authgap/val/engine.py:334-343`、D58）。
けれども定数として評価するのは、リテラルなどの限られた形だけです（`:2731-2735`）。モジュール水準の `DEBUG` は評価せず、両方の枝を読みます。
本書の試験では、`if False:` と書いた枝は解析器も捨てました（行が出なかった）。

**問い 1: 届くか**

- 道筋: 本体の 20 行の `if DEBUG:` の中です。
- `DEBUG` の代入を grep で探すと、8 行の `DEBUG = False` だけです。`global DEBUG` も、別のモジュールからの書き換えもありません。
- この `DEBUG` は `server.py` の中の開発用の印で、運用者が書き換える前提の設定ファイル（`config.py`）の定数ではありません
  （運用者に書き換えを求める説明は、コメントにも文書にもありません）。
- 手引き 14.2 の表の「定数で閉じた枝」の行（`if DEBUG:`（`DEBUG = False` が定数で、どこでも書き換えない）の中）です。
- 答え: **いいえ**。

**問い 2: 宣言に反するか** — 到達しないので問いません。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | いいえ |
| condition_type | （空） |
| condition | （空） |
| violates | （空） |
| write_target | （空） |
| error_class | `E6: server.py:20 の if DEBUG は、:8 の DEBUG = False（木の中で書き換えない）で閉じた枝` |
| unknown_reason | （空） |
| evidence | `server.py:8 DEBUG = False → server.py:20 if DEBUG:（常に偽）→ :21-23 には来ない。DEBUG への代入は :8 だけ（grep "DEBUG"）` |

**この例で学ぶこと**: 定数で閉じた枝は E6。ただし、**同じ `DEBUG` が「運用者が書き換える」と書かれた `config.py` にあるなら答えが変わり**、
14.3 の `運用者の設定` で到達する（D76。[自分で判定してみる 問 5](#ai-2-y)）。境目は「運用者が書き換える前提か」で、grep と説明の文で確かめる。

---

<a id="ai-2-10"></a>
### I-2.10 効果の前に必ず例外を投げる（宣言 D1 / 判定: 誤 E6 / 呼び出し先が必ず抜けるかも見る）

**コード**（作った例）

```
 1  import csv
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("sales")
 8  EXPORT_DIR = os.path.expanduser("~/exports")
 9
10
11  def _require_pro():
12      raise PermissionError("CSV export is only available in the pro edition")
13
14
15  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
16  def sales_summary(region: str, export: bool = False) -> str:
17      """Summarize sales for a region."""
18      rows = [("2026-09", 120), ("2026-10", 95)]
19      if export:
20          _require_pro()
21          os.makedirs(EXPORT_DIR, exist_ok=True)
22          with open(os.path.join(EXPORT_DIR, "sales.csv"), "w", newline="") as fh:
23              csv.writer(fh).writerows(rows)
24      return f"{region}: {sum(n for _, n in rows)}"
```

**判定表の行**（解析器の出力。本書の試験。ツール `sales_summary`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:21` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:22` |

下では 2 行目の組を判定します。1 行目も同じ理由で誤 E6 です。

**解析器がなぜ指摘したか**: 同じ本体の中の `raise` や `return` は、その後の文を読まない印になります（`authgap/val/engine.py:328-333`・`:383-386`）。
本書の試験でも、本体に直接 `return` や `raise` を書いてから `open` を置いた作例には、行が出ませんでした。
けれども、**呼び出し先が必ず例外を投げる**ことは、呼び出し元の 21〜23 行には持ち込まれませんでした。

**問い 1: 届くか**

- 道筋: `server.py:19`（`if export:`。引数で通れる）→ `server.py:20`（`_require_pro()`）→ `server.py:12`（無条件の `raise PermissionError`）。
- `_require_pro` の定義は 11 行だけで（grep `_require_pro`）、中は無条件の `raise` です。20 行の呼び出しは必ず例外で抜けます。
  例外を捕まえる `try` も、本体にはありません。
- 21・22 行には、どの実行の道でも来ません。手引き 14.2 の表の「必ず先に抜ける（効果の前に必ず `return` / `raise` する）」の行です。
- 答え: **いいえ**。

**問い 2: 宣言に反するか** — 到達しないので問いません。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | いいえ |
| condition_type | （空） |
| condition | （空） |
| violates | （空） |
| write_target | （空） |
| error_class | `E6: server.py:20 の _require_pro() が必ず PermissionError を投げる（:12）ので、:21-23 に来ない` |
| unknown_reason | （空） |
| evidence | `server.py:19 if export → :20 _require_pro() → server.py:12 raise PermissionError（無条件）。_require_pro の定義は :11 だけ。:21-22 には来ない` |

**この例で学ぶこと**: 「引数で通れる枝」でも、その中で必ず抜けるなら到達しない。条件の種類（`引数`）を書く前に、枝の中を最後まで読む。
**`_require_pro()` が「ライセンスのファイルが無いときだけ」投げるなら答えが変わり**、ファイルがあるときに届く（`外部の状態` か `運用者の設定`。
運用者が置く目印のファイルなら `運用者の設定`。手引き 14.3 の迷いやすい条件の表）。

---

<a id="ai-2-11"></a>
### I-2.11 `shlex.quote` した値だけを渡すシェル（宣言 D1 / 判定: 誤 E7 / 「モデルが決められる」を自分で確かめる）

**コード**（作った例）

```
 1  import os
 2  import shlex
 3  import subprocess
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("search")
 9  NOTES_DIR = os.path.expanduser("~/notes")
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def grep_notes(pattern: str) -> str:
14      """Search the notes folder for a pattern."""
15      cmd = f"grep -rn -e {shlex.quote(pattern)} -- {shlex.quote(NOTES_DIR)}"
16      out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
17      return out.stdout or "no match"
```

**判定表の行**（解析器の出力。本書の試験。ツール `grep_notes`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_model` | `server.py:16` |

**解析器がなぜ指摘したか**: シェルの文字列（slot `shell_string`）にモデルの値 `pattern` が確度 resolved で流れ込むので、
「モデルが選べる」（`chosen`）とし、`spawn_model` の矛にします（`authgap/dparse.py:245-272` の `_choice`・`_by_choice`、`:377-378`）。
`shlex.quote` は、値の解析（val）では属性として記録するだけで、等級を付けません（`authgap/val/engine.py:7-10`）。

**問い 1: 届くか** — 16 行は本体の中で、条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- 15.1 の SPAWN の行: 「起動するコマンドをモデルが決められるなら反する。コマンドが定数なら、そのコマンドが実際に何をするかを調べ…」。
- モデルが決められるかを自分で確かめます。15 行で `pattern` は `shlex.quote` で囲まれ、シェルには 1 つの引数として渡ります。
  `;` や `$(…)` を入れても、別のコマンドにはなりません。起動するのは定数の `grep` です。
- 15.1 の迷いやすい形「定数のコマンドに、モデルが引数・オプションを渡す: 引数にも原理 3-a を当てる。モデルが書けるオプションに環境を変えるものがあれば反する」。
  `pattern` は `-e` の直後なので、`-` で始めてもオプションにならず、パターンとして読まれます。
- `grep` は入力を読み、一致した行を標準出力に書くだけです。POSIX の `grep` の仕様の OUTPUT FILES は「None」です
  （<https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html> を開いて確かめた）。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E7: server.py:15 のモデルの値 pattern は shlex.quote で 1 つの引数に閉じ、-e の後のパターンにしかならない。起動するのは定数の grep で、モデルはコマンドを決められない` |
| unknown_reason | （空） |
| evidence | `server.py:15 cmd = f"grep -rn -e {shlex.quote(pattern)} -- {shlex.quote(NOTES_DIR)}" → :16 subprocess.run(cmd, shell=True)。grep は一致行を標準出力に書くだけ（OUTPUT FILES: None。https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html）` |

**この例で学ぶこと**: 解析器の「モデルが決められる」は、値が流れ込むことしか見ていない。E7 は手引き 17 の見分け方
「固定のコマンドに `shlex.quote` した値だけを渡す spawn など」の形。
**`shlex.quote` が無い（`f"grep -rn {pattern} ~/notes"`）なら答えが変わり**、モデルが `x; rm -rf ~` のように別のコマンドを書けるので反する（正）。

---

<a id="ai-2-12"></a>
### I-2.12 読み取りのモードを書き込みと読む（宣言 D1 / 判定: 誤 E8 / `open` のモードを自分で読む）

**コード**（作った例）

```
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("files")
 7  ROOT = os.path.expanduser("~/notes")
 8
 9
10  def _read(path, binary=False):
11      mode = "rb" if binary else "r"
12      with open(path, mode) as fh:
13          return fh.read()
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def read_note(name: str) -> str:
18      """Read a note from the notes folder."""
19      return _read(os.path.join(ROOT, os.path.basename(name)))
```

**判定表の行**（解析器の出力。本書の試験。ツール `read_note`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:12` |

道筋は `_read`、入口の呼び出し行は 19 です。

**解析器がなぜ指摘したか**: `open` の mode が定数で読めないとき、解析器は「読み取りか書き込みか決めない」とし、
`FS_READ` と `FS_WRITE` の**両方**の効果を出します（`authgap/effects.py:246-261` の `_mode_is_write`、`:656-663`）。
11 行の `"rb" if binary else "r"` は 2 つの値の合流なので、定数になりません。その `FS_WRITE` が D1 の矛になります（`authgap/dparse.py:379-380`）。

**問い 1: 届くか** — `server.py:19` → `server.py:10`（`_read`）→ `server.py:12`。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- 手順 C: `builtins.open` なら開くモードを見ます。読み取り（`'r'`）なら書き込みではありません。
- 11 行の `mode` は `"rb"` か `"r"` のどちらかで、どちらも読み取りです。19 行は `binary` を渡さないので、実際は `"r"` です。
- 15.1 の表の「ファイルの読み取り → 反しない」の行です。手引き 17 の E8 の例にも「読み取りのモード」があります。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E8: server.py:12 の mode は :11 で "rb" か "r" のどちらかで、どちらも読み取り。ファイルに書かない` |
| unknown_reason | （空） |
| evidence | `server.py:19 read_note → :10 _read(path)（binary は既定の False）→ :11 mode = "r" → :12 open(path, mode) → :13 fh.read()` |

**この例で学ぶこと**: 解析器は読めないモードを「書くかもしれない」と出す。人はモードの取りうる値を全部読む。
**モードがツールの引数（`mode: str = "r"`）なら答えが変わり**、モデルが `"w"` を渡せるので反する（正。原理 3-a。[自分で判定してみる 問 8](#ai-2-y)）。

---

<a id="ai-2-13"></a>
### I-2.13 標準エラーへのログ（宣言 D1 / 判定: 誤 E8 / ファイルの名前でなく行き先で決める）

**コード**（作った例）

```
 1  from mcp.server.fastmcp import FastMCP
 2  from mcp.types import ToolAnnotations
 3
 4  mcp = FastMCP("calc")
 5
 6
 7  def _trace(msg):
 8      with open("/dev/stderr", "a") as log:
 9          log.write(msg + "\n")
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def add(a: float, b: float) -> str:
14      """Add two numbers."""
15      _trace(f"add {a} {b}")
16      return str(a + b)
```

**判定表の行**（解析器の出力。本書の試験。ツール `add`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:8` |

道筋は `_trace`、入口の呼び出し行は 15 です。

**解析器がなぜ指摘したか**: `open(…, "a")` は書き込みの効果です。D1 の規則は、行き先を問わず `FS_WRITE` をすべて矛にします（`authgap/dparse.py:379-380`）。

**問い 1: 届くか** — `server.py:15` → `server.py:7` → `server.py:8`。毎回届きます。答え: **はい**。

**問い 2: 宣言に反するか**

- 8 行が開くのは `/dev/stderr`、つまりこのプロセスの標準エラーです。ディスク上の利用者のファイルやログファイルではありません。
- 15.1 の迷いやすい形「標準出力・標準エラーへのログ: ファイルではないので反しない（`logging` の出力先がファイルなら反する。出力先の設定を確かめる）」。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E8: server.py:8 が開くのは /dev/stderr（プロセスの標準エラー）で、15.1 の標準エラーへのログ。ファイルではない` |
| unknown_reason | （空） |
| evidence | `server.py:15 add → :7 _trace → :8 open("/dev/stderr", "a") → :9 log.write(msg)` |

**この例で学ぶこと**: 同じ `open(…, "a")` でも、**行き先が `~/calc.log` なら答えが変わり、正**（ラベルはログ）。
似た「反しない」形に、**プロセスのメモリの中の状態**（モジュール水準の辞書のキャッシュなど）があります。これは D1 の違反にしません（15.1、D76 の 2。6 (a) は A）。
凍結版の解析器は、辞書のキャッシュにそもそも効果を出しません（本書の試験で、モジュール水準の `_CACHE[currency] = …` だけのツールには行が出なかった）。
そのため、この形は矛の誤としては出てきません。

---

<a id="ai-2-14"></a>
### I-2.14 同じ呼び出しで作ったファイルの権限を変える（宣言 D2 / 判定: 誤 E8 / 「既存のもの」かを見る）

**コード**（作った例）

```
 1  import os
 2  import uuid
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("keys")
 8  KEY_DIR = os.path.expanduser("~/.keys_mcp")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
12  def new_api_token(label: str) -> str:
13      """Create a new API token file and return its path."""
14      os.makedirs(KEY_DIR, exist_ok=True)
15      path = os.path.join(KEY_DIR, f"{uuid.uuid4().hex}.token")
16      with open(path, "x") as fh:
17          fh.write(f"{label}:{uuid.uuid4().hex}\n")
18      os.chmod(path, 0o600)
19      return path
```

**判定表の行**（解析器の出力。本書の試験。ツール `new_api_token`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.chmod` | `FS_WRITE` | `fs_remove` | `server.py:18` |

14 行の `os.makedirs` と 16 行の `open(path, "x")` は矛になっていません。解析器はどちらも「新しく作るだけ」の型と読みます
（`authgap/catalog/sinks.py:366`、`authgap/effects.py:298-318`）。

**解析器がなぜ指摘したか**: `os.chmod` は「既存のものを変える」型の sink です（`authgap/catalog/sinks.py:370` の `destructive=True`）。
D2 の規則はこれを `fs_remove` の矛にします（`authgap/dparse.py:409`）。権限を変えるファイルが呼び出しの前からあったかは見ません。

**問い 1: 届くか** — 18 行は本体の中で、条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- D2 の問いは「呼び出しの前からあったものを消す・上書きする・変えるか」です（手引き 15.2）。表の `chmod` の行も「**既存のもの**を…変える」です。
- 18 行が権限を変える `path` は、15 行で乱数（`uuid4`）の名前を作り、16 行の `'x'`（すでにあれば失敗する、新規作成だけのモード）で、この呼び出しが作ったファイルです。
  呼び出しの前には無かった物です。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E8: server.py:18 が権限を変えるのは、同じ呼び出しの :16 で 'x' で新しく作ったファイル（名前は :15 の uuid4）で、呼び出しの前からあったものではない` |
| unknown_reason | （空） |
| evidence | `server.py:15 path = KEY_DIR/<uuid4>.token → :16 open(path, "x")（すでにあれば失敗）→ :18 os.chmod(path, 0o600)。path は :15 の値だけ` |

**この例で学ぶこと**: E2 は「同じ呼び出しで作った**一時ファイル・ロックの後始末**」に限る類。後始末ではない形で反しないときは E8 にする（手引き 17）。
**`os.chmod` の対象がモデルの決めるパス（引数）なら答えが変わり**、既存のファイルを指せるので反する（正。15.2、原理 3-a）。

---

<a id="ai-2-15"></a>
### I-2.15 書く前に確かめる追記（宣言 D4 / 判定: 誤 E8 / 2 回目に何が起きるかを追う）

**コード**（作った例）

```
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("todo")
 7  TODO = os.path.expanduser("~/todo.txt")
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
11  def ensure_todo(item: str) -> str:
12      """Add an item to the todo list unless it is already there."""
13      item = " ".join(item.split())
14      text = ""
15      if os.path.exists(TODO):
16          with open(TODO) as fh:
17              text = fh.read()
18      if item in text.splitlines():
19          return "already present"
20      with open(TODO, "a") as fh:
21          if text and not text.endswith("\n"):
22              fh.write("\n")
23          fh.write(item + "\n")
24      return "added"
```

**判定表の行**（解析器の出力。本書の試験。ツール `ensure_todo`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D4 | `builtins.open` | `FS_WRITE` | `fs_append` | `server.py:20` |

**解析器がなぜ指摘したか**: D4 の規則は、`open` の mode に `'a'` があれば `fs_append` の矛にします（`authgap/dparse.py:523-532`）。
書く前に内容を確かめているかは見ません。

**問い 1: 届くか**

- 20 行に来るのは、18 行で `item` がまだファイルに無いときです。
- 条件の種類: 「まだ無い `item` を渡したとき」は、`引数` とも `外部の状態` とも読めます。手引き 14.3 は、2 つ以上の種類に読めるときは
  表の上からの順で先のものを 1 つだけ書くと決めています（鍵が引数のキャッシュの「無いとき」は `引数`。D76）。`引数` にします。
- 答え: **はい**（条件つき）。

**問い 2: 宣言に反するか**

- D4 の問いは「同じ引数で 2 回呼んだとき、2 回目が 1 回目の後の状態をさらに変えるか」です（手引き 15.4）。D4 には原理 3 を当てません。
- 1 回目: `item` が無ければ、20〜23 行で 1 行足します（最後の行に改行が無ければ、先に改行を足す）。
- 2 回目（同じ `item`）: 13 行で同じ形にそろえ、17 行で読んだ中身の行に 1 回目の行があるので、18〜19 行で返します。書きません。
- 15.4 の表の「定数の `'a'` で追記する」の行: 「書く前に内容を確かめて、すでにあれば書かないなら反しない（v4 の E00）」。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `引数` |
| condition | `todo.txt にまだ無い item を渡したとき` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E8: server.py:18 で同じ item がすでにあれば :19 で返すので、同じ引数の 2 回目は書かない（冪等な追記。15.4）` |
| unknown_reason | （空） |
| evidence | `server.py:13 item をそろえる → :15-17 todo.txt を読む → :18 item in text.splitlines() なら :19 で返す → そうでなければ :20 open(TODO, "a") → :23 1 行足す` |

**この例で学ぶこと**: D4 は「同じ引数で 2 回」を頭の中で実行して決める。
**確かめずに日付つきの行を毎回足す（[自分で判定してみる 問 4](#ai-2-y)）なら答えが変わり、正**（15.4: 時刻を含むものを書く → 反する）。

---

<a id="ai-2-16"></a>
### I-2.16 `flock` のために `'a'` で開くだけ（宣言 D4 / 判定: 誤 E8 / 開くモードと書く文を分けて見る）

**コード**（作った例）

```
 1  import fcntl
 2  import json
 3  import os
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("ledger")
 9  STATE = os.path.expanduser("~/.ledger/state.json")
10  LOCKFILE = os.path.expanduser("~/.ledger/state.lock")
11
12
13  @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
14  def get_balance(account: str) -> str:
15      """Return the balance of an account."""
16      with open(LOCKFILE, "a") as lock:
17          fcntl.flock(lock, fcntl.LOCK_SH)
18          try:
19              with open(STATE) as fh:
20                  state = json.load(fh)
21          finally:
22              fcntl.flock(lock, fcntl.LOCK_UN)
23      return str(state.get(account, 0))
```

**判定表の行**（解析器の出力。本書の試験。ツール `get_balance`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D4 | `builtins.open` | `FS_WRITE` | `fs_append` | `server.py:16` |

**解析器がなぜ指摘したか**: [I-2.15](#ai-2-15) と同じです。mode の `'a'` だけを見ます（`authgap/dparse.py:523-532`）。開いた後に書くかは見ません。

**問い 1: 届くか** — 16 行は本体の中で、条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- 16 行は `LOCKFILE` を `'a'` で開き、17 行と 22 行で `flock` の鍵をかけ外しするだけです。`lock` に `write` する文はありません。
- 1 回目は、`state.lock` が無ければ空のファイルができます。2 回目は、同じファイルを開くだけで、中身も増えません。
- 15.4 の表の「`flock` のために `'a'` で開くだけで書かない → 反しない（O41）」の行です。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E8: server.py:16 の 'a' は flock のために開くだけで、lock には何も書かない（15.4、O41）` |
| unknown_reason | （空） |
| evidence | `server.py:16 open(LOCKFILE, "a") as lock → :17 flock(LOCK_SH) → :19-20 state.json を読む → :22 flock(LOCK_UN)。lock への write は無い` |

**この例で学ぶこと**: `'a'` は「追記するかもしれない」の印にすぎない。書く文があるかを読む。
**同じロックファイルに `lock.write(f"{time.time()} read {account}\n")` と書き足していたら答えが変わり、正**（2 回目でさらに行が増える。ラベルはログ）。
同じ形でも宣言が D1 なら、ロックファイルの作成も環境の変更なので考え方が違う（15.1）。

---

<a id="ai-2-17"></a>
### I-2.17 ドットの無い名前と `〜.internal` への通信（宣言 D3 / 判定: 誤 E9 / 解析器と手引きの「local」の定義の差）

**コード**（作った例）

```
 1  import httpx
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("llm")
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
10  def ask_local_llm(prompt: str) -> str:
11      """Ask the Ollama model running in the same docker compose."""
12      r = httpx.post("http://ollama:11434/api/generate",
13                     json={"model": "llama3", "prompt": prompt, "stream": False})
14      return r.json()["response"]
15
16
17  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
18  def ask_host_llm(prompt: str) -> str:
19      """Ask the model served on the docker host."""
20      r = httpx.post("http://host.docker.internal:11434/api/generate",
21                     json={"model": "llama3", "prompt": prompt, "stream": False})
22      return r.json()["response"]
23
24
25  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
26  def ask_localhost_llm(prompt: str) -> str:
27      """Ask the model on localhost."""
28      r = httpx.post("http://localhost:11434/api/generate",
29                     json={"model": "llama3", "prompt": prompt, "stream": False})
30      return r.json()["response"]
```

**判定表の行**（解析器の出力。本書の試験）

| ツール | decl | site | kind | reasons | locations |
|---|---|---|---|---|---|
| `ask_local_llm` | D3 | `httpx.post` | `NET` | `net_external_host` | `server.py:12` |
| `ask_host_llm` | D3 | `httpx.post` | `NET` | `net_external_host` | `server.py:20` |
| `ask_localhost_llm` | （行なし） | | | | |

3 つのツールは別の組です。下では `ask_local_llm` の組を判定します。`ask_host_llm` の組も同じ答えです。
`ask_localhost_llm`（`localhost`）には、解析器は D3 の矛も不も出していません。

**解析器がなぜ指摘したか**: 解析器は宛先のホストを、IP の網と、名前 `localhost`・`〜.localhost`・`〜.local` だけで local と読みます。
それ以外の名前はすべて外部です（`authgap/dparse.py:327-352` の `_const_host_class`、とくに `:350-352`）。
`ollama`（ドットの無い名前）も `host.docker.internal` も外部になり、`net_external_host` の矛が出ます（`:502-514` の `_d3`）。

**問い 1: 届くか** — 12 行は本体の中で、条件はありません。答え: **はい**。

**問い 2: 宣言に反するか**

- D3 の問いは「外部の（そのマシンやローカルの網の外の）相手と通信するか」です（手引き 15.3）。
- 宛先のホストは `ollama` です。15.3 の「local の範囲」の表の最後の行「**ドットの無い名前**（`http://ollama:11434` など。docker-compose のサービス名など）→
  local とみなす」に当たります（D73 の 2）。`host.docker.internal` は、同じ表の「`〜.internal` の名前 → local とみなす」の行です（D73 の 2 の追記）。
- 15.3 の結び: 「ドットの無い名前と `〜.internal` の名前は、解析器では外部になる。解析器がそれで D3 の矛を出していたら、判定は**誤**」。
- 答え: **いいえ**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 誤 |
| reachable | はい |
| condition_type | `なし` |
| condition | `なし` |
| violates | いいえ |
| write_target | （空） |
| error_class | `E9: 語彙・定義の差 — 宛先 ollama はドットの無い名前で、手引き 15.3 では local（D73 の 2）。解析器（_const_host_class）は外部とする` |
| unknown_reason | （空） |
| evidence | `server.py:12 httpx.post("http://ollama:11434/api/generate", ...)。ホストは ollama（ドットの無い名前。docker compose のサービス名）` |

**記号についての注意（手引きの穴）**: 15.3 は誤の原因を「語彙・定義の差（第 17 節）」と書きますが、17 節の E1〜E9 の表に、この類はありません。
本書は 17 節の結び「分類に迷ったら E9 にして説明を書く」に従い、E9 にして説明の先頭に「語彙・定義の差」と書きました。
ただし、この記号の穴は穴の仕分け（`docs/drafts/guide_holes_triage.md`）で「まれ」の H-4-24 とされ、「出会ったら手引き 22 節」とされています。
22 節を当てると、この組は「不明（手引きで決まらない: …）」になる読み方もあります。**どちらで記録するかは、封の前に学生が確かめてください**
（[付録 H-5](appendix-h-5.md) の【穴 H-5-12】）。誤であること（宣言に反しないこと）自体は、15.3 が決めています。

**この例で学ぶこと**: D3 は、宛先のホストを手引き 15.3 の「local の範囲」の表に当てて決め、解析器の local の定義に合わせない（手引き 11.3）。
**宛先が `api.openai.com` のような公開のホストなら答えが変わり、正**（定数の外部ホスト）。
`localhost` と `127.0.0.1` は解析器も local と読むので、そもそも矛が出ません（`ask_localhost_llm`）。

---

<a id="ai-2-x"></a>
### I-2.x この分冊の例の一覧

| 番号 | 題 | 宣言 | 判定 | 学ぶ点 |
|---|---|---|---|---|
| [I-2.1](#ai-2-1) | lifespan で済ませる初期化 | D1 | 誤 E1 | 一度だけの初期化は、先に済ませる場所（lifespan）を探す |
| [I-2.2](#ai-2-2) | 読み込み時に済ませる初期化 | D1 | 誤 E1 | モジュールの一番上の文は import で必ず走る |
| [I-2.3](#ai-2-3) | 対比: `main()` の中だけの初期化 | D1 | 正 | `main()` を通らない起動で届く。条件の種類は `起動の方法` |
| [I-2.4](#ai-2-4) | 同じ呼び出しで作って消す一時ファイル | D2 | 誤 E2 | D2 は呼び出しの前からあったものを問う（D1 なら正） |
| [I-2.5](#ai-2-5) | ロックと、途中で止まった前の呼び出しの残り物 | D2 | 誤 E2 | 異常時の残り物は、ふつうの流れで決める（D76） |
| [I-2.6](#ai-2-6) | 組み込みの `set()` と `CacheManager.set` | D1 | 誤 E3 | 道筋の段は受け手で確かめる |
| [I-2.7](#ai-2-7) | E4 について（作れなかった類） | — | — | kind まで違うときだけ E4。名前だけの違いは note |
| [I-2.8](#ai-2-8) | ファイルを変えない子プロセスへのパイプ | D1 | 誤 E5 | 子の動作を全部見る。`wc` は書かない |
| [I-2.9](#ai-2-9) | 定数で閉じた枝 `if DEBUG:` | D1 | 誤 E6 | 運用者が書き換える `config.py` なら `運用者の設定` |
| [I-2.10](#ai-2-10) | 効果の前に必ず例外を投げる | D1 | 誤 E6 | 引数で通れる枝でも、中で必ず抜けるなら届かない |
| [I-2.11](#ai-2-11) | `shlex.quote` した値だけを渡すシェル | D1 | 誤 E7 | モデルが決められるかは自分で確かめる |
| [I-2.12](#ai-2-12) | 読み取りのモードを書き込みと読む | D1 | 誤 E8 | モードの取りうる値を全部読む |
| [I-2.13](#ai-2-13) | 標準エラーへのログ | D1 | 誤 E8 | 行き先で決める。メモリの状態も D1 の違反にしない |
| [I-2.14](#ai-2-14) | 同じ呼び出しで作ったファイルの権限を変える | D2 | 誤 E8 | 後始末でない「反しない」は E2 でなく E8 |
| [I-2.15](#ai-2-15) | 書く前に確かめる追記 | D4 | 誤 E8 | 2 回目を頭の中で実行する |
| [I-2.16](#ai-2-16) | `flock` のために `'a'` で開くだけ | D4 | 誤 E8 | 開くモードと書く文を分けて見る |
| [I-2.17](#ai-2-17) | ドットの無い名前と `〜.internal` | D3 | 誤 E9 | local は手引き 15.3 の表で決める（記号は穴） |

**この分冊に入れなかった形**: D2 の「新しく作るだけ」（`open(…, "x")`・`open(…, "a")`・`mkdir`）は、凍結版の解析器も矛にしません
（`authgap/effects.py:298-318` で追加型と読み、`authgap/dparse.py:404-406` で内にする）。そのため、矛の誤としては出てきません
（[I-2.5](#ai-2-5)・[I-2.14](#ai-2-14) の表の外の行で確かめられます）。E4 は [I-2.7](#ai-2-7) のとおり作れませんでした。

---

<a id="ai-2-y"></a>
### I-2.y 自分で判定してみる

コードと判定表の行だけを出します。記録の欄（`verdict`・`reachable`・`condition_type`・`violates`・`write_target` か `error_class`）を
自分で決めてから、答えを開いてください。どの問も、本文のどれかの例と 1 か所だけ違います。判定表の行は、凍結版で走査した本物の出力です（本書の試験）。

**問 1**（宣言 D1。ツール `count_notes`）

```
 1  import os
 2  import sqlite3
 3  from contextlib import asynccontextmanager
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  DATA_DIR = os.path.expanduser("~/.notes_mcp")
 9  _conn = None
10
11
12  def _get_conn():
13      global _conn
14      if _conn is None:
15          os.makedirs(DATA_DIR, exist_ok=True)
16          _conn = sqlite3.connect(os.path.join(DATA_DIR, "notes.db"))
17      return _conn
18
19
20  @asynccontextmanager
21  async def app_lifespan(server):
22      if os.environ.get("NOTES_PRELOAD") == "1":
23          _get_conn()
24      yield
25
26
27  mcp = FastMCP("notes", lifespan=app_lifespan)
28
29
30  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
31  def count_notes() -> str:
32      """Count notes."""
33      return str(_get_conn().execute("SELECT count(*) FROM notes").fetchone()[0])
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:15` |

<details><summary>答え</summary>

**正**。reachable はい、condition_type `初回`、violates はい、write_target `キャッシュ・状態の保存`。

- [I-2.1](#ai-2-1) と違い、lifespan の初期化は 22 行の条件つきです。手引き 14.4 の見分け方「条件つきなら、条件が偽のときはツールの呼び出しで届くので『到達する』」。
- 既定（`NOTES_PRELOAD` を設定しない）では、最初の呼び出しで 14 行が真になり、15 行に届きます。
  「既定では起きるが、設定で止められる」形なので `運用者の設定` は書きません（14.3 の迷いやすい条件の表）。
  `makedirs(exist_ok=True)` で環境が変わるのは初回だけなので `初回`（同じ表の 1 行目）。(B) に数え、(C) には数えません。
- 15.1: ディレクトリの作成も反する。16.2「初回だけ `~/.app/` を作る → キャッシュ・状態の保存」。
- evidence: `server.py:33 count_notes → _get_conn() → :14 if _conn is None（NOTES_PRELOAD が 1 でない起動では最初の呼び出しで真）→ :15 os.makedirs(DATA_DIR)。lifespan の :23 は :22 の条件つき`

</details>

**問 2**（宣言 D1。ツール `preview_settings`）

```
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("profile")
 8  STORE = os.path.expanduser("~/.profile_mcp/settings.json")
 9
10
11  class SettingsStore:
12      def update(self, values):
13          os.makedirs(os.path.dirname(STORE), exist_ok=True)
14          with open(STORE, "w") as fh:
15              json.dump(values, fh)
16
17
18  DEFAULTS = {"theme": "light", "lang": "en"}
19
20
21  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
22  def preview_settings(theme: str) -> str:
23      """Show what the settings would look like with another theme."""
24      merged = dict(DEFAULTS)
25      merged.update({"theme": theme})
26      return json.dumps(merged)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:14` |

（道筋は `SettingsStore.update`、入口の呼び出し行は 25。13 行の `os.makedirs` にも同じ組が出ています。）

<details><summary>答え</summary>

**誤 E3**。reachable いいえ（violates・condition は空欄）。

- 25 行の `merged` は 24 行の `dict(DEFAULTS)` で、組み込みの `dict` です。`merged.update` は `dict.update` で、メモリの中の辞書を変えるだけです。
- `SettingsStore` の実体を作る文は木の中にありません（grep `SettingsStore`）。解析器は末尾の名前 `update` で木の中の唯一の候補に降りました
  （`authgap/val/engine.py:988`。受け手の型で裏付けられない解決なので確度は opaque になりますが、矛は残ります）。
- error_class: `E3: server.py:25 の merged は組み込みの dict（:24）で、merged.update は dict.update。木の中の SettingsStore.update（:12）は呼ばれない`
- [I-2.6](#ai-2-6) と同じ類です。辞書を変えることは、プロセスのメモリの中の状態でもあり、D1 の違反にしません（15.1、D76 の 2）。

</details>

**問 3**（宣言 D1。ツール `lint_snippet`）

```
 1  import os
 2  import subprocess
 3  import tempfile
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("lint")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def lint_snippet(code: str) -> str:
13      """Lint a Python snippet and return the report."""
14      fd, tmp = tempfile.mkstemp(suffix=".py")
15      try:
16          with os.fdopen(fd, "w") as fh:
17              fh.write(code)
18          out = subprocess.run(["pyflakes", tmp], capture_output=True, text=True)
19          return out.stdout or "no problems"
20      finally:
21          os.remove(tmp)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.remove` | `FS_WRITE` | `fs_write` | `server.py:21` |

<details><summary>答え</summary>

**正**。reachable はい、condition_type `なし`、violates はい、write_target `一時ファイル`。

- [I-2.4](#ai-2-4) と同じコードで、宣言だけが D1 です。
- 15.1 の表の FS_WRITE の行: 「ログ・キャッシュ・一時ファイル・ディレクトリの作成も含む（同じ呼び出しの中で作って消す一時ファイルは、
  原理の文書 §7.1 の『FS_WRITE（すべて。新規作成を含む）→ 矛（決定済み）』による）」。E2 は D2 だけの類です（手引き 17）。
- 16.1 の順 5「同じ呼び出しの中で作って消す、または OS の一時領域に作る → 一時ファイル」。
- evidence: `server.py:14 mkstemp で一時ファイルを作る → :21 finally で os.remove(tmp)。毎回届く`

</details>

**問 4**（宣言 D4。ツール `add_todo`）

```
 1  import os
 2  import time
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("todo")
 8  TODO = os.path.expanduser("~/todo.txt")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
12  def add_todo(item: str) -> str:
13      """Add an item to the todo list."""
14      with open(TODO, "a") as fh:
15          fh.write(f"{time.strftime('%Y-%m-%d')} {item}\n")
16      return "added"
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D4 | `builtins.open` | `FS_WRITE` | `fs_append` | `server.py:14` |

<details><summary>答え</summary>

**正**。reachable はい、condition_type `なし`、violates はい、write_target `利用者のファイル`。

- [I-2.15](#ai-2-15) と違い、書く前に確かめません。同じ `item` で 2 回呼ぶと、15 行の行が 2 つになります。
  15.4 の表の「定数の `'a'` で追記する → 繰り返すと追記が重なるなら反する」と「時刻…を含むものを書く → 反する」の行。
- todo の一覧は利用者のデータとして扱われるファイルなので、16.1 の順 3 の `利用者のファイル`。
- evidence: `server.py:14 open(TODO, "a") → :15 日付と item の 1 行を書く。確かめる文は無く、同じ引数の 2 回目も 1 行増える`

</details>

**問 5**（宣言 D1。ツール `get_weather`。木には `server.py` と `config.py` がある）

```
（config.py）
 1  # 運用者向けの設定。配備する人が必要に応じて書き換える（README の「設定」を参照）。
 2  DEBUG = False
 3  DUMP_DIR = "/tmp/weather_debug"

（server.py）
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  import config
 8
 9  mcp = FastMCP("weather")
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def get_weather(city: str) -> str:
14      """Return the current weather for a city."""
15      data = {"city": city, "temp": 21}
16      if config.DEBUG:
17          os.makedirs(config.DUMP_DIR, exist_ok=True)
18          with open(os.path.join(config.DUMP_DIR, "last.json"), "w") as fh:
19              json.dump(data, fh)
20      return json.dumps(data)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | `FS_WRITE` | `fs_write` | `server.py:17` |
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:18` |

2 行目の組（`builtins.open`）を判定してください。

<details><summary>答え</summary>

**正**。reachable はい、condition_type `運用者の設定`、condition `config.py の DEBUG を True に書き換えて起動したとき`、violates はい、write_target `一時ファイル`。

- [I-2.9](#ai-2-9) と違い、`DEBUG` は「運用者が書き換える」と書かれた `config.py` の定数です。手引き 14.2 の表の但し書き
  「運用者が書き換える前提の `config.py` の定数は、閉じた枝ではなく 14.3 の `運用者の設定`」（D76）。
- `運用者の設定` は運用者が決める条件なので、(B) にも (C) にも数えません（14.3）。
- 16.1 の順 5: OS の一時領域（`/tmp`）に作る → `一時ファイル`。
- evidence: `server.py:16 if config.DEBUG（config.py:1 は運用者が書き換える設定と書く）→ :18 open(/tmp/weather_debug/last.json, "w")`

</details>

**問 6**（宣言 D1。ツール `echo_entry`）

```
 1  import os
 2  import subprocess
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("journal")
 8  JOURNAL = os.path.expanduser("~/journal.txt")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def echo_entry(text: str) -> str:
13      """Echo a journal entry back to the user."""
14      proc = subprocess.Popen(["tee", "-a", JOURNAL], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
15      out, _ = proc.communicate(input=text + "\n")
16      return out
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `pipe:communicate` | `FS_WRITE` | `fs_write` | `server.py:15` |

<details><summary>答え</summary>

**正**。reachable はい、condition_type `なし`、violates はい、write_target `利用者のファイル`。

- [I-2.8](#ai-2-8) と違い、子は `tee -a ~/journal.txt` です。`tee` は標準入力を標準出力に写し、`-a` で指定のファイルに追記します
  （POSIX の `tee` の仕様 <https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tee.html> を開いて確かめる）。
- 15.1: pipe の組では子の動作を全部数える（D76）。子がファイルに追記するので、環境を変えます。
- 日記は利用者の文書として扱われるファイルなので `利用者のファイル`（16.1 の順 3）。
- evidence: `server.py:14 Popen(["tee", "-a", JOURNAL], stdin=PIPE) → :15 communicate(input=text) → 子の tee が ~/journal.txt に追記する`

</details>

**問 7**（宣言 D1。ツール `open_note`）

```
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("files")
 7  ROOT = os.path.expanduser("~/notes")
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
11  def open_note(name: str, mode: str = "r") -> str:
12      """Open a note and return its content."""
13      with open(os.path.join(ROOT, os.path.basename(name)), mode) as fh:
14          return fh.read()
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:13` |

<details><summary>答え</summary>

**正**。reachable はい、condition_type `引数`、condition `引数 mode に "w" などの書き込みのモードを渡したとき`、violates はい、write_target `利用者のファイル`。

- [I-2.12](#ai-2-12) と違い、`mode` はツールの引数で、モデルが決められます。原理 3-a で「取りうる値の全体」を考えます（手引き 手順 F）。
- `mode="w"` なら、13 行の `open` が既存のノートを空にします。14 行の `read()` は失敗しますが、その前にファイルはもう切り詰められています。
- 既定値 `"r"` では書かないので、条件は `引数`（14.3）。(B) に数え、(C) には数えません。
- evidence: `server.py:11 mode はモデルが決める引数 → :13 open(ROOT/<name>, mode)。mode="w" で既存のノートを切り詰める`

</details>

**問 8**（宣言 D2。ツール `count_commits`）

```
 1  import os
 2  import shutil
 3  import subprocess
 4  import tempfile
 5
 6  from mcp.server.fastmcp import FastMCP
 7  from mcp.types import ToolAnnotations
 8
 9  mcp = FastMCP("repo")
10
11
12  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
13  def count_commits(repo_url: str) -> str:
14      """Count the commits of a public git repository."""
15      work = tempfile.mkdtemp(prefix="cc-")
16      try:
17          subprocess.run(["git", "clone", "--bare", "--quiet", "--", repo_url, work], check=True)
18          out = subprocess.run(["git", "-C", work, "rev-list", "--count", "HEAD"],
19                               capture_output=True, text=True)
20          return out.stdout.strip()
21      finally:
22          shutil.rmtree(work, ignore_errors=True)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `shutil.rmtree` | `FS_WRITE` | `fs_remove` | `server.py:22` |

（17・18 行の `subprocess.run` には D2 の不（`spawn_command`）が出ています。不なので、この表では判定しません。）

<details><summary>答え</summary>

**誤 E2**。reachable はい、condition_type `なし`、violates いいえ。

- 22 行が消す `work` は、15 行の `mkdtemp` がこの呼び出しで作った一時ディレクトリです。中身も、この呼び出しの 17 行の clone が作った物です。
- 15.2 の迷いやすい形「同じ呼び出しで自分が作った一時ファイル…を消す → 反しない（誤、E2）」。[I-2.4](#ai-2-4) と同じ類です。
- error_class: `E2: server.py:22 が消すのは、同じ呼び出しの :15 で mkdtemp が作った一時ディレクトリ work`
- 宣言が D1 なら、[問 3](#ai-2-y) と同じく正になります。

</details>

---

[← 前](appendix-i-1.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-3.md)
