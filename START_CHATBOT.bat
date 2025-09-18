@echo off
echo 🚗 FetiiPro Chatbot Sharing Setup
echo ====================================
echo.
echo 📍 Your IP Address: 192.168.1.103
echo 🌐 Port: 8082
echo.
echo 📧 Share this URL with your interviewer:
echo    http://192.168.1.103:8082
echo.
echo 📋 Instructions for your interviewer:
echo    1. Open their web browser
echo    2. Go to: http://192.168.1.103:8082
echo    3. Start asking questions about FetiiPro data!
echo.
echo 🔒 Firewall Note:
echo    If your interviewer can't access the chatbot:
echo    1. Allow Python through Windows Firewall
echo    2. Or temporarily disable Windows Firewall
echo    3. Or add a firewall rule for port 8082
echo.
echo 🚀 Starting your chatbot server...
echo    Press Ctrl+C to stop when done
echo.
pause
python src/langchain_web_app.py
