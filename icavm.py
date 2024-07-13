import sys

class Icavm:
    def __init__(self):
        self.regs_v1 = {"ra": 0, "rb": 0, "rc": 0, "a1": 0, "a2": 0, "a3": 0, "a4": 0, "stk": [], "top": ""}
        self.regs_v2 = {"r1": 0, "r2": 0, "ta": 0, "tb": 0, "t1": 0, "t2": 0, "t3": 0, "t4": 0, "t5": 0, "sis": [], "tp": ""}
        self.datas = {}
        self.fcontent = ""
        self.compare = []

    def push1(self, value):
        if isinstance(value, str):
            if value in self.regs_v1.keys():
                self.regs_v1["stk"].append(self.regs_v1[value])
            elif value in self.datas.keys():
                self.regs_v1["stk"].append(self.datas[value])
            else:
                print(f"Error: unknown register: {value}")
        else:
            self.regs_v1["stk"].append(value)
        self.regs_v1["top"] = self.regs_v1["stk"][-1]

    def pop1(self, reg):
        if reg in self.regs_v1.keys():
            self.regs_v1[reg] = self.regs_v1["stk"].pop()
        elif reg in self.datas:
            self.datas[reg] = self.regs_v1["stk"].pop()
        else:
            print(f"Error: unknown register: {reg}")
            sys.exit(1)
        if self.regs_v1["stk"]:
            self.regs_v1["top"] = self.regs_v1["stk"][-1]
        else:
            self.regs_v1["top"] = 0

    def push2(self, value):
        if isinstance(value, str):
            if value in self.regs_v2.keys():
                self.regs_v2["sis"].append(self.regs_v2[value])
            if value in self.datas.keys():
                self.regs_v2["sis"].append(self.datas[value])
            else:
                print(f"Error: unknown register: {value}")
        else:
            self.regs_v2["sis"].append(value)
        self.regs_v2["tp"] = self.regs_v2["sis"][-1]

    def pop2(self, reg):
        if reg in self.regs_v2.keys():
            self.regs_v2[reg] = self.regs_v2["sis"].pop()
        if reg in self.datas.keys():
            self.datas[reg] = self.regs_v2["sis"].pop()
        else:
            print(f"Error: unknown register: {reg}")
            sys.exit(1)
        if self.regs_v2["sis"]:
            self.regs_v2["tp"] = self.regs_v2["sis"][-1]
        else:
            self.regs_v2["tp"] = 0

    def mov1(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v1.keys():
                if value in self.regs_v1.keys():
                    self.regs_v1[reg] = self.regs_v1[value]
                elif value in self.datas.keys():
                    self.regs_v1[reg] = self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v1.keys():
                    self.datas[reg] = self.regs_v1[value]
                elif value in self.datas.keys():
                    self.datas[reg] = self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v1.keys():
                self.regs_v1[reg] = value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def mov2(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v2.keys():
                if value in self.regs_v2.keys():
                    self.regs_v2[reg] = self.regs_v2[value]
                elif value in self.datas.keys():
                    self.regs_v2[reg] = self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v2.keys():
                    self.datas[reg] = self.regs_v2[value]
                elif value in self.datas.keys():
                    self.datas[reg] = self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v2.keys():
                self.regs_v2[reg] = value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def syscall1(self):
        if self.regs_v1["rc"] == 3:
            if self.regs_v1["rb"] == 1:
                print(self.regs_v1["ra"], end="")
        elif self.regs_v1["rc"] == 2:
            sys.exit(self.regs_v1["rb"])
        elif self.regs_v1["rc"] == 1:
            if self.regs_v1["rb"] == 1:
                with open(self.regs_v1["ra"], "r") as f:
                    self.fcontent = f.read()
            elif self.regs_v1["rb"] == 2:
                with open(self.regs_v1["ra"], "w") as f:
                    f.write(self.regs_v1["a1"])
            elif self.regs_v1["rb"] == 3:
                with open(self.regs_v1["ra"], "a") as f:
                    f.write(self.regs_v1["a1"])

    def syscall2(self):
        if self.regs_v2["r1"] == 2:
            if self.regs_v2["r2"] == 1:
                print(self.regs_v2["ta"], end="")
        elif self.regs_v2["r1"] == 1:
            sys.exit(self.regs_v2["r2"])
        elif self.regs_v2["r1"] == 3:
            if self.regs_v2["r2"] == 3:
                with open(self.regs_v2["ta"], "r") as f:
                    self.fcontent = f.read()
            elif self.regs_v2["r2"] == 2:
                with open(self.regs_v2["ta"], "w") as f:
                    f.write(self.regs_v2["tb"])
            elif self.regs_v2["r2"] == 1:
                with open(self.regs_v2["ta"], "a") as f:
                    f.write(self.regs_v2["tb"])

    def addata(self, name, value):
        self.datas[name] = value

    def add1(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v1.keys():
                if value in self.regs_v1.keys():
                    self.regs_v1[reg] += self.regs_v1[value]
                elif value in self.datas.keys():
                    self.regs_v1[reg] += self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v1.keys():
                    self.datas[reg] += self.regs_v1[value]
                elif value in self.datas.keys():
                    self.datas[reg] += self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v1.keys():
                self.regs_v1[reg] += value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def add2(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v2.keys():
                if value in self.regs_v2.keys():
                    self.regs_v2[reg] += self.regs_v2[value]
                elif value in self.datas.keys():
                    self.regs_v2[reg] += self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v2.keys():
                    self.datas[reg] += self.regs_v2[value]
                elif value in self.datas.keys():
                    self.datas[reg] += self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v2.keys():
                self.regs_v2[reg] += value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def sub1(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v1.keys():
                if value in self.regs_v1.keys():
                    self.regs_v1[reg] -= self.regs_v1[value]
                elif value in self.datas.keys():
                    self.regs_v1[reg] -= self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v1.keys():
                    self.datas[reg] -= self.regs_v1[value]
                elif value in self.datas.keys():
                    self.datas[reg] -= self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v1.keys():
                self.regs_v1[reg] -= value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def sub2(self, reg, value):
        if isinstance(value, str):
            if reg in self.regs_v2.keys():
                if value in self.regs_v2.keys():
                    self.regs_v2[reg] -= self.regs_v2[value]
                elif value in self.datas.keys():
                    self.regs_v2[reg] -= self.datas[value]
                else:
                    print(f"Error: unknown register: {reg}")
                    sys.exit(1)
            elif reg in self.datas.keys():
                if value in self.regs_v2.keys():
                    self.datas[reg] -= self.regs_v2[value]
                elif value in self.datas.keys():
                    self.datas[reg] -= self.datas[value]
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)
        else:
            if reg in self.regs_v2.keys():
                self.regs_v2[reg] -= value
            else:
                print(f"Error: unknown register: {reg}")
                sys.exit(1)

    def compare1(self, reg1, reg2):
        if reg1 in self.regs_v1.keys():
            if reg2 in self.regs_v1.keys():
                self.compare = [self.regs_v1[reg1], self.regs_v1[reg2]]
            else:
                print("Error: you can only use registers!")
                sys.exit(1)
        else:
            print("Error: you can only use registers!")
            sys.exit(1)

    def compare2(self, reg1, reg2):
        if reg1 in self.regs_v2.keys():
            if reg2 in self.regs_v2.keys():
                self.compare = [self.regs_v1[reg1], self.regs_v1[reg2]]
            else:
                print("Error: you can only use registers!")
                sys.exit(1)
        else:
            print("Error: you can only use registers!")
            sys.exit(1)

    def equal(self):
        if self.compare[0] == self.compare[1]:
            return True
        else:
            return False

    def nequal(self):
        if self.compare[0] != self.compare[1]:
            return True
        else:
            return False

    def greater(self):
        if self.compare[0] > self.compare[1]:
            return True
        else:
            return False

    def less(self):
        if self.compare[0] < self.compare[1]:
            return True
        else:
            return False

    def grequal(self):
        if self.compare[0] >= self.compare[1]:
            return True
        else:
            return False

    def lessequal(self):
        if self.compare[0] <= self.compare[1]:
            return True
        else:
            return False

def normalcode1(code, virm, labels):
        tokens = code.split()
        tokenpos = 0
        vm = virm
        in_comment = [False]

        while tokenpos < len(tokens):
            token = tokens[tokenpos]
            tokenpos += 1
            
            if not in_comment[0]:
                if token == "push":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.push2(int(token))
                    else:
                        vm.push1(token)
                elif token == "pop":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        print("Error: can't push int values")
                        sys.exit(1)
                    else:
                        vm.pop1(token)
                elif token == "call":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token in labels.keys():
                        normalcode1(" ".join(labels[token]), vm, labels)
                    else:
                        print(f"Error: unknown label: {token}")
                elif token == "jump":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token in labels.keys():
                        normalcode1(" ".join(labels[token]), vm, labels)
                        break
                    else:
                        print(f"Error: unknown label: {token}")
                elif token == "move":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.mov1(reg, int(token))
                    else:
                        vm.mov1(reg, token)
                elif token == "sys":
                    vm.syscall1()
                elif token == "add":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.add1(reg, int(token))
                    else:
                        vm.add1(reg, token)
                elif token == "sub":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.sub1(reg, int(token))
                    else:
                        vm.sub1(reg, token)
                elif token == "/*":
                    in_comment[0] = True
                elif token == "comp":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    vm.compare1(reg, token)
                elif token == "je":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.equal()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jne":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.nequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jl":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.less()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jg":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.greater()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jge":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.grequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jle":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.lessequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode2(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
            elif in_comment[0]:
                if token == "*/":
                    in_comment[0] = False
                else:
                    pass

def normalcode2(code, virm, labels):
        tokens = code.split()
        tokenpos = 0
        vm = virm
        in_comment = [False]

        while tokenpos < len(tokens):
            token = tokens[tokenpos]
            tokenpos += 1
            
            if not in_comment[0]:
                if token == "push":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.push2(int(token))
                    else:
                        vm.push2(token)
                elif token == "pop":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        print("Error: can't push int values")
                        sys.exit(1)
                    else:
                        vm.pop2(token)
                elif token == "call":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token in labels.keys():
                        normalcode2(" ".join(labels[token]), vm, labels)
                    else:
                        print(f"Error: unknown label: {token}")
                elif token == "jump":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token in labels.keys():
                        normalcode2(" ".join(labels[token]), vm, labels)
                        break
                    else:
                        print(f"Error: unknown label: {token}")
                elif token == "move":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.mov2(reg, int(token))
                    else:
                        vm.mov2(reg, token)
                elif token == "sys":
                    vm.syscall2()
                elif token == "add":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.add2(reg, int(token))
                    else:
                        vm.add2(reg, token)
                elif token == "sub":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    if token.isdigit() or (token.startswith("-") and "".join(token[1:]).isdigit()):
                        vm.sub2(reg, int(token))
                    else:
                        vm.sub2(reg, token)
                elif token == "/*":
                    in_comment[0] = True
                elif token == "comp":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    reg = token
                    token = tokens[tokenpos]
                    tokenpos += 1
                    vm.compare2(reg, token)
                elif token == "je":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.equal()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jne":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.nequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jl":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.less()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jg":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.greater()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jge":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.grequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
                elif token == "jle":
                    token = tokens[tokenpos]
                    tokenpos += 1
                    istrue = vm.lessequal()
                    if istrue:
                        if token in labels.keys():
                            normalcode1(" ".join(labels[token]), vm, labels)
                            break
                        else:
                            print(f"Error: unknown label: {token}")
            elif in_comment[0]:
                if token == "*/":
                    in_comment[0] = False
                else:
                    pass
        
def assembler(code, mode):
    vm = Icavm()
    tokens = code.split()
    tokenpos = 0
    labels = {}
    in_label = [False]
    labelname = [""]

    while tokenpos < len(tokens):
        token = tokens[tokenpos]
        tokenpos += 1

        if not in_label[0]:
            if token.endswith(":"):
                labelname[0] = token.split(":")[0].strip()
                labels[labelname[0]] = []
                in_label[0] = True
            elif token == ".data":
                finalvalue = []
                token = tokens[tokenpos]
                tokenpos += 1
                name = token
                while token != "end" and tokenpos < len(token):
                    token = tokens[tokenpos]
                    tokenpos += 1

                    if token == "end":
                        break
                    else:
                        finalvalue.append(token.replace("\\n", "\n").replace("\\s", " "))
                finalvalue = " ".join(finalvalue)
                if finalvalue.isdigit() or (finalvalue.startswith("-") and "".join(finalvalue[1:].isdigit)):
                    vm.addata(name, int(finalvalue))
                else:
                    vm.addata(name, finalvalue)
        elif in_label[0]:
            if token == "end":
                in_label[0] = False
            else:
                labels[labelname[0]].append(token)
    if mode == "1" or mode == 1:
        try:
            normalcode1(" ".join(labels["main"]), vm, labels)
        except:
            pass
    else:
        try:
            normalcode2(" ".join(labels["main"]), vm, labels)
        except:
            pass
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [mode] [file.icm]")
        print("modes:")
        print("  -m1     mode 1")
        print("  -m2     mode 2")
        print("modes have diferent features and registers")
        sys.exit(1)
    else:
        if sys.argv[1] == "-m1":
            if sys.argv[2].endswith(".icm"):
                with open(sys.argv[2], "r") as f:
                    assembler(f.read(), 1)
        elif sys.argv[1] == "-m2":
            if sys.argv[2].endswith(".icm"):
                with open(sys.argv[2], "r") as f:
                    assembler(f.read(), 2)
        else:
            print(f"Error: unknown mode: {sys.argv[1]}")
            sys.exit(1)
