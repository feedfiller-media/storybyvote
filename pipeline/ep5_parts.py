
# ================= Episode 5: Phone =================
SCENE_OF_LINE = ["hook", "recap_a", "recap_b", "grab", "grab", "gallery", "gallery", "gallery", "hatch5", "hatch5",
                 "two", "newphoto", "newphoto", "quiet", "hole", "own", "poll", "poll"]
CAP_Y = {"hook": 560, "recap_a": 520, "recap_b": 560, "grab": 520, "gallery": 440, "hatch5": 520, "two": 520,
         "newphoto": 440, "quiet": 560, "hole": 520, "own": 470, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
TOTAL = dur + 2.4
COVER_T = TOTAL - 1.0
PART = 5
def TL(w):
    ks = [k for k, t_ in enumerate(tokens) if t_[0] == w]; return starts[ks[-1]]

def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    tv = T("voice.")
    if t >= tv and (t - tv) % 0.5 < 0.25:
        d.text((685, 323), "3?", font=font(60), fill=(255, 70, 70), anchor="mm")
    else:
        d.text((685, 323), "2", font=font(54), fill=(110, 255, 140), anchor="mm")

# ---------- hook: the sleeping world, two kids awake ----------
def r_hook(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    fr.alpha_composite(alpha_q("tg", TOWERGLOW, 0.7 + 0.3*abs(math.sin(t*math.pi*0.9))))
    sway = math.sin(t*2*math.pi*0.45)
    for x, y, ci, ph in CROWD:
        sc = 0.55 + (y - 1320)/330*0.55
        im = WALK[ci][2].resize((int(200*sc), int(420*sc)), Image.BILINEAR)
        xx = int(x % W) + int(sway*10*sc)
        fr.alpha_composite(im, (xx - im.width//2, int(y - im.height)))
    if t > T("kids.") - 0.2:
        k = ease((t - T("kids.") + 0.2)/0.5)
        fr.alpha_composite(tint((0, 0, 0), int(110*k)))
        fr.alpha_composite(alpha_q("spot2", SPOT2, k))
        put_max(fr, 430, 1640, 0.42, "scared", "down", t, 1, gaze=1)
        put_lena(fr, 650, 1640, 0.42, "worried", t, arms="flash_bat")
    fr.alpha_composite(VIG["mid"])
SPOT2 = blur_layer(lambda c: c.el(300, 1150, 780, 1720, (255, 250, 220, 120)), 60)

# ---------- recap A: the message from mom ----------
def mom_card(n_bubbles, t):
    c = Cv(440, 620, 2)
    c.rr(0, 0, 440, 620, 50, (22, 22, 28)); c.rr(14, 14, 426, 606, 40, (240, 240, 246))
    c.rect(14, 60, 426, 150, (230, 230, 238)); c.circ(80, 105, 32, (190, 150, 170)); c.text((80, 105), "M", 34, (255, 255, 255))
    c.text((230, 105), "Mom", 42, (20, 20, 30))
    for k, txt in enumerate(["Lena is lying.", "Check her phone."][:n_bubbles]):
        y = 220 + k*130
        c.rr(40, y, 380, y + 100, 34, (225, 225, 232)); c.text((210, y + 50), txt, 34, (20, 20, 30))
    return c.out(440, 620)

def r_recap_a(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 120))
    put_max(fr, 330, 2000, 1.25, "shocked", "phone_hold", t, local, gaze=1, tremble=0.3)
    fr.alpha_composite(alpha_q("phg", PGLOW, 0.8 + 0.2*math.sin(t*4)))
    nb = 2 if t > T("Check") - 0.1 else 1
    fr.alpha_composite(mom_card(nb, t), (600, 660))
    fr.alpha_composite(VIG["mid"]); previously(fr, t)

def r_recap_b(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(20, 18, 32))
    t_rev = starts[tok("phone.", 1)]
    rv = ease((t - t_rev)/0.25) if t >= t_rev else 0
    q = ease((t - line_start[2] - 0.1)/1.8)
    for i, (lab, val, col) in enumerate([("TUNNEL", 27, (220, 60, 70)), ("PHONE", 73, (60, 200, 110))]):
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

# ---------- Max grabs the phone ----------
def r_grab(fr, t, local, li):
    tg = T("grabs")
    got = t >= tg + 0.25
    d = ImageDraw.Draw(fr)
    d.ellipse([524, 482, 556, 520], fill=(90, 90, 96))
    lx = 760 - (0 if got else 0)
    put_lena(fr, lx, 1700, 0.85, "worried" if got else "angry", t, arms="bat_hide" if got else "flash_bat", gaze=-1)
    mx = 250 + (120*ease((t - tg)/0.25) if tg <= t < tg + 0.25 else 0)
    put_max(fr, mx, 1720, 0.85, "angry" if not got else "worried", "phone_hold" if got else "reach", t, local, gaze=1, tremble=0.2)
    if got: fr.alpha_composite(alpha_q("pg2", PGLOW2, 0.85))
    else: fr.alpha_composite(alpha_q("beam", BEAM, 0.85))
    fr.alpha_composite(tint((0, 0, 10), 110))
    if li == 4 and t > T("whispers:"):
        a = int(255*ease((t - T("whispers:"))/0.4))
        d = ImageDraw.Draw(fr)
        d.rounded_rectangle([560, 1120, 1020, 1210], 40, fill=(255, 120, 120, int(a*0.85)))
        d.text((790, 1165), "Lena (whispering)", font=font(36), fill=(60, 10, 10, a), anchor="mm")
    fr.alpha_composite(VIG["mid"])
PGLOW2 = blur_layer(lambda c: c.circ(250, 1340, 200, (150, 200, 255, 110)), 50)

# ---------- phone screen helpers ----------
def sleeper_thumb(seed, w=200, h=200):
    c = Cv(w, h, 2)
    random.seed(seed)
    c.rect(0, 0, w, h, (30 + random.randint(0, 15), 34, 60 + random.randint(0, 20)))
    c.rr(int(w*0.1), int(h*0.55), int(w*0.95), int(h*0.95), 14, (60, 60, 110))
    c.rr(int(w*0.08), int(h*0.42), int(w*0.4), int(h*0.62), 14, (210, 210, 225))
    hd = HEAD.resize((int(w*0.42), int(h*0.43)))
    c.im.alpha_composite(hd, (int(w*0.32), int(h*0.38)))
    return c.out(w, h)
HEAD = make_max("neutral", False, False, "down", 0).crop((120, 70, 480, 440)).resize((180, 184), Image.LANCZOS)
THUMBS = [sleeper_thumb(s) for s in range(12)]

def phone_frame(fr, screen, t):
    """big phone held in Max's hand; screen is a 640x1140 RGBA image"""
    d = ImageDraw.Draw(fr)
    x0, y0 = 200, 580
    d.rounded_rectangle([x0, y0, x0 + 680, y0 + 1180], 60, fill=(18, 18, 22))
    fr.alpha_composite(screen, (x0 + 20, y0 + 20))
    d.rounded_rectangle([x0 + 270, y0 + 30, x0 + 410, y0 + 56], 13, fill=(18, 18, 22))
    # hand: fingers on the left side, thumb on the right, sleeve at the bottom
    for k in range(3): d.ellipse([x0 - 40, y0 + 560 + k*110, x0 + 30, y0 + 650 + k*110], fill=SKIN)
    d.ellipse([x0 + 600, y0 + 820, x0 + 720, y0 + 960], fill=SKIN)
    d.rounded_rectangle([x0 + 560, y0 + 900, x0 + 760, H], 60, fill=HOOD)

def r_gallery(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 200))
    scr = Image.new("RGBA", (640, 1140), (250, 250, 252, 255)); d = ImageDraw.Draw(scr)
    d.text((40, 70), "Photos", font=font(56), fill=(20, 20, 30), anchor="lm")
    t_new = T("newest")
    if t < t_new:
        k = ease((t - line_start[5])/0.5)
        scroll = 0 if li == 5 else (t - line_start[6])*260
        for i in range(30):
            r_, c_ = divmod(i, 3)
            y = 140 + r_*212 - int(scroll) % 1272
            if -220 < y < 1140:
                scr.alpha_composite(alpha_mul(THUMBS[i % 12], k), (10 + c_*210, y))
        if li == 6:
            d.rounded_rectangle([140, 1040, 500, 1110], 35, fill=(20, 20, 30))
            n_ = min(347, int((t - line_start[6])*120) + 12)
            d.text((320, 1075), f"{n_} photos of Max", font=font(32), fill=(255, 255, 255), anchor="mm")
    else:
        k = ease((t - t_new)/0.35)
        ph = PHOTO_BEHIND.resize((int(200 + 440*k), int(200 + 700*k)))
        scr.alpha_composite(ph, (int(10 + (320 - 100 - 220*k) - 10), int(140 + 80*k)))
        if t > T("ago.") - 0.1:
            d.rounded_rectangle([170, 1040, 470, 1105], 32, fill=(220, 40, 50))
            d.text((320, 1072), "3 min ago", font=font(34), fill=(255, 255, 255), anchor="mm")
    phone_frame(fr, scr, t)
    if li == 7 and t > T("behind."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.5 + 0.3*abs(math.sin(t*math.pi*2))))
    fr.alpha_composite(VIG["mid"])

def photo_behind():
    c = Cv(640, 900, 2)
    c.rect(0, 0, 640, 900, (22, 40, 26))
    c.rect(0, 640, 640, 900, (30, 52, 34)); c.rect(40, 200, 260, 214, (40, 70, 44))
    # Max from behind: hoodie, brown hair, hood
    c.rr(120, 470, 300, 720, 60, (40, 90, 160)); c.el(150, 440, 270, 500, (30, 70, 130))
    c.el(140, 300, 280, 460, (59, 42, 31))
    # Lena from behind: red hoodie, auburn hair, ponytail
    c.rr(360, 470, 540, 720, 60, (150, 50, 60)); c.el(380, 290, 520, 450, (150, 72, 38)); c.rr(430, 400, 470, 560, 18, (150, 72, 38))
    im = c.out(640, 900)
    a = np.array(im).astype(float); a[..., 0] *= 0.55; a[..., 1] = np.minimum(255, a[..., 1]*1.25 + 20); a[..., 2] *= 0.55
    im = Image.fromarray(a.astype(np.uint8), "RGBA")
    dd = ImageDraw.Draw(im); dd.text((30, 40), "REC", font=font(34), fill=(255, 60, 60)); dd.ellipse([110, 50, 128, 68], fill=(255, 60, 60))
    return im
PHOTO_BEHIND = photo_behind()

# ---------- the open hatch, something climbing ----------
def draw_open_hatch(fr, t, eyes=0.0, fingers=0.0):
    d = ImageDraw.Draw(fr)
    hx0, hy0, hx1, hy1 = 360, 1560, 720, 1760
    d.rectangle([hx0, hy0, hx1, hy1], fill=(10, 8, 10))
    fr.alpha_composite(alpha_q("hole", HOLEGLOW, 0.5 + 0.5*abs(math.sin(t*3))))
    for k in range(5):
        y = hy0 + 30 + k*34; d.line([(hx0 + 90, y), (hx1 - 90, y)], fill=(70, 70, 76), width=8)
    d.line([(hx0 + 90, hy0), (hx0 + 90, hy1)], fill=(70, 70, 76), width=8); d.line([(hx1 - 90, hy0), (hx1 - 90, hy1)], fill=(70, 70, 76), width=8)
    top = hy0 - 260
    d.polygon([(hx0, top), (hx1, top), (hx1, hy0), (hx0, hy0)], fill=(96, 100, 110))
    for rx in (hx0 + 20, hx1 - 20): d.ellipse([rx - 7, top + 13, rx + 7, top + 27], fill=(60, 60, 66))
    d.rectangle([520, top + 40, 560, top + 60], fill=(40, 40, 44))
    if eyes > 0:
        a = int(255*eyes)
        for ex in (505, 575): d.ellipse([ex - 16, 1690 - 9, ex + 16, 1690 + 9], fill=(255, 255, 230, a)); d.ellipse([ex - 5, 1684, ex + 5, 1696], fill=(10, 10, 10, a))
    if fingers > 0:
        for k, fx in enumerate([420, 450, 480, 600, 630, 660]):
            ln = 50*fingers; wig = math.sin(t*5 + k)*3
            d.rounded_rectangle([fx - 11, hy0 - 6, fx + 11, hy0 + ln], 11, fill=FINGER)
            d.ellipse([fx - 7 + wig, hy0 - 4, fx + 7 + wig, hy0 + 10], fill=(150, 150, 140))

def r_hatch5(fr, t, local, li):
    put_max(fr, 220, 1500, 0.66, "shocked" if li == 9 else "scared", "phone_hold", t, local, gaze=1, tremble=0.5)
    put_lena(fr, 840, 1500, 0.66, "scared" if li == 9 else "worried", t, arms="bat_hide", gaze=-1, tremble=0.4)
    tc = T("climbing")
    draw_open_hatch(fr, t, eyes=ease((t - tc)/0.6) if t > tc else 0, fingers=ease((t - tc - 0.6)/1.0) if t > tc + 0.6 else 0)
    fr.alpha_composite(tint((0, 0, 10), 90))
    if li == 9: fr.alpha_composite(alpha_q("red", VIG["red"], 0.3 + 0.3*abs(math.sin(t*math.pi*1.4))))
    fr.alpha_composite(VIG["mid"])

# ---------- Lena explains ----------
def r_two(fr, t, local, li):
    put_max(fr, 330, 1900, 1.05, "worried", "phone_hold", t, local, gaze=1, tremble=0.3)
    put_lena(fr, 790, 1900, 1.05, "worried", t, arms="bat_hide", gaze=-1)
    d = ImageDraw.Draw(fr)
    d.ellipse([555, 1360, 625, 1430], fill=SKIN)                      # her hand on his arm
    fr.alpha_composite(alpha_q("pg2", PGLOW2, 0.6), (80, 300))
    fr.alpha_composite(tint((0, 0, 10), 110)); fr.alpha_composite(VIG["mid"])

# ---------- new photo arrives: taken from inside the tunnel ----------
def photo_from_tunnel():
    c = Cv(600, 900, 2)
    c.rect(0, 0, 600, 900, (6, 6, 8))
    c.rect(170, 40, 430, 250, (70, 72, 80))                 # opening of the hatch above
    c.line([(40, 900), (200, 250)], (60, 60, 66), 16); c.line([(560, 900), (400, 250)], (60, 60, 66), 16)
    for k in range(6):
        y = 860 - k*110; f = (900 - y)/650
        c.line([(40 + 160*f, y), (560 - 160*f, y)], (60, 60, 66), 12)
    hd = make_max("shocked", True, False, "down", 0).crop((120, 70, 480, 440)).resize((500, 512), Image.LANCZOS)
    c.im.alpha_composite(hd, (350, 60))
    c.rr(330, 180, 380, 250, 8, (150, 200, 255)); c.circ(355, 255, 22, SKIN)
    im = c.out(600, 900)
    a = np.array(im).astype(float); a[..., 0] *= 0.6; a[..., 1] = np.minimum(255, a[..., 1]*1.2 + 15); a[..., 2] *= 0.6
    im = Image.fromarray(a.astype(np.uint8), "RGBA")
    ImageDraw.Draw(im).text((20, 840), "NOW", font=font(40), fill=(255, 60, 60))
    return im
PHOTO_TUNNEL = photo_from_tunnel()

def r_newphoto(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 200))
    tv = T("vibrates"); ta = T("arrives.")
    scr = Image.new("RGBA", (640, 1140), (250, 250, 252, 255)); d = ImageDraw.Draw(scr)
    d.text((40, 70), "Photos", font=font(56), fill=(20, 20, 30), anchor="lm")
    for i in range(12):
        r_, c_ = divmod(i, 3); scr.alpha_composite(THUMBS[i], (10 + c_*210, 140 + r_*212))
    if t > tv - 0.1:
        k = ease((t - tv + 0.1)/0.3)
        d.rounded_rectangle([20, int(-100 + 150*k), 620, int(-100 + 150*k) + 110], 30, fill=(40, 40, 50))
        d.text((320, int(-100 + 150*k) + 55), "Unknown: sent a photo", font=font(34), fill=(255, 255, 255), anchor="mm")
    if li == 12:
        k = ease((t - line_start[12])/0.35)
        ph = PHOTO_TUNNEL.resize((int(200 + 400*k), int(300 + 600*k)))
        scr.alpha_composite(ph, (320 - ph.width//2, 140 + int(60*k)))
    shk = math.sin(t*80)*10 if tv - 0.1 <= t < tv + 0.9 else 0
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    phone_frame(tmp, scr, t)
    fr.alpha_composite(tmp, (int(shk), 0))
    if li == 12 and t > T("tunnel."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.5 + 0.3*abs(math.sin(t*math.pi*2))))
    fr.alpha_composite(VIG["mid"])

# ---------- the humming stops ----------
def r_quiet(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    ts = T("stops.")
    on = t < ts
    if on: fr.alpha_composite(alpha_q("tg", TOWERGLOW, 0.8))
    d = ImageDraw.Draw(fr)
    sway = math.sin(t*2*math.pi*0.45) if on else 0
    for x, y, ci, ph in CROWD:
        sc = 0.55 + (y - 1320)/330*0.55
        im = WALK[ci][2].resize((int(200*sc), int(420*sc)), Image.BILINEAR)
        xx = int(x % W) + int(sway*10*sc)
        fr.alpha_composite(im, (xx - im.width//2, int(y - im.height)))
        if on:
            mx, my = xx, int(y - im.height + 104*sc); r_ = 6*sc
            d.ellipse([mx - r_, my - r_*0.8, mx + r_, my + r_*1.2], fill=(40, 10, 16))
    if on: rings(fr, t, 540, 1350, (255, 90, 90), 0.9, 3, 600)
    else: fr.alpha_composite(tint((0, 0, 0), int(80*ease((t - ts)/0.5))))
    fr.alpha_composite(VIG["hard"])

# ---------- the voice from the hatch ----------
def r_hole(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(40, 42, 48))
    d.rectangle([140, 640, 940, 1560], fill=(6, 5, 7))
    fr.alpha_composite(alpha_q("hg5", HOLEGLOW5, 0.4 + 0.4*abs(math.sin(t*2))))
    for k in range(7):
        y = 700 + k*120; f = k/7
        d.line([(330 + 40*f, y), (750 - 40*f, y)], fill=(54, 54, 60), width=14)
    d.line([(330, 640), (370, 1560)], fill=(54, 54, 60), width=14); d.line([(750, 640), (710, 1560)], fill=(54, 54, 60), width=14)
    d.rectangle([120, 620, 960, 660], fill=(96, 100, 110)); d.rectangle([120, 620, 160, 1580], fill=(96, 100, 110)); d.rectangle([920, 620, 960, 1580], fill=(96, 100, 110))
    tm = TL("Max.")
    if t > tm - 0.2:
        a = ease((t - tm + 0.2)/0.5)
        for ex in (480, 600):
            d.ellipse([ex - 26, 1300 - 14, ex + 26, 1300 + 14], fill=(int(250*a), int(250*a), int(230*a)))
            d.ellipse([ex - 8, 1292, ex + 8, 1308], fill=(10, 10, 10))
    fr.alpha_composite(tint((0, 0, 10), 60)); fr.alpha_composite(VIG["hard"])
HOLEGLOW5 = blur_layer(lambda c: c.rect(200, 1200, 880, 1560, (255, 40, 40, 110)), 60)

def r_own(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 160))
    put_max(fr, 540, 2600, 2.1, "shocked", "phone_hold", t, local, gaze=0, tremble=0.6)
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.45 + 0.35*abs(math.sin(t*math.pi*1.6))))
    fr.alpha_composite(VIG["hard"])

# ---------- poll ----------
POLL_BG = None
def r_poll(fr, t, local, li):
    global POLL_BG
    if POLL_BG is None:
        c = Cv(W, H, S)
        c.rect(0, 0, W, H, (20, 18, 32))
        c.rr(40, 720, 528, 1470, 40, (60, 50, 60)); c.rr(552, 720, 1040, 1470, 40, (40, 30, 40))
        c.rect(120, 1000, 450, 1240, (96, 100, 110))                          # SLAM: closed hatch
        for rx in (140, 430): c.circ(rx, 1020, 8, (60, 60, 66))
        c.rect(260, 1110, 310, 1130, (40, 40, 44))
        for k in range(3): c.line([(130 + k*100, 880), (150 + k*100, 960)], (255, 255, 255), 8)
        c.rect(632, 960, 960, 1260, (6, 5, 7))                                # LOOK: open hole with eyes
        for k in range(4): c.line([(700, 1000 + k*65), (890, 1000 + k*65)], (54, 54, 60), 8)
        POLL_BG = c.out(W, H)
    fr.alpha_composite(POLL_BG)
    d = ImageDraw.Draw(fr)
    for ex in (760, 830): d.ellipse([ex - 18, 1170, ex + 18, 1190], fill=(250, 250, 230)); d.ellipse([ex - 6, 1174, ex + 6, 1186], fill=(10, 10, 10))
    put_max(fr, 440, 1330, 0.4, "angry", "reach", t, 1, gaze=-1, tremble=0.3)
    put_max(fr, 980, 1330, 0.4, "scared", "phone_hold", t, 1, gaze=-1, tremble=0.4)
    hl = None
    if T("slam") - 0.2 <= t < T("Or") or T("Slam,") - 0.1 <= t < T("Look?"): hl = 0
    elif T("Or") <= t < T("Vote") or t >= T("Look?"): hl = 1
    if hl is not None:
        x0 = 40 if hl == 0 else 552
        d.rounded_rectangle([x0-6, 714, x0+494, 1476], 44, outline=(255, 230, 80), width=10)
    p = 1 + 0.06*math.sin(t*5)
    d.text((284, 1400), "SLAM", font=font(90*p), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((796, 1400), "LOOK", font=font(90*(2-p)), fill=(255, 230, 80), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.ellipse([480, 1040, 600, 1160], fill=(255, 255, 255)); d.text((540, 1100), "VS", font=font(56), fill=(20, 18, 32), anchor="mm")
    k = ease(local/0.4)
    d.rounded_rectangle([110, 405, 970, 495], 45, fill=(230, 40, 60))
    d.text((540, 451), "VOTE IN THE COMMENTS", font=font(int(58*(0.75+0.25*k))), fill=(255, 255, 255), anchor="mm")

# ---------- fixed series cover (end card + TikTok cover) ----------
def make_cover(part):
    c = Cv(W, H, S, mode="RGB")
    for y in range(0, H, 10):
        k = y/H; c.rect(0, y, W, y+10, (int(12+20*k), int(12+14*k), int(34+30*k)))
    im = c.out(W, H).convert("RGBA")
    im.alpha_composite(blur_layer(lambda c: c.circ(540, 1000, 420, (255, 40, 40, 150)), 120))
    random.seed(3); d = ImageDraw.Draw(im)
    for _ in range(70): x, y = random.uniform(0, W), random.uniform(0, H); d.ellipse([x-2, y-2, x+2, y+2], fill=(240, 240, 220))
    face = make_max("shocked", True, False, "down", 0).crop((110, 60, 490, 440)).resize((720, 720), Image.LANCZOS)
    im.alpha_composite(face, (180, 660))
    d.text((540, 470), "LAST GUY", font=font(130), fill=(255, 255, 255), anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
    d.text((540, 610), "AWAKE", font=font(150), fill=(255, 220, 60), anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
    d.rounded_rectangle([290, 1390, 790, 1540], 75, fill=(230, 40, 60), outline=(255, 255, 255), width=8)
    d.text((540, 1465), f"PART {part}", font=font(100), fill=(255, 255, 255), anchor="mm")
    return im.convert("RGB").convert("RGBA")


