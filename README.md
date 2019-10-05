### Compare active packages installed on Cisco routers and display the differences using Nornir and Python   

In an environment with multiple Cisco IOS-XR devices in one or more setup, it may be necessary to have the same package line up in all or a group of devices. This utility helps to identify the devices and their packages that are not in sync with the packages installed on reference device and displays the diff.

This utility can be also used for devices running IOS XE or NX-OS by updating the platform field in groups.yaml to 'cisco_ios' and 'cisco_nxos' respectively.    

It uses Nornir (a python based automation framework) to parallelize the information gathering from multiple devices and python to process and display the result in tabular format. Sample output can found [here](https://github.com/skip-sudo/ciscopkg_audit/blob/master/ciscopkg_audit_output.png) 

Why use Nornir? Its highly scalable by processing each device in a separate thread and uses a templatized and flexible inventory management scheme to accommodate any use case as illustrated by this utility. 

### Pre-requisite 
A Linux, Mac or Windows environment (laptop, desktop or server including VM or container) with python 3.7 installed. This will work on other python versions as well as long as the required set of python packages are installed. 

### Installation 
#### Clone the repo 
```
git clone https://github.com/skip-sudo/ciscopkg_audit
cd ciscopkg_audit 
```

#### Install Python packages 
First create a python virtual environment. It is not a hard requirement but recommended.
```
virtualenv -p python3 venv3-ciscopkag
source venv3-ciscopkag/bin/activate
```
Next install the required python packages 
```
pip install -r requirements.txt
```

### Configuration
#### Update the Nornir configuration and device files   
There are three files used by Nornir at the basic level. One configuration file (config.yaml) and two inventory files (hosts.yaml and groups.yaml)

* config.yaml - here we are specifying the number of threads to run in parallel. Adjust appropriately depending on the number of devices in the setup
* hosts.yaml - in this file we define the router hostname, their IP address, ports, groups they belong to and any arbitrary data in key:value format. We are using role and testbed as an example to show the logical grouping. Update as appropriate. 
* groups.yaml - the groups referenced by the devices. Since username, password, platform will be common to the devices, it makes sense to keep them in group. 

### Usage
#### Run the script 
```
# ciscopkg_audit.py [-h] router_name [-role_name ROLE_NAME] [-tb_name TB_NAME]

Arguments:

router_name - reference router name whose active packages will be used to compare against active packages of other routers 
role_name - role name assigned to the router (the key name 'role' or its value can be changed in hosts.yaml for a given device)
tb_name - testbed name assigned to the router (the key name 'tb' or its value can be changed in hosts.yaml for a given device)
```

If optional arguments are not passed, all the devices defined in hosts file will be compared against the reference router. Otherwise a filtered list of the inventory will be built based on the argument values of roles and testbed and the subset of devices will be used instead. 

#### Output

[Sample output](https://github.com/skip-sudo/ciscopkg_audit/blob/master/ciscopkg_audit_output.png)

Output Legend: 

Router - router name

Missing Package - installed active package(s) in reference router but not active in current router 

Additional Package - installed active package(s) in current router but not active in reference router

If the package line up of the given router matches exactly with reference router, both Missing Package and Aditional Package cell will be blank

### Use case example 
1) 5 setup (testbed) with 10 IOS-XR devices in each setup (total 50 devices)
2) Each device belongs to a role (edge role, lsr role, etc). The IOS-XR packages installed are based on a role
3) In inventory file (hosts.yaml), create a custom data variable "tb" to identify the testbed and variable "role" to identify the appropriate role the device belongs
4) Now we can use the utility for the following use cases 
   - compare package list of all routers in a given role in a specific testbed compared to reference router 
     - use -role <> and -tb <> argument
   - compare package list of all routers in a given role across all testbeds compared to reference router 
     - use -role <> argument (leave out -tb argument)
   - compare package list of all routers in a given testbed across all roles compared to reference router
     - use =tb <> argument (leave out -role argument)
   - compare package list of all routers across all roles and testbeds compared to reference router 
     - leave out both optional arguments 

A quick benchmarking of running this utility for the above use case on 50 physical devices in 5 testbeds, produced the desired output from all devices in approximately 12 seconds.    

### Credits and references

[Nornir](https://nornir.readthedocs.io/en/stable/index.html)
