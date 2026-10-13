import os
from pydantic import BaseModel
from langchain_core.tools import tool
from agents import function_tool


class Req(BaseModel):
    path: str


@tool
def lc_model(req: Req) -> str:
    os.remove(req.path)
    return "ok"


@function_tool
def oa_model(req: Req) -> str:
    os.remove(req.path)
    return "ok"
