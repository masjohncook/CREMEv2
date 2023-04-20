# CREME reproduction scanning
#  I this step the attacker server try to perform nmap scan to the target server

import time
import sys
import os
from nmap import nmap


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]

    output_time_file_start = 'time_step_1_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)
    # put the attack launch command
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target_ip, arguments='-O -A -p 0-65535')

    except Exception as e:
        print(e)
        pass
    
    time.sleep(60)
    output_time_file_end = 'time_step_1_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(60)


main(sys.argv)
