from app.store import store
from app.protocols.encoder import resp_encoder


def execute(args):
    key = args[1]
    elements = args[2:][::-1]  # reverse before prepending
    if key not in store:
        store[key] = ([], None)
    store[key][0][:0] = elements  # prepend
    return resp_encoder(len(store[key][0]))
