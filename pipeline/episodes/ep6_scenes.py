
# ================= Episode 6: Slam =================
SCENE_OF_LINE = ["hook", "recap_a", "recap_b", "slam", "slam", "slam", "lena6", "hands", "gdoor", "empty", "prints",
                 "photo6", "photo6", "photo6", "knock", "poll", "poll"]
CAP_Y = {"hook": 560, "recap_a": 1400, "recap_b": 560, "slam": 520, "lena6": 520, "hands": 520, "gdoor": 470,
         "empty": 560, "prints": 560, "photo6": 440, "knock": 520, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
TOTAL = dur + 1.4
COVER_T = 1e9
PART = 6

def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    tf = T("face.")
    if t >= tf and (t - tf) % 0.5 < 0.25:
        d.text((685, 323), "3?", font=font(60), fill=(255, 70, 70), anchor="mm")
    else:
        d.text((685, 323), "2", font=font(54), fill=(110, 255, 140), anchor="mm")

# ---------- recap A: eyes in the tunnel ----------
def r_recap_a6(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(40, 42, 48)); d.rectangle([140, 640, 940, 1560], fill=(6, 5, 7))
    fr.alpha_composite(alpha_q("hg5", HOLEGLOW5, 0.4 + 0.4*abs(math.sin(t*2))))
    for k in range(7):
        y = 700 + k*120; f = k/7; d.line([(330 + 40*f, y), (750 - 40*f, y)], fill=(54, 54, 60), width=14)
    d.line([(330, 640), (370, 1560)], fill=(54, 54, 60), width=14); d.line([(750, 640), (710, 1560)], fill=(54, 54, 60), width=14)
    d.rectangle([120, 620, 960, 660], fill=(96, 100, 110)); d.rectangle([120, 620, 160, 1580], fill=(96, 100, 110)); d.rectangle([920, 620, 960, 1580], fill=(96, 100, 110))
    for ex in (480, 600):
        d.ellipse([ex - 26, 1286, ex + 26, 1314], fill=(250, 250, 230)); d.ellipse([ex - 8, 1292, ex + 8, 1308], fill=(10, 10, 10))
    fr.alpha_composite(VIG["hard"]); previously(fr, t)

def r_recap_b6(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(20, 18, 32))
    t_rev = T("slam.")
    rv = ease((t - t_rev)/0.25) if t >= t_rev else 0
    q = ease((t - line_start[2] - 0.1)/1.8)
    for i, (lab, val, col) in enumerate([("SLAM", 75, (60, 200, 110)), ("LOOK", 25, (220, 60, 70))]):
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

# ---------- slam the hatch, toolbox, knocks ----------
def knock_times():
    t0 = T("Then"); return [t0 + 0.9, T("knocks.") + 0.05, T("From") - 0.05]
def fast_knocks():
    t0 = T("knocking"); return [t0 + 0.3 + k*0.32 for k in range(10)]

def draw_hatch_closed(fr, t, lid_p=1.0, box_p=1.0, jolts=()):
    d = ImageDraw.Draw(fr)
    hx0, hy0, hx1, hy1 = 360, 1560, 720, 1760
    j = 0
    for th in jolts:
        if 0 <= t - th < 0.18: j = int(10*(1 - (t - th)/0.18))
    d.rectangle([hx0, hy0, hx1, hy1], fill=(10, 8, 10))
    if lid_p < 1:      # lid still falling: from upright to flat
        top = hy0 - int(260*(1 - lid_p)); bot = hy0 + int((hy1 - hy0)*lid_p)
        d.polygon([(hx0, top), (hx1, top), (hx1, max(hy0, bot)), (hx0, max(hy0, bot))], fill=(96, 100, 110))
    else:
        d.rectangle([hx0, hy0 - j, hx1, hy1 - j], fill=(96, 100, 110))
        for rx, ry in ((hx0 + 20, hy0 + 20), (hx1 - 20, hy0 + 20), (hx0 + 20, hy1 - 20), (hx1 - 20, hy1 - 20)):
            d.ellipse([rx - 7, ry - 7 - j, rx + 7, ry + 7 - j], fill=(60, 60, 66))
        d.rectangle([515, 1650 - j, 565, 1670 - j], fill=(40, 40, 44))
        if j:
            for k in range(8):
                x = hx0 + 20 + k*42; d.ellipse([x - 4, hy0 - 20 - j*2, x + 4, hy0 - 12 - j*2], fill=(200, 200, 190))
    if box_p > 0:      # heavy red toolbox dragged on top
        bx = int(1100 - (1100 - 400)*box_p)
        d.rectangle([bx, 1560 - j - 120, bx + 280, 1560 - j + 40], fill=(180, 40, 40)); d.rectangle([bx, 1560 - j - 70, bx + 280, 1560 - j - 60], fill=(120, 20, 20))
        d.rectangle([bx + 100, 1560 - j - 150, bx + 180, 1560 - j - 120], outline=(60, 60, 60), width=10)

def r_slam(fr, t, local, li):
    ts = T("slams"); tb = T("drags")
    lid = ease((t - ts)/0.22) if t >= ts else 0.0
    box = ease((t - tb)/1.2) if t >= tb else 0.0
    put_max(fr, 220, 1500, 0.66, "angry" if li == 3 else "scared", "phone_hold", t, local, gaze=1, tremble=0.3)
    lx = 840 - 300*box if li == 3 else 840
    put_lena(fr, lx, 1500, 0.66, "angry" if li == 3 else "scared", t, arms="bat_hide", gaze=-1, tremble=0.3)
    draw_hatch_closed(fr, t, lid, box, knock_times())
    fr.alpha_composite(tint((0, 0, 10), 90))
    if li == 5: fr.alpha_composite(alpha_q("red", VIG["red"], 0.35 + 0.3*abs(math.sin(t*math.pi*1.5))))
    fr.alpha_composite(VIG["mid"])

def r_lena6(fr, t, local, li):
    p = ease(local/1.2)
    put_max(fr, 300, 1900, 1.0, "worried", "phone_hold", t, local, gaze=1, tremble=0.2)
    put_lena(fr, 760 + 120*p, 1900, 1.0, "scared", t, arms="bat_hide", gaze=-1, tremble=0.5)
    fr.alpha_composite(alpha_q("pg2", PGLOW2, 0.6), (50, 300))
    fr.alpha_composite(tint((0, 0, 10), 110)); fr.alpha_composite(VIG["mid"])

# ---------- dusty hands close-up ----------
def r_hands(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(tint((0, 0, 10), 170))
    sh = math.sin(t*30)*3
    for side, cx in ((-1, 330), (1, 750)):
        x = cx + sh*side
        d.rounded_rectangle([x - 150, 1450, x + 150, H + 40], 70, fill=HOOD)            # sleeve
        d.ellipse([x - 150, 1080, x + 150, 1500], fill=SKIN)                           # palm
        for k in range(4):                                                             # fingers
            fx = x - 105 + k*70; d.rounded_rectangle([fx - 28, 830 + abs(k - 1.5)*30, fx + 28, 1160], 28, fill=SKIN)
        tx = x + side*-1*170; d.rounded_rectangle([min(tx, x + side*-1*60) - 30, 1180, max(tx, x + side*-1*60) + 30, 1250], 30, fill=SKIN)  # thumb
        random.seed(cx)
        for _ in range(40):                                                            # dust smudges
            px, py = x + random.uniform(-130, 130), random.uniform(870, 1460); r_ = random.uniform(6, 22)
            d.ellipse([px - r_, py - r_*0.7, px + r_, py + r_*0.7], fill=(120, 112, 100, 170))
    # Lena's phone lying in his right palm
    d.rounded_rectangle([680, 1150, 820, 1400], 16, fill=(18, 18, 22)); d.rounded_rectangle([690, 1162, 810, 1388], 10, fill=(150, 200, 255))
    for k in range(18):                                                                # falling dust
        p = ((t*0.6) + k/18) % 1; x = 200 + (k*97) % 700; y = 1100 + p*700
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(200, 190, 170, int(200*(1 - p))))
    if t > T("before."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.5*ease((t - T("before."))/0.4)))
    fr.alpha_composite(VIG["mid"])

