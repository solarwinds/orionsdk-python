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

    alert_name = 'NTA Alert on machine-hostname'
    query_results = swis.query('Select Uri FROM Orion.AlertConfigurations WHERE Name = @alertname_par', alertname_par=alert_name)
    uri = query_results['results'][0]['Uri']

    # Disable alert
    props = {
        'Enabled':  False
    }
    swis.update(uri, **props)

    # Enable alert
    props = {
        'Enabled':  True
    }
    swis.update(uri, **props)


if __name__ == '__main__':
    main()

