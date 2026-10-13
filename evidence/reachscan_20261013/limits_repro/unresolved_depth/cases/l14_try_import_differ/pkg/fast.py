import os


def save(path):
    os.remove(path)  # SINK: FS_WRITE destructive, on the branch that normally runs
    return "ok"
