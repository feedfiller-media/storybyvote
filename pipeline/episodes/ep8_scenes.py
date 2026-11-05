
# ================= Episode 8: Explain =================
SCENE_OF_LINE = ["hook", "recap_a", "recap_b", "talk", "talk", "talk", "scars", "scars", "closet8", "closet8", "closet8",
                 "drop", "doorway", "poll", "poll"]
CAP_Y = {"hook": 560, "recap_a": 1450, "recap_b": 560, "talk": 520, "scars": 470, "closet8": 470, "drop": 520,
         "doorway": 1400, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
TOTAL = dur + 1.4
COVER_T = 1e9
PART = 8
BEDBG = bg_bedroom(True).convert("RGBA")

def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    tf = T("doorway,")
    if t >= tf and (t - tf) % 0.5 < 0.25:
        d.text((685, 323), "3?", font=font(60), fill=(255, 70, 70), anchor="mm")
    else:
        d.text((685, 323), "2", font=font(54), fill=(110, 255, 140), anchor="mm")

def closet_draw(fr, t, gap, eyes=0.0, inside=0, sleeper=0.0):
    d = ImageDraw.Draw(fr)
    d.rectangle([80, 700, 520, 1500], fill=(96, 70, 52))
    d.rectangle([300 - gap//2, 712, 300 + gap//2, 1490], fill=(6, 5, 8))
    if inside and gap > 200:
        cx = 300
        d.line([(cx - 160, 780), (cx + 160, 780)], fill=(120, 120, 130), width=8)          # rod
        d.polygon([(cx - 20, 790), (cx + 20, 790), (cx, 770)], outline=(150, 150, 160))      # hanger
        d.rounded_rectangle([cx - 90, 800, cx + 90, 1080], 40, fill=(196, 62, 72))           # red hoodie
        d.rectangle([cx - 130, 820, cx - 90, 1040], fill=(196, 62, 72)); d.rectangle([cx + 90, 820, cx + 130, 1040], fill=(196, 62, 72))
        d.line([(cx - 20, 820), (cx - 24, 900)], fill=(255, 255, 255), width=4); d.line([(cx + 20, 820), (cx + 24, 900)], fill=(255, 255, 255), width=4)
    if sleeper > 0:
        sp = SLEEPER.copy(); a = np.array(sp); a[..., 3] = (a[..., 3]*sleeper).astype(np.uint8)
        fr.alpha_composite(Image.fromarray(a), (300 - sp.width//2, 1480 - sp.height))
    lw = 220 - gap//2
    if lw > 8:
        d.rectangle([92, 712, 92 + lw - 4, 1490], fill=(110, 80, 60)); d.rectangle([508 - lw + 4, 712, 508, 1490], fill=(110, 80, 60))
    if eyes > 0 and not inside:
        for ex in (290, 310): d.ellipse([ex - 7, 960, ex + 7, 972], fill=(int(250*eyes), int(250*eyes), int(230*eyes)))
_sl = make_lena("neutral", False, "down", 0).rotate(90, expand=True, resample=Image.BICUBIC)
SLEEPER = _sl.resize((int(_sl.width*0.33), int(_sl.height*0.33)), Image.LANCZOS)

# ---------- recap ----------
def r_recap_a8(fr, t, local, li):
    fr.alpha_composite(BEDBG)
    closet_draw(fr, t, 90, eyes=1.0)
    put_max(fr, 760, 1800, 0.75, "shocked", "phone_hold", t, local, gaze=-1, tremble=0.5)
    put_lena(fr, 950, 1820, 0.75, "angry", t, arms="bat", gaze=-1)
    fr.alpha_composite(tint((0, 0, 20), 120)); fr.alpha_composite(VIG["mid"]); previously(fr, t)

def r_recap_b8(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(20, 18, 32))
    t_rev = T("explain.")
    rv = ease((t - t_rev)/0.25) if t >= t_rev else 0
    q = ease((t - line_start[2] - 0.1)/1.8)
    for i, (lab, val, col) in enumerate([("EXPLAIN", 75, (60, 200, 110)), ("CLOSET", 25, (220, 60, 70))]):
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

# ---------- Max explains ----------
def r_talk(fr, t, local, li):
    fr.alpha_composite(BEDBG); fr.alpha_composite(tint((0, 0, 20), 150))
    talk = any(starts[k] <= t < ends[k] for k in range(len(tokens))) and li in (3, 4)
    put_max(fr, 290, 1950, 1.05, "worried" if li < 5 else "scared", "up", t, local, gaze=1, talk=talk, tremble=0.3)
    put_lena(fr, 800, 1950, 1.05, "angry", t, arms="bat", gaze=-1)
    if li == 5 and t > T("whispers."):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.35))
    fr.alpha_composite(VIG["mid"])

# ---------- the same scar on both hands ----------
def hand(d, cx, top, sleeve, scar):
    d.rounded_rectangle([cx - 170, min(top + 520, H - 10), cx + 170, H + 40], 70, fill=sleeve)
    d.ellipse([cx - 150, top + 160, cx + 150, top + 560], fill=SKIN)
    for k in range(4):
        fx = cx - 105 + k*70; d.rounded_rectangle([fx - 28, top - 60 + abs(k - 1.5)*30, fx + 28, top + 250], 28, fill=SKIN)
    if scar > 0:
        pts = [(cx - 90 + i*30, top + 360 + (12 if i % 2 else -12)) for i in range(7)]
        d.line(pts[:max(2, int(7*scar))], fill=(200, 90, 110), width=12)
def r_scars(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(tint((0, 0, 10), 190))
    ts = T("scar"); tl = T("sleeve.")
    hand(d, 300, 900, HOOD, ease((t - ts)/0.6) if t > ts else 0)
    if li == 7:
        p = ease((t - line_start[7])/0.6)
        hand(d, 780, int(1500 - 600*p), (196, 62, 72), ease((t - tl)/0.6) if t > tl else 0)
    if li == 7 and t > T("same"):
        fr.alpha_composite(alpha_q("red", VIG["red"], 0.45))
    fr.alpha_composite(VIG["mid"])

# ---------- the closet opens: Lena's hoodie, a sleeping Lena ----------
def r_closet8(fr, t, local, li):
    fr.alpha_composite(BEDBG)
    gap = int(90 + 330*ease((t - line_start[8])/0.8))
    sl = ease((t - T("asleep.", 1) + 0.3)/0.6) if t > T("asleep.", 1) - 0.3 else 0
    closet_draw(fr, t, gap, inside=1, sleeper=sl)
    put_max(fr, 760, 1800, 0.75, "shocked", "phone_hold", t, local, gaze=-1, tremble=0.4)
    put_lena(fr, 950, 1820, 0.75, "scared" if li >= 9 else "angry", t, arms="bat", gaze=-1, tremble=0.3 if li == 10 else 0)
    fr.alpha_composite(tint((0, 0, 20), 100))
    if li == 10 and t > T("face."): fr.alpha_composite(alpha_q("red", VIG["red"], 0.5))
    fr.alpha_composite(VIG["mid"])

# ---------- Lena drops the bat ----------
def r_drop(fr, t, local, li):
    fr.alpha_composite(BEDBG); fr.alpha_composite(tint((0, 0, 20), 150))
    td = T("drops")
    put_lena(fr, 560, 2050, 1.3, "shocked", t, arms="down" if t > td else "bat", gaze=0, tremble=0.5)
    if t > td:
        p = min(1.0, (t - td)/0.5)
        im = Image.new("RGBA", (80, 520), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([20, 0, 60, 520], 20, fill=(176, 120, 70)); dd.rectangle([22, 400, 58, 470], fill=(40, 40, 40))
        im = im.rotate(-90*p, expand=True, resample=Image.BICUBIC)
        fr.alpha_composite(im, (int(700 - im.width/2), int(1250 + 520*p*p - im.height/2)))
    fr.alpha_composite(VIG["mid"])

# ---------- a figure in the doorway ----------
def r_doorway(fr, t, local, li):
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, W, H], fill=(12, 12, 18)); d.rectangle([0, 1600, W, H], fill=(30, 26, 26))
    d.rectangle([300, 520, 780, 1600], fill=(200, 190, 160))                          # lit hallway through the door
    fr.alpha_composite(alpha_q("dl", DOORLIGHT, 0.8))
    p = ease((t - line_start[12])/1.5)
    sh = 0.9 + 0.1*p
    d.ellipse([540 - 70*sh, 760, 540 + 70*sh, 900], fill=(10, 10, 14))                  # silhouette head
    d.rounded_rectangle([540 - 120*sh, 880, 540 + 120*sh, 1600], 60, fill=(10, 10, 14))
    if t > T("doorway,"):
        a = ease((t - T("doorway,"))/0.4)
        for ex in (515, 565): d.ellipse([ex - 9, 822, ex + 9, 836], fill=(int(255*a), int(80*a), int(80*a)))
    fr.alpha_composite(VIG["hard"])
DOORLIGHT = blur_layer(lambda c: c.poly([(300, 1600), (780, 1600), (1000, 1920), (80, 1920)], (220, 210, 170, 90)), 40)

# ---------- poll ----------
POLL_BG = None
def r_poll(fr, t, local, li):
    global POLL_BG
    if POLL_BG is None:
        c = Cv(W, H, S)
        c.rect(0, 0, W, H, (20, 18, 32))
        c.rr(40, 720, 528, 1470, 40, (40, 50, 80)); c.rr(552, 720, 1040, 1470, 40, (60, 40, 46))
        c.rect(640, 860, 960, 1300, (200, 190, 160)); c.circ(800, 960, 50, (10, 10, 14)); c.rr(720, 1000, 880, 1300, 40, (10, 10, 14))
        for k in range(3): c.line([(100 + k*20, 1000 + k*60), (180 + k*20, 1000 + k*60)], (255, 255, 255), 8)   # speed lines
        POLL_BG = c.out(W, H)
    fr.alpha_composite(POLL_BG)
    d = ImageDraw.Draw(fr)
    for ex in (788, 812): d.ellipse([ex - 5, 950, ex + 5, 960], fill=(255, 80, 80))
    put_lena(fr, 250, 1330, 0.4, "scared", t, arms="down")
    put_max(fr, 380, 1330, 0.4, "scared", "reach", t, 1, gaze=-1, walk=1.0)
    hl = None
    if T("grab") - 0.2 <= t < T("Or") or T("Run,") - 0.1 <= t < T("Turn?"): hl = 0
    elif T("Or") <= t < T("Vote") or t >= T("Turn?"): hl = 1
    if hl is not None:
        x0 = 40 if hl == 0 else 552
        d.rounded_rectangle([x0-6, 714, x0+494, 1476], 44, outline=(255, 230, 80), width=10)
    p = 1 + 0.06*math.sin(t*5)
    d.text((284, 1400), "RUN", font=font(90*p), fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((796, 1400), "TURN", font=font(90*(2-p)), fill=(255, 230, 80), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.ellipse([480, 1040, 600, 1160], fill=(255, 255, 255)); d.text((540, 1100), "VS", font=font(56), fill=(20, 18, 32), anchor="mm")
    k = ease(local/0.4)
    d.rounded_rectangle([110, 405, 970, 495], 45, fill=(230, 40, 60))
    d.text((540, 451), "VOTE IN THE COMMENTS", font=font(int(58*(0.75+0.25*k))), fill=(255, 255, 255), anchor="mm")

COVER = make_cover(PART); COVER.convert("RGB").save(f"cover_part{PART}.png")
print("ep8 backgrounds")
BLK = Image.new("RGBA", (W, H), (0, 0, 0, 255))
BG = {k: BLK for k in ORDER}
R = {"hook": r_hook, "recap_a": r_recap_a8, "recap_b": r_recap_b8, "talk": r_talk, "scars": r_scars,
     "closet8": r_closet8, "drop": r_drop, "doorway": r_doorway, "poll": r_poll}
CAM = {"hook": (1.0, 1.15, 540, 1300), "recap_a": (1.0, 1.0, 540, 960), "recap_b": (1.0, 1.0, 540, 960),
       "talk": (1.0, 1.15, 540, 1250), "scars": (1.0, 1.1, 540, 1250), "closet8": (1.0, 1.3, 330, 1150),
       "drop": (1.0, 1.25, 560, 1300), "doorway": (1.0, 1.35, 540, 900), "poll": (1.0, 1.0, 540, 960)}
TRANS = {"recap_a": ("flash", 0.3), "recap_b": ("flash", 0.3), "talk": ("fade", 0.35), "scars": ("fade", 0.3),
         "closet8": ("black", 0.35), "drop": ("flash", 0.25), "doorway": ("black", 0.4), "poll": ("flash", 0.4)}

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
    for th, amp in [(line_start[8], 10), (T("face."), 8), (T("drops") + 0.5, 12), (T("doorway,"), 10)]:
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
    def pad(freqs, t0, t1, amp, att=1.5, rel=1.5, trem=0.0):
        e = env(t0, t1, att, rel); m = e > 0; s = np.zeros(n)
        for f in freqs:
            ph = 2*np.pi*f*tt[m] + 0.3*np.sin(2*np.pi*0.2*tt[m]); s[m] += np.sin(ph) + 0.3*np.sin(2.003*ph)
        if trem: s *= 1 - trem*(0.5 + 0.5*np.sin(2*np.pi*3*tt))
        a[:] += s*e*amp/len(freqs)
    def hit(t0, f, dec, amp, noise=0.0):
        i0 = int(t0*SR); i1 = min(n, i0 + int(dec*5*SR))
        if i0 >= n or i0 < 0: return
        x = np.arange(i1 - i0)/SR; e = np.exp(-x/dec); s = np.sin(2*np.pi*f*x*(1 + 0.5*np.exp(-x/0.03)))
        if noise: nz = np.convolve(np.random.randn(len(x)), np.ones(40)/40, "same"); s += noise*nz*4
        a[i0:i1] += s*e*amp
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
    hit(T("explain.") - 0.03, 48, 0.8, 0.35, noise=0.15)
    pad([73.4, 110.0], ls[3], ls[8], 0.06, 0.6, 0.6)
    hit(T("scar"), 50, 0.9, 0.3, noise=0.1); hit(T("same"), 40, 1.2, 0.5, noise=0.2)
    sweep(ls[8] - 0.1, 1.0, 300, 170, 0.06, noise=0.3); hit(ls[8], 36, 1.2, 0.5, noise=0.3)
    pad([41.2, 43.7], ls[8], ls[13], 0.1, 0.5, 0.6, trem=0.3)
    hit(T("face."), 36, 1.4, 0.6, noise=0.3)
    hit(T("drops") + 0.5, 180, 0.08, 0.5, noise=0.6); hit(T("drops") + 0.62, 160, 0.06, 0.25, noise=0.5)
    hb = ls[10]; per = 0.7
    while hb < ls[13]:
        hit(hb, 45, 0.08, 0.4); hit(hb + 0.18, 42, 0.08, 0.28); per = max(0.42, per*0.94); hb += per
    hit(T("doorway,"), 34, 1.6, 0.7, noise=0.35)
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
