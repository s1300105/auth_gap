import os


def save(path):
    os.remove(path)  # SINK: only on the fallback branch
    return "ok"
