[← 前](appendix-i-3.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md)

---

# 付録 I-4 不明になる例と、不の中身の判定 — 決められないものを決められないと書く

<a id="ai-4-0"></a>
## この分冊で学ぶこと

この分冊の答えは**本書の答え（本記録者の判定）**です。正解ではありません。最終評価の判定は、学生が手引きで行います。

この分冊は 2 つの群に分かれます。

- **第 1 群（I-4.1〜I-4.6）: 決められない形。** 解析器が矛を出した組、または何も出さなかったツールのうち、人が読んでも
  「到達するか」か「宣言に反するか」が決まらない形です。手引き 19 節の「不明」と、その理由の類を学びます。
  I-4.4 は、難しそうに見えて**1 ファイル読めば決まる**形です。不明にしてはいけない例として、I-4.3 と並べて置きます。
- **第 2 群（I-4.7〜I-4.16）: 不の中身を決める。** 解析器が「不」（静的に決まらない）を出した組を、手引き 18A 節の手順で
  「違反 / 違反でない / 不明」に決めます。中心は HTTP の `POST`（`net_post`）と、定数のコマンドの起動（`spawn_command`）です。
  どちらも手引き 15.1 の表が「調べて決める」と書いている行です。

使う手引きの節は次のとおりです（手引き = `docs/drafts/final_judging_guide_draft.md`、D76 を反映し、D83・D84・D86 を足した版）。

| 節 | 中身 | この分冊で使う例 |
|---|---|---|
| 手引き 13（手順 A〜H） | 矛の 1 組の判定と記録の欄 | I-4.1・I-4.5 |
| 手引き 18.2〜18.4 | 見落としの判定（出力を見る前にコードを読む）と、`不明（打ち切り）` | I-4.2・I-4.3・I-4.4・I-4.6 |
| 手引き 18A | 不の中身の判定（違反 / 違反でない / 不明） | I-4.7〜I-4.16 |
| 手引き 15.1 の `POST` の行と `SPAWN` の行 | 相手の API の意味・コマンドの動作を調べて決める | I-4.7〜I-4.15 |
| 手引き 19 | 不明にするとき・20〜30 分・理由の類 | 全部 |
| 手引き 21 の 6 | AI は事実を調べる補助としてだけ使う | I-4.7・I-4.11 |

**記録の欄**: 矛の組（I-4.1・I-4.5 と問 5・問 7）は手引き 手順 H の D83 の形で、判定ごとに必要な欄だけを書きます（正は `verdict`・
`evidence`・`write_target`・`condition_type`、誤は `verdict`・`evidence`・`error_class`、不明は `verdict`・`evidence`・`unknown_reason`。
`reachable`・`violates`・`condition` は書かない）。D1 の正には `target_by_arg` も書きます（D84）が、この分冊に D1 の矛の正の例はありません。
不の中身（18A.3）の表には `reachable`・`violates`・`condition` が残り、`target_by_arg` は書きません。見落とし（18.4）の表にも書きません。

教科書の本文では、[第 52 章](ch52.md)（見落とし・不の中身・不明）、[第 50 章](ch50.md)（15.1 の迷いやすい形）、
[第 48 章](ch48.md)（手順 A〜H）が同じ範囲です。手引きの文を 1 行ずつ追う読み本は[付録 H-6](appendix-h-6.md)・
[付録 H-7](appendix-h-7.md)・[付録 H-8](appendix-h-8.md) です。ただし付録 H は D76 の前の下書きを引いています。
食い違うときは手引きの今の文に従います。

**本書の試験**: 例はすべて作った例です（v4 の実例は使っていません）。小さな木を作り、凍結版の解析器（タグ
`analyzer-freeze-3`。走らせる前に `git diff analyzer-freeze-3 -- authgap/` が空であることを確かめた）で
`python -m authgap scan <木>` を走らせました。「判定表の行」は、その manifest の行の注記
`contradiction_reason:<宣言>:<理由>`（矛）と `contradiction_unknown:<宣言>:<理由>`（不）から、本物の出力をそのまま写したものです。
組の矛 / 不の決め方は `scripts/contradiction_by_decl.py` と同じです（同じ宣言に矛の注記が 1 つでもあれば矛）。

<a id="ai-4-00"></a>
## 先に押さえる 4 つの約束

### 1. 不明は失敗ではない。ただし、調べれば分かるものを不明にしない

手引き 19 節の書き出しの 2 文です。

> 不明は失敗ではない。**分からないものを黙って正や誤に倒さないこと**が、この研究の約束である（CLAUDE.md 規則 4）。
> ただし、調べれば分かるものを不明にしない。目安として、**20〜30 分調べても決められなければ不明**にし、理由を書く。

20〜30 分は `minutes` と同じ測り方で数えます。手順 A を始めてから記録を書き終えるまでの時計の時間です。休憩は除き、
AI に聞いた時間は含めます（手引き 12.3）。この分冊の記録の例に書いた `minutes` は**記入の例**です。

### 2. 「確かめた」と言えるのは、公式の文書かソースを自分で開けたときだけ

ライブラリの動作や API の意味のような、行ではない事実の基準です（手引き 19、D76）。

- 公式の文書かソースを**自分で開けた**ときだけ、確かめたとします。開いた URL かパスを `evidence` に書きます。
- **手元で動かして確かめたものは、確かめたことにしません。**
- 名前（`refresh-stock.sh`・`/sync`）から推しただけのものも、確かめたことになりません。
- ただ 1 つの例外は `POST` の意味です（D86 の 15）。API 名が作成・更新・削除（または照会）を**はっきり示す**ときだけ、名前で決めて
  よく、`evidence` に「API 名から」と書きます（件数を報告する）。`/sync` のように 2 通りに読める名前は、この例外に入りません（I-4.11）。

調べる範囲も節で違います。

| 判定の種類 | 木の外のライブラリのソース |
|---|---|
| 矛（手順 A〜H）・不の中身（18A） | 20〜30 分の中なら、入れて読んでよい（手引き 18A.2 の 3、19） |
| 見落とし（18.2） | 読まない（手引き 18.2 の 2、19） |

### 3. 不明の理由の類は固定で、1 件に 1 つ

`unknown_reason` の先頭に次の類を 1 つ書き、そのあとに説明を書きます（手引き 19、D76）。

| 類 | 中身 | この分冊の例 |
|---|---|---|
| 外の値 | 書き先・宛先・コマンドが、木の外のライブラリの戻り値や実行時の外部の状態で決まり、読み切れない | I-4.1 |
| 相手の API | `POST` の先の意味が、文書にもコードにも無い | I-4.11・問 8 |
| 起動・初期化 | 起動の方法・初期化の場所が読み切れない（手引き 14.4） | （この分冊では扱わない） |
| 動的な呼び出し | `getattr(obj, name)()`・プラグインの読み込み・木の外のライブラリが木の中の関数を呼び戻す形で、呼び出し先・呼ばれる時点が決まらない（呼び戻しは D86 の 7 でこの類） | I-4.2・I-4.3 |
| 打ち切り | 解析器の打ち切りが原因（18.3 の `不明（打ち切り）`） | I-4.6 |
| 手引きで決まらない | 手引き 22 節 | （この分冊では扱わない） |
| その他 | 上のどれでもない（説明を書く） | I-4.5・I-4.15 |

「その他」は逃げ道ではありません。上の典型の字義に当たらないときに使う類です。I-4.5 で、なぜ典型に当たらないかを
書きます。

### 4. AI に聞いてよいのは事実だけ

手引き 21 の 6（D70 の 3）の要点です。判定を決めるのも記録するのも判定者です。

| 聞いてよい問い（事実） | 聞かない問い（判定） |
|---|---|
| この `POST` 先の API は、作成・更新・削除・照会のどれをする？ | このツールは読み取り専用か |
| このコマンドは、ファイルを書く？ 書くならどこに？ | これは `readOnlyHint` / `destructiveHint` に反するか |
| この関数はどこから呼ばれる？ | これは正か誤か。違反か |
| この変数にはどこで何が入る？ 引数から届く？ | これは環境を変える？（宣言の問いの言い換え。D76） |

- **渡さないもの**: 宣言の値、解析器の答え（矛 / 不 / 理由コード / 判定表の行）、自分の結論。コードを貼る前に
  `annotations=…` と、宣言を述べる文（コメント・docstring）を伏せます。
- **AI に聞く前の仮の判定を `note` に書きます。**
- AI が示した資料や行は、**自分で開いたものだけ** `evidence` に書きます。AI の答えは「確かめた」ことになりません（約束 2）。
- 記録: `ai_used`（`なし` / `あり`）・`ai_model`（モデル名と版、使った画面。記憶の無い設定で使ったこと）・`ai_log`
  （`ai_logs/<会話の番号>.md`。会話ごとに 1 ファイル。中に使った件の id を書く）。

---

## 第 1 群 決められない形

この群の例は、手引き 11.2 の表の下の 2 行に当たります。

| 到達する | 宣言に反する | 判定 |
|---|---|---|
| 決められない | — | **不明** |
| はい | 決められない | **不明** |

解析器が何も出さなかったツール（I-4.2・I-4.3・I-4.4・I-4.6）は、矛の判定ではなく**見落としの判定**（手引き 18.2）で扱います。
見落としの判定表には解析器の欄が載りません（D76、D77 の 7）。この分冊では、18.2 の 4 で初めて開く解析器の出力を、
「判定表の行」の欄に分けて書きます。

<a id="ai-4-1"></a>
### I-4.1 消すファイルのパスが、ソースの無いライブラリの戻り値（宣言 D2 / 判定: 不明 / 学ぶ点: 外の値）

**コード**（作った例。`server.py`）

