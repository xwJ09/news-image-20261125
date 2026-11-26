#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Wednesday 25 November 2026.

A single 1024x1024 PNG summing up that day's world news, built only from
the 36 verified stories in the notes file. Pure Pillow + DejaVu, no network.
Run:  python3 draw_image.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 248, 242)
INK = (18, 18, 18)
GREY = (92, 92, 88)
GOLD = (176, 132, 30)
GOLD_SOFT = (238, 226, 196)
RED = (158, 28, 28)
OCEAN = (216, 230, 240)
LAND = (198, 198, 190)
PANEL = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, width, fill=INK, max_lines=None, leading=None):
    """Draw wrapped text; returns the y just below the last line drawn."""
    lines = wrap(text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    step = leading if leading is not None else int(fnt.size * 1.28)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def rule(d, x0, y, x1, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def section_head(d, x, y, label, x1):
    d.text((x, y), label, font=sans_b(13), fill=INK)
    rule(d, x + sans_b(13).getlength(label) + 10, y + 8, x1, 1, GOLD)
    return y + 20


# ---------------------------------------------------------------- masthead
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28                      # side margin
RX = W - MX                  # right edge

d.text((MX, 12), "THE WORLD TODAY", font=serif_b(52), fill=INK)
d.text((RX - sans_b(12).getlength("36 STORIES  ·  7 REGIONS  ·  16 FIELDS"), 30),
       "36 STORIES  ·  7 REGIONS  ·  16 FIELDS", font=sans_b(12), fill=GOLD)
rule(d, MX, 78, RX, 3, INK)
d.text((MX, 86), "WEDNESDAY 25 NOVEMBER 2026", font=sans_b(19), fill=RED)
d.text((RX - sans(13).getlength("THE DAY IN FULL — EVERY STORY SOURCED"), 90),
       "THE DAY IN FULL — EVERY STORY SOURCED", font=sans(13), fill=GREY)
rule(d, MX, 112, RX, 1, INK)

# ------------------------------------------------------- four lead panels
LEADS = [
    ("14", "US PROPOSES TARIFFS ON 14 ECONOMIES",
     "After the Supreme Court struck down earlier across-the-board duties, "
     "Washington proposes new levies on China and the EU among 14 economies.",
     "REPORTED · REUTERS"),
    ("4.3%", "US ECONOMY GREW 4.3% IN Q3",
     "Second estimate lifts annualised growth from 3.4%. October PCE inflation "
     "+0.3% on the month, +3.8% on the year; core PCE +3.3%.",
     "OFFICIAL · BEA"),
    ("4000", "JUDGES: DROP NETANYAHU CASE 4000",
     "Judges recommend prosecutors drop the Case 4000 bribery charge and "
     "reconsider Case 2000. The prime minister calls the trial “over”.",
     "REPORTED · REUTERS / CNN / HAARETZ"),
    ("24", "SHENZHOU-24 DOCKS; PAKISTANI FIRST ABOARD",
     "Spacecraft docks with Tiangong at 03:56 UTC, about 3.5 hours after launch. "
     "Muhammad Zeeshan Ali is the first foreigner aboard the station.",
     "OFFICIAL · CMSA / XINHUA"),
]

LY, LH = 120, 170
GAP = 10
PW = (RX - MX - 3 * GAP) // 4
for i, (num, head, body, src) in enumerate(LEADS):
    x0 = MX + i * (PW + GAP)
    d.rectangle([x0, LY, x0 + PW, LY + LH], fill=PANEL, outline=INK, width=2)
    d.rectangle([x0, LY, x0 + PW, LY + 6], fill=GOLD)
    nw = sans_b(40).getlength(num)
    d.text((x0 + (PW - nw) / 2, LY + 12), num, font=sans_b(40), fill=RED)
    y = LY + 62
    y = para(d, x0 + 10, y, head, sans_b(12), PW - 20, max_lines=2, leading=15)
    y = para(d, x0 + 10, y + 3, body, sans(10), PW - 20, max_lines=4, leading=13)
    d.text((x0 + 10, LY + LH - 15), src, font=sans_b(8), fill=GREY)

# ---------------------------------------------------------- numbers strip
NUMBERS = [
    ("KOSPI -6.2%", "Seoul plunges; Samsung -9.9%, SK Hynix -11.1%"),
    ("NASDAQ -2%", "Near bear market, ~20% off its October record"),
    ("EUR 115BN", "Ukraine needs for 2027, Zelenskyy says"),
    ("+36%", "Bangladesh raises garment minimum wage"),
    ("$44BN", "CrowdStrike buys Zscaler"),
    ("4,400 KG", "US Army detonates lead azide in Iowa"),
]

NY, NH = 298, 44
d.rectangle([MX, NY, RX, NY + NH], fill=GOLD_SOFT, outline=GOLD, width=1)
CW = (RX - MX) // 6
for i, (val, lab) in enumerate(NUMBERS):
    x0 = MX + i * CW
    if i:
        d.line([(x0, NY + 6), (x0, NY + NH - 6)], fill=GOLD, width=1)
    d.text((x0 + 8, NY + 4), val, font=sans_b(15), fill=RED)
    para(d, x0 + 8, NY + 24, lab, sans(8), CW - 14, fill=GREY,
         max_lines=2, leading=10)

# ------------------------------------------------------------- UTC timeline
TIMELINE = [
    ("01:19", "Zelenskyy: Ukraine needs EUR 115bn external financing for 2027."),
    ("04:00", "Shenzhou-24 docks with Tiangong at 03:56 UTC."),
    ("09:13", "US tells its citizens to leave Iran; State Dept alert."),
    ("11:24", "Israeli strike kills Hamas security official Abu al-Awf in Gaza."),
    ("19:22", "Poland to create a no-fly zone near the Ukraine border."),
]

TY = section_head(d, MX, 350, "THE DAY IN UTC — FIRST REPORTED", RX)
TW = (RX - MX) // 5
axis_y = TY + 22
rule(d, MX, axis_y, RX, 2, INK)
for i, (tm, txt) in enumerate(TIMELINE):
    cx = MX + i * TW + TW // 2
    d.ellipse([cx - 5, axis_y - 5, cx + 5, axis_y + 5], fill=GOLD,
              outline=INK, width=1)
    tw = sans_b(13).getlength(tm)
    d.text((cx - tw / 2, TY + 2), tm, font=sans_b(13), fill=RED)
    para(d, MX + i * TW + 6, axis_y + 10, txt, sans(9), TW - 12,
         max_lines=3, leading=12)

# ---------------------------------------------------------- mid stories 5-16
MIDS = [
    (5, "HORMUZ: TWO TANKERS HIT MINES",
     "IRGC says naval mines struck two tankers, both ablaze in the strait.",
     "CLAIM · IRGC"),
    (6, "POLAND PLANS NO-FLY ZONE",
     "Warsaw to create a zone near the Ukraine border after Russian airspace incursions.",
     "OFFICIAL · REUTERS"),
    (7, "US TO CITIZENS: LEAVE IRAN",
     "State Dept alert after Iran attacks in Bahrain and Kuwait and a Houthi strike on a Riyadh tower.",
     "OFFICIAL · STATE DEPT"),
    (8, "HOUTHIS ADVANCE ON ADEN",
     "Fighters about 50 miles from Yemen's temporary capital; residents prepare to flee.",
     "REPORTED · REUTERS"),
    (9, "SAUDI COALITION HITS HODEIDAH",
     "Coalition strikes the port and targets in Saada and Amran.",
     "OFFICIAL · COALITION"),
    (10, "ODESA STRIKE KILLS 2",
     "Russian strike kills two and injures three, including a child; Kyiv flats ablaze.",
     "REPORTED · AP"),
    (11, "UKRAINE HITS 2 REFINERIES",
     "Drones set Rosneft's Syzran and Kuibyshev refineries ablaze; one killed, 145 drones downed.",
     "REPORTED · REUTERS"),
    (12, "KOSPI PLUNGES 6.2%",
     "Samsung -9.9%, SK Hynix -11.1%; Nikkei -2.78%, Taiex about -5%.",
     "CONFIRMED · REUTERS"),
    (13, "NASDAQ NEARS BEAR MARKET",
     "Down 2% on Wednesday, about 20% off its October record; VIX up 60% in November.",
     "CONFIRMED · REUTERS"),
    (14, "ANTHROPIC BELOW IPO PRICE",
     "Shares fall well below the $83 IPO price days after the record listing.",
     "REPORTED · REUTERS"),
    (15, "CROWDSTRIKE BUYS ZSCALER",
     "$44bn deal as cyber threats mount.",
     "REPORTED · REUTERS"),
    (16, "MICROSOFT DECLARES 'CODE RED'",
     "Emergency after a historic outage, internal memos show.",
     "REPORTED · REUTERS"),
]

MY = section_head(d, MX, 446, "THE DAY'S NEWS", RX)
COLW = (RX - MX - 2 * 12) // 3
ROWH = 53
for idx, (num, head, body, src) in enumerate(MIDS):
    col, row = idx % 3, idx // 3
    x0 = MX + col * (COLW + 12)
    y0 = MY + row * ROWH
    d.text((x0, y0), "%d. %s" % (num, head), font=sans_b(12), fill=INK)
    y = para(d, x0, y0 + 15, body, sans(10), COLW, max_lines=2, leading=12)
    d.text((x0, y0 + 40), src, font=sans_b(8), fill=GREY)

# ------------------------------------------- schematic map + also today 17-36
AY = section_head(d, MX, 684, "AROUND THE WORLD — ALSO TODAY", RX)
MAP_X, MAP_Y, MAP_W, MAP_H = MX, AY, 332, 228
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=OCEAN,
            outline=INK, width=2)
d.text((MAP_X + 8, MAP_Y + 4), "SCHEMATIC MAP — NOT TO SCALE",
       font=sans_b(8), fill=GREY)

# Rough continent outlines, in fractions of the map box (my own sketch).
CONTINENTS = [
    [(0.05, 0.20), (0.10, 0.10), (0.22, 0.08), (0.28, 0.14), (0.26, 0.22),
     (0.20, 0.26), (0.14, 0.32), (0.08, 0.30)],                       # N America
    [(0.20, 0.44), (0.26, 0.42), (0.30, 0.50), (0.27, 0.64),
     (0.22, 0.60)],                                                     # S America
    [(0.45, 0.34), (0.53, 0.32), (0.58, 0.40), (0.56, 0.54),
     (0.50, 0.57), (0.46, 0.46)],                                      # Africa
    [(0.55, 0.12), (0.75, 0.07), (0.95, 0.12), (0.97, 0.24),
     (0.85, 0.30), (0.70, 0.28), (0.58, 0.24)],                       # Eurasia
    [(0.82, 0.64), (0.90, 0.62), (0.93, 0.70), (0.86, 0.74)],          # Australia
]
for poly in CONTINENTS:
    pts = [(MAP_X + fx * MAP_W, MAP_Y + fy * MAP_H) for fx, fy in poly]
    d.polygon(pts, fill=LAND, outline=GREY)

# Numbered pins: (story number, x-fraction, y-fraction).
PINS = [(5, 0.60, 0.38), (6, 0.56, 0.20), (10, 0.58, 0.25), (17, 0.54, 0.50),
        (18, 0.83, 0.32), (19, 0.86, 0.26), (22, 0.56, 0.43), (23, 0.84, 0.58),
        (24, 0.16, 0.30), (25, 0.50, 0.38), (31, 0.22, 0.44), (32, 0.60, 0.28)]
for num, fx, fy in PINS:
    cx, cy = MAP_X + fx * MAP_W, MAP_Y + fy * MAP_H
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD, outline=INK, width=1)
    label = str(num)
    lw = sans_b(8).getlength(label)
    d.text((cx - lw / 2, cy - 6), label, font=sans_b(8), fill=INK)

