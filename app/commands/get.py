import time

from app.protocols.encoder import resp_encoder
from app.store import store


def execute(args):
    value, expires_at = store.get(args[1], (None, None))
    if expires_at and expires_at < time.time() * 1000:  # expired
        # del store[args[1]]
        value = None
    return resp_encoder(value)
