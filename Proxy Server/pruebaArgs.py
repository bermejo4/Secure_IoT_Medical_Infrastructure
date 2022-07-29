import sys
import os
from turtle import clear
import subprocess

print(sys.argv)

if sys.argv[len(sys.argv)-1]==sys.argv[0]:
    print("No hay:"+str(sys.argv))
else:
    print("Hay:"+str(sys.argv))



def deploy_new_AesPythonServerToMQTT(port_number):
    while True:
        out = subprocess.run(['python3', 'AesPythonServerToMQTT.py', str(port_number), '&'], capture_output=True, text=True)
        stdout,stderr = out.communicate()
        print("stdout:"+str(stdout))
        print("stdeer:"+str(stderr))
        if "Address already in use" in str(stdout):
            port_number=port_number+1
        else:
            break
    return port_number

   # while True:
   #     try:
   #         resp=os.system('python3 AesPythonServerToMQTT.py '+str(port_number))
   #         print("Respuesta:"+str(resp))
   #         return port_number
   #     except OSError:
   #         print("this port is in use, we try other up")
   #         port_number=port_number+1
    


print(deploy_new_AesPythonServerToMQTT(9998))