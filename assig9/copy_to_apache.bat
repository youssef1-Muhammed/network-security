@echo off
echo ========================================
echo Copy Files to Apache Document Root
echo ========================================
echo.

REM Try to find Apache document root
set DOCUMENT_ROOT=

REM Check common XAMPP location
if exist "C:\xampp\htdocs" (
    set DOCUMENT_ROOT=C:\xampp\htdocs
    goto :found
)

REM Check common WAMP location
if exist "C:\wamp64\www" (
    set DOCUMENT_ROOT=C:\wamp64\www
    goto :found
)

if exist "C:\wamp\www" (
    set DOCUMENT_ROOT=C:\wamp\www
    goto :found
)

REM Check Apache24 location
if exist "C:\Apache24\htdocs" (
    set DOCUMENT_ROOT=C:\Apache24\htdocs
    goto :found
)

:notfound
echo ERROR: Could not find Apache document root automatically.
echo.
echo Please manually specify the path to your Apache htdocs/www directory.
echo.
set /p DOCUMENT_ROOT="Enter Apache document root path: "
if "%DOCUMENT_ROOT%"=="" (
    echo No path provided. Exiting.
    pause
    exit /b 1
)

:found
echo Found Apache document root: %DOCUMENT_ROOT%
echo.
echo Current directory: %CD%
echo.
echo This will copy all PHP files to: %DOCUMENT_ROOT%
echo.
set /p CONFIRM="Continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Copying files...
echo.

REM Create a subdirectory in document root
set TARGET_DIR=%DOCUMENT_ROOT%\assignment
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

REM Copy PHP files
copy /Y *.php "%TARGET_DIR%\"
if exist "xss_payload.html" copy /Y xss_payload.html "%TARGET_DIR%\"

echo.
echo ========================================
echo Files copied successfully!
echo ========================================
echo.
echo Your files are now available at:
echo   http://localhost/assignment/vulnerable_page.php
echo   http://localhost/assignment/cookie_receiver.php
echo.
echo You can also access them directly if copied to root:
echo   http://localhost/vulnerable_page.php
echo   http://localhost/cookie_receiver.php
echo.
pause

