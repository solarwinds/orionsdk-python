import orionsdk
import datetime

server = 'orion_server'
username = 'username'
password = 'password'
ip_address = '192.168.1.1'  # change this to the node you want to use


sw = orionsdk.SwisClient(server, username, password)
uri = sw.query("SELECT Uri FROM Orion.Nodes WHERE NodeID=@node_id", IPAddress=ip_address)['results'][0]['Uri']

# to specify an end time change None to a datetime object
sw.invoke('Orion.AlertSuppression', 'SuppressAlerts', [uri], datetime.datetime.now(), None)