```python
 1  import os
 2
 3  import docrender  # 社外の描画エンジン（wheel だけで配られ、Python のソースは無い）
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("reports")
 8
 9
10  def _head_text(path: str) -> str:
11      with open(path, "rb") as fh:
12          return fh.read(4000).decode("latin-1")
13
14
15  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
16  def preview_report(report_id: str) -> str:
17      """Render a report to PDF and return its first part."""
18      pdf_path = docrender.render(report_id, fmt="pdf")
19      text = _head_text(pdf_path)
20      os.remove(pdf_path)
21      return text
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.remove` | `FS_WRITE` | `fs_remove`（矛） | `server.py:20` |

ユニットの `opaque` に `unresolved` があります（`docrender.render` を解決できていない）。

**問い 1: 届くか** — 本体の 18 行で `docrender.render` がパスを返し、19 行で読み、20 行で `os.remove` します。
本体の中で、条件はありません。答え: **はい**。条件の種類: `なし`。

**問い 2: 宣言に反するか** — 手引き 15.2 の表の「既存のものを消す（`unlink` …）」の行なら反します。ただし 15.2 の
迷いやすい形に「同じ呼び出しで自分が作った一時ファイルを消す → 反しない（誤、E2）」と「前の呼び出しが残したファイルを
消すなら反する」があります。分かれ目は、**20 行で消すファイルが、呼び出しの前からあったか**です。

それを決めるのは `docrender.render` です。

- 毎回新しいファイルを作って返すなら、同じ呼び出しで作ったものを消すので反しません（E2）。
- 描画の結果をキャッシュに置き、2 回目から同じパスを返すなら、前の呼び出しが残したファイルを消すので反します。

調べたこと（記入の例）: docrender の公式の文書（取引先の配布ページ）には「Renders the report and returns the path of the PDF.」
としか無く、ファイルの寿命も場所も書かれていません。配布物は `.so` だけで、ソースを開けません。
答え: **決められない**。

**判定と記録**（手引き 手順 H）

| 欄 | 値 |
|---|---|
| `verdict` | `不明` |
| `unknown_reason` | `外の値: 消すファイルのパスが docrender.render の戻り値。呼び出しごとに新しく作るのか、前からあるファイル（キャッシュ）を返すのかが、公式の文書に無く、ソースも無い（.so だけ）` |
| `evidence` | `server.py:18 pdf_path = docrender.render(report_id, fmt="pdf") → server.py:20 os.remove(pdf_path)。docrender の文書 <開いた URL> に戻り値のファイルの寿命の記述なし。site-packages の docrender は .so だけ`。 |
| `note` | `E2 か正かは render の動作しだい` |
| `minutes` | `25`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 「外のライブラリの戻り値」というだけでは不明になりません。**文書かソースで戻り値の性質が分かれば
決まります。** たとえば標準ライブラリの `tempfile.mkstemp` は、公式の文書に「Creates a temporary file in the most secure manner
possible.」とあり、毎回新しいファイルを作ります。`mkstemp` のパスを同じ呼び出しで消すなら、答えは**誤（E2）**に変わります
（自分で判定してみる の問 5）。

<a id="ai-4-2"></a>
### I-4.2 外の SDK が呼び戻すかもしれない保存の関数（宣言 D1 / 判定: 不明 / 学ぶ点: 呼び戻しと「動的な呼び出し」の類）

**コード**（作った例。`server.py`）

```python
 1  import json
 2  import os
 3
 4  from acmecloud import Client  # 社外の SDK（ソースは配られない）
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("acme")
 9  TOKEN_FILE = os.path.expanduser("~/.acme/token.json")
10
11
12  def _save_token(token: dict) -> None:
13      with open(TOKEN_FILE, "w") as fh:
14          json.dump(token, fh)
15
16
17  def _client() -> Client:
18      with open(TOKEN_FILE) as fh:
19          token = json.load(fh)
20      return Client(token=token, on_token_refresh=_save_token)
21
22
23  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
24  def list_buckets() -> str:
25      """List storage buckets."""
26      return "\n".join(b.name for b in _client().buckets())
```

**判定表の行**（見落としの表。D1 を明示し、D1 の矛が無いツール）

| tree | unit | decl |
|---|---|---|
| （作った木） | `list_buckets`（`server.py:24`） | D1 |

18.2 の 4 で初めて開く解析器の出力: 矛も不もありません。効果は `builtins.open` の `FS_READ`（`server.py:18`、道筋 `_client`）だけです。
`opaque` に `unresolved` があります。解析器は `on_token_refresh=_save_token` を呼び出しとは読んでいません。

**問い 1: 届くか** — 本体（深さ 0）の 26 行が `_client()`（深さ 1）を呼び、18 行で読み、20 行で `Client` を作ります。
`_save_token`（12〜14 行、`open(TOKEN_FILE, "w")`）は、**木の中のどこからも直接は呼ばれていません。** `Client` に渡しているだけです。
呼ぶかどうか、いつ呼ぶかは acmecloud の中で決まります。

- 見落としの判定では、木の外のライブラリのソースは読みません（手引き 18.2 の 2、19）。
- acmecloud の公式の文書（記入の例）は `on_token_refresh` を「callable, optional」と並べるだけで、いつ呼ぶかを書いていません。

答え: **決められない**。

**問い 2: 宣言に反するか** — 呼ばれれば、13 行はファイルの書き込みです。手引き 15.1 の `FS_WRITE` の行で反します。
到達が決まらないので、判定は問い 1 で止まります。

**判定と記録**（手引き 18.4）

| 欄 | 値 |
|---|---|
| `outcome` | `不明` |
| `cause` | （空。見落としのときだけ） |
| `depth` | （空。`_save_token` は木の中から呼ばれないので数えられない。`note` に書く） |
| `unknown_reason` | `動的な呼び出し: 木の外の SDK（acmecloud）が木の中の _save_token を呼び戻すか・いつ呼ぶかが、公式の文書に無い。見落としの判定ではライブラリのソースを読まない` |
| `output_found` | （空） |
| `evidence` | `読んだ範囲 server.py:12-26。server.py:26 → server.py:20 Client(..., on_token_refresh=_save_token)。server.py:13 open(TOKEN_FILE, "w") は呼び戻されたときだけ。acmecloud の文書 <開いた URL> に呼ぶ時期の記述なし` |
| `note` | `解析器は不も出していない`（手引き 18.2 の 5。D76） |
| `ai_found` | （空。点検しなかった） |
| `ai_used` | `なし` |

**類の選び方**: 典型 1（外の値）は書き先・宛先・コマンドの**値**が決まらない形です。典型 4（動的な呼び出し）は**呼び出し先**や
**呼ばれる時点**が決まらない形です。ここは呼び出し先（`_save_token`）も書き先（`TOKEN_FILE`）も決まっていて、**呼ばれるかどうか・
いつ呼ばれるか**が外のコードで決まります。前の版の本書は、典型 1・4 の字義のどちらにも当たらないとして「その他」にしていましたが、
D86 の 7（2026-10-07）で、木の外のライブラリが木の中の関数を呼び戻す形は**動的な呼び出し**と決まり、手引き 19 節の典型 4 に
「木の外のライブラリが木の中の関数を呼び戻す形で、呼び出し先・呼ばれる時点が決まらない（呼び戻しは D86 でこの類にした）」と
書き足されました。手引き 18.2 の 5 の表も、「木の外のライブラリが木の中の関数を呼び戻す形」を不明の例に挙げています。

**この例で学ぶこと**: 呼び戻しの時期が**公式の文書に書いてあれば**決まります。たとえば requests の hooks は、文書
（`https://requests.readthedocs.io/en/latest/user/advanced/` の Event Hooks）に「response: The response generated from a Request.」
とあり、応答のたびに呼ばれます。`requests.get(url, hooks={"response": _log})` の `_log` がファイルに追記するなら、到達し、
反するので**見落とし**になります（ライブラリのソースではなく文書で決めている点に注意）。

<a id="ai-4-3"></a>
### I-4.3 プラグインの読み込みで、呼び出し先が木の外で決まる（宣言 D1 / 判定: 不明 / 学ぶ点: 動的な呼び出し）

**コード**（作った例。`server.py` と `pyproject.toml`）

```python
 1  import os
 2  import shutil
 3  from importlib.metadata import entry_points
 4
 5  from mcp.server.fastmcp import FastMCP
 6  from mcp.types import ToolAnnotations
 7
 8  mcp = FastMCP("notekit")
 9  CACHE_DIR = os.path.expanduser("~/.notekit/cache")
10
11
12  class PruneCache:
13      """contrib の後始末（どの配布物が登録するかは木に書かれていない）"""
14
15      def run(self, note_id: str) -> str:
16          shutil.rmtree(CACHE_DIR, ignore_errors=True)
17          return "pruned"
18
19
20  class ShowNote:
21      def run(self, note_id: str) -> str:
22          with open(os.path.join(CACHE_DIR, note_id + ".md")) as fh:
23              return fh.read()
24
25
26  def _actions() -> dict:
27      return {ep.name: ep.load() for ep in entry_points(group="notekit.actions")}
28
29
30  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
31  def note_action(action: str, note_id: str) -> str:
32      """Run a note action provided by an installed plugin."""
33      plugin = _actions()[action]()
34      return plugin.run(note_id)
```

```toml
# pyproject.toml（抜粋）
[project.entry-points."notekit.actions"]
show = "server:ShowNote"
```

**判定表の行**（見落としの表）

| tree | unit | decl |
|---|---|---|
| （作った木） | `note_action`（`server.py:31`） | D1 |

18.2 の 4 で初めて開く解析器の出力: 矛も不もなく、効果も 0 です。`opaque` に `unresolved`。解析器は
`plugin.run` の呼び出し先を解決していません。

**問い 1: 届くか** — 本体（深さ 0）は 33 行で `_actions()`（深さ 1）を呼びます。`_actions` は、**入っている配布物すべて**の
`notekit.actions` の登録を読みます。34 行の `plugin.run` が何を呼ぶかは、その登録で決まります。

