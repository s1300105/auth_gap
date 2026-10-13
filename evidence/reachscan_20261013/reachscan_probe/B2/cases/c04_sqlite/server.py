"""c04: sqlite3 UPDATE / SELECT / DELETE."""
import sqlite3

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c04_sqlite")
DB_PATH = "app.db"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def rename_user(uid: int, name: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, uid))  # SINK UPDATE
    conn.commit()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_users() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")  # SELECT only
    return cursor.fetchall()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def drop_user(uid: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM users WHERE id = ?", (uid,))  # SINK DELETE (extra)
    conn.commit()
    return "ok"


if __name__ == "__main__":
    mcp.run()
