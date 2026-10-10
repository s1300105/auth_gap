# 7. FAQ: 迷いやすい形と、手引きでの答え（59 項目）

この章は、判定の途中で「この形はどう読むか」に迷ったときに引くものです。`02_steps.md` の各段の「迷ったら」から Q の番号で
参照しています。

- 2026-10-09 に本記録者（AI）が、手引きの下書き・決定・決定シート・教科書・CLAUDE.md から集めたもの。作例はこの章のための架空の
  コード。正解の一覧ではなく、手引きの規則の当てはめの例です。**練習の件（W-01・T-01〜T-03）の参考の答えを書いたのと同じ作業の
  中で書いたので、練習の件から目隠しされていません**（練習の件に近すぎる例は点検で外した。限界は `evidence/practice_survey/README.md`）。
- 【手引きに無い】の印のある項目は、手引きにも決定にも規則が無く、O47・O48 で封の前に学生が決める点です（新しい穴 N1〜N9 は
  O48 (6)。末尾の表）。各項目に**練習の仮の扱い**か「仮の扱いは無い」を書きました。扱い方は `02_steps.md` の段 8 の 5 と同じです:
  仮の扱いがあればそれで決め、答えかラベルが決まったら `note` に「O48 (n) の仮の扱い: …」（N の項目は「O48 (6) N<k> の仮の扱い: …」）
  と書く。仮の扱いが無く、それで答えが変わるなら `不明`（`手引きで決まらない: …`。22 節）。
- 「手引き（:NNN）」は手引きの下書きの行番号（2026-10-09 の版）。

## 前提

- **対象**: 名簿の 1 件（D1 = `readOnlyHint: true`）。ツールの本体から深さ 4 まで、解析器の出力を見ずに読み、D1 に反する動作に届くかを決める。手順は見落としの判定（手引き 18 節）と同じ（D82、`docs/decisions.md:4276-4280`）。
- **結果の値**: `違反` / `違反（深さ 4 の外）` / `違反でない` / `不明` / `対象外`（D82、D85 の `docs/decisions.md:4400-4402`）。値どうしの優先と、書く欄の細部はまだ決まっていない（O48 (4)）。
- **違反に付けるラベル**: `condition_type`（条件の中身は `condition` 欄）と `write_target`（D82）。
  - `target_by_arg` は付けない（D84、`docs/decisions.md:4371`「実態調査の「違反」には付けない」）。
  - `cause` は書かない。これは O48 (4) の推奨で、まだ決まっていない。
- **手引き**は `docs/drafts/final_judging_guide_draft.md` を指す。行番号はこの版のもの。下書きで、まだ封をしていない。封の後は封をした版と照らし直す。
- **解析器の挙動の記述**（Q10・Q13・Q14・Q15）は、深さを「解析器の数え方で数える」（手引き 18.2 の 2）ための参考で、作例を凍結版の解析器で走らせた結果（2026-10-09）。判定の中で解析器を走らせるわけではない。
- **【手引きに無い】** の印は、手引きでも決定でもまだ決まっていない点に付けた。O48 の項目か「新しい穴 N1〜N9」（O48 (6)。末尾の一覧）を添えた。
- **答えが割れるときの扱い**（`README.md` の 3 節、`02_steps.md` の段 8 の 5 と同じ）: ① 仮の扱いがあれば、それで決めて `note` に書く。② 仮の扱いが無い点（各項目に「仮の扱いは無い」と書いたもの、手引きが「まれ」として 22 節に回した穴）で答えが変わるときは、22 節に従って `不明` にし、`unknown_reason` に「手引きで決まらない: …」と書く。③ 答えが変わらないときは、読み方を `note` に書いて先へ進む。

---

## A. 名簿の件とツールの本体

### Q01. ツールが登録用の関数の中で定義されている（入れ子の定義）

```python
def register(mcp):
    store = Store(DATA_DIR)                 # register が呼ばれたときに 1 回
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def search(q: str) -> str:
        return store.find(q)                # store は外側の変数（閉包）
register(mcp)                               # モジュールの一番上で呼ぶ
```

- **すること**:
  - 深さ 0 は内側の `search`。
  - `store` の型は外側の `Store(DATA_DIR)` で決め、`store.find` に降りる（深さ 1）。
  - `Store.__init__` の中の動作は `register(mcp)` が走る時点に済む。この例ではモジュールの読み込み時なので、ツールの呼び出しでは届かない。
  - `register(mcp)` を `main()` の中だけで呼ぶ形は Q28 を見る。
- **結果**:
  - `store.find` の中の書き込みは、ふつうどおり判定する。
  - `Store.__init__` の書き込みは届かないので数えない。ほかに違反が無ければ `違反でない`。
- **出典**:
  - CLAUDE.md:50「入れ子定義を落とさない。」
  - 手引き 14.4（:365「モジュールの読み込み時（モジュールの一番上の文、モジュール水準の変数の初期化）| 到達しない」）
  - 教科書 `docs/textbook/ch12.md:913-948`

### Q02. クラスのメソッドがツール（`self.<attr>` の受け手）

```python
class NoteTools:
    def __init__(self, mcp, root):
        self.cache = JsonCache(root)                         # 構築の時点
        mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.search)
    def search(self, q: str) -> str:
        return self.cache.lookup(q)
NoteTools(mcp, "/srv/notes")
```

- **すること**:
  - 本体は `search`。
  - `self.cache` に何が入るかを、`__init__` とクラスの中のほかの代入（`self.cache =` で grep）で全部確かめ、その型のメソッドに降りる（深さ 1）。
  - `__init__` の中の動作は構築の時点（この例では読み込み時）に済むので、ツールの呼び出しでは届かない。
  - 代入が複数あって型が割れるときは Q23 を見る。
- **結果**: Q01 と同じ。
- **出典**:
  - CLAUDE.md:52
  - 手引き 12.2（:109-110「呼び出し先が本当にその関数かは、受け手の型（その変数に何が入っているか）で確かめる」）
  - 手引き 手順 D の 3（:167）

### Q03. 宣言の書き方が違う（辞書・変数・SDK 2.x）／宣言がツールに付いていない

```python
RO = {"readOnlyHint": True}
@mcp.tool(annotations=RO)                                         # 辞書・変数
def a(): ...
@server.tool(annotations=ToolAnnotations(read_only_hint=True))    # SDK 2.x の書き方
def b(): ...
EXAMPLE = {"name": "demo", "annotations": {"readOnlyHint": True}} # 文書の例・設定だけ
```

- **すること**:
  - 名簿の規則では、3 つとも D1 の宣言（D85 の 2）。
  - 判定者は、その宣言が実際に登録されるツールに付いているかを確かめる。
- **結果**:
  - a・b はふつうに判定する。
  - `EXAMPLE` は登録されない例・設定の辞書なので `対象外`。理由を書く。分母には入れず、件数を報告する。対象外も 1 件と数える。
- **出典**: `docs/decisions.md:4392-4393`（D85 の 2・3）、`:4400-4402`

### Q04. 1 つの宣言を複数のツールが使う（名簿の `unmapped`）【手引きに無い: O48 (5)】

```python
def setup(mcp):
    ro = ToolAnnotations(readOnlyHint=True)
    @mcp.tool(annotations=ro)
    def list_a(): ...
    @mcp.tool(annotations=ro)
    def list_b(): ...
```

- **すること**:
  - D85 は「判定者が読んでツールを決める」とだけ書いている。
  - **仮の扱い**（O48 (5) の推奨）: 宣言を使うツールを定義の順に並べ、seed ⑦ の乱数で 1 つ選ぶ。練習の件にこの形は無い。
  - 選び方を `note` に書く。
- **結果**: 選んだ 1 つをふつうに判定する。
- **出典**: `docs/open_questions.md`、`docs/decisions.md:4393`

### Q05. 低水準のサーバ（`Tool(...)` とハンドラの分岐、自前の表）【一部 手引きに無い: O48 (4)】

```python
TOOLS = [Tool(name="stats", annotations=ToolAnnotations(readOnlyHint=True), inputSchema={})]
async def serve():
    server = Server("x")
    @server.call_tool()
    async def call_tool(name, args):
        audit(name, args)              # どの分岐にも入らない共通の処理
        if name == "stats":
            return _stats(args)
        elif name == "purge":
            shutil.rmtree(CACHE)       # 別のツールの分岐
```

- **すること**:
  - ハンドラは `serve()` の中の入れ子にあることがあるので、落とさない。
  - 動作は `name == "stats"` の分岐とその先を読む。ほかの名前の分岐（`purge`）は数えない。
  - `if name != "stats": raise` のような `!=` の分岐を見落とさない。
  - 次の 2 点は手引きに無い。O48 (4) が「低水準のサーバ（`tool_ctor`・`dict_registry`）の本体」として挙げている。自前の表 `{"stats": {"handler": _stats}}` も同じ扱い。
    - 共通の処理（`audit`）を読む範囲に入れるか。
    - 深さ 0 をハンドラにするか、分岐にするか。
  - **仮の扱い**（O48 (4)。`02_steps.md` の段 1 の表）: 深さ 0 は `name == "stats"` の分岐とし、分岐の前の共通の処理（`audit`）も深さ 0 として読む（そのツールの呼び出しで必ず走るので、14.1 の「届く」に当たる）。
- **結果**:
  - 分岐の中の書き込みはふつうどおり判定する。
  - `audit` の中にファイルへの書き込みがあれば `違反`（`note` に「O48 (4) の仮の扱い: 共通の処理を深さ 0 として読んだ」）。
- **出典**: CLAUDE.md:50、教科書 `docs/textbook/ch12.md:750-911`、`docs/open_questions.md`

### Q06. 1 つの木に複数のサーバ・`mount`・起動されないサーバ【一部 手引きに無い: O48 (4)】

