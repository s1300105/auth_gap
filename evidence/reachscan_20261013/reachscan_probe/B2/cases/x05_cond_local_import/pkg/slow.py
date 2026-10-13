def save(path, data):
    with open(path, "w") as f:  # SINK slow.save
        f.write(data)
