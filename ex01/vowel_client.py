import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8000))

message = input("Enter a sentence: ")
client.sendall(message.encode())

result = client.recv(1024).decode()
print("Server response:", result)

client.close()