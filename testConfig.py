#===============================================================================
# Necessary configs:
TARGET_PEER_PORT = 39951
TARGET_PEER_IP   = '137.189.97.35'



#================================================================================
# Configuration for Sending Terminal
MAX_SND_PEER = 10

MIN_SND_PORT_NUM = 50500
MAX_SND_PORT_NUM = MIN_SND_PORT_NUM + 2 * MAX_SND_PEER

MAX_SND_PKT_DATA = 'o' * 1000# in bytes => 10 KB, upper bound for packet size
AVG_SND_PKT_NUM  = 100	# Average no. of packets to send for each peer
STD_SND_PKT_NUM  = 50	# Standard deviation of no. of packets to send for each peer

AVG_SND_RATE = 5	# No. of packets sent per second;
			# Switching interval follows exponential distribution

# Configuration for The Target Peer
#TARGET_PEER_PORT = 39951
#TARGET_PEER_IP	 = '137.189.97.35'
#TARGET_PEER_IP	 = '137.189.97.35'

#RCV_Terminal_IP = '54.248.144.148'
RCV_Terminal_IP = '127.0.0.1'
MAX_RCV_PEER 	 = 1

MIN_RCV_PORT_NUM = 40001
MAX_RCV_PORT_NUM = MIN_RCV_PORT_NUM + 2 * MAX_RCV_PEER

MAX_RCV_PKT_DATA = '*' * 10240
AVG_RCV_PKT_NUM  = 100
STD_SND_PKT_NUM  = 50

AVG_RCV_RATE = 50

'''
Readme for The Target Peer

1. The peer switch between sendto() and recvfrom() randomly;
2. The peer behaves similar to Sending Terminal

Others:

For Receiving Terminal, it just needs to create peers binded to
[MIN_RCV_PORT_NUM, MAX_RCV_PORT_NUM]

'''
