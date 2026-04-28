import socket  # noqa: F401
import selectors

from app.protocols.decoder import resp_decoder
from app.commands import echo, ping, get, set

COMMANDS = {
    b"PING": ping.execute,
    b"ECHO": echo.execute,
    b"SET": set.execute,
    b"GET": get.execute,
}

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
            conn.send(handler(args))
    else:
        print("closing", conn)
        sel.unregister(conn)
        conn.close()


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == "__main__":
    main()
