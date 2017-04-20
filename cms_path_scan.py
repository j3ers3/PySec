#! encoding:utf-8
import os,sys
import Queue
import urllib2
import threading

#扫描CMS路径，将源代码下载到本地作为字典进行扫描
__author__ = 'kkk'
__date__ = '2015/10/10'

if len(sys.argv) != 2:
    print "\tCMS directory scan"
    print "[*] python {script} http://xxx.com/ CMS_PATH".format(script=sys.argv[0])

target = sys.argv[1]
my_filter = ['.jpg','png','.css','.gif']
directory = sys.argv[2]
if not os.path.exists(directory):
    print "[-] Not found directory!"
    exit(1)
threads = 10

os.chdir(directory)

#定义一个存放路径字典的队列
web_paths = Queue.Queue()

#将过滤掉后的路径存入web_paths
for r,d,f in os.walk('.'):
    for file in f:
	remote_path = "{path}/{file}".format(path=r,file=file)
	if remote_path.startswith('.'):
	    remote_path = remote_path[1:]
	if os.path.splitext(file)[1] not in my_filter:
	    web_paths.put(remote_path)

def scan():
    while not web_paths.empty():
	path = web_paths.get()
	url = "{target}/{path}".format(target=target, path=path)
	
	request = urllib2.Request(url)
	try:
	    response = urllib2.urlopen(request)
	    print "[{code}] => {path}".format(code=response.code, path=path)
	    response.close()
	except urllib2.HTTPError as error:
	    #print "%s is %s" % (path,error.code)
	    pass

def main():
    for i in range(threads):
        print "[*] Starting thread:{thread}".format(thread=i)
        t = threading.Thread(target=scan)
        t.start()

if __name__ == '__main__':
        main()    
