#!/usr/bin/python
'''

Topologia:

   h1 --- s1 --- h2


sudo python dia3_example1.py 

Controlador: 

sudo docker run -it --name onos1 --rm onosproject/onos bash

Ya una vez dentro del contenedor:

app activate org.onosproject.openflow
app activate org.onosproject.fwd
apps -a -s

'''


from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.net import Containernet
from mininet.log import info, setLogLevel

import os

setLogLevel('info')

info('*** Create the controller \n')
c0 = RemoteController('c0', ip = "172.17.0.2", port = 6653)
info(c0)
"Create Simple topology example."
net = Containernet(build=False)
# Initialize topology
 
# Add containers
info('*** Adding docker containers using openswitch/ubuntuscapy images\n')
h1 = net.addDocker('h1', ip='10.0.0.251', dimage="openswitch/ubuntuscapy")
h2 = net.addDocker('h2', ip='10.0.0.252', dimage="openswitch/ubuntuscapy")

# Add switches    
info('*** Adding switches\n')
s1 = net.addSwitch('s1')

# Add links    
info('*** Creating links\n')
net.addLink( h1, s1 )
net.addLink( h2, s1 )
net.addController(c0)

# Build the network
info('*** Build the network\n')
net.build()
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()



