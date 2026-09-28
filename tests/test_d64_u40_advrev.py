"""D64 / U40 の敵対的レビューの所見（U40-R1〜R6、R8）の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U40 の敵対的レビュー）。** 件数には合わせず、Python の意味
（インスタンス属性がメソッドより先に引かれること、モジュール直下の `locals()` は `globals()` と同じ辞書であること、
クラス本体の名前は LOAD_NAME でクラスの名前空間 → グローバルの順に引かれ、囲む関数のスコープを飛ばすこと、
スクリプトとして動かすと `sys.path[0]` がスクリプトのディレクトリになること）と、D64 の U40 行・
`evidence/review/triage.json` の fix_outline（位置引数 0 は登録文のスコープで厳密に解く。解けないものは採らない。
誤警報は作らない）から導いた。

所見ごとの規則（段階 B の指示）:

- R1: `self.<m>` の上書きの確認で、基底は末尾名でなく `_Resolver.expr` で解く（Subscript は value、import の別名と
  モジュール水準の代入をたどる）。解けない基底を持つ木内クラスが m を束縛していれば採らない。
- R2: `object.__setattr__(self, "m", v)` / `super().__setattr__("m", v)` / `self.__setattr__("m", v)` /
  `self.__dict__["m"] = v` / `vars(self)["m"] = v` も属性 m の書き換えとして数える（採らない）。
- R3: モジュール直下とクラス本体の `locals()` の書き込み、`vars(sys.modules[__name__])` /
  `sys.modules[__name__].__dict__` への書き込みは名前空間の書き換え（解かない）。
- R4: `import pkg.impl; pkg.impl.purge = x`（受け手が Attribute の連鎖）と `setattr(pkg.impl, "purge", x)` も
  `(pkg.impl, purge)` の書き換え。受け手が解けないもの（`sys.modules[...]`、`import_module(...)`）でも属性名が
  一致すれば書き換えとみなす（見過ぎる側）。
- R5: クラス本体で、クラスのローカルな束縛が参照より後にしか無いなら、その名前はグローバルに落ちる
  （囲む関数のスコープは飛ばす）。条件つきの束縛（`if` の中の def）は採らない。
- R6: import する側のファイルと同じディレクトリに `<先頭>.py` / `<先頭>/__init__.py` があり、完全一致の木内
  モジュールと違うなら決めない。
- R8: tools-list のユニットは、呼び出し形のユニットの qualname（名前）ではなく `(module, qualname)` だけで除く。

記号: 「矛」 = 行の注記に `contradiction:<宣言>`。
"""

from __future__ import annotations

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

H = "from mcp.server.fastmcp import FastMCP\nfrom mcp.types import ToolAnnotations\n"

