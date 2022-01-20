import time, os, sys
from nmap import nmap

def ip_scan():
    nm = nmap.PortScanner('192.168.1.0/24')
    nm.all_hosts()


if __name__ == "__main__":
    ip_scan()

