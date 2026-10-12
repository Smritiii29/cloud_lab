
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

clients = []


def handle_client(client_socket, addr):
    print(f"[Connected] {addr}")

    while True:
        try:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            print(f"[{addr}] {data}")

            if data.lower().strip() == "bye":
                break

            # Send the message to every other connected client
            for client in clients:
                if client != client_socket:
                    try:
                        client.sendall(f"[{addr}] {data}".encode())
                    except OSError:
                        pass

        except OSError:
            break

    print(f"[Disconnected] {addr}")

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, addr)
    )
    thread.start()
