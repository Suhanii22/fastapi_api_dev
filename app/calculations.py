

def add(num1: int, num2 : 2):
    return num1 + num2 


class InsufficintFunds(Exception):
    pass

class BankAccount():
    def __init__(self , starting_balance=0):
        self.balance = starting_balance

    def deposit(self,amount):
        self.balance += amount

    def withdraw(self,amount):
        if amount > self.balance:
        #    raise Exception("Insufficient funds in ac")
             raise InsufficintFunds("Insufficient funds in ac")
        self.balance -= amount

    def collect_intrest(self):
        self.balance *= 1.1            
        