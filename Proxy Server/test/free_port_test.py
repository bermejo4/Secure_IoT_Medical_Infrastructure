
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 0)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
port=sock.getsockname()[1]
print("the server port free is "+str(port))
sock.close()

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_off=('localhost', port)
# Listen for incoming connections
print('starting up on {} port {}'.format(*server_address_off))
sock1.bind(server_address_off)

sock1.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock1.accept()