#!/usr/bin/python3

import sys
import random
import os

user=os.getlogin()









#####################################################################################
########################  PARSE ARGUEMENTS INTO VARIABLES ###########################
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--mode', '-m', help="Set vlc mode (udp/rtp)")
	parser.add_argument('--caching', '-c', help="Set manual network caching in miliseconds")
	parser.add_argument('--port', '-p', help="Set listening port")
	parser.add_argument('--force', '-f', help="Force kill other direct-send container before starting")
	parser.add_argument('--destroy', '-d', help="Destroy direct-send container")

	## Replicate above line to add more optional input arguments
	
	args = parser.parse_args()
	print()
	print("Mode set   : ", args.mode)
	print("Cashing set: ", args.caching, "ms")
	mode=args.mode
	caching=args.caching
	port=args.port
	force=args.force
	destroy=args.destroy
#####################################################################################
########################  END PARSE ARGUEMENTS INTO VARIABLES #######################














#####################################################################################
############################# BUILD CVLC RUN COMMAND ################################

def buildCvlcLauncher():
	print('*** building \"hostfiles/start-relay-receive.sh"  function -- running ***')
	import stat
	## open file for writing
	direct_recevie_file = open("hostfiles/start-relay-receive.sh", "wb")
	direct_recevie_file.write(bytes("#!/bin/bash\n", 'UTF-8'))
	direct_recevie_file.write(bytes("cvlc {}://@:{} ".format(mode, port), 'UTF-8'))
	direct_recevie_file.write(bytes("-I dummy ", 'UTF-8'))
	direct_recevie_file.write(bytes("--ignore-config ", 'UTF-8'))
	direct_recevie_file.write(bytes("--network-caching=" + caching + " ", 'UTF-8'))
	direct_recevie_file.write(bytes("--decklink-vout-video-connection sdi ", 'UTF-8'))
	direct_recevie_file.write(bytes("--decklink-mode Hi59 ", 'UTF-8'))
	direct_recevie_file.write(bytes("--decklink-aspect-ratio=16:9 ", 'UTF-8'))
	direct_recevie_file.write(bytes("-V decklinkoutput ", 'UTF-8'))
	direct_recevie_file.write(bytes("-A decklinkoutput ", 'UTF-8'))
	direct_recevie_file.write(bytes("--decklink-vout-mode Hi59 ", 'UTF-8'))
	##direct_recevie_file.write(bytes("--decklink-aout-audio-rate 48000 ", 'UTF-8'))
	##direct_recevie_file.write(bytes("--decklink-aout-audio-channels 2", 'UTF-8'))

	direct_recevie_file.close()

#####################################################################################
############################# END BUILD CVLC RUN COMMAND ############################













#####################################################################################
#############################    BUILD DOCKER LAUNCHER    ###########################

def dockerLauncher():
	print('*** building \"hostfiles/start-docker.sh"  function -- running ***')

	import subprocess
	import stat
	## open file for writing
	start_docker_file = open("hostfiles/start-docker.sh", "wb")
	start_docker_file.write(bytes("#!/bin/bash\n", 'UTF-8'))
	start_docker_file.write(bytes("sudo docker run ", 'UTF-8'))
	start_docker_file.write(bytes("--network=\"split\" ", 'UTF-8'))
	start_docker_file.write(bytes("--ip=\"10.0.10.5\" ", 'UTF-8'))
	start_docker_file.write(bytes("--name \"relay-receive\" ", 'UTF-8'))
	start_docker_file.write(bytes("-v /home/" + user +"/apps/relay-receive/hostfiles:/data/hostfiles ", 'UTF-8'))
	start_docker_file.write(bytes("--privileged -i -t ", 'UTF-8'))
	start_docker_file.write(bytes("-p {}:{}/udp ".format(port, port), 'UTF-8'))
	start_docker_file.write(bytes("--device /dev/blackmagic/io0 ", 'UTF-8'))
	start_docker_file.write(bytes("--entrypoint=\"/data/hostfiles/start-relay-receive.sh\" ", 'UTF-8'))
	start_docker_file.write(bytes("pmw1/vlc", 'UTF-8'))

	start_docker_file.close()

	os.chmod('hostfiles/start-docker.sh', stat.S_IXOTH)
	proc = subprocess.Popen('sudo hostfiles/start-docker.sh', shell=True)

#####################################################################################
############################# END BUILD DOCKER LAUNCHER ############################


def testDestroyOption():
	if(destroy=='1'):
		print("Existing Relay Receive Container DESTROYED !!!")
		bashCommand="sudo docker rm -f relay-receive"
		os.system(bashCommand)
		quit()


def testForceOption():
	if(force=='1'):
		print("Forcing shutdown of running relay receive container")
		bashCommand="sudo docker rm -f relay-receive"
		os.system(bashCommand)




#####################################################################################

#####################################################################################

#####################################################################################

						#END DEFINITIONS AND BEGIN SCRINT##

#####################################################################################

#####################################################################################

#####################################################################################


testDestroyOption()
testForceOption()


buildCvlcLauncher()
dockerLauncher()


