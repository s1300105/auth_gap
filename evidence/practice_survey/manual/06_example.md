# 6. 例題: 1 件を最初から最後まで

この章は、`02_steps.md` の段 0〜9 を、**この手順書のために作った架空のサーバ**で通してやってみせるものです。実在の木ではなく、
練習の件（W-01・T-01〜T-03）とも関係ありません。答えを確かめてあるので、手順の流れと記録の書き方を覚えるのに使ってください
（読むのに 15〜20 分）。

## 6.1 コード

木 `ex-notes`、ファイル `notes_server.py`（左の数字は行番号）:

```
 1  import json
 2  import logging
 3  import os
 4  import time
 5
 6  import httpx
 7  from mcp.server.fastmcp import FastMCP
 8  from mcp.types import ToolAnnotations
 9
10  logging.basicConfig(level=logging.INFO)
11  log = logging.getLogger(__name__)
12
13  mcp = FastMCP("notes")
14  STATE_DIR = os.path.expanduser("~/.notes_mcp")
15  os.makedirs(STATE_DIR, exist_ok=True)
16
17
18  class NotesClient:
19      def __init__(self, base_url):
20          self.base_url = base_url
21          self._http = httpx.Client(timeout=10)
22
23      def search(self, q):
24          r = self._http.get(f"{self.base_url}/api/notes", params={"q": q})
25          r.raise_for_status()
26          return r.json()
27
28
29  def _remember_query(q):
30      with open(os.path.join(STATE_DIR, "history.jsonl"), "a") as fh:
31          fh.write(json.dumps({"at": time.time(), "query": q}) + "\n")
32
33
34  def _search(q, save_history):
35      client = NotesClient(os.environ.get("NOTES_URL", "http://localhost:8080"))
36      hits = client.search(q)
37      if save_history:
38          _remember_query(q)
39      return hits
40
41
42  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
43  def search_notes(query: str, save_history: bool = False) -> str:
44      """Search the notes service. Read-only."""
45      if not query.strip():
46          return "empty query"
47      log.info("search %s", query)
48      return json.dumps(_search(query, save_history))
49
50
51  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
52  def list_tags() -> str:
53      """List tags."""
54      client = NotesClient(os.environ.get("NOTES_URL", "http://localhost:8080"))
55      return json.dumps(client.search("tag:*"))
56
57
58  if __name__ == "__main__":
59      mcp.run()
```

名簿（`scripts/survey_roster.py` をこの木に当てた結果。2026-10-09 に確かめた）:

| `pair_id` | `tool` | `roster_form` | `roster_relpath` | `roster_lineno` | `decl_lineno` |
|---|---|---|---|---|---|
| EX-1 | `search_notes` | `decorator` | `notes_server.py` | 43 | 42 |
| EX-2 | `list_tags` | `decorator` | `notes_server.py` | 52 | 51 |

## 6.2 EX-1（`search_notes`）を段ごとに

段 0〜8 は頭の中で考えるだけで、何も書きません。表に書くのは段 9 の `outcome` と `evidence` だけです（D90）。

**段 0**: 表の行を開き、木の窓を開いて読み込みを待った。

**段 1**: 名簿の値は表の行で読む。`roster_form` は `decorator` → 段 2 では `def` の上のデコレータを見る。

**段 2**: 宣言の行 `notes_server.py:42` を開いて `readOnlyHint=True` を確かめた。`:42` の `@mcp.tool(...)` が `:43` の `search_notes` を
登録し、`mcp` は `:13` の `FastMCP("notes")`。対象外ではない。本体は `notes_server.py:43-48`。`search_notes` という名前の関数はほかに
無い。

**段 3**:

- 引数: `query: str`、`save_history: bool = False`（どちらもモデルが決める値。既定は偽）。枠組みが入れる引数は無い。
- 自前のデコレータ: なし（デコレータは `@mcp.tool(...)`（ライブラリ）だけ）。middleware: なし（`FastMCP("notes")` に渡していない）。
- docstring の「Read-only」は根拠にしない。
- `:45-46` 空の検索語なら抜ける（それ以外の道では先へ進むので、後ろの動作は届く）。
- 呼ぶもの: `_search`（`:48`。木の中 → 深さ 1）。木の外の `log.info`（`:47`。`logging`。ログを出すので反しうる行の候補）と
  `json.dumps`（`:48`。環境を変えない）。

**段 4**: 読む順に、深さ 1 = `_search`（`:34-39`）。深さ 2 = `NotesClient.__init__`（`:19-21`、`:35` の構築）、`NotesClient.search`
（`:23-26`、`:36`。受け手は `:35` の `NotesClient`）、`_remember_query`（`:29-31`、`:38`。`:37` の `if save_history:` の中）。深さ 3 の
木の中の関数は無い（`httpx`・`json`・`time`・`os.path` は木の外）。深さ 2 の `:21` の `httpx.Client(timeout=10)`、`:24` の
`self._http.get`、`:30-31` の `open(..., "a")`・`fh.write` は反しうる行の候補。

