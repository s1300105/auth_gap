"""D64 / U09 の 3 巡目（再点検の所見 U09-R1）の反例と対照。

**期待値は authgap/ を直す前に書いた（D64 / U09 の 3 巡目）。** 観測は再点検の再現の木
（scratchpad/d64recheck/U09/x/ の n4 と対照 n4c）を元にしたもので、期待値は所見の expected（Python の
star import の意味: `from M import *` は `__all__` が無ければ M の名前空間の名前をすべて持ち込み、M 自身が
star import で持ち込んだ名前も含む）と、D17 改訂 2（木の中で再束縛される名前は定数として読まない）から導いた。
v2 / v3 の件数には合わせていない。

- U09-R1: 互いに star import する 2 モジュール（pkg.b ↔ pkg.c）の循環があるとき、`from pkg.b import *` が
  持ち込む `config`（pkg.c の `from pkg import config`）への `config.MODE = v` は pkg.config.MODE の再束縛。
  判定は**無関係なファイル（aaa.py）の有無やファイル名の並び順に依存してはならない**（n4 と n4c が同じ判定）。

- `test_fix_*`: 直す前の解析器で**落ちる**（所見の expected）。
- `test_keep_*`: 直した後も壊してはいけない対照。

観測は manifest の効果行（fs_mode / destructive）と行の注記（`contradiction:*` / `contradiction_unknown:*`）だけで行う。
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


def _brief(u: dict) -> list:
    return [(e["kind"], e.get("resolution"), e.get("fs_mode"), e.get("destructive")) for e in u["effects"]]


def _status(u: dict, kind: str, decl: str) -> str:
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（効果行が消えている）: {_brief(u)}"
    notes = [n for r in rows for n in r.get("notes", [])]
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方: {notes}"
    if hit:
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, kind: str, decl: str) -> set[str]:
    out = set()
    for r in u["rows"]:
        if r["kind"] != kind:
            continue
        for n in r.get("notes", []):
            for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
                if n.startswith(pre):
                    out.add(n[len(pre):])
    return out


def _fs_effects(u: dict) -> list[dict]:
    es = [e for e in u["effects"] if e["kind"] == "FS_WRITE"]
    assert es, _brief(u)
    return es


CONFIG = 'MODE = "a"\n'

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

WRITER = "from pkg.b import *\n\n\ndef set_mode(v):\n    config.MODE = v\n"
READER = "from pkg.b import *\n\n\ndef show():\n    return config.MODE\n"


def _cycle(admin: str, extra: dict[str, str]) -> dict[str, str]:
    """再点検の n4c: pkg.b ↔ pkg.c が互いに star import し、pkg.c が `from pkg import config`。"""
    files = {
        "pkg/__init__.py": "",
        "pkg/config.py": CONFIG,
        "pkg/b.py": "from pkg.c import *\n",
        "pkg/c.py": "from pkg.b import *\nfrom pkg import config\n",
        "pkg/admin.py": admin,
        "pkg/server.py": SERVER,
    }
    files.update(extra)
    return files


def _cycle3(admin: str, extra: dict[str, str]) -> dict[str, str]:
    """3 つの循環 b → c → d → b（`config` は d が持ち込む）。"""
    files = {
        "pkg/__init__.py": "",
        "pkg/config.py": CONFIG,
        "pkg/b.py": "from pkg.c import *\n",
        "pkg/c.py": "from pkg.d import *\n",
        "pkg/d.py": "from pkg.b import *\nfrom pkg import config\n",
        "pkg/admin.py": admin,
        "pkg/server.py": SERVER,
    }
    files.update(extra)
    return files


UNRELATED_C = "from pkg.c import *\n\nX = 1\n"
UNRELATED_B = "from pkg.b import *\n\nX = 1\n"
UNRELATED_D = "from pkg.d import *\n\nX = 1\n"

TREES = {
    # 再点検の n4c（対照: 無関係なファイルなし。直す前も矛）
    "n4c": _cycle(WRITER, {}),
    # 再点検の n4（無関係な aaa.py が循環の片側を先に star import する）
    "n4": _cycle(WRITER, {"pkg/aaa.py": UNRELATED_C}),
    # 同じ無関係なファイルが後ろに並ぶ名前
    "n4_zzz": _cycle(WRITER, {"pkg/zzz.py": UNRELATED_C}),
    # 無関係なファイルが循環のもう片側（pkg.b）を star import する
    "n4_aaa_b": _cycle(WRITER, {"pkg/aaa.py": UNRELATED_B}),
    # 無関係なファイルが 2 つ（両側から）
    "n4_both": _cycle(WRITER, {"pkg/aaa.py": UNRELATED_C, "pkg/aab.py": UNRELATED_B}),
    # 3 つの循環
    "c3": _cycle3(WRITER, {}),
    "c3_aaa_c": _cycle3(WRITER, {"pkg/aaa.py": UNRELATED_C}),
    "c3_aaa_d": _cycle3(WRITER, {"pkg/aaa.py": UNRELATED_D}),
    # 対照: 同じ循環で `config` を読むだけ（書き換えは無い）
    "n4_read_only": _cycle(READER, {"pkg/aaa.py": UNRELATED_C}),
    "n4c_read_only": _cycle(READER, {}),
}

FIX_TREES = ["n4c", "n4", "n4_zzz", "n4_aaa_b", "n4_both", "c3", "c3_aaa_c", "c3_aaa_d"]


@pytest.fixture(scope="module")
def r1(tmp_path_factory):
    return {k: _units(tmp_path_factory, f"u09r3_{k}", v) for k, v in TREES.items()}


@pytest.mark.parametrize("tree", FIX_TREES)
@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_r1_star_cycle_alias_store(r1, tree, tool):
    """U09-R1: star import の循環を通って来た `config` への `config.MODE = v` は再束縛 → mode 不明で D2 矛。
    無関係なファイルの有無・名前（並び順）で判定が変わらない。"""
    u = r1[tree][tool]
    for e in _fs_effects(u):
        assert e.get("destructive") is not False and e.get("fs_mode") != "a", f"{tree}/{tool}: {_brief(u)}"
    got = _status(u, "FS_WRITE", "D2")
    assert got == "矛", f"{tree}/{tool}: D2 {got}（期待 矛）effects={_brief(u)}"
    assert "fs_unknown_model_path" in _reasons(u, "FS_WRITE", "D2"), _reasons(u, "FS_WRITE", "D2")


@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_fix_r1_same_verdict_with_and_without_unrelated_file(r1, tool):
    """U09-R1: n4 と n4c（違いは無関係な aaa.py だけ）は同じ効果行・同じ判定。"""
    a, b = r1["n4"][tool], r1["n4c"][tool]
    assert _brief(a) == _brief(b)
    assert _status(a, "FS_WRITE", "D2") == _status(b, "FS_WRITE", "D2")
    assert _reasons(a, "FS_WRITE", "D2") == _reasons(b, "FS_WRITE", "D2")


@pytest.mark.parametrize("tree", ["n4_read_only", "n4c_read_only"])
@pytest.mark.parametrize("tool", ["append_attr", "append_from"])
def test_keep_r1_star_cycle_read_only(r1, tree, tool):
    """対照: 循環を通って来た `config` の属性を読むだけなら書き換えは無い → "a" のまま D2 内。"""
    u = r1[tree][tool]
    es = _fs_effects(u)
    assert all(e.get("fs_mode") == "a" and e.get("destructive") is False for e in es), _brief(u)
    assert _status(u, "FS_WRITE", "D2") == "内", _brief(u)
