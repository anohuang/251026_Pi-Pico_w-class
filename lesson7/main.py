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
#print("IP:", wifi.get_ip())

# 測試外部網路
#if wifi.test_internet():
#    print("外部網路 OK")
#else:
#    print("外部網路無法連線")

import wifi_connect as wifi
import time
from umqtt.simple import MQTTClient

# MQTT 設定
MQTT_BROKER = "172.20.10.3"  # 公開測試用 Broker
MQTT_PORT = 1883
CLIENT_ID = "pico_w_publisher"
TOPIC = "pico/test"

# 嘗試連線 WiFi
wifi.connect()

# 顯示 IP
print("IP:", wifi.get_ip())

# 建立 MQTT 連線
print("正在連接 MQTT Broker...")
client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.connect()
print(f"已連接到 {MQTT_BROKER}")

#檢查程式碼，找出中文訊息導致錯誤的原因。
#問題在於 umqtt.simple 的 publish() 方法需要 bytes 類型，而不是字串。使用中文時，需要先將字串編碼為 UTF-8 bytes。
#問題原因
#在 umqtt.simple 中：publish() 方法的第一個參數（主題）和第二個參數（訊息）都必須是 bytes 類型如果直接傳入包含中文的字串，會出現編碼錯誤
#解決方法: 需要將主題和訊息都轉換為 bytes。以下是修正後的程式碼：

# 每隔 10 秒發布一次訊息
counter = 0
while True:
    counter += 1
    message = f"來自 Pico W 的訊息！ #{counter}"  # 中文訊息
    
    print("-" * 30)
    # 將主題和訊息都轉換為 bytes
    client.publish(TOPIC.encode('utf-8'), message.encode('utf-8'))
    print(f"已發布訊息: {message}")
    print(f"主題: {TOPIC}")
    
    print("等待 10 秒後再次發布...")
    time.sleep(10)