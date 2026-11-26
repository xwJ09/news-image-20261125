#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: broadsheet front page, 1024x1024.
36 stories, all happened or first reported Wed 25 Nov 2026 (see
~/workspace/makefun/news-image-20261125-notes.md for the fact list).
Reuses the v5 newspaper formula (masthead + giant date, numbers strip,
4 numeral-led lead panels, UTC timeline, mid grid, world map with
numbered pins, ALSO list, DATE CHECK footer, epistemic tags + per-story
sources) with all-new stories for 25 November.
PIL + DejaVu only; no photos, so no garbled text.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def f(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

SERIF = f("DejaVuSerif-Bold.ttf", 46)
MAST = f("DejaVuSans-Bold.ttf", 17)
SUB = f("DejaVuSans-Bold.ttf", 20)
COUNT = f("DejaVuSans-Bold.ttf", 16)
STRIP_N = f("DejaVuSans-Bold.ttf", 23)
STRIP_L = f("DejaVuSans-Bold.ttf", 10)
STRIP_T = f("DejaVuSans-Bold.ttf", 13)
TAG = f("DejaVuSans-Bold.ttf", 13)
TAGSM = f("DejaVuSans-Bold.ttf", 11)
HEAD = f("DejaVuSans-Bold.ttf", 18)
CAP = f("DejaVuSans.ttf", 13)
TL_H = f("DejaVuSans-Bold.ttf", 15)
TL_T = f("DejaVuSans-Bold.ttf", 11)
MID_T = f("DejaVuSans-Bold.ttf", 13)
MID_C = f("DejaVuSans.ttf", 11)
MID_S = f("DejaVuSans.ttf", 10)
ALSO = f("DejaVuSans-Bold.ttf", 10)
LAB = f("DejaVuSans-Bold.ttf", 13)
FOOT = f("DejaVuSans.ttf", 12)
FOOTB = f("DejaVuSans-Bold.ttf", 12)
PIN = f("DejaVuSans-Bold.ttf", 9)
PINSM = f("DejaVuSans-Bold.ttf", 8)

NAVY = (16, 42, 87)
STEEL = (24, 78, 150)
GREEN = (0, 128, 0)
RUST = (178, 58, 32)
TEAL = (0, 128, 128)
AMBER = (166, 110, 0)
SLATE = (70, 85, 105)
PAPER = (240, 244, 248)
GOLD = (255, 193, 7)
GOLDD = (176, 124, 0)
REDL = (255, 130, 120)
MAPFILL = (205, 214, 224)
MAPLINE = (150, 162, 175)
OCEAN = (232, 240, 247)

TAGC = {"CONFIRMED": GREEN, "OFFICIAL": STEEL, "REPORTED": AMBER,
        "CLAIM": RUST, "ONGOING": TEAL}

def wrap(text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def num_font(text, max_size, max_width):
    size = max_size
    while size > 20 and d.textlength(text, font=f("DejaVuSans-Bold.ttf", size)) > max_width:
        size -= 2
    return f("DejaVuSans-Bold.ttf", size)

def draw_segments(x, y, segs, font):
    """Draw [(text, colour), ...] left to right; returns end x."""
    for text, colour in segs:
        d.text((x, y), text, font=font, fill=colour)
        x += d.textlength(text, font=font)
    return x

# ---------------------------------------------------------------- header
d.rectangle([0, 0, W, 108], fill=NAVY)
d.text((32, 10), "THE DAY IN NUMBERS", font=MAST, fill=GOLD)
counts = "36 STORIES  \u2022  7 REGIONS  \u2022  16 FIELDS"
d.text((W - 32 - d.textlength(counts, font=COUNT), 10), counts,
       font=COUNT, fill="white")
d.text((32, 34), "WEDNESDAY 25 NOVEMBER 2026", font=SERIF, fill="white")
d.text((32, 84), "TARIFFS ON 14 ECONOMIES  \u2022  GDP 4.3%  \u2022  NETANYAHU CASE FALTERS",
       font=SUB, fill=REDL)
d.rectangle([0, 108, W, 112], fill=GOLD)

# ---------------------------------------------------------- numbers strip
d.text((32, 122), "BY THE", font=STRIP_T, fill=GOLDD)
d.text((32, 138), "NUMBERS", font=STRIP_T, fill=GOLDD)
strip = [
    ("-6.2%", "KOSPI", RUST),
    ("-2%", "NASDAQ", RUST),
    ("\u20ac115BN", "UKRAINE NEEDS", STEEL),
    ("36%", "BANGLADESH WAGE", GREEN),
    ("$44BN", "CROWDSTRIKE DEAL", STEEL),
    ("4,400KG", "IOWA BLAST", RUST),
]
sx = 150
for num, lab, col in strip:
    d.text((sx, 120), num, font=STRIP_N, fill=col)
    d.text((sx, 148), lab, font=STRIP_L, fill=SLATE)
    sx += 142
d.rectangle([0, 160, W, 163], fill=GOLD)

# ------------------------------------------------------------- lead panels
def illustration(kind, x, y, col):
    """Small flat scene, 64x64 box at (x, y)."""
    if kind == "globe":
        d.ellipse([x + 8, y + 8, x + 56, y + 56], fill=col)
        d.arc([x + 8, y + 8, x + 56, y + 56], 200, 340, fill="white",
              width=3)
        d.arc([x + 16, y + 14, x + 48, y + 50], 200, 340, fill="white",
              width=2)
        d.line([x + 8, y + 32, x + 56, y + 32], fill="white", width=2)
        d.ellipse([x + 40, y + 40, x + 54, y + 54], fill=GREEN)
        d.line([x + 47, y + 40, x + 47, y + 30], fill=GREEN, width=3)
    elif kind == "bank":
        d.polygon([(x + 32, y + 6), (x + 6, y + 22), (x + 58, y + 22)],
                  fill=col)
        for i, xx in enumerate((x + 12, x + 28, x + 44)):
            d.rectangle([xx, y + 26, xx + 8, y + 52], fill=col)
        d.rectangle([x + 6, y + 54, x + 58, y + 60], fill=col)
    elif kind == "scales":
        d.line([x + 32, y + 6, x + 32, y + 58], fill=col, width=3)
        d.line([x + 8, y + 14, x + 56, y + 14], fill=col, width=3)
        d.polygon([(x + 8, y + 14), (x + 22, y + 14), (x + 15, y + 36)],
                  outline=col, width=2)
        d.polygon([(x + 42, y + 14), (x + 56, y + 14), (x + 49, y + 36)],
                  outline=col, width=2)
        d.rectangle([x + 20, y + 58, x + 44, y + 62], fill=col)
    elif kind == "rocket":
        d.polygon([(x + 32, y + 2), (x + 44, y + 22), (x + 20, y + 22)],
                  fill=col)
        d.rectangle([x + 20, y + 22, x + 44, y + 48], fill=col)
        d.ellipse([x + 27, y + 28, x + 37, y + 38], fill="white")
        d.polygon([(x + 20, y + 42), (x + 8, y + 56), (x + 20, y + 52)],
                  fill=col)
        d.polygon([(x + 44, y + 42), (x + 56, y + 56), (x + 44, y + 52)],
                  fill=col)
        d.polygon([(x + 26, y + 48), (x + 38, y + 48), (x + 32, y + 62)],
                  fill=RUST)

def panel(x, y, w, h, colour, num, tag, tagline, source, headline, caption,
          kind):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=PAPER,
                        outline=colour, width=3)
    d.rounded_rectangle([x, y, x + w, y + 28], radius=12, fill=colour)
    d.rectangle([x, y + 14, x + w, y + 28], fill=colour)
    d.text((x + 12, y + 6), tagline, font=TAG, fill="white")
    right = f"{tag} \u00b7 {source}"
    d.text((x + w - 12 - d.textlength(right, font=TAGSM), y + 7), right,
           font=TAGSM, fill="white")
    # Giant numeral, left column.
    nfont = num_font(num, 92, 150)
    bbox = d.textbbox((0, 0), num, font=nfont)
    n_top = y + 28 + (h - 28 - (bbox[3] - bbox[1])) // 2 - bbox[1]
    d.text((x + 14, n_top), num, font=nfont, fill=colour)
    # Headline + caption, middle column.
    tx, tw = x + 172, w - 172 - 84
    hlines = wrap(headline, HEAD, tw)[:2]
    clines = wrap(caption, CAP, tw)[:3]
    block_h = len(hlines) * 22 + 4 + len(clines) * 16
    yy = y + 28 + max(0, (h - 28 - block_h) // 2)
    for line in hlines:
        d.text((tx, yy), line, font=HEAD, fill=(20, 20, 20))
        yy += 22
    yy += 4
    for line in clines:
        d.text((tx, yy), line, font=CAP, fill=SLATE)
        yy += 16
    illustration(kind, x + w - 76, y + 28 + (h - 28 - 64) // 2, colour)
    print(tagline, "headline:", len(hlines), "caption:", len(clines))

PW, PH = 478, 138
panel(24, 168, PW, PH, STEEL, "14", "REPORTED", "1 \u00b7 TRADE \u2022 USA",
      "REUTERS", "TARIFFS ON 14 ECONOMIES",
      "US targets China and EU after court kills earlier duties.", "globe")
panel(522, 168, PW, PH, GREEN, "4.3%", "OFFICIAL", "2 \u00b7 ECONOMY \u2022 USA",
      "BEA", "US ECONOMY GREW 4.3% IN Q3",
      "Second estimate lifts growth from 3.4%; inflation 3.8%.", "bank")
panel(24, 314, PW, PH, RUST, "4000", "REPORTED", "3 \u00b7 LAW \u2022 ISRAEL",
      "REUTERS", "DROP THE NETANYAHU BRIBERY CASE",
      "Judges say conviction unlikely; PM calls trial \u2018over\u2019.", "scales")
panel(522, 314, PW, PH, TEAL, "24", "OFFICIAL", "4 \u00b7 SPACE \u2022 CHINA",
      "CMSA", "FIRST PAKISTANI IN ORBIT",
      "Shenzhou-24 docks with Tiangong after 3.5-hour flight.", "rocket")

# ------------------------------------------------------------ UTC timeline
d.text((32, 464), "THE DAY IN UTC", font=LAB, fill=NAVY)
timeline = [
    ("01:19", "Ukraine needs \u20ac115bn for 2027"),
    ("04:00", "Shenzhou-24 docks with Tiangong"),
    ("09:13", "US tells citizens to leave Iran"),
    ("11:24", "Gaza strike kills Hamas official"),
    ("19:22", "Poland plans no-fly zone"),
]
tx = 32
for hour, ev in timeline:
    d.text((tx, 484), hour, font=TL_H, fill=RUST)
    for i, line in enumerate(wrap(ev, TL_T, 156)[:2]):
        d.text((tx, 502 + i * 13), line, font=TL_T, fill=SLATE)
    tx += 195

# -------------------------------------------------------------- mid stories
d.text((32, 534), "MORE FROM THE DAY", font=LAB, fill=NAVY)
mids = [
    ("5. HORMUZ: TWO TANKERS HIT MINES",
     "IRGC says mines struck two tankers; both ablaze.", "CLAIM", "IRGC"),
    ("6. POLAND PLANS NO-FLY ZONE",
     "Zone near Ukraine border after Russian incursions.", "OFFICIAL",
     "REUTERS"),
    ("7. US TO CITIZENS: LEAVE IRAN",
     "Warning after attacks in Bahrain, Kuwait, Riyadh.", "OFFICIAL",
     "STATE DEPT"),
    ("8. HOUTHIS ADVANCE ON ADEN",
     "Fighters 50 miles from Yemen's temporary capital.", "REPORTED",
     "REUTERS"),
    ("9. SAUDI COALITION HITS HODEIDAH",
     "Strikes port and targets in Saada and Amran.", "OFFICIAL",
     "COALITION"),
    ("10. ODESA STRIKE KILLS 2",
     "Russian strike hits Odesa; Kyiv flats ablaze, 2 hurt.", "REPORTED",
     "AP"),
    ("11. UKRAINE HITS 2 REFINERIES",
     "Drones set Syzran and Kuibyshev ablaze overnight.", "REPORTED",
     "REUTERS"),
    ("12. KOSPI PLUNGES 6.2%",
     "Samsung -9.9%, SK Hynix -11.1% as AI rout spreads.", "CONFIRMED",
     "REUTERS"),
    ("13. NASDAQ NEARS BEAR MARKET",
     "Down 2% Wed, ~20% off October's record high.", "CONFIRMED",
     "REUTERS"),
    ("14. ANTHROPIC BELOW IPO PRICE",
     "Shares slide below $83 after record listing.", "REPORTED",
     "REUTERS"),
    ("15. CROWDSTRIKE BUYS ZSCALER",
     "$44bn deal as cyber threats mount.", "REPORTED", "REUTERS"),
    ("16. MICROSOFT DECLARES 'CODE RED'",
     "Emergency after historic outage, memos show.", "REPORTED",
     "REUTERS"),
]
for i, (title, cap, tag, src) in enumerate(mids):
    cx = 24 + (i % 3) * 329
    cy = 556 + (i // 3) * 45
    d.text((cx, cy), title, font=MID_T, fill=(20, 20, 20))
    d.text((cx, cy + 17), cap, font=MID_C, fill=SLATE)
    draw_segments(cx, cy + 31, [(tag, TAGC[tag]), (" \u00b7 " + src, SLATE)],
                  MID_S)
    print("mid", title[:20], "title w:",
          round(d.textlength(title, font=MID_T)), "cap w:",
          round(d.textlength(cap, font=MID_C)))

# ------------------------------------------------------- map + ALSO TODAY
d.text((32, 738), "WHERE IT HAPPENED \u2014 PINS = STORY NUMBERS", font=LAB,
       fill=NAVY)
d.text((530, 738), "ALSO TODAY", font=LAB, fill=NAVY)
d.rectangle([24, 760, 506, 918], fill=OCEAN)

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 64)],
    # South America
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-45, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-73, -53), (-70, -20), (-80, -5), (-80, 5)],
    # Africa
    [(-10, 35), (-5, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (48, 11), (40, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, 4), (-8, 4), (-15, 12),
     (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 52),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (110, 20), (108, 12), (105, 9), (100, 8),
     (97, 16), (92, 21), (88, 22), (80, 13), (77, 8), (73, 16),
     (66, 25), (60, 25), (57, 26), (52, 26), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (27, 37), (23, 36), (19, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Australia
    [(114, -22), (114, -30), (116, -35), (124, -33), (130, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -23), (146, -19), (142, -11), (137, -12), (132, -11),
     (126, -14), (122, -17), (118, -20)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 40),
     (142, 44), (140, 42)],
    # Indonesia islands
    [(95, 5), (100, 0), (104, -3), (106, -6), (104, -6), (99, -1)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3),
     (109, 0)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -7), (136, -4), (131, -2)],
]

