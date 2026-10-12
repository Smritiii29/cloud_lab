import socket
import threading
import time
import sys

ME = int(sys.argv[1])
N = 3
PORT = 7000 + ME

replies = 0
requesting = False
deferred = []

def send(pid, msg):
    try:
        s = socket.socket()
        s.connect(("localhost", 7000 + pid))
        s.send(msg.encode())
        s.close()
    except:
        pass

def handle(msg):
    global replies

    parts = msg.split()

    if parts[0] == "REQUEST":
        pid = int(parts[1])

        print("REQUEST from P%d" % pid)

        if requesting:
            deferred.append(pid)
        else:
            send(pid, "REPLY %d" % ME)

    elif parts[0] == "REPLY":
        replies += 1
        print("REPLY from P%d (%d/%d)" % (int(parts[1]), replies, N - 1))

def listener():
    server = socket.socket()
    server.bind(("localhost", PORT))
    server.listen(5)
    server.settimeout(1)

    try:
        while True:
            try:
                conn, addr = server.accept()
                msg = conn.recv(1024).decode()
                conn.close()
                handle(msg)
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

threading.Thread(target=listener, daemon=True).start()

print("Process", ME, "started")

try:
    while True:

        input("Press Enter to request Critical Section...")

        requesting = True
        replies = 0

        for i in range(1, N + 1):
            if i != ME:
                send(i, "REQUEST %d" % ME)

        while replies < N - 1:
            time.sleep(0.1)

        print(">>> P%d ENTERED Critical Section" % ME)
        time.sleep(5)
        print("<<< P%d LEFT Critical Section" % ME)

        requesting = False

        for pid in deferred:
            send(pid, "REPLY %d" % ME)

        deferred.clear()

except KeyboardInterrupt:
    print("\nProcess stopped.")