
import socket
import threading
import time
import sys

HOST = "127.0.0.1"

NODES = {
    1: 9101,
    2: 9102,
    3: 9103
}

# Get this process's ID
if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 token_ring.py <1|2|3>")

my_id = int(sys.argv[1])

if my_id not in NODES:
    raise SystemExit("Process ID must be 1, 2, or 3.")

my_port = NODES[my_id]

# Define the next process in the ring
next_process = {
    1: 2,
    2: 3,
    3: 1
}

has_token = False
state_lock = threading.Lock()
token_event = threading.Event()


def send_message(to_port, message):
    """Send a message to another process."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        s.connect((HOST, to_port))
        s.sendall(message.encode())


def handle_message(message):
    """Handle an incoming token."""
    global has_token

    parts = message.split()

    if not parts:
        return

    if parts[0] == "TOKEN":
        with state_lock:
            has_token = True

        print(f"[P{my_id}] Received the token.")
        token_event.set()


def listen_for_messages():
    """Listen for incoming messages."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, my_port))
    server.listen()

    print(f"[P{my_id}] Listening on port {my_port}")

    while True:
        conn, addr = server.accept()

        with conn:
            data = conn.recv(1024).decode()

        if data:
            try:
                handle_message(data)
            except (ValueError, IndexError, OSError) as error:
                print(f"[P{my_id}] Message error: {error}")


def request_critical_section():
    """Wait for token, enter CS, then pass token onward."""
    global has_token

    print(f"[P{my_id}] Waiting for the token...")

    # Wait until the token reaches this process
    token_event.wait()

    with state_lock:
        if not has_token:
            return

        has_token = False
        token_event.clear()

    print(f"[P{my_id}] >>> ENTERING CRITICAL SECTION")
    time.sleep(3)
    print(f"[P{my_id}] <<< EXITING CRITICAL SECTION")

    # Pass token to the next process
    next_id = next_process[my_id]

    try:
        send_message(
            NODES[next_id],
            "TOKEN"
        )
        print(f"[P{my_id}] Passed token to P{next_id}.")

    except OSError as error:
        print(f"[P{my_id}] Could not pass token: {error}")

        # Restore the token locally if transfer failed
        with state_lock:
            has_token = True
        token_event.set()


# Start the listener
listener = threading.Thread(
    target=listen_for_messages,
    daemon=True
)
listener.start()

# Give the listener time to start
time.sleep(0.5)

# P1 creates the initial token
if my_id == 1:
    has_token = True
    token_event.set()
    print("[P1] Created the initial token.")

print(f"[P{my_id}] Ready.")
print("Press Enter to request the critical section.")
print("Type 'exit' to stop.")

while True:
    try:
        choice = input(f"[P{my_id}] Your choice: ").strip()

        if choice.lower() == "exit":
            break

        request_critical_section()

    except (ConnectionRefusedError, OSError) as error:
        print(f"[P{my_id}] Communication error: {error}")
