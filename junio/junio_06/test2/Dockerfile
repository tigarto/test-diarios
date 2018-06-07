# To build: sudo docker build -t ubuntu-test .

FROM ubuntu:xenial
MAINTAINER manuel.peuster@uni-paderborn.de

RUN	apt-get update && apt-get install -y \
	net-tools \
	iproute \
	inetutils-ping \
        curl \
        python \
	wget
        
CMD /bin/bash
