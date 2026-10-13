"""L9c: MCP でない枠組みの @tool（crewai / agno / claude_agent_sdk）。"""
import os

from agno.tools import tool as agno_tool
from claude_agent_sdk import tool as sdk_tool
from crewai.tools import tool


@tool("Delete File")
def crew_delete(path: str) -> str:
    """Delete a file."""
    os.remove(path)
    return "ok"


@agno_tool
def agno_delete(path: str) -> str:
    os.remove(path)
    return "ok"


@sdk_tool("sdk_delete", "Delete a file", {"path": str})
async def sdk_delete(args):
    os.remove(args["path"])
    return {"content": []}
