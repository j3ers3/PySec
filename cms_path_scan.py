#!coding:utf-8
import os,sys
import Queue
import urllib2
import threading

#扫描CMS，博客等平台的路径，将源代码下载到本地作为字典进行扫描
print "\tCMS directory scan"
print "[*]./%s target threads" % sys.argv[0]

target = sys.argv[1]
my_filter = ['.jpg','png','.css','.gif']
directory = "/var/www/phpcmsv9"
threads = int(sys.argv[2])

os.chdir(directory)

#定义一个存放路径字典的队列
web_paths = Queue.Queue()

#将过滤掉后的路径存入web_paths
for r,d,f in os.walk('.'):
    for files in f:
	remote_path = "%s/%s" % (r,files)
	if remote_path.startswith('.'):
	    remote_path = remote_path[1:]
	if os.path.splitext(files)[1] not in my_filter:
	    web_paths.put(remote_path)

def scan():
    while not web_paths.empty():
	path = web_paths.get()
	url = "%s%s" % (target, path)
	
	request = urllib2.Request(url)
	try:
	    response = urllib2.urlopen(request)
	    print "[%d] => %s" % (response.code, path)
	    response.close()
	except urllib2.HTTPError as error:
	    #print "%s is %s" % (path,error.code)
	    pass

for i in range(threads):
    print "[*] Starting thread:%d" %i
    t = threading.Thread(target=scan)
    t.start()

    
