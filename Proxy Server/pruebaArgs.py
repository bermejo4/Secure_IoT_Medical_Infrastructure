import sys
import os
from turtle import clear
import subprocess
import socket

#print(sys.argv)

#if sys.argv[len(sys.argv)-1]==sys.argv[0]:
    #print("No hay:"+str(sys.argv))
#else:
    #print("Hay:"+str(sys.argv))




def deploy_new_AesPythonServerToMQTT(port_number):
    #resp=os.system('python3 AesPythonServerToMQTT.py ' +str(port_number)+' &')

    while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port_number)) == 0:
                    s.close() 
                    print("Puerto: "+ str(port_number)+" ocupado, siguiente puerto.")
                    port_number=port_number+1
                else:
                    s.close() 
                    break
    subprocess.Popen(['python3', 'AesPythonServerToMQTT.py', str(port_number)])
    return port_number

    #while True: 
        #try:
            #ClientSocket.connect((host, port))
            #break
        #except socket.error as e:
            #print(str(e))
            #port_number=port_number+1
    #return port_number
    #while True:
        #out = subprocess.Popen(['python3', 'AesPythonServerToMQTT.py', str(port_number)])
        #if :
            #port_number=port_number+1
        #else:
            #break
    #return port_number

    #while True:
        #out = subprocess.run(['python3', 'AesPythonServerToMQTT.py', str(port_number), '&'], capture_output=True, text=True)
        #stdout,stderr = out.communicate()
        #print("stdout:"+str(stdout))
        #print("stdeer:"+str(stderr))
        #if "Address already in use" in str(stdout):
            #port_number=port_number+1
        #else:
            #break
    #return port_number

   # while True:
   #     try:
   #         resp=os.system('python3 AesPythonServerToMQTT.py '+str(port_number))
   #         print("Respuesta:"+str(resp))
   #         return port_number
   #     except OSError:
   #         print("this port is in use, we try other up")
   #         port_number=port_number+1
    


print("portnumber:"+str(deploy_new_AesPythonServerToMQTT(10004)))
print("creo que ha salido bien.")

