from machine import Pin
from time import sleep

btn_pin=14
rled_pin=15
yled_pin=13

button=Pin(btn_pin, Pin.IN, Pin.PULL_UP) #PULL_UP為上拉電阻>>正電自pin14流出，按鈕按下形成通路流入GND，故電位由1變0
#PULL_DOWN為下拉電阻>>負電自pin14流入，按鈕按下形成通路流入VCC，故電位由0變1
rled=Pin(rled_pin, Pin.OUT)
yled=Pin(yled_pin, Pin.OUT)

while(True):
    if button.value()==0:
        rled.on()
        yled.off()
    else:
        rled.off()
        yled.on()
    