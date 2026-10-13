"""B1 case 7 control 2: c07ctl_chain_order with only "memo" claiming readOnlyHint=True.

save-note / archive-note / purge-note claim readOnlyHint=False, destructiveHint=True; "memo" claims readOnlyHint=True.
"""
import os
from enum import Enum

import mcp.types as types
from mcp.server.lowlevel import Server

SAVE_NOTE = "save-note"


class ToolName(str, Enum):
    ARCHIVE = "archive-note"
    PURGE = "purge-note"


server = Server("notes")


def write_note_impl(arguments: dict) -> str:
    with open(arguments["path"], "w") as f:
        f.write(arguments["content"])
    return "saved"


def archive_impl(arguments: dict) -> str:
    os.rename(arguments["path"], arguments["path"] + ".bak")
    return "archived"


def purge_impl(arguments: dict) -> str:
    os.remove(arguments["path"])
    return "purged"


def memo_writer(arguments: dict) -> str:
    with open(arguments["path"], "a") as f:
        f.write(arguments["content"])
    return "memo"


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="save-note", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
        types.Tool(name=ToolName.ARCHIVE, description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
        types.Tool(name=ToolName.PURGE.value, description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
        types.Tool(name="memo", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == SAVE_NOTE:
        text = write_note_impl(arguments)
    elif name == ToolName.ARCHIVE:
        text = archive_impl(arguments)
    elif name == "memo":
        text = memo_writer(arguments)
    elif name == ToolName.PURGE.value:
        text = purge_impl(arguments)
    else:
        raise ValueError(name)
    return [types.TextContent(type="text", text=text)]
