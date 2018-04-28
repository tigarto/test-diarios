# Ejemplos


> **Objetivos**
> * Correr algunos ejemplos de la pagina.
> * Entender dichos ejemplos

* **Fecha**: 27/04/2018

## Ejemplos

### Ejemplo 1 - Other Demo Scripts
**URL**: https://github.com/sonata-nfv/son-examples/wiki/Other-Demo-Scripts


### Ejemplo 2 - Containernet and SONATA Emulator Demo

**URL**: https://github.com/mpeuster/son-tutorials/tree/master/upb-containernet-emulator-summerschool-demo


***********
cd /home/tigarto/Documents/test-diarios/abril27/test1/topologias


containernet> nodes
available nodes are:
c0 dc1.s1 dc2.s1 s1
containernet> links
dc1.s1-eth1<->s1-eth1 (OK OK)
dc2.s1-eth1<->s1-eth2 (OK OK)
containernet> net
dc1.s1 lo:  dc1.s1-eth1:s1-eth1
dc2.s1 lo:  dc2.s1-eth1:s1-eth2
s1 lo:  s1-eth1:dc1.s1-eth1 s1-eth2:dc2.s1-eth1
c0



T2
son-workspace --init --workspace $PWD/ws-test1
cd ws-test1/projects/
Se copia aqui el proyecto: sonata-fw-service-sp

son-package --project sonata-fw-service-sp/ -n sonata-fw-dpi-service

*********
