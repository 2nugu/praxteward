def load(rows):
    # shortcut: keeps all rows in memory (measured max 200), stream when a run exceeds 10k rows
    return list(rows)


def send(msg):
    # shortcut: no retry
    return msg