```python
app = FastMCP("app", lifespan=app_life)
sub = FastMCP("sub", lifespan=sub_life)
@sub.tool(annotations=ToolAnnotations(readOnlyHint=True))
def stats() -> str: ...
if os.getenv("ENABLE_SUB"):
    app.mount(sub, prefix="sub")
```

- **すること**:
  - デコレータの変数（`sub`）が、どのサーバかを確かめる。
  - 起動時の初期化（Q26）を判断するときは、そのサーバの `lifespan=` と、取り付け先の親の lifespan を読む。
  - `grep 'lifespan='` は uvicorn の `lifespan="on"` や FastAPI の lifespan にも当たる。渡している相手を開いて確かめる。
  - 取り付けが環境変数しだいなら、14.3 の「ツールの登録そのものが設定しだい」と同じ形と読む（**仮の扱い**、O48 (4)）。
  - 起動する行が木の中に見つからないサーバのツールも、登録されていれば判定する（**仮の扱い**、O48 (4)。`02_steps.md` の段 2 の 4）。MCP 以外の枠組みにだけ登録しているときは**仮の扱いは無い**（答えが変わるなら 22 節）。
- **結果**: 条件つきの取り付けの先で違反に届くなら、`condition_type` = `運用者の設定`。
- **出典**:
  - 手引き 14.3（:335）、14.4（:371）
  - 教科書 `docs/textbook/ch09.md:606-633`、`docs/textbook/ch12.md:711-746`
  - `docs/open_questions.md`

### Q07. ツールの登録そのものが設定しだい

```python
if settings.ENABLE_EXPORT:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def export_report(path: str) -> str: ...
```

- **すること**: ツールとして登録されうるので、対象外にはしない。
- **結果**:
  - 違反なら `condition_type` = `運用者の設定`。ほかの条件と重なれば `;` で並べる。
  - (B) に数えない。
- **出典**: 手引き 14.3（:335「ツールの登録そのものが設定しだい（`if ENABLE_X:` の中の `@mcp.tool`）| `運用者の設定`」、:321-322）

### Q08. docstring・コメント・README・関数名を根拠にしない【明文は無い: O48 (4)】

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_summary(doc_id: str) -> str:
    """Read-only. Does not modify anything."""
    _remember(doc_id)            # 中で履歴ファイルに追記する
```

- **すること**:
  - 判定はコードの動作で決める。
  - `get_`・`list_`・`search_` の名前や、説明文の「read-only」「cache」で決めない。
  - 起動の方法もコードだけから決める。
  - AI に貼るときは docstring と `annotations=` を伏せる。
- **結果**: 動作どおりに決める。この例は `違反`。
- **出典**:
  - 手引き 11.2（:71-72「判定するのはコードの動作で、解析器の説明ではない。」）
  - 手引き 14.4（:359「起動の方法はコードだけから決める。」）
  - 手引き 20.1（:819「名前ではなく動作で決める。」）、21 の 6（:901）
  - `docs/open_questions.md`

---

## B. 読む範囲と深さ

### Q09. 深さの数え方の基本

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def tool(q):          # 深さ 0
    return a(q)       # a = 1 → b = 2 → c = 3 → d = 4（d の中身は読む）
def d(q):
    e(q)              # e = 5: 名前だけメモし、中は読まない
    os.remove(q)      # ライブラリの関数は深さを消費しない（深さ 4 の中の効果）
```

- **すること**:
  - 木の中の関数に降りるときだけ 1 段と数える。
  - 値の変換（`os.path.join` など）とライブラリの関数は深さを消費しない。
  - 深さ 4 の関数の中身は読む。深さ 5 より奥は探しに行かない。
  - 深さのメモ（`0 tool(server.py:10) → 1 a(:20) → …`）を、そのまま `evidence` の「読んだ範囲」にする。
- **結果**:
  - 違反が深さ 4 の外にだけあれば `違反（深さ 4 の外）`。主の数には入れず、別に数える。
  - 深さ 4 の中にもあれば中のものを主にし、外のものは `note` に書く。
- **出典**:
  - 手引き 18.2 の 2（:598-599「本体から、**木の中の**呼び出し先を**深さ 4 まで**たどる（本体 = 深さ 0、本体が呼ぶ関数 = 深さ 1、…）」）
  - 手引き 18.3（:643-647）
  - `docs/decisions.md:4278-4279`
  - 教科書 `docs/textbook/ch15.md:406-420`、`docs/textbook/ch52.md:466-489, 560-577`

### Q10. 構築 `Cls(...)` と dataclass【一部 手引きに無い: 新しい穴 N1】

```python
def tool(q):
    s = Store(ROOT)     # Store.__init__ に降りる（深さ 1）
    c = Cfg()           # @dataclass: 作られる __init__ が __post_init__・default_factory を呼ぶ
```

- **すること**:
  - 木の中のクラスの構築は、`__init__` に降りて 1 段（手引きの文）。
  - dataclass の `__post_init__` と `field(default_factory=f)` の `f` を読むか、何段と数えるかは手引きに無い（N1）。凍結版はどちらにも降りなかった（作例を凍結版で走らせた結果）。
  - **仮の扱い**（O48 (6) N1。`02_steps.md` の段 4 の表）: 構築のたびに走るので読み、`__init__` と同じ 1 段と数える。
- **結果**: 書き込みがあれば `違反`（深さは構築を書いた関数 + 1）。`note` に「O48 (6) N1 の仮の扱い: …」。
- **出典**: 手引き 18.2 の 2（:601「構築（`Cls(...)` から `__init__`）と `Thread(target=…)` の `target` は 1 段」）、教科書 `docs/textbook/ch15.md:845`

### Q11. デコレータの wrapper と、重ねる順【一部 手引きに無い: O48 (4)】

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
@audited                        # 登録されるのは wrapper。呼ぶたびに wrapper が先に走る
def search(q): ...

@audited
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))   # 登録されるのは本体。wrapper は走らない
def other(q): ...
```

- **すること**:
  - `@mcp.tool` 以外の、木の中で定義されたデコレータは、定義を開いて wrapper を読む。
  - `functools.wraps` は名前を写すだけで、呼ばれるのは wrapper。
  - デコレータは下から順に掛かる。`@mcp.tool` が上にあるか下にあるかで、wrapper が道筋に乗るかが変わる。
  - `mcp.tool(...)(fn)` の形なら、`fn` の定義に付いたデコレータを見る。
  - 深さは wrapper の分を足さない。**仮の扱い**（O48 (4)）: wrapper の中の文はツールの本体と同じ深さ 0。wrapper が本体を呼ぶこと（`asyncio.to_thread(fn)` などを通しても）は段に数えず、本体は深さ 0 のまま。wrapper が本体のほかに呼ぶ木の中の関数が深さ 1。
- **結果**: wrapper の中の書き込みも違反に数える。
- **出典**:
  - 手引き 18.2 の 2（:601-603「「たどらない」は**深さを数えない**という意味で、wrapper（デコレータなど）の中の動作もツールの呼び出しで実行されるので、読む範囲に入れる（深さは wrapper の分を足さない。D86）」）
  - `docs/decisions.md:4441`
  - 教科書 `docs/textbook/ch09.md:2067-2090, 2161-2180`
  - `docs/open_questions.md`

### Q12. サーバ全体の middleware【手引きに無い: O48 (1)】

```python
class Audit(Middleware):
    async def on_call_tool(self, context, call_next):
        append_line(AUDIT_LOG, context.message.name)
        return await call_next(context)
mcp = FastMCP("x", middleware=[Audit()])
```

- **すること**:
  - 各ツールの呼び出しで走るが、読む範囲に入れるかは手引きに無い。
  - **仮の扱い**（O48 (1) の推奨 (a)。`02_steps.md` の段 3 の 5）: 木の中の middleware と呼び戻しの関数は、wrapper と同じく深さを足さずに読む。
- **結果**: `違反`、`condition_type` = `なし`、`write_target` = ログ（`note` に「O48 (1) の仮の扱い: middleware を読んだ」）。
- **`mount()` のとき**: サーバ `sub` を親のサーバ `app` に `app.mount(sub)` で取り付けているなら、`app` の middleware も読む（仮の扱い、
  O48 (1)。`02_steps.md` の段 3 の 5）。親の middleware は親の入口を通した呼び出しでだけ走るので、そこにだけある違反の
  `condition_type` は `運用者の設定`（どの入口で公開するかは運用者が決める。**仮の扱い**、O48 (4)）とし、`note` に書く。
- **深さ**: middleware の中の文は深さ 0。そこから呼ぶ木の中の関数は深さ 1（`04_rules.md` の 1 節）。
- **出典**: `docs/open_questions.md`

### Q13. 別のスレッド・タスクで動かす形【一部 手引きに無い: O48 (2)・新しい穴 N2】

```python
await asyncio.to_thread(_save, q)            # 1 段（解析器の INDIRECT の表）
loop.run_in_executor(None, _save, q)         # 1 段
pool.submit(_save, q)                        # 1 段
Thread(target=_save, args=(q,)).start()      # 1 段
asyncio.create_task(_save_async(q))          # 書かれた呼び出し _save_async(q) で 1 段
list(pool.map(_save, qs))                    # 表に無い
loop.call_soon(_save, q)                     # 表に無い
```

- **すること**:
  - **到達**: 呼び出しが返った後に走っても到達する。
  - **深さが決まっている形**: `to_thread`・`run_in_executor`・`Executor.submit`・`Thread`/`Process(target=)`・`functools.partial` は、解析器の表（`authgap/catalog/transfers.py:129-139`）で 1 段と決まっている。O48 (2) で残っているのは、これを手引きに列挙するかどうかだけ。
  - **書かれた呼び出し**: `create_task(f(x))`・`gather(f(x))` は `f(x)` という書かれた呼び出しなので 1 段。凍結版でも 1 段だった（作例を凍結版で走らせた結果）。
  - **深さが決まっていない形**: `Executor.map`・`call_soon`・`add_done_callback` は表に無く、凍結版は降りなかった（N2）。**仮の扱い**（O48 (6) N2）: 表の形と同じく、渡した関数を 1 段と数える。
- **結果**: 書き込みがあれば `違反`。表に無い形で深さを決めたら `note` に「O48 (6) N2 の仮の扱い: …」。
- **出典**:
  - 手引き 14.1（:289-290「ツールが積んだもの・始めたもの（queue に積んだ仕事、起動したスレッド・プロセス）を、**呼び出しが返った後に**別のスレッド・プロセスが書くときも、**到達する**」）
  - 手引き 18.2 の 2（:601）
  - `docs/open_questions.md`
  - 教科書 `docs/textbook/ch15.md:406-420`

### Q14. 暗黙に走るコード（`@property`・`cached_property`・`__enter__`/`__exit__`・`__call__`・pydantic の検証子）【手引きに無い: 新しい穴 N1】

```python
class Repo:
    @cached_property
    def workdir(self):
        os.makedirs(WORK, exist_ok=True); return WORK   # r.workdir と書くだけで走る（初回）
    def __enter__(self):
        self.lock = open(LOCK, "w"); return self        # with Repo() as r: で走る
    def __exit__(self, *a):
        os.remove(LOCK)
