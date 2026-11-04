
# ================= Episode 4: Trust =================
SCENE_OF_LINE = ["recap_a", "recap_b", "garage4", "photo", "garage4b", "blackout", "tower", "hum", "door",
                 "hatch", "hatch", "door2", "msg", "msg", "hide", "poll", "poll"]
CAP_Y = {"recap_a": 1000, "recap_b": 560, "garage4": 520, "photo": 1380, "garage4b": 520, "blackout": 1000, "tower": 1300,
         "hum": 560, "door": 520, "hatch": 520, "door2": 520, "msg": 520, "hide": 520, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
def T(w, n=0): return starts[tok(w, n)]

def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((685, 323), "2", font=font(54), fill=(110, 255, 140), anchor="mm")

# ---------- Lena ----------
_lena = {}
def make_lena(expr="neutral", eyes=True, arms="flash_bat", gaze=-1):
    key = (expr, eyes, arms, gaze)
    if key in _lena: return _lena[key]
    im = make_max(expr, eyes, False, arms, gaze)
    a = np.array(im).astype(np.int16)
    def swap(src, dst, tol=46):
        dist = np.abs(a[..., :3] - np.array(src)).sum(-1)
        msk = (dist < tol) & (a[..., 3] > 0)
        a[msk, :3] = dst
    swap((47, 128, 237), (196, 62, 72)); swap((35, 100, 190), (156, 44, 54)); swap((59, 42, 31), (150, 72, 38))
    swap((43, 53, 80), (40, 40, 48))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
    c = Cv(600, 900, 2)
    hair = (150, 72, 38)
    c.rr(128, 200, 178, 470, 25, hair); c.rr(422, 200, 472, 470, 25, hair)
    c.el(440, 120, 560, 230, hair); c.rr(500, 180, 560, 420, 30, hair)
    for ex, s_ in ((245, -1), (355, 1)):
        c.line([(ex + s_*26, 262), (ex + s_*40, 250)], (40, 30, 30), 5)
    ov = c.out(600, 900); im.alpha_composite(ov)
    _lena[key] = im
    return im

_ls = {}
def put_lena(fr, x, feet, scale, expr, t, night_k=None, eyes=None, arms="flash_bat", gaze=-1, tremble=0.0):
    if eyes is None: eyes = not ((t % 3.1) < 0.12)
    key = (expr, eyes, round(scale, 2), night_k, arms, gaze)
    if key not in _ls:
        im = make_lena(expr, eyes, arms, gaze)
        if night_k: im = night(im, night_k)
        _ls[key] = im.resize((int(600*scale), int(900*scale)), Image.LANCZOS)
    sp = _ls[key]
    by = math.sin(t*2*math.pi*0.4)*4*scale
    x += math.sin(t*37)*3*tremble
    fr.alpha_composite(sp, (int(x - sp.width/2), int(feet - sp.height + by)))
    return sp

def previously(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([340, 400, 740, 470], 35, fill=(255, 255, 255, 220))
    d.text((540, 435), "PREVIOUSLY", font=font(40), fill=(20, 18, 32), anchor="mm")

# ---------- garage (lit by Lena's phone) ----------
def bg_garage():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (44, 46, 52)); c.rect(0, 1480, W, H, (64, 64, 68))
    for y in range(500, 1480, 120): c.rect(0, y, W, y + 3, (52, 54, 60))
    c.rect(60, 560, 380, 580, (90, 70, 50)); c.rect(60, 820, 380, 840, (90, 70, 50))
    for x, h_, col in [(80, 120, (150, 60, 50)), (170, 90, (70, 110, 150)), (260, 140, (160, 140, 60))]:
        c.rect(x, 560 - h_, x + 70, 560, col)
    c.rr(80, 700, 200, 820, 10, (120, 120, 130)); c.rr(230, 740, 360, 820, 10, (90, 120, 80))
    c.rr(560, 1180, 1100, 1500, 60, (36, 38, 48)); c.rr(640, 1080, 1000, 1220, 50, (36, 38, 48))
    c.circ(680, 1500, 70, (20, 20, 24)); c.circ(980, 1500, 70, (20, 20, 24))
    c.rect(420, 620, 780, 900, (60, 58, 60))
    c.line([(540, 380), (540, 470)], (30, 30, 30), 4); c.rr(522, 466, 558, 486, 4, (70, 70, 74))   # bulb socket
    return c.out(W, H)

def polaroid(back=False):
    c = Cv(260, 300, 2)
    c.rr(0, 0, 260, 300, 6, (240, 238, 230))
    if not back:
        c.rect(16, 16, 244, 230, (40, 44, 70))
        c.rr(40, 150, 220, 230, 20, (60, 60, 110)); c.rr(40, 120, 110, 160, 20, (220, 220, 230))
        hd = make_max("neutral", False, False, "down", 0).crop((120, 70, 480, 440)).resize((160, 164), Image.LANCZOS)
        c.im.alpha_composite(hd, (110, 160))
    c.circ(130, 12, 12, (220, 40, 50))
    return c.out(260, 300)
POLA = polaroid().rotate(-7, expand=True, resample=Image.BICUBIC)
BEAM = blur_layer(lambda c: c.poly([(606, 1362), (612, 1384), (110, 1560), (150, 950)], (255, 250, 220, 130)), 22)
BULB = blur_layer(lambda c: c.circ(540, 500, 230, (255, 220, 150, 120)), 60)

def garage_base(fr, t, lena_arms, max_arms, max_expr, lena_expr="neutral", pola_on_wall=False, local=1.0, bulb=0.0):
    d = ImageDraw.Draw(fr)
    if pola_on_wall: fr.alpha_composite(POLA, (520, 650))
    if bulb > 0:
        fr.alpha_composite(alpha_q("bulb", BULB, bulb)); d.ellipse([524, 482, 556, 520], fill=(255, int(200 + 55*bulb), int(120 + 100*bulb)))
    else:
        d.ellipse([524, 482, 556, 520], fill=(90, 90, 96))
    put_lena(fr, 760, 1700, 0.85, lena_expr, t, arms=lena_arms)
    if lena_arms == "flash_bat": fr.alpha_composite(alpha_q("beam", BEAM, 0.85))
    put_max(fr, 250, 1720, 0.85, max_expr, max_arms, t, local, gaze=1, tremble=0.3)

def r_recap_a(fr, t, local, li):
    garage_base(fr, t, "flash_bat", "up", "shocked", pola_on_wall=True, local=local)
    fr.alpha_composite(tint((0, 0, 10), 70))
    fr.alpha_composite(VIG["mid"]); previously(fr, t)

def r_recap_b(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(20, 18, 32))
    t_rev = T("trust.")
    rv = ease((t - t_rev)/0.25) if t >= t_rev else 0
    q = ease((t - line_start[1] - 0.1)/1.8)
    for i, (lab, val, col) in enumerate([("TRUST", 75, (60, 200, 110)), ("ESCAPE", 25, (220, 60, 70))]):
        y = 900 + i*260; full = 760*val/100*q
        d.rounded_rectangle([160, y, 920, y+150], 30, fill=(40, 38, 60))
        grey = (150, 150, 165); c_ = tuple(int(grey[j]*(1-rv) + col[j]*rv) for j in range(3))
        if full > 30: d.rounded_rectangle([160, y, 160+full, y+150], 30, fill=c_)
        if rv > 0:
            pop = 1 + 0.25*(1 - rv); a_ = int(255*rv)
            d.text((200, y+75), lab, font=font(70*pop), fill=(255, 255, 255, a_), anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0, a_))
            d.text((890, y+75), f"{val}%", font=font(70*pop), fill=(255, 255, 255, a_), anchor="rm", stroke_width=5, stroke_fill=(0, 0, 0, a_))
        else:
            d.text((540, y+75), "?", font=font(70), fill=(230, 230, 240), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    if 0 <= t - t_rev < 0.2: fr.alpha_composite(tint((255, 255, 255), int(120*(1 - (t - t_rev)/0.2))))
    fr.alpha_composite(VIG["mid"]); previously(fr, t)

def r_garage4(fr, t, local, li):
    t_low = T("lowers"); t_ar = T("around.")
    marms = "up" if t < t_low + 0.2 else "down"
    if t < T("turns") - 0.2: la = "flash_bat"
    else: la = "flash_photo" if t < t_ar else "flash_photo_b"
    garage_base(fr, t, la, marms, "worried" if t > t_low else "shocked", local=local)
    if t >= T("turns") - 0.2: ImageDraw.Draw(fr).rectangle([540, 660, 780, 900], fill=(60, 58, 60))   # empty spot on the board
    fr.alpha_composite(tint((0, 0, 10), 80)); fr.alpha_composite(VIG["mid"])

def r_garage4b(fr, t, local, li):
    garage_base(fr, t, "flash_photo_b", "down", "scared", lena_expr="worried", local=local)
    fr.alpha_composite(tint((0, 0, 10), 80)); fr.alpha_composite(VIG["mid"])
    if t > T("Tonight."):
        a = ease((t - T("Tonight."))/0.3)
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.5*a))

