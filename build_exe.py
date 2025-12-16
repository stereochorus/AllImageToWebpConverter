"""
Build script for ALLimageToWebpConverter.exe
Author: MadS
"""

import PyInstaller.__main__
import os
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# PyInstaller configuration
PyInstaller.__main__.run([
    str(current_dir / 'converter.py'),  # Main script
    '--onefile',  # Create single executable
    '--name=ALLimageToWebpConverter',  # Executable name
    '--icon=NONE',  # No icon (you can add later if needed)
    '--noconsole',  # Remove console window (change to --console if you want to see output)
    '--add-data=requirements.txt;.',  # Include requirements.txt
    '--version-file=version_info.txt',  # Version information
    '--clean',  # Clean cache before build

    # Metadata
    '--copyright=Copyright (c) 2025 MadS',
    '--win-private-assemblies',
    '--win-no-prefer-redirects',
])

print("\n" + "="*70)
print("Build Complete!")
print("="*70)
print(f"Executable location: {current_dir / 'dist' / 'ALLimageToWebpConverter.exe'}")
print("="*70)
