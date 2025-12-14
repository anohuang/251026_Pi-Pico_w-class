from machine import Pin
from time import sleep

btn_pin=14
rled_pin=15
yled_pin=13

button=Pin(btn_pin, Pin.IN, Pin.PULL_UP)
rled=Pin(rled_pin, Pin.OUT)
yled=Pin(yled_pin, Pin.OUT)

# 初始狀態：紅燈亮，黃燈滅
led_state = True  # True: 紅燈亮, False: 黃燈亮
rled.on()
yled.off()

# 防彈跳延遲時間（毫秒）
DEBOUNCE_DELAY = 50

# 記錄按鈕前一個狀態
last_button_state = button.value()

while(True):
    current_button_state = button.value()
    
    # 檢測按鈕從未按下（1）到按下（0）的邊緣
    if last_button_state == 1 and current_button_state == 0:
        # 按鈕剛被按下，等待防彈跳延遲
        sleep(DEBOUNCE_DELAY / 1000)
        
        # 再次檢查按鈕狀態，確認確實被按下
        if button.value() == 0:
            # 等待按鈕放開
            while button.value() == 0:
                sleep(0.01)  # 短暫延遲，避免過度占用 CPU
            
            # 按鈕已放開，再次等待防彈跳延遲
            sleep(DEBOUNCE_DELAY / 1000)
            
            # 確認按鈕確實已放開
            if button.value() == 1:
                # 切換 LED 狀態
                led_state = not led_state
                if led_state:
                    rled.on()
                    yled.off()
                else:
                    rled.off()
                    yled.on()
    
    # 更新按鈕前一個狀態
    last_button_state = current_button_state
    sleep(0.01)  # 短暫延遲，避免過度占用 CPU
    
