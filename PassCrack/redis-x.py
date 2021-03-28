#!/usr/bin/env python
# encoding:utf8
from threading import Thread
import optparse
import socket
import Queue
import sys

# 🔧 Redis综合利用工具 
__prog__ = 'x-redis'
__author__ = 'whois'
__version__ = 'v0.1'
__update__ = '2020/08/04'

purp = '\033[95m'
blue = '\033[94m'
red = '\033[31m'
yellow = '\033[93m'
end = '\033[0m'

def banner():
    return red + """
██████╗ ███████╗██████╗ ██╗███████╗
██╔══██╗██╔════╝██╔══██╗██║██╔════╝
██████╔╝█████╗  ██║  ██║██║███████╗
██╔══██╗██╔══╝  ██║  ██║██║╚════██║
██║  ██║███████╗██████╔╝██║███████║
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚══════╝
                        
                    """ + yellow + "by {0} {1}\n".format(__author__, __version__) + end


def redis_check(ip, port=6379):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(3)

        s.connect((str(ip), int(port)))

        # 发送info语句
        s.send("INFO\r\n")

        result = s.recv(1024)

        # 未授权测试
        if "redis_version" in result:
            print(purp + "[+] {0}:{1} -> 未授权访问".format(ip, port) + end)

        # 简单弱口令检测
        elif "Authentication" in result:
            pass_list = ['123456', '1234567', '12345678', '123', 'pass', 'password', 'admin', 'redis', 'redis1',
                         'Redis', 'redis01!', 'redis!', 'redis_pass', 'redis_best', 'root', 'abc123', 'redis123', 'redis000',
                         'redis_password', '111111', '888888', '666666', 'pass123', '12345', '1234', '000', 'specialpassword', 'abc12345', 'abc12345']

            for p in pass_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                s.send("AUTH {0}\r\n".format(p))

                result = s.recv(1024)

                if "OK" in result:
                    print(blue + "[+] {0}:{1} -> 弱口令：{2}".format(ip, port, p) + end)
        else:
            pass

        s.close()

    except Exception as e:
        #print(e)
        pass


def main():
    print(banner())
    parser = optparse.OptionParser(
        usage="Usage: %prog [options]",
        version="{0}: v{1} ({2})".format(__prog__, __version__, __author__),
        epilog="""[#] All Check: python x-redis.py -f url.txt\t\t\t
                  [#] Crack Single Target: python x-redis.py -i ip -a pass_file.txt -t threads""",
    )

    parser.add_option("-f", "--file", dest="file",
                      help="Target file")
    parser.add_option("-i", "--ip", dest="ip",
                      help="Single Target")
    parser.add_option("-p", "--port", dest="port",
                      help="Specify Port")
    parser.add_option("-a", "--auth", dest="auth",
                      help="Specify Password file")
    parser.add_option("-t", "--threads", dest="threads", type='int',
                      help="Specify threads default 8")

    (options, args) = parser.parse_args()

    ip = options.ip
    port = options.port

    if options.file == None and options.ip == None:
        parser.print_help()
        exit(1)

    if options.file:
        with open(options.file) as f:
            for line in f.readlines():
                try:
                    redis_check(line.strip().split(":")[0], line.strip().split(":")[1])
                except:
                    redis_check(line.strip())

    elif options.ip:
        pass

    else:
        print("x")


if __name__ == '__main__':
    main()
