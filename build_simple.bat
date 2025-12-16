@echo off
REM Simple build script with all dependencies explicitly included
REM Author: MadS

echo ======================================================================
echo Simple Build Script - ALLimageToWebpConverter.exe
echo ======================================================================
echo.

REM Install all required packages
echo Step 1: Installing required packages...
pip install --upgrade pip
pip install Pillow piexif pyinstaller
echo.

REM Clean old build
echo Step 2: Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build with explicit options
echo Step 3: Building executable...
pyinstaller ^
    --onefile ^
    --name=ALLimageToWebpConverter ^
    --add-data="requirements.txt;." ^
    --hidden-import=PIL ^
    --hidden-import=PIL._imaging ^
    --hidden-import=PIL.Image ^
    --hidden-import=piexif ^
    --collect-all=PIL ^
    --collect-all=piexif ^
    --console ^
    converter.py

echo.
echo ======================================================================
if exist dist\ALLimageToWebpConverter.exe (
    echo BUILD SUCCESS!
    echo Location: dist\ALLimageToWebpConverter.exe
) else (
    echo BUILD FAILED! Check errors above.
)
echo ======================================================================
pause
