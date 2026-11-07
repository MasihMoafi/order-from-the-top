"""Extract Matilda's face and three Love Spot character portraits from the Elpis source into this folder."""

import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
E = Path.home() / "Desktop/p/Elpis/apps/elpis-desktop"
face = (E / "bridge/matilda-face.cjs").read_text()
m = re.search(r"tiltSmile: avatar\('data:image/webp;base64,([A-Za-z0-9+/=]+)'", face)
(HERE / "matilda.webp").write_bytes(base64.b64decode(m.group(1)))
chars = (E / "lib/love-characters.ts").read_text()
block = chars[
    chars.index("export const portraits") : chars.index("export const boardPortraits")
]
for name in ("researcher", "critic", "builder"):
    mm = re.search(
        name + r"""\s*:\s*["'`](data:image/[^;]+);base64,([A-Za-z0-9+/=]+)""", block
    )
    print(name, mm.group(1) if mm else "NOT FOUND")
    if mm:
        ext = "svg" if "svg" in mm.group(1) else "png"
        (HERE / f"{name}.{ext}").write_bytes(base64.b64decode(mm.group(2)))
