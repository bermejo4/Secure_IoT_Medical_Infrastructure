#!/bin/bash

#Docker infrastructure deployment:
#----------------------------------

#Docker network creation
docker network create --subnet=172.20.0.0/16 IoT_Net

#Docker images building:
docker build -f dockerfiles/nodered/Dockerfile -t noderedbermejo:1 .
# docker build -f dockerfiles/pythonServers/Dockerfile -t pythonserversbermejo:1 .

docker-compose up