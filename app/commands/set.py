import time

from app.store import store

MULTIPLIER = {b"PX": 1, b"EX": 1000}


def execute(args):
    key, value = args[1], args[2]
    option = args[3].upper() if len(args) > 3 else None
    expires_at = (
        time.time() * 1000 + int(args[4]) * MULTIPLIER[option]
        if option in MULTIPLIER
        else None
    )
    store[key] = (value, expires_at)
    return b"+OK\r\n"
