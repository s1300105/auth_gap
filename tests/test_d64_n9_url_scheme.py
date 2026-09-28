"""D64 / N9: URL の `://` は、その前が RFC 3986 の scheme の文法のときだけ scheme の区切り（§9.6 の改訂 7''）。

**期待値はこのテストで、`authgap/` を直す前に書いた（2026-09-28、学生の決定で凍結の前に直す）。** 所見は
`evidence/review/advrev_u33_u36.md` の N9。`client.get("oauth/authorize?redirect_uri=http://localhost:8080/cb")` の
クエリの中の `://` を区切りにして宛先を `localhost` と読み、`openWorldHint: false` の D3 を 内 にしていた（false-clean）。
`/` で始まらない相対参照の宛先は読まない（R3d-r6-2 は記録のまま）ので、直した後は 内 でなければよい（不か矛）。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _units(tmp_path_factory, name, src):
    d = tmp_path_factory.mktemp(name)
    (d / "server.py").write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _status(u: dict, decl: str = "D3") -> str:
    rows = [r for r in u["rows"] if r["kind"] == "NET"]
    assert rows, f"{u['unit']['qualname']}: NET の行が無い（前提が崩れている）"
    notes = [n for r in rows for n in r.get("notes", [])]
    if f"contradiction:{decl}" in notes:
        return "矛"
    return "不" if any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes) else "内"


SRC = '''
import httpx
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
client = httpx.Client(base_url="https://api.example.com")


@mcp.tool(annotations={"openWorldHint": False})
def fix_query_redirect(p: str) -> str:
    client.get("oauth/authorize?redirect_uri=http://localhost:8080/cb&state=" + p)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
def fix_query_redirect_requests(p: str) -> str:
    requests.get("callback?next=http://127.0.0.1/done&q=" + p)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
def keep_absolute_local(p: str) -> str:
    requests.get("http://localhost:8080/cb?q=" + p)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
def keep_absolute_external_with_local_query(p: str) -> str:
    requests.get("https://api.example.com/x?next=http://localhost/&q=" + p)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
def keep_scheme_with_plus(p: str) -> str:
    requests.get("git+https://evil.example/repo?q=" + p)
    return "x"


@mcp.tool(annotations={"openWorldHint": False})
def keep_relative_slash(p: str) -> str:
    client.get("/items?q=" + p)
    return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    return _units(tmp_path_factory, "n9", SRC)


@pytest.mark.parametrize("tool", ["fix_query_redirect", "fix_query_redirect_requests"])
def test_fix_query_scheme_is_not_authority(units, tool):
    """N9: クエリの中の `://` の前は scheme の文法に合わない → 絶対 URL ではない。宛先を localhost と読まない（内にしない）。"""
    assert _status(units[tool]) != "内"


@pytest.mark.parametrize(
    "tool, want",
    [
        ("keep_absolute_local", "内"),  # scheme `http` は正しい → localhost
        ("keep_absolute_external_with_local_query", "矛"),  # host は api.example.com（クエリの localhost に惑わされない）
        ("keep_scheme_with_plus", "矛"),  # `git+https` は scheme の文法に合う → evil.example
        # `/` 始まりの相対参照は base_url の宛先（D57）。ただしモジュール水準の client の base_url は D17 で確度 opaque
        # なので宛先を読まず不（書いた当初は矛と見込んだが、D17 の規則から導くと不。直す前に改めた）
        ("keep_relative_slash", "不"),
    ],
)
def test_keep(units, tool, want):
    assert _status(units[tool]) == want
