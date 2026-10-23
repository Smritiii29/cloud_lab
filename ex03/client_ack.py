
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to the server.")
print("Type a message to broadcast to other clients.")
print("Type 'bye' to disconnect.")


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            if data.startswith("MSG:"):
                print(f"\nMessage received: {data[4:]}")

                # Send acknowledgement back to the server
                client_socket.sendall(
                    b"ACK: Message received successfully."
                )

            else:
                print(f"\n{data}")

        except OSError:
            break


receiver = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True
)
receiver.start()

try:
    while True:
        message = input("You: ").strip()

        if not message:
            continue

        client.sendall(message.encode())

        if message.lower() == "bye":
            break

finally:
    client.close()
    print("Disconnected.")
