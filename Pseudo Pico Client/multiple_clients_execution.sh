#!/bin/bash

#docker build . -t noderedbermejo:1 &
#docker-compose up &


#open "http://localhost:18083/?#/connections" &
#open "http://localhost:1880/#" &
#open "http://localhost:1880/ui/#!/0?socketid=A1dIg7Agq7tI8pDRAAAX" &

xterm -e "python3 pseudo_pico_client.py 1" &
#sleep 1
#xterm -e "python3 pseudo_pico_client.py 3" &
#sleep 1
#xterm -e "python3 pseudo_pico_client.py 4" &