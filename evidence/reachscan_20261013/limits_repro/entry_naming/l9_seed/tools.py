"""L9d: 同じ本体・同じ pydantic 引数で、LangChain の @tool（framework=mcp と付く）と openai-agents の @function_tool を並べる。"""
import os
import subprocess

from agents import function_tool
from langchain_core.tools import tool
from pydantic import BaseModel


class Req(BaseModel):
    path: str
    cmd: str


@tool
def lc_model(req: Req) -> str:
    """lc"""
    os.remove(req.path)
    subprocess.run(req.cmd, shell=True)
    return "ok"


@function_tool
def oa_model(req: Req) -> str:
    os.remove(req.path)
    subprocess.run(req.cmd, shell=True)
    return "ok"
