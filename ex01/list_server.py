import socket
import pickle
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8001))
server.listen(1)

print("Server waiting for client...")
conn, addr = server.accept()
print("Connected to:", addr)

# Receive the length of the serialized data
header = conn.recv(4)
length = struct.unpack("!I", header)[0]

# Receive the complete serialized list
data = b""
while len(data) < length:
    data += conn.recv(length - len(data))

# Deserialize bytes into a Python list
numbers = pickle.loads(data)
print("Received list:", numbers)

# Calculate sum and send as a message
message = f"Sum of list = {sum(numbers)}"
conn.sendall(message.encode())

conn.close()
server.close()