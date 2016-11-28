#!/usr/bin/env python
# encoding:utf-8
import requests
import re
import sys
import optparse
from bs4 import BeautifulSoup

##########################################################

__version__ = "0.2"
__prog__    = "Searpy"
__author__  = "Whois"
__date__    = "2016/1/1"
#########################################################

Proxy = {'http':'http://127.0.0.1:8787'}
Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
                'Accept-Language':'zh-cn,zh;q=0.5', 
                'Cache-Control':'max-age=0', 
                'Connection':'keep-alive', 
                'Keep-Alive':'115',
                    'User-Agent':'Mozilla/5.0 (X11; U; Linux x86; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/9.9 (maverick) Firefox/3.6.14'}
Url_list = [] 

    
def zoomeye(search,type1,output):
    
    url = 'https://zoomeye.org/search'
   
    for page in xrange(1,11):
        try:
            payload = {'q':search,'p':str(page),'t':type1}
            r = requests.get(url,params=payload,headers=Headers)
            print r.url 
            [Url_list.append(u) for u in rer.findall(r.content) if u not in Url_list ]
        except Exception:
            pass
    
    with open(output,'a') as f:        
        for uu in url_list:
            f.writelines('http://'+uu+'\n')

def baidu(search,page,output):

    for x in range(0,(page+1)*10,10):
        url = 'http://wap.baidu.com/s'   
        payload = {'pn':x,'word':search}
        r = requests.get(url,params=payload,headers=Headers)
        soup = BeautifulSoup(r.content,'lxml')
        html = soup.find('div', id="results")
        html_doc = html.find_all('div', class_="c-showurl") if html else "[-] Error..."
        if not html_doc:
            print "[-] Warning"
        else:
            for doc in html_doc:
                try:
                    href=doc.find_all('span')[0].find_all(text=True)[0]
                    url = "http://" + str(href)
                    if url not in Url_list:
                        Url_list.append(url)
                except:
                    pass
    for u in Url_list:
        print u

    with open(output,'a') as f:  
        for uu in Url_list:  
            f.writelines(uu+'\n')

def google():
   """ url = "http://www.google.com/search?start=" + str(page) + "&q" + search + "&hl=en"
    try:
        r = requests.get(url,proxies=Proxy,headers=Headers,timeout=5)
    except:
        print "[-] Google cant access"
        exit(1)
    results = r.content
"""


if __name__ == '__main__':
    
    parser = optparse.OptionParser(
                usage="Usage: %prog [OPTION]",
                version="%s: v%s (%s)" % (__prog__, __version__, __author__),
                epilog="Example: Searpy -b -s inurl:php -p 30 -o file.txt ",
            )
    
    parser.add_option("-z", "--zoomeye", action='store_true', dest="zoomeye",
            help="Using Zoomeye Search")
    parser.add_option("-b", "--baidu", action="store_true", dest="baidu",
            help="Using Baidu Search")
    parser.add_option("-g","--google",action="store_true", dest="google",
            help="Using Google Search")
    parser.add_option("-s", "--search", dest="search",type="string",
            help="Specify Keyword")
    parser.add_option("-o", "--output", dest="output", default="output.txt",
            type="string", help="Specify output file default output.txt")
    parser.add_option("-t", "--type", dest="type1", default="web",
            type="string", help="Zoomeye Search Type default [web],[host]")
    parser.add_option("-p","--page",dest="page",default=250,
            type="int", help="Baidu &Google page default 25")

    (options, args) = parser.parse_args()
    
    if options.zoomeye == None and options.baidu == None:
        parser.print_help()
        sys.exit(0)

    if options.zoomeye:
        if options.type1 == "host": 
            rer = re.compile(r'<a class="ip" href="\/search\?q=ip:.*?">(.*?)</a>')
        elif options.type1 == "web":
            rer = re.compile(r'<p class="domain">(.*?)</p>')
        else:
            print "[-] Type is error!"
            sys.exit(1)
        zoomeye(options.search,options.type1,options.output)

    if options.baidu:
        baidu(options.search,options.page,options.output)    

    if options.google:
        pass
