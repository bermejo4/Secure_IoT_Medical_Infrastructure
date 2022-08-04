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