#-------------------------------------#
#   2012 - 2013 Final Year Project    #
#   NeP2P                             #
#   Task1.1: RUDP Server-N:Clients    #
#   YIN  MING  : IE / 5, CUHK         #
#   YING XUHANG: IE / 4, CUHK         #
#-------------------------------------#
#   Client & Server Dev Module        #
#-------------------------------------#

from rudp import *
from time import sleep, time
from threading import Timer
from random import random
from os import stat
from math import ceil
from json import dumps as jsonEncode
from sys import stdout
from simulationConfig import *

TIME_CHECK_PERIOD = 3
strTime = time()
pktNum  = 0

def checkTimeOut(conns):
	global pktNum
	conNum = len(conns)
	curTime   = time()
	print '\nOnline C:', conNum, 'time:', curTime - strTime , 'sec', 'pktNum:', pktNum
	pktNum = 0
	for k in conns.keys():
		if curTime - conns[k].time > END_WAIT:
			del conns[k]
			stdout.write('x ')
			stdout.flush()
	t = Timer(TIME_CHECK_PERIOD, checkTimeOut, [conns])
	t.daemon = True
	t.start()

class rudpServer:
	def __init__(self, srcPort):
		self.skt = socket(AF_INET, SOCK_DGRAM) #UDP
		self.skt.bind(('', srcPort)) #used for recv
		self.conns = {}
		self.strTime = time()
		
	def __del__(self):
		self.skt.close()

	def start(self):
		global pktNum
		checkTimeOut(self.conns)
		while True:
			recvData, addr = self.skt.recvfrom(MAX_DATA)
			pktNum += 1
			try:
				recvPkt = decode(recvData)
				try:
					c = self.conns[addr]
				except KeyError:
					if recvPkt['pktType'] == SYN:
						c = rudpConnection(addr, False)
						self.conns[addr] = c
					else: continue
				sendPkt = rudpProcessSwitch[recvPkt['pktType']](recvPkt, c)
			except: continue
			else:
				self.skt.sendto(encode(sendPkt), addr)
				if sendPkt['pktType'] == FIN_ACK: 
					del self.conns[addr]
					stdout.write('o ')
					stdout.flush()

class logClient:
	def __init__(self, srcAddr, desAddr, logAddr):
		self.logAddr   = logAddr
		self.srcAddr   = srcAddr
		self.desAddr   = desAddr

		self.pktSend   = 0
		self.pktReSend = 0
		self.pktRecv   = 0
		self.bytSend   = 0
		self.bytReSend = 0
		
		self.strTimePt = 0
		self.endTimePt = 0
		self.special   = []
		self.status    = False

	def printLog(self):
		print self.srcAddr, '<=>', self.desAddr
		print '\tstrTimePt :', self.strTimePt
		print '\tendTimePt :', self.endTimePt
		print '\tlogAddr   :', self.logAddr
		print '\tpktSend   :', self.pktSend
		print '\tpktReSend :', self.pktReSend
		print '\tpktRecv   :', self.pktRecv
		print '\tbytSend   :', self.bytSend
		print '\tbytReSend :', self.bytReSend
		for s in self.special:
			print '\tSpecial Event:', s
		print 'status: [', self.status, ']'

	#def printShortLong(self):
        #       print 'Client at {}:'.format(self.srcAddr)
        #       pass
                #print 'time={}'.format((self.endTime-self.))

	def convertDic(self):
		dic = {
			'srcAddr'  : self.srcAddr,
			'desAddr'  : self.desAddr,
			'pktSend'  : self.pktSend,
			'pktReSend': self.pktReSend,
			'pktRecv'  : self.pktRecv,
			'bytSend'  : self.pktSend,
			'bytReSend': self.bytReSend,
			'strTimePt': self.strTimePt,
			'endTimePt': self.endTimePt,
			'special'  : self.special,
			'status'   : self.status
		}
		return dic

	def sendLog(self, skt):
		self.endTimePt = time()
		#self.printLog()
		skt.sendto(jsonEncode(self.convertDic()), self.logAddr)

