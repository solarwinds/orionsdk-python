import requests
from orionsdk import SwisClient

npm_server = 'localhost'
username = 'admin'
password = ''

verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


swis = SwisClient(npm_server, username, password)

print("Query Test:")
results = swis.query("SELECT TOP 3 NodeID, DisplayName FROM Orion.Nodes")

for row in results['results']:
    print("{NodeID:<5}: {DisplayName}".format(**row))



