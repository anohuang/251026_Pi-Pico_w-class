#import time

#while True:
#    print("Hello! pico!")
#   time.sleep(3)

import wifi_connect as wifi #as 後面接的字可替代前述之function名稱，但下面記得要一併更換

# 嘗試連線 WiFi
wifi.connect()

# 顯示 IP
print("IP:", wifi.get_ip())

# 測試外部網路
if wifi.test_internet():
    print("外部網路 OK")
else:
    print("外部網路無法連線")
