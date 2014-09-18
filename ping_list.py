#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sys
import re

#ip_prefix = "10.4.6."
logger_path = "logger.txt"

def os_ping(ip_prefix, lower_hostid, upper_hostid):
    if os.path.exists(logger_path):
        os.remove(logger_path)

    st = int(time.time())

    for i in range(int(lower_hostid), int(upper_hostid)):
        ip = ip_prefix + str(i)
        #TODO: ping cost too much time, should be optimized
        res = os.system("ping -c 10 -W 1 "+ip+ " |tail -3 >> " + logger_path)
#    if res:
#            print ip + " ping failed"
    ft = int(time.time())
    print "time:"+str(ft - st)+"s"

def parse_logger():
    if not os.path.exists(logger_path):
        print "No ping logger exists, something must be wrong!"
        return False        
    success = lost = fail = 0
    #ip regular expression
    f = open(logger_path)
    ip_pattern = '([1-9]|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){3}'
    num_pattern = '\d{1,3}\.\d%'
    percent = ''
    while True:
        line = f.readline()
        if not line:
            break
        m = re.search(ip_pattern, line)
        if m:
            line = f.readline()
            percent = re.search(num_pattern, line)
            if percent:
                if percent.group(0) == '0.0%':
                    print m.group(0) + ": OK"
                elif percent.group(0) != '100.0%':
                    print m.group(0) + ": " + percent.group(0) + " LOSS"
                elif percent.group(0) == '100.0%':
                    print m.group(0) + ": FAILED"
    f.close()

def ping_list(ip_prefix, lower_hostid, upper_hostid):
    os_ping(ip_prefix, lower_hostid, upper_hostid)
    parse_logger()

def check_param_valid(ip_prefix, lower_hostid, upper_hostid):
    if not lower_hostid.isdigit():
        print "The lower hostid is not valid\n"
        return False
    if not upper_hostid.isdigit():
        print "The upper hostid is not valid\n"
        return False
    if int(lower_hostid) >= int(upper_hostid):
        print "The upper hostid must be bigger than lower hostid\n"
        return False
    #the ip net-id format:
    # xxx.xxx.xxx.
    pattern = '([1-9]|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])(\\.(\\d|[1-9]\\d|1\\d{2}|2[0-4]\\d|25[0-5])){2}\.'
    m = re.search(pattern, ip_prefix)
    if not m or m.group(0) != ip_prefix:#short expression
        print "The ip prefix is invalid\n"
        return False
    return True

def help():
    print "-----------------------------------------------"
    print "How to use this script:"
    print "python ping_list.py ip_prefix lower_hostid upper_hostid"
    print "For example:"
    print "python ping_list.py 10.4.6. 1 10"
    print "-----------------------------------------------\n"

if __name__ == '__main__':
    #sys.argv[1] ---> ip_prefix
    #sys.argv[2] ---> lower_hostid
    #sys.argv[3] ---> upper_hostid
    if check_param_valid(sys.argv[1], sys.argv[2], sys.argv[3]):
        ping_list(sys.argv[1], sys.argv[2], sys.argv[3]) 
    else:
        help()
        quit()
 #  print "script_name:", sys.argv[0]
 #  for i in range(1, len(sys.argv)):
 #  	   print "parameter:", i, sys.argv[i]