- この木の `pyproject.toml` が登録しているのは `show = "server:ShowNote"` だけです。`ShowNote.run`（22 行）は読み取りで、反しません。
- `PruneCache.run`（16 行の `shutil.rmtree`）は D1 に反する動作です。しかし、この木は `PruneCache` を登録していません。
  docstring は「contrib」と書き、別の配布物が登録しうることを示しています。どの配布物が入っているかは、実行時の外部の状態です。

答え: **決められない**（`PruneCache.run` に届くかが決まらない）。

**問い 2: 宣言に反するか** — 届けば、16 行は削除で反します（手引き 15.1 の `FS_WRITE`）。

**判定と記録**（手引き 18.4）

| 欄 | 値 |
|---|---|
| `outcome` | `不明` |
| `cause` | （空） |
| `depth` | （空。届けば `PruneCache.run` は深さ 1 だが、届くかが決まらない） |
| `unknown_reason` | `動的な呼び出し: plugin.run の呼び出し先は importlib.metadata の entry_points の登録で決まる。この木の pyproject.toml は show（ShowNote、読み取り）だけを登録。PruneCache（server.py:16 rmtree）を登録する配布物があるかは木に無い` |
| `evidence` | `読んだ範囲 server.py:12-34、pyproject.toml。server.py:33 → server.py:27 entry_points(group="notekit.actions") → server.py:34 plugin.run。候補 server.py:16 shutil.rmtree(CACHE_DIR)` |
| `note` | `解析器は不も出していない。登録されている ShowNote.run は読み取り` |
| `ai_used` | `なし` |

**この例で学ぶこと**: 手引き 19 の典型 4「プラグインの読み込みで、呼び出し先が決まらない」そのものです。もし `pyproject.toml` に
`prune = "server:PruneCache"` の 1 行があれば、モデルが `action="prune"` を渡すだけで届きます。答えは**見落とし**（条件の種類
`引数`）に変わります。次の I-4.4 は、この「1 行を読めば決まる」側の例です。

<a id="ai-4-4"></a>
### I-4.4 動的に見えるが、表がもう 1 つのファイルに書いてある（宣言 D1 / 判定: 見落とし / 学ぶ点: 決められるものを不明にしない）

**コード**（作った例。`server.py` と `actions.py`）

```python
# server.py
 1  from mcp.server.fastmcp import FastMCP
 2  from mcp.types import ToolAnnotations
 3
 4  from actions import ACTIONS
 5
 6  mcp = FastMCP("notekit")
 7
 8
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
10  def note_action(action: str, note_id: str) -> str:
11      """Run a note action (show, stats, ...)."""
12      if action not in ACTIONS:
13          return "unknown action: " + action
14      return ACTIONS[action](note_id)
```

```python
# actions.py
 1  import os
 2  import shutil
 3
 4  CACHE_DIR = os.path.expanduser("~/.notekit/cache")
 5
 6
 7  def show(note_id: str) -> str:
 8      with open(os.path.join(CACHE_DIR, note_id + ".md")) as fh:
 9          return fh.read()
10
11
12  def stats(note_id: str) -> str:
13      return str(os.path.getsize(os.path.join(CACHE_DIR, note_id + ".md")))
14
15
16  def prune(note_id: str) -> str:
17      shutil.rmtree(CACHE_DIR, ignore_errors=True)
18      return "pruned"
19
20
21  ACTIONS = {"show": show, "stats": stats, "prune": prune}
```

**判定表の行**（見落としの表）

| tree | unit | decl |
|---|---|---|
| （作った木） | `note_action`（`server.py:10`） | D1 |

18.2 の 4 で初めて開く解析器の出力: 矛も不もなく、効果も 0 です。`opaque` に `unresolved`。解析器は `ACTIONS[action](...)` の
呼び出し先を解決していません。

**問い 1: 届くか** — `server.py:14` の `ACTIONS[action](note_id)` は、一見 I-4.3 と同じ動的な呼び出しです。しかし `ACTIONS` は
`actions.py:21` に**定数の辞書**として書かれています。中身は `show`・`stats`・`prune` の 3 つで、木の外から足す道はありません。
`action` はモデルが決める引数です。モデルが `"prune"` を渡せば、`actions.py:16`（深さ 1）の `prune` に届きます。
答え: **はい**。条件の種類: `引数`。

**問い 2: 宣言に反するか** — `actions.py:17` の `shutil.rmtree(CACHE_DIR)` はディレクトリの削除です。手引き 15.1 の
`FS_WRITE` の行で**反します**。

**判定と記録**（手引き 18.4）

| 欄 | 値 |
|---|---|
| `outcome` | `見落とし` |
| `cause` | `呼び出しの解決`（`opaque` に `unresolved`。手引き 18.2 の 6） |
| `write_target` | `キャッシュ・状態の保存`（同じツールが `action="show"` で `CACHE_DIR` を読み返す。手引き 16.1 の順 6。「読み返す」の主語は判定しているツール） |
| `condition_type` | `引数` |
| `condition` | `引数 action に "prune" を渡したとき` |
| `depth` | `1` |
| `unknown_reason` | （空） |
| `output_found` | （空） |
| `evidence` | `読んだ範囲 server.py:9-14、actions.py:1-21。server.py:14 ACTIONS[action](note_id) → actions.py:21 ACTIONS = {"show": show, "stats": stats, "prune": prune}（定数）→ actions.py:17 shutil.rmtree(CACHE_DIR)。action はモデルが決める引数` |
| `note` | （空） |
| `minutes` | `6`（記入の例） |
| `ai_used` | `なし` |

**20〜30 分で決められるか、の目安**: この例は、`ACTIONS` の定義へ飛ぶだけで 5 分ほどで決まります。「動的な呼び出しだから不明」と
書くのは、手引き 19 の「調べれば分かるものを不明にしない」に反します。I-4.3 との違いは 1 点です。**呼び出し先の一覧が
木の中に定数で閉じているか**（I-4.4）、**木の外の登録で増えうるか**（I-4.3）。

**この例で学ぶこと**: 不明にする前に、「あと 1 ファイル読めば決まらないか」を確かめます。`getattr(self, "op_" + action)` の
ように名前を組み立てる形でも、候補のメソッドが木の中のクラスに閉じていれば、同じように決められます。

<a id="ai-4-5"></a>
### I-4.5 中身の見えない子プロセスの標準入力に書く（宣言 D1 / 判定: 不明 / 学ぶ点: 子の動作が分からないとき E5 に倒さない）

**コード**（作った例。`server.py`）

```python
 1  import base64
 2  import subprocess
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("scan")
 8  OCR_BIN = "ocrd"  # 取引先の OCR エンジン（閉じたバイナリ。PATH に置いて使う）
 9
10
11  def _ocr(data: bytes) -> str:
12      proc = subprocess.Popen(
13          [OCR_BIN, "--stdin", "--format", "text"],
14          stdin=subprocess.PIPE,
15          stdout=subprocess.PIPE,
16      )
17      out, _ = proc.communicate(input=data)
18      return out.decode("utf-8")
19
20
21  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
22  def read_scanned_page(image_b64: str) -> str:
23      """Extract text from a scanned page."""
24      return _ocr(base64.b64decode(image_b64))
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `pipe:communicate` | `FS_WRITE` | `fs_write`（矛） | `server.py:17` |

同じユニットに、別の組として `subprocess.Popen` × `SPAWN` × D1 の不（`spawn_command`、`server.py:12`）もあります。

**問い 1: 届くか** — 本体の 24 行 → `_ocr`（11 行）→ 12 行で起動 → 17 行で標準入力に画像を書きます。条件はありません。
答え: **はい**。条件の種類: `なし`。

**問い 2: 宣言に反するか** — 17 行はファイルの書き込みではなく、子プロセスの標準入力への書き込みです。手引き 15.1 の
迷いやすい形に、「それ自体はファイルを変えない。子プロセスがそれを受けて何をするかで決める」「pipe の組では、子プロセスの
動作は全部数える（D76）」とあります。

調べたこと（記入の例）: `ocrd` は取引先の閉じたバイナリで、ソースはありません。取引先のマニュアルは起動の引数と出力の形式
だけを書き、作業ファイル・キャッシュ・ログを書くかに触れていません。答え: **決められない**。

**判定と記録**（手引き 手順 H）

| 欄 | 値 |
|---|---|
| `verdict` | `不明` |
| `unknown_reason` | `その他: 子プロセス ocrd（取引先の閉じたバイナリ）が、標準入力を受けてファイルを書くかが、マニュアルに無く、ソースも無い` |
| `evidence` | `server.py:24 → server.py:12 subprocess.Popen(["ocrd", "--stdin", "--format", "text"], stdin=PIPE) → server.py:17 proc.communicate(input=data)。ocrd のマニュアル <開いた URL> に書き込みの記述なし`。 |
| `note` | `同じユニットの subprocess.Popen × SPAWN の不（spawn_command）も、同じ理由で決まらない` |
| `minutes` | `20`（記入の例） |
| `ai_used` | `なし` |

**類の選び方**: コマンド（`ocrd`）は定数で決まっています。決まらないのは**子プロセスの中の動作**です。典型 1〜4 のどれの字義にも
当たらないので「その他」にします（手引きの穴の仕分け `docs/drafts/guide_holes_triage.md` の H-7-2 も、子プロセスを「典型に当たらない
不明」に挙げています）。

**この例で学ぶこと**: 手引き 17 の E5 は「子プロセスがファイルを変えない」と**分かった**ときの誤です。分からないのに E5 に倒すのは、
黙って誤に倒すことです。子が `sort` のように標準出力に返すだけと文書で分かれば**誤（E5）**、子が「認識結果を `~/.cache/ocrd/` に
保存する」と文書にあれば**正**に変わります（種類は、子が書く先で付けます。手引き 20.2 の M59 の例）。

<a id="ai-4-6"></a>
### I-4.6 解析器が途中で読むのをやめたユニット（宣言 D1 / 判定: 不明（打ち切り） / 学ぶ点: 見えていても見落としに数えない）

**コード**（作った例。`server.py`。600 個の `elif` は生成スクリプトが書いた表）

```python
 1  import os
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("rules")
 7  LOG_PATH = os.path.expanduser("~/.rules/lookup.log")
 8
 9
