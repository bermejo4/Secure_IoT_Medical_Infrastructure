from machine import Pin

output_yellow = Pin(2, Pin.OUT)
input_green = Pin(3, Pin.IN)
input_blue = Pin(4, Pin.IN)
output_yellow.on()
print('Verde_value:'+str(input_green.value()))
print('Azul_value:'+str(input_blue.value()))

if input_green.value()==1:
    print('verde')
if input_blue.value()==1:
    print('azul')