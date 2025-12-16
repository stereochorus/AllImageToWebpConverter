# All Image to WebP Converter

Program untuk mengkonversi semua format gambar menjadi WebP dengan kualitas tinggi dan preservasi metadata lengkap.

## Fitur

- ✅ **Balanced Compression** - Hasil WebP maksimal 150 KB dengan kualitas optimal!
- ✅ **Metadata ALWAYS Preserved** - GPS, EXIF, DateTime SELALU dipertahankan!
- ✅ **Smart Multi-Pass Optimization** - Otomatis menyesuaikan quality dan ukuran gambar untuk mencapai target
- ✅ **Intelligent Resizing** - Untuk file >100 MB, otomatis resize dengan kualitas optimal
- ✅ **Continuous Monitoring Mode** - Program berjalan terus-menerus dan otomatis memproses gambar baru
- ✅ **Bilingual Interface** - Pesan dalam Bahasa Indonesia dan English
- ✅ **Real-time Size Tracking** - Menampilkan perbandingan ukuran file sebelum dan sesudah konversi
- ✅ Konversi semua format gambar (JPG, PNG, BMP, TIFF, GIF, ICO, dll) ke WebP
- ✅ Dynamic Quality Adjustment - Quality disesuaikan otomatis (25-70) berdasarkan ukuran source
- ✅ Output ke subfolder berdasarkan tanggal (mmddyyyy)
- ✅ Auto-delete source file setelah konversi sukses
- ✅ Auto-move ke folder failedConvert jika konversi gagal
- ✅ Nama file hasil sama dengan source (hanya extension yang berbeda)

## Instalasi

### Option 1: Download .exe Langsung (Termudah - Recommended)

**Tidak perlu install Python atau build apapun!**

