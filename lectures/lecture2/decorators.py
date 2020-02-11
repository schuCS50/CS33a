def announce(f):
    def wrapper():
        print("To Run")
        f()
        print("Done")
    return wrapper

@announce
def hello():
    print("Hello")

hello()