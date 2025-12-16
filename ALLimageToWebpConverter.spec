# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec file for ALLimageToWebpConverter
# Author: MadS
# Version: 1.0.0
#

block_cipher = None

a = Analysis(
    ['converter.py'],
    pathex=[],
    binaries=[],
    datas=[('requirements.txt', '.')],
    hiddenimports=[
        'PIL',
        'PIL._imaging',
        'PIL.Image',
        'PIL.ImageFile',
        'PIL.ImageFilter',
        'PIL.ImageDraw',
        'piexif',
        'piexif._dump',
        'piexif._load',
        'piexif._common',
        'piexif._exif',
        'piexif._gps',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ALLimageToWebpConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon=None,  # Add icon file path here if you have one
)