# ---------- garage door goes up by itself ----------
DOORBG = bg_door().convert("RGBA")
def r_gdoor(fr, t, local, li):
    tu = T("up.") - 0.3
    p = ease((t - tu)/2.0) if t > tu else 0
    out = STREET_DARK.crop((140, 700, 940, 1720)).resize((800, 1020))
    fr.alpha_composite(out, (140, 580))
    door = DOORBG.crop((140, 580, 940, 1600))
    dimg = Image.new("RGBA", (800, 1020), (0, 0, 0, 0)); dimg.alpha_composite(door, (0, -int(980*p)))
    fr.alpha_composite(dimg, (140, 580))
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, 580], fill=(40, 42, 48)); d.rectangle([0, 580, 140, 1600], fill=(40, 42, 48)); d.rectangle([940, 580, W, 1600], fill=(40, 42, 48))
    d.rectangle([0, 1600, W, H], fill=(58, 58, 62))
    fr.alpha_composite(tint((0, 0, 8), 110))
    if p > 0: fr.alpha_composite(alpha_q("leak6", LEAK6, p))
    fr.alpha_composite(VIG["hard"])
LEAK6 = blur_layer(lambda c: c.poly([(140, 1600), (940, 1600), (1080, 1920), (0, 1920)], (150, 160, 200, 90)), 30)

