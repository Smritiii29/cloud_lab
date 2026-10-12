import socket
import threading
import sys
import time

ME = int(sys.argv[1])
N = 3

NEXT = ME % N + 1
PORT = 8000 + ME

want = False

def send_token():
    try:
        s = socket.socket()
        s.connect(("localhost", 8000 + NEXT))
        s.send(b"TOKEN")
        s.close()
    except:
        pass

def use_token():
    global want

    print("P%d received TOKEN" % ME)

    if want:
        print("P%d ENTERED Critical Section" % ME)
        time.sleep(3)
        print("P%d LEFT Critical Section" % ME)
        want = False

    print("P%d passed TOKEN to P%d" % (ME, NEXT))
    time.sleep(1)
    send_token()

def request_cs():
    global want

    while True:
        try:
            input("Press Enter to request Critical Section...")
            want = True
        except KeyboardInterrupt:
            break

threading.Thread(target=request_cs, daemon=True).start()

server = socket.socket()
server.bind(("localhost", PORT))
server.listen(5)
server.settimeout(1)

print("Process", ME, "started")

# Process 1 starts with the token
if ME == 1:
    time.sleep(2)
    use_token()

try:
    while True:
        try:
            conn, addr = server.accept()
            msg = conn.recv(1024).decode()
            conn.close()

            if msg == "TOKEN":
                use_token()

        except socket.timeout:
            pass

except KeyboardInterrupt:
    print("\nProcess stopped.")

finally:
    server.close()