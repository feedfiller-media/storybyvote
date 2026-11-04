def night(im, k=(0.6, 0.65, 0.9)):
    r, g, b, a = im.split()
    return Image.merge("RGBA", (r.point(lambda v: int(v*k[0])), g.point(lambda v: int(v*k[1])), b.point(lambda v: int(v*k[2])), a))

def bg_street_night():
    c = Cv(W, H, S, mode="RGB")
    for y in range(0, 1300, 10):
        k = y/1300; c.rect(0, y, W, y+10, (int(10+25*k), int(12+20*k), int(40+35*k)))
    random.seed(11)
    for _ in range(90): c.circ(random.uniform(0, W), random.uniform(0, 900), random.choice([2, 2, 3]), (250, 250, 230))
    c.circ(220, 520, 70, (240, 236, 205))
    c.el(500, 760, 1500, 1300, (24, 30, 46))                  # hill
    tx, ty = 860, 760                                          # radio tower
    c.line([(tx-60, 980), (tx, ty)], (60, 64, 80), 10); c.line([(tx+60, 980), (tx, ty)], (60, 64, 80), 10)
    for i in range(1, 6):
        y = ty + i*40; hw = 60*(y-ty)/220
        c.line([(tx-hw, y), (tx+hw, y)], (60, 64, 80), 5)
    for i, (x0, w, h) in enumerate([(-20, 220, 330), (200, 180, 420), (380, 230, 300), (600, 200, 380), (790, 300, 280)]):
        col = (30, 30, 50); c.rect(x0, 1260-h, x0+w, 1260, col)
        c.poly([(x0-10, 1260-h), (x0+w/2, 1260-h-90), (x0+w+10, 1260-h)], (26, 26, 44))
        for wy in range(1260-h+40, 1220, 90):
            for wx in range(x0+30, x0+w-40, 70):
                c.rect(wx, wy, wx+30, wy+40, (255, 214, 140) if (wx*7+wy) % 5 == 0 else (40, 42, 66))
    c.rect(0, 1260, W, 1310, (60, 60, 72)); c.rect(0, 1310, W, H, (40, 42, 50))
    for x in range(20, W, 180): c.rect(x, 1560, x+100, 1572, (110, 110, 120))
    return c.out(W, H)

def walker_sprites():
    out = []
    random.seed(5)
    cols = [(120, 90, 140), (90, 110, 150), (140, 110, 90), (100, 130, 110)]
    hairs = [(60, 40, 30), (150, 110, 70), (30, 30, 30), (120, 70, 40)]
    for ci in range(4):
        ph = []; hair = hairs[ci]
        for leg in (0, 1):
            c = Cv(200, 420, 2)
            a1, a2 = (20, -20) if leg else (-20, 20)
            for a in (a1, a2):
                x2 = 100 + 110*math.sin(math.radians(a)); c.line([(100, 260), (x2, 400)], (40, 40, 52), 26)
            c.rr(60, 120, 140, 290, 36, cols[ci])
            c.line([(115, 160), (190, 175)], cols[ci], 22); c.circ(192, 176, 13, SKIN)
            sleeper_head(c, 105, 70, 48, hair=hair)
            ph.append(night(c.out(200, 420), (0.55, 0.58, 0.85)))
        c = Cv(200, 420, 2)                                  # front view, looking up, eyes open
        c.line([(80, 270), (75, 400)], (40, 40, 52), 26); c.line([(120, 270), (125, 400)], (40, 40, 52), 26)
        c.rr(55, 120, 145, 290, 36, cols[ci]); c.line([(62, 150), (45, 280)], cols[ci], 22); c.line([(138, 150), (155, 280)], cols[ci], 22)
        c.circ(100, 70, 50, hair); c.circ(100, 80, 46, SKIN); c.el(56, 26, 144, 62, hair)
        for ex in (82, 118): c.el(ex-11, 60, ex+11, 78, (255, 255, 240)); c.circ(ex, 64, 5, (20, 20, 20))
        ph.append(night(c.out(200, 420), (0.55, 0.58, 0.85)))
        out.append(ph)
    return out
WALK = walker_sprites()
random.seed(9)
CROWD = [(random.uniform(-200, W), random.choice([1320, 1380, 1440, 1500, 1580, 1650]), random.randrange(4), random.uniform(0, 6)) for _ in range(26)]
CROWD.sort(key=lambda c: c[1])
TOWERGLOW = blur_layer(lambda c: c.circ(860, 755, 60, (255, 40, 40, 200)), 20)

