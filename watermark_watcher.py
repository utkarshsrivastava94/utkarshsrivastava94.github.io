"""
watermark_watcher.py
--------------------
Watches assets/img/portfolio/ subfolders for new photos and automatically
applies the watermark (bottom center, semi-transparent) to each one.

Original photos are preserved in a sibling folder called `originals/`.
Watermarked versions replace the file in-place for the website.

Usage:
    python watermark_watcher.py

Requirements:
    pip install Pillow watchdog
"""

import time
import shutil
import logging
from pathlib import Path
from PIL import Image
import numpy as np
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ─────────────────────────────────────────────
# CONFIG — adjust these paths if needed
# ─────────────────────────────────────────────

# Root of your Jekyll repo (folder containing assets/)
REPO_ROOT = Path(__file__).parent

# Folders to watch (relative to repo root)
WATCH_FOLDERS = [
    REPO_ROOT / "assets" / "img" / "portfolio" / "landscape",
    REPO_ROOT / "assets" / "img" / "portfolio" / "wildlife",
    REPO_ROOT / "assets" / "img" / "portfolio" / "portraits",
]

# Your watermark image (place watermark.png next to this script)
WATERMARK_PATH = REPO_ROOT / "watermark.png"

# Watermark size as a fraction of the photo's width
WATERMARK_WIDTH_RATIO = 0.12

# Watermark opacity (0.0 = invisible, 1.0 = fully opaque)
WATERMARK_OPACITY = 0.55

# Bottom margin as a fraction of photo height
BOTTOM_MARGIN_RATIO = 0.03

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff"}

# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("watermark")

# Remove Pillow's decompression bomb limit (default is ~178MP)
# Safe to disable here since we control the input files
Image.MAX_IMAGE_PIXELS = None
 
# Disable Pillow's decompression bomb limit (default is ~179MP which is too
# small for high-resolution photography files). Set to None = no limit.
Image.MAX_IMAGE_PIXELS = None

def wait_for_file(path: Path, timeout: int = 30) -> bool:
    """
    Wait until a file is fully written and released by Windows.
    Polls file size stability then tries an exclusive open.
    Returns True if ready, False if timed out.
    """
    deadline = time.time() + timeout
    last_size = -1

    while time.time() < deadline:
        try:
            current_size = path.stat().st_size
            if current_size == 0:
                time.sleep(0.5)
                continue
            if current_size == last_size:
                # Size is stable — try exclusive open to confirm released
                with open(path, "rb+"):
                    return True
            last_size = current_size
            time.sleep(0.5)
        except (PermissionError, OSError):
            # File still locked by another process — keep waiting
            time.sleep(0.5)

    log.error(f"Timed out waiting for file to be released: {path.name}")
    return False


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
    """Load, clean, resize and apply opacity to the watermark."""
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
        # Skip cover images
        if photo_path.stem == "cover":
            log.info(f"Skipping cover image: {photo_path.name}")
            return

        # Wait for Windows to fully release the file before touching it
        log.info(f"Waiting for file to be ready: {photo_path.name}")
        if not wait_for_file(photo_path):
            log.error(f"Skipping {photo_path.name} — could not access file.")
            return

        # Save original
        originals_dir = photo_path.parent / "originals"
        originals_dir.mkdir(exist_ok=True)
        original_dest = originals_dir / photo_path.name

        if not original_dest.exists():
            shutil.copy2(photo_path, original_dest)
            log.info(f"Original saved → originals/{photo_path.name}")
        else:
            log.info(f"Original already backed up: {photo_path.name}")

        # Open photo
        photo = Image.open(photo_path).convert("RGBA")
        photo_w, photo_h = photo.size

        # Prepare watermark
        wm = prepare_watermark(photo_w)
        wm_w, wm_h = wm.size

        # Position: bottom center
        x = (photo_w - wm_w) // 2
        y = photo_h - wm_h - int(photo_h * BOTTOM_MARGIN_RATIO)

        # Composite
        canvas = Image.new("RGBA", photo.size, (0, 0, 0, 0))
        canvas.paste(photo, (0, 0))
        canvas.paste(wm, (x, y), wm)

        # Save (convert back to RGB for JPEGs)
        ext = photo_path.suffix.lower()
        if ext in {".jpg", ".jpeg"}:
            canvas.convert("RGB").save(photo_path, quality=95)
        else:
            canvas.save(photo_path)

        log.info(f"Watermarked: {photo_path.name}")

    except Exception as e:
        log.error(f"Failed to watermark {photo_path.name}: {e}")


def is_already_watermarked(photo_path: Path) -> bool:
    """Check if original already exists (meaning it was already processed)."""
    original = photo_path.parent / "originals" / photo_path.name
    return original.exists()


class PhotoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            return
        if path.parent.name == "originals":
            return  # ignore files created inside originals/

        log.info(f"New photo detected: {path.name}")
        apply_watermark(path)  # wait_for_file handles all timing internally

    def on_modified(self, event):
        # Ignore modifications — only process new files
        pass


def process_existing(folder: Path):
    """Watermark any existing photos in the folder that haven't been processed."""
    count = 0
    for f in sorted(folder.iterdir()):
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
            if f.stem == "cover":
                continue
            if is_already_watermarked(f):
                log.info(f"Already watermarked, skipping: {f.name}")
                continue
            apply_watermark(f)
            count += 1
    return count


def main():
    if not WATERMARK_PATH.exists():
        log.error(f"Watermark file not found at: {WATERMARK_PATH}")
        log.error("Place watermark.png in the same folder as this script.")
        return

    # Create watch folders if they don't exist
    for folder in WATCH_FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)

    log.info("=" * 55)
    log.info("Photography Watermark Watcher")
    log.info("=" * 55)
    log.info(f"Watermark: {WATERMARK_PATH.name}")
    log.info(f"Opacity:   {int(WATERMARK_OPACITY * 100)}%")
    log.info(f"Size:      {int(WATERMARK_WIDTH_RATIO * 100)}% of photo width")
    log.info(f"Position:  Bottom center")
    log.info("")

    # Process any existing unprocessed photos first
    total = 0
    for folder in WATCH_FOLDERS:
        log.info(f"Scanning: {folder.relative_to(REPO_ROOT)}")
        total += process_existing(folder)
    if total:
        log.info(f"Processed {total} existing photo(s).")
    else:
        log.info("No unprocessed existing photos found.")

    log.info("")
    log.info("Watching for new photos... (Press Ctrl+C to stop)")
    log.info("")

    # Start watching
    observer = Observer()
    handler = PhotoHandler()
    for folder in WATCH_FOLDERS:
        observer.schedule(handler, str(folder), recursive=False)
        log.info(f"Watching: {folder.relative_to(REPO_ROOT)}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Stopping watcher...")
        observer.stop()
    observer.join()
    log.info("Done.")


if __name__ == "__main__":
    main()