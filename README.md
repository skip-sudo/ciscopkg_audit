Compare active packages installed on Cisco routers with reference router and display the differences   

    Use Case:        
        In an environment with multiple testbeds and multiple IOS-XR devices per testbed, the packages installed on the devices can often go out of sync
        This utility identifies the devices and its packages that are not in sync with the reference device

        This can be also used for devices running IOS or NX-OS by updating the platform field in groups.yaml to 'cisco_ios' and 'cisco_nxos' respectively   

    Usage: 
        ciscopkg_audit.py [-h] router_name [-role_name ROLE_NAME] [-tb_name TB_NAME]

        router_name - reference router name whose active packages will be used to compare against active packages of other routers 
        role_name - role name assigned to the router (the key name 'role' or its value can be changed in hosts.yaml for a given device)
        tb_name - testbed name assigned to the router (the key name 'tb' or its value can be changed in hosts.yaml for a given device)

    Output Legend: 
        Router - router name 
        Missing Package - installed active package(s) in reference router not active in current router 
        Additional Package - installed active package(s) in current router not active in reference router

    Python Version Tested: 3.7.3
