"""D64 / U40 の 3 巡目（最後）: 2 巡目の直しの再点検の所見（U40-RC1〜RC4）の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U40 の 3 巡目）。** 件数には合わせず、Python の意味（MRO で
サブクラスの基底はその基底の基底より前に来ること、インスタンス属性がメソッドより先に引かれること、スクリプト
として動かすと `sys.path[0]` がスクリプトのディレクトリになり、名前空間パッケージの部分は `sys.path` の順に
並ぶこと）と、再点検のスタブ実行（`d64recheck/U40/n/`）で確かめた登録される関数から導いた。

所見ごとの規則（段階 B の 3 巡目の指示）:

- RC1: `self.<m>` の上書きの確認で、確かなサブクラスか、そこから `cls` を通らずにたどれる基底が**解けない基底**を
  持つなら、その基底が m を束縛しうるとして採らない。確かなサブクラスの外にある、解けない基底を持つクラスで
  `self.m` の解決をすべて失わない（対照）。
- RC2: 木外（extern）と判定した基底の dotted 名の末尾が、木内のクラス名（対象のクラス・サブクラス・m を束縛する
  クラス）と一致するなら、解けない基底として扱う（走査の根がパッケージそのもので `from proj.s import Server`）。
- RC3: import する側と同じディレクトリの `<先頭>/`（`__init__.py` の無い名前空間パッケージ）の下に残りの dotted の
  ファイルがあれば兄弟とみなし、根のモジュールと違えば決めない。
- RC4: `X.__dict__ |= {...}` / `X.__dict__ = {...}`（`__dict__` そのものへの Store / AugAssign）は属性の書き換え。
  右辺が定数キーの dict ならそのキーの、そうでなければどの名前でもありうる書き換え。

記号: 「矛」 = 行の注記に `contradiction:<宣言>`。
"""

from __future__ import annotations

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

H = "from mcp.server.fastmcp import FastMCP\nfrom mcp.types import ToolAnnotations\n"


def _manifest(tmp_path_factory, name, files, root=""):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d / root) if root else str(d), population="mcp_server", full=True))
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


def _no_clean(m, qualname, relpath=None):
    """`qualname` を矛なしのユニットにしない（採らないか、採るなら D1 の矛）。"""
    for u in _hits(m, qualname, relpath):
        assert _contra(u), f"{qualname} が矛なしのユニット（誤 clear）: {_have(m)}"


#: 登録する側（s.py）。handle は書き込まない。
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

WRITE_MIXIN = '''class WriteMixin:
    def handle(self, path: str) -> str:
        with open(path, "w") as fh:
            fh.write("x")
        return "ok"
'''


# ---------------------------------------------------------------------------
# U40-RC1: 確かなサブクラスの解けない基底（ミックスイン）
# ---------------------------------------------------------------------------


def test_rc1_try_except_mixin_in_definite_subclass(tmp_path_factory):
    """n/m1: `try: from mixins import WriteMixin / except ImportError: from pkg.mixins import WriteMixin` の
    ミックスインを持つ確かなサブクラス `FileServer(WriteMixin, Server)`。MRO で WriteMixin が Server より前なので
    登録されるのは書き込む handle（スタブ実行で `registered WriteMixin.handle mixins`）。Server.handle を
    矛なしのユニットにしない。"""
    impl = (
        "try:\n    from mixins import WriteMixin\nexcept ImportError:\n    from pkg.mixins import WriteMixin\n"
        "from s import Server\n\n\nclass FileServer(WriteMixin, Server):\n    pass\n\n\napp = FileServer()\n"
    )
    m = _manifest(
        tmp_path_factory,
        "rc1_try",
        {
            "s.py": SERVER_NOOP,
            "mixins.py": WRITE_MIXIN,
            "pkg/__init__.py": "",
            "pkg/mixins.py": WRITE_MIXIN,
            "impl.py": impl,
        },
    )
    _no_clean(m, "Server.handle")


def test_rc1_call_expression_mixin_in_definite_subclass(tmp_path_factory):
    """n/m1c: `class FileServer(pick(), Server)`（pick() は mixins.WriteMixin を返す）。"""
    impl = (
        "import mixins\nfrom s import Server\n\n\ndef pick():\n    return mixins.WriteMixin\n\n\n"
        "class FileServer(pick(), Server):\n    pass\n"
    )
    m = _manifest(
        tmp_path_factory,
        "rc1_call",
        {"s.py": SERVER_NOOP, "mixins.py": WRITE_MIXIN, "impl.py": impl},
    )
    _no_clean(m, "Server.handle")


