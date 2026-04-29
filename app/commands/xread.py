from app.store import store
from app.protocols.encoder import resp_encoder, resp_entry_encoder


def parse_id(entry_id):
    ms, seq = entry_id.split(b"-")
    return int(ms), int(seq)


def execute(args):
    # args: [XREAD, STREAMS, key1, key2..., id1, id2...]
    streams_idx = next(i for i, a in enumerate(args) if a.upper() == b"STREAMS") + 1
    half = (len(args) - streams_idx) // 2
    keys = args[streams_idx : streams_idx + half]
    ids = args[streams_idx + half :]

    result = b""
    count = 0
    for key, start_id in zip(keys, ids):
        entries, _ = store.get(key, ([], None))
        start = parse_id(start_id)

        stream_entries = b""
        entry_count = 0
        for entry_id, fields in entries:
            if parse_id(entry_id) > start:
                stream_entries += resp_entry_encoder(entry_id, fields)
                entry_count += 1

        if entry_count:
            result += b"*2\r\n" + resp_encoder(key)
            result += b"*" + str(entry_count).encode() + b"\r\n" + stream_entries
            count += 1

    return b"*" + str(count).encode() + b"\r\n" + result
