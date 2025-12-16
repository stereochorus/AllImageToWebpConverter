# Build Guide - ALLimageToWebpConverter.exe

Program image converter dengan kompresi optimal dan preservasi metadata lengkap.

**Author**: MadS
**Version**: 1.0.0
**Date**: December 2025

---

## Prerequisites

Sebelum build, pastikan Anda sudah install:

1. **Python 3.8+**
   - Download dari: https://www.python.org/downloads/

2. **Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **PyInstaller**
   ```bash
   pip install pyinstaller
   ```

---

## Cara Build ke .exe

### Method 1: Simple Build (RECOMMENDED - Paling Mudah)

**Windows:**
```bash
build_simple.bat
```

Script ini akan otomatis:
- ✅ Install semua dependencies (Pillow, piexif, PyInstaller)
- ✅ Collect semua library yang diperlukan
- ✅ Build executable dengan metadata lengkap
- ✅ Output: `dist\ALLimageToWebpConverter.exe`

### Method 2: Advanced Build

**Windows:**
```bash
build.bat
```

Script dengan validasi dan cleanup otomatis.

### Method 2: Manual PyInstaller

```bash
pyinstaller --clean --noconfirm ALLimageToWebpConverter.spec
```

### Method 3: PyInstaller Command Line

```bash
pyinstaller --onefile --name=ALLimageToWebpConverter --version-file=version_info.txt --console converter.py
```

---

## Output Location

Setelah build berhasil, executable akan tersimpan di:
```
dist\ALLimageToWebpConverter.exe
```

---

## File Structure Setelah Build

```
AllImageTowebpConverter/
├── build/                      # Build cache (bisa dihapus)
├── dist/
│   └── ALLimageToWebpConverter.exe  # ← Executable file
├── source/                     # Folder untuk source images
├── result/                     # Folder untuk hasil konversi
├── failedConvert/             # Folder untuk file yang gagal
├── converter.py               # Source code utama
├── requirements.txt           # Python dependencies
├── version_info.txt           # Version metadata
├── ALLimageToWebpConverter.spec  # PyInstaller config
├── build.bat                  # Build script
└── README.md                  # Dokumentasi
```

---

## Distribusi

Untuk distribusi, Anda hanya perlu file:
1. `ALLimageToWebpConverter.exe` (dari folder `dist/`)

User tidak perlu install Python atau dependencies!

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'PIL'"
**Penyebab:** PyInstaller tidak meng-include library Pillow

**Solusi:**
```bash
# Method 1: Use build_simple.bat (RECOMMENDED)
build_simple.bat

# Method 2: Rebuild dengan collect-all
pip install Pillow piexif
pyinstaller --onefile --collect-all=PIL --collect-all=piexif --hidden-import=PIL --hidden-import=piexif converter.py
```

### Error: "PyInstaller not found"
**Solusi:**
```bash
pip install pyinstaller
```

### Error: "Module not found"
**Solusi:**
```bash
pip install -r requirements.txt
# atau
pip install Pillow piexif
```

### Executable terlalu besar
**Solusi:**
Edit `ALLimageToWebpConverter.spec`, ubah `upx=False` untuk disable compression, atau install UPX:
```bash
# Download UPX dari: https://upx.github.io/
```

### Console window tidak muncul
Edit `ALLimageToWebpConverter.spec`, ubah:
```python
console=False  # Ganti jadi True untuk show console
```

---

## Program Metadata

```
Product Name    : ALL Image to WebP Converter
File Name       : ALLimageToWebpConverter.exe
Version         : 1.0.0.0
Author          : MadS
Copyright       : Copyright (c) 2025 MadS. All rights reserved.
Description     : Balanced compression with metadata preservation
```

---

## Features

✅ **Max Output**: 150 KB per file
✅ **Metadata**: GPS, EXIF, DateTime SELALU terjaga
✅ **Quality**: Dynamic adjustment (25-70)
✅ **Formats**: JPG, PNG, BMP, TIFF, GIF, ICO, WebP, dan lainnya
✅ **Bilingual**: English & Indonesian interface
✅ **Auto-monitoring**: Continuous folder monitoring

---

## Support

Untuk issues atau feedback, hubungi: **MadS**

---

**Built with ❤️ by MadS**
