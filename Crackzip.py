#!/usr/bin/env python
# encoding:utf8
import zipfile
import optparse
import sys

__prog__ = 'Crackzip'
__author__ = 'whois'
__version__ = '1.0'

def banner():
    print """
_______                       __           .__        
\_   ___ \____________    ____ |  | _________|__|_____  
/    \  \/\_  __ \__  \ _/ ___\|  |/ /\___   /  \____ \ 
\     \____|  | \// __ \\  \___|    <  /    /|  |  |_> >
 \______  /|__|  (____  /\___  >__|_ \/_____ \__|   __/ 
        \/            \/     \/     \/      \/  |__| \n"""

def crack(zFile, passwd):
    
    try:
        zFile.extractall(pwd=passwd)
        print("\n[+] Password is " + passwd)
        exit(1)
    except Exception as err:
        pass

def main():

    parser = optparse.OptionParser(
            usage="%prog -f <zipfile> -d <dictionary>",
            version="%s: v%s (%s)" % (__prog__, __version__, __author__),
            epilog="Example: Crackzip -f test.zip -d dic.txt"
        )

    parser.add_option('-f', '--file', dest='zname', type='string',
            help='specify zip file')
    parser.add_option('-d', '--dict', dest='dname',
            type='string',help='specify dictionary file')

    (options, args) = parser.parse_args()

    if (options.zname == None) and (options.dname == None):
        print "[x] Please use -h to see help"
        exit(0)

    zFile = zipfile.ZipFile(options.zname)

    with open(options.dname, 'r') as f:
        for passwd in f.readlines():
            passwd = passwd.rstrip()
            sys.stdout.write('\r{0} '.format(passwd))
            
            crack(zFile,passwd)            

if __name__ == '__main__':
    banner()
    main()
