import shlex, subprocess
def git_log(argstr):
    parts = shlex.split(argstr)
    subprocess.run(["git", "log"] + parts, shell=False)
