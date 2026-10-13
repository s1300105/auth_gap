"""Write helpers imported by pkg/server.py in four different ways."""


def save_plain(path, data):
    with open(path, "w") as f:  # SINK save_plain
        f.write(data)


def save_alias(path, data):
    with open(path, "w") as f:  # SINK save_alias
        f.write(data)


def save_modalias(path, data):
    with open(path, "w") as f:  # SINK save_modalias
        f.write(data)


def save_dotted(path, data):
    with open(path, "w") as f:  # SINK save_dotted
        f.write(data)
