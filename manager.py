import os
import sys
import argparse
import time

from queue import Queue
from multiprocessing.managers import BaseManager


BROKER = None
def get_broker_handler():
    global BROKER
    if not BROKER:
        BROKER = Queue()
    return BROKER



class QueueManager(BaseManager):
    pass


QueueManager.register('get_queue', callable=lambda:get_broker_handler())

def _get_manager(broker_host, broker_port):
    return QueueManager(address=(broker_host, broker_port), authkey=b'default')

def get_server():
    broker_host = "127.0.0.1"
    broker_port = 50000
    m = _get_manager(broker_host, broker_port)
    server = m.get_server()
    return server

def get_queue():
    import os
    broker_host = "127.0.0.1"
    broker_port = 50000
    m = _get_manager(broker_host, broker_port)
    m.connect()
    q = m.get_queue()
    return q


def func1(x):
    return x


def func2(x):
    x += 1
    return x


def producer():
    queue = get_queue()
    while not queue.empty():
        queue.get(block=False)

    x = 0
    while True:

        results = func1(x)
        print("put results to queue: {}".format(results))
        queue.put(results)
        time.sleep(1)
        x += 1


def consumer():
    queue = get_queue()
    while True:
        results = queue.get(block=True)
        print("get results from queue: {}".format(results))
        updated_results = func2(results)
        print("evaluate results: {}".format(updated_results))

        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", dest="producer",
                        action="store_true",
                        required=False,
                        default=False)
    parser.add_argument("--consumer", dest="consumer",
                        action="store_true",
                        required=False,
                        default=False)
    parser.add_argument("--server", dest="server",
                        action="store_true",
                        required=False,
                        default=False)
    argv = parser.parse_args(sys.argv[1:])
    if argv.server:
        server = get_server()
        server.serve_forever()
    if argv.producer:
        producer()
    if argv.consumer:
        consumer()
