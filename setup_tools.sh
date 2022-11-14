#!/bin/bash

sudo apt update
sudo apt install expect -y
sudo apt install python3-pip -y
sudo apt install python-is-python3
# virtual environment
sudo apt install python3-venv -y

# install ssh server
sudo apt install openssh-server -y

# install atop
sudo apt remove --purge atop -y
sudo apt install -y libz-dev libncurses5-dev zlib1g libncurses5 gcc make
cd ~/
tar xvzf CREMEv2/CREME_backend_execution/scripts/04_general/atop-1.26_modified.tar.gz
cd atop-1.26
sudo make install
cd -


# install argus-serer and argus-client
#wget http://qosient.com/argus/src/argus-3.0.8.2.tar.gz
#wget http://qosient.com/argus/src/argus-clients-3.0.8.2.tar.gz
#
#tar -xvzf argus-3.0.8.2.tar.gz
#tar -xvzf argus-clients-3.0.8.2.tar.gz

sudo apt update
sudo apt install flex -y
sudo apt install bison -y
sudo apt install libpcap-dev -y
sudo apt install tmux -y
sudo apt install sshpass -y
sudo apt install argus-client argus-server -y
sudo spt install nmap

#cd argus-3.0.8.2
#chmod +x configure
#./configure
#sudo make install
#
#cd -
#
#cd argus-clients-3.0.8.2
#chmod +x configure
#./configure
#sudo make install

#install redis
cd ~/
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make MALLOC=libc
cd -
chown -R $(whoami):$(whoami) redis-stable
