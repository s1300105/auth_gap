"""D64 / U09: モジュール・クラス水準の値の読み（`_module_value`）。所見 R1-r4-1, R4-r2-7, R1-r4-11, R1-r4-13, R1-r3-9。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U09）。** v2 / v3 の件数には合わせず、
Python の束縛の意味（import・`global`・タプル代入・クラス本体）、D17（モジュール水準の名前は束縛の
flow-insensitive な join。改訂 2〜5: 再束縛される名前は型と主体を保って確度を opaque、コンテナ / オブジェクトは
`_opaque_deep`、opaque の定数は読まない）、D35 (a)（`Obj ⊔ None = Obj`）、D61 G3（再公開の健全性の条件）、
§7.1 / §7.2 / §9.4（`docs/contradiction_principles.md`）と、D64 の U09 行・`evidence/review/triage.json` の
U09 fix_outline から導いた。

- `test_fix_*`（今の解析器で**落ちる**）: 所見の expected。
- `test_keep_*`（今の解析器で**通る**）: 検証役の反例（素朴な直し方で誤 clear になる形）、所見の対照、
  今正しく判定できている形。直した後もこれが通らなければならない。

単位ごとの規則:

1. R1-r4-1 モジュール別名の属性 `config.X` / `cfg.X`: from-import の対照と同じ出力。反例は検証役 p1 の
   f1_shadow / f1_dynattr / f1_condimport / f1_local と、条件 (iv)「木のどこかに」「他モジュールからの
   `config.X = ...`」「元のモジュールでの `global` 再束縛」の変種。
2. R4-r2-7 関数内の `global` 束縛: 右辺を候補に入れ、型を保つ join（`Obj ⊔ Unknown` で型を捨てない）。
   反例 r7_unknown_join（purge_y）、r7_local_shadow、r7_multitype（2 型の受け手の分割降下）。
3. R1-r4-11 `pkg/__init__.py` の再公開: 対照と同じ出力。反例 cx11・try/except の予備・import の後の代入・
   元のモジュールの `global`・他モジュールからの `pkg.ROOT = v`。
4. R1-r4-13 タプル代入: 同じ長さの Tuple / List だけ位置で対応（入れ子は再帰）、Starred があれば読まない。
   今ある誤 clear（swapped / plain_then_tuple）は直す側。
5. R1-r3-9 クラス属性 `Cls.ATTR`: **学生の決定は規則 B**（型と主体だけ付け、確度は常に opaque。定数でも
   resolved にしない）。受け手の NET / DB 行は出るようになる（落ちる側）。定数の連結・mode は今の
   opaque のまま（通る側）。規則 A（定数を resolved）の期待は書かない。

新しい注記・鍵は仮定しない。観測は manifest の効果行（kind / slots の prin・prov / http_method /
sql_head / fs_mode / destructive）と行の注記（`contradiction:*` / `contradiction_reason:*` /
`contradiction_unknown:*`）だけで行う。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

HDR = 'from mcp.server.fastmcp import FastMCP\n\nmcp = FastMCP("t")\n\n'


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
        out.append((e["kind"], e["site"], e.get("resolution"), e.get("http_method"), e.get("sql_head"),
                    e.get("fs_mode"), e.get("destructive"), slots))
    return out


def _notes(u: dict, kind: str) -> list[str]:
    return [n for r in u["rows"] if r["kind"] == kind for n in r.get("notes", [])]


def _status(u: dict, kind: str, decl: str) -> str:
    """`kind` の行の宣言 `decl` の判定: 矛 / 不 / 内（tests/test_contradiction_principles.py と同じ読み方）。"""
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
    """反例の共通の読み: 値が分からない形を「内」（矛盾なし）にしない。"""
    got = _status(u, kind, decl)
    assert got in ("矛", "不"), f"{u['unit']['qualname']} {decl}: 内（誤 clear）notes={_notes(u, kind)} effects={_brief(u)}"


def _resolved_consts(v: dict) -> set:
    """値の形の中で確度 resolved の定数（Str の要素を含む）。"""
    out = set()
    if not v:
        return out
    shape = v.get("shape") or {}
    if v.get("prov") == "resolved" and "const" in shape:
        out.add(shape["const"])
    for it in shape.get("items") or []:
        out |= _resolved_consts(it)
    return out


def _path_not_resolved(u: dict) -> None:
    for e in _effects(u, "FS_WRITE"):
        s = _slot(e, "path")
        assert s.get("prov") != "resolved", f"{u['unit']['qualname']}: path が resolved: {_brief(u)}"


def _no_append_mode(u: dict) -> None:
    """mode が分からない形で `"a"`（destructive=False）を読んでいない。"""
    for e in _effects(u, "FS_WRITE"):
        assert e.get("destructive") is not False and e.get("fs_mode") != "a", f"{u['unit']['qualname']}: {_brief(u)}"


# ===========================================================================
# 1. R1-r4-1 モジュール別名の属性 `config.X` / `cfg.X`
# ===========================================================================

A_CONFIG_OBJ = '''import sqlite3

import httpx

ROOT = "/srv/data"
client = httpx.Client(base_url="https://api.example.com")
conn = sqlite3.connect("/tmp/x.db")
'''

A_SERVER_OBJ = '''from mcp.server.fastmcp import FastMCP

import pkg.config as cfg
from . import config
from .config import ROOT, client, conn

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def write_attr(name: str, text: str) -> str:
    with open(config.ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_alias_attr(name: str, text: str) -> str:
    with open(cfg.ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_from_control(name: str, text: str) -> str:
    with open(ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_attr(item: str) -> str:
    config.client.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_from_control(item: str) -> str:
    client.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def db_attr(q: str) -> str:
    cfg.conn.execute("DELETE FROM t WHERE id = " + q)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def db_from_control(q: str) -> str:
    conn.execute("DELETE FROM t WHERE id = " + q)
    return "ok"
'''

A_CONFIG_CONST = '''SQL_PURGE = "DELETE FROM sessions WHERE expired = 1"
METHOD = "DELETE"
MODE = "a"
'''

A_SERVER_CONST = '''import sqlite3

import requests
from mcp.server.fastmcp import FastMCP

from . import config
from .config import SQL_PURGE, METHOD, MODE
import pkg.config as cfg

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_via_module_attr(db: str) -> str:
    conn = sqlite3.connect(db)
    conn.execute(config.SQL_PURGE)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_via_module_alias(db: str) -> str:
    conn = sqlite3.connect(db)
    conn.execute(cfg.SQL_PURGE)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def delete_via_module_attr(url: str) -> str:
    requests.request(config.METHOD, url)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def append_via_module_attr(path: str, text: str) -> str:
    with open(path, config.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def control_purge_from_import(db: str) -> str:
    conn = sqlite3.connect(db)
    conn.execute(SQL_PURGE)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def control_delete_from_import(url: str) -> str:
    requests.request(METHOD, url)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def control_append_from_import(path: str, text: str) -> str:
    with open(path, MODE) as fh:
        fh.write(text)
    return "ok"
'''

A_CONFIG_RM = 'ROOT = "/srv/data"\nMODE = "a"\n'

#: 反例 f1_shadow（検証役 p1）: 親パッケージが同じ葉の名前 `config` を値として束縛し、pkg/config.py も在る。
A_SHADOW_INIT = '''import json
import os


def _load():
    return json.loads(os.environ.get("APP_CONFIG", "{}"))


config = _load()
'''

A_SHADOW_SERVER = HDR.replace("\n\nmcp =", "\n\nfrom . import config\n\nmcp =") + '''
@mcp.tool(annotations={"destructiveHint": False})
def write_shadowed_attr(name: str, text: str) -> str:
    with open(config.ROOT + "/" + name, config.MODE) as fh:
        fh.write(text)
    return "ok"
'''

#: 反例 f1_dynattr（検証役 p1）: 非定数名の属性書き換え（属性読みは遅延束縛）。
A_DYN_SERVER = HDR.replace("\n\nmcp =", "\n\nfrom . import config\n\nmcp =") + '''
@mcp.tool(annotations={"readOnlyHint": True})
def set_option(key: str, value: str) -> str:
    setattr(config, key, value)
    vars(config)[key] = value
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_after_dynamic(name: str, text: str) -> str:
    with open(config.ROOT + "/" + name, config.MODE) as fh:
        fh.write(text)
    return "ok"
'''

#: 条件 (iv) の「木のどこかに」: 非定数名の setattr が**別のモジュール**にある。
A_DYN_OTHER_ADMIN = '''from pkg import config


def set_option(key, value):
    setattr(config, key, value)
'''

A_READ_SERVER = HDR.replace("\n\nmcp =", "\n\nfrom . import config\n\nmcp =") + '''
@mcp.tool(annotations={"destructiveHint": False})
def write_config_attr(name: str, text: str) -> str:
    with open(config.ROOT + "/" + name, config.MODE) as fh:
        fh.write(text)
    return "ok"
'''

#: 他モジュールからの定数名の属性書き込み `config.MODE = v`（D17 改訂 2 の `_tree_attr_writes`）。
A_WRITE_OTHER_ADMIN = '''from pkg import config


def set_mode(v):
    config.MODE = v
    config.ROOT = v
'''

#: 元のモジュールでの `global` 再束縛（D17 改訂 2）。
A_CONFIG_GLOBAL = '''ROOT = "/srv/data"
MODE = "a"


def configure(root, mode):
    global ROOT, MODE
    ROOT = root
    MODE = mode
'''

#: 反例 f1_condimport（検証役 p1）: 読む側で別名が 2 回束縛される（try の予備）。
A_COND_SERVER = '''import os
import types

from mcp.server.fastmcp import FastMCP

try:
    from . import config
except ImportError:
    config = types.SimpleNamespace(ROOT=os.environ["ROOT"], MODE="w")

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def write_cond(name: str, text: str) -> str:
    with open(config.ROOT + "/" + name, config.MODE) as fh:
        fh.write(text)
    return "ok"
'''

#: 反例 f1_local（検証役 p1）と、局所の同名が MODEL 由来の変種（素朴に別名を読むと MODEL → OP の誤 clear）。
A_LOCAL_SERVER = '''import json

from mcp.server.fastmcp import FastMCP

from . import config

mcp = FastMCP("t")


def load_user_config(name):
    return None


@mcp.tool(annotations={"destructiveHint": False})
def write_local_shadow(name: str, text: str) -> str:
    config = load_user_config(name)
    with open(config.ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_local_model_config(spec: str) -> str:
    config = json.loads(spec)
    with open(config.ROOT, "w") as fh:
        fh.write("x")
    return "ok"
'''


@pytest.fixture(scope="module")
def a_obj(tmp_path_factory):
    return _units(tmp_path_factory, "u09_a_obj",
                  {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_OBJ, "pkg/server.py": A_SERVER_OBJ})


@pytest.fixture(scope="module")
def a_const(tmp_path_factory):
    return _units(tmp_path_factory, "u09_a_const",
                  {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_CONST, "pkg/server.py": A_SERVER_CONST})


@pytest.fixture(scope="module")
def a_counter(tmp_path_factory):
    """反例の木（互いに干渉しないよう木を分ける）。"""
    trees = {
        "shadow": {"pkg/__init__.py": A_SHADOW_INIT, "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_SHADOW_SERVER},
        "dyn": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_DYN_SERVER},
        "dyn_other": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_READ_SERVER,
                      "pkg/admin.py": A_DYN_OTHER_ADMIN},
        "write_other": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_READ_SERVER,
                        "pkg/admin.py": A_WRITE_OTHER_ADMIN},
        "origin_global": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_GLOBAL, "pkg/server.py": A_READ_SERVER},
        "cond": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_COND_SERVER},
        "local": {"pkg/__init__.py": "", "pkg/config.py": A_CONFIG_RM, "pkg/server.py": A_LOCAL_SERVER},
    }
    return {k: _units(tmp_path_factory, f"u09_a_{k}", v) for k, v in trees.items()}


# --- 直す側（R1-r4-1 の expected）---

@pytest.mark.parametrize("tool", ["write_attr", "write_alias_attr"])
def test_fix_r1_r4_1_module_attr_path_const(a_obj, tool):
    """R1-r4-1: `config.ROOT` / `cfg.ROOT` は from-import と同じ束縛 → path MODEL/resolved → §7.2 書き出しで D2 矛。"""
    u = a_obj[tool]
    for e in _effects(u, "FS_WRITE"):
        s = _slot(e, "path")
        assert (s.get("prin"), s.get("prov")) == ("MODEL", "resolved"), _brief(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_fix_r1_r4_1_module_attr_client_receiver(a_obj):
    """R1-r4-1: `config.client`（モジュール水準の httpx.Client）の受け手の型 → NET 行、DELETE → §7.1 で D1 矛。"""
    u = a_obj["net_attr"]
    assert any(e.get("http_method") == "DELETE" for e in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_fix_r1_r4_1_module_attr_conn_receiver(a_obj):
    """R1-r4-1: `cfg.conn`（モジュール水準の sqlite3 接続）の受け手の型 → DB 行、SQL が MODEL → §9.4 の 2 で D1 矛。"""
    u = a_obj["db_attr"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")


@pytest.mark.parametrize("tool", ["purge_via_module_attr", "purge_via_module_alias"])
def test_fix_r1_r4_1_module_attr_sql_const(a_const, tool):
    """R1-r4-1: `config.SQL_PURGE` は定数の SQL → OP/resolved、先頭語 DELETE → §7.1 で D1 矛（db_modify）。"""
    u = a_const[tool]
    es = _effects(u, "DB")
    assert es, _brief(u)
    for e in es:
        s = _slot(e, "sql")
        assert (s.get("prov"), (s.get("shape") or {}).get("const")) == (
            "resolved", "DELETE FROM sessions WHERE expired = 1"), _brief(u)
        assert e.get("sql_head") == "DELETE", _brief(u)
    _check(u, "DB", "D1", "矛", "db_modify")


def test_fix_r1_r4_1_module_attr_method_const(a_const):
    """R1-r4-1: `config.METHOD` は定数 "DELETE" → http_method=DELETE → §7.1 で D1 矛（net_modify）。"""
    u = a_const["delete_via_module_attr"]
    assert any(e.get("http_method") == "DELETE" for e in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_fix_r1_r4_1_module_attr_mode_const(a_const):
    """R1-r4-1: `config.MODE` は定数 "a" → fs_mode=a / destructive=False → §7.2 追記型で D2 内（今は mode 不明の誤警報）。"""
    u = a_const["append_via_module_attr"]
    es = _effects(u, "FS_WRITE")
    assert es and all(e.get("fs_mode") == "a" and e.get("destructive") is False for e in es), _brief(u)
    _check(u, "FS_WRITE", "D2", "内")


# --- 壊さない側（対照と反例）---

def test_keep_r1_r4_1_from_import_controls(a_obj, a_const):
    """R1-r4-1 の対照: from-import 形は今も期待どおり（直した後の属性形はこれと同じ出力になる）。"""
    _check(a_obj["write_from_control"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")
    _check(a_obj["net_from_control"], "NET", "D1", "矛", "net_modify")
    _check(a_obj["db_from_control"], "DB", "D1", "矛")
    _check(a_const["control_purge_from_import"], "DB", "D1", "矛", "db_modify")
    _check(a_const["control_delete_from_import"], "NET", "D1", "矛", "net_modify")
    _check(a_const["control_append_from_import"], "FS_WRITE", "D2", "内")


@pytest.mark.parametrize("tree,tool", [
    ("shadow", "write_shadowed_attr"),      # 反例 f1_shadow: 条件 (iii) 親パッケージの同名
    ("dyn", "write_after_dynamic"),         # 反例 f1_dynattr: 条件 (iv) setattr / vars で "*"
    ("dyn_other", "write_config_attr"),     # 条件 (iv) の「木のどこかに」: setattr が別モジュール
    ("write_other", "write_config_attr"),   # 他モジュールからの `config.MODE = v`（D17 改訂 2）
    ("origin_global", "write_config_attr"),  # 元のモジュールでの `global MODE`（D17 改訂 2）
    ("cond", "write_cond"),                 # 反例 f1_condimport: 条件 (ii) 束縛がちょうど 1 つ
])
def test_keep_r1_r4_1_counterexamples_stay_opaque(a_counter, tree, tool):
    """R1-r4-1 の検証役の反例（p1 で内 = 誤 clear になった形）: ROOT / MODE を定数に決め打ちしない。"""
    u = a_counter[tree][tool]
    _path_not_resolved(u)
    _no_append_mode(u)
    _not_clear(u, "FS_WRITE", "D2")


def test_keep_r1_r4_1_local_shadow(a_counter):
    """R1-r4-1 の反例 f1_local: 局所の `config` は別名ではない（条件 (i)）。path は resolved にしない。"""
    u = a_counter["local"]["write_local_shadow"]
    _path_not_resolved(u)
    _check(u, "FS_WRITE", "D2", "不")


def test_keep_r1_r4_1_local_model_shadow(a_counter):
    """条件 (i) の変種: 局所の `config = json.loads(spec)` は MODEL 由来。別名を読むと path が OP に化ける（主体の誤 clear）。"""
    u = a_counter["local"]["write_local_model_config"]
    es = _effects(u, "FS_WRITE")
    assert es and all(_slot(e, "path").get("prin") == "MODEL" for e in es), _brief(u)
    _not_clear(u, "FS_WRITE", "D2")


# ===========================================================================
# 2. R4-r2-7 関数内の `global` 束縛
# ===========================================================================

B_GLOBAL = '''import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

_conn = None


def init_db() -> None:
    global _conn
    _conn = sqlite3.connect("/data/app.db")


def get_conn():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect("/data/app.db")
    return _conn


@mcp.tool(annotations={"readOnlyHint": True})
def purge_global(item_id: str) -> str:
    _conn.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_after_init(item_id: str) -> str:
    init_db()
    _conn.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_getter(item_id: str) -> str:
    get_conn().execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

#: 検証役の設計の確認（global_typed）: 変種 A（型は直下）と変種 B（型は注釈と global の書き込みにしか無い）。
B_TYPED = '''import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

_conn = sqlite3.connect("/data/app.db")


def reset_db() -> None:
    global _conn
    _conn = sqlite3.connect("/data/other.db")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_typed_global(item_id: str) -> str:
    _conn.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


_conn2: "sqlite3.Connection | None" = None


def init_db2() -> None:
    global _conn2
    _conn2 = sqlite3.connect("/data/app.db")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_annotated_none(item_id: str) -> str:
    init_db2()
    _conn2.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

#: 反例 r7_unknown_join（検証役）: 素の value_join で `Obj ⊔ Unknown = Unknown` にすると purge_y の行が消える。
B_UNKNOWN = '''import os
import sqlite3

from mcp.server.fastmcp import FastMCP
from somewhere import external_factory

mcp = FastMCP("t")

W = sqlite3.connect("/data/app.db")
if os.environ.get("EXT"):
    W = external_factory()

V = sqlite3.connect("/data/app.db")
if os.environ.get("OFF"):
    V = None

Y = sqlite3.connect("/data/app.db")


def swap():
    global Y
    Y = external_factory()


@mcp.tool(annotations={"readOnlyHint": True})
def purge_w(item_id: str) -> str:
    W.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_v(item_id: str) -> str:
    V.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_y(item_id: str) -> str:
    Y.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

#: 反例 r7_local_shadow（検証役）: 書き戻し (c) が呼び出し側の同名の局所を潰す形。右辺が仮引数の init_from も。
B_LOCAL = '''import sqlite3

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

_conn = None


def init_db() -> None:
    global _conn
    _conn = sqlite3.connect("/data/app.db")


def init_from(path: str) -> None:
    global _conn
    _conn = sqlite3.connect(path)


@mcp.tool(annotations={"readOnlyHint": True})
def local_shadow(item_id: str) -> str:
    _conn = httpx.Client()
    init_db()
    _conn.get("http://x/" + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def inline_global(item_id: str) -> str:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect("/data/app.db")
    _conn.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def after_init_from(item_id: str, path: str) -> str:
    init_from(path)
    _conn.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

#: 「確かめること」: 2 型以上の Obj になった受け手の分割降下（D35 (d)）と、後始末関数 `global X; X = None` との合流。
B_MULTI = '''import os
import sqlite3

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class Fake:
    def execute(self, sql):
        return None


X1 = sqlite3.connect("/data/app.db")
if os.environ.get("FAKE"):
    X1 = Fake()

X2 = sqlite3.connect("/data/app.db")
if os.environ.get("HTTP"):
    X2 = httpx.Client()

Y = sqlite3.connect("/data/app.db")


def swap():
    global Y
    Y = Fake()


Z2 = None


def init_real():
    global Z2
    Z2 = sqlite3.connect("/data/app.db")


def init_fake():
    global Z2
    Z2 = Fake()


C = None


def open_c():
    global C
    C = sqlite3.connect("/data/app.db")


def close_c():
    global C
    if C is not None:
        C.close()
    C = None


@mcp.tool(annotations={"readOnlyHint": True})
def purge_x1(item_id: str) -> str:
    X1.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_x2(item_id: str) -> str:
    X2.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_y(item_id: str) -> str:
    Y.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_z2(item_id: str) -> str:
    Z2.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_c(item_id: str) -> str:
    C.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''


@pytest.fixture(scope="module")
def b(tmp_path_factory):
    trees = {"global": B_GLOBAL, "typed": B_TYPED, "unknown": B_UNKNOWN, "local": B_LOCAL, "multi": B_MULTI}
    return {k: _units(tmp_path_factory, f"u09_b_{k}", {"server.py": v}) for k, v in trees.items()}


def _db_model_sql(u: dict) -> None:
    es = _effects(u, "DB")
    assert es, f"{u['unit']['qualname']}: DB 行が無い: {_brief(u)}"
    for e in es:
        s = _slot(e, "sql")
        # fix_outline の期待の細部: SQL の slot は MODEL/resolved（受け手の確度は slot に載らない）
        assert (s.get("prin"), s.get("prov")) == ("MODEL", "resolved"), _brief(u)
    # 理由コードは固定しない（U33 の §9.6 で MODEL の SQL の定数の先頭語 DELETE は db_modify になった）
    _check(u, "DB", "D1", "矛")


# --- 直す側 ---

@pytest.mark.parametrize("tree,tool", [
    ("global", "purge_global"),          # 所見: 候補が None だけで受け手の型が消える
    ("global", "purge_after_init"),      # 所見: 書き込みが実行経路上にあっても消える
    ("typed", "purge_annotated_none"),   # 検証役の変種 B: 型は注釈と global の書き込みにしか無い
    ("local", "after_init_from"),        # 右辺が被呼び出しの仮引数（右辺はその関数のスコープで評価）
    ("multi", "purge_z2"),               # 2 型（sqlite3 ⊔ 木内 Fake）: sqlite3 の経路の行を落とさない（D35 (d)）
    ("multi", "purge_c"),                # 後始末の `global C; C = None` との合流: Obj ⊔ None = Obj（D35 (a)）
])
def test_fix_r4_r2_7_global_rebinding_gives_receiver_type(b, tree, tool):
    """R4-r2-7: `global X; X = <ctor>()` の右辺を候補に入れ、型を保つ join → DB 行と D1 矛（SQL が MODEL。理由コードは U33 の §9.6 に従う）。"""
    _db_model_sql(b[tree][tool])


def test_fix_r4_r2_7_type_preserving_join_module_level(b):
    """R4-r2-7 (b) 型を保つ join: 直下の `W = connect(); if ...: W = external()` も Obj ⊔ Unknown で型を捨てない。

    fix_outline は同じ join を直下で書いた purge_w を「同じ族の既存の誤 clear」とし、検証役は `_module_value`
    の中の型を保つ join で一緒に直ると書いた（D17 改訂 4: 型と主体を保って確度だけ opaque）。
    """
    _db_model_sql(b["unknown"]["purge_w"])


# --- 壊さない側 ---

@pytest.mark.parametrize("tree,tool", [
    ("global", "purge_getter"),          # 所見の対照（getter 形は今も行が出る）
    ("typed", "purge_typed_global"),     # 変種 A: 型は直下、global で同じ型に再束縛
    ("unknown", "purge_v"),              # D35 (a) の対照: Obj ⊔ None
    ("unknown", "purge_y"),              # 反例 r7_unknown_join: global 側が Unknown でも型を捨てない
    ("local", "inline_global"),          # 同じ関数での global 束縛
    ("multi", "purge_x1"),               # 2 型の直下の join（木内 Fake）
    ("multi", "purge_x2"),               # 2 型の直下の join（外部 httpx）
    ("multi", "purge_y"),                # global で木内 Fake に差し替え: sqlite3 の経路を落とさない（D35 (d)）
])
def test_keep_r4_r2_7_rows_that_exist_now(b, tree, tool):
    """R4-r2-7 の反例と対照: 今 DB 行と D1 矛（SQL が MODEL。理由コードは U33 の §9.6 に従う）が出ている形は、直した後も出る。"""
    _db_model_sql(b[tree][tool])


def test_keep_r4_r2_7_local_shadow_not_overwritten(b):
    """反例 r7_local_shadow: 局所 `_conn = httpx.Client()` は init_db() の global 書き込みと別の変数。

    書き戻し (c) を入れても、呼び出し側の同名の局所（global 宣言なし）を sqlite3 の接続で潰さない。
    潰すと `.get` の NET 行が消える（誤 clear）。
    """
    u = b["local"]["local_shadow"]
    assert any(e.get("http_method") == "GET" for e in _effects(u, "NET")), _brief(u)
    assert not _effects(u, "DB"), _brief(u)


# ===========================================================================
# 3. R1-r4-11 `pkg/__init__.py` の再公開
# ===========================================================================

C_CONFIG = '''import httpx

ROOT = "/srv/data"
client = httpx.Client(base_url="https://api.example.com")
'''

C_MAIN = '''from mcp.server.fastmcp import FastMCP

from pkg import ROOT, client
from pkg.config import ROOT as ROOT_DIRECT, client as client_direct

mcp = FastMCP("t")


@mcp.tool(annotations={"destructiveHint": False})
def write_reexport(name: str, text: str) -> str:
    with open(ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_direct_control(name: str, text: str) -> str:
    with open(ROOT_DIRECT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_reexport(item: str) -> str:
    client.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_direct_control(item: str) -> str:
    client_direct.request("DELETE", "/items/" + item)
    return "ok"
'''

C_READ_MAIN = HDR.replace("\n\nmcp =", "\n\nfrom pkg import MODE, ROOT\n\nmcp =") + '''
@mcp.tool(annotations={"destructiveHint": False})
def write_reexport_rebound(name: str, text: str) -> str:
    with open(ROOT + "/" + name, MODE) as fh:
        fh.write(text)
    return "ok"
'''

C_ROOT_CFG = 'ROOT = "/srv/data"\nMODE = "a"\n'
C_PLAIN_INIT = "from .config import MODE, ROOT\n"

#: 反例 cx11（検証役）: 再公開するモジュールでの `global ROOT; ROOT = r`（MODE も同じ形で足した）。
C_CX11_INIT = '''from .config import MODE, ROOT


def set_root(r, m):
    global ROOT, MODE
    ROOT = r
    MODE = m
'''

#: try/except の予備 import（fix_outline が反例テストに入れると指定）。
C_TRY_INIT = '''import os

try:
    from .config import MODE, ROOT
except ImportError:
    ROOT = os.environ.get("APP_ROOT", "/")
    MODE = os.environ.get("APP_MODE", "w")
'''

#: import の後の代入（束縛がちょうど 1 つでない）。
C_AFTER_INIT = '''import os

from .config import MODE, ROOT

ROOT = os.environ.get("APP_ROOT") or ROOT
MODE = os.environ.get("APP_MODE") or MODE
'''

#: 元のモジュールでの `global` 再束縛（rebound の判定は再公開元にも掛ける）。
C_ORIGIN_CONFIG = '''ROOT = "/srv/data"
MODE = "a"


def set_root(r, m):
    global ROOT, MODE
    ROOT = r
    MODE = m
'''

#: 他モジュールからの `pkg.ROOT = v`（両モジュールに `_tree_attr_writes` を掛ける）。
C_OTHER_ADMIN = '''import pkg


def set_root(v):
    pkg.ROOT = v
    pkg.MODE = v
'''


@pytest.fixture(scope="module")
def c_reexport(tmp_path_factory):
    return _units(tmp_path_factory, "u09_c_reexport",
                  {"pkg/__init__.py": "from .config import ROOT, client\n", "pkg/config.py": C_CONFIG, "main.py": C_MAIN})


@pytest.fixture(scope="module")
def c_counter(tmp_path_factory):
    trees = {
        "cx11": {"pkg/__init__.py": C_CX11_INIT, "pkg/config.py": C_ROOT_CFG, "main.py": C_READ_MAIN},
        "try": {"pkg/__init__.py": C_TRY_INIT, "pkg/config.py": C_ROOT_CFG, "main.py": C_READ_MAIN},
        "after": {"pkg/__init__.py": C_AFTER_INIT, "pkg/config.py": C_ROOT_CFG, "main.py": C_READ_MAIN},
        "origin": {"pkg/__init__.py": C_PLAIN_INIT, "pkg/config.py": C_ORIGIN_CONFIG, "main.py": C_READ_MAIN},
        "other": {"pkg/__init__.py": C_PLAIN_INIT, "pkg/config.py": C_ROOT_CFG, "main.py": C_READ_MAIN,
                  "admin.py": C_OTHER_ADMIN},
    }
    return {k: _units(tmp_path_factory, f"u09_c_{k}", v) for k, v in trees.items()}


def test_fix_r1_r4_11_reexported_const(c_reexport):
    """R1-r4-11: `from pkg import ROOT`（`__init__.py` で再公開）→ 対照と同じ path MODEL/resolved → D2 矛。"""
    u = c_reexport["write_reexport"]
    for e in _effects(u, "FS_WRITE"):
        assert (_slot(e, "path").get("prin"), _slot(e, "path").get("prov")) == ("MODEL", "resolved"), _brief(u)
        assert "/srv/data" in _resolved_consts(_slot(e, "path")), _brief(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_fix_r1_r4_11_reexported_client(c_reexport):
    """R1-r4-11: 再公開した httpx.Client の受け手の型 → 対照と同じ NET 行（DELETE）→ D1 矛（net_modify）。"""
    u = c_reexport["net_reexport"]
    assert any(e.get("http_method") == "DELETE" for e in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_keep_r1_r4_11_direct_controls(c_reexport):
    """R1-r4-11 の対照: 元のモジュールから直接 import する形は今も矛。"""
    _check(c_reexport["write_direct_control"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")
    _check(c_reexport["net_direct_control"], "NET", "D1", "矛", "net_modify")


@pytest.mark.parametrize("tree", ["cx11", "try", "after", "origin", "other"])
def test_keep_r1_r4_11_counterexamples_stay_opaque(c_counter, tree):
    """R1-r4-11 の反例（cx11・予備 import・import の後の代入・元のモジュールの global・他モジュールの書き込み）。

    G3 の健全性の条件（束縛がちょうど 1 つ、直下の from-import、書き換えない）を再公開するモジュールと元の
    モジュールの両方に掛ける。ROOT / MODE を config.py の定数に決め打ちしない → "/srv/data" を resolved の
    定数として読まず、mode "a"（destructive=False）の内にしない。
    """
    u = c_counter[tree]["write_reexport_rebound"]
    for e in _effects(u, "FS_WRITE"):
        assert "/srv/data" not in _resolved_consts(_slot(e, "path")), _brief(u)
    _no_append_mode(u)
    _not_clear(u, "FS_WRITE", "D2")


# ===========================================================================
# 4. R1-r4-13 タプル代入
# ===========================================================================

D_TUPLE = '''import sqlite3

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

SQL_PURGE, SQL_COUNT = "DELETE FROM sessions", "SELECT count(*) FROM sessions"
SQL_PURGE_PLAIN = "DELETE FROM sessions"
(SQL_N1, SQL_N2), N3 = ("DELETE FROM sessions", "SELECT 1"), 3
[SQL_L, OTHER_L] = ["DELETE FROM sessions", 2]
DB, HTTP = sqlite3.connect("/data/app.db"), httpx.Client()

SQL_A = "SELECT 1"
SQL_B = "DELETE FROM sessions"
SQL_A, SQL_B = SQL_B, SQL_A

SQL_C = "SELECT count(*) FROM sessions"
SQL_C, OTHER_C = "DELETE FROM sessions", 1

HEAD = ("DELETE FROM sessions",)
SQL_S1, SQL_S2 = *HEAD, "SELECT 1"
*REST_T, SQL_T = "SELECT 1", "SELECT 2", "DELETE FROM sessions"

SQL_R, OTHER_R = "SELECT 1", 2


def set_sql_r(v):
    global SQL_R
    SQL_R = v


@mcp.tool(annotations={"readOnlyHint": True})
def module_tuple_const(db: str) -> str:
    sqlite3.connect(db).execute(SQL_PURGE)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def control_module_plain_const(db: str) -> str:
    sqlite3.connect(db).execute(SQL_PURGE_PLAIN)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def nested_tuple_const(db: str) -> str:
    sqlite3.connect(db).execute(SQL_N1)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def list_target_const(db: str) -> str:
    sqlite3.connect(db).execute(SQL_L)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def tuple_receiver(q: str) -> str:
    DB.execute("DELETE FROM t WHERE id = " + q)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def swapped(db: str) -> str:
    sqlite3.connect(db).execute(SQL_A)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def plain_then_tuple(db: str) -> str:
    sqlite3.connect(db).execute(SQL_C)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def starred_rhs(db: str) -> str:
    sqlite3.connect(db).execute(SQL_S1)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def starred_target(db: str) -> str:
    sqlite3.connect(db).execute(SQL_T)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def tuple_rebound(db: str) -> str:
    sqlite3.connect(db).execute(SQL_R)
    return "ok"
'''


@pytest.fixture(scope="module")
def d(tmp_path_factory):
    return _units(tmp_path_factory, "u09_d_tuple", {"server.py": D_TUPLE})


def _sql_const_delete(u: dict) -> None:
    es = _effects(u, "DB")
    assert es, _brief(u)
    for e in es:
        s = _slot(e, "sql")
        assert (s.get("prin"), s.get("prov"), (s.get("shape") or {}).get("const")) == (
            "OP", "resolved", "DELETE FROM sessions"), _brief(u)
        assert e.get("sql_head") == "DELETE", _brief(u)
    _check(u, "DB", "D1", "矛", "db_modify")


@pytest.mark.parametrize("tool", [
    "module_tuple_const",   # 所見: 同じ長さのタプル → 位置で対応
    "nested_tuple_const",   # fix_outline: 入れ子は再帰で対応を取る
    "list_target_const",    # fix_outline: 対象・右辺が List でも同じ
])
def test_fix_r1_r4_13_tuple_const(d, tool):
    """R1-r4-13: `A, B = x, y` は `A = x` と同じ束縛 → 対照と同じ OP/resolved の DELETE → D1 矛（db_modify）。"""
    _sql_const_delete(d[tool])


def test_fix_r1_r4_13_tuple_receiver(d):
    """R1-r4-13 の検証役 notes: タプル束縛のモジュール水準の接続も受け手の型を失わない → DB 行と D1 矛。"""
    u = d["tuple_receiver"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")


@pytest.mark.parametrize("tool", ["swapped", "plain_then_tuple"])
def test_fix_r1_r4_13_existing_false_clean(d, tool):
    """R1-r4-13 の検証役の反例: 今は先の単純代入の SELECT を resolved と決め打ちして内（誤 clear）。

    タプル側も候補に入れると swap は再帰で opaque、混在は SELECT と DELETE の join になる → 内ではない。
    """
    u = d[tool]
    for e in _effects(u, "DB"):
        s = _slot(e, "sql")
        assert not (s.get("prov") == "resolved" and str((s.get("shape") or {}).get("const", "")).startswith("SELECT")), _brief(u)
    _not_clear(u, "DB", "D1")


def test_keep_r1_r4_13_plain_control(d):
    """R1-r4-13 の対照: 単純代入の定数は今も OP/resolved の DELETE → D1 矛。"""
    _sql_const_delete(d["control_module_plain_const"])


@pytest.mark.parametrize("tool", [
    "starred_rhs",     # 右辺の Starred: Starred を除いて位置を詰めると SQL_S1 が "SELECT 1" に化ける
    "starred_target",  # 対象の Starred: 長さが違う。位置で読むと SQL_T が "SELECT 2" に化ける
    "tuple_rebound",   # タプル束縛にも単純代入と同じ再束縛の検査（関数内 global）を掛ける
])
def test_keep_r1_r4_13_not_read_as_select(d, tool):
    """R1-r4-13 の避ける条件: Starred があれば読まない・再束縛の検査を掛ける → SELECT の resolved で内にしない。"""
    u = d[tool]
    for e in _effects(u, "DB"):
        assert _slot(e, "sql").get("prov") != "resolved", _brief(u)
    _not_clear(u, "DB", "D1")


# ===========================================================================
# 5. R1-r3-9 クラス属性 `Cls.ATTR`（規則 B: 型と主体だけ、確度は常に opaque）
# ===========================================================================

E_CLASS = '''import os
import sqlite3

import httpx
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class Clients:
    http = httpx.Client()
    session = requests.Session()


class Store:
    conn = sqlite3.connect("/data/app.db")


class Cfg:
    PREFIX = "echo "
    ROOT = "/data"
    MODE = "w"


class Q:
    PURGE = "DELETE FROM sessions"


class M:
    MODE = "a"


PREFIX_MOD = "echo "
ROOT_MOD = "/data"


@mcp.tool(annotations={"readOnlyHint": True})
def receiver_via_class(url: str) -> str:
    return Clients.http.request("DELETE", url).text


@mcp.tool(annotations={"readOnlyHint": True})
def receiver_via_class2(url: str) -> str:
    return Clients.session.post(url).text


@mcp.tool(annotations={"readOnlyHint": True})
def db_receiver_via_class(q: str) -> str:
    Store.conn.execute("DELETE FROM t WHERE id = " + q)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def const_via_class_shell(cmd: str) -> str:
    os.system(Cfg.PREFIX + cmd)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def const_via_class_path(name: str, text: str) -> str:
    with open(Cfg.ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def const_via_class_mode(path: str, text: str) -> str:
    with open(path, Cfg.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def class_sql_const(db: str) -> str:
    sqlite3.connect(db).execute(Q.PURGE)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def class_append_mode(path: str, text: str) -> str:
    with open(path, M.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def control_const_via_module_shell(cmd: str) -> str:
    os.system(PREFIX_MOD + cmd)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def control_const_via_module_path(name: str, text: str) -> str:
    with open(ROOT_MOD + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"
'''

E_SETTINGS = '''import httpx


class Settings:
    ROOT = "/data"
    PREFIX = "echo "


class RemoteClients:
    http = httpx.Client(base_url="https://api.example.com")
'''

E_CROSS_SERVER = '''import os

from mcp.server.fastmcp import FastMCP

from .settings import RemoteClients, Settings

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def cross_module_class_const(cmd: str) -> str:
    os.system(Settings.PREFIX + cmd)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def cross_module_class_root(name: str, text: str) -> str:
    with open(Settings.ROOT + "/" + name, "w") as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def cross_module_class_receiver(item: str) -> str:
    RemoteClients.http.request("DELETE", "/items/" + item)
    return "ok"
'''

#: 反例 ce9a_cls_store（検証役）: `cls.` / `setattr(cls, ...)` / `type(self).` / 別名経由の再束縛。
E_CE9A = '''import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class Cfg:
    MODE = "r"
    BIN = "/usr/bin/true"
    SHELL = False

    @classmethod
    def set_mode(cls, m):
        cls.MODE = m

    @classmethod
    def set_bin(cls, b):
        setattr(cls, "BIN", b)

    def set_shell(self, s):
        type(self).SHELL = s


def alias_store(v):
    C = Cfg
    C.MODE = v


@mcp.tool(annotations={"destructiveHint": False})
def open_with_class_mode(path: str, text: str) -> str:
    with open(path, Cfg.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def run_class_bin(arg: str) -> str:
    subprocess.run([Cfg.BIN, arg], shell=Cfg.SHELL)
    return "ok"
'''

#: 外部の基底（メタクラスで属性の意味が変わりうる: Enum・pydantic BaseSettings）と、局所の同名。
E_EXT = '''import json
import os
from enum import Enum

from mcp.server.fastmcp import FastMCP
from pydantic_settings import BaseSettings

mcp = FastMCP("t")


class Settings(BaseSettings):
    MODE: str = "a"


class Mode(Enum):
    APPEND = "a"


class Cmd:
    PREFIX = "echo "


@mcp.tool(annotations={"destructiveHint": False})
def settings_mode(path: str, text: str) -> str:
    with open(path, Settings.MODE) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def enum_member_mode(path: str, text: str) -> str:
    with open(path, Mode.APPEND) as fh:
        fh.write(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def local_class_shadow(spec: str) -> str:
    Cmd = json.loads(spec)
    os.system(Cmd.PREFIX)
    return "ok"
'''


@pytest.fixture(scope="module")
def e(tmp_path_factory):
    trees = {
        "cls": {"server.py": E_CLASS},
        "cross": {"pkg/__init__.py": "", "pkg/settings.py": E_SETTINGS, "pkg/server.py": E_CROSS_SERVER},
        "ce9a": {"server.py": E_CE9A},
        "ext": {"server.py": E_EXT},
    }
    return {k: _units(tmp_path_factory, f"u09_e_{k}", v) for k, v in trees.items()}


# --- 直す側（規則 B でも受け手の型は付く）---

@pytest.mark.parametrize("tree,tool", [
    ("cls", "receiver_via_class"),            # 所見: class Clients: http = httpx.Client()
    ("cross", "cross_module_class_receiver"),  # 別モジュールのクラス（import 表 → get_class(strict=True)）
])
def test_fix_r1_r3_9_class_attr_client_delete(e, tree, tool):
    """R1-r3-9（規則 B）: クラス属性のクライアントに型が付く → NET 行、DELETE は実引数の定数 → D1 矛（net_modify）。"""
    u = e[tree][tool]
    assert any(e_.get("http_method") == "DELETE" for e_ in _effects(u, "NET")), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_fix_r1_r3_9_class_attr_session_post(e):
    """R1-r3-9（規則 B）: `Clients.session.post` → NET 行、POST → §7.1 で D1 不（net_post）。"""
    u = e["cls"]["receiver_via_class2"]
    assert _effects(u, "NET"), _brief(u)
    _check(u, "NET", "D1", "不", "net_post")


def test_fix_r1_r3_9_class_attr_db_receiver(e):
    """R1-r3-9（規則 B）: `Store.conn`（sqlite3 接続）に型が付く → DB 行、SQL が MODEL → D1 矛。"""
    u = e["cls"]["db_receiver_via_class"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")


# --- 壊さない側（規則 B: 定数でも確度は opaque のまま）---

@pytest.mark.parametrize("tree,tool,slot,kind,decl,want,reason", [
    ("cls", "const_via_class_shell", "shell_string", "SPAWN", "D1", "不", "spawn_model_opaque"),
    ("cross", "cross_module_class_const", "shell_string", "SPAWN", "D1", "不", "spawn_model_opaque"),
    ("cls", "const_via_class_path", "path", "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque"),
    ("cross", "cross_module_class_root", "path", "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque"),
])
def test_keep_r1_r3_9_rule_b_const_stays_opaque(e, tree, tool, slot, kind, decl, want, reason):
    """R1-r3-9 規則 B: `Cfg.PREFIX + cmd` は主体 MODEL・確度 opaque のまま → *_opaque の不（規則 A の矛は期待しない）。"""
    u = e[tree][tool]
    es = _effects(u, kind)
    assert es, _brief(u)
    for e_ in es:
        s = _slot(e_, slot)
        if s:
            assert (s.get("prin"), s.get("prov")) == ("MODEL", "opaque"), _brief(u)
    _check(u, kind, decl, want, reason)


def test_keep_r1_r3_9_rule_b_sql_const_stays_opaque(e):
    """R1-r3-9 規則 B: `Q.PURGE` は定数でも resolved にしない → SQL は opaque（D17 改訂 5: opaque の定数は読まない）→ D1 不。"""
    u = e["cls"]["class_sql_const"]
    es = _effects(u, "DB")
    assert es, _brief(u)
    for e_ in es:
        assert _slot(e_, "sql").get("prov") == "opaque", _brief(u)
        assert e_.get("sql_head") is None, _brief(u)
    _check(u, "DB", "D1", "不")


@pytest.mark.parametrize("tree,tool", [
    ("cls", "const_via_class_mode"),    # 所見: mode "w" でも path が MODEL なので今も矛
    ("cls", "class_append_mode"),       # 規則 B: `M.MODE = "a"` を resolved の追記にしない（規則 A なら内）
    ("ce9a", "open_with_class_mode"),   # 反例 ce9a_cls_store: cls. / 別名で再束縛される MODE
    ("ext", "settings_mode"),           # 外部の基底（pydantic BaseSettings）
    ("ext", "enum_member_mode"),        # 外部の基底（Enum のメンバーは文字列ではない）
])
def test_keep_r1_r3_9_class_mode_unknown(e, tree, tool):
    """R1-r3-9 規則 B と反例: クラス属性の mode は分からない → FS_WRITE 行が残り、mode 不明・path MODEL で D2 矛。"""
    u = e[tree][tool]
    _no_append_mode(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_unknown_model_path")


def test_keep_r1_r3_9_ce9a_spawn_bin_shell(e):
    """反例 ce9a_cls_store: `Cfg.BIN` / `Cfg.SHELL` は `setattr(cls, ...)` / `type(self).` で再束縛 → 決め打ちしない。

    shell=True になりうる経路の shell_string 行を残し、SPAWN の効果行はどれも resolved にしない。
    """
    u = e["ce9a"]["run_class_bin"]
    es = _effects(u, "SPAWN")
    assert es and all(e_.get("resolution") == "opaque" for e_ in es), _brief(u)
    assert any("shell_string" in (e_.get("slots") or {}) for e_ in es), _brief(u)
    _not_clear(u, "SPAWN", "D1")


def test_keep_r1_r3_9_module_const_controls(e):
    """R1-r3-9 の対照: 同じ定数をモジュール直下に書く形は今も矛（規則 B でクラス側はこれと揃わない = 記録する限界）。"""
    _check(e["cls"]["control_const_via_module_shell"], "SPAWN", "D1", "矛", "spawn_model")
    _check(e["cls"]["control_const_via_module_path"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_keep_r1_r3_9_local_shadow_keeps_model(e):
    """R1-r3-9 の避ける条件（名前が env / local_bindings に無いときだけ）: 局所 `Cmd = json.loads(spec)` はクラスではない。

    クラス本体を読むと `Cmd.PREFIX` が OP の "echo " に化ける（主体の誤 clear）。shell_string の主体は MODEL のまま。
    """
    u = e["ext"]["local_class_shadow"]
    es = _effects(u, "SPAWN")
    assert es, _brief(u)
    for e_ in es:
        s = _slot(e_, "shell_string")
        if s:
            assert s.get("prin") == "MODEL", _brief(u)
    _not_clear(u, "SPAWN", "D1")
