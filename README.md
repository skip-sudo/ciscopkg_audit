### Compare active packages installed on Cisco routers and display the differences using Nornir and Python   

In an environment with multiple Cisco IOS-XR devices in one or more setup, the packages installed on the devices can often go out of sync. It may be necessary to have the same package line up in all or a group of devices. This utility identifies the devices and its packages that are not in sync with the packages of the reference device and displays the diff.

This utility can be also used for devices running IOS XE or NX-OS by updating the platform field in groups.yaml to 'cisco_ios' and 'cisco_nxos' respectively.    

It uses Nornir (a python based automation framework) to parallelize the information gathering from multiple devices and python to process and display the result in tabular format. 

### How to Use 
#### Clone the repo 
```
git clone https://github.com/skip-sudo/ciscopkg_audit
cd ciscopkg_audit 
```

#### Install Python packages 
First create a python virtual environment. It is not a hard requirement but recommended. And use python3 (tested on python 3.7.3).
```
virtualenv -p python3 venv3-ciscopkag
source venv3-ciscopkag/bin/activate
```
Next install the required python packages 
```
pip install -r requirements.txt
```

#### Uppdate the Nornir configuration and device files   
There are three files used by Nornir at the basic level. One configuration file (config.yaml) and two inventory files (hosts.yaml and groups.yaml)

* config.yaml - here we are specifying the number of threads to run in parallel. Adjust appropriately depending on the number of devices in the setup
* hosts.yaml - in this file we define the router hostname, their IP address, ports, groups they belong to and any arbitrary data in key:value format. We are using role and testbed as an example to show the logical grouping. Update as appropriate. 
* groups.yaml - the groups referenced by the devices. Since username, password, platform will be common to the devices, it makes sense to keep them in group. 

#### Run the script 
##### Usage: 
        ciscopkg_audit.py [-h] router_name [-role_name ROLE_NAME] [-tb_name TB_NAME]

        router_name - reference router name whose active packages will be used to compare against active packages of other routers 
        role_name - role name assigned to the router (the key name 'role' or its value can be changed in hosts.yaml for a given device)
        tb_name - testbed name assigned to the router (the key name 'tb' or its value can be changed in hosts.yaml for a given device)

If optional arguments are not passed, all the devices defined in hosts file will be compared against the reference router. Otherwise a filtered list of the inventory will be built based on the argument values of roles and testbed and the subset of devices will be used instead. 

#### Output

(venv3-smuaudit) $ ./ciscopkg_audit.py D11_TB2_5508_PF -role edge 


|      Router      |             Missing Package              |            Additional Package            |
| ---------------- | -----------------------------------------| ---------------------------------------- |
| D11_TB1_5508_PF  |                                          |                                          |
|------------------|------------------------------------------|------------------------------------------|
| D11_TB2_5508_PF  |                                          |                                          |
|------------------|------------------------------------------|------------------------------------------|
| D11_TB6_5508_PF  | ncs5500-dpa-                             | ncs5500-infra-6.1.0.1-r653.CSCvo13888    |
|                  | fwding-5.0.0.10-r653.CSCvo81436          | ncs5500-dpa-                             |
|                  | ncs5500-dpa-3.0.0.5-r653.CSCvq45452      | fwding-5.0.0.3-r653.CSCvp52569           |
|                  | ncs5500-infra-6.1.0.4-r653.CSCvo92663    | ncs5500-routing-4.0.0.1-r653.CSCvp04860  |
|                  | openssh-sshd-6.6p1.p1-r0.0.CSCvp70185.xr | ncs5500-mpls-te-                         |
|                  | ncs5500-os-                              | rsvp-3.1.0.1-r653.CSCvp46117             |
|                  | support-6.0.0.2-r653.CSCvo92663          | ncs5500-dpa-3.0.0.2-r653.CSCvp52569      |
|                  | ncs5500-mpls-te-                         |                                          |
|                  | rsvp-3.1.0.2-r653.CSCvo94609             |                                          |
|                  | ncs5500-routing-4.0.0.3-r653.CSCvo77677  |                                          |
|--------------------------------------------------------------------------------------------------------|

(venv3-smuaudit)$

Output Legend: 

Router - router name 
Missing Package - installed active package(s) in reference router but not active in current router 
Additional Package - installed active package(s) in current router but not active in reference router

