#!/usr/bin/env python
#encoding:utf8
import json
import sys
import os
import time

rate = 500
del_file = 'masscan.json'

"""
将masscan结果输出为ip：port到文件中
扫描     => m 10.8.1.1/16 80
"""

def name(ips):
    t = str(time.time()).split('.')[0]
    name = ips.split('/')[0]
    try:
        name2 = ips.split('/')[1]
        return name+"_"+name2+"_"+t
    except:
        return name+"_"+t
    


def masscan_scan(ips, ports):
    try:
        os.system("masscan {1} -p{2} --rate {0} --wait 1 -oJ {3}".format(rate, ips, ports, del_file))
    except Exception as e:
        print("[-] masscan is error!!")


def masscan_json(name):
    scan_port = ''

    with open(del_file, 'r') as f:
        content = f.read()
        if content == '':
            print("[x] Not Fund Port or you can reset rate!!")
            exit()

        data = json.loads(content)

        for i in range(len(data)):
            ip = data[i]['ip']
            port = str(data[i]['ports'][0]['port'])
            res = ip + ":" + port
            print(res)

            with open('{0}'.format(name), 'a') as f:
                f.writelines(res + '\n')

    print("[+] output {0}".format(name))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("[*] port scan mode")
        print("[Example] python {0} 10.45.8.1/16 80,3306,3389".format(sys.argv[0]))
        print("\n[*] cscan with port scan result mode")
        print("[Example] python {0} 10.45.8.1/16 80,8080 cscan".format(sys.argv[0]))
        exit(1)

    ips = sys.argv[1]
    ports = sys.argv[2]

    out_file = name(ips) + '.txt'

    masscan_scan(ips, ports)
    masscan_json(out_file)

    os.system("rm -rf {0}".format(del_file))

    try:
        if sys.argv[3] == 'cscan':
            try:
                os.system('cscan -f {0}'.format(out_file))
            except:
                print("[-] git clone https://github.com/j3ers3/Cscan")
    except Exception as e:
        exit(1)


