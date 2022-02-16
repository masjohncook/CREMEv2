## CREME reproduction scanning
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

    output_time_file = 'time_step_1_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)
    nm = nmap.PortScanner()
    nm.scan(target_ip)


    # put the attack launch command

    while client.jobs.list:
        time.sleep(1)


    time.sleep(10)
    output_time_file = 'time_step_1_end.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)


main(sys.argv)