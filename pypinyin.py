#!/usr/bin/env python
# encoding:utf8
try:
	import pinyin
except:
	print "[-] pip install pinyin"
	exit(1)
import sys
import optparse

__version__ = "0.4"
__prog__    = "pypinyin"
__author__  = "whois"

# 将姓名转化成首字母缩写
def szm_pinyin(filename, newfile):
	
	with open(filename,'r') as f:
		for n in f.readlines():
			try:
				name = unicode(n.rstrip(),'utf-8')  # 转换unicode
				szm = ''.join([ pinyin.get(l, format="strip")[0] for l in list(name) ])
			
				with open(newfile,'a') as ff:
					ff.writelines(szm + '\n')
			except:
				pass

# 将姓名转换为拼音
def xm_pinyin(filename, newfile):
	
	with open(filename,'r') as f:
		for n in f.readlines():
			try:
				name = pinyin.get(n.rstrip(), format="strip")

				with open(newfile,'a') as ff:
					ff.writelines(name+'\n')
			except:
				pass

def main():

	parser = optparse.OptionParser(
		usage="Usage: pypinyin.py -f <filename> -w <output> -m mode",
		version="%s: v%s (%s)" % (__prog__, __version__, __author__),
		epilog="Example: pypinyin.py -f name.txt -w output.txt  -m 1",
	)
	parser.add_option('-f','--file',dest='filename',type='string',
		help='Dict file name')
	parser.add_option('-w','--save',dest='savefile',type='string',
		help='Output file name')
	parser.add_option('-m','--mode',dest='mode',type='int',
		help='Specify mode : 1 => pinyin | 2 => szm pinyin')	

	(options, args) = parser.parse_args()

	if options.filename == None and options.savefile == None and options.mode == None:
		parser.print_help()
		sys.exit(0)
	if options.mode == 1:
		xm_pinyin(options.filename, options.savefile)
	elif options.mode == 2:
		szm_pinyin(options.filename, options.savefile)
	else:
		print '[-] Choose mode 1 or 2'

if __name__ == '__main__':
	main()
