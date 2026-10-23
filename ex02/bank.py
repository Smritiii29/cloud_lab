
import Pyro4

@Pyro4.expose
class Bank:

    def __init__(self):
        self.balance = 1000

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid deposit amount"

        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid withdrawal amount"

        if amount > self.balance:
            return "Insufficient balance"

        self.balance -= amount
        return self.balance

    def check_balance(self):
        return self.balance
