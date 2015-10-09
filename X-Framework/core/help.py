#!/usr/bin/env python
#!encoding:utf-8

from core import mycolor

def help():

    print("\n")
    print(mycolor.color.blue + "Commands\t\tDescription" + mycolor.color.end)
    print(mycolor.color.green + "---------------\t\t--------------" + mycolor.color.end)
    print("set \t\t\tSet Value Of Options To Modules")
    print("run \t\t\tExecute Modules")
    print("exploit\t\t\tExecute Modules")
    print("use \t\t\tSelect  Module For Use")
    print("back\t\t\tExit Current Module")
    print("help\t\t\tShow Help Infomation")
    print("exit\t\t\tExit")
    print("!  \t\t\tRun Linux Commands(ex: ! ifconfig)")
    print("show modules\t\tShow Modules")
    print("show options\t\tShow Current Options Of Selected Module")
    print("")
