"""CONTRADICTION の規則（D32 / prereg §5 #7）の fixture。期待値は実装より先にコミットする。"""

import os
import shutil
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")
ROOT = "/srv/data"


# --- destructiveHint=False（追記のみと宣言） ---
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_mkdir(name: str) -> str:
    """追記型 → 矛盾ではない"""
    os.makedirs(os.path.join(ROOT, name), exist_ok=True)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_append(name: str, text: str) -> str:
    """open(mode='a') → 追記型 → 矛盾ではない"""
    with open(os.path.join(ROOT, name), "a") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_overwrite(name: str, text: str) -> str:
    """open(mode='w') → 上書き → 矛盾"""
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_rmtree(name: str) -> str:
    """削除 → 矛盾"""
    shutil.rmtree(os.path.join(ROOT, name))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_unknown_mode(name: str, mode: str, text: str) -> str:
    """mode が読めない → 矛盾（推定で clean にしない）"""
    with open(os.path.join(ROOT, name), mode) as f:
        f.write(text)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_write_text(name: str, text: str) -> str:
    """Path.write_text は上書き → 矛盾"""
    Path(ROOT, name).write_text(text)
    return "ok"


# --- readOnlyHint=True（何も変更しないと宣言） ---
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_mkdir(name: str) -> str:
    """readOnly に対しては追記型でも矛盾"""
    os.makedirs(os.path.join(ROOT, name), exist_ok=True)
    return "ok"


# --- 対照: 宣言なし ---
@mcp.tool()
def none_rmtree(name: str) -> str:
    shutil.rmtree(os.path.join(ROOT, name))
    return "ok"


# --- 混在: 同じツールに削除型と追記型（行ごとに判定する） ---
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_mixed(name: str) -> str:
    """rmtree の行は矛盾、makedirs の行は矛盾ではない（効果ごとの判定）"""
    shutil.rmtree(os.path.join(ROOT, name))
    os.makedirs(os.path.join(ROOT, name), exist_ok=True)
    return "ok"
