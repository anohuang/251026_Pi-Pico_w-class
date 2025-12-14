from machine import ADC, Pin, PWM
from time import sleep

# 初始化 ADC（使用 GPIO 27）
potentiometer = ADC(Pin(27))
rled = PWM(Pin(15))
yled = PWM(Pin(13))
rled.freq(1000)  # 設定 PWM 頻率為 1000Hz
yled.freq(500)  # 設定 PWM 頻率為 500Hz

while True:
    # 讀取 ADC 值（0 ~ 65535）
    raw_value = potentiometer.read_u16()
    
    # 轉換為電壓值（0 ~ 3.3V）
    voltage = raw_value * 3.3 / 65535
    
    # 轉換為百分比（0% ~ 100%）
    percentage = raw_value * 100 / 65535
    
    print(f"原始值: {raw_value}, 電壓: {voltage:.2f}V, 百分比: {percentage:.1f}%")
    
     # 直接將 ADC 值作為 PWM 的 duty cycle
    rled.duty_u16(raw_value)
    yled.duty_u16(raw_value)
    
    sleep(0.5)


