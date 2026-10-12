import socket
import threading
import time
import sys

HOST = "127.0.0.1"

NODES = {
    1: 9001,
    2: 9002,
    3: 9003
}

# Get this process's ID from the command line
my_id = int(sys.argv[1])

if my_id not in NODES:
    raise SystemExit("Process ID must be 1, 2, or 3.")

my_port = NODES[my_id]

# State maintained by this process
clock = 0
requesting_cs = False
in_cs = False
request_timestamp = 0

replies_received = set()
deferred_replies = []

state_lock = threading.Lock()


def send_message(to_port, message):
    """Send one message to another process."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, to_port))
        s.sendall(message.encode())


def handle_message(message):
    """Process an incoming REQUEST or REPLY message."""
    global clock

    parts = message.split()
    if not parts:
        return

    if parts[0] == "REQUEST":
        sender_id = int(parts[1])
        sender_timestamp = int(parts[2])

        with state_lock:
            clock = max(clock, sender_timestamp) + 1

            # The request with the smaller (timestamp, process ID)
            # has higher priority.
            own_priority = (request_timestamp, my_id)
            incoming_priority = (sender_timestamp, sender_id)

            defer = (
                in_cs
                or (
                    requesting_cs
                    and own_priority < incoming_priority
                )
            )

            if defer:
                deferred_replies.append(sender_id)
                print(
                    f"[P{my_id}] Deferred reply to P{sender_id}"
                )
            else:
                print(f"[P{my_id}] Replying to P{sender_id}")

        if not defer:
            send_message(
                NODES[sender_id],
                f"REPLY {my_id}"
            )

    elif parts[0] == "REPLY":
        sender_id = int(parts[1])

        with state_lock:
            replies_received.add(sender_id)

        print(f"[P{my_id}] Received REPLY from P{sender_id}")


def listen_for_messages():
    """Listen for messages from other processes."""
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
    """Request permission, enter CS, then release it."""
    global clock, requesting_cs, in_cs, request_timestamp

    with state_lock:
        clock += 1
        request_timestamp = clock
        requesting_cs = True
        replies_received.clear()

        my_timestamp = request_timestamp

    print(
        f"[P{my_id}] Requesting CS "
        f"with timestamp {my_timestamp}"
    )

    # Request permission from every other process
    for process_id, port in NODES.items():
        if process_id != my_id:
            send_message(
                port,
                f"REQUEST {my_id} {my_timestamp}"
            )

    # Wait until every other process has replied
    while True:
        with state_lock:
            if len(replies_received) == len(NODES) - 1:
                in_cs = True
                break

        time.sleep(0.05)

    print(f"[P{my_id}] >>> ENTERING CRITICAL SECTION")
    time.sleep(3)  # Simulate work in the protected section
    print(f"[P{my_id}] <<< EXITING CRITICAL SECTION")

    # Release the CS and send any deferred replies
    with state_lock:
        in_cs = False
        requesting_cs = False

        waiting_processes = list(deferred_replies)
        deferred_replies.clear()

    for process_id in waiting_processes:
        send_message(
            NODES[process_id],
            f"REPLY {my_id}"
        )
        print(f"[P{my_id}] Sent deferred REPLY to P{process_id}")


# Start the listener in the background
listener = threading.Thread(
    target=listen_for_messages,
    daemon=True
)
listener.start()

# Give the listener time to start
time.sleep(0.5)

print(f"[P{my_id}] Ready.")
print("Press Enter to request the critical section.")
print("Type 'exit' to stop this process.")

while True:
    try:
        choice = input(f"[P{my_id}] Your choice: ").strip()

        if choice.lower() == "exit":
            break

        request_critical_section()

    except (ConnectionRefusedError, OSError) as error:
        print(f"Communication error: {error}")
        print("Check that all three processes are running.")
        time.sleep(1)
