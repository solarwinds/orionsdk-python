from __future__ import print_function
import re
import requests
from orionsdk import SwisClient

def main():
    # Connect to SWIS
    server = 'localhost'
    username = 'admin'
    password = ''
    swis = SwisClient(server, username, password)

    engine_id = 1
    node_caption = 'example.com'
    node_props = {
        'IPAddress': '10.0.0.1',
        'EngineID': engine_id,
        'Caption': node_caption,
        'ObjectSubType': 'SNMP',
        'Community': 'public',
        'SNMPVersion': 2,
        'DNS': '',
        'SysName': ''
    }

    # Add node
    swis.create('Orion.Nodes', **node_props)
    query_results = swis.query('SELECT NodeID FROM Orion.Nodes WHERE Caption = @caption_par', caption_par=node_caption)
    node_id = query_results['results'][0]['NodeID']
    print('New node with ID {0} created'.format(node_id))

     # Discovere and add interfaces
    results = swis.invoke('Orion.NPM.Interfaces', 'DiscoverInterfacesOnNode', node_id)
    swis.invoke('Orion.NPM.Interfaces', 'AddInterfacesOnNode', node_id, results['DiscoveredInterfaces'], 'AddDefaultPollers')
    query_results = swis.query('SELECT InterfaceID FROM Orion.NPM.Interfaces WHERE NodeID = @node_id_par', node_id_par=node_id)
    print('Discovered and added {0} interfaces for node with id {1}'.format(len(query_results['results']), node_id))
    interface_ids = [ r['InterfaceID'] for r in query_results['results'] ]

    # Add Flow sources for every interface - enable flow collection on every interface
    swis.invoke('Orion.Netflow.Source', 'EnableFlowSources', interface_ids, 'AddDefaultPollers')
    query_results = swis.query('SELECT NetflowSourceID FROM Orion.Netflow.Source WHERE NodeID = @node_id_par', node_id_par=node_id)
    print('Added {0} Flow sources for node with id {1}'.format(len(query_results['results']), node_id))


if __name__ == '__main__':
    main()
