### Compare active packages installed on Cisco routers and display the differences using Nornir and Python   

In an environment with multiple Cisco IOS-XR devices in one or more setup, the packages installed on the devices can often go out of sync. It may be necessary to have the same package line up in all or a group of devices. This utility identifies the devices and its packages that are not in sync with the packages of the reference device and displays the diff.

This utility can be also used for devices running IOS XE or NX-OS by updating the platform field in groups.yaml to 'cisco_ios' and 'cisco_nxos' respectively.    

It uses Nornir (a python based automation framework) to parallelize the information gathering from multiple devices and python to process and display the result in tabular format. Sample output can found [here](https://github.com/skip-sudo/ciscopkg_audit/blob/master/ciscopkg_audit_output.png) 

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

#### Update the Nornir configuration and device files   
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

[Sample output](https://github.com/skip-sudo/ciscopkg_audit/blob/master/ciscopkg_audit_output.png)

Output Legend: 

Router - router name

Missing Package - installed active package(s) in reference router but not active in current router 

Additional Package - installed active package(s) in current router but not active in reference router

### Credits and references

[Nornir](https://nornir.readthedocs.io/en/stable/index.html)