**段 5**: 候補は、読む順に `:47` の `log.info`（深さ 0）、`:21` の構築・`:24` の GET・`:30-31` の追記（深さ 2）と、モジュールの一番上の
`:15` の `os.makedirs`。`:47` のロガーへの出力は、読む順で `:30-31` より前にあるので、止める前にログの出力先を確かめる（段 5 の 3）。
段 5 の 3 の 6 語の正規表現で木全体に検索した → 当たりは `:10` の `basicConfig(level=logging.INFO)` だけ（このサーバの起動で走る。
ファイルの指定が無いので標準エラー）。

**段 6**（# は候補の番号。読む順は #5 → #2 → #3 → #4）:

| # | ファイル:行と何をするか | 深さ | 届くか | D1 に反するか |
|---|---|---|---|---|
| 1 | `:15` `os.makedirs(STATE_DIR, exist_ok=True)` | — | 届かない（モジュールの読み込み時。14.4） | — |
| 2 | `:21` `httpx.Client(timeout=10)` の構築 | 2 | 届く | 反しない（接続の準備だけ） |
| 3 | `:24` `GET {base_url}/api/notes` | 2 | 届く | 反しない（15.1 の GET の行） |
| 4 | `:30-31` `~/.notes_mcp/history.jsonl` に時刻と検索語を 1 行追記 | 2 | 届く（`:37` `save_history` が真のとき） | **反する**（15.1 のファイルの行） |
| 5 | `:47` `log.info` | 0 | 届く（`:45-46` の空の検索語で先に抜けるのは数えない。14.3） | 反しない（`:10` の設定で標準エラー。15.1） |

（この表は説明のためのもので、判定では書かない。前の版はここで #4 に条件の種類と書き込み先の種類を付けていたが、D90 で
記録しないので決めない。）

**段 7**: 読む順で #5・#2・#3 は反しないと決まり、#4 が届いて反すると決まった → ここで止める（D88。`_remember_query` は読む最後の
関数なので、止めても読む範囲は変わらない）。`違反`。

**段 8**: 20 分より前に決まった。

**段 9**: 表の行の `outcome` と `evidence` を 1 回で書いた（6.3）。`evidence` は道筋だけ。`evidence` の行（`:30`）を開き直した。
保存して確かめの道具にかけ、「よい」。

## 6.3 EX-1 の表の行

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `evidence` | notes_server.py:43 search_notes → notes_server.py:34 _search → notes_server.py:29 _remember_query → notes_server.py:30: open(~/.notes_mcp/history.jsonl, "a") に時刻と検索語を追記 |

## 6.4 EX-2（`list_tags`）の表の行（短く）

本体 `:52-55`（深さ 0）が `NotesClient(...)`（`:54` → `__init__` `:19-21`、深さ 1）と `client.search("tag:*")`（`:55` → `:23-26`、深さ 1）を
呼ぶ。環境を変えうるのは `:24` の `GET` だけで、ログの設定は `:10` で標準エラー → `違反でない`。

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `evidence` | notes_server.py:52 list_tags → notes_server.py:19 NotesClient.__init__ → httpx.Client（外）／notes_server.py:52 list_tags → notes_server.py:23 NotesClient.search → httpx.Client.get（外） |

## 6.5 例題を少し変えると（答えがどう変わるか）

| 変えたところ | 答え | 理由 |
|---|---|---|
| `:15` の `os.makedirs` を `_remember_query` の最初に移す | `違反`。同じ関数の中で先の行の `makedirs` が先に確定するので、そこで止める（同じ深さでは呼ばれる行の順に読む【O48 (4)】）。道筋は `makedirs` の行まで | 15.1 のファイルの行。段 7 の 3 |
| `save_history: bool = True`（既定を真） | `違反` | 引数の既定値のままで書き込みに届く（14.1） |
| `:10` を `logging.basicConfig(filename="notes.log", level=logging.INFO)` | `違反`。浅い深さから読むので、最初に反すると決まるのは `:47` のログ（道筋は `notes_server.py:47 log.info: notes.log に追記`） | ログの出力先がファイル（18.3・15.1）。段 7 の 3 |
| `:24` を `self._http.post(f"{self.base_url}/api/notes/search", json={"q": q})` | **`違反` のまま**（`:30-31` の追記は変わらず届いて反する。違反 ＞ 不明）。POST の意味で変わるのは止める位置だけ: 作成・更新なら `:24` で止める。照会（相手の文書か、名前「search」がはっきり照会を示すなら「API 名から」）か、決められないなら `:30` まで読んで止める | 15.1 の POST の行（D86 の 15）。段 7 の 1・3 |
| `:24` を `/api/notes/sync` への POST に変え、さらに `:37-38`（`save_history` の追記）を消す | POST の意味で答えが決まる: 相手の文書で照会なら `違反でない`、作成・更新なら `違反`、文書が無く名前の `sync` でも決まらなければ `不明` | 15.1 の POST の行。段 7 の 1 |
| `if save_history:` を `if os.environ.get("NOTES_SAVE"):` | `違反` | 環境変数を設定すれば届く（14.1・14.3） |
| `:42` の宣言を削り、`READ_ONLY = {"readOnlyHint": True}` を `docs_examples.py` に置くだけ（どこにも登録しない） | `対象外` | ツールの宣言ではない（D85） |