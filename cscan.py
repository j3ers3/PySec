#!/usr/bin/env python
# encoding:utf8

import sys
import socket
import ipaddr
import requests
from time import time
from threading import Thread
from bs4 import BeautifulSoup 

if sys.version_info.major == 2:
    from Queue import Queue
else:
    from queue import Queue


requests.packages.urllib3.disable_warnings()


__author__ = "whois"
__update__ = "2019/06/30"
"""
C段web扫描，选取几个web端口，获取标题，版本信息

"""

Ports_web = [80, 81, 82, 88, 89, 443, 5000, 5001, 7001, 7070, 7777, 7788, 8000, 8001, 8002, 8008, 8080, 8081, 8088, 8089, 8090, 8443, 8888, 8899]

Ports_other = [21, 22, 445, 1433, 1434, 1521, 3306, 3389]

Ports = Ports_other + Ports_web

Threads = 45


user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"

purp   = '\033[95m'
blue   = '\033[94m'
red    = '\033[31m'
yellow = '\033[93m'
end    = '\033[0m'

queue = Queue()


def banner():
    print(red + """
                        ..:::::::::..
                  ..:::aad88x8888baa:::..
              .::::d:?88888xxx888?::8b::::.
            .:::d8888:?888xxxxx??a888888b:::.
          .:::d8888888a8888xxxaa8888888888b:::.
         ::::dP::::::::88888x88888::::::::Yb::::
        ::::dP:::::::::Y888888888P:::::::::Yb::::
       ::::d8::::x::::::Y8888888P:::::x:::::8b::::
      .::::88::::::::::::Y88888P::::::::::::88::::.
      :::::Y8baaaaaaaaaa88P:T:Y88aaaaaaaaaad8P:::::
      :::::::Y88888888888P::|::Y88888888888P:::::::
      ::::::::::::::::888:::|:::888::::::::::::::::
      `:::::::::::::::8888888888888b::::::::::::::'
       :::::::::::::::88888888888888::::::::::::::
        :::::::::::::d88888888888888:::::::::::::
         ::::::::::::88::88::88:::88::::::::::::
          `::::::::::88::88::88:::88::::::::::'
            `::::::::88::88::P::::88::::::::'
              `::::::88::88:::::::88::::::'
                 ``:::::::::::::::::::''
                      ``:::::::::''""" + yellow + """

    =================   WEB Info Scan  ==================
    =================   Code by whois  ==================
    +++++++++++++++++++++++++++++++++++++++++++++++++++++
                      
""" + end)


def get_info(url):
    try:
        # 页面的跳转没解决
        r = requests.get(url, headers={'UserAgent': user_agent}, timeout=6, verify=False, allow_redirects=True)
        soup = BeautifulSoup(r.content, 'lxml')

        info = blue + soup.title.string + end if soup.title.string else "No title"
 
        if 'Server' in r.headers:
            info += "\t" + yellow + r.headers['Server'] + end
        if 'X-Powered-By' in r.headers:
            info += "\t" + purp + r.headers['X-Powered-By'] + end 

        return info
    except Exception as e:
        pass


def do(ip):
    for port in Ports:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.settimeout(0.6)
            s.connect((str(ip),port))

            if port in Ports_other:
                url = str(ip) + ":" + str(port)
                info = blue + "open" + end

            else:
                if port in [443,8443]:
                    url = "https://" + str(ip)
                else:
                    url = "http://" + str(ip) + ":" + str(port)
                info = get_info(url)

            sys.stdout.write("%-28s %-30s\n" % (url, info))

            s.close()

        except Exception as e:
            s.close()
            continue


def scan():
    while not queue.empty():
        do(queue.get())


def main():

    if len(sys.argv) != 2:
        banner()
        print("[x] python {0} ip/24".format(sys.argv[0])) 
        exit(1)

    banner()

    ips = ipaddr.IPNetwork(sys.argv[1])

    for ip in ips:
        queue.put(ip)

    time_start = time()

    threads_list = []
    threads = Threads

    for i in range(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)

    for i in range(threads):
        threads_list[i].join() 

    time_end = time() - time_start
    print(blue + "\nScan End Time is {0}\n".format(time_end))



if __name__ == '__main__':
      main()





