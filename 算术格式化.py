# 导入正则表达式模块
import re


# 主函数
def arithmetic_arranger(problems, answer=False):
    # count是数学式子的数量
    count = len(problems)

    # 参数异常判定
    if count > 5:
        return 'Error: Too many problems.'

    # 声明六个空列表
    num1s = list()  # 第一个数
    num2s = list()  # 第二个数
    operators = list()  # 运算符
    dashes = list()  # 破折号
    lengths = list()  # 式子的长度
    results = list()  # 运算结果

    # 正则表达式
    re_numb = r'[0-9]+'  # 用于提取数
    re_oper = r'[+-]'  # 用于提取运算符
    re_1 = r'[/*]'  # 用于异常判定（乘除无效）
    re_2 = r'[^0-9+-]'  # 用于异常判定（数字以外无效）

    # 遍历所有数学式子
    for problem in problems:

        # 参数异常判定
        problem = problem.replace(' ', '')
        if re.search(re_1, problem) is not None:
            return "Error: Operator must be '+' or '-'."
        if re.search(re_2, problem) is not None:
            return 'Error: Numbers must only contain digits.'

        # 提取数和运算符
        numb_list = re.findall(re_numb, problem)
        oper_list = re.findall(re_oper, problem)

        # 该式子占据的长度
        length = maxlen(numb_list[0], numb_list[1]) + 2

        # 参数异常判定
        if length - 2 > 4:
            return 'Error: Numbers cannot be more than four digits.'

        # 第一个数放进num1s
        num1s.append(numb_list[0])
        # 第二个数放进num2s
        num2s.append(numb_list[1])
        # 运算符放进operators
        operators.append(oper_list[0])
        # 长度放进lengths
        lengths.append(length)
        # 根据数的长度生成破折号放进dashes
        dashes.append(makedash(length))

        # 计算结果，然后把结果放进results

        if oper_list[0] == '+':
            res = int(numb_list[0]) + int(numb_list[1])
        else:
            res = int(numb_list[0]) - int(numb_list[1])
        results.append(str(res))

    # 返回结果总共四行，所以分别声明四个字符串
    row1 = str()
    row2 = str()
    row3 = str()
    row4 = str()

    # 填充四行
    for i in range(count):
        row1 += format1(num1s[i], lengths[i])
        row2 += format2(num2s[i], operators[i], lengths[i])
        row3 += dashes[i]
        row4 += format1(results[i], lengths[i])
        # 每个问题之间有四个空格
        if i != count - 1:
            row1 += '    '
            row2 += '    '
            row3 += '    '
            row4 += '    '

    # 最终结果，每行之间加换行
    arranged_problems = row1 + '\n' + row2 + '\n' + row3
    # 如果参数answer为真就加上答案
    if answer:
        arranged_problems += '\n' + row4
    # 返回结果
    return arranged_problems


# 辅助函数
# 返回两个字符串中最大的长度
def maxlen(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    return len1 if len1 > len2 else len2


# 辅助函数
# 生成指定长度的破折号
def makedash(length):
    dash = str()
    for i in range(length):
        dash += '-'
    return dash


# 辅助函数
# 用于在第一个数或者计算结果前面补空格
def format1(num, length):
    row1 = str()
    len1 = len(num)  # 数的长度
    len2 = length - len1  # 空格长度
    for i in range(len2):
        row1 += ' '
    row1 += num
    return row1


# 辅助函数
# 用于在第二个数前面补运算符和空格
def format2(num2, oper, length):
    row2 = str()
    len1 = len(num2)  # 数的长度
    len2 = length - len1 - 1  # 空格长度
    row2 += oper
    for i in range(len2):
        row2 += ' '
    row2 += num2
    return row2


# 测试函数功能
print(arithmetic_arranger(["32 + 8", "1 - 3801", "9999 + 9999", "523 - 49"], True))
