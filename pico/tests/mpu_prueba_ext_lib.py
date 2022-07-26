
from mpu6050 import MPU6050



def data_collector():
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
        #cord_x=g.Gx
        #cord_y=g.Gy
        #cord_z=g.Gz
        print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}  Temp:{:.2f}".format(g.Gx,g.Gy,g.Gz,g.Temperature))
        #break



if __name__ == "__main__":
    data_collector()

