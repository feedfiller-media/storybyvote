# ---------------- HUD + captions ----------------
def hud(fr, t):
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([60, 245, 330, 360], 28, fill=(0, 0, 0, 150))
    d.rounded_rectangle([350, 245, 1020, 360], 28, fill=(0, 0, 0, 150))
    d.text((195, 275), "DAY", font=font(30), fill=(200, 200, 200), anchor="mm")
    d.text((195, 323), "1", font=font(54), fill=(255, 255, 255), anchor="mm")
    d.text((685, 275), "PEOPLE AWAKE", font=font(30), fill=(200, 200, 200), anchor="mm")
    t9 = line_start[9]
    if t < t9: val, col, sz = "?", (255, 255, 255), 54
    elif t < t9 + 1.4:
        p = (t-t9)/1.4; n = int(8_100_000_000*(1-p)**3) + 1
        val, col, sz = f"{n:,}", (255, 90, 90), 50
    else:
        val, col = "1", (255, 90, 90); sz = 54 * (1 + 0.25*max(0, 1-(t-t9-1.4)/0.3))
    d.text((685, 323), val, font=font(sz), fill=col, anchor="mm")

def captions(fr, t, y):
    d = ImageDraw.Draw(fr)
    ci = None
    for n, ch in enumerate(chunks):
        s0 = starts[ch[0]]
        nxt = starts[chunks[n+1][0]] if n+1 < len(chunks) else ends[ch[-1]] + 1.5
        e = min(nxt, ends[ch[-1]] + 0.9)
        if s0 - 0.05 <= t < e: ci = n
    if ci is None: return
    ch = chunks[ci]; k = min(1, (t - starts[ch[0]] + 0.05)/0.12)
    sz = 92*(0.85 + 0.15*k); f = font(sz)
    words = [tokens[q][0].upper() for q in ch]
    widths = [d.textlength(w + " ", font=f) for w in words]
    lines = [[0]]; lw = widths[0]
    for q in range(1, len(words)):
        if lw + widths[q] > 860: lines.append([q]); lw = widths[q]
        else: lines[-1].append(q); lw += widths[q]
    for li_, ln in enumerate(lines):
        tw = sum(widths[q] for q in ln) - d.textlength(" ", font=f)
        x = 525 - tw/2; yy = y + (li_ - (len(lines)-1)/2)*sz*1.1
        for q in ln:
            active = starts[ch[q]] <= t + 0.03 and (q == len(ch)-1 or starts[ch[q+1]] > t + 0.03)
            d.text((x, yy), words[q], font=f, fill=(255, 214, 60) if active else (255, 255, 255), anchor="lm",
                   stroke_width=8, stroke_fill=(0, 0, 0))
            x += widths[q]

