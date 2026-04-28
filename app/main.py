import socket  # noqa: F401
import selectors

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()
    print("accepted", conn, "from", addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1024)
    if data:
        if b"*1\r\n$4\r\nPING\r\n" in data:
            conn.send(b"+PONG\r\n")
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
