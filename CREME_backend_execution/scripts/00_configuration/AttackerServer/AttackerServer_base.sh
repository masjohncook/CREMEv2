#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set controller_ip [lindex $argv 4]
set controller_user [lindex $argv 5]
set controller_pass [lindex $argv 6]
set controller_path [lindex $argv 7]
set server_ip [lindex $argv 8]

set timeout 1200

# SSH connection
spawn /bin/bash $delKnownHosts
send "exit\r"
spawn ssh $username@$ip
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$password\r"

## update time
expect "*:~# "
send "timedatectl set-timezone Asia/Taipei\r"
set timeout 60

# config new dns
expect "*:~# "
send "rm ~/.ssh/known_hosts\r"
expect "*:~# "
send "scp -r $controller_user@$controller_ip:$controller_path/CREMEv2/CREME_backend_execution/scripts/00_configuration/BenignClient/ConfigureFiles/resolv.conf  /etc\r"
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$controller_pass\r"
# add executable permission
expect "*:~# "
send "chmod +x /etc/resolv.conf\r"
expect "*:~# "
send "sed -i \"s/my_dns_1/$server_ip/g\" /etc/resolv.conf\r"

expect "*:~# "
send "exit\r"
