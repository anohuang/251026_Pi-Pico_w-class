from machine import Pin
from time import sleep

btn_pin=14
rled_pin=15
yled_pin=13

button=Pin(btn_pin, Pin.IN, Pin.PULL_UP)
rled=Pin(rled_pin, Pin.OUT)
yled=Pin(yled_pin, Pin.OUT)

while(True):
    if button.value()==0:
        rled.on()
        yled.off()
    else:
        rled.off()
        yled.on()
    
