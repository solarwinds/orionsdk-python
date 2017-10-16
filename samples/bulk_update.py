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

# select the top 3 nodes from the inventory
results = swis.query("SELECT TOP 3 N.CustomProperties.Uri FROM Orion.Nodes N")

# extract just the Uris from the results
uris = [row['Uri'] for row in results['results']]

# submit the request
swis.bulkupdate(uris, City='Austin', DeviceType='Router', Department='Billing')
