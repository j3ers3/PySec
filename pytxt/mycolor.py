#!/usr/bin/env python
# encoding:utf-8

""" Color 
    from mycolor import color
    print color.purple + "[+]" + color.end
""" 

class color:
    
    purple   = '\033[95m' 
    cyan     = '\033[96m' 
    darkcyan = '\033[36m' 
    blue     = '\033[94m' 
    green    = '\033[92m'
    yellow   = '\033[93m'
    red	= '\033[91m'

    bold     = '\033[1m'  
    underl   = '\033[4m'  
    end      = '\033[0m'  
    
    backBlack   = '\033[40m' 
    backRed     = '\033[41m'
    backGreen   = '\033[42m'
    backYellow  = '\033[43m'
    backBlue    = '\033[44m'
    backMagenta = '\033[45m' 
    backCyan    = '\033[46m'
    backWhite   = '\033[47m'
