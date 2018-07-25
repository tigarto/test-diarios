# Apuntes de repaso

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

Para contenedor:

docker run -p 6633:6633 --name c0 --hostname c0 --net=none --rm -ti hsrnetwork/ryu bash


Switch:

sudo ovs-vsctl set-controller s1 tcp:192.168.10.1:6633

sudo ovs-vsctl set-fail-mode s1 secure

sudo ovs-vsctl show



## Enlaces de inicio
1. Cosas con flowVisor: https://docs.google.com/document/d/1gVq0S7pWOarwClP_oTOpJ8wMMSRDyqEuNcjvAH2N0tw/edit
2. Integrando una red Vlan con flowvisor: https://docs.google.com/document/d/1PYDIvfqTN7cavWoFU61jfqckUDL0BnWWIcfBdKY7i70/edit
3. Cosas con Sonata: https://docs.google.com/document/d/1ytIuO8aywIx-oZarcbbv42vZFiX3NPn1V2Y4pN3f-rM/edit
4. Creando topologia experimental con docker: https://docs.google.com/document/d/1juNEsmRrVgplxZZPGs2noB-VCJNxFCZOX81WGo9yyyM/edit#
5. Retomando el uso de controladores - reporte 29: https://docs.google.com/document/d/1WB7cm2Wdj2KDC78LDUmcRs9uHpfSST1cS2h3Ggu-LfU/edit
6. etomando el uso de controladores - reporte 30: https://docs.google.com/document/d/1IkHtc8qiUOpK7kDUN5sKJZeQ_n_OUe_c56o9kWg-XbU/edit#heading=h.t407xxhvh3jg
7. Networking containers: https://docs.google.com/document/d/1UvEdKZXz3bNKkJtcHYhPsXk9bycV5kcMtHUNIm6SqE8/edit
8. 


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
