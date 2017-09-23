#!/usr/bin/env python
# encoding:utf8
from os.path import exists
import optparse
import sys

__author__ = 'whois'
__prog__ = 'genpass'
__version__ = '0.2'
__date__ = '2016/1/1'

R = '\033[31m'	 # red
G = '\033[32m'	 # green
B = '\033[34m' 	 # blue
W = '\033[0m' 	 # white (normal)

""" 字典生成，攻击个人账号"""
"""  
	准备加入身份证
	优化字典 

"""

def banner():
	print G + '''
           _,---.       _,.---._          _ __       ,---.         ,-,--.     ,-,--.  
       _.='.'-,  \    ,-.' , -  `.     .-`.' ,`.   .--.'  \      ,-.'-  _\  ,-.'-  _\ 
      /==.'-     /   /==/_,  ,  - \   /==/, -   \  \==\-/\ \    /==/_ ,_.' /==/_ ,_.' 
     /==/ -   .-'   |==|   .=.     | |==| _ .=. |  /==/-|_\ |   \==\  \    \==\  \    
     |==|_   /_,-.  |==|_ : ;=:  - | |==| , '=',|  \==\,   - \   \==\ -\    \==\ -\   
     |==|  , \_.' ) |==| , '='     | |==|-  '..'   /==/ -   ,|   _\==\ ,\   _\==\ ,\  
     \==\-  ,    (   \==\ -    ,_ /  |==|,  |     /==/-  /\ - \ /==/\/ _ | /==/\/ _ | 
      /==/ _  ,  /    '.='. -   .'   /==/ - |     \==\ _.\=\.-' \==\ - , / \==\ - , / 
      `--`------'       `--`--''     `--`---'      `--`          `--`---'   `--`---' 
	[gopass -n xx-xx -b yy-yy-yy]
	  [sort uniq -->  good job]
	''' + W

def print_err(err):
	sys.exit(R + '[-] ' + err + W)

def main():
	
	number = ['00','000','001','111','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
	letter = []
	spe = ['!','@','#','$','%','^','&','*','!@#','!!']
	number += [n for n in range(22)]
	letter += [chr(l) for l in range(97,123)]
	
	parser = optparse.OptionParser(
		usage="Usage: genpass.py xxx",
		version="%s: v%s (%s)" % (__prog__, __version__, __author__),
		epilog="Example: genpass -n zhang-wei -b 1991-01-02  -m 138888888 -t all -o baidu -p top100.txt -w zhangwei.txt",
	)
	parser.add_option('-n','--name',dest='name',type='string',\
		help='Specify target name')
	parser.add_option('-b','--birth',dest='birth',type='string',\
		help='Specify target birthday')
	parser.add_option('-m','--mobile',dest='mobile',type='string',\
		help='Specify target mobile')
	parser.add_option('-w','--write',dest='save_f',type='string',\
		help='Specify save file')
	parser.add_option('-p','--pass',dest='pass_f',type='string',\
		help='Specify other password wordlist')
	parser.add_option('-t','--type',dest='type1',type='string',\
		help='[number, letter, spe, all]')
	parser.add_option('-o','--other',dest='other',type='string',\
		help='Specify Favorite things [Company,like]')

	(options, args) = parser.parse_args()
	
	name   = options.name
	birth  = options.birth
	mobile = options.mobile
	save_f = options.save_f
	pass_f = options.pass_f
	ty     = options.type1
	other  = options.other 

	if name == None and birth == None:
		print parser.print_help()
		print_err('Specify target name and birth,using --help')
		exit(1)
		
	name_list = name.split('-')

	xing = name_list[0]

	ming = ''.join(x for x in name_list[1:])

	xm = name.replace('-','')

	szm = ''.join(x[0] for x in name_list)

	xm2 = xing + ''.join(x[0] for x in name_list[1:]) 

	# zhang-wei => [zhang, wei, zhangwei, zhangw, zw]
	name_x = [xing,ming,xm,xm2,szm]

	birth_list = birth.split('-')

	year = birth_list[0]

	year2 = year + birth_list[1]

	mothday = ''.join(x for x in birth_list[1:])

	year3 = year[2:] + mothday

	nyr = birth.replace('-','')

	# 1990-01-22 => [1990, 199001, 900122, 0122, 19900122]
	birth_x = [year,year2,year3,mothday,nyr]
	
		
	#[dic_list.append(n) for n in name_x]
	dic_list = [n for n in name_x]
	dic_list += [n.upper() for n in name_x]
	dic_list += [b for b in birth_x]
	dic_list += [n+b for n in name_x for b in birth_x]
	dic_list += [b+n for n in name_x for b in birth_x]
	dic_list += [n.upper()+b for n in name_x for b in birth_x]
	dic_list += [b+n.upper() for n in name_x for b in birth_x]
	dic_list += [n+mobile for n in name_x if mobile]
	dic_list += [n.upper()+mobile for n in name_x if mobile]

	# 判断是否使用特殊字符
	if ty:
		# 在姓名后增加数字类
		if ty == 'number':
			[dic_list.append(n+str(nn)) for n in name_x for nn in number]
			[dic_list.append(str(nn)+n) for n in name_x for nn in number]
		# 在姓名后增加字母，默认全体小写字母
		elif ty == 'letter':
			[dic_list.append(n+l) for n in name_x for l in letter]
		# 在姓名后增加特殊符合
		elif ty == 'spe':
			[dic_list.append(n+s) for n in name_x for s in spe]
		# 全部使用
		elif ty == 'all':
			[dic_list.append(n+str(nn)) for n in name_x for nn in number]
			[dic_list.append(n+l) for n in name_x for l in letter]
			[dic_list.append(n+s) for n in name_x for s in spe]
		else:
			print_err('Type [number,letter,spe,all]')

	# 判断是否使用其他
	if other:
		dic_list += [n+str(other) for n in name_x]
		dic_list += [b+str(other) for b in birth_x]
		dic_list += [n+b+str(other) for n in name_x for b in birth_x]
		dic_list += [str(other)]

	# 判断是否使用弱密码					
	if pass_f:
		if exists(pass_f):
			with open(pass_f,'r') as f:
				other_list = [x.rstrip() for x in f.readlines() ]
				
			dic_list += other_list
			dic_list += [n+o for n in name_x for o in other_list]
			dic_list += [b+o for b in birth_x for o in other_list]
 		else:
 			print_err('File not found!')

	# 保存
	if save_f:
		with open(save_f,'w') as f:
			[f.writelines(x+'\n') for x in dic_list ]

	# 不保持就打印出来	
	else:
		for x in dic_list:
			print G + x
			
if __name__ == '__main__':
	banner()
	main()
