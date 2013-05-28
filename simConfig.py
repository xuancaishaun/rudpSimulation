hostnames = [
	"ricepl-1.cs.rice.edu",
	"planet3.cs.ucsb.edu",
	#"planetlab-01.vt.nodes.planet-lab.org",
	#"planetlab2-santiago.lan.redclara.net"
	"planetlab2.cs.uoregon.edu",
	"planetlab01.alucloud.com"
]
hosts = [
	"128.42.142.41",
	"128.111.52.63",
	#"198.82.160.238",
	#"200.0.206.203"
	"128.223.8.112",
	"135.109.221.103"
]

#We use the first two hosts
hosts = hosts[:4]

# Specific port for both sending and receiving data
PEER_PORT = 39940

# Inter-sending interval for a peer
# E.g. 
VAR_SEND_INT = 100	# gamma; exponential distri.

# Prob. of sending reliable messages
VAR_SEND_REL = 0.2	# uniform distri.

# Message size follows normal distri.
# E.g. int(abs(gauss( average, std. )))
VAR_MSG_AVG = 1024
VAR_MSG_STD = 100

# Flag for output printing 
OUTPUT_CLEAN = True 

# Local testing
LOCAL_TEST = False
LOCAL_PEER_NUM = 4
