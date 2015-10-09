#!/usr/bin/env python
#!encoding:utf-8
''' 指定目录进行打包,支持tar，gzip,bzip2 '''

import os,sys
import tarfile

if len(sys.argv) != 3:
    print "*" * 50
    print "[*] Usage: " + sys.argv[0] + " [tar/gz/bz2] [files/dirs]"
    exit(1)

my_dirs  = sys.argv[2]
my_type  = sys.argv[1]

if not os.path.isfile(my_dirs) and not os.path.isdir(my_dirs):
    print "[-] File or Dirs not Found !!"
    exit(1)

if my_type not in ['tar','gz','bz2']:
    print "[-] Type is not found!"
    exit(1)

if my_type == 'tar':
    tar_dirs = os.path.basename(my_dirs) + '.' + my_type
    tar = tarfile.open(tar_dirs,'w')
else:
    tar_dirs = os.path.basename(my_dirs) + '.tar.' + my_type
    tar = tarfile.open(tar_dirs,'w|' + my_type)

for root, dirs, files in os.walk(my_dirs):
    for f in files:
	tar.add(os.path.join(root,f))

tar.close()

print "[+] Succeed, ----> " + tar_dirs
before = os.popen('ls -lh ' + my_dirs ).read().split()[1]
after  = os.popen('ls -lh ' + tar_dirs).read().split()[4]
print "[+] " + before + ' \t---> ' + after
