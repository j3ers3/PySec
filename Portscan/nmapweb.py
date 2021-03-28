#! /usr/bin/env python
# encoding:utf8
from sys import argv
import subprocess

output = "/var/www/nmapx/"

"""
<?xml-stylesheet href="nmap-bootstrap.xsl" type="text/xsl"?>

扫描结束后的文件与nmap-bootstrap.xsl放在同一个web目录下

"""

boot_url = "nmap-bootstrap.xsl"


def scan_all(url_file, out_file):
    cmd = "nohup nmap -sV -T4 -Pn -p- --open --stylesheet {0} -iL {1} -oX {2}&".format(boot_url, url_file, out_file)
    print("[+] Start a full scan\n {0}".format(cmd))
    subprocess.call(cmd, shell=True)


def scan_fast(url_file, out_file):
    cmd = "nohup nmap -sV -T4 -Pn --open -p 21,22,23,25,53,80-100,110,111,389,443,445,488,512-514,873,901,1043,1080-1100,1158,1352,1433,1434,1521,1522,2121,2180,2181,2601,3128,3306,33060,3380,3388,3389,3390,4100,4646,4848,4949,4444,5000,5280,5432,5632,5900,5984,6082,6379,6660-6669,7000-7077,7777,8000-8100,8443,8686,8649,8787,8800-8899,9000-9090,9200,9201,9300,9700,9797,9999,11211,16992,22222,27017,27018,27019,28017,33890-33899,13389,23389,50070,50075,65522,8161,61616,65534 --stylesheet {0} -iL {1} -oX {2}&".format(
        boot_url, url_file, out_file)
    print("[+] Start a quick scan\n {0}".format(cmd))
    subprocess.call(cmd, shell=True)


def scan_a(ips, out_file):
    cmd = "nohup sudo nmap -sV -T4 -Pn --open --stylesheet {0} {1} -oX {2}&".format(boot_url, ips, out_file)
    print("[+] Start scanning an ips, not full scan\n {0}".format(cmd))
    subprocess.call(cmd, shell=True)


def main():
    if len(argv) != 4:
        print("[-] python {0} <url_file> <out_file> mode".format(argv[0]))
        print("[E] python {0} url.txt test.xml all".format(argv[0]))
        print("[E] python {0} url.txt test.xml fast".format(argv[0]))
        print("[E] python {0} 1.1.1.1/24 test.xml scan".format(argv[0]))
        exit(1)

    mode, out_file = argv[3], output + argv[2]

    if mode == "all":
        scan_all(argv[1], out_file)
    elif mode == "fast":
        scan_fast(argv[1], out_file)
    elif mode == "scan":
        scan_a(argv[1], out_file)
    else:
        print("[x] mode is all or fast !")
        exit(1)


if __name__ == '__main__':
    main()
