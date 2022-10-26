#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]


set timeout 900

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

expect "*:~# "
send "cd $path\r"

### Configure Postgresql
#expect "$path# "
#send "msfdb init \r"
#set timeout 30
#
##start MSFRPCD
#expect "$path# "
#send "msfrpcd -P kali -S \r"
#set timeout 30

# install pip3
expect "$path# "
send "sudo apt install -y python3-pip \r"

# Pymetasploit (Py3)
expect "$path# "
send "pip install --user pymetasploit3 \r"

# install python-nmap
expect "$path# "
send "pip install --user python-nmap \r"

expect "$path# "
send "exit\r"
