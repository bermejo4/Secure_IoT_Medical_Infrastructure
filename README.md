# Medical IoT Infrastructure: 
------
## General information:

This project is based in a previous one called [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) that you can also find in this Github account or clicking into the link.

-------
## IoT Medical Device:
- ### Raspberry Pi Pico and ESP8266:
There aren't big changes from the [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) previous mentioned, only a slide switch have been added to stablish the operation mode of the device, to change between Configuration Mode or Working Mode. 
The pinout diagram is the following:

![Diagram Pico](/Documentation/Images/Diagram_pico.png)


#### Configuration Mode:
1. The device transform itself in an Access Point, called IoT_Med, to wich a computer or a phone can connect via WiFi. It only accept 1 connection (Cybersecurity action).

![](/Documentation/Images/Ap_view_laptop.png)

2. To access to the device you have to enter in your browser and write "192.168.4.1". The device have deployed a web server in this address.
3. A configuration page is shown, maybe it takes 15 seconds in load, wait for it to finish please. The page looks like this: 
![](/Documentation/Images/Conf_page.png)
4. Introduce the data required, and the Keys. First one is the key and the second is the initialization vector.
5. Once the form is completed, clicking on the "Save" button the information is encrypted with Keys using AES 128-bits CBC mode, and the data is sent to the pico. The comunication is encrypted to avoid Man In The Middle attack (To learn more obout it go to [cibersecurity](#cybersecurity) section in this readme).
6. When the information arrives to the pico it is decrypted and stored as a JSON in a configuration .txt file --> [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt)
7. After that, the device change itself to the working mode. For that it change its behaviour from Access Point to client.

#### Working Mode:
1. The device read the [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt) to know the Access Point where it have to connect, it's password, and information about the server, like the Server address or the port, and load this information into varibles.
2. The device connects to the Access Point.
3. The device collects data from it's sensors, bunch it in a string JSON format and it is encrypted using AES 128-bit CBC mode. The keys are different from the Configuration mode.
4. The device sends the information encrypted to the port and address specified by the user. It is the same operation mode than in the previous project mentioned, but a new data have been added, other device information, the accelerometer module temperature.
5. Steps 3 and 4 are repited in a loop.


#### Cybersecurity:
In the whole project the symetric encryption is used because clients and servers are previously well knowed, because they form part from the same infrastructure.
The cibersecurity actions taken are to protect the system from "Man in the Middle" attacks, and the consequences of them, like the data reading or the manipulation of the information to change parameters.
Both modes (Configuration Mode and Working Mode) communications are ciphered with AES, using the CBC mode (Cipher Block Chaining). In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted. This way, each ciphertext block depends on all plaintext blocks processed up to that point. To make each message unique, an initialization vector must be used in the first block.
![](/Documentation/Images/cbc_aes.jpeg)
The keys and initialization vectors are saved in configuration files. Please read the advice: [Keys Advice](#keys-and-password-advice)

The library used for the AES encryption and decryption inside the pico is the maes from [maes github](https://github.com/piaca/micropython-aes).


- ### Pseudo Pico Client:
[Pseudo Pico Client](/Pseudo%20Pico%20Client/pseudo_pico_client.py) is a Python program that simulates the behaviour of the original IoT device (which is composed by the Raspberry Pi Pico, ESP8266 and some sensors). To avoid the costs of developing many IoT Devices, and to test the Multiclient infrastructure I consider to implement this solution. 
The data sent can be modified from the terminal of the program following a menu that is shown during its running, except the ECG cardiogram. 

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

The ECG cardiogram is provided by [scipy.misc.electrocardiogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.electrocardiogram.html):
```
from scipy.misc import electrocardiogram
```

The data is also encrypted with AES 128-bit key using the CBC mode. But the library used is different. In the Pico maes is employed but here, in the pseudo pico, the cryptodome library is used. 
```
from Crypto.Cipher import AES
``` 

----------------

## Server:

![](/Documentation/Images/Diagram_Server.png)

- #### Proxy Server: 

[Proxy Server](/Proxy%20Server/Server_multi.py) is a server that listens in 9998 port (the port can be changed), and receives TCP connections to that port from a external device. Once it receives a connection, this connection is managed by a thread, that deploys a [Internal Server](/Proxy%20Server/AesPythonServerToMQTT.py) with a specific port listen (from port 10700 upwards), and then establishes a TCP connection with it. Everything that the proxy server receives from this first external connection it sends to the new intrnal server deployed, it is like a bypass as it can be observed in the previous figure. 
When other connection arrives from other device to the port 9998, other thread is created and, as previously have been described, a new internal server (different from the another, in other port, maybe 10701) is deployed and is connected to it, sending to it everything that it receives. If it receives other connection, the same process ir repeated, and so on. 
At the moment it can only manage 5 connections simultaneously, but that can be changed in the code.

- #### Internal Server:

[Internal Server](/Proxy%20Server/AesPythonServerToMQTT.py) is the brain of the whole server. As have been described previously, it is deployed by the [Proxy Server](/Proxy%20Server/Server_multi.py) and it listens from port 10700 upwards. It develops many functions:
1. Authentication: When data flow arrives to the server, it is ciphered and is unreadable, so the internal server must identify whom it belongs to load the respective keys. For that, it has a file with all the keys and initialization vectors for each device, and it tries to decrypt the message with each one, when it finds something that it expects with a determined format, it assumes that it has identified the user, so it loads the key and the initialization vector.

2. AES Decryption: Once the key and the initialization vector are loaded it decrypts the data with them. The AES is 128-bit and CBC mode. 

3. Unformat JSON into variables: When the decryption occurs the server finds a string with a JSON format, so it unformats the JSON into different variables, which then they will be used in the topic publication.

4. MQTT Connection with Broker: The Broker is listening in the port 1883, so the connection is established with that port. A library in python helps with that process and the next function (the topic publication) and is:
```
from paho.mqtt import client as mqtt_client
```

5. Topics Publication in Broker: The topics follows this directory format:
```
Pico/iot_dev_01/Physiological_Data/Temperature
Pico/iot_dev_01/Physiological_Data/Pulse_Signal
Pico/iot_dev_01/Physiological_Data/Accelerometer/x
Pico/iot_dev_01/Physiological_Data/Accelerometer/y
Pico/iot_dev_01/Physiological_Data/Accelerometer/z
Pico/iot_dev_01//Internal_Device_Data/Temperature/MCU
Pico/iot_dev_01//Internal_Device_Data/Temperature/MPU
```
Where iot_dev_01 is the device identified previously. 
The variables that were saved in the JSON unformat are published in their respective topics.

- #### MQTT Broker (EMQX):
- #### Docker:


## Node Red:

-----------------
## Other useful information:

## Keys and Password advice:
 ⚠️ The following files are only to show examples or as samples. 
They are not the official keys or password.

- [DEVICES_KEYS.txt](/Python%20Server/DEVICES_KEYS.txt)
- [PKEYS_CLIENT_MOD.txt](/Raspberry%20Pi%20Pico/PKEYS_CLIENT_MOD.txt)
- [PKEYS_SERVER_MOD.txt](/Raspberry%20Pi%20Pico/PKEYS_SERVER_MOD.txt)
- [conf_file.txt](/Raspberry%20Pi%20Pico/conf_file.txt) 

**⚠️ Please, if you are going to use this code change the keys and password!!! ⚠️**

## Some useful tricks to monitoring the project:

#### View ports listening in your unix computer:
Open the terminal and write:
```
lsof -i -P | grep -i listen
``` 
A table with the process listening and their ports will be shown.
If you want to close some process you have to find the process ID in this table and write in the terminal the following:
```
kill -15 [Process_ID]
``` 