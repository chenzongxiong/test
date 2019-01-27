### test1.py: parallell processing, both function f1, f2 are executed

import threading

def f1(name):
    while True:
        print("{} is running".format(name))


def f2(name):
    while True:
        print("{} is running".format(name))


if __name__ == "__main__":
    thread1 = threading.Thread(target=f1, args=("thread-1", ))
    thread2 = threading.Thread(target=f2, args=("thread-2", ))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
