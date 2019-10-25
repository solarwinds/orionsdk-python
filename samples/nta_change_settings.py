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

    # List available Orion Settings
    # Uncomment if you want to get  all available Orion Settings
    # query_results = swis.query('SELECT SettingID, Name, Description, Units, Minimum, Maximum, CurrentValue, DefaultValue, Hint FROM Orion.Settings')
    # pprint.pprint(query_results['results'])

    setting_id = 'CBQoS_Enabled'
    query_results = swis.query('SELECT Uri FROM Orion.Settings WHERE SettingID = @settingid_par', settingid_par=setting_id)
    uri = query_results['results'][0]['Uri']
    props = {
        'CurrentValue': 0   # Change this value to 1 to enable setting
    }
    swis.update(uri, **props)
    query_results = swis.query('SELECT SettingID, Name, Description, Units, Minimum, Maximum, CurrentValue, DefaultValue, Hint FROM Orion.Settings WHERE SettingID = @settingid_par', settingid_par=setting_id)
    print('Status of the setting {0} after the change'.format(setting_id))
    pprint.pprint(query_results['results'])

if __name__ == '__main__':
    main()
