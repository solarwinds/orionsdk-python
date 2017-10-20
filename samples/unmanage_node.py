import requests
from orionsdk import SwisClient
from datetime import datetime, timedelta


def main():
    hostname = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(hostname, username, password)
    results = swis.query('SELECT NodeID, Caption FROM Orion.Nodes WHERE IPAddress = @ip_addr', ip_addr='127.0.0.1')
    if results['results']:
        nodeId = results['results'][0]['NodeID']
        caption = results['results'][0]['Caption']
        netObjectId = 'N:{}'.format(nodeId)
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        swis.invoke('Orion.Nodes', 'Unmanage', netObjectId, now, tomorrow, False)
        print('Done...{} will be unmanaged until {}'.format(caption, tomorrow))
    else:
        print("Device doesn't Exist")


requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()