# ---------- photo close-up: back side with the address ----------
HAND = (225, 175, 140)
def r_photo(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(26, 26, 32))
    fr.alpha_composite(alpha_q("pb", BULB, 0.0))
    ang = math.radians(-4 + math.sin(t*1.3)*1.5)
    c = Cv(700, 820, 2)
    c.rr(0, 0, 700, 820, 14, (240, 236, 222))
    ink = (30, 36, 80)
    k = ease((t - line_start[3] - 0.2)/1.6)          # handwriting appears
    lines = ["14 Maple Lane", "Room upstairs.", "He sleeps", "by the window."]
    for i, ln in enumerate(lines):
        c.text((350, 220 + i*120), ln, 66 if i == 0 else 54, ink)
    im = c.out(700, 820)
    # reveal mask for the writing
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rectangle([0, 0, 700, int(140 + 560*k)], fill=255)
    base = Image.new("RGBA", im.size, (0, 0, 0, 0)); c2 = Cv(700, 820, 2); c2.rr(0, 0, 700, 820, 14, (240, 236, 222)); paper = c2.out(700, 820)
    im = Image.composite(im, paper, m)
    im = im.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    x0, y0 = 540 - im.width//2, 920 - im.height//2 + int(math.sin(t*2)*4)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 120)); sh.putalpha(im.split()[3].point(lambda v: v*0.5))
    fr.alpha_composite(sh, (x0 + 18, y0 + 24)); fr.alpha_composite(im, (x0, y0))
    # Lena's fingers holding the photo (bottom corners)
    for hx in (250, 830):
        d.ellipse([hx - 70, 1260, hx + 70, 1420], fill=HAND); d.ellipse([hx - 40, 1230, hx + 20, 1300], fill=(235, 188, 156))
        d.rectangle([hx - 80, 1380, hx + 80, 1560], fill=(196, 62, 72))
    if t > T("handwriting.") - 0.1:
        a = int(255*ease((t - T("handwriting.") + 0.1)/0.4))
        d.text((540, 470), "HIS handwriting", font=font(62), fill=(255, 80, 80, a), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0, a))
    fr.alpha_composite(tint((0, 0, 20), 40)); fr.alpha_composite(VIG["hard"])

