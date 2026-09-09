from tools import git_log
ALLOWED_TOOLS = {"git_log", "git_show"}
def dispatch(name, argstr):
    if name not in ALLOWED_TOOLS:
        raise PermissionError(name)
    git_log(argstr)
