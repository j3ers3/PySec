#!/usr/bin/env python
# encoding:utf-8
import requests
import re
import sys
import optparse
from bs4 import BeautifulSoup
from urllib import quote

##########################################################

__version__ = "0.4"
__prog__    = "Searpy"
__author__  = "kkk"
__date__    = "2016/1/1"
#########################################################

Proxy = {'http':'http://127.0.0.1:8787'}
Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cache-Control':'max-age=0', 
                'Connection':'keep-alive', 
                'Keep-Alive':'115',
                'Referer': 'https://www.zoomeye.org',
                'Cookie': '__jsluid=fae27ad046bd22fca181a42209bf2a21; __jsl_clearance=1492699998.338|0|AIrJFUIrEfNaNz%2FeQLHWFMGeHzg%3D; Hm_lvt_e58da53564b1ec3fb2539178e6db042e=1492413982,1492608716,1492673792,1492695782; Hm_lpvt_e58da53564b1ec3fb2539178e6db042e=1492700941',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 
            }
url_list = [] 

def save_fun(save_file, content):
    with open(save_file, 'a') as f:
        f.writelines(content + '\n')
    
def zoomeye(search,mypage,type1,output):
    
    url = "https://www.zoomeye.org/search"
   
    for page in xrange(1,mypage+1):
        try:
            payload = {'q':search,'p':str(page),'t':type1}
            r = requests.get(url,params=payload,headers=Headers)
            print r.url
            [url_list.append(u) for u in rer.findall(r.content) if u not in url_list ]
        except Exception:
            pass
    
    with open(output,'a') as f:        
        for uu in url_list:
            if options.type1 == "web": 
                f.writelines('http://'+uu+'\n') 
            else:
                f.writelines(uu+'\n')

def baidu(search,page):

    for n in range(0,(page+1)*10,10):
        base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
        try:
            r = requests.get(base_url,headers=Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = requests.get(a['href'], headers=Headers,timeout=4).url
                yield url
        except:
            yield None

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
    parser.add_option("-o", "--output", dest="output", default="search_output.txt",
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
        zoomeye(options.search,options.page,options.type1,options.output)

    if options.baidu:
        for url in baidu(options.search,options.page):
            if url:
                print url
                save_fun(options.output, url)
            else:
                pass


    if options.google:
        pass
