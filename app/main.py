import time
import socket  # noqa: F401
import selectors

from app.protocols.decoder import resp_decoder
from app.commands import COMMANDS
from app.store import waiting

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1024)
    if data:
        args = resp_decoder(data)
        command = args[0].upper()  # command

        handler = COMMANDS.get(command)
        if handler:
            if command == b"BLPOP":
                response = handler(args, conn)  # pass conn
            else:
                response = handler(args)

            if response:
                conn.send(response)
    else:
        print("closing", conn)
        sel.unregister(conn)
        conn.close()


def check_expired_waiters():
    now = time.time()
    for key, waiters in list(waiting.items()):
        expired = [(c, d) for c, d in waiters if d and now >= d]
        for conn, deadline in expired:
            waiters.remove((conn, deadline))
            conn.send(b"*-1\r\n")


def get_next_timeout():
    deadlines = [d for waiters in waiting.values() for _, d in waiters if d]
    if not deadlines:
        return None
    return max(0, min(deadlines) - time.time())


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, accept)

    while True:
        events = sel.select(timeout=get_next_timeout())
        check_expired_waiters()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == "__main__":
    main()
