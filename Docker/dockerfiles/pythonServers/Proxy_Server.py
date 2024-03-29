import socket
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
ServerSocket.listen(10)

def free_port_looking():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 0)
    sock.bind(server_address)
    port=sock.getsockname()[1]
    sock.close()
    return port


def deploy_new_AesPythonServerToMQTT():
    #print("Entro en deploy_new_AesPythonServerToMQTT con el intento de puerto "+str())
    port_number=free_port_looking()
    subprocess.Popen(['python3', 'AesPythonServerToMQTT.py', str(port_number)])
    #xterm -e "python3 pseudo_pico_client.py 2" &
    #command= "python3 AesPythonServerToMQTT.py "+str(port_number)
    #subprocess.Popen(['xterm','-e','python3', 'AesPythonServerToMQTT.py', str(port_number),'&'])
    return port_number 

def fill_ip_and_port_string_until_21(string):
    if len(string)==21:
        return string
    else:
        difference=21-len(string)
        for num in range(difference):
            string=string+'@'
        return string



def threaded_client(connection):
    #print("entro en thread client")
    server_deployed_port_number=deploy_new_AesPythonServerToMQTT()
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', server_deployed_port_number)
    try:
        sock.connect(server_address)
    except socket.error as e:
        print("Conexion Rechazada, mensaje: "+str(e))
    #connection.send(str.encode('Welcome to the Servern'))
    ip_and_port_dev=str(address[0])+"&"+str(address[1])
    sock.sendall(fill_ip_and_port_string_until_21(ip_and_port_dev).encode())
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