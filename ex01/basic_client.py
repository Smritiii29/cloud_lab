
import socket

HOST = "127.0.0.1"
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to the server.")
print("Enter integers separated by spaces, or type exit.")

with client:
    stream = client.makefile("rwb")

    while True:
        message = input("Enter numbers: ").strip()

        stream.write((message + "\n").encode())
        stream.flush()

        response = stream.readline().decode().strip()
        print("Server response:", response)

        if message.lower() == "exit":
            break

print("Client closed.")
