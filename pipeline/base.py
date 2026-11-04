import json, math, re, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
import os as _os
FB = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fonts", "Poppins-Bold.ttf") if "__file__" in globals() else "fonts/Poppins-Bold.ttf"
if not _os.path.exists(FB): FB = "fonts/Poppins-Bold.ttf"
_fc = {}
def font(sz):
    sz = int(sz)
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FB, sz)
    return _fc[sz]

SCRIPT = open("script.txt", encoding="utf-8").read().strip().split("\n")

# ---------------- timing ----------------
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","voice.mp3"]).decode())
log = subprocess.run(["ffmpeg","-i","voice.mp3","-af","silencedetect=noise=-35dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
sil = []
if se and (not ss or se[0] < ss[0]): sil.append((0.0, se[0])); se = se[1:]
for a, b in zip(ss, se + [dur]*(len(ss)-len(se))): sil.append((a, b))
speech = []; cur = 0.0
for a, b in sil:
    if a > cur: speech.append((cur, a))
    cur = b
if cur < dur - 0.05: speech.append((cur, dur))
gaps = [(speech[i][1], speech[i+1][0]) for i in range(len(speech)-1)]

tokens = []  # (word, line, punct_after)
for li, line in enumerate(SCRIPT):
    ws = line.split()
    for wi, w in enumerate(ws):
        tokens.append([w, li, bool(re.search(r"[.,?!…]$", w)) or wi == len(ws)-1])
wt = np.array([len(re.sub(r"\W", "", w)) + 1.5 for w, _, _ in tokens], float)

def voiced_map(frac_list, s0, s1):
    """map fractions of voiced time inside [s0,s1] to real time"""
    ivs = [(max(a, s0), min(b, s1)) for a, b in speech if b > s0 and a < s1]
    tot = sum(b - a for a, b in ivs) or 1e-6
    out = []
    for fr in frac_list:
        need = fr * tot
        for a, b in ivs:
            if need <= b - a + 1e-9: out.append(a + need); break
            need -= b - a
        else: out.append(s1)
    return out

# initial proportional boundaries
cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
bt = voiced_map(cum, speech[0][0], speech[-1][1])
pb = [k+1 for k, t in enumerate(tokens[:-1]) if t[2]]  # boundary after token k
# DP align punctuation boundaries to gaps
INF = 1e9
nP, nG = len(pb), len(gaps)
D = np.full((nP+1, nG+1), INF); D[0, :] = np.arange(nG+1)*0.9; D[:, 0] = np.arange(nP+1)*0.5
bk = {}
for i in range(1, nP+1):
    for j in range(1, nG+1):
        g = (gaps[j-1][0]+gaps[j-1][1])/2
        c = [D[i-1, j-1] + abs(bt[pb[i-1]] - g)*1.2, D[i-1, j] + 0.5, D[i, j-1] + 0.9]
        k = int(np.argmin(c)); D[i, j] = c[k]; bk[(i, j)] = k
i, j = nP, nG; anchors = []
while i > 0 and j > 0:
    k = bk[(i, j)]
    if k == 0: anchors.append((pb[i-1], gaps[j-1])); i -= 1; j -= 1
    elif k == 1: i -= 1
    else: j -= 1
anchors.sort()
starts = [0.0]*len(tokens); ends = [0.0]*len(tokens)
seg = [(0, speech[0][0])] + [(b, g) for b, g in anchors] + [(len(tokens), None)]
for n in range(len(seg)-1):
    b0 = seg[n][0]; b1 = seg[n+1][0]
    s0 = speech[0][0] if n == 0 else seg[n][1][1]
    s1 = speech[-1][1] if seg[n+1][1] is None else seg[n+1][1][0]
    w = wt[b0:b1]; c = np.concatenate([[0], np.cumsum(w)]) / w.sum()
    ts = voiced_map(c, s0, s1)
    for q in range(b1-b0):
        starts[b0+q] = ts[q]; ends[b0+q] = ts[q+1]
line_start = {}
for k, t in enumerate(tokens):
    line_start.setdefault(t[1], starts[k])
json.dump([[t[0], round(starts[k], 2), round(ends[k], 2)] for k, t in enumerate(tokens)], open("timing.json", "w"))

# chunks of max 3 words
chunks = []; curc = []
for k, t in enumerate(tokens):
    curc.append(k)
    if len(curc) == 3 or t[2] and re.search(r"[.?!…]$", t[0]) or k == len(tokens)-1 or tokens[k+1][1] != t[1]:
        chunks.append(curc); curc = []
if curc: chunks.append(curc)

# audio rms per frame
raw = subprocess.check_output(["ffmpeg","-v","error","-i","voice.mp3","-ac","1","-ar","16000","-f","s16le","-"])
au = np.frombuffer(raw, np.int16).astype(float)/32768
def rms(t):
    a = int(t*16000); seg_ = au[a:a+533]
    return float(np.sqrt((seg_**2).mean())) if len(seg_) else 0.0

# ---------------- drawing helpers ----------------
class Cv:
    def __init__(s, w, h, sc, bg=(0,0,0,0), mode="RGBA"):
        s.sc = sc; s.im = Image.new(mode, (int(w*sc), int(h*sc)), bg); s.d = ImageDraw.Draw(s.im)
    def P(s, *v): return [x*s.sc for x in v]
    def rr(s, x0,y0,x1,y1, r, fill, outline=None, width=0):
        s.d.rounded_rectangle(s.P(x0,y0,x1,y1), r*s.sc, fill=fill, outline=outline, width=int(width*s.sc))
    def el(s, x0,y0,x1,y1, fill, outline=None, width=0):
        s.d.ellipse(s.P(x0,y0,x1,y1), fill=fill, outline=outline, width=int(width*s.sc))
    def circ(s, x,y,r, fill, **k): s.el(x-r,y-r,x+r,y+r, fill, **k)
    def rect(s, x0,y0,x1,y1, fill): s.d.rectangle(s.P(x0,y0,x1,y1), fill=fill)
    def poly(s, pts, fill): s.d.polygon([(x*s.sc, y*s.sc) for x, y in pts], fill=fill)
    def line(s, pts, fill, width):
        s.d.line([(x*s.sc, y*s.sc) for x, y in pts], fill=fill, width=int(width*s.sc), joint="curve")
        for x, y in (pts[0], pts[-1]): s.circ(x, y, width/2-0.5, fill)
    def arc(s, x0,y0,x1,y1, a0,a1, fill, width):
        s.d.arc(s.P(x0,y0,x1,y1), a0, a1, fill=fill, width=int(width*s.sc))
    def text(s, xy, txt, sz, fill, anchor="mm", stroke=0, sf=None):
        s.d.text((xy[0]*s.sc, xy[1]*s.sc), txt, font=font(sz*s.sc), fill=fill, anchor=anchor,
                 stroke_width=int(stroke*s.sc), stroke_fill=sf)
    def out(s, w, h):
        return s.im.resize((w, h), Image.LANCZOS)

DARK = (40, 30, 30)
SKIN = (245, 198, 160)

def face_closed(c, cx, cy, sz=1.0):
    for dx in (-0.38, 0.38):
        c.arc(cx+dx*100*sz-22*sz, cy-14*sz, cx+dx*100*sz+22*sz, cy+14*sz, 20, 160, DARK, 5*sz)

def sleeper_head(c, cx, cy, r, hair=(90,60,40), skin=SKIN, tilt=0):
    c.circ(cx, cy-r*0.25, r*1.02, hair)
    c.circ(cx, cy, r, skin)
    c.el(cx-r*0.95, cy-r*1.0, cx+r*0.95, cy-r*0.35, hair)
    for dx in (-0.38, 0.38):
        c.arc(cx+dx*r-r*0.2, cy-r*0.12, cx+dx*r+r*0.2, cy+r*0.14, 20, 160, DARK, max(3, r*0.07))
    c.el(cx-r*0.12, cy+r*0.35, cx+r*0.12, cy+r*0.55, (150, 70, 70))

# ---------------- Max sprite ----------------
HOOD = (47, 128, 237); HOOD2 = (35, 100, 190)
def make_max(expr="neutral", eyes=True, mouth=False, arms="down", gaze=0):
    if expr == "yawn": eyes = False; mouth = True
    c = Cv(600, 900, 3)
    def arm(sh, ang, ln=210):
        x = sh[0] + ln*math.cos(math.radians(ang)); y = sh[1] + ln*math.sin(math.radians(ang))
        c.line([sh, (x, y)], HOOD, 58); return (x, y)
    hands = []
    # legs + shoes
    c.rr(222, 660, 292, 850, 20, (43, 53, 80)); c.rr(308, 660, 378, 850, 20, (43, 53, 80))
    c.rr(200, 825, 296, 872, 22, (245, 245, 245)); c.rr(304, 825, 400, 872, 22, (245, 245, 245))
    c.rect(204, 860, 292, 872, (60, 60, 60)); c.rect(308, 860, 396, 872, (60, 60, 60))
    poses = {"down": (110, 70, 210), "up": (232, 308, 210), "reach": (110, -8, 230),
             "bat": (110, 300, 200), "scared": (38, 142, 150), "phone_hold": (38, 142, 150),
             "phone_ear": (110, 62, 135), "flash_bat": (150, 140, 120), "flash_photo": (150, 140, 120), "flash_photo_b": (150, 140, 120), "bat_hide": (96, 140, 120)}
    FBP = ("flash_bat", "flash_photo", "flash_photo_b", "bat_hide")
    la, ra, ln = poses[arms]
    if arms in ("phone_ear",) + FBP:
        hands.append(arm((198, 480), la, 210 if arms == "phone_ear" else 115))
        el_r = arm((402, 480), ra, ln)
    elif arms not in ("scared", "phone_hold"):
        hands.append(arm((198, 480), la, ln)); hands.append(arm((402, 480), ra, ln))
    # body
    c.rr(172, 425, 428, 712, 75, HOOD)
    c.rr(228, 590, 372, 665, 28, HOOD2)
    c.el(215, 395, 385, 478, HOOD2)
    c.rect(270, 395, 330, 440, (225, 175, 140))
    c.line([(276, 462), (270, 545)], (240, 240, 240), 9); c.line([(324, 462), (330, 545)], (240, 240, 240), 9)
    if arms in ("scared", "phone_hold"):
        hands.append(arm((198, 490), la, ln)); hands.append(arm((402, 490), ra, ln))
    if arms in FBP:
        # bat resting on the right shoulder, handle in the right hand in front of the chest
        hx, hy = el_r
        bx0, by0, bx1, by1 = hx + 10, hy + 40, 585, 95
        ang = math.atan2(by1 - by0, bx1 - bx0); nx, ny = -math.sin(ang), math.cos(ang)
        def bw(p): return 15 + 30*max(0, (p - 0.3)/0.7)
        pts = []
        for p in [i/10 for i in range(11)]:
            x = bx0 + (bx1 - bx0)*p; y = by0 + (by1 - by0)*p; pts.append((x + nx*bw(p), y + ny*bw(p)))
        for p in [i/10 for i in range(10, -1, -1)]:
            x = bx0 + (bx1 - bx0)*p; y = by0 + (by1 - by0)*p; pts.append((x - nx*bw(p), y - ny*bw(p)))
        c.poly([(x + 4, y + 4) for x, y in pts], (70, 44, 26))
        c.poly(pts, (214, 160, 98))
        c.line([(bx0 + (bx1-bx0)*0.4 + nx*14, by0 + (by1-by0)*0.4 + ny*14), (bx1 - nx*20, by1 - ny*20)], (236, 190, 130), 6)
        c.line([(bx0 - (bx1-bx0)*0.04, by0 - (by1-by0)*0.04), (bx0 + (bx1-bx0)*0.25, by0 + (by1-by0)*0.25)], (30, 30, 34), 32)   # grip tape
        c.circ(bx0 - (bx1-bx0)*0.05, by0 - (by1-by0)*0.05, 22, (30, 30, 34))                                                     # knob
        c.circ(bx1, by1, 44, (214, 160, 98))
        hands.append((hx, hy))
        # left forearm pointing toward the viewer's left, phone with flashlight in the hand
        ex, ey = hands[0]
        if arms == "bat_hide": hands.pop(0)
        else:
            c.line([(ex, ey), (165, 590)], HOOD, 52)
            hands[0] = (165, 590)
    if arms == "bat":
        hx, hy = hands[1]
        c.line([(hx, hy+30), (hx+40, 40)], (170, 110, 60), 34); c.circ(hx+40, 40, 24, (170, 110, 60))
    for hx, hy in hands: c.circ(hx, hy, 31, SKIN)
    if arms == "flash_bat":
        c.rr(100, 490, 178, 620, 12, (24, 24, 30)); c.rr(108, 498, 170, 612, 8, (52, 58, 80))
        c.circ(122, 512, 12, (255, 255, 225)); c.circ(122, 512, 6, (255, 255, 255))
        c.circ(168, 588, 30, SKIN); c.el(150, 548, 178, 586, SKIN); c.el(96, 560, 126, 590, SKIN)
    if arms in ("flash_photo", "flash_photo_b"):
        c.rr(58, 420, 208, 596, 4, (240, 238, 230))
        if arms == "flash_photo":
            c.rect(68, 430, 198, 552, (40, 44, 70)); c.rr(82, 500, 184, 548, 12, (60, 60, 110)); c.circ(140, 498, 22, SKIN); c.el(118, 470, 162, 492, (59, 42, 31))
        else:
            for k_ in range(4): c.line([(76, 450 + k_*30), (150 + (k_ % 2)*40, 446 + k_*30)], (40, 40, 60), 5)
        c.circ(168, 588, 30, SKIN); c.el(150, 548, 178, 586, SKIN); c.el(96, 560, 126, 590, SKIN)
    if arms == "phone_hold":
        c.rr(262, 520, 338, 640, 12, (24, 24, 30)); c.rr(270, 528, 330, 630, 8, (150, 200, 255))
        for hx, hy in hands: c.circ(hx, hy, 26, SKIN)
    # head
    c.el(142, 82, 458, 290, (59, 42, 31))
    c.el(132, 245, 188, 325, SKIN); c.el(412, 245, 468, 325, SKIN)
    c.el(155, 110, 445, 420, SKIN)
    c.poly([(158, 215), (178, 130), (235, 92), (300, 82), (365, 92), (422, 130), (442, 215), (410, 168),
            (378, 196), (345, 150), (305, 190), (262, 152), (228, 194), (192, 165)], (59, 42, 31))
    c.el(188, 318, 232, 346, (244, 160, 150)); c.el(368, 318, 412, 346, (244, 160, 150))
    # eyes
    for ex in (245, 355):
        if eyes:
            rx, ry, pr = (37, 43, 11) if expr == "shocked" else (31, 37, 15)
            c.el(ex-rx, 285-ry, ex+rx, 285+ry, (255, 255, 255), outline=DARK, width=4)
            c.circ(ex+gaze*11, 290, pr, DARK); c.circ(ex+gaze*11+5, 284, 5, (255, 255, 255))
        else:
            c.arc(ex-28, 268, ex+28, 300, 20, 160, DARK, 6)
    brows = {"neutral": [(215, 236, 270, 230), (330, 230, 385, 236)],
             "worried": [(213, 240, 272, 220), (328, 220, 387, 240)],
             "scared": [(213, 240, 272, 220), (328, 220, 387, 240)],
             "shocked": [(215, 210, 270, 200), (330, 200, 385, 210)],
             "shout": [(215, 222, 272, 236), (328, 236, 385, 222)],
             "angry": [(213, 220, 274, 242), (326, 242, 387, 220)], "yawn": [(215, 228, 270, 222), (330, 222, 385, 228)]}[expr]
    for x0, y0, x1, y1 in brows: c.line([(x0, y0), (x1, y1)], (59, 42, 31), 11)
    if mouth or expr == "shocked":
        big = expr in ("shocked", "shout", "yawn")
        c.el(300-(26 if big else 22), 345, 300+(26 if big else 22), 345+(52 if big else 36), (110, 30, 35))
        c.el(285, 345+(36 if big else 24), 315, 345+(50 if big else 34), (230, 110, 110))
    elif expr == "neutral": c.arc(262, 322, 338, 378, 25, 155, DARK, 6)
    elif expr in ("worried", "scared"): c.arc(272, 358, 328, 395, 205, 335, DARK, 6)
    elif expr == "angry": c.line([(275, 368), (325, 362)], DARK, 7)
    else: c.arc(270, 340, 330, 380, 25, 155, DARK, 6)
    if arms == "phone_ear":
        ex, ey = el_r
        c.rr(418, 232, 484, 372, 14, (24, 24, 30)); c.rr(424, 240, 478, 364, 9, (150, 200, 255))
        c.line([(ex, ey), (458, 368)], HOOD, 52)
        c.circ(452, 340, 32, SKIN); c.el(424, 318, 446, 362, (230, 182, 150))
    return c.out(600, 900)

_sp = {}
def sprite(expr, eyes, mouth, arms, scale, night=False, sq=1.0):
    key = (expr, eyes, mouth, arms, round(scale, 3), night, round(sq, 2))
    if key not in _sp:
        base_key = (expr, eyes, mouth, arms)
        if base_key not in _sp: _sp[base_key] = make_max(*base_key)
        im = _sp[base_key]
        if night:
            r, g, b, a = im.split()
            r = r.point(lambda v: int(v*0.55)); g = g.point(lambda v: int(v*0.6)); b = b.point(lambda v: int(v*0.85))
            im = Image.merge("RGBA", (r, g, b, a))
        w = int(600*scale/sq**0.5); h = int(900*scale*sq)
        _sp[key] = im.resize((w, h), Image.LANCZOS)
    return _sp[key]

def put_max(fr, x, feet, scale, expr, arms, t, local, night=False, talk=False, bob=True):
    eyes = not ((t % 3.3) < 0.13)
    mouth = talk and rms(t) > 0.04
    sq = 1.0
    if local < 0.25: sq = 1 - 0.12*math.sin(local/0.25*math.pi)
    sp = sprite(expr, eyes, mouth, arms, scale, night, sq)
    by = (math.sin(t*2*math.pi*0.9)*6*scale) if bob else 0
    if expr in ("scared",): x += math.sin(t*40)*2.5
    # shadow
    sh = Image.new("RGBA", (int(320*scale), int(60*scale)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([0, 0, sh.width-1, sh.height-1], fill=(0, 0, 0, 70))
    fr.alpha_composite(sh, (int(x - sh.width/2), int(feet - sh.height/2)))
    fr.alpha_composite(sp, (int(x - sp.width/2), int(feet - sp.height + by + 4*scale)))

# ---------------- backgrounds ----------------
S = 2
def bg_bedroom(night=False):
    c = Cv(W, H, S, mode="RGB")
    wall = (40, 48, 82) if night else (205, 226, 246); floor = (60, 50, 60) if night else (200, 155, 110)
    c.rect(0, 0, W, H, wall); c.rect(0, 1480, W, H, floor)
    for y in range(1520, H, 90): c.rect(0, y, W, y+4, tuple(int(v*0.85) for v in floor))
    c.rect(0, 1470, W, 1490, tuple(int(v*0.8) for v in wall))
    # window
    c.rr(90, 430, 470, 820, 14, (240, 240, 240) if not night else (90, 95, 120))
    sky = (15, 20, 50) if night else (140, 200, 250)
    c.rect(112, 452, 448, 798, sky)
    if night:
        c.circ(360, 540, 52, (245, 240, 200)); c.circ(382, 525, 46, sky)
        for sx, sy in [(160, 500), (220, 690), (300, 610), (410, 740), (180, 760)]: c.circ(sx, sy, 4, (255, 255, 230))
    else:
        c.circ(360, 560, 60, (255, 220, 90))
        c.el(150, 650, 330, 720, (255, 255, 255)); c.el(220, 620, 340, 700, (255, 255, 255))
    c.rect(276, 452, 284, 798, (230, 230, 230) if not night else (80, 85, 110)); c.rect(112, 621, 448, 629, (230, 230, 230) if not night else (80, 85, 110))
    # poster + clock
    c.rr(620, 460, 900, 800, 10, (240, 110, 90) if not night else (90, 50, 60))
    c.circ(760, 600, 70, (255, 210, 90) if not night else (110, 95, 60)); c.rect(650, 700, 870, 720, (255, 255, 255) if not night else (110, 100, 110))
    # bed
    bed = (120, 80, 60) if not night else (55, 40, 45)
    c.rr(600, 1240, 1060, 1300, 20, bed); c.rr(600, 1300, 1060, 1560, 26, bed)
    c.rr(620, 1270, 790, 1350, 30, (250, 250, 250) if not night else (110, 110, 130))
    c.rr(615, 1330, 1060, 1500, 30, (255, 160, 70) if not night else (70, 70, 120))
    if night:
        # door with lock on left
        c.rect(0, 0, 0, 0, wall)
    return c.out(W, H)

def bg_mom():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (240, 222, 200)); c.rect(0, 1480, W, H, (170, 130, 100))
    c.rr(80, 460, 400, 760, 10, (250, 250, 245)); c.rect(100, 480, 380, 740, (200, 190, 230))
    c.circ(240, 610, 80, (170, 150, 210))
    # nightstand + lamp
    c.rr(880, 1200, 1040, 1480, 10, (150, 100, 70)); c.rect(950, 1080, 966, 1200, (90, 70, 60))
    c.poly([(890, 1090), (1030, 1090), (995, 980), (925, 980)], (255, 220, 140))
    # bed
    c.rr(440, 1050, 880, 1130, 26, (110, 70, 55)); c.rr(440, 1130, 880, 1560, 28, (110, 70, 55))
    c.rr(470, 1110, 660, 1200, 34, (255, 255, 255))
    sleeper_head(c, 565, 1165, 62, hair=(150, 110, 80))
    c.rr(450, 1215, 880, 1470, 40, (150, 110, 200)); c.rr(450, 1215, 880, 1260, 20, (240, 240, 250))
    return c.out(W, H)

def car(c, x, y, col, hair):
    c.rr(x, y+70, x+380, y+200, 40, col); c.rr(x+60, y, x+300, y+110, 40, col)
    c.rr(x+85, y+20, x+275, y+95, 20, (190, 225, 245))
    sleeper_head(c, x+170, y+78, 28, hair=hair)
    c.circ(x+85, y+200, 40, (40, 40, 40)); c.circ(x+295, y+200, 40, (40, 40, 40))
    c.circ(x+85, y+200, 16, (170, 170, 170)); c.circ(x+295, y+200, 16, (170, 170, 170))

def bg_street(sunset=False):
    c = Cv(W, H, S, mode="RGB")
    top, bot = ((250, 150, 90), (255, 200, 140)) if sunset else ((120, 190, 245), (190, 228, 252))
    for y in range(0, 1300, 10):
        k = y/1300; c.rect(0, y, W, y+10, tuple(int(top[i]*(1-k)+bot[i]*k) for i in range(3)))
    if sunset: c.circ(780, 1000, 120, (255, 120, 70))
    bcol = [(150, 160, 190), (120, 130, 170), (170, 150, 170), (135, 150, 175)]
    if sunset: bcol = [(150, 100, 120), (120, 80, 110), (170, 110, 120), (135, 90, 115)]
    for i, (x0, w, h) in enumerate([(-20, 240, 560), (230, 200, 700), (440, 260, 520), (710, 200, 640), (900, 220, 480)]):
        col = bcol[i % 4]; c.rect(x0, 1250-h, x0+w, 1250, col)
        for wy in range(1250-h+40, 1220, 80):
            for wx in range(x0+25, x0+w-40, 60):
                c.rect(wx, wy, wx+30, wy+42, (255, 230, 150) if sunset and (wx+wy) % 3 == 0 else tuple(min(255, v+45) for v in col))
    c.rect(0, 1250, W, 1300, (190, 190, 190)); c.rect(0, 1300, W, H, (85, 88, 95))
    for x in range(20, W, 180): c.rect(x, 1555, x+100, 1570, (240, 240, 240))
    car(c, 20, 1300, (220, 70, 70), (60, 40, 30))
    # bus right
    c.rr(640, 1150, 1140, 1460, 30, (250, 195, 50))
    for wx in (700, 840, 980): c.rr(wx, 1190, wx+110, 1290, 12, (190, 225, 245))
    sleeper_head(c, 760, 1270, 30, hair=(30, 30, 30))
    c.circ(730, 1460, 44, (40, 40, 40)); c.circ(1010, 1460, 44, (40, 40, 40))
    # mailman on sidewalk
    c.rr(470, 1258, 640, 1292, 14, (70, 90, 160)); sleeper_head(c, 455, 1262, 26, hair=(110, 70, 40))
    c.rr(560, 1230, 620, 1270, 6, (160, 110, 70))
    # sleeping dog
    c.el(300, 1255, 400, 1295, (170, 120, 70)); c.circ(300, 1268, 22, (170, 120, 70))
    c.el(282, 1250, 300, 1280, (120, 80, 45)); face_closed(c, 300, 1268, 0.2)
    return c.out(W, H)

def bg_tv():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (170, 200, 180)); c.rect(0, 1480, W, H, (150, 115, 90))
    c.rr(60, 1300, 640, 1480, 16, (120, 80, 60))
    c.rr(70, 860, 650, 1270, 22, (35, 35, 40))
    c.rect(95, 885, 625, 1245, (60, 110, 190))
    c.rect(95, 1100, 625, 1245, (130, 85, 60))
    sleeper_head(c, 360, 1075, 52, hair=(200, 150, 60))
    c.rr(250, 1110, 470, 1150, 20, (190, 60, 80))
    c.rect(95, 900, 330, 950, (220, 40, 40)); c.text((212, 925), "LIVE", 34, (255, 255, 255))
    c.rect(95, 1200, 625, 1245, (240, 240, 240)); c.text((360, 1222), "BREAKING NEWS", 30, (200, 30, 30))
    c.rect(340, 1270, 380, 1300, (35, 35, 40))
    # sofa corner
    c.rr(700, 1330, 1100, 1560, 40, (200, 90, 90))
    return c.out(W, H)

def bg_globe():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (12, 14, 40))
    random.seed(4)
    for _ in range(160): c.circ(random.randint(0, W), random.randint(0, H), random.choice([2, 2, 3, 4]), (255, 255, 240))
    c.circ(540, 1000, 345, (60, 120, 230))
    land = Cv(W, H, S);
    for (x, y, rx, ry) in [(420, 820, 140, 100), (600, 960, 120, 170), (380, 1110, 90, 130), (720, 1180, 120, 80), (520, 720, 90, 50), (300, 950, 60, 90)]:
        land.el(x-rx, y-ry, x+rx, y+ry, (90, 190, 110))
    mask = Image.new("L", c.im.size, 0); ImageDraw.Draw(mask).ellipse([(540-345)*S, (1000-345)*S, (540+345)*S, (1000+345)*S], fill=255)
    lm = Image.composite(land.im, Image.new("RGBA", c.im.size, (0, 0, 0, 0)), mask)
    c.im.paste(lm, (0, 0), lm)
    d = ImageDraw.Draw(c.im)
    d.arc([(540-345)*S, (1000-345)*S, (540+345)*S, (1000+345)*S], 200, 330, fill=(170, 210, 255), width=6*S)
    return c.out(W, H)

def bg_stairs():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (30, 26, 44))
    c.poly([(0, 0), (260, 300), (260, 1700), (0, H)], (22, 19, 34)); c.poly([(W, 0), (820, 300), (820, 1700), (W, H)], (22, 19, 34))
    # doorway glow at bottom
    c.rect(400, 640, 680, 1050, (70, 60, 50)); c.rect(420, 660, 660, 1050, (110, 95, 70))
    for i in range(9):
        y0 = 1050 + i*75; k = i/8
        x0 = 400 - k*330; x1 = 680 + k*330
        c.poly([(x0, y0), (x1, y0), (x1+40, y0+75), (x0-40, y0+75)], (58+i*3, 48+i*3, 62+i*3))
        c.rect(x0-40, y0+70, x1+40, y0+75, (20, 18, 28))
    c.rect(840, 900, 860, 1900, (60, 45, 40)); c.line([(860, 900), (1080, 650)], (80, 60, 50), 22)
    return c.out(W, H)

