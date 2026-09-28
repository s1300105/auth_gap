"""D64 / U40: 呼び出し形の登録を入口にする。所見 R2-r1-2（`x.tool(...)(fn)` と `add_tool`）と R2-r5-3（gptme spec_object）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U40）。** v2 / v3 の件数には合わせず、
PEP 318（`@d(...) def f` は `f = d(...)(f)` の糖衣）、公式 SDK の `FastMCP.tool` / `MCPServer.tool`
（`def decorator(fn): self.add_tool(fn, ...)` を返すだけ）、gptme の `ToolSpec(name=..., execute=fn)`
（`gptme/tools/base.py` の dataclass）、Def 2 R2（カタログ化した入口の仮引数が MODEL）、§7.1（FS_WRITE → D1 の矛）、
D64 の U40 行と `evidence/review/triage.json` の fix_outline（避ける条件）、学生の決定（`add_tool` も直す、
ToolSpec は import 元で照合）から導いた。

直すべき挙動（今は落ちる）:

- (A) `mcp.tool(...)(fn)` / `mcp.tool()(fn)` / `self.mcp.tool()(self.m)` / `wrapped = mcp.tool(...)(fn)` /
  `def register(mcp): mcp.tool()(fn)` の位置引数 0 がユニットになる。`annotations=` / `name=` は外側の
  `tool(...)` のキーワードから読む。
- (B) `mcp.add_tool(fn, annotations=...)` / `self.mcp.add_tool(self.m, ...)` もユニットになる（ENTRY_RULES の
  names に add_tool を足す逸脱）。
- (C) `ToolSpec(name="...", execute=fn)` を import 元が gptme の ToolSpec（`gptme.tools.base.ToolSpec`、再公開の
  `gptme.tools.ToolSpec`、gptme 内の `from .base import ToolSpec` / `from . import ToolSpec`）のときだけユニットにする。
  framework `gptme`、entry_kind `spec_object`、tool_name は `name=`、仮引数は `confirm` も含めて全部 MODEL（R2 例外は凍結）。
- 同じ関数の二重登録は 1 ユニット。

壊してはいけない挙動（今は通る。直した後も通ること）:

- 検証役の反例 cx_r1_2_extern: 位置引数 0 を末尾名の索引で引かない。木外を指す import なら採らない。
  同じ名前の無関係な木内の関数を偽のユニットにしない（readOnlyHint に対する D1 の誤警報になる）。
- `self.<attr>` は囲むクラスの中だけで解く。別クラスの同名メソッドを採らない。
- 解決できない引数（lambda、partial、ループ変数、`Tool.from_function(fn)`）は採らない。
- `require_positional` の規則は同じ構造条件で見る（`click.command()(main)` をユニットにしない）。
- 裸名 `ToolSpec` の末尾一致にしない（木内の自前 ToolSpec、`handler=` の ToolSpec、`ClientToolSpec`、他ライブラリの
  ToolSpec）。gptme の `execute=create_mcp_execute_function(...)` のような呼び出し式は採らない。
- デコレータ形の既存のユニットと矛は変えない。

仮定（notes に明記）: 呼び出し形のユニットの `entry_kind` は決め打ちしない（`decorator` でも新しい値でもよい）。
framework は `_match_decorator` と同じく先頭の規則 `mcp`。記号: 「矛」 = 行の注記に `contradiction:<宣言>`。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


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


def _one(m, qualname, relpath=None):
    hits = _hits(m, qualname, relpath)
    have = sorted((u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"])
    where = f"{relpath}:{qualname}" if relpath else qualname
    assert hits, f"{where} がユニットにならない: {have}"
    assert len(hits) == 1, f"{where} が {len(hits)} ユニット（二重登録）: {have}"
    return hits[0]


def _contra(u, decl="D1"):
    return any(n == f"contradiction:{decl}" for r in u["rows"] for n in r.get("notes", []))


def _any_contra(m):
    return any(
        "CONTRADICTION" in r.get("verdicts", []) or any(n.startswith("contradiction:") for n in r.get("notes", []))
        for u in m["units"]
        for r in u["rows"]
    )


def _kinds(u):
    return sorted({(e["kind"], e["site"]) for e in u["effects"]})


def _slot(u, site, slot):
    effs = [e for e in u["effects"] if e["site"] == site]
    assert effs, f"{u['unit']['qualname']}: {site} の効果が無い: {_kinds(u)}"
    s = effs[0]["slots"][slot]
    return s["prin"], s["prov"]


def _param_names(u):
    return [p["name"] for p in u["unit"]["params"]]


def _excluded(u):
    return {p["name"]: p["excluded"] for p in u["unit"]["params"] if "excluded" in p}


# ---------------------------------------------------------------------------
# R2-r1-2 の再現（t10_add_tool）+ 代入形・入れ子の登録
# ---------------------------------------------------------------------------

#: 所見 R2-r1-2 の repro_code そのまま（`scratchpad/review/R2/r1/t10_add_tool/server.py`）に、
#: fix_outline (A) の「wrapped = mcp.tool(...)(fn)」と条件 (4)「def register(mcp): mcp.tool()(fn)」を足した。
SRC_CALL = r'''import os
import shutil
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")


def via_add_tool(path: str) -> str:
    shutil.rmtree(path)
    return "ok"


def via_direct_call(path: str) -> str:
    os.remove(path)
    return "ok"


def via_direct_call_named(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"


def via_assign(path: str) -> str:
    os.remove(path)
    return "ok"


def via_register(path: str) -> str:
    os.remove(path)
    return "ok"


mcp.add_tool(via_add_tool, annotations=ToolAnnotations(readOnlyHint=True))
mcp.tool()(via_direct_call)
mcp.tool(name="renamed", annotations=ToolAnnotations(readOnlyHint=True))(via_direct_call_named)
wrapped = mcp.tool(annotations={"readOnlyHint": True})(via_assign)


def register(server):
    server.tool(annotations={"readOnlyHint": True})(via_register)

    def local_rm(path: str) -> str:
        os.remove(path)
        return "ok"

    server.tool(annotations={"readOnlyHint": True})(local_rm)


class FileServer:
    def __init__(self) -> None:
        self.mcp = FastMCP("cls")
        self.mcp.tool()(self.delete_file)
        self.mcp.add_tool(self.write_file, annotations=ToolAnnotations(readOnlyHint=True))

    def delete_file(self, path: str) -> str:
        os.remove(path)
        return "ok"

    def write_file(self, path: str, text: str) -> str:
        with open(path, "w") as f:
            f.write(text)
        return "ok"


# control: decorator form in the same tree
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def control_deco(path: str) -> str:
    os.remove(path)
    return "ok"
'''


@pytest.fixture(scope="module")
def call_tree(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_call", {"server.py": SRC_CALL})


# -- 直すべき挙動（今は落ちる）---------------------------------------------


def test_r1_2_direct_call_empty_parens_is_unit(call_tree):
    """R2-r1-2 (A): `mcp.tool()(fn)` は `@mcp.tool()` と同じ。宣言 ⊥ で FS_WRITE の行が出る（矛は無い）。"""
    u = _one(call_tree, "via_direct_call")
    assert u["unit"]["framework"] == "mcp"
    assert u["D_kind"]["bottom"] is True
    assert ("FS_WRITE", "os.remove") in _kinds(u)
    assert _slot(u, "os.remove", "path") == ("MODEL", "resolved")
    assert not _contra(u)


def test_r1_2_direct_call_reads_outer_name_and_annotations(call_tree):
    """R2-r1-2 (A): `name=` / `annotations=` は外側の `tool(...)` から読む。readOnlyHint と open('w') → §7.1 D1 の矛。"""
    u = _one(call_tree, "via_direct_call_named")
    assert u["unit"]["tool_name"] == "renamed"
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _param_names(u) == ["path", "text"]
    assert any(e["kind"] == "FS_WRITE" for e in u["effects"]), _kinds(u)
    assert _contra(u, "D1")


def test_r1_2_assigned_call_form_is_unit(call_tree):
    """fix_outline (A): `wrapped = mcp.tool(...)(fn)` も同じ経路。dict 形の annotations も読む → D1 の矛。"""
    u = _one(call_tree, "via_assign")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_r1_2_registration_inside_function_is_unit(call_tree):
    """fix_outline 条件 (4): `def register(server): server.tool(...)(fn)` の中の登録も落とさない（モジュール水準の fn）。"""
    u = _one(call_tree, "via_register")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_r1_2_local_def_registered_in_function_is_unit(call_tree):
    """条件 (4) と (1): 登録文の囲む関数の中の def（入れ子 def の @mcp.tool を拾う既存方針の呼び出し形）。"""
    u = _one(call_tree, "register.local_rm")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_r1_2_add_tool_is_unit(call_tree):
    """R2-r1-2 (B) と学生の決定（add_tool を names に足す逸脱）: `mcp.add_tool(fn, annotations=RO)` → rmtree で D1 の矛。"""
    u = _one(call_tree, "via_add_tool")
    assert u["unit"]["framework"] == "mcp"
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert any(e["kind"] == "FS_WRITE" for e in u["effects"]), _kinds(u)
    assert _contra(u, "D1")


def test_r1_2_self_method_via_tool_call_is_unit(call_tree):
    """R2-r1-2 (A) と条件 (2): `self.mcp.tool()(self.delete_file)` を囲むクラスの中で解く。self は MODEL にしない。"""
    u = _one(call_tree, "FileServer.delete_file")
    assert _param_names(u) == ["path"]
    assert u["D_kind"]["bottom"] is True
    assert ("FS_WRITE", "os.remove") in _kinds(u)
    assert not _contra(u)


def test_r1_2_self_method_via_add_tool_is_unit(call_tree):
    """R2-r1-2 (B): `self.mcp.add_tool(self.write_file, annotations=RO)` → open('w') で D1 の矛。"""
    u = _one(call_tree, "FileServer.write_file")
    assert _param_names(u) == ["path", "text"]
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


# -- 壊してはいけない挙動（今も通る）---------------------------------------


def test_r1_2_control_decorator_unchanged(call_tree):
    """対照: 同じ木のデコレータ形は 1 ユニットで D1 の矛のまま。"""
    u = _one(call_tree, "control_deco")
    assert u["unit"]["entry_kind"] == "decorator"
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_r1_2_registrars_are_not_units(call_tree):
    """対照: 登録する側（`register` / `__init__`）はツールではない。"""
    assert not _hits(call_tree, "register")
    assert not _hits(call_tree, "FileServer.__init__")


# ---------------------------------------------------------------------------
# 二重登録（registered 集合）
# ---------------------------------------------------------------------------

SRC_DOUBLE = r'''import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def both(path: str) -> str:
    os.remove(path)
    return "ok"


def twice(path: str) -> str:
    os.remove(path)
    return "ok"


mcp.tool()(both)
mcp.tool()(twice)
mcp.add_tool(twice)
'''


@pytest.fixture(scope="module")
def double_tree(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_double", {"server.py": SRC_DOUBLE})


def test_double_decorator_and_call_is_one_unit(double_tree):
    """反例（変えない）: デコレータ形と呼び出し形の両方で登録された関数は 1 ユニットのまま、デコレータの宣言と矛を保つ。"""
    u = _one(double_tree, "both")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_double_call_and_add_tool_is_one_unit(double_tree):
    """fix_outline (A): 二重登録は (module, qualname) の registered 集合で 1 ユニットにする。"""
    _one(double_tree, "twice")


# ---------------------------------------------------------------------------
# 検証役の反例 cx_r1_2_extern と、スコープ解決の条件 (1)
# ---------------------------------------------------------------------------

#: `scratchpad/verify/R2_hm_1/cx_r1_2_extern` の counterexample_code そのまま。
CX_EXTERN_B = r'''from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from vendor_search_lib import search  # external package, not in the tree

mcp = FastMCP("t")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(search)
'''

CX_EXTERN_A = r'''import os

def search(path: str) -> str:
    """Unrelated helper sharing the name `search`; never registered."""
    os.remove(path)
    return "ok"
'''


def test_cx_r1_2_extern_no_false_unit(tmp_path_factory):
    """検証役の反例 cx_r1_2_extern: 木外の search の登録で、木内の無関係な a.search を偽のユニットにしない（D1 の誤警報）。"""
    m = _manifest(tmp_path_factory, "cx_r1_2_extern", {"a.py": CX_EXTERN_A, "b.py": CX_EXTERN_B})
    assert m["units"] == [], [(u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"]]
    assert not _any_contra(m)


CX_EXTERN_ATTR_B = r'''from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import vendor_search_lib as vsl  # external package, not in the tree

mcp = FastMCP("t")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(vsl.search)
mcp.add_tool(vsl.search, annotations=ToolAnnotations(readOnlyHint=True))
'''


def test_cx_extern_attribute_and_add_tool_no_false_unit(tmp_path_factory):
    """条件 (1) の Attribute 形と add_tool 形: 木外モジュールの属性は採らない。a.search を偽のユニットにしない。"""
    m = _manifest(tmp_path_factory, "cx_extern_attr", {"a.py": CX_EXTERN_A, "b.py": CX_EXTERN_ATTR_B})
    assert m["units"] == [], [(u["unit"]["relpath"], u["unit"]["qualname"]) for u in m["units"]]
    assert not _any_contra(m)


#: 同じモジュールの束縛を先に見る: b.py の search（読むだけ）を登録。a.py の同名 search は危険だが登録されない。
SAME_MOD_B = r'''from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")


def search(path: str) -> str:
    with open(path) as f:
        return f.read()


mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(search)
'''


@pytest.fixture(scope="module")
def same_mod_tree(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_same_mod", {"a.py": CX_EXTERN_A, "b.py": SAME_MOD_B})


def test_same_module_binding_never_resolves_to_other_module(same_mod_tree):
    """条件 (1) の反例（変えない）: 末尾名の索引で引かない。a.search はユニットにならず、木に矛は出ない。"""
    assert not _hits(same_mod_tree, "search", "a.py")
    assert not _any_contra(same_mod_tree)


def test_same_module_binding_is_unit(same_mod_tree):
    """条件 (1): 登録文のモジュールのスコープで引いた b.search がユニット（readOnlyHint、読むだけなので矛なし）。"""
    u = _one(same_mod_tree, "search", "b.py")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert not _contra(u)


#: 木内の別モジュールからの import（`from .impl import purge` / `from pkg import impl` の属性）。
CROSS_IMPL = r'''import os


def purge(path: str) -> str:
    os.remove(path)
    return "ok"


def purge_attr(path: str) -> str:
    os.remove(path)
    return "ok"
'''

CROSS_SERVER = r'''from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from . import impl
from .impl import purge

mcp = FastMCP("t")
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(purge)
mcp.add_tool(impl.purge_attr, annotations=ToolAnnotations(readOnlyHint=True))
'''

#: 同名の無関係な purge（登録されない）。
CROSS_DECOY = r'''import shutil


def purge(path: str) -> str:
    shutil.rmtree(path)
    return "ok"
'''


@pytest.fixture(scope="module")
def cross_tree(tmp_path_factory):
    return _manifest(
        tmp_path_factory,
        "u40_cross",
        {
            "pkg/__init__.py": "",
            "pkg/impl.py": CROSS_IMPL,
            "pkg/server.py": CROSS_SERVER,
            "other/__init__.py": "",
            "other/decoy.py": CROSS_DECOY,
        },
    )


def test_cross_module_import_resolves_strictly(cross_tree):
    """条件 (1): 木内モジュールは import 表と resolve_import_module で厳密に解く。pkg/impl.py の purge がユニット。"""
    u = _one(cross_tree, "purge", "pkg/impl.py")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _contra(u, "D1")


def test_cross_module_attribute_resolves_strictly(cross_tree):
    """条件 (1) の Attribute 形: `impl.purge_attr` を add_tool で登録 → pkg/impl.py の purge_attr。"""
    u = _one(cross_tree, "purge_attr", "pkg/impl.py")
    assert _contra(u, "D1")


def test_cross_module_decoy_not_unit(cross_tree):
    """条件 (1) の反例（変えない）: 同名の other/decoy.py の purge はユニットにしない。"""
    assert not _hits(cross_tree, "purge", "other/decoy.py")


# ---------------------------------------------------------------------------
# 条件 (1) の入れ子のスコープ: 囲む関数のローカル def がモジュールの同名 def を隠す
# ---------------------------------------------------------------------------

SRC_SHADOW = r'''import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")


def clean(path: str) -> str:
    os.remove(path)
    return "ok"


def register(server):
    def clean(path: str) -> str:
        with open(path) as f:
            return f.read()

    server.tool(annotations=ToolAnnotations(readOnlyHint=True))(clean)
'''


def test_local_def_shadows_module_def(tmp_path_factory):
    """条件 (1) の反例（変えない）: ローカルの clean を登録している。モジュール水準の危険な clean はユニットにせず、矛も出さない。"""
    m = _manifest(tmp_path_factory, "u40_shadow", {"server.py": SRC_SHADOW})
    assert not _hits(m, "clean")
    assert not _any_contra(m)


# ---------------------------------------------------------------------------
# 条件 (2): self.<attr> は囲むクラスの中だけ
# ---------------------------------------------------------------------------

SRC_SELF_SCOPE = r'''import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from vendor_base import VendorServer  # external base class


class Danger:
    def delete_file(self, path: str) -> str:
        os.remove(path)
        return "ok"

    def lookup(self, path: str) -> str:
        os.remove(path)
        return "ok"


class Borrowing(VendorServer):
    """delete_file を持たない（木外の基底から来るかもしれない）。"""

    def __init__(self) -> None:
        self.mcp = FastMCP("b")
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.delete_file)


class Reader:
    def __init__(self) -> None:
        self.mcp = FastMCP("r")
        self.mcp.add_tool(self.lookup, annotations=ToolAnnotations(readOnlyHint=True))

    def lookup(self, path: str) -> str:
        with open(path) as f:
            return f.read()
'''


@pytest.fixture(scope="module")
def self_scope_tree(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_self_scope", {"server.py": SRC_SELF_SCOPE})


def test_self_attr_other_class_not_unit(self_scope_tree):
    """条件 (2) の反例（変えない）: 別クラス Danger の同名メソッドを採らない。木に矛は出ない。"""
    assert not _hits(self_scope_tree, "Danger.delete_file")
    assert not _hits(self_scope_tree, "Danger.lookup")
    assert not _any_contra(self_scope_tree)


def test_self_attr_enclosing_class_is_unit(self_scope_tree):
    """条件 (2): `self.mcp.add_tool(self.lookup, ...)` は囲むクラス Reader の lookup（読むだけ、矛なし）。"""
    u = _one(self_scope_tree, "Reader.lookup")
    assert u["unit"]["annotations"] == {"readOnlyHint": True}
    assert _param_names(u) == ["path"]
    assert not _contra(u)


# ---------------------------------------------------------------------------
# 条件 (3): 解決できない引数は採らない / require_positional の構造条件
# ---------------------------------------------------------------------------

SRC_UNRESOLVABLE = r'''import functools
import os
import shutil

import click
from flask import Flask
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool
from mcp.types import ToolAnnotations

mcp = FastMCP("t")
app = Flask(__name__)
RO = ToolAnnotations(readOnlyHint=True)


def rm_in(path: str, root: str) -> str:
    os.remove(os.path.join(root, path))
    return "ok"


def rm_lambda_target(path: str) -> str:
    os.remove(path)
    return "ok"


def rm_loop_a(path: str) -> str:
    os.remove(path)
    return "ok"


def rm_loop_b(path: str) -> str:
    shutil.rmtree(path)
    return "ok"


def rm_from_function(path: str) -> str:
    os.remove(path)
    return "ok"


def main(path: str) -> None:
    os.remove(path)


def route_handler(path: str) -> str:
    os.remove(path)
    return "ok"


mcp.tool(annotations=RO)(functools.partial(rm_in, root="/srv"))
mcp.tool(annotations=RO)(lambda path: rm_lambda_target(path))
for _fn in (rm_loop_a, rm_loop_b):
    mcp.tool(annotations=RO)(_fn)
mcp.add_tool(Tool.from_function(rm_from_function, annotations=RO))
cli = click.command()(main)
app.route("/rm")(route_handler)
'''


@pytest.fixture(scope="module")
def unresolvable_tree(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_unresolvable", {"server.py": SRC_UNRESOLVABLE})


@pytest.mark.parametrize(
    "qualname",
    ["rm_in", "rm_lambda_target", "rm_loop_a", "rm_loop_b", "rm_from_function"],
)
def test_unresolvable_argument_not_unit(unresolvable_tree, qualname):
    """条件 (3) の反例（変えない）: partial / lambda / ループ変数 / `Tool.from_function(fn)` は採らない（数え落としのまま）。"""
    assert not _hits(unresolvable_tree, qualname)


def test_require_positional_and_foreign_call_not_unit(unresolvable_tree):
    """反例（変えない）: `click.command()(main)` は AutoGPT 規則の構造条件（位置引数 3）を満たさない。`app.route(...)` は語彙外。"""
    assert not _hits(unresolvable_tree, "main")
    assert not _hits(unresolvable_tree, "route_handler")


def test_unresolvable_tree_has_no_contradiction(unresolvable_tree):
    """反例（変えない）: 採らない形から誤警報（readOnlyHint に対する D1 の矛）を作らない。"""
    assert not _any_contra(unresolvable_tree)


# ---------------------------------------------------------------------------
# R2-r5-3: gptme の ToolSpec（spec_object）
# ---------------------------------------------------------------------------

#: 所見 R2-r5-3 の repro_code そのまま（`scratchpad/review/R2/r5/t113_gptme_toolspec/tools_shell.py`）。
GPTME_SHELL = r'''# t113_gptme_toolspec/tools_shell.py
import subprocess
from collections.abc import Generator

from gptme.message import Message
from gptme.tools.base import ToolSpec


def execute_shell(code: str | None, args=None, kwargs=None, confirm=None) -> Generator[Message, None, None]:
    out = subprocess.run(code, shell=True, capture_output=True, text=True).stdout
    yield Message("system", out)


tool = ToolSpec(
    name="shell",
    desc="Executes shell commands.",
    execute=execute_shell,
    block_types=["shell"],
)
__doc__ = tool.get_doc(__doc__)
'''


@pytest.fixture(scope="module")
def gptme_shell(tmp_path_factory):
    return _manifest(tmp_path_factory, "u40_gptme_shell", {"tools_shell.py": GPTME_SHELL})


def test_r5_3_toolspec_execute_is_unit(gptme_shell):
    """R2-r5-3: `ToolSpec(name="shell", execute=execute_shell)`（gptme.tools.base から import）→ spec_object/gptme のユニット。"""
    u = _one(gptme_shell, "execute_shell")
    assert u["unit"]["framework"] == "gptme"
    assert u["unit"]["entry_kind"] == "spec_object"
    assert u["unit"]["tool_name"] == "shell"


def test_r5_3_all_params_model_including_confirm(gptme_shell):
    """R2-r5-3 と検証役の corrected_expected: 仮引数は confirm も含めて全部 MODEL（R2 例外は月 3 凍結）。D は ⊥。"""
    u = _one(gptme_shell, "execute_shell")
    assert _param_names(u) == ["code", "args", "kwargs", "confirm"]
    assert _excluded(u) == {}
    assert u["D_kind"]["bottom"] is True
    assert not _any_contra(gptme_shell)


def test_r5_3_spawn_shell_string_model(gptme_shell):
    """R2-r5-3: `subprocess.run(code, shell=True)` の SPAWN 行に shell_string MODEL/resolved。"""
    u = _one(gptme_shell, "execute_shell")
    assert ("SPAWN", "subprocess.run") in _kinds(u)
    assert _slot(u, "subprocess.run", "shell_string") == ("MODEL", "resolved")


#: gptme の木そのもの: 22 モジュールの `from .base import ToolSpec` と、1 モジュールの `from . import ToolSpec`（再公開）。
GPTME_BASE = r'''from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class ToolSpec:
    name: str
    desc: str = ""
    execute: Optional[Callable] = None
'''

GPTME_INIT = r'''from .base import ToolSpec

__all__ = ["ToolSpec"]
'''

GPTME_SAVE = r'''from pathlib import Path

from .base import ToolSpec


def execute_save(code: str | None, args=None, kwargs=None, confirm=None):
    Path(args[0]).write_text(code)
    yield "saved"


tool = ToolSpec(name="save", desc="Save a file.", execute=execute_save)
'''

GPTME_PATCH = r'''import os

from . import ToolSpec


def execute_rm(code: str | None, args=None, kwargs=None, confirm=None):
    os.remove(code)
    yield "removed"


tool = ToolSpec(name="rm", desc="Remove a file.", execute=execute_rm)
'''

GPTME_MCP = r'''from .base import ToolSpec


def create_mcp_execute_function(tool_name, client):
    def execute(code=None, args=None, kwargs=None, confirm=None):
        return client.call_tool(tool_name, kwargs)

    return execute


tool = ToolSpec(name="mcp", desc="MCP", execute=create_mcp_execute_function("x", None))
'''


@pytest.fixture(scope="module")
def gptme_tree(tmp_path_factory):
    return _manifest(
        tmp_path_factory,
        "u40_gptme_tree",
        {
            "gptme/__init__.py": "",
            "gptme/tools/__init__.py": GPTME_INIT,
            "gptme/tools/base.py": GPTME_BASE,
            "gptme/tools/save.py": GPTME_SAVE,
            "gptme/tools/rm.py": GPTME_PATCH,
            "gptme/tools/mcp.py": GPTME_MCP,
        },
    )


def test_r5_3_relative_import_from_base_is_unit(gptme_tree):
    """R2-r5-3 (C): gptme 内の `from .base import ToolSpec` を resolve_import_module で gptme.tools.base.ToolSpec に解く。"""
    u = _one(gptme_tree, "execute_save", "gptme/tools/save.py")
    assert u["unit"]["framework"] == "gptme"
    assert u["unit"]["entry_kind"] == "spec_object"
    assert u["unit"]["tool_name"] == "save"
    assert any(e["kind"] == "FS_WRITE" for e in u["effects"]), _kinds(u)


def test_r5_3_reexport_from_package_is_unit(gptme_tree):
    """R2-r5-3 (C) と検証役 (iii): 再公開の `from . import ToolSpec`（gptme.tools.ToolSpec）も受ける。"""
    u = _one(gptme_tree, "execute_rm", "gptme/tools/rm.py")
    assert u["unit"]["framework"] == "gptme"
    assert u["unit"]["tool_name"] == "rm"
    assert ("FS_WRITE", "os.remove") in _kinds(u)


def test_r5_3_call_expression_execute_not_unit(gptme_tree):
    """fix_outline (C) 条件 (4) の反例（変えない）: `execute=create_mcp_execute_function(...)` は採らない。"""
    assert not _hits(gptme_tree, "create_mcp_execute_function")
    assert not _hits(gptme_tree, "create_mcp_execute_function.execute")


def test_r5_3_toolspec_class_itself_not_unit(gptme_tree):
    """対照（変えない）: ToolSpec のクラス定義の側はユニットにしない。"""
    assert not [u for u in gptme_tree["units"] if u["unit"]["relpath"] == "gptme/tools/base.py"]


GPTME_DOWNSTREAM = r'''import os

from gptme.tools import ToolSpec


def execute_purge(code: str | None, args=None, kwargs=None, confirm=None):
    os.remove(code)
    yield "ok"


tool = ToolSpec(name="purge", desc="Purge.", execute=execute_purge)
'''


def test_r5_3_downstream_reexport_is_unit(tmp_path_factory):
    """R2-r5-3 (C): 下流のプラグインの `from gptme.tools import ToolSpec`（木外の再公開名）も受ける。"""
    m = _manifest(tmp_path_factory, "u40_gptme_downstream", {"plugin_purge.py": GPTME_DOWNSTREAM})
    u = _one(m, "execute_purge")
    assert u["unit"]["framework"] == "gptme"
    assert u["unit"]["entry_kind"] == "spec_object"
    assert u["unit"]["tool_name"] == "purge"


#: gptme の execute= が木外の関数を指す。木内の無関係なモジュールに同名の run_it がある。
GPTME_EXTERN_EXEC = r'''from gptme.tools.base import ToolSpec
from gptme_ext.runner import run_it  # external, not in the tree

tool = ToolSpec(name="ext", desc="External.", execute=run_it)
'''

DECOY_RUN_IT = r'''import os


def run_it(code=None, args=None, kwargs=None, confirm=None):
    os.remove(code)
'''


def test_r5_3_extern_execute_no_false_unit(tmp_path_factory):
    """(C) と条件 (1) の反例（変えない）: execute= が木外を指せば採らない。木内の同名 run_it を末尾名で引かない。"""
    m = _manifest(tmp_path_factory, "u40_gptme_extern", {"tool_ext.py": GPTME_EXTERN_EXEC, "helpers.py": DECOY_RUN_IT})
    assert not _hits(m, "run_it")


# -- 裸名 ToolSpec の末尾一致にしない（避ける条件 (1)）--------------------------

#: 木内の自前 ToolSpec（execute= を取る）。gptme ではない。
OWN_SPEC = r'''from dataclasses import dataclass
from typing import Callable


@dataclass
class ToolSpec:
    name: str
    execute: Callable
'''

OWN_TOOLS = r'''import os

from myapp.spec import ToolSpec


def own_rm(path: str) -> str:
    os.remove(path)
    return "ok"


SPEC = ToolSpec(name="own_rm", execute=own_rm)
'''

#: rag-toolkit の形（`handler=`）。
RAG_TOOLS = r'''import shutil

from rag.mcp.spec import ToolSpec


def rag_wipe(path: str) -> dict:
    shutil.rmtree(path)
    return {}


SPEC = ToolSpec(name="rag_wipe", description="wipe", handler=rag_wipe)
'''

#: OpenHands の `ClientToolSpec` と、別ライブラリの ToolSpec（execute=）。
FOREIGN_TOOLS = r'''import os

from openhands.core.tools import ClientToolSpec
from other_agent_lib.tools import ToolSpec


def client_rm(path: str) -> str:
    os.remove(path)
    return "ok"


def foreign_rm(path: str) -> str:
    os.remove(path)
    return "ok"


A = ClientToolSpec(name="client_rm", execute=client_rm)
B = ToolSpec(name="foreign_rm", execute=foreign_rm)
'''


@pytest.fixture(scope="module")
def non_gptme_tree(tmp_path_factory):
    return _manifest(
        tmp_path_factory,
        "u40_non_gptme",
        {
            "myapp/__init__.py": "",
            "myapp/spec.py": OWN_SPEC,
            "myapp/tools.py": OWN_TOOLS,
            "rag/__init__.py": "",
            "rag/mcp/__init__.py": "",
            "rag/mcp/tools.py": RAG_TOOLS,
            "foreign.py": FOREIGN_TOOLS,
        },
    )


def test_non_gptme_toolspec_no_gptme_unit(non_gptme_tree):
    """避ける条件 (1) の反例（変えない）: import 元が gptme でない ToolSpec / ClientToolSpec からは gptme のユニットを作らない。"""
    assert not [u for u in non_gptme_tree["units"] if u["unit"]["framework"] == "gptme"]


@pytest.mark.parametrize("qualname", ["own_rm", "rag_wipe", "client_rm", "foreign_rm"])
def test_non_gptme_toolspec_function_not_unit(non_gptme_tree, qualname):
    """避ける条件 (1) の反例（変えない）: 裸名 ToolSpec の末尾一致で MCP 母集団の分母を動かさない。"""
    assert not _hits(non_gptme_tree, qualname)


# ---------------------------------------------------------------------------
# gptme の二重登録: spec_object は tools_list より前に置き registered に入れる（fix_outline (C) 条件 (3)）
# ---------------------------------------------------------------------------

GPTME_AND_LIST = r'''import os

from gptme.tools.base import ToolSpec


def execute_both(code: str | None, args=None, kwargs=None, confirm=None):
    os.remove(code)
    yield "ok"


tool = ToolSpec(name="both", desc="Both.", execute=execute_both)
tools = [execute_both]
'''


def test_r5_3_spec_object_before_tools_list(tmp_path_factory):
    """fix_outline (C) 条件 (3): ToolSpec と `tools = [fn]` の両方に出る関数は 1 ユニットで、framework は gptme。"""
    m = _manifest(tmp_path_factory, "u40_gptme_list", {"tool_both.py": GPTME_AND_LIST})
    u = _one(m, "execute_both")
    assert u["unit"]["framework"] == "gptme"
    assert u["unit"]["entry_kind"] == "spec_object"
    assert u["unit"]["tool_name"] == "both"
