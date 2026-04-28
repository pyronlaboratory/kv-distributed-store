import socket  # noqa: F401


def main():
    # print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        sock, _ = server_socket.accept()
        data = sock.recv(1024).strip()
        if data.startswith(b"*1\r\n$4\r\nPING\r\n"):
            response = b"+PONG\r\n"
            sock.sendall(response)
        sock.close()


if __name__ == "__main__":
    main()
