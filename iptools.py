#!/usr/bin/env python
#!encoding:utf-8

import optparse
from cymruwhois import Client
import os

# 读取ip列表进行查询
def look(ip_list):

    c = Client()
    try:
	r = c.lookupmany_dict(ip_list)
	for ip in ip_list:
	    pt = r[ip].prefix + " ------> " + r[ip].ip + "\n" + \
		 r[ip].cc + "\t" + r[ip].owner
	    print pt + "\n" + "-"*60   
    except Exception as e:
	print e
	pass


def get_ips(ipfile):

    ip_list = []

    if not os.path.isfile(ipfile):
        print '[-] ' + ipfile + ' does not exist.'
        exit(1)
    if not os.access(ipfile, os.R_OK):
        print '[-] ' + ipfile + ' access denied.'
        exit(1)
    print '[+] Querying from:  ' + ipfile

    with open(ipfile,'r') as f:
	for line in f.readlines():
	    ip_list.append(line.rstrip())
    return ip_list    
	
def main():

    parser = optparse.OptionParser('%prog ' + \
	    '-r <ip_file> || -i <ip>')
    parser.add_option('-r', dest='ipfile', type='string',\
	    help='specify target file with ips')
    parser.add_option('-i', dest='ip', type='string',\
	    help='specify target with ip')

    (options, args) = parser.parse_args()
    ip	   = options.ip
    ipfile = options.ipfile

    if ip == None and ipfile == None:
	print parser.usage
	exit(1)

    if ip and ipfile :
	print parser.usage
	exit(1)

    if ipfile != None:  
	ip_list = get_ips(ipfile)
	look(ip_list)
    else:
	c = Client()
	try:
	    try:
		r = c.lookup(ip)
	    except Exception as e:print e
	    pt = r[ip].prefix + " ------> " + r[ip].ip + "\n" + \
		 r[ip].cc + "\t" + r[ip].owner
	    print pt + "\n" + "-"*60
	except Exception as e:
	    print e

if __name__ == '__main__':
    main()