10  def _audit(msg: str) -> None:
11      with open(LOG_PATH, "a") as fh:
12          fh.write(msg + "\n")
13
14
15  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
16  def explain_rule(code: str) -> str:
17      """Explain a lint rule by its code."""
18      _audit("explain_rule " + code)
19      # 以下は生成スクリプトが書いた 600 個の elif（規則の説明の表）
20      if code == "E0000":
21          text = "rule E0000"
22      elif code == "E0001":
23          text = "rule E0001"
        # …（E0002〜E0599 の elif が続く）
1220      else:
1221          text = "unknown rule"
1222      return text
```

**判定表の行**（見落としの表）

| tree | unit | decl |
|---|---|---|
| （作った木） | `explain_rule`（`server.py:16`） | D1 |

18.2 の 4 で初めて開く解析器の出力: 矛も不もなく、効果も 0 です。ユニットの `notes` に **`TRUNCATED(recursion)`** があります。
長い `elif` の連なりで解析器の再帰が上限を超え、このユニットを読むのをやめた印です（Python 3.10・3.12 のどちらで走らせても同じ）。

**問い 1: 届くか** — 出力を見る前に読んだ結果: 本体（深さ 0）の 18 行が毎回 `_audit`（深さ 1）を呼び、11 行で
`open(LOG_PATH, "a")` します。答え: **はい**。条件の種類: `なし`。

**問い 2: 宣言に反するか** — ログファイルへの追記です。手引き 15.1 の `FS_WRITE` の行で**反します**（ログも含む）。

ここまでなら**見落とし**です。しかし手引き 18.3 の 1 つ目の点があります。

> 打ち切りの印（`truncated`）があるユニットで、解析器が途中で読むのをやめたことが原因と分かったものは、**全部
> `不明（打ち切り）`** にする（見落としにしない。読み切れないときも `不明（打ち切り）`。D70 の 2、D76）。

解析器はこのユニットの効果を 1 つも出していません（18 行の呼び出しも読めていない）。`notes` の印から、原因は打ち切りと分かります。

**判定と記録**（手引き 18.4）

| 欄 | 値 |
|---|---|
| `outcome` | `不明（打ち切り）` |
| `cause` | （空。見落としにしないので書かない） |
| `depth` | `1` |
| `unknown_reason` | `打ち切り: ユニットの notes に TRUNCATED(recursion)。解析器はこのユニットの効果を 1 つも出していない（600 個の elif で再帰の上限）。反する動作 server.py:11 は見つけたが、打ち切りが原因なので見落としに数えない` |
| `output_found` | （空） |
| `evidence` | `読んだ範囲 server.py:10-1222。server.py:18 _audit(...) → server.py:11 open(LOG_PATH, "a")（毎回）` |
| `note` | （空） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 「打ち切り」は**ユニットの `notes` の `TRUNCATED(...)` だけ**です（D77 の 18）。深さの上限に当たった印
（`cap_hits` の `depth`）は打ち切りではありません。深さの上限の向こうに違反があれば、それは `見落とし（深さ 4 の外）` です
（自分で判定してみる の問 4）。D77 の 18 の数え方では、v4 で `TRUNCATED` のユニットは 3,696 のうち 1 で、まれです。

---

## 第 2 群 不の中身を決める

不の中身の判定（手引き 18A）は、**D1 と D2 の不だけ**が対象です。D3・D4 の不は判定しません（件数と理由だけ）。同じ宣言に矛と不の
両方の注記がある組は、矛として扱い、ここには来ません（18A.1、D76）。

結果は 3 つです（18A.2 の 4）。

| 結果 | 条件 |
|---|---|
| **違反** | 到達し、かつ宣言に反する |
| **違反でない** | 到達しない、または宣言に反しない |
| **不明** | 判定者が原ソースを読んでも決められない（手引き 19） |

違反なら書き込み先の種類（手引き 16）と条件の種類（14.3）を付けます。違反でないなら、理由を 1 文で `note` に書きます（D76）。

`POST` の組は、手引き 15.1 の表の `POST` の行で決めます。

> **相手の API の意味を調べて決める**。相手のドキュメントや API 名から「作成・更新・削除」なら反する、「照会」（検索 API・
> RPC の読み取り）なら反しない、分からなければ不明

D2 は 15.2 の `POST` の行です（「既存の資源を更新・削除するなら反する」）。D1 と D2 で答えが分かれることがあります（I-4.10）。

<a id="ai-4-7"></a>
### I-4.7 検索 API への POST（宣言 D1 / 判定: 違反でない / 学ぶ点: POST でも照会なら反しない）

**コード**（作った例。`server.py`）

```python
 1  import os
 2
 3  import httpx
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("docsearch")
 8  ES_URL = os.environ.get("ES_URL", "http://localhost:9200")
 9
10
11  def _search(index: str, text: str, size: int) -> list:
12      body = {"query": {"match": {"body": text}}, "size": size}
13      resp = httpx.post(f"{ES_URL}/{index}/_search", json=body, timeout=10)
14      resp.raise_for_status()
15      return [h["_source"]["title"] for h in resp.json()["hits"]["hits"]]
16
17
18  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
19  def search_docs(text: str, size: int = 10) -> str:
20      """Full-text search over the internal docs index."""
21      return "\n".join(_search("docs", text, size))
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `httpx.post` | `NET` | `net_post`（不） | `server.py:13` |

**問い 1: 届くか** — 本体の 21 行 → `_search`（11 行）→ 13 行。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.1 の `POST` の行で、相手の API の意味を調べます。

1. **宛先を読む**: `ES_URL`（運用者の設定。既定は `http://localhost:9200`）の `/docs/_search`。名前と既定のポートから、
   Elasticsearch の検索 API と読めます。モデルが決めるのは検索語 `text` と件数 `size` だけで、パスもメソッドも定数です。
2. **公式の文書を開く**: Elasticsearch の Search API（`https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search`）。
   `GET /{index}/_search` と `POST /{index}/_search` の両方が同じ操作として載り、説明は「Get search hits that match the query defined
   in the request.」です。**照会**です。
3. 本文は `match` の検索だけで、文書を足したり消したりする指定はありません。

答え: **いいえ**（反しない）。

**AI を使うなら**（手引き 21 の 6）: 聞いてよいのは「Elasticsearch の `POST /{index}/_search` は、作成・更新・削除・照会のどれをする？」
です。「このツールは `readOnlyHint` に反する？」は聞きません。AI が「照会」と答えても、上の 2 の文書を自分で開くまでは
`evidence` に書きません。この例では AI を使わずに決められました。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `reachable` | `はい` |
| `violates` | `いいえ` |
| `write_target`・`condition_type`・`condition` | （空。違反のときだけ） |
| `unknown_reason` | （空） |
| `evidence` | `server.py:21 → server.py:13 httpx.post(f"{ES_URL}/{index}/_search", json=body)。index は定数 "docs"、本文は match の検索。https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search（Search API: "Get search hits that match the query defined in the request."、GET と POST が同じ操作）` |
| `note` | `違反でない: POST 先は Elasticsearch の検索 API（照会）で、相手の状態を変えない` |
| `minutes` | `8`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 解析器が `POST` を「不」にするのは、メソッドだけでは意味が決まらないからです（手引き 13.1）。人は相手の
文書で決めます。同じ Elasticsearch でも、宛先が `/{index}/_doc`（文書の追加）や `/{index}/_delete_by_query` なら、答えは**違反**に
変わります。

<a id="ai-4-8"></a>
### I-4.8 チャットへの投稿（宣言 D1 / 判定: 違反 / 学ぶ点: 作成の POST・外部の状態の条件）

**コード**（作った例。`server.py`）

```python
 1  import os
 2
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("build")
 8  CI_URL = "https://ci.example.org/api"
 9  SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]
10  CHANNEL = os.environ.get("BUILD_CHANNEL", "#builds")
11
12
13  def _notify(text: str) -> None:
14      requests.post(
15          "https://slack.com/api/chat.postMessage",
16          headers={"Authorization": f"Bearer {SLACK_TOKEN}"},
17          json={"channel": CHANNEL, "text": text},
18          timeout=10,
19      )
20
21
22  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
23  def build_status(job: str) -> str:
24      """Return the status of a CI job."""
25      state = requests.get(f"{CI_URL}/jobs/{job}", timeout=10).json()["state"]
26      if state == "failed":
27          _notify(f"job {job} failed")
28      return state
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | `net_post`（不） | `server.py:14` |

25 行の `requests.get` は D1 では内（反しない）なので、組にはなっていません。

**問い 1: 届くか** — 本体の 25 行で CI の状態を取り、26 行で `"failed"` のときだけ 27 行 → `_notify`（13 行）→ 14 行です。
CI の応答で決まる条件なので、手引き 14.3 の `外部の状態`（相手が特定の応答を返したとき）です。答え: **はい**。

**問い 2: 宣言に反するか** — 宛先は定数の `https://slack.com/api/chat.postMessage` です。公式の文書
（`https://docs.slack.dev/reference/methods/chat.postMessage`。`api.slack.com/methods/chat.postMessage` から移った先）は
`POST https://slack.com/api/chat.postMessage` を「Sends a message to a channel.」と説明します。チャンネルにメッセージを**作る**ので、
相手のサーバの状態を変えます（原理 1-ii-b）。答え: **はい**（反する）。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `reachable` | `はい` |
| `violates` | `はい` |
| `write_target` | `相手側の状態`（手引き 16.1 の順 1） |
| `condition_type` | `外部の状態` |
| `condition` | `CI の API が job の状態として "failed" を返したとき` |
| `evidence` | `server.py:25 requests.get(...)["state"] → server.py:26 if state == "failed" → server.py:27 → server.py:14 requests.post("https://slack.com/api/chat.postMessage", ...)。https://docs.slack.dev/reference/methods/chat.postMessage（"Sends a message to a channel."）` |
| `note` | （空） |
| `minutes` | `7`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 「通知だから軽い」は判定に持ち込みません（手引き 11.3）。軽重は書き込み先の種類で表します。似た形の
`ctx.info()` や `ctx.report_progress()` は**クライアントへの通知**で、環境を変えないので反しません（手引き 15.1 の迷いやすい形）。
相手のサーバに残るかどうかが分かれ目です。

