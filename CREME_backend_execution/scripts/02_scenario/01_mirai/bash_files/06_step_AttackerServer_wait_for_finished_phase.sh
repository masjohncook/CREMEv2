#!/usr/bin/expect -f
# run at controller to wait until specific phase finished
set delKnownHosts [lindex $argv 0]
set CNC_ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]
set finishedPhaseFile [lindex $argv 5]
set logs_path [lindex $argv 6]
set outputTime [lindex $argv 7]
set flag 0

set timeout 10

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$CNC_ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"
set timeout 60

# Record time
set DATE [exec date +%s]
set outputTimeFile [open $logs_path/$outputTime "w+"]
puts $outputTimeFile $DATE
close $outputTimeFile

expect "*:~# "
send "cat $path/$finishedPhaseFile\r"

flag=0
while [ $flag -lt 1 ]
do
expect "True"
incr flag

send "cat $path/$finishedPhaseFile\r"
sleep 1
done

expect "*:~# "
send "exit\r"
