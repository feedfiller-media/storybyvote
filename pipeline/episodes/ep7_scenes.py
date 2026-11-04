
# ================= Episode 7: Home =================
SCENE_OF_LINE = ["hook", "recap_a", "recap_b", "run", "prints7", "stairs7", "door7", "door7", "bed7", "note", "note",
                 "batpoint", "closet", "poll", "poll"]
CAP_Y = {"hook": 560, "recap_a": 1450, "recap_b": 560, "run": 520, "prints7": 560, "stairs7": 520, "door7": 470,
         "bed7": 520, "note": 440, "batpoint": 520, "closet": 520, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
TOTAL = dur + 1.4
COVER_T = 1e9
PART = 7

def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    tf = T("clicks")
    if t >= tf and (t - tf) % 0.5 < 0.25:
        d.text((685, 323), "3?", font=font(60), fill=(255, 70, 70), anchor="mm")
    else:
        d.text((685, 323), "2", font=font(54), fill=(110, 255, 140), anchor="mm")

# ---------- recap: the photo of someone in his bed ----------
def r_recap_a7(fr, t, local, li):
    fr.alpha_composite(tint((0, 0, 10), 200))
    scr = Image.new("RGBA", (640, 1140), (250, 250, 252, 255))
    ph = PHB[1 if t > T("face.") - 0.15 else 0].resize((620, 690))
    scr.alpha_composite(ph, (10, 220))
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); phone_frame(tmp, scr, t); fr.alpha_composite(tmp)
    fr.alpha_composite(VIG["mid"]); previously(fr, t)

def r_recap_b7(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(20, 18, 32))
    t_rev = T("home.")
    rv = ease((t - t_rev)/0.25) if t >= t_rev else 0
    q = ease((t - line_start[2] - 0.1)/1.8)
    for i, (lab, val, col) in enumerate([("HOME", 77, (60, 200, 110)), ("HATCH", 23, (220, 60, 70))]):
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

