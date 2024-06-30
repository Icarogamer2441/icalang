import compiler
import sys
import os
import subprocess

functions = {}
stack = []
running_while = [False]
defines = {}
memory = []

def find_icarolibs_dir(start_path):
    current_path = start_path
    while True:
        for root, dirs, files in os.walk(current_path):
            if 'icarolibs' in dirs:
                return os.path.join(root, 'icarolibs')
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            return None
        current_path = parent_path

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
    in_value = [False]
    defname = [""]
    in_def = [False]
    in_add = [False]
    in_sub = [False]
    in_def1 = [False]
    in_def2 = [False]
    def1 = [""]
    def2 = [""]

    while tokenpos <= len(tokens):
        token = tokens[tokenpos - 1]
        tokenpos += 1

        if not in_str[0] and not in_func[0] and not in_if[0] and not in_comment[0] and not in_while[0] and not in_import[0] and not in_def[0] and not in_add[0] and not in_sub[0]:
            if token.startswith("\""):
                finalstr = []
                if token.endswith("\""):
                    finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
                    string = list("".join(" ".join(finalstr)[::-1]))
                    compiler.pushstr("".join("".join(string)[::-1]))
                    stack.append(0)
                    for char in string:
                        asciichar = ord(char)
                        stack.append(asciichar)
                else:
                    in_str[0] = True
                    finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
            elif token.isdigit() or token.startswith("-") and "".join(token[1:]).isdigit():
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
            elif token == "fun":
                in_func[0] = True
                endnum += 1
            elif token == "==":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                compiler.pop()
                if item1 == item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "!=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                compiler.pop()
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
                string1 = []
                string2 = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string1.append(chr(letter))
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string2.append(chr(letter))
                string1 = "".join(string1)
                string2 = "".join(string2)
                if string1 == string2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "!==":
                string1 = []
                string2 = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string1.append(chr(letter))
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string2.append(chr(letter))
                string1 = "".join(string1)
                string2 = "".join(string2)
                if string1 != string2:
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
                stack.append(num1 - num2)
                compiler.substk()
            elif token == "stk":
                compiler.msg("Stack:\\n")
                for item in stack:
                    compiler.msg(str(item) if isinstance(item, int) else item)
                    compiler.msg("\\n")
            elif token == ">=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                compiler.pop()
                if item1 >= item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "<=":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                compiler.pop()
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
                compiler.pop()
                if item1 > item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "<":
                item1 = stack[len(stack) - 2]
                item2 = stack.pop()
                compiler.pop()
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
            elif token == "argv0":
                if len(sys.argv) >= 2:
                    compiler.pushstr(join(sys.argv[1][::-1]))
                    for char in reversed(sys.argv[1]):
                        stack.append(ord(char))
                else:
                    print("Error: can't get pos argv 1 (filename)")
                    sys.exit(1)
            elif token == "argv1":
                if len(sys.argv) >= 3:
                    compiler.pushstr("".join(sys.argv[2][::-1]))
                    for char in reversed(sys.argv[2]):
                        stack.append(ord(char))
                else:
                    print("Error: can't get pos argv 2 (arg1)")
                    sys.exit(1)
            elif token == "argv2":
                if len(sys.argv) >= 4:
                    compiler.pushstr("".join(sys.argv[3][::-1]))
                    for char in reversed(sys.argv[3]):
                        stack.append(ord(char))
                else:
                    print("Error: can't get pos argv 3 (arg2)")
                    sys.exit(1)
            elif token == "argv3":
                if len(sys.argv) >= 5:
                    compiler.pushstr("".join(sys.argv[4][::-1]))
                    for char in reversed(sys.argv[4]):
                        stack.append(ord(char))
                else:
                    print("Error: can't get pos argv 4 (arg3)")
                    sys.exit(1)
            elif token == "import":
                in_import[0] = True
            elif token == "def":
                in_def[0] = True
            elif token in defines.keys():
                if isinstance(defines[token], str):
                    stack.append(0)
                    compiler.pushstr(defines[token])
                    for char in list("".join(defines[token][::-1])):
                        asciinum = ord(char)
                        stack.append(asciinum)
                else:
                    stack.append(defines[token])
                    compiler.push(defines[token])
            elif token == "add":
                in_add[0] = True
                in_def1[0] = True
            elif token == "sub":
                in_sub[0] = True
                in_def1[0] = True
            elif token == "exit1":
                string = []
                while True:
                    item = stack.pop()
                    compiler.pop()
                    if item == 0:
                        break
                    else:
                        string.append(chr(item))
                string = "".join(string)
                print(string)
                sys.exit(1)
            elif token == "prtinput":
                string = []
                while True:
                    item = stack.pop()
                    compiler.pop()
                    if item == 0:
                        break
                    elif token == 32:
                        pass
                    else:
                        string.append(chr(item))
                string = "".join(string)
                compiler.prtinp(string)
            elif token == "split":
                string = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string.append(chr(letter))
                string = "".join("".join(string)[::-1]).split()
                for word in string:
                    stack.append(0)
                    compiler.pushstr(word)
                    for char in list(word):
                        stack.append(ord(char))
            elif token == "and":
                item1 = stack.pop()
                item2 = stack.pop()
                compiler.pop()
                compiler.pop()
                if item1 and item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "or":
                item1 = stack.pop()
                item2 = stack.pop()
                compiler.pop()
                compiler.pop()
                if item1 or item2:
                    stack.append(1)
                    compiler.push(1)
                else:
                    stack.append(0)
                    compiler.push(0)
            elif token == "take":
                item = stack.pop()
                compiler.pop()
                memory.append(item)
            elif token == "drop":
                item = memory.pop()
                stack.append(item)
                compiler.push(item)
            elif token == "swap":
                item1 = stack.pop()
                item2 = stack.pop()
                compiler.pop()
                compiler.pop()
                stack.append(item2)
                stack.append(item1)
                compiler.push(item2)
                compiler.push(item1)
            elif token == "reversed":
                string = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        break
                    else:
                        string.append(chr(letter))
                string = "".join("".join(string))
                compiler.pushstr(string)
                stack.append(0)
                for char in list(string):
                    asciinum = ord(char)
                    stack.append(asciinum)
            elif token == "mem":
                compiler.msg("Memory:\\n")
                for item in memory:
                    compiler.msg(f"{item}\\n")
            elif token == "dupstr":
                string = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    if letter == 0:
                        string.append(chr(0))
                        break
                    else:
                        string.append(chr(letter))
                string = "".join("".join(string)[::-1])
                compiler.pushstr(string)
                compiler.pushstr(string)
                for char in list(string):
                    stack.append(ord(char))
                for char in list(string):
                    stack.append(ord(char))
            elif token == "<<":
                item2 = stack.pop()
                item1 = stack.pop()
                compiler.pop()
                compiler.pop()
                compiler.push(item1 << item2)
                stack.append(item1 << item2)
            elif token == ">>":
                item2 = stack.pop()
                item1 = stack.pop()
                compiler.pop()
                compiler.pop()
                compiler.push(item1 >> item2)
                stack.append(item1 >> item2)
            elif token == "bor":
                item2 = stack.pop()
                item1 = stack.pop()
                compiler.pop()
                compiler.pop()
                compiler.push(item1 | item2)
                stack.append(item1 | item2)
            elif token == "band":
                item2 = stack.pop()
                item1 = stack.pop()
                compiler.pop()
                compiler.pop()
                compiler.push(item1 & item2)
                stack.append(item1 & item2)
            elif token == "readfile":
                filename = []
                while True:
                    letter = stack.pop()
                    compiler.pop()
                    
                    if letter == 0:
                        break
                    else:
                        filename.append(chr(letter))
                filename = "".join(filename)
                with open(filename, "r") as fi:
                    compiler.pushstr("".join(fi.read()[::-1]))
                
                with open(filename, "r") as fi:
                    stack.append(0)
                    for char in fi.read()[::-1]:
                        stack.append(ord(char))
            else:
                print(f"Error: Unknown keyword: '{token}'")
                sys.exit(1)
        elif in_str[0]:
            if token.endswith("\""):
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
                in_str[0] = False
                string = list("".join(" ".join(finalstr)[::-1]))
                compiler.pushstr("".join("".join(string)[::-1]))
                stack.append(0)
                for char in string:
                    asciichar = ord(char)
                    stack.append(asciichar)
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
                elif token == "fun" or token == "while" or token == "def":
                    functions[funcname[0]].append(token)
                    endnum += 1
                else:
                    functions[funcname[0]].append(token)
        elif in_if[0]:
            if token == "if":
                pass
            else:
                item = stack.pop()
                compiler.pop()
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
                elif token == "fun" or token == "while" or token == "def":
                    endnum += 1
                    while_code.append(token)
                else:
                    while_code.append(token)
        elif in_import[0]:
            if token == "import":
                pass
            else:
                if token.endswith(".icaro"):
                    start_directory = os.getcwd()
                    if token.startswith("./"):
                        with open(token, "r") as fi:
                            compile(fi.read())
                        in_import[0] = False
                    else:
                        result = find_icarolibs_dir(start_directory)
                        with open(f"{result}/{token}", "r") as fi:
                            compile(fi.read())
                        in_import[0] = False
                else:
                    print("Error: use .icaro file extension in import")
                    sys.exit(1)
        elif in_def[0]:
            if token == "end":
                in_value[0] = False
                in_def[0] = False
            if not in_value[0]:
                if token == "def":
                    pass
                elif token == "end":
                    pass
                else:
                    defname[0] = token
                    in_value[0] = True
            elif in_value[0]:
                if token == defname[0]:
                    pass
                elif token.isdigit():
                    defines[defname[0]] = int(token)
                    compiler.createintvar(defname[0], int(token))
                    in_value[0] = False
                elif token == "strstack":
                    string = []
                    while True:
                        letter = stack.pop()
                        compiler.pop()
                        if letter == 0:
                            break
                        else:
                            string.append(chr(letter))
                    string = "".join(string)
                    compiler.createstrvar(defname[0], "".join(string).replace("\n", ""))
                    defines[defname[0]] = "".join(string)
                    in_value[0] = False
                elif token == "input":
                    compiler.strinp(defname[0])
                    in_value[0] = False
        elif in_add[0]:
            if token == "stop":
                in_def1[0] = False
                in_def2[0] = False
                in_add[0] = False
                defines[def1[0]] += defines.get(def2[0])
                compiler.sumvar(def1[0], def2[0])
            if in_def1[0]:
                if token == "add":
                    pass
                else:
                    def1[0] = token
                    in_def1[0] = False
                    in_def2[0] = True
            elif in_def2[0]:
                if token == def1[0]:
                    pass
                else:
                    def2[0] = token
                    in_def2[0] = False
        elif in_sub[0]:
            if token == "stop":
                in_def1[0] = False
                in_def2[0] = False
                in_sub[0] = False
                defines[def1[0]] -= defines.get(def2[0])
                compiler.subvar(def1[0], def2[0])
            if in_def1[0]:
                if token == "sub":
                    pass
                else:
                    def1[0] = token
                    in_def1[0] = False
                    in_def2[0] = True
            elif in_def2[0]:
                if token == def1[0]:
                    pass
                else:
                    def2[0] = token
                    in_def2[0] = False

