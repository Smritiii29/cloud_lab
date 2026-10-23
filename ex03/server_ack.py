
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

clients = []
lock = threading.Lock()


def handle_client(client_socket, addr):
    print(f"[Connected] {addr}")

    try:
        while True:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            # Handle acknowledgement separately
            if data.startswith("ACK:"):
                print(f"[Confirmation received by server] {addr}: {data[4:]}")
                continue

            if data.lower().strip() == "bye":
                break

            print(f"[Message from {addr}] {data}")

            # Copy the recipient list safely
            with lock:
                recipients = [
                    client for client in clients
                    if client != client_socket
                ]

            # Broadcast to all other clients
            for recipient in recipients:
                try:
                    recipient.sendall(
                        f"MSG:{addr}: {data}".encode()
                    )
                except OSError:
                    pass

            # Confirm to the original sender
            client_socket.sendall(
                b"SERVER: Message broadcast successfully."
            )

    except OSError:
        pass

    finally:
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)

        client_socket.close()
        print(f"[Disconnected] {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()

    with lock:
        clients.append(client_socket)

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, addr),
        daemon=True
    )
    thread.start()
