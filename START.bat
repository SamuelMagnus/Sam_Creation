@echo off
title SamCreation Inventory
echo.
echo  Starting SamCreation...
echo  Your browser will open automatically.
echo.

:: Try python first, then py launcher
where python >nul 2>&1
if %errorlevel% == 0 (
    python "%~dp0server.py"
    goto done
)

where py >nul 2>&1
if %errorlevel% == 0 (
    py "%~dp0server.py"
    goto done
)

echo  ERROR: Python not found on this computer.
echo.
echo  Please install Python from https://www.python.org/downloads/
echo  Make sure to tick "Add Python to PATH" during install.
echo.
pause

:done
