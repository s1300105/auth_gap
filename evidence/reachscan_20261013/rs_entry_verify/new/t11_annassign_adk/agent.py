import os
from google.adk.agents import Agent


def purge(path: str) -> str:
    os.remove(path)
    return "ok"


root_agent: Agent = Agent(name="a", tools=[purge])
