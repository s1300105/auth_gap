"""矛盾の判定原理（`docs/contradiction_principles.md` §6 の選択、§7 の判定表）どおりに判定する。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。
§7 の表（`914c4af` でコミット済み）の行ごとにツールを 1 つ置いた。

記号: `"矛"` = 行に CONTRADICTION と注記 `contradiction:<宣言>`、`"不"` = 注記
`contradiction_unknown:<宣言>:<理由>`（CONTRADICTION ではない）、`"内"` = どちらも無い。
宣言: D1 = readOnlyHint: true / D2 = destructiveHint: false（readOnly でないとき）/
D3 = openWorldHint: false / D4 = idempotentHint: true（readOnly でないとき）。

ツールの仮引数はモデル（MODEL）由来、リテラルは OP の定数、`os.environ[...]` は OP で定数に読めない。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = r'''
import os
import shutil
import sqlite3
import subprocess
import urllib.request
from pathlib import Path

import httpx
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")

def db():
    return sqlite3.connect("x.db")

RO = {"readOnlyHint": True}
ND = {"destructiveHint": False}
CW = {"openWorldHint": False}
ID = {"idempotentHint": True}

# ---- D1 readOnly ---------------------------------------------------------
@mcp.tool(annotations=RO)
async def d1_exec_const(p: str) -> str:
    eval("1 + 1"); return "x"

@mcp.tool(annotations=RO)
async def d1_spawn_model(cmd: str) -> str:
    subprocess.run([cmd]); return "x"

@mcp.tool(annotations=RO)
async def d1_spawn_const(p: str) -> str:
    subprocess.run(["nvidia-smi"]); return "x"

@mcp.tool(annotations=RO)
async def d1_spawn_shell_model(cmd: str) -> str:
    subprocess.run(cmd, shell=True); return "x"

@mcp.tool(annotations=RO)
async def d1_fs_mkdir(p: str) -> str:
    os.makedirs("/tmp/authgap_x"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_insert(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES (?)", (p,)); return "x"

@mcp.tool(annotations=RO)
async def d1_db_pragma_wal(p: str) -> str:
    db().execute("PRAGMA journal_mode=WAL"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_pragma_fk(p: str) -> str:
    db().execute("PRAGMA foreign_keys=ON"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_pragma_read(p: str) -> str:
    db().execute("PRAGMA table_info(users)"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_begin(p: str) -> str:
    db().execute("BEGIN"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_vacuum(p: str) -> str:
    db().execute("VACUUM"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_attach(p: str) -> str:
    db().execute("ATTACH DATABASE 'y.db' AS y"); return "x"

@mcp.tool(annotations=RO)
async def d1_db_model_sql(sql: str) -> str:
    db().execute(sql); return "x"

@mcp.tool(annotations=RO)
async def d1_db_op_sql(p: str) -> str:
    db().execute(os.environ["QUERY"]); return "x"

@mcp.tool(annotations=RO)
async def d1_net_get(url: str) -> str:
    httpx.get(url); return "x"

@mcp.tool(annotations=RO)
async def d1_net_post(p: str) -> str:
    httpx.post("https://api.example.com/rpc", json={"q": p}); return "x"

@mcp.tool(annotations=RO)
async def d1_net_delete(p: str) -> str:
    requests.delete("https://api.example.com/items/1"); return "x"

@mcp.tool(annotations=RO)
async def d1_net_put(p: str) -> str:
    requests.put("https://api.example.com/items/1", data=p); return "x"

@mcp.tool(annotations=RO)
async def d1_net_request_const(p: str) -> str:
    httpx.request("DELETE", "https://api.example.com/items/1"); return "x"

@mcp.tool(annotations=RO)
async def d1_net_request_get(p: str) -> str:
    httpx.request("GET", "https://api.example.com/items/1"); return "x"

@mcp.tool(annotations=RO)
async def d1_net_request_model(method: str) -> str:
    httpx.request(method, "https://api.example.com/items/1"); return "x"

@mcp.tool(annotations=RO)
async def d1_net_urlopen(p: str) -> str:
    urllib.request.urlopen("https://api.example.com/items/1"); return "x"

# ---- D2 destructive=false ------------------------------------------------
@mcp.tool(annotations=ND)
async def d2_exec_const(p: str) -> str:
    eval("1 + 1"); return "x"

@mcp.tool(annotations=ND)
async def d2_spawn_const(p: str) -> str:
    subprocess.run(["nvidia-smi"]); return "x"

@mcp.tool(annotations=ND)
async def d2_spawn_model(cmd: str) -> str:
    subprocess.run([cmd]); return "x"

@mcp.tool(annotations=ND)
async def d2_fs_mkdir(p: str) -> str:
    os.makedirs("/tmp/authgap_x"); return "x"

@mcp.tool(annotations=ND)
async def d2_open_append(p: str) -> str:
    open("/tmp/authgap_log", "a").write(p); return "x"

@mcp.tool(annotations=ND)
async def d2_unlink_const(p: str) -> str:
    os.unlink("/tmp/authgap_x"); return "x"

@mcp.tool(annotations=ND)
async def d2_chmod_const(p: str) -> str:
    os.chmod("/tmp/authgap_x", 0o600); return "x"

@mcp.tool(annotations=ND)
async def d2_write_text_const(p: str) -> str:
    Path("/tmp/authgap_out.txt").write_text(p); return "x"

@mcp.tool(annotations=ND)
async def d2_write_text_model(path: str) -> str:
    Path(path).write_text("x"); return "x"

@mcp.tool(annotations=ND)
async def d2_open_w_const(p: str) -> str:
    open("/tmp/authgap_out.txt", "w").write(p); return "x"

@mcp.tool(annotations=ND)
async def d2_open_w_model(path: str) -> str:
    open(path, "w").write("x"); return "x"

@mcp.tool(annotations=ND)
async def d2_copy_const(p: str) -> str:
    shutil.copy("/tmp/authgap_a", "/tmp/authgap_b"); return "x"

@mcp.tool(annotations=ND)
async def d2_db_insert(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES (?)", (p,)); return "x"

@mcp.tool(annotations=ND)
async def d2_db_update(p: str) -> str:
    db().execute("UPDATE t SET a = ?", (p,)); return "x"

@mcp.tool(annotations=ND)
async def d2_db_pragma_wal(p: str) -> str:
    db().execute("PRAGMA journal_mode=WAL"); return "x"

@mcp.tool(annotations=ND)
async def d2_db_pragma_fk(p: str) -> str:
    db().execute("PRAGMA foreign_keys=ON"); return "x"

@mcp.tool(annotations=ND)
async def d2_db_model_sql(sql: str) -> str:
    db().execute(sql); return "x"

@mcp.tool(annotations=ND)
async def d2_db_unknown_head(p: str) -> str:
    db().execute("NOTIFY chan"); return "x"

@mcp.tool(annotations=ND)
async def d2_net_delete(p: str) -> str:
    requests.delete("https://api.example.com/items/1"); return "x"

@mcp.tool(annotations=ND)
async def d2_net_patch(p: str) -> str:
    requests.patch("https://api.example.com/items/1", data=p); return "x"

@mcp.tool(annotations=ND)
async def d2_net_put_const(p: str) -> str:
    requests.put("https://api.example.com/items/1", data=p); return "x"

@mcp.tool(annotations=ND)
async def d2_net_put_model(url: str) -> str:
    requests.put(url, data="x"); return "x"

@mcp.tool(annotations=ND)
async def d2_net_post(p: str) -> str:
    httpx.post("https://api.example.com/rpc", json={"q": p}); return "x"

@mcp.tool(annotations=ND)
async def d2_net_get(url: str) -> str:
    httpx.get(url); return "x"

# ---- D3 openWorld=false --------------------------------------------------
@mcp.tool(annotations=CW)
async def d3_net_localhost(p: str) -> str:
    httpx.get("http://localhost:8080/x"); return "x"

@mcp.tool(annotations=CW)
async def d3_net_private(p: str) -> str:
    httpx.get("http://10.0.0.5/x"); return "x"

@mcp.tool(annotations=CW)
async def d3_net_external(p: str) -> str:
    httpx.get("https://api.example.com/x"); return "x"

@mcp.tool(annotations=CW)
async def d3_net_model_host(url: str) -> str:
    httpx.get(url); return "x"

@mcp.tool(annotations=CW)
async def d3_net_env_host(p: str) -> str:
    httpx.get(os.environ["API_URL"]); return "x"

@mcp.tool(annotations=CW)
async def d3_spawn_const(p: str) -> str:
    subprocess.run(["nvidia-smi"]); return "x"

@mcp.tool(annotations=CW)
async def d3_spawn_model(cmd: str) -> str:
    subprocess.run([cmd]); return "x"

@mcp.tool(annotations=CW)
async def d3_fs_mkdir(p: str) -> str:
    os.makedirs("/tmp/authgap_x"); return "x"

# ---- D4 idempotent=true --------------------------------------------------
@mcp.tool(annotations=ID)
async def d4_open_append(p: str) -> str:
    open("/tmp/authgap_log", "a").write(p); return "x"

@mcp.tool(annotations=ID)
async def d4_open_w_model(path: str) -> str:
    open(path, "w").write("x"); return "x"

@mcp.tool(annotations=ID)
async def d4_db_insert(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES (?)", (p,)); return "x"

@mcp.tool(annotations=ID)
async def d4_db_delete(p: str) -> str:
    db().execute("DELETE FROM t WHERE a = ?", (p,)); return "x"

@mcp.tool(annotations=ID)
async def d4_net_post(p: str) -> str:
    httpx.post("https://api.example.com/rpc", json={"q": p}); return "x"

@mcp.tool(annotations=ID)
async def d4_net_put(p: str) -> str:
    requests.put("https://api.example.com/items/1", data=p); return "x"

@mcp.tool(annotations=ID)
async def d4_spawn_model(cmd: str) -> str:
    subprocess.run([cmd]); return "x"

# ---- 組み合わせ ------------------------------------------------------------
@mcp.tool(annotations={"readOnlyHint": True, "idempotentHint": True})
async def ro_idem_open_append(p: str) -> str:
    open("/tmp/authgap_log", "a").write(p); return "x"

@mcp.tool(annotations={"readOnlyHint": True, "openWorldHint": False})
async def ro_closed_external_get(p: str) -> str:
    httpx.get("https://api.example.com/x"); return "x"

@mcp.tool()
async def none_delete(p: str) -> str:
    requests.delete("https://api.example.com/items/1"); os.unlink("/tmp/authgap_x"); return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("principles")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _status(u: dict, kind: str, decl: str) -> str:
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（前提が崩れている）"
    notes = [n for r in rows for n in r.get("notes", [])]
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    contra = any("CONTRADICTION" in r["verdicts"] for r in rows)
    assert not (hit and unk), f"{decl} が矛と不の両方"
    if hit:
        assert contra, "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


CASES = [
    # D1
    ("d1_exec_const", "EXEC", "D1", "矛"),
    ("d1_spawn_model", "SPAWN", "D1", "矛"),
    ("d1_spawn_const", "SPAWN", "D1", "不"),
    ("d1_spawn_shell_model", "SPAWN", "D1", "矛"),
    ("d1_fs_mkdir", "FS_WRITE", "D1", "矛"),
    ("d1_db_insert", "DB", "D1", "矛"),
    ("d1_db_pragma_wal", "DB", "D1", "矛"),
    ("d1_db_pragma_fk", "DB", "D1", "内"),
    ("d1_db_pragma_read", "DB", "D1", "内"),
    ("d1_db_begin", "DB", "D1", "内"),
    ("d1_db_vacuum", "DB", "D1", "矛"),
    ("d1_db_attach", "DB", "D1", "不"),
    ("d1_db_model_sql", "DB", "D1", "矛"),
    ("d1_db_op_sql", "DB", "D1", "不"),
    ("d1_net_get", "NET", "D1", "内"),
    ("d1_net_post", "NET", "D1", "不"),
    ("d1_net_delete", "NET", "D1", "矛"),
    ("d1_net_put", "NET", "D1", "矛"),
    ("d1_net_request_const", "NET", "D1", "矛"),
    ("d1_net_request_get", "NET", "D1", "内"),
    ("d1_net_request_model", "NET", "D1", "矛"),
    ("d1_net_urlopen", "NET", "D1", "不"),
    # D2
    ("d2_exec_const", "EXEC", "D2", "矛"),
    ("d2_spawn_const", "SPAWN", "D2", "不"),
    ("d2_spawn_model", "SPAWN", "D2", "矛"),
    ("d2_fs_mkdir", "FS_WRITE", "D2", "内"),
    ("d2_open_append", "FS_WRITE", "D2", "内"),
    ("d2_unlink_const", "FS_WRITE", "D2", "矛"),
    ("d2_chmod_const", "FS_WRITE", "D2", "矛"),
    ("d2_write_text_const", "FS_WRITE", "D2", "不"),
    ("d2_write_text_model", "FS_WRITE", "D2", "矛"),
    ("d2_open_w_const", "FS_WRITE", "D2", "不"),
    ("d2_open_w_model", "FS_WRITE", "D2", "矛"),
    ("d2_copy_const", "FS_WRITE", "D2", "不"),
    ("d2_db_insert", "DB", "D2", "内"),
    ("d2_db_update", "DB", "D2", "矛"),
    ("d2_db_pragma_wal", "DB", "D2", "不"),
    ("d2_db_pragma_fk", "DB", "D2", "内"),
    ("d2_db_model_sql", "DB", "D2", "矛"),
    ("d2_db_unknown_head", "DB", "D2", "不"),
    ("d2_net_delete", "NET", "D2", "矛"),
    ("d2_net_patch", "NET", "D2", "矛"),
    ("d2_net_put_const", "NET", "D2", "不"),
    ("d2_net_put_model", "NET", "D2", "矛"),
    ("d2_net_post", "NET", "D2", "不"),
    ("d2_net_get", "NET", "D2", "内"),
    # D3
    ("d3_net_localhost", "NET", "D3", "内"),
    ("d3_net_private", "NET", "D3", "内"),
    ("d3_net_external", "NET", "D3", "矛"),
    ("d3_net_model_host", "NET", "D3", "矛"),
    ("d3_net_env_host", "NET", "D3", "不"),
    ("d3_spawn_const", "SPAWN", "D3", "不"),
    ("d3_spawn_model", "SPAWN", "D3", "矛"),
    ("d3_fs_mkdir", "FS_WRITE", "D3", "内"),
    # D4
    ("d4_open_append", "FS_WRITE", "D4", "矛"),
    ("d4_open_w_model", "FS_WRITE", "D4", "内"),
    ("d4_db_insert", "DB", "D4", "不"),
    ("d4_db_delete", "DB", "D4", "内"),
    ("d4_net_post", "NET", "D4", "不"),
    ("d4_net_put", "NET", "D4", "内"),
    ("d4_spawn_model", "SPAWN", "D4", "不"),
    # 組み合わせ: readOnly があれば D4 は評価しない（仕様: meaningful only when readOnlyHint == false）
    ("ro_idem_open_append", "FS_WRITE", "D1", "矛"),
    ("ro_idem_open_append", "FS_WRITE", "D4", "内"),
    # D1 と D3 は独立に評価する
    ("ro_closed_external_get", "NET", "D1", "内"),
    ("ro_closed_external_get", "NET", "D3", "矛"),
    # 宣言が無ければ何も出ない
    ("none_delete", "NET", "D1", "内"),
    ("none_delete", "NET", "D2", "内"),
    ("none_delete", "FS_WRITE", "D2", "内"),
]


@pytest.mark.parametrize("tool,kind,decl,want", CASES, ids=[f"{c[0]}-{c[2]}" for c in CASES])
def test_principle_table(units, tool, kind, decl, want):
    assert _status(units[tool], kind, decl) == want


def test_other_declarations_silent(units):
    """1 つの宣言しか無いツールで、他の宣言の注記が出ない。"""
    for tool, kind, decl, _ in CASES:
        if tool.startswith(("ro_", "none_")):
            continue
        u = units[tool]
        for other in ("D1", "D2", "D3", "D4"):
            if other == decl:
                continue
            assert _status(u, kind, other) == "内", (tool, other)
