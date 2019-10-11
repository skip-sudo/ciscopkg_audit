#!/usr/bin/env python

"""
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

"""

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
import logging, argparse, sys 
from tabulate import tabulate
import texttable as tt


rtr_data = {}
table_header_list = ['Router', 'Missing Package', 'Additional Package']
table = []
tab = tt.Texttable()
tab.header(table_header_list)
tab.set_cols_align(['l', 'l', 'l'])
tab.set_cols_width([16, 40, 40])


def get_router_packages(rtr, rtr_output):
    # return the active installed packages of router from router output 
    rtr_res = []
    rtr_res = [x.strip() for x in str(rtr_output).split('\n') if x != '' and 'Active Packages' not in x ]

    return rtr_res[1:] # strip timestamp in first line     

def main():

    rtr_data = {}

    # parse command line switch
    parser = argparse.ArgumentParser(description='SMU Audit script arguments', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('router_name', help='Reference router name')
    parser.add_argument('-role_name', help='router role name', required=False)
    parser.add_argument('-tb_name', help='router testbed name', required=False)
    args = parser.parse_args()

    ref_rtr = args.router_name

    # Initialize Nornir 
    nr = InitNornir(config_file="config.yaml")
  
    # check router name is defined in hosts file 
    if args.router_name not in (nr.inventory.hosts.keys()):
        print('ERROR: Router name', args.router_name, 'not defined in hosts file')
        sys.exit(0)

    # get group name of reference router 
    ref_rtr_group = nr.inventory.hosts[ref_rtr].groups[0]

    # get command line for ref rtr group 
    cmd_line = nr.inventory.groups[ref_rtr_group].data['cmd']

    # filter hosts based on optional args 
    filtered_host = nr # initialize filtered_host to initialized Nornir object
    if args.role_name:
        filtered_host = filtered_host.filter(role=args.role_name)
    if args.tb_name:
        filtered_host = filtered_host.filter(tb=args.tb_name)

    # check ref_rtr is in filtered host else smu_audit is not applicable
    filtered_host_list = filtered_host.inventory.hosts.keys()
    if ref_rtr not in filtered_host.inventory.hosts.keys():
        print('ERROR: Reference router', ref_rtr, 'not in filtered host list', list(filtered_host_list), '- check filter combinations')
        sys.exit(0)

    # get output of active packages installed on filtered devices 
    result = filtered_host.run(
        task=netmiko_send_command,
        command_string=cmd_line
    )

    # create master list of active packages from reference router
    ref_rtr_result = result[ref_rtr][0]
    ref_rtr_packages = get_router_packages(ref_rtr, ref_rtr_result)

    # verify active packages from ref router could be extracted 
    if not ref_rtr_packages:
        print('ERROR: Active packages could not be retrieved from reference router', ref_rtr, '- check filter combination')
        sys.exit(0)

    # loop over all routers and compare active packahes with ref rtr 
    for rtr in result.keys():
        rtr_data = get_router_packages(rtr, result[rtr][0]) 
        pkg_missing = list(set(ref_rtr_packages).difference(rtr_data))
        pkg_additional = list(set(rtr_data).difference(ref_rtr_packages))
        tab.add_row([rtr, '\n'.join(pkg_missing), '\n'.join(pkg_additional)])

    #print tabulate(table, headers=table_header_list, tablefmt='fancy_grid', stralign='left')
    print(tab.draw())


if __name__ == '__main__':
    main()