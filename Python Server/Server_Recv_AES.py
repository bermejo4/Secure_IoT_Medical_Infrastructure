#Bermejo4
import socket
import json
from Crypto.Cipher import AES
import binascii
import sys

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

def data_from_pico_desencrypter(text, key, iv):
    segundo=text
    data_decrypted = ''
    obj2 = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    for i in range(segundo.count('+') + 1):
        primer, segundo = segmentate_in_ciphered_strings(segundo)
        #print('primer: ' + primer)
        #print('segundo: ' + segundo)
        cifrado = primer.encode("utf8")
        cifra = binascii.unhexlify(cifrado)
        data_decrypted += clean_string_binary_remains(str(obj2.decrypt(cifra)))
        #print(obj2.decrypt(cifra))
    data_decrypted=data_decrypted.replace('&','')
    return data_decrypted

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
    print(json_dict)
    for a in json_dict:
        key=json_dict[a][0]
        iv=json_dict[a][1]
        print(data_from_pico_desencrypter(ciphertext, key, iv))
        if "Temp" in data_from_pico_desencrypter(ciphertext, key, iv):
            print("Founded: "+ a)
            device_searched=a
            break
        else:
            return "Not_found_dev",0,0
    return device_searched, json_dict[device_searched][0], json_dict[device_searched][1]


class Servidor:
    def __init__(self):
        self.IP_ADDRESS='0.0.0.0'
        self.PORT_ADDRESS=9999
        self.SERVER_ADDRESS=(self.IP_ADDRESS, self.PORT_ADDRESS)
        #self.fecha=str(date.today().day)+'/'+str(date.today().month)+'/'+str(date.today().year)
        #self.hora=str(datetime.now().hour)+':'+str(datetime.now().minute)

class DataPico:
    def __init__(self):
        self.temp_array_y = []
        self.temp_array_x = []
        self.temp_mcu_array_y = []
        self.temp_mcu_array_x = []
        self.pulse_array_y=[]
        self.pulse_array_x = []
        self.x_acel_array_y=[]
        self.x_acel_array_x = []
        self.y_acel_array_y=[]
        self.y_acel_array_x=[]
        self.z_acel_array_y=[]
        self.z_acel_array_x = []


ciphertext="b102ea0ad185e800792364c204a18248+eddde8a2d9f314ba1181677d75192b83+f1b05010657ce23b94d935b362ba3910+6b9c88c72dfa3a247d02c24e8ffdaf4c+6968a09c1fb9d64c364d76be162a0b14+49f657df4bcf47479cab8d034a0c98cc+cafa765f1eaa23932dd5c93035eddb71+c8161a67c0467a922d64c0a1869c2ec5+c42e0f042a319174ce185ee19fa73445+7afa9091bc6336d5973a45d9895f4b67"
device_id, key, iv = autentication_and_ID_assignation(ciphertext)
if device_id=="Not_found_dev":
    print("POSSIBLE HACKING ATTACK DETECTED!!! SERVER DOWN")
    sys.exit()
print(device_id, key, iv )


server=Servidor()
socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(2)
solicitud = ''
print('Servidor escuchando en el puerto: ' + str(server.PORT_ADDRESS))
conexion, CLIENT_ADDRESS = socketTCP.accept()

atentication_check=False

while True:
        solicitud = ''
        solicitud = conexion.recv(400)
        print("solicitud:" + str(solicitud))
        print("\n")
        data_from_pico = solicitud.decode()
        print(data_from_pico)
        # data_json=json.loads(data_from_pico)
        print('RECIBOO:'+str(data_from_pico))
        ###----------------checkear si esto funciona:
        if not atentication_check:
            device_id, key, iv = autentication_and_ID_assignation(str(data_from_pico))
            if device_id=="Not_found_dev":
                print("POSSIBLE HACKING ATTACK DETECTED!!! SERVER DOWN")
                sys.exit()
            print(device_id, key, iv )
            atentication_check=True

        # data_pico_saved.temp_array[counter]=data_json["Temp"]
        # print(data_pico_saved)
        # print('Temperature: '+data_json["Temp"]+"ºC")
        # print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
        # print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
        # print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")
        if "+" in data_from_pico:
            print(data_from_pico_desencrypter(data_from_pico, KEY, IV))
            #data_json = json.loads(data_from_pico_desencrypter(data_from_pico))
            print('RECIBOO:' + str(data_from_pico))
            #data_pico_saved.temp_array_y.append(float(data_json["Temp"]))
            #data_pico_saved.temp_mcu_array_y.append(float(data_json["TempMcu"]))
            # data_pico_saved.pulse_array_y.append(float(data_json["PulseSig"]))
            # data_pico_saved.x_acel_array_y.append(float(data_json["Acel_x"]))
            # data_pico_saved.y_acel_array_y.append(float(data_json["Acel_y"]))
            # data_pico_saved.z_acel_array_y.append(float(data_json["Acel_z"]))