def mx(lon):
    return 24 + (lon + 170) / 360 * 482

def my(lat):
    return 760 + (75 - lat) / 130 * 158

for poly in CONTINENTS:
    pts = [(mx(lon), my(lat)) for lon, lat in poly]
    d.polygon(pts, fill=MAPFILL, outline=MAPLINE)

PINS = [
    ("1\u00b72", -100, 40), ("13", -73, 41), ("14", -122, 42),
    ("24", -87, 28), ("31", -75, 10),
    ("3\u00b732", 37, 33), ("5\u00b77", 60, 25), ("8\u00b79", 43, 12),
    ("6\u00b710", 28, 48), ("11", 50, 53), ("12\u00b719", 126, 40),
    ("18", 119, 29), ("4", 100, 40), ("29", 108, 28), ("22", 28, 23),
    ("23", 107, -7), ("25", 16, 34), ("20", 160, -9), ("27", 12, 56),
    ("28", 0, 51), ("30", -9, 38), ("21", 12, 42),
]
for label, lon, lat in PINS:
    x, y = mx(lon), my(lat)
    if "\u00b7" in label:
        font = PINSM
        tw = d.textlength(label, font=font)
        hw, hh = tw / 2 + 5, 8
        d.rounded_rectangle([x - hw, y - hh, x + hw, y + hh], radius=hh,
                            fill=RUST, outline="white", width=1)
        d.text((x - tw / 2, y - 5), label, font=font, fill="white")
    else:
        font = PIN
        r = 6
        d.ellipse([x - r, y - r, x + r, y + r], fill=RUST,
                  outline="white", width=1)
        tw = d.textlength(label, font=font)
        th = font.getbbox(label)[3]
        d.text((x - tw / 2, y - th / 2 - 1), label, font=font, fill="white")