def _manifest(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return manifest_json(res, "t")


def _hits(m, qualname, relpath=None):
    return [
        u
        for u in m["units"]
        if u["unit"]["qualname"] == qualname and (relpath is None or u["unit"]["relpath"] == relpath)
    ]


def _have(m):
    return sorted((u["unit"]["relpath"], u["unit"]["qualname"], u["unit"]["framework"]) for u in m["units"])


def _one(m, qualname, relpath=None):
    hits = _hits(m, qualname, relpath)
    where = f"{relpath}:{qualname}" if relpath else qualname
    assert hits, f"{where} がユニットにならない: {_have(m)}"
    assert len(hits) == 1, f"{where} が {len(hits)} ユニット: {_have(m)}"
    return hits[0]


def _contra(u, decl="D1"):
    return any(n == f"contradiction:{decl}" for r in u["rows"] for n in r.get("notes", []))


def _any_contra(m):
    return any(
        "CONTRADICTION" in r.get("verdicts", []) or any(n.startswith("contradiction:") for n in r.get("notes", []))
        for u in m["units"]
        for r in u["rows"]
    )


# ---------------------------------------------------------------------------
# U40-R1: self.<m> の上書きの確認で、基底を末尾名で結ばない
# ---------------------------------------------------------------------------

#: 登録する側（s.py）。handle は書き込まない。サブクラスが handle を書き込みありで上書きする。
SERVER_NOOP = H + '''

class Server:
    def __init__(self):
        self.mcp = FastMCP("t")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.handle)

    def handle(self, path: str) -> str:
        return "noop"
'''

#: 登録する側（s.py）。handle が書き込む（上書きが無ければ readOnlyHint に対する D1 の矛）。
SERVER_WRITE = H + '''

class Server:
    def __init__(self):
        self.mcp = FastMCP("t")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.handle)

    def handle(self, path: str) -> str:
        with open(path, "w") as fh:
            fh.write("x")
        return "ok"
'''


def _override(header: str, cls_line: str) -> str:
    return (
        header
        + "\n\n"
        + cls_line
        + '''
    def handle(self, path: str) -> str:
        with open(path, "w") as fh:
            fh.write("x")
        return "ok"
'''
    )


def test_r1_aliased_import_base_override_not_taken(tmp_path_factory):
    """t/cA: `from s import Server as BaseServer; class FileServer(BaseServer)` が handle を上書きする。
    FileServer のインスタンスでは self.handle は書き込む方なので、s.py の Server.handle を readOnly の
    矛なしユニットにしない（規則: 木内のサブクラスが m を束縛する → 採らない）。"""
    m = _manifest(
        tmp_path_factory,
        "r1_alias",
        {
            "s.py": SERVER_NOOP,
            "impl.py": _override("from s import Server as BaseServer", "class FileServer(BaseServer):")
            + "\n\napp = FileServer()\n",
        },
    )
    assert not _hits(m, "Server.handle"), _have(m)


def test_r1_module_assignment_alias_base_not_taken(tmp_path_factory):
    """t/cA2: `import s; Base = s.Server; class FileServer(Base)`（モジュール水準の代入の別名）。"""
    m = _manifest(
        tmp_path_factory,
        "r1_assign",
        {"s.py": SERVER_NOOP, "impl.py": _override("import s\n\nBase = s.Server", "class FileServer(Base):")},
    )
    assert not _hits(m, "Server.handle"), _have(m)


def test_r1_subscript_base_not_taken(tmp_path_factory):
    """t/cB: `class Server(Generic[T])` と `class FileServer(Server[str])`（Subscript の基底は value を見る）。"""
    src = (
        "from typing import Generic, TypeVar\n"
        + SERVER_NOOP.replace("class Server:", 'T = TypeVar("T")\n\n\nclass Server(Generic[T]):')
        + _override("", "class FileServer(Server[str]):")
        + "\n\napp = FileServer()\n"
    )
    m = _manifest(tmp_path_factory, "r1_subscript", {"s.py": src})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r1_unresolvable_base_binding_attr_not_taken(tmp_path_factory):
    """解けない基底（呼び出し式）を持つ木内クラスが handle を束縛する → 見過ぎる側に倒して採らない。"""
    m = _manifest(
        tmp_path_factory,
        "r1_call_base",
        {
            "s.py": SERVER_NOOP,
            "impl.py": _override(
                "import s\n\n\ndef make_base():\n    return s.Server", "class FileServer(make_base()):"
            ),
        },
    )
    assert not _hits(m, "Server.handle"), _have(m)


def test_r1_unresolvable_base_intermediate_not_taken(tmp_path_factory):
    """解けない基底を持つ中間クラス Mid（handle を束縛しない）の下の Leaf が handle を束縛する → 採らない。"""
    src = (
        "import s\n\n\ndef make_base():\n    return s.Server\n\n\nclass Mid(make_base()):\n    pass\n"
    )
    m = _manifest(
        tmp_path_factory,
        "r1_mid",
        {"s.py": SERVER_NOOP, "impl.py": _override(src, "class Leaf(Mid):")},
    )
    assert not _hits(m, "Server.handle"), _have(m)


def test_r1_control_no_subclass_is_unit_with_contradiction(tmp_path_factory):
    """対照: サブクラスが無ければ self.handle は Server.handle（書き込みあり）→ ユニットで D1 の矛。"""
    m = _manifest(tmp_path_factory, "r1_ctl_none", {"s.py": SERVER_WRITE})
    u = _one(m, "Server.handle", "s.py")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u)


