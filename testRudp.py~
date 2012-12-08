from rudp import *
from rudpException import *
from testConfig import *
from collections import OrderedDict
from sys import stdout, argv
from random import random, expovariate, gauss, randint

class SNDTerminal():
	def __init__(self):
		self.sndPeerList = []
		self.pktSentCount = (0, 0, 0) # min/avg/max

	def start(self):
		for i in range(MIN_SND_PORT_NUM, MIN_SND_PORT_NUM + MAX_SND_PEER):
			newSndPeer = rudpSocket(i)
			newSndPeer.pktCount = int(abs(gauss(AVG_SND_PKT_NUM, STD_SND_PKT_NUM)))
			# normal distribution
			self.sndPeerList.append(newSndPeer)

		while True:
			if len(self.sndPeerList) != 0:
				peerIdx = randint(0, len(self.sndPeerList) - 1)
				# uniform distribution
				if self.sndPeerList[peerIdx].pktCount == 0:
					self.sndPeerList.pop(peerIdx)
				else:
					self.sndPeerList[peerIdx].sendto(MAX_SND_PKT_DATA, (TARGET_PEER_IP, TARGET_PEER_PORT), True)
					self.sndPeerList[peerIdx].pktCount -= 1
					stdout.write('~')
					stdout.flush()
			else:
				break
			sleep(expovariate(AVG_SND_RATE))
			# exponential distribution.
		print 'Sending OK'

class RCVTerminal():
	def __init__(self):
		self.rcvPeerList = []

	def start(self):
		print '==> Creating {0} receiving peers'.format(MAX_RCV_PEER) 
		print '==> RCV Terminal @ {0}\n'.format(RCV_Terminal_IP)
		for i in range(MIN_RCV_PORT_NUM, MAX_RCV_PORT_NUM + 1):
			newRcvPeer = rudpSocket(i)
			self.rcvPeerList.append(newRcvPeer)

		while True:
			try:
				for i in range(0, len(self.rcvPeerList)):
					try: 
						recvData, addr = self.rcvPeerList[i].recvfrom()
						stdout.write('o')
						stdout.flush()
					except NO_RECV_DATA: continue
			except KeyboardInterrupt:
				return
			sleep(0)
							

class TargetPeer():	
	def __init__(self):
		self.pktCountDict = dict()
		self.destPortList = []
		self.targetPeer = rudpSocket(TARGET_PEER_PORT)

	def rcvLoop(self):
		while True:
			try: 
				recvData, addr = self.targetPeer.recvfrom()
				stdout.write('o')
				stdout.flush()
				sleep(0.0001)
			except NO_RECV_DATA: 
				stdout.write('.')
				stdout.flush()
				sleep(0.2)

	def sndLoop(self):
		while True:
			if len(self.destPortList) != 0:
				idx = randint(0, len(self.destPortList) - 1)
				# uniform distribution
				if self.pktCountDict[self.destPortList[idx]] == 0:
					self.pktCountDict.pop(self.destPortList[idx])
					self.destPortList.pop(idx)
				else:
					self.targetPeer.sendto(MAX_RCV_PKT_DATA, (RCV_Terminal_IP, self.destPortList[idx]), True)
					stdout.write('~')
					stdout.flush()
					self.pktCountDict[self.destPortList[idx]] -= 1
			else:
				for i in range(MIN_RCV_PORT_NUM, MIN_RCV_PORT_NUM + MAX_RCV_PEER):
					self.pktCountDict[i] = int(abs(gauss(AVG_RCV_PKT_NUM, STD_SND_PKT_NUM)))	
					# normal distribution.
					self.destPortList.append(i)
				#print 'Sending OK'
				#break
			sleep(expovariate(AVG_RCV_RATE))

	def start(self):
		spawn(self.rcvLoop)
		spawn(self.sndLoop)
		while True: sleep(0)

if len(argv) == 2:
	if int(argv[1]) == 1:
		s = SNDTerminal()
		s.start()
	elif int(argv[1])  == 2:
		r = RCVTerminal()
		r.start()
	elif int(argv[1])  == 3:
		t = TargetPeer()
		t.start()
else:
	rcvTerminal = RCVTerminal()
	sndTerminal = SNDTerminal()
	targetPeer  = TargetPeer()
	rcvTerminal.start()
	targetPeer.start()
	sndTerminal.start()

