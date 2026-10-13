import os
from agno.agent import Agent as AgnoAgent
from google.adk.agents import Agent


def purge(path: str) -> str:
    os.remove(path)
    return "ok"


def purge2(path: str) -> str:
    os.remove(path)
    return "ok"


adk_agent = Agent(name="a", tools=[purge])
agno_agent = AgnoAgent(tools=[purge2])
