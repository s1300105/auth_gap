from tools import run_shell
REGISTRY = {"sh": run_shell}
def dispatch(name, cmd):
    if not confirm(name):
        raise PermissionError(name)
    run_shell(cmd)
def llm_loop(tc):
    REGISTRY[tc.name](tc.args)
