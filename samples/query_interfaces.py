#!/usr/bin/env python
import requests
from orionsdk import SwisClient


npm_server = 'localhost'
username = 'admin'
password = ''

verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    swis = SwisClient(npm_server, username, password)

    query = """
        SELECT TOP 10
            n.NodeID,
            n.Caption AS NodeName,
            i.InterfaceID,
            i.Caption AS InterfaceName
        FROM
            Orion.Nodes n
        JOIN
            Orion.NPM.Interfaces i ON n.NodeID = i.NodeID
    """

    results = swis.query(query)

    for row in results['results']:
        print("{NodeID} [{NodeName}] : {InterfaceID} [{InterfaceName}]".format(**row))


if __name__ == '__main__':
    main()

