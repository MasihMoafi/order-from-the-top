"""Render a supply-room .excalidraw file to SVG (and PNG with rsvg-convert).

A plain preview for checking runs; open the .excalidraw file itself in
Excalidraw for the real view. Usage: python3 game/render.py <file.excalidraw>
"""

import html
import json
import subprocess
import sys
from pathlib import Path


def svg(doc):
    els = [e for e in doc["elements"] if not e.get("isDeleted")]
    xs = [e["x"] + e["width"] for e in els] + [0]
    ys = [e["y"] + e["height"] for e in els] + [0]
    w, h = max(xs) + 40, max(ys) + 40
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="-20 -30 {w} {h}">',
        f'<rect x="-20" y="-30" width="{w}" height="{h}" fill="white"/>',
    ]
    for e in els:
        x, y, ew, eh = e["x"], e["y"], e["width"], e["height"]
        fill = e["backgroundColor"] if e["backgroundColor"] != "transparent" else "none"
        st = f'stroke="{e["strokeColor"]}" stroke-width="2" fill="{fill}" fill-opacity="0.6"'
        t = e["type"]
        if t == "frame":
            out.append(
                f'<rect x="{x}" y="{y}" width="{ew}" height="{eh}" fill="none" stroke="#adb5bd"/>'
            )
            out.append(
                f'<text x="{x}" y="{y - 6}" font-size="13" font-family="sans-serif">{html.escape(e["name"])}</text>'
            )
        elif t == "rectangle":
            out.append(f'<rect x="{x}" y="{y}" width="{ew}" height="{eh}" {st}/>')
        elif t == "ellipse":
            out.append(
                f'<ellipse cx="{x + ew / 2}" cy="{y + eh / 2}" rx="{ew / 2}" ry="{eh / 2}" {st}/>'
            )
        elif t == "diamond":
            pts = f"{x + ew / 2},{y} {x + ew},{y + eh / 2} {x + ew / 2},{y + eh} {x},{y + eh / 2}"
            out.append(f'<polygon points="{pts}" {st}/>')
        elif t == "line":
            (x0, y0), (x1, y1) = e["points"][0], e["points"][-1]
            out.append(
                f'<line x1="{x + x0}" y1="{y + y0}" x2="{x + x1}" y2="{y + y1}" stroke="{e["strokeColor"]}" stroke-width="3"/>'
            )
        elif t == "text":
            for i, line in enumerate(e["text"].split("\n")):
                out.append(
                    f'<text x="{x}" y="{y + 14 + i * e["fontSize"] * 1.25}" font-size="{e["fontSize"]}" '
                    f'font-family="monospace">{html.escape(line)}</text>'
                )
    out.append("</svg>")
    return "\n".join(out)


def main():
    src = Path(sys.argv[1])
    dst = src.with_suffix(".svg")
    dst.write_text(svg(json.loads(src.read_text())))
    subprocess.run(
        ["rsvg-convert", "-o", str(dst.with_suffix(".png")), str(dst)], check=True
    )
    print(dst.with_suffix(".png"))


if __name__ == "__main__":
    main()
