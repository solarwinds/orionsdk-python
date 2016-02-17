import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(npm_server, username, password)
    print("Discover and add interfaces:")
    results = swis.invoke('Orion.NPM.Interfaces', 'DiscoverInterfacesOnNode', 1)

    # use the results['DiscoveredInterfaces'] for all interfaces
    # or get a subset of interfaces using a comprehension like below
    eth_only = [
            x for x
            in results['DiscoveredInterfaces']
            if x['Caption'].startswith('eth')]

    print(eth_only)

    results2 = swis.invoke(
            'Orion.NPM.Interfaces',
            'AddInterfacesOnNode',
            1,                    # use a valid nodeID!
            eth_only,
            'AddDefaultPollers')

    print(results2)


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
