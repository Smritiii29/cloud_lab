
class Process:
    def __init__(self, name):
        self.name = name
        self.clock = 0

    def local_event(self):
        self.clock += 1
        print(f"{self.name}: Local event -> Clock = {self.clock}")

    def send_message(self):
        self.clock += 1
        timestamp = self.clock
        print(f"{self.name}: Sending message -> Timestamp = {timestamp}")
        return timestamp

    def receive_message(self, timestamp):
        self.clock = max(self.clock, timestamp) + 1
        print(
            f"{self.name}: Received message "
            f"(Timestamp = {timestamp}) -> Clock = {self.clock}"
        )


# Create two processes
P1 = Process("P1")
P2 = Process("P2")

# Events in P1
P1.local_event()
timestamp = P1.send_message()

# P2 receives the message
P2.receive_message(timestamp)

# Another local event in P2
P2.local_event()

# P2 sends a message back
timestamp = P2.send_message()

# P1 receives the message
P1.receive_message(timestamp)
