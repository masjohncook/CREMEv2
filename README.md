# CREME-N: A toolchain of automatic dataset collection for machine learning in intrusion detection based on MITRE ATT&CK

<!-- ABOUT THE PROJECT -->
## About The Project

* This tool is an extended part of [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://github.com/buihuukhoi/CREME).
* In this part we try to improve the stages used in previous CREME into N stages and try to improve the labeling


## Basic Info
This tool need to be run at the [Virtualbox](https://www.virtualbox.org/wiki/Downloads) environtment. You need install the Virtualbox first. In pricipal, we need 10 vm to be launched to run this tool. The VMs are:
* Controller Machine
* Data Logger Machine
* Vulnerable Client
* Non Vulnerable Client * 2
* Attacker Machine(**provided**)
* Malicious Client(**provided**) 
* Target Machine(**provided**)
* Benign Machine(**provided**)
* Router(**provided**)

### Provided OVA's
* [Router](https://drive.google.com/file/d/1IT0w5QxJlWIou4cPKWEOSIxhbEmAkrmE/view?usp=sharing)
* [Attacker Machine](https://drive.google.com/file/d/1zJa7NnR6H2pGFx0Q9ltlyAwFAp_yWXJo/view?usp=sharing)
* [Malicious Client](https://drive.google.com/file/d/1XNrXRrvk_iuqcQ2f0RLz9kHkoJ-vbnWs/view)
* [Target Machine](https://drive.google.com/file/d/1dbUNo7AUhTCz18CiBB82nkYE-fh_UN3V/view)
* [Benign Machine](https://drive.google.com/file/d/1JqF4WyBSz0L63DT6cHBargdjtqb7UHld/view)

### System Requirements
* 6 Cores of CPU
* 32 GB of RAM
* More than 300GB of storage drive



<!-- GETTING STARTED -->
## How To's
You need to prepare belowing **5 VMs** of [Ubuntu Server 20.04](https://ubuntu.com/download/server) and set **NAT network** by yourself follow [this](https://docs.google.com/document/d/1RJ2kCqVoS9TZtRMELRRKbjcuih4vC6Tv/edit) tutorial.
* Controller Machine
* Data Logger Machine
* Non Vulnerable Client * 2
* Vulnerable Client

### VM Setting
* You need to import all provided VMs and install the other 5 VMs
* Set all VMs:
    * Set the **root** password with `qsefthuk`(by default the password of all provided machines `qsefthuk`)
    * Network Adapter 1 to **Host-Only** except Router (Don't forget to set you host OS Virtualbox Interface IP to `192.168.56.1`)
    * Network Adapter 2 to **NAT**



##### VMs on Virtual Box
![](https://i.imgur.com/R4FWhjS.png)

### Setup
### Run
1. Login to your Controller Machine 
2. run  `~# chmod +x ./run_creme.sh` then `~# ./run_creme.sh`
3. Access the web interface using your Host OS Browser `http://<your controller IP>:8000`

##### Example of Web Interface
![](https://i.imgur.com/5xTMXRn.png)




<!-- Dataset -->
<!--## Generated Dataset

The dataset can be found at [here](https://drive.google.com/drive/folders/1bEsx64H2vogJKgI_OTVQ8n71VahtLxz5?usp=sharing)-->

## Publications
* [CREME: A toolchain of automatic dataset collection for machine learning in intrusion detection](https://www.sciencedirect.com/science/article/abs/pii/S1084804521002137)
