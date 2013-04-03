#RUDY lib
from rudp import *
from rudpException import *
#Config lib
from simConfig import *
from socket import gethostname, gethostbyname
#Python lib
from sys import stdout
from random import random, expovariate, gauss, randint, sample

hosts.remove(gethostbyname(gethostname()))
hostLength = len(hosts)

print hostLength, hosts

class rudpPeer():
	def __init__(self):
		self.destList = [(hostname, PEER_PORT) for hostname in hosts]
		self.socket = rudpSocket(PEER_PORT)

	def rcvLoop(self):
		while True:
			try:
				recvData, addr = self.socket.recvfrom(False)
				if not OUTPUT_CLEAN:
					stdout.write('o')
					stdout.flush()
				else:
					print 'recvData'
				sleep(0)
			except NO_RECV_DATA:
				if not OUTPUT_CLEAN:
					stdout.write('.')
					stdout.flush()
				else:
					print 'noData'
				sleep(0.001)

	def sndLoop(self):
		global hostLength
		while True:
			for addr in self.socket.failed:
				if addr in self.destList:
					self.destList.remove(addr)
					hostLength -= 1
				print '\none destination failed', addr
			self.socket.failed = []
			if hostLength == 0:
				print '\nno host to send'
				break
			dests = sample( self.destList, randint(1, hostLength) )
			for dest in dests:
				self.socket.sendto( 'o' * int(abs(gauss(VAR_MSG_AVG, VAR_MSG_STD))), dest, random() < VAR_SEND_REL)
				if not OUTPUT_CLEAN:
					stdout.write('~')
					stdout.flush()
				else:
					print 'sendData'
			sleep( expovariate(VAR_SEND_INT) )

	def start(self):
		spawn(self.rcvLoop)
		spawn(self.sndLoop)
		while True: sleep(0) 

try:
	peer = rudpPeer()
	peer.start()
except:
	del peer
