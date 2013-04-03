#Fabric lib
from fabric.api import env, run, local
#Python lib
from time import sleep
#Local lib
from simConfig import *

env.user = 'cuhk_inc_01'
env.key_filename = '~/.ssh/PlanetLabKey'

env.hosts = hosts
path = '~/Dropbox/PythonServer/rudpSimulation/'

def start():
	run('python ' + path + 'simStart.py')
	