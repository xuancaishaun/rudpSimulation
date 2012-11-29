from rudp import *
from rudpException import *
from testConfig import *
from collections import OrderedDict
from sys import stdout, argv
from random import random, expovariate, gauss, randint
from gevent import sleep


class rudpSocketDev(rudpSocket):
	def initPktCount(self, pktCount):
		self.pktCount = pktCount

	def sendtoDev(self, destAddr):
		if self.pktCount == 0:
			return False
		else:
			self.pktCount = self.pktCount - 1
			try:
				self.sendto(MAX_SND_PKT_DATA, destAddr, isReliable = True)
				return True
			except Exception as e:
				raise Exception
			#	print e.message

class SNDTerminal():
	def __init__(self):
		self.sndFreePortDict = OrderedDict()
		self.sndBusyPortDict = OrderedDict()
		for i in xrange(MIN_SND_PORT_NUM, MAX_SND_PORT_NUM):
			self.sndFreePortDict[str(i)] = 1	# 1 => dunmy value
		self.sndPeerList  = []

	def start(self):
		print '==> Creating {0} sending peers'.format(MAX_SND_PEER)
		while len(self.sndPeerList) < MAX_SND_PEER:
			try: (nextFreePort, nonsense) = self.sndFreePortDict.popitem(last = False)
			except KeyError:
				print '\t Error: no free port'

			newPeer = rudpSocketDev(int(nextFreePort))
			self.sndBusyPortDict[str(nextFreePort)] = 0	# add nextFreePort to sndBusyPortDict
			newPeer.portNum = nextFreePort
			newPeer.initPktCount(int(abs(gauss(AVG_RCV_PKT_NUM, STD_SND_PKT_NUM))))
			self.sndPeerList.append(newPeer)

		print '==> Start sending data to target peer'

		while True:
			peerToSendId = randint(0, len(self.sndPeerList) - 1)
			try: peerToSend = self.sndPeerList[peerToSendId]
			except IndexError:
				print '\t---> no peer to send'
				continue
			if not peerToSend.sendtoDev((TARGET_PEER_IP, TARGET_PEER_PORT)):
				# pktCount = 0 or sendto() failure
				# this peer has done its job
				self.sndPeerList.pop(peerToSendId)	###
				freedPort = peerToSend.portNum
				peerToSend.__del__()
				try: self.sndBusyPortDict.pop(freedPort);  ###
				except KeyError:
					print '\t Error: fail to free port'
				self.sndFreePortDict[str(freedPort)] = 1	###

				# Creat a new peer
				try: (nextFreePort, nonsense) = self.sndFreePortDict.popitem(last = False) ###
				except KeyError:
					print '\t Error: no free port'
				newPeer = rudpSocketDev(int(nextFreePort))
				self.sndBusyPortDict[str(nextFreePort)] = 0		###
				newPeer.portNum = nextFreePort
				newPeer.initPktCount(int(abs(gauss(AVG_RCV_PKT_NUM, STD_SND_PKT_NUM))))
				self.sndPeerList.append(newPeer)	###
			else: 
				print peerToSend.pktCount, peerToSend.notACKed
			sleep(3)


class RCVTerminal():
	def __init__(self):
		self.rcvPortDict = OrderedDict()
		for i in xrange(MIN_SND_PORT_NUM, MAX_SND_PORT_NUM):
			self.rcvPortDict[str(i)] = 1	# 1 => available port
		self.rcvPeerList = []

	def start(self):
		print '==> Creating {0} receiving peers from Port {1} to {2}'.format(MAX_RCV_PORT_NUM - MIN_RCV_PORT_NUM, MIN_RCV_PORT_NUM, MAX_RCV_PORT_NUM - 1) 
		print '==> RCV Terminal @ {0}\n'.format(RCV_Terminal_IP)
		while len(self.rcvPeerList) < (MAX_RCV_PORT_NUM - MIN_RCV_PORT_NUM):
			(nextPortNum, nonsense) = self.rcvPortDict.popitem(last = False)
			newPeer = rudpSocketDev(int(nextPortNum))
			self.rcvPeerList.append(newPeer)

		while True:
			try:
				for i in range(0, len(self.rcvPeerList)):
					try: 
						recvData, addr = self.rcvPeerList[i].recvfrom()
						stdout.write('o')
					except NO_RECV_DATA:
						pass
			except KeyboardInterrupt:
				return
				
				

class TargetPeer():	
	def __init__(self):
		self.destPortDict = OrderedDict()
		for i in xrange(MIN_SND_PORT_NUM, MAX_SND_PORT_NUM):
			self.destPortDict[str(i)] = 1	# 1 => dunmy value
		self.pktCountDict = OrderedDict()
		self.activePortList = []

	def start(self):
		targetPeer = rudpSocketDev(TARGET_PEER_PORT)
		while True:
			#if randint(0,1):  # 1 => recvfrom
			if 1:
				try: 
					recvData, addr = targetPeer.recvfrom()
					print len(recvData)
				except NO_RECV_DATA: 
					stdout.write('.')
					stdout.flush()
					sleep(0.5)
					continue
			else:
				stdout.write('~')
				stdout.flush()
				while True:
					if len(self.activePortList) < MAX_RCV_PEER:
						try: (nextDestPort, nonsense) = self.destPortDict.popitem(last = False)
						except KeyError: print '\t Error: fail to get next dest port'
						self.pktCountDict[str(nextDestPort)] = int(abs(gauss(AVG_RCV_PKT_NUM, STD_SND_PKT_NUM)))
						self.activePortList.append(nextDestPort)
						# no. of packets to send
						break
					else:
						activePortId = randint(0, len(self.activePortList) - 1)
						activePort = self.activePortList[activePortId]
						if self.pktCountDict[str(activePort)] > 0: 
							if targetPeer.sendto(MAX_RCV_PKT_DATA, (RCV_Terminal_IP, activePort), isReliable = True):
								self.pktCountDict[str(activePort)] -= 1
						else:
							# The peer has sent out all data to this port.
							self.destPortDict[str(activePort)] = 1
							self.activePortList.pop(activePort)
							self.pktCountDict.popitem(activePort)
						sleep(0.1)
						break
					


if len(argv) == 2:
	if int(argv[1]) == 1:
		r = RCVTerminal()
		r.start()
	elif int(argv[1])  == 2:
		s = SNDTerminal()
		s.start()
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

