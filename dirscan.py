#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import sys
import Queue
import random

__author__ = 'kkk'
__date__   = '17/5/17'

with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

if len(sys.argv) == 1:
    print "[]-----------------Dir Scan----------------[]"
    print "[]================bypass-waf===============[]"
    print "[*] python {0} [target] <proxy_ip>".format(sys.argv[0])
    exit(1)

TARGET = sys.argv[1]
IPFILES = sys.argv[2] if len(sys.argv) >= 3 else 'output/proxy_ip.txt'
WEBPATH = sys.argv[3] if len(sys.argv) == 4 else "e:\Tools\PassList\Webpath\\fuckyou.txt"

with open(IPFILES,'r') as f:
    proxy_ip_list = [ line.rstrip() for line in f.readlines()]

web_file = Queue.Queue()
with open(WEBPATH,'r') as f:
    for line in f.readlines():
        web_file.put(line.rstrip())

def cc(web_file):
    HEADERS = {'user-agent':random.choice(agents_list)}
    proxy_ip = random.choice(proxy_ip_list)
    url = TARGET + '/' + web_file
    try:
        r = requests.get(url, headers=HEADERS,timeout=10, proxies={'http':proxy_ip})
        if r.status_code not in [404,400,500,505]:
            print "[" + str(r.status_code) + "] " + " [" + len(r.content) + "] " + url + " ["+proxy_ip+"]"
    except:
        pass

def attack():
    while not web_file.empty():
        cc(web_file.get())

def main():
    threads_list = []
    threads = 10

    for i in range(threads):
        t = Thread(target=attack)
        t.start()
        threads_list.append(t)
    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