# ---------- blackout: garage bulb dies, then the city goes dark ----------
WINDOWS = []
for x0, w, h in [(-20, 220, 330), (200, 180, 420), (380, 230, 300), (600, 200, 380), (790, 300, 280)]:
    for wy in range(1260-h+40, 1220, 90):
        for wx in range(x0+30, x0+w-40, 70): WINDOWS.append((wx, wy))
STREET = bg_street_night().convert("RGBA")
STREET_DARK = STREET.copy(); _dd = ImageDraw.Draw(STREET_DARK)
for wx, wy in WINDOWS: _dd.rectangle([wx, wy, wx+30, wy+40], fill=(22, 24, 40))
_dd.ellipse([150, 450, 290, 590], fill=(60, 58, 60))           # moon behind clouds
STREET_DARK = Image.blend(STREET_DARK, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.35)
WINLIT = Image.new("RGBA", (W, H), (0, 0, 0, 0)); _wl = ImageDraw.Draw(WINLIT)
for wx, wy in WINDOWS: _wl.rectangle([wx, wy, wx+30, wy+40], fill=(255, 214, 140))
LAMPS = [(150, 1180), (520, 1180), (900, 1180)]

def r_blackout(fr, t, local, li):
    t_die = T("dies."); t_city = T("city"); t_blk = T("black.")
    if t < t_city - 0.15:
        fr.alpha_composite(BG["garage4"])
        fl = 1.0 if t < T("light") else (0.0 if t > t_die + 0.15 else (1.0 if math.sin(t*60) > 0.2 else 0.15))
        garage_base(fr, t, "flash_photo_b", "down", "scared" if fl < 1 else "worried", local=local, bulb=fl)
        fr.alpha_composite(tint((0, 0, 10), int(80 + 175*(1 - fl))))
        if fl == 0: ImageDraw.Draw(fr).ellipse([600, 1355, 618, 1373], fill=(255, 255, 230))
        return
    fr.alpha_composite(STREET_DARK)
    # windows switch off in a wave from left to right, then the street lamps
    lit = WINLIT.copy(); a = np.array(lit)
    for wx, wy in WINDOWS:
        off = t_blk - 0.5 + (wx + 50)/1150*0.9
        if t > off: a[wy:wy+41, max(0, wx):wx+31, 3] = 0
    fr.alpha_composite(Image.fromarray(a))
    d = ImageDraw.Draw(fr)
    for k, (lx, ly) in enumerate(LAMPS):
        d.rectangle([lx-5, ly, lx+5, 1300], fill=(30, 30, 36))
        if t < t_blk + 0.4 + k*0.15: d.ellipse([lx-18, ly-18, lx+18, ly+18], fill=(255, 230, 160)); fr.alpha_composite(alpha_q("lamp", LAMPGLOW[k], 0.8))
    fr.alpha_composite(VIG["hard"])
LAMPGLOW = [blur_layer(lambda c, lx=lx, ly=ly: c.circ(lx, ly, 120, (255, 220, 150, 120)), 40) for lx, ly in LAMPS]

# ---------- radio tower glows and hums ----------
def rings(fr, t, cx, cy, col, speed=0.6, n=4, rmax=700):
    d = ImageDraw.Draw(fr)
    for i in range(n):
        p = ((t*speed) + i/n) % 1
        r = 40 + rmax*p; a = int(200*(1 - p))
        d.ellipse([cx-r, cy-r*0.6, cx+r, cy+r*0.6], outline=col + (a,), width=6)

