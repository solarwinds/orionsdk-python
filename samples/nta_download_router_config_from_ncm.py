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

    node_name = 'example.com'
    interface_name = 'GigabitEthernet0/1'

    # Get information about requested node and interface
    query = '''
        SELECT s.NetflowSourceID, s.NodeID, s.InterfaceID, s.Enabled, s.LastTimeFlow, s.LastTime, s.EngineID, 
            s.Node.NodeName,
            s.Interface.Name as InterfaceName, s.Interface.Index as RouterIndex
        FROM Orion.Netflow.Source s
        WHERE s.Node.NodeName = @nodename_par AND s.Interface.InterfaceName = @interfacename_par
    '''
    params = {
        'nodename_par': node_name,
        'interfacename_par': interface_name
    }
    query_results = swis.query(query, **params)
    print('Netflow source information for node {0} and interface {1}'.format(node_name, interface_name))
    pprint.pprint(query_results['results'])
    node_id = query_results['results'][0]['NodeID']

    # Download node configuration from NCM
    query = '''
        SELECT TOP 1 C.NodeID AS NcmNodeId, C.NodeProperties.CoreNodeId, C.DownloadTime, C.ConfigType, C.Config
        FROM NCM.ConfigArchive C
        WHERE C.NodeProperties.CoreNodeID = @orionnodeid_par
        ORDER BY C.DownloadTime DESC
    '''
    params = {
        'orionnodeid_par': node_id
    }

    query_results = swis.query(query, **params)
    last_config = query_results['results'][0]['Config']

    # Uncomment if you want to write configuration to console
    # print(last_config)

    # You can analyze configuration manually or write some parser. To identify data related to concrete Netflow Source 
    # you can use retrieved information from the first query


if __name__ == '__main__':
    main()
