from lib2to3.pygram import python_grammar_no_print_statement
import socket
import os
from _thread import *
import subprocess

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def threaded_internal_servers(port_number):
    pass
    #while True:
        #out = subprocess.Popen(['python3', 'AesPythonServerToMQTT.py', str(port_number), '&'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #stdout,stderr = out.communicate()
        #print("stdout:"+str(stdout))
        #print("stdeer:"+str(stderr))
        #if "Address already in use" in str(stdout):
            #port_number=port_number+1
        #else:
            #break
        #out = subprocess.Popen(['python3', 'client_multi.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 





def threaded_client(connection):
    start_new_thread(threaded_internal_servers, (9995,))
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()