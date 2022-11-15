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

set timeout 600

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$CNC_ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

# Record time
set DATE [exec date +%s]
set outputTimeFile [open $logs_path/$outputTime "w+"]
puts $outputTimeFile $DATE
close $outputTimeFile

set timeout 120

expect "*:~# "
send "cat $path/$finishedPhaseFile\r"

set flag 0
while {$flag<1} {
      expect "True"
      incr flag

      send "cat $path/$finishedPhaseFile\r"
      sleep 1
}
set timeout 120

expect "*:~# "
send "exit\r"
