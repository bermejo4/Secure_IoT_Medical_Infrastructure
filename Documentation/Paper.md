# Development of a Secure Medical IoT Infrastructure:
# Abstract
# 1. Introduction:

The Internet of Things (IoT) is the concept of connecting any device (so long as it has an on/off switch) to the Internet and to other connected devices [1]. The IoT world is mostly made up of systems with low computing power, power consumption, memory and disk space that are deployed in insecure networking environments [2] for that reason IoT devices and their infrastructure can be considered vulnerable assets which must be protected using different controls and cybersecurity policies in order to avoid failures, and especially in the health sector, due to, consequences of IoT security failures might cause a direct loss of life [3]. 

An IoT ecosystem is typically composed of embedded devices and sensors, mobile applications, cloud infrastructure, and network communication protocols [4], and in each one of these components must be present the CIA triad (Confidentiality, integrity and availability) to be a secure system, that is a model designed to guide policies for information security within an organization. The elements of the triad are considered the three most crucial components of security [5]. A solution to fulfill these requirements is the encryption of the communication between the elements that compose the IoT infrastructure. Symmetric or asymmetric encryption can be applied, the difference is trust between the data intermediaries. In this work symmetric will be enough because there is trust in the IoT ecosystem. The most famous, used and secure symmetric encryption algorithm is AES (Advanced Encryption Standard). It is based on a design principle known as a substitution–permutation network and is efficient in both software and hardware. AES processes blocks of 128 bits using a secret key of 128, 192 or 256 bits [6]. AES has a variety of modes of operation. In cryptography, a block cipher mode of operation is an algorithm that uses a block cipher to provide information security such as confidentiality or authenticity. [7]

The secure IoT infrastructure challenge is well known by the whole cybersecurity community, and proof of that is the work of K. Siva Kumar Swamy et al.[8] where a secure IoT infrastructure is built using esp32 board as a device and client, MQTT bridge and broker (Mosquitto) as intermediaries, MQTT protocol with AES over WiFi as communication protocols, and services as final receivers. MQTT is a Machine-Machine connectivity protocol. It works on top of the TCP/IP stack but is extremely lightweight because it minimizes messaging using a publish-subscribe architecture [9]. One of the main problems with MQTT is that authentication is optional, and even if it is used, it is unencrypted by default. When credentials are transmitted in cleartext, attackers with a man-in-the-middle position on the network can steal them and also brokers don't typically limit the number of authentication attempts per client [10]. So before using MQTT these problems should be solved or be used in a controlled environment. A system very similar to the previous work mentioned is shown by Mohammad Al-Mashhadani et al. [11], using also AES, but they avoid MQTT and their infrastructure. The Esp32 is also used, a versatile and multifunction, but more functionality than a device needs, increasing the ways an attacker can exploit it [12], and also, as more disadvantages, the device has high consumes and size.

One disadvantage of encryption is that increase the consumption, complexity and delays of the system in a way directly proportional to the size of data to be encrypted. Some cryptographers try to improve the AES algorithm to be applied in a light mode to IoT devices in order to reduce the consumption and times, as Meryam Saad Fadhil et al.[13] show in their work. The problem with that is that it is trying to reinvent the wheel when AES is standardized and tested, and applying a new algorithm (or only a little modification) that has not been sufficiently tested can be a risky action in cybersecurity words only to reduce a little unit of consumption or time. 

From a broad point of view, the final destination of this project is to improve the previous project [14] developed giving it security and new features to enhance the system and infrastructure to a close user-friendly and professional experience.


# 2. Technical Proposal:

The main purpose is to develop a platform that reaches the following objectives:

- First, keep the features and objectives reached in the previous project of multisensor, wearable, wireless, low-cost, scalable, and small device system without interfering with the new objectives here proposed. 

- Second, Configurability: some parameters can change in the IoT environment like the Server IP and port, or the wifi network and its password. For a more user-friendly experience, it can be changed put the device in a configuration mode, and modify it in a web browser with a graphical user interface.

