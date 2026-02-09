# ===== さらにコードスメルを追加 =====

# 1. 巨大クラス（Large Class）
class MonsterClass:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0

    def method1(self): return self.a
    def method2(self): return self.b
    def method3(self): return self.c
    def method4(self): return self.d
    def method5(self): return self.e
    def method6(self): return self.f
    def method7(self): return self.a + self.b
    def method8(self): return self.c + self.d
    def method9(self): return self.e + self.f
    def method10(self): return self.a + self.b + self.c
    def method11(self): return self.d + self.e + self.f
    def method12(self): return self.a * self.b * self.c
    def method13(self): return self.d * self.e * self.f


# 2. Boolean引数アンチパターン
def boolean_argument(flag):
    if flag == True:
        print("Flag is true")
    else:
        print("Flag is false")


# 3. 意味のない条件分岐
def pointless_condition(x):
    if x == x:  # 常にTrue
        return True
    else:
        return False


# 4. 同じロジックのコピペ量産（重複）
def duplicate_code_3(a, b):
    if a > b:
        return a - b
    else:
        return b - a


def duplicate_code_4(a, b):
    if a > b:
        return a - b
    else:
        return b - a


# 5. 深すぎるネスト（if + for）
def insane_nesting(n):
    for i in range(n):
        if i > 0:
            for j in range(n):
                if j > 0:
                    for k in range(n):
                        if k > 0:
                            print(i, j, k)


# 6. 不要なelse（早期returnできる）
def useless_else(x):
    if x > 0:
        return "positive"
    else:
        return "not positive"


# 7. 空の関数（実装なし）
def empty_function():
    pass


# 8. 不要な型変換
def useless_cast(x):
    y = int(x)
    z = int(y)
    return int(z)


# 9. 定数化すべき値の乱用
def more_magic_numbers():
    return (5 * 17) + (99 / 3) - 42 + 1234


# 10. try-exceptの乱用
def exception_abuse():
    try:
        try:
            try:
                x = int("not_a_number")
            except:
                pass
        except:
            pass
    except:
        pass


# 11. 未使用関数（Dead Code）
def never_called_function():
    print("I will never be called")


# 12. 条件分岐の肥大化（if-elif地獄）
def switch_like(value):
    if value == "a":
        return 1
    elif value == "b":
        return 2
    elif value == "c":
        return 3
    elif value == "d":
        return 4
    elif value == "e":
        return 5
    elif value == "f":
        return 6
    elif value == "g":
        return 7
    elif value == "h":
        return 8
    elif value == "i":
        return 9
    else:
        return 0


# 13. グローバル変数さらに悪用
def global_mess():
    global GLOBAL_B
    GLOBAL_B = GLOBAL_B * 2 + 1 - 3 + 7
    return GLOBAL_B


# 14. 意味のないループ
def useless_loop():
    for i in range(1000):
        pass
    return "done"


