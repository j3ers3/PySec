#!/usr/bin/env python

import zipfile
from threading import Thread
import optparse

def crack(zFile,passwd):
    
    try:
	zFile.extractall(pwd=passwd)
	print("[+]Password is " + passwd)
    except:pass

def main():

    parser = optparse.OptionParser("usage%prog " +\
	"-f <zipfile> -d <dictionary> -v <verbose>")
    parser.add_option('-f','--file',dest='zname',type='string',\
	help='specify zip file')
    parser.add_option('-d','--dict',dest='dname',\
	type='string',help='specify dictionary file')
    parser.add_option('-v','--verbose',dest='verbose',\
	action='store_true',default=False,help='show verbose')

    (options, args) = parser.parse_args()

    if (options.zname == None) and (options.dname == None):
	print(parser.usage)
	exit(0)

    zFile = zipfile.ZipFile(options.zname)

    with open(options.dname,'r') as f:

	for passwd in f.readlines():
	    if options.verbose:
		print("[*] Try passwd:" + passwd.rstrip())
	    t = Thread(target=crack,args=(zFile,passwd.rstrip())).start()

if __name__ == '__main__':
    main()
