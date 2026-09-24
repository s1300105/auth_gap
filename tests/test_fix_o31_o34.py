"""O31 / O34 の修正（`docs/decisions.md` D58、規則は `6da93f6` でコミット済み）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。
解決を上げる変更（O31）なので、**刈ってはいけない形**を反例として入れた。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

O31_SRC = r'''
import os
import shutil
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def write_text(path, text):
    if not path:
        return None
    Path(path).write_text(text)
    return path


def payload(text, out_path=None):
    return write_text(out_path, text)


def sync(target, force=False):
    if force and os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)


def reassigned(path, text):
    path = path or "/tmp/authgap_default"
    if not path:
        return None
    Path(path).write_text(text)


class Flagged:
    def __init__(self):
        self.enabled = False

    def run(self, p):
        if self.enabled:
            os.remove(p)


def checked(p):
    if os.path.isfile(p):
        os.remove(p)


def by_mode(p, mode):
    if mode == "a":
        return 1
    elif mode == "w":
        os.remove(p)


def both_return(p, flag):
    if flag:
        return 1
    else:
        return 2
    os.remove(p)


def always_raise(p):
    raise ValueError("no")
    os.remove(p)


def try_return(p):
    try:
        return 1
    finally:
        pass
    os.remove(p)


def pick(a):
    if not a:
        return "/tmp/authgap_picked"
    return a


@mcp.tool(annotations={"destructiveHint": False})
async def omitted_default(p: str) -> str:
    payload(p); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def passed_none(p: str) -> str:
    write_text(None, p); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def passed_model_path(path: str) -> str:
    write_text(path, "x"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def force_false(p: str) -> str:
    sync("/tmp/authgap_a", force=False); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def force_default(p: str) -> str:
    sync("/tmp/authgap_a"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def force_true(p: str) -> str:
    sync("/tmp/authgap_a", force=True); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def force_model(force: bool) -> str:
    sync("/tmp/authgap_a", force=force); return "x"


@mcp.tool()
async def reassigned_none(p: str) -> str:
    reassigned(None, p); return "x"


@mcp.tool()
async def attribute_condition(p: str) -> str:
    Flagged().run(p); return "x"


@mcp.tool()
async def call_condition(p: str) -> str:
    checked(p); return "x"


@mcp.tool()
async def elif_const(p: str) -> str:
    by_mode(p, "a"); return "x"


@mcp.tool()
async def elif_const_taken(p: str) -> str:
    by_mode(p, "w"); return "x"


@mcp.tool()
async def both_branches_return(p: str, flag: bool) -> str:
    both_return(p, flag); return "x"


@mcp.tool()
async def raise_first(p: str) -> str:
    always_raise(p); return "x"


@mcp.tool()
async def return_in_try(p: str) -> str:
    try_return(p); return "x"


@mcp.tool()
async def return_value_kept(p: str) -> str:
    Path(pick(None)).write_text(p); return "x"
'''


@pytest.fixture(scope="module")
def o31(tmp_path_factory):
    d = tmp_path_factory.mktemp("o31")
    (d / "server.py").write_text(O31_SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _sites(u, kind="FS_WRITE"):
    return sorted({e["site"] for e in u["effects"] if e["kind"] == kind})


@pytest.mark.parametrize(
    "tool,site,present",
    [
        # 刈る形
        ("omitted_default", "pathlib.Path.write_text", False),   # 既定値 None → if not path: return
        ("passed_none", "pathlib.Path.write_text", False),
        ("force_false", "shutil.rmtree", False),                 # force=False → and が偽
        ("force_default", "shutil.rmtree", False),               # 既定値 False
        ("elif_const", "os.remove", False),                      # mode == "a" の枝だけ
        ("both_branches_return", "os.remove", False),            # 両方の枝が return
        ("raise_first", "os.remove", False),                     # raise の後
        # 刈ってはいけない形（反例）
        ("passed_model_path", "pathlib.Path.write_text", True),  # モデル由来の path は定数でない
        ("force_true", "shutil.rmtree", True),
        ("force_model", "shutil.rmtree", True),
        ("reassigned_none", "pathlib.Path.write_text", True),    # 仮引数を再代入している
        ("attribute_condition", "os.remove", True),              # 属性の条件は評価しない
        ("call_condition", "os.remove", True),                   # 呼び出しの条件は評価しない
        ("elif_const_taken", "os.remove", True),                 # mode == "w" の枝は取られる
        ("return_in_try", "os.remove", True),                    # try は終わるとみなさない（保守側）
        # 刈っても makedirs は残る
        ("force_false", "os.makedirs", True),
        ("force_default", "os.makedirs", True),
    ],
)
def test_o31(o31, tool, site, present):
    assert (site in _sites(o31[tool])) is present, (tool, _sites(o31[tool]))


def test_o31_return_value_from_taken_branch_is_kept(o31):
    effs = [e for e in o31["return_value_kept"]["effects"] if e["site"] == "pathlib.Path.write_text"]
    assert effs, "取られる枝の return の値が捨てられて効果が消えた"


def test_o31_contradiction_follows(o31):
    # force=True だけが destructiveHint: false に反する（force=False / 既定値の誤警報が消える）
    def contra(u):
        return any("CONTRADICTION" in r["verdicts"] for r in u["rows"] if r["site"] == "shutil.rmtree")
    assert contra(o31["force_true"])
    assert not [r for r in o31["force_false"]["rows"] if r["site"] == "shutil.rmtree"]


# ---------------------------------------------------------------------------
# O34: 主語一致は値の MODEL の根すべてに要求する
# ---------------------------------------------------------------------------

O34_SRC = r'''
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

ALLOWED = ("a", "b")


@mcp.tool()
async def one_root_checked(name: str) -> str:
    if name not in ALLOWED:
        raise ValueError("bad")
    os.system("echo " + name)
    return "x"


@mcp.tool()
async def two_roots_one_checked(name: str, body: str) -> str:
    if name not in ALLOWED:
        raise ValueError("bad")
    os.system("echo " + name + body)
    return "x"


@mcp.tool()
async def two_roots_both_checked(name: str, body: str) -> str:
    if name not in ALLOWED:
        raise ValueError("bad")
    if body not in ALLOWED:
        raise ValueError("bad")
    os.system("echo " + name + body)
    return "x"
'''


@pytest.fixture(scope="module")
def o34(tmp_path_factory):
    d = tmp_path_factory.mktemp("o34")
    (d / "server.py").write_text(O34_SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _inject(u):
    return any("GAP_INJECT" in r["verdicts"] for r in u["rows"] if r["site"] == "os.system")


def test_o34_premise_single_root_gate_clears(o34):
    # 前提: 根が 1 つで検証されていれば GAP_INJECT は出ない（ゲートが効いている）
    assert [r for r in o34["one_root_checked"]["rows"] if r["site"] == "os.system"]
    assert not _inject(o34["one_root_checked"])


def test_o34_unchecked_root_keeps_inject(o34):
    # body は検証されていないので、name の検証だけで GAP_INJECT を消してはならない
    assert _inject(o34["two_roots_one_checked"])


def test_o34_all_roots_checked_clears(o34):
    # 反例: 両方の根が検証されていれば GAP_INJECT は出ない
    assert not _inject(o34["two_roots_both_checked"])


# ---------------------------------------------------------------------------
# D58 の改訂: 静的な名前は「束縛し直さない仮引数」だけ（run15 の敵対的レビューで見つけた誤 clear）
#
# 下の反例はどれも**実行時に sink に届く**。O31 の改訂前はここで枝を捨てていた（誤 clear）。
# 前提として O31 より前（289624c）のエンジンではすべて効果が出ることを確かめてある。
# ---------------------------------------------------------------------------

O31R_SRC = r"""
import asyncio
import os
import shutil

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def helper_remove(p):
    os.remove(p)


