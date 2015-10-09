#!/usr/bin/env python
#!encoding:utf-8

import socket
import Queue
from threading import Thread
import optparse
import mycolor
import time
import os
import signal

tag_ok   = mycolor.color.blue + '[+]' + mycolor.color.end
tag_info = mycolor.color.yellow + '[*]' + mycolor.color.end

def scan(domain,target_port):	

    while not target_port.empty():
	port = target_port.get()
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	socket.setdefaulttimeout(1)

	try:
	    client.connect((domain,port))
	    
	    if port in [80,81,82,443,8080,8088,8008,8843]:	
		client.send("GET / HTTP/1.0\r\n\r\n")	
	    else:
	        client.send("scan")
	
	    banner = mycolor.color.cyan + client.recv(512) + mycolor.color.end
	    
	    if banner:
	        print(tag_ok + mycolor.color.green + " Port:%s is open \n" %port + banner)
	    else:
	    	print(tag_ok + mycolor.color.green + "  Port:%s is open \n" %port)
 
	except Exception,e: pass

	client.close()

def kill_me(a,b):
      
    print "[!] End!"
    pid = os.getpid()
    os.system('kill -9 ' + str(pid))

def main():
    
    parser = optparse.OptionParser("Usage: ./kscan.py -d <domain> -t <threads> -v ")
    parser.add_option('-d','--domain',dest='domain',type='string',\
	help='specify target domain')
    parser.add_option('-t','--threads',dest='threads',type='int',\
	help='specify threads,default 20')
    parser.add_option('-v','--verbose',dest='verbose',\
	action='store_true',default=False,help='show verbose')
    
    (options, args) = parser.parse_args()

    domain  = options.domain
    threads = options.threads

    if domain == None:
	print(parser.usage)
	exit(0)

    if threads == None:
	threads = 30
    
    port_queue = Queue.Queue()
    port_list = [21,22,23,25,53,80,81,82,110,111,139,161,199,443,445,3306,1443,1521,3389,8008,8080,8088,8843]

    for p in port_list:
	port_queue.put(p)

    if options.verbose:
	print(tag_info + mycolor.color.yellow + "Starting post scan..." + mycolor.color.end)
	print(tag_info + mycolor.color.yellow + "Target is " + domain + ',Threads is ' + str(threads) + mycolor.color.end + '\n')
	time.sleep(1)

    for t in range(threads):
	Thread(target=scan,args=(domain,port_queue,)).start()
	signal.signal(signal.SIGINT,kill_me) 

if __name__ == "__main__":
    main()
