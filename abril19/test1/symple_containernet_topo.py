#!/usr/bin/python
'''

Topologia:

   h1 --- s1 --- h2


sudo python symple_containernet_topo.py 

Controlador: 
./pox.py log.level --DEBUG openflow.of_01 --port=6653 forwarding.l2_learning 

Otros comandos:

tigarto@fuck-pc:~/Documents/test_diarios_tesis/abril18/test1$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
        fail_mode: secure
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
    ovs_version: "2.5.4"


tigarto@fuck-pc:~/pox$ sudo docker container ls
CONTAINER ID        IMAGE                    COMMAND             CREATED             STATUS              PORTS               NAMES
2f5e5333d738        openswitch/ubuntuscapy   "/bin/bash"         4 minutes ago       Up 4 minutes                            mn.h2
90131fdbdc02        openswitch/ubuntuscapy   "/bin/bash"         4 minutes ago       Up 4 minutes                            mn.h1

'''


from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.net import Containernet
from mininet.log import info, setLogLevel

import os

setLogLevel('info')

info('*** Create the controller \n')
c0 = RemoteController('c0',port = 6653)
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



