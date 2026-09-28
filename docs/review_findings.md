# 添削の所見の表（3 観点の突き合わせ。`scripts/review_table.py` で再生成）

所見 151 件。3 観点そろった 147 件のうち **生き残り 146 / 落ちた 1**（未完 4）。生き残り = 2 観点以上を生き延びたもの（review_plan.md §4.2）。

| 生き残りの重大度（代表値） | D1 / D2 に効く | 評価の道具 |
|---|---|---|
| 高 | 14 | 0 |
| 中 | 50 | 6 |
| 低 | 55 | 21 |

向き（生き残り）: 誤 clear 76、数え落とし 36、誤警報 26、規則との食い違い 7、非決定 1

## 生き残った所見（重大度順）

| id | 重大度（探索 / 設計 / 一般性） | 向き | 影響 | 実行 | 設計 | 一般性 | 直し方は一般に正しいか | 所見 |
|---|---|---|---|---|---|---|---|---|
| R1-r1-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `env_join` の「片側だけの束縛はその側の値を残す」規則が属性パス（`self.x` / `OBJ.x`）と `global` 名にも適用され、片方の枝の書き込みが他方の経路で読める既存の値（フィールド / モジュール値）と合流せず、MODEL → OP / mode が |
| R1-r1-2 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `**` 実引数と呼び出し先の `*args` / `**kwargs` を捨てる: `f(**d)` の `d` は評価も受け渡しもされず受け取る仮引数が OP/resolved の `Atom(formal)` になる、`*args` / `**kwargs` は種付けされず |
| R1-r1-3 | **高**（高 / 高 / 中） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | 継承したメソッドの呼び出しが、木の別のクラスに同名メソッドがあるだけで解決されず効果が消える（`_resolve_in_tree` の `typed_classes` の絞り込みが受け手の自クラス名だけで、基底を含む家族 `_class_family` を使わない） |
| R1-r3-2 | **高**（高 / 中 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | ローカルのオブジェクトへの属性書き込み `c.cmd = cmd` は env の鍵 `c.cmd` にしか記録されず `Obj.fields` に載らないので、そのオブジェクトを**引数（位置 / キーワード）として渡す / 関数から返す / 2 段の属性 `h.config. |
| R1-r4-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | モジュール別名経由の属性読み出し `config.ROOT` / `cfg.SQL_PURGE` / `config.client`（`from . import config` / `import pkg.config as cfg`）が木内モジュールの束縛に一度も解かれない: |
| R2-r1-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | snake_case の ToolAnnotations（read_only_hint= / destructive_hint=）は mcp>=2.0 では protocol に届く宣言なのに、版を見ずに常に D_malformed（⊥）にして D1 / D2 を判定しない（誤  |
| R2-r1-2 | **高**（高 / 中 / 高） | 数え落とし | D1+D2 | ○ | ✗ | ○ | ○ | デコレータ構文でない登録（mcp.tool(...)(fn) / mcp.tool()(fn) / self.mcp.tool()(self.m) / mcp.add_tool(fn, annotations=...)）を入口にせず、ツールが宣言ごと丸ごと消える（数え落とし・誤  |
| R2-r3-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | mcp 2.x 低レベル（Server(on_call_tool=)）のハンドラでは `params` を裸の Atom として種付けするため `params.arguments[...]` が MODEL/opaque(unresolved) になり、原理 3-a の行（D2  |
| R4-r1-1 | **高**（高 / 中 / 高） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | asyncio.create_subprocess_exec(*cmd) の * 展開で argv0 がリスト全体になり、定数の program でも MODEL 由来として矛（本来は不） |
| R4-r2-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | INDIRECT 表は `args_pos` の位置引数 1 つ（または `args=`）しか渡さず、`to_thread(f, a, b)` / `partial(f, a, b)` の 2 つ目以降の実引数と `Thread(target=f, kwargs=…)` を捨てる |
| R4-r2-2 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | INDIRECT 形（to_thread / partial / Thread(target=)）の target が bound method（`store.delete` / `self._delete`）のとき受け手を評価も受け渡しもしないので、被呼び出しの `self.< |
| R4-r4-1 | **高**（高 / 高 / 高） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | FastMCP / 低レベル Server の lifespan 文脈（`ctx.request_context.lifespan_context` / `server.request_context.lifespan_context`）経由の受け手に型が付かず、その先の DB  |
| R4-r4-2 | **高**（高 / 高 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | pydantic BaseModel / dataclass で型付けしたツール引数（`req: WriteReq`）のフィールド読み出し `req.path` が MODEL/opaque(unresolved) になり、原理 3-a の「選べる」（MODEL かつ resol |
| R5-r1-1 | **高**（高 / 中 / 高） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | analyze._SELF_FIELD_CACHE が id(index) を鍵にするため、1 プロセスで複数の木を解析すると（scan_v2.py / two_sided.py）別の木のクラスのフィールドが流用され、self.<field> 経由の効果が消える（false-cl |
| R1-r1-4 | **中**（高 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `lambda` の本体を一度も評価しない（`_ev_Lambda` は `dynamic` を返すだけ）ので、`asyncio.to_thread(lambda: ...)` / `run_in_executor(None, lambda: ...)` / 名前に束縛した la |
| R1-r1-5 | **中**（中 / 中 / 中） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | INDIRECT 行 `loop.run_in_executor` は受け手がローカル変数（`loop = asyncio.get_event_loop()`）だと `resolve_call_name` が None を返すので当たらず、`asyncio.get_event_l |
| R1-r1-6 | **中**（中 / 中 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | 読む側モジュールの条件つき import（try/except・if/else で同じ名前を 2 回 import）は `ambiguous` にはなるが候補が import 表の最後の 1 件だけで、先に書かれた import 先の効果が消える（ソースの順序に依存） |
| R1-r1-7 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | K = 16 を超える要素を `tail` に畳まず捨てる（`_ev_List` / `_ev_Dict` / `_concat` / Path の `/`）ので、17 番目以降の MODEL 要素が消え、`" ".join(cmd)` の shell_string や argv |
| R1-r1-8 | **中**（中 / 中 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | dataclass 形（`__init__` 無し）の構築で基底クラスの annotated field を無視し自クラスの field 順で実引数を割り当てる。さらに `_construct_in_tree` の Obj は主体 OP なので、記録されないフィールドの読み出しが |
| R1-r2-1 | **中**（中 / 中 / 中） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 外部ライブラリの呼び出し（import 表で木外のモジュールに解決する `subprocess.run` / `requests.get` / `builtins.open`、または受け手型が外部クラスの `httpx.AsyncClient().post`）が、末尾名だけで木内 |
| R1-r2-2 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | ジェネレータ関数（`yield`）を `for` / `async for` / `list()` / `join` / 内包で消費すると、yield された値が呼び出し元に流れず、MODEL 由来の値が OP/resolved の Unknown になる（誤 clear: 矛  |
| R1-r2-3 | **中**（中 / 中 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 内包表記（list / set / dict / generator）のループ変数を囲む関数の env に束縛するので、同名の外側の変数が上書きされる: MODEL の変数が定数に落ちる（誤 clear）／定数が MODEL になる（誤警報）。Python 3 では内包は独自スコ |
| R1-r2-4 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 入れ子の関数（閉包）を新しい空の env で実行するので、囲む関数の仮引数・局所変数（MODEL）が `opaque(unresolved)` の OP になり、`nonlocal` の書き込みは戻らず、`def f(c=cmd)` の既定値の捕捉も評価されない（誤 clear） |
| R1-r2-5 | **中**（中 / 中 / 高） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | クラスの構築 `C(...)` が import の意味（別名・`__init__.py` の再公開）を解かない: `from .impl import Runner as R; R(cmd)`、`from pkg import Runner`（pkg/__init__.py が |
| R1-r2-6 | **中**（中 / 低 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | クラス名を通した非束縛メソッド呼び出し `Base.__init__(self, cmd)` / `Base.run(self, line)` を Python の意味（第 1 位置引数がインスタンス）で扱わない: `Base.__init__` は同名候補が 2 つ以上で解決さ |
| R1-r3-1 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `with` / `async with` の文脈式が木内クラスのインスタンスのとき `__enter__` / `__exit__`（`__aenter__` / `__aexit__`）を一度も実行・解決しない: `as` の名前は `__enter__` の戻り値ではなくイ |
| R1-r3-10 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_builtin_value_op` に無い組込みの読み書き: `parts.pop(0)` / `opts.pop("cmd")` は MODEL/opaque（矛 → 不）、`opts.setdefault("cmd", cmd)` は書き込みが反映されず後の `opts[ |
| R1-r3-3 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_apply_transfer` のメソッド名だけの TRANSFER 照合（`resolve` / `format` / `encode` / `decode` / `split` / `rsplit` / `strip` / `lower` / `upper` / `rep |
| R1-r3-4 | **中**（中 / 中 / 中） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `Map` の widening が定数の項目を全部捨てる: 分岐の合流（`_shape_join` の同種 Map → `Map((), None)`）と添字代入 / `update`（`_bind` Subscript → `_append_tail` → `value_jo |
| R1-r3-7 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 要素をそのまま渡す組込みの反復（`enumerate` / `zip` / `sorted` / `reversed` / `dict.items` / `dict.values`）が未解決の呼び出し（D44）として扱われループ変数が MODEL/**opaque** になるので |
| R1-r3-8 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | D50 / G4 の注釈型付け（`sqlite3.Connection` / `httpx.Client` などの受け手型）が `_seed_params`（降下のとき）にしか無く、`_self_fields`（メソッド形ツールのクラスの `__init__` の仮引数）と `_ |
| R1-r3-9 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | クラス名経由の属性読み出し `Cls.ATTR`（`class Settings: ROOT = "/data"` の名前空間クラス、`class Clients: http = httpx.Client()`）が `_module_value` の対象外（`_module_as |
| R1-r4-11 | **中**（低 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 値（定数・モジュール水準のインスタンス）の再公開 `pkg/__init__.py: from .config import ROOT, client` を経た `from pkg import ROOT, client` が解けない: `_module_value` は `_m |
| R1-r4-2 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_element_of` が `tail` のある列 / 辞書で **tail だけ**を返し、既知の先頭要素 `elems` を捨てる: 長さの違う列の分岐合流（`cmds = [cmd]; if flag: cmds.append("rm ...")`、`[cmd, "ec |
| R1-r4-3 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | INDIRECT 形（`asyncio.to_thread` / `threading.Thread(target=)` / `functools.partial` / `submit` / `run_in_executor`）の target の解決が `_resolve_in |
| R1-r4-4 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `super().m(...)` の解決（`_super_callees`）が**直接の基底だけ**を見て止まる（`_find_init` / `_class_family` の「基底 3 段まで」と食い違う）ので、メソッドを定義しない中間クラスを 1 つ挟む継承（`A(B)`、 |
| R1-r5-1† | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_shape_join` の「None リテラルとの合流は None 側が dead」の規則（D35 (a)）が `Obj` にしか無く、`Path` / `Seq` / `Map` / `Atom(定数)` と `None` の合流が `Unknown` / `Atom()` |
| R1-r5-2† | **中**（高 / 中 / 中） | 数え落とし | D1+D2 | ○ | ✗ | ○ | ○ | `Obj.classes` が末尾名だけ（モジュール無し）なので、木の中の別モジュールに同名クラスがあり同名メソッドを持つと、`r = Runner(cmd); r.go()` の 2 文形は `_resolve_in_tree` の型絞り込みが 2 候補のまま `[]` を返し |
| R1-r5-3† | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ✗ | 組込みのコンテナ構築子 `set()` / `list()` / `dict()` / `collections.deque()` が未解決の呼び出し（OP/opaque の Unknown）になるため、その後の `parts.add(cmd)` は `container`（Se |
| R1-r5-4† | **中**（中 / 中 / 中） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 辞書の反復が**値**を束縛する: `_element_of(Map)` は値の join（または tail）を返すので、`for k in opts:` / `[k for k in opts]` / `sep.join(opts)` / `yield from opts` / |
| R2-r1-3 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | 低レベルハンドラが name 分岐を別関数（dispatch(name, arguments)）に委譲すると、効果はその関数から拾うのに join は手前のハンドラ本体しか見ず、全ツールの宣言が黙って未 join（⊥）になる（誤 clear） |
| R2-r2-1 | **中**（中 / 中 / 中） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | デコレータを変数に束縛した登録（ro_tool = mcp.tool(annotations=...); @ro_tool def f）は末尾名が tool でないので入口にならず、ツールが宣言ごと丸ごと消える（数え落とし・誤 clear。野外 1 木で 159 登録） |
| R2-r3-4 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `Tool(...)` リテラルの検出が書かれた名前の末尾成分 `Tool` にしか当たらないため、`from mcp.types import Tool as MCPTool`（corpus に 45+ 行、自前の `Tool` クラスと衝突する木で常套）で作った宣言が 1 つ |
| R3-r1-1 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 定数の複文 SQL（executescript / psycopg execute / exec_driver_sql）を先頭語だけで判定し、2 文目以降の DELETE / DROP が黙って「内」になる |
| R3-r1-2 | **中**（中 / 中 / 低） | 規則との食い違い | D1+D2 | ○ | ○ | ○ | ○ | SQL の先頭にコメント（`--` / `/* */`）があると先頭語が `--` になり、DELETE / UPDATE が「矛」でなく「不」になる |
| R3-r2-1 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 定数どうしの Str（str.upper/strip/replace/format() の結果、定数の join、定数 + 定数）は Value.const が None なので、SQL は「接頭辞」・HTTP メソッドは「読めない」扱いになる: `requests.reques |
| R4-r1-10 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | INDIRECT 形（to_thread / run_in_executor / partial）の target がライブラリ sink（subprocess.run / os.remove / os.chmod）のとき、また lambda 本体の sink と map(sin |
| R4-r1-2 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | proc.communicate(data)（位置引数）は pipe 行にならず、インタプリタへのコード投入 EXEC が消える（KW("input") しか引かない） |
| R4-r1-3 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | A(pos) に kw が無い行は、仮引数名で渡した呼び出しで slot（または効果行全体）を落とす: Popen/run(args=…)、open(file=…)、unpack_archive(…, extract_dir=…)、urlretrieve(…, filename= |
| R4-r1-4 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 受け手型が要る直接 sink（pandas.DataFrame.query / jinja2.Environment.from_string）と proxy 受け手型（neo4j.AsyncDriver/AsyncSession、arango、requests.session() |
| R4-r1-5 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | Path を返す pathlib のメソッド（expanduser / joinpath / with_suffix / absolute / Path.home() / Path.cwd()）が TRANSFER に無く、受け手が Unknown になって後続の pathlib |
| R4-r1-6 | **中**（中 / 中 / 低） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | ツール引数の注釈が Path / pathlib.Path のとき種が Atom になり、その引数への write_text / unlink（語彙にある sink）が受け手型で照合されず消える |
| R4-r1-7 | **中**（中 / 中 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 呼び出し式が文の先頭行より後の行から始まると entry_lineno に CFG ノードが無く、低レベル MCP ハンドラでは効果が join した全ツールに帰属して他ツールの宣言（readOnly）で矛になる（FastMCP では支配判定が cfg.exit に落ちる） |
| R4-r1-9 | **中**（中 / 中 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | str.split() / shlex.split() の結果は先頭の定数トークンを失い（Seq((), tail=全体)）、さらに tail 付き Seq の + 連結が後続要素を index 0 に置くので、argv0 が定数 "git" でも MODEL 由来として矛（本来 |
| R4-r2-3 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `str(p)` / `os.fspath(p)` / `p.as_posix()` / `str(cmd)` の恒等変換が TRANSFER に無く（`str` は組込み名の解決にも無い）、MODEL/resolved のパス・コマンドが `opaque(unresolved) |
| R4-r2-4 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `@property` / `@cached_property` で返す受け手（`store.conn` → `return self._conn`）を `_ev_Attribute` がフィールドと型遷移表でしか引かず、プロパティ本体を評価しないので受け手型が無くなり、その先の |
| R4-r2-5 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | メソッド形ツール / 閉包の注釈つき引数の `self` の種を作る `_self_fields` が自クラスの `__init__` とクラス体しか見ず、基底の `__init__`・`super().__init__()`・基底のクラス体既定値で束縛したフィールド経由の si |
| R4-r2-6 | **中**（中 / 低 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ✗ | `__init__` で `self.conn = None` とし別のメソッド（`connect()` / `start()` / lifespan）で束縛する遅延初期化では、`_self_fields` / `_construct_in_tree` が `__init__`  |
| R4-r2-7 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | モジュール水準の名前を関数内の `global` 再束縛で初期化する形（`_conn = None` + `init_db(): global _conn; _conn = sqlite3.connect(...)`）で、`_module_value` が `global` 側の |
| R4-r2-8 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | `Popen([sys.executable, ...], stdin=PIPE)` + `communicate(input=code)` / `stdin.write` で、`sys.executable` が interpreter カタログの `python*` に当たら |
| R4-r2-9 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `@classmethod` ファクトリの `cls(...)` が木内クラスの構築にならない（`cls` が局所束縛なので `_construct_in_tree` が None を返し unresolved）ため、`Store.open(path)` で作ったインスタンスの受 |
| R5-r1-2 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 同じモジュールに同名の関数定義が 2 つあると（if/else・try/except の分岐で別々に定義するツール）、2 つ目の定義が SourceIndex._funcs.setdefault で黙って捨てられ、ユニットにも記録にも残らない（count-loss → false |
| R5-r1-5 | **中**（中 / 中 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 起動スクリプト X.py とパッケージ X/ が同じディレクトリにあると、SourceIndex のモジュール表が X → X.py に固定され、X/__init__.py のツールが X.py の import 表で解析されて sink が黙って消える（false-clean） |
| R5-r2-2 | **中**（中 / 中 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | parse に失敗した / AST_NODE_CAP で落とした木内モジュールの関数を呼ぶツールは効果も行も出ず、unit 水準の印は外部呼び出しと同じ `opaque_reasons: unresolved` だけなので、宣言 D1/D2 に対して黙って「内」に見える（記録はフ |
| R2-r5-2† | **中**（中 / 中 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | `tools_list` 規則の要素解決が import 表を使わず裸の末尾名で木全体を引く: 別モジュールから import した関数は、木のどこか（tests/ の stub、examples/ の同名関数）に同名の関数があるだけで「一意でない」として黙って落ち（`fs_to |
| R2-r5-3† | **中**（中 / 低 / 中） | 規則との食い違い | tooling | ○ | ○ | ○ | ○ | ENTRY_RULES の gptme 規則（`spec_object` / `ToolSpec`）を実装しているコードが無い: `find_units` は decorator / method の 2 形しか扱わず（`find_entry_rule` も未使用）、`ToolS |
| R4-r1-8 | **中**（中 / 低 / 中） | 数え落とし | tooling | ○ | ✗ | ○ | ○ | ループ本体（2 周固定点）と中間の被呼び出しの複数呼び出し箇所で、バイト同一の効果行が重複して出力され、行単位の件数（compare_scans の「効果」、summary の rows / verdict 集計、review_plan §6 の 8,337）が膨らむ（run20 |
| R5-r1-3 | **中**（中 / 中 / 中） | 数え落とし | tooling | ○ | ○ | ○ | ○ | 評価道具のユニット同一性の鍵にモジュール / relpath が無いため、別モジュールの同名ツール（同じ関数名）の D1/D2 の矛が 1 件に潰れる: contradictions.json の n（scan_v2 は unit_id = framework:qualname: |
| R5-r1-4 | **中**（中 / 中 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | contradiction_by_decl.py はファイル名に '-' を含まない manifest を黙って読み飛ばす（`"-" not in fn`）ため、木の名前に '-' が無い run では矛 / 不がすべて 0 になる。intersection_rows.py /  |
| R5-r3-1 | **中**（中 / 中 / 中） | 誤警報 | tooling | ○ | ○ | ○ | ○ | scan_v2.py の contradictions.json（手検証の候補表）が、同じ (unit, site, kind) の矛の行を畳むとき relpath は最初の行、lineno は別ファイルの行の min から取るため、存在しない位置（別ファイルの行番号）を指す。r |
| R1-r1-10 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | 関数内の `try: from .m import f as g` / `except ImportError: g = None` の後の `g(p)` が、`g` が `local_bindings` にあるため import 表の写像を捨てて解決されない（別名なしの同じ形は |
| R1-r1-11 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | O31 の静的仮引数: 第 1 仮引数が `self` / `cls` 以外の名前のインスタンスメソッドでは実引数が 1 つずれて割り当てられ（`_seed_params_raw` / `_static_params` の offset を名前で決める）、リテラルの既定値で枝が刈 |
| R1-r1-12 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | G4 の外部型判定 `_is_external_class` が `resolve_module_strict` の末尾成分一致に依存するため、木に外部パッケージと同名のモジュール（`app/requests.py`）があると `requests.Session()` が木内の同 |
| R1-r1-9 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `cmd[0] = exe` のような添字代入が要素を置換せず列の末尾に追加する（`_bind` Subscript → `_append_tail`）ので、argv0 がリテラルのまま残り MODEL の argv0 が不になる |
| R1-r2-7 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ✗ | ○ | ○ | O31 の静的判定が `ast.If` にしか掛からず、条件式 `x if c else y` と短絡 `c and f()` / `c or f()` は静的な仮引数でも両側を評価する: `open(path, "a" if append else "w")` に `appen |
| R1-r2-8 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | インスタンスの呼び出し `r()` / `Runner(cmd)()` が `__call__` に解決されず、効果行が 1 本も出ない（数え落とし） |
| R1-r3-11 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 別名（`alias = r` / `argv = cmd`）の追跡が `is` 同一性だけで、`env_join` は両側に同じ Value がある鍵にも `value_join` で新しいオブジェクトを作るため、分岐・ループ・try を 1 つでも通ると別名が切れて `alia |
| R1-r3-12 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `try` 本体が必ず終わる（`return` / `raise`）ときも `else` 節を実行するので、到達しない `else` の sink が効果行になり readOnly の矛になる（誤警報。D58 規則 3 は try が関数を「終える」かの話で、`else` の到達 |
| R1-r3-5 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `match` 文の capture パターン（`case {"cmd": c}` / `case [exe, *rest]` / `case str(c)` / `case … as c` / `case c`）を一度も束縛しないので、MODEL の subject から取り出 |
| R1-r3-6 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 拡張アンパック `a, *rest, c = seq` で `*rest` に列全体が束縛され（スライスではない）、`*` より後の対象が左からの添字で割り当てられる（右端から数えない）ので、`_, *rest = ["prefix", exe, arg]` の argv0 がリ |
| R1-r4-10 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 名前を束縛し直しても古い属性パスの鍵（`s.path`）が env に残る: `_bind`（Name）は `env[name]` だけを置き換え `name.*` を消さず、`_ev_Attribute` は env の鍵を `Obj.fields` より先に読み、`_rece |
| R1-r4-12 | **低**（低 / 中 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | 木内で定義したデコレータ（`@audited` = 閉包 `wrapper` を返す関数）で包んだ関数 / ツールを呼ぶとき、`_descend_env` はデコレータを無視して元の def の本体だけを実行するので、wrapper の中の sink（監査ログの追記 `open( |
| R1-r4-13 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | モジュール水準のタプル代入 `SQL_PURGE, SQL_COUNT = "DELETE FROM sessions", "SELECT ..."` を `_module_assignments` が読まない（`ast.Name` の対象しか見ない。G3 の `_module_ |
| R1-r4-14 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | G4 / D50 の注釈型付けが、`Optional[...]` / `X ｜ None` の**中**に書いた前方参照の文字列（`conn: Optional["sqlite3.Connection"]`、`conn: "sqlite3.Connection" ｜ None`） |
| R1-r4-15 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `del cmds[0]` を無視する（`ast.Delete` は no-op）ので、`cmds = ["ls", cmd]; del cmds[0]; subprocess.run(cmds)` の argv0 が消したはずの定数 'ls' のまま（SPAWN_CONST_A |
| R1-r4-5 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | G3 改訂 3 の「読む側で呼ぶ名前が関数の中で書き換えられるなら ambiguous」の実装が `_scan_module_writes`（D17 改訂 2）をそのまま使うため、**別の関数の仮引数 / 局所変数**が import した関数と同名なだけで（`from .ren |
| R1-r4-6 | **低**（低 / 低 / 中） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | dataclass 形（`__init__` 無し）の構築で `__post_init__` を一度も実行しない: `__post_init__` で導いたフィールド（`self.cmd = "echo " + self.raw`）は `Obj.fields` に無く、読むと O |
| R1-r4-7 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 辞書表示の `**` 展開 `{**base, "target": target}` を `_ev_Dict` が `"<dynamic>"` キーの 1 項目（base の Map 全体）として置き、base の項目を平らにしないので、`d["exe"]`（base 側の定数キ |
| R1-r4-8 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ✗ | ○ | ○ | G4 / D50 の注釈型付け（`_seed_params`）がリテラルの `None`（`conn: Optional[sqlite3.Connection] = None` の既定値、または明示の `None` 実引数）を `Obj(sqlite3.Connection)`  |
| R1-r5-5† | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | G4 / D50 の注釈型付けが `Optional` の包みを import 表で解かず字面 `"Optional"` / `"typing.Optional"` でしか外さない（`_annotation_receiver_type` :2365、`_annotation_he |
| R1d-r6-5† | **低**（低 / 低 / 低） | 規則との食い違い | D4 | ○ | ○ | ○ | ○ | §7.4 の「DB: それ以外の先頭語 → 内」が §7.5「それ以外（ATTACH / NOTIFY / 分類に無い PRAGMA など）→ 不」と原理 2-a に反し、`_d4` は表どおり `NOTIFY` / `CALL proc()` / `COPY t FROM …` |
| R1d-r6-6† | **低**（低 / 低 / 低） | 誤 clear | D3 | ○ | ○ | ○ | ○ | `urljoin(BASE, ref)` の TRANSFER が「実引数が全部リテラルなら結果 = 受け手（BASE）の定数」とするため、`ref` が絶対 URL や `//host/x` の定数（`urljoin("http://localhost:8000/api/",  |
| R1d-r6-7† | **低**（低 / 低 / 低） | 誤 clear | D3 | ○ | ○ | ○ | ○ | `_host_class` が `url.host` の `Value.const`（Atom）しか読まないため、`crawl4ai.AsyncWebCrawler.arun_many([...])` の `urls`（`A(0, kw="urls")` の Seq）は要素が全部 |
| R2-r1-11 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | pydantic の lax 変換で True になる値（readOnlyHint=1 / "true"、destructiveHint=0）を『真偽値でない = 上界を動かさない』として ⊥ にする（誤 clear。まれ） |
| R2-r1-13 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | デコレータの第 1 位置引数で与えたツール名（@mcp.tool("delete_file")）を読まず関数名を tool_name にするので、同名の Tool リテラル / D_op の名前と join できない（まれ） |
| R2-r1-5 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | Tool(...) リテラルをツール名だけで木全体から join し、リテラルがどのサーバ / モジュール（テストを含む）に属するかを見ない: 別サーバ・テストの宣言が付く（誤警報）、同名の別サーバのリテラルに先勝ちで負けて自分の宣言を失う（誤 clear） |
| R2-r1-6 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 支配する name 判定のツール名が join されていない（リテラル名が非リテラル・またはリテラル無し）と、その効果を「共通処理」として join 済み全ツールに帰属し、他ツールの readOnly で矛にする（§2.9 (b) と不一致、誤警報） |
| R2-r1-7 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | `if name == ToolName.DELETE:` / `== ToolName.READ.value`（Enum 比較）から候補名を取らず、文字列名の Tool リテラルが 1 つも join されない（match 文では同じ Enum 表を引くのに Compare で |
| R2-r1-9 | **低**（低 / 中 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | for / while ブロックの直下で定義したデコレータ付きツールを索引しない（入れ子定義の落とし。数え落とし） |
| R2-r2-2 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 低レベルハンドラの name 分岐が否定形（`if name != "x": raise` / `if name not in ("x",): raise`）や定数が左の比較（`"x" == name`）だと候補名が 1 つも取れず、Tool リテラルが join されずに宣言が |
| R2-r2-3 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | デコレータ呼び出しの annotations が素のキーワードでない（`@mcp.tool(**RO)` / `@mcp.tool(name=..., **COMMON)` / 公式 SDK の位置引数 `@mcp.tool("n", None, "d", ToolAnnotat |
| R2-r2-4 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 引数値の比較の定数（`arguments["action"] == "write"`）が join 済みツール名と一致すると、その分岐の効果がそのツールにも帰属し、別ツールの厳しい宣言（destructiveHint:false）で矛にする（誤警報。§2.9 (b) の name |
| R2-r2-5 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `if name == "a" or name == "b":` の分岐は短絡 CFG で 2 つの test に分かれ、どちらも単独では効果を支配しないので join 済み全ツールに帰属し、readOnly の別ツールの D1 で矛にする（同値の `name in ("a",  |
| R2-r3-2 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | `add_request_handler("tools/call", ...)` の入口規則が SDK の署名と合わず一度も当たらない: mcp 2.x は全リリースで `(method, params_type, handler)` の 3 引数なのに `node.args[1 |
| R2-r3-3 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `Server(on_call_tool=h)` のハンドラを裸の末尾名で木全体から引く（呼び出し元モジュールの import 表 `scope` は作って捨てている）ので、tests/ の同名の test double や無関係な同名関数が lowlevel_v2 ユニットにな |
| R2-r4-1 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | R2-r4-1 [R2] mcp 2.x 低レベルの入口照合が書かれた呼び出し名の末尾 `Server` にしか当たらず、`Server` のサブクラス（`FsServer("fs", on_call_tool=h)` / `super().__init__(..., on_ca |
| R2-r4-2 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | R2-r4-2 [R2] デコレータの受け手が Call / Subscript のとき（`@get_mcp().tool(annotations=...)` / `@SERVERS["fs"].tool(annotations={...})`）`dotted_of` が Non |
| R2-r4-3 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | R2-r4-3 [R2] 同じ関数にカタログのデコレータが 2 段重なる（`@mcp.tool()` の下に `@admin.tool(annotations=ToolAnnotations(readOnlyHint=True))`、`@tool` の下に `@mcp.tool( |
| R3-r1-3 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | SQLite の括弧形の設定 `PRAGMA journal_mode(WAL)` / `PRAGMA user_version(3)` を「= の無い PRAGMA = 読み取り」として内に落とす（永続する設定なのに D1 矛 / D2 不にならない） |
| R3-r1-4 | **低**（低 / 低 / 低） | 数え落とし | D2 | ○ | ✗ | ○ | ○ | 低レベルハンドラの複数ツール帰属で `meet_d_kind` が explicit を和にするため、readOnly のツールが 1 つでも混ざると destructiveHint:false のツールの D2 が一度も評価されない（D2 の宣言別件数の数え落とし） |
| R3-r1-5 | **低**（低 / 低 / 低） | 誤警報 | D2 | ○ | ○ | ✗ | ✗ | `open(path, "a+")` / `"x+"` を「書き出し（上書き）」に分類する — Python の open では `a+` / `x+` は既存の内容を消せない追記型なので D2 で誤警報（path MODEL → 矛、path 定数 → 不。期待は内） |
| R3-r4-1 | **低**（中 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | 低レベル MCP ハンドラで name 判定が入れ子（外側 `name in ("peek", "rm", "mk")` の中に内側 `if name == "rm"` / `elif name == "mk"`）のとき、`_attribute_effects_to_tools` |
| R3-r4-2 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_first_element` が `Str`（連結した文字列）に対して `parts[0]` を返すので、shell=False で**文字列**（列ではない）を args に渡す `subprocess.run("/usr/bin/" + tool)` / `subproc |
| R3-r4-3 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `%` / `str.format` の書式テンプレートの先頭がプレースホルダで実引数に非リテラルが混ざる形（`"%s FROM t WHERE id = %s" % ("DELETE", os.environ["ID"])` / `"{} FROM t WHERE id = { |
| R3d-r6-3† | **低**（低 / 低 / 低） | 誤警報 | D3 | ○ | ○ | ○ | ○ | D3 の「private」の判定が名前について `localhost` / `*.localhost` / `*.local` の 3 形だけで、標準で私用と定まる名前（`*.internal`（ICANN 2024 予約、`host.docker.internal` を含む）・ |
| R4-r1-11 | **低**（低 / 中 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | 語彙にある sink の再公開別名（asyncio.subprocess.create_subprocess_exec / from asyncio.subprocess import …、sympy.parse_expr）が _suffix_match の完全一致・末尾 2 要 |
| R4-r3-2 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `_suffix_match` の末尾 2 要素一致が、木の中のモジュールがライブラリと同名（`app/requests.py` / `app/subprocess.py` / `pkg/os.py`、相対 import `from . import os` を含む）のとき、その |
| R4-r3-3 | **低**（中 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | スライスで複製した定数の列（`cmd = base[:]` / `base[1:]`）に MODEL を append / insert / extend / 添字代入すると、`_ev_Subscript` が Slice を要素の join（Atom）に潰し `_append_ |
| R4-r3-4 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ✗ | ○ | ○ | `git.cmd.Git` の proxy 行（method `*`、argv0 ← 'git' 定数）が GitPython の `Git.execute(command, ..., shell=)` にも当たり、実際の argv（command の先頭）と `shell=Tr |
| R4-r3-5 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `is_interpreter` が `/` でしか basename を切らないので、Windows のパス（`C:\\Python311\\python.exe`）を argv0 にした Popen + stdin パイプが EXEC にならず FS_WRITE の情報行にな |
| R4-r3-6 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ○ | ○ | ○ | `_pipe` の受け手判定 `"Popen" in c` が部分文字列一致なので、名前に Popen を含む木内クラス（`PopenRecorder` など）の `communicate(input=…)` / `stdin.write` が pipe 形の FS_WRITE  |
| R4-r4-4 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | `_self_fields` (1) のクラス体の走査が条件を逆に書いていて（`if not name.startswith("self.")` の後で `name[len("self."):]`）、クラス体の名前 N と `self` から N[5:] という捏造フィールド（` |
| R4-r4-5 | **低**（低 / 低 / 低） | 誤警報 | D1+D2 | ○ | ✗ | ○ | ○ | `git.cmd.Git` の proxy 行（method `*`）が GitPython の**子プロセスを起こさない**明示メソッド（`custom_environment` の with 文 / `update_environment` / `clear_cache` / |
| R5-r1-9 | **低**（低 / 低 / 低） | 誤 clear | D1+D2 | ○ | ○ | ○ | ○ | _self_fields の再帰打ち切り用の番兵 `()` が、__init__ の評価で RecursionError が出た後も cache に残るため、同じクラスの 2 つ目以降のユニットは印なしで self のフィールドを失う（順序依存の false-clean） |
| R5-r2-5 | **低**（低 / 低 / 低） | 数え落とし | D1+D2 | ○ | ○ | ○ | ○ | SourceIndex._index_body の再帰が If / Try / With の入れ子 1 段ごとに 1 フレーム使うため、約 1,000 段の入れ子（例: 1,200 分岐の elif 連鎖）を含むファイルが 1 つあると index.build() が Recur |
| R2-r1-12 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | ToolAnnotations(readOnlyHint=True, **EXTRA) のように明示キーワードと読めない展開が混ざると、確定している明示宣言まで捨てて全体を D_unknown にする（宣言の数え落とし。まれ） |
| R2-r1-4 | **低**（低 / 低 / 低） | 規則との食い違い | tooling | ○ | ○ | ○ | ○ | annotations のフィールド値が定数でない（readOnlyHint=IS_RO / Cfg.ro / not False、{**COMMON}）とき、その項を黙って落として ⊥ にし D_unknown にしない（仕様「読めない形は D_unknown とし ⊥ と混ぜ |
| R2-r2-6 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | `find_tools_list_units` の `already`（裸の関数名の集合）が、別モジュールの同名関数まで除外する: `@mcp.tool() def delete_file` が木にあると `Agent(tools=[delete_file])` に並べた別モジュ |
| R2-r4-4 | **低**（低 / 低 / 低） | 誤警報 | tooling | ○ | ○ | ○ | ○ | R2-r4-4 [R2] agno の method 規則（bases=Toolkit, names="*"）が、メソッドの**中に入れ子で定義した局所関数**（`FileTools.__init__._log` / `FileTools.run._run_impl`）までユニッ |
| R2-r4-5 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | R2-r4-5 [R2] method 規則の基底照合 `_class_bases` が書かれた基底名しか見ない: (a) `from langchain_core.tools import BaseTool as LCBaseTool` の `class RmAliasTool |
| R2-r5-1† | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | クラス形の入口（method 規則 / langroid ToolMessage）の認識が「書かれたクラス本体と直接の基底」だけを見て継承（MRO）を追わない: (a) `_run` を BaseTool 派生でない mixin から継承する / `_run = shared_f |
| R2-r5-4† | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | langroid の handler 解決が (a) `request` 値と同名のメソッドを**どのクラスからでも**拾う（Agent でない helper クラスの `search` / `update` / `add` が toolmessage_handler ユニットに |
| R3-r1-7 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | MODEL が選べる（resolved）連結 SQL の接頭辞が変更の文（`"DELETE … " + x`）でも理由を `db_model_sql` にするため、感度分析 3-b が「model を含む理由」として矛 → 不に倒し、3-b の行を過小に数える |
| R3-r1-8 | **低**（低 / 低 / 低） | 誤警報 | tooling | ○ | ○ | ○ | ✗ | `sqlalchemy.text("DELETE …")` を別の文で作って `execute(stmt)` すると、1 つの文が `text` 行の矛と `execute` 行の不（`db_sql_unreadable`）の 2 組になり、不の件数が水増しされる |
| R5-r1-10 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | シンボリックリンクのディレクトリは os.walk（followlinks=False）で辿られず、その中のツールはユニットにも parse_failures / truncations にも残らない |
| R5-r1-6 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | 木の時間上限（max_tree_seconds）に途中で当たって解析しなかったユニットは manifest に痕跡が無く（truncations: []）、evidence の manifest だけを読む道具（intersection_rows / compare_scans  |
| R5-r1-8 | **低**（低 / 低 / 低） | 規則との食い違い | tooling | ○ | ○ | ○ | ○ | contradictions.json（手検証の候補表）の destructive は行の効果ではなく同じ (site, kind) の最初の効果から取られるため、追記 open('a') の後に書き出し open(path,'w') がある D2 の矛の行に destructi |
| R5-r2-1 | **低**（中 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | two_sided.py の経路の鍵に入口ツール名が無い（witness_chain は被呼び出しの列だけ）ため、同じヘルパを通る兄弟ツールが 1 経路に潰れて最弱が残り、片方のツールにだけ入った修正（等級 / req_val の変化）が両側通過の分子から消える |
| R5-r2-3 | **低**（中 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | diff_effects.py は効果行の値を slot の主体 / 確度と resolution だけで比べるので、§7 の判定に効く属性（sql_head / fs_mode / destructive / http_method / exec_mode / 定数）の変化と矛 |
| R5-r2-4 | **低**（低 / 低 / 低） | 規則との食い違い | tooling | ○ | ○ | ○ | ○ | run と解析器の実装を結ぶ記録が無い: scan_v2.py は git HEAD しか残さず（docs だけの commit / 未コミットの変更を区別しない）、manifest の fingerprint.sha256 はカタログだけなので D1 の判定が違う実装（672f |
| R5-r2-6 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | 孤立サロゲートを含む文字列定数（"\ud800"）が slot の定数として manifest に入ると、scan_v2.py の utf-8 の書き出しが UnicodeEncodeError で落ち、try の外なので木が analysis_failed になるのではなく r |
| R5-r2-7 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | scan_v2.py は同じ label の再走査で古い木の manifest を消さず（progress.jsonl だけ消す / --resume は標本に無い木を見ない / analysis_failed の木は新しい manifest を書かない）、contradicti |
| R5-r3-2 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | RecursionError で打ち切ったユニットは runner の代替 UnitReport に D_kind が無く（analyze_unit_f0a も parse_d_kind を engine.analyze の後に呼ぶ）、宣言があるのに manifest では D_ |
| R5-r3-3 | **低**（低 / 低 / 低） | 数え落とし | tooling | ○ | ○ | ○ | ○ | compare_scans.py の「消えた CONTRADICTION」は宣言を区別しない集合差なので、同じ (木, ユニット, site, kind) に D3/D4 の矛が残っていれば D1/D2 の矛が消えても（主指標 153 が減っても）「消えた 0」になり、回帰検査を |
| R5-r3-4 | **低**（低 / 低 / 低） | 非決定 | tooling | ○ | ○ | ○ | ○ | unit_id（schema_hash）は仮引数の既定値を ast.unparse した文字列から作るため、既定値が lambda や入れ子引用符の f-string のツールでは Python 3.10 と 3.12 で unit_id が変わる（ast.unparse の出力 |
| R5-r4-1 | **低**（低 / 低 / 低） | 規則との食い違い | tooling | ○ | ○ | ○ | ○ | two_sided.py の事前登録照合 / 座標一致が、片側にしか無いサイト（sink の置換・呼び出し点の追加で修正側にだけ現れた site）を `from: null` の等級変化や任意の座標の「変化」として数える: `SiteRecord.value()` が欠けている側 |

## 落ちた所見（2 観点以上で反証）

| id | 実行 | 設計 | 一般性 | 所見 |
|---|---|---|---|---|
| R2-r1-10 | ○ | ✗ | ✗ | FastMCP が実行時にスキーマから除く `ctx: Context` 仮引数を MODEL として種付けし、ctx 由来の path / argv が主体 MODEL になる（D1 / D2 の理由が *_model_opaque に付き、SELECT 座標では誤警報） |

## 未完（観点が欠けている）

- R1d-r6-2: exec=○, design=—, generality=—
- R1d-r6-3: exec=○, design=—, generality=—
- R3d-r6-1: exec=○, design=○, generality=—
- R3d-r6-2: exec=○, design=—, generality=—

記号: ○ = その観点を生き延びた、✗ = 反証された、— = 未実施。判定の全文は `evidence/review/verify_*.json`、再現は `evidence/review/exec_lens_*.json`、所見の本文は `evidence/review/explore_*.json`。† = 第 5 回（事前登録の上限 4 回の外。review_plan.md §7.3）。
