# Apuntes de repaso

# Dia 1

## Fecha: 24/07/2018

## Sobre mininet (contanernet)

### Opciones mininet ###

1. **\-x, --xterm**: Inicia una terminal xterm para cada host y cada switch
2. **--link=LINK**: Comando que permite fijar los parámetros del enlace tales como ancho de banda (bw) y retardo entre otros (delay).
3. **--test=TEST**: Este comando permite llevar a cabo test de regresión. Estos test, permiten llevar a cabo pruebas sin necesidad de usar el CLI de mininet.
4. **--topo=TOPO**: Permite especificar la topología mininet. Opciones preconstruidas: minimal, N - reversed, N - linear, N - Topo, N, M
5. **--switch=SWITCH**: Define el switch que será usado. Por default, el switch OVSK será el empleado.
6. **--controller=CONTROLER**: Define el controlador que será usado. Si no se especifica nada el controlador por defecto es usado con un comportamiento por defecto como hub.
7. **--version**: Muestra la versión del mininet

**Ejemplos de uso**

sudo mn --mac --topo single,3 --switch OVSK


Llamando la topologia desde un script:

sudo python archivo_topologia.py
sudo mn --custom /home/mininet/Documents/ejemplos_mininet/topo_2h_2s.py --topo mytopo
–test pingall


**Otras utilidades**

dpctl [OPTIONS] SWITCH COMMAND [ARG...]

dpctl -h
man dpctl

1. **show**: El comando show se conecta el switch y muestra el estado del puerto y capacidades.

```
dpctl show SWITCH
```

Ejemplo:

```
dpctl show tcp:127.0.0.1:6634
```

2. **dump-flows** El comando dump-flows muestra todos las entradas de flujo.

```
dpctl dump-flows SWITCH
```

Ejemplo:

```
dpctl dump-flows tcp:127.0.0.1:6634
```

2. **dump-ports**: Da información física y estadísticas del puerto como contadores de Tx, Rx y Error counters.

```
dpctl dump-ports SWITCH
```

Ejemplo:

```
dpctl dump-ports tcp:127.0.0.1:6634
```

4. **mod-ports**: Modifica el comportamiento de puertos. Posibles comandos son: Up, Down, Flood, Noflood.

```
dpctl mod-port SWITCH IFACE ACT
```

Ejemplo:

```
dpctl mod-ports tcp:127.0.0.1:6634
dpctl mod-ports tcp:127.0.0.1:6634 2 Up
```

5. **add-flow**: Permite agregar un flujo por medio de (1) la descripción de este en el comando o desde un (2) archivo.

* Desde el comando:

```
dpctl add-flow SWITCH FLOW
```

* Desde un archivo:

```
dpctl add-flow SWITCH FILE
```

Ejemplo:

```
dpctl add-flow tcp:127.0.0.1:6634 in_port=1,actions=output:2
```
6. **show-protostat**: Reporta las estadísticas de un protocolo 

```
dpctl show_protostat SWITCH
```

Ejemplo:

```
dpctl show_protostat tcp:127.0.0.1:6634
```

## Sobre POX ###

**Modo de uso**:

```
./pox [OPTIONS] [comp1] [args_comp1] ... [compN] [args_compN]
```

**Donde**:
* **./pox**: Comando para invocar el contrador POX.
* **[OPTIONS]**: Opciones del controlador -verbose, --no-cli, --no-openflow
* **[comp1,..., comN]**: Componentes que seran cargados al ejecutar el controlador.
* **[Args_comp1,..., args_compN]**: Opciones del componente que sera cargado en OpenFlow.

**Algunos ejemplos**:
* ./pox --no-cli forwarding.l2_learning
* ./pox --no-cli forwarding.l2_learning web.webcore
* ./pox --no-cli forwarding.l2_learning --transparent web.webcore --port=8888

Meta las cosas dentro de la carpeta ext de pox.

### Pasos para la creación de un componente propio en POX ###

1. Es necesario importar como mínimo el core.

```python
# Importanto las librerias necesarias

from pox.core import core

...
```

2. Esta parte consiste en implementar la lógica asociada al componente. La comunicación entre el Switch (S) y el Controlador (C) es la que determina lo que hace el código (lógica del componente):
  * C -> S: El código implementado código envía un mensaje.
  * S -> C: Se genera un evento el cual es manejado por el handler asociado. Generalmente hay un evento correspondiente a cada tipo de mensaje (como se vio previamente).

**Forma 1**: Desde la función launch() empleando la función addListenerByName().

```python
def lauch():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
```

**Forma 2**: Desde el init de una clase a través de la función addListeners().

```python
class MyComponent(object):
  def __init__ (self):
    core.openflow.addListeners(self)
    
  # Despues de esto se implementan todos los handlers a manejar ...
  ...

def lauch():
  core.registerNew(MyComponent)
```