<a id="ai-4-9"></a>
### I-4.9 課題の状態を動かす POST（宣言 D2 / 判定: 違反 / 学ぶ点: 「既存の資源を更新する」POST）

**コード**（作った例。`server.py`。次の I-4.10 と同じ木）

```python
 1  import os
 2
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("jira")
 8  BASE = "https://example-team.atlassian.net/rest/api/3"
 9  AUTH = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
10
11
12  def _post(path: str, payload: dict) -> int:
13      resp = requests.post(BASE + path, json=payload, auth=AUTH, timeout=15)
14      return resp.status_code
15
16
17  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
18  def resolve_issue(key: str, transition_id: str) -> str:
19      """Move an issue to another status (e.g. Done)."""
20      code = _post(f"/issue/{key}/transitions", {"transition": {"id": transition_id}})
21      return f"HTTP {code}"
22
23
24  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
25  def add_comment(key: str, text: str) -> str:
26      """Add a comment to an issue."""
27      doc = {"type": "doc", "version": 1,
28             "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}]}
29      code = _post(f"/issue/{key}/comment", {"body": doc})
30      return f"HTTP {code}"
```

**判定表の行**（解析器の出力。本書の試験。ユニット `resolve_issue`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `requests.post` | `NET` | `net_post`（不） | `server.py:13` |

**問い 1: 届くか** — 本体の 20 行 → `_post`（12 行）→ 13 行。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.2 の `POST` の行「相手の API の意味で決める（既存の資源を更新・削除するなら反する）」です。
宛先は Jira Cloud の REST API v3 の `/issue/{key}/transitions` で、`key` はモデルが決める引数です。

公式の文書（`https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/` の Transition issue）は、
`POST /rest/api/3/issue/{issueIdOrKey}/transitions` を「Performs an issue transition and, if the transition has a screen, updates the fields
from the transition screen.」と説明します。**呼び出しの前からある課題**の状態を変えます。答え: **はい**（反する）。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `reachable` | `はい` |
| `violates` | `はい` |
| `write_target` | `相手側の状態` |
| `condition_type` | `なし` |
| `condition` | `なし` |
| `evidence` | `server.py:20 _post(f"/issue/{key}/transitions", ...) → server.py:13 requests.post(BASE + path, ...)。BASE は Jira Cloud の /rest/api/3、key はモデルが決める引数。https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/（Transition issue: "Performs an issue transition and, ... updates the fields from the transition screen."）` |
| `note` | （空） |
| `minutes` | `10`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: D2 の問いは「呼び出しの前からあったものを変えるか」です。メソッドが `POST` でも、相手の文書が既存の資源の
更新を書いていれば反します。同じ文書の Get transitions（`GET` の同じパス。「Returns either all transitions or a transition that can be
performed by the user on an issue, based on the issue's status.」）は照会です。パスが同じでもメソッドと文書で意味が変わります。

<a id="ai-4-10"></a>
### I-4.10 コメントを足す POST（宣言 D2 / 判定: 違反でない / 学ぶ点: D1 と D2 で答えが分かれる）

**コード**: I-4.9 と同じ木の `add_comment`（`server.py:24-30`）。

**判定表の行**（解析器の出力。本書の試験。ユニット `add_comment`）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `requests.post` | `NET` | `net_post`（不） | `server.py:13` |

**問い 1: 届くか** — 本体の 29 行 → `_post` → 13 行。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか** — 宛先は `/issue/{key}/comment` です。公式の文書
（`https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/` の Add comment）は、
`POST /rest/api/3/issue/{issueIdOrKey}/comment` を「Adds a comment to an issue.」と説明します。**新しいコメントを足す**だけです。
手引き 15.2 の表の「新しく作るだけ → 反しない」に当たります。答え: **いいえ**（反しない）。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `reachable` | `はい` |
| `violates` | `いいえ` |
| `evidence` | `server.py:29 _post(f"/issue/{key}/comment", {"body": doc}) → server.py:13 requests.post(BASE + path, ...)。https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/（Add comment: "Adds a comment to an issue."）` |
| `note` | `違反でない: コメントを新しく足すだけで、呼び出しの前からあるものを消す・変える API ではない（15.2 の「新しく作るだけ」）` |
| `minutes` | `5`（記入の例。同じ木の I-4.9 で下調べ済み） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 同じ `POST` を D1 に照らすと答えが変わります。D1 の問いは「呼び出しの後に残る何かを変えるか」で、
相手のサーバにコメントが残るので**違反**です。宣言ごとに問いが違うので、組ごとに宣言の節（15.1 / 15.2）を開き直します。

<a id="ai-4-11"></a>
### I-4.11 文書の無い社内 API への POST（宣言 D1 / 判定: 不明 / 学ぶ点: 相手の API と AI への問い方）

**コード**（作った例。`server.py`）

```python
 1  import os
 2
 3  import requests
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("ops")
 8  OPS_API = "https://ops.corp-tools.example.net/api"
 9  OPS_KEY = os.environ["OPS_API_KEY"]
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def project_health(project: str) -> str:
14      """Report the deployment health of a project."""
15      resp = requests.post(
16          f"{OPS_API}/v2/projects/{project}/sync",
17          headers={"X-Api-Key": OPS_KEY},
18          timeout=30,
19      )
20      data = resp.json()
21      return f"{project}: {data.get('state')} ({data.get('updated_at')})"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | `net_post`（不） | `server.py:15` |

**問い 1: 届くか** — 本体の 15 行。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.1 の `POST` の行で、相手の API の意味を調べます。順に手を動かします。

1. **木の中を探す**: `docs/`・`README`・OpenAPI の定義（`openapi.yaml` など）・クライアントのコメント。この木には何もありません。
2. **API の持ち主の文書を探す**: `ops.corp-tools.example.net` は社内の運用ツールで、公開の文書はありません。API の持ち主が出している
   文書を開ければ、それが公式の文書です。この例では開けませんでした。
3. **API 名を読む**: `/v2/projects/{project}/sync`。「sync」は「同期の状態を返す」とも「同期を始める」とも読めます。応答の
   `state`・`updated_at` も、どちらにも合います。名前からは決まりません。API 名で決めてよいのは、名前が作成・更新・削除（または照会）を
   はっきり示すときだけです（手引き 15.1 の POST の行。そのときは `evidence` に「API 名から」と書き、件数を報告する。D86 の 15）。

**AI を使った場合の手順**（手引き 21 の 6。記入の例）:

- 聞く前に、`note` に仮の判定を書きます: 「仮: 不明（相手の API）。sync が照会か起動かは名前から決まらない」。
- 貼るのは 12〜21 行のコードだけです。`annotations=ToolAnnotations(readOnlyHint=True)` を伏せます（docstring は宣言を述べる文では
  ないので、この例では残しました）。`OPS_KEY` の値はコードに書かれていないので、伏せる秘密はありません。
- 問い（事実）: 「この `POST /v2/projects/{project}/sync` は、作成・更新・削除・照会のどれをする？ 根拠の文書はある？」
- 聞かない問い（判定）: 「このツールは読み取り専用と言える？」「これは `readOnlyHint` に反する？」「これは環境を変える？」
- AI の答え（例）:「一般に sync という名前の端点は同期の処理を始めることが多い。ただし、この API の文書は見当たらない」。
  これは**名前からの推測**で、公式の文書でもソースでもありません。手引き 19 の基準では、確かめたことになりません。

答え: **決められない**。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `不明` |
| `reachable` | `はい` |
| `violates` | `決められない` |
| `unknown_reason` | `相手の API: POST /v2/projects/{project}/sync が照会か、同期を始める（相手の状態を変える）操作かが、木の中にも公開の文書にも無い。名前と応答の欄からは決まらない` |
| `evidence` | `server.py:15 requests.post(f"{OPS_API}/v2/projects/{project}/sync", ...)。OPS_API は定数 https://ops.corp-tools.example.net/api。木の中に API の文書・OpenAPI の定義なし。公開の文書なし（探した場所: <検索した URL>）` |
| `note` | `仮: 不明（相手の API）。AI に API の意味を聞いたが、名前からの推測だけで文書は示されず、判定に使わなかった` |
| `minutes` | `25`（記入の例。AI に聞いた時間を含む） |
| `ai_used` | `あり` |
| `ai_model` | `<モデル名> <版>（Web、記憶なしの設定）` |
| `ai_log` | `ai_logs/<会話の番号>.md` |

この件のために AI を使ったので、`ai_used` は `あり` です（手引き 12.3「AI を使ったかどうかも 1 件ごとに記録する」）。答えを判定の
根拠にしなかったことは `note` に書きます。

**この例で学ぶこと**: 不明の理由は「相手の API」です（手引き 19 の典型 2）。API の持ち主の文書を開けて、「`sync` は同期のジョブを
作って始める」と書いてあれば**違反**（`相手側の状態`）、「最後の同期の結果を返す」と書いてあれば**違反でない**に変わります。
AI の推測だけで違反に倒すのは、黙って倒すことと同じです。

<a id="ai-4-12"></a>
### I-4.12 `git log` を起動する（宣言 D1 / 判定: 違反でない / 学ぶ点: 定数のコマンドは文書で動作を調べる）