def test_r1_control_generic_base_without_subclass_is_unit(tmp_path_factory):
    """対照: Server 自身の基底が `Generic[T]`（木外）でも、サブクラスが無ければユニットで D1 の矛。"""
    src = "from typing import Generic, TypeVar\n" + SERVER_WRITE.replace(
        "class Server:", 'T = TypeVar("T")\n\n\nclass Server(Generic[T]):'
    )
    m = _manifest(tmp_path_factory, "r1_ctl_generic", {"s.py": src})
    assert _contra(_one(m, "Server.handle", "s.py"))


def test_r1_control_aliased_subclass_without_override_is_unit(tmp_path_factory):
    """対照: 別名の基底のサブクラスが handle を上書きしなければ、Server.handle のまま（D1 の矛）。"""
    m = _manifest(
        tmp_path_factory,
        "r1_ctl_nooverride",
        {
            "s.py": SERVER_WRITE,
            "impl.py": "from s import Server as BaseServer\n\n\nclass FileServer(BaseServer):\n"
            "    def other(self) -> str:\n        return 'x'\n",
        },
    )
    assert _contra(_one(m, "Server.handle", "s.py"))


def test_r1_control_unrelated_class_binding_attr_is_unit(tmp_path_factory):
    """対照: 基底が解けて Server と無関係なクラス（`class Other(dict)`）が handle を束縛しても、Server.handle のまま。"""
    m = _manifest(
        tmp_path_factory,
        "r1_ctl_unrelated",
        {
            "s.py": SERVER_WRITE,
            "other.py": "class Other(dict):\n    def handle(self, path: str) -> str:\n        return 'noop'\n",
        },
    )
    assert _contra(_one(m, "Server.handle", "s.py"))


# ---------------------------------------------------------------------------
# U40-R2: __setattr__ / __dict__ / vars(self) によるインスタンス属性での隠蔽
# ---------------------------------------------------------------------------


def _shadow_server(stmt: str) -> str:
    return (
        H
        + '''

def write_file(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("x")
    return "ok"


class Base:
    pass


class Server(Base):
    def __init__(self, writable: bool = True, name: str = "handle"):
        if writable:
            '''
        + stmt
        + '''
        self.mcp = FastMCP("t")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.handle)

    def handle(self, path: str) -> str:
        return "noop"
'''
    )


