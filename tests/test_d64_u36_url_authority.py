"""D64 / U36: D3 の宛先ホストを RFC 3986 の authority の文法で取り出す（`docs/contradiction_principles.md` §9.6 の 7）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U36）。** 期待値は §7.3（宛先が定数で
localhost / private / loopback → 内、定数の外部ホスト → 矛、読めない → 不）と §9.6 の 7（IP リテラルを先に試す、
次に `urlparse('//' + 権威部).hostname`、末尾ドットは名前の比較だけで落とす、ValueError と `\\` は不）から
導いた。v2 / v3 の件数には合わせていない。

所見は `evidence/review/explore_d3d4.json` の R3d-r6-1（userinfo・角括弧 IPv6 + ポート・末尾ドットの手元宛てを
外部と読む誤警報）。同じ単位の R3d-r6-2（相対参照）と R1d-r6-7（列）は D64 で記録に回すので対象外。

- 今の解析器で**落ちる**側（`FIX_*`）: 所見の 6 件（矛 → 内）、今の手書き分解が作っている誤 clear
  （`localhost:pw@evil.example` / `10.0.0.5:80@evil.example`、内 → 矛）、§9.6 の 7 の「`\\` と ValueError は不」。
- 今の解析器で**通る**側（`KEEP_*`）: 検証役の反例（`evidence/review/verify_d3d4.json` の R3d-r6-1 と
  `evidence/review/triage.json` の U36 fix_outline の (a)〜(d)）、所見の対照、今正しく判定できている形。
  直した後もこれが通らなければならない。

`_split_url` は変えない（SSRF の座標 `url.host` は権威部全体のまま。§2.6 と整合）ことも KEEP で固定する。
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


def _net_notes(u: dict) -> list[str]:
    rows = [r for r in u["rows"] if r["kind"] == "NET"]
    assert rows, f"{u['unit']['qualname']}: NET の行が無い（前提が崩れている）"
    return [n for r in rows for n in r.get("notes", [])]


def _status(u: dict, decl: str = "D3") -> str:
    """NET の行の宣言 `decl` の判定: 矛 / 不 / 内（tests/test_contradiction_principles.py と同じ読み方）。"""
    rows = [r for r in u["rows"] if r["kind"] == "NET"]
    notes = _net_notes(u)
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方"
    if hit:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, decl: str = "D3") -> set[str]:
    out = set()
    for n in _net_notes(u):
        for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
            if n.startswith(pre):
                out.add(n[len(pre):])
    return out


def _host_consts(u: dict) -> list:
    return [
        ((e.get("slots") or {}).get("url.host") or {}).get("shape", {}).get("const")
        for e in u["effects"]
        if e["kind"] == "NET"
    ]


def _check(units, tool, want, reason):
    u = units[tool]
    got = _status(u)
    assert got == want, f"{tool} D3: {got}（期待 {want}）notes={_net_notes(u)} url.host={_host_consts(u)}"
    if reason is not None:
        assert reason in _reasons(u), f"{tool} D3: 理由 {_reasons(u)}（期待 {reason}）"


HEAD = '''
import httpx
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
'''


def _tool(name: str, call: str) -> str:
    return f'''

@mcp.tool(annotations={{"openWorldHint": False}})
async def {name}(p: str) -> str:
    {call}; return "x"
'''


# ---------------------------------------------------------------------------
# 直すべき挙動（今は落ちる）
# ---------------------------------------------------------------------------

# (tool, 呼び出し, 期待, 理由, 根拠)
FIX_CASES = [
    # R3d-r6-1 の所見の 6 件（§7.3: 宛先の host は loopback / link-local / localhost → 内）
    ("fix_ipv6_loopback_port", 'httpx.get("http://[::1]:8080/x")', "内", None,
     "R3d-r6-1: 角括弧 IPv6 + ポート。host は ::1（loopback）"),
    ("fix_ipv6_linklocal_port", 'httpx.get("http://[fe80::1]:80/x")', "内", None,
     "R3d-r6-1: 角括弧 IPv6 + ポート。host は fe80::1（link-local。実装は is_link_local を local に含める）"),
    ("fix_userinfo_localhost_port", 'httpx.get("http://user:pass@localhost:8080/x")', "内", None,
     "R3d-r6-1: userinfo + ポート。host は localhost"),
    ("fix_userinfo_localhost", 'httpx.get("http://user:pass@localhost/x")', "内", None,
     "R3d-r6-1: userinfo。host は localhost（今は ':' の前の user を host と読む）"),
    ("fix_userinfo_ipv4", 'requests.get("http://admin@127.0.0.1/x")', "内", None,
     "R3d-r6-1: userinfo。host は 127.0.0.1"),
    ("fix_trailing_dot", 'httpx.get("http://localhost./x")', "内", None,
     "R3d-r6-1: 末尾ドットは名前の比較で落とす（§9.6 の 7、RFC 6761 の localhost.）"),
    # 同じ規則から導ける形
    ("fix_trailing_dot_no_path", 'httpx.get("http://localhost.")', "内", None,
     "§9.6 の 7: 末尾ドットの欠落はパスの有無によらない（検証役の補足 (2)）"),
    ("fix_trailing_dot_port", 'httpx.get("http://localhost.:8080/x")', "内", None,
     "§9.6 の 7: ポートを外してから末尾ドットを名前の比較で落とす"),
    ("fix_trailing_dot_sub_localhost", 'httpx.get("http://api.localhost./x")', "内", None,
     "§9.6 の 7: `.localhost` の名前の比較も末尾ドットを落としてから"),
    ("fix_ipv6_mapped_loopback_port", 'httpx.get("http://[::ffff:127.0.0.1]:8080/x")', "内", None,
     "§9.6 の 7: 角括弧 + ポートを外した IP リテラルは IPv4 写像の loopback"),
    # 今の手書き分解が作っている誤 clear（triage U36: 候補では 矛）
    ("fix_userinfo_colon_external", 'httpx.get("http://localhost:pw@evil.example/x")', "矛", "net_external_host",
     "verify R3d-r6-1 一般性: userinfo の ':' の前を host と読む誤 clear。実際の宛先は evil.example"),
    ("fix_userinfo_ip_port_external", 'httpx.get("http://10.0.0.5:80@evil.example/x")', "矛", "net_external_host",
     "verify R3d-r6-1 一般性: userinfo が private IP + ポートの形の誤 clear。実際の宛先は evil.example"),
    # §9.6 の 7: 権威部に `\` があればクライアントで読みが割れるので不（規則 4）
    ("fix_backslash_userinfo_requests", 'requests.get("http://evil.example\\\\@localhost/x")', "不", "net_host_unknown",
     "triage U36 反例 (c): urllib3 は evil.example、urlparse / httpx は localhost と読む。§9.6 の 7 で不"),
    ("fix_backslash_host_first", 'requests.get("http://localhost\\\\@evil.example/x")', "不", "net_host_unknown",
     "§9.6 の 7: `\\` の位置が逆でも読みが割れる（urllib3 は localhost、urlparse は evil.example）ので不"),
    # 取り出した host が空（userinfo だけ）は読めない
    ("fix_userinfo_empty_host", 'httpx.get("http://user:pass@/x")', "不", "net_host_unknown",
     "§9.6 の 7: hostname が空なら宛先は読めない（今は user を外部 host と読む）"),
]

FIX_SRC = HEAD + "".join(_tool(t, call) for t, call, *_ in FIX_CASES)


@pytest.fixture(scope="module")
def fix_units(tmp_path_factory):
    return _units(tmp_path_factory, "u36_fix", {"server.py": FIX_SRC})


@pytest.mark.parametrize("tool,call,want,reason,why", FIX_CASES, ids=[c[0] for c in FIX_CASES])
def test_fix_authority(fix_units, tool, call, want, reason, why):
    _check(fix_units, tool, want, reason)


# §9.6 の 7 / triage U36「別件: `://` 側の分岐の ValueError」: 閉じない角括弧で木全体が落ちてはならず、
# その宛先は読めない（不）。同じ木の他のツールの判定は残る。
CRASH_SRC = HEAD + _tool("fix_unbalanced_no_path", 'httpx.get("http://[::1")') + _tool(
    "other_external", 'httpx.get("https://api.example.com/x")'
)


def test_fix_unbalanced_bracket_does_not_fail_tree(tmp_path_factory):
    """triage U36 / verify R3d-r6-1: `http://[::1` は urlparse が ValueError。§9.6 の 7 で不、木は落ちない。"""
    units = _units(tmp_path_factory, "u36_crash", {"server.py": CRASH_SRC})
    _check(units, "fix_unbalanced_no_path", "不", "net_host_unknown")
    _check(units, "other_external", "矛", "net_external_host")


# ---------------------------------------------------------------------------
# 壊してはいけない挙動（今も通る。直した後も通らなければならない）
# ---------------------------------------------------------------------------

KEEP_CASES = [
    # 所見の対照（パスが無いと urlparse の枝を通って今も 内）
    ("keep_ipv6_no_path", 'httpx.get("http://[::1]:8080")', "内", None, "R3d-r6-1 対照"),
    ("keep_userinfo_no_path", 'httpx.get("http://user:pass@localhost:8080")', "内", None, "R3d-r6-1 対照"),
    ("keep_ipv4_port", 'httpx.get("http://127.0.0.1:8080/x")', "内", None, "R3d-r6-1 対照"),
    # 今正しく判定できている local の形
    ("keep_localhost_port", 'httpx.get("http://localhost:8080/x")', "内", None, "§7.3 表の d3_net_localhost と同形"),
    ("keep_private", 'httpx.get("http://192.168.1.10/x")', "内", None, "§7.3 private"),
    ("keep_ipv6_loopback_no_port", 'httpx.get("http://[::1]/x")', "内", None, "§7.3 loopback"),
    ("keep_dot_local", 'httpx.get("http://printer.local/x")', "内", None, "§7.3（実装の .local）"),
    # triage U36 反例 (a): 角括弧無しの裸 IPv6。素朴な urlparse('//'+c) だと fe80 → 矛 / ::1 → 不 に退行する
    ("keep_bare_ipv6_linklocal", 'httpx.get("http://fe80::1/x")', "内", None, "triage U36 (a): IP リテラルを先に試す"),
    ("keep_bare_ipv6_loopback", 'httpx.get("http://::1/x")', "内", None, "triage U36 (a): IP リテラルを先に試す"),
    # 外部のまま（userinfo による偽装を含む）
    ("keep_external_userinfo", 'httpx.get("http://user:pass@api.example.com/x")', "矛", "net_external_host",
     "triage U36: user:pass@api.example.com は external のまま"),
    ("keep_external_userinfo_port", 'httpx.get("http://user@evil.example:80/x")', "矛", "net_external_host",
     "triage U36: user@evil.example:80 は external のまま"),
    ("keep_userinfo_localhost_spoof", 'httpx.get("http://localhost@evil.example/x")', "矛", "net_external_host",
     "RFC 3986: userinfo の localhost は宛先ではない"),
    ("keep_external_port", 'httpx.get("https://api.example.com:8443/x")', "矛", "net_external_host", "§7.3 外部"),
    ("keep_external_fqdn", 'httpx.get("https://kapi.kakao.com/v1/x")', "矛", "net_external_host",
     "D56 の手検証の本物の FQDN"),
    ("keep_ipv4_mapped_external", 'httpx.get("http://[::ffff:8.8.8.8]/x")', "矛", "net_external_host",
     "triage U36: IPv4 写像は写像先で分類（外部）"),
    ("keep_localhost_prefix_external", 'httpx.get("http://localhost.evil.example/x")', "矛", "net_external_host",
     "末尾ドットの処理が名前の前方一致に化けない"),
    ("keep_localhost_prefix_trailing_dot", 'httpx.get("http://localhost.example./x")', "矛", "net_external_host",
     "§9.6 の 7: 末尾ドットを落としても localhost.example は外部"),
    # MODEL の宛先（定数でない）は今どおり
    ("keep_model_host", 'httpx.get(f"http://{p}/x")', "矛", "net_model_host", "§7.3 MODEL の宛先"),
]

# 「内に落ちてはならない」だけを固定する形（今は 矛。直した後は 不 または 矛）
KEEP_NOT_LOCAL = [
    ("keep_nl_backslash_userinfo_requests", 'requests.get("http://evil.example\\\\@localhost/x")',
     "triage U36 (c): urlparse / httpx の読み（localhost）で 内 にすると誤 clear（urllib3 は evil.example に接続）"),
    ("keep_nl_backslash_host_first", 'requests.get("http://localhost\\\\@evil.example/x")',
     "§9.6 の 7: `\\` のある権威部は 内 にしない（urlparse は evil.example と読む）"),
    ("keep_nl_ip_trailing_dot", 'httpx.get("http://127.0.0.1./x")',
     "triage U36 (d): IP の解釈には rstrip を使わない（127.0.0.1. は IP リテラルではない）"),
]

KEEP_SRC = HEAD + "".join(_tool(t, call) for t, call, *_ in KEEP_CASES) + "".join(
    _tool(t, call) for t, call, _ in KEEP_NOT_LOCAL
)


@pytest.fixture(scope="module")
def keep_units(tmp_path_factory):
    return _units(tmp_path_factory, "u36_keep", {"server.py": KEEP_SRC})


@pytest.mark.parametrize("tool,call,want,reason,why", KEEP_CASES, ids=[c[0] for c in KEEP_CASES])
def test_keep_authority(keep_units, tool, call, want, reason, why):
    _check(keep_units, tool, want, reason)


@pytest.mark.parametrize("tool,call,why", KEEP_NOT_LOCAL, ids=[c[0] for c in KEEP_NOT_LOCAL])
def test_keep_not_local(keep_units, tool, call, why):
    u = keep_units[tool]
    assert _status(u) != "内", f"{tool}: 内 に落ちた（誤 clear）notes={_net_notes(u)}"


# triage U36 反例 (b): 閉じない角括弧 + パス。素朴な直し方（urlparse('//'+c)）だと ValueError で木全体が落ちる。
# 他の KEEP を巻き込まないよう別の木に置く。
UNBALANCED_SRC = HEAD + _tool("keep_unbalanced_bracket_path", 'httpx.get("http://[::1/x")') + _tool(
    "other_localhost", 'httpx.get("http://localhost:8080/x")'
)


def test_keep_unbalanced_bracket_path(tmp_path_factory):
    """triage U36 (b): `http://[::1/x` は角括弧を外した ::1 を IP リテラルとして先に読み 内。木は落ちない。"""
    units = _units(tmp_path_factory, "u36_unbalanced", {"server.py": UNBALANCED_SRC})
    _check(units, "keep_unbalanced_bracket_path", "内", None)
    _check(units, "other_localhost", "内", None)


# §9.6 の 7 / triage U36:「`_split_url` は変えない」。SSRF の座標 url.host は権威部全体のまま。
@pytest.mark.parametrize(
    "tool,const",
    [
        ("fix_userinfo_localhost_port", "user:pass@localhost:8080"),
        ("fix_ipv6_loopback_port", "[::1]:8080"),
        ("fix_userinfo_ipv4", "admin@127.0.0.1"),
        ("fix_trailing_dot", "localhost."),
    ],
)
def test_keep_url_host_slot_is_whole_authority(fix_units, tool, const):
    assert _host_consts(fix_units[tool]) == [const], _host_consts(fix_units[tool])


def test_premise_declarations(fix_units, keep_units):
    """前提: 全ツールで openWorldHint: false が読めていて、NET の効果が 1 つある。"""
    for units in (fix_units, keep_units):
        for name, u in units.items():
            dk = u["D_kind"]
            assert not dk.get("unknown"), f"{name}: 注釈が読めていない"
            assert dk.get("closed_world") is True, (name, dk)
            assert len([e for e in u["effects"] if e["kind"] == "NET"]) == 1, (name, u["effects"])


def test_other_declarations_silent(fix_units, keep_units):
    """D3 だけの宣言のツールで、D1 / D2 / D4 の注記が出ない（宛先の読み方は D3 にだけ効く）。"""
    for units in (fix_units, keep_units):
        for name, u in units.items():
            for other in ("D1", "D2", "D4"):
                assert _status(u, other) == "内", (name, other)
