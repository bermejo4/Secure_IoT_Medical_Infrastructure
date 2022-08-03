import binascii
import json
from mimetypes import init
import socket
import sys
from matplotlib import pyplot as plt
import numpy as np
from pip import main
from scipy.misc import electrocardiogram
from _thread import *
import time
from Crypto.Cipher import AES



class Pseudo_Pico():
    def __init__(self):
        self.pulse_signal=[]
        self.patient_temp=36.6
        self.accelerometer_x=0
        self.accelerometer_y=0
        self.accelerometer_z=0
        self.mcu_temp=23.7
        self.mpu_temp=23.4
    
    def initialize_ecg(self):
        self.pulse_signal=self.ecg_transformation()
    
    def ecg_transformation(self):
        ecg = electrocardiogram()
        new_ecg=[ecg[0]]
        ecg2=electrocardiogram()[0:1600]
        #print("Ecg2: "+str(ecg2))
        counter=0
        for val in ecg:
            if counter == 5:
                new_ecg.append(val+2)
                counter=0
            else:
                counter=counter+1
        new_ecg2=new_ecg[0:400]
        return new_ecg2
    
    def JSON_transform(self, moment):
        data_string="{"\
                     +"\"Temp\":\""+"{:.3f}".format(self.patient_temp)+"\""\
                     +",\"TempMcu\":\""+"{:.3f}".format(self.mcu_temp)+"\""\
                     +",\"PulseSig\":\""+"{:.3f}".format(self.pulse_signal[moment])+"\""\
                     +",\"Acel_x\":\""+"{:.3f}".format(self.accelerometer_x)+"\""\
                     +",\"Acel_y\":\""+"{:.3f}".format(self.accelerometer_y)+"\""\
                     +",\"Acel_z\":\""+"{:.3f}".format(self.accelerometer_z)+"\""\
                     +",\"TempMpu\":\""+"{:.3f}".format(self.mpu_temp)+"\""\
                     +"}"
        #print("Data String: "+ data_string)
        return data_string


def conexion_to_server(SERVER_PORT, device_id):
    SERVER_IP = 'localhost'
    #SERVER_PORT = 9998
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (SERVER_IP, SERVER_PORT)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        counter = 0
        while True:
            if counter == 399:
                counter = 0
            counter = counter+1
            # Send data
            #print("counter:"+str(counter))
            time.sleep(0.05)
            message = cipher_data_chain_builder(device_id, str(pico.JSON_transform(counter)))
            #print("Message sending:"+str(message))
            message = message.encode()
            #message = b'This is the message.  It will be repeated.'
            #print('sending {!r}'.format(message))
            sock.sendall(message)

    finally:
        print('closing socket')
        sock.close()

def modification_menu():
    option = 0
    print(
        "If you want to change some parameter indicate the number option:\n"+
        "1. Increase (+) the patient temperature 0.5ºC.\n"+
        "2. Decrease (-) the patient temperature 0.5ºC.\n"+
        "3. Increase (+) the MCU temperature 0.5ºC.\n"+
        "4. Decrease (-) the MCU temperature 0.5ºC.\n"+
        "5. Increase (+) the MPU temperature 0.5ºC.\n"+
        "6. Decrease (-) the MPU temperature 0.5ºC.\n"+
        "-----------------------------------------------\n"+
        "7. Increase (+) 0.1 the X Acceleromenter component\n"+
        "8. Decrease (-) 0.1 the X Acceleromenter component\n"+
        "9. Increase (+) 0.1 the Y Acceleromenter component\n"+
        "10. Decrease (-) 0.1 the Y Acceleromenter component\n"+
        "11. Increase (+) 0.1 the Z Acceleromenter component\n"+
        "12. Decrease (-) 0.1 the Z Acceleromenter component\n"+
        "-----------------------------------------------\n\n"
        )

    while True:
        try:
            option = int(input("Insert your option (number):"))
            if option<=0:
                raise ValueError
            elif option>=13:
                raise ValueError
            break
        except ValueError:
            print("Oops!  That was no valid number or option.  Try again...\n")
    return option

