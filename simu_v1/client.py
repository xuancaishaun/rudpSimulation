from rudpUser import *
from time import sleep
from testCase import *
from sys import argv

if len(argv) != 2:
	print '--Usage: python client.py <Case ID>    # Case ID: 1 - 18'
	pass
else:
	caseID = int(argv[1])

	client = rudpSender()
	destPort = RCV_PORT
	destAddr = '137.189.97.35'

	data = '[START] (From The Standard)...Regrettably, his inflexible and headstrong handling of the national education controversy has reinforced among some people the deep-seated mistrust of CY that he is a lackey of the Chinese Communist Party. Does he realize that his "communist comrade" image is so strong that even after he openly and publicly signed a declaration that he did not belong to any "political" party, the public largely held him to do so anyway? What"s wrong with this? Trust is the key to this bizarre attitude among the public towards CY....[END]'

	if TestOn == False:
		print 'Client is going to transfer a large amount of data.'	
		if client.sendData(data, destAddr, destPort): print '\nClient: data delivery - OK\n'
		else: print '\nClient: data delivery - failure\n'
	else:
		print '\n---------------------START (Client)---------------------'
		print '===> [TEST  ID] {}'.format(TestCase[caseID][0])
		print '===> [Scenario] {}'.format(TestCase[caseID][1])
		print '===> [Solution] {}'.format(TestCase[caseID][2])
			
		if TestCase[caseID][0] == 1:
			print ''
			print '--> Client: will not send any data to Server'
			print '--> Effect: No SYN sent to Server'
			print ''
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 2:
			client.rudp.desAddr = (destAddr, destPort)
			print ''	
			print '--> Client: send SYN to Server (wrong TYPE)'
			client.rudp.send(DAT, client.rudp.pktId, '')
			sleep(1)
			print '--> Server should ignore this wrong SYN'
			print ''
			print '--> Client: send valid SYN to Server and transfer data normally'
			client.sendData(data, destAddr, destPort)
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] in {3, 4, 5, 7, 8, 9, 13, 14, 15}:
			print '--> Client: send valid SYN to Server and transfer data normally'	
			if client.sendData(data, destAddr, destPort): print '--> Client: data delivery - OK'
			else: print '--> Client: data delivery - failure'
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 6:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			print '---> Client: send SYN again after Handshaking'
			for i in xrange(2):
				print '---> Client: send SYN to Server (duplicate)'
				client.rudp.send(SYN, client.rudp.pktId - 1, '')
				client.rudp.recv()
				sleep(1)
			print '--> Client: send valid SYN to Server and transfer data normally'	
			if client.sendData(data, destAddr, destPort): print '--> Client: data delivery - OK'
			else: print '--> Client: data delivery - failure'
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0]==10:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			print '---> Client: send only one DAT to Server'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0]==11:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---> Client2: send DAT to Client (wrong IPADDR)'
			client2 = rudpSender(SDR_PORT + 1000)
			client2.rudp.pktId = client.rudp.pktId
			client2.rudp.desAddr = client.rudp.desAddr
			client2.rudp.send(DAT, client2.rudp.pktId, '')
			sleep(1)
			print '---> Client: send DAT to Client (ID = pktId - 1)'
			client.rudp.send(DAT, client.rudp.pktId - 1, '')
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 12:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---> Client: send DAT to Client (wrong TYPE or other ID)'
			# please comment either one
			client.rudp.send(SYN, client.rudp.pktId, '')
			#client.rudp.send(DAT, client.rudp.pktId + 100, '')
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 16:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---> Client: Enter Data-Delivery'
			print '---> Client: Closing the connection'
			print '---> Client2: send FIN to Server'
			client2 = rudpSender(SDR_PORT + 1000)
			client2.rudp.pktId = client.rudp.pktId
			client2.rudp.desAddr = client.rudp.desAddr
			client2.rudp.send(FIN, client2.rudp.pktId, '')
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 17:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---> Client: Enter Data-Delivery'
			print '---> Client: Closing the connection'
			print '---> Client: send FIN to Server (wrong ID)'
			client.rudp.send(FIN, client.rudp.pktId + 100, '')
			print '---------------------END (Client)-----------------------\n'
		elif TestCase[caseID][0] == 18:
			client.rudp.connect(destAddr, destPort)
			print '---> Client: connect() - OK'
			client.rudp.send(DAT, client.rudp.pktId, 'the only DAT')
			client.rudp.pktId += 1
			print '---> Client: Enter Data-Delivery'
			print '---> Client: Closing the connection'
			print '---> Client: send FIN to Server (repeatedly)'
			for i in xrange(5):
				client.rudp.send(FIN, client.rudp.pktId, '')
				sleep(2)
			print '---------------------END (Client)-----------------------\n'
		else: pass