# ---------- empty street, footprints ----------
def r_empty(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    d = ImageDraw.Draw(fr)
    for k in range(14):                                                               # leaves blowing
        p = ((t*0.25) + k/14) % 1; x = -50 + p*1200; y = 1400 + 200*math.sin(k + t)
        d.ellipse([x - 8, y - 4, x + 8, y + 4], fill=(110, 90, 60))
    fr.alpha_composite(VIG["hard"])

FOOT = []
random.seed(21)
for k in range(140):
    lane = random.uniform(-1, 1); dist = random.uniform(0, 1)
    FOOT.append((540 + lane*(80 + 460*dist), 1330 + 590*dist, random.uniform(0, 1), dist))
def r_prints(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    d = ImageDraw.Draw(fr)
    p = ease((t - line_start[10])/2.5)
    for x, y, r_, dist in FOOT:
        if r_ < p:
            s = 0.4 + 1.2*dist
            d.ellipse([x - 9*s, y - 16*s, x + 9*s, y + 16*s], fill=(150, 140, 120)); d.ellipse([x - 6*s, y - 26*s, x + 6*s, y - 18*s], fill=(150, 140, 120))
    if t > T("house."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.45*ease((t - T("house."))/0.4)))
    fr.alpha_composite(VIG["hard"])

# ---------- photo of his bedroom: someone in his bed ----------
BEDROOM = bg_bedroom(True).convert("RGBA")
def photo_bed(open_eyes):
    im = BEDROOM.crop((0, 700, 1080, 1900)).resize((600, 667))
    c = Cv(600, 667, 2); c.im.alpha_composite(im.resize((1200, 1334)))
    c.rr(40, 400, 580, 667, 40, (70, 70, 120)); c.rr(60, 250, 400, 420, 40, (220, 220, 230))
    hd = make_max("neutral", open_eyes, False, "down", 1 if open_eyes else 0).crop((120, 70, 480, 440)).resize((520, 532), Image.LANCZOS)
    c.im.alpha_composite(hd, (160, 330))
    c.rr(30, 560, 590, 667, 40, (80, 80, 130))
    im = c.out(600, 667)
    a = np.array(im).astype(float); a[..., 0] *= 0.8; a[..., 1] = np.minimum(255, a[..., 1]*1.1 + 10); a[..., 2] *= 0.8
    im = Image.fromarray(a.astype(np.uint8), "RGBA")
    ImageDraw.Draw(im).text((20, 610), "NOW", font=font(40), fill=(255, 60, 60))
    return im
PHB = [photo_bed(False), photo_bed(True)]
def r_photo6(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 200))
    scr = Image.new("RGBA", (640, 1140), (250, 250, 252, 255)); d = ImageDraw.Draw(scr)
    d.text((40, 70), "Photos", font=font(56), fill=(20, 20, 30), anchor="lm")
    for i in range(12):
        r_, c_ = divmod(i, 3); scr.alpha_composite(THUMBS[i], (10 + c_*210, 140 + r_*212))
    tl = T("up.", 1) if len([k for k, t_ in enumerate(tokens) if t_[0] == "up."]) > 1 else line_start[11]
    k0 = ease((t - line_start[11])/0.3)
    d.rounded_rectangle([20, int(-100 + 150*k0), 620, int(-100 + 150*k0) + 110], 30, fill=(40, 40, 50))
    d.text((320, int(-100 + 150*k0) + 55), "Unknown: sent a photo", font=font(34), fill=(255, 255, 255), anchor="mm")
    if li >= 12:
        k = ease((t - line_start[12])/0.35)
        ph = PHB[1 if t >= T("face.") - 0.15 else 0]
        ph = ph.resize((int(200 + 420*k), int(220 + 470*k)))
        scr.alpha_composite(ph, (320 - ph.width//2, 160 + int(60*k)))
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); phone_frame(tmp, scr, t)
    fr.alpha_composite(tmp)
    if li == 13: fr.alpha_composite(alpha_q("red", VIG["red"], 0.5 + 0.3*abs(math.sin(t*math.pi*2))))
    fr.alpha_composite(VIG["mid"])

def r_knock(fr, t, local, li):
    draw_hatch_closed(fr, t, 1.0, 1.0, fast_knocks())
    put_max(fr, 220, 1500, 0.66, "shocked", "phone_hold", t, local, gaze=1, tremble=0.6)
    put_lena(fr, 860, 1500, 0.66, "scared", t, arms="bat_hide", gaze=-1, tremble=0.6)
    fr.alpha_composite(tint((0, 0, 10), 90))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.4 + 0.35*abs(math.sin(t*math.pi*3))))
    fr.alpha_composite(VIG["mid"])

