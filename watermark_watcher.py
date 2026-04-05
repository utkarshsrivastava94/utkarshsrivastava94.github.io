"""
watermark_processor.py
----------------------
Scans assets/img/photography/ subfolders once, applies watermarks,
saves originals, and exits. No active watching.

Usage:
    python watermark_processor.py
"""

import time
import shutil
import logging
from pathlib import Path
from PIL import Image
import numpy as np

# ─────────────────────────────────────────────
# CONFIG — Updated to your 'photography' path
# ─────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent

# Folders to scan (relative to repo root)
SCAN_FOLDERS = [
    REPO_ROOT / "assets" / "img" / "photography" / "landscape",
    REPO_ROOT / "assets" / "img" / "photography" / "wildlife",
    REPO_ROOT / "assets" / "img" / "photography" / "portraits",
]

WATERMARK_PATH = REPO_ROOT / "watermark.png"
WATERMARK_WIDTH_RATIO = 0.12
WATERMARK_OPACITY = 0.55
BOTTOM_MARGIN_RATIO = 0.03
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}

# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("watermark")
Image.MAX_IMAGE_PIXELS = None

def remove_white_background(wm_img: Image.Image) -> Image.Image:
    """Convert white/cream background of watermark to transparent."""
    wm = wm_img.convert("RGBA")
    data = np.array(wm)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3
    max_rgb = np.maximum(np.maximum(r.astype(int), g.astype(int)), b.astype(int))
    min_rgb = np.minimum(np.minimum(r.astype(int), g.astype(int)), b.astype(int))
    saturation = max_rgb - min_rgb
    is_background = (brightness > 200) & (saturation < 40)
    semi_bg = (brightness > 170) & (saturation < 60) & ~is_background
    data[:,:,3] = np.where(is_background, 0, a)
    data[:,:,3] = np.where(semi_bg, (data[:,:,3] * 0.4).astype(np.uint8), data[:,:,3])
    return Image.fromarray(data)

def prepare_watermark(photo_width: int) -> Image.Image:
    wm = Image.open(WATERMARK_PATH)
    wm = remove_white_background(wm)
    target_w = int(photo_width * WATERMARK_WIDTH_RATIO)
    ratio = target_w / wm.width
    target_h = int(wm.height * ratio)
    wm = wm.resize((target_w, target_h), Image.LANCZOS)
    data = np.array(wm)
    data[:,:,3] = (data[:,:,3] * WATERMARK_OPACITY).astype(np.uint8)
    return Image.fromarray(data)

def apply_watermark(photo_path: Path):
    """Apply watermark to a single photo, saving original first."""
    try:
        if photo_path.stem == "cover":
            return False

        originals_dir = photo_path.parent / "originals"
        originals_dir.mkdir(exist_ok=True)
        original_dest = originals_dir / photo_path.name

        # Save original if it doesn't exist
        if not original_dest.exists():
            shutil.copy2(photo_path, original_dest)
        
        # Open and process
        photo = Image.open(photo_path).convert("RGBA")
        photo_w, photo_h = photo.size
        wm = prepare_watermark(photo_w)
        wm_w, wm_h = wm.size

        x = (photo_w - wm_w) // 2
        y = photo_h - wm_h - int(photo_h * BOTTOM_MARGIN_RATIO)

        canvas = Image.new("RGBA", photo.size, (0, 0, 0, 0))
        canvas.paste(photo, (0, 0))
        canvas.paste(wm, (x, y), wm)

        ext = photo_path.suffix.lower()
        if ext in {".jpg", ".jpeg"}:
            # Lowered quality slightly to 85% to help with your Git file size issues
            canvas.convert("RGB").save(photo_path, quality=85, optimize=True)
        else:
            canvas.save(photo_path)
        
        log.info(f"Successfully processed: {photo_path.name}")
        return True
    except Exception as e:
        log.error(f"Failed to watermark {photo_path.name}: {e}")
        return False

def is_already_processed(photo_path: Path) -> bool:
    """Check if the photo is already in the originals folder."""
    original = photo_path.parent / "originals" / photo_path.name
    return original.exists()

def main():
    if not WATERMARK_PATH.exists():
        log.error(f"Watermark not found at: {WATERMARK_PATH}")
        return

    log.info("=" * 55)
    log.info("Starting Photography Watermark Scan")
    log.info("=" * 55)

    total_watermarked = 0

    for folder in SCAN_FOLDERS:
        if not folder.exists():
            log.warning(f"Skipping missing folder: {folder}")
            continue

        log.info(f"Scanning folder: {folder.name}...")
        
        for file_path in folder.iterdir():
            # Skip directories (like 'originals') and non-images
            if file_path.is_dir() or file_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            
            # Skip covers
            if file_path.stem == "cover":
                continue

            # Check if processed
            if is_already_processed(file_path):
                continue

            # Process
            if apply_watermark(file_path):
                total_watermarked += 1

    log.info("=" * 55)
    log.info(f"Scan Complete. Total images watermarked: {total_watermarked}")
    log.info("=" * 55)

if __name__ == "__main__":
    main()