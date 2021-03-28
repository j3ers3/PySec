#!/usr/bin/env python3
# encoding:utf8
import requests
import random
from time import time
import optparse
import threadpool

__author__ = 'whois'
__date__   = '19/09/26'
__prog__ = "bypass waf with random ip"
__version__ = '2.0'

purp   = '\033[95m'
blue   = '\033[94m'
red    = '\033[31m'
yellow = '\033[93m'
end    = '\033[0m'



banner = red + """
█████╗ ██╗██████╗ ██╗    ██╗ █████╗ ███████╗
██╔══██╗██║██╔══██╗██║    ██║██╔══██╗██╔════╝
██║  ██║██║██████╔╝██║ █╗ ██║███████║█████╗  
██║  ██║██║██╔══██╗██║███╗██║██╔══██║██╔══╝  
██████╔╝██║██║  ██║╚███╔███╔╝██║  ██║██║     
╚═════╝ ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     
""" + yellow + """
                            code by whois""" + end


with open('/Users/tianxia/DeathNote/Coder/Python/PySec/pytxt/user-agents.txt', 'r') as f:
    agents_list = [ line.rstrip() for line in f.readlines()]


# 使用代理池获取ip
# https://github.com/jhao104/proxy_pool
def get_proxy():
    json = requests.get("http://118.24.52.95/get_all/").json()
    for p in jsion:
        print(p.get("proxy"))


def scan(web_file):

    headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(agents_list),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'close',
        }

    proxy_ip = random.choice(proxy_ip_list)

    url = TARGET + '/' + web_file

    try:
        r = requests.get(url, headers=headers, timeout=12, proxies={"http":"http://{0}".format(proxy_ip)})

        if r.status_code not in [404,400,500,501,502,503,504,505]:
            print(red + "["+str(r.status_code)+"]" + "\t" + purp + str(len(r.content)) + "\t" +  yellow + url + "\t" + blue + proxy_ip + end)
    except Exception as e:
        # print(e)
        pass


def main():
    global proxy_ip_list
    global TARGET

    parser = optparse.OptionParser(
        usage="Usage: %prog [options]",
        version="{0}: v{1} ({2})".format(__prog__, __version__, __author__),
        epilog=yellow + """[Ex] python3 dirwaf.py -u http://1.1.1.1
                                [Ex] python3 dirwaf.py -u http://1.1.1.1 -t 10 -w w.txt -p proxy.txt""" + end,
    )

    parser.add_option("-u", "--url", dest="url",
            help="Target url")

    parser.add_option("-p", "--proxy", dest="proxy",
            help="proxy ip list")

    parser.add_option("-w", "--wordlist", dest="wordlist",
            help="wordlist")

    parser.add_option("-t", "--thread", dest="thread", type='int', 
            help="Specify threads default 12")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,
            help="verbose mode")

    (options, args) = parser.parse_args()

    if options.url == None:
        print(banner)
        parser.print_help()
        exit(1) 

    THREAD = 8 if not options.thread else options.thread
    WEBPATH = "/Users/tianxia/Pentest/PassList/Webpath/fuckyou.txt" if not options.wordlist else options.wordlist
    IPFILES = "/Users/tianxia/DeathNote/Coder/Python/PySec/output/proxy_ip.txt" if not options.proxy else options.proxy

    with open(IPFILES, 'r') as f:
        proxy_ip_list = [ line.rstrip() for line in f.readlines() ]

    TARGET = options.url

    if 'http' not in TARGET:
        print("[x] Perhaps you meant http://{0}".format(TARGET))
        exit(1) 

    if options.verbose:
        print("[+] Load webpath {0}".format(WEBPATH))
        print("[+] Load proxy_ip_file {0}".format(IPFILES))
        print("[+] Scan with {0} threads\n".format(THREAD))

    with open(WEBPATH, 'r') as f:
        lines = f.read().splitlines()
        try:
            time_start = time()

            pool = threadpool.ThreadPool(THREAD)
            requests = threadpool.makeRequests(scan, lines)
            [pool.putRequest(req) for req in requests]
            pool.wait() 

            time_end = time() - time_start       
            print(blue + "\nScan End Time is {0}\n".format(time_end))

        except KeyboardInterrupt:
            print(red + "[-] Ctrl+C")
            exit(1)


if __name__ == '__main__':
    main()

