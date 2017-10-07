#!/usr/bin/env python
# encoding:utf8
import requests
import re
import sys
import optparse
from bs4 import BeautifulSoup
from urllib import quote

##########################################################

__version__ = "1.0"
__prog__    = "Searpy"
__author__  = "whois"
__date__    = "2016/1/1"
#########################################################

banner = """
    
"""

# set shadowsocks proxy
Proxy = {
    'http':'http://127.0.0.1:1080',
    'https':'http://127.0.0.1:1080'
    }

Headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cache-Control':'max-age=0', 
                'Connection':'keep-alive', 
                'Referer': 'https://www.zoomeye.org',
                'Cookie': '__jsluid=fae27ad046bd22fca181a42209bf2a21;',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 
            }

url_list = [] 

def save_file(save_file, content):
    with open(save_file, 'a') as f:
        f.writelines(content + '\n')

# www.zoomeye.com    
def zoomeye(search,mypage,type1,output):
    
    url = "https://www.zoomeye.org/search"
   
    for page in xrange(1,mypage+1):
        try:
            payload = {'q':search,'p':str(page),'t':type1}
            r = requests.get(url,params=payload,headers=Headers)
            print r.url
            [ url_list.append(u) for u in rer.findall(r.content) if u not in url_list ]
        except Exception:
            pass
    
    with open(output,'a') as f:        
        for uu in url_list:
            if options.type1 == "web": 
                f.writelines('http://'+uu+'\n') 
            else:
                f.writelines(uu+'\n')


# www.baidu.com
def baidu(search,page):

    for n in range(0, page*10, 10):
        base_url = 'https://www.baidu.com/s?wd=' + str(quote(search)) + '&oq=' + str(quote(search)) + '&ie=utf-8' + '&pn=' + str(n)
        try:
            r = requests.get(base_url, headers=Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.c-container > h3 > a'):
                url = requests.get(a['href'], headers=Headers,timeout=5).url
                yield url
        except:
            yield None


# www.so.com
def so(search, page):

    for n in range(1, page+1):
        base_url = 'https://www.so.com/s?q=' + str(quote(search)) + '&pn=' + str(n) + '&fr=so.com'
        try:
            r = requests.get(base_url, headers=Headers)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('li.res-list > h3 > a'):
                url1 = requests.get(a['href'], headers=Headers, timeout=5)
                url = re.findall("URL='(.*?)'", url1.text)[0] if re.findall("URL='(.*?)'", url1.text) else url1.url
                yield url
        except:
            yield None


# www.google.com.hk
def google(search, page):

    for n in range(0, 10*page, 10):
        base_url = 'https://www.google.com.hk/search?safe=strict&q=' + str(quote(search)) + '&oq=' + str(quote(search)) + 'start=' + str(n)
        try:
            r = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}, proxies=Proxy, timeout=16)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('div.kv cite'):
                url = a.text
                yield url
        except Exception as e:
            print e
            yield None



if __name__ == '__main__':
    
    parser = optparse.OptionParser(
                usage="Usage: %prog [OPTION]",
                version="%s: v%s (%s)" % (__prog__, __version__, __author__),
                epilog="Example: Searpy -b -s site:baidu.com -p 10 -o file.txt ",
            )
    
    parser.add_option("-z", "--zoomeye", action='store_true', dest="zoomeye",
            help="Using Zoomeye Search")
    parser.add_option("-b", "--baidu", action="store_true", dest="baidu",
            help="Using Baidu Search")
    parser.add_option("-g", "--google", action="store_true", dest="google",
            help="Using Google Search")
    parser.add_option("-x", "--so", action="store_true", dest="so",
            help="Using 360So Search")
    parser.add_option("-s", "--search", dest="search",type="string",
            help="Specify Keyword")
    parser.add_option("-o", "--output", dest="output",
            type="string", help="Specify output file default output.txt")
    parser.add_option("-t", "--type", dest="type1", default="web",
            type="string", help="Zoomeye Search Type default [web],[host]")
    parser.add_option("-p","--page",dest="page",default=100,
            type="int", help="Baidu &Google page default 10")

    (options, args) = parser.parse_args()
    
    if options.zoomeye == None and options.baidu == None and options.so == None and options.google == None:
        parser.print_help()
        sys.exit(0)

    if options.zoomeye:
        if options.type1 == "host": 
            rer = re.compile(r'<a class="ip" href="\/search\?q=ip:.*?">(.*?)</a>')
        elif options.type1 == "web":
            rer = re.compile(r'<p class="domain">(.*?)</p>')
        else:
            print "[x] Type is error!"
            sys.exit(1)
        zoomeye(options.search,options.page,options.type1,options.output)

    if options.baidu:
        for url in baidu(options.search, options.page):
            if options.output:
                print url
                save_file(options.output, url)
            else:
                print url

    if options.so:
        for url in so(options.search, options.page):
            if options.output:
                print url
                save_file(options.output, url)
            else:
                print url

    if options.google:
        for url in google(options.search, options.page):
            if options.output:
                print url
                save_file(options.output, url)
            else:
                print url

