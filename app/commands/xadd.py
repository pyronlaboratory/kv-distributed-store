from app.store import store
from app.protocols.encoder import resp_encoder

ERR_SMALL = b"-ERR The ID specified in XADD is equal or smaller than the target stream top item\r\n"
ERR_ZERO = b"-ERR The ID specified in XADD must be greater than 0-0\r\n"


def resolve_id(entry_id, entries):
    ms, seq = entry_id.split(b"-")
    ms = int(ms)

    if seq == b"*":
        if entries:
            last_ms, last_seq = parse_id(entries[-1][0])
            seq = last_seq + 1 if last_ms == ms else 0
        else:
            seq = 1 if ms == 0 else 0
    else:
        seq = int(seq)

    return ms, seq


def parse_id(entry_id):
    ms, seq = entry_id.split(b"-")
    return int(ms), int(seq)


def execute(args):
    key, entry_id = args[1], args[2]
    entries, _ = store.get(key, ([], None))
    ms, seq = resolve_id(entry_id, entries)

    if (ms, seq) == (0, 0):
        return ERR_ZERO
    if entries and (ms, seq) <= parse_id(entries[-1][0]):
        return ERR_SMALL

    resolved_id = f"{ms}-{seq}".encode()
    if key not in store:
        store[key] = ([], None)
    store[key][0].append(
        (resolved_id, {args[i]: args[i + 1] for i in range(3, len(args), 2)})
    )
    return resp_encoder(resolved_id)
