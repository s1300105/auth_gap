import os
from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool as lc_tool

mcp = FastMCP("demo")
tool = mcp.tool


@tool()
def via_alias(path: str) -> str:
    os.remove(path)
    return "ok"


@lc_tool
def via_lc_alias(path: str) -> str:
    os.remove(path)
    return "ok"