```

- **すること**:
  - どれもツールの呼び出しで実行されるので、wrapper（D86 の 16）と同じ理由で読む。
  - 属性の読み（`r.workdir`）や `obj(...)` が、クラスの定義で `@property`・`__call__` になっていないかを確かめる。
  - `with X:` があれば、`X` のクラスの `__enter__`・`__exit__` を読む。
  - 読むかと深さは手引きに無い（N1。凍結版はどれもたどらない）。**仮の扱い**（O48 (6) N1）: 読む。書かれた位置（属性の読み・`with`・`obj(...)` を書いた関数）から 1 段と数え、`note` に書く。
- **結果**:
  - `cached_property` の作成: `違反`、`condition_type` = `初回`、`write_target` = キャッシュ・状態の保存（初回に作る作業ディレクトリ）。
  - `__enter__` で作って `__exit__` で消すロック: `違反`、`condition_type` = `なし`、`write_target` = 一時ファイル（同じ呼び出しの中で作って消す）。
- **出典**:
  - 教科書 `docs/textbook/ch15.md:845-856`（「`with Lock():` の `Lock.__enter__` | **たどらない**」ほか）、`:928-940`
  - `docs/open_questions.md`（U16「暗黙に呼ばれる木内コード」）
  - 手引き 16.1（:521）、16.2（:538）

### Q15. 既定値の関数・依存の注入【一部 手引きに無い: O48 (4)・O48 (6) N9】

```python
def _lookup(q, writer=_write_history):       # 呼ぶ側で writer を渡していなければ既定値
    writer(q)
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(q: str, ctx: Context, db=Depends(get_db)) -> str: ...   # 枠組みが入れる引数
```

- **すること**:
  - 既定値の関数に降りるかと、その深さは手引きに無い（N9）。**仮の扱い**（O48 (6) N9。`02_steps.md` の段 4 の表）: 呼ぶ側で別の値を渡していなければ既定値の関数に降り、`writer(q)` を書いた関数から 1 段と数える。
  - 枠組みが呼んで値を入れる関数（`Depends(get_db)` など）は、木の外のライブラリが木の中の関数を呼び戻す形。呼ぶ時期が公式の文書で分かれば決まる。分からなければ不明（類「動的な呼び出し」）。
  - `ctx` など枠組みが入れる引数は、モデルの値として扱わない（**仮の扱い**、O48 (4)）。
- **結果**: `_write_history` が書けば `違反`（`note` に「O48 (6) N9 の仮の扱い: …」）。
- **出典**:
  - 手引き 19（:730-731, :741）
  - `docs/decisions.md:4432`（D86 の 7）
  - `docs/open_questions.md`
  - 教科書 `docs/textbook/appendix-i-4.md:273`、`docs/textbook/appendix-i.md:116`

### Q16. コールバック（かっこの無い関数名）【一部 手引きに無い: O48 (1)】

```python
client = ExtClient(token_saver=_save_token)   # 呼んでいない。値として渡している
```

- **すること**:
  - `_save_token(` で grep すると定義しか出ない。かっこを付けずに `grep -rnw '_save_token'` でも探す。
  - 呼び戻されるか、いつ呼ばれるかは、外のライブラリの公式の文書で決める。
  - 文書で決まらなければ不明（類「動的な呼び出し」。D86 の 7）。
  - 深さは手引きに無い。**仮の扱い**（O48 (1)。`04_rules.md` の 1 節）: 呼び戻される関数は、関数を渡した行のある関数と同じ深さとして読む（深さを足さない）。
- **結果**: 文書で「トークンの更新のたびに呼ぶ」と分かれば `違反`、`condition_type` = `失敗・期限切れ`、`write_target` = キャッシュ・状態の保存（16.2 の OAuth のトークンの行）。
- **出典**:
  - 手引き 18.2 の 5（:615）、19（:730-731）、16.2（:536）
  - `docs/decisions.md:4432`
  - 教科書 `docs/textbook/ch09.md:2364-2375, 2537-2548`

### Q17. 動的な呼び出し（`getattr`・表・`importlib`・プラグイン）

```python
OPS = {"stats": _stats, "reindex": _reindex}       # 表が同じ木にある
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def run(op: str) -> str:
    return OPS[op]()                               # op はモデルが決める
```

- **すること**:
  - 候補が読めるなら、候補を全部読む。モデルが `op` を選べるなら、取りうる値の全体で考える（原理 3-a）。
  - 「あと 1 ファイル読めば決まらないか」を確かめてから不明にする。
  - entry_points のプラグインのように、木の外で候補が増える形は不明（類「動的な呼び出し」）。
- **結果**: 候補のどれかが書けば `違反`、`condition_type` = `引数`。
- **出典**:
  - 手引き 11.3（:91「モデルが選べる引数は「取りうる値の全体」で考える」）、19（:730-731）
  - 教科書 `docs/textbook/appendix-i.md:118`、`docs/textbook/appendix-i-4.md:448`

### Q18. 木の外のライブラリ（関数そのものが環境を変えるか、ライブラリの中の書き込み）【一部 手引きに無い: O48 (3)】

```python
df.to_csv(out_path)                          # 名前で書き出しと分かる
np.save(path, arr)
model = AutoModel.from_pretrained(name)      # 文書: 重みを ~/.cache に保存（ライブラリの中の書き込み）
```

- **すること**:
  - ライブラリの中は読まないが、関数そのものが環境を変えるなら、呼んでいれば数える。手引きの例は `requests.put`・`sqlite3` の `execute("DELETE …")`・`shutil.rmtree`。
  - 公式の文書を読むのは「中を読む」ことではない。
  - 知られていない関数の決め方は手引きに無い。**仮の扱い**（O48 (3) の推奨。`02_steps.md` の段 4 の 5）:
    - 名前がはっきり示すなら名前で決め、`evidence` に「関数名から」と書く。
    - そうでなければ公式の文書で決める。
    - 決まらず、答えが変わるなら `不明`（類は、相手のサーバの API なら `相手の API`、それ以外は `外の値`）。
  - 文書で**ライブラリの中の書き込み**に気づいたときの扱いも手引きに無い。**仮の扱い**（O48 (3)）: 読む範囲の外なので答えは変えず、`note` に書く。
  - 実態調査では（見落としの判定と同じく）ライブラリのソースは開かない（19 節）。開いてよいかは O48 (3) の (c) で、まだ決まっていない。
- **結果**:
  - `to_csv` は `違反`。`write_target` は書き先で決める（モデルが決めた場所なら利用者のファイル）。
  - `from_pretrained` のキャッシュは、推奨どおりなら答えに入れず `note` に書く。
- **出典**:
  - 手引き 18.2 の 2（:598-600）、19（:720-723）
  - `docs/open_questions.md`
  - 教科書 `docs/textbook/ch52.md:502-531`

### Q19. 木の中か外か（同梱のコード・`vendor/`・テスト・例のファイル）【手引きに無い: O48 (4)】

- **すること**:
  - 迷ったら定義を grep する（`grep -rn 'def helper'`）。木の中のファイルに定義があれば木の中。
  - 同梱された別のプロジェクトのコード（`vendor/`・`third_party/`）も、ファイルが木の中にあるので木の中として読む（教科書の読み）。
  - テスト・例のファイルの扱いは手引きに無い。**仮の扱い**（O48 (4)。`02_steps.md` の段 4 の 3）: ツールの道筋から呼ばれていれば、木の中として読む。テストからだけ呼ばれる関数はツールの道筋に無いので読まない（14.2 の死んだコード）。
- **出典**: 教科書 `docs/textbook/ch52.md:491-500`、`docs/open_questions.md`

### Q20. 同じ関数に、深さの違う 2 つの道で着く【手引きに無い: O48 (4)】

```python
def tool(q):
    _save(q)       # 深さ 1 で _save に着く
    a(q)           # a → b → c → d → _save（深さ 5）
```

- **すること**: **仮の扱い**（O48 (4)）はいちばん浅い深さ。教科書も「浅いほうの深さで数えるのが自然です（手引きは明示していません。本書の読み）」と書いている。
- **結果**: この例は深さ 1 として `違反`。
- **出典**: `docs/open_questions.md`、教科書 `docs/textbook/ch52.md:480-482`

### Q21. 受け手の型を確かめるために、深さ 4 より奥を覗く【教科書の読み】

- **すること**:
  - `conn.execute(...)` の `conn` を作る関数が深さ 5 にあっても、型を確かめるために覗くのは構わない。
  - ただし、そこで見つけた**効果**は深さ 4 の外として扱う。
  - 深さ 4 より奥を探しに行く必要はない。
  - 手引きは「深さ 4 より奥を探しに行く必要はない」とだけ書く（18.3）。覗いてよいことと、そこで見つけた効果の扱いは教科書の読み。
- **出典**: 教科書 `docs/textbook/ch52.md:569-571`、手引き 18.3（:643-645）

### Q22. 同じ名前の関数・メソッドの取り違え

```python
from .fs import save            # 同じ名前の save が store/ と fs/ にある
seen: set[str] = set()
seen.add(q)                     # 組み込みの set.add。木の中の Cache.add ではない
```

- **すること**:
  - import の行で、どの定義かを決める。見るもの: `as` の別名、相対 import、`__init__.py` での再輸出、`from x import *`。
  - メソッドは受け手の型で決める。組み込みの `set()`・`dict.get()`・`list.append()` を、木の中の同名のメソッドと取り違えない。
  - エディタの「定義へ移動」も AI の答えも、名前で当てていることがある。
- **結果**: 組み込みのメソッドなら、その行は書き込みではない。
- **出典**:
  - 手引き 12.2（:109-110）、手順 C（:151-153）、17 の E3（:573）
  - CLAUDE.md:67-69
  - 教科書 `docs/textbook/ch09.md:2364-2375, 2517-2527`

### Q23. 受け手のクラスが 1 つに決まらない（設定で選ぶ実装・抽象クラス）

```python
backend = make_backend(os.getenv("HISTORY", "memory"))   # "memory" か "file"
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(q):
    backend.record(q)        # MemoryBackend は書かない。FileBackend は追記する
```

- **すること**:
  - `make_backend` を開き、候補の実装を全部読む。
  - 既定（`memory`）は書かないが、運用者が `file` を選ぶと書く → その設定で起動すれば届く。
  - 選ばれ方がプラグインや外の値で決まらなければ不明（類「動的な呼び出し」か「外の値」）。
  - 外の SDK のクラスなら Q18・Q47 を見る。
- **結果**: `違反`、`condition_type` = `運用者の設定`（(B) に数えない）。
- **出典**: 手引き 14.1（:287「そのツールが呼ばれたとき、その効果が起きる実行の道が 1 つでもあるか」）、14.3（:316）、19（:727, :730-731）

### Q24. 関数の中の import（遅延 import）【手引きに無い:「まれ」H-3-20 → 22 節】

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(q):
    from . import heavy_index        # 最初の呼び出しで読み込まれる
    return heavy_index.lookup(q)
# heavy_index.py の一番上: os.makedirs(INDEX_DIR, exist_ok=True)
```

- **すること**:
  - `heavy_index.lookup` はふつうに 1 段。
  - 読み込まれるモジュールの一番上の文が、最初の呼び出しで走る形は、14.4 の表が名指ししていない。「まれ」として決めずに封をした穴 H-3-20 に当たる。
  - まず、同じモジュールがサーバの起動時にほかの所で import されていないかを grep する。されていれば、読み込み時の初期化なので到達しない。
- **結果**: 22 節なら次のとおり。
  - `outcome` = `不明`
  - `unknown_reason` = `手引きで決まらない: ツールの中の遅延 import で走るモジュールの一番上の書き込み`
  - `note` に「読めば `初回` で到達」と書く。
- **出典**:
  - 教科書 `docs/textbook/ch49.md:1642-1664`
  - `docs/drafts/guide_holes_triage.md:72`
  - 手引き 22（:919-921, :928）

### Q25. `try: import … except ImportError`・`if TYPE_CHECKING:`

```python
try:
    from loguru import logger
    logger.add(LOG_PATH)               # loguru が入っているときだけファイルに出す
except ImportError:
    import logging; logger = logging.getLogger(__name__)   # 標準エラー
if TYPE_CHECKING:
    from .store import Store           # 実行時には走らない（型のためだけ）
```

- **すること**:
  - 両方の枝を読む。どちらが走るかは、任意の依存が入っているかで決まる。
  - `TYPE_CHECKING` の中の import は、実行時の動作に関係しない。
- **結果**: ツールが毎回 `logger.info` を呼ぶなら `違反`、`condition_type` = `運用者の設定`、`write_target` = ログ。
- **出典**: CLAUDE.md:51、手引き 14.3（:336「運用者が置く目印のファイル・OS・任意の依存・… で決まる | `運用者の設定`（`外部の状態` にしない）」）

---

## C. 到達するか

### Q26. 一度だけの初期化（`main()`・lifespan・読み込み時・包む部品のフック）

```python
_db = None
def get_db():
    global _db
    if _db is None:
        _db = init_db()       # DB のファイルと表を作る
    return _db
```

- **すること**: 初期化が、ツールの受付より前に必ず済んでいるかで決める。

  | 初期化を先に済ませる場所 | 到達 | 結果 |
  |---|---|---|
  | `main()` / `if __name__ == "__main__":` の中だけ | する | `condition_type` = `起動の方法` |
  | lifespan の中（必ず走る） | しない | その動作は数えない |
  | モジュールの一番上 | しない | その動作は数えない |
  | `mcp` を包む部品の起動フック | する | `condition_type` = `起動の方法`（D86） |
  | どこでも先に済ませない | する | `condition_type` = `初回` |
  | 読み切れない | — | 不明（類「起動・初期化」） |

- **戻す行も確かめる**:
  - 初期化が済んだ後に `_db = None` に戻す行を grep する。
  - 戻す行は、ツールの受付の途中で走りうる場所だけを数える。`atexit` とテストの中は数えない。
- **出典**:
  - 手引き 14.4（:361-367, :374-376）、手順 D の 4（:170-171）、14.3（:313）
  - 教科書 `docs/textbook/ch49.md:1372-1391`（「どこでも先に済ませない」の行は本書が補った読み）

### Q27. lifespan が条件つき・失敗を握りつぶす【一部 手引きに無い: 新しい穴 N7】

```python
@asynccontextmanager
async def life(server):
    if os.environ.get("PREBUILD"):     # 設定しなければ、起動時に済まない
        _ensure_index()
    yield {}

@asynccontextmanager
async def life2(server):
    try:
        _ensure_index()
    except Exception:
        pass                           # 失敗しても受付を始める
    yield {}
```

- **すること**:
  - lifespan が初期化を「必ず」済ませるかを読む。
  - 条件つきなら、条件が偽のとき最初の呼び出しで届くので、到達する。これは「既定では起きるが、設定で止められる」形なので、`運用者の設定` は書かずに `初回` と書く。
  - 失敗を握りつぶす形も、失敗したときは呼び出しで届くので到達する。ただし `condition_type` の例が手引きに無い（N7）。**仮の扱い**（O48 (6) N7）: `失敗・期限切れ` と書き、`note` に書く。
  - `yield` の後は終了時の処理なので、ツールの受付の後に走る。
- **結果**: `life` は `違反`、`condition_type` = `初回`（(B) に数える）。
- **出典**:
  - 手引き 14.4（:372-373「lifespan が初期化を**必ず**済ませるか（例外で抜けたら受付が始まらないか、条件つきではないか）も見る。条件つきなら、条件が偽のときはツールの呼び出しで届くので「到達する」」）
  - 手引き 14.3（:334）
  - 教科書 `docs/textbook/ch49.md:1113-1130`、`docs/textbook/ch09.md:555-590`

### Q28. 14.4 の表に無い起動の形【手引きに無い: H-3-17・H-3-19（まれ）と教科書の境目 6 → 22 節】

```python
def main():
    mcp = FastMCP("x")          # サーバを関数の中で作る（H-3-17）
    register_tools(mcp)         # 登録が main() の中だけ（教科書の境目 6）
    _init()
    mcp.run()
# ほかに: 一番上の初期化が mcp.run() の後ろにある・条件つき・失敗を握りつぶす（H-3-19）
```

- **すること**:
  - 14.4 の `main()` の行は、「`main()` を通らない起動でも、ツールが登録されている」ことを前提にしている。
  - 登録が `main()` の中だけなら、どの起動でも「ツールの呼び出しが `_init()` に届く道」が無いと読める。ただし手引きは名指ししていない。
  - 答えがこの形で決まるときだけ、22 節に従う。
- **結果**: 不明にし、`unknown_reason` に「手引きで決まらない: …」と書く（本番では事前登録の §5 に記録する。練習では repo を書き換えず、ワークシートの J 節に書いて送る）。読んだ答え（「到達しないと読める」など）は `note` に書く。
- **出典**:
  - 教科書 `docs/textbook/ch49.md:1665-1690`
  - `docs/drafts/guide_holes_triage.md:69-71`
  - 手引き 22（:919-924, :928）

### Q29. 毎回実行されるが、環境が変わるのは一部

```python
os.makedirs(CACHE_DIR, exist_ok=True)                       # 無いときだけ作る
conn.execute("CREATE TABLE IF NOT EXISTS hist (q TEXT)")    # 無いときだけ作る
Path(STALE).unlink(missing_ok=True)                         # あるときだけ消す
```

- **すること**:
  - 環境が変わる場合の条件を書く。
  - `初回` とも `外部の状態` とも読めるときは、表の上にある `初回` を 1 つだけ書く。
- **結果**: `違反`。作る側は `condition_type` = `初回`、前の残りを消す側は `外部の状態`。(C) に数えない。
- **出典**:
  - 手引き 14.3（:329「行は毎回実行されるが、環境が変わるのは一部（`makedirs(d, exist_ok=True)`・`CREATE TABLE IF NOT EXISTS`・`unlink(missing_ok=True)`）| 環境が変わる場合の条件（`初回` / `外部の状態`）。(C) に数えない」、:340-343）
  - 教科書 `docs/textbook/appendix-i.md:100-101`

### Q30. 引数で分かれる・既定値・モデルが値を選べる

```python
def export(q: str, save: bool = True):    # 既定値で書く
    if save: _write(q)
def peek(path: str, mode: str = "r"):     # モデルが "w" を渡せる
    return open(path, mode).read()
def trace(q: str, debug: bool = False):
    if debug or os.environ.get("TRACE"):  # 「または」
        _append(q)
```

- **すること**:
  - 既定値で起きるなら `なし`。
  - モデルが選べる値は、取りうる値の全体で考える。`mode` に `"w"` を渡せば書けるので、反する。
  - 毎回届くが、反するのが一部の値のときだけなら、反する場合の条件を書く（モデルの値 → `引数`）。
  - 「または」でつながる条件は、一番弱い道の条件だけを書く。
- **結果**:
  - `export`: `違反`、`condition_type` = `なし`。
  - `peek`: `違反`、`condition_type` = `引数`（(C) に数えない）。
  - `trace`: `違反`、`condition_type` = `引数`（(B) に数える）。
- **出典**: 手引き 11.3（:91）、手順 F（:180）、14.3（:312, :330, :333, :337）

### Q31. 環境変数・目印のファイル・OS・`config.py` の定数【一部 手引きに無い: 新しい穴 N5】

```python
if os.getenv("HISTORY_FILE"): _append(q)          # 設定で有効になる
if not os.getenv("NO_CACHE"): _save_cache(q)      # 既定で起きる
if os.path.exists("/etc/app/enable_audit"): ...   # 運用者が置く目印
if sys.platform == "win32": ...                   # OS
# config.py
SAVE_HISTORY = False                              # 運用者が書き換える前提か、ただの定数か
```

- **すること**:
  - 14.3 の表の行に当てる（下の結果）。
  - `DEBUG = False` がどこでも書き換えない定数なら、閉じた枝で到達しない。
  - 運用者が書き換える前提の `config.py` の定数なら `運用者の設定`。
  - 「書き換える前提」かをどう見分けるか（ファイル名・コメント・README）は手引きに無い（N5）。**仮の扱いは無い**: それで答えが変わるなら 22 節（`不明`、`手引きで決まらない: …`）。
  - 実行時にできたファイルや相手の応答は `外部の状態` で、運用者が決める条件とは分ける。
  - **ツールが動くのに要る設定と、機能を有効にする設定を分ける**【手引きに無い O48 (4)】: 設定が無いとツールがエラーで抜ける（API の
    キー・接続先が無ければ例外）なら、14.3 の「前提の崩れで、効果の前に抜ける」として条件に数えない。設定が無くてもツールは動き、
    その効果だけが起きない（`if os.getenv("HISTORY_FILE"):`）なら `運用者の設定`。どちらか読み分けられなければ、練習の仮の扱いと
    して `運用者の設定` を書き（(B) に数えない側。14.3 の表の順の規則ではない）、`note` に書く。
- **結果**:
  - `HISTORY_FILE`: `運用者の設定`
  - `NO_CACHE`: `運用者の設定` を書かない（ほかに条件が無ければ `なし`）
  - 目印のファイル・OS: `運用者の設定`
  - `config.py`: 見分けられれば上の行どおり。見分けられず、それで答えが変わるなら `不明`
- **出典**: 手引き 14.2（:299）、14.3（:315-316, :334, :336）

### Q32. 失敗・再試行の道の書き込みと、失敗で先に抜けるだけの形

```python
try:
    return _fetch(q)
except Exception as e:
    _dump_crash(e)        # 失敗したときだけ書く
if not q:
    return "empty"        # 空の入力で抜けるだけ
_append_log(q)
```

- **結果**:
  - `_dump_crash`: `違反`、`condition_type` = `失敗・期限切れ`。
  - `_append_log`: `違反`、`condition_type` = `なし`。空の入力で先に抜けることは、条件に数えない。
- **出典**:
  - 手引き 14.3（:314「トークンの更新、再試行、エラー時の後始末」、:332「空の入力・失敗・前提の崩れ…で、効果の前に抜ける | 条件に数えない」）
  - 教科書 `docs/textbook/ch49.md:1094-1112`

### Q33. 相手のサーバの応答しだいで起きる書き込み

```python
r = httpx.get(f"{API}/items/{item_id}")    # item_id はモデルの引数
if r.status_code == 410:
    _purge_local(item_id)
```

- **結果**: `違反`。`condition_type` は、応答だけで決まるなら `外部の状態`。モデルの引数で 410 を起こせると読めるなら、「1 つだけ」の規則で `引数`。
- **出典**: 手引き 14.3（:331）、`docs/decisions.md:4429`（D86 の 4）

### Q34. 呼び出しが返った後に走る書き込み（queue・常駐の worker・`atexit`）【一部 手引きに無い: 新しい穴 N2】

```python
JOBS.put(q)                                 # ツールは積むだけ
def _worker():                              # 起動時に Thread で始めた常駐の worker
    while True:
        _index(JOBS.get())                  # ファイルに書く
atexit.register(_flush_history)             # ツールが溜めた履歴を終了時に書く
```

- **すること**:
  - ツールが積んだもの・始めたものを、後で別のスレッドが書くなら到達する（14.1、決定シートの問 4 (b) の A）。
  - 常駐の worker はツールから呼ばれないので、深さの数え方が無い（N2）。**仮の扱い**（O48 (6) N2）: worker の関数（`_worker`）を、積む行（`JOBS.put(q)`）のある関数から 1 段と数える（`Thread(target=)` と同じ）。その先はふつうに数える。
  - 仕分けでは `atexit` も問 4 (b) に含めて決めたが、手引きの文は queue・スレッド・プロセスだけを挙げている（14.4 は `atexit` を「`None` に戻す場所」に数えないとだけ書く）。`atexit` には**仮の扱いは無い**: それで答えが変わるなら 22 節。
- **結果**: queue と worker の形は `違反`。`condition_type` は worker の書き方で決める。
- **出典**:
  - 手引き 14.1（:289-290）、14.4（:374-376）
  - `docs/drafts/guide_decision_sheet.md:35, 166`
  - `docs/drafts/guide_holes_triage.md:53`

### Q35. 値の出どころ（定数に見えて書き換わる値・別のツールが入れた値）【一部 手引きに無い: 新しい穴 N6】

```python
CMD = ["git", "status"]
def set_cmd(c): global CMD; CMD = c.split()       # 別のツールが書き換える
os.environ["OUT_DIR"] = out; ...; os.environ["OUT_DIR"]   # 書いて読み戻す
url = BASE.format(host=host)                      # テンプレートの穴に引数が入る
```

- **すること**:
  - 原理 3-a（モデルが選べる値）を当てる前に、値の出どころを全部たどる。見るもの: `global` での再束縛、同じ関数での `os.environ` の書き込みと読み戻し、書式テンプレートの穴。
  - 別のツールの引数がメモリに残り、判定しているツールのコマンドや書き先を決める形（ツールをまたぐ値の流れ）を「モデルの値」とするかは、手引きに無い。
- **結果**:
  - 同じツールの中で引数から届くなら、モデルの値（SPAWN なら反する）。
  - ツールをまたぐ形は手引きに無い（N6）。**仮の扱いは無い**: `note` に書き、それで答えが変わるなら 22 節（`不明`）。
- **出典**: CLAUDE.md:76-79、手引き 11.3（:91）、15.1（:407）

---

## D. D1 に反するか

### Q36. ログ（出力先・設定の場所・`main()` だけ・水準）【一部 手引きに無い: 新しい穴 N3】

```python
logging.basicConfig(level=logging.INFO)               # 標準エラー → 反しない
logging.basicConfig(filename="app.log", level=logging.INFO)  # ファイル → INFO 以上が反する（水準の指定が無ければ WARNING 以上だけ）
logger.addHandler(RotatingFileHandler(LOG))
logging.config.dictConfig(CFG)                        # handler の class / filename を読む
logging.config.fileConfig("logging.ini")              # ini が木に無ければ読み切れない
from loguru import logger; logger.add("~/.app/x.log")
```

- **すること**:
  - ツールの道筋に `logger.xxx(...)` があれば、ロガーの出どころを import でさかのぼる。
  - 出力先の設定を**木全体**で grep し、このサーバの起動で走るものを選ぶ（`02_steps.md` の段 5 の 3）。モジュールの一番上・設定のファイル・`main()` の中にあることが多い。
  - 名前の付いたロガーの記録は、ルートのロガーにも伝わる。`basicConfig` は最初の 1 回だけ効く。
  - 設定が `main()` の中だけなら `運用者の設定` を 1 つだけ書く。
  - ログの水準で書かれない記録の扱いは手引きに無い（N3）。**仮の扱いは無い**（教科書は 22 節に従うとしている）: それで答えが変わるなら `不明`。例: 水準が `WARNING` 固定で `logger.info` だけ、水準を環境変数で変えられる。
- **結果**: ファイルに書くなら `違反`、`write_target` = ログ（「いつ・何をした」を書く行）。
- **出典**:
  - 手引き 15.1（:419）、18.3（:648-649）、14.3（:340-343）、16.2（:540）
  - 教科書 `docs/textbook/ch09.md:1379-1420, 1528-1541`、`docs/textbook/ch50.md:2407`

### Q37. 標準出力・標準エラー・`print`・クライアントへの通知

```python
print("done")
print(res, file=sys.stderr)
await ctx.info("searching"); await ctx.report_progress(1, 3)
print(res, file=fh)                  # fh が開いたファイルなら書き込み
```

- **結果**:
  - 標準出力・標準エラー・`ctx` の通知は反しない。
  - `print(..., file=開いたファイル)` はファイルへの書き込み。
- **出典**: 手引き 15.1（:419, :423）、教科書 `docs/textbook/ch09.md:1528-1541`

### Q38. 一時ファイル（同じ呼び出しで作って消す）

```python
fd, tmp = tempfile.mkstemp(suffix=".json")
try:
    ...
finally:
    os.remove(tmp)
```

- **すること**:
  - D1 では、作って消すだけでも反する。D2 なら反しない形なので、混同しない。
  - `TemporaryDirectory`・`NamedTemporaryFile` も同じ。`io.StringIO` はメモリなので書き込みではない。
- **結果**: `違反`、`condition_type` = `なし`、`write_target` = 一時ファイル。
- **出典**: 手引き 14.5（:382-385）、15.1（:405）、16.1（:521）、15.2（:449-450）

### Q39. ディレクトリの作成・`touch`・`'a'` で開くだけ（`flock`）【一部 手引きに無い: 新しい穴 N8（ラベル）】

```python
Path(DATA).mkdir(parents=True, exist_ok=True)
Path(MARK).touch()
with open(LOCK, "a") as fh:
    fcntl.flock(fh, fcntl.LOCK_EX)     # 何も書かない
```

- **すること**:
  - D1 では、ディレクトリの作成も環境の変更。
  - `'a'` で開くだけなら、ファイルが無いときだけ作る。
  - `touch()` は、無ければ作り、あれば更新の時刻（mtime）を書き換える。呼ぶたびにファイルが変わる。
  - 15.4 の「`flock` のために `'a'` で開くだけ → 反しない」は D4 の表の規則で、D1 には当てない。
- **結果**:
  - `mkdir(exist_ok=True)` と、`'a'` で開くだけ: `違反`、`condition_type` = `初回`（14.3 の「環境が変わるのは一部」）。
  - `touch()`: `違反`、`condition_type` = `なし`（呼ぶたびに更新の時刻が変わる）。
  - `write_target`: 作業ディレクトリはキャッシュ・状態の保存。消さずに残るロックファイル・目印のファイルは種類の表に行が無い（N8）。**仮の扱い**（O48 (6) N8）: その他・不明（`note` の先頭に「その他: 」）。
- **出典**:
  - 手引き 15.1（:405）、15.4（:499）、14.3（:329）、16.2（:538, :548-551）
  - 教科書 `docs/textbook/ch09.md:1037-1050`

### Q40. `sqlite3.connect` と「開くと作る」類【一部 手引きに無い: H-4-3（まれ）・O48 (3)・新しい穴 N8】

```python
conn = sqlite3.connect(DB_PATH)                 # 無ければ空のファイルを作る
rows = conn.execute("SELECT ...").fetchall()
db = shelve.open(PATH)                          # 既定の flag 'c' は無ければ作る
mem = sqlite3.connect(":memory:"); mem.execute("CREATE TABLE t(x)")
```

- **すること**:
  - `sqlite3.connect` が無いファイルを作るのは、ファイルの作成として反する（条件つき）。
  - ほかのライブラリの「開くと作る」形（`shelve`・`dbm` の `'c'` など）は、作ることを公式の文書で確かめられれば同じに読む。決め方は O48 (3)。
  - `:memory:` の DB の変更や、同じ呼び出しで `ROLLBACK` する変更は、「まれ」の H-4-3 として決めずに封をした（**仮の扱いは無い**）。D76 の 2 の「メモリの中」とも読めるが、答えが変わるなら 22 節。
- **結果**:
  - `違反`、`condition_type` = `初回`。
  - `write_target`: 同じ DB を変える文（`INSERT`・`CREATE`）もあれば、データベース。作成だけのときは表に例が無い（N8）。**仮の扱い**（O48 (6) N8）: その他・不明（`note` の先頭に「その他: 」）。
- **出典**:
  - 手引き 15.1（:427-428「**`sqlite3.connect` が無いファイルを作る**: ファイルの作成として反する。条件つきで、条件の種類は 14.3 の「環境が変わるのは一部」の行による（D76）」）
  - 手引き 16.2（:546, :548-551）
  - `docs/decisions.md:4430`
  - `docs/drafts/guide_holes_triage.md:79`

### Q41. DB の変更・残る設定・接続単位・ORM【一部: O48 (3)】

```python
conn.execute("PRAGMA journal_mode=WAL")     # DB のファイルに残る
conn.execute("PRAGMA foreign_keys=ON")      # 接続単位
conn.execute("BEGIN"); ...; conn.commit()   # トランザクション
session.add(Hit(q=q)); session.commit()     # ORM の INSERT
Base.metadata.create_all(engine)            # 表が無ければ作る
```

- **すること**:
  - SQL は先頭の語と中身で決める。
  - ORM は、どの SQL になるかを公式の文書で確かめる（決め方は O48 (3)）。
  - `create_all` がモジュールの一番上にあるなら、読み込み時なので到達しない（Q26）。
- **結果**:
  - 反する: `PRAGMA journal_mode=WAL`、`INSERT`、`VACUUM` など。`write_target` = データベース。
  - 反しない: 接続単位の `PRAGMA`、`BEGIN`/`COMMIT`、`SELECT`。
  - 呼び出しの中で毎回 `create_all` を呼ぶなら `condition_type` = `初回`。
- **出典**: 手引き 15.1（:408-411）、16.1（:518）、教科書 `docs/textbook/ch50.md:479-480`

### Q42. HTTP のメソッド（GET で作る API・POST の意味・ヘルパーに隠れたメソッド）

```python
httpx.get(f"{API}/send?to={to}")                       # GET で送信する API
requests.post(f"{API}/v1/search", json={"q": q})       # 照会の POST
requests.post(f"{API}/v1/notes", json=note)            # 作成の POST
def _call(method, path, **kw): return session.request(method, BASE + path, **kw)
_call("DELETE", f"/cache/{k}")                         # メソッドは呼ぶ側の定数
```

- **すること**:
  - `PUT`・`PATCH`・`DELETE` は反する。
  - `GET`・`HEAD`・`OPTIONS` は反しない。`GET` で送信・作成する API でも、表の行を採って反しない。
  - `POST` は相手の API の意味で決める。作成・更新・削除なら反し、照会なら反しない。
  - API 名で決めてよいのは、名前が作成・更新・削除（または照会）をはっきり示すときだけ。そのときは `evidence` に「API 名から」と書く。
  - ツールの docstring は、相手の API の文書ではない。
  - メソッドを引数で受けるヘルパーは、呼ぶ側の値までさかのぼる。モデルがメソッドを決められるなら反する。
  - 分からなければ不明（類「相手の API」）。
- **結果**: 作成の POST は `違反`、`write_target` = 相手側の状態。
- **出典**:
  - 手引き 15 の前書き（:389-397）、15.1（:412-414）、13.1（:276）、19（:722-723, :728）
  - `docs/decisions.md:4440`

### Q43. GraphQL

```python
requests.post(GQL, json={"query": "query { items { id } }"})          # 照会
requests.post(GQL, json={"query": "mutation { addTag(id: 1) { ok } }"}) # 書き込み
requests.post(GQL, json={"query": query_from_model})                   # 文をモデルが決める
```

- **すること**:
  - どれも同じ URL への `POST` なので、本体の文が `query` か `mutation` かで決める。
  - 文をモデルが決めるなら、取りうる値の全体（`mutation` も書ける）で考えると読める。手引きの例は SQL の `db_model_sql` だけで、GraphQL の文をモデルが決める例は無い（**仮の扱い**、O48 (4)）。
- **結果**:
  - `mutation`: `違反`、`write_target` = 相手側の状態。
  - `query`: `違反でない`。
  - モデルが文を決める形: `違反`、`condition_type` = `引数`（仮の扱い。`note` に「O48 (4) の仮の扱い: …」）。
- **出典**: 手引き 15.1（:413）、11.3（:91）、13.1（:269）、教科書 `docs/textbook/ch50.md:529-547`

### Q44. 認証・トークン・ログインの POST と、トークンの保存

```python
tok = requests.post(f"{AUTH}/oauth/token", data=creds).json()
TOKEN_FILE.write_text(json.dumps(tok))      # 期限切れのときだけ更新して保存
```

- **すること**:
  - `POST` そのものは、相手の文書で決める。文書に無ければ不明。
  - 保存は、ファイルの書き込みとして別に読む。
- **結果**: 保存は `違反`、`condition_type` = `失敗・期限切れ`、`write_target` = キャッシュ・状態の保存。
- **出典**: 手引き 15.1（:429「相手の文書で決める。文書に無ければ不明（D76）」）、14.3（:314）、16.2（:536）

### Q45. 外のログ・エラー収集・テレメトリ・syslog【一部: O48 (3)】

```python
sentry_sdk.init(dsn=DSN)                   # 以後、例外のたびにライブラリが送る
posthog.capture(user, "search", {"q": q})
logger.addHandler(SysLogHandler(address="/dev/log"))
```

- **すること**:
  - `POST` の行と同じく、相手の API の意味で決める。
  - `init` だけ書いて、例外のたびにライブラリが中で送る形は、「ライブラリの中の動作」の扱い（O48 (3)）に当たる。
- **結果**:
  - ツールの道筋で直接送る呼び出し（`posthog.capture(...)`）: 相手の文書で記録の作成と確かめれば `違反`、`write_target` = 相手側の状態。
  - `sentry_sdk.init` だけで、ライブラリが中で送る形: 読む範囲の外なので答えは変えず、`note` に書く（**仮の扱い**、O48 (3) の ④）。
  - `SysLogHandler` をロガーに付けていて、ツールの道筋がそのロガーに書く: syslog への送信として、15.1 の外のログの行で決める。
- **出典**: 手引き 15.1（:430）、`docs/open_questions.md`

### Q46. HTTP 以外で相手を変えるもの（メール・キュー・クラウドの保存・gRPC）【一部 手引きに無い: O48 (4)】

```python
smtp.send_message(msg)
s3.put_object(Bucket=B, Key=k, Body=b)
channel.basic_publish(exchange="", routing_key="jobs", body=q)
stub.CreateItem(req)                       # gRPC
```

- **すること**:
  - 15.1 の表に行が無い。**仮の扱い**（O48 (4)。`04_rules.md` の 2 節）: 15.1 の問いの文（呼び出しの後に、相手のサーバの状態が残るか）で決める（15 の前書きは、表の行と問いの文が食い違うときに表の行を採るとだけ書く。行が無ければ問いの文）。
  - 何をするかは、名前か公式の文書で決める（決め方は Q47、O48 (3)）。分からなければ `不明`（類 `相手の API`）。
  - `write_target` は 16.1 を上から当てはめる。決められなければ その他・不明（`note` の先頭に「不明: 」。16.2 の末尾）。
- **結果**: 送信・保存・投入・作成は `違反`（`note` に「O48 (4) の仮の扱い: 15.1 の問いの文で決めた」）。
- **出典**: 手引き 15 の前書き（:389-397）、15.1（:401）、16.1（:513-517）、16.2（:548-551）、`docs/open_questions.md`

### Q47. SDK のメソッドが HTTP を隠している【手引きに無い: O48 (3)】

```python
repo.create_issue(title=t)          # 名前で作成と分かる
jira.transition_issue(key, "Done")  # 名前で更新と分かる
client.sync(project_id)             # 名前で分からない
```

- **すること**: **仮の扱い**（O48 (3) の推奨。`02_steps.md` の段 4 の 5）で決める。
  - 名前が作成・更新・削除・書き出し・送信か、読み取りをはっきり示すなら名前で決め、`evidence` に「関数名から」と書く。
  - そうでなければ公式の文書で決める。
  - 決まらず、答えが変わるなら `不明`（類 `相手の API`）。
  - 名前で決めた件は数えて報告する（POST の API 名の規則と同じ扱い）。
- **結果**: `create_issue` は `違反`（相手側の状態）。`sync` は文書しだいで、文書が無ければ `不明`。
- **出典**: `docs/open_questions.md`、手引き 15.1（:413）、`docs/decisions.md:4440`、教科書 `docs/textbook/appendix-i-4.md:939`

### Q48. 定数のコマンド（SPAWN）と、実態調査で調べてよい範囲【一部: O48 (3)】

```python
subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True)
subprocess.run(["git", "diff", path], capture_output=True)          # path はモデルの引数
subprocess.run("grep -n " + shlex.quote(q) + " notes.txt", shell=True)
```

- **すること**:
  - 起動するコマンドをモデルが決められるなら、反する。
  - 定数なら、そのコマンドが実際に何をするかを公式の文書で調べる。名前から「読み取り」と決めない。`git status` は、既定で index を書き出すと文書にある。
  - モデルが引数・オプションを渡せるなら、環境を変えるオプション（`git diff --output=`）があれば反する。
  - `shlex.quote` は別のコマンドをつなげるのを防ぐが、`-` で始まるオプションは通す。
  - 実態調査（見落としの手順）では、ライブラリの中を読まない。付録 I-4.13 は不の中身の判定で、git のソースまで開いて条件を決めた例なので、そのまま写さない。ソースを開いてよいかは O48 (3) の (c) で、まだ決まっていない。
- **結果**:
  - 文書で書くと分かれば `違反`、`write_target` = プロセスの起動・コードの実行。子が何を変えるか分かっても、常にこの種類。
  - 文書で分からなければ `不明`。
- **出典**:
  - 手引き 15.1（:407, :431-432）、16.2（:543）、19（:720-723）
  - 教科書 `docs/textbook/appendix-i-4.md:1004-1069`、`docs/textbook/ch50.md:576-662`

### Q49. 子プロセスの標準入力・木の中のスクリプトの起動【一部 手引きに無い: 新しい穴 N4】

```python
p = subprocess.Popen([sys.executable, "-m", "app.worker"], stdin=PIPE)   # 木の中の worker
p.communicate(json.dumps(job).encode())
subprocess.run(["./bin/convert", q])                                     # 木に無いプログラム
```

- **すること**:
  - 標準入力に書くこと自体は、ファイルを変えない。
  - 子プロセスの動作は全部数える（標準入力の中身で起きる動作に限らない）。
  - 木の中のスクリプトなら読む。木に無いなら、名前から推さずに不明（付録 I-4.15 の類は「その他」）。
  - 子のスクリプトの中を何段と数えるかは、手引きに無い（N4。解析器は降りない）。**仮の扱いは無い**: 深さ 4 の内か外かで答えが変わるときだけ 22 節。
- **結果**: 子が書けば `違反`、`write_target` = プロセスの起動・コードの実行。
- **出典**:
  - 手引き 15.1（:420-422）、18.2 の 5（:615「子プロセスの中の動作」）、16.2（:543）
  - 教科書 `docs/textbook/appendix-i-4.md:516`（分からないのに E5 に倒さない）、`:1201`

### Q50. プロセスのメモリの中の状態・`os.environ`・`chdir`【未決: O47・O48 (4)】

```python
_HISTORY.append(q)            # モジュール水準の list
@lru_cache(maxsize=256)
def _lookup(q): ...
os.environ["LAST_QUERY"] = q
os.chdir(project_dir)
```

- **すること**:
  - 今の手引きでは、メモリの中に残る状態は反しない（D76 の 2）。
  - ただし O47 で、この決定を保つか（a）、数えるか（b）を、学生が封の前に決める。
  - `os.environ`・`chdir`・ログの設定の書き換えなど、メモリ以外のプロセスの状態は手引きに無い。**仮の扱い**（O48 (4)。`04_rules.md` の 2 節）: プロセスが終われば消えるので、D76 の 2 と同じく数えない。
  - 起動して残る子プロセス（常駐するサーバ）は、15.1 のプロセスの起動の行で決める。
- **結果**:
  - メモリの状態: 今の手引きでは数えない（D76 の 2）。
  - `os.environ`・`chdir`: 数えない（それで答えが決まったなら `note` に「O48 (4) の仮の扱い: …」）。
- **出典**:
  - 手引き 15.1（:424-426「**プロセスのメモリの中に残る状態**（モジュール水準の辞書・キャッシュなど）: **反しない**」）
  - `docs/decisions.md:4117-4120`
  - `docs/open_questions.md`

### Q51. キャッシュの置き場所（メモリ・ディスク）と、鍵が引数のとき

```python
_cache[q] = res                                        # メモリ → Q50
(CACHE_DIR / f"{h(q)}.json").write_text(res)           # ディスク: 毎回書く
p = CACHE_DIR / f"{h(q)}.json"
if not p.exists(): p.write_text(res)                   # ディスク: 無いときだけ書く
cdb.execute("INSERT OR REPLACE INTO c VALUES (?, ?)", (q, res))   # SQLite のキャッシュ
```

- **すること**:
  - ディスクのキャッシュは反する。
  - 毎回書くなら `なし`。「無いときだけ書く」形で鍵が引数なら、`引数` とも `初回` とも読めるので、表の上の `引数` を 1 つ書く。
  - 書き込み先の種類は次のとおり決める。
    - 判定しているツールが読み返すなら、キャッシュ・状態の保存。
    - SQLite のキャッシュ DB なら、データベース（順 2 が順 6 より先）。
    - 読み返さないなら、名前がキャッシュでもキャッシュ・状態の保存にしない（Q53）。
- **結果**:
  - 毎回書く行: `違反`、`condition_type` = `なし`。無いときだけ書く行: `違反`、`condition_type` = `引数`。
  - `write_target`: このツールが同じファイルを読み返すなら キャッシュ・状態の保存。読み返さないなら その他・不明（`note` の先頭に「その他: 」。Q53）。SQLite のキャッシュ DB は データベース。
- **出典**: 手引き 14.3（:340-341）、15.1（:405, :424）、16.1（:522, :526）、16.2（:546）、20.1（:816-819）

### Q52. ファイルを読むだけ・開くモードの読み違い

```python
open(path).read()                         # 'r'
open(path, encoding="utf-8", mode="w")    # mode= が後ろにある
open(path, "w")                           # write しなくても、開いた時点で中身が消える
open(path, "a" if append else "w")        # 両方の枝を考える
open(path, "r+")                          # 読み書き。書けば上書き
```

- **すること**:
  - モードを `mode=` まで確かめる。変数ならさかのぼり、条件で変わるなら両方の枝を考える。
  - ファイルの読み取りは反しない（表の行）。atime などメタデータだけの変化も、この行で読む。
- **結果**: `'w'`・`'a'`・`'x'`・`'w+'`・`'a+'` と、書く `'r+'` は `違反`。
- **出典**: 手引き 手順 C（:150）、15.1（:415）、教科書 `docs/textbook/ch09.md:1037-1050, 1104-1118`

---

## E. 書き込み先の種類（`write_target`）

### Q53. 「読み返す」の主語と、ログとその他の境

- **すること**:
  - 「読み返す」の主語は、判定しているツールだけ。同じサーバの別のツールが読み返しても、数えない。
  - 名前がキャッシュでも、そのツールの道筋で読み返していなければ、キャッシュ・状態の保存にしない。16.1 の順 5（一時ファイル）以降を当て、当たらなければその他・不明にし、`note` の先頭に「その他: キャッシュの名前だが読み返しが無い」と書く（16.2 の末尾）。初回に作る作業ディレクトリだけは、読み返さなくてもキャッシュ・状態の保存（16.2）。
  - 読み返さない記録のうち、ログにするのは「いつ・何をした」を書く行だけ。
- **出典**: 手引き 16.1（:520, :522, :526）、16.2（:540）、20.1（:816-819）

### Q54. 境目のラベル

| 形 | 付ける種類 |
|---|---|
| `/tmp`・`tempfile` に置き、後で読み返す・前の残りを消す | 一時ファイル（場所で決める） |
| ツール自身の設定ファイル | 読み返す状態ならキャッシュ・状態の保存、利用者が開いて直す設定なら利用者のファイル（D86 の 6） |
| 運用者が環境変数で決めた場所への書き込み | 中身で決める |
| 初回に作る作業ディレクトリ（読み返さなくても） | キャッシュ・状態の保存 |
| 受け渡しファイルの残りの削除 | その他・不明（`note` の先頭に「その他:」） |
| 利用者の文書・データとして扱われるファイル（ツールが読み返しても） | 利用者のファイル（16.1 は上から当てはめ、順 3 が順 6 より先）。利用者のデータかどうかを決められないときだけ その他・不明（`note` の先頭に「不明: 」） |

- **出典**: 手引き 16.2（:536-546, :548-551）、`docs/decisions.md:4430-4431`、教科書 `docs/textbook/ch54.md:3231, 3242`

### Q55. 違反が複数あるとき（どの位置でラベルを取るか・読む順・`;` の順）【一部 手引きに無い: O48 (4)】

- **すること**:
  - 最初に見つけた違反で止めてよく、ラベルはその位置から取る（D82。(B)(C) は下限）。
  - 止めずに複数を読んだら、条件の一番弱い動作の種類・条件・深さを書く。弱い順は、なし → 引数 → 初回 → 失敗・期限切れ → 外部の状態 → 運用者の設定・起動の方法。
  - 次の 4 点は手引きに無い。**仮の扱い**（O48 (4)）を添える。
    - 読む順（どれが「最初」か）。仮の扱い: 浅い深さから、同じ深さでは呼ばれる行の順。
    - 「かつ」で重なった条件（`引数;初回` など）の強さの比べ方。仮の扱い: 重なった中で一番強いものの強さ（重なった方が起きにくい）。
    - `condition_type` を `;` で並べる順。集計は書いた順のまま組み合わせを数えるので、全件で同じ順にそろえる。仮の扱い: 14.3 の表の順（手引き 14.3 の例 `運用者の設定;失敗・期限切れ` は表の順と違う）。
    - `違反（深さ 4 の外）` に付けるラベル。仮の扱い: `違反` と同じ付け方。
- **出典**:
  - `docs/decisions.md:4278`
  - 手引き 18.2 の 7（:630-631）、手順 G（:191-198）
  - `docs/open_questions.md`

---

## F. 進め方と記録

### Q56. 見てはいけないもの・AI の使い方

- **すること**:
  - 解析器の出力（矛・不・summary）、v4 の判定、付録の答えは見ない。
  - 実態調査を最初に判定し、終えるまで最終評価の解析器の出力を見ない。
  - 18.2 の 1〜7（読む・書き出す・結果とラベルを記録する）は、AI を使わずに行う。Python の書き方やライブラリの意味が分からないときは、公式の文書を自分で開く。
  - 英語の文書を機械翻訳にかけるのは `ai_used` に当たらない。ただし訳すのは自然言語の文書だけで、コードと宣言は渡さない。使った翻訳の道具を `note` に書く。
  - 記録した後に、AI に事実の問いで点検させてよい。新しく見つかった動作は自分で開いて確かめ、`ai_found` に書く。`outcome` は変えない。
  - AI に貼る前に、`annotations=…`、宣言を述べる文（docstring・コメントの「read-only」など）、秘密の値（API キーなど）を伏せる。
  - 使う AI は、記憶を切った新しい会話（件ごとに新しく）。この repo を開いた道具や、repo の文書を読ませた会話は使わない。
  - 宣言の値・解析器の出力・自分の結論は渡さない。「読み取り専用か」「宣言に反するか」のような判断の問い（言い換えも）は聞かない。
  - 手順は `02_steps.md` の段 10。
- **出典**:
  - `docs/decisions.md:4276-4283`（D82）、`:3860`（D70 の 3 の条件 3）、`:4439`
  - 手引き 18.2（:595, :632-636）、21 の 6（:880-913）

### Q57. いつ「不明」にするか

- **すること**:
  - 20〜30 分（`minutes` と同じ測り方）調べても決まらなければ不明にする。調べれば分かるものは不明にしない。
  - 手引きで決まらない点（仮の扱いも無いもの）は、20〜30 分を待たずに不明にしてよい（目安は「調べれば分かるもの」のため）。
  - 届くかを決められなくても、届いたとしても反しない動作は、不明の理由にしない（`違反でない` のまま。D86 の 10。Q58）。
  - 理由の類を 1 つ選ぶ: 外の値 / 相手の API / 起動・初期化 / 動的な呼び出し / 手引きで決まらない / その他。
  - 実態調査は解析器を見ないので、`打ち切り` は使わない（O48 (4) の推奨）。
  - 手引きのどの規則にも当てはまらない形は 22 節に従う。途中で規則を足さない。
  - 深さ 4 までを時間の中で読み切れないときの扱いは手引きに無い。**仮の扱い**（O48 (4)）: 読み続ける。やめるなら `不明`・類 `その他`。
- **出典**: 手引き 19（:716-744）、22（:917-928）、`docs/open_questions.md`

### Q58. 到達・反するの組み合わせと、結果の値

| 状況 | 結果 |
|---|---|
| 到達しない | その動作は数えない。ほかに無ければ `違反でない` |
| 到達は決められないが、どう見ても反しない | `違反でない`（D86 の 10） |
| 到達するが反するか決められない、または到達が決められず反しうる | `不明` |
| 違反が深さ 4 の外にだけある | `違反（深さ 4 の外）` |
| 1 つのツールに違う結果の動作が混ざる | 違反 ＞ 不明 ＞ 違反でない（18.2 の「見落とし ＞ 不明 ＞ …」の当てはめ。**仮の扱い**、O48 (4)）。深さ 4 の外の違反と、深さ 4 の中の決められない動作が重なるときは `違反（深さ 4 の外）`（18.3 の字義「深さ 4 の中に「反する動作」が無く…」。中の動作は `note` に「深さ 4 の中の不明: …」） |

- **出典**:
  - 手引き 11.2（:62-69）、18.2（:619）、18.3（:643-647）
  - `docs/decisions.md:4435`
  - `docs/open_questions.md`

### Q59. 記録の落とし穴

- **すること**:
  - `違反でない` でも、読んだ範囲（深さのメモ）を `evidence` に書く。
  - 行は自分で開き直して書く。AI・教科書・v4 の記録の行番号を写さない。パスは木の根から書く。
  - 条件の中身は `condition` 欄に書く。`condition_type` が `なし` のときは空にする（O48 (4) の推奨）。
  - `target_by_arg` は付けない。`cause` は書かない（O48 (4) の推奨）。
- **出典**:
  - 手引き 18.4（:653-667、:662「**「反する動作は無い」でも、読んだ範囲を書く**」）、手順 H（:235, :247-248）
  - `docs/decisions.md:4371`
  - `docs/open_questions.md`

---

## まだ決まっていない点と、どの項目が関わるか

**未決の項目（O47・O48）**

| 項目 | 関わる FAQ |
|---|---|
| O47（メモリの中の状態を数えるか） | Q50 |
| O48 (1)（middleware・枠組みが呼び戻す関数） | Q12、Q16 |
| O48 (2)（間接の呼び出しの列挙） | Q13 |
| O48 (3)（外のライブラリの関数の意味の決め方、ライブラリの中の書き込み） | Q18、Q40、Q41、Q45、Q47、Q48 |
| O48 (4)（実態調査の節） | Q05、Q06、Q08、Q11、Q15、Q19、Q20、Q46、Q50、Q55、Q57、Q58、Q59 |
| O48 (5)（1 つの宣言を複数のツールが使う） | Q04 |

**「まれ」として決めずに封をした穴、と 22 節に送る形**

| 穴 | 関わる FAQ |
|---|---|
| H-3-20（遅延 import） | Q24 |
| H-3-17・H-3-19（起動の形） | Q28 |
| 教科書の境目 6（登録が `main()` の中だけ。仕分けの表に無い） | Q28 |
| H-4-3（`:memory:`・`ROLLBACK`） | Q40 |

**新しい穴（O48 (6)）**。`note` には「O48 (6) N<k> の仮の扱い: …」と書く。「無い」の行は、それで答えが変わるときだけ 22 節（`不明`）。

| 番号 | 中身 | 練習の仮の扱い | 関わる FAQ |
|---|---|---|---|
| N1 | 暗黙に走るコードの読む範囲と深さ（`@property`・`cached_property`・`__enter__`/`__exit__`・`__call__`・dataclass の `__post_init__`/`default_factory`・pydantic の検証子） | 読む。書かれた位置から 1 段（構築で走るものは `__init__` と同じ 1 段） | Q10、Q14 |
| N2 | 解析器の INDIRECT の表に無い間接の形（`Executor.map`・`call_soon`・`add_done_callback`）、起動時から常駐の worker、`atexit` の書き出しの深さ（`atexit` の到達の明文も無い） | 表に無い形も 1 段。常駐の worker は積む行の関数から 1 段。`atexit` は無い | Q13、Q34 |
| N3 | ログの水準で書かれない記録（水準が定数、または環境変数） | 無い | Q36 |
| N4 | 起動した木の中のスクリプト（子プロセス）の深さ | 無い | Q49 |
| N5 | `config.py` の定数が「運用者が書き換える前提」かの見分け方 | 無い | Q31 |
| N6 | ツールをまたぐ値の流れ（別のツールが入れた値をモデルの値とするか） | 無い | Q35 |
| N7 | lifespan の初期化の失敗を握りつぶす形の `condition_type` | `失敗・期限切れ` | Q27 |
| N8 | 作成だけの空のファイル（`sqlite3.connect` だけ・消さないロックファイル）の `write_target` | その他・不明（`note` の先頭に「その他: 」） | Q39、Q40 |
| N9 | 呼ぶ側が渡さなかった引数の既定値の関数に降りるかと、その深さ | 降りる。`writer(q)` を書いた関数から 1 段 | Q15 |

**教科書や手引きの当てはめで答えた項目**（手引きに直接の例は無い）: Q06 の条件つきの `mount`、Q43 の GraphQL の文をモデルが決める形。