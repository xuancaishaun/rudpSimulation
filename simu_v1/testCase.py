from sys import argv

TESTING = True
TestOn = True

TestCase = dict()
TestCase[1] = (1, '[Handshaking] Server: No SYN for very long time', 'Server: auto shutdown')
TestCase[2] = (2, '[Handshaking] Server: pkts with wrong type and id received','Server: ignore')
TestCase[3] = (3, '[Handshaking] Client: No SYN_ACK for very long time','Client: ignore')
TestCase[4] = (4, '[Handshaking] Client: SYN_ACK with wrong DESTADDR', 'Client: ignore')
TestCase[5] = (5, '[Handshaking] Client: SYN_ACK with wrong TYPE or ID', 'Client: "Close"')
TestCase[6] = (6, '[Handshaking ~ Data-Delivery] Server: SYN again after last SYN_ACK', 'Server: SYN_ACK / END_TIME_OUT')
TestCase[7] = (7, '[Data-Delivery] Client: No ACK for RTO_TIME_OUT / MAX_RESND', 'Client: Re-transmission / "Close"')
TestCase[8] = (8, '[Data-Delivery] Client: ACK with wrong DESTADDR or ID = pktId - 1', 'Client: ignore')
TestCase[9] = (9, '[Data-Delivery] Client: ACK with wrong TYPE or other ID', 'Client: "Close"')
TestCase[10] = (10,'[Data-Delivery] Server: NO DAT for END_TIME_OUT', 'Server: "End"')
TestCase[11] = (11,'[Data-Delivery] Server: DAT with wrong DESTADDR or ID = pktId - 1', 'Server: ignore')
TestCase[12] = (12,'[Data-Delivery] Server: DAT with wrong TYPE (SYN) or other ID', 'Server: "End"')  ##***
TestCase[13] = (13,'[Shutdown] Client: No FIN_ACK for RTO_TIME_OUT / MAX_RESND', 'Client: Re-transmission / "Close"')
TestCase[14] = (14,'[Shutdown] Client: FIN_ACK with wrong DESTADDR', 'Client: ignore')
TestCase[15] = (15,'[Shutdown] Client: FIN_ACK with wrong TYPE or other ID', 'Server: "End"')
TestCase[16] = (16,'[Shutdown] Server: FIN with wrong DESTADDR', 'Server: ignore')
TestCase[17] = (17,'[Shutdown] Server: FIN with wrong ID', 'Server: "End"')
TestCase[18] = (18,'[Shutdown] Server: FIN again after last FIN_ACK', 'Server: FIN_ACK / END_TIME_OUT')


if __name__ == '__main__':

	if len(argv) != 2 or (len(argv) == 2 and int(argv[1]) not in range(1,19)):
		print '--> Usage: $ python testCase.py <Case ID>    # Case ID: 1 - 18'
		pass
	else:
		try: 
			ID = int(argv[1])
			print '===> [TEST  ID] {}'.format(TestCase[ID][0])
			print '===> [Scenario] {}'.format(TestCase[ID][1])
			print '===> [Solution] {}'.format(TestCase[ID][2])
		except KeyError:
			print '--> Usage: $ python testCase.py <Case ID>    # Case ID: 1 - 17'
			pass