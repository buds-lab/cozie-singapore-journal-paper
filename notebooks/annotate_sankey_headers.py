"""Add column headers and a color key to the hand-organized survey-flow Sankey (Figure 8).

Presentation only: the source image (cozie-sankey-organized.png) is copied unchanged onto a
taller canvas, with a header band naming the survey question in each node column (using the
question wording of the micro-survey figure) and a footer key explaining node colors and band
widths. Node x-positions and colors were measured from the source image and match the stage
colors in the companion notebook's C1 Sankey cell.

Usage (from the repository root):
    python notebooks/annotate_sankey_headers.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIG = Path("figures/data_characterization")
SRC = FIG / "cozie-sankey-organized.png"
OUT = FIG / "cozie-sankey-organized-labeled.png"

SCALE = 2          # upsample so added text renders crisply
HEADER_H = 78      # header band height (source px)
FOOTER_H = 34      # footer band height (source px)

# (center x of node column in source px, header lines, swatch colors for the stage(s) in the column)
COLUMNS = [
    (120, ["Noise Distraction", "Nearby?"], ["#4F94CD"]),
    (330, ["Kind of", "Noise?"], ["#7B5C87"]),
    (539, ["Wearing", "Earphones?"], ["#8CC152"]),
    (740, ["Thermal", "Preference"], ["#E5943A"]),
    (942, ["Location"], ["#4E9D9D"]),
    (1143, ["Kind of Office? /", "Kind of Transport?"], ["#1A1A1A", "#7FC6E4"]),
    (1330, ["Alone or", "in a Group?"], ["#7A4B2C"]),
    (1585, ["Activity", "(Alone / Group)"], ["#CDA24C"]),
]
FOOTER = ("Node color identifies the survey question (column header); grey band width is proportional "
          "to the number of responses along each path; conditional questions are answered only by the "
          "responses that reach them.")


def font(size, bold=False):
    candidates = (["/System/Library/Fonts/Supplemental/Arial Bold.ttf"] if bold else []) + [
        "/System/Library/Fonts/Supplemental/Arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size * SCALE)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    src = Image.open(SRC).convert("RGB")
    w, h = src.size
    big = src.resize((w * SCALE, h * SCALE), Image.LANCZOS)
    canvas = Image.new("RGB", (w * SCALE, (h + HEADER_H + FOOTER_H) * SCALE), "white")
    canvas.paste(big, (0, HEADER_H * SCALE))
    d = ImageDraw.Draw(canvas)

    f_head, f_foot = font(15, bold=True), font(12.5)
    sw, gap, line_h = 13 * SCALE, 2 * SCALE, 19 * SCALE
    for cx, lines, colors in COLUMNS:
        cx *= SCALE
        y0 = (HEADER_H * SCALE - len(lines) * line_h) // 2 + 6 * SCALE
        for i, text in enumerate(lines):
            tw = d.textlength(text, font=f_head)
            d.text((cx - tw / 2, y0 + i * line_h), text, font=f_head, fill="#2c3e50")
        # color swatch(es) above the header text act as the color key
        total = len(colors) * sw + (len(colors) - 1) * gap
        sx = cx - total / 2
        sy = y0 - sw - 5 * SCALE
        for c in colors:
            d.rectangle([sx, sy, sx + sw, sy + sw], fill=c, outline="#888888", width=1)
            sx += sw + gap

    tw = d.textlength(FOOTER, font=f_foot)
    d.text(((w * SCALE - tw) / 2, (HEADER_H + h + 9) * SCALE), FOOTER, font=f_foot, fill="#555555")
    canvas.save(OUT, dpi=(300, 300))
    print(f"Saved {OUT} ({canvas.width} x {canvas.height} px)")


if __name__ == "__main__":
    main()
