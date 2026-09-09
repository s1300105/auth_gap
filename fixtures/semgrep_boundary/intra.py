"""source と sink が**同一関数内**にある形。Semgrep CE はこれを報告できる。"""

import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("boundary")


@mcp.tool()
def same_function(command: str) -> str:
    return subprocess.run(command, shell=True).stdout
