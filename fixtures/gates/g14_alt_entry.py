"""G14: 第 2 のユニット入口（無ガード）。

期待: NODOM(alt_entry) -> GAP_SELECT。**前身は guarded=True = 誤 clear（不健全）。**

`llm_loop` に**カタログ化 LLM 呼び出し（R1）を置くのは必須**である
（無いと trig が assumed になり期待 `GAP_SELECT` が原理的に出ない）。

**`run_shell` は R2 のカタログ化エントリではないのでユニット入口として数えない**
（付録 G の唯一の例外）。
"""

from _prelude import ApprovalDenied, confirm
from _tools import run_shell

REGISTRY = {"sh": run_shell}


def dispatch(name, cmd):
    if not confirm(name):  # WITNESS
        raise ApprovalDenied(name)
    run_shell(cmd)


def llm_loop(client, prompt):
    resp = client.chat.completions.create(model="m", messages=prompt)
    for tc in resp.tool_calls:
        REGISTRY[tc.name](tc.args)  # EFFECT
