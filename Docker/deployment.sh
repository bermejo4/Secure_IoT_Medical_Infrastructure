#!/bin/bash

#Docker infrastructure deployment:
#----------------------------------

#Docker images building:
docker build -f dockerfiles/nodered/Dockerfile -t noderedbermejo:1 .
docker build -f dockerfiles/pythonServers/Dockerfile -t pythonserversbermejo:1 .

docker-compose up