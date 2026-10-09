# 6. 例題: 1 件を最初から最後まで

この章は、`02_steps.md` の段 0〜11 を、**この手順書のために作った架空のサーバ**で通してやってみせるものです。実在の木ではなく、
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

**段 0**: 木の窓を開き、読み込みを待った（`t_setup` = 1）。ワークシートを写した。止めるかの方針は「止めない」とする。

**段 1**: 時計を動かした（`t_start` = 14:05）。`roster_form` は `decorator` → 段 2 では `def` の上のデコレータを見る。

**段 2**: `:42` の `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))` が `:43` の `search_notes` を登録。`mcp` は `:13` の
`FastMCP("notes")`。対象外ではない。本体は `notes_server.py:43-48`。`search_notes` という名前の関数はほかに無い。

**段 3**:

- 引数: `query: str`（モデル）、`save_history: bool = False`（モデル、既定は偽）。フレームワークが入れる引数は無い。
- デコレータは `@mcp.tool(...)`（ライブラリ）だけ。`FastMCP("notes")` に middleware は無い。
- docstring の「Read-only」は根拠にしない。
- `:45-46` 空の検索語なら抜ける → 条件に数えない（14.3）。
- 呼ぶもの: `log.info`（`:47`。木の外の `logging`）、`_search`（`:48`。木の中 → 深さ 1）、`json.dumps`（木の外、環境を変えない）。

**段 4**（ワークシートの D 節）:

| 深さ | 関数 | ファイル:行の範囲 | どこから呼ばれるか | 呼ばれる条件 | 環境を変えうる行 |
|---|---|---|---|---|---|
| 0 | `search_notes` | `notes_server.py:43-48` | （本体） | | `:47` `log.info` |
| 1 | `_search` | `:34-39` | `:48` | 空でない検索語 | |
| 2 | `NotesClient.__init__` | `:19-21` | `:35`（構築） | | `:21` `httpx.Client(...)` |
| 2 | `NotesClient.search` | `:23-26` | `:36`（受け手は `:35` の `NotesClient`） | | `:24` `GET` |
| 2 | `_remember_query` | `:29-31` | `:38` | `:37` `save_history` が真 | `:30-31` `open(..., "a")`・`write` |

深さ 3 の木の中の関数は無い（`httpx`・`json`・`time`・`os.path` は木の外）。

**段 5**: ログの設定を `FileHandler|basicConfig|logger\.add|dictConfig` で検索 → `:10` の `basicConfig(level=logging.INFO)` だけ（ファイルの
指定が無いので標準エラー）。モジュールの一番上の `:15` の `os.makedirs` も候補に入れる（届くかは段 6）。

**段 6**（ワークシートの F 節）:

| # | ファイル:行 | 何をするか | 深さ | 届くか | `condition_type` | `condition` | D1 に反するか | `write_target` |
|---|---|---|---|---|---|---|---|---|
| 1 | `:15` | `os.makedirs(STATE_DIR, exist_ok=True)` | — | 届かない（モジュールの読み込み時。14.4） | | | — | |
| 2 | `:21` | `httpx.Client(timeout=10)` の構築 | 2 | 届く | `なし` | | 反しない（接続の準備だけ） | |
| 3 | `:24` | `GET {base_url}/api/notes` | 2 | 届く | `なし` | | 反しない（15.1 の GET の行） | |
| 4 | `:30-31` | `~/.notes_mcp/history.jsonl` に時刻と検索語を 1 行追記 | 2 | 届く | `引数` | 引数 save_history に真を渡したとき（既定は False） | **反する**（15.1 のファイルの行） | `ログ` |
| 5 | `:47` | `log.info` | 0 | 届く | `なし` | | 反しない（`:10` の設定で標準エラー。15.1） | |

#4 の書き込み先の種類: 16.1 を上から当てる。相手側の状態（通信ではない）→ いいえ。データベース → いいえ。利用者のファイル（利用者や
モデルが指定した場所・利用者の文書）→ いいえ（場所はサーバが決めた `~/.notes_mcp`）。ログ（記録のためだけに書き、ツールの動作では
読み返さない）→ **はい**（「いつ・何をした」を書く行で、`search_notes` の道筋に読み返す行は無い。16.2 の「読み返さない記録」）。

**段 7**: 深さ 4 の中に反する動作 #4 がある → `違反`。反する動作は 1 つなので、ラベルは #4 から。止めても止めなくても同じ。

**段 8**: 20 分より前に決まった（メモなし）。

**段 9**: 表に写し、`evidence` の行（`:30`）を開き直した。ラップ 23 分 → `t_noai` = 23。

**段 10**: しない。

**段 11**: 時計を止めた（`t_end` = 14:31、休憩 3 分 → `t_break` = 3）。`minutes` = 23。手引きの 16.2 を読み返した 2 分 → `t_guide` = 2。
確かめの道具で「よい」。

