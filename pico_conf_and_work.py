import sys
import maes
import ubinascii
import maes_decrypter
import maes_encrypter
import uos
import machine
import utime
from machine import Pin
import DataExterCollector
from mpu6050 import MPU6050
import json


recv_buf="" # receive buffer global variable
uart0 = machine.UART(0, baudrate=115200)
print(uart0)


def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res
def Connect_WiFi(cmd, uart=uart0, timeout=300):
    print("CMD: " + cmd)
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
    print()

def Send_AT_Cmd(cmd, uart=uart0, timeout=300):
    print("CMD: " + cmd)
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
    print()
    
def Wait_ESP_Rsp(uart=uart0, timeout=300):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
        
def html_to_strigline_transformer(html_file):
    file = open(html_file, "r")
    html_array=[]
    html_code=" "
    while True:
        if not html_code:
            break
        else:
            html_code=file.read(2000)
            #string_line=html_code.replace("\n","")
            #html_code=string_line
            string_line=html_code
            #string_line=html_code.replace("\t","")
            html_array.append(string_line)
    file.close()
    return html_array


def filter_response(response_string, delimiter1, delimiter2):
    tmp=response_string.partition(delimiter1)[2]
    tmp2=tmp.partition(delimiter2)[0]
    return tmp2
    

#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])
    
    output_yellow = Pin(2, Pin.OUT)
    CONF_MODE = Pin(3, Pin.IN) #green wire
    WORK_MODE = Pin(4, Pin.IN)  #blue _wire
    output_yellow.on()
    
    if CONF_MODE.value()==1:
        print('CONF_MODE_ACTIVATED')
        Send_AT_Cmd('AT\r\n')          #Test AT startup
        Send_AT_Cmd('AT+GMR\r\n')      #Check version information
        Send_AT_Cmd('AT+CIPSERVER=0\r\n')      #Check version information
        Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
        Send_AT_Cmd('AT+CWMODE=3\r\n') #Set the Wi-Fi 3=Station mode+AP, 1=staMode, 2=ApMode 
        Send_AT_Cmd('AT+CWSAP="Med_IoT","",11,0,3\r\n') #ssid, passwd, channel, encryp_mod, max_stations
        #encryp_mod: 0: OPEN//2: WPA_PSK//3: WPA2_PSK//4: WPA_WPA2_PSK
        Send_AT_Cmd('AT+CIPMUX=1\r\n') #Establish TCP connections, 0=single 1=Multiple
        utime.sleep(1.0)
        Send_AT_Cmd('AT+CIPSERVER=1,80\r\n')    #Enable web server port 80
        utime.sleep(1.0)
        print ('Starting connection to ESP8266...')
        html_array=html_to_strigline_transformer('init_page.html')
        while True:
            res =""
            res=Rx_ESP_Data()
            utime.sleep(2.0)
            if '+IPD' in res: # if the buffer contains IPD(a connection), then respond with HTML handshake
                id_index = res.find('+IPD')
                if 'server_ip' in res:
                    print('+++++++++++++++++++++++++')
                    SERVER_IP_ENCRYPTED=filter_response(res, 'server_ip=', '&')
                    SERVER_PORT_ENCRYPTED=filter_response(res, 'server_port=', '&')
                    WIFI_NAME_ENCRYPTED=filter_response(res, 'wifi_name=', '&')
                    WIFI_PASS_ENCRYPTED=filter_response(res, 'wifi_pass=', ' HTTP/1.1')
                    print('Server_ip:'+SERVER_IP_ENCRYPTED)
                    print('Server_port:'+SERVER_PORT_ENCRYPTED)
                    print('Wifi name:'+WIFI_NAME_ENCRYPTED)
                    print('Wifi password:'+WIFI_PASS_ENCRYPTED)
                    print('+++++++++++++++++++++++++')
                    utime.sleep(1)
                    break
                print("resp:")
                print(res)
                connection_id =  res[id_index+5]
                print("connectionId:" + connection_id)
                print ('! Incoming connection - sending webpage')
                #print(html1+"----html1------"+str(len(html1)))
                for segment in html_array:
                    #print(segment)
                    uart0.write('AT+CIPSEND='+connection_id+','+ str(len(segment)) + '\r\n')  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
                    #uart0.write('AT+CIPSEND='+connection_id+','+ str(700) + '\r\n')
                    utime.sleep_ms(100)
                    #uart0.write('HTTP/1.1 200 OK'+'\r\n')
                    #uart0.write('Content-Type: text/html'+'\r\n')
                    #uart0.write('Connection: close'+'\r\n')
                    #uart0.write(''+'\r\n')
                    #uart0.write('<!DOCTYPE HTML>'+'\r\n')
                    #html ='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong></strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
                    uart0.write(segment +'\r\n')
                    utime.sleep_ms(250)
                    #print(html2+"-----html2------"+str(len(html2)))
                #uart0.write('AT+CIPSEND='+connection_id+','+ str(len(html2)) + '\r\n')  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
                #uart0.write('AT+CIPSEND='+connection_id+','+ str(700) + '\r\n')
                #utime.sleep(1.0)
                #uart0.write(html2 +'\r\n')
                #uart0.write('HTTP/1.1 200 OK'+'\r\n')
                #uart0.write('Content-Type: text/html'+'\r\n')
                #uart0.write('Connection: close'+'\r\n')
                #uart0.write(''+'\r\n')
                #uart0.write('<!DOCTYPE HTML>'+'\r\n')
                #html ='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong></strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
                #uart0.write(html2 +'\r\n')
                #utime.sleep(5.0)
                #print(html2+"-----html2------"+str(len(html2)))
                #uart0.write('AT+CIPSEND='+connection_id+','+ str(len(html3)) + '\r\n')  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
                #uart0.write('AT+CIPSEND='+connection_id+','+ str(700) + '\r\n')
                #utime.sleep(1.0)
                #uart0.write(html3 +'\r\n')
                #uart0.write('HTTP/1.1 200 OK'+'\r\n')
                #uart0.write('Content-Type: text/html'+'\r\n')
                #uart0.write('Connection: close'+'\r\n')
                #uart0.write(''+'\r\n')
                #uart0.write('<!DOCTYPE HTML>'+'\r\n')
                #html ='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong></strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
                #uart0.write(html3 +'\r\n')
                #utime.sleep(5.0)
                utime.sleep(4)
                Send_AT_Cmd('AT+CIPCLOSE='+ connection_id+'\r\n') # once file sent, close connection
                utime.sleep(3)
                res="" #reset buffer
                print ('Waiting For connection...')
        #Decryption:
        SERVER_IP = maes_decrypter.decrypt_cipher_data(SERVER_IP_ENCRYPTED)
        SERVER_PORT = maes_decrypter.decrypt_cipher_data(SERVER_PORT_ENCRYPTED)
        WIFI_NAME = maes_decrypter.decrypt_cipher_data(WIFI_NAME_ENCRYPTED)
        WIFI_PASS = maes_decrypter.decrypt_cipher_data(WIFI_PASS_ENCRYPTED)
        print('Server_ip:'+SERVER_IP)
        print('Server_port:'+SERVER_PORT)
        print('Wifi_name:'+WIFI_NAME)
        print('Wifi_password:'+WIFI_PASS)
        
        f = open ('conf_file.txt','w')
        f.write('{\"Server_ip\":\"'+SERVER_IP+'\",\n'+'\"Server_port\":\"'+SERVER_PORT+'\",\n'+'\"Wifi_name\":\"'+WIFI_NAME+'\",\n'+'\"Wifi_password\":\"'+WIFI_PASS+'\"}')
        f.close()
        #Changing to Second Phase:
    #Send_AT_Cmd('AT+CWMODE=1\r\n') NO SE TE OLVIDE DESCOMENTAR ESTAS DOS LINEAS
    #utime.sleep(3)
    if WORK_MODE.value()==1:
        print('WORK_MODE_ACTIVATED')
        file = open("conf_file.txt", "r")
        configuration=file.read()
        conf=json.loads(configuration)
        SERVER_IP=conf["Server_ip"]
        SERVER_PORT=conf["Server_port"]
        WIFI_NAME=conf["Wifi_name"]
        WIFI_PASS=conf["Wifi_password"]
        file.close()
    file = open("PKEYS_CLIENT_MOD.txt", "r")
    keys_as_client_file=file.read()
    key_as_client=json.loads(keys_as_client_file)
    KEY=key_as_client["key"]
    IV=key_as_client["iv"]
    print(KEY)
    print(IV)    
    string_to_send=DataExterCollector.data_collector()
    print(string_to_send)
    string_to_send=maes_encrypter.encrypt_data(KEY.encode('ascii'), IV.encode('ascii'), DataExterCollector.data_collector().encode('ascii'))
    print(string_to_send)

    
    
        
        
    
    
