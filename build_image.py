#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 editorial front-page infographic summing up
the world news of Tuesday, 17 November 2026. Pure Pillow drawing, no
photographic material, no network. Run: python3 build_image.py"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (250, 247, 240)   # warm newsprint
INK = (17, 17, 17)
NAVY = (27, 58, 92)
RED = (176, 42, 30)
GREY = (90, 86, 80)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bridge(d, x, y, s, c):
    # suspension bridge: deck, two pylons, cables
    d.line([(x, y + 0.62 * s), (x + s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.22 * s, y + 0.15 * s), (x + 0.22 * s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.78 * s, y + 0.15 * s), (x + 0.78 * s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.22 * s, y + 0.15 * s), (x + 0.5 * s, y + 0.62 * s)], fill=c, width=2)
    d.line([(x + 0.78 * s, y + 0.15 * s), (x + 0.5 * s, y + 0.62 * s)], fill=c, width=2)
    # broken span: gap in the deck
    d.line([(x + 0.44 * s, y + 0.62 * s), (x + 0.44 * s, y + 0.78 * s)], fill=c, width=3)
    d.line([(x + 0.56 * s, y + 0.62 * s), (x + 0.56 * s, y + 0.78 * s)], fill=c, width=3)
    d.line([(x, y + 0.85 * s), (x + s, y + 0.85 * s)], fill=c, width=3)


def draw_tanker(d, x, y, s, c):
    # oil tanker hull + waves
    d.polygon([(x, y + 0.35 * s), (x + s, y + 0.35 * s),
               (x + 0.85 * s, y + 0.62 * s), (x + 0.15 * s, y + 0.62 * s)], fill=c)
    d.rectangle([x + 0.55 * s, y + 0.12 * s, x + 0.8 * s, y + 0.35 * s], fill=c)
    d.line([(x + 0.62 * s, y + 0.02 * s), (x + 0.62 * s, y + 0.12 * s)], fill=c, width=3)
    for wy in (0.74, 0.86):
        d.arc([x, y + wy * s - 6, x + 0.45 * s, y + wy * s + 6], 0, 180, fill=c, width=3)
        d.arc([x + 0.55 * s, y + wy * s - 6, x + s, y + wy * s + 6], 0, 180, fill=c, width=3)


def draw_globe(d, x, y, s, c):
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    d.ellipse([x + 0.28 * s, y, x + 0.72 * s, y + s], outline=c, width=3)
    d.line([(x, y + 0.5 * s), (x + s, y + 0.5 * s)], fill=c, width=3)
    d.arc([x, y + 0.18 * s, x + s, y + 0.82 * s], 200, 340, fill=c, width=3)


def draw_chip(d, x, y, s, c):
    d.rectangle([x + 0.18 * s, y + 0.18 * s, x + 0.82 * s, y + 0.82 * s],
                outline=c, width=4)
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s], fill=c)
    for i in range(3):
        t = 0.3 + 0.2 * i
        d.line([(x + t * s, y), (x + t * s, y + 0.18 * s)], fill=c, width=3)
        d.line([(x + t * s, y + 0.82 * s), (x + t * s, y + s)], fill=c, width=3)
        d.line([(x, y + t * s), (x + 0.18 * s, y + t * s)], fill=c, width=3)
        d.line([(x + 0.82 * s, y + t * s), (x + s, y + t * s)], fill=c, width=3)


def draw_ledger(d, x, y, s, c):
    d.rectangle([x + 0.08 * s, y + 0.08 * s, x + 0.92 * s, y + 0.92 * s],
                outline=c, width=4)
    for i, yy in enumerate((0.28, 0.48, 0.68)):
        d.line([(x + 0.22 * s, y + yy * s), (x + 0.62 * s, y + yy * s)],
               fill=c, width=3)
    # red X mark on the audit
    d.line([(x + 0.68 * s, y + 0.55 * s), (x + 0.88 * s, y + 0.78 * s)], fill=RED, width=5)
    d.line([(x + 0.88 * s, y + 0.55 * s), (x + 0.68 * s, y + 0.78 * s)], fill=RED, width=5)


def draw_jet(d, x, y, s, c):
    # fighter jet, side profile, nose to the right
    d.polygon([(x + 0.02 * s, y + 0.55 * s), (x + 0.55 * s, y + 0.42 * s),
               (x + 0.98 * s, y + 0.5 * s), (x + 0.55 * s, y + 0.62 * s)],
              fill=c)
    d.polygon([(x + 0.18 * s, y + 0.55 * s), (x + 0.30 * s, y + 0.18 * s),
               (x + 0.42 * s, y + 0.55 * s)], fill=c)          # tail fin
    d.polygon([(x + 0.38 * s, y + 0.60 * s), (x + 0.55 * s, y + 0.95 * s),
               (x + 0.68 * s, y + 0.60 * s)], fill=c)          # wing
    d.line([(x + 0.02 * s, y + 0.55 * s), (x + 0.30 * s, y + 0.55 * s)],
           fill=c, width=3)


