#!/usr/bin/env python
#!encoding:utf-8
# show modules 
# 8/14

from mycolor import color

def show_modules():
    
    red_line = color.red + "------------------\t\t\t---------------" + color.end 
    print(color.blue + "Information Modules\t\t\tDescription" + color.end )    
    print(red_line)
   # print("info/shodan\t\t\t\t使用shodan查找域名信息")
    print("info/dir_scan\t\t\t\t目录爬行")
    print("\n")
    print(color.blue + "Exploit Modules\t\t\t\tDescription" + color.end)
    print(red_line)
    print("exp/discuz\t\t\t\tdiscuz 注入漏洞")
    print("exp/sms\t\t\t\tSMS attack")
    print("\n")
    print(color.blue + "Tools Modules\t\t\t\tDescription" + color.end)
    print(red_line)
    print("tools/12306\t\t\t\t12306火车票查询")
    print("tools/ip\t\t\t\tIP查询")
    print("\n")
    print(color.blue + "Netword Modules\t\t\t\tDescription" + color.end)
    print(red_line)
    print("\n")
    print(color.blue + "Password Modules\t\t\t\tDescription" + color.end)
    print(red_line)
    print("burp/web\t\t\t\t对认证页面进行暴力破解")
    print("\n")

    