- Third, communication encryption and authentification: using AES 128-bit key for both purposes. The encryption is reasonable with AES, authentification is a consequence of it because only those who have the key can encrypt and decrypt the data, and only two parties know the key, so each one can identify the other. 

- Fourth, multiclient service: The server can manipulate multiple TCP/IP connections that arrive and deploy a new service for each connection that arrives authenticating each device depending on a list of keys previously registered in the server as well-known devices.

- Fifth, MQTT Broker and MQTT: as a scalable system to share the data collected from each device and share it with authenticated applications or other devices.

The system now works as follows:

If the system has never been configured it must be put in configuration mode with a slide button that is in the device. Then a wifi network is enabled without a password, when the user access it, opens the web browser and searches "192.168.4.1", then a page is shown as in figure 1, where the user can register the IP address and port of the server, the Wi-Fi where the device will be connected and its password, also there are two keys that must be entered to cipher the data which will be sent to the device. Once everything is completed the user clicks on the save button and this information is saved into the device. 

![Configuration Page image](/Documentation/Images/Conf_page.png)
**Figure 1.** *Configuration page shown in the browser*

Next, the device switches automatically to work mode, it collects data and sends it to an access point (using the Wi-Fi network and password specified in the configuration mode). A server in the IP address and listen in the port specified receives the data and sends it to an MQTT broker where it will be published to be used by authenticated applications, like a dashboard where the data will be shown in a graphical mode.

# 3. Architecture: 

The architecture can be understood in two phases, the first one the configuration phase, where the device operates as an access point and web server, and the second, the work phase, where the device operates as a client. 

## 3.1. The device as an access point and server:

The device works as an access point enabling a Wi-Fi network called "Med_IoT" without a password but allowing only one connection as a cybersecurity policy. Then whatever user can access it with a laptop or a smartphone.
Immediately after the access point is enabled, a web server is deployed in port 80, so the device is working as a server, and the laptop or smartphone that is used to communicate with it as a client. It offers a web page based on HTML and Javascript in the IP address 192.168.4.1 (the IP address of the device in the network created by itself) called "init_page.html". When the user clicks on save the data is sent ciphered to the device, where will be decrypted and stored in a configuration file. All the communication process is carried over HTTP/TCP. Figure 2 shows the whole process.

![Pico as a web server](/Documentation/Images/Pico_as_web_server.png)
**Figure 2.** *Pico as server diagram*

## 3.2. The device as a Client:
Once the data is configured the device starts to operate in work mode or also if the slide button is in work mode state. It takes the parameter that needs to establish the TCP connection with the server (IP address and port 9998; and the Wi-Fi network and password as network gateway), collects the data from its sensors, formats it in a JSON, encrypts it using AES and then sends the encrypted data through the connection established. Next, it starts again the loop since the part of collecting sensor data and so on as Figure 3 shows.

![Intern process](/Documentation/Images/pico_intern_process.png) 
**Figure 3.** *Pico intern process diagram* 

Then the data travel secure, by the encryption, through a network, that can be a local network or the Internet, until arriving at the destination, a server listens in the 9998 port. 
The server can be explained in three parts: proxy server, internal server and MQTT broker. The proxy server listens in the 9998 port, when a connection arrives it manages the connection, deploys an internal server listens in a specific port (from 10700 upwards), establishes a TCP connection with that port, and bypass all the traffic that arrives from the initial connection to the TCP connection that connects with the internal server. If it receives another connection in port 9998, the same process is repeated, and so on but changing the port of the internal server. When the data is received by the internal server deployed it has the following tasks:

- Authentication: When data flow arrives at the server, it is ciphered and is unreadable, so the internal server must identify to whom it belongs to load the respective key. For that, it has a file with all the keys for each device, and it tries to decrypt the message with each one, when it finds something that it expects with a determined format, it assumes that it has identified the user, so it loads the key and the initialization vector. This process only occurs once, then the key will be associated with the connection.