3. Implementacion de la logica:
  * Una vez que los eventos son registrados (paso anterior), el siguiente paso consistirá en agregar las funciones manejadoras (handlers).
  * Los handlers se encargarán de analizar los paquetes e implementar las acciones (lógica de control) que llevará a cabo el componente.

```python
def lauch():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
```

Del fragmento de codigo anterior tenemos 3 handlers los cuales son:
* **_handle_ConnectionUp**: Asociado al evento ConnectionUp
* **_handle_ConnectionDown**: Asociado al evento ConnectionDown
* **_handle_PacketIn**: Asociado al evento PacketIn

Tal y como en el caso anterior, la implementacion de los manejadores se
hará de dos formas:

**Forma 1**: Como funciones, si los listeners se registraron en el launch.

```python
def _handle_ConnectionUp (self, event):
  # logica _handle_ConnectionUp
  log.debug("Switch %s arriba", dpid_to_str(event.dpid))
  ...

def _handle_ConnectionDown(self, event):
  # logica _handle_ConnectionDown
  log.debug("Switch %s abajo", dpid_to_str(event.dpid))
  ...

def _handle_PacketIn (event):
  # logica _handle_PacketIn
  packet = event.parsed
  ...
```
**Forma 2**: Como funciones de la clase, si los listers se registraron en el init de
la clase creada.

```python
class MyComponent(object):
  def __init__ (self):
    core.openflow.addListeners(self)
    # Despues de esto se implementan todos los handlers a manejar ...
    ...
    
  def _handle_ConnectionUp(self, event):
    # logica _handle_ConnectionUp
    log.debug("Switch %s arriba", dpid_to_str(event.dpid))
    ...
  
  def _handle_ConnectionDown(self, event):
    # logica _handle_ConnectionDown
    log.debug("Switch %s abajo", dpid_to_str(event.dpid))
    ...
  
  def _handle_PacketIn (event):
    # logica _handle_PacketIn
    packet = event.parsed
    dst_port = table.get(packet.dst)
    ....

```

Resumiendo todo lo anterior para un caso particular de codigo:

**Caso en el que no se usa POO**

```python
from pox.core import core

def _handle_ConnectionUp (self, event):
  log.debug("Switch %s arriba", dpid_to_str(event.dpid))

def _handle_ConnectionDown(self, event):
  log.debug("Switch %s abajo", dpid_to_str(event.dpid))

def _handle_PacketIn (event):
  packet = event.parsed
  msg = of.ofp_flow_mod()
  msg.match.dl_src = packet.src
  msg.match.dl_dst = packet.dst
  msg.actions.append(of.ofp_action_output(port = dst_port))
  event.connection.send(msg)

def lauch():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("ConnectionDown", _handle_ConnectionDown)
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
```

**Caso en el que se usa POO**
```python

from pox.core import core

class MyComponent(object):
  def __init__ (self):
    core.openflow.addListeners(self)
    # Despues de esto se implementan todos los handlers a manejar ...
  
  def _handle_ConnectionUp(self, event):
    log.debug("Switch %s arriba", dpid_to_str(event.dpid))
    
  def _handle_ConnectionDown(self, event):
    log.debug("Switch %s abajo", dpid_to_str(event.dpid))

  def _handle_PacketIn (event):
    packet = event.parsed
    dst_port = table.get(packet.dst)
    msg = of.ofp_flow_mod()
    msg.match.dl_src = packet.src
    msg.match.dl_dst = packet.dst
    msg.actions.append(of.ofp_action_output(port = dst_port))
    self.connection.send(msg)

  def lauch():
    core.registerNew(MyComponent)
```

Tenga en cuenta lo anterior para despues.

# Ejemplos

### Ejemplo 1: ### 

Ejecución de un comando sencillo que monta una topologia single con 2 host:

```
sudo mn
```

Comandos ejecutados en la consola de mininet:


```
net
nodes
links
xterm c0 s1 h1 h2
py h1.cmd('ifconfig')
py h2.cmd('ifconfig')
py s1.cmd('ifconfig')
py c0.cmd('ifconfig')

```

h1 --> h1-eth0: 10.0.0.1/8
   ---> lo: 127.0.0.1/8

h2 --> h2-eth0: 10.0.0.2/8
   ---> lo: 127.0.0.1/8

c0 --> lo: 127.0.0.1/8

s1 --> lo: 127.0.0.1/8

s1-eth2: ?? --> IPv6: fe80::8dc:b3ff:fe16:5099/64
s1-eth1: ?? --> IPv6: fe80::3882:b9ff:fe03:332a/64

Al dar uso con el comando IP en containernet vemos que todo se reduce al localhost tanto para el controlador como para el switch:

```
containernet> py s1.IP
<bound method OVSSwitch.IP of <OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=13561> >

containernet> py s1.IP()
127.0.0.1

<bound method Controller.IP of <Controller c0: 127.0.0.1:6653 pid=13547> >

containernet> py c0.IP()
127.0.0.1

```

Vamos a ejecutar algunos comandos en containernet de ovs-ofctl = dpctl para mirar informacion relacionada con el switch. Se sigue la siguiente forma:

