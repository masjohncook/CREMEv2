#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set dataLoggerServer [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]

set timeout 1200

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"

spawn ssh $username@$dataLoggerServer
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"
set timeout 60

## update time
expect "*:~# "
send "timedatectl set-timezone Asia/Taipei\r"
set timeout 60

expect "*:~# "
send "exit\r"
