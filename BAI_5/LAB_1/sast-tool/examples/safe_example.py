import ast


def parse_literal(text):
    return ast.literal_eval(text)


if __name__ == "__main__":
    print(parse_literal("[1, 2, 3]"))
