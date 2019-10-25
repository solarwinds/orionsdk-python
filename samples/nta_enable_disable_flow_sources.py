from __future__ import print_function
import re
import requests
import pprint
from orionsdk import SwisClient

def main():
    # Connect to SWIS
    server = 'localhost'
    username = 'admin'
    password = ''
    swis = SwisClient(server, username, password)
    
    # Get data required for configuration
    node_caption = 'My test node'
    query_results = swis.query('SELECT NodeID FROM Orion.Nodes WHERE Caption = @nodecaption_par', nodecaption_par=node_caption)
    node_id = query_results['results'][0]['NodeID']
    query_results = swis.query('SELECT NetflowSourceID FROM Orion.Netflow.Source WHERE NodeID = @nodeid_par', nodeid_par = node_id)
    netflow_sources_ids = [ r['NetflowSourceID'] for r in query_results['results'] ]

    # Disable Flow Sources
    swis.invoke('Orion.Netflow.Source', 'DisableFlowSources', netflow_sources_ids)
    query_results = swis.query('SELECT NetflowSourceID FROM Orion.Netflow.Source WHERE NodeID = @nodeid_par and Enabled = false', nodeid_par = node_id)
    print('Disabled {0} Flow Sources for node with ID {1}'.format(len(query_results['results']), node_id))

    # Enable Flow Sources
    swis.invoke('Orion.Netflow.Source', 'EnableFlowSources', netflow_sources_ids)
    query_results = swis.query('SELECT NetflowSourceID FROM Orion.Netflow.Source WHERE NodeID = @nodeid_par and Enabled = true', nodeid_par = node_id)
    print('Enabled {0} Flow Sources for node with ID {1}'.format(len(query_results['results']), node_id))


if __name__ == '__main__':
    main()