def modification_pico_paramenters_manually(option):
    if option == 1:
        pico.patient_temp = pico.patient_temp + 0.5
    elif option == 2:
        pico.patient_temp = pico.patient_temp - 0.5
    elif option == 3:
        pico.mcu_temp = pico.mcu_temp + 0.5
    elif option == 4:
        pico.mcu_temp = pico.mcu_temp - 0.5
    elif option == 5:
        pico.mpu_temp = pico.mpu_temp + 0.5
    elif option == 6:
        pico.mpu_temp = pico.mpu_temp - 0.5
    elif option == 7:
        if (pico.accelerometer_x + 0.1) > 1:
            pico.accelerometer_x = 1 - ((pico.accelerometer_x+0.1) - 1)
        else:
            pico.accelerometer_x = pico.accelerometer_x + 0.1
    elif option == 8:
        if (pico.accelerometer_x - 0.1) < -1:
            pico.accelerometer_x = -1 + (-1*((pico.accelerometer_x-0.1) + 1))
        else:
            pico.accelerometer_x = pico.accelerometer_x - 0.1
    elif option == 9:
        if (pico.accelerometer_y + 0.1) > 1:
            pico.accelerometer_y = 1 - ((pico.accelerometer_y+0.1) - 1)
        else:
            pico.accelerometer_y = pico.accelerometer_y + 0.1
    elif option == 10:
        if (pico.accelerometer_y - 0.1) < -1:
            pico.accelerometer_y = -1 + (-1 * ((pico.accelerometer_y - 0.1) + 1))
        else:
            pico.accelerometer_y = pico.accelerometer_y - 0.1
    elif option == 11:
        if (pico.accelerometer_z + 0.1) > 1:
            pico.accelerometer_z = 1 - ((pico.accelerometer_z + 0.1) - 1)
        else:
            pico.accelerometer_z = pico.accelerometer_z + 0.1
    elif option == 12:
        if (pico.accelerometer_z - 0.1) < -1:
            pico.accelerometer_z = -1 + (-1 *( (pico.accelerometer_z - 0.1) + 1))
        else:
            pico.accelerometer_z = pico.accelerometer_z - 0.1

def load_keys(device_id):
    json_dict={}
    device_searched=""
    f = open("KEY_PSEUDO_PICO.txt", "r")
    while True:
        linea=f.readline()
        if linea=='':
            break
        else:
            device=json.loads(linea)
            json_dict[device["id"]]=[device["key"], device["iv"]]
    #print("json_dict:"+str(json_dict))
    key=json_dict[str((int(device_id)))][0]
    iv=json_dict[str((int(device_id)))][1]
    return key, iv

def clean_string_binary_remains(binary_string):
    tmp=binary_string.replace('\'','')
    tmp=tmp.replace('b','', 1)
    return tmp

def add_until_16(word):
    for i in range(16-len(word)):
        word+='&'
    return word


def cipher_data_chain_builder(device_id, data):
    KEY, IV = load_keys(device_id)
    chain = ""
    while len(data)>=16:
        ciphertext = encrypt_data_by_16_block(data[0:16], KEY, IV)
        cifrado_limpio=clean_string_binary_remains(str(binascii.hexlify(ciphertext)))
        chain+=cifrado_limpio
        chain+="+"
        data=data[16:len(data)]
    if len(data)<16:
        ciphertext = encrypt_data_by_16_block(add_until_16(data),KEY, IV)
        cifrado_limpio=clean_string_binary_remains(str(binascii.hexlify(ciphertext)))
        chain+=cifrado_limpio
    return chain


def encrypt_data_by_16_block(text, key, iv):
    obj = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    message = text
    ciphertext = obj.encrypt(message.encode("utf8"))
    return ciphertext

pico=Pseudo_Pico()


if __name__ == '__main__':
    print("return load keys: "+str(load_keys(sys.argv[1])))
    #if sys.argv[len(sys.argv)-1]==sys.argv[0]:
        #print("No hay:"+str(sys.argv))
    #else:
        #print("Hay:"+str(sys.argv))
    pico.initialize_ecg()
    start_new_thread(conexion_to_server, (9998, sys.argv[1], ))
    while True:
        option=modification_menu()
        print("Selected option: "+str(option))
        modification_pico_paramenters_manually(option)
        print("aacel_z:"+str(pico.accelerometer_x))
        print(str(pico.JSON_transform(0)))
    

