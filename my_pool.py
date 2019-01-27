### an simpler implementation of process pools in python

import multiprocessing
import random
import time


class ProcessPool(object):
    def __init__(self, pool_size=2):
        self._pool_size = pool_size
        # func, func_args
        self.tasks = []
        self.task_results = {}
        self.pool = []


    def run(self):
        while True:
            try:
                while len(self.pool) == self._pool_size:
                    print("task is full")
                    for i in range(self._pool_size):
                        if not self.pool[i].is_alive():
                            print("process {} is removed".format(i))
                            self.pool.pop(i)
                            break
                task = self.tasks.pop()
                func, func_args = task
                # import ipdb; ipdb.set_trace()

                p = multiprocessing.Process(target=func, args=func_args)
                p.start()
                p.join()
                self.pool.append(p)
            except IndexError:
                # no tasks in the queue
                print()
                exit = True
                for i in range(len(self.pool)):
                    if self.pool[i].is_alive():
                        exit = False
                if exit is True:
                    break
                else:
                    time.sleep(1)

    def put(self, task):
        self.tasks.append(task)

    def map(self, func, func_args_list):
        for func_args in func_args_list:
            self.put((func, func_args))
        self.run()


def func1(name):
    # ts = random.randint(1, 2)
    ts = random.random()
    print("*func-1* {} is going to sleep {}s".format(name, ts))
    time.sleep(ts)


def func2(name):
    ts = random.random()
    print("*func-2* {} is going to sleep {}s".format(name, ts))
    time.sleep(ts)


if __name__ == "__main__":
    size = 50
    pool = ProcessPool(4)
    func_list = [func1, func2]
    tasks = [(func_list[i % 2], ("task-{}".format(i),)) for i in range(size)]
    for task in tasks:
        pool.put(task)

    pool.run()
    print("====================use map====================")
    pool.map(func1, [("mapping-task-{}".format(i),) for i in range(size)])
