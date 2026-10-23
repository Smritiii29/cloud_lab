
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

# //on vm1(target)
# sudo apt update 
# sudo apt install openssh-server -y 
# sudo systemctl enable --now ssh

# sudo mkdir -p /var/www/html/site2 (on vm1)
# //on vm2
# //first check what files exist
# ls -l /var/www/html
# //transfer files
# rsync -av /var/www/html/ username@VM1_IP:~/vm2-site/(to get username try whoami)
# //now again on vm1 
# sudo cp -r ~/vm2-site/. /var/www/html/site2/

# //to verify if two servers are suitable for consolidation 
# //check cpu, memory , disk storage , file compatability 
# free -h //memory
# top //cpu 
# df -h //filesystem space avail
# du -sh /var/www/html //size of website directory
