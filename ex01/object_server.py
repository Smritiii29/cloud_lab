
import socket
import pickle
import struct
from data_object import DataObject

HOST = "127.0.0.1"
PORT = 8001


def receive_exact(conn, size):
    data = b""

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            return None

        data += chunk

    return data


def receive_packet(conn):
    header = receive_exact(conn, 4)

    if header is None:
        return None

    size = struct.unpack("!I", header)[0]
    return receive_exact(conn, size)


def send_packet(conn, data):
    header = struct.pack("!I", len(data))
    conn.sendall(header + data)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Object server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    with conn:
        print(f"Connected to client: {addr}")

        try:
            raw_data = receive_packet(conn)

            if raw_data is None:
                continue

            obj = pickle.loads(raw_data)

            if not isinstance(obj, DataObject):
                send_packet(
                    conn, b"Error: Invalid data object"
                )
                continue

            print(f"Received object: {obj}")
            total = sum(obj.values)

            response = (
                f"Hello {obj.name}! Sum of values = {total}"
            )

            send_packet(conn, response.encode())
            print(f"Sent response: {response}")

        except (pickle.UnpicklingError, AttributeError,
                EOFError, ValueError, TypeError) as error:
            print(f"Could not process data: {error}")
