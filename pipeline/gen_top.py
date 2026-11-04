
# ================= v2: mood, camera, light, sound =================
import os
_al = json.load(open("timing_aligned.json"))
starts = [w[1] for w in _al]; ends = [w[2] for w in _al]
line_start = {}
for k, t_ in enumerate(tokens): line_start.setdefault(t_[1], starts[k])
def tok(word, n=0):
    ks = [k for k, t_ in enumerate(tokens) if t_[0] == word]; return ks[n]
TOTAL = dur + 1.4
SCENE_OF_LINE = ["bed_day", "bed_day", "mom", "mom", "street", "street", "street", "tv", "tv", "globe",
                 "sunset", "bed_night", "bed_night", "stairs", "stairs", "bed_end", "poll", "poll"]
CAP_Y = {"bed_day": 720, "mom": 760, "street": 760, "tv": 620, "globe": 520, "sunset": 620, "bed_night": 700, "stairs": 520, "bed_end": 700, "poll": 600}
ORDER = []
for s_ in SCENE_OF_LINE:
    if s_ not in ORDER: ORDER.append(s_)
def scene_start(name):
    return min(line_start[k] for k, s in enumerate(SCENE_OF_LINE) if s == name) - 0.05
def scene_len(name):
    i = ORDER.index(name)
    return (scene_start(ORDER[i+1]) if i+1 < len(ORDER) else TOTAL) - scene_start(name)
def cur_line(t):
    li = 0
    for k in range(len(SCRIPT)):
        if line_start[k] <= t + 0.05: li = k
    return li
def ease(p): p = max(0, min(1, p)); return p*p*(3-2*p)
def flick(t, seed=0):
    return 0.5 + 0.22*math.sin(t*7.3+seed) + 0.15*math.sin(t*13.1+seed*2) + 0.13*math.sin(t*23.7+seed*3)

# ---- Max sprite with gaze + breathing ----
_sp2 = {}
def sprite2(expr, eyes, mouth, arms, gaze, scale, night, sq):
    key = (expr, eyes, mouth, arms, gaze, round(scale, 3), night, round(sq, 3))
    if key not in _sp2:
        bk = (expr, eyes, mouth, arms, gaze)
        if bk not in _sp2: _sp2[bk] = make_max(*bk)
        im = _sp2[bk]
        if night:
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (r.point(lambda v: int(v*0.55)), g.point(lambda v: int(v*0.62)), b.point(lambda v: int(v*0.9)), a))
        _sp2[key] = im.resize((int(600*scale/sq**0.5), int(900*scale*sq)), Image.LANCZOS)
    return _sp2[key]

def put_max(fr, x, feet, scale, expr, arms, t, local, night=False, talk=False, gaze=0, eyes=None, walk=0.0, tremble=0.0, bob=1.0):
    if eyes is None: eyes = not ((t % 3.7) < 0.12)
    mouth = (talk and rms(t) > 0.04) or expr == "yawn"
    sq = 1 + 0.012*math.sin(t*2*math.pi*0.35)              # breathing
    if local < 0.3: sq *= 1 - 0.1*math.sin(local/0.3*math.pi)  # squash on entry
    sq = round(sq*200)/200
    g = round(gaze*2)/2
    sp = sprite2(expr, eyes, mouth, arms, g, scale, night, sq)
    by = math.sin(t*2*math.pi*0.5)*4*scale*bob
    if walk > 0: by -= abs(math.sin(t*math.pi*4))*28*scale*walk
    x += math.sin(t*47)*tremble*3 + math.sin(t*31)*tremble*2
    sh = Image.new("RGBA", (int(320*scale), int(60*scale)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([0, 0, sh.width-1, sh.height-1], fill=(0, 0, 0, 80 if not night else 110))
    fr.alpha_composite(sh, (int(x - sh.width/2), int(feet - sh.height/2)))
    fr.alpha_composite(sp, (int(x - sp.width/2), int(feet - sp.height + by + 4*scale)))

# ---- layers ----
def blur_layer(draw_fn, rad):
    c = Cv(W, H, 1); draw_fn(c); return c.im.filter(ImageFilter.GaussianBlur(rad))
def vignette(strength, col=(0, 0, 0)):
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx-W/2)/(W*0.62))**2 + ((yy-H*0.55)/(H*0.6))**2)
    a = (np.clip((r-0.55)/0.6, 0, 1)**1.6*255*strength).astype(np.uint8)
    im = np.zeros((H, W, 4), np.uint8); im[..., 0], im[..., 1], im[..., 2] = col; im[..., 3] = a
    return Image.fromarray(im, "RGBA")
def tint(col, a):
    return Image.new("RGBA", (W, H), col + (a,))
def alpha_mul(im, k):
    k = max(0, min(1, k))
    if k >= 0.999: return im
    r, g, b, a = im.split(); return Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v*k))))
_am = {}
def alpha_q(name, im, k):
    q = round(max(0, min(1, k))*20)/20
    if (name, q) not in _am: _am[(name, q)] = alpha_mul(im, q)
    return _am[(name, q)]

print("drawing layers")
VIG = {"soft": vignette(0.45), "mid": vignette(0.7), "hard": vignette(1.0), "red": vignette(0.8, (110, 0, 10))}
RAYS = blur_layer(lambda c: c.poly([(112, 452), (448, 452), (980, 1700), (330, 1700)], (255, 236, 170, 70)), 35)
MOONBEAM = blur_layer(lambda c: c.poly([(112, 452), (448, 452), (760, 1720), (260, 1720)], (150, 175, 255, 55)), 35)
DOORGLOW = blur_layer(lambda c: (c.el(330, 560, 750, 1150, (255, 190, 110, 150)), c.poly([(420, 1050), (660, 1050), (900, 1750), (180, 1750)], (255, 180, 100, 45))), 45)
TVGLOW = blur_layer(lambda c: c.el(-100, 700, 900, 1500, (120, 170, 255, 120)), 70)
SUNGLOW = blur_layer(lambda c: c.circ(780, 1000, 330, (255, 160, 90, 120)), 90)
MOONGLOW = blur_layer(lambda c: c.circ(360, 540, 150, (230, 235, 255, 90)), 40)
random.seed(7)
DUST = [(random.uniform(150, 900), random.uniform(500, 1650), random.uniform(0, 6.28), random.uniform(2, 5)) for _ in range(40)]
LEAVES = [(random.uniform(0, W), random.uniform(1280, 1650), random.uniform(0, 6.28), random.choice([(200, 140, 60), (170, 110, 50), (210, 170, 70)])) for _ in range(7)]
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0, 6.28), random.choice([2, 2, 3, 4])) for _ in range(170)]

