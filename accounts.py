class Account:
    def __init__(self, name, password, balance):
        self.name = name
        self.password = password
        self.balance = balance
        self.unlimited_money = False

    def send_money(self, money, other):
        if not self.unlimited_money and money > self.balance:
            return False
        self.balance -= money
        other.balance += money
        return True


accounts = {"admin": Account("admin", "admin", 0)}

accounts["admin"].unlimited_money = True
