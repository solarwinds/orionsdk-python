import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''
    AlertID = 1 #AlertID for which we export data in xml file.

    swis = SwisClient(npm_server, username, password)
    results = swis.invoke('Orion.AlertConfigurations', 'Export', AlertID)
    print(results)

    with open('out.xml', 'w') as f:
        f.write(results)

requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()