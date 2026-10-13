def save(path, data):
    with open(path, "w") as f:  # SINK fast.save
        f.write(data)
