#!/bin/bash
sudo docker run --network="split" --ip="10.0.10.5" --name "relay-receive" -v /home/kevin/apps/relay-receive/hostfiles:/data/hostfiles --privileged -i -t -p 3001:3001/udp --device /dev/blackmagic/io0 --entrypoint="/data/hostfiles/start-relay-receive.sh" pmw1/vlc