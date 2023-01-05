from __future__ import print_function
import re
import requests
from orionsdk import SwisClient

def main():
    npm_server = 'localhost'
    username = 'admin'
    password = ''
    target_node_ip = '1.2.3.4'
    #Credential ID from Orion.Credential where Orion.Credential.CredentialOwner is:
    #SolarWinds.Orion.Core.Models.Credentials.SnmpCredentialsV2 or
    #SolarWinds.Orion.Core.Models.Credentials.SnmpCredentialsV3 or
    #SolarWinds.Orion.Core.SharedCredentials.Credentials.UsernamePasswordCredential
    #where 3 is SNMPV2 community string 'public' and present by default.
    credential_id = 3
    orion_engine_id = 1

    swis = SwisClient(npm_server, username, password)
    print("Add an SNMP v3 node:")

    corePluginContext = {
    	'BulkList': [{'Address': target_node_ip}],
    	'Credentials': [
    		{
    			'CredentialID': credential_id,
    			'Order': 1
    		}
    	],
    	'WmiRetriesCount': 0,
    	'WmiRetryIntervalMiliseconds': 1000
    }

    corePluginConfig = swis.invoke('Orion.Discovery', 'CreateCorePluginConfiguration', corePluginContext)

    discoveryProfile = {
    	'Name': 'discover_one_node.py',
    	'EngineID': orion_engine_id,
    	'JobTimeoutSeconds': 3600,
    	'SearchTimeoutMiliseconds': 5000,
    	'SnmpTimeoutMiliseconds': 5000,
    	'SnmpRetries': 2,
    	'RepeatIntervalMiliseconds': 1800,
    	'SnmpPort': 161,
    	'HopCount': 0,
    	'PreferredSnmpVersion': 'SNMP2c',
    	'DisableIcmp': False,
    	'AllowDuplicateNodes': False,
    	'IsAutoImport': True,
    	'IsHidden': True,
    	'PluginConfigurations': [{'PluginConfigurationItem': corePluginConfig}]
    }

    print("Running discovery...")
    result = swis.invoke('Orion.Discovery', 'StartDiscovery', discoveryProfile)
    print("Returned discovery profile id {}".format(result))

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    main()
