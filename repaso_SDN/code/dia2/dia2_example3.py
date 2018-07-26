#!/usr/bin/python
'''

Topologia:

   h1 --- s1 --- h2


sudo python dia2_example3.py 

Controlador: 
sudo docker run --name c0 -p 6653:6653 -it --rm osrg/ryu /bin/bash

Ya una vez dentro del contenedor:

cd ryu
ryu-manager --ofp-tcp-listen-port 6653 ryu/app/simple_switch.py


Otros comandos:

tigarto@fuck-pc:~/Documents/test_diarios_tesis/abril18/test1$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:172.17.0.2:6653"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
    ovs_version: "2.5.4"


CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                    NAMES
85ea942326f6        osrg/ryu            "/bin/bash"         About a minute ago   Up About a minute   0.0.0.0:6653->6653/tcp   c0

sudo docker container inspect c0
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



