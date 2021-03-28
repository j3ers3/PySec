# encoding:utf8
import socket
import struct
import argparse
import asyncio
from netaddr import IPNetwork

pkt = b'\x00\x00\x00\xc0\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x00\x08\x00\x01\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x00\x00\x00\x02\x00\x00\x00\x02\x02\x10\x02"\x02$\x02\x00\x03\x02\x03\x10\x03\x11\x03\x00\x00\x00\x00\x01\x00&\x00\x00\x00\x00\x00\x01\x00 \x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\n\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'

red = '\033[31m'
blue = '\033[94m'
end = '\033[0m'

def banner():
    print(red + """

███████╗███╗   ███╗██████╗  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
██╔════╝████╗ ████║██╔══██╗██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
███████╗██╔████╔██║██████╔╝██║  ███╗███████║██║   ██║███████╗   ██║   
╚════██║██║╚██╔╝██║██╔══██╗██║   ██║██╔══██║██║   ██║╚════██║   ██║   
███████║██║ ╚═╝ ██║██████╔╝╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
╚══════╝╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝ """ + blue + """
                
                                                         by whois\n""" + end)

count = 0

async def connet(ip, sem):
    global count

    async with sem:
        try:
            fut = asyncio.open_connection(ip, 445)
            reader, writer = await asyncio.wait_for(fut, timeout=3)
            writer.write(pkt)
            await writer.drain()
            size, = struct.unpack(">I", (await reader.read(4)))
            ret = await reader.read(size)

            if ret[68:70] != b"\x11\x03" or ret[70:72] != b"\x02\x00":
                print("[-] {} Not vul".format(ip))
            else:
                print("[+] " + ip + red + " Vulnerable!!" + end)
                count += 1

        except Exception as e:
            #print(e)
            pass


async def scan(ips, t):
    sem = asyncio.Semaphore(t)

    tasks = []
    ips = [str(ip) for ip in IPNetwork(ips)]
    for ip in ips:
        tasks.append(asyncio.create_task(connet(ip, sem)))
    await asyncio.wait(tasks)


async def scan_file(myfile, t):
    tasks = []
    ips = []
    sem = asyncio.Semaphore(t)

    with open(myfile, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            ips.append(line)

    for ip in ips:
        tasks.append(asyncio.create_task(connet(ip, sem)))
    await asyncio.wait(tasks)


def main():

    parser = argparse.ArgumentParser(
        usage='smbghost -i 1.1.1.1/24',
        description="SMBGhost Check",
    )

    parser.add_argument("-i", dest="ips",
                        help="Use ip segment")
    parser.add_argument("-f", dest="file",
                        help="Use ip file")
    parser.add_argument("-t", dest="threads", type=int, default=60,
                        help="Set thread (default 60)")

    args = parser.parse_args()

    if args.ips is None and args.file is None:
        #banner()
        print("[x] smbghost.py -h")
        exit(0)

    if args.ips:
        asyncio.run(scan(args.ips, args.threads))

    if args.file:
        asyncio.run(scan_file(args.file, args.threads))

    print("\n总共发现 {0} 个存在CVE-2020-0796漏洞".format(count))


if __name__ == '__main__':
    banner()
    main()