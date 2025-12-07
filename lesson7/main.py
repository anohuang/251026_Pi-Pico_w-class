#import time

#while True:
#    print("Hello! pico!")
#   time.sleep(3)

import wifi_connect as wifi #as 後面接的字可替代前述之function名稱，但下面記得要一併更換

# 嘗試連線 WiFi
wifi.connect() #括弧內沒寫的話表示全用預設值
#connect(ssid=WIFI_SSID, password=WIFI_PASSWORD, retry=20) 上面括弧內有三個引述名稱及預設參數值
#ssid、password和retry為引述名稱
#括弧內如果有打引述名稱的話，位置可任意調動; 若只打參數值則必須按照function內的引述名稱位置填寫
#混合引述: 若前面有打一個引述名稱的話，後面的也都必須加引述名稱，才不會出錯

# 顯示 IP
print("IP:", wifi.get_ip())

# 測試外部網路
if wifi.test_internet():
    print("外部網路 OK")
else:
    print("外部網路無法連線")