```
dpctl command [arg1] [arg2]
```

Los comandos elegidos consultados de:
1. [OVS Commands Reference de Pica](http://pleiades.ucsc.edu/doc/pica8/ovs-commands-reference.pdf)
2. [Using OpenFlow](http://docs.openvswitch.org/en/latest/faq/openflow/)

Ahora si:

```
dpctl help
ovs-ofctl show s1 
```

Haciendo el ultimo comando fuera: 

```
containernet> dpctl show 
*** s1 ------------------------------------------------------------------------
OFPT_FEATURES_REPLY (xid=0x2): dpid:0000000000000001
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
actions: output enqueue set_vlan_vid set_vlan_pcp strip_vlan mod_dl_src mod_dl_dst mod_nw_src mod_nw_dst mod_nw_tos mod_tp_src mod_tp_dst
 1(s1-eth1): addr:0a:dc:b3:16:50:99
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 2(s1-eth2): addr:3a:82:b9:03:33:2a
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 LOCAL(s1): addr:4a:94:93:b2:e9:48
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0

```

**Conclusiones**:
1. No se ha logrado aun descifrar las Ips de la interfaz de red del switch.
2. Tanto el switch como el controlador estan corriendo en el localhost.
3. Para los host al parecer tambien aplica lo anterior.
4. Hay full conectividad. 


###  Ejemplo 2: ### 

Ejecución de un comando sencillo que monta una topologia single con 2 host con controler remoto:

**Parte 1**: Arrancando la topologia

```
sudo mn --controller remote
```

Resultados basicos:

```
containernet> pingall
*** Ping: testing ping reachability
h1 -> X 
h2 -> X 
*** Results: 100% dropped (0/2 received)
containernet> py c0.IP()
127.0.0.1
containernet> py s1.IP()
127.0.0.1
containernet> py h1.IP()
10.0.0.1
containernet> py h2.IP()
10.0.0.2

containernet> dpctl show
*** s1 ------------------------------------------------------------------------
OFPT_FEATURES_REPLY (xid=0x2): dpid:0000000000000001
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
actions: output enqueue set_vlan_vid set_vlan_pcp strip_vlan mod_dl_src mod_dl_dst mod_nw_src mod_nw_dst mod_nw_tos mod_tp_src mod_tp_dst
 1(s1-eth1): addr:de:56:e9:01:7d:af
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 2(s1-eth2): addr:16:d2:46:12:e5:12
     config:     0
     state:      0
     current:    10GB-FD COPPER
     speed: 10000 Mbps now, 0 Mbps max
 LOCAL(s1): addr:0e:c6:58:47:e3:44
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0
```

**Conclusiones**:
1. No hay conectividad.

**Parte 2**: Arrancando el controlador (remoto). Ahora para el caso intentemos dar conectividad desde un controlador.

``` 
./pox.py log.level --DEBUG --no-cli forwarding.l2_learning 
```

Antes de la ejecucion del comando fue necesario reiniciar la conexion:

``` 
sudo mn --controller remote
```

En terminos de codigo, el presente ejemplo tambien puede ser ejecutado siguiendo las instrucciones del siguiente script: [dia2_example1.py](code/dia2/dia2_example1.py)

###  Ejemplo 3: ### 

**Pregunta:**¿Como puedo lograr que el control de la red sea realizado desde un contenedor con POX y no desde el localhost como en los casos anteriores?

En el siguiente [enlace](https://hub.docker.com/r/juanmejia/reproducingnetwork/) donde se manejo la siguiente [publicacion](http://sbsstc.ac.in/icccs2014/Papers/Paper28.pdf). El enlace estaba roto pero se dejo la cosa debido al paper.

Vamos a descarga el siguiente contenedor de ryu de sonada: https://hub.docker.com/r/sonatanfv/sonata-ryu-vnf/ (para mas detalles ver: https://github.com/sonata-nfv/son-examples/tree/master/vnfs/sonata-ryu-vnf-docker)

Descargando imagen del contenedor.

```
sudo docker pull sonatanfv/sonata-ryu-vnf
```
Corriendo el contenedor:

```
docker run -p 6633:6633 --name c0 --hostname c0 --rm -ti sonatanfv/sonata-ryu-vnf bash
```

Comandos dentro del contenedor:

```
cd ryu/bin
./ryu-manager ../ryu/app/simple_switch_13.py 
```

Se arranco el controlador como switch:

```
loading app ../ryu/app/simple_switch_13.py
loading app ryu.controller.ofp_handler
instantiating app ../ryu/app/simple_switch_13.py of SimpleSwitch13
instantiating app ryu.controller.ofp_handler of OFPHandler
```


Se lanza la topologia:

```
sudo mn --controller remote
```

La salida queda en el controlador queda:

```
root@c0:~/ryu/bin# ./ryu-manager ../ryu/app/simple_switch_13.py 
loading app ../ryu/app/simple_switch_13.py
loading app ryu.controller.ofp_handler
instantiating app ../ryu/app/simple_switch_13.py of SimpleSwitch13
instantiating app ryu.controller.ofp_handler of OFPHandler
packet in 1 d2:e7:dd:9a:b8:10 33:33:00:00:00:16 2
packet in 1 42:f9:1a:4e:3f:4d 33:33:00:00:00:16 1
packet in 1 d2:e7:dd:9a:b8:10 33:33:00:00:00:16 2
packet in 1 d2:e7:dd:9a:b8:10 33:33:00:00:00:02 2
```

Cuando se prueba conectividad esta es posible. Pero hay mucha llegada de paquetes, se presume por otras cosas que pueden estar usando el localhost por lo tanto digamos que el trafico esta contaminado por asi decirlo (nota, esta es una supocision no probada).


**Conclusiones**:
1. El siguiente comando ```docker run -p 6633:6633 --name c0 --hostname c0 --net=none --rm -ti sonatanfv/sonata-ryu-vnf bash``` no da.
2. El contenedor del controlador establece la comunicacion con el switch al parecer desde la interfaz localhost. Desde aqui se podria pensar en hacer pruebas.
3. No es lo que se queria, esperaba hacer el escenario mas realista fijando las IP tanto en el controlador como en la interfaz del switch que se conecta a este.
4. Aunque no entiendo lo que quiere decir, el siguiente [enlace](https://github.com/containernet/containernet/issues/29) parece ser interesante.
5. Ver tambien este: https://github.com/hadik3r/containernet



###  Ejemplo 4: ### 

**Pregunta:**¿Como puedo lograr que el control de la red sea realizado desde un contenedor con POX y no desde el localhost como en los casos anteriores?


Cambiamos un poco las cosas siguiendo los siguientes comandos en su respectivo orden:

1. Llamando el contenedor, pero en este caso cambiando parametros de networking:
```
docker run -p 6633:6633 --name c0 --hostname c0 --net=host --rm -ti sonatanfv/sonata-ryu-vnf bash
ifconfig

---------------------------------------------------------------

br-912338f2b9c4 Link encap:Ethernet  HWaddr 02:42:bd:87:60:0c  
          inet addr:172.25.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          ...
```
2. Corriendo la topologia y cambiando la configuracion de switch.

```
sudo mn --controller remote

---------------------------------------------------------------

xterm s1
```

Dentro de la consola del s1:

```
root@fuck-pc:~/Documents/test-diarios/repaso_SDN# ovs-vsctl set-controller s1 t
cp:172.25.0.1:6633
root@fuck-pc:~/Documents/test-diarios/repaso_SDN# ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:172.25.0.1:6633"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
    ovs_version: "2.5.4"
```

3. Corriendo la aplicacion en el controlador:

```
root@c0:~# cd ryu/bin
root@c0:~/ryu/bin# ./ryu-manager ../ryu/app/simple_switch_13.py 

loading app ../ryu/app/simple_switch_13.py
loading app ryu.controller.ofp_handler
instantiating app ../ryu/app/simple_switch_13.py of SimpleSwitch13
instantiating app ryu.controller.ofp_handler of OFPHandler
packet in 1 4a:4e:53:c3:16:1d 33:33:00:00:00:02 1
packet in 1 4a:4e:53:c3:16:1d ff:ff:ff:ff:ff:ff 1
packet in 1 32:88:0d:b9:0d:31 4a:4e:53:c3:16:1d 2
packet in 1 4a:4e:53:c3:16:1d 32:88:0d:b9:0d:31 1
```

En containernet haciendo el pingall:

```
containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)
```

**Conclusiones**:
1. Cambiando la interfaz por otra diferente ya el trafico entre el controlador y el switch no se ve tan espureo.
2. Los comanos de configuracion de switch se vieron de: http://networkstatic.net/openflow-openvswitch-lab/

# Dia 2

## Fecha: 25/07/2018

>
> **Pregunta a resolver**
> ¿En sonata el switch se ejecuta como contenedor o como elemento en el localhost?
>

###  Parte 1 - sin sonata ### 

**Caso 1**: Inicialmente se lanza una topologia lineal para ver que pasa con los switches.

Se emplearon los siguientes comandos. 

**Para containernet**
```
sudo mn --topo=linear,3
```

**En la consola**

```
sudo ovs-vsctl show         // Informacion de los 3 sw
sudo docker ps              // Informacion de los contenedores
sudo docker container ls
```

Hasta el momento no se aprecia ningun switch corriendo como container, asi mismo para cada caso los switches asumen que el controlador iria en el localhost. Sin embargo todavia no hay conclusiones certeras. En lo que respecta al comportamiento de las IPs la cosa no cambia. 

**Caso 2**: Lanzar una topologia simple con dos contenedores conectados. Mirar como es la informacion asociada al switch. El codigo es [dia2_example2.py](code/dia2/dia2_example2.py). **Nota**: Se asume que las imagenes empleadas por los containers ya se encuentran descargadas.

A continuación se muestran los pasos de ejecución:

1. Lanzar la topologia:

```
sudo python dia2_example2.py 
```

2. Lanzar el controlador:

```
cd ~/pox
./pox.py log.level --DEBUG openflow.of_01 --port=6653 forwarding.l2_learning 
```

**Ejecutando el paso 1**: ```sudo python dia2_example2.py```

Comandos ejecutados:

```
sudo ovs-vsctl show
sudo docker ps
```

Veamos evidencias de salida:

```
tigarto@fuck-pc:~$ sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
        fail_mode: secure
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1-eth2"
            Interface "s1-eth2"
    ovs_version: "2.5.4"
tigarto@fuck-pc:~$ sudo docker ps
CONTAINER ID        IMAGE                    COMMAND             CREATED              STATUS              PORTS               NAMES
9d8979b853fb        openswitch/ubuntuscapy   "/bin/bash"         About a minute ago   Up About a minute                       mn.h2
6359ba15e2a0        openswitch/ubuntuscapy   "/bin/bash"         About a minute ago   Up About a minute                       mn.h1

-------------------------------------------

containernet> nodes
available nodes are: 
c0 h1 h2 s1

containernet> py h1.IP()
10.0.0.251

containernet> py h2.IP()
10.0.0.252

containernet> py s1.IP()
127.0.0.1

containernet> py c0.IP()
127.0.0.1

containernet> py s1.intfs
{0: <Intf lo>, 1: <Intf s1-eth1>, 2: <Intf s1-eth2>}

containernet> py s1.name
s1

containernet> py s1.controlIntf
<Intf lo>

containernet> py s1.failmode
'OVSSwitch' object has no attribute 'failmode'

containernet> py s1.failMode
secure

containernet> py s1.connected
<bound method OVSSwitch.connected of <OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=13087> >

containernet> pingall
*** Ping: testing ping reachability
h1 -> X 
h2 -> X 
*** Results: 100% dropped (0/2 received)
```

**Ejecutando el paso 2**: ```./pox.py log.level --DEBUG openflow.of_01 --port=6653 forwarding.l2_learning```

A continuación se muestran diferentes comandos. Como se podrá notar no hay mayor cambio.

```
containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)

containernet> py dir(s1.intfs[1])
['IP', 'MAC', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_ipMatchRegex', '_macMatchRegex', 'cmd', 'config', 'delete', 'ifconfig', 'ip', 'isUp', 'link', 'mac', 'name', 'node', 'params', 'prefixLen', 'rename', 'setIP', 'setMAC', 'setParam', 'status', 'updateAddr', 'updateIP', 'updateMAC']

containernet> py s1.intfs[1].mac
3e:87:59:c8:4f:41

containernet> py s1.intfs[1].ip

containernet> py s1.intfs[1].ifconfig
<bound method Intf.ifconfig of <Intf s1-eth1>>

containernet> py s1.intfs[1].link
<mininet.link.Link object at 0x7f5f7d74c750>
```

**Caso 3**: Lanzar una topologia simple donde se haga uso del controlador pero en este caso dicho controlador será un contenedor.

**Ejemplo solución**: Ver [dia2_example3.py](code/dia2/dia2_example3.py).

Pasos de ejecucion:

1. Ejecute la topologia

```
sudo python dia2_example3.py 
```

2. Ejecute el contenedor: sem emplea el puerto 6653 por que este es el que se usa desde containernet

```
sudo docker run --name c0 -p 6653:6653 -it --rm osrg/ryu /bin/bash
```

3. Una vez dentro del contenedor, llame el modulo que se ejecutara desde el ryu:

```
cd ryu
ryu-manager --ofp-tcp-listen-port 6653 ryu/app/simple_switch.py
```

**Notas**:
1. Tengase en cuenta que la IP congurada para el controlador esta en la misma red de docker0, o algo asi. Para el caso con ```ifconfig docker0``` tiene como ip  172.17.0.1.

Ejecutando todo:

```
--------------------------------- CONSOLA 1 -CONTAINERNE --------------------------------
sudo python dia2_example3.py 

dpctl -h 
 (vemos que la IP no coincide con la del ovs) por lo que sera necesario realizar el cambio en la configuracion de switch).

dpctl show 
py s1.cmd('ovs-vsctl show')

containernet> pingall
*** Ping: testing ping reachability
h1 -> X 
h2 -> X 
*** Results: 100% dropped (0/2 received)


containernet> py s1.cmd('ovs-vsctl get-controller s1')
tcp:172.17.0.2:6653

containernet> py s1.cmd('ovs-vsctl set-controller s1 tcp:172.17.0.4:6653')

containernet> py s1.cmd('ovs-vsctl get-controller s1')
tcp:172.17.0.4:6653

containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)

Para el ultimo caso vemos que ahora si fue posible la conectividad.
-------------------------------- CONSOLA 2 - CONTROLADOR --------------------------------
cd ryu
ryu-manager --ofp-tcp-listen-port 6653 ryu/app/simple_switch.py

--------------------------------- CONSOLA 3 - TERMINAL ----------------------------------
sudo docker ps // contenedore corriendo:  c0, mn.h1, mn.h2
sudo ovs-vsctl show // Bridge "s1": Controller "tcp:172.17.0.2:6653", fail_mode: secure,...
sudo docker inspect c0

sudo docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c0
172.17.0.4 

---> OTROS COMANDOS
tigarto@fuck-pc:~/pox$ sudo docker network ls
NETWORK ID          NAME                     DRIVER              SCOPE
72c2ba2a6f49        bridge                   bridge              local
14163286e489        host                     host                local
a14e90146526        none                     null                local
912338f2b9c4        zookeepertests_default   bridge              local  (** Creada en algun momento)

sudo docker network inspect bridge
[
    {
        "Name": "bridge",
        ...
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        ...
        "Containers": {
            "18a504bcb4c80f36fdb20287b43c5c51dcb2f0b08b55991e204ac53a86a02563": {
                "Name": "mn.h1",
                "EndpointID": "206bd044f9417647b041359b23c7c20068214038dd800d2ae9491fe6237f0b34",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "245739a0d35a1641a0d0cfa3ea726c499cc24a3b21f0335c8221d2803ab86301": {
                "Name": "mn.h2",
                "EndpointID": "cffbd6f599df8b9652f1fb23cde761ddc271c60743e82decb59cc59845c50343",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            },
            "dde989da7218502ab6f8d4b77124716b81eadd9883c059406a9f12c37ba40623": {
                "Name": "c0",
                "EndpointID": "9715141632f1cd6798c0684052e766af8b61eaab2a7968efb1ec4dd9ca5a7321",
                "MacAddress": "02:42:ac:11:00:04",
                "IPv4Address": "172.17.0.4/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]

```

Vemos que de alguna manera los host estan en la misma red de docker0 asociada al controlador tambien, sin embargo al parecer el aislamiento entre IPs se confirma tal y como se muestra a continuación pues haciendo ping con las ips asociadas con el inspect no hay respuesta, diferente al caso de las asociadas con las generadas por mininet:

```
containernet> py h2.cmd('ping -c 2 172.0.0.2')
PING 172.0.0.2 (172.0.0.2) 56(84) bytes of data.

--- 172.0.0.2 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1029ms


containernet> py h2.cmd('ping -c 2 10.0.0.251')
PING 10.0.0.251 (10.0.0.251) 56(84) bytes of data.
64 bytes from 10.0.0.251: icmp_seq=1 ttl=64 time=0.287 ms
64 bytes from 10.0.0.251: icmp_seq=2 ttl=64 time=0.082 ms

--- 10.0.0.251 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 0.082/0.184/0.287/0.103 ms
```

###  Parte 2 - con sonata -> Ejemplo 1 ###

Se procede a replicar alguno de los ejemplos de https://github.com/sonata-nfv/son-emu/wiki o en su defecto de https://github.com/tigarto/test-diarios/tree/master/abril21/. 

**Elementos involucrados**:
1. sonata_y1_demo_topology_1.py (script de pyhon)

```
--------------------------------- CONSOLA 1  ---------------------------------
sudo python sonata_y1_demo_topology_1.py
---
containernet> nodes
available nodes are: 
c0 dc1.s1 dc2.s1 s1
containernet> net
dc1.s1 lo:  dc1.s1-eth1:s1-eth1
dc2.s1 lo:  dc2.s1-eth1:s1-eth2
s1 lo:  s1-eth1:dc1.s1-eth1 s1-eth2:dc2.s1-eth1
c0
containernet> py s1.IP()
127.0.0.1
containernet> py c0.IP()
127.0.0.1

containernet> dump
<OVSSwitch dc1.s1: lo:127.0.0.1,dc1.s1-eth1:None pid=24809> 
<OVSSwitch dc2.s1: lo:127.0.0.1,dc2.s1-eth1:None pid=24812> 
<OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=24815> 
<RemoteController c0: 127.0.0.1:6653 pid=24800> 

*** Despues de ejecutar los comandos de son-emu-cli ***


containernet> dump
<EmulatorCompute client: client-eth0:10.0.0.2 pid=26524> 
<EmulatorCompute server: server-eth0:10.0.0.4 pid=26741> 
<OVSSwitch dc1.s1: lo:127.0.0.1,dc1.s1-eth1:None,dc1.s1-eth2:None pid=26239> 
<OVSSwitch dc2.s1: lo:127.0.0.1,dc2.s1-eth1:None,dc2.s1-eth2:None pid=26242> 
<OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=26245> 
<RemoteController c0: 127.0.0.1:6653 pid=26232> 

** cadena

containernet> dump
<EmulatorCompute client: client-eth0:10.0.0.2 pid=26524> 
<EmulatorCompute server: server-eth0:10.0.0.4 pid=26741> 
<OVSSwitch dc1.s1: lo:127.0.0.1,dc1.s1-eth1:None,dc1.s1-eth2:None pid=26239> 
<OVSSwitch dc2.s1: lo:127.0.0.1,dc2.s1-eth1:None,dc2.s1-eth2:None pid=26242> 
<OVSSwitch s1: lo:127.0.0.1,s1-eth1:None,s1-eth2:None pid=26245> 
<RemoteController c0: 127.0.0.1:6653 pid=26232> 


containernet> client ping -c2 server
PING 10.0.0.4 (10.0.0.4): 56 data bytes
64 bytes from 10.0.0.4: icmp_seq=0 ttl=64 time=122.919 ms
64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=60.550 ms
--- 10.0.0.4 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 60.550/91.734/122.919/31.185 ms

--------------------------------- CONSOLA 2  ---------------------------------

son-emu-cli compute start -d dc1 -n client -i sonatanfv/sonata-empty-vnf
son-emu-cli compute start -d dc2 -n server -i sonatanfv/sonata-empty-vnf
son-emu-cli network add -b -src client:client-eth0 -dst server:server-eth0 (cadena)

--------------------------------- CONSOLA 3  ---------------------------------

sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1"
            Interface "s1"
                type: internal

    Bridge "dc1.s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "dc1.s1"
            Interface "dc1.s1"
                type: internal
        Port "dc1.s1-eth1"
            Interface "dc1.s1-eth1"

    Bridge "dc2.s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "dc2.s1"
            Interface "dc2.s1"
                type: internal
        Port "dc2.s1-eth1"
            Interface "dc2.s1-eth1"
    ovs_version: "2.5.4"


sudo docker network ls
NETWORK ID          NAME                     DRIVER              SCOPE
72c2ba2a6f49        bridge                   bridge              local
14163286e489        host                     host                local
a14e90146526        none                     null                local
912338f2b9c4        zookeepertests_default   bridge              local


*** Despues de ejecutar los comandos de son-emu-cli ***
sudo docker network ls --> No cambia la salida

sudo ovs-vsctl show
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1-eth1"
            Interface "s1-eth1"
        Port "s1"
            Interface "s1"
                type: internal
    Bridge "dc2.s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "dc2.s1"
            Interface "dc2.s1"
                type: internal
        Port "dc2.s1-eth1"
            Interface "dc2.s1-eth1"
        Port "dc2.s1-eth2"
            Interface "dc2.s1-eth2"
    Bridge "dc1.s1"
        Controller "tcp:127.0.0.1:6653"
            is_connected: true
        fail_mode: standalone
        Port "dc1.s1"
            Interface "dc1.s1"
                type: internal
        Port "dc1.s1-eth2"
            Interface "dc1.s1-eth2"
        Port "dc1.s1-eth1"
            Interface "dc1.s1-eth1"
    ovs_version: "2.5.4"

```

El comportamiendo para el switch es similar que para el caso con mininet, con containernet y con sonata. Al parecer ambos estan en el localhost. Por lo menos hasta ahora. 

###  Parte 2 - con sonata -> Ejemplo 2 ###


Se procede a replicar alguno de los ejemplos de https://github.com/tigarto/test-diarios/tree/master/abril21/. 

**Elementos involucrados**:
1. sonata_y1_demo_topology_1.py (script de pyhon)
2. ws-test1 (directorio)


```
--------------------------------- CONSOLA 1  ---------------------------------
sudo python sonata_y1_demo_topology_1.py
---

containernet> nodes
containernet> net
containernet> dump
containernet> py s1.IP()
127.0.0.1
containernet> py c0.IP()
127.0.0.1
containernet> py h1.IP()
name 'h1' is not defined
containernet> py server.IP()
10.0.0.11
containernet> py client.IP()
10.0.0.9


--------------------------------- CONSOLA 2  ---------------------------------
cd .... ws-test1/projects
son-package --project sonata-ovs-service-emu/ -n sonata-ovs-service
curl -i -X POST -F package=@sonata-ovs-service.son http://127.0.0.1:5000/packages
curl -X POST http://127.0.0.1:5000/instantiations -d "{}"
son-emu-cli compute start -d dc2 -n client -i sonatanfv/sonata-iperf3-vnf
son-emu-cli compute start -d dc2 -n server -i sonatanfv/sonata-iperf3-vnf
son-emu-cli compute list
son-emu-cli network add -b -src client:client-eth0 -dst ovs1:port1
son-emu-cli network add -b -src ovs1:port2 -dst server:server-eth0


--------------------------------- CONSOLA 3  ---------------------------------
sudo ovs-vsctl show


tigarto@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia2$ sudo docker ps
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS               NAMES
204933a25b59        sonatanfv/sonata-iperf3-vnf   "/bin/bash"         2 minutes ago       Up 2 minutes                            mn.server
a20b0b19bed3        sonatanfv/sonata-iperf3-vnf   "/bin/bash"         2 minutes ago       Up 2 minutes                            mn.client
ecb53d89f726        sonatanfv/sonata-ryu-vnf      "/bin/bash"         2 minutes ago       Up 2 minutes                            mn.ctrl
8d559f6bdfe0        sonatanfv/sonata-ovs1-vnf     "/bin/bash"         2 minutes ago       Up 2 minutes                            mn.ovs1

Estos son los contenedores

sudo docker inspect mn.ctrl --> 172.17.0.3/16
sudo docker inspect mn.ovs1 --> 172.17.0.2/16
sudo docker inspect mn.server -->  172.17.0.5
sudo docker inspect mn.client -->  172.17.0.4

```

**Analisis del caso anterior**: Aqui si se agrega un switch ovs como contenedor pero este ira dentro de la nvf presumiblemente conectando s1 con el ovs y a partir de este con el controlador en cuestion. En resumen algo como esto creeria yo.

```
             NVF
              |
              |
(dc1) ------- s1 ------- (dc2)
```
Donde la NVF sera:

```
      ctrl ----- ovs
```

de este modo **puede???** que el resultado neto sea:

```
  ctrl ----- ovs
              |
              |
(dc1) ------- s1 ------- (dc2)
```

La pregunta en el fondo es: Esto para que?
1. No agrega nuevas redes.
2. s1 sigue estando en el localhost
3. sera que tiene que ver con los multiples puntos de presencia.



**Pendiente -- Conclusiones finales respondiendo a las preguntas que estan en el cuaderno**
*** Pregunta con una network: https://github.com/tigarto/2018-1/tree/master/ensayo2/
https://www.southampton.ac.uk/~drn1e09/ofertie/openflow_qos_mininet.pdf


----





Para contenedor:


Switch:

sudo ovs-vsctl set-controller s1 tcp:192.168.10.1:6633

sudo ovs-vsctl set-fail-mode s1 secure

sudo ovs-vsctl show



## Enlaces de inicio
1. [Cosas con flowVisor](https://docs.google.com/document/d/1gVq0S7pWOarwClP_oTOpJ8wMMSRDyqEuNcjvAH2N0tw/edit)
2. [Integrando una red Vlan con flowvisor](https://docs.google.com/document/d/1PYDIvfqTN7cavWoFU61jfqckUDL0BnWWIcfBdKY7i70/edit)
3. [Cosas con Sonata]( https://docs.google.com/document/d/1ytIuO8aywIx-oZarcbbv42vZFiX3NPn1V2Y4pN3f-rM/edit)
4. [Creando topologia experimental con docker]( https://docs.google.com/document/d/1juNEsmRrVgplxZZPGs2noB-VCJNxFCZOX81WGo9yyyM/edit#)
5. [Retomando el uso de controladores - reporte 29]( https://docs.google.com/document/d/1WB7cm2Wdj2KDC78LDUmcRs9uHpfSST1cS2h3Ggu-LfU/edit)
6. [Retomando el uso de controladores - reporte 30]( https://docs.google.com/document/d/1IkHtc8qiUOpK7kDUN5sKJZeQ_n_OUe_c56o9kWg-XbU/edit#heading=h.t407xxhvh3jg)
7. [Networking containers](https://docs.google.com/document/d/1UvEdKZXz3bNKkJtcHYhPsXk9bycV5kcMtHUNIm6SqE8/edit)
8. [Container Tutorials - Using OVS bridge for docker networking](http://containertutorials.com/network/ovs_docker.html)


## Enlaces de referencia
1. https://github.com/tigarto/testbed/tree/master/test7
2. https://github.com/tigarto/testbed/tree/master/test11
3. https://docs.google.com/document/d/14AjUkqLIBVtaFDvHuwwjyk8dSkC0d9fYykWIoJbpgB8/edit
4. https://docs.google.com/document/d/14C295CkmQPDvqYQXnQhXEFnWBH4uMMe6KQD-OipmuU/edit
5. https://docs.google.com/document/d/151qjsGVx0bE_yeJB8gueiW5JgqRTEKcdg2Hf0egAC2c/edit
6. https://github.com/tigarto/testbed
7. https://github.com/tigarto/testbed/tree/master/test4
8. https://github.com/tigarto/testbed/tree/master/test69. 
9. https://docs.google.com/document/d/1eY7oePA7YOQ283wV1gqfdpo2fOyJJDqEkETLNylwJuA/edit
10. https://docs.google.com/document/d/1PYDIvfqTN7cavWoFU61jfqckUDL0BnWWIcfBdKY7i70/edit
11. https://docs.google.com/document/d/1iJhZ2F_j_M7H2rnfKioTnA9-9k4SEMS2DC2zyzvuAa8/edit
12. https://docs.google.com/document/d/1IkHtc8qiUOpK7kDUN5sKJZeQ_n_OUe_c56o9kWg-XbU/edit
13. https://docs.google.com/document/d/1WB7cm2Wdj2KDC78LDUmcRs9uHpfSST1cS2h3Ggu-Lf/edit
