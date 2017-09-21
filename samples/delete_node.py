import requests
from orionsdk import SwisClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# setup swis params
npm_server = 'localhost'
username = 'admin'
password = ''

# disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup the swis connection
swis = SwisClient(npm_server, username, password)

# Find the Uri you want to delete based on a SWQL query
results = swis.query("SELECT IPAddress, Caption, Uri FROM Orion.Nodes WHERE IPAddress = @ip_addr", ip_addr='127.0.0.6')

# Use as needed
if len(results['results']) > 1:
    print('refine your search. Found more than one node matching that criteria.')
elif len(results['results']) == 1:
    print("Deleting {}".format(results['results'][0]['IPAddress']))
    response = swis.delete(results['results'][0]['Uri'])
    print("Done")

else:
    print("Nothing to delete")
