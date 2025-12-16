@echo off
echo ======================================================================
echo Building ALLimageToWebpConverter.exe
echo Author: MadS
echo ======================================================================
echo.

REM Check and install dependencies
echo Checking dependencies...
python -c "import PIL" 2>NUL
if errorlevel 1 (
    echo Pillow not found. Installing...
    pip install Pillow
)

python -c "import piexif" 2>NUL
if errorlevel 1 (
    echo piexif not found. Installing...
    pip install piexif
)

python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo All dependencies installed!
echo.

REM Clean previous build
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
echo Building executable...
pyinstaller --clean --noconfirm ALLimageToWebpConverter.spec

echo.
echo ======================================================================
echo Build Complete!
echo ======================================================================
if exist dist\ALLimageToWebpConverter.exe (
    echo SUCCESS! Executable created at: dist\ALLimageToWebpConverter.exe
    echo.
    echo File size:
    dir dist\ALLimageToWebpConverter.exe | find "ALLimageToWebpConverter.exe"
) else (
    echo ERROR! Build failed. Check error messages above.
)
echo ======================================================================
echo.
pause
