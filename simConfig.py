hostnames = [
	'planetlab4.williams.edu',
	'planetlab2.fri.uni-lj.si', 
	'planetlab2-santiago.lan.redclara.net', 
	'plab3.eece.ksu.edu', 
	'planetlab-3.cmcl.cs.cmu.edu', 
	'planet-lab2.itba.edu.ar', 
	'pl02.comp.polyu.edu.hk'
]
hosts = [
	'137.165.1.114', 
	'212.235.189.115', 
	'200.0.206.203', 
	'129.130.252.140', 
	'128.2.211.115', 
	'190.227.163.141', 
	'202.125.215.12'
]

#We use the first two hosts
hosts = hosts[:2]

# Specific port for both sending and receiving data
PEER_PORT = 39951

# Inter-sending interval for a peer
# E.g. 
VAR_SEND_INT = 100	# gamma; exponential distri.

# Prob. of sending reliable messages
VAR_SEND_REL = 0.7	# uniform distri.

# Message size follows normal distri.
# E.g. int(abs(gauss( average, std. )))
VAR_MSG_AVG = 1024
VAR_MSG_STD = 100

# Flag for output printing 
OUTPUT_CLEAN = True 

# Local testing
LOCAL_TEST = False
LOCAL_PEER_NUM = 4