# Apuntes de repaso

> **Preguntas y actividades en torno a las cuales gira este guiin**
> 1. Como lograr que el controlador ONOS permita la comunicacion en una topologia que use dos nodos mininet imitando lo que se hizo los dias 1 y 2 con pox y ryu.
> 2. Mirar como programar un par de flujos sencillo por linea de comandos, pox, ryu y onos. Esto para retomar un poco el protocolo OF.
> 3. Mirar de los documentos viejos que se habia hecho con los ataques de denegación de servicio.
> 4. Mirar como implementar una topologia distribuida cuando se usa ONOS. Puede que sea necesario repasar nuevamente lo que en algun momento se estudio de flowvisor.

# Dia 3

## Fecha: 26/07/2018

# Ejemplos

### Ejemplo 1: ###
Este ejemplo gira en torno a la pregunta 1. ¿Como emplear onos para que controle una red? Para el caso se va a emplear una topologia minimal como siempre se ha usado. 

**Parte 1**: Sin hacer uso de contenedores como host.

Teniendo en cuenta los siguientes enlaces:
* https://wiki.onosproject.org/display/ONOS/Running+the+published+Docker+ONOS+images
* http://sdnhub.org/tutorials/onos/experimenting-with-onos-clustering/
* https://speakerdeck.com/eueung/basic-onos-tutorial
* https://wiki.onosproject.org/display/ONOS/Tutorials

**Prerequisitos**
Imagen de onos descargada de: https://hub.docker.com/r/onosproject/onos/ 

```
sudo docker pull onosproject/onos
```

A continuacion se describen los pasos tomando como base https://wiki.onosproject.org/display/ONOS/Running+the+published+Docker+ONOS+images
1. **Paso 1**: Iniciar el controlador onos, para el caso el contenedor se coloco con el nombre onos1:

```
sudo docker run -it --name onos1 --rm onosproject/onos bash
```

2. **Paso 2**: Obtener la IP del controlador:

**Forma 1**:

```
summary
```

Asi mismo si todo esta bien se puede acceder a la interfaz web asociada al controlador: http://172.17.0.2:8181/onos/ui/login.html con:
* **User**: onos
* **Password**: rocks	

Para ver los puertos expuestos ver el Dockerfile: https://hub.docker.com/r/onosproject/onos/~/dockerfile/

**Forma 2**:

```
 sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' onos1
```

3. **Paso 3 - Cargar los modulos**: Para el caso como el controlador solo tiene los modulos esenciales cargados, es necesario cargar los modulos que seran empleados, para el caso es neceario activar las aplicaciones openflow u forwarding:

```
onos> app activate org.onosproject.openflow
onos> app activate org.onosproject.fwd
```

Para ver las aplicaciones activas se puede usar el comando:

```
onos> apps -a -s
```

4. **Paso 4 - Arranque la topologia mininet**: Para el caso se empleo una topologia minima. Suponiendo que la IP del controlador era 172.17.0.2 el comando para instanciar la red fue:

```
sudo mn --topo single --mac --switch ovsk,protocols=OpenFlow13 --controller remote,172.17.0.2
```

5. **Paso 5 - Interactuar con la red**: Relacionada con la ejecucion de comandos mininet:

```
pingall
```

6. **Paso 5 - Salir del controlador**: 

```
logout
```

**Parte 1**: Haciendo uso de contenedores como host.

```
----------------------------- CONSOLA 1 -------------------------------
sudo python dia3_example1.py 
-- containernet -->
pingall

-------------------------- CONSOLA 2 - ONOS ---------------------------
sudo docker run -it --name onos1 --rm onosproject/onos bash
summary
apps -a -s
app activate org.onosproject.openflow
app activate org.onosproject.fwd
apps -a -s
flows
nodes
links
host
-------------------- CONSOLA 3 - OTROS COMANDOS  -----------------------
tigarto@fuck-pc:~$ sudo docker ps
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                              NAMES
624f27755d5c        openswitch/ubuntuscapy   "/bin/bash"              2 minutes ago       Up 2 minutes                                                           mn.h2
75980e34a55c        openswitch/ubuntuscapy   "/bin/bash"              2 minutes ago       Up 2 minutes                                                           mn.h1
047711ee6cdd        onosproject/onos         "./bin/onos-servic..."   2 minutes ago       Up 2 minutes        6640/tcp, 6653/tcp, 8101/tcp, 8181/tcp, 9876/tcp   onos1


```
En lo que respecta a la interfaz web: http://172.17.0.2:8181/onos/ui/login.html
* **User**: onos
* **Password**: rocks	

Salida detallada de los flujos:

