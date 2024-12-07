@echo off
setlocal enabledelayedexpansion

REM Get the directory of this batch file
set "ScriptDir=%~dp0"

REM Set the base directory for data and logs
set "BASE_DIR=%ScriptDir%.."

REM Check if the first argument is 'start' or 'stop'
if "%1"=="start" (

    set directory[0]="cassandra2"
    set directory[1]="langflow\postgres"
    set directory[3]="langflow\config"

    REM Create all data directories if it doesn't exist
    for /L %%i in (0,1,%count%) do (
        mkdir /p %BASE_DIR%\data\!element[%%i]!
    )

    echo Starting Docker containers...
    docker-compose up -d
) else if "%1"=="stop" (
    echo Stopping Docker containers...
    docker-compose down
) else (
    echo Usage: %0 start|stop
)

endlocal
REM End of script