import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''
    importfile = 'out.xml' #file which contain AlertConfiguration in xml format.

    swis = SwisClient(npm_server, username, password)

    with open(importfile, 'r') as f:
        alert = f.read()

        results = swis.invoke('Orion.AlertConfigurations', 'Import', alert)
        print(results)

requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()