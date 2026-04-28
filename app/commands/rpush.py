from app.store import store, waiting
from app.protocols.encoder import resp_encoder, resp_array_encoder


def execute(args):
    key = args[1]
    elements = args[2:]
    if key not in store:
        store[key] = ([], None)
    store[key][0].extend(elements)
    count = len(store[key][0])  # count BEFORE popping for waiter

    if key in waiting and waiting[key]:
        conn, _ = waiting[key].popleft()
        element = store[key][0].pop(0)
        conn.send(resp_array_encoder([key, element]))

    return resp_encoder(count)  # return original count
