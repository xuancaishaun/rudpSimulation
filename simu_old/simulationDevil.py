from simulationRudpUserDev import *
from sys import argv
from random import randint
from time import sleep
from simulationConfig import *
#argv - pure random
#1: pktNumLimit - Default:10
#2: pktInterval - Default:1p/s - 0 for inf
argc = len(argv)
pktNumLimit = 10
pktInterval = 1
if argc >= 2:
	pktNumLimit = int(argv[1])
	if argc >= 3:
		pktInterval = int(argv[2]) 
print 'Devil:', pktNumLimit, 'packets', pktInterval, 's'

PACKET_TYPE_LIST = [SYN, ACK, FIN, DAT, SYN_ACK, FIN_ACK]

def randomPacket(pktType = None, pktId = None, pktData = None):
	pktType = pktType if pktType else PACKET_TYPE_LIST[randint(0, 5)]
	pktId   = pktId   if pktId   else randint(0, 10000)
	pktData = pktData if pktData and pktType == DAT else ''
	return rudpPacket(pktType, pktId, pktData)


c = rudpClient(30303)
serverAddr = (SERVER_IP, SERVER_PORT)

for i in xrange(pktNumLimit):
	pkt = randomPacket()
	print i,':',pkt
	c.skt.sendto(encode(pkt), serverAddr)
	if pktInterval: sleep(pktInterval)