def r_tower(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    t_hum = T("hum.")
    pulse = 0.6 + 0.4*abs(math.sin(t*math.pi*0.9))
    fr.alpha_composite(alpha_q("tg", TOWERGLOW, pulse)); ImageDraw.Draw(fr).ellipse([848, 743, 872, 767], fill=(255, 70, 70))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.25*pulse))
    if t > t_hum - 0.1: rings(fr, t, 860, 755, (255, 70, 70), 0.7, 4, 900*ease((t - t_hum)/1.5) + 100)
    fr.alpha_composite(VIG["hard"])

# ---------- every sleepwalker hums along ----------
def r_hum(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    fr.alpha_composite(alpha_q("tg", TOWERGLOW, 0.7 + 0.3*abs(math.sin(t*math.pi*0.9))))
    d = ImageDraw.Draw(fr)
    sway = math.sin(t*2*math.pi*0.45)     # everybody sways in the same rhythm
    breath = 0.5 + 0.5*math.sin(t*2*math.pi*0.45)
    for x, y, ci, ph in CROWD:
        sc = 0.55 + (y - 1320)/330*0.55
        im = WALK[ci][2].resize((int(200*sc), int(420*sc)), Image.BILINEAR)
        xx = int(x % W) + int(sway*10*sc)
        fr.alpha_composite(im, (xx - im.width//2, int(y - im.height)))
        mx, my = xx, int(y - im.height + 104*sc)          # open humming mouth, same size for all
        r_ = (4 + 4*breath)*sc
        d.ellipse([mx - r_, my - r_*0.8, mx + r_, my + r_*1.2], fill=(40, 10, 16))
    rings(fr, t, 540, 1350, (255, 90, 90), 0.9, 3, 600)
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.3 + 0.25*breath))
    fr.alpha_composite(VIG["mid"])

# ---------- the garage door gets hit ----------
def bg_door():
    c = Cv(W, H, S, mode="RGB")
    c.rect(0, 0, W, H, (40, 42, 48)); c.rect(0, 1600, W, H, (58, 58, 62))
    c.rect(120, 560, 960, 1600, (30, 30, 34))
    for i in range(8):
        y = 580 + i*128; c.rect(140, y, 940, y + 118, (88, 92, 100)); c.rect(140, y + 112, 940, y + 118, (60, 62, 70))
        for x in range(170, 940, 200): c.rect(x, y + 20, x + 160, y + 96, (80, 84, 92))
    c.rect(500, 1540, 580, 1560, (40, 40, 44))         # handle
    return c.out(W, H)
SPOT = blur_layer(lambda c: c.circ(540, 1100, 380, (255, 250, 220, 150)), 80)

def dents(fr, t, hits, bend=0.0):
    d = ImageDraw.Draw(fr)
    for k, th in enumerate(hits):
        if t >= th:
            cx, cy = [(600, 1000), (420, 1180), (640, 1260)][k]; r = 60 + 30*k
            d.ellipse([cx - r, cy - r*0.7, cx + r, cy + r*0.7], fill=(60, 62, 70)); d.arc([cx - r, cy - r*0.7, cx + r, cy + r*0.7], 200, 340, fill=(130, 134, 142), width=6)
    if bend > 0:
        b = int(120*bend)
        d.polygon([(140, 1580), (540, 1580 - b), (940, 1580), (940, 1600), (140, 1600)], fill=(20, 8, 10))

def r_door(fr, t, local, li):
    hits = [T("Bang."), T("Again."), T("Harder.")]
    dents(fr, t, hits)
    fr.alpha_composite(tint((0, 0, 8), 120))
    sx = 540 + math.sin(t*2.3)*60
    fr.alpha_composite(alpha_q("spot", SPOT, 0.4), (int(sx - 540), 0))
    d = ImageDraw.Draw(fr)
    for th in hits:                                    # dust falling after each hit
        if 0 <= t - th < 1.2:
            p = (t - th)/1.2; random.seed(int(th*100))
            for _ in range(26):
                x = random.uniform(150, 930); y = 560 + random.uniform(0, 80) + p*random.uniform(200, 600)
                d.ellipse([x-3, y-3, x+3, y+3], fill=(200, 200, 190, int(200*(1 - p))))
            if t - th < 0.12: fr.alpha_composite(tint((255, 255, 255), 60))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.2 + 0.3*abs(math.sin(t*math.pi))))
    fr.alpha_composite(VIG["hard"])

