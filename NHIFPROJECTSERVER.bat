@echo off
setlocal EnableDelayedExpansion

:: Prompt for the password
set /p "userpass=Say my name: "

:: Check if the password is correct
if "%userpass%"=="daddy" (
    echo Password correct! Detecting local IP...

    :: Get the local IPv4 address
    for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr "IPv4 Address"') do (
        set "ip=%%A"
    )
    for /f "tokens=* delims= " %%B in ("!ip!") do set "ip=%%B"

    echo Using IP: !ip!

    :: Change directory to the project folder
    cd /d "C:\Users\hp\nhif_project"

    :: Start the Django server using the detected IP address
    start cmd /k "python manage.py runserver !ip!:8000"

    echo Waiting for the server to start...
    timeout /t 10 /nobreak

    :: Open the browser with the correct address
    start "" "http://!ip!:8000"
) else (
    echo Incorrect password! Exiting...
    timeout /t 3 /nobreak
)

endlocal
