from app.store import store
from app.protocols.encoder import resp_array_encoder


def execute(args):
    key, start, stop = args[1], int(args[2]), int(args[3])
    lst, _ = store.get(key, ([], None))
    return resp_array_encoder(lst[start : stop + 1])  # stop is inclusive
