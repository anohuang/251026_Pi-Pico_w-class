"""
Streamlit MQTT 監控儀表板
即時顯示智慧家居感測器數據（電燈狀態、溫度、濕度）
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time
from mqtt_client import MQTTClient
from data_handler import load_today_data
from config import AUTO_REFRESH_INTERVAL


# 頁面配置
st.set_page_config(
    page_title="MQTT 監控儀表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_mqtt_client():
    """初始化 MQTT 客戶端（僅執行一次）"""
    if 'mqtt_client' not in st.session_state:
        st.session_state.mqtt_client = MQTTClient()
        st.session_state.mqtt_client.start()
        # 等待連接建立
        time.sleep(1)


def get_current_data():
    """取得當前感測器數據"""
    if 'mqtt_client' in st.session_state:
        # 檢查是否有新的數據從佇列中來
        new_data = st.session_state.mqtt_client.get_queued_data()
        if new_data:
            st.session_state.current_data = new_data
        
        # 如果沒有新數據，使用最新數據
        if 'current_data' not in st.session_state:
            st.session_state.current_data = st.session_state.mqtt_client.get_latest_data()
    
    return st.session_state.get('current_data', None)


def display_light_status(light_status):
    """顯示電燈狀態"""
    if light_status == "on":
        st.success("🟢 電燈：開啟")
    elif light_status == "off":
        st.info("⚪ 電燈：關閉")
    else:
        st.warning(f"⚠️ 電燈狀態：{light_status}")


def create_temperature_humidity_chart(df):
    """建立溫濕度趨勢圖表"""
    if df.empty or len(df) == 0:
        st.info("📊 尚無數據，等待 MQTT 訊息...")
        return None
    
    # 確保 timestamp 欄位存在
    if 'timestamp' not in df.columns:
        st.error("數據格式錯誤：缺少 timestamp 欄位")
        return None
    
    # 轉換 timestamp 為 datetime（如果需要的話）
    try:
        df['datetime'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    except:
        df['datetime'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # 建立圖表
    fig = go.Figure()
    
    # 添加溫度曲線（左 Y 軸，紅色）
    if 'temperature' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['temperature'],
            name='溫度 (°C)',
            line=dict(color='#FF6B6B', width=2),
            mode='lines+markers',
            yaxis='y'
        ))
    
    # 添加濕度曲線（右 Y 軸，藍色）
    if 'humidity' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['humidity'],
            name='濕度 (%)',
            line=dict(color='#4ECDC4', width=2),
            mode='lines+markers',
            yaxis='y2'
        ))
    
    # 設定雙 Y 軸
    fig.update_layout(
        title={
            'text': '溫濕度趨勢圖表',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='時間',
            showgrid=True
        ),
        yaxis=dict(
            title='溫度 (°C)',
            titlefont=dict(color='#FF6B6B'),
            tickfont=dict(color='#FF6B6B'),
            side='left',
            showgrid=True
        ),
        yaxis2=dict(
            title='濕度 (%)',
            titlefont=dict(color='#4ECDC4'),
            tickfont=dict(color='#4ECDC4'),
            side='right',
            overlaying='y',
            showgrid=False
        ),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig


# 主應用程式
def main():
    # 標題
    st.title("🏠 智慧家居 MQTT 監控儀表板")
    st.markdown("---")
    
    # 初始化 MQTT 客戶端
    init_mqtt_client()
    
    # 側邊欄 - 即時狀態顯示
    with st.sidebar:
        st.header("📊 即時狀態")
        
        # 取得當前數據
        current_data = get_current_data()
        
        if current_data:
            # 電燈狀態
            st.subheader("💡 電燈狀態")
            display_light_status(current_data.get('light_status', 'unknown'))
            
            st.markdown("---")
            
            # 溫度顯示
            st.subheader("🌡️ 當前溫度")
            temperature = current_data.get('temperature', 0.0)
            st.metric(
                label="溫度",
                value=f"{temperature:.1f}",
                delta=None,
                delta_color="normal"
            )
            st.markdown("單位：°C")
            
            st.markdown("---")
            
            # 濕度顯示
            st.subheader("💧 當前濕度")
            humidity = current_data.get('humidity', 0.0)
            st.metric(
                label="濕度",
                value=f"{humidity:.1f}",
                delta=None,
                delta_color="normal"
            )
            st.markdown("單位：%")
            
            st.markdown("---")
            
            # 最後更新時間
            timestamp = current_data.get('timestamp', 'N/A')
            st.caption(f"🕐 最後更新：{timestamp}")
        else:
            st.info("⏳ 等待 MQTT 數據...")
            st.caption("請確保 MQTT Broker 正在運行，並且有數據發送到主題 '客廳/感測器'")
        
        # MQTT 連接狀態
        st.markdown("---")
        if 'mqtt_client' in st.session_state:
            if st.session_state.mqtt_client.is_running():
                st.success("🟢 MQTT 已連接")
            else:
                st.error("🔴 MQTT 未連接")
    
    # 主區域 - 溫濕度趨勢圖表
    st.header("📈 溫濕度趨勢圖表")
    
    # 讀取當天的歷史數據
    df = load_today_data()
    
    if not df.empty:
        # 建立並顯示圖表
        fig = create_temperature_humidity_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # 顯示數據統計
        with st.expander("📋 數據統計資訊"):
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'temperature' in df.columns:
                    st.metric("平均溫度", f"{df['temperature'].mean():.1f} °C")
            with col2:
                if 'humidity' in df.columns:
                    st.metric("平均濕度", f"{df['humidity'].mean():.1f} %")
            with col3:
                st.metric("數據筆數", len(df))
    else:
        st.info("📊 尚無歷史數據，等待 MQTT 訊息...")
    
    # 底部 - 數據儲存狀態
    st.markdown("---")
    st.caption("💾 數據自動儲存：每當收到新的 MQTT 訊息時，數據會自動追加到當天的 Excel 檔案中")
    
    # 自動刷新
    time.sleep(AUTO_REFRESH_INTERVAL)
    st.rerun()


if __name__ == "__main__":
    main()
