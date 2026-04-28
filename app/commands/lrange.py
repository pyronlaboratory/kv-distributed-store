from app.store import store
from app.protocols.encoder import resp_array_encoder


def execute(args):
    key, start, stop = args[1], int(args[2]), int(args[3])
    lst, _ = store.get(key, ([], None))
    stop_idx = stop + 1 or None  # when stop == -1, stop+1 == 0 which is falsy → None
    return resp_array_encoder(lst[start:stop_idx])
