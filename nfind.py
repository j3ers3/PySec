#!/usr/bin/env python
# encoding:utf8
import sys
import os

"""
    用nmap的脚本针对内网常见服务的快速扫描
    主要发现弱口令，一些漏洞
    脚本和端口可自己选择
"""

user_path = 'E:\Tools\PassList\Passwords\Services\username.txt'
pass_path = 'E:\Tools\PassList\Passwords\Services\password.txt'
result = 'output/result.txt'

if len(sys.argv) != 2:
    print '[*] python nmap.py target'
    print 'ex: python find.py 192.168.0.1/16'
    exit(1)
    
target = sys.argv[1] 

command = 'nmap -sS -sV -v -T4 -oN {output} -D 223.99.11.1,me,111.11.123.1 --script rdp-vuln-ms12-020,ssl-heartbleed,rsync-list-modules,ftp-vsftpd-backdoor,ftp-proftpd-backdoor,irc-unrealircd-backdoor,ftp-brute,ms-sql-brute,mysql-brute,pop3-brute,redis-brute,rexec-brute,rlogin-brute,smb-brute,smtp-brute,snmp-brute,telnet-brute,vnc-brute --script-args "userdb={user},passdb={pwd}" -p 21,22,23,25,53,67,68,69,80,88,110,111,389,443,445,488,512,514,873,901,1080,1024,1089,1090,1158,1352,1433,1434,1521,2181,2375,2601,3128,3306,3389,4848,4444,5432,5632,5900,5984,6082,6379,6666,6667,7001,7002,8000,8001,8008,8069,8080,8081,8083,8087,8161,8443,8686,8649,8787,8888,9090,9200,9300,11211,22222,27017,27018,33389,50000,50070 --open -Pn -iL {target}'.format(output=result, user=user_path, pwd=pass_path, target=target)

os.system(command)
