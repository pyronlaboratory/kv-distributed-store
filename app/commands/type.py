from app.store import store


def execute(args):
    key = args[1]
    entry = store.get(key)
    if entry is None:
        return b"+none\r\n"
    value, _ = entry
    if isinstance(value, list):
        return b"+list\r\n"
    return b"+string\r\n"
