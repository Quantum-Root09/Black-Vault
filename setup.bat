@echo off
setlocal

echo.
echo   ╔════════════════════════════════════════╗
echo   ║     BlackVault ^— Setup Script          ║
echo   ║     by venkatsai                       ║
echo   ╚════════════════════════════════════════╝
echo.

:: ── Check Python ──────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo   [!] Python not found. Please install Python 3.8+ and add it to PATH.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo   [+] %PYVER% found

:: ── Create virtual environment ────────────────────────────
if exist venv\ (
    echo   [~] Existing venv found -- skipping creation.
) else (
    echo   [+] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo   [!] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: ── Activate ──────────────────────────────────────────────
echo   [+] Activating virtual environment...
call venv\Scripts\activate.bat

:: ── Install dependencies ──────────────────────────────────
echo   [+] Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo   [!] Dependency installation failed. Check requirements.txt and your internet connection.
    pause
    exit /b 1
)

echo.
echo   ╔════════════════════════════════════════╗
echo   ║  [OK]  Setup complete!                 ║
echo   ╚════════════════════════════════════════╝
echo.
echo   To launch BlackVault:
echo.
echo     venv\Scripts\activate
echo     python blackvault.py
echo.
pause
endlocal
