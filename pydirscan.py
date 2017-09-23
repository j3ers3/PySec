#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import sys
import Queue
import random

__author__ = 'whois'
__date__   = '17/5/17'
__say__ = "bypass waf with random ip"

with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

banner = """
_ __  _   _  __| (_)_ __ ___  ___ __ _ _ __  
| '_ \| | | |/ _` | | '__/ __|/ __/ _` | '_ \ 
| |_) | |_| | (_| | | |  \__ \ (_| (_| | | | |
| .__/ \__, |\__,_|_|_|  |___/\___\__,_|_| |_|
|_|    |___/ 
"""

if len(sys.argv) == 1:
    print banner
    print "[*] bypass waf"                         
    print "[*] python {0} url <proxy_ip> <webpath>".format(sys.argv[0])
    exit(1)

TARGET = sys.argv[1]
IPFILES = sys.argv[2] if len(sys.argv) >= 3 else 'output/proxy_ip.txt'
WEBPATH = sys.argv[3] if len(sys.argv) == 4 else "e:\Tools\PassList\Webpath\\fuckyou2.txt"

with open(IPFILES,'r') as f:
    proxy_ip_list = [ line.rstrip() for line in f.readlines() ]

web_file = Queue.Queue()

with open(WEBPATH,'r') as f:
    for line in f.readlines():
        web_file.put(line.rstrip())

def scan(web_file):
    HEADERS = {'user-agent':random.choice(agents_list)}
    proxy_ip = random.choice(proxy_ip_list)
    url = TARGET + '/' + web_file

    try:
        r = requests.get(url, headers=HEADERS,timeout=10, proxies={'http':proxy_ip})

        if r.status_code not in [404,400,500,501,502,503,504,505]:
            print "[{0}]\t{1}\t{2}\t{3}".format(r.status_code, len(r.content), url, proxy_ip)
            #print "[" + str(r.status_code) + "] " + " [" + len(r.content) + "] " + url 
        else:
            #sys.stdout.write('\r{0} '.format(web_file))
            pass
    except:
        pass

def attack():
    while not web_file.empty():
        scan(web_file.get())

def main():
    threads_list = []
    threads = 8

    for i in range(threads):
        t = Thread(target=attack)
        t.start()
        threads_list.append(t)
    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
