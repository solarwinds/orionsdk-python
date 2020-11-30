from __future__ import print_function
import re
import netifaces as ni
import requests
from orionsdk import SwisClient

def main():
    orion_server = '' #orion ip adress here
    username = '' # orion username
    password = '' # orion user password

    network_interface_name = 'eth0' # local network interface to detect ip
    
    # decide if you want to only remove information about agent from Orion or also uninstall it from monitored node,
    # this flag is important only when the node is monitored by agent.
    should_uninstall_agent_from_node = True

    ni.ifaddresses(network_interface_name)
    ip_address = ni.ifaddresses(network_interface_name)[ni.AF_INET][0]['addr']

    swis = SwisClient(orion_server, username, password)

    node_id = swis.query("SELECT Uri FROM Orion.Nodes WHERE IPAddress = '{}'".format(ip_address))
    
    if len(node_id['results']) > 0:
        print("Deleting node")
        swis.delete(node_id['results'][0]['Uri'])
        print("Deleted Node")

    # query to get the agent id
    agent_id_results = swis.query("SELECT AgentId FROM Orion.AgentManagement.Agent WHERE IP = '{}'".format(ip_address))

    # this 'if' checks if orion contains agent information for this node
    if len(agent_id_results['results']) > 0:
        agent_id = agent_id_results['results'][0]['AgentId']
        if should_uninstall_agent_from_node:
            print('Uninstalling agent...')
            uninstall_agent = swis.invoke('Orion.AgentManagement.Agent', 'Uninstall', agent_id)
            print('Agent uninstalled!')
        else:
            print('Deleting agent...')
            delete_agent = swis.invoke('Orion.AgentManagement.Agent', 'Delete', agent_id)
            print('Agent deleted!')

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    main()