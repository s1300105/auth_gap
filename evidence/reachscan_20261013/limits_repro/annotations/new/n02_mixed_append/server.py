"""L1: readOnlyHint=<module constant True> together with destructiveHint=False.
At runtime readOnlyHint is True, so D1 applies (destructiveHint is meaningless).
Each body does something that is a D1 contradiction but within D2."""
import sqlite3
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")
RO = True


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def append_nonlit(path: str, content: str) -> str:
    with open(path, "a") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def append_lit(path: str, content: str) -> str:
    with open(path, "a") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def insert_nonlit(item: str) -> str:
    con = sqlite3.connect("db.sqlite")
    con.execute("INSERT INTO items(v) VALUES (?)", (item,))
    con.commit()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False))
def insert_lit(item: str) -> str:
    con = sqlite3.connect("db.sqlite")
    con.execute("INSERT INTO items(v) VALUES (?)", (item,))
    con.commit()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=not False, idempotentHint=True))
def append_idem_nonlit(path: str, content: str) -> str:
    with open(path, "a") as f:
        f.write(content)
    return "ok"
