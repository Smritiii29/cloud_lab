
import socket
import time

HOST = "127.0.0.1"
PORT = 9200


def send_request(message):
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())

        if message == "REQUEST":
            return s.recv(1024).decode()

        return None


print("Requesting permission from coordinator...")

response = send_request("REQUEST")

if response == "GRANT":
    print("Permission granted.")
    print(">>> ENTERING CRITICAL SECTION")

    time.sleep(10)

    print("<<< EXITING CRITICAL SECTION")

    send_request("RELEASE")
    print("Released permission to coordinator.")

else:
    print("Permission denied. Try running the client again later.")
