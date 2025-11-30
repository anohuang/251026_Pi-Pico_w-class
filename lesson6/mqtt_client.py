"""
MQTT 客戶端模組 - 處理 MQTT 訂閱和訊息接收
"""

import paho.mqtt.client as mqtt
import threading
import queue
from config import BROKER_HOST, BROKER_PORT, MQTT_TOPIC
from data_handler import parse_mqtt_message, save_to_excel


class MQTTClient:
    """
    MQTT 訂閱客戶端類別
    使用單例模式確保只有一個 MQTT 連接
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MQTTClient, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.client = None
        self.data_queue = queue.Queue()  # 用於 Streamlit 和 MQTT 線程之間的通信
        self.latest_data = None  # 最新的感測器數據
        self.is_connected = False
        self._initialized = True
    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        """連接回調函數"""
        if reason_code.is_failure:
            print(f"❌ MQTT 連接失敗，錯誤代碼: {reason_code}")
            self.is_connected = False
        else:
            print(f"✅ 成功連接到 MQTT Broker: {BROKER_HOST}:{BROKER_PORT}")
            print(f"📡 正在訂閱主題: {MQTT_TOPIC}")
            client.subscribe(MQTT_TOPIC, qos=1)
            self.is_connected = True
    
    def on_subscribe(self, client, userdata, mid, reason_codes, properties):
        """訂閱回調函數"""
        print(f"✅ 成功訂閱主題，訊息 ID: {mid}")
    
    def on_message(self, client, userdata, message):
        """接收訊息回調函數"""
        try:
            # 解析訊息
            data = parse_mqtt_message(message.payload)
            
            if data:
                # 更新最新數據
                self.latest_data = data
                
                # 將數據放入佇列供 Streamlit 讀取
                self.data_queue.put(data)
                
                # 自動儲存到 Excel
                save_to_excel(data)
                
                print(f"📨 收到新數據: 溫度={data['temperature']}°C, 濕度={data['humidity']}%, 電燈={data['light_status']}")
        except Exception as e:
            print(f"處理 MQTT 訊息時發生錯誤: {e}")
    
    def start(self):
        """啟動 MQTT 客戶端"""
        if self.client is not None and self.client.is_connected():
            print("MQTT 客戶端已經在運行中")
            return
        
        try:
            # 建立 MQTT 客戶端（使用 API 版本 2）
            self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
            
            # 設定回調函數
            self.client.on_connect = self.on_connect
            self.client.on_subscribe = self.on_subscribe
            self.client.on_message = self.on_message
            
            # 連接到 Broker
            print(f"🔗 正在連接到 MQTT Broker: {BROKER_HOST}:{BROKER_PORT}...")
            self.client.connect(BROKER_HOST, BROKER_PORT, 60)
            
            # 在背景線程中啟動網路循環
            self.client.loop_start()
            
        except Exception as e:
            print(f"啟動 MQTT 客戶端時發生錯誤: {e}")
            self.is_connected = False
    
    def stop(self):
        """停止 MQTT 客戶端"""
        if self.client is not None:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                print("🔌 已斷開 MQTT 連接")
                self.is_connected = False
            except Exception as e:
                print(f"停止 MQTT 客戶端時發生錯誤: {e}")
    
    def get_latest_data(self):
        """取得最新的感測器數據"""
        return self.latest_data
    
    def get_queued_data(self):
        """從佇列中取得數據（非阻塞）"""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None
    
    def is_running(self):
        """檢查 MQTT 客戶端是否正在運行"""
        return self.client is not None and self.is_connected

