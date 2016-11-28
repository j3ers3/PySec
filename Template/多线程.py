import Queue
from threading import Thread

q = Queue.Queue()

def do(x):
    pass

def worker():
    while not q.empty():
        do(q.get())

def main():

    threads_list = []
    threads = 20

    # start threads
    for i in range(threads):
        t = Thread(target=worker, args=())
        t.start()
        threads_list.append(t)

    # wait for all
    for i in range(threads):
        threads_list[i].join()

if __name__ == '__main__':
    main()