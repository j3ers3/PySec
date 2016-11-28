#!/usr/bin/env python
#!encoding:utf8
import requests

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04',
    'Cookie':'ok',
    'X-Forwarded-For':'60.216.8.147'        #$_SERVER['HTTP_X_FORWARDED_FOR'] ip1,ip2
}
timeout = 15
proxy = {'http':'http://124.250.236.26:80'}   #$_SERVER['REMOTE_ADDR']
