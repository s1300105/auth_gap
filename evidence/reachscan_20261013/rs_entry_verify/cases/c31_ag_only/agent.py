import os
from agno.tools import Toolkit
from gptme.tools.base import ToolSpec
from autogpt.command_decorator import command
from langroid.agent.tool_message import ToolMessage
from langroid.agent.chat_agent import ChatAgent


class FileTools(Toolkit):
    name = "file_tools"

    def __init__(self):
        super().__init__(name="file_tools", tools=[self.purge])

    def purge(self, path: str) -> str:
        os.remove(path)
        return "ok"


def gp_exec(code, args, kwargs, confirm):
    os.remove(args[0])
    return "ok"


tool = ToolSpec(name="gp_purge", desc="x", execute=gp_exec)


@command("ag_purge", "Delete a file", {"path": {"type": "string"}})
def ag_purge(path: str, agent) -> str:
    os.remove(path)
    return "ok"


class PurgeTool(ToolMessage):
    request: str = "lr_purge"
    purpose: str = "x"
    path: str


class MyAgent(ChatAgent):
    def lr_purge(self, msg: PurgeTool) -> str:
        os.remove(msg.path)
        return "ok"
