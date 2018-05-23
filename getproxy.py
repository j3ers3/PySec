#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import Queue
import random
import sys
import re

__author__    = 'whois'
__update__    = '18/2/1'
__version__    = '1.1'
__proxy_site__ = [
            'http://www.samair.ru/proxy/',
            'http://www.xicidaili.com',
            'http://spys.ru/',
            'https://www.kuaidaili.com/free/'
        ]


def banner():
    print """
  ____      _   ____                      
 / ___| ___| |_|  _ \ _ __ _____  ___   _ 
| |  _ / _ \ __| |_) | '__/ _ \ \/ / | | |
| |_| |  __/ |_|  __/| | | (_) >  <| |_| |
 \____|\___|\__|_|   |_|  \___/_/\_\\__, |
                                    |___/\n
                             code by whois\n
"""


with open('pytxt/user-agents.txt','r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]


HEADERS = {'user-agent':random.choice(agents_list), 'referer':'http://www.baidu.com'}
SITE_CHOOSE = 1                     # 选择代理网站，1为西刺，2为快代
TEST_SITE = 'http://a.newfree.pw'                       
TIMEOUT = 7
PROXY = ''
PAGE = 30
THREADS = 10
output1 = 'output/proxy_ips.txt'
output2 = 'output/proxy_ips_ok.txt'


def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        print "[*] Request " + url
    except Exception as e:
        print "[x] Some error -> request proxy_site !"
        exit(1)
    return r.content


def file_output(output_file, ips):
    with open(output_file, 'a') as f:
        f.writelines(ips)


def do(pr_ip):
    try:
        r = requests.get(TEST_SITE, headers=HEADERS, timeout=TIMEOUT, proxies={'http':pr_ip})
        if r.content:
            print pr_ip
            file_output(output2, pr_ip+'\n')
    except:
        pass


def check():
    while not proxy_ip.empty():
        do(proxy_ip.get())


def getmode(save_file):
    if SITE_CHOOSE == 1:
        # 西刺代理的正则
        TARGET = 'http://www.xicidaili.com/nn/'
        rer = re.compile(r'<td>([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})</td>\s*<td>(\d{2,4})</td>')

    elif SITE_CHOOSE == 2:
        # 快代的正则
        TARGET = 'https://www.kuaidaili.com/free/inha/'
        rer = re.compile(r'IP">(.*?)</td>\n\s*<td data-title="PORT">(.*?)</td>')

    for i in xrange(1, PAGE):
        url = TARGET + str(i)
        web_content = get_content(url)
        ip_port = rer.findall(web_content)

        # ('110.73.40.66', '8123')

        for ip, port in ip_port:
            file_output(save_file, ip + ':' + port + '\n')


def checkmode(proxy_ip_file):
    global proxy_ip
    proxy_ip = Queue.Queue()

    with open(proxy_ip_file, 'r') as f:
        for line in f.readlines():
            # 判断是否加上了http://
            if 'http' in line:
                proxy_ip.put(line.rstrip())
            else:
                proxy_ip.put('http://' + line.rstrip())

    threads_list = []
    
    for i in xrange(THREADS):
        t = Thread(target=check)
        t.start()
        threads_list.append(t)
    for i in range(THREADS):
        threads_list[i].join()


def main():
    if len(sys.argv) < 2:
        banner()
        print "[v] python getproxy.py [mode] <file> default output/proxy_ips.txt\n"
        print "[v] python getproxy.py get <save_file>"
        print "[v] python getproxy.py check <read_file>\n"
        print "[Example] python getproxy.py get"
        print "[Example] python getproxy.py check proxy_ip.txt"
        exit(1)
    
    mode = sys.argv[1]

    if mode == 'get':
        getmode(sys.argv[2]) if len(sys.argv) == 3 else getmode(output1)
       
    elif mode == 'check':
        checkmode(sys.argv[2]) if len(sys.argv) == 3 else checkmode(output1)
            
    else:
        banner()
        exit(1)


if __name__ == '__main__':
    main()