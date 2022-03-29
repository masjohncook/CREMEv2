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

expect "*:~# "
send "cd $path\r"

## install metasploit
#expect "$path# "
#send "sudo apt install curl -y\r"
#expect "$path# "
#send "curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall \r"
#expect "$path# "
#send "chmod +x msfinstall \r"
#expect "$path# "
#send "sudo ./msfinstall \r"

# Nmap instalation
expect "$path# "
send "apt install -y nmap \r"

# Metasploit instalation
expect "$path# "
send "apt update && apt upgrade -y \r"
## Java instalation
expect "$path# "
send "apt install openjdk-8-jdk \r"
expect "$path# "
send "apt install openjdk-8-jre \r"
expect "$path# "
send "echo 'JAVA_HOME=$(which java)' | sudo tee -a /etc/environment \r"
expect "$path# "
send "source /etc/environment \r"
expect "$path# "
send "echo $JAVA_JAVA_HOME" ## create checking logic for java home

## Dependencies instalation
expect "$path# "
send "apt install -y build-essential libreadline-dev libssl-dev libpq5 libpq-dev libreadline5 libsqlite3-dev libpcap-dev git-core autoconf postgresql pgadmin3 curl zlib1g-dev libxml2-dev libxslt1-dev libyaml-dev curl zlib1g-dev gawk bison libffi-dev libgdbm-dev libncurses5-dev libtool sqlite3 libgmp-dev gnupg2 dirmngr \r"

## Configure database postgresql for Metasploit
expect "$path# "
send "sudo -s \r"
expect "$path# "
send "su postgres \r"
expect "$path# "
send "createuser msf -P -S -R -D \r"
send "1234 \r"
send "1234 \r"
expect "$path# "
send "createdb -O msf msf \r"
expect "$path# "
send "exit \r"
expect "$path# "
send "exit \r"

## Ruby instalation
expect "$path# "
send "git clone https://github.com/rbenv/rbenv.git ~/.rbenv \r"
expect "$path# "
send "echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc \r""
expect "$path# "
send "echo 'eval "$(rbenv init -)"' >> ~/.bashrc \r"
expect "$path# "
send "source ~/.bashrc \r"
expect "$path# "
send "type rbenv \r"
expect "$path# "
send "git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build \r"
expect "$path# "
send "rbenv install $(rbenv install -l | grep -v - | tail -1) \r"
expect "$path# "
send "rbenv global $(rbenv install -l | grep -v - | tail -1) \r"
expect "$path# "
send "echo 'gem: --no-document' > ~/.gemrc"
expect "$path# "
send "gem install bundler \r"
expect "$path# "
send "gem env home \r"
expect "$path# "
send "rails -v \r"

## Metasploit installation
expect "$path# "
send "cd /opt \r"
expect "$path# "
send "sudo git clone https://github.com/rapid7/metasploit-framework.git \r"
expect "$path# "
send "cd metasploit-framework \r"
expect "$path# "
send "gem install bundler \r"
expect "$path# "
send "bundler install \r"
expect "$path# "
send "bash -c 'for MSF in $(ls msf*); do ln -s /opt/metasploit-framework/$MSF /usr/local/bin/$MSF;done' \r"

## Configure Postgresql
expect "$path# "
send "cp /opt/metasploit-framework/config/database.yml.example /opt/metasploit-framework/config/database.yml"
expect "$path# "
send "sed -i -e 's/database: metasploit_framework_development/database: msf/' /opt/metasploit-framework/config/database.yml \r"
expect "$path# "
send "sed -i -e 's/username: metasploit_framework_development/username: msf/' /opt/metasploit-framework/config/database.yml \r"
expect "$path# "
send "sed -i -e 's/password: __________________________________/password: 1234/' /opt/metasploit-framework/config/database.yml \r"
expect "$path# "
send "echo 'export PATH=$PATH:/usr/lib/postgresql/10/bin' >> ~/.bashrc \r"
expect "$path# "
send ". ~/.bashrc \r"

# install python 3.8
expect "$path# "
send "sudo add-apt-repository ppa:deadsnakes/ppa \r"
expect "to cancel adding it"
send "\r"
expect "$path# "
send "sudo apt update \r"
expect "$path# "
send "sudo apt install python3.8 -y \r"
expect "$path# "
send "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1 \r"
expect "$path# "
send "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 \r"
expect "$path# "
send "sudo apt install python3.8-distutils -y \r"
expect "$path# "
send "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \r"
expect "$path# "
send "python3.8 get-pip.py \r"

#expect "*:~# "
#send "sudo apt install python3-pip -y \r"
#expect "*:~# "
#send "sudo python3.8 -m easy_install pip \r"
#expect "*:~# "
#send "sudo apt remove python3-pip -y \r"
#expect "*:~# "
#send "sudo python3.8 -m easy_install pip \r"

# Pymetasploit (Py3)
expect "$path# "
send "python3.8 -m pip install --user pymetasploit3 \r"

expect "$path# "
send "exit\r"
