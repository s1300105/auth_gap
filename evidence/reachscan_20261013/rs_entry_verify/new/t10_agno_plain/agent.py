import os
from agno.agent import Agent


def purge2(path: str) -> str:
    os.remove(path)
    return "ok"


agno_agent = Agent(tools=[purge2])
