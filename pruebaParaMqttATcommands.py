import sys
import maes
import ubinascii
import maes_decrypter
import uos
import machine
import utime
from machine import Pin
import DataExterCollector
from mpu6050 import MPU6050


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

if __name__ == "__main__":
    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])
    
    Send_AT_Cmd('AT\r\n')          #Test AT startup
    Send_AT_Cmd('AT+GMR\r\n')      #Check version information
    Send_AT_Cmd('AT+cpin?\r\n') 