"""エントリ発見の smoke fixture。実在のパターンを 1 ファイルに集めた。"""

import subprocess
from typing import Annotated

import mcp.types as types
from mcp.server import Server
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")
server = Server("demo-lowlevel")


@mcp.tool()
def git_log(repo_path: str, max_count: int = 10) -> str:
    """高レベル登録。執行表では Def 5 側。"""
    return subprocess.run(["git", "log", f"-n{max_count}"], cwd=repo_path, shell=False).stdout


@mcp.tool(name="run_shell")
def _run_shell(command: str) -> str:
    return subprocess.run(command, shell=True).stdout


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """低レベル v1 デコレータ形。ハンドラ内の name 分岐が DISPATCH。"""
    if name == "git_log":
        return git_log(arguments["repo_path"])
    elif name in ("run_shell", "exec"):
        return _run_shell(arguments["command"])
    raise ValueError(name)


TOOLS = [
    types.Tool(
        name="git_log",
        description="show the log",
        annotations=types.ToolAnnotations(readOnlyHint=True, destructiveHint=False),
    ),
    types.Tool(
        name="run_shell",
        description="run a shell command",
        annotations={"openWorldHint": True, "read_only_hint": True},
    ),
]


def hidden_param(
    q: str,
    ctx: Annotated[str, {"include_in_function_choices": False}] = "",
) -> str:
    return q + ctx
