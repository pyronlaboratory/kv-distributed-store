from app.store import store, waiting
from app.protocols.encoder import resp_array_encoder
from collections import deque


def execute(args, conn):
    key = args[1]
    lst, _ = store.get(key, ([], None))
    if lst:
        element = lst.pop(0)
        return resp_array_encoder([key, element])

    # block — register waiter, return nothing
    waiting.setdefault(key, deque()).append(conn)
    return None
