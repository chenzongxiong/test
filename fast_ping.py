#! /usr/bin/python

"""
ping a list of ip
"""

"""
It will occure error when ping more than 100 at the same time
And I'll fix this problem in the future
"""
import os
import re
import threading
import time
from config import *

RESULT_PATTERN = re.compile(r'(\d+.\d)% packet loss')

class Ping(threading.Thread):
    def __init__(self, ip_address):
        threading.Thread.__init__(self)
        self.ip_address = ip_address

    def run(self):
        # ping an ip and return the loss of package
        result = os.popen('ping -c 10 %s' % self.ip_address).read()
        match = RESULT_PATTERN.search(result)
        lost_count = match and float(match.group(1))

        # add a lock to avoid chaos displaying
        global lock
        lock.acquire()
        #print match

        if lost_count == 0.0:
            print 'ping %-15s         stabled   ------   %.1f' % (self.ip_address, lost_count)
        elif lost_count == 100.0:
            print 'ping %-15s         timeout   ------   %.1f' % (self.ip_address, lost_count)
        else:
            print 'ping %-15s         unstabled ------   %.1f' % (self.ip_address, lost_count)

        lock.release()

def bulk_ping(ip_prefix, start=0, end=100):
    print 'pinging ip addresses from %s.%d to %s.%d' % (ip_prefix, start, ip_prefix, end)
    for i in range(start, end):
        ping_thread = Ping('%s.%d' %(ip_prefix, i))
        ping_thread.start()

if __name__ == '__main__':
#    start_ip = "10.4.6.54"
#    end_ip = "10.4.6.235"
    global lock
    lock = threading.Lock()
    start_ip_items = start_ip.split('.')
    end_ip_items = end_ip.split('.')
    for first in range(int(start_ip_items[0]), int(end_ip_items[0])+1):
        for second in range(int(start_ip_items[1]), int(end_ip_items[1])+1):
            for third in range(int(start_ip_items[2]), int(end_ip_items[2])+1):
                ip_prefix = str(first)+'.'+str(second)+'.'+str(third)
                start = int(start_ip_items[3])
                end = int(end_ip_items[3])
                bulk_ping(ip_prefix, start, end)
