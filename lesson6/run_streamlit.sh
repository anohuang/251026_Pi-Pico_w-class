#!/bin/bash
# Streamlit 應用程式執行腳本

cd "$(dirname "$0")"
uv run streamlit run app.py

