import uos
import machine
import utime
from machine import Pin

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
    html_code=str(file.read())
    file.close()
    string_line=html_code.replace("\n","")
    html_code=string_line
    string_line=html_code.replace("\t","")
    return string_line

def find_ip_server(response_string):
    tmp=response_string.partition('server_ip=')[2]
    tmp2=tmp.partition('&')[0]
    return tmp2

def find_port_server(response_string):
    tmp=response_string.partition('server_port=')[2]
    tmp2=tmp.partition(' HTTP/1.1')[0]
    return tmp2
    

#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])
    
    Send_AT_Cmd('AT\r\n')          #Test AT startup
    Send_AT_Cmd('AT+GMR\r\n')      #Check version information
    Send_AT_Cmd('AT+CIPSERVER=0\r\n')      #Check version information
    Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
    Send_AT_Cmd('AT+CWMODE=3\r\n') #Set the Wi-Fi mode = Station mode
    Send_AT_Cmd('AT+CIPMUX=1\r\n')    #
    utime.sleep(1.0)
    Send_AT_Cmd('AT+CIPSERVER=1,80\r\n')    #
    utime.sleep(1.0)
    print ('Starting connection to ESP8266...')
    html=html_to_strigline_transformer('init_page.html')
    print(html)
    while True:
        res =""
        res=Rx_ESP_Data()
        utime.sleep(2.0)
        if '+IPD' in res: # if the buffer contains IPD(a connection), then respond with HTML handshake
            id_index = res.find('+IPD')
            if 'server_ip' in res:
                print('+++++++++++++++++++++++++')
                SERVER_IP=find_ip_server(res)
                SERVER_PORT=find_port_server(res)
                print('Server_ip:'+SERVER_IP)
                print('Server_port:'+SERVER_PORT)
                print('+++++++++++++++++++++++++')
                utime.sleep(1)
            print("resp:")
            print(res)
            connection_id =  res[id_index+5]
            print("connectionId:" + connection_id)
            print ('! Incoming connection - sending webpage')
            print(html)
            uart0.write('AT+CIPSEND='+connection_id+','+ str(len(html)) + '\r\n')  #Send a HTTP response then a webpage as bytes the 108 is the amount of bytes you are sending, change this if you change the data sent below
            utime.sleep(1.0)
            uart0.write('HTTP/1.1 200 OK'+'\r\n')
            uart0.write('Content-Type: text/html'+'\r\n')
            uart0.write('Connection: close'+'\r\n')
            uart0.write(''+'\r\n')
            uart0.write('<!DOCTYPE HTML>'+'\r\n')
            #html ='<html> <head> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <link rel=\"stylesheet\" href=\"https://use.fontawesome.com/releases/v5.7.2/css/all.css\" integrity=\"sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr\" crossorigin=\"anonymous\"> <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; } .button { background-color: #ce1b0e; border: none; color: white; padding: 16px 40px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; } .button1 { background-color: #000000; } </style> </head> <body> <h2>Raspberry Pi Pico Web Server</h2> <p>LED state: <strong></strong></p> <p> <i class=\"fas fa-lightbulb fa-3x\" style=\"color:#c81919;\"></i> <a href=\\\"?led_on\\\"><button class=\"button\">LED ON</button></a> </p> <p> <i class=\"far fa-lightbulb fa-3x\" style=\"color:#000000;\"></i> <a href=\\\"?led_off\\\"><button class=\"button button1\">LED OFF</button></a> </p> </body> </html>'
            uart0.write(html +'\r\n')
            utime.sleep(9.0)
            Send_AT_Cmd('AT+CIPCLOSE='+ connection_id+'\r\n') # once file sent, close connection
            utime.sleep(3.0)
            res="" #reset buffer
            print ('Waiting For connection...')