**コード**（作った例。`server.py`）

```python
 1  import subprocess
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("repo")
 7  REPO_DIR = "/srv/project"
 8
 9
10  def _git(*args: str) -> str:
11      return subprocess.run(
12          ["git", "-C", REPO_DIR, *args], capture_output=True, text=True, check=True
13      ).stdout
14
15
16  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
17  def recent_commits() -> str:
18      """Show the 20 most recent commits."""
19      return _git("log", "--oneline", "-n", "20")
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:11` |

**問い 1: 届くか** — 本体の 19 行 → `_git`（10 行）→ 11 行。条件はありません。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.1 の `SPAWN` の行「コマンドが定数なら、**そのコマンドが実際に何をするか**を調べ、環境を
変えるなら反する・変えないなら反しない・分からなければ不明」です。

- 起動するのは `git -C /srv/project log --oneline -n 20` で、全部定数です。モデルが渡す引数はありません。
- 公式の文書（`https://git-scm.com/docs/git-log`）: NAME は「git-log - Show commit logs」、DESCRIPTION は「Shows the commit logs.」。
  使っているオプション（`--oneline`・`-n`）は表示の形と件数だけを決めます。
- 標準出力は `capture_output=True` で受け取るだけです。

答え: **いいえ**（反しない）。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `reachable` | `はい` |
| `violates` | `いいえ` |
| `evidence` | `server.py:19 _git("log", "--oneline", "-n", "20") → server.py:11 subprocess.run(["git", "-C", REPO_DIR, *args])。引数はすべて定数。https://git-scm.com/docs/git-log（"Shows the commit logs."）` |
| `note` | `違反でない: git log はコミットの記録を表示するだけで、使っているオプションは表示の形と件数` |
| `minutes` | `6`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 同じ `git log` でも、**モデルがオプションを渡せる**と答えが変わります。git-log の文書には diff の
オプション `--output=<file>`（「Output to a specific file instead of stdout.」）があります。手引き 15.1 の迷いやすい形「定数のコマンドに、
モデルが引数・オプションを渡す」により、**違反**になります（自分で判定してみる の問 3）。

<a id="ai-4-13"></a>
### I-4.13 `git status` を起動する（宣言 D1 / 判定: 違反 / 学ぶ点: 読み取りに見えるコマンドも文書を開く）

**コード**（作った例。`server.py`）

```python
 1  import subprocess
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("repo")
 7  REPO_DIR = "/srv/project"
 8
 9
10  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
11  def changed_files() -> str:
12      """List files with uncommitted changes."""
13      out = subprocess.run(
14          ["git", "status", "--porcelain"],
15          cwd=REPO_DIR, capture_output=True, text=True, check=True,
16      ).stdout
17      return out or "clean"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:13` |

**問い 1: 届くか** — 本体の 13 行。毎回起動します。答え: **はい**。

**問い 2: 宣言に反するか** — 「`git status` は状態を見るだけ」と思いがちです。しかし手引き 15.1 の `SPAWN` の行は、名前ではなく
**実際に何をするか**を調べよ、と言います。公式の文書（`https://git-scm.com/docs/git-status` の BACKGROUND REFRESH）には次の文があります。

> By default, `git status` will automatically refresh the index, updating the cached stat information from the working tree and
> writing out the result. Writing out the updated index is an optimization that isn't strictly necessary …

つまり `git status` は、既定で **index（`.git/index` のファイル）を更新して書き出します**。ファイルの書き込みなので、15.1 の
`FS_WRITE` の行と同じく環境の変更です（原理 1-i-b。軽重は判定に持ち込まない。手引き 11.3）。答え: **はい**（反する）。

条件: 文書は「既定で書き出す」とだけ書き、いつ書くかを書いていません。20〜30 分の中なら木の外のソースも読んでよいので（手引き 19、
D76）、git のソースを開きます。`builtin/commit.c` の `cmd_status` は `repo_update_index_if_able` を呼び、`read-cache.c` のその関数は
`cache_changed`（index の記録を更新した）か `has_racy_timestamp`（時刻が際どい）のときだけ `write_locked_index` で書き出し、
そうでなければロックを捨てます。行は毎回実行されるが、環境が変わるのは一部、という形なので、手引き 14.3 の迷いやすい形の表により
`外部の状態` を書きます。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `reachable` | `はい` |
| `violates` | `はい` |
| `write_target` | `プロセスの起動・コードの実行`（手引き 16.2: SPAWN の正は、子が何を変えるか分かるときも常にこの種類。D76） |
| `condition_type` | `外部の状態` |
| `condition` | `index の stat の記録を更新する必要があるとき（作業木のファイルが index の記録とずれているときなど。git status が index を書き出す）` |
| `evidence` | `server.py:13 subprocess.run(["git", "status", "--porcelain"], cwd=REPO_DIR)。引数はすべて定数。https://git-scm.com/docs/git-status の BACKGROUND REFRESH（"automatically refresh the index, ... and writing out the result"）。git のソース builtin/commit.c の cmd_status → read-cache.c の repo_update_index_if_able（cache_changed か has_racy_timestamp のとき write_locked_index）` |
| `note` | （空） |
| `minutes` | `12`（記入の例） |
| `ai_used` | `なし` |

**この例で学ぶこと**: 起動の行が `git --no-optional-locks status` なら、答えは変わりえます。git の文書（`https://git-scm.com/docs/git`）は
`--no-optional-locks` を「Do not perform optional operations that require locks.」と説明します。git-status の文書は、上の書き出しを
「isn't strictly necessary」な最適化とし、ロックを取ることを書いたうえで、このオプションを勧めています。書き出しが省かれることを
文書かソースで確かめられたら、**違反でない**と書けます。「読み取りの名前のコマンドだから違反でない」と、文書を開かずに決めないことが要点です。

<a id="ai-4-14"></a>
### I-4.14 一覧の前にスナップショットを取る（宣言 D1 / 判定: 違反 / 学ぶ点: 位置が複数ある不の組）

**コード**（作った例。`server.py`）

```python
 1  import subprocess
 2
 3  from mcp.server.fastmcp import FastMCP
 4  from mcp.types import ToolAnnotations
 5
 6  mcp = FastMCP("notes")
 7  NOTES_DIR = "/srv/notes"
 8
 9
10  def _snapshot() -> None:
11      subprocess.run(["git", "add", "-A"], cwd=NOTES_DIR, check=True)
12      subprocess.run(["git", "commit", "-q", "-m", "auto snapshot"], cwd=NOTES_DIR)
13
14
15  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
16  def list_notes() -> str:
17      """List note files (takes a snapshot first so the list is consistent)."""
18      _snapshot()
19      out = subprocess.run(["git", "ls-files"], cwd=NOTES_DIR, capture_output=True, text=True)
20      return out.stdout
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:11`, `server.py:12`, `server.py:19` |

**問い 1: 届くか** — 本体の 18 行 → `_snapshot`（10 行）→ 11 行・12 行。続いて 19 行。どれも毎回起動します。答え: **はい**。

**問い 2: 宣言に反するか** — 位置が 3 つあります。手引き 18A.2 の 3 の最後の点（D76）により、手順 G と同じく「1 つでも到達し、かつ
反する位置があれば違反」です。

| 位置 | コマンド | 公式の文書 | 反するか |
|---|---|---|---|
| `server.py:11` | `git add -A` | `https://git-scm.com/docs/git-add`: 「Add contents of new or changed files to the index.」 | 反する（index を書き換える） |
| `server.py:12` | `git commit -q -m …` | `https://git-scm.com/docs/git-commit`: 「Create a new commit containing the current contents of the index …」 | 反する（コミットを作り、ブランチを動かす） |
| `server.py:19` | `git ls-files` | `https://git-scm.com/docs/git-ls-files`: 「Show information about files in the index and the working tree」 | 反しない（表示だけ） |

最初に反すると分かったのは 11 行です。答え: **はい**（反する）。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `違反` |
| `reachable` | `はい` |
| `violates` | `はい` |
| `write_target` | `プロセスの起動・コードの実行` |
| `condition_type` | `外部の状態` |
| `condition` | `ノートの作業木に、まだ index・コミットに入っていない変更があるとき` |
| `evidence` | `server.py:18 _snapshot() → server.py:11 subprocess.run(["git", "add", "-A"], cwd=NOTES_DIR)。https://git-scm.com/docs/git-add（"Add contents of new or changed files to the index."）` |
| `note` | `12 行の git commit も反する（https://git-scm.com/docs/git-commit）。19 行の git ls-files は表示だけで反しない` |
| `minutes` | `10`（記入の例） |
| `ai_used` | `なし` |

条件の種類: 変更が無ければ `git add -A` は index を書き出しません（git のソース `builtin/add.c` は `write_locked_index` に
`SKIP_IF_UNCHANGED` を渡します）。`git commit` も、コミットするものが無ければコミットを作りません。手引き 14.3 の「行は毎回実行されるが、
環境が変わるのは一部」の行により `外部の状態` です。

**この例で学ぶこと**: 不の組にも位置が複数あります。反しない位置（19 行）があっても、組の結果は変わりません。逆に、全部の位置が
反しないときだけ「違反でない」にでき、そのときは全部の位置を読みます（手順 G）。

<a id="ai-4-15"></a>
### I-4.15 木に無いスクリプトを起動する（宣言 D1 / 判定: 不明 / 学ぶ点: 名前から推して決めない）

**コード**（作った例。`server.py`）

