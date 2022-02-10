# This step is the step tried to reach public facing application through password guessing/cracking
# The password guessing in performed on the vulneratble and non vulnerable client for 02_mirai scenarion and target server for other scenario

import time, subprocess, os, sys



def record_timestamp(folder, output_time_file):
    output_time_file = os.path.join(folder, output_time_file)
    with open(output_time_file, "w+") as fw:
        fw.write('%f' % time.time())


def main(argv):
    # put the configuration

    output_time_file = 'time_stage_1_start.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)
    # print('Start 1')

    # put the attack launch command

    while client.jobs.list:
        time.sleep(1)

    time.sleep(10)
    output_time_file = 'time_stage_1_end.txt'
    record_timestamp(folder, output_time_file)
    time.sleep(2)


main(sys.argv)