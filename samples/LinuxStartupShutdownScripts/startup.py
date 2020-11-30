from __future__ import print_function
import re
import netifaces as ni
import requests
from orionsdk import SwisClient

def main():
    orion_server = '' #orion ip adress here
    username = '' # orion username
    password = '' # orion user password

    engine_id = 1

    network_interface_name = 'eth0' # local network interface to detect ip
    
    # decide if you want monitor machine by Agent
    deploy_agent = True

    ni.ifaddresses(network_interface_name)
    ip_address = ni.ifaddresses(network_interface_name)[ni.AF_INET][0]['addr']

    swis = SwisClient(orion_server, username, password)
    
    if deploy_agent:
        print('Deploying agent...')
        
        machine_username = '' # linux machine username
        machine_password = '' # linux machine password
    
        deploy_agent_result = swis.invoke('Orion.AgentManagement.Agent', 'Deploy', engine_id, ip_address, ip_address, ip_address, machine_username, machine_password)
        
        print('Agent deployed!')
    else:
        print("Add an SNMP v2c node:")

        # fill these in for the node you want to add!
        community = 'public'

        # set up property bag for the new node
        props = {
            'IPAddress': ip_address,
            'Caption': ip_address,
            'EngineID': engine_id,
            'ObjectSubType': 'SNMP',
            'SNMPVersion': 2,
            'Community': community,

            'DNS': '',
            'SysName': ''
        }

        print("Adding node {}... ".format(props['IPAddress']), end="")
        results = swis.create('Orion.Nodes', **props)
        print("DONE!")

        # extract the nodeID from the result
        nodeid = re.search(r'(\d+)$', results).group(0)

        pollers_enabled = {
            'N.Status.ICMP.Native': True,
            'N.Status.SNMP.Native': False,
            'N.ResponseTime.ICMP.Native': True,
            'N.ResponseTime.SNMP.Native': False,
            'N.Details.SNMP.Generic': True,
            'N.Uptime.SNMP.Generic': True,
            'N.Cpu.SNMP.HrProcessorLoad': True,
            'N.Memory.SNMP.NetSnmpReal': True,
            'N.AssetInventory.Snmp.Generic': True,
            'N.Topology_Layer3.SNMP.ipNetToMedia': False,
            'N.Routing.SNMP.Ipv4CidrRoutingTable': False
        }

        pollers = []
        for k in pollers_enabled:
            pollers.append(
                {
                    'PollerType': k,
                    'NetObject': 'N:' + nodeid,
                    'NetObjectType': 'N',
                    'NetObjectID': nodeid,
                    'Enabled': pollers_enabled[k]
                }
            )

        for poller in pollers:
            print("  Adding poller type: {} with status {}... ".format(poller['PollerType'], poller['Enabled']), end="")
            swis.create('Orion.Pollers', **poller)
            print("DONE!")

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    main()