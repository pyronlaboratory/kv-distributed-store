import socket  # noqa: F401


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        sock, addr = server_socket.accept()
        data = sock.recv(1024).strip()
        print(f"Received data from client: {data}")
        sock.sendall(b"+PONG\r\n")
        sock.close()


if __name__ == "__main__":
    main()
