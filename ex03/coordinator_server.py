
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 9200

# Tracks whether the critical section is occupied
cs_busy = False

# Ensures only one client changes the coordinator's state at a time
state_lock = threading.Lock()


def handle_client(conn, addr):
    global cs_busy

    with conn:
        request = conn.recv(1024).decode().strip()

        if request == "REQUEST":
            print(f"Request received from {addr}")

            # Check and update CS status safely
            with state_lock:
                if not cs_busy:
                    cs_busy = True
                    response = "GRANT"
                else:
                    response = "DENY"

            conn.sendall(response.encode())

            if response == "GRANT":
                print("Permission granted.")
            else:
                print("CS busy. Permission denied.")

        elif request == "RELEASE":
            with state_lock:
                cs_busy = False

            print("Critical section released.")


def start_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print(f"Coordinator running on port {PORT}")

    while True:
        conn, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()


start_server()
