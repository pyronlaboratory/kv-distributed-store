from app.store import store
from app.protocols.encoder import resp_encoder


def execute(args):
    lst, _ = store.get(args[1], ([], None))
    return resp_encoder(lst.pop(0) if lst else None)
