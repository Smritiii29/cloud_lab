import socket
import pickle
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8001))

numbers = list(map(int, input("Enter integers separated by spaces: ").split()))

# Serialize the list into bytes
data = pickle.dumps(numbers)

# Send the data length first, then the serialized data
client.sendall(struct.pack("!I", len(data)))
client.sendall(data)

# Receive the server's sum message
message = client.recv(1024).decode()
print("Server response:", message)

client.close()