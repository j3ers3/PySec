#!/usr/bin/python

import re
import os

# password = open("C:\\密码字典.txt")
password = open("../../PassList/Passwords/pass_web_good.txt")
pass_ok = open("ok.txt",'a+')
#匹配8-16个字符，必须满足大写字母、小写字母、数字、特殊符号四个条件
# patten = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[\\`~!@#$%^&*()_+\/*\-=.\[\]\{\}\":;\'?,<>]).{8,16}$"

#匹配8-16个字符，大小写字母，数字，特殊符号，满足三个条件即可
patten = "^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\\W_]+$)(?![a-z0-9]+$)(?![a-z\\W_]+$)(?![0-9\\W_]+$)[a-zA-Z0-9\\W_]{1,16}$"

#匹配8-16个字符，至少存在1个字母，1个数字和1个特殊字符：
# patten = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[\\`~!@#$%^&*()_+\/*\-=.\[\]\{\}\":;\'?,<>])[A-Za-z\d\\`~!@#$%^&*()_+\/*\-=.\[\]\{\}\":;\'?,<>]{6,16}$"

#匹配8-16个字符，至少存在一个大写字母 一个小写字母  一个数字8-16位 不带特殊字符
# patten = "(?![0-9A-Z]+$)(?![0-9a-z]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,20}$"

#匹配8-16个字符，数字和字母须同时存在
#patten = "^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{1,15}$"

#匹配8-16个字符，至少存在一个大写字母、一个数字，不能有三个相同的字符，特殊字符包括~!@&$%^*()_#

count = 0
ok_count = 0
passlist = []

for count,line in enumerate(password):
    passlist.append(line)
count += 1 
print("共读取到 "+str(count)+" 条密码")

for pwd in passlist:
    pwd = pwd.strip("\n")
    try:
        re_ok = re.search(patten,pwd).group(0)
        ok_count += 1 
        info = re_ok+"\n"
        pass_ok.write(info)
        print(re_ok)
    except Exception:
        continue
    # print(re_ok)
print("在%d条密码中提取到了%s条符合条件的密码" % (count,ok_count))
