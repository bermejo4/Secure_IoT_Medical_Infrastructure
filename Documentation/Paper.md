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



### 3.2.1. Client.
### 3.2.2. Server.
# 4. Implementations:
## 4.1. Configurability:
## 4.2. Cybersecurity:
## 4.3. Multiclient Server.
## 4.4. MQTT & Broker
## 4.5. Docker.
# 5. Results:
Power consumption 
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