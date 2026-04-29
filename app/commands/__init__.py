from . import ping, echo, set, get, rpush, lrange, lpush, lpop, llen, blpop, type

COMMANDS = {
    b"PING": ping.execute,
    b"ECHO": echo.execute,
    b"SET": set.execute,
    b"GET": get.execute,
    b"RPUSH": rpush.execute,
    b"LPUSH": lpush.execute,
    b"LRANGE": lrange.execute,
    b"LPOP": lpop.execute,
    b"LLEN": llen.execute,
    b"BLPOP": blpop.execute,
    b"TYPE": type.execute,
}
