def dangerous_eval(user_input):
    return eval(user_input)


def read_file(filename):
    with open(filename, "r") as source:
        data = source.read()
    return data


def execute_code(code):
    exec(code)


if __name__ == "__main__":
    dangerous_eval("print('Hello from eval')")
