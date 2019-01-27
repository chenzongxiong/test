### to see the different performance between multiple thread, multiple process and sequence processing
### if the ~size~ is far too smaller, such as 1 or 10, then multiple threads will be out-performance than
### multiple-process
### if the ~size~ grows bigger, such as 1000 or 10000, then multiple process will be faster than multiple
### thread

import threading
import multiprocessing
import random
import time


size = 100000
cores = 4
my_list = [[] for _ in range(cores)]
TIMES = 10

DEBUG = False


def func(core, size, name='serial'):
    for i in range(size):
        my_list[core].append(random.random())
    if DEBUG:
        print("{} has {} elements in my_list[{}]".format(name, len(my_list[core]), core))


def multithreaded(cores, size):
    threads = []
    for core in range(cores):
        threads.append(threading.Thread(target=func, args=(core, size, "thread-{}".format(core))))

    for i in range(cores):
        threads[i].start()
    for i in range(cores):
        threads[i].join()


def serial(cores, size):
    for core in range(cores):
        func(core, size)


def multiprocessed(cores, size):
    processes = []
    for core in range(cores):
        processes.append(multiprocessing.Process(target=func, args=(core, size, "process-{}".format(core))))
    for i in range(cores):
        processes[i].start()

    for i in range(cores):
        processes[i].join()


def timeit(mode, TIMES=100):
    if mode == "thread":
        costs = []
        for _ in range(TIMES):
            start = time.time()
            multithreaded(cores, size)
            end = time.time()
            costs.append(end-start)
        print("Evaluate threads mode {} times and the average cost is {}s".format(TIMES, sum(costs)/TIMES))
    elif mode == "serial":
        costs = []
        for _ in range(TIMES):
            start = time.time()
            serial(cores, size)
            end = time.time()
            costs.append(end-start)
        print("Evaluate serial mode {} times and the average cost is {}s".format(TIMES, sum(costs)/TIMES))
    elif mode == "process":
        costs = []
        for _ in range(TIMES):
            start = time.time()
            multiprocessed(cores, size)
            end = time.time()
            costs.append(end-start)
        print("Evaluate serial mode {} times and the average cost is {}s".format(TIMES, sum(costs)/TIMES))



if __name__ == "__main__":
    # multithreaded(cores, size)
    # serial(cores, size)
    # multiprocessed(cores, size)

    # timeit("serial")
    timeit("thread")
    timeit("process")
    # global inteperter lock
