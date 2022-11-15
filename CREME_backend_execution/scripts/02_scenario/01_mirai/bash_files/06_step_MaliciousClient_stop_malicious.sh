#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]
set pids_file [lindex $argv 5]
#set pids_file "pids_file.txt"
set logs_path [lindex $argv 6]
set outputTime [lindex $argv 7]

set timeout 600

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

# Record time
set DATE [exec date +%s]
set outputTimeFile [open $logs_path/$outputTime "w+"]
puts $outputTimeFile $DATE
close $outputTimeFile

set timeout 300

# Stop pids
expect "*:~# "
send "tmppid=\$(sed -n -e 1p $path/$pids_file)\r"
expect "*:~# "
send "tmpname=\$(ps -o cmd= \$tmppid)\r"
expect "*:~# "
send "tmpname=\$(echo \$tmpname | awk '{print \$1;}')\r"
expect "*:~# "
send "pkill -f \$tmpname\r"

expect "*:~# "
send "exit\r"
