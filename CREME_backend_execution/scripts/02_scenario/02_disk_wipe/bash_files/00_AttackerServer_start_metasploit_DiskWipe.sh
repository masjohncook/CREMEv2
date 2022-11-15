#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]
set pids_file [lindex $argv 5]

set timeout 300

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

## Configure Postgresql
expect "$path# "
send "msfdb init\r"

#start MSFRPCD
expect "$path# "
send "msfrpcd -P kali -S\r"

expect "*:~# "
send "ps -ef | grep 'msfrpcd' | awk '{print \$2}' > $path/$pids_file\r"

expect "*:~# "
send "exit\r"
