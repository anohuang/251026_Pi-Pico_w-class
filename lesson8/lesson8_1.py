from machine import Pin
import time #也可以寫成from time import sleep#

led_pin=15
led=Pin(led_pin, Pin.OUT)

while(True):
    led.toggle()
    time.sleep(2) #如果按上面註解裡的寫，那此處寫成sleep即可#