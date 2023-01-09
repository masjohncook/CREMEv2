import time
import sys
import os
import subprocess


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]

    # print(client.sessions.list['4'])
    time.sleep(60)
    
    output_time_file_end = 'time_step_6_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)

    time.sleep(2)
    output_time_file_start = 'time_step_7_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(60)

    change_mode = 'chmod +x local_slowloris.py'
    launch_attack = 'timeout 60s ./local_slowloris &'
    subprocess.run(change_mode.split(), stdout=subprocess.PIPE)
    subprocess.run(launch_attack.split(), stdout=subprocess.PIPE)


    time.sleep(60)


main(sys.argv)
