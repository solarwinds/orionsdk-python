import requests
from orionsdk import SwisClient


def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(npm_server, username, password)
    print("Invoke Test:")
    aliases = swis.invoke(
        'Metadata.Entity',
        'GetAliases',
        'SELECT B.Caption FROM Orion.Nodes B')
    print(aliases)


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
