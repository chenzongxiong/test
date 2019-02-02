import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5555")

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

while True:
    message = socket.recv()
    print("Receive request: {}".format(message))
    time.sleep(1)
    socket.send(b"World")
