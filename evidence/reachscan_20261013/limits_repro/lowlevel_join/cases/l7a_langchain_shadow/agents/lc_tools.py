"""An unrelated LangChain agent in the same repository. langchain_core.tools.Tool has no MCP annotations."""
from langchain_core.tools import Tool


def _search(query: str) -> str:
    return query


search_tool = Tool(name="search", func=_search, description="web search")
