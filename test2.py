### test2.py: parallell processing, both function f1, f2 are executed

import multiprocessing

def f1(name):
    while True:
        print("{} is running".format(name))

def f2(name):
    while True:
        print("{} is running".format(name))

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=f1, args=("process-1",))
    p2 = multiprocessing.Process(target=f2, args=("process-2",))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
