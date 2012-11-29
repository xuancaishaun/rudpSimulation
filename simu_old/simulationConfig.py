##############################
#			    ##
#    M-SC Configuration     ##
#			    ##
##############################

#SERVER_IP   	= '127.0.0.1' 		# Local Host
SERVER_IP  	= '137.189.97.35'  	# lab.neP2P.com
#SERVER_IP 	= '54.248.144.148' 	# AWS Ubuntu Server
SERVER_PORT 	= 39951			# 39951 - 40000
LOG_PORT    	= 39999
LOG_IP		= SERVER_IP
MAX_PKT_SIZE   	= 1000 			#  MAX_PKT_SIZE = MAX_DATA - 4 = 1000
MAX_BLOCK_SIZE 	= 1000000

##############################
#			    ##
#  Simulation Configuration ##
#			    ##
##############################

MEAN_INT_ARRIVAL= 5	# inver-arrival time between two clients
MEAN_JOB_SIZE 	= 10240	# average of data length = 15000 bytes, 15 packets if MAX_PKT_SIZE = 1000
STD_JOB_SIZE 	= 1024	# standard deviation of data length = 5000 bytes
BASE_PORT 	= 50020	# Port range: [BASE_PORT, BASE_PORT + MAX_PORT]
MAX_PORT 	= 1000 	# Max clients supported: MAX_PORT
