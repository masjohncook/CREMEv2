#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set dataLoggerServer [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set controller_ip [lindex $argv 4]
set controller_user [lindex $argv 5]
set controller_pass [lindex $argv 6]
set controller_path [lindex $argv 7]

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

# install and configure rsyslog remote for syslog collection
expect "*:~# "
send "apt update && apt install -y rsyslog\r"
expect "*:~# "
send "rm ~/.ssh/known_hosts\r"
expect "*:~# "
send "scp $controller_user@$controller_ip:$controller_path/CREMEv2/CREME_backend_execution/scripts/04_general/rsyslog_server/rsyslog.conf /etc/\r"
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$controller_pass\r"
set timeout 60
expect "*:~# "
send "systemctl restart rsyslog\r"

# install tcpdump for Network Packets colection
expect "*:~# "
send "apt update && apt -y install tcpdump\r"

# install atop to process atop data from other machines
# expect "*:~# "
# send "apt update && apt install atop\r"
expect "*:~# "
send "rm ~/.ssh/known_hosts\r"
expect "*:~# "
send "scp $controller_user@$controller_ip:$controller_path/CREMEv2/CREME_backend_execution/scripts/04_general/atop-1.26_modified.tar.gz /root\r"
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$controller_pass\r"
set timeout 30
expect "*:~# "
send "apt remove --purge atop -y\r"
expect "*:~# "
send "apt install -y libz-dev libncurses5-dev zlib1g libncurses5 gcc make\r"
expect "*:~# "
send "tar -xzvf atop-1.26_modified.tar.gz\r"
expect "*:~# "
send "cd atop-1.26\r"
expect "*atop-1.26# "
send "make install\r"
expect "*atop-1.26# "
send "cd\r"


## update time
expect "*:~# "
send "timedatectl set-timezone Asia/Taipei\r"
set timeout 60

expect "*:~# "
send "exit\r"
