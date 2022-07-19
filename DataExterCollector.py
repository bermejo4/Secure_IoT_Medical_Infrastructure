from mpu6050 import MPU6050
from machine import Pin, ADC, Signal
import utime
import machine



class pico_data:
    def __init__(self, temp=None, temp_mcu=None, pulse_sig=None, cord_x=None, cord_y=None, cord_z=None, temp_mpu=None):
        self.temp = temp
        self.temp_mcu = temp_mcu
        self.pulse_sig=pulse_sig
        self.cord_x=cord_x
        self.cord_y=cord_y
        self.cord_z=cord_z
        self.temp_mpu=temp_mpu
        
    def JSON_transform(self):
        data_string="{"\
                     +"\"Temp\":\""+str(self.temp)+"\""\
                     +",\"TempMcu\":\""+str(self.temp_mcu)+"\""\
                     +",\"PulseSig\":\""+str(self.pulse_sig)+"\""\
                     +",\"Acel_x\":\""+str(self.cord_x)+"\""\
                     +",\"Acel_y\":\""+str(self.cord_y)+"\""\
                     +",\"Acel_z\":\""+str(self.cord_z)+"\""\
                     +",\"TempMpu\":\""+str(self.temp_mpu)+"\""\
                     +"}"
        return data_string


def data_collector():
    pico=pico_data()
    #----------------------------------------------------
    #ACELEROMETER (SDA -> GP14, SCL -> GP15)
    UseFifo = True
    mpu = MPU6050()
    mpu.enableFifo(UseFifo)
    mpu.setSampleRate(40)
    mpu.setGyroResolution(250)
    mpu.setGResolution(2)
    while True:
        if UseFifo:
            byteCount = mpu.readFifoCount()
            if byteCount>= 14:
                g = mpu.convertData(mpu.readDataFromFifo(14))
            else:
                continue
        else:
            g=mpu.readData()
            #utime.sleep_ms(25)
        pico.cord_x=g.Gx
        pico.cord_y=g.Gy
        pico.cord_z=g.Gz
        pico.temp_mpu=g.Temperature
        #print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}  Temp:{:.2f}".format(g.Gx,g.Gy,g.Gz,g.Temperature))
        break
    #----------------------------------------------------
    #PULSE SIGNAL (SIGNAL -> GP26)
    pulse_sensor=machine.ADC(0)
    #utime.sleep(0.07)
    conversion_factor = 3.3 / (65535)
    signal_value = pulse_sensor.read_u16()*conversion_factor
    print(signal_value)
    pico.pulse_sig=signal_value
    #--------------------------------------------------
    #MCU TEMPERATURE
    sensortemp = machine.ADC(4)
    factorconversion = 3.3 / 65365
    rawValue = sensortemp.read_u16() * factorconversion
    temperatura_mcu = 27 - (rawValue - 0.706) / 0.001721
    pico.temp_mcu=temperatura_mcu
    #--------------------------------------------------
    #Returnind data in JSON Format:
    return pico.JSON_transform()

    

#To Test Sensors and code:
#-----------------------------------
# if __name__ == "__main__":
#     while True:
#         print(data_collector())