```
onos> flows
deviceId=of:0000000000000001, flowRuleCount=6
    id=100007a585b6f, state=ADDED, bytes=0, packets=0, duration=285, liveType=UNKNOWN, priority=40000, tableId=0, appId=org.onosproject.core, payLoad=null, selector=[ETH_TYPE:bddp], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:CONTROLLER], deferred=[], transition=None, meter=[], cleared=true, StatTrigger=null, metadata=null}
    id=100009465555a, state=ADDED, bytes=0, packets=0, duration=285, liveType=UNKNOWN, priority=40000, tableId=0, appId=org.onosproject.core, payLoad=null, selector=[ETH_TYPE:lldp], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:CONTROLLER], deferred=[], transition=None, meter=[], cleared=true, StatTrigger=null, metadata=null}
    id=10000ea6f4b8e, state=ADDED, bytes=336, packets=8, duration=285, liveType=UNKNOWN, priority=40000, tableId=0, appId=org.onosproject.core, payLoad=null, selector=[ETH_TYPE:arp], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:CONTROLLER], deferred=[], transition=None, meter=[], cleared=true, StatTrigger=null, metadata=null}
    id=9d000056345eca, state=ADDED, bytes=98, packets=1, duration=9, liveType=UNKNOWN, priority=10, tableId=0, appId=org.onosproject.fwd, payLoad=null, selector=[IN_PORT:2, ETH_DST:C2:7C:4F:E2:A1:F3, ETH_SRC:C6:BD:E6:62:BC:26], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:1], deferred=[], transition=None, meter=[], cleared=false, StatTrigger=null, metadata=null}
    id=9d00006152c86d, state=ADDED, bytes=98, packets=1, duration=9, liveType=UNKNOWN, priority=10, tableId=0, appId=org.onosproject.fwd, payLoad=null, selector=[IN_PORT:1, ETH_DST:C6:BD:E6:62:BC:26, ETH_SRC:C2:7C:4F:E2:A1:F3], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:2], deferred=[], transition=None, meter=[], cleared=false, StatTrigger=null, metadata=null}
    id=10000021b41dc, state=ADDED, bytes=392, packets=4, duration=278, liveType=UNKNOWN, priority=5, tableId=0, appId=org.onosproject.core, payLoad=null, selector=[ETH_TYPE:ipv4], treatment=DefaultTrafficTreatment{immediate=[OUTPUT:CONTROLLER], deferred=[], transition=None, meter=[], cleared=true, StatTrigger=null, metadata=null}
```


### Ejemplo 2: ###
En este ejercicio se llevará a cabo la programación de dos flujos de manera sencilla en una topologia single. Para ello se tratara de seguir la siguiente tabla:

**Matching fields**

| Campos match | Flujo 1  | Flujo 2  |
|---|---|---|
| Switch port | 1 | 2 |
| MAC Src |||
| MAC Dst |||
| Eth Type |||
| VLAN ID |||
| IP Src |||
| IP Dst |||
| IP Prot |||
| IP ToS |||
| TCP/UDP Sport |||
| TCP/UDP Dport |||

**Action fields**

Para cada caso de los campos match se realizaran las siguientes acciones:
* **match 1**: enviar (fordward el paquete por el puerto 2)
* **match 2**: enviar (fordward el paquete por el puerto 1)

**Forma 1 - Ejecucion manual**:

Inicialmente se cargo la topologia:

```
sudo mn --topo single,2 --mac --switch ovsk --controller remote
```

```
---------------------------- CONSOLA 1 - MININET ---------------------------
containernet> py s1.cmd("ovs-vsctl show")
9ec06414-9bd9-4579-81d4-8e7801c2eb61
    Bridge "s1"
        Controller "tcp:127.0.0.1:6653"
        Controller "ptcp:6634"
        fail_mode: secure
        Port "s1-eth2"
            Interface "s1-eth2"
        Port "s1"
            Interface "s1"
                type: internal
        Port "s1-eth1"
            Interface "s1-eth1"
    ovs_version: "2.5.4"

containernet> py s1.listenPort
6634

containernet> py s1.failMode
secure

containernet> py s1.IP()
127.0.0.1

containernet> pingall
*** Ping: testing ping reachability
h1 -> X 
h2 -> X 
*** Results: 100% dropped (0/2 received)

-> Despues de agregar los flujos

containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)


------------------------- CONSOLA 2 - COMANDOS OVS -------------------------
-> containernet> xterm s1

# Estadisticas del switch (puertos)
root@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3# dpctl  dump-ports tcp:127.0.0.1:6634
stats_reply (xid=0x16dbf0c3): flags=none type=4(port)
 3 ports
  port 65534: rx pkts=0, bytes=0, drop=0, errs=0, frame=0, over=0, crc=0
           tx pkts=0, bytes=0, drop=0, errs=0, coll=0
  port  1: rx pkts=11, bytes=942, drop=0, errs=0, frame=0, over=0, crc=0
           tx pkts=32, bytes=4361, drop=0, errs=0, coll=0
  port  2: rx pkts=11, bytes=926, drop=0, errs=0, frame=0, over=0, crc=0
           tx pkts=32, bytes=4361, drop=0, errs=0, coll=0

# Verificando que no hay flujos
root@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3# dpctl  dump-flows tcp:127.0.0.1:6634
stats_reply (xid=0x138b764b): flags=none type=1(flow)

# Agregando los flujos
root@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3# dpctl add-flow tcp:127.0.0.1:6634 in_port=1,actions=output:2
root@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3# dpctl add-flow tcp:127.0.0.1:6634 in_port=2,actions=output:1

# Verificando que los flujos esten agregados
root@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3# dpctl  dump-flows tcp:127.0.0.1:6634
stats_reply (xid=0x578f55e0): flags=none type=1(flow)
  cookie=0, duration_sec=7s, duration_nsec=64000000s, table_id=0, priority=32768, n_packets=0, n_bytes=0, idle_timeout=60,hard_timeout=0,in_port=1,actions=output:2
  cookie=0, duration_sec=1s, duration_nsec=594000000s, table_id=0, priority=32768, n_packets=0, n_bytes=0, idle_timeout=60,hard_timeout=0,in_port=2,actions=output:1

```

