store = {}  # in-memory store

waiting = {}  # for BLPOP: key -> deque of (conn, deadline)
xread_waiting = {}  # for XREAD BLOCK: key -> deque of (conn, start_id, deadline)
