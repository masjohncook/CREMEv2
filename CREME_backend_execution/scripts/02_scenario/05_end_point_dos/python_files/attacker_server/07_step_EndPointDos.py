import time
import sys
import os
import subprocess


def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    if len(argv) != 4:
        print("Usage: {} Folder local_ip target_ip".format(argv[0]))

    folder = argv[1]
    my_ip = argv[2]
    target_ip = argv[3]



    time.sleep(2)
    output_time_file_start = 'time_step_7_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    change_mode = 'chmod +x local_slowloris.py'
    launch_attack = 'timeout 60s ./local_slowloris &'
    subprocess.run(change_mode.split(), stdout=subprocess.PIPE)
    subprocess.run(launch_attack.split(), stdout=subprocess.PIPE)


    time.sleep(30)


main(sys.argv)
