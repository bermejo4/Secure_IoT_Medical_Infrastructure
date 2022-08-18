from lib2to3.pygram import python_grammar_no_print_statement
import socket
import os
from _thread import *
import subprocess
import time

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 9998
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
    print('Proxy Server in '+str(socket.gethostbyname(socket.gethostname()))+' listens in port '+str(port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def deploy_new_AesPythonServerToMQTT(port_number):
    while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port_number)) == 0:
                    s.close() 
                    print("[Multiserver Says:]"+" Port: "+ str(port_number)+" used, trying the next port.")
                    port_number=port_number+1
                else:
                    s.close() 
                    break
    subprocess.Popen(['python3', 'AesPythonServerToMQTT.py', str(port_number)])
    #xterm -e "python3 pseudo_pico_client.py 2" &
    #command= "python3 AesPythonServerToMQTT.py "+str(port_number)
    #subprocess.Popen(['xterm','-e','python3', 'AesPythonServerToMQTT.py', str(port_number),'&'])
    return port_number 



def threaded_client(connection):
    server_deployed_port_number=deploy_new_AesPythonServerToMQTT(10700)
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', server_deployed_port_number)
    try:
        sock.connect(server_address)
    except socket.error as e:
        print("Conexion Rechazada, mensaje: "+str(e))
    #connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(263)
        #reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        #connection.sendall(str.encode(reply))
        sock.sendall(data)
    connection.close()
    sock.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ' : ' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()