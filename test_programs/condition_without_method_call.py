
def isSmaller(a, b):
    return a < b

def my_func():
    a = 1
    b = 2
     
    if a < b:
        print("smaller")
    
    if isSmaller(a, b):
        print("smaller")

    if isSmaller(a,b) and a < b:
        print("smaller")

    if  a < b and isSmaller(a,b) :
        print("smaller")

    if isSmaller(a,b) and isSmaller(b, a):
        print("smaller")

    if not a<b and isSmaller(a,b):
        print("smaller")

    if not isSmaller(a,b) and a<b:
        print("smaller")

    if not isSmaller(a,b):
        print("smaller")

    if not isSmaller(a,b) and isSmaller(b,a):
        print("smaller")

if __name__ == "__main__":
    my_func()