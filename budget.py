class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    def deposit(self, amount, description=""):
        self.ledger.append({"amount" : amount, "description" : description})
    def withdraw(self, amount, description=""):
        neg_amount = -1 * amount
        total = 0
        for dict in self.ledger:
            total += dict["amount"]
        if self.check_funds(amount):
            self.ledger.append({"amount" : neg_amount, "description" : description})
            return True
        else:
            return False
    def calc_withdrawals(self):
        total = 0
        for dict in self.ledger:
            if dict["amount"] < 0:
                total += dict["amount"]
        return -1 * total
    def get_balance(self):
        total = 0
        for dict in self.ledger:
            total += dict["amount"]
        return total
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True
    def __str__(self):
        title = f"{self.name:*^30}\n"
        products = ""
        total = 0
        for product in self.ledger:
            products += f"{product['description'][0:23]:23}" + f"{product['amount']:>7.2f}" + '\n'
            total += product["amount"]
        receipt = title + products + 'Total: ' + str(total)
        return receipt

def create_spend_chart(categories):
    bar_chart = "Percentage spent by category\n"
    y_value = 100
    total = 0
    cat_names_withdrawals = {}
    cat_names_percent = {}
    cat_names = []

    for category in categories:
        if category.calc_withdrawals() != 0:
            cat_names.append(category.name)
            total += category.calc_withdrawals()
            cat_names_withdrawals[category.name] = category.calc_withdrawals()
            print(category.name)
    while y_value <= 100 and y_value != -10:
        if y_value < 100:
            y_axis = str(y_value).rjust(3) + "| "
        else:
            y_axis = str(y_value) + "| "
        bar_chart += y_axis
        for i in range(len(categories)):
            cat_percent = cat_names_withdrawals[categories[i].name] / total * 100
            cat_names_percent[categories[i].name] = cat_percent
            if cat_names_percent[categories[i].name] >= y_value:
                bar_chart += "o  "
            else:
                bar_chart += "   "
        bar_chart += "\n"
        y_value -= 10
    
    x_axis = "    -" + ("---"*len(categories)) + "\n     "
    longest_cat_name = max(cat_names, key=len)
    for x in range(len(longest_cat_name)):
        for category in categories:
            difference = len(longest_cat_name) - len(category.name)
            if difference != 0:
                category.name += " " * difference
            x_axis = x_axis + category.name[x] + "  "
        x_axis = x_axis + "\n     " if x != len(longest_cat_name) else x_axis
    bar_chart += x_axis
    bar_chart = bar_chart.strip() + "  "

    return bar_chart
