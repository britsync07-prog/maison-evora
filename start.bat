@echo off
title Maison Evora - QR & Social Hub
echo ===================================================
echo           MAISON EVORA - QR & SOCIAL HUB
echo ===================================================
echo.
echo Starting local web server...
echo.
python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(('8.8.8.8', 80)); print('>> Local Network URL: http://' + s.getsockname()[0] + ':8000'); s.close()"
echo >> PC Browser URL:    http://localhost:8000
echo.
echo Press Ctrl+C in this window anytime to stop the server.
echo.
start http://localhost:8000
python -m http.server 8000
pause
