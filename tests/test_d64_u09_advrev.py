"""D64 / U09 の敵対的レビュー（所見 U09-A1〜A5）の反例と対照。

**期待値は authgap/ を直す前に書いた（D64 / U09 の敵対的レビュー）。** 観測はレビューの再現の木
（scratchpad/d64review/U09/ の t1, t3, t4, t6, t6b, t9, t10, t7, t11）を最小にしたもので、期待値は所見の expected
（Python の import・スコープ・MRO の意味）と、D17 改訂 2（木の中で再束縛される名前は定数として読まない）・
D64 の U09 行・`evidence/review/triage.json` の U09 fix_outline（条件 (i)〜(v)、規則 B）から導いた。
v2 / v3 の件数には合わせていない。

- U09-A1: 点つきの連鎖での書き込み `pkg.config.MODE = v` は pkg.config.MODE の再束縛（D17 改訂 2）。
- U09-A2: `from pkg import *` で来た `config` はパッケージの名前空間にある pkg.config のモジュールオブジェクト。
- U09-A3: `__init__.py` が `from . import config as settings` と再公開した `settings` は pkg.config そのもの。
- U09-A4: 入れ子関数から見た名前は、外側の関数の束縛（局所の import・class・def）が先に効く（LEGB）。
- U09-A5: `class C(A, B)` のクラス属性は MRO の左（A）が勝つ。多重継承で定義するクラスが 2 つ以上なら、
  MRO を実装しない限り型を付けない（不の側に倒す）。

- `test_fix_*`: 直す前の解析器で**落ちる**（所見の expected）。
- `test_keep_*`: 直した後も壊してはいけない対照（所見の対照・could_not_break の形・今正しく読めている形）。

観測は manifest の効果行（kind / slots / fs_mode / destructive / http_method）と行の注記
（`contradiction:*` / `contradiction_reason:*` / `contradiction_unknown:*`）だけで行う。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _units(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u: dict, kind: str) -> list[dict]:
    return [e for e in u["effects"] if e["kind"] == kind]


def _slot(e: dict, name: str) -> dict:
    return (e.get("slots") or {}).get(name) or {}


def _brief(u: dict) -> list:
    out = []
    for e in u["effects"]:
        slots = {k: (v.get("prin"), v.get("prov"), (v.get("shape") or {}).get("const")) for k, v in (e.get("slots") or {}).items()}
        out.append((e["kind"], e["site"], e.get("resolution"), e.get("http_method"), e.get("fs_mode"), e.get("destructive"), slots))
    return out


def _notes(u: dict, kind: str) -> list[str]:
    return [n for r in u["rows"] if r["kind"] == kind for n in r.get("notes", [])]


def _status(u: dict, kind: str, decl: str) -> str:
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（効果行が消えている）: {_brief(u)}"
    notes = [n for r in rows for n in r.get("notes", [])]
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方: {notes}"
    if hit:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, kind: str, decl: str) -> set[str]:
    out = set()
    for n in _notes(u, kind):
        for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
            if n.startswith(pre):
                out.add(n[len(pre):])
    return out


def _check(u: dict, kind: str, decl: str, want: str, reason: str | None = None) -> None:
    got = _status(u, kind, decl)
    q = u["unit"]["qualname"]
    assert got == want, f"{q} {kind} {decl}: {got}（期待 {want}）notes={_notes(u, kind)} effects={_brief(u)}"
    if reason is not None:
        assert reason in _reasons(u, kind, decl), f"{q} {decl}: 理由 {_reasons(u, kind, decl)}（期待 {reason}）"


def _not_clear(u: dict, kind: str, decl: str) -> None:
    got = _status(u, kind, decl)
    assert got in ("矛", "不"), f"{u['unit']['qualname']} {decl}: 内（誤 clear）notes={_notes(u, kind)} effects={_brief(u)}"


def _no_append_mode(u: dict) -> None:
    """mode が分からない形で `"a"`（destructive=False）を読んでいない。"""
    es = _effects(u, "FS_WRITE")
    assert es, _brief(u)
    for e in es:
        assert e.get("destructive") is not False and e.get("fs_mode") != "a", f"{u['unit']['qualname']}: {_brief(u)}"


def _append_mode(u: dict) -> None:
    """対照: 書き換えの無い定数 `"a"` は今までどおり読む（fs_mode=a / destructive=False）。"""
    es = _effects(u, "FS_WRITE")
    assert es and all(e.get("fs_mode") == "a" and e.get("destructive") is False for e in es), _brief(u)


CONFIG = 'MODE = "a"\n'

#: 読む側（属性の形と from-import の形）。どちらも path は MODEL。
SERVER = '''from mcp.server.fastmcp import FastMCP

from . import config
from .config import MODE

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def append_attr(path: str, text: str) -> str:
    with open(path, config.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def append_from(path: str, text: str) -> str:
    with open(path, MODE) as fh:
        fh.write(text)
    return "ok"
'''


def _pkg(init: str, admin: str | None) -> dict:
    files = {"pkg/__init__.py": init, "pkg/config.py": CONFIG, "pkg/server.py": SERVER}
    if admin is not None:
        files["pkg/admin.py"] = admin
    return files


# ===========================================================================
# U09-A1: 点つきの連鎖での書き込み `pkg.config.MODE = v`
# ===========================================================================

A1_TREES = {
    # レビューの t1
    "chain": _pkg("", "import pkg.config\n\n\ndef set_mode(v):\n    pkg.config.MODE = v\n"),
    # 同じ連鎖の del
    "chain_del": _pkg("", "import pkg.config\n\n\ndef drop():\n    del pkg.config.MODE\n"),
    # 別名つきの親パッケージから連鎖で書く
    "chain_alias": _pkg("", "import pkg as p\nimport pkg.config\n\n\ndef set_mode(v):\n    p.config.MODE = v\n"),
    # 対照: 連鎖で別の名前を書く（MODE は書き換えられない）
    "chain_other_name": _pkg("", "import pkg.config\n\n\ndef set_other(v):\n    pkg.config.OTHER = v\n"),
}


@pytest.fixture(scope="module")
def a1(tmp_path_factory):
    return {k: _units(tmp_path_factory, f"u09adv_a1_{k}", v) for k, v in A1_TREES.items()}


@pytest.mark.parametrize("tree", ["chain", "chain_del", "chain_alias"])
@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_a1_dotted_chain_store_is_rebinding(a1, tree, tool):
    """U09-A1: `pkg.config.MODE = v`（連鎖での再束縛）の後、MODE は "a" と決まらない → mode 不明で D2 矛。
    from-import の形（`from .config import MODE`）も同じ書き込みで同じになる（前からあった穴も閉じる）。"""
    u = a1[tree][tool]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_unknown_model_path")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_keep_a1_chain_store_of_other_name(a1, tool):
    """対照: 連鎖で別の名前 `pkg.config.OTHER` を書いても MODE は再束縛されない → "a" のまま D2 内。"""
    u = a1["chain_other_name"][tool]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")


# ===========================================================================
# U09-A2: `from pkg import *` で来た `config` への書き込み
# ===========================================================================

A2_TREES = {
    # レビューの t3
    "star": _pkg("from . import config\n", "from pkg import *\n\n\ndef set_mode(v):\n    config.MODE = v\n"),
    # star import で来た別名の流出（setattr）
    "star_setattr": _pkg("from . import config\n", "from pkg import *\n\n\ndef set_any(k, v):\n    setattr(config, k, v)\n"),
    # `__init__.py` が import しなくても、server.py の `from . import config` で pkg の属性になる（__all__ なし）
    "star_submodule": _pkg("", "from pkg import *\n\n\ndef set_mode(v):\n    config.MODE = v\n"),
    # 相対の star import
    "star_relative": _pkg("from . import config\n", "from . import *\n\n\ndef set_mode(v):\n    config.MODE = v\n"),
    # 対照: star import で来た `config` を読むだけ
    "star_read_only": _pkg("from . import config\n", "from pkg import *\n\n\ndef show():\n    return config.MODE\n"),
}


@pytest.fixture(scope="module")
def a2(tmp_path_factory):
    return {k: _units(tmp_path_factory, f"u09adv_a2_{k}", v) for k, v in A2_TREES.items()}


@pytest.mark.parametrize("tree", ["star", "star_submodule", "star_relative"])
@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_a2_star_import_alias_store(a2, tree, tool):
    """U09-A2: star import で来た `config` はパッケージの名前空間の pkg.config。`config.MODE = v` は再束縛 → D2 矛。"""
    u = a2[tree][tool]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_unknown_model_path")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_a2_star_import_alias_escape(a2, tool):
    """U09-A2: star import で来た `config` を setattr に渡す（モジュールオブジェクトの流出、条件 (iv)）→ 内にしない。"""
    u = a2["star_setattr"][tool]
    _no_append_mode(u)
    _not_clear(u, "FS_WRITE", "D2")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_keep_a2_star_import_read_only(a2, tool):
    """対照: star import で来た `config` の属性を読むだけなら書き換えは無い → "a" のまま D2 内。"""
    u = a2["star_read_only"][tool]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")


# ===========================================================================
# U09-A3: `__init__.py` が別名で再公開したモジュールへの書き込み
# ===========================================================================

A3_TREES = {
    # レビューの t10
    "reexport": _pkg("from . import config as settings\n",
                     "from pkg import settings\n\n\ndef set_mode(v):\n    settings.MODE = v\n"),
    # 同じ別名の流出（setattr）
    "reexport_setattr": _pkg("from . import config as settings\n",
                             "from pkg import settings\n\n\ndef set_any(k, v):\n    setattr(settings, k, v)\n"),
    # 親パッケージの属性の連鎖で再公開名に書く（A1 と A3 の合成）
    "reexport_chain": _pkg("from . import config as settings\n",
                           "import pkg\n\n\ndef set_mode(v):\n    pkg.settings.MODE = v\n"),
    # 2 段の再公開: pkg/__init__ が sub の再公開名をさらに再公開する
    "reexport_two_hops": {
        "pkg/__init__.py": "from .sub import settings\n",
        "pkg/sub/__init__.py": "from .. import config as settings\n",
        "pkg/config.py": CONFIG,
        "pkg/server.py": SERVER,
        "pkg/admin.py": "from pkg import settings\n\n\ndef set_mode(v):\n    settings.MODE = v\n",
    },
    # 対照: 再公開名を読むだけ
    "reexport_read_only": _pkg("from . import config as settings\n",
                               "from pkg import settings\n\n\ndef show():\n    return settings.MODE\n"),
}


@pytest.fixture(scope="module")
def a3(tmp_path_factory):
    return {k: _units(tmp_path_factory, f"u09adv_a3_{k}", v) for k, v in A3_TREES.items()}


@pytest.mark.parametrize("tree", ["reexport", "reexport_chain", "reexport_two_hops"])
@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_a3_reexported_module_store(a3, tree, tool):
    """U09-A3: 再公開名 `settings` は pkg.config のモジュールオブジェクト。`settings.MODE = v` は再束縛 → D2 矛。"""
    u = a3[tree][tool]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_unknown_model_path")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_a3_reexported_module_escape(a3, tool):
    """U09-A3: 再公開名を setattr に渡す（流出）→ 内にしない。"""
    u = a3["reexport_setattr"][tool]
    _no_append_mode(u)
    _not_clear(u, "FS_WRITE", "D2")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_keep_a3_reexport_read_only(a3, tool):
    """対照: 再公開名を読むだけなら "a" のまま D2 内。"""
    u = a3["reexport_read_only"][tool]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")


# ===========================================================================
# U09-A4: 入れ子関数から見た、外側の関数の束縛
# ===========================================================================

A4_CONFIG_FILES = {"pkg/__init__.py": "", "pkg/config.py": CONFIG, "pkg/other.py": 'MODE = "w"\n'}

#: 読む側の見出し。どのモジュールも直下で pkg.config を `config` / `MODE` に束縛する。
A4_HDR = '''from mcp.server.fastmcp import FastMCP

from . import config
from .config import MODE

mcp = FastMCP("t")


'''

#: 1 モジュールに tool を 1 つ置く（同名の入れ子 `inner` が木に 2 つあると呼び出しが解けず（`_uniq`）、
#: 効果行が出なくなって確かめにならない。仮引数の名前は `_scan_module_writes` がモジュールの書き込みに
#: 数えるので、同じモジュールに置くと他の tool の from-import の形まで opaque になる）。
A4_TOOLS = {
    # レビューの t6: 外側の局所 import `from . import other as config`
    "append_closure": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure(path: str, text: str) -> str:
    from . import other as config

    def inner():
        with open(path, config.MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # レビューの t6b: 外側の局所 `from .other import MODE`（from-import の形の前からの穴）
    "append_closure_from": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_from(path: str, text: str) -> str:
    from .other import MODE

    def inner():
        with open(path, MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # `import pkg.other as config`
    "append_closure_import_as": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_import_as(path: str, text: str) -> str:
    import pkg.other as config

    def inner():
        with open(path, config.MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # 2 段外側の局所 import
    "append_closure_two_levels": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_two_levels(path: str, text: str) -> str:
    from . import other as config

    def middle():
        def inner():
            with open(path, config.MODE) as fh:
                fh.write(text)

        inner()

    middle()
    return "ok"
''',
    # 外側の仮引数 MODE（既定値だけでは決まらない）
    "append_closure_param": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_param(path: str, text: str, MODE: str = "a") -> str:
    def inner():
        with open(path, MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # 対照: 外側の関数が `config` を束縛しない閉包
    "append_closure_control": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_control(path: str, text: str) -> str:
    def inner():
        with open(path, config.MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # 対照: 外側の関数が `MODE` を束縛しない閉包（from-import の形）
    "append_closure_from_control": '''@mcp.tool(annotations={"destructiveHint": False})
def append_closure_from_control(path: str, text: str) -> str:
    def inner():
        with open(path, MODE) as fh:
            fh.write(text)

    inner()
    return "ok"
''',
    # 対照: 直に読む
    "append_plain": '''@mcp.tool(annotations={"destructiveHint": False})
def append_plain(path: str, text: str) -> str:
    with open(path, config.MODE) as fh:
        fh.write(text)
    return "ok"
''',
    # 対照: 読む関数自身の局所 import（条件 (ii) の関数の中の import）
    "append_local_import": '''@mcp.tool(annotations={"destructiveHint": False})
def append_local_import(path: str, text: str) -> str:
    from . import config as cfg

    with open(path, cfg.MODE) as fh:
        fh.write(text)
    return "ok"
''',
}

#: レビューの t9（外側の関数の局所クラス / 局所 import のクラス）と対照（外側が束縛しない）。
A4_CLASS_HDR = '''import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class LocalStore:
    def request(self, method, path):
        return None


class Cfg:
    client = httpx.Client(base_url="https://api.example.com")


'''

A4_CLASS_TOOLS = {
    "get_item": '''@mcp.tool(annotations={"readOnlyHint": True})
def get_item(item: str) -> str:
    class Cfg:
        client = LocalStore()

    def inner():
        Cfg.client.request("DELETE", "/items/" + item)

    inner()
    return "ok"
''',
    "get_item_import": '''@mcp.tool(annotations={"readOnlyHint": True})
def get_item_import(item: str) -> str:
    from .store import Holder as Cfg

    def inner():
        Cfg.client.request("DELETE", "/items/" + item)

    inner()
    return "ok"
''',
    "get_item_control": '''@mcp.tool(annotations={"readOnlyHint": True})
def get_item_control(item: str) -> str:
    def inner():
        Cfg.client.request("DELETE", "/items/" + item)

    inner()
    return "ok"
''',
}

A4_STORE = '''class LocalStore:
    def request(self, method, path):
        return None


class Holder:
    client = LocalStore()
'''


def _uniq(src: str, k: str) -> str:
    """入れ子の関数名を木の中で一意にする（別のモジュールに同名の入れ子 `inner` があると、今の解析器は末尾名の
    曖昧さで呼び出しに降りず、効果行が出ない。確かめたいのは値の読みなので名前を分ける）。"""
    return src.replace("inner", f"inner_{k}").replace("middle", f"middle_{k}")


@pytest.fixture(scope="module")
def a4(tmp_path_factory):
    fs = {**A4_CONFIG_FILES, **{f"pkg/s_{k}.py": A4_HDR + _uniq(v, k) for k, v in A4_TOOLS.items()}}
    cls = {"pkg/__init__.py": "", "pkg/store.py": A4_STORE,
           **{f"pkg/s_{k}.py": A4_CLASS_HDR + _uniq(v, k) for k, v in A4_CLASS_TOOLS.items()}}
    return {
        "fs": _units(tmp_path_factory, "u09adv_a4_fs", fs),
        "cls": _units(tmp_path_factory, "u09adv_a4_cls", cls),
    }


@pytest.mark.parametrize("tool", [
    "append_closure",
    "append_closure_from",
    "append_closure_import_as",
    "append_closure_two_levels",
])
def test_fix_a4_enclosing_function_binding(a4, tool):
    """U09-A4 (a): 内側の関数の `config` / `MODE` は外側の関数の束縛（pkg.other・仮引数）。モジュール直下の
    pkg.config.MODE = "a" を読まない → mode 不明（path は外側の仮引数を閉包で読むので OP/opaque）で内にしない。"""
    u = a4["fs"][tool]
    _no_append_mode(u)
    _not_clear(u, "FS_WRITE", "D2")


def test_keep_a4_enclosing_param(a4):
    """対照（直す前から正しい形）: 外側の関数の仮引数 `MODE` を閉包で読む。仮引数の名前は `_scan_module_writes`
    が書き込みに数えるので、from-import の `MODE` は opaque → mode 不明で D2 不。"""
    u = a4["fs"]["append_closure_param"]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "不")


@pytest.mark.parametrize("tool", ["get_item", "get_item_import"])
def test_fix_a4_enclosing_local_class(a4, tool):
    """U09-A4 (b): 内側の関数の `Cfg` は外側の関数の局所クラス / 局所 import（client は LocalStore）。モジュール
    直下の `Cfg.client`（httpx）の型を付けない → NET 行は出ず、D1 の矛にもならない。"""
    u = a4["cls"][tool]
    assert not _effects(u, "NET"), _brief(u)
    assert not any(n == "contradiction:D1" for r in u["rows"] for n in r.get("notes", [])), u["rows"]


@pytest.mark.parametrize("tool", ["append_plain", "append_local_import"])
def test_keep_a4_no_enclosing_binding(a4, tool):
    """対照: 直に読む形と、読む関数自身の局所 import は今までどおり pkg.config.MODE = "a" を読む → D2 内。"""
    u = a4["fs"][tool]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")


@pytest.mark.parametrize("tool", ["append_closure_control", "append_closure_from_control"])
def test_keep_a4_closure_without_enclosing_binding(a4, tool):
    """対照: 外側の関数が同名を束縛しない閉包は、モジュール直下の "a" を読む → fs_mode=a で D2 内
    （path は閉包で読む外側の仮引数なので OP/opaque）。直す前も同じ（閉包を一律に opaque にしない）。"""
    u = a4["fs"][tool]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")


def test_keep_a4_closure_reads_module_class(a4):
    """対照: 外側が束縛しない閉包の `Cfg.client` はモジュール直下の httpx.Client（規則 B で型だけ）→ NET 行、DELETE で D1 矛。"""
    u = a4["cls"]["get_item_control"]
    assert any(e.get("http_method") == "DELETE" for e in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


# ===========================================================================
# U09-A5: 多重継承のクラス属性（MRO の左が勝つ）
# ===========================================================================

A5_SERVER = '''import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class LocalStore:
    def request(self, method, path):
        return None


class LocalMixin:
    store = LocalStore()
    METHOD = "GET"


class RemoteBase:
    store = httpx.Client(base_url="https://api.example.com")
    METHOD = "DELETE"


class Plain:
    pass


class Backend(LocalMixin, RemoteBase):
    pass


class Deep(Backend):
    pass


class Single(RemoteBase):
    pass


class OneDefiner(Plain, RemoteBase):
    pass


@mcp.tool(annotations={"readOnlyHint": True})
def get_item(item: str) -> str:
    Backend.store.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def get_item_deep(item: str) -> str:
    Deep.store.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def get_item2(item: str) -> str:
    httpx.request(Backend.METHOD, "https://api.example.com/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def get_single(item: str) -> str:
    Single.store.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def get_one_definer(item: str) -> str:
    OneDefiner.store.request("DELETE", "/items/" + item)
    return "ok"
'''


@pytest.fixture(scope="module")
def a5(tmp_path_factory):
    return _units(tmp_path_factory, "u09adv_a5", {"pkg/__init__.py": "", "pkg/server.py": A5_SERVER})


@pytest.mark.parametrize("tool", ["get_item", "get_item_deep"])
def test_fix_a5_multiple_inheritance_left_wins(a5, tool):
    """U09-A5: `class Backend(LocalMixin, RemoteBase)` の `store` は MRO の左の LocalMixin.store（LocalStore）。
    httpx の型を付けない → NET 行は出ず、D1 の矛にもならない。"""
    u = a5[tool]
    assert not _effects(u, "NET"), _brief(u)
    assert not any(n == "contradiction:D1" for r in u["rows"] for n in r.get("notes", [])), u["rows"]


def test_keep_a5_class_const_method_not_read(a5):
    """対照（could_not_break）: 規則 B のクラス属性の定数は http_method として読まれない → net_method_unknown で D1 不。"""
    _check(a5["get_item2"], "NET", "D1", "不", "net_method_unknown")


@pytest.mark.parametrize("tool", ["get_single", "get_one_definer"])
def test_keep_a5_single_definer(a5, tool):
    """対照: 単一継承、または多重継承でも属性を定義するクラスが 1 つだけなら、その値（httpx.Client）の型が付く
    （規則 B）→ NET 行、DELETE で D1 矛。"""
    u = a5[tool]
    assert any(e.get("http_method") == "DELETE" for e in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


# ===========================================================================
# 崩せなかった形（could_not_break）: 直した後も同じでなければならない
# ===========================================================================

T7_SERVER = '''import types

from mcp.server.fastmcp import FastMCP

from . import config

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def append_closure_assign(path: str, text: str) -> str:
    config = types.SimpleNamespace(MODE="w")

    def inner():
        with open(path, config.MODE) as fh:
            fh.write(text)

    inner()
    return "ok"


def make_server():
    from . import other as config

    @mcp.tool(annotations={"destructiveHint": False})
    def nested_tool(path: str, text: str) -> str:
        with open(path, config.MODE) as fh:
            fh.write(text)
        return "ok"

    return mcp
'''

T11_READER = '''from mcp.server.fastmcp import FastMCP

from . import config

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def append_attr(path: str, text: str) -> str:
    with open(path, config.MODE) as fh:
        fh.write(text)
    return "ok"
'''

T11_TREES = {
    "a": {"__init__.py": "from .settings import config\n", "config.py": CONFIG,
          "settings.py": 'import types\nconfig = types.SimpleNamespace(MODE="w")\n'},
    "b": {"__init__.py": "from . import other as config\n", "config.py": CONFIG, "other.py": 'MODE = "w"\n'},
    "c": {"__init__.py": "", "config.py": '(MODE, *REST), X = ("a", "b", "c"), 1\n'},
    "d": {"__init__.py": "", "config.py": 'MODE = "a"\n\ndef load():\n    global MODE\n    [MODE := m for m in ("w",)]\n'},
    "e": {"__init__.py": "", "config.py": CONFIG,
          "admin.py": "import {p}\nimport {p}.config\n\ndef g(v):\n    c = {p}.config\n    c.MODE = v\n"},
    "f": {"__init__.py": "", "config.py": CONFIG, "admin.py": "import {p}\n\ndef g(k, v):\n    setattr({p}.config, k, v)\n"},
    "g": {"__init__.py": "", "config.py": CONFIG},
}


@pytest.fixture(scope="module")
def cnb(tmp_path_factory):
    out = {"t7": _units(tmp_path_factory, "u09adv_t7", {**A4_CONFIG_FILES, "pkg/server.py": T7_SERVER})}
    for k, files in T11_TREES.items():
        p = f"t11{k}"
        tree = {f"{p}/{rel}": src.replace("{p}", p) for rel, src in files.items()}
        tree[f"{p}/server.py"] = T11_READER
        out[k] = _units(tmp_path_factory, f"u09adv_t11{k}", tree)
    return out


def test_keep_cnb_t7_closure_local_assign(cnb):
    """t7: 閉包が外側の局所代入 `config = SimpleNamespace(MODE="w")` を読む → D2 不のまま。"""
    u = cnb["t7"]["append_closure_assign"]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "不")


def test_keep_cnb_t7_nested_tool(cnb):
    """t7: 入れ子の tool 定義が外側の局所 import `other as config` を読む → 内にしない（D2 矛のまま）。"""
    u = cnb["t7"]["make_server.nested_tool"]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛")


@pytest.mark.parametrize("tree", ["a", "b", "c", "d", "e", "f"])
def test_keep_cnb_t11_stay_opaque(cnb, tree):
    """t11 a〜f: 親パッケージが葉の名前を別の値にする・Starred・global の下の `:=`・別名への代入・連鎖の setattr
    は、どれも MODE を "a" と決めない → D2 矛のまま。"""
    u = cnb[tree]["append_attr"]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛")


def test_keep_cnb_t11_control(cnb):
    """t11 g（対照）: 書き換えの無い `config.MODE` は "a" → D2 内。"""
    u = cnb["g"]["append_attr"]
    _append_mode(u)
    _check(u, "FS_WRITE", "D2", "内")
