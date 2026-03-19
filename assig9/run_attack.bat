@echo off
echo Starting Slowloris Attack...
echo.
echo Usage examples:
echo   run_attack.bat http://localhost
echo   run_attack.bat http://localhost:8080
echo   run_attack.bat http://localhost --sockets 300
echo.

if "%1"=="" (
    echo Error: Please provide a target URL
    echo Example: run_attack.bat http://localhost
    pause
    exit /b 1
)

REM Try different Python commands
where python >nul 2>&1
if %errorlevel%==0 (
    python slowloris_attack.py %*
    goto :end
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    python3 slowloris_attack.py %*
    goto :end
)

where py >nul 2>&1
if %errorlevel%==0 (
    py slowloris_attack.py %*
    goto :end
)

echo Error: Python not found!
echo Please install Python or add it to your PATH
echo.
echo You can also run directly with:
echo   python slowloris_attack.py %*
pause
exit /b 1

:end
pause