- MQTT Connection with Broker: When the authentication is successful, the internal server connects with the MQTT Broker. The Broker is listening on port 1883, so the connection is established with that port.

- AES Decryption: Once the key is loaded it decrypts the data with it. 

- Unformat JSON into variables: after decryption, the server finds a string with a JSON format, so it unformats the JSON into different variables, which then will be used in the topic publication.

- Topics Publication in Broker: variables are related to an MQTT topic, which will be sent together to the broker.

Figure 4 shows the workflow of the internal diagram between the tasks.

![workflow internal server](/Documentation/Images/internal_server_process.png)
**Figure 4.** *Internal server workflow diagram.* 

The broker is at the heart of any publish/subscribe protocol. The broker is responsible for receiving all messages, filtering the messages, determining who is subscribed to each message, and sending the message to these subscribed clients. The broker also holds the session data of all clients that have persistent sessions, including subscriptions and missed messages. Another responsibility of the broker is the authentication and authorization of clients [15].

All the server infrastructure can be dockerized, giving the infrastructure the advantage that offers containerization, like portability, lightweighty and security. Figure 5 shows the whole server work.

![all servers](/Documentation/Images/Diagram_Server.png)
**Figure 5.** *Server dockerized workflow diagram* 

# 4. Implementations:

## 4.1. Cybersecurity:

All the communications susceptible to Man in the Middle attacks are encrypted using AES. Specifically, AES CBC (Cipher Block Chaining) operation mode, using a 128-bit key and a 128-bit initialization vector. In CBC mode, each block of plaintext is XORed with the previous ciphertext block before being encrypted. This way, each ciphertext block depends on all plaintext blocks processed up to that point. To make each message unique, an initialization vector must be used in the first block. The initialization vector can be generated randomly.
Other cybersecurity policies applied to the infrastructure can be the unique connection to the wi-fi network generated by the device in the configuration mode, the lack of the Internet in that phase, the avoidance of MQTT protocol and its threats in the device, or the dockerization of the server isolate it.

## 4.2. Configurability:

The device is configurated thanks to a user graphical interface developed with HTML, for the structure, JavaScript, for the functionality, and some CSS for the style. All are summarized into a file called "init_page.html", which the web server running on the device sends to the client when the user searches in the browser "192.168.4.1". JavaScript is used to check user inputs and cipher the text inputs when being sent to the device, for that last one a pure JavaScript AES implementation library, called "aes-js", is employed. Something to emphasize is that the system doesn't have Internet access, which is good to avoid external hacking attacks, but it's a disadvantage when using JavaScript because it works with libraries referenced using the Internet. But it can be solved by writing in the library into the HTML code, it is 62 KB additional to a page of 3 KB, with a wi-fi board rate bit of 6,66 KBps it takes about 9 seconds to load the page. By becoming a better and more secure system the price to pay is in time. Making a system configurable could open vulnerabilities that previously doesn't exist, for that reason the configuration must be implemented bearing in mind all the possible leaking features which can be exploited. One is that the board doesn't support HTTPS, for that an HTTP combined with AES cipher is used.

## 4.3. MQTT & Broker

MQTT is implemented from the internal server towards the MQTT Broker and beyond. For its implementation, the "paho-mqtt" python library is employed in the server. The topics are defined by the internal server, the MQTT broker publishes them, and then each device or service must know the topic which it wants to access for each information. The topic has a directory string structure so it has an intuitive format. The internal server shares the following topics (where "iot_dev_01" refers to the identified IoT device):
```
Pico/iot_dev_01/Physiological_Data/Temperature
Pico/iot_dev_01/Physiological_Data/Pulse_Signal
Pico/iot_dev_01/Physiological_Data/Accelerometer/x
Pico/iot_dev_01/Physiological_Data/Accelerometer/y
Pico/iot_dev_01/Physiological_Data/Accelerometer/z
Pico/iot_dev_01//Internal_Device_Data/Temperature/MCU
Pico/iot_dev_01//Internal_Device_Data/Temperature/MPU
```
The Broker is implemented with the most powerful, open-source and industry employed nowadays, called EMQX. It's true that Mosquitto is the most used, but only in maker environments due to its lack of security.

