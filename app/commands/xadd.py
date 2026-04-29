from app.store import store
from app.protocols.encoder import resp_encoder


def execute(args):
    key, entry_id = args[1], args[2]
    pairs = args[3:]
    entry = {pairs[i]: pairs[i + 1] for i in range(0, len(pairs), 2)}

    if key not in store:
        store[key] = ([], None)  # list of (id, entry) tuples

    store[key][0].append((entry_id, entry))
    return resp_encoder(entry_id)
