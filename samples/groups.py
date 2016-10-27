from __future__ import print_function
import re
import requests
from orionsdk import SwisClient

def main():
	npm_server = 'localhost'
	username = 'admin'
	password = ''

	swis = SwisClient(npm_server, username, password)
	
	#
	# CREATING A NEW GROUP
	#
	# Creating a new group with initial Cisco and Windows devices.
	#
	swis.invoke('Orion.Container', 'CreateContainer',
		# group name
		'Sample Python Group',

		# owner, must be 'Core'
		'Core',

		# refresh frequency in seconds
		60,

		# Status rollup mode:
		# 0 = Mixed status shows warning
		# 1 = Show worst status
		# 2 = Show best status
		0,

		# group description
		'Group created by the Python sample script.',

		# polling enabled/disabled = true/false
		True,

		# group members
		[
			{'Name': 'Cisco Devices',   'Definition': "filter:/Orion.Nodes[Vendor='Cisco']"},
			{'Name': 'Windows Devices', 'Definition': "filter:/Orion.Nodes[Vendor='Windows']"}
		]
	)

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
	main()
