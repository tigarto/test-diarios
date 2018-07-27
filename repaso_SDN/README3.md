# Hecho de afan #

http://sdnhub.org/tutorials/onos/
https://wiki.onosproject.org/display/ONOS/A+Beginner%27s+Guide+to+Contribution
https://www.youtube.com/watch?v=l25Ukkmk6Sk
https://github.com/chunhai/sdn_ONOS_CORD/wiki/Build-and-debug-a-new-project-of-ONOS

**A tener en cuenta**:
* En IDEs se descargo el InteliJ. Fala instalarlo.

**Enlace importante**: https://wiki.onosproject.org/display/ONOS/Developer+Guide
Otra parte donde tambien se habla de esto esta en: https://wiki.onosproject.org/display/test/Building+ONOS


**Instalando prerequisitos**

```
sudo apt install maven

sudo apt-get install software-properties-common -y && \
sudo add-apt-repository ppa:webupd8team/java -y && \
sudo apt-get update && \
echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections && \
sudo apt-get install oracle-java8-installer oracle-java8-set-default -y
```

**Download ONOS code & Build ONOS**

```
cd ~
git clone https://gerrit.onosproject.org/onos
cd onos
export ONOS_ROOT=$(pwd)
tools/build/onos-buck build onos --show-output
```

**Run ONOS**  (-- Apenas vamos aca)

```
tools/build/onos-buck run onos-local -- clean debug  # 'clean' to delete all previous running status; 'debug' to enable Remote Debug function
```