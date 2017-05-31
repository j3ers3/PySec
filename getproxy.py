#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import Queue
import random
import time
import re

__author__ = 'kkk'
__date__   = '16/7/26'
__pro__    = 'get proxies from some websites'
__list__    = [
    'http://www.samair.ru/proxy/',
    'http://www.xicidaili.com',
    'http://spys.ru/',]

with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

HEADERS = {'user-agent':random.choice(agents_list),'referer':'http://www.baidu.com'}
TARGET = 'http://www.xicidaili.com/nn/'
TIMEOUT = 6
PROXY = ''
PAGE = 2
output = 'output/proxy_ips.txt'

def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS,timeout=TIMEOUT)
        print "[*] Request " + url
    except:
        print "[-] Some error, Please your network or websites"
        exit(1)
    return r.content

def file_output(ips):
    print output
    with open(output,'a') as f:
        f.writelines(ips)

def get_proxy(url):
    rer = re.compile(r'<td>([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})</td>\s*<td>(\d{2,4})</td>')
    web_content = get_content(url)
    m = rer.findall(web_content)
    return m

def do(proxy_ip):
    test_sites = 'http://baidu.com'
    try:
        r = requests.get(test_sites, headers=HEADERS,timeout=TIMEOUT, proxies={'http':proxy_ip})
        if r.status_code == 200:
            print url
            with open(output+'.ok','a') as f:
                f.writelines(u)
    except:
        pass

def check():
    while not proxy_ip.empty():
        do(proxy_ip.get())

def main():

    for i in range(1,PAGE):
        url = TARGET + str(i)
        m = get_proxy(url)
        for k, v in m:
            file_output(k + ':' + v + '\n')

    check = raw_input('check proxy ..(y/n)')
    if check == 'y':
        proxy_ip = Queue.Queue()
        with open(output,'r') as f:
            for line in f.readlines():
                proxy_ip.put('http://' + u.rstrip())

        threads_list = []
        threads = 15
        for i in range(threads):
            t = Thread(target=check)
            t.start()
            threads_list.append(t)
        for i in range(threads):
            threads_list[i].join()
    else:
        exit

if __name__ == '__main__':
    main()
        
