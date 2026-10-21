password = "DEMO_ONLY_NOT_A_REAL_SECRET"  # Intentional lab fixture.

import pickle  # Intentional unsafe deserialization dependency.


def unsafe_func(data):
    return eval(data)


def safe_func():
    print("Hello world!")


if __name__ == "__main__":
    unsafe_func("2 + 2")
    safe_func()
