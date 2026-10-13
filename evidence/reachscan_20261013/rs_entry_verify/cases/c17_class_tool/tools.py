import os
from langchain_core.tools import BaseTool


class PurgeNamed(BaseTool):
    name: str = "purge_named"
    description: str = "x"

    def _run(self, path: str) -> str:
        os.remove(path)
        return "ok"


class PurgeUnnamed(BaseTool):
    description: str = "x"

    def _run(self, path: str) -> str:
        os.remove(path)
        return "ok"
