[← 前](appendix-i-2.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-4.md)

---

# 付録 I-3 条件とラベルの付け方 — 条件つきで届く・書き込み先の種類

> **この分冊の答えは、本書の答え（本記録者の判定）です。** 最終評価の判定は、学生が手引きを当てて自分で行います。

<a id="ai-3-0"></a>
## この分冊で学ぶこと

この分冊の例は、**ほとんどが正**（到達して、宣言に反する）です。正か誤かではなく、正にした後に書く 2 つの欄の付け方を練習します。

- **`condition_type`（条件の種類）**: 効果が「どんなときに」起きるか。手引き 14.3 の 7 種類から選びます。
- **`write_target`（書き込み先の種類）**: 何に書いたか。手引き 16.1 の 8 種類から選びます。D3 の正では、代わりに通信先の種類（手引き 16.3）を書きます。
- **`target_by_arg`**（D84。**D1 の正だけ**）: 変える場所（書き先のパス、DB の表・行、相手側の資源、起動するコマンドとその引数）を、ツールの引数の値が一部でも決めるか。`はい` / `いいえ` / `決められない`。決まったフォルダの外に出られるかなどは `note` に書きます。この分冊の例の表にも書き足しました。

どちらの欄も、**正か誤かを変えません。** 変わるのは、併記の数 (B)(C) と、ラベルの内訳です。だから、1 例ごとに「この選び方で (A)(B)(C) のどれに数えるか」を書きます。

手引きの文は、今の手引き `docs/drafts/final_judging_guide_draft.md`（D76 を反映した版）に従います。[付録 H-3](appendix-h-3.md) と [付録 H-5](appendix-h-5.md) は直す前の下書きを引用しているので、食い違うところは手引きの今の文（とくに「（D76）」の印の文）を採ります。考え方の説明は [第 49 章](ch49.md)（条件つきの到達）と [第 51 章](ch51.md)（ラベル）にあります。

<a id="ai-3-rules"></a>
## 先に押さえる規則（手引きから）

### 条件の種類と (A)(B)(C)（手引き 14.3）

| `condition_type` | 例 | (A) | (B) | (C) |
|---|---|---|---|---|
| `なし` | 毎回届く | 数える | 数える | 数える |
| `引数` | モデルが渡す引数の値による | 数える | 数える | 数えない |
| `初回` | 初回だけ・キャッシュが無いときだけ | 数える | 数える | 数えない |
| `失敗・期限切れ` | トークンの更新、再試行、エラー時の後始末 | 数える | 数える | 数えない |
| `外部の状態` | ファイルが無いとき、相手が特定の応答を返したとき | 数える | 数える | 数えない |
| `運用者の設定` | 環境変数・設定ファイル・起動の引数で有効になる | 数える | **数えない** | 数えない |
| `起動の方法` | 初期化が `main()` の中だけにあり、`main()` を通らない起動で届く | 数える | **数えない** | 数えない |

- **(A)** は主の数で、条件を問いません。**(B)** は運用者が決める条件（運用者の設定・起動の方法）が 1 つでもある正を除いた数、**(C)** は条件なしで届く正だけの数です（[第 49 章](ch49.md) の 49.3 節）。
- 条件が「かつ」で重なるときは全部を `;` で並べます。1 つでも運用者が決める条件があれば (B) に数えません。

手引き 14.3 の「迷いやすい条件の書き方」（D76）は、この分冊の中心です。

