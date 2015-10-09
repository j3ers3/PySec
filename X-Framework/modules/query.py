#!/usr/bin/env python
#!encoding:utf-8
# 利用接口进行查询 http://www.haoservice.com
# create 15/8/26

import requests
from comm import *

options = ['2015-8-26','上海','北京']
options1 = ['114.114.114.114','']

class MyTools(object):
	
    def __init__(self):
	self.api_tr  = 'ca1d05bfbb594d598b53622bfd2431fa'
	self.api_ip  = 'ec914171d8b240da8bfca81a87fc40af'
	self.url     = 'http://apis.haoservice.com'
	self.train   = '/lifeservice/train/ypcx'
	self.ip      = '/getLocationbyip'

    def query_12306(self):
	self.full_url = self.url + self.train
	self.payload = {
			    'date':options[0],
			    'from':options[1],
			    'to'  :options[2],
			    'key' :self.api_tr	
		       }
	ksf_1 = ksf_line("Tools 12306")
	com  = raw_input(ksf_1)
	try:
	    if com[0:8] == 'set DATE':
		date = com[9:]
		options[0] = date
		print(tag_true + "set DATE --> " + options[0])
		MyTools().query_12306()
	    elif com[0:8] == 'set FROM':
		from1 = com[9:]
		options[1] = from1
		print(tag_true + "set FROM --> " + options[1])
		MyTools().query_12306()
	    elif com[0:6] == 'set TO':
		to = com[7:]
		options[2] = to
		print(tag_true + "set TO --> " + options[2])
		MyTools().query_12306()
	    elif com[0:12] == 'show options':
		show_op()
		print("DATE\t\t" + options[0] + "\t\t 出发日期" )
		print("FROM\t\t" + options[1] + "\t\t\t 出发站")
		print("TO\t\t"   + options[2] + "\t\t\t 到达站")
		MyTools().query_12306()
	    elif com[0:4] == 'back':
		pass
	    elif com[0:3] == 'run':
		try:
		    r = requests.get(self.full_url,params=self.payload)
		except:
		    print_err('requests is err')
		result = eval(r.content)
		res_list = result['result']
		for x in res_list:
		    print(x['from_station_name'] + ' --> ' + x['to_station_name'] + ' 车次:' + x['train_no'] + ' 类型:' + x['train_class_name'] + ' 出发时间:' + x['start_time'] + ' 到达时间:' + x['arrive_time'] + ' 历时:' + x['lishi']+ ' 硬卧:' + x['yw_num'] + ' 硬座:' + x['yz_num'])
		MyTools().query_12306()
	    else:
		MyTools().query_12306()
	except:
	    print_err("Error,System Exit...")

# ip定位--------------------------------------------
    def loc_ip(self):
	full_url = self.url + self.ip
	null	 = "not found"
	payload  = {
			'ip' :options1[0],
			'key':self.api_ip
		    }
	ksf_1 = ksf_line("Tools IP")
	com   = raw_input(ksf_1)
	if com[0:6] == 'set IP':
	    options1[0] = com[7:]
	    print(tag_true + "set IP --> " + options1[0])
	    MyTools().loc_ip()
	elif com[0:10] == 'set DOMAIN':
	    options1[1] = com[11:]
	    print(tag_true + "set DOMAIN --> " + options1[1])
	    MyTools().loc_ip()
	elif com[0:12] == 'show options':
	    show_op()
	    print("IP\t\t" + options1[0] + "\t\t\t IP地址" )
	    print("DOMAIN\t\t" + options1[1] + "\t\t\t 域名地址")
	    MyTools().loc_ip()
	elif com[0:3] == 'run':
	    if options1[1] != '':
		from socket import gethostbyname
		options1[0] = gethostbyname(options1[1])
	    try:		
		r = requests.get(full_url,params=payload)
	    except:
		print('error')
	    
	    result   = eval(r.content)
	    res_dic = result['result']
	    if res_dic == 'not found':
		print_err("[-]国外ip无法定位")	
		MyTools().loc_ip()
	    print(tag_true + "IP:" + res_dic['IP'] + " 地址:" + res_dic['address'] + " 详细地址:" + res_dic['district'] + ' '+ res_dic['street'] + " 简要地址:" + res_dic['simpleaddress'] + ' ' + res_dic['city']) 
	    print(tag_true + "经纬度：" + str(res_dic['baidu_lng']) + "  " + str(res_dic['baidu_lat']))
	    MyTools().loc_ip()
	elif com[0:4] == 'back':
	    pass
	elif com[0:4] == 'exit':
	    exit(0)
	else:
	    MyTools().loc_ip()
