from . import ping, echo, set, get, rpush, lrange

COMMANDS = {
    b"PING": ping.execute,
    b"ECHO": echo.execute,
    b"SET": set.execute,
    b"GET": get.execute,
    b"RPUSH": rpush.execute,
    b"LRANGE": lrange.execute,
}
