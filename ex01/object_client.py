
import socket
import pickle
import struct
from data_object import DataObject

HOST = "127.0.0.1"
PORT = 8001


def receive_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Server disconnected")

        data += chunk

    return data


def receive_packet(sock):
    header = receive_exact(sock, 4)
    size = struct.unpack("!I", header)[0]
    return receive_exact(sock, size)


def send_packet(sock, data):
    header = struct.pack("!I", len(data))
    sock.sendall(header + data)


name = input("Enter your name: ")

try:
    values_text = input("Enter integers separated by spaces: ")
    values = [int(x) for x in values_text.split()]

    if not values:
        raise ValueError("Enter at least one integer.")

    obj = DataObject(name, values)
    print("Sending object:", obj)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        serialized_data = pickle.dumps(obj)
        send_packet(client, serialized_data)

        response = receive_packet(client).decode()
        print("Response from server:", response)

except ValueError as error:
    print("Invalid input:", error)
except (ConnectionRefusedError, ConnectionError, OSError) as error:
    print("Connection error:", error)