FINGER = (196, 196, 180)
def r_door2(fr, t, local, li):
    hits = [T("Bang."), T("Again."), T("Harder.")]
    bend = ease((t - T("bends.") + 0.2)/0.8)
    dents(fr, t, hits, bend)
    d = ImageDraw.Draw(fr)
    # red tower light leaking under the bent door
    fr.alpha_composite(alpha_q("leak", LEAK, bend))
    t_f = T("Fingers")
    if t > t_f - 0.1:
        p = ease((t - t_f + 0.1)/1.6)
        for k, fx in enumerate([250, 290, 330, 370, 640, 680, 720, 760, 450, 500]):
            ln = (30 + 70*p)*(0.8 + 0.3*((k*37) % 5)/5)
            base = 1580 - int(120*bend*(1 - abs(fx - 540)/400))
            wig = math.sin(t*6 + k)*4
            d.rounded_rectangle([fx - 12 + wig, base - 4, fx + 12 + wig, base + ln], 12, fill=FINGER)
            d.ellipse([fx - 8 + wig, base + ln - 16, fx + 8 + wig, base + ln - 2], fill=(150, 150, 140))
    fr.alpha_composite(tint((0, 0, 8), 110))
    fr.alpha_composite(alpha_q("spot", SPOT, 0.35), (0, 300))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.35 + 0.3*abs(math.sin(t*math.pi*1.5))))
    fr.alpha_composite(VIG["hard"])
LEAK = blur_layer(lambda c: c.rect(140, 1440, 940, 1620, (255, 40, 40, 150)), 40)

# ---------- the hatch ----------
RUG = (130, 50, 50)
def r_hatch(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    t_k = T("kicks"); t_h = T("hatch."); t_tu = T("tunnel.")
    put_max(fr, 220, 1500, 0.66, "scared" if li == 9 else "shocked", "scared", t, local, gaze=1, tremble=0.4)
    # hatch in the floor
    hx0, hy0, hx1, hy1 = 360, 1560, 720, 1760
    op = ease((t - t_tu + 0.2)/0.7)
    d.rectangle([hx0, hy0, hx1, hy1], fill=(10, 8, 10))
    if op > 0:
        for k in range(5):                       # ladder rungs going down
            y = hy0 + 30 + k*34; d.line([(hx0 + 90, y), (hx1 - 90, y)], fill=(70, 70, 76), width=8)
        d.line([(hx0 + 90, hy0), (hx0 + 90, hy1)], fill=(70, 70, 76), width=8); d.line([(hx1 - 90, hy0), (hx1 - 90, hy1)], fill=(70, 70, 76), width=8)
        if li == 10: fr.alpha_composite(alpha_q("hole", HOLEGLOW, 0.5 + 0.5*abs(math.sin(t*3))))
    # lid: lies flat, then swings up
    lh = int((hy1 - hy0)*(1 - op)); top = hy0 - int(260*op)
    d.polygon([(hx0, hy0 - (hy0 - top)), (hx1, hy0 - (hy0 - top)), (hx1, hy0 + lh), (hx0, hy0 + lh)] if op < 1 else
              [(hx0, top), (hx1, top), (hx1, hy0), (hx0, hy0)], fill=(96, 100, 110))
    for rx in (hx0 + 20, hx1 - 20):
        d.ellipse([rx - 7, top + 13, rx + 7, top + 27], fill=(60, 60, 66))
    d.rectangle([520, top + 40 if op > 0.5 else hy0 + lh//2 - 10, 560, (top + 60) if op > 0.5 else hy0 + lh//2 + 10], fill=(40, 40, 44))
    # rug slides away when Lena kicks it
    rp = ease((t - t_k)/0.5) if t > t_k else 0
    rx = int(340 + 760*rp)
    if rp < 1:
        d.rectangle([rx, 1540, rx + 400, 1780], fill=RUG); d.rectangle([rx + 20, 1560, rx + 380, 1760], outline=(200, 160, 80), width=8)
    lx = 840 - (100 if t_k <= t < t_k + 0.5 else 0)
    put_lena(fr, lx, 1500, 0.66, "angry" if li == 9 else "neutral", t, arms="flash_bat")
    if li == 10: fr.alpha_composite(alpha_q("hb", HBEAM, 0.9))
    fr.alpha_composite(tint((0, 0, 10), 90)); fr.alpha_composite(VIG["mid"])
HOLEGLOW = blur_layer(lambda c: c.rect(380, 1640, 700, 1760, (255, 50, 50, 120)), 30)
HBEAM = blur_layer(lambda c: c.poly([(745, 1150), (760, 1170), (700, 1760), (380, 1700)], (255, 250, 220, 110)), 22)

# ---------- message from mom ----------
def msg_card(t):
    c = Cv(440, 620, 2)
    c.rr(0, 0, 440, 620, 50, (22, 22, 28)); c.rr(14, 14, 426, 606, 40, (240, 240, 246))
    c.rect(14, 60, 426, 150, (230, 230, 238)); c.circ(80, 105, 32, (190, 150, 170)); c.text((80, 105), "M", 34, (255, 255, 255))
    c.text((230, 105), "Mom", 42, (20, 20, 30))
    t1 = line_start[13]; t2 = T("Check")
    for k, (txt, tt_) in enumerate([("Lena is lying.", t1), ("Check her phone.", t2)]):
        if t >= tt_ - 0.1:
            y = 220 + k*130
            c.rr(40, y, 380, y + 100, 34, (225, 225, 232)); c.text((210, y + 50), txt, 34, (20, 20, 30))
    if line_start[12] <= t < t1 - 0.1:
        for i in range(3):
            c.circ(80 + i*36, 260, 12 + 4*abs(math.sin(t*6 + i)), (160, 160, 170))
    return c.out(440, 620)

def r_msg(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(tint((0, 0, 10), 120))
    bz = T("buzzes.")
    shk = math.sin(t*80)*10 if bz - 0.1 <= t < bz + 0.8 else 0
    put_max(fr, 330 + shk*0.3, 2000, 1.25, "shocked" if li == 13 else "worried", "phone_hold", t, local, gaze=1, tremble=0.3)
    fr.alpha_composite(alpha_q("phg", PGLOW, 0.8 + 0.2*math.sin(t*4)))
    k = ease((t - bz + 0.2)/0.4)
    if k > 0:
        card = msg_card(t)
        fr.alpha_composite(alpha_mul(card, k), (int(600 + shk), int(640 + (1 - k)*100)))
    if li == 13 and t > T("lying."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.4 + 0.25*abs(math.sin(t*math.pi*1.6))))
    fr.alpha_composite(VIG["mid"])
PGLOW = blur_layer(lambda c: c.circ(330, 1540, 230, (150, 200, 255, 110)), 60)

# ---------- Lena hides her phone ----------
def r_hide(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 130))
    th = T("hides")
    arms = "flash_bat" if t < th else "bat_hide"
    put_lena(fr, 560, 2050, 1.3, "worried" if t < th else "neutral", t, arms=arms, gaze=-1 if t < th else 1)
    if t >= th:
        fr.alpha_composite(alpha_q("hg", HIDEGLOW, 0.6 + 0.4*abs(math.sin(t*2.2))))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.3)); fr.alpha_composite(VIG["hard"])
