#!/usr/bin/python
"""Custom topology example

---------------------------------------------------------------------------------------------
Test sin controlador:

Topologia:

   h1 --- s1 --- h2

sudo mn --custom dia2_example2.py --topo mytopo --mac



Otros comandos:

containernet > pingall


tigarto@fuck-pc:~/Documents/test_diarios_tesis/abril18/test1$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "ptcp:6634"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: secure
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
    ovs_version: "2.5.4"

---------------------------------------------------------------------------------------------
Test con controlador:

Plantilla


Topologia:

sudo mn --custom dia2_example2.py --topo mytopo --mac \
        --controller=remote,ip=127.0.0.1,port=6633

Controlador:

./pox.py log.level --DEBUG forwarding.l2_learning

El comando anterior se baso en: sudo mn --controller=remote,ip=[controller IP],port=[controller listening port]

Otros comandos:

tigarto@fuck-pc:~/Documents/test_diarios_tesis/abril18/test1$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "ptcp:6634"
        Controller "tcp:127.0.0.1:6633"
            is_connected: true
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth1"
            Interface "s1-eth1"
    ovs_version: "2.5.4"
"""

from mininet.topo import Topo

class MyTopo( Topo ):
  "Simple topology example."
  def __init__( self ):
    "Create custom topo."

    # Initialize topology
    Topo.__init__( self )

    # Add hosts and switches
    h1 = self.addHost( 'h1' )
    h2 = self.addHost( 'h2' )
    s1 = self.addSwitch( 's1' )

    # Add links
    self.addLink( h1, s1 )
    self.addLink( h2, s1 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
