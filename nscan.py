import os
import sys
from platform import system
try:
    from terminaltables import DoubleTable
except:
    print "[-] Not found modules --  pip install terminaltables"
    sys.exit(1)

def scan(ip): 
    print "[+] Maping your network ..."
    scan = os.popen("nmap "+ip+" -n -sP ").read()
    output = "nmap-scan-ip.txt"

    with open(output,'w') as f:
        f.write(scan)

    devices = os.popen(" grep report " + output + " | gawk '{print $5}'").read()
    my_mac = os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | gawk '{print $2}' | cut -f1  -d'/'").read().upper() if system() != 'Windows' else 'Unknow' 
    devices_mac = os.popen("grep MAC "+ output + " | gawk '{print $3}'").read() + my_mac
    devices_name = os.popen("grep MAC " + output + " | gawk '{print $4 ,S$5 $6}'").read() + "\033[1;32m(This device)\033[1;m"
    
    table_data = [ 
        ['IP Address', 'Mac Address', 'Manufacturer'],
        [devices, devices_mac, devices_name]
    ]
    table = DoubleTable(table_data)

    print("\033[1;95m[+]===========[ Devices found on your network ]==========[+]\n\033[1;m")
    print(table.table)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print """
                +----------------------------------------+
                |                Map Your Network          |
                |                           by whois              |
                +----------------------------------------+
            """
        print "[*] Usage: python nscan.py ip/24"
        sys.exit(1)
    scan(sys.argv[1])