**Forma 2 - Empleando el controlador POX**:
A continuacion se muestra el caso para POX. El codigo de la aplicación que se ejecuta en el controlador POX es [dia3_pox2flow.py](code/dia3/dia3_pox2flow.py)

```
------------------------------------------ CONSOLA 1 - POX -----------------------------------------

tigarto@fuck-pc:~/pox$ ./pox.py log.level --DEBUG dia3_pox2flow.py
POX 0.5.0 (eel) / Copyright 2011-2014 James McCauley, et al.
Module not found: dia3_pox2flow.py
tigarto@fuck-pc:~/pox$ ./pox.py log.level --DEBUG dia3_pox2flow
POX 0.5.0 (eel) / Copyright 2011-2014 James McCauley, et al.
DEBUG:core:POX 0.5.0 (eel) going up...
DEBUG:core:Running on CPython (2.7.12/Dec 4 2017 14:50:18)
DEBUG:core:Platform is Linux-4.13.0-45-generic-x86_64-with-Ubuntu-16.04-xenial
INFO:core:POX 0.5.0 (eel) is up.
DEBUG:openflow.of_01:Listening on 0.0.0.0:6633
INFO:openflow.of_01:[00-00-00-00-00-01 2] connected
DEBUG:dia3_pox2flow:*** Switch 00-00-00-00-00-01 has come up ***
DEBUG:dia3_pox2flow:+ Installing flow --> in_port: 2, out_port: 1.
DEBUG:dia3_pox2flow:+ Installing flow --> in_port: 1, out_port: 2.


------------------------------------------ CONSOLA 2 - MININET -----------------------------------------
tigarto@fuck-pc:~/Documents/test-diarios/repaso_SDN/code/dia3$ sudo mn --topo single,2 --mac --switch ovsk --controller remote
*** Creating network
*** Adding controller
Unable to contact the remote controller at 127.0.0.1:6653
Connecting to remote controller at 127.0.0.1:6633
*** Adding hosts:
h1 h2 
*** Adding switches:
s1 
*** Adding links:
(h1, s1) (h2, s1) 
*** Configuring hosts
h1 h2 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
*** Starting CLI:

containernet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)
```

Vemos que para el caso anterior hay ping.

**Forma 3 - Empleando el controlador Ryu**:
A continuacion se muestra el caso para Ryu. En este caso vamos a tratar de correr ryu en un contenedor. 

```
------------------------------------------ CONSOLA 1 - Ryu -----------------------------------------
** Tengase en cuenta que cuando se usa -v significa: -v dir_local_machine:dir_container

# Corriendo el contenedor
docker run -p 6633:6633 --name c0 --hostname c0 -v $PWD:/home --rm -ti sonatanfv/sonata-ryu-vnf bash

# Llamando la aplicacion que instala los flujos
cd /home
sudo ryu-manager --verbose dia3_ryu2flow.py

----------------------------------------- CONSOLA 2 - Mininet -------------------------------------

# Se lanzo despues de tener el controlador up

sudo mn --topo single --mac --switch ovsk --controller remote,172.17.0.2:6633

------------------------------------ CONSOLA 3 - Terminal normal-----------------------------------
sudo docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c0
172.17.0.2

sudo ovs-ofctl dump-flows s1
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=115.246s, table=0, n_packets=13, n_bytes=1006, idle_age=43, in_port=2 actions=output:1
 cookie=0x0, duration=115.246s, table=0, n_packets=13, n_bytes=1006, idle_age=43, in_port=1 actions=output:2

```