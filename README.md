# CREME-N: A toolchain of automatic dataset collection for machine learning in intrusion detection based on MITRE ATT&CK

<!-- ABOUT THE PROJECT -->
## About The Project

* This tool is an extended part of [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://github.com/buihuukhoi/CREME).
* In this part we try to:
  1. improve the stages from original 3 stages into N stages (follow [MITRE ATT&CK](https://attack.mitre.org/))
  2. improve the labeling


## Basic Info
This tool need to be run at the [Virtualbox](https://www.virtualbox.org/wiki/Downloads) environtment. You need install the Virtualbox first. In pricipal, we need 10 vm to be launched to run this tool. The VMs are:

### Not provided
  * Controller Machine
  * Data Logger Server
  * Vulnerable Client
  * Non Vulnerable Client * 2

### Provided
  * [Attacker Server](https://drive.google.com/file/d/1zJa7NnR6H2pGFx0Q9ltlyAwFAp_yWXJo/view?usp=sharing)
  * [Malicious Client](https://drive.google.com/file/d/1XNrXRrvk_iuqcQ2f0RLz9kHkoJ-vbnWs/view)
  * [Target Server](https://drive.google.com/file/d/1dbUNo7AUhTCz18CiBB82nkYE-fh_UN3V/view)
  * [Benign Server](https://drive.google.com/file/d/1JqF4WyBSz0L63DT6cHBargdjtqb7UHld/view)
  * [Router](https://drive.google.com/file/d/1IT0w5QxJlWIou4cPKWEOSIxhbEmAkrmE/view?usp=sharing)

### Recommand System Requirements
* 6 Cores of CPU
* At least 32 GB of RAM
* At 300GB of storage spaces



<!-- GETTING STARTED -->
## How To's
You need to prepare follow [Setup](#Setup) tutorial:
  * Nat network
  * 5 VMs we didn't provide
  * 5 VMs we provide
  * 2 network adapters of each VM

##### VMs on Virtual Box
![](https://i.imgur.com/R4FWhjS.png)

### VMs_Information
* Not provided:
  * Controller Machine (more than 4GB of RAM, 8GB if possible)
     * `IP`: 192.168.56.111
     * `hostname`: controller-machine
     * `passwd`: qsefthuk
  * Data Logger Server
     * `IP`: 192.168.56.121
     * `hostname`: data-logger-machine
     * `passwd`: qsefthuk
  * Vulnerable Client
     * `IP`: 192.168.56.151
     * `hostname`: vulnerable-machine
     * `passwd`: qsefthuk
  * Non Vulnerable Client 1
     * `IP`: 192.168.56.141
     * `hostname`: non-vulnerable-machine-1
     * `passwd`: qsefthuk
  * Non Vulnerable Client 2
     * `IP`: 192.168.56.142
     * `hostname`: non-vulnerable-machine-2
     * `passwd`: qsefthuk
* Provided:
  * Attacker Server
     * `IP`: 192.168.56.131
     * `hostname`: attacker-server
     * `passwd`: qsefthuk
  * Malicious Client
     * `IP`: 192.168.56.161
     * `hostname`: malicious-client
     * `passwd`: qsefthuk
  * Target Server
     * `IP`: 192.168.56.181
     * `hostname`: metasploitable3-ub1404
     * `passwd`: qsefthuk
  * Benign Server
     * `IP`: 192.168.56.171
     * `hostname`: metasploitable3-ub1404
     * `passwd`: qsefthuk

### Setup
0. You should use a `local network` in your testbed, not a public network. Because in the scanning phase of the attack, we assume we don't know the vulnerable clients, so we will scan in the network (with subnet mask 24) then try to find the vulnerable clients (similar to real attacks). You may get into some trouble if using the public network.
1. `Create a Nat network`:\
    Open VirtualBox 🡪 File 🡪 Preferences… 🡪 Network 🡪 Add a new NatNetwork 🡪 Right click on the new network 🡪 Edit NAT Network 🡪 Update Network CIDR to 192.168.56.0/24 🡪 OK 🡪 OK
2. `Import 5 provided VMs into VirtualBox`:\
    Import from [Provided](#Provided) and check the informations are all correct ([VMs_Information](#VMs_Information)).
3. `Install 5 VMs we didn't provide`:\
    OS version should be [Ubuntu 20.04(server/desktop)](https://ubuntu.com/download). create hostname and passwd follow [VMs_Information](#VMs_Information).
4. `Set network adapters of each VM`(note the sequence): Right click on the VM 🡪 Setting 🡪 Network 🡪 Adapter
    * Set Network Adapter 1 to **Host-Only** (Don't forget to set you host OS Virtualbox Interface IP to `192.168.56.1`):
    * Set Network Adapter 2 to **NAT network you created in step1**
5. `Set 5 VMs you created in step3`: Startup VMs 🡪 Settings 🡪
    * Network 🡪 Choose Ethernet enp0s8(adapter2) wired botton 🡪 IPv4 🡪 Manual
        * Address: follow [VMs_Information](#VMs_Information)
        * Netmask: 24
        * Gateway: 192.168.56.2
        * DNS: 8.8.8.8, 8.8.4.4 (turn off Automatic botton)
    * About 🡪 Software Updates 🡪 Updates 🡪 Automatically check for updates 🡪 Never
6. `Continue to set 5 VMs you created`: Open terminal and do the followings
    * `sudo passwd root` 🡪 Set passwd to **qsefthuk**
    * `sudo apt update` 🡪 `sudo apt install openssh-server` 🡪 `sudo apt install vim`
    * `sudo vim /etc/ssh/sshd_config` 🡪 Find the line contains **PermitRootLogin** 🡪\
    Updates it to `PermitRootLogin yes` 🡪 save and quit
    * `systemctl restart sshd`
7. `Clone and set the Repository`:    
    `git clone https://github.com/masjohncook/CREME-N.git` 🡪 `sudo chown -R user:user CREME-N/` 🡪\
    `sudo chmod -R 777 CREME-N` 🡪 `cd CREME-N` 🡪 `chmod +x setup.sh setup_tool.sh run_creme.sh` 🡪\
    `sudo ./setup_tool.sh` 🡪 `./setup.sh` 🡪 Wait till all processes is finished

### Run
1. Turn on all or your machines(10 Machines)
2. Login to your controller
3. `cd CREME-N/` 🡪 `~# ./run_creme.sh`
4. Access the controll interface using your **Host OS Browser** `http://<your controller IP>:8000`

##### Example of Web Interface
![](https://i.imgur.com/5xTMXRn.png)



<!-- Dataset -->
<!--## Generated Dataset

The dataset can be found at [here](https://drive.google.com/drive/folders/1bEsx64H2vogJKgI_OTVQ8n71VahtLxz5?usp=sharing)-->

## Publications
* [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://www.sciencedirect.com/science/article/abs/pii/S1084804521002137)
