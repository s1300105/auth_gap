"""O36 / O37 の修正（`docs/decisions.md` D59、規則は `693ee79` でコミット済み）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。
直す前のエンジンでは「直す」側の期待がすべて落ちることを確かめてからコミットする。
「変えない」側（片側だけの束縛の値を残す、import の無い経路の値）は反例として入れた。
"""

from __future__ import annotations

import pytest

from authgap.ir import Atom, Prin, Value, value_join
from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = r'''
import os
import subprocess

import httpx
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool()
async def neg_const(p: str) -> str:
    os.system(-5); return "x"


@mcp.tool()
async def not_const(p: str) -> str:
    subprocess.run(["echo", not True]); return "x"


@mcp.tool()
async def not_none(p: str) -> str:
    subprocess.run(["echo", not None]); return "x"


@mcp.tool()
async def handler_sees_try_assignment(url: str) -> str:
    c = None
    try:
        c = httpx.Client()
        raise ValueError("x")
    except ValueError:
        c.post(url)
    return "x"


@mcp.tool()
async def handler_before_only(url: str) -> str:
    c = httpx.Client()
    try:
        pass
    except ValueError:
        c.post(url)
    return "x"


@mcp.tool()
async def try_import_value(p: str) -> str:
    try:
        from shlex import quote as q
    except ImportError:
        q = None
    os.system(q)
    return "x"


@mcp.tool()
async def one_sided_kept(url: str, flag: bool) -> str:
    if flag:
        c = httpx.Client()
    c.post(url)
    return "x"


@mcp.tool()
async def req_post_json(url: str, payload: str) -> str:
    requests.post(url, json={"q": payload}); return "x"


@mcp.tool()
async def req_post_data(url: str, payload: str) -> str:
    requests.post(url, data={"q": payload}); return "x"


@mcp.tool()
async def httpx_post_data(url: str, payload: str) -> str:
    httpx.post(url, data={"q": payload}); return "x"


@mcp.tool()
async def session_post_data(url: str, payload: str) -> str:
    c = httpx.Client()
    c.post(url, data={"q": payload}); return "x"


@mcp.tool()
async def session_request_json(url: str, payload: str) -> str:
    c = httpx.Client()
    c.request("POST", url, json={"q": payload}); return "x"


@mcp.tool()
async def httpx_request_json(url: str, payload: str) -> str:
    httpx.request("POST", url, json={"q": payload}); return "x"


@mcp.tool()
async def session_get_json(url: str, payload: str) -> str:
    c = httpx.Client()
    c.get(url, json={"q": payload}); return "x"


@mcp.tool()
async def req_post_content_not_in_spec(url: str, payload: str) -> str:
    httpx.post(url, content=payload); return "x"


@mcp.tool()
async def req_post_const_body(url: str) -> str:
    requests.post(url, json={"q": "fixed"}); return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("o36")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u, site_suffix):
    return [e for e in u["effects"] if e["site"].endswith(site_suffix)]


# ---------------------------------------------------------------------------
# O36-1: 単項演算の値
# ---------------------------------------------------------------------------


def test_neg_const_is_negated(units):
    (e,) = _effects(units["neg_const"], "os.system")
    assert e["slots"]["shell_string"]["shape"].get("const") == -5


@pytest.mark.parametrize("tool", ["not_const", "not_none"])
def test_not_const_is_inverted(units, tool):
    (e,) = _effects(units[tool], "subprocess.run")
    items = e["slots"]["argv[*]"]["shape"]["items"]
    # `not True` は False、`not None` は True。被演算子の値のまま（True / None）にしない
    want = False if tool == "not_const" else True
    assert items[1]["shape"].get("const") is want, items[1]


# ---------------------------------------------------------------------------
# O36-2: Atom の合流は可換（none と定数の型を比べる）
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a,b",
    [
        (Atom(none=True), Atom()),
        (Atom(const=True), Atom(const=1)),
        (Atom(const=0), Atom(const=False)),
        (Atom(none=True), Atom(const="x")),
    ],
)
def test_atom_join_commutative_and_not_constant(a, b):
    ab = value_join(Value(Prin.OP, shape=a), Value(Prin.OP, shape=b))
    ba = value_join(Value(Prin.OP, shape=b), Value(Prin.OP, shape=a))
    assert ab.shape == ba.shape
    assert ab.shape == Atom(), ab.shape


def test_atom_join_same_kept():
    v = Value(Prin.OP, shape=Atom(const="x"))
    assert value_join(v, v).shape == Atom(const="x")


# ---------------------------------------------------------------------------
# O36-3: 関数本体の import は名前を束縛し直す / 片側だけの束縛はその側の値を残す（変えない）
# ---------------------------------------------------------------------------


def test_try_import_value_is_not_constant_none(units):
    # try 側では `q` は import した関数（木外なので opaque(unresolved)）、except 側では None。
    # 合流は「確度 resolved の定数 None」ではない（manifest は `none` を出さないので確度で見る）。
    (e,) = _effects(units["try_import_value"], "os.system")
    slot = e["slots"]["shell_string"]
    assert slot["prov"] != "resolved", slot


def test_one_sided_binding_keeps_receiver_type(units):
    # 反例（変えない）: `if flag: c = httpx.Client()` の後の `c.post` は、他方の経路では NameError。
    # Unknown と合流すると受け手型が落ちて効果が消える（誤 clear）。
    assert _effects(units["one_sided_kept"], ".post")


# ---------------------------------------------------------------------------
# O36-4: except 節の入口は try 前と try 本体の各文の後の合流
# ---------------------------------------------------------------------------


def test_handler_sees_try_assignment(units):
    assert _effects(units["handler_sees_try_assignment"], ".post")


def test_handler_before_only_kept(units):
    # 反例（変えない）: try 前に束縛した受け手は今までどおり見える
    assert _effects(units["handler_before_only"], ".post")


# ---------------------------------------------------------------------------
# O37: body は仕様書どおり data|json（仕様書 229 行目）。content= は仕様に無いので足さない（O39）
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tool,site",
    [
        ("req_post_json", "requests.post"),
        ("req_post_data", "requests.post"),
        ("httpx_post_data", "httpx.post"),
        ("session_post_data", ".post"),
        ("session_request_json", ".request"),
        ("httpx_request_json", "httpx.request"),
        ("session_get_json", ".get"),
    ],
)
def test_body_is_data_or_json(units, tool, site):
    (e,) = _effects(units[tool], site)
    body = e["slots"].get("body")
    assert body is not None and body["prin"] == "MODEL", e["slots"]


def test_content_kw_not_in_spec(units):
    # 仕様書に無い `content=` は body にしない（sink 語彙は月 3 凍結。O39 の限界）
    (e,) = _effects(units["req_post_content_not_in_spec"], "httpx.post")
    assert "body" not in e["slots"]


def test_const_body_is_op(units):
    (e,) = _effects(units["req_post_const_body"], "requests.post")
    assert e["slots"]["body"]["prin"] == "OP"
