from app.store import store
from app.protocols.encoder import resp_encoder, resp_array_encoder


def execute(args):
    lst, _ = store.get(args[1], ([], None))
    if len(args) > 2:
        n = int(args[2])
        popped, lst[:n] = lst[:n], []
        return resp_array_encoder(popped)
    return resp_encoder(lst.pop(0) if lst else None)
