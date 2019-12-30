from orionsdk import SwisClient

solarwinds_server = 'server.local'  # Change this to your solarwinds IP or hostname
username = 'myusername'  # Change this to your username
password = 'mypassword'  # Change this to your password

node_1_ip = '192.168.1.1'  # example of an IP address of node we want to delete
node_2_ip = '192.168.1.2'  # example of an IP address of node we want to delete

sw = SwisClient(solarwinds_server, username, password)

# Gather URI's for each node we want to delete
node_1_uri = sw.query("SELECT Uri FROM Orion.Nodes WHERE IPAddress = @ip", ip=node_1_ip)['results'][0]['Uri']
node_2_uri = sw.query("SELECT Uri FROM Orion.Nodes WHERE IPAddress = @ip", ip=node_2_ip)['results'][0]['Uri']

# delete nodes
sw.bulkdelete([node_1_uri, node_2_uri])