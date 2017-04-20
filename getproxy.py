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
__list__ = ['http://www.samair.ru/proxy/',
            'http://www.xicidaili.com',
            'http://spys.ru/',
            ''
           ]

with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]

HEADERS = {'user-agent':random.choice(agents_list),'referer':'http://www.baidu.com'}
TARGET = 'http://www.xicidaili.com/nn/'
TIMEOUT = 5
PROXY = ''
PAGE = 11

def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS,timeout=TIMEOUT)
        print "[*] Request " + url
    except:
        print "[-] Some error, Please your network or websites"
        exit(1)
    return r.content

def file_output(ips):
    o_time = time.strftime('%d-%H-%M', time.localtime())
    output = 'output/' + 'ips-' + o_time + '.txt'
    with open(output,'a') as f:
        f.writelines(ips)
    return output

def get_proxy(url):
    rer = re.compile(r'<td>([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})</td>\s*<td>(\d{2,4})</td>')
    web_content = get_content(url)
    m = rer.findall(web_content)
    return m

    
def check_proxy(ip_file):

    test_sites = 'http://www.baidu.com'
    with open(ip_file,'r') as f:
        for u in f.readlines():
            url = 'http://' + u.rstrip()

            try:
                r = requests.get(test_sites, headers=HEADERS,timeout=TIMEOUT, proxies={'http':url})
                if r.status_code == 200:
                    print url
                    with open(ip_file+'.ok','a') as ff:
                        ff.writelines(u)
            except:
                pass

def main():
    for i in range(1,PAGE):
        url = TARGET + str(i)
        m = get_proxy(url)
        for k, v in m:
            ip_file = file_output(k + ':' + v + '\n')
    check = raw_input('check proxy ..(y/n)')
    check_proxy(ip_file) if check == 'y' else exit

if __name__ == '__main__':
    main()
        
