import requests
from orionsdk import SwisClient

def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''

    swis = SwisClient(npm_server, username, password)

    r = swis.query('SELECT TOP 1 AlertObjectID FROM Orion.AlertActive ORDER BY TriggeredDateTime DESC')['results']
    
    if len(r) == 0:
        print('No active alerts found.')
        return

    alertObjectId = r[0]['AlertObjectID']
    alerts = [alertObjectId] # AppendNode expects a list of AlertObjectID values
    note = 'Python was here'

    success = swis.invoke('Orion.AlertActive', 'AppendNote', alerts, note)

    if success:
        print('It worked.')
    else:
        print('Something went wrong.')

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    main()
