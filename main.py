data = []

# Code tokens
def tokenizer(code):
    code = code.splitlines()
    tokens = []
    tk = ""
    chars = ["(", ")", "=", "+", "-", "*", "/", "%"]
    string = False
    backslash = False

    for line in code:
        for ch in line:
            if backslash:
                if ch == 'n':
                    tk += "\n"
                elif ch == '"':
                    tk += '"'
                elif ch == "'":
                    tk += "'"
                elif ch == "\\":
                    tk += "\\"

                backslash = False
                continue

            if ch == '\\':
                backslash = True
                continue

            if ch == '"':
                string = not(string)
                if tk != "":
                    tokens.append(tk)
                tk = ""
                tokens.append(ch)
                continue

            if ch == " " and not(string):
                if tk != "":
                    tokens.append(tk)
                tk = ""
                continue

            if ch in chars:
                if tk != "":
                    tokens.append(tk)
                tokens.append(ch)
                tk = ""
                continue

            tk += ch
        
        if tk != "":
            tokens.append(tk)
        tokens.append("\n")
        tk = ""

    return tokens

# Code execution
def run(tokens):
    i = 0
    ifBraces = 0

    while i < len(tokens):
        if i + 1 < len(tokens):

            # Comments
            if tokens[i] == '/':
                if tokens[i+1] == '/':
                    while tokens[i] != "\n":
                        i += 1
                elif tokens[i+1] == '*':
                    while not(tokens[i] == '*' and tokens[i+1] == '/'):
                        i += 1
                    i += 2

            # Other
            if tokens[i] == 'print':
                output = ""

                if tokens[i+2] == '"':
                    output = tokens[i+3]
                    i += 2
                elif tokens[i+2][0].isalpha():
                    for v in data:
                        if tokens[i+2] == v[0]:
                            output = v[1]
                else:
                    output = tokens[i+3]

                print(output)

                i += 3
            elif tokens[i] == 'var':
                if tokens[i+3] == '"':
                    data.append((tokens[i+1], tokens[i+4]))
                    i += 2
                else:
                    data.append((tokens[i+1], tokens[i+3]))
                i += 3
            elif tokens[i] == 'if':
                truth = 'false'

                if tokens[i+2] != 'true' and tokens[i+2] != 'false':
                    for v in data:
                        if tokens[i+2] == v[0]:
                            truth = v[1]
                else:
                    truth = tokens[i+2]

                if truth == 'false':
                    while not(tokens[i] == '}' and ifBraces == 0):
                        if tokens[i] == '{':
                            ifBraces += 1
                        if tokens[i] == '}':
                            ifBraces -= 1
                            if ifBraces == 0:
                                break
                        
                        i += 1
                else:
                    i += 4

            # Useless tokens
            elif tokens[i] == '}' or tokens[i] == "\n":
                pass
            else:
                print(f"???: {tokens[i]}")

        
        i += 1

if __name__ == "__main__":
    with open("main.ds", "r") as f:
        c = f.read()

    tokens = tokenizer(c)

    run(tokens)

    # print(tokens)