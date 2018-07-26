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

