#!/usr/bin/env python3
"""THE WORLD TODAY - Saturday, 21 November 2026.

Draws a one-page newspaper front page summing up the world's news of
Saturday 21 November 2026, using only the Python standard library.
Writes entry.png into MAKEFUN_OUTPUT_DIR (default "out").
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (30, 64, 120)
GREY = (90, 90, 86)
TAN = (214, 200, 160)
DARK = (24, 24, 24)

# 5x7 bitmap font: each glyph is 7 strings of 5 chars, '#' = on.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '%': ("10001", "10010", "00100", "01000", "01001", "10001", "10001"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
}

# --- canvas ---------------------------------------------------------------
px = bytearray(PAPER[0:1] * 0)  # placeholder, replaced in main()
buf = bytearray()


def new_canvas():
    global buf
    buf = bytearray(PAPER * W * H)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, c)


def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)


def circle(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_px(xx, yy, c)


def ring(cx, cy, r, c, t=2):
    for yy in range(cy - r - t, cy + r + t + 1):
        for xx in range(cx - r - t, cx + r + t + 1):
            d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
            if r - t <= d <= r + t:
                set_px(xx, yy, c)


def poly(points, c):
    # simple scanline fill for a convex-ish polygon
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(int(x1 + (y - y1) * (x2 - x1) / (y2 - y1)))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for x in range(xs[k], xs[k + 1] + 1):
                set_px(x, y, c)


# --- text ------------------------------------------------------------------
def text_w(s, sc):
    return len(s) * 6 * sc - sc


def draw_char(x, y, ch, sc, c):
    g = FONT.get(ch.upper(), FONT[' '])
    for r in range(7):
        row = g[r]
        for col in range(5):
            if row[col] == '1':
                rect(x + col * sc, y + r * sc, sc, sc, c)


def draw_text(x, y, s, sc, c=INK):
    cx = x
    for ch in s:
        draw_char(cx, y, ch, sc, c)
        cx += 6 * sc
    return cx


def draw_centered(y, s, sc, c=INK, cx=W // 2):
    draw_text(cx - text_w(s, sc) // 2, y, s, sc, c)


def wrap(s, sc, maxw):
    words = s.split(' ')
    lines, cur = [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if text_w(t, sc) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, sc, maxw, c=INK, lh=None):
    lh = lh or (9 * sc)
    for ln in wrap(s, sc, maxw):
        draw_text(x, y, ln, sc, c)
        y += lh
    return y


# --- PNG -------------------------------------------------------------------
def chunk(tag, data):
    out = struct.pack('>I', len(data)) + tag + data
    out += struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', ihdr)
    data += chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    data += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(data)
    return len(data)


# --- layout ----------------------------------------------------------------
def badge(x, y, n, sc=2):
    circle(x + 9 * sc // 2, y + 7 * sc // 2, 9 * sc // 2 + 2, RED)
    draw_centered(y + 2, str(n), sc, (255, 255, 255), x + 9 * sc // 2 + 1)
    return 11 * sc


def story(x, y, w, num, kicker, head, deck, sc_head=2, sc_deck=1):
    bx = badge(x, y, num)
    draw_text(x + bx + 4, y + 2, kicker, 2, RED)
    y += 24
    y = para(x, y, head, sc_head, w, INK, 9 * sc_head + 2)
    y += 3
    y = para(x, y, deck, sc_deck, w, (60, 60, 58), 10)
    return y + 4


def draw_page():
    new_canvas()
    # outer frame
    rect(0, 0, W, 10, INK)
    rect(0, H - 10, W, 10, INK)
    rect(0, 0, 10, H, INK)
    rect(W - 10, 0, 10, H, INK)

    # masthead
    draw_centered(28, "THE WORLD TODAY", 7, INK)
    hline(40, 108, W - 80, INK, 4)
    draw_centered(122, "SATURDAY, 21 NOVEMBER 2026", 4, RED)
    draw_centered(158, "ONE DAY. EVERY STORY THAT MATTERED.", 2, GREY)
    hline(40, 188, W - 80, INK, 2)

    # lead story
    draw_centered(206, "RUSSIA RAINS 400 DRONES", 4, INK)
    draw_centered(240, "AND 110 MISSILES ON UKRAINE", 4, INK)
    draw_centered(282, "Eight killed in Kyiv as bridges and rail stations are hit.", 2, (60, 60, 58))
    draw_centered(302, "Two missiles and a drone land in Poland. Tusk calls it", 2, (60, 60, 58))
    draw_centered(322, "a deliberate provocation. NATO: a grave violation.", 2, (60, 60, 58))
    hline(40, 348, W - 80, INK, 2)

    # --- world map panel ---
    mx, my, mw, mh = 40, 362, W - 80, 210
    rect(mx, my, mw, mh, (232, 226, 205))
    vline(mx, my, mh, INK, 2)
    vline(mx + mw, my, mh, INK, 2)
    hline(mx, my, mw, INK, 2)
    hline(mx, my + mh, mw, INK, 2)
    draw_text(mx + 10, my + 8, "WHERE IT HAPPENED - 21 NOVEMBER 2026", 2, BLUE)
    # rough continents (equirect-ish sketch)
    # North America
    poly([(90, 430), (150, 405), (230, 410), (250, 440), (210, 470), (150, 465), (100, 450)], TAN)
    # South America
    poly([(250, 490), (300, 485), (315, 520), (290, 555), (265, 530)], TAN)
    # Europe
    poly([(470, 415), (540, 405), (570, 425), (550, 450), (500, 450), (470, 435)], TAN)
    # Africa
    poly([(480, 470), (540, 465), (565, 500), (545, 545), (505, 540), (480, 500)], TAN)
    # Asia
    poly([(580, 405), (700, 395), (820, 410), (860, 440), (800, 470), (680, 465), (600, 445)], TAN)
    # Australia
    poly([(800, 520), (850, 515), (865, 535), (830, 545), (800, 540)], TAN)

    markers = [
        (1, 540, 420, "KYIV", -42, 14), (2, 500, 408, "POLAND", -30, -24),
        (3, 470, 420, "BRUSSELS", -78, 2), (4, 600, 435, "ANTALYA", 18, -6),
        (5, 265, 520, "PERU", 18, -6), (6, 560, 472, "GAZA", -52, 14),
        (7, 800, 425, "SEOUL", 18, -6), (8, 640, 418, "TBILISI", 18, -22),
        (9, 640, 465, "RIYADH", 18, 8), (10, 165, 440, "NEW YORK", 18, -6),
    ]
    for n, x, y, lab, dx, dy in markers:
        circle(x, y, 11, RED)
        ring(x, y, 15, RED, 1)
        draw_centered(y - 7, str(n), 2, (255, 255, 255), x)
        draw_text(x + dx, y + dy, lab, 1, INK)

    # --- three columns ---
    col_y = 600
    col_w = 296
    xs = [40, 366, 692]
    hline(40, 588, W - 80, INK, 2)

    y1 = story(xs[0], col_y, col_w, 2, "POLAND",
               "MISSILES LAND ON NATO SOIL",
               "Two Russian missiles and a suspected drone land in south-east Poland. Warsaw: a provocation.")
    y1 = story(xs[0], y1, col_w, 3, "BRUSSELS",
               "UK AND EU SIGN LANDMARK POST-BREXIT DEAL",
               "Food checks scrapped, carbon markets linked, youth mobility for 100,000 each side.")
    story(xs[0], y1, col_w, 6, "GAZA",
          "STRIKES KILL PALESTINIANS IN GAZA",
          "Israeli strikes kill six in Gaza on Friday, civil defence says. West Bank violence goes on.")

    y2 = story(xs[1], col_y, col_w, 4, "ANTALYA, TURKIYE",
               "COP31 CLIMATE TALKS RUN PAST DEADLINE",
               "Nearly 200 nations fail to agree a final text as the summit goes into overtime.")
    y2 = story(xs[1], y2, col_w, 5, "PERU",
               "6.8 QUAKE SHAKES PERU, LIMA FLEES OUTDOORS",
               "A magnitude 6.8 quake centred in Junin rattles Lima. No immediate casualties or major damage.")
    story(xs[1], y2, col_w, 7, "SEOUL",
          "EX-PM HAN'S 15-YEAR SENTENCE OVERTURNED",
          "Court quashes Han Duck-soo's sentence over the martial-law attempt. Retrial ordered.")

    y3 = story(xs[2], col_y, col_w, 8, "TBILISI",
               "GAS BLAST KILLS SIX, FLATTENS FLATS",
               "A suspected gas blast partly collapses a Tbilisi apartment block. Six dead, including a child.")
    y3 = story(xs[2], y3, col_w, 9, "RIYADH",
               "HOUTHI MISSILES AIMED AT RIYADH STOPPED",
               "Saudi-led coalition intercepts three Houthi missiles aimed at Riyadh after a strike on the PIF tower.")
    story(xs[2], y3, col_w, 10, "NEW YORK",
          "AI ROUT: S&P 500 FALLS INTO CORRECTION",
          "S&P 500 down 3.7%, Nasdaq down 5.3%. Nikkei falls 5.06%, gold down 3.98%, Bitcoin below $58,000.")

    # --- also in brief ---
    by = 898
    hline(40, by - 8, W - 80, INK, 2)
    draw_text(40, by + 2, "ALSO TODAY:", 2, RED)
    para(40, by + 26,
         "BUKELE TO SEEK THIRD TERM IN EL SALVADOR - US COURT LETS TRUMP END TPS FOR 600,000 VENEZUELANS - "
         "CANCER PILL MAKES TUMOURS UNDETECTABLE IN 1 IN 12 PATIENTS - GEN Z PROTESTS IN 25 EUROPEAN COUNTRIES - "
         "ALCARAZ UNBEATEN AT ATP FINALS - TRUMP-XI-PUTIN SUMMIT ENDS WITH JOINT DECLARATION",
         1, W - 80, INK, 13)

    # --- market ticker ---
    ty = 956
    rect(10, ty, W - 20, 58, DARK)
    draw_text(28, ty + 12, "MARKETS 21 NOV:", 2, (255, 210, 90))
    draw_text(28, ty + 34,
              "S&P -3.7%   NAS -5.3%   NIKKEI -5.1%   GOLD -4.0%   BTC -4.2%   BRENT $89.87 +0.5%",
              2, (255, 255, 255))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    draw_page()
    path = os.path.join(outdir, "entry.png")
    n = write_png(path)
    # verify IHDR dimensions back
    with open(path, 'rb') as f:
        data = f.read(33)
    w2, h2 = struct.unpack('>II', data[16:24])
    assert (w2, h2) == (W, H), (w2, h2)
    assert n <= 1048576, n
    print("wrote %s %dx%d %d bytes" % (path, w2, h2, n))


if __name__ == "__main__":
    main()
