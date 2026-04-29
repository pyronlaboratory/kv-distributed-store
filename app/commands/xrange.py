from app.store import store
from app.protocols.encoder import resp_entry_encoder


def parse_bound(bound, default_seq):
    if bound == b"-":
        return (0, 0)
    if b"-" in bound:
        ms, seq = bound.split(b"-")
        return int(ms), int(seq)
    return int(bound), default_seq


def execute(args):
    key, start, end = args[1], args[2], args[3]
    entries, _ = store.get(key, ([], None))

    start_id = parse_bound(start, 0)
    end_id = parse_bound(end, float("inf"))

    result = b""
    count = 0
    for entry_id, fields in entries:
        ms, seq = int(entry_id.split(b"-")[0]), int(entry_id.split(b"-")[1])
        if start_id <= (ms, seq) <= end_id:
            result += resp_entry_encoder(entry_id, fields)
            count += 1

    return b"*" + str(count).encode() + b"\r\n" + result