# 4.4 External Applications using the data

The broker works as an API, where services request a directory (topic) and it sends you the information stored there, but with correct MQTT words, services subscribe to that topic and receive periodically the data that contain that topic. It can be employed by external applications like a dashboard. To show how easy is and how it works a dashboard application using NodeRed has been deployed as shown in Figure 6.

![nodered dashboard](/Documentation/Images/Dashboard.png)
**Figure 6.** *Dashboard application using NodeRed* 


## 4.5. Docker.

Docker offers standardization, being portable anywhere; lightweight, it only installs and uses resources that it will need; and security, isolating the programs and services running from the host machine. First, a dockerfile is used to configure specific dependencies that the containers need, like libraries, but based in an image. Then a docker-compose is used to run the containers. There are 3 containers running with different ports opened depending on the service:
- Python: 9998
- EMQX: 18083 and 1883
- NodeRed: 1880

# 5. Results:

To test all the infrastructure a python program has been written to simulate the behavior of the IoT medical device, calling it "pseudo_pico_client.py". It is implemented to avoid the costs of developing many IoT devices and test the multiclient infrastructure. Simultaneous clients are running at the same time using the infrastructure and it responds properly. Respecting the power consumption of the device in the previous work it was of 110 mAh and now in the configuration mode is _____ and in working mode with the encryption is _____ .

# 6. Conclusion:
# Acknowledgments:
# References:
[1] https://www.ibm.com/blogs/internet-of-things/what-is-the-iot/

[2] Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods. Practical IoT Hacking, The Definitive Guide to Attacking the Internet of Things. no starch press, 2021 (ISBN: 978-1718500907). Page 18.

[3] Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods. Practical IoT Hacking, The Definitive Guide to Attacking the Internet of Things. no starch press, 2021 (ISBN: 978-1718500907). Page 6.

[4] 

[5] Eric Knipp, Cisco Network Security. Syncress, 2002 (ISBN: 978-1931836562)

[6] Jean-Philippe Aumsson. Serious Cryptography, A Practical Introduction to Modern Encryption. no starch press, 2017 (ISBN: 978-1593278267). Page 59.

[7] https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

[8] K. Siva Kumar Swamy, G.Sony, Ch.Jagadeesh Ram, B.Navven ,J.Harshitha. Secure IoT Devices using AES Encryption. Journal of Engineering Sciences. Vol 11, issue 4, 2020 (ISSN: 0377-9354)

[9] Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods. Practical IoT Hacking, The Definitive Guide to Attacking the Internet of Things. no starch press, 2021 (ISBN: 978-1718500907). Page 73.

[10] Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods. Practical IoT Hacking, The Definitive Guide to Attacking the Internet of Things. no starch press, 2021 (ISBN: 978-1718500907). Page 74.

[11] Mohammad Al-Mashhadani, Mohamed Shujaa. IoT Security Using AES Encryption Technology based ESP32 Platform. The International Arab Journal of Information Technology, vol 19, no 2, 2022 (ISSN: 1683-3198)

[12] Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods. Practical IoT Hacking, The Definitive Guide to Attacking the Internet of Things. no starch press, 2021 (ISBN: 978-1718500907). Page 18.

[13] Meryam Saad Fadhil, Alaa Kadhim Farhan, Mohammad Natiq Fadhil. A lightweight AES Algorithm Implementation for Secure IoT Environment. Iraqi Journal of Science, vol 62, no 8, 2021, pp: 2759-2770 (ISSN: 0067-2904)

[14] J.Bermejo Torres, Development of a medical monitoring system based on the Internet of Things, Madrid, May 2022.

[15] https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/