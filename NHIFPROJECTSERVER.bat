@echo off
setlocal

:: Prompt for the password
set /p "userpass=Say my name: "

:: Check if the password is correct
if "%userpass%"=="daddy" (
    echo Password correct! Running the Django server...
    
    REM Change directory to the project folder
    cd C:\Users\hp\Desktop\nhif_project

    REM Start the Django server using your local IP address on port 8000
    start cmd /k "python manage.py runserver 192.168.0.116:8000"

    echo Waiting for the server to start...
    timeout /t 10 /nobreak

    REM Open the browser with the correct path
    start "" "C:\Program Files (x86)\Mozilla Firefox\firefox.exe" "http://192.168.0.116:8000"
) else (
    echo Incorrect password! Exiting...
    timeout /t 3 /nobreak
)

endlocal
