from simulationRudpUserDev import *
from sys import argv

c = rudpClient(int(argv[1]))
#c = rudpClient(50020);
if len(argv) == 3: dataSize = int(argv[2])
else: dataSize = 10000
data = 'o' * dataSize

try: c.connect(SERVER_IP, SERVER_PORT)
except MAX_RESND_FAIL:
	print 'Error: connection failure (MAX_RESND_FAIL)'
	exit()
except: exit()

try: c.sendData(data)
except MAX_RESND_FAIL:
	print 'Error: data transfer failure (MAX_RESND_FAIL)'
	exit()
except: exit()

try: c.close()
except:
	print 'Error: connection shutdown failure'
	exit()
