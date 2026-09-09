"""source と sink が**別関数**にある形。Semgrep CE は手続き内 taint のみなので
これを報告できない。§8-4 が要求する機能境界の実測はこの 2 本の差である。"""

import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("boundary")


def _run(cmd: str) -> str:
    return subprocess.run(cmd, shell=True).stdout


@mcp.tool()
def across_functions(command: str) -> str:
    return _run(command)
