# CREMEv2: A toolchain of automatic dataset collection for machine learning in intrusion detection based on MITRE ATT&CK

<!-- ABOUT THE PROJECT -->
## About The Project

* This tool is an extended part of 1st version [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://github.com/buihuukhoi/CREME).
* In this part we try to:
  1. improve the stages from original 3 stages into N stages (follow [MITRE ATT&CK](https://attack.mitre.org/))
  2. improve the labeling --> the data will be labelled using MITRE technique


## Basic Info
This tool need to be run at the [Virtualbox](https://www.virtualbox.org/wiki/Downloads) environment. You need install the Virtualbox first. In pricipal, we need at least 10 VMs to be launched to run this tool. The VMs are:

### VMs_Links
  * [Controller Machine](https://drive.google.com/file/d/1SKsLgNj-9fyTp854x1EwKyROSVqlUJXa/view?usp=sharing)
  * [Data Logger Server](https://drive.google.com/file/d/1me4T5wy0Vtn1XE89S8PHIJqpq23yT7lG/view?usp=sharing)
  * [Attacker Server](https://drive.google.com/file/d/1xrIjN2AYGRTewz1DuGxILgsEEclVpOtZ/view?usp=sharing)
  * [Non Vulnerable Client-1](https://drive.google.com/file/d/1gFP1xIumpLdcwvSo_aTLaG1RFWPUJtCt/view?usp=sharing)
  * [Non Vulnerable Client-2](https://drive.google.com/file/d/1NF6uL4lL1_QzP2i6JWF_JTLu9ebeVdqV/view?usp=sharing)
  * [Vulnerable Client](https://drive.google.com/file/d/1jgrI87fCKzE17Ar0ZpqmvbjgYJ4n7Ddb/view?usp=sharing)
  * [Malicious Client](https://drive.google.com/file/d/1d9kbB0IBYdukO2_ZL17ZM-vhbs-gHyRf/view?usp=sharing)
  * [Benign Server](https://drive.google.com/file/d/1sGVZfg5WLbXkfdrQeiCMtywtlykwSQKt/view?usp=sharing)
  * [Target Server](https://drive.google.com/file/d/1SLsuOdLY3gx9W38bnmsawqAuQZ5r_bwp/view?usp=sharing)
  * [Router](https://drive.google.com/drive/folders/1IGquyUqcym9Mvd-9hWRIaQrEEhzt1y9M?usp=sharing)
<!--   * [Attacker Server](https://drive.google.com/file/d/1zJa7NnR6H2pGFx0Q9ltlyAwFAp_yWXJo/view?usp=sharing)
  * [Malicious Client](https://drive.google.com/file/d/1XNrXRrvk_iuqcQ2f0RLz9kHkoJ-vbnWs/view)
  * [Target Server](https://drive.google.com/file/d/1dbUNo7AUhTCz18CiBB82nkYE-fh_UN3V/view)
  * [Benign Server](https://drive.google.com/file/d/1JqF4WyBSz0L63DT6cHBargdjtqb7UHld/view)
  * [Router](https://drive.google.com/file/d/14EuAsLdLqKamik_jdN1xt0-MNq474jwk/view?usp=sharing) -->

### Recommand System Requirements
* 6 Cores of CPU
* At least 32 GB of RAM
* At least 200GB of storage spaces



<!-- GETTING STARTED -->
## How To's
You need to prepare follow [Setup](#Setup) tutorial:
  * adapters of each VM
  * 10 VMs we provide

##### VMs on Virtual Box
![](https://i.imgur.com/R4FWhjS.png)

### VMs_Information
* Controller Machine (more than 8GB of RAM)
  * `IP`: 192.168.56.111
  * `hostname`: controller-machine
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Data Logger Server
  * `IP`: 192.168.56.121
  * `hostname`: data-logger-machine
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Vulnerable Client
  * `IP`: 192.168.56.151
  * `hostname`: vulnerable-machine
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Non Vulnerable Client 1
  * `IP`: 192.168.56.141
  * `hostname`: non-vulnerable-machine-1
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Non Vulnerable Client 2
  * `IP`: 192.168.56.142
  * `hostname`: non-vulnerable-machine-2
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Attacker Server
   * `IP`: 192.168.56.131
   * `hostname`: attacker-server
   * `password`: qsefthuk
   * `Adapter 1`: Host-Only adapter
* Malicious Client
   * `IP`: 192.168.56.161
   * `hostname`: malicious-client
   * `password`: qsefthuk
   * `Adapter 1`: Host-Only adapter
* Target Server
  * `IP`: 192.168.56.181
  * `hostname`: metasploitable3-ub1404
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Benign Server
  * `IP`: 192.168.56.171
  * `hostname`: metasploitable3-ub1404
  * `password`: qsefthuk
  * `Adapter 1`: Host-Only adapter
* Router
  * `Adapter 1`: Host-Only adapter
  * `Adapter 2`: NAT

### Network Topology
![](https://i.imgur.com/pLAkRIy.jpg)

### Setup
<!-- 1. `Create a Nat network`:\
    Open VirtualBox 🡪 File 🡪 Preferences… 🡪 Network 🡪 Add a new NatNetwork 🡪 Right click on the new network 🡪 Edit NAT Network 🡪 Update Network CIDR to 192.168.56.0/24 🡪 OK 🡪 OK -->
1. **Import 10 provided VMs into VirtualBox**:\
    Import from [VMs_Links](#VMs_Links) and check the informations are all correct ([VMs_Information](#VMs_Information)).
<!-- 2. **Install the 5 VMs we didn't provide**:\
    OS version should be [Ubuntu 20.04(server/desktop)](https://ubuntu.com/download). Create hostname and password follow [VMs_Information](#VMs_Information). -->
2. **Check network adapter of each VM we provided** (follow [VMs_Information](#VMs_Information)):\
    Right click on the VM 🡪 Setting 🡪 Network 🡪 Adapter 🡪 choose `Host-Only Ethernet Adapter`
3. **Set Host-Only Ethernet Adapter on your host OS**: Open network adapter settings **on your host OS** 🡪 Right click **VirtualBox Host-Only Network** adapter 🡪 content 🡪 IPv4 content, then type in the following informations
    * IP Address: `192.168.56.1`
    * Netmask: 255.255.255.0/24
4. **Check VMs we provided**: Startup VMs 🡪 Settings 🡪
    * Network 🡪 Choose Ethernet wired botton 🡪 IPv4 🡪 Manual
        * IP Address: follow [VMs_Information](#VMs_Information)
        * Netmask: 255.255.255.0/24
        * Gateway: `192.168.56.2`
        * DNS: 8.8.8.8, 8.8.4.4 (turn off Automatic botton)
    * About 🡪 Software Updates 🡪 Updates 🡪 Automatically check for updates 🡪 Never
<!-- 5. **Continue to set the 5 VMs you created**: Open terminal and type in the following commands\
    `sudo passwd root`, then set the password to **qsefthuk** 🡪\
    `sudo apt update` 🡪 `sudo apt install openssh-server vim -y` 🡪\
    `sudo vim /etc/ssh/sshd_config`, then find the line contains **PermitRootLogin**, Updates it to `PermitRootLogin yes` 🡪 save and quit 🡪\
    `systemctl restart sshd` -->
5. **Clone and set the Repository on Controller machine**: Open terminal and then type in the following commands\
    * `git clone https://github.com/masjohncook/CREMEv2.git`
    * `sudo chown -R controller-machine:controller-machine CREMEv2/`
    * `sudo chmod -R 777 CREMEv2`
    * `cd CREMEv2`
    * `chmod +x setup.sh setup_tools.sh run_creme.sh`
    * `source ./setup_tools.sh`
    * `cd CREMEv2`
    * `./setup.sh`

### Run
1. Turn on all your machines (10 Machines)
2. Login to your `Controller`
3. `cd CREMEv2/` 🡪 `./run_creme.sh`
4. Access the controll interface using your **Host OS Browser** `http://192.168.56.111:8000`

### Please Note
1. You should use a `local network` in your testbed, not a public network. Because in the scanning phase of the attack, we assume we don't know the vulnerable clients, so we will scan in the network (with subnet mask 24) then try to find the vulnerable clients (similar to real attacks). You may get into some trouble if using the public network.
2. If you would like to rerun several times, you can `take a snapshot` before running, then back to that snapshot to rerun again. The reason is that we already finished configuring some services, so if we reconfigure them again, it may have some behaviors different from the first time
3. If you try to run, but the error messages showed in the Dash Board indicate that you can't connect to any VM, just check if the [VMs_Information](#VMs_Information) are all correct, then try to type in the cmd `systemctl restart ssh` on the VM you can't connect to.
4. If you want to check the Tmux messages when CREMEv2 is running, open a terminal and type in `tail -f CREMEv2/celery.log`, then you can check the last 10 messages in Tmux.

##### Example of Web Interface
![](https://i.imgur.com/5xTMXRn.png)

<!-- Dataset -->
<!--## Generated Dataset

The dataset can be found at [here](https://drive.google.com/drive/folders/1bEsx64H2vogJKgI_OTVQ8n71VahtLxz5?usp=sharing)-->

## Publications
* [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://www.sciencedirect.com/science/article/abs/pii/S1084804521002137)