| 形 | `condition_type` に書くもの | この分冊の例 |
|---|---|---|
| 行は毎回実行されるが、環境が変わるのは一部（`exist_ok=True`・`IF NOT EXISTS`・`missing_ok=True`） | 環境が変わる場合の条件（`初回` / `外部の状態`） | [I-3.4](#ai-3-4)・[I-3.7](#ai-3-7) |
| 空の入力・失敗・前提の崩れで、効果の前に抜ける | 条件に数えない | [I-3.13](#ai-3-13) |
| 引数の既定値で効果が起きる（`save: bool = True`） | `なし` | [I-3.3](#ai-3-3) |
| 既定では起きるが、設定で止められる | `運用者の設定` を書かない | [I-3.9](#ai-3-9)・問 1 |
| ツールの登録そのものが設定しだい | `運用者の設定` | 問 5 |
| 「または」でつながる条件 | 一番弱い道の条件だけ | [I-3.11](#ai-3-11) |
| 「かつ」で重なる条件 | 全部を `;` で並べる | [I-3.12](#ai-3-12)・問 8 |

1 つの条件が 2 つの種類に読めるときは、表の上の方を **1 つだけ** 書きます（鍵が引数のキャッシュの「無いとき」は `引数`。`起動の方法` の位置で最初の呼び出しだけ起きるものは `起動の方法` だけ）。

### 書き込み先の種類（手引き 16.1・16.2）

**上から順に当てはめ、最初に当てはまったものを付けます。**

| 順 | 種類 | 一言で |
|---|---|---|
| 1 | 相手側の状態 | NET の効果で相手のサーバの状態を変える |
| 2 | データベース | DB の行・スキーマ・残る設定を変える |
| 3 | 利用者のファイル | 利用者・モデルが指定した場所、または利用者の文書・データ |
| 4 | ログ | 記録のためだけに書き、判定しているツールは読み返さない（「いつ・何をした」の行） |
| 5 | 一時ファイル | 同じ呼び出しで作って消す、または OS の一時領域（`tempfile`・`/tmp`）に作る |
| 6 | キャッシュ・状態の保存 | ツールの動作のために保存し、後で読み返す。初回に作る作業ディレクトリ・設定ファイル |
| 7 | プロセスの起動・コードの実行 | SPAWN / EXEC の正 |
| 8 | その他・不明 | どれにも当てはまらない、または決められない |

D76 で決まった境目（手引き 16.2）: 初回に作る作業ディレクトリは、中身を読み返さなくてもキャッシュ・状態の保存です。OS の一時領域に置いたものは、後で読み返しても一時ファイルです（場所で決める）。運用者が環境変数で決めた場所は、中身で決めます。SPAWN / EXEC の正は、子が何を変えるか分かっても、常にプロセスの起動・コードの実行です。

### 1 組に位置が複数あるとき（手引き 手順 G）

- 1 つでも「到達する かつ 反する」位置があれば正。**条件つきの位置で正が見つかったら、そこで止めてよい**（`note` に書く。D76）。
- `condition_type` は読んだ位置のうち一番弱い条件。弱い順は `なし` → 運用者が決めない条件 → 運用者が決める条件（`運用者の設定`・`起動の方法`）で、運用者が決めない条件どうしは 14.3 の表の上からの順（`引数` → `初回` → `失敗・期限切れ` → `外部の状態`）で先のものを弱いとします（手順 G。2026-10-06 に手引きに書き足された）。読まなかった位置に弱いものがありうるので、**(B)(C) は報告で下限**です。
- 種類が違う位置が複数あるときは、**最初に正と分かった位置の種類**を付けます（D76）。

<a id="ai-3-test"></a>
## 本書の試験について

この分冊の例は、すべて本書のために書いた小さな FastMCP のサーバです。1 例を 1 つの木（`server.py` 1 つ）にして、凍結版の解析器（タグ `analyzer-freeze-3`。走らせる前に `git diff analyzer-freeze-3 -- authgap/` が空であることを確かめた）で、Python 3.12 で走らせました。走らせ方は `scripts/scan_v2.py` と同じ `authgap.runner.run(RunConfig(...))` で、判定表の行は `scripts/final_sample.py` の `classify_pairs`・`pair_locations`（抜き取りの道具が判定表を作るのと同じ関数）で出しました。各例の「判定表の行」は、その出力の写しです。

- コードの左の数字は行番号です（写して使うときは消してください）。`locations` と `evidence` の行番号はこの番号です。
- sqlite3 の呼び出しは、解析器が site を `psycopg.Cursor.execute` と表示します。動作の種類（kind = `DB`）は合っているので、判定には影響しません（手引き 手順 C）。
- `evidence` のパスは木の根からの相対です（手引き 手順 H）。正の例では `error_class`・`unknown_reason` を書きません（D83）。D1 の正には `target_by_arg` を書きます（D84）。

---

<a id="ai-3-1"></a>
### I-3.1 毎回届くログの追記（宣言 D1 / 判定: 正 / 学ぶ点: 条件 `なし` とラベル「ログ」の基準点）

**コード**（作った例）

```python
 1  import os
 2  import time
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("notes")
 7  NOTES_DIR = os.path.expanduser("~/notes")
 8  LOG_PATH = os.path.expanduser("~/.notes_search.log")
 9
10
11  def _log(query, n):
12      with open(LOG_PATH, "a") as fh:
13          fh.write(f"{time.time():.0f} search {query!r} hits={n}\n")
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def search_notes(query: str) -> list[str]:
18      """Search note titles."""
19      hits = [n for n in os.listdir(NOTES_DIR) if query.lower() in n.lower()]
20      _log(query, len(hits))
21      return hits
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:12` |

**問い 1: 届くか** — 本体の 20 行 `_log(query, len(hits))` から、11 行の `_log` に入り、12 行で `open(LOG_PATH, "a")` を開きます（解析器の道筋 `_log`）。道筋に `if` はなく、`return` も先にありません。答え: **はい**。条件の種類: **`なし`**（毎回届く）。

**問い 2: 宣言に反するか** — 手引き 15.1 の表の 1 行目「ファイルの書き込み・作成・削除・移動・権限の変更（`FS_WRITE` すべて）→ 反する。ログ・キャッシュ・一時ファイル…も含む」に当たります。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | なし |
| write_target | ログ |
| target_by_arg | いいえ |
| evidence | `server.py:20 → server.py:12` `open(LOG_PATH, "a")`。`LOG_PATH` は `~/.notes_search.log`。呼ぶたびに時刻・検索語・件数の 1 行を追記する。条件なし。 |
| note | `search_notes` の道筋に `LOG_PATH` を読む行は無い（16.1 の「読み返す」の主語は判定しているツールだけ）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: ログの 1 行でも D1 には反します（手引き 11.3。軽重はラベルで表す）。ラベルは、「いつ・何をした」を書くだけで読み返さないので「ログ」です（16.2、D76）。**違い**: 同じ 1 行を標準エラー（`print(..., file=sys.stderr)`）に出すなら、ファイルではないので反しません（15.1 の迷いやすい形）。

---

<a id="ai-3-2"></a>
### I-3.2 引数を渡したときだけ書き出す（宣言 D1 / 判定: 正 / 学ぶ点: 条件 `引数` とラベル「利用者のファイル」）

**コード**（作った例）

```python
 1  import json
 2  import sqlite3
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("sales")
 7  DB_PATH = "sales.db"
 8
 9
10  def _query(region):
11      conn = sqlite3.connect(DB_PATH)
12      rows = conn.execute("SELECT month, total FROM sales WHERE region = ?", (region,)).fetchall()
13      conn.close()
14      return rows
15
16
17  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
18  def sales_report(region: str, output_file: str = "") -> str:
19      """Summarize sales for a region. Optionally save the report."""
20      rows = _query(region)
21      report = json.dumps({"region": region, "rows": rows}, indent=2)
22      if output_file:
23          with open(output_file, "w") as fh:
24              fh.write(report)
25          return f"saved to {output_file}"
26      return report
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:23` |

**問い 1: 届くか** — 本体の 22 行 `if output_file:` が真のとき、23 行で `open(output_file, "w")` を開きます。`output_file` はツールの引数で、既定値 `""` のままなら書きません。モデルが空でない値を渡せば届きます。答え: **はい**。条件の種類: **`引数`**（手引き 14.3「モデルが渡す引数の値による」）。なお 12 行の `SELECT` は読み取りで、解析器も矛を出していません。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 引数 |
| write_target | 利用者のファイル |
| target_by_arg | はい |
| evidence | `server.py:22`（`if output_file:`）→ `server.py:23` `open(output_file, "w")`。`output_file` はモデルが決める引数で、そのパスにレポートを書き出す。条件: 引数 `output_file` を空でない値で渡したとき。 |
| note | target_by_arg: 書き先のパスを引数 `output_file` が丸ごと決める（どこでも指せる）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: 引数の条件はモデルが選べるので、(B) には残ります。(C) からだけ外れます。ラベルは、モデルが指定した場所への書き出しなので「利用者のファイル」です（16.1 の順 3、16.2「モデルが決めたパスへのエクスポート」）。v4 の M18 と同じ形です（手引き 20.2）。**違い**: 既定値が `output_file: str = "report.json"` なら、引数を渡さなくても書くので `なし` になります（次の例）。

---

<a id="ai-3-3"></a>
### I-3.3 引数の既定値で毎回起きる（宣言 D1 / 判定: 正 / 学ぶ点: 既定値で起きるものは `なし`）

**コード**（作った例）

```python
 1  import os
 2  import time
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("notes")
 7  NOTES_DIR = os.path.expanduser("~/notes")
 8  ACCESS_LOG = os.path.expanduser("~/.notes_access.log")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def read_note(name: str, track: bool = True) -> str:
13      """Read one note. Access is recorded unless track is False."""
14      with open(os.path.join(NOTES_DIR, name)) as fh:
15          body = fh.read()
16      if track:
17          with open(ACCESS_LOG, "a") as log:
18              log.write(f"{time.time():.0f} read {name}\n")
19      return body
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:17` |

**問い 1: 届くか** — 本体の 16 行 `if track:` が真のとき、17 行で `open(ACCESS_LOG, "a")` を開きます。`track` の既定値は `True` です。モデルが `track` を渡さなければ、毎回書きます。答え: **はい**。条件の種類: **`なし`**（手引き 14.3 の迷いやすい書き方「引数の既定値で効果が起きる（`save: bool = True`）→ `なし`（引数を渡さなくても起きる）」、D76）。14 行の `open` は読み取り（`'r'`）で、組には入りません。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | なし |
| write_target | ログ |
| target_by_arg | いいえ |
| evidence | `server.py:16`（`if track:`、`track` の既定値は `True`）→ `server.py:17` `open(ACCESS_LOG, "a")`。呼ぶたびに時刻と読んだノートの名前を `~/.notes_access.log` に追記する。 |
| note | 16 行の `if track:` は既定値 `True` で真。`track=False` を渡したときだけ書かないが、何も渡さなくても届くので条件なし（14.3、D76）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: 「`if` があるから条件つき」ではありません。**何もしなくても起きるか**で決めます。**違い**: `track: bool = False` なら、モデルが `track=True` を渡したときだけ書くので `引数` になり、(C) から外れます。

---

<a id="ai-3-4"></a>
### I-3.4 `exist_ok=True` で作る作業ディレクトリ（宣言 D1 / 判定: 正 / 学ぶ点: 毎回実行される行の `初回` と「初回に作る作業ディレクトリ」）

**コード**（作った例）

```python
 1  import os
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("projects")
 6  WORKDIR = os.path.expanduser("~/.projtool")
 7
 8
 9  def _workspace():
10      os.makedirs(WORKDIR, exist_ok=True)
11      return WORKDIR
12
13
14  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
15  def list_projects() -> list[str]:
16      """List saved projects."""
17      d = _workspace()
18      return sorted(n for n in os.listdir(d) if n.endswith(".json"))
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.makedirs` | FS_WRITE | `fs_write` | `server.py:10` |

**問い 1: 届くか** — 本体の 17 行 `_workspace()` から、10 行の `os.makedirs(WORKDIR, exist_ok=True)` に届きます。この行は毎回実行されます。しかし環境が変わる（ディレクトリができる）のは、`~/.projtool` がまだ無いとき、つまり最初の呼び出しだけです。答え: **はい**。条件の種類: **`初回`**（手引き 14.3 の迷いやすい書き方の 1 行目「行は毎回実行されるが、環境が変わるのは一部（`makedirs(d, exist_ok=True)` …）→ 環境が変わる場合の条件」、D76）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行（ディレクトリの作成も含む）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 初回 |
| write_target | キャッシュ・状態の保存 |
| target_by_arg | いいえ |
| evidence | `server.py:17 → server.py:10` `os.makedirs(WORKDIR, exist_ok=True)`。`WORKDIR` は `~/.projtool`。無ければ作る。18 行でその中を一覧する。条件: `~/.projtool` がまだ無いとき（最初の呼び出し）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: `exist_ok=True` は「毎回」ではなく `初回` です（D76 で決めた。v4 の M06 も、今の規則ではこの読み方です。手引き 20.2）。ラベルは手引き 16.2「初回だけ `~/.app/` を作る → キャッシュ・状態の保存（作業ディレクトリ）」です。中身を読み返さなくても同じです（16.2、D76）。**違い**: 同じ `os.makedirs` がモジュールの一番上（import 時）にあれば、ツールの道筋ではないので到達しません（手引き 14.2・14.4。解析器もこの組を出しません。[I-3.9](#ai-3-9) の 10 行）。

---

<a id="ai-3-5"></a>
### I-3.5 初回だけ作る索引を `/tmp` に置く（宣言 D1 / 判定: 正 / 学ぶ点: `初回` と、場所で決まる「一時ファイル」）

**コード**（作った例）

```python
 1  import json
 2  import os
 3  import tempfile
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("dict")
 8  WORDS = "/usr/share/dict/words"
 9  INDEX = os.path.join(tempfile.gettempdir(), "dictmcp", "index.json")
10
11
12  def _build_index():
13      idx = {}
14      with open(WORDS) as fh:
15          for w in fh:
16              idx.setdefault(w[:1].lower(), []).append(w.strip())
17      os.makedirs(os.path.dirname(INDEX), exist_ok=True)
18      with open(INDEX, "w") as fh:
19          json.dump(idx, fh)
20
21
22  def _load_index():
23      if not os.path.exists(INDEX):
24          _build_index()
25      with open(INDEX) as fh:
26          return json.load(fh)
27
28
29  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
30  def words_starting_with(letter: str) -> list[str]:
31      """Words that start with the letter."""
32      return _load_index().get(letter.lower(), [])[:50]
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:18` |
| D1 | `os.makedirs` | FS_WRITE | `fs_write` | `server.py:17` |

この例では 1 行目（`builtins.open` の組）を判定します。2 行目は別の組です（答えは下に添えます）。

**問い 1: 届くか** — 本体の 32 行 `_load_index()` → 23 行 `if not os.path.exists(INDEX):` → 24 行 `_build_index()` → 18 行 `open(INDEX, "w")`（解析器の道筋 `_load_index -> _build_index`）。`INDEX` は引数に依らない固定のパスです。索引がまだ無いとき、つまり最初の呼び出しで書きます。答え: **はい**。条件の種類: **`初回`**（手引き 14.3「初回だけ・キャッシュが無いときだけ」）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行（一時ファイルも含む）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 初回 |
| write_target | 一時ファイル |
| target_by_arg | いいえ |
| evidence | `server.py:32 → server.py:23`（`if not os.path.exists(INDEX):`）`→ server.py:24 → server.py:18` `open(INDEX, "w")`。`INDEX` は `tempfile.gettempdir()` の下の固定のパス。無ければ索引を作って書く。条件: 索引 `<一時領域>/dictmcp/index.json` がまだ無いとき。 |
| note | 25 行で同じツールが読み返すので順 6 にも当たるが、OS の一時領域に置くので順 5 が先（16.2、D76）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。2 行目の `os.makedirs` の組も、同じ道筋・同じ条件（`初回`）・同じラベル（一時ファイル）で正です。

**この例で学ぶこと**: ラベルは上から順に当て、**場所で決まる**ことがあります。読み返すキャッシュでも、`/tmp` や `tempfile` の下なら「一時ファイル」です（手引き 16.2「OS の一時領域に置き、後で読み返す → 一時ファイル（場所で決める）」、D76）。**違い（2 つ）**: `INDEX` が `~/.cache/dictmcp/index.json` なら「キャッシュ・状態の保存」です。また、鍵が引数のキャッシュ（`f"{letter}.json"` が無いとき）なら、条件の種類は `初回` ではなく `引数` です（14.3「1 つだけ。表の上からの順で先のもの」、D76。[I-3.9](#ai-3-9)）。

---

<a id="ai-3-6"></a>
### I-3.6 トークンの期限切れで保存し直す（宣言 D1 / 判定: 正 / 学ぶ点: `失敗・期限切れ` とトークンの保存）

**コード**（作った例）

```python
 1  import json
 2  import os
 3  import time
 4  import requests
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("calendar")
 9  TOKEN_FILE = os.path.expanduser("~/.calmcp/token.json")
10  API = "https://calendar.example.com/v1"
11
12
13  def _refresh(tok):
14      r = requests.post(f"{API}/oauth/token", data={"refresh_token": tok["refresh_token"]})
15      new = r.json()
16      with open(TOKEN_FILE, "w") as fh:
17          json.dump(new, fh)
18      return new
19
20
21  def _token():
22      with open(TOKEN_FILE) as fh:
23          tok = json.load(fh)
24      if tok["expires_at"] < time.time():
25          tok = _refresh(tok)
26      return tok["access_token"]
27
28
29  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
30  def list_events(day: str) -> list[dict]:
31      """List calendar events on a day."""
32      headers = {"Authorization": f"Bearer {_token()}"}
33      return requests.get(f"{API}/events", params={"day": day}, headers=headers).json()
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:16` |

解析器は同じツールに、`requests.post`（14 行）× D1 の**不**（理由 `net_post`）も出しています。不は別の組で、不の中身の手順（手引き 18A）で扱います。ここでは扱いません。

**問い 1: 届くか** — 本体の 32 行 `_token()` → 24 行 `if tok["expires_at"] < time.time():` → 25 行 `_refresh(tok)` → 16 行 `open(TOKEN_FILE, "w")`（道筋 `_token -> _refresh`）。保存してあるトークンの期限が切れているときに届きます。答え: **はい**。条件の種類: **`失敗・期限切れ`**（手引き 14.3「トークンの更新、再試行、エラー時の後始末」）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 失敗・期限切れ |
| write_target | キャッシュ・状態の保存 |
| target_by_arg | いいえ |
| evidence | `server.py:32 → server.py:24`（期限の比較）`→ server.py:25 → server.py:16` `open(TOKEN_FILE, "w")`。`TOKEN_FILE` は `~/.calmcp/token.json`。更新したトークンで上書きする。22 行で同じツールが読み返す。条件: 保存したアクセストークンの期限が切れているとき。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: 期限切れは運用者が決める条件ではないので (B) に残ります。ラベルは手引き 16.2「OAuth のトークンをファイルに保存 → キャッシュ・状態の保存（後で読み返す）」です。**違い**: OAuth を使うかどうかが環境変数で決まり、かつ期限切れのときだけ書くなら、`運用者の設定;失敗・期限切れ` と並べ、(B) から外れます（14.3 の「かつ」の行。v4 の R04。[問 8](#ai-3-y)）。

---

<a id="ai-3-7"></a>
### I-3.7 前の呼び出しの残りを消す（宣言 D1 / 判定: 正 / 学ぶ点: `missing_ok=True` の `外部の状態` と、ラベル「その他・不明」に決めた境目）

**コード**（作った例。`~/.worker_mailbox` は、別に動いているワーカーのプロセスとの受け渡しの場所です。ワーカーは `request.json` を読み、答えを `response.json` に書きます）

```python
 1  import json
 2  import os
 3  from pathlib import Path
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("worker")
 8  MAILBOX = Path(os.path.expanduser("~/.worker_mailbox"))
 9
10
11  def _send_request(question):
12      (MAILBOX / "request.json").write_text(json.dumps({"q": question}))
13
14
15  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
16  def ask_worker(question: str) -> str:
17      """Ask the local worker process a question."""
18      stale = MAILBOX / "response.json"
19      stale.unlink(missing_ok=True)
20      _send_request(question)
21      return "queued"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `pathlib.Path.unlink` | FS_WRITE | `fs_write` | `server.py:19` |
| D1 | `pathlib.Path.write_text` | FS_WRITE | `fs_write` | `server.py:12` |

この例では 1 行目（`unlink` の組）を判定します。2 行目は別の組です。

**問い 1: 届くか** — 本体の 19 行 `stale.unlink(missing_ok=True)` は毎回実行されます。しかし環境が変わる（ファイルが消える）のは、前の質問への応答 `response.json` が残っているときだけです。答え: **はい**。条件の種類: **`外部の状態`**（手引き 14.3 の迷いやすい書き方の 1 行目「`unlink(missing_ok=True)` → 環境が変わる場合の条件（`外部の状態`）」、D76）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行（削除も含む）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 外部の状態 |
| write_target | その他・不明 |
| target_by_arg | いいえ |
| evidence | `server.py:18-19` `(MAILBOX / "response.json").unlink(missing_ok=True)`。`MAILBOX` は `~/.worker_mailbox`。ワーカーが前の質問に書いた応答が残っていれば消す。条件: 前の呼び出しへの応答 `response.json` が受け渡しの場所に残っているとき。 |
| note | 不明: 別のプロセスとの受け渡しファイルのうち、前の呼び出しが残した応答ファイルの削除。手引き 16.2 の 1 行目（D76）により「その他・不明」。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: `missing_ok=True` も「毎回」ではなく、残りがあるときだけの `外部の状態` です。ラベルは、手引き 16.2 が「迷う形は既定（その他・不明）でそろえる」と先に決めた形です。v4 の M20 と同じ形です（手引き 20.2）。**違い**: 同じ呼び出しの中で作って消す受け渡しファイルなら「一時ファイル」です（16.2 の 2 行目）。また宣言が D2（`destructiveHint=False`）でも、前の呼び出しが残したファイルを消すので反します（15.2 の迷いやすい形）。

---

<a id="ai-3-8"></a>
### I-3.8 環境変数で有効になる監査ログ（宣言 D1 / 判定: 正 / 学ぶ点: `運用者の設定` と、運用者が決めた場所は中身で決める）

**コード**（作った例）

```python
 1  import os
 2  import time
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("files")
 7  AUDIT_LOG = os.environ.get("FILES_AUDIT_LOG")
 8
 9
10  def _audit(action, path):
11      if AUDIT_LOG:
12          with open(AUDIT_LOG, "a") as fh:
13              fh.write(f"{time.time():.0f} {action} {path}\n")
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def read_file(path: str) -> str:
18      """Read a text file."""
19      _audit("read", path)
20      with open(path) as fh:
21          return fh.read()
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:12` |

**問い 1: 届くか** — 本体の 19 行 `_audit("read", path)` → 11 行 `if AUDIT_LOG:` → 12 行 `open(AUDIT_LOG, "a")`。`AUDIT_LOG` は 7 行で環境変数 `FILES_AUDIT_LOG` から読みます。既定は `None` で、書きません。運用者がこの環境変数を設定して起動すれば、毎回届きます。答え: **はい**。条件の種類: **`運用者の設定`**（手引き 14.3「環境変数・設定ファイル・起動の引数で有効になる」）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 運用者の設定 |
| write_target | ログ |
| target_by_arg | いいえ |
| evidence | `server.py:19 → server.py:11`（`if AUDIT_LOG:`）`→ server.py:12` `open(AUDIT_LOG, "a")`。`AUDIT_LOG` は 7 行で環境変数 `FILES_AUDIT_LOG` から読む。時刻・操作・パスの 1 行を追記する。条件: 環境変数 `FILES_AUDIT_LOG` にパスを設定して起動したとき。 |
| note | target_by_arg: 書き先は運用者の環境変数で決まる。引数 `path` は追記する行の中身と、読むファイル（20 行）を決めるだけ。 |

**数え方**: (A) 数える・(B) **数えない**・(C) 数えない。

**この例で学ぶこと**: 書く場所を運用者が決めたことだけでは「利用者のファイル」にしません。中身（「いつ・何をした」の行）で「ログ」です（手引き 16.2「運用者が環境変数で決めた場所への書き込み → 中身で決める」、D76）。**違い**: `os.environ.get("FILES_AUDIT_LOG", "~/.files_audit.log")` のように既定値があれば、運用者が何もしなくても届きます。そのときは `運用者の設定` を書かず、ほかに条件が無ければ `なし` です（14.3「既定では起きるが、設定で止められる」と同じ考え）。

---

<a id="ai-3-9"></a>
### I-3.9 既定で有効なキャッシュ、置き場所は環境変数（宣言 D1 / 判定: 正 / 学ぶ点: 止められる設定は書かない・鍵が引数のキャッシュは `引数`）

**コード**（作った例）

```python
 1  import hashlib
 2  import os
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("fetch")
 8  CACHE_DIR = os.environ.get("FETCH_CACHE_DIR", os.path.expanduser("~/.cache/fetchmcp"))
 9  NO_CACHE = os.environ.get("FETCH_NO_CACHE") == "1"
10  os.makedirs(CACHE_DIR, exist_ok=True)
11
12
13  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
14  def fetch_page(url: str) -> str:
15      """Fetch a web page (cached on disk)."""
16      path = os.path.join(CACHE_DIR, hashlib.sha256(url.encode()).hexdigest())
17      if not NO_CACHE and os.path.exists(path):
18          with open(path) as fh:
19              return fh.read()
20      text = requests.get(url, timeout=10).text
21      if not NO_CACHE:
22          with open(path, "w") as fh:
23              fh.write(text)
24      return text
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:22` |

**問い 1: 届くか** — 本体の 16 行で、引数 `url` のハッシュからキャッシュのパスを作ります。17 行で、そのファイルがあれば読んで返します（書きません）。無ければ 20 行で取得し、21 行 `if not NO_CACHE:` → 22 行 `open(path, "w")` で書きます。答え: **はい**。条件は 2 つあります。

1. 「その `url` のキャッシュが無いとき」: 鍵が引数のキャッシュです。`引数` とも `初回` とも読めるので、表の上の方の **`引数`** を 1 つだけ書きます（手引き 14.3 の最後の段落、D76）。
2. `if not NO_CACHE:`: 既定では書き、運用者が `FETCH_NO_CACHE=1` で止められるだけです。**`運用者の設定` を書きません**（手引き 14.3「既定では起きるが、設定で止められる → `運用者の設定` を書かない」、D76）。

10 行の `os.makedirs` はモジュールの読み込み時に走るので、ツールの道筋ではありません（手引き 14.4。解析器もこの行を組に出していません）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 引数 |
| write_target | キャッシュ・状態の保存 |
| target_by_arg | はい |
| evidence | `server.py:16`（`url` からパスを作る）→ `server.py:17`（キャッシュがあれば返す）→ `server.py:21-22` `open(path, "w")`。既定（`FETCH_NO_CACHE` 未設定）で書く。18 行で同じツールが読み返す。条件: 引数 `url` のページがまだキャッシュに無いとき。 |
| note | `FETCH_NO_CACHE` は止めるための設定なので条件に書かない（14.3、D76）。置き場所 `FETCH_CACHE_DIR` は運用者が決めるが、ラベルは中身で決める（16.2、D76）。target_by_arg: ファイル名を引数 `url` のハッシュが決める（一部でも決めるので `はい`）。ハッシュの 16 進の名前なので、`CACHE_DIR` の外には出られない。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: 運用者の設定が出てくるたびに `運用者の設定` を書くのではありません。**設定しないと届かない**ときだけ書きます。**違い**: `if os.environ.get("FETCH_CACHE") == "1":` のように既定で無効なら、届くには運用者の設定が要るので `引数;運用者の設定` と並べ、(B) から外れます。

---

<a id="ai-3-10"></a>
### I-3.10 `main()` の中だけで初期化する DB（宣言 D1 / 判定: 正 / 学ぶ点: `起動の方法` だけを書き、`初回` を重ねない）

**コード**（作った例）

```python
 1  import sqlite3
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("bookmarks")
 6  _conn = None
 7
 8
 9  def _init_db():
10      conn = sqlite3.connect("bookmarks.db")
11      conn.execute("CREATE TABLE IF NOT EXISTS bookmarks (url TEXT PRIMARY KEY, title TEXT)")
12      return conn
13
14
15  def _db():
16      global _conn
17      if _conn is None:
18          _conn = _init_db()
19      return _conn
20
21
22  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
23  def list_bookmarks() -> list[tuple]:
24      """List bookmarks."""
25      return _db().execute("SELECT url, title FROM bookmarks").fetchall()
26
27
28  def main():
29      _db()
30      mcp.run()
31
32
33  if __name__ == "__main__":
34      main()
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | DB | `db_modify` | `server.py:11` |

**問い 1: 届くか** — 本体の 25 行 `_db()` → 17 行 `if _conn is None:` → 18 行 `_init_db()` → 11 行 `CREATE TABLE IF NOT EXISTS`（道筋 `_db -> _init_db`）。29 行の `main()` が先に `_db()` を呼ぶので、`python server.py` で起動すれば初期化は受付の前に済みます。しかし `fastmcp run server.py:mcp` のように `main()` を通らずに起動すると、最初のツール呼び出しで 11 行が走ります。`lifespan=` は無く、`_conn` を `None` に戻す行もありません（ファイルを検索して確かめる）。答え: **はい**（手引き 14.4 の表の 1 行目「`main()` の中だけ → 到達する」）。条件の種類: **`起動の方法`**。

この効果は最初の呼び出しでだけ起きますが、`初回` は重ねません（手引き 14.3 の最後の段落「`起動の方法` の位置の効果が最初の呼び出しでだけ起きるときは、`初回` を重ねずに `起動の方法` だけを書く」、D76）。`初回` だけを書くと、運用者が決める条件が落ちて (B) に誤って残ります。だから `起動の方法` を書きます。`IF NOT EXISTS` の「表が無いときだけ」も、同じく重ねません。

**問い 2: 宣言に反するか** — 手引き 15.1 の「DB のデータ・スキーマの変更（`CREATE` …）→ 反する」。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 起動の方法 |
| write_target | データベース |
| target_by_arg | いいえ |
| evidence | `server.py:25 → server.py:17`（`if _conn is None:`）`→ server.py:18 → server.py:11` `CREATE TABLE IF NOT EXISTS bookmarks`。初期化は `main()`（29 行）の中だけで、`lifespan` は無い。条件: `main()` を通らない起動（`fastmcp run server.py:mcp` など）で、最初のツール呼び出しのとき。 |
| note | site は `psycopg.Cursor.execute` と出るが、実際は sqlite3 の接続。kind（DB）は合っている。10 行の `sqlite3.connect` が無いファイルを作る効果は解析器の行に無く、この組の判定には入れない（それ自体は手引き 15.1 の迷いやすい形により D1 に反する）。 |

**数え方**: (A) 数える・(B) **数えない**・(C) 数えない。

**この例で学ぶこと**: `main()` の中だけの初期化は「到達する」で、条件は `起動の方法` です（手引き 14.4、D67 の 2）。**違い**: `FastMCP("bookmarks", lifespan=app_lifespan)` の lifespan の中で `_db()` を済ませるなら、どの起動でも受付の前に済むので到達しません（誤、E1）。逆に、`main()` での先回りが無ければ、ただの `初回` です。

---

<a id="ai-3-11"></a>
### I-3.11 「または」でつながる条件（宣言 D1 / 判定: 正 / 学ぶ点: 一番弱い道の条件だけを書く）

**コード**（作った例）

```python
 1  import json
 2  import os
 3  import time
 4  import httpx
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("status")
 9  TRACE_FILE = os.path.expanduser("~/.statusmcp/trace.jsonl")
10  os.makedirs(os.path.dirname(TRACE_FILE), exist_ok=True)
11
12
13  def _trace(event):
14      with open(TRACE_FILE, "a") as fh:
15          fh.write(json.dumps({"t": time.time(), **event}) + "\n")
16
17
18  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
19  def service_status(service: str, trace: bool = False) -> str:
20      """Return the status of a local service."""
21      r = httpx.get(f"http://127.0.0.1:9000/status/{service}")
22      if trace or os.environ.get("STATUS_TRACE"):
23          _trace({"service": service, "code": r.status_code})
24      return r.text
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:14` |

**問い 1: 届くか** — 本体の 22 行 `if trace or os.environ.get("STATUS_TRACE"):` → 23 行 `_trace(...)` → 14 行 `open(TRACE_FILE, "a")`。届く道は 2 つあります。モデルが `trace=True` を渡す道（`引数`）と、運用者が `STATUS_TRACE` を設定する道（`運用者の設定`）です。答え: **はい**。条件の種類: **`引数`**（手引き 14.3 の迷いやすい書き方「「または」でつながる条件 → 一番弱い道の条件だけ（手順 G の順）」、D76）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。21 行の `httpx.get` は `GET` で、反しません（解析器も組に出していません）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 引数 |
| write_target | ログ |
| target_by_arg | いいえ |
| evidence | `server.py:22`（`if trace or os.environ.get("STATUS_TRACE"):`）`→ server.py:23 → server.py:14` `open(TRACE_FILE, "a")`。時刻つきの 1 行を `~/.statusmcp/trace.jsonl` に追記する。読み返さない。条件: 引数 `trace=True` を渡したとき（または環境変数 `STATUS_TRACE` を設定したとき）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: 「または」は、弱い方の道だけで届きます。両方を `;` で並べると、運用者の設定が入って (B) から**誤って**外れます（決定シート 2 (d) の推奨の理由）。`evidence` の条件の文には両方の道を書いてかまいませんが、`condition_type` は 1 つです。**違い**: 「かつ」なら全部を並べます（次の例）。

---

<a id="ai-3-12"></a>
### I-3.12 「かつ」で重なる条件（宣言 D1 / 判定: 正 / 学ぶ点: `;` で並べ、1 つでも運用者の条件があれば (B) から外す）

**コード**（作った例）

```python
 1  import csv
 2  import os
 3  import sqlite3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("crm")
 8  EXPORT_ENABLED = os.environ.get("CRM_ALLOW_EXPORT") == "1"
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def find_customers(city: str, export_path: str = "") -> list[tuple]:
13      """Find customers in a city. Optionally export them as CSV."""
14      conn = sqlite3.connect("crm.db")
15      rows = conn.execute("SELECT name, email FROM customers WHERE city = ?", (city,)).fetchall()
16      if export_path and EXPORT_ENABLED:
17          with open(export_path, "w", newline="") as fh:
18              csv.writer(fh).writerows(rows)
19      return rows
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:17` |

**問い 1: 届くか** — 本体の 16 行 `if export_path and EXPORT_ENABLED:` → 17 行 `open(export_path, "w", newline="")`。`EXPORT_ENABLED` は 8 行で環境変数 `CRM_ALLOW_EXPORT` から読みます。モデルが `export_path` を渡し、**かつ**運用者が `CRM_ALLOW_EXPORT=1` で起動したときだけ届きます。答え: **はい**。条件の種類: **`引数;運用者の設定`**（手引き 14.3「条件が重なるとき…は全部を `;` で並べる」と、迷いやすい書き方の最後の行、D76）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 引数;運用者の設定 |
| write_target | 利用者のファイル |
| target_by_arg | はい |
| evidence | `server.py:8`（`EXPORT_ENABLED` を環境変数から読む）、`server.py:16`（`export_path and EXPORT_ENABLED`）`→ server.py:17` `open(export_path, "w")`。`export_path` はモデルが決める引数で、顧客の一覧を CSV で書き出す。条件: 引数 `export_path` を渡し、かつ環境変数 `CRM_ALLOW_EXPORT=1` で起動したとき。 |

**数え方**: (A) 数える・(B) **数えない**・(C) 数えない。

**この例で学ぶこと**: 条件の並べ方で (B) が変わります。「かつ」に運用者の設定が 1 つでも入れば (B) から外れます（手引き 14.3「1 つでも運用者が決める条件があれば (B) に数えない」）。ラベルは、運用者の設定があっても、書き先がモデルの指定した場所なので「利用者のファイル」です。**違い**: `export_path or EXPORT_ENABLED` なら、前の例と同じく `引数` だけです。

---

<a id="ai-3-13"></a>
### I-3.13 失敗で先に抜けるのは条件ではない（宣言 D1 / 判定: 正 / 学ぶ点: 前提の崩れは条件に数えない・履歴でも DB は「データベース」）

**コード**（作った例）

```python
 1  import os
 2  import sqlite3
 3  import time
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("library")
 8  DB_PATH = os.path.expanduser("~/.library/library.db")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def search_books(query: str) -> list[tuple]:
13      """Search books by title."""
14      if not query.strip():
15          return []
16      if not os.path.exists(DB_PATH):
17          raise RuntimeError("library database not found; run setup first")
18      conn = sqlite3.connect(DB_PATH)
19      rows = conn.execute("SELECT title, author FROM books WHERE title LIKE ?", (f"%{query}%",)).fetchall()
20      conn.execute("INSERT INTO search_history (query, at) VALUES (?, ?)", (query, time.time()))
21      conn.commit()
22      return rows
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | DB | `db_modify` | `server.py:20` |

**問い 1: 届くか** — 本体の 14〜15 行で、空の検索語なら空の一覧を返します。16〜17 行で、DB が無ければ例外で抜けます。どちらも抜けなければ、20 行で `INSERT INTO search_history` を実行します。答え: **はい**。条件の種類: **`なし`**（手引き 14.3 の迷いやすい書き方「空の入力・失敗・前提の崩れ（表が無い、認証が通らない）で、効果の前に抜ける → 条件に数えない（ほかに条件が無ければ `なし`）」、D76）。

**問い 2: 宣言に反するか** — 手引き 15.1 の「DB のデータ・スキーマの変更（`INSERT` …）→ 反する」。19 行の `SELECT` は読み取りです。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | なし |
| write_target | データベース |
| target_by_arg | いいえ |
| evidence | `server.py:14-17`（空の入力と DB が無いときは先に抜ける）`→ server.py:20` `INSERT INTO search_history (query, at)`。検索のたびに検索語と時刻の行を足す。 |
| note | site は `psycopg.Cursor.execute` と出るが sqlite3。kind（DB）は合っている。target_by_arg: DB のファイルと表 `search_history` は定数。引数 `query` は足す行の中身を決めるだけ（表紙の「決めていない点」13）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: 失敗や前提の崩れまで条件にすると、ほとんどの効果が条件つきになり、(C) が意味を失います（決定シート 1 (b) の推奨の理由）。また、検索の履歴は「いつ・何をした」の記録ですが、DB の行を足すので順 2 の「データベース」が順 4 の「ログ」より先です。**違い**: 16〜17 行が「DB が無ければ作る」なら、その作成の効果は `初回` です（抜けるのではなく、環境が変わる側の条件だから）。

---

<a id="ai-3-14"></a>
### I-3.14 相手の応答しだいで既読にする（宣言 D1 / 判定: 正 / 学ぶ点: 相手が返す値は `外部の状態`・ラベル「相手側の状態」）

**コード**（作った例）

```python
 1  import requests
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("tracker")
 6  API = "https://tracker.example.com/api/v2"
 7
 8
 9  def _mark_read(issue_id):
10      requests.patch(f"{API}/issues/{issue_id}", json={"unread": False}, timeout=10)
11
12
13  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
14  def get_issue(issue_id: int) -> dict:
15      """Get one issue from the tracker."""
16      issue = requests.get(f"{API}/issues/{issue_id}", timeout=10).json()
17      if issue.get("unread"):
18          _mark_read(issue_id)
19      return issue
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.patch` | NET | `net_modify` | `server.py:10` |

**問い 1: 届くか** — 本体の 16 行で課題を `GET` し、17 行 `if issue.get("unread"):` が真なら、18 行 `_mark_read(issue_id)` → 10 行 `requests.patch(...)`。`unread` は相手のサーバが返す値です。モデルは `issue_id` を選べますが、どの課題が未読かは相手の状態で決まり、引数の値で起こせるものではありません（まだ使っていない鍵を渡せば必ず起きる、鍵が引数のキャッシュ（[I-3.9](#ai-3-9)）とはここが違います）。答え: **はい**。条件の種類: **`外部の状態`**（手引き 14.3「相手が特定の応答を返したとき」）。

**問い 2: 宣言に反するか** — 手引き 15.1 の「HTTP の `PUT` / `PATCH` / `DELETE` → 反する（原理 1-ii-b）」。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 外部の状態 |
| write_target | 相手側の状態 |
| target_by_arg | はい |
| evidence | `server.py:16`（課題を `GET`）`→ server.py:17`（`unread` が真なら）`→ server.py:18 → server.py:10` `requests.patch(f"{API}/issues/{issue_id}", json={"unread": False})`。相手のサーバで課題を既読に変える。条件: 相手のサーバが課題を未読（`unread` が真）と返したとき。 |
| note | target_by_arg: 引数 `issue_id`（int）が `PATCH` する課題 `/issues/{issue_id}` を決める。ホストは定数。 |

**数え方**: (A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: NET の効果で相手のサーバの状態を変えるので、ラベルは順 1 の「相手側の状態」です。**違い**: 既読にするかを引数 `mark_read` で選ぶなら `引数` です。また送るのが `POST` なら、解析器は矛ではなく不（`net_post`）を出し、人は相手の API の意味で決めます（15.1 の `POST` の行。不の中身の手順は手引き 18A）。

---

<a id="ai-3-15"></a>
### I-3.15 モデルが選ぶリンターを起動する（宣言 D1 / 判定: 正 / 学ぶ点: SPAWN の正は常に「プロセスの起動・コードの実行」）

**コード**（作った例）

```python
 1  import subprocess
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("lint")
 6
 7
 8  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
 9  def lint(path: str, linter: str = "ruff") -> str:
10      """Run a linter on a file and return its report."""
11      proc = subprocess.run([linter, "check", "--fix", path], capture_output=True, text=True)
12      return proc.stdout + proc.stderr
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | SPAWN | `spawn_model` | `server.py:11` |

**問い 1: 届くか** — 本体の 11 行で毎回 `subprocess.run([linter, "check", "--fix", path])` を起動します。`linter` の既定値は `"ruff"` で、引数を渡さなくても起動します。答え: **はい**。条件の種類: **`なし`**。

**問い 2: 宣言に反するか** — 手引き 15.1 の `SPAWN` の行「起動するコマンドをモデルが決められるなら反する」。起動するプログラム（`argv[0]`）が引数 `linter` で、モデルが選べます（原理 3-a）。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | なし |
| write_target | プロセスの起動・コードの実行 |
| target_by_arg | はい |
| evidence | `server.py:11` `subprocess.run([linter, "check", "--fix", path])`。起動するプログラム `linter` はモデルが決める引数（既定 `"ruff"`）。 |
| note | 既定の `ruff check --fix` は `path` のファイルを書き換えるが、ラベルは子の動作で変えない（16.2、D76）。 |

**数え方**: (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: 子が利用者のファイルを書き換えると分かっていても、ラベルは「プロセスの起動・コードの実行」です（手引き 16.2「SPAWN / EXEC の正で、子が何を変えるか分かるとき → 常にこの種類」、D76）。**違い**: コマンドが定数（`["ruff", "check", "--fix", path]`）なら、解析器は矛ではなく不（`spawn_command`）を出します。そのときは不の中身の手順（手引き 18A）で、コマンドが実際に何をするかを調べます（15.1 の `SPAWN` の行。`--fix` があるので環境を変える）。

---

<a id="ai-3-16"></a>
### I-3.16 同じ呼び出しで作って消す一時ファイル（宣言 D1 / 判定: 正 / 学ぶ点: D1 では反する・ラベル「一時ファイル」）

**コード**（作った例）

```python
 1  import os
 2  import subprocess
 3  import tempfile
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("diagram")
 8
 9
10  def _render(source):
11      fd, src = tempfile.mkstemp(suffix=".dot")
12      with os.fdopen(fd, "w") as fh:
13          fh.write(source)
14      try:
15          out = subprocess.run(["dot", "-Tsvg", src], capture_output=True, text=True, check=True)
16          return out.stdout
17      finally:
18          os.remove(src)
19
20
21  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
22  def render_graph(dot_source: str) -> str:
23      """Render Graphviz source to SVG text."""
24      return _render(dot_source)
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `os.remove` | FS_WRITE | `fs_write` | `server.py:18` |

解析器は同じツールに、`subprocess.run`（15 行）× D1 の**不**（理由 `spawn_command`）も出しています。別の組なので、ここでは扱いません。

**問い 1: 届くか** — 本体の 24 行 `_render(dot_source)` → 11 行 `tempfile.mkstemp` でファイルを作り、12〜13 行で書き、18 行の `finally` で `os.remove(src)` を実行します。`finally` なので、`dot` が失敗しても消します。答え: **はい**。条件の種類: **`なし`**（手引き 14.5「同じ呼び出しの中で作って消すもの → 到達はする」）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。「同じ呼び出しの中で作って消す一時ファイルは、原理の文書 §7.1 の「FS_WRITE（すべて。新規作成を含む）→ 矛（決定済み）」による」とあります。答え: **はい**。

**判定と記録**

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | なし |
| write_target | 一時ファイル |
| target_by_arg | いいえ |
| evidence | `server.py:24 → server.py:11`（`tempfile.mkstemp` で作る）`→ server.py:18` `os.remove(src)`（`finally` の中で毎回消す）。 |
| note | 解析器の語彙に `tempfile.mkstemp`・`os.fdopen` は無く（`authgap/catalog/` を検索して確かめた）、作成と書き込みは行に出ない。この組（`os.remove`）の判定には関係しない。 |

**数え方**: (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: ラベルは手引き 16.1 の順 5 の定義「同じ呼び出しの中で作って消す」そのものです。v4 の M58 と同じ形です（手引き 20.2）。**違い**: 宣言が D2（`destructiveHint=False`）なら、消したのは呼び出しの前からあったものではないので反しません（誤、E2。手引き 15.2 の迷いやすい形）。同じ削除が D1 では正、D2 では誤です。

---

<a id="ai-3-17"></a>
### I-3.17 位置が 2 つ: 最初の正で止める（宣言 D1 / 判定: 正 / 学ぶ点: 止めてよい・ラベルは最初の正の位置・(B)(C) は下限）

**コード**（作った例）

```python
 1  import json
 2  import os
 3  import time
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("recipes")
 8  RECIPES = os.path.expanduser("~/recipes.json")
 9  HISTORY = os.path.expanduser("~/.recipes_history.log")
10
11
12  def _export(hits, export_path):
13      with open(export_path, "w") as fh:
14          json.dump(hits, fh, ensure_ascii=False)
15
16
17  def _remember(query):
18      with open(HISTORY, "a") as fh:
19          fh.write(f"{time.time():.0f} {query}\n")
20
21
22  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
23  def find_recipes(query: str, export_path: str = "") -> list[dict]:
24      """Find recipes whose name contains the query."""
25      with open(RECIPES) as fh:
26          hits = [r for r in json.load(fh) if query in r["name"]]
27      if export_path:
28          _export(hits, export_path)
29      _remember(query)
30      return hits
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:13 server.py:18` |

同じツール・同じ site・同じ kind の効果が 2 か所にあるので、1 つの組に 2 つの位置が並びます（手引き 11.1）。

**問い 1: 届くか** — `locations` の並びの順に読みます。

- **1 つ目 `server.py:13`**: 本体の 27 行 `if export_path:` → 28 行 `_export(...)` → 13 行 `open(export_path, "w")`。モデルが `export_path` を渡せば届きます。到達する、条件は `引数`。15.1 の `FS_WRITE` の行で反する。**ここで正と分かりました。**
- 手引き 手順 G「条件つきの位置で正が見つかったときも、そこで止めてよい（止めたことを `note` に書く。D76）」により、ここで止めます。

答え: **はい**。条件の種類: **`引数`**（読んだ位置のうち一番弱いもの）。

**問い 2: 宣言に反するか** — 手引き 15.1 の `FS_WRITE` の行。答え: **はい**。

**判定と記録**（1 つ目で止めたとき）

| 欄 | 値 |
|---|---|
| verdict | 正 |
| condition_type | 引数 |
| write_target | 利用者のファイル |
| target_by_arg | はい |
| evidence | `server.py:27`（`if export_path:`）`→ server.py:28 → server.py:13` `open(export_path, "w")`。`export_path` はモデルが決める引数で、検索結果を書き出す。条件: 引数 `export_path` を渡したとき。 |
| note | `server.py:13` で正と分かり、止めた（手順 G、D76）。`server.py:18` は読んでいない。 |

**もし 2 つ目も読んでいたら**: `server.py:18` は、本体の 29 行 `_remember(query)` から毎回届く `open(HISTORY, "a")` で、条件は `なし`、反します。正にできる位置のうち一番弱い条件は `なし` なので、`condition_type` は **`なし`** になります。ラベルは、最初に正と分かった位置（`server.py:13`）の **利用者のファイル** のままです（手順 G・16.1、D76）。`target_by_arg` も、本書は同じく最初に正と分かった位置（13 行。書き先は引数 `export_path`）で **`はい`** と書きます。18 行の書き先 `HISTORY` は定数なので、位置ごとに答えが違う形です。どの位置で書くかは D84 も手引きも決めていません（表紙の「決めていない点」12）。

| 読み方 | `condition_type` | `write_target` | (A) | (B) | (C) |
|---|---|---|---|---|---|
| 1 つ目で止めた | 引数 | 利用者のファイル | 数える | 数える | **数えない** |
| 2 つとも読んだ | なし | 利用者のファイル | 数える | 数える | **数える** |

**数え方**: 止めたので、(A) 数える・(B) 数える・(C) 数えない。

**この例で学ぶこと**: 止めると速くなる代わりに、(C) を少なく数えることがあります。だから報告では (B)(C) を**下限**と書きます（手順 G、D76）。主の数 (A) は変わりません。**違い**: 誤にするときは止められません。全部の位置を読み、全部が「到達しない」か「反しない」と確かめます（手順 G）。また、`server.py:18` を先に読んでいたら、ラベルは「ログ」になります。どの位置で正と分かったかを `note` に書くのは、このためです。

---

<a id="ai-3-18"></a>
### I-3.18 D3 の通信先の種類 3 つ（宣言 D3 / 判定: 正 / 学ぶ点: D3 では書き込み先の代わりに通信先の種類）

**コード**（作った例。3 つのツールが、それぞれ 1 組になります）

```python
 1  import subprocess
 2  import httpx
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("devhelper")
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
11  def latest_release(repo: str) -> str:
12      """Latest release tag of a GitHub repo."""
13      r = requests.get(f"https://api.github.com/repos/{repo}/releases/latest", timeout=10)
14      return r.json().get("tag_name", "")
15
16
17  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
18  def fetch_text(url: str) -> str:
19      """Fetch a URL and return its text."""
20      return httpx.get(url, timeout=10).text
21
22
23  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
24  def run_shell(command: str) -> str:
25      """Run a shell command in the project directory."""
26      return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
```

**判定表の行**（解析器の出力。本書の試験）

| unit | decl | site | kind | reasons | locations |
|---|---|---|---|---|---|
| `latest_release` | D3 | `requests.get` | NET | `net_external_host` | `server.py:13` |
| `fetch_text` | D3 | `httpx.get` | NET | `net_model_host` | `server.py:20` |
| `run_shell` | D3 | `subprocess.run` | SPAWN | `spawn_model` | `server.py:26` |

**問い 1: 届くか** — 3 つとも本体の 1 行で、毎回実行されます。答え: **はい**。条件の種類: **`なし`**（3 組とも）。

**問い 2: 宣言に反するか** — 手引き 15.3 の表で、

- `latest_release`: 宛先 `api.github.com` はコードに書かれた外部のホスト（local の範囲に入らない）→「宛先が定数の外部ホスト → 反する」。`repo` はパスの一部で、ホストは変えられません。
- `fetch_text`: 宛先 `url` はツールの引数 →「宛先をモデルが決められる → 反する（原理 3-a）」。
- `run_shell`: `shell=True` で、文字列 `command` をモデルが決める →「実行するコード・起動するコマンドをモデルが決められる → 反する」。

答え: 3 組とも **はい**。

**判定と記録**

| 欄 | `latest_release` | `fetch_text` | `run_shell` |
|---|---|---|---|
| verdict | 正 | 正 | 正 |
| condition_type | なし | なし | なし |
| write_target | 定数の外部ホスト | モデルが決める宛先 | モデルが決めるコード・コマンド |
| evidence | `server.py:13` `requests.get("https://api.github.com/repos/{repo}/releases/latest")`。ホストは定数の外部。 | `server.py:20` `httpx.get(url)`。`url` はモデルが決める引数。 | `server.py:26` `subprocess.run(command, shell=True)`。`command` はモデルが決める引数。 |

**数え方**: 3 組とも (A) 数える・(B) 数える・(C) 数える。

**この例で学ぶこと**: D3 の正には、`write_target` 欄に通信先の種類（手引き 16.3）を書きます。書き込み先の 8 種類は使いません（手引き 16 の前書き）。**違い**: 宛先が `http://ollama:11434` のようなドットの無い名前なら local で、反しません。解析器はこれを外部として矛を出すので、判定は誤です（手引き 15.3。誤の原因は語彙・定義の差）。宛先が環境変数で決まり、既定値が外部なら、人の判定では 15.3 の「宛先が運用者の設定で決まる」の行で反し、通信先の種類は「その他・不明」です（16.3 の例）。

---

<a id="ai-3-sum"></a>
### この分冊の 20 組をまとめて数えると

I-3.1〜I-3.18 の組は、I-3.18 が 3 組なので 20 組です（I-3.5・I-3.7 の 2 行目の組は数えない）。全部が正です。

| 数 | 数え方 | 正の数 |
|---|---|---|
| (A) | 条件を問わない | 20 |
| (B) | 運用者が決める条件のある正（I-3.8・I-3.10・I-3.12）を除く | 17 |
| (C) | 条件 `なし` の正だけ（I-3.1・3.3・3.13・3.15・3.16・3.18 の 3 組） | 8 |

I-3.17 で 2 つ目まで読んでいれば (C) は 9 です。**止めた分だけ (C) は少なく出ます。** これが「(B)(C) は下限」の意味です。(A) は、条件の種類をどう書いても変わりません。

---

<a id="ai-3-x"></a>
### I-3.x この分冊の例の一覧

| 番号 | 題 | 宣言 | 判定 | `condition_type` | `write_target` | 学ぶ点 |
|---|---|---|---|---|---|---|
| [I-3.1](#ai-3-1) | 毎回届くログの追記 | D1 | 正 | なし | ログ | 条件なしとログの基準点 |
| [I-3.2](#ai-3-2) | 引数を渡したときだけ書き出す | D1 | 正 | 引数 | 利用者のファイル | 引数は (B) に残り (C) から外れる |
| [I-3.3](#ai-3-3) | 引数の既定値で毎回起きる | D1 | 正 | なし | ログ | 既定値で起きるものは `なし`（D76） |
| [I-3.4](#ai-3-4) | `exist_ok=True` の作業ディレクトリ | D1 | 正 | 初回 | キャッシュ・状態の保存 | 毎回実行される行でも `初回`（D76） |
| [I-3.5](#ai-3-5) | 初回だけ作る索引を `/tmp` に置く | D1 | 正 | 初回 | 一時ファイル | 読み返しても場所で一時ファイル（D76） |
| [I-3.6](#ai-3-6) | トークンの期限切れで保存し直す | D1 | 正 | 失敗・期限切れ | キャッシュ・状態の保存 | トークンの保存 |
| [I-3.7](#ai-3-7) | 前の呼び出しの残りを消す | D1 | 正 | 外部の状態 | その他・不明 | `missing_ok=True` と 16.2 の境目（D76） |
| [I-3.8](#ai-3-8) | 環境変数で有効になる監査ログ | D1 | 正 | 運用者の設定 | ログ | 運用者が決めた場所は中身で決める（D76） |
| [I-3.9](#ai-3-9) | 既定で有効なキャッシュ | D1 | 正 | 引数 | キャッシュ・状態の保存 | 止められる設定は書かない・鍵が引数なら `引数`（D76） |
| [I-3.10](#ai-3-10) | `main()` の中だけで初期化する DB | D1 | 正 | 起動の方法 | データベース | `初回` を重ねない（D76） |
| [I-3.11](#ai-3-11) | 「または」でつながる条件 | D1 | 正 | 引数 | ログ | 一番弱い道だけ（D76） |
| [I-3.12](#ai-3-12) | 「かつ」で重なる条件 | D1 | 正 | 引数;運用者の設定 | 利用者のファイル | `;` で並べ (B) から外す |
| [I-3.13](#ai-3-13) | 失敗で先に抜けるのは条件ではない | D1 | 正 | なし | データベース | 前提の崩れは条件にしない（D76）・順 2 が順 4 より先 |
| [I-3.14](#ai-3-14) | 相手の応答しだいで既読にする | D1 | 正 | 外部の状態 | 相手側の状態 | 相手が返す値・順 1 |
| [I-3.15](#ai-3-15) | モデルが選ぶリンターを起動する | D1 | 正 | なし | プロセスの起動・コードの実行 | SPAWN の正は常にこの種類（D76） |
| [I-3.16](#ai-3-16) | 同じ呼び出しで作って消す一時ファイル | D1 | 正 | なし | 一時ファイル | D1 では正、D2 なら誤 E2 |
| [I-3.17](#ai-3-17) | 位置が 2 つ: 最初の正で止める | D1 | 正 | 引数 | 利用者のファイル | 止めてよい・(B)(C) は下限（D76） |
| [I-3.18](#ai-3-18) | D3 の通信先の種類 3 つ | D3 | 正（3 組） | なし | 定数の外部ホスト / モデルが決める宛先 / モデルが決めるコード・コマンド | D3 は通信先の種類 |

---

<a id="ai-3-y"></a>
### I-3.y 自分で判定してみる

8 問です。どれも作った例で、判定表の行は凍結版の解析器の本物の出力です。各問で、`verdict`・`condition_type`・`write_target`（D1 の正なので `target_by_arg` も。D84）と、(A)(B)(C) のどれに数えるかを答えてください。答えは開いて確かめます。

<a id="ai-3-y1"></a>
#### 問 1

```python
 1  import os
 2  import time
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("glossary")
 7  HISTORY = os.path.expanduser("~/.glossary_history")
 8  TERMS = {"mcp": "Model Context Protocol", "sdk": "software development kit"}
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def define(term: str) -> str:
13      """Look up a term in the glossary."""
14      if not os.environ.get("GLOSSARY_NO_HISTORY"):
15          with open(HISTORY, "a") as fh:
16              fh.write(f"{time.time():.0f} define {term}\n")
17      return TERMS.get(term.lower(), "unknown term")
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:15` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`なし`**、`write_target` は **ログ**、`target_by_arg` は **`いいえ`**（書き先は定数の `~/.glossary_history`。引数 term は書く行の中身だけ）。(A)(B)(C) すべてに数える。
- 14 行の `if not os.environ.get("GLOSSARY_NO_HISTORY"):` は、既定では真です。運用者が何もしなければ毎回書くので、`運用者の設定` を書きません（手引き 14.3「既定では起きるが、設定で止められる」、D76）。ほかに条件は無いので `なし` です。
- 15 行の追記は時刻と操作の記録で、`define` は読み返しません → ログ（16.2、D76）。
- evidence: `server.py:14`（既定で真）`→ server.py:15` `open(HISTORY, "a")`。
- [I-3.8](#ai-3-8)（既定で無効 → `運用者の設定`）と比べてください。

</details>

<a id="ai-3-y2"></a>
#### 問 2

```python
 1  import json
 2  import os
 3  from pathlib import Path
 4  import requests
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("weather")
 9  CACHE = Path(os.path.expanduser("~/.cache/weathermcp"))
10  CACHE.mkdir(parents=True, exist_ok=True)
11
12
13  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
14  def forecast(city: str) -> dict:
15      """Weather forecast for a city (cached)."""
16      p = CACHE / f"{city.lower()}.json"
17      if p.exists():
18          return json.loads(p.read_text())
19      data = requests.get("https://weather.example.com/v1/forecast", params={"q": city}, timeout=10).json()
20      p.write_text(json.dumps(data))
21      return data
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `pathlib.Path.write_text` | FS_WRITE | `fs_write` | `server.py:20` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`引数`**、`write_target` は **キャッシュ・状態の保存**、`target_by_arg` は **`はい`**（書き先のファイル名を引数 `city` が決める。`city` に `../` を含めるか `/` で始めれば `~/.cache/weathermcp` の外にも書けることを `note` に書く）。(A)(B) に数え、(C) には数えない。
- 書くのは、引数 `city` のキャッシュがまだ無いときです（17〜18 行であれば返す）。鍵が引数のキャッシュの「無いとき」は `引数` とも `初回` とも読めるので、表の上の **`引数`** を 1 つだけ書きます（手引き 14.3、D76）。
- `~/.cache/` は OS の一時領域ではありません。18 行で同じツールが読み返すので、順 6 です。
- 10 行の `mkdir` はモジュールの読み込み時なので、ツールの道筋ではありません（解析器も組に出していません）。
- evidence: `server.py:16`（`city` からパスを作る）`→ server.py:17`（あれば返す）`→ server.py:20` `p.write_text(...)`。

</details>

<a id="ai-3-y3"></a>
#### 問 3

```python
 1  import json
 2  import os
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("theme")
 7  SETTINGS = os.path.expanduser("~/.thememcp/settings.json")
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
11  def preview_theme(theme: str, dry_run: bool = True) -> str:
12      """Preview a color theme. Set dry_run=False to apply it."""
13      with open(SETTINGS) as fh:
14          settings = json.load(fh)
15      before = settings.get("theme")
16      if not dry_run:
17          settings["theme"] = theme
18          with open(SETTINGS, "w") as fh:
19              json.dump(settings, fh)
20      return f"{before} -> {theme}"
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:18` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`引数`**、`write_target` は **キャッシュ・状態の保存**、`target_by_arg` は **`いいえ`**（書き先は定数の `~/.thememcp/settings.json`。引数 theme は書く中身、dry_run は書くかどうかを決めるだけ）。(A)(B) に数え、(C) には数えない。
- `dry_run` の既定値は `True` で、既定では書きません。モデルが `dry_run=False` を渡したときだけ 18 行に届きます → `引数`。[I-3.3](#ai-3-3)（既定値で起きる → `なし`）の裏返しです。
- 書き先はツール自身の設定ファイル（`~/.thememcp/settings.json`）です。利用者やモデルが指定した場所でも、利用者の文書でもないので、順 3 には当たりません。ツールの動作のために保存し、13 行で同じツールが読み返すので、順 6 の定義に当たります。
- evidence: `server.py:16`（`if not dry_run:`）`→ server.py:18` `open(SETTINGS, "w")`。

</details>

<a id="ai-3-y4"></a>
#### 問 4

```python
 1  import os
 2  import sqlite3
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("geo")
 8  CACHE_DB = os.path.expanduser("~/.cache/geomcp.db")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def geocode(address: str) -> dict:
13      """Geocode an address."""
14      data = requests.get("https://geo.example.com/v1/search", params={"q": address}, timeout=10).json()
15      conn = sqlite3.connect(CACHE_DB)
16      conn.execute("INSERT OR REPLACE INTO geocache (address, lat, lon) VALUES (?, ?, ?)",
17                   (address, data["lat"], data["lon"]))
18      conn.commit()
19      return data
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | DB | `db_modify` | `server.py:16` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`なし`**、`write_target` は **データベース**、`target_by_arg` は **`決められない`**。(A)(B)(C) すべてに数える。
- `target_by_arg`: DB のファイル `~/.cache/geomcp.db` と表 `geocache` は定数です。`INSERT OR REPLACE` がどの既存の行を置き換えるかは表の一意の鍵で決まりますが、表を作る文（スキーマ）が木にありません。`address` が鍵なら、置き換える行を引数が選ぶので `はい`、鍵でなければ新しい行を足すだけで `いいえ` です。`note` にこのことを書きます（表紙の「決めていない点」13）。
- 16 行の `INSERT OR REPLACE` は毎回実行され、毎回 DB の行を足すか置き換えます。D1 では 15.1 の「DB のデータ…の変更（`INSERT` …）→ 反する」です（15 の前書きの表の `INSERT OR REPLACE` の行は D2 の話です）。
- 名前はキャッシュですが、SQLite に書くので順 2 のデータベースが順 6 より先です（16.2「SQLite のキャッシュ DB への書き込み → データベース」）。
- site は `psycopg` と出ますが sqlite3 です。kind は合っています（`note` に書く）。
- evidence: `server.py:15 → server.py:16` `INSERT OR REPLACE INTO geocache`。

</details>

<a id="ai-3-y5"></a>
#### 問 5

```python
 1  import os
 2  import sqlite3
 3  import time
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("auth")
 8  DB = "auth.db"
 9
10  if os.environ.get("AUTH_ENABLE_ADMIN_TOOLS") == "1":
11
12      @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13      def session_stats() -> dict:
14          """Count active sessions."""
15          conn = sqlite3.connect(DB)
16          conn.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
17          conn.commit()
18          n = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
19          return {"active": n}
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `psycopg.Cursor.execute` | DB | `db_modify` | `server.py:16` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`運用者の設定`**、`evidence` に入れる条件は「環境変数 `AUTH_ENABLE_ADMIN_TOOLS=1` で起動したとき」、`write_target` は **データベース**、`target_by_arg` は **`いいえ`**（消す行は `expires_at` と時刻で決まり、ツールに引数は無い）。(A) だけに数え、(B)(C) には数えない。
- 16 行の `DELETE` はツールの中では毎回実行されますが、ツールの登録そのもの（10 行の `if` の中の `@mcp.tool`）が設定しだいです → `運用者の設定`（手引き 14.3「ツールの登録そのものが設定しだい」、D76）。
- `DELETE` は 15.1 の「DB のデータ…の変更」で反します。
- evidence: `server.py:10`（登録は環境変数しだい）、`server.py:16` `DELETE FROM sessions WHERE expires_at < ?`。

</details>

<a id="ai-3-y6"></a>
#### 問 6

```python
 1  import subprocess
 2  from mcp.server.fastmcp import FastMCP
 3  from mcp.types import ToolAnnotations
 4
 5  mcp = FastMCP("convert")
 6
 7
 8  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
 9  def word_count(path: str, post_cmd: str = "") -> int:
10      """Count words in a text file. post_cmd runs afterwards if given."""
11      with open(path) as fh:
12          n = len(fh.read().split())
13      if post_cmd:
14          subprocess.run(post_cmd, shell=True, check=False)
15      return n
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | SPAWN | `spawn_model` | `server.py:14` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`引数`**、`write_target` は **プロセスの起動・コードの実行**、`target_by_arg` は **`はい`**（起動するコマンドを引数 post_cmd が丸ごと決める）。(A)(B) に数え、(C) には数えない。
- 13 行 `if post_cmd:` → モデルが空でないコマンドを渡したときだけ起動します → `引数`。
- `shell=True` で、文字列をモデルが決めるので、15.1 の `SPAWN` の行で反します。子が何をするかに関係なく、ラベルは常にこの種類です（16.2、D76）。
- evidence: `server.py:13`（`if post_cmd:`）`→ server.py:14` `subprocess.run(post_cmd, shell=True)`。

</details>

<a id="ai-3-y7"></a>
#### 問 7

```python
 1  import difflib
 2  import os
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("watch")
 8  SNAP = "/tmp/watchmcp_latest.html"
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def page_changes() -> str:
13      """Show what changed on the status page since the last check."""
14      new = requests.get("https://status.example.com/", timeout=10).text
15      old = ""
16      if os.path.exists(SNAP):
17          with open(SNAP) as fh:
18              old = fh.read()
19      with open(SNAP, "w") as fh:
20          fh.write(new)
21      return "\n".join(difflib.unified_diff(old.splitlines(), new.splitlines()))
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:19` |

<details><summary>答え</summary>

- **正**。`condition_type` は **`なし`**、`write_target` は **一時ファイル**、`target_by_arg` は **`いいえ`**（書き先は定数の `/tmp/watchmcp_latest.html`。ツールに引数は無い）。(A)(B)(C) すべてに数える。
- 16 行の `if` は読み取り（17 行）の枝で、19 行の書き込みは毎回実行されます → `なし`。
- 書き先は `/tmp` の下です。次の呼び出しで読み返しますが、OS の一時領域に置くので場所で決め、一時ファイルです（16.2、D76。[I-3.5](#ai-3-5) と同じ境目）。
- evidence: `server.py:19` `open(SNAP, "w")`。`SNAP` は `/tmp/watchmcp_latest.html`。毎回上書きし、次の呼び出しで 17 行が読み返す。

</details>

<a id="ai-3-y8"></a>
#### 問 8

```python
 1  import json
 2  import os
 3  import time
 4  import requests
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("drive")
 9  AUTH_MODE = os.environ.get("DRIVE_AUTH", "apikey")
10  TOKEN_FILE = os.path.expanduser("~/.drivemcp/oauth.json")
11  API = "https://drive.example.com/v3"
12
13
14  def _headers():
15      if AUTH_MODE != "oauth":
16          return {"X-Api-Key": os.environ["DRIVE_API_KEY"]}
17      with open(TOKEN_FILE) as fh:
18          tok = json.load(fh)
19      if tok["expires_at"] < time.time():
20          tok = requests.post(f"{API}/token", data={"refresh_token": tok["refresh_token"]}).json()
21          with open(TOKEN_FILE, "w") as fh:
22              json.dump(tok, fh)
23      return {"Authorization": f"Bearer {tok['access_token']}"}
24
25
26  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
27  def list_files(folder: str) -> list[dict]:
28      """List files in a folder."""
29      return requests.get(f"{API}/files", params={"folder": folder}, headers=_headers(), timeout=10).json()
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `builtins.open` | FS_WRITE | `fs_write` | `server.py:21` |

（解析器は同じツールに `requests.post`（20 行）× D1 の不 `net_post` も出しています。別の組です。）

<details><summary>答え</summary>

- **正**。`condition_type` は **`運用者の設定;失敗・期限切れ`**、`write_target` は **キャッシュ・状態の保存**、`target_by_arg` は **`いいえ`**（書き先は定数の `~/.drivemcp/oauth.json`。引数 folder は 29 行の `GET` の中身だけ）。(A) だけに数え、(B)(C) には数えない。
- 15 行は、認証の方式が `oauth` でなければ先に返します。これは失敗や前提の崩れではなく、運用者が `DRIVE_AUTH` で選ぶ設定です。そのうえで 19 行の期限切れが重なるので、「かつ」で全部を並べます（手引き 14.3 の最後の行、v4 の R04 と同じ形、D76）。
- OAuth のトークンをファイルに保存し、17 行で読み返します → キャッシュ・状態の保存（16.2）。
- evidence: `server.py:29 → server.py:15`（`DRIVE_AUTH` が `oauth` のとき進む）`→ server.py:19`（期限切れ）`→ server.py:21` `open(TOKEN_FILE, "w")`。
- [I-3.6](#ai-3-6)（認証の方式の設定が無い → `失敗・期限切れ` だけ）と比べてください。

</details>

---

[← 前](appendix-i-2.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md) ｜ [次 →](appendix-i-4.md)
