"""別モジュールに置く効果本体。G14 / G15 が要求する。"""

import shlex
import subprocess


def run_shell(cmd):
    subprocess.run(cmd, shell=True)


def git_log(argstr):
    parts = shlex.split(argstr)
    subprocess.run(["git", "log"] + parts, shell=False)
