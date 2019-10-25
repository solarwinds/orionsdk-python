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

    # Disable/Enable CBQoS Sources
    node_caption = 'My testing router'
    query_results = swis.query('SELECT NodeID FROM Orion.Nodes WHERE Caption = @nodecaption_par', nodecaption_par=node_caption)
    node_id = query_results['results'][0]['NodeID']
    query_results = swis.query('SELECT Uri FROM Orion.Netflow.CBQoSSource WHERE NodeID = @nodeid_par', nodeid_par = node_id)
    enabled_flag = False    # Change this value to True if you want to enable sources
    props = {
        'Enabled': enabled_flag
    }

    for row in query_results['results']:
        swis.update(row['Uri'], **props)

    # Print results
    query_results = swis.query('SELECT CBQoSSourceID FROM Orion.Netflow.CBQoSSource WHERE NodeID = @nodeid_par and Enabled = @enabled_par', 
        nodeid_par=node_id, enabled_par=enabled_flag)
    print('Changed enabled status to {0} for {1} CBQoS sources for node with ID {2}'
        .format(enabled_flag, len(query_results['results']), node_id))


if __name__ == '__main__':
    main()