```python
 1  import os
 2  import subprocess
 3
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("inventory")
 8  TOOLS_DIR = "/opt/inventory/bin"  # 配備のときに運用チームが置く（この repo には無い）
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def stock_level(sku: str) -> str:
13      """Return the current stock level of a product."""
14      subprocess.run([os.path.join(TOOLS_DIR, "refresh-stock.sh")], check=True, timeout=60)
15      with open("/var/lib/inventory/stock.csv") as fh:
16          for line in fh:
17              if line.startswith(sku + ","):
18                  return line.strip()
19      return "not found"
```

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:14` |

**問い 1: 届くか** — 本体の 14 行。毎回起動します。答え: **はい**。

**問い 2: 宣言に反するか** — 起動するのは `/opt/inventory/bin/refresh-stock.sh` です。

1. 木の中を `refresh-stock` で検索します。見つかりません（8 行のコメントのとおり、配備のときに置かれる）。
2. README・配備の文書を探します。スクリプトの中身や動作の説明はありません。
3. 名前（refresh）と、直後に `stock.csv` を読むことから、「`stock.csv` を書き直すのだろう」と**推せます**。しかし推測です。
   手引き 19 の基準では、公式の文書かソースを開けたときだけ確かめたとします。

答え: **決められない**。

**判定と記録**（手引き 18A.3）

| 欄 | 値 |
|---|---|
| `outcome` | `不明` |
| `reachable` | `はい` |
| `violates` | `決められない` |
| `unknown_reason` | `その他: 起動するスクリプト /opt/inventory/bin/refresh-stock.sh が木に無く（配備のときに置かれる）、中身も動作の文書も無い。名前からは stock.csv の更新と推せるが確かめられない` |
| `evidence` | `server.py:14 subprocess.run([os.path.join(TOOLS_DIR, "refresh-stock.sh")])。TOOLS_DIR は定数 /opt/inventory/bin。木の中を refresh-stock で検索して該当なし。README・docs に記述なし` |
| `note` | （空） |
| `minutes` | `20`（記入の例） |
| `ai_used` | `なし` |

**類の選び方**: コマンドのパスは定数で決まっています（典型 1 の「コマンドが外の値で決まる」ではない）。決まらないのは子の中身です。
I-4.5 と同じく「その他」にし、説明を書きます。

**この例で学ぶこと**: 名前から推して**違反に倒すのも、違反でないに倒すのも**、手引き 19 に反します。スクリプトが木の中に
あれば、それを開いて決めます（自分で判定してみる の問 6 は `Makefile` が木の中にある形）。

<a id="ai-4-16"></a>
### I-4.16 宛先が設定で決まり、既定値が外部（宣言 D3 / 判定: 判定しない（練習では反する） / 学ぶ点: 対象かを先に確かめる）

**コード**（作った例。`server.py`）

```python
 1  import os
 2
 3  import httpx
 4  from mcp.server.fastmcp import FastMCP
 5  from mcp.types import ToolAnnotations
 6
 7  mcp = FastMCP("geo")
 8  GEO_URL = os.environ.get("GEO_URL", "https://geocoder.mapvendor.io")
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
12  def geocode(address: str) -> str:
13      """Convert an address to coordinates."""
14      resp = httpx.get(f"{GEO_URL}/search", params={"q": address}, timeout=10)
15      hit = resp.json()[0]
16      return f"{hit['lat']},{hit['lon']}"
```

（`geocoder.mapvendor.io` は作った名前です。公開のジオコーディングのサービスとして読んでください。）

**判定表の行**（解析器の出力。本書の試験）

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D3 | `httpx.get` | `NET` | `net_host_unknown`（不） | `server.py:14` |

D1 の組はありません（`GET` は D1 で内）。

**まず、判定の対象かを確かめる**: 手引き 18A.1 は「D3・D4 の不は判定しない（件数と理由だけ）」と書きます。この組は**最終評価の
判定表に載りません**。判定表に載らない組に時間を使わないことが、最初の手順です。

以下は、15.3 の表を読む**練習**です（D3 の矛を判定するときと同じ読み方）。

**問い 1: 届くか** — 本体の 14 行。毎回通信します。答え: **はい**。

**問い 2: 宣言に反するか** — 手引き 15.3 の表の「宛先が運用者の設定で決まる（環境変数の URL など）」の行です。

> 設定の既定値や文書で外部を想定しているなら反する、ローカルを想定しているなら反しない、分からなければ不明

8 行の既定値は `https://geocoder.mapvendor.io` で、公開の外部のホストです。答え: **はい**（反する）。

**練習としての記入**（最終評価の判定表には載らない。D3 の矛として出たときの、D83 の形の書き方）

| 欄 | 値 |
|---|---|
| `verdict` | `正`（既定値が外部のホスト） |
| `condition_type` | `なし` |
| `write_target` | `その他・不明`（手引き 16.3 の例「宛先が運用者の設定で、既定値が外部のもの」） |
| `note` | 先頭に `その他:` を書き、「宛先が運用者の設定 GEO_URL、既定値が外部のホスト」と書く（手引き 16.2 の最後の段落と 16.3。D76） |
| `evidence` | `server.py:8 GEO_URL = os.environ.get("GEO_URL", "https://geocoder.mapvendor.io") → server.py:14 httpx.get(f"{GEO_URL}/search", ...)` |

**この例で学ぶこと**: 既定値が `http://localhost:8080` や `http://geocoder:8080`（ドットの無い名前）なら、15.3 の local の範囲に入り、
「ローカルを想定している」ので反しません。既定値が無く（`os.environ["GEO_URL"]`）、README にも想定が書かれていなければ、
「分からなければ不明」の側です。どれも、最終評価では D3 の**矛**として出たときにだけ判定します。

---

<a id="ai-4-x"></a>
### I-4.x この分冊の例の一覧

