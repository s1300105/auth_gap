import os
from crewai.tools import tool


@tool("Delete File")
def delete_file(path: str) -> str:
    """Delete a file."""
    os.remove(path)
    return "ok"
