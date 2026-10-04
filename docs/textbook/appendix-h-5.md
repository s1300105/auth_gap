[← 前](appendix-h-4.md) ｜ [付録 H の表紙](appendix-h.md) ｜ [目次](README.md) ｜ [次 →](appendix-h-6.md)

---

# 付録 H-5 ラベルを付ける — 書き込み先の種類・通信先の種類・誤の原因

<a id="ah-5-0"></a>
### この分冊で読む範囲

判定の手引きの下書き `docs/drafts/final_judging_guide_draft.md`（コミット af897ef の時点）の **L406〜L469** を読みます。
手引きの冒頭の「承認の前に学生が確かめること」の 5 と 6 が、この範囲です（`docs/drafts/final_judging_guide_draft.md:23-24`）。

| 本書の節 | 手引きの節 | 手引きの行 | 中身 |
|---|---|---|---|
| [H-5.1](#ah-5-1) | 第 16 節の前書き | L406-409 | ラベルは何のためか。重みではない |
| [H-5.2](#ah-5-2) | 16.1 の見出しと順番の規則 | L411-416 | 上から順に当てはめる |
| [H-5.3](#ah-5-3)〜[H-5.10](#ah-5-10) | 16.1 の表の 8 行 | L417-424 | 書き込み先の種類 8 つを 1 つずつ |
| [H-5.11](#ah-5-11) | 16.2 境界の例 | L426-438 | 先に決めた 6 つの事例と、決められないとき |
| [H-5.12](#ah-5-12)〜[H-5.16](#ah-5-16) | 16.3 通信先の種類 | L440-449 | D3 の正に付ける 4 つ |
| [H-5.17](#ah-5-17) | 第 17 節の前書きと表の見出し | L451-457 | 誤の原因の欄 |
| [H-5.18](#ah-5-18)〜[H-5.26](#ah-5-26) | 第 17 節の表の 9 行 | L458-466 | E1〜E9 を 1 つずつ |
| [H-5.27](#ah-5-27) | 第 17 節の結び | L468 | 迷ったら E9、内訳は限界の材料 |

同じ中身を教科書の側から説明しているのが[第 51 章](ch51.md)です。この分冊は、手引きの文を 1 行ずつ追い、学生が承認する前に
「自分ならそう付けるか」を確かめるためのものです。第 51 章と重なる説明は短くし、リンクで送ります。

**注意（行番号のずれ）**: 第 51 章が引く下書きの行番号は、前の版の下書きの行です。今の下書き（af897ef）では、第 16・17 節が
**23 行うしろ**にずれています（例: 第 51 章の `final_judging_guide_draft.md:388-401` は、今の L411-424）。この分冊の行番号は、
すべて今の下書きの行です。

<a id="ah-5-0b"></a>
### 前の分冊から持ってくる知識

付録 H の前の分冊（手引きの第 11〜15 節を読んだ分冊）から、次の知識を使います。忘れていたら、括弧の章で読み直してください。

- **組**: 判定の単位。(木, ユニット, site, kind, 宣言) で 1 組（`docs/drafts/final_judging_guide_draft.md:38-39`。[第 48 章](ch48.md#s48-2)）。
- **正・誤・不明**: 「到達するか」と「宣言に反するか」の両方が「はい」なら正。どちらかが「いいえ」なら誤。決められなければ不明
  （`docs/drafts/final_judging_guide_draft.md:43-54`）。
- **kind**: 効果の種類。`FS_WRITE`（ファイルの書き込み・作成・削除）、`DB`（データベースの操作）、`NET`（通信）、`SPAWN`（プロセスの起動）、
  `EXEC`（コードの実行）（[第 13 章](ch13.md)）。**site** は、効果を起こす関数の名前（`builtins.open`、`os.remove` など）。
- **手順 H の欄**: 正にしたら `write_target` に種類を、誤にしたら `error_class` に原因を書く（`docs/drafts/final_judging_guide_draft.md:179-180`）。
- **手順 G**: 1 組に位置が複数あれば、1 つでも「到達する かつ 反する」位置があれば正。1 つ正が見つかれば止めてよい
  （`docs/drafts/final_judging_guide_draft.md:158-163`）。
- **到達しない形**（14.2）と、その誤の原因の記号 E1・E3 / E4・E6（`docs/drafts/final_judging_guide_draft.md:240-246`）。
- **宣言ごとの問い**（第 15 節）: D1 は「呼び出しの後に残る何かを変えるか」、D2 は「呼び出しの前からあったものを消す・上書きする・
  変えるか」、D3 は「外部の相手、またはモデルが決める相手と通信しうるか」、D4 は「同じ引数で 2 回呼ぶと 2 回目がさらに変えるか」。
- **D3 の local の範囲**（15.3）。ドットの無い名前と `〜.internal` は local。解析器はそれを外部とするので、それで出た D3 の矛は誤
  （`docs/drafts/final_judging_guide_draft.md:371-388`）。
- **原理 3-a**: モデルが決める値は「取りうる値の全体」で考える（`docs/contradiction_principles.md:72-77`）。

<a id="ah-5-0c"></a>
### この分冊の「本書の試験」について

この分冊では、作った例のいくつかを、凍結版の解析器（`analyzer-freeze-3`。本書の執筆時の作業木の `authgap/` は、このタグと差分が
ありません）で実際に走らせ、出た注記を書きます。走らせたものには「（作った例。本書の試験）」と書きます。
試験のファイルは repo の外（本記録者の作業用の場所）に置いたので、確かめたいときは、下のコードを空のディレクトリに写して
`.venv/bin/python -m authgap scan <ディレクトリ>` を走らせてください。出力の `units[].rows[].notes` に `contradiction:` で始まる注記が出ます。

**試験 A**（`server.py`）:

```python
import os
import shlex
import subprocess
import uuid

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("h5")
_store = None


def _get_store():
    global _store
    if _store is None:
        os.makedirs(os.path.expanduser("~/.h5"), exist_ok=True)
        _store = {}
    return _store


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def regional(region: str) -> str:
    return requests.get(f"https://{region}.api.example.com/v1/status").text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def fetch_with_curl(url: str) -> str:
    return subprocess.run(f"curl -s {shlex.quote(url)}", shell=True, capture_output=True, text=True).stdout


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def save_note(name: str, body: str) -> str:
    path = os.path.join("/srv/notes", f"{name}-{uuid.uuid4().hex}.txt")
    with open(path, "w") as fh:
        fh.write(body)
    return path


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def summarize(data: str) -> str:
    p = subprocess.Popen(["python3", "summarize.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate(input=data)
    return out


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def count_items() -> str:
    return str(len(_get_store()))


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def ask_ollama(prompt: str) -> str:
    return requests.post("http://ollama:11434/api/generate", json={"prompt": prompt}).text
```

**試験 B**（`server.py`）:

```python
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("h5b")


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def export_new(path: str, body: str) -> str:
    if os.path.exists(path):
        raise FileExistsError(path)
    with open(path, "w") as fh:
        fh.write(body)
    return "ok"
```

**試験 C**（`server.py` と、同じ場所の `settings.py` の 1 行 `DEBUG = False`）:

```python
import os
import tempfile

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

import settings

mcp = FastMCP("h5c")


class AuditLog:
    def add(self, line):
        with open("audit.log", "a") as fh:
            fh.write(line + "\n")


def _collect(items):
    seen = set()
    for it in items:
        seen.add(it)
    return sorted(seen)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def unique(items: list[str]) -> list[str]:
    return _collect(items)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def status() -> str:
    if settings.DEBUG:
        with open("debug.txt", "w") as fh:
            fh.write("status called")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def convert(text: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        return path
    finally:
        os.remove(path)


@mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
def mark_seen(tag: str) -> str:
    path = "seen.txt"
    if os.path.exists(path) and tag in open(path).read().split():
        return "already"
    with open(path, "a") as fh:
        fh.write(tag + "\n")
    return "added"
```

**試験 D**（`server.py`）:

```python
import os
import shlex
import subprocess
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

_index = None


def _get_index():
    global _index
    if _index is None:
        os.makedirs("/var/lib/h5/index", exist_ok=True)
        _index = {}
    return _index


@asynccontextmanager
async def app_lifespan(server):
    _get_index()
    yield {}


mcp = FastMCP("h5d", lifespan=app_lifespan)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lookup(key: str) -> str:
    return str(_get_index().get(key))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def sort_lines(text: str) -> str:
    p = subprocess.Popen(["sort"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate(input=text)
    return out


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def history(ref: str) -> str:
    return subprocess.run(f"git log --oneline {shlex.quote(ref)}", shell=True, capture_output=True, text=True).stdout
```

**試験 E**（`server.py`）:

```python
import os

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("h5e")
API = os.environ.get("NOTES_API", "https://notes.example.com")


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def list_remote() -> str:
    return requests.get(API + "/notes").text
```

解析器の出力（矛 `contradiction:` と不 `contradiction_unknown:` の注記だけを抜き出したもの）:

| 試験 | ツール | site × kind | 注記 |
|---|---|---|---|
| A | `ask_ollama` | `requests.post` × NET | `contradiction_reason:D3:net_external_host` |
| A | `count_items` | `os.makedirs` × FS_WRITE（道筋 `_get_store`） | `contradiction_reason:D1:fs_write` |
| A | `fetch_with_curl` | `subprocess.run` × SPAWN | `contradiction_reason:D3:spawn_model` |
| A | `regional` | `requests.get` × NET | `contradiction_reason:D3:net_model_host` |
| A | `save_note` | `builtins.open` × FS_WRITE | `contradiction_unknown:D2:fs_writeout_model_path_opaque`（矛ではなく不） |
| A | `summarize` | `subprocess.Popen` × SPAWN / `pipe:communicate` × EXEC | 前者は `contradiction_unknown:D1:spawn_command`、後者は `contradiction_reason:D1:exec` |
| B | `export_new` | `builtins.open` × FS_WRITE | `contradiction_reason:D2:fs_writeout_model_path` |
| C | `unique` | `builtins.open` × FS_WRITE（道筋 `_collect -> AuditLog.add`） | `contradiction_reason:D1:fs_write` |
| C | `status` | `builtins.open` × FS_WRITE | `contradiction_reason:D1:fs_write` |
| C | `convert` | `os.remove` × FS_WRITE | `contradiction_reason:D2:fs_remove` |
| C | `mark_seen` | `builtins.open` × FS_WRITE | `contradiction_reason:D4:fs_append` |
| D | `lookup` | `os.makedirs` × FS_WRITE（道筋 `_get_index`） | `contradiction_reason:D1:fs_write` |
| D | `sort_lines` | `subprocess.Popen` × SPAWN / `pipe:communicate` × FS_WRITE | 前者は `contradiction_unknown:D1:spawn_command`、後者は `contradiction_reason:D1:fs_write` |
| D | `history` | `subprocess.run` × SPAWN | `contradiction_reason:D1:spawn_model` |
| E | `list_remote` | `requests.get` × NET | `contradiction_unknown:D3:net_host_unknown`（矛ではなく不） |

表の読み方: 1 行が、解析器が出した 1 つの組です。たとえば 2 行目は「試験 A の `count_items` は、道筋 `_get_store` の中の
`os.makedirs` を、D1（読み取り専用）への矛（理由 `fs_write`）にした」と読みます。どの行を誤にするか・正にするかは、この後の
各節で、手引きの規則を当てて考えます。**これは作った例で、v4 や最終評価のデータではありません。**

---

<a id="ah-5-1"></a>
### H-5.1 第 16 節の前書き — ラベルは何のためか（手引き L406-409）

> 【原文 L406-409】
> ## 16. 書き込み先の種類の付け方
>
> **D1・D2・D4 の正の各件に 1 つだけ**付ける（D67 の 1、D68 の 3）。**重みではない**（どれも違反であることは同じ）。読み手が
> 「見つけた違反は些細では」と問うたときに、事実で答えるための列。D3 の正には付けず、通信先の種類を記録する（16.3）。

**一言で言うと**: 正にした件には、「何を変えた違反か」を表す名前（書き込み先の種類）を **1 つだけ** 付けます。これは重みではなく、
「見つけた違反は些細では」と聞かれたときに事実で答えるための列です。D3 の正には、代わりに「通信先の種類」を付けます。

**ことばの確認**:
- **書き込み先の種類**: 違反が変えたものの置き場所の分類。8 つあります（[H-5.2](#ah-5-2)）。判定表の `write_target` 欄に書きます。
- **ラベル**: ここでは「付けるけれども、判定（正・誤）には効かない印」の意味です。
- **重み**: 違反ごとに「重い・軽い」の点数を付け、精度などの計算に入れること。この研究は、これを**しない**と決めました。
- **正の各件**: 判定で「正」にした組の 1 件ずつ。
- **D67 の 1・D68 の 3**: `docs/decisions.md` の決定の番号と、その中の項目の番号（[第 0 章](ch00.md)の表記のきまり）。
- **通信先の種類**: D3（`openWorldHint: false`）の正に付ける、別の分類。4 つあります（[H-5.12](#ah-5-12)）。

**1 文ずつ読む**:
1. 「**D1・D2・D4 の正の各件に 1 つだけ付ける**」: 読み取り専用（D1）・破壊しない（D2）・冪等（D4）の宣言で正にした組には、必ず
   1 つ、そして 1 つだけ種類を書きます。2 つ書いたり、空にしたりしません。
2. 「**（D67 の 1、D68 の 3）**」: 根拠の決定です。D67 の 1 が「重みを付けずラベルを記録する」を決め、D68 の 3 がラベルを 1 つ
   足し（プロセスの起動・コードの実行）、D3 を別の分類にしました。
3. 「**重みではない（どれも違反であることは同じ）**」: ログへの 1 行の追記でも、利用者のファイルの上書きでも、正は正です。
   精度の計算では、どちらも同じ「正 1 件」です。
4. 「**読み手が『見つけた違反は些細では』と問うたときに、事実で答えるための列**」: 論文を読む人は「その違反の多くはログや
   キャッシュでは？」と思うかもしれません。そのときに「正のうち、ログは何件、利用者のファイルは何件」と、表で答えられるように
   しておく、ということです。
5. 「**D3 の正には付けず、通信先の種類を記録する（16.3）**」: D3 の違反は何かを書き換えることではなく外と通信することなので、
   書き込み先の分類は使いません。同じ `write_target` 欄に、通信先の種類を書きます（`docs/drafts/final_judging_guide_draft.md:442`）。

**なぜこう決めたのか**:
- **重みを付けない理由**は D67 の 1 に 3 つ書かれています（`docs/decisions.md:3767-3772`）。
  1. 研究の問いは「宣言は正しいか」で、「危ないか」ではない（`:3770`）。
  2. 重みの線引きには正解が無く、実世界でも割れている（`:3770-3771`。調べた記録は `docs/incidental_writes_practice.md`）。
  3. v4 の結果を見た後の区別で数字を作り直すと、恣意的に見える（`:3771`）。
  そのうえで、内訳を出すのは「見つけた違反は些細では」という問いに事実で答えるため、と書いています（`:3772`）。
- **ラベルを 1 つ足し、D3 を分けた理由**は D68 の 3 です（`docs/decisions.md:3809-3814`）。「その他・不明」に入れると、任意の
  コマンドを実行できる違反が、分類できなかったものと同じ箱に入って見えなくなる（`:3812`）。D3 の違反は書き込みではなく外部との
  通信なので、書き込み先の種類が当てはまらない（`:3813`）。ラベルを足したのは最終評価のデータを見る前なので、結果に合わせた
  変更ではない（`:3814`）。
- この決定の前の経緯（v4 では正に「本来の動作 / 裏側・補助」の重大度の列を付けていた。O44）は `docs/open_questions.md:1227-1250` と
  [第 43 章](ch43.md#s43-11)にあります。
- 「1 つだけ」の理由は、手引きにも決定にも書かれていません。本書の読み: 1 件に 1 つなら、内訳の表の合計が正の件数と一致し、
  読み手がそのまま割合として読めます。

**例で確かめる**:

（作った例）同じ「読み取り専用」のツールで、正になる 2 つの違反を並べます。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(query: str) -> str:
    with open("activity.log", "a") as fh:      # (1) 記録のためだけの追記
        fh.write(f"search {query}\n")
    return do_search(query)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def render(doc_path: str) -> str:
    html = to_html(doc_path)
    with open(doc_path, "w") as fh:            # (2) モデルが指定した文書を上書き
        fh.write(html)
    return html
```

- (1) も (2) も、D1 の問い「呼び出しの後に残る何かを変えるか」に「はい」なので、どちらも**正**です
  （`docs/drafts/final_judging_guide_draft.md:318`。ログも含む）。
- ラベルだけが違います。(1) は「ログ」（[H-5.6](#ah-5-6)）、(2) は「利用者のファイル」（[H-5.5](#ah-5-5)）。
- 「(1) は軽いから誤にしよう」はできません。手引きの 11.3 節が「軽重は書き込み先の種類のラベルで表し、判定の正誤には持ち込まない」
  と書いています（`docs/drafts/final_judging_guide_draft.md:63-64`）。

**迷いやすいところ**:
- **ラベルを付ける対象**: この前書きは「正の各件」と書きますが、見落としで見つけた違反（18.2 の 7、`docs/drafts/final_judging_guide_draft.md:499`）
  と、不の中身で「違反」にしたもの（18A.2 の 5、`:556`）にも同じラベルを付けます。D68 の 3 の文も「D1・D2・D4 の正と見落としに付ける」
  です（`docs/decisions.md:3810`）。この前書きだけを読んで「正だけ」と思わないでください。
- **誤と不明にはラベルを付けない**: 誤には `error_class`（[H-5.17](#ah-5-17)）、不明には `unknown_reason` を書きます。
- **ラベルを先に考えない**: 先にラベルを考えると「ログだから軽い」という気持ちが判定に入りやすくなります。判定を決めた**後**に付けます
  （[第 51 章](ch51.md#s51-2)）。

**承認の前に自分に問うこと**:
1. ログ 1 行の追記を「正」と数えることに、自分は納得しているか。納得していないなら、それは原理（1-i-b）の問題で、ラベルでは
   直せないことを分かっているか。
2. 「重みは付けない、ラベルで内訳を出す」という形で、読み手の「些細では」という問いに十分に答えられると思うか。
3. 1 件に 1 つだけ、という制約で困る形を思いつくか（[H-5.11](#ah-5-11) の【穴 H-5-7】を見てから答える）。

**この節で手引きが決めていないこと**: 見つからなかった（1 組に種類の違う位置が複数あるときの選び方は、16.2 の 1 行目に関わるので
[H-5.11](#ah-5-11) で挙げます）。

---

<a id="ah-5-2"></a>
### H-5.2 16.1 種類と定義 — 上から順に当てはめる（手引き L411-416）

> 【原文 L411-416】
> ### 16.1 種類と定義
>
> **上から順に当てはめ、最初に当てはまったものを付ける。**
>
> | 順 | 種類 | 定義 | 例 |
> |---|---|---|---|

**一言で言うと**: 書き込み先の種類は 8 つあり、表の**上から順に**「当てはまるか」を見て、**最初に当てはまったもの**を付けます。
1 つの書き込みが 2 つの定義に当てはまっても、これで必ず 1 つに決まります。

**ことばの確認**:
- **順**: 表の左の列の 1〜8。当てはめる順番で、重さの順ではありません。
- **定義**: その種類に入る条件。種類の名前ではなく、この条件で決めます。
- **例**: その種類に入る典型。例は定義を言い換えたものではなく、定義に当てはまる代表です。

**1 文ずつ読む**:
1. 「**### 16.1 種類と定義**」: この小節の見出しです。手順書の版では「（下書き）」が付いていましたが、手引きでは外しました
   （`docs/drafts/final_judging_guide_draft.md:12`）。
2. 「**上から順に当てはめ、最初に当てはまったものを付ける。**」: 順 1 から順に「定義に当てはまるか」を問い、「はい」になった最初の
   種類で止めます。下の種類にも当てはまっていても、見ません。
3. 表の見出し「**順 / 種類 / 定義 / 例**」: 各行は、この 4 つの欄でできています。

**なぜこう決めたのか**: 順番を決めた**理由は、手引きにも決定にも書かれていません**。D67 の 1 はラベルの名前を並べただけで、その並び
（利用者のファイルが先頭）は手引きの表の並び（相手側の状態が先頭）と違います（`docs/decisions.md:3769`）。順番の規則が最初に
現れたのは手順書の第 2 版（コミット ffca5a7、2026-09-30。`docs/final_evaluation_procedure.md:1093`）で、本記録者が書いたものです。
本書の読み（[第 51 章](ch51.md#s51-4)と同じ）: (1) 1 件に 1 つだけ付けるには、重なったときの決め方が要る。(2) 判定者が 1 人なので
（D67 の 4）、その日の印象で選ぶとぶれる。(3) 上から順だと、たとえば「データベース」が「DB を変えた違反の全部」を意味するように
なり、読み手が表を読みやすい。
なお、7 番（プロセスの起動・コードの実行）が 8 番（その他・不明）の前にある理由だけは、D68 の 3 に書かれています（[H-5.9](#ah-5-9)）。

**例で確かめる**:

（作った例）キャッシュとして SQLite の DB に書くツール。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def geocode(address: str) -> str:
    db = sqlite3.connect(os.path.expanduser("~/.geo/cache.db"))
    row = db.execute("SELECT result FROM cache WHERE q = ?", (address,)).fetchone()
    if row:
        return row[0]
    result = call_geocoder(address)
    db.execute("INSERT INTO cache VALUES (?, ?)", (address, result))
    db.commit()
    return result
```

- 順 1（相手側の状態）: NET の効果ではないので当てはまらない。
- 順 2（データベース）: `INSERT` で DB の行を変えるので**当てはまる** → ここで止める。**データベース**。
- 順 6（キャッシュ・状態の保存）にも当てはまります（後で読み返す）が、見ません。16.2 の境界の例の最後の行と同じ答えです
  （`docs/drafts/final_judging_guide_draft.md:435`）。

**迷いやすいところ**:
- **下から（思いついた種類から）付ける**: 「キャッシュだから 6」と先に決めると、上の 1〜3 に当たるものを見落とします。必ず 1 から問います。
- **順番を重さと読む**: 1 番の相手側の状態が一番重い、という意味ではありません（重みは付けない。[H-5.1](#ah-5-1)）。
- **2 つ書く**: `write_target` には 1 つだけ。もう 1 つの見方は `note` に書きます。

**承認の前に自分に問うこと**:
1. 自分なら、SQLite のキャッシュ DB への書き込みを「データベース」と「キャッシュ」のどちらと呼びたいか。手引きの順番の答え
   （データベース）と違うなら、順番を変えたいか、それとも順番どおりでよいか。
2. 理由の書かれていない順番を、そのまま承認してよいか。理由を一言、手引きか決定に足したいか。

**この節で手引きが決めていないこと**: 順番そのものは決まっています。順番の**理由**が書かれていないことは穴ではありません
（規則として決まっている）が、承認のときの確認点です。個々の種類の定義の重なりで決まらない形は、各種類の節で挙げます。

---

<a id="ah-5-3"></a>
### H-5.3 順 1「相手側の状態」（手引き L417）

> 【原文 L417】
> | 1 | **相手側の状態** | NET の効果で、通信相手のサーバの状態を変える | Jira の課題の更新、Slack への投稿 |

**一言で言うと**: 通信（NET）で、相手のサーバの中身を変える違反です。自分のマシンには何も残らなくても、相手の側が変わります。

**ことばの確認**:
- **NET の効果**: HTTP などの通信の効果（kind が `NET`）。
- **通信相手のサーバの状態**: 相手のサービスに残るもの（課題・投稿・ファイル・設定など）。
- **Jira**: 課題（作業の項目）を管理するサービス。**Slack**: チャットのサービス。

**1 文ずつ読む**（表の 1 行目）:
- 種類「**相手側の状態**」。
- 定義「**NET の効果で、通信相手のサーバの状態を変える**」: 2 つの条件があります。(a) kind が NET であること。(b) 相手の状態を
  変えること。相手の状態を変えない通信（検索の `GET` など）は、そもそも D1・D2 の正になりません（`docs/drafts/final_judging_guide_draft.md:327`）。
- 例「**Jira の課題の更新、Slack への投稿**」: 課題が書き換わる・メッセージが増える、という相手側の変化です。

**なぜこう決めたのか**: 採った原理 1-ii-b（相手側の状態を変えることも「環境の変更」）があるので、通信だけの違反が正になります
（`docs/contradiction_principles.md:55-56`、手引き 11.3 の表 `docs/drafts/final_judging_guide_draft.md:71`）。その正を、ホストの
ファイルの違反と区別して数えるための種類です。手引きはこれを 1 番に置いた理由を書いていません（[H-5.2](#ah-5-2)）。

**例で確かめる**:

（作った例 1。当てはまる）D1 で、課題の状態を `PUT` で変える。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def triage(issue_key: str) -> str:
    requests.put(f"https://jira.example.com/rest/api/2/issue/{issue_key}",
                 json={"fields": {"labels": ["triaged"]}})
    return "ok"
```

`PUT` は D1 に反します（`docs/drafts/final_judging_guide_draft.md:325`）。正で、NET の効果で相手の課題を変えるので**相手側の状態**。
解析器は D1 の `PUT` に `net_modify` を出します（`authgap/dparse.py:387-388`）。

（作った例 2。当てはまる）D2 で、相手のファイルを `DELETE` で消す。

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def tidy(file_id: str) -> str:
    httpx.delete(f"https://files.example.com/api/files/{file_id}")
    return "deleted"
```

`DELETE` は既存のものを消すので D2 に反します（`docs/drafts/final_judging_guide_draft.md:343`）。種類は**相手側の状態**。

（作った例 3。境界）D1 で、記録をログ収集サービスへ `PUT` で送る。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lookup(sym: str) -> str:
    requests.put("https://logs.example.com/ingest/lookup", json={"sym": sym, "ts": time.time()})
    return quote_of(sym)
```

目的は「ログ」（順 4 の「記録のためだけに書き」）ですが、上から順に当てると、順 1 の「NET の効果で相手の状態を変える」が先に
当たります。**相手側の状態**（16.1 の順番の規則、`docs/drafts/final_judging_guide_draft.md:413`）。[第 51 章](ch51.md#s51-4)の表の
3 行目と同じ答えです。

**迷いやすいところ**:
- **DB の相手が遠くにあっても、kind が DB なら順 1 ではない**: たとえば別のマシンの PostgreSQL への `UPDATE` は、kind が `DB` なので
  順 1 の「NET の効果で」に当たらず、順 2 のデータベースです（本書の読み。定義の「NET の効果で」をそのまま当てた）。
- **`POST` の正**: 解析器は `POST` を不にします（`authgap/dparse.py:389-390`）。不の中身の判定で、人が相手の API を調べて「違反」に
  したときにも、この種類を付けます（`docs/drafts/final_judging_guide_draft.md:556`）。
- **プロセスを起動して通信する**（`subprocess.run(["curl", "-X", "DELETE", ...])`）: kind は `SPAWN` で、順 1 の「NET の効果で」に
  当たりません。[H-5.9](#ah-5-9) を見てください。

**承認の前に自分に問うこと**:
1. 「NET の効果で」という条件があるため、`curl` で相手を変える形は順 1 に入りません。それでよいか。
2. ログ収集サービスへの送信を「相手側の状態」と呼ぶことに違和感はないか。違和感があっても、順番の規則で決まることを受け入れるか。

**この節で手引きが決めていないこと**: 見つからなかった（プロセス経由の通信は [H-5.9](#ah-5-9) の【穴 H-5-2】で扱う）。

---

<a id="ah-5-4"></a>
### H-5.4 順 2「データベース」（手引き L418）

> 【原文 L418】
> | 2 | **データベース** | DB の行・スキーマ・DB に残る設定を変える | `UPDATE sessions SET revoked_at …`、`PRAGMA journal_mode=WAL` |

**一言で言うと**: DB の中身（行）、作り（スキーマ）、DB のファイルに残る設定を変える違反です。

**ことばの確認**:
- **行**: 表の 1 件のデータ。`INSERT`（足す）・`UPDATE`（変える）・`DELETE`（消す）で変わります。
- **スキーマ**: 表の作り。`CREATE` / `ALTER` / `DROP` で変わります。
- **DB に残る設定**: `PRAGMA journal_mode=WAL` のように、DB のファイルに記録されて、接続を閉じても残る設定。接続を閉じれば消える
  設定（`PRAGMA foreign_keys=ON` など）は違反にならないので、ここにも来ません（`docs/drafts/final_judging_guide_draft.md:323`）。

**1 文ずつ読む**（表の 2 行目）:
- 種類「**データベース**」。
- 定義「**DB の行・スキーマ・DB に残る設定を変える**」: 3 つのどれかを変えれば当てはまります。「kind が DB であること」は
  定義に書かれていません（[H-5.9](#ah-5-9) の【穴 H-5-2】に関わる）。
- 例「**`UPDATE sessions SET revoked_at …`、`PRAGMA journal_mode=WAL`**」: 前者は行の変更（v4 の M00 と同じ形。
  `docs/drafts/final_judging_guide_draft.md:676`）、後者は残る設定の変更です。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧にあります（`docs/decisions.md:3769`）。残る設定まで入れるのは、原理 1-i-b
（呼び出しを越えて残るものはすべて環境。接続単位だけ除く）を採ったからです（`docs/contradiction_principles.md:49`）。
解析器も、残る設定を D1 の矛（`db_persistent`）にします（`authgap/dparse.py:382`、`:495-496`）。

**例で確かめる**:

（作った例 1。当てはまる）D2 で、既存の行を消す。

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def logout(session_id: str) -> str:
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    return "bye"
```

`DELETE` は既存の行を消すので D2 に反し、正。行を変えるので**データベース**。

（作った例 2。当てはまる）D1 で、DB を開くたびに WAL に切り替える。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def stats() -> str:
    conn = sqlite3.connect("app.db")
    conn.execute("PRAGMA journal_mode=WAL")
    return str(conn.execute("SELECT count(*) FROM items").fetchone())
```

`journal_mode` は DB のファイルに残る設定なので D1 に反し（`docs/drafts/final_judging_guide_draft.md:322`）、正。**データベース**。

（作った例 3。境界）D1 で、監査の記録を DB の表に足す。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_report(report_id: str) -> str:
    conn.execute("INSERT INTO audit(at, what) VALUES (datetime('now'), ?)", (report_id,))
    conn.commit()
    return load_report(report_id)
```

目的は記録（順 4 のログ）ですが、上から順に当てると、順 2 の「DB の行を変える」が先に当たります。**データベース**
（16.1 の順番の規則）。16.2 の「SQLite のキャッシュ DB → データベース。順 2 が順 6 より先」と同じ考え方です
（`docs/drafts/final_judging_guide_draft.md:435`）。

**迷いやすいところ**:
- **利用者の DB**: 利用者のメモを入れた DB を上書きしても、順 3（利用者のファイル）より順 2 が先なので**データベース**です。
  「利用者のデータだから 3」とはしません（順番の規則）。
- **接続単位の設定・トランザクション**: `BEGIN` / `COMMIT` / `PRAGMA foreign_keys=ON` は D1 に反しない（`docs/drafts/final_judging_guide_draft.md:323`）
  ので、正にならず、ラベルも付きません。

**承認の前に自分に問うこと**:
1. 監査の記録を DB に書くのを「データベース」と呼ぶことに納得するか（読み手は「データベース」の行を見て、本来のデータの変更だと
   思うかもしれない）。
2. 利用者のノートが DB に入っているとき、その上書きを「利用者のファイル」でなく「データベース」に数えてよいか。

**この節で手引きが決めていないこと**: 見つからなかった（kind が DB でない書き込みが DB を変える形は【穴 H-5-2】で扱う）。

---

<a id="ah-5-5"></a>
### H-5.5 順 3「利用者のファイル」（手引き L419）

> 【原文 L419】
> | 3 | **利用者のファイル** | 利用者（またはモデル）が指定した場所のファイル、または利用者の文書・データとして扱われるファイル | モデルが決めた `output_file` へのレポートの書き出し、編集対象のファイルの上書き |

**一言で言うと**: 使う人（またはその代わりのモデル）が「ここに」と指定したファイルか、使う人の文書・データとして扱われるファイルへの
書き込みです。

**ことばの確認**:
- **利用者**: ツールを使う人。MCP では、利用者の代わりにモデル（AI）が引数を決めることが多いので「（またはモデル）」と書いてあります。
- **指定した場所**: 引数などで、書き先のパスを決めたこと。
- **文書・データとして扱われるファイル**: 利用者のノート、編集対象のソース、利用者のエクスポートの置き場など。
- **運用者**: サーバを動かす人（環境変数や設定ファイルを決める人）。手引きはこの言葉を 14.3・15.3 で使いますが、この定義の中には
  出てきません。

**1 文ずつ読む**（表の 3 行目）:
- 種類「**利用者のファイル**」。
- 定義の前半「**利用者（またはモデル）が指定した場所のファイル**」: 書き先を決めたのが利用者かモデルなら当てはまる。
- 定義の後半「**または利用者の文書・データとして扱われるファイル**」: 場所を指定していなくても、そのファイルが利用者の文書やデータ
  なら当てはまる。
- 例「**モデルが決めた `output_file` へのレポートの書き出し**」は前半、「**編集対象のファイルの上書き**」は後半（または両方）の例です。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧の先頭にあります（`docs/decisions.md:3769`）。定義の文の理由は書かれていません。
本書の読み: D2 の原理 3-a（モデルが書き先を決められるなら、既存のファイルを指して上書きできる。`docs/drafts/final_judging_guide_draft.md:344`）
で正になる件が、ここに集まります。読み手にとって「利用者の持ち物に触れた違反」は区別して数えたいもの、という読みです。

**例で確かめる**:

（作った例 1。当てはまる。前半）

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def export_csv(output_file: str, query: str) -> str:
    rows = run_query(query)
    with open(output_file, "w") as fh:
        csv.writer(fh).writerows(rows)
    return output_file
```

書き先 `output_file` をモデルが決めるので D2 に反し、正（原理 3-a）。**利用者のファイル**。手引き 20.1 の組 2 と同じ形です
（`docs/drafts/final_judging_guide_draft.md:666`）。

（作った例 2。当てはまる。後半）

```python
NOTES_DIR = Path.home() / "Notes"

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def tag_note(title: str, tag: str) -> str:
    p = NOTES_DIR / f"{title}.md"
    p.write_text(p.read_text() + f"\n#{tag}\n")
    return "tagged"
```

書き先の置き場 `~/Notes` は定数ですが、中のファイルは利用者のノート（文書）です。D1 に反し正。**利用者のファイル**（定義の後半）。

（作った例 3。境界）モデルが決めたパスにログを追記する。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def check(url: str, log_to: str = "check.log") -> str:
    status = probe(url)
    with open(log_to, "a") as fh:
        fh.write(f"{url} {status}\n")
    return status
```

目的はログ（順 4）ですが、書き先 `log_to` をモデルが決めるので、順 3 の前半が先に当たります。**利用者のファイル**
（16.1 の順番の規則。[第 51 章](ch51.md#s51-4)の表の 4 行目と同じ答え）。

**迷いやすいところ**:
- **「モデルが書き先に影響する」と「モデルが書き先を指定する」**: 手引き 20.1 の組 1 は、書き先のファイル名がモデルの `query` から
  作られますが、手引きは「その他・不明」にしています（`docs/drafts/final_judging_guide_draft.md:652-655`）。名前の一部がモデルの値でも、
  置き場（`~/.demo_cache`）はツールのものなので「利用者が指定した場所」とは読まなかった、と本書は読みます。
- **利用者の DB**: 順 2 が先です（[H-5.4](#ah-5-4)）。

**承認の前に自分に問うこと**:
1. 書き先のパスの一部（ファイル名だけ）をモデルが決める形を、「利用者が指定した場所」に入れるか。手引き 20.1 の組 1 の答え
   （その他・不明）と合っているか。
2. 運用者が環境変数で決めた場所への書き込みを、自分は「利用者のファイル」と呼ぶか（下の【穴 H-5-3】）。

**この節で手引きが決めていないこと**:

【穴 H-5-3】**運用者が環境変数や設定ファイルで決めた場所への書き込みは「利用者が指定した場所」か**
- 何が決まっていないか: 定義は「利用者（またはモデル）が指定した場所」と書きますが、運用者が決めた場所を含むかを書いていません。
  手元で動かす MCP サーバ（stdio）では、利用者と運用者が同じ人であることが多く、区別があいまいです。
- 困る事例（作った例）:

  ```python
  EXPORT_DIR = os.environ.get("NOTES_EXPORT_DIR", "~/notes-export")

  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
  def snapshot() -> str:
      path = os.path.join(os.path.expanduser(EXPORT_DIR), "snapshot.json")
      Path(path).write_text(json.dumps(load_all()))
      return path
  ```

  書き出し先は運用者の環境変数で決まり、中身は利用者のノートの写しです。順 3 の前半（指定した場所）に当たるか、後半（利用者のデータ）
  に当たるか、どちらにも当たらず順 6 や順 8 か、で分かれます。
- 考えられる選択肢: (a) 運用者も「利用者」に含める（順 3）。(b) 運用者の設定は含めず、中身で決める（利用者のデータの写しなら後半で順 3、
  そうでなければ下へ）。(c) 決められないとして順 8（その他・不明）と `note`。
- 関係する決定: D67 の 1（`docs/decisions.md:3767-3772`）。条件の種類の「運用者の設定」（14.3、`docs/drafts/final_judging_guide_draft.md:262`）
  は到達の話で、ラベルの話ではありません。

---

<a id="ah-5-6"></a>
### H-5.6 順 4「ログ」（手引き L420）

> 【原文 L420】
> | 4 | **ログ** | 記録のためだけに書き、ツールの動作では読み返さない | ログファイル・監査ログ・トレースへの追記 |

**一言で言うと**: 「いつ・何をした」を残すためだけに書き、ツール自身はそれを読み返さない書き込みです。

**ことばの確認**:
- **監査ログ**: 誰が何をしたかの記録。**トレース**: 処理の流れを追うための記録。
- **読み返す**: 書いたファイルを、ツールの処理の中で開いて読むこと。

**1 文ずつ読む**（表の 4 行目）:
- 種類「**ログ**」。
- 定義「**記録のためだけに書き、ツールの動作では読み返さない**」: 2 つの条件の両方が要ります。(a) 記録のためだけ。(b) ツールの動作では
  読み返さない。読み返すなら、順 6（キャッシュ・状態の保存）の側です。
- 例「**ログファイル・監査ログ・トレースへの追記**」。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧にあります（`docs/decisions.md:3769`）。v4 では、正の多くが「裏側・補助」の書き込み
（ログ・キャッシュ・一時ファイルなど）だったことが、この種類を分けて数える動機です（`docs/open_questions.md:1221-1222`、O43 の
読み方の注意。件数は v4 の本記録者の判定で、論文には使わない。D66 の 5）。

**例で確かめる**:

（作った例 1。当てはまる）`logging` の出力先がファイル。

```python
logging.basicConfig(filename="server.log", level=logging.INFO)
log = logging.getLogger(__name__)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def price(sym: str) -> str:
    log.info("price %s", sym)
    return fetch_price(sym)
```

出力先がファイルなので D1 に反します（`docs/drafts/final_judging_guide_draft.md:332`）。記録のためだけで、読み返さないので**ログ**。
なお、解析器は `logging` の出力をふつう効果として出さないので、この形は見落としの判定で出会うことが多いはずです（本書の読み。
v4 の R19 は loguru の `logger.add` が語彙に無い見落としだった。`docs/drafts/final_judging_guide_draft.md:685`）。

（作った例 2。当てはまる）活動ログへの追記（v4 の wikimind の形）。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wiki_ask(q: str) -> str:
    Path("wiki/log.md").open("a").write(f"- {datetime.now():%F %T} ask: {q}\n")
    return answer(q)
```

16.2 の境界の例「活動ログ `log.md` への追記 → ログ（読み返さない）」と同じです（`docs/drafts/final_judging_guide_draft.md:433`）。

（作った例 3。境界）ログを書き、同じツールがそれを読み返して「前回の結果」を返す。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def last_check(url: str) -> str:
    prev = Path("checks.log").read_text().splitlines()[-1:] if Path("checks.log").exists() else []
    status = probe(url)
    with open("checks.log", "a") as fh:
        fh.write(f"{url} {status}\n")
    return f"now {status}, before {prev}"
```

名前は「ログ」でも、ツールの動作で読み返しているので、順 4 の (b) に当たりません。順 5 にも当たらず、順 6 の「ツールの動作の
ために自分で保存し、後で読み返す」に当たります。**キャッシュ・状態の保存**（定義の (b) と順番の規則）。

**迷いやすいところ**:
- **標準出力・標準エラーへのログ**: ファイルではないので D1 に反せず（`docs/drafts/final_judging_guide_draft.md:332`）、正にならないので
  ラベルも付きません。
- **名前で決めない**: ファイル名が `.log` でも、読み返していればログではありません。手引き 20.1 の組 1 の「名前ではなく動作で決める」
  （`docs/drafts/final_judging_guide_draft.md:655`）と同じ考え方です。
- **読み返しは grep で確かめる**: 「読み返さない」は「無いこと」の確認なので、そのファイル名やパスの変数で木の中を検索してから
  決めます（手引き 20.1 の組 1 が「読み返しが木のどこにも無いことを grep で確かめた」と書いている。`:653-654`）。

**承認の前に自分に問うこと**:
1. 別のツール（たとえば `show_logs`）がそのログを読んで利用者に見せるとき、それは「ツールの動作で読み返す」に当たると思うか
   （下の【穴 H-5-4】）。
2. ログの出力先を運用者が環境変数で選べる（ファイルにも標準エラーにもできる）とき、正にするか、ラベルは何か（到達の条件の種類は
   14.3 の「運用者の設定」）。

**この節で手引きが決めていないこと**:

【穴 H-5-4】**「読み返す」「読み返さない」の主語は、そのツールか、同じサーバの別のツールも含むか**
- 何が決まっていないか: 順 4 は「ツールの動作では読み返さない」、順 6 は「ツールの動作のために自分で保存し、後で読み返す」と書きます。
  「ツール」が判定している組のツール 1 つなのか、同じサーバのツールすべてなのかが書かれていません。
- 困る事例（作った例）:

  ```python
  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
  def search(q: str) -> str:
      with open("history.jsonl", "a") as fh:
          fh.write(json.dumps({"q": q}) + "\n")
      return do_search(q)

  @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
  def recent_searches() -> str:
      return Path("history.jsonl").read_text()
  ```

  `search` は履歴を読み返しませんが、`recent_searches` が読みます。`search` の正のラベルは、ログ（そのツールは読み返さない）か、
  キャッシュ・状態の保存（サーバの中で読み返す）か、利用者のデータ（検索履歴は利用者に見せるデータ）か。
- 考えられる選択肢: (a) 主語は判定しているツールだけ（→ ログ）。(b) 同じサーバのどのツールでも読み返せば順 6。(c) 決められないとして順 8 と `note`。
- 関係する決定: D67 の 1。手引き 20.1 の組 1 の grep は「木のどこにも無いこと」を確かめています（`docs/drafts/final_judging_guide_draft.md:653-654`）。
  これは (b) の読みに近い、とも読めます（本書の読み）。

---

<a id="ah-5-7"></a>
### H-5.7 順 5「一時ファイル」（手引き L421）

> 【原文 L421】
> | 5 | **一時ファイル** | 同じ呼び出しの中で作って消す、または OS の一時領域（`tempfile`、`/tmp`）に作る | `mkstemp` した受け渡し用のファイルとその削除 |

**一言で言うと**: その呼び出しの中で作ってすぐ消すファイルか、OS の一時置き場に作るファイルです。

**ことばの確認**:
- **同じ呼び出しの中**: ツールが 1 回呼ばれて、結果を返すまでのあいだ。
- **OS の一時領域**: OS が「一時ファイルの置き場」として用意した場所。Python の `tempfile` が使う場所や `/tmp`。
- **`mkstemp`**: `tempfile.mkstemp`。一時領域に、ほかと重ならない名前の新しいファイルを作る関数（[第 9 章](ch09.md)）。
- **受け渡し用のファイル**: 別のプログラムにデータを渡すためだけに作るファイル。

**1 文ずつ読む**（表の 5 行目）:
- 種類「**一時ファイル**」。
- 定義の前半「**同じ呼び出しの中で作って消す**」: 置き場所はどこでもよい。
- 「**または**」: 2 つのどちらか 1 つで当てはまります。
- 定義の後半「**OS の一時領域（`tempfile`、`/tmp`）に作る**」: 消さなくても当てはまる。
- 例「**`mkstemp` した受け渡し用のファイルとその削除**」: 前半と後半の両方に当たる典型。v4 の ru-marketplace（M58）の形です
  （`docs/drafts/final_judging_guide_draft.md:679`）。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧にあります（`docs/decisions.md:3769`）。定義の文の理由は書かれていません。
なお、同じ呼び出しで作って消す形は、D1 では正（`docs/drafts/final_judging_guide_draft.md:318`、`:679`）、D2 では誤（E2。
`:351-353`）です。ラベルの「一時ファイル」は、D1（と D4）の正で使われることが多いはずです（本書の読み）。

**例で確かめる**:

（作った例 1。当てはまる。前半と後半）D1 で、変換のために一時ファイルを作って消す。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def to_pdf(markdown: str) -> str:
    fd, src = tempfile.mkstemp(suffix=".md")
    try:
        os.write(fd, markdown.encode())
        os.close(fd)
        return run_pandoc(src)
    finally:
        os.remove(src)
```

D1 では作成も削除も環境の変更なので正（`docs/drafts/final_judging_guide_draft.md:318`）。**一時ファイル**。

（作った例 2。当てはまる。前半だけ）作業ディレクトリの中に作って、同じ呼び出しで消す。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lint(code: str) -> str:
    p = Path("work") / f"{uuid.uuid4().hex}.py"
    p.write_text(code)
    try:
        return run_linter(p)
    finally:
        p.unlink()
```

置き場は OS の一時領域ではありませんが、同じ呼び出しで作って消すので**一時ファイル**（定義の前半）。

（作った例 3。境界）`/tmp` に置いて、次の呼び出しで読み返す。

```python
CACHE = Path("/tmp/weather_cache.json")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def weather(city: str) -> str:
    data = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if city not in data:
        data[city] = fetch(city)
        CACHE.write_text(json.dumps(data))
    return data[city]
```

使い方はキャッシュそのもの（順 6）ですが、定義と順番をそのまま当てると、順 5 の後半「OS の一時領域に作る」が先に当たり、
**一時ファイル**になります（16.1 の順番の規則）。[第 51 章](ch51.md#s51-6)が未決の境界の 2 として挙げた形です。

**迷いやすいところ**:
- **D2 の誤との取り違え**: 同じ呼び出しで作って消す形は、D2 では「前からあったものではない」ので反しない（誤、E2）。ラベルの話では
  ありません。D1 で正にしたときにだけ、この種類を付けます。
- **「前の呼び出しが残したもの」を消す**: 同じ呼び出しで作ったものではないので、前半には当たりません（[H-5.11](#ah-5-11) の【穴 H-5-7】）。

**承認の前に自分に問うこと**:
1. `/tmp` に置いたキャッシュを「一時ファイル」と数えることに納得するか。それとも「後で読み返すなら順 6」と、順番より使い方を優先したいか。
2. 「OS の一時領域」の範囲を、自分はどこまでと考えるか（`$TMPDIR` で変えた場所、`/var/tmp`、`mkstemp(dir=".")` で作ったファイル）。

**この節で手引きが決めていないこと**:

【穴 H-5-5】**OS の一時領域に置き、後で読み返すもの（順 5 と順 6）と、「OS の一時領域」の範囲**
- 何が決まっていないか: (i) 上の作った例 3 のように、`/tmp` に置いて次の呼び出しで読み返すものは、順番どおりなら順 5 ですが、16.2 の
  境界の例に無く、手引きがそれを意図したかが分かりません（[第 51 章](ch51.md#s51-6) の未決の 2 と同じ）。(ii)「OS の一時領域」が
  `tempfile` と `/tmp` の 2 つの例でしか示されていません。`tempfile.mkstemp(dir="./work")`（一時ファイルの関数だが置き場は作業ディレクトリ）、
  `/var/tmp`（再起動でも消えない一時領域）、環境変数 `TMPDIR` で変えた場所が、入るかが分かりません。
- 困る事例: 上の作った例 3。もう 1 つ（作った例）: `tempfile.NamedTemporaryFile(dir=os.path.expanduser("~/.app"), delete=False)` で
  作り、消さずに次の呼び出しで読み返す。
- 考えられる選択肢: (a) 順番どおり（場所が一時領域なら順 5）。(b) 「後で読み返す」なら順 6 を先にする例外を 16.2 に足す。
  (c) 一時領域の範囲を「`tempfile` の関数で作ったもの」か「`/tmp` 以下」かのどちらかに決める。
- 関係する決定: D67 の 1。

---

<a id="ah-5-8"></a>
### H-5.8 順 6「キャッシュ・状態の保存」（手引き L422）

> 【原文 L422】
> | 6 | **キャッシュ・状態の保存** | ツールの動作のために自分で保存し、後で読み返す | キャッシュ、トークン・セッションの保存、索引、初回に作る作業ディレクトリ・設定ファイル |

**一言で言うと**: ツールが自分の仕事のために保存し、後でまた読むものです。

**ことばの確認**:
- **キャッシュ**: 同じ問い合わせを速く返すために、前の結果を取っておくもの。
- **トークン・セッション**: ログインの証明。保存しておけば、次の呼び出しでログインし直さずに済みます。
- **索引**: 検索を速くするための表。
- **作業ディレクトリ・設定ファイル**: ツールが自分の置き場として作るディレクトリや、自分の設定を書いたファイル。

**1 文ずつ読む**（表の 6 行目）:
- 種類「**キャッシュ・状態の保存**」。
- 定義「**ツールの動作のために自分で保存し、後で読み返す**」: 3 つの条件があります。(a) ツールの動作のため。(b) 自分で保存する
  （利用者が指定した場所ではない）。(c) 後で読み返す。
- 例「**キャッシュ、トークン・セッションの保存、索引、初回に作る作業ディレクトリ・設定ファイル**」: 最後の「初回に作る作業ディレクトリ」は、
  ディレクトリ自体は「読み返す」ものではないので、(c) とどう合わせるかで迷います（下の【穴 H-5-6】）。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧にあります（`docs/decisions.md:3769`）。v4 の正の多くがこの類（初回の初期化・
キャッシュ・トークンの保存など）だったことが背景です（`docs/open_questions.md:1221-1222`。v4 は本記録者の判定で、数は論文に使わない）。

**例で確かめる**:

（作った例 1。当てはまる）OAuth のトークンをファイルに保存して、次の呼び出しで読む。

```python
TOKEN = Path.home() / ".myapp" / "token.json"

def _token():
    if TOKEN.exists():
        return json.loads(TOKEN.read_text())
    t = login()
    TOKEN.parent.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(json.dumps(t))
    return t

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_events() -> str:
    return api_get("/events", token=_token())
```

16.2 の「OAuth のトークンをファイルに保存 → キャッシュ・状態の保存（後で読み返す）」と同じです（`docs/drafts/final_judging_guide_draft.md:431`）。

（作った例 2。当てはまる）検索の索引を作って保存し、次から使う。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def find(term: str) -> str:
    idx_path = Path(".index/terms.pkl")
    if idx_path.exists():
        idx = pickle.loads(idx_path.read_bytes())
    else:
        idx = build_index()
        idx_path.parent.mkdir(exist_ok=True)
        idx_path.write_bytes(pickle.dumps(idx))
    return ", ".join(idx.get(term, []))
```

自分で保存し、次の呼び出しで読み返すので**キャッシュ・状態の保存**。

（作った例 3。境界）名前はキャッシュだが、読み返さない。手引き 20.1 の組 1 そのものです。

```python
CACHE_DIR = os.path.expanduser("~/.demo_cache")

def _save_cache(name, text):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(os.path.join(CACHE_DIR, name), "w") as fh:
        fh.write(text)
```

手引きは、読み返しが木のどこにも無いことを grep で確かめたうえで、**その他・不明**とし、`note` に「キャッシュの名前だが読み返しが無い」と
書く、としています（`docs/drafts/final_judging_guide_draft.md:652-655`）。定義の (c) に当たらないからです。

**迷いやすいところ**:
- **SQLite のキャッシュ DB**: 順 2 が先なので**データベース**（`docs/drafts/final_judging_guide_draft.md:435`。[H-5.2](#ah-5-2)）。
- **`/tmp` のキャッシュ**: 順 5 が先（[H-5.7](#ah-5-7) の【穴 H-5-5】）。
- **初回だけ作るディレクトリ**: 16.2 は「初回だけ `~/.app/` を作る → キャッシュ・状態の保存（作業ディレクトリ）」と決めています
  （`docs/drafts/final_judging_guide_draft.md:432`）。けれども、その中のファイルを読み返していない場合（上の作った例 3 の 11 行目の
  `os.makedirs`）をどうするかは、下の【穴 H-5-6】です。

**承認の前に自分に問うこと**:
1. 「初回に作る作業ディレクトリ」は、中身を読み返さなくても順 6 でよいか。
2. 上の作った例 3（手引き 20.1 の組 1）で、ファイル（12 行目）は「その他・不明」、ディレクトリ（11 行目）は「キャッシュ・状態の保存」と、
   同じ仕組みの 2 つの部品に違うラベルが付いてもよいか。

**この節で手引きが決めていないこと**:

【穴 H-5-6】**初回に作る作業ディレクトリで、中身を後で読み返さないもの（順 6 か順 8 か）**
- 何が決まっていないか: 16.1 の順 6 の例と 16.2 の 3 行目は「初回に作る作業ディレクトリ」を順 6 に入れます（`docs/drafts/final_judging_guide_draft.md:422`、`:432`）。
  一方、順 6 の定義の中心は「後で読み返す」で、20.1 の組 1 は「読み返しが無い」ので順 8 にしました（`:652-655`）。同じ置き場の
  ディレクトリの作成（`os.makedirs(CACHE_DIR)`）にどちらを当てるかが、書かれていません。
- 困る事例: 手引き 20.1 の練習用のサーバの `search_notes` × `os.makedirs` × D1（11 行目）。[第 53 章](ch53.md#s53-6)が「自分で判定する組」として
  扱った組です。
- 考えられる選択肢: (a) 16.2 の 3 行目を字義どおり当てて順 6。(b)「中身を読み返すときだけ順 6」と一言足し、この形は順 8。
  (c) 決められないとして順 8 と `note`（16.2 の最後の規則）。
- 関係する決定: D67 の 1。

【食い違い】第 53 章の考え方の例と、手引きの 16.2 の 3 行目
- 手引き: 「初回だけ `~/.app/` を作る → キャッシュ・状態の保存（作業ディレクトリ）」（`docs/drafts/final_judging_guide_draft.md:432`）。
- [第 53 章](ch53.md#s53-6): 練習用サーバの `os.makedirs(CACHE_DIR, exist_ok=True)`（最初の呼び出しで `~/.demo_cache` を作る）を、
  本記録者の考え方の例として「**その他・不明**」にしています（`docs/textbook/ch53.md:1143`、`:1219`、理由は `:1276-1333`）。
  第 53 章自身が「16.2 節の例を字義どおりに当てて『キャッシュ・状態の保存』にする読み方も、ありえない読み方ではありません」と書いています。
- 本書はどちらにも合わせません。決めるのは学生です（上の【穴 H-5-6】）。

---

<a id="ah-5-9"></a>
### H-5.9 順 7「プロセスの起動・コードの実行」（手引き L423）

> 【原文 L423】
> | 7 | **プロセスの起動・コードの実行**（D68 の 3 で足した） | SPAWN / EXEC の正 | モデルが決めたコマンドの起動、`eval` / `exec` |

**一言で言うと**: 別のプログラムを動かす（SPAWN）か、文字列をコードとして実行する（EXEC）違反です。D68 の 3 で足されました。

**ことばの確認**:
- **SPAWN**: 子プロセス（別のプログラム）を起動する効果。`subprocess.run` など。
- **EXEC**: 文字列をプログラムとして実行する効果。`eval` / `exec` など。
- **D68 の 3**: この種類を足した決定（`docs/decisions.md:3809-3814`）。

**1 文ずつ読む**（表の 7 行目）:
- 種類「**プロセスの起動・コードの実行**（D68 の 3 で足した）」。
- 定義「**SPAWN / EXEC の正**」: ほかの行と違い、置き場所ではなく **kind** で定義されています。
- 例「**モデルが決めたコマンドの起動、`eval` / `exec`**」。

**なぜこう決めたのか**: D68 の 3 の理由は「『その他・不明』に入れると、任意のコマンドを実行できる違反が分類できなかったものと同じ箱に
入って見えなくなる」です（`docs/decisions.md:3812`）。だから 8 番の**前**に置かれています。決定の文は「D1 / D2 の SPAWN・EXEC の正」に
付けると書いています（`:3809-3810`）。D4 の SPAWN / EXEC は、解析器が不にする（`authgap/dparse.py:551-552`）ので、矛の判定では
正になりません（本書の読み）。

**例で確かめる**:

（作った例 1。当てはまる）D1 で、モデルが決めた文字列をシェルで実行する。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def run_check(command: str) -> str:
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
```

起動するコマンドをモデルが決められるので D1 に反し（`docs/drafts/final_judging_guide_draft.md:320`）、正。**プロセスの起動・コードの実行**。
解析器の理由は `spawn_model`（`authgap/dparse.py:377-378`）。

（作った例 2。当てはまる）D1 で、モデルが渡した式を `eval` する。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def calc(expr: str) -> str:
    return str(eval(expr))
```

D1 ではコードの実行は反する（`docs/drafts/final_judging_guide_draft.md:319`。表 D41 で決定済み）。正で、**プロセスの起動・コードの実行**。
解析器の理由は `exec`（`authgap/dparse.py:375-376`）。

（作った例 3。境界）D2 で、固定のコマンドが、モデルが指定したファイルを消す。

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def shred(path: str) -> str:
    subprocess.run(["shred", "-u", "--", path], check=True)
    return "done"
```

人が調べて「`shred -u` は指定したファイルを上書きして消す」と分かれば、D2 に反するので正です（15.1 の SPAWN の行の考え方。
`docs/drafts/final_judging_guide_draft.md:320`。解析器は argv0 が定数なので不 `spawn_command`）。このとき、ラベルは 2 通りに読めます。
- 順 7 の定義「SPAWN / EXEC の正」にそのまま当てると**プロセスの起動・コードの実行**。
- けれども、上から順に当てると、順 3 の「利用者（またはモデル）が指定した場所のファイル」が先に当たる、とも読めます。順 3 の定義は
  kind を限っていないからです。

この形は下の【穴 H-5-2】です。

**迷いやすいところ**:
- **子プロセスの標準入力への書き込み（`pipe:write`）は、kind が FS_WRITE か EXEC**: 解析器は、子がシェルかインタプリタなら EXEC、そうでなければ
  FS_WRITE の行にします（`authgap/effects.py:844-847`）。kind が FS_WRITE の正（`tee <ファイル>` に流すなど）なら、この種類ではなく、
  `tee` が書くファイルで 1〜6 を当てます（本書の読み）。
- **D3 の SPAWN / EXEC の正には、この種類を付けない**: D3 は通信先の種類の「モデルが決めるコード・コマンド」です（[H-5.15](#ah-5-15)）。

**承認の前に自分に問うこと**:
1. 子プロセスが DB や利用者のファイルを書くと分かっている SPAWN の正に、自分は「何を変えたか」（順 2・3）と「どうやって変えたか」（順 7）の
   どちらのラベルを付けたいか。
2. モデルが任意のコマンドを実行できる違反と、固定のコマンドがたまたまファイルを書く違反が、同じ「プロセスの起動」の箱に入ってよいか。

**この節で手引きが決めていないこと**:

【穴 H-5-2】**書き込みが子プロセスやコードの実行を通るとき、順 2〜6 と順 7 のどちらを先に当てるか**
- 何が決まっていないか: 順 1 だけは「NET の効果で」と kind を限りますが、順 2〜6 の定義は kind を限っていません。だから「上から順」を
  字義どおり当てると、SPAWN / EXEC の正でも、子が変えるものが DB なら順 2、利用者のファイルなら順 3 に先に当たります。一方、順 7 の定義
  「SPAWN / EXEC の正」と D68 の 3 の文（`docs/decisions.md:3809-3810`）は、SPAWN / EXEC の正には順 7 を付ける、とも読めます。
  [第 51 章](ch51.md#s51-6)が未決の境界の 3 として挙げた形です。
- 困る事例: 上の作った例 3（`shred -u -- path`）。もう 1 つ（作った例）: `subprocess.run(["sqlite3", DB, "DELETE FROM jobs WHERE done=1"])`
  （D2 の正で、子が DB の行を消す）。
- 考えられる選択肢: (a) SPAWN / EXEC の正は常に順 7（kind で決める）。(b) 子が何を変えるか分かっていれば上から順（順 2〜6）、
  分からなければ順 7。(c) 決められないとして順 8 と `note`。
- 関係する決定: D68 の 3（`docs/decisions.md:3809-3814`）。

---

<a id="ah-5-10"></a>
### H-5.10 順 8「その他・不明」（手引き L424）

> 【原文 L424】
> | 8 | **その他・不明** | 上のどれにも当てはまらない、または決められない | |

**一言で言うと**: 1〜7 のどれにも当てはまらないもの、または、どれか決められないものです。

**ことばの確認**:
- **当てはまらない**: 定義を 1 つずつ当てて、どれも「いいえ」だったとき。
- **決められない**: 当てはまるかどうかを、コードを読んでも決められないとき。

**1 文ずつ読む**（表の 8 行目）:
- 種類「**その他・不明**」。
- 定義「**上のどれにも当てはまらない、または決められない**」: 2 つの場合を 1 つの箱にまとめています。
- 例の欄は空です。手引きの中の具体例は、20.1 の組 1（読み返しの無いキャッシュの名前のファイル）です（`docs/drafts/final_judging_guide_draft.md:652-655`）。

**なぜこう決めたのか**: D67 の 1 のラベルの一覧の最後にあります（`docs/decisions.md:3769`）。決められないものを近い種類に押し込まない
ための受け皿です。CLAUDE.md の規則 4（解決できなかったものは不明として記録する。黙って安全側に倒さない）と同じ考え方です（本書の読み）。

**例で確かめる**:

（作った例 1。当てはまらない）D1 で、ロックのためのファイルを作って、消さずに残す。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def report() -> str:
    Path("/var/run/myapp.pid").write_text(str(os.getpid()))
    return build_report()
```

相手側でも DB でもなく、利用者のファイルでも、記録のためでも、一時領域でも、読み返す状態でもありません（本書の読み）。**その他・不明**。

（作った例 2。決められない）書き先が木の外のライブラリの戻り値で決まる。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fetch_dataset(name: str) -> str:
    path = thirdparty.download(name)   # どこに何を置くかはライブラリしだい
    return Path(path).read_text()[:200]
```

`thirdparty.download` がどこに書くかを読み切れない（判定そのものも不明になりうる）。判定を正にできたとしても、ラベルは**その他・不明**。

（作った例 3。境界）手引き 20.1 の組 1。名前はキャッシュでも、読み返しが無いので順 6 に当たらない → **その他・不明**（`:652-655`）。
これは「当てはまらない」のほうです。

**迷いやすいところ**:
- **ラベルが決められないことと、判定が決められないことは別**: ラベルだけ決められないなら、判定は正のままで、ラベルを「その他・不明」に
  します。判定（正・誤）が手引きで決まらないなら、22 節の規則で判定を不明にします（[第 51 章](ch51.md#s51-6)の使い分けの表）。
- **迷ったら近いものに入れて `note` に書く、ではない**: 手引きは「その他・不明にし、事例を `note` に書く」と決めています
  （`docs/drafts/final_judging_guide_draft.md:437`。[H-5.11](#ah-5-11)）。

**承認の前に自分に問うこと**:
1. 「その他」と「不明」が 1 つの箱にまとまっていて、集計の表で区別できないことに困らないか。
2. その他・不明が多くなったら、論文でどう書くか。

**この節で手引きが決めていないこと**:

【穴 H-5-8】**「その他」と「不明」を 1 つにまとめた箱を、集計で分けるか**
- 何が決まっていないか: 順 8 は「当てはまらない」と「決められない」の 2 つの場合を 1 つにしています。集計の表（事前登録の下書きの
  「正の書き込み先の種類の内訳」、`docs/drafts/prereg_2_12_draft.md:141`）で、どちらだったかを区別する書き方が決まっていません。
  `note` に書く事例の書き方（どちらの場合か）もそろえていません。16.3 の「その他・不明」も同じです。
- 困る事例: 上の作った例 1（当てはまらない）と作った例 2（決められない）が、同じ行に数えられます。読み手が「その他・不明 N 件」を
  「判定者が分からなかった件」と読むと、例 1 の類まで「分からなかった」に見えます。
- 考えられる選択肢: (a) 1 つの箱のまま。(b) `note` の先頭に「その他:」か「不明:」を書く約束を足し、集計で分ける。(c) 種類を 2 つに分ける。
- 関係する決定: D67 の 1（ラベルの一覧に「その他・不明」が 1 つ）。

---

<a id="ah-5-11"></a>
### H-5.11 16.2 境界の例（手引き L426-438）

> 【原文 L426-429】
> ### 16.2 境界の例（先に決めておく）
>
> | 事例 | 付ける種類 | 理由 |
> |---|---|---|

**一言で言うと**: 迷いやすい 6 つの事例について、ラベルを先に決めてあります。決められない事例が判定の途中で出たら、「その他・不明」にして
`note` に書き、途中で定義を足しません。

**ことばの確認**:
- **境界の例**: 2 つの種類の境目にあって、迷いやすい事例。
- **先に決めておく**: データを見る前（封の前）に答えを書いておく、という意味です。
- **mailbox**: 2 つのプログラムが、決まったディレクトリにファイルを置き合って話す仕組み（v4 の reaper-mcp。[第 43 章](ch43.md#s43-13)）。

**1 文ずつ読む**:

まず見出しと表の見出しです。「**### 16.2 境界の例（先に決めておく）**」の次に、「**事例 / 付ける種類 / 理由**」の 3 つの欄の表が来ます。
ここからは表の行を 1 つずつ読みます。

> 【原文 L430】
> | 別のプロセスと話すための受け渡しファイル（v4 の reaper-mcp の mailbox。前の呼び出しが残した応答ファイルの削除、初回のディレクトリの作成） | **一時ファイル**（同じ呼び出しで作って消すもの）/ **キャッシュ・状態の保存**（呼び出しを越えて残る作業ディレクトリ） | 定義 5 と 6 で分ける。1 組に両方あれば、正にした位置で決める |

- 事例は、別のプロセス（v4 では REAPER という音楽のソフト）と話すためのファイルです。括弧の中に、2 つの動作が挙げられています。
  (a)「前の呼び出しが残した応答ファイルの削除」、(b)「初回のディレクトリの作成」。
- 付ける種類は 2 つ書かれています。「**一時ファイル**（同じ呼び出しで作って消すもの）」と「**キャッシュ・状態の保存**（呼び出しを越えて
  残る作業ディレクトリ）」。
- 理由は「**定義 5 と 6 で分ける。1 組に両方あれば、正にした位置で決める**」。つまり、同じ呼び出しで作って消すファイルなら 5、
  残る作業ディレクトリなら 6。1 組に両方の位置があれば、正にした位置の動作で決めます。
- 読むときの注意: 括弧の中の (b) は 6 に当たりますが、(a)「前の呼び出しが残した」ファイルは「同じ呼び出しで作って消すもの」では
  ありません。(a) をどちらにするかは、この行からは読み取れません（下の【穴 H-5-7】）。

> 【原文 L431】
> | OAuth のトークンをファイルに保存 | キャッシュ・状態の保存 | 後で読み返す |

- OAuth（ほかのサービスにログインするための仕組み）のトークンを保存する形は、**キャッシュ・状態の保存**。理由は「後で読み返す」。
  順 6 の定義の (c) です。

> 【原文 L432】
> | 初回だけ `~/.app/` を作る | キャッシュ・状態の保存 | 作業ディレクトリ |

- 初回だけ `~/.app/` を作る形は、**キャッシュ・状態の保存**。理由は「作業ディレクトリ」。順 6 の例の「初回に作る作業ディレクトリ」です。
  中身を読み返さないときの扱いは、[H-5.8](#ah-5-8) の【穴 H-5-6】。

> 【原文 L433】
> | 活動ログ `log.md` への追記（v4 の wikimind） | ログ | 読み返さない |

- 活動ログ `log.md` への追記（v4 の wikimind）は、**ログ**。理由は「読み返さない」。順 4 の定義の (b) です。

> 【原文 L434】
> | モデルが決めたパスへのエクスポート | 利用者のファイル | |

- モデルが決めたパスへのエクスポートは、**利用者のファイル**。理由の欄は空ですが、順 3 の定義の前半（モデルが指定した場所）にそのまま
  当たるからです（本書の読み）。

> 【原文 L435】
> | SQLite のキャッシュ DB への書き込み | データベース | 順 2 が順 6 より先 |

- SQLite のキャッシュ DB への書き込みは、**データベース**。理由は「順 2 が順 6 より先」。上から順の規則を名指しで使った、唯一の行です。

> 【原文 L437-438】
> **判定の途中で境界の事例が出て決められないときは「その他・不明」にし、事例を `note` に書く。** 途中で定義を足さない
> （第 22 節）。

- 「**判定の途中で境界の事例が出て決められないときは『その他・不明』にし、事例を `note` に書く。**」: この表に無い境界に出会い、
  どの種類か決められなければ、順 8 にし、どの定義のどこで迷ったかを `note` に書きます。
- 「**途中で定義を足さない（第 22 節）**」: その場で新しい種類を作ったり、定義を広げたりしません。22 節は、手引きで決まらない事例が
  出たときの手続きです（`docs/drafts/final_judging_guide_draft.md:729-737`）。

**なぜこう決めたのか**: 「先に決めておく」のは、判定の途中で結果を見ながら基準を変えないためです。CLAUDE.md の規則 5（凍結した項目は、
凍結後に見た結果で変えない）と同じ考え方です。6 つの事例のうち 2 つ（reaper-mcp・wikimind）は v4 で実際に出た形で、v4 の
`severity` の列を書き込み先の種類に置き換える準備でもあります（`docs/drafts/final_judging_guide_draft.md:671`）。
事例ごとの理由は表の「理由」の欄のとおりで、それより深い理由は書かれていません。

**例で確かめる**:

（v4 の例。出典 `docs/drafts/final_judging_guide_draft.md:678`）M20 は reaper-mcp の `get_takes` × `unlink` × D1 で正、「種類は 16.2 の
境界の例」と書かれています。けれども、M20 の `unlink` が消すのは「別のプロセスとの受け渡しファイルを毎回消す」もので、16.2 の 1 行目の
(a)（前の呼び出しが残した応答ファイルの削除）に近い形です。16.2 の 1 行目は (a) にどちらのラベルを付けるかを書いていないので、
**手引きの文面からは M20 のラベルが 1 つに決まりません**（本書の読み。[第 43 章](ch43.md#s43-13)と[第 51 章](ch51.md#s51-6)も同じ指摘）。

（作った例。1 組に両方の位置がある）

```python
MAILBOX = Path.home() / ".bridge" / "mailbox"

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ask_daw(cmd: str) -> str:
    MAILBOX.mkdir(parents=True, exist_ok=True)          # 位置 1: 初回のディレクトリ
    req = MAILBOX / f"req-{uuid.uuid4().hex}.json"
    req.write_text(json.dumps({"cmd": cmd}))             # 位置 2: 同じ呼び出しで作る
    resp = wait_for_response(req)
    req.unlink()                                         # 位置 3: 同じ呼び出しで消す
    return resp
```

3 つの位置は site がすべて違う（`pathlib.Path.mkdir`・`pathlib.Path.write_text`・`pathlib.Path.unlink`）ので、別々の組です（組は site を含む。`docs/drafts/final_judging_guide_draft.md:38`）。D1 ではどれも正で、`mkdir` の組は呼び出しを越えて残る作業ディレクトリなので
キャッシュ・状態の保存、`write_text` と `unlink` の組は同じ呼び出しで作って消すファイルなので一時ファイル、と 16.2 の 1 行目どおりに分かれます。

**迷いやすいところ**:
- **16.2 の最後の規則と 22 節の違い**: ラベルだけが決まらないなら、判定は正のまま、ラベルを「その他・不明」に、事例を `note` に。
  判定そのものが決まらないなら、判定を不明にし、事前登録の §5 にも書く（22 節）。[第 51 章](ch51.md#s51-6)の使い分けの表を見てください。
- **「正にした位置で決める」と手順 G**: 手順 G は「1 つ正が見つかった時点で止めてよい」（`docs/drafts/final_judging_guide_draft.md:163`）
  ので、どの位置を先に読んだかでラベルが変わりえます（下の【穴 H-5-1】）。

**承認の前に自分に問うこと**:
1. 6 つの事例の答えに、自分は同意するか。同意しない行があるか。
2. reaper-mcp の「前の呼び出しが残した応答ファイルの削除」を、自分ならどちらに付けるか（あるいは順 8 か）。
3. 判定の途中で決められない境界に出会ったとき、「その他・不明」と `note` だけで足りるか。後で同じ形をまとめて数えられるように、
   `note` の書き方をそろえる約束が要るか。

**この節で手引きが決めていないこと**:

【穴 H-5-7】**前の呼び出しが残した受け渡しファイルの削除（16.2 の 1 行目の括弧の (a)）のラベル**
- 何が決まっていないか: 1 行目は事例として「前の呼び出しが残した応答ファイルの削除」を挙げながら、付ける種類は「同じ呼び出しで作って
  消すもの → 5」「呼び出しを越えて残る作業ディレクトリ → 6」の 2 つしか書いていません。(a) はどちらの説明にも当たりません。
- 困る事例: v4 の M20（reaper-mcp `get_takes` × `unlink` × D1。`docs/drafts/final_judging_guide_draft.md:678`）。作った例:
  `for f in MAILBOX.glob("resp-*.json"): f.unlink()`（前の呼び出しの残りをまとめて消す）。
- 考えられる選択肢: (a) 受け渡しのファイルなので 5（一時ファイル）に入れる。(b) 呼び出しを越えて残っていたので 6 に入れる。
  (c) どちらにも当たらないので 8（その他・不明）と `note`。
- 関係する決定: D67 の 1。[第 43 章](ch43.md#s43-13)、[第 51 章](ch51.md#s51-6)の未決の 1。

【穴 H-5-1】**1 組で正にした位置が 2 つ以上あり、位置ごとに種類が違うとき、どの位置でラベルを決めるか**
- 何が決まっていないか: 16.2 の 1 行目は「1 組に両方あれば、正にした位置で決める」と書きます。けれども、正にした位置が 2 つ以上あり、
  位置ごとに種類が違うときの選び方がありません。手順 G は「1 つ正が見つかれば止めてよい」ので、読む順でラベルが変わりえます。
  条件の種類は「条件の一番弱い位置」で記録する（`docs/drafts/final_judging_guide_draft.md:164-166`、D68 の 1）と決まっていますが、
  ラベルの位置との関係は書かれていません。[第 51 章](ch51.md#s51-6)の未決の 4 と同じです。
- 困る事例（作った例）: 1 組 `export` × `builtins.open` × D1 の `locations` に 2 つの位置があり、1 つはモデルが決めた `output_file` への
  書き出し（利用者のファイル）、もう 1 つは `export.log` への追記（ログ）。どちらも正。
- 考えられる選択肢: (a) 最初に正にした位置（読む順しだい）。(b) 条件の種類を記録した位置（条件の一番弱い位置）と同じ位置。
  (c) 上から順で一番上の種類（この例なら利用者のファイル）。(d) 決められないとして順 8 と `note`。
- 関係する決定: D68 の 1（`docs/decisions.md:3796-3804`）、D67 の 1。

---

<a id="ah-5-12"></a>
### H-5.12 16.3 D3 の正に付ける通信先の種類 — 前書き（手引き L440-445）

> 【原文 L440-442】
> ### 16.3 D3 の正に付ける通信先の種類（D68 の 3）
>
> D3（`openWorldHint: false`）の違反は書き込みではなく外部との通信なので、書き込み先の種類の代わりに次のどれかを `write_target` 欄に書く。

> 【原文 L444-445】
> | 種類 | 定義 | 例 |
> |---|---|---|

**一言で言うと**: D3（関わる範囲が閉じている）の違反は「外と通信したこと」なので、書き込み先の 8 つの種類の代わりに、通信先の
4 つの種類から 1 つを、同じ `write_target` 欄に書きます。

**ことばの確認**:
- **D3**: `openWorldHint: false`。「このツールは外の世界とは関わらない」という宣言。
- **外部との通信**: そのマシンやローカルの網（家庭や社内の網）の外の相手と通信すること。local の範囲は 15.3 で決まっています
  （`docs/drafts/final_judging_guide_draft.md:371-388`）。
- **宛先**: 通信の相手。HTTP なら URL のホストの部分（`https://api.example.com/x` の `api.example.com`）。

**1 文ずつ読む**:
1. 見出し「**16.3 D3 の正に付ける通信先の種類（D68 の 3）**」: 根拠は D68 の 3 です。
2. 「**D3 の違反は書き込みではなく外部との通信なので**」: たとえば、外の天気の API に `GET` するだけのツールは、何も書き換えませんが
   D3 には反します。書き込み先の種類を当てようとしても、どれにも当たりません。
3. 「**書き込み先の種類の代わりに次のどれかを `write_target` 欄に書く**」: 欄は同じ `write_target` です。D3 の行だけ、中身の語彙が
   違う、ということです。
4. 表の見出し「**種類 / 定義 / 例**」: 16.1 と違って「順」の欄がありません。上から順の規則も書かれていません。

**なぜこう決めたのか**: D68 の 3 が「D3 の正には書き込み先の種類を付けず、通信先の種類を記録する」と決め、4 つの名前を挙げました
（`docs/decisions.md:3810-3811`）。理由は「D3 の違反は書き込みではなく外部との通信なので、書き込み先の種類が当てはまらない
（v4 の D3 の矛は 0 件だった）」です（`:3813`）。つまり、この 4 つは実例を見る前に、定義から作ったものです。4 つの分け目は
「宛先（またはコマンド）を誰が決めるか」で、解析器の D3 の理由コードの分け方（`authgap/dparse.py:502-520`）とも対応します
（本書の読み。[第 51 章](ch51.md#s51-7)の対応表）。

**例で確かめる**: 種類ごとの例は次の H-5.13〜H-5.16 で見ます。ここでは「D3 の正にならない形」を 1 つ確かめます。

（作った例）宛先が loopback。

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def local_llm(prompt: str) -> str:
    return requests.post("http://127.0.0.1:11434/api/generate", json={"prompt": prompt}).text
```

宛先 `127.0.0.1` は local なので D3 に反しません（`docs/drafts/final_judging_guide_draft.md:363`、`:376`）。正にならないので、通信先の
種類も付けません。

**迷いやすいところ**:
- **D3 の正に書き込み先の種類を書く**: 書きません。たとえ相手の状態を変える `PUT` でも、D3 の組の正なら通信先の種類です
  （同じ `PUT` の D1 の組なら、書き込み先の種類「相手側の状態」）。組の宣言で欄の語彙が決まります。
- **「順」が無い**: 2 つに当たりそうなとき、上から順では決められません（[H-5.15](#ah-5-15) の【穴 H-5-10】）。

**承認の前に自分に問うこと**:
1. 同じ `write_target` 欄に 2 つの語彙が入ることで、集計のときに混ざる心配はないか（宣言の列で分ければ混ざらない、で足りるか）。
2. 4 つの種類は実例を見る前に作ったものです。それでも、データを見る前に足したい種類はあるか（たとえば「運用者の設定」）。

**この節で手引きが決めていないこと**: 見つからなかった（種類どうしの重なりは各節で挙げる）。

---

<a id="ah-5-13"></a>
### H-5.13 通信先の種類「定数の外部ホスト」（手引き L446）

> 【原文 L446】
> | **定数の外部ホスト** | コードに書かれた外部のホストと通信する | `requests.get("https://api.example.com/…")` |

**一言で言うと**: コードに書かれた決まった外部のホストと通信する違反です。モデルは宛先を変えられません。

**ことばの確認**:
- **定数**: コードに直接書かれた、実行のたびに変わらない値。
- **外部のホスト**: local の範囲（15.3）に入らない宛先。

**1 文ずつ読む**（表の 1 行目）:
- 種類「**定数の外部ホスト**」。
- 定義「**コードに書かれた外部のホストと通信する**」: (a) ホストがコードに書かれている。(b) そのホストが外部。
- 例「**`requests.get("https://api.example.com/…")`**」。

**なぜこう決めたのか**: D68 の 3 の名前の一覧にあります（`docs/decisions.md:3811`）。解析器の理由 `net_external_host`（宛先が定数の
外部ホスト。`authgap/dparse.py:509-510`）に対応します。

**例で確かめる**:

（作った例 1。当てはまる）

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def weather(city: str) -> str:
    return requests.get("https://api.weather.example.com/v1/now", params={"q": city}).text
```

モデルが決めるのは問い合わせの中身（`city`）だけで、ホストは定数の外部ホストです。D3 に反し（`docs/drafts/final_judging_guide_draft.md:365`）、
正。**定数の外部ホスト**。

（作った例 2。当てはまる）定数を別の名前に置いてから使う。

```python
BASE = "https://hooks.example.com/notify"

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def ping() -> str:
    return requests.head(BASE).reason
```

`BASE` はモジュールの一番上の定数で、書き換える行が無ければ、コードに書かれたホストです。**定数の外部ホスト**。

（作った例 3。境界）宛先のパスだけをモデルが決める。

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def wiki(title: str) -> str:
    return requests.get(f"https://en.wikipedia.example.org/wiki/{title}").text
```

ホスト `en.wikipedia.example.org` は定数で、モデルが決めるのはパスだけです。「モデルが決める宛先」の定義は「宛先の**ホスト**をモデルが
決められる」なので当たらず、**定数の外部ホスト**です（[第 51 章](ch51.md#s51-7)のつまずきと同じ）。

**迷いやすいところ**:
- **ドットの無い名前・`〜.internal`**: 解析器は外部とします（`authgap/dparse.py:349-352`。`localhost`・`〜.localhost`・`〜.local` だけを
  local にする）。けれども手引きは local とするので、それで出た矛は D3 の正ではなく誤です（`docs/drafts/final_judging_guide_draft.md:387-388`）。
  正にならないので、この種類も付けません（試験 A の `ask_ollama` は、`http://ollama:11434` に `net_external_host` が出た。[H-5.26](#ah-5-26)）。
- **運用者の設定の既定値**: `os.environ.get("API", "https://…")` の既定値は「コードに書かれて」いますが、宛先を決めるのは運用者です。
  手引きの 16.3 の例は、これを「その他・不明」にしています（[H-5.16](#ah-5-16)）。

**承認の前に自分に問うこと**:
1. リポジトリの中の設定ファイル（`config.yaml`）に書かれたホストは、自分には「コードに書かれた」と見えるか、「運用者の設定」と見えるか。
2. 定数のホストが外部か local か分からない名前（`api.corp`）に出会ったら、まず 15.3 の local の範囲の表で判定（正・誤・不明）を決め、
   ラベルはその後、という順を守れるか。

**この節で手引きが決めていないこと**:

【穴 H-5-11】**リポジトリの中の設定ファイルに書かれた外部ホストは「コードに書かれた」か「運用者の設定」か**
- 何が決まっていないか: 定義は「コードに書かれた」、16.3 のその他・不明の例は「宛先が運用者の設定で、既定値が外部のもの」です。
  ソースと一緒に配られる設定ファイル（運用者が書き換えてもよいが、ふつうはそのまま使う）が、どちらに当たるかが書かれていません。
  判定（正かどうか）は 15.3 の「宛先が運用者の設定で決まる」の行で決められても、ラベルが割れます。
- 困る事例（作った例）:

  ```python
  CFG = yaml.safe_load(Path(__file__).with_name("config.yaml").read_text())   # base_url: https://api.example.com

  @mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
  def status() -> str:
      return requests.get(CFG["base_url"] + "/status").text
  ```

- 考えられる選択肢: (a) リポジトリに入っている値は「コードに書かれた」とみなし定数の外部ホスト。(b) 運用者が書き換えられる場所の値は
  運用者の設定とみなし、その他・不明。(c) 決められないとしてその他・不明と `note`。
- 関係する決定: D68 の 3（`docs/decisions.md:3810-3811`）、15.3 の運用者の設定の行（`docs/drafts/final_judging_guide_draft.md:367`）。

---

<a id="ah-5-14"></a>
### H-5.14 通信先の種類「モデルが決める宛先」（手引き L447）

> 【原文 L447】
> | **モデルが決める宛先** | 宛先のホストをモデルが決められる | `httpx.get(url)`（`url` はツールの引数） |

**一言で言うと**: 通信の相手のホストを、モデルが選べる違反です。

**ことばの確認**:
- **モデルが決められる**: ツールの引数などモデルの値が、宛先のホストの位置まで届き、モデルが値を選べること（原理 3-a）。
- **ツールの引数**: モデルがツールを呼ぶときに渡す値。

**1 文ずつ読む**（表の 2 行目）:
- 種類「**モデルが決める宛先**」。
- 定義「**宛先のホストをモデルが決められる**」: 決められるのが**ホスト**であることが条件です。パスや問い合わせの中身だけなら当たりません。
- 例「**`httpx.get(url)`（`url` はツールの引数）**」。

**なぜこう決めたのか**: D68 の 3 の名前の一覧にあります（`docs/decisions.md:3811`）。15.3 の「宛先をモデルが決められる → 反する（原理 3-a）」
（`docs/drafts/final_judging_guide_draft.md:366`）で正になる件です。解析器の理由 `net_model_host`（`authgap/dparse.py:511-512`）に
対応します。

**例で確かめる**:

（作った例 1。当てはまる）

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def fetch(url: str) -> str:
    return httpx.get(url).text
```

モデルは外部のどのホストでも指せるので D3 に反し、正。**モデルが決める宛先**。

（作った例 2。当てはまる）ホスト名だけを引数でもらう。

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def health(host: str) -> str:
    return requests.get(f"https://{host}/healthz").text
```

ホストの全体をモデルが決めます。**モデルが決める宛先**。

（作った例 3。境界。本書の試験）ホストの一部だけをモデルが決め、ドメインは定数の外部（試験 A の `regional`）。

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def regional(region: str) -> str:
    return requests.get(f"https://{region}.api.example.com/v1/status").text
```

解析器は `contradiction_reason:D3:net_model_host` を出しました（試験 A）。モデルが `region` に何を入れても宛先は `*.api.example.com`
（定数の外部ドメインの中）なので、外部に出ることはモデルが選ばなくても決まっています。一方で、ホスト名の一部はモデルが決めています。
ラベルが「モデルが決める宛先」か「定数の外部ホスト」かは、下の【穴 H-5-9】です。

**迷いやすいところ**:
- **判定は正**: この境界の例でも、D3 に反すること（外部と通信する）は変わりません。迷うのはラベルだけです。
- **検証があるとき**: モデルの URL を検証して手元に絞っているなら、反しない（誤）こともあります。検証が本当に絞っているかを確かめる
  （[第 50 章](ch50.md#s50-8)の `\` を含む URL の例）。

**承認の前に自分に問うこと**:
1. ホストの一部（サブドメイン）だけをモデルが決める形は、自分にはどちらの種類に見えるか。
2. `region` が `Literal["us", "eu"]` のように 2 つに限られていたら、答えは変わるか。

**この節で手引きが決めていないこと**:

【穴 H-5-9】**ホストの一部をモデルが決めるが、定数の外部ドメインの中に閉じる形**
- 何が決まっていないか: 定義は「宛先のホストをモデルが決められる」です。ホストの**一部**だけを決められる形（サブドメイン、ポート、
  選択肢の中から 1 つ）が当たるかが書かれていません。解析器は `url.host` の主体が MODEL なら `net_model_host` にします
  （試験 A。`authgap/dparse.py:289-290`）。
- 困る事例: 上の作った例 3（試験 A の `regional`）。もう 1 つ（作った例）: `BASES = {"prod": "https://api.example.com", "stg": "https://stg.example.com"}`
  から引数 `env` で選ぶ。
- 考えられる選択肢: (a) ホストの文字列にモデルの値が入れば「モデルが決める宛先」。(b) 取りうる宛先がすべて定数の外部ドメインの中なら
  「定数の外部ホスト」。(c) 決められないとして「その他・不明」と `note`。
- 関係する決定: D68 の 3、原理 3-a（`docs/contradiction_principles.md:77`）。

---

<a id="ah-5-15"></a>
### H-5.15 通信先の種類「モデルが決めるコード・コマンド」（手引き L448）

> 【原文 L448】
> | **モデルが決めるコード・コマンド** | 実行するコード・起動するコマンドをモデルが決められる（通信しうる） | `subprocess.run(cmd, shell=True)` |

**一言で言うと**: 実行するコードや起動するコマンドをモデルが選べるので、モデルはそれを使って外と通信させられる、という違反です。

**ことばの確認**:
- **（通信しうる）**: コードやコマンドを選べれば、`curl` などで外と通信させられる、という意味です。実際に通信するコードかどうかは問いません。
- **`shell=True`**: 文字列をシェル（コマンドを解釈するプログラム）に渡して実行すること。

**1 文ずつ読む**（表の 3 行目）:
- 種類「**モデルが決めるコード・コマンド**」。
- 定義「**実行するコード・起動するコマンドをモデルが決められる（通信しうる）**」。
- 例「**`subprocess.run(cmd, shell=True)`**」（`cmd` をモデルが決める場合）。

**なぜこう決めたのか**: D68 の 3 の名前の一覧にあります（`docs/decisions.md:3811`）。15.3 の「実行するコード・起動するコマンドを
モデルが決められる → 反する」（`docs/drafts/final_judging_guide_draft.md:368`）で正になる件です。解析器の理由は `exec_model`・
`spawn_model`（`authgap/dparse.py:516-519`）。コードやコマンドが定数なら、解析器は D3 で不にする（同じ行）ので、矛の判定では
この種類の正になりません。

**例で確かめる**:

（作った例 1。当てはまる）

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def shell(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
```

モデルは `curl https://…` も実行させられるので D3 に反し、正。**モデルが決めるコード・コマンド**。

（作った例 2。当てはまる）

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def py(code: str) -> str:
    env = {}
    exec(code, env)
    return str(env.get("result"))
```

モデルが書いた Python のコードを実行します。`urllib` で外と通信させられるので、正。**モデルが決めるコード・コマンド**。

（作った例 3。境界。本書の試験）固定のコマンドに、モデルの URL を引用して渡す（試験 A の `fetch_with_curl`）。

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def fetch_with_curl(url: str) -> str:
    return subprocess.run(f"curl -s {shlex.quote(url)}", shell=True, capture_output=True, text=True).stdout
```

解析器は `contradiction_reason:D3:spawn_model` を出しました（試験 A）。`shlex.quote` があるので、モデルは別のコマンドを足せません。
起動するコマンドはいつも `curl` で、モデルが決めるのは `curl` の宛先です（`-` で始まる値で `curl` の選択肢を足すこともできる）。
D3 には反する（モデルが外部の宛先を選べる）ので正ですが、ラベルは「モデルが決める宛先」（宛先のホストをモデルが決める）か
「モデルが決めるコード・コマンド」（解析器の理由と kind の SPAWN に合わせる）かで割れます。下の【穴 H-5-10】です。

**迷いやすいところ**:
- **解析器の理由は手がかり**: `spawn_model` が出ていても、モデルが本当に選べるのがコマンドかどうかは、自分で確かめます（E7 の形。
  [H-5.24](#ah-5-24)）。
- **D1・D2 の SPAWN の正とは語彙が違う**: D1・D2 の同じ形の正には、書き込み先の種類の「プロセスの起動・コードの実行」を付けます（[H-5.9](#ah-5-9)）。

**承認の前に自分に問うこと**:
1. 試験 A の `fetch_with_curl` のラベルを、自分ならどちらにするか。
2. 16.3 に「上から順」の規則が無いことを、そのままにしてよいか。

**この節で手引きが決めていないこと**:

【穴 H-5-10】**固定のコマンドの引数としてモデルが宛先を渡す形（2 つの種類に当たる）と、16.3 の当てはめる順**
- 何が決まっていないか: 「モデルが決める宛先」の定義は kind を限っていません（宛先のホストをモデルが決められる）。一方、kind が SPAWN /
  EXEC の正は「モデルが決めるコード・コマンド」の定義にも近く見えます（解析器の理由も `spawn_model`）。16.3 には 16.1 のような
  「上から順に当てはめる」の規則が無いので、2 つに当たるときに決められません。
- 困る事例: 上の作った例 3（試験 A の `fetch_with_curl`）。もう 1 つ（作った例）: `subprocess.run(["git", "clone", "--", repo_url, dest])`
  （argv0 は定数で、解析器は D3 で不 `spawn_command`。不の中身の判定は D1・D2 だけなので、この形は D3 では判定に出てこないが、
  D3 の矛が出る形との釣り合いの問題として残る）。
- 考えられる選択肢: (a) 16.3 の表の上から順（この例なら「モデルが決める宛先」が先）。(b) kind で決める（SPAWN / EXEC はいつも
  「モデルが決めるコード・コマンド」）。(c) 決められないとして「その他・不明」と `note`。
- 関係する決定: D68 の 3（`docs/decisions.md:3810-3811`）。

---

<a id="ah-5-16"></a>
### H-5.16 通信先の種類「その他・不明」（手引き L449）

> 【原文 L449】
> | **その他・不明** | 上のどれにも当てはまらない、または決められない | 宛先が運用者の設定で、既定値が外部のもの |

**一言で言うと**: 上の 3 つのどれにも当たらないか、決められない D3 の正です。手引きの例は「宛先が運用者の設定で、既定値が外部のもの」です。

**ことばの確認**:
- **運用者の設定**: 環境変数・設定ファイル・起動の引数など、サーバを動かす人が決める値（14.3、`docs/drafts/final_judging_guide_draft.md:262`）。
- **既定値**: 運用者が何も設定しなかったときに使う値（`os.environ.get("X", "<既定値>")` の 2 つ目）。

**1 文ずつ読む**（表の 4 行目）:
- 種類「**その他・不明**」。
- 定義「**上のどれにも当てはまらない、または決められない**」: 16.1 の順 8 と同じ 2 つの場合をまとめた箱です。
- 例「**宛先が運用者の設定で、既定値が外部のもの**」: 15.3 は、この形を「既定値や文書で外部を想定しているなら反する」としています
  （`docs/drafts/final_judging_guide_draft.md:367`）。だから正になりえます。けれども、宛先を決めるのはコードの定数でもモデルでもなく
  運用者なので、上の 3 つに当たらず、ここに来ます。

**なぜこう決めたのか**: D68 の 3 の名前の一覧の最後にあります（`docs/decisions.md:3811`）。「運用者の設定」という種類を別に作らなかった
理由は書かれていません。本書の読み: v4 の D3 の矛は 0 件で（`:3813`）、実例を見る前に作った 4 つなので、最小限にした、と読めます。

**例で確かめる**:

（作った例 1。当てはまる。手引きの例の形。本書の試験 E）

```python
API = os.environ.get("NOTES_API", "https://notes.example.com")

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def list_remote() -> str:
    return requests.get(API + "/notes").text
```

既定値が外部なので D3 に反する、と読めて正。宛先を決めるのは運用者なので、上の 3 つに当たらず**その他・不明**（[第 51 章](ch51.md#s51-7)の作例と同じ）。
ただし、本書の試験 E では、解析器はこの形に**矛ではなく不**（`contradiction_unknown:D3:net_host_unknown`）を出しました。宛先のホストの主体を
運用者（OP）と読み、定数としては読まなかったからです（`authgap/dparse.py:283-290` で、定数でもモデルでもなければ `unknown`、`:515` で不）。
D3 の不は判定しない（`docs/drafts/final_judging_guide_draft.md:535`）ので、**手引きの例の形そのものは、ふつう D3 の正として判定に出てきません**。
この種類が使われるのは、解析器が定数の外部ホストやモデルの宛先と読んだ矛を、人が読んで「実は運用者の設定で決まる」と分かったときです（次の例 3）。

（作った例 2。当てはまる）環境変数に既定値が無く、README に「`https://api.example.com` を設定する」と書いてある。

```python
API = os.environ["EXAMPLE_API"]
```

15.3 の「文書で外部を想定しているなら反する」で正。宛先は運用者の設定なので、上の 3 つに当たらず**その他・不明**（定義どおり）。
（解析器がこの形に矛を出すかは確かめていません。例 1 と同じく不になると本書は見込みます。）

（作った例 3。境界。走らせていない）定数の URL を、`main()` の中で運用者の環境変数で書き換える。

```python
API = "https://notes.example.com"

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def list_remote() -> str:
    return requests.get(API + "/notes").text

def main():
    global API
    API = os.environ.get("NOTES_API", API)
    mcp.run()
```

仮に解析器が `API` を定数と読んで `net_external_host` の矛を出したとします。理由のコードは「定数の外部ホスト」を指しますが、`main()` を通る
起動では運用者の設定で宛先が変わり、`main()` を通らない起動（`fastmcp run`）では定数のまま、という形です。種類を「定数の外部ホスト」にするか、
「その他・不明」（運用者の設定）にするかは、14.4 の「起動の方法」の考え方とも絡み、手引きの文面だけでは割れます（本書の読み。
`main()` を通らない起動で定数の外部ホストに届くので正、までは決まる）。決められなければ、16.3 の「その他・不明」の定義の後半（決められない）に当たる、と本書は読みます。

**迷いやすいところ**:
- **解析器が「定数」と読んだ宛先が、実は運用者の設定の既定値だった**: そのときは「定数の外部ホスト」ではなく、この種類です（[第 51 章](ch51.md#s51-7)）。
- **既定値が local**: 運用者の設定で、既定値や文書が local を想定しているなら、そもそも反しません（`docs/drafts/final_judging_guide_draft.md:367`）。

**承認の前に自分に問うこと**:
1. 手引きの例の形（運用者の設定で、既定値が外部）は、解析器がふつう不を出すので D3 の正としては判定に出てこない（本書の試験 E）。
   それを知ったうえで、16.3 の表の例をこのままにするか。
2. 「運用者の設定の宛先」が D3 の正に多く出たら、それが「その他・不明」の箱に入って見えなくなることを、受け入れるか。
   （D68 の 3 が「プロセスの起動」を足したのと同じ理由で、データを見る前に「運用者の設定」を足す選択もありえます。決めるのは学生です。）
3. 「その他」と「不明」を分けて数えたいか（[H-5.10](#ah-5-10) の【穴 H-5-8】は 16.3 にも当てはまります）。

**この節で手引きが決めていないこと**: 見つからなかった（「その他」と「不明」の区別は【穴 H-5-8】、設定ファイルの値は【穴 H-5-11】）。

---

<a id="ah-5-17"></a>
### H-5.17 第 17 節 誤の原因の分類 — 前書きと表の見出し（手引き L451-457）

> 【原文 L451-454】
> ## 17. 誤の原因の分類
>
> 誤にしたときは、次のどれかを `error_class` に書く（v3・v4 で出た類を最初から用意した）。
> 記号の E1〜E9 は誤の原因の分類で、v4 の判定記録の id（`E00` など）とは関係ない。

> 【原文 L456-457】
> | 記号 | 類 | 見分け方 | これまでの例 |
> |---|---|---|---|

**一言で言うと**: 誤にしたときは、解析器が**なぜ**間違えたかを E1〜E9 の 9 つの類から選んで `error_class` に書きます。
類は、v3・v4 で実際に出た誤りから、最初に用意したものです。

**ことばの確認**:
- **誤の原因**: 解析器が矛を出したのに、人の判定で誤（到達しない、または宣言に反しない）になった理由の分類。
- **`error_class`**: 判定表の欄。記号と 1 文の説明を書きます（例「E1: lifespan の init_db が起動時に済ませる」。
  `docs/drafts/final_judging_guide_draft.md:179`）。
- **v4 の判定記録の id**: `evidence/population_v4/v4_judgments.json` の組の番号。D4 の組の id は `E00`・`E01`… と E で始まるので、
  誤の原因の記号と紛らわしい（[第 51 章](ch51.md#s51-8)）。
- **見分け方**: その類だと分かる目印。多くは手引きのほかの節への参照です。

**1 文ずつ読む**:
1. 「**誤にしたときは、次のどれかを `error_class` に書く**」: 正や不明には書きません。
2. 「**（v3・v4 で出た類を最初から用意した）**」: 判定の途中で類を作らないよう、これまでに出た誤の類を先に並べた、ということです。
3. 「**記号の E1〜E9 は誤の原因の分類で、v4 の判定記録の id（`E00` など）とは関係ない**」: 手引きの 20.2 の表に出る「v4 の E00」は
   判定記録の番号で、誤の原因の E1〜E9 とは別物です（`docs/drafts/final_judging_guide_draft.md:681`）。
4. 表の見出し「**記号 / 類 / 見分け方 / これまでの例**」: 4 つの欄です。

**なぜこう決めたのか**: D67 の 2 は、起動時の初期化の類（lifespan の形）について「解析器は変えず、設計の選択による限界（誤警報の向き）として
件数を報告する。判定の手引きの誤の原因の欄に、この類を設ける」と決めました（`docs/decisions.md:3777-3778`）。件数を報告するには、
誤の原因を決まった類で記録しなければなりません。E1 以外の類を用意したことは、どの決定にも名指しされていません。v3・v4 で出た類を
並べたのは本記録者で、その元は O41（v3）と O43（v4）の表です（`docs/open_questions.md:1061-1074`、`:1188-1199`）。

**例で確かめる**: 類ごとの例は H-5.18〜H-5.26 で見ます。どの類も、**解析器のどの仕組みから誤が生まれるか**をコードの行で示し、
本書の試験で実際に矛が出ることを確かめます。

**迷いやすいところ**:
- **誤の 2 つの落ち方**: E1・E3・E4・E6 は主に「到達しない」で落ちる誤、E2・E5・E7・E8 は主に「宣言に反しない」で落ちる誤です
  （本書の整理。[第 51 章](ch51.md#s51-8)の「2 つの問いのどちらで落ちたか」）。E3・E4 は「その操作ではない」（手順 C）でも落ちます。
- **不明に E を付けない**: 判定が決められないなら誤ではなく不明で、`unknown_reason` を書きます。

**承認の前に自分に問うこと**:
1. 1 つの誤に原因が 2 つ重なったら、`error_class` にどう書くか（下の【穴 H-5-13】）。
2. 9 つの類で、自分が思いつく誤の形は全部分けられそうか。

**この節で手引きが決めていないこと**:

【穴 H-5-13】**1 つの誤に原因が 2 つ以上重なるときの書き方**
- 何が決まっていないか: `error_class` は「第 17 節の分類（E1〜E9）と 1 文の説明」（`docs/drafts/final_judging_guide_draft.md:179`）です。
  記号を 1 つだけ書くのか、`;` で並べるのかが決まっていません。条件の種類は「複数の条件が重なるなら全部を `;` で並べる」と決めています
  （`:176`）。[第 51 章](ch51.md#s51-17)が未決として挙げた形です。
- 困る事例（作った例）: lifespan の初期化の中で、書く前に内容を確かめる追記（`'a'`）をする形を、D4 の組で判定する。到達しない（E1）と、
  冪等なので反しない（E8）の両方が当たります。v4 の E00〜E02 は、v4 の時点では到達しない理由と冪等の理由が重なっていました
  （`docs/drafts/final_judging_guide_draft.md:681`）。もう 1 つは試験 B の `export_new`（[H-5.25](#ah-5-25) の【穴 H-5-15】）。
- 考えられる選択肢: (a) 1 つだけ書く（その場合の優先の順を決める。たとえば到達しない側を先）。(b) `;` で全部を並べ、集計では
  重複して数える。(c) 1 つ目を主、残りを `note` に書く。
- 関係する決定: D67 の 2（`docs/decisions.md:3773-3778`）。

---

<a id="ah-5-18"></a>
### H-5.18 E1 起動時の初期化（手引き L458）

> 【原文 L458】
> | **E1** | 起動時の初期化（lifespan・import 時） | 第 14.4 節 | shyhurricane（v4） |

**一言で言うと**: 効果が「一度だけの初期化」の中にあり、その初期化が lifespan かモジュールの読み込み時に必ず先に済んでいるので、
ツールの呼び出しでは届かない誤です。

**ことばの確認**:
- **lifespan**: `FastMCP(..., lifespan=…)` に渡す、サーバの起動時にツールの受付より前に走る関数（[第 3 章](ch03.md)）。
- **import 時**: モジュールが読み込まれた時点。モジュールの一番上の文はそこで走ります。
- **一度だけの初期化**: `if _x is None: _x = _init()` のように、最初の 1 回だけ準備をする形。
- **shyhurricane**: v4 で E1 の形が出た木（`docs/drafts/final_judging_guide_draft.md:680` の M01）。

**1 文ずつ読む**（表の E1 の行）:
- 記号 **E1**。類「**起動時の初期化（lifespan・import 時）**」。
- 見分け方「**第 14.4 節**」: 14.4 の表で「到達しない（誤、E1）」になる 2 つの行（lifespan の中・モジュールの読み込み時）
  （`docs/drafts/final_judging_guide_draft.md:289-290`）。`main()` の中だけで先に済ませる形は「到達する」なので E1 ではありません（`:288`）。
- これまでの例「**shyhurricane（v4）**」。

**なぜこう決めたのか**: D67 の 2 が、lifespan の形を誤とし、この類を誤の原因の欄に設けると決めました（`docs/decisions.md:3773-3778`）。
解析器を直さない理由は O43 にあります。lifespan の形を正しく扱うには、順序・状態・戻らない・失敗しないの 4 つを全部確かめる必要があり、
1 つでも外すと誤 clear（見落とし）を作ること、しかも v4 の結果を見て気づいた変更なので「結果を元に解析器を変えない」（D66）に当たること
（`docs/open_questions.md:1209-1215`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器は、`if` の条件が定数で決まらなければ、**両方の枝を実行**します（`authgap/val/engine.py:334-352`）。条件を定数で決めるのは、
  ローカルの名前・リテラル・`not` / `and` / `or` / 単一の比較だけです（`authgap/val/engine.py:2731-2735`）。だから `if _index is None:` の
  ような大域変数の守りの中にも入り、初期化の中の効果をツールの効果として出します。
- lifespan の関数の本体そのものの効果は、ツールには付けません（`authgap/entry_seed.py:20-21`「lifespan 本体の起動時の効果はツールに付けない」）。
  けれども、ツールの道筋が同じ初期化の関数を呼んでいれば、そちらから降りて効果を出します。
- O43 は、この類を「起動時の初期化をツールの経路に数える」として記録しています（`docs/open_questions.md:1190`）。

**例で確かめる**:

（作った例。本書の試験 D の `lookup`）

```python
_index = None

def _get_index():
    global _index
    if _index is None:
        os.makedirs("/var/lib/h5/index", exist_ok=True)
        _index = {}
    return _index

@asynccontextmanager
async def app_lifespan(server):
    _get_index()
    yield {}

mcp = FastMCP("h5d", lifespan=app_lifespan)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lookup(key: str) -> str:
    return str(_get_index().get(key))
```

解析器は `lookup` × `os.makedirs` × D1 に `fs_write` の矛を出しました（道筋 `_get_index`。試験 D）。けれども、lifespan が受付の前に
`_get_index()` を呼び、`_index` が `{}` になります。`_index` を `None` に戻す行もありません（grep で確かめる。14.4 の見分け方）。
ツールの呼び出しでは `os.makedirs` に届かないので、**誤、E1**。

（作った例の変種 1）同じコードで、lifespan が無く、`main()` の中で `_get_index()` を呼んでから `mcp.run()` する形なら、14.4 の 1 行目で
「到達する」になり、E1 にはなりません（`docs/drafts/final_judging_guide_draft.md:288`）。
（作った例の変種 2）lifespan の中で `if os.environ.get("PREWARM"): _get_index()` と条件つきで呼ぶなら、条件が偽のときツールの呼び出しで
届くので「到達する」です（`:296-297`）。

**迷いやすいところ**:
- **E1 と E6**: どちらも「到達しない」ですが、起動時の初期化だけは E1 に分けます。集計で「解析器の設計の限界による誤警報」として
  別に数えるためです（[第 49 章](ch49.md#s49-3)、[第 51 章](ch51.md#s51-9)）。
- **1 組の位置の片方だけが初期化**: 手順 G で、ほかの位置が毎回届けば組は正（v4 の M06。`docs/drafts/final_judging_guide_draft.md:677`）。

**承認の前に自分に問うこと**:
1. lifespan の形は誤、`main()` の形は正、という分け方が「解析器に有利な側と不利な側の両方がある」こと（`docs/drafts/final_judging_guide_draft.md:302-303`）
   に納得しているか。
2. import 時の初期化が、別のモジュールの読み込み（`import store` の時点で `store.py` の一番上が走る）でも E1 になることを確かめたか。

**この節で手引きが決めていないこと**: 見つからなかった（条件つきの lifespan や `None` に戻す形は 14.4 で決まっている。原因が重なる形は【穴 H-5-13】）。
関連する章: [第 48 章](ch48.md#s48-12)（手順 G の位置が 3 つある例）、[第 49 章](ch49.md#s49-5)（14.4 のくわしい見分け方）、[第 51 章](ch51.md#s51-9)（v4 の shyhurricane の実物）。

---

<a id="ah-5-19"></a>
### H-5.19 E2 同じ呼び出しで作った一時ファイル・ロックの後始末（D2）（手引き L459）

> 【原文 L459】
> | **E2** | 同じ呼び出しで作った一時ファイル・ロックの後始末（D2） | 第 15.2 節 | ccr（v4）、`mkstemp` / atomic write（v3、O41） |

**一言で言うと**: D2（破壊しない）の組で、ツールが同じ呼び出しの中で自分で作った一時ファイルやロックを消しているのを、解析器が
「既存のものを消す」と読んだ誤です。

**ことばの確認**:
- **ロック（ロックファイル）**: 同時に 2 つの処理が同じものを触らないように、目印として作るファイル。
- **後始末**: 使い終わったものを消すこと。
- **atomic write**: 一時ファイルに書いてから、本来の名前に置き換える書き方。失敗しても半端なファイルが残りません。
- **ccr**: v4 で E2 の形が出た木。

**1 文ずつ読む**（表の E2 の行）:
- 記号 **E2**。類「**同じ呼び出しで作った一時ファイル・ロックの後始末（D2）**」: D2 の組だけの類です。
- 見分け方「**第 15.2 節**」: 15.2 の迷いやすい形「同じ呼び出しで自分が作った一時ファイル・ロックファイルを消す: 呼び出しの前からあった
  ものではないので反しない（誤、E2）」（`docs/drafts/final_judging_guide_draft.md:351-353`）。
- これまでの例「**ccr（v4）、`mkstemp` / atomic write（v3、O41）**」。

**なぜこう決めたのか**: D2 の問いは「呼び出しの前からあったものを消す・上書きする・変えるか」です（`docs/drafts/final_judging_guide_draft.md:338`）。
自分が作ったものは前からあったものではないので、反しません。解析器を直さない理由は O41 にあります。MCP の仕様の「追加か破壊か」で
読めば破壊ではないが、採った原理の読み替えになるので直さない（`docs/open_questions.md:1063-1064`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器の sink の表は、`os.remove` / `os.unlink` に「破壊的（`destructive=True`）」の属性を付けています（`authgap/catalog/sinks.py:363-364`）。
- D2 の判定で、破壊的な FS_WRITE は「remove」の類になり（`authgap/dparse.py:365-368`）、理由 `fs_remove` の矛になります（`:408-409`）。
  そのファイルを**同じ呼び出しで作ったか**は見ていません。

**例で確かめる**:

（作った例。本書の試験 C の `convert`）

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def convert(text: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        return path
    finally:
        os.remove(path)
```

解析器は `convert` × `os.remove` × D2 に `fs_remove` の矛を出しました（試験 C）。`os.remove` が消すのは、同じ呼び出しの `mkstemp` で
作ったファイルだけです。**誤、E2**。

（作った例の変種）同じ形を D1 の組で判定すると、作成も削除も環境の変更なので**正**です（`docs/drafts/final_judging_guide_draft.md:318`。
v4 の M58。`:679`）。ラベルは一時ファイル（[H-5.7](#ah-5-7)）。宣言で答えが逆になります。

（作った例。境界）前の呼び出しが残したロックを消す。

```python
LOCK = Path("/var/lock/myapp.lock")

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def sync() -> str:
    if LOCK.exists():
        LOCK.unlink()          # 前の呼び出しが落ちて残したロックを掃除
    LOCK.touch()
    try:
        return do_sync()
    finally:
        LOCK.unlink()
```

最後の `unlink` は E2 の形ですが、最初の `unlink` は**前の呼び出しが残したもの**を消すので、呼び出しの前からあったものです。15.2 は
「前の呼び出しが残したファイルを消すなら反する」と書いています（`docs/drafts/final_judging_guide_draft.md:352-353`）。手順 G で、
1 つでも反する位置があれば組は正です。

**迷いやすいところ**:
- **E2 は D2 だけ**: D1 では同じ形が正です。D1 の組を E2 で誤にしないでください。
- **atomic write の置き換え先**: 一時ファイルを本来の名前に `os.replace` するとき、置き換え先に前からファイルがあれば、前の中身を置き換える
  ので反します（[第 50 章](ch50.md#s50-7)）。消しているのが一時ファイルの側か、置き換え先の側かを見分けます。

**承認の前に自分に問うこと**:
1. 「自分が作ったものを消すのは破壊ではない」という読みに納得しているか。
2. 同時に動く別の呼び出しのロックを消しうる形を、E2 にしてよいか（[第 50 章](ch50.md#s50-12)の候補 4）。

**この節で手引きが決めていないこと**: 見つからなかった（同時の呼び出しのロックの扱いは第 15 節の側の穴として[第 50 章](ch50.md#s50-12)が挙げている）。
関連する章: [第 49 章](ch49.md#s49-6)（14.5 同じ呼び出しで作って消すもの）、[第 50 章](ch50.md#s50-7)（E2 の実物と変種）、[第 51 章](ch51.md#s51-10)。

---

<a id="ah-5-20"></a>
### H-5.20 E3 名前だけの解決の誤り（手引き L460）

> 【原文 L460】
> | **E3** | 名前だけの解決の誤り（呼び出し先の取り違え） | 呼んでいるのは組み込みのメソッドや別のクラスの同名メソッド | 組み込みの `set()` を `CacheManager.set` に（v4 の rails-lens）、`bytearray.append`（v3） |

**一言で言うと**: 解析器が、呼び出し先を**名前だけ**で木の中の別の関数に結んでしまい、実際には呼ばれていない関数の効果を出した誤です。

**ことばの確認**:
- **名前だけの解決**: `x.add(...)` の `add` という末尾の名前だけを手がかりに、木の中の `add` という名前の関数・メソッドに結ぶこと。
- **受け手**: `x.add(...)` の `x`。受け手の型（`x` に何が入っているか）が分かれば、正しいメソッドに結べます。
- **組み込みのメソッド**: Python に最初からある型（`set`・`dict`・`list`・`bytearray` など）のメソッド。
- **rails-lens**: v4 で E3 の形が出た木（M04。`docs/drafts/final_judging_guide_draft.md:682`）。

**1 文ずつ読む**（表の E3 の行）:
- 記号 **E3**。類「**名前だけの解決の誤り（呼び出し先の取り違え）**」。
- 見分け方「**呼んでいるのは組み込みのメソッドや別のクラスの同名メソッド**」。
- これまでの例「**組み込みの `set()` を `CacheManager.set` に（v4 の rails-lens）、`bytearray.append`（v3）**」。

**なぜこう決めたのか**: 手順 C は「組み込みの `set()`・`dict.get()`・`list.append()` を、木の中の同名のメソッドと取り違えていないか」を
確かめるよう求めます（`docs/drafts/final_judging_guide_draft.md:127-128`）。解析器を直さない理由は O41 にあります。値の形で組み込みの型と
決めて結ばないように直そうとしたが、値の形は型の証明ではなく、誤 clear（見落とし）を作ったので取り消した（`docs/open_questions.md:1073-1074`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器は、受け手の型で裏付けられないときも、候補が 1 つなら**末尾の名前だけで**木の中のメソッドに降ります（`authgap/val/engine.py:1029-1041`）。
  降りないと本当の道筋が消えるからです（同じ箇所の注記、D17 の改訂）。
- そうして降りた道筋の効果には、確度 `opaque(unresolved)` を合流します（`authgap/effects.py:232-243`）。けれども D1 の FS_WRITE は、確度を
  見ずに矛にします（`authgap/dparse.py:379-380`）。だから名前だけの取り違えでも D1 の矛が出ます。

**例で確かめる**:

（作った例。本書の試験 C の `unique`）

```python
class AuditLog:
    def add(self, line):
        with open("audit.log", "a") as fh:
            fh.write(line + "\n")

def _collect(items):
    seen = set()
    for it in items:
        seen.add(it)
    return sorted(seen)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def unique(items: list[str]) -> list[str]:
    return _collect(items)
```

解析器は `unique` × `builtins.open` × D1 に `fs_write` の矛を出し、道筋は `_collect -> AuditLog.add` でした（試験 C）。けれども
`seen.add(it)` の `seen` は組み込みの `set` で、`AuditLog.add` は呼ばれません。**誤、E3**。

（作った例の変種）`seen = AuditLog()` なら、本当に `AuditLog.add` が呼ばれ、`audit.log` に追記するので**正**（ラベルはログ）。
受け手が何かで答えが逆になります。

**迷いやすいところ**:
- **E3 と E6 の境**: 道筋の呼び出しが**別の関数を指していた**なら E3、道筋にそもそも呼び出しが無く、**別の入口からだけ**呼ばれるなら E6
  （[第 49 章](ch49.md#s49-3)の形 2・形 3）。
- **エディタの「定義へ移動」も名前で当てることがある**ので、受け手の型で確かめる（`docs/drafts/final_judging_guide_draft.md:88-89`）。

**承認の前に自分に問うこと**:
1. 受け手の型を確かめるとき、どこまで遡れば「組み込みの `set` だ」と言えるか（代入の 1 行で足りるか、引数で渡ってくるなら呼び出し元まで見るか）。
2. 受け手の型を決められないとき、E3（誤）ではなく不明にする、という順を守れるか。

**この節で手引きが決めていないこと**: 見つからなかった。
関連する章: [第 48 章](ch48.md#s48-8)（手順 C、作例 3）、[第 49 章](ch49.md#s49-3)（形 2）、[第 51 章](ch51.md#s51-11)（rails-lens の実物）。

---

<a id="ah-5-21"></a>
### H-5.21 E4 受け手の型の読み違いで、動作の種類まで違う（手引き L461）

> 【原文 L461】
> | **E4** | 受け手の型の読み違いで、**動作の種類まで違う** | site のライブラリが違い、その結果 kind も違う | （kind が合っていれば E4 にしない。13 手順 C） |

**一言で言うと**: 解析器が受け手の型を読み違え、別のライブラリの関数だと思ったせいで、**動作の種類（kind）まで違う**効果を出した誤です。
ライブラリの名前だけが違って kind が合っていれば、E4 にはしません。

**ことばの確認**:
- **site のライブラリ**: site の名前の前半（`psycopg.Cursor.execute` なら psycopg）。
- **kind が違う**: たとえば、解析器は DB の書き込みと言うが、実際はただの文字列の処理だった、など。
- **13 手順 C**: 手引きの手順 C の「site 名のライブラリが違っていても、動作の種類（kind）が合っていれば判定には影響しない。`note` に書く」
  （`docs/drafts/final_judging_guide_draft.md:129-130`）。

**1 文ずつ読む**（表の E4 の行）:
- 記号 **E4**。類「**受け手の型の読み違いで、動作の種類まで違う**」。
- 見分け方「**site のライブラリが違い、その結果 kind も違う**」: 2 つの条件の両方です。
- これまでの例「**（kind が合っていれば E4 にしない。13 手順 C）**」: これまでの例の欄に、例ではなく注意が書かれています。v3・v4 には
  E4 の例が無かった、と本書は読みます（[第 51 章](ch51.md#s51-18)の当てはめの表にも E4 の行は無い）。

**なぜこう決めたのか**: 判定するのはコードの動作で、解析器の説明ではないからです（`docs/drafts/final_judging_guide_draft.md:56-57`）。
kind が合っていれば、宣言に反するかの材料（動作）は変わりません。kind まで違えば、解析器が主張した動作そのものが起きていません。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器は、受け手の値の形（`Path` か、どのクラスのオブジェクトか）から sink の名前を作ります（`authgap/effects.py:432-449`）。
  たとえば受け手の型が `sqlite3.Cursor` なら、`execute` は DB の sink に当たります（`authgap/catalog/sinks.py:504-510`）。
- だから、受け手の型の推論が外れると、別の kind の sink に当たりえます。kind は合っていて名前だけ違う例が、練習用サーバの `SELECT` を
  `psycopg.Cursor.execute` と表示する形です（sqlite3 と psycopg を同じ行にまとめた sink の行の名前で決まる。`authgap/catalog/sinks.py:514-517`
  の注記。`docs/drafts/final_judging_guide_draft.md:643`）。

**例で確かめる**:

（作った例。本書は走らせていない。仮の出力）受け手の型を、分岐の合流で読み違える形。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def describe(name: str, offline: bool = True) -> str:
    db = FakeCursor() if offline else sqlite3.connect("x.db").cursor()
    if offline:
        return db.execute(f"DELETE FROM t WHERE name = '{name}'")   # FakeCursor.execute は文字列を返すだけ
    return str(db.execute("SELECT * FROM t").fetchall())
```

仮に、解析器が `db` の型を `sqlite3.Cursor` と読み、4 行目を DB × `DELETE` の矛にしたとします。実際には、4 行目に届くとき `db` は
`FakeCursor`（文字列を作って返すだけの木の中のクラス）で、DB は変わりません。site のライブラリが違い、kind も違う（DB ではない）ので
**誤、E4**。（この例は説明のための仮の形で、凍結版の解析器が実際にこう読むかは確かめていません。）

（作った例。E4 にならない）練習用サーバの `conn.execute("SELECT …")` を、解析器が `psycopg.Cursor.execute` と表示しても、kind は DB で合っています。
判定に影響しないので `note` に書くだけです（`docs/drafts/final_judging_guide_draft.md:129-130`、`:643`）。

**迷いやすいところ**:
- **E3 と E4**: E3 は道筋の中の**呼び出し先**の取り違え（組み込みや同名メソッド）、E4 は効果の行の **site** の取り違えで kind まで違うもの
  （[第 51 章](ch51.md#s51-12)の表）。迷ったら E9 にして説明を書く（`docs/drafts/final_judging_guide_draft.md:468`）。
- **kind が違うのに、実際の動作も宣言に反する**: 下の【穴 H-5-16】。

**承認の前に自分に問うこと**:
1. 「site の名前が違うだけなら誤の原因にしない」という線引きに納得しているか。
2. 解析器が NET と言ったが実際は DB だった、のように kind は違うが両方とも宣言に反する形を、正にするか誤にするか。

**この節で手引きが決めていないこと**:

【穴 H-5-16】**kind は違うが、実際の動作も宣言に反する形は、正か誤（E4）か**
- 何が決まっていないか: E4 の類は「kind まで違う」ことしか書かず、実際の動作が宣言に反するときを除いていません。一方、11.2 は「理由（site 名や注記）が
  間違っていても、2 つの問いの答えが『はい』なら正」（`docs/drafts/final_judging_guide_draft.md:56-57`）と書き、組は kind を含む 5 つで決まります
  （`:38`）。[第 51 章](ch51.md#s51-12)が未決として挙げた形です。
- 困る事例（作った例）: 解析器が `store.delete(key)` をファイルの削除（FS_WRITE）と読んだが、実際は遠くの保存サービスの物を消す HTTP の `DELETE`
  （NET）で、D2 にはどちらでも反する。
- 考えられる選択肢: (a) 正（動作で判定。11.2）。(b) 誤 E4（組の kind が外れている）。(c) 手引きで決まらないとして不明（22 節）。
- 関係する決定: なし（手引き 11.1・11.2 の読み方の問題）。

関連する章: [第 48 章](ch48.md#s48-8)（手順 C）、[第 51 章](ch51.md#s51-12)。

---

<a id="ah-5-22"></a>
### H-5.22 E5 子プロセスの標準入力・パイプを書き込みと読んだ（手引き L462）

> 【原文 L462】
> | **E5** | 子プロセスの標準入力・パイプを書き込みと読んだ | `pipe:write` / `pipe:communicate` で、子が受け取ったものでファイルを変えない | ru-marketplace（v4）、helm / kubectl（v3、O41） |

**一言で言うと**: 子プロセスの標準入力にデータを流しただけなのに、解析器がそれを「ファイルへの書き込み」と読んだ誤です。

**ことばの確認**:
- **子プロセス**: ツールが起動した別のプログラム。
- **標準入力**: プログラムが入力を受け取る口。`Popen(..., stdin=PIPE)` で開き、`p.stdin.write(...)` や `p.communicate(input=...)` で流します。
- **`pipe:write` / `pipe:communicate`**: 解析器がこの 2 つの流し込みに付ける site の名前（`authgap/effects.py:851`）。

**1 文ずつ読む**（表の E5 の行）:
- 記号 **E5**。類「**子プロセスの標準入力・パイプを書き込みと読んだ**」。
- 見分け方「**`pipe:write` / `pipe:communicate` で、子が受け取ったものでファイルを変えない**」: site の名前と、子の動作の 2 つで見分けます。
- これまでの例「**ru-marketplace（v4）、helm / kubectl（v3、O41）**」。

**なぜこう決めたのか**: 15.1 の迷いやすい形が「子プロセスの標準入力への書き込み: それ自体はファイルを変えない。子プロセスがそれを受けて何をするかで決める」
としています（`docs/drafts/final_judging_guide_draft.md:333`）。解析器を直さない理由は O41 です。インタプリタの一覧に無い argv0 でも、標準入力は
コードの実行やファイルの書き込みに届く（`env python3`・`tee` など）ので、情報行は保守的な上界として正しい、として直すのを取り消した
（`docs/open_questions.md:1070-1072`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器は、受け手が `Popen` などの子プロセスの取っ手で、`stdin.write` / `communicate` なら、効果を 1 行出します（`authgap/effects.py:803-864`）。
- 子がシェルか、argv0 がインタプリタの一覧にあれば kind を `EXEC`、それ以外なら `FS_WRITE` にします（`authgap/effects.py:844-847`）。
  子が何をするかは見ません。
- D1 では FS_WRITE はすべて矛（`authgap/dparse.py:379-380`）、EXEC も矛（`:375-376`）です。

**例で確かめる**:

（作った例。本書の試験 D の `sort_lines`）

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def sort_lines(text: str) -> str:
    p = subprocess.Popen(["sort"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate(input=text)
    return out
```

解析器は `sort_lines` × `pipe:communicate` × D1 に `fs_write` の矛を出しました（試験 D。同じツールの `subprocess.Popen` には不 `spawn_command`）。
`sort` は受け取った行を並べ替えて標準出力に返すだけで、ファイルを変えません。**誤、E5**。

（作った例の変種）`["tee", "/var/log/out.txt"]` に流すなら、子がファイルに書くので D1 に反し**正**（[第 50 章](ch50.md#s50-5)）。ラベルは `tee` が
書くファイルで決めます（この例ならログか、その他・不明）。

（作った例。境界。本書の試験 A の `summarize`）子が Python で、標準入力はデータ。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def summarize(data: str) -> str:
    p = subprocess.Popen(["python3", "summarize.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = p.communicate(input=data)
    return out
```

解析器は `summarize` × `pipe:communicate` × **EXEC** × D1 に `exec` の矛を出しました（試験 A）。argv0 の `python3` がインタプリタなので、
流し込みを「コードの実行」と読んだのです。けれども `python3 summarize.py` は、標準入力をコードとしてではなく、データとして読みます
（`summarize.py` が環境を変えないと確かめられれば）。子はファイルを変えないので誤ですが、解析器は「書き込み」ではなく「コードの実行」と
読んでいます。E5 の類の文（書き込みと読んだ）に当たるかは、下の【穴 H-5-14】です。

**迷いやすいところ**:
- **`pipe:` の矛がいつも E5 ではない**: 子が何をするかで決めます。`sort`・`wc` なら誤、`tee <ファイル>`・`sh` なら正になりえます（[第 50 章](ch50.md#s50-5)）。
- **同じツールの SPAWN の組は別の組**: `subprocess.Popen` × SPAWN の不は、不の中身の判定の側です。

**承認の前に自分に問うこと**:
1. 子のプログラム（`summarize.py` のような木の中のスクリプト）の中身まで読んで「ファイルを変えない」と言うのは、深さの数え方（18.2 の深さ 4）と
   どう関係するか。矛の判定では深さの制限は無いと考えてよいか。
2. 解析器が EXEC と読んだ流し込みの誤を、E5 と呼ぶか、E9 と呼ぶか。

**この節で手引きが決めていないこと**:

【穴 H-5-14】**パイプの流し込みを解析器が EXEC（コードの実行）と読んだ誤は E5 か**
- 何が決まっていないか: E5 の類は「書き込みと読んだ」、見分け方は「`pipe:write` / `pipe:communicate` で、子が受け取ったものでファイルを変えない」
  です。解析器は子がインタプリタなら流し込みを EXEC にする（`authgap/effects.py:844-846`）ので、site は `pipe:` でも kind が EXEC の誤が
  ありえます。見分け方（site）では E5、類の文（書き込みと読んだ）では E5 でない、と割れます。
- 困る事例: 上の試験 A の `summarize`。
- 考えられる選択肢: (a) site が `pipe:` なら kind によらず E5。(b) kind が EXEC なら E5 ではなく E9（説明を書く）。(c) E5 の類の文を
  「書き込み・コードの実行と読んだ」と読み替える一言を足す。
- 関係する決定: O41（`docs/open_questions.md:1070-1072`）。

関連する章: [第 48 章](ch48.md#s48-8)（作例 4）、[第 50 章](ch50.md#s50-5)、[第 51 章](ch51.md#s51-13)（ru-marketplace と helm / kubectl の実物）。

---

<a id="ah-5-23"></a>
### H-5.23 E6 到達しない（E1 以外）（手引き L463）

> 【原文 L463】
> | **E6** | 到達しない（E1 以外）: 死んだコード・別の入口だけ・定数で閉じた枝・必ず先に抜ける | 第 14.2 節 | |

**一言で言うと**: 起動時の初期化（E1）以外の理由で、ツールの呼び出しでは効果に届かない誤です。4 つの形をまとめた類です。

**ことばの確認**:
- **死んだコード**: どこからも呼ばれていない関数の中の効果。
- **別の入口だけ**: CLI・テスト・スクリプトからだけ呼ばれ、ツールの道筋からは呼ばれない。
- **定数で閉じた枝**: `if False:` や、定数で偽になり書き換えられない `if DEBUG:` の中。
- **必ず先に抜ける**: 効果の前で必ず `return` / `raise` する。

**1 文ずつ読む**（表の E6 の行）:
- 記号 **E6**。類「**到達しない（E1 以外）: 死んだコード・別の入口だけ・定数で閉じた枝・必ず先に抜ける**」。
- 見分け方「**第 14.2 節**」: 14.2 の表の、原因が E6 の 3 つの行（`docs/drafts/final_judging_guide_draft.md:244-246`）と、「別の入口からしか
  呼ばれないことは、木の中を検索して確かめる」（`:248`）。
- これまでの例「（空）」: v3・v4 では、この類の誤は記録されていません（本書の読み）。

**なぜこう決めたのか**: E1 を除いた到達しない形を 1 つにまとめた理由は書かれていません。本書の読み: E1 は D67 の 2 で別に件数を報告すると
決まった類なので、それ以外を 1 つにまとめた（[第 49 章](ch49.md#s49-3)の「E1 だけが 1 つの形に専用の記号」）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器は、同じ関数の本体の中で `return` / `raise` で必ず終わった後の文は実行しません（`authgap/val/engine.py:291-308`）。
- `if` の条件は、ローカルの名前・リテラルなどで定数に決まるときだけ片方の枝にします。**属性・呼び出し・添字は評価しない**（誤って枝を捨てない
  ため。`authgap/val/engine.py:2731-2735`）。だから `if settings.DEBUG:` のような属性の条件は両方の枝を実行し、閉じた枝の効果も出します。
- 呼んだ関数が必ず例外を投げることまでは使っていない、と[第 51 章](ch51.md#s51-14)は試験から読んでいます（解析器のコードで確かめたものではない、
  と同章が書いている）。

**例で確かめる**:

（作った例。本書の試験 C の `status`。`settings.py` は `DEBUG = False` の 1 行）

```python
import settings

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def status() -> str:
    if settings.DEBUG:
        with open("debug.txt", "w") as fh:
            fh.write("status called")
    return "ok"
```

解析器は `status` × `builtins.open` × D1 に `fs_write` の矛を出しました（試験 C）。`settings.DEBUG` は `False` の定数で、木の中で書き換える行が
無ければ（`grep -rn "DEBUG\s*=" .` で確かめる）、枝は閉じています。**誤、E6**（定数で閉じた枝）。

（作った例の変種。E6 にならない）`DEBUG = os.environ.get("DEBUG") == "1"` なら、運用者の設定で届くので「到達する」、条件の種類は「運用者の設定」
（`docs/drafts/final_judging_guide_draft.md:262`）。正になりえます。

（作った例。境界）効果のある関数が CLI からだけ呼ばれているように見えるが、プラグインの読み込み（`getattr(mod, name)()`）でツールからも
呼ばれうる。呼び出し先が決まらないので、E6 にせず**不明**（`docs/drafts/final_judging_guide_draft.md:580`）。

**迷いやすいところ**:
- **「到達しないなら全部 E6」ではない**: 起動時の初期化は E1、取り違えは E3・E4（[第 49 章](ch49.md#s49-3)）。
- **grep で確かめる**: 定数が書き換えられないこと、別の入口からしか呼ばれないことは、「無いこと」の確認なので木の全体を検索します。

**承認の前に自分に問うこと**:
1. 「定数で、どこでも書き換えない」を確かめる範囲は、木の中だけでよいか（外のライブラリや設定の読み込みで書き換わる形は不明か）。
2. 4 つの形を 1 つの E6 にまとめると、集計で区別できなくなります。説明の文で形を書けば足りるか。

**この節で手引きが決めていないこと**: 見つからなかった（必ず抜けるかを読み切れない形は 19 節の不明）。
関連する章: [第 49 章](ch49.md#s49-3)（形 3〜5）、[第 51 章](ch51.md#s51-14)（必ず例外を投げる関数の後ろの試験）。

---

<a id="ah-5-24"></a>
### H-5.24 E7 モデルが決められないのに決められるとした（手引き L464）

> 【原文 L464】
> | **E7** | モデルが決められないのに決められるとした | 固定のコマンドに `shlex.quote` した値だけを渡す spawn など | v3（O41） |

**一言で言うと**: 解析器が「モデルがこの値を選べる」と読んだのに、実際にはモデルは選べず、そのうえ固定の動作は宣言に反しない誤です。

**ことばの確認**:
- **決められる**: 原理 3-a の前提。モデルの値が、その位置（起動するコマンド、書き先のパス、宛先など）まで届き、値を選べること。
- **`shlex.quote`**: 文字列をシェルにとって 1 つの引数になるよう引用符で包む関数（[第 9 章](ch09.md)）。
- **spawn**: プロセスの起動。

**1 文ずつ読む**（表の E7 の行）:
- 記号 **E7**。類「**モデルが決められないのに決められるとした**」。
- 見分け方「**固定のコマンドに `shlex.quote` した値だけを渡す spawn など**」: 「など」なので、spawn 以外（書き先・宛先）にも当たりえます。
- これまでの例「**v3（O41）**」: v3 の clawking（[第 51 章](ch51.md#s51-15)）。

**なぜこう決めたのか**: 15.1 の SPAWN の行が「コマンドが定数なら、そのコマンドが実際に何をするかを調べ、環境を変えるなら反する・変えないなら
反しない」としています（`docs/drafts/final_judging_guide_draft.md:320`）。モデルが選べないと分かり、固定のコマンドが反しないと分かったときの
誤がこれです。解析器を直さない理由は O41 に名指しがあるだけです（`docs/open_questions.md:1065`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- 解析器の「モデルが選べる」は、slot の値の主体が MODEL で確度が resolved であることです（`authgap/dparse.py:245-262`）。選べれば矛、
  流れ込むだけなら `…_opaque` の不です（`:265-272`）。
- `shlex.quote` は、値の主体を変えず、「quoted」という属性を付けるだけの変換です（`authgap/catalog/transfers.py:67`）。val は等級を付けない
  （`authgap/val/engine.py:8-10`）。だから引用した値が入ったシェルの文字列も「モデルが選べる」になり、`spawn_model` の矛になります
  （`authgap/dparse.py:377-378`）。

**例で確かめる**:

（作った例。走らせていない）固定のコマンドに引用した値を渡し、`--` で選択肢も閉じる。

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def count_lines(path: str) -> str:
    return subprocess.run(f"wc -l -- {shlex.quote(path)}", shell=True, capture_output=True, text=True).stdout
```

解析器はシェルの文字列にモデルの値が入るので `spawn_model` を出すはずです（下の試験 D と同じ形）。けれども、起動されるのはいつも `wc -l` で、
`--` の後の値はファイル名としてしか読まれません。`wc` は読むだけなので D1 に反しません。**誤、E7**。

（作った例。本書の試験 D の `history`。境界）

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def history(ref: str) -> str:
    return subprocess.run(f"git log --oneline {shlex.quote(ref)}", shell=True, capture_output=True, text=True).stdout
```

解析器は `history` × `subprocess.run` × D1 に `spawn_model` の矛を出しました（試験 D）。一見 E7 ですが、`shlex.quote` は**選択肢**までは防ぎません。
モデルが `ref` に `--output=/home/u/.bashrc` を入れると、`git log` はその選択肢を受け付けてファイルに書きます（本書の執筆時に git 2.43.0 で、
`git log --oneline -1 '--output=<ファイル>'` がファイルを作ることを確かめた）。取りうる値の全体で読めば（原理 3-a）環境を変えうるので、
E7 にはできません（正。[第 51 章](ch51.md#s51-15)の「引用は選択肢までは防がない」、[第 50 章](ch50.md#s50-12)の候補 3）。

**迷いやすいところ**:
- **E7 は 2 段**: (1) モデルが選べない、と分かる。(2) そのうえで、固定の動作が宣言に反しない、と分かる。(1) だけでは誤になりません
  （[第 51 章](ch51.md#s51-15)の表）。
- **書き先や宛先の E7**: 「など」に入る形。たとえばモデルの値がファイル名に入るが、置き場とモードで既存のファイルに当たらない、など。
  ただし E8 との境になります（[H-5.25](#ah-5-25) の【穴 H-5-15】）。

**承認の前に自分に問うこと**:
1. 選択肢として読まれうるか（`-` で始まる値）を、コマンドごとに調べる手間を、判定の時間の見込みに入れているか。
2. 「モデルが選べない」と「固定の動作が反しない」の両方が要ることに納得しているか。

**この節で手引きが決めていないこと**: E7 と E8 の境は [H-5.25](#ah-5-25) の【穴 H-5-15】で挙げる。定数のコマンドの引数を
モデルが決める形の判定（正・誤）は第 15 節の側の穴として[第 50 章](ch50.md#s50-12)の候補 3 が挙げている。
関連する章: [第 50 章](ch50.md#s50-4)（作例 `toy_d1c`）、[第 51 章](ch51.md#s51-15)（clawking の実物）。

---

<a id="ah-5-25"></a>
### H-5.25 E8 宣言に反しない（E2 以外）（手引き L465）

> 【原文 L465】
> | **E8** | 宣言に反しない（E2 以外）: 冪等な追記（D4）、`flock` のための `'a'`（D4）、読み取りのモード、接続単位の設定など | 第 15 節 | ccr の条件つき追記（v4 の E00） |

**一言で言うと**: 効果には届くが、宣言に反しない誤のうち、E2（自分が作った一時ファイルの後始末）以外のものです。

**ことばの確認**:
- **冪等な追記**: 書く前に内容を確かめ、すでにあれば書かない追記。2 回目は何も足さないので、D4 に反しません。
- **`flock` のための `'a'`**: ファイルにロックを掛けるために `'a'` で開くだけで、何も書かない形。
- **読み取りのモード**: `open` のモードが `'r'` / `'rb'` で、書かない。
- **接続単位の設定**: `PRAGMA foreign_keys=ON` / `BEGIN` / `COMMIT` など、接続を閉じれば消えるもの。

**1 文ずつ読む**（表の E8 の行）:
- 記号 **E8**。類「**宣言に反しない（E2 以外）: 冪等な追記（D4）、`flock` のための `'a'`（D4）、読み取りのモード、接続単位の設定など**」。
- 見分け方「**第 15 節**」: 宣言ごとの問いの表と迷いやすい形（D4 は `docs/drafts/final_judging_guide_draft.md:398-399`、D1 は `:323`・`:328`）。
- これまでの例「**ccr の条件つき追記（v4 の E00）**」（`docs/drafts/final_judging_guide_draft.md:681`）。

**なぜこう決めたのか**: 「宣言に反しない」の誤の受け皿です。E2 だけを別にしたのは、O41・O43 で同じ類が繰り返し出たからと本書は読みます
（`docs/open_questions.md:1063-1064`、`:1191`）。`flock` の形は O41 に名指しがあります（`:1069`）。

**解析器の仕組み（なぜこの誤が出るか）**:
- D4 では、`open` のモードに `a` が入っていれば `fs_append` の矛にします（`authgap/dparse.py:531-532`）。書く前に確かめているか、
  開くだけで書かないかは見ません。
- `open` のモードが定数で読めないとき、解析器は**読みと書きの両方の効果を出します**（「clean に潰さない」。`authgap/effects.py:656-663`）。
  だから、モードが `"rb" if binary else "r"` のような読み取りの 2 択でも、D1 の `fs_write` の矛が出ることがあります（[第 48 章](ch48.md#s48-8)の作例 6）。
- 接続単位の SQL は、解析器も宣言の内にします（`authgap/dparse.py:497`）。だから E8 の「接続単位の設定」は、SQL の読み違いなどで解析器が
  変更の文と読んだときに起きる、と本書は読みます（走らせて確かめた例はありません）。

**例で確かめる**:

（作った例。本書の試験 C の `mark_seen`）

```python
@mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
def mark_seen(tag: str) -> str:
    path = "seen.txt"
    if os.path.exists(path) and tag in open(path).read().split():
        return "already"
    with open(path, "a") as fh:
        fh.write(tag + "\n")
    return "added"
```

解析器は `mark_seen` × `builtins.open` × D4 に `fs_append` の矛を出しました（試験 C）。同じ `tag` で 2 回呼ぶと、2 回目は `already` で抜け、
書きません。D4 に反しない（`docs/drafts/final_judging_guide_draft.md:398`）ので、**誤、E8**。

（作った例の変種）確かめずに毎回 `'a'` で足すなら、2 回目もさらに 1 行増えるので D4 に反し**正**（ラベルはログか、状態の保存か、読み返しで決める）。

（作った例。境界。本書の試験 B の `export_new`）

```python
@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def export_new(path: str, body: str) -> str:
    if os.path.exists(path):
        raise FileExistsError(path)
    with open(path, "w") as fh:
        fh.write(body)
    return "ok"
```

解析器は `export_new` × `builtins.open` × D2 に `fs_writeout_model_path` の矛を出しました（試験 B）。モデルは書き先を選べますが、既存の
ファイルを指したときは必ず先に `raise` で抜けるので、上書きは起きません（存在の確認と書き込みのあいだに別の処理がファイルを作る、という
競合を考えなければ）。誤だとすると、原因は 3 通りに読めます。(1) E8: 書き出しだが既存を上書きしないので D2 に反しない。(2) E7: モデルは
「既存のファイル」を選べないのに選べるとした。(3) E6 に近い: 既存のファイルの場合だけ、効果の前に必ず抜ける。下の【穴 H-5-15】です。
（競合を考えるなら、判定そのものが「決められない」になりえます。）

**迷いやすいところ**:
- **E2 と E8**: D2 で自分が作ったものを消すのは E2。そのほかの「反しない」は E8。
- **読み取りのモードは手順 C で気づく**: 効果の行を開き、モードを見れば分かります（`docs/drafts/final_judging_guide_draft.md:125`）。

**承認の前に自分に問うこと**:
1. 「書く前に確かめる追記」を冪等とみなすとき、確かめ方が不完全（たとえば部分一致で調べる）なら、どう判定するか。
2. 試験 B の `export_new` の原因を、自分なら何と書くか。

**この節で手引きが決めていないこと**:

【穴 H-5-15】**E6・E7・E8 の境 — 既存の書き先を指したときだけ必ず先に抜ける書き出し**
- 何が決まっていないか: 試験 B のように、モデルが書き先を選べるが、既存のファイルを指すと必ず先に抜ける形の誤を、どの記号にするかが
  決まっていません。E7 の「決められないのに決められるとした」、E8 の「宣言に反しない」、E6 の「必ず先に抜ける」の 3 つに部分的に当たります。
  手引きの規則「分類に迷ったら E9」（`docs/drafts/final_judging_guide_draft.md:468`）で E9 に行けますが、「迷う」かどうかは判定者しだいなので、
  同じ形が E7・E8・E9 に割れうる、というぶれが残ります。
- 困る事例: 試験 B の `export_new`。
- 考えられる選択肢: (a) E8（宣言の問いで落ちたので「反しない」の受け皿）。(b) E7（モデルの能力の読み違い）。(c) 迷ったら E9 の規則を当て、
  `note` に 3 つの読みを書く。(d) この形を 16.2 のような「境界の例」として 17 節に先に書いておく。
- 関係する決定: D67 の 2（`docs/decisions.md:3773-3778`）、原理 3-a。

関連する章: [第 48 章](ch48.md#s48-8)（作例 6 の読み取りのモード）、[第 50 章](ch50.md#s50-9)（D4 の 3 つの `fs_append`）、[第 51 章](ch51.md#s51-16)（ccr と helios の実物）。

---

<a id="ah-5-26"></a>
### H-5.26 E9 その他（手引き L466）

> 【原文 L466】
> | **E9** | その他 | 自由記述 | |

**一言で言うと**: E1〜E8 のどれにも当たらない誤、または分類に迷った誤です。記号だけでなく、説明を自由に書きます。

**ことばの確認**:
- **自由記述**: 決まった言葉ではなく、自分の言葉で書く説明。

**1 文ずつ読む**（表の E9 の行）:
- 記号 **E9**。類「**その他**」。見分け方「**自由記述**」。これまでの例「（空）」。

**なぜこう決めたのか**: 迷った件を近い類に押し込むと、その類の件数に、本当にそうかは分からない件が混ざります（[第 51 章](ch51.md#s51-17)）。
規則は結びの文（L468）にあります（[H-5.27](#ah-5-27)）。

**解析器の仕組み（関わる例）**: D3 の宛先の類は、`localhost`・`〜.localhost`・`〜.local` と、明示の網（loopback・RFC 1918・ULA・link-local・未指定）
だけを local にし、ほかの名前は外部にします（`authgap/dparse.py:293-301`、`:349-352`）。ドットの無い名前や `〜.internal` は外部になります。

**例で確かめる**:

（作った例。本書の試験 A の `ask_ollama`）

```python
@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def ask_ollama(prompt: str) -> str:
    return requests.post("http://ollama:11434/api/generate", json={"prompt": prompt}).text
```

解析器は `ask_ollama` × `requests.post` × D3 に `net_external_host` の矛を出しました（試験 A）。手引きは、ドットの無い名前（`ollama`）を
local とするので、D3 に反しません。判定は**誤**で、手引きは原因を「語彙・定義の差（第 17 節）」と書いています
（`docs/drafts/final_judging_guide_draft.md:387-388`。D73 の 2 も同じ言葉。`docs/decisions.md:4015-4016`）。けれども、第 17 節の E1〜E9 に
「語彙・定義の差」という類はありません。E1〜E8 のどれにも当たらないので E9、と読むのが自然ですが、手引きはそう書いていません
（下の【穴 H-5-12】）。

（作った例。E9 になりうる形）モデルの URL を検証して `127.0.0.1` のポートだけを選ばせているのに、解析器が `net_model_host` を出した。
E7（選べないのに選べるとした）か E8（反しない）かで迷うので、規則どおり E9 にして説明を書く（[第 50 章](ch50.md#s50-8)の結び）。

**迷いやすいところ**:
- **E9 と不明**: E9 は誤の原因です。判定そのものが決められないなら、誤ではなく不明（`unknown_reason`）。
- **E9 は手抜きではない**: 迷った件を正直に分けておく記号です。説明の文があれば、後で集め直せます。

**承認の前に自分に問うこと**:
1. ドットの無い名前・`〜.internal` で出た D3 の誤を、E9 と書くか、「語彙・定義の差」を 1 つの記号として足すか。
2. E9 の説明の書き方（たとえば先頭に短い見出しの言葉を置く）をそろえる約束が要るか。

**この節で手引きが決めていないこと**:

【穴 H-5-12】**15.3 の「原因は語彙・定義の差（第 17 節）」に当たる記号が、E1〜E9 に無い**
- 何が決まっていないか: 15.3 は、解析器がドットの無い名前・`〜.internal` の名前で D3 の矛を出していたら、判定は誤で「原因は語彙・定義の差
  （第 17 節）」と書きます（`docs/drafts/final_judging_guide_draft.md:387-388`）。けれども、第 17 節の表にこの類はありません。どの記号を
  `error_class` に書くかが決まっていません。
- 困る事例: 試験 A の `ask_ollama`（`http://ollama:11434`）。`http://host.docker.internal:8000` も同じ（D73 の 2 の追記、`docs/decisions.md:4018-4025`）。
- 考えられる選択肢: (a) E9 にし、説明に「語彙・定義の差: ドットの無い名前」と書く。(b) 第 17 節に新しい記号（たとえば「語彙・定義の差」）を
  足す（封の前なら手引きの変更として足せる）。(c) E8（宣言に反しない）とみなす。
- 関係する決定: D73 の 2（`docs/decisions.md:4012-4025`）。

関連する章: [第 50 章](ch50.md#s50-8)（D3 の local の範囲）、[第 51 章](ch51.md#s51-17)、[第 10 章](ch10.md)（ドットの無い名前）。

---

<a id="ah-5-27"></a>
### H-5.27 第 17 節の結び — 迷ったら E9、内訳は限界の材料（手引き L468）

> 【原文 L468】
> 分類に迷ったら E9 にして説明を書く。**分類は集計で「誤の原因の内訳」になり、論文の限界の節の材料になる。**

**一言で言うと**: 分類に迷ったら E9 にして説明を書きます。誤の原因の分類は集計で「誤の原因の内訳」になり、論文の限界の節の材料になります。

**ことばの確認**:
- **誤の原因の内訳**: 誤を E1〜E9 ごとに数えた表。事前登録の下書きの参考と併記に「誤の原因の内訳（E1〜E9）」があります
  （`docs/drafts/prereg_2_12_draft.md:140`）。
- **論文の限界の節**: 解析器や評価の弱いところを正直に書く節。

**1 文ずつ読む**:
1. 「**分類に迷ったら E9 にして説明を書く。**」: E1〜E8 の 2 つで迷ったら、どちらにも入れず E9。説明の文に、どれとどれで迷ったかを書きます。
2. 「**分類は集計で『誤の原因の内訳』になり、**」: 1 件ずつの `error_class` が、論文の表の 1 行 1 行になります。
3. 「**論文の限界の節の材料になる。**」: たとえば E1 の件数は「各呼び出しをサーバの状態を仮定せずに独立に解析する設計の限界（誤警報の向き）」
   として書かれます（`docs/open_questions.md:1215`、D67 の 2 `docs/decisions.md:3777`）。

**なぜこう決めたのか**: D67 の 2 が「設計の選択による限界（誤警報の向き）として件数を報告する」と決めたこと（`docs/decisions.md:3777-3778`）の延長です。
迷った件を近い類に入れないのは、類ごとの件数を信用できるものにするためです（本書の読み。[第 51 章](ch51.md#s51-17)）。

**例で確かめる**: [H-5.26](#ah-5-26) の「検証で local に絞った URL」の例（E7 か E8 か迷う → E9）。[H-5.25](#ah-5-25) の試験 B の `export_new`
（E6・E7・E8 で迷う → この規則なら E9）。

**迷いやすいところ**:
- **「迷う」の線**: どこから「迷った」とするかは判定者しだいです。1 人の判定者の中でも、日によって E8 と書いたり E9 と書いたりしうる、
  というぶれが残ります（【穴 H-5-15】）。
- **E9 が多いのは悪いことではない**: 用意した類で分けきれない誤が多かった、という事実になります。

**承認の前に自分に問うこと**:
1. 「迷ったら E9」と「原因が 2 つ重なったら」（【穴 H-5-13】）は、同じ件で両方当たりうる。そのときの書き方を決めておくか。
2. 誤の原因の内訳の表を、論文のどこに、どの粒度で載せたいか。

**この節で手引きが決めていないこと**: 見つからなかった（重なりは【穴 H-5-13】、迷うかどうかのぶれは【穴 H-5-15】）。
関連する章: [第 51 章](ch51.md#s51-18)（2 つの内訳の表と、v3・v4 の誤を E に当てた表）。

---
<a id="ah-5-x"></a>
### H-5.x この分冊のまとめ

- 判定を決めた**後**に、正には「何を変えた違反か」のラベルを 1 つ、誤には「なぜ解析器が間違えたか」の記号を 1 つ付けます。どちらも判定
  （正・誤）を変えません（D67 の 1・D68 の 3、`docs/decisions.md:3767-3772`、`:3809-3814`）。
- **ラベルは重みではありません**。理由は、研究の問いが「宣言は正しいか」であること、重みの線引きに正解が無いこと、結果を見た後で
  数字を作り直すと恣意的に見えることです（`docs/decisions.md:3770-3771`）。内訳は「些細では」という問いに事実で答えるために出します（`:3772`）。
- 書き込み先の種類は 8 つで、**上から順に当てはめ、最初に当てはまったもの**を付けます（L413）。順番の理由は書かれていません。
  順 1 だけが kind（NET）を条件にし、順 7 は kind（SPAWN / EXEC）で定義され、順 2〜6 は書き先の性質で定義されています。
- **名前ではなく動作で決めます**。「キャッシュ」の名前でも読み返さなければ順 6 ではない（20.1 の組 1。L652-655）。
- 境界の 6 つの事例は先に決めてあり（L430-435）、決められない事例は「その他・不明」にして `note` に書き、途中で定義を足しません（L437-438）。
- D3 の正には、通信先の種類（定数の外部ホスト / モデルが決める宛先 / モデルが決めるコード・コマンド / その他・不明）を、同じ `write_target`
  欄に書きます。分け目は「宛先（またはコマンド）を誰が決めるか」で、16.3 には「上から順」の規則がありません。
  16.3 の「その他・不明」の例の形（運用者の設定で、既定値が外部）には、解析器はふつう矛ではなく不を出すので、D3 の正としては
  判定に出にくい、と本書の試験 E で分かりました（D3 の不は判定しない。L535）。
- 誤の原因 E1〜E9 は、v3・v4 で出た類を最初から用意したものです。どの類も、解析器の具体的な仕組みから生まれます。
  E1 は守りの `if` の両方の枝を実行すること（`authgap/val/engine.py:334-352`）、E2 は削除が破壊的かを sink の属性だけで決めること
  （`authgap/dparse.py:365-368`）、E3 は末尾名だけの解決（`authgap/val/engine.py:1029-1041`）、E4 は受け手の型からの sink の当て方
  （`authgap/effects.py:432-449`）、E5 はパイプの流し込みを子の動作を見ずに効果にすること（`authgap/effects.py:844-847`）、E6 は属性の条件や
  呼んだ関数の例外を使わないこと（`authgap/val/engine.py:2731-2735`）、E7 は `shlex.quote` を属性としてしか扱わないこと
  （`authgap/catalog/transfers.py:67`）、E8 は `'a'` のモードだけで追記の矛にすること（`authgap/dparse.py:531-532`）。
- 本書の試験（作った例を凍結版の解析器で走らせたもの）で、E1・E2・E3・E5・E6・E7（の形）・E8 の矛が実際に出ることを確かめました。
  E4 は走らせていない仮の例です。
- 分類に迷ったら E9 にして説明を書きます（L468）。誤の原因の内訳は、論文の限界の節の材料になります。
- 手引きが決めていないこと（穴）が 16 個見つかりました（下の表）。どれも本書は決めていません。

<a id="ah-5-y"></a>
### H-5.y この分冊の穴の一覧

| 番号 | 節 | 中身 | 関係する決定 |
|---|---|---|---|
| 【穴 H-5-1】 | [H-5.11](#ah-5-11) | 1 組で正にした位置が複数あり種類が違うとき、どの位置でラベルを決めるか（手順 G の「1 つ正で止めてよい」と合わせると、読む順でラベルが変わる） | D68 の 1、D67 の 1 |
| 【穴 H-5-2】 | [H-5.9](#ah-5-9) | 書き込みが子プロセス・コードの実行を通るとき、順 2〜6（変えたもの）と順 7（SPAWN / EXEC）のどちらを先に当てるか | D68 の 3 |
| 【穴 H-5-3】 | [H-5.5](#ah-5-5) | 運用者が環境変数・設定ファイルで決めた場所への書き込みは「利用者が指定した場所」か | D67 の 1 |
| 【穴 H-5-4】 | [H-5.6](#ah-5-6) | 「読み返す / 読み返さない」の主語は、判定しているツールか、同じサーバの別のツールも含むか | D67 の 1 |
| 【穴 H-5-5】 | [H-5.7](#ah-5-7) | OS の一時領域に置いて後で読み返すもの（順 5 か順 6 か）と、「OS の一時領域」の範囲（`$TMPDIR`・`/var/tmp`・`mkstemp(dir=…)`） | D67 の 1 |
| 【穴 H-5-6】 | [H-5.8](#ah-5-8) | 初回に作る作業ディレクトリで、中身を読み返さないもの（順 6 か順 8 か）。第 53 章の考え方の例との【食い違い】つき | D67 の 1 |
| 【穴 H-5-7】 | [H-5.11](#ah-5-11) | 前の呼び出しが残した受け渡しファイルの削除（16.2 の 1 行目の括弧の (a)）のラベル。v4 の M20 | D67 の 1 |
| 【穴 H-5-8】 | [H-5.10](#ah-5-10) | 「その他」と「不明」を 1 つにした箱を、集計や `note` で分けるか（16.1 と 16.3 の両方） | D67 の 1、D68 の 3 |
| 【穴 H-5-9】 | [H-5.14](#ah-5-14) | ホストの一部（サブドメイン・選択肢）をモデルが決めるが、定数の外部ドメインの中に閉じる形の通信先の種類 | D68 の 3 |
| 【穴 H-5-10】 | [H-5.15](#ah-5-15) | 固定のコマンドの引数としてモデルが宛先を渡す形（`curl <引用した URL>`）が 2 つの通信先の種類に当たる。16.3 に当てはめる順が無い | D68 の 3 |
| 【穴 H-5-11】 | [H-5.13](#ah-5-13) | リポジトリの中の設定ファイルに書かれた外部ホストは「コードに書かれた」か「運用者の設定」か | D68 の 3 |
| 【穴 H-5-12】 | [H-5.26](#ah-5-26) | 15.3 の「原因は語彙・定義の差（第 17 節）」に当たる記号が E1〜E9 に無い（ドットの無い名前・`〜.internal` の D3 の誤） | D73 の 2 |
| 【穴 H-5-13】 | [H-5.17](#ah-5-17) | 1 つの誤に原因が 2 つ以上重なるとき、`error_class` に 1 つ書くか `;` で並べるか | D67 の 2 |
| 【穴 H-5-14】 | [H-5.22](#ah-5-22) | パイプの流し込みを解析器が EXEC（コードの実行）と読んだ誤（子がインタプリタで、標準入力はデータ）は E5 か | O41 |
| 【穴 H-5-15】 | [H-5.25](#ah-5-25) | 既存の書き先を指したときだけ必ず先に抜ける書き出し（試験 B）の誤は E6・E7・E8 のどれか。「迷ったら E9」の「迷う」の線のぶれ | D67 の 2 |
| 【穴 H-5-16】 | [H-5.21](#ah-5-21) | kind は違うが実際の動作も宣言に反する形は、正か誤（E4）か | なし（手引き 11.1・11.2 の読み方） |

**【食い違い】の一覧**（1 件）:

| 節 | 手引き | 教科書 |
|---|---|---|
| [H-5.8](#ah-5-8) | 16.2: 「初回だけ `~/.app/` を作る → キャッシュ・状態の保存（作業ディレクトリ）」（`docs/drafts/final_judging_guide_draft.md:432`） | [第 53 章](ch53.md#s53-6): 練習用サーバの `os.makedirs(CACHE_DIR, exist_ok=True)` を、本記録者の考え方の例として「その他・不明」（`docs/textbook/ch53.md:1143`、`:1219`、`:1276-1333`）。同章は字義どおりの読みもありうると書いている |

すでに[第 51 章](ch51.md)が「未決」として挙げていたもの: 【穴 H-5-1】（51.5 の 4）、【穴 H-5-2】（51.5 の 3）、【穴 H-5-5】の (i)（51.5 の 2）、
【穴 H-5-7】（51.5 の 1）、【穴 H-5-13】（51.16）、【穴 H-5-16】（51.11）。ほかの 10 個は、この分冊で新しく挙げたものです。

<a id="ah-5-z"></a>
### H-5.z 確認問題

**問 1**: 読み取り専用（D1）のツールが、毎回 `server.log` に 1 行追記していました。判定とラベルは何ですか。「軽いので誤にする」はなぜできませんか。

<details><summary>答え</summary>

判定は**正**、ラベルは**ログ**（記録のためだけに書き、読み返さない。読み返しが無いことは grep で確かめる）。ログでもファイルの書き込みは
D1 に反します（`docs/drafts/final_judging_guide_draft.md:318`）。手引きは「軽重は書き込み先の種類のラベルで表し、判定の正誤には持ち込まない」
と書き（`:63-64`）、D67 の 1 は重みを付けないと決めています（`docs/decisions.md:3767`）。ラベルは判定の**後**に付ける事実の記録です（[H-5.1](#ah-5-1)）。

</details>

**問 2**: SQLite のファイルを検索結果のキャッシュとして使い、`INSERT` で足しているツールの D1 の正には、どのラベルを付けますか。根拠の規則も答えてください。

<details><summary>答え</summary>

**データベース**。16.1 は「上から順に当てはめ、最初に当てはまったものを付ける」（L413）。順 2「DB の行を変える」が、順 6「後で読み返す」より
先に当たります。16.2 の最後の行も「SQLite のキャッシュ DB への書き込み → データベース。順 2 が順 6 より先」と名指ししています（L435。[H-5.2](#ah-5-2)）。

</details>

**問 3**: モデルが `log_to` という引数でログの書き先を決められるツールが、そこに追記していました（D1 の正）。ラベルは何ですか。

<details><summary>答え</summary>

**利用者のファイル**。目的はログ（順 4）ですが、順 3 の「利用者（またはモデル）が指定した場所のファイル」が先に当たります（[H-5.5](#ah-5-5) の作った例 3）。

</details>

**問 4**: D3 の組で、`requests.get("https://api.weather.example.com/v1/now", params={"q": city})`（`city` はツールの引数）を正にしました。
通信先の種類は「モデルが決める宛先」ですか。

<details><summary>答え</summary>

いいえ。**定数の外部ホスト**です。「モデルが決める宛先」の定義は「宛先の**ホスト**をモデルが決められる」で（L447）、ここでモデルが決めるのは
問い合わせの中身だけです（[H-5.13](#ah-5-13)）。

</details>

**問 5**: D2（破壊しない）のツールが、`mkstemp` で作った一時ファイルを `finally` で `os.remove` していて、解析器が `fs_remove` の矛を出しました。
判定と記号は何ですか。同じコードが D1 の組なら、どうなりますか。

<details><summary>答え</summary>

D2 では**誤、E2**（同じ呼び出しで自分が作ったものは呼び出しの前からあったものではない。`docs/drafts/final_judging_guide_draft.md:351-352`、L459）。
解析器は削除が破壊的かを sink の属性だけで決め、同じ呼び出しで作ったかを見ないので、この誤が出ます（`authgap/catalog/sinks.py:363`、
`authgap/dparse.py:365-368`、`:408-409`）。D1 の組なら、作成も削除も環境の変更なので**正**で、ラベルは**一時ファイル**です（L318、v4 の M58 `:679`）。

</details>

**問 6**: 解析器が `sort` の子プロセスへの `p.communicate(input=text)` に `pipe:communicate` × FS_WRITE × D1 の矛を出しました。
判定と記号は何ですか。子が `tee /var/log/out.txt` ならどうですか。

<details><summary>答え</summary>

`sort` なら、子は並べ替えて標準出力に返すだけでファイルを変えないので**誤、E5**（L462、15.1 の迷いやすい形 `docs/drafts/final_judging_guide_draft.md:333`）。
`tee <ファイル>` なら、子がファイルに書くので D1 に反し**正**になりえます。`pipe:` の矛がいつも E5 ではありません（[H-5.22](#ah-5-22)）。

</details>

**問 7**: `subprocess.run(f"git log --oneline {shlex.quote(ref)}", shell=True)` を読み取り専用のツールが実行し、解析器が `spawn_model` の矛を出しました。
「`shlex.quote` があるのでモデルはコマンドを選べない。`git log` は読むだけ。だから E7」と判定してよいですか。

<details><summary>答え</summary>

よくありません。`shlex.quote` は別のコマンドを足されるのは防ぎますが、`-` で始まる値を選択肢として読ませるのは防ぎません。`git log` は
`--output=<ファイル>` を受け付けてファイルに書く（本書が git 2.43.0 で確かめた）ので、取りうる値の全体で読めば（原理 3-a）環境を変ええます。
E7 にするには「モデルが選べない」と「固定の動作が反しない」の両方が要ります（[H-5.24](#ah-5-24)）。

</details>

**問 8**: 解析器が `http://ollama:11434` への `POST` に D3 の `net_external_host` の矛を出しました。判定は何ですか。`error_class` に何を書くかは、手引きで決まっていますか。

<details><summary>答え</summary>

ドットの無い名前は local なので D3 に反せず、判定は**誤**です（`docs/drafts/final_judging_guide_draft.md:383`、`:387-388`）。手引きは原因を
「語彙・定義の差（第 17 節）」と書きますが、第 17 節の E1〜E9 にその類が無く、どの記号を書くかは**決まっていません**（【穴 H-5-12】。
E9 にして説明を書く、新しい記号を足す、などの選択肢があり、決めるのは学生です）。

</details>

**問 9**: 1 つの組の `locations` に 2 つの位置があり、どちらも正でした。片方はモデルが決めた書き先への書き出し、もう片方はログへの追記です。
ラベルはどう決まりますか。

<details><summary>答え</summary>

手引きでは**決まっていません**。16.2 の 1 行目は「1 組に両方あれば、正にした位置で決める」としか書かず、正の位置が 2 つで種類が違うときの
選び方がありません。手順 G は 1 つ正が見つかれば止めてよいので、読む順でラベルが変わりえます（【穴 H-5-1】）。決めていないまま判定に入るなら、
16.2 の最後の規則で「その他・不明」にして `note` に事例を書く、という扱いになります（L437）。

</details>

---

[← 前](appendix-h-4.md) ｜ [付録 H の表紙](appendix-h.md) ｜ [目次](README.md) ｜ [次 →](appendix-h-6.md)
