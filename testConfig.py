# Configuration for Sending Terminal
MAX_SND_PEER = 100

MIN_SND_PORT_NUM = 50001
MAX_SND_PORT_NUM = MIN_SND_PORT_NUM + 2*MAX_SND_PEER

MAX_SND_PKT_SIZE = 10240# in bytes => 10 KB, upper bound for packet size
AVG_SND_PKT_NUM  = 100	# Average no. of packets to send for each peer
STD_SND_PKT_NUM  = 50	# Standard deviation of no. of packets to send for each peer

AVG_SND_RATE = 100	# No. of packets sent per second;
			# Switching interval follows exponential distribution

'''
Readme for Sending Terminal

1. At most MAX_SND_PEER peers will send data concurrently to the target peer;
2. Each arriving peer will send a random no. of packets to the target peer;
   This number follows normal distribution with AVG_PKT_NUM and STD_PKT_NUM;
   Each packet has a size of MAX_PKT_SIZE bytes;
3. The terminal will uniformly pick one peer to send one packet to the target;
   The switching interval follows exponential distribution with AVG_SND_RATE;
4. If a peer uses up its packet quota, it will be removed from the list and
   a new peer is added to the list;

'''

# Configuration for The Target Peer
MAX_RCV_PEER = 100

MIN_RCV_PORT_NUM = 60001
MAX_RCV_PORT_NUM = MIN_RCV_PORT_NUM + 2*MAX_RCV_PEER

MAX_RCV_PKT_SIZE = 10240
AVG_RCV_PKT_NUM  = 100
STD_SND_PKT_NUM  = 50

AVG_RCV_RATE = 100

'''
Readme for The Target Peer

1. The peer switch between sendto() and recvfrom() randomly;
2. The peer behaves similar to Sending Terminal

Others:

For Receiving Terminal, it just needs to create peers binded to
[MIN_RCV_PORT_NUM, MAX_RCV_PORT_NUM]

'''