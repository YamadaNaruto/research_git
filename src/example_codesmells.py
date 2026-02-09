# smelly_code.py
# 意図的にコードスメルを大量に含むサンプル

import os, sys, json, math, random, datetime  # 未使用importだらけ

GLOBAL_A = 10
GLOBAL_B = 20
GLOBAL_LIST = []


class VeryBadClass:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def do_everything(self, a, b, c, d, e, f, g):  # 引数が多すぎる
        result = 0
        if a > 0:
            if b > 0:
                if c > 0:
                    if d > 0:
                        if e > 0:
                            if f > 0:
                                if g > 0:  # 深すぎるネスト
                                    result = a + b + c + d + e + f + g
                                else:
                                    result = -1
                            else:
                                result = -2
                        else:
                            result = -3
                    else:
                        result = -4
                else:
                    result = -5
            else:
                result = -6
        else:
            result = -7

        for i in range(100):
            for j in range(100):  # 無意味な二重ループ
                result += 1

        return result


def god_function(x):  # 神関数（長すぎ・責務過多）
    total = 0
    data = []
    tmp = None

    for i in range(50):
        if i % 2 == 0:
            total += i
        else:
            total -= i

    for i in range(10):
        for j in range(10):
            for k in range(10):
                total += i + j + k

    if x == 1:
        print("one")
    elif x == 2:
        print("two")
    elif x == 3:
        print("three")
    elif x == 4:
        print("four")
    elif x == 5:
        print("five")
    elif x == 6:
        print("six")
    elif x == 7:
        print("seven")
    elif x == 8:
        print("eight")
    elif x == 9:
        print("nine")
    else:
        print("other")

    try:
        a = 1 / 0  # 例外をわざと発生
    except:
        pass  # 例外握りつぶし

    unused_variable = 12345  # 未使用変数
    data.append(total)
    return total


def duplicate_code_1(a, b):
    if a > b:
        return a - b
    else:
        return b - a


def duplicate_code_2(a, b):  # コード重複
    if a > b:
        return a - b
    else:
        return b - a


def magic_numbers():
    x = 42
    y = 1337
    z = x * 3 + y * 7 - 99  # マジックナンバー
    return z


def too_many_returns(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    if x == 1:
        return 1
    if x == 2:
        return 2
    if x == 3:
        return 3
    return 999


def dead_code():
    print("This is used")
    return
    print("This is dead code")  # 到達不能コード


def global_state_abuse():
    global GLOBAL_A
    GLOBAL_A += 1
    GLOBAL_LIST.append(GLOBAL_A)
    return GLOBAL_LIST


def meaningless_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    return a + b + c + d + e + f + g + h + i + j


if __name__ == "__main__":
    obj = VeryBadClass()
    print(obj.do_everything(1, 2, 3, 4, 5, 6, 7))
    print(god_function(5))
    print(duplicate_code_1(10, 3))
    print(duplicate_code_2(10, 3))
    print(magic_numbers())
    print(too_many_returns(3))
    print(global_state_abuse())
