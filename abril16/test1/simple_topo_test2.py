#!/usr/bin/python

"""
Antes de correr tener instaladas las imagenes:

sudo docker pull openswitch/ubuntuscapy



This example shows how to create a simple network and how to create docker containers (based on existing images) to it.
Two directly connected switches plus a host for each switch:
          c0
          |
          |
   A --- s1 --- V
         
Use: sudo python simple_topo_containers.py 
"""

from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link


def topology():
    "Create a network with some docker containers acting as hosts."

    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')   

    info('*** Adding docker containers\n')
    
    # Containers de imagenes con herramientas de red 
    A = net.addDocker('A', ip='10.0.0.100', dimage="openswitch/ubuntuscapy", volumes=["/home/tigarto/Documents/test_diarios_tesis/abril16/test1/trazas:/mnt/trazas:rw"])
    V = net.addDocker('V', ip='10.0.0.101', dimage="openswitch/ubuntuscapy") 


    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    

    info('*** Creating links\n')
    net.addLink(A, s1)
    net.addLink(s1, V)
    

    info('*** Starting network\n')
    net.start()
    
    info('***Testing network connectivity***')
    net.pingAll()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