def srch(p, focus=None):
    if focus:
        os.remove(p)


def backfill(p, raw=False):
    cached = not raw
    if cached:
        os.remove(p)


def joined(p, flag, n):
    v = None if flag else n
    if v is not None:
        os.remove(p)


def extract(p, mode):
    m = mode
    if mode == "off":
        m = None
    if m == "eager":
        os.remove(p)


def loop_rebind(p, flag=False):
    for flag in (True,):
        pass
    if flag:
        os.remove(p)


def aug_rebind(p, n=0):
    n += 1
    if n == 1:
        os.remove(p)


def inner(p, force=False):
    if force:
        shutil.rmtree(p)


def outer(p, force=False):
    inner(p, force=force)


@mcp.tool()
async def kwargs_forward(p: str) -> str:
    srch(p, **{"focus": "x"}); return "x"


@mcp.tool()
async def starred_args(p: str) -> str:
    srch(*[p, "x"]); return "x"


@mcp.tool()
async def indirect_thread(p: str) -> str:
    await asyncio.to_thread(srch, p, "x"); return "x"


@mcp.tool()
async def not_assigned(p: str) -> str:
    backfill(p); return "x"


@mcp.tool()
async def join_with_none(p: str, flag: bool) -> str:
    joined(p, flag, 3); return "x"


