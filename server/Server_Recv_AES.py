#Bermejo4
import socket
import json
from Crypto.Cipher import AES
import binascii

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

def data_from_pico_desencrypter(text):
    segundo=text
    data_decrypted = ''
    obj2 = AES.new('1234567890123456'.encode("utf8"), AES.MODE_CBC, 'AAAAAAAAAAAAAAAA'.encode("utf8"))
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

server=Servidor()
socketTCP=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketTCP.bind(server.SERVER_ADDRESS)
socketTCP.listen(2)
solicitud = ''
print('Servidor escuchando en el puerto: ' + str(server.PORT_ADDRESS))
conexion, CLIENT_ADDRESS = socketTCP.accept()

while True:
        solicitud = ''
        solicitud = conexion.recv(400)
        print("solicitud:" + str(solicitud))
        print("\n")
        data_from_pico = solicitud.decode()
        print(data_from_pico)
        # data_json=json.loads(data_from_pico)
        print('RECIBOO:'+str(data_from_pico))
        # data_pico_saved.temp_array[counter]=data_json["Temp"]
        # print(data_pico_saved)
        # print('Temperature: '+data_json["Temp"]+"ºC")
        # print('Temperature from mcu: '+data_json["TempMcu"]+"ºC")
        # print('Pulse signal: ' + data_json["PulseSig"] + " Volts")
        # print('Acelerometer: (' + data_json["Acel_x"] + ","+data_json["Acel_y"]+","+data_json["Acel_z"]+")")
        if "+" in data_from_pico:
            print(data_from_pico_desencrypter(data_from_pico))
            #data_json = json.loads(data_from_pico_desencrypter(data_from_pico))
            print('RECIBOO:' + str(data_from_pico))
            #data_pico_saved.temp_array_y.append(float(data_json["Temp"]))
            #data_pico_saved.temp_mcu_array_y.append(float(data_json["TempMcu"]))
            # data_pico_saved.pulse_array_y.append(float(data_json["PulseSig"]))
            # data_pico_saved.x_acel_array_y.append(float(data_json["Acel_x"]))
            # data_pico_saved.y_acel_array_y.append(float(data_json["Acel_y"]))
            # data_pico_saved.z_acel_array_y.append(float(data_json["Acel_z"]))