def test_rc1_mixin_reachable_from_subclass_has_unknown_base(tmp_path_factory):
    """確かなサブクラスからたどれる基底 `Mixin`（handle を束縛しない）の基底が解けない（呼び出し式）。
    その基底は WriteMixin で、MRO で Server より前に来る。"""
    impl = (
        "import mixins\nfrom s import Server\n\n\ndef pick():\n    return mixins.WriteMixin\n\n\n"
        "class Mixin(pick()):\n    pass\n\n\nclass FileServer(Mixin, Server):\n    pass\n"
    )
    m = _manifest(
        tmp_path_factory,
        "rc1_reach",
        {"s.py": SERVER_NOOP, "mixins.py": WRITE_MIXIN, "impl.py": impl},
    )
    _no_clean(m, "Server.handle")


def test_rc1_control_unrelated_unknown_base_class_keeps_unit(tmp_path_factory):
    """対照: サブクラスの外にある、解けない基底を持つクラス（handle を束縛しない）で self.handle の解決を
    失わない → Server.handle（書き込みあり）はユニットで D1 の矛。"""
    other = "def make():\n    return dict\n\n\nclass Other(make()):\n    pass\n"
    m = _manifest(tmp_path_factory, "rc1_ctl_other", {"s.py": SERVER_WRITE, "other.py": other})
    assert _contra(_one(m, "Server.handle", "s.py"))


def test_rc1_control_definite_subclass_resolved_bases_keeps_unit(tmp_path_factory):
    """対照: 確かなサブクラスの基底がすべて解けて handle を束縛しない（木内のミックスインが別名のメソッドだけ）。
    別の所に解けない基底を持つクラスがあっても、Server.handle はユニットで D1 の矛。"""
    impl = (
        "from s import Server\n\n\nclass LogMixin:\n    def log(self) -> str:\n        return 'x'\n\n\n"
        "class FileServer(LogMixin, Server):\n    pass\n\n\n"
        "def make():\n    return dict\n\n\nclass Other(make()):\n    pass\n"
    )
    m = _manifest(tmp_path_factory, "rc1_ctl_sub", {"s.py": SERVER_WRITE, "impl.py": impl})
    assert _contra(_one(m, "Server.handle", "s.py"))


# ---------------------------------------------------------------------------
# U40-RC2: 走査の根がパッケージそのもの（extern に落ちた基底の末尾名）
# ---------------------------------------------------------------------------


def test_rc2_root_is_package_imported_by_own_name(tmp_path_factory):
    """n/e1/proj: 走査の根が proj/ そのもの。impl.py の `from proj.s import Server; class FileServer(Server)`
    が handle を書き込みありで上書きする（スタブ実行で `registered FileServer.handle proj.impl`）。
    Server.handle を矛なしのユニットにしない。"""
    impl = (
        "from proj.s import Server\n\n\nclass FileServer(Server):\n"
        "    def handle(self, path: str) -> str:\n        with open(path, \"w\") as fh:\n"
        "            fh.write(\"x\")\n        return \"ok\"\n"
    )
    m = _manifest(
        tmp_path_factory,
        "rc2_pkgroot",
        {"proj/__init__.py": "", "proj/s.py": SERVER_NOOP, "proj/impl.py": impl},
        root="proj",
    )
    _no_clean(m, "Server.handle")


def test_rc2_control_extern_base_other_tail_keeps_unit(tmp_path_factory):
    """対照: 木外の基底の末尾名（Helper）が木内のどのクラス名とも一致しなければ、木外のまま。
    FileServer は Server のサブクラスではないので、Server.handle（書き込みあり）はユニットで D1 の矛。"""
    other = (
        "from somelib.base import Helper\n\n\nclass FileServer(Helper):\n"
        "    def handle(self, path: str) -> str:\n        return 'noop'\n"
    )
    m = _manifest(tmp_path_factory, "rc2_ctl", {"s.py": SERVER_WRITE, "other.py": other})
    assert _contra(_one(m, "Server.handle", "s.py"))


# ---------------------------------------------------------------------------
# U40-RC3: 名前空間パッケージの兄弟
# ---------------------------------------------------------------------------

ROOT_CLEANUP = '''def cleanup(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("")
    return "ok"
'''

SIB_CLEANUP = '''def cleanup(path: str) -> str:
    return "would clear"
'''

