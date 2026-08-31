@echo off
chcp 65001 >nul
cd /d "D:\htmltool2"
start /min "" python -m http.server 8765
