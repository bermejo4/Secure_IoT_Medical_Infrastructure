# Development of a Secure Medical IoT Infrastructure: 
------
## General information:

This project is based on a previous one called [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) which you can also find in this GitHub account or by clicking on the link.

## Index:
- [IoT Medical Device](#iot-medical-device)
    - [Raspberry Pi Pico and ESP8266](#raspberry-pi-pico-and-esp8266)
    - Modes:
        - [Configuration Mode](#configuration-mode)
        - [Working Mode](#working-mode)
    - [Cybersecurity](#cybersecurity)
    - [Pseudo Pico Client](#pseudo-pico-client)
- [Server](#server)
    - [Proxy Server](#proxy-server)
    - [Internal Server](#internal-server)
    - [MQTT Broker](#mqtt-broker-emqx)
    - [Docker](#docker)
    - [Node-Red](#node-red)
- [Other useful information](#other-useful-information)
    - [Keys and Password advice](#keys-and-password-advice)
    - [Some useful tricks to monitoring the project](#some-useful-tricks-to-monitoring-the-project)
- [Paper](#paper)

-------
-------
-------
## IoT Medical Device:
- ### Raspberry Pi Pico and ESP8266:
There aren't big changes from the [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) previously mentioned, only a slide switch has been added to establish the operation mode of the device, to change between Configuration Mode or Working Mode. 
The pinout diagram is the following:

![Diagram Pico](/Documentation/Images/Diagram_pico.png)


#### Configuration Mode:
1. The device transforms itself into an Access Point, called IoT_Med, to which a computer or a phone can connect via WiFi. It only accepts 1 connection (Cybersecurity action).

![](/Documentation/Images/Ap_view_laptop.png)

2. To access the device you have to enter in your browser and write "192.168.4.1". The device has deployed a web server at this address. 

3. A configuration page (whose code is [init_page.html](/Raspberry%20Pi%20Pico/init_page.html)) is shown, maybe it takes 10 seconds to load, wait for it to finish, please. The page looks like this: 

![](/Documentation/Images/Conf_page_laptop.png)

This webpage has been developed using HTML and JavaScript. The HTML for the structure of the page and JS for the functionality. It is important to say that the reason why the time loading average is about 10 seconds is that we are working with a device that hasn't got access to the Internet in this mode, so the JS library used for the AES encryption is fully injected in the webpage without using script URL reference, so all this information have to be sent by the device, about 61772 bytes of library code (all the HTML file is 65.3 KB), in packets of 2000 bytes (esp8266 maximum limit is 2048 bytes buffer to send), in a period of 300 ms each packet; it's about 9 additional seconds of loading without taking account the delay time of the browser and the wifi card of your computer or smartphone. The rest of the page without the library is only 3.6KB that is sent in 500 ms more or less. By becoming a better and more secure system the price to pay is in time.

4. Introduce the data required and the Keys. The first one is the key and the second is the initialization vector. 


5. Once the form is completed, by clicking on the "Save" button the information is encrypted with Keys using AES 128-bits CBC mode, and the data is sent to the pico. The communication is encrypted to avoid Man In The Middle attack (To learn more about it go to the [cybersecurity](#cybersecurity) section in this readme). 
![Pico as server Diagram](/Documentation/Images/Pico_as_web_server.png) 


6. When the information arrives at the pico it is decrypted and stored as a JSON in a configuration .txt file --> [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt) 

7. After that, the device change itself to the working mode. For that, it changes its behavior from Access Point mode to Client mode.

#### Working Mode:
1. The device read the [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt) to know the Access Point where it has to connect, its password, and information about the server, like the Server address or the port and loads this information into variables.
2. The device connects to the Access Point.
3. The device collects data from its sensors, bunch it in a string JSON format and it is encrypted using AES 128-bit CBC mode. The keys are different from the Configuration mode.
4. The device sends the information encrypted to the port and address specified by the user. It is the same operation mode as in the previous project mentioned, but new data have been added, including other device information, which is the accelerometer module temperature.
5. Steps 3 and 4 are repeated in a loop.


#### Cybersecurity:
In the whole project, symmetric encryption is used because clients and servers are previously well known because they form part of the same infrastructure.
The cybersecurity actions taken are to protect the system from "Man in the Middle" attacks, and the consequences of them, like the data reading or the manipulation of the information to change parameters.
Both modes (Configuration Mode and Working Mode) communications are ciphered with AES, using the CBC mode (Cipher Block Chaining). In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted. This way, each ciphertext block depends on all plaintext blocks processed up to that point. To make each message unique, an initialization vector must be used in the first block.
![](/Documentation/Images/cbc_aes.jpeg)
The keys and initialization vectors are saved in configuration files. Please read the advice: [Keys Advice](#keys-and-password-advice)

The library used for the AES encryption and decryption inside the pico is the Maes from [Maes Github](https://github.com/piaca/micropython-aes).


- ### Pseudo Pico Client:
[Pseudo Pico Client](/Pseudo%20Pico%20Client/pseudo_pico_client.py) is a Python program that simulates the behavior of the original IoT device (which is composed of the Raspberry Pi Pico, ESP8266 and some sensors). To avoid the costs of developing many IoT Devices, and to test the Multiclient infrastructure I consider implementing this solution. 
The data sent can be modified from the terminal of the program following a menu that is shown during its running, except for the ECG signal. 

The terminal menu:
```
If you want to change some parameter indicate the number option:
1. Increase (+) the patient temperature 0.5ºC.
2. Decrease (-) the patient temperature 0.5ºC.
3. Increase (+) the MCU temperature 0.5ºC.
4. Decrease (-) the MCU temperature 0.5ºC.
5. Increase (+) the MPU temperature 0.5ºC.
6. Decrease (-) the MPU temperature 0.5ºC.
-----------------------------------------------
7. Increase (+) 0.1 the X Acceleromenter component
8. Decrease (-) 0.1 the X Acceleromenter component
9. Increase (+) 0.1 the Y Acceleromenter component
10. Decrease (-) 0.1 the Y Acceleromenter component
11. Increase (+) 0.1 the Z Acceleromenter component
12. Decrease (-) 0.1 the Z Acceleromenter component
-----------------------------------------------
Insert your option (number):
```

The ECG cardiogram is provided by [Scipy.misc.electrocardiogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.electrocardiogram.html):
```
from scipy.misc import electrocardiogram
```

The data is also encrypted with the AES 128-bit key using the CBC mode. But the library used is different. In the Pico, Maes is employed but here, in the pseudo pico, the Cryptodome library is used. 
```
from Crypto.Cipher import AES
``` 

----------------

## Server:

![](/Documentation/Images/Diagram_Server_light.png)

- #### Proxy Server: 

The [Proxy Server](/Proxy%20Server/Proxy_Server.py) is a server that listens on port 9998 (the port can be changed) and receives TCP connections to that port from an external device. Once it receives a connection, this connection is managed by a thread, that deploys an [Internal Server](/Proxy%20Server/AesPythonServerToMQTT.py) with a specific port listen (random free port), and then establishes a TCP connection with it. Everything that the proxy server receives from this first external connection it sends to the new internal server deployed, is like a bypass as can be observed in the previous figure. 
When another connection arrives from another device to port 9998, another thread is created and, as previously have been described, a new internal server (different from the other, in another free port) is deployed and is connected to it, sending to it everything that it receives. If it receives another connection, the same process is repeated, and so on. 
At the moment it can only manage 5 connections simultaneously, but that can be changed in the code.

- #### Internal Server:

The [Internal Server](/Proxy%20Server/AesPythonServerToMQTT.py) is the brain of the whole server. As has been described previously, it is deployed by the [Proxy Server](/Proxy%20Server/Server_multi.py) and it listens from port 10700 upwards. It develops many functions:
1. Authentication: When data flow arrives at the server, it is ciphered and unreadable, so the internal server must identify to whom it belongs to load the respective keys. For that, it has a file with all the keys and initialization vectors for each device, and it tries to decrypt the message with each one, when it finds something that it expects with a determined format, it assumes that it has identified the user, so it loads the key and the initialization vector.

2. AES Decryption: Once the key and the initialization vector are loaded it decrypts the data with them. The AES is 128-bit and CBC mode. 

3. Unformat JSON into variables: When the decryption occurs the server finds a string with a JSON format, so it unformats the JSON into different variables, which then will be used in the topic publication.

4. MQTT Connection with Broker: The Broker is listening on port 1883, so the connection is established with that port. A library in python helps with that process and the next function (the topic publication) and is:
```
from paho.mqtt import client as mqtt_client
```

5. Topics Publication in Broker: The topics format follows this directory structure:
```
Pico/iot_dev_01/Physiological_Data/Temperature
Pico/iot_dev_01/Physiological_Data/Pulse_Signal
Pico/iot_dev_01/Physiological_Data/Accelerometer/x
Pico/iot_dev_01/Physiological_Data/Accelerometer/y
Pico/iot_dev_01/Physiological_Data/Accelerometer/z
Pico/iot_dev_01//Internal_Device_Data/Temperature/MCU
Pico/iot_dev_01//Internal_Device_Data/Temperature/MPU
Pico/iot_dev_01/Ip_address
Pico/iot_dev_01/Port_address
Pico/iot_dev_01/Internal_Server/Ip_address
Pico/iot_dev_01/Internal_Server/Port_address
```
Where iot_dev_01 is the device identified previously. 
The variables that were saved in the JSON unformat are published in their respective topics.

- #### MQTT Broker (EMQX): 

EMQX is an Open-source MQTT broker with a high-performance real-time message processing engine, powering event streaming for IoT devices at a massive scale. [](https://www.emqx.io/docs/en/v5.0/#benefits)
As the most scalable MQTT broker, EMQX can connect any device, at any scale. Move and process IoT data anywhere. 

The broker acts as a post office. MQTT clients don't use a direct connection address of the intended recipient but use the subject line called "Topic". Anyone who subscribes receives a copy of all messages for that topic. Multiple clients can subscribe to a topic from a single broker (one to many capabilities), and a single client can register subscriptions to topics with multiple brokers (many to one).
The EMQX service is running in the server with only a piece of code in the [docker-compose.yml](/Python%20Server/docker-compose.yml)

- #### Docker:

Docker offers:
- standardization, being portable anywhere.
- lightweight, it only installs and uses the resources that it will need.
- Security, isolating the programs and services running from the host machine. 

First, a Dockerfile is used to configure specific dependencies that containers employed need, like libraries, but based on an image. Then a docker-compose is used to run the containers. Five containers are running with different ports opened (or not) depending on the service offered:

- Python: 9998
- EMQX: 18083 and 1883
- NodeRed: 1880
- 2 sniffers:
    - EMQX Sniffer: without port opened. It captures all the traffic that passes through the EMQX internal network interface.
    - Python Server Sniffer. It captures all the traffic that passes through its python server-internal network interface.

An internal network is deployed to connect EMQX, Python Server and NodeRed containers. A static IP address has been set for them, that can be modified in the docker-compose file. The network is 172.20.0.0/16 and the static addresses given are:
- Python Server: 172.20.0.10
- EMQX: 172.20.0.20
- NodeRed: 172.20.0.25

The Sniffers capture all the traffic and save it in two files (with .pcap extension) that can be accessed when the infrastructure is working to watch what is happening inside the docker network.
The files are located in the Docker directory in the data folder. It can be read using Wireshark and then each packet can be filtered using the tools that offer this program. 

#### Node-Red:

Node-Red is employed to test that the MQTT publications from the MQTT Broker work properly and also, due to Node-Red gives an easy framework to make graphical user interfaces (GUIs), it is used as a dashboard to show clearly all the parameters that the system can offer.

The flows in NodeRed look like in the following image:
![](/Documentation/Images/nodered_flows_example.png)
Each device has its group of flows. All the flow configuration is in [flows.json](/Docker/dockerfiles/nodered/flows.json).

The Dashboard looks like the following snapshot:
![](/Documentation/Images/dashboard_complete.png)
The dashboard has been customized using CSS. The CSS style used is in [styles-dashboard.css](/Docker/dockerfiles/nodered/styles-dashboard.css), and it must be introduced into the "template" node in the flow diagram.


-----------------
## Other useful information:
-----------------
## Keys and Password advice:
 ⚠️ The following files are only to show examples or as samples. 
They are not official keys or passwords.

- [DEVICES_KEYS.txt](/Python%20Server/DEVICES_KEYS.txt)
- [PKEYS_CLIENT_MOD.txt](/Raspberry%20Pi%20Pico/PKEYS_CLIENT_MOD.txt)
- [PKEYS_SERVER_MOD.txt](/Raspberry%20Pi%20Pico/PKEYS_SERVER_MOD.txt)
- [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt) 

**⚠️ Please, if you are going to use this code change the keys and password!!! ⚠️**

-----------------
## Some useful tricks to monitoring the project:

#### To view ports listening in your Unix computer:
Open the terminal and write:
```
lsof -i -P | grep -i listen
``` 
A table with the process listening and their ports will be shown.
If you want to close some process you have to find the process ID in this table and write in the terminal the following:
```
kill -15 [Process_ID]
``` 

----------
----------

## Paper:

[Project Paper in pdf](/Medical_iot_secure_infrastructure.pdf)
