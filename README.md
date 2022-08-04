# Medical IoT Infrastructure: 
------
## General information:

This project is based in a previous one called [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) that you can also find in this Github account or clicking into the link.

-------
## IoT Device:
- #### Raspberry Pi Pico and ESP8266:
There aren't big changes from the [IoT_Medical_Device](https://github.com/bermejo4/IoT_Medical_Device) previous mentioned, only a slide switch have been added to stablish the operation mode of the device, to change between Configuration Mode or Working Mode. 
The pinout diagram is the following:

![Diagram Pico](/Documentation/Images/Diagram_pico.png)


- #### Pseudo Pico Client:
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


### Cybersecurity:

### Configurability:

----------------

## Server:

![](/Documentation/Images/Diagram_Server.png)

- #### Proxy Server:
- #### Internal Server:
- #### MQTT Broker (EMQX):
- #### Docker:

## Cybersecurity:

## MQTT:

-----------------
## Other useful information:

## ⚠️ Keys and Password advice:
The following files are only to show examples or as samples. 
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