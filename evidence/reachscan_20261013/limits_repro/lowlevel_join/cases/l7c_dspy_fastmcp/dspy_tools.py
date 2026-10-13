"""An unrelated DSPy program in the same repository. dspy.Tool(func, name=...) has no MCP annotations."""
import dspy


def _search(query: str) -> str:
    return query


search_tool = dspy.Tool(_search, name="search", desc="web search")
