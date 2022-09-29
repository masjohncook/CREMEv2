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
set timeout 30

## Configure Postgresql
expect "$path# "
send "msfdb init"
set timeout 30

#start MSFRPCD
expect "$path# "
send "msfrpcd -P kali -S"
set timeout 30

# Pymetasploit (Py3)
expect "$path# "
send "pip install --user pymetasploit3 \r"
set timeout 30

expect "$path# "
send "exit\r"
