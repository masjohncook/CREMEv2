#!/bin/bash

# install python 3.6
sudo apt install build-essential checkinstall -y
sudo apt install libreadline-gplv2-dev libncursesw5-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
sudo apt install libssl-dev libncurses5-dev libreadline-dev libgdm-dev libdb4o-cil-dev -y
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
tar xvf Python-3.6.2.tar.xz	
cd Python-3.6.2/	
./configure
sudo make
sudo make install
cd ..
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 2


sudo apt-get update
sudo apt-get install expect -y

# virtual environment
sudo apt-get install python3-venv -y

# install ssh server
sudo apt-get install openssh-server -y

# install atop
sudo apt-get install atop -y

# install argus-serer and argus-client
wget http://qosient.com/argus/src/argus-3.0.8.2.tar.gz
wget http://qosient.com/argus/src/argus-clients-3.0.8.2.tar.gz

tar -xvzf argus-3.0.8.2.tar.gz
tar -xvzf argus-clients-3.0.8.2.tar.gz

sudo apt-get update
sudo apt-get install flex -y
sudo apt-get install bison -y
sudo apt-get install libpcap-dev -y
sudo apt-get install tmux -y

cd argus-3.0.8.2
chmod +x configure
./configure
sudo make install

cd -

cd argus-clients-3.0.8.2
chmod +x configure
./configure
sudo make install
sudo make install

cd -
