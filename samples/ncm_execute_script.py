from __future__ import print_function
import re
import requests
from orionsdk import SwisClient
from time import sleep

def main():
	npm_server = 'localhost'
	username = 'admin'
	password = ''

	swis = SwisClient(npm_server, username, password)
	
	ip = '10.199.252.6'
	data = swis.query('SELECT NodeID FROM Cirrus.Nodes WHERE AgentIP = @ip', ip=ip)['results']
	nodeId = data[0]['NodeID']
	script = 'show clock'

	swis.invoke('Cirrus.ConfigArchive', 'Execute', [nodeId], script, username)

	transferId = '{{{0}}}:{1}:ExecuteScript'.format(nodeId, username)

	status = 'Queued'
	while status != 'Complete' and status != 'Error':
		sleep(1)
		data = swis.query('SELECT T.Status, T.Error FROM Cirrus.TransferQueue T WHERE T.TransferID=@transfer', transfer=transferId)['results']
		status = data[0]['Status']

	data = swis.query('SELECT T.Log FROM Cirrus.TransferQueue T WHERE T.TransferID=@transfer', transfer=transferId)['results']
	output = data[0]['Log']
	print(output)

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
	main()