ALSO = [
    (17, "RSF DRONES KILL 19 IN SUDAN", "Blue Nile strikes hit homes and a dam; 20 wounded.", "AP"),
    (18, "SHANGHAI CHIEF PROBED FOR GRAFT", "China investigates politburo member Chen Jining.", "REUTERS"),
    (19, "N. KOREA EXPELS SWISS ENVOY", "Pyongyang shuts office; envoy has 48 hours to leave.", "KCNA"),
    (20, "SOLOMONS-AUSTRALIA TREATY", "Treaty bars any foreign military base in Solomons.", "AP"),
    (21, "POPE LAMENTS COP31 FAILURE", "'Extreme events ever more frequent,' the Pope says.", "AP"),
    (22, "CAIRO FUEL FIRE: 30 DEAD", "Petroleum vehicle overturns; 27 vehicles burn, 25 hurt.", "AP"),
    (23, "MINERS TRAPPED IN FLOODED JAVA MINE", "26-29 workers unaccounted in West Java gold mine.", "AP"),
    (24, "CESSNA CRASH: 6 DEAD OFF MISSISSIPPI", "Plane plunges into the Gulf off Mississippi.", "AP"),
    (25, "2 LIBYAN OFFICERS DIE OF WOUNDS", "Die of wounds from a drone strike on the Merkury.", "LNA"),
    (26, "ARMY DETONATES 4,400 KG OF EXPLOSIVES", "Controlled Iowa blast of degraded lead azide.", "AP"),
    (27, "DENMARK BANS HEADSCARVES", "Prosecutors barred from religious dress.", "SCMP"),
    (28, "UK POLICE STILL 'RACIST', REVIEW FINDS", "Met still institutionally racist, review finds.", "SCMP"),
    (29, "ALICE HUANG MONEY TRAIL", "Firms linked to AI servers inside China.", "REUTERS"),
    (30, "ABREGO GARCIA LEAVES US FOR SPAIN", "Migrant symbol of Trump crackdown departs.", "AP"),
    (31, "COLOMBIA HOSTAGES FREED IN RAID", "Forces storm a Cartagena supermarket; all are safe.", "AP"),
    (32, "TURKISH HELI CRASH: 5 DEAD", "Military helicopter crashes in training.", "AP"),
    (33, "TATUM 41, CELTICS BEAT WIZARDS 131-116", "Boston ends a four-game skid.", "AP"),
    (34, "FLAGG 24+12, MAVS BEAT NUGGETS 120-101", "Dallas wins in the NBA Cup.", "AP"),
    (35, "MCDANIELS 34, WOLVES ROUT NETS 142-116", "Minnesota beats Brooklyn.", "AP"),
    (36, "EAST COAST STORM LOOMS", "Rain and strong winds to hit Thanksgiving travel.", "REUTERS"),
]

