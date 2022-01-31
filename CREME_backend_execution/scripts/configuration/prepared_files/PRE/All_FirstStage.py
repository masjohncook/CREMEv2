import time, subprocess, os, sys
from nmap import nmap


def ip_scan():
    nbt = "nbtscan"
    nm = nmap.PortScanner()
    nm.scan('192.168.56.0/24', '0-65535')
    host_list = nm.all_hosts()
    print("====================List of Target====================")
    for x in host_list:
        state = nm[x].state()
        nbt_command = nbt+" -e " + x #+ " |awk '{print $2}'"
        nbt_scan = str(os.system(nbt_command))
        print(x + " : " + nbt_scan)
        # if nbt_scan == 0:
        #     print(x + " : " + state + " --> Netbios name was not discovered")
        # else:
        #     print(x + " : " + state + " -->" + str(nbt_scan))


def netbios_scan():
    print()


if __name__ == "__main__":
    ip_scan()