#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set path [lindex $argv 4]
set target_server_ip [lindex $argv 5]

set timeout 600

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

#expect "*:~# "
#send "mkdir /usr/share/wordlists"
#expect "*:~# "
#send "echo 'admin\n123456\n12345\n123456789\npassword\niloveyou\nqwerty\n111111\n000000\niloveme\n987654321\nqsefthuk\n999999' >> /usr/share/wordlists/unix_password_modified.txt"
expect "*:~# "
send "python3 $path/02_step_PRE_NonMirai.py $path $ip $target_server_ip\r"

expect "*:~# "
send "exit\r"