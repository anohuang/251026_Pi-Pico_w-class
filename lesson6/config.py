"""
配置模組 - 定義 MQTT 和數據儲存相關常數
"""

# MQTT Broker 設定
BROKER_HOST = "localhost"  # MQTT Broker 地址
BROKER_PORT = 1883  # MQTT Broker 端口
MQTT_TOPIC = "客廳/感測器"  # 訂閱的主題名稱

# 可選：MQTT 認證設定（如果需要）
# MQTT_USERNAME = None
# MQTT_PASSWORD = None

# 數據儲存設定
DATA_DIR = "data"  # Excel 檔案儲存目錄
EXCEL_FILENAME_PREFIX = "sensor_data_"  # Excel 檔案名稱前綴
EXCEL_FILE_EXTENSION = ".xlsx"  # Excel 檔案副檔名

# Excel 檔案欄位定義
EXCEL_COLUMNS = [
    "timestamp",      # 時間戳記
    "light_status",   # 電燈狀態
    "temperature",    # 溫度
    "humidity"        # 濕度
]

# 數據更新設定
AUTO_REFRESH_INTERVAL = 2  # Streamlit 自動刷新間隔（秒）

