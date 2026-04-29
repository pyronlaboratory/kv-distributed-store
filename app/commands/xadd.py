from app.store import store
from app.protocols.encoder import resp_encoder

ERR_SMALL = b"-ERR The ID specified in XADD is equal or smaller than the target stream top item\r\n"
ERR_ZERO = b"-ERR The ID specified in XADD must be greater than 0-0\r\n"


def parse_id(entry_id):
    ms, seq = entry_id.split(b"-")
    return int(ms), int(seq)


def execute(args):
    key, entry_id = args[1], args[2]
    ms, seq = parse_id(entry_id)

    if (ms, seq) == (0, 0):
        return ERR_ZERO

    entries, _ = store.get(key, ([], None))

    if entries:
        last_ms, last_seq = parse_id(entries[-1][0])
        if (ms, seq) <= (last_ms, last_seq):
            return ERR_SMALL

    if key not in store:
        store[key] = ([], None)
    store[key][0].append(
        (entry_id, {args[i]: args[i + 1] for i in range(3, len(args), 2)})
    )
    return resp_encoder(entry_id)
