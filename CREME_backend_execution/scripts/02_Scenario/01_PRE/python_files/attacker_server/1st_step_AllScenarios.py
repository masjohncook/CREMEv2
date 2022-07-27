## CREME reproduction scanning
#  I this step the attacker server try to perform nmap scan to the target server

import time, subprocess, os, sys
from nmap import nmap

def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())



def main(argv):
    # put the configuration

    output_time_file = 'time_stage_1_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)
    # print('Start 1')

    # put the attack launch command

    while client.jobs.list:
        time.sleep(1)


    time.sleep(10)
    output_time_file = 'time_stage_1_end.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)


main(sys.argv)