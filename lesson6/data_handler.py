"""
數據處理模組 - 處理 MQTT 訊息解析、Excel 儲存和讀取
"""

import json
import os
from datetime import datetime
import pandas as pd
from config import (
    DATA_DIR,
    EXCEL_FILENAME_PREFIX,
    EXCEL_FILE_EXTENSION,
    EXCEL_COLUMNS
)


def parse_mqtt_message(payload):
    """
    解析 MQTT 訊息（JSON 格式）
    
    Args:
        payload: MQTT 訊息的 payload（bytes 或 str）
    
    Returns:
        dict: 解析後的數據字典，包含 timestamp, light_status, temperature, humidity
    """
    try:
        # 如果是 bytes，轉換為字串
        if isinstance(payload, bytes):
            payload = payload.decode('utf-8')
        
        # 解析 JSON
        data = json.loads(payload)
        
        # 提取數據並標準化格式
        result = {
            "timestamp": data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "light_status": data.get("light_status", "unknown"),
            "temperature": float(data.get("temperature", 0.0)),
            "humidity": float(data.get("humidity", 0.0))
        }
        
        return result
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"解析 MQTT 訊息時發生錯誤: {e}")
        return None


def get_today_excel_filename():
    """
    取得當天的 Excel 檔案名稱
    
    Returns:
        str: 完整的檔案路徑
    """
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{EXCEL_FILENAME_PREFIX}{today}{EXCEL_FILE_EXTENSION}"
    filepath = os.path.join(DATA_DIR, filename)
    return filepath


def save_to_excel(data_dict):
    """
    將數據追加到當天的 Excel 檔案
    
    Args:
        data_dict: 包含感測器數據的字典
    
    Returns:
        bool: 儲存是否成功
    """
    try:
        # 確保數據目錄存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # 取得當天的 Excel 檔案路徑
        filepath = get_today_excel_filename()
        
        # 建立 DataFrame
        df_new = pd.DataFrame([data_dict])
        
        # 如果檔案存在，讀取現有數據並追加
        if os.path.exists(filepath):
            df_existing = pd.read_excel(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            # 如果檔案不存在，建立新檔案
            df_combined = df_new
        
        # 儲存到 Excel
        df_combined.to_excel(filepath, index=False, engine='openpyxl')
        
        return True
    except Exception as e:
        print(f"儲存 Excel 檔案時發生錯誤: {e}")
        return False


def load_today_data():
    """
    讀取當天的所有數據
    
    Returns:
        pd.DataFrame: 包含當天所有數據的 DataFrame，如果檔案不存在則返回空的 DataFrame
    """
    try:
        filepath = get_today_excel_filename()
        
        if os.path.exists(filepath):
            df = pd.read_excel(filepath, engine='openpyxl')
            # 確保 timestamp 欄位是字串格式
            if 'timestamp' in df.columns:
                df['timestamp'] = df['timestamp'].astype(str)
            return df
        else:
            # 如果檔案不存在，返回空的 DataFrame
            return pd.DataFrame(columns=EXCEL_COLUMNS)
    except Exception as e:
        print(f"讀取 Excel 檔案時發生錯誤: {e}")
        return pd.DataFrame(columns=EXCEL_COLUMNS)