| 番号 | 題 | 宣言 | 解析器 | 判定（本書の答え） | 学ぶ点 |
|---|---|---|---|---|---|
| [I-4.1](#ai-4-1) | 消すファイルのパスが、ソースの無いライブラリの戻り値 | D2 | 矛 `fs_remove` | 不明（外の値） | 戻り値のファイルが前からあったかで E2 か正かが分かれる |
| [I-4.2](#ai-4-2) | 外の SDK が呼び戻すかもしれない保存の関数 | D1 | 何も出さない | 不明（動的な呼び出し） | 呼び戻しの時期が文書に無い。呼び戻しの類は D86 で決まった |
| [I-4.3](#ai-4-3) | プラグインの読み込みで、呼び出し先が木の外で決まる | D1 | 何も出さない | 不明（動的な呼び出し） | entry_points の登録は木の外で増えうる |
| [I-4.4](#ai-4-4) | 動的に見えるが、表がもう 1 つのファイルに書いてある | D1 | 何も出さない | 見落とし（呼び出しの解決） | 1 ファイル読めば決まるものを不明にしない |
| [I-4.5](#ai-4-5) | 中身の見えない子プロセスの標準入力に書く | D1 | 矛 `fs_write`（pipe） | 不明（その他） | 分からないのに E5 に倒さない |
| [I-4.6](#ai-4-6) | 解析器が途中で読むのをやめたユニット | D1 | 何も出さない（`TRUNCATED(recursion)`） | 不明（打ち切り） | 違反が見えても見落としに数えない |
| [I-4.7](#ai-4-7) | 検索 API への POST | D1 | 不 `net_post` | 違反でない | POST でも照会なら反しない |
| [I-4.8](#ai-4-8) | チャットへの投稿 | D1 | 不 `net_post` | 違反（相手側の状態、外部の状態） | 作成の POST。通知の軽重を持ち込まない |
| [I-4.9](#ai-4-9) | 課題の状態を動かす POST | D2 | 不 `net_post` | 違反（相手側の状態） | 既存の資源を更新する POST |
| [I-4.10](#ai-4-10) | コメントを足す POST | D2 | 不 `net_post` | 違反でない | D1 と D2 で答えが分かれる |
| [I-4.11](#ai-4-11) | 文書の無い社内 API への POST | D1 | 不 `net_post` | 不明（相手の API） | AI の推測は確かめたことにならない |
| [I-4.12](#ai-4-12) | `git log` を起動する | D1 | 不 `spawn_command` | 違反でない | 定数のコマンドは文書で動作を調べる |
| [I-4.13](#ai-4-13) | `git status` を起動する | D1 | 不 `spawn_command` | 違反（外部の状態） | 読み取りに見えるコマンドも文書を開く |
| [I-4.14](#ai-4-14) | 一覧の前にスナップショットを取る | D1 | 不 `spawn_command`（3 位置） | 違反（外部の状態） | 位置が複数ある不の組 |
| [I-4.15](#ai-4-15) | 木に無いスクリプトを起動する | D1 | 不 `spawn_command` | 不明（その他） | 名前から推して決めない |
| [I-4.16](#ai-4-16) | 宛先が設定で決まり、既定値が外部 | D3 | 不 `net_host_unknown` | 判定しない（練習では反する） | 18A の対象かを先に確かめる |

内訳: 不明 7（うち打ち切り 1）・違反 4・違反でない 3・見落とし 1・判定しない 1。宣言は D1 が 12、D2 が 3、D3 が 1 です。

<a id="ai-4-y"></a>
### I-4.y 自分で判定してみる

コードと、解析器の出力（判定表の行）だけを出します。どの問いも、凍結版の解析器で実際に走らせた出力です。手引きを開いて、
結果と、記録の主な欄（条件の種類・書き込み先の種類・`unknown_reason` など）を決めてください。

**問 1**（D1）

```python
 7  mcp = FastMCP("gh")
 8  TOKEN = os.environ["GITHUB_TOKEN"]
 9  QUERY = "query { viewer { login repositories(first: 20) { nodes { name } } } }"
10
11
12  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
13  def my_repos() -> str:
14      """List my repositories."""
15      resp = requests.post("https://api.github.com/graphql",
16                           json={"query": QUERY},
17                           headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
18      nodes = resp.json()["data"]["viewer"]["repositories"]["nodes"]
19      return "\n".join(n["name"] for n in nodes)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | `net_post`（不） | `server.py:15` |

<details><summary>答え</summary>

**違反でない**。GitHub の GraphQL API は、照会（query）も変更（mutation）も `POST` で送ります。公式の文書
（`https://docs.github.com/en/graphql/guides/forming-calls-with-graphql`）は「you'll provide a JSON-encoded body whether you're performing a
query or a mutation, so the HTTP verb is `POST`」と書き、query を「Queries operate like `GET` requests」と説明します。送る文書は 9 行の
定数で、`query { … }`（照会）です。`note`: 「違反でない: 送る GraphQL の文書は定数の query（照会）」。

</details>

**問 2**（D1）

```python
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def github_graphql(document: str) -> str:
13      """Run a GraphQL document against the GitHub API and return the JSON."""
14      resp = requests.post("https://api.github.com/graphql",
15                           json={"query": document},
16                           headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
17      return resp.text
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | `net_post`（不） | `server.py:14` |

<details><summary>答え</summary>

**違反**。送る GraphQL の文書 `document` はモデルが決める引数です。モデルが決める値は「取りうる値の全体」で考えます（手引き 手順 F、
原理 3-a）。同じ文書は mutation を「Mutations operate like `POST`/`PATCH`/`DELETE`」と説明し、モデルは mutation を送れます。
`write_target`: `相手側の状態`。`condition_type`: `引数`（`condition`: 引数 document に mutation を渡したとき）。問 1 との違いは、
送る文書が定数かモデルの値か、の 1 点です。

</details>

**問 3**（D1）

```python
 9  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
10  def history(extra_args: list[str]) -> str:
11      """Show git history. extra_args are passed to `git log` (e.g. ["--since=2.weeks"])."""
12      cmd = ["git", "log", "--oneline", *extra_args]
13      return subprocess.run(cmd, cwd="/srv/project", capture_output=True, text=True).stdout
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:13` |

<details><summary>答え</summary>

**違反**。コマンド（`git log`）は定数で、解析器は `spawn_model` ではなく `spawn_command` を出しています。しかしモデルがオプションを
渡せます。手引き 15.1 の迷いやすい形「定数のコマンドに、モデルが引数・オプションを渡す: 引数にも原理 3-a を当てる。モデルが書ける
オプションに環境を変えるもの（`--output=` など）があれば反する（D76）」に当たります。git-log の文書
（`https://git-scm.com/docs/git-log`）に `--output=<file>`「Output to a specific file instead of stdout.」があります。
`write_target`: `プロセスの起動・コードの実行`。`condition_type`: `引数`。I-4.12 との違いは、モデルが引数を渡せるかの 1 点です。

</details>

**問 4**（D1。見落としの表の行。解析器の出力は 18.2 の 4 で開く）

```python
 8  STATE = os.path.expanduser("~/.cfgtool/state.json")
 9
10
11  def _l6(d):
12      with open(STATE, "w") as fh:
13          json.dump(d, fh)
14
15
16  def _l5(d):
17      _l6(d)
    # …（_l4 → _l5、_l3 → _l4、_l2 → _l3、_l1 → _l2 と 1 段ずつ呼ぶ）
36  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
37  def show_config(name: str) -> str:
38      """Show a config entry."""
39      d = {"last": name}
40      _l1(d)
41      return name
```

解析器の出力: 矛も不もなく、効果も 0 です。ユニットの `cap_hits` に `depth`（`opaque` にも `depth`）。`notes` に `TRUNCATED` はありません。

<details><summary>答え</summary>

**見落とし（深さ 4 の外）**（`cause`: `深さ`）。本体が深さ 0、`_l1` が深さ 1 で、12 行の `open(STATE, "w")` は `_l6` の中の
深さ 6 です。深さ 4 より奥の違反を見つけたので、手引き 18.3 により `見落とし（深さ 4 の外）` にします（主の見落としの数に入れない）。
`不明（打ち切り）` ではありません。`cap_hits` の `depth` は深さの上限の印で、打ち切りの印（`notes` の `TRUNCATED(...)`）ではないからです
（D77 の 18）。読む範囲は深さ 4 までなので、ふつうは深さ 5 以降を探しに行きません。この問いはファイルが短く、偶然見えた形です。

</details>

**問 5**（D2）

```python
11  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
12  def format_snippet(code: str) -> str:
13      """Format a Python snippet with black and return it."""
14      fd, path = tempfile.mkstemp(suffix=".py")
15      with os.fdopen(fd, "w") as fh:
16          fh.write(code)
17      subprocess.run(["black", "-q", path])
18      with open(path) as fh:
19          out = fh.read()
20      os.remove(path)
21      return out
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `os.remove` | `FS_WRITE` | `fs_remove`（矛） | `server.py:20` |

（同じユニットに、別の組として `subprocess.run` × `SPAWN` × D2 の不 `spawn_command`、`server.py:17` もあります。）

<details><summary>答え</summary>

**誤（E2）**（到達するが反しない。D83 の形なので `reachable`・`violates` の欄は書かず、`error_class` に `E2: server.py:20 が消すのは、同じ呼び出しの :14 で mkstemp が作った一時ファイル` と書く）。20 行が消す `path` は、14 行の `tempfile.mkstemp` が同じ呼び出しで作ったファイルです。
Python の公式の文書（`https://docs.python.org/3/library/tempfile.html`）は `mkstemp` を「Creates a temporary file in the most secure manner
possible.」と説明し、消すのは使う側の責任と書きます。手引き 15.2 の迷いやすい形「同じ呼び出しで自分が作った一時ファイルを消す → 反しない
（誤、E2）」です。I-4.1 との違いは、戻り値の性質が公式の文書で分かるかの 1 点です。

</details>

**問 6**（D1。木の中に `Makefile` がある）

```python
 7  mcp = FastMCP("proj")
 8  PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
 9
10
11  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
12  def code_stats() -> str:
13      """Line counts of the project's Python sources."""
14      out = subprocess.run(["make", "-s", "stats"], cwd=PROJECT_DIR, capture_output=True, text=True)
15      return out.stdout
```

```make
# Makefile（server.py と同じフォルダ）
stats:
	@mkdir -p build
	@find src -name "*.py" | xargs wc -l > build/stats.txt
	@cat build/stats.txt
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `subprocess.run` | `SPAWN` | `spawn_command`（不） | `server.py:14` |

<details><summary>答え</summary>

**違反**。`make` が何をするかは、`cwd` の `Makefile` で決まります。`PROJECT_DIR` は `server.py` のフォルダで、その `Makefile` は木の中に
あります。`stats` の手順は `build/` を作り、`build/stats.txt` に書き出します。ファイルの作成・書き込みなので反します（手引き 15.1）。
`write_target`: `プロセスの起動・コードの実行`。`condition_type`: `なし`（毎回書き出す）。`evidence` は
`server.py:14 → Makefile の stats の 3 行目（> build/stats.txt）` の形です。I-4.15 との違いは、起動する中身が木の中にあり、
1 ファイル読めば決まることです。

</details>

**問 7**（D2）

```python
 8  CRM = "https://crm.internal-apps.example.net/api/v1"
 9  KEY = os.environ["CRM_KEY"]
10
11
12  @mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
13  def tag_customer(customer_id: str, tag: str) -> str:
14      """Attach a tag to a customer."""
15      resp = requests.put(f"{CRM}/customers/{customer_id}/tags",
16                          json={"tag": tag}, headers={"X-Key": KEY}, timeout=10)
17      return str(resp.status_code)
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D2 | `requests.put` | `NET` | `net_put_model_url`（矛） | `server.py:15` |

<details><summary>答え</summary>

**正**。社内 API で文書がありませんが、不明にはしません。手引き 15.2 の表の `PUT` の行は「宛先をモデルが決められるなら反する。
そうでなければ、既存の資源の置き換えか新規作成かで決める」です。宛先の `customers/{customer_id}/tags` の `customer_id` はモデルが
決める引数で、モデルは既存の顧客の資源を指せます。表の前半で決まるので、API の意味を調べる後半には進みません。
`condition_type`: `なし`、`write_target`: `相手側の状態`（D83 の形なので `reachable`・`violates` の欄は書かない。D2 の正なので `target_by_arg` も書かない。D84）。手引きの表の行で決まる形を、文書が無いことを
理由に不明にしないこと（手引き 19 の「調べれば分かるものを不明にしない」）が要点です。

</details>

**問 8**（D1）

```python
 8  API = "https://api.ledgerly-partner.example.com"
 9
10
11  def _login() -> str:
12      resp = requests.post(f"{API}/auth/login",
13                           json={"user": os.environ["LEDGER_USER"], "password": os.environ["LEDGER_PW"]},
14                           timeout=10)
15      return resp.json()["token"]
16
17
18  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
19  def account_balance(account: str) -> str:
20      """Return the balance of an account."""
21      token = _login()
22      resp = requests.get(f"{API}/accounts/{account}/balance",
23                          headers={"Authorization": f"Bearer {token}"}, timeout=10)
24      return str(resp.json()["balance"])
```

| decl | site | kind | reasons | locations |
|---|---|---|---|---|
| D1 | `requests.post` | `NET` | `net_post`（不） | `server.py:12` |

`ledgerly-partner` は作った取引先で、API の文書は公開されていないものとします。

<details><summary>答え</summary>

**不明**（`unknown_reason`: `相手の API: POST /auth/login がセッションを作る（相手の状態を変える）かが、公開の文書にもコードにも無い`）。
手引き 15.1 の迷いやすい形に「認証・トークン・ログインの `POST`: 上の表の `POST` の行のとおり、相手の文書で決める。文書に無ければ
不明（D76）」とあります。「ログインはセッションを作るから違反」とも「ログインは読み取りの前置きだから違反でない」とも、文書なしには
決めません。`reachable`: `はい`（`なし`）、`violates`: `決められない`。相手の文書に「ログインはセッションを作る」とあれば違反
（`相手側の状態`）に変わります。

</details>

---

[← 前](appendix-i-3.md) ｜ [付録 I の表紙](appendix-i.md) ｜ [目次](README.md)
