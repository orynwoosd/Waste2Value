"""For processing images during upload"""
import uuid
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps

PROFILE_PICS_DIR = Path("media/profile_imgs")
LANDMARK_PICS_DIR = Path("media/landmark_imgs")

CHOSEN_PATH = {
    "pf": {"dir": PROFILE_PICS_DIR, "dimension": (300, 300)},
    "lm": {"dir": LANDMARK_PICS_DIR, "dimension": (800, 600)}
}
# Image processing
def process_image(content: bytes, type: str) -> str:
    choice = CHOSEN_PATH[type]
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, choice["dimension"], method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = choice["dir"] / filename

        choice["dir"].mkdir(parents=True, exist_ok=True)

        img.save(filepath, "JPEG", quality=85, optimize=True)
        print(filename)
    return filename


# Delete file

def delete_img(filename: str | None, type: str) -> None:
    choice = CHOSEN_PATH['type']
    if filename is None:
        return 
    filepath = choice["dir"] / filename
    if filepath.exists():
        filepath.unlink()