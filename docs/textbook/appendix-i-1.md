[← 前](appendix-i.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-2.md)

---

# 付録 I-1 正になる例 — 宣言に反する動作に届く

<a id="ai-1-0"></a>
## この分冊の読み方

この分冊の答えは**本書の答え（本記録者の判定）**です。正解ではありません。最終評価の判定は、学生が手引きで行います。

この分冊には、**最後に「宣言に反する動作に届く」と分かる例**を 18 個集めました。多くは解析器が矛（宣言に反する）を出し、人が読んでも正になる例です。ただし、次の 2 つの形も入れました。どちらも「解析器の答え」と「人の読み」が違う、学ぶ価値の高い例です。

- **解析器は不（決められない）を出したが、人が読むと反する**（[I-1.10](#ai-1-10)・[I-1.11](#ai-1-11)。ほかに [I-1.14](#ai-1-14) の D4 の組）。この判定は矛の判定表ではなく、**不の中身の判定表**（手引き 18A）に載ります。結果の欄は `正` ではなく `違反` です。
- **解析器は矛も不も出さないが、人が読むと反する**（[I-1.9](#ai-1-9)・[I-1.15](#ai-1-15)）。この判定は**見落としの判定表**（手引き 18）に載ります。結果の欄は `見落とし` です。

規則の正本は、判定の手引きの下書き `docs/drafts/final_judging_guide_draft.md` の今の版（D76 を書き写した版）です。「手引き 15.2」のように節で引きます。[付録 H](appendix-h.md) は D76 の前の版を引用しているので、食い違えば手引きの今の文に従います。

**例の作り方と本書の試験**: 例はすべて、この付録のために書いた小さな FastMCP のサーバです（作った例。repo には入っていません）。1 例を 1 つの木（`server.py` が 1 つ）にして、凍結版の解析器（タグ `analyzer-freeze-3`。走らせる前に `git diff analyzer-freeze-3 -- authgap/` が空であることを確かめた）で走らせました。走らせ方は `scripts/scan_v2.py` と同じ `authgap.runner.run(RunConfig(src_root=<木>, population="mcp_server", full=True))` です。**判定表の行は、その出力から写しました。**「〜なら答えが変わる」に書いた解析器の出力も、書き換えた木を同じように走らせて確かめたものです。

**判定表の行の読み方**: 手引き 13 の手順 A の欄のうち、`decl`（照らす宣言）・`site`（効果を起こす関数）・`kind`（効果の種類）・`reasons`（理由のコード。手引き 13.1）・`locations`（その組の効果の位置）を出します。不の組は `reasons` を「不: `net_post`」のように書きます。その下の「解析器の言い分」は手順 B の道具（`scripts/show_target.py`）で見える、道筋（`witness_chain`）・入口の呼び出し行（`entry_lineno`）・slot の主体です。

**記録の欄**: 手引き 13 の手順 H のとおりに書きます。手順 H の既定（D76）により、11.2 の表の「—」に当たる欄と、当てはまらない欄（正のときの `error_class`・`unknown_reason` など）は空欄にします。表では空欄を「（空）」と書きます。`minutes`・`ai_used` などの欄は、例では省きます。

---

<a id="ai-1-1"></a>
### I-1.1 2 段奥のヘルパーでキャッシュを書く（宣言 D1 / 判定: 正 / 学ぶ点: 道筋のたどり方と「鍵が引数のキャッシュ」の条件）

**コード**（作った例）

```python
 1  import json
 2  import os
 3
 4  import requests
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("geo")
 9  CACHE_DIR = os.path.expanduser("~/.geo_cache")
10  API = "https://geocode.example.com/v1/search"
11
12
13  def _save_cache(path, data):
14      os.makedirs(CACHE_DIR, exist_ok=True)
15      with open(path, "w") as fh:
16          json.dump(data, fh)
17
18
19  def _lookup(place):
20      path = os.path.join(CACHE_DIR, place.lower() + ".json")
21      if os.path.exists(path):
22          with open(path) as fh:
23              return json.load(fh)
24      data = requests.get(API, params={"q": place}, timeout=10).json()
25      _save_cache(path, data)
26      return data
27
28
29  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
30  def geocode(place: str) -> str:
31      """Return latitude and longitude for a place name."""
32      d = _lookup(place)
33      return f"{d['lat']},{d['lon']}"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:15` |

解析器の言い分（手順 B）: 道筋 `_lookup -> _save_cache`、入口の呼び出し行 32、slot `path` の主体は MODEL。同じツールには、別の組 `os.makedirs` × `FS_WRITE` × D1（`server.py:14`、`fs_write`）もあります。

**問い 1: 届くか** — 32 行で `geocode` が `_lookup(place)` を呼びます。`_lookup` は 21 行で、その地名のキャッシュファイルがあれば 23 行で返します。無ければ 24 行で API に問い合わせ、25 行で `_save_cache(path, data)` を呼びます。`_save_cache` の 15 行が `open(path, "w")` です。途中の条件は 21 行の「その地名のキャッシュが無いとき」だけです。地名はモデルが決める引数です。答え: **はい**。条件の種類は、手引き 14.3 の「迷いやすい条件の書き方」の下の文により `引数` です。「鍵が引数のキャッシュの『無いとき』は `引数` か `初回` か」と 2 つに読めるときは、表の上の順で先の `引数` を 1 つだけ書きます。

**問い 2: 宣言に反するか** — 手引き 15.1 の表の 1 行目「ファイルの書き込み・作成・削除…（`FS_WRITE` すべて）→ 反する。ログ・キャッシュ…も含む」に当たります。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | 引数 |
| `condition` | 引数 place の地名のキャッシュファイル（`~/.geo_cache/<place>.json`）がまだ無いとき |
| `violates` | はい |
| `write_target` | キャッシュ・状態の保存 |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:32`（geocode が `_lookup(place)` を呼ぶ）→ `server.py:21-25`（キャッシュが無ければ 25 行で `_save_cache(path, data)`）→ `server.py:15` `open(path, "w")`。path は `~/.geo_cache/<place>.json` で、place はモデルが決める引数 |

**この例で学ぶこと**: 道筋は `witness_chain` を地図にして、自分で 1 段ずつ開きます（手順 D）。種類が「キャッシュ・状態の保存」になるのは、判定しているツール自身が 22 行で**読み返す**からです（手引き 16.1 の順 6 と、その下の「読み返す」の主語）。**読み返しが無ければ、名前がキャッシュでも「その他・不明」になります**（手引き 20.1 の組 1）。別の組の `os.makedirs`（14 行。`exist_ok=True`）は、ディレクトリが無い最初のときだけ環境が変わるので、条件は `初回` です（手引き 14.3 の「迷いやすい条件の書き方」の 1 行目）。

---

<a id="ai-1-2"></a>
### I-1.2 SQLite の `INSERT` と `PRAGMA journal_mode=WAL` が 1 組に並ぶ（宣言 D1 / 判定: 正 / 学ぶ点: 位置が 2 つの組と手順 G）

**コード**（作った例）

```python
 1  import sqlite3
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("docs")
 7  DB = "docs.db"
 8
 9
10  def _connect():
11      conn = sqlite3.connect(DB)
12      conn.execute("PRAGMA journal_mode=WAL")
13      conn.execute("PRAGMA foreign_keys=ON")
14      return conn
15
16
17  def _remember(conn, query, n):
18      conn.execute(
19          "INSERT INTO search_history (query, hits) VALUES (?, ?)", (query, n)
20      )
21      conn.commit()
22
23
24  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
25  def search_docs(query: str) -> str:
26      """Search the document index."""
27      conn = _connect()
28      rows = conn.execute(
29          "SELECT title FROM docs WHERE title LIKE ?", (f"%{query}%",)
30      ).fetchall()
31      _remember(conn, query, len(rows))
32      return "\n".join(r[0] for r in rows)
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | `DB` | `db_modify`、`db_persistent` | `server.py:12`、`server.py:18` |

解析器の言い分（手順 B）: 12 行の効果は道筋 `_connect`・入口 27・SQL の先頭語 `PRAGMA`。18 行の効果は道筋 `_remember`・入口 31・先頭語 `INSERT`。13 行の `PRAGMA foreign_keys=ON` も効果として拾っていますが、`locations` には入っていません。

**問い 1: 届くか** — 手順 C: site は psycopg と表示されますが、コードは sqlite3 の接続です。動作の種類（`DB`）は合っているので、判定には影響しません（`note` に書く）。位置は 2 つです。

- 12 行: 27 行 `_connect()` → 12 行。毎回実行されます。ただし `journal_mode=WAL` は DB のファイルに残る設定なので、環境が変わるのは、まだ WAL になっていない最初のときだけです。手引き 14.3 の「迷いやすい条件の書き方」の 1 行目により `初回` です。
- 18 行: 31 行 `_remember(conn, query, len(rows))` → 18 行。毎回、行が 1 つ増えます。`search_history` の表が無ければ失敗しますが、これは「前提の崩れ」で条件に数えません（同じ表の 2 行目）。条件は `なし` です。

答え: **はい**。

**問い 2: 宣言に反するか** — 18 行は手引き 15.1 の「DB のデータ・スキーマの変更（`INSERT` …）→ 反する」、12 行は「DB に残る設定・保守（`PRAGMA journal_mode=WAL` …）→ 反する」に当たります。13 行の `foreign_keys=ON` は「接続単位の設定 → 反しない」なので、`locations` に無いのは正しい扱いです。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | データベース |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:31`（search_docs が `_remember` を呼ぶ）→ `server.py:18-20` `INSERT INTO search_history`。毎回届く |
| `note` | 位置 `server.py:12`（27 → 12、`PRAGMA journal_mode=WAL`）も正。条件は 初回。site は psycopg と表示されるが sqlite3 の接続で、kind DB は合う |

**この例で学ぶこと**: 1 組に位置が複数あれば、1 つでも「届き、かつ反する」位置があれば正です（手順 G）。条件の種類は、**正にできる位置のうち一番弱いもの**（ここでは 18 行の `なし`）を書きます。12 行を先に読んで正と分かった時点で止めてもかまいません（D76）。**そのときの条件は `初回` になり、(B)(C) は報告で下限と書きます。** 書き込み先の種類は「最初に正と分かった位置」の種類ですが、ここではどちらもデータベースです（16.1 の順 2）。`sqlite3.connect` が無い `docs.db` を作る点は、解析器が組にしない別の動作です。この組の判定には入れず、気づいたら `note` に書きます（手順 H の既定）。

---

<a id="ai-1-3"></a>
### I-1.3 `main()` の中だけで済ませる DB の初期化（宣言 D1 / 判定: 正 / 学ぶ点: 起動時の初期化と `起動の方法`）

**コード**（作った例）

```python
 1  import sqlite3
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("recipes")
 7  _conn = None
 8
 9
10  def _db():
11      global _conn
12      if _conn is None:
13          _conn = sqlite3.connect("recipes.db", check_same_thread=False)
14          _conn.execute(
15              "CREATE TABLE IF NOT EXISTS recipes (name TEXT PRIMARY KEY, body TEXT)"
16          )
17      return _conn
18
19
20  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
21  def get_recipe(name: str) -> str:
22      """Return a recipe by name."""
23      row = _db().execute("SELECT body FROM recipes WHERE name = ?", (name,)).fetchone()
24      return row[0] if row else "not found"
25
26
27  def main():
28      _db()
29      mcp.run()
30
31
32  if __name__ == "__main__":
33      main()
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | `DB` | `db_modify` | `server.py:14` |

解析器の言い分（手順 B）: 道筋 `_db`、入口の呼び出し行 23、SQL の先頭語 `CREATE`。

**問い 1: 届くか** — 23 行で `get_recipe` が `_db()` を呼びます。12 行の「一度だけ」の守り（`if _conn is None:`）の中の 14 行が `CREATE TABLE IF NOT EXISTS` です。手順 D の 4 により、この初期化がツールの受付より前に**必ず**済んでいるかを見ます。

- 先に済ませているのは 28 行の `main()` の中だけです。`FastMCP(...)` に `lifespan=` はありません（6 行）。
- `_conn` を `None` に戻す箇所は、モジュールの一番上の 7 行だけです（grep で確かめる）。

手引き 14.4 の表の 1 行目「`main()` の中だけ → 到達する」に当たります。6 行の `mcp` はモジュールの一番上にあるので、`fastmcp run server.py:mcp` のように `main()` を通らずに起動できます。そのときは最初の `get_recipe` で 14 行に届きます。答え: **はい**。条件の種類は `起動の方法` です。`CREATE TABLE IF NOT EXISTS` は表が無いときだけ環境を変えますが、手引き 14.3 の最後の段落により、`起動の方法` の位置の効果が最初の呼び出しでだけ起きるときは `初回` を重ねず、`起動の方法` だけを書きます。

**問い 2: 宣言に反するか** — 手引き 15.1 の「DB のデータ・スキーマの変更（…`CREATE`…）→ 反する」。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | 起動の方法 |
| `condition` | `main()` を通らない起動（`fastmcp run server.py:mcp` など）で、最初に get_recipe を呼んだとき |
| `violates` | はい |
| `write_target` | データベース |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:23`（get_recipe が `_db()` を呼ぶ）→ `server.py:12`（`_conn` が None のとき）→ `server.py:14-16` `CREATE TABLE IF NOT EXISTS recipes`。先に済ませるのは `main()`（28 行）だけで lifespan は無い。`_conn` を None にするのは 7 行だけ |

**この例で学ぶこと**: `起動の方法` は (A) に数え、(B)(C) には数えません（手引き 14.3 の表）。**同じ `_db()` を lifespan の中で呼んでいれば、どの起動でも受付より前に済むので「到達しない」（誤、E1）になります**（手引き 14.4 の表の 2 行目）。モジュールの一番上で `_conn = _db()` としていても E1 です（同じ表の 3 行目）。13 行の `sqlite3.connect` がファイルを作る点は、I-1.2 と同じく `note` に書きます。

---

<a id="ai-1-4"></a>
### I-1.4 読むついでに相手のサーバへ `PUT` する（宣言 D1 / 判定: 正 / 学ぶ点: 相手側の状態を変える HTTP）

**コード**（作った例）

```python
 1  import os
 2  import time
 3
 4  import requests
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("desk")
 9  API = "https://desk.example.com/api"
10  TOKEN = os.environ.get("DESK_TOKEN", "")
11
12
13  def _headers():
14      return {"Authorization": f"Bearer {TOKEN}"}
15
16
17  def _touch(ticket_id):
18      requests.put(
19          f"{API}/tickets/{ticket_id}/last_viewed",
20          json={"viewer": "mcp-bot", "at": int(time.time())},
21          headers=_headers(),
22          timeout=10,
23      )
24
25
26  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
27  def get_ticket(ticket_id: int) -> dict:
28      """Show a support ticket."""
29      resp = requests.get(f"{API}/tickets/{ticket_id}", headers=_headers(), timeout=10)
30      _touch(ticket_id)
31      return resp.json()
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.put` | `NET` | `net_modify` | `server.py:18` |

解析器の言い分（手順 B）: 道筋 `_touch`、入口の呼び出し行 30。29 行の `requests.get` は D1 の行になりません。

**問い 1: 届くか** — 30 行で `get_ticket` が `_touch(ticket_id)` を呼び、18 行で `requests.put` を送ります。前に `if` はありません。送る中身に時刻（20 行の `"at"`）があるので、相手の状態は毎回変わります。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 手引き 15.1 の「HTTP の `PUT` / `PATCH` / `DELETE` → 反する（原理 1-ii-b）」。「最後に見た人を記録するだけ」でも、相手のサーバの状態を変えることに変わりはありません。軽重は種類のラベルで表し、判定には持ち込みません（手引き 11.3）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | 相手側の状態 |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:30`（get_ticket が `_touch(ticket_id)` を呼ぶ）→ `server.py:18-23` `requests.put(f"{API}/tickets/{ticket_id}/last_viewed", json={…, "at": 時刻})`。API は `https://desk.example.com/api`（9 行） |

**この例で学ぶこと**: HTTP は**メソッドで表の行が決まります**。29 行の `GET` は反しません（15.1 の `GET` の行）。**18 行が `requests.post` なら、解析器は不（`net_post`）を出し、人は相手の API の意味を調べて決めます**（[I-1.10](#ai-1-10)）。種類は 16.1 の順 1「相手側の状態」で、DB やファイルより先に当てはめます。

---

<a id="ai-1-5"></a>
### I-1.5 モデルが決めたコマンドを起動する（宣言 D1・D3 / 判定: 正（2 組） / 学ぶ点: 1 つの効果に宣言ごとの組）

**コード**（作った例）

```python
 1  import subprocess
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("diag")
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
10  def run_diagnostic(command: str) -> str:
11      """Run a diagnostic command (e.g. 'df -h') and return its output."""
12      proc = subprocess.run(
13          command, shell=True, capture_output=True, text=True, timeout=30
14      )
15      return proc.stdout + proc.stderr
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_model` | `server.py:12` |
| D3 | `subprocess.run` | `SPAWN` | `spawn_model` | `server.py:12` |

解析器の言い分（手順 B）: 本体の中（道筋なし）。slot `shell_string` の主体は MODEL。

**問い 1: 届くか** — 12 行は本体の中で、前に条件はありません。答え: **はい**（2 組とも）。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 組は宣言ごとに別なので、2 回答えます。

- D1: 手引き 15.1 の「プロセスの起動（`SPAWN`）→ 起動するコマンドをモデルが決められるなら反する」。`command` はモデルが決める引数で、`shell=True` で丸ごとシェルに渡ります。原理 3-a で「取りうる値の全体」を考えるので、`rm` も書き込みも起動できます。答え: **はい**。
- D3: 手引き 15.3 の「実行するコード・起動するコマンドをモデルが決められる → 反する」。`curl` で外部と通信できます。答え: **はい**。

**判定と記録**

| 欄 | D1 の組 | D3 の組 |
|---|---|---|
| `verdict` | 正 | 正 |
| `reachable` | はい | はい |
| `condition_type` | なし | なし |
| `condition` | なし | なし |
| `violates` | はい | はい |
| `write_target` | プロセスの起動・コードの実行 | モデルが決めるコード・コマンド |
| `error_class`・`unknown_reason` | （空） | （空） |
| `evidence` | `server.py:12-14` `subprocess.run(command, shell=True, …)`。command はモデルが決める引数で、本体で毎回届く | 同じ |

**この例で学ぶこと**: D3 の正には書き込み先の種類ではなく、**通信先の種類**（手引き 16.3）を書きます。D1 の SPAWN の正は、子が何を変えるか分かっても常に「プロセスの起動・コードの実行」です（16.2）。**コマンドが定数（`subprocess.run(["df", "-h"])`）なら、解析器は D1・D3 とも不（`spawn_command`）を出します**（本書で試した）。D1 の不は（抜き取りで選ばれれば）不の中身の判定表に載り、人は `df` が何をするかを調べて「違反でない」と決めます（15.1 の SPAWN の行）。D3 の不は判定しません（18A.1）。

---

<a id="ai-1-6"></a>
### I-1.6 引数で指定されたときだけレポートを書き出す（宣言 D1 / 判定: 正 / 学ぶ点: `引数` の条件と既定値）

**コード**（作った例）

```python
 1  import os
 2  import sqlite3
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("sales")
 8
 9
10  def _render(rows):
11      return "\n".join(f"- {r[0]}: {r[1]}" for r in rows)
12
13
14  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
15  def sales_report(month: str, out_dir: str = "") -> str:
16      """Summarise sales for a month. If out_dir is given, also save report.md there."""
17      conn = sqlite3.connect("sales.db")
18      rows = conn.execute(
19          "SELECT item, SUM(qty) FROM sales WHERE month = ? GROUP BY item", (month,)
20      ).fetchall()
21      text = _render(rows)
22      if out_dir:
23          os.makedirs(out_dir, exist_ok=True)
24          with open(os.path.join(out_dir, "report.md"), "w") as fh:
25              fh.write(text)
26      return text
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:24` |

解析器の言い分（手順 B）: 本体の中。slot `path` の主体は MODEL。別の組 `os.makedirs` × D1（`server.py:23`）もあります。

**問い 1: 届くか** — 22 行 `if out_dir:` の中の 24 行です。`out_dir` の既定値は空文字で、偽です。モデルが空でない値を渡したときだけ届きます。モデルが選べる引数なので、到達します（手引き 14.3 の表の `引数` の行。例「`if output_file:`」と同じ形）。答え: **はい**。条件の種類は `引数`。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | 引数 |
| `condition` | 引数 out_dir に空でない値を渡したとき |
| `violates` | はい |
| `write_target` | 利用者のファイル |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:22`（`if out_dir:`）→ `server.py:24` `open(os.path.join(out_dir, "report.md"), "w")`。out_dir はモデルが決める引数 |

**この例で学ぶこと**: 書き先をモデルが指定するので、種類は 16.1 の順 3「利用者のファイル」です（16.2 の「モデルが決めたパスへのエクスポート」）。**既定値が `out_dir: str = "reports"` のように真なら、引数を渡さなくても書くので条件は `なし` になります**（手引き 14.3 の「迷いやすい条件の書き方」の 3 行目）。`os.makedirs` の組は別の組として、同じ手順で判定します。

---

<a id="ai-1-7"></a>
### I-1.7 一時ディレクトリを作って `shutil.rmtree` で消す（宣言 D1 / 判定: 正 / 学ぶ点: 同じ呼び出しで作って消すものも D1 では反する）

**コード**（作った例）

```python
 1  import os
 2  import shutil
 3  import tempfile
 4  import zipfile
 5
 6  import requests
 7  from mcp.server.fastmcp import FastMCP
 8  from mcp.types import ToolAnnotations
 9
10  mcp = FastMCP("archive")
11
12
13  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
14  def list_archive(url: str) -> str:
15      """Download a zip archive and list the files inside it."""
16      workdir = tempfile.mkdtemp(prefix="arch_")
17      try:
18          path = os.path.join(workdir, "a.zip")
19          with open(path, "wb") as fh:
20              fh.write(requests.get(url, timeout=30).content)
21          with zipfile.ZipFile(path) as zf:
22              names = zf.namelist()
23      finally:
24          shutil.rmtree(workdir, ignore_errors=True)
25      return "\n".join(names)
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `shutil.rmtree` | `FS_WRITE` | `fs_write` | `server.py:24` |

解析器の言い分（手順 B）: 本体の中。slot `path` の主体は OP、確度は opaque。別の組 `builtins.open` × D1（`server.py:19`、`'wb'` での書き込み）もあります。

**問い 1: 届くか** — 24 行は `finally` の中です。ダウンロードや展開が失敗しても、毎回走ります。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行です。注意の欄に「一時ファイル…も含む（同じ呼び出しの中で作って消す一時ファイルは、原理の文書 §7.1 の『FS_WRITE（すべて。新規作成を含む）→ 矛（決定済み）』による）」とあります。手引き 14.5 も「到達はする。宣言に反するかは宣言による」としています。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | 一時ファイル |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:16`（`tempfile.mkdtemp` で作業ディレクトリを作る）→ `server.py:23-24` `finally:` で `shutil.rmtree(workdir)`。毎回届く |

**この例で学ぶこと**: 種類は 16.1 の順 5「一時ファイル」（同じ呼び出しの中で作って消す、OS の一時領域に作る）です。**同じコードを D2（`destructiveHint: false`）で判定すると、呼び出しの前からあったものではないので反しません**（誤、E2。手引き 15.2 の迷いやすい形の 1 つ目）。D1 と D2 で答えが逆になる代表の形です。16 行の `mkdtemp` もディレクトリを作りますが、解析器はこれを効果に挙げていません。この組の判定には関係しないので、気づいたら `note` に書きます。

---

<a id="ai-1-8"></a>
### I-1.8 環境変数を設定したときだけ監査ログを書く（宣言 D1 / 判定: 正 / 学ぶ点: `運用者の設定` と (B)）

**コード**（作った例）

```python
 1  import datetime
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("hr")
 8  AUDIT_PATH = os.environ.get("HR_AUDIT_FILE")
 9  EMPLOYEES = {"e001": "Sato", "e002": "Suzuki"}
10
11
12  def _audit(action, target):
13      if not AUDIT_PATH:
14          return
15      stamp = datetime.datetime.now().isoformat()
16      with open(AUDIT_PATH, "a") as fh:
17          fh.write(f"{stamp} {action} {target}\n")
18
19
20  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
21  def lookup_employee(employee_id: str) -> str:
22      """Look up an employee name by id."""
23      _audit("lookup", employee_id)
24      return EMPLOYEES.get(employee_id, "unknown")
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:16` |

解析器の言い分（手順 B）: 道筋 `_audit`、入口の呼び出し行 23。slot `path` の主体は OP。

**問い 1: 届くか** — 23 行で `_audit` を呼びます。13 行で `AUDIT_PATH` が空なら抜けます。`AUDIT_PATH` は環境変数 `HR_AUDIT_FILE` で、既定値がありません（8 行）。運用者がこの環境変数を設定して起動したときだけ、16 行の追記に届きます。答え: **はい**。条件の種類は `運用者の設定`（手引き 14.3 の表）。13 行は「前提の崩れ」ではなく、運用者が機能を有効にするかどうかの分かれ目です。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。手引き 11.3 の例「読み取り専用のツールがログファイルに 1 行追記するのは…違反である」そのものです。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | 運用者の設定 |
| `condition` | 環境変数 HR_AUDIT_FILE を設定して起動したとき |
| `violates` | はい |
| `write_target` | ログ |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:23`（lookup_employee が `_audit` を呼ぶ）→ `server.py:13`（AUDIT_PATH が空なら抜ける。AUDIT_PATH は 8 行の環境変数 HR_AUDIT_FILE）→ `server.py:16-17` `open(AUDIT_PATH, "a")` で「時刻 操作 対象」の 1 行を追記 |

**この例で学ぶこと**: `運用者の設定` の正は (A) に数え、(B) には数えません。書く場所を運用者が決めても、それだけで「利用者のファイル」にはしません。中身で決めます（16.2）。「いつ・何をした」の行なので「ログ」です。**8 行が `os.environ.get("HR_AUDIT_FILE", "hr_audit.log")` のように既定値を持つなら、運用者が何もしなくても書くので条件は `なし` です**（本書で試した。解析器の出力は同じ矛 `server.py:16`）。

---

<a id="ai-1-9"></a>
### I-1.9 `logging` の出力先がファイル（宣言 D1 / 結果: 見落とし / 学ぶ点: 解析器は何も出さないが、人が読めば反する）

**この例は見落としの判定表に載る形です**（手引き 18）。対象は「D1 か D2 を明示していて、その宣言への矛が 1 件も出ていないツール」（18.1）で、抜き取りで選ばれれば判定します。

**コード**（作った例）

```python
 1  import json
 2  import logging
 3  import os
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  LOG_FILE = os.environ.get("NOTES_LOG", "notes_server.log")
 9  logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
10  log = logging.getLogger("notes")
11
12  mcp = FastMCP("notes")
13  NOTES_FILE = os.path.expanduser("~/notes.json")
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def find_notes(keyword: str) -> str:
18      """Find notes that contain a keyword."""
19      log.info("find_notes keyword=%s", keyword)
20      with open(NOTES_FILE, encoding="utf-8") as fh:
21          notes = json.load(fh)
22      return "\n".join(n["title"] for n in notes if keyword in n["body"])
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| （行なし） | | | | |

解析器は、このツールに D1 の矛も不も出していません。効果として拾ったのは 20 行の読み取り（`FS_READ`）だけです。

**問い 1: 届くか**（手引き 18.2 の 1〜3。解析器の出力を見る前に読む） — 本体は 17〜22 行です。木の中の呼び出し先はありません。19 行の `log.info(...)` は木の外のライブラリ（`logging`）ですが、18.3 の最後の注意により、**モジュール水準の設定**を確かめます。9 行の `logging.basicConfig(filename=LOG_FILE, level=logging.INFO)` で、ルートのロガーにファイルの出力先が付いています。INFO の水準なので、19 行は呼び出しのたびに `LOG_FILE` へ 1 行を追記します。`LOG_FILE` は環境変数 `NOTES_LOG` ですが、既定値 `notes_server.log` があるので、運用者が何もしなくても書きます。答え: **はい**。条件の種類は `なし`。深さは 0（本体）。

**問い 2: 宣言に反するか** — 手引き 15.1 の迷いやすい形の 1 つ目「`logging` の出力先がファイルなら反する。出力先の設定を確かめる」。答え: **はい**。

**判定と記録**（見落としの判定表の欄。手引き 18.4）

| 欄 | 値 |
|---|---|
| `outcome` | 見落とし |
| `cause` | 語彙 |
| `write_target` | ログ |
| `condition_type` | なし |
| `condition` | なし |
| `depth` | 0 |
| `unknown_reason` | （空） |
| `output_found` | （空） |
| `evidence` | 読んだ範囲は `server.py:1-22`（本体 17-22。木の中の呼び出し先は無い）。`server.py:9` `logging.basicConfig(filename=LOG_FILE, level=logging.INFO)`（モジュールの一番上。LOG_FILE は 8 行、既定 `notes_server.log`）→ `server.py:19` `log.info(...)` が毎回 LOG_FILE に 1 行追記する |

**この例で学ぶこと**: 原因の「語彙」は、sink の語彙に無いライブラリの書き込みです（18.2 の 6 の例「loguru の `logger.add` のファイル出力」と同じ類）。`basicConfig` が import のときにファイルを開く分は読み込み時なので届きませんが、19 行の追記は毎回届きます。**9 行が `level=logging.WARNING` なら 19 行の `info` は書かれず、`stream=sys.stderr` なら出力先がファイルではないので、どちらも「反する動作は無い」になります**（[問 8](#ai-1-y) と比べる）。

---

<a id="ai-1-10"></a>
### I-1.10 何も見つからないと課題を作る `POST`（宣言 D1 / 結果: 不の中身で違反 / 学ぶ点: 相手の API の文書を開いて決める）

**この例は不の中身の判定表に載る形です**（手引き 18A。D1・D2 の不の組から抜き取りで選ばれれば判定します）。解析器が出したのは矛ではなく不なので、結果の欄は `違反` / `違反でない` / `不明` のどれかです。

**コード**（作った例）

```python
 1  import os
 2
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("issues")
 8  GH = "https://api.github.com"
 9  REPO = "example-org/handbook"
10  HEADERS = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}"}
11
12
13  def _open_issue(title, body):
14      requests.post(
15          f"{GH}/repos/{REPO}/issues",
16          json={"title": title, "body": body},
17          headers=HEADERS,
18          timeout=10,
19      )
20
21
22  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
23  def search_handbook(query: str) -> str:
24      """Search the handbook issues. Files a 'missing doc' issue when nothing matches."""
25      resp = requests.get(
26          f"{GH}/search/issues",
27          params={"q": f"repo:{REPO} {query}"},
28          headers=HEADERS,
29          timeout=10,
30      )
31      items = resp.json().get("items", [])
32      if not items:
33          _open_issue(f"Missing doc: {query}", "Requested via MCP search.")
34      return "\n".join(i["title"] for i in items)
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | 不: `net_post` | `server.py:14` |

解析器の言い分（手順 B）: 道筋 `_open_issue`、入口の呼び出し行 33。25 行の `requests.get` は D1 の行になりません。

**問い 1: 届くか** — 25〜31 行で検索し、32 行 `if not items:` が真なら 33 行で `_open_issue` を呼び、14 行で `POST` します。条件は「検索の結果が空のとき」です。これは、モデルが渡す `query` でも、相手のリポジトリの中身でも決まります。手引き 14.3 の最後の段落により、2 つの種類（`引数` と `外部の状態`）に読めるときは表の上の順で先の **`引数`** を 1 つだけ書きます。モデルはどこにも当たらない語を渡せるので、届きます。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.1 の `POST` の行「相手のドキュメントや API 名から『作成・更新・削除』なら反する」。18A.2 の 3 の `net_post` の要点のとおり、相手の API の意味を調べます。宛先は `https://api.github.com/repos/{owner}/{repo}/issues` への `POST` です。GitHub の公式の文書「Create an issue」（`https://docs.github.com/en/rest/issues/issues#create-an-issue`。2026-10-05 に開いた）は、この宛先とメソッドを課題の作成の API として載せ、「Any user with pull access to a repository can create an issue.」と書いています。作成なので反します。手引き 19 の「確かめた」の基準（公式の文書を自分で開けた）を満たします。答え: **はい**。

**判定と記録**（不の中身の判定表の欄。手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | 違反 |
| `reachable` | はい |
| `violates` | はい |
| `write_target` | 相手側の状態 |
| `condition_type` | 引数 |
| `condition` | 引数 query で検索した結果が空のとき |
| `unknown_reason` | （空） |
| `evidence` | `server.py:32`（検索結果が空なら）→ `server.py:33` → `server.py:14-19` `requests.post(f"{GH}/repos/{REPO}/issues", json={"title": …})`。調べた資料: GitHub REST の「Create an issue」`https://docs.github.com/en/rest/issues/issues#create-an-issue`（`POST /repos/{owner}/{repo}/issues` は課題を作る） |

**この例で学ぶこと**: 解析器は `POST` を一律に不にします（13.1 の `net_post`）。人は相手の文書で決めます。**同じ `POST` でも、GitHub の GraphQL に `query`（読み取り）を送るだけなら照会なので「違反でない」になり、理由を `note` に 1 文で書きます**（18A.2 の 5）。文書にもコードにも意味が無ければ、`不明`（理由の類は「相手の API」。手引き 19）です。

---

<a id="ai-1-11"></a>
### I-1.11 一覧を読み、1 つ足して同じファイルに書き戻す（宣言 D2 / 結果: 不の中身で違反 / 学ぶ点: 表の行を採る）

**この例は不の中身の判定表に載る形です**（手引き 18A）。

**コード**（作った例）

```python
 1  import json
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("bookmarks")
 8  BOOKMARKS = os.path.expanduser("~/.bookmarks.json")
 9
10
11  def _load():
12      if not os.path.exists(BOOKMARKS):
13          return []
14      with open(BOOKMARKS) as fh:
15          return json.load(fh)
16
17
18  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
19  def add_bookmark(url: str, title: str) -> str:
20      """Add a bookmark. Existing bookmarks are kept."""
21      items = _load()
22      items.append({"url": url, "title": title})
23      with open(BOOKMARKS, "w") as fh:
24          json.dump(items, fh, indent=2)
25      return f"{len(items)} bookmarks"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `builtins.open` | `FS_WRITE` | 不: `fs_writeout` | `server.py:23` |

解析器の言い分（手順 B）: 本体の中。slot `path` の主体は OP（書き先はモデルが決めない）。

**問い 1: 届くか** — 21 行で `~/.bookmarks.json` を読み、22 行で 1 件足し、23 行で同じファイルを `'w'` で開いて全部を書き直します。毎回届き、毎回ファイルを書くので、条件の種類は `なし`。答え: **はい**。

**問い 2: 宣言に反するか** — 18A.2 の 3 の `fs_writeout` の要点のとおり、書き先に呼び出しの前からファイルがありうるかを見ます。前の呼び出しが書いたファイルが毎回あります。手引き 15 の前書きの表の 1 行目「D2: 一覧を読み、1 つ足して同じファイルに `'w'` で書き戻す → 反する（15.2 の書き出しの行）」にそのまま当たります。docstring は「既存のブックマークは残す」と言い、データの単位では足すだけに見えます。それでも、**表の行と問いの文が違う答えを指すときは表の行を採ります**（15 の前書き、D76）。答え: **はい**。

**判定と記録**（不の中身の判定表の欄）

| 欄 | 値 |
|---|---|
| `outcome` | 違反 |
| `reachable` | はい |
| `violates` | はい |
| `write_target` | 利用者のファイル |
| `condition_type` | なし |
| `condition` | なし |
| `unknown_reason` | （空） |
| `evidence` | `server.py:21`（`_load` で `~/.bookmarks.json` を読む。14 行）→ `server.py:23-24` `open(BOOKMARKS, "w")` で同じファイルを全部書き直す。前の呼び出しが書いた内容を毎回上書きする |

**この例で学ぶこと**: ブックマークは利用者のデータとして扱われるファイルなので、16.1 の順 3「利用者のファイル」です（ツールが読み返してもいますが、順 3 が順 6 より先）。**1 件を 1 行にして `'a'` で追記する作りなら、15.2 の「新しく作るだけ（`open('a')` の追記）」で反しません。** 書き先をモデルが決められる形なら、解析器は矛（`fs_writeout_model_path`）を出し、矛の判定表に載ります（[I-1.13](#ai-1-13)）。

---

<a id="ai-1-12"></a>
### I-1.12 「アーカイブに残す」と言いながら元のメモを消す（宣言 D2 / 判定: 正 / 学ぶ点: 動かすのも既存のものを変える）

**コード**（作った例）

```python
 1  import os
 2  import shutil
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("notes")
 8  NOTES = os.path.expanduser("~/notes")
 9  ARCHIVE = os.path.join(NOTES, "archive")
10
11
12  def _move_to_archive(src):
13      os.makedirs(ARCHIVE, exist_ok=True)
14      shutil.copy2(src, ARCHIVE)
15      os.remove(src)
16
17
18  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
19  def archive_note(name: str) -> str:
20      """Archive a note. The note is kept in the archive folder."""
21      src = os.path.join(NOTES, name)
22      if not os.path.isfile(src):
23          return "no such note"
24      _move_to_archive(src)
25      return "archived"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.remove` | `FS_WRITE` | `fs_remove` | `server.py:15` |

解析器の言い分（手順 B）: 道筋 `_move_to_archive`、入口の呼び出し行 24。slot `path` の主体は MODEL。同じツールには、別の組 `shutil.copy2` × D2（`server.py:14`、不: `fs_writeout`）もあります。

**問い 1: 届くか** — 21 行で `src` を `~/notes/<name>` にします（`name` はモデルが決める引数）。22 行でファイルが無ければ抜けます。これは「前提の崩れで効果の前に抜ける」形なので条件に数えません（手引き 14.3 の「迷いやすい条件の書き方」の 2 行目）。24 行 → 14 行でコピーし、15 行で元を消します。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 手引き 15.2 の表「既存のものを消す・動かす・変える（`unlink` …）→ 反する」。22 行で確かめたとおり、消すのは呼び出しの前からあった利用者のメモです。コピーを残しても、元の場所のファイルが消えることに変わりはありません。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | 利用者のファイル |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:21`（src は `~/notes/<name>`、name はモデルが決める引数）→ `server.py:22`（ファイルがあるときだけ進む）→ `server.py:24` → `server.py:15` `os.remove(src)` |

**この例で学ぶこと**: docstring の言い分ではなく、コードの動作で決めます（手引き 11.2）。**消すのが同じ呼び出しで自分が作った一時ファイルなら、反しません**（誤、E2。15.2 の迷いやすい形）。別の組の `shutil.copy2`（14 行）は、アーカイブにある同じ名前の古いメモを上書きしうる書き出しで、不の中身の判定表で別に判定します。

---

<a id="ai-1-13"></a>
### I-1.13 「新しいメモを作る」がモデルの決めた名前で上書きする（宣言 D2 / 判定: 正 / 学ぶ点: 書き先をモデルが決められる書き出し）

**コード**（作った例）

```python
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("notes")
 7  NOTES_DIR = os.path.expanduser("~/notes")
 8
 9
10  def _note_path(title):
11      safe = title.replace("/", "_").strip()
12      return os.path.join(NOTES_DIR, f"{safe}.md")
13
14
15  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
16  def create_note(title: str, body: str) -> str:
17      """Create a new note."""
18      os.makedirs(NOTES_DIR, exist_ok=True)
19      path = _note_path(title)
20      with open(path, "w", encoding="utf-8") as fh:
21          fh.write(body)
22      return path
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `builtins.open` | `FS_WRITE` | `fs_writeout_model_path` | `server.py:20` |

解析器の言い分（手順 B）: 本体の中。slot `path` の主体は MODEL。18 行の `os.makedirs` は D2 の行になりません（新しく作るだけ）。

**問い 1: 届くか** — 19 行で `_note_path(title)` が `~/notes/<title>.md` を作り、20 行で `'w'` で開きます。前に `if` はありません。引数の値を**使う**だけで、`if` で分かれてはいないので、条件は `なし` です（手引き 14.3 の表の `引数` の例はどれも `if` で分かれる形。本書の読みは[付録 H-3](appendix-h-3.md#ah-3-4) の「行 1: `なし`」の注意と同じ）。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.2 の書き出しの行「書き先をモデルが決められるなら反する（既存のファイルを指せば上書きできる。原理 3-a）」。モデルが既存のメモと同じ題を渡せば、そのメモを上書きします。ツール名が「作る」でも、取りうる値の全体で考えます。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | 利用者のファイル |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:19`（path = `~/notes/<title>.md`。`_note_path` は 10-12 行）→ `server.py:20` `open(path, "w")`。title はモデルが決める引数で、既存のメモと同じ題なら上書きする |

**この例で学ぶこと**: 「書き先をモデルが決められるか」は問い 2 の話で、問い 1 の条件ではありません。**20 行が `open(path, "x")`（無いときだけ作る）なら、15.2 の「新しく作るだけ」で反しません。** 名前を毎回 `uuid` などで新しく作る作りでも、「呼び出しごとに新しい名前なら反しない」（15.2 の書き出しの行）です。

---

<a id="ai-1-14"></a>
### I-1.14 頁を見せるたびに閲覧数を `+1` する（宣言 D2・D4 / 判定: D2 は正、D4 は判定しない不 / 学ぶ点: `UPDATE` と D4 の不）

**コード**（作った例）

```python
 1  import sqlite3
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("wiki")
 7  DB = "wiki.db"
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False, idempotentHint=True))
11  def get_page(slug: str) -> str:
12      """Return a wiki page."""
13      conn = sqlite3.connect(DB)
14      row = conn.execute("SELECT body FROM pages WHERE slug = ?", (slug,)).fetchone()
15      if row is None:
16          return "not found"
17      conn.execute("UPDATE pages SET views = views + 1 WHERE slug = ?", (slug,))
18      conn.commit()
19      return row[0]
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `psycopg.Cursor.execute` | `DB` | `db_modify` | `server.py:17` |
| D4 | `psycopg.Cursor.execute` | `DB` | 不: `db_nonidempotent_statement` | `server.py:17` |

解析器の言い分（手順 B）: 本体の中。17 行の SQL の先頭語は `UPDATE`。

**問い 1: 届くか** — 15 行で頁が無ければ抜けます（前提の崩れ。条件に数えない）。頁があれば 17 行の `UPDATE` に毎回届きます。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか**

- D2: 手引き 15.2 の表「DB の `UPDATE` …→ 反する」。既存の行の `views` を変えます。答え: **はい**。
- D4: 手引き 15.4 の表「DB の `UPDATE`: `SET x = x + 1` …なら反する」。同じ `slug` で 2 回呼ぶと、2 回目でさらに 1 増えます。人が読めば反します。ただし、**D4 の不は判定しません**（手引き 18A.1「D3・D4 の不は判定しない（件数と理由だけ）」）。この組は判定表に載りません。

**判定と記録**（D2 の組。矛の判定表）

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | データベース |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:14`（SELECT で頁を読む）→ `server.py:15-16`（無ければ抜ける）→ `server.py:17` `UPDATE pages SET views = views + 1 WHERE slug = ?` |

**この例で学ぶこと**: 1 つの効果でも、宣言ごとに組と扱いが分かれます。D4 の組は、解析器が不を出し、人は反すると読みますが、判定はしません。報告には不の件数と理由だけが出ます（18A.1）。**17 行が `SET is_read = 1` なら、D4 には反しません（同じ値になる）が、D2 には反するままです**（既存の行を変える）。

---

<a id="ai-1-15"></a>
### I-1.15 httpx のクライアントで課題に `PATCH` する（宣言 D2 / 結果: 見落とし / 学ぶ点: 「足す」に見える `PATCH` と、語彙の外のメソッド）

**この例は見落としの判定表に載る形です**（手引き 18）。

**コード**（作った例）

```python
 1  import os
 2
 3  import httpx
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("tracker")
 8  API = "https://tracker.example.com/api/v2"
 9  HEADERS = {"Authorization": f"Token {os.environ.get('TRACKER_TOKEN', '')}"}
10
11
12  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
13  def add_label(issue_id: int, label: str) -> str:
14      """Add a label to an issue."""
15      with httpx.Client(base_url=API, headers=HEADERS, timeout=10) as client:
16          issue = client.get(f"/issues/{issue_id}").json()
17          labels = issue.get("labels", []) + [label]
18          client.patch(f"/issues/{issue_id}", json={"labels": labels})
19      return ", ".join(labels)
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| （行なし） | | | | |

解析器は、このツールに D2 の矛も不も出していません。効果として拾ったのは 16 行の `GET`（site 名は `httpx.AsyncClient.get`）だけです。

**問い 1: 届くか**（18.2 の 1〜3） — 本体は 13〜19 行で、木の中の呼び出し先はありません。18 行の `client.patch(...)` は、ライブラリの関数そのものが相手の状態を変える呼び出しです（18.2 の 2 の「ライブラリの関数そのもの」）。前に `if` は無く、毎回届きます。答え: **はい**。条件の種類は `なし`。深さは 0。

**問い 2: 宣言に反するか** — 手引き 15.2 の表「既存のものを…変える（…HTTP の `DELETE` / `PATCH`）→ 反する」。「ラベルを 1 つ足す」は足すだけに聞こえますが、動作は**既存の課題**の `labels` を書き換える `PATCH` です。表の行で決めます。答え: **はい**。

**判定と記録**（見落としの判定表の欄）

| 欄 | 値 |
|---|---|
| `outcome` | 見落とし |
| `cause` | 語彙 |
| `write_target` | 相手側の状態 |
| `condition_type` | なし |
| `condition` | なし |
| `depth` | 0 |
| `unknown_reason` | （空） |
| `output_found` | （空） |
| `evidence` | 読んだ範囲は `server.py:1-19`（本体 13-19。木の中の呼び出し先は無い）。`server.py:15` `httpx.Client(base_url=API, …)`（API は `https://tracker.example.com/api/v2`）→ `server.py:18` `client.patch(f"/issues/{issue_id}", json={"labels": labels})` で既存の課題を書き換える |

**この例で学ぶこと**: 本書で確かめると、解析器の sink の語彙（`authgap/catalog/sinks.py:536-558`）の httpx のセッションの行は `get`・`post`・`request` だけで、`patch` がありません。だから原因は「語彙」です（18.2 の 6）。**同じ 18 行を `requests.patch(...)` にすると、解析器は矛（`net_modify`、`server.py:19`）を出し、矛の判定表で正になります**（本書で試した）。site 名 `httpx.AsyncClient.get` は実際の `httpx.Client` と違いますが、kind が合っていれば判定に影響しません（手順 C）。

---

<a id="ai-1-16"></a>
### I-1.16 定数の外部ホストに祝日を問い合わせる（宣言 D3 / 判定: 正 / 学ぶ点: D3 は読み取りでも反しうる）

**コード**（作った例）

```python
 1  import httpx
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("calendar")
 6  HOLIDAYS_URL = "https://holidays.example.org/api/v1/jp"
 7
 8
 9  def _holidays(year):
10      resp = httpx.get(f"{HOLIDAYS_URL}/{year}", timeout=10)
11      resp.raise_for_status()
12      return resp.json()
13
14
15  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
16  def is_holiday(date: str) -> bool:
17      """Tell whether a date (YYYY-MM-DD) is a public holiday."""
18      return date in _holidays(date[:4])
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D3 | `httpx.get` | `NET` | `net_external_host` | `server.py:10` |

解析器の言い分（手順 B）: 道筋 `_holidays`、入口の呼び出し行 18。slot `url.host` の主体は OP（定数）。D1 の行はありません（`GET` なので）。

**問い 1: 届くか** — 18 行で `_holidays(date[:4])` を呼び、10 行で `httpx.get` を送ります。条件はありません。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 宛先は 6 行の `https://holidays.example.org/…` です。手引き 15.3 の「local の範囲」のどれでもない、ドットのある公開の名前です。表の「宛先が定数の外部ホスト → 反する」。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | 定数の外部ホスト |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:18`（is_holiday が `_holidays` を呼ぶ）→ `server.py:10` `httpx.get(f"{HOLIDAYS_URL}/{year}")`。HOLIDAYS_URL は `https://holidays.example.org/api/v1/jp`（6 行） |

**この例で学ぶこと**: D3 は「環境を変えるか」ではなく「外の相手と通信するか」です。読み取りの `GET` でも反します。D1 は反しません。**6 行が `http://holidays:8080/…`（ドットの無い名前）なら、解析器は同じ矛（`net_external_host`）を出しますが、手引き 15.3 ではドットの無い名前は local なので反しません。判定は誤です**（本書で試した。原因は 15.3 の「語彙・定義の差」。E1〜E9 のどれを書くかは手引きに書かれていません。[付録 H-4](appendix-h-4.md) の穴 H-4-24）。

---

<a id="ai-1-17"></a>
### I-1.17 宛先の URL をモデルが変えられる（宣言 D3 / 判定: 正 / 学ぶ点: 既定値が local でも、取りうる値の全体で読む）

**コード**（作った例）

```python
 1  import requests
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("docs-proxy")
 6  DEFAULT_BASE = "http://localhost:8080"
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
10  def fetch_doc(path: str, base_url: str = DEFAULT_BASE) -> str:
11      """Fetch a page from the local documentation server."""
12      resp = requests.get(f"{base_url}/{path.lstrip('/')}", timeout=10)
13      return resp.text[:5000]
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D3 | `requests.get` | `NET` | `net_model_host` | `server.py:12` |

解析器の言い分（手順 B）: 本体の中。slot `url.host` の主体は MODEL。

**問い 1: 届くか** — 12 行は本体の中で、毎回届きます。`base_url` は使うだけで、`if` で分かれません。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — `base_url` の既定値は `http://localhost:8080`（local）です。しかし、モデルは `base_url` に任意の URL を渡せます。手引き 15.3 の表「宛先をモデルが決められる → 反する（原理 3-a）」。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | モデルが決める宛先 |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:10`（引数 base_url。既定は `http://localhost:8080`）→ `server.py:12` `requests.get(f"{base_url}/…")`。base_url はモデルが決める引数で、外部の URL を渡せば外部と通信する |

**この例で学ぶこと**: 既定値や docstring（「ローカルの文書サーバ」）ではなく、モデルが**選べる**値の全体で読みます（手引き 11.3 の原理 3）。**`base_url` を引数から外し、宛先を定数の `DEFAULT_BASE` だけにすると、解析器は D3 の行を出さず、人も「local なので反しない」と読みます**（本書で試した）。

---

<a id="ai-1-18"></a>
### I-1.18 変換のたびに履歴へ追記する（宣言 D4 / 判定: 正 / 学ぶ点: D4 は「同じ引数で 2 回」）

**コード**（作った例）

```python
 1  import datetime
 2  import os
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("units")
 8  HISTORY = os.path.expanduser("~/.unit_history.txt")
 9  FACTORS = {("km", "mi"): 0.621371, ("mi", "km"): 1.609344}
10
11
12  def _record(line):
13      with open(HISTORY, "a", encoding="utf-8") as fh:
14          fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {line}\n")
15
16
17  @mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
18  def convert(value: float, src: str, dst: str) -> float:
19      """Convert a length between km and mi."""
20      result = value * FACTORS[(src, dst)]
21      _record(f"{value}{src} -> {result:.3f}{dst}")
22      return result
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D4 | `builtins.open` | `FS_WRITE` | `fs_append` | `server.py:13` |

解析器の言い分（手順 B）: 道筋 `_record`、入口の呼び出し行 21。

**問い 1: 届くか** — 20 行で換算し（対応しない単位なら `KeyError` で抜ける。前提の崩れ）、21 行で `_record` を呼び、13 行で `'a'` で開きます。答え: **はい**。条件の種類は `なし`。

**問い 2: 宣言に反するか** — 手引き 15.4 の問い「同じ引数で 2 回呼んだとき、2 回目が 1 回目の後の状態をさらに変えるか」。2 回目も 1 行増えます。表の「定数の `'a'` で追記する → 繰り返すと追記が重なるなら反する」と「時刻…を含むものを書く（ログの 1 行…）→ 反する」の両方に当たります。D4 には原理 3 を当てないので、同じ引数だけを考えます。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| `verdict` | 正 |
| `reachable` | はい |
| `condition_type` | なし |
| `condition` | なし |
| `violates` | はい |
| `write_target` | ログ |
| `error_class` | （空） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:21`（convert が `_record(...)` を呼ぶ）→ `server.py:13-14` `open(HISTORY, "a")` で時刻つきの 1 行を足す。同じ引数で 2 回呼ぶと 2 行になる |

**この例で学ぶこと**: 「いつ・何をした」の行で、ツールは読み返さないので「ログ」です（16.2）。**`_record` が「同じ行がすでにあれば書かない」作り（時刻なし）なら、解析器は同じ矛（`fs_append`）を出しますが、15.4 の「書く前に内容を確かめて、すでにあれば書かない → 反しない」により誤（E8）です**（本書で試した）。

---

<a id="ai-1-x"></a>
### I-1.x この分冊の例の一覧

「判定」の欄の「正」は矛の判定表、「違反」は不の中身の判定表（18A）、「見落とし」は見落としの判定表（18）での結果です。

| 番号 | 題 | 宣言 | 解析器 | 判定 | 学ぶ点 |
|---|---|---|---|---|---|
| [I-1.1](#ai-1-1) | 2 段奥のヘルパーでキャッシュを書く | D1 | 矛 `fs_write` | 正（`引数`、キャッシュ・状態の保存） | 道筋のたどり方。鍵が引数のキャッシュは `引数` |
| [I-1.2](#ai-1-2) | `INSERT` と `PRAGMA journal_mode=WAL` | D1 | 矛 `db_modify`・`db_persistent` | 正（`なし`、データベース） | 位置が 2 つの組（手順 G）。接続単位の PRAGMA は反しない |
| [I-1.3](#ai-1-3) | `main()` の中だけの DB の初期化 | D1 | 矛 `db_modify` | 正（`起動の方法`、データベース） | 14.4。lifespan なら E1 |
| [I-1.4](#ai-1-4) | 読むついでに `PUT` | D1 | 矛 `net_modify` | 正（`なし`、相手側の状態） | HTTP はメソッドで決まる |
| [I-1.5](#ai-1-5) | モデルが決めたコマンドを起動 | D1・D3 | 矛 `spawn_model`（2 組） | 正・正 | 宣言ごとの組。D3 は通信先の種類 |
| [I-1.6](#ai-1-6) | 引数があればレポートを書き出す | D1 | 矛 `fs_write` | 正（`引数`、利用者のファイル） | `引数` と既定値 |
| [I-1.7](#ai-1-7) | 一時ディレクトリと `rmtree` | D1 | 矛 `fs_write` | 正（`なし`、一時ファイル） | D1 では反し、D2 なら E2 |
| [I-1.8](#ai-1-8) | 環境変数で有効になる監査ログ | D1 | 矛 `fs_write` | 正（`運用者の設定`、ログ） | (B) に数えない条件 |
| [I-1.9](#ai-1-9) | `logging` の出力先がファイル | D1 | 何も出さない | 見落とし（語彙） | モジュール水準のログの設定を見る |
| [I-1.10](#ai-1-10) | 結果が空なら課題を作る `POST` | D1 | 不 `net_post` | 違反（`引数`、相手側の状態） | 相手の公式の文書を開いて決める |
| [I-1.11](#ai-1-11) | 読んで 1 つ足して書き戻す | D2 | 不 `fs_writeout` | 違反（`なし`、利用者のファイル） | 15 の前書きの表の行を採る |
| [I-1.12](#ai-1-12) | アーカイブと言いつつ元を消す | D2 | 矛 `fs_remove` | 正（`なし`、利用者のファイル） | 前提の崩れは条件に数えない |
| [I-1.13](#ai-1-13) | モデルの決めた名前で上書き | D2 | 矛 `fs_writeout_model_path` | 正（`なし`、利用者のファイル） | 書き先は問い 2、条件は問い 1 |
| [I-1.14](#ai-1-14) | 閲覧数を `+1` | D2・D4 | 矛 `db_modify`・不 `db_nonidempotent_statement` | D2 は正、D4 は判定しない | D4 の不は数に入らない |
| [I-1.15](#ai-1-15) | httpx で `PATCH` | D2 | 何も出さない | 見落とし（語彙） | 「足す」に見える `PATCH` も反する |
| [I-1.16](#ai-1-16) | 定数の外部ホストに問い合わせ | D3 | 矛 `net_external_host` | 正（定数の外部ホスト） | ドットの無い名前なら誤 |
| [I-1.17](#ai-1-17) | 宛先の URL をモデルが変えられる | D3 | 矛 `net_model_host` | 正（モデルが決める宛先） | 既定値ではなく取りうる値の全体 |
| [I-1.18](#ai-1-18) | 変換のたびに履歴へ追記 | D4 | 矛 `fs_append` | 正（`なし`、ログ） | 中身を確かめてから書くなら E8 |

---

<a id="ai-1-y"></a>
### I-1.y 自分で判定してみる

コードと判定表の行（凍結版の解析器の本物の出力）だけを出します。手引きを開いて、判定と記録の欄（`verdict`・`condition_type`・`write_target`）を書いてから、答えを開いてください。行が無い問題は、そのツールが見落としの判定表に載ったとして、`outcome` を答えてください。

#### 問 1（宣言 D1）

```python
 1  import json
 2  import os
 3  import time
 4
 5  import requests
 6  from mcp.server.fastmcp import FastMCP
 7  from mcp.types import ToolAnnotations
 8
 9  mcp = FastMCP("crm")
10  API = "https://crm.example.com/api"
11  AUTH_URL = "https://crm.example.com/oauth/token"
12  TOKEN_FILE = os.path.expanduser("~/.crm_token.json")
13
14
15  def _token():
16      with open(TOKEN_FILE) as fh:
17          tok = json.load(fh)
18      if tok["expires_at"] < time.time():
19          resp = requests.post(
20              AUTH_URL,
21              data={"grant_type": "refresh_token", "refresh_token": tok["refresh_token"]},
22              timeout=10,
23          )
24          tok = resp.json()
25          with open(TOKEN_FILE, "w") as fh:
26              json.dump(tok, fh)
27      return tok["access_token"]
28
29
30  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
31  def get_contact(contact_id: str) -> dict:
32      """Show a CRM contact."""
33      headers = {"Authorization": f"Bearer {_token()}"}
34      return requests.get(f"{API}/contacts/{contact_id}", headers=headers, timeout=10).json()
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:25` |

<details><summary>答え</summary>

- 判定: **正**。`reachable` はい、`violates` はい。
- 問い 1: 33 行の `_token()` → 18 行でトークンの期限が切れていれば → 25 行 `open(TOKEN_FILE, "w")`。`condition_type` は **`失敗・期限切れ`**（手引き 14.3 の表の例「トークンの更新」）。`condition` は「保存したトークンの期限が切れているとき」。
- 問い 2: 15.1 の `FS_WRITE` の行。
- `write_target`: **キャッシュ・状態の保存**（16.2「OAuth のトークンをファイルに保存 → 後で読み返す」。16 行で同じツールが読み返す）。
- `evidence`: `server.py:33 → server.py:18 → server.py:25`。
- 補足: 同じツールの別の組 `requests.post` × D1（`server.py:19`、不: `net_post`）は、トークンを得る `POST` です。15.1 の迷いやすい形により相手の文書で決め、文書に無ければ不明にします（不の中身の判定表）。

</details>

#### 問 2（宣言 D2）

```python
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("files")
 7  ROOT = os.path.expanduser("~/Documents")
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
11  def rename_file(old_name: str, new_name: str) -> str:
12      """Rename a file in the Documents folder."""
13      src = os.path.join(ROOT, old_name)
14      dst = os.path.join(ROOT, new_name)
15      os.rename(src, dst)
16      return dst
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.rename` | `FS_WRITE` | `fs_remove` | `server.py:15` |

<details><summary>答え</summary>

- 判定: **正**。`condition_type` は `なし`（本体で毎回届く）。
- 問い 2: 15.2 の表「既存のものを消す・動かす・変える（…`rename`…）→ 反する」。元の名前のファイルが無くなります（さらに、`new_name` に既存のファイルの名前を渡せば上書きします）。
- `write_target`: **利用者のファイル**（モデルが指定した `~/Documents` の中のファイル）。
- `evidence`: `server.py:13-14`（src・dst は `~/Documents/<引数>`）→ `server.py:15` `os.rename(src, dst)`。

</details>

#### 問 3（宣言 D1）

```python
 1  import os
 2  import shutil
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("images")
 8  PREVIEW = "/tmp/mcp_preview.png"
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def image_size(path: str) -> int:
13      """Return the size in bytes of an image, keeping a preview copy."""
14      shutil.copy(path, PREVIEW)
15      return os.path.getsize(PREVIEW)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `shutil.copy` | `FS_WRITE` | `fs_write` | `server.py:14` |

<details><summary>答え</summary>

- 判定: **正**。`condition_type` は `なし`。
- 問い 2: 15.1 の `FS_WRITE` の行（コピーもファイルの書き込み）。
- `write_target`: **一時ファイル**。書き先は固定の `/tmp/mcp_preview.png` で、利用者が指定した場所ではありません。16.1 の順 5「OS の一時領域（`tempfile`、`/tmp`）に作る」に当たり、16.2 の「OS の一時領域に置き、後で読み返す → 一時ファイル（場所で決める）」とも合います。
- `evidence`: `server.py:14` `shutil.copy(path, PREVIEW)`。PREVIEW は `/tmp/mcp_preview.png`（8 行）。毎回届く。

</details>

#### 問 4（宣言 D1）

```python
 1  import os
 2  import time
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("search")
 8  TRACE_FILE = "search_trace.log"
 9  INDEX = {"alpha": ["a.txt"], "beta": ["b.txt"]}
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def search(word: str, trace: bool = False) -> list:
14      """Search the index."""
15      hits = INDEX.get(word, [])
16      if trace or os.environ.get("SEARCH_TRACE"):
17          with open(TRACE_FILE, "a") as fh:
18              fh.write(f"{time.time():.0f} search {word} -> {len(hits)}\n")
19      return hits
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | `FS_WRITE` | `fs_write` | `server.py:17` |

<details><summary>答え</summary>

- 判定: **正**。
- 問い 1: 16 行は「`trace` が真 **または** 環境変数 `SEARCH_TRACE` が設定されている」。手引き 14.3 の「迷いやすい条件の書き方」の「または」の行により、一番弱い道の条件だけを書きます。`condition_type` は **`引数`**（`運用者の設定` を並べない。(B) に数える）。`condition` は「引数 trace に真を渡したとき」。
- 問い 2: 15.1 の `FS_WRITE` の行。
- `write_target`: **ログ**（「時刻 search 語 -> 件数」の、いつ・何をしたの行。読み返さない）。
- `evidence`: `server.py:16`（`if trace or os.environ.get("SEARCH_TRACE")`）→ `server.py:17-18` `open(TRACE_FILE, "a")`。

</details>

#### 問 5（宣言 D2）

```python
 1  import requests
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("kv")
 6
 7
 8  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
 9  def store_value(endpoint: str, value: str) -> int:
10      """Store a value at a key-value endpoint (e.g. http://kv.local/keys/foo)."""
11      resp = requests.put(endpoint, data=value, timeout=10)
12      return resp.status_code
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `requests.put` | `NET` | `net_put_model_url` | `server.py:11` |

<details><summary>答え</summary>

- 判定: **正**。`condition_type` は `なし`。
- 問い 2: 15.2 の表「HTTP の `PUT`: 宛先をモデルが決められるなら反する」。`endpoint` はモデルが決める引数で、既存のキーを指せば値を置き換えます（原理 3-a）。
- `write_target`: **相手側の状態**（16.1 の順 1）。
- `evidence`: `server.py:11` `requests.put(endpoint, data=value)`。endpoint はモデルが決める引数。

</details>

#### 問 6（宣言 D2。行なし → 見落としの判定）

```python
 1  import sqlite3
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("prefs")
 7  DB = "prefs.db"
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
11  def set_preference(key: str, value: str) -> str:
12      """Save a user preference."""
13      conn = sqlite3.connect(DB)
14      conn.execute("INSERT OR REPLACE INTO prefs (key, value) VALUES (?, ?)", (key, value))
15      conn.commit()
16      return "saved"
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| （行なし） | | | | |

<details><summary>答え</summary>

- `outcome`: **反する動作は無い**。
- 18.2 の 3 で書き出す候補は 14 行の `INSERT OR REPLACE` です。手引き 15 の前書きの表「D2: `INSERT OR REPLACE`・`ON CONFLICT … DO UPDATE`・`CREATE OR REPLACE` → 反しない（15.2 の『新しく作るだけ』の行の `INSERT` / `CREATE`）」により、反する動作に入りません。13 行の `sqlite3.connect` が DB のファイルを作るのも、D2 では新しく作るだけです。
- `evidence` には、読んだ範囲（`server.py:11-16`）を書きます（18.4「反する動作は無いでも、読んだ範囲を書く」）。
- 注意: 「既存の値を置き換えるのでは」と感じても、表の行を採ります（15 の前書き、D76）。

</details>

#### 問 7（宣言 D1）

```python
 1  import sqlite3
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("metrics")
 7  DB = "metrics.db"
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
11  def table_sizes(optimize: bool = True) -> dict:
12      """Report the row count of each table."""
13      conn = sqlite3.connect(DB)
14      if optimize:
15          conn.execute("VACUUM")
16      names = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
17      return {n: conn.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0] for n in names}
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | `DB` | `db_persistent` | `server.py:15` |

<details><summary>答え</summary>

- 判定: **正**。
- 問い 1: 14 行 `if optimize:` ですが、既定値が `True` なので、引数を渡さなくても届きます。手引き 14.3 の「迷いやすい条件の書き方」の 3 行目により、`condition_type` は **`なし`**（`引数` にしない）。
- 問い 2: 15.1 の表「DB に残る設定・保守（`PRAGMA journal_mode=WAL`、`VACUUM` など）→ 反する」。
- `write_target`: **データベース**。
- `evidence`: `server.py:14`（optimize の既定は True）→ `server.py:15` `conn.execute("VACUUM")`。
- 手順 C: site は psycopg と表示されますが sqlite3 で、kind DB は合います（`note` に書く）。

</details>

#### 問 8（宣言 D1。行なし → 見落としの判定）

```python
 1  import logging
 2  import sys
 3
 4  from mcp.server.fastmcp import Context, FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  logging.basicConfig(stream=sys.stderr, level=logging.INFO)
 8  log = logging.getLogger("dict")
 9
10  mcp = FastMCP("dict")
11  WORDS = {"apple": "a fruit", "river": "a large stream of water"}
12
13
14  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
15  async def define(word: str, ctx: Context) -> str:
16      """Look up a word."""
17      log.info("define %s", word)
18      await ctx.info(f"looking up {word}")
19      return WORDS.get(word, "not found")
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| （行なし） | | | | |

<details><summary>答え</summary>

- `outcome`: **反する動作は無い**。
- 18.3 の最後の注意どおりモジュール水準のログの設定を見ると、7 行の出力先は標準エラーです。手引き 15.1 の迷いやすい形「標準出力・標準エラーへのログ: ファイルではないので反しない」。18 行の `ctx.info()` も「クライアントへの通知: 環境を変えないので反しない」。
- [I-1.9](#ai-1-9) との違いは 7 行（`basicConfig(filename=…)` か `stream=sys.stderr` か）だけです。
- `evidence` には読んだ範囲（`server.py:1-19`）を書きます。

</details>

---

[← 前](appendix-i.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-2.md)
