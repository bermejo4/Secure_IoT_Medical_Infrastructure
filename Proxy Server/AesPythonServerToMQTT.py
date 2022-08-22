#Bermejo4
from encodings import utf_8
import socket
import json
from Crypto.Cipher import AES
import binascii
import sys
import random
import time
from paho.mqtt import client as mqtt_client


def segmentate_in_ciphered_strings(cadena):
    first=''
    for letter in cadena:
        if letter == '+':
            cadena=cadena.replace('+','',1)
            #print('cadena:'+cadena)
            break
        else:
            first+=letter
    return first, cadena.replace(first,'')

def clean_string_binary_remains(binary_string):
    tmp=binary_string.replace('\'','')
    tmp=tmp.replace('b','',1)
    return tmp

def data_from_pseudo_pico_desencrypter(text, key, iv):
    segundo=text
    data_decrypted = ''
    obj2 = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    for i in range(segundo.count('+') + 1):
        primer, segundo = segmentate_in_ciphered_strings(segundo)
        cifrado = primer.encode("utf-8")
        obj2 = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        cifra = binascii.unhexlify(cifrado)
        data_decrypted += clean_string_binary_remains(str(obj2.decrypt(cifra)))
        primer=''
    data_decrypted=data_decrypted.replace('&','')
    return data_decrypted

def data_from_pico_desencrypter(text, key, iv):
    segundo=text
    data_decrypted = ''
    obj2 = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    for i in range(segundo.count('+') + 1):
        primer, segundo = segmentate_in_ciphered_strings(segundo)
        cifrado = primer.encode("utf-8")
        #obj2 = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
        cifra = binascii.unhexlify(cifrado)
        data_decrypted += clean_string_binary_remains(str(obj2.decrypt(cifra)))
        primer=''
    data_decrypted=data_decrypted.replace('&','')
    return data_decrypted

def check_words_in_decrypted_string(text):
    if "\"Temp\"" in text:
        print("temp_si:"+text)
        if "\"TempMcu\"" in text:
            print("temp_mcu_si")
            if "\"PulseSig\"" in text:
                print("pulse_sig_si")
                if "\"Acel_x\"" in text:
                    print("accel_x_si")
                    if "\"Acel_y\"" in text:
                        print("accel_y_si")
                        if "\"Acel_z\"" in text:
                            print("accel_z_si")
                            if "\"TempMpu\"" in text:
                                print("temp_mpu_si")
                                return True
    return False


def autentication_and_ID_assignation(ciphertext):
    #this function read DEVICES_KEYS.txt and check the ciphertext with each key in the file to identify devices.
    json_dict={}
    device_searched=""
    f = open("DEVICES_KEYS.txt", "r")
    while True:
        linea=f.readline()
        if linea=='':
            break
        else:
            device=json.loads(linea)
            json_dict[device["id"]]=[device["key"], device["iv"]]
    #print(json_dict)
    for a in json_dict:
        #print("a:"+a)
        key=json_dict[a][0]
        iv=json_dict[a][1]
        #print("Key used:"+str(key)+"// Iv used:"+str(iv)+"|")
        #print("Data from pico desencripted:"+str(data_from_pico_desencrypter(ciphertext, key, iv)))
        if check_words_in_decrypted_string(data_from_pseudo_pico_desencrypter(ciphertext, key, iv)):
            print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+"Founded: "+ a)
            device_searched=a
            simulator_mode=True
            break
        if check_words_in_decrypted_string(data_from_pico_desencrypter(ciphertext, key, iv)):
            print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+"Founded: "+ a)
            device_searched=a
            simulator_mode=False
            break

    if device_searched=="":
        return "Not_found_dev",0,0

    return device_searched, json_dict[device_searched][0], json_dict[device_searched][1], simulator_mode


def connect_mqtt(client_id, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+"Connected to MQTT Broker!")
        else:
            print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+"Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    #msg = f"messages: {msg_count}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        pass
        #print(f"Send `{msg}` to topic `{topic}`")
    else:
        pass
        #print(f"Failed to send message to topic {topic}")


class Servidor:
    def __init__(self, port_address):
        self.IP_ADDRESS='0.0.0.0'
        self.PORT_ADDRESS=int(port_address)
        self.SERVER_ADDRESS=(self.IP_ADDRESS, self.PORT_ADDRESS)
        #self.fecha=str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year)
        #self.hora=str(datetime.now().hour)+':'+str(datetime.now().minute)

class DataPico:
    def __init__(self):
        self.temp_array = []
        self.temp_mcu_array = []
        self.pulse_array=[]
        self.x_acel_array=[]
        self.y_acel_array=[]
        self.z_acel_array = []
        self.temp_mpu_array = []

