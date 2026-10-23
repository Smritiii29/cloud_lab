
class Process:
    def __init__(self, name, process_id, total_processes):
        self.name = name
        self.process_id = process_id
        self.vector = [0] * total_processes

    def local_event(self):
        self.vector[self.process_id] += 1
        print(f"{self.name}: Local event -> Vector = {self.vector}")

    def send_message(self):
        self.vector[self.process_id] += 1
        message_vector = self.vector.copy()
        print(f"{self.name}: Sending message -> Vector = {message_vector}")
        return message_vector

    def receive_message(self, received_vector):
        for i in range(len(self.vector)):
            self.vector[i] = max(
                self.vector[i], received_vector[i]
            )

        self.vector[self.process_id] += 1
        print(
            f"{self.name}: Received message "
            f"-> Vector = {self.vector}"
        )


# Create two processes: IDs 0 and 1
P1 = Process("P1", 0, 2)
P2 = Process("P2", 1, 2)

# P1 performs an event and sends a message
P1.local_event()
message = P1.send_message()

# P2 receives the message
P2.receive_message(message)

# P2 performs an event and sends a reply
P2.local_event()
reply = P2.send_message()

# P1 receives the reply
P1.receive_message(reply)

# nano script.sh

# for i in {1..6}; do
#     echo "Hello Selcia" >> /home/ubuntu/output.log
#     sleep 10
# done

# chmod +x script.sh

# crontab -e

# * * * * * /home/ubuntu/script.sh

# tail -f /home/ubuntu/output.log

# cat /home/ubuntu/output.log (Verification)