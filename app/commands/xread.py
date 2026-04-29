import time
from collections import deque
from app.store import store, xread_waiting
from app.protocols.encoder import resp_encoder, resp_entry_encoder


def parse_id(entry_id):
    ms, seq = entry_id.split(b"-")
    return int(ms), int(seq)


def build_response(key, entries, start):
    stream_entries = b""
    count = 0
    for entry_id, fields in entries:
        if parse_id(entry_id) > start:
            stream_entries += resp_entry_encoder(entry_id, fields)
            count += 1
    if not count:
        return None
    return (
        b"*1\r\n*2\r\n"
        + resp_encoder(key)
        + b"*"
        + str(count).encode()
        + b"\r\n"
        + stream_entries
    )


def execute(args, conn=None):
    block_ms = None
    if args[1].upper() == b"BLOCK":
        block_ms = int(args[2])
        args = [args[0]] + list(args[3:])  # strip BLOCK <ms>

    streams_idx = next(i for i, a in enumerate(args) if a.upper() == b"STREAMS") + 1
    half = (len(args) - streams_idx) // 2
    keys = args[streams_idx : streams_idx + half]
    ids = args[streams_idx + half :]

    # try immediate response first
    result = b""
    count = 0
    for key, start_id in zip(keys, ids):
        entries, _ = store.get(key, ([], None))
        start = parse_id(start_id)
        stream_result = build_response(key, entries, start)
        if stream_result:
            result += stream_result
            count += 1

    if count:
        return b"*" + str(count).encode() + b"\r\n" + result

    # block if requested
    if block_ms is not None and conn:
        deadline = time.time() + block_ms / 1000 if block_ms > 0 else None
        for key, start_id in zip(keys, ids):
            xread_waiting.setdefault(key, deque()).append(
                (conn, parse_id(start_id), deadline)
            )
        return None

    return b"*0\r\n"
