"""A LangChain BaseTool (not an MCP tool) named cleanup that removes a file."""
import os

from langchain_core.tools import BaseTool


class CleanupTool(BaseTool):
    name: str = "cleanup"
    description: str = "remove a file"

    def _run(self, path: str) -> str:
        os.remove(path)
        return "ok"
