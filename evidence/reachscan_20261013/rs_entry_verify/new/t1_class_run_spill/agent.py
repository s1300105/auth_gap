import os
from agno.tools import Toolkit


class FileTools(Toolkit):
    name = "file_tools"

    def list_files(self) -> str:
        return "x"


class Janitor:
    def _run(self, path: str) -> None:
        os.remove(path)
