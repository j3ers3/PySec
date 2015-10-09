#!/usr/bin/env python
#!encoding:utf-8
from core import mycolor

def ksf_line(module_name):
    ksf_1 = mycolor.color.blue + mycolor.color.bold + mycolor.color.underl + "WHOIS" + mycolor.color.end
    ksf_1 += ':' 
    ksf_1 += mycolor.color.blue + mycolor.color.bold + mycolor.color.underl + module_name + mycolor.color.end
    ksf_1 += ' > '
    return ksf_1


tag_true = mycolor.color.blue + mycolor.color.bold + "[+]" + mycolor.color.end

def print_info(string):
    print(mycolor.color.bold + mycolor.color.blue + string  + mycolor.color.end)

def print_err(string):
    print(mycolor.color.bold + mycolor.color.red + string + mycolor.color.end)

def show_op():
    print("")
    print("Options\t\t Value\t\t\t Description")
    print("-------\t\t---------------------\t-----------------")