STORIES = [
    {
        "tag": "EUROPE  ·  WAR",
        "color": (140, 43, 43),
        "icon": draw_bridge,
        "headline": "Kerch Bridge hit again — road span collapses",
        "summary": "Ukraine struck the bridge to Crimea for a second day; Russia hit Kyiv's river bridges in reply.",
    },
    {
        "tag": "MIDDLE EAST",
        "color": (138, 90, 0),
        "icon": draw_tanker,
        "headline": "Tankers struck near Hormuz as third U.S. carrier arrives",
        "summary": "Iran said two tankers hit mines by the strait; a U.S. carrier joined two others in the region.",
    },
    {
        "tag": "ASIA-PACIFIC",
        "color": (27, 94, 122),
        "icon": draw_globe,
        "headline": "Trump in Manila; Xi–Trump–Putin summit set",
        "summary": "China confirmed the first three-way meeting of Xi, Trump and Putin, in Shenzhen on Thursday 19 November.",
    },
    {
        "tag": "TECH  ·  MARKETS",
        "color": (31, 107, 58),
        "icon": draw_chip,
        "headline": "Nvidia beats forecasts in first results without Huang",
        "summary": "Revenue hit $115.8bn, up 103% on a year ago; the board said it will not reinstate Jensen Huang.",
    },
    {
        "tag": "UNITED STATES",
        "color": (46, 58, 89),
        "icon": draw_ledger,
        "headline": "Pentagon fails its ninth straight financial audit",
        "summary": "Auditors could not verify accounts covering $4.8tn in assets; 14 of 25 units passed for the first time.",
    },
    {
        "tag": "ASIA-PACIFIC",
        "color": (91, 58, 140),
        "icon": draw_jet,
        "headline": "Japan scrambles jets after Russian airspace incursion",
        "summary": "Tokyo launched fighters and lodged a strong protest after two suspected Russian aircraft crossed in.",
    },
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title_f = font(SERIF_B, 46)
    d.text((W // 2, 34), "THE WORLD IN ONE PICTURE", font=title_f,
           fill=NAVY, anchor="ma")
    d.line([(MARGIN, 96), (W - MARGIN, 96)], fill=INK, width=2)

    # Date band
    d.rectangle([MARGIN, 108, W - MARGIN, 164], fill=NAVY)
    date_f = font(SANS_B, 36)
    d.text((W // 2, 136), "TUESDAY, 17 NOVEMBER 2026", font=date_f,
           fill=WHITE, anchor="mm")

    sub_f = font(SERIF, 21)
    d.text((W // 2, 188), "Six stories that defined the day — from Crimea to Manila",
           font=sub_f, fill=GREY, anchor="ma")

    # ---- Story grid: 2 cols x 3 rows ----
    gap = 16
    pw = (W - 2 * MARGIN - gap) // 2          # 476
    ph = 236
    gx, gy = MARGIN, 214
    tag_f = font(SANS_B, 15)
    head_f = font(SANS_B, 26)
    body_f = font(SANS, 19)

    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph

        d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)
        d.rectangle([x0, y0, x1, y0 + 6], fill=st["color"])

        # tag chip
        tw = d.textlength(st["tag"], font=tag_f)
        chip_w = int(tw) + 22
        d.rounded_rectangle([x0 + 16, y0 + 18, x0 + 16 + chip_w, y0 + 46],
                            radius=6, fill=st["color"])
        d.text((x0 + 27, y0 + 32), st["tag"], font=tag_f, fill=WHITE, anchor="lm")

        # icon, top right
        st["icon"](d, x1 - 78, y0 + 16, 56, st["color"])

        # headline, up to 2 lines (fail loudly rather than truncate text)
        inner = pw - 32
        lines = wrap(d, st["headline"], head_f, inner)
        assert len(lines) <= 2, f"headline too long: {st['headline']!r} -> {lines}"
        hy = y0 + 62
        for ln in lines:
            d.text((x0 + 16, hy), ln, font=head_f, fill=INK)
            hy += 32

        # summary, up to 3 lines (fail loudly rather than truncate text)
        slines = wrap(d, st["summary"], body_f, inner)
        assert len(slines) <= 3, f"summary too long: {st['summary']!r} -> {slines}"
        sy = y0 + 62 + len(lines) * 32 + 8
        for ln in slines:
            d.text((x0 + 16, sy), ln, font=body_f, fill=(51, 51, 51))
            sy += 25

    # ---- Footer: sources ----
    foot_f = font(SANS, 15)
    d.text((W // 2, 990),
           "Sources: BBC · Reuters · Al Jazeera · Forbes · Military Times · Just Security · Outlook India — all reported 17 November 2026",
           font=foot_f, fill=GREY, anchor="ms")

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
