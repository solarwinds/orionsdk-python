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
results = swis.query("SELECT TOP 3 Caption, URI FROM Orion.Nodes")
nodes = results['results']

# build the body that will be passed to the query
body = {"uris": [], "properties": {}}

# add the URIs with a '/CustomProperties' suffix to each
for node in nodes:
    body["uris"].append(node["URI"] + "/CustomProperties")

# set as many custom properties as you like
body["properties"]["City"] = "Austin"
body["properties"]["DeviceType"] = "Router"
body["properties"]["Department"] = "Billing"

# submit the request
swis.bulkupdate(body)
