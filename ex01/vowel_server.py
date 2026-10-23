import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8000))
server.listen(1)

print("Server waiting for client...")
conn, addr = server.accept()
print("Connected to:", addr)

message = conn.recv(1024).decode()
print("Received text:", message)

vowels = set("aeiou")
distinct_vowels = set(message.lower()) & vowels

result = f"Number of distinct vowels: {len(distinct_vowels)}"
conn.sendall(result.encode())

conn.close()
server.close()