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

| Campos  | Flujo 1  | Flujo 2  |
|---|---|---|
| Switch port | 1 | 3 |
| MAC Src |||
| MAC Dst |||
| Eth Type |||
| VLAN ID |||
| IP Src |||
| IP Dst |||
| IP Prot |||
| IP Sport |||
| IP Dport |||
| Action |Out 3| Out 1 |
| Stats |||
