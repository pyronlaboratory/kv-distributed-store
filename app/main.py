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
        args = resp_decoder(data)
        command = args[0].upper()  # command
        if command == b"PING":
            conn.send(b"+PONG\r\n")
        if command == b"ECHO":
            conn.send(resp_encoder(args[1]))
    else:
        print("closing", conn)
        sel.unregister(conn)
        conn.close()


def resp_decoder(data):
    input = data.split(b"\r\n")
    it = iter(input)
    length = int(next(it)[1:])  # *N
    return [next(it) for _ in (next(it) for _ in range(length))]  # skip $N, yield value


def resp_encoder(value):
    match value:
        case int():
            return b":" + str(value).encode() + b"\r\n"
        case None:
            return b"$-1\r\n"
        case str():
            value = value.encode()
        case bytes():
            pass
    return b"$" + str(len(value)).encode() + b"\r\n" + value + b"\r\n"


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
