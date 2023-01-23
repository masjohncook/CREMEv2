#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]
set target_server_ip [lindex $argv 5]

set timeout 1200

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

expect "*:~# "
<<<<<<<< HEAD:CREME_backend_execution/scripts/02_scenario/02_disk_wipe/bash_files/01_step_AttackerServer_DiskWipe.sh
send "python3 $path/01_step_DiskWipe.py $path $ip $target_server_ip\r"
========
send "python3 $path/01_DiskWipe_AllStep.py $path $ip $target_server_ip\r"
>>>>>>>> Dev/V2.5:CREME_backend_execution/scripts/02_scenario/02_disk_wipe/bash_files/01_DiskWipe_AllStep_AttackerServer.sh

expect "*:~# "
send "exit\r"