from multiprocessing import Process, Value, Array, Lock

import time
import random

# synchronize via lock
def f1(l, i):
    l.acquire()
    try:
        time.sleep(random.randint(1, 3))
        print('hello world', i)
    finally:
        l.release()
        pass

## exchange value among process
def f2(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]


def f3(l, a, b=0):

    for i in range(len(a)):
        time.sleep(random.randint(1, 2))
        a[i] = a[i] * 2

    # l.acquire()
    try:
        b = 2
    finally:
        l.release()
    # try:
    #     time.sleep(random.randint(2, 3))
    #     for i in range(len(a)):
    #         a[i] = a[i] * 2
    # finally:
    #     # l.release()
    #     pass

def f4(l, a):
    # l.acquire()

    try:
        for i in range(len(a)):
            time.sleep(random.randint(1, 2))
            a[i] = a[i] + 3
    finally:
        # l.release()
        pass


if __name__ == '__main__':
    lock = Lock()

    # for num in range(10):
    #     Process(target=f1, args=(lock, num)).start()

    num = Value('d', 0.0)
    arr = Array('i', range(10))

    # print(num.value)
    # print(arr[:])

    # p2 = Process(target=f2, args=(num, arr))
    # p2.start()
    # p2.join()
    # print(num.value)
    # print(arr[:])

    p1 = Process(target=f3, args=(lock, arr))
    # p3 = Process(target=f3, args=(lock, arr))
    # p4 = Process(target=f3, args=(lock, arr))
    p1.start()
    p2 = Process(target=f4, args=(lock, arr))
    p2.start()

    p2.join()
    p1.join()
    print(arr[:])
    # [3, 5, 7, ...]
