from app.store import store
from app.protocols.encoder import resp_encoder


def execute(args):
    key = args[1]
    elements = args[2:]
    if key not in store:
        store[key] = ([], None)
    store[key][0].extend(elements)
    return resp_encoder(len(store[key][0]))