# ---------- running through the empty street ----------
def r_run(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    p = local/scene_len("run")
    bob = abs(math.sin(t*9))*14
    put_lena(fr, 260 + 520*p, 1640 - bob*0.8, 0.55, "angry", t, arms="bat_hide")
    put_max(fr, 420 + 520*p, 1660 - bob, 0.55, "scared", "phone_hold", t, local, gaze=1, walk=1.0)
    fr.alpha_composite(VIG["hard"])

def r_prints7(fr, t, local, li):
    fr.alpha_composite(STREET_DARK)
    d = ImageDraw.Draw(fr)
    p = ease((t - line_start[4])/2.2)
    for x, y, r_, dist in FOOT:
        if r_ < p:
            s = 0.4 + 1.2*dist
            d.ellipse([x - 9*s, y - 16*s, x + 9*s, y + 16*s], fill=(150, 140, 120)); d.ellipse([x - 6*s, y - 26*s, x + 6*s, y - 18*s], fill=(150, 140, 120))
    if t > T("house."): fr.alpha_composite(alpha_q("red", VIG["red"], 0.4*ease((t - T("house."))/0.4)))
    fr.alpha_composite(VIG["hard"])

STAIRS = Image.open("assets/bg_stairs3.png").convert("RGBA").resize((W, H))
def r_stairs7(fr, t, local, li):
    fr.alpha_composite(STAIRS)
    p = ease(local/scene_len("stairs7"))
    put_max(fr, 470 + 120*p, 1720 - 330*p, 0.62, "scared", "phone_hold", t, local, gaze=1, walk=0.6, tremble=0.2)
    put_lena(fr, 300 + 120*p, 1820 - 250*p, 0.62, "worried", t, arms="bat_hide")
    fr.alpha_composite(tint((0, 0, 20), 120)); fr.alpha_composite(VIG["hard"])

# ---------- the bedroom door, locked from the outside ----------
WOOD = (120, 82, 58)
def r_door7(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(70, 66, 84)); d.rectangle([0, 1600, W, H], fill=(60, 48, 40))
    tk = T("key."); to = T("open.")
    op = ease((t - to + 0.3)/1.0) if t > to - 0.3 else 0
    d.rectangle([240, 560, 840, 1600], fill=(10, 8, 12))                       # dark room behind
    dw = int(600*(1 - 0.8*op))
    d.rectangle([240, 560, 240 + dw, 1600], fill=WOOD)
    for y0 in (620, 1120):
        d.rectangle([270, y0, 240 + dw - 30, y0 + 420], outline=(96, 64, 44), width=10)
    if dw > 120:
        kx = 240 + dw - 80
        d.ellipse([kx - 22, 1060, kx + 22, 1104], fill=(200, 180, 90))           # lock plate
        ang = math.radians(90*ease((t - tk)/0.4)) if t > tk else 0             # key turns
        x2, y2 = kx + 70*math.cos(ang), 1082 + 70*math.sin(ang)
        d.line([(kx, 1082), (x2, y2)], fill=(220, 200, 110), width=12); d.ellipse([x2 - 22, y2 - 22, x2 + 22, y2 + 22], fill=(220, 200, 110))
        if li == 7 and t < to:                                                 # Lena's hand on the key
            d.ellipse([x2 - 45, y2 - 40, x2 + 45, y2 + 40], fill=SKIN); d.rectangle([x2 + 20, y2 - 50, W, y2 + 60], fill=(196, 62, 72))
    if li == 6:
        d.text((540, 1300), "LOCKED FROM OUTSIDE", font=font(46), fill=(255, 90, 90), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    fr.alpha_composite(tint((0, 0, 10), 80)); fr.alpha_composite(VIG["hard"])

# ---------- empty bed, blanket still moving ----------
BEDBG = bg_bedroom(True).convert("RGBA")
def r_bed7(fr, t, local, li):
    fr.alpha_composite(BEDBG)
    d = ImageDraw.Draw(fr)
    tb = T("moving.") - 0.6
    m = 0.5 + 0.5*math.sin(t*7) if t > tb else 0
    d.rounded_rectangle([615, 1330, 1060, 1500], 30, fill=(70, 70, 120))
    d.ellipse([720, int(1310 - 40*m), 960, int(1400 - 10*m)], fill=(80, 80, 132))     # bump under the blanket
    put_max(fr, 260, 1760, 0.7, "shocked", "phone_hold", t, local, gaze=1, tremble=0.4)
    put_lena(fr, 430, 1800, 0.7, "scared", t, arms="bat_hide", gaze=1)
    fr.alpha_composite(tint((0, 0, 20), 110))
    if t > tb: fr.alpha_composite(alpha_q("red", VIG["red"], 0.3 + 0.2*m))
    fr.alpha_composite(VIG["mid"])

# ---------- the note in Max's handwriting ----------
def r_note(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(tint((0, 0, 10), 190))
    tp = T("picks")
    lift = ease((t - tp)/0.6) if t > tp else 0
    y0 = int(1250 - 400*lift)
    if lift < 0.2: d.rounded_rectangle([200, 1380, 880, 1700], 60, fill=(110, 110, 130))   # pillow
    c = Cv(620, 760, 2); c.rr(0, 0, 620, 760, 10, (244, 240, 226))
    for k in range(10): c.line([(30, 90 + k*64), (590, 90 + k*64)], (190, 200, 225), 3)
    im = c.out(620, 760)
    if li == 10:
        k = ease((t - line_start[10])/1.6)
        dd = ImageDraw.Draw(im); words = ["Don't trust", "the one", "who came home."]
        for i, w in enumerate(words):
            if k > i/3: dd.text((310, 200 + i*130), w, font=font(64), fill=(30, 36, 80), anchor="mm")
    im = im.rotate(-4 + math.sin(t*1.5)*1.5, expand=True, resample=Image.BICUBIC)
    fr.alpha_composite(im, (540 - im.width//2, y0 - im.height//2))
    if lift > 0:                                                                # Lena's fingers holding the note
        for hx in (300, 780):
            d.ellipse([hx - 60, y0 + 320, hx + 60, y0 + 450], fill=SKIN); d.rectangle([hx - 70, y0 + 420, hx + 70, H], fill=(196, 62, 72))
    if li == 10: fr.alpha_composite(alpha_q("red", VIG["red"], 0.4 + 0.3*abs(math.sin(t*math.pi*1.5))))
    fr.alpha_composite(VIG["mid"])

# ---------- Lena points the bat at Max ----------
def r_batpoint(fr, t, local, li):
    fr.alpha_composite(BEDBG); fr.alpha_composite(tint((0, 0, 20), 150))
    tl = T("lifts")
    arms = "bat" if t > tl else "bat_hide"
    put_max(fr, 280, 1950, 1.05, "scared", "phone_hold", t, local, gaze=1, tremble=0.6)
    put_lena(fr, 800, 1950, 1.05, "angry", t, arms=arms, gaze=-1, tremble=0.2)
    if t > T("points"): fr.alpha_composite(alpha_q("red", VIG["red"], 0.45))
    fr.alpha_composite(VIG["mid"])

# ---------- the closet clicks open ----------
def r_closet(fr, t, local, li):
    fr.alpha_composite(BEDBG)
    d = ImageDraw.Draw(fr)
    tc = T("clicks")
    gap = int(90*ease((t - tc)/1.2)) if t > tc else 0
    d.rectangle([80, 700, 520, 1500], fill=(96, 70, 52))
    d.rectangle([300 - gap//2, 712, 300 + gap//2, 1490], fill=(6, 5, 8))
    d.rectangle([92, 712, 300 - gap//2 - 4, 1490], fill=(110, 80, 60)); d.rectangle([300 + gap//2 + 4, 712, 508, 1490], fill=(110, 80, 60))
    d.ellipse([270 - gap//2, 1080, 290 - gap//2, 1100], fill=(200, 180, 90)); d.ellipse([310 + gap//2, 1080, 330 + gap//2, 1100], fill=(200, 180, 90))
    if gap > 50:
        a = ease((t - tc - 0.8)/0.4)
        for ex in (290, 310): d.ellipse([ex - 7, 960, ex + 7, 972], fill=(int(250*a), int(250*a), int(230*a)))
    put_max(fr, 760, 1800, 0.75, "shocked", "phone_hold", t, local, gaze=-1, tremble=0.5)
    put_lena(fr, 950, 1820, 0.75, "scared", t, arms="bat", gaze=-1)
    fr.alpha_composite(tint((0, 0, 20), 120))
    fr.alpha_composite(alpha_q("red", VIG["red"], 0.35 + 0.3*abs(math.sin(t*math.pi*2))))
    fr.alpha_composite(VIG["mid"])

# ---------- poll ----------
POLL_BG = None
def r_poll(fr, t, local, li):
    global POLL_BG
    if POLL_BG is None:
        c = Cv(W, H, S)
        c.rect(0, 0, W, H, (20, 18, 32))
        c.rr(40, 720, 528, 1470, 40, (40, 50, 80)); c.rr(552, 720, 1040, 1470, 40, (60, 40, 46))
        c.rr(150, 860, 420, 990, 40, (255, 255, 255)); c.poly([(200, 985), (240, 985), (190, 1030)], (255, 255, 255))   # speech bubble
        for k in range(3): c.circ(220 + k*65, 925, 14, (40, 40, 60))
        c.rect(660, 860, 940, 1280, (96, 70, 52)); c.rect(795, 870, 805, 1270, (6, 5, 8))                                 # closet
        POLL_BG = c.out(W, H)
    fr.alpha_composite(POLL_BG)
    d = ImageDraw.Draw(fr)
    for ex in (795, 805): d.ellipse([ex - 4, 1000, ex + 4, 1008], fill=(250, 250, 230))
    put_max(fr, 300, 1330, 0.4, "worried", "up", t, 1, gaze=1, tremble=0.2)
    put_lena(fr, 980, 1330, 0.4, "angry", t, arms="bat")
    hl = None
    if T("explain?") - 0.6 <= t < T("Or") or T("Explain,") - 0.1 <= t < T("Closet?"): hl = 0
    elif T("Or") <= t < T("Vote") or t >= T("Closet?"): hl = 1
    if hl is not None:
        x0 = 40 if hl == 0 else 552
        d.rounded_rectangle([x0-6, 714, x0+494, 1476], 44, outline=(255, 230, 80), width=10)
    p = 1 + 0.06*math.sin(t*5)
    d.text((284, 1400), "EXPLAIN", font=font(78*p), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((796, 1400), "CLOSET", font=font(80*(2-p)), fill=(255, 230, 80), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.ellipse([480, 1040, 600, 1160], fill=(255, 255, 255)); d.text((540, 1100), "VS", font=font(56), fill=(20, 18, 32), anchor="mm")
    k = ease(local/0.4)
    d.rounded_rectangle([110, 405, 970, 495], 45, fill=(230, 40, 60))
    d.text((540, 451), "VOTE IN THE COMMENTS", font=font(int(58*(0.75+0.25*k))), fill=(255, 255, 255), anchor="mm")

COVER = make_cover(PART); COVER.convert("RGB").save(f"cover_part{PART}.png")
print("ep7 backgrounds")
GAR = bg_garage().convert("RGBA")
BLK = Image.new("RGBA", (W, H), (0, 0, 0, 255))
BG = {"hook": BLK, "recap_a": GAR, "recap_b": BLK, "run": BLK, "prints7": BLK, "stairs7": BLK, "door7": BLK,
      "bed7": BLK, "note": BEDBG, "batpoint": BLK, "closet": BLK, "poll": BLK}
R = {"hook": r_hook, "recap_a": r_recap_a7, "recap_b": r_recap_b7, "run": r_run, "prints7": r_prints7, "stairs7": r_stairs7,
     "door7": r_door7, "bed7": r_bed7, "note": r_note, "batpoint": r_batpoint, "closet": r_closet, "poll": r_poll}
CAM = {"hook": (1.0, 1.15, 540, 1300), "recap_a": (1.0, 1.0, 540, 960), "recap_b": (1.0, 1.0, 540, 960),
       "run": (1.0, 1.1, 540, 1400), "prints7": (1.0, 1.25, 540, 1500), "stairs7": (1.0, 1.15, 540, 1300),
       "door7": (1.0, 1.15, 540, 1100), "bed7": (1.0, 1.2, 760, 1350), "note": (1.0, 1.08, 540, 1000),
       "batpoint": (1.0, 1.2, 540, 1250), "closet": (1.0, 1.3, 330, 1100), "poll": (1.0, 1.0, 540, 960)}
TRANS = {"recap_a": ("flash", 0.3), "recap_b": ("flash", 0.3), "run": ("fade", 0.35), "prints7": ("fade", 0.3),
         "stairs7": ("black", 0.4), "door7": ("fade", 0.3), "bed7": ("fade", 0.3), "note": ("fade", 0.3),
         "batpoint": ("flash", 0.25), "closet": ("black", 0.35), "poll": ("flash", 0.4)}

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
    for th, amp in [(T("open."), 8), (T("lifts") + 0.2, 10), (T("clicks"), 14), (T("home.", 1), 6)]:
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
    def sweep(t0, d_, f0, f1, amp, noise=0.0):
        i0 = int(t0*SR); L = int(d_*SR)
        if i0 < 0 or i0 + L >= n: return
        x = np.arange(L)/SR; f = f0 + (f1 - f0)*x/d_; s = np.sin(2*np.pi*np.cumsum(f)/SR)
        if noise: s += noise*np.convolve(np.random.randn(L), np.ones(30)/30, "same")*4
        a[i0:i0+L] += s*amp*np.minimum(1, x/0.03)*np.minimum(1, (d_ - x)/0.1)
    ls = line_start
    hit(0.02, 50, 0.7, 0.3, noise=0.1)
    pad([55.0, 58.3], 0, ls[2] + 0.3, 0.07, 0.6, 0.5)
    hit(T("kids.") - 0.03, 50, 0.9, 0.3, noise=0.1)
    hit(T("home.") - 0.03, 48, 0.8, 0.35, noise=0.15)
    for k in np.arange(ls[3], ls[4], 0.22): hit(k, 90, 0.04, 0.25, noise=0.4)                # running steps
    pad([73.4, 110.0], ls[3], ls[6], 0.06, 0.6, 0.6)
    for k in (T("creak") - 0.1, T("every") + 0.1, T("step.") + 0.2): sweep(k, 0.45, 380, 250, 0.04, noise=0.2)
    pad([41.2, 43.7], ls[6], ls[13], 0.1, 0.5, 0.6, trem=0.3)
    click(T("key."), 0.2, 900); click(T("key.") + 0.25, 0.15, 900)
    sweep(T("open.") - 0.3, 1.0, 300, 180, 0.05, noise=0.3)
    for k in np.arange(T("moving.") - 0.6, ls[9], 0.15): click(k, 0.02, 2500)                 # blanket rustle
    hit(T("handwriting."), 50, 0.9, 0.35, noise=0.1)
    hit(ls[10], 40, 1.2, 0.5, noise=0.2)
    hit(T("lifts") + 0.2, 200, 0.06, 0.2, noise=0.5)
    hb = ls[11]; per = 0.7
    while hb < ls[13]:
        hit(hb, 45, 0.08, 0.4); hit(hb + 0.18, 42, 0.08, 0.28); per = max(0.42, per*0.94); hb += per
    hit(T("clicks"), 900, 0.03, 0.4, noise=0.3); hit(T("clicks") + 0.05, 36, 1.3, 0.6, noise=0.3)
    sweep(T("clicks") + 0.1, 1.2, 260, 160, 0.04, noise=0.3)
    pad([55.0, 82.4], ls[13] - 0.2, TOTAL, 0.08, 0.5, 1.0)
    return a
voice_raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", "voice.mp3", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
voice = np.frombuffer(voice_raw, np.int16).astype(float)/32768
amb = make_ambient()
mix = amb.copy(); mix[:len(voice)] += voice[:len(mix)]
mix = mix/max(1.0, np.abs(mix).max()*1.02)
import wave
with wave.open("mix.wav", "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((mix*32767).astype(np.int16).tobytes())
