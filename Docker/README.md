# DOCKER 
3 Docker containers are used in this project:
- Python: to run the proxy server and the internal servers. 
- EMQX: to deploy the MQTT Broker and their services in a fast mode.
- Node-Red: to deploy a fast graphical user interface and test that the MQTT part works properly.

## Docker-files:

Some of the containers need images with specific dependencies and changes. For that, there are different dockerfiles.
To obtain (build) a new image from a dockerfile the following command must be employed: 

```
docker build . -t noderedbermejo:1
```