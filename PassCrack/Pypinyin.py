#!/usr/bin/env python
# encoding:utf8
import sys
import optparse
try:
	import pinyin
except:
	print "[x] pip install pinyin"
	exit(1)

__version__ = "0.5"
__prog__    = "Pypinyin"
__author__  = "whois"
__say__ = """
	汉字转为拼音的几种方式，如：
	张伟 
	全拼音 -> zhangwei
	首字母 -> zw
	名.姓  -> wei.zhang

"""

# output
def save_file(save_file, content):
	with open(save_file, 'a') as f:
		try:
			f.writelines(content + '\n')
		except:
			pass


# readfile
def name_list_fun(filename):
	name_list = []
	with open(filename, 'r') as f:
		for line in f.readlines():
			name_list.append(line.rstrip())
	return name_list


# 将姓名转化成首字母缩写
def szm_pinyin(name_list):
	
	for n in name_list:
		try:
			name = unicode(n, 'utf-8')  # 转换unicode
			szm = str(''.join([ pinyin.get(l, format="strip")[0] for l in list(name) ]))
			yield szm
		except Exception as e:
			yield None


# 将姓名转换为拼音
def xm_pinyin(name_list):

	for n in name_list:
		try:
			xm = pinyin.get(n, format="strip")
			yield xm
		except Exception as e:
			yield None


# 名.姓转化
def mx_pinyin(name_list):

	for n in name_list:
		try:
			name = unicode(n, 'utf-8') 
			pinyin_list = [ pinyin.get(l, format="strip") for l in list(name) ]
			mx = str(''.join(pinyin_list[1:])) + '.' + str(pinyin_list[0])
			yield mx
		except Exception as e:
			yield None


def main():

	parser = optparse.OptionParser(
		usage="Usage: {0} -f <filename> -o <output> -m mode".format(__prog__),
		version="%s: v%s (%s)" % (__prog__, __version__, __author__),
		epilog="""Ex: Pypinyin.py -f name.txt -o output.txt  -m 1
				  Ex: Pypinyin.py -f name.txt -m 1 | sort -rn | uniq > name_pinyin.txt""",
	)
	parser.add_option('-f', '--file', dest='filename', type='string',
		help='Dict file name')
	parser.add_option('-o', '--output', dest='output', type='string',
		help='Output file name')
	parser.add_option('-m', '--mode', dest='mode', type='int',
		help=u"""Specify mode : 
									1 => 全拼音模式 
									2 => 首字母缩写 
									3 => 名.姓""")	

	(options, args) = parser.parse_args()

	if options.filename == None  and options.mode == None:
		parser.print_help()
		sys.exit(0)

	name_list = name_list_fun(options.filename)

	if options.mode == 1:
		for p in xm_pinyin(name_list):
			if options.output:
				save_file(options.output, p)
			else:
				print p

	elif options.mode == 2:
		for p in szm_pinyin(name_list):
			if options.output:
				save_file(options.output, p)
			else:
				print p

	elif options.mode == 3:
		for p in mx_pinyin(name_list):
			if options.output:
				save_file(options.output, p)
			else:
				print p

	else:
		print '[x] Choose mode'

if __name__ == '__main__':
	main()
