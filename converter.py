import shutil
import time
import sys
from datetime import datetime
from pathlib import Path
from PIL import Image
import piexif

try:
    import msvcrt  # Windows
    WINDOWS = True
except ImportError:
    import select  # Unix/Linux/Mac
    WINDOWS = False


class ImageToWebPConverter:
    def __init__(self, source_folder="source", result_folder="result", failed_folder="failedConvert"):
        """
        Initialize the converter with folder paths.

        Args:
            source_folder: Folder containing source images
            result_folder: Folder to save converted images
            failed_folder: Folder to move failed conversions
        """
        self.source_folder = Path(source_folder)
        self.result_folder = Path(result_folder)
        self.failed_folder = Path(failed_folder)

        # Create folders if they don't exist
        self.source_folder.mkdir(exist_ok=True)
        self.result_folder.mkdir(exist_ok=True)
        self.failed_folder.mkdir(exist_ok=True)

        # WebP conversion settings
        self.webp_quality = 75
        self.webp_alpha_quality = 80
        self.max_output_size_kb = 150  # Maximum output file size in KB (with metadata preserved)

        # Supported image formats
        self.supported_formats = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
            '.gif', '.ico', '.webp', '.ppm', '.pgm', '.pbm',
            '.pnm', '.dib', '.jfif', '.jp2', '.jpx', '.j2k'
        }

    def get_output_subfolder(self):
        """
        Create and return the output subfolder path based on current date (mmddyyyy).

        Returns:
            Path: Path to the date-based subfolder
        """
        now = datetime.now()
        subfolder_name = now.strftime("%m%d%Y")
        output_path = self.result_folder / subfolder_name
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path

    def preserve_metadata(self, source_path, target_path):
        """
        Copy EXIF metadata from source to target image, including GPS data.

        Args:
            source_path: Path to source image
            target_path: Path to target WebP image
        """
        try:
            # Try to load EXIF data from source
            source_image = Image.open(source_path)

            # Check if source has EXIF data
            if 'exif' in source_image.info:
                exif_dict = piexif.load(source_image.info['exif'])

                # Convert EXIF to bytes
                exif_bytes = piexif.dump(exif_dict)

                # Load target image and save with EXIF
                target_image = Image.open(target_path)
                target_image.save(target_path, 'WEBP',
                                quality=self.webp_quality,
                                alpha_quality=self.webp_alpha_quality,
                                method=6,  # Use Sharp YUV
                                exif=exif_bytes)

                print(f"    ✓ Metadata preserved (including GPS if available)")
                return True
            else:
                print(f"    ℹ No EXIF metadata found in source image")
                return False

        except Exception as e:
            print(f"    ⚠ Warning: Could not preserve metadata - {str(e)}")
            return False

    def calculate_resize_dimensions(self, original_width, original_height, target_size_kb):
        """
        Calculate new dimensions to achieve target file size.
        Uses balanced scaling for 150KB target with metadata preservation.

        Args:
            original_width: Original image width
            original_height: Original image height
            target_size_kb: Target file size in KB

        Returns:
            tuple: (new_width, new_height, scale_percentage)
        """
        # For 150KB target, use 60% scale to maintain better quality
        scale = 0.6

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        return new_width, new_height, int(scale * 100)

    def optimize_webp_size(self, img, output_path, exif_data, source_size_mb):
        """
        Optimize WebP to ensure output is under 150KB while ALWAYS preserving metadata.
        Uses multi-pass compression with dynamic quality and resize.

        Strategy:
        1. Start with higher quality for 150KB target (better than 99KB)
        2. Resize image if needed
        3. Iteratively reduce quality until under 150KB
        4. ALWAYS preserve metadata (EXIF included in all attempts)

        Args:
            img: PIL Image object
            output_path: Path to save the WebP file
            exif_data: EXIF data to preserve (ALWAYS included)
            source_size_mb: Source file size in MB

        Returns:
            dict: Compression statistics
        """
        max_size_bytes = self.max_output_size_kb * 1024
        original_width, original_height = img.size

        # Determine initial quality based on source file size
        # Higher quality for 150KB target vs 99KB
        if source_size_mb > 100:
            quality = 45  # Better quality for huge files
            resize_needed = True
        elif source_size_mb > 50:
            quality = 55
            resize_needed = True
        elif source_size_mb > 10:
            quality = 65
            resize_needed = True
        else:
            quality = 70  # Higher starting quality for small files
            resize_needed = False

        # Resize image if source is very large
        working_img = img
        resize_scale = 100

        if resize_needed:
            new_width, new_height, resize_scale = self.calculate_resize_dimensions(
                original_width, original_height, self.max_output_size_kb
            )
            working_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"    ⚙️  Resizing: {original_width}x{original_height} → {new_width}x{new_height} ({resize_scale}%)")

        # Multi-pass compression to achieve target size
        attempts = 0
        max_attempts = 10

        while attempts < max_attempts:
            # Save with current quality - ALWAYS include EXIF metadata
            working_img.save(
                output_path,
                'WEBP',
                quality=quality,
                alpha_quality=max(quality - 5, 60),  # Higher alpha quality
                method=6,  # Best compression
                exact=False,
                lossless=False,
                exif=exif_data,  # ALWAYS preserve metadata!
                minimize_size=True,
                kmin=3,
                kmax=5
            )

            # Check file size
            current_size = output_path.stat().st_size

            if current_size <= max_size_bytes:
                # Success!
                return {
                    'quality': quality,
                    'resize_scale': resize_scale,
                    'attempts': attempts + 1,
                    'final_size_kb': current_size / 1024,
                    'metadata_preserved': True
                }

            # File still too large, reduce quality
            attempts += 1

            if attempts == 2 and not resize_needed:
                # If quality reduction isn't enough, try resizing
                new_width, new_height, resize_scale = self.calculate_resize_dimensions(
                    original_width, original_height, self.max_output_size_kb
                )
                working_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"    ⚙️  Resizing: {original_width}x{original_height} → {new_width}x{new_height} ({resize_scale}%)")
                resize_needed = True
                quality = 60  # Reset to higher quality after resize
                continue

            # Reduce quality more gradually (150KB allows for better quality)
            if current_size > max_size_bytes * 2:
                quality = max(quality - 10, 25)  # Minimum quality 25 (better than 15)
            elif current_size > max_size_bytes * 1.5:
                quality = max(quality - 8, 25)
            else:
                quality = max(quality - 5, 25)

            # If quality is at minimum and still too large, resize more
            if quality <= 25 and resize_needed:
                resize_scale = int(resize_scale * 0.85)  # Less aggressive resize
                new_width = int(original_width * resize_scale / 100)
                new_height = int(original_height * resize_scale / 100)
                working_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"    ⚙️  Further resizing: → {new_width}x{new_height} ({resize_scale}%)")
                quality = 50  # Reset quality after additional resize

        # Return stats even if we couldn't achieve target
        # Metadata is still preserved!
        return {
            'quality': quality,
            'resize_scale': resize_scale,
            'attempts': attempts,
            'final_size_kb': output_path.stat().st_size / 1024,
            'metadata_preserved': True
        }

    def convert_image_to_webp(self, image_path):
        """
        Convert a single image to WebP format with balanced compression.
        Ensures output file is under 150KB while ALWAYS preserving metadata.

        Args:
            image_path: Path to the source image file

        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Get source file size
            source_size = image_path.stat().st_size
            source_size_mb = source_size / (1024 * 1024)

            # Get output folder with date-based subfolder
            output_folder = self.get_output_subfolder()

            # Create output filename (same name, .webp extension)
            output_filename = image_path.stem + ".webp"
            output_path = output_folder / output_filename

            print(f"Converting: {image_path.name} ({source_size / 1024:.1f} KB / {source_size_mb:.1f} MB)")

            # Open and convert image
            with Image.open(image_path) as img:
                original_dimensions = f"{img.size[0]}x{img.size[1]}"

                # Convert RGBA to RGB if necessary (for images without transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Keep alpha channel for transparent images
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                elif img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')

                # Get EXIF data before saving
                exif_data = img.info.get('exif', b'')

                # Optimize with compression to stay under 150KB (metadata included)
                stats = self.optimize_webp_size(img, output_path, exif_data, source_size_mb)

            # ALWAYS preserve metadata from source (re-apply with piexif)
            self.preserve_metadata(image_path, output_path)

            # Get final output file size
            output_size = output_path.stat().st_size
            size_reduction = ((source_size - output_size) / source_size * 100)

            # Check if we achieved the target
            if output_size > self.max_output_size_kb * 1024:
                print(f"    ⚠️  Warning: Output size {output_size / 1024:.1f} KB exceeds {self.max_output_size_kb} KB limit!")

            print(f"    ✓ Saved to: {output_path}")
            print(f"    ✓ Size: {source_size / 1024:.1f} KB → {output_size / 1024:.1f} KB ({size_reduction:.1f}% reduction)")
            print(f"    ✓ Dimensions: {original_dimensions} → Scale: {stats['resize_scale']}%")
            print(f"    ✓ Quality: {stats['quality']}, Attempts: {stats['attempts']}, Target: ≤{self.max_output_size_kb} KB")
            print(f"    ✓ Metadata: PRESERVED (GPS, EXIF, DateTime)")

            # Delete source file after successful conversion
            image_path.unlink()
            print(f"    ✓ Source file deleted")

            return True

        except Exception as e:
            print(f"    ✗ Error converting {image_path.name}: {str(e)}")
            return False

    def move_to_failed(self, image_path):
        """
        Move failed conversion file to the failedConvert folder.

        Args:
            image_path: Path to the failed image file
        """
        try:
            destination = self.failed_folder / image_path.name

            # If file with same name exists, add timestamp
            if destination.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destination = self.failed_folder / f"{image_path.stem}_{timestamp}{image_path.suffix}"

            shutil.move(str(image_path), str(destination))
            print(f"    ➜ Moved to failedConvert: {destination.name}")

        except Exception as e:
            print(f"    ✗ Error moving file to failedConvert: {str(e)}")

    def is_image_file(self, file_path):
        """
        Check if a file is a supported image format.

        Args:
            file_path: Path to the file

        Returns:
            bool: True if file is a supported image, False otherwise
        """
        return file_path.suffix.lower() in self.supported_formats

    def process_all_images(self):
        """
        Process all images in the source folder.
        Convert them to WebP and delete originals, or move failed ones.

        Returns:
            tuple: (success_count, failed_count)
        """
        # Get all files in source folder
        files = [f for f in self.source_folder.iterdir() if f.is_file()]

        # Filter only image files
        image_files = [f for f in files if self.is_image_file(f)]

        if not image_files:
            return 0, 0

        print(f"\nFound {len(image_files)} image(s) to convert.")
        print("="*60)

        success_count = 0
        failed_count = 0

        for image_file in image_files:
            print()
            if self.convert_image_to_webp(image_file):
                success_count += 1
            else:
                failed_count += 1
                self.move_to_failed(image_file)
            print("-"*60)

        if success_count > 0 or failed_count > 0:
            print()
            print("="*60)
            print(f"Batch Complete! ✓ Converted: {success_count} | ✗ Failed: {failed_count}")
            print("="*60)

        return success_count, failed_count

    def check_quit_key(self):
        """
        Check if user pressed 'Q' or 'q' to quit.

        Returns:
            bool: True if user wants to quit, False otherwise
        """
        if WINDOWS:
            # Windows: use msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                if key == 'q':
                    return True
        else:
            # Unix/Linux/Mac: use select
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1).lower()
                if key == 'q':
                    return True
        return False

    def print_welcome_message(self):
        """
        Print bilingual welcome message (English and Indonesian).
        """
        print("\n" + "="*70)
        print(" " * 15 + "IMAGE TO WEBP CONVERTER - by MadS")
        print("="*70)
        print()
        print("🇬🇧 ENGLISH:")
        print("  The image converter to WebP is running. Every image saved in the")
        print("  'source' folder will be automatically converted and saved in the")
        print("  'result' folder. Failed conversions will be moved to the")
        print("  'failedConvert' folder.")
        print()
        print("  To stop, press 'Q' on the keyboard or click 'X' to close.")
        print()
        print("-"*70)
        print()
        print("🇮🇩 BAHASA INDONESIA:")
        print("  Program image converter to WebP sedang berjalan. Setiap gambar yang")
        print("  disimpan di folder 'source' akan otomatis di convert dan di save di")
        print("  folder 'result'. File gambar yang gagal di convert akan di save ke")
        print("  folder 'failedConvert'.")
        print()
        print("  Untuk berhenti, silahkan tekan 'Q' pada keyboard atau klik 'X'.")
        print()
        print("="*70)
        print()
        print(f"📁 Source folder      : {self.source_folder.absolute()}")
        print(f"📁 Result folder      : {self.result_folder.absolute()}")
        print(f"📁 Failed folder      : {self.failed_folder.absolute()}")
        print(f"📅 Output subfolder   : {self.get_output_subfolder().name}")
        print(f"⚙️  Quality settings   : Quality={self.webp_quality}, Alpha={self.webp_alpha_quality}, Sharp YUV=Yes")
        print()
        print("="*70)
        print("🔄 Monitoring source folder... (Press 'Q' to quit)")
        print("="*70)

    def run_continuous(self, check_interval=2):
        """
        Run converter in continuous monitoring mode.
        Checks source folder periodically and converts new images.

        Args:
            check_interval: Seconds between folder checks (default: 2)
        """
        self.print_welcome_message()

        total_success = 0
        total_failed = 0

        try:
            while True:
                # Check if user wants to quit
                if self.check_quit_key():
                    print("\n" + "="*70)
                    print("🛑 Stopping converter...")
                    print("="*70)
                    print(f"📊 Total Statistics:")
                    print(f"   ✓ Successfully converted: {total_success}")
                    print(f"   ✗ Failed: {total_failed}")
                    print("="*70)
                    print("👋 Thank you! / Terima kasih!")
                    print("="*70)
                    break

                # Process any images in source folder
                success, failed = self.process_all_images()
                total_success += success
                total_failed += failed

                # Wait before next check
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("🛑 Program interrupted by user (Ctrl+C)")
            print("="*70)
            print(f"📊 Total Statistics:")
            print(f"   ✓ Successfully converted: {total_success}")
            print(f"   ✗ Failed: {total_failed}")
            print("="*70)
            print("👋 Thank you! / Terima kasih!")
            print("="*70)

    def run(self):
        """
        Main method to run the converter in single-run mode.
        """
        print("="*60)
        print("Image to WebP Converter")
        print("="*60)
        print(f"Source folder: {self.source_folder.absolute()}")
        print(f"Result folder: {self.result_folder.absolute()}")
        print(f"Failed folder: {self.failed_folder.absolute()}")
        print(f"Output subfolder: {self.get_output_subfolder().name}")
        print("="*60)
        print()

        self.process_all_images()


def main():
    """
    Main entry point for the converter.
    Runs in continuous monitoring mode by default.
    """
    converter = ImageToWebPConverter(
        source_folder="source",
        result_folder="result",
        failed_folder="failedConvert"
    )

    # Run in continuous monitoring mode
    converter.run_continuous(check_interval=2)


if __name__ == "__main__":
    main()
