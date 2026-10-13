"""c08: pathlib ancestors + mkdir (AuthGap D43), Path.write_text, os.replace, shutil.copy."""
import os
import shutil
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c08_paths")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_cache_mkdir(url: str) -> str:
    cache_dir = Path(__file__).resolve().parents[2] / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)  # SINK Path.mkdir (D43)
    return str(cache_dir)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_write_text(path: str, data: str) -> str:
    Path(path).write_text(data)  # SINK Path.write_text
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_replace(src: str, dst: str) -> str:
    os.replace(src, dst)  # SINK os.replace
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_copy(src: str, dst: str) -> str:
    shutil.copy(src, dst)  # SINK shutil.copy
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_cache_mkdir(url: str) -> str:
    cache_dir = Path(__file__).resolve().parents[2] / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)  # SINK Path.mkdir (destr=False)
    return str(cache_dir)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_write_text(path: str, data: str) -> str:
    Path(path).write_text(data)  # SINK Path.write_text (destr=False)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_replace(src: str, dst: str) -> str:
    os.replace(src, dst)  # SINK os.replace (destr=False)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_copy(src: str, dst: str) -> str:
    shutil.copy(src, dst)  # SINK shutil.copy (destr=False)
    return "ok"


if __name__ == "__main__":
    mcp.run()