class Mqtt_publisher:
    def __init__(self, device_id):
        self.broker = 'localhost'
        self.port = 1883
        self.topic = [
            "Pico/"+device_id+"/Physiological_Data/Temperature", #0
            "Pico/"+device_id+"/Physiological_Data/Pulse_Signal", #1
            "Pico/"+device_id+"/Physiological_Data/Accelerometer/x", #2
            "Pico/"+device_id+"/Physiological_Data/Accelerometer/y", #3
            "Pico/"+device_id+"/Physiological_Data/Accelerometer/z", #4
            "Pico/"+device_id+"/Internal_Device_Data/Temperature/MCU", #5
            "Pico/"+device_id+"/Internal_Device_Data/Temperature/MPU", #6
            "Pico/"+device_id+"/Ip_address", #7
            "Pico/"+device_id+"/Port_address", #8
            "Pico/"+device_id+"/Internal_Server/Ip_address", #9
            "Pico/"+device_id+"/Internal_Server/Port_address" #10

        ]
        self.client_id = device_id
        # username = 'emqx'
        # password = 'public'


    

if sys.argv[len(sys.argv)-1]==sys.argv[0]:
    #print("No hay:"+str(sys.argv))
    server=Servidor(10700)
else:
    #print("Hay:"+str(sys.argv))
    server=Servidor(sys.argv[1])


socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(1)
solicitud = ''
print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+'Server listening in the port: ' + str(server.PORT_ADDRESS))

extra_info=49
device_ip_address="none"
device_port_address="none"

first_package=True

#simulator_mode=False

while True:
    conexion, CLIENT_ADDRESS = socketTCP.accept()

    atentication_check=False


    while True:
            solicitud = ''
            if first_package:
                solicitud = conexion.recv(21)
                first_package=False
            else:   
                solicitud = conexion.recv(263)
            #print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+ "solicitud:" + str(solicitud))
            data_from_pico = solicitud.decode()
            #print("\n")
            #print(data_from_pico)
            # data_json=json.loads(data_from_pico)
            #print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+'RECIBO:'+str(data_from_pico))
            ###----------------checkear si esto funciona:
            if '&' in data_from_pico:
                data_from_pico=data_from_pico.replace('@','')
                dev_ip_and_port=data_from_pico.split("&")
                device_ip_address=dev_ip_and_port[0]
                device_port_address=dev_ip_and_port[1]
                #data_from_pico=dev_ip_and_port[2]
                print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+'Origin: '+str(data_from_pico))
            elif '+' in data_from_pico:
                if not atentication_check:
                    device_id, KEY, IV, simulator_mode = autentication_and_ID_assignation(str(data_from_pico))
                    if device_id=="Not_found_dev":
                        print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+"POSSIBLE HACKING ATTACK DETECTED!!! SERVER DOWN")
                        sys.exit()
                    mqtt_publisher=Mqtt_publisher(device_id)
                    client_mqtt_publisher = connect_mqtt(mqtt_publisher.client_id , mqtt_publisher.broker, mqtt_publisher.port)
                    print(device_id, KEY, IV)
                    atentication_check=True

                #print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+'RECIBOO:' + str(data_from_pico))
                if simulator_mode:
                    data_string=data_from_pseudo_pico_desencrypter(data_from_pico, KEY, IV)
                else:
                    data_string=data_from_pico_desencrypter(data_from_pico, KEY, IV)
                print("Data String:"+str(data_string))
                pico=json.loads(data_string)
                publish(client_mqtt_publisher,mqtt_publisher.topic[0] , str(pico["Temp"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[1] , str(pico["PulseSig"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[2] , str(pico["Acel_x"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[3] , str(pico["Acel_y"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[4] , str(pico["Acel_z"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[5] , str(pico["TempMcu"]))
                publish(client_mqtt_publisher,mqtt_publisher.topic[6] , str(pico["TempMpu"]))
                extra_info=extra_info+1
                if extra_info==50:
                    extra_info=0
                    publish(client_mqtt_publisher,mqtt_publisher.topic[7] , str(device_ip_address))
                    publish(client_mqtt_publisher,mqtt_publisher.topic[8] , str(device_port_address))
                    publish(client_mqtt_publisher,mqtt_publisher.topic[9] , str(socket.gethostbyname(socket.gethostname())))
                    publish(client_mqtt_publisher,mqtt_publisher.topic[10] , str(socketTCP.getsockname()[1]))

            else:
                print("Server in port ["+str(server.PORT_ADDRESS)+"] says: "+'Received: '+str(data_from_pico))
                print("Server in port ["+str(server.PORT_ADDRESS)+"] says:"+"Something strange received, CLOSING CONNECTION")
                conexion.close()
                print("Server in port ["+str(server.PORT_ADDRESS)+"] says:"+"SERVER CLOSED")
                sys.exit()
                break