📥 **[Download ALLimageToWebpConverter.exe](https://github.com/stereochorus/AllImageToWebpConverter/raw/main/dist/ALLimageToWebpConverter.exe)**

Atau kunjungi folder: [`/dist`](https://github.com/stereochorus/AllImageToWebpConverter/tree/main/dist)

**Cara Menggunakan:**
1. Klik link download di atas
2. Double-click `ALLimageToWebpConverter.exe`
3. Program langsung siap digunakan!
4. **Tidak perlu install Python, Pillow, atau dependency apapun**

### Option 2: Menjalankan dari Source Code (untuk Developer)

1. Install Python 3.8+
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Jalankan:
```bash
python converter.py
```

### Option 3: Build .exe Sendiri

Lihat [BUILD_GUIDE.md](BUILD_GUIDE.md) untuk instruksi lengkap build executable.

## Struktur Folder

```
AllImageTowebpConverter/
├── converter.py          # Program utama
├── source/              # Taruh gambar di sini
├── result/              # Hasil konversi (otomatis dibuat)
│   └── mmddyyyy/       # Subfolder berdasarkan tanggal
└── failedConvert/      # File yang gagal dikonversi
```

## Cara Penggunaan

1. Jalankan program:
```bash
python converter.py
```

2. Program akan menampilkan pesan selamat datang dalam 2 bahasa (English & Indonesian)

3. Letakkan gambar apapun ke folder `source/` - program akan otomatis mendeteksi dan mengkonversinya

4. Hasil konversi akan tersimpan di `result/mmddyyyy/`

5. File source akan otomatis terhapus setelah berhasil dikonversi

6. File yang gagal akan dipindah ke `failedConvert/`

7. Untuk menghentikan program:
   - Tekan `Q` pada keyboard, atau
   - Tekan `Ctrl+C`, atau
   - Klik `X` untuk menutup window

## Format Gambar yang Didukung

- JPG/JPEG
- PNG
- BMP
- TIFF/TIF
- GIF
- ICO
- WebP
- PPM/PGM/PBM/PNM
- DIB
- JFIF
- JPEG 2000 (JP2/JPX/J2K)

## Contoh Output

```
======================================================================
               IMAGE TO WEBP CONVERTER
======================================================================

🇬🇧 ENGLISH:
  The image converter to WebP is running. Every image saved in the
  'source' folder will be automatically converted and saved in the
  'result' folder. Failed conversions will be moved to the
  'failedConvert' folder.

  To stop, press 'Q' on the keyboard or click 'X' to close.

----------------------------------------------------------------------

🇮🇩 BAHASA INDONESIA:
  Program image converter to WebP sedang berjalan. Setiap gambar yang
  disimpan di folder 'source' akan otomatis di convert dan di save di
  folder 'result'. File gambar yang gagal di convert akan di save ke
  folder 'failedConvert'.

  Untuk berhenti, silahkan tekan 'Q' pada keyboard atau klik 'X'.

======================================================================

📁 Source folder      : F:\python project\AllImageTowebpConverter\source
📁 Result folder      : F:\python project\AllImageTowebpConverter\result
📁 Failed folder      : F:\python project\AllImageTowebpConverter\failedConvert
📅 Output subfolder   : 12162025
⚙️  Quality settings   : Quality=75, Alpha=80, Sharp YUV=Yes

======================================================================
🔄 Monitoring source folder... (Press 'Q' to quit)
======================================================================

Found 2 image(s) to convert.
============================================================

Converting: photo1.jpg (2543.5 KB / 2.5 MB)
    ⚙️  Resizing: 4000x3000 → 2400x1800 (60%)
    ✓ Metadata preserved (including GPS if available)
    ✓ Saved to: result\12162025\photo1.webp
    ✓ Size: 2543.5 KB → 142.8 KB (94.4% reduction)
    ✓ Dimensions: 4000x3000 → Scale: 60%
    ✓ Quality: 62, Attempts: 4, Target: ≤150 KB
    ✓ Metadata: PRESERVED (GPS, EXIF, DateTime)
    ✓ Source file deleted
------------------------------------------------------------

Converting: huge_image.png (153600 KB / 150.0 MB)
    ⚙️  Resizing: 8000x6000 → 4800x3600 (60%)
    ⚙️  Further resizing: → 4080x3060 (51%)
    ✓ Metadata preserved (including GPS if available)
    ✓ Saved to: result\12162025\huge_image.webp
    ✓ Size: 153600.0 KB → 148.2 KB (99.9% reduction)
    ✓ Dimensions: 8000x6000 → Scale: 51%
    ✓ Quality: 38, Attempts: 6, Target: ≤150 KB
    ✓ Metadata: PRESERVED (GPS, EXIF, DateTime)
    ✓ Source file deleted
------------------------------------------------------------

============================================================
Batch Complete! ✓ Converted: 2 | ✗ Failed: 0
============================================================

[Program continues monitoring... press Q to stop]

======================================================================
🛑 Stopping converter...
======================================================================
📊 Total Statistics:
   ✓ Successfully converted: 2
   ✗ Failed: 0
======================================================================
👋 Thank you! / Terima kasih!
======================================================================
```

## Metadata yang Dipreservasi

Program ini mempertahankan semua metadata EXIF dari gambar source, termasuk:
- GPS Latitude & Longitude
- DateTime (Original, Digitized, Modified)
- Camera Make & Model
- Orientation
- Dan semua metadata EXIF lainnya

## Teknik Kompresi Balanced dengan Metadata Preservation

Program ini menggunakan **multi-pass optimization** untuk memastikan hasil WebP **maksimal 150 KB** dengan **METADATA SELALU DIPERTAHANKAN**:

### Strategi Kompresi:

#### 1. **Dynamic Quality Adjustment**
Berdasarkan ukuran file source (kualitas lebih tinggi dari target 99KB):
- **>100 MB**: Quality dimulai dari 45 (lebih baik untuk file besar)
- **50-100 MB**: Quality dimulai dari 55
- **10-50 MB**: Quality dimulai dari 65
- **<10 MB**: Quality dimulai dari 70 (kualitas tinggi)

#### 2. **Intelligent Resizing**
- File besar otomatis di-resize hingga 60% dari ukuran asli (lebih besar dari 50%)
- Jika masih terlalu besar, resize lebih lanjut secara bertahap (85% per iterasi)
- Menggunakan LANCZOS resampling untuk kualitas optimal

#### 3. **Iterative Compression**
- Maksimal 10 iterasi untuk mencapai target ≤150 KB
- Setiap iterasi mengurangi quality 5-10 poin (lebih gradual)
- Jika quality minimum (25) tercapai, lakukan resize tambahan

#### 4. **Metadata Management - ALWAYS PRESERVED!**
- ✅ Metadata (EXIF, GPS, DateTime) **SELALU** dipertahankan di semua iterasi
- ✅ Tidak ada kondisi dimana metadata dihapus
- ✅ Ruang 150 KB cukup untuk metadata lengkap (10-20 KB) + image data berkualitas (130-140 KB)

### Parameter Teknis:
- **Method: 6** - Kompresi terbaik (0-6, 6 adalah terbaik)
- **exact=False** - Transformasi color space untuk kompresi lebih baik
- **minimize_size=True** - Extra pass untuk meminimalkan ukuran file
- **kmin=3, kmax=5** - Key frame optimization
- **Quality Range: 25-70** - Disesuaikan dinamis (lebih tinggi dari 15-60)
- **Max Output: 150 KB** - Target maksimal dengan metadata
- **Metadata: ALWAYS INCLUDED** - GPS, EXIF, DateTime selalu ada

### Hasil yang Diharapkan:

| Source Size | Compression Strategy | Expected Output | Quality Range |
|-------------|---------------------|-----------------|---------------|
| < 10 MB     | Quality 70, minimal resize | ~120-150 KB | Sangat Baik |
| 10-50 MB    | Quality 65, 60% resize | ~130-150 KB | Baik |
| 50-100 MB   | Quality 55, 60% resize | ~135-150 KB | Baik |
| > 100 MB    | Quality 45, aggressive resize | ~140-150 KB | Cukup Baik |

### Perbandingan Ukuran File:
```
Contoh hasil konversi (SEMUA ≤150 KB dengan METADATA LENGKAP):
- photo.jpg (2.5 MB)     → photo.webp (143 KB)   = 94.3% reduction ✅ + Metadata
- huge.png (150 MB)      → huge.webp (148 KB)    = 99.9% reduction ✅ + Metadata
- screenshot.png (5 MB)  → screenshot.webp (138 KB) = 97.2% reduction ✅ + Metadata
- graphic.bmp (50 MB)    → graphic.webp (145 KB) = 99.7% reduction ✅ + Metadata
```

### Keuntungan Target 150 KB:

✅ **Metadata Lengkap Terjaga**: GPS, EXIF, DateTime selalu dipertahankan
✅ **Kualitas Visual Lebih Baik**: Quality 25-70 vs 15-60 (sebelumnya)
✅ **Resize Lebih Ringan**: 60% vs 50% (dimensi lebih besar)
✅ **Masih Sangat Kecil**: File 100 MB → 150 KB = kompresi 99.85%
✅ **Perfect for Web/Mobile**: 150 KB loading sangat cepat

### Catatan Penting:
✅ **Best Balance**: Target 150 KB adalah sweet spot antara ukuran minimal dan kualitas optimal dengan metadata lengkap. Untuk file sangat besar (>100 MB), gambar akan di-resize namun kualitas visual tetap baik dan **semua metadata tetap dipertahankan**.

## Troubleshooting

Jika ada error saat instalasi piexif atau Pillow, coba:
```bash
pip install --upgrade pip
pip install Pillow piexif
```