if __name__ == "__main__":
    version = "1.9"
    if len(sys.argv) == 1:
        print(f"Icaro language version: {version}")
        print(f"Usage: {sys.argv[0]} [arg] [cmd]")
        print(f"args:")
        print("  <file>          compile your file.")
        print("  -p              compile your project. you need ./src/main.icaro and ./build/ directory.")
        print("  -r <file>       compile and run your file")
        print("commands:")
        print("  --dont-rm-asm   don't delete your assembly output file")
    else:
        if sys.argv[1].endswith(".icaro"):
            outputname = sys.argv[1].replace(".icaro", "")
            with open(sys.argv[1], "r") as f:
                compiler.start(outputname)
                compile(f.read())
                compiler.end()
                if len(sys.argv) > 2:
                    if sys.argv[2] == "--dont-rm-asm":
                        pass
                    else:
                        print("Error: You can only use: --dont-rm-asm.")
                        sys.exit(1)
                else:
                    print(f"EXEC: rm -rf {outputname}.asm")
                    subprocess.run(f"rm -rf {outputname}.asm", shell=True)
        elif sys.argv[1] == "-p":
            outputname = "build/output"
            with open("src/main.icaro", "r") as f:
                compiler.start(outputname)
                compile(f.read())
                compiler.end()
                if len(sys.argv) > 2:
                    if sys.argv[2] == "--dont-rm-asm":
                        pass
                    else:
                        print("Error: You can only use: --dont-rm-asm.")
                        sys.exit(1)
                else:
                    print(f"EXEC: rm -rf {outputname}.asm")
                    subprocess.run(f"rm -rf {outputname}.asm", shell=True)
        elif sys.argv[1] == "-r":
            if len(sys.argv) > 2:
                if sys.argv[2].endswith(".icaro"):
                    outputname = sys.argv[2].replace(".icaro", "")
                    with open(sys.argv[2], "r") as f:
                        compiler.start(outputname)
                        compile(f.read())
                        compiler.end()
                    if len(sys.argv) > 3:
                        if sys.argv[3] == "--dont-rm-asm":
                            pass
                        else:
                            print("Error: You can only use: --dont-rm-asm.")
                            sys.exit(1)
                    else:
                        print(f"EXEC: rm -rf {outputname}.asm")
                        subprocess.run(f"rm -rf {outputname}.asm", shell=True)
                    print("INFO: running your compiled file")
                    print(f"EXEC: ./{outputname}")
                    subprocess.run(f"./{outputname}", shell=True)
                else:
                    print("Error: where's the file path?")
                    sys.exit(1)
        else:
            print("Error: use a valid argument! (file with extension .icaro or 'proj' as an argument).")
