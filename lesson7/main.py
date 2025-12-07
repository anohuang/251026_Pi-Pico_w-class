import wifi_connect as wifi
import time
import json
import random
from umqtt.simple import MQTTClient

# MQTT 設定
MQTT_BROKER = "192.168.137.37"  # 公開測試用 Broker #broker裡要用伺服器的ip，pico要和伺服器同網域
MQTT_PORT = 1883
CLIENT_ID = "pico_w_publisher"
TOPIC = "客廳/感測器"
KEEPALIVE = 60  # 保持連線時間（秒）

# 嘗試連線 WiFi
wifi.connect()

# 顯示 IP
print("IP:", wifi.get_ip())

# 建立 MQTT 連線（加入 keepalive 設定）
client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=KEEPALIVE)

def mqtt_connect():
    """連接 MQTT Broker"""
    print("正在連接 MQTT Broker...")
    client.connect()
    print(f"已連接到 {MQTT_BROKER}")

# 初始連線
mqtt_connect()

# 在 while True 之前宣告計數器
counter = 0

# 每隔 10 秒發布一次訊息
while True:
    # 每次迴圈加 1
    counter += 1

    # 產生亂數資料
    temperature = round(random.uniform(20.0, 35.0), 1)  # 溫度 20~35°C
    humidity = round(random.uniform(40.0, 80.0), 1)     # 濕度 40~80%
    light_status = random.choice(["開", "關"])          # 燈光狀態
    
    # 建立 JSON 資料
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "light_status": light_status
    }
    message = json.dumps(data)
    
    print("-" * 30)
    
    # 嘗試發布，如果失敗則重新連線
    try:
        client.publish(TOPIC.encode('utf-8'), message.encode('utf-8'))
        print(f"已發布訊息: {counter}")
        print(f"  溫度: {temperature}°C")
        print(f"  濕度: {humidity}%")
        print(f"  燈光: {light_status}")
        print(f"主題: {TOPIC}")
    except OSError as e:
        print(f"發布失敗: {e}")
        print("嘗試重新連線...")
        mqtt_connect()
        # 重新連線後再發布一次
        client.publish(TOPIC, message)
        print("重新連線後發布成功!")
    
    print("等待 10 秒後再次發布...")
    time.sleep(10)
      #問題在於 umqtt.simple 的 publish() 方法需要 bytes 類型，而不是字串。使用中文時，需要先將字串編碼為 UTF-8 bytes。
      #問題原因在 umqtt.simple 中：publish() 方法的第一個參數（主題）和第二個參數（訊息）都必須是 bytes 類型如果直接傳入包含中文的字串，會出現編碼錯誤
      #將主題和訊息都轉換為 UTF-8 bytes

