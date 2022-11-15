#!/usr/bin/expect -f
set delKnownHosts [lindex $argv 0]
set client_ip [lindex $argv 1]
set username [lindex $argv 2]
set password [lindex $argv 3]
set controller_ip [lindex $argv 4]
set controller_user [lindex $argv 5]
set controller_pass [lindex $argv 6]
set controller_path [lindex $argv 7]
set datalogger_ip [lindex $argv 8]
set rsyslog_file [lindex $argv 9]

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

# install and setting rsyslog client for syslog collection
expect "*:~# "
send "apt update && apt install rsyslog\r"
# download configured file from controller
expect "*:~# "
send "rm ~/.ssh/known_hosts\r"
expect "*:~# "
send "scp $controller_user@$controller_ip:$controller_path/CREMEv2/CREME_backend_execution/scripts/04_general/rsyslog_client/$rsyslog_file  /etc/rsyslog.conf\r"
set timeout 30
expect "*continue connecting (yes/no*)? "
send "yes\r"
expect " password: "
send "$controller_pass\r"
expect "*:~# "
send "sed -i \"s/dataloggerserver_ip/$datalogger_ip/g\" /etc/rsyslog.conf\r"
expect "*:~# "
send "systemctl restart rsyslog\r"

# configure Port Mirroring for Network Packets colection
expect "*:~# "
send "iptables -t mangle -D POSTROUTING -j TEE --gateway $datalogger_ip\r"
expect "*:~# "
send "iptables -t mangle -I POSTROUTING -j TEE --gateway $datalogger_ip\r"
# iptables-persistent
expect "*:~# "
send "DEBIAN_FRONTEND=noninteractive apt -y install iptables-persistent\r"
expect "*:~# "
send "iptables-save > /etc/iptables/rules.v4\r"

# install atop for accouting collection
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

# exit
expect "*:~# "
send "exit\r"