@mcp.tool()
async def model_join_none(p: str, mode: str) -> str:
    extract(p, mode); return "x"


@mcp.tool()
async def rebound_by_for(p: str) -> str:
    loop_rebind(p); return "x"


@mcp.tool()
async def rebound_by_augassign(p: str) -> str:
    aug_rebind(p); return "x"


@mcp.tool()
async def join_none_twice(p: str, mode: str, flag: bool) -> str:
    m = mode
    if flag:
        m = None
    if flag:
        m = None
    if m == "eager":
        os.remove(p)
    return "x"


@mcp.tool()
async def static_passthrough(p: str) -> str:
    outer(p, force=False); return "x"


@mcp.tool()
async def static_passthrough_default(p: str) -> str:
    outer(p); return "x"


@mcp.tool()
async def static_passthrough_true(p: str) -> str:
    outer(p, force=True); return "x"
"""


@pytest.fixture(scope="module")
def o31r(tmp_path_factory):
    d = tmp_path_factory.mktemp("o31r")
    (d / "server.py").write_text(O31R_SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _all_sites(u):
    return sorted({e["site"] for e in u["effects"]})


@pytest.mark.parametrize(
    "tool,site,present",
    [
        # 刈ってはいけない（改訂前は誤 clear）
        ("kwargs_forward", "os.remove", True),        # (A) `**` で渡した focus を既定値 None にしていた
        ("starred_args", "os.remove", True),          # (A) `*` の要素を 1 つの位置引数にしていた
        ("indirect_thread", "os.remove", True),       # (A') 間接の降下
        ("not_assigned", "os.remove", True),          # (B) `cached = not raw` が raw と同じ真偽になっていた
        ("join_with_none", "os.remove", True),        # (C) None との合流が定数 None
        ("model_join_none", "os.remove", True),       # (C) MODEL の値が if の後で定数 None
        ("join_none_twice", "os.remove", True),       # (C) 2 回目の合流で `Atom(none)` が勝つ（memory-hub write_memory）
        ("rebound_by_for", "os.remove", True),        # 仮引数を for で束縛し直す
        ("rebound_by_augassign", "os.remove", True),  # 仮引数を += で束縛し直す
        # 刈る（呼び出し元で静的な名前をそのまま渡す）
        ("static_passthrough", "shutil.rmtree", False),
        ("static_passthrough_default", "shutil.rmtree", False),
        ("static_passthrough_true", "shutil.rmtree", True),
    ],
)
def test_o31_revised(o31r, tool, site, present):
    assert (site in _all_sites(o31r[tool])) is present, (tool, _all_sites(o31r[tool]))


# (D) try の片側だけの束縛（auto_grocer `seed_recipes` の形）。同じファイルからの import は O31 より前でも
# 解決しないので、別モジュールから import する（前提: 289624c のエンジンで `requests.get` が出る）。
O31D_YT = """
import requests


def is_youtube_url(url) -> bool:
    return "youtube" in str(url)


def fetch(url):
    return requests.get(url, timeout=3).text


def youtube_recipe_from_url(url):
    return fetch(url)
"""

O31D_SERVER = """
from typing import Callable

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool()
def seed(url: str = "", ingredients: list | None = None) -> dict:
    if ingredients is None:
        ingredients = []
    is_youtube_url: Callable[[str], bool] | None
    try:
        from pkg.yt import is_youtube_url, youtube_recipe_from_url
    except Exception:
        is_youtube_url = None
    if is_youtube_url and is_youtube_url(url) and not ingredients:
        youtube_recipe_from_url(url)
    return {}
"""


def test_o31_revised_try_import_one_sided(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "yt.py").write_text(O31D_YT, encoding="utf-8")
    (pkg / "server.py").write_text(O31D_SERVER, encoding="utf-8")
    res = run(RunConfig(src_root=str(tmp_path), population="mcp_server", full=True))
    units = {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}
    assert "requests.get" in _all_sites(units["seed"]), _all_sites(units["seed"])
