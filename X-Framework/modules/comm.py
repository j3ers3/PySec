#!/usr/bin/env python
# encoding:utf-8
from core.mycolor import color

def ksf_line(module_name):
    ksf_1 = color.blue + color.bold + color.underl + "EXP" + color.end
    ksf_1 += ':' 
    ksf_1 += color.blue + color.bold + color.underl + module_name + color.end
    ksf_1 += ' > '
    ksf_1 += color.yellow
    return ksf_1


tag_true = color.blue + color.bold + "[+]" + color.end

def print_info(string):
    print color.bold + color.blue + string + color.end 

def print_err(string):
    print color.bold + color.red + string + color.end 

def show_op():
    print "" 
    print "Options\t\t Value\t\t\t Description" 
    print "-------\t\t---------------------\t-----------------" 

