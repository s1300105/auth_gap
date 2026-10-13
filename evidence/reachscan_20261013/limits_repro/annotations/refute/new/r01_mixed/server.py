import os
import sqlite3

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("mixed")
RO = True
OW = False


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def nl_append(path: str, text: str) -> str:
    with open(path, "a") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def lit_append(path: str, text: str) -> str:
    with open(path, "a") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def nl_write_const(text: str) -> str:
    with open("/var/tmp/out.txt", "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def lit_write_const(text: str) -> str:
    with open("/var/tmp/out.txt", "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def nl_insert(v: str) -> str:
    conn = sqlite3.connect("db.sqlite")
    conn.execute("INSERT INTO t (v) VALUES (?)", (v,))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def lit_insert(v: str) -> str:
    conn = sqlite3.connect("db.sqlite")
    conn.execute("INSERT INTO t (v) VALUES (?)", (v,))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, idempotentHint=True))
def nl_idem_overwrite(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
def lit_idem_overwrite(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=OW))
def nl_closed_world(q: str) -> str:
    return requests.get("https://api.example.com/search", params={"q": q}).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def lit_closed_world(q: str) -> str:
    return requests.get("https://api.example.com/search", params={"q": q}).text


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=RO))
def lit_ro_nl_destr(path: str) -> str:
    os.remove(path)
    return "ok"
