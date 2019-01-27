import multiprocessing

x = 0

def incr(name):
    global x
    while True:
        x = x + 1
        print("{} of x: {}".format(name, x))


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=incr, args=("process-1", ))
    p2 = multiprocessing.Process(target=incr, args=("process-2", ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
