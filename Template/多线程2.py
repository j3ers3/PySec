# -*- coding:utf-8 -*-
 
import Queue
import threading
import time
import os
import sys
import urllib2
import string
 
#任务管理，管理任务列表、控制任务执行
class WorkManager(object):
    def __init__(self, work_lock, thread_num=0, func_job=0, argslist_job=[]):
        self.work_lock = work_lock
        self.work_queue = Queue.Queue() 
        self.__init_work_queue(func_job, argslist_job)
        self.thread_pool = []
        self.__init_thread_pool(thread_num)
 
    #初始化任务队列
    def __init_work_queue(self, func_job, argslist_job):
        for i in range(len(argslist_job)):
            self.add_job(func_job, argslist_job[i])
 
    #添加一项任务入队
    def add_job(self, func, args):
        self.work_queue.put((func, args)) #任务入队，Queue内部实现了同步机制
 
    #检查剩余队列任务
    def check_queue(self):
        return self.work_queue.qsize()
 
    #初始化线程池
    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.thread_pool.append(WorkThread(self.work_lock, self.work_queue))
 
    #开始运行线程池中所有线程
    def start_allwork(self):
        for item in self.thread_pool:
            if (item.isAlive() == False and item.isRuned == False):      
                item.start()
 
    #添加执行线程
    def add_thread(self, thread_num):
        for i in range(thread_num):
            self.thread_pool.append(WorkThread(self.work_lock, self.work_queue))
 
    #等待所有线程运行完毕 
    def wait_allcomplete(self):
        for item in self.thread_pool:
            if (item.isAlive() == True and item.isRuned == True):
                item.join()
 
    #清理线程池 
    def clear_thread_pool(self):
        count_del = 0
        for i in range(len(self.thread_pool)):
            if (self.thread_pool[i-count_del].isAlive() == False and self.thread_pool[i-count_del].isRuned == True):
                del self.thread_pool[i-count_del]
                count_del = count_del + 1
 
#任务线程，从任务队列中获取一个任务执行
class WorkThread(threading.Thread):
    def __init__(self, work_lock, work_queue):
        threading.Thread.__init__(self)
        self.work_lock = work_lock
        self.work_queue = work_queue
        self.isRuned = False
 
    #线程执行函数，取任务执行
    def run(self):
        self.isRuned = True
        while True:
            try:
                func, args = self.work_queue.get(block=False) #任务异步出队，Queue内部实现了同步机制
                func(self.work_lock, args) #执行任务函数
                self.work_queue.task_done() #通知系统任务完成，触发一个线程异常
            except Exception,e:
                #print str(e)
                if self.work_queue.qsize() == 0:
                    break #退出线程
                else:
                    self.work_lock.acquire()
                    print func, args, 'exception'
                    self.work_lock.release()
                    continue
 
#线程打印
def lock_print(work_lock, content):
    work_lock.acquire()
    print content
    work_lock.release()
 
#测试任务，参数：(线程锁, 参数列表)
def work_sleep(work_lock, arglist):
    lock_print(work_lock, arglist)
    time.sleep(1 * arglist)#模拟处理时间
    #print threading.current_thread(), list(args)
 
#下载函数
def work_down(work_lock, arglist): 
    url = arglist[0]
    path_downdir = arglist[1]
    if os.path.exists(path_downdir) == False:
        os.mkdir(path_downdir)
    filename = url[url.rfind('/')+1:]
    path_downfile = os.path.join(path_downdir, filename)
    while os.path.exists(path_downfile):
        filename = '+' + filename
        path_downfile = os.path.join(path_downdir, filename)
    response = urllib2.urlopen(url, timeout=300).read()
    file_down = open(path_downfile, 'wb+')
    file_down.write(response)
    file_down.close()
    #time.sleep(5)
    lock_print(work_lock, filename + ' ok!')   
 
#任务计划
def plan(work_lock, work_manager):
    #work_manager.add_job(work_sleep, 50)
    path_curdir = os.path.split(os.path.realpath(__file__))[0]
    path_urls = os.path.join(path_curdir, '\\urls.txt')
    path_downdir = os.path.join(path_curdir, '\\down')
    count_threads = 50
    if len(sys.argv) > 1:
        path_urls = sys.argv[1] 
    if len(sys.argv) > 2:
        path_downdir = sys.argv[2]    
    if os.path.exists(path_urls) == False:
        print 'file url list no exists.'
        return
    if os.path.exists(path_downdir) == False:
        print 'path down dir error.'
        return
    if len(sys.argv) > 3:
        count_threads = string.atoi(sys.argv[3])
    work_manager.add_thread(count_threads)
    file_urls = open(path_urls, 'rb')
    list_url = file_urls.readlines()
    file_urls.close()
    for i in range(len(list_url)):
        work_manager.add_job(work_down, [list_url[i].strip(), path_downdir])
 
#主程序
def main():
    work_lock = threading.RLock() #线程同步锁
    work_manager = WorkManager(work_lock) #任务管理
    plan(work_lock, work_manager) #任务安排
    work_manager.start_allwork() #开始工作
    work_manager.wait_allcomplete() #等待完成
 
if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print "cost all time: %s" % (end-start)
 