import os
from pydantic_ai import Agent
from autogen import ConversableAgent
from llama_index.core.tools import FunctionTool
from swarm import Agent as SwarmAgent
import dspy
from metagpt.tools.tool_registry import register_tool

agent = Agent("openai:gpt-4o")
assistant = ConversableAgent("a")


@agent.tool_plain
def pa_plain(path: str) -> str:
    os.remove(path)
    return "ok"


@assistant.register_for_llm(description="x")
def ag_llm(path: str) -> str:
    os.remove(path)
    return "ok"


def li_fn(path: str) -> str:
    os.remove(path)
    return "ok"


def sw_fn(path: str) -> str:
    os.remove(path)
    return "ok"


def dspy_fn(path: str) -> str:
    os.remove(path)
    return "ok"


@register_tool(tags=["x"])
class MgTool:
    def run(self, path: str) -> str:
        os.remove(path)
        return "ok"


li_tool = FunctionTool.from_defaults(fn=li_fn, name="li_named")
sw_agent = SwarmAgent(functions=[sw_fn])
dspy_tool = dspy.Tool(dspy_fn, name="dspy_named")
