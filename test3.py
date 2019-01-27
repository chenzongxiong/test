### differece between ~thread~ and ~process~
### mainly, thread is much light-weight than process and all threads in the same process sharing data segments
### however, difference processes have different data segments

import threading

x = 0

def incr(name):
    global x
    while True:
        x = x + 1
        print("{} of x: {}".format(name, x))


if __name__ == "__main__":
    thread1 = threading.Thread(target=incr, args=("thread-1",))
    thread2 = threading.Thread(target=incr, args=("thread-2",))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