AX = MAP_X + MAP_W + 20
ACOLW = (RX - AX - 12) // 2
AROWH = 23
for idx, (num, head, detail, src) in enumerate(ALSO):
    col, row = idx % 2, idx // 2
    x0 = AX + col * (ACOLW + 12)
    y0 = AY + row * AROWH
    d.text((x0, y0), "%d. %s" % (num, head), font=sans_b(10), fill=INK)
    d.text((x0, y0 + 12), "%s · %s" % (detail, src), font=sans(9), fill=GREY)

# ------------------------------------------------------------ DATE CHECK footer
FY = 942
rule(d, MX, FY, RX, 2, GOLD)
d.text((MX, FY + 6), "DATE CHECK — NOT TODAY'S NEWS", font=sans_b(12), fill=RED)
para(d, MX, FY + 24,
     "Excluded as earlier days: COP31 collapsed Sun 22 Nov; Nvidia +31%, the NATO "
     "AWACS announcement, US Iran sanctions and the Colombia car bomb Mon 23 Nov; "
     "the Huawei verdict, Dell revenue, Dow 50,000, the turkey pardon, the O'Hare "
     "ground stop, the CIA breach and consumer confidence Tue 24 Nov. Every one of "
     "the 36 stories above happened, or was first reported, on Wednesday 25 November 2026.",
     sans(10), RX - MX, max_lines=3, leading=13)
rule(d, MX, 1012, RX, 1, INK)

img.save(OUT, "PNG")
print("wrote", OUT, img.size)
