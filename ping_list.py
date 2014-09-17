# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import time
import sys


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
        if res:
            print ip + " ping failed"
    ft = int(time.time())
    print "time:"+str(ft - st)+"s"

def parse_logger():
    if not os.path.exists(logger_path):
        print "No ping logger exists, something must be wrong!"
        return

    print "Enter the function parse_logger"
    f = open(logger_path)
    while True:
        line = f.readline()
        if not line:
            break
        
        ip = ''
        loss = ''
        if line.find('statistics') != -1:
            i = 4
            while line[i] != 'p':
                ip = ip + line[i]
                i = i + 1

            line = f.readline()
            
            pos = line.find('packet loss')
            if pos != -1:
                pos = pos - 2
                while line[pos] != ',':
                    loss = loss + line[pos]
                    pos = pos - 1
            loss = loss[::-1]
            if loss == ' 0.0%':
                print ip + ":" + loss + ' Pass'
            elif loss != ' 100.0%':
                print ip + ':' + loss + ' Loss'

    f.close()

def ping_list(ip_prefix, lower_hostid, upper_hostid):
    print "In ping_list function\n"
    os_ping(ip_prefix, lower_hostid, upper_hostid)
    parse_logger()
#	 print "Hello world in ping_list function"



def check_param_valid(ip_prefix, lower_hostid, upper_hostid):
    if not lower_hostid.isdigit():
        print "The lower hostid is not valid\n"
        return False
    if not upper_hostid.isdigit():
        print "The upper hostid is not valid\n"
        return False
    
    #the ip net-id format:
    # xxx.xxx.xxx.
    ip_num = ''
    dot_count = 0
    
    for c in ip_prefix:
        if c != '.':
            ip_num += c
        elif ip_num.isdigit():
            dot_count += 1
            if int(ip_num) > 0 and int(ip_num) <= 255:
                ip_num = ''
            else:
                print "The ip prefix inputted is invalid\n"
                print "The number should be between in 1~255\n"
                return False

    if dot_count != 3:
        print "The ip prefix inputted is invalid\n"
        print "it should be inputted as followed:\n"
        print "xxx.xxx.xxx."
        return False
    return True

def help():
    print "How to use this script:\n"
    print "python ping_list.py ip_prefix lower_hostid upper_hostid\n"
    print "For example:\n"
    print "python ping_list.py 10.4.6. 1 10"

if __name__ == '__main__':
    #sys.argv[1] ---> ip_prefix
    #sys.argv[2] ---> lower_hostid
    #sys.argv[3] ---> upper_hostid
    if check_param_valid(sys.argv[1], sys.argv[2], sys.argv[3]):
        ping_list(sys.argv[1], sys.argv[2], sys.argv[3]) 
    else:
        quit()
 #  print "script_name:", sys.argv[0]
 #  for i in range(1, len(sys.argv)):
 #  	   print "parameter:", i, sys.argv[i]
