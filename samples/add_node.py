from __future__ import print_function
import re
import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(npm_server, username, password)
    print("Add an SNMP v2c node:")

    # fill these in for the node you want to add!
    ip_address = '127.0.0.1'
    community = 'public'

    # set up property bag for the new node
    props = {
        'IPAddress': ip_address,
        'EngineID': 1,
        'ObjectSubType': 'SNMP',
        'SNMPVersion': 2,
        'Community': community
    }

    print("Adding node {}... ".format(props['IPAddress']), end="")
    results = swis.create('Orion.Nodes', **props)
    print("DONE!")

    # extract the nodeID from the result
    nodeid = re.search('(\d+)$', results).group(0)

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
        response = swis.create('Orion.Pollers', **poller)
        print("DONE!")


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
