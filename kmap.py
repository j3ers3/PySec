#!/usr/bin/env python
# encoding:utf8
from pytxt import mycolor
from threading import Thread
import socket
import Queue
import optparse
import time
import os
import signal

__version__ = "0.3"
__prog__    = "kmap"
__author__  = "whois"
__say__ = "玩玩而已"

tag_ok   = mycolor.color.blue + '[+]' + mycolor.color.end
tag_info = mycolor.color.yellow + '[*]' + mycolor.color.end
def scan(domain, target_port):

	while not target_port.empty():
		port = target_port.get()
	    	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)

		try:
			client.connect((domain,port))

			if port in [80, 81, 82, 88, 443, 8000, 8001, 8080, 8088, 8008, 8888, 8843]:
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

    	parser = optparse.OptionParser("Usage: kmap.py -d <domain> -t <threads> -v ")
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
		threads = 10

	port_queue = Queue.Queue()
	port_list = [21,22,23,25,53,67,68,69,80,88,110,111,389,443,445,488,512,514,873,901,1080,1024,1089,1090,1158,1352,1433,1434,1521,2181,2375,2601,3128,3306,3389,4848,4444,5432,5632,5900,5984,6082,6379,6666,6667,7001,7002,8000,8001,8008,8069,8080,8081,8083,8087,8161,8443,8686,8649,8787,8888,9090,9200,9300,11211,22222,27017,27018,33389,50000,50070]

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
