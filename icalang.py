import compiler
import sys

functions = {}
stack = []
string_stack = []
running_while = [False]

def compile(code):
    tokens = code.split() or code.split("\t")
    tokenpos = 1
    in_str = [False]
    finalstr = []
    in_func = [False]
    endnum = 0
    in_code = [False]
    funcname = [""]
    in_if = [False]
    in_comment = [False]
    in_while = [False]
    while_code = []
    in_import = [False]

    while tokenpos <= len(tokens):
        token = tokens[tokenpos - 1]
        tokenpos += 1

        if not in_str[0] and not in_func[0] and not in_if[0] and not in_comment[0] and not in_while[0] and not in_import[0]:
            if token.startswith("\""):
                in_str[0] = True
                stack.append(0)
                compiler.push(0)
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
            elif token.isdigit():
                compiler.push(int(token))
                stack.append(int(token))
            elif token == "show":
                stack.pop()
                compiler.printstack()
            elif token == "print":
                asciichar = stack.pop()
                compiler.pop()
                compiler.asciimsg(asciichar)
            elif token == "pop":
                compiler.pop()
                stack.pop()
            elif token == "pops":
                string_stack.pop()
            elif token == "strtostack":
                string = string_stack.pop()
                stack.append(0)
                compiler.push(0)
                for char in list(string):
                    asciichar = ord(char)
                    stack.append(asciichar)
                    compiler.push(asciichar)
            elif token == "fun":
                in_func[0] = True
                endnum += 1
            elif token == "==":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 == item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "!=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 != item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token in functions.keys():
                compile(" ".join(functions[token]))
            elif token == "if":
                in_if[0] = True
            elif token == "===":
                item1 = string_stack[len(string_stack) - 2]
                item2 = string_stack.pop()
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                if item1 == item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "!==":
                item1 = string_stack[len(string_stack) - 2]
                item2 = string_stack.pop()
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                if item1 != item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "/*":
                in_comment[0] = True
            elif token == "stopwhile":
                running_while[0] = False
            elif token == "while":
                in_while[0] = True
                endnum += 1
                running_while[0] = True
                while_code = []
            elif token == "+":
                num2 = stack.pop()
                num1 = stack.pop()
                stack.append(num1 + num2)
                compiler.sumstk()
            elif token == "-":
                num2 = stack.pop()
                num1 = stack.pop()
                stack.append(num1 + num2)
                compiler.substk()
            elif token == "stk":
                compiler.msg("Stack:\\n")
                for item in stack:
                    compiler.msg(str(item) if isinstance(item, int) else item)
                    compiler.msg("\\n")
            elif token == ">=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 >= item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "<=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 <= item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "dup":
                stack.append(stack[-1])
                compiler.push(stack[-1])
            elif token == ">":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 > item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "<":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                if item1 < item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "not":
                item = stack.pop()
                compiler.pop()
                if item >= 1:
                    stack.append(0)
                    compiler.push(0)
                else:
                    stack.append(1)
                    compiler.push(1)
            elif token == "nothing":
                print("", end="")
            elif token == "split":
                item = string_stack.pop()
                splited = item.split()
                for itemm in splited:
                    compiler.push(0)
                    stack.append(0)
                    for char in list(itemm):
                        asciinum = ord(char)
                        stack.append(asciinum)
                        compiler.push(asciinum)
            elif token == "argv0":
                if len(sys.argv) >= 2:
                    string_stack.append("".join(sys.argv[1][::-1]))
                else:
                    print("Error: can't get pos argv 1 (filename)")
                    sys.exit(1)
            elif token == "argv1":
                if len(sys.argv) >= 3:
                    string_stack.append("".join(sys.argv[2][::-1]))
                else:
                    print("Error: can't get pos argv 2 (arg1)")
                    sys.exit(1)
            elif token == "argv2":
                if len(sys.argv) >= 4:
                    string_stack.append("".join(sys.argv[3][::-1]))
                else:
                    print("Error: can't get pos argv 3 (arg2)")
                    sys.exit(1)
            elif token == "argv3":
                if len(sys.argv) >= 5:
                    string_stack.append("".join(sys.argv[4][::-1]))
                else:
                    print("Error: can't get pos argv 4 (arg3)")
                    sys.exit(1)
            elif token == "strstack":
                compiler.msg("String stack:\\n")
                for string in string_stack:
                    compiler.msg(string)
                    compiler.msg("\\n")
            elif token == "import":
                in_import[0] = True
            else:
                print(f"Error: Unknown keyword: '{token}'")
                sys.exit(1)
        elif in_str[0]:
            if token.endswith("\""):
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
                in_str[0] = False
                string = list("".join(" ".join(finalstr)[::-1]))
                string_stack.append("".join(string))
                for char in string:
                    asciichar = ord(char)
                    stack.append(asciichar)
                    compiler.push(asciichar)
            else:
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
        elif in_func[0]:
            if not in_code[0]:
                if token == "fun":
                    pass
                else:
                    funcname[0] = token
                    in_code[0] = True
                    functions[funcname[0]] = []
            elif in_code[0]:
                if token == "end":
                    endnum -= 1
                    if endnum <= 0:
                        endnum = 0
                        in_func[0] = False
                        in_code[0] = False
                    else:
                        functions[funcname[0]].append(token)
                elif token == "fun" or token == "while":
                    functions[funcname[0]].append(token)
                    endnum += 1
                else:
                    functions[funcname[0]].append(token)
        elif in_if[0]:
            if token == "if":
                pass
            else:
                item = stack.pop()
                if item:
                    compile(token)
                else:
                    pass
                in_if[0] = False
        elif in_comment[0]:
            if token == "*\\":
                in_comment[0] = False
            else:
                pass
        elif in_while[0]:
            if not in_code[0]:
                if token == "while":
                    pass
                else:
                    in_code[0] = True
                    while_code.append(token)
            elif in_code[0]:
                if token == "end":
                    endnum -= 1
                    if endnum <= 0:
                        in_code[0] = False
                        in_while[0] = False
                        finalcode = " ".join(while_code)
                        running_while[0] = True
                        while running_while[0]:
                            compile(finalcode)
                    else:
                        while_code.append(token)
                elif token == "fun" or token == "while":
                    endnum += 1
                    while_code.append(token)
                else:
                    while_code.append(token)
        elif in_import[0]:
            if token == "import":
                pass
            else:
                if token.endswith(".icaro"):
                    with open(token, "r") as fi:
                        compile(fi.read())
                    in_import[0] = False
                else:
                    print("Error: use .icaro file extension in import")
                    sys.exit(1)

if __name__ == "__main__":
    version = "1.0"
    if len(sys.argv) == 1:
        print(f"Icaro language version: {version}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".icaro"):
            outputname = sys.argv[1].replace(".icaro", "")
            with open(sys.argv[1], "r") as f:
                compiler.start(outputname)
                compile(f.read())
                compiler.end()
        else:
            print("Error: use .icaro file extension!")
