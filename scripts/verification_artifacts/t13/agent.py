from tools import run_shell
def dispatch(name, cmd):
    if not confirm(name):
        raise PermissionError(name)
    run_shell(cmd)
def retry(name, cmd):
    run_shell(cmd)
