# 预算应用
class Category:
    # 初始化
    def __init__(self, name):
        # 类别
        self.name = name
        # 余额
        self.balance = 0
        # 账单
        self.ledger = []

    # 打印预算对象
    def __repr__(self):
        # 格式化标题
        def title_format(name):
            name_len = len(name)
            left_len = (30 - name_len) // 2
            right_len = 30 - name_len - left_len
            return '*' * left_len + name + '*' * right_len + '\n'

        # 格式化账单
        def record_format(rec):
            description = rec['description']
            amount = rec['amount']
            des_len = len(description)
            if des_len >= 23:
                des_format = description[0:23]
            else:
                des_format = description + ' ' * (23 - des_len)
            amount_format = '%7.2f' % amount
            return des_format + amount_format + '\n'

        # 标题
        new_string = title_format(self.name)
        # 账单
        for record in self.ledger:
            new_string += record_format(record)
        # 余额
        new_string += 'Total: %.2f' % self.balance

        return new_string

    # 存款
    def deposit(self, amount, description=""):
        self.balance += amount
        record = dict()
        record["amount"] = amount
        record["description"] = description
        self.ledger.append(record)

    # 取款
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.balance -= amount
            record = dict()
            record["amount"] = -amount
            record["description"] = description
            self.ledger.append(record)
            return True
        else:
            return False

    # 查询余额
    def get_balance(self):
        return self.balance

    # 转账
    def transfer(self, amount, account):
        if self.check_funds(amount):
            # 更新self账户
            self.balance -= amount
            record1 = dict()
            record1["amount"] = -amount
            record1["description"] = 'Transfer to ' + account.name
            self.ledger.append(record1)
            # 更新account账户
            account.balance += amount
            record2 = dict()
            record2["amount"] = amount
            record2["description"] = 'Transfer from ' + self.name
            account.ledger.append(record2)
            return True
        else:
            return False

    # 检查余额
    def check_funds(self, funds):
        result = False if funds > self.balance else True
        return result


def create_spend_chart(categories):
    # 类别名字列表
    names = list()
    # 类别花销字典
    spend_sums = dict()
    # 所有类别的总花销
    total = 0
    # 遍历categories
    for category in categories:
        # 更新类别名字列表
        names.append(category.name)
        # 计算该类别总花销
        spend_sum = 0
        for record in category.ledger:
            if record["amount"] < 0:
                spend_sum += abs(record["amount"])
        # 更新类别花销字典
        spend_sums[category.name] = spend_sum
        # 更新所有类别的总花销
        total += spend_sum
    # 所有类别花销占比
    percentages = dict()
    for name in names:
        percentages[name] = int(spend_sums[name] / total * 10)
    print(percentages)
    # 最长的名字的长度
    name_maxlen = len(max(names, key=len))
    # 类别的数量
    categories_len = len(categories)
    rows = ['Percentage spent by category',
            '100| ',
            ' 90| ',
            ' 80| ',
            ' 70| ',
            ' 60| ',
            ' 50| ',
            ' 40| ',
            ' 30| ',
            ' 20| ',
            ' 10| ',
            '  0| ',
            '    -']
    # 扩展行
    for i in range(name_maxlen):
        rows.append(' ' * 5)
    # 补分割线
    rows[12] += '---' * categories_len
    # 把o加上去
    for name in names:
        perc = percentages[name]
        for i in range(1, 11 - perc):
            rows[i] += '   '
        for i in range(11 - perc, 12):
            rows[i] += 'o  '
    # 把类别名字加上去
    for name in names:
        # 补名字
        for i in range(len(name)):
            rows[13 + i] = rows[13 + i] + name[i] + '  '
        # 补空格
        for i in range(13 + len(name), len(rows)):
            rows[i] += '   '
    # 合并rows
    final_str = str()
    for i in range(len(rows)):
        if i == len(rows) - 1:
            final_str += rows[i]
        else:
            final_str += rows[i] + '\n'

    return final_str


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)
print(create_spend_chart([food, clothing, auto]))
