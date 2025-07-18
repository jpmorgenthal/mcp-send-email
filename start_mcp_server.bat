@echo off
cd /d C:\Users\jpmor\mcp-send-email
call mcp\Scripts\activate.bat
python email_mcp.py
pause