## 6.3 EX-1 の表の行

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `write_target` | `ログ` |
| `condition_type` | `引数` |
| `condition` | 引数 save_history に真を渡したとき（既定は False） |
| `depth` | `2` |
| `unknown_reason` | （空） |
| `evidence` | 登録: notes_server.py:42 の宣言で :13 の FastMCP("notes") に search_notes を登録／道筋: notes_server.py:43-48 search_notes（深さ 0。:48 で _search(query, save_history)）→ :34-39 _search（深さ 1。条件: :37 save_history が真）→ :29-31 _remember_query（深さ 2）:30 open(STATE_DIR/history.jsonl, "a") で時刻と検索語を 1 行追記（STATE_DIR は :14 の ~/.notes_mcp）。このツールは history.jsonl を読み返さない／読んだ範囲: notes_server.py:1-48（深さ 0〜2。NotesClient.__init__ :19-21・search :23-26 は深さ 2）／確かめたこと: HTTP は :24 の GET だけ。ログの設定は :10 の basicConfig(level=INFO) だけで標準エラー（FileHandler\|basicConfig\|logger\.add\|dictConfig をファイル全体で検索）。:15 の makedirs はモジュールの読み込み時で届かない（14.4） |
| `ai_found` | （空） |
| `note` | （空） |
| `minutes` | `23` |
| `ai_used` | `なし` |
| `ai_model`・`ai_log` | （空） |
| `stopped_early` | `いいえ` |
| `t_start` / `t_end` | `14:05` / `14:31` |
| `t_break` / `t_noai` / `t_ai` / `t_guide` / `t_setup` | `3` / `23` / `0` / `2` / `1` |

（`evidence` の中の `\|` は、この表の中で `|` を表すための書き方です。表計算のソフトには `|` だけを書きます。）

## 6.4 EX-2（`list_tags`）の表の行（短く）

本体 `:52-55`（深さ 0）が `NotesClient(...)`（`:54` → `__init__` `:19-21`、深さ 1）と `client.search("tag:*")`（`:55` → `:23-26`、深さ 1）を
呼ぶ。環境を変えうるのは `:24` の `GET` だけ → `違反でない`。

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `evidence` | 登録: notes_server.py:51 の宣言で :13 の FastMCP("notes") に list_tags を登録／読んだ範囲: notes_server.py:52-55（深さ 0）、:19-21 NotesClient.__init__（深さ 1、:54 の構築）、:23-26 NotesClient.search（深さ 1、:55）／反しない理由: HTTP は :24 の GET だけ（15.1 の GET の行）。書き込み・DB・プロセスの起動は無い／確かめたこと: このツールはログを出さない。ログの設定は :10 で標準エラー。:15 の makedirs はモジュールの読み込み時で届かない（14.4） |
| `stopped_early` | `違反なし` |
| ラベルの 4 欄・`unknown_reason` | （空） |

## 6.5 例題を少し変えると（答えがどう変わるか）

| 変えたところ | 答え | 理由 |
|---|---|---|
| `:15` の `os.makedirs` を `_remember_query` の最初に移す | `違反`。**止めずに読めば**、`makedirs` は `引数;初回`（「かつ」）で `引数` より強いので選ばず、ラベルは追記（`ログ`・`引数`）のまま。**最初の違反で止めるなら**、先に確定する `makedirs` のラベル（`キャッシュ・状態の保存`・`引数;初回`。16.2 の「初回だけ `~/.app/` を作る」）になる | 14.3（`exist_ok=True` は `初回`）。段 7 の 2・3 |
| `save_history: bool = True`（既定を真） | `違反`、`condition_type` = `なし`、`condition` は空 | 引数の既定値で効果が起きる → `なし`（14.3） |
| `:10` を `logging.basicConfig(filename="notes.log")` | `違反`。止めずに読めば、条件の一番弱い `:47` のログ（`なし`、深さ 0、`ログ`）がラベルになる | ログの出力先がファイル（18.3・15.1）。段 7 の 2 |
| `:24` を `self._http.post(f"{self.base_url}/api/notes/search", json={"q": q})` | API の意味しだい。相手の文書で検索（照会）なら反しない、文書が無く名前「search」がはっきり照会を示すなら「API 名から」反しない、決められなければ `不明`（`相手の API`） | 15.1 の POST の行（D86） |
| `if save_history:` を `if os.environ.get("NOTES_SAVE"):` | `違反`、`condition_type` = `運用者の設定`、`condition` = 環境変数 NOTES_SAVE を設定したとき | 14.3（環境変数で有効になる） |
| `:42` の宣言を削り、`READ_ONLY = {"readOnlyHint": True}` を `docs_examples.py` に置くだけ（どこにも登録しない） | `対象外` | ツールの宣言ではない（D85） |
