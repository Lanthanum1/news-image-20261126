#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Written by hand in this session. Pure PIL, no network, deterministic:
same input -> same bytes every run (fixed fonts, fixed layout, no dates
taken from the clock).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)      # off-white newsprint
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
LIGHT = (232, 228, 218)
DARKBOX = (24, 24, 24)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag(draw, x, y, label):
    f = font(15, bold=True)
    w = int(draw.textlength(label, font=f)) + 16
    draw.rectangle([x, y, x + w, y + 24], fill=RED)
    draw.text((x + 8, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    CW = W - 2 * M  # 952

    # ---- Masthead ----
    d.text((M, 26), "THE WORLD IN ONE PICTURE", font=font(52, bold=True), fill=INK)
    d.text((M, 92), "Thursday, 26 November 2026  •  The day's world news, at a glance",
           font=font(20), fill=GREY)
    d.rectangle([M, 128, W - M, 133], fill=RED)
    d.rectangle([M, 137, W - M, 139], fill=INK)

    # ---- Hero story ----
    hy = 156
    tag(d, M, hy, "TRADE  •  LEAD STORY")
    d.text((M, hy + 36), "Trump's new tariff hit list:",
           font=font(42, bold=True), fill=INK)
    d.text((M, hy + 86), "US threatens India, China",
           font=font(42, bold=True), fill=INK)
    draw_wrapped(d, M, hy + 146,
                 "Washington proposes tariffs of up to 25% on Indian goods "
                 "(17% if a trade deal is clinched) and as high as 40% on "
                 "China. India is among seven nations on the new list.",
                 font(20), CW, leading=27)
    # hero fact strip inside hero area
    fy = hy + 146 + 2 * 27 + 10
    d.rectangle([M, fy, W - M, fy + 2], fill=LIGHT)
    d.text((M, fy + 12), "INDIA up to 25%  •  CHINA up to 40%  •  7 nations named",
           font=font(19, bold=True), fill=RED)

    # ---- Divider before grid ----
    gy = 420
    d.rectangle([M, gy, W - M, gy + 2], fill=INK)

    stories = [
        ("MARKETS", "Memory-chip selloff deepens",
         "SK Hynix -11% and Samsung -9.9% in Seoul; KOSPI -6.2% as "
         "TrendForce cuts its 2027 DRAM price outlook."),
        ("MIDDLE EAST", "Houthis strike Riyadh again",
         "Second attack on the KAFD tower in under a week; 2 Indians "
         "injured. Tankers hit near the Strait of Hormuz."),
        ("UNITED STATES", "Trump may pardon Jensen Huang",
         "After Nvidia's comeback, Trump floats a pardon; a Democrat "
         "accuses Huang of breaching export controls."),
        ("WORLD", "Ramaphosa report ruled unlawful",
         "South African court voids the impeachment report. China to "
         "welcome its first foreign astronaut aboard Tiangong."),
        ("WORLD", "Bangladesh workers win 36% pay rise",
         "Garment workers secure the hike after weeks of protests. "
         "China investigates Politburo member Chen Jining."),
        ("SPORT", "Teen star smashes 204 off 53 balls",
         "15-year-old Vaibhav Sooryavanshi stuns UAE. Real Madrid "
         "thrash PSV 5-1: Bellingham stunner, Mbappe brace."),
    ]

    col_w = (CW - 28) // 2
    row_h = 138
    y0 = gy + 14
    for i, (cat, head, summ) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 28)
        y = y0 + row * row_h
        tag(d, x, y, cat)
        draw_wrapped(d, x, y + 30, head, font(21, bold=True), col_w, leading=25)
        draw_wrapped(d, x, y + 72, summ, font(15), col_w, leading=19)

    # ---- Bottom markets strip ----
    by = y0 + 3 * row_h + 8
    d.rectangle([M, by, W - M, by + 2], fill=INK)
    d.text((M, by + 12), "MARKETS AT A GLANCE",
           font=font(17, bold=True), fill=RED)
    draw_wrapped(d, M, by + 38,
                 "KOSPI -6.2%  •  SK Hynix -11%  •  Samsung -9.9%  •  "
                 "SKHY -9.9%  •  Micron -11%  •  Goldman cuts SK Hynix "
                 "target 43%; BNP cuts Micron to $775",
                 font(18), CW, leading=24)
    fy2 = by + 38 + 2 * 24 + 14
    d.rectangle([M, fy2, W - M, fy2 + 2], fill=LIGHT)
    d.text((M, fy2 + 10),
           "Also: Shein agrees $100m US settlement  •  Flipkart CEO to step down in December",
           font=font(16), fill=GREY)
    d.text((M, H - 34), "26 November 2026 — sources: wire reports of the day.",
           font=font(14), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
