# MQTT 使用說明 - umqtt.simple

本說明文件介紹如何在 Raspberry Pi Pico W 上使用 `umqtt.simple` 套件進行 MQTT 通訊。

---

## 📦 已安裝套件

- ✅ `umqtt.simple` - MicroPython MQTT 客戶端庫

---

## 📁 檔案說明

| 檔案名稱 | 說明 |
|---------|------|
| `mqtt_client.py` | MQTT 客戶端封裝模組（類似 `wifi_connect.py`） |
| `mqtt_example_simple.py` | 最簡單的 MQTT 使用範例（直接使用 umqtt.simple） |
| `mqtt_example_publish.py` | 發布訊息範例 |
| `mqtt_example_subscribe.py` | 訂閱訊息範例 |
| `main.py` | 整合 WiFi 和 MQTT 的完整範例 |

---

## 🚀 快速開始

### 步驟 1：設定 MQTT Broker

首先，你需要有一個正在運行的 MQTT Broker。常見的選擇：

1. **本地 Raspberry Pi**（如果有的話）
   - 安裝 mosquitto：`sudo apt install mosquitto mosquitto-clients`
   - 啟動服務：`sudo systemctl start mosquitto`
   - 預設 IP：你的 Raspberry Pi IP（例如：`192.168.1.100`）

2. **公共 MQTT Broker**（測試用）
   - `test.mosquitto.org`（不建議用於生產環境）
   - `broker.hivemq.com`

3. **雲端 MQTT 服務**
   - Adafruit IO
   - AWS IoT Core
   - Google Cloud IoT

### 步驟 2：修改設定

開啟任何一個範例檔案，修改以下設定：

```python
MQTT_BROKER = "192.168.1.100"  # 改為你的 MQTT Broker IP
MQTT_TOPIC = "pico/sensor"     # 主題名稱（可自訂）
```

### 步驟 3：上傳並執行

將檔案上傳到 Pico W，然後執行：

```python
# 在 Thonny 中執行
exec(open('mqtt_example_simple.py').read())
```

---

## 📖 使用方式

### 方式一：使用封裝模組（推薦）

使用 `mqtt_client.py` 模組，類似於 `wifi_connect.py` 的使用方式：

```python
import wifi_connect as wifi
import mqtt_client as mqtt
import time

# 1. 連線 WiFi
wifi.connect()

# 2. 連線 MQTT
client = mqtt.connect(broker="192.168.1.100", client_id="pico_001")

# 3. 發布訊息
data = {"temperature": 25.5, "humidity": 60}
mqtt.publish(client, "sensor/data", data)

# 4. 斷線
mqtt.disconnect(client)
```

### 方式二：直接使用 umqtt.simple

直接使用 `umqtt.simple`，更靈活但需要自己處理細節：

```python
from umqtt.simple import MQTTClient
import time

# 1. 建立客戶端
client = MQTTClient("pico_001", "192.168.1.100", 1883)

# 2. 連線
client.connect()

# 3. 發布訊息
client.publish(b"sensor/data", b"Hello MQTT!")

# 4. 斷線
client.disconnect()
```

---

## 🔧 mqtt_client.py 模組功能

### `connect(broker, port, client_id, keepalive)`

連線到 MQTT Broker。

**參數：**
- `broker`: MQTT Broker 的 IP 或主機名稱
- `port`: 連接埠（預設：1883）
- `client_id`: 客戶端 ID（每個設備應該不同）
- `keepalive`: 保持連線時間（秒，預設：60）

**範例：**
```python
client = mqtt.connect(broker="192.168.1.100", client_id="pico_001")
```

---

### `publish(client, topic, message, qos, retain)`

發布訊息到指定的主題。

**參數：**
- `client`: MQTTClient 物件
- `topic`: 主題名稱（字串）
- `message`: 訊息內容（字串、bytes 或字典）
- `qos`: 服務品質等級（0, 1, 或 2，預設：0）
- `retain`: 是否保留訊息（預設：False）

**範例：**
```python
# 發布字串
mqtt.publish(client, "test/topic", "Hello!")

# 發布字典（會自動轉換為 JSON）
data = {"temp": 25.5, "humi": 60}
mqtt.publish(client, "sensor/data", data)
```

---

### `subscribe(client, topic, qos)`

訂閱指定的主題。

**參數：**
- `client`: MQTTClient 物件
- `topic`: 主題名稱
- `qos`: 服務品質等級（預設：0）

**範例：**
```python
mqtt.subscribe(client, "sensor/data")
```

---

### `set_callback(client, callback_func)`

