#!/usr/bin/env python
#!encoding:utf-8

'''
    这只是一个分析网页源码的小程序
    只使用-u 遍历目标地址链接，只到二级链接为止
    加上-a 加 -t 使用另一个模式，得到目标url的标签
    -i 得到头信息，邮箱，ip 
'''

from bs4 import BeautifulSoup
import requests
import Queue
from urlparse import urlsplit
import optparse
import re,sys
import socket

def banner():

    print("""
         __________________
        < WebInfo by whois >
	 ------------------
	        \   ^__^
		 \  (oo)\_______
		    (__)\       )\/\/
		        ||----w |
		        ||     ||  
	    """)

def get_url(url):

    url_list = []

    try:
	r = requests.get(url)
    except:
        sys.exit("[-] Please check your network")

    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)
    
    for link in soup.find_all('a'):
        try:
            new_url = urlsplit(link['href'])[1]
        except:pass

        if new_url not in url_list and url not in url_list:
            url_list.append(new_url)

    print("[+] ---> " + url)

    for x in url_list:print('\t' + x)
    
    return url_list

def url_all(url,tag):

    r    = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text)
    
    if tag == 'link':
        for t in soup.find_all('a'):
            print(t['href'])
    else:
        for t in soup.find_all(tag):
            print(t.prettify())
    
def get_headers(url):

    r = requests.get(url)
    print('[Status] --> ' + str(r.status_code))
    headers = r.headers
    
    for x in headers.keys():
        print(x + " : " + str(headers[x]))

    print("\n[+] Emails found:\n" + '-'* 40)
    reg_emails = re.compile('[a-zA-Z0-9.-_]*' + '@' + '[a-zA-Z0-9.-]*')
    
    for email in reg_emails.findall(r.text):
        print(email)

def get_ips(domain):
    
    result = socket.getaddrinfo(domain,None,0,socket.SOCK_STREAM)
    count = 1
    print("\n[+] IP found:\n" + '-' * 40 + '\n\n')
    
    for ip in result:
        print(str(count) + ' : ' + ip[4][0])
        count += 1    

def my_shodan(ip):

    from shodan import Shodan

    SHODAN_API_KEY = "sphexJZnbzincTbmgrmofXwGNjusg4Wr"
    api = Shodan(SHODAN_API_KEY)
    
    try:
        host = api.host(ip)
    except:
        sys.exit("\n[-] Shodan err,please check your domain or network!!!")

    print("[+] Shodan search:" + '\n' + '-' * 40)
    print(""" 
    IP:%s
    Organization:%s
    OS:%s
    """ % (host['ip_str'], host.get('org','n/a'), host.get('os','n/a')))

    for item in host['data']:
        print "Port:%s\nBanner:%s" % (item['port'], item['data'])
 
def main():

    banner()
    parser = optparse.OptionParser("[+]Usage: -u <url> | -a [url_all] -t <tag> or <link> | -i [info]")
    parser.add_option('-u','--url',dest='url',type='string',\
	help='Specify target url')
    parser.add_option('-a','--all',dest='all',\
	action='store_true',default=False,help='Show verbose url')
    parser.add_option('-t','--tag',dest='tag',type='string',\
	help='Specify tag for url or using link show other url')
    parser.add_option('-i','--info',dest='info',\
	action='store_true',default=False,help='Show targets infomation')

    (options,args) = parser.parse_args()

    url = options.url

    if options.url == None:
        sys.exit(parser.usage)
    
    if options.info:
        if not options.all and options.tag == None:
            domain = urlsplit(url)[1]
            ip = socket.gethostbyname(domain)
            get_headers(url)
            get_ips(domain)
            my_shodan(ip)
            exit(0)
        else:
            sys.exit(parser.usage)

    if options.all:
        if options.tag == None:
            sys.exit("[-]Using tag or link")
        else:
            print("[+] Get all tag for " + url)
            url_all(url,options.tag)
            exit(0)

    url_queue = Queue.Queue()
    for q in get_url(url):
        url_queue.put(q)

    while not url_queue.empty():
        new_link = 'http://' + url_queue.get()
        try:
            get_url(new_link)
        except:pass

if __name__ == '__main__':
    main()
