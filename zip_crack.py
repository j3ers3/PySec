#!/usr/bin/env python

import zipfile
import optparse
import sys

def crack(zFile,passwd):
    
    try:
        zFile.extractall(pwd=passwd)
        print("[+] Password is " + passwd)
        sys.exit(1)
    except:pass

def main():

    parser = optparse.OptionParser("usage%prog " +
            "-f <zipfile> -d <dictionary> -v <verbose>")
    parser.add_option('-f','--file',dest='zname',type='string',
            help='specify zip file')
    parser.add_option('-d','--dict',dest='dname',
            type='string',help='specify dictionary file')
    parser.add_option('-v','--verbose',dest='verbose',
            action='store_true',
            default=False,help='show verbose')

    (options, args) = parser.parse_args()

    if (options.zname == None) and (options.dname == None):
        print(parser.print_help())
        exit(0)

    zFile = zipfile.ZipFile(options.zname)

    with open(options.dname,'r') as f:
        for passwd in f.readlines():
            passwd = passwd.rstrip()
            if options.verbose:
                print("[*] Try :" + passwd)
            
            crack(zFile,passwd)            

if __name__ == '__main__':
    main()