def door_lock():
    c = Cv(W, H, S)
    c.rr(80, 900, 420, 1490, 10, (70, 55, 60)); c.rr(110, 930, 390, 1470, 8, (85, 66, 70))
    c.circ(360, 1210, 14, (200, 180, 120))
    c.rr(300, 1240, 400, 1320, 12, (230, 190, 60)); c.arc(315, 1185, 385, 1265, 180, 360, (200, 200, 210), 14)
    return c.out(W, H)
DOOR = door_lock()

def zzz(fr, x, y, t, sz=40, col=(255, 255, 255)):
    d = ImageDraw.Draw(fr)
    for i in range(3):
        p = ((t*0.6) + i/3) % 1
        d.text((x + p*40 + i*8, y - p*110), "Z", font=font(sz*(0.6+0.6*p)), fill=col + (int(255*(1-p)),),
               anchor="mm", stroke_width=3, stroke_fill=(40, 40, 60, int(255*(1-p))))

def phone(fr, x, y, t, local):
    c = Cv(380, 620, 2)
    c.rr(0, 0, 380, 620, 50, (25, 25, 30)); c.rr(16, 16, 364, 604, 40, (40, 45, 60))
    c.circ(190, 170, 70, (120, 130, 160)); c.text((190, 170), "M", 70, (255, 255, 255))
    c.text((190, 290), "Mom", 52, (255, 255, 255))
    if local < 1.6: c.text((190, 350), "Calling" + "." * (int(local*3) % 4), 34, (190, 200, 220))
    else: c.text((190, 350), "No answer", 38, (255, 90, 90))
    c.circ(190, 500, 50, (230, 60, 60)); c.rr(160, 492, 220, 508, 8, (255, 255, 255))
    im = c.out(380, 620)
    k = min(1, local/0.25); yy = y + (1-k)*200
    fr.alpha_composite(im, (int(x), int(yy)))

