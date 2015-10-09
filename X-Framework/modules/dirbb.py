#!/usr/bin/env python

import requests
from threading import Thread
import Queue
import os
from core import help
from comm import *

options = ["http://www.exploit.com","/root/Py/X/dir.txt",20]

def dirscan():

    ksf_1 = ksf_line('Info Scan')
    com = raw_input(ksf_1)

    try:
	if com[0:10] == 'set THREAD':
	    threads    = com[11:]
	    options[2] = threads
	    print(tag_true + "set THREAD --> " + str(options[2]))
	    dirscan()

	elif com[0:9] == 'set RHOST':
	    target = com[10:]
	    options[0] = target
	    print(tag_true + "set RHOST --> " + options[0])
	    dirscan()
    
	elif com[0:8] == 'set DICT':
	    file_path = com[9:]
	    options[1] = file_path
	    print(tag_true + 'set DICT --> ' + options[1])
	    dirscan()

	elif com[0:12] == 'show options':
	    show_op()
	    print("RHOST\t\t"  + options[0] + "\t Target url")
	    print("DICT\t\t"   + options[1] + "\t Dict path")
	    print("THREAD\t\t" + str(options[2]) + "\t\t\t Specify Threads")
	    dirscan()

	elif com[0:1] == '!':
	    os.system(com[1:])
	    dirscan()

	elif com[0:4] == 'help':
	    help.help()
	    dirscan()
    
	elif com[0:4] == 'back':
	    pass
   
	elif com[0:4] == 'exit':
	    exit
 
	elif com[0:3] == 'run' or com[0:7] == 'exploit':
	    print_info("[*] Scan url")	
	    dir_path = Queue.Queue()
	    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/10100101 Firefox/19.0'}

	    with open(options[1],'r') as f:
		for line in f.readlines():
		    if not line.startswith('#'):
			line = line.rstrip()
			dir_path.put(line)
	
	    def scan(url):		
		while not dir_path.empty():
		    if url[-1:] != '/':
			url += '/'

		    url += dir_path.get()
		    r = requests.get(url,headers=headers)
	
		    if r.status_code != 404:
			print(tag_true + url + '\t' + str(r.status_code))
		    url = options[0]
	    
	    for t in range(int(options[2])):
		Thread(target=scan,args=(options[0],)).start()
	    dirscan()
	else:
	    dirscan()
    except KeyboardInterrupt:
	print_err("[*] Detected Ctrl-C ,System Exit...")

