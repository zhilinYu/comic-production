#!/usr/bin/env python3
"""
Comic Assembly Script (混知风格科普漫画)
Assembles individually generated panel images into a long-form vertical comic.

Usage:
  python3 assemble.py --title "标题" --subtitle "副标题" --panels panels.json --output comic.png [--output-jpg]

panels.json format:
[
  {
    "image": "/path/to/panel.png",
    "title": "面板标题",
    "description": "描述文字"
  },
  ...
]
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


def find_font(bold=False):
    """Find a CJK font on macOS."""
    candidates = [
        '/System/Library/Fonts/STHeiti Medium.ttc' if bold else '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/Supplemental/Songti.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
    ]
    for fp in candidates:
        if os.path.exists(fp):
            return fp
    return None


def assemble(
    panels_data,
    title="科普漫画",
    subtitle="",
    width=1080,
    padding=40,
    text_band_h=95,
    title_h=180,
    gap=10,
    bottom_h=80,
    top_bar_h=6,
    output_path="comic.png",
    output_jpg=False,
):
    # Colors
    BG = (245, 245, 245)
    TEXT_BG = (35, 40, 55)
    TITLE_COLOR = (230, 60, 60)
    SUBTITLE_COLOR = (120, 120, 120)
    PANEL_BORDER = (200, 200, 200)
    ACCENT = (250, 200, 30)
    WHITE = (255, 255, 255)
    NUM_BG = (250, 200, 30)
    NUM_TEXT = (35, 40, 55)
    DESC_COLOR = (200, 200, 200)

    # Fonts
    font_bold = find_font(bold=True)
    font_light = find_font(bold=False)
    if not font_bold or not font_light:
        print("Warning: CJK font not found, text may not render correctly.")

    def mkfont(size, bold=False):
        fp = font_bold if bold else font_light
        return ImageFont.truetype(fp, size) if fp else ImageFont.load_default()

    title_font = mkfont(52, bold=True)
    subtitle_font = mkfont(22)
    num_font = mkfont(28, bold=True)
    panel_title_font = mkfont(26, bold=True)
    desc_font = mkfont(19)
    attr_font = mkfont(18)

    # Load and scale panels
    scaled_panels = []
    for p in panels_data:
        img = Image.open(p["image"]).convert("RGB")
        pw, ph = img.size

        # Remove AI watermark (bottom-right corner, ~15% height strip)
        wm_h = int(ph * 0.06)  # watermark height estimate
        wm_w = int(pw * 0.25)  # watermark width estimate
        # Sample background color from just above watermark area
        sample_y = ph - wm_h - 5
        sample_x = pw - 10
        if sample_y > 0 and sample_x > 0:
            bg_sample = img.getpixel((sample_x, sample_y))
            # Paint over watermark area with sampled background color
            draw_img = ImageDraw.Draw(img)
            draw_img.rectangle([pw - wm_w, ph - wm_h, pw, ph], fill=bg_sample)

        scale = (width - padding * 2) / pw
        new_w = int(pw * scale)
        new_h = int(ph * scale)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        scaled_panels.append((resized, new_w, new_h))

    # Calculate total height
    total_h = title_h + top_bar_h
    line_h = 28
    for (_, _, sh), pdata in zip(scaled_panels, panels_data):
        text_lines = pdata.get("lines", [])
        if not text_lines and pdata.get("description"):
            text_lines = [pdata["description"]]
        actual_band_h = max(text_band_h, 56 + len(text_lines) * line_h + 10)
        total_h += sh + gap + actual_band_h + gap
    total_h += bottom_h

    # Create canvas
    canvas = Image.new("RGB", (width, total_h), BG)
    draw = ImageDraw.Draw(canvas)

    # Top accent bar
    draw.rectangle([0, 0, width, top_bar_h], fill=ACCENT)

    # Title
    y = top_bar_h + 20
    tbbox = draw.textbbox((0, 0), title, font=title_font)
    tw = tbbox[2] - tbbox[0]
    draw.text(((width - tw) // 2, y), title, fill=TITLE_COLOR, font=title_font)

    # Subtitle
    y += 65
    if subtitle:
        sbbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sw = sbbox[2] - sbbox[0]
        draw.text(((width - sw) // 2, y), subtitle, fill=SUBTITLE_COLOR, font=subtitle_font)

    # Decorative line
    y += 40
    draw.line([(padding + 50, y), (width - padding - 50, y)], fill=PANEL_BORDER, width=1)
    y += 15

    # Draw each panel + text band
    num_panels = len(scaled_panels)
    for i, ((panel_img, pw, ph), pdata) in enumerate(zip(scaled_panels, panels_data)):
        # Panel image
        px = (width - pw) // 2
        draw.rectangle([px - 3, y - 3, px + pw + 3, y + ph + 3], fill=PANEL_BORDER)
        canvas.paste(panel_img, (px, y))
        y += ph + gap

        # Text band
        # Support both "description" (single string) and "lines" (array of strings)
        text_lines = pdata.get("lines", [])
        if not text_lines and pdata.get("description"):
            text_lines = [pdata["description"]]

        # Dynamic text band height based on line count
        line_h = 28  # height per line
        actual_band_h = max(text_band_h, 56 + len(text_lines) * line_h + 10)

        draw.rectangle([padding, y, width - padding, y + actual_band_h], fill=TEXT_BG)

        # Number badge
        bx = padding + 18
        by = y + 14
        bw, bh = 44, 34
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=6, fill=NUM_BG)
        num_str = str(i + 1)
        nbbox = draw.textbbox((0, 0), num_str, font=num_font)
        nw = nbbox[2] - nbbox[0]
        nh = nbbox[3] - nbbox[1]
        draw.text((bx + (bw - nw) // 2, by + (bh - nh) // 2 - 2), num_str, fill=NUM_TEXT, font=num_font)

        # Panel title
        tx = bx + bw + 15
        draw.text((tx, by + 3), pdata.get("title", ""), fill=ACCENT, font=panel_title_font)

        # Story lines (multi-line support)
        for li, line_text in enumerate(text_lines):
            ly = y + 56 + li * line_h
            # Last line (punchline) in slightly brighter color
            line_color = (220, 220, 220) if li == len(text_lines) - 1 else DESC_COLOR
            draw.text((padding + 22, ly), line_text, fill=line_color, font=desc_font)

        y += actual_band_h + gap

    # Bottom attribution (removed per user preference)
    # draw.line([(padding + 50, y + 10), (width - padding - 50, y + 10)], fill=PANEL_BORDER, width=1)
    # attr = "混知风格 · AI科普漫画 · by QoderWork"
    # abbox = draw.textbbox((0, 0), attr, font=attr_font)
    # aw = abbox[2] - abbox[0]
    # draw.text(((width - aw) // 2, y + 25), attr, fill=SUBTITLE_COLOR, font=attr_font)

    # Save PNG
    canvas.save(output_path, quality=95)
    print(f"Saved PNG: {output_path} ({canvas.size[0]}x{canvas.size[1]})")

    # Optional JPG
    if output_jpg:
        jpg_path = str(Path(output_path).with_suffix(".jpg"))
        canvas.convert("RGB").save(jpg_path, "JPEG", quality=85)
        print(f"Saved JPG: {jpg_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Assemble comic panels into a long-form vertical comic.")
    parser.add_argument("--title", default="科普漫画", help="Comic title")
    parser.add_argument("--subtitle", default="", help="Subtitle text")
    parser.add_argument("--panels", required=True, help="Path to panels.json")
    parser.add_argument("--output", default="comic.png", help="Output file path")
    parser.add_argument("--width", type=int, default=1080, help="Output width in px")
    parser.add_argument("--padding", type=int, default=40, help="Horizontal padding in px")
    parser.add_argument("--text-band-h", type=int, default=95, help="Text band height in px")
    parser.add_argument("--title-h", type=int, default=180, help="Title area height in px")
    parser.add_argument("--gap", type=int, default=10, help="Gap between elements in px")
    parser.add_argument("--output-jpg", action="store_true", help="Also export JPG version")

    args = parser.parse_args()

    with open(args.panels, "r", encoding="utf-8") as f:
        panels_data = json.load(f)

    assemble(
        panels_data=panels_data,
        title=args.title,
        subtitle=args.subtitle,
        width=args.width,
        padding=args.padding,
        text_band_h=args.text_band_h,
        title_h=args.title_h,
        gap=args.gap,
        output_path=args.output,
        output_jpg=args.output_jpg,
    )


if __name__ == "__main__":
    main()
