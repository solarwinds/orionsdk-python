import requests
from orionsdk import SwisClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# setup swis params
npm_server = '127.0.0.1'
username = 'admin'
password = ''

# disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup the connection
swis = SwisClient(npm_server, username, password)

# Find the Uri you want to delete based on a SWQL query
results = swis.query("SELECT IPAddress, Caption, Uri FROM Orion.Nodes WHERE IPAddress LIKE '127.0.0.5'")

# Use as needed
if len(results['results']) > 1:
    print('refine your search found more than one node matching that criteria')
    [print("{Caption} - {IPAddress} - {Uri}".format(**row)) for row in results['results']]
elif len(results['results']) == 1:
    response = swis.delete(results['results'][0]['Uri'])
    print("Deleted Node - %s".format(response))
else:
    print("nothing to delete")