HIDEGLOW = blur_layer(lambda c: c.circ(330, 1700, 90, (160, 210, 255, 160)), 40)

# ---------- poll ----------
POLL_BG = None
def r_poll(fr, t, local, li):
    global POLL_BG
    if POLL_BG is None:
        c = Cv(W, H, S)
        c.rect(0, 0, W, H, (20, 18, 32))
        c.rr(40, 720, 528, 1470, 40, (60, 50, 60)); c.rr(552, 720, 1040, 1470, 40, (40, 60, 110))
        c.rect(140, 1080, 430, 1300, (8, 6, 8))
        for k in range(5): c.line([(180, 1100 + k*40), (390, 1100 + k*40)], (80, 80, 86), 8)
        c.rect(140, 900, 430, 1080, (96, 100, 110))
        c.rr(690, 820, 900, 1240, 26, (22, 22, 28)); c.rr(704, 840, 886, 1220, 16, (150, 200, 255))
        c.text((795, 1030), "?", 120, (255, 255, 255))
        POLL_BG = c.out(W, H)
    fr.alpha_composite(POLL_BG)
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(alpha_q("pgl", POLLGLOW, 0.5 + 0.5*abs(math.sin(t*3))))
    put_max(fr, 400, 1330, 0.4, "scared", "scared", t, 1, gaze=-1, tremble=0.4)
    put_lena(fr, 960, 1330, 0.42, "neutral", t, arms="bat_hide")
    hl = None
    if line_start[15] <= t < T("Or") or T("Tunnel,") - 0.1 <= t < T("Phone?"): hl = 0
    elif T("Or") <= t < T("Vote") or t >= T("Phone?"): hl = 1
    if hl is not None:
        x0 = 40 if hl == 0 else 552
        d.rounded_rectangle([x0-6, 714, x0+494, 1476], 44, outline=(255, 230, 80), width=10)
    p = 1 + 0.06*math.sin(t*5)
    d.text((284, 1400), "TUNNEL", font=font(86*p), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((796, 1400), "PHONE", font=font(86*(2-p)), fill=(255, 230, 80), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.ellipse([480, 1040, 600, 1160], fill=(255, 255, 255)); d.text((540, 1100), "VS", font=font(56), fill=(20, 18, 32), anchor="mm")
    k = ease(local/0.4)
    d.rounded_rectangle([110, 405, 970, 495], 45, fill=(230, 40, 60))
    d.text((540, 451), "VOTE IN THE COMMENTS", font=font(int(58*(0.75+0.25*k))), fill=(255, 255, 255), anchor="mm")
POLLGLOW = blur_layer(lambda c: c.rect(150, 1120, 420, 1300, (255, 50, 50, 140)), 30)

print("ep4 backgrounds")
GAR = bg_garage().convert("RGBA")
BLK = Image.new("RGBA", (W, H), (0, 0, 0, 255))
BG = {"recap_a": GAR, "recap_b": BLK, "garage4": GAR, "photo": BLK, "garage4b": GAR, "blackout": BLK,
      "tower": BLK, "hum": BLK, "door": bg_door().convert("RGBA"), "hatch": GAR, "msg": GAR, "hide": GAR, "poll": BLK}
BG["door2"] = BG["door"]
R = {"recap_a": r_recap_a, "recap_b": r_recap_b, "garage4": r_garage4, "photo": r_photo, "garage4b": r_garage4b,
     "blackout": r_blackout, "tower": r_tower, "hum": r_hum, "door": r_door, "door2": r_door2, "hatch": r_hatch,
     "msg": r_msg, "hide": r_hide, "poll": r_poll}
CAM = {"recap_a": (1.0, 1.0, 540, 960), "recap_b": (1.0, 1.0, 540, 960), "garage4": (1.0, 1.15, 600, 1250),
       "photo": (1.0, 1.12, 540, 920), "garage4b": (1.25, 1.45, 760, 1150), "blackout": (1.0, 1.0, 540, 1100),
       "tower": (1.0, 1.7, 860, 820), "hum": (1.0, 1.2, 540, 1350), "door": (1.0, 1.15, 540, 1100),
       "door2": (1.15, 1.5, 540, 1450), "hatch": (1.0, 1.2, 540, 1500), "msg": (1.0, 1.1, 640, 1100),
       "hide": (1.0, 1.35, 540, 1300), "poll": (1.0, 1.0, 540, 960)}
TRANS = {"recap_b": ("flash", 0.3), "garage4": ("fade", 0.4), "photo": ("fade", 0.3), "garage4b": ("fade", 0.3),
         "tower": ("fade", 0.4), "hum": ("slide", 0.35), "door": ("black", 0.4), "hatch": ("fade", 0.3),
         "door2": ("fade", 0.25), "msg": ("black", 0.4), "hide": ("fade", 0.4), "poll": ("flash", 0.4)}

def render_scene(name, t):
    li = cur_line(t)
    if SCENE_OF_LINE[li] != name:
        li = max(k for k in range(len(SCRIPT)) if SCENE_OF_LINE[k] == name)
    local = t - scene_start(name)
    fr = BG[name].copy()
    R[name](fr, t, local, li)
    z0, z1, fx, fy = CAM[name]
    z = z0 + (z1 - z0)*ease(local/scene_len(name))
    shx = shy = 0
    shakes = [(T("Bang."), 14), (T("Again."), 18), (T("Harder."), 26), (T("bends."), 20), (T("black."), 8), (T("buzzes."), 4)]
    for th, amp in shakes:
        if 0 <= t - th < 0.35: a = (1 - (t - th)/0.35)*amp; shx += math.sin(t*90)*a; shy += math.cos(t*70)*a
    if z > 1.001 or shx or shy:
        z = max(z, 1.03)
        w, h = W/z, H/z
        x0 = min(max(fx - w/2, 0), W - w) + shx; y0 = min(max(fy - h/2, 0), H - h) + shy
        fr = fr.transform((W, H), Image.EXTENT, (x0, y0, x0+w, y0+h), Image.BILINEAR)
    return fr

# ---------- sound ----------
SR = 44100
def make_ambient():
    n = int(TOTAL*SR); a = np.zeros(n); tt = np.arange(n)/SR
    def env(t0, t1, att=1.5, rel=1.5): return np.clip((tt-t0)/att, 0, 1)*np.clip((t1-tt)/rel, 0, 1)
    def pad(freqs, t0, t1, amp, att=1.5, rel=1.5, trem=0.0, vib=0.0):
        e = env(t0, t1, att, rel); m = e > 0; s = np.zeros(n)
        for f in freqs:
            ph = 2*np.pi*f*tt[m] + 0.3*np.sin(2*np.pi*0.2*tt[m]) + vib*np.sin(2*np.pi*(4.6 + f % 1)*tt[m])
            s[m] += np.sin(ph) + 0.3*np.sin(2.003*ph)
        if trem: s *= 1 - trem*(0.5 + 0.5*np.sin(2*np.pi*3*tt))
        a[:] += s*e*amp/len(freqs)
    def hit(t0, f, dec, amp, noise=0.0):
        i0 = int(t0*SR); i1 = min(n, i0 + int(dec*5*SR))
        if i0 >= n or i0 < 0: return
        x = np.arange(i1 - i0)/SR; e = np.exp(-x/dec); s = np.sin(2*np.pi*f*x*(1 + 0.5*np.exp(-x/0.03)))
        if noise: nz = np.convolve(np.random.randn(len(x)), np.ones(40)/40, "same"); s += noise*nz*4
        a[i0:i1] += s*e*amp
    def click(t0, amp, ln=300):
        i0 = int(t0*SR)
        if 0 <= i0 and i0 + ln < n: a[i0:i0+ln] += np.random.randn(ln)*np.exp(-np.arange(ln)/(ln/6))*amp
    def sweep(t0, d_, f0, f1, amp, noise=0.0):
        i0 = int(t0*SR); L = int(d_*SR)
        if i0 + L >= n: return
        x = np.arange(L)/SR; f = f0 + (f1 - f0)*x/d_; s = np.sin(2*np.pi*np.cumsum(f)/SR)
        if noise: s += noise*np.convolve(np.random.randn(L), np.ones(30)/30, "same")*4
        a[i0:i0+L] += s*amp*np.minimum(1, x/0.03)*np.minimum(1, (d_ - x)/0.1)
    def buzz(t0):
        for k in range(2):
            i0 = int((t0 + k*0.35)*SR); L = int(0.25*SR)
            if i0 + L < n:
                x = np.arange(L)/SR; a[i0:i0+L] += np.sign(np.sin(2*np.pi*150*x))*0.05*np.sin(np.pi*x/0.25)
    ls = line_start
    pad([55.0, 58.3], 0, ls[1] + 0.3, 0.09, 0.4, 0.5)
    hit(T("trust.") - 0.03, 48, 0.8, 0.35, noise=0.15)
    pad([110.0, 164.8, 138.6], ls[1], ls[2] + 0.4, 0.05, 0.3, 0.6)
    pad([73.4, 110.0], ls[2] - 0.2, ls[5] + 0.5, 0.07, 0.8, 0.8)
    click(T("turns"), 0.06, 1200); sweep(T("around."), 0.25, 3000, 1500, 0.02, noise=0.4)
    hit(T("handwriting.") - 0.05, 52, 0.9, 0.35, noise=0.1)
    hit(T("Tonight."), 45, 0.9, 0.4, noise=0.2)
    for k in np.arange(T("light"), T("dies.") + 0.15, 0.05): click(k, 0.05, 200)       # flicker buzz
    sweep(T("dies.") + 0.1, 0.9, 140, 30, 0.12)
    hit(T("black.") - 0.03, 38, 1.4, 0.6, noise=0.3)
    for k, wx in enumerate(range(0, 900, 150)): click(T("black.") - 0.4 + k*0.15, 0.08, 400)   # breakers clicking off
    hum0 = T("hum.") - 0.3
    pad([98.0, 196.0], hum0, ls[15], 0.07, 1.2, 1.0, vib=0.8)
    pad([98.0, 147.0, 196.0, 98.6, 146.2], ls[7] - 0.2, ls[15], 0.09, 1.0, 1.0, vib=1.6)
    pad([98.0, 147.0], ls[15], TOTAL, 0.05, 0.5, 1.2, vib=1.2)
    for k, w_ in enumerate(("Bang.", "Again.", "Harder.")):
        th = T(w_) - 0.03; amp = 0.6 + 0.2*k
        hit(th, 55, 0.22, amp, noise=0.5); hit(th, 310, 0.08, 0.15, noise=0.6)
        for r_ in range(6): click(th + 0.1 + r_*0.06, 0.08*(1 - r_/6), 700)            # metal rattle
    sweep(T("kicks"), 0.5, 200, 120, 0.03, noise=0.8)
    hit(T("hatch.") - 0.05, 220, 0.25, 0.25, noise=0.3)
    sweep(T("tunnel.") - 0.1, 0.9, 420, 260, 0.05, noise=0.2)
    pad([41.2, 43.7], ls[10], ls[11] + 0.3, 0.12, 0.4, 0.4, trem=0.4)
    sweep(T("bends.") - 0.1, 1.0, 70, 45, 0.25, noise=0.5)
    for k in np.arange(T("Fingers"), T("Fingers") + 1.6, 0.09): click(k, 0.03, 1500)    # scraping
    buzz(T("buzzes.") - 0.05)
    hit(ls[13] - 0.05, 1320, 0.15, 0.06); hit(T("Check") - 0.05, 1320, 0.15, 0.06)
    hb = ls[13]; per = 0.7
    while hb < ls[15]:
        hit(hb, 45, 0.08, 0.4); hit(hb + 0.18, 42, 0.08, 0.28); per = max(0.42, per*0.95); hb += per
    hit(T("hides"), 40, 1.0, 0.4, noise=0.15)
    pad([55.0, 82.4], ls[15] - 0.2, TOTAL, 0.08, 0.5, 1.0)
    return a
voice_raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", "voice.mp3", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
voice = np.frombuffer(voice_raw, np.int16).astype(float)/32768
amb = make_ambient()
mix = amb.copy(); mix[:len(voice)] += voice[:len(mix)]
mix = mix/max(1.0, np.abs(mix).max()*1.02)
import wave
with wave.open("mix.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((mix*32767).astype(np.int16).tobytes())