class rudpClient:
	def __init__(self, srcPort, logAddr = (LOG_IP, LOG_PORT)):
		self.skt = socket(AF_INET, SOCK_DGRAM) #UDP
		self.skt.bind(('', srcPort)) #used for recv
		self.log = logClient(self.skt.getsockname(), None, logAddr)
	
	def __del__(self):
		self.skt.close()

	def srs(self, sendPkt): #sendPkt --> recvPkt --> sendPkt		
		isReSend = False

		for i in xrange(MAX_RESND):
			try:
				if isReSend:
					dataSent = self.skt.sendto(encode(sendPkt), self.conn.destAddr)
					self.log.bytSend += dataSent
					self.log.bytReSend += dataSent
					self.log.pktSend += 1
					self.log.pktReSend += 1
				else:
					self.log.bytSend += self.skt.sendto(encode(sendPkt), self.conn.destAddr)
					self.log.pktSend += 1
				while True:
					recvData, addr = self.skt.recvfrom(MAX_DATA)
					self.log.pktRecv += 1
					try:
						recvPkt = decode(recvData)
						return rudpProcessSwitch[recvPkt['pktType']](recvPkt, self.conn)
					except WRONG_PKT:
						self.log.special.append('Wrong packet')
						continue
					except KeyError:
						self.log.special.append('Invalid packet type')
						continue
			except timeout:
				self.log.special.append('Timeout in connect()')
				isReSend = True
				continue
		self.log.special.append('Resend 3 times')
		raise MAX_RESND_FAIL()

	def connect(self, destIP = SERVER_IP, destPort = SERVER_PORT):
		self.conn = rudpConnection(None, True)
		self.conn.destAddr = (destIP, destPort)

		self.log.desAddr = self.conn.destAddr
		self.log.strTimePt = time()

		self.skt.settimeout(RTO)
		try:
			self.srs( rudpPacket(SYN, self.conn.pktId) )
		except:
			print 'fail'
			self.log.sendLog(self.skt)
			return False
		return True
	
	def sendData(self, data):
		# Compute total size of data and prepare data packets to be sent
		total_pkt = int(ceil(len(data)/float(MAX_PKT_SIZE)))
		data_pkt = range(total_pkt)
		for i in xrange(0, total_pkt, 1):
			data_pkt[i] = data[i*MAX_PKT_SIZE : (i+1)*MAX_PKT_SIZE]
			
		# [HandShaking] - Done
		# [Data-Delivery]
		sendPkt = rudpPacket(DAT, self.conn.pktId)
		for i in xrange(0, len(data_pkt), 1):
			sendPkt['data'] = data_pkt[i]
			try:
				sendPkt = self.srs( sendPkt )
			except Exception as e:
				self.log.sendLog(self.skt)
				return False
		return True

	def close(self):
		# [Shutdown]
		sendPkt = rudpPacket(FIN, self.conn.pktId)
		self.conn.wait = FIN_ACK
		try:
			self.srs( sendPkt )
		except END_CONNECTION:
			self.log.status = True
			self.log.sendLog(self.skt)
			del self.conn
			return True
		except Exception as e:
			print e.message
			self.log.sendLog(self.skt)
			return False
		
	def sendFile(self, filepath):
		# Read form file block by block
		# Block size is the size of data that can be sent by calling sendData() every time
		
		fileSize = stat(filepath).st_size
		numOfBlocks = int(ceil(fileSize / float(MAX_BLOCK_SIZE)))

		infile = open(filepath, 'r')
		infile.seek(0)

		for i in xrange(0, numOfBlocks, 1):
			try:
				dataBlock = infile.read(MAX_BLOCK_SIZE)
				if self.sendData(dataBlock): continue
			except Exception as e:
				print e.message
				return False
		infile.close()
		return True