設定接收訊息時的回調函式。

**參數：**
- `client`: MQTTClient 物件
- `callback_func`: 回調函式，格式為 `callback(topic, message)`

**範例：**
```python
def on_message(topic, message):
    print(f"收到：{topic.decode()} = {message.decode()}")

mqtt.set_callback(client, on_message)
```

---

### `check_msg(client, timeout)`

檢查是否有新訊息（非阻塞）。

**參數：**
- `client`: MQTTClient 物件
- `timeout`: 超時時間（秒，預設：1）

**範例：**
```python
while True:
    mqtt.check_msg(client)  # 檢查訊息
    time.sleep(0.1)
```

---

### `disconnect(client)`

斷開 MQTT 連線。

**範例：**
```python
mqtt.disconnect(client)
```

---

## 📝 完整範例

### 範例 1：發布感測器數據

```python
import wifi_connect as wifi
import mqtt_client as mqtt
import time

wifi.connect()
client = mqtt.connect(broker="192.168.1.100", client_id="pico_sensor")

while True:
    data = {
        "temperature": 25.5,
        "humidity": 60.0,
        "timestamp": time.time()
    }
    mqtt.publish(client, "sensor/data", data)
    time.sleep(5)
```

---

### 範例 2：訂閱並接收訊息

```python
import wifi_connect as wifi
import mqtt_client as mqtt
import time

def on_message(topic, message):
    print(f"收到：{topic.decode()} = {message.decode()}")

wifi.connect()
client = mqtt.connect(broker="192.168.1.100", client_id="pico_subscriber")
mqtt.set_callback(client, on_message)
mqtt.subscribe(client, "sensor/data")

while True:
    mqtt.check_msg(client)
    time.sleep(0.1)
```

---

## ❓ 常見問題

### Q1：無法連線 MQTT Broker？

**檢查項目：**
1. ✅ MQTT Broker 是否正在運行？
   ```bash
   # 在 Raspberry Pi 上檢查
   sudo systemctl status mosquitto
   ```

2. ✅ IP 位址是否正確？
   - 確認 Broker 的 IP 位址
   - 使用 `ping` 測試連線

3. ✅ 防火牆是否允許連接埠 1883？
   ```bash
   sudo ufw allow 1883
   ```

4. ✅ Pico 和 Broker 是否在同一個網路？

---

### Q2：如何測試 MQTT 連線？

**在 Raspberry Pi 上使用 mosquitto 客戶端：**

```bash
# 訂閱主題（接收訊息）
mosquitto_sub -h localhost -t "pico/sensor" -v

# 發布訊息（發送訊息）
mosquitto_pub -h localhost -t "pico/sensor" -m "Hello from Pi!"
```

---

### Q3：訊息格式應該用什麼？

**建議使用 JSON 格式：**

```python
import ujson

data = {
    "device": "Pico W",
    "temperature": 25.5,
    "humidity": 60.0
}
message = ujson.dumps(data)
mqtt.publish(client, "sensor/data", message)
```

---

### Q4：QoS 是什麼？應該用哪個等級？

**QoS（Quality of Service）服務品質等級：**

- **QoS 0**：最多傳送一次（最快，但可能遺失訊息）
- **QoS 1**：至少傳送一次（保證送達，但可能重複）
- **QoS 2**：只傳送一次（最可靠，但最慢）

**建議：**
- 感測器數據：QoS 0（遺失一兩筆沒關係）
- 重要指令：QoS 1（必須送達）

---

### Q5：如何同時發布和訂閱？

```python
import wifi_connect as wifi
import mqtt_client as mqtt
import time

def on_message(topic, message):
    print(f"收到：{message.decode()}")

wifi.connect()
client = mqtt.connect(broker="192.168.1.100", client_id="pico_dual")

# 訂閱
mqtt.set_callback(client, on_message)
mqtt.subscribe(client, "commands")

# 發布
count = 0
while True:
    # 發布數據
    mqtt.publish(client, "sensor/data", {"count": count})
    count += 1
    
    # 檢查是否有收到的訊息
    mqtt.check_msg(client)
    
    time.sleep(1)
```

---

## 📚 參考資源

- [umqtt.simple 官方文件](https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple)
- [MQTT 協議說明](https://mqtt.org/)
- [Mosquitto MQTT Broker](https://mosquitto.org/)

---

## 🎯 下一步

1. ✅ 修改範例中的 IP 和主題名稱
2. ✅ 測試發布訊息
3. ✅ 測試訂閱訊息
4. ✅ 整合到你的專案中

祝你使用愉快！🚀

