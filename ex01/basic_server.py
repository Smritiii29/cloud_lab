
import socket

HOST = "127.0.0.1"
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected to client: {addr}")

    with conn:
        stream = conn.makefile("rwb")

        while True:
            message = stream.readline()

            if not message:
                break

            text = message.decode().strip()

            if text.lower() == "exit":
                stream.write(b"Connection closed\n")
                stream.flush()
                break

            try:
                numbers = [int(x) for x in text.split()]
                total = sum(numbers)

                print(f"Received numbers: {numbers}")
                print(f"Sum: {total}")

                response = f"Sum = {total}\n"
            except ValueError:
                response = "Error: Enter integers separated by spaces\n"

            stream.write(response.encode())
            stream.flush()

    print("Client disconnected")