also = [
    (17, "RSF DRONES KILL 19 IN SUDAN", "AP", "REPORTED"),
    (18, "SHANGHAI CHIEF PROBED", "RTRS", "REPORTED"),
    (19, "N. KOREA EXPELS SWISS", "KCNA", "OFFICIAL"),
    (20, "AUSTRALIA-SOLOMONS PACT", "AP", "OFFICIAL"),
    (21, "POPE LAMENTS COP31 FAILURE", "AP", "OFFICIAL"),
    (22, "CAIRO FUEL FIRE: 30 DEAD", "AP", "REPORTED"),
    (23, "MINERS TRAPPED IN JAVA", "AP", "ONGOING"),
    (24, "CESSNA CRASH: 6 DEAD", "AP", "REPORTED"),
    (25, "2 LIBYAN OFFICERS DIE", "LNA", "REPORTED"),
    (26, "ARMY DETONATES 4,400 KG", "AP", "OFFICIAL"),
    (27, "DENMARK HEADSCARF BAN", "SCMP", "OFFICIAL"),
    (28, "MET 'RACIST' REPORT", "SCMP", "REPORTED"),
    (29, "HUANG MONEY TRAIL", "REUTERS", "REPORTED"),
    (30, "ABREGO GARCIA LEAVES US", "AP", "REPORTED"),
    (31, "COLOMBIA HOSTAGES FREED", "AP", "REPORTED"),
    (32, "TURKISH HELI CRASH: 5 DEAD", "AP", "REPORTED"),
    (33, "TATUM 41, CELTICS WIN", "AP", "CONFIRMED"),
    (34, "FLAGG 24+12, MAVS WIN", "AP", "CONFIRMED"),
    (35, "MCDANIELS 34, WOLVES ROUT", "AP", "CONFIRMED"),
    (36, "EAST COAST STORM", "REUTERS", "REPORTED"),
]
for i, (n, title, src, tag) in enumerate(also):
    ax = 530 + (i % 2) * 238
    ay = 762 + (i // 2) * 15
    num = f"{n}."
    d.text((ax, ay), num, font=ALSO, fill=TAGC[tag])
    d.text((ax + 24, ay), f"{title} ({src})", font=ALSO, fill=(20, 20, 20))
    print("also", n, "w:",
          round(24 + d.textlength(f"{title} ({src})", font=ALSO)))

# ------------------------------------------------------------------ footer
d.rectangle([0, 926, W, 930], fill=GOLD)
draw_segments(32, 938, [
    ("TAGS:  ", (20, 20, 20)),
    ("CONFIRMED", GREEN), (" 2+ outlets  ", SLATE),
    ("OFFICIAL", STEEL), (" on record  ", SLATE),
    ("REPORTED", AMBER), (" one outlet  ", SLATE),
    ("CLAIM", RUST), (" one side  ", SLATE),
    ("ONGOING", TEAL), (" unfolding", SLATE),
], FOOTB)
dc = ("DATE CHECK \u2014 Every story happened, or was first reported, on Wednesday "
      "25 November 2026 (UTC). Left out: COP31 Sun 22 Nov \u00b7 Nvidia +31%, AWACS, "
      "Iran sanctions, Colombia bomb \u2014 Mon 23 Nov \u00b7 Huawei, Dell, Dow 50,000, "
      "turkey pardon, O'Hare, CIA breach \u2014 Tue 24 Nov \u00b7 Sparta II Sat 21 Nov.")
yy = 958
for line in wrap(dc, FOOT, 960):
    d.text((32, yy), line, font=FOOT, fill=SLATE)
    yy += 15
foot = "THE DAY IN NUMBERS  \u2022  36 STORIES  \u2022  COMPILED 25 NOVEMBER 2026"
d.text(((W - d.textlength(foot, font=FOOTB)) / 2, 996), foot,
       font=FOOTB, fill=NAVY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