APP = (
    H
    + '''from tools.cleanup import cleanup

mcp = FastMCP("demo")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(cleanup)

if __name__ == "__main__":
    mcp.run()
'''
)


def test_rc3_namespace_package_sibling_not_resolved_to_root(tmp_path_factory):
    """n/m2: examples/demo/app.py の `from tools.cleanup import cleanup`。スクリプトとして動かすと
    `tools.cleanup.__file__` は examples/demo/tools/cleanup.py（書き込みなし。実行で確認済み）。
    根の tools/cleanup.py に宣言を付けない（決めない）。"""
    m = _manifest(
        tmp_path_factory,
        "rc3_ns",
        {
            "tools/cleanup.py": ROOT_CLEANUP,
            "examples/demo/tools/cleanup.py": SIB_CLEANUP,
            "examples/demo/app.py": APP,
        },
    )
    assert not _hits(m, "cleanup", "tools/cleanup.py"), _have(m)
    assert not _any_contra(m)


def test_rc3_control_importer_at_root_is_unit(tmp_path_factory):
    """対照: import する側が根にあれば、名前空間の兄弟は根の tools/cleanup.py そのもの → ユニットで D1 の矛。"""
    m = _manifest(
        tmp_path_factory,
        "rc3_ctl_root",
        {"tools/cleanup.py": ROOT_CLEANUP, "examples/demo/tools/cleanup.py": SIB_CLEANUP, "app.py": APP},
    )
    assert _contra(_one(m, "cleanup", "tools/cleanup.py"))


def test_rc3_control_namespace_sibling_without_module_is_unit(tmp_path_factory):
    """対照: 兄弟の examples/demo/tools/ はあるが cleanup.py が無い → `tools.cleanup` は根の方に当たる
    （名前空間パッケージの部分を順に探す）。ユニットで D1 の矛。"""
    m = _manifest(
        tmp_path_factory,
        "rc3_ctl_nomod",
        {"tools/cleanup.py": ROOT_CLEANUP, "examples/demo/tools/other.py": SIB_CLEANUP, "examples/demo/app.py": APP},
    )
    assert _contra(_one(m, "cleanup", "tools/cleanup.py"))


# ---------------------------------------------------------------------------
# U40-RC4: `__dict__` そのものへの Store / AugAssign
# ---------------------------------------------------------------------------


def _dict_server(stmt: str, handle_body: str = 'return "noop"') -> str:
    return (
        H
        + '''

def write_file(path: str) -> str:
    with open(path, "w") as fh:
        fh.write("x")
    return "ok"


class Server:
    def __init__(self, writable: bool = True, extra: dict = {}):
        if writable:
            '''
        + stmt
        + '''
        self.mcp = FastMCP("t")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.handle)

    def handle(self, path: str) -> str:
        '''
        + handle_body
        + "\n"
    )


def test_rc4_dict_ior_constant_key_not_taken(tmp_path_factory):
    """n/m3: `self.__dict__ |= {"handle": write_file}` → self.handle は write_file（スタブ実行で
    `registered write_file s`）。Server.handle を採らない。"""
    m = _manifest(tmp_path_factory, "rc4_ior", {"s.py": _dict_server('self.__dict__ |= {"handle": write_file}')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_rc4_dict_assign_constant_key_not_taken(tmp_path_factory):
    """`self.__dict__ = {"handle": write_file}`（インスタンス辞書の置き換え）。"""
    m = _manifest(tmp_path_factory, "rc4_assign", {"s.py": _dict_server('self.__dict__ = {"handle": write_file}')})
    assert not _hits(m, "Server.handle"), _have(m)


def test_rc4_dict_ior_nonconstant_not_taken(tmp_path_factory):
    """`self.__dict__ |= extra`（どの名前でもありうる）。"""
    m = _manifest(tmp_path_factory, "rc4_nonconst", {"s.py": _dict_server("self.__dict__ |= extra")})
    assert not _hits(m, "Server.handle"), _have(m)


def test_rc4_control_dict_ior_other_key_is_unit(tmp_path_factory):
    """対照: 別の名前だけの `self.__dict__ |= {"other": 1}` は handle を隠さない（handle が書き込めば D1 の矛）。"""
    src = _dict_server('self.__dict__ |= {"other": 1}', handle_body="return write_file(path)")
    m = _manifest(tmp_path_factory, "rc4_ctl", {"s.py": src})
    assert _contra(_one(m, "Server.handle", "s.py"))
