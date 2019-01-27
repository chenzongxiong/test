### test0.py: serial process, function f2 nerver be executed
import time

def f1(name):
    while True:
        print("{} is running".format(name))
        time.sleep(1)

def f2(name):
    while True:
        print("{} is running".format(name))
        time.sleep(1)

if __name__ == "__main__":
    f1(name="f1")
    f2(name="f2")
