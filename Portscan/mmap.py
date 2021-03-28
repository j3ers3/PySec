#!/usr/bin/env python3
# encoding: utf8
import os
import sys
import json
import socket
import time

"""
利用masscan快速扫描全端口，再调用nmap扫描服务,单一目标扫描
"""

blue = '\033[94m'
red = '\033[31m'
end = '\033[0m'

'''
配置masscan发包率，过大会导致丢包
T is 1500
X is 5000
local is 700
'''
rate = 600

outfile = 'masscan.json'


def banner():
    print(red + """

 ███▄ ▄███▓ ███▄ ▄███▓ ▄▄▄       ██▓███  
▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▒████▄    ▓██░  ██▒
▓██    ▓██░▓██    ▓██░▒██  ▀█▄  ▓██░ ██▓▒
▒██    ▒██ ▒██    ▒██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒
▒██▒   ░██▒▒██▒   ░██▒ ▓█   ▓██▒▒██▒ ░  ░
░ ▒░   ░  ░░ ▒░   ░  ░ ▒▒   ▓▒█░▒▓▒░ ░  ░
░  ░      ░░  ░      ░  ▒   ▒▒ ░░▒ ░     
░      ░   ░      ░     ░   ▒   ░░       
       ░          ░         ░  ░        

                            code by whois
""" + end)


def check_command():
    # if true return 0
    if os.system("command -v nmap >/dev/null 2>&1"):
        print("[-] nmap not found!")
        exit(1)
    elif os.system("command -v masscan >/dev/null 2>&1"):
        print("[-] masscan not found!")
        exit(1)


def rm():
    if os.path.exists(outfile):
        os.system("rm -rf {0}".format(outfile))
    if os.path.exists('paused.conf'):
        os.system("rm -rf paused.conf")


def getlocation(ip):
    print(blue + "[+] Get Location" + end)
    os.system("curl --connect-timeout 10 http://www.cip.cc/{0}".format(ip))


def domain2ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        pass


def masscan_scan(ip):
    print(blue + "\n[+] Masscan Staring" + end)
    # 存储为json格式
    os.system("masscan {1} -p1-65535 --rate {0} --wait 1 -oJ {2}".format(rate, ip, outfile))


def nmap_scan(ip, port_str):
    print(blue + "\n[+] Nmap scaning ports [{0}]\n".format(port_str) + end)
    os.system("nmap -sV -T4 -Pn {0} -p {1}".format(ip, port_str))


def json_port():
    scan_port = ''

    with open(outfile, 'r') as f:
        content = f.read()
        if content == '':
            print(red + "[x] Not Fund Port or you can reset rate!!")
            exit()

        data = json.loads(content)

        # masscan的格式是一个ip对一个端口
        # scan_ip = data[0]['ip']

        for i in range(len(data)):
            port = str(data[i]['ports'][0]['port'])
            scan_port += port + ','

    return scan_port


def main():
    banner()
    check_command()

    if len(sys.argv) != 2:
        print("[x] {0} [IP/Domain]".format(sys.argv[0]))
        exit(1)

    fuck_ip = domain2ip(sys.argv[1])

    start_time = time.time()

    print(blue + "[+] Current delivery rate is " + red + "{0}".format(rate) + end)
    getlocation(fuck_ip)
    masscan_scan(fuck_ip)
    nmap_scan(fuck_ip, json_port())

    end_time = time.time() - start_time

    print(red + "\n[+] All time is {0}".format(end_time) + end)

    rm()


if __name__ == "__main__":
    main()
