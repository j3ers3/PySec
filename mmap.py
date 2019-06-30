#!/usr/bin/env python3
# encoding: utf8
import os
import sys
import json
import socket
import time

"""
利用masscan快速扫描全端口，再调用nmap扫描服务
"""

blue   = '\033[94m'
red    = '\033[31m'
end    = '\033[0m'

'''
配置masscan发包率
T is 1500
X is 5000
local is 700
'''
rate = 1000


def getlocation(ip):
    print(blue + "[+] Get Location\n" + end)
    os.system("curl http://www.cip.cc/{0}".format(ip))



def domain2ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        pass


def masscan_scan(ip):
    print(blue + "\n[+] Masscan Staring" + end)
    os.system("masscan {1} -p1-65535 --rate {0} --wait 1 -oJ masscan.json".format(rate, ip))


def nmap_scan(ip, port_str):
    print(blue + "\n[+] Nmap scaning ports [{0}]\n".format(port_str) + end)
    os.system("nmap -sV -Pn {0} -p {1}".format(ip, port_str))
    

def json_port():
    scan_port = ''

    with open('masscan.json', 'r') as f:
        content = f.read()
        if content == '':
            print("[x] Not Fund Port!!!")
            exit()

        data = json.loads(content)

        # masscan的格式是一个ip对一个端口
        # scan_ip = data[0]['ip']

        for i in range(len(data)):
            port = str(data[i]['ports'][0]['port'])
            scan_port += port + ','

    return scan_port

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[x] python {0} IP_or_Domain".format(sys.argv[0]))
        exit(1)
        
    fuck_ip = domain2ip(sys.argv[1])

    start_time = time.time()
    print(blue + "[+] Current delivery rate is {0}\n".format(rate) + end)
    getlocation(fuck_ip)
    masscan_scan(fuck_ip)
    nmap_scan(fuck_ip, json_port())

    end_time = time.time() - start_time

    print(red + "\n[+] All time is {0}".format(end_time) + end)


