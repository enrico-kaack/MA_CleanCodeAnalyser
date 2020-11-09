
def isSmaller(a, b):
    if a == 0:
        return None
    return a < b


def my_func():
    a = 1
    b = 2

    if a < b:
        print("smaller")

    if isSmaller(a, b):
        print("smaller")

if __name__ == "__main__":
    my_func()