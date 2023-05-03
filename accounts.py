from datetime import *

class Account:
    def __init__(self, name, password, balance):
        self.name = name
        self.password = password
        self.balance = balance
        self.unlimited_money = False
        self.debt = 0
        self.debt_payment_size = 0
        self.last_debt_payment = datetime.now()

    def send_money(self, money, other):
        if not self.unlimited_money and money > self.balance:
            return False
        self.balance -= money
        other.balance += money
        return True

    def update_debt(self):
        if self.debt == 0:
            return False
        while self.last_debt_payment + timedelta(minutes=5) < datetime.now():
            cpayment = min(self.debt, self.debt_payment_size)
            if cpayment > self.balance:
                return True
            self.debt -= cpayment
            self.balance -= cpayment
            self.debt += ((self.debt + 9) // 10)
            self.last_debt_payment += timedelta(minutes=5)
        return False

    def take_loan(self, size, payment_size):
        if self.debt != 0 or (size + 9) // 10 >= payment_size:
            return False
        self.balance += size
        self.debt = size
        self.debt_payment_size = payment_size
        self.last_debt_payment = datetime.now()
        return True


accounts = {"admin": Account("admin", "admin", 0)}

accounts["admin"].unlimited_money = True
