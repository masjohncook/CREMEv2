#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]


set timeout 1200

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"
set timeout 60

expect "*:~# "
send "cd $path\r"

## Configure Postgresql
expect "$path# "
send "sudo systemctl start postgresql.service"

# Pymetasploit (Py3)
expect "$path# "
send "pip install --user pymetasploit3 \r"

expect "$path# "
send "exit\r"
