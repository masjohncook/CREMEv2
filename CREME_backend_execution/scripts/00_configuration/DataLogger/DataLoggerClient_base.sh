#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set client_ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]

set timeout 1200

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"

spawn ssh $username@$client_ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"
set timeout 60

## update time
expect "*:~# "
send "timedatectl set-timezone Asia/Taipei\r"
set timeout 60


# exit
expect "*:~# "
send "exit\r"
