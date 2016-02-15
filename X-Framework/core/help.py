#!/usr/bin/env python
# encoding:utf-8

from core.mycolor import color

def help():

    print "\n" 
    print color.blue + "Commands\t\tDescription" + color.end 
    print color.green + "---------------\t\t--------------" + color.end 
    print "set \t\t\tSet Value Of Options To Modules" 
    print "run \t\t\tExecute Modules" 
    print "exploit\t\t\tExecute Modules" 
    print "use \t\t\tSelect  Module For Use" 
    print "back\t\t\tExit Current Module" 
    print "help\t\t\tShow Help Infomation" 
    print "exit\t\t\tExit" 
    print "!  \t\t\tRun Linux Commands(ex: ! ifconfig)" 
    print "show modules\t\tShow Modules" 
    print "show options\t\tShow Current Options Of Selected Module" 
    print "" 