# ---------- poll ----------
POLL_BG = None
def r_poll(fr, t, local, li):
    global POLL_BG
    if POLL_BG is None:
        c = Cv(W, H, S)
        c.rect(0, 0, W, H, (20, 18, 32))
        c.rr(40, 720, 528, 1470, 40, (40, 50, 80)); c.rr(552, 720, 1040, 1470, 40, (60, 40, 46))
        c.poly([(120, 1000), (284, 860), (448, 1000)], (90, 60, 50)); c.rect(150, 1000, 418, 1240, (70, 74, 96))   # HOME
        c.rect(180, 1040, 260, 1110, (255, 214, 140)); c.rect(310, 1120, 380, 1240, (40, 30, 30))
        c.rect(630, 1080, 960, 1260, (96, 100, 110)); c.rect(700, 960, 900, 1080, (180, 40, 40))                   # HATCH + toolbox
        POLL_BG = c.out(W, H)
    fr.alpha_composite(POLL_BG)
    d = ImageDraw.Draw(fr)
    jy = 6 if (t*3) % 1 < 0.15 else 0
    if jy: d.rectangle([630, 1080 - jy, 960, 1090], fill=(200, 200, 190))
    ImageDraw.Draw(fr).ellipse([195, 1050, 245, 1100], fill=(240, 220, 200))       # a face in the window
    put_max(fr, 440, 1330, 0.4, "scared", "phone_hold", t, 1, gaze=-1, tremble=0.3)
    put_lena(fr, 980, 1330, 0.4, "scared", t, arms="bat_hide", gaze=-1)
    hl = None
    if T("run") - 0.2 <= t < T("Or") or T("Home,") - 0.1 <= t < T("Hatch?"): hl = 0
    elif T("Or") <= t < T("Vote") or t >= T("Hatch?"): hl = 1
    if hl is not None:
        x0 = 40 if hl == 0 else 552
        d.rounded_rectangle([x0-6, 714, x0+494, 1476], 44, outline=(255, 230, 80), width=10)
    p = 1 + 0.06*math.sin(t*5)
    d.text((284, 1400), "HOME", font=font(90*p), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((796, 1400), "HATCH", font=font(86*(2-p)), fill=(255, 230, 80), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.ellipse([480, 1040, 600, 1160], fill=(255, 255, 255)); d.text((540, 1100), "VS", font=font(56), fill=(20, 18, 32), anchor="mm")
    k = ease(local/0.4)
    d.rounded_rectangle([110, 405, 970, 495], 45, fill=(230, 40, 60))
    d.text((540, 451), "VOTE IN THE COMMENTS", font=font(int(58*(0.75+0.25*k))), fill=(255, 255, 255), anchor="mm")

COVER = make_cover(PART); COVER.convert("RGB").save(f"cover_part{PART}.png")
print("ep6 backgrounds")
GAR = bg_garage().convert("RGBA")
BLK = Image.new("RGBA", (W, H), (0, 0, 0, 255))
BG = {"hook": BLK, "recap_a": BLK, "recap_b": BLK, "slam": GAR, "lena6": GAR, "hands": GAR, "gdoor": BLK,
      "empty": BLK, "prints": BLK, "photo6": GAR, "knock": GAR, "poll": BLK}
R = {"hook": r_hook, "recap_a": r_recap_a6, "recap_b": r_recap_b6, "slam": r_slam, "lena6": r_lena6, "hands": r_hands,
     "gdoor": r_gdoor, "empty": r_empty, "prints": r_prints, "photo6": r_photo6, "knock": r_knock, "poll": r_poll}
CAM = {"hook": (1.0, 1.15, 540, 1300), "recap_a": (1.0, 1.0, 540, 960), "recap_b": (1.0, 1.0, 540, 960),
       "slam": (1.0, 1.4, 540, 1550), "lena6": (1.0, 1.12, 560, 1200), "hands": (1.0, 1.15, 540, 1200),
       "gdoor": (1.0, 1.1, 540, 1100), "empty": (1.0, 1.2, 540, 1300), "prints": (1.0, 1.25, 540, 1500),
       "photo6": (1.0, 1.1, 540, 1000), "knock": (1.2, 1.6, 540, 1580), "poll": (1.0, 1.0, 540, 960)}
TRANS = {"recap_a": ("flash", 0.3), "recap_b": ("flash", 0.3), "slam": ("fade", 0.35), "lena6": ("fade", 0.3),
         "hands": ("fade", 0.3), "gdoor": ("black", 0.4), "empty": ("fade", 0.4), "prints": ("fade", 0.3),
         "photo6": ("fade", 0.3), "knock": ("black", 0.35), "poll": ("flash", 0.4)}

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
    for th, amp in [(T("slams") + 0.2, 16), (T("face.") - 0.1, 10)] + [(k, 6) for k in knock_times()] + [(k, 5) for k in fast_knocks()]:
        if 0 <= t - th < 0.3: a = (1 - (t - th)/0.3)*amp; shx += math.sin(t*90)*a; shy += math.cos(t*70)*a
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
    def wind(t0, t1, amp):
        i0, i1 = int(t0*SR), min(n, int(t1*SR)); L = i1 - i0
        nz = np.convolve(np.random.randn(L), np.ones(400)/400, "same")*20
        e = np.minimum(1, np.arange(L)/SR/0.8)*np.minimum(1, (L - np.arange(L))/SR/0.8)*(0.6 + 0.4*np.sin(np.arange(L)/SR*0.9))
        a[i0:i1] += nz*e*amp
    ls = line_start
    hit(0.02, 50, 0.7, 0.3, noise=0.1)
    pad([55.0, 58.3], 0, ls[2] + 0.3, 0.07, 0.6, 0.5)
    hit(T("kids.") - 0.03, 50, 0.9, 0.3, noise=0.1)
    hit(T("slam.") - 0.03, 48, 0.8, 0.35, noise=0.15)
    hit(T("slams") + 0.2, 60, 0.3, 0.9, noise=0.6); hit(T("slams") + 0.2, 300, 0.1, 0.25, noise=0.6)
    for k in np.arange(T("drags"), T("drags") + 1.2, 0.04): click(k, 0.04, 900)            # toolbox scraping
    hit(T("drags") + 1.2, 120, 0.15, 0.4, noise=0.4)
    for k in knock_times(): hit(k, 110, 0.06, 0.6, noise=0.3)
    pad([41.2, 43.7], ls[4], ls[8], 0.1, 0.4, 0.6, trem=0.3)
    pad([1318.5, 1396.9], T("before."), ls[8] + 0.3, 0.01, 0.3, 0.6, trem=0.6)
    tu = T("up.") - 0.3
    for k in np.arange(tu, tu + 2.0, 0.07): click(k, 0.06, 1200)                              # door rattling up
    pad([60.0, 90.0], tu, tu + 2.0, 0.08, 0.2, 0.3)
    wind(ls[9], ls[11] + 0.5, 0.05)
    hit(T("house.") - 0.05, 40, 1.1, 0.5, noise=0.2)
    hit(ls[11], 1320, 0.15, 0.06)
    pad([55.0, 82.4], ls[11], ls[14], 0.07, 0.6, 0.4)
    hit(T("face.") - 0.05, 36, 1.4, 0.65, noise=0.3)
    for k in fast_knocks(): hit(k, 110, 0.06, 0.6, noise=0.3)
    hb = ls[12]; per = 0.7
    while hb < ls[15]:
        hit(hb, 45, 0.08, 0.4); hit(hb + 0.18, 42, 0.08, 0.28); per = max(0.42, per*0.95); hb += per
    pad([55.0, 82.4], ls[15] - 0.2, TOTAL, 0.08, 0.5, 1.0)
    return a
voice_raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", "voice.mp3", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
voice = np.frombuffer(voice_raw, np.int16).astype(float)/32768
# echo on "Open up, Max. It's me." so it sounds like it comes from under the hatch
ko = tok("Open"); i0 = int((starts[ko] - 0.05)*SR); i1 = int((ends[tok("me.")] + 0.1)*SR)
seg = np.convolve(voice[i0:i1].copy(), np.ones(10)/10, "same")
amb = make_ambient()
mix = amb.copy(); mix[:len(voice)] += voice[:len(mix)]
for dl, g in [(0.22, 0.4), (0.44, 0.25), (0.66, 0.14)]:
    j = i0 + int(dl*SR); mix[j:j+len(seg)] += seg[:max(0, len(mix)-j)]*g
mix = mix/max(1.0, np.abs(mix).max()*1.02)
import wave
with wave.open("mix.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((mix*32767).astype(np.int16).tobytes())
