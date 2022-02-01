## CREME reproduction scanning
#  I this step the attacker server try to perform nmap scan to the target server

import time, subprocess, os, sys
from nmap import nmap


def ip_scan():
        nm = nmap.PortScanner()
        nm.scan('192.168.56.161/24', '0-65535')




if __name__ == "__main__":
    ip_scan()