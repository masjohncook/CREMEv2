# CREME reproduction scanning
# I this step the attacker server try to perform nmap scan to the target server

import time
import sys
import os
from nmap import nmap


def record_timestamp(folder, output_time_file):
    time_output_file = os.path.join(folder, output_time_file)
    with open(time_output_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    if len(argv) != 4:
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))

    folder = argv[1]
    target_ip = argv[3]

    output_time_file = 'time_step_1_mirai_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(10)

    # put the attack launch command
    nm = nmap.PortScanner()
    nm.scan(hosts=target_ip, arguments='-O -A -p 0-65535')

    time.sleep(10)
    output_time_file = 'time_step_1_mirai_end.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(10)


main(sys.argv)