def test_r2_object_setattr_not_taken(tmp_path_factory):
    """t/cQ: `object.__setattr__(self, "handle", write_file)` → self.handle は write_file。採らない。"""
    m = _manifest(tmp_path_factory, "r2_obj", {"s.py": _shadow_server('object.__setattr__(self, "handle", write_file)')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_super_setattr_not_taken(tmp_path_factory):
    """t/cQ2: `super().__setattr__("handle", write_file)`。"""
    m = _manifest(tmp_path_factory, "r2_super", {"s.py": _shadow_server('super().__setattr__("handle", write_file)')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_bound_dunder_setattr_not_taken(tmp_path_factory):
    """束縛メソッド形 `self.__setattr__("handle", write_file)`。"""
    m = _manifest(tmp_path_factory, "r2_bound", {"s.py": _shadow_server('self.__setattr__("handle", write_file)')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_instance_dict_write_not_taken(tmp_path_factory):
    """`self.__dict__["handle"] = write_file`（インスタンス辞書への直接の書き込み）。"""
    m = _manifest(tmp_path_factory, "r2_dict", {"s.py": _shadow_server('self.__dict__["handle"] = write_file')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_vars_self_write_not_taken(tmp_path_factory):
    """`vars(self)["handle"] = write_file`。"""
    m = _manifest(tmp_path_factory, "r2_vars", {"s.py": _shadow_server('vars(self)["handle"] = write_file')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_nonconstant_dunder_setattr_not_taken(tmp_path_factory):
    """名前が定数でない `object.__setattr__(self, name, write_file)`（どの属性でもありうる）。"""
    m = _manifest(tmp_path_factory, "r2_nonconst", {"s.py": _shadow_server("object.__setattr__(self, name, write_file)")})
    assert not _hits(m, "Server.handle"), _have(m)


def test_r2_control_other_attr_setattr_is_unit(tmp_path_factory):
    """対照: 別の属性名への `object.__setattr__(self, "other", 1)` は handle を隠さない（handle が書き込めば D1 の矛）。"""
    src = _shadow_server('object.__setattr__(self, "other", 1)').replace(
        '    def handle(self, path: str) -> str:\n        return "noop"\n',
        '    def handle(self, path: str) -> str:\n        return write_file(path)\n',
    )
    m = _manifest(tmp_path_factory, "r2_ctl", {"s.py": src})
    u = _one(m, "Server.handle", "s.py")
    assert _contra(u)


# ---------------------------------------------------------------------------
# U40-R3: locals() / sys.modules 経由の名前空間の書き換え
# ---------------------------------------------------------------------------


def _ns_module(stmt: str, pre: str = "") -> str:
    return (
        pre
        + H
        + '''
mcp = FastMCP("t")


def fetch(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("x")
    return "ok"


def dry_fetch(path: str) -> str:
    return "noop"


'''
        + stmt
        + '''
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(fetch)
'''
    )


def test_r3_module_locals_write_not_resolved(tmp_path_factory):
    """t/cH: モジュール直下の `locals()["fetch"] = dry_fetch` は globals() と同じ辞書への書き込み。
    登録されるのは dry_fetch（書き込みなし）なので、fetch を readOnly の矛にしない。"""
    m = _manifest(tmp_path_factory, "r3_locals", {"s.py": _ns_module('locals()["fetch"] = dry_fetch')})
    assert not _hits(m, "fetch"), _have(m)
    assert not _any_contra(m)


def test_r3_vars_sys_modules_write_not_resolved(tmp_path_factory):
    """`vars(sys.modules[__name__])["fetch"] = dry_fetch`。"""
    m = _manifest(
        tmp_path_factory,
        "r3_vars_mod",
        {"s.py": _ns_module('vars(sys.modules[__name__])["fetch"] = dry_fetch', "import sys\n")},
    )
    assert not _hits(m, "fetch"), _have(m)
    assert not _any_contra(m)


def test_r3_sys_modules_dict_write_not_resolved(tmp_path_factory):
    """`sys.modules[__name__].__dict__["fetch"] = dry_fetch`。"""
    m = _manifest(
        tmp_path_factory,
        "r3_mod_dict",
        {"s.py": _ns_module('sys.modules[__name__].__dict__["fetch"] = dry_fetch', "import sys\n")},
    )
    assert not _hits(m, "fetch"), _have(m)
    assert not _any_contra(m)


def test_r3_class_body_locals_write_not_taken(tmp_path_factory):
    """クラス本体の `locals()["handle"] = write_file`（def の後）はクラス属性 handle を書き換える。
    self.handle は write_file なので、K.handle を readOnly の矛なしユニットにしない。"""
    src = (
        H
        + '''

def write_file(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("x")
    return "ok"


class K:
    def __init__(self):
        self.mcp = FastMCP("t")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.handle)

    def handle(self, path: str) -> str:
        return "noop"

    locals()["handle"] = write_file
'''
    )
    m = _manifest(tmp_path_factory, "r3_cls_locals", {"s.py": src})
    assert not _hits(m, "K.handle"), _have(m)


def test_r3_control_function_locals_does_not_block(tmp_path_factory):
    """対照: 関数の中の `locals()`（書き込みは関数のローカルにも伝わらない）はモジュールの名前を書き換えない。
    fetch はユニットのままで D1 の矛。"""
    src = _ns_module('def helper(x):\n    locals()["fetch"] = x\n    return dict(locals())\n')
    m = _manifest(tmp_path_factory, "r3_ctl", {"s.py": src})
    assert _contra(_one(m, "fetch", "s.py"))


# ---------------------------------------------------------------------------
# U40-R4: 連鎖形・解けない受け手によるモジュール属性の書き換え
# ---------------------------------------------------------------------------

PKG_IMPL = '''def purge(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("")
    return "purged"
'''

S_PURGE = (
    "import patch  # noqa: F401\n"
    + H
    + '''from pkg.impl import purge

mcp = FastMCP("t")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(purge)
'''
)


def _patch_tree(tmp_path_factory, name, patch_src):
    return _manifest(
        tmp_path_factory,
        name,
        {"pkg/__init__.py": "", "pkg/impl.py": PKG_IMPL, "patch.py": patch_src, "s.py": S_PURGE},
    )


DRY = '''

def dry_purge(path: str) -> str:
    return "would purge " + path


'''


def test_r4_chained_module_attr_write_not_resolved(tmp_path_factory):
    """t/cE: `import pkg.impl; pkg.impl.purge = dry_purge` → 登録されるのは dry_purge。矛にしない。"""
    m = _patch_tree(tmp_path_factory, "r4_chain", "import pkg.impl" + DRY + "pkg.impl.purge = dry_purge\n")
    assert not _hits(m, "purge", "pkg/impl.py"), _have(m)
    assert not _any_contra(m)


def test_r4_chained_setattr_not_resolved(tmp_path_factory):
    """`setattr(pkg.impl, "purge", dry_purge)`（受け手が Attribute の連鎖）。"""
    m = _patch_tree(tmp_path_factory, "r4_setattr", "import pkg.impl" + DRY + 'setattr(pkg.impl, "purge", dry_purge)\n')
    assert not _hits(m, "purge", "pkg/impl.py"), _have(m)
    assert not _any_contra(m)


def test_r4_sys_modules_receiver_not_resolved(tmp_path_factory):
    """`sys.modules["pkg.impl"].purge = dry_purge`（受け手が解けない → 属性名の一致で書き換えとみなす）。"""
    m = _patch_tree(tmp_path_factory, "r4_sysmod", "import sys" + DRY + 'sys.modules["pkg.impl"].purge = dry_purge\n')
    assert not _hits(m, "purge", "pkg/impl.py"), _have(m)
    assert not _any_contra(m)


def test_r4_import_module_receiver_not_resolved(tmp_path_factory):
    """`importlib.import_module("pkg.impl").purge = dry_purge`。"""
    m = _patch_tree(
        tmp_path_factory,
        "r4_importlib",
        "import importlib" + DRY + 'importlib.import_module("pkg.impl").purge = dry_purge\n',
    )
    assert not _hits(m, "purge", "pkg/impl.py"), _have(m)
    assert not _any_contra(m)


def test_r4_control_alias_form_still_not_resolved(tmp_path_factory):
    """対照（t/cE2、変えない）: `import pkg.impl as m; m.purge = dry_purge` は採らない。"""
    m = _patch_tree(tmp_path_factory, "r4_ctl_alias", "import pkg.impl as m" + DRY + "m.purge = dry_purge\n")
    assert not _hits(m, "purge", "pkg/impl.py"), _have(m)
    assert not _any_contra(m)


def test_r4_control_other_attr_is_unit(tmp_path_factory):
    """対照: 別の属性名 `pkg.impl.other = 1` と、インスタンス属性 `self.purge = ...` は purge を書き換えない。"""
    patch_src = (
        "import pkg.impl\n\npkg.impl.other = 1\n\n\nclass Holder:\n"
        "    def __init__(self, fn):\n        self.purge = fn\n"
    )
    m = _patch_tree(tmp_path_factory, "r4_ctl_other", patch_src)
    u = _one(m, "purge", "pkg/impl.py")
    assert _contra(u)


# ---------------------------------------------------------------------------
# U40-R5: クラス本体の前方参照（LOAD_NAME）
# ---------------------------------------------------------------------------

FETCH_WRITE = '''def fetch(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("")
    return "ok"
'''


def test_r5_class_body_forward_reference_falls_to_global(tmp_path_factory):
    """t/cF: 登録の文がクラスのローカルな def より前 → 名前はグローバルの fetch（書き込みあり）に落ちる。
    Tools.fetch を矛なしユニットにせず、モジュールの fetch が readOnly に対する D1 の矛になる。"""
    src = (
        H
        + '\nmcp = FastMCP("t")\n\n\n'
        + FETCH_WRITE
        + '''

class Tools:
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(fetch)

    def fetch(self, path: str) -> str:
        return "noop"
'''
    )
    m = _manifest(tmp_path_factory, "r5_fwd", {"s.py": src})
    assert not _hits(m, "Tools.fetch"), _have(m)
    assert _contra(_one(m, "fetch", "s.py"))


def test_r5_class_in_function_skips_enclosing_scope(tmp_path_factory):
    """クラス本体でローカルな名前（後で束縛される）は LOAD_NAME で囲む関数を飛ばしてグローバルへ落ちる。
    登録されるのはモジュールの fetch（書き込みなし）で、囲む関数の fetch（書き込みあり）ではない。矛は無い。"""
    src = (
        H
        + '''
mcp = FastMCP("t")


def fetch(path: str) -> str:
    return "noop"


def build():
    def fetch(path: str) -> str:
        with open(path, "w") as fh:
            fh.write("")
        return "ok"

    class Tools:
        mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(fetch)

        def fetch(self, path: str) -> str:
            return "noop"

    return Tools
'''
    )
    m = _manifest(tmp_path_factory, "r5_nested", {"s.py": src})
    assert not _hits(m, "build.fetch"), _have(m)
    assert not _hits(m, "build.Tools.fetch"), _have(m)
    assert not _any_contra(m)


def test_r5_conditional_class_binding_not_taken(tmp_path_factory):
    """クラス本体の `if` の中の def は、条件しだいで束縛されない（そのときはグローバルの fetch）。
    Tools.fetch を readOnly の矛なしユニットにしない。"""
    src = (
        H
        + '\nimport os\n\nmcp = FastMCP("t")\n\n\n'
        + FETCH_WRITE
        + '''

class Tools:
    if os.environ.get("DRY"):
        def fetch(self, path: str) -> str:
            return "noop"

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(fetch)
'''
    )
    m = _manifest(tmp_path_factory, "r5_cond", {"s.py": src})
    assert not _hits(m, "Tools.fetch"), _have(m)


def test_r5_control_class_def_before_reference_is_unit(tmp_path_factory):
    """対照: クラス本体の def が登録の文より前にあれば、その def（書き込みあり）がユニットで D1 の矛。"""
    src = (
        H
        + '''
mcp = FastMCP("t")


def fetch(path: str) -> str:
    return "noop"


class Tools:
    def fetch(path: str) -> str:
        with open(path, "w") as fh:
            fh.write("")
        return "ok"

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(fetch)
'''
    )
    m = _manifest(tmp_path_factory, "r5_ctl", {"s.py": src})
    assert _contra(_one(m, "Tools.fetch", "s.py"))
    assert not _hits(m, "fetch", "s.py"), _have(m)


# ---------------------------------------------------------------------------
# U40-R6: スクリプトの兄弟モジュールと完全一致の木内モジュール
# ---------------------------------------------------------------------------

ROOT_TOOLS = '''def cleanup(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("")
    return "cleared"
'''

SIB_TOOLS = '''def cleanup(path: str) -> str:
    return "would clear " + path
'''

APP = (
    H
    + '''from tools import cleanup

mcp = FastMCP("demo")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(cleanup)

if __name__ == "__main__":
    mcp.run()
'''
)


def test_r6_sibling_module_not_resolved_to_root(tmp_path_factory):
    """t/cS: examples/demo/app.py の `from tools import cleanup` は、スクリプトとして動かせば兄弟の
    examples/demo/tools.py（書き込みなし）。根の tools.py に宣言を付けない（決めない）。"""
    m = _manifest(
        tmp_path_factory,
        "r6_sib",
        {"tools.py": ROOT_TOOLS, "examples/demo/tools.py": SIB_TOOLS, "examples/demo/app.py": APP},
    )
    assert not _hits(m, "cleanup", "tools.py"), _have(m)
    assert not _any_contra(m)


def test_r6_sibling_package_not_resolved_to_root(tmp_path_factory):
    """兄弟がパッケージ（examples/demo/tools/__init__.py）でも同じ。"""
    m = _manifest(
        tmp_path_factory,
        "r6_sibpkg",
        {"tools.py": ROOT_TOOLS, "examples/demo/tools/__init__.py": SIB_TOOLS, "examples/demo/app.py": APP},
    )
    assert not _hits(m, "cleanup", "tools.py"), _have(m)
    assert not _any_contra(m)


def test_r6_control_importer_at_root_is_unit(tmp_path_factory):
    """対照: import する側が根にあれば、兄弟は完全一致の tools.py そのもの → ユニットで D1 の矛。"""
    m = _manifest(
        tmp_path_factory,
        "r6_ctl_root",
        {"tools.py": ROOT_TOOLS, "examples/demo/tools.py": SIB_TOOLS, "app.py": APP},
    )
    assert _contra(_one(m, "cleanup", "tools.py"))


def test_r6_control_no_sibling_is_unit(tmp_path_factory):
    """対照: 兄弟が無ければ、完全一致の根の tools.py に解く（従来どおり、D1 の矛）。"""
    m = _manifest(
        tmp_path_factory,
        "r6_ctl_nosib",
        {"tools.py": ROOT_TOOLS, "examples/demo/app.py": APP},
    )
    assert _contra(_one(m, "cleanup", "tools.py"))


# ---------------------------------------------------------------------------
# U40-R8: 呼び出し形のユニットの名前で tools-list の別関数を消さない
# ---------------------------------------------------------------------------


def test_r8_same_name_other_module_tools_list_kept(tmp_path_factory):
    """t/cD: srv.py の `mcp.add_tool(search)` と、agent.py の無関係な `search`（tools=[search]）。
    agent.py:search は tools-list のユニットのまま残る（書き込みの行がある）。"""
    m = _manifest(
        tmp_path_factory,
        "r8",
        {
            "srv.py": 'from mcp.server.fastmcp import FastMCP\n\nmcp = FastMCP("t")\n\n\n'
            "def search(query: str) -> str:\n    return query.upper()\n\n\nmcp.add_tool(search)\n",
            "agent.py": "from agents import Agent\n\n\ndef search(path: str) -> str:\n"
            '    with open(path, "w") as fh:\n        fh.write("x")\n    return "ok"\n\n\n'
            'agent = Agent(name="a", tools=[search])\n',
        },
    )
    s = _one(m, "search", "srv.py")
    assert s["unit"]["framework"] == "mcp"
    a = _one(m, "search", "agent.py")
    assert a["unit"]["framework"] == "tools-list"
    assert a["rows"], a


def test_r8_control_same_function_registered_twice_is_one_unit(tmp_path_factory):
    """対照: 同じ関数を add_tool と tools=[...] の両方に並べても 1 ユニット（(module, qualname) で除く）。"""
    m = _manifest(
        tmp_path_factory,
        "r8_ctl",
        {
            "srv.py": "from agents import Agent\nfrom mcp.server.fastmcp import FastMCP\n\n"
            'mcp = FastMCP("t")\n\n\ndef search(path: str) -> str:\n'
            '    with open(path, "w") as fh:\n        fh.write("x")\n    return "ok"\n\n\n'
            'mcp.add_tool(search)\nagent = Agent(name="a", tools=[search])\n',
        },
    )
    u = _one(m, "search", "srv.py")
    assert u["unit"]["framework"] == "mcp"
